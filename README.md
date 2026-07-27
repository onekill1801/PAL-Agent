# PAL-Agent — Adaptive AI Senior Learning Mentor

Trợ lý AI đào tạo cá nhân hoá (Senior Mentor / System Architect) dùng **Obsidian
Vault** làm bộ nhớ tri thức dạng graph, đưa người học Zero → Hero qua 4 cấp độ.

> **Trạng thái: Phase 1 nucleus.** Bản này mới dựng lõi *State Hydration* — parse
> Vault (`.md` + YAML frontmatter + `[[WikiLinks]]`) thành graph trong RAM và truy
> vấn. F2/F3/F4, NetworkX, Docker Sandbox, Codegraph, LLM là backlog (xem SRD).

## Yêu cầu
Python ≥ 3.10, **stdlib-only** (chưa cần cài gì).

## Chạy thử

```bash
# Hydrate vault mẫu → JSON summary (nodes/edges/orphans/dangling)
python -m pal_agent.cli hydrate

# Hydrate một Obsidian Vault thật
python -m pal_agent.cli hydrate /đường/dẫn/tới/vault

python -m pal_agent.cli --version
```

## Test

```bash
python -m unittest discover -s tests -t .
```

## Cấu trúc

```
pal_agent/
  cli.py             # entry: hydrate | --version
  memory/
    vault.py         # parse .md + frontmatter + wikilinks (F1.1)
    graph.py         # graph node/edge, neighbors, orphans (F2.3), dangling
sample_vault/        # vault mẫu đúng schema SRD mục 6
tests/               # unittest
```

## Lộ trình (backlog → phát triển bằng auto-dev)
PyYAML + NetworkX (<10ms, N1) · Activity Ledger writer (F1.3, N3) · Auto-Atomization
ingest (F2.1) · Narrative Synthesizer (F2.2) · Semantic Graph Linter (F2.3) ·
Adaptive Scenario Generator Level 1–4 (F3) · Docker Sandbox + Codegraph verify (F4) ·
Model layer JSON Schema (N4) · Orchestrator LangGraph/Dify.
