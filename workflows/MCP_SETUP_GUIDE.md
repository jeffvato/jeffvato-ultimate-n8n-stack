# MCP setup (reviewed 2026-11-12)

Servers are optional and start per client connection. Start the base stack first.
Run commands from the existing repository directory:

```bash
docker compose --profile mcp pull n8n-docs-mcp playwright-mcp postgres-mcp
docker compose run --rm --no-deps -T n8n-docs-mcp
```

Use the MCP client's documented configuration location; merge this example rather
than overwriting the client's configuration. Replace the directory with your
absolute checkout path:

```json
{
  "mcpServers": {
    "n8n-docs": {
      "command": "docker",
      "args": ["compose", "--project-directory", "/absolute/path/to/stack", "run", "--rm", "--no-deps", "-T", "n8n-docs-mcp"]
    },
    "playwright": {
      "command": "docker",
      "args": ["compose", "--project-directory", "/absolute/path/to/stack", "run", "--rm", "--no-deps", "-T", "playwright-mcp"]
    },
    "postgres": {
      "command": "docker",
      "args": ["compose", "--project-directory", "/absolute/path/to/stack", "run", "--rm", "--no-deps", "-T", "postgres-mcp"]
    }
  }
}
```

The client must use the same Docker context, checkout, .env and Compose project
identity as the stack. If you use `-p`, include the same project selection above.
`--no-deps` intentionally avoids starting/recreating dependencies.

## Credentials and privileges

- Documentation tools work without N8N_API_KEY. Workflow-management tools require
  a current key from n8n Settings → n8n API (labels may vary). Keep it only in .env.
  New stdio connections read the updated value; restarting old containers is not enough.
- n8n keys can permit workflow writes/execution. Review tool calls before use.
- PostgreSQL MCP uses restricted mode, but currently receives POSTGRES_USER.
  This does not replace a dedicated least-privilege role. Do not give it to
  untrusted clients or treat restricted mode as a security isolation boundary.
- The MCP DATABASE_URI requires URI-percent-encoding for reserved characters in
  database passwords. Configure an encoded URI override for MCP if needed; do not
  change an existing database password just to match this example.
- Playwright is browser automation, not an isolation boundary. Do not expose
  sensitive internal services to untrusted browsing.

## Legacy files

`claude-mcp-http.json` and `claude-mcp-webhook.json` are old JSON-RPC webhook
demonstrations with placeholder tools, not complete MCP transport/session handling.
They are not required by these servers. Do not activate them as working MCP
integration. Inspect them in a disposable instance only; create fresh header-auth
credentials in the UI. Never reuse a public API token from Git history.

The setup script now prints a notice only. It does not query the database, import
credentials, activate workflows or make network calls. Revoke any token previously
copied from it; removal does not erase public Git history.

Upstream: [n8n MCP](https://github.com/czlonkowski/n8n-mcp),
[Playwright MCP](https://github.com/microsoft/playwright-mcp),
[Postgres MCP](https://github.com/crystaldba/postgres-mcp).
