# Ollama Local Gateway

This use case proves the LiteLLM gateway locally before using any managed model provider.

It runs:

- LiteLLM proxy and UI on `http://localhost:4001`
- Ollama with two tiny local models
- Postgres for the LiteLLM UI/admin pages
- Two one-shot model pull jobs

Models:

- `local-free-chat` -> `qwen2.5:0.5b`
- `local-tiny-chat` -> `smollm2:135m`
- `local-dummy-chat` -> intentionally broken, used to test fallback
- `gpt-4o-mini` -> local alias backed by `qwen2.5:0.5b`

## Start

From this folder:

```bash
cp env.example .env

docker compose --env-file .env down --remove-orphans

docker compose --env-file .env up -d
```

From the repo root:

```bash
cp ollama/env.example ollama/.env

docker compose --env-file ollama/.env -f ollama/docker-compose.yml down --remove-orphans

docker compose --env-file ollama/.env -f ollama/docker-compose.yml up -d
```

Do not add `-v` unless you want to delete downloaded Ollama models and Postgres UI data.

## Check Containers

```bash
docker ps -a
```

Expected:

- `lite-llm-ollama-proxy` is running.
- `lite-llm-ollama` is healthy.
- `lite-llm-ollama-postgres` is healthy.
- `lite-llm-ollama-pull-primary` exited with `0`.
- `lite-llm-ollama-pull-secondary` exited with `0`.

## Test Models

```bash
set -a
source .env
set +a

curl "http://localhost:${LITELLM_PORT:-4001}/v1/models" \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY"
```

You should see `local-free-chat`, `local-tiny-chat`, `local-dummy-chat`, and `gpt-4o-mini`.

## Test Chat

```bash
curl "http://localhost:${LITELLM_PORT:-4001}/v1/chat/completions" \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "local-free-chat",
    "messages": [
      {"role": "user", "content": "Reply with one short sentence: LiteLLM local works."}
    ]
  }'
```

## Test Fallback

```bash
curl "http://localhost:${LITELLM_PORT:-4001}/v1/chat/completions" \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "local-dummy-chat",
    "messages": [
      {"role": "user", "content": "Say fallback worked in one short sentence."}
    ]
  }'
```

Expected: `local-dummy-chat` fails internally, then LiteLLM falls back to `local-free-chat` or `local-tiny-chat`.

## Open UI

```text
http://localhost:4001/ui/
```

Use `LITELLM_MASTER_KEY` from `.env` as the UI password.

The API can run without Postgres, but the LiteLLM UI/admin features need a database. That is why this use case includes Postgres.

## Logs

```bash
docker compose --env-file .env logs -f litellm
```

## Stop

```bash
docker compose --env-file .env down
```
