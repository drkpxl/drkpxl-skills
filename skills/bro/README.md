# Bro — say that again, in plain English

A one-line skill. You invoke it after your agent hands you a wall of jargon, and it
restates its own last message like a human talking to another human.

No API key, no MCP server, no reference files. Just `SKILL.md`.

---

## What it does

Rewrites the agent's **previous message** — same content, no jargon, shorter, plainer. It
does not do new work, re-run tools, or change its answer; it re-says it.

The skill sets `disable-model-invocation: true`, so the agent will never trigger it on its
own. It only fires when you ask for it, which is the point — you decide when an answer
needed translating.

---

## Usage

In Claude Code, after any response you didn't like the shape of:

```
/bro
```

Or just ask for it in words ("say that again in plain English") — same result, since the
skill is a single instruction.

---

## Install (Claude Code)

```bash
git clone https://github.com/drkpxl/drkpxl-skills.git
cp -r drkpxl-skills/skills/bro ~/.claude/skills/bro
```

Or as a plugin:

```
/plugin marketplace add drkpxl/drkpxl-skills
/plugin install bro@drkpxl-skills
```

---

## Files

| File | Purpose |
|---|---|
| `SKILL.md` | The whole skill — one instruction, manual invocation only |

---

[github.com/drkpxl/drkpxl-skills](https://github.com/drkpxl/drkpxl-skills)
