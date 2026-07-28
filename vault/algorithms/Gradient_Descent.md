---
topic: "Gradient Descent"
current_level: "Level 3: Anomaly Detection"
mastery_score: 0.0
prerequisites:
  - "[[Big_O_Complexity]]"
weaknesses: []
strengths: []
courses: [C04, C07]
last_evaluated: 2026-07-28
---

Thuật toán **tối ưu** lặp: đi ngược hướng đạo hàm (gradient) của hàm mất mát để giảm dần
sai số. Chính là cơ chế trong [[Training_And_Loss]] của [[Neural_Network]]. Biến thể:
**SGD** (dùng mini-batch, nhanh & nhiễu), Momentum, Adam.

Cạm bẫy: **learning rate** quá lớn → phân kỳ, quá nhỏ → hội tụ chậm; kẹt ở **local
minimum / saddle point**; gradient **vanishing/exploding** ở mạng sâu.

**Áp dụng (domain):** huấn luyện mọi mô hình ML/DL (C04) — đây là ví dụ rõ nhất cho việc
"một thuật toán tối ưu kinh điển là trái tim của AI hiện đại".
