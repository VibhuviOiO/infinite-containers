# Running local docker registry

This is safe to run in local network without opening the port or service to the external network which is public facing. 

Here we are running docker registry  with the docker registry UI, is optional. It is just a GUI to view and search for the docker image. 

#### Run as container

Created the docker compose for the `registry` and `joxit/docker-registry-ui`, run with `docker-compose up -d`

#### Tag the image and push

```bash
docker image pull debian 
docker tag debian localhost:5000/debian
docker push localhost:5000/debian
```

#### Clean 

Remove the volume and delete the containers with `docker-compose down --volumes --rmi all`