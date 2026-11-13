# Étape 05 : variantes (règle 36). Tuiles 16×16 complètes qui gardent EXACTEMENT les bords de
# la tuile de base (remplissage : bord tout c ; croûte : colonnes 0/15 et rangée 15 de la tuile
# du haut). Chaque rangée est décidée à la main (rle). Le script vérifie les bords et écrit.
import sys; sys.path.insert(0, '../../outils')
from pxlib import rle, load_grid
I = load_grid('etape03_ilot.txt')
haut = [I[y][16:24] + I[y][8:16] for y in range(16)]   # tuile « croûte » de base

V = {}
# Remplissage 1 : grande fissure en Y qui traverse la face (règle 41 : b + lèvre d, fourche).
V['etape05_rempl1.txt'] = ['c16', 'c10 b c5', 'c9 b d c5', 'c8 b d c6', 'c8 b c7', 'c7 b d c7',
    'c7 b c8', 'c6 b d c8', 'c5 b b b d c7', 'c4 b d c c b c7', 'c3 b d c3 b d c6',
    'c3 b c6 b c5', 'c c b d c6 b d c4', 'c11 b c4', 'c12 d c3', 'c16']
# Remplissage 2 : poche de cristal turquoise dans la roche (rappel du thème, sans halo :
# la lueur reste pour les grands cristaux). Face gauche éclairée w, droite u/t, pointe W ;
# plafond de la poche sombre (a), lèvre du bas éclairée (d).
V['etape05_rempl2.txt'] = ['c16', 'c16', 'c16', 'c16', 'c7 b b c7', 'c6 b a W a b c5',
    'c5 b a w v u a b c4', 'c5 b a w v u a W b c3', 'c5 b a w v u w u a c3',
    'c5 b a v v t v t a c3', 'c6 b a5 d c3', 'c7 d5 c4', 'c16', 'c16', 'c16', 'c16']
# Croûte 1 : une pierre affleure dans la mousse (haut éclairé e, ombre b dessous).
V['etape05_croute1.txt'] = ['O16', 'j i h h e e d h i j j i h i j j',
    'i i h d e d d c h i3 h i3', 'h h g d d c c b g i h h g h h i',
    'g3 b c c b g g h g4 h h', 'g b4 b g b b g g b b b g g', haut[6]] + haut[7:]
# Croûte 2 : une grosse touffe pend sous l'avancée (gouttes jusqu'à y9) + un filament à x3.
V['etape05_croute2.txt'] = haut[:4] + ['g4 h g3 h3 g3 h h', 'g b b b g g b b g h g g b b g g',
    'g b b g b4 g h g g b4', 'c3 g c3 b g g g b c4', 'c8 b g g b c4', 'c9 g b c5'] + haut[10:]
# Le contour de la croûte 1 : la pierre affleure à ras, le contour du haut ne bouge pas.
fill_border = lambda g: g[0] == 'c'*16 and g[15] == 'c'*16 and all(r[0] == 'c' and r[15] == 'c' for r in g)
for name, rows in V.items():
    g = [r if len(r) == 16 and ' ' not in r and not r[1:].isdigit() and r in haut else rle(r) for r in rows]
    assert len(g) == 16 and all(len(r) == 16 for r in g), (name, [len(r) for r in g])
    if 'rempl' in name:
        assert fill_border(g), name
    else:
        assert all(g[y][0] == haut[y][0] and g[y][15] == haut[y][15] for y in range(16)) and g[15] == haut[15], name
    open(name, 'w').write('# ' + name + ' (écrit par etape05_variantes.py)\n' + '\n'.join(g) + '\n')
    print(name, 'ok')
