# Generic HTTP MCP client — Tiny Air

Any MCP client that supports the Streamable HTTP transport can connect to Tiny Air directly:

```
POST https://air.drkpxl.com/mcp   (Streamable HTTP, stateless)
```

The server is stateless — no session setup or persistent connection is required. Each
request is independent. Point your client at the URL above and select whichever of the
four tools you need:

- `get_air_quality` — current AQI for a US zip, city, or lat/lon
- `check_air_quality_threshold` — boolean exceeded flag against a max_aqi or min_category
- `find_nearby_stations` — monitoring stations near a location
- `list_aqi_categories` — the Good→Hazardous AQI band definitions

No API key is required for hosted access.

## Coverage note

Tiny Air is US-only (data source: AirNow.gov).
