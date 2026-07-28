---
topic: "Graph & Traversal (BFS/DFS)"
current_level: "Level 2: Operation"
mastery_score: 0.0
prerequisites:
  - "[[Big_O_Complexity]]"
weaknesses: []
strengths: []
courses: [C07]
last_evaluated: 2026-07-28
---

Đồ thị = đỉnh + cạnh (có/không hướng, có/không trọng số). Duyệt: **BFS** (hàng đợi, tìm
đường ngắn nhất theo số cạnh, theo tầng) và **DFS** (ngăn xếp/đệ quy, phát hiện chu trình,
topological sort). Chi phí **O(V + E)**.

Cạm bẫy: quên đánh dấu đã thăm → lặp vô hạn trên đồ thị có chu trình; chọn nhầm BFS/DFS
cho bài toán (đường ngắn nhất không trọng số → BFS, không phải DFS).

**Áp dụng (domain):** chính **knowledge graph của vault này** (`hydrate`, tìm orphan),
giải quyết phụ thuộc (build/package), mạng xã hội, web crawler; có trọng số → [[Dijkstra_ShortestPath]].
