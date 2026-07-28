---
topic: "Drone Flight Controller"
current_level: "Level 3: Anomaly Detection"
mastery_score: 0.0
prerequisites:
  - "[[PID_Control]]"
  - "[[IMU_Sensor_Fusion]]"
  - "[[Power_Battery]]"
weaknesses: []
strengths: []
courses: [C09, C10]
last_evaluated: 2026-07-28
---

Bộ não bay: vòng lặp real-time (thường **RTOS**, hàng trăm–nghìn Hz) đọc [[IMU_Sensor_Fusion]]
→ chạy [[PID_Control]] cho roll/pitch/yaw → xuất **PWM** tới 4 ESC/motor. Quadcopter giữ
thăng bằng bằng cách vi chỉnh tốc độ 4 cánh liên tục.

Vật lý (C10): lực nâng ∝ tốc độ cánh²; yaw nhờ chênh mô-men xoắn; trọng tâm & quán tính
quyết định độ ổn định. Hỏng thường gặp: loop quá chậm/jitter → mất ổn định; PID sai → dao động;
[[Power_Battery]] sụt áp khi tải → mất điều khiển.

**Cầu nối:** hội tụ C09 (điều khiển) + C10 (khí động/động lực học) + real-time (C02).
