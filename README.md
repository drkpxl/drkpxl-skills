# drkpxl-skills

Installable skills for AI agents, by drkpxl. Each skill is a self-contained directory
under `skills/` that you can clone and drop into your agent's skill folder — no build
step, no API keys (unless noted), no backend to run.

---

## Available skills

| Skill | Path | Description |
|---|---|---|
| **Bro** | [`skills/bro/`](skills/bro/) | Restates the agent's last message in plain human language, with no jargon. Manual invocation only — you decide when an answer needed translating. |
| **Copywriting** | [`skills/copywriting/`](skills/copywriting/) | Conversion copywriting for website pages (homepage, landing, pricing, feature, about). Finds where the copy lives and edits it in place — no copy dumped into chat. |
| **Prototype** | [`skills/prototype/`](skills/prototype/) | Throwaway code that answers one design question: a single shareable HTML file for state/logic, or several toggleable UI variants on one route. Forked from [mattpocock/skills](https://github.com/mattpocock/skills). |
| **Research** | [`skills/research/`](skills/research/) | Delegates a question to a background agent that reads primary sources and leaves cited findings in a Markdown file. Forked from [mattpocock/skills](https://github.com/mattpocock/skills). |
| **Tiny Air** | [`skills/tiny-air/`](skills/tiny-air/) | Real-time US air quality (AQI) via a hosted MCP server. Ask about smoke, set proactive alerts, or query by ZIP / city / coordinates. |

---

## Repo conventions

Each skill lives in `skills/<name>/` and contains:

| File / folder | Purpose |
|---|---|
| `SKILL.md` | The skill definition loaded by the agent (e.g., Claude Code's `~/.claude/skills/`) — **required** |
| `README.md` | Install instructions and usage details |
| `references/` | Heavy reference material the `SKILL.md` links to on demand (optional) |
| `agents/openai.yaml` | Codex sidecar, read from beside `SKILL.md` — UI metadata plus invocation policy (see below) |
| `configs/` | Per-agent **MCP server** config snippets, one file per agent type (optional — for MCP/server skills) |
| `recipes/` | Canonical prompt recipes and scheduling patterns (optional) |

Only `SKILL.md` is required. Pure-prompt skills (like Copywriting) ship just `SKILL.md`,
an optional `README.md`, and any `references/`; MCP/server skills (like Tiny Air) add
`configs/` and `recipes/`. `agents/` and `configs/` are different things and both must keep
their names: `agents/openai.yaml` is a spec'd sidecar Codex looks for next to `SKILL.md`,
while `configs/` is just documentation this repo writes for humans wiring up MCP servers.

### Frontmatter is kept spec-legal

Every `SKILL.md` here sticks to the six fields the [Agent Skills](https://agentskills.io)
spec allows — `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`
— so the same files load in Claude Code, Codex, pi, Hermes, and claude.ai uploads unchanged.
Anything agent-specific goes under `metadata:` (e.g. `metadata.hermes.category`, which Hermes
uses for grouping). The one deliberate exception is `disable-model-invocation: true` on
**Bro** — honored by Claude Code and pi, and mirrored for Codex by
`policy.allow_implicit_invocation: false` in its `agents/openai.yaml`, since Codex ignores
the frontmatter field. It does mean Bro can't be uploaded to claude.ai as-is, which is fine:
it's a terminal skill.

## Install in Claude Code

This repo is a Claude Code plugin marketplace — each skill installs as its own plugin:

```
/plugin marketplace add drkpxl/drkpxl-skills
/plugin install bro@drkpxl-skills
/plugin install copywriting@drkpxl-skills
/plugin install prototype@drkpxl-skills
/plugin install research@drkpxl-skills
/plugin install tiny-air@drkpxl-skills
```

Or manually, by copying a skill into your personal skills folder:

```bash
git clone https://github.com/drkpxl/drkpxl-skills.git
cp -r drkpxl-skills/skills/<name> ~/.claude/skills/<name>
```

## Install on other agents

These skills are plain [Agent Skills](https://agentskills.io) directories, so anything that
reads `SKILL.md` can run them. The easiest route is the `skills` CLI, which picks the right
directory per agent:

```bash
npx skills@latest add drkpxl/drkpxl-skills -a codex,pi,hermes-agent
```

Add `-g` for a global (user-level) install, `--all` to take every skill without prompts, and
`--copy` to copy files instead of symlinking. Or copy the folders yourself:

| Agent | Global | Per-project |
|---|---|---|
| Claude Code | `~/.claude/skills/<name>/` | `.claude/skills/<name>/` |
| Codex | `~/.codex/skills/<name>/` (`$CODEX_HOME/skills`) | `.agents/skills/<name>/` |
| pi | `~/.pi/agent/skills/<name>/` | `.pi/skills/<name>/` |
| Hermes | `~/.hermes/skills/<name>/` (`$HERMES_HOME/skills`) | `.hermes/skills/<name>/` |

Copy the whole skill directory, not just `SKILL.md` — the `references/` and `agents/` files
have to travel with it.

Notes per agent:

- **Codex** — invoke with `$skill-name`. It reads `agents/openai.yaml` from beside `SKILL.md`
  for the picker label and, for Bro, to keep the model from auto-invoking.
- **pi** — invoke with `/skill:<name>`. It also honors `disable-model-invocation`. `~/.agents/skills/`
  and `.agents/skills/` work too, so a Codex project install is picked up by pi as well.
- **Hermes** — skills live under `~/.hermes/skills/`; extra directories can be listed in
  `config.yaml` under `skills.external_dirs`. Tiny Air additionally needs its MCP server wired
  up — see [`skills/tiny-air/configs/hermes.yaml`](skills/tiny-air/configs/hermes.yaml).

See each skill's `README.md` for usage details and MCP server setup.

---

[github.com/drkpxl/drkpxl-skills](https://github.com/drkpxl/drkpxl-skills)
