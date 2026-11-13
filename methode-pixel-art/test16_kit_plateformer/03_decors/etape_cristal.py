"""Grand cristal 32×32 en 9 étapes (B6-D). Une idée par étape ; chaque étape écrit sa grille.
Lumière : haut gauche (règle 23). Les prismes viennent de cristal_prismes.py (nombres choisis
à la main), le rocher du pied est dessiné à la main en RLE."""
import sys; sys.path.insert(0, '../../outils')
from pxlib import rle, save_grid
from cristal_prismes import P1, P2, P3, P4, ORDRE, W, H

# ---- Rocher du pied, à la main (deux bosses, la gauche plus haute ; lumière haut gauche)
ROCHER = {23: '..OOOOO.........................',
          24: '.OeeeedO...................OOOO.',
          25: 'OeeeddddOOOOOO.........OOOOeeedO',
          26: 'OeddddccbeeeeeOOOOOOOOOeeeeedddO',
          27: 'OdddccccbdeeeeeeeeeeeedcddddccbO',
          28: 'OcccccbbbcddddddddddddcbccccbbaO',
          29: 'ObcccbbbbcccccccccccbbbcccbbbaaO',
          30: '.ObbbaaaabbbbbbbbbbbbaaaabbbaaO.',
          31: '..OOOOOOOOOOOOOOOOOOOOOOOOOOOO..'}
for y, s in ROCHER.items(): assert len(s) == 32, (y, len(s))

def vide(): return [['.'] * W for _ in range(H)]
def poser_rocher(g, dessus=True):
    for y, s in ROCHER.items():
        for x, ch in enumerate(s):
            if ch != '.': g[y][x] = ch

def composite():
    """Étiquettes visibles (occlusion du fond vers l'avant) : {(x,y): étiquette}."""
    vis = {}
    for P in ORDRE:
        vis.update(P)
    for y, s in ROCHER.items():
        for x, ch in enumerate(s):
            if ch != '.': vis.pop((x, y), None)
    return vis

def prisme_de(et): return et[0] if et != 'O' else None

def ecrire(g, nom):
    save_grid([''.join(r) for r in g], nom + '.txt')

# ---- Étape 1 : esquisse, 4 prismes en fil de fer qui se chevauchent
g = vide()
for P in ORDRE:
    for (x, y), e in P.items():
        if e == 'O' and 0 <= x < W and 0 <= y < H: g[y][x] = 'O'
poser_rocher(g)
for y in ROCHER:  # le rocher en fil de fer aussi
    for x, ch in enumerate(ROCHER[y]):
        if ch not in '.O': g[y][x] = '.'
ecrire(g, 'cristal_e1_esquisse')

# ---- Étape 2 : chevauchements résolus (les traits cachés disparaissent)
vis = composite()
# quel prisme possède chaque pixel visible (le contour 'O' appartient au dernier posé)
proprio = {}
for i, P in enumerate(ORDRE):
    for k in P: proprio[k] = i
for y in ROCHER:
    for x, ch in enumerate(ROCHER[y]):
        if ch != '.': proprio.pop((x, y), None)
g = vide()
for (x, y), e in vis.items():
    if e == 'O': g[y][x] = 'O'
poser_rocher(g)
for y in ROCHER:
    for x, ch in enumerate(ROCHER[y]):
        if ch not in '.O': g[y][x] = '.'
ecrire(g, 'cristal_e2_chevauchements')

# ---- Étape 3 : aplats + arêtes des facettes tracées (avant tout ombrage)
g = vide()
for (x, y), e in vis.items():
    g[y][x] = 'O' if e == 'O' else 'u'
for (x, y), e in vis.items():
    if e == 'O': continue
    for dx, dy in ((1, 0), (0, -1)):
        n = vis.get((x + dx, y + dy))
        if n and n != 'O' and n[0] == e[0] and n != e:
            g[y][x] = 't'
poser_rocher(g)
for y in ROCHER:
    for x, ch in enumerate(ROCHER[y]):
        if ch not in '.O': g[y][x] = 'c'
ecrire(g, 'cristal_e3_facettes')

# ---- Étape 4 : ombrage de base, un ton par facette (gauche éclairée, avant, droite ombre)
TON = {'g': 'w', 'a': 'v', 'd': 'u', 'G': 'w', 'A': 'w', 'D': 'v'}
def base():
    g = vide()
    for (x, y), e in vis.items():
        g[y][x] = 'O' if e == 'O' else TON[e[1]]
    poser_rocher(g)
    return g
g = base(); ecrire(g, 'cristal_e4_ombrage')

# ---- Étape 5 : ombres secondaires
# prisme du fond (2) un ton plus sombre ; AO au pied (2 rangs au-dessus du rocher) ;
# arête claire le long de la crête gauche/avant du grand prisme (moitié haute seulement)
PLUS_SOMBRE = {'W': 'w', 'w': 'v', 'v': 'u', 'u': 't', 't': 't'}
def etape5(g):
    for (x, y), e in vis.items():
        if e == 'O': continue
        if e[0] == '2': g[y][x] = PLUS_SOMBRE[g[y][x]]
    for (x, y), e in vis.items():   # AO : le pixel juste au-dessus du rocher s'assombrit
        if e != 'O' and (x, y + 1) not in vis and y + 1 in ROCHER and g[y + 1][x] != '.':
            g[y][x] = PLUS_SOMBRE[g[y][x]]
    for (x, y), e in vis.items():   # crête : dernier px de la face gauche, rangs du haut
        if e == '1g' and vis.get((x + 1, y)) == '1a' and y <= 16:
            g[y][x] = 'W'
    return g
g = etape5(base()); ecrire(g, 'cristal_e5_ombres')

# ---- Étape 6 : éclats aux pointes + contour coloré (selout)
POINTES = [(13, 2), (13, 3), (24, 8), (5, 17), (27, 23)]
def etape6(g):
    for x, y in POINTES:
        if vis.get((x, y), 'O') != 'O': g[y][x] = 'W'
    for (x, y), e in vis.items():
        if e != 'O': continue
        # le bord d'un cristal devient teal sombre, plus clair (u) sur les bords haut-gauche
        voisins = [vis.get((x + dx, y + dy)) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))]
        dehors_hg = vis.get((x - 1, y)) is None or vis.get((x, y - 1)) is None
        interieur = vis.get((x + 1, y), 'O') != 'O' or vis.get((x, y + 1), 'O') != 'O'
        g[y][x] = 'u' if (dehors_hg and interieur and y < 24) else 't'
    return g
g = etape6(etape5(base())); ecrire(g, 'cristal_e6_eclats')

# ---- Étape 7 : contre-jour violet en bas à droite (la lumière traverse le cristal)
def etape7(g):
    for (x, y), e in vis.items():
        if e == 'O' or e[1] not in 'dD': continue
        if vis.get((x + 1, y), 'O') == 'O' and y >= 12:
            g[y][x] = 'x'
    return g
g = etape7(etape6(etape5(base()))); ecrire(g, 'cristal_e7_contrejour')

# ---- Étape 8 : variation de teinte ; rebond turquoise sur le rocher près des pieds,
def etape8(g):
    # rebond turquoise : deux petites taches choisies à la main sous les pieds les plus
    # lumineux (un pointillé régulier faisait du bruit, essai rejeté)
    for x, y in ((11, 27), (12, 27), (13, 27)): g[y][x] = 'v'
    for x, y in ((10, 28), (11, 28), (24, 27), (25, 27)): g[y][x] = 'u'
    return g
g = etape8(etape7(etape6(etape5(base())))); ecrire(g, 'cristal_e8_variation')

# ---- Étape 9 : finitions : fissure du rocher (règle 41), étincelles détachées, nettoyage
def etape9(g):
    for x, y in ((3, 26), (4, 27), (4, 28), (5, 29)): g[y][x] = 'b'   # fissure (trait b)
    for x, y in ((5, 28), (6, 29)): g[y][x] = 'd'                 # lèvre claire en bas à droite
    for cx, cy in ((4, 9), (29, 3)):                          # étincelles en croix
        g[cy][cx] = 'W'
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)): g[cy + dy][cx + dx] = 'w'
    g[13][1] = 'v'                                            # point isolé, plus petit
    return g
g = etape9(etape8(etape7(etape6(etape5(base())))))
ecrire(g, 'cristal_e9_final'); ecrire(g, 'cristal_grand')
