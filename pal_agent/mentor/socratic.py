"""Socratic Feedback Loop (F4.3).

When a learner is wrong, do NOT hand over the answer and do NOT flatter. Return a
probing question that points at the root concept they're missing. Output is
validated JSON (N4); the question is guaranteed to end with '?'.
"""

from __future__ import annotations

from ..llm import get_provider
from ..llm.provider import LLMProvider

FEEDBACK_SCHEMA = {
    "type": "object",
    "properties": {
        "question": {"type": "string"},
        "focus_concept": {"type": "string"},
        "hint_only": {"type": "boolean"},
    },
    "required": ["question", "focus_concept"],
    "additionalProperties": True,
}

_SYSTEM = ("You are a Socratic mentor. The learner's answer is wrong or incomplete. "
           "Do NOT reveal the correct answer. Do NOT praise. Respond with ONE probing "
           "question that leads them to the root concept they are missing. Answer in "
           "the learner's language.")


def _ensure_question(text: str) -> str:
    text = (text or "").strip()
    if not text:
        return "Điều gì trong khái niệm gốc khiến câu trả lời này chưa đúng?"
    return text if text.endswith("?") else text.rstrip(".") + "?"


def probe(concept: str, wrong_answer: str, provider: LLMProvider | None = None) -> dict:
    provider = provider or get_provider()
    prompt = (f"Concept under study: {concept}\n"
              f"Learner's (incorrect) answer: {wrong_answer}\n"
              f"Ask one probing question targeting the gap.")
    result = provider.structured(prompt, FEEDBACK_SCHEMA, system=_SYSTEM)
    result["question"] = _ensure_question(result.get("question", ""))
    result.setdefault("focus_concept", concept)
    result["provider"] = provider.name
    return result
