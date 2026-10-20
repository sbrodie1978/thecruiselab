// node capture.js <file.html> <duration_s> <outdir> [fps]
const puppeteer=require('puppeteer-core');
const path=require('path');const fs=require('fs');
const CHROME='/home/claude/.cache/puppeteer/chrome/linux-131.0.6778.204/chrome-linux64/chrome';

(async()=>{
  const [,,html,durS,outdir,fpsS]=process.argv;
  const dur=parseFloat(durS),fps=parseInt(fpsS||'30');
  fs.mkdirSync(outdir,{recursive:true});
  const browser=await puppeteer.launch({executablePath:CHROME,headless:true,
    args:['--no-sandbox','--disable-gpu','--disable-dev-shm-usage','--force-device-scale-factor=1',
          '--hide-scrollbars','--font-render-hinting=none','--disable-lcd-text']});
  const page=await browser.newPage();
  await page.setViewport({width:1080,height:1920,deviceScaleFactor:1});
  await page.goto('file://'+path.resolve(html),{waitUntil:'networkidle0'});
  await page.evaluate(()=>document.fonts.ready);
  await page.evaluate(()=>window.seek(0));
  const N=Math.round(dur*fps);
  const t0=Date.now();
  for(let f=0;f<N;f++){
    await page.evaluate(t=>window.seek(t),f/fps);
    await page.screenshot({path:path.join(outdir,`f${String(f).padStart(4,'0')}.jpg`),
      type:'jpeg',quality:94});
    if(f%120===0)console.log(`frame ${f}/${N} (${((Date.now()-t0)/1000).toFixed(0)}s)`);
  }
  await browser.close();
  console.log(`done: ${N} frames in ${((Date.now()-t0)/1000).toFixed(0)}s`);
})().catch(e=>{console.error(e);process.exit(1);});
