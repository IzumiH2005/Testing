// Le cœur : outils de dessin, annulation, journal, sauvegarde.
const test = require('node:test');
const assert = require('node:assert/strict');
const { AP, texte, trait } = require('./aide.cjs');

test('le crayon pose un pixel par case traversée', () => {
  const a = new AP.Atelier({ doc: { w: 16, h: 16 } });
  a.act('couleur', { c1: '#ff0000' });
  trait(a, [[1, 1], [2, 1], [2, 2], [3, 2]]);
  assert.equal(texte(a.doc, 0, 4), '................\n.#..............\n..##............\n................\n');
});

test('ellipse, puis ligne tracée avec Maj (m = 1)', () => {
  const a = new AP.Atelier({ doc: { w: 16, h: 16 } });
  a.act('outil', { nom: 'ellipse' }); a.input({ type: 'down', x: 4, y: 4 }); a.input({ type: 'up', x: 13, y: 11 });
  assert.equal(texte(a.doc, 4, 12), [
    '.......####.....', '.....##....##...', '....#........#..', '....#........#..',
    '....#........#..', '....#........#..', '.....##....##...', '.......####.....'].join('\n') + '\n');
  a.act('outil', { nom: 'ligne' }); a.input({ type: 'down', x: 0, y: 15, m: 0 }); a.input({ type: 'up', x: 8, y: 11, m: 1 });
  assert.equal(texte(a.doc, 12, 16), '......##........\n....##..........\n..##............\n##..............\n');
});

test('annuler puis refaire garde le journal intègre', () => {
  const a = new AP.Atelier({ doc: { w: 16, h: 16 } });
  trait(a, [[0, 0], [5, 0]]);
  const avant = texte(a.doc);
  a.act('annule'); assert.notEqual(texte(a.doc), avant);
  a.act('refait'); assert.equal(texte(a.doc), avant);
  assert.equal(a.integrite().ok, true);
});

test('un projet sauvegardé se recharge à l\'identique', () => {
  const a = new AP.Atelier({ doc: { w: 16, h: 16 } });
  trait(a, [[2, 2], [9, 7]]);
  const b = new AP.Atelier(); b.charge(JSON.parse(JSON.stringify(a.projet())));
  assert.equal(b.integrite().ok, true);
  assert.equal(b.journal.length, a.journal.length);
  assert.equal(texte(b.doc), texte(a.doc));
});
