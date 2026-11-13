#!/usr/bin/env python3
"""trace_env.py : pose des primitives DÉCIDÉES À LA MAIN et écrit une grille px.py.

Ne calcule aucune forme, aucune ombre, aucun dégradé (méthode R3) : il recopie des blocs
de pixels écrits à la main (`grid`) et remplit des formes dont l'auteur a fixé chaque
coordonnée (`rect`, `hline`, `vline`, `px`, `poly`). Sert aux sources de art/src/env/.

Format d'une source (en-tête comme px.py, puis des commandes) :
    # commentaires (recopiés dans la grille de sortie)
    palette: /home/user/Testing/jeu/studio/palette_v2.txt
    size: 128x16
    fill C                      remplit tout (C = caractère, '.' = transparent)
    rect C x1 y1 x2 y2          rectangle plein, bornes incluses
    hline C x1 x2 y | vline C x y1 y2
    px C x y [x y ...]          pixels isolés décidés
    poly C x1 y1 x2 y2 ...      polygone plein (sommets décidés, remplissage par centre de pixel)
    grid X Y                    bloc écrit à la main, collé en (X,Y) jusqu'à la ligne `end`
                                ('.' dans un bloc = ne touche pas le pixel ; ',' = rend transparent)
    copy x1 y1 x2 y2 dx dy      recopie une zone déjà dessinée (répétition d'un module décidé)
Usage : python3 trace_env.py source.txt grille_sortie.txt
"""
import sys


def poly_fill(g, c, pts):
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    n = len(pts)
    for y in range(int(min(ys)), int(max(ys)) + 1):
        cy = y + 0.5
        for x in range(int(min(xs)), int(max(xs)) + 1):
            cx = x + 0.5
            inside = False
            j = n - 1
            for i in range(n):
                xi, yi = pts[i]
                xj, yj = pts[j]
                if (yi > cy) != (yj > cy):
                    xint = xi + (cy - yi) * (xj - xi) / (yj - yi)
                    if cx < xint:
                        inside = not inside
                j = i
            if inside:
                put(g, x, y, c)


def put(g, x, y, c):
    if 0 <= y < len(g) and 0 <= x < len(g[0]):
        g[y][x] = "." if c == "," else c  # ',' = rendre transparent (ouverture)


def main():
    src, out = sys.argv[1], sys.argv[2]
    header, g = [], None
    lines = open(src, encoding="utf-8").read().split("\n")
    i = 0
    while i < len(lines):
        raw = lines[i]
        s = raw.strip()
        i += 1
        if not s:
            continue
        if s.startswith("#") or s.startswith("palette:") or s.startswith("frames:"):
            header.append(s)
            continue
        if s.startswith("size:"):
            header.append(s)
            w, h = [int(v) for v in s.split(":")[1].strip().split("x")]
            g = [["."] * w for _ in range(h)]
            continue
        p = s.split()
        op = p[0]
        if op == "fill":
            for row in g:
                for x in range(len(row)):
                    row[x] = p[1]
        elif op == "rect":
            c, x1, y1, x2, y2 = p[1], *map(int, p[2:6])
            for y in range(y1, y2 + 1):
                for x in range(x1, x2 + 1):
                    put(g, x, y, c)
        elif op == "hline":
            c, x1, x2, y = p[1], *map(int, p[2:5])
            for x in range(x1, x2 + 1):
                put(g, x, y, c)
        elif op == "vline":
            c, x, y1, y2 = p[1], *map(int, p[2:5])
            for y in range(y1, y2 + 1):
                put(g, x, y, c)
        elif op == "px":
            c = p[1]
            v = list(map(int, p[2:]))
            for k in range(0, len(v), 2):
                put(g, v[k], v[k + 1], c)
        elif op == "poly":
            c = p[1]
            v = list(map(float, p[2:]))
            poly_fill(g, c, [(v[k], v[k + 1]) for k in range(0, len(v), 2)])
        elif op == "copy":
            x1, y1, x2, y2, dx, dy = map(int, p[1:7])
            blk = [[g[y][x] for x in range(x1, x2 + 1)] for y in range(y1, y2 + 1)]
            for yy, row in enumerate(blk):
                for xx, c in enumerate(row):
                    put(g, dx + xx, dy + yy, c)
        elif op == "grid":
            X, Y = int(p[1]), int(p[2])
            yy = 0
            while lines[i].strip() != "end":
                row = lines[i].rstrip("\n")
                for xx, c in enumerate(row):
                    if c == ".":
                        continue
                    put(g, X + xx, Y + yy, "." if c == "," else c)
                yy += 1
                i += 1
            i += 1
        else:
            raise SystemExit(f"{src}: commande inconnue '{op}' (ligne {i})")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(header) + "\n---\n")
        f.write("\n".join("".join(r) for r in g) + "\n")
    print("grille", out)


if __name__ == "__main__":
    main()
