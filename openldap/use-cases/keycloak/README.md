# OpenLDAP + Keycloak

This use case demonstrates integrating **OpenLDAP with Keycloak** using LDAP federation.

Keycloak connects to OpenLDAP, synchronizes LDAP users, and allows those users to authenticate through Keycloak.

## Architecture

```text
                ┌─────────────────┐
                │    Keycloak     │
                │                 │
                │ LDAP Federation │
                └────────┬────────┘
                         │
                         │ LDAP Bind
                         │
                         │ Manager
                         │ CHANGEPassword123
                         ▼
                ┌─────────────────┐
                │    OpenLDAP     │
                │                 │
                │ dc=vibhuvioio   │
                └────────┬────────┘
                         │
                         │ LDAP Users
                         │
                         │ User password:
                         │ password123
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
      developer        admin        superadmin
```

## Prerequisites

Start the OpenLDAP base first:

```bash
cd ../../base
docker compose up -d
```

The OpenLDAP and Keycloak containers must be connected to the same external Docker network.

## Start Keycloak

```bash
cd use-cases/keycloak
docker compose up -d
```

Keycloak imports the realm configuration from:

```text
realm/realm.json
```

The realm configures:

* LDAP connection
* LDAP bind credentials
* User search base
* Username mapping
* Email mapping
* First-name mapping
* Last-name mapping
* Automatic user synchronization

## Verify LDAP Sync

Check the Keycloak logs:

```bash
docker logs -f keycloak
```

A successful synchronization looks like:

```text
Sync changed users finished: 5 imported users, 0 updated users
```

## Test Login

Open:

```text
http://localhost:8080
```

Select the `vibhuvioio` realm and authenticate using an LDAP user.

Example:

```text
Username: developer
Password: password123
```

The LDAP users are defined in the OpenLDAP base:

```text
../base/init/employee_data_global.ldif
```

## Configuration

The Keycloak LDAP federation configuration is stored entirely in:

```text
realm/realm.json
```

This makes the use case reproducible without manually configuring LDAP federation through the Keycloak UI.

## Reset the Lab

To completely recreate the environment:

```bash
# OpenLDAP
cd ../../base
docker compose down -v
docker compose up -d

# Keycloak
cd ../use-cases/keycloak
docker compose down -v
docker compose up -d
```

> **Note:** `down -v` removes the containers' volumes and therefore resets the lab data.

## What This Lab Demonstrates

* OpenLDAP as an external identity store
* Keycloak LDAP federation
* LDAP user synchronization
* LDAP attribute mapping
* Keycloak authentication against LDAP
* Reproducible Keycloak realm configuration
* Docker Compose based identity infrastructure
