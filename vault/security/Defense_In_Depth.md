---
topic: "Defense in Depth"
current_level: "Level 2: Operation"
mastery_score: 0.0
prerequisites:
  - "[[Threat_Modeling]]"
weaknesses: []
strengths: []
courses: [C08]
last_evaluated: 2026-07-28
---

Phòng thủ **nhiều lớp**: không đặt cược vào một hàng rào duy nhất — một lớp thủng, lớp sau
vẫn chặn. Ví dụ: WAF → validate input → parameterized query → least-privilege DB → mã hoá
at-rest → giám sát/alert.

Nguyên tắc kèm theo: **fail secure** (lỗi thì khoá, không mở), **least privilege**,
**zero trust** (không tin theo vị trí mạng), giảm attack surface, và **giám sát + phản ứng**
(giả định sẽ bị xâm nhập). Bảo mật là quá trình, không phải tính năng bật một lần.

**Cầu nối:** khung hợp nhất mọi biện pháp của [[SQL_Injection]], [[XSS]],
[[Auth_And_Session]], [[Privilege_Escalation]].
