from litellm import completion

models = [
    "huggingface/Qwen/Qwen2.5-7B-Instruct",
    "huggingface/microsoft/Phi-3-mini-4k-instruct",
    "huggingface/google/gemma-2-2b-it",
]

for model in models:
    try:
        print(f"\nTrying: {model}")

        response = completion(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": "Say hello"
                }
            ]
        )

        print("\nSUCCESS")
        print(response["choices"][0]["message"]["content"])
        break

    except Exception as e:
        print(f"FAILED: {e}")