// La méthode : règles extraites du document, portes bloquantes en mode Claude.
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { AP, trait, RACINE } = require('./aide.cjs');

const FICHE = { quoi: 'potion', usage: 'inventaire', couleurs: '8', projection: 'de face', lumiere: 'haut gauche', matiere: 'verre', accent: 'rouge' };

test('les 42 règles impératives sont extraites du document', () => {
  const R = AP.extraitRegles(fs.readFileSync(path.join(RACINE, 'METHODE_PIXEL_ART.md'), 'utf8'));
  assert.equal(R.length, 42);
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
  at.act('outil', { nom: 'crayon' }); trait(at, [[3, 3], [3, 8]]);
  assert.ok(AP.etatEtape(at).portes.every(p => p.manque === null));
  assert.match(at.act('etape.valide').refus, /Case non cochée/);
});
