/* Claude Pixel — noyau (sans DOM).
 * Tout changement d'état passe par input(ev) ou act(nom, args), et tout est journalisé.
 * Ce fichier tourne aussi sans navigateur (rejeu, vérification d'intégrité, tests node). */
(function (G) {
'use strict';
const AP = G.AP = G.AP || {};
AP.FORMATS = ['claude-pixel', 'atelier-pixel']; // l'ancien nom reste lisible

/* ---------- Couleurs ---------- */
const pack = (r, g, b, a = 255) => ((r & 255) | ((g & 255) << 8) | ((b & 255) << 16) | ((a & 255) << 24)) >>> 0;
const unpack = c => [c & 255, (c >>> 8) & 255, (c >>> 16) & 255, (c >>> 24) & 255];
const h2 = n => n.toString(16).padStart(2, '0');
function hex(c, alpha) {
  const [r, g, b, a] = unpack(c);
  return '#' + h2(r) + h2(g) + h2(b) + ((alpha || a !== 255) ? h2(a) : '');
}
function parseHex(s) {
  s = String(s).trim().replace(/^#/, '');
  if (/^[0-9a-f]{3}$/i.test(s)) s = s.split('').map(x => x + x).join('');
  if (!/^[0-9a-f]{6}([0-9a-f]{2})?$/i.test(s)) throw new Error('Couleur invalide : ' + s);
  const n = parseInt(s.slice(0, 6), 16);
  const a = s.length === 8 ? parseInt(s.slice(6), 16) : 255;
  return pack((n >> 16) & 255, (n >> 8) & 255, n & 255, a);
}
function rgb2hsv(r, g, b) {
  r /= 255; g /= 255; b /= 255;
  const mx = Math.max(r, g, b), mn = Math.min(r, g, b), d = mx - mn;
  let h = 0;
  if (d) {
    if (mx === r) h = ((g - b) / d) % 6; else if (mx === g) h = (b - r) / d + 2; else h = (r - g) / d + 4;
    h *= 60; if (h < 0) h += 360;
  }
  return [h, mx ? d / mx : 0, mx];
}
function hsv2rgb(h, s, v) {
  h = ((h % 360) + 360) % 360;
  const c = v * s, x = c * (1 - Math.abs((h / 60) % 2 - 1)), m = v - c;
  let r, g, b;
  if (h < 60) [r, g, b] = [c, x, 0]; else if (h < 120) [r, g, b] = [x, c, 0];
  else if (h < 180) [r, g, b] = [0, c, x]; else if (h < 240) [r, g, b] = [0, x, c];
  else if (h < 300) [r, g, b] = [x, 0, c]; else [r, g, b] = [c, 0, x];
  return [Math.round((r + m) * 255), Math.round((g + m) * 255), Math.round((b + m) * 255)];
}
function rgb2hsl(r, g, b) {
  r /= 255; g /= 255; b /= 255;
  const mx = Math.max(r, g, b), mn = Math.min(r, g, b), l = (mx + mn) / 2, d = mx - mn;
  let h = 0, s = 0;
  if (d) {
    s = d / (1 - Math.abs(2 * l - 1));
    if (mx === r) h = ((g - b) / d) % 6; else if (mx === g) h = (b - r) / d + 2; else h = (r - g) / d + 4;
    h *= 60; if (h < 0) h += 360;
  }
  return [h, s, l];
}
function hsl2rgb(h, s, l) {
  const c = (1 - Math.abs(2 * l - 1)) * s;
  const v = l + c / 2, sv = v ? 2 * (1 - l / v) : 0;
  return hsv2rgb(h, Math.max(0, Math.min(1, sv)), Math.max(0, Math.min(1, v)));
}
/* Clarté perçue (L d'OKLab), 0..1 : sert à la vue grise et aux détecteurs. */
function lum(c) {
  const [r, g, b] = unpack(c).map(v => { v /= 255; return v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); });
  const l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b;
  const m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b;
  const s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b;
  return 0.2104542553 * Math.cbrt(l) + 0.7936177850 * Math.cbrt(m) - 0.0040720468 * Math.cbrt(s);
}
Object.assign(AP, { pack, unpack, hex, parseHex, rgb2hsv, hsv2rgb, rgb2hsl, hsl2rgb, lum });

/* Rampe A6-A : ton moyen au milieu ; vers l'ombre la teinte tourne vers le froid, la
 * saturation monte un peu ; vers la lumière la teinte tourne vers le chaud, la saturation
 * baisse ; marches plus courtes près du blanc ; jamais 0 % ni 100 %. */
function genereRampe(hexMoyen, n = 5, decal = 15) {
  const [r, g, b] = unpack(parseHex(hexMoyen));
  const [h, s, v] = rgb2hsv(r, g, b);
  const mid = Math.floor((n - 1) / 2), out = [];
  const vers = (h0, cible, deg) => {
    let d = ((cible - h0 + 540) % 360) - 180;
    return h0 + Math.sign(d) * Math.min(Math.abs(d), deg);
  };
  for (let i = 0; i < n; i++) {
    const k = i - mid;
    let hh = h, ss = s, vv = v;
    if (k < 0) {
      hh = vers(h, 250, decal * -k);
      ss = Math.min(0.92, s + 0.06 * -k);
      vv = v * Math.pow(0.74, -k);
    } else if (k > 0) {
      hh = vers(h, 55, decal * k);
      ss = Math.max(0.06, s - 0.13 * k);
      vv = v + (0.97 - v) * (1 - Math.pow(0.55, k));
    }
    vv = Math.max(0.06, Math.min(0.97, vv));
    const [rr, gg, bb] = hsv2rgb(hh, ss, vv);
    out.push(hex(pack(rr, gg, bb)));
  }
  return out;
}
AP.genereRampe = genereRampe;

/* ---------- Base64 ---------- */
const B64 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/';
function b64enc(u8) {
  let s = '';
  for (let i = 0; i < u8.length; i += 3) {
    const a = u8[i], b = u8[i + 1], c = u8[i + 2];
    const n = (a << 16) | ((b || 0) << 8) | (c || 0);
    s += B64[(n >> 18) & 63] + B64[(n >> 12) & 63] + (i + 1 < u8.length ? B64[(n >> 6) & 63] : '=') + (i + 2 < u8.length ? B64[n & 63] : '=');
  }
  return s;
}
function b64dec(s) {
  s = s.replace(/[^A-Za-z0-9+/]/g, '');
  const out = new Uint8Array(Math.floor(s.length * 3 / 4));
  let o = 0;
  for (let i = 0; i < s.length; i += 4) {
    const n = (B64.indexOf(s[i]) << 18) | (B64.indexOf(s[i + 1]) << 12) | ((B64.indexOf(s[i + 2]) & 63) << 6) | (B64.indexOf(s[i + 3]) & 63);
    out[o++] = (n >> 16) & 255;
    if (s[i + 2] !== undefined && o < out.length) out[o++] = (n >> 8) & 255;
    if (s[i + 3] !== undefined && o < out.length) out[o++] = n & 255;
  }
  return out.slice(0, o);
}
AP.b64enc = b64enc; AP.b64dec = b64dec;

/* ---------- Géométrie ---------- */
function ligne(x0, y0, x1, y1, f) {
  const dx = Math.abs(x1 - x0), dy = -Math.abs(y1 - y0), sx = x0 < x1 ? 1 : -1, sy = y0 < y1 ? 1 : -1;
  let e = dx + dy;
  for (;;) {
    f(x0, y0);
    if (x0 === x1 && y0 === y1) break;
    const e2 = 2 * e;
    if (e2 >= dy) { e += dy; x0 += sx; }
    if (e2 <= dx) { e += dx; y0 += sy; }
  }
}
/* Pentes propres (A8) : 0, 90°, 1:1, 2:1, 1:2, 3:1, 1:3. Renvoie le bout aimanté et le pas. */
const PENTES = [[1, 0], [0, 1], [1, 1], [2, 1], [1, 2], [3, 1], [1, 3]];
function aimantePente(x0, y0, x1, y1) {
  const dx = x1 - x0, dy = y1 - y0;
  if (!dx && !dy) return { x: x1, y: y1, pas: null };
  let best = null;
  for (const [a, b] of PENTES) {
    for (const sx of a ? [1, -1] : [1]) for (const sy of b ? [1, -1] : [1]) {
      const vx = a * sx, vy = b * sy, n2 = vx * vx + vy * vy;
      const k = Math.max(1, Math.round((dx * vx + dy * vy) / n2));
      const ex = vx * k, ey = vy * k;
      const d = (ex - dx) ** 2 + (ey - dy) ** 2;
      if (!best || d < best.d) best = { d, vx, vy, k };
    }
  }
  return best;
}
/* Ligne propre : k marches identiques (ex. 2-2-2 pour 2:1). */
function lignePropre(x0, y0, p, f) {
  const { vx, vy, k } = p;
  const ax = Math.abs(vx), ay = Math.abs(vy), sx = Math.sign(vx), sy = Math.sign(vy);
  let x = x0, y = y0;
  if (ax >= ay) {
    for (let i = 0; i < k; i++) {
      for (let j = 0; j < ax; j++) { f(x, y); x += sx; }
      if (ay) { y += sy; }
      if (!ay && i === k - 1) f(x, y);
    }
    if (ax === ay) f(x, y);
  } else {
    for (let i = 0; i < k; i++) {
      for (let j = 0; j < ay; j++) { f(x, y); y += sy; }
      x += sx;
    }
  }
}
function remplisEllipse(x0, y0, x1, y1) {
  const xa = Math.min(x0, x1), xb = Math.max(x0, x1), ya = Math.min(y0, y1), yb = Math.max(y0, y1);
  const cx = (xa + xb + 1) / 2, cy = (ya + yb + 1) / 2, rx = (xb - xa + 1) / 2, ry = (yb - ya + 1) / 2;
  const set = new Set();
  for (let y = ya; y <= yb; y++) {
    const dy = (y + 0.5 - cy) / ry;
    const dx = rx * Math.sqrt(Math.max(0, 1 - dy * dy));
    let a = Math.round(cx - dx), b = Math.round(cx + dx) - 1;
    if (b < a) { a = Math.floor(cx - 0.5); b = Math.ceil(cx - 0.5); }
    for (let x = a; x <= b; x++) set.add(x + ',' + y);
  }
  return { set, xa, xb, ya, yb };
}
function bordEllipse(x0, y0, x1, y1) {
  const { set } = remplisEllipse(x0, y0, x1, y1);
  const bord = new Set();
  for (const k of set) {
    const [x, y] = k.split(',').map(Number);
    if (!set.has((x + 1) + ',' + y) || !set.has((x - 1) + ',' + y) || !set.has(x + ',' + (y + 1)) || !set.has(x + ',' + (y - 1))) bord.add(k);
  }
  return nettoieL(bord);
}
/* Retire les coins en « L » d'un tracé d'1 px (A6-H, doubles). */
function nettoieL(set) {
  const has = (x, y) => set.has(x + ',' + y);
  let change = true;
  while (change) {
    change = false;
    for (const k of Array.from(set)) {
      const [x, y] = k.split(',').map(Number);
      const n = has(x, y - 1), s = has(x, y + 1), e = has(x + 1, y), w = has(x - 1, y);
      const ortho = n + s + e + w;
      if (ortho !== 2 || (n && s) || (e && w)) continue;
      // les deux voisins sont en diagonale l'un de l'autre : le coin est en trop si la diagonale opposée est vide
      const dx = e ? 1 : -1, dy = s ? 1 : -1;
      if (!has(x - dx, y - dy) && !has(x + dx, y + dy)) {
        const autres = has(x - dx, y) || has(x, y - dy);
        if (!autres) { set.delete(k); change = true; }
      }
    }
  }
  return set;
}
AP.ligne = ligne; AP.aimantePente = aimantePente; AP.lignePropre = lignePropre; AP.nettoieL = nettoieL;
AP.remplisEllipse = remplisEllipse; AP.bordEllipse = bordEllipse;

/* ---------- Trames (A7) ---------- */
const BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]];
const TRAMES = {
  aucune: () => true,
  t25: (x, y) => (x % 2 === 0) && ((y % 2 === 0) ? (x % 4 === 0) : (x % 4 === 2)),
  t50: (x, y) => ((x + y) & 1) === 0,
  t75: (x, y) => !((x % 2 === 1) && ((y % 2 === 0) ? (x % 4 === 1) : (x % 4 === 3))),
  lignes: (x, y) => (y & 1) === 0,
  colonnes: (x, y) => (x & 1) === 0
};
AP.BAYER = BAYER; AP.TRAMES = TRAMES;

/* ---------- Palettes de départ (palettes libres d'usage) ---------- */
AP.PALETTES = {
  'Méthode (O violet)': ['#2a1a2e', '#4a2f4f', '#7a4a5f', '#b8727a', '#e8b896', '#fbe9d0', '#3b3f6b', '#5a6fae', '#8fb2df', '#2f5a3c', '#5f9a4c', '#b8d86a', '#8a3a2a', '#d0603a', '#f2b33d', '#ffffff'],
  'Sweetie 16': ['#1a1c2c', '#5d275d', '#b13e53', '#ef7d57', '#ffcd75', '#a7f070', '#38b764', '#257179', '#29366f', '#3b5dc9', '#41a6f6', '#73eff7', '#f4f4f4', '#94b0c2', '#566c86', '#333c57'],
  'PICO-8': ['#000000', '#1d2b53', '#7e2553', '#008751', '#ab5236', '#5f574f', '#c2c3c7', '#fff1e8', '#ff004d', '#ffa300', '#ffec27', '#00e436', '#29adff', '#83769c', '#ff77a8', '#ffccaa'],
  'Gris 8': ['#141414', '#2e2e2e', '#4a4a4a', '#6b6b6b', '#8f8f8f', '#b5b5b5', '#d9d9d9', '#f5f5f5'],
  'GB 4': ['#0f380f', '#306230', '#8bac0f', '#9bbc0f']
};

/* ---------- Document ---------- */
function nouveauDoc(o = {}) {
  const w = Math.max(1, Math.min(512, o.w | 0 || 32)), h = Math.max(1, Math.min(512, o.h | 0 || 32));
  const d = {
    v: 1, w, h, nom: o.nom || 'sans titre', type: o.type || 'objet',
    palette: (o.palette || AP.PALETTES['Méthode (O violet)']).slice(),
    rampes: [],
    calques: [], images: [{ ms: 100, role: '', change: '', principe: '', validee: false }],
    cels: {}, celData: {}, etiquettes: [], next: 1,
    meta: { fiche: {}, etape: 0, coches: {}, justifs: {}, planche: {}, reglesLues: false, valideEtapes: [], methode: 27, carnet: [], zones: { taille: 16, faites: {} } },
    lumiere: { az: 135, el: 40, forme: 'gonfle', posee: false },
    tuile: { on: false, tw: 16, th: 16 },
    carte: { cols: 20, rows: 12, terrain: [], tuiles: [] }
  };
  ajouteCalque(d, 'Calque 1', 'normal');
  return d;
}
function ajouteCalque(d, nom, type = 'normal', pos) {
  const id = 'L' + d.next++;
  const c = { id, nom, visible: true, opacite: 100, verrou: false, type, px: 1, teinte: null };
  if (pos === undefined) d.calques.push(c); else d.calques.splice(pos, 0, c);
  d.cels[id] = d.images.map(() => null);
  return c;
}
function nouveauCel(d, data) {
  const id = 'c' + d.next++;
  d.celData[id] = data || new Uint32Array(d.w * d.h);
  return id;
}
function copieDoc(d) {
  const o = JSON.parse(JSON.stringify(Object.assign({}, d, { celData: {} })));
  for (const k in d.celData) o.celData[k] = d.celData[k].slice();
  return o;
}
function serialiseDoc(d) {
  const o = JSON.parse(JSON.stringify(Object.assign({}, d, { celData: {} })));
  for (const k in d.celData) o.celData[k] = b64enc(new Uint8Array(d.celData[k].buffer, d.celData[k].byteOffset, d.celData[k].byteLength));
  return o;
}
function deserialiseDoc(o) {
  const d = JSON.parse(JSON.stringify(Object.assign({}, o, { celData: {} })));
  for (const k in o.celData) {
    const u8 = b64dec(o.celData[k]);
    const buf = new Uint8Array(d.w * d.h * 4); buf.set(u8.subarray(0, buf.length));
    d.celData[k] = new Uint32Array(buf.buffer);
  }
  // tolérance : champs ajoutés après coup
  d.meta = Object.assign({ fiche: {}, etape: 0, coches: {}, justifs: {}, planche: {}, reglesLues: false, valideEtapes: [] }, d.meta || {});
  d.tuile = d.tuile || { on: false, tw: 16, th: 16 };
  d.carte = d.carte || { cols: 20, rows: 12, terrain: [], tuiles: [] };
  d.rampes = d.rampes || []; d.etiquettes = d.etiquettes || [];
  return d;
}
/* Mélange normal d'un pixel src (avec opacité 0..1) sur dst. */
function melange(dst, src, op) {
  const sa = ((src >>> 24) & 255) / 255 * op;
  if (sa <= 0) return dst;
  const da = ((dst >>> 24) & 255) / 255;
  const oa = sa + da * (1 - sa);
  if (oa <= 0) return 0;
  const f = (s, t) => Math.round(((s * sa) + (t * da * (1 - sa))) / oa);
  const [sr, sg, sb] = unpack(src), [dr, dg, db] = unpack(dst);
  return pack(f(sr, dr), f(sg, dg), f(sb, db), Math.round(oa * 255));
}
/* Composition d'une image. filtre : 'export' (calques normaux visibles), 'visible' (tout ce qui est visible). */
function compose(d, f, filtre = 'export', sauf) {
  const out = new Uint32Array(d.w * d.h);
  for (const c of d.calques) {
    if (!c.visible || c === sauf) continue;
    if (filtre === 'export' && c.type !== 'normal') continue;
    const id = d.cels[c.id][f];
    if (!id) continue;
    const src = d.celData[id], op = c.opacite / 100;
    for (let i = 0; i < out.length; i++) {
      const s = src[i];
      if (!(s >>> 24)) continue;
      out[i] = (op >= 1 && (s >>> 24) === 255) ? s : melange(out[i], s, op);
    }
  }
  return out;
}
function couleursUtilisees(px) {
  const m = new Map();
  for (const c of px) if (c >>> 24) m.set(c, (m.get(c) || 0) + 1);
  return m;
}
function budgetPourTaille(w, h) {
  const t = Math.max(w, h);
  if (t <= 16) return { tons: '2–3', total: 8, aa: 'aucun', idees: 1 };
  if (t <= 32) return { tons: '3–4', total: 16, aa: 'rare, à l\'intérieur', idees: 2 };
  if (t <= 64) return { tons: '4–5', total: 24, aa: 'grandes courbes', idees: 4 };
  return { tons: '5+', total: Infinity, aa: 'oui, à la main', idees: Infinity };
}
Object.assign(AP, { nouveauDoc, copieDoc, serialiseDoc, deserialiseDoc, compose, melange, couleursUtilisees, budgetPourTaille, ajouteCalque });

/* ---------- RotSprite (Scale2x ×3, rotation au plus proche, réduction) ---------- */
function scale2x(src, w, h) {
  const o = new Uint32Array(w * h * 4), W = w * 2;
  const at = (x, y) => src[Math.max(0, Math.min(h - 1, y)) * w + Math.max(0, Math.min(w - 1, x))];
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
    const P = at(x, y), A = at(x, y - 1), B = at(x + 1, y), C = at(x - 1, y), D = at(x, y + 1);
    let e0 = P, e1 = P, e2 = P, e3 = P;
    if (C === A && C !== D && A !== B) e0 = A;
    if (A === B && A !== C && B !== D) e1 = B;
    if (D === C && D !== B && C !== A) e2 = C;
    if (B === D && B !== A && D !== C) e3 = D;
    o[(y * 2) * W + x * 2] = e0; o[(y * 2) * W + x * 2 + 1] = e1;
    o[(y * 2 + 1) * W + x * 2] = e2; o[(y * 2 + 1) * W + x * 2 + 1] = e3;
  }
  return o;
}
function rotsprite(src, w, h, deg) {
  let s = src, sw = w, sh = h;
  for (let i = 0; i < 3; i++) { s = scale2x(s, sw, sh); sw *= 2; sh *= 2; }
  const a = -deg * Math.PI / 180, ca = Math.cos(a), sa = Math.sin(a);
  const out = new Uint32Array(w * h), cx = w / 2, cy = h / 2;
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
    const dx = x + 0.5 - cx, dy = y + 0.5 - cy;
    const ux = (dx * ca - dy * sa + cx) * 8, uy = (dx * sa + dy * ca + cy) * 8;
    const ix = Math.floor(ux), iy = Math.floor(uy);
    if (ix >= 0 && iy >= 0 && ix < sw && iy < sh) out[y * w + x] = s[iy * sw + ix];
  }
  return out;
}
AP.rotsprite = rotsprite;

/* ---------- Autotile blob 47 par quarts (gabarit 3×3 + 2×2 coins intérieurs) ---------- */
function quartAutotile(n, e, s, w, ne, se, sw, nw, q) {
  // q : 0 = HG, 1 = HD, 2 = BG, 3 = BD. Renvoie [tx, ty] dans le gabarit (colonnes 0..4).
  const V = [[n, w, nw], [n, e, ne], [s, w, sw], [s, e, se]][q];
  const [a, b, c] = V; // a = vertical, b = horizontal, c = diagonale
  const ext = [[0, 0], [2, 0], [0, 2], [2, 2]][q];
  const vert = [[1, 0], [1, 0], [1, 2], [1, 2]][q];   // pas de voisin vertical : bord haut / bas
  const hor = [[0, 1], [2, 1], [0, 1], [2, 1]][q];    // pas de voisin horizontal : bord gauche / droit
  const inter = [[4, 1], [3, 1], [4, 0], [3, 0]][q];  // coin intérieur (bloc 2×2 au trou central, colonnes 3–4)
  if (!a && !b) return ext;
  if (!a) return vert;
  if (!b) return hor;
  if (!c) return inter;
  return [1, 1];
}
AP.quartAutotile = quartAutotile;

/* ---------- Atelier ---------- */
const OUTILS = ['crayon', 'gomme', 'ligne', 'rect', 'ellipse', 'seau', 'pipette', 'selrect', 'lasso', 'baguette', 'deplace', 'ombrage', 'remplace', 'degrade'];
const OPTIONS = {
  taille: v => Math.max(1, Math.min(16, v | 0)),
  forme: v => v === 'rond' ? 'rond' : 'carre',
  pp: v => !!v, trame: v => (v in TRAMES || v === 'bayer') ? v : 'aucune', bayer: v => Math.max(0, Math.min(16, v | 0)),
  rempli: v => !!v, symX: v => !!v, symY: v => !!v, axeX2: v => v | 0, axeY2: v => v | 0,
  verrouAlpha: v => !!v, tolerance: v => Math.max(0, Math.min(255, v | 0)), contigu: v => !!v,
  rampe: v => v | 0, tousCalques: v => !!v
};
AP.OUTILS = OUTILS;

class Atelier {
  constructor(o = {}) {
    this.mode = o.mode || 'humain';
    this.enregistre = o.enregistre !== false;
    this.horloge = o.horloge || (() => Date.now());
    this.t0 = this.horloge();
    this.decalT = 0;
    this.journal = [];
    this.ecoutes = new Set();
    this.hist = []; this.futur = [];
    this.trait = null;
    this.messages = [];
    this.s = this._etatDefaut();
    this.doc = null;
    if (!o.vide) this.act('doc.nouveau', o.doc || { w: 32, h: 32 });
  }
  _etatDefaut() {
    return {
      outil: 'crayon', c1: parseHex('#2a1a2e'), c2: 0, taille: 1, forme: 'carre', pp: true,
      trame: 'aucune', bayer: 8, rempli: false, symX: false, symY: false, axeX2: 32, axeY2: 32,
      verrouAlpha: false, tolerance: 0, contigu: true, rampe: -1, tousCalques: false,
      calque: 0, image: 0, selection: null, pinceau: null
    };
  }
  ecoute(f) { this.ecoutes.add(f); return () => this.ecoutes.delete(f); }
  _emet(quoi, info) { for (const f of this.ecoutes) try { f(quoi, info); } catch (e) { console.error(e); } }
  _note(ev) {
    if (!this.enregistre) return;
    ev.t = this.decalT + (this.horloge() - this.t0);
    this.journal.push(ev);
  }
  dit(msg, niveau = 'info') {
    this.messages.push({ msg, niveau, t: this.horloge() });
    if (this.messages.length > 50) this.messages.shift();
    this._emet('message', { msg, niveau });
  }
  refuse(msg) { this.dit(msg, 'refus'); const e = new Error(msg); e.refus = true; throw e; }

  /* --- accès --- */
  get calque() { return this.doc.calques[this.s.calque]; }
  celId(l = this.s.calque, f = this.s.image) { const c = this.doc.calques[l]; return c ? this.doc.cels[c.id][f] : null; }
  cel(l, f) { const id = this.celId(l, f); return id ? this.doc.celData[id] : null; }
  pixel(x, y, filtre = 'visible') {
    if (x < 0 || y < 0 || x >= this.doc.w || y >= this.doc.h) return 0;
    return compose(this.doc, this.s.image, filtre)[y * this.doc.w + x];
  }
  dans(x, y) { return x >= 0 && y >= 0 && x < this.doc.w && y < this.doc.h; }

  /* --- entrée pointeur --- */
  input(ev) {
    ev = { k: 'i', type: ev.type, x: Math.floor(ev.x), y: Math.floor(ev.y), b: ev.b | 0, m: ev.m || 0 };
    // m : bits 1 = Maj, 2 = Alt, 4 = Ctrl
    try {
      if (ev.type === 'down') this._down(ev);
      else if (ev.type === 'move') { if (!this.trait) return; this._move(ev); }
      else if (ev.type === 'up') { if (!this.trait) return; this._move(ev); this._up(ev); }
      else if (ev.type === 'cancel') { if (!this.trait) return; this._annuleTrait(); }
      else return;
    } catch (e) {
      if (e.refus) { this._note({ k: 'i', type: ev.type, x: ev.x, y: ev.y, b: ev.b, m: ev.m, refus: e.message }); return { refus: e.message }; }
      throw e;
    }
    this._note(ev);
    this._emet(ev.type === 'move' ? 'trait' : 'pixels', ev);
    return { ok: true };
  }
  _verifieDessin(outil) {
    const lecture = outil === 'pipette' || outil === 'selrect' || outil === 'lasso' || outil === 'baguette';
    if (lecture) return;
    const c = this.calque;
    if (!c) this.refuse('Aucun calque.');
    if (c.verrou) this.refuse('Le calque « ' + c.nom + ' » est verrouillé.');
    if (!c.visible) this.refuse('Le calque « ' + c.nom + ' » est caché : on ne dessine pas à l\'aveugle.');
    if (this.mode === 'claude') {
      const m = this.doc.meta;
      if (!m.reglesLues) this.refuse('Relis les 42 règles impératives avant de dessiner (onglet Méthode).');
      if (AP.ficheIncomplete && AP.ficheIncomplete(this.doc)) this.refuse('Remplis la fiche d\'intention avant le premier pixel (B0 / C0 / F0 / E0).');
      if (c.type === 'reference') this.refuse('Le calque de référence ne se dessine pas.');
    }
  }
  _down(ev) {
    if (this.trait) this._annuleTrait();
    const outil = (ev.m & 2) && (this.s.outil === 'crayon' || this.s.outil === 'seau') ? 'pipette' : this.s.outil;
    this._verifieDessin(outil);
    const t = this.trait = { outil, b: ev.b, m: ev.m, x0: ev.x, y0: ev.y, x: ev.x, y: ev.y, pts: [], vu: null, cree: null };
    if (outil === 'pipette') { this._pipette(ev); return; }
    if (outil === 'selrect' || outil === 'lasso' || outil === 'baguette') { this._selDown(ev); return; }
    // cel à écrire
    let id = this.celId();
    if (!id) {
      id = nouveauCel(this.doc);
      this.doc.cels[this.calque.id][this.s.image] = id;
      t.cree = { lid: this.calque.id, f: this.s.image, id };
    }
    t.id = id; t.data = this.doc.celData[id]; t.avant = t.data.slice();
    t.vu = new Uint8Array(this.doc.w * this.doc.h);
    if (outil === 'deplace') this._depDown(ev);
    else if (outil === 'seau') this._seau(ev);
    else if (outil === 'remplace') this._remplaceClic(ev);
    else if ((outil === 'crayon' || outil === 'gomme' || outil === 'ombrage') && (ev.m & 1) && this.dernierPoint) {
      // Maj + clic : trait droit depuis le dernier point (geste Aseprite)
      t.x = this.dernierPoint.x; t.y = this.dernierPoint.y; t.x0 = t.x; t.y0 = t.y;
      this._move(ev, false);
    }
    else this._move(ev, true);
  }
  _move(ev, premier) {
    const t = this.trait; if (!t) return;
    const x = ev.x, y = ev.y;
    switch (t.outil) {
      case 'crayon': case 'gomme': case 'ombrage': {
        if (premier) { this._point(x, y); }
        else if (x !== t.x || y !== t.y) {
          let px = t.x, py = t.y, first = true;
          ligne(t.x, t.y, x, y, (a, b) => { if (first) { first = false; return; } this._point(a, b); px = a; py = b; });
        }
        break;
      }
      case 'ligne': case 'rect': case 'ellipse': case 'degrade':
        t.data.set(t.avant); t.vu.fill(0);
        this._forme(t, x, y, ev.m);
        break;
      case 'pipette': this._pipette(ev); break;
      case 'selrect': case 'lasso': this._selMove(ev); break;
      case 'deplace': this._depMove(ev); break;
    }
    t.x = x; t.y = y; t.m = ev.m;
  }
  _couleurTrait() {
    const t = this.trait;
    if (t.outil === 'gomme') return 0;
    return t.b === 2 ? this.s.c2 : this.s.c1;
  }
  _point(x, y) {
    const t = this.trait;
    const pp = this.s.pp && this.s.taille === 1 && (t.outil === 'crayon' || t.outil === 'gomme');
    t.pts.push([x, y]);
    this._tampon(x, y);
    if (pp && t.pts.length >= 3) {
      const n = t.pts.length, a = t.pts[n - 3], b = t.pts[n - 2], c = t.pts[n - 1];
      const diag = Math.abs(a[0] - c[0]) === 1 && Math.abs(a[1] - c[1]) === 1;
      const adj = (p, q) => Math.abs(p[0] - q[0]) + Math.abs(p[1] - q[1]) === 1;
      if (diag && adj(a, b) && adj(b, c)) {
        // coin en L : on rend au pixel du milieu sa valeur d'avant le trait
        const dejaAvant = t.pts.slice(0, n - 2).some(p => p[0] === b[0] && p[1] === b[1]);
        if (!dejaAvant) this._restaure(b[0], b[1]);
        t.pts.splice(n - 2, 1);
      }
    }
  }
  _miroirs(x, y) {
    const out = [[x, y]];
    if (this.s.symX) out.push([this.s.axeX2 - 1 - x, y]);
    if (this.s.symY) for (const p of out.slice()) out.push([p[0], this.s.axeY2 - 1 - p[1]]);
    return out;
  }
  _restaure(x, y) {
    const t = this.trait, w = this.doc.w;
    for (const [mx, my] of this._miroirs(x, y)) {
      if (!this.dans(mx, my)) continue;
      const i = my * w + mx; t.data[i] = t.avant[i]; t.vu[i] = 0;
    }
  }
  _tampon(x, y) {
    const P = this.s.pinceau, t = this.trait;
    if (P && t && t.outil === 'crayon') {
      // pinceau personnalisé (pris dans une sélection) : chaque pixel opaque est posé avec sa couleur
      const ox = Math.floor(P.w / 2), oy = Math.floor(P.h / 2);
      for (const [cx, cy] of this._miroirs(x, y))
        for (let j = 0; j < P.h; j++) for (let i = 0; i < P.w; i++) {
          const c = P.px[j * P.w + i]; if (!(c >>> 24)) continue;
          this._ecrit(cx - ox + i, cy - oy + j, c);
        }
      return;
    }
    const n = this.s.taille, o = Math.floor((n - 1) / 2);
    for (const [cx, cy] of this._miroirs(x, y)) {
      for (let j = 0; j < n; j++) for (let i = 0; i < n; i++) {
        if (this.s.forme === 'rond' && n > 2) {
          const dx = i - (n - 1) / 2, dy = j - (n - 1) / 2;
          if (dx * dx + dy * dy > (n / 2) * (n / 2)) continue;
        }
        this._ecrit(cx - o + i, cy - o + j);
      }
    }
  }
  _masque(x, y) {
    if (!this.dans(x, y)) return false;
    const sel = this.s.selection;
    if (sel && !sel[y * this.doc.w + x]) return false;
    const tr = this.s.trame;
    if (tr === 'bayer') { if (!(BAYER[y & 3][x & 3] < this.s.bayer)) return false; }
    else if (tr !== 'aucune' && !TRAMES[tr](x, y)) return false;
    return true;
  }
  _ecrit(x, y, couleur) {
    const t = this.trait;
    if (!this._masque(x, y)) return;
    const i = y * this.doc.w + x;
    if (this.s.verrouAlpha && !(t.avant[i] >>> 24)) return;
    if (t.outil === 'ombrage') {
      if (t.vu[i]) return;
      const v = this._ombre(t.avant[i], t.b === 2 ? -1 : 1);
      if (v === null) return;
      t.data[i] = v; t.vu[i] = 1; return;
    }
    const c = couleur === undefined ? this._couleurTrait() : couleur;
    t.data[i] = (this.s.verrouAlpha && c >>> 24) ? c : c;
    t.vu[i] = 1;
  }
  /* Encre d'ombrage : avance d'une marche dans la rampe qui contient la couleur. */
  _ombre(c, sens) {
    if (!(c >>> 24)) return null;
    const rampes = this.s.rampe >= 0 && this.doc.rampes[this.s.rampe] ? [this.doc.rampes[this.s.rampe]] : this.doc.rampes;
    for (const r of rampes) {
      const vals = r.couleurs.map(parseHex);
      const k = vals.indexOf(c);
      if (k < 0) continue;
      const n = Math.max(0, Math.min(vals.length - 1, k + sens));
      return vals[n];
    }
    return null;
  }
  _forme(t, x, y, m) {
    const maj = m & 1;
    const plot = (a, b) => this._ecrit(a, b);
    if (t.outil === 'ligne') {
      if (maj) { const p = aimantePente(t.x0, t.y0, x, y); if (p.vx !== undefined) lignePropre(t.x0, t.y0, p, (a, b) => this._tampon(a, b)); else this._tampon(x, y); }
      else ligne(t.x0, t.y0, x, y, (a, b) => this._tampon(a, b));
      return;
    }
    let x1 = x, y1 = y;
    if (maj) { const d = Math.max(Math.abs(x - t.x0), Math.abs(y - t.y0)); x1 = t.x0 + Math.sign(x - t.x0 || 1) * d; y1 = t.y0 + Math.sign(y - t.y0 || 1) * d; }
    if (t.outil === 'rect') {
      const xa = Math.min(t.x0, x1), xb = Math.max(t.x0, x1), ya = Math.min(t.y0, y1), yb = Math.max(t.y0, y1);
      for (let j = ya; j <= yb; j++) for (let i = xa; i <= xb; i++)
        if (this.s.rempli || i === xa || i === xb || j === ya || j === yb) this._tamponFin(i, j);
      return;
    }
    if (t.outil === 'ellipse') {
      const set = this.s.rempli ? remplisEllipse(t.x0, t.y0, x1, y1).set : bordEllipse(t.x0, t.y0, x1, y1);
      for (const k of set) { const [a, b] = k.split(',').map(Number); this._tamponFin(a, b); }
      return;
    }
    if (t.outil === 'degrade') this._degrade(t, x, y);
  }
  _tamponFin(x, y) { for (const [a, b] of this._miroirs(x, y)) this._ecrit(a, b); }
  _region(x, y, src) {
    const w = this.doc.w, h = this.doc.h, out = new Uint8Array(w * h);
    if (!this.dans(x, y)) return out;
    const c0 = src[y * w + x], tol = this.s.tolerance;
    const proche = c => {
      if (c === c0) return true;
      if (!tol) return false;
      const a = unpack(c), b = unpack(c0);
      return Math.max(Math.abs(a[0] - b[0]), Math.abs(a[1] - b[1]), Math.abs(a[2] - b[2]), Math.abs(a[3] - b[3])) <= tol;
    };
    if (!this.s.contigu) { for (let i = 0; i < out.length; i++) if (proche(src[i])) out[i] = 1; return out; }
    const pile = [y * w + x]; out[y * w + x] = 1;
    while (pile.length) {
      const i = pile.pop(), px = i % w, py = (i / w) | 0;
      for (const [nx, ny] of [[px + 1, py], [px - 1, py], [px, py + 1], [px, py - 1]]) {
        if (nx < 0 || ny < 0 || nx >= w || ny >= h) continue;
        const j = ny * w + nx;
        if (out[j] || !proche(src[j])) continue;
        out[j] = 1; pile.push(j);
      }
    }
    return out;
  }
  _seau(ev) {
    const t = this.trait;
    const src = this.s.tousCalques ? compose(this.doc, this.s.image, 'visible') : t.avant;
    const reg = this._region(ev.x, ev.y, src);
    for (let i = 0; i < reg.length; i++) if (reg[i]) this._ecrit(i % this.doc.w, (i / this.doc.w) | 0);
  }
  _remplaceClic(ev) {
    const t = this.trait;
    if (!this.dans(ev.x, ev.y)) return;
    const de = t.avant[ev.y * this.doc.w + ev.x];
    const vers = this._couleurTrait();
    // Fusion silencieuse : si la couleur d'arrivée est déjà dans le calque, les deux tons se confondent pour de bon.
    if (vers !== de && t.avant.some(c => c === vers)) this.dit('Fusion : ' + hex(de) + ' rejoint ' + hex(vers) + ', déjà présente. Les deux tons ne font plus qu\'un ; un remplacement suivant de ' + hex(vers) + ' changera les deux.', 'alerte');
    for (let i = 0; i < t.data.length; i++) if (t.avant[i] === de) this._ecrit(i % this.doc.w, (i / this.doc.w) | 0, vers);
  }
  _degrade(t, x, y) {
    const w = this.doc.w;
    let reg = this.s.selection;
    if (!reg) { const s0 = this.s.contigu; reg = this._region(t.x0, t.y0, t.avant); this.s.contigu = s0; }
    const dx = x - t.x0, dy = y - t.y0, L2 = dx * dx + dy * dy || 1;
    for (let i = 0; i < reg.length; i++) {
      if (!reg[i]) continue;
      const px = i % w, py = (i / w) | 0;
      if (this.s.verrouAlpha && !(t.avant[i] >>> 24)) continue;
      let k = ((px - t.x0) * dx + (py - t.y0) * dy) / L2;
      k = Math.max(0, Math.min(1, k));
      const seuil = (BAYER[py & 3][px & 3] + 0.5) / 16;
      t.data[i] = k > seuil ? this.s.c2 : this.s.c1; t.vu[i] = 1;
    }
  }
  _pipette(ev) {
    if (!this.dans(ev.x, ev.y)) return;
    const c = this.pixel(ev.x, ev.y, 'visible');
    if (!(c >>> 24)) return;
    if (this.trait.b === 2) this.s.c2 = c; else this.s.c1 = c;
    this._emet('etat');
  }
  /* --- sélection --- */
  _selDown(ev) {
    const t = this.trait, w = this.doc.w, h = this.doc.h;
    t.selAvant = this.s.selection ? this.s.selection.slice() : null;
    t.lasso = [[ev.x, ev.y]];
    if (t.outil === 'baguette') {
      const src = this.s.tousCalques ? compose(this.doc, this.s.image, 'visible') : (this.cel() || new Uint32Array(w * h));
      this._combineSel(this._region(ev.x, ev.y, src), ev.m);
      return;
    }
    this._selMove(ev);
  }
  _combineSel(m, mods) {
    const base = this.trait.selAvant;
    const out = new Uint8Array(m.length);
    for (let i = 0; i < m.length; i++) {
      if (mods & 1) out[i] = (base && base[i]) || m[i] ? 1 : 0;
      else if (mods & 2) out[i] = base && base[i] && !m[i] ? 1 : 0;
      else out[i] = m[i];
    }
    this.s.selection = out.some(v => v) ? out : null;
  }
  _selMove(ev) {
    const t = this.trait, w = this.doc.w, h = this.doc.h, m = new Uint8Array(w * h);
    if (t.outil === 'selrect') {
      const xa = Math.max(0, Math.min(t.x0, ev.x)), xb = Math.min(w - 1, Math.max(t.x0, ev.x));
      const ya = Math.max(0, Math.min(t.y0, ev.y)), yb = Math.min(h - 1, Math.max(t.y0, ev.y));
      for (let y = ya; y <= yb; y++) for (let x = xa; x <= xb; x++) m[y * w + x] = 1;
    } else {
      const L = t.lasso, last = L[L.length - 1];
      if (last[0] !== ev.x || last[1] !== ev.y) L.push([ev.x, ev.y]);
      for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
        let dedans = false;
        for (let i = 0, j = L.length - 1; i < L.length; j = i++) {
          const [xi, yi] = L[i], [xj, yj] = L[j];
          if ((yi > y) !== (yj > y) && x < (xj - xi) * (y - yi) / ((yj - yi) || 1e-9) + xi) dedans = !dedans;
        }
        if (dedans) m[y * w + x] = 1;
      }
      for (let i = 0; i < L.length; i++) { const a = L[i], b = L[(i + 1) % L.length]; ligne(a[0], a[1], b[0], b[1], (x, y) => { if (this.dans(x, y)) m[y * w + x] = 1; }); }
    }
    this._combineSel(m, t.m);
  }
  /* --- déplacer --- */
  _depDown(ev) {
    const t = this.trait, w = this.doc.w, h = this.doc.h, sel = this.s.selection;
    t.flotte = new Uint32Array(w * h); t.base = t.avant.slice();
    t.selDep = sel ? sel.slice() : null;
    for (let i = 0; i < w * h; i++) {
      if (sel && !sel[i]) continue;
      t.flotte[i] = t.avant[i];
      if (!(ev.m & 2)) t.base[i] = 0;
    }
  }
  _depMove(ev) {
    const t = this.trait, w = this.doc.w, h = this.doc.h;
    const ox = ev.x - t.x0, oy = ev.y - t.y0;
    t.data.set(t.base);
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
      const c = t.flotte[y * w + x]; if (!(c >>> 24)) continue;
      const nx = x + ox, ny = y + oy;
      if (nx < 0 || ny < 0 || nx >= w || ny >= h) continue;
      t.data[ny * w + nx] = c;
    }
    if (t.selDep) {
      const s = new Uint8Array(w * h);
      for (let i = 0; i < w * h; i++) if (t.selDep[i]) { const nx = i % w + ox, ny = ((i / w) | 0) + oy; if (nx >= 0 && ny >= 0 && nx < w && ny < h) s[ny * w + nx] = 1; }
      this.s.selection = s;
    }
  }
  _up() {
    const t = this.trait; this.trait = null;
    if (!t.data) { this._emet('etat'); return; }
    const idx = [], av = [], ap = [];
    for (let i = 0; i < t.data.length; i++) if (t.data[i] !== t.avant[i]) { idx.push(i); av.push(t.avant[i]); ap.push(t.data[i]); }
    if (!idx.length && !t.cree) return;
    if (!idx.length && t.cree) { delete this.doc.celData[t.cree.id]; this.doc.cels[t.cree.lid][t.cree.f] = null; return; }
    this._pousse({ t: 'px', id: t.id, idx: Int32Array.from(idx), av: Uint32Array.from(av), ap: Uint32Array.from(ap), cree: t.cree, outil: t.outil, n: idx.length });
    this.dernierTrait = { outil: t.outil, n: idx.length, x0: t.x0, y0: t.y0, x1: t.x, y1: t.y };
    if (t.outil === 'crayon' || t.outil === 'gomme' || t.outil === 'ombrage') this.dernierPoint = { x: t.x, y: t.y };
  }
  _annuleTrait() {
    const t = this.trait; this.trait = null;
    if (t.data) t.data.set(t.avant);
    if (t.cree) { delete this.doc.celData[t.cree.id]; this.doc.cels[t.cree.lid][t.cree.f] = null; }
    if (t.selAvant !== undefined) this.s.selection = t.selAvant;
    if (t.selDep !== undefined) this.s.selection = t.selDep;
    this.dit('Geste annulé (Échap).');
  }
  /* --- historique --- */
  _pousse(e) { this.hist.push(e); if (this.hist.length > 300) this.hist.shift(); this.futur = []; }
  _applique(e, sens) {
    if (e.t === 'px') {
      if (sens > 0 && e.cree) { this.doc.celData[e.cree.id] = new Uint32Array(this.doc.w * this.doc.h); this.doc.cels[e.cree.lid][e.cree.f] = e.cree.id; }
      const d = this.doc.celData[e.id];
      if (d) { const v = sens > 0 ? e.ap : e.av; for (let k = 0; k < e.idx.length; k++) d[e.idx[k]] = v[k]; }
      if (sens < 0 && e.cree) { delete this.doc.celData[e.cree.id]; this.doc.cels[e.cree.lid][e.cree.f] = null; }
    } else {
      const snap = sens > 0 ? e.ap : e.av;
      this.doc = copieDoc(snap.doc);
      this.s.calque = Math.min(snap.calque, this.doc.calques.length - 1);
      this.s.image = Math.min(snap.image, this.doc.images.length - 1);
      this.s.selection = null;
    }
  }
  _structure(fn) {
    const av = { doc: copieDoc(this.doc), calque: this.s.calque, image: this.s.image };
    const r = fn();
    const ap = { doc: copieDoc(this.doc), calque: this.s.calque, image: this.s.image };
    this._pousse({ t: 'doc', av, ap });
    return r;
  }

  /* --- actions --- */
  act(nom, a = {}) {
    const f = ACTIONS[nom];
    if (!f) throw new Error('Action inconnue : ' + nom);
    if (this.trait && nom !== 'option' && nom !== 'couleur') this._annuleTrait();
    let r;
    try { r = f.call(this, a); }
    catch (e) {
      if (e.refus) { this._note({ k: 'a', n: nom, a: jsonable(a), refus: e.message }); return { refus: e.message }; }
      throw e;
    }
    this._note({ k: 'a', n: nom, a: jsonable(a) });
    this._emet('act', { nom, a });
    return r === undefined ? { ok: true } : r;
  }

  /* --- projet --- */
  projet() {
    return { format: 'claude-pixel', version: 1, doc: serialiseDoc(this.doc), journal: this.journal, mode: this.mode, etat: { c1: hex(this.s.c1, true), c2: hex(this.s.c2, true) } };
  }
  charge(p) {
    if (!p || !AP.FORMATS.includes(p.format)) throw new Error('Ce fichier n\'est pas un projet Claude Pixel.');
    this.doc = deserialiseDoc(p.doc);
    this.journal = Array.isArray(p.journal) ? p.journal.slice() : [];
    const dernier = this.journal.length ? this.journal[this.journal.length - 1].t || 0 : 0;
    this.decalT = dernier + 1000; this.t0 = this.horloge();
    this.hist = []; this.futur = []; this.trait = null;
    this.s = Object.assign(this._etatDefaut(), { axeX2: this.doc.w, axeY2: this.doc.h });
    try { if (p.etat) { this.s.c1 = parseHex(p.etat.c1); this.s.c2 = parseHex(p.etat.c2); } } catch (e) { /* couleurs par défaut */ }
    this._emet('doc');
  }
  static rejoue(journal, jusqua = Infinity, mode = 'humain') {
    const a = new Atelier({ vide: true, enregistre: false, mode });
    a._rejeu = true;
    for (let i = 0; i < journal.length && i < jusqua; i++) a.joueEvenement(journal[i]);
    return a;
  }
  joueEvenement(ev) {
    if (ev.refus) return;
    if (ev.k === 'i') this.input(ev);
    else if (ev.k === 'a') { if (ev.n === 'doc.charge') return; this.act(ev.n, ev.a); }
  }
  /* Vérifie que chaque pixel vient des gestes du journal. */
  integrite() {
    const b = Atelier.rejoue(this.journal, Infinity, this.mode);
    const d1 = this.doc, d2 = b.doc;
    const ecarts = [];
    if (!d2 || d1.w !== d2.w || d1.h !== d2.h) return { ok: false, ecarts: ['taille différente'] };
    if (d1.calques.length !== d2.calques.length || d1.images.length !== d2.images.length) ecarts.push('structure différente (calques ou images)');
    for (let f = 0; f < Math.min(d1.images.length, d2.images.length); f++) {
      for (let l = 0; l < Math.min(d1.calques.length, d2.calques.length); l++) {
        const a = d1.cels[d1.calques[l].id][f], c = d2.cels[d2.calques[l].id] ? d2.cels[d2.calques[l].id][f] : null;
        const A = a ? d1.celData[a] : null, C = c ? d2.celData[c] : null;
        let n = 0;
        for (let i = 0; i < d1.w * d1.h; i++) if ((A ? A[i] : 0) !== (C ? C[i] : 0)) n++;
        if (n) ecarts.push('image ' + (f + 1) + ', calque « ' + d1.calques[l].nom + ' » : ' + n + ' pixels différents');
      }
    }
    return { ok: !ecarts.length, ecarts, evenements: this.journal.length };
  }
}
function jsonable(a) {
  if (a === null || typeof a !== 'object') return a;
  if (ArrayBuffer.isView(a)) return Array.from(a);
  if (Array.isArray(a)) return a.map(jsonable);
  const o = {}; for (const k in a) o[k] = jsonable(a[k]); return o;
}

const ACTIONS = {
  'doc.nouveau'(a) {
    let pal = a.palette;
    if (typeof pal === 'string') pal = AP.PALETTES[pal];
    this.doc = nouveauDoc(Object.assign({}, a, { palette: pal }));
    this.hist = []; this.futur = []; this.trait = null;
    const garde = { outil: this.s.outil, c1: this.s.c1, c2: this.s.c2 };
    this.s = Object.assign(this._etatDefaut(), garde, { axeX2: this.doc.w, axeY2: this.doc.h });
    if (pal && pal.length) this.s.c1 = parseHex(pal[0]);
    this._emet('doc');
  },
  'doc.redim'(a) {
    const w = Math.max(1, Math.min(512, a.w | 0)), h = Math.max(1, Math.min(512, a.h | 0));
    const ax = { g: 0, c: 0.5, d: 1 }[a.ax || 'c'], ay = { h: 0, c: 0.5, b: 1 }[a.ay || 'c'];
    this._structure(() => {
      const d = this.doc, ox = Math.round((w - d.w) * ax), oy = Math.round((h - d.h) * ay);
      for (const k in d.celData) {
        const src = d.celData[k], dst = new Uint32Array(w * h);
        for (let y = 0; y < d.h; y++) for (let x = 0; x < d.w; x++) {
          const nx = x + ox, ny = y + oy;
          if (nx >= 0 && ny >= 0 && nx < w && ny < h) dst[ny * w + nx] = src[y * d.w + x];
        }
        d.celData[k] = dst;
      }
      d.w = w; d.h = h; this.s.axeX2 = w; this.s.axeY2 = h; this.s.selection = null;
    });
    this._emet('doc');
  },
  'doc.echelle'(a) {
    const f = Number(a.f) || 2;
    this._structure(() => {
      const d = this.doc, w = Math.max(1, Math.round(d.w * f)), h = Math.max(1, Math.round(d.h * f));
      if (w > 512 || h > 512) this.refuse('Trop grand (512 px au plus).');
      for (const k in d.celData) {
        const src = d.celData[k], dst = new Uint32Array(w * h);
        for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) dst[y * w + x] = src[Math.min(d.h - 1, Math.floor(y / f)) * d.w + Math.min(d.w - 1, Math.floor(x / f))];
        d.celData[k] = dst;
      }
      d.w = w; d.h = h; this.s.axeX2 = w; this.s.axeY2 = h; this.s.selection = null;
    });
    if (f > 1) this.dit('Agrandir fait des « super pixels » (A6-H) : redessine à la taille finale.', 'alerte');
    this._emet('doc');
  },
  'doc.nom'(a) { this.doc.nom = String(a.nom || '').slice(0, 80) || 'sans titre'; },
  'outil'(a) { if (!OUTILS.includes(a.nom)) this.refuse('Outil inconnu : ' + a.nom); this.s.outil = a.nom; this._emet('etat'); },
  'couleur'(a) {
    if (a.c1 !== undefined) this.s.c1 = parseHex(a.c1);
    if (a.c2 !== undefined) this.s.c2 = parseHex(a.c2);
    this._emet('etat');
  },
  'couleur.echange'() { const t = this.s.c1; this.s.c1 = this.s.c2; this.s.c2 = t; this._emet('etat'); },
  'option'(a) {
    if (!(a.cle in OPTIONS)) this.refuse('Option inconnue : ' + a.cle);
    this.s[a.cle] = OPTIONS[a.cle](a.valeur);
    this._emet('etat');
  },
  'annule'() {
    const e = this.hist.pop(); if (!e) { this.dit('Rien à annuler.'); return { vide: true }; }
    this._applique(e, -1); this.futur.push(e); this._emet('doc');
  },
  'refait'() {
    const e = this.futur.pop(); if (!e) { this.dit('Rien à refaire.'); return { vide: true }; }
    this._applique(e, 1); this.hist.push(e); this._emet('doc');
  },
  /* calques */
  'calque.ajoute'(a) {
    this._structure(() => {
      const type = ['normal', 'construction', 'reference'].includes(a.type) ? a.type : 'normal';
      const pos = this.s.calque + 1;
      const c = ajouteCalque(this.doc, a.nom || (type === 'construction' ? 'Construction' : type === 'reference' ? 'Référence' : 'Calque ' + (this.doc.calques.length + 1)), type, pos);
      if (type === 'construction') { c.teinte = a.teinte || null; c.opacite = 60; }
      if (type === 'reference') c.opacite = 50;
      this.s.calque = pos;
    });
    this._emet('doc');
  },
  'calque.supprime'(a) {
    const i = a.i === undefined ? this.s.calque : a.i;
    if (this.doc.calques.length <= 1) this.refuse('Il faut garder au moins un calque.');
    this._structure(() => {
      const c = this.doc.calques[i]; this.doc.calques.splice(i, 1);
      for (const id of this.doc.cels[c.id]) if (id && !this._celUtilise(id, c.id)) delete this.doc.celData[id];
      delete this.doc.cels[c.id];
      this.s.calque = Math.max(0, Math.min(this.s.calque, this.doc.calques.length - 1));
    });
    this._emet('doc');
  },
  'calque.duplique'(a) {
    const i = a.i === undefined ? this.s.calque : a.i;
    this._structure(() => {
      const src = this.doc.calques[i];
      const c = ajouteCalque(this.doc, src.nom + ' copie', src.type, i + 1);
      Object.assign(c, { visible: src.visible, opacite: src.opacite, teinte: src.teinte, px: src.px });
      this.doc.cels[c.id] = this.doc.cels[src.id].map(id => id ? nouveauCel(this.doc, this.doc.celData[id].slice()) : null);
      this.s.calque = i + 1;
    });
    this._emet('doc');
  },
  'calque.deplace'(a) {
    const i = a.i === undefined ? this.s.calque : a.i, j = i + (a.sens | 0);
    if (j < 0 || j >= this.doc.calques.length) return;
    this._structure(() => { const L = this.doc.calques; [L[i], L[j]] = [L[j], L[i]]; this.s.calque = j; });
    this._emet('doc');
  },
  'calque.fusionne'(a) {
    const i = a.i === undefined ? this.s.calque : a.i;
    if (i <= 0) this.refuse('Pas de calque dessous.');
    this._structure(() => {
      const d = this.doc, haut = d.calques[i], bas = d.calques[i - 1];
      for (let f = 0; f < d.images.length; f++) {
        const ih = d.cels[haut.id][f]; if (!ih) continue;
        let ib = d.cels[bas.id][f];
        if (!ib) { ib = nouveauCel(d); d.cels[bas.id][f] = ib; }
        const H = d.celData[ih], B = d.celData[ib], op = haut.opacite / 100;
        for (let k = 0; k < H.length; k++) if (H[k] >>> 24) B[k] = melange(B[k], H[k], op);
      }
      d.calques.splice(i, 1); delete d.cels[haut.id];
      this.s.calque = i - 1;
    });
    this._emet('doc');
  },
  'calque.choisit'(a) { const i = a.i | 0; if (i < 0 || i >= this.doc.calques.length) this.refuse('Calque inexistant.'); this.s.calque = i; this._emet('etat'); },
  'calque.prop'(a) {
    const i = a.i === undefined ? this.s.calque : a.i, c = this.doc.calques[i];
    if (!c) this.refuse('Calque inexistant.');
    this._structure(() => {
      if (a.nom !== undefined) c.nom = String(a.nom).slice(0, 40) || c.nom;
      if (a.visible !== undefined) c.visible = !!a.visible;
      if (a.opacite !== undefined) c.opacite = Math.max(0, Math.min(100, a.opacite | 0));
      if (a.verrou !== undefined) c.verrou = !!a.verrou;
      if (a.type !== undefined && ['normal', 'construction', 'reference'].includes(a.type)) c.type = a.type;
      if (a.teinte !== undefined) c.teinte = a.teinte;
      if (a.px !== undefined) c.px = Math.max(0, Math.min(2, Number(a.px) || 0));
    });
    this._emet('doc');
  },
  /* images */
  'image.ajoute'(a) {
    this._structure(() => {
      const d = this.doc, pos = this.s.image + 1;
      d.images.splice(pos, 0, { ms: d.images[this.s.image].ms, role: '', change: '', principe: '', validee: false });
      for (const c of d.calques) d.cels[c.id].splice(pos, 0, null);
      this.s.image = pos;
    });
    this._emet('doc');
  },
  'image.duplique'(a) {
    this._structure(() => {
      const d = this.doc, f = this.s.image, pos = f + 1;
      d.images.splice(pos, 0, Object.assign({}, d.images[f], { validee: false }));
      for (const c of d.calques) {
        const id = d.cels[c.id][f];
        d.cels[c.id].splice(pos, 0, id ? (a.lie ? id : nouveauCel(d, d.celData[id].slice())) : null);
      }
      this.s.image = pos;
    });
    this._emet('doc');
  },
  'image.supprime'(a) {
    const f = a.i === undefined ? this.s.image : a.i;
    if (this.doc.images.length <= 1) this.refuse('Il faut garder au moins une image.');
    this._structure(() => {
      const d = this.doc;
      d.images.splice(f, 1);
      for (const c of d.calques) { const id = d.cels[c.id].splice(f, 1)[0]; if (id && !this._celUtilise(id)) delete d.celData[id]; }
      d.etiquettes = d.etiquettes.filter(t => t.de < d.images.length).map(t => Object.assign(t, { a: Math.min(t.a, d.images.length - 1) }));
      this.s.image = Math.min(f, d.images.length - 1);
    });
    this._emet('doc');
  },
  'image.deplace'(a) {
    const de = a.de === undefined ? this.s.image : a.de, vers = a.vers | 0, d = this.doc;
    if (vers < 0 || vers >= d.images.length || de === vers) return;
    this._structure(() => {
      d.images.splice(vers, 0, d.images.splice(de, 1)[0]);
      for (const c of d.calques) d.cels[c.id].splice(vers, 0, d.cels[c.id].splice(de, 1)[0]);
      this.s.image = vers;
    });
    this._emet('doc');
  },
  'image.choisit'(a) { const i = a.i | 0; if (i < 0 || i >= this.doc.images.length) this.refuse('Image inexistante.'); this.s.image = i; this._emet('etat'); },
  'image.info'(a) {
    const i = a.i === undefined ? this.s.image : a.i, im = this.doc.images[i];
    if (!im) this.refuse('Image inexistante.');
    this._structure(() => {
      if (a.ms !== undefined) im.ms = Math.max(10, Math.min(10000, a.ms | 0));
      for (const k of ['role', 'change', 'principe']) if (a[k] !== undefined) im[k] = String(a[k]).slice(0, 120);
      if (a.validee !== undefined) im.validee = !!a.validee;
    });
    this._emet('doc');
  },
  'cel.delie'() {
    const id = this.celId(); if (!id) return;
    this._structure(() => { this.doc.cels[this.calque.id][this.s.image] = nouveauCel(this.doc, this.doc.celData[id].slice()); });
    this._emet('doc');
  },
  'etiquette.ajoute'(a) {
    this._structure(() => this.doc.etiquettes.push({ nom: String(a.nom || 'anim').slice(0, 30), de: Math.max(0, a.de | 0), a: Math.min(this.doc.images.length - 1, a.a | 0), sens: ['avant', 'arriere', 'pingpong'].includes(a.sens) ? a.sens : 'avant' }));
    this._emet('doc');
  },
  'etiquette.supprime'(a) { this._structure(() => this.doc.etiquettes.splice(a.i | 0, 1)); this._emet('doc'); },
  /* palette */
  'palette.ajoute'(a) {
    const h = hex(parseHex(a.hex));
    if (this.doc.palette.includes(h)) return { deja: true };
    this._structure(() => this.doc.palette.push(h)); this._emet('doc');
  },
  'palette.retire'(a) { this._structure(() => this.doc.palette.splice(a.i | 0, 1)); this._emet('doc'); },
  'palette.modifie'(a) {
    const i = a.i | 0, ancien = this.doc.palette[i]; if (!ancien) this.refuse('Teinte inexistante.');
    const nv = hex(parseHex(a.hex));
    this._structure(() => {
      this.doc.palette[i] = nv;
      for (const r of this.doc.rampes) r.couleurs = r.couleurs.map(c => c === ancien ? nv : c);
      if (a.remap) {
        const de = parseHex(ancien), vers = parseHex(nv);
        for (const k in this.doc.celData) { const D = this.doc.celData[k]; for (let j = 0; j < D.length; j++) if (D[j] === de) D[j] = vers; }
      }
    });
    if (this.s.c1 === parseHex(ancien)) this.s.c1 = parseHex(nv);
    this._emet('doc');
  },
  'palette.remplace'(a) {
    const L = (a.liste || []).map(h => hex(parseHex(h)));
    if (!L.length) this.refuse('Palette vide.');
    this._structure(() => { this.doc.palette = Array.from(new Set(L)).slice(0, 256); });
    this._emet('doc');
  },
  'palette.depuisImage'() {
    const m = couleursUtilisees(compose(this.doc, this.s.image, 'export'));
    const L = Array.from(m.keys()).sort((a, b) => lum(a) - lum(b)).map(c => hex(c));
    if (!L.length) this.refuse('L\'image est vide.');
    this._structure(() => { this.doc.palette = L; });
    this._emet('doc');
  },
  'rampe.ajoute'(a) {
    const cs = (a.couleurs || []).map(h => hex(parseHex(h)));
    if (cs.length < 2) this.refuse('Une rampe a au moins 2 tons.');
    this._structure(() => {
      this.doc.rampes.push({ nom: String(a.nom || 'Rampe ' + (this.doc.rampes.length + 1)).slice(0, 30), couleurs: cs });
      for (const c of cs) if (!this.doc.palette.includes(c)) this.doc.palette.push(c);
    });
    this._emet('doc');
  },
  'rampe.retire'(a) { this._structure(() => this.doc.rampes.splice(a.i | 0, 1)); this._emet('doc'); },
  /* sélection */
  'selection.tout'() { this.s.selection = new Uint8Array(this.doc.w * this.doc.h).fill(1); this._emet('etat'); },
  'selection.rien'() { this.s.selection = null; this._emet('etat'); },
  'selection.inverse'() {
    const s = this.s.selection, n = new Uint8Array(this.doc.w * this.doc.h);
    for (let i = 0; i < n.length; i++) n[i] = s && s[i] ? 0 : 1;
    this.s.selection = n.some(v => v) ? n : null; this._emet('etat');
  },
  /* pixels hors pinceau */
  'efface'() { this._pixels(D => { const s = this.s.selection; for (let i = 0; i < D.length; i++) if (!s || s[i]) D[i] = 0; }); },
  'transforme'(a) {
    const w = this.doc.w, h = this.doc.h, op = a.op;
    const fait = D => {
      const s = this.s.selection;
      let xa = 0, ya = 0, xb = w - 1, yb = h - 1;
      if (s) { xa = w; ya = h; xb = -1; yb = -1; for (let i = 0; i < s.length; i++) if (s[i]) { const x = i % w, y = (i / w) | 0; xa = Math.min(xa, x); xb = Math.max(xb, x); ya = Math.min(ya, y); yb = Math.max(yb, y); } if (xb < 0) return; }
      const bw = xb - xa + 1, bh = yb - ya + 1, src = new Uint32Array(bw * bh);
      for (let y = 0; y < bh; y++) for (let x = 0; x < bw; x++) { const i = (ya + y) * w + xa + x; if (!s || s[i]) { src[y * bw + x] = D[i]; D[i] = 0; } }
      let out, ow = bw, oh = bh;
      if (op === 'miroirH') { out = new Uint32Array(bw * bh); for (let y = 0; y < bh; y++) for (let x = 0; x < bw; x++) out[y * bw + x] = src[y * bw + bw - 1 - x]; }
      else if (op === 'miroirV') { out = new Uint32Array(bw * bh); for (let y = 0; y < bh; y++) for (let x = 0; x < bw; x++) out[y * bw + x] = src[(bh - 1 - y) * bw + x]; }
      else if (op === 'rot180') { out = src.slice().reverse(); }
      else if (op === 'rot90' || op === 'rot270') {
        ow = bh; oh = bw; out = new Uint32Array(ow * oh);
        for (let y = 0; y < bh; y++) for (let x = 0; x < bw; x++) {
          const v = src[y * bw + x];
          if (op === 'rot90') out[x * ow + (bh - 1 - y)] = v; else out[(bw - 1 - x) * ow + y] = v;
        }
      } else if (op === 'rotsprite') { out = rotsprite(src, bw, bh, Number(a.angle) || 0); }
      else this.refuse('Transformation inconnue.');
      const cx = xa + Math.floor((bw - ow) / 2), cy = ya + Math.floor((bh - oh) / 2);
      for (let y = 0; y < oh; y++) for (let x = 0; x < ow; x++) {
        const v = out[y * ow + x]; if (!(v >>> 24)) continue;
        const nx = cx + x, ny = cy + y; if (nx >= 0 && ny >= 0 && nx < w && ny < h) D[ny * w + nx] = v;
      }
    };
    if (a.cible === 'images') {
      const garde = this.s.image;
      for (let f = 0; f < this.doc.images.length; f++) { this.s.image = f; this._pixels(fait, true); }
      this.s.image = garde; this._emet('doc');
    } else this._pixels(fait);
    if (op === 'rotsprite') this.dit('RotSprite : repasse le contour à la main (A6-H), la rotation casse les marches.', 'alerte');
  },
  'pinceau.capture'() {
    const sel = this.s.selection, D = this.cel(), w = this.doc.w, h = this.doc.h;
    if (!sel || !D) this.refuse('Sélectionne d\'abord une zone dessinée du calque.');
    let x0 = w, y0 = h, x1 = -1, y1 = -1;
    for (let i = 0; i < sel.length; i++) if (sel[i] && (D[i] >>> 24)) { const x = i % w, y = (i / w) | 0; x0 = Math.min(x0, x); y0 = Math.min(y0, y); x1 = Math.max(x1, x); y1 = Math.max(y1, y); }
    if (x1 < 0) this.refuse('La sélection ne contient aucun pixel.');
    const pw = x1 - x0 + 1, ph = y1 - y0 + 1;
    if (pw > 32 || ph > 32) this.refuse('Un pinceau tient dans 32×32 px.');
    const px = new Uint32Array(pw * ph);
    for (let y = 0; y < ph; y++) for (let x = 0; x < pw; x++) { const i = (y + y0) * w + x + x0; if (sel[i]) px[y * pw + x] = D[i]; }
    this.s.pinceau = { w: pw, h: ph, px };
    this.s.outil = 'crayon';
    this.dit('Pinceau ' + pw + '×' + ph + ' pris dans la sélection.');
    this._emet('etat');
  },
  'pinceau.retire'() { this.s.pinceau = null; this._emet('etat'); },
  'decale'(a) {
    // décalage cyclique du calque (raccords de tuile, F2-A)
    const w = this.doc.w, h = this.doc.h, dx = ((a.dx | 0) % w + w) % w, dy = ((a.dy | 0) % h + h) % h;
    if (!dx && !dy) return;
    this._pixels(D => { const s = D.slice(); for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) D[((y + dy) % h) * w + (x + dx) % w] = s[y * w + x]; });
  },
  'calque.pileE6'() {
    // pile fixe d'animation (E6) : ref, ombre, arriere, corps, avant, fx, eclat, pivot (du bas vers le haut)
    const pile = [['ref', 'reference'], ['ombre', 'normal'], ['arriere_bras', 'normal'], ['corps', 'normal'], ['avant_bras', 'normal'], ['fx', 'normal'], ['eclat', 'normal'], ['pivot', 'construction']];
    this._structure(() => {
      const d = this.doc;
      for (const [nom, type] of pile) {
        if (d.calques.some(c => c.nom === nom)) continue;
        const c = ajouteCalque(d, nom, type);
        if (type === 'reference') { c.opacite = 50; d.calques.unshift(d.calques.pop()); }
        if (type === 'construction') { c.opacite = 80; c.teinte = '#3b82f6'; }
      }
      this.s.calque = Math.max(0, d.calques.findIndex(c => c.nom === 'corps'));
    });
    this._emet('doc');
  },
  'remplace.couleur'(a) {
    const de = parseHex(a.de), vers = parseHex(a.vers);
    const faire = D => { const s = this.s.selection; for (let i = 0; i < D.length; i++) if (D[i] === de && (!s || s[i])) D[i] = vers; };
    if (a.portee === 'tout') this._structure(() => { for (const k in this.doc.celData) faire(this.doc.celData[k]); });
    else this._pixels(faire);
    this._emet('doc');
  },
  'contour.auto'(a) {
    // Contour du calque seul (C14-B étape 4) : chaque pixel vide qui touche le calque devient trait.
    const w = this.doc.w, h = this.doc.h, c = parseHex(a.couleur || hex(this.s.c1));
    const diag = !!a.diagonales;
    this._pixels(D => {
      const src = D.slice();
      for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
        if (src[y * w + x] >>> 24) continue;
        const v = [[1, 0], [-1, 0], [0, 1], [0, -1]].concat(diag ? [[1, 1], [1, -1], [-1, 1], [-1, -1]] : []);
        if (v.some(([dx, dy]) => { const nx = x + dx, ny = y + dy; return nx >= 0 && ny >= 0 && nx < w && ny < h && (src[ny * w + nx] >>> 24); })) D[y * w + x] = c;
      }
    });
  },
  'importe'(a) {
    const type = a.type === 'reference' ? 'reference' : 'normal';
    if (this.mode === 'claude' && type !== 'reference') this.refuse('Mode Claude : une image importée ne va que dans un calque de référence. Les pixels se dessinent à la souris.');
    const w = a.w | 0, h = a.h | 0, u8 = typeof a.data === 'string' ? b64dec(a.data) : Uint8Array.from(a.data || []);
    if (u8.length < w * h * 4) this.refuse('Image importée illisible.');
    const src = new Uint32Array(u8.slice(0, w * h * 4).buffer);
    this._structure(() => {
      const d = this.doc, pos = this.s.calque + 1;
      const c = ajouteCalque(d, a.nom || (type === 'reference' ? 'Référence' : 'Import'), type, pos);
      if (type === 'reference') c.opacite = 50;
      const D = new Uint32Array(d.w * d.h);
      const ox = Math.floor((d.w - w) / 2), oy = Math.floor((d.h - h) / 2);
      for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) { const nx = x + ox, ny = y + oy; if (nx >= 0 && ny >= 0 && nx < d.w && ny < d.h) D[ny * d.w + nx] = src[y * w + x]; }
      d.cels[c.id][this.s.image] = nouveauCel(d, D);
      this.s.calque = pos;
    });
    this._emet('doc');
  },
  /* tuiles et carte */
  'tuile.reglage'(a) {
    this._structure(() => {
      const t = this.doc.tuile;
      if (a.on !== undefined) t.on = !!a.on;
      if (a.tw) t.tw = Math.max(4, Math.min(128, a.tw | 0));
      if (a.th) t.th = Math.max(4, Math.min(128, a.th | 0));
    });
    this._emet('doc');
  },
  'carte.peint'(a) {
    const c = this.doc.carte, i = (a.y | 0) * c.cols + (a.x | 0);
    if (a.x < 0 || a.y < 0 || a.x >= c.cols || a.y >= c.rows) return;
    if (a.terrain !== undefined) c.terrain[i] = a.terrain ? 1 : 0;
    if (a.tuile !== undefined) c.tuiles[i] = a.tuile | 0;
    this._emet('carte');
  },
  'carte.efface'() { this.doc.carte.terrain = []; this.doc.carte.tuiles = []; this._emet('carte'); },
  /* méthode */
  'fiche'(a) { this._structure(() => { Object.assign(this.doc.meta.fiche, a.champs || {}); if (a.type) this.doc.type = a.type; }); this._emet('methode'); },
  /* Lumière (partie 0-C) : d'où elle vient, sa hauteur et la forme imaginée pour le guide. */
  'lumiere'(a) {
    const l = this.doc.lumiere = Object.assign({ az: 135, el: 40, forme: 'gonfle', posee: false }, this.doc.lumiere || {});
    if (a.az !== undefined) { const v = Number(a.az); if (!Number.isFinite(v)) this.refuse('Direction invalide.'); l.az = ((Math.round(v) % 360) + 360) % 360; l.posee = true; }
    if (a.el !== undefined) { const v = Number(a.el); if (!(v >= 5 && v <= 85)) this.refuse('Hauteur entre 5 et 85 degrés.'); l.el = Math.round(v); }
    if (a.forme !== undefined) { if (!['gonfle', 'sphere', 'cylindre'].includes(a.forme)) this.refuse('Forme : gonfle, sphere ou cylindre.'); l.forme = a.forme; }
    this._emet('methode');
  },
  'regles.lues'() { this.doc.meta.reglesLues = true; this._emet('methode'); },
  'coche'(a) { const k = String(a.cle); this.doc.meta.coches[k] = !!a.valeur; this._emet('methode'); },
  'justifie'(a) {
    const t = String(a.texte || '').trim();
    if (t && t.length < 12) this.refuse('Une justification tient en une vraie phrase (12 caractères au moins).');
    if (t) this.doc.meta.justifs[a.cle] = t; else delete this.doc.meta.justifs[a.cle];
    this._emet('methode');
  },
  /* Carnet de conception (0-N) : on n'efface jamais une idée, on la barre en disant pourquoi. */
  'carnet.ajoute'(a) {
    const t = String(a.texte || '').trim().slice(0, 600);
    if (!t) this.refuse('Écris l\'idée avant de l\'ajouter au carnet.');
    const R = ['vision', 'structure', 'formes', 'unique', 'logique', 'variante', 'essai', 'iteration', 'detail', 'passe', 'critique', 'piece', 'choix'];
    const rub = R.includes(a.rubrique) ? a.rubrique : 'vision';
    const m = this.doc.meta; m.carnet = m.carnet || [];
    m.carnet.push({ n: m.carnet.length + 1, rubrique: rub, texte: t, barre: false, raison: '' });
    this._emet('methode');
  },
  'carnet.barre'(a) {
    const m = this.doc.meta, e = (m.carnet || [])[a.i | 0];
    if (!e) this.refuse('Idée inexistante.');
    const r = String(a.raison || '').trim().slice(0, 300);
    if (r.length < 8) this.refuse('Pour barrer une idée, écris pourquoi (8 caractères au moins).');
    e.barre = true; e.raison = r;
    this._emet('methode');
  },
  'planche.reponse'(a) { this.doc.meta.planche[a.cle] = String(a.texte || '').slice(0, 400); this._emet('methode'); },
  'etape.valide'() {
    const res = AP.verifieEtape ? AP.verifieEtape(this) : { ok: true, manque: [] };
    if (!res.ok) {
      if (this.mode === 'claude') this.refuse('Étape non validée : ' + res.manque.join(' ; '));
      this.dit('Étape passée malgré : ' + res.manque.join(' ; '), 'alerte');
    }
    const m = this.doc.meta;
    m.valideEtapes[m.etape] = { ok: res.ok, manque: res.manque };
    m.etape = Math.min(m.etape + 1, (AP.nbEtapes ? AP.nbEtapes(this.doc) : 99));
    this._emet('methode');
    return res;
  },
  /* Passe à la loupe (0-AE, 0-AF) : chaque zone de 8×8 ou 16×16 se retravaille puis se marque. */
  'zones.taille'(a) {
    const t = a.taille === 8 ? 8 : 16, m = this.doc.meta;
    m.zones = Object.assign({ faites: {} }, m.zones || {}, { taille: t }); this._emet('methode');
  },
  'zones.marque'(a) {
    const m = this.doc.meta; m.zones = m.zones || { taille: 16, faites: {} };
    const t = m.zones.taille, x = a.x | 0, y = a.y | 0;
    if (x < 0 || y < 0 || x * t >= this.doc.w || y * t >= this.doc.h) this.refuse('Zone hors du dessin.');
    const k = t + ':' + x + ',' + y;
    if (a.faite === false) delete m.zones.faites[k]; else m.zones.faites[k] = true;
    this._emet('methode');
  },
  /* Ramener le calque à la palette : chaque pixel prend la couleur de palette la plus proche
   * (après des passes en opacité, pour garder des tons choisis). */
  'calque.indexe'() {
    const pal = this.doc.palette.map(parseHex);
    if (!pal.length) this.refuse('La palette est vide.');
    const lab = c => { const r = c & 255, g = (c >>> 8) & 255, b = (c >>> 16) & 255; return [0.299 * r + 0.587 * g + 0.114 * b, r - g, (r + g) / 2 - b]; };
    const P = pal.map(lab), cache = new Map();
    this._pixels(D => {
      for (let i = 0; i < D.length; i++) {
        const c = D[i]; if (!(c >>> 24)) continue;
        let v = cache.get(c);
        if (v === undefined) {
          const L = lab(c); let best = 0, bd = Infinity;
          P.forEach((q, j) => { const d = 3 * (q[0] - L[0]) ** 2 + (q[1] - L[1]) ** 2 + (q[2] - L[2]) ** 2; if (d < bd) { bd = d; best = j; } });
          v = ((pal[best] & 0xffffff) | (c & 0xff000000)) >>> 0; cache.set(c, v);
        }
        D[i] = v;
      }
    });
    this._emet('doc');
  },
  'methode.migre'() {
    // Passe un document à la méthode actuelle sans perdre où il en est : on garde l'étape
    // courante par son identifiant (ou la dernière étape commune qui la précède).
    const m = this.doc.meta, ancien = AP.etapesDe(this.doc), cour = ancien[Math.min(m.etape, ancien.length - 1)];
    const v = AP.METHODE_ACTUELLE; if (!v || (m.methode || 0) >= v) this.refuse('Le document suit déjà la méthode actuelle.');
    const avant = m.methode || 0; m.methode = v;
    const neuf = AP.etapesDe(this.doc);
    let i = neuf.findIndex(e => e.id === cour.id);
    for (let k = ancien.indexOf(cour); i < 0 && k >= 0; k--) i = neuf.findIndex(e => e.id === ancien[k].id);
    const vieux = m.valideEtapes || [];
    m.valideEtapes = neuf.map(e => { const k = ancien.findIndex(x => x.id === e.id); return k >= 0 ? vieux[k] : undefined; });
    m.etape = Math.max(0, i);
    this.dit('Méthode v' + avant + ' → v' + v + ' : étape « ' + neuf[m.etape].titre + ' ». Les étapes nouvelles d\'avant restent à faire : reviens-y depuis la liste des étapes.', 'info');
    this._emet('methode');
  },
  'etape.va'(a) {
    const i = a.i | 0, m = this.doc.meta;
    if (this.mode === 'claude' && i > m.etape) this.refuse('On ne saute pas d\'étape : valide celle-ci d\'abord.');
    m.etape = Math.max(0, i); this._emet('methode');
  }
};
/* helpers liés aux actions */
Atelier.prototype._pixels = function (fn, silencieux) {
  const c = this.calque;
  if (c.verrou) this.refuse('Calque verrouillé.');
  let id = this.celId(), cree = null;
  if (!id) { id = nouveauCel(this.doc); this.doc.cels[c.id][this.s.image] = id; cree = { lid: c.id, f: this.s.image, id }; }
  const D = this.doc.celData[id], av = D.slice();
  fn(D);
  const idx = [], a1 = [], a2 = [];
  for (let i = 0; i < D.length; i++) if (D[i] !== av[i]) { idx.push(i); a1.push(av[i]); a2.push(D[i]); }
  if (!idx.length) { if (cree) { delete this.doc.celData[id]; this.doc.cels[c.id][this.s.image] = null; } return; }
  this._pousse({ t: 'px', id, idx: Int32Array.from(idx), av: Uint32Array.from(a1), ap: Uint32Array.from(a2), cree, n: idx.length });
  if (!silencieux) this._emet('pixels');
};
Atelier.prototype._celUtilise = function (id, sauf) {
  for (const lid in this.doc.cels) if (lid !== sauf && this.doc.cels[lid].includes(id)) return true;
  return false;
};
AP.ACTIONS = ACTIONS;
AP.Atelier = Atelier;
if (typeof module !== 'undefined') module.exports = AP;
})(typeof window !== 'undefined' ? window : globalThis);
