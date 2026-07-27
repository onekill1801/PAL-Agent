import unittest

from pal_agent.llm import provider
from pal_agent.llm.provider import SchemaError, StubProvider, get_provider

SCHEMA = {
    "type": "object",
    "properties": {"question": {"type": "string"}, "level": {"type": "integer"}},
    "required": ["question", "level"],
    "additionalProperties": False,
}


class StubProviderTest(unittest.TestCase):
    def test_complete_echoes(self):
        out = StubProvider().complete("Explain concurrency")
        self.assertIn("[stub]", out)
        self.assertIn("Explain concurrency", out)

    def test_complete_canned(self):
        self.assertEqual(StubProvider(text="hello").complete("anything"), "hello")

    def test_structured_from_obj(self):
        obj = {"question": "What is a race condition?", "level": 3}
        got = StubProvider(obj=obj).structured("x", SCHEMA)
        self.assertEqual(got, obj)

    def test_structured_default_satisfies_schema(self):
        got = StubProvider().structured("x", SCHEMA)
        self.assertIn("question", got)
        self.assertIn("level", got)

    def test_structured_rejects_bad_obj(self):
        bad = StubProvider(obj={"question": "q"})  # missing required 'level'
        with self.assertRaises(Exception):
            bad.structured("x", SCHEMA)


class ExtractJsonTest(unittest.TestCase):
    def test_plain(self):
        self.assertEqual(provider._extract_json('{"a": 1}'), {"a": 1})

    def test_fenced(self):
        self.assertEqual(provider._extract_json('text\n```json\n{"a": 2}\n```\n'), {"a": 2})

    def test_embedded(self):
        self.assertEqual(provider._extract_json('sure: {"a": 3} done'), {"a": 3})

    def test_none_raises(self):
        with self.assertRaises(SchemaError):
            provider._extract_json("no json here")


class StructuredRetryTest(unittest.TestCase):
    def test_retries_then_fails(self):
        class Bad(provider.LLMProvider):
            name = "bad"
            def complete(self, prompt, system=None):
                return "not json"
        with self.assertRaises(SchemaError):
            Bad().structured("x", SCHEMA)


class FactoryTest(unittest.TestCase):
    def test_explicit_stub(self):
        self.assertIsInstance(get_provider("stub"), StubProvider)


if __name__ == "__main__":
    unittest.main()
