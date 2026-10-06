# Colorado Traffic

Live Colorado road events for AI agents. The agent queries CDOT's public COtrip 511 API and answers from that JSON. No API key. No scraping Google Maps or Waze.

Default corridor is I-70 from Golden to east Denver (mile points 259–279). Other corridors are a flag, not a different skill.

## Features

- **Now / upcoming / Waze, kept separate.** `active: true` is not "happening now." Future night closures are flagged active. Trust `when`.
- **Mile-point filter.** Incidents, closures, construction, Waze, winter driving, and chain laws, clipped to the corridor you asked for.
- **Direction from the feed.** Positive is eastbound on I-70 and northbound on I-25. Both-directions stays both.
- **No key for the live feed.** Optional Google Routes travel time only if a key is already in the environment. The script never reads it.

## Requirements

- Python 3.10 or newer (`zoneinfo`, `int | None`). On macOS, system Python may be 3.9 — use the agent venv interpreter.
- Network access to `https://api-511x-co.carsprogram.org`. No account.
- Optional: `GOOGLE_MAPS_API_KEY` already set, only if you want a traffic-aware drive time. Missing key means no travel-time number. Do not guess.

## Install

Copy the whole directory, not just `SKILL.md`. The script and `references/` have to travel with it.

Hermes (this is the path `SKILL.md` runs):

```bash
git clone https://github.com/drkpxl/drkpxl-skills.git
cp -r drkpxl-skills/skills/colorado-traffic ~/.hermes/skills/colorado-traffic
```

Or, after this repo is pushed, from a machine that already has the `drkpxl/drkpxl-skills` tap:

```bash
hermes skills install drkpxl/drkpxl-skills/colorado-traffic --name colorado-traffic -y
```

Claude Code:

```
/plugin marketplace add drkpxl/drkpxl-skills
/plugin install colorado-traffic@drkpxl-skills
```

Other agents: `npx skills@latest add drkpxl/drkpxl-skills -a hermes-agent,codex,pi` and pick Colorado Traffic, or copy `skills/colorado-traffic/` into that agent's skills folder. See the repo README for the per-agent paths.

## Usage

Ask about Colorado traffic, I-70, COtrip, or the Golden–Denver commute. The agent runs:

```bash
python3 ~/.hermes/skills/colorado-traffic/scripts/cotrip_corridor.py
```

Tighter Golden-to-I-25 box: `--corridor i70-golden-i25`. Another highway: `--route "I-25" --min-mp 210 --max-mp 216`.

Floyd Hill and the Eisenhower Tunnel are west of the default box. This skill will not mix them into a Golden–Denver answer unless you ask.

A repeating alert is a separate cron, and only if you ask for one. A one-off question does not start a watcher.

## License

MIT
