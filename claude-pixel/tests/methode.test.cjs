// La méthode : règles extraites du document, portes bloquantes en mode Claude.
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { AP, trait, RACINE } = require('./aide.cjs');

const FICHE = { quoi: 'potion', usage: 'inventaire', couleurs: '8', projection: 'de face', lumiere: 'haut gauche', matiere: 'verre', accent: 'rouge' };

test('les 60 règles impératives sont extraites du document', () => {
  const R = AP.extraitRegles(fs.readFileSync(path.join(RACINE, 'METHODE_PIXEL_ART.md'), 'utf8'));
  assert.equal(R.length, 60);
  assert.deepEqual(R.map(r => r.n), Array.from({ length: 60 }, (_, i) => i + 1));
  assert.ok(R.every(r => r.texte && r.groupe));
});

test('en mode Claude, rien ne se dessine avant la lecture des règles', () => {
  const at = new AP.Atelier({ mode: 'claude', doc: AP.nouveauDoc({ w: 16, h: 16, type: 'objet' }) });
  assert.match(at.input({ type: 'down', x: 3, y: 3, b: 0 }).refus, /règles impératives/);
  assert.match(at.act('etape.valide').refus, /Fiche incomplète/);
});

test('fiche + règles lues ouvrent l\'étape 2, qui exige ses cases cochées', () => {
  const at = new AP.Atelier({ mode: 'claude', doc: AP.nouveauDoc({ w: 16, h: 16, type: 'objet' }) });
  at.act('fiche', { champs: FICHE }); at.act('regles.lues');
  assert.deepEqual(at.act('etape.valide'), { ok: true, manque: [] });
  assert.equal(at.doc.meta.etape, 1);
  assert.equal(AP.etapeCourante(at.doc).id, 'construction');
  assert.match(at.act('etape.valide').refus, /construction/);
  at.act('calque.ajoute', { type: 'construction' });
  at.act('outil', { nom: 'crayon' }); trait(at, [[3, 3], [3, 8]]);
  assert.ok(AP.etatEtape(at).portes.every(p => p.manque === null));
  assert.match(at.act('etape.valide').refus, /Case non cochée/);
});

test('v17 : l\'étape « deux familles » exige la lumière posée et un volume qui la suit', () => {
  const at = new AP.Atelier({ mode: 'claude', doc: AP.nouveauDoc({ w: 24, h: 24, type: 'objet' }) }), d = at.doc;
  d.meta.etape = AP.etapesDe(d).findIndex(e => e.id === 'lumiere');
  // une sphère ombrée à l'envers (lumière en bas à droite)
  const id = d.cels[d.calques[0].id][0] = 'cz'; d.celData[id] = new Uint32Array(24 * 24);
  for (let y = 0; y < 24; y++) for (let x = 0; x < 24; x++) { const dx = x - 11.5, dy = y - 11.5; if (Math.hypot(dx, dy) < 11) d.celData[id][y * 24 + x] = AP.parseHex(dx + dy > 0 ? '#c0a0f0' : '#302050'); }
  let st = AP.etatEtape(at);
  assert.match(st.portes.find(p => p.id === 'lumierePosee').manque, /onglet Lumière/);
  at.act('lumiere', { az: 135 });
  st = AP.etatEtape(at);
  assert.equal(st.portes.find(p => p.id === 'lumierePosee').manque, null);
  assert.match(st.portes.find(p => p.id === 'volume').manque, /accord/);
  at.act('lumiere', { az: 315, el: 10 }); // lumière rasante : le terminateur coupe la sphère en deux
  assert.equal(AP.etatEtape(at).portes.find(p => p.id === 'volume').manque, null);
});

test('un document d\'avant la v17 garde ses étapes', () => {
  const d = AP.nouveauDoc({ w: 16, h: 16, type: 'objet' }); delete d.meta.methode;
  assert.equal(AP.nbEtapes(d), AP.ETAPES_V16.objet.length);
  assert.equal(AP.etapesDe(d)[1].id, 'forme');
});
