"""Dessin trait par trait sur un calque d'une frame. Un appel = un geste.

python3 trait.py <dossier_frame> <calque> <commande> ...
  ligne x0 y0 x1 y1 C [x2 y2 ...]   polyligne pixel-perfect (Bresenham)
  px C x y [x y ...]                pixels isolés
  rang C y x0 x1                    segment horizontal
  remplir C x y                     pot de peinture (4-connexe, sur le calque)
  gomme x y [x y ...]               efface des pixels
  coller src x0 y0 x1 y1 dx dy      copie un rectangle du calque dessin d'une autre frame, décalé
  annuler                           revient au dernier état du calque
python3 trait.py <dossier_frame> - voir [zoom]   -> <dossier>/vue.png (calque + mannequin)
Calques : guide.txt (construction, en magenta) puis dessin.txt (le sprite).
"""
import sys, os, json
from PIL import Image

ICI = os.path.dirname(os.path.abspath(__file__))
PAL = {k: v for k, v in json.load(open(os.path.join(ICI, '..', 'palette.json'))).items() if not k.startswith('_')}
W, H = 48, 56
rgb = lambda h: tuple(int(h.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

def lire(f):
    if not os.path.exists(f): return [['.'] * W for _ in range(H)]
    return [list(l.rstrip('\n').ljust(W, '.')) for l in open(f)]

def ecrire(f, g):
    open(f, 'w').write(''.join(''.join(r) + '\n' for r in g))

def bres(x0, y0, x1, y1):
    dx, dy = abs(x1 - x0), -abs(y1 - y0); sx = 1 if x0 < x1 else -1; sy = 1 if y0 < y1 else -1
    e = dx + dy; out = []
    while True:
        out.append((x0, y0))
        if (x0, y0) == (x1, y1): return out
        e2 = 2 * e
        if e2 >= dy: e += dy; x0 += sx
        if e2 <= dx: e += dx; y0 += sy

def poser(g, x, y, c):
    if 0 <= x < W and 0 <= y < H: g[y][x] = c

def vue(d, z):
    ref = [f for f in os.listdir(d) if f.endswith('_ref.png')]
    fond = Image.new('RGBA', (W * z, H * z), (250, 250, 250, 255))
    if ref:
        m = Image.open(os.path.join(d, ref[0])).convert('RGBA').resize((W * z, H * z), Image.NEAREST)
        m.putalpha(m.getchannel('A').point(lambda a: a * 90 // 255)); fond.alpha_composite(m)
    for cal, alpha in (('guide', 200), ('dessin', 255)):
        g = lire(os.path.join(d, cal + '.txt'))
        im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); p = im.load()
        for y in range(H):
            for x in range(W):
                if g[y][x] in PAL: p[x, y] = rgb(PAL[g[y][x]]) + (alpha,)
        fond.alpha_composite(im.resize((W * z, H * z), Image.NEAREST))
    # grille légère toutes les 4 cases pour lire les coordonnées
    p = fond.load()
    for x in range(0, W * z, 4 * z):
        for y in range(H * z): p[x, y] = (200, 200, 210, 255) if p[x, y][:3] == (250, 250, 250) else p[x, y]
    for y in range(0, H * z, 4 * z):
        for x in range(W * z): p[x, y] = (200, 200, 210, 255) if p[x, y][:3] == (250, 250, 250) else p[x, y]
    # sprite seul à droite, taille x4 et x1
    g = lire(os.path.join(d, 'dessin.txt')); seul = Image.new('RGBA', (W, H), (0, 0, 0, 0)); q = seul.load()
    for y in range(H):
        for x in range(W):
            if g[y][x] in PAL and g[y][x] != 'g': q[x, y] = rgb(PAL[g[y][x]]) + (255,)
    tout = Image.new('RGBA', (W * z + W * 4 + W + 30, H * z), (250, 250, 250, 255))
    tout.alpha_composite(fond); tout.alpha_composite(seul.resize((W * 4, H * 4), Image.NEAREST), (W * z + 10, 0))
    tout.alpha_composite(seul, (W * z + W * 4 + 20, 0))
    tout.save(os.path.join(d, 'vue.png'))

d, cal, cmd, *a = sys.argv[1:]
if cmd == 'voir':
    vue(d, int(a[0]) if a else 12); sys.exit()
f = os.path.join(d, cal + '.txt'); hist = f + '.hist'
g = lire(f)
if cmd == 'annuler':
    h = open(hist).read().split('\n=\n') if os.path.exists(hist) else []
    if h: open(f, 'w').write(h.pop()); open(hist, 'w').write('\n=\n'.join(h))
    sys.exit()
open(hist, 'a').write(('\n=\n' if os.path.exists(hist) and os.path.getsize(hist) else '') + ''.join(''.join(r) + '\n' for r in g))
n = list(map(int, a)) if cmd == 'gomme' else [] if cmd == 'ligne' else list(map(int, a[1:]))
if cmd == 'coller':
    src = lire(os.path.join(a[0], 'dessin.txt')); x0, y0, x1, y1, dx, dy = n
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if src[y][x] != '.': poser(g, x + dx, y + dy, src[y][x])
if cmd == 'ligne':
    pts = list(map(int, a[:-1])); c = a[-1]
    for i in range(0, len(pts) - 2, 2):
        for x, y in bres(*pts[i:i + 4]): poser(g, x, y, c)
elif cmd == 'px':
    for i in range(0, len(n), 2): poser(g, n[i], n[i + 1], a[0])
elif cmd == 'rang':
    y, x0, x1 = n
    for x in range(min(x0, x1), max(x0, x1) + 1): poser(g, x, y, a[0])
elif cmd == 'remplir':
    x, y = n; cible = g[y][x]; c = a[0]; pile = [(x, y)]
    if cible != c:
        while pile:
            x, y = pile.pop()
            if 0 <= x < W and 0 <= y < H and g[y][x] == cible:
                g[y][x] = c; pile += [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
elif cmd == 'gomme':
    for i in range(0, len(n), 2): poser(g, n[i], n[i + 1], '.')
ecrire(f, g)
