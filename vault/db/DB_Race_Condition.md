---
topic: "Race Condition trong Database"
current_level: "Level 1: Recognition"
mastery_score: 0.0
prerequisites:
  - "[[Race_Condition]]"
weaknesses: []
strengths: []
last_evaluated: 2026-07-28
---

Ở tầng DB, race condition xảy ra giữa các **transaction đồng thời** cùng đọc/ghi một
hàng. Các bất thường kinh điển: [[Lost_Update]], dirty read, non-repeatable read,
phantom read — được kiểm soát qua [[Transaction_Isolation_Levels]].

Không phải là: chuyện chỉ xảy ra khi "nhiều server". Ngay 1 app đa luồng nối 1 DB
cũng dính. Công cụ chống: [[Optimistic_Locking]] (version) và [[Pessimistic_Locking]]
(`FOR UPDATE`), hoặc dồn logic vào **một câu UPDATE có điều kiện** (atomic).
