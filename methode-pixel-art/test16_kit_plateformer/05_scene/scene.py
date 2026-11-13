"""Scène de démonstration (F5 composition, F6 contrôles). Ne dessine rien de neuf : elle pose
les pièces du kit. Ordre des plans (du fond vers l'avant) : L0 paroi (fixe), L1 piliers ×0,25,
L2 ruines ×0,5, halo du cristal, roche jouable (autotile), dalles, décors, épines, personnage,
premier plan ×1,25. Caméra : pas de 4 px, donc L1 avance de 1 px, L2 de 2 px, FG de 5 px :
toujours des pas entiers (F3, pas de pixel « flottant »)."""
import sys, json
sys.path.insert(0, '../../outils')
from pxlib import *
from autotile import render_map
K = '..'
pal = load_palette(f'{K}/00_intention/palette.json')
G = lambda p: grid_to_image(load_grid(f'{K}/{p}'), pal)
W, H, DY = 320, 180, 12                       # écran ; DY = rangée de pixels coupée en haut
carte = [r for r in open('niveau.txt').read().splitlines() if not r.startswith('#')]
solide = [''.join('X' if c == 'X' else '.' for c in r) for r in carte]
T = f'{K}/01_tuiles'
var = json.load(open(f'{T}/variantes.json'))
var = {k: [load_grid(f'{T}/{f}') for f in v] for k, v in var.items()}
roche = render_map(load_grid(f'{T}/etape03_ilot.txt'), load_grid(f'{T}/etape04_coins.txt'), pal, solide, var)
LW = roche.width
fonds = {n: G(f'04_fonds/{f}.txt') for n, f in
         [('L0', 'fond_l0_paroi'), ('L1', 'fond_l1_piliers'), ('L2', 'fond_l2_ruines'), ('FG', 'fond_fg')]}

def boucle(im, dx):
    """Couche de 320 px décalée de dx (entier), recollée en boucle."""
    dx %= im.width
    out = Image.new('RGBA', im.size, (0, 0, 0, 0))
    out.alpha_composite(im.crop((dx, 0, im.width, im.height)), (0, 0))
    out.alpha_composite(im.crop((0, 0, dx, im.height)), (im.width - dx, 0))
    return out

# ---- plan jouable : roche, dalles, épines, décors posés (coordonnées du niveau, en px) -------
jeu = Image.new('RGBA', (LW, len(carte) * 16), (0, 0, 0, 0))
halo = Image.new('RGBA', jeu.size, (0, 0, 0, 0))
pieges = Image.new('RGBA', jeu.size, (0, 0, 0, 0))
jeu.alpha_composite(roche)
for y, r in enumerate(carte):
    xs = [x for x, c in enumerate(r) if c == '=']
    for x in xs:
        nom = 'dalle_g' if x - 1 not in xs else 'dalle_d' if x + 1 not in xs else ('dalle_m1', 'dalle_m2')[x % 2]
        jeu.alpha_composite(G(f'02_dalles/{nom}.txt'), (x * 16, y * 16))
    for x, c in enumerate(r):
        if c == '^':
            pieges.alpha_composite(G(f'03_decors/epines{1 + x % 2}.txt'), (x * 16, y * 16))
DECORS = [  # (fichier, x, y) : y = haut de l'image ; les pieds posent sur la croûte (2 px dedans)
 ('rocher_compose', 6, 106), ('touffe1', 66, 122), ('cristal_petit', 92, 114),
 ('racines', 196, 32), ('racines', 262, 48), ('touffe2', 222, 106), ('touffe3', 312, 106),
 ('colonne_brisee', 296, 66), ('cristal_grand', 238, 82), ('touffe1', 420, 130), ('cristal_petit', 448, 114),
 ('rocher_compose', 400, 106), ('racines', 330, 16),
]
for f, x, y in DECORS:
    jeu.alpha_composite(G(f'03_decors/{f}.txt'), (x, y))
    if f == 'cristal_grand':
        halo.alpha_composite(G('03_decors/cristal_grand_halo.txt'), (x - 8, y - 8))
perso = G('03_decors/perso_test.txt'); PERSO = (52, 128 - 24 + 1)   # 1 px dans la croûte

def ecran(cam, avec_perso=True):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 255))
    im.alpha_composite(fonds['L0'])
    im.alpha_composite(boucle(fonds['L1'], cam // 4))
    im.alpha_composite(boucle(fonds['L2'], cam // 2))
    for calque in (halo, jeu, pieges):
        im.alpha_composite(calque.crop((cam, DY, cam + W, DY + H)))
    if avec_perso:
        im.alpha_composite(perso, (PERSO[0] - cam, PERSO[1] - DY))
    im.alpha_composite(boucle(fonds['FG'], cam * 5 // 4))
    return im

if __name__ == '__main__':
    sc = ecran(0)
    sc.save('scene_320x180.png'); scale(sc, 4).save('scene_x4.png')
    # GIF de parallaxe : aller-retour, caméra 0 → 160 par pas de 4 px
    cams = list(range(0, 161, 4)); cams += cams[-2:0:-1]
    frames = [scale(ecran(c), 2).convert('P', palette=Image.ADAPTIVE, colors=64) for c in cams]
    frames[0].save('parallaxe.gif', save_all=True, append_images=frames[1:], duration=60, loop=0)
    print('ok', len(frames), 'images')
