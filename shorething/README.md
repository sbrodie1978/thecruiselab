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

## Sailing picker (v2) — line → ship → date

The primary way to build a guide is now a three-step picker: **cruise line →
ship → sailing date**, which resolves to a known itinerary and builds the guide
automatically. The manual port-by-port builder is still there as a secondary
option ("Don't see your sailing? Build it by hand"), unchanged.

### Data layer (designed for a clean Widgety swap later)

Three files under `data/` plus a build script:

- **`fleet.json`** — the roster: cruise lines and their ships (ids + display
  names). Populated for Princess; the other 9 Tier-1 lines are stubbed with
  empty ship arrays so they still appear in the picker (and route to manual
  entry until ships are added). Fill the ship arrays from the fleet roster.
- **`itinerary-templates.json`** — AUTHORING layer, hand-maintained. Each
  template is one repeating itinerary (ordered day-by-day port sequence +
  `nights`) plus the list of embarkation `dates` it runs on. One template
  covers dozens of sailings. Port ids must exist in `ports.json`; use
  `{"type":"sea"}` for sea days.
- **`sailings.json`** — GENERATED, do not edit. `build_sailings.py` expands each
  template's date list into individual dated sailing records. Its shape mirrors
  a Widgety cruise feed (operator + ship + sail date + duration + ordered port
  visits) on purpose.
- **`build_sailings.py`** — run after editing templates: `python3 build_sailings.py`.
  Validates every line/ship/port id against fleet.json and ports.json, refuses
  to write on error, and reports coverage.

### The swap point

The app talks to sailing data ONLY through the `SailingSource` adapter object in
`index.html` (`lines()`, `shipsForLine()`, `sailingsFor()`, `sailingById()`).
Today those read the generated `sailings.json`. To swap in a licensed live feed
(e.g. **Widgety** — the main cruise-itinerary data aggregator, API at
widgety.org, ~60+ lines, itineraries updated up to 12×/day) replace only the
adapter's internals to call the API; the rest of the app is untouched. The
`widgetyId` fields in fleet.json / templates are placeholders for mapping
Widgety operator/ship/cruise references when that happens.

### Adding itinerary coverage

1. Add the line's ships to `fleet.json` (if not already there).
2. Add itinerary templates to `itinerary-templates.json` (port sequence + dates).
3. Run `python3 build_sailings.py`.
4. Deploy. A ship with no templates still appears in the picker and routes the
   user to manual entry — no dead ends.

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
