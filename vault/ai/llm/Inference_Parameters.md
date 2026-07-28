---
topic: "Inference Parameters (temperature, context)"
current_level: "Level 1: Recognition"
mastery_score: 0.0
prerequisites:
  - "[[Large_Language_Model]]"
weaknesses: []
strengths: []
last_evaluated: 2026-07-28
---

Khi [[Large_Language_Model]] sinh chữ (inference), có vài "núm vặn":
- **Temperature**: độ ngẫu nhiên. Thấp (0–0.3) → chắc chắn, lặp lại, hợp code/facts;
  cao (0.8–1) → sáng tạo, đa dạng, dễ lạc đề.
- **Context window**: "trí nhớ ngắn hạn" — tối đa bao nhiêu [[Token_And_Embedding]] model
  thấy cùng lúc (prompt + câu trả lời). Vượt quá thì phần cũ bị cắt.
- **Top-p / max tokens**: giới hạn lựa chọn từ / độ dài đầu ra.

Analogy: temperature như "độ liều" của người kể chuyện. Hiểu núm này = biết vì sao cùng
câu hỏi mà mỗi lần trả lời một khác, và cách điều khiển nó.
