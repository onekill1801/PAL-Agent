import os
import tempfile
import unittest

from pal_agent.memory import vault

NOTE = """\
---
topic: "Concurrency in Go"
current_level: "Level 3: Anomaly Detection"
mastery_score: 68.5
prerequisites:
  - "[[Golang_Basics]]"
  - "[[Pointers_And_Memory]]"
strengths:
  - "Goroutine stack allocation"
last_evaluated: 2026-07-27
---

Body references [[Golang_Basics]] and a fresh [[Channel_Deadlock]].
"""


class ParseFrontmatterTest(unittest.TestCase):
    def test_scalars_are_coerced(self):
        meta, _body = vault.parse_frontmatter(NOTE)
        self.assertEqual(meta["topic"], "Concurrency in Go")
        self.assertEqual(meta["current_level"], "Level 3: Anomaly Detection")
        self.assertEqual(meta["mastery_score"], 68.5)
        self.assertIsInstance(meta["mastery_score"], float)

    def test_lists_parsed_raw(self):
        # parse_frontmatter returns raw YAML values; wikilink stripping for
        # prerequisites happens in load_note (see LoadVaultTest).
        meta, _ = vault.parse_frontmatter(NOTE)
        self.assertEqual(meta["prerequisites"], ["[[Golang_Basics]]", "[[Pointers_And_Memory]]"])
        self.assertEqual(meta["strengths"], ["Goroutine stack allocation"])

    def test_body_is_separated(self):
        _meta, body = vault.parse_frontmatter(NOTE)
        self.assertIn("Body references", body)
        self.assertNotIn("topic:", body)

    def test_no_frontmatter(self):
        meta, body = vault.parse_frontmatter("just text, no ---")
        self.assertEqual(meta, {})
        self.assertEqual(body, "just text, no ---")


class WikilinkTest(unittest.TestCase):
    def test_extract_dedup_ordered(self):
        links = vault.extract_wikilinks("a [[X]] b [[Y]] c [[X]] d [[Z|alias]]")
        self.assertEqual(links, ["X", "Y", "Z"])


class LoadVaultTest(unittest.TestCase):
    def test_loads_and_skips_ledger(self):
        with tempfile.TemporaryDirectory() as d:
            with open(os.path.join(d, "State_Concurrency.md"), "w", encoding="utf-8") as f:
                f.write(NOTE)
            with open(os.path.join(d, "Activity_Ledger.md"), "w", encoding="utf-8") as f:
                f.write("## ledger\n")
            notes = vault.load_vault(d)
        self.assertEqual([n.name for n in notes], ["State_Concurrency"])
        note = notes[0]
        self.assertEqual(note.prerequisites, ["Golang_Basics", "Pointers_And_Memory"])
        self.assertEqual(note.links, ["Golang_Basics", "Channel_Deadlock"])
        # edges = prerequisites + body links, deduped
        self.assertEqual(note.edges,
                         ["Golang_Basics", "Pointers_And_Memory", "Channel_Deadlock"])

    def test_missing_vault_raises(self):
        with self.assertRaises(FileNotFoundError):
            vault.load_vault("/no/such/vault/here")


if __name__ == "__main__":
    unittest.main()
