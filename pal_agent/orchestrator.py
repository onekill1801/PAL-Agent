"""Agent Core Orchestrator — the Socratic Adaptive Learning Loop.

Wires the layers into one cycle (SRD 2.2): hydrate a note -> generate a level-tuned
challenge -> verify the learner's response -> update mastery/level + log a milestone
on success, or return a Socratic probe + record the weakness on failure. A
deliberately small state machine rather than a heavyweight framework — the modules
it calls are where the real work lives.
"""

from __future__ import annotations

import os

from .llm import get_provider
from .llm.provider import LLMProvider
from .memory import ledger, state
from .mentor import scenarios, socratic
from .mentor.scenarios import parse_level
from .memory.vault import load_note, load_vault
from .verify.sandbox import run_code

MAX_LEVEL = 4
PROMOTE_BONUS = 10.0


def _find_note_path(vault: str, name: str) -> str:
    for root, _dirs, files in os.walk(vault):
        if f"{name}.md" in files:
            return os.path.join(root, f"{name}.md")
    raise FileNotFoundError(f"note '{name}' not found under {vault}")


def run_cycle(vault: str, note_name: str, *, answer: str = "", code: str = "",
              language: str = "python", passed: bool | None = None,
              use_docker: bool = False, provider: LLMProvider | None = None,
              today: str | None = None) -> dict:
    """Run one adaptive learning cycle. Returns a transcript dict.

    Evaluation precedence: run ``code`` in the sandbox if given; else use the
    explicit ``passed`` flag (human judgement for concept levels); else the cycle
    only *generates* a challenge and awaits evaluation.
    """
    provider = provider or get_provider()
    path = _find_note_path(vault, note_name)
    note = load_note(path)
    level = parse_level(note.meta)

    scenario = scenarios.generate(note, level=level, provider=provider)
    transcript = {"note": note_name, "level": level, "challenge": scenario.get("challenge"),
                  "provider": provider.name}

    verdict = None
    if code:
        v = run_code(code, language=language, use_docker=use_docker)
        verdict = v.to_dict()
        passed = v.passed
    transcript["verdict"] = verdict

    if passed is None:
        transcript["status"] = "awaiting_evaluation"
        return transcript

    if passed:
        new_level = min(level + 1, MAX_LEVEL)
        new_score = min(100.0, float(note.meta.get("mastery_score", 0) or 0) + PROMOTE_BONUS)
        meta = state.update_note_state(path, updates={
            "mastery_score": new_score,
            "current_level": f"Level {new_level}: {scenarios.LEVELS[new_level][0]}"})
        ledger.append_milestone(
            os.path.join(vault, "Activity_Ledger.md"),
            ledger.Milestone(topic=note_name, status=f"Promoted to Level {new_level}",
                             challenge=(scenario.get("challenge") or {}).get("prompt", "")[:120],
                             date=today or ""))
        transcript.update(status="promoted", new_level=new_level, mastery_score=new_score)
    else:
        probe = socratic.probe(note.meta.get("topic", note_name), answer or "(no answer)",
                               provider=provider)
        weakness = (scenario.get("challenge") or {}).get("kind", "unresolved")
        state.update_note_state(path, add_weaknesses=[weakness])
        transcript.update(status="needs_work", socratic=probe, recorded_weakness=weakness)
    return transcript


def hydrate(vault: str) -> dict:
    """State Hydration convenience: list notes with level/score."""
    notes = load_vault(vault)
    return {"count": len(notes),
            "notes": [{"name": n.name, "level": n.meta.get("current_level"),
                       "mastery_score": n.meta.get("mastery_score")} for n in notes]}
