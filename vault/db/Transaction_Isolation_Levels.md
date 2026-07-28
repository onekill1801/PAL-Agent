---
topic: "Transaction Isolation Levels"
current_level: "Level 2: Operation"
mastery_score: 0.0
prerequisites:
  - "[[DB_Race_Condition]]"
weaknesses: []
strengths: []
last_evaluated: 2026-07-28
---

Bốn mức (SQL): **Read Uncommitted** (cho dirty read) → **Read Committed** (mặc định
Postgres) → **Repeatable Read** (chặn non-repeatable read; MySQL InnoDB mặc định) →
**Serializable** (như chạy tuần tự, chặn phantom).

Đánh đổi: mức càng cao càng an toàn nhưng càng giảm song song / dễ bị abort (serialization
failure → phải retry). Lưu ý: **Repeatable Read KHÔNG tự chặn [[Lost_Update]]** trong mọi
engine — vẫn cần [[Optimistic_Locking]] hoặc `FOR UPDATE`.
