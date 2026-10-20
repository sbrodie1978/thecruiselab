/* The Cruise Lab — deterministic kinetic engine. Everything is a pure function of t (seconds). */
const clamp=(x,a,b)=>Math.max(a,Math.min(b,x));
const lerp=(a,b,p)=>a+(b-a)*p;
const ph=(t,t0,d)=>clamp((t-t0)/d,0,1);
const outCubic=p=>1-Math.pow(1-p,3);
const outQuint=p=>1-Math.pow(1-p,5);
const inCubic=p=>p*p*p;
const outBack=(p,k=1.9)=>{const c=k+1;return 1+c*Math.pow(p-1,3)+k*Math.pow(p-1,2);};
const outElastic=p=>p===0?0:p===1?1:Math.pow(2,-10*p)*Math.sin((p*10-0.75)*(2*Math.PI/3))+1;

/* ---------- impacts: shared camera shake + flashes ---------- */
const IMPACTS=[];
function impact(t,shake=1,flash=0,gold=0){IMPACTS.push({t,shake,flash,gold});}
function applyCamera(t,driftZoom=1.02){
  let sx=0,sy=0,rot=0,fl=0,gf=0;
  for(const im of IMPACTS){
    const dt=t-im.t;
    if(dt>=0&&dt<0.55){
      const d=Math.exp(-dt*11);
      sx+=im.shake*24*d*Math.sin(dt*96+im.t*7.3);
      sy+=im.shake*17*d*Math.sin(dt*79+im.t*12.1);
      rot+=im.shake*0.65*d*Math.sin(dt*63+im.t*3.7);
      if(im.flash) fl=Math.max(fl,im.flash*Math.exp(-dt*16));
      if(im.gold)  gf=Math.max(gf,im.gold *Math.exp(-dt*9));
    }
  }
  const z=1+(driftZoom-1)*(0.5+0.5*Math.sin(t*0.5)); // slow breathing
  document.getElementById('cam').style.transform=
    `translate(${sx}px,${sy}px) rotate(${rot}deg) scale(${z})`;
  document.getElementById('flash').style.opacity=fl.toFixed(3);
  document.getElementById('goldflash').style.opacity=gf.toFixed(3);
}

/* ---------- element movers ---------- */
function hide(el){el.style.opacity=0;}
function punch(el,t,t0,{d=0.4,from=3.0,rot=0,y=0,hold=Infinity,exit=0.25}={}){
  if(t<t0){hide(el);return false;}
  if(t>t0+hold+exit){hide(el);return false;}
  let s,o,r;
  if(t<=t0+hold){
    const p=ph(t,t0,d),e=outBack(p,1.7);
    s=lerp(from,1,e); o=clamp(p*3.5,0,1); r=lerp(rot,0,e);
  }else{
    const p=ph(t,t0+hold,exit);
    s=lerp(1,0.82,inCubic(p)); o=1-p*p; r=0;
  }
  el.style.opacity=o; el.style.transform=`translateY(${y}px) scale(${s.toFixed(4)}) rotate(${r}deg)`;
  return t>=t0;
}
function rise(el,t,t0,{d=0.5,from=90,hold=Infinity,exit=0.3}={}){
  if(t<t0||t>t0+hold+exit){hide(el);return false;}
  if(t<=t0+hold){
    const p=outQuint(ph(t,t0,d));
    el.style.opacity=clamp(p*2,0,1);
    el.style.transform=`translateY(${lerp(from,0,p)}px)`;
  }else{
    const p=ph(t,t0+hold,exit);
    el.style.opacity=1-p; el.style.transform=`translateY(${-40*inCubic(p)}px)`;
  }
  return true;
}
function stampIn(el,t,t0,{d=0.24,rot=-7,hold=Infinity}={}){
  if(t<t0||t>t0+hold){hide(el);return false;}
  const p=ph(t,t0,d),e=outCubic(p);
  const s=lerp(3.4,1,e);
  const jig=p>=1?Math.exp(-(t-t0-d)*8)*2.2*Math.sin((t-t0)*70):0;
  el.style.opacity=clamp(p*4,0,1);
  el.style.transform=`translate(-50%,-50%) scale(${s.toFixed(4)}) rotate(${rot+jig}deg)`;
  return true;
}
function counter(el,t,t0,d,from,to,fmt){
  const p=outCubic(ph(t,t0,d));
  el.textContent=fmt(lerp(from,to,p));
}
function setMeter(el,t,t0,d,pct){
  el.style.width=(outCubic(ph(t,t0,d))*pct).toFixed(2)+'%';
}
function shakeEl(el,t,amp,freq=9){ // continuous wobble (motion card)
  const dx=amp*Math.sin(t*freq), dy=amp*0.6*Math.sin(t*freq*0.7+1.3), r=amp*0.25*Math.sin(t*freq*0.5);
  el.style.transform=`translate(${dx}px,${dy}px) rotate(${r}deg)`;
}

/* ---------- word-by-word hook ---------- */
function words(el,text){
  el.innerHTML='';
  return text.split(' ').map(w=>{
    const s=document.createElement('span');s.className='hookword';s.textContent=w;
    el.appendChild(s);el.appendChild(document.createTextNode(' '));return s;
  });
}

/* ---------- flask mark ---------- */
function flaskSVG(size=280){
  return `<svg width="${size}" height="${size}" viewBox="0 0 200 200" fill="none">
  <defs>
    <linearGradient id="fg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#f0d087"/><stop offset="1" stop-color="#d9b45c"/>
    </linearGradient>
    <clipPath id="body"><path d="M84 34 h32 v44 l40 74 a14 14 0 0 1-12 21 H56 a14 14 0 0 1-12-21 l40-74 z"/></clipPath>
  </defs>
  <g clip-path="url(#body)">
    <rect x="30" y="112" width="140" height="70" fill="#0d2445"/>
    <path id="w1" d="M30 124 q17 -12 35 0 t35 0 t35 0 t35 0 v60 h-140 z" fill="#123059"/>
    <path id="w2" d="M30 132 q17 -10 35 0 t35 0 t35 0 t35 0 v60 h-140 z" fill="#46c3a8" opacity="0.55"/>
    <circle id="bub" cx="100" cy="150" r="7" fill="url(#fg)"/>
  </g>
  <path d="M84 34 h32 v44 l40 74 a14 14 0 0 1-12 21 H56 a14 14 0 0 1-12-21 l40-74 z"
        stroke="url(#fg)" stroke-width="7" stroke-linejoin="round"/>
  <path d="M76 26 h48" stroke="url(#fg)" stroke-width="7" stroke-linecap="round"/>
</svg>`;
}

/* ---------- shared end card ---------- */
function buildEndCard(toolName,cta){
  const ec=document.createElement('div');ec.id='endcard';
  ec.innerHTML=`
    ${cta?`<div id="eccta" style="font-family:Outfit;font-weight:600;font-size:52px;color:var(--foam);max-width:820px;text-align:center;line-height:1.25">${cta}</div>`:''}
    <div id="ecflask">${flaskSVG(290)}</div>
    <div class="wordmark goldgrad" id="ecword">THE CRUISE LAB</div>
    <div class="toolchip" id="ectool">${toolName}</div>
    <div class="free" id="ecfree">FREE · LINK IN BIO</div>
    <div class="url" id="ecurl">thecruiselab.com</div>`;
  document.getElementById('cam').appendChild(ec);
  return ec;
}
function endCard(t,t0){
  const ec=document.getElementById('endcard');
  if(t<t0){ec.style.opacity=0;return;}
  ec.style.opacity=clamp(ph(t,t0,0.25)*1.5,0,1);
  const cta=document.getElementById('eccta');
  if(cta) rise(cta,t,t0+0.05,{d:.4,from:60});
  punch(document.getElementById('ecflask'),t,t0,{d:.4,from:2.4});
  rise(document.getElementById('ecword'),t,t0+0.22,{d:.45,from:70});
  punch(document.getElementById('ectool'),t,t0+0.45,{d:.35,from:1.9});
  rise(document.getElementById('ecfree'),t,t0+0.65,{d:.4,from:50});
  rise(document.getElementById('ecurl'),t,t0+0.8,{d:.4,from:50});
  // bubble rises in the flask
  const bub=document.getElementById('bub');
  if(bub){const p=(t-t0)%1.8/1.8;bub.setAttribute('cy',(158-40*p).toFixed(1));bub.setAttribute('opacity',(1-p).toFixed(2));}
  const w2=document.getElementById('w2');
  if(w2){w2.setAttribute('transform',`translate(${(6*Math.sin(t*2)).toFixed(2)} 0)`);}
}
