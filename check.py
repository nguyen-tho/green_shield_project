import json
import os

def infer_schema_from_json(json_data):
    """
    Suy luận schema từ một đối tượng JSON mẫu.
    Đây là hàm đệ quy để xử lý các cấu trúc lồng ghép.
    """
    schema = {}
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            field_info = {"required": True} # Mặc định coi là required
            if isinstance(value, str):
                field_info["type"] = "string"
            elif isinstance(value, int):
                field_info["type"] = "int"
            elif isinstance(value, float):
                field_info["type"] = "float"
            elif isinstance(value, bool):
                field_info["type"] = "bool"
            elif isinstance(value, dict):
                field_info["type"] = "object"
                field_info["fields"] = infer_schema_from_json(value)
            elif isinstance(value, list):
                field_info["type"] = "array"
                if value: # Nếu mảng không rỗng, suy luận schema cho các phần tử đầu tiên
                    first_item = value[0]
                    if isinstance(first_item, dict):
                        field_info["items"] = {
                            "type": "object",
                            "fields": infer_schema_from_json(first_item)
                        }
                    elif isinstance(first_item, str):
                        field_info["items"] = {"type": "string"}
                    elif isinstance(first_item, int):
                        field_info["items"] = {"type": "int"}
                    elif isinstance(first_item, float):
                        field_info["items"] = {"type": "float"}
                    elif isinstance(first_item, bool):
                        field_info["items"] = {"type": "bool"}
                    # Cần cân nhắc xử lý trường hợp mảng có các kiểu hỗn hợp hoặc rỗng
                    # Hiện tại, nếu mảng rỗng, items sẽ không được định nghĩa chi tiết
                    # Nếu mảng có kiểu hỗn hợp, nó sẽ lấy kiểu của phần tử đầu tiên.
                else:
                    # Nếu mảng rỗng, chúng ta chỉ biết nó là một mảng
                    # Không thể suy luận kiểu của các phần tử bên trong.
                    # Cần lưu ý rằng việc này có thể dẫn đến schema lỏng lẻo hơn cho các mảng rỗng.
                    field_info["items"] = {"type": "any"} # Hoặc một giá trị mặc định nào đó
            elif value is None:
                # Xử lý trường hợp giá trị là null (None trong Python)
                # Có thể cần định nghĩa rõ hơn type mong muốn nếu null được phép
                field_info["type"] = "null" # Hoặc "string", "int", v.v. tùy ngữ cảnh
                field_info["required"] = False # null thường ngụ ý không bắt buộc
            else:
                field_info["type"] = "unknown" # Xử lý các kiểu không xác định
            schema[key] = field_info
    elif isinstance(json_data, list):
        # Nếu JSON gốc là một list, chúng ta sẽ tạo một schema cho từng item trong list
        if json_data:
            return {"items": {"type": "object", "fields": infer_schema_from_json(json_data[0])}}
        else:
            return {"items": {"type": "any"}} # Nếu list rỗng
    return schema

def validate_json_structure(json_data, schema):
    """
    Kiểm tra cấu trúc của dữ liệu JSON dựa trên một schema đã định nghĩa.
    Sử dụng lại hàm validate_json_structure trước đó.
    """
    if not isinstance(json_data, dict) and not isinstance(json_data, list):
        return False, "Dữ liệu JSON gốc phải là một đối tượng (dictionary) hoặc mảng (list)."

    if isinstance(json_data, dict):
        for field_name, rules in schema.items():
            is_required = rules.get("required", False)
            field_type = rules.get("type")

            if field_name not in json_data:
                if is_required:
                    return False, f"Lỗi: Trường '{field_name}' là bắt buộc nhưng không có."
                continue

            field_value = json_data[field_name]

            # Kiểm tra kiểu dữ liệu
            if field_type == "string" and not isinstance(field_value, str):
                return False, f"Lỗi: Trường '{field_name}' phải là chuỗi."
            elif field_type == "int" and not isinstance(field_value, int):
                return False, f"Lỗi: Trường '{field_name}' phải là số nguyên."
            elif field_type == "float" and not isinstance(field_value, (int, float)):
                return False, f"Lỗi: Trường '{field_name}' phải là số thực."
            elif field_type == "bool" and not isinstance(field_value, bool):
                return False, f"Lỗi: Trường '{field_name}' phải là boolean."
            elif field_type == "object":
                if not isinstance(field_value, dict):
                    return False, f"Lỗi: Trường '{field_name}' phải là đối tượng."
                nested_schema = rules.get("fields")
                if nested_schema:
                    is_valid, msg = validate_json_structure(field_value, nested_schema)
                    if not is_valid:
                        return False, f"Lỗi trong trường '{field_name}': {msg}"
            elif field_type == "array":
                if not isinstance(field_value, list):
                    return False, f"Lỗi: Trường '{field_name}' phải là mảng."
                item_schema = rules.get("items")
                if item_schema:
                    for i, item in enumerate(field_value):
                        if item_schema["type"] == "object":
                            # Kiểm tra từng phần tử trong mảng nếu nó là object
                            is_valid, msg = validate_json_structure(item, item_schema["fields"])
                            if not is_valid:
                                return False, f"Lỗi trong mảng '{field_name}' tại phần tử thứ {i}: {msg}"
                        elif item_schema["type"] != "any": # Kiểm tra kiểu dữ liệu nếu không phải "any"
                            expected_type = {
                                "string": str,
                                "int": int,
                                "float": (int, float),
                                "bool": bool
                            }.get(item_schema["type"])
                            if expected_type and not isinstance(item, expected_type):
                                return False, f"Lỗi: Phần tử thứ {i} trong mảng '{field_name}' phải là kiểu '{item_schema['type']}'."
                # else: Nếu item_schema không được định nghĩa (mảng rỗng trong schema chuẩn)
                # thì chúng ta không có thông tin chi tiết về các phần tử
        return True, "Valid JSON structure"

    elif isinstance(json_data, list):
        # Nếu JSON gốc là một list
        if "items" in schema and schema["items"]["type"] == "object":
            item_fields_schema = schema["items"]["fields"]
            for i, item in enumerate(json_data):
                if not isinstance(item, dict):
                    return False, f"Lỗi: Phần tử thứ {i} trong JSON gốc phải là đối tượng."
                is_valid, msg = validate_json_structure(item, item_fields_schema)
                if not is_valid:
                    return False, f"Lỗi trong phần tử thứ {i} của JSON gốc: {msg}"
            return True, "Valid JSON structure"
        elif "items" in schema and schema["items"]["type"] != "any":
            expected_type = {
                "string": str,
                "int": int,
                "float": (int, float),
                "bool": bool
            }.get(schema["items"]["type"])
            for i, item in enumerate(json_data):
                if expected_type and not isinstance(item, expected_type):
                    return False, f"Lỗi: Phần tử thứ {i} trong JSON gốc phải là kiểu '{schema['items']['type']}'."
            return True, "Valid JSON structure"
        elif "items" in schema and schema["items"]["type"] == "any":
            # Nếu schema cho phép bất kỳ loại item nào trong list
            return True, "Valid JSON structure"
        else:
            return False, "Lỗi: Schema không định nghĩa rõ ràng cấu trúc cho các phần tử trong list gốc."
    return False, "Dữ liệu JSON không hợp lệ."


def load_json_file(filepath):
    """Tải dữ liệu từ file JSON."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return True, data
    except FileNotFoundError:
        return False, f"Lỗi: Không tìm thấy file '{filepath}'."
    except json.JSONDecodeError as e:
        return False, f"Lỗi cú pháp JSON trong file '{filepath}': {e}"
    except Exception as e:
        return False, f"Lỗi khi đọc file '{filepath}': {e}"

def check_all_json_files_for_consistency(root_dir="ConvertedQuiz"):
    """
    Kiểm tra sự đồng nhất cấu trúc của tất cả các file JSON trong thư mục gốc.
    """
    json_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".json"):
                json_files.append(os.path.join(dirpath, filename))

    if not json_files:
        print(f"Không tìm thấy file JSON nào trong thư mục '{root_dir}'.")
        return

    print(f"Tìm thấy {len(json_files)} file JSON. Đang kiểm tra tính đồng nhất...")

    # 1. Lấy file JSON đầu tiên làm chuẩn
    first_file_path = json_files[0]
    print(f"\nSử dụng '{first_file_path}' làm file chuẩn để so sánh cấu trúc.")
    status, reference_data = load_json_file(first_file_path)

    if not status:
        print(f"Lỗi: Không thể tải hoặc parse file chuẩn '{first_file_path}'. Vui lòng kiểm tra file này.")
        print(f"Chi tiết lỗi: {reference_data}")
        return

    # Suy luận schema từ file chuẩn
    reference_schema = infer_schema_from_json(reference_data)
    print("\nSchema được suy luận từ file chuẩn:")
    # print(json.dumps(reference_schema, indent=4, ensure_ascii=False)) # In ra schema nếu muốn kiểm tra

    all_consistent = True
    inconsistent_files = []

    # 2. Kiểm tra từng file JSON còn lại
    for i, file_path in enumerate(json_files):
        if file_path == first_file_path:
            continue # Bỏ qua file chuẩn

        print(f"\nĐang kiểm tra file: {file_path}")
        status, current_data = load_json_file(file_path)

        if not status:
            print(f"  --> KHÔNG HỢP LỆ: {current_data}")
            inconsistent_files.append((file_path, current_data))
            all_consistent = False
            continue

        is_valid, message = validate_json_structure(current_data, reference_schema)

        if is_valid:
            print(f"  --> HỢP LỆ. Cấu trúc đồng nhất với file chuẩn.")
        else:
            print(f"  --> KHÔNG HỢP LỆ: Cấu trúc KHÔNG đồng nhất. Lỗi: {message}")
            inconsistent_files.append((file_path, message))
            all_consistent = False

    print("\n--- TÓM TẮT KẾT QUẢ ---")
    if all_consistent:
        print("✅ Tất cả các file JSON đều có cấu trúc đồng nhất.")
    else:
        print("❌ Có file JSON có cấu trúc KHÔNG đồng nhất.")
        print("Các file không đồng nhất:")
        for fp, err_msg in inconsistent_files:
            print(f"- {fp}: {err_msg}")
        
        
check_all_json_files_for_consistency("ConvertedQuiz")