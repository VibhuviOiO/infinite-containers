from litellm import completion

response = completion(
    model="groq/llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": "Explain Kubernetes simply"}]
)

print(response)