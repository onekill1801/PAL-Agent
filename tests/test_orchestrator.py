import os
import shutil
import tempfile
import unittest

from pal_agent import orchestrator
from pal_agent.llm.provider import StubProvider
from pal_agent.memory.vault import load_note


def _sample_vault():
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(here, "sample_vault")


class RunCycleTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.vault = os.path.join(self.tmp.name, "vault")
        shutil.copytree(_sample_vault(), self.vault)
        self.note_path = os.path.join(self.vault, "02_State", "State_Concurrency.md")

    def tearDown(self):
        self.tmp.cleanup()

    def test_pass_promotes_and_logs(self):
        out = orchestrator.run_cycle(
            self.vault, "State_Concurrency", code="print('ok')",
            use_docker=False, provider=StubProvider(), today="2026-07-27")
        self.assertEqual(out["status"], "promoted")
        self.assertEqual(out["new_level"], 4)  # was Level 3
        note = load_note(self.note_path)
        self.assertIn("Level 4", note.meta["current_level"])
        with open(os.path.join(self.vault, "Activity_Ledger.md"), encoding="utf-8") as f:
            self.assertIn("Promoted to Level 4", f.read())

    def test_fail_returns_socratic_and_records_weakness(self):
        out = orchestrator.run_cycle(
            self.vault, "State_Concurrency", answer="it never deadlocks",
            code="import sys; sys.exit(1)", use_docker=False, provider=StubProvider())
        self.assertEqual(out["status"], "needs_work")
        self.assertTrue(out["socratic"]["question"].endswith("?"))
        self.assertEqual(out["recorded_weakness"], "Anomaly Detection")  # Level 3 kind
        note = load_note(self.note_path)
        self.assertIn("Anomaly Detection", note.meta.get("weaknesses", []))

    def test_awaiting_evaluation_when_no_signal(self):
        out = orchestrator.run_cycle(self.vault, "Golang_Basics", provider=StubProvider())
        self.assertEqual(out["status"], "awaiting_evaluation")

    def test_hydrate(self):
        h = orchestrator.hydrate(self.vault)
        self.assertEqual(h["count"], 3)


if __name__ == "__main__":
    unittest.main()
