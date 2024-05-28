---
title:  "Elasticsearch Single Node using Docker Compose"
description: Deploying the elasticsearch and Kibana as docker containers 
metadate: "hide"
categories: [ NoSQL, Search Engine, Elasticsearch ]
tags: [ Elasticsearch ]
image: "/assets/images/elasticsearch.svg"
---

## Preface

This post assumes that you have some basic understanding of Docker, Docker Compose, and the key components used in the docker ecosystem. Get up to speed, with the [Prepare Your Docker Eenvironment](https://docs.docker.com/get-started/#prepare-your-docker-environment) section of Docker docs.

1. Install [Docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
2. install [docker-compose](https://docs.docker.com/compose/install/)

## Deploy Elasticsearch Single node with docker-compose

![Elasticsarch Single Node on Docker](https://raw.githubusercontent.com/JinnaBalu/elasticsearch/master/images/elasticsearch.svg)

Elasticsearch Single Node Instance and Kibana Using Docker Compose. Create the `docker-compose.yml` with the following

```yaml
---
version: '3.6'
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.2.1
    container_name: elasticsearch
    environment:
      - cluster.name="es-data-cluster"
      - node.name=es-node
      - discovery.type=single-node
      - bootstrap.memory_lock=true
      - network.host=0.0.0.0
      - transport.host=0.0.0.0
      - discovery.zen.minimum_master_nodes=1
      - xpack.license.self_generated.type=trial
      - xpack.security.enabled=false
      - "ES_JAVA_OPTS=-Xms1024m -Xmx1024m"
      # - xpack.security.enabled='false'
      # - xpack.monitoring.enabled='false'
      # - xpack.watcher.enabled='false'
      # - xpack.ml.enabled='false'
      # - http.cors.enabled='true'
      # - http.cors.allow-origin="*"
      # - http.cors.allow-methods=OPTIONS, HEAD, GET, POST, PUT, DELETE
      # - http.cors.allow-headers=X-Requested-With,X-Auth-Token,Content-Type, Content-Length
      # - logger.level: debug
    ports: ['9200:9200']
    networks: ['stack']
    volumes:
      - 'es_data:/usr/share/elasticsearch/data'
    healthcheck:
      test: curl -s https://localhost:9200 >/dev/null; if [[ $$? == 52 ]]; then echo 0; else echo 1; fi
      interval: 30s
      timeout: 10s
      retries: 5
      
networks: {stack: {}}
volumes:
  es_data:
```


[![Try in PWD](https://cdn.rawgit.com/play-with-docker/stacks/cff22438/assets/images/button.png)](http://play-with-docker.com?stack=https://raw.githubusercontent.com/JinnaBalu/elasticsearch/master/single-node/docker-compose.yml)


## Run 

```bash
docker-compose up -d
```


