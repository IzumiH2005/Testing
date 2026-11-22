// La vraie séance « potion » : le fichier enregistré par la souris se recharge, intègre et fini.
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { AP, RACINE } = require('./aide.cjs');

const F = path.join(RACINE, 'seances', 'potion', 'fichiers', 'potion-de-soin.claude-pixel.json');

test('la potion de la séance filmée : méthode terminée, journal intègre, aucun défaut', { skip: !fs.existsSync(F) && 'séance absente' }, () => {
  const at = new AP.Atelier(); at.charge(JSON.parse(fs.readFileSync(F, 'utf8')));
  assert.equal(at.integrite().ok, true);
  assert.equal(at.doc.w, 16); assert.equal(at.doc.h, 16);
  assert.ok(at.doc.meta.etape >= AP.nbEtapes(at.doc));
  assert.deepEqual(AP.detecte(at.doc).map(x => x.id), []);
});
