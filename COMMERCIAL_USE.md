# Commercial use and hosting

Reviewed 2026-11-12. This is an operational checklist, not a legal opinion or a
complete software bill of materials. The operator must verify the exact shipped
versions, dependencies, model licenses and commercial agreement for its offering.

## What MIT covers

Jeff Brown has selected MIT for original repository configuration, scripts and
documentation. Include LICENSE with copies or substantial portions. MIT permits
commercial reuse/resale of that material and provides no warranty or support SLA.
It does not transfer third-party copyrights, remove attribution requirements,
grant trademarks, or license container applications/models under MIT.
Separately marked third-party material retains its own terms.

The author's intent is to give this configuration away for exposure, not sell
hosting. There is no extra attribution condition beyond MIT's notice requirement.
A public link/credit is appreciated, not mandatory. MIT does not promise payment,
visible marketing placement or endorsement. Recipients' hosting/resale is their
own business activity, and their upstream-license obligations remain separate.

## n8n is a separate commercial gate

The pinned n8n 2.47.5 release contains the Sustainable Use License and separately
licensed enterprise components. Its current publisher guidance distinguishes:

- Selling access to hosted n8n, white-labeling it, or letting external customers
  build/configure workflows: requires a commercial agreement. Hiding the editor
  behind an API, MCP server or AI agent does not avoid that requirement.
- Operator-built workflows where clients only receive outputs, and installation/
  management on a client's own server: may fit different permitted cases under
  n8n's guidance. These are not blanket authorization for hosted n8n resale.

Before launch, have n8n confirm the actual architecture and sales model in
writing and obtain any required license. Do not assume an ordinary internal-use
Business/Enterprise subscription grants hosting, redistribution or sublicensing
rights; the signed agreement must cover the intended offer.

Sources:
- [Exact n8n 2.47.5 license](https://github.com/n8n-io/n8n/blob/n8n%402.47.5/LICENSE.md)
- [n8n publisher use-case guidance](https://support.n8n.io/article/can-i-use-your-license-for-my-use-case)
- [n8n commercial terms](https://n8n.io/legal/eula/)
- License questions: license@n8n.io; commercial sales: sales@n8n.io.

## Other upstream obligations

Preserve notices and review the exact image contents, not just this short list.
This list is not an attribution bundle or transitive license clearance:

| Component | Authoritative source / required review |
| --- | --- |
| Open WebUI | [License](https://github.com/open-webui/open-webui/blob/v0.13.3/LICENSE), [publisher guidance](https://docs.openwebui.com/license/). Keep original branding unless an explicit exception or commercial agreement applies. |
| Redis Stack | [Stack licenses](https://github.com/redis-stack/redis-stack/blob/master/LICENSE). Review server and module terms for the pinned release and any database-service restrictions. |
| PostgreSQL / pgAdmin | [PostgreSQL license](https://www.postgresql.org/about/licence/), [pgAdmin license](https://www.pgadmin.org/licence/). Preserve notices. |
| Qdrant | [Release license](https://github.com/qdrant/qdrant/blob/v1.20.0/LICENSE). Review dependencies too. |
| Ollama and models | [Runtime license](https://github.com/ollama/ollama/blob/v0.40.16/LICENSE). Each downloaded model has separate terms; runtime permission does not license model weights. |
| SearXNG | [License](https://github.com/searxng/searxng/blob/master/LICENSE). Review AGPL obligations, modifications and network-source requirements, plus search-provider terms. |
| ImageMagick | [License](https://imagemagick.org/script/license.php). Review delegate libraries and utility-container contents. |
| MCP servers | [n8n MCP](https://github.com/czlonkowski/n8n-mcp), [Playwright MCP](https://github.com/microsoft/playwright-mcp), [Postgres MCP](https://github.com/crystaldba/postgres-mcp). Review each pinned release and dependencies; n8n MCP permission does not license n8n itself. |

## Deployment acceptance before customer hosting

The checked-in stack is a local, single-stack baseline, not a finished hosted
multi-tenant service. CI proves configuration, image availability, the n8n build
and a version/WebP smoke test, not customer security or production readiness.

Before accepting customers:

- Obtain applicable commercial rights and assemble exact-version notices/SBOM.
- Revoke/rotate any token previously copied from the public setup script. Never
  reuse the author's .env, accounts, encryption key, workflows, databases or backups.
- Provision fresh per-deployment secrets, owner accounts and encrypted storage.
- Keep backing databases/APIs private. Put only intended application endpoints
  behind TLS, authentication and controlled reverse-proxy access.
- Decide tenant isolation explicitly. Do not use this shared Compose network,
  shared database superuser or restricted MCP mode as a tenant-security boundary.
- Replace local internal task runners with approved isolated external runners;
  restrict workflow editors, shell-capable nodes and credential/tool access.
- Establish least-privilege database roles and customer-data access policies.
- Test persisted-data migrations, representative workflows, credential access,
  webhook delivery, backup restore, rollback and disaster recovery.
- Measure capacity, concurrency, resource limits, monitoring and incident response.
- Establish privacy/data-processing terms, retention, service ownership and support.

This update does not perform those actions or purchase licenses. Do not advertise
the entire stack as MIT-only, unrestricted for hosted resale, security-certified,
or production-ready merely because CI passes.
