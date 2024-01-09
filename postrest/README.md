# Postrest POC

- RUn the container `docker-compose up -d`
- Enter into the container `docker exec -it postgres psql -U app_user -d app_db`
- Create a table `student` and insert some data

```sql
CREATE TABLE IF NOT EXISTS student (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    rolenumber INT
);

INSERT INTO student (name, rolenumber) VALUES
    ('Ram', 101),
    ('Seetha', 102),
    ('Laxmana', 106);
```
## Test the postrest
- GET : Open the browser with [http://localhost:3000/student](http://localhost:3000/student) or execute the `curl -X GET http://localhost:3000/student`
- POST :

```bash
curl -X 'POST' \
  'http://0.0.0.0:3000/student' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "id": 3,
  "name": "Bharata",
  "rolenumber": 103
}'

curl -X 'POST' \
  'http://0.0.0.0:3000/student' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "id": 4,
  "name": "Shathragna",
  "rolenumber": 104
}'

```
- PUT :
```bash
curl -X PUT \
  'http://localhost:3000/student?id=eq.10' \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"id": 10, "name": "Shathragjna", "rolenumber": 105}'
```
- DELETE:
```bash
 curl -X DELETE \
  'http://localhost:3000/student?id=eq.1' \ 
  -H 'Accept: application/json'
```