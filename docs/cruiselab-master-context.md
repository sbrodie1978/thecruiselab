# The Cruise Lab — Master Context

Last updated: 12 July 2026 (rev 12). This document is the single source of truth for The Cruise Lab initiative — every property, where it lives, how it is built and deployed. All enhancements, new tools, and maintenance work should be consistent with it; update it whenever the estate changes. Changes in rev 12: **Ocean View** (live cruise cams & free cruise video) launched at watch.thecruiselab.com with a hub card; GetMyBarTab and GetMyCruiseConnection recorded accurately as *built but never deployed* (v1 files exist only as 5 Jul chat attachments); Stuart moved to a new MacBook (fresh clones, fresh Chrome extension permissions); several hard-won lessons added (dead YouTube live embed endpoint, global pages.dev namespace, concurrent-session sandbox collisions).

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

All Cruise Lab source lives in the GitHub repo **sbrodie1978/thecruiselab** (public, as are all of Stuart's repos as of 5 Jul 2026), cloned locally at `~/cruiselab` on Stuart's MacBook (**re-cloned fresh 12 Jul 2026 on the new MacBook** — see lessons). Layout:

```
thecruiselab/
├── hub/                  → Pages project "thecruiselab"      → thecruiselab.com
├── casinopoints/         → Pages project "sys-points"        → casinopoints.thecruiselab.com
│   ├── index.html          (cruise line chooser)
│   └── princess/index.html (Sea You Soon calculator)
├── getmycruiseweather/   → Pages project "getmycruiseweather" → getmycruiseweather.com / weather.thecruiselab.com
├── oceanview/            → Pages project "oceanview"          → watch.thecruiselab.com
├── forevervoyage/        → Pages project "forever-voyage"     → forevervoyage.thecruiselab.com
└── docs/
    └── cruiselab-master-context.md   (this document)
```

Exception: Good Cabin Bad Cabin keeps its own repo, sbrodie1978/goodcabinbadcabin (also public — note its README states the underlying Princess cabin data is not licensed for redistribution; Stuart has accepted this repo being public, including the committed MSC deck-plan SVGs and PDFs). **The GCBC clone does not yet exist on the new MacBook** — re-clone to `~/goodcabinbadcabin` when next needed, and reinstall PyMuPDF for the MSC pipeline. Workflow for any change: edit in the repo folder, deploy with wrangler, then commit and push. `.wrangler/` is gitignored.

## The estate — every property, where it lives

All web properties are Cloudflare Pages projects in Stuart's Cloudflare account (login stuartfbrodie@outlook.com, account ID 9c5f5919b1ef204bd2aacf415c814cda). Both domains are registered at Namecheap with DNS hosted on Cloudflare (nameservers anuj.ns.cloudflare.com / emerie.ns.cloudflare.com). Namecheap email-forwarding MX and SPF records were preserved on both zones. A quick census of every Pages project in the account: `npx wrangler pages project list`.

### 1. The hub
- URL: https://thecruiselab.com (plus www and thecruiselab.pages.dev)
- Cloudflare Pages project: `thecruiselab`
- Repo path: `~/cruiselab/hub` (single index.html)
- Content: hero with flask mark and "The Cruise Lab" wordmark (small tracked "THE" above "CRUISE LAB"), tagline, "The Fleet" divider, one card per live tool, then an "In the Lab" divider with three named coming-soon tiles (dashed border / sea-glass chip style): **Shore Thing** (per-sailing port guides), **All Aboard Store** (curated cruise-kit shop), **GetMyCruiseMap** (keepsake route-map print). Names finalised 5 Jul 2026 (earlier working names The Kit Locker and Wake Map were replaced). Structure note: live tools sit in `<main class="fleet">`, coming-soon tiles in a following `<section class="fleet">` (only one `<main>` per page).
- Current card links (5 live tools as of 12 Jul 2026): cabins.thecruiselab.com · casinopoints.thecruiselab.com/princess/ · weather.thecruiselab.com · forevervoyage.thecruiselab.com · watch.thecruiselab.com. Ocean View's card uses a porthole icon (echoing the tool's own mark).
- WARNING (lesson from 5 Jul 2026, reinforced 12 Jul): parallel sessions editing the hub from different bases have twice caused silent overwrites/wrong deploys — before editing hub/index.html, always start from the live repo (`git pull` first), never from a possibly-stale copy in project knowledge.

### 2. Good Cabin Bad Cabin — cabin scoring
- URL: https://cabins.thecruiselab.com (plus goodcabinbadcabin.pages.dev)
- Cloudflare Pages project: `goodcabinbadcabin`
- Source: GitHub repo sbrodie1978/goodcabinbadcabin (public); **no local clone on the new MacBook yet**
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
- The Princess app is a single self-contained index.html (~15.7KB). (The old backup copy at `~/Downloads/sea-you-soon-deploy/` lived on the previous MacBook.)

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
- Design: hub navy/gold system (Cinzel + Outfit, standard tokens). Own mark: a rotating gold compass rose with a sea-glass wave. Sections: hero → sample showcase → what you get → how it works → multi-currency rate card → mailto CTA → FAQ → footer. The sample showcase is a gold-framed photo mosaic (one feature image + five tiles, hover captions), built from the sample's guaranteed-faceless scenery shots (fjord / ship / port views — rib-fjord-view, 06-ship-in-fjord, 07-funicular-view, rib-waterfall-view, 01-southampton-park, rib-2016-poster), each tile linking through to the full sample. It replaced an earlier embedded-iframe browser mock that rendered the whole site at tiny scale and looked poor. IMPORTANT: if the sample's photo set ever changes, re-check that those six mosaic filenames still exist and are face-free before relying on them, since they are hotlinked from the sample domain into the service page.
- Rate card (indicative, editable): Standard up to 7 days $99 / £79 / €95; Standard up to 14 days $199 / £159 / €189; Bespoke POA. Currency toggle (GBP default) swaps prices client-side via data-attributes. Tiers scope the labour: 7-day ~40 photos; 14-day adds scrapbook pages + video; bespoke = custom design / own domain / unlimited.
- CTA: gold "Start your journal" button = a `mailto:` with a pre-filled enquiry template. Contact address and sample URL are set once at the top of the `<script>` block (`CONTACT_EMAIL`, `SAMPLE_URL`). CTA currently points at stuartfbrodie@outlook.com (temporary). **TODO: create the `hello@thecruiselab.com` forward in Namecheap, then switch `CONTACT_EMAIL` to the branded address.**

### 5a. The Forever Voyage sample (anonymised norwaywithmum clone)
- URL: https://forever-voyage-sample.pages.dev — its own Pages project `forever-voyage-sample` (production branch `main`); the service page links to exactly this URL.
- Origin: Stuart's real norwaywithmum site (project `norwaywithmum`, live at norwaywithmum.pages.dev). Built outside the monorepo; source of truth is the live Cloudflare deployment.
- Built by a script: `build-forever-voyage-sample.py` (v4; stdlib + opencv-python; committed at the repo root). It downloads the live site, detects faces with the YuNet DNN model (cached at `~/.cache/forevervoyage/face_detection_yunet_2023mar.onnx` — cache is per-machine; the script re-downloads on first run on the new MacBook), pixelates them, anonymises names (Frances→Mum, Stuart→Son and phrase variants), disables family download links and video playback via injected CSS lockdown (not DOM removal, to avoid JS null-reference errors), rewrites the download-section copy, and outputs a deployable `./forever-voyage-sample/` folder (gitignored). The script flags photos where it found no face for manual eyeballing. Re-run any time the real norwaywithmum changes.
- Ethics note used on the service page + FAQ: the sample is Stuart's own trip, shown with his mum's blessing, names changed and faces blurred; a customer's own site is never used as an example without explicit permission.

### 6. Ocean View — live cruise cams & free cruise video (NEW, 12 Jul 2026)
- URL: https://watch.thecruiselab.com — canonical Pages URL is **oceanview-17z.pages.dev** (NOT oceanview.pages.dev, which belongs to a stranger — see lessons)
- Cloudflare Pages project: `oceanview` (production branch `main`)
- Repo path: `~/cruiselab/oceanview` (index.html + README.md; hub-card snippet kept with the delivery zips, not the repo)
- What it is: a curated player for freely available cruise video. Two sections behind a gold pill switcher: **Live** (Port Cams · Ship Cams · Ship Tracker) and **Watch** (Reviews & Tips · Golden Age). Cards open a modal player with the embed (click-to-load — nothing autoloads), or link out with an "Opens site ↗" chip. Own mark: a gold porthole with the animated sea inside (echoes the hub flask).
- **Legal posture: embed, never rehost.** YouTube via the official iframe player (creators keep views/ad revenue); Internet Archive films via archive.org's embed player; ship tracker is VesselFinder's official free embeddable map; PTZtv ports are link-out cards only (their business is ad-funded viewing on their own sites; re-streaming prohibited); cruise-line ship cams are link-out cards. Sources credited on cards, in the player and in the footer.
- **Everything is driven by one `FEEDS` array** at the top of the script — one entry per feed, four kinds: `yt-video` (one YouTube video/live stream by video id), `yt-uploads` (a channel's uploads playlist: its UC… channel id with UC→UU — plays latest videos), `archive` (archive.org item id), `link` (no embed; opens srcUrl in a new tab). Swapping a dead feed is a one-line edit.
- **Verification workflow: `?debug=1`** renders every embed plus the tracker inline on one page — the standard post-deploy sweep. All feeds and link-outs were verified live on 12 Jul 2026 (details in the tool's README, including the corrected Princess/AIDA/Viking/TUI URLs and the @Cruisewith handle gotcha).
- Content at launch: Southampton live cam (Solent Ships' 24/7 Ocean Terminal stream, pinned video id `WxdeHH9T7Yk` — if the stream rotates, get the new id from the channel's /streams page); PTZtv portfolio + six PTZtv port link cards (Canaveral, Everglades, Miami, Nassau, Paradise Island, Key West); five ship-cam link cards (Princess Bridgecams with a "Still · ~5 min" honesty chip, AIDA flagship bugcam, Viking + TUI via Cruising Earth's per-line indexes, Cruising Earth full directory); VesselFinder tracker with six region presets (Southampton default → South Florida, Caribbean, Med, Fjords, Alaska); Tips For Travellers + Emma Cruises uploads embeds; Harr Travel / La Lido Loca / Cruise With Ben and David / CruiseTipsTV link cards; three archive.org Golden Age films (Queen Mary launch at Clydebank, QE2 launch 1967, Queens of the Seas).
- Deploy: `npx wrangler pages deploy ~/cruiselab/oceanview --project-name=oceanview` then verify with `curl -sL https://oceanview-17z.pages.dev`.

### 7. Built but NOT deployed: GetMyBarTab and GetMyCruiseConnection
Both tools reached delivered v1 builds on 5 Jul 2026 but the trail then went cold: **no Pages projects exist for either** (confirmed via `wrangler pages project list` 12 Jul 2026), nothing was committed to the repo, and no hub cards were added. After the MacBook swap, the v1 files most likely exist only as attachments in the 5 Jul conversations — recover them from those chats' downloads (or rebuild) before anything else.

- **GetMyBarTab** — drinks spend predictor / bar tab tool. v1 delivered as `getmybartab-v1-20260705.html`; single-file, Cruise Lab design system. Design principle: line-blind on package prices (user brings their own quoted price); curated slowly-drifting à la carte prices per line (only Princess curated in v1); spend prediction is the hero output, not break-even comparison. Known v1 limitations: approximate fixed currency conversion; only Princess has a real package page link.
- **GetMyCruiseConnection** — WiFi/mobile/eSIM/VPN guide. v1 delivered; affiliate link infrastructure in a `LINKS` object at the top of the script (Airalo via Impact, Holafly coupon, GigSky, RedBull Mobile, VPN). Key content facts: standard travel eSIMs (Airalo, Holafly) work only on land networks (port days); GigSky (WMS Cellular at Sea) and RedBull Mobile Maritime (Telenor Maritime) are the two eSIMs that work at open sea — ship compatibility must be checked in each provider's app before purchase.
- **Path to launch for each:** recover v1 file → repo folder (`~/cruiselab/getmybartab/`, `~/cruiselab/getmycruiseconnection/`) with a README per the repo-discipline rule → create Pages project → deploy → custom subdomain (suggest bartab.thecruiselab.com / connection.thecruiselab.com — confirm names with Stuart) → hub cards → commit/push → rev 13 of this doc.

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
npx wrangler pages deploy ~/cruiselab/oceanview --project-name=oceanview
npx wrangler pages deploy ~/cruiselab/forevervoyage --project-name=forever-voyage --branch=production
```

The Forever Voyage **sample** is deployed from its generated folder (not the repo):

```bash
cd forever-voyage-sample && npx wrangler pages deploy . --project-name=forever-voyage-sample
```

After deploying, commit and push the change: `cd ~/cruiselab && git add -A && git commit -m "..." && git push`. Note the Pages projects are direct-upload type, not git-connected — pushing to GitHub does NOT auto-deploy; wrangler is the deploy mechanism.

Notes and lessons learned:
- **Production branches differ per project**: `thecruiselab` (hub), `oceanview` and `forever-voyage-sample` use `main`; `forever-voyage` uses `production`. Deploying to the wrong branch silently creates a preview deployment — the tell is an "alias URL" line in wrangler output. Verify with `curl -L` on the canonical `.pages.dev` URL after deploying.
- **pages.dev subdomains are a GLOBAL namespace** (12 Jul 2026): if a project name is taken by anyone anywhere, Cloudflare silently suffixes yours — project `oceanview` got `oceanview-17z.pages.dev`, and plain `oceanview.pages.dev` is a stranger's site. Never verify a deploy against the unsuffixed name; read the actual URL from wrangler output or the dashboard. (Same pattern seen elsewhere in the account: `signal-atlas-73z`.)
- **YouTube's `embed/live_stream?channel=<id>` endpoint is DEAD** (verified 12 Jul 2026 — embeds render "This video is unavailable"). For live cams either pin the current live **video id** (`youtube.com/embed/<videoId>`, recovery path: the channel's `/streams` page — note PTZtv's `/live` redirect goes to their airport cam, not the ports) or embed the channel's uploads playlist (`embed/videoseries?list=UU…`, i.e. channel id with UC→UU), where a 24/7 streamer's live broadcast sits at the top. Also: loading an embed URL directly in the address bar shows "Error 153 — configuration error" because there is no host-page referrer — that is NOT a broken embed; always test embeds inside a page/iframe (Ocean View's `?debug=1` exists for exactly this).
- **Concurrent Claude sessions collide — now proven in the sandbox too** (12 Jul 2026): two project conversations working on the same tool wrote to the same sandbox working folder; an early wrong-file zip got deployed before being caught, and a later patch appeared in files mid-session. Rule: **one build conversation per tool at a time**; if anything looks off, check file sizes/timestamps (`ls -la --time-style=full-iso`) before zipping, delivering or deploying, and verify the deployed title/content with `curl` after every deploy.
- **New MacBook (Jul 2026)**: nothing local survives a machine swap — repo clones (`~/cruiselab` re-cloned 12 Jul; GCBC still to re-clone), pip packages (PyMuPDF), model caches (YuNet), Downloads-folder deliverables, and the Claude-in-Chrome extension (reinstall + it prompts per-site permission on first visit to each domain). `mkdir -p` in deploy scripts can silently mask a missing clone — if `git pull` says "not a git repository", stop and re-clone before doing anything else.
- Verify a Pages project has deployments before chasing DNS/522 errors: `npx wrangler pages deployment list --project-name=X`; `npx wrangler pages project list` is the quick census of the whole estate.
- Cloudflare Pages 308-redirects `/index.html` to `/`; when curling a deployed file, always use `curl -L`.
- Wrangler deduplicates uploads by content hash — "0 files uploaded (N already uploaded)" is normal and fine.
- Old deployments remain accessible at their unique `<hash>.<project>.pages.dev` URLs (useful for recovering previous content).
- Custom domains attach to Pages projects via dashboard → project → Custom domains; DNS records are created automatically because both zones are on Cloudflare. The "up to 48 hours" banner is pessimistic — same-zone domains typically go live in a minute or two.
- iOS Safari caches deployed sites hard — fully close and reopen the tab after each deploy.

## Backlog / ideas

- **GetMyBarTab + GetMyCruiseConnection: recover v1 files from the 5 Jul chats, then deploy** (repo folders + READMEs + Pages projects + subdomains + hub cards) — see estate section 7. Follow-ups after launch: BarTab à la carte prices for more lines, better currency conversion, real package links per line.
- **Ocean View v2 ideas** (parked in its README): "Sail-away now" (surface ports with an imminent departure); favourites via localStorage; weather chip per port cam (GetMyCruiseWeather / Open-Meteo tie-in); more port cams (Galveston, Kiel, Vancouver, Funchal, Juneau — harvest their YouTube channel/video ids); more Golden Age films from archive.org; auto-detect dead embeds.
- Forever Voyage launched 5 Jul 2026 (service page + hub card + anonymised sample). Next: (1) create the `hello@thecruiselab.com` forward in Namecheap, then switch `CONTACT_EMAIL` in the service page back to the branded address; (2) later — Stripe payment links or a proper enquiry form instead of mailto; testimonials; real custom-domain option for the bespoke tier; consider a forevervoyage.com domain if the service takes off.
- **Shore Thing** (announced on hub 5 Jul 2026, not built): individual downloadable guides for each upcoming sailing across the major cruise lines — one guide per sailing, no personalisation. Per-port paragraphs stored once and reused (many sailings share ports, so content is written/generated once per port, not per sailing). Guide is presented on-screen with a download link. Each port summary carries Stuart's Viator partner link, deep-linked to that destination with tours/excursions filtered to the port day's date (commission on bookings). A prior personalised prototype (built for Steven and family) is the reference for structure/tone.
- **All Aboard Store** (formerly working name "The Kit Locker"; announced on hub 5 Jul 2026, not built): curated cruise-gear shop monetised via Amazon Associates. Categories: packing (cubes, luggage scales, compression bags), onboard cabin kit (magnetic hooks, towel clips/pegs, over-door organisers, power strips-non-surge, nightlights, lanyards), fun (cruising ducks to hide around the ship), and luggage tags/holders (line-specific e-tag holders are a classic). Catalogue to be curated before build; affiliate disclosure required on the page per Associates programme rules.
- **GetMyCruiseMap** (formerly working name "Wake Map"; announced on hub 5 Jul 2026, not built): user supplies itinerary/ship/sail date plus a few photos; tool renders a high-quality route map of the voyage with one photo per port alongside each stop (template format TBD). Output file is pushed to a print-on-demand service (Dazzle / Redbubble / CafePress or similar) for a framed print shipped to the user, with commission on the sale. Open questions: which POD service has a proper referral/API route; print resolution/aspect requirements; photo upload handling on a static-hosting estate (may need a Worker or client-side-only compositing). Market note (12 Jul): Emma Cruises promotes satellite-data cruise-route prints — an existing player worth studying before build.
- "Part of The Cruise Lab" footer badge inside the Sea You Soon Princess calculator (GCBC done 5 Jul 2026).
- GCBC data-use permissions: Stuart has written authority to proceed from **Princess, MSC, P&O and Carnival** (email replies stored). MSC launch is unblocked; P&O and Carnival are the natural next lines after MSC. Other lines still need asking before their data is used.
- GCBC / MSC: **LIVE 5 Jul 2026** at cabins.thecruiselab.com/msc/ — 24 ships, 43,479 scored cabins across 7 classes. Full build (harvest → extraction → geometry frame → 7 hand-read zone maps → scorer → payloads → app → chooser tile) done and committed. Harvest was via Claude-in-Chrome (msccruises.com/.co.uk are behind an Akamai bot wall; ALL direct HTTP 403s — use the in-page fetch + single-bundle download trick; Chrome silently blocks multi-file downloads). Everything documented in `pipeline/msc/HARVEST.md` (READ before re-harvesting: four filename schemes, refit suffixes, lazy-loading traps, the frame/orientation findings). Solved mysteries: `#003891` = Deluxe Balcony with Promenade View (World class, MANUAL_LEGEND alias); Poesia deck 11 (D'Annunzio) exists in the DAM but is absent from the site viewer (harvested separately). Open follow-ups (none blocking): (a) QUIET-AXIS CALIBRATION — reads high (most cabins 90-100) because MSC builds cabins forward and lidos aft so they rarely stack; architecturally honest but may want more discrimination once real ships are eyeballed; (b) World-class review Qs still open (outdoor promenade weight vs indoor Galleria; whether 5-deck YC cabins nearer the private pool score higher); (c) odd=Port derivation unverified vs a real onboard photo; (d) Magnifica deck 12 (Portovenere) unpublished mid-refit — re-harvest later; (e) icon TYPE decoding (accessible/whirlpool/obstructed) still to do. Remaining chooser tiles (RCI, Carnival, NCL, Celebrity, HAL, P&O, Cunard, Disney, Virgin, Costa) follow the same pattern; P&O + Carnival are next (permissions in hand).
- Casino points calculators for Carnival (Fun Play), Royal Caribbean (Casino Royale), Norwegian (Casinos at Sea) — folders under the sys-points project.
- Sea You Soon v2 ideas from original build: "What did I earn?" mode (enter final points, get the offer styled like the SYS letter); points-per-day pacing projection; link from reward stateroom tiers to Good Cabin Bad Cabin.
- Cruise industry awards: Wave Awards 2027 entries typically open Feb–Mar 2027 (judged entries ~£250+VAT per category; public-voted "Favourite Cruise Influencer" category is the accessible route). Seatrade Cruise Awards innovation categories are a possible B2B-framing fit.
- Delete the redundant Netlify projects (cruiseweatherstuart, getmycruiseweather, remarkable-cucurucho-b7209c) once comfortable.

## Working style

Stuart is technical and hands-on: he runs terminal commands himself (wrangler, curl, dig) and prefers being handed a file plus a one-liner deploy command over dashboard clicking. Output-oriented sessions; informal, direct communication. Claude may also drive his Chrome browser (Claude in Chrome extension) for dashboard work on Cloudflare/Namecheap when asked — Stuart handles all logins and password entry himself; on the new MacBook the extension prompts for per-site permission on first visit to each domain. File-delivery discipline: unique versioned filenames, one attachment per message, multi-file deliveries as a single uniquely-named zip; every tool gets a git-committed folder with a README covering what it is, where it's deployed, how to use it and how it's built. One build conversation per tool at a time.
