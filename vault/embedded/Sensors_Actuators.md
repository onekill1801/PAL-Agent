---
topic: "Sensors & Actuators"
current_level: "Level 2: Operation"
mastery_score: 0.0
prerequisites:
  - "[[I2C_SPI_UART]]"
weaknesses: []
strengths: []
courses: [C09]
last_evaluated: 2026-07-28
---

**Sensor** biến đại lượng vật lý → tín hiệu điện (nhiệt độ, gia tốc, ánh sáng, khoảng cách);
**actuator** làm ngược lại (motor, servo, van, LED). Vòng điều khiển = đọc sensor → tính →
xuất actuator.

Cần xử lý: **nhiễu** (lọc trung bình/thông thấp), **hiệu chỉnh (calibration)**, tần số lấy
mẫu đủ (Nyquist). Actuator cần driver công suất (motor không nối thẳng chân MCU — dùng
transistor/H-bridge).

**Cầu nối:** đầu vào cho [[PID_Control]] và [[IMU_Sensor_Fusion]]; vật lý cảm biến ở C10.
