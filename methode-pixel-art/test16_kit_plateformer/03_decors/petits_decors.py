"""Racines pendantes 16×32 et touffes de mousse 16×8 ×3. Chemins et pixels choisis à la main.
Racine : 2 px de large, bord gauche éclairé (h), droit sombre (g), contour O côté ombre."""
import sys; sys.path.insert(0, '../../outils'); from pxlib import save_grid
g = [['.'] * 16 for _ in range(32)]
BRINS = [  # (x de départ par rang, en commençant au rang 0) ; dernier rang = pointe d'1 px
    [5,5,5,6,6,6,6,5,5,5,4,4,4,4,5,5,5,6,6,6,6,6,5,5,5,5,4,4,4,4],
    [10,10,11,11,11,12,12,12,12,11,11,11,11,10,10,10,10,11,11,11],
    [2,2,2,1,1,1,1,2,2,2,2,2,2]]
for chemin in BRINS:
    n = len(chemin)
    for y, x in enumerate(chemin):
        pointe = y >= n - 3
        g[y][x] = 'h'
        if not pointe and chemin is not BRINS[2]: g[y][x + 1] = 'g'
        bord = x + (1 if (pointe or chemin is BRINS[2]) else 2)
        if g[y][bord] == '.': g[y][bord] = 'O'
    g[n][chemin[-1]] = 'O'   # bout
FEUILLES = [(7, 9, 'i'), (8, 9, 'h'), (8, 10, 'O'), (3, 15, 'i'), (2, 16, 'h'), (3, 16, 'O'),
            (8, 21, 'i'), (9, 21, 'j'), (9, 22, 'O'), (13, 6, 'i'), (14, 6, 'h'), (14, 7, 'O'),
            (9, 14, 'j'), (8, 14, 'i'), (8, 15, 'O'), (0, 6, 'i'), (0, 7, 'O')]
for x, y, t in FEUILLES: g[y][x] = t
save_grid([''.join(r) for r in g], 'racines.txt')

TOUFFES = {
 'touffe1': ["................",
             "................",
             "................",
             "......O.O.......",
             "....OOjOjOO.O...",
             "...OjiiiiijOjO..",
             "..OihhihhhhihhO.",
             "..Ogghggggghggg."],
 'touffe2': ["................",
             "........O.......",
             ".......OjO......",
             "...O...OiO..O...",
             "..OjO.OjhiOOjO..",
             "..OihOOihhjihO..",
             ".OihhhhhhghhhgO.",
             ".Oggggggggggggg."],
 'touffe3': ["................",
             "................",
             "................",
             "................",
             "...........O....",
             ".....OOO..OjO...",
             "....OjjiOOihO...",
             "...Oihhhhhhhg...."[:16]],
}
for n, rows in TOUFFES.items():
    assert all(len(r) == 16 for r in rows), n
    save_grid(rows, n + '.txt')
