import unittest

from pal_agent.memory.graph import KnowledgeGraph
from pal_agent.memory.vault import Note


def _note(name, links=None, prereqs=None):
    return Note(name=name, path=f"{name}.md", links=links or [], prerequisites=prereqs or [])


class KnowledgeGraphTest(unittest.TestCase):
    def setUp(self):
        # State_Concurrency -> Golang_Basics, Pointers_And_Memory (prereqs)
        # Golang_Basics -> State_Concurrency (back link)
        # Orphan_Note -> (nothing); Pointers_And_Memory has no file (dangling)
        self.g = KnowledgeGraph.from_notes([
            _note("State_Concurrency", links=["Golang_Basics"],
                  prereqs=["Golang_Basics", "Pointers_And_Memory"]),
            _note("Golang_Basics", links=["State_Concurrency"]),
            _note("Orphan_Note"),
        ])

    def test_nodes_include_dangling_target(self):
        self.assertEqual(
            self.g.nodes,
            ["Golang_Basics", "Orphan_Note", "Pointers_And_Memory", "State_Concurrency"])
        self.assertEqual(len(self.g.file_nodes), 3)

    def test_edges_dedup_prereq_and_link(self):
        self.assertEqual(
            self.g.edges,
            [("Golang_Basics", "State_Concurrency"),
             ("State_Concurrency", "Golang_Basics"),
             ("State_Concurrency", "Pointers_And_Memory")])

    def test_neighbors(self):
        self.assertEqual(self.g.neighbors("Golang_Basics"), ["State_Concurrency"])

    def test_dangling(self):
        self.assertEqual(self.g.dangling(), ["Pointers_And_Memory"])

    def test_orphans(self):
        self.assertEqual(self.g.orphans(), ["Orphan_Note"])

    def test_summary_shape(self):
        s = self.g.summary()
        self.assertEqual(s["nodes"], 4)
        self.assertEqual(s["file_nodes"], 3)
        self.assertEqual(s["edges"], 3)
        self.assertEqual(s["orphans"], ["Orphan_Note"])


if __name__ == "__main__":
    unittest.main()
