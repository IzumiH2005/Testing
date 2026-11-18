"use strict";
/* =========================================================================
   Réimpression par 3 IA (entraînées pour ce projet, voir ../training/).
   La page photographiée est reconstruite comme si une imprimante couleur
   l'avait imprimée sur une feuille neuve, au même format.

   IA 1 « œil du papier » : vraie couleur de la feuille (code + nom) et aspect du papier nu sur la photo.
   IA 2 « trieur »        : pour chaque point : papier, texte/trait, aplat, image, ou défaut (tache, pli, doigt…).
   IA 3 « imprimante »    : quantité d'encre Cyan, Magenta, Jaune, Noir à déposer en chaque point.
   Impression : couleur du papier × filtres des 4 encres (synthèse soustractive, comme une vraie imprimante).
   ========================================================================= */
const Reprint = (() => {
  const lin = v => v <= 0.04045 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4;
  const enc = v => v <= 0.0031308 ? 12.92 * v : 1.055 * Math.pow(v, 1 / 2.4) - 0.055;
  const INKS = [[0, 174, 239], [236, 0, 140], [255, 242, 0], [16, 16, 16]]; // C, M, J, N à 100 %
  const INK_A = INKS.map(c => c.map(v => 1 - lin(v / 255)));               // part de lumière absorbée
  const ENC = new Uint8ClampedArray(4097); for (let i = 0; i <= 4096; i++) ENC[i] = Math.round(enc(i / 4096) * 255);
  const hex = c => "#" + c.map(v => Math.max(0, Math.min(255, Math.round(v))).toString(16).padStart(2, "0")).join("").toUpperCase();

  function nameFr(rgb) { // même règle que training/common.py
    const [r, g, b] = rgb.map(v => v / 255), mx = Math.max(r, g, b), mn = Math.min(r, g, b), l = (mx + mn) / 2;
    const s = mx === mn ? 0 : l <= 0.5 ? (mx - mn) / (mx + mn) : (mx - mn) / (2 - mx - mn);
    if (s < 0.08 || (l > 0.9 && s < 0.25 && mx - mn < 0.035)) return l > 0.9 ? "blanc" : l > 0.7 ? "gris clair" : l > 0.35 ? "gris" : "noir";
    let h = mx === r ? ((g - b) / (mx - mn)) % 6 : mx === g ? (b - r) / (mx - mn) + 2 : (r - g) / (mx - mn) + 4;
    h = (h * 60 + 360) % 360;
    const N = [[15, "rouge"], [40, "orange"], [65, "jaune"], [160, "vert"], [200, "turquoise"], [255, "bleu"], [290, "violet"], [335, "rose"], [360, "rouge"]];
    let base = N.find(n => h < n[0])[1];
    if (base === "orange" && l > 0.75) base = s < 0.6 ? "crème" : "pêche";
    if (base === "jaune" && l > 0.85 && s < 0.6) base = "crème";
    return l > 0.82 ? base + (l > 0.9 ? " très clair" : " clair") : l < 0.3 ? base + " foncé" : base;
  }

  /* ---------- aides ---------- */
  function canvasOf(w, h) { const c = document.createElement("canvas"); c.width = w; c.height = h; return c; }
  function chw(src, w, h) { // image redimensionnée -> Float32 [3,h,w] 0..1
    const c = canvasOf(w, h), x = c.getContext("2d", { willReadFrequently: true });
    x.imageSmoothingEnabled = true; x.imageSmoothingQuality = "high"; x.drawImage(src, 0, 0, w, h);
    const d = x.getImageData(0, 0, w, h).data, n = w * h, o = new Float32Array(3 * n);
    for (let i = 0; i < n; i++) { o[i] = d[i * 4] / 255; o[n + i] = d[i * 4 + 1] / 255; o[2 * n + i] = d[i * 4 + 2] / 255; }
    return o;
  }
  function resize(a, C, h, w, H, W) { // bilinéaire, centres de pixels (= PyTorch align_corners=False / OpenCV)
    const o = new Float32Array(C * H * W), sy = h / H, sx = w / W, x0 = new Int32Array(W), x1 = new Int32Array(W), fx = new Float32Array(W);
    for (let X = 0; X < W; X++) { let u = (X + 0.5) * sx - 0.5; if (u < 0) u = 0; const i = Math.min(w - 1, u | 0); x0[X] = i; x1[X] = Math.min(w - 1, i + 1); fx[X] = u - i; }
    for (let Y = 0; Y < H; Y++) {
      let v = (Y + 0.5) * sy - 0.5; if (v < 0) v = 0; const j = Math.min(h - 1, v | 0), j1 = Math.min(h - 1, j + 1), fy = v - j;
      for (let c = 0; c < C; c++) { const r0 = c * h * w + j * w, r1 = c * h * w + j1 * w, ob = c * H * W + Y * W;
        for (let X = 0; X < W; X++) { const a0 = a[r0 + x0[X]] + (a[r0 + x1[X]] - a[r0 + x0[X]]) * fx[X], a1 = a[r1 + x0[X]] + (a[r1 + x1[X]] - a[r1 + x0[X]]) * fx[X];
          o[ob + X] = a0 + (a1 - a0) * fy; } }
    }
    return o;
  }
  function crop(a, C, H, W, y0, x0, h, w) {
    const o = new Float32Array(C * h * w);
    for (let c = 0; c < C; c++) for (let y = 0; y < h; y++) o.set(a.subarray(c * H * W + (y0 + y) * W + x0, c * H * W + (y0 + y) * W + x0 + w), c * h * w + y * w);
    return o;
  }
  const tick = () => new Promise(r => setTimeout(r, 0));

  /* ---------- les 3 IA ---------- */
  async function analyse(src, onProg, onStep) {
    const o = await AI.loadRuntime();
    // IA 1 : œil du papier (photo entière en 256 × 256)
    onStep && onStep("IA 1 : couleur du papier…");
    const s1 = await AI.session("paper", onProg);
    const r1 = await s1.run({ photo: new o.Tensor("float32", chw(src, 256, 256), [1, 3, 256, 256]) });
    const paper = Array.from(r1.paper.data), E64 = r1.E.data;
    // IA 2 : trieur (512 px de grand côté)
    onStep && onStep("IA 2 : tri du texte, des images et des défauts…");
    const k2 = 512 / Math.max(src.width, src.height), w2 = Math.round(src.width * k2), h2 = Math.round(src.height * k2);
    const s2 = await AI.session("select", onProg);
    const r2 = await s2.run({ photo: new o.Tensor("float32", chw(src, w2, h2), [1, 3, h2, w2]),
                              E: new o.Tensor("float32", resize(E64, 3, 64, 64, h2, w2), [1, 3, h2, w2]) });
    const sel = r2.sel.data;
    // IA 3 : imprimante (jusqu'à 1280 px, par tuiles qui se chevauchent)
    onStep && onStep("IA 3 : calcul des encres C, M, J, N…");
    const k3 = Math.min(1, 1280 / Math.max(src.width, src.height)), W = Math.round(src.width * k3), H = Math.round(src.height * k3);
    const ph = chw(src, W, H), E = resize(E64, 3, 64, 64, H, W), S = resize(sel, 5, h2, w2, H, W);
    const s3 = await AI.session("print", onProg), cov = new Float32Array(4 * H * W);
    const T = 512, M = 32, starts = n => { if (n <= T) return [0]; const a = []; for (let p = 0; ; p += T - 2 * M) { if (p + T >= n) { a.push(n - T); break; } a.push(p); } return a; };
    const ys = starts(H), xs = starts(W), th = Math.min(T, H), tw = Math.min(T, W);
    let done = 0;
    for (const y0 of ys) for (const x0 of xs) {
      const r3 = await s3.run({ photo: new o.Tensor("float32", crop(ph, 3, H, W, y0, x0, th, tw), [1, 3, th, tw]),
                                E: new o.Tensor("float32", crop(E, 3, H, W, y0, x0, th, tw), [1, 3, th, tw]),
                                sel: new o.Tensor("float32", crop(S, 5, H, W, y0, x0, th, tw), [1, 5, th, tw]) });
      const c = r3.cov.data;
      // on garde le centre de chaque tuile (les bords d'une tuile voient moins de contexte)
      const ya = y0 === 0 ? 0 : M, yb = y0 + th >= H ? th : th - M, xa = x0 === 0 ? 0 : M, xb = x0 + tw >= W ? tw : tw - M;
      for (let ch = 0; ch < 4; ch++) for (let y = ya; y < yb; y++)
        cov.set(c.subarray(ch * th * tw + y * tw + xa, ch * th * tw + y * tw + xb), ch * H * W + (y0 + y) * W + x0 + xa);
      done++; onStep && onStep(`IA 3 : calcul des encres C, M, J, N… ${Math.round(100 * done / (ys.length * xs.length))} %`); await tick();
    }
    return { paper, cov, W, H };
  }

  /* ---------- impression : papier × filtres des encres ---------- */
  function print(a, outW, outH, paperRGB) {
    const cov = (outW === a.W && outH === a.H) ? a.cov : resize(a.cov, 4, a.H, a.W, outH, outW), n = outW * outH;
    const P = paperRGB.map(v => lin(v / 255)), A = INK_A;
    const c = canvasOf(outW, outH), x = c.getContext("2d"), img = x.createImageData(outW, outH), d = img.data;
    for (let i = 0; i < n; i++) {
      const c0 = cov[i], c1 = cov[n + i], c2 = cov[2 * n + i], c3 = cov[3 * n + i];
      for (let ch = 0; ch < 3; ch++) {
        const t = P[ch] * (1 - c0 * A[0][ch]) * (1 - c1 * A[1][ch]) * (1 - c2 * A[2][ch]) * (1 - c3 * A[3][ch]);
        d[i * 4 + ch] = ENC[Math.max(0, Math.min(4096, Math.round(t * 4096)))];
      }
      d[i * 4 + 3] = 255;
    }
    x.putImageData(img, 0, 0);
    return c;
  }

  /* Point d'entrée : page redressée -> page réimprimée (même taille) + infos papier/encres */
  async function run(warped, opts = {}) {
    const a = warped._reprint || (warped._reprint = await analyse(warped, opts.onProg, opts.onStep));
    const found = a.paper.map(v => Math.round(v * 255)), fInfo = { rgb: found, hex: hex(found), name: nameFr(found) };
    const white = opts.paper === "white", usedRGB = white ? [255, 255, 255] : found;
    const out = print(a, warped.width, warped.height, usedRGB);
    const n = a.W * a.H, mean = [0, 1, 2, 3].map(k => { let s = 0; for (let i = 0; i < n; i++) s += a.cov[k * n + i]; return s / n; });
    out._info = { found: fInfo, paper: white ? { rgb: usedRGB, hex: "#FFFFFF", name: "blanc" } : fInfo, inkMean: mean };
    return out;
  }
  return { run, nameFr, hex };
})();
