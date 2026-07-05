# Ports data (safe expansion framework)

This site only ships ports that have verified coordinates (lat/lon).

## Source of truth
- `data/ports.json`

## Add ports safely
1. Add 25–50 ports per release.
2. Every port must include lat/lon (no runtime geocoding).
3. Validate with `tools/port-validator.html` (Open‑Meteo archive check).
4. Merge into `data/ports.json`.
5. Deploy a new versioned build (easy rollback).

## Display format
UI shows **Port only** (e.g., “Southampton”). Each entry is uniquely identified by id + coordinates.
