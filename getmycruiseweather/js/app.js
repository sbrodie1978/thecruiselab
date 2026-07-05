
(function(){
  
// Ports are loaded from /data/ports.json (pre-shipped coordinates only)
let PORTS = [];

async function loadPorts(){
  try{
    const res = await fetch("./data/ports.json", { cache: "no-cache" });
    if(!res.ok) throw new Error("HTTP " + res.status);
    const list = await res.json();
    if(!Array.isArray(list)) throw new Error("Invalid ports.json");

    const canonicalPortName = (name) => {
      if(!name) return "";
      let n = String(name);

      // remove parenthetical descriptors like "(Paris)" and collapse whitespace
      n = n.replace(/\s*\([^)]*\)\s*/g, " ").replace(/\s+/g, " ").trim();

      // normalize accents/diacritics
      if(n.normalize){
        n = n.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
      // strip country/region suffix after comma (e.g., "Oslo, Norway")
      n = n.split(",")[0].trim(); // keep Port only

      }

      // common alias fixes (keep UI as Port only)
            // also strip dash suffix (e.g., "Oslo - Norway")
      n = n.split(" - ")[0].trim();

      const alias = {
        "valetta": "Valletta",
        "cagliari": "Cagliari",
        "kusadasi": "Kusadasi",
        "seville": "Seville",
      };
      const key = n.toLowerCase().replace(/[^a-z0-9\s]/g, "").replace(/\s+/g, " ").trim();
      if(alias[key]) return alias[key];

      // tidy punctuation variants
      n = n.replace(/[^\w\s-]/g, " ").replace(/\s+/g, " ").trim();
      return n;
    };


    PORTS = [];
    const seen = new Set();
    for (const p of list){
      if(!p || typeof p.name !== "string" || typeof p.lat !== "number" || typeof p.lon !== "number") continue;
      const canon = canonicalPortName(p.name);
      const key = canon.toLowerCase().replace(/[^a-z0-9\s]/g,"").replace(/\s+/g," ").trim();
      if(seen.has(key)) continue;
      seen.add(key);
      PORTS.push({
        id: String(p.id || canon).toLowerCase().replace(/[^a-z0-9]+/g,"-").replace(/(^-|-$)/g,""),
        name: canon,
        lat: p.lat,
        lon: p.lon, region: p.region || "Europe"
      });
    }
    PORTS.sort((a,b)=>a.name.localeCompare(b.name, undefined, { sensitivity:"base" }));
return PORTS;
  }catch(e){
    console.warn("Ports load failed:", e);
    PORTS = [];
    return PORTS;
  }
}

function handlePortsUnavailable(){
  const portSelect = document.getElementById("portSelect");
  if(portSelect){
    portSelect.innerHTML = '<option value="">Ports unavailable (reload)</option>';
    portSelect.disabled = true;
  }
}
function buildViatorUrl(portName){
  // Viator affiliate tracking (hard-coded from your Partner account)
  const base = "https://www.viator.com/searchResults/all";
  const qs = new URLSearchParams();
  qs.set("text", portName || "Cruise port");
  qs.set("pid", "P00290711");
  qs.set("mcid", "42383");
  qs.set("medium", "link");
  return `${base}?${qs.toString()}`;
}
function updateViatorLink(portName){
  const name = portName || "this port";
  const a = document.getElementById("viatorLink");
  if(a){
    a.href = buildViatorUrl(name);
  }
  const vp = document.getElementById("viatorPortName");
  if(vp){ vp.textContent = name; }
  const vc = document.getElementById("viatorPortCta");
  if(vc){ vc.textContent = name; }
}
function $(id){ return document.getElementById(id); }
  function clamp(n,a,b){ return Math.max(a, Math.min(b,n)); }
  function fmt2(n){ return String(n).padStart(2,"0"); }

  // ------------------ Units (C / F) ------------------
  const UNIT_KEY = "gmcw:unit";
  function getUnit(){ const u = localStorage.getItem(UNIT_KEY); return (u === "F") ? "F" : "C"; }
  function setUnit(u){ localStorage.setItem(UNIT_KEY, u === "F" ? "F" : "C"); }
  function cToF(c){ return (c * 9/5) + 32; }
  function fmtTemp(c){ const u=getUnit(); const v=(u==="F")?cToF(c):c; return `${Math.round(v)}°${u}`; }
  function fmtRange(lowC, highC){ const u=getUnit(); const lo=(u==="F")?cToF(lowC):lowC; const hi=(u==="F")?cToF(highC):highC; return `${Math.round(lo)}°${u}–${Math.round(hi)}°${u}`; }

  // ------------------ Storage helpers ------------------
  function getJSON(key){ try{ return JSON.parse(localStorage.getItem(key)||"null"); }catch(e){ return null; } }
  function setJSON(key,val){ try{ localStorage.setItem(key, JSON.stringify(val)); }catch(e){} }

  // ------------------ Open‑Meteo Archive (no key) ------------------
  const ARCHIVE_ENDPOINT = "https://archive-api.open-meteo.com/v1/archive";

  function monthDayFromISO(isoDate){ const d=new Date(isoDate+"T12:00:00"); return {month:d.getMonth()+1, day:d.getDate()}; }
  function yearsToFetch(count){ const y=new Date().getFullYear(); return Array.from({length:count},(_,i)=>(y-1)-i); }
  function histCacheKey(portId, isoDate){ const md=monthDayFromISO(isoDate); return `gmcw:hist:${portId}:${fmt2(md.month)}-${fmt2(md.day)}`; }

  async function fetchOneDay(lat, lon, isoDate, year){
    const md = monthDayFromISO(isoDate);

    // Handle Feb 29 on non-leap years
    const isLeap = (year % 4 === 0 && year % 100 !== 0) || (year % 400 === 0);
    let month = md.month;
    let day = md.day;
    if(month === 2 && day === 29 && !isLeap) day = 28;

    const date = `${year}-${fmt2(month)}-${fmt2(day)}`;

    const baseParams =
      `latitude=${encodeURIComponent(lat)}` +
      `&longitude=${encodeURIComponent(lon)}` +
      `&start_date=${date}&end_date=${date}` +
      `&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,windspeed_10m_max`;

    const urls = [
      `${ARCHIVE_ENDPOINT}?${baseParams}&timezone=auto`,
      `${ARCHIVE_ENDPOINT}?${baseParams}&timezone=UTC`
    ];

    let lastErr = null;
    for(const url of urls){
      try{
        const res = await fetch(url);
        if(!res.ok) throw new Error(`Archive error (${res.status})`);
        const data = await res.json();
        const d = data && data.daily;
        if(!d || !d.time || !d.time.length) throw new Error("No daily data");
        const high = d.temperature_2m_max?.[0];
        const low  = d.temperature_2m_min?.[0];
        const rain = d.precipitation_sum?.[0];
        const wind = d.windspeed_10m_max?.[0];
        if([high,low,rain,wind].some(v => typeof v !== "number" || isNaN(v))) throw new Error("Invalid numeric data");
        return {year, high, low, rain, wind};
      } catch(e){ lastErr = e; }
    }
    throw lastErr || new Error("Archive fetch failed");
  }

  async function fetchHistory(port, isoDate){
    const key = histCacheKey(port.id, isoDate);
    const cached = getJSON(key);
    if(cached && cached.rows && cached.rows.length >= 3) return cached.rows;

    const tryCounts = [5, 10];
    let best = [];
    for(const count of tryCounts){
      const years = yearsToFetch(count);
      const rows = [];
      for(const y of years){
        try{ rows.push(await fetchOneDay(port.lat, port.lon, isoDate, y)); }
        catch(e){ /* skip */ }
      }
      if(rows.length > best.length) best = rows;
      if(rows.length >= 3){ setJSON(key, {rows}); return rows; }
    }
    throw new Error("Not enough historical data");
  }

  // ------------------ Scoring (0–100) ------------------
  function warmthScore(high, low){
    const avg = (high + low) / 2;
    const range = high - low;
    const avgScore = 100 - Math.abs(24 - avg) * 6;
    const rangePenalty = Math.max(0, (range - 9) * 2.2);
    return clamp(Math.round(avgScore - rangePenalty), 0, 100);
  }
  function rainRiskScore(rainMm){ const risk = 5 + (rainMm / 14) * 95; return clamp(Math.round(risk), 0, 100); }
  function windExposureScore(windKmh){ const expo = 5 + (windKmh / 38) * 95; return clamp(Math.round(expo), 0, 100); }

  function hintWarmth(score){ if(score>=75) return "Often warm"; if(score>=55) return "Mild"; if(score>=40) return "Often cool"; return "Often cold"; }
  function hintRain(risk){ if(risk<=20) return "Low rain risk"; if(risk<=40) return "Some rain risk"; if(risk<=60) return "Moderate rain risk"; return "Higher rain risk"; }
  function hintWind(expo){ if(expo<=25) return "Often calm"; if(expo<=45) return "Often breezy"; if(expo<=65) return "Often windy"; return "Frequently windy"; }

  // ------------------ UI helpers ------------------
  function setBar(el, value){ if(el) el.style.width = clamp(value,0,100) + "%"; }
  function populatePorts(selectEl){
    const regionSelect = document.getElementById("regionSelect");
    const portField = document.getElementById("portField");
    const region = regionSelect ? regionSelect.value : "";
    if(!selectEl) return;

    // Show/hide the port dropdown until region selected
    if(portField){
      portField.style.display = region ? "" : "none";
    }

    selectEl.innerHTML = "";
    const ph = document.createElement("option");
    ph.value = "";
    ph.textContent = "Select a port";
    selectEl.appendChild(ph);

    const list = region ? PORTS.filter(p => (p.region || "") === region) : [];
    const sorted = [...list].sort((a,b)=>a.name.localeCompare(b.name, undefined, { sensitivity:"base" }));

    for(const p of sorted){
      const opt = document.createElement("option");
      opt.value = p.id;
      opt.textContent = p.name;
      selectEl.appendChild(opt);
    }

    // Disable until region selected
    selectEl.disabled = !region;
  }function getSelectedPort(id){ const found=PORTS.find(p=>p.id===id); if(found) return found; const sorted=[...PORTS].sort((a,b)=>a.name.localeCompare(b.name,"en",{sensitivity:"base"})); return sorted[0]; }
  function readQuery(){ const qs=new URLSearchParams(window.location.search); return {region:qs.get("region"), port:qs.get("port"), date:qs.get("date")}; }
  function writeQuery(region, port, date){ const qs=new URLSearchParams(); if(region) qs.set("region", region); qs.set("port", port); qs.set("date", date); return "results.html?" + qs.toString(); }

  // ------------------ Packing recommendations ------------------
  
  function packingRecommendations(payload){
    // Return: { summary: string, items: string[] } (top 5)
    const high = Number(payload?.expected?.high ?? 0);          // °C
    const low  = Number(payload?.expected?.low  ?? 0);          // °C
    const rainRisk = Number(payload?.scores?.rainRisk ?? 0);    // 0-100
    const windExpo = Number(payload?.scores?.windExpo ?? 0);    // 0-100
    const windKmh  = Number(payload?.expected?.windKmh ?? 0);   // km/h (if available)
    const range = (isFinite(high) && isFinite(low)) ? (high - low) : 0;

    const candidates = [];
    const add = (text, weight) => candidates.push({text, weight: Number(weight)||0});

    // Bands (°C)
    const veryHot = high >= 30;
    const hot     = high >= 26 && high < 30;
    const warm    = high >= 20 && high < 26;
    const mild    = high >= 15 && high < 20;
    const cool    = high >= 10 && high < 15;
    const cold    = high < 10;

    // --- Temperature driven ---
    if(veryHot){
      add("Light, breathable clothing (linen/technical fabrics).", 95);
      add("Sun protection: sunscreen + sunglasses.", 90);
      add("A brimmed sun hat for shade ashore.", 85);
      add("Refillable water bottle (stay hydrated).", 65);
      add("Breathable footwear for hot pavements.", 55);
    } else if(hot){
      add("Breathable daytime outfits + a light layer for A/C.", 85);
      add("Sun protection: sunscreen + sunglasses.", 80);
      add("Hat/cap for daytime shore time.", 60);
      add("Comfortable walking shoes for excursions.", 55);
    } else if(warm){
      add("Light layers you can adjust through the day.", 70);
      add("Comfortable walking shoes for excursions.", 60);
      add("A light layer for breezier deck moments.", 50);
    } else if(mild){
      add("A light jacket or cardigan for the day.", 75);
      add("Layering pieces (tee + jumper) for flexibility.", 60);
      add("Closed‑toe shoes for cooler streets.", 45);
    } else if(cool){
      add("A warmer mid‑layer (jumper/fleece) for daytime.", 85);
      add("A windproof outer layer for deck time.", 70);
      add("Closed‑toe shoes + warm socks.", 55);
    } else if(cold){
      add("Warm coat + insulating layers (thermals if needed).", 95);
      add("Windproof outer layer (ports feel colder by the water).", 85);
      add("Gloves + scarf for cold deck time.", 70);
    }

    // --- Evenings & swings ---
    if(low <= 12 && high >= 18) add("Evenings can feel cooler: pack a light jumper/cardigan.", 65);
    if(low <= 8 && high >= 15) add("Cool evenings: a warmer layer for deck time.", 75);
    if(range >= 10 && high >= 18) add("Big temperature swing: dress in layers you can add/remove.", 55);

    // --- Rain ---
    if(rainRisk >= 70){
      add("High rain risk: a lightweight waterproof jacket.", 95);
      add("Quick‑dry clothing + spare socks.", 70);
      add("Water‑resistant day bag (or rain cover) for valuables.", 55);
    } else if(rainRisk >= 40){
      add("Chance of showers: packable rain jacket or compact umbrella.", 70);
      add("Quick‑dry layer (handy after a shower).", 45);
    }

    // --- Wind ---
    const windy  = (windExpo >= 65) || (windKmh >= 28);
    const breezy = (windExpo >= 45) || (windKmh >= 18);
    if(windy){
      add("Windy: a proper windbreaker (hooded if possible).", 85);
      if(high <= 20) add("Wind chill: add an extra warm layer for deck time.", 70);
      if(high <= 20 && (low <= 8 || (low <= 10 && windy))) add("Optional: beanie/hat if you feel the cold on deck.", 20);
    } else if(breezy){
      add("Breezy at sea: a light windproof layer.", 55);
    }

    // --- Footwear ---
    if(rainRisk >= 50) add("Grippy footwear (wet port pavements can be slippery).", 50);
    if(high >= 24 && rainRisk < 40) add("Breathable footwear for warm excursions.", 35);

    // --- Humid / tropical proxy ---
    if(high >= 28 && rainRisk >= 40){
      add("Humid heat: moisture‑wicking tops help you stay comfortable.", 55);
      add("Insect repellent for evening/outdoor excursions.", 35);
    }

    // Deduplicate and pick top 5
    const best = new Map();
    for(const c of candidates){
      const k = c.text.trim().toLowerCase();
      if(!best.has(k) || best.get(k).weight < c.weight) best.set(k, c);
    }
    const items = Array.from(best.values()).sort((a,b)=>b.weight-a.weight).slice(0,5).map(x=>x.text);

    // Summary
    let summaryParts = [];
    if(veryHot) summaryParts.push("Very hot day");
    else if(hot) summaryParts.push("Hot day");
    else if(warm) summaryParts.push("Warm day");
    else if(mild) summaryParts.push("Mild day");
    else if(cool) summaryParts.push("Cool day");
    else summaryParts.push("Cold day");

    if(rainRisk >= 70) summaryParts.push("high chance of rain");
    else if(rainRisk >= 40) summaryParts.push("showers possible");
    else summaryParts.push("low rain risk");

    if(windy) summaryParts.push("windy");
    else if(breezy) summaryParts.push("breezy");

    const summary = summaryParts.join(" • ") + ".";
    return { summary, items };
  }
// ------------------ Analysis ------------------
  async function analyse(portId, isoDate){
    const port = getSelectedPort(portId);
    const rows = await fetchHistory(port, isoDate);

    const avgHigh = rows.reduce((s,r)=>s+r.high,0) / rows.length;
    const avgLow  = rows.reduce((s,r)=>s+r.low,0) / rows.length;
    const avgRain = rows.reduce((s,r)=>s+r.rain,0) / rows.length;
    const avgWind = rows.reduce((s,r)=>s+r.wind,0) / rows.length;

    const warmth = warmthScore(avgHigh, avgLow);
    const rainRisk = rainRiskScore(avgRain);
    const windExpo = windExposureScore(avgWind);

    return {
      portId: port.id,
      portName: port.name,
      date: isoDate,
      expected: { high: Math.round(avgHigh), low: Math.round(avgLow), rainMm: Number(avgRain.toFixed(1)), windKmh: Math.round(avgWind) },
      scores: { warmth, rainRisk, windExpo },
      labels: { warmth: hintWarmth(warmth), rain: hintRain(rainRisk), wind: hintWind(windExpo) },
      history: rows.map(r => ({ year: r.year, high: Math.round(r.high), low: Math.round(r.low), rain: Number(r.rain.toFixed(1)), wind: Math.round(r.wind) }))
    };
  }

  function persist(payload){ localStorage.setItem("gmcw:last", JSON.stringify(payload)); }
  function restore(){ try{ return JSON.parse(localStorage.getItem("gmcw:last") || "null"); }catch(e){ return null; } }

  let CURRENT_PAYLOAD = null;

  function renderResults(payload){
    if(!payload) return;
    CURRENT_PAYLOAD = payload;

    updateViatorLink(payload.portName);

    $("warmthPct").textContent = payload.scores.warmth;
    $("rainPct").textContent   = payload.scores.rainRisk;
    $("windPct").textContent   = payload.scores.windExpo;

    $("warmthHint").textContent = payload.labels.warmth;
    $("rainHint").textContent   = payload.labels.rain;
    $("windHint").textContent   = payload.labels.wind;

    setBar($("warmthBar"), payload.scores.warmth);
    setBar($("rainBar"),   payload.scores.rainRisk);
    setBar($("windBar"),   payload.scores.windExpo);

    const pack = packingRecommendations(payload);
    const sumEl = $("packSummary");
    const listEl = $("packList");
    if(sumEl) sumEl.textContent = pack.summary;
    if(listEl){
      listEl.innerHTML = "";
      pack.items.forEach(t => {
        const li=document.createElement("li");
        li.innerHTML = `<span class="reco__dot" aria-hidden="true"></span><div class="reco__text">${t}</div>`;
        listEl.appendChild(li);
      });
    }

    const tbody = $("historyBody");
    if(tbody){
      tbody.innerHTML = "";
      payload.history.forEach(r => {
        const tr=document.createElement("tr");
        tr.innerHTML = `
          <td data-label="Year">${r.year}</td>
          <td data-label="High">${fmtTemp(r.high)}</td>
          <td data-label="Low">${fmtTemp(r.low)}</td>
          <td data-label="Rain">${r.rain.toFixed(1)} mm</td>
          <td data-label="Wind">${r.wind} km/h</td>
        `;
        tbody.appendChild(tr);
      });
    }
  }

  function wireUnitToggle(){
    // New premium segmented control
    const btnC = $("unitC");
    const btnF = $("unitF");

    function sync(){
      const u = getUnit();
      if(btnC) btnC.setAttribute("aria-pressed", u==="C" ? "true" : "false");
      if(btnF) btnF.setAttribute("aria-pressed", u==="F" ? "true" : "false");
    }

    if(btnC && btnF){
      btnC.addEventListener("click", () => {
        setUnit("C");
        sync();
        if(CURRENT_PAYLOAD) renderResults(CURRENT_PAYLOAD);
      });
      btnF.addEventListener("click", () => {
        setUnit("F");
        sync();
        if(CURRENT_PAYLOAD) renderResults(CURRENT_PAYLOAD);
      });
      sync();
      return;
    }

    // Legacy switch fallback (if present)
    const btn = $("unitToggleBtn");
    if(!btn) return;
    btn.setAttribute("aria-pressed", getUnit()==="F" ? "true" : "false");
    btn.addEventListener("click", () => {
      const next = (getUnit()==="C") ? "F" : "C";
      setUnit(next);
      btn.setAttribute("aria-pressed", next==="F" ? "true" : "false");
      if(CURRENT_PAYLOAD) renderResults(CURRENT_PAYLOAD);
    });
  }

  async function wireForm(){
    const regionSelect = $("regionSelect");
    const portSelect = $("portSelect");
    const dateInput  = $("dateInput");
    const btn        = $("analyseBtn");
    if(!regionSelect || !portSelect || !dateInput || !btn) return;

    await loadPorts();
    if(!PORTS || PORTS.length===0){ handlePortsUnavailable(); return; }

    const savedRegion = sessionStorage.getItem("gmcw_region") || "";
    if(savedRegion) regionSelect.value = savedRegion;
    regionSelect.addEventListener("change", ()=>{ sessionStorage.setItem("gmcw_region", regionSelect.value || ""); portSelect.value=""; populatePorts(portSelect); });

    populatePorts(portSelect);

    const savedPort = localStorage.getItem("gmcw:selectedPort");
    if(savedPort) portSelect.value = savedPort;
    portSelect.addEventListener("change", () => localStorage.setItem("gmcw:selectedPort", portSelect.value));

    function updateBtn(){ btn.disabled = !(regionSelect.value && portSelect.value && dateInput.value); }
    dateInput.addEventListener("input", updateBtn);
    updateBtn();

    btn.addEventListener("click", () => {
      if(!dateInput.value) return;
      window.location.href = writeQuery(regionSelect.value, portSelect.value, dateInput.value);
    });
  }

  async function initResultsPage(){
  await loadPorts();
  if(!PORTS || PORTS.length===0) handlePortsUnavailable();
    const q = readQuery();
    const regionSelect = $("regionSelect");
    const portSelect = $("portSelect");
    const dateInput  = $("dateInput");
    const btn        = $("analyseBtn");
    if(!regionSelect || !portSelect || !dateInput || !btn) return;

    // Restore region first (query param wins)
    const savedRegion = sessionStorage.getItem("gmcw_region") || "";
    regionSelect.value = (q.region || savedRegion || "Europe");

    regionSelect.addEventListener("change", () => {
      sessionStorage.setItem("gmcw_region", regionSelect.value || "");
      // reset port when region changes
      portSelect.value = "";
      populatePorts(portSelect);
      updateViatorLink(getPortNameById(portSelect.value));
    });

    populatePorts(portSelect);
    wireUnitToggle();

    const last = restore();
    let desiredPortId = q.port || (last && last.portId) || localStorage.getItem("gmcw:selectedPort") || "";
    const isoDate = q.date || (last && last.date) || "";

    // Ensure port exists within selected region
    const available = Array.from(portSelect.options).map(o => o.value).filter(v => v);
    const portId = (desiredPortId && available.includes(desiredPortId)) ? desiredPortId : (available[0] || "");


    portSelect.value = portId;
    dateInput.value = isoDate;
    localStorage.setItem("gmcw:selectedPort", portSelect.value);
    updateViatorLink(getPortNameById(portSelect.value));

    portSelect.addEventListener("change", () => {
      localStorage.setItem("gmcw:selectedPort", portSelect.value);
      updateViatorLink(getPortNameById(portSelect.value));
    });

    btn.addEventListener("click", async () => {
      if(!dateInput.value) return;
      try{
        btn.disabled = true;
        $("warmthHint").textContent = "Loading...";
        $("rainHint").textContent = "Loading...";
        $("windHint").textContent = "Loading...";
        const res = await analyse(portSelect.value, dateInput.value);
        persist(res);
        renderResults(res);
        history.replaceState(null, "", writeQuery(regionSelect.value, portSelect.value, dateInput.value));
      } catch(e) {
        const msg = "Unable to load historical data for this port/date.";
        $("warmthHint").textContent = msg;
        $("rainHint").textContent = msg;
        $("windHint").textContent = msg;
      } finally {
        btn.disabled = false;
      }
    });

    try{
      if(isoDate){
        $("warmthHint").textContent = "Loading...";
        $("rainHint").textContent = "Loading...";
        $("windHint").textContent = "Loading...";
        const res = await analyse(portId, isoDate);
        persist(res);
        renderResults(res);
      } else if(last) {
        renderResults(last);
      }
    } catch(e) {
      const msg = "Unable to load historical data for this port/date.";
      $("warmthHint").textContent = msg;
      $("rainHint").textContent = msg;
      $("windHint").textContent = msg;
    }
  }

  function getPortNameById(id){
    const p = PORTS.find(x => x.id === id);
    return p ? p.name : "";
  }

  window.GMCW = { initResultsPage };
  document.addEventListener("DOMContentLoaded", () => { wireForm(); });
}
)();