import os
import shutil


if __name__ == "__main__":
    # Set source and destination directories
    source_dir = os.path.join(os.getcwd(), "specs")  # Path relative to repository root
    destination_dir = os.path.join(os.getcwd(), "specs2")  # Path relative to repository root

def move_files(source_dir, destination_dir, changed_files):
    for file in changed_files:
        source_path = os.path.join(source_dir, file)
        destination_path = os.path.join(destination_dir, file)
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)
        shutil.copyfile(source_path, destination_path)

    if __name__ == "__main__":
    # Set source and destination directories
    source_dir = os.path.join(os.getcwd(), "specs")  # Path relative to repository root
    destination_dir = os.path.join(os.getcwd(), "specs2")


    # Fetch list of changed files from environment variable
    changed_files_str = os.getenv('CHANGED_FILES')
    if changed_files_str:
        changed_files = changed_files_str.split("\n")
        move_files(source_dir, destination_dir, changed_files)
    else:
        print("No changed files found.")
