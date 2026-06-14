import time
from litellm import completion
from litellm.exceptions import RateLimitError

MODELS = [
    "openrouter/openai/gpt-oss-20b:free",
    "openrouter/qwen/qwen3-coder:free",
    "openrouter/meta-llama/llama-3.2-3b-instruct:free",
    "openrouter/google/gemma-4-26b-a4b-it:free",
]

for model in MODELS:
    try:
        print(f"\nTrying: {model}")

        response = completion(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": "Write a Python hello world"
                }
            ]
        )

        print("\nSUCCESS")
        print(response["choices"][0]["message"]["content"])
        break

    except RateLimitError as e:
        print(f"Rate limited on {model}")

        retry_after = 15
        try:
            retry_after = int(
                e.response.json()["error"]["metadata"]
                .get("retry_after_seconds", 15)
            )
        except Exception:
            pass

        print(f"Retrying after {retry_after}s")
        time.sleep(retry_after)

    except Exception as e:
        print(f"Failed: {e}")