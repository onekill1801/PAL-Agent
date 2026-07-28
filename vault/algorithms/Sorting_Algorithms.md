---
topic: "Sorting Algorithms"
current_level: "Level 2: Operation"
mastery_score: 0.0
prerequisites:
  - "[[Big_O_Complexity]]"
weaknesses: []
strengths: []
courses: [C03, C07]
last_evaluated: 2026-07-28
---

So sánh-đổi chỗ: **quicksort** (O(n log n) trung bình, O(n²) worst, in-place),
**mergesort** (O(n log n) ổn định, cần O(n) bộ nhớ phụ, hợp **external sort**),
**heapsort** (O(n log n), in-place, dùng [[Heap_PriorityQueue]]). Không so sánh:
counting/radix sort O(n) khi khoá số nguyên hẹp.

Khái niệm cần nhớ: **stable** (giữ thứ tự phần tử bằng nhau) và **external sort** (sắp
dữ liệu lớn hơn RAM bằng cách chia mảnh + merge trên đĩa).

**Áp dụng (domain):** DB `ORDER BY`, **merge join** & external sort (C03); chuẩn hoá dữ
liệu trước [[Binary_Search]].
