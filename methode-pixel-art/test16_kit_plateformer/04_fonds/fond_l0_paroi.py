"""L0 — paroi du fond (fixe, 320×180), version 2. F3 : pas de contour, valeurs basses (base 4).
La seule zone claire est la faille en haut à gauche, source de lumière du jeu (règle 23).
La v1 est gardée (paroi_v1_rejet.txt) : faille en œuf flou, masses en autocollants.
Étapes :
 e1 masses : polygones irréguliers choisis à la main (grand / moyen / petit, A4b). Liseré +1 sur
    le bord tourné vers la faille, seulement à moins de 110 px d'elle (la lumière décroît).
 e2 strates : essayées puis retirées (lisaient comme de la pluie).
 e3 faille : fente dentelée décidée rang par rang, cœur 9, bord 8 ; halo serré (8→7→6→5),
    transitions en Bayer 4×4 sur 3 px, et le halo ne mord que la paroi, pas les masses en retrait.
 e4 rayons : deux bandes en Bayer, qui visent le point focal (le grand cristal, x≈262 y≈104).
 e5 fissures : sombre −1 + lèvre +1 côté lumière (règle 41 transposée au fond)."""
import sys, math; sys.path.insert(0, '../../outils'); from pxlib import save_grid
W, H = 320, 180
B4 = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]
def bayer(x, y, f): return B4[y % 4][x % 4] < f * 16
def dedans(px, py, poly):
    c = False
    for i in range(len(poly)):
        x1, y1 = poly[i]; x2, y2 = poly[(i + 1) % len(poly)]
        if (y1 > py) != (y2 > py) and px < x1 + (py - y1) * (x2 - x1) / (y2 - y1): c = not c
    return c
SRC = (48, 14)  # centre de la faille
def save(n, g): save_grid([''.join(r) for r in g], n)

# ---- e1 masses -------------------------------------------------------------------------
MASSES = [  # (ton, polygone) ; tons : 3 = en retrait (ombre), 5 = avancée vers la lumière
 ('3', [(0, 58), (9, 54), (15, 57), (24, 55), (33, 61), (38, 60), (47, 70), (52, 82), (50, 90),
        (56, 101), (54, 112), (47, 121), (45, 133), (37, 146), (30, 151), (24, 165), (12, 180), (0, 180)]),
 ('3', [(156, 0), (320, 0), (320, 34), (309, 38), (298, 37), (288, 44), (276, 46), (266, 43),
        (252, 47), (240, 45), (229, 40), (214, 39), (204, 33), (193, 30), (184, 24), (176, 23), (166, 14)]),
 ('5', [(104, 0), (150, 0), (147, 9), (152, 18), (149, 27), (151, 36), (148, 45), (151, 47), (156, 55),
        (153, 63), (155, 70), (148, 79), (138, 82), (127, 87), (117, 85), (107, 79), (101, 71), (95, 60), (99, 48), (103, 38), (101, 27), (106, 16), (103, 8)]),
 ('3', [(232, 124), (241, 117), (252, 116), (260, 109), (271, 106), (283, 108), (292, 104),
        (304, 107), (313, 113), (320, 112), (320, 180), (221, 180), (224, 160), (230, 148), (228, 136)]),
 ('5', [(74, 4), (82, 2), (90, 0), (100, 0), (106, 8), (104, 17), (96, 23), (88, 27), (80, 24), (75, 16)]),
]
g = [['4'] * W for _ in range(H)]
masque = [[None] * W for _ in range(H)]
for i, (ton, poly) in enumerate(MASSES):
    for y in range(H):
        for x in range(W):
            if dedans(x + .5, y + .5, poly): g[y][x] = ton; masque[y][x] = i
    for y in range(H):
        for x in range(W):
            if masque[y][x] != i: continue
            haut = y == 0 or masque[y - 1][x] != i; gauche = x == 0 or masque[y][x - 1] != i
            bas = y == H - 1 or masque[y + 1][x] != i; droite = x == W - 1 or masque[y][x + 1] != i
            d = math.hypot(x - SRC[0], y - SRC[1])
            if (haut or gauche) and d < 110 and y > 0 and x > 0:
                g[y][x] = str(int(ton) + 1)
            elif (bas or droite) and ton == '5':
                g[y][x] = '4'          # face d'ombre : un ton plus bas, sans contour
for i, (ton, poly) in enumerate(MASSES):
    if ton != '5': continue
    xs = [p[0] for p in poly]; ys = [p[1] for p in poly]
    for y in range(H):
        for x in range(W):
            if masque[y][x] != i or g[y][x] != '5': continue
            # position le long de la direction de la lumière (haut-gauche -> bas-droite), 0..1
            u = ((x - min(xs)) / (max(xs) - min(xs)) + (y - min(ys)) / (max(ys) - min(ys))) / 2
            if u > 0.62 or (u > 0.5 and bayer(x, y, (u - 0.5) / 0.12)): g[y][x] = '4'
save('paroi_e1_masses.txt', g)

# ---- e2 strates : essai rejeté (des tirets fins lisaient comme de la pluie). Au loin, moins de
# détail (F3) : la paroi garde ses grandes masses et quelques fissures seulement.

# ---- e3 faille -----------------------------------------------------------------------------
# Rang par rang : (début, fin) de la fente. Elle s'ouvre au plafond, se resserre, fait deux
# décrochements (y 9 et y 22) puis finit en fil.
FENTE = {0: (35, 52), 1: (36, 51), 2: (37, 50), 3: (38, 49), 4: (39, 49), 5: (40, 48), 6: (41, 48),
 7: (41, 47), 8: (42, 47), 9: (44, 49), 10: (45, 49), 11: (45, 50), 12: (46, 50), 13: (46, 50),
 14: (47, 50), 15: (47, 51), 16: (48, 51), 17: (48, 51), 18: (49, 51), 19: (49, 52), 20: (50, 52),
 21: (50, 52), 22: (52, 54), 23: (53, 55), 24: (53, 55), 25: (54, 55), 26: (54, 56), 27: (55, 56),
 28: (55, 56), 29: (56, 57), 30: (56, 57), 31: (57, 58), 32: (58, 59)}
BRANCHE = [(41, 10), (40, 11), (39, 12), (38, 13), (38, 14), (37, 15)]   # petite fêlure qui part à gauche
ANNEAUX = [(1, '8'), (5, '7'), (11, '6'), (20, '5')]
pts = [(x, y) for y, (a, b) in FENTE.items() for x in range(a, b)] + BRANCHE
def dist(x, y): return min(math.hypot(x - px, (y - py) * 0.9) for px, py in pts)
for y in range(0, 60):
    for x in range(10, 100):
        d = dist(x, y)
        if d > 26: continue
        ton = None
        for r0, t0 in ANNEAUX:
            if d <= r0 + 0.5: ton = t0; break
            if d <= r0 + 3.5 and bayer(x, y, (r0 + 3.5 - d) / 6): ton = t0; break
        if ton is None and d < 26 and bayer(x, y, (26 - d) / 12): ton = '5'
        if ton and (masque[y][x] is None or MASSES[masque[y][x]][0] == '5') and g[y][x] < ton:
            g[y][x] = ton
for x, y in pts:
    a, b = FENTE.get(y, (x, x + 1))
    g[y][x] = '9' if a < x < b - 1 or b - a <= 2 else '8'
save('paroi_e3_faille.txt', g)

# ---- e4 rayons -----------------------------------------------------------------------------
RAYONS = [((50, 22), (262, 104), 8, 0.5), ((46, 26), (186, 150), 4, 0.35)]
for (x0, y0), (x1, y1), hw, fmax in RAYONS:
    L = math.hypot(x1 - x0, y1 - y0); ux, uy = (x1 - x0) / L, (y1 - y0) / L
    for y in range(H):
        for x in range(W):
            t = (x - x0) * ux + (y - y0) * uy; n = abs(-(x - x0) * uy + (y - y0) * ux)
            if 24 < t < L and n < hw * (0.7 + 0.7 * t / L):
                f = fmax * (1 - t / L) * (1 if n < hw * 0.4 else 0.5)
                if g[y][x] in '345' and bayer(x, y, f): g[y][x] = str(int(g[y][x]) + 1)
save('paroi_e4_rayons.txt', g)

# ---- e5 fissures ---------------------------------------------------------------------------
FISSURES = [
 [(150, 58), (151, 59), (151, 60), (152, 61), (154, 62), (155, 63), (155, 64), (156, 65)],
 [(16, 96), (17, 97), (17, 98), (18, 99), (20, 100), (21, 101), (21, 102), (22, 103)],
 [(284, 58), (285, 59), (286, 60), (286, 61), (287, 62), (289, 63), (290, 64)],
 [(122, 112), (123, 113), (125, 114), (126, 115), (126, 116), (127, 117), (129, 118)],
]
for f in FISSURES:
    for x, y in f:
        if g[y][x].isdigit(): g[y][x] = str(max(1, int(g[y][x]) - 1))
    for x, y in f:
        if (x - 1, y) not in f and g[y][x - 1].isdigit() and (x - 1, y - 1) not in f:
            g[y][x - 1] = str(min(7, int(g[y][x - 1]) + 1))
save('fond_l0_paroi.txt', g)
