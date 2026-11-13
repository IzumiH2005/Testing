"""Planches d'étapes (B6) : chaque étape côte à côte, sur un fond moyen pour que les traits
sombres de l'esquisse se voient."""
import sys; sys.path.insert(0, '../../outils'); from pxlib import *
pal = load_palette('../00_intention/palette.json')
def bande(fichiers, sortie, k, fond=(96, 92, 108, 255)):
    ims = [grid_to_image(load_grid(f), pal) for f in fichiers]
    W = sum(i.width + 4 for i in ims) + 4; H = max(i.height for i in ims) + 8
    im = Image.new('RGBA', (W, H), fond); x = 4
    for i in ims: im.alpha_composite(i, (x, 4)); x += i.width + 4
    scale(im, k).save(sortie)
D = '../03_decors/'
bande([D + f'cristal_e{i}_{n}.txt' for i, n in enumerate(
    ['esquisse', 'chevauchements', 'facettes', 'ombrage', 'ombres', 'eclats', 'contrejour', 'variation', 'final'], 1)],
    'c8_etapes_cristal.png', 4)
bande([D + f for f in ['rocher_e1_formes.txt', 'rocher_e2_deformer.txt', 'rocher_e3a_sousplans_rejet.txt',
                       'rocher_e3_sousplans.txt', 'rocher_e4_polir.txt']], 'c8_etapes_rocher.png', 5)
F = '../04_fonds/'
bande([F + f for f in ['paroi_v1_rejet.txt', 'paroi_e1_masses.txt', 'paroi_e3_faille.txt', 'paroi_e4_rayons.txt',
                       'fond_l0_paroi.txt']], 'c8_etapes_paroi.png', 1)
bande([D + 'perso_test_v1_rejet.txt', D + 'perso_test.txt'], 'c8_perso_contour_selectif.png', 6, (40, 38, 56, 255))
print('ok')
