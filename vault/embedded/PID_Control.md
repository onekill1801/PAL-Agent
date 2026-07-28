---
topic: "PID Control"
current_level: "Level 3: Anomaly Detection"
mastery_score: 0.0
prerequisites:
  - "[[Sensors_Actuators]]"
weaknesses: []
strengths: []
courses: [C07, C09]
last_evaluated: 2026-07-28
---

Bộ điều khiển phản hồi: tính **sai số** e = mục tiêu − đo được, rồi xuất điều khiển =
**Kp·e + Ki·∫e + Kd·de/dt**. P (phản ứng theo sai số), I (khử sai số tồn dư), D (giảm vọt lố,
dựa xu hướng). Là **thuật toán** điều khiển kinh điển (nên cũng thuộc C07).

Tinh chỉnh (tuning): Kp lớn → dao động; thiếu D → vọt lố; I quá lớn → **integral windup**
(kẹp giá trị I). Ứng dụng: giữ nhiệt, tốc độ motor, và giữ thăng bằng [[Drone_FlightController]].

**Cầu nối:** C07 (thuật toán điều khiển) × C09 (chạy trên MCU với [[Sensors_Actuators]]).
