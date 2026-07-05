# The Cruise Lab — Master Context

Last updated: 5 July 2026 (rev 10 — merges the two 5-Jul doc forks: rev 6's Forever Voyage launch [built in a parallel session] folded into the rev 7→9 line [MSC + In the Lab tiles]; hub redeployed with the Forever Voyage card restored after the In-the-Lab deploy briefly dropped it). This document is the single source of truth for The Cruise Lab initiative. All enhancements, new tools, and maintenance work should be consistent with it. Update it when the estate changes.

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

Fonts: Cinzel (500/600/700) for headings, Outfit (300–700) for UI/body, loaded from Google Fonts. Headline treatment: gold vertical gradient text (gold-bright → gold) via background-clip. Section dividers: thin gold gradient rules with centred uppercase letterspaced labels. Cards: panel gradient background, panel-edge border, 14px radius, lift on hover with gold border. "Coming soon" cards: dashed border, sea-glass chip. Conventions: pure HTML/CSS/JS, single self-contained file per page where practical, no build step, no frameworks.

## Source of truth: the monorepo

All Cruise Lab source lives in the GitHub repo **sbrodie1978/thecruiselab** (public, as are all of Stuart's repos as of 5 Jul 2026), cloned locally at `~/cruiselab` on Stuart's MacBook. Layout:

```
thecruiselab/
├── hub/                  → Pages project "thecruiselab"      → thecruiselab.com
├── casinopoints/         → Pages project "sys-points"        → casinopoints.thecruiselab.com
│   ├── index.html          (cruise line chooser)
│   └── princess/index.html (Sea You Soon calculator)
├── getmycruiseweather/   → Pages project "getmycruiseweather" → getmycruiseweather.com / weather.thecruiselab.com
└── docs/
    └── cruiselab-master-context.md   (this document)
```

Exception: Good Cabin Bad Cabin keeps its own repo, sbrodie1978/goodcabinbadcabin (also public — note its README states the underlying Princess cabin data is not licensed for redistribution; Stuart has accepted this repo being public, including the committed MSC deck-plan SVGs and PDFs). Workflow for any change: edit in the repo folder, deploy with wrangler, then commit and push. `.wrangler/` is gitignored.

## The estate — every property, where it lives

All web properties are Cloudflare Pages projects in Stuart's Cloudflare account (login stuartfbrodie@outlook.com, account ID 9c5f5919b1ef204bd2aacf415c814cda). Both domains are registered at Namecheap with DNS hosted on Cloudflare (nameservers anuj.ns.cloudflare.com / emerie.ns.cloudflare.com). Namecheap email-forwarding MX and SPF records were preserved on both zones.

### 1. The hub
- URL: https://thecruiselab.com (plus www and thecruiselab.pages.dev)
- Cloudflare Pages project: `thecruiselab`
- Repo path: `~/cruiselab/hub` (single index.html)
- Content: hero with flask mark and "The Cruise Lab" wordmark (small tracked "THE" above "CRUISE LAB"), tagline, "The Fleet" divider, one card per live tool, then an "In the Lab" divider with three named coming-soon tiles (dashed border / sea-glass chip style): **Shore Thing** (per-sailing port guides), **All Aboard Store** (curated cruise-kit shop), **GetMyCruiseMap** (keepsake route-map print). Names finalised 5 Jul 2026 (earlier working names The Kit Locker and Wake Map were replaced). The old generic "In the Lab" flask card was replaced by this section on 5 Jul 2026. Structure note: live tools sit in `<main class="fleet">`, coming-soon tiles in a following `<section class="fleet">` (only one `<main>` per page).
- Current card links: cabins.thecruiselab.com · casinopoints.thecruiselab.com/princess/ · weather.thecruiselab.com · forevervoyage.thecruiselab.com. WARNING (lesson from 5 Jul 2026): two parallel sessions edited the hub from different bases and the In-the-Lab deploy briefly dropped the Forever Voyage card — before editing hub/index.html, always start from `~/cruiselab/hub/index.html` (or `git pull`), never from a possibly-stale copy in project knowledge.

### 2. Good Cabin Bad Cabin — cabin scoring
- URL: https://cabins.thecruiselab.com (plus goodcabinbadcabin.pages.dev)
- Cloudflare Pages project: `goodcabinbadcabin`
- Source: GitHub repo sbrodie1978/goodcabinbadcabin (public)
- What it is: scores every cabin from the deck plans — quietness, motion, convenience, space — across five traveller profiles, with a cross-section of what's above/below/beside each cabin. Princess (17 ships, ~27,500 staterooms) and MSC (24 ships, ~43,500 staterooms) are both LIVE; more lines to follow.
- Structure (since 5 Jul 2026): root index.html is a hand-maintained cruise-line chooser (Princess + MSC live; ~10 more leading lines as coming-soon tiles with hover veil — typographic tiles with brand-colour accent bars, deliberately no official logos for trademark reasons). Each line lives in its own folder: `/princess/` and `/msc/`, each holding the generated app plus `data/ship-N.json` (ship IDs restart from 1 per line; MSC 1-24 in class order, newest first). Further lines get their own folder + pipeline (P&O and Carnival next — permissions already in hand).
- Design: GCBC keeps its own identity, distinct from the hub — paper/ink utilitarian look (--ink:#122740 on --paper:#eef1ec), Saira Stencil One display, Azeret Mono labels, Hanken Grotesk body.
- Pipeline (Princess): frontend is GENERATED — edit `pipeline/build_frontend.py`, never `princess/index.html` directly. Rebuild: `fleet_build.py` → `make_payload.py` → `build_frontend.py` (stdlib Python only). Data from Princess's public deck-plan API, used with permission; refits re-harvested per `pipeline/HARVEST.md`.
- Pipeline (MSC): lives in `pipeline/msc/`. Chain (5 steps): `parse_svgs.py` (harvested SVGs + page legends → `msc_extracted.json`, gitignored: per-cabin geometry, category, ship-normalised b + side) → `msc_build.py` (scorer → `msc_scored.json`, gitignored) → `msc_payload.py` (→ `app/public/msc/data/ship-N.json` score payloads + `fleet_meta_msc.json`) → `msc_plan.py` (→ `app/public/msc/data/ship-N-plan.json` deck-plan geometry) → `msc_frontend.py` (→ `app/public/msc/index.html`). `msc_frontend.py` IMPORTS the HTML template from `build_frontend.py` (one source of truth for the app design; `build_frontend.py`'s Princess write is guarded under `if __name__=="__main__"` so importing has no side effects). Scoring model mirrors Princess (quiet/stability/convenience/space, 5 profiles) but adapted: b/side already normalised in extraction (no per-deck registration); lift positions from `CLASS_VENUE_DECKS[cls]['lift_b']`; no launderettes (MSC has none) so convenience = lifts + venues; no sqft so space = category tier + within-ship SVG footprint percentile. House rules from `msc_classes.py`: Yacht Club convenience floor (72), Aurea spa bonus (+8), promenade-view quiet penalty (-8). Category classifier + ship names/GT in `msc_categories.py`; seven class zone maps + ZONE_PEN + house-rule constants in `msc_classes.py`. IMPORTANT: each ship needs TWO data files — `ship-N.json` (scores, from msc_payload.py) AND `ship-N-plan.json` (deck-plan polygon geometry, from msc_plan.py). The frontend's "Deck plan" view fetches the plan file separately and, if it 404s, silently falls back to the whole-ship strip view with no error (this bit us: MSC shipped without plan files and the Deck plan button did nothing until msc_plan.py was added). Plan geometry is bbox rectangles from the SVG footprints, oriented forward-left / port-top; could be upgraded to true SVG-path polygons later. NOTE: MSC payloads emit a core cabin `type` at row index 18, enabling working category filtering + per-type ranking (the Princess payload doesn't populate this yet — worth backfilling). Dev-only dependency: PyMuPDF (`extract_pdftext.py`), never runs in the app. Deck-plan PDFs are committed under `data-source/msc/pdf/` as workshop source (Stuart accepted the redistribution exposure alongside the already-public SVG harvests).
- Deploy: `cd app && npx wrangler pages deploy public --project-name=goodcabinbadcabin`
- The Princess app footer now carries the "Part of The Cruise Lab" badge + disclaimer.

### 3. Casino Points (Sea You Soon) — casino comp points
- URL: https://casinopoints.thecruiselab.com (plus sys-points.pages.dev)
- Cloudflare Pages project: `sys-points`
- Repo path: `~/cruiselab/casinopoints`
- Structure: root index.html is a cruise-line chooser (Princess live; Carnival, Royal Caribbean, Norwegian shown as coming soon). Each cruise line lives in its own subfolder: `/princess/` currently hosts the Sea You Soon calculator (Princess SYS programme: voyage-length selector, optional points-so-far input, nine-tier offer ladder with free-play values, stateroom types, Princess Plus chips; point system effective 1 Sep 2025). Future lines are added as new folders (e.g. `carnival/index.html`) plus activating the matching chooser card.
- The Princess app is a single self-contained index.html (~15.7KB). A backup copy exists at `~/Downloads/sea-you-soon-deploy/index.html`.

### 4. GetMyCruiseWeather — port-by-port cruise weather
- URLs: https://getmycruiseweather.com (primary, its own consumer brand) and https://weather.thecruiselab.com (Cruise Lab alias) — both plus www and getmycruiseweather.pages.dev
- Cloudflare Pages project: `getmycruiseweather`
- Repo path: `~/cruiselab/getmycruiseweather`
- Structure: multi-file static site — index.html (port picker), results.html, js/app.js, css/styles.css, data/ports.json (ports database), assets (logos + Viator affiliate logos), tools/port-validator.html, ports_readme.md.
- Data: weather from the Open-Meteo archive API, called client-side, no API key. Google Analytics (gtag) installed. Viator affiliate links for shore excursions.
- History: migrated from Netlify on 5 Jul 2026 (was Netlify project `cruiseweatherstuart`, deployed via Netlify Drop, team "Stuart Cruise"). The Netlify project is now redundant and can be deleted. The app had real traffic at migration time (~28 requests/hour).

### 5. Forever Voyage — bespoke keepsake cruise sites (PAID SERVICE)
- URL: https://forevervoyage.thecruiselab.com (service landing page)
- Cloudflare Pages project: `forever-voyage` — NOTE its production branch is `production` (not `main`); deploy with `--branch=production` or the deploy silently lands as a preview.
- Repo path: `~/cruiselab/forevervoyage` (single self-contained index.html, ~25KB)
- What it is: The Cruise Lab's first paid offering. Stuart builds a private, bespoke "travel journal" website for a customer's own cruise — day-by-day story, scrapbook pages, downloadable photo/video bundles for the family, their own web address, hosted and kept. Same look/output as the norwaywithmum site Stuart made of his own Norway-with-mum trip on Sky Princess (the origin of the idea and the sample of the work).
- Design: hub navy/gold system (Cinzel + Outfit, standard tokens). Own mark: a rotating gold compass rose with a sea-glass wave. Sections: hero → sample showcase (framed iframe of the sample) → what you get → how it works → multi-currency rate card → mailto CTA → FAQ → footer.
- Rate card (indicative, editable): Standard up to 7 days $99 / £79 / €95; Standard up to 14 days $199 / £159 / €189; Bespoke POA. Currency toggle (GBP default) swaps prices client-side via data-attributes. Tiers scope the labour: 7-day ~40 photos; 14-day adds scrapbook pages + video; bespoke = custom design / own domain / unlimited.
- CTA: gold "Start your journal" button = a `mailto:` with a pre-filled enquiry template. Contact address and sample URL are set once at the top of the `<script>` block (`CONTACT_EMAIL`, `SAMPLE_URL`). CTA currently points at stuartfbrodie@outlook.com (temporary). **TODO: create the `hello@thecruiselab.com` forward in Namecheap, then switch `CONTACT_EMAIL` to the branded address.**

### 5a. The Forever Voyage sample (anonymised norwaywithmum clone)
- URL: https://forever-voyage-sample.pages.dev — its own Pages project `forever-voyage-sample` (production branch `main`); the service page links to exactly this URL.
- Origin: Stuart's real norwaywithmum site (project `norwaywithmum`, live at norwaywithmum.pages.dev). Built outside the monorepo; source of truth is the live Cloudflare deployment.
- Built by a script: `~/cruiselab/build-forever-voyage-sample.py` (v4; stdlib + opencv-python). It downloads the live site, detects faces with the YuNet DNN model (cached at `~/.cache/forevervoyage/face_detection_yunet_2023mar.onnx`, frontal + flipped + upscaled passes) and pixelates them, anonymises names (Frances→Mum, Stuart→Son and phrase variants), disables family download links and video playback via injected CSS lockdown (not DOM removal, to avoid JS null-reference errors), rewrites the download-section copy, and outputs a deployable `./forever-voyage-sample/` folder (gitignored). The script flags photos where it found no face for manual eyeballing. Re-run any time the real norwaywithmum changes.
- Ethics note used on the service page + FAQ: the sample is Stuart's own trip, shown with his mum's blessing, names changed and faces blurred; a customer's own site is never used as an example without explicit permission.

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
npx wrangler pages deploy ~/cruiselab/forevervoyage --project-name=forever-voyage --branch=production
```

The Forever Voyage **sample** is deployed from its generated folder (not the repo):

```bash
cd forever-voyage-sample && npx wrangler pages deploy . --project-name=forever-voyage-sample
```

After deploying, commit and push the change: `cd ~/cruiselab && git add -A && git commit -m "..." && git push`. Note the Pages projects are direct-upload type, not git-connected — pushing to GitHub does NOT auto-deploy; wrangler is the deploy mechanism.

Notes and lessons learned:
- **Production branches differ per project**: `thecruiselab` (hub) and `forever-voyage-sample` use `main`; `forever-voyage` uses `production`. Deploying to the wrong branch silently creates a preview deployment — the tell is an "alias URL" line in wrangler output. Verify with `curl -L` on the canonical `.pages.dev` URL after deploying.
- A stray `~/Downloads/wrangler.toml` triggers a harmless warning on every deploy; deleting it silences this.
- Cloudflare Pages 308-redirects `/index.html` to `/`; when curling a deployed file, always use `curl -L`.
- Wrangler deduplicates uploads by content hash — "0 files uploaded (N already uploaded)" is normal and fine.
- Old deployments remain accessible at their unique `<hash>.<project>.pages.dev` URLs and can be listed with `npx wrangler pages deployment list --project-name=<project>` (useful for recovering previous content).
- Custom domains attach to Pages projects via dashboard → project → Custom domains; DNS records are created automatically because both zones are on Cloudflare.

## Backlog / ideas

- Forever Voyage launched 5 Jul 2026 (service page + hub card + anonymised sample). Next: (1) create the `hello@thecruiselab.com` forward in Namecheap, then switch `CONTACT_EMAIL` in the service page back to the branded address; (2) later — Stripe payment links or a proper enquiry form instead of mailto; testimonials; real custom-domain option for the bespoke tier; consider a forevervoyage.com domain if the service takes off.
- **Shore Thing** (announced on hub 5 Jul 2026, not built): individual downloadable guides for each upcoming sailing across the major cruise lines — one guide per sailing, no personalisation. Per-port paragraphs stored once and reused (many sailings share ports, so content is written/generated once per port, not per sailing). Guide is presented on-screen with a download link. Each port summary carries Stuart's Viator partner link, deep-linked to that destination with tours/excursions filtered to the port day's date (commission on bookings). A prior personalised prototype (built for Steven and family) is the reference for structure/tone.
- **All Aboard Store** (formerly working name "The Kit Locker"; announced on hub 5 Jul 2026, not built): curated cruise-gear shop monetised via Amazon Associates. Categories: packing (cubes, luggage scales, compression bags), onboard cabin kit (magnetic hooks, towel clips/pegs, over-door organisers, power strips-non-surge, nightlights, lanyards), fun (cruising ducks to hide around the ship), and luggage tags/holders (line-specific e-tag holders are a classic). Catalogue to be curated before build; affiliate disclosure required on the page per Associates programme rules.
- **GetMyCruiseMap** (formerly working name "Wake Map"; announced on hub 5 Jul 2026, not built): user supplies itinerary/ship/sail date plus a few photos; tool renders a high-quality route map of the voyage with one photo per port alongside each stop (template format TBD). Output file is pushed to a print-on-demand service (Dazzle / Redbubble / CafePress or similar) for a framed print shipped to the user, with commission on the sale. Open questions: which POD service has a proper referral/API route; print resolution/aspect requirements; photo upload handling on a static-hosting estate (may need a Worker or client-side-only compositing).
- "Part of The Cruise Lab" footer badge inside the Sea You Soon Princess calculator (GCBC done 5 Jul 2026).
- GCBC data-use permissions: Stuart has written authority to proceed from **Princess, MSC, P&O and Carnival** (email replies stored). MSC launch is unblocked; P&O and Carnival are the natural next lines after MSC. Other lines still need asking before their data is used.
- GCBC / MSC: **LIVE 5 Jul 2026** at cabins.thecruiselab.com/msc/ — 24 ships, 43,479 scored cabins across 7 classes. Full build (harvest → extraction → geometry frame → 7 hand-read zone maps → scorer → payloads → app → chooser tile) done and committed. Harvest was via Claude-in-Chrome (msccruises.com/.co.uk are behind an Akamai bot wall; ALL direct HTTP 403s — use the in-page fetch + single-bundle download trick; Chrome silently blocks multi-file downloads). Everything documented in `pipeline/msc/HARVEST.md` (READ before re-harvesting: four filename schemes, refit suffixes, lazy-loading traps, the frame/orientation findings). Solved mysteries: `#003891` = Deluxe Balcony with Promenade View (World class, MANUAL_LEGEND alias); Poesia deck 11 (D'Annunzio) exists in the DAM but is absent from the site viewer (harvested separately). Open follow-ups (none blocking): (a) QUIET-AXIS CALIBRATION — reads high (most cabins 90-100) because MSC builds cabins forward and lidos aft so they rarely stack; architecturally honest but may want more discrimination once real ships are eyeballed; (b) World-class review Qs still open (outdoor promenade weight vs indoor Galleria; whether 5-deck YC cabins nearer the private pool score higher); (c) odd=Port derivation unverified vs a real onboard photo; (d) Magnifica deck 12 (Portovenere) unpublished mid-refit — re-harvest later; (e) icon TYPE decoding (accessible/whirlpool/obstructed) still to do. Remaining chooser tiles (RCI, Carnival, NCL, Celebrity, HAL, P&O, Cunard, Disney, Virgin, Costa) follow the same pattern; P&O + Carnival are next (permissions in hand).
- Casino points calculators for Carnival (Fun Play), Royal Caribbean (Casino Royale), Norwegian (Casinos at Sea) — folders under the sys-points project.
- Sea You Soon v2 ideas from original build: "What did I earn?" mode (enter final points, get the offer styled like the SYS letter); points-per-day pacing projection; link from reward stateroom tiers to Good Cabin Bad Cabin.
- Cruise industry awards: Wave Awards 2027 entries typically open Feb–Mar 2027 (judged entries ~£250+VAT per category; public-voted "Favourite Cruise Influencer" category is the accessible route). Seatrade Cruise Awards innovation categories are a possible B2B-framing fit.
- Delete the redundant Netlify projects (cruiseweatherstuart, getmycruiseweather, remarkable-cucurucho-b7209c) once comfortable.

## Working style

Stuart is technical and hands-on: he runs terminal commands himself (wrangler, curl, dig) and prefers being handed a file plus a one-liner deploy command over dashboard clicking. Output-oriented sessions; informal, direct communication. Claude may also drive his Chrome browser (Claude in Chrome extension) for dashboard work on Cloudflare/Namecheap when asked — Stuart handles all logins and password entry himself.
