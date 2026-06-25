# Proactive air-quality alerts with Tiny Air

## The stateless model — the agent owns alerting

Tiny Air is a stateless MCP server: it answers queries on demand but never pushes
notifications or remembers previous calls. This is intentional — it keeps the server
simple and gives your agent full control over when and how you are notified.

The pattern is:

1. You tell your agent a location, a threshold, and a schedule.
2. The agent polls `check_air_quality_threshold` on that schedule.
3. If the response includes `exceeded: true`, the agent sends you an alert with the
   current AQI and category.
4. The agent implements suppression (don't alert again until conditions reset) and
   any reset schedule you specify — the server has no memory of prior checks.

This means proactive alerts work with any agent that supports scheduled or recurring
tasks. Two canonical recipes are below.

---

## Recipe A — numeric threshold, frequent polling, with suppression and nightly reset

Paste this into your agent as a standing instruction or scheduled task:

```
Every 20 minutes, check Tiny Air for my air quality (zip 80202) and alert me whenever the
AQI is worse than 60. Use check_air_quality_threshold with max_aqi 60; if exceeded is true,
send me the current AQI and category — then don't alert me again until the AQI drops back
below 50. Reset each night at midnight.
```

The suppression band (alert above 60, reset below 50) prevents notification storms during
borderline conditions.

---

## Recipe B — category threshold, daily morning check

Paste this into your agent as a standing instruction or scheduled task:

```
Every morning at 7am, check Tiny Air for my air quality (zip 80202) and DM me only if
it's worse than "Unhealthy for Sensitive Groups". Use check_air_quality_threshold with
min_category "Unhealthy for Sensitive Groups"; if exceeded is true, send the AQI + category.
```

Use `list_aqi_categories` to find the exact category name strings if you want a different
threshold (e.g., "Moderate", "Unhealthy", "Very Unhealthy", "Hazardous").

---

## Per-agent scheduling notes

### Hermes
Use the Hermes built-in scheduler. Define a recurring job in your Hermes config pointing
to a task that calls the `tinyair` MCP tools. Hermes handles the timing; your task
definition implements the suppression logic using Hermes memory or a scratchpad file.

### OpenClaw
Add a `HEARTBEAT.md` to your OpenClaw project. OpenClaw reads `HEARTBEAT.md` on each
agent heartbeat cycle and executes the instructions there. Example:

```markdown
- Every morning at 7am, call tinyair `check_air_quality_threshold` for zipcode 80202
  with min_category "Unhealthy for Sensitive Groups". If `exceeded` is true, send me
  the current AQI and category.
```

OpenClaw manages the timing; the agent reads the instruction and calls the MCP tool.

### Claude Code / Claude Desktop
Use a background task or system cron to invoke Claude Code on a schedule:

```bash
# crontab -e — run Claude Code every 20 minutes to check air quality
*/20 * * * * claude -p "Check Tiny Air for zip 80202. Use check_air_quality_threshold with max_aqi 60. If exceeded is true, notify me." 2>&1 >> ~/air-quality.log
```

For a more integrated approach, ask Claude Code to set up a background task that polls
on your behalf and uses your preferred notification method (macOS notification, email,
Slack, etc.).
