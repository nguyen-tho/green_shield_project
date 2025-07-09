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
