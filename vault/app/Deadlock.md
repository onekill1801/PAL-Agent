---
topic: "Deadlock"
current_level: "Level 3: Anomaly Detection"
mastery_score: 0.0
prerequisites:
  - "[[Mutex_Lock]]"
weaknesses: []
strengths: []
courses: [C02, C03, C09]
last_evaluated: 2026-07-28
---

Deadlock: hai (hay nhiều) luồng/giao dịch **chờ nhau vòng tròn** giữ tài nguyên → không ai
tiến. Cần đủ **4 điều kiện Coffman**: mutual exclusion, hold-and-wait, no preemption,
**circular wait**. Phá 1 điều kiện là hết deadlock.

**Phòng/xử lý (điều cần nhớ):** **lock ordering** (luôn khoá theo cùng thứ tự — phá circular
wait), `tryLock`/timeout, giữ [[Critical_Section]] ngắn, một khoá thay nhiều. DB tự **phát hiện**
deadlock và abort một giao dịch (nạn nhân) → app phải retry. Khác **livelock** (bận mà không tiến)
và **priority inversion** (xem [[RTOS_RealTime]]).

**Cầu nối:** C02 ([[Mutex_Lock]]), C03 ([[Pessimistic_Locking]]), C09 (real-time). Bà con với [[Race_Condition]].
