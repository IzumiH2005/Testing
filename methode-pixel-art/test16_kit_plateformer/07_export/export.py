"""Export ×1 prêt pour un moteur (Godot, etc.) : une PNG par pièce, les fonds, l'atlas des 47
tuiles et un atlas des décors avec ses coordonnées (atlas_decors.json). Les .txt restent la
source ; ces PNG se régénèrent avec ce script."""
import sys, os, json; sys.path.insert(0, '../../outils')
from pxlib import *
from autotile import atlas
pal = load_palette('../00_intention/palette.json')
G = lambda p: grid_to_image(load_grid(p), pal)
os.makedirs('pieces', exist_ok=True); os.makedirs('fonds', exist_ok=True)
T = '../01_tuiles/'
im, n = atlas(load_grid(T + 'etape03_ilot.txt'), load_grid(T + 'etape04_coins.txt'), pal)
im.save('tuiles_47.png')
for f in ['etape05_rempl1', 'etape05_rempl2', 'etape05_croute1', 'etape05_croute2']:
    G(T + f + '.txt').save(f'pieces/tuile_{f[8:]}.png')
PIECES = {f: f'../02_dalles/{f}.txt' for f in ['dalle_g', 'dalle_m1', 'dalle_m2', 'dalle_d']}
PIECES.update({f: f'../03_decors/{f}.txt' for f in
               ['cristal_grand', 'cristal_grand_halo', 'cristal_petit', 'rocher_compose', 'colonne_brisee',
                'racines', 'touffe1', 'touffe2', 'touffe3', 'epines1', 'epines2', 'perso_test']})
ims = {k: G(v) for k, v in PIECES.items()}
for k, i in ims.items(): i.save(f'pieces/{k}.png')
# atlas des décors : rangement en étagères de 256 px, 1 px de marge (pas de fuite au filtrage)
x = y = h = 0; coords = {}; W = 256
for k in sorted(ims, key=lambda k: -ims[k].height):
    i = ims[k]
    if x + i.width + 1 > W: x, y, h = 0, y + h + 1, 0
    coords[k] = [x, y, i.width, i.height]; x += i.width + 1; h = max(h, i.height)
at = Image.new('RGBA', (W, y + h), (0, 0, 0, 0))
for k, (x, y, w, hh) in coords.items(): at.alpha_composite(ims[k], (x, y))
at.save('atlas_decors.png'); json.dump(coords, open('atlas_decors.json', 'w'), indent=1)
for f, nom in [('fond_l0_paroi', 'l0_paroi_fixe'), ('fond_l1_piliers', 'l1_piliers_x0.25'),
               ('fond_l2_ruines', 'l2_ruines_x0.5'), ('fond_fg', 'fg_premier_plan_x1.25')]:
    G(f'../04_fonds/{f}.txt').save(f'fonds/{nom}.png')
print(n, 'tuiles,', len(ims), 'pièces, atlas', at.size)
