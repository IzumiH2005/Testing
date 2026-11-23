// La méthode : règles extraites du document, portes bloquantes en mode Claude.
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { AP, trait, RACINE } = require('./aide.cjs');

// Les documents v22 gardent les essais à 6 silhouettes et le design des pièces.
const v22 = d => { d.meta.methode = 22; return d; };

const FICHE = { quoi: 'potion', usage: 'inventaire', couleurs: '8', projection: 'de face', lumiere: 'haut gauche', matiere: 'verre', accent: 'rouge' };

test('les 90 règles impératives sont extraites du document', () => {
  const R = AP.extraitRegles(fs.readFileSync(path.join(RACINE, 'METHODE_PIXEL_ART.md'), 'utf8'));
  assert.equal(R.length, 90);
  assert.deepEqual(R.map(r => r.n), Array.from({ length: 90 }, (_, i) => i + 1));
  assert.ok(R.every(r => r.texte && r.groupe));
});

test('en mode Claude, rien ne se dessine avant la lecture des règles', () => {
  const at = new AP.Atelier({ mode: 'claude', doc: AP.nouveauDoc({ w: 16, h: 16, type: 'objet' }) });
  assert.match(at.input({ type: 'down', x: 3, y: 3, b: 0 }).refus, /règles impératives/);
  assert.match(at.act('etape.valide').refus, /Fiche incomplète/);
});

test('v22 : fiche + règles lues ouvrent l\'étape 2, qui exige ses cases cochées', () => {
  const at = new AP.Atelier({ mode: 'claude', doc: { w: 16, h: 16, type: 'objet' } }); v22(at.doc);
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

test('un document v17 garde ses 15 étapes ; un document v22 a l\'étape « pièces »', () => {
  const d = v22(AP.nouveauDoc({ w: 16, h: 16, type: 'objet' }));
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
  const at = new AP.Atelier({ doc: { w: 16, h: 16, type: 'objet' } }), d = v22(at.doc);
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
  // 0-AC-C : un design d'objet se juge à 64 px de haut au moins
  assert.match(porte('validation').find(p => p.id === 'taille64').manque, /64 px/);
  // un écart écrit après la note, sans note, ne la masque pas
  at.act('carnet.ajoute', { rubrique: 'critique', texte: 'Écart avec la référence : le calice reste plat.' });
  assert.equal(porte('validation').find(p => p.id === 'critiqueDessin').manque, null);
});

test('v24 : un nouveau document itère sur une forme de base, sans essais ni pièces', () => {
  const at = new AP.Atelier({ doc: AP.nouveauDoc({ w: 64, h: 64, type: 'objet' }) }), d = at.doc;
  assert.equal(d.meta.methode, 26);
  const ids = AP.etapesDe(d).map(e => e.id);
  assert.ok(!ids.includes('essais') && !ids.includes('pieces'));
  assert.equal(ids.indexOf('iterations'), ids.indexOf('vision') + 1);
  assert.equal(ids.indexOf('rough'), ids.indexOf('iterations') + 1);
  d.meta.etape = ids.indexOf('iterations');
  const manque = () => AP.etatEtape(at).portes.find(p => p.id === 'carnetIterations').manque;
  assert.match(manque(), /3 « Itération »/);
  for (let k = 1; k <= 3; k++) {
    at.act('carnet.ajoute', { rubrique: 'iteration', texte: 'v' + k + ' : coins cassés' });
    at.act('carnet.ajoute', { rubrique: 'critique', texte: 'v' + k + ' : ' + (16 + k * 2) + '/30' });
  }
  assert.match(manque(), /Choix retenu/);
  at.act('carnet.ajoute', { rubrique: 'choix', texte: 'v3, la plus lisible' });
  assert.equal(manque(), null);
});

test('v24 : le décor suit le pipeline d\'un tileset de plateforme', () => {
  const d = AP.nouveauDoc({ w: 160, h: 128, type: 'decor' });
  assert.deepEqual(AP.etapesDe(d).map(e => e.id),
    ['fiche', 'vision', 'iterations', 'palette', 'gabarit', 'centre', 'micro', 'bords', 'lumiere', 'variantes', 'carte', 'details', 'planche']);
  // un document décor v22 garde ses étapes
  assert.ok(AP.etapesDe(v22(AP.nouveauDoc({ w: 16, h: 16, type: 'decor' }))).some(e => e.id === 'essais'));
});

test('v25 : chaque parcours a une étape de micro-détails tenue au carnet', () => {
  for (const t of ['objet', 'personnage', 'chibi', 'creature', 'decor']) {
    const ids = AP.etapesDe(AP.nouveauDoc({ w: 64, h: 64, type: t })).map(e => e.id);
    assert.ok(ids.includes('micro'), t);
  }
  const at = new AP.Atelier({ doc: { w: 64, h: 64, type: 'objet' } }), d = at.doc;
  d.meta.etape = AP.etapesDe(d).findIndex(e => e.id === 'micro');
  const manque = () => AP.etatEtape(at).portes.find(p => p.id === 'carnetDetails8').manque;
  assert.match(manque(), /8 « Détail »/);
  for (let k = 0; k < 8; k++) at.act('carnet.ajoute', { rubrique: 'detail', texte: 'pierre ' + k + ' : contour repris, deux tons' });
  assert.equal(manque(), null);
});

test('v25 : un document v24 passe à la méthode actuelle sans perdre son étape', () => {
  const at = new AP.Atelier({ doc: { w: 160, h: 128, type: 'decor' } }), d = at.doc;
  d.meta.methode = 24;
  d.meta.etape = AP.etapesDe(d).findIndex(e => e.id === 'variantes');
  d.meta.valideEtapes[0] = { ok: true, manque: [] };
  at.act('methode.migre');
  assert.equal(d.meta.methode, AP.METHODE_ACTUELLE);
  assert.equal(AP.etapeCourante(d).id, 'variantes');
  assert.deepEqual(d.meta.valideEtapes[0], { ok: true, manque: [] });
  // on peut revenir à l'étape nouvelle qui précède
  at.act('etape.va', { i: AP.etapesDe(d).findIndex(e => e.id === 'micro') });
  assert.equal(AP.etapeCourante(d).id, 'micro');
  assert.ok(at.act('methode.migre').refus);
});

test('v26 : la passe à la loupe demande chaque zone de la tuile centrale, marquée une par une', () => {
  const at = new AP.Atelier({ doc: { w: 160, h: 128, type: 'decor' } }), d = at.doc;
  at.act('tuile.reglage', { on: true, tw: 32, th: 32 });
  // de la terre partout
  const id = d.cels[d.calques[0].id][0] = 'cz'; d.celData[id] = new Uint32Array(160 * 128).fill(AP.parseHex('#8e5a4a'));
  d.meta.etape = AP.etapesDe(d).findIndex(e => e.id === 'micro');
  const porte = () => AP.etatEtape(at).portes.find(p => p.id === 'zonesTuile').manque;
  assert.match(porte(), /4 zone\(s\) sur 4/);           // tuile centrale, zones de 16 px
  at.act('zones.taille', { taille: 8 });
  assert.match(porte(), /16 zone\(s\) sur 16/);
  for (let y = 4; y < 8; y++) for (let x = 4; x < 8; x++) at.act('zones.marque', { x, y });
  assert.equal(porte(), null);
  assert.ok(at.act('zones.marque', { x: 40, y: 0 }).refus);
});

test('v26 : la tuile centrale se rend en six passes notées au carnet', () => {
  const d = AP.nouveauDoc({ w: 160, h: 128, type: 'decor' });
  const e = AP.etapesDe(d).find(x => x.id === 'centre');
  assert.ok(e.portes.includes('carnetPasses'));
  assert.equal(e.faire.filter(f => /^\d\. /.test(f)).length, 6);
});

test('ramener un calque à la palette', () => {
  const at = new AP.Atelier({ doc: { w: 4, h: 1 } }), d = at.doc;
  d.palette = ['#000000', '#ffffff', '#ff0000'];
  const id = d.cels[d.calques[0].id][0] = 'cz'; d.celData[id] = Uint32Array.from([AP.parseHex('#101010'), AP.parseHex('#f0f0f0'), AP.parseHex('#e01010'), 0]);
  at.act('calque.indexe');
  assert.deepEqual([...d.celData[d.cels[d.calques[0].id][0]]].map(c => c ? AP.hex(c) : 0), ['#000000', '#ffffff', '#ff0000', 0]);
});
