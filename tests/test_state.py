import os
import tempfile
import unittest

import yaml

from pal_agent.memory import ledger, state
from pal_agent.memory.vault import load_note

NOTE = """\
---
topic: "Concurrency in Go"
current_level: "Level 2: Operation"
mastery_score: 55.0
prerequisites:
  - "[[Golang_Basics]]"
weaknesses:
  - "Unbuffered channel deadlock"
last_evaluated: 2026-07-20
---

Body líne with a [[Golang_Basics]] link. Giữ nguyên tiếng Việt.
"""


class UpdateNoteStateTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.tmp.name, "State_Concurrency.md")
        with open(self.path, "w", encoding="utf-8") as f:
            f.write(NOTE)

    def tearDown(self):
        self.tmp.cleanup()

    def test_updates_and_preserves(self):
        state.update_note_state(
            self.path,
            updates={"mastery_score": 72.5, "current_level": "Level 3: Anomaly Detection"},
            add_weaknesses=["Sync.Map race condition"])
        note = load_note(self.path)
        # updated
        self.assertEqual(note.meta["mastery_score"], 72.5)
        self.assertEqual(note.meta["current_level"], "Level 3: Anomaly Detection")
        self.assertIn("Sync.Map race condition", note.meta["weaknesses"])
        self.assertIn("Unbuffered channel deadlock", note.meta["weaknesses"])  # kept
        # preserved: untouched key, prerequisites, body (incl. unicode)
        self.assertEqual(note.meta["topic"], "Concurrency in Go")
        self.assertEqual(note.prerequisites, ["Golang_Basics"])
        self.assertIn("Giữ nguyên tiếng Việt", note.body)

    def test_output_is_valid_yaml(self):
        state.update_note_state(self.path, updates={"mastery_score": 90})
        with open(self.path, encoding="utf-8") as f:
            text = f.read()
        block = text.split("---")[1]
        meta = yaml.safe_load(block)  # must not raise (N3)
        self.assertEqual(meta["mastery_score"], 90)

    def test_no_duplicate_weakness(self):
        state.update_note_state(self.path, add_weaknesses=["Unbuffered channel deadlock"])
        note = load_note(self.path)
        self.assertEqual(note.meta["weaknesses"].count("Unbuffered channel deadlock"), 1)


class LedgerTest(unittest.TestCase):
    def test_append_creates_header_once(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "Activity_Ledger.md")
            ledger.append_milestone(path, ledger.Milestone(
                topic="Golang_Concurrency", status="Promoted to Level 3",
                challenge="Fixed race condition", passed_constraints="RAM < 15MB",
                detected_weakness="Channel_Deadlock_Unbuffered", date="2026-07-27"))
            ledger.append_milestone(path, ledger.Milestone(
                topic="Docker", status="Promoted to Level 2", date="2026-07-28"))
            with open(path, encoding="utf-8") as f:
                text = f.read()
        self.assertEqual(text.count("## 📅 Milestone Activity Ledger"), 1)
        self.assertIn("### 🟢 2026-07-27 | Topic: [[Golang_Concurrency]]", text)
        self.assertIn("- **Detected Weakness:** [[Channel_Deadlock_Unbuffered]]", text)
        self.assertIn("Topic: [[Docker]]", text)


if __name__ == "__main__":
    unittest.main()
