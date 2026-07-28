---
topic: "Knowledge Map — bản đồ tri thức"
tags: [moc, root]
last_evaluated: 2026-07-28
---

MOC gốc: **một graph tri thức duy nhất**, nhìn qua **6 thấu kính (course)** chồng lấn.
Course là *góc nhìn / lộ trình gợi ý*, KHÔNG phải ngăn tủ — một atomic note có thể thuộc
nhiều course (xem `courses:` trong frontmatter mỗi note).

## 6 thấu kính
- [[Course_01_LowLevel_Systems]] — bộ nhớ, allocator, kernel
- [[Course_02_Backend_Concurrency]] — Java/Go concurrency, reporting
- [[Course_03_Database_Engineering]] — SQL, index, transaction
- [[Course_04_Agentic_AI]] — agent, LLM, RAG, multi-node
- [[Course_05_GPU_Hardware_Tuning]] — GPU, nhiệt, inference 24/7
- [[Course_06_Enterprise_Modernization]] — legacy uplift, kiến trúc lớn

## Cầu nối liên-course (tri thức KHÔNG rời rạc)
- Bộ nhớ ⇄ Concurrency: [[Shared_Mutable_State]] (C01+C02)
- Concurrency ⇄ Database: [[Race_Condition]] ⇄ [[DB_Race_Condition]];
  [[Mutex_Lock]] ⇄ [[Pessimistic_Locking]]; [[TOCTOU]] → [[Pessimistic_Locking]]
- AI ⇄ GPU: [[Large_Language_Model]], [[Deep_Learning]], [[Inference_Parameters]] (C04+C05)
- AI ⇄ Enterprise: [[AI_Agent]] trong IOC (C04+C06)

## Nguyên tắc
1. Atomic note là gốc — 1 khái niệm, sống 1 chỗ, link tự do.
2. Course = tag `courses: [..]` (đa thành viên) + MOC, không phải thư mục.
3. Lộ trình học = chuỗi `prerequisites`, băng qua nhiều course.
