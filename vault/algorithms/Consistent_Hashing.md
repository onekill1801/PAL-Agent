---
topic: "Consistent Hashing"
current_level: "Level 3: Anomaly Detection"
mastery_score: 0.0
prerequisites:
  - "[[Hash_Table]]"
weaknesses: []
strengths: []
courses: [C03, C07]
last_evaluated: 2026-07-28
---

Khi sharding dữ liệu ra N node, [[Hash_Table]] kiểu `hash(key) % N` gặp thảm hoạ: đổi N
→ **hầu hết khoá phải remap**. Consistent hashing đặt node và khoá lên **vòng tròn hash**;
mỗi khoá thuộc node kế tiếp theo chiều kim đồng hồ → thêm/bớt 1 node chỉ dời **~1/N khoá**.

Cạm bẫy: phân bố lệch (một node ôm nhiều khoá) → dùng **virtual nodes** (mỗi node xuất
hiện nhiều điểm trên vòng) để cân bằng.

**Áp dụng (domain):** sharding DB/cache (C03), phân phối trong Redis Cluster/Cassandra/
DynamoDB, load balancing, CDN.
