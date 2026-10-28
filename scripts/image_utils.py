"""Helpers for resolving local catalog images across common file formats."""
from __future__ import annotations

from pathlib import Path

SUPPORTED_IMAGE_EXTENSIONS = (
    ".webp", ".png", ".jpg", ".jpeg", ".svg", ".gif", ".bmp"
)
_EXTENSION_PRIORITY = {ext: index for index, ext in enumerate(SUPPORTED_IMAGE_EXTENSIONS)}


def resolve_local_image(images_dir: Path, image_value: str) -> Path | None:
    """Find an image by exact filename or by its base name if the extension changed.

    A catalog entry containing puzzle.webp also resolves to puzzle.jpg when that
    is the available file. Extensionless values such as puzzle are supported too.
    Remote URLs should be handled by the caller.
    """
    relative = Path(image_value)
    if relative.is_absolute() or ".." in relative.parts:
        return None

    direct = images_dir / relative
    if direct.is_file() and direct.suffix.lower() in SUPPORTED_IMAGE_EXTENSIONS:
        return direct

    stem = relative.stem if relative.suffix else relative.name
    if not stem:
        return None

    matches = [
        path for path in images_dir.iterdir()
        if path.is_file()
        and path.stem.casefold() == stem.casefold()
        and path.suffix.casefold() in SUPPORTED_IMAGE_EXTENSIONS
    ]
    if not matches:
        return None

    return sorted(
        matches,
        key=lambda path: (
            _EXTENSION_PRIORITY.get(path.suffix.lower(), len(_EXTENSION_PRIORITY)),
            path.name.casefold(),
        ),
    )[0]
