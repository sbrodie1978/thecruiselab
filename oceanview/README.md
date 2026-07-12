# Ocean View — live cruise cams & free cruise video

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
| `yt-live`    | YouTube **channel** id     | A channel's current live stream. Most durable — follows whatever the channel streams, survives stream-ID rotation. Prefer this for port cams. |
| `yt-uploads` | channel id with `UC` → `UU`| A channel's all-uploads playlist — plays their latest videos. No stale video IDs to maintain. |
| `archive`    | archive.org identifier     | An Internet Archive film — the id from its `archive.org/details/<id>` URL. |
| `link`       | none (uses `srcUrl`)       | Anything that can't or shouldn't be embedded; card opens the source in a new tab. |

Finding a YouTube channel id: open the channel page → View Source → search
`channelId`. IDs are **case-sensitive** — copy exactly. Tracker regions are
the `TRACKER_PRESETS` array.

## Verification

`?debug=1` on the URL renders every embed inline on one page for a quick
eyeball sweep — use after any feed change and after each deploy.

Verified at build (12 Jul 2026): Solent Ships channel id, PTZtv channel id,
Emma Cruises and Tips For Travellers channel ids, all three archive.org film
ids, the VesselFinder embed pattern, and the PTZtv link-out URLs.

**Not yet click-checked** (a wrong path just lands somewhere on the right
site, but tidy up when convenient): the four cruise-line ship-cam URLs
(Princess / AIDA / Viking / TUI) and the four creator `@handle` link-outs
(Harr Travel, La Lido Loca, Ben & David, CruiseTipsTV).

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
