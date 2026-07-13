# Ocean View (v2) — live cruise cams & free cruise video

Part of **The Cruise Lab** (thecruiselab.com). A curated player for freely
available cruise video: live port webcams, cruise-line ship cams, a live ship
tracker, cruise creators' reviews and tours, and ocean liner films from the
golden age.

- **Live URL:** https://watch.thecruiselab.com (Cloudflare Pages project `oceanview`, production branch `main`)
- **Repo path:** `~/cruiselab/oceanview` in the `sbrodie1978/thecruiselab` monorepo
- **Stack:** single self-contained `index.html` — pure HTML/CSS/JS, no build
  step, no dependencies. Cruise Lab design system (midnight navy / champagne
  gold, Cinzel + Outfit, standard tokens).

## The legal posture (do not break this)

**Embed, never rehost.** Nothing is downloaded, re-encoded or re-served:

- YouTube content plays via the official iframe player, so creators keep their
  views and ad revenue.
- Internet Archive films play via archive.org's official embed player.
- The ship tracker is VesselFinder's official free embeddable map
  (vesselfinder.com/embed).
- PTZtv's business is ad-funded viewing on their own sites (re-streaming
  prohibited), so beyond their own YouTube rolling stream, PTZtv ports are
  **link-out cards** to their sites — never framed or scraped.
- Cruise-line ship cams are link-out cards to the lines' own pages.
- Sources are credited on every card, in the player, and in the page footer.

## How the feed list works

Everything on the page is driven by the single `FEEDS` array at the top of the
`<script>` block. Add, remove or swap a feed by editing one entry; nothing else
needs touching. Four feed kinds:

| kind         | id needed                  | use for |
|--------------|----------------------------|---------|
| `yt-video`   | YouTube **video** id       | One video or live stream. For live cams this is the only option — YouTube retired the old `live_stream?channel=` embed (confirmed dead 12 Jul 2026). When a cam's stream rotates, get the new id from `youtube.com/channel/<UC id>/streams`. |
| `yt-uploads` | channel id with `UC` → `UU`| A channel's all-uploads playlist — plays their latest videos. No stale video IDs to maintain. |
| `archive`    | archive.org identifier     | An Internet Archive film — the id from its `archive.org/details/<id>` URL. |
| `link`       | none (uses `srcUrl`)       | Anything that can't or shouldn't be embedded; card opens the source in a new tab. |

Finding a YouTube channel id: open the channel page → View Source → search
`channelId`. IDs are **case-sensitive** — copy exactly. Tracker regions are
the `TRACKER_PRESETS` array.


## v2 (13 Jul 2026) — the app re-imagined

Four views behind the nav pills: **Harbour** (the "EPG" re-imagined — My Deck,
Live now with local time + day/night per port, Fresh reviews, archive rail),
**Live** (Port Cams / Ship Cams / VesselFinder tracker with region presets),
**Ships** (top-3 most-viewed reviews for ~175 ships across 12 lines, from
`data/reviews.json` — see `pipeline/README.md` for the harvest), and **Watch**
(creators + Golden Age films). Product promises: nothing autoplays, everything
visible is free and watchable, no accounts.

- **My Deck**: heart anything; persisted in `localStorage` key `ov-deck`. No
  accounts by design.
- **Search**: press `/` anywhere. Client-side over FEEDS + the ship catalogue,
  grouped results, every hit playable.
- **Embed-first rule**: all reviews/creators/films play in the in-page modal
  via official embeds (URL never leaves watch.thecruiselab.com); link-out cards
  remain only where the owner requires on-site viewing (PTZtv, cruise-line cams).
- **Data**: `data/reviews.json` is fetched at runtime — deploy the folder and
  the app picks up each day's harvest automatically. Ships with no reviews yet
  render a graceful "being gathered" state. `window.__REVIEWS__` overrides the
  fetch (used by the jsdom test suite).
- **Cards**: hearts sit on a stretched invisible `.cover` action layer —
  never nest interactive elements (the HTML parser ejects them; this bit us).
- `?debug=1` still renders every embed + the tracker for post-deploy sweeps.

## Verification

`?debug=1` on the URL renders every embed inline on one page for a quick
eyeball sweep — use after any feed change and after each deploy.

Verified live in production (12 Jul 2026 sweep via Claude-in-Chrome): both
creator uploads embeds, all three archive.org films, the VesselFinder
tracker, and the Southampton Cruise Cam video id. Solent Ships and PTZtv
run several simultaneous streams — pick the right one from their /streams
page, not the /live redirect (PTZtv's /live goes to their airport cam).

All link-outs click-checked 12 Jul 2026. Corrections made in that sweep:
Princess bridgecams moved to `/ships-and-experience/ships/bridgecams`
(old `/cruise-ships/bridge-cams/` 404s); AIDA has no all-fleet page, so
the card targets the flagship's official bugcam
(`aida.de/schiffe/aidacosma/bugcam` — per-ship pattern); Viking's own
PANOMAX pages (`viking.panomax.com/<ship>`) were down entirely, and TUI's
`meinschiff.com/webcams` silently redirects to the homepage, so both cards
target Cruising Earth's per-line indexes; and "Ben & David" is **Cruise
With Ben and David** at `youtube.com/@Cruisewith` — the obvious-looking
`@BenandDavid` is an unrelated comedy channel. Creator handles verified:
@HarrTravel, @LaLidoLoca, @Cruisewith, @CruiseTipsTV.

## Known behaviours

- A `yt-live` channel that isn't currently streaming shows YouTube's own
  "offline" panel inside the player — the modal's footer "Open at source"
  button is the escape hatch. The player shows a loading/offline hint behind
  the iframe.
- Closing the modal empties the iframe, which stops playback/audio.
- iOS Safari caches hard — fully close and reopen the tab after a deploy.

## Deploy

```bash
npx wrangler pages deploy ~/cruiselab/oceanview --project-name=oceanview
```

First-time setup: create the Pages project (`npx wrangler pages project create
oceanview --production-branch=main`), deploy, then attach the custom domain
`watch.thecruiselab.com` in the Cloudflare dashboard (Pages → oceanview →
Custom domains). Verify with `curl -L https://oceanview.pages.dev` after
deploying. Commit and push from `~/cruiselab` as usual — Pages projects are
direct-upload, so wrangler is the deploy mechanism, not git.

## v2 ideas (parked)

- "Sail-away now": surface ports with an imminent departure.
- Favourites via localStorage (fine on a real deployed site).
- Weather chip per port cam via GetMyCruiseWeather / Open-Meteo.
- More port cams (Galveston, Kiel, Vancouver, Funchal, Juneau) once their
  YouTube channel ids are harvested; more Golden Age films from archive.org.
- Auto-detect a dead embed and surface the offline state proactively.
