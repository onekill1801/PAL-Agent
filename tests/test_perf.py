import time
import unittest

from pal_agent.memory.graph import KnowledgeGraph
from pal_agent.memory.vault import Note


class PathLatencyTest(unittest.TestCase):
    """N1: graph path queries must stay well under 10ms on a RAM-resident graph."""

    def setUp(self):
        # A 500-node prerequisite chain: N0 -> N1 -> ... -> N499
        notes = [Note(name=f"N{i}", path=f"N{i}.md", prerequisites=[f"N{i + 1}"])
                 for i in range(499)]
        notes.append(Note(name="N499", path="N499.md"))
        self.g = KnowledgeGraph.from_notes(notes)

    def test_path_query_under_10ms(self):
        # warm any lazy graph construction, then measure a single query
        self.g.shortest_path("N0", "N499")
        start = time.perf_counter()
        path = self.g.shortest_path("N0", "N499")
        elapsed_ms = (time.perf_counter() - start) * 1000
        self.assertEqual(len(path), 500)
        self.assertLess(elapsed_ms, 10.0, f"path query took {elapsed_ms:.2f}ms (N1 budget 10ms)")


if __name__ == "__main__":
    unittest.main()
