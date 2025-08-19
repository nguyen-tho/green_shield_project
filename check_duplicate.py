import os
import json

def has_duplicate_questions_advanced(data):
    """
    Kiểm tra trùng lặp dựa trên ID và question_text.
    """
    questions = data.get("contents", [])[0].get("questions", [])
    seen_ids = set()
    seen_texts = set()
    duplicate_ids = set()
    duplicate_texts = set()
    
    for q in questions:
        q_id = q.get("question_id")
        q_text = q.get("question_text")
        
        if q_id in seen_ids:
            duplicate_ids.add(q_id)
        else:
            seen_ids.add(q_id)
            
        if q_text in seen_texts:
            duplicate_texts.add(q_text)
        else:
            seen_texts.add(q_text)
            
    return list(duplicate_ids), list(duplicate_texts)

def check_all_quizzes(base_dir):
    """
    Duyệt qua tất cả các tệp JSON và kiểm tra trùng lặp.
    """
    total_files = 0
    duplicates_found = False

    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                total_files += 1
                
                print(f"Kiểm tra tệp: {file_path}")
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        
                        duplicate_ids, duplicate_texts = has_duplicate_questions_advanced(data)
                        
                        if duplicate_ids or duplicate_texts:
                            duplicates_found = True
                            print("    ❌ Phát hiện trùng lặp!")
                            if duplicate_ids:
                                print(f"        - Trùng ID: {duplicate_ids}")
                            if duplicate_texts:
                                print(f"        - Trùng nội dung: {duplicate_texts}")
                        else:
                            print("    ✅ Không có trùng lặp.")
                except json.JSONDecodeError:
                    print(f"    ⚠️ Lỗi đọc tệp JSON: {file_path}")
                except IndexError:
                    print(f"    ⚠️ Cấu trúc dữ liệu không hợp lệ: {file_path}")
                print("-" * 30)

    if not duplicates_found:
        print(f"🎉 Hoàn thành kiểm tra {total_files} tệp. Không phát hiện trùng lặp nào.")

# Giả sử thư mục gốc là 'ConvertedQuiz'
base_directory = 'ConvertedQuiz'
check_all_quizzes(base_directory)