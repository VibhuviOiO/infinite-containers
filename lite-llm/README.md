# LiteLLM Proxy

This repo contains small LiteLLM gateway use cases. Each use case is isolated in its own folder with a Docker Compose file, env example, LiteLLM config, and README.

## Use Cases

- [ollama/README.md](ollama/README.md): local free-model success path using Ollama, plus Postgres for the LiteLLM UI.
- [free-models-gateway/README.md](free-models-gateway/README.md): hosted free/free-tier provider gateway with fallback across Gemini, Groq, OpenRouter, Cloudflare, and Hugging Face.
- [dev-bedrock/README.md](dev-bedrock/README.md): LiteLLM with AWS Bedrock, no Postgres or Redis.
- [prod-bedrock/README.md](prod-bedrock/README.md): LiteLLM with AWS Bedrock plus Postgres and Redis.

Defaults are intentionally lightweight for testing: Ollama uses `qwen2.5:0.5b` and `smollm2:135m`, free hosted providers use their free/free-tier chat models, and Bedrock chat uses `amazon.nova-micro-v1:0`.

## Recommended Flow

Start with [ollama/README.md](ollama/README.md) to prove LiteLLM routing, UI, local models, and fallback without cloud credentials.

Then use [free-models-gateway/README.md](free-models-gateway/README.md) to test hosted free/free-tier provider fallback through one gateway.

Use [dev-bedrock/README.md](dev-bedrock/README.md) to test AWS Bedrock access with the smallest useful setup.

Use [prod-bedrock/README.md](prod-bedrock/README.md) after dev Bedrock works and you want Postgres plus Redis in the stack.

## Folder Purpose

- `ollama/`: learn the gateway pattern locally, test fallback safely, and use the LiteLLM UI without cloud provider setup.
- `free-models-gateway/`: route one app alias across hosted free/free-tier providers and prove provider fallback.
- `dev-bedrock/`: validate AWS credentials, region, Bedrock model access, and LiteLLM-to-Bedrock routing.
- `prod-bedrock/`: add the production-shaped dependencies: Postgres for UI/admin state and Redis for cache.

## Notes

- The LiteLLM API can run without Postgres, but the LiteLLM UI/admin features need a database.
- `/v1/models` proves LiteLLM loaded config; it does not prove provider permissions or model access.
- Fallback is easiest to understand in the Ollama use case because `local-dummy-chat` intentionally fails and routes to a real local model.
- Keep provider routing, env, cache, database, and cloud resources in files/IaC so the setup is repeatable.

