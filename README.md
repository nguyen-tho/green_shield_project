# green_shield_project
## Đây là repo chứa data được chuyển hoá từ tài liệu e-book "Lá chắn xanh" gốc sang dạng dữ liệu key-value (json) dê phục vụ cho việc CRUD dữ liệu dễ dàng hơn
## Cấu trúc cơ bản của ebook

```txt
app Lá chắn xanh ---
                    |
                    |----ebook-------|
                                     |------ Chương 1------|
                                                           |--------- Tiểu mục cấp 1 (1, 2, 3)------|
                                                                                                    |--------- Tiểu mục cấp 2 (1.1, 1.2)-----------|
                                                                                                                                                   |--------Tiểu mục cấp 3 (1.1.1, 1.1.2)-----------|
                                                                                                                                                                                                    |-------- Statement(ý chính)-------|
                                                                                                                                                                                                                                       |------- Substatement (ý phụ)----|
.......................................
Việc đặt các tên key sao cho phù hợp với tiêu đề của ebook
Yêu cầu phải lọc dữ liệu sao cho ngắn gọn, hàm súc, bao quát đầy đủ ý của ebook nhằm cho team DEV có thể truy vấn vào json được dễ dàng hơn


```

## Cấu trúc của một câu hỏi trắc nghiệm trong mini quiz
```json
{
                    "question_id": "q1", //id của câu hỏi
                    "question_text": "Ma túy làm hủy hoại sức khỏe, gây rối loạn sinh lý, và tàn phá các hệ cơ quan nào trong cơ thể?", // nội dung câu hỏi
                    "question_options": [ // 4 đáp án để lựa chọn
                        "Hệ tiêu hóa, hệ tuần hoàn, và hệ thần kinh.",
                        "Hệ hô hấp, hệ bài tiết, và hệ sinh sản",
                        "Hệ cơ xương, hệ miễn dịch, và hệ nội tiết",
                        "Hệ bạch huyết, hệ giác quan, và hệ vận động."
                    ],
                    "answer": 0, // index của đáp án đúng
                    "difficulty": "easy", // độ khó của câu hỏi có 3 cấp độ "easy", "medium", "hard"
                    "score": 10 // giá trị điểm số theo độ khó 10, 20, 30
                },
```
