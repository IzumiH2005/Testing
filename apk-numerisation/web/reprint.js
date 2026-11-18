/* Réimpression : la page photographiée est reconstruite comme si une imprimante couleur
   l'avait imprimée sur une feuille neuve, au même format.

   Trois étapes (trois « modules ») :
   1. ŒIL DU PAPIER : mesure la vraie couleur du papier (sans l'éclairage, les ombres, les taches)
      et donne son code (#RRGGBB) et son nom. La feuille neuve prend cette couleur.
   2. TRI : apprend les encres de la page (k-moyennes, apprentissage non supervisé sur la page elle-même),
      puis classe chaque point : papier, encre unie (texte, titre, aplat) ou zone d'image (illustration, photo).
      Les traces pâles (plis, grain, usure, poussière) ne sont pas des encres : elles sont jetées.
   3. IMPRIMANTE : comme une vraie imprimante, l'encre est un filtre posé sur le papier
      (synthèse soustractive : couleur finale = couleur du papier × transmission de l'encre).
      Les aplats sont imprimés en encre pure, les bords restent nets, les images sont imprimées en ton continu. */
const Reprint = (() => {
  const NAMES = [["blanc", 255, 255, 255], ["blanc cassé", 246, 243, 234], ["ivoire", 255, 250, 232], ["crème", 252, 242, 212],
    ["beige", 238, 224, 196], ["jaune pâle", 255, 249, 195], ["jaune", 255, 232, 125], ["pêche", 255, 224, 198],
    ["saumon clair", 255, 204, 184], ["rose clair", 255, 224, 230], ["rose", 252, 192, 208], ["lavande", 232, 226, 252],
    ["mauve clair", 228, 208, 238], ["bleu ciel", 208, 232, 252], ["bleu clair", 184, 212, 242], ["vert d'eau", 216, 242, 228],
    ["vert clair", 204, 236, 194], ["gris clair", 228, 228, 228], ["gris", 196, 196, 196], ["kraft", 218, 188, 148], ["orange clair", 255, 212, 155]];
  const hex = c => "#" + c.map(v => Math.max(0, Math.min(255, Math.round(v))).toString(16).padStart(2, "0")).join("").toUpperCase();
  function nameOf(c) { let best = NAMES[0], be = 1e9; for (const n of NAMES) { const e = (n[1] - c[0]) ** 2 + (n[2] - c[1]) ** 2 + (n[3] - c[2]) ** 2; if (e < be) { be = e; best = n; } } return best[0]; }
  function rng(seed) { return () => (seed = (seed * 1664525 + 1013904223) >>> 0) / 4294967296; }
  const poly = (c, X, Y) => c[0] + c[1] * X + c[2] * Y + c[3] * X * X + c[4] * X * Y + c[5] * Y * Y;

  /* 1. Œil du papier.
     Difficulté : une feuille blanche sous une lampe chaude paraît jaune, à l'ombre d'un ciel elle paraît bleue.
     Les éclairages ne teintent que sur l'axe chaud ↔ froid (orange ↔ bleu) ; une teinte hors de cet axe
     (rose, vert, lavande…) vient donc du papier. Sur l'axe, seule une teinte très marquée (jaune vif, kraft)
     est attribuée au papier. */
  function paperColor(light) {
    const WHITE = { rgb: [255, 255, 255], hex: "#FFFFFF", name: "blanc" };
    if (!light.co || light.paperFrac < 0.03) return WHITE;
    const s = [0, 0, 0]; let n = 0;
    for (let Y = -0.8; Y <= 0.81; Y += 0.2) for (let X = -0.8; X <= 0.81; X += 0.2) { for (let o = 0; o < 3; o++) s[o] += Math.max(8, poly(light.co[o], X, Y)); n++; }
    const l = s.map(v => Math.log(v / n));
    let a = l[0] - l[2], g = (2 * l[1] - l[0] - l[2]) / 2;            // a : chaud/froid, g : vert/magenta
    const off = Math.abs(g) > 0.06;                                    // teinte hors de l'axe des lampes : c'est le papier
    if (!off) { a = Math.sign(a) * Math.max(0, Math.abs(a) - 0.3); g = Math.sign(g) * Math.max(0, Math.abs(g) - 0.03); }
    const L = [a / 2 - g / 3, 2 * g / 3, -a / 2 - g / 3], m = Math.max(...L);
    const rgb = L.map(v => Math.round(255 * Math.exp(v - m)));          // l'exposition est retirée : seule la teinte compte
    if (Math.max(...rgb) - Math.min(...rgb) < 14) return WHITE;
    return { rgb, hex: hex(rgb), name: nameOf(rgb) };
  }

  function normalize(warped, light) { // papier -> 255 (on travaille « par rapport au papier »)
    const w = warped.width, h = warped.height;
    if (light.colorful > 0.07 && light.co) {
      const img = warped.getContext("2d").getImageData(0, 0, w, h), d = img.data, co = light.co;
      for (let y = 0; y < h; y++) { const Y = y / h * 2 - 1;
        for (let x = 0; x < w; x++) { const X = x / w * 2 - 1, i = (y * w + x) * 4;
          for (let o = 0; o < 3; o++) d[i + o] = d[i + o] / Math.max(30, poly(co[o], X, Y)) * 255; } }
      return img;
    }
    return flatten(warped, 1);
  }

  function kmeans(S, k, rand) {
    const n = S.length / 3, C = [];
    const i0 = Math.floor(rand() * n); C.push([S[i0 * 3], S[i0 * 3 + 1], S[i0 * 3 + 2]]);
    const dm = new Float32Array(n).fill(1e9);
    while (C.length < k) { const c = C[C.length - 1]; let tot = 0;
      for (let i = 0; i < n; i++) { const e = (S[i * 3] - c[0]) ** 2 + (S[i * 3 + 1] - c[1]) ** 2 + (S[i * 3 + 2] - c[2]) ** 2; if (e < dm[i]) dm[i] = e; tot += dm[i]; }
      let r = rand() * tot, j = 0; for (; j < n - 1; j++) { r -= dm[j]; if (r <= 0) break; } C.push([S[j * 3], S[j * 3 + 1], S[j * 3 + 2]]); }
    const cnt = new Float32Array(k);
    for (let it = 0; it < 12; it++) {
      const acc = new Float32Array(k * 3); cnt.fill(0);
      for (let i = 0; i < n; i++) { let b = 0, be = 1e18; for (let c = 0; c < k; c++) { const e = (S[i * 3] - C[c][0]) ** 2 + (S[i * 3 + 1] - C[c][1]) ** 2 + (S[i * 3 + 2] - C[c][2]) ** 2; if (e < be) { be = e; b = c; } }
        cnt[b]++; acc[b * 3] += S[i * 3]; acc[b * 3 + 1] += S[i * 3 + 1]; acc[b * 3 + 2] += S[i * 3 + 2]; }
      for (let c = 0; c < k; c++) if (cnt[c]) C[c] = [acc[c * 3] / cnt[c], acc[c * 3 + 1] / cnt[c], acc[c * 3 + 2] / cnt[c]];
    }
    return C.map((c, i) => ({ c, n: cnt[i] / n }));
  }

  // composantes connexes (4-voisinage) d'un masque ; appelle fn(liste de pixels)
  function components(mask, w, h, fn) {
    const seen = new Uint8Array(w * h), st = new Int32Array(w * h);
    for (let s = 0; s < w * h; s++) { if (!mask[s] || seen[s]) continue; let top = 0, len = 0; const comp = []; st[top++] = s; seen[s] = 1;
      while (top) { const c = st[--top]; comp.push(c); len++; const x = c % w;
        if (x > 0 && mask[c - 1] && !seen[c - 1]) { seen[c - 1] = 1; st[top++] = c - 1; }
        if (x < w - 1 && mask[c + 1] && !seen[c + 1]) { seen[c + 1] = 1; st[top++] = c + 1; }
        if (c >= w && mask[c - w] && !seen[c - w]) { seen[c - w] = 1; st[top++] = c - w; }
        if (c < w * h - w && mask[c + w] && !seen[c + w]) { seen[c + w] = 1; st[top++] = c + w; } }
      fn(comp); }
  }

  function run(warped, light, opts = {}) {
    const w = warped.width, h = warped.height, N = w * h;
    const found = paperColor(light), paper = opts.paper === "white" ? { rgb: [255, 255, 255], hex: "#FFFFFF", name: "blanc" } : found;
    const img = normalize(warped, light), d = img.data;

    /* 2. Tri */
    const D = new Float32Array(N); // distance au papier
    for (let i = 0; i < N; i++) D[i] = Math.max(255 - d[i * 4], 255 - d[i * 4 + 1], 255 - d[i * 4 + 2], 0);
    const pap = []; for (let i = 0; i < N; i += 7) if (D[i] < 80) pap.push(D[i]); pap.sort((a, b) => a - b);
    const med = pap[pap.length >> 1] || 0, mad = pap.map(v => Math.abs(v - med)).sort((a, b) => a - b)[pap.length >> 1] || 4;
    const t0 = Math.max(22, Math.min(60, med + 5 * 1.4826 * mad)); // en dessous : c'est du papier (grain, pli léger, salissure)
    const rand = rng(7), samp = [], step = Math.max(1, Math.floor(N / 60000));
    for (let i = 0; i < N; i += step) if (D[i] > t0 + 25) samp.push(d[i * 4], d[i * 4 + 1], d[i * 4 + 2]);
    let inks = samp.length > 300 ? kmeans(samp, Math.min(10, Math.floor(samp.length / 90)), rand) : [{ c: [20, 20, 20], n: 1 }];
    inks = inks.filter(o => o.n > 0.004).sort((a, b) => b.n - a.n);
    const pal = [[255, 255, 255]];
    for (const o of inks) if (pal.every(p => Math.hypot(p[0] - o.c[0], p[1] - o.c[1], p[2] - o.c[2]) > 26)) pal.push(o.c.map(v => Math.max(0, Math.min(255, v))));
    const K = pal.length, R = new Float32Array(N * 3).fill(255), res = new Float32Array(N), ink = new Uint8Array(N), pale = new Uint8Array(N), solid = new Uint8Array(N), dist = new Float32Array(K), idx = [0, 0, 0, 0];
    for (let i = 0; i < N; i++) {
      if (D[i] < t0) continue;
      const p = i * 4, r = d[p], g = d[p + 1], b = d[p + 2];
      for (let c = 0; c < K; c++) dist[c] = (r - pal[c][0]) ** 2 + (g - pal[c][1]) ** 2 + (b - pal[c][2]) ** 2;
      idx[0] = 0; let m = 1; const used = new Uint8Array(K); used[0] = 1;
      for (let t = 0; t < 3; t++) { let bi = -1, be = 1e18; for (let c = 1; c < K; c++) if (!used[c] && dist[c] < be) { be = dist[c]; bi = c; } if (bi < 0) break; used[bi] = 1; idx[m++] = bi; }
      let best = 1e18, A = 0, B = 0, T = 0;
      for (let u = 0; u < m; u++) { const cu = idx[u]; if (dist[cu] < best) { best = dist[cu]; A = cu; B = cu; T = 0; } }
      for (let u = 0; u < m; u++) for (let v = u + 1; v < m; v++) { // mélange de deux encres (bord de lettre, encre sur encre)
        const P = pal[idx[u]], Q = pal[idx[v]], ex = Q[0] - P[0], ey = Q[1] - P[1], ez = Q[2] - P[2], L = ex * ex + ey * ey + ez * ez;
        const t = ((r - P[0]) * ex + (g - P[1]) * ey + (b - P[2]) * ez) / L; if (t <= 0 || t >= 1) continue;
        const e = (r - P[0] - t * ex) ** 2 + (g - P[1] - t * ey) ** 2 + (b - P[2] - t * ez) ** 2;
        if (e < best) { best = e; A = idx[u]; B = idx[v]; T = t; } }
      if (A === 0 && B !== 0) { pale[i] = T < 0.45 ? 1 : 0; T = Math.min(1, Math.max(0, (T - 0.12) / 0.7)); } // bord d'encre ou voile
      else if (T < 0.1) T = 0; else if (T > 0.9) T = 1;    // encre franche
      const P = pal[A], Q = pal[B];
      R[i * 3] = P[0] + (Q[0] - P[0]) * T; R[i * 3 + 1] = P[1] + (Q[1] - P[1]) * T; R[i * 3 + 2] = P[2] + (Q[2] - P[2]) * T;
      res[i] = Math.sqrt(best); ink[i] = (A !== 0 || T > 0) ? 1 : 0;
      if (!pale[i] && ink[i]) solid[i] = 1;
    }
    // voiles pâles loin de toute encre franche (pli, frottement, grain) : jetés ; près d'une lettre, c'est son bord lissé : gardé
    const near = morph(solid, w, h, 2, true);
    for (let i = 0; i < N; i++) if (pale[i] && !near[i]) { R[i * 3] = R[i * 3 + 1] = R[i * 3 + 2] = 255; ink[i] = 0; }
    // zones d'image : là où deux encres pures n'expliquent pas ce qu'on voit (dégradés, photo)
    const BS = Math.max(12, Math.round(Math.max(w, h) / 90)), gw = Math.ceil(w / BS), gh = Math.ceil(h / BS);
    let ph = new Uint8Array(gw * gh), drop = new Uint8Array(gw * gh);
    const sr = new Float32Array(gw * gh), si = new Float32Array(gw * gh), sn = new Float32Array(gw * gh);
    for (let i = 0; i < N; i++) { const g = (((i / w) | 0) / BS | 0) * gw + ((i % w) / BS | 0); sn[g]++; if (D[i] >= t0) { si[g]++; sr[g] += res[i]; } }
    for (let g = 0; g < gw * gh; g++) ph[g] = si[g] > 0.35 * sn[g] && sr[g] / Math.max(1, si[g]) > 13 ? 1 : 0;
    ph = morph(morph(ph, gw, gh, 1, true), gw, gh, 1, false);
    components(ph, gw, gh, comp => {
      if (comp.length < 6) { for (const c of comp) ph[c] = 0; return; }                 // texte épais, logo : pas une image
      let edge = false; for (const c of comp) { const x = c % gw, y = (c / gw) | 0; if (!x || !y || x === gw - 1 || y === gh - 1) { edge = true; break; } }
      if (edge && comp.length < 0.03 * gw * gh) for (const c of comp) { ph[c] = 0; drop[c] = 1; } // collée au bord et petite : doigt, coin abîmé, support
    });
    let pm = null, photoArea = 0;
    if (ph.some(v => v)) {
      pm = new Float32Array(N); for (let i = 0; i < N; i++) pm[i] = ph[(((i / w) | 0) / BS | 0) * gw + ((i % w) / BS | 0)];
      pm = boxBlur(boxBlur(pm, w, h, BS >> 1), w, h, BS >> 1);
      for (let i = 0; i < N; i++) { const t = Math.min(1, pm[i] * 1.5); pm[i] = t; if (t <= 0.01) continue; photoArea++;
        const keep = D[i] >= t0 * 0.6; // dans l'image, on garde les vrais tons ; le papier autour reste papier
        for (let c = 0; c < 3; c++) { const src = keep ? Math.min(255, d[i * 4 + c]) : 255; R[i * 3 + c] += (src - R[i * 3 + c]) * t; } }
    }
    // poussière (minuscules points isolés) et usure des bords (traces collées au bord, sans rien vers l'intérieur)
    const minA = Math.max(4, Math.round((Math.max(w, h) / 1000) ** 2 * 3)), mx = Math.round(w * 0.035), my = Math.round(h * 0.035);
    const dropW = morph(drop, gw, gh, 1, true);
    const erase = comp => { for (const c of comp) { R[c * 3] = R[c * 3 + 1] = R[c * 3 + 2] = 255; if (pm) pm[c] = 0; } };
    components(ink, w, h, comp => {
      if (comp.length < minA) { if (!(pm && pm[comp[0]] > 0.01)) erase(comp); return; }
      let x0 = w, y0 = h, x1 = 0, y1 = 0; for (const c of comp) { const x = c % w, y = (c / w) | 0; if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y; }
      const inBand = (x1 < mx || x0 > w - 1 - mx || y1 < my || y0 > h - 1 - my), touches = x0 === 0 || y0 === 0 || x1 === w - 1 || y1 === h - 1;
      if (touches && inBand) erase(comp);                                 // trace collée au bord : usure, bout de support
      else if (touches) erase(comp.filter(c => dropW[(((c / w) | 0) / BS | 0) * gw + ((c % w) / BS | 0)])); // dans la zone d'un doigt / coin abîmé
    });

    /* 3. Imprimante : encre = filtre posé sur le papier neuf */
    const out = new ImageData(w, h), od = out.data, pr = paper.rgb;
    for (let i = 0; i < N; i++) { const p = i * 4;
      od[p] = pr[0] * R[i * 3] / 255; od[p + 1] = pr[1] * R[i * 3 + 1] / 255; od[p + 2] = pr[2] * R[i * 3 + 2] / 255; od[p + 3] = 255; }
    const cv = newCanvas(w, h); cv.getContext("2d").putImageData(out, 0, 0);
    cv._info = { paper, found, inks: pal.slice(1).map(c => hex(c.map((v, o) => pr[o] * v / 255))), photo: photoArea / N, t0 };
    return cv;
  }
  return { run, paperColor };
})();
