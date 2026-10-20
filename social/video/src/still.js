// node still.js <html> <outprefix> t1 t2 ...
const puppeteer=require('puppeteer-core');const path=require('path');
const CHROME='/home/claude/.cache/puppeteer/chrome/linux-131.0.6778.204/chrome-linux64/chrome';
(async()=>{
  const [,,html,pre,...ts]=process.argv;
  const b=await puppeteer.launch({executablePath:CHROME,headless:true,args:['--no-sandbox','--disable-gpu','--force-device-scale-factor=1','--font-render-hinting=none']});
  const p=await b.newPage();await p.setViewport({width:1080,height:1920});
  await p.goto('file://'+path.resolve(html),{waitUntil:'networkidle0'});
  await p.evaluate(()=>document.fonts.ready);
  p.on('pageerror',e=>console.log('PAGEERR',e.message));
  for(const t of ts){await p.evaluate(t=>window.seek(t),parseFloat(t));
    await p.screenshot({path:`${pre}_${t}.png`});}
  await b.close();console.log('stills ok');
})().catch(e=>{console.error(e.message);process.exit(1);});
