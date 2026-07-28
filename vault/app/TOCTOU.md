---
topic: TOCTOU (Time-of-check to Time-of-use)
current_level: 'Level 3: Anomaly Detection'
mastery_score: 0.0
prerequisites:
- '[[Race_Condition]]'
weaknesses: []
strengths: []
last_evaluated: 2026-07-28
courses:
- C02
---

TOCTOU là [[Race_Condition]] nơi có **khoảng trống giữa lúc KIỂM TRA và lúc DÙNG**
một tài nguyên. Ví dụ: `if exists(file): open(file)` — file có thể bị xoá/đổi giữa hai
bước; hay `if balance >= amount: withdraw(amount)` chạy song song gây rút âm.

Không sửa được bằng kiểm tra kỹ hơn — phải làm **kiểm-tra-và-hành-động nguyên tử**:
khoá ([[Mutex_Lock]]/[[Pessimistic_Locking]]), thao tác atomic (CAS), hoặc ràng buộc
ở DB (`UPDATE ... WHERE balance >= amount`). Liên quan bảo mật: leo thang đặc quyền.
