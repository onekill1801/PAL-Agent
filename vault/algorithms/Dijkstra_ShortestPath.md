---
topic: "Dijkstra — Shortest Path"
current_level: "Level 3: Anomaly Detection"
mastery_score: 0.0
prerequisites:
  - "[[Graph_And_Traversal]]"
  - "[[Heap_PriorityQueue]]"
weaknesses: []
strengths: []
courses: [C07]
last_evaluated: 2026-07-28
---

Tìm đường ngắn nhất từ 1 nguồn trên đồ thị **trọng số không âm**: tham lam mở rộng đỉnh
gần nhất chưa chốt, dùng [[Heap_PriorityQueue]] → **O((V+E) log V)**.

Cạm bẫy quan trọng: **sai khi có cạnh âm** (dùng Bellman-Ford); nếu cần đường ngắn nhất
mọi cặp → Floyd-Warshall; thêm heuristic → A*. Không nhớ chốt đỉnh (visited) → lặp thừa.

**Áp dụng (domain):** định tuyến mạng/OSPF, bản đồ chỉ đường, và **chính hàm
`shortest_path` trong `memory/graph.py`** của PAL-Agent (lộ trình học giữa các note).
