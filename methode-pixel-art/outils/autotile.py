"""autotile.py : assemble les 47 tuiles « blob » à partir de 4 pièces dessinées à la main
(F2-C). Ne dessine rien : il découpe l'îlot 32×32 et le bloc des coins intérieurs 16×16 en
quarts de 8×8 et les recolle selon les voisins.

  python3 autotile.py ilot.txt coins.txt palette.json carte.txt sortie.png [variantes.json]
  python3 autotile.py ilot.txt coins.txt palette.json --atlas sortie.png

Carte : 'X' = sol, tout autre caractère = vide. variantes.json (facultatif) :
{"remplissage": ["var1.txt", ...], "croute": ["croute1.txt", ...]} : tuiles 16×16 complètes
qui remplacent, selon un hasard fixe (graine), une tuile de remplissage ou de croûte."""
import sys, json, random
from PIL import Image
from pxlib import *

Q = 8
# position du quart -> type -> (qx, qy) dans l'îlot
SRC = {
    'TL': {'out': (0, 0), 'h': (2, 0), 'v': (0, 2), 'fill': (2, 2)},
    'TR': {'out': (3, 0), 'h': (1, 0), 'v': (3, 2), 'fill': (1, 2)},
    'BL': {'out': (0, 3), 'h': (2, 3), 'v': (0, 1), 'fill': (2, 1)},
    'BR': {'out': (3, 3), 'h': (1, 3), 'v': (3, 1), 'fill': (1, 1)},
}
INNER = {'TL': (0, 0), 'TR': (1, 0), 'BL': (0, 1), 'BR': (1, 1)}
# pour chaque quart : voisin vertical, horizontal, diagonal
NB = {'TL': ((0, -1), (-1, 0), (-1, -1)), 'TR': ((0, -1), (1, 0), (1, -1)),
      'BL': ((0, 1), (-1, 0), (-1, 1)), 'BR': ((0, 1), (1, 0), (1, 1))}
OFF = {'TL': (0, 0), 'TR': (Q, 0), 'BL': (0, Q), 'BR': (Q, Q)}

def quarter(rows, qx, qy):
    return [r[qx * Q:(qx + 1) * Q] for r in rows[qy * Q:(qy + 1) * Q]]

def tile(ilot, coins, solid):
    """solid(dx, dy) -> bool. Renvoie 16 lignes de 16 caractères."""
    out = [[''] * 2 for _ in range(16)]
    t = [['.'] * 16 for _ in range(16)]
    for pos in SRC:
        (vx, vy), (hx, hy), (dx, dy) = NB[pos]
        v, h, d = solid(vx, vy), solid(hx, hy), solid(dx, dy)
        if v and h:
            q = quarter(ilot, *SRC[pos]['fill']) if d else quarter(coins, *INNER[pos])
        elif v:
            q = quarter(ilot, *SRC[pos]['v'])
        elif h:
            q = quarter(ilot, *SRC[pos]['h'])
        else:
            q = quarter(ilot, *SRC[pos]['out'])
        ox, oy = OFF[pos]
        for y in range(Q):
            for x in range(Q):
                t[oy + y][ox + x] = q[y][x]
    return [''.join(r) for r in t]

def render_map(ilot, coins, pal, carte, variantes=None, seed=7):
    H, W = len(carte), max(len(r) for r in carte)
    carte = [r.ljust(W, '.') for r in carte]
    S = lambda x, y: 0 <= y < H and 0 <= x < W and carte[y][x] == 'X'
    S2 = lambda x, y: (not (0 <= y < H and 0 <= x < W)) or carte[y][x] == 'X'  # bords = sol
    rnd = random.Random(seed)
    im = Image.new('RGBA', (W * 16, H * 16), (0, 0, 0, 0))
    for y in range(H):
        for x in range(W):
            if not S(x, y):
                continue
            sol = lambda dx, dy: S(x + dx, y + dy) if (0 <= y + dy < H) else True
            rows = tile(ilot, coins, sol)
            all8 = all(sol(dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1))
            top = (not sol(0, -1)) and all(sol(dx, dy) for dx, dy in [(-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)])
            if variantes:
                if all8 and variantes.get('remplissage') and rnd.random() < 0.3:
                    rows = rnd.choice(variantes['remplissage'])
                elif top and variantes.get('croute') and rnd.random() < 0.4:
                    rows = rnd.choice(variantes['croute'])
            im.alpha_composite(grid_to_image(rows, pal), (x * 16, y * 16))
    return im

def atlas(ilot, coins, pal):
    """Les 47 combinaisons utiles, rangées 8 par ligne."""
    seen, tiles = set(), []
    for m in range(256):
        n = [(m >> i) & 1 for i in range(8)]
        dirs = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]
        sol = lambda dx, dy: n[dirs.index((dx, dy))] == 1
        # un coin ne compte que si ses deux côtés sont pleins
        key = tuple(sol(*d) if d[0] == 0 or d[1] == 0 else (sol(*d) and sol(d[0], 0) and sol(0, d[1])) for d in dirs)
        if key in seen:
            continue
        seen.add(key)
        tiles.append(tile(ilot, coins, sol))
    cols = 8
    im = Image.new('RGBA', (cols * 16, ((len(tiles) + cols - 1) // cols) * 16), (0, 0, 0, 0))
    for i, t in enumerate(tiles):
        im.alpha_composite(grid_to_image(t, pal), ((i % cols) * 16, (i // cols) * 16))
    return im, len(tiles)

if __name__ == '__main__':
    ilot, coins = load_grid(sys.argv[1]), load_grid(sys.argv[2])
    pal = load_palette(sys.argv[3])
    if sys.argv[4] == '--atlas':
        im, n = atlas(ilot, coins, pal); im.save(sys.argv[5]); print(sys.argv[5], n, 'tuiles')
    else:
        carte = load_grid(sys.argv[4])
        var = None
        if len(sys.argv) > 6:
            spec = json.load(open(sys.argv[6]))
            var = {k: [load_grid(p) for p in v] for k, v in spec.items()}
        im = render_map(ilot, coins, pal, carte, var)
        im.save(sys.argv[5]); print(sys.argv[5], im.size)
