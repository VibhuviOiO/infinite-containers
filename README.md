# infinite-docker-compose

Various Docker Compose configurations, infrastructure labs, POCs, and production-like setups I use for development and experimentation.

The repository contains both standalone infrastructure components and complete use-cases showing how different systems can be integrated and operated.

---

#### AI | ML

* [Ollama and Ollama WebUI](https://github.com/JinnaBalu/infinite-docker-compose/blob/main/ollama/docker-compose.yml) - Run LLMs locally
* [Flowise](https://github.com/JinnaBalu/infinite-docker-compose/blob/main/flowise/docker-compose.yml) - Visual UI for LLM orchestration
* [Marqo](https://github.com/JinnaBalu/infinite-docker-compose/blob/main/marqo/docker-compose.yml) - Vector database and vector search engine
* [Qdrant](https://github.com/JinnaBalu/infinite-docker-compose/blob/main/qdrant/docker-compose.yml) - Vector database and vector search engine
* [ChromaDB](https://github.com/JinnaBalu/infinite-docker-compose/blob/main/chromadb/docker-compose.yml) - Vector embeddings database

#### LLM Engineering Platform

* [LiteLLM](https://github.com/JinnaBalu/infinite-docker-compose/tree/main/lite-llm) - LLM gateway with multiple deployment and provider scenarios
* [Langfuse Developer Quickstart](https://github.com/JinnaBalu/infinite-docker-compose/tree/main/langfuse)
* [AI Gateway - LiteLLM](https://github.com/JinnaBalu/infinite-docker-compose/tree/main/lite-llm)

##### LiteLLM Use Cases

The LiteLLM implementation includes multiple practical scenarios:

* **Free Models Gateway** - Gateway for accessing free/low-cost model providers through a unified OpenAI-compatible API
* **Free Model Samples** - Direct examples for Cloudflare, Gemini, Groq, Hugging Face, OpenRouter, and other providers
* **Ollama** - Local model gateway using LiteLLM and Ollama
* **AWS Bedrock Development** - LiteLLM gateway for development workloads using Amazon Bedrock
* **AWS Bedrock Production** - Production-oriented Bedrock gateway configuration

See the [LiteLLM documentation](https://github.com/JinnaBalu/infinite-docker-compose/tree/main/lite-llm) for configuration, environment variables, provider setup, and examples.

---

#### IAM

* [OpenLDAP](https://github.com/JinnaBalu/infinite-docker-compose/tree/main/openldap) - LDAP directory service with users, groups, schemas, initialization, and verification
* [Keycloak + OpenLDAP](https://github.com/JinnaBalu/infinite-docker-compose/tree/main/openldap/use-cases/keycloak) - Keycloak LDAP federation with OpenLDAP

---

#### LB | Reverse Proxy | Application Server

* [Caddy](https://github.com/JinnaBalu/infinite-docker-compose/blob/main/caddy/docker-compose.yml)

---

#### SMTP | MailServer

---

#### REST

* [PostgREST POC](https://github.com/ContainerTalks/infinite-docker-compose/tree/main/postrest)

---

#### Image

* [darthsim/imgproxy](https://github.com/JinnaBalu/infinite-docker-compose/blob/main/image-proxy/docker-compose.yml) | [Info](https://docs.imgproxy.net/getting_started)

---

#### Monitoring

* logflare
* tancloud/hertzbeat

---

#### ETL

* [Vector](https://github.com/JinnaBalu/infinite-docker-compose/blob/main/vector/docker-compose.yml) - Ship logs from a wide range of sources

---

#### Object Store

* [MinIO](https://github.com/JinnaBalu/infinite-docker-compose/blob/main/minio/docker-compose.yml) - S3-compatible object storage

---

#### Mock

* [stripe-mock](https://github.com/JinnaBalu/infinite-docker-compose/blob/main/stripe-mock/docker-compose.yml)

---

#### Note Taking

* [Memos](https://github.com/JinnaBalu/infinite-docker-compose/blob/main/memos/docker-compose.yml)

---

#### Swagger

* [Swagger UI](https://github.com/JinnaBalu/infinite-docker-compose/blob/main/swagger-ui/docker-compose.yml)

---

## Implementation Labs

Some components contain complete implementation labs rather than a single Compose file.

These labs document real infrastructure patterns, integrations, configurations, and verification steps.

### LiteLLM

```text
lite-llm/
├── dev-bedrock/
├── free-models-gateway/
├── free-models-samples/
├── ollama/
└── prod-bedrock/
```

The LiteLLM lab demonstrates:

```text
Multiple LLM Providers
        │
        ▼
     LiteLLM
        │
 ┌──────┼──────────┬───────────┐
 ▼      ▼          ▼           ▼
Ollama  Bedrock   Free Models  OpenRouter
```

Scenarios include:

* Local LLM gateway with Ollama
* Free model gateway
* Provider-specific API examples
* AWS Bedrock development environment
* AWS Bedrock production environment
* Unified OpenAI-compatible access to multiple providers

### OpenLDAP

The OpenLDAP implementation contains:

* Single-node LDAP deployment
* Persistent LDAP data
* User and group initialization
* LDAP schemas
* Monitoring
* Verification commands

### Keycloak + OpenLDAP

The Keycloak use-case demonstrates:

```text
                 Keycloak
                    │
            LDAP Federation
                    │
                    ▼
                OpenLDAP
                    │
             Users / Groups
```

The implementation includes:

* Keycloak realm configuration
* LDAP federation
* LDAP user synchronization
* User attribute mapping
* Group-based identity structure
* Reproducible Docker Compose setup
* Verification through Keycloak synchronization logs
