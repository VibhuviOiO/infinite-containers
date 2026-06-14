from litellm import completion

response = completion(
    model="gemini/gemini-2.5-flash",
    messages=[{"role": "user", "content": "hello"}]
)

print(response)
