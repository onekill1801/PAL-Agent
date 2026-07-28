---
topic: "RAG (Retrieval-Augmented Generation)"
current_level: "Level 1: Recognition"
mastery_score: 0.0
prerequisites:
  - "[[Prompting]]"
  - "[[Token_And_Embedding]]"
weaknesses: []
strengths: []
last_evaluated: 2026-07-28
---

RAG = **tìm tài liệu liên quan rồi nhét vào prompt** trước khi [[Large_Language_Model]]
trả lời. Giải quyết 2 điểm yếu của LLM: không biết dữ liệu riêng của bạn, và hay **bịa
(hallucinate)**.

Cách chạy: cắt tài liệu thành mẩu → tạo [[Token_And_Embedding]] cho từng mẩu, lưu vào
**vector database** → khi có câu hỏi, tìm mẩu gần nghĩa nhất → đưa kèm câu hỏi cho model.
Analogy: cho thí sinh **mở sách đúng trang** rồi mới hỏi. Không phải là: huấn luyện lại
model — RAG chỉ **cung cấp ngữ cảnh** lúc hỏi, rẻ và cập nhật nhanh.
