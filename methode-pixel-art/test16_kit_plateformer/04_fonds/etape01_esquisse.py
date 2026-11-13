"""F5 « taille d'abord » : esquisse de la scène en 3 tons sur un canevas réduit 80×45 (¼ de
l'écran 320×180). Elle fixe les masses avant tout pixel : premier plan sombre (1), plan
jouable moyen (c), fond (3) avec la tache claire de la faille en haut à gauche (8). Point
focal : le grand cristal sur la corniche au tiers droit (v). Le rayon mène de la faille vers
lui. Chaque rang est décidé à la main (RLE)."""
import sys; sys.path.insert(0, '../../outils'); from pxlib import save_grid
rows = []
for y in range(45):
    r = ['3'] * 80
    # faille : colonne claire x10-16 en haut, qui s'élargit en éventail (rayon) vers le bas droite
    if y < 14:
        for x in range(10 + y // 5, 15 + y // 4): r[x] = '8'
    for x in range(80):           # rayon : bande en biais, une seule, qui pointe vers la corniche
        if 0 < (x - 14) - 1.9 * (y - 6) < 9 and 6 < y < 30 and x < 66: r[x] = '5' if r[x] == '3' else r[x]
    rows.append(r)
def bloc(x0, y0, x1, y1, t):
    for y in range(y0, y1):
        for x in range(x0, x1): rows[y][x] = t
bloc(40, 0, 80, 4, 'c'); bloc(48, 4, 80, 6, 'c'); bloc(60, 6, 80, 9, 'c'); bloc(74, 9, 80, 12, 'c')
bloc(0, 32, 24, 45, 'c'); bloc(0, 36, 30, 45, 'c'); bloc(56, 28, 80, 45, 'c')
bloc(30, 42, 56, 45, 'c'); bloc(36, 40, 44, 42, 'c')            # fosse et son petit pilier
bloc(28, 28, 46, 29, 'c')                                        # dalles traversables
bloc(31, 40, 36, 42, 'q'); bloc(45, 40, 54, 42, 'q')             # épines (danger)
bloc(62, 20, 70, 28, 'v')                                        # grand cristal = point focal
bloc(10, 26, 12, 32, 'k')                                        # personnage, tiers gauche
bloc(0, 0, 8, 3, 'O'); bloc(0, 42, 10, 45, 'O'); bloc(68, 43, 80, 45, 'O')  # premier plan
save_grid([''.join(r) for r in rows], 'etape01_esquisse.txt')
