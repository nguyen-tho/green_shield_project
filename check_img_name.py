import json
import os

def check_image_names(root_folder, json_file_path):
    """
    Checks if the image filenames in each subfolder of the root folder
    match the 'image_name' attribute in the corresponding JSON data.

    Args:
        root_folder (str): The root path containing the drug-related folders.
        json_file_path (str): The path to the JSON file.
    """
    # Load the JSON data
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy file JSON tại đường dẫn '{json_file_path}'.")
        return
    except json.JSONDecodeError:
        print(f"Lỗi: File JSON '{json_file_path}' không hợp lệ.")
        return

    # Create a dictionary to map folder names to a list of image names
    image_map = {}
    for item in data.get('ref', []):
        folder = item.get('folder_name')
        image = item.get('image_name')
        if folder and image:
            if folder not in image_map:
                image_map[folder] = []
            image_map[folder].append(image)

    # Check each folder and its files
    for folder_name, image_names in image_map.items():
        full_folder_path = os.path.join(root_folder, folder_name)
        
        # Check if the folder exists
        if not os.path.exists(full_folder_path) or not os.path.isdir(full_folder_path):
            print(f"❌ Thư mục '{full_folder_path}' không tồn tại.")
            continue
        
        # Get the list of files in the folder
        files_in_folder = os.listdir(full_folder_path)
        
        print(f"Kiểm tra thư mục: '{folder_name}'")
        
        # Check if each image name from JSON is in the folder
        for img_name in image_names:
            if img_name in files_in_folder:
                print(f"✅ Khớp: '{img_name}' có trong thư mục '{folder_name}'.")
            else:
                print(f"❌ Không khớp: '{img_name}' không tìm thấy trong thư mục '{folder_name}'.")
        
        print("-" * 30)

# Main execution block
if __name__ == "__main__":
    folder_path = r"D:\Lá chắn xanh\green_shield_project\green_shield_project\ma_tuy"
    json_path = r"D:\Lá chắn xanh\green_shield_project\green_shield_project\ma_tuy\references.json"
    
    check_image_names(folder_path, json_path)