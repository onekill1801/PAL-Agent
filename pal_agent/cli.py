"""PAL-Agent command-line entry point.

Phase 1 surface: hydrate the knowledge graph from an Obsidian Vault and print a
JSON summary. Later phases (F2 expansion, F3 scenarios, F4 verification) add
subcommands here — see the deferred backlog in the product brief.
"""

import argparse
import json
import os
import sys

from . import __version__
from .knowledge.ingest import ingest_inbox
from .knowledge.linter import lint_vault
from .knowledge.synthesizer import synthesize
from .llm import get_provider
from .memory import ledger, state
from .memory.graph import KnowledgeGraph
from .memory.vault import load_vault
from .mentor.scenarios import scenario_for_vault
from .mentor.socratic import probe
from .verify.codegraph import analyze
from .verify.sandbox import run_code

# Bundled sample vault (repo-relative), used when no path is given.
_DEFAULT_VAULT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                              "sample_vault")


def _cmd_hydrate(args) -> int:
    """State Hydration (SRD 2.2 step 1): Vault -> graph -> summary."""
    vault = args.vault or _DEFAULT_VAULT
    try:
        notes = load_vault(vault)
    except FileNotFoundError as e:
        print(json.dumps({"error": True, "message": str(e)}), file=sys.stderr)
        return 1
    graph = KnowledgeGraph.from_notes(notes)
    out = {
        "vault": os.path.abspath(vault),
        "summary": graph.summary(),
        "notes": [
            {"name": n.name, "level": n.meta.get("current_level"),
             "mastery_score": n.meta.get("mastery_score"), "edges": n.edges}
            for n in notes
        ],
    }
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return 0


def _find_note(vault: str, name: str) -> str:
    """Locate ``<name>.md`` anywhere under the vault."""
    for root, _dirs, files in os.walk(vault):
        if f"{name}.md" in files:
            return os.path.join(root, f"{name}.md")
    raise FileNotFoundError(f"note '{name}' not found under {vault}")


def _cmd_record(args) -> int:
    """F1.3: write back mastery/level state and log a milestone to the ledger."""
    try:
        note_path = _find_note(args.vault, args.note)
    except FileNotFoundError as e:
        print(json.dumps({"error": True, "message": str(e)}), file=sys.stderr)
        return 1
    updates = {}
    if args.score is not None:
        updates["mastery_score"] = args.score
    if args.level:
        updates["current_level"] = args.level
    meta = state.update_note_state(note_path, updates=updates,
                                   add_weaknesses=[args.add_weakness] if args.add_weakness else None)
    logged = None
    if args.status:
        logged = ledger.append_milestone(
            os.path.join(args.vault, "Activity_Ledger.md"),
            ledger.Milestone(topic=args.note, status=args.status, challenge=args.challenge or "",
                             passed_constraints=args.constraints or "",
                             detected_weakness=args.weakness_link or ""))
    print(json.dumps({"ok": True, "note": note_path,
                      "mastery_score": meta.get("mastery_score"),
                      "current_level": meta.get("current_level"),
                      "milestone_logged": bool(logged)}, ensure_ascii=False))
    return 0


def _cmd_ingest(args) -> int:
    """F2.1: atomize raw docs from an inbox into the vault, auto-linked."""
    try:
        created = ingest_inbox(args.inbox, args.vault)
    except FileNotFoundError as e:
        print(json.dumps({"error": True, "message": str(e)}), file=sys.stderr)
        return 1
    print(json.dumps({"ok": True, "count": len(created), "created": created}, ensure_ascii=False))
    return 0


def _cmd_lint(args) -> int:
    """F2.3: report orphan notes and suggested links."""
    vault = args.vault or _DEFAULT_VAULT
    print(json.dumps(lint_vault(vault), indent=2, ensure_ascii=False))
    return 0


def _provider(args):
    return get_provider(getattr(args, "llm", "") or None)


def _cmd_read(args) -> int:
    """F2.2: synthesize a narrative for a topic (read-only)."""
    vault = args.vault or _DEFAULT_VAULT
    out = synthesize(vault, args.topic, provider=_provider(args))
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return 1 if out.get("error") else 0


def _cmd_challenge(args) -> int:
    """F3: generate an adaptive Level 1-4 challenge for a note."""
    vault = args.vault or _DEFAULT_VAULT
    out = scenario_for_vault(vault, args.note, level=args.level, provider=_provider(args))
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return 1 if out.get("error") else 0


def _cmd_verify(args) -> int:
    """F4.1: run a code file in the sandbox, print the verdict."""
    with open(args.file, encoding="utf-8") as f:
        code = f.read()
    verdict = run_code(code, language=args.language, use_docker=not args.no_docker,
                       race=args.race)
    print(json.dumps(verdict.to_dict(), indent=2, ensure_ascii=False))
    return 0 if verdict.passed else 1


def _cmd_codecheck(args) -> int:
    """F4.2: structural validation of a Python file."""
    with open(args.file, encoding="utf-8") as f:
        report = analyze(f.read())
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report.get("ok") else 1


def _cmd_feedback(args) -> int:
    """F4.3: Socratic probing question for a wrong answer."""
    out = probe(args.concept, args.answer, provider=_provider(args))
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="pal-agent",
                                description="Adaptive AI Senior Learning Mentor")
    p.add_argument("--version", action="version", version=f"pal-agent {__version__}")
    sub = p.add_subparsers(dest="cmd")

    h = sub.add_parser("hydrate", help="load an Obsidian Vault into the knowledge graph")
    h.add_argument("vault", nargs="?", default="", help="vault dir (default: bundled sample_vault)")
    h.set_defaults(func=_cmd_hydrate)

    r = sub.add_parser("record", help="write back progress state + log a milestone (F1.3)")
    r.add_argument("vault")
    r.add_argument("note", help="note name (file stem)")
    r.add_argument("--score", type=float, default=None)
    r.add_argument("--level", default="")
    r.add_argument("--add-weakness", default="")
    r.add_argument("--status", default="", help="milestone status; logs to ledger if set")
    r.add_argument("--challenge", default="")
    r.add_argument("--constraints", default="")
    r.add_argument("--weakness-link", default="")
    r.set_defaults(func=_cmd_record)

    ig = sub.add_parser("ingest", help="atomize raw docs from an inbox into the vault (F2.1)")
    ig.add_argument("inbox", help="inbox dir with raw .md/.txt docs")
    ig.add_argument("--vault", required=True)
    ig.set_defaults(func=_cmd_ingest)

    lt = sub.add_parser("lint", help="find orphan notes + suggest links (F2.3)")
    lt.add_argument("vault", nargs="?", default="")
    lt.set_defaults(func=_cmd_lint)

    rd = sub.add_parser("read", help="synthesize a narrative for a topic (F2.2)")
    rd.add_argument("topic")
    rd.add_argument("vault", nargs="?", default="")
    rd.add_argument("--llm", default="", help="stub|claude (default: auto)")
    rd.set_defaults(func=_cmd_read)

    ch = sub.add_parser("challenge", help="generate an adaptive challenge (F3)")
    ch.add_argument("note")
    ch.add_argument("vault", nargs="?", default="")
    ch.add_argument("--level", type=int, default=None)
    ch.add_argument("--llm", default="")
    ch.set_defaults(func=_cmd_challenge)

    vf = sub.add_parser("verify", help="run code in the sandbox (F4.1)")
    vf.add_argument("file")
    vf.add_argument("--language", default="python")
    vf.add_argument("--no-docker", action="store_true")
    vf.add_argument("--race", action="store_true")
    vf.set_defaults(func=_cmd_verify)

    cc = sub.add_parser("codecheck", help="structural validation of a Python file (F4.2)")
    cc.add_argument("file")
    cc.set_defaults(func=_cmd_codecheck)

    fb = sub.add_parser("feedback", help="Socratic probing question (F4.3)")
    fb.add_argument("--concept", required=True)
    fb.add_argument("--answer", required=True)
    fb.add_argument("--llm", default="")
    fb.set_defaults(func=_cmd_feedback)

    args = p.parse_args(argv)
    if not getattr(args, "func", None):
        p.print_help()
        return 0
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
