"""Colonne brisée 16×48 (décor posé, langage ruine : pierre taillée, un ton par bande).
Fût cylindrique éclairé à gauche : 8 bandes choisies à la main, tambours tous les 11 rangs,
cassure en dents irrégulières en haut, socle plus large en bas. Tout est décidé ici à la main
(nombres et listes) ; la boucle ne fait que recopier les bandes rang par rang."""
import sys; sys.path.insert(0, '../../outils'); from pxlib import save_grid, rle
W, H = 16, 48
g = [['.'] * W for _ in range(H)]
FUT = 'deedccba'                     # x4..x11 : bord clair, reflet, ombre propre, bord sombre
HAUT = {4: 13, 5: 11, 6: 8, 7: 9, 8: 12, 9: 14, 10: 13, 11: 15}   # haut de la cassure par colonne
for x in range(4, 12):
    for y in range(HAUT[x], 41):
        g[y][x] = FUT[x - 4]
    g[HAUT[x] - 1][x] = 'O'
    # la tranche cassée : 1 à 2 px clairs rugueux sous le contour (dessus, donc e/d)
    g[HAUT[x]][x] = 'e' if x < 8 else 'd'
    if x in (6, 7, 9): g[HAUT[x] + 1][x] = 'd' if x < 8 else 'c'
for y in range(min(HAUT.values()), 41):             # contours gauche et droit du fût
    if y >= HAUT[4]: g[y][3] = 'O'
    if y >= HAUT[11]: g[y][12] = 'O'
for x in range(4, 12):                              # contour des marches de la cassure
    for y in range(HAUT[x], 41):
        if x > 4 and y < HAUT[x - 1] and g[y][x - 1] == '.': g[y][x - 1] = 'O'
        if x < 11 and y < HAUT[x + 1] and g[y][x + 1] == '.': g[y][x + 1] = 'O'
# tambours : joint = rang b sur toute la largeur + lèvre d au-dessous côté lumière (règle 41)
for yj in (20, 31):
    for x in range(4, 12): g[yj][x] = 'b' if x < 10 else 'a'
    for x in (4, 5, 6): g[yj + 1][x] = 'e'
# socle : chapiteau inversé (tore) puis plinthe, plus larges ; dessus clair, face, bas sombre
SOCLE = {41: '. O d e3 d c3 b2 a2 O .',
         42: '. O d e4 d c3 b2 a O .',
         43: 'O e d e5 d c3 b a2 O',
         44: 'O d c d4 c4 b2 a2 O',
         45: 'O c b c5 b4 a3 O',
         46: 'O b a b5 a7 O',
         47: '. O14 .'}
for y, s in SOCLE.items():
    r = rle(s); assert len(r) == 16, (y, len(r)); g[y] = list(r)
# fissure du tambour du haut : part de l'arête droite cassée, Y, lèvre claire à droite
for x, y in ((10, 16), (9, 17), (9, 18), (8, 19), (10, 18)): g[y][x] = 'a'
for x, y in ((10, 17), (11, 19)): g[y][x] = 'c'
# éclat manquant sur l'arête gauche du tambour du bas (creux inversé) et mousse
for x, y in ((4, 35), (4, 36), (5, 36)): g[y][x] = 'b'
g[37][5] = 'd'; g[35][3] = '.'; g[36][3] = '.'; g[35][2] = '.'
g[35][3] = 'O'; g[36][3] = 'O'
MOUSSE = [(5, 9, 'i'), (6, 7, 'j'), (7, 8, 'i'), (5, 10, 'h'), (7, 9, 'h'), (6, 8, 'h'),
          (5, 11, 'g'), (6, 9, 'g'), (7, 10, 'g'),
          (1, 41, 'h'), (2, 41, 'i'), (3, 41, 'i'), (4, 41, 'h'), (13, 41, 'h'), (12, 41, 'g'),
          (2, 40, 'O'), (3, 40, 'O'), (4, 40, 'O'), (1, 40, 'O'), (13, 40, 'O'),
          (2, 42, 'g'), (3, 42, 'h'), (4, 43, 'g'), (13, 42, 'g'), (5, 39, 'g'), (5, 40, 'h')]
for x, y, t in MOUSSE: g[y][x] = t
save_grid([''.join(r) for r in g], 'colonne_brisee.txt')
