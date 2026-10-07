"""Build dist/ from src/ and static/.

- Inlines src/engine.js into src/app.html and writes dist/index.html.
- Writes dist/_headers (noindex while the game is unlaunched).
- Copies everything in static/ into dist/ (estate icon kit + manifest).
"""
import pathlib, shutil
root = pathlib.Path(__file__).parent
app = (root / "src/app.html").read_text()
engine = (root / "src/engine.js").read_text()
engine = engine.replace("if(typeof module!=='undefined') module.exports", "if(typeof module!=='undefined'&&module.exports) module.exports")
assert "/*ENGINE*/" in app
out = root / "dist"
out.mkdir(exist_ok=True)
(out / "index.html").write_text(app.replace("/*ENGINE*/", engine))
(out / "_headers").write_text("/*\n  X-Robots-Tag: noindex, nofollow\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n")
static = root / "static"
if static.is_dir():
    shutil.copytree(static, out, dirs_exist_ok=True)
need = ["icons/apple-touch-icon.png", "favicon.ico", "manifest.webmanifest"]
missing = [n for n in need if not (out / n).exists()]
if missing:
    print("WARNING: icon kit incomplete in dist/, missing:", ", ".join(missing))
    print("Copy icons/ and favicon.ico from ~/cruiselab/hub into static/ and rebuild.")
files = [p for p in out.rglob("*") if p.is_file()]
print("built", (out / "index.html").stat().st_size, "bytes,", len(files), "files in dist/")
