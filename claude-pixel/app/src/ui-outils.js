/* Claude Pixel — interface : rail d'outils, barre de réglages, couleurs actives,
 * barre du haut, menu Fichier (nouveau, ouvrir, enregistrer, exports, import). */
(function (G) {
'use strict';
const AP = G.AP, U = AP.UI;
const { $, h } = U;

/* ---------- Action avec retour visible ---------- */
U.act = function (nom, a) {
  const r = U.at.act(nom, a);
  if (r && r.refus) U.alertePorte(r.refus);
  U.redessine();
  return r;
};

/* ---------- Icônes (24×24, tracés droits pour rester nets) ---------- */
const S = 'fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="miter" stroke-linecap="square"';
const ICONES = {
  crayon: `<path d="M4 20l1-5L15 5l4 4L9 19z"/><path d="M13 7l4 4"/>`,
  gomme: `<path d="M4 16l8-8 7 7-4 4H8z"/><path d="M9 11l6 6"/><path d="M14 20h6"/>`,
  ligne: `<path d="M5 19L19 5"/><rect x="3" y="17" width="4" height="4" fill="currentColor" stroke="none"/><rect x="17" y="3" width="4" height="4" fill="currentColor" stroke="none"/>`,
  rect: `<rect x="4" y="6" width="16" height="12"/>`,
  ellipse: `<ellipse cx="12" cy="12" rx="8" ry="6"/>`,
  seau: `<path d="M5 10l7-6 7 7-7 7z"/><path d="M5 10h14"/><path d="M20 14v4"/>`,
  pipette: `<path d="M15 4l5 5-3 3-5-5z"/><path d="M12 8l-7 7v4h4l7-7"/>`,
  selrect: `<rect x="4" y="5" width="16" height="14" stroke-dasharray="3 2"/>`,
  lasso: `<path d="M6 15c-3-3-1-9 6-9s9 5 6 8-7 3-9 2" stroke-dasharray="3 2"/><path d="M8 16l-2 5"/>`,
  baguette: `<path d="M4 20L15 9"/><path d="M17 3v4M15 5h4M20 10v2M19 11h2M11 3v2M10 4h2"/>`,
  deplace: `<path d="M12 3v18M3 12h18"/><path d="M9 6l3-3 3 3M9 18l3 3 3-3M6 9l-3 3 3 3M18 9l3 3-3 3"/>`,
  ombrage: `<rect x="4" y="4" width="16" height="16"/><path d="M12 4v16M12 8h8M12 12h8M12 16h8" />`,
  remplace: `<rect x="3" y="3" width="8" height="8"/><rect x="13" y="13" width="8" height="8" fill="currentColor" stroke="none"/><path d="M15 5h3v3M9 19H6v-3"/>`,
  degrade: `<rect x="4" y="4" width="16" height="16"/><rect x="4" y="4" width="4" height="16" fill="currentColor" stroke="none"/><rect x="8" y="4" width="4" height="16" fill="currentColor" stroke="none" opacity=".6"/><rect x="12" y="4" width="4" height="16" fill="currentColor" stroke="none" opacity=".3"/>`
};
const NOMS_OUTILS = {
  crayon: 'Crayon', gomme: 'Gomme', ligne: 'Ligne', rect: 'Rectangle', ellipse: 'Ellipse', seau: 'Pot de peinture',
  pipette: 'Pipette', selrect: 'Sélection rectangle', lasso: 'Lasso', baguette: 'Baguette magique', deplace: 'Déplacer',
  ombrage: 'Encre d\'ombrage', remplace: 'Remplacer une couleur', degrade: 'Dégradé tramé'
};
const AIDES_OUTILS = {
  crayon: 'Clic : C1 · clic droit : C2 · Maj : ligne depuis le dernier point',
  gomme: 'Efface vers le transparent',
  ligne: 'Maj : angles pixel art (1:1, 2:1, 1:2…)',
  rect: 'Maj : carré', ellipse: 'Maj : cercle',
  seau: 'Remplit la zone de même couleur',
  pipette: 'Clic : C1 · clic droit : C2',
  selrect: 'Maj : ajoute · Alt : retire', lasso: 'Trace un contour fermé', baguette: 'Sélectionne une zone de couleur',
  deplace: 'Glisse la sélection ou le calque',
  ombrage: 'Clic : une marche plus claire dans la rampe · clic droit : plus sombre',
  remplace: 'Clic : remplace la couleur cliquée par C1 partout',
  degrade: 'Glisse : dégradé tramé selon la rampe'
};
const ORDRE = [['crayon', 'gomme', 'ombrage'], ['ligne', 'rect', 'ellipse', 'degrade'], ['seau', 'remplace', 'pipette'], ['selrect', 'lasso', 'baguette', 'deplace']];
const TOUCHE = {}; for (const k in U.RACCOURCIS) TOUCHE[U.RACCOURCIS[k]] = k.toUpperCase();
const svg = (corps, cls = '') => `<svg viewBox="0 0 24 24" ${S} class="${cls}" aria-hidden="true">${corps}</svg>`;

/* ---------- Rail ---------- */
let c1b, c2b;
function initRail() {
  const rail = $('#rail'); rail.replaceChildren();
  ORDRE.forEach((g, i) => {
    if (i) rail.appendChild(h('div.sep'));
    for (const nom of g) {
      rail.appendChild(h('button.outil', {
        'data-cible': 'outil-' + nom, 'data-outil': nom, title: NOMS_OUTILS[nom] + ' (' + TOUCHE[nom] + ')',
        'aria-label': NOMS_OUTILS[nom], 'aria-pressed': 'false', html: svg(ICONES[nom]) + `<span class="k">${TOUCHE[nom]}</span>`,
        on: { click: () => U.act('outil', { nom }) }
      }));
    }
  });
  rail.appendChild(h('div.sep'));
  c1b = h('button.c1', { 'data-cible': 'couleur-c1', title: 'Couleur 1 (clic gauche) : ouvrir les couleurs', 'aria-label': 'Couleur 1', on: { click: () => U.ouvreOnglet && U.ouvreOnglet('couleurs') } });
  c2b = h('button.c2', { 'data-cible': 'couleur-c2', title: 'Couleur 2 (clic droit)', 'aria-label': 'Couleur 2', on: { click: () => U.ouvreOnglet && U.ouvreOnglet('couleurs') } });
  rail.appendChild(h('div.couleurs-actives', c1b, c2b,
    h('button.ech', { 'data-cible': 'couleur-echange', title: 'Échanger C1 et C2 (X)', 'aria-label': 'Échanger les couleurs', html: svg('<path d="M4 9h12l-3-3M20 15H8l3 3"/>'), on: { click: () => U.act('couleur.echange') } })));
}
function fondCouleur(c) {
  if (!(c >>> 24)) return 'repeating-conic-gradient(var(--damier-a) 0 25%, var(--damier-b) 0 50%) 0 0/10px 10px';
  return AP.hex(c);
}
function majRail() {
  const s = U.at.s;
  for (const b of document.querySelectorAll('#rail .outil')) b.setAttribute('aria-pressed', String(b.dataset.outil === s.outil));
  if (c1b) { c1b.style.background = fondCouleur(s.c1); c1b.title = 'C1 ' + AP.hex(s.c1); }
  if (c2b) { c2b.style.background = fondCouleur(s.c2); c2b.title = 'C2 ' + ((s.c2 >>> 24) ? AP.hex(s.c2) : 'transparent'); }
}

/* ---------- Barre de réglages de l'outil ---------- */
const opt = (cle, valeur) => U.act('option', { cle, valeur });
function caseOpt(cle, txt, titre) {
  return h('label', { title: titre || txt }, h('input', { type: 'checkbox', checked: !!U.at.s[cle], 'data-cible': 'opt-' + cle, on: { change: e => opt(cle, e.target.checked) } }), txt);
}
function nombreOpt(cle, txt, min, max, pas = 1) {
  return h('label', txt, h('input.champ.mono', { type: 'number', min, max, step: pas, value: U.at.s[cle], 'data-cible': 'opt-' + cle, on: { change: e => opt(cle, Number(e.target.value)) } }));
}
function choixOpt(cle, txt, options) {
  const sel = h('select.champ', { 'data-cible': 'opt-' + cle, on: { change: e => opt(cle, isNaN(+e.target.value) ? e.target.value : +e.target.value) } },
    options.map(([v, t]) => h('option', { value: v, selected: String(U.at.s[cle]) === String(v) }, t)));
  return h('label', txt, sel);
}
function modsOpt(cle, options) {
  return h('div.mods', { role: 'group' }, options.map(([v, t, titre]) => h('button.btn', {
    'aria-pressed': String(U.at.s[cle] === v), title: titre || t, 'data-cible': 'opt-' + cle + '-' + v, on: { click: () => opt(cle, v) }
  }, t)));
}
const V = () => h('span.v');
const TRAMES = [['aucune', 'Aucune'], ['t25', '25 %'], ['t50', '50 % (damier)'], ['t75', '75 %'], ['lignes', 'Lignes'], ['colonnes', 'Colonnes'], ['bayer', 'Bayer 4×4']];
function rampesOpt() {
  const r = U.at.doc.rampes;
  return choixOpt('rampe', 'Rampe', [[-1, r.length ? 'Toutes' : 'Aucune rampe']].concat(r.map((x, i) => [i, x.nom || 'Rampe ' + (i + 1)])));
}
function pinceauOpts(o) {
  const s = U.at.s, l = [nombreOpt('taille', 'Taille', 1, 16), modsOpt('forme', [['carre', '■', 'Carré'], ['rond', '●', 'Rond']])];
  if (o.pp) l.push(caseOpt('pp', 'Pixel parfait', 'Retire les coins doublés des traits à main levée (évite les « L »)'));
  if (s.pinceau) l.push(h('span.puce.ok', 'pinceau ' + s.pinceau.w + '×' + s.pinceau.h), h('button.btn', { 'data-cible': 'pinceau-retire', on: { click: () => U.act('pinceau.retire') } }, 'Retirer'));
  return l;
}
function trameOpts() {
  const l = [V(), choixOpt('trame', 'Trame', TRAMES)];
  if (U.at.s.trame === 'bayer') l.push(nombreOpt('bayer', 'Niveau', 0, 16));
  return l;
}
function symOpts() {
  const s = U.at.s, l = [V(), caseOpt('symX', 'Sym. ↔', 'Symétrie gauche-droite (K)'), caseOpt('symY', 'Sym. ↕', 'Symétrie haut-bas')];
  if (s.symX) l.push(h('label', 'axe x', h('input.champ.mono', { type: 'number', step: 0.5, min: 0, max: U.at.doc.w, value: s.axeX2 / 2, 'data-cible': 'opt-axeX2', on: { change: e => opt('axeX2', Math.round(Number(e.target.value) * 2)) } })));
  if (s.symY) l.push(h('label', 'axe y', h('input.champ.mono', { type: 'number', step: 0.5, min: 0, max: U.at.doc.h, value: s.axeY2 / 2, 'data-cible': 'opt-axeY2', on: { change: e => opt('axeY2', Math.round(Number(e.target.value) * 2)) } })));
  return l;
}
function regionOpts(tous = true) {
  const l = [nombreOpt('tolerance', 'Tolérance', 0, 255), caseOpt('contigu', 'Contigu', 'Décoché : toutes les zones de même couleur')];
  if (tous) l.push(caseOpt('tousCalques', 'Tous les calques', 'Lit l\'image composée, pas seulement le calque actif'));
  return l;
}
function selOpts() {
  const s = U.at.s, l = [];
  l.push(h('button.btn', { 'data-cible': 'sel-tout', on: { click: () => U.act('selection.tout') } }, 'Tout'),
    h('button.btn', { 'data-cible': 'sel-rien', disabled: !s.selection, on: { click: () => U.act('selection.rien') } }, 'Rien'),
    h('button.btn', { 'data-cible': 'sel-inverse', on: { click: () => U.act('selection.inverse') } }, 'Inverser'));
  if (s.selection) l.push(V(), h('button.btn', { 'data-cible': 'pinceau-capture', title: 'La sélection devient un pinceau (32×32 au plus)', on: { click: () => U.act('pinceau.capture') } }, 'En pinceau'),
    h('button.btn.danger', { 'data-cible': 'sel-efface', on: { click: () => U.act('efface') } }, 'Effacer'));
  return l;
}
function majOptions() {
  const s = U.at.s, o = s.outil, l = [h('span.nom-outil', NOMS_OUTILS[o])];
  switch (o) {
    case 'crayon': l.push(...pinceauOpts({ pp: true }), ...trameOpts(), ...symOpts(), V(), caseOpt('verrouAlpha', 'Verrou alpha', 'Ne peint que sur les pixels déjà opaques')); break;
    case 'gomme': l.push(...pinceauOpts({ pp: true }), ...symOpts()); break;
    case 'ombrage': l.push(...pinceauOpts({ pp: true }), V(), rampesOpt(), ...symOpts()); break;
    case 'ligne': l.push(nombreOpt('taille', 'Taille', 1, 16), ...trameOpts(), ...symOpts()); break;
    case 'rect': case 'ellipse': l.push(caseOpt('rempli', 'Rempli'), nombreOpt('taille', 'Trait', 1, 16), ...trameOpts(), ...symOpts()); break;
    case 'seau': l.push(...regionOpts(), ...trameOpts()); break;
    case 'remplace': break; // remplace toujours partout, à l'identique : ni tolérance ni contiguïté
    case 'degrade': l.push(rampesOpt(), caseOpt('contigu', 'Zone contiguë')); break;
    case 'pipette': l.push(caseOpt('tousCalques', 'Image composée', 'Décoché : lit seulement le calque actif')); break;
    case 'baguette': l.push(...regionOpts(), V(), ...selOpts()); break;
    case 'selrect': case 'lasso': case 'deplace': l.push(...selOpts()); break;
  }
  if (AIDES_OUTILS[o]) l.push(V(), h('span.aide-txt', { style: { color: 'var(--fg-3)', fontSize: '12px' } }, AIDES_OUTILS[o]));
  $('#options').replaceChildren(...l);
}

/* ---------- Barre du haut ---------- */
function majBarre() {
  const at = U.at, d = at.doc, t = $('#titre-doc');
  if (document.activeElement !== t) t.value = d.nom;
  $('#b-annule').disabled = !at.hist.length;
  $('#b-refait').disabled = !at.futur.length;
  $('#b-zoom').textContent = '×' + U.vue.zoom;
  const st = AP.etatEtape(at), chip = $('#etape-chip');
  chip.querySelector('b').textContent = st.fini ? '✓' : (st.index + 1) + '/' + st.total;
  chip.querySelector('span').textContent = st.fini ? 'Méthode terminée' : st.etape.titre;
  const bloque = !st.fini && st.portes.some(p => p.manque);
  chip.title = 'Étape ' + (st.index + 1) + ' : ' + st.etape.titre + (bloque ? ' — portes à ouvrir' : '');
  const pt = document.querySelector('.onglet[data-onglet="methode"] .pt'); if (pt) pt.hidden = !bloque;
}
function initBarre() {
  const t = $('#titre-doc');
  t.addEventListener('change', () => { U.act('doc.nom', { nom: t.value }); t.blur(); sauveAuto(); });
  t.addEventListener('keydown', e => { if (e.key === 'Enter') t.blur(); e.stopPropagation(); });
  $('#b-annule').addEventListener('click', () => U.act('annule'));
  $('#b-refait').addEventListener('click', () => U.act('refait'));
  $('#b-dezoom').addEventListener('click', () => U.zoomPas(-1));
  $('#b-zoom-plus').addEventListener('click', () => U.zoomPas(1));
  $('#b-zoom').addEventListener('click', () => { U.ajuste(); majBarre(); });
  $('#b-theme').addEventListener('click', () => U.basculeTheme());
  $('#etape-chip').addEventListener('click', () => U.ouvreOnglet && U.ouvreOnglet('methode'));
  $('#b-fichier').addEventListener('click', e => menuFichier(e.currentTarget));
  $('#b-panneau').addEventListener('click', () => U.basculePanneau && U.basculePanneau());
}

/* ---------- Enregistrement ---------- */
const sauveAuto = U.debounce(() => {
  try { U.stocke.ecris('auto', U.at.projet()); }
  catch (e) { /* quota : on garde le document sans le journal */ try { const p = U.at.projet(); p.journal = []; U.stocke.ecris('auto', p); } catch (e2) { /* rien */ } }
}, 800);
U.sauveAuto = sauveAuto;
U.enregistreProjet = function () {
  const p = U.at.projet();
  sauveAuto();
  return U.telecharge(U.nomFichier(U.at.doc.nom) + '.claude-pixel.json', JSON.stringify(p), 'application/json');
};
async function ouvreProjet() {
  const f = await U.choisitFichier('.json,application/json'); if (!f) return;
  try {
    const p = JSON.parse(await U.litTexte(f));
    if (!p || !AP.FORMATS.includes(p.format)) throw new Error('Ce fichier n\'est pas un projet Claude Pixel.');
    U.at.charge(p); U.ajuste(); U.redessine(); sauveAuto();
    U.toast('Projet ouvert : ' + U.at.doc.nom, 'ok');
  } catch (e) { U.toast('Ouverture impossible : ' + e.message, 'refus'); }
}

/* ---------- Exports ---------- */
const nomDoc = () => U.nomFichier(U.at.doc.nom);
function modaleExport() {
  const d = U.at.doc, anim = d.images.length > 1;
  const ech = h('select.champ', { 'data-cible': 'export-echelle' }, [1, 2, 3, 4, 6, 8, 10, 16].map(n => h('option', { value: n, selected: n === (Math.max(d.w, d.h) <= 32 ? 8 : 4) }, '×' + n + ' (' + d.w * n + '×' + d.h * n + ')')));
  const cols = h('input.champ.mono', { type: 'number', min: 1, max: d.images.length, value: d.images.length, 'data-cible': 'export-colonnes' });
  const marge = h('input.champ.mono', { type: 'number', min: 0, max: 16, value: 0, 'data-cible': 'export-marge' });
  const etq = h('select.champ', { 'data-cible': 'export-etiquette' }, h('option', { value: -1 }, 'Toutes les images'), d.etiquettes.map((t, i) => h('option', { value: i }, t.nom + ' (' + (t.de + 1) + '–' + (t.a + 1) + ')')));
  const e = () => Number(ech.value) || 1;
  const fait = async (quoi) => {
    try {
      if (quoi === 'png1') await U.telecharge(nomDoc() + '.png', AP.pngImage(d, U.at.s.image, 1), 'image/png');
      else if (quoi === 'pngN') await U.telecharge(nomDoc() + '-x' + e() + '.png', AP.pngImage(d, U.at.s.image, e()), 'image/png');
      else if (quoi === 'gif') {
        const i = Number(etq.value), t = d.etiquettes[i];
        const o = t ? { echelle: e(), de: t.de, a: t.a, pingpong: t.sens === 'pingpong' } : { echelle: e() };
        await U.telecharge(nomDoc() + (t ? '-' + U.nomFichier(t.nom) : '') + '.gif', AP.gifDoc(d, o), 'image/gif');
      } else if (quoi === 'planche') {
        const p = AP.planche(d, { echelle: e(), colonnes: Number(cols.value) || d.images.length, marge: Number(marge.value) || 0 });
        await U.telecharge(nomDoc() + '-planche.png', p.png, 'image/png');
        await U.telecharge(nomDoc() + '-planche.json', p.json, 'application/json');
      } else if (quoi === 'hex') await U.telecharge(nomDoc() + '.hex.txt', AP.paletteHex(d), 'text/plain');
      else if (quoi === 'gpl') await U.telecharge(nomDoc() + '.gpl.txt', AP.paletteGpl(d), 'text/plain');
    } catch (err) { U.toast('Export impossible : ' + err.message, 'refus'); }
  };
  const ligneExp = (txt, sous, quoi, prim) => h('div.ligne', { style: { justifyContent: 'space-between' } },
    h('div', h('b', txt), h('br'), h('small', { style: { color: 'var(--fg-3)' } }, sous)),
    h('button.btn' + (prim ? '.prim' : ''), { 'data-cible': 'export-' + quoi, on: { click: () => fait(quoi) } }, 'Exporter'));
  const corps = h('div.pile',
    h('p.aide-txt', 'L\'export n\'inclut ni les calques de construction ni les références. On dessine à la taille finale : l\'agrandissement est fait ici, par multiples entiers seulement.'),
    h('div.grille2', h('label', 'Agrandissement', ech), anim ? h('label', 'GIF : séquence', etq) : null),
    ligneExp('PNG ×1', d.w + '×' + d.h + ', taille réelle (image ' + (U.at.s.image + 1) + ')', 'png1', true),
    ligneExp('PNG agrandi', 'au plus proche voisin, sans flou', 'pngN'),
    anim ? ligneExp('GIF animé', d.images.length + ' images, durées de la feuille de timing', 'gif') : null,
    anim ? h('div.grille2', h('label', 'Planche : colonnes', cols), h('label', 'Marge (px)', marge)) : null,
    ligneExp('Planche de sprites', 'PNG + JSON (format de type Aseprite, avec étiquettes)', 'planche'),
    ligneExp('Palette .hex', 'une couleur par ligne (Lospec)', 'hex'),
    ligneExp('Palette .gpl', 'GIMP / Aseprite / Krita', 'gpl'));
  U.modale('Exporter', corps, [{ txt: 'Fermer', valeur: null, cible: 'fermer' }], { large: false });
}

/* ---------- Import d'image ---------- */
function reduit(img, w, h) {
  const f = Math.min(w / img.w, h / img.h, 1);
  if (f >= 1) return img;
  const nw = Math.max(1, Math.round(img.w * f)), nh = Math.max(1, Math.round(img.h * f)), out = new Uint8ClampedArray(nw * nh * 4);
  for (let y = 0; y < nh; y++) for (let x = 0; x < nw; x++) {
    const sx = Math.min(img.w - 1, Math.floor((x + 0.5) / f)), sy = Math.min(img.h - 1, Math.floor((y + 0.5) / f));
    out.set(img.data.subarray((sy * img.w + sx) * 4, (sy * img.w + sx) * 4 + 4), (y * nw + x) * 4);
  }
  return { w: nw, h: nh, data: out };
}
async function importeImage() {
  const f = await U.choisitFichier('image/png,image/gif,image/jpeg,image/webp'); if (!f) return;
  let img; try { img = await U.litImage(f); } catch (e) { U.toast(e.message, 'refus'); return; }
  const d = U.at.doc, claude = U.at.mode === 'claude';
  let type = 'reference';
  const ch = h('div.choix-type', [['reference', 'Calque de référence', 'Modèle à 50 %, jamais exporté'], ['normal', 'Calque normal', claude ? 'refusé en mode Claude' : 'pixels utilisables']].map(([v, t, s]) =>
    h('button', { 'aria-pressed': String(v === type), disabled: claude && v === 'normal', 'data-cible': 'import-' + v, on: { click: e => { type = v; for (const b of ch.children) b.setAttribute('aria-pressed', String(b === e.currentTarget)); } } }, t, h('small', s))));
  const grand = img.w > d.w || img.h > d.h;
  const r = await U.modale('Importer une image', h('div.pile',
    h('p.aide-txt', f.name + ' : ' + img.w + '×' + img.h + ' px.' + (grand ? ' Elle sera réduite pour tenir dans la toile (' + d.w + '×' + d.h + ').' : '')),
    ch,
    h('p.aide-txt', 'Une référence sert à étudier et à copier à la main (G2). Elle ne remplace jamais le dessin pixel par pixel.')),
  [{ txt: 'Annuler', valeur: false, cible: 'non' }, { txt: 'Importer', valeur: true, prim: true, cible: 'oui' }]);
  if (!r) return;
  const im = reduit(img, d.w, d.h);
  U.act('importe', { type, w: im.w, h: im.h, data: U.b64(new Uint8Array(im.data.buffer, im.data.byteOffset, im.data.byteLength)), nom: f.name.replace(/\.[^.]+$/, '') });
}
async function importePalette() {
  const f = await U.choisitFichier('.hex,.gpl,.txt,text/plain'); if (!f) return;
  try {
    const l = AP.lisPalette(await U.litTexte(f));
    if (!l.length) throw new Error('aucune couleur lue');
    U.act('palette.remplace', { liste: l }); U.toast(l.length + ' couleurs chargées.', 'ok');
  } catch (e) { U.toast('Palette illisible : ' + e.message, 'refus'); }
}

/* ---------- Nouveau dessin ---------- */
const TAILLES = [8, 12, 16, 24, 32, 48, 64, 96, 128];
function modaleNouveau(bloque) {
  let type = U.at.doc.type in AP.TYPES ? U.at.doc.type : 'objet', w = 16, hh = 16;
  const types = h('div.choix-type', Object.keys(AP.TYPES).map(k => h('button', {
    'aria-pressed': String(k === type), 'data-cible': 'nouveau-type-' + k,
    on: { click: e => { type = k; for (const b of types.children) b.setAttribute('aria-pressed', String(b === e.currentTarget)); maj(); } }
  }, AP.TYPES[k].nom, h('small', AP.TYPES[k].ref + ' · ' + AP.ETAPES[k].length + ' étapes'))));
  const iw = h('input.champ.mono', { type: 'number', min: 1, max: 512, value: w, 'data-cible': 'nouveau-w', on: { input: () => { w = +iw.value | 0; maj(); } } });
  const ih = h('input.champ.mono', { type: 'number', min: 1, max: 512, value: hh, 'data-cible': 'nouveau-h', on: { input: () => { hh = +ih.value | 0; maj(); } } });
  const presets = h('div.mods', TAILLES.map(n => h('button.btn', { 'data-cible': 'nouveau-taille-' + n, on: { click: () => { iw.value = ih.value = w = hh = n; maj(); } } }, String(n))));
  const pal = h('select.champ', { 'data-cible': 'nouveau-palette' }, Object.keys(AP.PALETTES).map(n => h('option', { value: n }, n + ' (' + AP.PALETTES[n].length + ')')));
  const nom = h('input.champ', { value: 'sans titre', 'data-cible': 'nouveau-nom', spellcheck: false });
  const info = h('p.aide-txt');
  function maj() {
    for (const b of presets.children) b.setAttribute('aria-pressed', String(+b.textContent === w && w === hh));
    const b = AP.budgetPourTaille(w || 1, hh || 1);
    info.textContent = 'Table A3 pour ' + (w || '?') + '×' + (hh || '?') + ' : ' + b.tons + ' tons par matière, ' + (isFinite(b.total) ? '≤ ' + b.total + ' couleurs' : 'couleurs libres') +
      ', AA ' + b.aa + ', ' + (isFinite(b.idees) ? b.idees + ' idée(s) de détail' : 'détail libre') + '. On dessine à la taille finale (A4b).' +
      (type === 'decor' ? ' Décor : 16×16 ou 32×32, une tuile par toile.' : '');
  }
  maj();
  const corps = h('div.pile',
    h('label', 'Ce que tu dessines', types),
    h('div.grille2', h('label', 'Largeur', iw), h('label', 'Hauteur', ih)),
    presets, info,
    h('div.grille2', h('label', 'Palette de départ', pal), h('label', 'Nom', nom)));
  const boutons = [];
  if (!bloque) boutons.push({ txt: 'Annuler', valeur: false, cible: 'non' });
  boutons.push({ txt: 'Créer', valeur: true, prim: true, cible: 'oui', action: () => { if (!(w >= 1 && w <= 512 && hh >= 1 && hh <= 512)) { U.toast('Taille entre 1 et 512 px.', 'refus'); return false; } } });
  return U.modale('Nouveau dessin', corps, boutons, { large: true, bloque }).then(ok => {
    if (!ok) return false;
    const r = U.act('doc.nouveau', { w, h: hh, palette: pal.value, type, nom: nom.value.trim() || 'sans titre' });
    if (r && r.refus) return false;
    if (type === 'decor') U.act('tuile.reglage', { on: true, tw: w, th: hh });
    U.ajuste(); U.redessine(); sauveAuto();
    U.ouvreOnglet && U.ouvreOnglet('methode');
    return true;
  });
}
U.modaleNouveau = modaleNouveau;

/* ---------- Redimensionner / mettre à l'échelle ---------- */
function modaleTaille() {
  const d = U.at.doc;
  const iw = h('input.champ.mono', { type: 'number', min: 1, max: 512, value: d.w, 'data-cible': 'redim-w' });
  const ih = h('input.champ.mono', { type: 'number', min: 1, max: 512, value: d.h, 'data-cible': 'redim-h' });
  let ax = 'c', ay = 'c';
  const ancre = h('div', { style: { display: 'grid', gridTemplateColumns: 'repeat(3,36px)', gap: '3px' } });
  for (const y of ['h', 'c', 'b']) for (const x of ['g', 'c', 'd']) ancre.appendChild(h('button.btn', { 'aria-pressed': String(x === ax && y === ay), 'data-cible': 'redim-ancre-' + x + y, style: { minWidth: '36px', minHeight: '32px' }, on: { click: e => { ax = x; ay = y; for (const b of ancre.children) b.setAttribute('aria-pressed', String(b === e.currentTarget)); } } }, '·'));
  U.modale('Taille de la toile', h('div.pile',
    h('p.aide-txt', 'Agrandit ou rogne la toile sans toucher aux pixels. Pour changer l\'échelle du dessin, utilise × 2 ou ÷ 2 (déconseillé : on redessine à la taille finale).'),
    h('div.grille2', h('label', 'Largeur', iw), h('label', 'Hauteur', ih), h('label', 'Ancrage', ancre))),
  [{ txt: '÷ 2', valeur: 'moitie', cible: 'echelle-moitie' }, { txt: '× 2', valeur: 'double', cible: 'echelle-double' }, { txt: 'Annuler', valeur: false, cible: 'non' }, { txt: 'Appliquer', valeur: 'ok', prim: true, cible: 'oui' }]).then(v => {
    if (v === 'ok') U.act('doc.redim', { w: +iw.value, h: +ih.value, ax, ay });
    else if (v === 'double') U.act('doc.echelle', { f: 2 });
    else if (v === 'moitie') U.act('doc.echelle', { f: 0.5 });
    if (v) { U.ajuste(); U.redessine(); }
  });
}

/* ---------- Menu Fichier ---------- */
function menuFichier(ancre) {
  const anim = U.at.doc.images.length > 1, claude = U.at.mode === 'claude';
  const tr = (op, txt, kbd) => ({ txt, kbd, cible: 'transforme-' + op, action: () => U.act('transforme', { op }) });
  U.menu(ancre, [
    { sous: 'Projet' },
    { txt: 'Nouveau dessin…', cible: 'fichier-nouveau', action: () => modaleNouveau(false) },
    { txt: 'Ouvrir un projet (.claude-pixel.json)…', cible: 'fichier-ouvrir', action: ouvreProjet },
    { txt: 'Enregistrer le projet', kbd: 'Ctrl+S', cible: 'fichier-enregistrer', action: U.enregistreProjet },
    { txt: 'Exporter (PNG, GIF, planche, palette)…', cible: 'fichier-exporter', action: modaleExport },
    '-',
    { sous: 'Importer' },
    { txt: claude ? 'Image de référence…' : 'Image (référence ou calque)…', cible: 'fichier-importe-image', action: importeImage },
    { txt: 'Palette (.hex, .gpl)…', cible: 'fichier-importe-palette', action: importePalette },
    '-',
    { sous: 'Image' },
    { txt: 'Taille de la toile…', cible: 'fichier-taille', action: modaleTaille },
    tr('miroirH', 'Miroir horizontal'), tr('miroirV', 'Miroir vertical'),
    tr('rot90', 'Rotation 90° horaire'), tr('rot270', 'Rotation 90° antihoraire'), tr('rot180', 'Rotation 180°'),
    { txt: 'Rotation RotSprite…', cible: 'transforme-rotsprite', action: modaleRotsprite },
    anim ? { txt: 'Miroir sur toutes les images', cible: 'transforme-miroir-images', action: () => U.act('transforme', { op: 'miroirH', cible: 'images' }) } : { cache: true },
    { txt: 'Contour automatique (C1)', cible: 'contour-auto', action: () => U.act('contour.auto', { couleur: AP.hex(U.at.s.c1), diagonales: false }) },
    '-',
    { txt: 'Effacer l\'enregistrement local', cible: 'fichier-efface-local', action: async () => { if (await U.confirme('Effacer la sauvegarde locale ?', 'Le dessin ouvert reste à l\'écran. Seule la copie gardée dans ce navigateur est supprimée.', 'Effacer')) { U.stocke.retire('auto'); U.toast('Sauvegarde locale effacée.', 'ok'); } } }
  ]);
}
function modaleRotsprite() {
  const a = h('input.champ.mono', { type: 'number', min: -180, max: 180, step: 1, value: 15, 'data-cible': 'rotsprite-angle' });
  U.modale('Rotation RotSprite', h('div.pile', h('p.aide-txt', 'Tourne d\'un angle libre en gardant des pixels nets (agrandissement ×8, rotation, réduction). Repasse ensuite les contours à la main.'), h('label', 'Angle (degrés)', a)),
    [{ txt: 'Annuler', valeur: false, cible: 'non' }, { txt: 'Tourner', valeur: true, prim: true, cible: 'oui' }]).then(ok => { if (ok) U.act('transforme', { op: 'rotsprite', angle: +a.value || 0 }); });
}

/* ---------- Mise à jour groupée ---------- */
let rafOutils = 0, besoinOptions = true;
function maj(quoi) {
  if (quoi === 'etat' || quoi === 'doc' || quoi === 'act') besoinOptions = true;
  if (rafOutils) return;
  rafOutils = requestAnimationFrame(() => {
    rafOutils = 0;
    majRail(); majBarre();
    if (besoinOptions && !document.querySelector('#options .champ:focus')) { majOptions(); besoinOptions = false; }
  });
}
function initOutils() {
  initRail(); initBarre();
  U.at.ecoute((q) => { if (q !== 'pixels' && q !== 'trait') maj(q); else if (q === 'pixels') sauveAuto(); if (q === 'doc' || q === 'act') sauveAuto(); });
  maj('etat');
}
Object.assign(U, { initOutils, majOutils: maj, NOMS_OUTILS, modaleExport, ouvreProjet, importeImage });
})(window);
