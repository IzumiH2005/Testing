/* Claude Pixel — interface : panneau latéral (Couleurs, Calques, Méthode, Contrôle).
 * Les onglets Tuiles, Aide et Séance sont ajoutés par ui-plus.js dans U.RENDUS. */
(function (G) {
'use strict';
const AP = G.AP, U = AP.UI;
const { $, $$, h } = U;

const RENDUS = U.RENDUS = U.RENDUS || {};
const LEGERS = U.LEGERS = U.LEGERS || {};   // mises à jour légères (miniatures) sur 'pixels'/'trait'
let courant = null, enAttente = false, rafId = 0;
const defil = {};                            // position de défilement par onglet

const act = (n, a) => U.act(n, a);
const at = () => U.at;
const etroit = () => G.matchMedia && matchMedia('(max-width: 1099px)').matches;

/* ---------- Onglets et tiroir ---------- */
function ouvreOnglet(nom, o = {}) {
  if (!RENDUS[nom]) nom = 'couleurs';
  const c = $('#contenu');
  if (courant && c) defil[courant] = c.scrollTop;
  courant = nom;
  for (const b of $$('.onglet')) {
    const oui = b.dataset.onglet === nom;
    b.setAttribute('aria-selected', oui ? 'true' : 'false');
    b.tabIndex = oui ? 0 : -1;
    // l'onglet choisi et ses voisins restent visibles quand la barre déborde
    if (oui && b.scrollIntoView) { const n = b.nextElementSibling || b; try { n.scrollIntoView({ block: 'nearest', inline: 'nearest' }); b.scrollIntoView({ block: 'nearest', inline: 'nearest' }); } catch (e) { /* vieux navigateur */ } }
  }
  if (c) c.setAttribute('aria-label', ($('.onglet[data-onglet="' + nom + '"]') || {}).textContent || nom);
  U.stocke.ecris('onglet', nom);
  rendu(true);
  if (c) c.scrollTop = o.haut ? 0 : (defil[nom] || 0);
  if (etroit() && o.ouvre !== false) basculePanneau(true);
}
function basculePanneau(force) {
  const app = $('#app'); if (!app) return;
  const ouvert = force === undefined ? !app.classList.contains('panneau-ouvert') : !!force;
  app.classList.toggle('panneau-ouvert', ouvert);
  $('#b-panneau').setAttribute('aria-expanded', ouvert ? 'true' : 'false');
  if (ouvert && !courant) ouvreOnglet(U.stocke.lis('onglet', 'methode'), { ouvre: false });
}

/* Ne pas reconstruire sous les doigts : si un champ du panneau a le focus, on attend sa sortie. */
let doigtPose = false; // un bouton est pressé dans le panneau : reconstruire volerait le clic
function champActif() {
  if (doigtPose) return true;
  const a = document.activeElement, c = $('#contenu');
  return a && c && c.contains(a) && /^(INPUT|TEXTAREA|SELECT)$/.test(a.tagName) && a.type !== 'checkbox';
}
function rendu(force) {
  const c = $('#contenu'); if (!c || !courant || !U.at || !U.at.doc) return;
  if (!force && champActif()) { enAttente = true; return; }
  enAttente = false;
  const y = c.scrollTop;
  c.replaceChildren();
  try { RENDUS[courant](c); }
  catch (e) { console.error(e); c.appendChild(h('p.aide-txt', 'Ce panneau n\'a pas pu s\'afficher : ' + e.message)); }
  c.scrollTop = y;
}
function planifie() { if (rafId) return; rafId = requestAnimationFrame(() => { rafId = 0; rendu(false); }); }
let legerT = 0, legerAttente = null;
function leger() {
  if (!LEGERS[courant]) return;
  const maintenant = performance.now();
  if (maintenant - legerT < 180) { if (!legerAttente) legerAttente = setTimeout(() => { legerAttente = null; leger(); }, 200); return; }
  legerT = maintenant;
  try { LEGERS[courant]($('#contenu')); } catch (e) { console.error(e); }
}

/* Point rouge sur l'onglet Méthode quand une porte bloque l'étape. */
function majPastille() {
  const pt = $('.onglet[data-onglet="methode"] .pt'); if (!pt || !U.at || !U.at.doc) return;
  try { pt.hidden = AP.verifieEtape(U.at).ok; } catch (e) { pt.hidden = true; }
}

/* ---------- Petits composants ---------- */
const titre = (txt, ...droite) => h('h3', h('span', txt), h('span.espace'), ...droite);
const btn = (txt, o = {}) => h('button.btn' + (o.cls || ''), {
  'data-cible': o.cible, title: o.title, disabled: !!o.inactif, 'aria-pressed': o.presse === undefined ? undefined : String(!!o.presse),
  on: { click: o.click }
}, txt);
function champ(type, valeur, o = {}) {
  const el = type === 'textarea' ? h('textarea.champ', { rows: o.rows || 3 }) : type === 'select' ? h('select.champ') : h('input.champ', { type });
  if (type === 'select') for (const op of o.options || []) {
    const [v, t] = Array.isArray(op) ? op : [op, op];
    el.appendChild(h('option', { value: v }, t));
  }
  if (o.cible) el.dataset.cible = o.cible;
  if (o.placeholder) el.placeholder = o.placeholder;
  if (o.min !== undefined) el.min = o.min;
  if (o.max !== undefined) el.max = o.max;
  if (o.step !== undefined) el.step = o.step;
  if (o.label) el.setAttribute('aria-label', o.label);
  el.value = valeur ?? '';
  if (o.change) el.addEventListener('change', () => o.change(el.value, el));
  if (o.input) el.addEventListener('input', () => o.input(el.value, el));
  return el;
}
function miniature(px, w, hh, taille = 36) {
  const cv = h('canvas', { width: w, height: hh });
  if (px) U.pxVersCanvas(cv, px, w, hh);
  const k = taille / Math.max(w, hh);
  cv.style.width = Math.max(1, Math.round(w * k)) + 'px'; cv.style.height = Math.max(1, Math.round(hh * k)) + 'px';
  return cv;
}
const damier = 'repeating-conic-gradient(var(--surface-3) 0 25%, var(--surface-2) 0 50%) 0 0 / 8px 8px';

/* ======================================================================
 * COULEURS
 * ==================================================================== */
let hsv = null;          // couleur en cours dans le sélecteur
let rampeN = 5, rampeDecal = 15;

function hexVersHsv(x) { const [r, g, b] = AP.unpack(AP.parseHex(x)); return AP.rgb2hsv(r, g, b); }
function hsvVersHex(v) { const [r, g, b] = AP.hsv2rgb(v[0], v[1], v[2]); return AP.hex(AP.pack(r, g, b)); }

function rendCouleurs(c) {
  const A = at(), d = A.doc, hc1 = AP.hex(A.s.c1), hc2 = AP.hex(A.s.c2);
  if (!hsv) hsv = hexVersHsv(hc1);

  /* Budget A3 */
  const f = A.s.image, mes = AP.mesures(d, f), bud = AP.budgetPourTaille(d.w, d.h);
  const trop = mes.couleurs > bud.total;
  c.appendChild(titre('Palette', h('span.mono.aide-txt', { title: 'Couleurs utilisées dans l\'image / budget A3 pour cette taille' },
    mes.couleurs + ' / ' + bud.total + ' utilisées')));
  if (trop) c.appendChild(h('p.aide-txt', { style: { color: 'var(--warn)' } },
    'Au-dessus du budget A3 (' + bud.total + ' couleurs à ' + d.w + '×' + d.h + ') : fusionne les tons proches.'));

  /* Nuancier */
  const n = h('div.nuancier', { role: 'listbox', 'aria-label': 'Palette du dessin', 'data-cible': 'nuancier' });
  d.palette.forEach((hx, i) => {
    let appui = 0, long = false;
    const b = h('button.nuance' + (hx === hc1 ? '.c1' : '') + (hx === hc2 ? '.c2' : ''), {
      role: 'option', 'aria-selected': String(hx === hc1), title: hx + ' — clic : C1, clic droit : C2, appui long : options',
      'aria-label': 'Teinte ' + (i + 1) + ' ' + hx, 'data-cible': 'teinte-' + i, style: { background: hx },
      on: {
        click: () => { if (long) { long = false; return; } act('couleur', { c1: hx }); hsv = hexVersHsv(hx); },
        contextmenu: e => { e.preventDefault(); act('couleur', { c2: hx }); },
        pointerdown: e => { if (e.pointerType === 'mouse') return; clearTimeout(appui); appui = setTimeout(() => { long = true; menuTeinte(b, i, hx); }, 480); },
        pointerup: () => clearTimeout(appui), pointerleave: () => clearTimeout(appui), pointercancel: () => clearTimeout(appui)
      }
    }, h('span.n', String(i + 1)));
    n.appendChild(b);
  });
  n.appendChild(h('button.nuance.ajout', { title: 'Ajouter C1 à la palette', 'aria-label': 'Ajouter la couleur 1 à la palette', 'data-cible': 'palette-ajoute',
    on: { click: () => { const r = act('palette.ajoute', { hex: hc1 }); if (r && r.deja) U.toast('Cette teinte est déjà dans la palette.'); } } }, '+'));
  c.appendChild(n);

  const c1i = d.palette.indexOf(hc1);
  c.appendChild(h('div.ligne',
    btn('Échanger C1/C2', { cls: '.fantome', cible: 'couleur-echange', title: 'X', click: () => act('couleur.echange') }),
    btn('Retirer C1', { cls: '.fantome', cible: 'palette-retire', inactif: c1i < 0, click: () => act('palette.retire', { i: c1i }) }),
    btn('⋯', { cls: '.fantome', cible: 'menu-palette', title: 'Palettes, import et export', click: e => menuPalette(e.currentTarget) })));

  /* Sélecteur TSV */
  c.appendChild(titre('Sélecteur', h('span.mono.aide-txt', hsvVersHex(hsv))));
  const sv = h('canvas', { 'data-cible': 'selecteur-sv', 'aria-label': 'Saturation et valeur' });
  const te = h('canvas.teinte', { 'data-cible': 'selecteur-teinte', 'aria-label': 'Teinte' });
  const apercu = h('div', { style: { height: '28px', borderRadius: '6px', border: '1px solid var(--line)', background: hsvVersHex(hsv), flex: '1', minWidth: '40px' } });
  const hexIn = champ('text', hsvVersHex(hsv), { label: 'Code hexadécimal', cible: 'hex', change: v => {
    try { const x = AP.hex(AP.parseHex(v.trim().startsWith('#') ? v.trim() : '#' + v.trim())); hsv = hexVersHsv(x); peins(); } catch (e) { U.toast('Code couleur illisible.', 'alerte'); }
  } });
  hexIn.style.maxWidth = '110px'; hexIn.classList.add('mono');
  const peins = () => {
    dessineSV(sv, hsv); dessineTeinte(te, hsv);
    const x = hsvVersHex(hsv); apercu.style.background = x; if (document.activeElement !== hexIn) hexIn.value = x;
    const t = c.querySelector('h3:nth-of-type(2) .mono'); if (t) t.textContent = x + '  ·  T' + Math.round(hsv[0]) + ' S' + Math.round(hsv[1] * 100) + ' V' + Math.round(hsv[2] * 100);
  };
  glisse(sv, (x, y) => { hsv = [hsv[0], x, 1 - y]; peins(); });
  glisse(te, (x, y) => { hsv = [y * 360, hsv[1], hsv[2]]; peins(); });
  c.appendChild(h('div.selecteur', sv, te));
  c.appendChild(h('div.ligne', apercu, hexIn));
  const remap = h('input', { type: 'checkbox', 'data-cible': 'remap' });
  c.appendChild(h('div.ligne',
    btn('Prendre en C1', { cls: '.prim', cible: 'selecteur-c1', click: () => act('couleur', { c1: hsvVersHex(hsv) }) }),
    btn('Ajouter', { cible: 'selecteur-ajoute', click: () => { const r = act('palette.ajoute', { hex: hsvVersHex(hsv) }); if (r && r.deja) U.toast('Déjà dans la palette.'); } }),
    btn('Remplacer C1', { cible: 'selecteur-remplace', inactif: c1i < 0, title: 'Change la teinte C1 dans la palette et les rampes',
      click: () => { act('palette.modifie', { i: c1i, hex: hsvVersHex(hsv), remap: remap.checked }); act('couleur', { c1: hsvVersHex(hsv) }); } })));
  c.appendChild(h('label.coche.aide-txt', remap, h('span', 'Remplacer aussi dans les pixels (remap)')));
  requestAnimationFrame(peins);

  /* Rampes */
  c.appendChild(titre('Rampes', h('span.aide-txt', d.rampes.length + ' rampe' + (d.rampes.length > 1 ? 's' : ''))));
  c.appendChild(h('p.aide-txt', 'Une rampe = une matière, du plus sombre au plus clair, avec un décalage de teinte (C2, C4). L\'outil Ombre glisse le long de la rampe choisie.'));
  if (!d.rampes.length) c.appendChild(h('p.aide-txt', 'Aucune rampe : génère-en une depuis C1 ci-dessous.'));
  d.rampes.forEach((r, i) => {
    const choisie = A.s.rampe === i;
    c.appendChild(h('div.rampe-l',
      h('div.nom', h('b', r.nom), h('span.aide-txt.mono', r.couleurs.length + ' tons'), h('span.espace'),
        btn(choisie ? 'Pour l\'ombre ✓' : 'Pour l\'ombre', { cls: '.fantome', presse: choisie, cible: 'rampe-ombre-' + i,
          click: () => act('option', { cle: 'rampe', valeur: choisie ? -1 : i }) }),
        btn('Retirer', { cls: '.fantome', cible: 'rampe-retire-' + i, click: () => act('rampe.retire', { i }) })),
      h('div.rampe', { 'data-cible': 'rampe-' + i }, r.couleurs.map((x, j) => h('button', {
        style: { background: x }, title: x, 'aria-label': r.nom + ' ton ' + (j + 1) + ' ' + x, 'data-cible': 'rampe-' + i + '-' + j,
        on: { click: () => act('couleur', { c1: x }), contextmenu: e => { e.preventDefault(); act('couleur', { c2: x }); } }
      }))),
      h('span')));
  });

  /* Générateur */
  const base = hsvVersHex(hsv);
  const gen = AP.genereRampe(base, rampeN, rampeDecal);
  const nomR = champ('text', '', { placeholder: 'Nom de la matière (peau, métal…)', label: 'Nom de la rampe', cible: 'rampe-nom' });
  c.appendChild(h('div.etape-carte', { style: { marginTop: '8px' } },
    h('b', 'Générer depuis la couleur du sélecteur'),
    h('div.rampe', { style: { margin: '8px 0' } }, gen.map(x => h('button', { style: { background: x }, title: x, tabIndex: -1 }))),
    h('div.ligne',
      h('label.aide-txt', 'Tons ', champ('select', String(rampeN), { options: ['3', '4', '5', '6', '7', '8'], cible: 'rampe-n', label: 'Nombre de tons', change: v => { rampeN = +v; rendu(true); } })),
      h('label.aide-txt', { style: { flex: '1', display: 'flex', gap: '6px', alignItems: 'center' } }, 'Décalage ',
        champ('range', String(rampeDecal), { min: 0, max: 40, step: 1, label: 'Décalage de teinte', cible: 'rampe-decal', change: v => { rampeDecal = +v; rendu(true); } }),
        h('span.mono', rampeDecal + '°'))),
    h('div.ligne', nomR, btn('Ajouter la rampe', { cls: '.prim', cible: 'rampe-ajoute', click: () => act('rampe.ajoute', { nom: nomR.value.trim() || undefined, couleurs: gen }) })),
    h('p.aide-txt', 'Ombres vers le froid, lumières vers le chaud. Ajuste ensuite chaque ton à l\'œil.')));
}

function menuTeinte(ancre, i, hx) {
  U.menu(ancre, [
    { txt: 'Prendre en C1', cible: 'teinte-c1', action: () => act('couleur', { c1: hx }) },
    { txt: 'Prendre en C2', cible: 'teinte-c2', action: () => act('couleur', { c2: hx }) },
    { txt: 'Modifier dans le sélecteur', cible: 'teinte-modifie', action: () => { act('couleur', { c1: hx }); hsv = hexVersHsv(hx); rendu(true); } },
    '-',
    { txt: 'Retirer de la palette', cible: 'teinte-retire', action: () => act('palette.retire', { i }) }
  ]);
}
function menuPalette(ancre) {
  const items = [{ sous: 'Remplacer par' }];
  for (const nom in AP.PALETTES) items.push({ txt: nom + ' (' + AP.PALETTES[nom].length + ')', cible: 'palette-' + U.nomFichier(nom), action: async () => {
    if (await U.confirme('Remplacer la palette', 'La palette actuelle sera remplacée par « ' + nom + ' ». Les pixels ne changent pas.', 'Remplacer', false)) act('palette.remplace', { liste: AP.PALETTES[nom] });
  } });
  items.push('-',
    { txt: 'Palette depuis l\'image', cible: 'palette-image', action: () => act('palette.depuisImage') },
    { txt: 'Importer (.hex, .gpl, .txt)', cible: 'palette-importe', action: async () => {
      const f = await U.choisitFichier('.hex,.gpl,.txt,.pal'); if (!f) return;
      const l = AP.lisPalette(await U.litTexte(f));
      if (!l.length) { U.toast('Aucune couleur trouvée dans ce fichier.', 'alerte'); return; }
      act('palette.remplace', { liste: l });
    } },
    { txt: 'Exporter en .hex', cible: 'palette-hex', action: () => U.telecharge(U.nomFichier(U.at.doc.nom) + '.hex', AP.paletteHex(U.at.doc), 'text/plain') },
    { txt: 'Exporter en .gpl', cible: 'palette-gpl', action: () => U.telecharge(U.nomFichier(U.at.doc.nom) + '.gpl', AP.paletteGpl(U.at.doc), 'text/plain') });
  U.menu(ancre, items);
}

/* Glisser sur un canevas : rappel avec (x, y) normalisés 0–1. */
function glisse(cv, f) {
  let actif = false;
  const pos = e => { const r = cv.getBoundingClientRect(); f(Math.max(0, Math.min(1, (e.clientX - r.left) / r.width)), Math.max(0, Math.min(1, (e.clientY - r.top) / r.height))); };
  cv.addEventListener('pointerdown', e => { actif = true; cv.setPointerCapture(e.pointerId); pos(e); e.preventDefault(); });
  cv.addEventListener('pointermove', e => { if (actif) pos(e); });
  const fin = () => { actif = false; };
  cv.addEventListener('pointerup', fin); cv.addEventListener('pointercancel', fin);
}
function dessineSV(cv, v) {
  const W = Math.max(60, Math.round(cv.clientWidth || 240)), H = 150, dpr = Math.min(2, G.devicePixelRatio || 1);
  cv.width = W * dpr; cv.height = H * dpr;
  const x = cv.getContext('2d'); x.scale(dpr, dpr);
  x.fillStyle = hsvVersHex([v[0], 1, 1]); x.fillRect(0, 0, W, H);
  let g = x.createLinearGradient(0, 0, W, 0); g.addColorStop(0, '#fff'); g.addColorStop(1, 'rgba(255,255,255,0)'); x.fillStyle = g; x.fillRect(0, 0, W, H);
  g = x.createLinearGradient(0, 0, 0, H); g.addColorStop(0, 'rgba(0,0,0,0)'); g.addColorStop(1, '#000'); x.fillStyle = g; x.fillRect(0, 0, W, H);
  const px = v[1] * W, py = (1 - v[2]) * H;
  x.lineWidth = 2; x.strokeStyle = v[2] > .5 ? '#000' : '#fff'; x.beginPath(); x.arc(px, py, 6, 0, 7); x.stroke();
}
function dessineTeinte(cv, v) {
  const W = 22, H = 150, dpr = Math.min(2, G.devicePixelRatio || 1);
  cv.width = W * dpr; cv.height = H * dpr;
  const x = cv.getContext('2d'); x.scale(dpr, dpr);
  const g = x.createLinearGradient(0, 0, 0, H);
  for (let i = 0; i <= 6; i++) g.addColorStop(i / 6, hsvVersHex([i * 60 % 360, 1, 1]));
  x.fillStyle = g; x.fillRect(0, 0, W, H);
  const y = v[0] / 360 * H;
  x.fillStyle = '#fff'; x.strokeStyle = '#000'; x.lineWidth = 1;
  x.fillRect(0, y - 2, W, 4); x.strokeRect(.5, y - 2.5, W - 1, 5);
}

/* ======================================================================
 * CALQUES
 * ==================================================================== */
const TYPES_CALQUE = [['normal', 'Normal'], ['construction', 'Construction'], ['reference', 'Référence']];
const nomType = t => (TYPES_CALQUE.find(x => x[0] === t) || [t, t])[1];
const OEIL = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-7 11-7 11 7 11 7-4 7-11 7S1 12 1 12z"/><circle cx="12" cy="12" r="3"/></svg>';
const OEIL_NON = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 3l18 18"/><path d="M10.6 5.1A10 10 0 0 1 12 5c7 0 11 7 11 7a17 17 0 0 1-3.2 4M6.6 6.6A17 17 0 0 0 1 12s4 7 11 7a10 10 0 0 0 5.4-1.6"/></svg>';
const CADENAS = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/></svg>';
const CADENAS_NON = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 7.5-2"/></svg>';

function rendCalques(c) {
  const A = at(), d = A.doc, f = A.s.image, ia = A.s.calque, ca = d.calques[ia];
  c.appendChild(titre('Calques', h('span.aide-txt', 'image ' + (f + 1) + '/' + d.images.length)));
  const liste = h('div.calques', { role: 'list', 'data-cible': 'calques' });
  for (let i = d.calques.length - 1; i >= 0; i--) {
    const L = d.calques[i], px = A.cel(i, f);
    const vign = miniature(px, d.w, d.h, 36); vign.dataset.calque = String(i);
    const fond = h('div', { style: { width: '36px', height: '36px', display: 'grid', placeItems: 'center', borderRadius: '4px', background: damier, opacity: L.visible ? '1' : '.4' } }, vign);
    liste.appendChild(h('div.calque' + (i === ia ? '.actif' : ''), { role: 'listitem', 'data-cible': 'calque-' + i },
      fond,
      h('button.btn.ico.fantome', { title: L.visible ? 'Masquer' : 'Afficher', 'aria-label': (L.visible ? 'Masquer ' : 'Afficher ') + L.nom, 'aria-pressed': String(L.visible),
        'data-cible': 'calque-oeil-' + i, html: L.visible ? OEIL : OEIL_NON, on: { click: () => act('calque.prop', { i, visible: !L.visible }) } }),
      h('div.nom', { role: 'button', tabIndex: 0, 'data-cible': 'calque-choisit-' + i, 'aria-current': i === ia ? 'true' : undefined,
        on: { click: () => act('calque.choisit', { i }), keydown: e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); act('calque.choisit', { i }); } } } },
        h('b', L.nom), h('small', nomType(L.type) + ' · ' + L.opacite + ' %' + (L.teinte === 'aucune' ? ' · sans teinte' : L.teinte ? ' · teinté' : ''))),
      h('button.btn.ico.fantome', { title: L.verrou ? 'Déverrouiller' : 'Verrouiller', 'aria-label': (L.verrou ? 'Déverrouiller ' : 'Verrouiller ') + L.nom, 'aria-pressed': String(L.verrou),
        'data-cible': 'calque-verrou-' + i, html: L.verrou ? CADENAS : CADENAS_NON, on: { click: () => act('calque.prop', { i, verrou: !L.verrou }) } })));
  }
  c.appendChild(liste);

  c.appendChild(h('div.ligne',
    btn('+ Calque', { cls: '.prim', cible: 'calque-ajoute', click: () => act('calque.ajoute', { type: 'normal' }) }),
    btn('+ Construction', { cible: 'calque-ajoute-construction', title: 'Formes simples, lignes d\'action : n\'est pas exporté', click: () => act('calque.ajoute', { type: 'construction', nom: 'construction' }) }),
    btn('+ Référence', { cible: 'calque-ajoute-reference', title: 'Image importée, jamais exportée', click: () => act('calque.ajoute', { type: 'reference', nom: 'référence' }) })));
  c.appendChild(h('div.ligne',
    btn('Monter', { cls: '.fantome', cible: 'calque-monte', inactif: ia >= d.calques.length - 1, click: () => act('calque.deplace', { sens: 1 }) }),
    btn('Descendre', { cls: '.fantome', cible: 'calque-descend', inactif: ia <= 0, click: () => act('calque.deplace', { sens: -1 }) }),
    btn('Dupliquer', { cls: '.fantome', cible: 'calque-duplique', click: () => act('calque.duplique') }),
    btn('Fusionner ↓', { cls: '.fantome', cible: 'calque-fusionne', inactif: ia <= 0, title: 'Fusionne avec le calque du dessous', click: () => act('calque.fusionne') }),
    btn('Ramener à la palette', { cls: '.fantome', cible: 'calque-indexe', title: 'Chaque pixel du calque prend la couleur de palette la plus proche (après des passes en opacité, 0-AF)', click: () => act('calque.indexe') }),
    btn('Supprimer', { cls: '.fantome', cible: 'calque-supprime', inactif: d.calques.length <= 1, click: async () => {
      if (await U.confirme('Supprimer le calque', 'Le calque « ' + ca.nom + ' » et ses pixels sur toutes les images seront supprimés. Ctrl+Z annule.', 'Supprimer')) act('calque.supprime');
    } })));

  if (ca) {
    c.appendChild(titre('Calque actif'));
    const nom = champ('text', ca.nom, { label: 'Nom du calque', cible: 'calque-nom', change: v => act('calque.prop', { nom: v }) });
    const type = champ('select', ca.type, { options: TYPES_CALQUE, label: 'Type du calque', cible: 'calque-type', change: v => act('calque.prop', { type: v }) });
    const op = champ('range', String(ca.opacite), { min: 0, max: 100, step: 5, label: 'Opacité', cible: 'calque-opacite',
      input: (v, el) => { el.nextSibling.textContent = v + ' %'; }, change: v => act('calque.prop', { opacite: +v }) });
    c.appendChild(h('div.form-fiche',
      h('label', 'Nom', nom),
      h('label', 'Type', type, h('small', ca.type === 'construction' ? 'Visible pendant le travail, absent de l\'export et des contrôles.'
        : ca.type === 'reference' ? 'Pour copier à côté, jamais par-dessus (G2). Jamais exporté.' : 'Exporté et contrôlé.')),
      h('label', 'Opacité', h('div.ligne', op, h('span.mono.aide-txt', ca.opacite + ' %'))),
      ca.type !== 'normal' ? h('label', 'Teinte d\'affichage',
        h('div.ligne', h('input', { type: 'color', value: (ca.teinte && ca.teinte !== 'aucune') ? ca.teinte : '#5a6fae', 'data-cible': 'calque-teinte', 'aria-label': 'Teinte du calque',
          on: { change: e => act('calque.prop', { teinte: e.target.value }) } }),
          // « Sans teinte » : les vraies couleurs (esquisse en valeurs, itérations) ; « Bleu » : la teinte par défaut
          btn('Sans teinte', { cls: '.fantome', cible: 'calque-teinte-aucune', inactif: ca.teinte === 'aucune', click: () => act('calque.prop', { teinte: 'aucune' }) }),
          btn('Bleu', { cls: '.fantome', cible: 'calque-teinte-defaut', inactif: !ca.teinte, click: () => act('calque.prop', { teinte: null }) }))) : null));
  }

  if (AP.typeDe(d) === 'animation' || d.type === 'animation') {
    c.appendChild(titre('Pile d\'animation (E6)'));
    c.appendChild(h('p.aide-txt', 'Crée la pile fixe : référence, ombre, bras arrière, corps, bras avant, effets, éclat, pivot.'));
    c.appendChild(btn('Créer la pile E6', { cible: 'calque-pile-e6', click: () => act('calque.pileE6') }));
  }
  c.appendChild(h('p.aide-txt', { style: { marginTop: '14px' } }, 'Le calque actif est entouré. Les calques de construction et de référence ne sont ni exportés ni contrôlés.'));
}
LEGERS.calques = c => {
  const A = at(), d = A.doc;
  for (const cv of $$('canvas[data-calque]', c)) {
    const i = +cv.dataset.calque, px = A.cel(i, A.s.image);
    const x = cv.getContext('2d');
    if (px) U.pxVersCanvas(cv, px, d.w, d.h); else x.clearRect(0, 0, cv.width, cv.height);
  }
};

/* ======================================================================
 * MÉTHODE
 * ==================================================================== */
const DETECTEURS = new Set(['L', 'jaggies', 'orphelins', 'bandes', 'coussin', 'bruit', 'trame', 'superpixels', 'budget', 'noirPur', 'rampesGris', 'raccords', 'alpha', 'lumiere', 'volume', 'tampons']);
let reglesOuvertes = false;

/* Passe à la loupe : grille des zones à retravailler, une par une. */
function rendLoupe(c, tuileSeule) {
  const d = at().doc, Z = d.meta.zones || { taille: 16, faites: {} }, t = Z.taille || 16;
  const L = AP.zonesAFaire(d, tuileSeule), faites = L.filter(k => Z.faites[k]).length;
  c.appendChild(titre('Passe à la loupe', h('span.mono.aide-txt', faites + ' / ' + L.length + ' zones')));
  c.appendChild(h('p.aide-txt', 'Va dans une zone (la toile s\'y cadre), retravaille chaque élément comme un dessin entier (0-AE), puis marque-la. Ne marque une zone que si elle a vraiment été reprise.'));
  c.appendChild(h('div.mods', btn('Zones de 8 px', { cible: 'zones-taille-8', presse: t === 8, click: () => act('zones.taille', { taille: 8 }) }),
    btn('Zones de 16 px', { cible: 'zones-taille-16', presse: t === 16, click: () => act('zones.taille', { taille: 16 }) })));
  const grille = h('div.zones-grille', { 'data-cible': 'zones' });
  const cour = U.vue.zone;
  for (const k of L) {
    const [zx, zy] = k.split(':')[1].split(',').map(Number), fait = !!Z.faites[k], ici = cour && cour.x === zx && cour.y === zy && cour.t === t;
    grille.appendChild(h('button.zone' + (fait ? '.faite' : '') + (ici ? '.ici' : ''), { 'data-cible': 'zone-' + zx + '-' + zy, title: 'Zone ' + zx + ',' + zy + ' (x ' + zx * t + ', y ' + zy * t + ')',
      on: { click: () => { U.cadreZone && U.cadreZone(zx, zy, t); rendu(true); } } }, fait ? '✓' : zx + ',' + zy));
  }
  c.appendChild(grille);
  if (cour && cour.t === t) {
    const k = t + ':' + cour.x + ',' + cour.y, fait = !!Z.faites[k];
    c.appendChild(h('div.ligne', { style: { marginTop: '6px' } },
      btn(fait ? 'Zone ' + cour.x + ',' + cour.y + ' : rouvrir' : 'Zone ' + cour.x + ',' + cour.y + ' retravaillée', { cls: fait ? '.fantome' : '.prim', cible: 'zone-faite', click: () => act('zones.marque', { x: cour.x, y: cour.y, faite: !fait }) }),
      btn('Vue entière', { cls: '.fantome', cible: 'zone-sortie', click: () => { U.vue.zone = null; U.ajuste(); rendu(true); } })));
  }
}

/* Carnet de conception (0-N) : chaque idée reste, une idée abandonnée est barrée avec sa raison. */
let carnetRubrique = 'vision';
function rendCarnet(c, saisie) {
  const m = at().doc.meta, L = m.carnet || [], R = AP.RUBRIQUES;
  c.appendChild(titre('Carnet de conception', h('span.mono.aide-txt', L.filter(x => !x.barre).length + ' idée(s) · ' + L.filter(x => x.barre).length + ' barrée(s)')));
  c.appendChild(h('p.aide-txt', 'Une idée à la fois. Rien ne s\'efface : barre ce qui ne tient pas et écris pourquoi. Le carnet raconte comment le dessin a été pensé (0-N).'));
  const liste = h('ol.carnet-liste', { 'data-cible': 'carnet' });
  L.forEach((x, i) => {
    const li = h('li.idee' + (x.barre ? '.idee-barree' : ''), { 'data-cible': 'carnet-' + i },
      h('span.rub', R[x.rubrique] || x.rubrique), h('p', x.texte),
      x.barre ? h('small', 'Barrée : ' + x.raison) : null);
    if (saisie && !x.barre) {
      const raison = champ('input', '', { cible: 'carnet-raison-' + i, label: 'Pourquoi barrer l\'idée ' + (i + 1), placeholder: 'Pourquoi je l\'abandonne' });
      li.appendChild(h('div.ligne', raison, btn('Barrer', { cls: '.fantome', cible: 'carnet-barre-' + i, click: () => act('carnet.barre', { i, raison: raison.value }) })));
    }
    liste.appendChild(li);
  });
  if (L.length) c.appendChild(liste);
  if (!saisie) return;
  const rub = h('div.mods.rubriques', { role: 'group', 'aria-label': 'Rubrique' });
  for (const k in R) rub.appendChild(btn(R[k], { cible: 'carnet-rub-' + k, presse: carnetRubrique === k, click: () => { carnetRubrique = k; rendu(true); } }));
  const zone = champ('textarea', '', { rows: 3, cible: 'carnet-texte', label: 'Nouvelle idée', placeholder: 'Une idée, et pourquoi.' });
  c.appendChild(h('div.pile', rub, zone, h('div.ligne', btn('Ajouter au carnet', { cls: '.prim', cible: 'carnet-ajoute', click: () => { const r = act('carnet.ajoute', { rubrique: carnetRubrique, texte: zone.value }); if (!(r && r.refus)) zone.value = ''; } }))));
}
U.rendCarnet = rendCarnet;

function rendMethode(c) {
  const A = at(), d = A.doc, m = d.meta, st = AP.etatEtape(A), e = st.etape, T = AP.TYPES[AP.typeDe(d)];
  const claude = A.mode === 'claude';

  c.appendChild(titre(T.nom + ' · ' + T.ref, h('span.mono.aide-txt', st.fini ? 'terminé' : 'étape ' + (st.index + 1) + '/' + st.total)));

  if (st.fini) {
    c.appendChild(h('div.etape-carte', { 'data-cible': 'etape-carte' }, h('h4', 'Toutes les étapes sont validées'),
      h('p', 'Exporte le dessin et la planche (Fichier → Exporter). Rejoue la séance pour voir ton chemin.'),
      h('div.ligne', btn('Exporter', { cls: '.prim', cible: 'methode-exporte', click: () => U.modaleExport && U.modaleExport() }),
        btn('Revoir la séance', { cible: 'methode-seance', click: () => ouvreOnglet('seance') }))));
  } else {
    /* Carte d'étape */
    const carte = h('div.etape-carte', { 'data-cible': 'etape-carte' },
      h('h4', e.titre), h('span.mono.aide-txt', 'Méthode ' + e.ref),
      h('ol', e.faire.map(x => h('li', x))),
      e.pasEncore ? h('p.aide-txt', h('b', 'Pas encore : '), e.pasEncore) : null);
    if (e.outils && e.outils.length) carte.appendChild(h('div.ligne', h('span.aide-txt', 'Outils :'),
      e.outils.map(o => btn((U.NOMS_OUTILS && U.NOMS_OUTILS[o]) || o, { cls: '.fantome', presse: A.s.outil === o, cible: 'etape-outil-' + o, click: () => act('outil', { nom: o }) }))));
    c.appendChild(carte);

    /* Champs que certaines portes demandent ici même */
    if (e.portes.includes('analyse')) {
      c.appendChild(titre('Analyse de la pièce'));
      c.appendChild(h('p.aide-txt', 'Avant de copier : nombre de couleurs, rampes, lumière, contour, selout, AA, trame.'));
      c.appendChild(champ('textarea', m.planche.analyse || '', { rows: 5, cible: 'planche-analyse', label: 'Analyse',
        change: v => act('planche.reponse', { cle: 'analyse', texte: v }) }));
    }
    if (st.index === 0 || e.portes.includes('fiche')) rendFiche(c);
    if (e.portes.includes('regles')) {
      c.appendChild(titre('Les 92 règles', m.reglesLues ? h('span.aide-txt', { style: { color: 'var(--ok)' } }, 'lues ✓') : null));
      c.appendChild(h('p.aide-txt', 'Elles s\'appliquent à chaque dessin. Lis-les toutes avant de confirmer.'));
      c.appendChild(h('div.ligne',
        btn(reglesOuvertes ? 'Replier les règles' : 'Lire les règles', { cible: 'regles-ouvre', click: () => { reglesOuvertes = !reglesOuvertes; rendu(true); } }),
        btn(m.reglesLues ? 'Règles lues ✓' : 'J\'ai lu les 92 règles', { cls: m.reglesLues ? '.fantome' : '.prim', cible: 'regles-lues', inactif: m.reglesLues || !reglesOuvertes,
          title: reglesOuvertes ? '' : 'Ouvre d\'abord les règles', click: () => act('regles.lues') })));
      if (reglesOuvertes) c.appendChild(listeRegles());
    }

    const etapeCarnet = e.portes.some(p => /^carnet/.test(p));
    if (etapeCarnet) rendCarnet(c, true);

    /* Portes */
    c.appendChild(titre('Portes de l\'étape', h('span.aide-txt', claude ? 'bloquantes' : 'conseils')));
    if (!st.portes.length && !st.coches.length) c.appendChild(h('p.aide-txt', 'Aucune porte : valide quand tu es prêt.'));
    const portes = h('div.portes', { 'data-cible': 'portes' });
    for (const p of st.portes) {
      const just = m.justifs && m.justifs[p.id];
      const ok = !p.manque || (DETECTEURS.has(p.id) && just);
      const ligne = h('div.porte' + (ok ? '.ok' : '.non'), { 'data-cible': 'porte-' + p.id },
        h('span.i', ok ? '✓' : '!'),
        h('div', h('span', p.nom), p.manque ? h('small', p.manque) : null, just ? h('small', 'Justifié : « ' + just + ' »') : null));
      portes.appendChild(ligne);
      // Planche : chaque défaut restant peut être justifié ici (le détecteur peut se tromper, CLAUDE.md règle 5).
      if (p.manque && p.id === 'defauts') {
        const restants = AP.detecte(d, A.s.image).filter(x => x.niveau !== 'conseil' && !(m.justifs && m.justifs[x.id]));
        for (const x of restants) portes.appendChild(h('div', { style: { gridColumn: '1 / -1', margin: '0 0 6px 26px' } },
          h('small', x.titre), champ('textarea', '', { rows: 2, cible: 'justifie-' + x.id, label: 'Justifier ' + x.titre,
            placeholder: 'Si le détecteur se trompe, écris pourquoi (12 caractères au moins).', change: v => act('justifie', { cle: x.id, texte: v }) })));
      }
      if (p.manque && DETECTEURS.has(p.id)) {
        const zone = champ('textarea', just || '', { rows: 2, cible: 'justifie-' + p.id, label: 'Justifier ' + p.nom,
          placeholder: 'Si c\'est voulu, écris pourquoi en une phrase (12 caractères au moins).',
          change: v => act('justifie', { cle: p.id, texte: v }) });
        portes.appendChild(h('div', { style: { gridColumn: '1 / -1', margin: '0 0 6px 26px' } }, zone,
          h('div.ligne', btn('Montrer sur la toile', { cls: '.fantome', cible: 'porte-montre-' + p.id, click: () => montreDefaut(p.id) }))));
      }
    }
    c.appendChild(portes);

    /* Passe à la loupe (0-AE, 0-AF) : chaque zone se retravaille, puis se marque. */
    const pz = st.portes.find(p => p.id === 'zonesTuile' || p.id === 'zonesToutes');
    if (pz) rendLoupe(c, pz.id === 'zonesTuile');

    /* Cases à cocher */
    if (st.coches.length) {
      c.appendChild(titre('Vérifications'));
      for (const k of st.coches) {
        const cb = h('input', { type: 'checkbox', checked: k.ok, 'data-cible': 'coche-' + k.cle, on: { change: ev => act('coche', { cle: k.cle, valeur: ev.target.checked }) } });
        c.appendChild(h('label.coche', cb, h('span', k.txt)));
      }
    }

    const v = AP.verifieEtape(A);
    c.appendChild(h('div.ligne', { style: { marginTop: '12px' } },
      btn(st.index + 1 >= st.total ? 'Valider la dernière étape' : 'Valider l\'étape', { cls: '.prim', cible: 'etape-valide', click: () => act('etape.valide') }),
      !v.ok ? h('span.aide-txt', v.manque.length + ' point' + (v.manque.length > 1 ? 's' : '') + ' en suspens' + (claude ? '' : ' (conseil)')) : h('span.aide-txt', { style: { color: 'var(--ok)' } }, 'Tout est prêt.')));
  }

  /* Liste des étapes */
  c.appendChild(titre('Étapes'));
  if ((m.methode || 0) < AP.METHODE_ACTUELLE)
    c.appendChild(h('div.ligne', { style: { margin: '0 0 8px' } }, btn('Passer à la méthode v' + AP.METHODE_ACTUELLE, { cls: '.fantome', cible: 'methode-migre', title: 'Garde l\'étape en cours ; les étapes nouvelles d\'avant restent à faire', click: () => act('methode.migre') }),
      h('span.aide-txt', 'Ce document suit la méthode v' + (m.methode || 16) + '.')));
  const L = h('div.etapes-liste', { 'data-cible': 'etapes' });
  AP.etapesDe(d).forEach((x, i) => {
    const fait = (m.valideEtapes || []).includes(x.id) || i < m.etape;
    L.appendChild(h('button' + (i === m.etape ? '.cour' : ''), { 'data-cible': 'etape-' + i, 'aria-current': i === m.etape ? 'step' : undefined,
      disabled: claude && i > m.etape, on: { click: () => act('etape.va', { i }) } },
      h('span.n', String(i + 1).padStart(2, '0')), h('span', x.titre), h('span.s', { style: { color: fait ? 'var(--ok)' : 'var(--fg-3)' } }, fait ? '✓' : x.ref)));
  });
  c.appendChild(L);

  /* Table A3 */
  const col = AP.colonneA3(d);
  c.appendChild(titre('Budget par taille (A3)', h('span.mono.aide-txt', d.w + '×' + d.h)));
  c.appendChild(h('div.defile-x', h('table.tableau',
    h('thead', h('tr', h('th', ''), AP.TABLE_A3.colonnes.map((t, j) => h('th' + (j === col ? '.cour' : ''), t)))),
    h('tbody', AP.TABLE_A3.lignes.map(l => h('tr', h('th', l[0]), l.slice(1).map((t, j) => h('td' + (j === col ? '.cour' : ''), t))))))));

  if (!(st.index === 0 || e.portes.includes('fiche')) || st.fini) {
    c.appendChild(titre('Fiche d\'intention'));
    const det = h('details', h('summary', { style: { cursor: 'pointer', color: 'var(--fg-2)' } }, 'Revoir ou corriger la fiche'));
    rendFiche(det, true);
    c.appendChild(det);
  }
  if (!st.fini && !st.etape.portes.some(p => /^carnet/.test(p))) rendCarnet(c, true);
}

function rendFiche(c, sansTitre) {
  const d = at().doc, f = d.meta.fiche || {};
  if (!sansTitre) c.appendChild(titre('Fiche d\'intention', h('span.aide-txt', AP.ficheIncomplete(d) ? 'à compléter' : 'complète ✓')));
  const form = h('div.form-fiche', { 'data-cible': 'fiche' });
  form.appendChild(h('label', 'Type de dessin',
    champ('select', d.type, { options: Object.keys(AP.TYPES).map(k => [k, AP.TYPES[k].nom + ' (' + AP.TYPES[k].ref + ')']), cible: 'fiche-type',
      change: async (v, el) => {
        if (v === d.type) return;
        if (await U.confirme('Changer de type', 'Les étapes changent avec le type. La fiche et les pixels sont gardés.', 'Changer', false)) act('fiche', { type: v });
        else el.value = d.type;
      } }),
    h('small', 'Chaque type a ses propres étapes et questions de planche.')));
  for (const ch of AP.FICHES[AP.typeDe(d)]) {
    const v = f[ch.cle] ?? '';
    const ctl = ch.type === 'choix' ? champ('select', v, { options: [['', '—']].concat(ch.options || []), cible: 'fiche-' + ch.cle, label: ch.label })
      : ch.type === 'nombre' ? champ('number', v, { cible: 'fiche-' + ch.cle, label: ch.label })
      : (ch.long ? champ('textarea', v, { rows: 2, cible: 'fiche-' + ch.cle, label: ch.label }) : champ('text', v, { cible: 'fiche-' + ch.cle, label: ch.label }));
    ctl.addEventListener('change', () => act('fiche', { champs: { [ch.cle]: ctl.value } }));
    form.appendChild(h('label', h('span', ch.label, ch.requis ? h('span.req', { title: 'obligatoire' }, ' *') : null), ctl, ch.aide ? h('small', ch.aide) : null));
  }
  c.appendChild(form);
}

let reglesCache = null;
function listeRegles() {
  if (!reglesCache) reglesCache = AP.DOC_METHODE ? AP.extraitRegles(AP.DOC_METHODE) : [];
  const box = h('div', { 'data-cible': 'regles' });
  if (!reglesCache.length) { box.appendChild(h('p.aide-txt', 'Texte de la méthode absent de cette version : ouvre l\'onglet Aide.')); return box; }
  let g = null;
  for (const r of reglesCache) {
    if (r.groupe !== g) { g = r.groupe; box.appendChild(h('div.regle-groupe', g)); }
    box.appendChild(h('div.regle', h('b', String(r.n)), h('span', { html: inline(r.texte) })));
  }
  return box;
}
/* Gras, italique et code en ligne d'une phrase de la méthode (texte échappé d'abord). */
function inline(t) {
  return String(t).replace(/[&<>]/g, x => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[x]))
    .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>').replace(/\*([^*]+)\*/g, '<em>$1</em>').replace(/`([^`]+)`/g, '<code>$1</code>');
}
U.inline = inline;

/* ======================================================================
 * CONTRÔLE
 * ==================================================================== */
let defautsCache = null, defautsCle = '', montre = null;

function composeExport() { const A = at(); return AP.compose(A.doc, A.s.image, 'export'); }
function vues() {
  const A = at(), d = A.doc, px = composeExport(), V = AP.VUES, w = d.w, hh = d.h;
  const moins = V.uneCouleurDeMoins(px);
  return [
    { id: 'x1', nom: '×1', px, k: 1 },
    { id: 'x2', nom: '×2', px, k: 2 },
    { id: 'gris', nom: 'Gris', px: V.gris(px) },
    { id: 'notan', nom: 'Notan', px: AP.VOLUME.notan(px) },
    { id: 'guide', nom: 'Guide de volume', px: pxGuide(px, w, hh, AP.VOLUME.lumiereDe(d)) },
    { id: 'silhouette', nom: 'Silhouette', px: V.silhouette(px) },
    { id: 'miroir', nom: 'Miroir', px: V.miroir(px, w, hh) },
    { id: 'flou', nom: 'Plissé', px: V.flou(px, w, hh, Math.max(1, Math.round(Math.max(w, hh) / 32))) },
    { id: 'moins', nom: moins.de == null ? '1 couleur de moins' : '− ' + AP.hex(moins.de) + ' → ' + AP.hex(moins.vers), px: moins.px },
    { id: 'clair', nom: 'Fond clair', px: V.surFond(px, V.FONDS.clair) },
    { id: 'moyen', nom: 'Fond moyen', px: V.surFond(px, V.FONDS.moyen) },
    { id: 'sombre', nom: 'Fond sombre', px: V.surFond(px, V.FONDS.sombre) }
  ];
}
/* Le guide de volume en image : chaque zone a sa couleur (légende dans l'onglet Lumière). */
function pxGuide(px, w, hh, lum) {
  const g = AP.VOLUME.guide(px, w, hh, lum), o = new Uint32Array(w * hh);
  const C = AP.VOLUME.ZONES.map(z => z.coul ? AP.parseHex(z.coul) : 0);
  for (let i = 0; i < o.length; i++) if (g.zone[i]) o[i] = C[g.zone[i]];
  return o;
}
U.pxGuide = pxGuide;
function dessineVue(cv, v, w, hh) {
  U.pxVersCanvas(cv, v.px, w, hh);
  const k = v.k || Math.max(1, Math.floor(88 / Math.max(w, hh)));
  const kk = v.k ? v.k : Math.min(k, 4);
  // hauteur automatique : si max-width rétrécit la vue, elle garde ses proportions
  cv.style.width = (w * kk) + 'px'; cv.style.height = 'auto'; cv.style.aspectRatio = w + ' / ' + hh;
}
function detecteCache() {
  const A = at(), cle = A.journal.length + ':' + A.s.image + ':' + A.doc.w + 'x' + A.doc.h;
  if (cle !== defautsCle) { defautsCle = cle; try { defautsCache = AP.detecte(A.doc, A.s.image); } catch (e) { console.error(e); defautsCache = []; } }
  return defautsCache;
}
function montreDefaut(id, idx) {
  const L = detecteCache().filter(x => x.id === id);
  const pts = []; for (const x of (idx === undefined ? L : [L[idx]])) if (x) pts.push(...(x.pixels || []));
  if (!pts.length) { U.toast('Rien à montrer pour ce contrôle.'); return; }
  montre = id + ':' + (idx ?? '*');
  U.marques = { pixels: pts, niveau: (L[0] && L[0].niveau) || 'attention' };
  U.redessine();
  U.toast(pts.length + ' pixel' + (pts.length > 1 ? 's' : '') + ' marqué' + (pts.length > 1 ? 's' : '') + '. Échap efface les marques.');
  if (etroit()) basculePanneau(false);
}

function rendControle(c) {
  const A = at(), d = A.doc, w = d.w, hh = d.h;
  c.appendChild(titre('Vues de contrôle', h('span.aide-txt', 'image ' + (A.s.image + 1))));
  c.appendChild(h('p.aide-txt', 'Ce qui sera exporté, vu autrement. Les calques de construction et de référence sont exclus.'));
  const box = h('div.vues', { 'data-cible': 'vues' });
  for (const v of vues()) {
    const cv = h('canvas', { 'data-vue': v.id });
    dessineVue(cv, v, w, hh);
    box.appendChild(h('figure.vue', { 'data-cible': 'vue-' + v.id }, h('div', { style: { background: v.id === 'x1' || v.id === 'x2' || v.id === 'miroir' || v.id === 'silhouette' ? damier : 'none', lineHeight: 0 } }, cv), h('figcaption', v.nom)));
  }
  c.appendChild(box);

  /* Défauts */
  const L = detecteCache();
  const compte = { erreur: 0, attention: 0, conseil: 0 }; for (const x of L) compte[x.niveau]++;
  c.appendChild(titre('Défauts détectés', h('span.mono.aide-txt', compte.erreur + ' erreur · ' + compte.attention + ' attention · ' + compte.conseil + ' conseil')));
  if (!L.length) c.appendChild(h('p.aide-txt', { style: { color: 'var(--ok)' } }, 'Aucun défaut détecté sur cette image. Les détecteurs ne remplacent pas l\'œil : fais les tests pro ci-dessous.'));
  const box2 = h('div', { style: { display: 'grid', gap: '6px' }, 'data-cible': 'defauts' });
  const parId = {};
  L.forEach(x => { (parId[x.id] = parId[x.id] || []).push(x); });
  for (const id in parId) parId[id].forEach((x, j) => {
    const just = d.meta.justifs && d.meta.justifs[id];
    box2.appendChild(h('div.defaut.' + x.niveau + (montre === id + ':' + j ? '.montre' : ''), { 'data-cible': 'defaut-' + id + '-' + j },
      h('span.pt'),
      h('div', h('b', x.titre), h('span.mono.aide-txt', '  ' + (x.ref || '')), h('p', x.msg),
        just ? h('p.aide-txt', 'Justifié : « ' + just + ' »') : null),
      (x.pixels && x.pixels.length) ? btn('Montrer', { cls: '.fantome', cible: 'defaut-montre-' + id + '-' + j, click: () => { montreDefaut(id, j); rendu(true); } }) : h('span')));
  });
  c.appendChild(box2);
  if (U.marques) c.appendChild(h('div.ligne', btn('Effacer les marques', { cls: '.fantome', cible: 'marques-efface', click: () => { U.marques = null; montre = null; U.redessine(); rendu(true); } })));

  /* Tests pro */
  c.appendChild(titre('Tests pro'));
  for (const t of AP.TESTS_PRO) c.appendChild(h('div.test-pro', { 'data-cible': 'test-' + t.id },
    h('b', t.nom), h('span.mono.aide-txt', t.vue), h('small', 'Tu dois voir : ' + t.voir)));

  /* Planche */
  rendPlanche(c);
}
LEGERS.controle = c => {
  const A = at(), d = A.doc, cvs = $$('canvas[data-vue]', c); if (!cvs.length) return;
  const V = {}; for (const v of vues()) V[v.id] = v;
  for (const cv of cvs) if (V[cv.dataset.vue]) dessineVue(cv, V[cv.dataset.vue], d.w, d.h);
};

function rendPlanche(c) {
  const d = at().doc, p = d.meta.planche || {}, type = AP.typeDe(d);
  c.appendChild(titre('Planche de contrôle (A5-11)', h('span.aide-txt', 'réponds par écrit')));
  c.appendChild(h('p.aide-txt', 'Une réponse honnête par question. « Non » est une réponse utile : elle dit quoi corriger.'));
  const form = h('div.form-fiche', { 'data-cible': 'planche' });
  const q = (cle, label, rows = 2) => form.appendChild(h('label', h('span', label),
    champ('textarea', p[cle] || '', { rows, cible: 'planche-' + cle, label, change: v => act('planche.reponse', { cle, texte: v }) })));
  AP.QUESTIONS.forEach((t, i) => q('q' + i, (i + 1) + '. ' + t));
  (AP.QUESTIONS_TYPE[type] || []).forEach((t, i) => q('t' + i, AP.TYPES[type].ref + '. ' + t));
  q('reussi', 'Ce qui est réussi');
  q('ameliorer', 'Ce que je change la prochaine fois');
  if (type === 'etude') q('analyse', 'Analyse de la pièce (40 caractères au moins)', 4);
  c.appendChild(form);
  c.appendChild(h('div.ligne', btn('Exporter la planche', { cible: 'planche-exporte', click: () => U.modaleExport && U.modaleExport('planche') })));
}

/* ======================================================================
 * LUMIÈRE (partie 0-C) : direction, hauteur, forme, guide, mesure
 * ==================================================================== */
const ROSE = [['haut gauche', 'lum-hg', '↖'], ['haut', 'lum-h', '↑'], ['haut droite', 'lum-hd', '↗'],
  ['gauche', 'lum-g', '←'], [null, 'lum-c', '●'], ['droite', 'lum-d', '→'],
  ['bas gauche', 'lum-bg', '↙'], ['bas', 'lum-b', '↓'], ['bas droite', 'lum-bd', '↘']];
function rendLumiere(c) {
  const A = at(), d = A.doc, VO = AP.VOLUME, L = VO.lumiereDe(d), vue = U.vue;
  c.appendChild(titre('Lumière', h('span.aide-txt', d.lumiere && d.lumiere.posee ? 'posée' : 'pas encore posée')));
  c.appendChild(h('p.aide-txt', 'Une seule source, posée avant la première ombre (règle 50). Le guide montre où vont lumière, demi-ton, terminateur, ombre propre, rebond et ombre portée (0-C). Il ne dessine rien : tu poses chaque pixel.'));
  const dir = VO.nomDirection(L.az);
  const rose = h('div.rose', { role: 'group', 'aria-label': 'Direction de la lumière', 'data-cible': 'rose' });
  for (const [nom, cible, sym] of ROSE) {
    if (!nom) { rose.appendChild(h('span.rose-c', { title: 'L\'objet' }, sym)); continue; }
    rose.appendChild(btn(sym, { cible, title: 'Lumière ' + nom, presse: !!(d.lumiere && d.lumiere.posee) && dir === nom,
      click: () => act('lumiere', { az: VO.DIRECTIONS[nom] }) }));
  }
  const haut = h('div.mods', { role: 'group', 'aria-label': 'Hauteur de la lumière' });
  for (const k in VO.HAUTEURS) haut.appendChild(btn(k, { cible: 'lum-' + k, presse: Math.abs(L.el - VO.HAUTEURS[k]) < 8,
    click: () => act('lumiere', { el: VO.HAUTEURS[k], az: L.az }) }));
  const NOMS_F = { gonfle: 'silhouette gonflée', sphere: 'sphère', cylindre: 'cylindre' };
  const forme = h('div.mods', { role: 'group', 'aria-label': 'Forme imaginée' });
  for (const k of VO.FORMES) forme.appendChild(btn(NOMS_F[k], { cible: 'lum-forme-' + k, presse: L.forme === k, click: () => act('lumiere', { forme: k }) }));
  c.appendChild(h('div.lum-reglages', rose, h('div.pile',
    h('div', h('small.aide-txt', 'Hauteur'), haut),
    h('div', h('small.aide-txt', 'Forme du guide'), forme))));

  /* Sur la toile */
  c.appendChild(titre('Sur la toile'));
  const vues = h('div.mods', { role: 'group', 'aria-label': 'Vue de la toile' });
  for (const [k, t] of [['couleur', 'Couleur'], ['valeurs', 'Valeurs'], ['notan', 'Notan']])
    vues.appendChild(btn(t, { cible: 'vue-toile-' + k, presse: (vue.mode || 'couleur') === k, click: () => { vue.mode = k; U.redessine(); rendu(true); } }));
  c.appendChild(vues);
  c.appendChild(h('div.ligne', { style: { marginTop: '8px' } },
    btn(vue.miroir ? 'Remettre la toile à l\'endroit' : 'Retourner la toile', { cible: 'retourne', presse: !!vue.miroir, click: () => { U.retourne(); rendu(true); } }),
    btn(vue.guide ? 'Masquer le guide' : 'Afficher le guide', { cible: 'guide', presse: !!vue.guide, click: () => { vue.guide = !vue.guide; U.redessine(); rendu(true); } }),
    // grille de projection (0-AG) : les arêtes suivent la grille isométrique 2:1 du jeu
    btn(vue.grilleIso ? 'Masquer la grille iso' : 'Grille isométrique', { cible: 'grille-iso', presse: !!vue.grilleIso, title: 'Lignes 2:1 tous les ' + ((d.tuile && d.tuile.on ? d.tuile.tw : 16) / 2) + ' px de haut', click: () => { vue.grilleIso = !vue.grilleIso; U.redessine(); rendu(true); } })));
  c.appendChild(h('p.aide-txt', 'Le guide est calculé sur le calque courant (ou sur toute l\'image si le calque est vide). Valeurs et Notan aident à juger les deux familles (0-D).'));

  /* Légende */
  const leg = h('div.legende', { 'data-cible': 'legende' });
  for (const z of VO.ZONES) if (z.coul) leg.appendChild(h('span', h('i', { style: { background: z.coul } }), z.nom));
  c.appendChild(leg);

  /* Mesure */
  const px = AP.compose(d, A.s.image, 'export'), M = VO.mesure(px, d.w, d.h, L);
  const f2 = x => x === null ? '—' : x.toFixed(2);
  const ligne = (nom, val, ok, aide) => h('div.mesure' + (ok === null ? '' : ok ? '.ok' : '.ko'), h('b', nom), h('span.mono', val), h('small.aide-txt', aide));
  c.appendChild(titre('Le dessin suit-il la lumière ?', h('span.aide-txt', 'image ' + (A.s.image + 1))));
  c.appendChild(h('div.pile', { 'data-cible': 'mesure-volume' },
    ligne('Accord', f2(M.accord), M.accord === null ? null : M.accord >= 0.5, 'corrélation clarté / volume, par matière : 0,50 pour passer, 0,70 et plus = forme qui tourne'),
    ligne('Deux familles', f2(M.ecart), M.ecart === null ? null : M.ecart >= 0.08, 'clarté moyenne lumière − ombre : 0,08 au moins'),
    ligne('Inversions', M.inverses === null ? '—' : Math.round(M.inverses * 100) + ' %', M.inverses === null ? null : M.inverses <= 0.15, 'pixels côté lumière plus sombres que l\'ombre : 15 % au plus'),
    ligne('Étendue', f2(M.etendue), M.n < 12 ? null : M.etendue >= 0.45, 'du plus sombre au plus clair (5e-95e centile) : 0,45 au moins à 32 px et plus (règle 53)')));
  if (M.fautifs.length) c.appendChild(h('div.ligne', btn('Montrer les ' + M.fautifs.length + ' pixels du mauvais côté', { cible: 'lum-fautifs', click: () => { U.marques = { pixels: M.fautifs, niveau: 'attention' }; U.redessine(); } })));
}
LEGERS.lumiere = () => { planifie(); };

/* ---------- Branchement ---------- */
Object.assign(RENDUS, { couleurs: rendCouleurs, calques: rendCalques, methode: rendMethode, controle: rendControle, lumiere: rendLumiere });

function initPanneaux() {
  const onglets = $('#onglets');
  onglets.addEventListener('click', e => { const b = e.target.closest('.onglet'); if (b) ouvreOnglet(b.dataset.onglet, { ouvre: false }); });
  onglets.addEventListener('keydown', e => {
    if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
    const L = $$('.onglet', onglets), i = L.findIndex(b => b.getAttribute('aria-selected') === 'true');
    const n = L[(i + (e.key === 'ArrowRight' ? 1 : -1) + L.length) % L.length];
    ouvreOnglet(n.dataset.onglet, { ouvre: false }); n.focus(); e.preventDefault();
  });
  $('#contenu').addEventListener('focusout', () => setTimeout(() => { if (enAttente && !champActif()) rendu(false); }, 0));
  $('#contenu').addEventListener('pointerdown', () => { doigtPose = true; });
  const leve = () => { if (!doigtPose) return; setTimeout(() => { doigtPose = false; if (enAttente && !champActif()) rendu(false); }, 0); };
  window.addEventListener('pointerup', leve); window.addEventListener('pointercancel', leve);
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && etroit() && $('#app').classList.contains('panneau-ouvert') && !U.modaleOuverte && !U.menuOuvert) basculePanneau(false);
  });
  U.at.ecoute((quoi) => {
    if (quoi === 'pixels' || quoi === 'trait') { leger(); return; }
    if (quoi === 'etat' || quoi === 'doc' || quoi === 'act' || quoi === 'methode' || quoi === 'carte') {
      if (quoi !== 'etat') defautsCle = '';
      if (quoi === 'etat' && courant !== 'couleurs' && courant !== 'calques' && courant !== 'methode' && courant !== 'lumiere') { leger(); return; }
      planifie(); majPastille();
    }
  });
  if (!courant) ouvreOnglet(U.stocke.lis('onglet', 'methode'), { ouvre: false });
  majPastille();
}
/* Après un changement de document (Nouveau, Ouvrir) : tout reconstruire. */
function rafraichitPanneau() { hsv = null; defautsCle = ''; montre = null; rendu(true); majPastille(); }

Object.assign(U, { ouvreOnglet, basculePanneau, initPanneaux, rafraichitPanneau, rendPanneau: rendu, montreDefaut,
  get ongletCourant() { return courant; } });
})(window);
