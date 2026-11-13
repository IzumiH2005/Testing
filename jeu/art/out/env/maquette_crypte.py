#!/usr/bin/env python3
"""maquette_crypte.py : mise en situation 192x352 de la Crypte (procédure F6/F7).
Plans : bg0 (P0) + bg1 (P1) plein cadre ; bg2 (P2) en deux bandes x32-63 et x128-159 (le centre s'ouvre sur P0/P1) ;
murs : colonne intérieure gauche x16 = tuiles L, extérieure x0 = tuiles R ; intérieure droite x160 = R, extérieure x176 = L ;
sol de départ en bas, autel + flamme, héros idle accroché au mur gauche (prise x=7 de la cellule -> cellule x=25).
Sortie : maquette_crypte.png (x1), @3, et _ecran (recadrage 180 px de la caméra, x6-185)."""
from PIL import Image
import sys
D = "/home/user/Testing/jeu/art/out/env/"
HERO = sys.argv[1] if len(sys.argv) > 1 else "/tmp/hero_idle.png"
im = lambda n: Image.open(D + n + ".png").convert("RGBA")
W, H = 192, 352
out = Image.new("RGBA", (W, H), (0, 0, 0, 255))
bg0, bg1 = im("bg0_crypte"), im("bg1_crypte")
off0, off1 = 40, 120  # décalages de parallaxe arbitraires
for y in range(-256, H + 256, 256):
    out.alpha_composite(bg0, (-30, y - off0 % 256))
    out.alpha_composite(bg1, (-34, y - off1 % 256))
bg2, dec2 = im("bg2_crypte"), im("bg2_crypte_deco")
t = lambda img, x, y, w, h: img.crop((x, y, x + w, y + h))
T2 = [t(bg2, 0, 0, 32, 16), t(bg2, 0, 16, 32, 16)]
B32 = [t(bg2, 32, 0, 32, 32), t(bg2, 64, 0, 32, 32), t(bg2, 96, 0, 32, 32)]
for col, seq in ((32, "AABAAcAAAAaABAAAAbAAAAA"), (128, "AAAAbAAAAAAcAAAAAaAAAAA")):
    y = 0
    for ch in seq:
        if y >= H: break
        if ch == "A": out.alpha_composite(T2[(y // 16) % 2 if col == 32 else 0], (col, y)); y += 16
        elif ch == "B": out.alpha_composite(T2[1], (col, y)); y += 16
        else:
            out.alpha_composite(B32["abc".index(ch)], (col, y)); y += 32
out.alpha_composite(t(dec2, 0, 0, 32, 32), (128, 64))
out.alpha_composite(t(dec2, 64, 0, 32, 32), (32, 208))
L, R = im("wall_crypte_L"), im("wall_crypte_R")
lit = {"L": im("wall_crypte_lit_L"), "R": im("wall_crypte_lit_R")}
deco = {"L": im("wall_crypte_deco_L"), "R": im("wall_crypte_deco_R")}
rune = {"L": im("rune_crypte_L"), "R": im("rune_crypte_R")}
tr = {"L": im("wall_crypte_to_fonderie_L"), "R": im("wall_crypte_to_fonderie_R")}
base = {"L": L, "R": R}
def col(x, side, seq):
    y = 0
    for s in seq:
        k, i = s[0], int(s[1:]) if len(s) > 1 else 0
        if k == "t": out.alpha_composite(t(base[side], i * 16, 0, 16, 16), (x, y)); y += 16
        elif k == "l": out.alpha_composite(t(lit[side], i * 16, 0, 16, 16), (x, y)); y += 16
        elif k == "r": out.alpha_composite(t(rune[side], i * 16, 0, 16, 16), (x, y)); y += 16
        elif k == "x": out.alpha_composite(t(tr[side], i * 16, 0, 16, 16), (x, y)); y += 16
        elif k == "d": out.alpha_composite(t(deco[side], i * 16, 0, 16, 32), (x, y)); y += 32
SEQ_LI = "x1 x0 t0 t2 t1 t4 l0 d0 l1 t3 t0 t5 t1 r0 t2 t0 t3 t1 t7 t0 t2".split()
SEQ_RI = "x1 x0 t1 t3 t0 t2 d1 t0 t4 t1 t3 d2 t6 t2 r1 t1 t0 t3 t2".split()
SEQ_LO = "x1 x0 t1 t3 t2 t0 t3 t1 t2 t0 t4 t3 t1 t0 t2 t3 t1 t0 t2 t1 t3".split()
SEQ_RO = "x1 x0 t2 t0 t3 t1 t0 t2 t4 t1 t3 t0 t2 t1 t5 t3 t0 t2 t1 t0 t3".split()
col(16, "L", SEQ_LI); col(0, "R", SEQ_LO); col(160, "R", SEQ_RI); col(176, "L", SEQ_RO)
fl = im("floor_start")
for i in range(12):
    out.alpha_composite(t(fl, 0 if i == 0 else 32 if i == 11 else 16, 0, 16, 16), (i * 16, 336))
alt, fla = im("altar"), im("altar_flame")
out.alpha_composite(alt, (80, 304))
out.alpha_composite(t(fla, 0, 0, 8, 16), (92, 299))
hero = Image.open(HERO).convert("RGBA").crop((0, 0, 32, 32))
out.alpha_composite(hero, (22, 170))  # face du mur à x=10 de la cellule (bible §13)
out.save(D + "maquette_crypte.png")
out.resize((W * 3, H * 3), Image.NEAREST).save(D + "maquette_crypte@3.png")
out.crop((6, 0, 186, H)).resize((180 * 3, H * 3), Image.NEAREST).save(D + "maquette_crypte_ecran@3.png")
print("ok")
