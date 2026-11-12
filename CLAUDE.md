# Repository guidance

This is a local Docker Compose stack, not a verified production deployment.
Read README.md and workflows/MCP_SETUP_GUIDE.md before changes.

- Preserve existing Compose project names, volume keys, credentials and database names.
- Never run `docker compose down -v`, reset volumes, or upgrade PostgreSQL's
  major version as routine maintenance.
- Deployment, restarts, credential imports and workflow activation require separate authorization.
- n8n uses account-based login; N8N_BASIC_AUTH_* is obsolete.
- ImageMagick is built into n8n, but Execute Command is disabled by default.
- Shared image path is /web_images; host path is WEB_IMAGES_HOST_DIR.
- MCP servers use `docker compose run --rm --no-deps -T`, not docker exec.
- Legacy webhook JSON files are demonstrations, not complete MCP transports.
- Never commit tokens, .env files, sensitive logs or database dumps.
- Validate with `python scripts/validate_stack.py`, shell syntax checking and
  `docker compose --env-file .env.example --profile mcp config --quiet`.
- Image builds and smoke tests must pass before claiming runtime compatibility.
- Distributor-specific batching/rate-limit claims are not established by this repository.
