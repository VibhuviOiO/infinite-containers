# VibhuviOiO LDAP

OpenLDAP configuration for the VibhuviOiO environment using the `vibhuvioio/openldap:latest` Docker image.

This directory provides the **base LDAP environment** used by the integration labs under `use-cases/`.

## Directory Structure

```text
base/
├── docker-compose.yml
├── README.md
├── init/
│   ├── employee_data_global.ldif
│   └── init-data.sh
└── logs/
    └── slapd.log
```

## LDAP Configuration

| Setting     | Value                             |
| ----------- | --------------------------------- |
| LDAP Domain | `vibhuvioio.com`                  |
| Base DN     | `dc=vibhuvioio,dc=com`            |
| Admin DN    | `cn=Manager,dc=vibhuvioio,dc=com` |
| LDAP Port   | `389`                             |
| LDAPS Port  | `636`                             |
| Replication | Disabled                          |
| Monitoring  | Enabled                           |

## Directory Layout

```text
dc=vibhuvioio,dc=com
├── ou=People
├── ou=Group
└── ou=Services
```

Users are stored under:

```text
ou=People,dc=vibhuvioio,dc=com
```

Groups are stored under:

```text
ou=Group,dc=vibhuvioio,dc=com
```

## Users

Initial users are defined in:

```text
init/employee_data_global.ldif
```

Current users:

```text
superadmin
admin
developer
manager
cxp
```

Example:

```text
uid=admin,ou=People,dc=vibhuvioio,dc=com
```

## Groups

Current groups:

```text
SuperAdmin
Admin
Developer
Manager
CXP
```

Groups use the `groupOfNames` object class and reference users through the `member` attribute.

Example:

```text
cn=Admin,ou=Group,dc=vibhuvioio,dc=com
```

## Schemas

The following schemas are enabled:

```text
cosine
inetorgperson
nis
```

They are configured using:

```text
INCLUDE_SCHEMAS=cosine,inetorgperson,nis
```

## Initialization

The initialization script is:

```text
init/init-data.sh
```

It is mounted into:

```text
/docker-entrypoint-initdb.d/init-data.sh
```

The script:

1. Waits for LDAP to become available.
2. Authenticates using the Manager DN.
3. Checks whether the initial LDAP data already exists.
4. Loads `employee_data_global.ldif` when required.
5. Skips initialization when the data already exists.

This allows the LDAP environment to be recreated consistently while preserving existing data in persistent volumes.

## Start OpenLDAP

```bash
docker compose up -d
```

Check the container:

```bash
docker ps
```

Check logs:

```bash
docker logs -f openldap
```

## Verify Manager Authentication

```bash
docker exec openldap ldapwhoami \
  -x \
  -H ldap://localhost:389 \
  -D "cn=Manager,dc=vibhuvioio,dc=com" \
  -w 'CHANGEPassword123'
```

Expected:

```text
dn:cn=Manager,dc=vibhuvioio,dc=com
```

> Replace the password with the value configured in your environment.

## Verify Users

```bash
docker exec openldap ldapsearch \
  -x \
  -H ldap://localhost:389 \
  -D "cn=Manager,dc=vibhuvioio,dc=com" \
  -w 'CHANGEPassword123' \
  -b "ou=People,dc=vibhuvioio,dc=com" \
  "(objectClass=inetOrgPerson)" \
  uid cn mail
```

## Verify Groups

```bash
docker exec openldap ldapsearch \
  -x \
  -H ldap://localhost:389 \
  -D "cn=Manager,dc=vibhuvioio,dc=com" \
  -w 'CHANGEPassword123' \
  -b "ou=Group,dc=vibhuvioio,dc=com" \
  "(objectClass=groupOfNames)" \
  cn member
```

## Persistent Data

LDAP data is stored in:

```text
ldap-data
ldap-config
```

These volumes contain the LDAP database and configuration.

Avoid removing them unless you intentionally want to reset the directory.

## Reset the Lab

To completely recreate the LDAP environment:

```bash
docker compose down -v
docker compose up -d
```

> **Warning:** `down -v` deletes the LDAP data and configuration stored in Docker volumes.

The initialization process will recreate the configured users and groups.

## Logs

Container logs:

```bash
docker logs -f openldap
```

Host-mounted LDAP logs:

```text
logs/slapd.log
```

## Integration Labs

The base LDAP environment can be used by different applications and services.

Current integrations:

```text
use-cases/
└── keycloak/
```

Additional integrations can be added independently without changing the base LDAP configuration.

## Current Status

The base LDAP environment has been validated with:

* LDAP service running
* Manager authentication
* Base DN created
* Users loaded
* Groups loaded
* `cosine` schema loaded
* `inetorgperson` schema loaded
* `nis` schema loaded
* LDAP monitoring enabled
* Persistent LDAP volumes
* Idempotent initialization
