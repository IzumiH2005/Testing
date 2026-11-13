#!/usr/bin/env python3
"""raccords_env.py : contrôle des raccords (procédure : chaque jeu de tuiles répété en colonne de 22 rangées).
Usage : python3 raccords_env.py tuiles.png tw th sortie.png [cols_h]
 -> une colonne par tuile répétée 22 fois + 2 colonnes « tirage mixte » (base 0-3, 4 à 10 %, 5 à 6 %, comme tower.gd),
    + si cols_h : répétition horizontale (cols_h exemplaires côte à côte) pour les fonds. Rendu x1 et @3."""
import sys, random
from PIL import Image
src, tw, th, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
ch = int(sys.argv[5]) if len(sys.argv) > 5 else 1
im = Image.open(src).convert("RGBA")
n = im.width // tw
rows = 22 if th <= 16 else 11
tiles = [im.crop((i * tw, 0, (i + 1) * tw, th)) for i in range(n)]
gap = 4
W = (n + 2) * (tw * ch + gap)
H = rows * th
sheet = Image.new("RGBA", (W, H), (14, 10, 26, 255))
rnd = random.Random(7)
for c in range(n + 2):
    for r in range(rows):
        if c < n:
            t = tiles[c]
        else:
            x = rnd.random()
            i = 4 if (x < 0.10 and n > 4) else 5 if (x < 0.16 and n > 5) else rnd.randrange(min(4, n))
            t = tiles[i]
        for k in range(ch):
            sheet.paste(t, (c * (tw * ch + gap) + k * tw, r * th), t)
sheet.save(out)
sheet.resize((W * 3, H * 3), Image.NEAREST).save(out.replace(".png", "@3.png"))
print("ok", out, W, H)
