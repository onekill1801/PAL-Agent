---
topic: Optimistic Locking
current_level: 'Level 3: Anomaly Detection'
mastery_score: 0.0
prerequisites:
- '[[Lost_Update]]'
weaknesses: []
strengths: []
last_evaluated: 2026-07-28
courses:
- C03
---

Khoá lạc quan: **không khoá khi đọc**, giả định ít xung đột. Mỗi hàng có cột `version`
(hoặc timestamp). Khi ghi: `UPDATE ... SET ..., version = version + 1 WHERE id = ? AND
version = <giá trị đã đọc>`. Nếu **0 dòng** bị ảnh hưởng ⇒ ai đó đã sửa trước ⇒ **retry**.

Hợp khi tranh chấp thấp, đọc nhiều ghi ít (throughput cao vì không giữ khoá). Ngược lại
tranh chấp cao thì retry storm — lúc đó [[Pessimistic_Locking]] tốt hơn. Chống trực tiếp
[[Lost_Update]].
