# All Aboard Store

Curated cruise-gear shop for The Cruise Lab, monetised via **Amazon Associates**.
Part of the Fleet at https://thecruiselab.com.

- **URL:** https://store.thecruiselab.com
- **Cloudflare Pages project:** `allaboardstore` (production branch `main`)
- **Repo path:** `~/cruiselab/allaboardstore` (this folder — single self-contained `index.html`, no build step)

## What it is

A single-page, Cruise Lab-styled store. **Landing shows a grid of category
tiles** (icon, name, short description, product count) — all visible at once,
no horizontal scrolling. Selecting a tile drills into that category's catalogue
(hash-routed, e.g. `#port`), with a "← All categories" back control. The
signature **"Leave at Home"** anti-catalogue (items banned on board) sits on the
landing below the category grid. Each product card is a whole-card link to Amazon
with the Associates tag; a minimal "Amazon ↗" marker signals the outbound link.
No prices and no Amazon product imagery (both restricted under the Associates
Operating Agreement outside Amazon's own tooling); cards use the estate's
icon-chip style instead.

### Navigation model
- **Home view** (`#` / no hash): category grid + Leave at Home.
- **Category view** (`#<cat-id>`): back link, category title + blurb, product grid.
- Hash-routed via `hashchange` → browser back button works; category links are
  shareable/deep-linkable. Unknown hashes fall back to the landing grid.

## How the affiliate links work

All editable data lives at the top of the `<script>` in `index.html`
(same convention as GetMyCruiseConnection's `LINKS` object):

- `AFFILIATE.tag` — the Amazon Associates **UK** tracking ID (`thecruiselabh-21`).
- `AFFILIATE.tagUS` — the US tracking ID, pending; used via OneLink mapping, not in URLs.
- `PRODUCTS[]` — one object per product: `{cat, icon, name, blurb, note, asin, q}`.

Link builder (`productUrl`): if `asin` is set, links deep to
`amazon.co.uk/dp/<ASIN>?tag=<tag>`; if `asin` is `""`, it falls back to a
**tag-carrying Amazon search** for `q`. Both forms earn commission on anything
bought in the resulting session. The launch state ships all-search-links (no
invented ASINs); curate real ASINs over time via SiteStripe on amazon.co.uk and
paste them in — one field per product.

**OneLink (pending):** once the US Associates account exists and is linked in
Associates Central (store-ID mapping), paste Amazon's OneLink `<script>` snippet
into the marked comment slot before `</body>`. It geo-redirects non-UK visitors
to their local Amazon storefront with the mapped tag. Until then UK links work
worldwide but only earn on amazon.co.uk purchases.

## Compliance (do not remove)

- The disclosure **"As an Amazon Associate, The Cruise Lab earns from qualifying
  purchases"** appears above the first link and in the footer — the wording and
  prominent placement are contractual under the Associates agreement.
- Every product link carries `rel="sponsored nofollow noopener"`.
- No prices, no Amazon product images (see above).
- Footer links the estate Privacy & Cookies policy (thecruiselab.com/privacy).
  Per the rev-19 standing rule, adding Amazon Associates as a network requires a
  privacy-policy wording check (Amazon was anticipated in v1 — confirm and bump
  version if changed).
- **180-day rule:** the Associates account needs 3 qualifying sales (not personal
  orders) within 180 days of application or it is closed and the tag dies.

## Deploy

```bash
# one-time project creation (mind the branch flag — see master context lessons)
npx wrangler pages project create allaboardstore --production-branch=main

# deploy (always the explicit path)
npx wrangler pages deploy ~/cruiselab/allaboardstore --project-name=allaboardstore
```

Then attach the custom domain `store.thecruiselab.com` in the Cloudflare dashboard
(Pages → allaboardstore → Custom domains), verify with
`curl -sL "https://store.thecruiselab.com/?v=$(date +%s)" | grep -o "All Aboard Store" | head -1`,
and commit:

```bash
cd ~/cruiselab && git add -A && git commit -m "All Aboard Store v1" && git push
```

## Editing

- Add a product: append an object to `PRODUCTS` with an existing `cat` id.
- Add a category: add to `CATEGORIES` and use its `id` in products.
- Swap the tag: one field, `AFFILIATE.tag`.
- Everything renders from data at load — no markup edits needed for catalogue changes.

Built 15 July 2026 (v1); v2 whole-card click target + minimal marker; v3 slim header + disclosure-to-footer; v4 same day — category-first UX: landing grid of category tiles (all visible, no horizontal scroll), hash-routed drill-down to per-category catalogue with back link. Single file, pure HTML/CSS/JS, Cruise Lab design system
(navy/gold, Cinzel + Outfit, standard tokens).
