"""Étape 1 : découper la base en pièces (calques) pour pouvoir les bouger séparément.
Ordre d'arrière en avant : cape, jambe loin, main loin, buste+tête, jambe proche, main proche.
Les trous laissés sous une pièce retirée sont rebouchés avec la couleur de ce qu'il y a dessous."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))
from px import lire, ecrire, image

B = lire('../00_base/base_brute.txt')
H, W = len(B), len(B[0])
vide = lambda: [['.'] * W for _ in range(H)]
cape, buste, mp, ml, jp, jl = vide(), vide(), vide(), vide(), vide(), vide()

for y in range(H):
    for x in range(W):
        c = B[y][x]
        if c == '.': continue
        if y <= 37:
            # cape : orange et rouge sombre à l'arrière du corps (sous le col)
            if y >= 18 and c in 'oD' and x <= 6 or y >= 20 and c == 'C' and x == 4:
                cape[y][x] = c if c != 'C' else 'D'; continue
            # main proche : peau sur le flanc arrière
            if 28 <= y <= 35 and 5 <= x <= 10 and c in 'sSB':
                mp[y][x] = c
                buste[y][x] = 'F' if x == 5 else 'E'; continue
            # main loin : peau qui dépasse devant
            if 30 <= y <= 35 and x >= 16 and c in 'sSK':
                ml[y][x] = c; continue
            buste[y][x] = c
        else:
            if c in 'oD':
                cape[y][x] = c
            elif (x <= 10 and c in 'sSKC' and not (x == 10 and c == 'S' and y > 38)) or (y >= 48 and x == 11 and c in 'KC'):
                jp[y][x] = c
            else:
                jl[y][x] = c

for nom, g in [('cape', cape), ('buste', buste), ('main_proche', mp), ('main_loin', ml),
               ('jambe_proche', jp), ('jambe_loin', jl)]:
    ecrire(nom + '.txt', g, 'Pièce découpée dans la base (cadre 20x50, mêmes coordonnées).')

# contrôle : pièces recomposées == base ?
ordre = [cape, jl, ml, buste, jp, mp]
R = vide()
for g in ordre:
    for y in range(H):
        for x in range(W):
            if g[y][x] != '.': R[y][x] = g[y][x]
diff = [(x, y) for y in range(H) for x in range(W) if R[y][x] != B[y][x]]
print('pixels différents de la base :', len(diff), diff[:20])
from PIL import Image
planche = Image.new('RGBA', (7 * 22 * 6, 52 * 6), (255, 255, 255, 255))
for i, g in enumerate([B, cape, jl, ml, buste, jp, mp]):
    planche.paste(image(g, None, 6), (i * 22 * 6, 6), image(g, None, 6))
planche.save('pieces_x6.png')
