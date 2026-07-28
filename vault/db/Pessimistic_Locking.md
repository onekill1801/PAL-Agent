---
topic: Pessimistic Locking
current_level: 'Level 2: Operation'
mastery_score: 0.0
prerequisites:
- '[[Lost_Update]]'
- '[[Mutex_Lock]]'
weaknesses: []
strengths: []
last_evaluated: 2026-07-28
courses:
- C02
- C03
---

Khoá bi quan: **khoá hàng ngay khi đọc** để không ai sửa cho tới khi commit —
`SELECT ... FOR UPDATE` (trong một transaction). Tương tự [[Mutex_Lock]] nhưng ở DB.

Hợp khi tranh chấp cao (tránh retry storm của [[Optimistic_Locking]]). Cạm bẫy: giữ khoá
lâu làm nghẽn, và **[[Deadlock]]** khi hai transaction khoá hàng theo thứ tự ngược nhau —
giảm bằng cách luôn khoá theo cùng thứ tự và giữ transaction ngắn.
