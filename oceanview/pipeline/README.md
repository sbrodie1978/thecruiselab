# Ocean View — Ship Reviews harvest pipeline

Builds `data/reviews.json` for the Ocean View v2 "Ship Reviews" section: the
top 3 most-viewed **embeddable** YouTube tours/reviews for every ship across
the 12 leading cruise lines (~175 ships, ~525 videos).

- **Lives at:** `~/cruiselab/oceanview/pipeline/harvest_reviews.py`
- **Output:** `~/cruiselab/oceanview/data/reviews.json` (deployed with the app)
- **Dependencies:** none — Python 3 stdlib only. Needs a YouTube Data API v3 key.

## Getting an API key (one-off, ~10 minutes, free, no billing)

1. https://console.cloud.google.com → sign in with any Google account
2. Top bar project picker → **New Project** → name it `cruiselab` → Create
3. Menu → **APIs & Services → Library** → search **YouTube Data API v3** → **Enable**
4. **APIs & Services → Credentials → + Create credentials → API key** → copy it
5. Recommended: **Edit key → API restrictions → Restrict key → YouTube Data API v3**

**NEVER commit the key** — this repo is public. It is read from the
`YT_API_KEY` environment variable only.

## Running

```bash
export YT_API_KEY="paste-key-here"
python3 ~/cruiselab/oceanview/pipeline/harvest_reviews.py
```

Quota maths: ~101 units/ship against a 10,000-unit free daily quota, so
**~99 ships/day**. The script saves after every ship and exits cleanly on
quota exhaustion; run it again the next day and it resumes automatically.
Full fleet = 2 days. `--only "MSC"` limits to one line; `--dry-run` prints
the remaining plan without spending quota.

## Selection rule (v2, 13 Jul 2026 — after the v1 postmortem)

The search is **relevance-ordered** and the top 3 **by view count** are
picked from the relevant survivors. v1 ordered the search itself by view
count and the candidate pool filled with viral Shorts and accident clips —
60 of 119 ships returned zero, and Symphony of the Seas' "review" was a
kids-channel room tour with 68M views. Filters: embeddable only, no Shorts,
no live streams, minimum 8 minutes, ship name in the title, and a blocklist
(BLOCK_WORDS) that removes disaster-bait ("accident", "terror", "storm"…)
and room-only tours. Ships with fewer than 3 passing videos are
flagged in the run log (`<-- only N passed filters, eyeball this one`) —
usually brand-new or tiny ships; hand-pick via the FEEDS-style one-line edit
in reviews.json if needed.

## Maintaining the fleet

`FLEET` at the top of the script is the master ship list — believed current
July 2026. Edit freely as ships launch/leave (MSC World Asia joins Dec 2026;
Rhapsody of the Seas has left Royal Caribbean). Re-running only harvests
ships missing from reviews.json, so adding one ship costs ~101 units. To
force a refresh of everything (e.g. annually, as view counts drift), delete
data/reviews.json and re-run over 2 days.

## Output schema

```json
{ "generated": "...", "minMinutes": 8, "lines": {
    "Royal Caribbean": {
      "Icon of the Seas": { "candidates": 9, "reviews": [
        { "videoId": "...", "title": "...", "channel": "...",
          "views": 4210331, "published": "2024-01-27", "minutes": 41 } ] } } } }
```

The app embeds each review as `https://www.youtube.com/embed/<videoId>`
inside the Ocean View modal player — in-domain viewing throughout, per the
v2 embed-first rule.
