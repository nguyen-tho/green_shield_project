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
                    "score": 10, // giá trị điểm số theo độ khó 10, 20, 30
                    "explanation": "" //thông tin 
                },
```
## Một số bộ công cụ hỗ trợ tự động hoá trong việc xử lý các json data

1. edit.py
```txt
Input: các tập json data trong Quiz (bộ câu hỏi gốc)
Output: các tập json data trong ConvertedQuiz (bộ câu hỏi đã được xử lý)
Tính năng:
    Đồng nhất cấu trúc schema trong bộ câu hỏi gốc sao cho phù hợp với cấu trúc mẫu chuẩn
    Trả kết quả ra tập Output theo đúng thứ tự của Input
```

2. check.py
```txt
Input: các tập json data trong ConvertedQuiz
Output: Thông báo các file data đã đồng nhất về mặt cấu trúc schema hay chưa nếu có file nào chưa thông báo thì thống kê lại
Tính năng:
    Kiểm tra tính đồng nhất về mặt cấu trúc schema 
    Thống kê file nào chưa đồng nhất và nêu điểm chưa đồng nhất
    Tổng kết và báo cáo thống kê (thông báo ok nếu tất cả đồng nhất, nếu chưa thì hiện danh sách file chưa đồng nhất kèm cảnh báo)
```

3. question_counter.py
```txt
Input: các tập json data trong ConvertedQuiz
Output: Thông báo số lượng câu hỏi trong mỗi tập json câu hỏi
Tính năng:
    Đếm số lượng câu hỏi trong mỗi tập câu hỏi
    Kiểm tra đảm bảo mỗi tập json câu hỏi có ít nhất 3 câu hỏi
        Nếu thoả yêu cầu thì thông báo đã đạt yêu cầu và xuất danh sách các file đã đạt yêu cầu
        Nếu chưa thoả thì cảnh báo chưa đạt yêu cầu và xuất danh sách
```

4. get_folder_tree.py
```
Input: folder cần kiểm tra
Output: cấu trúc cây thư mục trong folder Input
Tính năng: 
    Xuất cây thư mục để quan sát ở màn hình terminal
```

5. update_quiz_answer.py
```txt
Input: các tập json data trong ConvertedQuiz (chưa xử lý)
Output: các tập json data trong ConvertedQuiz (đã xử lý)
Tính năng: 
    Tập Input có các file json chứa các câu hỏi dạng trắc nghiệm với các option riêng biệt đã được đồng nhất về 1 kiểu để lấy đáp án của câu hỏi
        Dạng 1: Đáp án được lấy thứ tự của các option (1,2,3,..n)
        Dạng 2: Đáp án được lấy theo index trong mảng các option (0,1,2,...n-1)
    Với việc đã đông nhất thủ công theo dạng 1 nhưng hệ thống cần dạng 2 thì có thể đồng nhất tự động bằng cách:
        question["answer"] = question["answer"] - 1
    Với việc đã đồng nhất thủ công theo dạng 2 nhưng hệ thống cần dạng 1 thì có thể đồng nhất tự động bằng cách:
        question["answer"] = question["answer"] + 1

    Cuối cùng lưu lại kết quả xử lý

    Lý do phải đồng nhất thủ công với tập Input:
        Do sự rối loạn và không thống nhất về dạng value trong field đáp án (nhất là trường hợp 1 file có cả 2 dạng)
        Cần sự kiểm soát và thống nhất chặt chẽ về mặt nội dung câu hỏi tránh trường hợp sai sót về mặt đáp án gây ảnh hưởng xấu đến trải nghiệm người dùng về sau
```
