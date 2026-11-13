# Dalles de ruine traversables : pierre TAILLÉE (A4b : rectangles, un ton par face).
# Dessus e (face la plus éclairée = où marcher), arête d, face avant c, bas b, contour O.
# Joints : b + lèvre d à droite (le côté qui regarde la lumière). Pas de contour intérieur
# (règle 40). Rangées décidées à la main (rle) ; le script vérifie et écrit.
import sys; sys.path.insert(0, '../../outils')
from pxlib import rle
vide = ['.16'] * 8
D = {
 # bout gauche : coin arrondi, face de bout éclairée (d), joint en x9
 'dalle_g': ['. O15', 'O e8 d e6', 'O e d7 b d6', 'O d c7 b d c5', 'O d c7 b c6',
             'O d c7 b c6', 'O c b7 a b6', '. O15'] + vide,
 # milieu 1 : joint en x11, usure du dessus en x3
 'dalle_m1': ['O16', 'e3 d e7 d e4', 'd3 c d7 b d4', 'c11 b d c3', 'c11 b c4',
              'c11 b c4', 'b11 a b4', 'O16'] + vide,
 # milieu 2 : joint en x4, petite fissure en x9-10, mousse qui déborde en x13 et pend
 'dalle_m2': ['O16', 'e4 d e4 d e3 i i e', 'd4 b d4 b d3 h h d', 'c4 b d c3 b d c c h g c',
              'c4 b c5 b d c g c c', 'c4 b c6 d c g c c', 'b4 a b8 g b b', 'O13 g O O',
              '.13 g . .', '.13 g . .', '.16', '.16', '.16', '.16', '.16', '.16'],
 # bout droit : cassure en marches (ruine), face cassée dans l'ombre, fissure près du bord
 'dalle_d': ['O12 .4', 'e6 d e3 d d O . . .', 'd6 b d d b d d c O . .',
             'c6 b c c b d c b O . .', 'c6 b c3 b d b a O .', 'c6 b c4 b b O . .',
             'b6 a b4 a O . . .', 'O12 .4'] + vide,
}
for k, rows in D.items():
    g = [rle(r) for r in rows]
    assert len(g) == 16 and all(len(r) == 16 for r in g), (k, [len(r) for r in g])
    open(k + '.txt', 'w').write('# ' + k + ' (écrit par etape01_dalles.py)\n' + '\n'.join(g) + '\n')
# raccords : la colonne 15 de chaque pièce doit continuer la colonne 0 de la suivante
