# mcp_integration.py
# ===================
# SINGLE TOPIC: MCP server integration (scoping, auth, resources, build-vs-use)
#
# What you learn:
#   - The MCP three-layer model: Host ⊃ Client ↔ Server
#   - Project-level .mcp.json (shared) vs user-level ~/.claude.json (personal)
#   - ${VAR} / ${VAR:-default} expansion keeps secrets out of version control
#   - MCP resources expose catalogues upfront, saving exploratory tool calls
#   - Community servers first; build custom only for team-specific workflows
#   - Sparse MCP tool descriptions lose to built-in tools — enhance them
#
# Exam domain covered:
#   Domain 2 — Tool Design & MCP Integration (Subdomain 2.4)
#   Weight: 18% of the CCAR-F exam.
#
# See also: .mcp.json at the repo root (a real project-level config).

# ══════════════════════════════════════════════════════════════════
# CONCEPT 1: Three-layer model
# ══════════════════════════════════════════════════════════════════
#
#   Host ⊃ Client ↔ Server          Protocol: JSON-RPC 2.0
#                                          over stdio or streamable HTTP
#   Host    — the app managing client lifecycle (Claude Desktop, IDE ext.)
#   Client  — one connector per server, created by the host; routes calls
#   Server  — exposes tools, resources, prompts (DB connector, FS server)
#
# Servers NEVER talk to each other directly — all traffic goes via client/host.
# Every configured + reachable server's tools are discovered at connection
# time and available simultaneously. No manual activation step.

# ══════════════════════════════════════════════════════════════════
# CONCEPT 2: Scoping — project-level vs user-level
# ══════════════════════════════════════════════════════════════════
#
# Project-level (.mcp.json at repo root — version-controlled, shared):
PROJECT_CONFIG = {
    "mcpServers": {
        # Remote server: "type": "http" + url. (A url with NO type is a
        # config error — Claude Code reads it as stdio, skips it.)
        "github": {
            "type": "http",
            "url": "https://api.githubcopilot.com/mcp/",
        },
        # Local server: command + args, speaks over stdio.
        "filesystem": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem",
                     "${WORKSPACE_ROOT:-.}"],
        },
    }
}
#
# User-level (~/.claude.json — personal, NOT version-controlled, NOT shared):
#   experimental servers, personal integrations, pre-proposal testing.
#
# EXAM TRAP: team-wide servers in ~/.claude.json never reach teammates.
# New-clone-misses-config ⇒ check whether it lives at user level.

# ══════════════════════════════════════════════════════════════════
# CONCEPT 3: Environment variable expansion (no secrets in git)
# ══════════════════════════════════════════════════════════════════
#
AUTH_CONFIG = {
    "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}",     # each dev sets their own
        "DATABASE_URL": "${DATABASE_URL}",
    }
}
# ${VAR}            → expands to VAR; Claude Code warns (not fails) if unset
# ${VAR:-default}   → falls back to `default` when unset (e.g. paths)
#
# Result: config is safe to commit, rotation needs no config change,
# and no secret ever enters repository history.

# ══════════════════════════════════════════════════════════════════
# CONCEPT 4: MCP resources (catalogues, not calls)
# ══════════════════════════════════════════════════════════════════
#
# Without resources: list_tables → describe_table × N (calls just to orient).
# With a schema resource: the agent knows the layout immediately.
#
# Expose as resources: issue summaries, doc hierarchies, DB schemas.
# Resources are application-controlled: the server lists them, the CLIENT
# decides when to attach one (Claude Code: @server:resource mentions).
#
# One-liner: resources show what data EXISTS; tools let the agent ACT on it.

# ══════════════════════════════════════════════════════════════════
# CONCEPT 5: Build-vs-use decision
# ══════════════════════════════════════════════════════════════════
#
# Standard integration (Jira, GitHub, Slack, Linear, Notion)?
#   → Evaluate COMMUNITY servers first. Always the correct first step.
# Build custom ONLY when: team-specific workflows community servers can't
#   handle, custom business logic in the tool layer, proprietary systems.
#
# EXAM TRAP: "build a custom MCP server for Jira" is wrong unless the
# scenario explicitly describes requirements community servers can't meet.

# ══════════════════════════════════════════════════════════════════
# CONCEPT 6: Enhance MCP tool descriptions
# ══════════════════════════════════════════════════════════════════
#
# Sparse MCP description ("Searches code") loses to rich built-in ones —
# the model defaults to tools it understands best (e.g. Grep).
SPARSE = "search_codebase: 'Searches code'"

ENHANCED = (
    "search_codebase: 'Performs semantic code search across the entire "
    "repository using AST-aware indexing. Returns matching functions, "
    "classes, and methods with file path, line numbers, and surrounding "
    "code. More accurate than text-based grep for finding code by intent "
    "rather than exact string match. Use this instead of Grep when "
    "searching for code by what it does rather than what it contains.'"
)
# 3–5 sentences: WHAT it does, WHAT it returns, WHEN to use it,
# and HOW it compares to the built-in alternative.


# ══════════════════════════════════════════════════════════════════
# KEY TAKEAWAYS
# ══════════════════════════════════════════════════════════════════
#
# 1. Host ⊃ Client ↔ Server; JSON-RPC 2.0 over stdio / streamable HTTP.
# 2. .mcp.json = team-shared (commit it). ~/.claude.json = personal.
# 3. ${VAR} for secrets, ${VAR:-default} for paths with fallbacks.
# 4. Resources = upfront catalogues (server lists, client attaches).
# 5. Community servers first; custom builds only for team-specific needs.
# 6. Rich MCP descriptions, or the agent will prefer built-in tools.
