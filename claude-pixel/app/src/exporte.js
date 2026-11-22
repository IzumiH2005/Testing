/* Claude Pixel — exports et vues de contrôle (sans DOM).
 * PNG (agrandissement entier seulement), GIF89a animé (LZW), planche de sprites + JSON
 * compatible Aseprite, palettes .hex / .gpl, vues A6-J (gris, silhouette, flou, miroir,
 * une couleur de moins), rejeu pas à pas pour le timelapse. */
(function (G) {
'use strict';
const AP = G.AP;
const { pack, unpack, hex, lum, compose } = AP;

/* ---------- Agrandissement entier (A3 : jamais de facteur non entier) ---------- */
function agrandit(px, w, h, f) {
  f = Math.max(1, Math.round(f) | 0);
  if (f === 1) return { px: px.slice(), w, h };
  const W = w * f, H = h * f, o = new Uint32Array(W * H);
  for (let y = 0; y < H; y++) {
    const ys = ((y / f) | 0) * w, yo = y * W;
    for (let x = 0; x < W; x++) o[yo + x] = px[ys + ((x / f) | 0)];
  }
  return { px: o, w: W, h: H };
}

/* ---------- PNG (deflate en blocs stockés : sans dépendance, sans perte) ---------- */
const CRC = (() => { const t = new Uint32Array(256); for (let n = 0; n < 256; n++) { let c = n; for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1; t[n] = c >>> 0; } return t; })();
function crc32(b, s = 0, e = b.length) { let c = 0xffffffff; for (let i = s; i < e; i++) c = CRC[(c ^ b[i]) & 255] ^ (c >>> 8); return (c ^ 0xffffffff) >>> 0; }
function adler32(b) { let a = 1, d = 0; for (let i = 0; i < b.length; i++) { a = (a + b[i]) % 65521; d = (d + a) % 65521; } return ((d << 16) | a) >>> 0; }
function png(px, w, h) {
  const raw = new Uint8Array((w * 4 + 1) * h);
  const src = new Uint8Array(px.buffer, px.byteOffset, w * h * 4);
  for (let y = 0; y < h; y++) { raw[y * (w * 4 + 1)] = 0; raw.set(src.subarray(y * w * 4, (y + 1) * w * 4), y * (w * 4 + 1) + 1); }
  const nb = Math.max(1, Math.ceil(raw.length / 65535));
  const z = new Uint8Array(2 + raw.length + nb * 5 + 4);
  let p = 0; z[p++] = 0x78; z[p++] = 0x01;
  for (let i = 0; i < nb; i++) {
    const s = i * 65535, n = Math.min(65535, raw.length - s);
    z[p++] = i === nb - 1 ? 1 : 0; z[p++] = n & 255; z[p++] = n >> 8; z[p++] = ~n & 255; z[p++] = (~n >> 8) & 255;
    z.set(raw.subarray(s, s + n), p); p += n;
  }
  const ad = adler32(raw); z[p++] = ad >>> 24; z[p++] = (ad >>> 16) & 255; z[p++] = (ad >>> 8) & 255; z[p++] = ad & 255;
  const chunks = [];
  const chunk = (type, data) => {
    const c = new Uint8Array(12 + data.length), dv = new DataView(c.buffer);
    dv.setUint32(0, data.length); for (let i = 0; i < 4; i++) c[4 + i] = type.charCodeAt(i);
    c.set(data, 8); dv.setUint32(8 + data.length, crc32(c, 4, 8 + data.length)); chunks.push(c);
  };
  const ih = new Uint8Array(13), dv = new DataView(ih.buffer);
  dv.setUint32(0, w); dv.setUint32(4, h); ih[8] = 8; ih[9] = 6; ih[10] = 0; ih[11] = 0; ih[12] = 0;
  chunk('IHDR', ih); chunk('IDAT', z.subarray(0, p)); chunk('IEND', new Uint8Array(0));
  const sig = [137, 80, 78, 71, 13, 10, 26, 10];
  const out = new Uint8Array(8 + chunks.reduce((s, c) => s + c.length, 0));
  out.set(sig); let q = 8; for (const c of chunks) { out.set(c, q); q += c.length; }
  return out;
}

/* ---------- GIF89a ---------- */
function lzw(ind, minCode) {
  const clear = 1 << minCode, eoi = clear + 1;
  let size = minCode + 1, next = eoi + 1, dict = new Map();
  const out = []; let cur = 0, nb = 0;
  const emit = c => { cur |= c << nb; nb += size; while (nb >= 8) { out.push(cur & 255); cur >>>= 8; nb -= 8; } };
  emit(clear);
  let pre = ind[0];
  for (let i = 1; i < ind.length; i++) {
    const k = ind[i], key = (pre << 8) | k, v = dict.get(key);
    if (v !== undefined) { pre = v; continue; }
    emit(pre);
    if (next === 4096) { emit(clear); next = eoi + 1; size = minCode + 1; dict = new Map(); }
    else { if (next >= (1 << size)) size++; dict.set(key, next++); }
    pre = k;
  }
  emit(pre); emit(eoi);
  if (nb > 0) out.push(cur & 255);
  return out;
}
/* images : [{px, ms}] de même taille. Les pixels d'alpha < 128 deviennent transparents. */
function gif(images, w, h, o = {}) {
  const coul = new Map(); let transp = false;
  for (const im of images) for (const c of im.px) { if ((c >>> 24) < 128) transp = true; else coul.set(c & 0xffffff, 1); }
  let liste = [...coul.keys()];
  const max = transp ? 255 : 256;
  if (liste.length > max) liste = liste.slice(0, max); // au-delà : couleur la plus proche
  const tab = transp ? [0, ...liste] : liste;
  let bits = 1; while ((1 << bits) < tab.length) bits++;
  const n = 1 << bits;
  const idx = new Map(tab.map((c, i) => [c, i]));
  const proche = c => {
    let b = transp ? 1 : 0, bd = Infinity; const [r, g, bl] = unpack(c);
    for (let i = transp ? 1 : 0; i < tab.length; i++) { const [R, G2, B] = unpack(tab[i]); const d = (r - R) ** 2 + (g - G2) ** 2 + (bl - B) ** 2; if (d < bd) { bd = d; b = i; } }
    idx.set(c & 0xffffff, b); return b;
  };
  const o8 = [];
  const str = s => { for (let i = 0; i < s.length; i++) o8.push(s.charCodeAt(i)); };
  const u16 = v => { o8.push(v & 255, (v >> 8) & 255); };
  str('GIF89a'); u16(w); u16(h); o8.push(0x80 | 0x70 | (bits - 1), 0, 0);
  for (let i = 0; i < n; i++) { const c = tab[i] || 0; o8.push(c & 255, (c >>> 8) & 255, (c >>> 16) & 255); }
  if (images.length > 1) { o8.push(0x21, 0xff, 11); str('NETSCAPE2.0'); o8.push(3, 1); u16(o.boucles | 0); o8.push(0); }
  const minCode = Math.max(2, bits);
  for (const im of images) {
    const cs = Math.max(2, Math.round((im.ms || 100) / 10));
    o8.push(0x21, 0xf9, 4, (transp ? 1 : 0) | ((transp ? 2 : 1) << 2)); u16(cs); o8.push(0, 0);
    o8.push(0x2c); u16(0); u16(0); u16(w); u16(h); o8.push(0);
    const ind = new Uint8Array(w * h);
    for (let i = 0; i < ind.length; i++) {
      const c = im.px[i];
      if ((c >>> 24) < 128) { ind[i] = 0; continue; }
      const v = idx.get(c & 0xffffff); ind[i] = v === undefined ? proche(c) : v;
    }
    o8.push(minCode);
    const data = lzw(ind, minCode);
    for (let i = 0; i < data.length; i += 255) { const k = Math.min(255, data.length - i); o8.push(k); for (let j = 0; j < k; j++) o8.push(data[i + j]); }
    o8.push(0);
  }
  o8.push(0x3b);
  return Uint8Array.from(o8);
}

/* ---------- Exports d'un document ---------- */
function imageExport(doc, f, echelle = 1) { const a = agrandit(compose(doc, f, 'export'), doc.w, doc.h, echelle); return a; }
function pngImage(doc, f, echelle = 1) { const a = imageExport(doc, f, echelle); return png(a.px, a.w, a.h); }
function gifDoc(doc, o = {}) {
  const e = Math.max(1, o.echelle | 0 || 1);
  const de = o.de || 0, a = o.a === undefined ? doc.images.length - 1 : o.a;
  const ims = [];
  for (let f = de; f <= a; f++) ims.push({ px: imageExport(doc, f, e).px, ms: doc.images[f].ms });
  if (o.pingpong) for (let f = a - 1; f > de; f--) ims.push({ px: imageExport(doc, f, e).px, ms: doc.images[f].ms });
  return gif(ims, doc.w * e, doc.h * e, o);
}
function planche(doc, o = {}) {
  const e = Math.max(1, o.echelle | 0 || 1), n = doc.images.length;
  const cols = Math.max(1, Math.min(n, o.colonnes | 0 || n)), rows = Math.ceil(n / cols), m = o.marge | 0;
  const fw = doc.w * e, fh = doc.h * e, W = cols * fw + (cols - 1) * m, H = rows * fh + (rows - 1) * m;
  const out = new Uint32Array(W * H), frames = [];
  for (let f = 0; f < n; f++) {
    const cx = (f % cols) * (fw + m), cy = ((f / cols) | 0) * (fh + m), im = imageExport(doc, f, e).px;
    for (let y = 0; y < fh; y++) out.set(im.subarray(y * fw, (y + 1) * fw), (cy + y) * W + cx);
    const info = doc.images[f];
    frames.push({ filename: (doc.nom || 'sprite') + ' ' + f, frame: { x: cx, y: cy, w: fw, h: fh }, duration: info.ms, role: info.role || '' });
  }
  const json = {
    frames,
    meta: {
      app: 'Claude Pixel', version: '1', image: (doc.nom || 'sprite') + '.png', format: 'RGBA8888',
      size: { w: W, h: H }, scale: String(e),
      frameTags: doc.etiquettes.map(t => ({ name: t.nom, from: t.de, to: t.a, direction: t.sens || 'forward' }))
    }
  };
  return { png: png(out, W, H), json: JSON.stringify(json, null, 2), w: W, h: H, px: out };
}
function paletteHex(doc) { return doc.palette.map(h => h.replace('#', '').slice(0, 6)).join('\n') + '\n'; }
function paletteGpl(doc) {
  const l = ['GIMP Palette', 'Name: ' + (doc.nom || 'Claude Pixel'), 'Columns: 8', '#'];
  for (const h of doc.palette) { const [r, g, b] = unpack(AP.parseHex(h)); l.push(String(r).padStart(3) + ' ' + String(g).padStart(3) + ' ' + String(b).padStart(3) + '\t' + h); }
  return l.join('\n') + '\n';
}
function lisPalette(texte) {
  const out = [];
  for (const ligne of String(texte).split(/\r?\n/)) {
    const s = ligne.trim(); if (!s || s.startsWith('#') && !/^#[0-9a-f]{6}\b/i.test(s)) continue;
    const m3 = s.match(/^(\d{1,3})\s+(\d{1,3})\s+(\d{1,3})/);
    if (m3) { out.push(hex(pack(+m3[1], +m3[2], +m3[3]))); continue; }
    const mh = s.match(/#?([0-9a-f]{6})\b/i);
    if (mh) out.push('#' + mh[1].toLowerCase());
  }
  return [...new Set(out)].slice(0, 256);
}

/* ---------- Vues de contrôle (A6-J) ---------- */
function gris(px) { const o = new Uint32Array(px.length); for (let i = 0; i < px.length; i++) { const c = px[i]; if (!(c >>> 24)) continue; const v = Math.round(lum(c) * 255); o[i] = pack(v, v, v, c >>> 24); } return o; }
function silhouette(px, c = pack(20, 16, 28)) { const o = new Uint32Array(px.length); for (let i = 0; i < px.length; i++) if ((px[i] >>> 24) >= 128) o[i] = c; return o; }
function miroir(px, w, h) { const o = new Uint32Array(px.length); for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) o[y * w + x] = px[y * w + (w - 1 - x)]; return o; }
/* « Plisser les yeux » : flou en boîte, rayon r, alpha prémultiplié. */
function flou(px, w, h, r = 1) {
  const o = new Uint32Array(px.length);
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
    let R = 0, Gg = 0, B = 0, A = 0, n = 0;
    for (let j = -r; j <= r; j++) for (let i = -r; i <= r; i++) {
      const xx = x + i, yy = y + j; n++;
      if (xx < 0 || yy < 0 || xx >= w || yy >= h) continue;
      const [a, b, c, d] = unpack(px[yy * w + xx]); const al = d / 255;
      R += a * al; Gg += b * al; B += c * al; A += al;
    }
    if (A > 0) o[y * w + x] = pack(Math.round(R / A), Math.round(Gg / A), Math.round(B / A), Math.round(A / n * 255));
  }
  return o;
}
/* « Une couleur de moins » : fusionne les deux couleurs les plus proches (distance perçue). */
function uneCouleurDeMoins(px) {
  const m = AP.couleursUtilisees(px), l = [...m.keys()];
  if (l.length < 2) return { px: px.slice(), de: null, vers: null };
  const d = (a, b) => { const [r, g, bl] = unpack(a), [R, G2, B] = unpack(b); const rm = (r + R) / 2; return (2 + rm / 256) * (r - R) ** 2 + 4 * (g - G2) ** 2 + (2 + (255 - rm) / 256) * (bl - B) ** 2; };
  let best = [l[0], l[1]], bd = Infinity;
  for (let i = 0; i < l.length; i++) for (let j = i + 1; j < l.length; j++) { const v = d(l[i], l[j]); if (v < bd) { bd = v; best = [l[i], l[j]]; } }
  const [a, b] = m.get(best[0]) >= m.get(best[1]) ? best : [best[1], best[0]];
  const o = px.slice(); for (let i = 0; i < o.length; i++) if (o[i] === b) o[i] = a;
  return { px: o, de: hex(b), vers: hex(a) };
}
function surFond(px, fond) { const o = new Uint32Array(px.length); for (let i = 0; i < px.length; i++) o[i] = (px[i] >>> 24) ? AP.melange(fond, px[i], 1) : fond; return o; }
const FONDS = { clair: pack(232, 226, 214), moyen: pack(120, 116, 128), sombre: pack(22, 20, 30) };

/* ---------- Rejeu pas à pas (lecteur, timelapse) ---------- */
/* Rend un lecteur : avance(n) joue n événements ; etat() rend l'image composée et le curseur. */
function lecteur(journal, mode = 'humain') {
  const at = new AP.Atelier({ vide: true, enregistre: false, mode });
  at._rejeu = true;
  let i = 0, curseur = { x: 0, y: 0, bas: false }, dernier = null;
  const chapitres = [], corrections = [];
  journal.forEach((ev, k) => {
    if (ev.k === 'a' && ev.n === 'etape.valide' && !ev.refus) chapitres.push({ i: k, t: ev.t });
    if (ev.k === 'a' && (ev.n === 'annule' || ev.n === 'efface') && !ev.refus) corrections.push({ i: k, t: ev.t });
    if (ev.k === 'i' && ev.type === 'cancel') corrections.push({ i: k, t: ev.t });
  });
  return {
    at, chapitres, corrections, total: journal.length,
    get i() { return i; },
    duree: journal.length ? journal[journal.length - 1].t - journal[0].t : 0,
    avance(n = 1) {
      for (let k = 0; k < n && i < journal.length; k++, i++) {
        const ev = journal[i]; dernier = ev;
        if (ev.k === 'i') curseur = { x: ev.x, y: ev.y, bas: ev.type === 'down' || ev.type === 'move' };
        try { at.joueEvenement(ev); } catch (e) { /* un événement cassé ne bloque pas le lecteur */ }
      }
      return i < journal.length;
    },
    jusquAuTemps(t) { while (i < journal.length && journal[i].t <= t) this.avance(1); },
    etat() { return { px: at.doc ? compose(at.doc, at.s.image, 'visible') : null, w: at.doc ? at.doc.w : 0, h: at.doc ? at.doc.h : 0, curseur, ev: dernier, i }; }
  };
}

Object.assign(AP, {
  agrandit, png, gif, lzw, crc32, imageExport, pngImage, gifDoc, planche, paletteHex, paletteGpl, lisPalette,
  VUES: { gris, silhouette, miroir, flou, uneCouleurDeMoins, surFond, FONDS }, lecteur
});
if (typeof module !== 'undefined') module.exports = AP;
})(typeof window !== 'undefined' ? window : globalThis);
