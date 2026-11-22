/* Claude Pixel — interface : timeline d'animation, onglets Tuiles, Aide et Séance,
 * lecture seule pour la souris (window.claudePixel) et démarrage de l'application. */
(function (G) {
'use strict';
const AP = G.AP, U = AP.UI;
const { $, $$, h } = U;

const RENDUS = U.RENDUS = U.RENDUS || {};
const LEGERS = U.LEGERS = U.LEGERS || {};

/* ---------- Petits constructeurs (mêmes conventions que ui-panneaux) ---------- */
const titre = (txt, ...droite) => h('h3', h('span', txt), h('span.espace'), ...droite);
const btn = (txt, o = {}) => h('button.btn' + (o.cls || ''), {
  'data-cible': o.cible, title: o.title, 'aria-label': o.label, disabled: !!o.inactif,
  'aria-pressed': o.presse === undefined ? undefined : String(!!o.presse), on: { click: o.click }
}, txt);
function champ(type, valeur, o = {}) {
  let el;
  if (type === 'select') {
    el = h('select.champ', { 'data-cible': o.cible, 'aria-label': o.label });
    for (const op of o.options || []) {
      const [v, t] = Array.isArray(op) ? op : [op, op];
      el.appendChild(h('option', { value: String(v), selected: String(v) === String(valeur) }, t));
    }
  } else if (type === 'textarea') {
    el = h('textarea.champ', { rows: o.rows || 2, 'data-cible': o.cible, 'aria-label': o.label, placeholder: o.placeholder });
    el.value = valeur == null ? '' : valeur;
  } else {
    el = h('input' + (type === 'checkbox' ? '' : '.champ') + (type === 'number' ? '.mono' : ''), { type, 'data-cible': o.cible, 'aria-label': o.label, placeholder: o.placeholder,
      min: o.min, max: o.max, step: o.step });
    if (type === 'checkbox') el.checked = !!valeur; else el.value = valeur == null ? '' : valeur;
  }
  if (o.change) el.addEventListener('change', () => o.change(type === 'checkbox' ? el.checked : el.value, el));
  if (o.input) el.addEventListener('input', () => o.input(el.value, el));
  return el;
}
const caseACocher = (txt, valeur, o) => h('label.ligne', { style: { gap: '6px' } }, champ('checkbox', valeur, o), h('span', txt));
const sansAccent = s => String(s).normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();
const fmtTemps = ms => { const s = Math.max(0, Math.round(ms / 1000)); return Math.floor(s / 60) + ':' + String(s % 60).padStart(2, '0'); };


/* ======================================================================
 * LECTURE DE L'ANIMATION (aperçu seulement : rien n'est journalisé)
 * ==================================================================== */
let lecture = null; // { t, f0 }
function sequence() {
  const d = U.at.doc, f = U.at.s.image;
  const t = d.etiquettes.find(e => f >= e.de && f <= e.a);
  let L = [];
  if (t) {
    for (let i = t.de; i <= t.a; i++) L.push(i);
    if (t.sens === 'arriere') L.reverse();
    else if (t.sens === 'pingpong' && L.length > 2) L = L.concat(L.slice(1, -1).reverse());
  } else for (let i = 0; i < d.images.length; i++) L.push(i);
  return L;
}
function arreteLecture() {
  if (!lecture) return;
  clearTimeout(lecture.t);
  const f0 = lecture.f0; lecture = null;
  if (U.at.doc && f0 < U.at.doc.images.length) U.at.s.image = f0;
  U.redessine(); planifieTimeline();
}
U.joue = function () {
  if (lecture) { arreteLecture(); return; }
  const d = U.at.doc;
  if (d.images.length < 2) { U.toast('Une seule image : ajoute une image pour animer.', 'alerte'); return; }
  const L = sequence(); let k = 0;
  lecture = { f0: U.at.s.image, t: 0 };
  const pas = () => {
    if (!lecture) return;
    const f = L[k % L.length]; k++;
    U.at.s.image = f; U.redessine(); majActif();
    lecture.t = setTimeout(pas, (d.images[f] && d.images[f].ms) || 100);
  };
  pas(); planifieTimeline();
};
U.arreteLecture = arreteLecture;
Object.defineProperty(U, 'enLecture', { get: () => !!lecture });
/* Toute action arrête l'aperçu d'abord : l'image courante redevient celle du journal. */
const actBase = U.act;
U.act = function (nom, a) { if (lecture) arreteLecture(); return actBase(nom, a); };

/* ======================================================================
 * TIMELINE
 * ==================================================================== */
const COUL_ETIQ = ['#f2b84b', '#5ec8c0', '#8f6bd6', '#e0736a', '#7fb069', '#d68fd6'];
let tlRaf = 0, tlAttente = false;
function tlFocus() {
  const a = document.activeElement, t = $('#timeline');
  return a && t && t.contains(a) && /^(INPUT|SELECT|TEXTAREA)$/.test(a.tagName) && a.type !== 'checkbox';
}
function planifieTimeline() {
  if (tlRaf) return;
  tlRaf = requestAnimationFrame(() => { tlRaf = 0; if (tlFocus()) { tlAttente = true; return; } rendTimeline(); });
}
const celLie = (d, f) => d.calques.some(c => { const id = d.cels[c.id][f]; return id && d.cels[c.id].some((x, g) => g !== f && x === id); });
function miniature(cv, f) {
  const d = U.at.doc;
  U.pxVersCanvas(cv, AP.compose(d, f, 'export'), d.w, d.h);
}
function rendTimeline() {
  const tl = $('#timeline'); if (!tl || !U.at || !U.at.doc) return;
  tlAttente = false;
  const d = U.at.doc, f = U.at.s.image, n = d.images.length, im = d.images[f];
  const replie = !!U.stocke.lis('timelineRepliee', false);
  tl.classList.toggle('repliee', replie);
  const ancienne = $('.bande', tl), defil = ancienne ? ancienne.scrollLeft : 0;

  const ms = champ('number', im.ms, { min: 10, max: 10000, step: 1, cible: 'image-ms', label: 'Durée de l\'image en millisecondes',
    change: v => {
      let x = +v || 100;
      if (U.stocke.lis('snapMs', true)) x = Math.max(17, Math.round(Math.round(x / (1000 / 60)) * (1000 / 60)));
      U.act('image.info', { ms: x });
    } });
  ms.style.width = '74px';
  const ctrl = h('div.ctrl',
    btn(lecture ? '■' : '▶', { cls: '.ico' + (lecture ? '.prim' : ''), cible: 'joue', title: 'Lire l\'animation (Entrée)', label: lecture ? 'Arrêter la lecture' : 'Lire l\'animation', click: () => U.joue() }),
    h('span.mono', { style: { fontSize: '12px', minWidth: '38px', textAlign: 'center' }, 'data-cible': 'image-n' }, (f + 1) + '/' + n),
    btn('+', { cls: '.ico', cible: 'image-ajoute', title: 'Nouvelle image vide après celle-ci', label: 'Ajouter une image', click: () => U.act('image.ajoute') }),
    btn('Dupl.', { cible: 'image-duplique', title: 'Dupliquer l\'image (copie indépendante)', click: () => U.act('image.duplique', { lie: false }) }),
    btn('Liée', { cible: 'image-lie', title: 'Dupliquer en liant les cels (modifier l\'une modifie l\'autre)', click: () => U.act('image.duplique', { lie: true }) }),
    btn('✕', { cls: '.ico', cible: 'image-supprime', title: 'Supprimer l\'image', label: 'Supprimer l\'image', inactif: n < 2, click: () => U.act('image.supprime') }),
    btn('‹', { cls: '.ico', cible: 'image-recule', title: 'Déplacer l\'image vers la gauche', label: 'Déplacer à gauche', inactif: f === 0, click: () => U.act('image.deplace', { vers: f - 1 }) }),
    btn('›', { cls: '.ico', cible: 'image-avance', title: 'Déplacer l\'image vers la droite', label: 'Déplacer à droite', inactif: f === n - 1, click: () => U.act('image.deplace', { vers: f + 1 }) }),
    h('label.ligne', { style: { gap: '4px', fontSize: '12px' } }, ms, h('span', 'ms')),
    h('label.ligne', { style: { gap: '4px', fontSize: '12px' }, title: 'Arrondir aux images d\'un écran à 60 Hz (16,7 ms)' },
      champ('checkbox', U.stocke.lis('snapMs', true), { cible: 'snap-ms', change: v => U.stocke.ecris('snapMs', v) }), h('span', '60 Hz')),
    btn('Pelure', { cible: 'pelure', title: 'Pelure d\'oignon : image précédente en rouge, suivante en vert', presse: U.vue.pelure, click: () => { U.vue.pelure = !U.vue.pelure; U.redessine(); rendTimeline(); } }),
    btn('Étiq.', { cible: 'etiquettes', title: 'Étiquettes de boucle (avant, arrière, ping-pong)', click: modaleEtiquettes }),
    btn('Timing', { cible: 'feuille-timing', title: 'Feuille de timing (C13)', click: modaleTiming }),
    btn(replie ? '▴' : '▾', { cls: '.ico.fantome', cible: 'timeline-replie', title: replie ? 'Déplier la timeline' : 'Replier la timeline', label: replie ? 'Déplier' : 'Replier',
      click: () => { U.stocke.ecris('timelineRepliee', !replie); rendTimeline(); } })
  );
  const bande = h('div.bande', { role: 'listbox', 'aria-label': 'Images', 'data-cible': 'bande' });
  for (let g = 0; g < n; g++) {
    const cv = h('canvas.vide-damier'); miniature(cv, g);
    const el = h('div.image-t' + (g === f ? '.actif' : ''), { role: 'option', 'aria-selected': String(g === f), tabIndex: g === f ? 0 : -1,
      'data-cible': 'image-' + (g + 1), 'data-i': String(g), title: 'Image ' + (g + 1) + (d.images[g].role ? ' — ' + d.images[g].role : ''),
      on: { click: () => { if (g !== U.at.s.image || lecture) U.act('image.choisit', { i: g }); } } },
      cv, h('span.ms', d.images[g].ms + ' ms'));
    if (celLie(d, g)) el.appendChild(h('span.lie', { title: 'Cel liée à une autre image' }, '∞'));
    if (d.images[g].validee) el.appendChild(h('span.ok', { title: 'Image validée' }, '✓'));
    d.etiquettes.forEach((t, k) => {
      if (g >= t.de && g <= t.a) el.appendChild(h('span.etiq', { title: t.nom + ' (' + t.sens + ')', style: { background: COUL_ETIQ[k % COUL_ETIQ.length], top: (-2 + 4 * (k % 3)) + 'px' } }));
    });
    bande.appendChild(el);
  }
  bande.addEventListener('keydown', e => {
    if (e.key !== 'ArrowLeft' && e.key !== 'ArrowRight') return;
    e.preventDefault(); e.stopPropagation();
    const i = Math.max(0, Math.min(n - 1, U.at.s.image + (e.key === 'ArrowRight' ? 1 : -1)));
    if (i !== U.at.s.image) U.act('image.choisit', { i });
    setTimeout(() => { const a = $('.image-t.actif'); if (a) a.focus(); }, 30);
  });
  tl.replaceChildren(ctrl, bande);
  bande.scrollLeft = defil;
  montreActif(bande);
}
function montreActif(bande) {
  const a = $('.image-t.actif', bande); if (!a) return;
  const g = a.offsetLeft, l = a.offsetWidth;
  if (g < bande.scrollLeft) bande.scrollLeft = g - 4;
  else if (g + l > bande.scrollLeft + bande.clientWidth) bande.scrollLeft = g + l - bande.clientWidth + 4;
}
/* Pendant la lecture : on déplace seulement le cadre actif, sans reconstruire. */
function majActif() {
  const f = U.at.s.image;
  for (const el of $$('#timeline .image-t')) {
    const oui = +el.dataset.i === f;
    el.classList.toggle('actif', oui); el.setAttribute('aria-selected', String(oui));
  }
  const nb = $('#timeline [data-cible="image-n"]'); if (nb) nb.textContent = (f + 1) + '/' + U.at.doc.images.length;
  const b = $('#timeline .bande'); if (b) montreActif(b);
}
let miniT = 0, miniAttente = null;
function majMiniature() {
  const t = performance.now();
  if (t - miniT < 150) { if (!miniAttente) miniAttente = setTimeout(() => { miniAttente = null; majMiniature(); }, 160); return; }
  miniT = t;
  const f = U.at.s.image, cv = $('#timeline .image-t[data-i="' + f + '"] canvas');
  if (cv) miniature(cv, f);
  // les images liées partagent la cel : on les rafraîchit aussi
  for (const el of $$('#timeline .image-t')) { const g = +el.dataset.i; if (g !== f && el.querySelector('.lie')) miniature(el.querySelector('canvas'), g); }
}

function modaleEtiquettes() {
  const d = U.at.doc, n = d.images.length;
  const liste = h('div.pile');
  const remplit = () => {
    liste.replaceChildren();
    if (!d.etiquettes.length) liste.appendChild(h('p.aide-txt', 'Aucune étiquette. Une étiquette nomme une boucle (marche, idle…) et fixe son sens de lecture.'));
    d.etiquettes.forEach((t, k) => liste.appendChild(h('div.ligne', { style: { gap: '8px' } },
      h('span', { style: { width: '10px', height: '10px', borderRadius: '2px', background: COUL_ETIQ[k % COUL_ETIQ.length], flex: 'none' } }),
      h('span', { style: { flex: '1' } }, h('b', t.nom), ' · images ' + (t.de + 1) + ' à ' + (t.a + 1) + ' · ' + ({ avant: 'avant', arriere: 'arrière', pingpong: 'ping-pong' }[t.sens] || t.sens)),
      btn('Supprimer', { cls: '.fantome.danger', cible: 'etiquette-supprime-' + (k + 1), click: () => { U.act('etiquette.supprime', { i: k }); remplit(); } }))));
  };
  remplit();
  const nom = champ('text', 'boucle', { cible: 'etiquette-nom', label: 'Nom' });
  const de = champ('number', 1, { min: 1, max: n, cible: 'etiquette-de', label: 'De' });
  const a = champ('number', n, { min: 1, max: n, cible: 'etiquette-a', label: 'À' });
  const sens = champ('select', 'avant', { options: [['avant', 'Avant'], ['arriere', 'Arrière'], ['pingpong', 'Ping-pong']], cible: 'etiquette-sens', label: 'Sens' });
  const ajoute = btn('Ajouter', { cls: '.prim', cible: 'etiquette-ajoute', click: () => {
    const x = Math.max(1, Math.min(n, +de.value | 0)), y = Math.max(1, Math.min(n, +a.value | 0));
    U.act('etiquette.ajoute', { nom: nom.value.trim() || 'boucle', de: Math.min(x, y) - 1, a: Math.max(x, y) - 1, sens: sens.value });
    remplit();
  } });
  const corps = h('div.pile', liste, h('hr'),
    h('div.grille2', h('label', 'Nom', nom), h('label', 'Sens', sens)),
    h('div.grille2', h('label', 'De l\'image', de), h('label', 'À l\'image', a)),
    h('div.ligne', ajoute),
    h('p.aide-txt', 'La lecture (Entrée) boucle sur l\'étiquette qui contient l\'image courante.'));
  U.modale('Étiquettes de boucle', corps, [{ txt: 'Fermer', valeur: true, prim: true, cible: 'oui' }]);
}

function modaleTiming() {
  const d = U.at.doc;
  const table = h('table.tableau.feuille-timing', h('thead', h('tr', h('th', '#'), h('th', 'ms'), h('th', 'Rôle'), h('th', 'Ce qui change'), h('th', 'Principe'), h('th', 'Validée'))));
  const corps = h('tbody'); table.appendChild(corps);
  const ROLES = [['', '—'], ['cle', 'Clé'], ['extreme', 'Extrême'], ['passage', 'Passage'], ['intervalle', 'Intervalle'], ['contact', 'Contact'], ['impact', 'Impact'], ['tenue', 'Tenue']];
  d.images.forEach((im, i) => {
    const ligne = (cle, el) => { el.addEventListener('change', () => U.act('image.info', { i, [cle]: el.type === 'checkbox' ? el.checked : (cle === 'ms' ? +el.value || 100 : el.value) })); return el; };
    corps.appendChild(h('tr',
      h('td.mono', String(i + 1)),
      h('td', ligne('ms', champ('number', im.ms, { min: 10, max: 10000, cible: 'timing-ms-' + (i + 1), label: 'ms image ' + (i + 1) }))),
      h('td', ligne('role', champ('select', im.role, { options: ROLES.some(r => r[0] === im.role) ? ROLES : ROLES.concat([[im.role, im.role]]), cible: 'timing-role-' + (i + 1), label: 'Rôle image ' + (i + 1) }))),
      h('td', ligne('change', champ('text', im.change, { cible: 'timing-change-' + (i + 1), label: 'Ce qui change, image ' + (i + 1) }))),
      h('td', ligne('principe', champ('text', im.principe, { cible: 'timing-principe-' + (i + 1), label: 'Principe, image ' + (i + 1), placeholder: 'anticipation, tassement…' }))),
      h('td', ligne('validee', champ('checkbox', im.validee, { cible: 'timing-validee-' + (i + 1), label: 'Image ' + (i + 1) + ' validée' })))));
  });
  const total = d.images.reduce((s, im) => s + im.ms, 0);
  U.modale('Feuille de timing', h('div.pile',
    h('p.aide-txt', 'Une ligne par image (C13). Total : ' + total + ' ms, soit ' + (1000 * d.images.length / Math.max(1, total)).toFixed(1) + ' images par seconde en moyenne.'),
    h('div', { style: { overflowX: 'auto' } }, table)),
  [{ txt: 'Fermer', valeur: true, prim: true, cible: 'oui' }], { large: true });
}

function initTimeline() {
  U.at.ecoute(q => {
    if (q === 'pixels' || q === 'trait') { if (!lecture) majMiniature(); return; }
    if (q === 'act' && lecture) arreteLecture();
    if (q === 'doc' || q === 'etat' || q === 'act') { if (!lecture) planifieTimeline(); }
  });
  $('#timeline').addEventListener('focusout', () => setTimeout(() => { if (tlAttente && !tlFocus()) rendTimeline(); }, 0));
  // Dessiner pendant la lecture désynchroniserait le journal : on arrête d'abord.
  document.addEventListener('pointerdown', e => {
    if (lecture && !(e.target.closest && e.target.closest('[data-cible="joue"]'))) arreteLecture();
  }, true);
  document.addEventListener('keydown', e => { if (lecture && e.key !== 'Enter') arreteLecture(); }, true);
  const b = $('#b-images');
  if (b) b.addEventListener('click', () => {
    const app = $('#app'), oui = !app.classList.contains('timeline-tel');
    app.classList.toggle('timeline-tel', oui); b.setAttribute('aria-expanded', String(oui));
  });
  rendTimeline();
}

/* ======================================================================
 * TUILES : réglage, raccords, carte de test (autotile), parallaxe
 * ==================================================================== */
const tu = { mode: 'terrain', tuile: 0, attente: new Map(), carteCv: null, paraCv: null, vit: {}, paraJoue: false, paraT: 0, paraRaf: 0 };
function tailleTuile(d) { return d.tuile.on ? { tw: d.tuile.tw, th: d.tuile.th } : { tw: d.w, th: d.h }; }
function docCanvas(d) {
  const c = document.createElement('canvas');
  return U.pxVersCanvas(c, AP.compose(d, U.at.s.image, 'export'), d.w, d.h);
}
function dessineCarte() {
  const cv = tu.carteCv; if (!cv || !cv.isConnected) return;
  const d = U.at.doc, c = d.carte, { tw, th } = tailleTuile(d);
  if (cv.width !== c.cols * tw || cv.height !== c.rows * th) { cv.width = c.cols * tw; cv.height = c.rows * th; }
  const x = cv.getContext('2d'); x.imageSmoothingEnabled = false; x.clearRect(0, 0, cv.width, cv.height);
  const src = docCanvas(d);
  const nx = Math.max(1, Math.floor(d.w / tw));
  const gabarit = d.tuile.on && d.w >= 5 * tw && d.h >= 3 * th;
  const valeur = (tab, i) => { const k = i + ''; return tu.attente.has(k) && tab in tu.attente.get(k) ? tu.attente.get(k)[tab] : (c[tab][i] | 0); };
  const ter = (X, Y) => X < 0 || Y < 0 || X >= c.cols || Y >= c.rows ? 0 : valeur('terrain', Y * c.cols + X);
  const hw = tw / 2, hh = th / 2;
  for (let Y = 0; Y < c.rows; Y++) for (let X = 0; X < c.cols; X++) {
    const i = Y * c.cols + X, t = valeur('tuiles', i);
    if (t > 0) { const k = t - 1; x.drawImage(src, (k % nx) * tw, Math.floor(k / nx) * th, tw, th, X * tw, Y * th, tw, th); }
    if (!ter(X, Y)) continue;
    if (!gabarit) { x.drawImage(src, 0, 0, tw, th, X * tw, Y * th, tw, th); continue; }
    const n = ter(X, Y - 1), e = ter(X + 1, Y), s = ter(X, Y + 1), w = ter(X - 1, Y);
    const ne = ter(X + 1, Y - 1), se = ter(X + 1, Y + 1), sw = ter(X - 1, Y + 1), nw = ter(X - 1, Y - 1);
    for (let q = 0; q < 4; q++) {
      const [tx, ty] = AP.quartAutotile(n, e, s, w, ne, se, sw, nw, q);
      const ox = (q & 1) * hw, oy = (q >> 1) * hh;
      x.drawImage(src, tx * tw + ox, ty * th + oy, hw, hh, X * tw + ox, Y * th + oy, hw, hh);
    }
  }
}
function brancheCarte(cv) {
  let bas = false, dernier = '';
  const cellule = e => {
    const r = cv.getBoundingClientRect(), c = U.at.doc.carte;
    return { x: Math.floor((e.clientX - r.left) / r.width * c.cols), y: Math.floor((e.clientY - r.top) / r.height * c.rows) };
  };
  const peint = e => {
    const { x, y } = cellule(e), c = U.at.doc.carte;
    if (x < 0 || y < 0 || x >= c.cols || y >= c.rows) return;
    const k = String(y * c.cols + x); if (k === dernier) return; dernier = k;
    const v = tu.mode === 'terrain' ? { terrain: 1 } : tu.mode === 'tuile' ? { tuile: tu.tuile + 1 } : { terrain: 0, tuile: 0 };
    tu.attente.set(k, Object.assign({ x, y }, tu.attente.get(k) || {}, v === undefined ? {} : (tu.mode === 'terrain' ? { terrain: 1 } : tu.mode === 'tuile' ? { tuiles: tu.tuile + 1 } : { terrain: 0, tuiles: 0 })));
    dessineCarte();
  };
  const fin = () => {
    if (!bas) return; bas = false; dernier = '';
    const L = [...tu.attente.values()]; tu.attente.clear();
    for (const p of L) {
      const a = { x: p.x, y: p.y };
      if ('terrain' in p) a.terrain = p.terrain;
      if ('tuiles' in p) a.tuile = p.tuiles;
      U.at.act('carte.peint', a);
    }
  };
  cv.addEventListener('pointerdown', e => { if (e.button > 0) return; bas = true; try { cv.setPointerCapture(e.pointerId); } catch (x) { /* rien */ } peint(e); e.preventDefault(); });
  cv.addEventListener('pointermove', e => { if (bas) peint(e); });
  cv.addEventListener('pointerup', fin); cv.addEventListener('pointercancel', fin); cv.addEventListener('lostpointercapture', fin);
}
function calquesPara(d) {
  const f = U.at.s.image;
  return d.calques.map((c, i) => ({ c, i, id: d.cels[c.id][f] })).filter(o => o.c.visible && o.c.type === 'normal' && o.id && d.celData[o.id]);
}
function raccordH(px, w, h) {
  let casse = 0, interne = 0, ni = 0;
  for (let y = 0; y < h; y++) {
    if (px[y * w] !== px[y * w + w - 1]) casse++;
    for (let x = 0; x < w - 1; x++) { if (px[y * w + x] !== px[y * w + x + 1]) interne++; ni++; }
  }
  const ref = ni ? interne / ni : 0, part = h ? casse / h : 0;
  return { casse, part, ref, mauvais: part > ref * 1.8 + 0.1 };
}
function dessinePara() {
  const cv = tu.paraCv; if (!cv || !cv.isConnected) { tu.paraJoue = false; return; }
  const d = U.at.doc, W = d.w * 2, H = d.h;
  if (cv.width !== W || cv.height !== H) { cv.width = W; cv.height = H; }
  const x = cv.getContext('2d'); x.imageSmoothingEnabled = false;
  x.fillStyle = U.couleurToken('--stage'); x.fillRect(0, 0, W, H);
  const tmp = document.createElement('canvas');
  for (const o of calquesPara(d)) {
    U.pxVersCanvas(tmp, d.celData[o.id], d.w, d.h);
    const v = tu.vit[o.c.id] !== undefined ? tu.vit[o.c.id] : Math.min(4, o.i);
    const dec = ((Math.floor(tu.paraT * v) % d.w) + d.w) % d.w;
    x.globalAlpha = (o.c.opacite == null ? 100 : o.c.opacite) / 100;
    for (let k = -1; k < 3; k++) x.drawImage(tmp, k * d.w - dec, 0);
    x.globalAlpha = 1;
  }
}
function bouclePara() {
  if (!tu.paraJoue) return;
  tu.paraT += 1; dessinePara();
  if (!tu.paraJoue) return;
  tu.paraRaf = setTimeout(bouclePara, 100);
}
RENDUS.tuiles = c => {
  const d = U.at.doc, t = d.tuile, { tw, th } = tailleTuile(d);
  c.appendChild(titre('Tuiles et décor'));
  c.appendChild(h('p.aide-txt', 'Décor : une tuile 16×16 ou 32×32 par toile, ou un gabarit de 5×3 tuiles pour l\'autotile (B6-A, A5-8c).'));
  const L = h('div.pile');
  L.appendChild(caseACocher('Mode tuile (répétition et raccords)', t.on, { cible: 'tuile-on', change: v => U.act('tuile.reglage', { on: v }) }));
  L.appendChild(h('div.grille2',
    h('label', 'Largeur de tuile', champ('number', t.tw, { min: 4, max: 128, cible: 'tuile-tw', change: v => U.act('tuile.reglage', { tw: +v }) })),
    h('label', 'Hauteur de tuile', champ('number', t.th, { min: 4, max: 128, cible: 'tuile-th', change: v => U.act('tuile.reglage', { th: +v }) }))));
  L.appendChild(caseACocher('Vue 3×3 sur la toile', U.vue.vue3x3, { cible: 'tuile-3x3', change: v => { U.vue.vue3x3 = v; U.redessine(); } }));
  c.appendChild(L);

  if (t.on) {
    const r = AP.DETECT.raccords(AP.compose(d, U.at.s.image, 'export'), d.w, d.h, t.tw, t.th);
    const pc = x => Math.round(x * 100) + ' %';
    const mauvais = r.pts.length > 0;
    c.appendChild(h('div.etape-carte', { 'data-cible': 'raccords' },
      h('b', mauvais ? 'Raccords à reprendre' : 'Raccords cohérents'),
      h('p.aide-txt', 'Bords qui ne se répondent pas : ' + pc(r.part) + ' (variation interne de référence : ' + pc(r.ref) + ').'),
      mauvais ? btn('Montrer sur la toile', { cible: 'raccords-montre', click: () => { U.marques = { pixels: r.pts, niveau: 'attention' }; U.redessine(); } }) : null));
  }

  /* carte de test */
  c.appendChild(titre('Carte de test', btn('Vider', { cls: '.fantome', cible: 'carte-efface', click: () => U.act('carte.efface') })));
  if (d.carte.cols * tw > 2560 || d.carte.rows * th > 1536) {
    c.appendChild(h('p.aide-txt', 'Toile trop grande pour la carte : active le mode tuile avec des tuiles de 128 px au plus.'));
  } else {
    const gabarit = t.on && d.w >= 5 * tw && d.h >= 3 * th;
    c.appendChild(h('p.aide-txt', gabarit ? 'Terrain : autotile par quarts depuis le gabarit 5×3 (centre en 2e colonne, coins intérieurs en colonnes 4 et 5).'
      : 'Terrain : la ' + (t.on ? 'première tuile' : 'toile entière') + ' sert de motif. Un gabarit 5×3 tuiles active l\'autotile.'));
    const modes = h('div.mods', { role: 'group', 'aria-label': 'Pinceau de carte' });
    for (const [m, txt] of [['terrain', 'Terrain'], ['tuile', 'Tuile'], ['gomme', 'Gomme']]) {
      modes.appendChild(btn(txt, { cible: 'carte-' + m, presse: tu.mode === m, click: () => { tu.mode = m; U.rendPanneau(true); } }));
    }
    c.appendChild(modes);
    if (tu.mode === 'tuile') {
      const nx = Math.max(1, Math.floor(d.w / tw)), ny = Math.max(1, Math.floor(d.h / th)), src = docCanvas(d);
      const jeu = h('div.jeu-tuiles', { 'data-cible': 'jeu-tuiles' });
      const ech = Math.max(1, Math.floor(32 / Math.max(tw, th)));
      for (let k = 0; k < Math.min(nx * ny, 64); k++) {
        const m = h('canvas', { width: tw, height: th, style: { width: tw * ech + 'px', height: th * ech + 'px' } });
        m.getContext('2d').drawImage(src, (k % nx) * tw, Math.floor(k / nx) * th, tw, th, 0, 0, tw, th);
        jeu.appendChild(h('button', { 'aria-pressed': String(tu.tuile === k), 'data-cible': 'tuile-' + (k + 1), title: 'Tuile ' + (k + 1), on: { click: () => { tu.tuile = k; U.rendPanneau(true); } } }, m));
      }
      c.appendChild(jeu);
    }
    const cv = h('canvas.carte-tuiles', { 'data-cible': 'carte' });
    tu.carteCv = cv; brancheCarte(cv);
    c.appendChild(cv); dessineCarte();
  }

  /* parallaxe */
  const couches = calquesPara(d);
  c.appendChild(titre('Parallaxe', couches.length ? btn(tu.paraJoue ? 'Pause' : 'Lire', { cible: 'para-joue', presse: tu.paraJoue, click: () => {
    tu.paraJoue = !tu.paraJoue; clearTimeout(tu.paraRaf); if (tu.paraJoue) bouclePara(); U.rendPanneau(true);
  } }) : null));
  if (!couches.length) { c.appendChild(h('p.aide-txt', 'Chaque calque visible (hors construction et référence) devient une couche qui défile en boucle.')); return; }
  const pcv = h('canvas.carte-tuiles', { 'data-cible': 'parallaxe', style: { cursor: 'default' } });
  tu.paraCv = pcv; c.appendChild(pcv); dessinePara();
  const tab = h('div.pile');
  for (const o of couches) {
    const v = tu.vit[o.c.id] !== undefined ? tu.vit[o.c.id] : Math.min(4, o.i);
    const rh = raccordH(d.celData[o.id], d.w, d.h);
    tab.appendChild(h('div.ligne', { style: { gap: '8px' } },
      h('span', { style: { flex: '1', minWidth: '0' } }, o.c.nom),
      h('label.ligne', { style: { gap: '4px', fontSize: '12px' } }, 'vitesse',
        champ('number', v, { min: 0, max: 4, step: 1, cible: 'para-vitesse-' + (o.i + 1), label: 'Vitesse de ' + o.c.nom, change: x => { tu.vit[o.c.id] = Math.max(0, Math.min(4, x | 0)); dessinePara(); } })),
      h('span.badge', { title: 'Raccord horizontal : colonne 1 contre dernière colonne' }, rh.mauvais ? rh.casse + ' raccord(s) cassé(s)' : 'boucle propre')));
  }
  c.appendChild(tab);
};
LEGERS.tuiles = () => { dessineCarte(); dessinePara(); };

/* ======================================================================
 * AIDE : la méthode complète, contextualisée, avec recherche
 * ==================================================================== */
let IDX = null; // { lignes, titres:[{l, niveau, txt, code, fin}], parCode:{}, regles }
function indexe() {
  if (IDX || !AP.DOC_METHODE) return IDX;
  const lignes = AP.DOC_METHODE.split('\n'), titres = [];
  let fence = false, h2 = null;
  lignes.forEach((ln, l) => {
    if (/^\s*```/.test(ln)) { fence = !fence; return; }
    if (fence) return;
    const m = /^(#{1,4})\s+(.+?)\s*#*\s*$/.exec(ln); if (!m) return;
    const niveau = m[1].length, txt = m[2];
    let code = null;
    if (niveau === 1) h2 = null;
    if (niveau === 2) { const c = /^([A-F]\d+b?)\./.exec(txt); h2 = c ? c[1] : null; code = h2; }
    if (niveau === 3 && h2) { const c = /^([A-Z]\d*b?|\d+[a-z]?)\./.exec(txt); code = c ? h2 + '-' + c[1] : null; }
    titres.push({ l, niveau, txt, code });
  });
  titres.forEach((t, k) => {
    let fin = lignes.length;
    for (let j = k + 1; j < titres.length; j++) if (titres[j].niveau <= t.niveau) { fin = titres[j].l; break; }
    t.fin = fin; t.k = k;
    t.feuilleFin = k + 1 < titres.length ? titres[k + 1].l : lignes.length;
  });
  const parCode = {};
  for (const t of titres) if (t.code && !parCode[t.code]) parCode[t.code] = t;
  IDX = { lignes, titres, parCode, regles: AP.extraitRegles(AP.DOC_METHODE), norm: titres.map(t => sansAccent(lignes.slice(t.l, t.feuilleFin).join('\n'))) };
  return IDX;
}
/* « B6-A · A5-7 · R4 » → sections et règles. */
function resous(ref) {
  const I = indexe(); if (!I || !ref) return { sections: [], regles: [] };
  const sections = [], regles = [];
  for (let p of String(ref).split(/[·,;]/)) {
    p = p.trim().replace(/\.$/, ''); if (!p) continue;
    const r = /^R(\d+)$/.exec(p);
    if (r) { const x = I.regles.find(g => g.n === +r[1]); if (x) regles.push(x); continue; }
    const m = /^([A-F]\d+b?)(?:-(.+))?$/.exec(p); if (!m) continue;
    const subs = m[2] ? m[2].split('/') : [null];
    for (const s of subs) { const t = I.parCode[s ? m[1] + '-' + s : m[1]] || I.parCode[m[1]]; if (t && !sections.includes(t)) sections.push(t); }
  }
  return { sections, regles };
}

/* Markdown → HTML (sous-ensemble de la méthode : titres, listes, tableaux, code, citations). */
function md(lignes) {
  const out = [], esc = s => String(s).replace(/[&<>"]/g, x => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[x]));
  const I = U.inline;
  const cellules = ln => ln.trim().replace(/^\|/, '').replace(/\|$/, '').split('|').map(s => s.trim());
  let i = 0;
  while (i < lignes.length) {
    const ln = lignes[i];
    if (/^\s*```/.test(ln)) {
      const corps = []; i++;
      while (i < lignes.length && !/^\s*```/.test(lignes[i])) corps.push(lignes[i++]);
      i++; out.push('<pre><code>' + esc(corps.join('\n')) + '</code></pre>'); continue;
    }
    if (!ln.trim()) { i++; continue; }
    const t = /^(#{1,4})\s+(.+?)\s*#*\s*$/.exec(ln);
    if (t) { const n = t[1].length; out.push('<h' + n + '>' + I(t[2]) + '</h' + n + '>'); i++; continue; }
    if (/^\s*(-{3,}|\*{3,}|_{3,})\s*$/.test(ln)) { out.push('<hr>'); i++; continue; }
    if (/^\s*\|/.test(ln)) {
      const rangs = [];
      while (i < lignes.length && /^\s*\|/.test(lignes[i])) rangs.push(lignes[i++]);
      let html = '<table>';
      rangs.forEach((r, k) => {
        if (/^\s*\|?\s*:?-{2,}/.test(r) && /^[\s|:-]+$/.test(r)) return;
        const tag = k === 0 ? 'th' : 'td';
        html += '<tr>' + cellules(r).map(c => '<' + tag + '>' + I(c) + '</' + tag + '>').join('') + '</tr>';
      });
      out.push(html + '</table>'); continue;
    }
    if (/^\s*>/.test(ln)) {
      const q = [];
      while (i < lignes.length && /^\s*>/.test(lignes[i])) q.push(lignes[i++].replace(/^\s*>\s?/, ''));
      out.push('<blockquote>' + md(q) + '</blockquote>'); continue;
    }
    const li = /^(\s*)([-*+]|\d+[.)])\s+(.*)$/.exec(ln);
    if (li) {
      const ordonnee = /\d/.test(li[2]), items = [];
      while (i < lignes.length) {
        const x = lignes[i], m = /^(\s*)([-*+]|\d+[.)])\s+(.*)$/.exec(x);
        if (m) { items.push({ ind: m[1].length, txt: m[3] }); i++; continue; }
        if (x.trim() && /^\s{2,}/.test(x) && items.length) { items[items.length - 1].txt += ' ' + x.trim(); i++; continue; }
        if (!x.trim() && i + 1 < lignes.length && (/^(\s*)([-*+]|\d+[.)])\s+/.test(lignes[i + 1]) || /^\s{2,}\S/.test(lignes[i + 1])) && items.length) { i++; continue; }
        break;
      }
      const tag = ordonnee ? 'ol' : 'ul';
      out.push('<' + tag + '>' + items.map(it => '<li' + (it.ind >= 2 ? ' style="margin-left:' + Math.min(4, Math.floor(it.ind / 2)) * 12 + 'px"' : '') + '>' + I(it.txt) + '</li>').join('') + '</' + tag + '>');
      continue;
    }
    const p = [];
    while (i < lignes.length && lignes[i].trim() && !/^(#{1,4})\s|^\s*```|^\s*\||^\s*>|^(\s*)([-*+]|\d+[.)])\s+/.test(lignes[i])) p.push(lignes[i++].trim());
    if (!p.length) { out.push('<p>' + I(ln) + '</p>'); i++; continue; }
    out.push('<p>' + I(p.join(' ')) + '</p>');
  }
  return out.join('');
}
/* Surligne les termes (insensible aux accents) dans les nœuds texte. */
function surligne(racine, termes) {
  if (!termes.length) return;
  const w = document.createTreeWalker(racine, NodeFilter.SHOW_TEXT), noeuds = [];
  while (w.nextNode()) noeuds.push(w.currentNode);
  for (const nd of noeuds) {
    const txt = nd.nodeValue, car = [...txt];
    const norm = car.map(ch => sansAccent(ch));
    if (norm.some(s => s.length !== 1) || car.length !== txt.length) continue;
    const n = norm.join(''), plages = [];
    for (const t of termes) { let k = n.indexOf(t); while (k >= 0) { plages.push([k, k + t.length]); k = n.indexOf(t, k + t.length); } }
    if (!plages.length) continue;
    plages.sort((a, b) => a[0] - b[0]);
    const frag = document.createDocumentFragment(); let p = 0;
    for (const [a, b] of plages) { if (a < p) continue; frag.appendChild(document.createTextNode(txt.slice(p, a))); frag.appendChild(h('mark', txt.slice(a, b))); p = b; }
    frag.appendChild(document.createTextNode(txt.slice(p)));
    nd.parentNode.replaceChild(frag, nd);
  }
}
const aide = { section: null, q: '' };
function termes(q) { return sansAccent(q).split(/\s+/).filter(t => t.length >= 2); }
function cherche(q) {
  const I = indexe(), T = termes(q); if (!I || !T.length) return [];
  const res = [];
  I.norm.forEach((txt, k) => {
    let score = 0; for (const t of T) { const n = txt.split(t).length - 1; if (!n) return; score += n; }
    const t0 = I.titres[k]; if (sansAccent(t0.txt).includes(T[0])) score += 20;
    const pos = txt.indexOf(T[0]);
    const brut = I.lignes.slice(t0.l + 1, t0.feuilleFin).join(' ').replace(/[#*`|>]/g, ' ').replace(/\s+/g, ' ');
    const bn = sansAccent(brut), p2 = Math.max(0, bn.indexOf(T[0]) - 60);
    res.push({ t: t0, score, extrait: (p2 > 0 ? '… ' : '') + brut.slice(p2, p2 + 160) + '…', pos });
  });
  return res.sort((a, b) => b.score - a.score).slice(0, 30);
}
function ouvreSection(t) { aide.section = t; U.ouvreOnglet('aide', { haut: true }); const c = $('#contenu'); if (c) c.scrollTop = 0; }
U.ouvreAide = ref => { const r = resous(ref); if (r.sections[0]) ouvreSection(r.sections[0]); else U.ouvreOnglet('aide'); };
RENDUS.aide = c => {
  const I = indexe();
  c.appendChild(titre('Aide — la méthode', aide.section ? btn('← Sommaire', { cls: '.fantome', cible: 'aide-retour', click: () => { aide.section = null; U.rendPanneau(true); } }) : null));
  if (!I) { c.appendChild(h('p.aide-txt', 'Le texte de la méthode n\'est pas inclus dans cette version.')); return; }
  const resultats = h('div.resultats', { 'data-cible': 'aide-resultats' });
  const majRes = () => {
    resultats.replaceChildren();
    if (termes(aide.q).length === 0) return;
    const R = cherche(aide.q);
    if (!R.length) { resultats.appendChild(h('p.aide-txt', 'Aucun passage ne contient tous ces mots.')); return; }
    for (const r of R) resultats.appendChild(h('button', { on: { click: () => ouvreSection(r.t) } }, h('b', r.t.txt), h('br'), h('small', r.extrait)));
  };
  const q = champ('search', aide.q, { cible: 'aide-cherche', label: 'Chercher dans la méthode', placeholder: 'Chercher : contour, rampe, sous-pixel…',
    input: U.debounce(v => { aide.q = v; majRes(); }, 180) });
  c.appendChild(q);
  c.appendChild(resultats); majRes();

  /* ce qui s'applique maintenant */
  try {
    const e = AP.etapeCourante(U.at.doc), r = resous(e.ref);
    const boite = h('div.etape-carte', { 'data-cible': 'aide-contexte' }, h('b', 'Étape en cours : ' + e.titre), h('div.mono', { style: { fontSize: '11.5px', color: 'var(--fg-3)' } }, e.ref || ''));
    const L = h('div.ligne', { style: { flexWrap: 'wrap', gap: '4px' } });
    for (const t of r.sections) L.appendChild(btn((t.code || '') + ' ' + t.txt.replace(/^[A-Z0-9]+b?\.\s*/, '').slice(0, 34), { cls: '.fantome', cible: 'aide-ref-' + t.code, click: () => ouvreSection(t) }));
    boite.appendChild(L);
    for (const g of r.regles) boite.appendChild(h('details', h('summary', 'Règle ' + g.n), h('p', { html: U.inline(g.texte) })));
    c.appendChild(boite);
  } catch (err) { /* pas d'étape : rien à montrer */ }

  if (aide.section) {
    const t = aide.section;
    const doc = h('div.doc-aide', { 'data-cible': 'aide-section', html: md(I.lignes.slice(t.l, t.fin)) });
    surligne(doc, termes(aide.q));
    c.appendChild(doc);
    const k = t.k, suiv = I.titres.slice(k + 1).find(x => x.l >= t.fin), prec = I.titres.slice(0, k).reverse().find(x => x.niveau === t.niveau);
    c.appendChild(h('div.ligne', { style: { justifyContent: 'space-between', marginTop: '12px' } },
      prec ? btn('← ' + prec.txt.slice(0, 28), { cls: '.fantome', cible: 'aide-prec', click: () => ouvreSection(prec) }) : h('span'),
      suiv ? btn(suiv.txt.slice(0, 28) + ' →', { cls: '.fantome', cible: 'aide-suiv', click: () => ouvreSection(suiv) }) : h('span')));
  } else {
    c.appendChild(titre('Sommaire'));
    const som = h('div.sommaire', { 'data-cible': 'aide-sommaire' });
    for (const t of I.titres) {
      if (t.niveau > 3) continue;
      som.appendChild(h('button' + (t.niveau === 2 ? '.n2' : t.niveau === 3 ? '.n3' : ''), { style: t.niveau === 1 ? { fontWeight: '600', color: 'var(--fg)' } : null, on: { click: () => ouvreSection(t) } }, t.txt));
    }
    c.appendChild(som);
    c.appendChild(h('p.aide-txt', I.titres.length + ' sections, ' + I.regles.length + ' règles impératives. Le texte est celui de METHODE_PIXEL_ART.md, en entier.'));
  }
  c.appendChild(h('hr'));
  c.appendChild(h('p.aide-txt', { 'data-cible': 'aide-mention' }, 'Claude Pixel est un projet personnel, non officiel, sans lien avec Anthropic. Il sert d\'atelier d\'entraînement : chaque pixel posé vient d\'un geste de souris ou de clavier, et chaque séance peut être rejouée.'));
};

/* ======================================================================
 * SÉANCE : rejeu, frise, timelapse, intégrité, archives
 * ==================================================================== */
const ARCH = 'seances', MAX_ARCH = 6;
const indicesNouveau = J => J.reduce((L, ev, i) => (ev.k === 'a' && ev.n === 'doc.nouveau' && !ev.refus ? L.concat(i) : L), []);
/* Une tranche du journal rejouable seule : on rend l'outil et les couleurs hérités. */
function tranche(J, debut, fin = J.length) {
  if (debut <= 0) return J.slice(0, fin);
  const avant = AP.Atelier.rejoue(J, debut, U.at.mode), t = J[debut].t;
  return [{ k: 'a', n: 'outil', a: { nom: avant.s.outil }, t }, { k: 'a', n: 'couleur', a: { c1: AP.hex(avant.s.c1, true), c2: AP.hex(avant.s.c2, true) }, t }].concat(J.slice(debut, fin));
}
function seanceCourante() {
  const J = U.at.journal, N = indicesNouveau(J);
  return tranche(J, N.length ? N[N.length - 1] : 0);
}
const significative = J => J.some(ev => ev.k === 'i');
function archive(J, nom) {
  if (!significative(J)) return;
  const L = U.stocke.lis(ARCH, []) || [];
  L.unshift({ nom: nom || 'sans titre', mode: U.at.mode, date: Date.now(), n: J.length, journal: J });
  while (L.length > MAX_ARCH) L.pop();
  while (L.length && !U.stocke.ecris(ARCH, L)) L.pop();
  if (!L.length) U.toast('Séance trop longue pour être archivée dans ce navigateur : enregistre le projet pour la garder.', 'alerte', 6000);
}
let nomAvantNouveau = '';
function surAction(info) {
  if (!info || info.nom !== 'doc.nouveau') return;
  const J = U.at.journal, N = indicesNouveau(J);
  if (N.length >= 2) archive(tranche(J, N[N.length - 2], N[N.length - 1]), nomAvantNouveau);
}

const lec = { J: null, L: null, nom: '', t: 0, joue: false, vitesse: 8, raf: 0, dernier: 0, anneaux: [], el: null, cv: null, frise: null, info: null };
function chargeLecteur(J, nom) {
  arretLecteur();
  lec.J = J; lec.nom = nom; lec.t = 0; lec.anneaux = [];
  lec.L = AP.lecteur(J, U.at.mode);
  lec.L.avance(2);
  lec.el = null;
}
const t0 = () => lec.J && lec.J.length ? lec.J[0].t : 0;
function vaA(t) {
  t = Math.max(0, Math.min(lec.L.duree, t));
  if (t < lec.t) { lec.L = AP.lecteur(lec.J, U.at.mode); lec.anneaux = []; }
  lec.t = t;
  const avant = lec.L.i;
  lec.L.jusquAuTemps(t0() + t);
  for (let k = avant; k < lec.L.i; k++) { const ev = lec.J[k]; if (ev.k === 'i' && ev.type === 'down') lec.anneaux.push({ x: ev.x, y: ev.y, t: performance.now(), droit: ev.b === 2 }); }
  if (lec.anneaux.length > 12) lec.anneaux.splice(0, lec.anneaux.length - 12);
  dessineLecteur();
}
function dessineLecteur() {
  const cv = lec.cv; if (!cv || !cv.isConnected) return;
  const e = lec.L.etat(), x = cv.getContext('2d');
  const w = e.w || 16, hh = e.h || 16, s = Math.max(1, Math.floor(320 / Math.max(w, hh)));
  if (cv.width !== w * s || cv.height !== hh * s) { cv.width = w * s; cv.height = hh * s; }
  x.imageSmoothingEnabled = false;
  x.fillStyle = U.couleurToken('--stage'); x.fillRect(0, 0, cv.width, cv.height);
  if (e.px) { const tmp = U.pxVersCanvas(document.createElement('canvas'), e.px, w, hh); x.drawImage(tmp, 0, 0, w * s, hh * s); }
  const maint = performance.now();
  lec.anneaux = lec.anneaux.filter(a => maint - a.t < 450);
  for (const a of lec.anneaux) {
    const k = (maint - a.t) / 450;
    x.strokeStyle = a.droit ? 'rgba(94,200,192,' + (1 - k) + ')' : 'rgba(180,140,255,' + (1 - k) + ')';
    x.lineWidth = 2; x.beginPath(); x.arc((a.x + 0.5) * s, (a.y + 0.5) * s, 4 + k * 12, 0, Math.PI * 2); x.stroke();
  }
  if (e.curseur) {
    const cx = (e.curseur.x + 0.5) * s, cy = (e.curseur.y + 0.5) * s;
    x.fillStyle = '#b48cff'; x.strokeStyle = '#140c1f'; x.lineWidth = 1.4;
    x.beginPath(); x.moveTo(cx, cy); x.lineTo(cx, cy + 16); x.lineTo(cx + 4.5, cy + 12); x.lineTo(cx + 7.5, cy + 18.5); x.lineTo(cx + 10.5, cy + 17); x.lineTo(cx + 7.6, cy + 10.8); x.lineTo(cx + 13.5, cy + 10.8); x.closePath();
    x.fill(); x.stroke();
  }
  const D = lec.L.duree || 1, p = lec.t / D * 100;
  if (lec.frise) { $('.tete', lec.frise).style.left = 'calc(' + p + '% - 1px)'; $('.rempli', lec.frise).style.width = p + '%'; }
  if (lec.info) lec.info.textContent = fmtTemps(lec.t) + ' / ' + fmtTemps(lec.L.duree) + ' · ' + lec.L.i + '/' + lec.L.total + ' événements';
  if (lec.anneaux.length && !lec.joue) requestAnimationFrame(dessineLecteur);
}
function boucleLecteur(now) {
  if (!lec.joue) return;
  if (!lec.cv || !lec.cv.isConnected) { lec.joue = false; return; }
  const dt = Math.min(250, now - (lec.dernier || now)); lec.dernier = now;
  vaA(lec.t + dt * lec.vitesse);
  if (lec.t >= lec.L.duree) { lec.joue = false; majBoutonLecteur(); return; }
  lec.raf = requestAnimationFrame(boucleLecteur);
}
function arretLecteur() { lec.joue = false; cancelAnimationFrame(lec.raf); }
function majBoutonLecteur() { const b = lec.el && $('[data-cible="seance-joue"]', lec.el); if (b) { b.textContent = lec.joue ? 'Pause' : 'Lire'; b.setAttribute('aria-pressed', String(lec.joue)); } }
function construitLecteur() {
  const D = lec.L.duree || 1;
  const cv = h('canvas', { 'data-cible': 'seance-toile', 'aria-label': 'Rejeu de la séance' });
  const frise = h('div.frise', { 'data-cible': 'seance-frise', title: 'Glisser pour se déplacer dans la séance' }, h('div.rempli'));
  for (const ch of lec.L.chapitres) frise.appendChild(h('div.chap', { title: 'Étape validée', style: { left: ((ch.t - t0()) / D * 100) + '%' } }));
  for (const co of lec.L.corrections) frise.appendChild(h('div.corr', { title: 'Correction', style: { left: ((co.t - t0()) / D * 100) + '%' } }));
  frise.appendChild(h('div.tete'));
  let glisse = false;
  const place = e => { const r = frise.getBoundingClientRect(); vaA(Math.max(0, Math.min(1, (e.clientX - r.left) / r.width)) * lec.L.duree); };
  frise.addEventListener('pointerdown', e => { glisse = true; try { frise.setPointerCapture(e.pointerId); } catch (x) { /* rien */ } place(e); });
  frise.addEventListener('pointermove', e => { if (glisse) place(e); });
  frise.addEventListener('pointerup', () => { glisse = false; });
  frise.addEventListener('pointercancel', () => { glisse = false; });
  const info = h('div.mono', { style: { fontSize: '11.5px', color: 'var(--fg-3)' } });
  const vit = champ('select', lec.vitesse, { options: [1, 2, 4, 8, 16, 32, 64].map(v => [v, '×' + v]), cible: 'seance-vitesse', label: 'Vitesse', change: v => { lec.vitesse = +v; } });
  const joue = btn('Lire', { cls: '.prim', cible: 'seance-joue', presse: false, click: () => {
    if (lec.joue) { arretLecteur(); majBoutonLecteur(); return; }
    if (lec.t >= lec.L.duree) vaA(0);
    lec.joue = true; lec.dernier = 0; majBoutonLecteur(); lec.raf = requestAnimationFrame(boucleLecteur);
  } });
  const el = h('div.lecteur.pile', cv, frise,
    h('div.ligne', { style: { gap: '6px', flexWrap: 'wrap' } }, joue, btn('Début', { cible: 'seance-debut', click: () => vaA(0) }), btn('Fin', { cible: 'seance-fin', click: () => vaA(lec.L.duree) }), vit),
    info,
    h('div.ligne', { style: { gap: '10px', fontSize: '11.5px', color: 'var(--fg-3)' } },
      h('span', h('span', { style: { display: 'inline-block', width: '8px', height: '8px', background: 'var(--info)', marginRight: '4px' } }), lec.L.chapitres.length + ' étape(s) validée(s)'),
      h('span', h('span', { style: { display: 'inline-block', width: '8px', height: '8px', background: 'var(--danger)', marginRight: '4px' } }), lec.L.corrections.length + ' correction(s)')));
  Object.assign(lec, { el, cv, frise, info });
  return el;
}
async function timelapse(J, nom) {
  if (!G.MediaRecorder || !HTMLCanvasElement.prototype.captureStream) {
    U.toast('Ce navigateur ne sait pas enregistrer de vidéo ici. La vidéo de la souris (séance enregistrée) reste disponible.', 'alerte', 6000); return;
  }
  const types = ['video/webm;codecs=vp9', 'video/webm;codecs=vp8', 'video/webm'];
  const type = types.find(t => MediaRecorder.isTypeSupported(t));
  if (!type) { U.toast('Format WebM non pris en charge par ce navigateur.', 'alerte'); return; }
  const L = AP.lecteur(J, U.at.mode); L.avance(2);
  const T = 480, cv = document.createElement('canvas'); cv.width = T; cv.height = T;
  const x = cv.getContext('2d'); x.imageSmoothingEnabled = false;
  const fond = U.couleurToken('--stage'), tmp = document.createElement('canvas');
  const dessine = () => {
    const e = L.etat(); x.fillStyle = fond; x.fillRect(0, 0, T, T);
    if (!e.px) return;
    const s = Math.max(1, Math.floor(Math.min((T - 32) / e.w, (T - 32) / e.h))), ox = (T - e.w * s) >> 1, oy = (T - e.h * s) >> 1;
    U.pxVersCanvas(tmp, e.px, e.w, e.h); x.drawImage(tmp, ox, oy, e.w * s, e.h * s);
    x.fillStyle = 'rgba(242,184,75,.9)'; x.fillRect(0, T - 4, T * L.i / Math.max(1, L.total), 4);
  };
  dessine();
  const rec = new MediaRecorder(cv.captureStream(30), { mimeType: type }), morceaux = [];
  rec.ondataavailable = e => { if (e.data && e.data.size) morceaux.push(e.data); };
  const fini = new Promise(ok => { rec.onstop = ok; });
  rec.start(500);
  U.toast('Timelapse en cours (environ 20 s)…', 'info', 4000);
  const parImage = Math.max(1, Math.ceil(L.total / (20 * 30)));
  await new Promise(ok => {
    const pas = () => { const reste = L.avance(parImage); dessine(); if (reste) setTimeout(pas, 1000 / 30); else setTimeout(ok, 1500); };
    pas();
  });
  rec.stop(); await fini;
  const blob = new Blob(morceaux, { type: 'video/webm' });
  const buf = new Uint8Array(await blob.arrayBuffer());
  await U.telecharge(U.nomFichier(nom) + '-timelapse.webm', buf, 'video/webm');
}
function verifieIntegrite() {
  const r = U.at.integrite();
  if (r.ok) U.toast('Intégrité vérifiée : chaque pixel du dessin sort des ' + (r.evenements || U.at.journal.length) + ' gestes du journal.', 'ok', 5000);
  else U.toast('Écart entre le dessin et son journal : ' + (r.ecarts || []).slice(0, 3).join(' ; '), 'refus', 8000);
  return r;
}
async function rejoueFichier() {
  const f = await U.choisitFichier('.json,application/json'); if (!f) return;
  try {
    const p = JSON.parse(await U.litTexte(f));
    if (!p || !AP.FORMATS.includes(p.format) || !Array.isArray(p.journal)) throw new Error('Ce fichier n\'est pas un projet Claude Pixel.');
    chargeLecteur(p.journal, (p.doc && p.doc.nom) || f.name);
    U.ouvreOnglet('seance');
  } catch (e) { U.toast(e.message || 'Fichier illisible.', 'refus'); }
}
RENDUS.seance = c => {
  const J = seanceCourante(), nom = U.at.doc.nom;
  if (!lec.J) chargeLecteur(J, nom + ' (séance en cours)');
  const duree = J.length ? J[J.length - 1].t - J[0].t : 0;
  c.appendChild(titre('Séance en cours'));
  c.appendChild(h('p.aide-txt', J.length + ' événements · ' + fmtTemps(duree) + ' · mode ' + (U.at.mode === 'claude' ? 'Claude (souris et clavier seulement)' : 'humain')));
  c.appendChild(h('div.ligne', { style: { gap: '6px', flexWrap: 'wrap' } },
    btn('Rejouer la séance', { cible: 'seance-rejoue', click: () => { chargeLecteur(seanceCourante(), nom + ' (séance en cours)'); U.rendPanneau(true); } }),
    btn('Timelapse WebM', { cible: 'seance-timelapse', title: 'Vidéo d\'environ 20 s de toute la séance', click: async e => { const b = e.currentTarget; b.disabled = true; try { await timelapse(seanceCourante(), nom); } finally { b.disabled = false; } } }),
    btn('Vérifier l\'intégrité', { cible: 'seance-integrite', click: verifieIntegrite })));

  c.appendChild(titre('Lecteur', h('small', { style: { fontWeight: '400', color: 'var(--fg-3)', minWidth: '0', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' } }, lec.nom)));
  c.appendChild(lec.el && lec.el.isConnected === false && lec.cv ? lec.el : construitLecteur());
  dessineLecteur();

  c.appendChild(titre('Séances archivées', btn('Ouvrir un .json…', { cls: '.fantome', cible: 'seance-fichier', click: rejoueFichier })));
  const L = U.stocke.lis(ARCH, []) || [];
  if (!L.length) c.appendChild(h('p.aide-txt', 'Chaque « Nouveau dessin » range la séance précédente ici (6 au plus, dans ce navigateur).'));
  L.forEach((s, k) => c.appendChild(h('div.seance-l', { 'data-cible': 'seance-' + (k + 1) },
    h('div', h('b', s.nom), h('br'), h('small', new Date(s.date).toLocaleString('fr-FR', { dateStyle: 'short', timeStyle: 'short' }) + ' · ' + s.n + ' év. · ' + (s.mode === 'claude' ? 'Claude' : 'humain'))),
    h('div.ligne', { style: { gap: '4px' } },
      btn('Rejouer', { cible: 'seance-rejoue-' + (k + 1), click: () => { chargeLecteur(s.journal, s.nom); U.rendPanneau(true); } }),
      btn('✕', { cls: '.ico.fantome', label: 'Supprimer cette séance', cible: 'seance-supprime-' + (k + 1), click: () => { const M = U.stocke.lis(ARCH, []) || []; M.splice(k, 1); U.stocke.ecris(ARCH, M); U.rendPanneau(true); } })))));
};

/* ======================================================================
 * LECTURE SEULE POUR LA SOURIS (aucune écriture possible par ici)
 * ==================================================================== */
function rect(el) { const r = el.getBoundingClientRect(); return { x: r.left, y: r.top, w: r.width, h: r.height, cx: r.left + r.width / 2, cy: r.top + r.height / 2 }; }
const lectureSeule = Object.freeze({
  version: 1,
  etat() {
    const at = U.at, d = at.doc, cv = $('#toile');
    let etape = null; try { const e = AP.etapeCourante(d); etape = { i: Math.min(d.meta.etape, AP.nbEtapes(d) - 1), titre: e.titre, ref: e.ref, finie: d.meta.etape >= AP.nbEtapes(d) }; } catch (x) { /* rien */ }
    return { mode: at.mode, outil: at.s.outil, c1: AP.hex(at.s.c1, true), c2: AP.hex(at.s.c2, true), taille: at.s.taille, calque: at.s.calque, image: at.s.image,
      nbCalques: d.calques.length, nbImages: d.images.length, docW: d.w, docH: d.h, nom: d.nom, type: d.type,
      zoom: U.vue.zoom, ox: U.vue.ox, oy: U.vue.oy, toile: cv ? rect(cv) : null, etape, panneau: U.ongletCourant || null, enLecture: !!lecture,
      modale: U.modaleOuverte, menu: U.menuOuvert, journal: at.journal.length };
  },
  pixels(o = {}) {
    const d = U.at.doc, px = AP.compose(d, o.image === undefined ? U.at.s.image : o.image, o.vue || 'export');
    const lignes = [];
    for (let y = 0; y < d.h; y++) { const L = []; for (let x = 0; x < d.w; x++) { const c = px[y * d.w + x]; L.push(c >>> 24 ? AP.hex(c, true) : null); } lignes.push(L); }
    return { w: d.w, h: d.h, lignes };
  },
  messages(n = 20) { return U.at.messages.slice(-n).map(m => ({ msg: m.msg, niveau: m.niveau })); },
  verifie() { return AP.verifieEtape(U.at); },
  integrite() { const r = U.at.integrite(); return { ok: r.ok, ecarts: r.ecarts || [] }; },
  cible(nom) {
    const L = $$('[data-cible="' + String(nom).replace(/"/g, '') + '"]').filter(el => el.getClientRects().length && getComputedStyle(el).visibility !== 'hidden');
    return L.length ? rect(L[L.length - 1]) : null;
  },
  cibles() { return $$('[data-cible]').filter(el => el.getClientRects().length).map(el => Object.assign({ nom: el.dataset.cible }, rect(el))); },
  ecranDeCellule(x, y) { return U.celluleVersEcran(x, y); },
  celluleDeEcran(x, y) { const p = U.ecranVersCellule(x, y), d = U.at.doc; const cx = Math.floor(p.x), cy = Math.floor(p.y); return { x: cx, y: cy, dedans: cx >= 0 && cy >= 0 && cx < d.w && cy < d.h }; },
  defauts() { return AP.detecte(U.at.doc, U.at.s.image).map(r => ({ id: r.id, niveau: r.niveau, titre: r.titre, ref: r.ref, msg: r.msg, pixels: r.pixels.slice(0, 200) })); },
  palette() { return U.at.doc.palette.map(c => AP.hex(c, true)); },
  /* Lumière et volume (0-C) : réglage, mesure, et trois images en lignes (valeurs, notan, guide). */
  volume() {
    const d = U.at.doc, f = U.at.s.image, VO = AP.VOLUME, L = VO.lumiereDe(d), px = AP.compose(d, f, 'export');
    const M = VO.mesure(px, d.w, d.h, L), g = VO.guide(px, d.w, d.h, L), gr = AP.VUES.gris(px), nt = VO.notan(px);
    const lignes = src => { const out = []; for (let y = 0; y < d.h; y++) { const r = []; for (let x = 0; x < d.w; x++) { const c = src(y * d.w + x); r.push(c); } out.push(r); } return out; };
    const hx = c => c >>> 24 ? AP.hex(c, true) : null;
    return {
      lumiere: { az: L.az, el: L.el, forme: L.forme, posee: !!(d.lumiere && d.lumiere.posee), nom: VO.nomDirection(L.az) },
      mesure: { accord: M.accord, ecart: M.ecart, inverses: M.inverses, etendue: M.etendue, fautifs: M.fautifs.length, n: M.n },
      w: d.w, h: d.h,
      valeurs: lignes(i => hx(gr[i])), notan: lignes(i => hx(nt[i])),
      guide: lignes(i => g.zone[i] ? VO.ZONES[g.zone[i]].coul : null)
    };
  }
});
Object.defineProperty(G, 'claudePixel', { value: lectureSeule, writable: false, configurable: false });

/* ======================================================================
 * DÉMARRAGE
 * ==================================================================== */
function demarre() {
  U.claude = U.detecteMode() === 'claude';
  const th = U.stocke.lis('theme', null); if (th) U.appliqueTheme(th);
  U.initTelechargements && U.initTelechargements();
  U.at = new AP.Atelier({ mode: U.claude ? 'claude' : 'humain' });
  const badge = $('#badge-mode');
  if (badge) { badge.lastElementChild.textContent = U.claude ? 'Claude' : 'Humain'; badge.classList.toggle('claude', U.claude); badge.title = U.claude ? 'Mode Claude : souris et clavier seulement, portes bloquantes' : 'Mode humain : les portes conseillent sans bloquer'; }
  let restaure = false;
  try { const p = U.stocke.lis('auto', null); if (p && AP.FORMATS.includes(p.format)) { U.at.charge(p); restaure = true; } } catch (e) { console.warn('Sauvegarde locale illisible', e); }
  U.initScene(); U.initOutils(); U.initPanneaux(); initTimeline();
  let dernierToast = '', dernierT = 0;
  U.at.ecoute((q, info) => {
    if (q === 'act') { surAction(info); nomAvantNouveau = U.at.doc.nom; return; }
    if (q === 'doc') { nomAvantNouveau = nomAvantNouveau || U.at.doc.nom; return; }
    if (q !== 'message' || !info) return;
    const t = performance.now();
    if (info.msg === dernierToast && t - dernierT < 1500) return;
    dernierToast = info.msg; dernierT = t;
    if (info.niveau === 'refus') { U.alertePorte(info.msg); U.toast(info.msg, 'refus'); }
    else if (info.niveau === 'alerte' || info.niveau === 'ok') U.toast(info.msg, info.niveau);
  });
  nomAvantNouveau = U.at.doc.nom;
  // le nom courant avant chaque action, pour nommer la séance archivée au « Nouveau »
  const actPrec = U.at.act.bind(U.at);
  U.at.act = function (n, a) { if (n === 'doc.nouveau') nomAvantNouveau = this.doc ? this.doc.nom : ''; return actPrec(n, a); };
  U.ajuste(); U.redessine();
  const sauveVite = () => { try { U.stocke.ecris('auto', U.at.projet()); } catch (e) { /* rien */ } };
  addEventListener('pagehide', sauveVite);
  document.addEventListener('visibilitychange', () => { if (document.visibilityState === 'hidden') sauveVite(); });
  addEventListener('resize', U.debounce(() => U.ajuste(), 150));
  if (!restaure) U.modaleNouveau(true);
}
try { demarre(); }
catch (e) {
  console.error(e);
  document.body.appendChild(h('div', { style: { position: 'fixed', inset: '16px', padding: '16px', background: '#2a1215', color: '#ffd7d7', border: '1px solid #ff6b6b', borderRadius: '8px', font: '14px/1.5 system-ui', zIndex: 999, overflow: 'auto' } },
    h('b', 'Claude Pixel n\'a pas pu démarrer.'), h('pre', { style: { whiteSpace: 'pre-wrap' } }, String(e && e.stack || e))));
}
})(window);
