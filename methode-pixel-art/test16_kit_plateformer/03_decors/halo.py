"""Halo du grand cristal (B6-D étape 9), calque séparé 48×48 posé sous le cristal (décalage
-8,-8). Couleur de la lumière émise (t, teal sombre) : un ton à peine plus clair que les fonds
4-5. Disque plein au centre, puis anneau tramé Bayer 4×4 à 50 % (A7)."""
import sys; sys.path.insert(0, '../../outils'); from pxlib import save_grid
B = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]
cx, cy = 23.5, 22.0      # centre : milieu du grand prisme, un peu au-dessus du pied
rows = []
for y in range(48):
    r = ''
    for x in range(48):
        d = (((x - cx) / 1.0) ** 2 + ((y - cy) / 0.85) ** 2) ** 0.5   # ellipse plus large que haute
        seuil = B[y % 4][x % 4]
        if d < 12: r += 't'
        elif d < 16: r += 't' if seuil < 8 else '.'   # anneau 50 % ; l'anneau 25 % (r<21)
        # faisait du bruit sur fond sombre : retiré
        else: r += '.'
    rows.append(r)
save_grid(rows, 'cristal_grand_halo.txt')
