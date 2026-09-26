## Cassandra

Install with command or use the dashboard to install plugins 

```bash
docker exec grafana grafana-cli plugins install hadesarchitect-cassandra-datasource

# OUTPUT
✔ Downloaded hadesarchitect-cassandra-datasource v3.0.0 zip successfully

Please restart Grafana after installing plugins. Refer to Grafana documentation for instructions if necessary.
```


- Creating the readonly requires 

authenticator: org.apache.cassandra.auth.PasswordAuthenticator
authorizer: org.apache.cassandra.auth.CassandraAuthorizer