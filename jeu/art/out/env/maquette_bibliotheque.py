#!/usr/bin/env python3
"""maquette_bibliotheque.py : mise en situation 192x352 de la Bibliothèque engloutie (procédure F6/F7).
P0 bg0_bibliotheque (décalé x32), P1 bg1_bibliotheque (décalé x16), bg2_bibliotheque en bandes x32-63 et x128-159
fermées par les piliers bg2_bord (D en x56-63, G en x128-135) ; murs : bas = transition depuis la Fonderie (y1/y0) ;
autel palette-swap + flamme ; héros idle au mur gauche. Usage : maquette_bibliotheque.py <hero.png> [fonderie]."""
from PIL import Image
import sys
D = "/home/user/Testing/jeu/art/out/env/"
HERO = sys.argv[1]
B = sys.argv[2] if len(sys.argv) > 2 else "bibliotheque"
im = lambda n: Image.open(D + n + ".png").convert("RGBA")
t = lambda img, x, y, w, h: img.crop((x, y, x + w, y + h))
W, H = 192, 352
out = Image.new("RGBA", (W, H), (0x0e, 0x0a, 0x1a, 255))
for n, dx in (("bg0_" + B, 32), ("bg1_" + B, 16)):
    L = im(n)
    for y in (0, 256):
        out.alpha_composite(t(L, dx, 0, W, 256), (0, y))
bg2 = im("bg2_" + B)
P = [t(bg2, i * 32, 0, 32, 32) for i in range(4)]
bord = im("bg2_bord"); bx = 32 if B == "bibliotheque" else 16
for x, seq in ((32, "0010203001200130"), (128, "0100300210020010")):
    for j, c in enumerate(seq[:11]):
        out.alpha_composite(P[int(c)], (x, j * 32))
for j in range(11):
    out.alpha_composite(t(bord, bx, 0, 8, 32), (56, j * 32))
    out.alpha_composite(t(bord, bx + 8, 0, 8, 32), (128, j * 32))
S = {}
for side in "LR":
    S["t", side] = im(f"wall_{B}_" + side); S["l", side] = im(f"wall_{B}_lit_" + side)
    S["d", side] = im(f"wall_{B}_deco_" + side); S["r", side] = im(f"rune_{B}_" + side)
    S["y", side] = im("wall_fonderie_to_bibliotheque_" + side); S["x", side] = im("wall_crypte_to_fonderie_" + side)
def col(x, side, seq):
    y = 0
    for s in seq.split():
        k, i = s[0], int(s[1:])
        h = 32 if k == "d" else 16
        out.alpha_composite(t(S[k, side], i * 16, 0, 16, h), (x, y)); y += h
if B == "bibliotheque":
    SEQ = ["t0 t2 t1 t4 l0 d0 l1 t3 t0 t5 t1 r1 t2 t0 t3 t1 t7 t2 t6 y1 y0",
           "t1 t3 t0 t2 d1 t0 t4 t1 t3 d2 t6 t2 r0 t1 t0 t5 t2 y1 y0",
           "t1 t3 t2 t0 t3 t1 t2 t0 t4 t3 t1 t0 t2 t3 t1 t0 t2 t5 t1 y1 y0",
           "t2 t0 t3 t1 t0 t2 t4 t1 t3 t0 t2 t1 d3 t0 t2 t1 t3 y1 y0"]
    alt = "altar_bibliotheque"
else:
    SEQ = ["y1 y0 t0 t2 t1 t4 l0 d0 l1 t3 t0 t5 t1 r1 t2 t0 t3 t1 t7 x1 x0",
           "y1 y0 t1 t3 t0 t2 d1 t0 t4 t1 t3 d2 t6 t2 r0 t1 t0 x1 x0",
           "y1 y0 t1 t3 t2 t0 t3 t1 t2 t0 t4 t3 t1 t0 t2 t3 t1 t0 t2 x1 x0",
           "y1 y0 t2 t0 t3 t1 t0 t2 t4 t1 t3 t0 t2 t1 d3 t0 t2 t1 x1 x0"]
    alt = "altar_fonderie"
col(16, "L", SEQ[0]); col(160, "R", SEQ[1]); col(0, "R", SEQ[2]); col(176, "L", SEQ[3])
fl = im("floor_start")
for i in range(12):
    out.alpha_composite(t(fl, 0 if i == 0 else 32 if i == 11 else 16, 0, 16, 16), (i * 16, 336))
out.alpha_composite(im(alt), (80, 304))
out.alpha_composite(t(im("altar_flame"), 16, 0, 8, 16), (92, 299))
out.alpha_composite(Image.open(HERO).convert("RGBA").crop((0, 0, 32, 32)), (22, 170))
nom = "maquette_" + B + ("_v2" if B == "fonderie" else "")
out.save(D + nom + ".png")
out.crop((6, 0, 186, H)).resize((180 * 3, H * 3), Image.NEAREST).save(D + nom + "_ecran@3.png")
print("ok", nom)
