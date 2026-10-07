/* ENGINE START */
const SYM = ['WILD','SCAT','LINER','FIZZ','COCK','ANCH','COMP','BUOY','A','K','Q','J'];
const PAYS = {
  WILD:[120,600,4000], LINER:[95,400,2000], FIZZ:[60,200,800], COCK:[50,160,480],
  ANCH:[30,95,310], COMP:[24,64,200], BUOY:[20,48,160],
  A:[14,35,120], K:[12,32,96], Q:[10,28,80], J:[8,24,64]
};
const WEIGHTS = [
  {WILD:0,SCAT:2,LINER:2,FIZZ:3,COCK:3,ANCH:4,COMP:4,BUOY:5,A:6,K:6,Q:7,J:8},
  {WILD:2,SCAT:2,LINER:2,FIZZ:3,COCK:3,ANCH:4,COMP:4,BUOY:5,A:6,K:6,Q:7,J:8},
  {WILD:2,SCAT:2,LINER:2,FIZZ:3,COCK:3,ANCH:4,COMP:4,BUOY:5,A:6,K:6,Q:7,J:8},
  {WILD:2,SCAT:2,LINER:2,FIZZ:3,COCK:3,ANCH:4,COMP:4,BUOY:5,A:6,K:6,Q:7,J:8},
  {WILD:2,SCAT:2,LINER:2,FIZZ:3,COCK:3,ANCH:4,COMP:4,BUOY:5,A:6,K:6,Q:7,J:8}
];
const LINES = [
  [1,1,1,1,1],[0,0,0,0,0],[2,2,2,2,2],[0,1,2,1,0],[2,1,0,1,2],
  [0,0,1,2,2],[2,2,1,0,0],[1,0,0,0,1],[1,2,2,2,1],[1,0,1,2,1],
  [1,2,1,0,1],[0,1,1,1,0],[2,1,1,1,2],[0,1,0,1,0],[2,1,2,1,2],
  [1,1,0,1,1],[1,1,2,1,1],[0,0,2,0,0],[2,2,0,2,2],[0,2,0,2,0]
];
function seeded(seed){ let s=seed>>>0; return ()=>{ s=(s*1664525+1013904223)>>>0; return s/4294967296; }; }
function buildStrips(){
  const strips=[];
  for(let r=0;r<5;r++){
    const rnd=seeded(7919*(r+1));
    let bag=[];
    for(const k in WEIGHTS[r]) for(let i=0;i<WEIGHTS[r][k];i++) bag.push(k);
    for(let i=bag.length-1;i>0;i--){ const j=Math.floor(rnd()*(i+1)); [bag[i],bag[j]]=[bag[j],bag[i]]; }
    // spread scatters and wilds: no two specials within 3 positions
    for(let pass=0;pass<200;pass++){
      let bad=-1;
      for(let i=0;i<bag.length;i++){
        if(bag[i]!=='SCAT') continue;
        for(let d=1;d<3;d++){ if(bag[(i+d)%bag.length]==='SCAT'){bad=(i+d)%bag.length;break;} }
        if(bad>=0) break;
      }
      if(bad<0) break;
      const j=Math.floor(rnd()*bag.length); [bag[bad],bag[j]]=[bag[j],bag[bad]];
    }
    strips.push(bag);
  }
  return strips;
}
const STRIPS = buildStrips();
function spinStops(rng){ return STRIPS.map(s=>Math.floor(rng()*s.length)); }
function gridFromStops(stops){
  // grid[reel][row]
  return stops.map((st,r)=>{ const s=STRIPS[r]; return [s[st%s.length],s[(st+1)%s.length],s[(st+2)%s.length]]; });
}
function evaluate(grid, lineBet){
  const wins=[]; let total=0;
  LINES.forEach((ln,li)=>{
    const syms=ln.map((row,r)=>grid[r][row]);
    if(syms[0]==='SCAT') return;
    // count leading wilds
    let lead=0; while(lead<5 && syms[lead]==='WILD') lead++;
    let base = lead<5 ? syms[lead] : 'WILD';
    if(base==='SCAT') base='WILD';
    let n=0; for(let i=0;i<5;i++){ if(syms[i]===base||syms[i]==='WILD') n++; else break; }
    let bestSym=base, bestN=n, bestPay = (n>=3 && PAYS[base]) ? PAYS[base][n-3] : 0;
    // pure wild run might pay more
    if(lead>=3 && PAYS.WILD[lead-3]>bestPay){ bestSym='WILD'; bestN=lead; bestPay=PAYS.WILD[lead-3]; }
    if(bestPay>0){
      const amt=bestPay*lineBet; total+=amt;
      wins.push({line:li,sym:bestSym,count:bestN,amount:amt,cells:ln.slice(0,bestN).map((row,r)=>[r,row])});
    }
  });
  let scat=0; const scatCells=[];
  grid.forEach((col,r)=>col.forEach((s,row)=>{ if(s==='SCAT'){scat++; scatCells.push([r,row]);} }));
  return {wins,total,scat,scatCells};
}
const SCAT_MULT = {3:1,4:2,5:5};
const BONUS_LIST = ['bartab','cabin','weather','excursion'];
const BARTAB = { values:[1,1,1,1,2,2,2,2,3], happyHour:2, topShelf:1, lastOrders:3, endAt:2, pkg:16 };
const CABIN = { prizes:[1,1,1,1,1,1,2,2,2,3,3], upgrades:4, bad:6, strikes:3, extraPerKey:5,
  grades:[{name:'Inside',mult:1},{name:'Oceanview',mult:2},{name:'Balcony',mult:3},{name:'Suite',mult:4}] };
const WEATHER = { ports:6, table:[['sun',3,0.20],['cloud',2,0.30],['rain',1,0.30],['rainbow',5,0.05],['storm',0,0.15]] };
const TRAIL = { values:[5,10,16,25,40,60,100,175], risk:[0.10,0.15,0.20,0.25,0.30,0.35,0.45], tuk:0.15 };
// Fixed jackpots. Value is a multiple of the total bet, odds are per paid spin and the same at every bet.
const JACKPOTS = [
  {key:'suite',name:'Suite',x:20,odds:500},
  {key:'balcony',name:'Balcony',x:8,odds:200},
  {key:'oceanview',name:'Oceanview',x:4,odds:100},
  {key:'inside',name:'Inside',x:2,odds:50}
];
const BETS = [20,40,100,200,400,1000];
function shuffle(a,rng){ a=a.slice(); for(let i=a.length-1;i>0;i--){const j=Math.floor(rng()*(i+1));[a[i],a[j]]=[a[j],a[i]];} return a; }
function pickWeather(rng){ let x=rng(),acc=0; for(const w of WEATHER.table){ acc+=w[2]; if(x<acc) return w; } return WEATHER.table[0]; }
// One draw per paid spin. Returns the jackpot won, or null. Rarest is checked first.
function rollJackpot(rng){ let x=rng(), acc=0; for(const j of JACKPOTS){ acc+=1/j.odds; if(x<acc) return j; } return null; }
if(typeof module!=='undefined') module.exports={SYM,PAYS,LINES,STRIPS,spinStops,gridFromStops,evaluate,SCAT_MULT,BONUS_LIST,BARTAB,CABIN,WEATHER,TRAIL,JACKPOTS,BETS,shuffle,pickWeather,rollJackpot};
/* ENGINE END */
