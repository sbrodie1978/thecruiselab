# Grand Voyage slots

A free play, cruise themed slot machine from The Cruise Lab. It is for entertainment only. There are no purchases, no cash value and no prizes. The four bonus games are each based on a Cruise Lab tool, so the game doubles as a shop window for the estate.

## Live deployment

- **URL:** https://cruiselab-slots.pages.dev (check the exact subdomain in `npx wrangler pages project list`)
- **Custom domain:** slots.thecruiselab.com (attached in the Cloudflare dashboard)
- **Cloudflare project:** cruiselab-slots
- **Production branch:** production
- **Access control:** public, but hidden. The page carries a `noindex` meta tag and an `X-Robots-Tag: noindex` header, and is not linked from the hub until launch.

## What it does

- 5 reels, 3 rows, 20 fixed paylines, wins pay left to right.
- The flask (estate brand mark) is wild. The ship's wheel is the scatter.
- Three or more ship's wheels trigger a full screen bonus wheel that picks one of four bonuses. Four wheels double the bonus, five multiply it by five. Each bonus is its own animated scene with intro and outcome slams, floating wins, sound, a finale count up and a coin shower.
  - **Happy Hour Bar** (GetMyBarTab). Pick glasses off a back bar. Drinks add to the tab. Happy Hour raises the multiplier on later drinks, Top Shelf doubles the tab, beating the drinks package price doubles the whole tab at closing. Two last orders bells close the bar.
  - **Upgrade Fever** (GCBC). Open cabin doors across three decks. Prizes add up, upgrade keys move a marker up a ship cross section from Inside x1 to Suite x4, and the final grade multiplies everything. Extra keys at Suite pay a perk. Three bad cabins and you check out.
  - **Sunshine Voyage** (GetMyCruiseWeather). Played on the main reels. A ship sails a six port route map. Each port gets a forecast with live sky and weather effects: rainbow x5, sunshine x3, cloud x2, rain x1, storm cancels the port. Every wild that lands is held for the rest of the voyage.
  - **Summit Rush** (Shore Thing). Climb a mountain trail past eight stops for bigger prizes, with a ticking clock and a suspense beat on every push. A tuk-tuk can skip a stop for free. Push too far and the ship sails without you.
- Four fixed cabin jackpots, not progressive. Each pays a set multiple of the current total bet (Inside 2x, Oceanview 4x, Balcony 8x, Suite 20x), so the panel values change when the bet changes. Odds per paid spin are the same at every bet: Inside 1 in 50, Oceanview 1 in 100, Balcony 1 in 200, Suite 1 in 500, so one lands about every 27 spins. The odds are shown on the panel. Every jackpot shows a splash banner over the reels, scaled up by tier, and closes itself or on tap. Inside and Oceanview do not stop autoplay. Balcony and Suite do.
- Layout fits the screen. Phones stack everything with the reels as wide as the screen allows. Wide screens (landscape, 860 pixels and up) put the reels on the left, sized to fill the screen height, with the logo, jackpots and controls in a 300 pixel column on the right. The jackpot row is about a quarter of the reel height on phones.
- Full screen button, and the F key, on browsers that support the Fullscreen API. iPhone Safari does not, so the button hides itself there. On iPhone, Share then Add to Home Screen opens the game without the browser bars.
- Big win celebrations with a coin shower, autoplay (10, 25, 50, 100), quick spin, sound toggle, pay table, free top ups.
- **Ship's ledger.** Shows spins, credits staked and won, the player's actual return, how far the house is up, and the built in return. This is the "we run the numbers" angle.
- After each bonus, a "Try the real tool" link to the matching Cruise Lab site.
- Player state (balance, bet, ledger, settings) is kept in the browser's localStorage under `tcl-grand-voyage-v1`. Nothing is sent anywhere.

## The maths

- Built in return is about 93%. Measured by `tools/rtp-sim.js` over two million simulated spins.
  - Line wins about 47%, bonuses about 30%, jackpots about 16%.
  - The Summit Rush figure assumes the player cashes out at step 5. Players who push further or stop earlier get a slightly different return.
- A bonus triggers roughly once every 77 spins. Each bonus averages 20 to 26 times the bet.
- If you change `PAYS`, `WEIGHTS`, `JACKPOTS` or any bonus table in `src/engine.js`, rerun the simulation and update `THEORETICAL_RTP` in `src/app.html` and the ledger copy.

```
node tools/rtp-sim.js
```

## Version history

- v9 (7 Oct 2026). Jackpot splash banner over the reels for every jackpot: rotating rays in a colour per tier, JACKPOT ribbon, tier icon (door, porthole, balcony, crown), 1 to 4 stars, count up, sparkle bursts, tiered fanfare. Balcony and Suite also shake the frame and shower coins.
- v8 (7 Oct 2026). Jackpots much more frequent (1 in 50 to 1 in 500) and much smaller (2x to 20x the bet). Line pays trimmed about 13% to keep the return near 93%.
- v7 (7 Oct 2026). Wide screens and full screen now fill the full height. Reel rows can stretch up to 1.3x taller than wide, and the layout is centred vertically. Side column widened to 300 pixels.
- v6 (7 Oct 2026). Jackpots shrunk to one compact row. Reels sized to fill the screen, with a two column layout on wide screens. Full screen option and home screen web app tags.
- v5 (7 Oct 2026). Jackpots no longer progressive. Fixed multiples of the bet with published odds. Inside and Oceanview much smaller and far more frequent. Line pays trimmed about 10% to keep the return at about 93%.
- v4 (7 Oct 2026). Fix: landing on Voyage from the bonus wheel left the wheel screen covering the reels. Wheel labels now always fit.
- v3 (7 Oct 2026). Progressive jackpot panel. All four bonuses rebuilt as full screen animated scenes with deeper mechanics. Return retuned to about 93%.
- v2 (4 Oct 2026). iPhone sound fixes.
- v1 (4 Oct 2026). First build.

## How it is built

- **Stack:** single file HTML, CSS and vanilla JavaScript. No framework.
- **Dependencies:** none at runtime apart from Google Fonts (Cinzel and Outfit, the estate fonts). Symbols are inline SVG. Sound is synthesised with the Web Audio API, so there are no audio files.
- **Build step:** `python3 build.py`. It inlines `src/engine.js` into `src/app.html` and writes `dist/index.html` and `dist/_headers`.
- **Source of truth:** `src/app.html` (layout, styling, game flow, the four bonus scenes) and `src/engine.js` (reel strips, paytable, paylines, bonus tables). **Never hand edit `dist/index.html`.** It is a build output and is overwritten every build.

## Repository layout

```
slots/
  src/app.html        page template, styles, game flow and bonus screens
  src/engine.js       maths: reel strips, paytable, paylines, bonus tables
  tools/rtp-sim.js    return to player simulation (Node)
  build.py            builds dist/ from src/
  dist/index.html     built artefact, the only thing deployed
  dist/_headers       Cloudflare Pages headers (noindex)
  README.md           this file
  DEPLOY.md           deployment procedure
  .gitignore
```

Only `dist/` is deployed, so the README, source and simulator are never public.

## Running locally

```
python3 build.py
open dist/index.html
```

Add `?debug=1` to the URL to get test hooks in the browser console:

- `GV.wheel()` triggers the bonus wheel. `GV.wheel('weather')` forces where it lands (bartab, cabin, weather, excursion)
- `GV.bonus('bartab')`, `GV.bonus('cabin')`, `GV.bonus('weather')`, `GV.bonus('excursion')` jump straight into Happy Hour Bar, Upgrade Fever, Sunshine Voyage or Summit Rush. Add a second argument of 4 or 5 to test the scatter multipliers.
- `GV.jackpot('inside')` awards a jackpot (inside, oceanview, balcony, suite)
- `GV.big(50)` shows a big win of 50 times the bet

## Configuration

All in the config block near the top of the second script in `src/app.html`:

- `START_BALANCE` free play credits on start and top up (5,000)
- `THEORETICAL_RTP` text shown in the ledger
- `SHORE_THING_LIVE` set to `true` when Shore Thing is revealed. Until then Summit Rush shows no Shore Thing name or link.
- `TOOLS` names, URLs and one line blurbs for the "Try the real tool" links. Check the blurbs still describe each tool accurately.

No secrets, no environment variables, no Functions.

## Deploying

See `DEPLOY.md`.

## Known limitations

- It is a polished browser game, not a licensed casino cabinet. Scenes are SVG, CSS and canvas. No 3D, no video.
- Full screen may be blocked inside embedded previews such as the claude.ai artifact frame. If so the game says so. It works on the deployed site and when opening dist/index.html directly.
- The bonus scenes were tuned on a 390 pixel wide phone and a desktop browser. Very short landscape screens may need scrolling in Upgrade Fever.
- The return figure is from simulation, not a certified test.
- Google Fonts are the one external request. If they fail, it falls back to Georgia and system fonts.
- The "Try the real tool" blurbs were written from the tool names and the brief, not from the live sites. Worth a check.
- Gambling content: kept clearly free play with an 18+ note and the GamCare helpline. Check Awin advertiser terms before linking it from the hub, as some travel advertisers restrict gambling content on publisher sites.

## Contacts

- **Owner:** Stuart Brodie
- **Platform:** Cloudflare account stuartfbrodie@outlook.com, GitHub sbrodie1978
