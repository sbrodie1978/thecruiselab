#!/usr/bin/env python3
"""
build_sailings.py — Shore Thing sailing data compiler.

Reads the hand-authored itinerary-templates.json and expands each template's
date list into individual dated 'sailing' records, written to sailings.json.

The output shape deliberately mirrors what a licensed Widgety cruise feed
provides (operator + ship + sail date + duration + ordered port visits), so
the app's data-source adapter can later swap the generated file for a live API
with no change to the app itself.

Usage:  python3 build_sailings.py
Run from the shorething/ directory (or anywhere; paths are relative to this file).
"""

import json, os, sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")

def load(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as f:
        return json.load(f)

def main():
    templates_doc = load("itinerary-templates.json")
    ports = {p["id"]: p for p in load("ports.json")}
    fleet = load("fleet.json")

    # Build lookup of valid ship ids per line for validation
    ships_by_line = {}
    line_names = {}
    for line in fleet["lines"]:
        line_names[line["id"]] = line["name"]
        ships_by_line[line["id"]] = {s["id"]: s["name"] for s in line["ships"]}

    sailings = []
    errors = []

    for t in templates_doc["templates"]:
        line, ship = t["line"], t["ship"]
        # Validate line/ship exist in fleet
        if line not in ships_by_line:
            errors.append(f"{t['id']}: unknown line '{line}'")
            continue
        if ship not in ships_by_line[line]:
            errors.append(f"{t['id']}: unknown ship '{ship}' for line '{line}'")
            continue
        # Validate every portId exists
        for d in t["days"]:
            if d.get("type") == "sea":
                continue
            if d["portId"] not in ports:
                errors.append(f"{t['id']} day {d['day']}: unknown portId '{d['portId']}'")

        # Expand each embarkation date into a discrete sailing
        for embark in t["dates"]:
            sailing_id = f"{t['id']}__{embark}"
            sailings.append({
                "id": sailing_id,
                "line": line,
                "lineName": line_names[line],
                "ship": ship,
                "shipName": ships_by_line[line][ship],
                "name": t["name"],
                "nights": t["nights"],
                "embarkDate": embark,
                "days": t["days"],          # ordered port/sea sequence
                "templateId": t["id"],
                "widgetyId": t.get("widgetyId")
            })

    if errors:
        print("VALIDATION ERRORS — nothing written:", file=sys.stderr)
        for e in errors:
            print("  -", e, file=sys.stderr)
        sys.exit(1)

    # Sort by line, ship, date for stable output
    sailings.sort(key=lambda s: (s["line"], s["ship"], s["embarkDate"]))

    out = {
        "_generated": f"built by build_sailings.py from itinerary-templates.json",
        "_comment": "GENERATED FILE — do not edit by hand. Edit itinerary-templates.json and re-run build_sailings.py. Shape mirrors a Widgety cruise feed for a clean future swap.",
        "count": len(sailings),
        "sailings": sailings
    }
    with open(os.path.join(DATA, "sailings.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)

    # Report
    by_line = {}
    for s in sailings:
        by_line.setdefault(s["lineName"], set()).add(s["ship"])
    print(f"Wrote {len(sailings)} sailings from {len(templates_doc['templates'])} templates.")
    for ln, ships in sorted(by_line.items()):
        n = sum(1 for s in sailings if s["lineName"] == ln)
        print(f"  {ln}: {n} sailings across {len(ships)} ship(s)")

if __name__ == "__main__":
    main()
