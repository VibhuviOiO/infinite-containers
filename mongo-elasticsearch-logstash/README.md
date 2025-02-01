# Data Pipeline:
**Use-case:** Read data from mongodb collection to elasticsearch indice
- Run mongodb as container
- Import different types of the data to a collection
- Run elasticsearch as container with kibana
- Create the logstash pipeline
- Validate the data

## Pre-requisites:
- Docker
- Docker Compose
- Clone the [repo]
- Create the docker network `docker network create datapipeline`

#### Run mongodb as container
- We'll be running mongo-express and mongodb as container with the following
```bash
docker compose -f mongo.yml up -d
```
- Import data into the mongo 
  ```bash
  docker cp movies.json mongodb:/
  docker exec -it mongodb bash
  mongosh
  use moviedb
  exit()
  mongoimport --db moviedb --collection movies --file /movies.json --jsonArray
  ```
- Access the mongo-express on [http://localhost:8081/](http://localhost:8081/)

#### Run elasticsearch as container
- Create the .env with the required environment variables.
- Run the elasticsearch three node clsuetr with kibana as container with the following html)
```bash
docker compose -f elasticsearch-kibana.yml up -d
```
- Access the kibana on [http://localhost:5601/](http://localhost:5601/)
> Note: Followed [Install Elasticsearch with Docker](https://www.elastic.co/guide/en/elasticsearch/reference/current/docker) instructions from the elasticsearch.

#### Run logstash
- Create the custom logstash docker image with mongo drivers, we can configure everything docker-compose but, for every restart it has to do the same activity which is time consuming, I prefer creating the custom docker image.
    - Download the mongo drivers from [Open-Source MongoDb JDBC Driver](https://dbschema.com/jdbc-driver/mongodb.html#DbSchema) and extract to `drivers` folder. `wget ` 
    - Create the docker image `docker build -t mongologstash .`
- Create the pipeline configuration. 
- Run the logstash container
```bash
docker compose -f logstash.yml up -d
```

> **Note:** Pipeline is self explanatory, if you read through the type data we have in the movie.json file, you will see the types of data coverted, and read each and every line of the pipeline to understand how that is write for different data types, and has respective comments for each type to explain better.

#### What is covered in the pipeline

I am taking an example of the movies data for running the pipleine to cover the multiple type sof data moving from mongodb to elasticsearch. 

**Strings:** "title", "name", "role".
**Numbers:** "rating", "releaseYear", "budget".
**Boolean:** "isAvailable".
**Dates:** "releaseDate".
**Nested Objects:**
  - "director" object contains details about the director.
  - "profit" is nested within "boxOffice".
**Arrays:**
  - "genres" is an array of strings.
  - "cast" is an array of objects.
**Array of Objects:** "cast" contains objects with actor details ("name", "role", "age").
**ObjectId:** _id is an ObjectId, representing MongoDB's unique identifier for each record.
**Null Value:** "age" of the director in the second record is null to show handling missing data.


#### Crean up:
```bash
docker stop $(docker ps -qa) && docker rm $(docker ps -qa) && docker volume rm $(docker volume ls -q -f dangling=true)
```
