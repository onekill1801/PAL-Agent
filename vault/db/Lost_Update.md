---
topic: Lost Update
current_level: 'Level 2: Operation'
mastery_score: 0.0
prerequisites:
- '[[DB_Race_Condition]]'
weaknesses: []
strengths: []
last_evaluated: 2026-07-28
courses:
- C03
---

Lost update: hai transaction cùng **đọc → sửa → ghi** một hàng; transaction ghi sau
đè mất cập nhật của cái trước. Ví dụ tồn kho: cả hai đọc `qty=10`, cùng trừ 1, cùng ghi
`9` → thực tế phải là `8`.

Cách chặn: (1) [[Optimistic_Locking]] — `UPDATE ... SET qty=9, version=version+1 WHERE
id=? AND version=<đã đọc>`, 0 dòng bị ảnh hưởng ⇒ retry; (2) [[Pessimistic_Locking]] —
`SELECT ... FOR UPDATE`; (3) atomic — `UPDATE ... SET qty = qty - 1 WHERE qty >= 1`.
