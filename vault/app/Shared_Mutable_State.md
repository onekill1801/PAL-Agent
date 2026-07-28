---
topic: "Shared Mutable State"
current_level: "Level 1: Recognition"
mastery_score: 0.0
prerequisites: []
weaknesses: []
strengths: []
last_evaluated: 2026-07-28
---

Trạng thái **vừa chia sẻ vừa thay đổi được** là gốc rễ của mọi [[Race_Condition]].
Nếu dữ liệu bất biến (immutable) hoặc không chia sẻ (thread-local, message passing)
thì không có đua tranh.

Không phải là: chỉ biến toàn cục. Bất kỳ ô nhớ nào ≥2 luồng cùng thấy và một luồng
ghi đều tính — field của object, phần tử slice/map, hàng trong DB. Chiến lược giảm
thiểu: bất biến hoá, giới hạn phạm vi, hoặc bao bằng [[Critical_Section]].
