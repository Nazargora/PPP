import os
import argparse
import shutil

def install_flows(changed_files):
    print("Installing Flows")
    
    if changed_files:
        # Get the GitHub workspace directory
        github_workspace = os.getenv('GITHUB_WORKSPACE')
        
        specs_dir = os.path.join(github_workspace, "specs")
        
        if not os.path.exists(specs_dir):
            print(f"'specs' directory not found in {github_workspace}.")
            return
        
        spec_files = [file for file in os.listdir(specs_dir) if file.endswith(".json")]
        
        # Split the changed_files string into separate file names
        changed_files = changed_files.split()
        
        files_to_copy = [file for file in changed_files if file in spec_files]
        
        if not files_to_copy:
            print("No matching files found in 'specs' directory. Skipping installation.")
        else:
            create_flow_spec(files_to_copy, specs_dir)
    else:
        print("No changed files provided. Skipping installation.")

def create_flow_spec(files_to_copy, specs_dir):
    # Get the GitHub workspace directory
    github_workspace = os.getenv('GITHUB_WORKSPACE')
    
    specs2_dir = os.path.join(github_workspace, "specs2")
    
    if not os.path.exists(specs2_dir):
        os.makedirs(specs2_dir)
    
    for file_name in files_to_copy:
        src = os.path.join(specs_dir, file_name)
        dest = os.path.join(specs2_dir, file_name)
        
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
    changed_files = " ".join(args.changed_files)
    install_flows(changed_files)



