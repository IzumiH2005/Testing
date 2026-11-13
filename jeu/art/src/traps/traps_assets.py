#!/usr/bin/env python3
"""Grilles des pièges F3 et créatures F11 d'ÉCHO (dessinées à la main, 1 caractère = 1 pixel).

python3 art/src/traps/traps_assets.py            -> régénère tout
python3 art/src/traps/traps_assets.py spikes saw -> seulement ces assets
"""
import math
import sys
from gen_traps import G, pad, over, recolor, write, asset, REGISTRY, ECHO

# ======================================================================= 1. ÉPINES
# Mur gauche : x=0 de la cellule = face du mur (WL). Les dents pointent vers la droite.
# Deux dents de 8 px par tuile, flancs à 45° (escalier 1-1-1-1 régulier), profondeur 5 (x 0-4) + contour k en x=5.
SPIKE = G("""
xk
xzk
xXzk
xXXzk
xXXzZk
xXXxk
xXxk
xxk
xk
xzk
xXzk
xXXzk
xXXzZk
xXXxk
xXxk
xxk
""")


@asset
def spikes():
    base = pad(SPIKE, 16, 16)
    # éclat en escalier sur la pointe de la dent haute (4,4) : point -> croix 3 -> croix 5 -> croix 3
    f1 = over(base, ["W"], 4, 4)
    f2 = over(base, G(".Z.\nZWZ\n.Z."), 3, 3)
    f3 = over(base, G("..Z..\n..W..\nZWWWZ\n..W..\n..Z.."), 2, 2)
    f4 = over(base, G(".z.\nzZz\n.z."), 3, 3)
    write("spikes", """
ÉCHO - O1 épines, mur GAUCHE (le moteur retourne l'image pour le mur droit). Cellule 16x16, 5 images.
Intention : « ça coupe, ne touche pas ce mur » lu en 0,2 s ; 2 dents de 8 px par tuile qui se raccordent à l'infini.
Géométrie : profondeur létale 5 px (x 0-4, = hz.gd Rect2(WL, y0+2, 5, ...)) ; contour k en x=5 (1 px de dépassement, §9.1).
Lumière haut-gauche : flanc haut des dents en z, flanc bas en x, cœur Z d'1 px sur la pointe haute ; x en x=0 = lueur sur le mur.
Timing (E3) : img | rôle | change | principe | durée
  0 | repos | - | tenue | 2 s (éclat toutes les 2 s)
  1 | départ éclat | point W | anticipation | 1/12 s
  2 | montée | croix 3 W/Z | accélération | 1/12 s
  3 | pic | croix 5 | extrême | 1/12 s
  4 | déclin | croix 3 Z/z | ralenti | 1/12 s  puis retour à 0
Budget : k x X z Z (+ W pour l'éclat) = 6 couleurs.
Défaut corrigé : v0 en 4 dents de 4 px = flancs en escalier 2-1-2 (jaggies) ; passé à 2 dents de 8 px à 45°.
""", [base, f1, f2, f3, f4], 16, 16)


@asset
def spikes_echo():
    # cristal accrochable : pointes émoussées d'1 px (plateau de 3 px à x=3), contour q
    g = G("""
qq
qcq
qtcq
qttcq
qtteq
qttcq
qttq
qtq
qq
qcq
qtcq
qttcq
qtteq
qttcq
qttq
qtq
""")
    write("spikes_echo", """
ÉCHO - O1 épines gravées (écho) : cristal accrochable, pointes émoussées d'1 px. Mur GAUCHE, 16x16, 1 image.
Intention : la même dent, mais sans danger : plateau de 3 px au lieu d'une pointe, rampe cyan, contour q (recul de lecture).
Timing : statique (le glyphe gravé est un autre asset).
Budget : q t c e = 4 couleurs (aucun magenta).
Défaut corrigé : la pointe e isolée faisait un orphelin ; elle est encadrée par c au-dessus et au-dessous.
""", [pad(g, 16, 16)], 16, 16)


# ======================================================================= 2. SCIE
def saw_frame(rot):
    """Rastérise la scie : disque r 6 (hitbox), 6 dents en cliquet jusqu'à r ~9,5, moyeu Z, 3 trous x."""
    C = 12
    body = {}
    for y in range(24):
        for x in range(24):
            dx, dy = x - C, y - C
            r = math.hypot(dx, dy)
            a = math.atan2(dy, dx)
            u = ((a - rot) * 6 / (2 * math.pi)) % 1.0
            rt = 6.4 + 3.2 * (1 - u)
            if r <= 6.4:
                body[(x, y)] = "disc"
            elif r <= rt:
                body[(x, y)] = "tooth"
    grid = [["."] * 24 for _ in range(24)]
    for (x, y), kind in body.items():
        dx, dy = x - C, y - C
        r = math.hypot(dx, dy)
        if kind == "tooth":
            grid[y][x] = "z" if (dx + dy) < -2 else ("x" if (dx + dy) > 3 else "X")
        else:
            if r > 5.4:
                grid[y][x] = "z" if (dx + dy) < -1 else ("x" if (dx + dy) > 1 else "X")
            else:
                grid[y][x] = "X"
    # trous qui tournent
    for k in range(3):
        a = rot + k * 2 * math.pi / 3 + math.pi / 6
        hx, hy = round(C + 3.4 * math.cos(a)), round(C + 3.4 * math.sin(a))
        grid[hy][hx] = "x"
    # moyeu
    for (x, y) in [(C, C - 1), (C - 1, C), (C, C), (C + 1, C), (C, C + 1)]:
        grid[y][x] = "Z"
    grid[C][C] = "W"
    # contour k (4-voisins)
    out = [r[:] for r in grid]
    for y in range(24):
        for x in range(24):
            if grid[y][x] == ".":
                for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if 0 <= nx < 24 and 0 <= ny < 24 and grid[ny][nx] != ".":
                        out[y][x] = "k"
                        break
    return ["".join(r) for r in out]


SAW_FIX = {}  # retouches à la main par image : {frame: [(x, y, ch), ...]}


def saw_frames():
    fr = []
    for f in range(4):
        g = saw_frame(-f * (2 * math.pi / 6) / 4)
        rows = [list(r) for r in g]
        for x, y, ch in SAW_FIX.get(f, []):
            rows[y][x] = ch
        fr.append(["".join(r) for r in rows])
    return fr


@asset
def saw():
    write("saw", """
ÉCHO - O2 scie, cellule 24x24, 4 images, centre de la scie au pixel (12,12) : ancrage p - (12,12).
Intention : un disque qui hurle ; la rotation se lit aux dents en cliquet et aux 3 trous qui tournent.
Géométrie : disque r 6 = cercle létal de hz.gd (r 6 par défaut), 6 dents jusqu'à r ~9,5 (Ø20) + contour k.
Lumière haut-gauche : bord du disque et dents en z en haut à gauche, en x en bas à droite ; moyeu Z, axe W.
Timing (E3) : 4 images à 50 ms (20 fps), rotation de 15° par image (sens antihoraire à l'écran), boucle sur 60°.
  0-3 | rotation | dents et trous avancent de 15° | mouvement continu | 50 ms chacune
Budget : k x X z Z W = 6 couleurs.
Défaut corrigé : rastérisation brute = dents en L et pixels orphelins sur les flancs ; retouche dans SAW_FIX.
""", saw_frames(), 24, 24)


@asset
def saw_echo():
    write("saw_echo", """
ÉCHO - O2 scie gravée : même sprite recoloré (q t c e, contour q), image 0 de la scie, 24x24.
Le code la fait tourner (ou anime la bande saw si besoin, même cellule) : scies et ennemis gravés continuent de bouger.
Budget : q t c e = 4 couleurs. Défaut corrigé : le W de l'axe passe en e (pas de blanc dans la gravure).
""", [recolor(f) for f in saw_frames()], 24, 24)


@asset
def saw_rail():
    h = pad(G("xkxkxkxkxkxkxkxk\nkkkkkkkkkkkkkkkk"), 16, 16, 0, 7)
    v = pad(["xk"[(y % 2)] + "k" for y in range(16)], 16, 16, 7, 0)
    cap = pad(G("""
.kkkk.
kmllmk
kmssnk
kmssnk
knnnnk
.kkkk.
"""), 16, 16, 5, 5)
    write("saw_rail", """
ÉCHO - O4/O5 rail de scie, 3 tuiles 16x16 : 0 = rail horizontal (rangée 7, centre de la scie), 1 = rail vertical
(colonne 7), 2 = butée de fin de course (borne de métal non létale, centrée en (8,8)).
Intention : dire la trajectoire de la scie avant qu'elle n'arrive, sans voler la lecture du danger.
Rail : pointillé x 1 px sur 2 (bible O4/O5) posé sur une rainure k. Butée : métal m l / s n, pas de magenta.
Timing : statique. Budget : k x (rail) ; k n s m l (butée) = 5 couleurs.
Défaut corrigé : rail en X plein = se lisait comme un laser éteint ; ramené à un pointillé x sombre.
""", [h, v, cap], 16, 16)


# ======================================================================= 3. LASER
EMIT = """
kkkkkk..
kmmmmsk.
kmsXXXXk
kmXEEEEE
ksXEEEEE
ksXXXXXk
knnnnnk.
kkkkkk..
"""


def emitter(fill):
    return G(EMIT.replace("EEEEE", fill))


@asset
def laser():
    write("laser", """
ÉCHO - O8 émetteur de laser, mur GAUCHE, cellule 8x8, 3 états. Ancrage : coin haut-gauche à (WL, y-4).
Intention : une bouche de pierre qui se charge ; le préavis se lit à la couleur de la bouche avant le tir.
Bouche X dans la pierre (s m n + contour k), lentille sur les rangées 3-4 = cœur du faisceau (y-1, y).
Timing (E3, émissif E2-F) : img | rôle | change
  0 | éteint (état 0) | bouche x sombre
  1 | lueur (état 1, préavis : le code alterne 0/1 à 10 Hz) | dégradé x X z z z vers la sortie
  2 | actif (état 2) | X z Z W W, le W touche le faisceau
Budget par image : k n s m + 2 à 3 tons danger (+W en actif) = 6 au plus.
Défaut corrigé : la lentille fermée par un contour k côté couloir coupait le faisceau ; la bouche est ouverte en x=7.
""", [emitter("xxxxx"), emitter("xXzzz"), emitter("XzZWW")], 8, 8)


@asset
def laser_echo():
    m = {"x": "q", "X": "t", "z": "c", "Z": "e", "W": "e"}
    write("laser_echo", """
ÉCHO - O8 émetteur gravé, 8x8, 1 image : la pierre reste, la bouche passe en t c e (ligne cyan permanente).
Budget : k n s m + t c e = 7 (pierre 4 + écho 3) ; la pierre n'est pas un ton de danger.
Défaut corrigé : rien de magenta ne reste sur un piège gravé.
""", [recolor(emitter("tccee"), m)], 8, 8)


def beam_tile(core, mid, edge):
    rows = ["." * 16] * 8
    rows[1] = edge
    rows[2] = mid
    rows[3] = core[0]
    rows[4] = core[1]
    rows[5] = mid
    rows[6] = edge
    return rows


@asset
def beam():
    warn = ["." * 16] * 8
    warn = [r for r in warn]
    warn[3] = "zzz.zzz.zzz.zzz."
    warn[4] = "xxx.xxx.xxx.xxx."
    a = beam_tile(("W" * 16, "Z" * 16), "z" * 16, "X" * 16)
    b = beam_tile(("Z" * 16, "W" * 16), "z" * 16, "XXXxXXXXXXXxXXXX")
    c = beam_tile(("ZZZWZZZZZZZWZZZZ", "ZZZZZZZWZZZZZZZW"), "z" * 16, "XxXXXXXxXXXXXXXx")
    write("beam", """
ÉCHO - O8 faisceau, tuile 16x8 répétable en x de WL+8 à WR-8, 4 images. Ancrage : coin haut-gauche à (x, y-4).
Rangées 2-5 = faisceau létal de 4 px (hz.gd Rect2(WL, y-2, WR-WL, 4)) ; rangées 1 et 6 = bords X (1 px de dépassement).
Intention : un trait qui tranche le couloir ; le préavis est un pointillé qui annonce l'axe sans le remplir.
Timing (E3) : img | rôle | change | principe | durée
  0 | préavis | tirets z de 3 px sur ombre x (rangées 3-4) | anticipation | tenue + clignotement 10 Hz du code
  1 | actif A | cœur W haut, Z bas | pic | 1/20 s
  2 | actif B | cœur inversé, 2 crans x dans le bord | vibration | 1/20 s
  3 | actif C | étincelles W isolées, bord crénelé | vibration | 1/20 s  (boucle 1-2-3)
Budget : x X z Z W = 5 couleurs (pas de contour : émissif à contour coloré X).
Défaut corrigé : faisceau de 3 px dans la bible élargi à 4 px pour coller à la hitbox du code.
""", [warn, a, b, c], 16, 8)


@asset
def beam_echo():
    t = ["." * 16] * 8
    t = [r for r in t]
    t[3] = "c" * 16
    t[4] = "qtqtqtqtqtqtqtqt"
    write("beam_echo", """
ÉCHO - O8 laser gravé : ligne cyan permanente, tuile 16x8 répétable, 1 image, même ancrage que beam.
Intention : la trace du laser, fine (2 px) et calme : rien ne vibre.
Budget : q t c = 3 couleurs. Défaut corrigé : une ligne c pleine de 4 px se lisait comme un laser actif ; réduite à 1 px + gravure.
""", [t], 16, 8)


if __name__ == "__main__":
    names = sys.argv[1:] or list(REGISTRY)
    for n in names:
        REGISTRY[n]()
        print("ok", n)
