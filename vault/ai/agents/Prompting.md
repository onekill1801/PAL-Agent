---
topic: "Prompting"
current_level: "Level 1: Recognition"
mastery_score: 0.0
prerequisites:
  - "[[Large_Language_Model]]"
weaknesses: []
strengths: []
last_evaluated: 2026-07-28
---

Prompt = **chỉ dẫn bạn đưa cho** [[Large_Language_Model]]. Vì model chỉ đoán token tiếp
theo, cách bạn đặt câu quyết định rất lớn tới chất lượng. Thường có **system prompt**
(vai trò/luật chung) + **user prompt** (yêu cầu cụ thể).

Kỹ thuật cơ bản: nói rõ vai trò + định dạng đầu ra mong muốn; **few-shot** (cho vài ví dụ
mẫu); **chain-of-thought** ("hãy suy nghĩ từng bước"). Analogy: giao việc cho một thực
tập sinh cực giỏi nhưng chỉ biết đúng những gì bạn viết ra — mơ hồ thì nhận kết quả mơ hồ.
Đây là nền của [[Tool_Calling]] và [[RAG]].
