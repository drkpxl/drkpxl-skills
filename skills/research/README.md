# Research — primary sources, cited, in a file

A pure-prompt skill that delegates reading legwork to a **background agent** so you keep
working. No API key, no MCP server. Just `SKILL.md` — 13 lines.

Forked from [mattpocock/skills](https://github.com/mattpocock/skills) (`skills/engineering/research`).

---

## What it does

Spins up a background agent that:

1. Investigates the question against **primary sources** — official docs, source code, specs,
   first-party APIs — not a secondary write-up of them, following every claim back to the
   source that owns it.
2. Writes the findings to a single Markdown file, citing each claim's source.
3. Saves it wherever the repo already keeps such notes, matching the existing convention — or
   somewhere sensible, and says where.

The output is a file you can read later and trust, not a chat answer that scrolls away.

Model-invocable, so an agent can reach for it when you ask for a topic to be researched — or
call it directly with `/research`.

**Needs a host that can spawn background agents.** Claude Code and Codex can; on a runtime
that can't, the skill still works, it just researches in the foreground.

---

## Install (Claude Code)

```bash
git clone https://github.com/drkpxl/drkpxl-skills.git
cp -r drkpxl-skills/skills/research ~/.claude/skills/research
```

Or as a plugin:

```
/plugin marketplace add drkpxl/drkpxl-skills
/plugin install research@drkpxl-skills
```

For Codex, pi, and Hermes, see [Install on other agents](../../README.md#install-on-other-agents).

---

## Files

| File / folder | Purpose |
|---|---|
| `SKILL.md` | The whole skill — the background-agent brief and its three rules |
| `agents/openai.yaml` | Codex UI metadata (display name, short description) |
| `LICENSE` | Upstream MIT license (© 2026 Matt Pocock) |

---

[github.com/drkpxl/drkpxl-skills](https://github.com/drkpxl/drkpxl-skills)
