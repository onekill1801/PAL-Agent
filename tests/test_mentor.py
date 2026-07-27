import os
import unittest

from pal_agent.knowledge.synthesizer import synthesize
from pal_agent.llm.provider import StubProvider
from pal_agent.mentor import scenarios, socratic
from pal_agent.memory.vault import Note


def _sample_vault():
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(here, "sample_vault")


class SynthesizerTest(unittest.TestCase):
    def test_gathers_neighbors_and_calls_provider(self):
        out = synthesize(_sample_vault(), "State_Concurrency",
                         provider=StubProvider(text="A woven narrative."))
        self.assertEqual(out["narrative"], "A woven narrative.")
        self.assertIn("State_Concurrency", out["sources"])
        self.assertIn("Golang_Basics", out["sources"])  # graph neighbour

    def test_missing_topic(self):
        out = synthesize(_sample_vault(), "Nonexistent", provider=StubProvider())
        self.assertTrue(out.get("error"))


class ScenarioTest(unittest.TestCase):
    def test_parse_level(self):
        self.assertEqual(scenarios.parse_level({"current_level": "Level 3: Anomaly"}), 3)
        self.assertEqual(scenarios.parse_level({}), 1)

    def test_generate_structured(self):
        note = Note(name="Concurrency", path="x.md",
                    meta={"topic": "Concurrency", "current_level": "Level 3"},
                    body="channels and goroutines")
        obj = {"level": 3, "kind": "Anomaly Detection",
               "prompt": "Find the race condition in this code.",
               "constraints": ["no global locks"]}
        out = scenarios.generate(note, provider=StubProvider(obj=obj))
        self.assertEqual(out["level"], 3)
        self.assertEqual(out["challenge"]["prompt"], obj["prompt"])

    def test_bad_level(self):
        note = Note(name="X", path="x.md", meta={"current_level": "Level 1"}, body="")
        self.assertTrue(scenarios.generate(note, level=9, provider=StubProvider()).get("error"))


class SocraticTest(unittest.TestCase):
    def test_probe_returns_question(self):
        obj = {"question": "Điều gì xảy ra khi channel không có buffer",
               "focus_concept": "Unbuffered channels"}
        out = socratic.probe("Concurrency", "It never deadlocks",
                             provider=StubProvider(obj=obj))
        self.assertTrue(out["question"].endswith("?"))  # forced question mark
        self.assertEqual(out["focus_concept"], "Unbuffered channels")

    def test_ensure_question_fallback(self):
        self.assertTrue(socratic._ensure_question("").endswith("?"))
        self.assertEqual(socratic._ensure_question("why."), "why?")


if __name__ == "__main__":
    unittest.main()
