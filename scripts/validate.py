#!/usr/bin/env python3
"""Validate generated HTML, local links and image files."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib.parse import urlsplit

from bs4 import BeautifulSoup
from PIL import Image

from image_utils import resolve_local_image

ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []


def check_html(path: Path) -> None:
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    if not soup.title or not soup.title.get_text(strip=True):
        ERRORS.append(f"{path.relative_to(ROOT)}: <title> ausente")
    h1 = soup.find_all("h1")
    if len(h1) != 1:
        ERRORS.append(f"{path.relative_to(ROOT)}: esperado 1 h1, encontrado {len(h1)}")

    ids = [tag.get("id") for tag in soup.find_all(attrs={"id": True})]
    if len(ids) != len(set(ids)):
        ERRORS.append(f"{path.relative_to(ROOT)}: IDs HTML duplicados")

    for tag, attr in [("a", "href"), ("img", "src"), ("link", "href"), ("script", "src")]:
        for node in soup.find_all(tag):
            value = node.get(attr)
            if not value or value.startswith(("http://", "https://", "mailto:", "tel:", "data:", "#")):
                continue
            clean = urlsplit(value).path
            if not clean:
                continue
            target = (path.parent / clean).resolve()
            try:
                target.relative_to(ROOT.resolve())
            except ValueError:
                ERRORS.append(f"{path.relative_to(ROOT)}: caminho sai do projeto: {value}")
                continue
            if not target.exists():
                ERRORS.append(f"{path.relative_to(ROOT)}: referência local inexistente: {value}")


def check_images() -> None:
    data = json.loads((ROOT / "data" / "jogos.json").read_text(encoding="utf-8"))
    for game in data:
        if game["image"].startswith(("http://", "https://")):
            continue
        path = resolve_local_image(ROOT / "images", game["image"])
        if path is None:
            ERRORS.append(
                f"Imagem ausente ou formato não suportado: images/{game['image']}"
            )
            continue
        if path.suffix.lower() == ".svg":
            if "<svg" not in path.read_text(encoding="utf-8")[:500]:
                ERRORS.append(f"SVG inválido: {path.relative_to(ROOT)}")
            continue
        try:
            with Image.open(path) as image:
                image.verify()
        except Exception as exc:
            ERRORS.append(f"Imagem inválida {path.relative_to(ROOT)}: {exc}")


def main() -> int:
    for html in [ROOT / "index.html", ROOT / "404.html", *sorted((ROOT / "pages").glob("*.html"))]:
        check_html(html)
    check_images()
    if ERRORS:
        print("Falhas encontradas:")
        for error in ERRORS:
            print(f"- {error}")
        return 1
    print("Validação concluída sem erros.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
