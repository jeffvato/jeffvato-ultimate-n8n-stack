"""Offline contract checks. Does not start services or load real credentials."""
import json
import pathlib
import re
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
compose_text = (ROOT / "docker-compose.yml").read_text()
compose = yaml.safe_load(compose_text)
services = compose["services"]
env = {}
for line in (ROOT / ".env.example").read_text().splitlines():
    if line and not line.startswith("#"):
        key, value = line.split("=", 1)
        env[key] = value.strip("'")

assert len(services) == 12
assert set(compose["volumes"]) == {
    "pgdata", "pgadmin-data", "redis-data", "n8n-data",
    "qdrant_storage", "ollama", "openwebui-data",
}
for service in services.values():
    for port in service.get("ports", []):
        assert port.startswith("${BIND_ADDRESS:-127.0.0.1}:")
    for dependency in service.get("depends_on", []):
        assert dependency in services
    for volume in service.get("volumes", []):
        if volume.startswith("./"):
            assert (ROOT / volume.split(":")[0]).exists(), volume

# Every interpolated variable must have a default or an example value.
for match in re.finditer(r"\$\{([A-Z_][A-Z_0-9]*)([^}]*)\}", compose_text):
    assert match[1] in env or match[2].startswith(":-"), match[1]
assert env["N8N_VERSION"] == "2.47.5"
assert env["N8N_VERSION"] in env["N8N_IMAGE_NAME"]
assert f'ARG N8N_VERSION={env["N8N_VERSION"]}' in (ROOT / "n8n.Dockerfile").read_text()
assert "n8n-nodes-base.executeCommand" in json.loads(env["NODES_EXCLUDE"])
assert "N8N_BASIC_AUTH_" not in services["n8n"]["environment"]
assert not any(k.startswith("N8N_BASIC_AUTH_") for k in services["n8n"]["environment"])
assert services["n8n"]["environment"]["N8N_RUNNERS_MODE"] == "internal"
assert services["postgres"]["image"].startswith("postgres:16")
assert services["openwebui"]["environment"]["ENABLE_WEB_SEARCH"] == "true"
assert "json" in yaml.safe_load((ROOT / "searxng/settings.yml").read_text())["search"]["formats"]
for name in ("n8n-docs-mcp", "playwright-mcp", "postgres-mcp"):
    assert services[name]["profiles"] == ["mcp"]
    assert services[name]["restart"] == "no"
    assert services[name]["stdin_open"] and not services[name]["tty"]
assert services["n8n-docs-mcp"]["environment"]["MCP_MODE"] == "stdio"
assert services["postgres-mcp"]["command"] == ["--access-mode=restricted"]
for path in (ROOT / "workflows").glob("*.json"):
    json.loads(path.read_text())
for path in ROOT.rglob("*"):
    if ".git" in path.parts or not path.is_file():
        continue
    if path.suffix in (".md", ".sh", ".json", ".yml", ".example"):
        text = path.read_text()
        assert not re.search(r"eyJ[A-Za-z0-9_-]{12,}\.[A-Za-z0-9_-]{12,}\.[A-Za-z0-9_-]{12,}", text), path
        assert "your-username" not in text, path
print("PASS: 12 services, persistent volume keys, local bindings, env coverage, MCP lifecycle, versions, JSON and secret-regression checks")
