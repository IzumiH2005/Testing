"""Bibliothèque commune des outils (partie D). Elle ne décide rien : elle lit des grilles
écrites à la main (1 caractère = 1 pixel, '.' = vide) et les rend en image."""
import json, os
from PIL import Image, ImageDraw

def load_palette(path):
    with open(path) as f:
        pal = json.load(f)
    out = {}
    for k, v in pal.items():
        if k.startswith('_'):
            continue
        v = v.lstrip('#')
        out[k] = (int(v[0:2], 16), int(v[2:4], 16), int(v[4:6], 16), 255)
    return out

def load_grid(path):
    rows = []
    with open(path) as f:
        for line in f:
            line = line.rstrip('\n')
            if not line or line.startswith('#'):
                continue
            rows.append(line)
    w = len(rows[0])
    for i, r in enumerate(rows):
        if len(r) != w:
            raise ValueError(f"{path}: ligne {i} largeur {len(r)} au lieu de {w}")
    return rows

def save_grid(rows, path):
    with open(path, 'w') as f:
        f.write('\n'.join(rows) + '\n')

def grid_to_image(rows, pal):
    h, w = len(rows), len(rows[0])
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    px = im.load()
    for y, r in enumerate(rows):
        for x, c in enumerate(r):
            if c == '.':
                continue
            if c not in pal:
                raise KeyError(f"couleur inconnue '{c}' en {x},{y}")
            px[x, y] = pal[c]
    return im

def scale(im, k):
    return im.resize((im.width * k, im.height * k), Image.NEAREST)

def vue(im, k=12, bg=(40, 40, 48, 255)):
    """Agrandi avec grille, pour lire les coordonnées."""
    big = Image.new('RGBA', (im.width * k, im.height * k), bg)
    big.alpha_composite(scale(im, k))
    d = ImageDraw.Draw(big)
    for x in range(0, big.width, k):
        col = (90, 90, 100, 255) if (x // k) % 8 else (160, 90, 90, 255)
        d.line([(x, 0), (x, big.height)], fill=col)
    for y in range(0, big.height, k):
        col = (90, 90, 100, 255) if (y // k) % 8 else (160, 90, 90, 255)
        d.line([(0, y), (big.width, y)], fill=col)
    return big

def gray(im):
    g = im.convert('LA').convert('RGBA')
    g.putalpha(im.getchannel('A'))
    return g

def silhouette(im, col=(10, 10, 14, 255)):
    s = Image.new('RGBA', im.size, col)
    s.putalpha(im.getchannel('A'))
    return s

def on_bg(im, col):
    b = Image.new('RGBA', im.size, col)
    b.alpha_composite(im)
    return b

def rle(s):
    """Notation courte d'une rangée décidée à la main : « O e d c26 b a O » = O, e, d, 26 fois c,
    b, a, O. Un jeton = un caractère suivi d'un nombre de répétitions facultatif. Ne calcule
    aucune forme : c'est la même rangée, écrite plus court pour ne pas se tromper en comptant."""
    out = ''
    for tok in s.split():
        out += tok[0] * (int(tok[1:]) if len(tok) > 1 else 1)
    return out
