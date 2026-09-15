---
name: morning-briefing
description: "Use when running the daily printable morning briefing."
version: 2.0.0
author: drkpxl
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [briefing, morning, print, newspaper, cron, weather, calendar, news, newsletter]
    related_skills: [hermes-cron-automation]
---

# Morning Briefing

A personal daily newspaper. Every morning, the agent gathers data from available sources, curates a single 8.5×11 page, renders it to PDF, and sends it to a network printer. The page is designed to be read over coffee — dense, scannable, and consistent.

This is a rubric, not a rigid pipeline. The agent discovers what tools are available at runtime and uses what it finds. Sources degrade gracefully — each section renders or renders its own error text. No silent gaps.

## When to Use

- Scheduled 6 AM cron run (daily)
- User says "run my briefing", "print my morning briefing", "generate today's briefing"
- Onboarding a new user: "set up morning briefing", "configure briefing skill"

Don't use for:
- Breaking news alerts (that's a different workflow)
- Full inbox triage (the briefing only scans known newsletter senders)
- Weather-only queries (use HA tools directly)

## Architecture

Full Hermes agent session. The value is curation and judgment — the agent decides what's worth reading, fits it on one page, and self-heals on source failures.

**No permanent scripts.** The skill contains no scripts directory. All Python scripts are throwaway — written to `/tmp/` at runtime by the agent, executed via `terminal`, then discarded. The skill is a rubric, not a codebase.

**Pipeline:** gather data → process images → write HTML → render PDF → check page count → trim if needed → print → notify on failure.

The agent does everything with Hermes tools:
- `ha_get_state` — weather, calendar, AQI
- `x_search` — X/Twitter discussion
- `web_search` — Hacker News, Reddit, news
- `web_extract` — NWS forecast API
- Gmail via `google_api.py` — newsletters
- `write_file` — write HTML, write throwaway Python scripts
- `terminal` — run Python scripts (image processing, PDF rendering), print via `lp`

## Config

User-specific config lives in `~/.hermes/scripts/morning-briefing-config.json`. Onboarding creates this file. The agent reads it at the start of each run.

| Setting | Purpose |
|---|---|
| weather_entity | HA weather entity ID |
| calendar_entities | List of HA calendar entity IDs |
| air_quality_entity | HA AQI sensor entity ID (or tinyair MCP) |
| printer_name | CUPS printer name |
| location | Display name + news geo-filter |
| news_topics | Interest profile — topics with keywords and descriptions |
| newsletter_senders | Email addresses of newsletters to scan |
| overflow_host | Tailscale hostname for overflow pages |
| overflow_port | Port for overflow HTTP server |
| overflow_dir | Directory for overflow HTML files |
| notify_entity | HA notify entity for failure alerts |

## Procedure

### 1. Read config

Read `~/.hermes/scripts/morning-briefing-config.json` with `read_file`. If missing, run onboarding (see `references/onboarding.md`).

### 2. Gather data sources

Each source is independent. If one fails, attempt one self-healing retry, then render error text in that section. Never skip a section silently.

**Weather** — `ha_get_state` for the configured weather entity. Extract: current temp, condition, humidity, wind speed/direction, visibility, pressure. Fetch the forecast (today's high/low, precipitation probability) via the NWS API at `https://api.weather.gov/gridpoints/<office>/<x>,<y>/forecast` using `web_extract` if the HA forecast service is unavailable.

**Calendar** — `ha_get_state` for each configured calendar entity. Extract events for today only. Sort by start time. If no events, render "No events scheduled today."

**Air quality** — `ha_get_state` for the AQI sensor. Extract: AQI value, category, PM2.5, PM10, O3. Alternatively, use tinyair MCP tools if HA sensor is unavailable.

**News** — This is the curation step, the core value of the briefing.
1. For each topic in the interest profile, run targeted searches:
   - `x_search` for X/Twitter discussion (last 24h)
   - `web_search` for Hacker News and Reddit (last 24h)
2. Score each candidate item against the interest profile — does this match what the user actually cares about within this topic?
3. Rank by relevance + signal strength. Discard noise.
4. Select the top N items that will fit in the news section.
5. For each selected item: write a 1-2 sentence summary with source attribution.

**Newsletters** — If Gmail is available and newsletter senders are configured:
1. Search Gmail for emails from configured newsletter senders received in the last 24h.
2. Extract the sections matching the user's interest profile.
3. Summarize each matching section in 1-2 sentences with the newsletter name.
4. Note non-matching sections: "Also in [newsletter]: [topics]."

### 3. Process images

Two image processing steps, both done via throwaway Python scripts written to `/tmp/` with `write_file`, then run with `terminal` using the Hermes venv Python (`~/.hermes/hermes-agent/venv/bin/python3`).

**Radar image** — Write a script to `/tmp/radar_process.py` that:
- Fetches `https://radar.weather.gov/ridge/standard/<station>_0.gif`
- Converts to RGB, crops ~33% centered on the user's location
- Resizes to 140×128px
- Outputs a base64 data URI string to stdout

**QR codes** — Write a script to `/tmp/qr_gen.py` that:
- Takes a list of URLs (hardcoded in the script)
- Generates QR codes with the `qrcode` library
- Outputs base64 data URIs to stdout

### 4. Write the HTML page

Assemble the complete HTML page with all data, QR codes, and radar image embedded as base64 data URIs. Write it to `/tmp/briefing.html` using `write_file`.

The page uses the design spec in `references/layout-spec.md` and the template structure in `templates/briefing.html`. Key rules:

1. **Layout uses real HTML `<table>` elements** — not CSS flexbox (PDF renderer doesn't support flexbox).
2. **Weather + Calendar share one section** — three weather columns in a table row, calendar nested below in the left cell, color radar in the right cell spanning both.
3. **News uses a 2-column masonry grid** with per-story QR codes on the right.
4. **Lead story** spans full width above the grid.
5. **Newsletter section** after the news grid.
6. **Joke of the Day** at the bottom, family-friendly.
7. **All black and white** except the color radar image.
8. **Serif body font** (Iowan Old Style/Palatino), sans-serif section headers (Helvetica).

### 5. Render PDF and check page count

Write a throwaway Python script to `/tmp/render_pdf.py` using `write_file` that:
- Sets `os.environ['DYLD_LIBRARY_PATH'] = '/opt/homebrew/lib'` (macOS — pango/glib from Homebrew)
- Imports weasyprint
- Renders `/tmp/briefing.html` to `/tmp/briefing.pdf`
- Prints the page count to stdout

Run it with: `~/.hermes/hermes-agent/venv/bin/python3 /tmp/render_pdf.py`

If page count > 1: trim the news section, re-write the HTML, re-render. Max 3 iterations.

### 6. Print

Send the PDF to the printer via `terminal`:

`lp -d <printer_name> -o media=letter /tmp/briefing.pdf`

Verify `lp` returns exit code 0 and a request ID.

### 7. Failure handling

- **Printer unreachable** — Send a notification to the user's preferred channel with a link to the rendered HTML.
- **Source failure** — After one retry, render error text in that section. Continue with other sources.
- **Complete failure** — Send a notification with the error.

### 8. Cleanup

- Leave rendered HTML and PDF in `/tmp/` for debugging
- Final response: one-line confirmation ending with a period (avoids GLM stop-length false positive)

## Onboarding

See `references/onboarding.md` for the full interactive onboarding flow.

## Cron Setup

- **Schedule:** `0 6 * * *` (6 AM local time)
- **Model:** pin explicitly with `hermes cron edit <job_id> --model <model> --provider <provider>` — never ride the global default
- **Deliver:** `local` (the printed page IS the deliverable)
- **Toolsets:** `homeassistant`, `file`, `terminal`, `web`, `browser`
- **Prompt:** self-contained, references this skill, tells the agent to write scripts to /tmp/ and run them (never inline Python)

## Common Pitfalls

1. **CRITICAL: Inline Python is blocked in cron mode.** Never use `python3 -c` or `execute_code` in a cron job. Always `write_file` a script to `/tmp/` first, then run it with `terminal`. This is the #1 reason cron runs fail.

2. **Pin the model on every cron job.** Use `hermes cron edit <job_id> --model <model> --provider <provider>`. If left null, the job inherits the global default, which may be a weaker model that can't follow the skill instructions.

3. **WeasyPrint needs DYLD_LIBRARY_PATH on macOS.** Set `os.environ['DYLD_LIBRARY_PATH'] = '/opt/homebrew/lib'` at the top of any Python script that imports weasyprint.

4. **Use real HTML `<table>` elements, not flexbox.** WeasyPrint does not support flexbox reliably. Tables render correctly every time.

5. **Page count check is mandatory.** Always render to PDF and check the page count.

6. **News curation is the product.** Don't dump search results. Score against the interest profile, discard noise, write concise summaries.

7. **Each section renders or renders its error.** No blank spaces.

8. **QR codes use base64 data URIs.** Embed as `data:image/png;base64,...` in the `<img src="...">`. Minimum rendered size: lead story 50px, grid cards 45px, newsletter 45px. Smaller than 45px won't scan reliably when printed.

9. **Gmail newsletter scanning needs Python 3.10+.** Run `google_api.py` with `~/.hermes/hermes-agent/venv/bin/python3`.

10. **GLM stop→length false positive.** End the cron response with a period.

11. **No permanent scripts in the skill.** All scripts are throwaway — written to `/tmp/` at runtime. The skill is a rubric, not a codebase.

## Verification Checklist

- [ ] Config file exists at `~/.hermes/scripts/morning-briefing-config.json`
- [ ] Every data source attempted; failures have error text in the rendered page
- [ ] HTML written to `/tmp/briefing.html` with `write_file`
- [ ] PDF rendered, page count verified as 1
- [ ] `lp` returned exit code 0 with a request ID
- [ ] Final response is a one-line confirmation ending with a period