---
topic: "Authentication & Session"
current_level: "Level 3: Anomaly Detection"
mastery_score: 0.0
prerequisites:
  - "[[Threat_Modeling]]"
weaknesses: []
strengths: []
courses: [C08]
last_evaluated: 2026-07-28
---

Phân biệt **authentication** (bạn là ai) vs **authorization** (bạn được làm gì) — lẫn hai
cái là nguồn lỗi lớn. Phiên: session cookie (server giữ state) vs **token/JWT** (self-
contained, khó thu hồi). Mật khẩu phải **hash chậm có salt**: bcrypt/scrypt/**argon2**,
KHÔNG md5/sha1 trần.

**Phòng thủ (điều cần nhớ):** MFA, chống brute-force (rate limit/lockout), quay vòng &
hết hạn token, chống fixation/CSRF, "deny by default". Lỗi kinh điển: IDOR (đổi id trên URL
truy cập tài nguyên người khác) — luôn kiểm authorization phía server.

**Cầu nối:** dùng [[Crypto_Basics]]; phòng escalation ở [[Privilege_Escalation]].
