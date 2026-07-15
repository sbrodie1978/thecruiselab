#!/usr/bin/env python3
"""
author_itinerary.py — turn a pasted itinerary into a validated template block.

Speeds up hand-authoring itinerary-templates.json. You paste a simple day-by-day
itinerary (referenced from a cruise line's OWN published schedule) and this:
  - fuzzy-matches each port line against the real ports.json ids
  - marks sea days automatically
  - flags anything it can't match confidently, so you fix ids not hunt them
  - emits a ready-to-paste template JSON block

It does NOT fetch, scrape, or download anything. Input is text you provide.

USAGE
  python3 author_itinerary.py --line princess --ship sky-princess \
      --name "7-Night Western Caribbean" --dates 2026-01-04,2026-01-18 < itin.txt

  ...where itin.txt (or stdin) is one line per day, e.g.:
      1 Fort Lauderdale
      2 At sea
      3 Grand Cayman
      4 Roatan
      5 Belize
      6 Costa Maya
      7 Sea day
      8 Fort Lauderdale
  Day numbers are optional; if absent, lines are numbered in order.
  Lines matching sea/at sea/cruising/day at sea -> sea day.

Review the output, then paste the block into itinerary-templates.json's
"templates" array and run build_sailings.py.
"""
import sys, json, os, re, argparse, difflib

HERE = os.path.dirname(os.path.abspath(__file__))
PORTS = json.load(open(os.path.join(HERE, "data", "ports.json"), encoding="utf-8"))

# Build searchable name index: normalised name/alias -> id
def norm(s):
    s = s.lower()
    s = re.sub(r"\(.*?\)", " ", s)          # drop parenthetical
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    return re.sub(r"\s+", " ", s).strip()

NAME_TO_ID = {}
ID_TO_NAME = {}
PORT_SEARCH = []  # (id, name, set_of_all_tokens_incl_parenthetical)
for p in PORTS:
    ID_TO_NAME[p["id"]] = p["name"]
    NAME_TO_ID[norm(p["name"])] = p["id"]
    lead = norm(p["name"].split(",")[0])
    NAME_TO_ID.setdefault(lead, p["id"])
    # full token set INCLUDING words inside parentheses (norm() strips those)
    raw_tokens = set(re.sub(r"[^a-z0-9 ]", " ", p["name"].lower()).split())
    PORT_SEARCH.append((p["id"], p["name"], raw_tokens))

SEA_RE = re.compile(r"\b(at sea|sea day|day at sea|cruising|scenic cruising)\b", re.I)

def match_port(raw):
    """Return (portId, confidence, note). confidence: exact|fuzzy|none."""
    n = norm(raw)
    if not n:
        return None, "none", "empty"
    if n in NAME_TO_ID:
        return NAME_TO_ID[n], "exact", ""
    in_tokens = set(n.split())
    # 1) input appears as a whole phrase inside a full port name (or vice versa)
    candidates = []
    for p in PORTS:
        pn = norm(p["name"])
        if n in pn or pn in n:
            candidates.append((p["id"], p["name"], pn))
    if len(candidates) == 1:
        pid, pname, _ = candidates[0]
        return pid, "exact", ""
    if len(candidates) > 1:
        # pick the shortest name (usually the canonical/least-qualified) but warn
        pid, pname, _ = min(candidates, key=lambda c: len(c[2]))
        others = ", ".join(c[1] for c in candidates if c[0] != pid)
        return pid, "fuzzy", f"'{raw.strip()}' -> {pname}  (also possible: {others})"
    # 2) all input tokens present in a port name's token set (incl. parenthetical)
    tok_hits = []
    for pid, pname, ptoks in PORT_SEARCH:
        if in_tokens and in_tokens.issubset(ptoks):
            tok_hits.append((pid, pname))
    if len(tok_hits) == 1:
        return tok_hits[0][0], "fuzzy", f"'{raw.strip()}' -> {tok_hits[0][1]}"
    if len(tok_hits) > 1:
        pid, pname = tok_hits[0]
        others = ", ".join(c[1] for c in tok_hits[1:])
        return pid, "fuzzy", f"'{raw.strip()}' -> {pname}  (also possible: {others})"
    # 3) fuzzy against all indexed keys
    hit = difflib.get_close_matches(n, NAME_TO_ID.keys(), n=1, cutoff=0.72)
    if hit:
        pid = NAME_TO_ID[hit[0]]
        return pid, "fuzzy", f"'{raw.strip()}' -> {ID_TO_NAME[pid]}"
    return None, "none", f"NO MATCH for '{raw.strip()}'"

def parse(lines):
    days = []
    warnings = []
    order = 0
    for ln in lines:
        ln = ln.rstrip()
        if not ln.strip():
            continue
        order += 1
        # optional leading day number
        m = re.match(r"\s*(\d+)[\.\)\:\-\s]+(.*)$", ln)
        if m:
            day = int(m.group(1)); rest = m.group(2)
        else:
            day = order; rest = ln
        if SEA_RE.search(rest) or not norm(rest):
            days.append({"day": day, "type": "sea"})
            continue
        pid, conf, note = match_port(rest)
        if conf == "none":
            days.append({"day": day, "portId": f"__UNMATCHED__{rest.strip()}"})
            warnings.append(f"  day {day}: {note} — fix the portId manually")
        else:
            days.append({"day": day, "portId": pid})
            if conf == "fuzzy":
                warnings.append(f"  day {day}: {note}  (verify)")
    return days, warnings

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--line", required=True)
    ap.add_argument("--ship", required=True)
    ap.add_argument("--name", required=True)
    ap.add_argument("--nights", type=int, default=None, help="defaults to (#days - 1)")
    ap.add_argument("--dates", default="", help="comma-separated ISO embark dates")
    ap.add_argument("--id", default=None, help="template id; auto-derived if omitted")
    args = ap.parse_args()

    days, warnings = parse(sys.stdin.readlines())
    if not days:
        print("No itinerary lines read on stdin.", file=sys.stderr); sys.exit(1)

    nights = args.nights if args.nights is not None else max(d["day"] for d in days) - 1
    tid = args.id or f"{args.ship}-{nights}n-" + re.sub(r"[^a-z0-9]+","-",args.name.lower()).strip("-")
    dates = [d.strip() for d in args.dates.split(",") if d.strip()]

    block = {
        "id": tid, "line": args.line, "ship": args.ship,
        "name": args.name, "nights": nights, "widgetyId": None,
        "days": days, "dates": dates
    }

    print("\n// ---- paste into itinerary-templates.json \"templates\" array ----")
    print(json.dumps(block, indent=6, ensure_ascii=False))
    if warnings:
        print("\n// REVIEW BEFORE USING:", file=sys.stderr)
        for w in warnings: print(w, file=sys.stderr)
        if any("NO MATCH" in w for w in warnings):
            print("\n// >>> Fix every __UNMATCHED__ portId before running build_sailings.py.", file=sys.stderr)
    else:
        print("\n// All ports matched exactly. Add dates if empty, then run build_sailings.py.", file=sys.stderr)

if __name__ == "__main__":
    main()
