import os
import json

def update_answer_in_json_files(root_folder):
    """
    Duyệt qua tất cả các file JSON trong cây thư mục và cập nhật 
    giá trị của trường 'answer' trong mỗi câu hỏi bằng cách trừ đi 1.

    Args:
        root_folder (str): Đường dẫn đến thư mục gốc để bắt đầu duyệt.
    """
    print(f"Bắt đầu duyệt và cập nhật các file JSON trong: {root_folder}\n")

    for dirpath, dirnames, filenames in os.walk(root_folder):
        for filename in filenames:
            # Lọc ra các file có đuôi .json
            if filename.endswith('.json'):
                file_path = os.path.join(dirpath, filename)
                print(f"Đang xử lý file: {file_path}")

                try:
                    # Đọc nội dung file JSON
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                    # Duyệt qua các nội dung và câu hỏi để cập nhật 'answer'
                    if 'contents' in data and isinstance(data['contents'], list):
                        for content in data['contents']:
                            if 'questions' in content and isinstance(content['questions'], list):
                                for question in content['questions']:
                                    if 'answer' in question and isinstance(question['answer'], int):
                                        # Trừ 1 từ giá trị 'answer'
                                        original_answer = question['answer']
                                        question['answer'] = original_answer - 1
                                        print(f"  - Cập nhật câu hỏi ID '{question.get('question_id', 'N/A')}': "
                                              f"answer từ {original_answer} -> {question['answer']}")
                    
                    # Ghi lại nội dung đã cập nhật vào file gốc
                    with open(file_path, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=4, ensure_ascii=False)
                    
                    print("  -> Cập nhật thành công.\n")

                except json.JSONDecodeError:
                    print(f"  -> Lỗi: File '{file_path}' không phải là một file JSON hợp lệ.\n")
                except Exception as e:
                    print(f"  -> Lỗi không xác định khi xử lý file '{file_path}': {e}\n")

# Thay đổi đường dẫn này thành thư mục gốc của bạn.
# Ví dụ: 'ConvertedQuiz' là thư mục gốc theo cấu trúc bạn đã cung cấp.
if __name__ == "__main__":
    root_directory = 'ConvertedQuiz'
    update_answer_in_json_files(root_directory)
    print("Hoàn tất việc cập nhật tất cả các file JSON.")