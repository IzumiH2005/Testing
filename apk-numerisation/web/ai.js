"use strict";
/* =========================================================================
   Module IA — réseaux de neurones exécutés dans le navigateur
   (onnxruntime-web, WebAssembly). Rien n'est envoyé sur Internet.
     corners : DocAligner (heatmap, LCNet)  → les 4 coins de la feuille (repérage)
     paper   : IA 1 « œil du papier »        → vraie couleur de la feuille   ┐ entraînées pour ce projet
     select  : IA 2 « trieur »               → texte / aplat / image / défaut ├ (voir ../training/)
     print   : IA 3 « imprimante »           → encres C, M, J, N             ┘
   Les modèles ne sont téléchargés qu'au premier usage, puis gardés en mémoire.
   ========================================================================= */
const AI = (() => {
  const url = p => new URL("ai/" + p, location.href).href;
  const MODELS = {
    corners: { parts: ["docaligner.onnx.wasm"], mb: 4.8, label: "repérage des coins" },
    paper:   { parts: ["ia1_papier.onnx.wasm"], mb: 0, label: "IA 1 · couleur du papier" },
    select:  { parts: ["ia2_trieur.onnx.wasm"], mb: 0, label: "IA 2 · tri" },
    print:   { parts: ["ia3_imprimante.onnx.wasm"], mb: 0, label: "IA 3 · imprimante" }
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
  function pixels(src, w, h, sx = 0, sy = 0, sw = src.width, sh = src.height) {
    const c = canvasOf(w, h), x = c.getContext("2d", { willReadFrequently: true });
    x.imageSmoothingQuality = "high"; x.drawImage(src, sx, sy, sw, sh, 0, 0, w, h);
    return x.getImageData(0, 0, w, h).data;
  }
  function toCHW(d, n, mean, std, scale = 1 / 255) {
    const x = new Float32Array(3 * n);
    for (let i = 0; i < n; i++) for (let c = 0; c < 3; c++) x[c * n + i] = (d[i * 4 + c] * scale - (mean ? mean[c] : 0)) / (std ? std[c] : 1);
    return x;
  }

  /* ---------- 1. coins de la feuille ---------- */
  async function corners(src, onProg) {
    const s = await session("corners", onProg), o = window.ort, N = 256, M = 128;
    const x = toCHW(pixels(src, N, N), N * N);
    const out = await s.run({ [s.inputNames[0]]: new o.Tensor("float32", x, [1, 3, N, N]) });
    const hm = out[s.outputNames[0]].data, quad = []; let score = 1;
    for (let ch = 0; ch < 4; ch++) {
      const off = ch * M * M; let bi = 0, bv = -1;
      for (let i = 0; i < M * M; i++) if (hm[off + i] > bv) { bv = hm[off + i]; bi = i; }
      score = Math.min(score, bv);
      if (bv < 0.3) return { quad: null, score };
      // tache autour du maximum (> 0.3) → barycentre pondéré, plus précis qu'un seul pixel
      const seen = new Uint8Array(M * M), st = [bi]; seen[bi] = 1; let sw = 0, sx = 0, sy = 0;
      while (st.length) { const i = st.pop(), v = hm[off + i], px = i % M, py = (i / M) | 0; sw += v; sx += v * px; sy += v * py;
        for (const [dx, dy] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) { const nx = px + dx, ny = py + dy; if (nx < 0 || ny < 0 || nx >= M || ny >= M) continue;
          const j = ny * M + nx; if (!seen[j] && hm[off + j] >= 0.3) { seen[j] = 1; st.push(j); } } }
      quad.push([(sx / sw + 0.5) / M * src.width, (sy / sw + 0.5) / M * src.height]);
    }
    return { quad, score }; // ordre : haut-gauche, haut-droite, bas-droite, bas-gauche
  }

  return { MODELS, session, ready, corners, loadRuntime };
})();
