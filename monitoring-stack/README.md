# monitoring-stack

Prometheus + Grafana, plus the exporters and datasources that feed them. Cross-product
infrastructure — OpenLDAP is one thing it can monitor, not the reason it exists.

| | |
|---|---|
| Prometheus | `:9090` |
| Grafana | `:3000` (admin / admin) |

## Layout

```
docker-compose.yml              Prometheus + Grafana; CREATES the `monitoring` network
conf/prometheus/prometheus.yml  scrape jobs; rule_files = conf/prometheus/rules/*.yml
conf/prometheus/rules/          fetched, not committed (see fetch-rules.sh)
conf/grafana/provisioning/      datasource + dashboard providers
exporters/<tool>/               one stack per exporter, attaches to `monitoring`
datasources/<tool>/             the database each exporter points at
fetch-rules.sh                  pulls the OpenLDAP alert rules from the exporter repo
```

## Start

The root stack creates the `monitoring` network, so it goes first — every
`exporters/*` and `datasources/*` compose attaches to it as `external`.

```bash
./fetch-artifacts.sh             # rules + dashboard, never copied
docker compose up -d             # prometheus + grafana

cd exporters/openldap
cp .env.vibhuvioio.example .env.vibhuvioio
docker compose up -d             # openldap + openldap-exporter
```

## Testing the openldap-exporter

`exporters/openldap/` brings up the thing under test and the exporter that reads it.
Prometheus and Grafana are **not** here — the exporter repo ships no Prometheus
runtime, and should not; only the published image is consumed.

```bash
docker compose -f exporters/openldap/docker-compose.yml up -d
open http://localhost:9330/metrics           # the exporter directly
open http://localhost:9090/targets           # job "openldap" must be up
open http://localhost:9090/alerts
```

Prometheus scrapes `openldap-exporter:9330` once; the exporter fans out to every
target in `openldap-exporter.yml` itself, so adding an OpenLDAP server is a change
to that file, not to `prometheus.yml`.

The config database bind DN is `cn=config` in this image, **not**
`cn=admin,cn=config` — the wrong DN silently costs you the syncrepl topology,
serverID and keepalive metrics. `openldap_config_readable` must be `1`.

## Rules and dashboards

Both `conf/prometheus/rules/openldap.rules.yml` and
`conf/grafana/dashboards/openldap.json` are **fetched** from
[openldap-exporter](https://github.com/VibhuviOiO/openldap-exporter) by
`fetch-artifacts.sh` and gitignored. Never copy them in by hand — edit the
exporter repo and re-run the script.

```bash
./fetch-artifacts.sh
docker compose restart prometheus grafana     # prometheus reloads rules, grafana re-scans
```

The rule file used to be `alert.yml`, which did not exist anywhere. Prometheus
v2.33 starts anyway and loads **zero** rules — `/api/v1/rules` returns
`{"groups":[]}` — so the stack looked healthy while alerting nothing. The Grafana
dashboard provider likewise pointed at the provisioning directory, which holds
only its own config, so no dashboard was ever provisioned.

## Local test: exporter dashboard end to end

```bash
./fetch-artifacts.sh                      # rules + dashboard
docker compose up -d                      # prometheus + grafana
cd exporters/openldap
cp .env.vibhuvioio.example .env.vibhuvioio
docker compose up -d                      # openldap (cn=Monitor on) + exporter
```

Then check, in order — each step isolates one link:

```bash
curl -s localhost:9330/metrics | head            # 1. exporter answers
curl -s localhost:9090/api/v1/targets \
  | python3 -c 'import json,sys;[print(t["labels"]["job"],t["health"]) for t in json.load(sys.stdin)["data"]["activeTargets"] if t["labels"]["job"]=="openldap"]'
                                                  # 2. expect: openldap up
curl -s localhost:9090/api/v1/rules | python3 -c 'import json,sys;print(len(json.load(sys.stdin)["data"]["groups"]),"rule groups")'
                                                  # 3. expect: 4 rule groups
open http://localhost:3000                        # 4. Dashboards -> OpenLDAP
```

**Step 4 is the one that needs the datasource name.** The dashboard's `datasource`
template variable defaults to the provisioned Prometheus datasource; if the panel
says "No data", set that variable to `Prometheus` in the dashboard header first.

Two things silently produce an empty dashboard:

- `openldap_config_readable` is `0` — the `cn=config` bind DN is wrong.
- `ENABLE_MONITORING` is not `true` on the OpenLDAP service — there is no
  `cn=Monitor`, so most panels have nothing to show.

## Known state

- `exporters/{blackbox,cadvisor,mysql}` and `datasources/*` are **not** running in
  the base stack; their targets show `down` in `/targets` until you start them.
- `GF_INSTALL_PLUGINS=grafana-piechart-panel` and Grafana 8.4.1 are pinned old. The
  piechart plugin is deprecated upstream.
