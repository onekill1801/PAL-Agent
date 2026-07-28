---
topic: "COURSE 03 — Database Engineering & Query Optimization"
current_level: "Level 3: Anomaly Detection"
mastery_score: 0.0
prerequisites:
  - "[[DB_Race_Condition]]"
weaknesses: []
strengths: []
tags: [moc, course]
last_evaluated: 2026-07-28
---

**Vùng tri thức:** PostgreSQL, MySQL, SQL optimization, indexing (B-Tree, Hash, GIN),
transactions & isolation levels.

## Mục tiêu Verify
- **L1–2:** Index Scan vs Seq Scan, cách Query Planner vận hành.
- **L3–4:** thiết kế index tối ưu giữ nguyên câu truy vấn gốc (strict query constraints),
  xử lý locking contention ở quy mô giao dịch lớn.

## Atomic notes (đã có)
- [[DB_Race_Condition]] · [[Lost_Update]] · [[Transaction_Isolation_Levels]] ·
  [[Optimistic_Locking]] · [[Pessimistic_Locking]]
- Sẽ tạo: `Index_BTree`, `Seq_vs_Index_Scan`, `Query_Planner`, `Lock_Contention`
