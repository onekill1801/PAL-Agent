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
from .memory import ledger, state
from .memory.graph import KnowledgeGraph
from .memory.vault import load_vault

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

    args = p.parse_args(argv)
    if not getattr(args, "func", None):
        p.print_help()
        return 0
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
