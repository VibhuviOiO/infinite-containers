
Optional : 

- Create the docker network with `bridge network` with a specific CIDR for assigning static IPs `docker network create --subnet=192.168.1.0/24 cassandra-network`
- CIDR 192.168.1.0/24 provides IPs in the range 192.168.1.1 to 192.168.1.254. You can pick any two IPs (e.g., 192.168.1.10 and 192.168.1.11) for the nodes.
