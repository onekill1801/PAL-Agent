---
topic: Critical Section
current_level: 'Level 1: Recognition'
mastery_score: 0.0
prerequisites:
- '[[Shared_Mutable_State]]'
weaknesses: []
strengths: []
last_evaluated: 2026-07-28
courses:
- C02
---

Critical section là **đoạn code truy cập [[Shared_Mutable_State]] cần được thực thi
độc quyền** (mutual exclusion) — tại một thời điểm chỉ một luồng được vào.

Nguyên tắc: giữ critical section **càng nhỏ càng tốt** (chỉ bao phần đọc-sửa-ghi),
vì khoá rộng làm giảm song song và dễ [[Deadlock]]. Được hiện thực bằng
[[Mutex_Lock]] (app) hoặc khoá hàng/bảng (DB).
