# GetMyCruiseConnection — cruise WiFi, roaming & eSIM guide

Part of **The Cruise Lab** (thecruiselab.com). Decodes staying connected on
a cruise: what actually works at open sea versus what only works on port
days, ship WiFi versus roaming versus travel eSIMs, with affiliate-linked
recommendations.

- **Live URL:** https://connection.thecruiselab.com (Cloudflare Pages project `getmycruiseconnection`, production branch `main`)
- **Repo path:** `~/cruiselab/getmycruiseconnection` in the `sbrodie1978/thecruiselab` monorepo
- **Stack:** single self-contained `index.html` (~42KB) — pure HTML/CSS/JS,
  no build step. Cruise Lab design system (navy/gold, Cinzel + Outfit).
- **History:** v1 built 5 Jul 2026, iterated to **v3 on 6 Jul 2026**
  (`getmycruiseconnection-v3-20260706.html` is the deployed version);
  recovered from that chat's attachments and deployed 12 Jul 2026 after the
  MacBook swap.

## Affiliate infrastructure (the monetisation layer)

All partner URLs live in **one `LINKS` object** at the top of the `<script>`
block — Airalo (via Impact), Holafly (coupon code), GigSky, RedBull Mobile,
and the VPN pick. Swapping or updating an affiliate link is a one-line edit.
Affiliate `rel="sponsored"` attributes are added in the JS card templates
(not hard-coded in the static HTML), and "Partner links — we may earn a
small commission" disclosure copy appears beside every recommendation block
and in the footer. Keep the disclosures if the copy is ever reworked.

## The key content facts (verified during the original build)

- Standard travel eSIMs (Airalo, Holafly) work **only on land networks** —
  they are port-day tools and do nothing at open sea.
- Only two consumer eSIMs work at open sea: **GigSky** (WMS Cellular at Sea
  network) and **RedBull Mobile Maritime** (Telenor Maritime network). They
  run on different maritime networks, so ship compatibility must be checked
  in each provider's app before buying. At-sea speeds are modest (~1–4 Mbps).

## Deploy

```bash
npx wrangler pages deploy ~/cruiselab/getmycruiseconnection --project-name=getmycruiseconnection
```

Read the actual `.pages.dev` URL from wrangler's output (pages.dev names are
a global namespace and may be suffixed) and verify with `curl -L` on it.
Custom domain `connection.thecruiselab.com` attaches via dashboard →
project → Custom domains.
