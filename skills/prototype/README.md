# Prototype — throwaway code that answers one question

A pure-prompt skill for building **prototypes, not products**. No API key, no MCP server, no
backend. Just `SKILL.md` and two reference files.

The defining idea: a prototype is throwaway code that answers a *question*, and the question
decides the shape. The skill's first move is to figure out which question is on the table,
then commit to one of two very different artifacts.

Forked from [mattpocock/skills](https://github.com/mattpocock/skills) (`skills/engineering/prototype`).

---

## What it does

Picks a branch, then builds to that branch's rules:

| Question | Branch | Artifact |
|---|---|---|
| "Does this logic / state model feel right?" | [`references/LOGIC.md`](references/LOGIC.md) | One self-contained HTML file — free-play buttons plus tabbed guided walkthroughs over a pure, liftable state module. Double-click to run, emailable to a PM or designer. |
| "What should this look like?" | [`references/UI.md`](references/UI.md) | 3 (max 5) **structurally different** UI variants on a single route, switched by `?variant=` and a floating bottom bar with arrow-key support, hidden in production builds. |

Rules both branches share: throwaway and clearly named as such, trivial to run, no
persistence, no tests or abstractions, full state surfaced after every action — and when the
question is answered, fold the decision into real code and park the prototype itself on a
throwaway branch rather than merging it to main.

The skill is model-invocable (no `disable-model-invocation`), so an agent can reach for it
when you say "let me see a few options for this page" — or you can call it directly.

---

## Install (Claude Code)

```bash
git clone https://github.com/drkpxl/drkpxl-skills.git
cp -r drkpxl-skills/skills/prototype ~/.claude/skills/prototype
```

Or as a plugin:

```
/plugin marketplace add drkpxl/drkpxl-skills
/plugin install prototype@drkpxl-skills
```

Install the whole folder — `SKILL.md` routes to `references/` on demand, and the agent needs
the branch file to build anything.

For Codex, pi, and Hermes, see [Install on other agents](../../README.md#install-on-other-agents).

---

## Try it without installing

```
Read and follow path/to/skills/prototype/SKILL.md — I want to see three options for the settings page.
```

---

## Files

| File / folder | Purpose |
|---|---|
| `SKILL.md` | The skill definition — picks the branch, holds the rules both branches share |
| `references/LOGIC.md` | The shareable-HTML branch: pure module shape, page hierarchy, walkthrough scenarios, anti-patterns |
| `references/UI.md` | The UI-variants branch: sub-shapes A/B, generating variants, the switcher, cleanup, anti-patterns |
| `agents/openai.yaml` | Codex UI metadata (display name, short description) |
| `LICENSE` | Upstream MIT license (© 2026 Matt Pocock) |

---

[github.com/drkpxl/drkpxl-skills](https://github.com/drkpxl/drkpxl-skills)
