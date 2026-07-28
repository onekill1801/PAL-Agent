---
topic: "LRU Cache"
current_level: "Level 2: Operation"
mastery_score: 0.0
prerequisites:
  - "[[Hash_Table]]"
weaknesses: []
strengths: []
courses: [C01, C03, C07]
last_evaluated: 2026-07-28
---

Least-Recently-Used: khi cache đầy, **loại phần tử lâu chưa dùng nhất**. Hiện thực O(1) =
[[Hash_Table]] (tra nhanh) + **doubly linked list** (giữ thứ tự dùng gần đây); mỗi lần
truy cập nhấc node lên đầu.

Cạm bẫy: LRU kém khi có **quét tuần tự lớn** (đẩy hết dữ liệu nóng ra — nên dùng LRU-K /
2Q / ARC); và trong đa luồng cần khoá ([[Race_Condition]]). So sánh: LFU (theo tần suất),
FIFO, Random.

**Áp dụng (domain):** **DB buffer pool** (C03), **CPU cache / page cache OS** (C01), CDN,
cache ứng dụng (Caffeine/Redis maxmemory-policy).
