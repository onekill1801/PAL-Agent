---
topic: "Microcontroller & GPIO"
current_level: "Level 2: Operation"
mastery_score: 0.0
prerequisites: []
weaknesses: []
strengths: []
courses: [C01, C09]
last_evaluated: 2026-07-28
---

Vi điều khiển (MCU: AVR, STM32, ESP32) = CPU + RAM + flash + ngoại vi trên một chip, chạy
"bare-metal" hoặc RTOS. Điều khiển phần cứng qua **thanh ghi** ánh xạ bộ nhớ (memory-mapped
register): set bit ở địa chỉ nhất định → bật/tắt chân **GPIO**.

Khái niệm nền: **digital vs analog (ADC/DAC)**, **PWM** (băm xung điều khiển độ sáng/tốc độ),
**interrupt** (ngắt — phản ứng sự kiện thay vì polling), tài nguyên **rất hạn chế** (KB RAM).

**Cầu nối:** C01 — lập trình sát phần cứng, thao tác bit/thanh ghi, không có OS che chắn.
Là nền cho [[I2C_SPI_UART]], [[RTOS_RealTime]].
