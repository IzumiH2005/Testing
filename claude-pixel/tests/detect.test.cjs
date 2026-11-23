// Les détecteurs de défauts (A8, A6) : chacun trouve son cas et laisse passer le bon dessin.
const test = require('node:test');
const assert = require('node:assert/strict');
const { AP, doc } = require('./aide.cjs');

const C = '#3a2b4c', Y = '#ffcc00';
const ids = d => AP.detecte(d).map(x => x.id);

test('« L » et pixel orphelin', () => {
  const p = [[2, 2, C], [3, 2, C], [3, 3, C], [4, 4, C], [10, 10, Y]];
  for (const [dx, dy] of [[-1, -1], [0, -1], [1, -1], [-1, 0], [1, 0], [-1, 1], [0, 1], [1, 1]]) p.push([10 + dx, 10 + dy, C]);
  assert.deepEqual(AP.detecte(doc(16, 16, p)).map(x => x.id + ':' + x.pixels.length), ['L:1', 'orphelins:1']);
});

test('un rectangle propre ne déclenche rien', () => {
  const p = []; for (let i = 2; i < 10; i++) p.push([i, 2, C], [i, 9, C], [2, i, C], [9, i, C]);
  assert.deepEqual(ids(doc(16, 16, p)), []);
});

test('escalier irrégulier 3-1-2-1-3 : jaggies ; escalier régulier : rien', () => {
  let p = [], x = 0; [3, 1, 2, 1, 3].forEach((n, y) => { for (let k = 0; k < n; k++) p.push([x + k, y, C]); x += n; });
  const r = AP.detecte(doc(16, 8, p));
  assert.equal(r.length, 1); assert.equal(r[0].id, 'jaggies'); assert.deepEqual(r[0].pixels, [[4, 2], [5, 2]]);
  p = []; x = 0; [2, 1, 2, 1, 2, 1].forEach((n, y) => { for (let k = 0; k < n; k++) p.push([x + k, y, C]); x += n; });
  assert.deepEqual(ids(doc(16, 8, p)), []);
});

const rampe = ['#201030', '#403060', '#6050a0', '#8080d0', '#b0b0f0'];
function disque(f) { const p = []; for (let y = 0; y < 20; y++) for (let x = 0; x < 20; x++) { const dx = x - 9.5, dy = y - 9.5; if (Math.hypot(dx, dy) < 9.5) p.push([x, y, rampe[f(dx, dy)]]); } return doc(20, 20, p); }

test('ombrage en coussin détecté, éclairage haut-gauche accepté', () => {
  assert.deepEqual(ids(disque((dx, dy) => Math.min(4, Math.floor((9.5 - Math.hypot(dx, dy)) / 2)))), ['coussin', 'lumiere']);
  assert.deepEqual(ids(disque((dx, dy) => Math.max(0, Math.min(4, Math.floor((-(dx + dy) / 19 + 0.5) * 5))))), []);
});

test('pixels doublés (superpixels)', () => {
  const p = []; for (let y = 0; y < 8; y++) for (let x = 0; x < 8; x++) p.push([x, y, ((x >> 1) + (y >> 1)) % 2 ? C : Y]);
  assert.deepEqual(ids(doc(8, 8, p)), ['superpixels']);
});

test('pixel semi-transparent : AA vers le vide signalé ; pixels opaques : rien', () => {
  const p = []; for (let i = 2; i < 10; i++) p.push([i, 2, C], [i, 9, C], [2, i, C], [9, i, C]);
  assert.deepEqual(ids(doc(16, 16, p)), []);
  p.push([1, 1, '#3a2b4c80']);
  const r = AP.detecte(doc(16, 16, p)).find(x => x.id === 'alpha');
  assert.ok(r); assert.deepEqual(r.pixels, [[1, 1]]);
});

test('raccords : dans un gabarit d\'autotile, seules les tuiles qui se répètent doivent se raccorder', () => {
  // 5×3 tuiles de 4 px : un bloc dont le bord haut est clair, le reste sombre.
  const tw = 4, w = 20, h = 12, px = new Uint32Array(w * h), C = AP.parseHex('#404040'), H = AP.parseHex('#c0c0c0');
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) px[y * w + x] = (y % tw === 0 && y < tw) ? H : C;
  // coin haut gauche : arrondi (un pixel vide) ; il n'a pas à se raccorder
  px[0] = 0;
  assert.equal(AP.DETECT.raccords(px, w, h, tw, tw, true).pts.length, 0);
  // le centre (tuile 1,1) qui ne se raccorde pas est signalé
  for (let k = 0; k < tw; k++) { px[(tw + k) * w + tw] = H; px[tw * w + tw + k] = H; }
  assert.ok(AP.DETECT.raccords(px, w, h, tw, tw, true).pts.length > 0);
});
