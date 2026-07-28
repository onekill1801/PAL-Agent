---
topic: "Dynamic Programming"
current_level: "Level 3: Anomaly Detection"
mastery_score: 0.0
prerequisites:
  - "[[Big_O_Complexity]]"
weaknesses: []
strengths: []
courses: [C04, C07]
last_evaluated: 2026-07-28
---

DP giải bài toán bằng cách **chia thành bài con gối nhau** và **lưu lại kết quả** (memo)
để không tính lại. Điều kiện: **optimal substructure** + **overlapping subproblems**.
Hai kiểu: top-down (đệ quy + memo) và bottom-up (bảng).

Cạm bẫy: xác định sai **trạng thái** và **hàm chuyển** → sai toàn bộ; và bùng nổ bộ nhớ
(giảm bằng rolling array). Khác **greedy** (DP xét mọi lựa chọn, greedy chọn cục bộ).

**Áp dụng (domain):** **edit distance** (chính là cơ chế `diff`/git), sequence alignment
(bioinformatics), knapsack/tối ưu, và quy hoạch động trong RL (C04).
