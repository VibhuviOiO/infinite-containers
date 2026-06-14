# Free Models Gateway

This use case proves one LiteLLM gateway can route across multiple hosted free/free-tier providers.

Use this after [../free-models-samples/README.md](../free-models-samples/README.md) works. The sample scripts prove each provider key and model directly. This folder proves the gateway layer: aliases, routing, and fallback.

It runs:

- LiteLLM proxy on `http://localhost:4004`
- LiteLLM admin UI on `http://localhost:4004/ui/` (built into the proxy, backed by Postgres for persistence)
- Open WebUI chat on `http://localhost:3004` (opt-in `ui` profile)
- Postgres for the LiteLLM admin UI (virtual keys, model store, request logs)
- No Redis
- Hosted free/free-tier providers behind one OpenAI-compatible API

Models:

- `free-chat` -> Gemini `gemini-2.5-flash` primary route
- `free-chat-groq` -> Groq `llama-3.3-70b-versatile`
- `free-chat-openrouter` -> OpenRouter `openai/gpt-oss-20b:free`
- `free-chat-cloudflare` -> Cloudflare Workers AI `@cf/meta/llama-3.3-70b-instruct-fp8-fast`
- `free-chat-huggingface` -> Hugging Face `Qwen/Qwen2.5-7B-Instruct`
- `free-dummy-chat` -> intentionally broken, used to test fallback

## Prepare Keys

Validate provider keys first with the smoke tests in [../free-models-samples/README.md](../free-models-samples/README.md), then:

```bash
cp env.example .env
```

Fill `.env` with the working keys. Do not commit real keys.

## Start

From this folder:

```bash
docker compose --env-file .env up -d
```

From the repo root:

```bash
cp free-models-gateway/env.example free-models-gateway/.env

docker compose --env-file free-models-gateway/.env -f free-models-gateway/docker-compose.yml up -d
```

## Test Config Loading

From this folder:

```bash
set -a
source .env
set +a

curl "http://localhost:${LITELLM_PORT:-4004}/v1/models" \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY"
```

You should see `free-chat`, provider-specific fallback aliases, and `free-dummy-chat`.

Important: `/v1/models` only proves LiteLLM loaded the config. It does not prove provider keys, free quota, or model availability.

## Test Primary Chat

```bash
curl "http://localhost:${LITELLM_PORT:-4004}/v1/chat/completions" \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "free-chat",
    "messages": [
      {"role": "user", "content": "Reply with one short sentence: free hosted gateway works."}
    ]
  }'
```

Expected path:

```text
curl -> LiteLLM -> Gemini
```

If Gemini rate limits or fails, LiteLLM can fall back to Groq, OpenRouter, Cloudflare, or Hugging Face.

## Test Each Provider Alias

Run one alias at a time when debugging provider-specific issues:

```bash
for model in free-chat free-chat-groq free-chat-openrouter free-chat-cloudflare free-chat-huggingface; do
  echo "Testing $model"
  curl "http://localhost:${LITELLM_PORT:-4004}/v1/chat/completions" \
    -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"model\": \"$model\", \"messages\": [{\"role\": \"user\", \"content\": \"Say provider route works in one short sentence.\"}]}"
  echo
  echo
done
```

## Intentional Provider Targeting

Each alias maps to exactly one provider. Calling the alias bypasses the routing pool and pins the request to that provider. Use this when you want a specific provider to answer (debugging, cost, license, latency, region).

| Intent | Call this alias | Hits |
| --- | --- | --- |
| Default smart route with fallback | `free-chat` | Gemini, then Groq / OpenRouter / Cloudflare / Hugging Face |
| Force Gemini only | `free-chat` with `fallbacks: []` (see below) | Gemini only |
| Force Groq | `free-chat-groq` | Groq |
| Force OpenRouter | `free-chat-openrouter` | OpenRouter |
| Force Cloudflare | `free-chat-cloudflare` | Cloudflare Workers AI |
| Force Hugging Face | `free-chat-huggingface` | Hugging Face Inference |
| Prove fallback chain | `free-dummy-chat` | Fails first, then cascades |

Example pinning Cloudflare only:

```bash
curl "http://localhost:${LITELLM_PORT:-4004}/v1/chat/completions" \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "free-chat-cloudflare",
    "messages": [{"role": "user", "content": "Reply in one sentence: pinned to Cloudflare."}]
  }'
```

## Graceful Fallback Walkthroughs

### 1. Guaranteed first failure, automatic cascade

`free-dummy-chat` points at a model name Gemini will reject. The router catches the error and walks its fallback list until one provider answers.

```bash
curl "http://localhost:${LITELLM_PORT:-4004}/v1/chat/completions" \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "free-dummy-chat",
    "messages": [{"role": "user", "content": "Say fallback worked in one sentence."}]
  }'
```

Expected flow:

```text
free-dummy-chat -> fail
  -> free-chat (Gemini)
    -> free-chat-groq
      -> free-chat-openrouter
        -> free-chat-cloudflare
          -> free-chat-huggingface
```

The first one that succeeds returns. The `model` field in the response shows which provider model actually answered.

### 2. Force the primary to fail without breaking the config

LiteLLM exposes a request-time flag that simulates a primary failure so you can prove the fallback path live:

```bash
curl "http://localhost:${LITELLM_PORT:-4004}/v1/chat/completions" \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "free-chat",
    "mock_testing_fallbacks": true,
    "messages": [{"role": "user", "content": "Say second provider answered in one sentence."}]
  }'
```

The router forces `free-chat` to fail and falls through to the next provider in `fallbacks`.

### 3. Per-request fallback override

Override the configured fallback list for one call. Useful for cost-only or licence-only fallback chains.

```bash
curl "http://localhost:${LITELLM_PORT:-4004}/v1/chat/completions" \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "free-chat",
    "fallbacks": ["free-chat-groq"],
    "mock_testing_fallbacks": true,
    "messages": [{"role": "user", "content": "Say Groq answered in one sentence."}]
  }'
```

To pin one provider with no fallback at all, send `"fallbacks": []`.

### 4. Inspect which provider actually answered

LiteLLM returns the resolved model in the response body and in response headers.

```bash
curl -i "http://localhost:${LITELLM_PORT:-4004}/v1/chat/completions" \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "free-dummy-chat",
    "messages": [{"role": "user", "content": "ping"}]
  }' | sed -n '1,40p'
```

Look at:

- `x-litellm-model-id` header: the alias and provider model that served
- `x-litellm-attempted-fallbacks` / `x-litellm-attempted-retries` headers when present
- `model` field in JSON body: the underlying provider model id
- Container logs: `docker compose logs -f litellm`

### 5. Streaming still falls back

Streaming requests honour the same fallback chain. If the primary fails before sending the first chunk, the router switches providers transparently. Use `mock_testing_fallbacks` to force this reliably (some upstream streaming errors return raw to the client and skip the fallback):

```bash
curl -N "http://localhost:${LITELLM_PORT:-4004}/v1/chat/completions" \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "free-chat",
    "stream": true,
    "mock_testing_fallbacks": true,
    "messages": [{"role": "user", "content": "stream one short sentence about fallback"}]
  }'
```

You should see standard `data: {...}` SSE chunks ending in `data: [DONE]`, served by a fallback provider.

### 6. What this does NOT do

- Mid-stream provider switch after chunks have started flowing. Once a provider has sent its first token, the request stays on that provider.
- Hard SLO guarantees. Free tiers throttle and rate-limit. The fallback chain hides single-provider hiccups, not a global outage of all five.
- Cost or quality routing. This setup is a fan-out for availability, not a quality scorer.

## UI

Two browser surfaces ship with this use case. They are different things and answer different questions.

```text
http://localhost:4004/ui/     LiteLLM admin UI    "is the gateway healthy?"
http://localhost:3004         Open WebUI chat     "can a human actually chat through it?"
```

### A. LiteLLM Admin UI (always on)

The LiteLLM proxy serves its own admin UI at:

```text
http://localhost:${LITELLM_PORT:-4004}/ui/
```

Important: the URL is `/ui/`, not `/`. Hitting `http://localhost:4004/` shows the Swagger / OpenAPI docs (the API spec viewer). The admin UI is the React app at `/ui/`. The trailing slash matters — `/ui` returns a 307 redirect to `/ui/`.

Log in with the master key from `.env` (use it as both username and password). With Postgres wired in, you get:

- Persistent model list view (same six aliases as `/v1/models`, plus any added through the UI).
- Test Key playground for quick chat calls against any alias.
- Virtual keys: create scoped keys with budgets and rate limits.
- Teams, users, budgets, spend tracking.
- Request logs that survive container restarts.
- SSO config (when you wire it).

The Postgres dependency is intentional. Without it, the API still works but most of the admin UI tabs render empty because they query a database that does not exist.

### B. Open WebUI chat (opt-in `ui` profile)

A full ChatGPT-style UI is wired into compose under the `ui` profile, so the default `docker compose up -d` stays lean. Bring it up only when you want to chat with the gateway from a browser.

Start:

```bash
docker compose --env-file .env --profile ui up -d
```

Open:

```text
http://localhost:${OPEN_WEBUI_PORT:-3004}
```

What you should see:

- A model picker that auto-lists every alias from `/v1/models`: `free-chat`, `free-chat-groq`, `free-chat-openrouter`, `free-chat-cloudflare`, `free-chat-huggingface`, `free-dummy-chat`.
- Pick `free-chat` for smart routing with fallback.
- Pick `free-chat-<provider>` to pin one provider for an A/B feel across Gemini, Groq, OpenRouter, Cloudflare, and Hugging Face.
- Pick `free-dummy-chat` to watch the gateway recover live: the first hop fails inside the gateway, and a real provider answers in the chat window without any visible error.

Stop just the UI:

```bash
docker compose --env-file .env --profile ui stop open-webui
```

Stop everything:

```bash
docker compose --env-file .env --profile ui down
```

Notes:

- The UI container talks to LiteLLM over the internal compose network at `http://litellm:4000/v1`. Your host only exposes the UI port `3004`. The gateway port `4004` and the UI port `3004` are separate.
- `WEBUI_AUTH=False` keeps the UI open on localhost for fast local testing. Turn it on (set `WEBUI_AUTH=True` and remove that env line) before exposing the port off your machine.
- All chat history lives in the `open-webui-data` named volume. `docker volume rm lite-llm-free-models_open-webui-data` resets the UI.
- Compose may report the UI as `unhealthy` while the page works. The image ships a healthcheck that assumes auth is on; with `WEBUI_AUTH=False` the probe can fail even though the UI is serving HTTP 200.

## Logs

```bash
docker compose --env-file .env logs -f litellm
```

## Stop

```bash
docker compose --env-file .env down
```

## When To Use This

Use this use case to prove hosted provider fallback before adding production concerns like UI, virtual keys, budgets, cache, or observability.

Keep [../free-models-samples/README.md](../free-models-samples/README.md) for direct provider smoke tests. Use this folder for gateway behavior.
