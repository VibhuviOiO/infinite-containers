import os
import requests

api_key = os.getenv("OPENROUTER_API_KEY")

response = requests.get(
    "https://openrouter.ai/api/v1/models",
    headers={
        "Authorization": f"Bearer {api_key}"
    }
)

data = response.json()["data"]

free_models = sorted([
    model["id"]
    for model in data
    if ":free" in model["id"]
])

print("\n=== FREE MODELS ===\n")

for model in free_models:
    print(model)

print(f"\nTotal free models: {len(free_models)}")