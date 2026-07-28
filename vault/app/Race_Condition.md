---
topic: Race Condition (ứng dụng)
current_level: 'Level 2: Operation'
mastery_score: 20.0
prerequisites:
- '[[Shared_Mutable_State]]'
- '[[Critical_Section]]'
weaknesses:
- 'Câu 4: chưa nêu tính phi tất định → khó reproduce/flaky test'
strengths: []
last_evaluated: 2026-07-28
courses:
- C01
- C02
---

Race condition xảy ra khi **kết quả phụ thuộc vào thứ tự/timing** của nhiều luồng
truy cập cùng một [[Shared_Mutable_State]], trong đó **ít nhất một** thao tác là ghi,
và **không có đồng bộ hoá**. Kinh điển: `counter++` không phải nguyên tử — nó gồm
read → add → write; hai goroutine/thread xen kẽ làm mất cập nhật.

Không phải là: bug do "thiếu goroutine" hay "máy chậm". Thêm luồng KHÔNG sửa được;
phải bảo vệ [[Critical_Section]] bằng [[Mutex_Lock]] hoặc thiết kế không chia sẻ state.
Một biến thể tinh vi là [[TOCTOU]]. Ở tầng dữ liệu, xem [[DB_Race_Condition]].
