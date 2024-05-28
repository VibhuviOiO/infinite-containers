for index in i1 i2 i3 i4 i5; do
  curl -H Content-Type:application/json -XPOST localhost:9200/_reindex?pretty -d'{
    "source": {
        "remote": {
        "host": "http://otherhost:9200",
        "username": "user",
        "password": "pass"
    },
      "index": "'$index'"
    },
    "dest": {
      "index": "'$index'-reindexed"
    }
  }'
done

curl -XGET '10.10.10.34:9200/_cat/indices?v' | grep "consu"

curl -XGET '10.10.10.34:9200/consultant?pretty' >> consultant__mappings_and_settings.json

# Create the index.json from above json and copy to the server

curl -vX PUT 'localhost:9200/di_consultant_new?pretty' -d @index.json --header "Content-Type: application/json"


curl -H Content-Type:application/json -XPOST localhost:9200/_reindex?pretty -d'{
  "source": {
      "remote": {
        "host": "http://10.10.10.34:9200"
      },
      "index": "consultant",
      "query": {
        "range": {
          "createdOn": {
            "gte": "2022-06-04",
            "lte": "2022-07-04"
          }
        }
      }
  },
  "dest": {
    "index": "di_consultant_new"
  }
}'