// Return to player simulation. Run: node tools/rtp-sim.js
// Mirrors the rules in src/engine.js and the bonus screens in src/app.html.
const E=require('../src/engine.js');
const rng=Math.random;
const N=+(process.argv[2]||2e6);
let line=0, trig=0, multSum=0, hits=0;
for(let i=0;i<N;i++){ const ev=E.evaluate(E.gridFromStops(E.spinStops(rng)),1); line+=ev.total; if(ev.total>0)hits++; if(ev.scat>=3){trig++; multSum+=E.SCAT_MULT[Math.min(ev.scat,5)];} }
const lineRTP=line/(N*20);
function bar(){const T=E.BARTAB;const cards=E.shuffle([...T.values.map(v=>['d',v]),...Array(T.happyHour).fill(['h']),...Array(T.topShelf).fill(['t']),...Array(T.lastOrders).fill(['l'])],rng);let tab=0,m=1,lo=0;for(const c of cards){if(c[0]==='l'){if(++lo>=T.endAt)break;}else if(c[0]==='h')m++;else if(c[0]==='t')tab*=2;else tab+=c[1]*m;}return tab>=T.pkg?tab*2:tab;}
function cabin(){const T=E.CABIN;const cards=E.shuffle([...T.prizes.map(v=>['p',v]),...Array(T.upgrades).fill(['u']),...Array(T.bad).fill(['b'])],rng);let s=0,t=0,u=0,x=0;for(const c of cards){if(c[0]==='b'){if(++s>=T.strikes)break;}else if(c[0]==='u'){u++;if(u>=T.grades.length)x+=T.extraPerKey;}else t+=c[1];}return t*T.grades[Math.min(u,T.grades.length-1)].mult+x;}
function weather(){const sticky=new Set();let tot=0;for(let p=0;p<E.WEATHER.ports;p++){const w=E.pickWeather(rng);if(w[1]===0)continue;const g=E.gridFromStops(E.spinStops(rng));sticky.forEach(k=>{const[r,row]=k.split(',');g[+r][+row]='WILD';});g.forEach((c,r)=>c.forEach((s,row)=>{if(s==='WILD')sticky.add(r+','+row);}));tot+=E.evaluate(g,1).total/20*w[1];}return tot;}
function trail(stop){const T=E.TRAIL;let k=0;while(k<stop-1){if(rng()<T.risk[k])return 0;k++;if(k<stop-1&&rng()<T.tuk)k++;}return T.values[Math.min(k,T.values.length-1)];}
const M=200000, avg=f=>{let s=0;for(let i=0;i<M;i++)s+=f();return s/M;};
const ev={bartab:avg(bar),cabin:avg(cabin),weather:avg(weather),excursion:avg(()=>trail(5))};
const bonusAvg=(ev.bartab+ev.cabin+ev.weather+ev.excursion)/4;
const bonusRTP=bonusAvg*(multSum/trig)*trig/N;
const jpRTP=E.JACKPOTS.reduce((s,j)=>s+j.x/j.odds,0);
console.log('Line wins RTP', lineRTP.toFixed(4), ' hit rate', (hits/N).toFixed(3));
console.log('Bonus 1 in', (N/trig).toFixed(1), 'spins, avg scatter multiplier', (multSum/trig).toFixed(3));
console.log('Bonus averages (x total bet, excursion assumes cashing out at step 5):', Object.fromEntries(Object.entries(ev).map(([k,v])=>[k,+v.toFixed(2)])));
console.log('Bonus RTP', bonusRTP.toFixed(4), ' Jackpot RTP', jpRTP.toFixed(4));
console.log('TOTAL', (lineRTP+bonusRTP+jpRTP).toFixed(4));
