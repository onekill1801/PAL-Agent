import os
import tempfile
import unittest

from pal_agent.knowledge import ingest, linter
from pal_agent.memory.vault import load_note, load_vault

RAW = """\
# Goroutine Scheduling
Goroutines are scheduled by the Go runtime onto OS threads. Relates to Golang_Basics.

# Channel Semantics
Channels pass data between goroutines. Deadlocks arise on unbuffered channels.
"""


class AtomizeTest(unittest.TestCase):
    def test_splits_by_heading(self):
        sections = ingest.atomize(RAW)
        self.assertEqual([t for t, _ in sections], ["Goroutine Scheduling", "Channel Semantics"])
        self.assertIn("scheduled by the Go runtime", sections[0][1])

    def test_slug(self):
        self.assertEqual(ingest.slug("Golang Basics"), "Golang_Basics")

    def test_auto_link(self):
        linked = ingest.auto_link("See Golang_Basics for context.", {"Golang_Basics"})
        self.assertIn("[[Golang_Basics]]", linked)
        # does not double-wrap
        again = ingest.auto_link(linked, {"Golang_Basics"})
        self.assertEqual(again.count("[[Golang_Basics]]"), 1)


class IngestInboxTest(unittest.TestCase):
    def test_creates_atomic_notes_and_links(self):
        with tempfile.TemporaryDirectory() as d:
            vault = os.path.join(d, "vault")
            inbox = os.path.join(d, "inbox")
            os.makedirs(vault)
            os.makedirs(inbox)
            # an existing note so ingest can auto-link to it
            with open(os.path.join(vault, "Golang_Basics.md"), "w", encoding="utf-8") as f:
                f.write("---\ntopic: Golang Basics\n---\nbasics\n")
            with open(os.path.join(inbox, "raw.md"), "w", encoding="utf-8") as f:
                f.write(RAW)

            created = ingest.ingest_inbox(inbox, vault, today="2026-07-27")
            self.assertEqual(len(created), 2)
            names = {load_note(p).name for p in created}
            self.assertEqual(names, {"Goroutine_Scheduling", "Channel_Semantics"})

            gs = load_note([p for p in created if p.endswith("Goroutine_Scheduling.md")][0])
            self.assertEqual(gs.meta["current_level"], "Level 1: Recognition")
            self.assertIn("Golang_Basics", gs.links)  # auto-linked to existing note


class LinterTest(unittest.TestCase):
    def test_finds_orphan_and_suggests(self):
        result = linter.lint_vault(_sample_vault())
        self.assertIn("Orphan_Note", result["orphans"])

    def test_score_symmetric_and_bounded(self):
        notes = load_vault(_sample_vault())
        s = linter.score(notes[0], notes[0])
        self.assertAlmostEqual(s, 1.0)


def _sample_vault():
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(here, "sample_vault")


if __name__ == "__main__":
    unittest.main()
