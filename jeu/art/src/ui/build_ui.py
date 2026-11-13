#!/usr/bin/env python3
"""build_ui.py : assets d'interface d'ÉCHO (famille F9, UI_UX §7), palette v2.

Chaque asset est dessiné ici par coordonnées explicites (lettres de palette_v2) ou lu dans une
source à la main (icons12.txt, icons16.txt), puis écrit comme grille texte au format tools/px.py
dans art/src/ui/grids/<nom>.txt, puis rendu en PNG (voir uicore.py).
Une grille marquée « # manuel » n'est plus réécrite : on peut la retoucher à la main.

Usage : python3 build_ui.py [--render] [noms...]
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from uicore import (C, strip, stack, bayer, asset, REGISTRY, write_grid, render,  # noqa: E402
                    ICONS12, ICONS16, icon12, icon16, HERE, OUT_GAME, OUT_ART, PAL, hex_to_rgba)


# ==============================================================================================
# Panneaux (§5.1)
# ==============================================================================================
def stone_frame(c, x, y, w, h, r1, r2, r3, fond, seal, outline="k"):
    """Bordure 3 px + contour : r1=(clair, sombre) anneau 1, r2 anneau 2, r3=(haut-g, bas-d) anneau 3."""
    c.rect(x + 1, y + 1, w - 2, h - 2, fond)
    c.ring(x, y, w, h, outline, outline, cut=True)
    c.ring(x + 1, y + 1, w - 2, h - 2, r1[0], r1[1])
    c.ring(x + 2, y + 2, w - 4, h - 4, r2, r2)
    c.ring(x + 3, y + 3, w - 6, h - 6, r3[0], r3[1])
    if seal:
        for sx, sy in ((x + 1, y + 1), (x + w - 4, y + 1), (x + 1, y + h - 4), (x + w - 4, y + h - 4)):
            c.put(sx, sy, seal)


@asset("panel", 1, """panel 24x24 · 9-patch marges 8 (content_margin 8).
Fond d ; bordure pierre 3 px : anneau 1 l (haut-gauche, arête éclairée) / n (bas-droite),
anneau 2 s, anneau 3 creux n (haut-gauche) / m (bas-droite) ; sceaux d'écho t aux coins ; contour k.""")
def panel():
    c = C(24, 24)
    stone_frame(c, 0, 0, 24, 24, ("l", "n"), "s", ("n", "m"), "d", "kqk/qtq/kqk".replace("k", "s"))
    # sceau : losange t sur s, cœur q (sceau éteint : l'écho n'est pas actif sur un panneau normal)
    for sx, sy in ((1, 1), (20, 1), (1, 20), (20, 20)):
        c.put(sx, sy, ".t./tqt/.t.")
    return c


@asset("panel_echo", 1, """panel_echo 24x24 · 9-patch marges 8. Panneau « écho » (vidéo, confirmation, record).
Fond d ; bordure q t c : anneau 1 c / q, anneau 2 t, anneau 3 q / c ; sceaux e aux coins ; contour k.""")
def panel_echo():
    c = C(24, 24)
    stone_frame(c, 0, 0, 24, 24, ("c", "q"), "t", ("q", "c"), "d", None)
    for sx, sy in ((1, 1), (20, 1), (1, 20), (20, 20)):
        c.put(sx, sy, ".e./ece/.e.")
    return c


@asset("panel_inset", 1, """panel_inset 24x24 · 9-patch marges 6. Creux (listes, cases, champs).
Fond b ; anneau creux k en haut-gauche / n en bas-droite ; ombre portée intérieure d sur la 2e rangée et
la 2e colonne ; pas de contour extérieur.""")
def panel_inset():
    c = C(24, 24)
    c.rect(0, 0, 24, 24, "b")
    c.ring(0, 0, 24, 24, "k", "n", cut=True)
    c.hl(1, 22, 1, "k")
    c.vl(1, 1, 22, "k")
    c.px(0, 0, ".")
    return c


# ==============================================================================================
# Boutons (§5.2)
# ==============================================================================================
BTN = {
    #        face top  glint shadow edge  outline
    "main": ("o", "a", "A", "R", "r"),
    "alt":  ("s", "m", "l", "n", "d"),
    "echo": ("c", "e", "W", "t", "q"),
}


def button_frame(face, top, glint, shadow, edge, dy=0, thick=True):
    c = C(48, 24)
    y0 = dy
    y1 = 23 if not thick else 23
    # corps : rangée y0 contour, y0+1..y0+2 biseau haut, face, (épaisseur 2 + pied), contour
    hface = 24 - y0
    c.rect(1, y0 + 1, 46, 22 - y0, face)
    c.ring(0, y0, 48, 24 - y0, "k", "k", cut=True)
    c.hl(1, 46, y0 + 1, top)
    c.hl(1, 46, y0 + 2, top)
    c.vl(1, y0 + 1, 19, top)            # bord gauche éclairé
    c.vl(46, y0 + 3, 22, edge)          # bord droit ombré
    if thick:
        c.hl(1, 46, 19, edge)           # arête basse de la face
        c.hl(1, 46, 20, shadow)
        c.hl(1, 46, 21, shadow)
        c.hl(1, 46, 22, edge)
        c.px(1, 20, shadow); c.px(1, 21, shadow); c.px(1, 22, edge)
    else:
        c.hl(1, 46, 21, edge)
        c.hl(1, 46, 22, edge)
        c.vl(1, y0 + 3, 21, face)
        c.px(1, 22, edge)
    c.px(1, y0 + 1, "k")  # coin intérieur arrondi
    c.px(46, y0 + 1, "k")
    c.px(1, 22, "k")
    c.px(46, 22, "k")
    if glint:
        c.hl(3, 5, y0 + 1, glint)
        c.px(2, y0 + 2, glint)
    return c


def button(kind):
    face, top, glint, shadow, edge = BTN[kind]
    normal = button_frame(face, top, glint, shadow, edge, 0, True)
    pressed = button_frame(face, top, None, shadow, edge, 2, False)
    # enfoncé : biseau haut assombri d'un cran (la face est rentrée)
    pressed.hl(2, 45, 3, top)
    pressed.hl(2, 45, 4, face)
    disabled = button_frame("n", "s", None, "d", "d", 2, False)
    return strip([normal, pressed, disabled])


BTN_DOC = """btn_{k} 144x24 = 3 images 48x24 : 0 normal · 1 enfoncé · 2 désactivé.
9-patch marges gauche 8, droite 8, haut 6, bas 8 (zone étirée : colonnes 8-39, rangées 6-15).
Normal : contour k arrondi, biseau haut {t} (2 rangées) + reflet {g}, face {f}, bord droit {e},
épaisseur {s} (2 rangées) + pied {e}. Enfoncé : la face descend de 2 px, plus d'épaisseur.
Désactivé : position enfoncée, face n, biseau s, libellé m. Libellé font_7 {lab}, y 7 (9 enfoncé)."""


@asset("btn_main", 3, BTN_DOC.format(k="main", t="a", g="A", f="o", e="r", s="R", lab="k"))
def btn_main():
    return button("main")


@asset("btn_alt", 3, BTN_DOC.format(k="alt", t="m", g="l", f="s", e="d", s="n", lab="w"))
def btn_alt():
    return button("alt")


@asset("btn_echo", 3, BTN_DOC.format(k="echo", t="e", g="W", f="c", e="q", s="t", lab="k") +
       "\nSeule face cyan autorisée hors écho (ARBITRAGES A12 : face c, texte k).")
def btn_echo():
    return button("echo")


# ==============================================================================================
# Onglets, barres, badges, pastilles
# ==============================================================================================
@asset("tab", 3, """tab 72x20 = 3 images 24x20 : 0 inactif · 1 actif · 2 enfoncé. 9-patch marges 6.
Inactif : face d, bord n, libellé l. Actif : face s, haut m, trait a de 2 px en bas, libellé w.
Enfoncé : face n. Coins hauts arrondis, base droite (l'onglet se pose sur le panneau).""")
def tab():
    fr = []
    for face, top, rim, bottom in (("d", "n", "n", None), ("s", "m", "m", "a"), ("n", "s", "s", None)):
        c = C(24, 20)
        c.rect(1, 1, 22, 18, face)
        c.ring(0, 0, 24, 20, "k", "k", cut=True)
        c.ring(1, 1, 22, 18, rim, rim)
        c.hl(2, 21, 2, top)
        c.px(1, 1, "k"); c.px(22, 1, "k")
        c.hl(1, 22, 18, "k" if bottom is None else bottom)
        c.hl(1, 22, 17, rim if bottom is None else bottom)
        c.hl(0, 23, 19, "k")
        c.px(0, 19, "k"); c.px(23, 19, "k")
        if bottom:
            c.vl(1, 2, 16, top)
        fr.append(c)
    return strip(fr)


@asset("bar", 5, """bar 40x6 = 5 images 8x6, 9-patch marges 2.
0 cadre (contour k, fond b) · 1 remplissage XP j/J · 2 or G/y · 3 écho c/e · 4 danger z/Z.
Les remplissages se posent dans le cadre (même 9-patch), rangée 1 claire, rangées 2-4 base.""")
def bar():
    fr = []
    c = C(8, 6)
    c.rect(1, 1, 6, 4, "b")
    c.ring(0, 0, 8, 6, "k", "k", cut=True)
    c.hl(1, 6, 4, "d")
    fr.append(c)
    for base, light in (("j", "J"), ("G", "y"), ("c", "e"), ("z", "Z")):
        c = C(8, 6)
        c.rect(1, 1, 6, 4, base)
        c.hl(1, 6, 1, light)
        fr.append(c)
    return strip(fr)


@asset("badge_new", 4, """badge_new 28x7 = 4 images 7x7 (pop en boucle, 120 ms) : 7x7 · 7x7 + reflet y · 5x5 · 7x7.
Rond G, « ! » k 1x4 (barre 3 + point), contour k.""")
def badge_new():
    big = ".kkkkk./kGGkGGk/kGGkGGk/kGGkGGk/kGGGGGk/kgGkGgk/.kkkkk."
    glint = ".kkkkk./kyGkGGk/kGGkGGk/kGGkGGk/kGGGGGk/kgGkGgk/.kkkkk."
    small = "......./..kkk../.kGkGk./.kGkGk./.kGGGk./..kkk../......."
    fr = []
    for s in (big, glint, small, big):
        c = C(7, 7)
        c.put(0, 0, s)
        fr.append(c)
    return strip(fr)


@asset("hud_pip", 2, "hud_pip 4x2 = 2 images 2x2 : 0 vide n · 1 plein G (compteur de vies / combo du HUD).")
def hud_pip():
    c = C(4, 2)
    c.rect(0, 0, 2, 2, "n")
    c.rect(2, 0, 2, 2, "G")
    c.px(2, 0, "y")
    return c


@asset("diff_pips", 3, """diff_pips 12x4 = 3 images 4x4 : 0 facile rond l · 1 moyen losange a · 2 dur triangle o.
Contour k ; les trois formes diffèrent aussi en silhouette (lecture sans couleur).""")
def diff_pips():
    c = C(12, 4)
    c.put(0, 0, ".kk./kwlk/kllk/.kk.")
    c.put(4, 0, ".k../kAk./.kak/..k.")
    c.put(8, 0, ".kk./koak/kook/kkkk")
    return c


# ==============================================================================================
# Icônes
# ==============================================================================================
@asset("icons12", 24, "icons12 288x12 = 24 icônes 12x12 (source à la main : art/src/ui/icons12.txt). Index : " +
       " ".join(f"{i}={n}" for i, (n, _) in enumerate(ICONS12)))
def icons12():
    return strip([c for _, c in ICONS12])


@asset("icons16", 16, "icons16 256x16 = 16 icônes 16x16 (source à la main : art/src/ui/icons16.txt). Index : " +
       " ".join(f"{i}={n}" for i, (n, _) in enumerate(ICONS16)))
def icons16():
    return strip([c for _, c in ICONS16])


# ==============================================================================================
# HUD
# ==============================================================================================
@asset("hud_bar", 1, """hud_bar 180x20 : bandeau haut du HUD. Rangées 0-15 k plein ; 16-17 trame Bayer 50 % k ;
18-19 trame 25 % k (fondu vers le jeu sans alpha).""")
def hud_bar():
    c = C(180, 20)
    c.rect(0, 0, 180, 16, "k")
    for y in range(16, 20):
        lvl = 8 if y < 18 else 4
        for x in range(180):
            if bayer(x, y, lvl):
                c.px(x, y, "k")
    return c


def lantern(state):
    c = C(12, 12)
    # anneau, chapeau, verre, socle
    c.put(0, 0, "............|.....kk.....|....k..k....|...kkkkkk...|..knmmmmnk..|..k......k..|"
                "..k......k..|..k......k..|..k......k..|..knnnnnnk..|...kkkkkk...|............".replace("|", "/"))
    c.put(3, 4, "mlll")
    glass = {
        0: "oaao/aAAa/aAWa/oaao",
        1: "oaao/aAAo/aWAa/oaao",
        2: "nnnn/nnsn/nsan/nnnn",
        3: "qttq/tcct/tcet/qttq",
    }[state]
    c.put(4, 5, glass)
    c.vl(3, 5, 8, {0: "o", 1: "o", 2: "n", 3: "q"}[state])
    c.vl(8, 5, 8, {0: "R", 1: "R", 2: "n", 3: "q"}[state])
    if state == 2:  # fumée l qui s'échappe
        c.px(8, 1, "l"); c.px(9, 0, "l"); c.px(3, 1, "l")
    if state in (0, 1):
        c.px(4 + (1 if state == 0 else 2), 5, "A")
    return c


@asset("ui_lantern", 4, """ui_lantern 48x12 = 4 images 12x12 (vies du HUD).
0 allumée (verre o a A, cœur W) · 1 flamme alternée (vacille, 2 images à 200 ms) ·
2 s'éteint (verre n, braise a, fumée l) · 3 éteinte = écho (verre q t c e, la vie devient écho).
Chapeau m l, socle n, contour k.""")
def ui_lantern():
    return strip([lantern(i) for i in range(4)])


# ==============================================================================================
# Bandeaux, toasts
# ==============================================================================================
def plaque(w, h, face, top, bottom, edge="k", notch=True):
    c = C(w, h)
    c.rect(1, 1, w - 2, h - 2, face)
    c.ring(0, 0, w, h, edge, edge, cut=True)
    c.hl(1, w - 2, 1, top)
    c.vl(1, 1, h - 3, top)
    c.hl(1, w - 2, h - 2, bottom)
    c.hl(1, w - 2, h - 3, bottom)
    c.vl(w - 2, 2, h - 2, bottom)
    c.px(1, 1, edge); c.px(w - 2, 1, edge); c.px(1, h - 2, edge); c.px(w - 2, h - 2, edge)
    if notch:  # queues d'aronde : encoche en V aux deux bouts, dans la marge 9-patch
        mid = h // 2
        for i, dy in enumerate((-1, 0, 1)):
            pass
        for y in range(mid - 2, mid + 2):
            d = 2 - abs(y - mid + 0.5) + 0.5
            for x in range(int(d)):
                c.px(x, y, ".")
                c.px(w - 1 - x, y, ".")
            c.px(int(d), y, edge)
            c.px(w - 1 - int(d), y, edge)
    return c


@asset("banner", 2, """banner 96x16 = 2 images 48x16, 9-patch marges 6 (gauche/droite), 4 (haut/bas).
0 or : face G, biseau y, ombre g, contour k, encoches en V aux deux bouts (record, niveau).
1 pierre : face s, biseau m, ombre n, contour k (titres de section).""")
def banner():
    gold = plaque(48, 16, "G", "y", "g")
    stone = plaque(48, 16, "s", "m", "n")
    return strip([gold, stone])


@asset("toast", 1, """toast 24x16, 9-patch marges 6. Fond k, bordure n, arête m en haut (1 px). Coins coupés.""")
def toast():
    c = C(24, 16)
    c.rect(1, 1, 22, 14, "k")
    c.ring(0, 0, 24, 16, "n", "n", cut=True)
    c.hl(1, 22, 0, "m")
    c.px(1, 1, "n"); c.px(22, 1, "n"); c.px(1, 14, "n"); c.px(22, 14, "n")
    return c


@asset("banner_tuto", 1, """banner_tuto 64x24, 9-patch marges 6. Bandeau tutoriel court : fond d, bordure n s
(anneau s éclairé en haut-gauche, n en bas-droite), contour k. Le pictogramme tuto16 se pose à x 4, y 4.""")
def banner_tuto():
    c = C(64, 24)
    c.rect(1, 1, 62, 22, "d")
    c.ring(0, 0, 64, 24, "k", "k", cut=True)
    c.ring(1, 1, 62, 22, "s", "n")
    c.ring(2, 2, 60, 20, "n", "n")
    c.hl(3, 60, 3, "b")
    return c


# ==============================================================================================
# Pictogrammes de tutoriel (16x16) et main tap (32x32)
# ==============================================================================================
HAND = [
    "..w......",
    ".wwl.....",
    ".wwl.....",
    ".wwl.....",
    ".wwkwwkww",
    ".wwkwlkwl",
    "wwwwwwwwl",
    "wwwwwwwwl",
    ".wwwwwwl.",
    "..lllll..",
]


def hand(c, tipx, tipy):
    """Pose la main (index pointé vers le haut) avec le bout du doigt en (tipx, tipy)."""
    c.put(tipx - 2, tipy, HAND)


def picto(kind, pose):
    c = C(16, 16)
    if kind == "tap":
        if pose == 0:
            hand(c, 7, 5)
        else:
            hand(c, 7, 4)
            c.px(4, 2, "l"); c.px(10, 2, "l"); c.px(7, 1, "w")
            c.px(3, 4, "l"); c.px(11, 4, "l")
    elif kind == "hold":
        hand(c, 7, 5)
        arc = [(4, 3), (4, 2), (5, 1), (6, 1), (7, 1), (8, 1), (9, 1), (10, 2), (10, 3)]
        n = 4 if pose == 0 else len(arc)
        for x, y in arc[:n]:
            c.px(x, y, "w" if (x, y) == arc[n - 1] else "l")
    elif kind == "volte":
        hand(c, 9, 5 if pose == 0 else 4)
        # petit arc de demi-tour en l'air (flèche courbe) à gauche
        c.put(1, 1, ".ll./l..w/l.ww/l...")
        if pose == 1:
            c.px(12, 3, "l"); c.px(9, 2, "w"); c.px(6, 3, "l")
    elif kind == "slide":
        x = 5 if pose == 0 else 9
        hand(c, x, 5)
        c.hl(2, 13, 2, "l")
        c.put(12, 1, "w./.w/w.")
        c.px(x, 3, "w")
    elif kind == "danger":
        tri = ["......w.......", ".....wwl......", ".....wll......", "....wwlll.....", "....wlklll....",
               "...wwlklll....", "...wllklll l..".replace(" ", "l"), "..wwlllllll...", "..wllllklll l.".replace(" ", "l"),
               ".wwwwwwwwwwll."]
        tri = ["......w.......",
               ".....wwl......",
               ".....wll......",
               "....wwkll.....",
               "....wlkll.....",
               "...wwlklll....",
               "...wllllll....",
               "..wwlllklll...",
               "..wlllllllll..",
               ".wwwwwwwwwwwl."]
        c.put(1, 2 if pose == 0 else 1, tri)
        # dents (piques) sous le triangle
        y = 12 if pose == 0 else 12
        c.put(2, y, "w.w.w.w.w.w." if pose == 0 else "l.l.l.l.l.l.")
        c.put(2, y + 1, "wlwlwlwlwlwl")
    elif kind == "altar":
        c.put(3, 8, "llllllllll/wwwwwwwwwl/.wllllll l./.wlllllll./wwwwwwwwwl".replace(" ", "l").replace("/", "/"))
        c.put(3, 8, "wwwwwwwwww")
        c.put(3, 9, "llllllllll")
        c.put(4, 10, "wlllllll")
        c.put(4, 11, "wlllllll")
        c.put(3, 12, "wwwwwwwwww")
        c.put(3, 13, "llllllllll")
        flame = ".w./wwl/.l." if pose == 0 else ".w./.w./wwl/wwl/.l."
        c.put(7, 5 if pose == 0 else 3, flame)
    c.outline("k")
    return c


TUTO = ["tap", "hold", "volte", "slide", "danger", "altar"]


@asset("tuto16", 6, """tuto16 96x32 = 6 pictogrammes 16x16 x 2 poses. Rangée 0 = pose A, rangée 1 = pose B
(alterner 400 ms). Colonnes : 0 tap · 1 maintenir (doigt + arc qui s'allonge) · 2 volte (tap en l'air,
arc de demi-tour) · 3 glisser · 4 danger (triangle + dents) · 5 autel (flamme qui grandit).
Couleurs w + l, contour k. Pictogrammes sans texte.""")
def tuto16():
    a = strip([picto(k, 0) for k in TUTO])
    b = strip([picto(k, 1) for k in TUTO])
    return stack([a, b])


BIG_HAND = [
    "...II.........",
    "..IIii........",
    "..Iiii........",
    "..Iiii........",
    "..Iiii........",
    "..IiiiII......",
    "..IiiikiII....",
    "..IiiikiikII..",
    "I.Iiiikiikiii.",
    "IIIiiiiiiikiii",
    "Iiiiiiiiiiiiii",
    ".Iiiiiiiiiiiii",
    ".Iiiiiiiiiiii.",
    "..Iiiiiiiiiii.",
    "...iiiiiiiiH..",
    "....iiiiiiH...",
    "....iiiiiiH...",
    "....iiiiiiH...",
]


@asset("tap", 2, """tap 64x32 = 2 images 32x32 (400 ms par image) : main posée sur le mur, à côté du héros.
0 doigt levé · 1 doigt appuyé (main descendue de 3 px, impacts I). Couleurs i I (+ H pour l'ombre du
poignet), contour k. Remplace sprites/tap.png (32x16, v1), qui reste en place pour main.gd.""")
def tap():
    fr = []
    for pose in (0, 1):
        c = C(32, 32)
        dy = 6 if pose == 0 else 9
        c.put(9, dy, BIG_HAND)
        if pose == 1:
            tip = (12, dy)
            for x, y in ((8, 5), (7, 6), (16, 5), (17, 6), (12, 3), (12, 2)):
                c.px(x, y, "I")
        c.outline("k")
        fr.append(c)
    return strip(fr)


# ==============================================================================================
# Tampon, cartes, piédestal
# ==============================================================================================
def stamp_rect(c, w, h, sparkle=False):
    x = (64 - w) // 2
    y = (24 - h) // 2
    c.rect(x, y, w, h, "d")
    c.ring(x, y, w, h, "k", "k", cut=True)
    if w >= 8 and h >= 6:
        c.ring(x + 1, y + 1, w - 2, h - 2, "G", "g", cut=False)
        c.ring(x + 2, y + 2, w - 4, h - 4, "g", "G", cut=False)
        c.hl(x + 2, x + w - 3, y + 1, "y")
        c.px(x + 1, y + 1, "k"); c.px(x + w - 2, y + 1, "k")
        c.px(x + 1, y + h - 2, "k"); c.px(x + w - 2, y + h - 2, "k")
    if sparkle:
        c.put(x + w - 5, y - 1 if y > 0 else 0, ".e./eWe/.e.")
        c.px(x + 3, y + h - 1, "e")


@asset("stamp_frame", 5, """stamp_frame 320x24 = 5 images 64x24 (pop du tampon « RECORD », 50 ms/image) :
0 50 % (27x10) · 1 115 % (62x23) · 2 écrasé (60x18) · 3 final (54x20) · 4 final + étincelle e.
Plaque d, double filet or G/g + reflet y, contour k. Texte posé par-dessus en font_l_outline.""")
def stamp_frame():
    fr = []
    for w, h, sp in ((27, 10, False), (62, 23, False), (60, 18, False), (54, 20, False), (54, 20, True)):
        c = C(64, 24)
        stamp_rect(c, w, h, sp)
        fr.append(c)
    return strip(fr)


@asset("card", 4, """card 96x24 = 4 images 24x24, 9-patch marges 6 (cartes de boutique / tenues).
0 normal : creux (panel_inset) + bordure n · 1 sélectionnée : bordure w 1 px + coins a ·
2 équipée : bordure G (+ reflet y) · 3 verrouillée : fond k, bordure n, trame d.""")
def card():
    fr = []
    for state in range(4):
        c = C(24, 24)
        c.rect(1, 1, 22, 22, "b" if state < 3 else "k")
        rim = {0: "n", 1: "w", 2: "G", 3: "n"}[state]
        c.ring(0, 0, 24, 24, rim, rim, cut=True)
        if state < 3:
            c.hl(1, 22, 1, "k")
            c.vl(1, 1, 22, "k")
        if state == 1:
            for x, y, sx, sy in ((0, 0, 1, 1), (23, 0, -1, 1), (0, 23, 1, -1), (23, 23, -1, -1)):
                c.px(x + sx, y, "a"); c.px(x + 2 * sx, y, "a")
                c.px(x, y + sy, "a"); c.px(x, y + 2 * sy, "a")
                c.px(x + sx, y + sy, "a")
        if state == 2:
            c.hl(2, 8, 0, "y")
        if state == 3:
            for y in range(2, 22):
                for x in range(2, 22):
                    if bayer(x, y, 4):
                        c.px(x, y, "d")
        fr.append(c)
    return strip(fr)


@asset("shop_pedestal", 1, """shop_pedestal 64x16 : socle de pierre de la boutique (la tenue se pose dessus, y 0).
Plateau l (arête) / m, devant s avec joints n, pied n, contour k.""")
def shop_pedestal():
    c = C(64, 16)
    c.rect(1, 1, 62, 4, "m")
    c.ring(0, 0, 64, 6, "k", "k", cut=True)
    c.hl(1, 62, 1, "l")
    c.hl(1, 62, 4, "s")
    c.rect(3, 6, 58, 8, "s")
    c.ring(2, 5, 60, 10, "k", "k")
    c.hl(3, 60, 5, "k")
    c.hl(3, 60, 6, "m")
    c.hl(3, 60, 12, "n")
    c.hl(3, 60, 13, "n")
    for x in (12, 26, 37, 51):
        c.vl(x, 7, 11, "n")
    c.vl(3, 6, 13, "m")
    c.vl(60, 6, 13, "n")
    c.hl(1, 62, 15, "k")
    c.rect(1, 14, 62, 1, "n")
    c.vl(0, 14, 15, "k"); c.vl(63, 14, 15, "k")
    c.ring(0, 13, 64, 3, "k", "k", cut=True)
    c.hl(1, 62, 14, "n")
    return c


# ==============================================================================================
# Coffre
# ==============================================================================================
def chest_body(c, ox, oy):
    """Corps du coffre 22x12, coin haut-gauche (ox, oy)."""
    c.rect(ox + 1, oy, 20, 11, "s")
    c.ring(ox, oy, 22, 12, "k", "k", cut=True)
    c.hl(ox + 1, ox + 20, oy, "k")
    c.hl(ox + 1, ox + 20, oy + 1, "m")
    c.hl(ox + 1, ox + 20, oy + 9, "n")
    c.hl(ox + 1, ox + 20, oy + 10, "n")
    c.vl(ox + 20, oy + 1, oy + 10, "n")
    for bx in (ox + 3, ox + 17):
        c.vl(bx, oy + 1, oy + 10, "G")
        c.vl(bx + 1, oy + 1, oy + 10, "g")
    c.put(ox + 9, oy + 1, "kkkk/kGyk/kgGk/kkgk/.kk.".replace("kkgk", "kGgk"))


def chest_lid(c, ox, oy, h=6):
    c.rect(ox + 1, oy + 1, 20, h - 1, "s")
    c.ring(ox, oy, 22, h + 1, "k", "k", cut=True)
    c.hl(ox + 2, ox + 19, oy + 1, "l")
    c.hl(ox + 1, ox + 20, oy + 2, "m")
    c.hl(ox + 1, ox + 20, oy + h - 1, "n")
    c.vl(ox + 20, oy + 2, oy + h - 1, "n")
    for bx in (ox + 3, ox + 17):
        c.vl(bx, oy + 1, oy + h - 1, "G")
        c.vl(bx + 1, oy + 1, oy + h - 1, "g")
    c.px(ox + 3, oy + 1, "y")


def chest_frame(i):
    c = C(32, 32)
    ox = 5 + {0: -1, 1: 1}.get(i, 0)
    by = 18
    if i in (0, 1):
        chest_lid(c, ox, by - 6)
        chest_body(c, ox, by)
        c.px(ox - 2, by + 2, "l"); c.px(ox + 23, by + 4, "l")  # traits de secousse
        return c
    # ouverture : le couvercle bascule vers l'arrière (il raccourcit et monte)
    lid = {2: (by - 8, 5), 3: (by - 10, 4), 4: (by - 11, 3), 5: (by - 11, 3), 6: (by - 11, 3), 7: (by - 11, 3)}[i]
    # couvercle ouvert : on voit son revers, debout derrière l'ouverture, articulé au corps
    lh = {2: 5, 3: 7, 4: 8, 5: 8, 6: 8, 7: 8}[i]
    top = by - lh
    c.rect(ox + 1, top + 1, 20, lh - 1, "n")
    c.ring(ox, top, 22, lh + 1, "k", "k", cut=True)
    c.hl(ox + 2, ox + 19, top + 1, "m")
    c.rect(ox + 2, top + 2, 18, lh - 3, "d")
    for bx in (ox + 3, ox + 17):
        c.vl(bx, top + 1, by - 1, "g")
        c.vl(bx + 1, top + 1, by - 1, "G")
    # lueur qui sort
    glow = {2: 1, 3: 3, 4: 6, 5: 8, 6: 7, 7: 0}[i]
    for g in range(glow):
        y = by - 1 - g
        half = 7 - g // 2 + (1 if i in (5, 6) and g % 2 else 0)
        col = "W" if (i == 3 and g < 2) else ("y" if g < 3 else "G")
        for x in range(16 - half, 16 + half):
            if g < 3 or bayer(x, y, 10 - g):
                c.px(x, y, col)
    if i in (5, 6):
        for x, y in ((6, 6), (25, 8), (9, 2), (22, 3)) if i == 5 else ((7, 4), (24, 5), (12, 1), (20, 2)):
            c.put(x - 1, y - 1, ".y./yWy/.y." if (x + i) % 2 else ".G./GyG/.G.")
    # ouverture visible : intérieur sombre + or
    c.rect(ox + 1, by, 20, 2, "k")
    c.hl(ox + 3, ox + 18, by, "G" if i < 7 else "g")
    c.hl(ox + 5, ox + 16, by, "y" if i in (3, 4, 5, 6) else "G")
    chest_body(c, ox, by + 1)
    c.hl(ox + 1, ox + 20, by + 1, "k")
    return c


@asset("chest", 8, """chest 256x32 = 8 images 32x32 (coffre de palier) : 0-1 secousse ±1 px · 2-4 ouverture
(couvercle qui bascule, lueur G, pic W sur l'image 3 seulement) · 5-6 lueur ouverte en boucle
(étincelles y) · 7 ouvert, final. Pierre s/m/n, cerclages et serrure G/g/y, contour k.""")
def chest():
    return strip([chest_frame(i) for i in range(8)])


# ==============================================================================================
# Popup de récompense (rayons)
# ==============================================================================================
@asset("popup_reward", 6, """popup_reward 384x64 = 6 images 64x64, 83 ms par image, en boucle (rotation de 7,5° par
image : 8 rayons = période 45°, la 7e image retombe sur la 1re). Rayons G (y près du centre, pointes
tramées) sur disque d ; anneau n puis contour k. L'objet gagné se pose au centre.""")
def popup_reward():
    fr = []
    cx = cy = 31.5
    for f in range(6):
        c = C(64, 64)
        rot = math.radians(7.5 * f)
        for y in range(64):
            for x in range(64):
                dx, dy = x - cx, y - cy
                r = math.hypot(dx, dy)
                if r > 31.5:
                    continue
                if r > 30.5:
                    c.px(x, y, "k")
                    continue
                if r > 29.5:
                    c.px(x, y, "n")
                    continue
                a = (math.atan2(dy, dx) - rot) % (math.pi / 4)
                width = 0.13 + 0.05 * (1 - r / 30)
                on = abs(a - math.pi / 8) < width * (math.pi / 4) * 1.6
                col = "d"
                if r < 9:
                    col = "y" if r < 6 else "G"
                elif on:
                    if r < 16:
                        col = "y"
                    elif r < 24:
                        col = "G"
                    elif bayer(x, y, 8 if r < 27 else 4):
                        col = "G"
                    else:
                        col = "d"
                c.px(x, y, col)
        fr.append(c)
    return strip(fr)


# ==============================================================================================
# Petits éléments
# ==============================================================================================
@asset("shard_mini", 4, """shard_mini 24x6 = 4 images 6x6 : éclat qui tourne (100 ms/image). 0 face · 1 trois-quarts ·
2 tranche · 3 trois-quarts inversé. Or g G y + o, contour k.""")
def shard_mini():
    fr = ["..kk../.kyGk./kyGgok/kGggok/.kgok./..kk..",
          "..kk../.kyGk./.kGgk./.kGgk./.kgok./..kk..",
          "..k.../.kyk../.kGk../.kgk../.kok../..k...",
          "..kk../.kGyk./.kgGk./.kgGk./.kogk./..kk.."]
    out = []
    for s in fr:
        c = C(6, 6)
        c.put(0, 0, s)
        out.append(c)
    out[2] = out[2]
    # recentrer la tranche
    t = C(6, 6)
    t.put(1, 0, fr[2])
    out[2] = t
    return strip(out)


@asset("dither", 4, """dither 16x4 = 4 images 4x4 : trame Bayer k à 25 / 50 / 75 / 100 % (fondus d'écran sans alpha,
4 pas de 50 ms). Se répète en mosaïque (TextureRect tile).""")
def dither():
    fr = []
    for lvl in (4, 8, 12, 16):
        c = C(4, 4)
        for y in range(4):
            for x in range(4):
                if bayer(x, y, lvl):
                    c.px(x, y, "k")
        fr.append(c)
    return strip(fr)


def disc(c, cx, cy, r, col):
    for y in range(c.h):
        for x in range(c.w):
            if (x - cx) ** 2 + (y - cy) ** 2 <= r * r:
                c.px(x, y, col)


@asset("xp_badge", 2, """xp_badge 40x20 = 2 images 20x20 : pastille de niveau (le nombre est écrit par-dessus en
font_7_outline). 0 normal : disque u, anneau U/j, reflet J, contour k · 1 montée de niveau : anneau G/g,
reflets y, étincelles y aux coins.""")
def xp_badge():
    fr = []
    for lvl in (0, 1):
        c = C(20, 20)
        rim_l, rim_d, hi = ("j", "U", "J") if lvl == 0 else ("G", "g", "y")
        disc(c, 9.5, 9.5, 9.6, "k")
        disc(c, 9.5, 9.5, 8.6, rim_d)
        # moitié haut-gauche de l'anneau plus claire
        for y in range(20):
            for x in range(20):
                if c.get(x, y) == rim_d and x + y < 19:
                    c.px(x, y, rim_l)
        disc(c, 9.5, 9.5, 6.7, "k")
        disc(c, 9.5, 9.5, 5.8, "u")
        c.put(4, 3, hi + hi + "/" + hi)
        if lvl == 1:
            c.put(15, 0, ".y./yWy/.y.")
            c.px(1, 17, "y"); c.px(2, 18, "G")
        fr.append(c)
    return strip(fr)


@asset("cal_cell", 3, """cal_cell 60x28 = 3 images 20x28 (case du calendrier de la tour du jour).
0 à venir : creux b (k haut-gauche, n bas-droite), chiffre écrit en s · 1 aujourd'hui : bordure a 1 px
+ fond d, chiffre w · 2 obtenu : fond n, coche f/F en bas.""")
def cal_cell():
    fr = []
    for st in range(3):
        c = C(20, 28)
        c.rect(0, 0, 20, 28, {0: "b", 1: "d", 2: "n"}[st])
        if st == 0:
            c.ring(0, 0, 20, 28, "k", "n", cut=True)
            c.hl(1, 18, 1, "k")
        elif st == 1:
            c.ring(0, 0, 20, 28, "a", "a", cut=True)
            c.ring(1, 1, 18, 26, "k", "k")
            c.hl(2, 17, 2, "A")  # reflet au bord haut
            c.hl(2, 17, 2, "d")
        else:
            c.ring(0, 0, 20, 28, "s", "k", cut=True)
            c.hl(1, 18, 1, "s")
            chk = C(12, 12)
            chk.put(0, 0, "............/............/.........Ff./........Fff./.......Fff../.F....Fff.../"
                    ".FF..Fff..../.fFFFff...../..fFff....../...ff......./............")
            chk.outline("k")
            c.blit(chk, 4, 14)
        fr.append(c)
    return strip(fr)


@asset("codex_cell", 3, """codex_cell 108x40 = 3 images 36x40 (case du codex : le piège 32x32 se pose en x 2, y 2).
0 inconnu : fond k, trame d, bordure n, « ? » s · 1 vu : creux b, bordure s · 2 maîtrisé : creux b,
bordure G/g, reflet y, coins y.""")
def codex_cell():
    fr = []
    for st in range(3):
        c = C(36, 40)
        c.rect(1, 1, 34, 38, "k" if st == 0 else "b")
        if st == 0:
            for y in range(2, 38):
                for x in range(2, 34):
                    if bayer(x, y, 3):
                        c.px(x, y, "d")
            c.ring(0, 0, 36, 40, "n", "n", cut=True)
            q = C(12, 16)
            q.put(2, 2, ".ssss./ss..ss/....ss/...ss./..ss../..ss../....../..ss..")
            q.outline("k")
            c.blit(q, 12, 10)
        else:
            rl, rd = ("s", "n") if st == 1 else ("G", "g")
            c.ring(0, 0, 36, 40, "k", "k", cut=True)
            c.ring(1, 1, 34, 38, rl, rd)
            c.hl(2, 33, 2, "k")
            c.vl(2, 2, 37, "k")
            if st == 2:
                c.hl(3, 10, 1, "y")
                c.vl(1, 3, 8, "y")
                c.put(30, 33, "..y/.yG/yGG".replace("G", "g"))
        fr.append(c)
    return strip(fr)


@asset("star5", 2, "star5 10x5 = 2 images 5x5 : étoile de niveau 0 vide n · 1 pleine G (pointe y). Sans contour : posée sur fond sombre.")
def star5():
    c = C(10, 5)
    shape = "..X../.XXX./XXXXX/.XXX./.X.X."
    c.put(0, 0, shape.replace("X", "n"))
    c.put(5, 0, shape.replace("X", "G"))
    c.px(7, 0, "y"); c.px(6, 1, "y")
    c.px(6, 3, "g"); c.px(8, 3, "g"); c.px(6, 4, "g"); c.px(8, 4, "g")
    c.px(1, 3, "d"); c.px(3, 3, "d")
    return c


@asset("toggle", 3, """toggle 96x16 = 3 images 32x16 (bascules des réglages).
0 coupé : rail n, bouton m à gauche · 1 actif : rail f, bouton w à droite avec coche f ·
2 barre « coupé » z 2 px en diagonale, 16x16 calée à gauche (posée par-dessus une icône 16 teintée s).""")
def toggle():
    fr = []
    for st in (0, 1):
        c = C(32, 16)
        rail = "n" if st == 0 else "f"
        raild = "d" if st == 0 else "V"
        c.rect(2, 3, 28, 10, rail)
        c.ring(1, 2, 30, 12, "k", "k", cut=True)
        c.hl(2, 29, 3, raild)          # creux du rail : ombre haute
        c.hl(3, 28, 12, "s" if st == 0 else "F")
        kx = 1 if st == 0 else 17
        knob = C(14, 14)
        disc(knob, 6.5, 6.5, 6.9, "k")
        disc(knob, 6.5, 6.5, 5.9, "m" if st == 0 else "l")
        disc(knob, 6.0, 6.0, 4.9, "m" if st == 0 else "w")
        knob.put(4, 3, "ll" if st == 0 else "WW")
        knob.px(3, 4, "l" if st == 0 else "W")
        if st == 1:
            knob.put(3, 5, "......f/.....ff/f...ff./ff.ff../.fff.../..f....")
        c.blit(knob, kx, 1)
        fr.append(c)
    m = C(32, 16)
    for i in range(14):
        x, y = 1 + i, 14 - i
        m.px(x, y, "z"); m.px(x + 1, y, "Z" if i % 3 == 0 else "z")
    m.outline("k")
    fr.append(m)
    return strip(fr)


@asset("slider", 3, """slider 24x12 : x 0-7 = rail (rangées 0-3 vide : contour k, fond n ; rangées 4-7 rempli :
contour k, l + reflet p), 9-patch marges 2 · x 8-15 = curseur 8x12 normal (m, arête l) ·
x 16-23 = curseur enfoncé (l, arête w).""")
def slider():
    c = C(24, 12)
    c.rect(0, 0, 8, 4, "n")
    c.ring(0, 0, 8, 4, "k", "k", cut=True)
    c.hl(1, 6, 1, "d")
    c.rect(0, 4, 8, 4, "l")
    c.ring(0, 4, 8, 4, "k", "k", cut=True)
    c.hl(1, 6, 5, "p")
    for i, (face, edge, dark) in enumerate((("m", "l", "s"), ("l", "w", "m"))):
        x = 8 + 8 * i
        c.rect(x + 1, 1, 6, 10, face)
        c.ring(x, 0, 8, 12, "k", "k", cut=True)
        c.vl(x + 1, 1, 9, edge)
        c.hl(x + 1, x + 6, 1, edge)
        c.vl(x + 6, 2, 10, dark)
        c.hl(x + 1, x + 6, 10, dark)
        c.vl(x + 3, 4, 7, dark)
        c.vl(x + 4, 4, 7, edge)
    return c


# ==============================================================================================
# Logo (F10, repris en v2 pour le lot P0)
# ==============================================================================================
def load_px_grid(path):
    rows, ing, size = [], False, None
    for raw in open(path, encoding="utf-8"):
        line = raw.rstrip("\n")
        if not ing:
            if line.strip() == "---":
                ing = True
            elif line.strip().startswith("size:"):
                size = tuple(int(v) for v in line.split(":")[1].strip().split("x"))
            continue
        rows.append(line)
    w, h = size
    c = C(w, h)
    for y, r in enumerate(rows[:h]):
        for x, ch in enumerate(r[:w]):
            if ch != ".":
                c.px(x, y, ch)
    return c


@asset("logo", 6, """logo 960x48 = 6 images 160x48 (100 ms/image ; l'image 0 est le logo fixe).
Lettres de art/src/ui/logo.txt (dessin v1 à la main, lettres p w l k + échos c t) rendues en palette v2,
centrées dans 160x48. Images 1-5 : reflet W qui balaie les lettres en diagonale (bande de 3 px).""")
def logo():
    src = load_px_grid(os.path.join(HERE, "logo.txt"))
    ox, oy = (160 - src.w) // 2, (48 - src.h) // 2
    fr = []
    for f in range(6):
        c = C(160, 48)
        c.blit(src, ox, oy)
        if f > 0:
            band = -20 + f * 36   # position de la diagonale x + y
            for y in range(48):
                for x in range(160):
                    d = (x - ox) + (y - oy) * 0.5 - band
                    if 0 <= d < 3 and c.get(x, y) in "pw":
                        c.px(x, y, "W")
                    elif 3 <= d < 5 and c.get(x, y) == "p":
                        c.px(x, y, "w")
        fr.append(c)
    return strip(fr)


# ==============================================================================================
# Compatibilité : icons.png (21 icônes 12x12 dans l'ordre de ui_kit.gd)
# ==============================================================================================
LEGACY = ["LIFE", "LIFE_USED", "SHARD", "PLAY", "SHARE", "VIDEO", "GEAR", "SOUND_ON", "SOUND_OFF", "BACK",
          "TROPHY", "CALENDAR", "LOCK", "CHECK", "PAUSE", "FLAME", "VIBRATION", "HOME", "SKULL", "CROWN", "SCARF"]


@asset("icons", 21, """icons 252x12 = 21 icônes 12x12 : atlas de COMPATIBILITÉ pour ui_kit.gd (ordre UIK :
""" + " ".join(f"{i}={n}" for i, n in enumerate(LEGACY)) + """).
LIFE/LIFE_USED = ui_lantern 0/3 ; SHARD, LOCK, CHECK, PAUSE, FLAME, TROPHY, VIDEO = icons12 ;
les autres = anciennes grilles de art/src/ui/icons.txt rendues en palette v2.
À abandonner quand le code utilisera icons12/icons16.""")
def icons():
    old = load_px_grid(os.path.join(HERE, "icons.txt"))
    m = {"LIFE": lantern(0), "LIFE_USED": lantern(3), "SHARD": icon12("shard"), "LOCK": icon12("lock"),
         "CHECK": icon12("check"), "PAUSE": icon12("pause"), "FLAME": icon12("flame"),
         "TROPHY": icon12("trophy"), "VIDEO": icon12("video")}
    out = []
    for i, n in enumerate(LEGACY):
        if n in m:
            out.append(m[n])
        else:
            c = C(12, 12)
            for y in range(12):
                for x in range(12):
                    c.px(x, y, old.get(i * 12 + x, y))
            out.append(c)
    return strip(out)


# ==============================================================================================
# P1 / P2
# ==============================================================================================
@asset("confetti", 8, """confetti 24x3 = 8 images 3x3 : 4 couleurs (G o c j) x 2 orientations (plat, tranche).
Pas de contour (particules de 1-3 px).""")
def confetti():
    fr = []
    for col, light in (("G", "y"), ("o", "a"), ("c", "e"), ("j", "J")):
        a = C(3, 3)
        a.put(0, 0, f"{light}{col}./{col}{col}{col}/.{col}.")
        b = C(3, 3)
        b.put(0, 0, f"..{light}/.{col}./{col}..")
        fr += [a, b]
    return strip(fr)


@asset("star8", 3, """star8 24x8 = 3 images 8x8 : étoile de fin de niveau 0 vide (n, contour k) · 1 pleine (G y,
contour k) · 2 éclat (pleine + cœur W, 1 image de flash).""")
def star8():
    shape = ["...XX...", "...XX...", "XXXXXXXX", ".XXXXXX.", "..XXXX..", ".XXXXXX.", ".XX..XX.", "........"]
    shape = ["....X...", "...XX...", ".XXXXXXX", "..XXXXX.", "...XXX..", "..XXXXX.", "..XX.XX.", "........"]
    fr = []
    for st in range(3):
        c = C(8, 8)
        inner = C(8, 8)
        for y, r in enumerate(["...X....", "..XXX...", "XXXXXXX.", ".XXXXX..", "..XXX...", ".XX.XX..", ".X...X..", "........"]):
            for x, ch in enumerate(r):
                if ch == "X":
                    inner.px(x, y, "n" if st == 0 else "G")
        if st > 0:
            inner.px(3, 1, "y"); inner.px(2, 2, "y"); inner.px(3, 2, "y")
            inner.px(4, 3, "g"); inner.px(4, 4, "g"); inner.px(5, 3, "g")
        if st == 2:
            inner.px(3, 3, "W"); inner.px(3, 2, "W")
        c.blit(inner, 0, 0)
        # contour : on décale la forme d'1 px vers le bas-droite pour garder la place du contour
        c2 = C(8, 8)
        for y in range(7):
            for x in range(7):
                ch = c.get(x, y)
                if ch != ".":
                    c2.px(x + 1, y, ch) if False else None
        c.outline("k")
        fr.append(c)
    return strip(fr)


@asset("level_node", 4, """level_node 64x16 = 4 images 16x16 (carte des niveaux) : 0 verrouillé (pierre n s, cadenas k) ·
1 disponible (pierre m l, cœur a) · 2 réussi (or G y) · 3 actuel (anneau c pulsé : 1 image).""")
def level_node():
    fr = []
    for st in range(4):
        c = C(16, 16)
        rl, rd, core = {0: ("s", "n", "d"), 1: ("l", "m", "a"), 2: ("y", "G", "g"), 3: ("e", "c", "t")}[st]
        disc(c, 7.5, 7.5, 7.6, "k")
        disc(c, 7.5, 7.5, 6.6, rd)
        for y in range(16):
            for x in range(16):
                if c.get(x, y) == rd and x + y < 13:
                    c.px(x, y, rl)
        disc(c, 7.5, 7.5, 3.8, "k")
        disc(c, 7.5, 7.5, 2.9, core)
        if st == 0:
            c.put(6, 6, "kkkk/k..k/kkkk".replace(".", "d"))
            c.put(6, 6, ".kk./kddk/kkkk")
        if st == 2:
            c.px(7, 6, "y")
        fr.append(c)
    return strip(fr)


@asset("focus_ring", 1, """focus_ring 8x8, 9-patch marges 3 (P2) : anneau de focus clavier / manette, c 1 px,
coins e. Posé autour du contrôle avec 1 px d'écart.""")
def focus_ring():
    c = C(8, 8)
    c.ring(0, 0, 8, 8, "c", "c", cut=True)
    c.put(0, 0, ".e/e.")
    c.put(6, 0, "e./.e")
    c.put(0, 6, "e./.e")
    c.put(6, 6, ".e/e.")
    c.px(1, 1, "c"); c.px(6, 1, "c"); c.px(1, 6, "c"); c.px(6, 6, "c")
    c.ring(0, 0, 8, 8, "c", "c", cut=True)
    for x, y in ((1, 0), (0, 1), (6, 0), (7, 1), (0, 6), (1, 7), (7, 6), (6, 7)):
        c.px(x, y, "e")
    return c


import rpg_ui  # noqa: E402,F401  (interface v3 : remplace btn_* et ajoute cadres, jauges…)


# ----------------------------------------------------------------------------------------------
def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    render_only = "--render" in sys.argv
    names = args or list(REGISTRY)
    for n in names:
        fn, frames, doc = REGISTRY[n]
        if not render_only:
            write_grid(n, fn(), frames, doc)
        img, fr = render(n)
        print(f"ok {n}: {img.width}x{img.height} ({fr} images)")
    legacy_tap()
    contact()


def legacy_tap():
    """sprites/tap.png (32x16, lu par main.gd en régions 16x16) refait en v2 : poses A et B du picto tap de tuto16."""
    from PIL import Image
    t = Image.open(os.path.join(OUT_GAME, "tuto16.png"))
    out = Image.new("RGBA", (32, 16), (0, 0, 0, 0))
    out.paste(t.crop((0, 0, 16, 16)), (0, 0))
    out.paste(t.crop((0, 16, 16, 32)), (16, 0))
    out.save(os.path.join(os.path.dirname(OUT_GAME), "sprites", "tap.png"))
    print("sprites/tap.png (32x16, v2)")


def contact():
    """Planche générale : tous les assets x2 sur d, étiquetés (art/out/ui/planche_ui.png)."""
    from PIL import Image
    from build_fonts import text_strip
    items = []
    for n in REGISTRY:
        p = os.path.join(OUT_GAME, n + ".png")
        if os.path.exists(p):
            items.append((n, Image.open(p).convert("RGBA")))
    W = 1000
    x = y = rowh = 0
    placed = []
    for n, im in items:
        s = 2 if im.width * 2 <= W else 1
        w, h = im.width * s, im.height * s + 12
        if x + w > W:
            x, y, rowh = 0, y + rowh + 6, 0
        placed.append((n, im, s, x, y))
        x += w + 10
        rowh = max(rowh, h)
    sheet = Image.new("RGBA", (W, y + rowh + 6), hex_to_rgba(PAL["d"]))
    for n, im, s, x, y in placed:
        sheet.alpha_composite(text_strip("font_5", n.upper(), "d"), (x, y))
        sheet.alpha_composite(im.resize((im.width * s, im.height * s), Image.NEAREST), (x, y + 12))
    sheet.save(os.path.join(OUT_ART, "planche_ui.png"))
    print("planche_ui.png", sheet.size)


if __name__ == "__main__":
    main()
