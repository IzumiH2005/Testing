"""Épines de cristal magenta 16×16 ×2 (danger : la seule couleur rose-rouge du lieu). Triangles
serrés pointus vers le haut (A4b). Facette gauche éclairée q, droite p, contour r, éclat X à la
pointe. Sommets choisis à la main ; la largeur croît d'1 px de chaque côté tous les 3 rangs."""
import sys; sys.path.insert(0, '../../outils'); from pxlib import save_grid
def epines(sommets):
    g = [['.'] * 16 for _ in range(16)]
    for sx, sy in sommets:          # dans l'ordre du fond vers l'avant
        g[sy - 1][sx] = 'r'
        for y in range(sy, 16):
            h = (y - sy) // 3
            for x in range(sx - h - 1, sx + h + 2):
                if not 0 <= x < 16: continue
                if x in (sx - h - 1, sx + h + 1): g[y][x] = 'r'
                else: g[y][x] = 'q' if x <= sx else 'p'
        g[sy][sx] = 'X'
        if sy + 1 < 16: g[sy + 1][sx] = 'X' if sy < 6 else 'q'
    for x in range(16):             # pied : rang du bas sombre (ancré dans le sol)
        if g[15][x] != '.': g[15][x] = 'r'
        if g[14][x] == 'p': g[14][x] = 'r'
    return g
for n, s in (('epines1', [(6, 3), (13, 6), (2, 7), (10, 9)]),
             ('epines2', [(3, 5), (11, 4), (7, 8), (14, 10)])):
    save_grid([''.join(r) for r in epines(s)], n + '.txt')
