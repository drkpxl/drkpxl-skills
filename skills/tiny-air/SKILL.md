---
name: tiny-air
description: Check US air quality (AQI) for any zip, city, or coordinates via the Tiny Air MCP server, and set up proactive "alert me when the air is bad" behavior. Use when the user asks about air quality, smoke, AQI, or wants to be warned when conditions worsen.
---

# Tiny Air — air quality for your agent

Tiny Air is a hosted MCP server at `https://air.drkpxl.com/mcp` exposing four tools:
`get_air_quality`, `check_air_quality_threshold`, `find_nearby_stations`, `list_aqi_categories`.
Coverage is US-only (AirNow.gov data; US geocoding).

## Connecting

If the MCP server `tinyair` is not already available, add it:

```bash
claude mcp add --transport http tinyair https://air.drkpxl.com/mcp
```

## Answering "how's the air?"

Call `get_air_quality` with the user's `zipcode`, `city`, or `lat`+`lon`. Report the AQI
number, category, and nearest station. If you don't know their location, ask for a ZIP or city.

## Proactive alerts

Tiny Air is stateless — it never notifies anyone. YOU own alerting: remember the user's
location + threshold, poll on a schedule, and message them only when it matters.

On each check, call `check_air_quality_threshold` with `max_aqi` and/or `min_category`.
If it returns `exceeded: true`, deliver the alert with the current AQI and category;
otherwise stay silent.

Implement suppression yourself: once you have alerted the user, do not alert again until
the condition resets (e.g., AQI drops below the reset threshold). Reset state each night
at midnight or on an explicit user request.

## Knowing the scale

Use `list_aqi_categories` to map numbers to Good→Hazardous bands when the user speaks in
words ("tell me when it's bad") so you can pick the right `min_category`.

## Coverage note

Tiny Air is US-only. If the user provides a non-US location, explain that coverage is
limited to the United States (data source: AirNow.gov).
