# Claude Code — Tiny Air setup

## Option A: Add the hosted MCP server

```bash
claude mcp add --transport http tinyair https://air.drkpxl.com/mcp
```

That's it. Claude Code will have access to the four Tiny Air tools
(`get_air_quality`, `check_air_quality_threshold`, `find_nearby_stations`, `list_aqi_categories`)
in every session that project or user scope covers.

## Option B: Install the Agent Skill (recommended for proactive alerts)

The Skill file teaches Claude Code how to answer air-quality questions and own the
alerting loop without extra prompting.

```bash
git clone https://github.com/drkpxl/drkpxl-skills.git
cp -r drkpxl-skills/skills/tiny-air ~/.claude/skills/tiny-air
```

The MCP server must still be added (Option A) — the Skill file adds behavior on top of
the connection, it does not replace it.

## Coverage note

Tiny Air is US-only (data source: AirNow.gov).
