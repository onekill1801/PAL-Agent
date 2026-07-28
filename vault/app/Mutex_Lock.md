---
topic: Mutex / Lock
current_level: 'Level 2: Operation'
mastery_score: 0.0
prerequisites:
- '[[Critical_Section]]'
weaknesses: []
strengths: []
last_evaluated: 2026-07-28
courses:
- C02
---

Mutex (mutual exclusion lock) đảm bảo chỉ một luồng vào [[Critical_Section]] một lúc:
`lock()` → thao tác → `unlock()`. Đây là **khoá bi quan** (pessimistic) ở tầng ứng dụng.

Cạm bẫy: quên `unlock` (dùng `defer`/`try-finally`), khoá quá rộng (giảm throughput),
và [[Deadlock]] khi nhiều khoá lấy sai thứ tự. Tương đương ở DB là
[[Pessimistic_Locking]] (`SELECT ... FOR UPDATE`).
