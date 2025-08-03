import os

def list_directory_tree(path):
    """
    Prints the directory tree of the specified path.

    Args:
        path (str): The path to the directory.
    """
    print(f"Directory tree for: {path}")
    print("---")
    for root, dirs, files in os.walk(path):
        level = root.replace(path, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print(f'{indent}📂 {os.path.basename(root)}/')
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print(f'{subindent}📄 {f}')

# Example usage: Replace '.' with the path to the folder you want to list
list_directory_tree('ConvertedQuiz')