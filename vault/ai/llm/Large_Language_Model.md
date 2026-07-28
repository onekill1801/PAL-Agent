---
topic: Large Language Model (LLM)
current_level: 'Level 1: Recognition'
mastery_score: 0.0
prerequisites:
- '[[Deep_Learning]]'
weaknesses: []
strengths: []
last_evaluated: 2026-07-28
courses:
- C04
- C05
---

LLM (như GPT, Claude) là [[Deep_Learning]] khổng lồ, huấn luyện trên **lượng văn bản
cực lớn**, với một nhiệm vụ đơn giản đến bất ngờ: **đoán từ (token) kế tiếp**. Lặp việc
đoán đó nhiều lần → sinh ra câu, đoạn, cả bài.

Analogy: một người đọc gần hết Internet rồi chơi trò "điền từ còn thiếu" siêu giỏi.
Từ kỹ năng đoán đó "nảy sinh" khả năng tóm tắt, dịch, code. Kiến trúc lõi là
[[Transformer_Attention]]; đơn vị xử lý là [[Token_And_Embedding]]. Không phải là: tra
cứu cơ sở dữ liệu hay "hiểu" như người — nó **dự đoán xác suất**, nên có thể **bịa (hallucinate)**.
