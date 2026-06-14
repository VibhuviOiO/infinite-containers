from litellm import completion
import os

response = completion(
    model="cloudflare/@cf/meta/llama-3.3-70b-instruct-fp8-fast",
    api_key=os.environ["CLOUDFLARE_API_TOKEN"],
    messages=[
        {
            "role": "user",
            "content": "Write a Python hello world"
        }
    ]
)

print(response["choices"][0]["message"]["content"])