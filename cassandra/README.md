# Running cassandra as container

- Run cassandra container with `docker-compose up -d`
- Create keyspace and tables in the cassandra with the following
```bash
docker exec -it cassandra bash

## OUTPUT: 

root@cassandra-db:/# cqlsh
Connected to SolarSystem at 127.0.0.1:9042.
[cqlsh 5.0.1 | Cassandra 3.11.10 | CQL spec 3.4.4 | Native protocol v4]
Use HELP for help.
cqlsh> 

## Create keyspace 

cqlsh> CREATE KEYSPACE ramayana
   ... WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};
cqlsh> use ramayana ;
cqlsh:ramayana>

## Create table 

cqlsh:ramayana> CREATE TABLE ramayana.characters (
            ...     id UUID PRIMARY KEY,
            ...     name TEXT,
            ...     description TEXT
            ... );

## Insert some data

cqlsh:ramayana> INSERT INTO characters (id, name, description) VALUES (uuid(), 'Rama', 'Hero of the Ramayana, seventh avatar of Vishnu.');
cqlsh:ramayana> INSERT INTO characters (id, name, description) VALUES (uuid(), 'Sita', 'Wife of Rama and central character of the Ramayana.');
cqlsh:ramayana> INSERT INTO characters (id, name, description) VALUES (uuid(), 'Lakshmana', 'Brother of Rama and loyal companion.');
```

### Test Client with NodeJS
- Create npm application `npm init -y`
- Install cassandra driver `npm install cassandra-driver`
- Run the index.js (Review the code for index.js which is copied from the cassandra-driver package )

```
node index.js
```