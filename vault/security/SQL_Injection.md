---
topic: "SQL Injection"
current_level: "Level 2: Operation"
mastery_score: 0.0
prerequisites:
  - "[[Threat_Modeling]]"
weaknesses: []
strengths: []
courses: [C03, C08]
last_evaluated: 2026-07-28
---

Đầu vào không tin cậy bị **nối chuỗi vào câu SQL** → kẻ tấn công đổi cấu trúc truy vấn
(`' OR '1'='1`, `; DROP TABLE`, UNION-based, blind/boolean, time-based). Hậu quả: lộ/hỏng
dữ liệu, bypass auth.

**Phòng thủ (điều cần nhớ):** **prepared statement / parameterized query** (tách dữ liệu
khỏi lệnh) — biện pháp gốc; bổ sung: least-privilege DB user, whitelist input, ORM đúng
cách, WAF chỉ là lớp phụ. Không bao giờ tin "đã escape thủ công".

**Cầu nối:** C03 (Database). Cùng họ với injection khác: command/LDAP/NoSQL injection.
