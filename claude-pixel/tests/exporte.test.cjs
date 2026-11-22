// Les exports : PNG, GIF (y compris gros LZW), planche, palettes, rejeu du journal.
const test = require('node:test');
const assert = require('node:assert/strict');
const { AP } = require('./aide.cjs');

const signature = (buf, octets) => assert.deepEqual([...buf.slice(0, octets.length)], octets);

function atelier() {
  const at = new AP.Atelier({ doc: { w: 16, h: 16, palette: 'PICO-8' } });
  at.input({ type: 'down', x: 2, y: 2 }); at.input({ type: 'move', x: 12, y: 9 }); at.input({ type: 'up', x: 12, y: 9 });
  at.act('image.duplique', {}); at.act('couleur', { c1: '#ff004d' });
  at.input({ type: 'down', x: 2, y: 12 }); at.input({ type: 'up', x: 13, y: 12 });
  return at;
}

test('PNG et GIF ont des en-têtes valides', () => {
  const at = atelier();
  signature(AP.pngImage(at.doc, 0, 8), [0x89, 0x50, 0x4e, 0x47]);
  signature(AP.gifDoc(at.doc, { echelle: 8 }), [0x47, 0x49, 0x46, 0x38]);
});

test('GIF de bruit 200×150 (dictionnaire LZW plein) et nombres de couleurs extrêmes', () => {
  for (const nc of [2, 5, 16, 200]) {
    const w = 200, h = 150, px = new Uint32Array(w * h); let s = 7;
    for (let i = 0; i < px.length; i++) { s = (s * 1103515245 + 12345) >>> 0; const k = (s >>> 16) % nc; px[i] = AP.pack(k * 7 % 256, k * 13 % 256, k * 29 % 256, (k === 0 && nc === 5) ? 0 : 255); }
    const g = AP.gif([{ px, ms: 50 }, { px, ms: 50 }], w, h);
    signature(g, [0x47, 0x49, 0x46, 0x38]); assert.equal(g[g.length - 1], 0x3b);
  }
});

test('planche : une image par case, durées dans le JSON', () => {
  const pl = AP.planche(atelier().doc, { echelle: 4, marge: 2 });
  signature(pl.png, [0x89, 0x50, 0x4e, 0x47]);
  const j = JSON.parse(pl.json);
  assert.equal(j.frames.length, 2); assert.equal(j.frames[0].duration, 100);
});

test('palettes GPL et HEX se relisent', () => {
  const d = atelier().doc;
  assert.match(AP.paletteGpl(d), /^GIMP Palette/);
  assert.equal(AP.lisPalette(AP.paletteGpl(d)).length, 16);
  assert.equal(AP.lisPalette(AP.paletteHex(d)).length, 16);
});

test('le journal se rejoue jusqu\'au dessin final', () => {
  const at = atelier();
  const L = AP.lecteur(at.journal); while (L.avance(1));
  const e = L.etat();
  assert.equal(e.w, 16); assert.equal(e.h, 16);
  assert.equal([...e.px].filter(c => c >>> 24).length, 23);
});
