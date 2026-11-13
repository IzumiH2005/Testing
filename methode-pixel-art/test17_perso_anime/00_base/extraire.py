"""Étape 0 : relever la grille de l'image Ludo (pixels de 12 px, 64x64) et la ramener à la palette."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))
from PIL import Image
from px import PAL, hexrgb, ecrire, image

im = Image.open('ludo_source.webp').convert('RGBA'); p = im.load()
cible = {k: hexrgb(v) for k, v in PAL.items()}
g = []
for y in range(64):
    r = []
    for x in range(64):
        c = p[x*12+6, y*12+6]
        if c[3] < 128: r.append('.'); continue
        # gris parasites (bruit de compression) -> vide
        if max(c[:3]) - min(c[:3]) < 30 and min(c[:3]) > 60: r.append('.'); continue
        r.append(min(cible, key=lambda k: sum((cible[k][i]-c[i])**2 for i in range(3))))
    g.append(r)
# recadrage sur le personnage
ys = [y for y in range(64) if any(ch != '.' for ch in g[y])]
xs = [x for x in range(64) if any(g[y][x] != '.' for y in range(64))]
g = [r[min(xs):max(xs)+1] for r in g[min(ys):max(ys)+1]]
ecrire('base_brute.txt', g, 'Relevé brut de l\'image Ludo, sans retouche.')
image(g, '#ffffff', 10).save('base_brute_x10.png')
print(len(g[0]), 'x', len(g))
