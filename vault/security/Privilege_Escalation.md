---
topic: "Privilege Escalation"
current_level: "Level 3: Anomaly Detection"
mastery_score: 0.0
prerequisites:
  - "[[Threat_Modeling]]"
weaknesses: []
strengths: []
courses: [C08]
last_evaluated: 2026-07-28
---

Leo thang đặc quyền: từ quyền thấp → quyền cao. **Vertical** (user → admin/root),
**horizontal** (truy cập tài nguyên người dùng khác — IDOR). Bàn đạp thường gặp: cấu hình
sai, setuid, secret lộ, và **[[TOCTOU]]** (đua giữa lúc kiểm quyền và lúc dùng).

**Phòng thủ (điều cần nhớ):** **least privilege** (mỗi thành phần chỉ quyền tối thiểu),
kiểm authorization **phía server cho mọi request**, tách vai trò, kiểm tra-và-hành-động
nguyên tử để chặn TOCTOU, audit log. "Đừng tin client đã ẩn nút."

**Cầu nối:** C02 ([[TOCTOU]] là race dẫn tới escalation); nền của [[Defense_In_Depth]].
