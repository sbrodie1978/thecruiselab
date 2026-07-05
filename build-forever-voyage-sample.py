#!/usr/bin/env python3
"""
build-forever-voyage-sample.py  (v4 — YuNet DNN detector + media/download lockdown)
------------------------------------------------------------------
Builds an anonymised, deployable clone of the live "norwaywithmum"
site for use as the PUBLIC Forever Voyage sample.

v3 replaces the Haar detector with OpenCV's YuNet DNN face detector,
which is far better at turned, close-up and edge-of-frame faces
(i.e. selfies). It downloads the YuNet model automatically on first
run and caches it in ~/.cache/forevervoyage/.

What it does:
  1. Downloads the live index.html from norwaywithmum.pages.dev
  2. Finds and downloads every image + any CSS/JS/font it references
  3. Blurs (pixelates) every detected face — native pass + horizontally
     flipped pass + an upscaled pass for small/distant faces
  4. Anonymises names in the HTML (Frances/Stuart -> Mum/Son, etc.)
  5. Disables the family photo/video downloads and the video clips
  6. Writes a self-contained ./forever-voyage-sample/ folder

Requirements:
  - Python 3.8+
  - opencv-python 4.x   ->   pip3 install --user "opencv-python<5"
  Everything else is standard library.

Run:
  python3 build-forever-voyage-sample.py

Re-runnable: it re-downloads and re-blurs from the live site each time,
so running it again is safe.

IMPORTANT: still eyeball the output before deploying. The script prints
any photo where it found NO face. It's your family, so this review is
the step that matters.
------------------------------------------------------------------
"""

import os, re, sys, ssl, urllib.request, urllib.error

# ----------------------------------------------------------------------
# Config
# ----------------------------------------------------------------------
ORIGIN = "https://norwaywithmum.pages.dev"
OUT    = "forever-voyage-sample"
UA     = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) ForeverVoyageBuilder/4.0"

# YuNet model (OpenCV Zoo, stored via Git-LFS -> use the media host).
MODEL_URLS = [
    "https://media.githubusercontent.com/media/opencv/opencv_zoo/main/"
    "models/face_detection_yunet/face_detection_yunet_2023mar.onnx",
]
MODEL_DIR  = os.path.expanduser("~/.cache/forevervoyage")
MODEL_PATH = os.path.join(MODEL_DIR, "face_detection_yunet_2023mar.onnx")

# Lower score threshold = catch more faces (a few background false-positives
# are harmless on a sample; a missed real face is not).
SCORE_THRESHOLD = 0.55
NMS_THRESHOLD   = 0.3
TOP_K           = 5000

ASSET_EXT = r"(?:jpg|jpeg|png|webp|gif|svg|css|js|ico|woff2?|ttf)"
IMG_EXT   = (".jpg", ".jpeg", ".png", ".webp")

NAME_SUBS = [
    ("Frances &amp; Stuart", "Mum &amp; Son"),
    ("Frances & Stuart",     "Mum & Son"),
    ("Stuart and Frances",   "a mother and son"),
    ("Frances and Stuart",   "a mother and son"),
    ("F &amp; S",            "M &amp; S"),
    ("F & S",                "M & S"),
    ("Frances",              "Mum"),
    ("Stuart",               "Son"),
]

# ----------------------------------------------------------------------
# Sample lockdown: make videos non-viewable and downloads non-functional
# ----------------------------------------------------------------------
LOCKDOWN_CSS = """<style id="fv-sample-lockdown">
/* Forever Voyage sample — viewing videos and downloads are disabled */
.video-wrap video{display:none!important}
.video-wrap .video-play-btn{display:none!important}
.video-wrap{pointer-events:none}
.lightbox-download{display:none!important}
.download-btn{pointer-events:none!important;opacity:.4;cursor:default!important}
</style>
"""

DL_INTRO_OLD = ("All the photos and videos from the journal, ready to download \u2014 "
                "for prints, framing, or just to keep. Tap any individual photo in the journal to grab it on its own.")
DL_INTRO_NEW = ("Every Forever Voyage comes with all the photos and videos bundled up for the "
                "whole family to download and keep. Downloads are disabled on this sample.")
DL_NOTE_OLD  = "All files are personal photos and videos \u00b7 for family use only \u00b7 please don't share publicly"
DL_NOTE_NEW  = "Downloadable photo &amp; video bundles are part of your own Forever Voyage \u00b7 disabled on this sample"

def disable_media(html):
    if "</head>" in html and "fv-sample-lockdown" not in html:
        html = html.replace("</head>", LOCKDOWN_CSS + "</head>", 1)
    html = html.replace(DL_INTRO_OLD, DL_INTRO_NEW)
    html = html.replace(DL_NOTE_OLD, DL_NOTE_NEW)
    return html

# ----------------------------------------------------------------------
# HTTP
# ----------------------------------------------------------------------
_ctx = ssl.create_default_context()

def fetch(url, binary=False):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, context=_ctx, timeout=120) as r:
        data = r.read()
    return data if binary else data.decode("utf-8", "replace")

# ----------------------------------------------------------------------
# YuNet detector
# ----------------------------------------------------------------------
def ensure_model():
    if os.path.exists(MODEL_PATH) and os.path.getsize(MODEL_PATH) > 100_000:
        return
    os.makedirs(MODEL_DIR, exist_ok=True)
    last_err = None
    for url in MODEL_URLS:
        try:
            print("Downloading YuNet model (first run only)...")
            data = fetch(url, binary=True)
            if len(data) < 100_000:
                last_err = "got %d bytes (looks like an LFS pointer, not the model)" % len(data)
                continue
            with open(MODEL_PATH, "wb") as f:
                f.write(data)
            print("  model saved to %s (%d KB)" % (MODEL_PATH, len(data) // 1024))
            return
        except Exception as e:
            last_err = str(e)
    sys.exit(
        "ERROR: could not download the YuNet model.\n"
        "  Last error: %s\n\n"
        "  Download it manually, then re-run this script:\n"
        "    mkdir -p %s\n"
        "    curl -L -o %s \\\n      %s\n"
        % (last_err, MODEL_DIR, MODEL_PATH, MODEL_URLS[0]))

def load_detector():
    try:
        import cv2
    except ImportError:
        sys.exit('ERROR: opencv-python is not installed.\n'
                 '  Run:  pip3 install --user "opencv-python<5"')
    if not hasattr(cv2, "FaceDetectorYN"):
        sys.exit('ERROR: your OpenCV (%s) has no FaceDetectorYN.\n'
                 '  Install the 4.x line:  pip3 install --user "opencv-python<5"'
                 % cv2.__version__)
    ensure_model()
    try:
        det = cv2.FaceDetectorYN.create(
            MODEL_PATH, "", (320, 320), SCORE_THRESHOLD, NMS_THRESHOLD, TOP_K)
    except cv2.error as e:
        try: os.remove(MODEL_PATH)
        except OSError: pass
        sys.exit("ERROR: the YuNet model failed to load (removed the cached copy so a\n"
                 "re-run will re-download it). Details: %s" % e)
    return cv2, det

def _detect(cv2, det, img):
    h, w = img.shape[:2]
    det.setInputSize((w, h))
    _, faces = det.detect(img)
    boxes = []
    if faces is not None:
        for f in faces:
            x, y, fw, fh = (int(round(v)) for v in f[:4])
            boxes.append((x, y, fw, fh))
    return boxes

def blur_faces(cv2, det, path):
    """Pixelate every detected face in-place. Returns face count (None if unreadable)."""
    img = cv2.imread(path)
    if img is None:
        return None
    H, W = img.shape[:2]

    boxes = list(_detect(cv2, det, img))

    # horizontally flipped pass (extra insurance on asymmetric/turned faces)
    flip = cv2.flip(img, 1)
    for (x, y, w, h) in _detect(cv2, det, flip):
        boxes.append((W - x - w, y, w, h))

    # upscaled pass to catch small / distant faces
    if max(H, W) < 2200:
        big = cv2.resize(img, (W * 3 // 2, H * 3 // 2), interpolation=cv2.INTER_LINEAR)
        for (x, y, w, h) in _detect(cv2, det, big):
            boxes.append((int(x * 2 / 3), int(y * 2 / 3), int(w * 2 / 3), int(h * 2 / 3)))

    for (x, y, w, h) in boxes:
        pad = int(w * 0.22)
        x0, y0 = max(0, x - pad), max(0, y - pad)
        x1, y1 = min(W, x + w + pad), min(H, y + h + pad)
        roi = img[y0:y1, x0:x1]
        if roi.size == 0:
            continue
        rh, rw = roi.shape[:2]
        small = cv2.resize(roi, (12, 12), interpolation=cv2.INTER_LINEAR)
        img[y0:y1, x0:x1] = cv2.resize(small, (rw, rh), interpolation=cv2.INTER_NEAREST)

    cv2.imwrite(path, img)
    return len(boxes)

# ----------------------------------------------------------------------
# HTML transform
# ----------------------------------------------------------------------
def transform_html(html):
    for a, b in NAME_SUBS:
        html = html.replace(a, b)
    html = re.sub(
        r'href="(?:' + re.escape(ORIGIN) + r')?/?downloads/[^"]*"',
        'href="#" data-sample="downloads disabled in sample" onclick="return false"',
        html)
    html = re.sub(
        r'(href|src)="(?:' + re.escape(ORIGIN) + r')?/?[^"]*\.mp4"',
        r'\1="#" data-sample="video omitted from sample"',
        html)
    html = re.sub(r'(["\(])' + re.escape(ORIGIN) + r'/', r'\1/', html)
    html = re.sub(r'(<meta name="description" content=")[^"]*(")',
                  r'\1A sample Forever Voyage travel journal — Norway, eight days.\2', html)
    html = disable_media(html)
    return html

def collect_assets(html):
    paths = set()
    for m in re.finditer(re.escape(ORIGIN) + r'/([^\s"\')]+?\.' + ASSET_EXT + r')', html):
        paths.add("/" + m.group(1))
    for m in re.finditer(
            r'(?:src|href)="(/?(?:images|videos/posters|css|js|assets|fonts)/[^"]+?\.' + ASSET_EXT + r')"',
            html):
        p = m.group(1)
        paths.add(p if p.startswith("/") else "/" + p)
    return {p for p in paths if not p.endswith(".mp4")}

# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------
def main():
    print("Forever Voyage — sample builder (v4, YuNet + lockdown)\n" + "-" * 40)
    cv2, det = load_detector()
    print("OpenCV %s — YuNet detector ready (score >= %.2f)." % (cv2.__version__, SCORE_THRESHOLD))

    print("Fetching", ORIGIN, "...")
    try:
        html = fetch(ORIGIN + "/")
    except urllib.error.URLError as e:
        sys.exit("ERROR: could not fetch the live site: %s" % e)

    assets = sorted(collect_assets(html))
    print("Found %d assets to mirror." % len(assets))
    os.makedirs(OUT, exist_ok=True)

    downloaded, images, failed, no_faces = 0, 0, [], []
    for rel in assets:
        url  = ORIGIN + rel
        dest = os.path.join(OUT, rel.lstrip("/"))
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        try:
            data = fetch(url, binary=True)
        except Exception as e:
            failed.append((rel, str(e)))
            continue
        with open(dest, "wb") as f:
            f.write(data)
        downloaded += 1
        if dest.lower().endswith(IMG_EXT):
            n = blur_faces(cv2, det, dest)
            images += 1
            if n == 0:
                no_faces.append(rel)
        sys.stdout.write("\r  downloaded %d/%d" % (downloaded, len(assets)))
        sys.stdout.flush()
    print()

    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write(transform_html(html))

    print("-" * 40)
    print("Done.  Output folder: ./%s/" % OUT)
    print("  HTML:   index.html  (names anonymised, downloads + videos disabled)")
    print("  Images: %d downloaded and face-blurred" % images)
    if failed:
        print("  WARNING: %d assets failed to download:" % len(failed))
        for rel, err in failed:
            print("    -", rel, "->", err)
    if no_faces:
        print("\n  REVIEW THESE — no face was detected (may be scenery, or a missed face):")
        for rel in no_faces:
            print("    -", rel)
        print("  Open each and check. If any shows an identifiable face, blur or crop")
        print("  it by hand before deploying.")

    print("\nNext steps:")
    print("  1. Open ./%s/index.html in a browser and review it end to end." % OUT)
    print("  2. Deploy it (production branch for this project is 'main'):")
    print("       cd %s && npx wrangler pages deploy . --project-name=forever-voyage-sample --branch=main --commit-dirty=true" % OUT)

if __name__ == "__main__":
    main()
