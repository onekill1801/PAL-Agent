---
topic: "XSS (Cross-Site Scripting)"
current_level: "Level 2: Operation"
mastery_score: 0.0
prerequisites:
  - "[[Threat_Modeling]]"
weaknesses: []
strengths: []
courses: [C08]
last_evaluated: 2026-07-28
---

Chèn **script chạy trong trình duyệt nạn nhân** do web nhả dữ liệu người dùng ra HTML mà
không khử. Ba loại: **stored** (lưu ở DB rồi phát lại), **reflected** (dội lại từ URL),
**DOM-based** (JS phía client). Hậu quả: trộm session, keylog, giả mạo hành động.

**Phòng thủ (điều cần nhớ):** **output encoding theo ngữ cảnh** (HTML/attr/JS/URL) — gốc;
**CSP** (Content-Security-Policy) hạn chế script; cookie `HttpOnly`/`SameSite`; khử input.
Framework hiện đại auto-escape — đừng phá bằng `innerHTML`/`dangerouslySetInnerHTML`.

**Cầu nối:** cùng nguyên lý "không tin input + khử ở ranh giới" như [[SQL_Injection]].
