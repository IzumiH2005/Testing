/* Claude Pixel — interface : socle (éléments, toasts, modales, menus, thème,
 * sauvegarde locale, téléchargements, mode Claude). */
(function (G) {
'use strict';
const AP = G.AP, U = AP.UI = AP.UI || {};
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];

/* h('div.classe#id', {attrs, on:{click}}, enfants...) */
function h(tag, props, ...kids) {
  const m = String(tag).match(/^([a-z0-9-]+)?((?:[.#][^.#]+)*)$/i) || [];
  const el = document.createElement(m[1] || 'div');
  (m[2] || '').replace(/([.#])([^.#]+)/g, (_, t, v) => { if (t === '.') el.classList.add(v); else el.id = v; });
  if (props && (typeof props !== 'object' || props instanceof Node || Array.isArray(props))) { kids.unshift(props); props = null; }
  if (props) for (const k in props) {
    const v = props[k];
    if (v === undefined || v === null || v === false) continue;
    if (k === 'on') for (const e in v) el.addEventListener(e, v[e]);
    else if (k === 'style' && typeof v === 'object') Object.assign(el.style, v);
    else if (k === 'text') el.textContent = v;
    else if (k === 'html') el.innerHTML = v;
    else if (k in el && typeof v !== 'string') el[k] = v;
    else el.setAttribute(k, v === true ? '' : v);
  }
  const add = c => {
    if (c === null || c === undefined || c === false) return;
    if (Array.isArray(c)) c.forEach(add);
    else el.appendChild(c instanceof Node ? c : document.createTextNode(String(c)));
  };
  kids.forEach(add);
  return el;
}

/* ---------- Toasts ---------- */
function toast(msg, niveau = 'info', ms) {
  const box = $('#toasts'); if (!box) return;
  const t = h('div.toast', { role: niveau === 'refus' ? 'alert' : 'status' }, msg);
  if (niveau === 'refus') t.classList.add('refus');
  else if (niveau === 'alerte') t.classList.add('alerte');
  else if (niveau === 'ok') t.classList.add('ok');
  box.appendChild(t);
  while (box.children.length > 4) box.firstChild.remove();
  setTimeout(() => t.remove(), ms || (niveau === 'refus' ? 6500 : niveau === 'alerte' ? 5000 : 2600));
}

/* ---------- Modales (sans alert/confirm/prompt) ---------- */
let modaleOuverte = null;
function modale(titre, corps, boutons = [], o = {}) {
  ferme();
  const pied = h('div.pied');
  const m = h('div.modale' + (o.large ? '.large' : ''), { role: 'dialog', 'aria-modal': 'true', 'aria-label': titre, 'data-cible': 'modale' },
    h('h2', titre), corps, pied);
  const voile = h('div.voile', { on: { pointerdown: e => { if (e.target === voile && !o.bloque) ferme(); } } }, m);
  const res = new Promise(ok => {
    voile._fin = ok;
    for (const b of boutons) {
      pied.appendChild(h('button.btn' + (b.prim ? '.prim' : '') + (b.danger ? '.danger' : ''), {
        'data-cible': 'modale-' + (b.cible || b.valeur || 'ok'),
        on: { click: async () => {
          if (b.action) { const r = await b.action(); if (r === false) return; }
          ferme(b.valeur);
        } }
      }, b.txt));
    }
  });
  document.body.appendChild(voile);
  modaleOuverte = voile;
  setTimeout(() => { const f = m.querySelector('input,select,textarea,button.prim') || m.querySelector('button'); if (f && !U.claude) f.focus(); }, 30);
  return res;
}
function ferme(v) {
  if (!modaleOuverte) return;
  const voile = modaleOuverte; modaleOuverte = null;
  voile.remove(); if (voile._fin) voile._fin(v);
}
function confirme(titre, texte, oui = 'Confirmer', danger = true) {
  return modale(titre, h('p.aide-txt', texte), [{ txt: 'Annuler', valeur: false, cible: 'non' }, { txt: oui, valeur: true, prim: !danger, danger, cible: 'oui' }]);
}

/* ---------- Menus déroulants ---------- */
let menuOuvert = null;
function menu(ancre, items) {
  fermeMenu();
  const m = h('div.menu', { role: 'menu', 'data-cible': 'menu' });
  for (const it of items) {
    if (it === '-') { m.appendChild(h('hr')); continue; }
    if (it.sous) { m.appendChild(h('div.sous', it.sous)); continue; }
    if (it.cache) continue;
    m.appendChild(h('button', { role: 'menuitem', 'data-cible': it.cible, disabled: !!it.inactif,
      on: { click: () => { fermeMenu(); it.action(); } } }, h('span', it.txt), it.kbd ? h('kbd', it.kbd) : null));
  }
  document.body.appendChild(m);
  const r = ancre.getBoundingClientRect();
  const W = innerWidth, H = innerHeight, mw = m.offsetWidth, mh = m.offsetHeight;
  m.style.left = Math.max(8, Math.min(r.left, W - mw - 8)) + 'px';
  m.style.top = (r.bottom + 4 + mh > H - 8 ? Math.max(8, r.top - mh - 4) : r.bottom + 4) + 'px';
  menuOuvert = { m, ancre };
  ancre.setAttribute('aria-expanded', 'true');
  setTimeout(() => document.addEventListener('pointerdown', horsMenu, true), 0);
  return m;
}
function horsMenu(e) { if (menuOuvert && !menuOuvert.m.contains(e.target) && !menuOuvert.ancre.contains(e.target)) fermeMenu(); }
function fermeMenu() {
  if (!menuOuvert) return;
  menuOuvert.ancre.setAttribute('aria-expanded', 'false');
  menuOuvert.m.remove(); menuOuvert = null;
  document.removeEventListener('pointerdown', horsMenu, true);
}

/* ---------- Stockage local (toujours protégé) ---------- */
const CLE = 'claude-pixel:';
const stocke = {
  lis(k, def) { try { const v = localStorage.getItem(CLE + k); return v === null ? def : JSON.parse(v); } catch (e) { return def; } },
  ecris(k, v) { try { localStorage.setItem(CLE + k, JSON.stringify(v)); return true; } catch (e) { return false; } },
  retire(k) { try { localStorage.removeItem(CLE + k); } catch (e) { /* rien */ } }
};

/* ---------- Téléchargements : capacité « downloads », sinon lien blob ---------- */
let dl = null, dlPret = false, dlEssai = null;
function initTelechargements() {
  dlEssai = (async () => {
    try { if (G.claude && typeof G.claude.use === 'function') dl = await G.claude.use('downloads'); } catch (e) { dl = null; }
    dlPret = true;
    return dl;
  })();
  return dlEssai;
}
function enBlob(data, type) { return data instanceof Blob ? data : new Blob([data], { type: type || 'application/octet-stream' }); }
async function telecharge(nom, data, type) {
  if (!dlPret && dlEssai) await Promise.race([dlEssai, new Promise(r => setTimeout(r, 1500))]);
  if (dl) {
    try {
      const r = await dl.save({ filename: nom, data: enBlob(data, type) });
      if (r && r.status === 'saved') toast('Fichier enregistré : ' + nom, 'ok');
      return true;
    } catch (e) {
      const c = e && e.code;
      if (c === 'declined') toast('Enregistrement annulé.', 'info');
      else if (c === 'rate_limited') toast('Une autre demande est en cours : réessaie dans un instant.', 'alerte');
      else if (c === 'rejected_extension') toast('Ce type de fichier est refusé par la visionneuse.', 'refus');
      else if (c === 'unavailable') { dl = null; toast('Enregistrement indisponible dans cette vue.', 'alerte'); }
      else toast('Échec de l\'enregistrement : ' + (e && e.message || c || 'inconnu'), 'refus');
      return false;
    }
  }
  // Hors visionneuse (fichier ouvert directement, tests) : lien blob classique.
  try {
    const url = URL.createObjectURL(enBlob(data, type));
    const a = h('a', { href: url, download: nom }); document.body.appendChild(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 4000);
    toast('Téléchargement : ' + nom, 'ok');
    return true;
  } catch (e) { toast('Téléchargement impossible ici.', 'refus'); return false; }
}

/* ---------- Ouverture d'un fichier local ---------- */
function choisitFichier(accept) {
  return new Promise(ok => {
    const i = h('input', { type: 'file', accept, style: { display: 'none' } });
    i.addEventListener('change', () => { ok(i.files && i.files[0] || null); i.remove(); });
    i.addEventListener('cancel', () => { ok(null); i.remove(); });
    document.body.appendChild(i); i.click();
  });
}
const litTexte = f => new Promise((ok, ko) => { const r = new FileReader(); r.onload = () => ok(r.result); r.onerror = ko; r.readAsText(f); });
function litImage(f) {
  return new Promise((ok, ko) => {
    const url = URL.createObjectURL(f), img = new Image();
    img.onload = () => {
      const c = document.createElement('canvas'); c.width = img.naturalWidth; c.height = img.naturalHeight;
      const x = c.getContext('2d'); x.drawImage(img, 0, 0);
      const d = x.getImageData(0, 0, c.width, c.height);
      URL.revokeObjectURL(url); ok({ w: c.width, h: c.height, data: d.data });
    };
    img.onerror = () => { URL.revokeObjectURL(url); ko(new Error('Image illisible')); };
    img.src = url;
  });
}

/* ---------- Thème ---------- */
function themeEffectif() {
  const t = document.documentElement.getAttribute('data-theme');
  if (t) return t;
  return G.matchMedia && matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
}
function appliqueTheme(t) {
  if (t) document.documentElement.setAttribute('data-theme', t); else document.documentElement.removeAttribute('data-theme');
  stocke.ecris('theme', t || null);
  U.redessine && U.redessine();
}
function basculeTheme() { appliqueTheme(themeEffectif() === 'dark' ? 'light' : 'dark'); }
function couleurToken(nom) { return getComputedStyle(document.documentElement).getPropertyValue(nom).trim() || '#000'; }

/* ---------- Mode Claude ---------- */
function detecteMode() {
  const q = (location.search || '').toLowerCase(), hs = (location.hash || '').toLowerCase();
  return /(^|&)mode=claude(&|$)/.test(q.replace(/^\?/, '')) || hs === '#claude' ? 'claude' : 'humain';
}

/* ---------- Petits utilitaires ---------- */
const hexDe = c => AP.hex(c);
const estVide = c => !(c >>> 24);
function pxVersCanvas(cv, px, w, h, fond) {
  cv.width = w; cv.height = h;
  const x = cv.getContext('2d');
  const id = x.createImageData(w, h);
  const s = new Uint8ClampedArray(px.buffer, px.byteOffset, w * h * 4);
  id.data.set(s);
  x.putImageData(id, 0, 0);
  if (fond) { x.globalCompositeOperation = 'destination-over'; x.fillStyle = fond; x.fillRect(0, 0, w, h); x.globalCompositeOperation = 'source-over'; }
  return cv;
}
function b64(u8) { let s = ''; for (let i = 0; i < u8.length; i += 0x8000) s += String.fromCharCode.apply(null, u8.subarray(i, i + 0x8000)); return btoa(s); }
function nomFichier(s) { return String(s || 'dessin').normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9-_]+/gi, '-').replace(/^-+|-+$/g, '').toLowerCase() || 'dessin'; }
function debounce(fn, ms) { let t; return (...a) => { clearTimeout(t); t = setTimeout(() => fn(...a), ms); }; }

/* Résultat d'une action : on affiche les refus (le message est déjà émis par l'atelier). */
function verifie(r) { return !(r && r.refus); }

Object.assign(U, {
  $, $$, h, toast, modale, ferme, confirme, menu, fermeMenu, stocke, initTelechargements, telecharge,
  choisitFichier, litTexte, litImage, themeEffectif, appliqueTheme, basculeTheme, couleurToken, detecteMode,
  hexDe, estVide, pxVersCanvas, b64, nomFichier, debounce, verifie,
  get modaleOuverte() { return !!modaleOuverte; }, get menuOuvert() { return !!menuOuvert; }
});
})(window);
