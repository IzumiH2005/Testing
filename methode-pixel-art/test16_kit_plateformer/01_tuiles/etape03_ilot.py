# Étape 03 : îlot 32×32 final. Chaque segment de rangée est décidé à la main (notation rle).
# Assemblage seulement : bord gauche + centre + bord droit ; le centre des rangées 8-23 est le
# remplissage 02d (tamponné, pas recalculé).
# Contraintes (F2-C) : bande du haut x8-23 qui boucle (x23 -> x8) ; bandes gauche/droite y8-23
# qui bouclent ; colonnes x7 = colonne 15 du milieu et x24 = colonne 0 du milieu (pilier de 1) ;
# rangées 7 et 24 neutres (plateforme de 1) ; rien d'important sur les bords de quarts.
import sys; sys.path.insert(0, '../../outils')
from pxlib import rle, load_grid
T = load_grid('etape02d_remplissage.txt')

# --- HAUT (y0-7) : croûte de mousse en 3 touffes (5, 6, 5 px) : reflet j en haut-gauche de
# chaque touffe, creux h entre elles, dessous g, gouttes g, ombre portée b sous l'avancée.
haut_g = ['. . . O5', '. . O j j i i h', '. O j i i i i h', 'O j i h i h h g',
          'O i h g h g g g', 'O i g b g b g b', 'O h g b5', 'O g b c5']
haut_m = ['O16',
          'i j j i h i j j j i h i j i i h',
          'i4 h i5 h i3 h h',
          'h i h h g h h i h h g h i h h g',
          'g h g3 g h h g3 g h g3',
          'b g g b b b g3 b b b g g b b',
          'b b g b b b b b g b7',
          'c16']
haut_d = ['O5 . . .', 'i i h h g O . .', 'i h h g g g O .', 'h h g g b b a O',
          'g g g b b b a O', 'b g b4 a O', 'b6 a O', 'c5 b a O']

# --- CÔTÉS (y8-23) : gauche éclairée (liseré e cassé, d), droite dans l'ombre (b, a).
# Un éclat dans chaque bord, loin des limites de quarts (gauche y11-12, droite y18-19).
gauche = ['O e d c5', 'O e d c5', 'O e c6', '. O e d c4', '. O e d c4', 'O e e d c4',
          'O d d c5', 'O e d c5',
          'O e d c5', 'O e d c5', 'O e d d d c3', 'O d d c5', 'O e c c c b b c', 'O e d c5',
          'O e c6', 'O e d c5']
droite = ['c5 b a O', 'c5 b a O', 'c5 c a O', 'c4 b b a O', 'c3 b c b a O', 'c5 b a O',
          'c5 b a O', 'c5 c a O',
          'c5 b a O', 'c5 b a O', 'c4 b a O .', 'c3 b b a O .', 'c4 b b a O', 'c5 b a O',
          'c5 c a O', 'c5 b a O']

# --- BAS (y24-31) : dessous sombre ; un renfoncement de 3 px dans le contour du milieu.
bas_g = ['O e d c5', 'O e d c5', 'O d c6', 'O d c6', 'O c b6', '. O b6', '. . O a5', '. . . O5']
bas_m = ['c16', 'c16', 'c3 d d c11', 'c5 b c10', 'b8 c b7', 'b b a b7 a3 b3',
         'a10 O3 a3', 'O10 . . . O3']
bas_d = ['c5 b a O', 'c5 b a O', 'c4 b b a O', 'c4 b a a O', 'b5 a a O', 'b4 a a O .',
         'a5 O . .', 'O5 . . .']

rows = []
for y in range(8):
    rows.append(rle(haut_g[y]) + rle(haut_m[y]) + rle(haut_d[y]))
for y in range(16):
    rows.append(rle(gauche[y]) + T[y] + rle(droite[y]))
for y in range(8):
    rows.append(rle(bas_g[y]) + rle(bas_m[y]) + rle(bas_d[y]))
assert len(rows) == 32 and all(len(r) == 32 for r in rows), [len(r) for r in rows]
# contrôles de raccord
assert all(rows[y][7] == rows[y][23] and rows[y][24] == rows[y][8] for y in list(range(8)) + list(range(24, 32))), 'colonnes 7/24'
open('etape03_ilot.txt', 'w').write('# Étape 03 : îlot final 32×32 (écrit par etape03_ilot.py)\n' + '\n'.join(rows) + '\n')
print('\n'.join(rows))
