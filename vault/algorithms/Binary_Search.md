---
topic: "Binary Search"
current_level: "Level 2: Operation"
mastery_score: 0.0
prerequisites:
  - "[[Big_O_Complexity]]"
weaknesses: []
strengths: []
courses: [C07]
last_evaluated: 2026-07-28
---

Tìm kiếm nhị phân: trên dữ liệu **đã sắp xếp**, mỗi bước loại nửa không gian → **O(log n)**.
Điều kiện tiên quyết là tính "đơn điệu" (sorted / monotonic predicate).

Cạm bẫy kinh điển: tính `mid = (lo + hi) / 2` tràn số → dùng `lo + (hi - lo) / 2`; và
lỗi biên (off-by-one) ở điều kiện `lo <= hi`. Biến thể mạnh: **binary search trên đáp án**
(tìm ngưỡng nhỏ nhất thoả điều kiện).

**Áp dụng (domain):** range scan trong DB index ([[BTree_Index]]), `git bisect`, tra bảng
sorted, tìm ngưỡng cấu hình.
