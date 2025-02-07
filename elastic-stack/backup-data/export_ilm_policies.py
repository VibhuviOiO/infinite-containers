import os
import json
from elasticsearch7 import Elasticsearch

def save_to_file(data, folder, filename):
    os.makedirs(folder, exist_ok=True)
    with open(os.path.join(folder, filename), "w") as file:
        json.dump(data, file, indent=4)

def get_ilm_policies(es_client):
    response = es_client.transport.perform_request("GET", "/_ilm/policy")
    ilm_policies = response if isinstance(response, dict) else response.body if hasattr(response, "body") else response
    save_to_file(ilm_policies, "ilm_policies", "ilm_policies.json")
    return ilm_policies

def main():
    elastic_ip = os.getenv("ELASTIC_IP", "localhost")
    elastic_user = os.getenv("ELASTIC_USER")
    elastic_password = os.getenv("ELASTIC_PASSWORD")

    if elastic_user and elastic_password:
        es_client = Elasticsearch([f"http://{elastic_ip}:9200"], http_auth=(elastic_user, elastic_password))
    else:
        es_client = Elasticsearch([f"http://{elastic_ip}:9200"])

    get_ilm_policies(es_client)

if __name__ == "__main__":
    main()

"""
With Authentication
ELASTIC_IP="your_elastic_ip" ELASTIC_USER="your_elastic_user" ELASTIC_PASSWORD="your_elastic_password" python3 export_ilm_policies.py

Without Authentication
ELASTIC_IP="your_elastic_ip" python3 export_ilm_policies.py
"""
