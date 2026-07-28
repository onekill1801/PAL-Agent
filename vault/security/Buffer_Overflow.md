---
topic: "Buffer Overflow"
current_level: "Level 3: Anomaly Detection"
mastery_score: 0.0
prerequisites:
  - "[[Threat_Modeling]]"
weaknesses: []
strengths: []
courses: [C01, C08]
last_evaluated: 2026-07-28
---

Ghi vượt biên vùng nhớ (buffer) → đè lên dữ liệu kề, kinh điển là **stack overflow** đè
**return address** → chuyển hướng thực thi. Gốc rễ: ngôn ngữ không kiểm biên (C/C++) +
[[Shared_Mutable_State]] bộ nhớ không kiểm soát. Anh em: heap overflow, **use-after-free**.

**Phòng thủ (điều cần nhớ):** dùng ngôn ngữ/hàm an toàn (bounds-checked), bật **stack
canary**, **ASLR**, **NX/DEP**, và fuzzing để phát hiện. Đây là lý do Rust/Go được ưa
cho code hệ thống mới.

**Cầu nối:** C01 (quản lý bộ nhớ). Hiểu cơ chế để **vá & phát hiện**, không để khai thác.
