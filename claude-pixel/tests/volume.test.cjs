// Lumière et volume (partie 0-C) : le guide place les zones au bon endroit, la mesure
// distingue un ombrage qui suit la lumière d'un coussin ou d'une lumière inversée.
const test = require('node:test');
const assert = require('node:assert/strict');
const { AP, doc } = require('./aide.cjs');
const V = AP.VOLUME;

const rampe = ['#201030', '#403060', '#6050a0', '#8080d0', '#b0b0f0'];
const W = 24;
function disque(f) {
  const p = [];
  for (let y = 0; y < W; y++) for (let x = 0; x < W; x++) { const dx = x - 11.5, dy = y - 11.5; if (Math.hypot(dx, dy) < 11) p.push([x, y, rampe[f(dx, dy)]]); }
  return doc(W, W, p);
}
const px = d => AP.compose(d, 0, 'export');
const hautGauche = disque((dx, dy) => Math.max(0, Math.min(4, Math.floor((-(dx + dy) / 22 + 0.5) * 5))));
const basDroite = disque((dx, dy) => Math.max(0, Math.min(4, Math.floor(((dx + dy) / 22 + 0.5) * 5))));
const coussin = disque((dx, dy) => Math.min(4, Math.floor((11 - Math.hypot(dx, dy)) / 2.2)));

test('vecteur de lumière : haut gauche pointe vers le haut et la gauche de l\'écran', () => {
  const [x, y, z] = V.vecteur({ az: 135, el: 40 });
  assert.ok(x < 0 && y < 0 && z > 0);
  assert.equal(V.nomDirection(135), 'haut gauche');
  assert.equal(V.nomDirection(10), 'droite');
});

test('guide : lumière en haut à gauche, ombre propre et rebond en bas à droite, ombre portée sous l\'objet', () => {
  const g = V.guide(px(hautGauche), W, W, { az: 135, el: 40, forme: 'sphere' });
  const z = (x, y) => g.zone[y * W + x];
  assert.ok([1, 2].includes(z(6, 6)), 'haut gauche éclairé');
  assert.ok([4, 5, 6].includes(z(18, 18)), 'bas droite dans la famille ombre');
  assert.ok(g.zone.includes(1), 'un éclat au moins');
  assert.ok(g.zone.includes(7), 'ombre portée posée');
  assert.ok(g.term.length > 10, 'un terminateur continu');
});

test('mesure : ombrage juste > 0,5 ; coussin < 0,3 ; inversé négatif ; aplat non mesuré', () => {
  const L = { az: 135, el: 40, forme: 'gonfle' };
  assert.ok(V.mesure(px(hautGauche), W, W, L).accord > 0.5);
  assert.ok(V.mesure(px(coussin), W, W, L).accord < 0.3);
  const inv = V.mesure(px(basDroite), W, W, L);
  assert.ok(inv.accord < 0 && inv.inverses > 0.5 && inv.fautifs.length > 20);
  assert.equal(V.mesure(px(disque(() => 2)), W, W, L).accord, null);
});

test('la couleur locale n\'est pas une erreur d\'ombrage : deux matières à plat ne déclenchent rien', () => {
  const p = []; for (let y = 2; y < 22; y++) for (let x = 2; x < 22; x++) p.push([x, y, y < 12 ? '#3060c0' : '#c03040']);
  assert.ok(!AP.detecte(doc(W, W, p)).some(r => r.id === 'lumiere'));
});

test('le détecteur suit la lumière du document : la même sphère est juste à droite, fausse à gauche', () => {
  const d = basDroite;
  d.lumiere = { az: 315, el: 40, forme: 'gonfle', posee: true };
  assert.ok(!AP.detecte(d).some(r => r.id === 'lumiere' || r.id === 'coussin'));
  d.lumiere = { az: 135, el: 40, forme: 'gonfle', posee: true };
  assert.ok(AP.detecte(d).some(r => r.id === 'lumiere'));
});

test('l\'action « lumiere » règle la source et la marque posée ; elle refuse les valeurs absurdes', () => {
  const at = new AP.Atelier({ doc: AP.nouveauDoc({ w: 16, h: 16 }) });
  assert.equal(at.doc.lumiere.posee, false);
  at.act('lumiere', { az: 45, el: 65, forme: 'sphere' });
  assert.deepEqual(at.doc.lumiere, { az: 45, el: 65, forme: 'sphere', posee: true });
  assert.ok(at.act('lumiere', { el: 99 }).refus);
  assert.ok(at.act('lumiere', { forme: 'cube' }).refus);
});

test('notan : deux valeurs seulement', () => {
  const n = V.notan(px(hautGauche)), s = new Set([...n].filter(c => c >>> 24));
  assert.equal(s.size, 2);
});

test('mesure : une rampe à teinte décalée reste une seule matière quand on donne les rampes du document', () => {
  // ombre violacée (teinte 335°), lumière rouge (350°) : deux paquets de teinte différents
  const R = [{ nom: 'velours', couleurs: ['#6f2846', '#963f4e'] }];
  const d = disque((dx, dy) => (dx + dy > 0 ? 0 : 1));
  const map = { [rampe[0]]: '#6f2846', [rampe[1]]: '#963f4e' };
  const p = []; const c = AP.compose(d, 0, 'export');
  for (let i = 0; i < c.length; i++) if (c[i]) p.push([i % W, (i / W) | 0, map[AP.hex(c[i]).slice(0, 7)]]);
  const d2 = doc(W, W, p), L = { az: 135, el: 40, forme: 'gonfle', posee: true };
  const sans = V.mesure(px(d2), W, W, L), avec = V.mesure(px(d2), W, W, L, R);
  assert.equal(sans.accord, null, 'sans les rampes, chaque ton est un aplat d\'une matière à part');
  assert.ok(avec.accord > 0.5, 'avec les rampes, ombre et lumière du velours sont mesurées ensemble : ' + avec.accord);
  assert.ok(avec.ecart > 0.05, 'écart des deux familles : ' + avec.ecart);
  assert.equal(V.matiere(AP.parseHex('#6f2846'), R), V.matiere(AP.parseHex('#963f4e'), R));
});
