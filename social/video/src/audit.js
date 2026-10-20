// node src/audit.js src/l1.html 21.0
// Samples the timeline and reports pairs of visible text elements whose boxes overlap.
const puppeteer = require('puppeteer-core');
const path = require('path');

const CHROME = '/home/claude/.cache/puppeteer/chrome/linux-131.0.6778.204/chrome-linux64/chrome';
const [,, htmlFile, durStr] = process.argv;
const dur = parseFloat(durStr);

(async () => {
  const browser = await puppeteer.launch({
    executablePath: CHROME, headless: 'new',
    args: ['--no-sandbox', '--force-device-scale-factor=1']
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1080, height: 1920 });
  await page.goto('file://' + path.resolve(htmlFile));
  await page.evaluate(() => document.fonts.ready);

  const clashes = {};
  for (let t = 0; t <= dur; t += 0.25) {
    const found = await page.evaluate((t) => {
      window.seek(t);
      // collect leaf-ish text elements that are actually visible
      const els = [...document.querySelectorAll('body *')].filter(el => {
        if (!el.innerText || !el.innerText.trim()) return false;
        // only elements whose own direct text is non-empty OR small containers
        const ownText = [...el.childNodes].filter(n => n.nodeType === 3)
          .map(n => n.textContent.trim()).join('');
        if (!ownText) return false;
        const st = getComputedStyle(el);
        if (st.display === 'none' || st.visibility === 'hidden') return false;
        // effective opacity up the chain
        let o = 1, p = el;
        while (p && p !== document.body) { o *= parseFloat(getComputedStyle(p).opacity); p = p.parentElement; }
        if (o < 0.12) return false;
        const r = el.getBoundingClientRect();
        if (r.width < 4 || r.height < 4) return false;
        if (r.bottom < 0 || r.top > 1920 || r.right < 0 || r.left > 1080) return false;
        return true;
      }).map(el => ({
        text: el.innerText.trim().slice(0, 40).replace(/\n/g, ' / '),
        rect: (() => { const r = el.getBoundingClientRect();
          return { l: r.left, t: r.top, r: r.right, b: r.bottom }; })(),
        path: (() => { let p = el, s = []; while (p && p !== document.body) {
          s.unshift(p.id ? '#' + p.id : p.className ? '.' + String(p.className).split(' ')[0] : p.tagName);
          p = p.parentElement; } return s.join('>'); })()
      }));
      // pairwise overlap between elements not in ancestor relation (different top-level groups)
      const out = [];
      for (let i = 0; i < els.length; i++) for (let j = i + 1; j < els.length; j++) {
        const a = els[i], b = els[j];
        if (a.path.startsWith(b.path + '>') || b.path.startsWith(a.path + '>')) continue;
        const topA = a.path.split('>')[0], topB = b.path.split('>')[0];
        const ox = Math.min(a.rect.r, b.rect.r) - Math.max(a.rect.l, b.rect.l);
        const oy = Math.min(a.rect.b, b.rect.b) - Math.max(a.rect.t, b.rect.t);
        if (ox > 8 && oy > 8) out.push({ a: a.text, b: b.text, ta: topA, tb: topB, ox: ox | 0, oy: oy | 0 });
      }
      return out;
    }, t);
    for (const c of found) {
      const key = `${c.ta} × ${c.tb} :: "${c.a}" × "${c.b}"`;
      if (!clashes[key]) clashes[key] = { first: t, last: t, ox: c.ox, oy: c.oy };
      else clashes[key].last = t;
    }
  }
  const keys = Object.keys(clashes);
  if (!keys.length) { console.log('CLEAN — no cross-group text overlaps'); }
  else for (const k of keys) {
    const c = clashes[k];
    console.log(`CLASH t=${c.first.toFixed(2)}–${c.last.toFixed(2)}  ovl ${c.ox}x${c.oy}px  ${k}`);
  }
  await browser.close();
})();
