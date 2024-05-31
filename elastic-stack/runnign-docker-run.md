Elasticsearch security features have been automatically configured!
✅ Authentication is enabled and cluster connections are encrypted.

ℹ️  Password for the elastic user (reset with `bin/elasticsearch-reset-password -u elastic`):
  4GxnqQgK*maDhJ1hyIKz

ℹ️  HTTP CA certificate SHA-256 fingerprint:
  e5184a288123796ef0e53a54c95527f17493727f95a9b54d219f9784673e5a0e

ℹ️  Configure Kibana to use this cluster:
• Run Kibana and click the configuration link in the terminal when Kibana starts.
• Copy the following enrollment token and paste it into Kibana in your browser (valid for the next 30 minutes):
  eyJ2ZXIiOiI4LjEzLjQiLCJhZHIiOlsiMTcyLjE5LjAuMjo5MjAwIl0sImZnciI6ImU1MTg0YTI4ODEyMzc5NmVmMGU1M2E1NGM5NTUyN2YxNzQ5MzcyN2Y5NWE5YjU0ZDIxOWY5Nzg0NjczZTVhMGUiLCJrZXkiOiJsN1VhMEk4QmgwYjVYR1Ftb1FoUDpoOUpQcTFtRFJ2bU1XSnhZX2NpQm13In0=

ℹ️ Configure other nodes to join this cluster:
• Copy the following enrollment token and start new Elasticsearch nodes with `bin/elasticsearch --enrollment-token <token>` (valid for the next 30 minutes):
  eyJ2ZXIiOiI4LjEzLjQiLCJhZHIiOlsiMTcyLjE5LjAuMjo5MjAwIl0sImZnciI6ImU1MTg0YTI4ODEyMzc5NmVmMGU1M2E1NGM5NTUyN2YxNzQ5MzcyN2Y5NWE5YjU0ZDIxOWY5Nzg0NjczZTVhMGUiLCJrZXkiOiJtYlVhMEk4QmgwYjVYR1Ftb1FoUTpJVWVsbVZkLVJES2hZQ0RaUTM1RUdBIn0=

  If you're running in Docker, copy the enrollment token and run:
  `docker run -e "ENROLLMENT_TOKEN=<token>" docker.elastic.co/elasticsearch/elasticsearch:8.13.4`