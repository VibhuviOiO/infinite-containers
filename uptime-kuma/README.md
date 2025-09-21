# Run Uptime Kuma
- Create the `docker-compose.yml` file 
- Execute the following
```bash

sudo mkdir -p /data/uptime/mariadb-data
sudo chown -R 999:999 /data/uptime/mariadb-data
sudo chcon -Rt svirt_sandbox_file_t /data/uptime/mariadb-data
podman compose -f mariadb.yml up -d
podman compose -f uptime.yml up -d
```
- We are running three services. MariaDB, UptimeKuma, PhpAdmin(UI for MariaDB)
- Connect through any service with tunnel

## Bulk Import the ping servers with csv using PhpAdmin

- Tunnel PHPAdmin with 8080 
- Open service on ont he browser -> expand `kuma_db` in the databases -> click on monitor table -> click on import -> choose `CSV` --> enter columns `name, type, interval, retry_interval, hostname, parent, active, user_id, method` -> click on import.
- Refresh the browsers you will see the data imported
- Either restart the uptime service with `podman compose -f uptime.yml down && podman compose -f uptime.yml up -d` or pause the monitoring and resume monitoring. 