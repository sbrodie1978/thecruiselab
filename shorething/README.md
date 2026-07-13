# Shore Thing

Port guides for your exact sailing — part of **The Cruise Lab** (thecruiselab.com).

## What it is

A free client-side tool: the user enters their cruise ports in order with dates,
and Shore Thing builds a port-by-port guide for that exact sailing — editorial
notes, quick facts, a "don't miss" list and a Lab tip per port, plus a
tours/excursions link (Viator) and a weather link (GetMyCruiseWeather) for each
port day. Gaps between dates render as "at sea" days on the route ribbon.

The guide can be:
- read on screen,
- printed / saved as PDF (a print stylesheet flips it to a paper-friendly
  "ship's programme" look), or
- downloaded as a standalone self-contained HTML file to take offline.

## Where it's deployed

- Cloudflare Pages project: `shorething` (production branch: `main`)
- Suggested custom domain: `shore.thecruiselab.com` (see monorepo master
  context doc for the estate's domain map)

Deploy from this folder:

    npx wrangler pages deploy . --project-name=shorething

Then curl the canonical `shorething.pages.dev` URL to confirm the deploy landed
on production (an `alias URL: <branch>.shorething.pages.dev` line in the
wrangler output means it went to a preview branch instead).

## How it's built

- Single self-contained `index.html` (no build step, no dependencies) in the
  house design system: midnight navy / champagne gold tokens, Cinzel display +
  Outfit body, `.panel` / `.eyebrow` / `.rule` / `.btn` patterns shared with
  the hub.
- Two data files fetched at load:
  - `data/ports.json` — 260 ports: the GetMyCruiseWeather port list, deduped
    from 265 to 216 (coordinate-based; alias entries like `alicante` /
    `alicante_spain` merged), plus 44 top-up ports GetMyCruiseWeather lacks
    (core Caribbean, private islands, Alaska, Mexican Riviera, US homeports).
    Each port: `{id, name, lat, lon, region, gw}`.
    `gw: true` means the id exists in GetMyCruiseWeather, so the per-day
    weather link is shown; `gw: false` suppresses it. Top-ups can be
    backported to GetMyCruiseWeather later (see `build_ports.py` history in
    the monorepo if regenerating).
  - `data/guide-content.json` — editorial keyed by port id. Ports without an
    entry still render gracefully (name, date, Viator + weather links, and a
    quiet "port notes coming" line).
- Itinerary state persists in `localStorage` under `shorething-sailing-v1`.

## Editorial schema

    "port_id": {
      "dock":  "Docked" | "Tender" | free text,     // highlighted chip
      "walk":  "Walkable downtown",                  // chip
      "cur":   "XCD / USD",                          // chip
      "lang":  "English",                            // chip
      "blurb": "Two sentences on the port.",
      "miss":  ["thing one", "thing two", "thing three"],
      "tip":   "One genuinely useful Lab note.",
      "noviator": true                               // optional — suppresses the
    }                                                //  Viator button (private islands)

Coverage as of v1: the Americas (76 entries — full Caribbean incl. private
islands, Bermuda, Mexico, Central America, Alaska, US/Canada homeports,
Greenland, Brazil). Europe, Asia, Oceania and Africa batches to follow — just
add entries to `guide-content.json`; no code changes needed.

## Affiliate links

Viator links are built in `viatorUrl()` in `index.html`:
`https://www.viator.com/searchResults/all?text=<port>&pid=P00290711&mcid=42383&medium=link`
plus `startDate`/`endDate` set to the port date. The pid/mcid pair matches the
rest of the estate (same as GetMyCruiseWeather). A discreet affiliate
disclosure line sits in the site footer (screen only, excluded from print).

## Testing

`smoke.js` (jsdom) in the build session exercised: port search/autocomplete,
stop ordering and dates, sea-day interstitials, day numbering, noviator
suppression, gw-flag weather links, affiliate URL construction, localStorage
persistence, and the standalone HTML download. 23/23 behaviours verified.
