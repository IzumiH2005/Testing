"""Personnage de test, v2 : contour sélectif (« sel-out »). Les pixels de contour y tournés vers
la faille (vide au-dessus ou à gauche) prennent la couleur éclairée de la matière qu'ils bordent :
c'est un liseré de lumière chaude, cohérent avec la règle 23, et il détache la silhouette des
fonds sombres. Le contour du côté ombre (bas, droite) reste y."""
import sys; sys.path.insert(0, '../../outils'); from pxlib import load_grid, save_grid
g = [list(r) for r in load_grid('perso_test_v1_rejet.txt')]
H, W = len(g), len(g[0])
LIT = {'N': 'S', 'n': 'N', 'k': 'l', 'l': 'l', 's': 's', 'S': 's'}
vide = lambda x, y: not (0 <= x < W and 0 <= y < H) or g[y][x] == '.'
out = [r[:] for r in g]
for y in range(H):
    for x in range(W):
        if g[y][x] != 'y' or not (vide(x, y - 1) or vide(x - 1, y)): continue
        # matière bordée : premier pixel non-contour vers la droite ou le bas
        for dx, dy in ((1, 0), (0, 1), (1, 1)):
            c = g[y + dy][x + dx] if not vide(x + dx, y + dy) else 'y'
            if c in LIT: out[y][x] = LIT[c]; break
save_grid([''.join(r) for r in out], 'perso_test.txt')
