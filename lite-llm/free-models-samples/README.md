# Free Model Samples

This folder contains direct LiteLLM Python smoke tests for free or free-tier model providers.

Use these samples before creating a full LiteLLM gateway use case. The idea is simple:

1. Prove the provider key and model work directly from Python.
2. Move the working model id into a LiteLLM `litellm_config.yaml`.
3. Expose it through the proxy with a clean local alias like `free-chat`.
4. Add fallback, budgets, cache, UI, or observability only after the basic provider route works.

## What These Samples Prove

These scripts do not start the LiteLLM proxy. They call providers through the LiteLLM Python SDK.

That is useful because it isolates provider issues first:

- API key is missing or invalid.
- Free quota is exhausted.
- Model id changed or is unavailable.
- Provider has rate limits.
- Your network or account cannot reach the provider.

After a sample works here, the same model can be added to a use-case folder with Docker Compose and `litellm_config.yaml`.

## Install

From this folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install litellm requests
```

## Environment Variables

Set only the keys for the provider you want to test.

```bash
export GEMINI_API_KEY="..."
export GROQ_API_KEY="..."
export OPENROUTER_API_KEY="..."
export HUGGINGFACE_API_KEY="..."
export CLOUDFLARE_API_TOKEN="..."
export CLOUDFLARE_ACCOUNT_ID="..."
```

Notes:

- Gemini uses `GEMINI_API_KEY`.
- Groq uses `GROQ_API_KEY`.
- OpenRouter uses `OPENROUTER_API_KEY`.
- Hugging Face uses `HUGGINGFACE_API_KEY`.
- Cloudflare Workers AI needs both token and account id for LiteLLM provider routing.

## Test Each Sample

Run one provider at a time.

### Gemini

```bash
python3 gemini.py
```

Current model:

```text
gemini/gemini-2.5-flash
```

Use this first if you want the easiest free-tier smoke test.

### Groq

```bash
python3 groq.py
```

Current model:

```text
groq/llama-3.3-70b-versatile
```

Use this when you want a fast hosted open-model test.

### OpenRouter

List available free models:

```bash
python3 open_router_models.py
```

Try free models with fallback inside the script:

```bash
python3 open_route.py
```

Current tested models:

```text
openrouter/openai/gpt-oss-20b:free
openrouter/qwen/qwen3-coder:free
openrouter/meta-llama/llama-3.2-3b-instruct:free
openrouter/google/gemma-4-26b-a4b-it:free
```

OpenRouter free models change often. Always run `open_router_models.py` before locking a model into a LiteLLM config.

### Hugging Face

```bash
python3 huggingface.py
```

Current tested models:

```text
huggingface/Qwen/Qwen2.5-7B-Instruct
huggingface/microsoft/Phi-3-mini-4k-instruct
huggingface/google/gemma-2-2b-it
```

Hugging Face free inference can be slower and less predictable than Gemini, Groq, or OpenRouter. Treat this as a fallback exploration provider, not the first recommended path.

### Cloudflare Workers AI

```bash
python3 cloudflare.py
```

Current model:

```text
cloudflare/@cf/meta/llama-3.3-70b-instruct-fp8-fast
```

Use this if you already have Cloudflare Workers AI enabled and want to test their hosted model route.

## How To Turn A Working Sample Into A LiteLLM Use Case

Create a dedicated use-case folder when a provider sample works and you want repeatable gateway testing.

Recommended folder pattern:

```text
free-models-gateway/
  docker-compose.yml
  env.example
  litellm_config.yaml
  README.md
```

The use-case folder should own:

- Docker Compose runtime
- `.env` shape
- LiteLLM model aliases
- fallback routing
- UI/database/cache only if that use case needs them

Keep `free-models-samples/` as direct provider smoke tests. Do not make every sample script its own production setup.

## LiteLLM Config Examples Per Provider

Use stable aliases in your app. Keep provider-specific model ids inside `litellm_config.yaml`.

### Gemini Config

```yaml
model_list:
  - model_name: free-gemini-chat
    litellm_params:
      model: gemini/gemini-2.5-flash
      api_key: os.environ/GEMINI_API_KEY
```

### Groq Config

```yaml
model_list:
  - model_name: free-groq-chat
    litellm_params:
      model: groq/llama-3.3-70b-versatile
      api_key: os.environ/GROQ_API_KEY
```

### OpenRouter Config

```yaml
model_list:
  - model_name: free-openrouter-chat
    litellm_params:
      model: openrouter/openai/gpt-oss-20b:free
      api_key: os.environ/OPENROUTER_API_KEY
```

### Hugging Face Config

```yaml
model_list:
  - model_name: free-huggingface-chat
    litellm_params:
      model: huggingface/Qwen/Qwen2.5-7B-Instruct
      api_key: os.environ/HUGGINGFACE_API_KEY
```

### Cloudflare Config

```yaml
model_list:
  - model_name: free-cloudflare-chat
    litellm_params:
      model: cloudflare/@cf/meta/llama-3.3-70b-instruct-fp8-fast
      api_key: os.environ/CLOUDFLARE_API_TOKEN
      account_id: os.environ/CLOUDFLARE_ACCOUNT_ID
```

## One Gateway With Provider Fallback

After each direct sample works, combine the stable providers into one gateway config:

```yaml
model_list:
  - model_name: free-chat
    litellm_params:
      model: gemini/gemini-2.5-flash
      api_key: os.environ/GEMINI_API_KEY

  - model_name: free-chat-groq
    litellm_params:
      model: groq/llama-3.3-70b-versatile
      api_key: os.environ/GROQ_API_KEY

  - model_name: free-chat-openrouter
    litellm_params:
      model: openrouter/openai/gpt-oss-20b:free
      api_key: os.environ/OPENROUTER_API_KEY

router_settings:
  num_retries: 1
  fallbacks:
    - free-chat: [free-chat-groq, free-chat-openrouter]
```

Application code should call only:

```text
free-chat
```

The gateway decides whether the request goes to Gemini, Groq, or OpenRouter.

## Suggested Testing Order

1. Run `gemini.py`.
2. Run `groq.py`.
3. Run `open_router_models.py`, then `open_route.py`.
4. Run `cloudflare.py` if you have Workers AI enabled.
5. Run `huggingface.py` last because free inference can be slower and less reliable.
6. Move the working model ids into a LiteLLM use-case folder.
7. Test `/v1/models` through the proxy.
8. Test `/v1/chat/completions` through the proxy.
9. Add fallback only after each individual provider route works.

## When To Create A New Use Case Folder

Create a new use case when you want to prove a gateway behavior, not just a provider call.

Good use-case candidates:

- `free-models-gateway/`: one LiteLLM proxy that routes across Gemini, Groq, OpenRouter, Hugging Face, and Cloudflare.
- `cost-governance/`: virtual keys, budgets, and per-key limits.
- `semantic-cache/`: Redis-backed cache to reduce repeated model calls.
- `guardrails/`: PII redaction and prompt filtering before provider calls.
- `observability/`: per-key usage, latency, and model routing visibility.

## Troubleshooting

- `/v1/models` only proves LiteLLM loaded config. It does not prove the provider key or free quota works.
- A direct Python sample failing usually means provider setup is wrong, not Docker or proxy config.
- OpenRouter free models can disappear or become rate-limited. Refresh the list before debugging.
- Hugging Face hosted inference may be cold, slow, or unavailable for some models.
- Cloudflare requires the right account id and Workers AI access in addition to the API token.
