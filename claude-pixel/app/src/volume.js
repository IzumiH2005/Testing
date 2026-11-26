/* Claude Pixel — lumière et volume (sans DOM).
 * Ce que fait un peintre avant d'ombrer : il place la lumière, imagine la forme en volume
 * et sait où passent la lumière, le demi-ton, le terminateur, l'ombre propre, la lumière
 * réfléchie, l'éclat et l'ombre portée (méthode, partie 0-C).
 * Ce module ne pose aucun pixel. Il calcule un GUIDE, affiché par-dessus la toile comme la
 * pelure d'oignon, et MESURE si l'ombrage dessiné suit la lumière. Le dessin reste à la main. */
(function (G) {
'use strict';
const AP = G.AP;
const op = c => (c >>> 24) > 0;

/* ---------- La lumière ----------
 * az : d'où vient la lumière, en degrés sur l'écran (0 = droite, 90 = haut, 180 = gauche).
 * el : hauteur au-dessus du plan de l'image (0 = rasante, 90 = face au spectateur).
 * Repère : x vers la droite, y vers le BAS (comme les pixels), z vers le spectateur. */
const DIRECTIONS = {
  'haut gauche': 135, 'haut': 90, 'haut droite': 45, 'gauche': 180, 'droite': 0,
  'bas gauche': 225, 'bas': 270, 'bas droite': 315
};
const HAUTEURS = { rasante: 20, moyenne: 40, haute: 65 };
const FORMES = ['gonfle', 'sphere', 'cylindre'];
const LUMIERE_DEFAUT = { az: 135, el: 40, forme: 'gonfle', posee: false };

function vecteur(l) {
  const a = (l.az ?? 135) * Math.PI / 180, e = (l.el ?? 40) * Math.PI / 180;
  return [Math.cos(e) * Math.cos(a), -Math.cos(e) * Math.sin(a), Math.sin(e)];
}
function nomDirection(az) {
  let best = 'haut gauche', d = 1e9;
  for (const k in DIRECTIONS) { const x = Math.abs(((az - DIRECTIONS[k] + 540) % 360) - 180); if (x < d) { d = x; best = k; } }
  return best;
}
const norme = v => { const n = Math.hypot(v[0], v[1], v[2]) || 1; return [v[0] / n, v[1] / n, v[2] / n]; };
const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];

/* ---------- Le masque : ce qui est opaque ---------- */
function masque(px) { const m = new Uint8Array(px.length); for (let i = 0; i < px.length; i++) m[i] = op(px[i]) ? 1 : 0; return m; }

/* Distance euclidienne (approchée, chanfrein 3-4) au vide le plus proche, en pixels. */
function distance(m, w, h) {
  const INF = 1e9, d = new Float32Array(w * h);
  for (let i = 0; i < d.length; i++) d[i] = m[i] ? INF : 0;
  const at = (x, y) => (x < 0 || y < 0 || x >= w || y >= h) ? 0 : d[y * w + x];
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
    const i = y * w + x; if (!d[i]) continue;
    d[i] = Math.min(d[i], at(x - 1, y) + 3, at(x, y - 1) + 3, at(x - 1, y - 1) + 4, at(x + 1, y - 1) + 4);
  }
  for (let y = h - 1; y >= 0; y--) for (let x = w - 1; x >= 0; x--) {
    const i = y * w + x; if (!d[i]) continue;
    d[i] = Math.min(d[i], at(x + 1, y) + 3, at(x, y + 1) + 3, at(x + 1, y + 1) + 4, at(x - 1, y + 1) + 4);
  }
  for (let i = 0; i < d.length; i++) d[i] /= 3;
  return d;
}
function boite(m, w, h) {
  let x0 = w, y0 = h, x1 = -1, y1 = -1;
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) if (m[y * w + x]) { if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y; }
  return x1 < 0 ? null : { x0, y0, x1, y1, cx: (x0 + x1 + 1) / 2, cy: (y0 + y1 + 1) / 2, rx: (x1 - x0 + 1) / 2, ry: (y1 - y0 + 1) / 2 };
}

/* ---------- Les normales : la forme imaginée en volume ----------
 * gonfle   : la silhouette gonflée comme un ballon (marche pour toute forme ronde) ;
 * sphere   : un ellipsoïde inscrit dans la boîte de la silhouette ;
 * cylindre : un cylindre vertical (bouteille, tronc, colonne). */
function normales(m, w, h, forme = 'gonfle') {
  const N = new Float32Array(w * h * 3), b = boite(m, w, h);
  if (!b) return N;
  if (forme === 'sphere' || forme === 'cylindre') {
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
      const i = y * w + x; if (!m[i]) continue;
      let nx = (x + 0.5 - b.cx) / b.rx, ny = forme === 'sphere' ? (y + 0.5 - b.cy) / b.ry : 0;
      const r = Math.hypot(nx, ny); if (r > 0.98) { nx *= 0.98 / r; ny *= 0.98 / r; }
      const n = norme([nx, ny, Math.sqrt(Math.max(0, 1 - nx * nx - ny * ny))]);
      N[i * 3] = n[0]; N[i * 3 + 1] = n[1]; N[i * 3 + 2] = n[2];
    }
    return N;
  }
  // gonfle : hauteur en profil de cercle, h = sqrt(R² − (R − d)²), puis lissage et pente.
  const d = distance(m, w, h); let R = 0; for (const v of d) if (v > R) R = v;
  R = Math.max(R, 1);
  let H = new Float32Array(w * h);
  for (let i = 0; i < H.length; i++) if (m[i]) { const t = Math.min(d[i], R) - 0.5; H[i] = Math.sqrt(Math.max(0, R * R - (R - t) * (R - t))); }
  for (let k = 0; k < 2; k++) {
    const O = new Float32Array(w * h);
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
      const i = y * w + x; if (!m[i]) continue;
      let s = 0, n = 0;
      for (let dy = -1; dy <= 1; dy++) for (let dx = -1; dx <= 1; dx++) {
        const X = x + dx, Y = y + dy; if (X < 0 || Y < 0 || X >= w || Y >= h) { n++; continue; }
        s += H[Y * w + X]; n++;
      }
      O[i] = s / n;
    }
    H = O;
  }
  const at = (x, y) => (x < 0 || y < 0 || x >= w || y >= h) ? 0 : H[y * w + x];
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
    const i = y * w + x; if (!m[i]) continue;
    const gx = (at(x + 1, y) - at(x - 1, y)) / 2, gy = (at(x, y + 1) - at(x, y - 1)) / 2;
    const n = norme([-gx, -gy, 0.9]);
    N[i * 3] = n[0]; N[i * 3 + 1] = n[1]; N[i * 3 + 2] = n[2];
  }
  return N;
}

/* ---------- Le guide : la famille et la zone de chaque pixel ----------
 * Les zones de la lumière sur une forme (Proko, Robertson, Gurney ; méthode 0-C). */
const ZONES = [
  { id: 0, nom: 'vide' },
  { id: 1, nom: 'éclat', famille: 'lumière', coul: '#fff6c8' },
  { id: 2, nom: 'lumière', famille: 'lumière', coul: '#ffcf5a' },
  { id: 3, nom: 'demi-ton', famille: 'lumière', coul: '#e8915a' },
  { id: 4, nom: 'ombre propre', famille: 'ombre', coul: '#4a2a7a' },
  { id: 5, nom: 'ombre', famille: 'ombre', coul: '#6a5aa8' },
  { id: 6, nom: 'lumière réfléchie', famille: 'ombre', coul: '#3fa0a0' },
  { id: 7, nom: 'ombre portée', famille: 'ombre', coul: '#2a2238' }
];
function guide(px, w, h, lum = LUMIERE_DEFAUT) {
  const m = masque(px), N = normales(m, w, h, lum.forme || 'gonfle'), L = vecteur(lum);
  const V = [0, 0, 1], H = norme([L[0] + V[0], L[1] + V[1], L[2] + V[2]]);
  // lumière de rebond : elle remonte du sol, à l'opposé de la source
  const B = norme([-L[0] * 0.6, 1, 0.25]);
  const zone = new Uint8Array(w * h), ndl = new Float32Array(w * h);
  for (let i = 0; i < w * h; i++) {
    if (!m[i]) continue;
    const n = [N[i * 3], N[i * 3 + 1], N[i * 3 + 2]], k = dot(n, L); ndl[i] = k;
    if (k > 0.12) zone[i] = Math.pow(Math.max(0, dot(n, H)), 60) > 0.55 ? 1 : k > 0.5 ? 2 : 3;
    else if (k > -0.18) zone[i] = 4;
    else zone[i] = dot(n, B) > 0.5 ? 6 : 5;
  }
  // l'éclat : au moins un pixel, le plus face à la demi-direction
  let best = -1, bv = -2;
  for (let i = 0; i < w * h; i++) if (m[i]) { const v = dot([N[i * 3], N[i * 3 + 1], N[i * 3 + 2]], H); if (v > bv) { bv = v; best = i; } }
  if (best >= 0 && ![...zone].includes(1)) zone[best] = 1;
  // ombre portée : une ellipse au sol, poussée à l'opposé de la lumière
  const b = boite(m, w, h);
  if (b) {
    const rx = Math.max(2, b.rx * 0.85), ry = Math.max(1, Math.round(b.rx * 0.18)), cy = b.y1 + 0.5;
    const cx = b.cx - L[0] * b.rx * 0.45 / Math.max(0.3, L[2] + 0.3);
    for (let y = Math.floor(cy - ry); y <= Math.ceil(cy + ry); y++) for (let x = Math.floor(cx - rx); x <= Math.ceil(cx + rx); x++) {
      if (x < 0 || y < 0 || x >= w || y >= h) continue;
      const i = y * w + x; if (m[i]) continue;
      if (((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - cy) / ry) ** 2 <= 1) zone[i] = 7;
    }
  }
  // terminateur : les arêtes entre un pixel de la famille lumière et un de la famille ombre
  const term = [];
  const fam = z => z >= 1 && z <= 3 ? 1 : z >= 4 && z <= 6 ? 2 : 0;
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
    const a = fam(zone[y * w + x]); if (!a) continue;
    if (x + 1 < w) { const b2 = fam(zone[y * w + x + 1]); if (b2 && b2 !== a) term.push([x + 1, y, x + 1, y + 1]); }
    if (y + 1 < h) { const b2 = fam(zone[(y + 1) * w + x]); if (b2 && b2 !== a) term.push([x, y + 1, x + 1, y + 1]); }
  }
  return { zone, ndl, masque: m, term, lumiere: L };
}

/* ---------- La mesure : le dessin suit-il la lumière ? ----------
 * Les pixels sont groupés par matière (teinte voisine) : une couleur locale différente
 * n'est pas une erreur d'ombrage. Dans chaque matière, la clarté doit monter avec n·l.
 *   accord   : corrélation clarté / n·l, moyenne pondérée sur les matières ombrées ;
 *   ecart    : clarté moyenne de la famille lumière − famille ombre (deux familles nettes) ;
 *   inverses : part des pixels côté lumière plus sombres que la moyenne côté ombre ;
 *   etendue  : écart de clarté (5e à 95e centile) sur tout l'objet.
 * rampes (facultatif) : les rampes du document, pour reconnaître une matière à teinte décalée. */
/* Avec les rampes du document, une couleur rangée dans une rampe appartient à cette rampe :
 * une rampe à teinte décalée (ombre vers le violet, lumière vers l'orangé) reste UNE matière.
 * Sans rampe, on groupe par teinte. */
function matiere(c, rampes) {
  if (rampes && rampes.length) {
    const hx = AP.hex(c).slice(0, 7).toLowerCase();
    for (let k = 0; k < rampes.length; k++) if ((rampes[k].couleurs || []).some(x => String(x).toLowerCase() === hx)) return 'rampe' + k;
  }
  const [r, g, b] = AP.unpack(c), [hh, s, v] = AP.rgb2hsv(r, g, b);
  if (s < 0.18 || v < 0.12) return 'neutre';
  return 'h' + Math.round(hh / 40) % 9;
}
function mesure(px, w, h, lum = LUMIERE_DEFAUT, rampes = null) {
  const g = guide(px, w, h, lum), d = distance(g.masque, w, h);
  const groupes = {}; const tous = [];
  for (let i = 0; i < w * h; i++) {
    if (!g.masque[i] || d[i] < 1.9) continue;   // le contour n'entre pas dans la mesure
    const l = AP.lum(px[i]); tous.push(l);
    const k = matiere(px[i], rampes); (groupes[k] = groupes[k] || { L: [], N: [], I: [] });
    groupes[k].L.push(l); groupes[k].N.push(g.ndl[i]); groupes[k].I.push(i);
  }
  const res = { n: tous.length, accord: null, ecart: null, inverses: null, etendue: 0, matieres: 0, fautifs: [] };
  if (tous.length < 12) return res;
  const tri = tous.slice().sort((a, b) => a - b);
  res.etendue = tri[Math.floor(tri.length * 0.95)] - tri[Math.floor(tri.length * 0.05)];
  let sa = 0, pa = 0, se = 0, pe = 0, inv = 0, ninv = 0;
  for (const k in groupes) {
    const { L, N, I } = groupes[k]; if (L.length < 10) continue;
    let mn = 1, mx = 0; for (const v of L) { if (v < mn) mn = v; if (v > mx) mx = v; }
    if (mx - mn < 0.04) continue;               // aplat : rien à mesurer
    const r = correl(L, N); sa += r * L.length; pa += L.length; res.matieres++;
    const lu = [], om = [];
    for (let j = 0; j < L.length; j++) (N[j] > 0.12 ? lu : N[j] < -0.18 ? om : []).push(L[j]);
    if (lu.length >= 4 && om.length >= 4) {
      const ml = lu.reduce((a, b) => a + b, 0) / lu.length, mo = om.reduce((a, b) => a + b, 0) / om.length;
      se += (ml - mo) * L.length; pe += L.length;
      for (const v of lu) { if (v < mo) inv++; ninv++; }
      // fautifs : un pixel bien tourné vers la lumière plus sombre que l'ombre moyenne, ou l'inverse
      for (let j = 0; j < L.length; j++) if ((N[j] > 0.35 && L[j] < mo) || (N[j] < -0.35 && L[j] > ml)) res.fautifs.push([I[j] % w, (I[j] / w) | 0]);
    }
  }
  if (pa) res.accord = sa / pa;
  if (pe) res.ecart = se / pe;
  if (ninv) res.inverses = inv / ninv;
  return res;
}
function correl(a, b) {
  const n = a.length; if (n < 3) return 0;
  let ma = 0, mb = 0; for (let i = 0; i < n; i++) { ma += a[i]; mb += b[i]; } ma /= n; mb /= n;
  let s = 0, sa = 0, sb = 0;
  for (let i = 0; i < n; i++) { const x = a[i] - ma, y = b[i] - mb; s += x * y; sa += x * x; sb += y * y; }
  return (sa && sb) ? s / Math.sqrt(sa * sb) : 0;
}
/* La lumière d'un document (tolère les anciens fichiers et la fiche d'intention). */
function lumiereDe(doc) {
  if (doc.lumiere && doc.lumiere.posee) return doc.lumiere;
  const f = doc.meta && doc.meta.fiche && doc.meta.fiche.lumiere;
  const az = f && DIRECTIONS[String(f).split(' (')[0]];
  return Object.assign({}, LUMIERE_DEFAUT, doc.lumiere || {}, az !== undefined ? { az } : {});
}
/* Notan : deux valeurs. Seuil = moyenne des clartés de l'objet. */
function notan(px) {
  let s = 0, n = 0; for (const c of px) if (op(c)) { s += AP.lum(c); n++; }
  const t = n ? s / n : 0.5, o = new Uint32Array(px.length);
  for (let i = 0; i < px.length; i++) if (op(px[i])) o[i] = AP.lum(px[i]) >= t ? AP.pack(225, 225, 225) : AP.pack(40, 40, 48);
  return o;
}

AP.VOLUME = { DIRECTIONS, HAUTEURS, FORMES, ZONES, LUMIERE_DEFAUT, vecteur, nomDirection, masque, distance, normales, guide, mesure, lumiereDe, notan, matiere };
if (typeof module !== 'undefined') module.exports = AP;
})(typeof window !== 'undefined' ? window : globalThis);
