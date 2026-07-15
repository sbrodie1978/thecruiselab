# The Cruise Lab — Master Context

Last updated: 15 July 2026 (rev 18). This document is the single source of truth for The Cruise Lab initiative — every property, where it lives, how it is built and deployed. All enhancements, new tools, and maintenance work should be consistent with it; update it whenever the estate changes. Changes in rev 18: **Shore Thing v2 — a cruise line → ship → sailing-date picker.** Instead of only typing ports and dates by hand, users now pick their **cruise line, then ship, then sailing date** and the guide builds itself; the manual port-by-port builder is kept as an understated secondary option ("Don't see your sailing? Build it by hand"). A new **data layer** underpins it, deliberately shaped so a licensed live feed can drop in later: `data/fleet.json` (roster of lines + ships), `data/itinerary-templates.json` (hand-authored repeating itineraries + date lists), `data/sailings.json` (GENERATED — do not hand-edit), and `build_sailings.py` (expands templates → dated sailings, validating every line/ship/port id). The app talks to sailing data ONLY through a `SailingSource` adapter object in index.html (`lines()`/`shipsForLine()`/`sailingsFor()`/`sailingById()`) — **the single swap point** for a future feed. **Data-sourcing decision (recorded):** build self-compiled static data now (zero recurring cost, survives indefinitely), architected so **Widgety** (the leading cruise-itinerary aggregator API) can be licensed later when a commission-based model at scale justifies the cost; the full plan, field mapping and trial caveats live in `shorething/WIDGETY-INTEGRATION.md`. Scraping third-party itinerary databases (e.g. via CruiseMapper/Apify) was considered and **rejected** — the data is compiled/terms-protected and a public named-brand tool shouldn't rest on it. To make legitimate authoring fast, `author_itinerary.py` turns a pasted itinerary (referenced from a line's own published schedule) into a validated template block, fuzzy-matching every port against `ports.json`. **Seed coverage: Princess only** (16 ships in fleet.json; 5 illustrative itinerary templates → 37 sample sailings). The other 9 Tier-1 lines are stubbed in fleet.json (empty ship arrays) so they appear in the picker and route to manual entry until ships are added. Verified by a 22-check jsdom picker smoke test + Playwright screenshots. Everything else — the 302-port database with COMPLETE editorial, the GetMyCruiseWeather backport task (still 86 `gw:false` ports + the Sydney-NS fix), the social estate, link hub, email routing, campaign — is **carried forward unchanged from rev 17**, which recorded Shore Thing editorial reaching **all 302 ports, every region**; and from rev 15: **the social estate is live and audited** under `@thecruiselabhq` (TikTok/Instagram/YouTube/Facebook), the **link hub** live at links.thecruiselab.com, and **Cloudflare Email Routing** done (`hello@`/`social@`). Standing lesson: Claude's web fetch can serve *days*-stale copies of Cruise Lab pages even with cache-busting — only Stuart's curl/browser verifies a deploy (a `?v=$(date +%s)` cache-buster on the curl also defeats it). Three link-hub plumbing facts remain **TO CONFIRM** below. *Open threads:* the 9-line **fleet roster** (being compiled via the Research feature → drops into fleet.json, no code change) and progressive **itinerary-template seeding** per ship. *Still deferred:* the Ocean View v2 write-up (YouTube harvest in progress) — the Ocean View entry is carried forward unchanged from rev 13.

## What The Cruise Lab is

The Cruise Lab (thecruiselab.com) is Stuart Brodie's umbrella brand for a collection of free web tools built for the cruising community — "free web tools built by a cruiser, for cruisers." Each tool keeps its own name and identity as a member of "The Fleet"; the hub at thecruiselab.com is the landing page from which users pick a tool. New tools and services launch under the brand and get a card on the hub, with an "In the Lab" section teasing what's next. Most of the Fleet is free; **Forever Voyage** is the first *paid, bespoke* offering — a made-to-order keepsake website built for an individual customer's cruise. All tools carry a disclaimer that they are independent and not affiliated with or endorsed by Princess Cruises or any cruise line.

## Brand and design system

The visual identity was derived from the Sea You Soon app: a "casino at sea" look — midnight navy with champagne gold, Cinzel for display type, Outfit for body text. The hub's signature mark is a gold laboratory flask containing an animated sea (navy and sea-glass waves) with a single gold bubble.

CSS tokens used across Cruise Lab properties:

```css
--ocean-deep:#081830;  --ocean:#0d2445;
--panel:#122c52;       --panel-edge:#1d3d6b;
--gold:#d9b45c;        --gold-bright:#f0d087;  --gold-dim:rgba(217,180,92,.35);
--foam:#f3efe4;        --mist:#8fa2bd;
--seaglass:#46c3a8;    --seaglass-dim:rgba(70,195,168,.18);
--radius:14px;
```

Fonts: Cinzel (500/600/700) for headings, Outfit (300–700) for UI/body, loaded from Google Fonts. Headline treatment: gold vertical gradient text (gold-bright → gold) via background-clip. Section dividers: thin gold gradient rules with centred uppercase letterspaced labels. Cards: panel gradient background, panel-edge border, 14px radius, lift on hover with gold border. "Coming soon" cards: dashed border, sea-glass chip. Conventions: pure HTML/CSS/JS, single self-contained file per page where practical, no build step, no frameworks. **Affiliate disclosure convention:** tools with affiliate links carry a discreet "may earn a commission" disclosure (GetMyCruiseConnection beside recommendation blocks + footer; Shore Thing screen-only footer line, excluded from print; link hub footer line). Keep disclosures when reworking copy; keep commission *mechanics* out of marketing copy.

## Source of truth: the monorepo

All Cruise Lab source lives in the GitHub repo **sbrodie1978/thecruiselab** (public, as are all of Stuart's repos), cloned locally at `~/cruiselab` on Stuart's MacBook. Layout:

```
thecruiselab/
├── hub/                    → Pages project "thecruiselab"          → thecruiselab.com
├── casinopoints/           → Pages project "sys-points"            → casinopoints.thecruiselab.com
│   ├── index.html            (cruise line chooser)
│   └── princess/index.html   (Sea You Soon calculator)
├── getmycruiseweather/     → Pages project "getmycruiseweather"    → getmycruiseweather.com / weather.thecruiselab.com
├── getmybartab/            → Pages project "getmybartab"           → bartab.thecruiselab.com
├── getmycruiseconnection/  → Pages project "getmycruiseconnection" → connection.thecruiselab.com
├── shorething/             → Pages project "shorething"            → shorething.thecruiselab.com
├── oceanview/              → Pages project "oceanview"             → watch.thecruiselab.com
├── forevervoyage/          → Pages project "forever-voyage"        → forevervoyage.thecruiselab.com
├── links/                  → link hub                              → links.thecruiselab.com  (folder name TO CONFIRM)
├── social/                 → idea bank, metrics, playbook, campaign, assets, promo renderer  (PLANNED — not yet created)
└── docs/
    └── cruiselab-master-context.md   (this document)
```

Exception: Good Cabin Bad Cabin keeps its own repo, sbrodie1978/goodcabinbadcabin (also public — note its README states the underlying Princess cabin data is not licensed for redistribution; Stuart has accepted this repo being public, including the committed MSC deck-plan SVGs and PDFs). **The GCBC clone does not yet exist on the new MacBook** — re-clone to `~/goodcabinbadcabin` when next needed, and reinstall PyMuPDF for the MSC pipeline. Workflow for any change: edit in the repo folder, deploy with wrangler, then commit and push. `.wrangler/` is gitignored.

## The estate — every property, where it lives

All web properties are Cloudflare Pages projects in Stuart's Cloudflare account (login stuartfbrodie@outlook.com, account ID 9c5f5919b1ef204bd2aacf415c814cda). Both registered domains are at Namecheap with DNS hosted on Cloudflare (nameservers anuj.ns.cloudflare.com / emerie.ns.cloudflare.com). **Cloudflare Email Routing is now live on the thecruiselab.com zone** (see Email routing below) — its MX/SPF records replaced the old Namecheap forwarding records. A quick census of every Pages project in the account: `npx wrangler pages project list`.

### 1. The hub
- URL: https://thecruiselab.com (plus www and thecruiselab.pages.dev)
- Cloudflare Pages project: `thecruiselab` (production branch `main`)
- Repo path: `~/cruiselab/hub` (single index.html)
- Content: hero with flask mark and "The Cruise Lab" wordmark, tagline, "The Fleet" divider with one card per live tool, then an "In the Lab" divider with coming-soon tiles (dashed border / sea-glass chip).
- **Current Fleet cards (8 live tools as of 13 Jul 2026, in order):** Good Cabin Bad Cabin (cabins.thecruiselab.com) · Sea You Soon (casinopoints.thecruiselab.com/princess/) · GetMyCruiseWeather (weather.thecruiselab.com) · Forever Voyage (forevervoyage.thecruiselab.com) · Ocean View (watch.thecruiselab.com) · GetMyBarTab (bartab.thecruiselab.com) · GetMyCruiseConnection (connection.thecruiselab.com) · Shore Thing (shorething.thecruiselab.com). Verified live in Stuart's browser 14 Jul (do NOT trust Claude-side fetches of this page — see lessons).
- **In the Lab (2 tiles):** All Aboard Store, GetMyCruiseMap.
- Structure note: live tools sit in `<main class="fleet">`, coming-soon tiles in a following `<section class="fleet">` (only one `<main>` per page).
- WARNING (repeatedly proven): before editing hub/index.html, always start from the live repo (`git pull` first), never from a possibly-stale copy in project knowledge — on 13 Jul the project-knowledge hub copy was three cards behind the live file and would have silently wiped the Ocean View, BarTab and Connection cards.

### 2. Good Cabin Bad Cabin — cabin scoring
- URL: https://cabins.thecruiselab.com (plus goodcabinbadcabin.pages.dev)
- Cloudflare Pages project: `goodcabinbadcabin`
- Source: GitHub repo sbrodie1978/goodcabinbadcabin (public); **no local clone on the new MacBook yet**
- What it is: scores every cabin from the deck plans — quietness, motion, convenience, space — across five traveller profiles, with a cross-section of what's above/below/beside each cabin. Princess (17 ships, ~27,500 staterooms) and MSC (24 ships, ~43,500 staterooms) are both LIVE; more lines to follow.
- Structure: root index.html is a hand-maintained cruise-line chooser (Princess + MSC live; ~10 more leading lines as coming-soon tiles). Each line lives in its own folder: `/princess/` and `/msc/`, each holding the generated app plus `data/ship-N.json`.
- Design: GCBC keeps its own identity, distinct from the hub — paper/ink utilitarian look (--ink:#122740 on --paper:#eef1ec), Saira Stencil One display, Azeret Mono labels, Hanken Grotesk body.
- Pipeline (Princess): frontend is GENERATED — edit `pipeline/build_frontend.py`, never `princess/index.html` directly. Rebuild: `fleet_build.py` → `make_payload.py` → `build_frontend.py` (stdlib Python only).
- Pipeline (MSC): lives in `pipeline/msc/` — five-step chain (`parse_svgs.py` → `msc_build.py` → `msc_payload.py` → `msc_plan.py` → `msc_frontend.py`); `msc_frontend.py` imports the HTML template from `build_frontend.py` (one source of truth). Each ship needs BOTH `ship-N.json` (scores) and `ship-N-plan.json` (deck-plan geometry) — a missing plan file silently falls back to the strip view. House rules in `msc_classes.py`; categories in `msc_categories.py`. Dev-only dependency: PyMuPDF. Full harvest notes in `pipeline/msc/HARVEST.md` (Akamai bot wall — Claude-in-Chrome in-page fetch + single-bundle download only).
- Deploy: `cd app && npx wrangler pages deploy public --project-name=goodcabinbadcabin`

### 3. Casino Points (Sea You Soon) — casino comp points
- URL: https://casinopoints.thecruiselab.com (plus sys-points.pages.dev)
- Cloudflare Pages project: `sys-points`
- Repo path: `~/cruiselab/casinopoints`
- Structure: root index.html is a cruise-line chooser (Princess live; Carnival, Royal Caribbean, Norwegian coming soon). `/princess/` hosts the Sea You Soon calculator (single self-contained index.html, ~15.7KB; SYS point system effective 1 Sep 2025).

### 4. GetMyCruiseWeather — port-by-port cruise weather
- URLs: https://getmycruiseweather.com (primary) and https://weather.thecruiselab.com (alias)
- Cloudflare Pages project: `getmycruiseweather`
- Repo path: `~/cruiselab/getmycruiseweather`
- Structure: multi-file static site — index.html (port picker), results.html, js/app.js, css/styles.css, data/ports.json (265 ports), assets, tools/port-validator.html.
- Data: Open-Meteo archive API, client-side, no key. Google Analytics installed. Viator affiliate links (pid=P00290711, mcid=42383).
- Results deep-link format: `results.html?port=<id>&date=YYYY-MM-DD` (+optional `region`) — Shore Thing links into this per port day.
- KNOWN DATA GAPS (audited 13 Jul during the Shore Thing build): ports.json has 49 coordinate-duplicate entries (e.g. `alicante`/`alicante_spain` — all audited as legitimate aliases) and is thin exactly where cruising is busiest — only 8 Caribbean ports, and Alaska is missing Juneau/Skagway/Ketchikan entirely. Shore Thing's `data/ports.json` contains the fix: the deduped 216 plus 44 curated top-ups (full core Caribbean incl. private islands, Alaska big six, Mexican Riviera, Galveston/Canaveral/Tampa, Bermuda, Cartagena/Colón/Puntarenas), each flagged `gw:false` — and batch 2 added another 42 (S. America, Hawaii, NZ/Pacific, Africa), also `gw:false`. **Backporting all 86 `gw:false` ports to GetMyCruiseWeather (then flipping their flags in Shore Thing) is a queued task. GetMyCruiseWeather's ports.json also has the "Sydney, Nova Scotia" filed under Oceania — fix it there too.**

### 5. GetMyBarTab — drinks spend predictor
- URL: https://bartab.thecruiselab.com (Cloudflare Pages project `getmybartab`, production branch `main`)
- Repo path: `~/cruiselab/getmybartab` (single self-contained index.html ~41KB + README)
- What it is: predicts what a cruiser will really spend on drinks — per person, split sea/port days, output styled as a literal itemised bar tab — then compares against a package price *the user supplies*.
- CORE DESIGN PRINCIPLE (do not break): **line-blind on package prices** — never store or guess a package price; the user pastes their quoted per-person/per-day number. What we curate is slow-moving à la carte per-drink pricing: `GENERIC_PRICES` fallback + per-line `LINES` overrides at the top of the `<script>` (only Princess individually curated in v1, incl. 18% service charge and the only real `pkgUrl`). `PRICE_STAMP` shows the curation date in the UI — update it whenever prices refresh (currently "July 2026").
- History: v1 built 5 Jul 2026, recovered from chat attachments and deployed 12 Jul 2026 after the MacBook swap. Hub card live.

### 6. GetMyCruiseConnection — WiFi, roaming & eSIM guide
- URL: https://connection.thecruiselab.com (Cloudflare Pages project `getmycruiseconnection`, production branch `main`) — custom domain confirmed **Active / SSL enabled** in the dashboard 13 Jul 2026.
- Repo path: `~/cruiselab/getmycruiseconnection` (single self-contained index.html ~42KB + README)
- What it is: decodes staying connected on a cruise — what works at open sea vs port days, ship WiFi vs roaming vs travel eSIMs, with affiliate-linked recommendations.
- Affiliate infrastructure: all partner URLs in one `LINKS` object at the top of the `<script>` (Airalo via Impact, Holafly coupon, GigSky, RedBull Mobile, VPN pick). `rel="sponsored"` added in the JS card templates; "Partner links — we may earn a small commission" disclosure beside every recommendation block and in the footer — keep disclosures if copy is reworked.
- Key content facts: standard travel eSIMs (Airalo, Holafly) work only on land networks (port days); GigSky (WMS Cellular at Sea) and RedBull Mobile Maritime (Telenor Maritime) are the two eSIMs that work at open sea — ship compatibility must be checked in each provider's app before purchase; Starlink fleet-wide rollout makes ship WiFi the primary sea-day recommendation.
- History: v1 built 5 Jul, iterated to v3 6 Jul 2026 (deployed version), recovered and deployed 12 Jul 2026. Hub card live.

### 7. Shore Thing — port guides for your exact sailing
- URL: https://shorething.thecruiselab.com (canonical Pages URL shorething.pages.dev — unsuffixed name secured)
- Cloudflare Pages project: `shorething` (production branch `main` — the project was first created interactively with branch `production` by mistake, then deleted and recreated correctly; see lessons)
- Repo path: `~/cruiselab/shorething` (index.html + data/ports.json + data/guide-content.json + **data/fleet.json + data/itinerary-templates.json + data/sailings.json** + build_sailings.py + author_itinerary.py + README + WIDGETY-INTEGRATION.md)
- What it is: the user enters their cruise ports in order with dates (optional ship/cruise name) and gets a port-by-port guide for that exact sailing — editorial blurb, quick-fact chips (docked/tender, walkability, currency, language), a "Don't miss" list and a "Lab note" tip per port, plus per-day **Viator** tours link and **GetMyCruiseWeather** weather link. Date gaps render as "at sea" interstitials on a gold route-ribbon timeline. Guide can be read on screen, printed (print stylesheet flips to a paper "ship's programme" look) or downloaded as a standalone self-contained HTML file. Itinerary persists in localStorage (`shorething-sailing-v1`).
- **v2 sailing picker (primary input):** three dependent dropdowns — **cruise line → ship → sailing date** — resolve to a known itinerary and build the guide automatically; a sea-glass preview card shows the route before building. The manual builder above is now the *secondary* path (understated "Don't see your sailing? Build it by hand" link; mode-switch both ways). A picker selection resolves to the same `[{id,date}]` array the manual builder produces and calls the SAME `buildGuide()` — the guide engine, editorial, affiliate/weather links, print and download are unchanged. Fallbacks with no dead ends: a line with no ships, or a ship with no sailings, routes the user to manual entry.
- **Data layer (Widgety-swap-ready):** `data/fleet.json` = roster of lines + ships (Princess populated with 16 ships; 9 other Tier-1 lines stubbed with empty `ships:[]`). `data/itinerary-templates.json` = AUTHORING layer, hand-maintained: each template is one repeating itinerary (ordered day-by-day port sequence + `nights`) plus the `dates` it runs; one template covers many sailings. `data/sailings.json` = GENERATED, do not hand-edit. `build_sailings.py` expands templates → individual dated sailings (Widgety-shaped), validating every line/ship/port id and refusing to write on error (`python3 build_sailings.py`). The app reads sailing data ONLY via the `SailingSource` adapter object in index.html — **the single swap point**: replace those four methods' internals to call a licensed feed later, nothing else changes. `widgetyId` placeholder fields are threaded through fleet/templates for that mapping. Seed: 5 Princess templates → 37 sailings.
- **Authoring helper:** `author_itinerary.py` — paste a day-by-day itinerary (referenced from a cruise line's OWN published schedule), it fuzzy-matches each port against `ports.json`, auto-detects sea days, flags anything it can't match confidently, and emits a ready-to-paste template block. Speeds up legitimate hand-authoring; does NOT fetch or scrape. (Bulk-scraping aggregator itinerary DBs was rejected — see WIDGETY-INTEGRATION.md and the header.)
- Data: `data/ports.json` — **302 ports** (`gw` flag controls the weather link). Built in two passes: the original 260 (GetMyCruiseWeather's 265 deduped to 216 + 44 top-ups) plus **batch 2's 42 additions** on 15 Jul — the southern-South-America circuit (Buenos Aires→Ushuaia, Punta Arenas, Valparaíso, Callao, Falklands), all four Hawaiian islands, seven NZ ports, the South Pacific (Fiji, Nouméa, Vanuatu, Tahiti/Moorea/Bora Bora, Pago Pago), Adelaide/Darwin/Whitsundays, and Africa/Indian Ocean (Cape Town, Durban, Port Elizabeth, Walvis Bay, Mombasa, Mauritius, Seychelles). All batch-2 ports are `gw:false`. A misfiled "Sydney, Nova Scotia" was moved from Oceania → North America (same bug still lives in GetMyCruiseWeather's ports.json — see backlog). `data/guide-content.json` — editorial keyed by port id; schema in the tool README; `"noviator":true` suppresses the Viator button (used for the 8 private islands, which have no independent tours). Ports without editorial render gracefully (links still work, quiet "notes coming" line).
- **Editorial coverage: COMPLETE — all 302 ports, every region (302 entries as of 15 Jul).** Written in batches: Americas first, then Europe (three sub-region batches), then the final push covering Asia (67), Oceania (27), the South American southern circuit, Hawaii, and Africa. River-cruise/inland calls (Lyon, Vienna, Verona, Chiang Mai, Beijing/Tianjin) are framed honestly as transfers/fly-ins, not walk-off ports; the duplicate id pairs (Edinburgh Leith + South Queensferry, Livorno/Florence ×2, Porto ×2, Cadiz/Seville) each have their own entry. **Standing lesson for future edits: always validate every editorial key against `ports.json` before merging** — across the batches, four invented/duplicate keys were caught this way (Dartmouth, Santander, Koper→`ljubljana-koper`, and `koh-chang`→`trat-koh-chang`) and removed. Adding a new port now means adding both a `ports.json` record and a `guide-content.json` entry.
- Affiliate: Viator links via `viatorUrl()` in index.html — same pid/mcid as GetMyCruiseWeather, plus `startDate`/`endDate` set to the port date. Screen-only footer disclosure line.
- Verified at launch by jsdom smoke test (23/23); v2 picker verified by a 22-check jsdom smoke test + Playwright screenshots.
- Deploy: `npx wrangler pages deploy ~/cruiselab/shorething --project-name=shorething` — after editing `itinerary-templates.json`, run `python3 build_sailings.py` first (regenerates sailings.json). Note: `sailings.json` edge-caches hard — verify with a `?v=$(date +%s)` cache-buster (a 0 count immediately post-deploy is edge lag, not failure).

### 8. Ocean View — live cruise cams & free cruise video
- URL: https://watch.thecruiselab.com — canonical Pages URL is **oceanview-17z.pages.dev** (NOT oceanview.pages.dev, a stranger's site)
- Cloudflare Pages project: `oceanview` (production branch `main`)
- Repo path: `~/cruiselab/oceanview` (index.html + README.md)
- What it is: curated player for freely available cruise video — Live (Port Cams · Ship Cams · Ship Tracker) and Watch (Reviews & Tips · Golden Age) behind a gold pill switcher; modal player, click-to-load embeds, link-out cards with "Opens site ↗" chips. [v2 rebuild — Harbour Board, per-port local time, Ships review section — is deployed but its write-up is deferred until the YouTube harvest completes.]
- Legal posture: **embed, never rehost** — YouTube iframe player, archive.org embeds, VesselFinder's official embeddable map; PTZtv and cruise-line cams are link-out only. Sources credited.
- Everything driven by one `FEEDS` array (kinds: `yt-video`, `yt-uploads`, `archive`, `link`); swapping a dead feed is a one-line edit. Post-deploy sweep: `?debug=1` renders every embed inline. YouTube `embed/live_stream?channel=` is DEAD — pin video ids or use UC→UU uploads playlists (details in the tool README).
- Deploy: `npx wrangler pages deploy ~/cruiselab/oceanview --project-name=oceanview` then curl oceanview-17z.pages.dev.

### 9. Forever Voyage — bespoke keepsake cruise sites (PAID SERVICE)
- URL: https://forevervoyage.thecruiselab.com (curl-verified 200 by Stuart, 14 Jul)
- Cloudflare Pages project: `forever-voyage` — NOTE production branch is `production`; deploy with `--branch=production` or the deploy silently lands as a preview.
- Repo path: `~/cruiselab/forevervoyage` (single self-contained index.html, ~25KB)
- What it is: The Cruise Lab's first paid offering — a private, bespoke "travel journal" website of a customer's own cruise (day-by-day story, scrapbook pages, downloadable bundles, own web address, hosted and kept), modelled on Stuart's norwaywithmum site.
- Rate card (indicative): Standard up to 7 days $99 / £79 / €95; up to 14 days $199 / £159 / €189; Bespoke POA. Currency toggle client-side.
- CTA: `mailto:` with pre-filled template; `CONTACT_EMAIL` and `SAMPLE_URL` set at the top of the `<script>`. **`CONTACT_EMAIL` is now `hello@thecruiselab.com`** — confirmed in the repo file 14 Jul (grep). *Verify the live deploy carries it:* `curl -sL https://forevervoyage.thecruiselab.com/ | grep -o "hello@thecruiselab.com" | head -1` — if empty, redeploy with `--branch=production`.
- Sample: https://forever-voyage-sample.pages.dev (own Pages project `forever-voyage-sample`, branch `main`), generated by `build-forever-voyage-sample.py` (v4; YuNet face pixelation, name anonymisation, download/video lockdown; model cache is per-machine and re-downloads on first run). Re-run whenever the real norwaywithmum changes; re-check the six hotlinked mosaic filenames still exist and are face-free.

### 10. Link hub — links.thecruiselab.com (LIVE, 14 Jul 2026)
- URL: https://links.thecruiselab.com — verified live: Cruise Lab-styled bio-link page, all 8 Fleet tools as buttons in hub order, Forever Voyage under a "Made to order" divider, "Everything at thecruiselab.com" line, independence + affiliate disclosure footer.
- Built in the deleted 14 Jul session. **TO CONFIRM (lost with that chat): Pages project name, repo folder (assumed `~/cruiselab/links`), production branch.** Recover with `npx wrangler pages project list` + `ls ~/cruiselab`; if the folder is missing from the repo, pull the live page down and commit it.
- Purpose: the bio link on every social platform. Queued enhancement: append the inbound `?src=` parameter to every outbound tool button (see campaign doc, Phase 0) so tool footfall can be attributed per platform.

## Social media

The Cruise Lab's social presence is **live** (accounts created 14 Jul 2026; much of the setup was done in a deleted chat — this section is the reconstruction of record). Positioning: a **data brand**, not a travel vlog — *"the account that runs the numbers on cruising."* Every post is a finding, verdict, ranking or myth-bust drawn from the estate's own data. Fully **faceless** — the gold flask is the face. Goal priority: 1) follower & view growth, 2) traffic to the tools, 3) affiliate revenue, 4) Forever Voyage leads. Time budget: 3–5 hrs/week.

### Live accounts (audited 14 Jul 2026)

| Platform | Identity | Status |
|---|---|---|
| YouTube | youtube.com/channel/UC_VM812P4JtvtqZkF3YN9Xg · handle @thecruiselabhq | ✅ Correct: name "The Cruise Lab", on-message about text, bio link → links.thecruiselab.com |
| Instagram | instagram.com/thecruiselabhq | ✅ Correct: name, roundel avatar, emoji bio, link → links.thecruiselab.com |
| Facebook | facebook.com/thecruiselabhq (page id 61591669721543) | ✅ Correct: **username set 14 Jul** (was numeric-only), bio emoji repaired 14 Jul, banner/avatar/website link in place, Instagram account linked |
| TikTok | tiktok.com/@thecruiselabhq | ⚠️ Handle, roundel avatar and emoji bio correct. **Two open fixes:** display name is still `thecruiselabhq` (must be "The Cruise Lab"; TikTok allows one name change per 7 days); no website link (locked until 1k followers on a standard account — **switch to Business account** to unlock the link field + analytics; trade-off is the commercial sound library, immaterial for the faceless format) |
| Pinterest, X, Threads, Bluesky | — | Not yet created — Phase 0 of the campaign doc |

- **Handle everywhere: `@thecruiselabhq`; display name everywhere: "The Cruise Lab."** Bluesky can later become `@thecruiselab.com` via DNS TXT (free verification).
- **Bio (all platforms):** ⚓ The account that runs the numbers on cruising 🧪 Cabin scores · bar tabs · casino points · port guides 🔗 All free ↓ — link: links.thecruiselab.com. (Facebook's bio emoji were pasted as `�` at creation; repaired 14 Jul — check emoji survive any future bio edits.)
- **Platform tiers:** Tier 1 (growth engine, identical short-form video) = TikTok · Instagram Reels · YouTube Shorts. Tier 2 = Facebook Page + Reels, Pinterest. Tier 3 (parked) = X · Threads · Bluesky; Reddit is listen/participate-only. Not doing: long-form YouTube, livestreams, paid ads.
- **Content pillars → Fleet mapping:** P1 Cabin Verdicts (GCBC — flagship) · P2 The Bar Tab (GetMyBarTab) · P3 Connected at Sea (GetMyCruiseConnection) · P4 Port Intel (Shore Thing + GetMyCruiseWeather) · P5 Casino Points & Cruise Maths (Sea You Soon). Series names: *Cabin Court*, *The Tab*, *Lab Report*, *Port File*.
- **Strategy documents (two-layer):**
  - `cruiselab-social-playbook-v1-20260713.md` — the *how*: positioning, platform strategy, pillars, format recipes (F1 The Verdict … F6 Tool Demo, max 1 in 6), hook library, weekly production system, funnel, metrics, 90-day plan.
  - `cruiselab-launch-campaign-v1-20260714.md` — the *what and when*: Phase 0 housekeeping (remaining accounts, TikTok fixes, `?src=` UTM tagging of every bio link, Cloudflare Web Analytics across the estate, `social/` folder), Phase 1 launch week (Day 1 = intro video posted natively + pinned everywhere, with per-platform captions; Days 2–7 = first four-video batch with specified hooks; Day 7 = Pinterest seeding), Phase 2 standing cadence with a 90-day rebalancing gate, ready-to-adapt message library, and the `metrics.md` template. **The campaign's scoreboard is bio-link clicks by `src` and tool sessions, not views.**
- **Brand assets:** avatar/banner pack `cruiselab-social-assets-v1-20260714.zip` (roundel avatar, per-platform banners, editable SVG masters) — deployed on all four live platforms.
- **Intro promo video:** `cruiselab-intro-promo-v1-20260714.mp4` — 40s, 1080×1920 (9:16), 30fps, silent, ~1MB. Fully animated in the design system: hook → "Meet Sarah" → three phone-POV chapters (01 The Cabin / GCBC in its paper-ink identity · 02 The Bar Tab · 03 The Ports) → SCORED. TALLIED. DECODED. ALL FREE. → flask end card + thecruiselab.com. Built with a single-file Python renderer (`render.py`, PIL + ffmpeg; Cinzel/Outfit variable TTFs fetched from the google/fonts GitHub repo) — re-render for copy tweaks or other aspect ratios with one command. Renderer + video belong in the `social/` folder when created. This is the campaign's Day-1 pinned post on every platform.
- **Operating rules (short form):** faceless always; one idea per video; hook in 2 seconds, brand only at the end; max 1 tool demo in 6 posts; same handle/avatar/voice everywhere; reply to comments in the first hour; batch weekly; every claim backed by the estate's data; disclosures live on-site, never commission talk in content; saves & shares are the growth currency.

### Email routing (DONE — Cloudflare Email Routing, 14 Jul 2026)
Live on the thecruiselab.com zone, both addresses forwarding to stuartfbrodie@outlook.com:
- **hello@thecruiselab.com** — public/customer address; Forever Voyage's `CONTACT_EMAIL` now points at it (repo confirmed; verify live deploy — see the Forever Voyage entry).
- **social@thecruiselab.com** — social platform signups only, keeping recovery/notification mail separate and filterable. Use it for the Phase 0 account creations (Pinterest, X, Bluesky).
Cloudflare's MX/SPF/DKIM records replaced the old Namecheap forwarding records on the zone (nothing live was lost — no working forward had ever been configured). Forwarding-in is all that's needed; sending *from* these addresses would need extra setup and isn't required.

## Deployment workflow (standard for all projects)

Deploys are done from Stuart's MacBook terminal with wrangler:

```bash
npx wrangler pages deploy <folder> --project-name=<project>
```

Standard deploys from the repo:

```bash
npx wrangler pages deploy ~/cruiselab/hub --project-name=thecruiselab
npx wrangler pages deploy ~/cruiselab/casinopoints --project-name=sys-points
npx wrangler pages deploy ~/cruiselab/getmycruiseweather --project-name=getmycruiseweather
npx wrangler pages deploy ~/cruiselab/getmybartab --project-name=getmybartab
npx wrangler pages deploy ~/cruiselab/getmycruiseconnection --project-name=getmycruiseconnection
npx wrangler pages deploy ~/cruiselab/shorething --project-name=shorething
npx wrangler pages deploy ~/cruiselab/oceanview --project-name=oceanview
npx wrangler pages deploy ~/cruiselab/forevervoyage --project-name=forever-voyage --branch=production
# link hub: project name / folder TO CONFIRM — add its line here once recovered
```

The Forever Voyage **sample** is deployed from its generated folder: `cd forever-voyage-sample && npx wrangler pages deploy . --project-name=forever-voyage-sample`.

After deploying, commit and push: `cd ~/cruiselab && git add -A && git commit -m "..." && git push`. Pages projects are direct-upload type — pushing to GitHub does NOT auto-deploy.

Notes and lessons learned:
- **Claude's web fetch of Cruise Lab pages can be DAYS stale (proven 14 Jul 2026):** Anthropic-side fetches of thecruiselab.com returned a ~9-day-old 4-card hub even with a cache-busting query string, and returned 522 for a Forever Voyage page that curl'd 200 from Stuart's machine. **Never use Claude's fetch to verify (or panic about) a deploy — Stuart's curl/browser is canonical.** Claude-side fetch is fine for reading page *content* when freshness doesn't matter.
- **Creating a new Pages project:** the command is `npx wrangler pages project create <name> --production-branch=main` — NOT `wrangler pages create`. If the flag is omitted and wrangler falls into its interactive prompt, the prompt's suggested branch is `production`, which recreates the Forever Voyage trap; if that happens before anything is deployed, delete (`wrangler pages project delete <name>`) and recreate rather than living with it.
- **Never run `wrangler pages deploy` from `~`**: without a directory argument it tries to upload the current working directory — from home it dies on `~/.Trash` with a permissions error. Always pass the explicit folder path.
- **Production branches differ per project**: everything uses `main` except `forever-voyage` (`production`). Deploying to the wrong branch silently creates a preview — the tell is an "alias URL" line in wrangler output. Verify with `curl -L` on the canonical `.pages.dev` URL after deploying.
- **pages.dev subdomains are a GLOBAL namespace**: if a name is taken by anyone anywhere, Cloudflare silently suffixes yours (project `oceanview` → oceanview-17z.pages.dev). Read the actual URL from wrangler output; never verify against an assumed name.
- **Custom domain attachment**: dashboard → project → Custom domains → Set up → enter domain → Continue → **Activate domain**. The definitive success check is the domain appearing in the list on the project's `/domains` page (status Initializing → Verifying → Active, ~1–2 minutes for same-zone).
- **Facebook page setup quirks (14 Jul 2026):** a brand-new page has NO username — facebook.com/<name> shows "content isn't available" until one is set at Settings → General Page settings → Username (Facebook demands a password re-entry to save). Emoji pasted into the bio can save as `�` — re-paste and re-check after saving.
- **Concurrent Claude sessions collide** — one build conversation per tool at a time; check file sizes/timestamps before zipping or deploying; curl-verify deployed title/content after every deploy (Stuart-side).
- Verify a project has deployments before chasing DNS/522 errors: `npx wrangler pages deployment list --project-name=X`; `npx wrangler pages project list` is the estate census.
- Cloudflare Pages 308-redirects `/index.html` to `/` — always `curl -L`.
- Wrangler dedupes uploads by content hash — "0 files uploaded (N already uploaded)" is normal.
- Old deployments remain at their `<hash>.<project>.pages.dev` URLs (useful for recovery).
- Mac local DNS caching: `curl --resolve domain:443:IP` bypasses the OS resolver; Chrome's Secure DNS is independent of the OS resolver (curl-200-but-Chrome-blank is a known non-failure).
- iOS Safari caches deployed sites hard — fully close and reopen the tab after each deploy.
- Claude-in-Chrome: extension prompts per-site permission on first visit per domain; the bridge drops when idle — reopening the Chrome side panel wakes it. Facebook/Instagram/TikTok block Claude's server-side fetch entirely — account reviews must go through Claude-in-Chrome (proven 14 Jul).

## Backlog / ideas

- **Campaign Phase 0 (next session, ~1 hr — see campaign doc):** TikTok display name → "The Cruise Lab" + switch to Business account + add website link; create Pinterest Business (claim domain via DNS TXT, five pillar boards) / X (park) / Bluesky (park; later @thecruiselab.com handle via DNS TXT) / Threads (inherits from Instagram); set `?src=` tagged bio links per platform.
- **Link hub `src` pass-through:** small JS addition so the hub forwards its inbound `?src=` on every outbound tool button — makes per-platform footfall attributable. (First: recover the link hub's plumbing — see estate entry 10.)
- **Cloudflare Web Analytics across the estate:** add the snippet to every Pages project so tool sessions are measurable (only GetMyCruiseWeather currently has any analytics).
- **`social/` folder in the monorepo:** playbook + campaign doc + `ideas.md` (seed 30 ideas, 6 per pillar) + `metrics.md` + asset pack + promo video & renderer. Then begin the weekly batch cadence (Phase 1 of the campaign).
- **Verify Forever Voyage live deploy carries `hello@`** (one grep — see estate entry 9).
- **Shore Thing editorial: COMPLETE** (all 302 ports have entries). Adding a new port needs both a `ports.json` record and a validated `guide-content.json` entry.
- **Shore Thing v2 open threads:** (1) **Fleet roster** — 9 remaining Tier-1 lines (Royal Caribbean, Carnival, Norwegian, MSC, Celebrity, Holland America, Costa, Disney, Virgin Voyages) being compiled via the Research feature; drops into `fleet.json` `ships[]` arrays, no code change, then the pickers light up. (2) **Itinerary-template seeding** — currently Princess-only (5 templates); author more per ship/line using `author_itinerary.py` from lines' own published schedules, then `build_sailings.py`. (3) **Known gap:** the Norway/North-Cape ports (Skjolden, Hardangerfjord, Trondheim, Honningsvåg, Tromsø, Molde) are NOT yet in `ports.json` — needed before real Sky Princess fjord/North-Cape sailings can be added; add ports + editorial first. (4) **Widgety** — license at the commission pivot; plan in `shorething/WIDGETY-INTEGRATION.md`.
- **Backport Shore Thing's 86 `gw:false` top-up ports to GetMyCruiseWeather**, then flip their `gw` flags to true in Shore Thing. Also fix the "Sydney, Nova Scotia" region misfile (Oceania → North America) in GetMyCruiseWeather's own ports.json.
- **GetMyBarTab follow-ups**: à la carte prices for more lines beyond Princess; better currency conversion; real package links per line.
- **Ocean View v2 write-up** for this doc once the YouTube harvest completes; v2 ideas parked in its README ("Sail-away now"; favourites; weather chip per port cam; more port cams; more Golden Age films; dead-embed detection).
- **Forever Voyage next**: Stripe payment links or a proper enquiry form instead of mailto; testimonials; real custom-domain option for the bespoke tier; consider forevervoyage.com if the service takes off.
- **All Aboard Store** (announced on hub, not built): curated cruise-gear shop via Amazon Associates. Catalogue to curate before build; affiliate disclosure required per Associates rules.
- **GetMyCruiseMap** (announced on hub, not built): itinerary + photos → keepsake route-map print via print-on-demand. Open questions: POD referral/API route; print resolution; photo handling on static hosting. Market note: Emma Cruises promotes satellite-data cruise-route prints — study before build.
- "Part of The Cruise Lab" footer badge inside the Sea You Soon Princess calculator (GCBC done).
- GCBC data-use permissions: written authority from **Princess, MSC, P&O and Carnival**. P&O + Carnival are the natural next lines.
- GCBC / MSC open follow-ups (none blocking): quiet-axis calibration; World-class review questions; odd=Port verification; Magnifica deck 12 re-harvest post-refit; icon TYPE decoding. Princess payload: backfill cabin `type` at row index 18.
- Casino points calculators for Carnival (Fun Play), Royal Caribbean (Casino Royale), Norwegian (Casinos at Sea) — folders under sys-points.
- Sea You Soon v2 ideas: "What did I earn?" mode; points-per-day pacing; link reward stateroom tiers to GCBC; footer badge.
- "My Cruise" anonymous cross-subdomain profile via `.thecruiselab.com` cookie — scoped, sequenced after current backlog; note getmycruiseweather.com cannot share the cookie (separate domain).
- Cruise industry awards: Wave Awards 2027 entries open Feb–Mar 2027; Seatrade innovation categories a possible B2B fit.
- Delete the redundant Netlify projects (cruiseweatherstuart, getmycruiseweather, remarkable-cucurucho-b7209c) once comfortable.
- Delete the stale clone at `~/Projects/goodcabinbadcabin` if still present.

## Working style

Stuart is technical and hands-on: he runs terminal commands himself (wrangler, curl, dig) and prefers being handed a file plus a one-liner deploy command over dashboard clicking. Output-oriented sessions; informal, direct communication. Claude may also drive his Chrome browser (Claude in Chrome extension) for dashboard and social-platform work when asked — Stuart handles all logins and password entry himself (Facebook demands password re-entry for username changes — always hand over at that point); the extension prompts for per-site permission on first visit to each domain. File-delivery discipline: unique versioned filenames, one attachment per message, multi-file deliveries as a single uniquely-named zip; every tool gets a git-committed folder with a README covering what it is, where it's deployed, how to use it and how it's built. One build conversation per tool at a time. **When a chat is lost/deleted, its outcomes are lost from Claude's memory — reconstruct into this doc promptly; this doc and the repo are the only durable records.**
