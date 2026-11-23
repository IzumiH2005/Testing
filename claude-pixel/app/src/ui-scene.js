/* Claude Pixel — interface : la toile (rendu, zoom, saisie pointeur et tactile,
 * raccourcis clavier, aperçus ×1 / ×2, curseur visible du mode Claude). */
(function (G) {
'use strict';
const AP = G.AP, U = AP.UI;
const { $, h } = U;
const ZOOMS = [1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32, 40, 48, 64];
const TEINTE_CONSTR = '#3b82f6';

const vue = U.vue = { zoom: 8, ox: 0, oy: 0, survol: null, pelure: false, vue3x3: true, grille: true, cacheConstr: false, mode: 'couleur', guide: false, miroir: false };
U.marques = null; // { pixels:[[x,y]], niveau }

let cv, ctx, scene, buf, bctx, dpr = 1, demande = false;

/* ---------- Composition d'affichage (construction teintée, référence en transparence) ---------- */
function composeAffichage(d, f, cacheConstr) {
  const out = new Uint32Array(d.w * d.h);
  for (const c of d.calques) {
    if (!c.visible) continue;
    if (c.type === 'construction' && cacheConstr) continue;
    const id = d.cels[c.id][f]; if (!id) continue;
    const src = d.celData[id], op = c.opacite / 100;
    let teinte = null;
    if (c.type === 'construction' && c.teinte !== 'aucune') { try { teinte = AP.parseHex(c.teinte || TEINTE_CONSTR) & 0xffffff; } catch (e) { teinte = AP.parseHex(TEINTE_CONSTR) & 0xffffff; } }
    for (let i = 0; i < out.length; i++) {
      let s = src[i]; const a = s >>> 24; if (!a) continue;
      if (teinte !== null) s = (teinte | (a << 24)) >>> 0;
      out[i] = (op >= 1 && a === 255) ? s : AP.melange(out[i], s, op);
    }
  }
  return out;
}
U.composeAffichage = composeAffichage;

function constructionCachee() {
  if (vue.cacheConstr) return true;
  try { const e = AP.etapeCourante(U.at.doc); return e && e.id === 'planche'; } catch (e) { return false; }
}

/* ---------- Lumière : guide de volume et repère (partie 0-C) ---------- */
function sourceGuide(d, f) {
  const c = d.calques[U.at.s.calque], id = c && c.type === 'normal' && d.cels[c.id][f];
  if (id) { const D = d.celData[id]; for (let i = 0; i < D.length; i++) if (D[i] >>> 24) return D; }
  return AP.compose(d, f, 'export');
}
let guideCache = { cle: '', g: null };
function guideDe(d, f) {
  const L = AP.VOLUME.lumiereDe(d), cle = U.at.journal.length + ':' + f + ':' + U.at.s.calque + ':' + L.az + ':' + L.el + ':' + L.forme + ':' + d.w + 'x' + d.h;
  if (guideCache.cle !== cle) guideCache = { cle, g: AP.VOLUME.guide(sourceGuide(d, f), d.w, d.h, L) };
  return guideCache.g;
}
function dessineGuide(d, f, X, Y, z) {
  const g = guideDe(d, f), Z = AP.VOLUME.ZONES;
  ctx.save(); ctx.globalAlpha = 0.5;
  for (let y = 0; y < d.h; y++) for (let x = 0; x < d.w; x++) {
    const k = g.zone[y * d.w + x]; if (!k) continue;
    ctx.fillStyle = Z[k].coul; ctx.fillRect(X + x * z, Y + y * z, z, z);
  }
  ctx.globalAlpha = 1; ctx.lineWidth = Math.max(2, z / 4); ctx.strokeStyle = '#ff3d6e'; ctx.lineCap = 'round';
  ctx.beginPath();
  for (const [x0, y0, x1, y1] of g.term) { ctx.moveTo(X + x0 * z, Y + y0 * z); ctx.lineTo(X + x1 * z, Y + y1 * z); }
  ctx.stroke(); ctx.restore();
}
function dessineSoleil(d, X, Y, W, H) {
  const L = AP.VOLUME.vecteur(d.lumiere), n = Math.hypot(L[0], L[1]) || 1, ux = L[0] / n, uy = L[1] / n;
  const cx = X + W / 2, cy = Y + H / 2, R = Math.hypot(W, H) / 2 + 26;
  const sx = cx + ux * R, sy = cy + uy * R, px = -uy, py = ux, demi = Math.min(W, H) * 0.32;
  ctx.save();
  ctx.fillStyle = 'rgba(255, 214, 102, 0.13)';
  ctx.beginPath(); ctx.moveTo(sx, sy); ctx.lineTo(cx + px * demi, cy + py * demi); ctx.lineTo(cx - px * demi, cy - py * demi); ctx.closePath(); ctx.fill();
  ctx.fillStyle = '#ffd666'; ctx.strokeStyle = '#7a5a00'; ctx.lineWidth = 1.5;
  ctx.beginPath(); ctx.arc(sx, sy, 7, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
  ctx.restore();
}

/* ---------- Coordonnées ---------- */
/* Toile retournée (0-AB-B) : la toile est retournée à l'écran par CSS ; les coordonnées suivent. */
function ecranVersCellule(cx, cy) {
  const r = cv.getBoundingClientRect(), lx = vue.miroir ? r.right - cx : cx - r.left;
  return { x: (lx - vue.ox) / vue.zoom, y: (cy - r.top - vue.oy) / vue.zoom };
}
function celluleVersEcran(x, y) {
  const r = cv.getBoundingClientRect(), lx = vue.ox + (x + 0.5) * vue.zoom;
  return { x: vue.miroir ? r.right - lx : r.left + lx, y: r.top + vue.oy + (y + 0.5) * vue.zoom };
}
function retourne(v) { vue.miroir = v === undefined ? !vue.miroir : !!v; if (cv) cv.style.transform = vue.miroir ? 'scaleX(-1)' : ''; redessine(); }
U.retourne = retourne;
U.ecranVersCellule = ecranVersCellule; U.celluleVersEcran = celluleVersEcran;

/* ---------- Zoom ---------- */
function ajuste() {
  const d = U.at.doc, r = scene.getBoundingClientRect();
  const marge = r.width < 500 ? 24 : 80;
  let z = 1;
  for (const zz of ZOOMS) if (d.w * zz <= r.width - marge && d.h * zz <= r.height - marge) z = zz;
  vue.zoom = z;
  vue.ox = Math.round((r.width - d.w * z) / 2);
  vue.oy = Math.round((r.height - d.h * z) / 2);
  majZoom(); redessine();
}
function zoomA(z, cx, cy) {
  const r = cv.getBoundingClientRect();
  if (cx === undefined) { cx = r.left + r.width / 2; cy = r.top + r.height / 2; }
  const px = cx - r.left, py = cy - r.top;
  const dx = (px - vue.ox) / vue.zoom, dy = (py - vue.oy) / vue.zoom;
  vue.zoom = z;
  vue.ox = Math.round(px - dx * z); vue.oy = Math.round(py - dy * z);
  majZoom(); redessine();
}
function zoomPas(sens, cx, cy) {
  let i = ZOOMS.findIndex(z => z >= vue.zoom); if (i < 0) i = ZOOMS.length - 1;
  if (ZOOMS[i] !== vue.zoom && sens < 0) { /* déjà entre deux crans */ } else i += sens;
  zoomA(ZOOMS[Math.max(0, Math.min(ZOOMS.length - 1, i))], cx, cy);
}
function majZoom() { const b = $('#b-zoom'); if (b) b.textContent = '×' + vue.zoom; }
U.ajuste = ajuste; U.zoomPas = zoomPas; U.zoomA = zoomA;

/* ---------- Rendu ---------- */
function redessine() { if (demande) return; demande = true; requestAnimationFrame(rendu); }
U.redessine = redessine;

function taille() {
  const r = scene.getBoundingClientRect();
  dpr = Math.max(1, Math.min(3, G.devicePixelRatio || 1));
  const W = Math.max(1, Math.round(r.width * dpr)), H = Math.max(1, Math.round(r.height * dpr));
  if (cv.width !== W || cv.height !== H) { cv.width = W; cv.height = H; cv.style.width = r.width + 'px'; cv.style.height = r.height + 'px'; }
}

function rendu() {
  demande = false;
  const at = U.at; if (!at || !at.doc) return;
  taille();
  const d = at.doc, z = vue.zoom, f = at.s.image;
  const tok = n => U.couleurToken(n);
  ctx.setTransform(1, 0, 0, 1, 0, 0);
  ctx.fillStyle = tok('--stage'); ctx.fillRect(0, 0, cv.width, cv.height);
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  ctx.imageSmoothingEnabled = false;
  const X = vue.ox, Y = vue.oy, W = d.w * z, H = d.h * z;

  // image composée
  if (buf.width !== d.w || buf.height !== d.h) { buf.width = d.w; buf.height = d.h; }
  let px = composeAffichage(d, f, constructionCachee());
  if (vue.mode === 'valeurs') px = AP.VUES.gris(px);
  else if (vue.mode === 'notan') px = AP.VOLUME.notan(px);
  U.pxVersCanvas(buf, px, d.w, d.h);

  const tuile = d.tuile && d.tuile.on && vue.vue3x3 && d.w <= d.tuile.tw * 1 && d.h <= d.tuile.th * 1;
  const damier = (x, y, w, hh) => {
    ctx.fillStyle = tok('--damier-a'); ctx.fillRect(x, y, w, hh);
    const c = Math.max(4, z * (d.w <= 16 ? 1 : 2));
    ctx.fillStyle = tok('--damier-b');
    ctx.save(); ctx.beginPath(); ctx.rect(x, y, w, hh); ctx.clip();
    for (let j = 0; j * c < hh; j++) for (let i = (j & 1); i * c < w; i += 2) ctx.fillRect(x + i * c, y + j * c, c, c);
    ctx.restore();
  };
  if (tuile) {
    // vue 3×3 : la tuile se répète, les voisines un peu atténuées
    for (let j = -1; j <= 1; j++) for (let i = -1; i <= 1; i++) {
      const x = X + i * W, y = Y + j * H;
      if (x > cv.width / dpr || y > cv.height / dpr || x + W < 0 || y + H < 0) continue;
      damier(x, y, W, H);
      ctx.globalAlpha = (i || j) ? 0.7 : 1;
      ctx.drawImage(buf, x, y, W, H);
      ctx.globalAlpha = 1;
    }
  } else damier(X, Y, W, H);

  // pelure d'oignon
  if (vue.pelure && d.images.length > 1) {
    const voisins = [[f - 1, 'rgba(230,70,90,'], [f + 1, 'rgba(60,170,120,']];
    for (const [g, coul] of voisins) {
      if (g < 0 || g >= d.images.length) continue;
      const p = composeAffichage(d, g, true);
      const o = document.createElement('canvas'); U.pxVersCanvas(o, p, d.w, d.h);
      const ox = o.getContext('2d'); ox.globalCompositeOperation = 'source-in'; ox.fillStyle = coul + '1)'; ox.fillRect(0, 0, d.w, d.h);
      ctx.globalAlpha = 0.28; ctx.drawImage(o, X, Y, W, H); ctx.globalAlpha = 1;
    }
  }
  ctx.drawImage(buf, X, Y, W, H);

  // guide de volume (0-C) : zones colorées et terminateur, par-dessus le dessin
  if (vue.guide) dessineGuide(d, f, X, Y, z);
  // repère de lumière : un point et un cône, comme sur les planches
  if (d.lumiere && d.lumiere.posee) dessineSoleil(d, X, Y, W, H);

  // grilles
  if (vue.grille && z >= 6) {
    ctx.beginPath();
    for (let i = 1; i < d.w; i++) { ctx.moveTo(X + i * z + 0.5 / dpr, Y); ctx.lineTo(X + i * z + 0.5 / dpr, Y + H); }
    for (let j = 1; j < d.h; j++) { ctx.moveTo(X, Y + j * z + 0.5 / dpr); ctx.lineTo(X + W, Y + j * z + 0.5 / dpr); }
    ctx.strokeStyle = U.themeEffectif() === 'light' ? 'rgba(0,0,0,.08)' : 'rgba(255,255,255,.07)';
    ctx.lineWidth = 1 / dpr; ctx.stroke();
  }
  if (d.tuile && d.tuile.on) {
    ctx.beginPath();
    for (let i = d.tuile.tw; i < d.w; i += d.tuile.tw) { ctx.moveTo(X + i * z, Y); ctx.lineTo(X + i * z, Y + H); }
    for (let j = d.tuile.th; j < d.h; j += d.tuile.th) { ctx.moveTo(X, Y + j * z); ctx.lineTo(X + W, Y + j * z); }
    ctx.strokeStyle = tok('--accent'); ctx.globalAlpha = 0.55; ctx.lineWidth = 1; ctx.stroke(); ctx.globalAlpha = 1;
  }
  ctx.strokeStyle = tok('--line-2'); ctx.lineWidth = 1; ctx.strokeRect(X - 0.5, Y - 0.5, W + 1, H + 1);

  // axes de symétrie
  const s = at.s;
  if (s.symX || s.symY) {
    ctx.save(); ctx.setLineDash([6, 4]); ctx.strokeStyle = tok('--info'); ctx.lineWidth = 1.5;
    ctx.beginPath();
    if (s.symX) { const ax = X + s.axeX2 / 2 * z; ctx.moveTo(ax, Y - 8); ctx.lineTo(ax, Y + H + 8); }
    if (s.symY) { const ay = Y + s.axeY2 / 2 * z; ctx.moveTo(X - 8, ay); ctx.lineTo(X + W + 8, ay); }
    ctx.stroke(); ctx.restore();
  }

  // sélection : contour des cases sélectionnées
  if (s.selection) {
    const sel = s.selection, path = new Path2D();
    for (let y = 0; y < d.h; y++) for (let x = 0; x < d.w; x++) {
      if (!sel[y * d.w + x]) continue;
      const x0 = X + x * z, y0 = Y + y * z;
      if (y === 0 || !sel[(y - 1) * d.w + x]) { path.moveTo(x0, y0); path.lineTo(x0 + z, y0); }
      if (y === d.h - 1 || !sel[(y + 1) * d.w + x]) { path.moveTo(x0, y0 + z); path.lineTo(x0 + z, y0 + z); }
      if (x === 0 || !sel[y * d.w + x - 1]) { path.moveTo(x0, y0); path.lineTo(x0, y0 + z); }
      if (x === d.w - 1 || !sel[y * d.w + x + 1]) { path.moveTo(x0 + z, y0); path.lineTo(x0 + z, y0 + z); }
    }
    ctx.save(); ctx.lineWidth = 1.5;
    ctx.strokeStyle = '#000'; ctx.stroke(path);
    ctx.setLineDash([4, 4]); ctx.strokeStyle = '#fff'; ctx.stroke(path); ctx.restore();
  }

  // défauts montrés depuis le Contrôle
  if (U.marques && U.marques.pixels) {
    ctx.save();
    ctx.strokeStyle = U.marques.niveau === 'erreur' ? tok('--danger') : tok('--warn');
    ctx.lineWidth = Math.max(1.5, z / 6);
    for (const [x, y] of U.marques.pixels) ctx.strokeRect(X + x * z + 1, Y + y * z + 1, z - 2, z - 2);
    ctx.restore();
  }

  // survol : empreinte de l'outil
  if (vue.survol && at.dans(vue.survol.x, vue.survol.y)) {
    const n = ['crayon', 'gomme', 'ombrage'].includes(s.outil) ? s.taille : 1, o = Math.floor((n - 1) / 2);
    const x0 = X + (vue.survol.x - o) * z, y0 = Y + (vue.survol.y - o) * z;
    ctx.save();
    ctx.lineWidth = 1; ctx.strokeStyle = '#000'; ctx.strokeRect(x0 - 0.5, y0 - 0.5, n * z + 1, n * z + 1);
    ctx.strokeStyle = '#fff'; ctx.strokeRect(x0 + 0.5, y0 + 0.5, n * z - 1, n * z - 1);
    ctx.restore();
  }

  apercus(d, f);
  hud();
}

/* ---------- Aperçus ×1 et ×2 (image d'export, sans construction ni référence) ---------- */
let apercuCle = '';
function apercus(d, f) {
  const a = $('#apercu'); if (!a || a.classList.contains('replie')) return;
  const px = AP.compose(d, f, 'export');
  const c1 = $('#apercu-1'), c2 = $('#apercu-2');
  U.pxVersCanvas(c1, px, d.w, d.h); U.pxVersCanvas(c2, px, d.w, d.h);
  const cle = d.w + 'x' + d.h;
  if (cle !== apercuCle) {
    apercuCle = cle;
    const big = Math.max(d.w, d.h) > 96;
    c1.style.width = d.w + 'px'; c1.style.height = d.h + 'px';
    c2.style.width = d.w * 2 + 'px'; c2.style.height = d.h * 2 + 'px';
    c2.parentElement.hidden = big;
  }
}

/* ---------- HUD ---------- */
function hud() {
  const at = U.at, el = $('#hud'); if (!el) return;
  const d = at.doc, p = vue.survol;
  const parts = [];
  if (p && at.dans(p.x, p.y)) {
    const c = at.pixel(p.x, p.y, 'export');
    parts.push(h('span.puce', p.x + ',' + p.y));
    parts.push(h('span.puce', h('i', { style: { display: 'inline-block', width: '10px', height: '10px', borderRadius: '2px', background: c >>> 24 ? AP.hex(c) : 'transparent', border: '1px solid var(--line-2)' } }), c >>> 24 ? AP.hex(c) : 'vide'));
  }
  parts.push(h('span.puce', d.w + '×' + d.h));
  const n = AP.couleursUtilisees(AP.compose(d, at.s.image, 'export')).size, b = AP.budgetPourTaille(d.w, d.h);
  parts.push(h('span.puce' + (n > b.total ? '.err' : n > b.total * 0.85 ? '.att' : '.ok'), n + (b.total < Infinity ? '/' + b.total : '') + ' coul.'));
  if (d.images.length > 1) parts.push(h('span.puce', 'img ' + (at.s.image + 1) + '/' + d.images.length));
  const c = at.calque; if (c) parts.push(h('span.puce' + (c.verrou || !c.visible ? '.err' : ''), c.nom + (c.type !== 'normal' ? ' · ' + c.type : '')));
  el.replaceChildren(...parts);
}

/* ---------- Alerte de porte (refus visible sur la toile) ---------- */
let alerteT = 0;
function alertePorte(msg) {
  const a = $('#alerte-porte'); if (!a) return;
  a.textContent = msg; a.hidden = false;
  clearTimeout(alerteT); alerteT = setTimeout(() => { a.hidden = true; }, 4500);
}
U.alertePorte = alertePorte;

/* ---------- Saisie pointeur ---------- */
const pointeurs = new Map();
let geste = null;        // { type:'dessin'|'pan'|'pinch'|'attente', ... }
let espace = false;
const mods = e => (e.shiftKey ? 1 : 0) | (e.altKey ? 2 : 0) | ((e.ctrlKey || e.metaKey) ? 4 : 0);

function envoie(type, cx, cy, b, m) {
  const p = ecranVersCellule(cx, cy);
  const r = U.at.input({ type, x: p.x, y: p.y, b, m });
  if (r && r.refus) alertePorte(r.refus);
  return r;
}
function survole(cx, cy) {
  const p = ecranVersCellule(cx, cy);
  const n = { x: Math.floor(p.x), y: Math.floor(p.y) };
  if (!vue.survol || vue.survol.x !== n.x || vue.survol.y !== n.y) { vue.survol = n; redessine(); }
}

function bas(e) {
  if (U.modaleOuverte) return;
  cv.setPointerCapture && cv.setPointerCapture(e.pointerId);
  pointeurs.set(e.pointerId, { x: e.clientX, y: e.clientY, x0: e.clientX, y0: e.clientY, t0: performance.now(), type: e.pointerType });
  e.preventDefault();
  if (e.pointerType === 'touch') return basTactile(e);
  if (e.button === 1 || espace) { geste = { type: 'pan', x: e.clientX, y: e.clientY, ox: vue.ox, oy: vue.oy }; scene.classList.add('tient'); return; }
  const b = e.button === 2 ? 2 : 0;
  geste = { type: 'dessin', b };
  envoie('down', e.clientX, e.clientY, b, mods(e));
  redessine();
}
function bouge(e) {
  const p = pointeurs.get(e.pointerId);
  if (p) { p.x = e.clientX; p.y = e.clientY; }
  if (e.pointerType === 'touch') return bougeTactile(e);
  survole(e.clientX, e.clientY);
  if (!geste) return;
  if (geste.type === 'pan') { vue.ox = geste.ox + e.clientX - geste.x; vue.oy = geste.oy + e.clientY - geste.y; redessine(); return; }
  if (geste.type === 'dessin') envoie('move', e.clientX, e.clientY, geste.b, mods(e));
}
function haut(e) {
  const p = pointeurs.get(e.pointerId);
  pointeurs.delete(e.pointerId);
  if (e.pointerType === 'touch') return hautTactile(e, p);
  if (!geste) return;
  if (geste.type === 'dessin') envoie('up', e.clientX, e.clientY, geste.b, mods(e));
  scene.classList.remove('tient');
  geste = null; redessine();
}
function annule(e) {
  pointeurs.delete(e.pointerId);
  if (geste && geste.type === 'dessin') U.at.input({ type: 'cancel', x: 0, y: 0 });
  geste = null; scene.classList.remove('tient'); redessine();
}

/* ---------- Tactile : 1 doigt dessine, 2 doigts zooment/déplacent,
 * tape à 2 doigts = annuler, à 3 doigts = refaire, appui long = pipette,
 * mode précision : le curseur suit le doigt décalé, on trace avec le bouton. ---------- */
let appuiLong = 0, tapes = null;
const precision = () => document.getElementById('app').classList.contains('tactile-precision');
const DECALAGE = 56;

function basTactile(e) {
  const n = pointeurs.size;
  if (n === 1) tapes = { max: 1, t0: performance.now(), bouge: false };
  else if (tapes) tapes.max = Math.max(tapes.max, n);
  if (precision()) { geste = { type: 'viseur' }; viseur(e.clientX, e.clientY); return; }
  if (n === 1) {
    geste = { type: 'attente', x: e.clientX, y: e.clientY, id: e.pointerId };
    clearTimeout(appuiLong);
    appuiLong = setTimeout(() => {
      if (geste && (geste.type === 'attente' || (geste.type === 'dessin' && geste.court))) {
        if (geste.type === 'dessin') U.at.input({ type: 'cancel', x: 0, y: 0 });
        const p = ecranVersCellule(geste.x, geste.y);
        U.at.input({ type: 'down', x: p.x, y: p.y, b: 0, m: 2 }); U.at.input({ type: 'up', x: p.x, y: p.y, b: 0, m: 2 });
        U.toast('Pipette : ' + AP.hex(U.at.s.c1), 'info', 1200);
        geste = { type: 'fini' };
      }
    }, 520);
    return;
  }
  // 2 doigts ou plus : on abandonne le trait commencé
  clearTimeout(appuiLong);
  if (geste && geste.type === 'dessin') U.at.input({ type: 'cancel', x: 0, y: 0 });
  const [a, b] = [...pointeurs.values()];
  geste = { type: 'pinch', d0: Math.hypot(a.x - b.x, a.y - b.y), z0: vue.zoom, cx: (a.x + b.x) / 2, cy: (a.y + b.y) / 2, ox: vue.ox, oy: vue.oy };
  redessine();
}
function demarreDessin() {
  const g = geste; clearTimeout(appuiLong);
  geste = { type: 'dessin', b: 0, court: true, x: g.x, y: g.y };
  envoie('down', g.x, g.y, 0, 0);
}
function bougeTactile(e) {
  if (!geste) return;
  const p = pointeurs.get(e.pointerId);
  if (p && tapes && Math.hypot(p.x - p.x0, p.y - p.y0) > 10) tapes.bouge = true;
  if (geste.type === 'viseur') { viseur(e.clientX, e.clientY); return; }
  if (geste.type === 'attente') {
    if (Math.hypot(e.clientX - geste.x, e.clientY - geste.y) > 4 || performance.now() - p.t0 > 90) demarreDessin();
    else return;
  }
  if (geste.type === 'dessin') { geste.court = false; clearTimeout(appuiLong); envoie('move', e.clientX, e.clientY, 0, 0); survole(e.clientX, e.clientY); return; }
  if (geste.type === 'pinch' && pointeurs.size >= 2) {
    const [a, b] = [...pointeurs.values()];
    const dd = Math.hypot(a.x - b.x, a.y - b.y), cx = (a.x + b.x) / 2, cy = (a.y + b.y) / 2;
    const cible = geste.z0 * dd / Math.max(1, geste.d0);
    let z = ZOOMS[0]; for (const zz of ZOOMS) if (zz <= cible * 1.08) z = zz;
    const r = cv.getBoundingClientRect();
    const dx = (geste.cx - r.left - geste.ox) / geste.z0, dy = (geste.cy - r.top - geste.oy) / geste.z0;
    vue.zoom = z; vue.ox = Math.round(cx - r.left - dx * z); vue.oy = Math.round(cy - r.top - dy * z);
    majZoom(); redessine();
  }
}
function hautTactile(e, p) {
  clearTimeout(appuiLong);
  if (geste && geste.type === 'attente') { demarreDessin(); }
  if (geste && geste.type === 'dessin') envoie('up', e.clientX, e.clientY, 0, 0);
  if (pointeurs.size === 0) {
    if (tapes && !tapes.bouge && performance.now() - tapes.t0 < 320) {
      if (tapes.max === 2) { U.act('annule'); }
      else if (tapes.max >= 3) { U.act('refait'); }
    }
    tapes = null;
    if (geste && geste.type !== 'viseur') geste = null;
    if (geste && geste.type === 'viseur') geste = null;
  } else if (geste && geste.type === 'pinch' && pointeurs.size === 1) geste = { type: 'fini' };
  redessine();
}
// mode précision
let viseurPos = null, traceViseur = null;
function viseur(cx, cy) {
  viseurPos = { x: cx, y: cy - DECALAGE };
  survole(viseurPos.x, viseurPos.y);
  if (traceViseur) envoie('move', viseurPos.x, viseurPos.y, traceViseur.b, 0);
}
function boutonPrecision(btn, b) {
  btn.addEventListener('pointerdown', e => {
    e.preventDefault(); if (!viseurPos) return;
    traceViseur = { b }; envoie('down', viseurPos.x, viseurPos.y, b, 0); redessine();
  });
  const fin = () => { if (!traceViseur) return; envoie('up', viseurPos.x, viseurPos.y, traceViseur.b, 0); traceViseur = null; redessine(); };
  btn.addEventListener('pointerup', fin); btn.addEventListener('pointercancel', fin); btn.addEventListener('pointerleave', fin);
}

/* ---------- Molette ---------- */
function molette(e) {
  e.preventDefault();
  if (e.ctrlKey || Math.abs(e.deltaY) >= Math.abs(e.deltaX) && !e.shiftKey) {
    const acc = (molette.acc = (molette.acc || 0) + e.deltaY);
    if (Math.abs(acc) < (e.ctrlKey ? 18 : 40)) return;
    molette.acc = 0;
    zoomPas(acc < 0 ? 1 : -1, e.clientX, e.clientY);
  } else { vue.ox -= e.deltaX || e.deltaY; redessine(); }
}

/* ---------- Clavier ---------- */
const RACCOURCIS = {
  b: 'crayon', e: 'gomme', l: 'ligne', r: 'rect', o: 'ellipse', g: 'seau', i: 'pipette',
  m: 'selrect', q: 'lasso', w: 'baguette', v: 'deplace', s: 'ombrage', h: 'remplace', d: 'degrade'
};
U.RACCOURCIS = RACCOURCIS;
function saisieTexte(t) { return t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' || t.tagName === 'SELECT' || t.isContentEditable); }
function clavier(e) {
  if (saisieTexte(e.target)) { if (e.key === 'Escape') e.target.blur(); return; }
  if (U.modaleOuverte) { if (e.key === 'Escape') U.ferme(); return; }
  const k = e.key.toLowerCase(), ctrl = e.ctrlKey || e.metaKey;
  if (e.key === ' ') { if (!espace) { espace = true; scene.classList.add('pan'); } e.preventDefault(); return; }
  if (ctrl && k === 'z') { e.preventDefault(); U.act(e.shiftKey ? 'refait' : 'annule'); return; }
  if (ctrl && k === 'y') { e.preventDefault(); U.act('refait'); return; }
  if (ctrl && k === 's') { e.preventDefault(); U.enregistreProjet && U.enregistreProjet(); return; }
  if (ctrl && k === 'a') { e.preventDefault(); U.act('selection.tout'); return; }
  if (ctrl && k === 'd') { e.preventDefault(); U.act('selection.rien'); return; }
  if (ctrl && k === 'i') { e.preventDefault(); U.act('selection.inverse'); return; }
  if (ctrl) return;
  if (e.key === 'Escape') { U.fermeMenu(); if (U.at.s.selection) U.act('selection.rien'); U.marques = null; redessine(); return; }
  if (e.key === 'Delete' || e.key === 'Backspace') { e.preventDefault(); U.act('efface'); return; }
  if (e.key === '+' || e.key === '=') { zoomPas(1); return; }
  if (e.key === '-' || e.key === '_') { zoomPas(-1); return; }
  if (e.key === '0') { ajuste(); return; }
  if (k === 'x') { U.act('couleur.echange'); return; }
  if (e.key === '[') { U.act('option', { cle: 'taille', valeur: U.at.s.taille - 1 }); return; }
  if (e.key === ']') { U.act('option', { cle: 'taille', valeur: U.at.s.taille + 1 }); return; }
  if (e.key === ',') { const i = U.at.s.image; if (i > 0) U.act('image.choisit', { i: i - 1 }); return; }
  if (e.key === '.') { const i = U.at.s.image; if (i < U.at.doc.images.length - 1) U.act('image.choisit', { i: i + 1 }); return; }
  if (k === 'n' && e.shiftKey) { U.act('calque.ajoute', {}); return; }
  if (e.key === 'Enter' && U.joue) { U.joue(); return; }
  if (k === "'" || k === '#') { vue.grille = !vue.grille; redessine(); return; }
  if (k === 'k') { U.act('option', { cle: 'symX', valeur: !U.at.s.symX }); return; }
  if (RACCOURCIS[k] && !e.altKey) { U.act('outil', { nom: RACCOURCIS[k] }); return; }
}
function clavierHaut(e) { if (e.key === ' ') { espace = false; scene.classList.remove('pan'); } }

/* ---------- Curseur visible du mode Claude (pour la vidéo) ---------- */
let curseur = null;
function initCurseurClaude() {
  curseur = h('div.curseur-claude', { html: '<svg viewBox="0 0 22 22" width="22" height="22"><path d="M2 2 L2 18 L6.5 14 L9.5 20.5 L12.5 19 L9.6 12.8 L15.5 12.8 Z" fill="#b48cff" stroke="#140c1f" stroke-width="1.4" stroke-linejoin="round"/></svg>' });
  document.body.appendChild(curseur);
  const place = (x, y) => { curseur.style.transform = 'translate(' + (x - 2) + 'px,' + (y - 2) + 'px)'; };
  document.addEventListener('pointermove', e => place(e.clientX, e.clientY), true);
  document.addEventListener('pointerdown', e => {
    place(e.clientX, e.clientY);
    const a = h('div.anneau' + (e.button === 2 ? '.droit' : ''), { style: { left: e.clientX + 'px', top: e.clientY + 'px' } });
    document.body.appendChild(a); setTimeout(() => a.remove(), 600);
  }, true);
}

/* ---------- Initialisation ---------- */
function init() {
  scene = $('#scene'); cv = $('#toile'); ctx = cv.getContext('2d');
  buf = document.createElement('canvas'); bctx = buf.getContext('2d');
  cv.addEventListener('pointerdown', bas);
  cv.addEventListener('pointermove', bouge);
  cv.addEventListener('pointerup', haut);
  cv.addEventListener('pointercancel', annule);
  cv.addEventListener('pointerleave', e => { if (e.pointerType !== 'touch' && !geste) { vue.survol = null; redessine(); } });
  cv.addEventListener('contextmenu', e => e.preventDefault());
  cv.addEventListener('wheel', molette, { passive: false });
  document.addEventListener('keydown', clavier);
  document.addEventListener('keyup', clavierHaut);
  boutonPrecision($('#b-prec-1'), 0); boutonPrecision($('#b-prec-2'), 2);
  $('#b-apercu').addEventListener('click', () => {
    const a = $('#apercu'); a.classList.toggle('replie');
    $('#b-apercu').textContent = a.classList.contains('replie') ? '+' : '×';
    U.stocke.ecris('apercuReplie', a.classList.contains('replie')); redessine();
  });
  if (U.stocke.lis('apercuReplie', false)) { $('#apercu').classList.add('replie'); $('#b-apercu').textContent = '+'; }
  $('#b-zoom').addEventListener('click', ajuste);
  $('#b-zoom-plus').addEventListener('click', () => zoomPas(1));
  $('#b-dezoom').addEventListener('click', () => zoomPas(-1));
  if (typeof ResizeObserver !== 'undefined') new ResizeObserver(() => redessine()).observe(scene);
  else addEventListener('resize', redessine);
  if (U.claude) initCurseurClaude();
}
U.initScene = init;
})(window);
