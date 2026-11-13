#!/usr/bin/env python3
"""tide_assets.py : sources de la marée et de l'eau d'ÉCHO (F5).

Grilles dessinées à la main. Le script assemble seulement : défilement bouclé de la crête
(8 px par image sur une tuile de 32), écriture des .txt, rendu par tools/px.py et planche.py.
Les halos additifs utilisent j avec une opacité fixe (couleurs locales #RRGGBBAA, mêmes RVB que palette_v2).

Usage : python3 art/src/tide/tide_assets.py [nom ...]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "fx"))
from pxlib import G, blank, over, wrapx, Writer, ROOT  # noqa: E402

W = Writer(HERE, os.path.join(ROOT, "game", "assets", "tide"), os.path.join(ROOT, "art", "out", "tide"))
REG = {}


def asset(fn):
    REG[fn.__name__] = fn
    return fn


CREST = G("""
.....JJJ.................jJJ....
...JJjjjJJ.............JjjjJ....
.JJjjUUUjjJJ.........JJjjUUjjJJ.
JjjUUUUUUUjjJJJ...JJJjjUUUUUUjjJ
jUUUUUUUUUUUjjjJJJjjjUUUUUUUUUUj
UUUUUUUUUUUUUUUjjjUUUUUUUUUUUUUU
UUUUuuUUUUUUUUUUjUUUUUUUuuUUUUUU
UUuuuuuUUUUuuUUUUUUUuuuuuuUUUUuU
uuuuuuuuuUUUuuuuuuUUUUuuuuuuuuuu
uuuUUuuuuuuuuuuuuuuuuuuUUUuuuuuu
uuuuuuuuuuuuuUUuuuuuuuuuuuuuuuuu
uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu
uuuuuuUUuuuuuuuuuuuuuuuuuuUUuuuu
uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu
uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu
uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu""")


@asset
def tide_crest():
    fr = [wrapx(CREST, 8 * i) for i in range(4)]
    W.write("tide_crest", """
tide_crest.png : 4 images 32x16, crête de la marée (tuile horizontale bouclable, se répète sur 192 px).
Écume J / crête j / corps U puis u ; la rangée 15 est en u pur et se raccorde à tide_body.
Les 4 images = la même crête qui défile de 8 px vers la droite (boucle exacte sur 32 px). Cycle de palette [E7-H] : 4 états, 150 ms par image en boucle.
Accalmie : appliquer pal_tide_calm (j -> J) et figer l'image courante.
Pivot : bord haut-gauche ; la crête monte avec la marée (y = niveau de la marée - 5).
""", fr, 32, 16)


BODY_DASH = [(3, 1, 3), (19, 3, 2), (11, 6, 4), (27, 8, 3), (5, 11, 2), (16, 13, 3), (24, 17, 2),
             (1, 19, 4), (12, 21, 2), (20, 24, 3), (7, 26, 3), (29, 28, 3), (14, 30, 2)]


@asset
def tide_body():
    g = ["u" * 32 for _ in range(32)]
    for (x, y, n) in BODY_DASH:
        row = list(g[y])
        for k in range(n):
            row[(x + k) % 32] = "U"
        g[y] = "".join(row)
    W.write("tide_body", """
tide_body.png : 1 image 32x32, tuile du corps de la marée (u, traits U de 2-4 px placés à la main,
bouclable en x et en y). Le cycle u <-> U est fait dans le shader (pas d'animation dans la tuile).
""", [g], 32, 32)


GLOW = G("""
%%%%%%%%%%%%..............%%%%%%
%%%%%%%%%%%%%%%%......%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%&&&&&&%%%%%%%%%%%%%%%%%&&&%%
%%&&&&&&&&&&&%%%%%%%%%%&&&&&&&&&
&&&&&&&&&&&&&&&&&%%%&&&&&&&&&&&&
&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
&&&&&&++++++&&&&&&&&&&&&&&&+++&&
&&&++++++++++++&&&&&&&&&+++++++&
++++++++++++++++++&&&+++++++++++
++++++++++++++++++++++++++++++++
++++++++++++++++++++++++++++++++
++++++++++++++++++++++++++++++++
++++++++++++++++++++++++++++++++
++++++++++++++++++++++++++++++++
++++++++++++++++++++++++++++++++""")


@asset
def tide_glow():
    W.write("tide_glow", """
tide_glow.png : 1 image 32x16, halo de la marée en 3 paliers durs (pas de dégradé) :
j à 12 % (haut) / 22 % / 35 % (bas, contre la crête). Bords en vagues larges, bouclable en x.
À dessiner en mode ADDITIF (CanvasItemMaterial blend_mode = Add), juste au-dessus de tide_crest
(bas du halo = haut de la crête). Défile avec la crête ou reste fixe : les deux bouclent.
""", [GLOW], 32, 16, local={"%": "#bd69db1f", "&": "#bd69db38", "+": "#bd69db59"})


@asset
def pal_tide_calm():
    W.write("pal_tide", """
pal_tide.png : 4x1, palette de référence de la marée, ordre u U j J (entrée de l'échange de palette).
""", [["uUjJ"]], 4, 1)
    W.write("pal_tide_calm", """
pal_tide_calm.png : 4x1, palette d'Accalmie : u U J J (la crête j passe à J, §8.4). Même ordre que pal_tide.
Pendant l'Accalmie, tide_crest est figée sur son image courante.
""", [["uUJJ"]], 4, 1)


def surf(shift):
    bumps = {(b + shift) % 16 for b in (2, 3, 10, 11)}
    r0 = "".join("9" if x in bumps else "." for x in range(16))
    r1 = "".join("0" if x in bumps else "9" for x in range(16))
    return [r0, r1] + ["0" * 16 for _ in range(14)]


@asset
def water():
    W.write("water_surface", """
water_surface.png : 4 images 16x16, surface d'eau O18 : ligne 9 ondulée d'1 px (bosses de 2 px, période 8),
fond 0. Les bosses avancent de 2 px par image (boucle exacte). Tuile bouclable en x.
Timing : 200 ms par image (cycle de palette O18). Pivot : haut-gauche, ligne d'eau en y = 1.
""", [surf(2 * i) for i in range(4)], 16, 16)
    body = ["0" * 16 for _ in range(16)]
    body = over(body, ["99"], 3, 4)
    body = over(body, ["999"], 10, 9)
    body = over(body, ["99"], 5, 13)
    W.write("water_body", """
water_body.png : 1 image 16x16, eau profonde 0 + 3 traits de caustique 9 (1 px de haut), bouclable en x et y.
Les caustiques suivent le cycle de palette 0/9 (4 états, 200 ms) côté shader.
""", [body], 16, 16)
    fr = [over(blank(8, 8), ["p"], 3, 5),
          over(blank(8, 8), G(".p.\np.w\n.p."), 2, 3),
          over(blank(8, 8), G("p...p\n.....\n.....\n.....\np...p"), 1, 1)]
    W.write("bubble", """
bubble.png : 3 images 8x8, bulle d'eau p (O18). 0 point · 1 anneau 3x3 + reflet w · 2 éclate en 4 points.
Timing : 0 et 1 en boucle (300 ms) pendant la montée, 2 (80 ms) à la surface. Pivot (4,4).
""", fr, 8, 8)


@asset
def tide_p1():
    fr = [over(blank(8, 8), ["U"], 4, 6), over(blank(8, 8), ["j"], 4, 5),
          over(blank(8, 8), G(".J.\nJjJ\n.J."), 3, 3), over(blank(8, 8), ["j"], 4, 2)]
    W.write("tide_motes", """
tide_motes.png : 4 images 8x8, particule qui monte de la marée : U -> j -> croix J/j -> j, 1 px plus haut à chaque image.
Timing : 120 ms par image, une fois ; la particule se dessine au-dessus de tide_glow. Pivot (4,8).
""", fr, 8, 8)
    chev = G("""
.......JJ.......
......JjjJ......
.....JjUUjJ.....
....JjU..UjJ....
...JjU....UjJ...
..JjU......UjJ..
..jU........Uj..
................
.......JJ.......
......JjjJ......
.....JjUUjJ.....
....JjU..UjJ....
...JjU....UjJ...
..JjU......UjJ..
..jU........Uj..
................""")
    dim = [r.replace("J", "j").replace("U", "u") for r in chev]
    W.write("tide_warning", """
tide_warning.png : 2 images 16x16, alerte « la marée monte » : double chevron J j U vers le haut.
0 allumé (J) · 1 éteint (j/u). Timing : 250 ms par image en boucle. Pivot (8,16), posé au bas de l'écran.
""", [chev, dim], 16, 16)


def main(names):
    for n in names or list(REG):
        REG[n]()
        print("ok", n)


if __name__ == "__main__":
    main(sys.argv[1:])
