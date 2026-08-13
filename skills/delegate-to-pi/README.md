# Delegate to pi — packet in, you check it

Say "delegate to pi" and the agent writes an 8-slot handoff packet of what it
already knows, then hands the *build* to the [`pi`](https://github.com/badlogic/pi-mono)
CLI running `deepseek-v4-flash:cloud` on Ollama. Pi executes the packet. It does
not re-explore the repo. The orchestrator then verifies against the **Done when**
list it wrote before pi started.

This is the orchestrator-worker split: the expensive model decides and checks,
the cheap model generates. Generating is the part you stop paying for, which is
why it pays on volume — a whole module from one packet — and not on a subtle
one-line fix.

---

## The packet

The prompt pi sees is not a greenfield spec. It is eight headings, in order:

| Slot | What it carries |
|---|---|
| **Goal** | One sentence |
| **Done when** | Numbered, checkable criteria |
| **Already decided** | Locked session facts — do not reopen |
| **Map** | Existing files, pattern to copy, interface to match |
| **Layout** | Files to create or edit |
| **Constraints** | Allowed paths, do-not-touch, deps |
| **Verify** | Exact commands the orchestrator will re-run |
| **Out of scope** | What this run is not |

Pi's standing brief says: implement from the packet, do not rediscover the repo.

---

## How it works

1. **Preflight** — `pi` on PATH, Ollama `ready`, note what already exists.
2. **Packet** — dump decisions, file map, and verify commands. pi cannot ask a
   clarifying question, so anything left implicit it will invent.
3. **Dispatch** — standing brief + packet as one prompt. Tools: `read,bash,edit,write`.
   Report in five sections (`FILES` / `COMMANDS` / `CRITERIA` / `SUMMARY` / `UNCERTAIN`).
4. **Inventory** — check the tree, do not trust pi's file list.
5. **Verify** — run it, walk each Done-when, write one assertion of your own,
   probe empty/zero/error paths.
6. **Follow up** — failures go back into the *same* session as a delta (exact
   command + expected vs actual), capped at two rounds. Not a rewritten packet.

---

## Why the criteria come first

Testing is not verification. Tests check that code runs; verification checks that
it does what was agreed. Pi wrote both the code and the tests, so a green suite
is self-consistent rather than correct.

For a brand-new project the numbered **Done when** lines are the only baseline
that exists. Pi's `CRITERIA:` report is a claim to check, not evidence.

That's also why the skill requires one assertion written by the verifier, not
the generator.

---

## Requirements

- **pi CLI** on PATH — developed against 0.84.1
- **Ollama provider ready** — `pi auth check --provider ollama --json`; the cloud
  tag needs Ollama cloud auth
- **`gtimeout`** (coreutils), recommended — macOS has no `timeout`, and pi runs can hang

---

## Install (Claude Code)

```bash
git clone https://github.com/drkpxl/drkpxl-skills.git
cp -r drkpxl-skills/skills/delegate-to-pi ~/.claude/skills/delegate-to-pi
```

Or as a plugin:

```
/plugin marketplace add drkpxl/drkpxl-skills
/plugin install delegate-to-pi@drkpxl-skills
```

For Codex, pi, and Hermes, see [Install on other agents](../../README.md#install-on-other-agents).

---

## Usage

Model-invocable — an agent reaches for it when you say things like:

```
delegate to pi: build a CLI that converts our CSV exports to JSON
have pi write the API layer, then check it
let pi scaffold the project
```

Or call it directly with `/delegate-to-pi`.

**Good fit:** a new project or module, a CLI, an API surface, models and
schemas, test scaffolding, many similar files.

**Bad fit:** a subtle bug fix, a change needing deep context, a design decision.
There the packet costs about what the work costs — do it directly.

For anything large, dispatch in stages with their own packets (schema, then API,
then CLI) and verify each before the next. One giant packet fails in ways that
are hard to attribute.

### Changing the model

```bash
--model qwen3.5:397b-cloud      # bigger cloud model
--model gemma4:12b-mlx          # fully local, ~10x slower on a trivial prompt
```

A pinned tag like `deepseek-v4-flash:0731-cloud` may warn `Model "..." not found
for provider "ollama". Using custom model id.` — cosmetic; it still runs. The
catalog pi ships can lag `ollama list`, and `pi update` refreshes it.

---

## Known rough edges

Observed while building this, all handled in the skill:

| Behavior | Handling |
|---|---|
| Runtimes swing from 10s to 230s for similar tasks | Cap the run (~5 min) rather than waiting |
| A run can hang with zero output and nothing written | Retry **once** with a new session id; a fresh session recovered in 10s |
| `-nt` (no tools) can hang | The skill never passes it |
| pi doesn't validate `-t` tool names | Typos silently drop a tool — the skill hardcodes `read,bash,edit,write` |
| pi will borrow another project's `.venv/bin/pytest` if the local runner is missing | The brief forbids it; verified pi then falls back to importing tests directly and discloses it |
| `pi -p` auto-approves every tool call | The `-t` allowlist and the brief are the only guardrails |

---

## Files

| File / folder | Purpose |
|---|---|
| `SKILL.md` | The whole skill — packet recipe, pi's brief, and the verify loop |
| `agents/openai.yaml` | Codex UI metadata (display name, short description) |

---

[github.com/drkpxl/drkpxl-skills](https://github.com/drkpxl/drkpxl-skills)
