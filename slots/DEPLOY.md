# Deploying Grand Voyage slots

## Prerequisites

- Node 22 (`nvm use 22`)
- Wrangler 4.x via `npx wrangler`
- Python 3 for the build
- Logged in to the Cloudflare account that holds the `cruiselab-slots` Pages project

## First time only

Create the Pages project with `production` as its production branch:

```
npx wrangler pages project create cruiselab-slots --production-branch=production
```

Then in the Cloudflare dashboard, Pages, cruiselab-slots, Custom domains, add `slots.thecruiselab.com`. The Activate click can fail silently. The domains list showing it as Active is the only proof.

## Build

```
python3 build.py
```

Output lands in `dist/`. Only ever deploy `dist/`. It should contain `index.html`, `_headers`, `favicon.ico`, `manifest.webmanifest` and `icons/` (7 PNGs), 11 files in all. The build warns if the icon kit is missing from `static/`.

## Deploy

Run from the `slots` folder, pointing at `dist`. Deploying from inside `dist` leaves a `.wrangler` cache there, which would then get uploaded:

```
npx wrangler pages deploy dist --project-name=cruiselab-slots --branch=production
```

`--branch=production` is required. Without it the deploy lands as a preview and never goes live. If the output shows `Deployment alias URL: main.` it went to preview.

## Verify

1. **File count.** Wrangler should report up to 10 files plus `_headers` on a full upload. On later deploys, `Uploaded N files` with N of at least 1 confirms something changed. 0 means nothing changed.
2. **Bytes, not status codes.** Compare the live size with the local file:

   ```
   wc -c < dist/index.html
   ```

   ```
   curl -s "https://cruiselab-slots.pages.dev/?cb=$(date +%s)" | wc -c
   ```

   The two numbers should match. Use the deployment hash URL from the wrangler output if the custom domain lags behind the edge cache.
3. **Icon.** `curl -sIL https://slots.thecruiselab.com/icons/apple-touch-icon.png | head -1` should be `HTTP/2 200`, and `grep -c apple-touch-icon dist/index.html` should be 1.
4. **Headers.** `curl -sI "https://slots.thecruiselab.com/?cb=$(date +%s)" | grep -ic robots` should print 0. The game is launched, so there is no noindex.

## Commit

From the monorepo root:

```
git add slots
git commit -m "Describe the actual change"
git push
```

## Registry

Add or update the row in the `The Cruise Lab` group of `sbrodie1978/personal-registry`, then deploy that with `--branch=production`. See its own README.

## Rollback

Old deployments stay live at their hash URLs. Roll back from the Cloudflare dashboard (Deployments, pick the previous one, Rollback), or check out the previous commit, rebuild and redeploy.
