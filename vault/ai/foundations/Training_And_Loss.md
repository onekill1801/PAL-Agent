---
topic: Training & Loss
current_level: 'Level 1: Recognition'
mastery_score: 0.0
prerequisites:
- '[[Neural_Network]]'
weaknesses: []
strengths: []
last_evaluated: 2026-07-28
courses:
- C04
---

Training = quá trình **chỉnh trọng số** của [[Neural_Network]] để đầu ra khớp dữ liệu.
Thước đo sai lệch gọi là **loss** (mất mát): dự đoán càng sai, loss càng cao. Mục tiêu là
**giảm loss** dần bằng thuật toán **gradient descent** (đi ngược hướng dốc của sai số).

Analogy: đi xuống núi trong sương mù — mỗi bước nhìn độ dốc dưới chân rồi bước xuống
thấp hơn, lặp lại tới đáy. Cạm bẫy: **overfitting** — học thuộc lòng dữ liệu luyện,
gặp dữ liệu mới thì sai. Chống bằng tách tập validation + regularization.
