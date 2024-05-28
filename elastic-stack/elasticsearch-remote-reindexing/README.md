# Elasticsearch Remote reindexing

In this tutorial we'll be playing with the docker playground to understand the remote indexing with simple steps

## Step 1

- Create two instances in [Docker Playground](https://labs.play-with-docker.com/), also check with the tutorial on [Play with Docker](https://medium.com/@JinnaBalu/play-with-docker-docker-swarm-80a77d64371f)
- Create a `.env` file with the IP and the version of es we want to use. As on current we have `7.6.0` as the current version of elasticsearch 

```bash
cat << EOF>> .env
NODE_ONE_IP=192.168.0.13
NODE_TWO_IP=192.168.0.12
ES_VERSION=7.6.0
EOF
```

## Step 2

- Create a single node elasticsearch with the following docker-compose.yml

```bash
cat << EOF>> docker-compose.yml

version: '3.7'
services:
  elasticsearch-one:
    container_name: elasticsearch-one
    image: docker.elastic.co/elasticsearch/elasticsearch:${ES_VERSION}
    ports: ['9200:9200', '9300:9300']
    env_file:
      - ./.env
    environment:
      cluster.name: "test-remote-cluster"
      node.name: "es-node-one"
      network.host: 0.0.0.0
      network.publish_host: ${NODE_ONE_IP}
      transport.host: 0.0.0.0
      discovery.zen.minimum_master_nodes: 1
      discovery.type: single-node
      ES_JAVA_OPTS: "-Xms512m -Xmx512m"
      xpack.license.self_generated.type: basic
    volumes:
      - 'es_data:/usr/share/elasticsearch-one/data'
    healthcheck:
      test: curl -s https://localhost:9200 >/dev/null; if [[ $$? == 52 ]]; then echo 0; else echo 1; fi
      interval: 30s
      timeout: 10s
      retries: 5
volumes:
    es_data:
EOF
```

- Run the containers `docker-compose up -d`
- Check with the status of the containers with `docker ps -a`
- If you see the error related `max virtual memory areas vm.max_map_count [65530] is too low, increase to at least [262144]`, run the following command and restart the container. 

```bash
sudo sysctl -w vm.max_map_count=262144
```
To get more better answer for different environment use the stackoverflow answer for


-- Create the indice with the name employee with the mappings and settings defined in `sample-data/employee.json` 

```bash

curl -vX PUT 'localhost:9200/employee?pretty' -d @employee.json --header "Content-Type: application/json"
```

- Insert sample data into the indice

```bash
curl -X POST "localhost:9200/employee/_doc/1005?pretty" -H 'Content-Type: application/json' -d'
{
    "name": "Jinna",
    "age" : "29",
    "experienceInYears" : "6"
}
'
```

- Lets insert another set of 1000 records with while loop

```bash
while ! curl -s "localhost:9200/_cat/indices?v" | grep green; do
  sleep 0.1
done

for i in `seq 1 1000`; do
curl -X POST "localhost:9200/employee/_doc/$i?pretty" -H 'Content-Type: application/json' -d'
{
    "name": "Jinna$i",
    "age" : "$i",
    "experienceInYears" : "$i-1"
}
'
done
```

- Get the indices `curl -XGET  "localhost:9200/_cat/indices?v"`

### Remote reindexing

start the node
create the index


create reindex the data



