# Dev Bedrock Gateway

This use case is the smallest verifiable LiteLLM + AWS Bedrock setup. The goal is to prove Bedrock IAM, region, and model access work before adding any state, cache, or admin UI on top.

It runs:

- LiteLLM proxy on `http://localhost:4002`
- No Postgres (so no LiteLLM admin UI here — see [../prod-bedrock/README.md](../prod-bedrock/README.md))
- No Redis (so no LiteLLM cache here)
- Local AWS credentials mounted from `~/.aws` (read-only)

Bedrock models:

- `gpt-4o-mini` -> `bedrock/amazon.nova-micro-v1:0` (chat)
- `text-embedding-3-large` -> `bedrock/amazon.titan-embed-text-v2:0` (embeddings)

The alias names match common OpenAI client defaults on purpose, so existing OpenAI-coded apps can point at this gateway with only a `base_url` change.

## Why A Separate Dev Profile

Most Bedrock setup pain has nothing to do with LiteLLM. It is AWS-side:

- IAM identity has no `bedrock:InvokeModel` permission.
- Model access has not been requested or approved in the AWS console.
- The region you are calling does not host the model you picked.
- Credentials are missing, expired, or scoped to a different account.

Adding Postgres, Redis, fallbacks, and a UI on top of that makes the failure surface five times wider. So this dev profile strips everything except the gateway and AWS, exposes Bedrock directly, and gives you four short curls that isolate exactly which layer broke.

When this profile works end to end, you graduate to [../prod-bedrock/README.md](../prod-bedrock/README.md) for the production-shape stack.

## Dev vs Prod — What Actually Differs

The Bedrock side is identical between the two profiles. Same model entries, same `aws_region_name`, same `~/.aws` mount, same auth flow. Everything that differs is platform infrastructure around the gateway.

| Concern                | dev-bedrock                                          | prod-bedrock                                              |
| ---------------------- | ---------------------------------------------------- | --------------------------------------------------------- |
| Port                   | `4002`                                               | `4003`                                                    |
| Services               | `litellm` only                                       | `litellm` + `postgres` + `redis` (both with healthchecks) |
| Admin UI (`/ui/`)      | Not available (needs Postgres)                       | Available at `http://localhost:4003/ui/`                  |
| Virtual keys / budgets | Not available (needs Postgres)                       | Available via the UI                                      |
| Response cache         | Off                                                  | On, Redis-backed                                          |
| `num_retries`          | `1`                                                  | `2`                                                       |
| `fallbacks`            | None                                                 | Declared in `router_settings`                             |
| `set_verbose`          | `true` (loud logs to debug AWS)                      | `false` (quieter logs)                                    |
| `DATABASE_URL`         | Not set                                              | `postgresql://...@postgres:5432/...`                      |
| `REDIS_HOST` / `_PORT` | Not set                                              | `redis` / `6379`                                          |
| Volumes                | None                                                 | `postgres_data`, `redis_data`                             |
| Bedrock model list     | Same as prod                                         | Same as dev                                               |
| AWS auth               | `~/.aws:/root/.aws:ro` mount, `AWS_PROFILE=default`  | Same                                                      |

If a Bedrock call fails in **prod** but works in **dev**, the bug is in the surrounding infrastructure (Postgres connectivity, cache config, fallback definition), not in Bedrock. If it fails in **dev**, the bug is AWS-side.

## Prepare AWS Access

Check credentials on your host first:

```bash
aws sts get-caller-identity --profile default
aws bedrock list-foundation-models --region us-east-1 --profile default
```

Your AWS identity needs:

- `bedrock:InvokeModel` on the model ARNs you use (Nova Micro and Titan Embed v2 here).
- Model access requested and approved for those models in the AWS console (Bedrock → Model access).
- A region in `AWS_REGION_NAME` that actually hosts those models.

## Start

From this folder:

```bash
cp env.example .env

docker compose --env-file .env up -d
```

From the repo root:

```bash
cp dev-bedrock/env.example dev-bedrock/.env

docker compose --env-file dev-bedrock/.env -f dev-bedrock/docker-compose.yml up -d
```

## Test Config Loading

This first call only proves LiteLLM parsed `litellm_config.yaml`. It does **not** prove AWS works.

```bash
set -a
source .env
set +a

curl "http://localhost:${LITELLM_PORT:-4002}/v1/models" \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY"
```

Expected: a JSON list containing `gpt-4o-mini` and `text-embedding-3-large`.

## Test Bedrock Chat

```bash
curl "http://localhost:${LITELLM_PORT:-4002}/v1/chat/completions" \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o-mini",
    "messages": [
      {"role": "user", "content": "Reply with one short sentence: Bedrock works."}
    ]
  }'
```

A successful response proves three things at once: AWS credentials are mounted, IAM allows `bedrock:InvokeModel`, and the region hosts `amazon.nova-micro-v1:0`.

## Test Bedrock Embeddings

```bash
curl "http://localhost:${LITELLM_PORT:-4002}/v1/embeddings" \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "text-embedding-3-large",
    "input": "LiteLLM dev Bedrock embedding test"
  }'
```

Embedding access is a separate model-access toggle in the Bedrock console, so this can fail even when chat already works.

## Test Provider Health

```bash
curl "http://localhost:${LITELLM_PORT:-4002}/health" \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY"
```

`/health` performs a minimal upstream probe per model. Use it as a single-shot sanity check.

## Bedrock Failure Modes — Check These Before Blaming The Gateway

When `/v1/models` returns `200` but chat or embeddings fail, the bug is almost always one of these. Walk them in order:

1. **Credentials not mounted.** Inside the container, run `docker exec -it lite-llm-dev-bedrock ls /root/.aws`. If empty, your host `~/.aws` is missing or the volume mount failed.
2. **Wrong profile.** The container uses `AWS_PROFILE` from `.env` (`default` by default). If your host uses a non-default profile, set it in `.env`.
3. **Expired SSO / STS credentials.** If you use AWS SSO, run `aws sso login --profile default` on the host, then restart the container.
4. **Missing IAM permission.** Attach a policy granting `bedrock:InvokeModel` (and `bedrock:InvokeModelWithResponseStream` if you plan to stream) on the specific model ARNs.
5. **Model access not granted.** AWS console → Bedrock → Model access → request and wait for approval for Nova Micro and Titan Embed v2.
6. **Wrong region.** Not every Bedrock model is in every region. Confirm with `aws bedrock list-foundation-models --region <region>`.
7. **Region mismatch between env vars.** LiteLLM reads `AWS_REGION_NAME`. The AWS SDK falls back to `AWS_REGION` or `AWS_DEFAULT_REGION`. Keep them aligned (this compose sets both).

If all seven check out and it still fails, then it is worth reading LiteLLM logs.

## Logs

```bash
docker compose --env-file .env logs -f litellm
```

`set_verbose: true` is on in `litellm_config.yaml` for this dev profile, so the logs are deliberately loud. The prod profile turns it off.

## Stop

```bash
docker compose --env-file .env down
```

There are no volumes in this profile, so nothing is left behind on disk.

## Next Step

When all four checks above pass, move to [../prod-bedrock/README.md](../prod-bedrock/README.md) to add Postgres, Redis, the admin UI, fallbacks, and the response cache on top of the same Bedrock model list.
