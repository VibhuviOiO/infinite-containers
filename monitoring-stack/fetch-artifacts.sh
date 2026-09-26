#!/usr/bin/env bash
# Everything this stack borrows from the exporter repo is fetched at setup time
# and gitignored, so rules and dashboards are maintained in exactly one place.
# Re-run after the exporter repo changes; do not copy these files in by hand.
set -euo pipefail
cd "$(dirname "$0")"

base="https://raw.githubusercontent.com/VibhuviOiO/openldap-exporter/main"

fetch() { # <remote path> <local path> <label> [count cmd]
  mkdir -p "$(dirname "$2")"
  curl -fsSL "$base/$1" -o "$2"
  printf '  %-28s -> %s\n' "$1" "$2"
}

fetch alerts/openldap.rules.yml    conf/prometheus/rules/openldap.rules.yml
fetch dashboards/openldap.json     conf/grafana/dashboards/openldap.json

echo "alerts:     $(grep -c '^\s*- alert:' conf/prometheus/rules/openldap.rules.yml)"
echo "dashboard:  $(python3 -c "import json;d=json.load(open('conf/grafana/dashboards/openldap.json'));print(d['title'], '-', len(d['panels']), 'panels')")"
