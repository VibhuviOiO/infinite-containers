import os
import json
import base64
import requests

SOURCE_KIBANA = os.getenv("KIBANA_URL", "https://localhost:5601")
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

EXPORT_FOLDER = "exported_kibana_data"

def get_spaces():
    url = f"{SOURCE_KIBANA}/api/spaces/space"
    response = requests.get(url, headers=HEADERS, verify=False)
    response.raise_for_status()
    return response.json()

def export_saved_objects(space_id):
    url = f"{SOURCE_KIBANA}/s/{space_id}/api/saved_objects/_export"
    payload = {"type": ["dashboard", "visualization", "index-pattern", "search"], "includeReferencesDeep": True}
    response = requests.post(url, headers=HEADERS, json=payload, verify=False)
    response.raise_for_status()
    return response.content

def save_to_local(space_id, data):
    space_folder = os.path.join(EXPORT_FOLDER, space_id)
    os.makedirs(space_folder, exist_ok=True)
    file_path = os.path.join(space_folder, "saved_objects.ndjson")
    with open(file_path, "wb") as file:
        file.write(data)

def main():
    os.makedirs(EXPORT_FOLDER, exist_ok=True)
    spaces = get_spaces()

    for space in spaces:
        space_id = space["id"]
        print(f"Exporting saved objects for space: {space_id}")
        saved_objects = export_saved_objects(space_id)
        save_to_local(space_id, saved_objects)

if __name__ == "__main__":
    main()

"""
With Authentication
KIBANA_URL="https://your-kibana-host:5601" KIBANA_USER="your_user" KIBANA_PASSWORD="your_password" python3 export_spaces_and_saved_objects_by_space.py

Without Authentication
KIBANA_URL="https://your-kibana-host:5601" python3 export_spaces_and_saved_objects_by_space.py
"""