---
topic: Tool Calling (Function Calling)
current_level: 'Level 1: Recognition'
mastery_score: 0.0
prerequisites:
- '[[Prompting]]'
weaknesses: []
strengths: []
last_evaluated: 2026-07-28
courses:
- C04
---

Tool calling cho [[Large_Language_Model]] **gọi hàm/API bên ngoài** thay vì chỉ nói. Bạn
mô tả các tool (tên, tham số) trong [[Prompting]]; khi cần, model trả về "hãy gọi
`get_weather(city='Hà Nội')`", chương trình của bạn chạy hàm rồi đưa kết quả lại cho model.

Điều này biến LLM từ "biết nói" thành "biết **làm**": tra DB, gửi email, chạy code. Analogy:
cho bộ não mượn đôi tay. Đây là mảnh ghép cốt lõi tạo nên [[AI_Agent]]; chuẩn mở để kết
nối tool là **MCP (Model Context Protocol)**.
