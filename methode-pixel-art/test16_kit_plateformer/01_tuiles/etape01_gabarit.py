# Étape 01 : gabarit grossier de l'autotile (F2-C), en aplats. Chaque rangée est décidée à la
# main (notation rle : « c26 » = 26 fois c). Le script ne fait que vérifier et écrire.
import sys; sys.path.insert(0, '../../outils')
from pxlib import rle
ilot = [rle(s) for s in [
'. . . O26 . . .',
'. . O i26 O . .',
'. O i28 O .',
'O i h28 g O',
'O i h27 g g O',
'O h g28 b O',
'O e g b27 a O',
] + ['O e d c26 b a O'] * 21 + [
'O e d b26 b a O',
'. O d b26 a O .',
'. . O a26 O . .',
'. . . O26 . . .',
]]
coins = [rle(s) for s in [
'i e d c10 b a i',
'i i d c10 a h i',
'i h g c9 b g h i',
'h h g b c7 b b g h h',
'h g b c8 b b g h h',
'g b c11 b g g',
'b c14 b',
'c16', 'c16', 'c16', 'c16', 'c16',
'b c14 b',
'b b c12 b b',
'a b b c9 b b b a',
'a a b c9 b a a a',
]]
for name, g, w in [('etape01_gabarit_ilot.txt', ilot, 32), ('etape01_gabarit_coins.txt', coins, 16)]:
    assert len(g) == w and all(len(r) == w for r in g), (name, [len(r) for r in g])
    open(name, 'w').write('# ' + name + ' — gabarit grossier, aplats (F2-C)\n' + '\n'.join(g) + '\n')
