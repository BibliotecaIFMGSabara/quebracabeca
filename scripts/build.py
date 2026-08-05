#!/usr/bin/env python3
"""Generate the static catalog from data/jogos.json.

Run from the repository root:
    python scripts/build.py
"""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "jogos.json"
TEMPLATES = ROOT / "templates"
PAGES = ROOT / "pages"


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFD", text)
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    return re.sub(r"\s+", " ", text.lower()).strip()


def load_games() -> list[dict[str, Any]]:
    games = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    ids = [game["id"] for game in games]
    if len(ids) != len(set(ids)):
        raise ValueError("Há IDs de jogos duplicados em data/jogos.json")

    required = {
        "id", "title", "subtitle", "summary", "image", "image_alt",
        "category", "category_label", "players", "time", "difficulty",
        "mode", "tags", "objective", "intro", "steps", "skills",
        "mediation", "adaptations", "care", "sources"
    }
    for game in games:
        missing = required - set(game)
        if missing:
            raise ValueError(f"{game.get('id', '<sem id>')}: campos ausentes: {sorted(missing)}")
        image = ROOT / "images" / game["image"]
        if not image.exists():
            raise FileNotFoundError(f"Imagem ausente para {game['id']}: {image}")
        search_parts = [
            game["title"], game.get("catalog_alias", ""), game["subtitle"],
            game["summary"], game["category_label"], *game["tags"],
            *(skill["title"] for skill in game["skills"])
        ]
        game["search_text"] = normalize(" ".join(search_parts))
    return games


def json_script(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def related_for(game: dict[str, Any], games: list[dict[str, Any]], limit: int = 3) -> list[dict[str, Any]]:
    same = [g for g in games if g["id"] != game["id"] and g["category"] == game["category"]]
    other = [g for g in games if g["id"] != game["id"] and g["category"] != game["category"]]
    return (same + other)[:limit]


def build() -> None:
    games = load_games()
    env = Environment(
        loader=FileSystemLoader(TEMPLATES),
        autoescape=select_autoescape(["html", "xml"]),
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
    )

    categories: list[dict[str, str]] = []
    seen_categories: set[str] = set()
    for game in games:
        if game["category"] not in seen_categories:
            categories.append({"id": game["category"], "label": game["category_label"]})
            seen_categories.add(game["category"])

    home_schema = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "Acervo de Jogos e Quebra-Cabeças",
        "description": "Catálogo educativo de jogos de estratégia, habilidade, lógica e montagem.",
        "mainEntity": {
            "@type": "ItemList",
            "numberOfItems": len(games),
            "itemListElement": [
                {"@type": "ListItem", "position": i, "name": g["title"], "url": f"pages/{g['id']}.html"}
                for i, g in enumerate(games, start=1)
            ]
        }
    }
    index_html = env.get_template("index.html.j2").render(
        games=games,
        categories=categories,
        json_ld=json_script(home_schema),
    )
    (ROOT / "index.html").write_text(index_html, encoding="utf-8")

    PAGES.mkdir(exist_ok=True)
    game_template = env.get_template("game.html.j2")
    expected_pages: set[str] = set()
    for game in games:
        expected_pages.add(f"{game['id']}.html")
        game_schema = {
            "@context": "https://schema.org",
            "@type": "CreativeWork",
            "name": game["title"],
            "description": game["summary"],
            "learningResourceType": "Guia de jogo e mediação",
            "educationalUse": "Experimentação, mediação e aprendizagem baseada em jogos",
            "isPartOf": {"@type": "CollectionPage", "name": "Acervo de Jogos e Quebra-Cabeças", "url": "../index.html"},
        }
        html = game_template.render(
            game=game,
            related_games=related_for(game, games),
            json_ld=json_script(game_schema),
        )
        (PAGES / f"{game['id']}.html").write_text(html, encoding="utf-8")

    for page in PAGES.glob("*.html"):
        if page.name not in expected_pages:
            page.unlink()

    print(f"Site gerado: {len(games)} páginas de jogos e página inicial.")


if __name__ == "__main__":
    build()
