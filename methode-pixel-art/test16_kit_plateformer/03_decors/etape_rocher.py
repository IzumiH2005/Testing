"""Rocher composé 32×24 (B6-B) : trois blocs de tailles différentes (grand, moyen, petit,
A4b), jamais alignés, qui se calent l'un contre l'autre. Lumière haut gauche : dessus e,
face avant c (bord gauche d), côté droit b, bas a. Chaque bloc est dessiné à la main ; on les
pose du fond vers l'avant. Là où le contour d'un bloc de devant tombe sur un bloc de
derrière, il devient l'ombre de contact a (pas de trait intérieur sur la pierre, règle 40)."""
import sys; sys.path.insert(0, '../../outils'); from pxlib import save_grid
W, H = 32, 24

GRAND = ["....OOOOOOOOO.....",
         "..OOeeeeeeeeeOOO..",
         ".OeeeeeeeeeeeeddO.",
         "OdeeeeeeeeeeedddbO",
         "OcddddddddddddcbbO",
         "OdcccccccccccccbbO",
         "OdccccccccccccbbbO",
         "OdccccccccccccbbbO",
         "OdccccccccccccbbbO",
         "OdccccccccccccbbbO",
         "OdccccccccccccbbbO",
         "OdccccccccccccbbbO",
         "OdccccccccccccbbbO",
         "ObccccccccccccbbbO",
         "ObcccccccccccbbbaO",
         "ObbcccccccccbbbaaO",
         "OabbbbbbbbbbbbaaaO",
         ".OOOOOOOOOOOOOOOO."]
MOYEN = ["...OOOOOOOOO...",
         ".OOeeeeeeeeeOO.",
         "OeeeeeeeeeeeddO",
         "OddddddddddcbbO",
         "OdcccccccccbbbO",
         "OdcccccccccbbbO",
         "OdcccccccccbbbO",
         "OdcccccccccbbbO",
         "ObcccccccccbbbO",
         "ObcccccccbbbbaO",
         "OabbbbbbbbbbaaO",
         ".OOOOOOOOOOOOO."]
PETIT = ["..OOOOOO..",
         ".OeeeeeddO",
         "OdeeeeedbO",
         "OcdddddcbO",
         "OdccccbbbO",
         "ObbbbbbaaO",
         ".OOOOOOOO."]
BLOCS = [(GRAND, 2, 6), (MOYEN, 14, 12), (PETIT, 0, 17)]   # du fond vers l'avant
for b, _, _ in BLOCS: assert len({len(r) for r in b}) == 1

def poser(blocs):
    g = [['.'] * W for _ in range(H)]
    for b, x0, y0 in blocs:
        for j, r in enumerate(b):
            for i, ch in enumerate(r):
                if ch == '.': continue
                x, y = x0 + i, y0 + j
                if ch == 'O' and g[y][x] not in '.O':
                    # contour sur un bloc de derrière : ombre de contact, sauf le bas
                    ch = 'a'
                g[y][x] = ch
    return g
def ecrire(g, n): save_grid([''.join(r) for r in g], n + '.txt')

# Étape 1 : formes de base (boîtes droites, 3 tons : dessus, face, côté)
def boite(w, h, haut, cote):
    rows = []
    for j in range(h):
        r = ''
        for i in range(w):
            if i in (0, w - 1) or j in (0, h - 1): r += 'O'
            elif j <= haut: r += 'e'
            elif i >= w - 1 - cote: r += 'b'
            else: r += 'c'
        rows.append(r)
    return rows
ecrire(poser([(boite(18, 18, 3, 3), 2, 6), (boite(15, 12, 2, 3), 14, 12),
              (boite(10, 7, 2, 2), 0, 17)]), 'rocher_e1_formes')

# Étape 2 : déformer (coins arrondis, arêtes irrégulières), mêmes trois faces
g = poser(BLOCS); ecrire(g, 'rocher_e2_deformer')

# Étape 3 : sous-plans (cassures et strates), un ton par orientation
SOUS_PLANS = {}  # (x, y): ton, choisis à la main
# grand bloc : facette haute gauche tournée vers la lumière (d), en triangle ; elle se sépare
# de la face par la valeur seule (règle 40). Essai 3a (cassure en « / » et tirets flottants)
# rejeté : il se lisait comme un symbole.
for y, x1 in ((11, 9), (12, 8), (13, 7), (14, 6), (15, 5)):
    for x in range(4, x1 + 1): SOUS_PLANS[(x, y)] = 'd'
for x in range(3, 9): SOUS_PLANS[(x, 17)] = 'b'          # strate attachée au bord gauche
for x in (12, 13, 14): SOUS_PLANS[(x, 9)] = 'd'          # dessus : facette qui descend
# moyen : facette éclairée haute gauche, strate qui part du côté droit
for y, x1 in ((16, 20), (17, 18)):
    for x in range(16, x1 + 1): SOUS_PLANS[(x, y)] = 'd'
for x in range(21, 25): SOUS_PLANS[(x, 19)] = 'b'
SOUS_PLANS[(3, 19)] = 'd'; SOUS_PLANS[(4, 19)] = 'd'      # petit : éclat sur l'arête
for (x, y), t in SOUS_PLANS.items(): g[y][x] = t
ecrire(g, 'rocher_e3_sousplans')

# Étape 4 : polir : fissure (trait b + lèvre d, règle 41), trous groupés de tailles
# différentes sur les faces sombres, mousse sur le dessus éclairé (langage du lieu)
POLIR = {
    # fissure qui part de l'arête haute du moyen et passe sur la face (trait b, lèvre d)
    (24, 15): 'b', (24, 16): 'b', (25, 17): 'b', (25, 18): 'b',
    (25, 16): 'd', (26, 17): 'c',
    # trous : un de 2 px et un de 1 px, sur les faces moyennes ; sombre en haut à gauche,
    # lèvre claire en bas à droite
    (18, 21): 'a', (19, 21): 'a', (19, 22): 'd', (20, 22): 'd', (11, 20): 'a', (12, 21): 'd',
    # croûte de mousse sur le dessus du grand bloc (langage du lieu), contour au-dessus
    (7, 6): 'i', (8, 6): 'j', (9, 6): 'j', (10, 6): 'i', (11, 6): 'h',
    (7, 5): 'O', (8, 5): 'O', (9, 5): 'O', (10, 5): 'O', (11, 5): 'O',
    (6, 7): 'h', (7, 7): 'h', (8, 7): 'i', (9, 7): 'i', (10, 7): 'h', (11, 7): 'g',
    (6, 8): 'g', (7, 8): 'h', (8, 8): 'g', (7, 9): 'g',
    # mousse sur le petit
    (2, 18): 'h', (3, 18): 'i', (4, 18): 'j', (5, 18): 'i', (6, 18): 'h',
}
for (x, y), t in POLIR.items(): g[y][x] = t
ecrire(g, 'rocher_e4_polir'); ecrire(g, 'rocher_compose')
