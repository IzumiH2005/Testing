"use strict";
/* =========================================================================
   Module IA — réseaux de neurones exécutés dans le navigateur
   (onnxruntime-web, WebAssembly). Rien n'est envoyé sur Internet.
     corners : DocAligner (heatmap, LCNet)  → les 4 coins de la feuille (repérage)
     paper   : IA 1 « œil du papier »        → éclairage de la page         ┐ entraînées pour ce projet
     select  : IA 2 « trieur »               → texte / aplat / image / défaut ├ (voir ../training/)
     print   : IA 3 « imprimante »           → encres C, M, J, N             ┘
   Les modèles ne sont téléchargés qu'au premier usage, puis gardés en mémoire.
   ========================================================================= */
const AI = (() => {
  const url = p => new URL("ai/" + p, location.href).href;
  const MODELS = {
    corners: { parts: ["docaligner.onnx.wasm"], mb: 4.8, label: "repérage des coins" },
    paper:   { parts: ["ia1_papier.onnx.wasm"], mb: 14.5, label: "IA 1 · éclairage" },
    select:  { parts: ["ia2_trieur.onnx.wasm"], mb: 3.8, label: "IA 2 · tri" },
    print:   { parts: ["ia3_imprimante.onnx.wasm"], mb: 0.9, label: "IA 3 · imprimante" }
  };
  let ortP = null; const sess = {};

  function loadRuntime() {
    if (ortP) return ortP;
    ortP = new Promise((res, rej) => {
      const s = document.createElement("script"); s.src = url("ort.wasm.min.js");
      s.onload = () => { const o = window.ort; o.env.wasm.wasmPaths = url(""); o.env.wasm.numThreads = 1; o.env.wasm.proxy = false; o.env.logLevel = "error"; res(o); };
      s.onerror = () => rej(new Error("runtime IA introuvable")); document.head.appendChild(s);
    });
    ortP.catch(() => { ortP = null; });
    return ortP;
  }
  async function fetchParts(parts, onProg) { // concatène les morceaux (fichiers ≤ 15 Mo) avec progression
    const bufs = []; let got = 0; const total = parts.reduce((s, p) => s + (p.size || 0), 0);
    for (const p of parts) {
      const r = await fetch(p.url); if (!r.ok) throw new Error("téléchargement " + r.status);
      if (!r.body || !onProg) { const b = new Uint8Array(await r.arrayBuffer()); got += b.length; bufs.push(b); onProg && onProg(got / total); continue; }
      const rd = r.body.getReader();
      for (;;) { const { done, value } = await rd.read(); if (done) break; bufs.push(value); got += value.length; onProg(Math.min(1, got / total)); }
    }
    const out = new Uint8Array(got); let o = 0; for (const b of bufs) { out.set(b, o); o += b.length; } return out;
  }
  function session(name, onProg) {
    if (sess[name]) return sess[name];
    const m = MODELS[name];
    sess[name] = (async () => {
      const o = await loadRuntime();
      const per = m.mb * 1e6 / m.parts.length;
      const bytes = await fetchParts(m.parts.map(p => ({ url: url(p), size: per })), onProg && (f => onProg(f, m)));
      return o.InferenceSession.create(bytes, { executionProviders: ["wasm"], graphOptimizationLevel: "all", logSeverityLevel: 3 });
    })();
    sess[name].catch(() => { delete sess[name]; });
    return sess[name];
  }
  const ready = name => !!sess[name];

  /* ---------- aides image ---------- */
  function canvasOf(w, h) { const c = document.createElement("canvas"); c.width = w; c.height = h; return c; }
  // réduction par moitiés successives (≈ moyenne de zone) : une réduction directe ×6-10 crénelle l'image et aveugle les IA
  function pixels(src, w, h, sx = 0, sy = 0, sw = src.width, sh = src.height) {
    let cur = src, cx = sx, cy = sy, cw = sw, ch = sh;
    while (cw > 2 * w || ch > 2 * h) {
      const nw = Math.max(w, Math.round(cw / 2)), nh = Math.max(h, Math.round(ch / 2)), c = canvasOf(nw, nh), x = c.getContext("2d");
      x.imageSmoothingQuality = "high"; x.drawImage(cur, cx, cy, cw, ch, 0, 0, nw, nh);
      cur = c; cx = 0; cy = 0; cw = nw; ch = nh;
    }
    const c = canvasOf(w, h), x = c.getContext("2d", { willReadFrequently: true });
    x.imageSmoothingQuality = "high"; x.drawImage(cur, cx, cy, cw, ch, 0, 0, w, h);
    return x.getImageData(0, 0, w, h).data;
  }
  function toCHW(d, n, mean, std, scale = 1 / 255) {
    const x = new Float32Array(3 * n);
    for (let i = 0; i < n; i++) for (let c = 0; c < 3; c++) x[c * n + i] = (d[i * 4 + c] * scale - (mean ? mean[c] : 0)) / (std ? std[c] : 1);
    return x;
  }

  /* ---------- 1. coins de la feuille ---------- */
  // box = [sx, sy, sw, sh] : ne regarder qu'une partie de la photo (2e passe, plus précise)
  async function corners(src, onProg, box) {
    const s = await session("corners", onProg), o = window.ort, N = 256, M = 128;
    const [bx, by, bw, bh] = box || [0, 0, src.width, src.height];
    const x = toCHW(pixels(src, N, N, bx, by, bw, bh), N * N);
    const out = await s.run({ [s.inputNames[0]]: new o.Tensor("float32", x, [1, 3, N, N]) });
    const hm = out[s.outputNames[0]].data, pts = [], scores = [];
    for (let ch = 0; ch < 4; ch++) {
      const off = ch * M * M; let bi = 0, bv = -1;
      for (let i = 0; i < M * M; i++) if (hm[off + i] > bv) { bv = hm[off + i]; bi = i; }
      // tache autour du maximum (≥ moitié du pic) → barycentre pondéré, plus précis qu'un seul pixel
      const lim = bv / 2, seen = new Uint8Array(M * M), st = [bi]; seen[bi] = 1; let sw = 0, sx = 0, sy = 0;
      while (st.length) { const i = st.pop(), v = hm[off + i], px = i % M, py = (i / M) | 0; sw += v; sx += v * px; sy += v * py;
        for (const [dx, dy] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) { const nx = px + dx, ny = py + dy; if (nx < 0 || ny < 0 || nx >= M || ny >= M) continue;
          const j = ny * M + nx; if (!seen[j] && hm[off + j] >= lim) { seen[j] = 1; st.push(j); } } }
      pts.push([bx + (sx / sw + 0.5) / M * bw, by + (sy / sw + 0.5) / M * bh]); scores.push(bv);
    }
    // ordre : haut-gauche, haut-droite, bas-droite, bas-gauche ; quad = null si un coin n'est pas sûr
    return { pts, scores, quad: scores.every(v => v >= 0.3) ? pts : null, score: Math.min(...scores) };
  }

  return { MODELS, session, ready, corners, loadRuntime };
})();
