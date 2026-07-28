---
topic: "COURSE 01 — Low-Level Systems & Memory Management"
current_level: "Level 3: Anomaly Detection"
mastery_score: 0.0
prerequisites: []
weaknesses: []
strengths: []
tags: [moc, course]
last_evaluated: 2026-07-28
---

**Vùng tri thức:** C/C++, Linux kernel, custom allocator (`malloc`/`free`), đọc/ghi bộ
nhớ tiến trình, con trỏ, tránh memory leak.

## Mục tiêu Verify
- **L1–2:** quản lý bộ nhớ của OS — Heap, Stack, Virtual Memory, Page Fault.
- **L3–4:** memory fragmentation, race condition trên shared memory, tối ưu custom
  allocator dưới tải cao.

## Atomic notes
- Liên quan sẵn: [[Shared_Mutable_State]] (bộ nhớ chia sẻ)
- Sẽ tạo khi verify: `Virtual_Memory`, `Heap_vs_Stack`, `Page_Fault`,
  `Memory_Fragmentation`, `Custom_Allocator`
