"""Auto-Atomization ingestion (F2.1).

Read raw docs from an ``/Inbox`` directory, split each into Atomic Notes (one
concept per ``.md``, per F1.2), and auto-insert ``[[WikiLinks]]`` to notes already
in the graph so new knowledge connects instead of landing as orphans. Splitting is
heuristic (by Markdown heading) — deterministic and offline; an LLM pass can refine
it later via the model layer.
"""

from __future__ import annotations

import datetime
import os
import re

from ..memory.state import render_note
from ..memory.vault import load_vault

_HEADING = re.compile(r"^#{1,6}\s+(.*\S)\s*$")


def slug(title: str) -> str:
    """Note stem from a title: ``"Golang Basics"`` -> ``"Golang_Basics"``."""
    s = re.sub(r"[^\w]+", "_", title.strip(), flags=re.UNICODE)
    return s.strip("_") or "Untitled"


def atomize(raw: str) -> list[tuple[str, str]]:
    """Split raw text into ``(title, body)`` sections by Markdown heading."""
    sections: list[tuple[str, str]] = []
    title, body = None, []
    for line in raw.splitlines():
        m = _HEADING.match(line)
        if m:
            if title is not None:
                sections.append((title, "\n".join(body).strip()))
            title, body = m.group(1).strip(), []
        elif title is None:
            if line.strip():  # preamble before any heading
                title, body = "Untitled", [line]
        else:
            body.append(line)
    if title is not None:
        sections.append((title, "\n".join(body).strip()))
    return sections


def auto_link(body: str, known_stems: set[str]) -> str:
    """Wrap the first mention of each known note (stem or spaced title) in ``[[ ]]``."""
    for stem in sorted(known_stems, key=len, reverse=True):
        spaced = stem.replace("_", " ")
        alts = sorted({re.escape(stem), re.escape(spaced)}, key=len, reverse=True)
        pattern = re.compile(r"(?<!\[\[)\b(?:" + "|".join(alts) + r")\b(?!\]\])")
        body = pattern.sub(f"[[{stem}]]", body, count=1)
    return body


def ingest_inbox(inbox_dir: str, vault_dir: str, subdir: str = "_ingested",
                 today: str | None = None) -> list[str]:
    """Atomize every doc in ``inbox_dir`` into ``vault_dir/subdir``. Returns paths."""
    if not os.path.isdir(inbox_dir):
        raise FileNotFoundError(f"inbox not found: {inbox_dir}")
    existing = {n.name for n in load_vault(vault_dir)} if os.path.isdir(vault_dir) else set()
    day = today or datetime.date.today().isoformat()

    docs = []
    for fn in sorted(os.listdir(inbox_dir)):
        if fn.endswith((".md", ".txt")):
            with open(os.path.join(inbox_dir, fn), encoding="utf-8") as f:
                docs.extend(atomize(f.read()))

    new_stems = {slug(t) for t, _ in docs}
    known = existing | new_stems
    out_dir = os.path.join(vault_dir, subdir)
    os.makedirs(out_dir, exist_ok=True)

    created = []
    for title, body in docs:
        stem = slug(title)
        linked = auto_link(body, known - {stem})
        meta = {"topic": title, "current_level": "Level 1: Recognition",
                "mastery_score": 0.0, "prerequisites": [], "last_evaluated": day}
        path = os.path.join(out_dir, f"{stem}.md")
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(render_note(meta, linked))
        created.append(path)
    return created
