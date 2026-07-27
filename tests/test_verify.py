import unittest

from pal_agent.verify import codegraph, sandbox


class SandboxTest(unittest.TestCase):
    """Uses the subprocess engine (use_docker=False) so no image pull is needed."""

    def test_passing_code(self):
        v = sandbox.run_code("print('hello')", use_docker=False)
        self.assertTrue(v.passed)
        self.assertEqual(v.exit_code, 0)
        self.assertIn("hello", v.stdout)
        self.assertEqual(v.engine, "subprocess")

    def test_failing_code(self):
        v = sandbox.run_code("import sys; sys.exit(3)", use_docker=False)
        self.assertFalse(v.passed)
        self.assertEqual(v.exit_code, 3)

    def test_unsupported_language(self):
        v = sandbox.run_code("x", language="brainfuck", use_docker=False)
        self.assertFalse(v.passed)
        self.assertIn("unsupported", v.error)


class CodegraphTest(unittest.TestCase):
    def test_clean_module(self):
        src = ("def b():\n    return 1\n\n"
               "def a():\n    return b() + 1\n")
        report = codegraph.analyze(src)
        self.assertTrue(report["ok"])
        self.assertIn(("a", "b"), report["edges"])
        self.assertEqual(report["cycles"], [])

    def test_detects_cycle(self):
        src = ("def a():\n    return b()\n\n"
               "def b():\n    return a()\n")
        report = codegraph.analyze(src)
        self.assertFalse(report["ok"])
        self.assertTrue(report["cycles"])

    def test_detects_undefined_call(self):
        src = "def a():\n    return does_not_exist()\n"
        self.assertIn("does_not_exist", codegraph.undefined_names(src))

    def test_syntax_error(self):
        report = codegraph.analyze("def a(:\n  pass\n")
        self.assertTrue(report.get("error"))


if __name__ == "__main__":
    unittest.main()
