#!/bin/bash
set -e

LDAP_URI="ldap://localhost:389"
ADMIN_DN="cn=Manager,dc=vibhuvioio,dc=com"
BASE_DN="dc=vibhuvioio,dc=com"

# Use the password supplied through the container environment.
# This comes from .env via docker-compose.yml.
ADMIN_PW="${LDAP_ADMIN_PASSWORD}"

if [ -z "$ADMIN_PW" ]; then
    echo "ERROR: LDAP_ADMIN_PASSWORD is not set"
    exit 1
fi

# Secure credential file to avoid exposing the password in ps output.
CREDS_FILE=$(mktemp /tmp/ldap_creds.XXXXXX)
chmod 600 "$CREDS_FILE"

printf '%s' "$ADMIN_PW" > "$CREDS_FILE"

trap 'rm -f "$CREDS_FILE"' EXIT

echo "Waiting for LDAP to be ready..."

LDAP_READY=false

for i in {1..30}; do
    if ldapsearch \
        -x \
        -H "$LDAP_URI" \
        -b "$BASE_DN" \
        -D "$ADMIN_DN" \
        -y "$CREDS_FILE" \
        -s base \
        dn >/dev/null 2>&1
    then
        echo "LDAP is ready"
        LDAP_READY=true
        break
    fi

    echo "Attempt $i/30 failed, waiting..."
    sleep 2
done

if [ "$LDAP_READY" != "true" ]; then
    echo "ERROR: LDAP did not become ready"
    exit 1
fi

echo "Checking if VibhuviOiO data already exists..."

if ldapsearch \
    -x \
    -H "$LDAP_URI" \
    -b "ou=People,$BASE_DN" \
    -D "$ADMIN_DN" \
    -y "$CREDS_FILE" \
    "(uid=superadmin)" \
    dn 2>/dev/null | grep -q "^dn:"
then
    echo "VibhuviOiO LDAP data already exists."
    echo "Skipping initialization."
    exit 0
fi

echo "Loading VibhuviOiO users and groups..."

ldapadd \
    -x \
    -H "$LDAP_URI" \
    -D "$ADMIN_DN" \
    -y "$CREDS_FILE" \
    -c \
    -f /data/employee_data_global.ldif

echo ""
echo "VibhuviOiO LDAP initialization completed successfully."
echo ""
echo "Users:"
echo "  - superadmin"
echo "  - admin"
echo "  - developer"
echo "  - manager"
echo "  - cxp"
echo ""
echo "Groups:"
echo "  - SuperAdmin"
echo "  - Admin"
echo "  - Developer"
echo "  - Manager"
echo "  - CXP"