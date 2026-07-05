# The Cruise Lab — Master Context

Last updated: 5 July 2026. This document is the single source of truth for The Cruise Lab initiative. All enhancements, new tools, and maintenance work should be consistent with it. Update it when the estate changes.

## What The Cruise Lab is

The Cruise Lab (thecruiselab.com) is Stuart Brodie's umbrella brand for a collection of free web tools built for the cruising community — "free web tools built by a cruiser, for cruisers." Each tool keeps its own name and identity as a member of "The Fleet"; the hub at thecruiselab.com is the landing page from which users pick a tool. New tools launch under the brand and get a card on the hub, with an "In the Lab" slot teasing what's next. All tools carry a disclaimer that they are independent and not affiliated with or endorsed by Princess Cruises or any cruise line.

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

## The estate — every property, where it lives

All web properties are Cloudflare Pages projects in Stuart's Cloudflare account (login stuartfbrodie@outlook.com, account ID 9c5f5919b1ef204bd2aacf415c814cda). Both domains are registered at Namecheap with DNS hosted on Cloudflare (nameservers anuj.ns.cloudflare.com / emerie.ns.cloudflare.com). Namecheap email-forwarding MX and SPF records were preserved on both zones.

### 1. The hub
- URL: https://thecruiselab.com (plus www and thecruiselab.pages.dev)
- Cloudflare Pages project: `thecruiselab`
- Local folder on Stuart's MacBook: `~/thecruiselab` (single index.html)
- Content: hero with flask mark and "The Cruise Lab" wordmark (small tracked "THE" above "CRUISE LAB"), tagline, "The Fleet" divider, one card per tool, an "In the Lab" coming-soon card, footer with disclaimer.
- Current card links: cabins.thecruiselab.com · casinopoints.thecruiselab.com/princess/ · weather.thecruiselab.com

### 2. Good Cabin Bad Cabin — cabin scoring
- URL: https://cabins.thecruiselab.com (plus goodcabinbadcabin.pages.dev)
- Cloudflare Pages project: `goodcabinbadcabin`
- Source: private GitHub repo sbrodie1978/goodcabinbadcabin
- What it is: scores every cabin on the Princess fleet — 17 ships, ~27,000 staterooms — so cruisers know before booking whether a cabin is a gem or a dud.

### 3. Casino Points (Sea You Soon) — casino comp points
- URL: https://casinopoints.thecruiselab.com (plus sys-points.pages.dev)
- Cloudflare Pages project: `sys-points`
- Local folder: `~/casinopoints`
- Structure: root index.html is a cruise-line chooser (Princess live; Carnival, Royal Caribbean, Norwegian shown as coming soon). Each cruise line lives in its own subfolder: `/princess/` currently hosts the Sea You Soon calculator (Princess SYS programme: voyage-length selector, optional points-so-far input, nine-tier offer ladder with free-play values, stateroom types, Princess Plus chips; point system effective 1 Sep 2025). Future lines are added as new folders (e.g. `carnival/index.html`) plus activating the matching chooser card.
- The Princess app is a single self-contained index.html (~15.7KB). A backup copy exists at `~/Downloads/sea-you-soon-deploy/index.html`.

### 4. GetMyCruiseWeather — port-by-port cruise weather
- URLs: https://getmycruiseweather.com (primary, its own consumer brand) and https://weather.thecruiselab.com (Cruise Lab alias) — both plus www and getmycruiseweather.pages.dev
- Cloudflare Pages project: `getmycruiseweather`
- Local folder: `~/Downloads/getmycruiseweather` (worth moving to `~/getmycruiseweather`)
- Structure: multi-file static site — index.html (port picker), results.html, js/app.js, css/styles.css, data/ports.json (ports database), assets (logos + Viator affiliate logos), tools/port-validator.html, ports_readme.md.
- Data: weather from the Open-Meteo archive API, called client-side, no API key. Google Analytics (gtag) installed. Viator affiliate links for shore excursions.
- History: migrated from Netlify on 5 Jul 2026 (was Netlify project `cruiseweatherstuart`, deployed via Netlify Drop, team "Stuart Cruise"). The Netlify project is now redundant and can be deleted. The app had real traffic at migration time (~28 requests/hour).

## Deployment workflow (standard for all projects)

Deploys are done from Stuart's MacBook terminal with wrangler:

```bash
npx wrangler pages deploy <folder> --project-name=<project>
```

e.g. `npx wrangler pages deploy ~/thecruiselab --project-name=thecruiselab`

Notes and lessons learned:
- A stray `~/Downloads/wrangler.toml` triggers a harmless warning on every deploy; deleting it silences this.
- Cloudflare Pages 308-redirects `/index.html` to `/`; when curling a deployed file, always use `curl -L`.
- Wrangler deduplicates uploads by content hash — "0 files uploaded (N already uploaded)" is normal and fine.
- Old deployments remain accessible at their unique `<hash>.<project>.pages.dev` URLs and can be listed with `npx wrangler pages deployment list --project-name=<project>` (useful for recovering previous content).
- Custom domains attach to Pages projects via dashboard → project → Custom domains; DNS records are created automatically because both zones are on Cloudflare.

## Backlog / ideas

- "Part of The Cruise Lab" footer badges inside Good Cabin Bad Cabin and the Princess calculator, linking back to thecruiselab.com (the chooser and hub already link out; the tools don't yet link home).
- Casino points calculators for Carnival (Fun Play), Royal Caribbean (Casino Royale), Norwegian (Casinos at Sea) — folders under the sys-points project.
- Sea You Soon v2 ideas from original build: "What did I earn?" mode (enter final points, get the offer styled like the SYS letter); points-per-day pacing projection; link from reward stateroom tiers to Good Cabin Bad Cabin.
- Cruise industry awards: Wave Awards 2027 entries typically open Feb–Mar 2027 (judged entries ~£250+VAT per category; public-voted "Favourite Cruise Influencer" category is the accessible route). Seatrade Cruise Awards innovation categories are a possible B2B-framing fit.
- Delete the redundant Netlify projects (cruiseweatherstuart, getmycruiseweather, remarkable-cucurucho-b7209c) once comfortable.

## Working style

Stuart is technical and hands-on: he runs terminal commands himself (wrangler, curl, dig) and prefers being handed a file plus a one-liner deploy command over dashboard clicking. Output-oriented sessions; informal, direct communication. Claude may also drive his Chrome browser (Claude in Chrome extension) for dashboard work on Cloudflare/Namecheap when asked — Stuart handles all logins and password entry himself.
