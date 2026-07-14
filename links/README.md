# The Cruise Lab — Link Hub (links.thecruiselab.com)

The self-hosted "link in bio" page for The Cruise Lab's social accounts. A single
Cruise Lab-styled page (navy/gold, animated flask, Cinzel) with one button per Fleet
tool in hub order, plus Forever Voyage set apart at the bottom as the paid offering.
On-brand, free, and keeps the click analytics in-house — the deliberate alternative
to Linktree.

Set this as the bio link on every social platform (@thecruiselabhq) once it's live.

## What it is
- Single self-contained `index.html` (~14KB, no build step, no frameworks, no JS beyond
  the CSS flask animation).
- Uses the exact Cruise Lab design tokens and the animated flask mark, lifted from the
  live hub so it stays pixel-consistent with the estate.
- Each tool button carries the tool's own icon (the same SVGs used on the hub cards), so
  the buttons read as mini Fleet cards rather than generic link bars.
- Fleet tools listed in hub order: Good Cabin Bad Cabin · Sea You Soon · GetMyCruiseWeather
  · Ocean View · GetMyBarTab · GetMyCruiseConnection · Shore Thing.
- Forever Voyage is separated under a "Made to order" divider with a gold-tinted card —
  the paid/bespoke offering, kept distinct from the free tools.
- Footer carries the standard independence disclaimer + affiliate disclosure (kept per
  estate convention).

## Accessibility / quality floor
- Responsive, mobile-first (max-width 520px, big tap targets).
- Visible keyboard focus ring (gold) on every link.
- `prefers-reduced-motion` respected — the flask waves freeze.
- Semantic `<nav>` groupings; icons are `aria-hidden`.

## How to update
When a tool is added, removed or reordered on the hub, mirror the change here: edit the
link rows in `index.html`. To keep icons/URLs consistent, copy them from the live hub
(`hub/index.html`) rather than hand-typing — the tool icons are the `.tool-icon` SVGs and
the URLs are the card `href`s. Keep Forever Voyage in the separate "Made to order" group.

## Where it's deployed
- URL: https://links.thecruiselab.com
- Cloudflare Pages project: `links` (production branch `main`)
- Repo path: `~/cruiselab/links` (single index.html + this README)

## Deploy
```bash
# First time only — create the Pages project with the correct production branch:
npx wrangler pages project create links --production-branch=main

# Deploy (always pass the explicit folder path):
npx wrangler pages deploy ~/cruiselab/links --project-name=links

# Verify against the canonical .pages.dev URL printed in wrangler output
# (pages.dev is a global namespace — read the actual URL, it may be suffixed):
curl -sL <the-printed-pages-dev-url> | grep -o "<title>.*</title>"
```

## Attach the custom domain
Cloudflare dashboard → Pages → `links` → Custom domains → Set up → `links.thecruiselab.com`
→ Continue → Activate. Same-zone attachment goes Initializing → Verifying → Active in ~1–2 min.
The definitive success check is the domain appearing in the project's Custom domains list.

## After deploy
Set `https://links.thecruiselab.com` as the bio link on TikTok, Instagram, YouTube,
Facebook, Pinterest, X, Threads and Bluesky (replacing the interim thecruiselab.com link).
