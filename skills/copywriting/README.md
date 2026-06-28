# Copywriting — conversion copy for website pages

A pure-prompt skill that turns your agent into a conversion copywriter for **website
pages** — homepage, landing, pricing, feature, and about pages. No API key, no MCP server,
no backend. Just `SKILL.md` and a reference file.

The defining behavior: this skill **edits the copy where it lives in your codebase**
(JSX/TSX, HTML, Markdown/MDX, Vue/Svelte templates) instead of dumping copy into chat for
you to paste. It applies the single strongest version, keeps diffs small, and leaves copy
that already works alone.

---

## What it does

- Rewrites or writes page copy: headlines, subheadlines, hero sections, body, CTAs.
- Finds where the copy lives and edits it **in place**; creates the file for net-new pages.
- Applies proven principles — clarity over cleverness, benefits over features, specificity,
  customer language — and the frameworks in
  [`references/copy-frameworks.md`](references/copy-frameworks.md).
- Commits to one strong version per element (no alternatives dumped in chat) and updates
  `<title>` / meta description when the page owns them.
- Respects strong copy: if a line already works, it leaves it alone rather than inventing
  problems to justify edits.

Scope is **website pages**. For email, popup, or offer copy, this isn't the skill.

---

## Install (Claude Code)

```bash
git clone https://github.com/drkpxl/drkpxl-skills.git
cp -r drkpxl-skills/skills/copywriting ~/.claude/skills/copywriting
```

Installing the folder (`SKILL.md` + `references/`) is sufficient — Claude Code picks up the
reference file when it needs the formulas.

---

## Try it without installing

Point any agent session at the file directly — no install required:

```
Read and follow path/to/skills/copywriting/SKILL.md, then rewrite the hero copy in index.html.
```

Because the skill edits files, run it in a repo where you can review the `git diff` and
discard freely.

---

## Files

| File / folder | Purpose |
|---|---|
| `SKILL.md` | The skill definition — workflow, principles, page structure, CTA and voice guidance |
| `references/copy-frameworks.md` | Headline formulas, persuasion frameworks (PAS/AIDA/BAB/FAB), page templates, proof/objection patterns, transition phrases |

---

[github.com/drkpxl/drkpxl-skills](https://github.com/drkpxl/drkpxl-skills)
