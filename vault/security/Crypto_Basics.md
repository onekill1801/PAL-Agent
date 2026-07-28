---
topic: "Cryptography Basics"
current_level: "Level 2: Operation"
mastery_score: 0.0
prerequisites:
  - "[[Threat_Modeling]]"
weaknesses: []
strengths: []
courses: [C07, C08]
last_evaluated: 2026-07-28
---

Ba trụ cột: **đối xứng** (AES — nhanh, cùng khoá; cần trao khoá an toàn), **bất đối xứng**
(RSA/ECC — cặp public/private, ký & trao khoá), **hash** (SHA-256 — một chiều, toàn vẹn).
TLS ghép cả ba: bắt tay bất đối xứng → khoá phiên đối xứng.

**Phòng thủ (misuse cần tránh):** tự chế thuật toán; ECB mode (lộ mẫu); hardcode khoá;
RNG yếu (không dùng `Math.random` cho khoá); hash mật khẩu bằng SHA trần (phải argon2 —
xem [[Auth_And_Session]]). Nguyên tắc: **"don't roll your own crypto"**, dùng thư viện đã kiểm.

**Cầu nối:** C07 — hash & modular arithmetic là giải thuật; nền cho chữ ký số, blockchain.
