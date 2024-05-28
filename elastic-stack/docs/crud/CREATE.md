# CRUD Operations

## Create

Elasticsearch supports runtime indexing with dynamic mappings. Mapping datatypes will be created with the values. Otherwise think it like creating the index with

### Create Index with  Mapping

#### Create the index only with mappings defined

```bash
curl -X PUT "localhost:9200/customer?pretty" -H 'Content-Type: application/json' -d'
{
  "settings": {
    "number_of_shards": 5,  
    "number_of_replicas": 0 
  },
  "mappings": {
    "properties": {
      "name": { "type": "text" }
    }
  }
}
'
```

Above query creates the index with mappings

#### Get list of indices

```bash
curl -X GET "localhost:9200/_cat/indices?v"
```
**OUTPUT**:

|health|status|index|uuid|pri|rep|docs.count|docs.deleted|store.size|pri.store.size|
|---|---|---|---|---|---|---|---|---|---|
|green|open|customer|NwVUkAz3ROWCbuG2MxFYVw|5|0|2|0|7.6kb|7.6kb|


#### Get the mappings and setting 

```bash
curl -X GET "localhost:9200/customer?pretty"
```
**Output**:
```json
{
  "customer" : {
    "aliases" : { },
    "mappings" : {
      "properties" : {
        "name" : {
          "type" : "text"
        }
      }
    },
    "settings" : {
      "index" : {
        "routing" : {
          "allocation" : {
            "include" : {
              "_tier_preference" : "data_content"
            }
          }
        },
        "number_of_shards" : "5",
        "provided_name" : "customer",
        "creation_date" : "1663736397929",
        "number_of_replicas" : "0",
        "uuid" : "NwVUkAz3ROWCbuG2MxFYVw",
        "version" : {
          "created" : "8040199"
        }
      }
    }
  }
}
```

#### Insert Data into index 

```bash
curl -X POST "localhost:9200/customer/_doc/?pretty" -H 'Content-Type: application/json' -d'
{
  "name": "Ram"
}
'

curl -X POST "localhost:9200/customer/_doc/?pretty" -H 'Content-Type: application/json' -d'
{
  "name": "Laxman"
}
'
```

#### Search the index

```bash
curl -X GET "localhost:9200/customer/_search?pretty" 
```

**Output**:
```json
{
  "took" : 628,
  "timed_out" : false,
  "_shards" : {
    "total" : 5,
    "successful" : 5,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 2,
      "relation" : "eq"
    },
    "max_score" : 1.0,
    "hits" : [
      {
        "_index" : "customer",
        "_id" : "mztvXoMB9Df6ADGYd_up",
        "_score" : 1.0,
        "_source" : {
          "name" : "Laxman"
        }
      },
      {
        "_index" : "customer",
        "_id" : "mjtrXoMB9Df6ADGYrfud",
        "_score" : 1.0,
        "_source" : {
          "name" : "Ram"
        }
      }
    ]
  }
}

```


### Insert Data with new mappings

Insert the new `json` object into the `customer` index and checkl the mappings. Create and update mappings with insert json object

```bash
curl -X POST "localhost:9200/customer/_doc/?pretty" -H 'Content-Type: application/json' -d'
{
  "name": "Bharatha",
  "birth_order": "Youngest Middle Child"
}
'
```

**Output**:

```bash
{
  "_index" : "customer",
  "_id" : "nDt4XoMB9Df6ADGYgvvf",
  "_version" : 1,
  "result" : "created",
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "failed" : 0
  },
  "_seq_no" : 1,
  "_primary_term" : 1
}
```

Try to get the mappings and see, you will be seeing the new mapping added with the default mapping type for string type of the value

```json
....
"properties" : {
  "birth_order" : {
    "type" : "text",
    "fields" : {
      "keyword" : {
        "type" : "keyword",
        "ignore_above" : 256
      }
    }
  },
  "name" : {
    "type" : "text"
  }
}
....
```
