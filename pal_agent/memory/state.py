"""Update an Atomic Note's YAML frontmatter without corrupting it (F1.3, N3).

The mentor writes back progress (``mastery_score``, ``current_level``, new
``weaknesses``) after every challenge. N3 requires this never mangle the note:
the body is preserved byte-for-byte, untouched frontmatter keys keep their value
and order, and only valid YAML is written. All writes go through here.
"""

from __future__ import annotations

import os

import yaml

from .vault import parse_frontmatter


def _dump_frontmatter(meta: dict) -> str:
    return yaml.safe_dump(meta, sort_keys=False, allow_unicode=True,
                          default_flow_style=False).rstrip("\n")


def render_note(meta: dict, body: str) -> str:
    """Serialize (meta, body) back to an Obsidian note string."""
    if not meta:
        return body if body.endswith("\n") else body + "\n"
    body = body.lstrip("\n")
    return f"---\n{_dump_frontmatter(meta)}\n---\n\n{body}".rstrip("\n") + "\n"


def update_note_state(path: str, updates: dict | None = None,
                      add_weaknesses: list[str] | None = None,
                      add_strengths: list[str] | None = None) -> dict:
    """Merge ``updates`` into a note's frontmatter and append list items.

    Returns the new meta dict. Raises FileNotFoundError if the note is missing.
    Body is preserved verbatim; existing keys keep their order (N3).
    """
    if not os.path.isfile(path):
        raise FileNotFoundError(f"note not found: {path}")
    with open(path, encoding="utf-8") as f:
        text = f.read()
    meta, body = parse_frontmatter(text)
    if not isinstance(meta, dict):
        meta = {}

    for key, value in (updates or {}).items():
        meta[key] = value

    for key, extra in (("weaknesses", add_weaknesses), ("strengths", add_strengths)):
        if not extra:
            continue
        current = meta.get(key)
        if not isinstance(current, list):
            current = []
        for item in extra:
            if item not in current:
                current.append(item)
        meta[key] = current

    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(render_note(meta, body))
    return meta
