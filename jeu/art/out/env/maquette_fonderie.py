#!/usr/bin/env python3
"""maquette_fonderie.py : mise en situation 192x352 de la Fonderie (procédure F6/F7), même montage que maquette_crypte.py.
P0/P1 : la Fonderie n'a pas encore de bg0/bg1 propres -> aplat k (#0e0a1a) pour juger murs et bg2 sans aide.
bg2_fonderie en deux bandes x32-63 et x128-159 ; murs : haut = transition vers la Bibliothèque (y1/y0), bas = transition
depuis la Crypte (x1/x0) puis une tuile de crypte ; autel palette-swap + flamme sur le sol ; héros idle au mur gauche."""
from PIL import Image
import sys
D = "/home/user/Testing/jeu/art/out/env/"
HERO = sys.argv[1]
im = lambda n: Image.open(D + n + ".png").convert("RGBA")
t = lambda img, x, y, w, h: img.crop((x, y, x + w, y + h))
W, H = 192, 352
out = Image.new("RGBA", (W, H), (0x0e, 0x0a, 0x1a, 255))
bg2 = im("bg2_fonderie")
P = [t(bg2, i * 32, 0, 32, 32) for i in range(4)]
for x, seq in ((32, "0010203001200130"), (128, "0100300210020010")):
    for j, c in enumerate(seq[:11]):
        out.alpha_composite(P[int(c)], (x, j * 32))
S = {}
for side in "LR":
    S["t", side] = im("wall_fonderie_" + side); S["l", side] = im("wall_fonderie_lit_" + side)
    S["d", side] = im("wall_fonderie_deco_" + side); S["r", side] = im("rune_fonderie_" + side)
    S["y", side] = im("wall_fonderie_to_bibliotheque_" + side); S["x", side] = im("wall_crypte_to_fonderie_" + side)
    S["c", side] = im("wall_crypte_" + side)
def col(x, side, seq):
    y = 0
    for s in seq.split():
        k, i = s[0], int(s[1:])
        h = 32 if k == "d" else 16
        out.alpha_composite(t(S[k, side], i * 16, 0, 16, h), (x, y)); y += h
SEQ_LI = "y1 y0 t0 t2 t1 t4 l0 d0 l1 t3 t0 t5 t1 r1 t2 t0 t3 t1 t7 x1 x0"
SEQ_RI = "y1 y0 t1 t3 t0 t2 d1 t0 t4 t1 t3 d2 t6 t2 r0 t1 t0 x1 x0"
SEQ_LO = "y1 y0 t1 t3 t2 t0 t3 t1 t2 t0 t4 t3 t1 t0 t2 t3 t1 t0 t2 x1 x0"
SEQ_RO = "y1 y0 t2 t0 t3 t1 t0 t2 t4 t1 t3 t0 t2 t1 d3 t0 t2 t1 x1 x0"
col(16, "L", SEQ_LI); col(0, "R", SEQ_LO); col(160, "R", SEQ_RI); col(176, "L", SEQ_RO)
fl = im("floor_start")
for i in range(12):
    out.alpha_composite(t(fl, 0 if i == 0 else 32 if i == 11 else 16, 0, 16, 16), (i * 16, 336))
out.alpha_composite(im("altar_fonderie"), (80, 304))
out.alpha_composite(t(im("altar_flame"), 16, 0, 8, 16), (92, 299))
out.alpha_composite(Image.open(HERO).convert("RGBA").crop((0, 0, 32, 32)), (22, 170))
out.save(D + "maquette_fonderie.png")
out.resize((W * 3, H * 3), Image.NEAREST).save(D + "maquette_fonderie@3.png")
out.crop((6, 0, 186, H)).resize((180 * 3, H * 3), Image.NEAREST).save(D + "maquette_fonderie_ecran@3.png")
print("ok")
