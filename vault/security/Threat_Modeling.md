---
topic: "Threat Modeling"
current_level: "Level 2: Operation"
mastery_score: 0.0
prerequisites: []
weaknesses: []
strengths: []
courses: [C08]
last_evaluated: 2026-07-28
---

Threat modeling = **có hệ thống hỏi "cái gì có thể sai?"** trước khi kẻ tấn công hỏi hộ.
Quy trình: vẽ **data flow + trust boundary** → liệt kê tài sản → duyệt **STRIDE**
(Spoofing, Tampering, Repudiation, Info disclosure, DoS, Elevation of privilege) → xếp
rủi ro → chọn biện pháp.

Neo vào mục tiêu **CIA**: Confidentiality, Integrity, Availability. Nguyên tắc nền:
**không tin đầu vào**, giả định vành đai sẽ thủng, giảm **attack surface**.

**Cầu nối:** là khung chung cho mọi lỗ hổng — [[Buffer_Overflow]], [[SQL_Injection]],
[[Prompt_Injection]]… đều bắt đầu từ một trust boundary bị vượt qua.
