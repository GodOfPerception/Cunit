import json
import os
import random
import string
import time
import shutil

global file_name

def process_json(input_json):
    data = json.loads(input_json)

    for item in data.get('item', []):
        name = item.get('name', '')
        response_list = item.get('response', [])
        
        if response_list:
            response_body = response_list[0].get('body', '')
        else:
            response_body = ''

        folder_name = data.get('info', {}).get('name', '')

        folder_path = os.path.join('/Users/shashank.shrivastav/Desktop/', folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        with open(os.path.join(folder_path, f"{name}_endpoint.json"), 'w') as file:
            file.write(response_body)
            



def generate_random_value(data_type):
    if data_type == "string":
        return ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    elif data_type == "number":
        return random.uniform(0, 100)
    elif data_type == "boolean":
        return random.choice([True, False])
    elif data_type == "null":
        return None
    elif data_type == "list":
        return [generate_random_value("string") for _ in range(3)]
    elif data_type == "object":
        return {"field_" + str(i): generate_random_value("string") for i in range(3)}
    else:
        raise ValueError("Unsupported data type: {}".format(data_type))

def generate_random_json(json_data):
    if isinstance(json_data, dict):
        return {key: generate_random_json(value) for key, value in json_data.items()}
    elif isinstance(json_data, list):
        return [generate_random_json(item) for item in json_data]
    elif isinstance(json_data, str):
        return generate_random_value("string")
    elif isinstance(json_data, int) or isinstance(json_data, float):
        return generate_random_value("number")
    elif isinstance(json_data, bool):
        return generate_random_value("boolean")
    elif json_data is None:
        return generate_random_value("null")
    else:
        return json_data

def process_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            try:
                with open(file_path, 'r') as file:
                    json_data = json.load(file)
                    
                if not json_data:
                    print(f"Skipping empty file: {filename}")
                    continue

                modified_json_data = generate_random_json(json_data)

                with open(file_path, 'w') as file:
                    json.dump(modified_json_data, file, indent=2)
            except json.JSONDecodeError as e:
                print(f"Error processing file {filename}: {e}")




def generate_yaml(folder_path):
    folder_name = os.path.basename(folder_path).replace(' ', '_')
    yaml_content = []

    for file_name in os.listdir(folder_path):
        if file_name.endswith('.json'):
            file_name_no_space = file_name.replace(' ', '_')
            endpoint = f"/{file_name_no_space[:-14]}" if file_name_no_space.endswith('_endpoint.json') else f"/{file_name_no_space[:-5]}"

            input_path = f"/integrations/coil_connectors/test-resources/input/{folder_name}/{file_name_no_space}"
            output_path = f"/integrations/coil_connectors/test-resources/output/{folder_name}/{file_name_no_space}"

            yaml_content.append(f'''
      - endpoint: "{endpoint}"
        requests:
          - input: "{input_path}"
        output: "{output_path}"
''')

    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    yaml_output_path = os.path.join(desktop_path, f"{folder_name}.yaml")
    with open(yaml_output_path, 'w') as yaml_file:
        yaml_file.write(''.join(yaml_content))




def copy_files_to_desktop(src_folder, dest_folder):
    if not os.path.exists(src_folder):
        print(f"Source folder '{src_folder}' does not exist.")
        wait_for_folder(src_folder)
        return

    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
        print(f"Destination folder '{dest_folder}' created.")

    for filename in os.listdir(src_folder):
        if filename.endswith(".json"):
            src_file_path = os.path.join("/private/var/tmp/", filename)

            if os.path.exists(src_file_path):
                dest_desktop_file_path = os.path.join(dest_folder, filename)

                shutil.copy(src_file_path, dest_desktop_file_path)
                print(f"File '{filename}' copied to '{dest_folder}'.")
            else:
                print(f"JSON file '{filename}' not found in /private/var/tmp/. Skipping.")

def wait_for_folder(folder_path):
    print(f"Waiting for '{folder_path}' to be generated...")
    while not os.path.exists(folder_path):
        time.sleep(1)  
    print(f"'{folder_path}' has been generated. Resuming the program.")






file_name = input ("Enter collection ")
with open(f'/Users/shashank.shrivastav/Desktop/{file_name}.json', 'r') as file:
    json_data = file.read()
process_json(json_data)

time.sleep(5)


desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
folder_path = os.path.join(desktop_path, file_name)
src_folder = os.path.join(desktop_path, file_name)
dest_folder = os.path.join(desktop_path, file_name)
time.sleep(5)

process_folder(folder_path)

time.sleep(5)


folder_path = f"/Users/shashank.shrivastav/Desktop/{file_name}"
generate_yaml(folder_path)

te = input("Did you generated the file")

if te=="yes":
    copy_files_to_desktop(src_folder, dest_folder)