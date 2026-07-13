# GetMyBarTab — cruise drinks spend predictor

Part of **The Cruise Lab** (thecruiselab.com). Tells cruisers what they'll
really spend on drinks — per person, split by sea days and port days — and
then compares that against a drinks package price *they* supply.

- **Live URL:** https://bartab.thecruiselab.com (Cloudflare Pages project `getmybartab`, production branch `main`)
- **Repo path:** `~/cruiselab/getmybartab` in the `sbrodie1978/thecruiselab` monorepo
- **Stack:** single self-contained `index.html` (~41KB) — pure HTML/CSS/JS,
  no build step. Cruise Lab design system (navy/gold, Cinzel + Outfit).
- **History:** v1 built and delivered 5 Jul 2026 (`getmybartab-v1-20260705.html`);
  recovered from that chat's attachments and deployed 12 Jul 2026 after the
  MacBook swap.

## The core design principle (do not break this)

**The tool is line-blind on package prices.** Package pricing changes
constantly and everyone is quoted a different post-discount number, so we
never store or guess package prices — the user pastes the per-person,
per-day price they were actually quoted, and we do a like-for-like
comparison. What we *do* curate is slow-moving à la carte per-drink pricing.

## Data model (all at the top of the `<script>`)

- `PRICE_STAMP` — human-readable "prices curated" date shown in the UI.
  Update it whenever prices are refreshed (currently "July 2026").
- `GENERIC_PRICES` — USD à la carte per-drink defaults (water, soft, coffee,
  beer, wine, cocktail, prosecco, champagne) used by every non-curated line.
- `LINES` — per-line overrides. **Only Princess is individually curated in
  v1** (its own prices, an 18% service charge, and the only real `pkgUrl`,
  pointing at Princess Plus/Premier). Other lines share GENERIC_PRICES.
  Adding a line = one new entry with `curated:true`, its prices, `sc`, and
  its package page URL.
- Currency conversion is approximate and fixed — onboard billing is
  USD-first; other currencies are display-only estimates (stated in the UI).

## Known v1 limitations / v2 backlog

- Curate à la carte prices for more lines (P&O, MSC, Royal Caribbean…).
- Real package-page links per line (only Princess in v1).
- Live-ish currency rates instead of fixed approximations.

## Deploy

```bash
npx wrangler pages deploy ~/cruiselab/getmybartab --project-name=getmybartab
```

Read the actual `.pages.dev` URL from wrangler's output (pages.dev names are
a global namespace and may be suffixed) and verify with `curl -L` on it.
Custom domain `bartab.thecruiselab.com` attaches via dashboard → project →
Custom domains.
