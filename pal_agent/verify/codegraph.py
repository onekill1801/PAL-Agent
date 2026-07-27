"""Codegraph Structural Validation (F4.2) — Python first cut.

Parse Python source with the stdlib ``ast`` into a function call graph, then flag
structural problems: dependency cycles (via networkx) and calls to names that are
neither defined, imported, nor builtin (a proxy for broken data flow after a
refactor). Multi-language Tree-sitter/SCIP is the later upgrade behind this same
interface.
"""

from __future__ import annotations

import ast
import builtins

try:
    import networkx as nx
except ImportError:  # pragma: no cover
    nx = None

_BUILTINS = set(dir(builtins))


def _collect(tree: ast.AST):
    funcs, imports = {}, set()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            funcs[node.name] = node
        elif isinstance(node, ast.Import):
            for a in node.names:
                imports.add((a.asname or a.name).split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            for a in node.names:
                imports.add(a.asname or a.name)
    return funcs, imports


def call_graph(source: str) -> tuple[list[str], list[tuple[str, str]]]:
    """Return (function names, edges caller->callee) for defined functions."""
    tree = ast.parse(source)
    funcs, _imports = _collect(tree)
    edges = []
    for name, node in funcs.items():
        for call in ast.walk(node):
            if isinstance(call, ast.Call) and isinstance(call.func, ast.Name):
                if call.func.id in funcs:
                    edges.append((name, call.func.id))
    return list(funcs), sorted(set(edges))


def find_cycles(source: str) -> list[list[str]]:
    nodes, edges = call_graph(source)
    if nx is None:  # pragma: no cover
        return []
    g = nx.DiGraph()
    g.add_nodes_from(nodes)
    g.add_edges_from(edges)
    return [list(c) for c in nx.simple_cycles(g)]


def undefined_names(source: str) -> list[str]:
    """Called names that are not defined here, imported, or builtin."""
    tree = ast.parse(source)
    funcs, imports = _collect(tree)
    assigned = {n.id for node in ast.walk(tree) if isinstance(node, ast.Assign)
                for n in ast.walk(node) if isinstance(n, ast.Name)}
    known = set(funcs) | imports | _BUILTINS | assigned
    missing = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id not in known and node.func.id not in missing:
                missing.append(node.func.id)
    return missing


def analyze(source: str) -> dict:
    """Structural report: functions, edges, cycles, and undefined-call issues."""
    try:
        nodes, edges = call_graph(source)
    except SyntaxError as e:
        return {"ok": False, "error": True, "message": f"syntax error: {e}"}
    cycles = find_cycles(source)
    undefined = undefined_names(source)
    issues = []
    if cycles:
        issues.append(f"dependency cycle(s): {cycles}")
    if undefined:
        issues.append(f"undefined call(s): {undefined}")
    return {"ok": not issues, "functions": nodes, "edges": edges,
            "cycles": cycles, "undefined": undefined, "issues": issues}
