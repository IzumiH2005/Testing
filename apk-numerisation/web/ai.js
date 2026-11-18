"use strict";
/* =========================================================================
   Module IA — 4 petits réseaux de neurones exécutés dans le navigateur
   (onnxruntime-web, WebAssembly). Rien n'est envoyé sur Internet.
     corners : DocAligner (heatmap, LCNet)     → les 4 coins de la feuille
     orient  : PP-LCNet doc_ori                → page à l'endroit (0/90/180/270°)
     dewarp  : UVDoc                           → remet à plat une page courbée
     erase   : MI-GAN                          → efface doigts / taches (inpainting)
   Les modèles ne sont téléchargés qu'au premier usage, puis gardés en mémoire.
   ========================================================================= */
const AI = (() => {
  const url = p => new URL("ai/" + p, location.href).href;
  const MODELS = {
    corners: { parts: ["docaligner.onnx.wasm"], mb: 4.8, label: "repérage des coins" },
    orient:  { parts: ["docori.onnx.wasm"], mb: 6.8, label: "orientation" },
    dewarp:  { parts: ["uvdoc.part0.wasm", "uvdoc.part1.wasm", "uvdoc.part2.wasm"], mb: 31.7, label: "remise à plat" },
    erase:   { parts: ["migan.part0.wasm", "migan.part1.wasm"], mb: 28.1, label: "gomme" }
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

  /* ---------- 2. orientation ---------- */
  async function orientation(src, onProg) {
    const s = await session("orient", onProg), o = window.ort, C = 224;
    const k = 256 / Math.min(src.width, src.height), sw = C / k, sh = C / k;
    const d = pixels(src, C, C, (src.width - sw) / 2, (src.height - sh) / 2, sw, sh);
    const x = toCHW(d, C * C, [0.485, 0.456, 0.406], [0.229, 0.224, 0.225]);
    const out = await s.run({ [s.inputNames[0]]: new o.Tensor("float32", x, [1, 3, C, C]) });
    let p = Array.from(out[s.outputNames[0]].data);
    const sum = p.reduce((a, b) => a + b, 0);
    if (Math.abs(sum - 1) > 0.05 || p.some(v => v < 0)) { const mx = Math.max(...p), e = p.map(v => Math.exp(v - mx)), t = e.reduce((a, b) => a + b, 0); p = e.map(v => v / t); }
    const i = p.indexOf(Math.max(...p));
    return { turns: i, conf: p[i] }; // la page est tournée de i×90° dans le sens horaire
  }

  /* ---------- 3. remise à plat d'une page courbée ---------- */
  async function dewarp(src, onProg) { // src : photo recadrée autour de la feuille ; renvoie un canvas de même taille
    const s = await session("dewarp", onProg), o = window.ort;
    const k = Math.min(1, 1800 / Math.max(src.width, src.height)), w = Math.round(src.width * k), h = Math.round(src.height * k), n = w * h;
    const x = toCHW(pixels(src, w, h), n);
    const out = await s.run({ [s.inputNames[0]]: new o.Tensor("float32", x, [1, 3, h, w]) });
    const t = out[s.outputNames[0]], [, , oh, ow] = t.dims, y = t.data, m = oh * ow;
    const c = canvasOf(ow, oh), cx = c.getContext("2d"), img = cx.createImageData(ow, oh), d = img.data;
    for (let i = 0; i < m; i++) { d[i * 4] = y[i] * 255; d[i * 4 + 1] = y[m + i] * 255; d[i * 4 + 2] = y[2 * m + i] * 255; d[i * 4 + 3] = 255; }
    cx.putImageData(img, 0, 0); return c;
  }

  /* ---------- 4. gomme : reconstruit la zone masquée ---------- */
  async function erase(src, mask, onProg) { // mask : Uint8Array (1 = à effacer), taille src ; renvoie un nouveau canvas
    const s = await session("erase", onProg), o = window.ort, W = src.width, H = src.height;
    let x0 = W, y0 = H, x1 = -1, y1 = -1;
    for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) if (mask[y * W + x]) { if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y; }
    const out = canvasOf(W, H), ox = out.getContext("2d"); ox.drawImage(src, 0, 0);
    if (x1 < 0) return out;
    // zone de travail : le masque + du contexte autour, ramenée à 512 px max (taille d'entraînement)
    const bw = x1 - x0 + 1, bh = y1 - y0 + 1, side = Math.min(Math.max(W, H), Math.max(bw, bh) * 1.8, Math.max(bw, bh) + 400);
    let rw = Math.min(W, Math.max(bw + 32, side)), rh = Math.min(H, Math.max(bh + 32, side));
    let rx = Math.round(Math.max(0, Math.min(W - rw, (x0 + x1) / 2 - rw / 2))), ry = Math.round(Math.max(0, Math.min(H - rh, (y0 + y1) / 2 - rh / 2)));
    rw = Math.round(rw); rh = Math.round(rh);
    const k = Math.min(1, 512 / Math.max(rw, rh)), w = Math.max(8, Math.round(rw * k)), h = Math.max(8, Math.round(rh * k)), n = w * h;
    const d = pixels(src, w, h, rx, ry, rw, rh), im = new Uint8Array(3 * n), mk = new Uint8Array(n);
    for (let i = 0; i < n; i++) { im[i] = d[i * 4]; im[n + i] = d[i * 4 + 1]; im[2 * n + i] = d[i * 4 + 2]; }
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) { // masque réduit, un peu élargi (255 = garder, 0 = trou)
      let hole = 0; const sx = rx + x / k, sy = ry + y / k, r = Math.ceil(1 / k) + 1;
      for (let dy = -r; dy <= r && !hole; dy += Math.max(1, r)) for (let dx = -r; dx <= r && !hole; dx += Math.max(1, r)) {
        const px = Math.round(sx + dx), py = Math.round(sy + dy); if (px >= 0 && py >= 0 && px < W && py < H && mask[py * W + px]) hole = 1; }
      mk[y * w + x] = hole ? 0 : 255;
    }
    const res = await s.run({ image: new o.Tensor("uint8", im, [1, 3, h, w]), mask: new o.Tensor("uint8", mk, [1, 1, h, w]) });
    const r = res[s.outputNames[0]].data, small = canvasOf(w, h), sx2 = small.getContext("2d"), simg = sx2.createImageData(w, h);
    for (let i = 0; i < n; i++) { simg.data[i * 4] = r[i]; simg.data[i * 4 + 1] = r[n + i]; simg.data[i * 4 + 2] = r[2 * n + i]; simg.data[i * 4 + 3] = 255; }
    sx2.putImageData(simg, 0, 0);
    // recolle uniquement les pixels masqués (bord adouci) à pleine résolution
    const big = canvasOf(rw, rh), bx = big.getContext("2d"); bx.imageSmoothingQuality = "high"; bx.drawImage(small, 0, 0, rw, rh);
    const bd = bx.getImageData(0, 0, rw, rh).data, od = ox.getImageData(rx, ry, rw, rh);
    const soft = new Float32Array(rw * rh); for (let y = 0; y < rh; y++) for (let x = 0; x < rw; x++) soft[y * rw + x] = mask[(ry + y) * W + rx + x];
    const rad = Math.max(2, Math.round(2 / k)), tmp = new Float32Array(rw * rh);
    for (let y = 0; y < rh; y++) { let acc = 0; for (let x = -rad; x < rw + rad; x++) { if (x + rad < rw) acc += soft[y * rw + x + rad]; if (x - rad - 1 >= 0) acc -= soft[y * rw + x - rad - 1]; if (x >= 0 && x < rw) tmp[y * rw + x] = acc; } }
    for (let x = 0; x < rw; x++) { let acc = 0; for (let y = -rad; y < rh + rad; y++) { if (y + rad < rh) acc += tmp[(y + rad) * rw + x]; if (y - rad - 1 >= 0) acc -= tmp[(y - rad - 1) * rw + x]; if (y >= 0 && y < rh) soft[y * rw + x] = Math.min(1, 2 * acc / ((2 * rad + 1) ** 2)); } }
    for (let i = 0; i < rw * rh; i++) { const a = soft[i]; if (!a) continue; for (let c = 0; c < 3; c++) od.data[i * 4 + c] = od.data[i * 4 + c] * (1 - a) + bd[i * 4 + c] * a; }
    ox.putImageData(od, rx, ry);
    return out;
  }

  /* ---------- détection automatique des doigts (couleur peau touchant le bord) ---------- */
  function skinMask(src) {
    const W = src.width, H = src.height, k = Math.min(1, 360 / Math.max(W, H)), w = Math.round(W * k), h = Math.round(H * k), n = w * h;
    const d = pixels(src, w, h), m = new Uint8Array(n), CR = new Float32Array(n), CB = new Float32Array(n);
    for (let i = 0; i < n; i++) { const r = d[i * 4], g = d[i * 4 + 1], b = d[i * 4 + 2];
      CR[i] = 128 + 0.5 * r - 0.4187 * g - 0.0813 * b; CB[i] = 128 - 0.1687 * r - 0.3313 * g + 0.5 * b; }
    // teinte du papier (médiane) : sous une lampe chaude le papier jaunit, il ne doit pas passer pour de la peau
    const med = a => { const t = Float32Array.from(a).sort(); return t[t.length >> 1]; }, pcr = med(CR), pcb = med(CB);
    for (let i = 0; i < n; i++) { const r = d[i * 4], g = d[i * 4 + 1], b = d[i * 4 + 2], Y = 0.299 * r + 0.587 * g + 0.114 * b, cr = CR[i], cb = CB[i];
      m[i] = Y > 40 && cr > 136 && cr < 180 && cb > 77 && cb < 128 && r > g && g > b * 0.9 && (r - b) / r > 0.25 &&
             Math.hypot(cr - pcr, cb - pcb) > 9 ? 1 : 0; }
    // composantes connexes : on ne garde que celles qui touchent un bord (un doigt entre par le bord)
    const lab = new Int32Array(n), keep = new Uint8Array(n); let id = 0, any = false;
    for (let s0 = 0; s0 < n; s0++) { if (!m[s0] || lab[s0]) continue; id++; const st = [s0], comp = []; lab[s0] = id; let edge = false;
      while (st.length) { const i = st.pop(); comp.push(i); const x = i % w, y = (i / w) | 0; if (x === 0 || y === 0 || x === w - 1 || y === h - 1) edge = true;
        for (const j of [i - 1, i + 1, i - w, i + w]) { if (j < 0 || j >= n || Math.abs((j % w) - x) > 1 || !m[j] || lab[j]) continue; lab[j] = id; st.push(j); } }
      if (edge && comp.length > n * 0.002 && comp.length < n * 0.3) { any = true; for (const i of comp) keep[i] = 1; } }
    if (!any) return null;
    // élargit (ombre et bord du doigt) puis remet à la taille réelle
    const r = Math.max(2, Math.round(w * 0.018)), dil = new Uint8Array(n);
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) { if (!keep[y * w + x]) continue;
      for (let dy = -r; dy <= r; dy++) for (let dx = -r; dx <= r; dx++) { const nx = x + dx, ny = y + dy; if (nx >= 0 && ny >= 0 && nx < w && ny < h && dx * dx + dy * dy <= r * r) dil[ny * w + nx] = 1; } }
    const full = new Uint8Array(W * H);
    for (let y = 0; y < H; y++) { const sy = Math.min(h - 1, (y * k) | 0); for (let x = 0; x < W; x++) full[y * W + x] = dil[sy * w + Math.min(w - 1, (x * k) | 0)]; }
    return full;
  }

  return { MODELS, session, ready, corners, orientation, dewarp, erase, skinMask, loadRuntime };
})();
