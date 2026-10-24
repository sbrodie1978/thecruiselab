# The Cruise Lab — Master Context

Last updated: 24 October 2026 (rev 30). This document is the single source of truth for The Cruise Lab initiative: every property, where it lives, how it is built and deployed. All enhancements, new tools, and maintenance work should be consistent with it; update it whenever the estate changes.

Changes in rev 30 (**production-branch facts corrected; no estate change**): a GetMyCruiseWeather redeploy during the rev-29 work silently landed as a Preview because this doc wrongly listed its production branch as `main`. It is actually `production`. The live site kept serving the old Viator build until it was redeployed with `--branch=production`, after which the edge cache was purged and both getmycruiseweather.com and weather.thecruiselab.com verified clean. Every project's real production branch was then checked with `npx wrangler pages deployment list`: **`sys-points`, `getmycruiseweather` and `cruiselab-slots` have production branch `production`** (as do the two registries); everything else (`thecruiselab`, `getmybartab`, `getmycruiseconnection`, `shorething`, `oceanview`, `links`) is `main`. The deploy commands and the production-branches lesson below are corrected accordingly. `sys-points` was also mis-documented (its deploy line lacked `--branch=production`) but was not deployed in the rev-29 work, so no live site was affected. Lesson reinforced: a deploy printing no alias-URL line is not sufficient proof it went to production; when in doubt, check `deployment list` for the row marked Production.

Changes in rev 29 (**the estate went fully FREE: all affiliate links and monetisation removed across the whole estate; both income-capable accounts closed**). This is Stuart's decision to take no income at all from The Cruise Lab. No estate tool's core function was harmed; only the money layer was stripped out.

1. **Amazon Associates — BOTH accounts CLOSED** (UK `thecruiselabh-21`, US `thecruiselabh-20`). The 180-day/3-sales gate is therefore moot (accounts gone, not lapsed).
2. **Viator partner account (pid `P00290711` / mcid `42383`) — payout methods removed and closure requested** by email to `affiliationteam@viator.com` (awaiting their written confirmation at time of writing). The ~$7 outstanding balance is below the $50 bank threshold and was never on a live payout method, so it will be withheld / forfeited, not paid. Lever used throughout: removing the payout destination guarantees no money moves, closure is tidy-up.
3. **All Aboard Store — DELETED entirely** (the estate's only Amazon-monetised tool). Cloudflare Pages project `allaboardstore` deleted; custom domain `store.thecruiselab.com` detached via the dashboard (CNAME auto-removed); repo folder `allaboardstore/` git-removed; hub Fleet card removed; link-hub row removed; personal-registry row marked **superseded** (not deleted, per registry convention). `store.thecruiselab.com` is now a free subdomain.
4. **Forever Voyage — DELETED entirely** (the estate's former paid keepsake-site service). Projects `forever-voyage` and `forever-voyage-sample` deleted; domain `forevervoyage.thecruiselab.com` detached; repo folder `forevervoyage/` and the generator `build-forever-voyage-sample.py` git-removed; hub card removed; link-hub "Made to order" section removed; registry rows (both FV and FV sample) marked **superseded**. **The estate now has NO paid offering.** `norwaywithmum` (the reference site that FV's sample was built from) is untouched and stays, see entry 13.
5. **Viator link-outs stripped from GetMyCruiseWeather** (the "Recommended shore excursions" section in `results.html`; `buildViatorUrl()`, `updateViatorLink()`, the now-unused `getPortNameById()` and all four calls in `js/app.js`; and the `assets/viator-logo.png` + `viator-logo.svg` assets) **and from Shore Thing** (`viatorUrl()`, the per-day "Tours & excursions" buttons, the `noviator` flag, the footer commission disclosure, and "tours" in the meta description + pending note). Weather links, scoring, packing, history and the rest of both tools are untouched. The ~330 lines of orphaned Viator CSS in GetMyCruiseWeather's `css/styles.css` were **left in place** (dead but harmless; strip in a later pass if a spotless file is wanted).
6. **GetMyCruiseConnection — affiliate framing stripped, recommendations kept.** Every `rel="noopener sponsored"` → `rel="noopener"` (6 buttons); the comparison-table commission sentence, the footer affiliate note, and the sea/port/VPN "we may earn a commission" disclosures all removed (the `${carrierPass}` US day-pass note kept). The GigSky / RedBull / Airalo / Holafly / VPN picks and their **plain destination links remain** as honest recommendations. These never earned anyway (the eSIM affiliate workstream was never wired to a paying account). The `LINKS` object's internal `// TODO affiliate link` dev comments were left in place (not user-facing); trivial tidy if wanted.
7. **Hub — Fleet now 6 live cards:** Good Cabin Bad Cabin, Sea You Soon, GetMyCruiseWeather, GetMyBarTab, GetMyCruiseConnection, Grand Voyage. The social-preview text "Eight free tools" was corrected to "Six".
8. **Link hub — 5 Fleet tools:** Good Cabin Bad Cabin, Sea You Soon, GetMyCruiseWeather, GetMyBarTab, GetMyCruiseConnection. The All Aboard Store row (which had quietly been added to the live link hub despite the rev-28 doc saying it was still missing), the Forever Voyage section and divider, and the affiliate disclosure footer line were all removed. Independence disclaimer kept.
9. **Privacy policy → Version 2, effective 24 Oct 2026.** All affiliate / Amazon Associates / Viator / Impact references removed; the Forever Voyage paragraph removed; section 6 repurposed from "Affiliate links" to **"No affiliate links or commission"**; the affiliate cookie bullet, the affiliate data-sharing bullet, and the Forever Voyage "performance of a contract" legal basis removed (email handling folded into legitimate interests); Grand Voyage added to the covered-tools list. Section numbering (1 to 15) deliberately preserved so cross-references still hold.
10. **Impact.com publisher account (ID 7483535) still exists** but is now entirely unused (it never earned; no bank details were ever added, so no income risk). Close it too if you want zero affiliate accounts anywhere (optional).
11. **Social knock-on (TO DO, not yet actioned):** the **L2 launch video** ("5 things confiscated at the gangway") and the **All Aboard Store promo video** both drive traffic to the now-deleted store, so **pull L2 from the relaunch** and shelve the promo. The social strategy docs (`social-playbook`, `launch-campaign`, `launch-scripts`, `ideas`) predate this pivot and still describe the affiliate funnel (Viator / eSIM / Amazon), goal #3 "affiliate revenue", goal #4 "Forever Voyage leads", and the L2 / L4 destinations. Treat them as historical; refresh when next touched.
12. **Goal priority simplified** to: **1) follower & view growth, 2) traffic to the tools.** Affiliate revenue and Forever Voyage leads are retired as goals.

All tool changes were deployed to Cloudflare Pages, committed and pushed (monorepo commits for the store/FV removal, hub, link hub, GetMyCruiseWeather, Shore Thing, GetMyCruiseConnection and the privacy policy; a personal-registry commit for the superseded rows). Everything else carried forward unchanged from rev 28. The rev 28 and earlier notes below are kept as history.

Changes in rev 28 (**social launch videos recovered into version control, relaunch prepared**. A documentation-gap fix; no estate or tool code changed.): (1) **The four launch videos (L1 to L4) and the "Meet Sarah" intro promo were BUILT on 15 to 16 July** and had simply never been recorded here. L1 to L4 were produced via a code video pipeline: animated HTML/CSS timelines (`src/l1.html` to `l4.html`), headless-Chrome frame capture (`capture.js`), ffmpeg encode, and Python-synthesised audio (`audio_synth.py`, no licensed music, so TikTok-safe). Delivered as `cruiselab-launch-batch-v3-20260715.zip` (L1 v5, L2 to L4 v2). Earlier revs and the `launch-scripts` doc's "Still to do before filming" section implied they were unfilmed. That stale-doc gap caused a later session to almost rebuild them from scratch via screen recordings and CapCut before it was caught. Corrected here. (2) **The batch is now COMMITTED to the monorepo** at `~/cruiselab/social/video/` (commit `59723de`): the four MP4 masters, the intro MP4, the full render source in `src/` (`l1` to `l4.html`, `helpers.js`, `capture.js`, `still.js`, `audio_synth.py`, `audit.js`, `style.css`), and a README. Until 20 Oct these were zip-only, a norwaywithmum-class recovery risk. **STANDING RULE:** Cruise Lab video VISUALS are built via this code pipeline and edited or rebuilt from `social/video/src/`, never re-created from screen recordings. A finished video batch is a first-class estate item that gets a master-context entry plus a repo commit, the same as a tool. (3) **Relaunch prepared.** The plan is a full re-launch, re-issuing every video regardless of prior posting. The post pack `social/cruiselab-relaunch-post-pack-v2-20261020.md` (commit `b6fdc13`) holds per-video, per-platform captions, the schedule (intro, then L1, L3, L4, L2, with post-days and engagement-days alternating), and the posting routine (native upload per platform, TikTok first then IG Reels and YouTube Shorts about two hours later then Facebook, reply to every comment in the first hour). Posting is done by Stuart from the phone apps. Claude cannot post (native file-upload dialog plus platform anti-automation), so the split is: Claude writes the content and captions, Stuart posts. **(Rev-29 note: L2 drives to the now-deleted All Aboard Store, so pull it from this relaunch.)** (4) **TikTok is linkless until 1,000 followers.** The website field is locked on a personal account and the Business switch needs a business-registration certificate Stuart does not have, so TikTok's CTA is the typed brand URL `thecruiselab.com` (also on every end card), while Instagram, Facebook and YouTube carry the clickable funnel. The existing intro stays on TikTok, pinned; TikTok's video run starts with L1. (5) **Funnel confirmed.** (Rev-29 note: All Aboard Store has since been removed from links.thecruiselab.com along with the tool itself.) IG and FB bio links are correct; the YouTube channel link is set. (6) **`social/` is no longer "planned".** It exists and is tracked: strategy docs, the assets zip, the relaunch pack, and `video/`. (7) **Follow-up logged, built but NOT yet committed or documented:** a **Cost Creep video series** (C1 to C5: `cruiselab-costcreep-scripts-v1-20260715.md` plus preview HTMLs) and an **All Aboard Store promo video** (`cruiselab-allaboardstore-promo-v1-20260716.mp4`) exist on disk from July but are not in the repo or this doc. **(Rev-29 note: the All Aboard Store promo is now dead content, the store is gone; shelve it. The Cost Creep series should still be folded into version control when next touched.)** (8) **Residual to confirm.** The committed intro MP4 is `cruiselab-intro-promo-v1-20260714.mp4`, but the version posted on TikTok is a ~22s cut with baked audio, whereas the rev-27 intro entry below describes a 40s silent v1; and the intro's own renderer (`render.py`, PIL-based) is NOT in `social/video/src/`. Confirm which intro cut is canonical and commit its renderer to close the last source gap. Everything else carried forward unchanged from rev 27. The rev 27 notes below are kept as history. Changes in rev 27 (**Grand Voyage LAUNCHED**, same day as rev 26): the slot is no longer hidden. (1) **noindex removed** from both places (the robots meta in `src/app.html` and the `X-Robots-Tag` line in `build.py`); live headers verified with no robots tag. (2) **Hub Fleet card added** as the 8th and last live card (line-art slot machine icon, "Free-play slots, lab-built" copy, Launch tag); verified live on thecruiselab.com. **(Rev-29 note: Fleet is now 6 live cards after the store and Forever Voyage were removed; Grand Voyage remains, now the 6th.)** (3) **Privacy & Cookies link added** to the slot footer. (4) **Not added to the link hub** (Claude recommended against it; Stuart's decision pending, see entry 10). (5) **Awin advertiser-terms check skipped at launch** by Stuart's call; still worth doing (backlog). **(Rev-29 note: with no affiliate tools left on the estate, this is far less pressing.)** Slot README/DEPLOY updated (v11). Monorepo commit `1c84b7b`. The rev 26 notes below describe the hidden pre-launch state and are kept as history. Changes in rev 26 (**NEW ESTATE PROPERTY: Grand Voyage slots**, see estate entry 14): (1) **Grand Voyage**, a free-play, cruise-themed slot machine in the Cruise Lab design system, is **LIVE at slots.thecruiselab.com** (new Pages project **`cruiselab-slots`**, production branch **`production`**, canonical **cruiselab-slots.pages.dev**, no suffix). Play money only, no purchases, no prizes, no affiliate links, 18+ note with the GamCare helpline. (2) It is the estate's **first tool with a build step**: source in `slots/src/` (`app.html` + `engine.js`), `build.py` inlines the engine and copies `static/` into `dist/`, and **only `dist/` is deployed**. **Deploy from the `slots` folder pointing at `dist`** (`npx wrangler pages deploy dist ...`), never from inside `dist`. (3) Its four bonus games are each themed on an estate tool, with a "Try the real tool" link after each: **Happy Hour Bar** (GetMyBarTab), **Upgrade Fever** (GCBC), **Sunshine Voyage** (GetMyCruiseWeather), **Summit Rush** (Shore Thing: name and link suppressed by a `SHORE_THING_LIVE=false` flag while Shore Thing is withheld). (4) **Icon kit shipped** (v10): estate gold flask copied from `hub/`, own manifest named "Grand Voyage". **Deliberate exception** to the estate head snippet: the slot sets `apple-mobile-web-app-capable` and `display: standalone`. (5) **Registry row added** in the personal registry, Cruise Lab group (commit `e1a3067`). Note the personal registry repo moved its site into `dist/` (commit `5749a77`): it now deploys from `dist` with `--branch=production`. (6) **Lesson (rev 26):** a brand-new Pages project's `<hash>.<project>.pages.dev` deployment URL can return nothing for a few minutes (certificate not issued yet) while the canonical `<project>.pages.dev` already serves: verify bytes on the canonical URL. Monorepo commits `d61ff60` (v9 build) and `a155d37` (v10 icon kit). Everything else carried forward unchanged from rev 25. Changes in rev 25 (**two per-site icons + a NEW documented property, norwaywithmum**): (1) **GetMyCruiseWeather now uses its OWN ship mark**, not the estate flask. (2) **NEW ESTATE PROPERTY documented — norwaywithmum** (see estate entry 13). (3) **RECOVERY EVENT (important lesson):** norwaywithmum had **no local source on the current MacBook and no git repo** — it existed live-only, and was reconstructed by mirroring the live site. (4) **norwaywithmum is now repo-backed** — new **PRIVATE** GitHub repo `sbrodie1978/norwaywithmum`. Everything else carried forward unchanged from rev 24. Changes in rev 24 (**estate-wide home-screen / bookmark icon kit added**): every live public property serves the **gold-flask mark** as its Apple touch icon + web-manifest icon. Kit source masters live in **`~/cruiselab/brand/`**. **NEW STANDING RULE: any new tool ships with the icon kit from day one.** Changes in rev 23 (**pre-launch: two tools temporarily withheld from public view**): **Ocean View** and **Shore Thing** are hidden from the public ahead of the social launch. They are still built, deployed and buildable, just delisted (moved to "In the Lab" on the hub, removed from the link hub, `noindex` on each). **To un-hide later:** revert each tool's card to a live Fleet card on the hub, re-add its link-hub row, delete the robots meta, redeploy all three. Changes in rev 22: **Audio standing rule added** to the social operating rules. Earlier rev notes (rev 18 to rev 21) covered Shore Thing v2 (the line/ship/date picker and the Widgety-swap-ready data layer), the Privacy policy launch, the Impact/eSIM commission workstream, and the All Aboard Store build and iteration; the substantive content of those is carried in the body below, updated for rev 29 where the de-monetisation touched it.

## What The Cruise Lab is

The Cruise Lab (thecruiselab.com) is Stuart Brodie's umbrella brand for a collection of **free** web tools built for the cruising community: "free web tools built by a cruiser, for cruisers." Each tool keeps its own name and identity as a member of "The Fleet"; the hub at thecruiselab.com is the landing page from which users pick a tool. New tools and services launch under the brand and get a card on the hub, with an "In the Lab" section teasing what's next. **The entire estate is now free, with no affiliate links and no paid offering (rev 29).** **Grand Voyage** (rev 26) is a free-play slot game whose bonuses showcase the Fleet. All tools carry a disclaimer that they are independent and not affiliated with or endorsed by Princess Cruises or any cruise line. (Forever Voyage, the former paid made-to-order keepsake-site service, was removed on 24 Oct 2026 when the estate went fully free; see rev 29 and estate entry 9.)

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

Fonts: Cinzel (500/600/700) for headings, Outfit (300–700) for UI/body, loaded from Google Fonts. Headline treatment: gold vertical gradient text. Cards: panel gradient background, panel-edge border, 14px radius, lift on hover. "Coming soon" cards: dashed border, sea-glass chip. Conventions: pure HTML/CSS/JS, single self-contained file per page where practical, no build step, no frameworks (Grand Voyage is the one exception with a tiny Python build step).

**Affiliate disclosure convention (rev 29):** the estate carries **no affiliate links** as of 24 Oct 2026 (all removed), so there are no commission disclosures to maintain. The standing independence disclaimer stays on every tool. If affiliate links are ever reintroduced, restore a discreet "may earn a commission" disclosure next to the links and in the footer, and keep commission *mechanics* out of marketing copy (the prior estate convention).

**Home-screen / bookmark icon (rev 24, standing):** the gold flask mark is the estate's app icon. Every live public property serves it via `<link rel="apple-touch-icon">` (180×180) + a `manifest.webmanifest` with 192/512 `any` and 192/512 `maskable` icons, plus PNG/`.ico` favicons. Source masters live in `~/cruiselab/brand/`. **Standing rule: any NEW tool ships with the icon kit from day one.** (GCBC is the one intentional exception: its own paper/ink identity. GetMyCruiseWeather uses its own ship mark, see entry 4. Grand Voyage uses the flask with its own manifest and standalone display, see entry 14.)

**Privacy policy maintenance rule (standing):** the estate-wide Privacy & Cookies policy at `hub/privacy.html` (estate entry 11) MUST be reviewed — and updated where needed — whenever a tool change would affect its statements. Triggers include: adding or changing an analytics/tracking service; adding a new affiliate partner or network; adding a new third-party embed or external API; anything that stores or transmits user data; or any new tool joining the estate. When the policy changes, bump its Version and Effective date. (Rev 29 did exactly this: removing all affiliates took the policy to Version 2.)

## Source of truth: the monorepo

All Cruise Lab source lives in the GitHub repo **sbrodie1978/thecruiselab** (public), cloned locally at `~/cruiselab` on Stuart's MacBook. Layout (rev 29, after the store and Forever Voyage folders were removed):

```
thecruiselab/
├── hub/                    → Pages project "thecruiselab"          → thecruiselab.com
│   ├── index.html            (hub landing page — 6 live Fleet cards)
│   └── privacy.html          (estate-wide Privacy & Cookies policy → /privacy, v2)
├── casinopoints/           → Pages project "sys-points"            → casinopoints.thecruiselab.com
│   ├── index.html            (cruise line chooser)
│   └── princess/index.html   (Sea You Soon calculator)
├── getmycruiseweather/     → Pages project "getmycruiseweather"    → getmycruiseweather.com / weather.thecruiselab.com
├── getmybartab/            → Pages project "getmybartab"           → bartab.thecruiselab.com
├── getmycruiseconnection/  → Pages project "getmycruiseconnection" → connection.thecruiselab.com
├── shorething/             → Pages project "shorething"            → shorething.thecruiselab.com
├── oceanview/              → Pages project "oceanview"             → watch.thecruiselab.com
├── links/                  → Pages project "links"                 → links.thecruiselab.com
├── slots/                  → Pages project "cruiselab-slots"       → slots.thecruiselab.com  [deploy slots/dist ONLY]
│   ├── src/                  (app.html + engine.js — the source of truth)
│   ├── static/               (icon kit + Grand Voyage manifest, copied into dist on build)
│   ├── tools/rtp-sim.js      (return-to-player simulator, Node)
│   ├── build.py              (builds dist/)
│   └── dist/                 (built output: the only thing deployed)
├── brand/                  → icon-kit source masters  [rev 24]
├── social/                 → strategy docs, idea bank, metrics, assets, relaunch post pack, plus video/
└── docs/
    └── cruiselab-master-context.md   (this document)
```

**REMOVED in rev 29:** the `allaboardstore/` folder and the `forevervoyage/` folder, plus the root-level `build-forever-voyage-sample.py` generator (git-removed, commit "Remove All Aboard Store and Forever Voyage"). Their Cloudflare Pages projects (`allaboardstore`, `forever-voyage`, `forever-voyage-sample`) were deleted and their custom domains (`store.thecruiselab.com`, `forevervoyage.thecruiselab.com`) detached.

**Home-screen icon files (rev 24):** every live public project root additionally carries `icons/` (7 PNGs), `favicon.ico`, and `manifest.webmanifest`, plus the head snippet in its `index.html`. Masters live once in `~/cruiselab/brand/`.

Exception: Good Cabin Bad Cabin keeps its own repo, sbrodie1978/goodcabinbadcabin (also public). **The GCBC clone does not yet exist on the new MacBook** — re-clone to `~/goodcabinbadcabin` when next needed. Workflow for any change: edit in the repo folder, deploy with wrangler, then commit and push. `.wrangler/` is gitignored.

## The estate — every property, where it lives

All web properties are Cloudflare Pages projects in Stuart's Cloudflare account (login stuartfbrodie@outlook.com, account ID 9c5f5919b1ef204bd2aacf415c814cda). Both registered domains are at Namecheap with DNS on Cloudflare. Cloudflare Email Routing is live on the thecruiselab.com zone. A census of every Pages project: `npx wrangler pages project list`.

### 1. The hub
- URL: https://thecruiselab.com (plus www and thecruiselab.pages.dev)
- Cloudflare Pages project: `thecruiselab` (production branch `main`)
- Repo path: `~/cruiselab/hub` (index.html + privacy.html)
- Content: hero with flask mark and wordmark, tagline, "The Fleet" divider with one card per live tool, then an "In the Lab" divider with coming-soon tiles.
- **Current Fleet cards (6 live as of 24 Oct 2026, rev 29, in order):** Good Cabin Bad Cabin (cabins.thecruiselab.com) · Sea You Soon (casinopoints.thecruiselab.com/princess/) · GetMyCruiseWeather (weather.thecruiselab.com) · GetMyBarTab (bartab.thecruiselab.com) · GetMyCruiseConnection (connection.thecruiselab.com) · Grand Voyage (slots.thecruiselab.com). **All Aboard Store and Forever Voyage cards were removed in rev 29** (both properties deleted). Verify live in Stuart's browser (do NOT trust Claude-side fetches of this page: see lessons).
- **In the Lab (3 tiles, dashed "Coming soon"):** Ocean View, Shore Thing, GetMyCruiseMap. (Ocean View + Shore Thing are temporarily withheld, not genuinely unbuilt — see rev 23.)
- **Footer:** independence disclaimer, a **"Privacy & Cookies" link → /privacy**, and the copyright line.
- **Impact.com site-verification meta tag** lives in `<head>` (`value="73cca54b-54cb-4ebc-a30a-35daad774ae5"`). It is harmless to leave (a verification string, not an active integration); leave it unless you specifically want it gone now the Impact workstream is wound down.
- Also served from this project: `privacy.html` → thecruiselab.com/privacy (entry 11).
- WARNING: before editing hub/index.html, always start from the live repo (`git pull` first), never a stale copy.

### 2. Good Cabin Bad Cabin — cabin scoring
- URL: https://cabins.thecruiselab.com (plus goodcabinbadcabin.pages.dev)
- Cloudflare Pages project: `goodcabinbadcabin`; Source: GitHub repo sbrodie1978/goodcabinbadcabin (public); **no local clone on the new MacBook yet**
- What it is: scores every cabin from the deck plans — quietness, motion, convenience, space — across five traveller profiles, with a cross-section of what's above/below/beside each cabin. Princess (17 ships, ~27,500 staterooms) and MSC (24 ships, ~43,500 staterooms) both LIVE.
- Structure: root index.html is a hand-maintained cruise-line chooser. Each line in its own folder: `/princess/` and `/msc/`.
- Design: GCBC keeps its own identity, distinct from the hub — paper/ink utilitarian look.
- Pipeline (Princess): frontend is GENERATED — edit `pipeline/build_frontend.py`, never `princess/index.html` directly.
- Pipeline (MSC): `pipeline/msc/` five-step chain; dev-only dependency PyMuPDF. Full harvest notes in `pipeline/msc/HARVEST.md`.
- Deploy: `cd app && npx wrangler pages deploy public --project-name=goodcabinbadcabin`

### 3. Casino Points (Sea You Soon) — casino comp points
- URL: https://casinopoints.thecruiselab.com (plus sys-points.pages.dev)
- Cloudflare Pages project: `sys-points` (production branch `production`: deploy with `--branch=production`); Repo path: `~/cruiselab/casinopoints`
- Structure: root index.html is a cruise-line chooser (Princess live; Carnival, Royal Caribbean, Norwegian coming soon). `/princess/` hosts the Sea You Soon calculator (SYS point system effective 1 Sep 2025).

### 4. GetMyCruiseWeather — port-by-port cruise weather
- URLs: https://getmycruiseweather.com (primary) and https://weather.thecruiselab.com (alias)
- Cloudflare Pages project: `getmycruiseweather` (production branch `production`: deploy with `--branch=production`); Repo path: `~/cruiselab/getmycruiseweather`
- Structure: multi-file static site — index.html (port picker), results.html, js/app.js, css/styles.css, data/ports.json (265 ports), assets, tools/port-validator.html.
- Data: Open-Meteo archive API, client-side, no key. Google Analytics installed.
- **Viator affiliate link-out REMOVED (rev 29):** the "Recommended shore excursions" card in `results.html`, the `buildViatorUrl()` / `updateViatorLink()` / `getPortNameById()` code and its four calls in `js/app.js`, and the `assets/viator-logo.png` + `viator-logo.svg` files are all gone. The old Viator IDs were pid `P00290711`, mcid `42383`. The tool no longer shows or links to excursions. **Orphaned Viator CSS (~lines 1127 to 1456 of `css/styles.css`) was left in place** — dead but harmless; strip in a later pass if wanted.
- Results deep-link format: `results.html?port=<id>&date=YYYY-MM-DD` (+optional `region`) — Shore Thing links into this per port day.
- KNOWN DATA GAPS (unchanged): ports.json has 49 coordinate-duplicate alias entries and is thin in the Caribbean (only 8 ports) and Alaska (missing Juneau/Skagway/Ketchikan). Shore Thing's ports.json carries the fix (86 `gw:false` top-ups). Backporting those to GetMyCruiseWeather is a queued task; also fix the misfiled "Sydney, Nova Scotia" (Oceania → North America).
- Uses Google Analytics (cookies) — the only estate tool that does; the Privacy policy describes this specifically.
- **Home-screen icon (rev 25): its OWN ship mark, NOT the estate flask.** If the estate icon kit is ever re-run across all tools, DO NOT overwrite GMCW's icons with the flask.

### 5. GetMyBarTab — drinks spend predictor
- URL: https://bartab.thecruiselab.com (Cloudflare Pages project `getmybartab`, production branch `main`); Repo path: `~/cruiselab/getmybartab` (single self-contained index.html ~41KB + README)
- What it is: predicts what a cruiser will really spend on drinks — per person, split sea/port days, output styled as a literal itemised bar tab — then compares against a package price *the user supplies*.
- CORE DESIGN PRINCIPLE (do not break): **line-blind on package prices** — the user pastes their quoted number. What we curate is slow-moving à la carte per-drink pricing: `GENERIC_PRICES` fallback + per-line `LINES` overrides (only Princess individually curated in v1). `PRICE_STAMP` shows the curation date (currently "July 2026"). No affiliate links.

### 6. GetMyCruiseConnection — WiFi, roaming & eSIM guide
- URL: https://connection.thecruiselab.com (Cloudflare Pages project `getmycruiseconnection`, production branch `main`); Repo path: `~/cruiselab/getmycruiseconnection` (single self-contained index.html ~42KB + README)
- What it is: decodes staying connected on a cruise — what works at open sea vs port days, ship WiFi vs roaming vs travel eSIMs, with recommended providers.
- **COMMISSION STATUS (rev 29): affiliate framing removed, no monetisation.** The provider recommendations (GigSky, RedBull Mobile, Airalo, Holafly, a VPN pick) remain as **plain, honest recommendation links** in the `LINKS` object. In rev 29 every `rel="noopener sponsored"` was changed to `rel="noopener"`, and all "Partner link(s) — we may earn a small commission" disclosures (comparison table, footer, and the sea/port/VPN plan blocks) were removed. The `${carrierPass}` US day-pass note was kept.
- **History of the (now-abandoned) affiliate workstream:** these links were never tracked affiliate links tied to a paying account — the eSIM affiliate workstream (Airalo/GigSky/Holafly via Impact; the Impact Marketplace application was declined for account 7483535) was never completed, so they never earned. The `LINKS` object still has internal `// TODO affiliate link` dev comments; these are not user-facing and were left in place (trivial tidy if wanted). **Do NOT re-wire affiliate tracking: the estate is deliberately free as of rev 29.**
- Key content facts (unchanged): standard travel eSIMs (Airalo, Holafly) work only on land networks (port days); GigSky (WMS Cellular at Sea) and RedBull Mobile Maritime (Telenor Maritime) are the two eSIMs that work at open sea; Starlink fleet-wide rollout makes ship WiFi the primary sea-day recommendation.

### 7. Shore Thing — port guides for your exact sailing
- **⚠️ WITHHELD FROM PUBLIC (15 Jul 2026, pre-launch):** delisted from the hub (an "In the Lab" coming-soon tile) and the link hub, `noindex` on `index.html` (line 4). Still built/deployed/buildable. To un-hide: restore its live Fleet card on the hub, re-add its link-hub row, delete the robots meta, redeploy. Editing caution: `index.html` has a SECOND `<head>` inside the downloadable-guide template, so a blanket `sed` on `<head>` double-inserts; edit precisely. **When un-hidden, also set `SHORE_THING_LIVE=true` in Grand Voyage so its Summit Rush bonus links here.**
- URL: https://shorething.thecruiselab.com (canonical shorething.pages.dev); Cloudflare Pages project: `shorething` (production branch `main`); Repo path: `~/cruiselab/shorething`
- What it is: the user enters their cruise ports in order with dates (or picks line → ship → sailing date) and gets a port-by-port guide — editorial blurb, quick-fact chips, a "Don't miss" list and a "Lab note" per port, plus a per-day **GetMyCruiseWeather** weather link. Readable on screen, printable, or downloadable as a standalone HTML file.
- **Viator link-out REMOVED (rev 29):** `viatorUrl()`, the per-day "Tours & excursions" buttons, the `noviator` flag, and the footer "Tours & excursions links go to Viator; we may earn a commission" disclosure are all gone, as is "tours" in the meta description and the pending-port note. The **"Weather that day"** button and everything else (the picker, editorial, print, download) are untouched.
- **v2 sailing picker (primary input):** three dependent dropdowns (line → ship → sailing date) resolve to a known itinerary and build the guide; the manual builder is the secondary path. Both call the same `buildGuide()`.
- **Data layer (Widgety-swap-ready):** `data/fleet.json`, `data/itinerary-templates.json` (authoring), `data/sailings.json` (GENERATED by `build_sailings.py`). The app reads sailing data ONLY via the `SailingSource` adapter in index.html (the single swap point for a future licensed feed). Seed: Princess only (16 ships, 5 templates → 37 sailings); 9 other Tier-1 lines stubbed.
- Data: `data/ports.json` — **302 ports** (`gw` flag controls the weather link); `data/guide-content.json` — editorial keyed by port id. **Editorial coverage: COMPLETE, all 302 ports.** Standing lesson: always validate every editorial key against `ports.json` before merging.
- Deploy: `npx wrangler pages deploy ~/cruiselab/shorething --project-name=shorething` — after editing `itinerary-templates.json`, run `python3 build_sailings.py` first.

### 8. Ocean View — live cruise cams & free cruise video
- **⚠️ WITHHELD FROM PUBLIC (15 Jul 2026, pre-launch):** delisted, `noindex`. Still built/deployed/buildable. To un-hide: as per Shore Thing.
- URL: https://watch.thecruiselab.com — canonical **oceanview-17z.pages.dev**; Cloudflare Pages project: `oceanview` (production branch `main`); Repo path: `~/cruiselab/oceanview`
- What it is: curated player for freely available cruise video — Live (Port Cams · Ship Cams · Ship Tracker) and Watch (Reviews & Tips · Golden Age).
- Legal posture: **embed, never rehost** — YouTube iframe, archive.org embeds, VesselFinder's embeddable map; PTZtv and cruise-line cams link-out only. These third-party embeds may set their own cookies (reflected in the Privacy policy).
- Everything driven by one `FEEDS` array. Deploy: `npx wrangler pages deploy ~/cruiselab/oceanview --project-name=oceanview`.

### 9. Forever Voyage — REMOVED (rev 29)
- **DELETED 24 Oct 2026.** Forever Voyage was the estate's only paid offering: a bespoke made-to-order keepsake "travel journal" website of a customer's own cruise, modelled on Stuart's norwaywithmum site. It was removed when the estate went fully free.
- What was torn down: Cloudflare Pages projects **`forever-voyage`** and **`forever-voyage-sample`** deleted; custom domain **`forevervoyage.thecruiselab.com`** detached (CNAME auto-removed); repo folder `forevervoyage/` and the root generator `build-forever-voyage-sample.py` git-removed; hub Fleet card removed; link-hub "Made to order" section removed; privacy-policy Forever Voyage references removed (v2); personal-registry rows for both FV and FV sample marked superseded.
- `forevervoyage.thecruiselab.com` and `forever-voyage.pages.dev` / `forever-voyage-sample.pages.dev` are now free. The old deployments remain rolled-backable at their `<hash>.pages.dev` URLs for a time, per Cloudflare retention, if the service is ever revived.
- **norwaywithmum is untouched and stays** (entry 13). It was only the *reference* for FV's sample; it is Stuart's personal site, nothing to do with income.

### 10. Link hub — links.thecruiselab.com (LIVE)
- URL: https://links.thecruiselab.com: Cruise Lab-styled bio-link page.
- **Current contents (rev 29):** 5 Fleet tools as buttons — Good Cabin Bad Cabin, Sea You Soon, GetMyCruiseWeather, GetMyBarTab, GetMyCruiseConnection — then "Everything at thecruiselab.com" and the independence-disclaimer footer. **Removed in rev 29:** the All Aboard Store row (it had been added to the live link hub at some point despite earlier docs saying it was still missing), the Forever Voyage "Made to order" section and divider, and the affiliate-disclosure footer line ("Some tools use partner links; we may earn a small commission"). Ocean View and Shore Thing remain off (pre-launch hide). Grand Voyage is deliberately NOT listed (Stuart's call: a casino-style game in a social bio is a poor fit).
- Pages project **`links`**, repo folder **`~/cruiselab/links`**, canonical **`links-a0e.pages.dev`**, production branch `main`. Deploy: `npx wrangler pages deploy ~/cruiselab/links --project-name=links`.
- Queued enhancement (still valid): append the inbound `?src=` parameter to every outbound tool button so per-platform footfall is attributable.

### 11. Privacy & Cookies policy (LIVE)
- URL: https://thecruiselab.com/privacy (also /privacy.html). Part of the `thecruiselab` hub Pages project — file at `~/cruiselab/hub/privacy.html`, deploys with the hub.
- Single self-contained HTML file in the Cruise Lab design system. Estate-wide policy covering every tool. UK GDPR / ICO-framed (Stuart Brodie, sole data controller, Dunfermline).
- **Version 2, effective 24 Oct 2026 (rev 29).** Rewritten to remove all affiliate / Amazon Associates / Viator / Impact references and the Forever Voyage paragraph: section 6 was repurposed from "Affiliate links" to **"No affiliate links or commission"**; the affiliate cookie bullet, affiliate data-sharing bullet, and FV "performance of a contract" legal basis were removed (email handling folded into legitimate interests); Grand Voyage was added to the covered-tools list. Section numbering 1 to 15 preserved. Still accurate and kept: no accounts/logins; client-side tools; localStorage on-device; Cloudflare Web Analytics cookieless; Google Analytics still on GetMyCruiseWeather; Ocean View third-party embeds; UK rights + ICO route; children/16; international transfers.
- Linked from the hub footer. Should be linked from every tool's footer over time (currently hub, Grand Voyage; All Aboard Store footer link died with the tool) — queued hygiene task.
- **Maintenance:** update this page and bump its Version/Effective date whenever a tool change affects its statements (see the maintenance rule under Brand and design system).

### 12. All Aboard Store — REMOVED (rev 29)
- **DELETED 24 Oct 2026.** All Aboard Store was the estate's only Amazon-Associates-monetised tool: a curated cruise-gear shop (six categories, 34 products, each a tag-carrying Amazon link) plus a "Leave at Home" anti-catalogue. It was removed when the estate went fully free.
- What was torn down: Cloudflare Pages project **`allaboardstore`** deleted; custom domain **`store.thecruiselab.com`** detached (CNAME auto-removed); repo folder `allaboardstore/` git-removed; hub Fleet card removed; link-hub row removed; personal-registry row marked superseded. The associated **Amazon Associates accounts (UK `thecruiselabh-21`, US `thecruiselabh-20`) were both closed**; OneLink was never set up; the 180-day/3-sales gate is moot.
- `store.thecruiselab.com` and `allaboardstore.pages.dev` are now free. The old deployment remains rolled-backable at its `<hash>.pages.dev` URL for a time if ever needed.

### 13. norwaywithmum — personal keepsake travel journal (NOT a Cruise Lab tool)
- URL: https://norwaywithmum.pages.dev (no custom domain); Cloudflare Pages project: `norwaywithmum` (production branch `main`, direct-upload)
- Repo: **`sbrodie1978/norwaywithmum` — PRIVATE** (family photos; the only private repo in the estate). Local source of record: **`~/norwaywithmum-site`** (its OWN folder, NOT in the monorepo).
- What it is: Stuart's private travel journal of his and his mum Frances's Norwegian fjords cruise (Sky Princess, 8–15 May 2026). It was the reference site behind the former Forever Voyage sample. **Rev 29 note: Forever Voyage was deleted, but norwaywithmum stays — it is Stuart's personal site and was never part of the monetisation.** The FV sample generator (`build-forever-voyage-sample.py`) that pulled from it was removed with FV; norwaywithmum itself is unaffected.
- Structure: `index.html` + `assets/` + `images/` (72 photos) + `videos/` + `downloads/` + icon kit. Total ~146 MB. Deploy: `npx wrangler pages deploy ~/norwaywithmum-site --project-name=norwaywithmum` (full folder only; direct-upload replaces the whole site).

### 14. Grand Voyage — free-play cruise slot machine (LIVE, launched 7 Oct 2026)
- URL: **https://slots.thecruiselab.com** (canonical **cruiselab-slots.pages.dev**). Custom domain Active / SSL enabled.
- Cloudflare Pages project: **`cruiselab-slots`**, production branch **`production`**: deploy with `--branch=production`.
- Repo path: **`~/cruiselab/slots`**. `src/app.html` + `src/engine.js` are the source of truth; `static/` holds the icon kit + manifest; `build.py` writes `dist/`; **only `dist/` is deployed**.
- What it is: a Vegas-style **free-play** slot in the Cruise Lab design system. **Play money only:** 5,000 credits, free top-ups, no purchases, no cash value, no prizes, **no affiliate links**, 18+ note + GamCare helpline. 5 reels × 3 rows, 20 lines; flask Wild, ship's-wheel Scatter. Four bonus games each themed on a Fleet tool, each with a "Try the real tool" link (Happy Hour Bar → GetMyBarTab, Upgrade Fever → GCBC, Sunshine Voyage → GetMyCruiseWeather, Summit Rush → Shore Thing, suppressed by `SHORE_THING_LIVE=false` until Shore Thing is un-hidden). Fixed cabin jackpots; built-in return ~93% (from `node tools/rtp-sim.js`).
- **Persistence:** localStorage `tcl-grand-voyage-v1`. Nothing transmitted.
- **Build & deploy:** `cd ~/cruiselab/slots && python3 build.py` then **from the `slots` folder** `npx wrangler pages deploy dist --project-name=cruiselab-slots --branch=production`. Never deploy from inside `dist`.

### Email routing (DONE — Cloudflare Email Routing)
Live on the thecruiselab.com zone, both forwarding to stuartfbrodie@outlook.com:
- **hello@thecruiselab.com** — public/customer address; the contact address in the Privacy policy. (Was also Forever Voyage's contact; FV is gone, the address stays as the general contact.)
- **social@thecruiselab.com** — social platform signups only.

## Social media

The Cruise Lab's social presence is **live** (accounts created 14 Jul 2026). Positioning: a **data brand**, not a travel vlog — *"the account that runs the numbers on cruising."* Every post is a finding, verdict, ranking or myth-bust drawn from the estate's own data. Fully **faceless** — the gold flask is the face. **Goal priority (rev 29, simplified): 1) follower & view growth, 2) traffic to the tools.** Affiliate revenue and Forever Voyage leads are retired as goals now the estate is free. Time budget: 3–5 hrs/week.

### Live accounts

| Platform | Identity | Status |
|---|---|---|
| YouTube | youtube.com/channel/UC_VM812P4JtvtqZkF3YN9Xg · @thecruiselabhq | ✅ name, bio link → links.thecruiselab.com |
| Instagram | instagram.com/thecruiselabhq | ✅ name, avatar, bio, link → links.thecruiselab.com |
| Facebook | facebook.com/thecruiselabhq (page id 61591669721543) | ✅ username, bio, banner/avatar, IG linked |
| TikTok | tiktok.com/@thecruiselabhq | ⚠️ linkless until 1,000 followers (personal account; Business switch needs a business-registration cert Stuart lacks). CTA is the typed brand URL. |
| Pinterest, X, Threads, Bluesky | — | Not yet created (Phase 0 of the campaign) |

- **Handle everywhere: `@thecruiselabhq`; display name: "The Cruise Lab."**
- **Bio (all platforms):** ⚓ The account that runs the numbers on cruising 🧪 Cabin scores · bar tabs · casino points · port guides 🔗 All free ↓ — link: links.thecruiselab.com.
- **Platform tiers:** Tier 1 (growth, identical short-form video) = TikTok · Instagram Reels · YouTube Shorts. Tier 2 = Facebook Page + Reels, Pinterest. Tier 3 (parked) = X · Threads · Bluesky; Reddit is listen/participate-only. Not doing: long-form YouTube, livestreams, paid ads.
- **Content pillars → Fleet mapping:** P1 Cabin Verdicts (GCBC — flagship) · P2 The Bar Tab (GetMyBarTab) · P3 Connected at Sea (GetMyCruiseConnection) · P4 Port Intel (Shore Thing + GetMyCruiseWeather) · P5 Casino Points & Cruise Maths (Sea You Soon). Series names: *Cabin Court*, *The Tab*, *Lab Report*, *Port File*.
- **Strategy documents (predate the rev-29 fully-free pivot — treat as historical, refresh when next touched):**
  - `cruiselab-social-playbook-v1-20260713.md` — the *how*. Still describes affiliate revenue as goal #3 and Forever Voyage leads as goal #4, and an affiliate funnel (Viator / eSIM / Amazon). Those are now retired.
  - `cruiselab-launch-campaign-v1-20260714.md` — the *what and when*. Its funnel ("the tool's own affiliate surfaces do the earning") is obsolete; there are no affiliate surfaces now. The structure (Phase 0 housekeeping, launch week, standing cadence, 90-day gate) still stands as a growth plan.
  - `launch-scripts-v1-20260715.md` — the four launch videos. **L2 ("5 things confiscated at the gangway") drives to the now-deleted All Aboard Store and must be pulled.** L4 ("the Paris day nobody packs for") points at GetMyCruiseWeather and is fine (the Viator layer it never used is gone anyway). L1 (GCBC) and L3 (GetMyBarTab) are fine.
  - `ideas.md` — the idea bank; the "Leave at Home / gear" angle tied to the store is dead, the rest stands.
- **Brand assets:** avatar/banner pack `cruiselab-social-assets-v1-20260714.zip`, deployed on all four platforms.
- **Intro promo video:** `cruiselab-intro-promo-v1-20260714.mp4` (committed at `social/video/`). Note the posted TikTok cut is a ~22s baked-audio version, not the 40s silent v1; its `render.py` is not yet in `social/video/src/`. Confirm the canonical cut and commit the renderer (open item from rev 28).
- **Launch video batch (BUILT + COMMITTED, rev 28):** L1 to L4 + intro at `~/cruiselab/social/video/` (commit `59723de`), full render source in `social/video/src/`. **STANDING RULE:** Cruise Lab video visuals are built via this code pipeline, never re-created from screen recordings. **Rev-29: L2 is now orphaned (store deleted) — drop it from the relaunch.**
- **Relaunch (rev 28):** post pack `social/cruiselab-relaunch-post-pack-v2-20261020.md` (commit `b6fdc13`), schedule intro → L1 → L3 → L4 → L2. **Rev-29: remove L2 from the schedule** (its destination is gone). Posting is done by Stuart from the phone apps; Claude writes content and captions.
- **Operating rules (short form):** faceless always; one idea per video; hook in 2 seconds, brand only at the end; max 1 tool demo in 6 posts; same handle/avatar/voice everywhere; reply to comments in the first hour; batch weekly; every claim backed by the estate's data; saves & shares are the growth currency. (The old "disclosures stay on; never commission talk in content" rule is now moot — there are no commissions.)
- **Audio standing rule (rev 22):** every published video gets an audio track (music bed + SFX; VO optional), but "sound-off first" still governs (captions always on, must work muted). TikTok Business account restricts to the Commercial Music Library — but TikTok is on a personal account for now (linkless), so this is latent.

## Deployment workflow (standard for all projects)

Deploys are done from Stuart's MacBook terminal with wrangler:

```bash
npx wrangler pages deploy ~/cruiselab/hub --project-name=thecruiselab            # hub + privacy.html
npx wrangler pages deploy ~/cruiselab/casinopoints --project-name=sys-points --branch=production
npx wrangler pages deploy ~/cruiselab/getmycruiseweather --project-name=getmycruiseweather --branch=production
npx wrangler pages deploy ~/cruiselab/getmybartab --project-name=getmybartab
npx wrangler pages deploy ~/cruiselab/getmycruiseconnection --project-name=getmycruiseconnection
npx wrangler pages deploy ~/cruiselab/shorething --project-name=shorething
npx wrangler pages deploy ~/cruiselab/oceanview --project-name=oceanview
npx wrangler pages deploy ~/cruiselab/links --project-name=links
cd ~/cruiselab/slots && python3 build.py && npx wrangler pages deploy dist --project-name=cruiselab-slots --branch=production   # Grand Voyage
```

**Removed in rev 29:** the `forever-voyage` and `allaboardstore` deploy lines (projects deleted). Outside the monorepo: GCBC (`cd ~/goodcabinbadcabin/app && npx wrangler pages deploy public --project-name=goodcabinbadcabin`) and **norwaywithmum** (`npx wrangler pages deploy ~/norwaywithmum-site --project-name=norwaywithmum`, branch `main`, full folder only). The Forever Voyage sample deploy is gone with the project.

After deploying, commit and push: `cd ~/cruiselab && git add -A && git commit -m "..." && git push`. Pages projects are direct-upload — pushing to GitHub does NOT auto-deploy.

**Deployment registry (rev 26):** every Cruise Lab Pages project should have a row in the **personal registry** (`personal-registry.pages.dev`; repo `sbrodie1978/personal-registry`; local clone at **`~/Downloads/personal-registry`**), group **"The Cruise Lab"**. The registry's site lives in **`dist/`**: edit `dist/index.html` (the `DATA` array; row = `[name, cf-project, primary.pages.dev, extra domains, note, superseded?]`), deploy **from the repo root** with `cd ~/Downloads/personal-registry && npx wrangler pages deploy dist --project-name=personal-registry --branch=production`. Clear any `dist/.wrangler/` cache before deploying. **Superseded entries are marked (`,…,1]` with a note), never deleted.** Rev 29 marked the All Aboard Store, Forever Voyage and Forever Voyage sample rows superseded this way.

Notes and lessons learned:
- **To delete a Pages project you must first detach its custom domain(s) (rev 29).** `wrangler pages project delete <name>` fails with "you must first delete all custom domains" while a custom domain is attached. Detach in the dashboard (Workers & Pages → project → Custom domains → the domain's ⋯ → Remove domain; it also removes the CNAME), then re-run the delete. This bit both the store (`store.thecruiselab.com`) and Forever Voyage (`forevervoyage.thecruiselab.com`).
- **Never deploy from inside a `dist/` folder** (leaves a `.wrangler/` cache that the next deploy uploads). Run from the project folder and pass `dist`.
- **A brand-new Pages project's hash deployment URL can be dead for a few minutes.** Verify bytes on the canonical URL.
- **Custom domain attach goes Initializing → Verifying → Active in about a minute on a same-zone domain.**
- **A live-only Pages site with no local source / no repo is a recovery risk** (proven with norwaywithmum). Every deployed site gets a git repo.
- **Claude's web fetch of Cruise Lab pages can be DAYS stale.** Never use Claude's fetch to verify a deploy — Stuart's curl/browser is canonical.
- **Edge-cache lag on a fresh deploy is normal.** Trust wrangler's "Uploaded N files" and the `<hash>.pages.dev` deployment URL.
- **Creating a new Pages project:** `npx wrangler pages project create <name> --production-branch=main`.
- **Never run `wrangler pages deploy` from `~`.**
- **Production branches differ per project (corrected rev 30):** `sys-points`, `getmycruiseweather` and `cruiselab-slots` have production branch `production`, as do the two registries; everything else (`thecruiselab`, `getmybartab`, `getmycruiseconnection`, `shorething`, `oceanview`, `links`) uses `main`. Deploying to the wrong branch silently creates a Preview and the live site never updates (a `main` deploy to a `production`-branch project lands as Preview with no obvious error). Verify with `npx wrangler pages deployment list --project-name=X`: the row marked Production shows the live branch.
- **pages.dev subdomains are a GLOBAL namespace** — read the actual URL from wrangler output.
- **Local/ISP DNS can lag a fresh custom-domain attach.** Confirm at source with `dig +short <domain> @anuj.ns.cloudflare.com`.
- **Stale uncommitted edits in a local clone block `git pull`.** Rev-29 hit this on the personal registry: after committing locally, a `git pull --rebase` cleanly placed the commit on top of someone else's Leven Thistle changes; then a redeploy was needed because the first deploy was built from `dist` before the rebase merged their rows in.
- **Facebook/Instagram/TikTok block Claude's server-side fetch entirely:** account work goes through Claude-in-Chrome. A fresh Claude-in-Chrome tab does NOT carry Stuart's logged-in session for those; **but the Cloudflare dashboard session IS shared** — rev 29 detached the two custom domains via Claude-in-Chrome on Stuart's already-logged-in dashboard. Claude-in-Chrome can only see/control tabs in its own group, not Stuart's existing tabs.
- **Affiliate networks are free for PUBLISHERS.** Impact publisher account: Stuart Brodie, ID 7483535 — **now unused (rev 29); the estate carries no affiliate links.** Close it if you want zero affiliate accounts.
- **Making sure no affiliate money ever reaches the bank (rev 29 lesson):** the reliable lever is removing the payout method/destination, not closing the account. Below-threshold balances roll over unpaid; Amazon won't release final earnings without a completed tax interview; Viator PayPal has NO minimum (so that's the real leak — remove it). Closing with no payout method set forfeits/withholds the balance.

## Backlog / ideas

- **Affiliate / monetisation: wound down (rev 29).** The estate is deliberately free with no affiliate links. The former commission workstream (Impact Marketplace re-request, Airalo/GigSky/Holafly via Impact or Awin, Amazon OneLink, real ASINs, the 180-day sales gate) is all **abandoned**. Remaining optional cleanup: (1) **close the Impact.com publisher account 7483535** if you want zero affiliate accounts (it earns nothing, no bank details, no urgency); (2) optionally remove the Impact site-verification meta tag from `hub/index.html`; (3) optionally tidy the `// TODO affiliate link` comments in GetMyCruiseConnection's `LINKS` object; (4) optionally strip the ~330 lines of orphaned Viator CSS from GetMyCruiseWeather's `styles.css`.
- **Social knock-on (rev 29):** pull **L2** ("5 things confiscated at the gangway") from the relaunch and shelve the **All Aboard Store promo video** — both point at the deleted store. Refresh the four social strategy docs for the fully-free pivot (retire goal #3 affiliate revenue, goal #4 FV leads, and the affiliate-funnel language) when next touched.
- **Grand Voyage follow-ups:** flip `SHORE_THING_LIVE=true` when Shore Thing is un-hidden; confirm the privacy-policy review; optional jackpot tuning. The Awin advertiser-terms check is now low-priority (no affiliate tools on the estate).
- **Personal registry hygiene:** deploy from the repo root (not inside `dist`); consider moving the clone out of `~/Downloads`.
- **Home-screen icon kit remaining coverage:** live on hub + estate tools + GetMyCruiseWeather (ship mark) + norwaywithmum (fjord mark) + Grand Voyage. Still to do when their moment comes: Ocean View & Shore Thing (when un-hidden), the Sea You Soon calculator sub-page, and GCBC (a paper/ink variant). (Forever Voyage and All Aboard Store icon tasks are moot — both removed.)
- **Audit the Cloudflare account for other live-only Pages sites with no repo.**
- **Link privacy policy from every tool's footer** (currently hub + Grand Voyage).
- **Un-hide Ocean View & Shore Thing when ready (rev 23):** restore each as a live Fleet card on the hub, re-add its link-hub row, delete the robots meta, redeploy; flip `SHORE_THING_LIVE` in Grand Voyage.
- **Campaign Phase 0 (still valid as a growth task):** TikTok display name + Business account (blocked on the business cert); create Pinterest / X / Bluesky / Threads; set `?src=`-tagged bio links per platform.
- **Link hub `src` pass-through:** forward the inbound `?src=` on every outbound tool button for per-platform footfall attribution.
- **Cloudflare Web Analytics across the estate:** add the snippet to every Pages project so tool sessions are measurable (only GetMyCruiseWeather currently has analytics).
- **Video assets still to commit + document (rev 28 follow-up):** the **Cost Creep series** (C1 to C5) still needs folding into `social/video/` with a commit and entry. (The All Aboard Store promo is now dead content.) Confirm the canonical intro cut and commit the intro's `render.py`.
- **Shore Thing v2 open threads:** fleet roster (9 remaining Tier-1 lines into `fleet.json`); itinerary-template seeding; Norway/North-Cape ports not yet in `ports.json`; Widgety license at a future pivot.
- **Backport Shore Thing's 86 `gw:false` top-up ports to GetMyCruiseWeather**, then flip their `gw` flags; fix the "Sydney, Nova Scotia" region misfile in GetMyCruiseWeather's ports.json.
- **GetMyBarTab follow-ups:** à la carte prices for more lines beyond Princess; better currency conversion. (The "real package links per line" item is now less relevant without a monetisation angle, but still a UX nicety.)
- **Ocean View v2 write-up** once the YouTube harvest completes.
- **GetMyCruiseMap** (announced on hub, not built): itinerary + photos → keepsake route-map print via print-on-demand. (Note: this would be a *paid* print product; it is on the roadmap but the estate is otherwise free — decide deliberately if/when built.)
- "Part of The Cruise Lab" footer badge inside the Sea You Soon Princess calculator.
- GCBC data-use permissions: written authority from Princess, MSC, P&O and Carnival.
- Casino points calculators for Carnival, Royal Caribbean, Norwegian.
- "My Cruise" anonymous cross-subdomain profile via `.thecruiselab.com` cookie (will require a privacy-policy cookie-section rewrite when built).
- Delete the redundant Netlify projects and the stale `~/Projects/goodcabinbadcabin` clone if still present.

## Working style

Stuart is technical and hands-on: he runs terminal commands himself (wrangler, curl, dig) and prefers being handed a file plus a one-liner deploy command over dashboard clicking. One terminal command at a time; he pastes the output back, which is the only evidence a step worked. Output-oriented sessions; informal, direct communication; honest pushback preferred; answers with a 1 to 10 confidence score where useful. Files come from `~/Downloads`. File-delivery discipline: unique versioned filenames, one attachment per message, multi-file deliveries as a single uniquely-named zip; every tool gets a git-committed folder with a README. One build conversation per tool at a time. **When a chat is lost/deleted, its outcomes are lost from Claude's memory — reconstruct into this doc promptly; this doc and the repo are the only durable records.**
