# PAL-Agent — Hướng dẫn sử dụng

Trợ lý AI mentor cá nhân hoá: học từ Obsidian Vault, ra bài tập theo cấp độ, chấm
code trong sandbox, và cập nhật tiến độ vào chính các note của bạn.

---

## 1. Cài đặt

```bash
cd work/pal-agent
pip install -e .          # cài PyYAML, NetworkX, jsonschema + lệnh `pal-agent`
```

Kiểm tra:
```bash
pal-agent --version                     # pal-agent 0.1.0
python -m unittest discover -s tests -t .   # 58 tests xanh
```

> Không cài cũng chạy được: thay `pal-agent <lệnh>` bằng `python3 -m pal_agent.cli <lệnh>`.

### Điều kiện tuỳ chọn
| Tính năng | Cần | Nếu thiếu |
|---|---|---|
| `read`, `challenge`, `feedback`, `mentor` (nội dung "thật") | `claude` CLI đã đăng nhập | tự chạy **stub** offline (nội dung mẫu) |
| `verify`, `mentor --docker` (sandbox cô lập) | Docker | dùng `verify --no-docker` (subprocess) |

Chọn backend LLM mỗi lệnh: `--llm claude` · `--llm stub` · bỏ trống = auto (có claude thì dùng claude).

---

## 2. Khái niệm

- **Vault**: một thư mục Obsidian chứa các file `.md`.
- **Atomic Note**: 1 file = 1 khái niệm, có YAML frontmatter:
  ```yaml
  ---
  topic: "Concurrency in Go"
  current_level: "Level 3: Anomaly Detection"   # Level 1..4
  mastery_score: 68.5
  prerequisites: ["[[Golang_Basics]]"]
  weaknesses: []
  strengths: []
  last_evaluated: 2026-07-27
  ---
  Nội dung, liên kết tới [[Note_Khác]].
  ```
- **Graph**: các note nối nhau qua `[[WikiLinks]]` + `prerequisites`.
- **Activity_Ledger.md**: nhật ký cột mốc (thăng cấp, thử thách đã qua).
- **4 cấp độ**: L1 Nhận biết · L2 Vận hành (code chạy đúng) · L3 Phát hiện bất thường
  (bug ngầm) · L4 Kiến trúc hệ thống (ràng buộc ngặt).

---

## 3. Các lệnh

### 3.1 Xem & kiểm tra tri thức
```bash
pal-agent hydrate ~/Vault          # tóm tắt graph: node/cạnh/orphan/link gãy
pal-agent lint ~/Vault             # note mồ côi + gợi ý nên nối với note nào
```

### 3.2 Nạp tài liệu mới
```bash
# Bổ nhỏ mọi .md/.txt trong ~/Inbox thành atomic note, tự chèn [[WikiLinks]]
pal-agent ingest ~/Inbox --vault ~/Vault
# -> tạo note trong ~/Vault/_ingested/
```

### 3.3 Học (cần claude để "thật")
```bash
# Đọc tổng quan 1 chủ đề (gom note liên quan, dệt thành bài mạch lạc)
pal-agent read State_Concurrency ~/Vault --llm claude

# Nhận 1 bài tập theo cấp độ (tự lấy level từ note, hoặc ép --level)
pal-agent challenge State_Concurrency ~/Vault --llm claude
pal-agent challenge State_Concurrency ~/Vault --level 4 --llm claude
```

### 3.4 Chấm bài
```bash
pal-agent verify bai_lam.py                 # chạy trong Docker (cô lập)
pal-agent verify bai_lam.py --no-docker     # chạy subprocess (không có Docker)
pal-agent verify bai_lam.go --language go --race   # Go + race detector
pal-agent codecheck module.py               # kiểm tra AST: vòng phụ thuộc, gọi hàm chưa định nghĩa
```

### 3.5 Ghi tiến độ thủ công
```bash
pal-agent record ~/Vault State_Concurrency \
    --score 80 --level "Level 4: System Architecture" \
    --add-weakness "False sharing" \
    --status "Promoted to Level 4" --challenge "Thiết kế hàng đợi lock-free" \
    --constraints "RAM<15MB" --weakness-link "False_Sharing"
# -> cập nhật frontmatter note (YAML an toàn) + append Activity_Ledger.md
```

---

## 4. Vòng học tự động (`mentor`)

Nối tất cả lại thành **một chu trình**: sinh bài tập → chấm code → nếu đúng thì
**thăng cấp + ghi ledger**, nếu sai thì trả **câu hỏi Socratic + ghi điểm yếu**.

```bash
# Có nộp code (Level 2–4): chấm bằng sandbox
pal-agent mentor ~/Vault State_Concurrency --code bai_lam.py --llm claude --docker

# Bài khái niệm (Level 1): tự chấm đúng/sai
pal-agent mentor ~/Vault Golang_Basics --answer "..." --passed --llm claude   # đúng
pal-agent mentor ~/Vault Golang_Basics --answer "..." --fail --llm claude      # sai
```

**Quy tắc:** ưu tiên `--code` (chạy sandbox) → nếu không có thì dùng `--passed/--fail`
→ nếu không có gì thì chỉ *sinh bài tập* và chờ đánh giá (`status: awaiting_evaluation`).

Kết quả trả về JSON gồm: `challenge` (bài tập), `verdict` (kết quả chấm),
`status` (`promoted` / `needs_work` / `awaiting_evaluation`), và `socratic` (khi sai).

---

## 5. Ví dụ end-to-end

```bash
cp -r sample_vault ~/my_vault                     # bắt đầu từ vault mẫu
pal-agent hydrate ~/my_vault                       # xem bức tranh
pal-agent challenge State_Concurrency ~/my_vault --llm claude   # nhận đề
# ... làm bài, lưu vào bai_lam.py ...
pal-agent mentor ~/my_vault State_Concurrency --code bai_lam.py --llm claude --docker
pal-agent hydrate ~/my_vault                       # thấy level/mastery đã đổi
tail ~/my_vault/Activity_Ledger.md                 # cột mốc mới
```

---

## 6. Xử lý sự cố

| Triệu chứng | Nguyên nhân / cách xử lý |
|---|---|
| Nội dung `challenge/read` nhạt, có `[stub]` | Không có `claude` CLI → đang dùng stub. Cài + đăng nhập `claude`, hoặc thêm `--llm claude`. |
| `verify` báo lỗi kéo image | Lần đầu Docker tải `python:3.11-slim`. Chờ, hoặc `--no-docker`. |
| `unrecognized arguments: --no-docker` với `mentor` | `mentor` dùng `--docker` (opt-in), mặc định đã là subprocess. |
| Ghi note làm hỏng YAML | Không xảy ra: mọi ghi đi qua `state.py` (round-trip an toàn, N3). |

## 7. Giới hạn hiện tại (first cut)
`codecheck` chỉ hỗ trợ **Python**; orchestrator là **state machine nhẹ** (chưa
LangGraph/Dify); linter dùng similarity **lexical** (chưa vector/embedding).
