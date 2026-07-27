"""Adaptive Scenario Generator (F3).

Produce a challenge tuned to the learner's current level (1–4), grounded in a
specific Atomic Note. Output is validated JSON (N4) so the verification layer can
consume it deterministically.
"""

from __future__ import annotations

import re

from ..llm import get_provider
from ..llm.provider import LLMProvider
from ..memory.vault import load_vault

# Per-level intent, straight from SRD F3.
LEVELS = {
    1: ("Recognition", "Định nghĩa, bản chất, First-Principles: 'X là gì và X KHÔNG "
                        "phải là gì?'. Không hỏi code."),
    2: ("Operation", "Yêu cầu viết code/config chạy đúng cho bài toán tiêu chuẩn "
                      "(happy path)."),
    3: ("Anomaly Detection", "Đưa một đoạn code có bug ngầm (race condition, deadlock, "
                             "memory leak, security flaw) HOẶC đúng nhưng vi phạm nguyên "
                             "lý; yêu cầu người học phát hiện và giải thích."),
    4: ("System Architecture", "Thử thách thiết kế hệ thống kèm ràng buộc ngặt nghèo "
                               "(RAM, latency, concurrency limit)."),
}

CHALLENGE_SCHEMA = {
    "type": "object",
    "properties": {
        "level": {"type": "integer", "minimum": 1, "maximum": 4},
        "kind": {"type": "string"},
        "prompt": {"type": "string"},
        "constraints": {"type": "array", "items": {"type": "string"}},
        "evaluation": {"type": "string"},
    },
    "required": ["level", "kind", "prompt"],
    "additionalProperties": True,
}

_SYSTEM = ("You are a rigorous senior mentor generating a single challenge. Be "
           "concrete and demanding. Answer in the note's language.")


def parse_level(note_meta: dict) -> int:
    m = re.search(r"Level\s*([1-4])", str(note_meta.get("current_level", "")))
    return int(m.group(1)) if m else 1


def build_prompt(note, level: int) -> str:
    name, guidance = LEVELS[level]
    return (f"Atomic note '{note.meta.get('topic', note.name)}':\n{note.body.strip()}\n\n"
            f"Generate a Level {level} ({name}) challenge. {guidance}")


def generate(note, level: int | None = None, provider: LLMProvider | None = None) -> dict:
    level = level or parse_level(note.meta)
    if level not in LEVELS:
        return {"error": True, "message": f"level must be 1..4, got {level}"}
    provider = provider or get_provider()
    challenge = provider.structured(build_prompt(note, level), CHALLENGE_SCHEMA, system=_SYSTEM)
    # Coerce empty/placeholder fields (e.g. from the stub provider) to real values.
    if not challenge.get("level"):
        challenge["level"] = level
    if not challenge.get("kind"):
        challenge["kind"] = LEVELS[level][0]
    return {"note": note.name, "level": level, "provider": provider.name, "challenge": challenge}


def scenario_for_vault(vault_dir: str, note_name: str, level: int | None = None,
                       provider: LLMProvider | None = None) -> dict:
    notes = {n.name: n for n in load_vault(vault_dir)}
    note = notes.get(note_name)
    if note is None:
        return {"error": True, "message": f"note '{note_name}' not found"}
    return generate(note, level=level, provider=provider)
