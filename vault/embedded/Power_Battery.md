---
topic: "Power & Battery (nhúng)"
current_level: "Level 2: Operation"
mastery_score: 0.0
prerequisites: []
weaknesses: []
strengths: []
courses: [C09, C10]
last_evaluated: 2026-07-28
---

Thiết bị chạy pin sống chết vì **ngân sách năng lượng**. Khái niệm: dung lượng **mAh**,
điện áp cell (LiPo ~3.7V), dòng xả **C-rate**, và **sleep modes** của MCU (deep sleep µA).
Tuổi thọ ≈ dung lượng / dòng tiêu thụ trung bình.

Thực chiến: đo dòng thật, tắt ngoại vi khi rảnh, đánh thức theo interrupt, dùng
regulator hiệu suất cao. Với drone: pin nặng ↔ thời gian bay ↔ lực nâng — bài toán đánh đổi.

**Cầu nối:** C10 — bản chất là [[Electrochemistry_Battery]] (hóa học biến thành điện);
cấp nguồn cho [[Drone_FlightController]].
