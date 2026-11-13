"""Petits outils : lire/écrire des grilles .txt (une lettre = une couleur), rendre en PNG/GIF."""
import json, os
from PIL import Image

ICI = os.path.dirname(os.path.abspath(__file__))
PAL = json.load(open(os.path.join(ICI, '..', 'palette.json')))
PAL = {k: v for k, v in PAL.items() if not k.startswith('_')}

def hexrgb(h):
    h = h.lstrip('#'); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def lire(chemin):
    lignes = [l.rstrip('\n') for l in open(chemin) if not l.startswith('#')]
    w = max(len(l) for l in lignes)
    return [list(l.ljust(w, '.')) for l in lignes]

def ecrire(chemin, g, entete=None):
    with open(chemin, 'w') as f:
        if entete:
            for l in entete.splitlines(): f.write('# ' + l + '\n')
        for r in g: f.write(''.join(r) + '\n')

def image(g, fond=None, zoom=1):
    h, w = len(g), len(g[0])
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0) if fond is None else hexrgb(fond) + (255,))
    p = im.load()
    for y, r in enumerate(g):
        for x, c in enumerate(r):
            if c in PAL: p[x, y] = hexrgb(PAL[c]) + (255,)
    if zoom > 1: im = im.resize((w * zoom, h * zoom), Image.NEAREST)
    return im
