# PAL-Agent — Adaptive AI Senior Learning Mentor

Trợ lý AI đào tạo cá nhân hoá (Senior Mentor / System Architect) dùng **Obsidian
Vault** làm bộ nhớ tri thức dạng graph, đưa người học Zero → Hero qua 4 cấp độ theo
vòng **Socratic Adaptive Learning Loop**.

## Yêu cầu
Python ≥ 3.10. Cài phụ thuộc: `pip install -e .` (PyYAML, NetworkX, jsonschema).
- **LLM (tuỳ chọn, cho `read`/`challenge`/`feedback`):** cần `claude` CLI trên PATH
  (bản subscription — không cần API key). Không có → tự dùng stub deterministic.
- **Docker (tuỳ chọn, cho `verify`):** cần Docker để chạy sandbox cô lập; không có →
  fallback subprocess (`--no-docker`).

## Kiến trúc (SRD → module)

```
pal_agent/
  cli.py                 # 8 lệnh CLI
  orchestrator.py        # Socratic Adaptive Learning Loop (nối mọi layer)
  memory/                # Memory & Knowledge layer
    vault.py             # parse .md + YAML frontmatter + [[WikiLinks]]        (F1.1)
    graph.py             # NetworkX graph, path <10ms cache, cycle detect       (N1)
    state.py             # ghi lại mastery/level, YAML round-trip an toàn        (F1.3, N3)
    ledger.py            # append Activity_Ledger.md                            (F1.3)
  knowledge/             # Knowledge Expansion & Synthesis
    ingest.py            # Auto-Atomization từ /Inbox + auto [[WikiLinks]]       (F2.1)
    synthesizer.py       # Dynamic Narrative Synthesizer (read-only)            (F2.2)
    linter.py            # Semantic Graph Linter (orphan + gợi ý link)          (F2.3)
  mentor/                # Adaptive teaching
    scenarios.py         # Scenario Generator Level 1–4 (JSON Schema)           (F3, N4)
    socratic.py          # Socratic Feedback Loop (hỏi, không đưa đáp án)       (F4.3)
  verify/                # Verification layer
    sandbox.py           # Docker/subprocess execution + benchmark              (F4.1)
    codegraph.py         # Python AST call-graph, cycle + undefined-call        (F4.2)
  llm/provider.py        # claude CLI + stub, structured output validate        (N4)
```

## Lệnh CLI

```bash
pal-agent hydrate [vault]                       # Vault -> graph summary (F1.1)
pal-agent lint [vault]                          # orphan + gợi ý link (F2.3)
pal-agent ingest <inbox> --vault <v>            # atomize raw docs (F2.1)
pal-agent read <topic> [vault] [--llm claude]   # tổng hợp bài đọc (F2.2)
pal-agent challenge <note> [vault] [--level N]  # sinh bài tập Level 1–4 (F3)
pal-agent verify <file.py> [--no-docker]        # chấm code trong sandbox (F4.1)
pal-agent codecheck <file.py>                   # kiểm tra cấu trúc AST (F4.2)
pal-agent feedback --concept X --answer Y       # câu hỏi Socratic (F4.3)
pal-agent record <vault> <note> --score .. --status ..   # ghi tiến độ + ledger (F1.3)
pal-agent mentor <vault> <note> --code f.py     # MỘT vòng học thích ứng (orchestrator)
```

Chọn backend LLM: `--llm claude` (thật) · `--llm stub` (offline) · bỏ trống = auto.

## Test

```bash
python -m unittest discover -s tests -t .     # 58 tests
```

## Trạng thái & giới hạn (trung thực)

- ✅ Toàn bộ backlog SRD (F1–F4, N1/N3/N4) đã có bản chạy được + test. Docker sandbox và
  LLM qua `claude` CLI đã kiểm chứng **chạy thật**.
- ⚠️ **First cut** (bản lõi, sẽ mở rộng): `codegraph` mới hỗ trợ **Python** (Tree-sitter đa
  ngôn ngữ để sau); orchestrator là **state machine nhẹ**, chưa phải LangGraph/Dify; linter
  dùng similarity **lexical** (chưa vector/embedding).
