// Outils communs aux tests : charge les modules de l'app dans Node (sans navigateur).
const path = require('node:path');
const SRC = path.join(__dirname, '..', 'app', 'src');
const AP = require(path.join(SRC, 'core.js'));
for (const m of ['volume.js', 'detect.js', 'methode.js', 'exporte.js']) require(path.join(SRC, m));

// Un document w×h rempli des points [x, y, '#rrggbb'].
function doc(w, h, pts) {
  const d = AP.nouveauDoc({ w, h }); const L = d.calques[0]; const id = 'cx';
  d.celData[id] = new Uint32Array(w * h); d.cels[L.id][0] = id;
  for (const [x, y, c] of pts) d.celData[id][y * w + x] = AP.parseHex(c);
  return d;
}
// Le dessin en texte : « # » pour un pixel posé, « . » sinon.
function texte(d, y0 = 0, y1 = d.h) {
  const px = AP.compose(d, 0); let s = '';
  for (let y = y0; y < y1; y++) { for (let x = 0; x < d.w; x++) s += px[y * d.w + x] ? '#' : '.'; s += '\n'; }
  return s;
}
const trait = (at, pts) => { at.input({ type: 'down', x: pts[0][0], y: pts[0][1], b: 0 }); for (const [x, y] of pts.slice(1, -1)) at.input({ type: 'move', x, y, b: 0 }); const [x, y] = pts[pts.length - 1]; at.input({ type: 'up', x, y, b: 0 }); };

module.exports = { AP, doc, texte, trait, RACINE: path.join(__dirname, '..') };
