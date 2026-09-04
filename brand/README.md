# The Cruise Lab — Home-screen / Bookmark Icon Kit (v1, 4 Sep 2026)

Makes the gold flask mark appear when someone taps **Add to Home Screen** on a phone
(and as the browser-tab favicon on desktop), instead of iOS grabbing a page screenshot
and Android showing a generic globe.

## What's in here
```
favicon.ico                       ← desktop tab icon (16/32/48 multi-res)
manifest.webmanifest              ← Android/Chrome "add to home screen" metadata
HEAD-SNIPPET.html                 ← the <head> tags to paste into each index.html
flask-icon-master.svg             ← vector master (edit here, re-render if ever needed)
flask-icon-maskable-master.svg    ← vector master for the padded Android version
icons/
  apple-touch-icon.png    180×180  ← iPhone/iPad home screen (the important one for iOS)
  icon-192.png            192×192  ← Android home screen
  icon-512.png            512×512  ← Android splash / high-res
  icon-192-maskable.png   192×192  ← Android adaptive (padded so the crop can't clip it)
  icon-512-maskable.png   512×512  ← Android adaptive high-res
  favicon-32.png / favicon-16.png  ← PNG favicons
```

## How to install on ONE Pages project (e.g. the hub)
1. Copy the files into the project folder root so the paths line up with the tags:
   ```
   ~/cruiselab/hub/favicon.ico
   ~/cruiselab/hub/manifest.webmanifest
   ~/cruiselab/hub/icons/            (the whole icons/ folder)
   ```
2. `git pull` first (per the master-context rule), then paste the contents of
   `HEAD-SNIPPET.html` into the `<head>` of `~/cruiselab/hub/index.html`.
3. Deploy:
   ```
   npx wrangler pages deploy ~/cruiselab/hub --project-name=thecruiselab
   ```

## Doing it estate-wide
Home-screen icons are resolved **per origin**, so each subdomain that users might
bookmark needs its own copy. The `icons/` folder + `favicon.ico` + `manifest.webmanifest`
are identical everywhere — just drop the same three into each project root and paste the
same head snippet, then redeploy that project. Suggested order (the tools users actually
bookmark): hub → GetMyCruiseWeather → GetMyBarTab → GetMyCruiseConnection → Sea You Soon
→ All Aboard Store → link hub.

### One exception — Good Cabin Bad Cabin
GCBC keeps its own paper/ink identity (not navy/gold). The flask still works for estate
consistency, but if you'd rather it had a GCBC-matched icon, say so and I'll cut a
paper/ink variant. GCBC also lives in its own repo (`~/goodcabinbadcabin`).

## Notes / gotchas
- **iOS caches hard.** Existing home-screen shortcuts won't update; add a fresh one after
  deploying to see the new icon.
- **iOS uses `apple-touch-icon`, not the manifest**, for the home-screen image — that's why
  the 180×180 PNG is the critical file for iPhones.
- iOS rounds the corners itself; the icon is a full navy square on purpose (no transparency,
  or iOS would put a black box behind it).
- The head snippet does **not** force full-screen/standalone launch on iOS, so tapping the
  icon opens a normal Safari tab (safer — the user keeps the address bar). Say the word if
  you want true standalone app behaviour and I'll add `apple-mobile-web-app-capable`.
- Verify after deploy (once edge cache settles):
  ```
  curl -sIL https://thecruiselab.com/icons/apple-touch-icon.png | head -1
  curl -sIL https://thecruiselab.com/manifest.webmanifest | head -1
  ```

## Re-rendering the PNGs (only if the art changes)
Needs `librsvg2-bin` (`rsvg-convert`) + Pillow:
```
rsvg-convert -w 180 -h 180 flask-icon-master.svg -o icons/apple-touch-icon.png
rsvg-convert -w 192 -h 192 flask-icon-master.svg -o icons/icon-192.png
rsvg-convert -w 512 -h 512 flask-icon-master.svg -o icons/icon-512.png
rsvg-convert -w 192 -h 192 flask-icon-maskable-master.svg -o icons/icon-192-maskable.png
rsvg-convert -w 512 -h 512 flask-icon-maskable-master.svg -o icons/icon-512-maskable.png
```
