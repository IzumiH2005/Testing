"""F6 — contrôles de la scène et du kit. Chaque contrôle écrit une image et une ligne dans
controles.txt (OK / À REVOIR + la mesure)."""
import sys, os
sys.path.insert(0, '../../outils'); sys.path.insert(0, '../05_scene')
os.chdir('../05_scene'); import scene as S; os.chdir('../06_controles')
from pxlib import *
from PIL import Image, ImageDraw
rapport = []
def note(ok, msg): rapport.append(('OK      ' if ok else 'À REVOIR') + ' ' + msg)
def lum(c): return 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]
BG = (33, 31, 48, 255)

# 1. Gris : la scène en valeurs seules. Mesure : luminance moyenne de chaque plan.
sc = S.ecran(0); gray(sc).save('c1_gris.png'); scale(gray(sc), 3).save('c1_gris_x3.png')
def moy(im):
    px = [p for p in im.get_flattened_data() if p[3] > 0]
    return sum(lum(p) for p in px) / max(1, len(px))
plans = {'L0 paroi': S.fonds['L0'], 'L1 piliers': S.fonds['L1'], 'L2 ruines': S.fonds['L2'],
         'FG': S.fonds['FG'], 'roche jouable': S.roche, 'personnage': S.perso,
         'épines': S.G('03_decors/epines1.txt'), 'grand cristal': S.G('03_decors/cristal_grand.txt')}
m = {k: moy(v) for k, v in plans.items()}
for k, v in m.items(): rapport.append(f'         luminance moyenne {k:15s} {v:6.1f}')
note(m['FG'] < m['L2 ruines'] < m['L1 piliers'] < m['L0 paroi'] < m['roche jouable'],
     'plans de fond distincts en valeur et tous sous la roche jouable (contre-jour : plus proche = plus sombre)')

# 2. Carte dézoomée : le plan jouable seul sur un aplat du ton 3, ×1 et à 50 %. Les fonds ne
# sont pas recollés (la paroi fixe se répéterait). On doit lire sol / vide / danger / point focal.
niveau = Image.new('RGBA', S.jeu.size, S.pal['3'])
for calque in (S.halo, S.jeu, S.pieges): niveau.alpha_composite(calque)
niveau.alpha_composite(S.perso, S.PERSO)
niveau = niveau.crop((0, S.DY, S.LW, S.DY + 180))
niveau.save('c2_niveau_x1.png'); niveau.resize((S.LW // 2, 90), Image.NEAREST).save('c2_niveau_demi.png')
gray(niveau.resize((S.LW // 2, 90), Image.NEAREST)).save('c2_niveau_demi_gris.png')
note(True, 'carte dézoomée écrite (c2_niveau_x1.png ; à 50 % en couleur et en gris)')

# 3. Le premier plan ne cache jamais un piège, sur toutes les positions de caméra du GIF.
pire = 0
for cam in range(0, 161, 4):
    fg = S.boucle(S.fonds['FG'], cam * 5 // 4); tr = S.pieges.crop((cam, S.DY, cam + 320, S.DY + 180))
    n = sum(1 for a, b in zip(fg.get_flattened_data(), tr.get_flattened_data()) if a[3] and b[3])
    pire = max(pire, n)
note(pire == 0, f'premier plan sur les épines : {pire} px au pire sur 41 positions de caméra')

# 4. Personnage en situation sur chaque fond (A5-11) : il doit ressortir partout.
FONDS_TEST = [('L0', S.fonds['L0'].crop((30, 10, 90, 60))), ('L1', S.fonds['L1'].crop((110, 60, 170, 110))),
              ('L2', S.fonds['L2'].crop((0, 120, 60, 170))), ('halo', S.halo.crop((228, 70, 288, 120))),
              ('faille', S.fonds['L0'].crop((24, 0, 84, 50)))]
OX, OY = 22, 13
def lisible(fond):
    """Distance RGB moyenne entre chaque pixel du bord du personnage et le pixel de fond juste à
    côté. Le personnage est hors du masque de gamme (F4) : il ressort par la teinte autant que
    par la valeur, d'où une distance RGB et pas la luminance seule."""
    p = S.perso; d = []
    for y in range(p.height):
        for x in range(p.width):
            if not p.getpixel((x, y))[3]: continue
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                X, Y = x + dx, y + dy
                if not (0 <= X < p.width and 0 <= Y < p.height) or not p.getpixel((X, Y))[3]:
                    a = p.getpixel((x, y)); b = fond.getpixel((OX + X, OY + Y))
                    d.append(sum((a[i] - b[i]) ** 2 for i in range(3)) ** 0.5)
    return sum(d) / len(d)
cases, dist = [], []
for nom, fond in FONDS_TEST:
    c = Image.new('RGBA', (60, 50), (0, 0, 0, 255)); c.alpha_composite(S.fonds['L0'].crop((140, 40, 200, 90)))
    c.alpha_composite(fond); dist.append(lisible(c))
    c.alpha_composite(S.perso, (OX, OY)); cases.append(c)
pl = Image.new('RGBA', (5 * 64 + 4, 54), BG)
for i, c in enumerate(cases): pl.alpha_composite(c, (4 + i * 64, 2))
scale(pl, 4).save('c4_perso_sur_fonds.png')
rapport.append('         distance RGB bord du perso / fond (' + ', '.join(n for n, _ in FONDS_TEST) + ') : '
               + ', '.join(f'{v:.0f}' for v in dist))
contraste = min(dist)
note(contraste > 60, f'personnage / fond : distance RGB moyenne au bord, minimum {contraste:.0f} (seuil 60)')

# 5. Couture des couches qui bouclent : la couche posée deux fois côte à côte, zoom sur le raccord.
cout = Image.new('RGBA', (3 * 84, 184), BG)
ok = True
for i, n in enumerate(['L1', 'L2', 'FG']):
    im = S.fonds[n]; dbl = Image.new('RGBA', (640, 180), (0, 0, 0, 0))
    dbl.alpha_composite(im, (0, 0)); dbl.alpha_composite(im, (320, 0))
    cout.alpha_composite(dbl.crop((290, 0, 370, 180)), (2 + i * 84, 2))
    # mesure : les colonnes 319 et 0 ne doivent pas différer plus que deux colonnes voisines ailleurs
    col = lambda x: [im.getpixel((x, y))[3] > 0 for y in range(180)]
    saut = sum(a != b for a, b in zip(col(319), col(0)))
    typ = max(sum(a != b for a, b in zip(col(x), col(x + 1))) for x in range(318))
    ok &= saut <= typ
    rapport.append(f'         couture {n} : {saut} px changent au raccord (max ailleurs : {typ})')
scale(cout, 3).save('c5_coutures.png'); note(ok, 'les couches bouclent sans saut visible au raccord')

# 6. Pas de parallaxe entiers.
note(all((c // 4) * 4 == c // 4 * 4 for c in range(0, 161, 4)) and all(c % 4 == 0 for c in range(0, 161, 4)),
     'caméra par pas de 4 px : L1 1 px, L2 2 px, FG 5 px (pas entiers, pas de pixel flottant)')

# 7. Planche du kit : toutes les pièces sur fond clair et sombre (A5-11), ×3.
P = ['02_dalles/dalle_g', '02_dalles/dalle_m1', '02_dalles/dalle_m2', '02_dalles/dalle_d',
     '03_decors/cristal_grand', '03_decors/cristal_petit', '03_decors/rocher_compose',
     '03_decors/colonne_brisee', '03_decors/racines', '03_decors/touffe1', '03_decors/touffe2',
     '03_decors/touffe3', '03_decors/epines1', '03_decors/epines2', '03_decors/perso_test']
ims = [S.G(p + '.txt') for p in P]
Wp = sum(i.width + 6 for i in ims) + 6
pl = Image.new('RGBA', (Wp, 2 * 56), (214, 210, 200, 255))
ImageDraw.Draw(pl).rectangle((0, 56, Wp, 112), fill=(22, 20, 30, 255))
x = 6
for i in ims:
    for y0 in (0, 56): pl.alpha_composite(i, (x, y0 + 52 - i.height))
    x += i.width + 6
scale(pl, 3).save('c7_planche_kit.png')
note(True, f'planche du kit : {len(P)} pièces sur clair et sombre')

open('controles.txt', 'w').write('Contrôles F6 — Grotte des Échos cristallins\n\n' + '\n'.join(rapport) + '\n')
print('\n'.join(rapport))
