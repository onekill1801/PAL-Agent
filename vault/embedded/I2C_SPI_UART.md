---
topic: "I2C / SPI / UART (giao thức nội bộ)"
current_level: "Level 2: Operation"
mastery_score: 0.0
prerequisites:
  - "[[Microcontroller_GPIO]]"
weaknesses: []
strengths: []
courses: [C09]
last_evaluated: 2026-07-28
---

Ba bus nối MCU với cảm biến/chip:
- **UART**: nối tiếp bất đồng bộ, 2 dây (TX/RX), điểm-điểm, cần khớp **baud rate**.
- **SPI**: đồng bộ, 4 dây (MOSI/MISO/SCLK/CS), **nhanh**, full-duplex, mỗi thiết bị 1 CS.
- **I2C**: 2 dây (SDA/SCL), nhiều thiết bị chung bus theo **địa chỉ**, chậm hơn, cần pull-up.

Chọn: I2C khi nhiều cảm biến chậm/ít dây; SPI khi cần tốc độ (màn hình, ADC); UART cho
GPS/module/serial debug. Cạm bẫy: xung đột địa chỉ I2C, quên pull-up, sai mức điện áp 3V3/5V.

**Cầu nối:** đường dẫn dữ liệu tới [[Sensors_Actuators]].
