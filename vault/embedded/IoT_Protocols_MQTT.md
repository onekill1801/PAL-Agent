---
topic: "IoT Protocols (MQTT & bạn bè)"
current_level: "Level 2: Operation"
mastery_score: 0.0
prerequisites:
  - "[[Microcontroller_GPIO]]"
weaknesses: []
strengths: []
courses: [C09]
last_evaluated: 2026-07-28
---

Kết nối thiết bị lên mạng. **MQTT**: publish/subscribe qua broker, nhẹ, hợp mạng chập chờn;
có **QoS 0/1/2** (at-most/at-least/exactly once) và **retained/last-will**. Anh em: **CoAP**
(REST trên UDP cho thiết bị siêu nhỏ), HTTP (nặng hơn), **LoRaWAN/Zigbee/BLE** (tầm & năng lượng).

Chọn theo: băng thông, năng lượng (pin), độ trễ, tầm phủ. Cạm bẫy bảo mật: MQTT mặc định
**không mã hoá/không auth** → phải TLS + credential (xem C08); đây là bề mặt tấn công IoT điển hình.

**Cầu nối:** C08 (bảo mật IoT). Tải dữ liệu sensor lên cloud/agent.
