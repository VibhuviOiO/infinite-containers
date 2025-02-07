import os
import json
from elasticsearch7 import Elasticsearch

def load_from_file(folder, filename):
    """
    Load ILM policies from a JSON file.
    """
    file_path = os.path.join(folder, filename)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} not found.")

    with open(file_path, "r") as file:
        return json.load(file)

def sanitize_policy(policy_body):
    """
    Remove version, modified_date, and in_use_by fields from the policy body.
    """
    policy_body.pop("version", None)
    policy_body.pop("modified_date", None)
    policy_body.pop("in_use_by", None)
    return policy_body

def save_ilm_policies_to_new_cluster(es_client, ilm_policies):
    """
    Save ILM policies to the new Elasticsearch cluster.
    """
    headers = {"Content-Type": "application/json"}
    for policy_name, policy_body in ilm_policies.items():
        sanitized_policy = sanitize_policy(policy_body)
        response = es_client.transport.perform_request(
            "PUT", f"/_ilm/policy/{policy_name}", body=json.dumps(sanitized_policy), headers=headers
        )
        print(f"Policy {policy_name} saved: {response}")

def main():
    ilm_policies = load_from_file("ilm_policies", "ilm_policies.json")

    elastic_ip = os.getenv("ELASTIC_IP", "localhost")
    elastic_user = os.getenv("ELASTIC_USER")
    elastic_password = os.getenv("ELASTIC_PASSWORD")

    if elastic_user and elastic_password:
        dest_es = Elasticsearch([f"http://{elastic_ip}:9200"], http_auth=(elastic_user, elastic_password))
    else:
        dest_es = Elasticsearch([f"http://{elastic_ip}:9200"])

    save_ilm_policies_to_new_cluster(dest_es, ilm_policies)

if __name__ == "__main__":
    main()

"""
With Authentication
ELASTIC_IP="your_elastic_ip" ELASTIC_USER="your_user" ELASTIC_PASSWORD="your_password" python3 import_ilm_policies.py

Without Authentication
ELASTIC_IP="your_elastic_ip" python3 import_ilm_policies.py
"""
