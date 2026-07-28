---
topic: "RTOS & Real-Time"
current_level: "Level 3: Anomaly Detection"
mastery_score: 0.0
prerequisites:
  - "[[Microcontroller_GPIO]]"
weaknesses: []
strengths: []
courses: [C02, C09]
last_evaluated: 2026-07-28
---

Hệ thời gian thực: **đúng hạn (deadline) quan trọng ngang đúng kết quả**. **Hard real-time**
(trễ = hỏng: airbag, flight controller) vs **soft** (trễ = giảm chất lượng). RTOS
(FreeRTOS, Zephyr) cung cấp scheduler ưu tiên + task.

Vấn đề kinh điển (giao với concurrency C02): **priority inversion** (task thấp giữ khoá
chặn task cao → dùng priority inheritance), **jitter**, [[Race_Condition]] giữa ISR và task
(dùng critical section/queue). Đo bằng **WCET** (worst-case execution time), không phải trung bình.

**Cầu nối:** C02 — scheduling & đồng bộ, nhưng dưới ràng buộc thời gian cứng.
