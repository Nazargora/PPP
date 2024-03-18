import os
import argparse
import shutil

def install_flows(changed_files):
    print("Installing Flows")
    
    if changed_files:
        spec_files = [file for file in os.listdir("specs") if file.endswith(".json")]
        
        # Adjust the path to consider only the file name
        changed_files = [os.path.basename(file) for file in changed_files]
        
        files_to_copy = [file for file in changed_files if file in spec_files]
        
        if not files_to_copy:
            print("No matching files found in 'specs' directory. Skipping installation.")
        else:
            create_flow_spec(files_to_copy)
    else:
        print("No changed files provided. Skipping installation.")

def create_flow_spec(files_to_copy):
    if not os.path.exists("specs2"):
        os.makedirs("specs2")
    
    for file_name in files_to_copy:
        src = os.path.join("specs", file_name)
        dest = os.path.join("specs2", file_name)
        
        # Check if the file already exists in specs2
        if not os.path.exists(dest):
            shutil.copy(src, dest)
            print(f"Copied {file_name} to 'specs2' directory")
        else:
            print(f"File {file_name} already exists in 'specs2' directory")

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description='Add arg change')
    arg_parser.add_argument('--changed_files', nargs='+', required=True, help='List of space-separated changed file names')
    args = arg_parser.parse_args()
    changed_files = args.changed_files
    install_flows(changed_files)

