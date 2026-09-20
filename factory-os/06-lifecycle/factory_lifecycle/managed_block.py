from __future__ import annotations

from pathlib import Path

from .fsutil import atomic_write_text

BEGIN = "<!-- CODEX_FACTORY_OS:BEGIN -->"
END = "<!-- CODEX_FACTORY_OS:END -->"


def has_block(text: str) -> bool:
    return BEGIN in text and END in text


def strip_block(text: str) -> str:
    if BEGIN not in text or END not in text:
        return text
    before, rest = text.split(BEGIN, 1)
    _managed, after = rest.split(END, 1)
    value = (before.rstrip() + "\n\n" + after.lstrip()).strip()
    return (value + "\n") if value else ""


def apply_block(path: Path, body: str) -> bool:
    old = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
    clean = strip_block(old)
    managed = f"{BEGIN}\n{body.strip()}\n{END}"
    new = managed + ("\n\n" + clean.strip() if clean.strip() else "") + "\n"
    changed = new != old
    if changed:
        atomic_write_text(path, new)
    return changed


def remove_block(path: Path) -> bool:
    if not path.exists():
        return False
    old = path.read_text(encoding="utf-8", errors="replace")
    new = strip_block(old)
    if new == old:
        return False
    if new.strip():
        atomic_write_text(path, new)
    else:
        path.unlink()
    return True
