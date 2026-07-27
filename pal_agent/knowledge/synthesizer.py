"""Dynamic Narrative Synthesizer — Read Mode (F2.2).

Gather a topic's Atomic Note plus its graph neighbours and ask the model to weave
them into one coherent explanation (with examples/analogies). Strictly read-only:
source notes are never modified — the narrative is generated on the fly.
"""

from __future__ import annotations

from ..llm import get_provider
from ..llm.provider import LLMProvider
from ..memory.graph import KnowledgeGraph
from ..memory.vault import load_vault

_SYSTEM = ("You are a senior mentor. Weave the provided atomic notes into ONE "
           "coherent, well-structured explanation with concrete examples and an "
           "analogy. Do not invent facts beyond the notes. Answer in the notes' "
           "language.")


def _find(notes, topic):
    lowered = topic.lower()
    for n in notes:
        if n.name.lower() == lowered or str(n.meta.get("topic", "")).lower() == lowered:
            return n
    # loose contains-match as a fallback
    for n in notes:
        if lowered in n.name.lower() or lowered in str(n.meta.get("topic", "")).lower():
            return n
    return None


def gather(vault_dir: str, topic: str):
    """Return (root_note, related_notes) for a topic, or (None, [])."""
    notes = load_vault(vault_dir)
    root = _find(notes, topic)
    if root is None:
        return None, []
    graph = KnowledgeGraph.from_notes(notes)
    by_name = {n.name: n for n in notes}
    related = [by_name[name] for name in graph.neighbors(root.name) if name in by_name]
    return root, related


def build_prompt(root, related) -> str:
    parts = [f"# Topic: {root.meta.get('topic', root.name)}",
             f"## Core note ({root.name})", root.body.strip()]
    for r in related:
        parts.append(f"## Related: {r.meta.get('topic', r.name)} ({r.name})")
        parts.append(r.body.strip())
    return "\n\n".join(parts)


def synthesize(vault_dir: str, topic: str, provider: LLMProvider | None = None) -> dict:
    root, related = gather(vault_dir, topic)
    if root is None:
        return {"error": True, "message": f"topic '{topic}' not found in vault"}
    provider = provider or get_provider()
    prompt = build_prompt(root, related)
    narrative = provider.complete(prompt, system=_SYSTEM)
    return {"topic": root.meta.get("topic", root.name), "root": root.name,
            "sources": [root.name] + [r.name for r in related],
            "provider": provider.name, "narrative": narrative}
