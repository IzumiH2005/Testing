// La méthode : règles extraites du document, portes bloquantes en mode Claude.
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { AP, trait, RACINE } = require('./aide.cjs');

const FICHE = { quoi: 'potion', usage: 'inventaire', couleurs: '8', projection: 'de face', lumiere: 'haut gauche', matiere: 'verre', accent: 'rouge' };

test('les 85 règles impératives sont extraites du document', () => {
  const R = AP.extraitRegles(fs.readFileSync(path.join(RACINE, 'METHODE_PIXEL_ART.md'), 'utf8'));
  assert.equal(R.length, 85);
  assert.deepEqual(R.map(r => r.n), Array.from({ length: 85 }, (_, i) => i + 1));
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
  // étape 2 : la vision s'écrit, et se corrige
  assert.equal(AP.etapeCourante(at.doc).id, 'vision');
  assert.match(at.act('etape.valide').refus, /Carnet/);
  for (const r of ['vision', 'structure', 'formes', 'unique', 'logique']) at.act('carnet.ajoute', { rubrique: r, texte: 'idée ' + r });
  assert.match(at.act('etape.valide').refus, /barre au moins une idée/);
  assert.ok(at.act('carnet.barre', { i: 0, raison: 'court' }).refus, 'une raison trop courte est refusée');
  at.act('carnet.ajoute', { rubrique: 'vision', texte: 'fiole en goutte inversée' });
  at.act('carnet.barre', { i: 0, raison: 'trop banal, on ne le reconnaît pas' });
  assert.equal(at.doc.meta.carnet[0].barre, true);
  assert.deepEqual(at.act('etape.valide'), { ok: true, manque: [] });
  // étape 3 : les essais, en calque de construction
  assert.equal(AP.etapeCourante(at.doc).id, 'essais');
  at.act('calque.ajoute', { type: 'construction' });
  at.act('outil', { nom: 'crayon' }); trait(at, [[3, 3], [3, 8]]);
  assert.match(at.act('etape.valide').refus, /Essai/);
  for (let k = 0; k < 6; k++) {
    at.act('carnet.ajoute', { rubrique: 'essai', texte: 'silhouette ' + k });
    at.act('carnet.ajoute', { rubrique: 'critique', texte: 'silhouette ' + k + ' : ' + (14 + k * 2) + '/30' });
  }
  assert.match(at.act('etape.valide').refus, /3 idées barrées/);
  at.act('carnet.barre', { i: 6, raison: 'silhouette illisible à ×1' });
  at.act('carnet.barre', { i: 8, raison: 'trop proche d\'une potion ronde' });
  at.act('carnet.ajoute', { rubrique: 'choix', texte: 'silhouette 5 : 24/30, le col tordu se lit' });
  assert.ok(AP.etatEtape(at).portes.every(p => p.manque === null));
  assert.match(at.act('etape.valide').refus, /Case non cochée/);
  for (const c of ['familles', 'generique', 'lisible']) at.act('coche', { cle: 'essais.' + c, valeur: true });
  assert.deepEqual(at.act('etape.valide'), { ok: true, manque: [] });
  // étape 4 (objet, v21) : le design des pièces, 9 variantes
  assert.equal(AP.etapeCourante(at.doc).id, 'pieces');
  assert.match(at.act('etape.valide').refus, /9 « Pièce »/);
  for (let k = 0; k < 9; k++) at.act('carnet.ajoute', { rubrique: 'piece', texte: 'variante ' + k });
  assert.equal(AP.etatEtape(at).portes.find(p => p.id === 'carnetPieces').manque, null);
});

test('un document v17 garde ses 15 étapes ; un nouveau document a l\'étape « pièces »', () => {
  const d = AP.nouveauDoc({ w: 16, h: 16, type: 'objet' });
  assert.equal(d.meta.methode, 22);
  assert.ok(AP.etapesDe(d).some(e => e.id === 'pieces'));
  d.meta.methode = 17;
  assert.equal(AP.nbEtapes(d), 15);
  assert.ok(!AP.etapesDe(d).some(e => e.id === 'pieces'));
});

test('la fusion silencieuse d\'une couleur est signalée', () => {
  const at = new AP.Atelier({ doc: AP.nouveauDoc({ w: 8, h: 8 }) });
  at.act('couleur', { c1: '#ff0000' }); at.act('outil', { nom: 'crayon' }); trait(at, [[1, 1], [1, 1]]);
  at.act('couleur', { c1: '#00ff00' }); trait(at, [[3, 3], [3, 3]]);
  at.act('outil', { nom: 'remplace' }); at.act('couleur', { c1: '#00ff00' });
  trait(at, [[1, 1], [1, 1]]);
  assert.ok(at.messages.some(m => /Fusion/.test(m.msg)));
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

test('v22 : le sketching d\'illustrateur, calque par calque, puis la validation du dessin', () => {
  const at = new AP.Atelier({ doc: AP.nouveauDoc({ w: 16, h: 16, type: 'objet' }) }), d = at.doc;
  const ids = AP.etapesDe(d).map(e => e.id);
  for (const [a, b] of [['pieces', 'rough'], ['rough', 'construction'], ['construction', 'esquisse'], ['esquisse', 'forme'], ['forme', 'polish'], ['polish', 'validation'], ['validation', 'aplats']])
    assert.equal(ids.indexOf(b), ids.indexOf(a) + 1, a + ' puis ' + b);
  const porte = id => { d.meta.etape = ids.indexOf(id); return AP.etatEtape(at).portes; };
  // un calque de construction par passe
  const passe = (nom, x) => { at.act('calque.ajoute', { type: 'construction', nom }); at.act('outil', { nom: 'crayon' }); trait(at, [[x, 2], [x, 6]]); };
  passe('vignettes', 1);
  assert.match(porte('rough').find(p => p.id === 'calquesConstr2').manque, /il y en a 1/);
  passe('rough', 3);
  assert.equal(porte('rough').find(p => p.id === 'calquesConstr2').manque, null);
  passe('volumes', 5);
  assert.match(porte('construction').find(p => p.id === 'dessousBaisse').manque, /Baisse/);
  for (const c of d.calques.filter(c => c.type === 'construction').slice(0, -1)) c.opacite = 30;
  assert.equal(porte('construction').find(p => p.id === 'dessousBaisse').manque, null);
  // la validation demande une note de 22/30 au moins
  assert.match(porte('validation').find(p => p.id === 'critiqueDessin').manque, /note du dessin/);
  at.act('carnet.ajoute', { rubrique: 'critique', texte: 'Dessin : 19/30, col trop long' });
  assert.match(porte('validation').find(p => p.id === 'critiqueDessin').manque, /19\/30/);
  at.act('carnet.ajoute', { rubrique: 'critique', texte: 'Dessin repris : 23/30' });
  assert.equal(porte('validation').find(p => p.id === 'critiqueDessin').manque, null);
  // un écart écrit après la note, sans note, ne la masque pas
  at.act('carnet.ajoute', { rubrique: 'critique', texte: 'Écart avec la référence : le calice reste plat.' });
  assert.equal(porte('validation').find(p => p.id === 'critiqueDessin').manque, null);
});
