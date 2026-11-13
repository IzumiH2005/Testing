#!/usr/bin/env python3
"""assemble.py : aperçu de contrôle du décor (lot 2 env).

Ne dessine rien : il découpe les PNG finaux en tuiles 16x16 et les juxtapose.
  apercu.png      192x352 : mur gauche, fond, mur droit (miroir), dalle en bas, plaque
  raccords_back.png  toutes les paires de tuiles 0-3 de back, en mosaïque
  raccords_wall.png  colonnes de wall dans plusieurs ordres
Chaque sortie a aussi une version x3 (suffixe @3).
Usage : python3 assemble.py [graine]
"""
import random, sys, os
from PIL import Image, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "..", "..", "..", "game", "assets", "env")
T = 16

def tiles(name):
    im = Image.open(os.path.join(ASSETS, name)).convert("RGBA")
    return [im.crop((i * T, 0, i * T + T, T)) for i in range(im.width // T)]

wall, back, floor = tiles("wall.png"), tiles("back.png"), tiles("floor.png")
plaque = Image.open(os.path.join(ASSETS, "plaque.png")).convert("RGBA")

def save(im, name):
    im.save(os.path.join(HERE, name + ".png"))
    im.resize((im.width * 3, im.height * 3), Image.NEAREST).save(os.path.join(HERE, name + "@3.png"))
    print("ok", name, im.size)

def pick_wall(rng, prev):
    r = rng.random()
    if r < 0.10 and prev != 4: return 4          # mousse
    if r < 0.16 and prev != 5: return 5          # fissure
    c = [i for i in range(4) if i != prev]
    return rng.choice(c)

def apercu(seed):
    rng = random.Random(seed)
    W, H = 12, 22
    im = Image.new("RGBA", (W * T, H * T), (0, 0, 0, 255))
    # fond : tuiles 0-3 au hasard, spéciales espacées
    grid = [[rng.choice(range(4)) for _ in range(1, W - 1)] for _ in range(H - 1)]
    last = {4: -99, 5: -99, 6: -99}
    gaps = {4: 9, 5: 7, 6: 11}
    for y in range(H - 1):
        for k in (4, 5, 6):
            if y - last[k] >= gaps[k] and rng.random() < 0.35:
                x = rng.randrange(1, W - 3)
                if all(c < 4 for c in grid[y]):
                    grid[y][x] = k
                    last[k] = y
    for y in range(H - 1):
        for x in range(1, W - 1):
            im.paste(back[grid[y][x - 1]], (x * T, y * T))
    # murs
    pl = pr = -1
    for y in range(H - 1):
        pl = pick_wall(rng, pl); pr = pick_wall(rng, pr)
        im.paste(wall[pl], (0, y * T))
        im.paste(ImageOps.mirror(wall[pr]), ((W - 1) * T, y * T))
    # dalle sur toute la largeur du puits
    y = (H - 1) * T
    im.paste(ImageOps.mirror(wall[0]), ((W - 1) * T, y)); im.paste(wall[1], (0, y))
    for x in range(1, W - 1):
        im.paste(floor[0 if x == 1 else 2 if x == W - 2 else 1], (x * T, y))
    # plaque posée sur le fond (comme un élément de score / niveau)
    im.alpha_composite(plaque, (80, 40))
    return im

def raccords_back():
    # chaque paire (a,b) en bloc 2x2 : a b / b a, séparés par rien : tout se touche
    n = 4
    im = Image.new("RGBA", (n * 2 * T, n * 2 * T))
    for a in range(n):
        for b in range(n):
            ox, oy = a * 2 * T, b * 2 * T
            im.paste(back[a], (ox, oy)); im.paste(back[b], (ox + T, oy))
            im.paste(back[b], (ox, oy + T)); im.paste(back[a], (ox + T, oy + T))
    return im

def raccords_back_seul():
    # une seule variante répétée 4x4, pour voir le motif
    im = Image.new("RGBA", (4 * 4 * T, 4 * T))
    for v in range(4):
        for y in range(4):
            im.paste(back[v], (v * 4 * T + (y % 2) * 0, y * T))
            for x in range(4):
                im.paste(back[v], (v * 4 * T + x * T, y * T))
    return im

def raccords_wall():
    orders = [[0, 1, 2, 3, 4, 5], [3, 2, 1, 0, 5, 4], [0, 0, 1, 1, 2, 2], [5, 3, 4, 2, 1, 0]]
    im = Image.new("RGBA", (len(orders) * 2 * T, 6 * T))
    for i, o in enumerate(orders):
        for y, t in enumerate(o):
            im.paste(wall[t], (i * 2 * T, y * T))
            im.paste(back[(y + i) % 4], (i * 2 * T + T, y * T))
    return im

seed = int(sys.argv[1]) if len(sys.argv) > 1 else 7
save(apercu(seed), "apercu")
save(raccords_back(), "raccords_back")
save(raccords_back_seul(), "raccords_back_seul")
save(raccords_wall(), "raccords_wall")
