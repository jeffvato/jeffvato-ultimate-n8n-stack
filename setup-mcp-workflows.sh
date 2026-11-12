#!/usr/bin/env bash
# Read-only notice: no credential imports, database access or workflow activation.
set -euo pipefail
printf '%s\n' \
  'Bundled webhook workflows are legacy demonstrations, not MCP servers.' \
  'Use workflows/MCP_SETUP_GUIDE.md for current on-demand stdio MCP setup.' \
  'Revoke/rotate any token copied from older revisions of this script.'
