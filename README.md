# drkpxl-skills

Installable skills for AI agents, by drkpxl. Each skill is a self-contained directory
under `skills/` that you can clone and drop into your agent's skill folder — no build
step, no API keys (unless noted), no backend to run.

---

## Available skills

| Skill | Path | Description |
|---|---|---|
| **Tiny Air** | [`skills/tiny-air/`](skills/tiny-air/) | Real-time US air quality (AQI) via a hosted MCP server. Ask about smoke, set proactive alerts, or query by ZIP / city / coordinates. |

---

## Repo conventions

Each skill lives in `skills/<name>/` and contains:

| File / folder | Purpose |
|---|---|
| `SKILL.md` | The skill definition loaded by the agent (e.g., Claude Code's `~/.claude/skills/`) |
| `README.md` | Install instructions, per-agent config table, usage details |
| `configs/` | Per-agent config snippets (one file per agent type) |
| `recipes/` | Canonical prompt recipes and scheduling patterns |

To install a skill into Claude Code:

```bash
git clone https://github.com/drkpxl/drkpxl-skills.git
cp -r drkpxl-skills/skills/<name> ~/.claude/skills/<name>
```

See each skill's `README.md` for agent-specific instructions and MCP server setup.

---

[github.com/drkpxl/drkpxl-skills](https://github.com/drkpxl/drkpxl-skills)
