---
topic: "Hash Table"
current_level: "Level 2: Operation"
mastery_score: 0.0
prerequisites:
  - "[[Big_O_Complexity]]"
weaknesses: []
strengths: []
courses: [C03, C07]
last_evaluated: 2026-07-28
---

Bảng băm: hàm hash ánh xạ khoá → chỉ số bucket → tra cứu/chèn **O(1) trung bình**. Xử lý
đụng độ bằng **chaining** (danh sách) hoặc **open addressing** (dò tuyến tính).

Cạm bẫy: hash kém → dồn cục (clustering) → suy biến **O(n)**; **resize/rehash** tốn O(n)
tại thời điểm giãn bảng; và (nối với [[Race_Condition]]) HashMap **không thread-safe** khi
resize đồng thời. Không giữ thứ tự (khác cây).

**Áp dụng (domain):** DB **hash index / hash join** (C03), cache, dedup, vocab tokenizer
của LLM (C04), [[Consistent_Hashing]] để sharding.
