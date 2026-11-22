#!/usr/bin/env node
/*
 * Souris de Claude Pixel : serveur local.
 *
 * Il ouvre l'atelier dans Chromium (Playwright), garde la page ouverte entre deux
 * commandes et filme toute la séance. Il ne transmet à la page que des événements
 * de souris et de clavier, plus des lectures par window.claudePixel (objet gelé,
 * en lecture seule). Aucune commande ne permet d'exécuter un script dans la page.
 *
 *   node serveur.mjs [--port 4917] [--id nom-de-seance] [--tel] [--humain]
 *
 * Les commandes arrivent par POST / (une ligne par commande) ; voir README.md.
 */
import http from 'node:http';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const { chromium } = require('playwright');

/* ---------- Arguments ---------- */
const argv = process.argv.slice(2);
const opt = (nom, def) => { const i = argv.indexOf('--' + nom); return i < 0 ? def : (argv[i + 1] && !argv[i + 1].startsWith('--') ? argv[i + 1] : true); };
const PORT = Number(opt('port', process.env.SOURIS_PORT || 4917));
const TEL = !!opt('tel', false);
const HUMAIN = !!opt('humain', false);
const ID = String(opt('id', new Date().toISOString().slice(0, 16).replace(/[:T]/g, '-')));

const ICI = path.dirname(fileURLToPath(import.meta.url));
const RACINE = path.resolve(ICI, '..');
const APP = path.join(RACINE, 'app', 'index.html');
const DOS = path.join(RACINE, 'seances', ID);
const REGARDS = path.join(DOS, 'regards');
const FICHIERS = path.join(DOS, 'fichiers');
const TMP = fs.mkdtempSync(path.join(os.tmpdir(), 'claude-pixel-souris-'));
for (const d of [DOS, REGARDS, FICHIERS]) fs.mkdirSync(d, { recursive: true });

const VUE = TEL ? { width: 390, height: 844 } : { width: 1280, height: 800 };

/* ---------- Page : l'artifact tel qu'il sera publié (squelette ajouté à la publication) ---------- */
const brut = fs.readFileSync(APP, 'utf8');
const PAGE = path.join(TMP, 'page.html');
fs.writeFileSync(PAGE, '<!doctype html><html><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1,viewport-fit=cover"></head><body>' + brut + '</body></html>');

/* ---------- Curseur et bandeau filmés ----------
 * Les vidéos de Playwright ne montrent pas le curseur : on dessine une flèche qui suit
 * la souris, un cercle à chaque clic et un bandeau avec la commande en cours.
 * Ces éléments ne reçoivent aucun événement (pointer-events: none) et ne touchent pas
 * à l'atelier. */
const HUD = () => {
  const mk = () => {
    if (document.getElementById('souris-hud')) return;
    const st = document.createElement('style');
    st.textContent = `#souris-hud{position:fixed;inset:0;pointer-events:none;z-index:2147483647}
#souris-fleche{position:absolute;left:0;top:0;width:22px;height:22px;transform:translate(-2px,-2px);filter:drop-shadow(0 1px 1px #0008)}
#souris-bandeau{position:absolute;left:10px;bottom:10px;max-width:70%;font:600 13px/1.3 "IBM Plex Mono",ui-monospace,monospace;color:#fff;background:#151320e6;border:1px solid #f2b84b;border-radius:6px;padding:5px 9px;white-space:pre-wrap}
#souris-bandeau:empty{display:none}
.souris-rond{position:absolute;width:26px;height:26px;margin:-13px 0 0 -13px;border:2px solid #f2b84b;border-radius:50%;animation:souris-r .5s ease-out forwards}
.souris-rond.droit{border-color:#cdb3ff}
@keyframes souris-r{from{transform:scale(.4);opacity:1}to{transform:scale(1.3);opacity:0}}`;
    document.documentElement.appendChild(st);
    const hud = document.createElement('div'); hud.id = 'souris-hud';
    hud.innerHTML = '<svg id="souris-fleche" viewBox="0 0 22 22"><path d="M2 2 L2 18 L6.5 13.5 L9.5 20 L12.5 18.6 L9.6 12.4 L16 12.4 Z" fill="#fff" stroke="#151320" stroke-width="1.4" stroke-linejoin="round"/></svg><div id="souris-bandeau"></div>';
    document.documentElement.appendChild(hud);
    const f = hud.firstChild;
    addEventListener('mousemove', e => { f.style.left = e.clientX + 'px'; f.style.top = e.clientY + 'px'; }, { capture: true, passive: true });
    addEventListener('mousedown', e => {
      const r = document.createElement('div'); r.className = 'souris-rond' + (e.button === 2 ? ' droit' : '');
      r.style.left = e.clientX + 'px'; r.style.top = e.clientY + 'px'; hud.appendChild(r); setTimeout(() => r.remove(), 600);
    }, { capture: true, passive: true });
    Object.defineProperty(window, '__sourisBandeau', { value: t => { const b = document.getElementById('souris-bandeau'); if (b) b.textContent = t; } });
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mk); else mk();
};

/* ---------- Navigateurs ---------- */
const navigateur = await chromium.launch();
const ctx = await navigateur.newContext({ viewport: VUE, deviceScaleFactor: 1, acceptDownloads: true, recordVideo: { dir: TMP, size: VUE } });
await ctx.addInitScript(HUD);
const page = await ctx.newPage();
const erreurs = [];
page.on('pageerror', e => erreurs.push(e.message));
page.on('download', async d => {
  const nom = d.suggestedFilename().replace(/[^\w.\-]+/g, '_');
  try { await d.saveAs(path.join(FICHIERS, nom)); journal('# fichier enregistré : fichiers/' + nom); } catch (e) { erreurs.push('téléchargement : ' + e.message); }
});
await page.goto('file://' + PAGE + (HUMAIN ? '' : '#claude'), { waitUntil: 'domcontentloaded' });
await page.waitForFunction(() => window.claudePixel && document.getElementById('toile'), null, { timeout: 15000 });
await page.evaluate(() => Promise.race([document.fonts.ready, new Promise(r => setTimeout(r, 5000))]));

/* Un second contexte, jamais filmé, sert à dessiner la loupe et les aperçus. */
const atelierYeux = await (await navigateur.newContext({ viewport: { width: 800, height: 800 } })).newPage();
await atelierYeux.setContent('<canvas id="c"></canvas>');

/* ---------- État de la souris ---------- */
let pos = { x: Math.round(VUE.width / 2), y: Math.round(VUE.height / 2) };
const tenus = new Set();      // boutons tenus
const mods = new Set();       // touches de modification tenues
let traitSurToile = false;    // le bouton tenu a été pressé sur la toile
let verrou = false;           // un trait vient d'être relâché sur la toile : regarder d'abord
let nRegard = 0;
await page.mouse.move(pos.x, pos.y);

const lit = (fn, ...a) => page.evaluate(([f, a]) => window.claudePixel[f](...a), [fn, a]);
const pause = ms => new Promise(r => setTimeout(r, ms));
const LOG = path.join(DOS, 'commandes.txt');
function journal(l) { fs.appendFileSync(LOG, new Date().toISOString().slice(11, 23) + '  ' + l + '\n'); }
journal('# séance ' + ID + ' · ' + (HUMAIN ? 'humain' : 'claude') + ' · ' + VUE.width + '×' + VUE.height);

/* La toile est-elle sous ce point, sans modale ni menu par-dessus ? (lecture seule) */
const surToile = (x, y) => page.evaluate(([x, y]) => {
  const el = document.elementFromPoint(x, y);
  return !!el && el.id === 'toile';
}, [x, y]);

async function caseVersEcran(cx, cy) { return lit('ecranDeCellule', cx, cy); }
// Les cases d'un segment, de a à b inclus (Bresenham).
function ligneDeCases([x0, y0], [x1, y1]) {
  const r = [], dx = Math.abs(x1 - x0), dy = -Math.abs(y1 - y0), sx = x0 < x1 ? 1 : -1, sy = y0 < y1 ? 1 : -1;
  let e = dx + dy;
  for (;;) { r.push([x0, y0]); if (x0 === x1 && y0 === y1) return r; const e2 = 2 * e; if (e2 >= dy) { e += dy; x0 += sx; } if (e2 <= dx) { e += dx; y0 += sy; } }
}

/* Un geste de main, pas une téléportation.
 * Durée selon la loi de Fitts (loin = un peu plus long, jamais lent), profil à jerk minimal
 * (départ et arrivée en douceur, vitesse au milieu), légère courbe comme un poignet qui
 * pivote, une position toutes les ~16 ms, et l'arrivée exactement sur la cible.
 * Sans courbe quand un bouton est tenu : un glisser va droit. */
const lisse = t => t * t * t * (10 - 15 * t + 6 * t * t);
async function bouge(x, y, lent = 1, { courbe = true } = {}) {
  const x0 = pos.x, y0 = pos.y, dx = x - x0, dy = y - y0, d = Math.hypot(dx, dy);
  if (d < 0.5) { await page.mouse.move(x, y); pos = { x, y }; return; }
  const duree = (30 + 55 * Math.log2(d / 16 + 1)) / lent;
  const n = Math.max(2, Math.round(duree / 16));
  // Courbe : décalage perpendiculaire en cloche, côté fixe selon le sens (main droite).
  const flec = courbe && !tenus.size ? Math.min(d * 0.05, 14) * (dx >= 0 ? -1 : 1) : 0, px = -dy / d, py = dx / d;
  const t0 = Date.now();
  for (let k = 1; k <= n; k++) {
    const t = k / n, s = lisse(t), b = Math.sin(Math.PI * s) * flec;
    const ex = k === n ? x : x0 + dx * s + px * b, ey = k === n ? y : y0 + dy * s + py * b;
    await page.mouse.move(ex, ey);
    const reste = t0 + duree * t - Date.now(); if (reste > 1) await pause(reste);
  }
  pos = { x, y };
}

/* ---------- Analyse des arguments de position ---------- */
// "12 8" : case ; "@640 300" : point de l'écran ; "=nom" : centre d'un élément data-cible.
async function point(args) {
  if (!args.length) throw new Error('Il manque la position.');
  const a = args[0];
  if (a.startsWith('=') || a.startsWith('#')) {
    const r = await lit('cible', a.slice(1));
    if (!r) throw new Error('Aucun élément visible « ' + a.slice(1) + ' ». Essaie : souris cibles ' + a.slice(1, 5));
    if (r.cx < 0 || r.cy < 0 || r.cx > VUE.width || r.cy > VUE.height) throw new Error('« ' + a.slice(1) + ' » est hors de l\'écran (' + Math.round(r.cx) + ',' + Math.round(r.cy) + ') : fais défiler son panneau avec la molette, puis recommence.');
    return { x: Math.round(r.cx), y: Math.round(r.cy), quoi: 'élément ' + a.slice(1) };
  }
  if (a.startsWith('@')) {
    const x = Number(a.slice(1)), y = Number(args[1]);
    if (!Number.isFinite(x) || !Number.isFinite(y)) throw new Error('Écris « @x y » en pixels d\'écran.');
    return { x, y, quoi: 'écran ' + x + ',' + y };
  }
  const [cx, cy] = a.includes(',') ? a.split(',').map(Number) : [Number(a), Number(args[1])];
  if (!Number.isInteger(cx) || !Number.isInteger(cy)) throw new Error('Écris une case « x y » (entiers), « @x y » pour l\'écran, « =nom » pour un élément.');
  const e = await caseVersEcran(cx, cy);
  return { x: Math.round(e.x * 10) / 10, y: Math.round(e.y * 10) / 10, quoi: 'case ' + cx + ',' + cy };
}
const caseDe = s => { const [x, y] = s.split(',').map(Number); if (!Number.isInteger(x) || !Number.isInteger(y)) throw new Error('Case attendue « x,y », reçu « ' + s + ' ».'); return [x, y]; };

function refuseSiVerrou(sur) {
  if (verrou && sur) throw new Error('Refusé : un trait vient d\'être relâché sur la toile. Fais « souris regarde » avant de dessiner à nouveau (SPEC 3.4).');
}

const BOUTONS = { gauche: 'left', droit: 'right', milieu: 'middle' };
const TOUCHES = { ctrl: 'Control', control: 'Control', maj: 'Shift', shift: 'Shift', alt: 'Alt', cmd: 'Meta', meta: 'Meta',
  echap: 'Escape', esc: 'Escape', entree: 'Enter', entrée: 'Enter', espace: 'Space', suppr: 'Delete', retour: 'Backspace', tab: 'Tab',
  haut: 'ArrowUp', bas: 'ArrowDown', gauche: 'ArrowLeft', droite: 'ArrowRight', debut: 'Home', fin: 'End', pgup: 'PageUp', pgdn: 'PageDown' };
const touche = t => t.split('+').map(k => TOUCHES[k.toLowerCase()] || (k.length === 1 ? k : k[0].toUpperCase() + k.slice(1))).join('+');

async function relacheTout() {
  for (const b of tenus) await page.mouse.up({ button: b });
  tenus.clear();
  for (const m of mods) await page.keyboard.up(m);
  mods.clear();
}

/* ---------- Les yeux ---------- */
const DESSINE = ([mode, d, opts]) => {
  const c = document.getElementById('c'), g = c.getContext('2d');
  const damier = (x, y, s) => { const n = s / 2; for (let j = 0; j < s; j += n) for (let i = 0; i < s; i += n) { g.fillStyle = ((i + j) / n) % 2 ? '#d8d8de' : '#f4f4f6'; g.fillRect(x + i, y + j, n, n); } };
  if (mode === 'loupe') {
    const R = 7, T = 26, M = 26, N = 2 * R + 1, { cx, cy } = opts;
    c.width = M + N * T + 2; c.height = M + N * T + 2;
    g.fillStyle = '#151320'; g.fillRect(0, 0, c.width, c.height);
    g.font = '10px monospace'; g.textAlign = 'center'; g.textBaseline = 'middle';
    for (let j = 0; j < N; j++) for (let i = 0; i < N; i++) {
      const x = cx - R + i, y = cy - R + j, px = M + i * T, py = M + j * T;
      if (x < 0 || y < 0 || x >= d.w || y >= d.h) { g.fillStyle = '#2a2638'; g.fillRect(px, py, T, T); g.strokeStyle = '#3a3550'; g.beginPath(); g.moveTo(px, py + T); g.lineTo(px + T, py); g.stroke(); continue; }
      damier(px, py, T);
      const v = d.lignes[y][x]; if (v) { g.fillStyle = v; g.fillRect(px, py, T, T); }
    }
    g.strokeStyle = '#00000055'; g.lineWidth = 1;
    for (let k = 0; k <= N; k++) { g.beginPath(); g.moveTo(M + k * T + .5, M); g.lineTo(M + k * T + .5, M + N * T); g.stroke(); g.beginPath(); g.moveTo(M, M + k * T + .5); g.lineTo(M + N * T, M + k * T + .5); g.stroke(); }
    for (let k = 0; k < N; k++) {
      const x = cx - R + k, y = cy - R + k;
      g.fillStyle = k === R ? '#f2b84b' : '#b9b4cc';
      g.fillText(String(x), M + k * T + T / 2, M / 2); g.fillText(String(y), M / 2, M + k * T + T / 2);
    }
    const ox = M + R * T, oy = M + R * T;
    g.strokeStyle = '#f2b84b'; g.lineWidth = 2; g.strokeRect(ox + 1, oy + 1, T - 2, T - 2);
    g.beginPath(); g.moveTo(ox + T / 2, oy - 6); g.lineTo(ox + T / 2, oy + 6); g.moveTo(ox + T / 2, oy + T - 6); g.lineTo(ox + T / 2, oy + T + 6);
    g.moveTo(ox - 6, oy + T / 2); g.lineTo(ox + 6, oy + T / 2); g.moveTo(ox + T - 6, oy + T / 2); g.lineTo(ox + T + 6, oy + T / 2); g.stroke();
    if (opts.defauts) { g.strokeStyle = '#ff5a6e'; g.lineWidth = 2; for (const [x, y] of opts.defauts) { const i = x - cx + R, j = y - cy + R; if (i >= 0 && j >= 0 && i < N && j < N) g.strokeRect(M + i * T + 4, M + j * T + 4, T - 8, T - 8); } }
  } else {
    // ×1, ×2, agrandi ; puis, agrandis aussi, les valeurs (gris) et le guide de volume (0-C)
    const gr = Math.max(4, Math.min(16, Math.floor(256 / Math.max(d.w, d.h))));
    const P = [[d.lignes, 1, '×1'], [d.lignes, 2, '×2'], [d.lignes, gr, '×' + gr]].concat((opts.extra || []).map(([L, t]) => [L, gr, t]));
    const G = 16, W = P.reduce((s, p) => s + d.w * p[1] + G, G), H = d.h * gr + 2 * G + 14;
    c.width = W; c.height = H; g.fillStyle = opts.fond; g.fillRect(0, 0, W, H);
    g.font = '11px monospace'; g.fillStyle = '#888'; let x0 = G;
    for (const [L, e, t] of P) {
      for (let y = 0; y < d.h; y++) for (let x = 0; x < d.w; x++) { const v = L[y][x]; if (v) { g.fillStyle = v; g.fillRect(x0 + x * e, G + y * e, e, e); } }
      g.fillStyle = '#ddd'; g.fillText(t, x0, H - 8); x0 += d.w * e + G;
    }
  }
  return c.toDataURL('image/png').split(',')[1];
};

const f2 = x => x === null || x === undefined ? '—' : x.toFixed(2);
async function regarde() {
  nRegard++;
  const n = String(nRegard).padStart(3, '0'), base = path.join(REGARDS, n);
  await pause(120);
  await page.screenshot({ path: base + '-ecran.png' });
  const [et, vis, exp, msgs, defs, ver, vol, car] = await Promise.all([lit('etat'), lit('pixels', { vue: 'visible' }), lit('pixels', { vue: 'export' }), lit('messages', 6), lit('defauts'), lit('verifie'), lit('volume'), lit('carnet')]);
  const cel = await lit('celluleDeEcran', pos.x, pos.y);
  const cx = Math.max(0, Math.min(vis.w - 1, cel.x)), cy = Math.max(0, Math.min(vis.h - 1, cel.y));
  const pres = defs.map(r => ({ ...r, pres: r.pixels.filter(([x, y]) => Math.max(Math.abs(x - cel.x), Math.abs(y - cel.y)) <= 4) }));
  const loupe = await atelierYeux.evaluate(DESSINE, ['loupe', vis, { cx, cy, defauts: pres.flatMap(r => r.pres) }]);
  fs.writeFileSync(base + '-loupe.png', Buffer.from(loupe, 'base64'));
  const dessin = await atelierYeux.evaluate(DESSINE, ['dessin', exp, { fond: '#8a8794', extra: [[vol.valeurs, 'valeurs'], [vol.guide, 'guide ' + vol.lumiere.nom]] }]);
  fs.writeFileSync(base + '-dessin.png', Buffer.from(dessin, 'base64'));
  const couleur = cel.dedans ? (vis.lignes[cel.y][cel.x] || 'transparent') + ' (exportée : ' + (exp.lignes[cel.y][cel.x] || 'transparent') + ')' : '(hors toile)';
  const L = [
    'regard ' + n + (tenus.size ? '  (bouton tenu : aperçu avant de relâcher)' : ''),
    'case ' + cel.x + ',' + cel.y + (cel.dedans ? '' : ' (hors du dessin)') + ' · couleur ' + couleur + ' · écran ' + Math.round(pos.x) + ',' + Math.round(pos.y),
    'outil ' + et.outil + ' · taille ' + et.taille + ' · c1 ' + et.c1 + ' · c2 ' + et.c2,
    'calque ' + (et.calque + 1) + '/' + et.nbCalques + ' · image ' + (et.image + 1) + '/' + et.nbImages + ' · dessin ' + et.docW + '×' + et.docH + ' « ' + et.nom + ' » (' + et.type + ')',
    (et.etape ? (et.etape.finie ? 'méthode terminée · dernière étape : ' : 'étape ') + (et.etape.i + 1) + ' · ' + et.etape.titre + ' (' + et.etape.ref + ')' : 'étape ?') + (et.panneau ? ' · onglet ' + et.panneau : '') + (et.modale ? ' · fenêtre ouverte' : '') + (et.menu ? ' · menu ouvert' : ''),
    'porte : ' + (ver.ok ? 'prête' : ver.manque.join(' | ')),
    'défauts : ' + (defs.length ? defs.map(r => r.titre + ' [' + r.niveau + '] ' + r.pixels.length + ' px' + (pres.find(p => p.id === r.id).pres.length ? ' (dont ' + pres.find(p => p.id === r.id).pres.map(p => p.join(',')).join(' ') + ' près du curseur)' : '')).join(' ; ') : 'aucun'),
    'volume : lumière ' + vol.lumiere.nom + ' (az ' + vol.lumiere.az + '°, él ' + vol.lumiere.el + '°, ' + vol.lumiere.forme + ')' + (vol.lumiere.posee ? '' : ' NON POSÉE') +
      ' · accord ' + f2(vol.mesure.accord) + ' · familles ' + f2(vol.mesure.ecart) + ' · inversions ' + (vol.mesure.inverses === null ? '—' : Math.round(vol.mesure.inverses * 100) + ' %') + ' · étendue ' + f2(vol.mesure.etendue),
    'carnet : ' + (car.length ? car.filter(e => !e.barre).length + ' idée(s), ' + car.filter(e => e.barre).length + ' barrée(s) · dernière : [' + car[car.length - 1].rubrique + '] ' + car[car.length - 1].texte.slice(0, 90) + (car[car.length - 1].barre ? ' (barrée : ' + car[car.length - 1].raison.slice(0, 60) + ')' : '') : 'vide'),
    'messages : ' + (msgs.length ? msgs.map(m => '[' + m.niveau + '] ' + m.msg).join(' / ') : 'aucun'),
    'images : ' + path.relative(process.cwd(), base) + '-{ecran,loupe,dessin}.png'
  ];
  if (erreurs.length) L.push('erreurs de page : ' + erreurs.splice(0).join(' / '));
  fs.writeFileSync(base + '.txt', L.join('\n') + '\n');
  verrou = false;
  return L.join('\n');
}

/* ---------- Commandes ---------- */
async function execute(ligne) {
  const mots = ligne.trim().match(/"[^"]*"|\S+/g) || [];
  const [cmd, ...args] = mots;
  if (!cmd) return '';
  switch (cmd) {
    case 'va': case 'survole': {
      const p = await point(args); await bouge(p.x, p.y);
      if (cmd === 'survole') await pause(900);
      return 'curseur sur ' + p.quoi + ' (' + Math.round(p.x) + ',' + Math.round(p.y) + ')';
    }
    case 'pas': {
      const dx = Number(args[0] || 0), dy = Number(args[1] || 0);
      const cel = await lit('celluleDeEcran', pos.x, pos.y), e = await caseVersEcran(cel.x + dx, cel.y + dy);
      await bouge(e.x, e.y, 0.8, { courbe: false }); return 'curseur sur la case ' + (cel.x + dx) + ',' + (cel.y + dy);
    }
    case 'appuie': {
      const b = BOUTONS[args[0] || 'gauche']; if (!b) throw new Error('Bouton : gauche, droit ou milieu.');
      const sur = await surToile(pos.x, pos.y); refuseSiVerrou(sur);
      await page.mouse.down({ button: b }); tenus.add(b); if (sur) traitSurToile = true;
      return 'bouton ' + (args[0] || 'gauche') + ' tenu' + (sur ? ' sur la toile' : '');
    }
    case 'relache': {
      if (!tenus.size) return 'aucun bouton tenu';
      for (const b of tenus) await page.mouse.up({ button: b }); tenus.clear();
      if (traitSurToile) { verrou = true; traitSurToile = false; return 'relâché : trait posé, regarde avant le suivant'; }
      return 'relâché';
    }
    case 'clic': case 'double': {
      let b = 'left';
      if (BOUTONS[args[0]]) { b = BOUTONS[args[0]]; args.shift(); }
      if (args.length) { const p = await point(args); await bouge(p.x, p.y); }
      const sur = await surToile(pos.x, pos.y); refuseSiVerrou(sur);
      await page.mouse.click(pos.x, pos.y, { button: b, clickCount: cmd === 'double' ? 2 : 1, delay: 40 });
      if (sur) verrou = true;
      await pause(90);
      return cmd + (sur ? ' sur la toile : regarde avant le suivant' : '');
    }
    case 'trace': {
      if (args.length < 2) throw new Error('trace demande au moins deux cases : trace 3,4 5,4 6,5');
      const cases = args.map(caseDe), pts = [];
      for (const [x, y] of cases) pts.push(await caseVersEcran(x, y));
      await bouge(pts[0].x, pts[0].y);
      const sur = await surToile(pos.x, pos.y); refuseSiVerrou(sur);
      await page.mouse.down(); await pause(30);
      // Case par case, de centre en centre : une diagonale ne frôle jamais le coin d'une case voisine.
      // Rythme d'une main sûre : vite sur une marche droite, un temps à chaque changement de
      // direction, ralenti sur les dernières cases pour poser la fin juste.
      const chemin = [];
      for (let i = 1; i < cases.length; i++) for (const c of ligneDeCases(cases[i - 1], cases[i]).slice(1)) chemin.push(c);
      let n = 1, avant = cases[0], dir = null;
      for (let j = 0; j < chemin.length; j++) {
        const [x, y] = chemin[j], d = (x - avant[0]) + ',' + (y - avant[1]);
        const e = await caseVersEcran(x, y);
        await page.mouse.move(e.x, e.y, { steps: 1 }); pos = { x: e.x, y: e.y }; n++;
        const fin = chemin.length - j <= 2, coin = dir !== null && d !== dir;
        await pause(fin ? 32 : coin ? 38 : 14);
        dir = d; avant = chemin[j];
      }
      await pause(45); await page.mouse.up();
      if (sur) verrou = true;
      return 'trait par ' + cases.length + ' points (' + n + ' cases)' + (sur ? ', regarde avant le suivant' : '');
    }
    case 'glisse': {
      if (args.length !== 2) throw new Error('glisse a b : deux cases « x,y » (ou « @x,y » à l\'écran).');
      const ec = async s => s.startsWith('@') ? (([x, y]) => ({ x, y }))(s.slice(1).split(',').map(Number)) : caseVersEcran(...caseDe(s));
      const a = await ec(args[0]), b = await ec(args[1]);
      await bouge(a.x, a.y);
      const sur = await surToile(pos.x, pos.y); refuseSiVerrou(sur);
      await page.mouse.down(); await pause(45); await bouge(b.x, b.y, 0.6, { courbe: false }); await pause(60); await page.mouse.up();
      if (sur) verrou = true;
      return 'glissé de ' + args[0] + ' à ' + args[1] + (sur ? ', regarde avant le suivant' : '');
    }
    case 'molette': {
      const n = Number(args[0]); if (!Number.isFinite(n)) throw new Error('molette n : nombre de crans (négatif = vers le haut).');
      await page.mouse.wheel(0, n * 100); await pause(100); return 'molette ' + n;
    }
    case 'defile': {
      // Tourne la molette au-dessus du panneau jusqu'à voir l'élément.
      const nom = (args[0] || '').replace(/^[=#]/, ''); if (!nom) throw new Error('defile =nom');
      for (let k = 0; k < 80; k++) {
        const r = await lit('cible', nom); if (!r) throw new Error('Aucun élément « ' + nom + ' ».');
        const haut = 120, bas = VUE.height - 80;
        if (r.cy >= haut && r.cy <= bas) return '« ' + nom + ' » est visible (' + Math.round(r.cx) + ',' + Math.round(r.cy) + ')';
        const x = Math.min(Math.max(r.cx, 10), VUE.width - 10);
        if (Math.abs(pos.x - x) > 4 || pos.y < haut || pos.y > bas) await bouge(x, VUE.height / 2);
        const d = r.cy < haut ? Math.max(-500, r.cy - VUE.height / 2) : Math.min(500, r.cy - VUE.height / 2);
        await page.mouse.wheel(0, d); await pause(90);
      }
      throw new Error('« ' + nom + ' » reste hors de vue après 80 crans.');
    }
    case 'tiens': case 'lache': {
      const k = touche(args[0] || ''); if (!['Shift', 'Control', 'Alt', 'Meta'].includes(k)) throw new Error('Touche de modification : maj, ctrl, alt, cmd.');
      if (cmd === 'tiens') { await page.keyboard.down(k); mods.add(k); } else { await page.keyboard.up(k); mods.delete(k); }
      return k + (cmd === 'tiens' ? ' tenue' : ' lâchée');
    }
    case 'touche': {
      if (!args[0]) throw new Error('touche b, touche ctrl+z, touche echap…');
      const k = touche(args[0]);
      await page.keyboard.press(k); await pause(70);
      if (k === 'Escape' && tenus.size) { for (const b of tenus) await page.mouse.up({ button: b }); tenus.clear(); traitSurToile = false; }
      return 'touche ' + k;
    }
    case 'tape': {
      const t = args.join(' ').replace(/^"|"$/g, '');
      await page.keyboard.type(t, { delay: 14 }); return 'tapé ' + t.length + ' caractère(s)';
    }
    case 'choisis': {
      // Ouvre une liste déroulante d'un vrai clic, puis descend avec les flèches jusqu'à l'option.
      const nom = (args[0] || '').replace(/^[=#]/, ''), voulu = args.slice(1).join(' ').replace(/^"|"$/g, '').toLowerCase();
      if (!nom || !voulu) throw new Error('choisis =nom "option"');
      const info = await page.evaluate(n => { const e = document.querySelector('[data-cible="' + n + '"]'); const s = e && (e.tagName === 'SELECT' ? e : e.querySelector('select')); return s ? { i: s.selectedIndex, o: [...s.options].map(o => o.textContent.trim()) } : null; }, nom);
      if (!info) throw new Error('« ' + nom + ' » n\'est pas une liste déroulante.');
      let j = info.o.findIndex(t => t.toLowerCase() === voulu); if (j < 0) j = info.o.findIndex(t => t.toLowerCase().startsWith(voulu));
      if (j < 0) throw new Error('Options de « ' + nom + ' » : ' + info.o.join(' | '));
      const p = await point(['=' + nom]); await bouge(p.x, p.y);
      await page.mouse.click(pos.x, pos.y, { delay: 40 }); await pause(160);
      const d = j - Math.max(0, info.i);
      for (let k = 0; k < Math.abs(d); k++) { await page.keyboard.press(d > 0 ? 'ArrowDown' : 'ArrowUp'); await pause(60); }
      await page.keyboard.press('Enter'); await pause(100);
      return 'choisi « ' + info.o[j] + ' »';
    }
    case 'regarde': return regarde();
    case 'etat': {
      const [et, ver] = await Promise.all([lit('etat'), lit('verifie')]);
      const cel = await lit('celluleDeEcran', pos.x, pos.y);
      return JSON.stringify({ curseur: { ecran: pos, case: cel }, tenus: [...tenus], mods: [...mods], verrou, ...et, porte: ver }, null, 1);
    }
    case 'cibles': {
      const L = await lit('cibles'), f = args[0] || '';
      return L.filter(c => c.nom.includes(f)).map(c => c.nom + ' @' + Math.round(c.cx) + ',' + Math.round(c.cy)).join('\n') || 'aucune';
    }
    case 'attends': { const ms = Math.min(5000, Number(args[0]) || 500); await pause(ms); return 'attendu ' + ms + ' ms'; }
    case 'fin': return null;
    default: throw new Error('Commande inconnue « ' + cmd + ' ». Commandes : va, pas, choisis, defile, appuie, relache, clic, double, trace, glisse, molette, tiens, lache, touche, tape, survole, regarde, etat, cibles, attends, fin.');
  }
}

async function fin() {
  await relacheTout();
  await page.evaluate(() => window.__sourisBandeau && window.__sourisBandeau('fin de séance'));
  await pause(800);
  const video = page.video();
  await page.close(); await ctx.close();
  const dest = path.join(DOS, 'seance.webm');
  if (video) await video.saveAs(dest);
  await navigateur.close();
  fs.rmSync(TMP, { recursive: true, force: true });
  journal('# fin');
  return 'séance terminée · vidéo ' + path.relative(process.cwd(), dest);
}

/* ---------- Serveur HTTP (localhost seulement) ---------- */
let file = Promise.resolve();
const serveur = http.createServer((req, res) => {
  const repond = (code, o) => { res.writeHead(code, { 'content-type': 'application/json; charset=utf-8' }); res.end(JSON.stringify(o)); };
  if (req.method === 'GET' && req.url === '/sante') return repond(200, { ok: true, id: ID, dossier: DOS, vue: VUE });
  if (req.method !== 'POST') return repond(405, { ok: false, msg: 'POST / avec une commande par ligne' });
  let corps = '';
  req.on('data', c => { corps += c; if (corps.length > 1e5) req.destroy(); });
  req.on('end', () => {
    file = file.then(async () => {
      const sorties = [];
      for (const l of corps.split('\n').map(s => s.trim()).filter(s => s && !s.startsWith('//'))) {
        journal(l);
        try { await page.evaluate(t => window.__sourisBandeau && window.__sourisBandeau(t), 'souris ' + l); } catch (e) { /* page fermée */ }
        try {
          const r = await execute(l);
          if (r === null) { const m = await fin(); repond(200, { ok: true, msg: sorties.concat(m).join('\n'), fin: true }); setTimeout(() => process.exit(0), 100); return; }
          sorties.push(r);
        } catch (e) {
          journal('  ✗ ' + e.message.split('\n')[0]);
          return repond(200, { ok: false, msg: sorties.concat('✗ ' + l + ' : ' + e.message.split('\n')[0]).join('\n') });
        }
      }
      repond(200, { ok: true, msg: sorties.join('\n') });
    });
  });
});
serveur.listen(PORT, '127.0.0.1', () => console.log('souris prête · port ' + PORT + ' · séance ' + ID + ' · ' + DOS));
