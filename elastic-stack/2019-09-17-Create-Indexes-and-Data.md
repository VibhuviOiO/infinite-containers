---
title:  "Create Indexes in elasticsearch and  frequently used commands"
metadate: "hide"
categories: [ NoSQL, Search Engine, Elasticsearch ]
tags: [ Elasticsearch ]
image: "/assets/images/elasticsearch.svg"
---

## Preface

## Preface

This post assumes that you have some basic understanding of Docker, Docker Compose, and the key components used in the docker ecosystem. Get up to speed, with the [Prepare Your Docker Eenvironment](https://docs.docker.com/get-started/#prepare-your-docker-environment) section of Docker docs.

1. Install [Docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
2. Install [docker-compose](https://docs.docker.com/compose/install/)
3. Install Elasticsearch or [Run Elasticsearch container](https://github.com/JinnaBalu/elasticsearch/blob/master/2019-08-29-Elasticsearch-Single-Node-using-Docker-Compose.md)


## Frequently used commands

- Check the status of the Elasticsearch

- Check the health status of the Elasticsearch

```bash
curl -X GET "localhost:9200/_cat/health"
```

- Get the number of nodes of the Elasticsearch Cluster

```bash
curl -X GET "localhost:9200/_cat/nodes"
```

- Check with the shards with 

```bash
curl -X GET "localhost:9200/_cat/shards"
```

- Get list of indices

```bash
curl -X GET "localhost:9200/_cat/indices?v"
```

- Get list of indices with specific column, we want to the column index, which will list the index names

```bash
curl -X GET "localhost:9200/_cat/indices?v&h=index"
```

- Get the list of indices sort by column

```bash
curl -X GET "localhost:9200/_cat/indices?v&s=docs.count:desc"

curl -X GET "localhost:9200/_cat/indices?v&s=docs.count:asc"

curl -X GET "localhost:9200/_cat/indices?v&s=index"

curl -X GET "localhost:9200/_cat/indices?v&s=docs.count:desc"

curl -X GET "localhost:9200/_cat/indices?v&s=docs.count:desc"
```

- Why the health status of the Elasticsearch is `red`

Number of nodes in the cluster was three so there was no extra node to create the replica, and restore the unassigned indexes, So the health was turning to red. Created the index with settings property and set the number_of_replicas as 0.

```bash
curl -XPUT 'localhost:9200/_settings' -H 'Content-Type: application/json' -d '
{
    "index" : {
        "number_of_replicas" : 0
    }
}'
```

curl -X PUT "localhost:9200/_cluster/settings?pretty" -H 'Content-Type: application/json' -d'
{
  "transient": {
    "cluster.routing.allocation.disk.watermark.low": "97%",
    "cluster.routing.allocation.disk.watermark.high": "98%",
    "cluster.routing.allocation.disk.watermark.flood_stage": "99%"
  }
}
'

### Create the Indice

- First, let's create a twitter user, and add some tweets

```bash
curl -XPUT 'http://127.0.0.1:9200/twitter/user/kimchy' -d '{ "name" : "Shay Banon" }'

curl -X PUT "localhost:9200/_cluster/settings?pretty" -H 'Content-Type: application/json' -d'
{
    "user": "kimchy",
    "postDate": "2009-11-15T13:12:00",
    "message": "Trying out Elasticsearch multinode, so far so good?"
}'

curl -XPUT 'http://127.0.0.1:9200/twitter/tweet/2' -d '
{
    "user": "kimchy",
    "postDate": "2009-11-15T14:12:12",
    "message": "Balu tweet, will it be indexed?"
}'
```

curl -X PUT "localhost:9200/_cluster/settings?pretty" -H 'Content-Type: application/json' -d'
{
  "persistent": {
    "action.auto_create_index": "my-index-000001,index10,-index1*,+ind*" 
  }
}
'
curl -X PUT "localhost:9200/_cluster/settings?pretty" -H 'Content-Type: application/json' -d'
{
  "persistent": {
    "action.auto_create_index": "false" 
  }
}
'
curl -X PUT "localhost:9200/_cluster/settings?pretty" -H 'Content-Type: application/json' -d'
{
  "persistent": {
    "action.auto_create_index": "true" 
  }
}
'


- Now, let's see if the information was added by GETting it:

```bash
curl -XGET 'http://127.0.0.1:9200/twitter/user/kimchy?pretty=true'
curl -XGET 'http://127.0.0.1:9200/twitter/tweet/1?pretty=true'
curl -XGET 'http://127.0.0.1:9200/twitter/tweet/2?pretty=true'
```

- Create customer entity with 1000 records 

```bash
curl -X PUT "localhost:9200/customer?pretty" -H 'Content-Type: application/json' -d'
{
  "settings": {
    "index": {
      "number_of_shards": 5,  
      "number_of_replicas": 0 
    }
  }
}
'



while ! curl -s "localhost:9200/_cat/indices?v" | grep green; do
  sleep 0.1
done

for i in `seq 1 10`; do
  curl -sXPUT "localhost:9200/customer/external/$i?pretty" -d "
  {
    \"id\": $i,
    \"name\": \"John Doe - $i\"
  }"
done
```


- Create student entity with 1000 records 

```bash
curl -sXPUT 'http://localhost:9200/student/?pretty' -d '{
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
  curl -sXPUT "localhost:9200/student/external/$i?pretty" -d "
  {
    \"number\": $i,
    \"name\": \"Ram - $i\"
  }"
done
```

- Somemore examples

```bash
curl -X PUT "localhost:9200/twitter?pretty"

curl -X PUT "localhost:9200/school?pretty" -H 'Content-Type: application/json' -d'
{
    "settings" : {
        "number_of_shards" : 3,
        "number_of_replicas" : 2
    },
    "mappings" : {
        "properties" : {
            "name" : { "type" : "text" }
        }
    }
}
'
```

### Delete index

```bash
curl -X DELETE "localhost:9200/school?pretty"
```

### Get Index

- Get the mappings and setting with the following

```bash
curl -X GET "localhost:9200/school?pretty"

curl -X GET "localhost:9200/school/_mapping?pretty"

curl -X GET "localhost:9200/school/_settings?pretty"

```

- Checks if an index exists

```bash
curl -I "localhost:9200/twitter?pretty"
```

- Get the count of Index

```bash
curl -I "localhost:9200/twitter?pretty"
```

- Update index settings API

```bash
curl -X PUT "localhost:9200/school/_settings?pretty" -H 'Content-Type: application/json' -d'
{
    "index" : {
        "number_of_replicas" : 2
    }
}
'
```

- Get the Statistics of the index

```bash
curl -X GET "localhost:9200/school/_stats?pretty"

curl -X GET "localhost:9200/_stats?pretty"

curl -X GET "localhost:9200/index1,index2/_stats?pretty"
```
