# CRUD Operations

## Create

Elasticsearch supports runtime indexing with dynamic mappings. Mapping datatypes will be created with the values. Otherwise think it like creating the index with

### Create Index with  Mapping

- Create the index only with mappings defined

```bash
curl -X PUT "localhost:9200/test?pretty" -H 'Content-Type: application/json' -d'
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

Above query creates the index only without mappings

### Insert Data 

### Create and Insert Data both with Insert Data


## Update

## Delete

## Search