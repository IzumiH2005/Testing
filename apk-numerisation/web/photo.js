"use strict";
/* =========================================================================
   Mode « photo » : pages presque entièrement imprimées (couvertures, affiches).
   Même règles que training/finish.py (enhance_photo, reprint_over_photo).

   1. La photo redressée est améliorée (balance des blancs, noirs, bruit, netteté).
   2. Réimpression partielle : le fond reste la photo (dégradés, bandes, motifs) ;
      seuls les éléments nets (texte, carrés, logos) sont réimprimés par-dessus
      en couleur unie, à bord franc. En cas de doute (reflet, rayure, bord flou),
      l'élément n'est pas touché.
   ========================================================================= */
const Photo = (() => {
  const OUT_LONG = 2400, PHOTO_MAX_PAPER = 0.3;

  /* ---------- couleurs : sRGB 0..1 <-> Lab (D65, comme OpenCV) ---------- */
  const LIN = new Float32Array(4097);
  for (let i = 0; i <= 4096; i++) { const v = i / 4096; LIN[i] = v <= 0.04045 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; }
  const lin = v => { const x = (v < 0 ? 0 : v > 1 ? 1 : v) * 4096, i = x | 0; return i >= 4096 ? LIN[4096] : LIN[i] + (LIN[i + 1] - LIN[i]) * (x - i); };
  const fLab = t => t > 0.008856 ? Math.cbrt(t) : 7.787 * t + 16 / 116;
  function toLab(r, g, b, out, o) {
    const R = lin(r), G = lin(g), B = lin(b);
    const X = (0.412453 * R + 0.357580 * G + 0.180423 * B) / 0.950456, Y = 0.212671 * R + 0.715160 * G + 0.072169 * B,
          Z = (0.019334 * R + 0.119193 * G + 0.950227 * B) / 1.088754;
    const fx = fLab(X), fy = fLab(Y), fz = fLab(Z);
    out[o] = Y > 0.008856 ? 116 * fy - 16 : 903.3 * Y; out[o + 1] = 500 * (fx - fy); out[o + 2] = 200 * (fy - fz);
  }
  function labPlanes(I, n) { // I planaire [3,n] -> L, a, b planaires
    const L = new Float32Array(3 * n), t = [0, 0, 0];
    for (let i = 0; i < n; i++) { toLab(I[i], I[n + i], I[2 * n + i], t, 0); L[i] = t[0]; L[n + i] = t[1]; L[2 * n + i] = t[2]; }
    return L;
  }
  const lab1 = c => { const t = [0, 0, 0]; toLab(c[0], c[1], c[2], t, 0); return t; };
  function labToRgb([L, a, b]) {
    const fy = (L + 16) / 116, fx = fy + a / 500, fz = fy - b / 200;
    const inv = f => f > 0.206893 ? f * f * f : (f - 16 / 116) / 7.787;
    const X = inv(fx) * 0.950456, Y = L > 8 ? fy * fy * fy : L / 903.3, Z = inv(fz) * 1.088754;
    const R = 3.240479 * X - 1.537150 * Y - 0.498535 * Z, G = -0.969256 * X + 1.875992 * Y + 0.041556 * Z, B = 0.055648 * X - 0.204043 * Y + 1.057311 * Z;
    const enc = v => { v = Math.max(0, Math.min(1, v)); return v <= 0.0031308 ? 12.92 * v : 1.055 * v ** (1 / 2.4) - 0.055; };
    return [enc(R), enc(G), enc(B)];
  }
  const dist3 = (p, q) => Math.hypot(p[0] - q[0], p[1] - q[1], p[2] - q[2]);

  /* ---------- aides image ---------- */
  function canvasOf(w, h) { const c = document.createElement("canvas"); c.width = w; c.height = h; return c; }
  function planar(src, w, h) { // canvas -> Float32 [3, w*h] 0..1 (redimensionné en haute qualité)
    const c = canvasOf(w, h), x = c.getContext("2d", { willReadFrequently: true });
    x.imageSmoothingEnabled = true; x.imageSmoothingQuality = "high"; x.drawImage(src, 0, 0, w, h);
    const d = x.getImageData(0, 0, w, h).data, n = w * h, o = new Float32Array(3 * n);
    for (let i = 0; i < n; i++) { o[i] = d[4 * i] / 255; o[n + i] = d[4 * i + 1] / 255; o[2 * n + i] = d[4 * i + 2] / 255; }
    return o;
  }
  function toCanvas(I, w, h) {
    const n = w * h, c = canvasOf(w, h), x = c.getContext("2d"), img = x.createImageData(w, h), d = img.data;
    for (let i = 0; i < n; i++) { d[4 * i] = I[i] * 255 + 0.5; d[4 * i + 1] = I[n + i] * 255 + 0.5; d[4 * i + 2] = I[2 * n + i] * 255 + 0.5; d[4 * i + 3] = 255; }
    x.putImageData(img, 0, 0); return c;
  }
  function quantile(arr, q) { // comme numpy (interpolation linéaire) ; arr est trié sur place
    const n = arr.length; if (!n) return NaN;
    arr.sort(); const p = q * (n - 1), i = Math.floor(p), f = p - i;
    return i + 1 < n ? arr[i] + (arr[i + 1] - arr[i]) * f : arr[i];
  }
  function histQuantile(v, n, q, step = 1) { // quantile approché (4096 cases) d'un tableau 0..1
    const h = new Uint32Array(4097); let cnt = 0;
    for (let i = 0; i < n; i += step) { h[Math.max(0, Math.min(4096, Math.round(v[i] * 4096)))]++; cnt++; }
    const target = q * cnt; let c = 0;
    for (let k = 0; k <= 4096; k++) { c += h[k]; if (c > target) return k / 4096; }
    return 1;
  }
  // flou gaussien séparable, taille de noyau et bord « reflect 101 » comme OpenCV (images flottantes)
  function gauss(a, w, h, sigma) {
    const ks = Math.round(sigma * 8 + 1) | 1, r = ks >> 1, k = new Float32Array(ks); let s = 0;
    for (let i = 0; i < ks; i++) { k[i] = Math.exp(-((i - r) ** 2) / (2 * sigma * sigma)); s += k[i]; }
    for (let i = 0; i < ks; i++) k[i] /= s;
    const refl = (i, n) => { if (n === 1) return 0; while (i < 0 || i >= n) i = i < 0 ? -i : 2 * n - 2 - i; return i; };
    const t = new Float32Array(w * h), o = new Float32Array(w * h), xi = new Int32Array(w + 2 * r), yi = new Int32Array(h + 2 * r);
    for (let i = -r; i < w + r; i++) xi[i + r] = refl(i, w);
    for (let i = -r; i < h + r; i++) yi[i + r] = refl(i, h);
    for (let y = 0; y < h; y++) { const b = y * w;
      for (let x = 0; x < w; x++) { let v = 0; for (let j = 0; j < ks; j++) v += k[j] * a[b + xi[x + j]]; t[b + x] = v; } }
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) { let v = 0; for (let j = 0; j < ks; j++) v += k[j] * t[yi[y + j] * w + x]; o[y * w + x] = v; }
    return o;
  }
  // max (dilatation) ou min (érosion) sur un carré k × k ; les points hors image sont ignorés (comme OpenCV)
  function morph(m, w, h, k, dil) {
    const r = k >> 1, t = new Uint8Array(w * h), o = new Uint8Array(w * h), hit = dil ? 1 : 0;
    for (let y = 0; y < h; y++) { const b = y * w;
      for (let x = 0; x < w; x++) { let v = dil ? 0 : 1; const x0 = Math.max(0, x - r), x1 = Math.min(w - 1, x + r);
        for (let j = x0; j <= x1; j++) if (m[b + j] === hit) { v = hit; break; } t[b + x] = v; } }
    for (let y = 0; y < h; y++) { const y0 = Math.max(0, y - r), y1 = Math.min(h - 1, y + r);
      for (let x = 0; x < w; x++) { let v = dil ? 0 : 1;
        for (let j = y0; j <= y1; j++) if (t[j * w + x] === hit) { v = hit; break; } o[y * w + x] = v; } }
    return o;
  }
  // médiane glissante k × k sur une image 8 bits (histogramme, bord répliqué), comme cv2.medianBlur
  function median8(u, w, h, k) {
    const r = k >> 1, o = new Uint8Array(w * h), half = (k * k) >> 1, cl = (v, n) => v < 0 ? 0 : v >= n ? n - 1 : v;
    for (let y = 0; y < h; y++) {
      const hist = new Uint32Array(256);
      for (let dy = -r; dy <= r; dy++) for (let dx = -r; dx <= r; dx++) hist[u[cl(y + dy, h) * w + cl(dx, w)]]++;
      for (let x = 0; x < w; x++) {
        if (x > 0) for (let dy = -r; dy <= r; dy++) { const row = cl(y + dy, h) * w; hist[u[row + cl(x - r - 1, w)]]--; hist[u[row + cl(x + r, w)]]++; }
        let c = 0, v = 0; for (; v < 256; v++) { c += hist[v]; if (c > half) break; }
        o[y * w + x] = v;
      }
    }
    return o;
  }
  function resizeBilinear(a, h, w, H, W) { // un plan
    const o = new Float32Array(H * W), sy = h / H, sx = w / W;
    for (let Y = 0; Y < H; Y++) {
      let v = (Y + 0.5) * sy - 0.5; if (v < 0) v = 0; const j = Math.min(h - 1, v | 0), j1 = Math.min(h - 1, j + 1), fy = v - j;
      for (let X = 0; X < W; X++) {
        let u = (X + 0.5) * sx - 0.5; if (u < 0) u = 0; const i = Math.min(w - 1, u | 0), i1 = Math.min(w - 1, i + 1), fx = u - i;
        const a0 = a[j * w + i] + (a[j * w + i1] - a[j * w + i]) * fx, a1 = a[j1 * w + i] + (a[j1 * w + i1] - a[j1 * w + i]) * fx;
        o[Y * W + X] = a0 + (a1 - a0) * fy;
      }
    }
    return o;
  }
  // composantes connexes (8-voisins) avec boîtes et aires
  function components(mask, w, h) {
    const lbl = new Int32Array(w * h), par = [0];
    const find = x => { while (par[x] !== x) { par[x] = par[par[x]]; x = par[x]; } return x; };
    const uni = (a, b) => { a = find(a); b = find(b); if (a !== b) { if (a < b) par[b] = a; else par[a] = b; } };
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
      const i = y * w + x; if (!mask[i]) continue;
      let l = 0; const nb = [];
      if (x > 0 && lbl[i - 1]) nb.push(lbl[i - 1]);
      if (y > 0) { if (lbl[i - w]) nb.push(lbl[i - w]); if (x > 0 && lbl[i - w - 1]) nb.push(lbl[i - w - 1]); if (x < w - 1 && lbl[i - w + 1]) nb.push(lbl[i - w + 1]); }
      if (!nb.length) { l = par.length; par.push(l); } else { l = nb[0]; for (let k = 1; k < nb.length; k++) uni(l, nb[k]); }
      lbl[i] = l;
    }
    const map = new Int32Array(par.length); let n = 1;
    for (let k = 1; k < par.length; k++) { const r = find(k); if (r === k) map[k] = n++; }
    for (let k = 1; k < par.length; k++) map[k] = map[find(k)];
    const st = { x0: new Int32Array(n).fill(1e9), y0: new Int32Array(n).fill(1e9), x1: new Int32Array(n).fill(-1), y1: new Int32Array(n).fill(-1), a: new Int32Array(n) };
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
      const i = y * w + x; if (!lbl[i]) continue; const l = lbl[i] = map[lbl[i]];
      if (x < st.x0[l]) st.x0[l] = x; if (x > st.x1[l]) st.x1[l] = x; if (y < st.y0[l]) st.y0[l] = y; if (y > st.y1[l]) st.y1[l] = y; st.a[l]++;
    }
    return { lbl, n, st };
  }

  // filtre bilatéral : moyenne des voisins proches et de même luminosité (les bords restent nets)
  function bilateral(I, W, H, R, ss, sr) {
    const n = W * H, O = new Float32Array(3 * n), Lm = new Float32Array(n), k2 = 1 / (2 * sr * sr), ws = [];
    for (let d = -R; d <= R; d++) ws.push(Math.exp(-d * d / (2 * ss * ss)));
    for (let i = 0; i < n; i++) Lm[i] = (I[i] + I[n + i] + I[2 * n + i]) / 3;
    for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
      const i = y * W + x, l0 = Lm[i]; let s = 0, r = 0, g = 0, b = 0;
      for (let dy = -R; dy <= R; dy++) { const yy = y + dy; if (yy < 0 || yy >= H) continue; const wy = ws[dy + R], row = yy * W;
        for (let dx = -R; dx <= R; dx++) { const xx = x + dx; if (xx < 0 || xx >= W) continue;
          const j = row + xx, d = Lm[j] - l0, wt = wy * ws[dx + R] * Math.exp(-d * d * k2);
          s += wt; r += wt * I[j]; g += wt * I[n + j]; b += wt * I[2 * n + j]; } }
      O[i] = r / s; O[n + i] = g / s; O[2 * n + i] = b / s;
    }
    return O;
  }
  const DENOISE = { passes: 1, r: 2, ss: 1.5, sr: 0.03 };

  /* ---------- choix du mode d'après l'IA 2 ---------- */
  function pageMode(sel, n) { // sel [5,n] : part des points « papier » sûrs
    let c = 0; for (let i = 0; i < n; i++) if (sel[i] > 0.6) c++;
    const paper = c / n; return { mode: paper < PHOTO_MAX_PAPER ? "photo" : "reprint", paper };
  }

  /* ---------- 1. photo améliorée ---------- */
  function enhance(src) {
    // travail à la taille d'origine si elle est plus petite (le bruit est retiré avant l'agrandissement)
    const k = OUT_LONG / Math.max(src.width, src.height), kw = Math.min(1, k);
    const W = Math.round(src.width * kw), H = Math.round(src.height * kw), n = W * H;
    const I = planar(src, W, H), R = I.subarray(0, n), G = I.subarray(n, 2 * n), B = I.subarray(2 * n);
    // balance des blancs : le blanc le plus clair et peu coloré de la page sert de référence
    const Lm = new Float32Array(n); for (let i = 0; i < n; i++) Lm[i] = (R[i] + G[i] + B[i]) / 3;
    const q97 = histQuantile(Lm, n, 0.97);
    const idx = []; for (let i = 0; i < n; i++) { const mx = Math.max(R[i], G[i], B[i]), mn = Math.min(R[i], G[i], B[i]);
      if (Lm[i] > q97 && (mx - mn) / Math.max(mx, 1e-3) < 0.3) idx.push(i); }
    let gain = [1, 1, 1], ref = null;
    if (idx.length > 0.002 * n) {
      ref = [R, G, B].map(P => { const v = new Float32Array(idx.length); idx.forEach((i, j) => { v[j] = P[i]; }); return quantile(v, 0.5); });
      gain = ref.map(v => Math.min(1.5, Math.max(0.75, 0.96 / Math.max(v, 1e-3))));
    }
    for (let c = 0; c < 3; c++) { const P = I.subarray(c * n, (c + 1) * n), g = gain[c]; for (let i = 0; i < n; i++) P[i] = Math.min(1, P[i] * g); }
    // niveaux : noirs un peu plus profonds
    for (let c = 0; c < 3; c++) { const P = I.subarray(c * n, (c + 1) * n), lo = Math.min(0.12, histQuantile(P, n, 0.003)), s = 1 / Math.max(1 - lo, 1e-3);
      for (let i = 0; i < n; i++) P[i] = Math.max(0, Math.min(1, (P[i] - lo) * s)); }
    // bruit du capteur : lissage qui s'arrête aux bords (filtre bilatéral), comme un débruitage doux
    const P_ = DENOISE; let O = I;
    for (let p = 0; p < P_.passes; p++) O = bilateral(O, W, H, P_.r, P_.ss, P_.sr);
    let OW = W, OH = H;
    if (k > 1) { OW = Math.round(src.width * k); OH = Math.round(src.height * k); O = planar(toCanvas(O, W, H), OW, OH); }
    const on = OW * OH;
    // netteté douce
    const sig = Math.max(1, 0.0006 * OUT_LONG);
    for (let c = 0; c < 3; c++) { const P = O.subarray(c * on, (c + 1) * on), bl = gauss(P, OW, OH, sig);
      for (let i = 0; i < on; i++) P[i] = Math.max(0, Math.min(1, P[i] + 0.6 * (P[i] - bl[i]))); }
    return { I: O, W: OW, H: OH, ref };
  }
  function enhanceCanvas(src) { const e = enhance(src); return toCanvas(e.I, e.W, e.H);
  }

  /* ---------- 2. réimpression partielle par-dessus la photo ---------- */
  function reprintOver(src, sel, w2, h2) {
    const T0 = performance.now();
    const { I, W, H } = enhance(src), n = W * H, L0 = Math.max(W, H);
    const lab = labPlanes(I, n);
    // fond local : médiane large calculée en petit (les éléments fins disparaissent, les dégradés restent)
    const s = 600 / L0, ws = Math.round(W * s), hs = Math.round(H * s), ksz = Math.floor(0.035 * 600) | 1;
    const small = planar(toCanvas(I, W, H), ws, hs), Bp = new Float32Array(3 * n);
    for (let c = 0; c < 3; c++) {
      const u = new Uint8Array(ws * hs); for (let i = 0; i < ws * hs; i++) u[i] = small[c * ws * hs + i] * 255; // troncature, comme astype(uint8)
      const md = median8(u, ws, hs, ksz), f = new Float32Array(ws * hs); for (let i = 0; i < ws * hs; i++) f[i] = md[i] / 255;
      Bp.set(resizeBilinear(gauss(f, ws, hs, 2), hs, ws, H, W), c * n);
    }
    const labB = labPlanes(Bp, n), D = new Float32Array(n), cand = new Uint8Array(n);
    for (let i = 0; i < n; i++) { D[i] = Math.hypot(lab[i] - labB[i], lab[n + i] - labB[n + i], lab[2 * n + i] - labB[2 * n + i]); cand[i] = D[i] > 22 ? 1 : 0; }
    // pente de l'écart (bord net = pente forte)
    const Ds = gauss(D, W, H, 1), Gm = new Float32Array(n);
    for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
      const i = y * W + x;
      const gx = x === 0 ? Ds[i + 1] - Ds[i] : x === W - 1 ? Ds[i] - Ds[i - 1] : (Ds[i + 1] - Ds[i - 1]) / 2;
      const gy = y === 0 ? Ds[i + W] - Ds[i] : y === H - 1 ? Ds[i] - Ds[i - W] : (Ds[i + W] - Ds[i - W]) / 2;
      Gm[i] = Math.hypot(gx, gy);
    }
    const sx = w2 / W, sy = h2 / H, defaut = (x, y) => { // proba « défaut » de l'IA 2 (bilinéaire)
      let u = (x + 0.5) * sx - 0.5, v = (y + 0.5) * sy - 0.5; if (u < 0) u = 0; if (v < 0) v = 0;
      const i = Math.min(w2 - 1, u | 0), j = Math.min(h2 - 1, v | 0), i1 = Math.min(w2 - 1, i + 1), j1 = Math.min(h2 - 1, j + 1), fx = u - i, fy = v - j, o = 4 * w2 * h2;
      const a0 = sel[o + j * w2 + i] + (sel[o + j * w2 + i1] - sel[o + j * w2 + i]) * fx, a1 = sel[o + j1 * w2 + i] + (sel[o + j1 * w2 + i1] - sel[o + j1 * w2 + i]) * fx;
      return a0 + (a1 - a0) * fy;
    };
    const { lbl, n: nc, st } = components(cand, W, H);
    const cands = [];
    for (let id = 1; id < nc; id++) {
      const x = st.x0[id], y = st.y0[id], w = st.x1[id] - x + 1, h = st.y1[id] - y + 1, a = st.a[id];
      if (a < 1e-5 * n || Math.max(w, h) > 0.12 * L0) continue;
      const thin = Math.min(w, h), long = Math.max(w, h);
      if (thin < 0.005 * L0 && long > 2.5 * thin) continue;              // trait très fin isolé : rayure probable
      const X0 = Math.max(0, x - 9), Y0 = Math.max(0, y - 9), X1 = Math.min(W, x + w + 9), Y1 = Math.min(H, y + h + 9), lw = X1 - X0, lh = Y1 - Y0, ln = lw * lh;
      const m = new Uint8Array(ln), free = new Uint8Array(ln), gi = k => (Y0 + ((k / lw) | 0)) * W + X0 + (k % lw);
      for (let k = 0; k < ln; k++) { const l = lbl[gi(k)]; m[k] = l === id ? 1 : 0; free[k] = l === 0 ? 1 : 0; }
      // l'IA 2 y voit un défaut (rayure, tache, bord)
      let pd = 0; for (let k = 0; k < ln; k++) if (m[k]) pd += defaut(X0 + k % lw, Y0 + ((k / lw) | 0));
      if (pd / a > 0.15) continue;
      const d = new Float32Array(a); let j = 0; for (let k = 0; k < ln; k++) if (m[k]) d[j++] = D[gi(k)];
      const q90 = Math.max(quantile(d, 0.9), 1e-3), q60 = quantile(d, 0.6);
      const d3 = morph(m, lw, lh, 3, true), e3 = morph(m, lw, lh, 3, false), d5 = morph(m, lw, lh, 5, true), d15 = morph(m, lw, lh, 15, true);
      const rim = [], ring = [];
      for (let k = 0; k < ln; k++) { if (d3[k] && !e3[k]) rim.push(Gm[gi(k)]); if (d15[k] && !d5[k] && free[k]) ring.push(D[gi(k)]); }
      const sharp = quantile(Float32Array.from(rim), 0.5) / q90, noise = ring.length ? quantile(Float32Array.from(ring), 0.5) : 0, solid = a / (w * h);
      if (!(sharp >= 0.12 || (solid > 0.85 && sharp >= 0.06 && thin > 0.01 * L0))) continue; // bord progressif : reflet ou flou
      const core = []; for (let k = 0; k < ln; k++) if (m[k] && D[gi(k)] > q60) core.push(gi(k));
      if (!core.length) for (let k = 0; k < ln; k++) if (m[k]) core.push(gi(k));
      const ink0 = [0, 1, 2].map(c => quantile(Float32Array.from(core, i => I[c * n + i]), 0.5));
      cands.push({ id, X0, Y0, lw, lh, m, d5, ink0, lab: lab1(ink0), a, cx: x + w / 2, cy: y + h / 2, h, noise, sharp, solid });
    }
    // lignes : éléments voisins de même taille et même encre (une ligne de texte, une rangée de carrés)
    const par = cands.map((_, i) => i), find = u => { while (par[u] !== u) { par[u] = par[par[u]]; u = par[u]; } return u; };
    for (let u = 0; u < cands.length; u++) { const e = cands[u];
      for (let v = u + 1; v < cands.length; v++) { const f = cands[v];
        if (0.75 < f.h / e.h && f.h / e.h < 1.33 && Math.abs(f.cy - e.cy) < 0.5 * e.h && Math.abs(f.cx - e.cx) < 2.5 * e.h && dist3(f.lab, e.lab) < 25) par[find(u)] = find(v);
      } }
    const lines = new Map();
    cands.forEach((e, u) => { const r = find(u); if (!lines.has(r)) lines.set(r, []); lines.get(r).push(e); });
    // décision par ligne entière (plus sûre qu'une lettre seule) : une ligne nette sur fond calme est
    // réimprimée en entier ; une ligne sous un reflet (fond agité, bords mous) reste en photo.
    // Élément isolé : réimprimé seulement si le fond autour est calme et le bord franc (ou forme pleine).
    const med = (ln, key) => quantile(Float32Array.from(ln, e => e[key]), 0.5);
    const elems = [];
    for (const ln of lines.values()) {
      if (ln.length >= 3) { if (med(ln, 'noise') <= 9 && med(ln, 'sharp') >= 0.17) elems.push(...ln); }
      else for (const e of ln) if (e.noise <= 9 && (e.sharp >= 0.17 || e.solid > 0.85)) elems.push(e);
    }
    // palette commune : des encres proches (même blanc, même jaune) deviennent une seule couleur
    elems.sort((p, q) => q.a - p.a);
    const pal = [];
    for (const e of elems) { let c = pal.find(c => dist3(e.lab, c.lab) < 20); if (!c) { c = { lab: e.lab.slice(), a: 0 }; pal.push(c); } c.a += e.a; e.c = c; }
    for (const c of pal) { if (c.lab[0] > 75 && Math.hypot(c.lab[1], c.lab[2]) < 18) c.lab = [100, 0, 0]; c.rgb = labToRgb(c.lab); } // presque blanc -> blanc pur
    // part d'encre de chaque point : projection de la photo sur le segment fond -> encre
    const alpha = new Float32Array(n), ink = new Float32Array(3 * n);
    for (const e of elems) {
      const { X0, Y0, lw, lh, d5, ink0 } = e, rgb = e.c.rgb;
      for (let k = 0; k < lw * lh; k++) { if (!d5[k]) continue;
        const i = (Y0 + ((k / lw) | 0)) * W + X0 + (k % lw);
        let num = 0, den = 0; for (let c = 0; c < 3; c++) { const b = Bp[c * n + i], v = ink0[c] - b; num += (I[c * n + i] - b) * v; den += v * v; }
        const t = Math.max(0, Math.min(1, num / Math.max(den, 1e-4)));
        if (t > alpha[i]) { alpha[i] = t; ink[i] = rgb[0]; ink[n + i] = rgb[1]; ink[2 * n + i] = rgb[2]; } }
    }
    // rendu : bord adouci d'un demi-point, fond lissé sous les éléments (plus de halo de la photo)
    const ab = gauss(alpha, W, H, 0.8), zm = new Uint8Array(n); for (let i = 0; i < n; i++) zm[i] = alpha[i] > 0.05 ? 1 : 0;
    const zd = morph(zm, W, H, 7, true), zf = new Float32Array(n); for (let i = 0; i < n; i++) zf[i] = zd[i];
    const zone = gauss(zf, W, H, 2);
    const c = canvasOf(W, H), cx = c.getContext("2d"), img = cx.createImageData(W, H), px = img.data;
    for (let i = 0; i < n; i++) {
      let t = Math.max(0, Math.min(1, (ab[i] - 0.3) / 0.4)); t = t * t * (3 - 2 * t); const z = zone[i];
      for (let ch = 0; ch < 3; ch++) { const o = ch * n + i, v = (I[o] * (1 - z) + Bp[o] * z) * (1 - t) + ink[o] * t; px[4 * i + ch] = v * 255 + 0.5; }
      px[4 * i + 3] = 255;
    }
    cx.putImageData(img, 0, 0);
    c._photoInfo = { ms: Math.round(performance.now() - T0), elements: elems.length, inks: [...new Set(pal.map(p => p.rgb.map(v => Math.round(v * 255)).join()))].map(t => t.split(',').map(Number)) };
    return c;
  }

  // papier presque blanc (blanc cassé, grisé ou crème léger) -> blanc de photocopie pur
  function nearWhite(rgb255) { const [L, a, b] = lab1(rgb255.map(v => v / 255)); return L > 80 && Math.hypot(a, b) < 8; }

  return { pageMode, enhance, enhanceCanvas, reprintOver, nearWhite, toCanvas };
})();
