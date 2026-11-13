#!/usr/bin/env python3
"""fx_assets.py : sources des FX d'ÉCHO, familles F2 (écho, gravure, autel) et F4 (collectibles, FX de mouvement).

Toutes les grilles sont dessinées à la main ci-dessous (1 caractère = 1 pixel, palette_v2).
Le script ne fait qu'assembler : placer une grille dans la cellule, recolorer or -> écho,
poser une étincelle dessinée à la main à une position choisie, écrire le .txt et rendre.
Seule exception : l'onde de gravure (anneau de rayon 0 -> 40) est rastérisée, comme la scie F3,
puis cassée en morceaux à la main (liste CUTS).

Usage : python3 art/src/fx/fx_assets.py [nom ...]
"""
import os
import sys
import math

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from pxlib import G, blank, pad, over, recolor, Writer, ROOT, GOLD2ECHO  # noqa: E402

W = Writer(HERE, os.path.join(ROOT, "game", "assets", "fx"), os.path.join(ROOT, "art", "out", "fx"))
REG = {}


def asset(fn):
    REG[fn.__name__] = fn
    return fn


# --- étincelles (règle E2-H : point -> croix 3 -> croix 5 -> croix 3 -> point -> rien) -------------
SPK_PT_W = G("W")
SPK_PT_Y = G("y")
SPK_X3 = G("""
.y.
yWy
.y.""")
SPK_X5 = G("""
..G..
..y..
GyWyG
..y..
..G..""")


def spark(base, kind, cx, cy):
    s = {"pt": SPK_PT_Y, "ptW": SPK_PT_W, "x3": SPK_X3, "x5": SPK_X5}[kind]
    r = len(s) // 2
    return over(base, s, cx - r, cy - r)


# =====================================================================================
# F4 : éclats d'or
# =====================================================================================
SH_FACE = G("""
........
...oo...
..oyGo..
.oyWGgo.
.oGGggo.
..oGgo..
...oo...
........""")
SH_TQ = G("""
........
...oo...
..oyGo..
..oyGo..
..oGgo..
..oGgo..
...oo...
........""")
SH_EDGE = G("""
........
...oo...
...yo...
...yo...
...Go...
...Go...
...oo...
........""")
SH_REV = G("""
........
...oo...
..oGyo..
..ogGo..
..oggo..
..oggo..
...oo...
........""")


@asset
def shard():
    fr = [SH_FACE, SH_TQ, SH_EDGE, spark(SH_REV, "pt", 6, 1), spark(SH_FACE, "x3", 6, 1), spark(SH_FACE, "pt", 6, 1)]
    W.write("shard", """
shard.png : 6 images 8x8, éclat d'or (gemme 6x6 g G y + cœur W, contour o), rotation + éclat.
0 face · 1 trois-quarts · 2 tranche · 3 revers + point · 4 face + croix 3 · 5 face + point.
Timing : 8 fps en boucle (125 ms). Pivot (4,4), centre de la gemme (3.5,3.5).
""", fr, 8, 8)


BIG = G("""
................
................
................
.......oo.......
......oyGo......
.....oyWGGo.....
....oyWyGGgo....
...oyyyGGGggo...
...oyGGGGgggo...
....oGGGgggo....
.....oGGggo.....
......oGgo......
.......oo.......
................
................
................""")


@asset
def shard_big():
    fr = [BIG, spark(BIG, "x3", 12, 3), spark(BIG, "x5", 12, 3), spark(BIG, "pt", 12, 3)]
    W.write("shard_big", """
shard_big.png : 4 images 16x16, gros éclat (gemme 10x10, facette W en diagonale, contour o).
0 repos · 1 croix 3 · 2 croix 5 · 3 point (scintillement en haut à droite, une étincelle à la fois).
Timing : 4 fps en boucle (250 ms). Pivot (8,8).
""", fr, 16, 16)


POP0 = pad(G("""
.oo.
oyGo
oGgo
.oo."""), 16, 16, 6, 6)
POP1 = pad(G("""
...oo...
..oyyo..
.oyWWyo.
oyWWWWyo
oyWWWWyo
.oyWWyo.
..oyyo..
...oo..."""), 16, 16, 4, 4)
POP2 = pad(G("""
...oooo...
..oyyyyo..
oyyWWWWyyo
oGGyyyyGGo
..oGGGGo..
...oooo..."""), 16, 16, 3, 5)
POP2 = over(POP2, G("y"), 3, 3)
POP2 = over(POP2, G("y"), 12, 3)
POP2 = over(POP2, G("y"), 3, 12)
POP2 = over(POP2, G("y"), 12, 12)
POP3 = blank(16, 16)
for (x1, y1, x2, y2) in [(1, 1, 2, 2), (14, 1, 13, 2), (1, 14, 2, 13), (14, 14, 13, 13)]:
    POP3 = over(POP3, G("y"), x1, y1)
    POP3 = over(POP3, G("G"), x2, y2)
POP4 = blank(16, 16)
for (x, y) in [(0, 0), (15, 0), (0, 15), (15, 15)]:
    POP4 = over(POP4, G("g"), x, y)


@asset
def shard_pop():
    W.write("shard_pop", """
shard_pop.png : 5 images 16x16, ramassage d'éclat : pop [E2-G] + 4 étincelles y.
0 gemme à 60 % (4x4) · 1 flash 130 % (8x8, cœur W) · 2 écrasée 10x6 + 4 étincelles naissantes
3 gemme partie, 4 traits y/G en diagonale · 4 4 points g aux coins, puis rien.
Timing : 40 · 50 · 60 · 70 · 80 ms (310 ms), une fois. Pivot (8,8) = centre de l'éclat ramassé.
""", [POP0, POP1, POP2, POP3, POP4], 16, 16)


# --- bulle de power-up + icônes ------------------------------------------------------
BUBBLE = G("""
....GGGG....
..GG....GG..
.G........G.
.G........G.
G..........G
G..........G
G..........G
G..........g
.G........g.
.G........g.
..GG....gg..
....GGgg....""")
REF_A = G("""
.W
y.
y.""")
REF_B = G("""
.y
W.
y.""")


def bub(dy, ref, dot):
    b = over(BUBBLE, ref, 2, 2)
    if dot:
        b = over(b, G("y"), 9, 8)
    return pad(b, 16, 16, 2, 2 + dy)


@asset
def powerup_bubble():
    fr = [bub(0, REF_A, False), bub(0, REF_A, True), bub(1, REF_B, False), bub(1, REF_B, True)]
    W.write("powerup_bubble", """
powerup_bubble.png : 4 images 16x16, bulle 12x12 contour G (bas droit g), intérieur transparent.
Reflet W/y en haut à gauche (glisse d'1 px en 2), petit reflet y en bas à droite (images 1, 3).
Flottement d'1 px : bulle en y=2 (images 0-1) puis y=3 (images 2-3).
Icône pu_* 8x8 posée en (4, 4 + dy), dy = 0,0,1,1. Timing : 4 fps en boucle (250 ms). Pivot (8,8).
""", fr, 16, 16)


PU_BURIN = G("""
......qq
.....qWq
....qecq
...qecq.
..qecq..
.qtcq...
.qtq....
..q.....""")
PU_PLUME = G("""
......ss
....sswp
...swwps
..swppls
..spls..
.slss...
.ls.....
l.......""")
PU_CALM = G("""
........
..JJ....
.j..j..j
j....jj.
........
..jj....
.U..U..U
U....UU.""")


@asset
def pu_icons():
    W.write("pu_burin", """
pu_burin.png : 1 image 8x8, icône Burin (lame d'écho c e, pointe W, contour q), posée dans la bulle.
""", [PU_BURIN], 8, 8)
    W.write("pu_plume", """
pu_plume.png : 1 image 8x8, icône Plume (plume claire w p l, contour s, tige l).
""", [PU_PLUME], 8, 8)
    W.write("pu_calm", """
pu_calm.png : 1 image 8x8, icône Accalmie (deux vagues figées de marée : J j puis U).
""", [PU_CALM], 8, 8)


# --- plume dorée -----------------------------------------------------------------------
FEATHER = G("""
................
...........oo...
..........oGyo..
.........oGyGo..
........oGyGgo..
.......oGyGgo...
......oGyGo.....
.....oGGygo.....
....oGGygo......
....oGygo.......
....oyo.........
...oyoo.........
..oyo...........
.oo.............
................
................""")
# inclinaison décidée rangée par rangée (dx par rangée 0-15) : seule la pointe (rangées 1-4)
# et le bout du tuyau (rangées 11-13) bougent, le milieu de la plume reste en place.
TILT = {
    "A": [0, -1, -1, -1, -1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0],
    "B": [0] * 16,
    "C": [0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, -1, -1, -1, 0, 0],
}


def feather_pose(t, dx, dy):
    out = blank(16, 16)
    for y, row in enumerate(FEATHER):
        out = over(out, [row], TILT[t][y] + dx, y + dy)
    return out


@asset
def feather_gold():
    seq = [("A", -1, 0), ("B", 0, 1), ("B", 1, 1), ("C", 2, 0), ("B", 1, 1), ("B", 0, 1)]
    W.write("feather_gold", """
feather_gold.png : 6 images 16x16, plume dorée en diagonale : tuyau y, barbes G (éclairées) / g, contour o.
Balancement de pendule en aller-retour : A (pointe redressée) · B · B · C (pointe couchée) · B · B.
Aux extrêmes la plume est 1 px plus haut, au passage du centre 1 px plus bas. dx : -1 0 +1 +2 +1 0.
Timing : 6 fps en boucle (166 ms). Pivot (8,8).
""", [feather_pose(*s) for s in seq], 16, 16)


# --- FX de mouvement -----------------------------------------------------------------
def stamp(points, w=16, h=16):
    g = blank(w, h)
    for (x, y, s) in points:
        g = over(g, [s], x, y)
    return g


# poussière de glissade : le mur est à gauche (x=0), la poussière monte et s'écarte.
# (x, y, pixels) : particules de 1-2 px, en groupes de 2-3, p puis l.
DUST = [
    [(1, 10, "pp"), (0, 12, "p"), (5, 6, "l"), (3, 11, "l"), (8, 4, "l")],
    [(3, 8, "pp"), (2, 10, "p"), (6, 5, "l"), (0, 13, "p")],
    [(5, 6, "l"), (3, 9, "l"), (1, 11, "pp"), (2, 13, "p")],
    [(7, 5, "l"), (3, 9, "pp"), (2, 12, "p"), (0, 14, "p")],
]


@asset
def fx_dust_wall():
    W.write("fx_dust_wall", """
fx_dust_wall.png : 4 images 16x16, poussière de glissade [A5-9] : p puis l, 1-2 px, groupes de 2-3.
Le mur est sur le bord GAUCHE de la cellule ; la poussière monte en s'écartant. Mur droit : flip_h.
Timing : 12 fps en boucle tant que le héros glisse (83 ms). Pivot (0,12) = point de contact main/mur.
""", [stamp(f) for f in DUST], 16, 16)


PUFF = [G("""
................
................
................
................
................
................
................
......ww........
.....pwwwp......
....pwwwwwp.....
.....ppwpp......
................
................
................
................
................"""), G("""
................
................
................
................
................
....pp...pp.....
...pwwp.pwwp....
...pwpl.pppl....
....ll...ll.....
......pp........
.....pwwl.......
......ll........
................
................
................
................"""), G("""
................
................
................
................
...l......l.....
..lpl....lpl....
...lm.....m.....
................
................
................
.....l.m........
......l.........
................
................
................
................"""), G("""
................
................
................
..m.............
...........m....
...m............
................
................
................
................
................
.......m........
................
................
................
................""")]


@asset
def fx_jump_puff():
    W.write("fx_jump_puff", """
fx_jump_puff.png : 4 images 16x16, bouffée de saut, du clair au sombre [E7-G].
0 nuage w bordé p · 1 se sépare en 3 bouffées p (cœurs w) · 2 bouffées l, bords m, plus haut
3 restes m en morceaux, puis rien. Timing : 50 · 70 · 90 · 110 ms, une fois. Pivot (8,9).
""", PUFF, 16, 16)


LAND = [G("""
................
................
................
................
w...............
w...............
ww..............
www.............
ww..............
w...............
w...............
................
................
................
................
................"""), G("""
................
................
....p...........
................
..p.............
................
...pp...........
w...............
....pp..........
................
..p.............
................
....p...........
................
................
................"""), G("""
.....l..........
................
................
...l............
................
.....l..........
................
......l.........
................
................
.....l..........
................
................
...l............
................
.....l.........."""), G("""
................
......m.........
................
................
................
................
................
.......m........
................
................
................
................
......m.........
................
................
................""")]


@asset
def fx_land():
    W.write("fx_land", """
fx_land.png : 4 images 16x16, impact sur le mur : 1 image de flash w, puis éclats p -> l -> m.
Le mur est sur le bord GAUCHE (x=0) ; mur droit : flip_h.
Timing : 40 (flash) · 60 · 80 · 100 ms, une fois. Pivot (0,7) = point d'impact.
""", LAND, 16, 16)


TURN = [G("""
................
................
................
................
................
.....yyyyyy.....
...yy......yy...
..y..........y..
..G..........G..
...GG......GG...
.....GGGGGG.....
................
................
................
................
................"""), G("""
................
................
................
................
....yyy..yyy....
..GG........GG..
.G............G.
G..............G
g..............g
.g............g.
..gg........gg..
....ggg..ggg....
................
................
................
................"""), G("""
................
................
................
................
................
..g..........g..
................
o..............o
................
................
..o..........o..
................
................
................
................
................""")]


@asset
def fx_turn():
    W.write("fx_turn", """
fx_turn.png : 3 images 16x16, volte : anneau ovale qui s'ouvre, haut y (éclairé), bas G.
0 anneau 12x6 plein · 1 anneau 16x8 ouvert en haut et en bas, G/g · 2 6 morceaux g/o, puis rien.
Timing : 50 · 70 · 90 ms, une fois. Pivot (8,8) = centre du héros.
""", TURN, 16, 16)
    W.write("fx_turn_echo", """
fx_turn_echo.png : 3 images 16x16, volte rechargée par l'écho : même dessin que fx_turn,
or -> écho (y -> e, G -> c, g -> t, o -> q). Timing et pivot identiques.
""", [recolor(f, GOLD2ECHO) for f in TURN], 16, 16)


@asset
def fx_graze():
    fr = [stamp([(8, 8, "w")]), stamp([(9, 6, "w"), (8, 7, "w"), (7, 8, "w")]), stamp([(10, 5, "w")])]
    W.write("fx_graze", """
fx_graze.png : 3 images 16x16, frôlé : étincelle w de 3 px, rien d'autre (GDD).
0 point · 1 trait diagonal 3 px · 2 point qui s'éloigne, puis rien.
Timing : 30 · 50 · 50 ms, une fois. Pivot (8,8) = point de frôlement.
""", fr, 16, 16)


# =====================================================================================
# F4 : pictogrammes d'onboarding (w, plis p l, contour k)
# La main reprend le dessin de art/src/sprites/tap.txt (même main partout).
# =====================================================================================
HAND_UP = G("""
.........kwpk...
.......kkkwpk...
......kwwwwppk..
.....kwwppppplk.
.....kwpplpplpk.
.....kwpppppppk.
.....kwppkkkkk..
.....kwppk......
.....kwppk......
.....kwppk......
.....kwppk......
......kkk.......""")
HAND_DOWN = G("""
.........kwpk...
.........kwpk...
.........kwpk...
.......kkkwpk...
......kwwwwppk..
.....kwwppppplk.
.....kwpplpplpk.
.....kwpppppppk.
.....kwppkkkkk..
.....kwppk......
.....kwppk......
.....kwppk......
.....kwppk......
......kkk.......""")
TAP_RING = G("""
..w.........w
.w...........w
.w...........w
..w.........w
...wwwwwwwwww""")


@asset
def pictos():
    tap1 = over(pad(HAND_DOWN, 16, 16), G("""
w.......w
.w.....w
.w.....w"""), 3, 11)
    W.write("picto_tap", """
picto_tap.png : 2 images 16x16, main qui tape (main de sprites/tap.txt), w p l contour k.
0 doigt levé · 1 doigt posé (2 px plus bas) + parenthèses d'impact w.
Timing : 400 · 300 ms en boucle ; effacement par morceaux géré par le moteur. Pivot (8,16) bas-centre.
""", [pad(HAND_UP, 16, 16), tap1], 16, 16)

    bar = G("""
kkkkkkkkkkkk
k..........k
kkkkkkkkkkkk""")
    hold = []
    for n in (2, 5, 8, 10):
        b = over(bar, ["w" * n], 1, 1)
        hold.append(over(pad(HAND_UP, 16, 16, 0, -1), b, 2, 13))
    W.write("picto_hold", """
picto_hold.png : 4 images 16x16, main tenue + barre de 0,28 s qui se remplit (w dans un cadre k).
Remplissage 2 · 5 · 8 · 10 px sur 10. Timing : 70 ms par image (0,28 s), puis tenir l'image 3.
Pivot (8,16).
""", hold, 16, 16)

    arrow0 = G("""
..kkkkk.....
.kwwwwwk....
kwkkkkkwk...
kwk...kwk...
kwk..kkwkk..
kwk.kwwwwwk.
.k...kwwwk..
......kwk...
.......k....""")
    arrow1 = G("""
..kkkkk.....
.kwwwwwk....
kwkkkkkwk...
kwk...kwk...
kwk...kwk...
kwk..kkwkk..
.k..kwwwwwk.
.....kwwwk..
......kwk...
.......k....""")
    hand_small = G("""
...kwpk
.kkkwpk
kwwwppk
kwppplk
kwppkk.
kwpk...
.kk....""")
    t0 = over(pad(arrow0, 16, 16, 0, 1), hand_small, 9, 9)
    t1 = over(pad(arrow1, 16, 16, 0, 1), hand_small, 9, 9)
    W.write("picto_turn", """
picto_turn.png : 2 images 16x16, main + flèche courbe (volte), w contour k.
La flèche tourne de gauche à droite puis plonge ; image 1 : pointe 1 px plus bas (pulsation).
Timing : 350 · 350 ms en boucle. Pivot (8,16).
""", [t0, t1], 16, 16)

    dia = G("""
..qq..
.qecq.
qeWctq
qcctq.
.qtq..
..q...""")
    dia = G("""
...q...
..qeq..
.qeWcq.
qecctq.
.qctq..
..qq...""")
    dia = G("""
..qq..
.qecq.
qeWctq
qcctq.
.qtq..
..q...""")
    e0 = over(pad(arrow0, 16, 16, 0, 1), dia, 9, 9)
    e1 = over(pad(arrow1, 16, 16, 0, 1), over(dia, G("W"), 2, 2), 9, 9)
    e1 = over(e1, G("e"), 15, 9)
    W.write("picto_echo", """
picto_echo.png : 2 images 16x16, losange d'écho (c e, cœur W, contour q) + flèche de volte w contour k.
Image 1 : pointe 1 px plus bas + point e au coin du losange (pulsation).
Timing : 350 · 350 ms en boucle. Pivot (8,16).
""", [e0, e1], 16, 16)


# =====================================================================================
# F2 : écho et gravure
# =====================================================================================
GLYPH = G("""
.qqqqq.
qqeeeqq
qeqqqeq
qeqeqeq
qeqqqeq
qqeeeqq
.qqqqq.""")


@asset
def fx_engrave_seal():
    f0 = pad(G("""
.q.
qeq
.q."""), 16, 16, 6, 6)
    f1 = pad(G("""
..qqqqq..
.qqeeeqq.
qqeqqqeqq
qeqqcqqeq
qeqcWcqeq
qeqqcqqeq
qqeqqqeqq
.qqeeeqq.
..qqqqq.."""), 16, 16, 3, 3)
    f2 = pad(G("""
.qqqqqqq.
qqeeeeeqq
qeqqWqqeq
qqeeeeeqq
.qqqqqqq."""), 16, 16, 3, 5)
    f3 = pad(GLYPH, 16, 16, 4, 4)
    W.write("fx_engrave_seal", """
fx_engrave_seal.png : 4 images 16x16, pop du sceau d'écho sur le piège [E2-G].
0 50 % (point e) · 1 115 % (anneau 9x9, cœur W c) · 2 écrasé 9x5 · 3 final = glyphe 7x7 (anneau e + point, fond q).
Timing : 50 · 60 · 60 ms puis tenir l'image 3 (elle sert d'état final). Pivot (7.5,7.5).
""", [f0, f1, f2, f3], 16, 16)


@asset
def grave():
    g = pad(GLYPH, 16, 16, 4, 4)
    fr = [g, over(g, G("W"), 7, 4), over(g, G("""
.e.
eWe
.e."""), 6, 3), over(g, G("e"), 7, 3)]
    W.write("grave", """
grave.png : 4 images 16x16, sceau gravé qui scintille (glyphe e 5x5 : anneau + point central, fond et contour q, sans halo).
0 repos · 1 la pointe du haut passe en W · 2 croix 3 e/W · 3 point e au-dessus, puis repos.
Timing : 2400 · 80 · 100 · 80 ms en boucle (un éclat toutes les ~2,7 s [E2-H]). Pivot (7.5,7.5).
""", fr, 16, 16)


ECHO_SH = [recolor(f, GOLD2ECHO) for f in (SH_FACE, SH_TQ, SH_EDGE, SH_REV)]


@asset
def echo_shard():
    fr = [over(ECHO_SH[0], G("e"), 6, 1), ECHO_SH[1], ECHO_SH[2], ECHO_SH[3]]
    W.write("echo_shard", """
echo_shard.png : 4 images 8x8, éclat d'écho au point de mort : même gemme que shard, or -> écho
(e c t + cœur W, contour q). 0 face + point e · 1 trois-quarts · 2 tranche · 3 revers.
Timing : 8 fps en boucle. Pivot (4,4). Fantôme à 50 % d'opacité si le moteur le souhaite (sinon 100 %).
""", fr, 8, 8)


@asset
def fx_echo_recharge():
    f0 = stamp([(1, 1, "e"), (14, 1, "e"), (1, 14, "e"), (14, 14, "e"),
                (2, 2, "c"), (13, 2, "c"), (2, 13, "c"), (13, 13, "c")])
    f1 = stamp([(4, 4, "e"), (11, 4, "e"), (4, 11, "e"), (11, 11, "e"),
                (5, 5, "c"), (10, 5, "c"), (5, 10, "c"), (10, 10, "c"),
                (2, 2, "t"), (13, 2, "t"), (2, 13, "t"), (13, 13, "t")])
    f2 = pad(G("""
...c...
...e...
...e...
ceeWeec
...e...
...e...
...c..."""), 16, 16, 4, 4)
    f3 = pad(G("""
...t...
.......
.t...t.
t..e..t
.t...t.
.......
...t..."""), 16, 16, 4, 4)
    W.write("fx_echo_recharge", """
fx_echo_recharge.png : 4 images 16x16, contact cyan : la volte se recharge.
0 4 traits e/c aux coins · 1 ils convergent (traînée t) · 2 croix 7 W/e/c au centre · 3 anneau de points t + cœur e.
Timing : 50 · 50 · 60 · 90 ms, une fois. Pivot (7.5,7.5) = centre du héros.
""", [f0, f1, f2, f3], 16, 16)


@asset
def fx_echo_trail():
    fr = [stamp([(3, 3, "ee"), (3, 4, "ec")], 8, 8),
          stamp([(3, 3, "c"), (4, 3, "e"), (4, 4, "c")], 8, 8),
          stamp([(4, 4, "c"), (2, 3, "t")], 8, 8),
          stamp([(4, 5, "t")], 8, 8)]
    W.write("fx_echo_trail", """
fx_echo_trail.png : 4 images 8x8, particule de traînée du fantôme-guide (c e), du clair au sombre.
0 bloc 2x2 e/c · 1 3 px c/e · 2 c + t qui se détache · 3 t seul qui tombe d'1 px, puis rien.
Timing : 60 ms par image, une fois ; une particule émise toutes les 2 images. Pivot (4,4).
""", fr, 8, 8)


def ring(r, th, colors, cuts=()):
    """Anneau rastérisé (centre 39.5,39.5) : pixels dont la distance est dans ]r-th, r]."""
    out = [["."] * 80 for _ in range(80)]
    for y in range(80):
        for x in range(80):
            d = math.hypot(x + 0.5 - 40, y + 0.5 - 40)
            if r - th < d <= r:
                a = (math.degrees(math.atan2(y + 0.5 - 40, x + 0.5 - 40)) + 360) % 360
                if any(a0 <= a < a1 for a0, a1 in cuts):
                    continue
                k = min(int((r - d) / th * len(colors)), len(colors) - 1)
                out[y][x] = colors[k]
    return ["".join(r) for r in out]


# morceaux effacés, décidés à la main (en degrés), image 4 et 5
CUTS4 = [(20, 34), (100, 112), (200, 216), (290, 300)]
CUTS5 = [(0, 18), (40, 70), (95, 125), (150, 170), (190, 230), (255, 275), (300, 340)]


@asset
def fx_engrave_wave():
    f0 = ring(4.5, 4.5, "Wee")
    f0 = over(f0, G("W"), 39, 39)
    fr = [f0,
          ring(12, 2.2, "ec"),
          ring(22, 2.2, "ec"),
          ring(30, 2.2, "ct"),
          ring(36, 1.2, "c", CUTS4),
          ring(39.5, 1.2, "t", CUTS5)]
    W.write("fx_engrave_wave", """
fx_engrave_wave.png : 6 images 80x80, onde de gravure (GDD §3.3, t = 0,63 s), rayon 0 -> 40.
0 disque r4 W/e · 1 anneau r12 2 px e/c · 2 r22 e/c · 3 r30 c/t · 4 r36 1 px c, 4 trous · 5 r40 1 px t en morceaux.
Anneau rastérisé (cercle exact, centre 40,40), trous choisis à la main (CUTS4, CUTS5).
Timing : 40 · 50 · 60 · 70 · 80 · 90 ms (390 ms), une fois. Pivot (40,40) = point d'impact.
""", fr, 80, 80)


# --- éclatement de mort (volutes) ------------------------------------------------------
CURL = {
    "a": G("""
.II
I..
.i."""),
    "b": G("""
iH.
..i
.H."""),
    "c": G("""
.H
h.
.h"""),
    "d": G("""
h.
.h"""),
}


def curls(placements):
    g = blank(32, 32)
    for (k, x, y) in placements:
        g = over(g, CURL[k] if k in CURL else [k], x, y)
    return g


@asset
def fx_death_burst():
    f0 = pad(G("""
..WW..
.WWWW.
WWWWWW
WWWWWW
.WWWW.
..WW.."""), 32, 32, 13, 13)
    f1 = curls([("a", 15, 9), ("a", 21, 12), ("a", 20, 19), ("a", 14, 21), ("a", 9, 17), ("a", 9, 11),
                ("o", 16, 15), ("a", 13, 16) if False else ("a", 16, 15)])
    f1 = curls([("a", 15, 9), ("a", 21, 12), ("a", 20, 19), ("a", 14, 21), ("a", 9, 17), ("a", 9, 11),
                ("o", 15, 15), ("a", 17, 16)])
    f2 = curls([("b", 15, 6), ("b", 23, 10), ("b", 22, 20), ("b", 13, 23), ("b", 6, 18), ("b", 7, 9),
                ("o", 18, 14), ("a", 13, 17)])
    f3 = curls([("c", 16, 3), ("c", 26, 8), ("c", 25, 20), ("c", 12, 25), ("c", 4, 19), ("c", 5, 6)])
    f4 = curls([("d", 16, 1), ("d", 28, 6), ("h", 27, 21), ("d", 11, 27), ("h", 3, 20), ("d", 3, 4)])
    f5 = curls([("h", 17, 0), ("h", 29, 4), ("h", 10, 29)])
    W.write("fx_death_burst", """
fx_death_burst.png : 6 images 32x32, volutes séparées du corps (si le moteur les détache du héros).
0 flash W 6x6 (1 image) · 1 6 volutes I/i + 2 éclats corail o a · 2 volutes i/H plus loin
3 volutes H/h · 4 morceaux h · 5 3 pixels h, puis rien. Du clair au sombre, effacement par morceaux [E7-G].
Timing : 33 · 80 · 90 · 100 · 110 · 120 ms, une fois. Pivot (16,16) = centre du héros.
""", [f0, f1, f2, f3, f4, f5], 32, 32)


# --- particules génériques -------------------------------------------------------------
@asset
def fx_spark():
    fr = [stamp([(3, 3, "y")], 8, 8), spark(blank(8, 8), "x3", 3, 3), spark(blank(8, 8), "x5", 3, 3),
          spark(blank(8, 8), "x3", 3, 3), stamp([(3, 3, "G")], 8, 8)]
    W.write("fx_spark", """
fx_spark.png : 5 images 8x8, étincelle d'or générique [E2-H] : point y -> croix 3 -> croix 5 -> croix 3 -> point G -> rien.
Timing : 60 ms par image, une fois. Pivot (3.5,3.5). Version écho : recolorer y->e, G->c, W reste W.
""", fr, 8, 8)


# --- autel (allumé / éteint) + flamme cyan ---------------------------------------------
ALTAR = G("""
................................
................................
................................
................................
................................
................................
................................
................................
.......kkkkkkkkkkkkkkkkkk.......
......kllllllllllllllllllk......
......klmbbbbbbbbbbbbbbmsk......
......kmmmmmmmmmmmmmmmmssk......
.......ksssssssssssssssnk.......
........kkkkkkkkkkkkkkkk........
..........kmmmmmmmmmsnk.........
..........klmmmmmmmssnk.........
.......kkkkkkkkkkkkkkkkkk.......
.......kllllllllllllllllk.......
.......klmmmmmmmmmmmmmssk.......
.......klmmmmmmmmmmmmmssk.......
.......klmmmmmmmmmmmmmssk.......
.......klmmmmmmmmmmmmmssk.......
.......klmmmmmmmmmmmmmssk.......
.......klmmmmmmmmmmmmmssk.......
.......klmmmmmmmmmmmmmssk.......
.......klmmmmmmmmmmmmmssk.......
.......knnnnnnnnnnnnnnnnk.......
.....kkkkkkkkkkkkkkkkkkkkkk.....
.....klllllllllllllllllllsk.....
.....kmmmmmmmmmmmmmmmmmmssk.....
.....knnnnnnnnnnnnnnnnnnnnk.....
.....kkkkkkkkkkkkkkkkkkkkkk.....""")
ALTAR_GLYPH_OFF = G("""
.nnn.
n...n
n.n.n
n...n
.nnn.""")
ALTAR_GLYPH_ON = G("""
.eee.
e...e
e.W.e
e...e
.eee.""")
ALTAR_LIT = G("""
...tccccccccccct
...ttttqqqtttt
""")


@asset
def altar():
    off = over(ALTAR, ALTAR_GLYPH_OFF, 13, 19)
    on = over(ALTAR, ALTAR_GLYPH_ON, 13, 19)
    # lumière de la flamme sur les dessus : bord de vasque et fond de vasque (décidé au pixel)
    on = over(on, G(".....pppeeeeppp"), 8, 9)
    on = over(on, G("qqqqtttttqqqq"), 9, 10)
    on = over(on, G(".....pppp"), 9, 17)
    W.write("altar", """
altar.png : 2 images 32x32, autel d'écho en pierre neutre (k n s m l, lumière haut-gauche).
0 éteint : vasque b, glyphe creusé n (anneau + point) · 1 allumé : glyphe e + cœur W, fond de vasque q/t,
bord de vasque et dessus du fût éclairés par la flamme (p, e). Pas une animation : 2 états.
Pivot (16,32) bas-centre. Flamme altar_flame posée en (12,-5) depuis le coin haut-gauche de l'autel
(sa base, rangée 15, tombe dans la vasque, rangée 10).
""", [off, on], 32, 32)


FLAMES = [G("""
........
........
........
....q...
...qcq..
...qeq..
..qcecq.
..qeWcq.
.qceWecq
.qcWWecq
.qcWWecq
.qceWecq
..qceccq
..qtcctq
...qttq.
....qq.."""), G("""
........
........
...q....
..qcq...
..qeq...
..qecq..
..qeecq.
.qceWcq.
.qceWecq
.qcWWecq
.qcWWecq
.qceWecq
..qceccq
..qtcctq
...qttq.
....qq.."""), G("""
..e.....
........
..q.....
..qq....
.qcq....
.qecq...
.qeccq..
.qceWcq.
.qceWecq
.qcWWecq
.qcWWecq
.qceWecq
..qceccq
..qtcctq
...qttq.
....qq.."""), G("""
........
........
........
........
....q...
...qcq..
...qeq..
..qcecq.
.qceWecq
.qcWWecq
.qcWWecq
.qceWecq
..qceccq
..qtcctq
...qttq.
....qq.."""), G("""
........
........
........
.....q..
....qcq.
....qeq.
...qecq.
..qceeq.
.qceWecq
.qcWWecq
.qcWWecq
.qceWecq
..qceccq
..qtcctq
...qttq.
....qq.."""), G("""
.....e..
........
.....q..
....qq..
....qcq.
...qceq.
..qcceq.
.qcWecq.
.qceWecq
.qcWWecq
.qcWWecq
.qceWecq
..qceccq
..qtcctq
...qttq.
....qq..""")]


@asset
def altar_flame():
    W.write("altar_flame", """
altar_flame.png : 6 images 8x16, flamme cyan de l'autel (cœur W, e, c, base t, contour q).
0 droite · 1 pointe à gauche · 2 haute à gauche + braise e détachée · 3 basse · 4 pointe à droite
5 haute à droite + braise. La base (rangées 8-15) ne bouge pas : seule la pointe vacille.
Timing : 10 fps en boucle (100 ms). Pivot (4,16) bas-centre.
""", FLAMES, 8, 16)


# =====================================================================================
# P1 F4
# =====================================================================================
@asset
def pu_p1():
    W.write("pu_magnet", """
pu_magnet.png : 1 image 8x8, icône Aimant (fer à cheval R/r, pôles w, contour k).
""", [G("""
.kkkkkk.
kRRRRrrk
kRk..krk
kRk..krk
kRk..krk
kwk..kwk
kwk..kwk
.k....k.""")], 8, 8)
    W.write("pu_lantern", """
pu_lantern.png : 1 image 8x8, icône Lanterne (cage s m, flamme a A, contour k).
""", [G("""
...kk...
..kssk..
.kmmmsk.
.kmaAmk.
.kmAamk.
.kmaamk.
.kssssk.
..kkkk..""")], 8, 8)
    W.write("pu_gold", """
pu_gold.png : 1 image 8x8, icône Pluie d'or (trois éclats g G y, contour o).
""", [G("""
.oo.....
oyGo.oo.
oGgooyGo
.oo.oGgo
..oo.oo.
.oyGo...
.oGgo...
..oo....""")], 8, 8)
    arcs = [G("""
................
................
................
................
....G......G....
...G........G...
...G........G...
....G......G....
................
................"""), G("""
................
................
................
..G..........G..
.G............G.
.G............G.
.G............G.
..G..........G..
................"""), G("""
................
................
G..............G
................
g..............g
g..............g
................
G..............G""")]
    W.write("fx_magnet", """
fx_magnet.png : 3 images 16x16, aimant actif : deux paires d'arcs G qui s'écartent du héros puis s'éteignent (g).
Timing : 100 ms par image en boucle. Pivot (8,6) = centre du héros.
""", [pad(a, 16, 16, 0, 1) for a in arcs], 16, 16)
    W.write("lantern_flame", """
lantern_flame.png : 4 images 8x8, flamme de lanterne (A a o, contour r). Pointe qui vacille.
Timing : 10 fps en boucle. Pivot (4,8).
""", [G("""
........
...r....
..rAr...
..rAar..
.raAaor.
.raAaor.
..rooar.
...rrr.."""), G("""
........
....r...
...rAr..
..rAar..
.raAaor.
.raAaor.
..rooar.
...rrr.."""), G("""
...r....
..rAr...
..rAr...
.raAar..
.raAaor.
.raAaor.
..rooar.
...rrr.."""), G("""
........
........
...rr...
..rAar..
.raAaor.
.raAaor.
..rooar.
...rrr..""")], 8, 8)
    rel = G("""
........
...kk...
..klmk..
.klGGmk.
.kmGgsk.
..kmsk..
...kk...
........""")
    W.write("relic_fragment", """
relic_fragment.png : 4 images 8x8, fragment de relique : pierre m l, cœur G, contour k.
0 repos · 1 cœur y · 2 point W au coin · 3 repos sans point. Timing : 6 fps en boucle. Pivot (4,4).
""", [rel, over(rel, G("yy"), 3, 3), over(over(rel, G("yy"), 3, 3), G("W"), 6, 1), rel], 8, 8)
    moon = recolor(BIG, {"y": "W", "G": "w", "g": "p", "o": "l"})
    W.write("moon_shard", """
moon_shard.png : 4 images 16x16, éclat de lune : gemme de shard_big recolorée w W + bord p, contour l.
Scintillement identique à shard_big, étincelle W/w/p. Timing : 4 fps. Pivot (8,8).
""", [moon] + [recolor(spark(BIG, k, 12, 3), {"y": "W", "G": "w", "g": "p", "o": "l"}) for k in ("x3", "x5", "pt")],
        16, 16)


def main(names):
    todo = names or list(REG)
    for n in todo:
        REG[n]()
        print("ok", n)


if __name__ == "__main__":
    main(sys.argv[1:])
