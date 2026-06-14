# Prod Bedrock Gateway

This use case is the production-shape LiteLLM + AWS Bedrock deployment, runnable on your laptop today and structurally aligned with what you ship to a server tomorrow.

It runs:

- LiteLLM proxy + admin UI on `http://localhost:4003`
- Postgres 16 for LiteLLM admin state (users, virtual keys, budgets, model overrides)
- Redis 7 for the LiteLLM response cache
- LiteLLM container healthcheck against `/health/liveliness`
- `STORE_MODEL_IN_DB=True` so the UI can manage models without redeploying
- Local AWS credentials mounted from `~/.aws` (read-only)

Bedrock models (starting placeholders — replace once your team approves real ones):

- `gpt-4o-mini` → `bedrock/amazon.nova-micro-v1:0` (chat)
- `text-embedding-3-large` → `bedrock/amazon.titan-embed-text-v2:0` (embeddings)

The alias names match common OpenAI client defaults on purpose, so existing OpenAI-coded apps point at this gateway with only a `base_url` change.

## Is This Actually Production-Grade?

Honest answer: this stack is **production-grade in shape**, not **production-ready for the public internet on day one**. The difference matters.

What is production-grade in this profile:

- The three-service topology (gateway + Postgres + Redis) is the same shape that LiteLLM is designed to run in production.
- Postgres + Redis both have healthchecks, and LiteLLM `depends_on` them with `condition: service_healthy`, so the gateway never starts before its dependencies are reachable.
- LiteLLM itself has a healthcheck (`/health/liveliness`) with a `start_period` long enough for Prisma migrations on first boot.
- `STORE_MODEL_IN_DB=True` is set, so the admin UI can add/edit/delete models, virtual keys, and budgets without a config redeploy.
- Bedrock auth uses the same `~/.aws` flow that EC2/ECS/EKS will provide via instance/task IAM roles in real production — you swap the mount for an IAM role, nothing else changes.
- `cache: true` with Redis cuts duplicate Bedrock invocation cost and latency.
- `set_verbose: false` keeps logs at production volume.
- `restart: unless-stopped` on every service.

What is explicitly NOT here, and you will need before exposing this to the public internet:

| Gap                                | Why it matters                                                 | Where to add it                                        |
| ---------------------------------- | -------------------------------------------------------------- | ------------------------------------------------------ |
| TLS termination                    | Bearer tokens cannot ride over plain HTTP in public networks   | Reverse proxy (Nginx, Caddy, ALB, Cloudflare) in front |
| Secret management                  | `LITELLM_MASTER_KEY` in `.env` is a laptop pattern, not prod   | AWS Secrets Manager / SSM / Vault sourced at deploy    |
| Postgres backups                   | The `postgres_data` volume is your only copy                   | RDS snapshots, or `pg_dump` cron + offsite             |
| Resource limits                    | Compose has none; a runaway model call can OOM the host        | Add `deploy.resources.limits` (Compose v3.x / Swarm)   |
| Network policy                     | Postgres and Redis are reachable from any container on the net | Bind Postgres/Redis to an internal-only network        |
| Observability (logs/metrics/trace) | You will fly blind during the first incident                   | Ship LiteLLM logs to your aggregator; expose Prometheus|
| Rate limiting / per-key budgets    | Possible via the UI, but not enforced by default               | Configure budgets and TPM/RPM caps per virtual key      |
| Guardrails (PII, prompt injection) | Not wired in                                                   | LiteLLM guardrails section, or pre/post middleware     |

If your "production" means *internal-network deployment on an EC2 host behind your existing ALB and IAM role*, this stack is ready as soon as you replace the `~/.aws` mount with an instance role, source the master key from your secret manager, and put TLS in front. If your "production" means *internet-facing customer endpoints*, the table above is your remaining checklist.

## Is It Ready For You To Test Once Your Team Provides The Models?

Yes — that is exactly the flow this profile is built for. Three steps:

1. Replace the two model entries in [litellm_config.yaml](./litellm_config.yaml) with the Bedrock model IDs your team approves. Keep the alias names (`gpt-4o-mini`, `text-embedding-3-large`) if you want OpenAI-coded apps to keep working unchanged, or rename them to whatever your team prefers.
2. If your team approves a second chat model and a second embedding model, uncomment the `fallbacks:` block in `litellm_config.yaml` and point each alias at its real fallback partner. (The previous self-referencing fallbacks were no-ops and have been removed.)
3. Confirm your AWS identity has `bedrock:InvokeModel` on the new model ARNs, and that model access is approved in the Bedrock console for the chosen region.

Then run the test sequence below.

## Dev vs Prod — What Differs

The Bedrock side is identical between [../dev-bedrock](../dev-bedrock/README.md) and this profile. Same model entries by default, same `aws_region_name`, same `~/.aws` mount, same auth flow. Everything that differs is the platform around the gateway:

| Concern                | dev-bedrock                                          | prod-bedrock (this one)                                   |
| ---------------------- | ---------------------------------------------------- | --------------------------------------------------------- |
| Port                   | `4002`                                               | `4003`                                                    |
| Services               | `litellm` only                                       | `litellm` + `postgres` + `redis` (both with healthchecks) |
| Admin UI (`/ui/`)      | Not available (needs Postgres)                       | Available                                                 |
| Virtual keys / budgets | Not available (needs Postgres)                       | Available via the UI                                      |
| `STORE_MODEL_IN_DB`    | Not set                                              | `True` (models manageable from UI)                        |
| Response cache         | Off                                                  | On, Redis-backed                                          |
| `num_retries`          | `1`                                                  | `2`                                                       |
| `fallbacks`            | None                                                 | Commented example, wire in once a 2nd model is approved   |
| `set_verbose`          | `true`                                               | `false`                                                   |
| Volumes                | None                                                 | `postgres_data`, `redis_data`                             |

If a Bedrock call fails in **prod** but works in **dev**, the bug is platform-side (Postgres connectivity, Redis cache config, fallback definition), not AWS. If it fails in **dev**, the bug is AWS-side.

## Prepare AWS Access

```bash
aws sts get-caller-identity --profile default
aws bedrock list-foundation-models --region us-east-1 --profile default
```

Your AWS identity needs `bedrock:InvokeModel` (and `bedrock:InvokeModelWithResponseStream` if you stream) on every model in `litellm_config.yaml`, plus approved model access in the Bedrock console for the region you target.

## Start

From this folder:

```bash
cp env.example .env

docker compose --env-file .env up -d
```

From the repo root:

```bash
cp prod-bedrock/env.example prod-bedrock/.env

docker compose --env-file prod-bedrock/.env -f prod-bedrock/docker-compose.yml up -d
```

First boot waits ~30–60s while LiteLLM runs Prisma migrations against the fresh Postgres. The container healthcheck has a 90s `start_period` to absorb this.

## Test Sequence

```bash
set -a
source .env
set +a

# 1. Config parsed?
curl "http://localhost:${LITELLM_PORT:-4003}/v1/models" \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY"

# 2. Bedrock chat works?
curl "http://localhost:${LITELLM_PORT:-4003}/v1/chat/completions" \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-4o-mini","messages":[{"role":"user","content":"Reply with one short sentence: production Bedrock works."}]}'

# 3. Bedrock embeddings work?
curl "http://localhost:${LITELLM_PORT:-4003}/v1/embeddings" \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"text-embedding-3-large","input":"LiteLLM prod Bedrock embedding test"}'

# 4. Cache working? Repeat call 2 — observe lower latency on the second hit.

# 5. Provider health probe.
curl "http://localhost:${LITELLM_PORT:-4003}/health" \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY"
```

## Open The Admin UI

```text
http://localhost:4003/ui/
```

Use `LITELLM_MASTER_KEY` from `.env` as the UI password. Trailing slash matters — `/ui` returns `307 → /ui/`.

What the UI lets you do (because Postgres + `STORE_MODEL_IN_DB=True` are wired):

- Add/edit/delete models without redeploying the container.
- Create virtual keys for each downstream team or application.
- Set per-key monthly budgets and TPM/RPM rate limits.
- View per-key spend, request counts, and error rates.
- Rotate the master key without losing model state.

The first three are what make this a "production-grade" setup rather than just "a config file in a container".

## Promoting To A Real Server

When you move this from your laptop to a real environment, the changes are localized:

1. Swap `~/.aws:/root/.aws:ro` for an EC2 instance profile / ECS task role / EKS IRSA. The `boto3` chain finds the role automatically; no config change.
2. Source `LITELLM_MASTER_KEY` and `POSTGRES_PASSWORD` from your secret manager at deploy time, not from a checked-in `.env`.
3. Put Nginx/Caddy/ALB in front for TLS termination.
4. Move Postgres to RDS (or your managed Postgres) for backups, point-in-time recovery, and HA.
5. Move Redis to ElastiCache (or your managed Redis) for failover.
6. Ship LiteLLM logs to your aggregator and expose Prometheus metrics (LiteLLM has built-in exporters; enable them in `litellm_settings`).

The compose, config, and alias structure stay the same shape. That is the whole point of validating it locally first.

## Logs

```bash
docker compose --env-file .env logs -f litellm
docker compose --env-file .env logs postgres
docker compose --env-file .env logs redis
```

## Stop

```bash
docker compose --env-file .env down
```

Remove local Postgres and Redis data:

```bash
docker compose --env-file .env down -v
```

## When To Use This

Use this after [../dev-bedrock/README.md](../dev-bedrock/README.md) works. If dev Bedrock fails, fix AWS credentials, model access, region, or IAM before debugging this production-shaped stack. The whole point of the two-profile split is that when prod fails after dev passes, you already know the bug is platform-side, not AWS-side.
