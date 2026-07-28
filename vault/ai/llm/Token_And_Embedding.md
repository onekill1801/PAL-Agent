---
topic: Token & Embedding
current_level: 'Level 1: Recognition'
mastery_score: 0.0
prerequisites:
- '[[Large_Language_Model]]'
weaknesses: []
strengths: []
last_evaluated: 2026-07-28
courses:
- C04
---

**Token** = mẩu văn bản mà [[Large_Language_Model]] xử lý — thường là một từ hoặc mảnh
từ ("học", "máy", "ing"). Model không đọc chữ, nó đọc **dãy token**.

**Embedding** = biến mỗi token thành một **vector số** (danh sách số) sao cho từ gần
nghĩa nằm gần nhau trong không gian: "vua" − "đàn ông" + "đàn bà" ≈ "nữ hoàng".
Analogy: đặt mọi khái niệm lên một tấm bản đồ nhiều chiều, khoảng cách = độ giống nghĩa.
Embedding cũng là nền của [[RAG]] (tìm tài liệu theo nghĩa, không theo từ khoá).
