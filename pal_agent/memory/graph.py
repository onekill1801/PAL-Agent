"""Build an in-memory knowledge graph from parsed Atomic Notes.

A minimal directed graph (stdlib dict adjacency) — the Phase 1 stand-in for the
NetworkX + RAM-cache engine on the backlog (see N1: <10ms path queries). Nodes are
note names; an edge ``A -> B`` means note A links to / requires B. Targets that have
no backing ``.md`` file (e.g. ``[[Pointers_And_Memory]]`` with no note yet) are
tracked as *dangling* so the Semantic Graph Linter (F2.3) can surface them.
"""

from __future__ import annotations

from dataclasses import dataclass, field

try:  # NetworkX backs the path/cycle queries (N1); dict adjacency is the fallback.
    import networkx as nx
except ImportError:  # pragma: no cover - fallback path
    nx = None

from .vault import Note


@dataclass
class KnowledgeGraph:
    adjacency: dict[str, list[str]] = field(default_factory=dict)  # name -> out-edges
    file_nodes: set[str] = field(default_factory=set)             # notes backed by a file

    @classmethod
    def from_notes(cls, notes: list[Note]) -> "KnowledgeGraph":
        g = cls()
        for n in notes:
            g.file_nodes.add(n.name)
            g.adjacency.setdefault(n.name, [])
        for n in notes:
            for target in n.edges:
                g.adjacency[n.name].append(target)
                g.adjacency.setdefault(target, [])  # ensure target is a node
        return g

    @property
    def nodes(self) -> list[str]:
        return sorted(self.adjacency)

    @property
    def edges(self) -> list[tuple[str, str]]:
        return sorted((src, dst) for src, dsts in self.adjacency.items() for dst in dsts)

    def neighbors(self, name: str) -> list[str]:
        return list(self.adjacency.get(name, []))

    def dangling(self) -> list[str]:
        """Referenced targets that have no backing note file."""
        return sorted(n for n in self.adjacency if n not in self.file_nodes)

    def orphans(self) -> list[str]:
        """File-backed notes with no edge in either direction (isolated — F2.3)."""
        indeg = {n: 0 for n in self.adjacency}
        for _src, dsts in self.adjacency.items():
            for dst in dsts:
                indeg[dst] += 1
        return sorted(n for n in self.file_nodes
                      if not self.adjacency.get(n) and indeg.get(n, 0) == 0)

    def summary(self) -> dict:
        return {
            "nodes": len(self.nodes),
            "file_nodes": len(self.file_nodes),
            "edges": len(self.edges),
            "dangling": self.dangling(),
            "orphans": self.orphans(),
        }

    # --- NetworkX-backed queries (N1: sub-10ms path lookups on a RAM graph) -------
    def to_networkx(self):
        """Return a cached ``networkx.DiGraph`` of the adjacency (N1: RAM-resident,
        built once so repeat path queries are sub-millisecond). Requires networkx."""
        if nx is None:  # pragma: no cover - fallback path
            raise RuntimeError("networkx not installed; `pip install networkx`")
        cached = getattr(self, "_nx_cache", None)
        if cached is not None:
            return cached
        g = nx.DiGraph()
        g.add_nodes_from(self.adjacency)
        for src, dsts in self.adjacency.items():
            for dst in dsts:
                g.add_edge(src, dst)
        self._nx_cache = g
        return g

    def shortest_path(self, source: str, target: str) -> list[str] | None:
        """Learning path source -> target following prerequisite/link edges.

        Falls back to a stdlib BFS if networkx is unavailable. Returns None if no
        path exists (or either node is unknown)."""
        if source not in self.adjacency or target not in self.adjacency:
            return None
        if nx is not None:
            try:
                return nx.shortest_path(self.to_networkx(), source, target)
            except nx.NetworkXNoPath:
                return None
        # stdlib BFS fallback
        from collections import deque
        prev, seen, q = {source: None}, {source}, deque([source])
        while q:
            cur = q.popleft()
            if cur == target:
                path = []
                while cur is not None:
                    path.append(cur)
                    cur = prev[cur]
                return list(reversed(path))
            for nxt in self.adjacency.get(cur, []):
                if nxt not in seen:
                    seen.add(nxt)
                    prev[nxt] = cur
                    q.append(nxt)
        return None

    def cycles(self) -> list[list[str]]:
        """Dependency cycles in the knowledge graph (empty = acyclic)."""
        if nx is None:  # pragma: no cover - fallback path
            return []
        return [list(c) for c in nx.simple_cycles(self.to_networkx())]
