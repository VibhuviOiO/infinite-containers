import os
import json
import base64
import requests

TARGET_KIBANA = os.getenv("KIBANA_URL", "https://localhost:5601")
KIBANA_USER = os.getenv("KIBANA_USER")
KIBANA_PASSWORD = os.getenv("KIBANA_PASSWORD")

HEADERS = {
    "elastic-api-version": "2023-10-31",
    "Content-Type": "application/json",
    "kbn-xsrf": "true"
}

if KIBANA_USER and KIBANA_PASSWORD:
    credentials = base64.b64encode(f"{KIBANA_USER}:{KIBANA_PASSWORD}".encode("utf-8")).decode("utf-8")
    HEADERS["Authorization"] = f"Basic {credentials}"

IMPORT_FOLDER = "exported_kibana_data"

def create_space(space_id):
    url = f"{TARGET_KIBANA}/api/spaces/space"
    payload = {"id": space_id, "name": space_id, "disabledFeatures": []}
    response = requests.post(url, headers=HEADERS, json=payload, verify=False)
    if response.status_code == 409:
        print(f"Space '{space_id}' already exists.")
    else:
        response.raise_for_status()
        print(f"Created space: {space_id}")

def import_saved_objects(space_id, file_path):
    url = f"{TARGET_KIBANA}/s/{space_id}/api/saved_objects/_import?createNewCopies=true"
    with open(file_path, "rb") as file:
        files = {"file": file}
        response = requests.post(url, headers={"kbn-xsrf": "true"}, files=files, verify=False)
        response.raise_for_status()
        print(f"Imported saved objects for space: {space_id}")

def main():
    for space_id in os.listdir(IMPORT_FOLDER):
        space_folder = os.path.join(IMPORT_FOLDER, space_id)
        if os.path.isdir(space_folder):
            create_space(space_id)
            file_path = os.path.join(space_folder, "saved_objects.ndjson")
            if os.path.exists(file_path):
                import_saved_objects(space_id, file_path)

if __name__ == "__main__":
    main()

"""
With Authentication
KIBANA_URL="https://your-kibana-host:5601" KIBANA_USER="your_user" KIBANA_PASSWORD="your_password" python3 import_spaces_and_saved_objects_by_space.py

Without Authentication
KIBANA_URL="https://your-kibana-host:5601" python3 import_spaces_and_saved_objects_by_space.py
"""