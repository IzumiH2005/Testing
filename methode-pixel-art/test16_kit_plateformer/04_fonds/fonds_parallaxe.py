"""Couches de parallaxe (F3) : chacune fait 320 px de large et boucle (le bord droit rejoint le
bord gauche : toutes les formes sont posées modulo 320). '.' = transparent.
 L1 piliers naturels ×0,25 : base 3, liseré gauche 5 (vers la faille), face d'ombre 2.
 L2 ruines ×0,5         : pierre taillée, un ton par face : face 2, dessus 4, flanc gauche 3,
                           joints 1. Plus proche = plus sombre (on est à contre-jour de la faille).
 FG premier plan ×1,25  : ton 1 (le plus sombre de la palette, sous O), liseré a ; stalactites en haut (≤ 30 px), buttes en bas (≤ 12 px).
Profils de largeur donnés par images clés à la main ; la rugosité des bords vient d'une suite
de décalages choisie à la main (RUG), lue avec un décalage propre à chaque forme."""
import sys, math; sys.path.insert(0, '../../outils'); from pxlib import save_grid
W, H = 320, 180
B4 = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]
def bayer(x, y, f): return B4[y % 4][x % 4] < f * 16
RUG = [0, 0, 1, 1, 0, 0, -1, 0, 1, 0, 0, -1, -1, 0, 0, 1, 0, 0, 0, -1, 0, 1, 1, 0]
def interp(cles, y):
    for (y0, a), (y1, b) in zip(cles, cles[1:]):
        if y0 <= y <= y1: return a + (b - a) * (y - y0) / max(1, y1 - y0)
    return None
def vide(): return [['.'] * W for _ in range(H)]
def put(g, x, y, c):
    if 0 <= y < H: g[y][x % W] = c
def save(n, g): save_grid([''.join(r) for r in g], n)

# ---------------------------------------------------------------- L1 piliers -------------
# (centre x par images clés, demi-largeur par images clés, phase de rugosité)
PILIERS = [
 ([(0, 128), (90, 134), (180, 126)], [(0, 17), (40, 10), (95, 6), (140, 11), (180, 19)], 0),  # colonne complète (laisse la faille dégagée)
 ([(0, 190), (70, 194)], [(0, 13), (30, 8), (60, 3), (70, 1)], 5),                             # stalactite
 ([(108, 199), (180, 196)], [(108, 1), (120, 4), (150, 11), (180, 16)], 9),                     # stalagmite en face
 ([(0, 276), (60, 280), (120, 274), (180, 278)], [(0, 11), (50, 6), (110, 5), (180, 13)], 14),  # colonne fine, coudée
 ([(124, 134), (180, 131)], [(124, 1), (140, 4), (180, 9)], 3),                                # petite stalagmite
]
L1 = vide()
for cx, hw, ph in PILIERS:
    for y in range(H):
        c = interp(cx, y); w = interp(hw, y)
        if c is None or w is None: continue
        r = RUG[(y // 2 + ph) % len(RUG)]
        x0 = round(c - w) + r; x1 = round(c + w) - RUG[(y // 2 + ph + 7) % len(RUG)]
        for x in range(x0, x1 + 1):
            put(L1, x, y, '3')
        if x1 - x0 >= 2:
            put(L1, x0, y, '5')
            if bayer(x0 + 1, y, 0.5): put(L1, x0 + 1, y, '4')
            put(L1, x1, y, '2')
            if x1 - x0 >= 8 and bayer(x1 - 1, y, 0.5): put(L1, x1 - 1, y, '2')
# sol lointain : butte continue en bas (cachée en grande partie par L2)
for x in range(W):
    top = 160 + round(5 * math.sin(x * 2 * math.pi / 160)) + RUG[(x // 3) % len(RUG)]
    for y in range(top, H): put(L1, x, y, '3')
    put(L1, x, top, '4')
save('fond_l1_piliers.txt', L1)

# ---------------------------------------------------------------- L2 ruines --------------
L2 = vide()
def rect(g, x0, y0, x1, y1, c):
    for y in range(y0, y1):
        for x in range(x0, x1): put(g, x, y, c)
def appareil(g, x0, y0, x1, y1, haut=6, long=12, dec=0):
    """Joints d'un mur de briques : un rang tous les `haut` px, briques de `long`, décalées d'un
    rang sur l'autre. Joints au ton 1, arête éclairée 3 juste dessous."""
    for y in range(y0, y1):
        for x in range(x0, x1):
            if L2[y][x % W] != '2': continue
            ry = (y - y0) % haut; rang = (y - y0) // haut
            jx = (x - x0 + dec + (long // 2) * (rang % 2)) % long
            if ry == 0 or jx == 0: put(g, x, y, '1')
            elif ry == 1 and jx > 1 and (x + rang) % 5: put(g, x, y, '3')
# arcade : deux piles et un arc brisé ; à l'écran de référence elle encadre le personnage
rect(L2, 10, 96, 26, 180, '2'); rect(L2, 90, 112, 106, 180, '2')
CASSE_P = [3, 0, 1, 4, 6, 5, 2, 0, 1, 3, 5, 7, 4, 2, 1, 0]   # sommet cassé de la pile droite
for i, x in enumerate(range(90, 106)):
    for y in range(112, 112 + CASSE_P[i]): put(L2, x, y, '.')
for y in range(50, 101):
    for x in range(10, 107):
        d = math.hypot(x - 58, y - 100)
        ang = math.degrees(math.atan2(100 - y, x - 58))
        if 32 <= d < 48 and y <= 100 and ang > 58:            # les voussoirs de droite sont tombés
            put(L2, x, y, '2')
appareil(L2, 10, 52, 107, 180, 6, 12, 3)
# voussoirs : joints rayonnants au lieu des rangs horizontaux, dans l'arc
for y in range(52, 101):
    for x in range(10, 107):
        if L2[y][x] in '13' and 32 <= math.hypot(x - 58, y - 100) < 48:
            a = math.degrees(math.atan2(100 - y, x - 58))
            put(L2, x, y, '1' if round(a) % 15 == 0 else '2')
# colonne isolée, fût cannelé, chapiteau, sommet cassé
CASSE = [0, 2, 3, 1, 4, 6, 5, 3, 2, 4, 1, 0]          # profondeur de cassure par colonne de pixel
rect(L2, 196, 120, 210, 180, '2'); rect(L2, 193, 114, 213, 120, '2')   # assez basse pour ne pas toucher la dalle (tangente)
for i, x in enumerate(range(193, 213)):
    for y in range(114, 114 + CASSE[i % 12]): put(L2, x, y, '.')
for y in range(122, 180):                             # une seule cannelure, en tambours de 9 px
    if y % 9: put(L2, 203, y, '1')
    else:
        for x in range(196, 210): put(L2, x, y, '1')
# mur bas qui passe la couture (x 236 → 320+30 = 30 : il boucle)
PROFIL = [(236, 140), (250, 134), (262, 136), (276, 128), (290, 131), (306, 138), (322, 142), (340, 150), (352, 156)]
for x in range(236, 352):
    top = round(interp([(a, b) for a, b in PROFIL], x))
    rect(L2, x, top, x + 1, 180, '2')
appareil(L2, 236, 128, 352, 180, 6, 14, 0)
# un tons par face : dessus 4, flanc gauche 3 (premier pixel opaque en partant du haut / de la gauche)
for x in range(W):
    for y in range(H):
        if L2[y][x] != '.':
            if y == 0 or L2[y - 1][x] == '.':
                put(L2, x, y, '4')
                if y + 1 < H and L2[y + 1][x] == '2': put(L2, x, y + 1, '3')
            elif L2[y][x - 1] == '.': put(L2, x, y, '3')
# bloc tombé au pied de l'arcade (rectangle légèrement basculé, 1 sur 6)
for x in range(140, 168):
    y0 = 166 - (x - 140) // 6
    for y in range(y0, 180): put(L2, x, y, '2')
    put(L2, x, y0, '4')
put(L2, 140, 167, '3')
save('fond_l2_ruines.txt', L2)

# ---------------------------------------------------------------- premier plan ------------
FG = vide()
STALAC = [(22, 11, 28), (58, 5, 14), (150, 8, 22), (246, 14, 30), (284, 4, 10)]   # centre, demi-largeur, longueur
for cx, hw, L in STALAC:
    for y in range(L):
        w = hw * (1 - y / L) ** 0.8
        r = RUG[(y + cx) % len(RUG)]
        x0, x1 = round(cx - w) + r, round(cx + w)
        for x in range(x0, x1 + 1): put(FG, x, y, '1')
        if x1 > x0: put(FG, x0, y, 'a')
BUTTES = [(0, 52, 12), (118, 40, 8), (226, 74, 11)]   # début, largeur, hauteur
for x0, w, h in BUTTES:
    for k in range(w):
        top = H - round(h * math.sin(math.pi * k / w) ** 0.6) + (RUG[k % len(RUG)] if 3 < k < w - 3 else 0)
        for y in range(top, H): put(FG, x0 + k, y, '1')
        put(FG, x0 + k, top, 'a')
save('fond_fg.txt', FG)
