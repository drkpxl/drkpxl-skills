# Tiny Air — air quality skill for AI agents

[Tiny Air](https://tinyair.drkpxl.com) is a hosted MCP server that gives your AI agent
real-time US air quality data. Ask about AQI, smoke, or set up proactive alerts when
conditions worsen — all via a single hosted endpoint, no API key required.

**Hosted MCP endpoint:** `https://air.drkpxl.com/mcp` (Streamable HTTP, stateless)

---

## What Tiny Air does

Tiny Air exposes four tools over a hosted MCP server:

| Tool | What it does |
|---|---|
| `get_air_quality` | Current AQI for a US zip, city, or lat/lon |
| `check_air_quality_threshold` | Returns `exceeded: true/false` against a `max_aqi` or `min_category` |
| `find_nearby_stations` | Monitoring stations near a location |
| `list_aqi_categories` | The Good → Hazardous AQI band definitions |

Coverage is **US-only** (data source: [AirNow.gov](https://www.airnow.gov/); US geocoding).

---

## Install by agent

| Agent | Config file | What it does |
|---|---|---|
| Claude Code | [configs/claude-code.md](configs/claude-code.md) | `claude mcp add` command + Skill install |
| Hermes | [configs/hermes.yaml](configs/hermes.yaml) | `config.yaml` snippet (hosted, no local process) |
| OpenClaw | [configs/openclaw.json](configs/openclaw.json) | `~/.openclaw/openclaw.json` snippet |
| Claude Desktop / Cursor | [configs/claude-desktop.json](configs/claude-desktop.json) | `claude_desktop_config.json` via `mcp-remote` |
| Any HTTP MCP client | [configs/generic.md](configs/generic.md) | POST to `https://air.drkpxl.com/mcp` |

---

## Install the Agent Skill (Claude Code)

The `SKILL.md` in this directory teaches Claude Code how to answer air-quality questions
and own the proactive-alert loop without extra prompting.

```bash
git clone https://github.com/drkpxl/drkpxl-skills.git
cp -r drkpxl-skills/skills/tiny-air ~/.claude/skills/tiny-air
```

The MCP server must also be added:

```bash
claude mcp add --transport http tinyair https://air.drkpxl.com/mcp
```

Installing the folder (`SKILL.md` + `configs/` + `recipes/`) is sufficient — Claude Code
picks up everything it needs from that tree.

---

## Proactive alerts

Tiny Air is stateless — your agent owns alerting. See
[recipes/proactive-alerts.md](recipes/proactive-alerts.md) for two canonical recipes
(numeric-threshold with suppression, and daily category-threshold check) plus
per-agent scheduling notes for Hermes, OpenClaw, and Claude Code / Desktop.

---

## Coverage and attribution

- **US-only.** Air quality data is sourced from [AirNow.gov](https://www.airnow.gov/),
  the US EPA's official real-time air quality reporting network. Geocoding is US-only.
- **Powered by Tiny Air** — see [tinyair.drkpxl.com](https://tinyair.drkpxl.com) for
  the web app, source attribution, and documentation.

---

[tinyair.drkpxl.com](https://tinyair.drkpxl.com) · [github.com/drkpxl/drkpxl-skills](https://github.com/drkpxl/drkpxl-skills)
