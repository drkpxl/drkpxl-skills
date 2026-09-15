# Morning Briefing

A personal daily newspaper for AI agents. Every morning, the agent gathers weather, calendar, air quality, curated news, and newsletter summaries, renders a single 8.5×11 page in newsprint style, and sends it to your network printer. Think of it as a replacement for the morning paper — tailored to your interests, printable, and ready when you wake up.

## What it looks like

![Morning Briefing sample](screenshot.png)

## Features

- **Weather**: Current conditions, high/low forecast, AQI, and a color NWS radar image cropped to your area
- **Calendar**: Today's events from Home Assistant or Google Calendar
- **News & Signal**: Curated from X/Twitter, Hacker News, and Reddit — scored against your personal interest profile, not just keyword-matched. Each story has a QR code linking to the full source
- **Newsletters**: Scans your Gmail for configured newsletters (Morning Brew, etc.) and summarizes the sections relevant to your interests
- **Joke of the Day**: Family-friendly, at the bottom of the page
- **One page, always**: 8.5×11, guaranteed to fit — the agent renders, checks page count, and trims if needed

## Design

- Black and white newsprint aesthetic (except the color radar)
- Serif body font, sans-serif section headers
- Masonry grid for news with QR codes on the right of each story
- Lead story spans full width above the grid
- Weather and calendar share a section with the radar image spanning both

## Requirements

- **Hermes Agent** (or any agent that supports skills, tools, and cron)
- **Home Assistant** (optional — for weather, calendar, AQI sensors) or Google Calendar
- **Network printer** accessible via CUPS (`lp` command)
- **WeasyPrint** (`pip install weasyprint`) + pango/glib (`brew install pango glib` on macOS)
- **qrcode** (`pip install qrcode[pil]`)
- **Pillow** (`pip install Pillow`) — for radar image processing
- **Gmail connector** (optional — for newsletter scanning)
- **xAI OAuth** (optional — for X/Twitter search)
- **Tailscale or Cloudflare Tunnel** (optional — for QR-coded overflow pages)

The skill is designed to degrade gracefully. No single source is required — the agent uses what's available and renders error text for anything that fails.

## Install

1. Clone this repo or copy the `skills/morning-briefing/` directory into your agent's skills folder
2. Install dependencies:
   ```bash
   pip install weasyprint qrcode[pil]
   brew install pango glib  # macOS only
   ```
3. Say "set up morning briefing" to your agent — it will run the interactive onboarding flow
4. The agent discovers your data sources, interviews you about your interests, scans for newsletters, and writes a config file
5. A cron job runs at 6 AM daily (configurable)

## Config

User config lives at `~/.hermes/scripts/morning-briefing-config.json`. Onboarding creates this file. Key settings:

| Setting | Purpose |
|---|---|
| `weather_entity` | Home Assistant weather entity ID |
| `calendar_entities` | List of HA or Google Calendar entity IDs |
| `air_quality_entity` | HA AQI sensor or tinyair MCP |
| `printer_name` | CUPS printer name |
| `location` | Display name + news geo-filter |
| `news_topics` | Interest profile — topics with keywords and descriptions |
| `newsletter_senders` | Email addresses of newsletters to scan |
| `overflow_host` | Tailscale hostname for overflow pages |

## Community

This is a personal tool shared in case it's useful. Issues and PRs welcome.

## License

MIT