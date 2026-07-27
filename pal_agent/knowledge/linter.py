"""Semantic Graph Linter (F2.3).

Find Isolated Nodes (orphan notes with no edges) and propose links to the most
related notes. Similarity here is lexical (token Jaccard over topic + body) — fully
offline and deterministic; swapping in vector/embedding similarity is a later, drop-
in upgrade behind the same ``score`` function.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from ..memory.graph import KnowledgeGraph
from ..memory.vault import Note, load_vault

_TOKEN = re.compile(r"\w+", re.UNICODE)
_STOP = {"the", "a", "an", "and", "or", "of", "to", "in", "is", "for", "với", "và",
         "là", "các", "một", "cho", "khi", "có"}


def _tokens(text: str) -> set[str]:
    return {t.lower() for t in _TOKEN.findall(text) if len(t) > 2 and t.lower() not in _STOP}


def score(a: Note, b: Note) -> float:
    """Jaccard similarity of two notes' token sets (0..1)."""
    ta, tb = _tokens(f"{a.meta.get('topic', a.name)} {a.body}"), _tokens(f"{b.meta.get('topic', b.name)} {b.body}")
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


@dataclass
class Suggestion:
    orphan: str
    target: str
    score: float


def suggest_for_orphan(orphan: Note, others: list[Note], top_k: int = 3,
                       threshold: float = 0.02) -> list[Suggestion]:
    ranked = sorted(((o.name, score(orphan, o)) for o in others if o.name != orphan.name),
                    key=lambda x: x[1], reverse=True)
    return [Suggestion(orphan.name, name, round(sc, 4))
            for name, sc in ranked[:top_k] if sc >= threshold]


def lint_vault(vault_dir: str, top_k: int = 3) -> dict:
    """Return orphan notes and, for each, ranked link suggestions."""
    notes = load_vault(vault_dir)
    by_name = {n.name: n for n in notes}
    graph = KnowledgeGraph.from_notes(notes)
    orphan_names = graph.orphans()
    result = []
    for name in orphan_names:
        orphan = by_name.get(name)
        if orphan is None:
            continue
        suggestions = suggest_for_orphan(orphan, notes, top_k=top_k)
        result.append({"orphan": name,
                       "suggestions": [{"target": s.target, "score": s.score}
                                       for s in suggestions]})
    return {"orphans": orphan_names, "suggestions": result}
