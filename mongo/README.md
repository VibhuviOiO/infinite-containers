# MongoDB as Container 

- [Create the keyfile for Internal Authentication](https://jinnabalu.com/Create-keyfile-for-MongoDB)
- [MongoDB Single Node Cluster with Replicaset](https://jinnabalu.com/Mongo-Single-Node-Cluster)
- [MongoDB 3 Node Cluster in Single Server with Replicaset](https://jinnabalu.com/Mongo-Three-Node-Cluster)
- [Validate the MongoDB Cluster]()
- [MongoDB 3 Node Cluster in Three Servers with Replicaset for Production]()
- [Connect to MongoSH and create collection]()
- [Common Commands used to interact with mongodb cluster]()
- [Errors in MongoDB Cluster Setup]()

## MongoDB Single Node Replica Set for dev environment

### Enabling Auth for Security
Generate keyfile for the machine you are working with

#### Mac
- Create the file if you are on mac and running as a container
```bash
openssl rand -base64 741 >> mongoKeyFileMac
chmod 600 mongoKeyFileMac
```

#### Linux
- Create the file if you are on linux and running as a container
```bash
openssl rand -base64 756 > mongoKeyFileLinux
chmod 600 mongoKeyFileLinux

# Do the foillowing commands at server lever

sudo chown 999 mongoKeyFileLinux
sudo chgrp 999 mongoKeyFileLinux
```

### Single Node 

#### Run the mongodb single node replicaset with docker-compose

- Run the application 

```bash
cd docker-mongo/single-node-rs
docker-compose up -d
```
- Restart the service 

```bash
cd docker-mongo/single-node-rs
docker-compose down
docker-compose up -d
```

#### Connection String

Here is the connection string for connecting to the mongo client from the any programing lang

```bash
mongodb://mongouser:mongopass@127.0.0.1:27017/?authSource=admin&readPreference=primary&ssl=false&replicaSet=mongo-rs
```

# Deploying Mongo 3 Node Cluster 

- Using docker-compose

```bash
cd three-node-rs/
docker-compose down
docker-compose up -d
```

### Initialise the 3 node cluster 

```bash
docker exec -it mongo1 mongosh --quiet -u mongouser -p mongopass --eval "rs.initiate({
 _id: \"mongo-rs\",
 members: [
   {_id: 0, host: \"mongo1\"},
   {_id: 1, host: \"mongo2\"},
   {_id: 2, host: \"mongo3\"}
 ]
})"
```

Expected Output is 

```bash
{ ok: 1 }
```
### Connect to MongoSH and create collection

```bash
# Connect to the mongo container
docker exec -it mongodb bash

# Connect to the mongosh client within the mongo container
mongosh --quiet -u mongouser -p mongopass

# Use any database, it creates the db if it doesn't exists
use devdb

# Create the collection with document inser query, which creates the schema and inserts document into the collection

db.movie.insert({"name":"Avengers: Endgame"})

# Get all the data from the movie collection 

db.movie.find()
```


### Verify the Multinode replica set with mongoDB 

- Verify the cluster
```bash
docker exec -it mongo1 mongosh --eval "rs.status()"
docker exec -it mongo2 mongosh --eval "rs.status()"
docker exec -it mongo3 mongosh --eval "rs.status()"
```
- Stop any node, `mongo1` and verify cluster connecting to `mongo2` or `mongo3`

```bash
docker stop mongo1
docker exec -it mongo2 mongosh --eval "rs.status()"
docker exec -it mongo-three mongosh --eval "rs.status()"
```
