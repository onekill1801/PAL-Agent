---
topic: "Big-O Complexity"
current_level: "Level 2: Operation"
mastery_score: 0.0
prerequisites: []
weaknesses: []
strengths: []
courses: [C07]
last_evaluated: 2026-07-28
---

Big-O mô tả **tốc độ tăng của chi phí (thời gian/bộ nhớ) theo kích thước đầu vào n**,
bỏ hằng số và số hạng bậc thấp. Thang quen thuộc: O(1) < O(log n) < O(n) < O(n log n)
< O(n²) < O(2ⁿ).

Không phải là: thời gian chạy thực tế (đó phụ thuộc phần cứng/hằng số) — Big-O nói về
**khả năng mở rộng**. Cạm bẫy: quên **độ phức tạp ẩn** (vd `list.contains` trong vòng lặp
→ O(n²)); và **worst vs average** (Hash O(1) trung bình nhưng O(n) khi đụng độ nhiều).

**Áp dụng (domain):** mọi domain — là ngôn ngữ chung để so sánh giải pháp.
