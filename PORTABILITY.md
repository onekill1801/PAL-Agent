# Portability — giữ ngữ cảnh khi đổi máy & đổi model

**Nguyên tắc cốt lõi:** ngữ cảnh học của bạn **không nằm trong model hay phiên chat**.
Nó nằm trong **vault (file Markdown) + git**. Vì thế:
- Đổi **máy** → `git clone` là có lại toàn bộ.
- Đổi **model** → model chỉ *sinh bài tập/bài đọc*; *trí nhớ* (graph, level, mastery,
  điểm yếu, ledger) là file, độc lập model → **không bị quên**.

## Cái gì được lưu (và ở đâu)
| Dữ liệu | Nơi lưu | Portable? |
|---|---|---|
| Kiến thức (atomic notes) | `vault/**/*.md` | ✅ git |
| Tiến độ (level, mastery_score, weaknesses) | frontmatter mỗi note | ✅ git |
| Cột mốc học | `vault/Activity_Ledger.md` | ✅ git |
| Cấu trúc course/lens | `courses:` tag + MOC | ✅ git |
| Chọn model | biến môi trường `PAL_LLM` (không lưu trong vault) | cấu hình mỗi máy |

## Đổi sang MÁY khác
```bash
git clone https://github.com/onekill1801/PAL-Agent.git
cd PAL-Agent/work/pal-agent      # (repo hiện chứa vault ở đây)
pip install -e .
pal-agent hydrate                # State Hydration: dựng lại toàn bộ ngữ cảnh
```
Vault là `./vault` mặc định. Muốn để vault chỗ khác: `export PAL_VAULT=/path/to/vault`.

## Đổi sang MODEL khác (context vẫn nguyên)
Chọn backend bằng `PAL_LLM` — trí nhớ không đổi, chỉ đổi "bộ não" sinh nội dung:

```bash
# Claude CLI (subscription, không cần key) — mặc định nếu có
export PAL_LLM=claude

# Model LOCAL qua Ollama (offline, đổi máy vẫn chạy)
export PAL_LLM=ollama
export OLLAMA_HOST=http://localhost:11434
export PAL_MODEL=llama3.1          # hoặc qwen2.5, mistral...

# OpenAI hoặc bất kỳ endpoint OpenAI-compatible (vLLM, LM Studio, Groq, Together...)
export PAL_LLM=openai
export OPENAI_BASE_URL=https://api.openai.com/v1   # hoặc http://localhost:1234/v1
export OPENAI_API_KEY=sk-...
export PAL_MODEL=gpt-4o-mini

# Không có model nào → stub offline (deterministic, để test/di chuyển)
export PAL_LLM=stub
```
Mọi provider dùng chung interface + **JSON-Schema structured output** (N4), nên
`challenge/read/feedback/mentor` chạy giống nhau bất kể model.

## Kiểm chứng nhanh sau khi chuyển
```bash
pal-agent hydrate | python -c "import sys,json;print(json.load(sys.stdin)['summary'])"
pal-agent challenge Race_Condition --level 2   # thử model mới sinh bài
```

## Ghi chú
- Đẩy tiến độ mới lên GitHub sau mỗi buổi học: `git add -A && git commit -m "learn: ..." && git push`.
  (Trong các buổi qua, tiến độ đã được commit + push tự động.)
- `PAL_MODEL`/`OPENAI_API_KEY` là cấu hình máy — **không** commit vào vault.
