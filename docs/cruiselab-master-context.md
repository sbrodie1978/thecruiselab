# The Cruise Lab — Master Context

Last updated: 5 July 2026 (rev 6 — Forever Voyage bespoke keepsake service launched; first paid offering). This document is the single source of truth for The Cruise Lab initiative. All enhancements, new tools, and maintenance work should be consistent with it. Update it when the estate changes.

## What The Cruise Lab is

The Cruise Lab (thecruiselab.com) is Stuart Brodie's umbrella brand for a collection of free web tools built for the cruising community — "free web tools built by a cruiser, for cruisers." Each tool keeps its own name and identity as a member of "The Fleet"; the hub at thecruiselab.com is the landing page from which users pick a tool. New tools and services launch under the brand and get a card on the hub, with an "In the Lab" slot teasing what's next. Most of the Fleet is free; **Forever Voyage** is the first *paid, bespoke* offering — a made-to-order keepsake website built for an individual customer's cruise. All tools carry a disclaimer that they are independent and not affiliated with or endorsed by Princess Cruises or any cruise line.

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
├── forevervoyage/        → Pages project "forever-voyage"      → forevervoyage.thecruiselab.com
│                           (the sample site is a SEPARATE project "forever-voyage-sample")
└── docs/
    └── cruiselab-master-context.md   (this document)
```

Exception: Good Cabin Bad Cabin keeps its own repo, sbrodie1978/goodcabinbadcabin (also public — note its README states the underlying Princess cabin data is not licensed for redistribution; Stuart has accepted this repo being public). Workflow for any change: edit in the repo folder, deploy with wrangler, then commit and push. `.wrangler/` is gitignored.

## The estate — every property, where it lives

All web properties are Cloudflare Pages projects in Stuart's Cloudflare account (login stuartfbrodie@outlook.com, account ID 9c5f5919b1ef204bd2aacf415c814cda). Both domains are registered at Namecheap with DNS hosted on Cloudflare (nameservers anuj.ns.cloudflare.com / emerie.ns.cloudflare.com). Namecheap email-forwarding MX and SPF records were preserved on both zones.

### 1. The hub
- URL: https://thecruiselab.com (plus www and thecruiselab.pages.dev)
- Cloudflare Pages project: `thecruiselab`
- Repo path: `~/cruiselab/hub` (single index.html)
- Content: hero with flask mark and "The Cruise Lab" wordmark (small tracked "THE" above "CRUISE LAB"), tagline, "The Fleet" divider, one card per tool, an "In the Lab" coming-soon card, footer with disclaimer.
- Current card links: cabins.thecruiselab.com · casinopoints.thecruiselab.com/princess/ · weather.thecruiselab.com · forevervoyage.thecruiselab.com (Forever Voyage graduated from "In the Lab" on 5 Jul 2026; the "In the Lab" teaser card is retained after it)

### 2. Good Cabin Bad Cabin — cabin scoring
- URL: https://cabins.thecruiselab.com (plus goodcabinbadcabin.pages.dev)
- Cloudflare Pages project: `goodcabinbadcabin`
- Source: GitHub repo sbrodie1978/goodcabinbadcabin (public)
- What it is: scores every cabin from the deck plans — quietness, motion, convenience, space — across five traveller profiles, with a cross-section of what's above/below/beside each cabin. Princess is live (17 ships, ~27,500 staterooms); more lines to follow.
- Structure (since 5 Jul 2026): root index.html is a hand-maintained cruise-line chooser (Princess live; MSC "up next"; ~10 more leading lines as coming-soon tiles with hover veil — typographic tiles with brand-colour accent bars, deliberately no official logos for trademark reasons). Each line lives in its own folder: `/princess/` holds the generated app plus `data/ship-N.json` (ship IDs restart from 1 per line). Future lines (MSC first) get their own folder + pipeline.
- Design: GCBC keeps its own identity, distinct from the hub — paper/ink utilitarian look (--ink:#122740 on --paper:#eef1ec), Saira Stencil One display, Azeret Mono labels, Hanken Grotesk body.
- Pipeline: frontend is GENERATED — edit `pipeline/build_frontend.py`, never `princess/index.html` directly. Rebuild: `fleet_build.py` → `make_payload.py` → `build_frontend.py` (stdlib Python only). Data from Princess's public deck-plan API, used with permission; refits re-harvested per `pipeline/HARVEST.md`.
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
- Cloudflare Pages project: `forever-voyage`
- Repo path: `~/cruiselab/forevervoyage` (single self-contained index.html)
- What it is: The Cruise Lab's first paid offering. Stuart builds a private, bespoke "travel journal" website for a customer's own cruise — day-by-day story, scrapbook pages, downloadable photo/video bundles for the family, their own web address, hosted and kept. Same look/output as the norwaywithmum site Stuart made of his own Norway-with-mum trip on Sky Princess (the origin of the idea and the sample of the work).
- Design: hub navy/gold system (Cinzel + Outfit, standard tokens). Own mark: a rotating gold compass rose with a sea-glass wave. Single self-contained file, no build step. Sections: hero → sample showcase (framed iframe of the sample) → what you get → how it works → multi-currency rate card → mailto CTA → FAQ → footer.
- Rate card (indicative, editable): Standard up to 7 days $99 / £79 / €95; Standard up to 14 days $199 / £159 / €189; Bespoke POA. Currency toggle (GBP default) swaps prices client-side via data-attributes. Tiers scope the labour: 7-day ~40 photos; 14-day adds scrapbook pages + video; bespoke = custom design / own domain / unlimited.
- CTA: gold "Start your journal" button = a `mailto:` with a pre-filled enquiry template (ship, dates, ports, photo count, videos y/n, who it's for). Contact address and sample URL are set once at the top of the `<script>` block (`CONTACT_EMAIL`, `SAMPLE_URL`) — edit there to change everywhere. **TODO: confirm `hello@thecruiselab.com` forwarding is actually configured in Namecheap** (MX/SPF are preserved on the zone, but the specific mailbox/forward rule needs verifying/creating).

### 5a. The Forever Voyage sample (anonymised norwaywithmum clone)
- URL (planned): https://forever-voyage-sample.pages.dev (auto URL of its own Pages project; the service page links to exactly this).
- Cloudflare Pages project: `forever-voyage-sample` (separate from the service page).
- Origin: Stuart's real norwaywithmum site (project `norwaywithmum`, live at norwaywithmum.pages.dev — single-page site, images at /images/, posters at /videos/posters/, family zips at /downloads/, RIB video clips at /videos/*.mp4). Built outside the monorepo; source of truth is the live Cloudflare deployment.
- Built by a script: `~/cruiselab/forevervoyage/build-forever-voyage-sample.py` (stdlib + opencv-python only). It downloads the live site, mirrors + pixelates faces in every photo (Haar frontal/profile/flipped), anonymises names (Frances/Stuart → Mum/Son etc.), disables the family download links, and OMITS the video clips (moving faces can't be reliably blurred — posters are kept and face-blurred). Output: `./forever-voyage-sample/` ready to deploy. The script prints any photo where it found no face so Stuart can eyeball those before going live. Re-run any time the real norwaywithmum changes.
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
npx wrangler pages deploy ~/cruiselab/forevervoyage --project-name=forever-voyage
```

The Forever Voyage **sample** is deployed from its generated folder (not the repo):

```bash
cd forever-voyage-sample && npx wrangler pages deploy . --project-name=forever-voyage-sample
```

After deploying, commit and push the change: `cd ~/cruiselab && git add -A && git commit -m "..." && git push`. Note the Pages projects are direct-upload type, not git-connected — pushing to GitHub does NOT auto-deploy; wrangler is the deploy mechanism.

Notes and lessons learned:
- A stray `~/Downloads/wrangler.toml` triggers a harmless warning on every deploy; deleting it silences this.
- Cloudflare Pages 308-redirects `/index.html` to `/`; when curling a deployed file, always use `curl -L`.
- Wrangler deduplicates uploads by content hash — "0 files uploaded (N already uploaded)" is normal and fine.
- Old deployments remain accessible at their unique `<hash>.<project>.pages.dev` URLs and can be listed with `npx wrangler pages deployment list --project-name=<project>` (useful for recovering previous content).
- Custom domains attach to Pages projects via dashboard → project → Custom domains; DNS records are created automatically because both zones are on Cloudflare.

## Backlog / ideas

- Forever Voyage launched 5 Jul 2026 (service page + hub card). Next: (1) verify/create the `hello@thecruiselab.com` forward in Namecheap so the CTA works; (2) build + deploy the anonymised sample via the script, attach subdomain if desired; (3) later — Stripe payment links or a proper enquiry form instead of mailto; testimonials; a real custom domain option for bespoke tier; consider a foreveryvoyage.com domain if the service takes off.
- "Part of The Cruise Lab" footer badge inside the Sea You Soon Princess calculator (GCBC done 5 Jul 2026).
- GCBC data-use permissions: Stuart has written authority to proceed from **Princess, MSC, P&O and Carnival** (email replies stored). MSC launch is unblocked; P&O and Carnival are the natural next lines after MSC. Other lines still need asking before their data is used.
- GCBC / MSC: **harvest complete 5 Jul 2026** — 24 ships, ~43,900 cabins, official per-deck SVGs (cabin number = element id, geometry native, category = fill colour) captured via Claude-in-Chrome (site is behind an Akamai bot wall; direct HTTP 403s). Raw data + docs live in the GCBC repo under `data-source/msc/` and `pipeline/msc/HARVEST.md` (read it before re-harvesting — four filename schemes, refit suffixes, lazy-loading traps). Known gaps: Magnifica deck 12 (mid Yacht-Club refit, plan unpublished — re-harvest later); Poesia count under published figure (reconcile vs PDF). Extraction done (5 Jul 2026): `pipeline/msc/parse_svgs.py` → per-cabin geometry + category, 97–100% group-resolved per ship (residue documented in `pipeline/msc/HARVEST.md`, incl. the World-class `#003891` category to identify via PDF). Remaining to go live: scoring (7 class deck-stack/venue maps + fleet_build-style scorer), `/msc/` payload + app folder, flip the chooser tile. Permission from MSC already in hand. Remaining chooser tiles (RCI, Carnival, NCL, Celebrity, HAL, P&O, Cunard, Disney, Virgin, Costa) follow the same pattern.
- Casino points calculators for Carnival (Fun Play), Royal Caribbean (Casino Royale), Norwegian (Casinos at Sea) — folders under the sys-points project.
- Sea You Soon v2 ideas from original build: "What did I earn?" mode (enter final points, get the offer styled like the SYS letter); points-per-day pacing projection; link from reward stateroom tiers to Good Cabin Bad Cabin.
- Cruise industry awards: Wave Awards 2027 entries typically open Feb–Mar 2027 (judged entries ~£250+VAT per category; public-voted "Favourite Cruise Influencer" category is the accessible route). Seatrade Cruise Awards innovation categories are a possible B2B-framing fit.
- Delete the redundant Netlify projects (cruiseweatherstuart, getmycruiseweather, remarkable-cucurucho-b7209c) once comfortable.

## Working style

Stuart is technical and hands-on: he runs terminal commands himself (wrangler, curl, dig) and prefers being handed a file plus a one-liner deploy command over dashboard clicking. Output-oriented sessions; informal, direct communication. Claude may also drive his Chrome browser (Claude in Chrome extension) for dashboard work on Cloudflare/Namecheap when asked — Stuart handles all logins and password entry himself.
