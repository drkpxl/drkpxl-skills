---
name: morning-briefing
description: "Use when running the daily printable morning briefing."
version: 1.0.1
author: drkpxl
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [briefing, morning, print, newspaper, cron, weather, calendar, news, newsletter]
    related_skills: [hermes-cron-automation]
---

# Morning Briefing

A personal daily newspaper. Every morning at 6 AM, the agent gathers data from available sources, curates a single 8.5×11 page, renders it to PDF, and sends it to a network printer. The page is designed to be read over coffee — dense, scannable, and consistent. Overflow content links to a QR-coded web page.

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

Full Hermes agent session. The value is curation and judgment — the agent decides what's worth reading, fits it on one page, and self-heals on source failures. A no-agent script can fetch data but cannot curate.

**Pipeline:** gather data → render HTML → check page count → trim if > 1 page → generate PDF → send to printer → notify on failure. Overflow content → QR code → Tailscale-hosted HTML page.

## Config

User-specific config lives in `~/.hermes/scripts/morning-briefing-config.json`. Onboarding creates this file. The agent reads it at the start of each run.

| Setting | Example value | Purpose |
|---|---|---|
| weather_entity | `<your HA weather entity>` | HA weather entity |
| calendar_entities | `<your HA calendar entities>` | HA calendar entities (list) |
| air_quality_entity | `<your AQI sensor>` | HA AQI sensor (or tinyair MCP) |
| printer_name | `<your CUPS printer name>` | CUPS printer name |
| location | `<your city, state>` | Display name + news geo-filter |
| news_topics | see interest profile | Topics + per-topic deep-dive |
| newsletter_senders | discovered at onboarding | Email addresses of newsletters to scan |
| overflow_host | `<your tailscale hostname>` | Tailscale hostname for overflow pages |
| overflow_port | `18091` | Port for overflow HTTP server |
| overflow_dir | `~/.hermes/www/briefing-overflow/` | Directory for overflow HTML files |
| notify_entity | `<your HA notify entity>` | HA notify entity for failure alerts |

## Procedure

### 1. Read config

Read `~/.hermes/scripts/morning-briefing-config.json`. If missing, run onboarding (see `references/onboarding.md`).

### 2. Gather data sources

Each source is independent. If one fails, attempt one self-healing retry, then render error text in that section. Never skip a section silently.

**Weather** — `ha_get_state` for the configured weather entity. Extract: current temp, condition, humidity, wind speed/direction, visibility, pressure. Also fetch the forecast (today's high/low, precipitation probability) via the NWS API at `https://api.weather.gov/gridpoints/<office>/<x>,<y>/forecast` if the HA forecast service is unavailable.

**Calendar** — `ha_get_state` for each configured calendar entity. Extract events for today only. For each event: start time, end time, summary, location (if any). Sort by start time. If no events, render "No events scheduled today."

**Air quality** — `ha_get_state` for the AQI sensor. Extract: AQI value, category (Good/Moderate/Unhealthy/etc.), PM2.5, PM10, O3 if available. Alternatively, use tinyair MCP tools (`mcp__tinyair__get_air_quality`) if HA sensor is unavailable.

**News** — This is the curation step, the core value of the briefing.
  1. For each topic in the interest profile, run targeted searches:
     - xAI `x_search` for X/Twitter discussion (last 24h)
     - `web_search` for Hacker News and Reddit (last 24h)
  2. Score each candidate item against the interest profile — does this match what the user actually cares about within this topic?
  3. Rank by relevance + signal strength. Discard noise (brand marketing, gear reviews, pass-purchase chatter unless there's a real announcement).
  4. Select the top N items that will fit in the news section (agent estimates based on remaining page space).
  5. For each selected item: write a 1-2 sentence summary with source attribution. Include the URL for the overflow page.

**Newsletters** — If Gmail connector is available and newsletter senders are configured:
  1. Search Gmail for emails from configured newsletter senders received in the last 24h.
  2. For each newsletter found, extract the sections matching the user's interest profile.
  3. Summarize each matching section in 1-2 sentences with the newsletter name as attribution.
  4. Note non-matching sections in a one-liner: "Also in [newsletter]: [topics]."

### 3. Render the page

Build an HTML page from the gathered data using the template at `templates/briefing.html`. The page has a fixed relative skeleton:

1. **Header** — title, date, location
2. **Weather + Calendar section** — current conditions + forecast + AQI + radar, calendar nested below
3. **News + Newsletter block** — fills remaining space, curated summaries with QR codes
4. **Joke of the Day** — family-friendly, at the bottom
5. **QR code** — per-story QR codes link to full sources; overflow QR at bottom if needed

The agent fills each section but never exceeds one page. See `references/layout-spec.md` for the full design spec.

### 4. Render-check-rerender loop

After generating the HTML, render it to PDF and check the page count:

```bash
DYLD_LIBRARY_PATH=/opt/homebrew/lib python3 -c "
from weasyprint import HTML
doc = HTML(filename='<html_path>').render()
print(f'Pages: {len(doc.pages)}')
doc.write_pdf('<pdf_path>')
"
```

If page count > 1:
- Trim the news section (remove lowest-ranked items, move them to overflow)
- Re-render and check again
- Repeat until it fits on one page (max 3 iterations)
- Move all trimmed content to the overflow page

If it still doesn't fit after 3 iterations, accept the best version and note the overflow.

### 5. Generate QR codes

Per-story QR codes link to the strongest source for each news item. Generate with the `qrcode` library and embed as base64 data URIs:

```python
import qrcode, base64, io
qr = qrcode.QRCode(version=1, box_size=3, border=1)
qr.add_data('https://example.com/full-story')
qr.make(fit=True)
img = qr.make_image(fill_color='black', back_color='white')
buf = io.BytesIO()
img.save(buf, format='PNG')
data_uri = f"data:image/png;base64,{base64.b64encode(buf.getvalue()).decode()}"
```

If there's overflow content (news items that didn't fit, full newsletter sections):
1. Write the overflow content to an HTML file at `<overflow_dir>/<date>.html`
2. Generate a QR code linking to `https://<overflow_host>:<overflow_port>/<date>.html`
3. Embed the overflow QR code at the bottom of the printed page

The overflow page auto-expires after 24h. Clean up overflow files older than 24h at the start of each run.

### 6. Print

Render final HTML → PDF via WeasyPrint, then send to printer:

```bash
DYLD_LIBRARY_PATH=/opt/homebrew/lib python3 <skill_dir>/scripts/render_and_print.py \
  --html <html_path> --pdf <pdf_path> --printer <your_printer_name>
```

The script handles the WeasyPrint render and `lp` command. Verify `lp` returns exit code 0 and a request ID.

### 7. Failure handling

- **Printer unreachable** — Send a notification to the user's preferred channel (squawk, HA push, etc.) with a link to the rendered HTML page. The user can read it on their phone.
- **Source failure** — After one retry, render error text in that section: "⚠ Weather unavailable: [error]". Continue with other sources.
- **Complete failure** — Send a notification: "Morning briefing failed: [error]".

### 8. Cleanup

- Delete overflow HTML files older than 24h from `<overflow_dir>/`
- Leave the rendered HTML and PDF in `/tmp/` for the session (useful for debugging)
- The cron job's final response should be a one-line confirmation: "Morning briefing printed. [N news items, M newsletter items, K overflow items.]"

## Onboarding

See `references/onboarding.md` for the full interactive onboarding flow. Summary:

1. **Auto-discovery** — probe for HA, Google Calendar, Gmail, tinyair, xAI, printer, Tailscale/Cloudflare
2. **Interest profile interview** — what topics, then deep-dive each topic
3. **Newsletter discovery** — scan inbox for newsletters, user confirms which to include
4. **Overflow hosting check** — verify Tailscale serve or Cloudflare tunnel is available
5. **Write config** — save to `~/.hermes/scripts/morning-briefing-config.json`
6. **Test run** — generate a sample briefing immediately to verify the pipeline

## Cron Setup

The cron job should be created with these toolsets: `homeassistant`, `file`, `terminal`, `web`, `browser`.

- **Schedule:** `0 6 * * *` (6 AM local time)
- **Model:** pin explicitly — never ride the global default
- **Deliver:** `local` (the printed page IS the deliverable; no chat notification needed on success)
- **Prompt:** should reference this skill by name and include the run procedure

## Design Spec

The briefing is a single 8.5×11 page, black and white newsprint aesthetic (except the color radar image). Key design decisions learned through iteration:

- **Layout uses real HTML `<table>` elements, NOT CSS flexbox.** WeasyPrint has unreliable flexbox support — `align-items: stretch` and `flex-direction: column` do not work. HTML tables render correctly every time.
- **Weather + Calendar share one section.** Three weather columns (temp, current, forecast) sit in a table row; the calendar nests below them inside the left cell. The color NWS radar image occupies the right cell, vertically centered, spanning both weather and calendar height.
- **Radar image is color, cropped to the user's area.** Fetch from `https://radar.weather.gov/ridge/standard/<station>_0.gif` (find your nearest NWS station at weather.gov). Convert to RGB, crop ~33% centered on the user's location, resize to 140×128px. Embed as base64 data URI.
- **News uses a 2-column masonry grid** (`column-count: 2`) with a vertical rule between columns. Each card has text on the left and a QR code (35px) on the right in a table cell. The lead story spans full width above the grid with a larger QR (38px).
- **QR codes link to the strongest source** for each story. Generate with `qrcode` library, embed as base64 data URIs so they work in both the preview pane and WeasyPrint PDF.
- **Newsletter section** appears after the news grid, separated by a solid rule. Summarizes matching sections from configured newsletters with a "Also in [newsletter]: [topics]" one-liner for non-matching content.
- **Joke of the Day** at the bottom, above the footer. Family-friendly.
- **All black and white** except the radar image. No color badges, no colored AQI — just text. Saves ink.
- **Serif body font** (Iowan Old Style/Palatino) for newsprint feel. Sans-serif (Helvetica) for section titles and topic labels.

See `templates/briefing.html` for the full template with placeholder variables.

## Common Pitfalls

1. **WeasyPrint needs DYLD_LIBRARY_PATH on macOS.** Set `DYLD_LIBRARY_PATH=/opt/homebrew/lib` before importing weasyprint. Without it, pango/glib won't load. The render script handles this automatically.

2. **WeasyPrint does NOT support flexbox reliably.** Use real HTML `<table>` elements for any multi-column layout. CSS `display: table` also works but real `<table>` elements are the most reliable.

3. **Page count check is mandatory.** The agent must render to PDF and check `len(doc.pages)` — never assume the page fits based on eyeballing the HTML. Use the render-check-rerender loop.

4. **News curation is the product.** Don't just dump search results. Score against the interest profile, discard noise, write concise summaries. A briefing that's just a keyword-filtered RSS feed has no value. Search X (x_search), HN, and Reddit for each topic.

5. **Each section renders or renders its error.** No blank spaces, no missing sections. If weather fails, the weather block says "⚠ Weather unavailable" — it doesn't disappear.

6. **Radar image must be cropped and in color.** The full NWS radar image shows too much of the surrounding area. Crop to ~33% centered on the user's location. Keep color — the precipitation levels (green/yellow/red) are useful. Convert to RGB, crop, resize, embed as base64.

7. **QR codes use base64 data URIs.** File-based QR images don't work reliably in WeasyPrint. Generate the QR, encode as base64 `data:image/png;base64,...`, and embed directly in the `<img src="...">`.

8. **Gmail newsletter scanning needs Python 3.10+.** The `google_api.py` script uses `str | None` syntax. System Python on macOS may be 3.9. Run with your agent's venv Python if needed.

9. **GLM stop→length false positive.** If using a GLM model, end the cron response with a period to avoid the heuristic that injects a fake "continue" prompt. See hermes-cron-automation skill for details.

10. **`execute_code` is blocked in cron mode.** Use `write_file` + `terminal` with the render script, not inline Python.

11. **Newsletter scanning needs the Gmail connector.** If the user doesn't have Gmail connected, skip the newsletter section gracefully — don't error the whole briefing. Search with `from:<sender> newer_than:1d`.

## Verification Checklist

- [ ] Config file exists at `~/.hermes/scripts/morning-briefing-config.json`
- [ ] Every data source was attempted; failures have error text in the rendered page
- [ ] PDF was generated and page count verified as 1
- [ ] `lp` returned exit code 0 with a request ID
- [ ] If overflow exists: QR code generated, overflow URL reachable (curl 200)
- [ ] Overflow files older than 24h cleaned up
- [ ] Final response is a one-line confirmation