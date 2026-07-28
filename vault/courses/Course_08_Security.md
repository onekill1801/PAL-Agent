---
topic: "COURSE 08 — Security & Vulnerability Engineering"
current_level: "Level 3: Anomaly Detection"
mastery_score: 0.0
prerequisites:
  - "[[Race_Condition]]"
weaknesses: []
strengths: []
tags: [moc, course]
courses: [C08]
last_evaluated: 2026-07-28
---

**Định hướng:** phòng thủ · pentest **được uỷ quyền** · giáo dục. Hiểu cơ chế lỗ hổng để
**phát hiện và vá**, threat modeling, hardening — không phục vụ tấn công trái phép.

**Vùng tri thức:** memory-safety exploit, web vuln (SQLi/XSS/SSRF), auth/session, crypto
misuse, privilege escalation, LLM/prompt injection, defense-in-depth.

## Mục tiêu Verify
- **L1–2:** phân loại lỗ hổng (OWASP), mô hình CIA, threat modeling cơ bản.
- **L3–4:** truy nguyên gốc lỗ hổng trong code thật + phác thảo bản vá; thiết kế phòng thủ
  nhiều lớp dưới ràng buộc.

## Cầu nối (lỗ hổng bám vào domain đã có)
- Bộ nhớ (C01): `Buffer_Overflow`, `Use_After_Free`
- Concurrency (C02): [[TOCTOU]] → race-based exploit
- Database (C03): `SQL_Injection`
- AI (C04): `Prompt_Injection`
- Giải thuật (C07): `Crypto_Basics` (hash, đối xứng/bất đối xứng)

## Atomic notes (sẽ tạo khi verify)
`Threat_Modeling` · `Buffer_Overflow` · `SQL_Injection` · `XSS` · `Auth_And_Session` ·
`Crypto_Basics` · `Privilege_Escalation` · `Defense_In_Depth` · `Prompt_Injection`
