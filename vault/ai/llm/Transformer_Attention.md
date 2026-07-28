---
topic: Transformer & Attention
current_level: 'Level 1: Recognition'
mastery_score: 0.0
prerequisites:
- '[[Token_And_Embedding]]'
weaknesses: []
strengths: []
last_evaluated: 2026-07-28
courses:
- C04
---

Transformer là kiến trúc [[Neural_Network]] đứng sau mọi [[Large_Language_Model]] hiện
đại (bài báo 2017 "Attention Is All You Need"). Cơ chế cốt lõi là **attention**: khi xử
lý một [[Token_And_Embedding]], model **"chú ý"** tới những token liên quan trong ngữ cảnh.

Analogy: đọc câu "Con mèo không ăn vì **nó** no", để hiểu "nó" là ai, bạn tự động ngoái
lại "con mèo". Attention làm đúng vậy — tính trọng số liên quan giữa các từ. Ưu điểm:
xử lý **song song** cả câu (nhanh) và nắm được **ngữ cảnh xa**. Đây là bước nhảy giúp AI
ngôn ngữ bùng nổ.
