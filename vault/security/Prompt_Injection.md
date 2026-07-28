---
topic: "Prompt Injection (LLM Security)"
current_level: "Level 3: Anomaly Detection"
mastery_score: 0.0
prerequisites:
  - "[[Threat_Modeling]]"
weaknesses: []
strengths: []
courses: [C04, C08]
last_evaluated: 2026-07-28
---

Lỗ hổng đặc trưng của [[Large_Language_Model]]: đầu vào không tin cậy (nội dung web, file,
email mà agent đọc) chứa chỉ dẫn **ghi đè** system prompt → model làm theo kẻ tấn công.
Nguy nhất khi ghép [[Tool_Calling]]: **data exfiltration**, gọi tool phá hoại. "Indirect
prompt injection" = payload nằm trong dữ liệu agent tự lấy về.

**Phòng thủ (điều cần nhớ):** coi mọi nội dung ngoài là **không tin cậy** (không phải chỉ
dẫn); tách kênh dữ liệu vs lệnh; **least privilege cho tool** + người duyệt thao tác nguy
hiểm; lọc input/output; sandbox. Chính là guardrail của [[AI_Agent]] (và của PAL-Agent này).

**Cầu nối:** C04 (AI) × C08 (Security) — bản dịch của [[SQL_Injection]] sang thời LLM.
