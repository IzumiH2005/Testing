"""Repos (idle) en 6 images : on garde les pixels Ludo, le buste respire d'un pixel,
les mains suivent, le bas de la cape ondule. Les jambes ne bougent pas."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rig import *

DY = [0, 0, 1, 1, 1, 0]          # buste et tête descendent d'un pixel (expiration)
TETE = [0, 0, 0, 1, 1, 1]        # la tête suit avec une image de retard (chevauchement)
HOULE = [0, 0, 0, -1, -1, 0]     # bas de la cape, encore en retard

def image_repos(i):
    C = canevas()
    cape_g = [r[:] for r in CAPE0]
    for y, r in enumerate(CAPE0):
        if y < 18: continue
        d = DY[i] if y < 30 else HOULE[i] + DY[i] * (y < 38)
        cape_g[y] = ['.'] * 20
        for x, c in enumerate(r):
            if c != '.' and 0 <= x + (HOULE[i] if y >= 30 else 0) < 20:
                cape_g[y][x + (HOULE[i] if y >= 30 else 0)] = c
    # cape : haut avec le buste, bas qui bascule
    g = [['.'] * 20 for _ in CAPE0]
    for y, r in enumerate(cape_g):
        yy = y + (DY[i] if y < 38 else 0)
        if yy < len(g):
            for x, c in enumerate(r):
                if c != '.': g[yy][x] = c
    coller(C, g)
    coller(C, JL0); coller(C, MAINL, 0, DY[i])
    coller(C, BUSTE, 0, DY[i], rows=(17, 37))
    coller(C, BUSTE, 0, DY[i], rows=(16, 16))      # le cou s'étire : pas de trou sous le menton
    coller(C, BUSTE, 0, TETE[i], rows=(0, 16))
    coller(C, JP0); coller(C, MAINP, 0, DY[i])
    return boucher(C)

if __name__ == '__main__':
    from px import image, ecrire
    from PIL import Image
    os.makedirs('repos', exist_ok=True)
    ims = [image_repos(i) for i in range(6)]
    for i, g in enumerate(ims): ecrire(f'repos/repos_{i}.txt', g, f'Repos, image {i}')
    Z = 6
    pl = Image.new('RGBA', (CW * Z * 6, CH * Z), (60, 52, 80, 255))
    for i, g in enumerate(ims):
        im = image(g, None, Z); pl.paste(im, (i * CW * Z, 0), im)
    pl.save('repos_planche_x6.png')
    fr = [image(g, '#3c3450', 4) for g in ims]
    fr[0].save('repos_x4.gif', save_all=True, append_images=fr[1:], duration=[220, 160, 160, 220, 160, 160], loop=0, disposal=2)
