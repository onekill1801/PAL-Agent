---
topic: "B-Tree / B+Tree Index"
current_level: "Level 3: Anomaly Detection"
mastery_score: 0.0
prerequisites:
  - "[[Big_O_Complexity]]"
weaknesses: []
strengths: []
courses: [C03, C07]
last_evaluated: 2026-07-28
---

Cây cân bằng **nhiều nhánh, thấp** (fanout lớn) → tra cứu/chèn/xoá **O(log n)** với **ít
lần đọc đĩa** (mỗi node = 1 page). B+Tree để dữ liệu ở lá + lá nối nhau → **range scan**
nhanh.

Vì sao DB chọn B-Tree thay [[Hash_Table]]: hash chỉ tốt cho `=`, còn B-Tree hỗ trợ `<, >,
BETWEEN, ORDER BY, prefix`. Cạm bẫy: index sai cột/thứ tự cột (composite index), hoặc
predicate không **sargable** → planner bỏ index, quay về Seq Scan.

**Áp dụng (domain):** index chính của PostgreSQL/MySQL (C03), filesystem, key-value store.
