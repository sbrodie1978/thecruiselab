# Shore Thing — Widgety integration note

**Status: PLANNED / not licensed.** This is the forward-plan for swapping Shore
Thing's self-compiled static sailing data for a live licensed feed. It exists so
the plan survives in the repo, not just in a chat. Written 15 Jul 2026.

## Why this file exists

Shore Thing v2 sources sailings from hand-authored templates
(`itinerary-templates.json`) compiled into `sailings.json` by `build_sailings.py`.
That is deliberately a **stopgap**: zero cost, survives indefinitely, but manually
maintained and only as current as the last compile. The intended long-term source
is a licensed cruise-itinerary feed. **Widgety** (widgety.org) is the leading
candidate — it aggregates itineraries, ships and ports from 60+ ocean & river
lines, updated up to 12×/day, with ports pre-mapped to exact locations.

This note records how Widgety's data model maps onto ours so that, when the swap
happens, it is a contained change to ONE object and a field-mapping layer — not a
rebuild.

## Decision context (do not lose this)

- **Model:** free keepsake guide now; pivot to a **commission-based** model in a
  few months once follower reach justifies a recurring data cost. Widgety is a
  B2B **trade** product (built for travel agents with an enquiry/booking flow),
  pricing undisclosed ("fill in the order form").
- **Trial caveat (confirmed 15 Jul 2026 from widgety.org):** the free trial is a
  **30-day trial of the embeddable Widget**, which is a *live runtime mirror* of
  Widgety content — it goes dark when the trial ends. The API Terms & Conditions
  grant a **Purpose-limited licence** to "access and use the API Data" and carry
  explicit IP-protection/infringement-cooperation clauses. Practical reading:
  **data pulled under a trial/licence may not be retained or redistributed after
  it ends.** So the trial is for *evaluation and integration testing*, NOT for
  harvesting a permanent dataset. Do not build production coverage on trial data.
- **Eligibility unknown:** the trial is offered "to agents." Whether Widgety will
  provision a consumer-facing free-tool operator (not a selling agent) is an open
  question — the first email to sales@widgety.co.uk should establish this before
  anything else. A "no" here is itself decisive and saves the trial window.
- **When to trial:** at the *start* of the commission pivot, when there is a clear
  month to integrate and act on it — not before there is audience or time. A
  30-day clock spent early is wasted.

## The swap point (already built)

The app talks to sailing data ONLY through the `SailingSource` adapter object in
`index.html`. Today its four methods read the generated `sailings.json`. To go
live, rewrite ONLY these method bodies to call the Widgety API and map the
response into our shapes. Nothing else in the app changes.

| Method | Today (static) | With Widgety |
|---|---|---|
| `load()` | fetches `fleet.json` + `sailings.json` | fetch operators+ships once (cache); sailings can be lazy per line/ship |
| `lines()` | returns `fleet.json` lines | map Widgety **operators** → `{id,name}` |
| `shipsForLine(lineId)` | ships from `fleet.json` | map operator's **ships** → `{id,name,shipClass}` |
| `sailingsFor(lineId,shipId)` | filters `sailings.json` | Widgety **cruises** request filtered by operator+ship → map to our sailing shape |
| `sailingById(id)` | finds in `sailings.json` | Widgety single **cruise** request → map |

A thin `mapWidgety*()` translation layer is the only new code. Recommend keeping
the static path behind the same adapter as a fallback (so gaps in the feed, or a
lapsed licence, degrade to manual entry rather than breaking).

## Field mapping (from Widgety's documented model → our schema)

Widgety structure (per their Cruise API docs): **operator → ship → cruise →
port-visits**, with every port "mapped to an exact location; no messy
duplications or confusing names," and port visits requestable separately from the
cruise. Version 2 of their API also includes **Non-Port Cruise Days** (their
"Cruising X" scenic days) — these map to our sea/scenic days.

### Our `fleet.json` line ← Widgety operator
| Ours | Widgety | Notes |
|---|---|---|
| `line.id` | our own slug | keep our stable slug; store their id in `widgetyId` |
| `line.name` | operator name | |
| `line.widgetyId` | operator id | **the mapping key** — fill when licensed |

### Our `fleet.json` ship ← Widgety ship
| Ours | Widgety | Notes |
|---|---|---|
| `ship.id` | our own slug | keep our slug; store their id in `widgetyId` |
| `ship.name` | ship name | |
| `ship.shipClass` | ship class/series | if provided |
| `ship.widgetyId` | ship id | **mapping key** |

### Our `sailings.json` sailing ← Widgety cruise
| Ours | Widgety | Notes |
|---|---|---|
| `id` | cruise reference | or keep composite; store theirs in `widgetyId` |
| `line` / `ship` | operator / ship id | resolve back to our slugs via the `widgetyId` maps |
| `name` | cruise/itinerary name | |
| `nights` | number of nights | |
| `embarkDate` | sail/departure date | |
| `days[]` | port-visits (ordered) | see day mapping below |
| `widgetyId` | cruise reference | |

### Day mapping — Widgety port-visit → our `days[]` entry
- Port call → `{day:N, portId:<OUR port id>}`
- Non-Port Cruise Day / sea day → `{day:N, type:"sea"}`
- **The critical join:** Widgety's port → **our `ports.json` id**. This is the
  one non-trivial mapping. Build a `widgety_port_id → shorething_port_id` lookup
  once (Widgety's exact-location mapping makes this reliable). Any unmapped
  Widgety port should fall back gracefully (render the day with no editorial,
  same as today's "notes coming" behaviour) and be logged for us to add to
  `ports.json` + `guide-content.json`. Our 302-port editorial library is keyed by
  our ids, so a good port map is what makes the whole editorial estate light up
  against live itineraries automatically.

## Concrete go-live checklist (when the pivot comes)

1. Email sales@widgety.co.uk — confirm a consumer free-tool operator can license,
   and get pricing. If no, stop; stay static or find an alternative feed.
2. Start the 30-day Widget/API trial **with dev time set aside**.
3. Capture the real API response shapes (operators, ships, cruises, port-visits)
   — save samples to `docs/` for reference. This hardens the mapping even if the
   trial then lapses.
4. Build `mapWidgety*()` + the `widgety_port_id → shorething_port_id` lookup.
5. Rewrite the four `SailingSource` methods; keep the static path as fallback.
6. Fill `widgetyId` across `fleet.json` (and stop hand-maintaining
   `itinerary-templates.json` for covered lines).
7. Validate against a spread of itineraries (jsdom smoke like the existing tests).
8. Confirm affiliate/booking posture fits Widgety's trade terms before launch.

## Sources checked (15 Jul 2026)
- widgety.org/product/cruise-api/ — data model, ports pre-mapped, port-visits separable
- widgety.org/api-terms-conditions/ — Purpose-limited licence, IP protection
- widgety.org/uses/travel-agents/ — 30-day Widget trial, agent-oriented
- widgety.org/product/widget/ — Widget is a live runtime mirror
- support.widgety.co.uk — V2 Non-Port Cruise Days
