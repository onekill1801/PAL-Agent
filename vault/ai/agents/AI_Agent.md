---
topic: AI Agent
current_level: 'Level 1: Recognition'
mastery_score: 0.0
prerequisites:
- '[[Tool_Calling]]'
- '[[RAG]]'
weaknesses: []
strengths: []
last_evaluated: 2026-07-28
courses:
- C04
- C06
---

AI Agent = [[Large_Language_Model]] chạy trong một **vòng lặp có mục tiêu**:
**quan sát → suy luận → hành động (dùng [[Tool_Calling]]) → quan sát kết quả → lặp lại**
cho tới khi xong việc. Khác chatbot ở chỗ nó **tự quyết nhiều bước** và **tác động ra
thế giới** (chạy lệnh, sửa file, gọi API).

Thành phần: model (bộ não) + tools (đôi tay) + **memory** (nhớ giữa các bước, thường qua
[[RAG]]) + vòng điều phối. Analogy: một nhân viên tự chủ — bạn giao mục tiêu, nó tự lên
kế hoạch và làm. Chính PAL-Agent (và toolkit bạn đang xây) là ví dụ agent. Rủi ro: sai
một bước có thể lan ra hành động thật → cần **guardrail** và người duyệt.
