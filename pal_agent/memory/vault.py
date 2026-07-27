"""Parse an Obsidian Vault into structured Atomic Notes (F1.1, minimal).

Reads every ``*.md`` file under a vault directory, extracts its YAML-style
frontmatter and its ``[[WikiLinks]]``. This is a deliberately small, stdlib-only
frontmatter reader covering the subset the PAL-Agent schema uses (scalars +
simple string lists) — see the backlog for the PyYAML upgrade. It never raises on
malformed input; a note with no frontmatter still parses (empty dict).
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field

_WIKILINK = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]*)?\]\]")
_SCALAR = re.compile(r"^([A-Za-z_][\w-]*):\s*(.*)$")
_LIST_ITEM = re.compile(r"^\s*-\s*(.*\S)\s*$")


def _coerce(value: str):
    """Turn a scalar frontmatter string into str / int / float."""
    v = value.strip().strip('"').strip("'")
    if not v:
        return ""
    try:
        return int(v)
    except ValueError:
        pass
    try:
        return float(v)
    except ValueError:
        return v


def _strip_wikilink(item: str) -> str:
    """`[[Golang_Basics]]` -> `Golang_Basics`; plain text passes through."""
    m = _WIKILINK.search(item)
    return m.group(1).strip() if m else item.strip().strip('"').strip("'")


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Split leading ``---`` frontmatter from the body. Returns (meta, body)."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return {}, text

    meta: dict = {}
    current_list_key = None
    for raw in lines[1:end]:
        if not raw.strip():
            continue
        item = _LIST_ITEM.match(raw)
        if item and current_list_key:
            meta[current_list_key].append(_strip_wikilink(item.group(1)))
            continue
        scalar = _SCALAR.match(raw)
        if scalar:
            key, val = scalar.group(1), scalar.group(2).strip()
            if val == "":
                # block list follows on subsequent `- item` lines
                current_list_key = key
                meta[key] = []
            elif val.startswith("[") and val.endswith("]"):
                # inline list, e.g. `prerequisites: []` or `tags: [a, b]`
                current_list_key = None
                inner = val[1:-1].strip()
                meta[key] = [_strip_wikilink(x) for x in inner.split(",") if x.strip()]
            else:
                current_list_key = None
                meta[key] = _coerce(val)
    body = "\n".join(lines[end + 1:])
    return meta, body


def extract_wikilinks(text: str) -> list[str]:
    """All distinct ``[[Target]]`` names in order of first appearance."""
    seen, out = set(), []
    for m in _WIKILINK.finditer(text):
        name = m.group(1).strip()
        if name and name not in seen:
            seen.add(name)
            out.append(name)
    return out


@dataclass
class Note:
    name: str                       # file stem, e.g. "State_Concurrency"
    path: str
    meta: dict = field(default_factory=dict)
    body: str = ""
    links: list[str] = field(default_factory=list)         # wikilinks in the body
    prerequisites: list[str] = field(default_factory=list)  # from frontmatter

    @property
    def edges(self) -> list[str]:
        """Outgoing edges = links (body) + prerequisites (frontmatter), deduped."""
        seen, out = set(), []
        for t in self.prerequisites + self.links:
            if t and t not in seen:
                seen.add(t)
                out.append(t)
        return out


def load_note(path: str) -> Note:
    with open(path, encoding="utf-8") as f:
        text = f.read()
    meta, body = parse_frontmatter(text)
    raw_prereqs = meta.get("prerequisites", [])
    if not isinstance(raw_prereqs, list):  # defensive: malformed frontmatter
        raw_prereqs = []
    prereqs = [str(p) for p in raw_prereqs if p]
    return Note(name=os.path.splitext(os.path.basename(path))[0], path=os.path.abspath(path),
                meta=meta, body=body, links=extract_wikilinks(body), prerequisites=prereqs)


def load_vault(vault_dir: str) -> list[Note]:
    """Load every ``*.md`` note under ``vault_dir`` (recursively), sorted by name.

    The Activity Ledger (``Activity_Ledger.md``) is skipped — it is an append-only
    log, not an atomic concept note.
    """
    if not os.path.isdir(vault_dir):
        raise FileNotFoundError(f"vault not found: {vault_dir}")
    notes = []
    for root, _dirs, files in os.walk(vault_dir):
        for fn in files:
            if fn.endswith(".md") and fn != "Activity_Ledger.md":
                notes.append(load_note(os.path.join(root, fn)))
    return sorted(notes, key=lambda n: n.name)
