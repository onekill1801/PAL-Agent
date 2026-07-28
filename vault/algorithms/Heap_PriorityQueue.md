---
topic: "Heap / Priority Queue"
current_level: "Level 2: Operation"
mastery_score: 0.0
prerequisites:
  - "[[Big_O_Complexity]]"
weaknesses: []
strengths: []
courses: [C02, C07]
last_evaluated: 2026-07-28
---

Binary heap: cây nhị phân "gần đầy" giữ tính chất **cha ≤ con** (min-heap). Lấy phần tử
nhỏ nhất O(1), push/pop **O(log n)**. Là hiện thực phổ biến của **priority queue**.

Mẹo: **top-k** dùng heap kích thước k → O(n log k) thay vì sort O(n log n). Cạm bẫy: heap
**không** cho tìm phần tử bất kỳ nhanh; và cập nhật ưu tiên (decrease-key) cần bản đồ vị trí.

**Áp dụng (domain):** scheduler luồng/tác vụ (C02), [[Dijkstra_ShortestPath]], rate limiter,
gộp log theo thời gian, event simulation.
