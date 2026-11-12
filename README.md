# Jeffvato Ultimate n8n Stack

Local Docker Compose automation, AI and database services for Linux/WSL2.
Reviewed against upstream releases on **2026-11-12**. This repository is a
configuration template, not a claim of production readiness or a completed upgrade
of your running machine.

## License and commercial hosting

The original configuration, scripts and documentation in this repository are
licensed under [MIT](LICENSE). They may be modified, redistributed and sold,
provided the MIT copyright and permission notice is retained. This grant does
not relicense third-party applications, container images, dependencies or models.

The author is sharing this configuration freely for community use and exposure,
not selling or operating a hosted n8n service. MIT permits recipients to use the
original material commercially, but does not guarantee prominent public credit,
a backlink, payment or endorsement. A voluntary repository link is appreciated.
Recipients operating a hosted/resold service remain responsible for upstream rights.

**Selling access to a hosted n8n service is not authorized by this repository's
MIT license.** n8n's current guidance requires a separate commercial license for
hosting n8n as a service, white-labeling, or allowing customers to build/configure
workflows, including through an API, MCP or AI agent. Some operator-managed
workflow services have different treatment; obtain written confirmation from n8n
for your exact offering before selling it.

See [commercial handoff requirements](COMMERCIAL_USE.md) for upstream license
links and deployment gates. No claim of commercial licensing clearance,
multi-tenant isolation or production-service readiness is made here.

## Revision baseline

| Service | Image/revision | Upgrade policy |
| --- | --- | --- |
| n8n custom ImageMagick build | 2.47.5 stable | Exact version; not 2.48 beta |
| PostgreSQL | 16-alpine | Latest available 16.x patch; preserve existing major/data layout |
| Redis Stack | 7.4.0-v8 | Preserve Stack/module compatibility; no silent Redis 8 migration |
| pgAdmin | 9.19 | Exact release |
| Qdrant | v1.20.0 | Exact release; read intermediate-version migration guidance |
| Ollama (CPU) | 0.40.16 | Exact release; models downloaded separately |
| Open WebUI | v0.13.3 | Exact release; backup data before migrations |
| n8n MCP | 2.102.0 | Optional stdio client process |
| Playwright MCP | 0.0.85 | Microsoft's image; optional stdio client process |
| PostgreSQL MCP | 0.3.0 | Restricted mode, optional stdio client process |
| SearXNG / utility ImageMagick | 2026-11-12 image digests | Rolling upstream tags frozen to verified registry digests |

Sources: [n8n releases](https://github.com/n8n-io/n8n/releases),
[Redis Stack releases](https://github.com/redis-stack/redis-stack/releases),
[pgAdmin 9.19](https://www.pgadmin.org/docs/pgadmin4/latest/release_notes_9_19.html),
[Qdrant releases](https://github.com/qdrant/qdrant/releases),
[Ollama releases](https://github.com/ollama/ollama/releases),
[Open WebUI releases](https://github.com/open-webui/open-webui/releases),
[n8n MCP releases](https://github.com/czlonkowski/n8n-mcp/releases),
[Playwright MCP releases](https://github.com/microsoft/playwright-mcp/releases),
[PostgreSQL MCP releases](https://github.com/crystaldba/postgres-mcp/releases).

Tags are not content-addressed guarantees. Record deployed image digests before
updates. Do not assume every upstream release is mutually compatible without
testing your workflows. Redis Stack is retained for compatibility, not claimed
to be the latest Redis product; RedisGraph is not included.

## Important changes for existing installations

- The old README advertised n8n 1.123.5 while its Dockerfile used 2.0.3.
  This baseline aligns both to 2.47.5. Review the
  [n8n 2.x breaking changes](https://docs.n8n.io/2-0-breaking-changes/)
  and [release notes](https://docs.n8n.io/release-notes/) before upgrading.
- n8n account-based login replaces the removed N8N_BASIC_AUTH_* configuration.
  Existing account data remains in the database; create an owner account only
  on a genuinely new installation.
- Execute Command and Local File Trigger remain disabled by default. If audited
  workflows need ImageMagick via Execute Command, set
  `NODES_EXCLUDE='["n8n-nodes-base.localFileTrigger"]'` in .env.
  This grants shell execution to workflows; only trusted editors should have access.
- File nodes are restricted to /web_images. Add other directories only deliberately.
  Environment access is blocked by default; audit Code nodes/expressions before
  retaining the older `N8N_BLOCK_ENV_ACCESS_IN_NODE=false` setting.
- Internal JavaScript task runners are enabled for this local stack. This is not
  the production-recommended isolated external-runner deployment. Python Code
  workflows require a separately configured matching external runner and tests;
  no insecure runner mode is enabled here.
- Ports bind to 127.0.0.1 by default. Remote LAN/Tailscale/reverse-proxy access
  will need deliberate bind, firewall, TLS and URL configuration. Do not set
  BIND_ADDRESS=0.0.0.0 casually: it exposes unauthenticated backing services too.
- MCP servers are on-demand tools, not always-running daemons. Old docker-exec
  instructions launched a second stdio process and depended on internal paths.
- A bearer token was previously committed in the setup script. **Revoke/rotate
  it if used.** Removal does not remove public Git history. No automatic
  credential import or database modification is performed by the script now.
- Legacy webhook workflows are demonstrations with placeholder tools, not
  complete MCP servers. See [MCP guide](workflows/MCP_SETUP_GUIDE.md).
- The repository now has an actual MIT LICENSE for its original material.
  Third-party licenses remain separate; see COMMERCIAL_USE.md before resale.

## Fresh setup

Use a maintained Docker Engine/Desktop and Compose v2 with BuildKit. The whole
AI stack can require substantial RAM and disk; 16 GB RAM is a starting point,
not a guarantee. Ollama model sizes and import workload determine actual needs.

```bash
git clone https://github.com/jeffvato/jeffvato-ultimate-n8n-stack.git
cd jeffvato-ultimate-n8n-stack
cp .env.example .env
chmod 600 .env
```

Edit .env: set unique PostgreSQL/pgAdmin passwords, a valid pgAdmin email and a
random SEARXNG_SECRET (`openssl rand -hex 32`). WEB_IMAGES_HOST_DIR defaults to
/mnt/e/web_images (E:\\web_images under WSL); create your chosen directory first.
Do not copy example passwords to a real system.

N8N_SECURE_COOKIE=false is for local HTTP only. Remote deployment needs HTTPS,
secure cookies, correct WEBHOOK_URL/N8N_EDITOR_BASE_URL and proxy configuration.
No reverse proxy/TLS or safe public-access deployment is supplied here.

```bash
docker compose --env-file .env config --quiet
docker compose build --pull n8n
docker compose pull --ignore-buildable
docker compose up -d
docker compose ps
docker compose logs --tail=100 n8n
```

Build smoke test (does not start your stack):

```bash
docker compose run --rm --no-deps --entrypoint /bin/sh n8n -ec \
  'n8n --version; magick -size 1x1 xc:white /tmp/check.webp; magick identify /tmp/check.webp'
```

The Dockerfile temporarily restores the matching Alpine package manager to
install ImageMagick/WebP support, then removes it. Its Alpine-version guard must
be reviewed when the n8n base changes.

## Upgrading an existing stack safely

1. Work in the **existing checkout and Compose project**. Before pulling changes,
   record `docker compose ls`, `docker compose config --volumes`,
   `docker compose images`, your current Git SHA and existing .env. Changing
   directories/project names can silently select new empty volumes. Keep the
   same `-p` / COMPOSE_PROJECT_NAME selection if one is already used.
2. Inspect the live n8n version and image IDs. Preserve/tag the old custom image.
   Preserve the exact old Compose/.env and images for all services being updated.
3. Back up before any application/database migration. Stop workflow execution
   and n8n for a consistent checkpoint. Back up PostgreSQL, **n8n-data including
   its encryption key**, and each other stateful service using its supported
   snapshot/backup method. PostgreSQL alone is not a full-stack backup.
4. Test restoring the backup into an isolated project. Never run the original
   and restored production schedules/webhooks against the same external systems.
5. Merge configuration manually; do **not** overwrite your existing .env with the
   example. Keep database names/passwords, encryption key, volume keys and image
   paths. Set N8N_VERSION and N8N_IMAGE_NAME together, or old .env values can
   override the new build/tag. Do not set a new encryption key on existing data.
6. Review all intermediate migrations, especially n8n, Qdrant and Open WebUI.
   Build/pull first and test representative workflows, credentials, webhooks,
   files, Code nodes and ImageMagick against restored data. Stage upgrades
   individually rather than assuming all services can be upgraded at once.
7. Only after acceptance, recreate the chosen services during a maintenance
   window. `docker compose restart` does not apply changed environment/images.
   No service restart is performed by this repository update.

Example PostgreSQL backup after n8n is stopped (run from the existing project;
output contains sensitive business data and must be protected):

```bash
mkdir -p backups
chmod 700 backups
docker compose stop n8n
docker compose exec -T postgres sh -ec \
  'pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Fc' > backups/postgres.dump
docker compose exec -T postgres sh -ec \
  'pg_restore --list' < backups/postgres.dump > /dev/null
```

This dump check is not a restore test. Also protect PostgreSQL roles/global
objects and other databases where applicable. Copy n8n's persistent volume
using your backup tool while n8n is stopped; preserve its ownership/permissions.
Do not print .env or decrypted credentials in logs.

**Rollback:** stop the new writers, restore the pre-upgrade database and service
volumes into the original project, and use the recorded old configuration and
images. Merely downgrading a container against migrated data is not safe.
Never use `docker compose down -v` or volume pruning as an upgrade step.
PostgreSQL stays on 16; a major upgrade requires its own dump/restore or pg_upgrade
plan and cannot reuse the old data directory blindly.

## Services and access

| Service | Local endpoint | Login / notes |
| --- | --- | --- |
| n8n | http://localhost:5678 | Existing account or first-run owner setup |
| pgAdmin | http://localhost:5050 | PGADMIN_DEFAULT_* initializes a new data volume only |
| Open WebUI | http://localhost:3000 | Account setup; existing admin settings can override env defaults |
| SearXNG | http://localhost:8080 | Local only; JSON format enabled for WebUI |
| PostgreSQL | localhost:5432 | Existing POSTGRES_* identity |
| Redis Stack | localhost:6379 | No auth configured; local-only exposure |
| Qdrant | http://localhost:6333 | No API key configured; local-only exposure |
| Ollama | http://localhost:11434 | CPU inference; no API authentication configured |

Services communicate by Docker service name, not localhost: postgres:5432,
ollama:11434, qdrant:6333, searxng:8080. Named volume keys are unchanged.
The shared image folder remains /web_images in n8n/PostgreSQL/Ollama and /work
in the utility container. Restrict mounts further if those services do not need them.

```bash
docker compose exec ollama ollama pull llama3.2
docker compose exec ollama ollama list
docker compose exec imagemagick magick input.jpg -resize 800x600 output.webp
```

WebUI uses ENABLE_WEB_SEARCH/WEB_SEARCH_* and SEARXNG_QUERY_URL. Existing WebUI
persistent settings may override them: verify Admin Settings → Web Search.
This is a single-process n8n stack, not queue mode; Redis presence alone does not
activate n8n queue execution.

## Optional MCP integration

See [workflows/MCP_SETUP_GUIDE.md](workflows/MCP_SETUP_GUIDE.md). MCP services
are excluded from ordinary `up -d` through a profile. Clients create one
temporary stdio process per connection with Compose run, no TTY and no restart
loop. PostgreSQL restricted mode is not a substitute for a least-privilege role.
An n8n API key can authorize workflow mutation; approve tool use accordingly.

## Validation and troubleshooting

```bash
python scripts/validate_stack.py  # requires PyYAML
bash -n setup-mcp-workflows.sh
docker compose --env-file .env.example --profile mcp config --quiet
docker compose ps
docker compose logs --tail=100 n8n postgres searxng
```

CI validates configuration, builds the n8n image and smoke-tests version/WebP.
These checks do not prove your persisted workflow/database migrations or full
service integration. No production-ready claim follows from a successful build.

For import memory issues, start with bounded batches and monitor actual usage.
NODE_OPTIONS caps the Node heap, not total container/stack memory. Four GB for
n8n plus Ollama, WebUI and databases needs additional host headroom.

Support: [repository issues](https://github.com/jeffvato/jeffvato-ultimate-n8n-stack/issues),
[n8n docs](https://docs.n8n.io/), [SearXNG docs](https://docs.searxng.org/),
[Open WebUI docs](https://docs.openwebui.com/).
