# The Cruise Lab — Launch Video Batch v1 (15 July 2026)

The four launch videos (L1–L4) from `launch-scripts-v1-20260715.md`, fully rendered
with soundtracks baked in. 1080×1920 (9:16 vertical), 30fps, H.264 yuv420p + AAC 192k.
Ready to post natively to TikTok / Instagram Reels / YouTube Shorts / Facebook.

## The videos

| File | Video | Length | Tool / destination |
|---|---|---|---|
| `cruiselab-L1-worst-oceanview-v5-20260715.mp4` | The worst oceanview on Sun Princess — cabin 6202, 55.8/100, #186 of 186 | 21s | Good Cabin Bad Cabin |
| `cruiselab-L2-leave-at-home-v2-20260715.mp4` | 5 things security takes at the gangway (candles → kettle → iron → drone → surge protector) | 24s | All Aboard Store |
| `cruiselab-L3-bar-tab-v2-20260715.mp4` | The £41 question — real Princess bar tab, £579 total, £41.32/day break-even | 29s | GetMyBarTab |
| `cruiselab-L4-le-havre-wind-v2-20260715.mp4` | The Paris day nobody packs for — Le Havre 31 Oct, wind 74%, 4-of-5-years gusts | 25s | GetMyCruiseWeather |

Every on-screen number was taken from the locked figures in `launch-scripts-v1` (which
were confirmed live in the tools). Accuracy guardrails observed: L1 uses the /100 scale
and frames the theatre as a location fact (not "noisy"); L3 never shows a package price
(the tool is line-blind) and names Princess Plus honestly; L4 says "last 5 years" and
leads with wind, not rain.

Audio: synthesised music beds + beat-timed SFX (stamp thunks, receipt ticks, buzzers,
wind gusts, risers) — **no copyrighted or licensed music anywhere**, so the tracks are
safe on every platform including the TikTok Business account (which is restricted to
commercial-library audio). Sound-off-first still holds: every beat is captioned and the
videos work fully muted.

## How they're built (rebuild any video from source)

Pipeline: animated HTML/CSS timeline → headless-Chrome frame capture → ffmpeg encode
→ Python-synthesised soundtrack → mux. Everything is a pure function of time `t`
(each HTML file exposes `window.seek(t)`), so renders are deterministic.

```
src/
  style.css        shared brand tokens, stage, kinetic classes, end card
  helpers.js       easing, punch/stamp/counter/meter helpers, camera shake,
                   flask SVG, buildEndCard()
  l1.html … l4.html  the four video timelines
  capture.js       node capture.js <html> <duration> <framesdir> [fps]
  still.js         node still.js <html> <prefix> <t1> <t2> …   (QA stills)
  audio_synth.py   python3 audio_synth.py <l1|l2|l3|l4> <dur> <out.wav>
```

Requirements: node 22 + `puppeteer-core` (npm install with
`PUPPETEER_SKIP_DOWNLOAD=1`, point it at a local Chrome), ffmpeg, Python 3 with
numpy + scipy. Fonts (Cinzel, Outfit, JetBrains Mono, Saira Stencil One) are fetched
as TTFs from the google/fonts GitHub repo into `fonts/` — capture waits on
`document.fonts.ready`.

Full rebuild of one video (L4 shown):

```bash
node src/capture.js src/l4.html 25.0 frames/l4 30
ffmpeg -y -framerate 30 -i frames/l4/f%04d.jpg -c:v libx264 -preset medium \
  -crf 18 -pix_fmt yuv420p out/l4_silent.mp4
python3 src/audio_synth.py l4 25.0 out/l4.wav
ffmpeg -y -i out/l4_silent.mp4 -i out/l4.wav -c:v copy -c:a aac -b:a 192k \
  -shortest out/cruiselab-L4-le-havre-wind-v2-20260715.mp4
```

Copy tweaks: edit the HTML, re-run the three commands. Timing tweaks: keep the
`impact()` times in the HTML and the hit times in `audio_synth.py` in sync — the
SFX are placed at the same timestamps as the visual hits.

## Posting notes (from the campaign doc)

- Post natively on each platform; pin nothing (the intro promo stays pinned).
- Captions per platform are in `cruiselab-launch-campaign-v1-20260714.md`.
- Growth videos (L1/L3/L4) end on the end card only; L2's CTA is the soft
  "full list — free, link in bio".
- Destination for all: links.thecruiselab.com (add `?src=` tags when the
  Phase-0 UTM pass is done).

## v2 batch revision (same day)

A full-timeline collision audit (`src/audit.js` — samples every 0.25s, measures
every visible text element's rendered bounding box, flags overlaps and frame
overflow) caught wording clashing with wording in all four videos. Fixed:

- **Hooks (all four):** several hook lines were sized for one line but wrapped,
  stacking into the lines below (worst: 215px of text-on-text). All hook lines
  resized to render single-line, respaced, and given explicit line-heights
  (Cinzel's default line box is very tall). Hooks now also fully exit before
  the next beat lands instead of coexisting with it.
- **L1:** the CHARGE 02 badge was being re-anchored by the shake wrapper's
  transform and pulled down into the "Motion score" label — moved outside the
  wrapper. Big counter numbers cleared from their labels. BAD CABIN stamp now
  lands below the score (OUT OF 100 fades as it slams), sub-line moved clear,
  and the stamp resized to fit inside the frame.
- **L2:** CONFISCATED stamp raised to slam across the icon only, clear of item
  names; verdict lines respaced.
- **L3:** hook respaced; "YOUR REAL BAR TAB." now two intentional lines.
- **L4:** sun moved above the hook text; wind-card counter cleared from its
  label and tag; year chips' entrance softened; "IT'S A WINDBREAKER." resized
  to fit the frame; verdict rows respaced.

Re-run the audit after any copy change:
`node src/audit.js src/l1.html 21.0` (etc.) — persistent overlaps are bugs;
single-sample flags during an entrance (stamps sweeping in) are the motion.

### v3 batch revision
"DEAD LAST." was printing over the ranking number: "#186 of 186" at 300px
wrapped mid-number, and the audit's ancestor check had a string-prefix bug
(#ranksub matched #rank) that hid the pair. Audit fixed (delimiter-aware),
rank restyled as two intentional rows (#186 giant / OF 186), sub moved clear.
L1 → v5; other videos unchanged.
