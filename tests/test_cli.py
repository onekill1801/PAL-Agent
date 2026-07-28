import io
import json
import os
import unittest
from contextlib import redirect_stdout

from pal_agent.cli import main

_SAMPLE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "sample_vault")


class CliTest(unittest.TestCase):
    def test_version_exits_zero(self):
        with self.assertRaises(SystemExit) as cm:
            main(["--version"])
        self.assertEqual(cm.exception.code, 0)

    def test_hydrate_bundled_sample_vault(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = main(["hydrate", _SAMPLE])  # explicit: default now resolves to ./vault
        self.assertEqual(rc, 0)
        out = json.loads(buf.getvalue())
        summary = out["summary"]
        self.assertEqual(summary["file_nodes"], 3)
        self.assertIn("Orphan_Note", summary["orphans"])
        self.assertIn("Pointers_And_Memory", summary["dangling"])


if __name__ == "__main__":
    unittest.main()
