/* Claude Pixel — détecteurs de défauts (A6-H, A5-10, F2) et contrôles chiffrés.
 * Chaque détecteur lit l'image exportée (calques normaux visibles) et rend
 *   { id, niveau: 'erreur'|'attention'|'conseil', titre, ref, pixels: [[x,y]...], msg }
 * Sans DOM : tourne aussi dans node. */
(function (G) {
'use strict';
const AP = G.AP;
const { lum, hex, compose, couleursUtilisees, budgetPourTaille } = AP;
const op = c => (c >>> 24) > 0;

function grille(px, w, h) {
  const at = (x, y) => (x < 0 || y < 0 || x >= w || y >= h) ? 0 : px[y * w + x];
  return at;
}

/* --- « L » : pixel doublé dans un trait (A5-6, règle 21) --- */
function coinsL(px, w, h) {
  const at = grille(px, w, h), out = [];
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
    const c = at(x, y); if (!op(c)) continue;
    const N = at(x, y - 1) === c, S = at(x, y + 1) === c, E = at(x + 1, y) === c, W = at(x - 1, y) === c;
    if (N + S + E + W !== 2) continue;
    let a = null;
    if (N && E) a = [[0, -1], [1, 0]]; else if (E && S) a = [[1, 0], [0, 1]];
    else if (S && W) a = [[0, 1], [-1, 0]]; else if (W && N) a = [[-1, 0], [0, -1]];
    if (!a) continue;
    const [[ax, ay], [bx, by]] = a;
    if (at(x + ax + bx, y + ay + by) === c) continue;            // bloc 2×2 : pas un trait
    // angle d'un rectangle : les deux bras continuent tout droit → voulu
    const brasA = at(x + 2 * ax, y + 2 * ay) === c, brasB = at(x + 2 * bx, y + 2 * by) === c;
    if (brasA && brasB) continue;
    // trait fin seulement : les pixels des bras n'ont pas d'épaisseur
    out.push([x, y]);
  }
  return out;
}

/* --- Alpha partiel : de l'AA vers le vide, qui fait un halo sur un autre fond (A6-F, règle 46) --- */
function alphaPartiel(px) {
  const out = [];
  for (let i = 0; i < px.length; i++) { const a = px[i] >>> 24; if (a > 0 && a < 255) out.push(i); }
  return out;
}

/* --- Jaggies : longueurs de segments irrégulières (A5-6, règle 22) --- */
function jaggies(px, w, h) {
  const at = grille(px, w, h), out = [];
  const passe = (horiz) => {
    // segments fins d'une couleur, dans une direction
    const runs = new Map(), liste = [];
    const L = horiz ? h : w, M = horiz ? w : h;
    const get = horiz ? (u, v) => at(u, v) : (u, v) => at(v, u);
    for (let v = 0; v < L; v++) {
      let u = 0;
      while (u < M) {
        const c = get(u, v);
        if (!op(c)) { u++; continue; }
        let u1 = u;
        while (u1 + 1 < M && get(u1 + 1, v) === c) u1++;
        let fin = true;
        for (let k = u; k <= u1; k++) if (get(k, v - 1) === c || get(k, v + 1) === c) { fin = false; break; }
        if (fin) { const r = { c, v, u0: u, u1, n: u1 - u + 1 }; runs.set(c + ':' + v + ':' + u, r); liste.push(r); }
        u = u1 + 1;
      }
    }
    for (const sens of [-1, 1]) {
      const suivant = r => runs.get(r.c + ':' + (r.v + sens) + ':' + (r.u1 + 1));
      const aPrec = new Set();
      for (const r of liste) { const s = suivant(r); if (s) aPrec.add(s); }
      for (const r of liste) {
        if (aPrec.has(r) || !suivant(r)) continue;
        const ch = [r]; let s = suivant(r);
        while (s && ch.length < 400) { ch.push(s); s = suivant(s); }
        if (ch.length < 4) continue;
        const n = ch.map(q => q.n);
        for (let i = 1; i < n.length - 1; i++) {
          const a = n[i - 1], b = n[i], c = n[i + 1];
          const extremum = (b > a && b > c) || (b < a && b < c);
          if (!extremum) continue;
          const periodique = (i >= 2 && n[i - 2] === b) || (i + 2 < n.length && n[i + 2] === b);
          if (periodique) continue;
          if (Math.abs(b - a) <= 0 && Math.abs(b - c) <= 0) continue;
          const q = ch[i];
          for (let k = q.u0; k <= q.u1; k++) out.push(horiz ? [k, q.v] : [q.v, k]);
        }
      }
    }
  };
  passe(true); passe(false);
  return out;
}

/* --- composantes connexes d'une couleur (4-voisins) --- */
function composantes(px, w, h) {
  const lab = new Int32Array(w * h).fill(-1), comps = [];
  for (let i = 0; i < w * h; i++) {
    if (lab[i] >= 0 || !op(px[i])) continue;
    const c = px[i], pile = [i], pts = []; lab[i] = comps.length;
    while (pile.length) {
      const j = pile.pop(); pts.push(j);
      const x = j % w, y = (j / w) | 0;
      for (const [dx, dy] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) {
        const X = x + dx, Y = y + dy; if (X < 0 || Y < 0 || X >= w || Y >= h) continue;
        const k = Y * w + X; if (lab[k] < 0 && px[k] === c) { lab[k] = comps.length; pile.push(k); }
      }
    }
    comps.push({ c, pts });
  }
  return { lab, comps };
}

/* --- Banding : un ton en bande fine qui longe deux autres tons (A6-H) --- */
function banding(px, w, h) {
  const { comps } = composantes(px, w, h), out = [];
  for (const k of comps) {
    if (k.pts.length < 5) continue;
    let x0 = w, x1 = 0, y0 = h, y1 = 0, interieur = 0;
    const vois = new Map(); let nv = 0;
    for (const j of k.pts) {
      const x = j % w, y = (j / w) | 0;
      x0 = Math.min(x0, x); x1 = Math.max(x1, x); y0 = Math.min(y0, y); y1 = Math.max(y1, y);
      let pareil = 0;
      for (const [dx, dy] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) {
        const X = x + dx, Y = y + dy;
        const v = (X < 0 || Y < 0 || X >= w || Y >= h) ? 0 : px[Y * w + X];
        if (v === k.c) { pareil++; continue; }
        vois.set(v, (vois.get(v) || 0) + 1); nv++;
      }
      if (pareil >= 3) interieur++;
    }
    if (x1 - x0 < 2 || y1 - y0 < 2) continue;            // la bande doit tourner avec la forme
    if (interieur > k.pts.length * 0.1) continue;          // pas une bande fine
    const tri = [...vois.entries()].sort((a, b) => b[1] - a[1]);
    if (tri.length < 2) continue;
    const [A, nA] = tri[0], [B, nB] = tri[1];
    if (!op(A) || !op(B) || nA < nv * 0.3 || nB < nv * 0.3) continue;
    const l = lum(k.c), la = lum(A), lb = lum(B);
    if (!((l > Math.min(la, lb)) && (l < Math.max(la, lb)))) continue;
    for (const j of k.pts) out.push([j % w, (j / w) | 0]);
  }
  return out;
}

/* --- Distance au bord de la silhouette (BFS) --- */
function distanceBord(px, w, h) {
  const d = new Int32Array(w * h).fill(-1), f = [];
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
    const i = y * w + x; if (!op(px[i])) continue;
    let bord = x === 0 || y === 0 || x === w - 1 || y === h - 1;
    if (!bord) for (const [dx, dy] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) if (!op(px[(y + dy) * w + x + dx])) { bord = true; break; }
    if (bord) { d[i] = 1; f.push(i); }
  }
  for (let q = 0; q < f.length; q++) {
    const i = f[q], x = i % w, y = (i / w) | 0;
    for (const [dx, dy] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) {
      const X = x + dx, Y = y + dy; if (X < 0 || Y < 0 || X >= w || Y >= h) continue;
      const k = Y * w + X; if (op(px[k]) && d[k] < 0) { d[k] = d[i] + 1; f.push(k); }
    }
  }
  return d;
}
function correl(a, b) {
  const n = a.length; if (n < 3) return 0;
  let ma = 0, mb = 0; for (let i = 0; i < n; i++) { ma += a[i]; mb += b[i]; } ma /= n; mb /= n;
  let s = 0, sa = 0, sb = 0;
  for (let i = 0; i < n; i++) { const x = a[i] - ma, y = b[i] - mb; s += x * y; sa += x * x; sb += y * y; }
  return (sa && sb) ? s / Math.sqrt(sa * sb) : 0;
}
/* --- Ombrage coussin / flash : la clarté suit le bord au lieu de la lumière (A5-8, règle 25) --- */
function coussin(px, w, h, lv) {
  const d = distanceBord(px, w, h), L = [], D = [], Dir = [], pts = [];
  const lx = lv ? lv[0] : -1, ly = lv ? lv[1] : -1;
  for (let i = 0; i < w * h; i++) {
    if (d[i] < 2) continue;                       // le contour n'entre pas dans le calcul
    const x = i % w, y = (i / w) | 0;
    L.push(lum(px[i])); D.push(d[i]); Dir.push(x * lx + y * ly); pts.push([x, y]);
  }
  if (pts.length < 24) return { pts: [], cd: 0, cl: 0 };
  const cd = correl(L, D), cl = correl(L, Dir);
  return { pts: (cd > 0.6 && cl < 0.3) ? pts : [], cd, cl };
}

/* --- Orphelins : un pixel seul au milieu d'une autre couleur (A5-10) --- */
function orphelins(px, w, h) {
  const at = grille(px, w, h), out = [];
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
    const c = at(x, y); if (!op(c)) continue;
    const v = at(x - 1, y - 1); if (v === c) continue;
    let ok = true;
    for (let dy = -1; dy <= 1 && ok; dy++) for (let dx = -1; dx <= 1; dx++) {
      if (!dx && !dy) continue; if (at(x + dx, y + dy) !== v) { ok = false; break; }
    }
    if (ok) out.push([x, y]);
  }
  return out;
}

/* --- Bruit : trop de pixels sans voisin de leur couleur --- */
function bruit(px, w, h) {
  const at = grille(px, w, h), out = []; let n = 0;
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
    const c = at(x, y); if (!op(c)) continue; n++;
    if (at(x + 1, y) !== c && at(x - 1, y) !== c && at(x, y + 1) !== c && at(x, y - 1) !== c) out.push([x, y]);
  }
  return { pts: (n >= 16 && out.length > n * 0.15) ? out : [], part: n ? out.length / n : 0 };
}

/* --- Damier : tramage AB/BA (A6-H « dithering décoratif », règle 31) --- */
function damier(px, w, h) {
  const at = grille(px, w, h), s = new Set();
  for (let y = 0; y < h - 1; y++) for (let x = 0; x < w - 1; x++) {
    const a = at(x, y), b = at(x + 1, y);
    if (a === b || !op(a) || !op(b)) continue;
    if (at(x, y + 1) === b && at(x + 1, y + 1) === a) { s.add(x + ',' + y); s.add((x + 1) + ',' + y); s.add(x + ',' + (y + 1)); s.add((x + 1) + ',' + (y + 1)); }
  }
  return s.size >= 8 ? [...s].map(k => k.split(',').map(Number)) : [];
}

/* --- Super pixels : tout est fait de blocs k×k (A6-H, A4b) --- */
function superpixels(px, w, h) {
  let n = 0; for (const c of px) if (op(c)) n++;
  if (n < 8) return 0;
  for (const k of [4, 3, 2]) {
    for (let oy = 0; oy < k; oy++) for (let ox = 0; ox < k; ox++) {
      let ok = true;
      for (let by = oy - k; by < h && ok; by += k) for (let bx = ox - k; bx < w && ok; bx += k) {
        let ref = null;
        for (let y = by; y < by + k && ok; y++) for (let x = bx; x < bx + k; x++) {
          const v = (x < 0 || y < 0 || x >= w || y >= h) ? null : px[y * w + x];
          if (v === null) continue;
          if (ref === null) ref = v; else if (v !== ref) { ok = false; break; }
        }
      }
      if (ok) return k;
    }
  }
  return 0;
}

/* --- Raccords de tuile : le bord droit doit continuer le bord gauche (F2-A) --- */
function raccords(px, w, h, tw, th) {
  const at = grille(px, w, h), out = [];
  const diff = (a, b) => a !== b ? 1 : 0;
  let interne = 0, ni = 0;
  for (let y = 0; y < h; y++) for (let x = 0; x < w - 1; x++) { interne += diff(at(x, y), at(x + 1, y)); ni++; }
  for (let y = 0; y < h - 1; y++) for (let x = 0; x < w; x++) { interne += diff(at(x, y), at(x, y + 1)); ni++; }
  const ref = ni ? interne / ni : 0;
  let nb = 0, mb = 0;
  for (let ty = 0; ty < h; ty += th) for (let tx = 0; tx < w; tx += tw) {
    for (let y = ty; y < Math.min(h, ty + th); y++) {
      const a = at(tx, y), b = at(Math.min(w, tx + tw) - 1, y); nb++;
      if (diff(a, b)) { mb++; out.push([tx, y], [Math.min(w, tx + tw) - 1, y]); }
    }
    for (let x = tx; x < Math.min(w, tx + tw); x++) {
      const a = at(x, ty), b = at(x, Math.min(h, ty + th) - 1); nb++;
      if (diff(a, b)) { mb++; out.push([x, ty], [x, Math.min(h, ty + th) - 1]); }
    }
  }
  const part = nb ? mb / nb : 0;
  return { pts: part > ref * 1.8 + 0.1 ? out : [], part, ref };
}

/* Tous les détecteurs. doc + image ; renvoie la liste des défauts trouvés. */
function detecte(doc, f = 0) {
  const { w, h } = doc, px = compose(doc, f, 'export'), res = [];
  const ajoute = (id, niveau, titre, ref, pixels, msg) => res.push({ id, niveau, titre, ref, pixels: pixels || [], msg });
  const couleurs = couleursUtilisees(px), nC = couleurs.size;
  let opaques = 0; for (const c of px) if (op(c)) opaques++;
  if (!opaques) return res;

  const L = coinsL(px, w, h);
  if (L.length) ajoute('L', 'erreur', 'Pixels doublés en « L »', 'A5-6 · règle 21', L,
    L.length + ' angle(s) en L dans le trait. Un trait de 1 px ne se touche qu\'en diagonale : supprime le pixel du coin.');
  const J = jaggies(px, w, h);
  if (J.length) ajoute('jaggies', 'attention', 'Jaggies (segments irréguliers)', 'A5-6 · règle 22', J,
    'Un segment casse la progression (ex. 3-1-2-1-3). Les longueurs doivent changer régulièrement (5-3-2-1-1) ou suivre un motif (2-1-2-1).');
  const O = orphelins(px, w, h);
  if (O.length) ajoute('orphelins', 'attention', 'Pixels orphelins', 'A5-10', O,
    O.length + ' pixel(s) seul(s) au milieu d\'une autre couleur. Garde-le seulement s\'il est voulu (éclat, rivet) et justifie-le ; sinon supprime-le ou groupe-le par 2-3.');
  const B = banding(px, w, h);
  if (B.length) ajoute('bandes', 'attention', 'Banding', 'A6-H', B,
    'Un ton forme une bande fine qui longe deux autres tons : les marches de la rampe se suivent en escalier. Varie la largeur des zones, casse l\'alignement.');
  const VO = AP.VOLUME, lumDoc = VO ? VO.lumiereDe(doc) : null, nomLum = VO ? VO.nomDirection(lumDoc.az) : 'haut gauche';
  const C = coussin(px, w, h, VO ? VO.vecteur(lumDoc) : null);
  if (C.pts.length) ajoute('coussin', 'erreur', 'Ombrage coussin / flash', 'A5-8 · règle 25', C.pts,
    'La clarté suit la distance au bord (r = ' + C.cd.toFixed(2) + ') et non la lumière ' + nomLum + ' (r = ' + C.cl.toFixed(2) + '). L\'ombre va du côté opposé à la source.');
  if (VO) {
    const M = VO.mesure(px, w, h, lumDoc);
    if (M.accord !== null && M.accord < 0.3) ajoute('lumiere', 'attention', 'L\'ombrage ne suit pas la lumière', '0-C · règle 50', M.fautifs,
      'Accord clarté / volume r = ' + M.accord.toFixed(2) + ' (il faut 0,30 au moins, 0,50 pour un rendu pro). Lumière ' + nomLum + ' : ouvre l\'onglet Lumière, affiche le guide et ' +
      'regarde où passe le terminateur. Les pixels marqués sont du mauvais côté : clairs dans l\'ombre ou sombres dans la lumière.');
    else if (M.ecart !== null && M.ecart < 0.05) ajoute('lumiere', 'attention', 'Lumière et ombre se confondent', '0-C · règle 51', M.fautifs,
      'Les deux familles (lumière, ombre) ne s\'écartent que de ' + M.ecart.toFixed(2) + ' en clarté. Groupe : toute la lumière au-dessus, toute l\'ombre au-dessous, avec un vrai saut au terminateur.');
  }
  const N = bruit(px, w, h);
  if (N.pts.length) ajoute('bruit', 'attention', 'Bruit', 'A6-H', N.pts,
    Math.round(N.part * 100) + ' % des pixels n\'ont aucun voisin de leur couleur. Regroupe la texture en amas de 2-3 (règle du tiers, A5-9).');
  const k = superpixels(px, w, h);
  const D = k ? [] : damier(px, w, h);
  if (D.length) ajoute('trame', Math.max(w, h) <= 32 ? 'attention' : 'conseil', 'Tramage en damier', 'A6-H · règle 31', D,
    'Trame AB/BA sur ' + D.length + ' px. Sous 32 px on ne trame pas ; plus grand, la trame sert une transition de matière, jamais le décor. Justifie-la si elle est voulue.');
  if (k) ajoute('superpixels', 'erreur', 'Super pixels', 'A6-H · A4b', [],
    'Toute l\'image est faite de blocs ' + k + '×' + k + ' : tu dessines en gros. Dessine à la taille finale (réduis la toile ÷' + k + ').');
  const bud = budgetPourTaille(w, h);
  if (nC > bud.total) ajoute('budget', 'attention', 'Trop de couleurs', 'A3', [],
    nC + ' couleurs pour un sprite de ' + Math.max(w, h) + ' px : la table A3 en permet ' + bud.total + '. Essaie « une couleur de moins » (A6-J).');
  const noir = AP.pack(0, 0, 0, 255);
  if (couleurs.has(noir)) {
    const pts = []; for (let i = 0; i < px.length; i++) if (px[i] === noir) pts.push([i % w, (i / w) | 0]);
    ajoute('noirPur', 'conseil', 'Noir pur', 'A5-7', pts, 'Le #000000 est mort : prends le ton le plus sombre de la rampe, teinté (violet, bleu nuit).');
  }
  for (const r of doc.rampes || []) {
    for (let i = 0; i + 1 < r.couleurs.length; i++) {
      try {
        const a = AP.parseHex(r.couleurs[i]), b = AP.parseHex(r.couleurs[i + 1]);
        if (Math.abs(lum(a) - lum(b)) < 0.06) {
          ajoute('rampesGris', 'attention', 'Rampe illisible en gris', 'A6-A · A6-J', [],
            'Rampe « ' + r.nom + ' » : ' + r.couleurs[i] + ' et ' + r.couleurs[i + 1] + ' ont presque la même valeur. En gris elles se confondent.');
          break;
        }
      } catch (e) { /* couleur invalide ignorée */ }
    }
  }
  const A = alphaPartiel(px);
  if (A.length) ajoute('alpha', 'attention', 'Pixels semi-transparents', 'A6-F · règle 46', A.map(i => [i % w, (i / w) | 0]),
    A.length + ' pixel(s) à demi transparents : c\'est de l\'AA vers le vide, qui fait un halo sur tout autre fond. Rends-les opaques ou efface-les ; l\'AA se fait à l\'intérieur du contour.');
  if (doc.tuile && doc.tuile.on) {
    const R = raccords(px, w, h, doc.tuile.tw, doc.tuile.th);
    if (R.pts.length) ajoute('raccords', 'erreur', 'Couture de tuile', 'F2-A', R.pts,
      Math.round(R.part * 100) + ' % des bords ne se raccordent pas (intérieur : ' + Math.round(R.ref * 100) + ' %). Regarde la grille 3×3 et corrige les bords.');
  }
  return res;
}

/* Mesures utiles à la méthode et aux portes. */
function mesures(doc, f = 0) {
  const px = compose(doc, f, 'export');
  const cols = couleursUtilisees(px);
  let n = 0; for (const c of px) if (op(c)) n++;
  return { couleurs: cols.size, opaques: n, palette: [...cols.keys()].map(c => hex(c)) };
}

Object.assign(AP, { detecte, mesures, DETECT: { coinsL, alphaPartiel, jaggies, banding, coussin, orphelins, bruit, damier, superpixels, raccords, composantes, distanceBord } });
if (typeof module !== 'undefined') module.exports = AP;
})(typeof window !== 'undefined' ? window : globalThis);
