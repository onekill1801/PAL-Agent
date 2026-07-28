---
topic: "IMU & Sensor Fusion"
current_level: "Level 3: Anomaly Detection"
mastery_score: 0.0
prerequisites:
  - "[[Sensors_Actuators]]"
weaknesses: []
strengths: []
courses: [C07, C09]
last_evaluated: 2026-07-28
---

IMU = gyroscope (vận tốc góc) + accelerometer (gia tốc) [+ magnetometer]. Vấn đề: gyro
**trôi (drift)** theo thời gian, accel **nhiễu** khi rung. **Sensor fusion** kết hợp chúng để
ước lượng tư thế (orientation) chính xác.

Thuật toán: **complementary filter** (đơn giản: tin gyro ngắn hạn + accel dài hạn) hoặc
**Kalman filter** (tối ưu theo mô hình nhiễu — cũng là một thuật toán ước lượng, C07). Sai
fusion → drone lật.

**Cầu nối:** C07 (Kalman/lọc) × C09; đầu vào tư thế cho [[Drone_FlightController]].
