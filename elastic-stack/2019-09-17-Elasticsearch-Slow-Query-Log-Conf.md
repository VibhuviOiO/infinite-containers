---
title:  "Elasticsearch Slow Query Log Configuration"
metadate: "hide"
categories: [ NoSQL, Elasticsearch ]
tags: [ Elasticsearch ]
image: "/assets/images/elasticsearch.svg"
---

## Slow Logs in Elasticsearch
- 1. Search slow logs - used to log the searches which are slow
- 2. Index slow logs

### Search Slow Logs

Search slow logs are used to log the searches which are slow. The slowness threshold depends on the application and its Elasticsearch implementation details. Each application can have different thresholds.

#### Search in Elasticsearch happens in two phases:

Query phase - In the query phase, Elasticsearch collects document ids of the relevant results. Upon the completion of this phase, only the ids of the documents which are matched against the search are returned, and there will be no other information like the fields or their values, etc.
Fetch phase - In the fetch phase, the documents ids from the query phase are used to fetch the real documents, and with this the search request can be said to be complete.
Search slow logs show the split times for both the query and the fetch phases with the query. Thus, we are able to get a complete picture of the time taken to complete the query and the fetch phases, and are able to inspect the entire query itself.

### Index Slow Logs

### Configuration sin elasticsearch

- elasticsearch.yml
- jvm.options
- log4j2.properties

- Run Single node elasticsearch

```bash
docker-compose up -d 
```

- Create the index

- Create student entity with 1000 records 

```bash
curl -sXPUT 'http://localhost:9200/student/?pretty' -H 'Content-Type: application/json' -d '{
  "settings" : {
      "index" : {
          "number_of_shards" : 5,
          "number_of_replicas" : 0
      }
  }
}'

while ! curl -s "localhost:9200/_cat/indices?v" | grep green; do
  sleep 0.1
done

for i in `seq 1 20`; do
  curl -sXPUT "localhost:9200/student/$i?pretty" -H 'Content-Type: application/json' -d "
  {
    \"number\": $i,
    \"name\": \"Ram - $i\"
  }"
done
```

