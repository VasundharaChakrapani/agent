import os


def read_repository_file(file_path: str):
    """
    Securely reads repository files.
    Prevents directory traversal attacks.
    """

    # Security check
    if ".." in file_path:
        return "Security Error: Invalid file path"

    # File existence check
    if not os.path.exists(file_path):
        return "Error: File does not exist"

    # Read file safely
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()