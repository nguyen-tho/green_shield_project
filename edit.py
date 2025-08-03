import json
import os
import re

def convert_nested_quiz_structure_preserving_folders(base_dataset_folder, output_base_folder):
    """
    Chuyển đổi cấu trúc các tệp JSON từ thư mục gốc của dataset (chứa L và P)
    sang định dạng mới với profile_id, mission_id và difficulty động,
    và lưu các tệp đã chuyển đổi vào một cấu trúc thư mục tương tự trong thư mục đầu ra.

    Đồng thời, hàm sẽ:
    - Thêm trường 'score' vào mỗi câu hỏi dựa trên 'difficulty' nếu chưa có.
    - Thêm trường 'explanation' rỗng vào mỗi câu hỏi nếu chưa có.
    - Đánh số lại 'question_id' trong mỗi tệp JSON đầu ra theo kiểu q1, q2, q3,...

    Args:
        base_dataset_folder (str): Đường dẫn đến thư mục gốc của dataset (ví dụ: 'Quiz' hoặc 'MyDataset').
        output_base_folder (str): Đường dẫn đến thư mục để lưu các tệp JSON đã chuyển đổi.
    """
    if not os.path.exists(output_base_folder):
        os.makedirs(output_base_folder)
        print(f"Đã tạo thư mục đầu ra: {output_base_folder}")

    # Duyệt qua các thư mục cấp cao nhất (L, P) trong base_dataset_folder
    for top_level_folder_name in os.listdir(base_dataset_folder):
        top_level_folder_path = os.path.join(base_dataset_folder, top_level_folder_name)

        if os.path.isdir(top_level_folder_path): # Đảm bảo đó là một thư mục (L hoặc P)

            # Tạo thư mục tương ứng trong output_base_folder
            output_top_level_folder_path = os.path.join(output_base_folder, top_level_folder_name)
            os.makedirs(output_top_level_folder_path, exist_ok=True)

            # Duyệt qua các thư mục con cấp 1 (L1, L2, P1, P2, ...)
            for profile_folder_name in os.listdir(top_level_folder_path):
                profile_folder_path = os.path.join(top_level_folder_path, profile_folder_name)

                if os.path.isdir(profile_folder_path): # Đảm bảo đó là một thư mục (L1, P1, v.v.)

                    # Tạo thư mục tương ứng trong output_top_level_folder_path
                    output_profile_folder_path = os.path.join(output_top_level_folder_path, profile_folder_name)
                    os.makedirs(output_profile_folder_path, exist_ok=True)

                    profile_id = None
                    profile_num = None

                    # Xác định profile_id dựa trên tên thư mục profile_folder_name
                    if re.match(r'^L\d+$', profile_folder_name):
                        profile_num = re.search(r'\d+', profile_folder_name).group()
                        profile_id = f"VD{profile_num}"
                    elif re.match(r'^P\d+$', profile_folder_name):
                        profile_num = re.search(r'\d+', profile_folder_name).group()
                        profile_id = f"HS{profile_num}"
                    else:
                        print(f"Cảnh báo: Không xác định được profile_id cho thư mục '{profile_folder_name}'. Bỏ qua.")
                        continue # Bỏ qua thư mục này nếu không khớp quy tắc

                    if profile_id:
                        # Duyệt qua các thư mục con cấp 2 (M1, M2, ...)
                        for mission_folder_name in os.listdir(profile_folder_path):
                            mission_folder_path = os.path.join(profile_folder_path, mission_folder_name)

                            if os.path.isdir(mission_folder_path) and re.match(r'^M\d+$', mission_folder_name):
                                
                                # Tạo thư mục tương ứng trong output_profile_folder_path
                                output_mission_folder_path = os.path.join(output_profile_folder_path, mission_folder_name)
                                os.makedirs(output_mission_folder_path, exist_ok=True)

                                mission_id = int(re.search(r'\d+', mission_folder_name).group())

                                # Duyệt qua các tệp JSON (easy.json, medium.json, hard.json)
                                for filename in os.listdir(mission_folder_path):
                                    if filename.endswith(".json"):
                                        input_filepath = os.path.join(mission_folder_path, filename)

                                        # Xác định difficulty từ tên file
                                        difficulty = filename.replace(".json", "").lower()
                                        if difficulty not in ["easy", "medium", "hard"]:
                                            print(f"Cảnh báo: Độ khó '{difficulty}' không chuẩn cho tệp '{filename}'.")
                                            # Bạn có thể chọn gán một giá trị mặc định hoặc bỏ qua

                                        try:
                                            with open(input_filepath, "r", encoding="utf-8") as f_in:
                                                old_json_data = json.load(f_in)

                                            # Tạo cấu trúc JSON mới cho từng tập hợp câu hỏi
                                            new_json_structure = {
                                                "appName": "Lá chắn xanh",
                                                "appVersion": "1.0.0",
                                                "appDescription": "",
                                                "appAuthor": "",
                                                "contents": [
                                                    {
                                                        "profile_id": profile_id,
                                                        "mission_id": mission_id,
                                                        "questions": []
                                                    }
                                                ]
                                            }

                                            # Đảm bảo old_json_data là một list để lặp qua
                                            questions_to_add = old_json_data if isinstance(old_json_data, list) else [old_json_data]

                                            for question_idx, question in enumerate(questions_to_add):
                                                # Gán difficulty cho từng câu hỏi
                                                if "difficulty" not in question:
                                                    question["difficulty"] = difficulty
                                                
                                                # Thêm trường 'score' nếu chưa có, dựa trên difficulty
                                                if "score" not in question:
                                                    if question.get("difficulty") == "easy":
                                                        question["score"] = 10
                                                    elif question.get("difficulty") == "medium":
                                                        question["score"] = 20
                                                    elif question.get("difficulty") == "hard":
                                                        question["score"] = 30
                                                    else:
                                                        question["score"] = 0 # Giá trị mặc định nếu difficulty không khớp

                                                # Thêm trường 'explanation' nếu chưa có, với giá trị rỗng
                                                if "explanation" not in question:
                                                    question["explanation"] = ""

                                                # Đánh số lại question_id
                                                question["question_id"] = f"q{question_idx + 1}"
                                                
                                                # Đồng nhất question options
                                                # Nếu có trường "options", đổi tên thành "question_options"
                                                if "options" in question:
                                                    question["question_options"] = question.pop("options")
                                                
                                                # Đồng nhất field đáp án
                                                # Nếu có trường "correct_answer_index", đổi tên thành "answer"
                                                if "correct_answer_index" in question:
                                                    question["answer"] = question.pop("correct_answer_index")
                                                new_json_structure["contents"][0]["questions"].append(question)
                                            
                                            # Tên tệp đầu ra sẽ giống tên tệp gốc (easy.json, medium.json, hard.json)
                                            output_filename = filename # Giữ nguyên tên file gốc
                                            output_filepath = os.path.join(output_mission_folder_path, output_filename)

                                            with open(output_filepath, "w", encoding="utf-8") as f_out:
                                                json.dump(new_json_structure, f_out, indent=2, ensure_ascii=False)

                                            # In ra đường dẫn tương đối để dễ đọc
                                            relative_input_path = os.path.relpath(input_filepath, base_dataset_folder)
                                            relative_output_path = os.path.relpath(output_filepath, output_base_folder)
                                            print(f"Đã chuyển đổi và chuẩn hóa '{relative_input_path}' -> '{relative_output_path}'")

                                        except json.JSONDecodeError as e:
                                            print(f"Lỗi cú pháp JSON trong tệp '{input_filepath}': {e}")
                                        except FileNotFoundError:
                                            print(f"Không tìm thấy tệp '{input_filepath}'.")
                                        except Exception as e:
                                            print(f"Đã xảy ra lỗi không mong muốn khi xử lý tệp '{input_filepath}': {e}")

# --- Cách sử dụng hàm ---

# Định nghĩa đường dẫn đến thư mục dataset gốc của bạn
# Ví dụ: nếu cấu trúc dataset của bạn bắt đầu từ thư mục 'Quiz'
# như trong ảnh bạn gửi (chứa L và P), thì base_dataset_dir sẽ là 'Quiz'.
base_dataset_dir = "Quiz" # Thay thế bằng đường dẫn thực tế đến dataset gốc của bạn

# Định nghĩa đường dẫn đến thư mục mà bạn muốn lưu kết quả đã chuyển đổi và chuẩn hóa
# Thư mục này sẽ có cấu trúc giống hệt thư mục gốc.
output_dir = "ConvertedQuiz"

# Gọi hàm chuyển đổi và chuẩn hóa
convert_nested_quiz_structure_preserving_folders(base_dataset_dir, output_dir)

print(f"\nQuá trình chuyển đổi và chuẩn hóa hoàn tất. Kiểm tra thư mục '{output_dir}' để xem kết quả.")