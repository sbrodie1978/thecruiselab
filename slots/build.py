"""Build dist/index.html by inlining src/engine.js into src/app.html."""
import pathlib
root = pathlib.Path(__file__).parent
app = (root / "src/app.html").read_text()
engine = (root / "src/engine.js").read_text()
engine = engine.replace("if(typeof module!=='undefined') module.exports", "if(typeof module!=='undefined'&&module.exports) module.exports")
assert "/*ENGINE*/" in app
out = root / "dist"
out.mkdir(exist_ok=True)
(out / "index.html").write_text(app.replace("/*ENGINE*/", engine))
(out / "_headers").write_text("/*\n  X-Robots-Tag: noindex, nofollow\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n")
print("built", (out / "index.html").stat().st_size, "bytes")
