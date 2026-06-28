# drkpxl-skills

Installable skills for AI agents, by drkpxl. Each skill is a self-contained directory
under `skills/` that you can clone and drop into your agent's skill folder — no build
step, no API keys (unless noted), no backend to run.

---

## Available skills

| Skill | Path | Description |
|---|---|---|
| **Copywriting** | [`skills/copywriting/`](skills/copywriting/) | Conversion copywriting for website pages (homepage, landing, pricing, feature, about). Finds where the copy lives and edits it in place — no copy dumped into chat. |
| **Tiny Air** | [`skills/tiny-air/`](skills/tiny-air/) | Real-time US air quality (AQI) via a hosted MCP server. Ask about smoke, set proactive alerts, or query by ZIP / city / coordinates. |

---

## Repo conventions

Each skill lives in `skills/<name>/` and contains:

| File / folder | Purpose |
|---|---|
| `SKILL.md` | The skill definition loaded by the agent (e.g., Claude Code's `~/.claude/skills/`) — **required** |
| `README.md` | Install instructions and usage details |
| `references/` | Heavy reference material the `SKILL.md` links to on demand (optional) |
| `configs/` | Per-agent config snippets, one file per agent type (optional — for MCP/server skills) |
| `recipes/` | Canonical prompt recipes and scheduling patterns (optional) |

Only `SKILL.md` is required. Pure-prompt skills (like Copywriting) ship just `SKILL.md`,
an optional `README.md`, and any `references/`; MCP/server skills (like Tiny Air) add
`configs/` and `recipes/`.

To install a skill into Claude Code:

```bash
git clone https://github.com/drkpxl/drkpxl-skills.git
cp -r drkpxl-skills/skills/<name> ~/.claude/skills/<name>
```

See each skill's `README.md` for agent-specific instructions and MCP server setup.

---

[github.com/drkpxl/drkpxl-skills](https://github.com/drkpxl/drkpxl-skills)
