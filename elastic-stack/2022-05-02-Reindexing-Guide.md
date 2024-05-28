# Elasticsearch Reindexing API

## Get Mapings and setting 

```bash
curl -XGET 'localhost:9200/<INDEX_NAME>/_mappings?pretty' >> original-mappings-settings.json

# example
curl -XGET 'localhost:9200/<INDEX_NAME>/_mappings?pretty' >> original-mappings-settings.json
````
## Create index.json

```json
{
	"settings" : {},
	"mappings" : {}
}
```

#### Remove the following properties from the settings

Omitting the following setting will allow us to create the new index

- index.creation_date
- index.version.created
- index.provided_name
- index.uuid

### Create the new index with the different name 
curl -vX PUT 'localhost:9200/<INDEX_NAME>_02052022?pretty' -d @index.json --header "Content-Type: application/json"

```bash
root@ip-192-31-2-66:/home/ubuntu/reindexing/<INDEX_NAME>_02052022# curl -vX PUT 'localhost:9200/<INDEX_NAME>_02052022?pretty' -d @index.json --header "Content-Type: application/json"
*   Trying 127.0.0.1...
* TCP_NODELAY set
* Connected to localhost (127.0.0.1) port 9200 (#0)
> PUT /<INDEX_NAME>_02052022?pretty HTTP/1.1
> Host: localhost:9200
> User-Agent: curl/7.58.0
> Accept: */*
> Content-Type: application/json
> Content-Length: 11624
> Expect: 100-continue
>
< HTTP/1.1 100 Continue
* We are completely uploaded and fine
< HTTP/1.1 200 OK
< content-type: application/json; charset=UTF-8
< content-length: 94
<
{
  "acknowledged" : true,
  "shards_acknowledged" : true,
  "index" : "<INDEX_NAME>_02052022"
}
* Connection #0 to host localhost left intact
```


curl -vXPOST 'localhost:9200/_reindex?pretty' -H 'Content-Type: application/json' -d'
{
  "source": {
    "index": "<INDEX_NAME>"
  },
  "dest": {
    "index": "<INDEX_NAME>_02052022"
  }
}
' >> result.txt

curl -XGET 'localhost:9200/<INDEX_NAME>/_count?pretty'

curl -XGET 'localhost:9200/<INDEX_NAME>_02052022/_count?pretty'

# Delete the old index    curl -X DELETE 'localhost:9200/<INDEX_NAME>?pretty'
curl -XPOST 'localhost:9200/_aliases?pretty' -H 'Content-Type: application/json' -d'
{
    "actions" : [
        { "add" : { "index" : "<INDEX_NAME>_02052022", "alias" : "<INDEX_NAME>" } }
    ]
}
'

curl -XGET 'localhost:9200/<INDEX_NAME>/_count?pretty'

curl -XGET 'localhost:9200/<INDEX_NAME>_02052022/_count?pretty'