#!/usr/bin/env python3
"""
Ocean View — Ship Reviews harvest (v1, 12 Jul 2026)

Finds the top 3 most-viewed, EMBEDDABLE YouTube ship tours/reviews for every
ship across the 12 leading cruise lines, and writes data/reviews.json for the
Ocean View app.

Usage:
    export YT_API_KEY="your-key-here"          # never commit this
    python3 harvest_reviews.py                 # harvest everything (resumable)
    python3 harvest_reviews.py --only "MSC"    # one line only
    python3 harvest_reviews.py --dry-run       # print the plan, no API calls

Quota: each ship costs ~101 units (1 search @100 + 1 videos.list @1).
The free daily quota is 10,000 units => ~99 ships/day. The script saves after
EVERY ship and exits cleanly when quota runs out — just run it again the next
day and it continues where it stopped. Full fleet (~178 ships) = 2 days.

Selection rule (per the 12 Jul design decision):
  - embeddable only (search pre-filter + verified per video)
  - no Shorts, no live streams
  - minimum duration MIN_MINUTES (default 8) to filter clickbait clips
  - ship name must appear in the video title (relevance guard)
  - top 3 by view count
"""

import json, os, re, sys, time, urllib.parse, urllib.request

API = "https://www.googleapis.com/youtube/v3"
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "reviews.json")
MIN_MINUTES = 8
SEARCH_POOL = 15          # candidates fetched per ship before filtering
SLEEP = 0.25              # politeness pause between API calls

# ---------------------------------------------------------------------------
# The fleet list — 12 leading lines, ~178 ships, believed current July 2026.
# EDIT FREELY: new ships launch, old ones leave. Full marketing names are used
# so searches disambiguate (Carnival Dream vs Disney Dream). Galapagos-only
# expedition trios etc. are deliberately excluded.
# ---------------------------------------------------------------------------
FLEET = {
  "Royal Caribbean": [
    "Icon of the Seas","Star of the Seas","Legend of the Seas","Utopia of the Seas",
    "Wonder of the Seas","Odyssey of the Seas","Spectrum of the Seas","Symphony of the Seas",
    "Harmony of the Seas","Ovation of the Seas","Anthem of the Seas","Quantum of the Seas",
    "Allure of the Seas","Oasis of the Seas","Independence of the Seas","Freedom of the Seas",
    "Liberty of the Seas","Adventure of the Seas","Voyager of the Seas","Navigator of the Seas",
    "Mariner of the Seas","Explorer of the Seas","Brilliance of the Seas","Radiance of the Seas",
    "Jewel of the Seas","Serenade of the Seas","Enchantment of the Seas","Grandeur of the Seas",
    "Vision of the Seas",
  ],
  "Carnival": [
    "Carnival Mardi Gras","Carnival Celebration","Carnival Jubilee","Carnival Firenze",
    "Carnival Venezia","Carnival Panorama","Carnival Horizon","Carnival Vista",
    "Carnival Breeze","Carnival Dream","Carnival Magic","Carnival Sunshine",
    "Carnival Sunrise","Carnival Radiance","Carnival Splendor","Carnival Glory",
    "Carnival Valor","Carnival Conquest","Carnival Freedom","Carnival Liberty",
    "Carnival Miracle","Carnival Pride","Carnival Legend","Carnival Spirit",
    "Carnival Luminosa","Carnival Elation","Carnival Paradise",
    "Carnival Adventure","Carnival Encounter",
  ],
  "MSC Cruises": [
    "MSC World America","MSC World Europa","MSC Euribia","MSC Seascape","MSC Seashore",
    "MSC Seaview","MSC Seaside","MSC Virtuosa","MSC Grandiosa","MSC Bellissima",
    "MSC Meraviglia","MSC Preziosa","MSC Divina","MSC Splendida","MSC Fantasia",
    "MSC Magnifica","MSC Poesia","MSC Orchestra","MSC Musica","MSC Opera",
    "MSC Lirica","MSC Sinfonia","MSC Armonia",
  ],
  "Norwegian": [
    "Norwegian Luna","Norwegian Aqua","Norwegian Viva","Norwegian Prima",
    "Norwegian Encore","Norwegian Bliss","Norwegian Joy","Norwegian Escape",
    "Norwegian Getaway","Norwegian Breakaway","Norwegian Epic","Norwegian Gem",
    "Norwegian Jade","Norwegian Pearl","Norwegian Jewel","Norwegian Dawn",
    "Norwegian Star","Norwegian Sun","Norwegian Sky","Norwegian Spirit",
  ],
  "Princess": [
    "Star Princess","Sun Princess","Enchanted Princess","Sky Princess","Discovery Princess",
    "Majestic Princess","Regal Princess","Royal Princess","Grand Princess","Ruby Princess",
    "Emerald Princess","Crown Princess","Caribbean Princess","Island Princess",
    "Coral Princess","Sapphire Princess","Diamond Princess",
  ],
  "Celebrity": [
    "Celebrity Xcel","Celebrity Ascent","Celebrity Beyond","Celebrity Apex","Celebrity Edge",
    "Celebrity Reflection","Celebrity Silhouette","Celebrity Eclipse","Celebrity Equinox",
    "Celebrity Solstice","Celebrity Summit","Celebrity Infinity","Celebrity Constellation",
    "Celebrity Millennium",
  ],
  "Holland America": [
    "Rotterdam","Nieuw Statendam","Koningsdam","Nieuw Amsterdam","Eurodam","Noordam",
    "Oosterdam","Westerdam","Zuiderdam","Zaandam","Volendam",
  ],
  "P&O Cruises": [
    "Arvia","Iona","Britannia","Azura","Ventura","Aurora","Arcadia",
  ],
  "Cunard": [
    "Queen Anne","Queen Mary 2","Queen Victoria","Queen Elizabeth",
  ],
  "Disney": [
    "Disney Wish","Disney Treasure","Disney Destiny","Disney Adventure",
    "Disney Fantasy","Disney Dream","Disney Magic","Disney Wonder",
  ],
  "Virgin Voyages": [
    "Scarlet Lady","Valiant Lady","Resilient Lady","Brilliant Lady",
  ],
  "Costa": [
    "Costa Smeralda","Costa Toscana","Costa Diadema","Costa Deliziosa","Costa Fascinosa",
    "Costa Favolosa","Costa Fortuna","Costa Pacifica","Costa Serena",
  ],
}

# Lines whose ships carry no brand prefix need it added to the SEARCH QUERY
# (not the title check) for disambiguation.
QUERY_PREFIX = {"Holland America": "Holland America", "P&O Cruises": "P&O",
                "Cunard": "Cunard", "Princess": ""}

# ---------------------------------------------------------------------------

def api_get(endpoint, params, key):
    params["key"] = key
    url = f"{API}/{endpoint}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r), None
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")
        if "quotaExceeded" in body or "dailyLimitExceeded" in body:
            return None, "QUOTA"
        return None, f"HTTP {e.code}: {body[:300]}"
    except Exception as e:
        return None, f"{type(e).__name__}: {e}"

def iso_minutes(iso):
    """PT1H2M3S -> minutes (int)."""
    m = re.fullmatch(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso or "")
    if not m:
        return 0
    h, mi, s = (int(x) if x else 0 for x in m.groups())
    return h * 60 + mi + (1 if s >= 30 else 0)

def title_matches(ship, title):
    t = title.lower()
    if ship.lower() in t:
        return True
    # allow all significant tokens present (handles punctuation variants)
    toks = [w for w in re.split(r"\W+", ship.lower()) if w and w not in ("of", "the")]
    return all(w in t for w in toks)

def harvest_ship(line, ship, key):
    prefix = QUERY_PREFIX.get(line)
    qname = f"{prefix} {ship}".strip() if prefix else ship
    q = f"{qname} cruise ship tour"
    search, err = api_get("search", {
        "part": "id", "q": q, "type": "video", "order": "viewCount",
        "videoEmbeddable": "true", "maxResults": SEARCH_POOL,
        "relevanceLanguage": "en", "safeSearch": "none",
    }, key)
    if err:
        return None, err
    ids = [i["id"]["videoId"] for i in search.get("items", []) if i.get("id", {}).get("videoId")]
    if not ids:
        return {"reviews": [], "candidates": 0}, None
    time.sleep(SLEEP)
    vids, err = api_get("videos", {
        "part": "snippet,contentDetails,statistics,status", "id": ",".join(ids),
    }, key)
    if err:
        return None, err
    passed = []
    for v in vids.get("items", []):
        sn, st = v.get("snippet", {}), v.get("status", {})
        dur = iso_minutes(v.get("contentDetails", {}).get("duration"))
        views = int(v.get("statistics", {}).get("viewCount", 0))
        title = sn.get("title", "")
        if not st.get("embeddable"):                 continue
        if sn.get("liveBroadcastContent") != "none": continue
        if dur < MIN_MINUTES:                        continue
        if "#short" in title.lower():                continue
        if not title_matches(ship, title):           continue
        passed.append({
            "videoId": v["id"], "title": title,
            "channel": sn.get("channelTitle", ""),
            "views": views, "published": sn.get("publishedAt", "")[:10],
            "minutes": dur,
        })
    passed.sort(key=lambda x: -x["views"])
    return {"reviews": passed[:3], "candidates": len(passed)}, None

def load_out():
    if os.path.exists(OUT):
        with open(OUT) as f:
            return json.load(f)
    return {"generated": "", "minMinutes": MIN_MINUTES, "lines": {}}

def save_out(data):
    data["generated"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    tmp = OUT + ".tmp"
    with open(tmp, "w") as f:
        json.dump(data, f, indent=1)
    os.replace(tmp, OUT)

def main():
    only = None
    dry = "--dry-run" in sys.argv
    if "--only" in sys.argv:
        only = sys.argv[sys.argv.index("--only") + 1].lower()

    key = os.environ.get("YT_API_KEY")
    if not key and not dry:
        sys.exit("ERROR: set YT_API_KEY first, e.g.  export YT_API_KEY=\"...\"")

    data = load_out()
    todo = []
    for line, ships in FLEET.items():
        if only and only not in line.lower():
            continue
        done = data["lines"].get(line, {})
        for ship in ships:
            if ship not in done:
                todo.append((line, ship))

    total = sum(len(s) for s in FLEET.values())
    print(f"Fleet: {total} ships across {len(FLEET)} lines. "
          f"Remaining this run: {len(todo)}. "
          f"(~{len(todo)*101} quota units needed; 10,000/day free.)")
    if dry:
        for line, ship in todo:
            print(f"  {line:16s} {ship}")
        return

    n = 0
    for line, ship in todo:
        result, err = harvest_ship(line, ship, key)
        if err == "QUOTA":
            save_out(data)
            print(f"\nDaily quota exhausted after {n} ships this run. "
                  f"Progress saved — run the script again tomorrow to continue.")
            return
        if err:
            print(f"  !! {ship}: {err} — skipping, will retry next run")
            time.sleep(SLEEP)
            continue
        data["lines"].setdefault(line, {})[ship] = result
        save_out(data)
        n += 1
        got = len(result["reviews"])
        flag = "" if got == 3 else f"  <-- only {got} passed filters, eyeball this one"
        top = result["reviews"][0]["views"] if got else 0
        print(f"  [{n}/{len(todo)}] {ship}: {got} reviews (top {top:,} views){flag}")
        time.sleep(SLEEP)

    print(f"\nDone. {n} ships harvested this run. Output: {os.path.abspath(OUT)}")

if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        pass
