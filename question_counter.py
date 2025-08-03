import json
import os

def get_question_count_from_quiz_file(filepath):
    """
    Đếm số lượng câu hỏi trong một file JSON của quiz.

    Args:
        filepath (str): Đường dẫn đến file JSON của quiz.

    Returns:
        tuple: (True, số lượng câu hỏi) nếu thành công và tìm thấy mảng questions.
               (False, thông báo lỗi) nếu có vấn đề khi đọc file hoặc không tìm thấy cấu trúc questions.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Kiểm tra cấu trúc cấp cao nhất
        if not isinstance(data, dict):
            return False, "Dữ liệu JSON gốc không phải là đối tượng."

        if "contents" not in data or not isinstance(data["contents"], list):
            return False, "Không tìm thấy trường 'contents' hoặc 'contents' không phải là mảng."

        total_questions = 0
        for content_item in data["contents"]:
            if not isinstance(content_item, dict):
                print(f"  Cảnh báo: Một phần tử trong 'contents' không phải là đối tượng. Bỏ qua.")
                continue

            if "questions" in content_item and isinstance(content_item["questions"], list):
                total_questions += len(content_item["questions"])
            else:
                print(f"  Cảnh báo: Không tìm thấy trường 'questions' hoặc 'questions' không phải là mảng trong content_item (profile_id: {content_item.get('profile_id', 'N/A')}).")
                # Nếu bạn muốn yêu cầu questions phải luôn có, bạn có thể trả về False ở đây
                # return False, f"Không tìm thấy mảng 'questions' trong content_item (profile_id: {content_item.get('profile_id', 'N/A')})."
        
        return True, total_questions

    except FileNotFoundError:
        return False, f"Lỗi: Không tìm thấy file '{filepath}'."
    except json.JSONDecodeError as e:
        return False, f"Lỗi cú pháp JSON trong file '{filepath}': {e}"
    except Exception as e:
        return False, f"Lỗi không xác định khi đọc file '{filepath}': {e}"
    
def check_all_quiz_files_for_question_count(root_dir="ConvertedQuiz"):
    """
    Kiểm tra và in ra số lượng câu hỏi của từng file JSON trong thư mục gốc và các thư mục con.
    """
    json_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".json"):
                json_files.append(os.path.join(dirpath, filename))

    if not json_files:
        print(f"Không tìm thấy file JSON nào trong thư mục '{root_dir}'.")
        return

    print(f"Tìm thấy {len(json_files)} file JSON. Đang kiểm tra số lượng câu hỏi...")

    # Danh sách các file json có ít hơn 3 câu hỏi
    passed_list = []
    not_passed_list = []
    for file_path in sorted(json_files): # Sắp xếp để dễ theo dõi
        print(f"\n--- Đang kiểm tra file: {file_path} ---")
        status, result = get_question_count_from_quiz_file(file_path)

        if status:
            print(f"  Tổng số câu hỏi: {result}")
        else:
            print(f"  Lỗi khi xử lý file: {result}")
        
        
        if status and result < 3:
            #print(f"  ⚠️ Cảnh báo: File '{file_path}' chỉ có {result} câu hỏi, ít hơn 3 câu hỏi yêu cầu.")
            not_passed_list.append((file_path, result))
        elif status and result >= 3:
            #print(f"  ✅ File '{file_path}' có {result} câu hỏi, đạt yêu cầu.")
            passed_list.append((file_path, result))
        elif not status:
            print(f"  ❌ Lỗi: {result}")
        
    for file, count in passed_list:
        print(f"  ✅ File '{file}' có {count} câu hỏi, đạt yêu cầu.")
    for file, count in not_passed_list:
        print(f"  ⚠️ Cảnh báo: File '{file}' chỉ có {count} câu hỏi, ít hơn 3 câu hỏi yêu cầu.")
if __name__ == "__main__":
    check_all_quiz_files_for_question_count("ConvertedQuiz")