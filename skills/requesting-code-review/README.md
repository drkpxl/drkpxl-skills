# Requesting Code Review — pre-commit verification, hardened for small models

A pure-prompt skill that runs an automated verification pipeline before code lands:
static security scan → regression-checked tests and lint → an independent reviewer
subagent → a bounded auto-fix loop → commit. No API key, no MCP server.

Adapted from the Hermes Agent skill of the same name (itself adapted from
[obra/superpowers](https://github.com/obra/superpowers) + MorAlekss), then rewritten
so that **small models** (DeepSeek flash, Gemma-class, etc.) can run it without
wrecking anything. Version 3.0.0.

**Core principle:** no agent verifies its own work. The reviewer is a separate
subagent with zero shared context — and zero tools.

---

## What "hardened for small models" means

Small models follow lookup tables, exact commands, and externalized state far more
reliably than prose judgment. The rewrite converts every judgment call it can into
one of those, and removes every command that can destroy work when fumbled:

| Hardening | Why |
|---|---|
| Hard-rules block up top; destructive git commands banned outright | `git stash` pop conflicts, `git reset`, and `git add -A` are exactly what small models fumble; none are needed |
| Baseline via read-only `git worktree`, never `git stash` | A conflicted stash pop can destroy the changes being verified |
| Scorecard reprinted after every step, explicit "attempt N of 2" counters | Small models lose loop state; the scorecard is externalized memory |
| Reviewer subagent gets **no tools** | It reads untrusted diff text; a reviewer with a terminal can be prompt-injected by a malicious diff into running commands |
| Instructions found inside a diff are themselves a blocking finding | Turns prompt injection attempts into an auto-fail instead of a vulnerability |
| Findings must quote a diff line verbatim, checked with `grep -F` | Small reviewers hallucinate blockers; unverifiable findings are discarded instead of feeding phantom fix loops |
| Strict JSON contract, one retry, then fail-closed with **no** fix loop | An unparseable verdict yields no trustworthy issue list — escalate, don't guess |
| Fix agent forbidden from touching tests | The classic small-model cheat is deleting the failing test |
| Scan patterns fixed and portability-tested | `grep "^+"` matched `+++ b/file` headers; `\s` isn't portable ERE — now `^\+[^+]` and `[[:space:]]`, tested on BSD and GNU grep |
| `\|\| true` on every grep, with "no output = clean" stated | grep exits 1 on no-match; small models read that as an error and retry forever |
| Lint rows gated on config-file existence; `node_modules/.bin` instead of `npx` | Bare `mypy .` on an unconfigured repo is an error avalanche; `npx` downloads tools mid-pipeline |
| Commit stages nothing new — `git add -A` removed from the commit step | The old version committed a wider diff than anyone reviewed |
| Failure endgame saves a patch and touches nothing | The old version suggested `git stash` or `git reset` to "undo" — destructive advice at the worst moment |

## Pipeline at a glance

```
0 scorecard → 1 diff → 2 static scan (S1–S7) → 3 tests + worktree baseline
→ 4 lint (changed files block) → 5 reviewer subagent (no tools, JSON verdict)
→ 6 combine → 7 fix loop (max 2, third context) → 8 commit "[verified] …"
```

---

## Install (Claude Code)

```bash
git clone https://github.com/drkpxl/drkpxl-skills.git
cp -r drkpxl-skills/skills/requesting-code-review ~/.claude/skills/requesting-code-review
```

Or as a plugin:

```
/plugin marketplace add drkpxl/drkpxl-skills
/plugin install requesting-code-review@drkpxl-skills
```

For Codex, pi, and Hermes, see [Install on other agents](../../README.md#install-on-other-agents).
The subagent steps use Hermes' `delegate_task` in the examples; on Claude Code the
agent (Task) tool is the equivalent, and the skill says what to do when no subagent
mechanism exists (self-review, marked as not independent).

---

## Try it without installing

```
Read and follow path/to/skills/requesting-code-review/SKILL.md — I'm done with this feature, verify and commit it.
```

---

## Files

| File / folder | Purpose |
|---|---|
| `SKILL.md` | The whole pipeline — hard rules, scorecard, scan commands, reviewer and fix-agent prompts, decision tables |
| `agents/openai.yaml` | Codex UI metadata (display name, short description) |

---

[github.com/drkpxl/drkpxl-skills](https://github.com/drkpxl/drkpxl-skills)
