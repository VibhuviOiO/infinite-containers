## Security recommendations and their status:

  ⚠️ Use a custom cluster name
  ✅ Disable member multicast discovery/join method
  ⚠️ Use advanced networking, separate client and member sockets
  ⚠️ Bind Server sockets to a single network interface (disable hazelcast.socket.server.bind.any)
  ⚠️ Allow Management Center operations only from specified remote addresses (use management-center/trusted-interfaces configuration)
  ✅ Disable scripting in the Management Center
  ✅ Disable console in the Management Center
  ⚠️ Enable Security (Enterprise)
  ⚠️ Use TLS communication protection (Enterprise)
  ⚠️ Enable auditlog (Enterprise)

Check the hazelcast-security-hardened.xml/yaml example config file to find why and how to configure these security related settings.

To view all kind of configurations and examples get into the container running it isolated and understand what kind of configurations are defined by default with the following steps. 

```bash
docker run hazelcast/hazelcast:5.4.0 -d --name learn_hazelcast

docker exec -it learn_hazelcast bash

bc4581d87851:/opt/hazelcast$ cd config/

bc4581d87851:/opt/hazelcast/config$ ls
examples                hazelcast-docker.xml    jmx_agent_config.yaml   jvm.options             log4j2.properties
hazelcast-client.xml    hazelcast.xml           jvm-client.options      log4j2-json.properties

bc4581d87851:/opt/hazelcast/config/examples$ ls
hazelcast-client-full-example.xml   hazelcast-docker.yaml               hazelcast-security-hardened.xml
hazelcast-client-full-example.yaml  hazelcast-full-example.xml          hazelcast-security-hardened.yaml
hazelcast-client.yaml               hazelcast-full-example.yaml         hazelcast.yaml
```

Adjust the configurations as defined in the default and examples available. and restart the container. 

