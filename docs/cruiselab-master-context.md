# The Cruise Lab — Master Context

Last updated: 14 July 2026 (rev 14). This document is the single source of truth for The Cruise Lab initiative — every property, where it lives, how it is built and deployed. All enhancements, new tools, and maintenance work should be consistent with it; update it whenever the estate changes. Changes in rev 14: **the social media estate launched** — the handle **@thecruiselabhq** is locked across all platforms (display name "The Cruise Lab" everywhere); a full strategy/playbook (`cruiselab-social-playbook-v1-20260713.md`) and a brand-accurate avatar/banner asset pack (`cruiselab-social-assets-v1-20260714.zip`) are produced; positioning fixed as *"the account that runs the numbers on cruising"* — fully faceless, the gold flask is the face. New **Social media** section added below. Email plan updated: **Cloudflare Email Routing** (not Namecheap forwarding) is the chosen path for `hello@` and `social@`. Two new build tasks queued: the self-hosted **link hub** at links.thecruiselab.com, and a **`social/` folder** in the monorepo (idea bank + metrics). *Deferred to a later rev:* the Ocean View **v2** write-up (Harbour Board / per-port local time / Ships review section) — the YouTube harvest is still in progress, so the Ocean View entry below is carried forward unchanged from rev 13.

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

Fonts: Cinzel (500/600/700) for headings, Outfit (300–700) for UI/body, loaded from Google Fonts. Headline treatment: gold vertical gradient text (gold-bright → gold) via background-clip. Section dividers: thin gold gradient rules with centred uppercase letterspaced labels. Cards: panel gradient background, panel-edge border, 14px radius, lift on hover with gold border. "Coming soon" cards: dashed border, sea-glass chip. Conventions: pure HTML/CSS/JS, single self-contained file per page where practical, no build step, no frameworks. **Affiliate disclosure convention:** tools with affiliate links carry a discreet "may earn a commission" disclosure (GetMyCruiseConnection beside recommendation blocks + footer; Shore Thing screen-only footer line, excluded from print). Keep disclosures when reworking copy; keep commission *mechanics* out of marketing copy.

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
└── docs/
    └── cruiselab-master-context.md   (this document)
```

Exception: Good Cabin Bad Cabin keeps its own repo, sbrodie1978/goodcabinbadcabin (also public — note its README states the underlying Princess cabin data is not licensed for redistribution; Stuart has accepted this repo being public, including the committed MSC deck-plan SVGs and PDFs). **The GCBC clone does not yet exist on the new MacBook** — re-clone to `~/goodcabinbadcabin` when next needed, and reinstall PyMuPDF for the MSC pipeline. Workflow for any change: edit in the repo folder, deploy with wrangler, then commit and push. `.wrangler/` is gitignored.

## The estate — every property, where it lives

All web properties are Cloudflare Pages projects in Stuart's Cloudflare account (login stuartfbrodie@outlook.com, account ID 9c5f5919b1ef204bd2aacf415c814cda). Both registered domains are at Namecheap with DNS hosted on Cloudflare (nameservers anuj.ns.cloudflare.com / emerie.ns.cloudflare.com). Namecheap email-forwarding MX and SPF records were preserved on both zones. A quick census of every Pages project in the account: `npx wrangler pages project list`.

### 1. The hub
- URL: https://thecruiselab.com (plus www and thecruiselab.pages.dev)
- Cloudflare Pages project: `thecruiselab` (production branch `main`)
- Repo path: `~/cruiselab/hub` (single index.html)
- Content: hero with flask mark and "The Cruise Lab" wordmark, tagline, "The Fleet" divider with one card per live tool, then an "In the Lab" divider with coming-soon tiles (dashed border / sea-glass chip).
- **Current Fleet cards (8 live tools as of 13 Jul 2026, in order):** Good Cabin Bad Cabin (cabins.thecruiselab.com) · Sea You Soon (casinopoints.thecruiselab.com/princess/) · GetMyCruiseWeather (weather.thecruiselab.com) · Forever Voyage (forevervoyage.thecruiselab.com) · Ocean View (watch.thecruiselab.com) · GetMyBarTab (bartab.thecruiselab.com) · GetMyCruiseConnection (connection.thecruiselab.com) · Shore Thing (shorething.thecruiselab.com).
- **In the Lab (2 tiles):** All Aboard Store, GetMyCruiseMap.
- Structure note: live tools sit in `<main class="fleet">`, coming-soon tiles in a following `<section class="fleet">` (only one `<main>` per page).
- WARNING (repeatedly proven, most recently 13 Jul): before editing hub/index.html, always start from the live repo (`git pull` first), never from a possibly-stale copy in project knowledge — on 13 Jul the project-knowledge hub copy was three cards behind the live file and would have silently wiped the Ocean View, BarTab and Connection cards.

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
- KNOWN DATA GAPS (audited 13 Jul during the Shore Thing build): ports.json has 49 coordinate-duplicate entries (e.g. `alicante`/`alicante_spain` — all audited as legitimate aliases) and is thin exactly where cruising is busiest — only 8 Caribbean ports, and Alaska is missing Juneau/Skagway/Ketchikan entirely. Shore Thing's `data/ports.json` contains the fix: the deduped 216 plus 44 curated top-ups (full core Caribbean incl. private islands, Alaska big six, Mexican Riviera, Galveston/Canaveral/Tampa, Bermuda, Cartagena/Colón/Puntarenas), each flagged `gw:false`. **Backporting those 44 to GetMyCruiseWeather (and then flipping their flags in Shore Thing) is a queued task.**

### 5. GetMyBarTab — drinks spend predictor
- URL: https://bartab.thecruiselab.com (Cloudflare Pages project `getmybartab`, production branch `main`)
- Repo path: `~/cruiselab/getmybartab` (single self-contained index.html ~41KB + README)
- What it is: predicts what a cruiser will really spend on drinks — per person, split sea/port days, output styled as a literal itemised bar tab — then compares against a package price *the user supplies*.
- CORE DESIGN PRINCIPLE (do not break): **line-blind on package prices** — never store or guess a package price; the user pastes their quoted per-person/per-day number. What we curate is slow-moving à la carte per-drink pricing: `GENERIC_PRICES` fallback + per-line `LINES` overrides at the top of the `<script>` (only Princess individually curated in v1, incl. 18% service charge and the only real `pkgUrl`). `PRICE_STAMP` shows the curation date in the UI — update it whenever prices refresh (currently "July 2026").
- History: v1 built 5 Jul 2026, recovered from chat attachments and deployed 12 Jul 2026 after the MacBook swap. Hub card live.

### 6. GetMyCruiseConnection — WiFi, roaming & eSIM guide
- URL: https://connection.thecruiselab.com (Cloudflare Pages project `getmycruiseconnection`, production branch `main`) — custom domain confirmed **Active / SSL enabled** in the dashboard 13 Jul 2026, closing the suspected failed-Activate from the 12 Jul dashboard wobble.
- Repo path: `~/cruiselab/getmycruiseconnection` (single self-contained index.html ~42KB + README)
- What it is: decodes staying connected on a cruise — what works at open sea vs port days, ship WiFi vs roaming vs travel eSIMs, with affiliate-linked recommendations.
- Affiliate infrastructure: all partner URLs in one `LINKS` object at the top of the `<script>` (Airalo via Impact, Holafly coupon, GigSky, RedBull Mobile, VPN pick). `rel="sponsored"` added in the JS card templates; "Partner links — we may earn a small commission" disclosure beside every recommendation block and in the footer — keep disclosures if copy is reworked.
- Key content facts: standard travel eSIMs (Airalo, Holafly) work only on land networks (port days); GigSky (WMS Cellular at Sea) and RedBull Mobile Maritime (Telenor Maritime) are the two eSIMs that work at open sea — ship compatibility must be checked in each provider's app before purchase; Starlink fleet-wide rollout makes ship WiFi the primary sea-day recommendation.
- History: v1 built 5 Jul, iterated to v3 6 Jul 2026 (deployed version), recovered and deployed 12 Jul 2026. Hub card live.

### 7. Shore Thing — port guides for your exact sailing (NEW, 13 Jul 2026)
- URL: https://shorething.thecruiselab.com (canonical Pages URL shorething.pages.dev — unsuffixed name secured)
- Cloudflare Pages project: `shorething` (production branch `main` — the project was first created interactively with branch `production` by mistake, then deleted and recreated correctly; see lessons)
- Repo path: `~/cruiselab/shorething` (index.html + data/ports.json + data/guide-content.json + README)
- What it is: the user enters their cruise ports in order with dates (optional ship/cruise name) and gets a port-by-port guide for that exact sailing — editorial blurb, quick-fact chips (docked/tender, walkability, currency, language), a "Don't miss" list and a "Lab note" tip per port, plus per-day **Viator** tours link and **GetMyCruiseWeather** weather link. Date gaps render as "at sea" interstitials on a gold route-ribbon timeline. Guide can be read on screen, printed (print stylesheet flips to a paper "ship's programme" look) or downloaded as a standalone self-contained HTML file. Itinerary persists in localStorage (`shorething-sailing-v1`).
- Data: `data/ports.json` — 260 ports (GetMyCruiseWeather's 265 deduped to 216 + 44 top-ups; `gw` flag controls the weather link). `data/guide-content.json` — editorial keyed by port id; schema in the tool README; `"noviator":true` suppresses the Viator button (used for the 8 private islands, which have no independent tours). Ports without editorial render gracefully (links still work, quiet "notes coming" line).
- **Editorial coverage: the Americas complete (76 entries).** Remaining batches queued: Europe (103 ports), then Asia (67) / Oceania (9) / Africa (4).
- Affiliate: Viator links via `viatorUrl()` in index.html — same pid/mcid as GetMyCruiseWeather, plus `startDate`/`endDate` set to the port date. Screen-only footer disclosure line.
- Verified at launch by jsdom smoke test (23/23): search, ordering, sea days, day numbering, noviator, gw flags, affiliate URL construction, persistence, standalone download.
- Deploy: `npx wrangler pages deploy ~/cruiselab/shorething --project-name=shorething`

### 8. Ocean View — live cruise cams & free cruise video
- URL: https://watch.thecruiselab.com — canonical Pages URL is **oceanview-17z.pages.dev** (NOT oceanview.pages.dev, a stranger's site)
- Cloudflare Pages project: `oceanview` (production branch `main`)
- Repo path: `~/cruiselab/oceanview` (index.html + README.md)
- What it is: curated player for freely available cruise video — Live (Port Cams · Ship Cams · Ship Tracker) and Watch (Reviews & Tips · Golden Age) behind a gold pill switcher; modal player, click-to-load embeds, link-out cards with "Opens site ↗" chips.
- Legal posture: **embed, never rehost** — YouTube iframe player, archive.org embeds, VesselFinder's official embeddable map; PTZtv and cruise-line cams are link-out only. Sources credited.
- Everything driven by one `FEEDS` array (kinds: `yt-video`, `yt-uploads`, `archive`, `link`); swapping a dead feed is a one-line edit. Post-deploy sweep: `?debug=1` renders every embed inline. YouTube `embed/live_stream?channel=` is DEAD — pin video ids or use UC→UU uploads playlists (details in the tool README).
- Deploy: `npx wrangler pages deploy ~/cruiselab/oceanview --project-name=oceanview` then curl oceanview-17z.pages.dev.

### 9. Forever Voyage — bespoke keepsake cruise sites (PAID SERVICE)
- URL: https://forevervoyage.thecruiselab.com
- Cloudflare Pages project: `forever-voyage` — NOTE production branch is `production`; deploy with `--branch=production` or the deploy silently lands as a preview.
- Repo path: `~/cruiselab/forevervoyage` (single self-contained index.html, ~25KB)
- What it is: The Cruise Lab's first paid offering — a private, bespoke "travel journal" website of a customer's own cruise (day-by-day story, scrapbook pages, downloadable bundles, own web address, hosted and kept), modelled on Stuart's norwaywithmum site.
- Rate card (indicative): Standard up to 7 days $99 / £79 / €95; up to 14 days $199 / £159 / €189; Bespoke POA. Currency toggle client-side.
- CTA: `mailto:` with pre-filled template; `CONTACT_EMAIL` and `SAMPLE_URL` set at the top of the `<script>`. CTA currently stuartfbrodie@outlook.com (temporary). **TODO: create hello@thecruiselab.com via Cloudflare Email Routing (see Email routing subsection), then switch `CONTACT_EMAIL`.**
- Sample: https://forever-voyage-sample.pages.dev (own Pages project `forever-voyage-sample`, branch `main`), generated by `build-forever-voyage-sample.py` (v4; YuNet face pixelation, name anonymisation, download/video lockdown; model cache is per-machine and re-downloads on first run). Re-run whenever the real norwaywithmum changes; re-check the six hotlinked mosaic filenames still exist and are face-free.

## Social media

The Cruise Lab's social presence launched in rev 14. It is positioned as a **data brand**, not a travel vlog — the tagline internally is *"the account that runs the numbers on cruising."* Every post is a finding, verdict, ranking or myth-bust drawn from the estate's own data (≈70k scored cabins, 265 port weather records, bar-tab maths, casino-point mechanics, eSIM-at-sea facts). The brand is **fully faceless** — the gold flask is the face, delivery is screen recordings / animated charts / deck-plan graphics / voiceover. Goal priority (set by Stuart): 1) follower & view growth, 2) traffic to the tools, 3) affiliate revenue, 4) Forever Voyage leads. Time budget: 3–5 hrs/week.

- **Handle (all platforms): `@thecruiselabhq`.** Chosen after `@thecruiselab` / `@cruiselab` were found taken on Instagram and elsewhere; `thecruiselabhq` verified free across the board (14 Jul). **Display name is "The Cruise Lab" everywhere** — the handle is secondary to the name users read.
- **Platform tiers:** Tier 1 (growth engine, same short-form video cross-posted) = **TikTok · Instagram Reels · YouTube Shorts**. Tier 2 (community/distribution) = **Facebook Page + Reels** (gateway to the huge cruise Facebook groups) and **Pinterest** (evergreen tool traffic). Tier 3 (park the handle, minimal effort) = X · Threads · Bluesky, plus Reddit as a listen/participate-only channel. Deliberately *not* doing: long-form YouTube, livestreams, paid ads (revisit once organic formats prove out).
- **Content pillars → Fleet mapping:** P1 Cabin Verdicts (GCBC — flagship, most differentiated) · P2 The Bar Tab (GetMyBarTab) · P3 Connected at Sea (GetMyCruiseConnection — myth-bust gold) · P4 Port Intel (Shore Thing + GetMyCruiseWeather) · P5 Casino Points & Cruise Maths (Sea You Soon). Recurring series names: *Cabin Court*, *The Tab*, *Lab Report*, *Port File*.
- **Bio (all platforms):** ⚓ The account that runs the numbers on cruising / 🧪 Cabin scores · bar tabs · casino points · port guides / 🔗 All free tools ↓ — link to thecruiselab.com for now, switch to links.thecruiselab.com once the link hub is built.
- **Brand assets:** avatar/banner pack `cruiselab-social-assets-v1-20260714.zip`. Static version of the hub flask mark (heavier stroke, no animation) so it reads at ~40px; roundel avatar (gold ring) used everywhere, ringless square variant for rare square uses; banners sized per platform (YouTube 2560×1440 with content inside the 1546×423 TV-safe centre, X 1500×500, Facebook 1640×624, LinkedIn 1584×396, Pinterest 800×450); editable SVG masters + build scripts included. Instagram/TikTok take no banner (avatar + bio only). Same navy/gold tokens, Cinzel wordmark, Outfit tagline as the web estate.
- **Strategy doc:** `cruiselab-social-playbook-v1-20260713.md` — positioning, platform strategy, pillars, format recipes (F1 The Verdict, F2 The Receipt, F3 The Myth-Bust, F4 The Ranking, F5 The Lab Report, F6 Tool Demo — max 1 in 6), hook library, the weekly production system (one ~2–2.5h batch → 4 videos + 15 min/day distribution + engagement), the funnel, metrics, and a 90-day launch plan.
- **Operating rules (short form):** faceless always; one idea per video; hook in 2 seconds, brand only at the end; never demo tools more than 1 post in 6; same handle/avatar/voice everywhere; reply to comments in the first hour; batch weekly; every claim backed by the estate's data; keep on-site affiliate disclosures doing the work (don't state commission mechanics in content); saves & shares are the growth currency, not likes.
- **Pending social tasks:** produce the `social/` monorepo folder (idea bank `ideas.md`, `metrics.md`, brand assets, playbook); build the link hub (below); set up email routing (below); begin batch production (lead with P1 Cabin Verdicts + P3 myth-busts). Forever Voyage is *not* marketed in the growth feed — one tasteful post/month on Facebook/Instagram plus the link-hub button.

### Link hub (planned — links.thecruiselab.com)
Self-hosted "link in bio" page, **not Linktree** — a single Cruise Lab-styled page (navy/gold, flask, Cinzel) with one button per Fleet tool in hub order plus Forever Voyage at the bottom. On-brand, free, keeps the analytics in-house. Small build (~1 hr in the design system); to be a new Cloudflare Pages project (`links` or a `/links` route on the hub) → `links.thecruiselab.com`. Set as the bio link on every platform once live.

### Email routing (planned — Cloudflare Email Routing)
Since DNS is on Cloudflare, use **Cloudflare Email Routing** (free, native to the zone) rather than Namecheap forwarding (unsupported with external nameservers). Create two custom addresses on the thecruiselab.com zone, both forwarding to stuartfbrodie@outlook.com:
- **hello@thecruiselab.com** — public/customer address; then switch Forever Voyage's `CONTACT_EMAIL` to it (closes the long-standing TODO).
- **social@thecruiselab.com** — used only for social platform signups, keeping recovery/notification mail separate and filterable.
Setup: Cloudflare dashboard → thecruiselab.com → Email → Email Routing → add + verify destination → create the two addresses → let Cloudflare add its MX/SPF/DKIM records. Caveat: this replaces the currently-present Namecheap MX/SPF records on the zone (no working forward was ever actually configured, so nothing live is lost). Forwarding-in is all signups need; sending *from* these addresses needs extra setup and isn't required here.

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
```

The Forever Voyage **sample** is deployed from its generated folder: `cd forever-voyage-sample && npx wrangler pages deploy . --project-name=forever-voyage-sample`.

After deploying, commit and push: `cd ~/cruiselab && git add -A && git commit -m "..." && git push`. Pages projects are direct-upload type — pushing to GitHub does NOT auto-deploy.

Notes and lessons learned:
- **Creating a new Pages project (13 Jul 2026):** the command is `npx wrangler pages project create <name> --production-branch=main` — NOT `wrangler pages create`. If the flag is omitted and wrangler falls into its interactive prompt, the prompt's suggested branch is `production`, which recreates the Forever Voyage trap; if that happens before anything is deployed, delete (`wrangler pages project delete <name>`) and recreate rather than living with it.
- **Never run `wrangler pages deploy` from `~`** (13 Jul 2026): without a directory argument it tries to upload the current working directory — from home it dies on `~/.Trash` with a permissions error after uploading who-knows-what. Always pass the explicit folder path.
- **Production branches differ per project**: everything uses `main` except `forever-voyage` (`production`). Deploying to the wrong branch silently creates a preview — the tell is an "alias URL" line in wrangler output. Verify with `curl -L` on the canonical `.pages.dev` URL after deploying.
- **pages.dev subdomains are a GLOBAL namespace**: if a name is taken by anyone anywhere, Cloudflare silently suffixes yours (project `oceanview` → oceanview-17z.pages.dev). Read the actual URL from wrangler output; never verify against an assumed name. (`shorething.pages.dev` came through unsuffixed.)
- **Custom domain attachment**: dashboard → project → Custom domains → Set up → enter domain → Continue → **Activate domain**. The Activate click is the historically flaky step; the definitive success check is the domain appearing in the list on the project's `/domains` page (status runs Initializing → Verifying → Active, ~1–2 minutes for same-zone). The 12 Jul GetMyCruiseConnection scare resolved itself — confirmed Active 13 Jul.
- **Concurrent Claude sessions collide** — one build conversation per tool at a time; check file sizes/timestamps before zipping or deploying; curl-verify deployed title/content after every deploy.
- Verify a project has deployments before chasing DNS/522 errors: `npx wrangler pages deployment list --project-name=X`; `npx wrangler pages project list` is the estate census.
- Cloudflare Pages 308-redirects `/index.html` to `/` — always `curl -L`.
- Wrangler dedupes uploads by content hash — "0 files uploaded (N already uploaded)" is normal.
- Old deployments remain at their `<hash>.<project>.pages.dev` URLs (useful for recovery).
- Mac local DNS caching: `curl --resolve domain:443:IP` bypasses the OS resolver; Chrome's Secure DNS is independent of the OS resolver (curl-200-but-Chrome-blank is a known non-failure).
- iOS Safari caches deployed sites hard — fully close and reopen the tab after each deploy.
- Claude-in-Chrome: extension prompts per-site permission on first visit per domain; the bridge drops when idle — reopening the Chrome side panel wakes it (proven again 13 Jul).

## Backlog / ideas

- **Shore Thing editorial batches**: Europe (103 ports) next, then Asia/Oceania/Africa. Drop entries into `data/guide-content.json` — no code changes needed (schema in the tool README).
- **Backport Shore Thing's 44 top-up ports to GetMyCruiseWeather** (Caribbean, private islands, Alaska, Mexican Riviera, US homeports), then flip their `gw` flags to true in Shore Thing so those port days get weather links.
- **GetMyBarTab follow-ups**: à la carte prices for more lines beyond Princess; better currency conversion; real package links per line.
- **Email routing (Cloudflare)**: create `hello@` and `social@thecruiselab.com` via Cloudflare Email Routing (both → Outlook), then switch Forever Voyage's `CONTACT_EMAIL` to `hello@`. Supersedes the old "Namecheap forward" plan — see the Email routing subsection above.
- **Link hub (links.thecruiselab.com)**: build the self-hosted bio-link page (design-system, not Linktree) and set it as the bio link on every platform. See the Link hub subsection above.
- **Social `social/` folder + production**: create `social/ideas.md` (seed 30 ideas, 6 per pillar), `social/metrics.md`, and drop the playbook + asset pack into the monorepo; then start the weekly batch cadence. See the Social media section and playbook.
- **Ocean View v2 ideas** (parked in its README): "Sail-away now"; favourites via localStorage; weather chip per port cam (GetMyCruiseWeather tie-in); more port cams (Galveston, Kiel, Vancouver, Funchal, Juneau); more Golden Age films; auto-detect dead embeds.
- **Forever Voyage next**: Stripe payment links or a proper enquiry form instead of mailto; testimonials; real custom-domain option for the bespoke tier; consider forevervoyage.com if the service takes off.
- **All Aboard Store** (announced on hub, not built): curated cruise-gear shop via Amazon Associates. Categories: packing, onboard cabin kit, fun (ducks), luggage tags. Catalogue to curate before build; affiliate disclosure required per Associates rules.
- **GetMyCruiseMap** (announced on hub, not built): itinerary + photos → keepsake route-map print via print-on-demand. Open questions: POD referral/API route; print resolution; photo handling on static hosting. Market note: Emma Cruises promotes satellite-data cruise-route prints — study before build.
- "Part of The Cruise Lab" footer badge inside the Sea You Soon Princess calculator (GCBC done).
- GCBC data-use permissions: written authority from **Princess, MSC, P&O and Carnival**. P&O + Carnival are the natural next lines. Other lines need asking first.
- GCBC / MSC open follow-ups (none blocking): quiet-axis calibration; World-class review questions (outdoor promenade weight vs indoor Galleria; 5-deck YC cabins near the private pool); odd=Port verification vs a real photo; Magnifica deck 12 re-harvest post-refit; icon TYPE decoding (accessible/whirlpool/obstructed). Princess payload: backfill cabin `type` at row index 18 (MSC has it; enables category filtering).
- Casino points calculators for Carnival (Fun Play), Royal Caribbean (Casino Royale), Norwegian (Casinos at Sea) — folders under sys-points.
- Sea You Soon v2 ideas: "What did I earn?" mode; points-per-day pacing; link reward stateroom tiers to GCBC; footer badge.
- Cruise industry awards: Wave Awards 2027 entries open Feb–Mar 2027; Seatrade innovation categories a possible B2B fit.
- Delete the redundant Netlify projects (cruiseweatherstuart, getmycruiseweather, remarkable-cucurucho-b7209c) once comfortable.

## Working style

Stuart is technical and hands-on: he runs terminal commands himself (wrangler, curl, dig) and prefers being handed a file plus a one-liner deploy command over dashboard clicking. Output-oriented sessions; informal, direct communication. Claude may also drive his Chrome browser (Claude in Chrome extension) for dashboard work on Cloudflare/Namecheap when asked — Stuart handles all logins and password entry himself; the extension prompts for per-site permission on first visit to each domain. File-delivery discipline: unique versioned filenames, one attachment per message, multi-file deliveries as a single uniquely-named zip; every tool gets a git-committed folder with a README covering what it is, where it's deployed, how to use it and how it's built. One build conversation per tool at a time.
