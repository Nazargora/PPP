import argparse
import base64
import json
import logging
import os
from urllib.error import URLError, HTTPError
from urllib.request import Request, urlopen

logger = logging.getLogger()


arg_parser = argparse.ArgumentParser(description='Load JSON specs from git')
arg_parser.add_argument('-e', '--env', required=True,  help='Target environment destination')
arg_parser.add_argument('-c', '--credentials', required=True, help='Target env backend credential pair in format username:password')
arg_parser.add_argument('-cf', '--changed_files', nargs='+', required=True, help='List of space-separated changed file names')
arg_parser.add_argument('-f', '--folder_path', required=True, help='Folder path of flow specs')


def install_flows(changed_files_list, folder_path):
    print("Installing Files")

    if changed_files_list:

        specs_dir = os.path.join(folder_path, "specs")

        if not os.path.exists(specs_dir):
            print(f"'specs' directory not found in {folder_path}.")
            return

        spec_files = [file for file in os.listdir(specs_dir) if file.endswith(".json")]

        # Extract only the file names from the full paths
        files_to_copy = [os.path.basename(file) for file in changed_files_list if os.path.basename(file) in spec_files]

        if not files_to_copy:
            print("No matching files found in 'specs' directory. Skipping installation.")
        else:
            create_flow_spec(files_to_copy, specs_dir)
    else:
        print("No changed files provided. Skipping installation.")


def create_flow_spec(files_to_copy, specs_dir):
    upload_requests = []
    for file_name in files_to_copy:
        src = os.path.join(specs_dir, file_name)
        if os.path.exists(src):
            with open(src, 'r') as f:
                file_content = f.read()
                name = file_name
                language = name.split('_')[-1].split('.')[0].upper()
                if language == 'F' or language == 'G':
                    continue

                single_request = {
                    'name': name,
                    'jsonString': json.dumps(json.loads(file_content)),
                    'language': language,
                    'excelSheetVersionId': None
                }

                print(f'{name} is processed')
                upload_requests.append(single_request)
        else:
            print(f"File {file_name} not found in 'specs' directory.")

    if upload_requests:
        upload_json_spec(upload_requests, env, credentials)
    else:
        print("No valid files to upload.")


def upload_json_spec(upload_requests, base_url, credentials_pair):
    base64auth = base64.b64encode(bytes(credentials_pair, 'utf-8')).decode()

    req = Request(f'https://bc-{base_url}-be.azurewebsites.net/bcapi/admin-api/json-specs', method='PUT', data=json.dumps(upload_requests).encode())
    req.add_header('Content-Type', 'application/json')
    req.add_header('Authorization', f'Basic {base64auth}')

    try:
        response = urlopen(req)
        response.read()
        print(f"{len(upload_requests)} JSON have deployed")
    except HTTPError as e:
        print(f"Request failed: {e.code} {e.reason}")
    except URLError as e:
        print(f"Server connection failed: {e.reason}")


if __name__ == '__main__':
    args = arg_parser.parse_args()
    env = args.env
    credentials = args.credentials
    folder_path = args.folder_path
    changed_files_list = [filename.split('/')[-1] for filename in args.changed_files]

    install_flows(changed_files_list, folder_path)
