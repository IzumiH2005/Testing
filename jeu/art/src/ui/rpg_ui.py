"""rpg_ui.py : interface v3 « RPG » d'ÉCHO (cadres ornés, bandeaux, jauges, médaillons).

Importé par build_ui.py : chaque @asset s'ajoute au registre commun.
Rebuild : python3 build_ui.py frame title_plate divider gauge medal slot laurel hud_plate colbar btn_main btn_alt btn_echo
"""
from uicore import C, strip, bayer, asset

# Métaux : (lumière, base, ombre, reflet)
STEEL = ("p", "l", "m", "w")
GOLD = ("G", "g", "o", "y")


def disc(c, cx, cy, r, col):
    for y in range(c.h):
        for x in range(c.w):
            if (x - cx) ** 2 + (y - cy) ** 2 <= r * r:
                c.px(x, y, col)


def flipv(t):
    o = C(t.w, t.h)
    for y in range(t.h):
        o.g[y] = t.g[t.h - 1 - y][:]
    return o


def mirror4(c, tile, ox=0, oy=0):
    """Pose un motif de coin haut-gauche (C) aux quatre coins de c, en miroir."""
    for fx in (False, True):
        for fy in (False, True):
            t = tile
            if fx:
                t = t.fliph()
            if fy:
                t = flipv(t)
            x = c.w - t.w - ox if fx else ox
            y = c.h - t.h - oy if fy else oy
            c.blit(t, x, y)


def bracket(size, arm, metal, gem):
    """Équerre de métal de coin (haut-gauche) : deux bras d'épaisseur `arm`, pointes en flèche,
    rivet-gemme dans l'angle, contour k. metal = (lumière, base, ombre, reflet)."""
    L, M, D, H = metal
    c = C(size, size)
    mask = set()
    for y in range(size):
        for x in range(size):
            if (x <= arm and y <= size - 2) or (y <= arm and x <= size - 2):
                mask.add((x, y))
    # pointes : les bras s'affinent sur les 2 derniers pixels
    for t in range(2):
        e = size - 3 + t
        for k in range(arm + 1):
            if t == 0 and k in (0, arm):
                mask.discard((e, k)); mask.discard((k, e))
            if t == 1 and abs(k - arm / 2) > 0.6:
                mask.discard((e, k)); mask.discard((k, e))
    mask.discard((0, 0))
    for (x, y) in mask:
        if x == 0 or y == 0:
            col = "k"
        elif x == 1 or y == 1:
            col = L
        elif (y == arm and x > arm) or (x == arm and y > arm):
            col = D
        else:
            col = M
        c.px(x, y, col)
    c.px(1, 1, H)
    c.px(2, 1, H)
    c.px(1, 2, H)
    # contour k vers l'intérieur
    src = set(mask)
    for (x, y) in list(src):
        for dx, dy in ((1, 0), (0, 1), (1, 1)):
            p = (x + dx, y + dy)
            if p not in src and 0 < p[0] < size and 0 < p[1] < size:
                c.px(p[0], p[1], "k")
    # gemme dans l'angle (losange 3x3 + cœur)
    g0, g1, g2 = gem
    gx = gy = arm // 2 + 1
    c.px(gx, gy - 1, g0); c.px(gx - 1, gy, g0)
    c.px(gx, gy, g1)
    c.px(gx + 1, gy, g2); c.px(gx, gy + 1, g2)
    return c


# ==============================================================================================
# Cadre de panneau orné
# ==============================================================================================
FRAMES = [
    # nom      métal  filet (clair, sombre)  gemme (clair, cœur, ombre)
    ("pierre", STEEL, ("G", "g"), ("y", "G", "g")),
    ("echo",   STEEL, ("c", "t"), ("e", "c", "t")),
    ("danger", STEEL, ("z", "X"), ("Z", "z", "X")),
    ("record", GOLD,  ("y", "G"), ("W", "y", "G")),
]


def frame_one(metal, trim, gem):
    S = 32
    c = C(S, S)
    c.rect(1, 1, S - 2, S - 2, "d")
    c.ring(0, 0, S, S, "k", "k", cut=True)
    c.ring(1, 1, S - 2, S - 2, "m", "n")       # arête éclairée haut-gauche
    c.ring(2, 2, S - 4, S - 4, "s", "n")
    c.ring(3, 3, S - 6, S - 6, "n", "d")
    c.ring(4, 4, S - 8, S - 8, "k", "k")       # gorge
    c.ring(5, 5, S - 10, S - 10, trim[0], trim[1])   # filet de couleur
    c.ring(6, 6, S - 12, S - 12, "k", "k")
    c.hl(7, S - 8, 7, "b")                     # ombre intérieure (le fond est en retrait)
    c.vl(7, 7, S - 8, "b")
    # pierre : quelques joints sombres sur la bordure (pas dans la zone étirée)
    for (x, y) in ((8, 2), (8, 3), (2, 8), (3, 8)):
        pass
    br = bracket(13, 4, metal, gem)
    mirror4(c, br)
    return c


@asset("frame", 4, """frame 128x32 = 4 images 32x32, 9-patch marges 13 (content 13/12/13/12).
Cadre de panneau « RPG ». Bordure de pierre 4 px (arête l/n, m/s, s/n) + gorge k + filet de couleur + k,
fond d avec ombre intérieure b. Équerres de métal aux 4 coins (bras 4 px, pointes en flèche, contour k)
avec gemme dans l'angle. 0 pierre (acier, filet or) · 1 écho (acier, filet et gemme cyan) ·
2 danger (acier, filet et gemme magenta) · 3 record (équerres or, filet y/G).""")
def frame():
    return strip([frame_one(m, t, g) for _, m, t, g in FRAMES])


# ==============================================================================================
# Bandeau-titre (ruban posé à cheval sur le haut du cadre)
# ==============================================================================================
PLATES = [
    # face, haut, reflet, ombre, queue, pli
    ("s", "m", "l", "n", "n", "d"),     # acier
    ("G", "y", "W", "g", "g", "o"),     # or
    ("X", "z", "Z", "x", "x", "r"),     # danger
    ("t", "c", "e", "q", "q", "k"),     # écho
]


def plate_one(face, top, glint, shadow, tail, fold):
    W, H = 48, 22
    c = C(W, H)
    # queues (derrière le ruban), en queue d'aronde
    for side in (0, 1):
        t = C(10, 14)
        t.rect(0, 0, 10, 14, tail)
        t.hl(0, 9, 0, shadow if tail != shadow else fold)
        for y in range(14):
            d = 3 - abs(y - 6.5) // 1 if abs(y - 6.5) < 3 else 0
            for x in range(int(d)):
                t.px(x, y, ".")
        tt = C(12, 16)
        tt.blit(t, 1, 1)
        tt.outline("k")
        if side:
            tt = tt.fliph()
        c.blit(tt, 0 if side == 0 else W - 12, 6)
    # pli : la queue passe derrière le ruban (coin sombre sous la bande)
    for x0 in (7, W - 10):
        c.rect(x0, 18, 3, 2, fold)
    # ruban principal
    x0, x1, y0, y1 = 6, W - 7, 1, 17
    c.rect(x0, y0, x1 - x0 + 1, y1 - y0 + 1, face)
    c.hl(x0, x1, y0, "k"); c.hl(x0, x1, y1, "k")
    c.vl(x0, y0, y1, "k"); c.vl(x1, y0, y1, "k")
    c.hl(x0 + 1, x1 - 1, y0 + 1, top)
    c.hl(x0 + 1, x1 - 1, y0 + 2, top)
    c.hl(x0 + 1, x1 - 1, y1 - 1, shadow)
    c.hl(x0 + 1, x1 - 1, y1 - 2, shadow)
    c.vl(x0 + 1, y0 + 1, y1 - 1, top)
    c.vl(x1 - 1, y0 + 3, y1 - 1, shadow)
    # double filet gravé
    c.hl(x0 + 3, x1 - 3, y0 + 3, shadow)
    c.hl(x0 + 3, x1 - 3, y1 - 3, top)
    # reflet
    c.hl(x0 + 2, x0 + 5, y0 + 1, glint)
    c.px(x0 + 1, y0 + 2, glint)
    # rivets aux deux bouts
    for rx in (x0 + 3, x1 - 4):
        c.put(rx, 8, ".k./kGk/.k." if face != "G" else ".k./kWk/.k.")
        c.px(rx + 1, 8, "k")
    return c


@asset("title_plate", 4, """title_plate 192x22 = 4 images 48x22, 9-patch marges gauche/droite 14, haut/bas 0.
Bandeau-titre en ruban : bande x 6-41 y 1-17 (contour k, biseau 2 rangées, ombre 2 rangées, double filet
gravé, reflet, rivet à chaque bout) ; queues en queue d'aronde derrière (y 6-21) avec pli sombre.
0 acier (texte W) · 1 or (texte k) · 2 danger (texte W) · 3 écho (texte k). Texte font_7 centré, y 4-13.""")
def title_plate():
    return strip([plate_one(*p) for p in PLATES])


# ==============================================================================================
# Séparateur orné
# ==============================================================================================
@asset("divider", 3, """divider 72x9 = 3 images 24x9 : 0 bout gauche (volute + filet) · 1 gemme centrale (posée
une fois, 24 de large dont 9 utiles centrés) · 2 bout droit (miroir). Bouts : 9-patch marge 10 du côté
volute, 0 de l'autre ; filet l (haut) / k (ombre). Gemme : losange or G/y/g, contour k, ailettes acier.""")
def divider():
    left = C(24, 9)
    left.hl(6, 23, 4, "l")
    left.hl(6, 23, 5, "k")
    # volute : petit enroulement + point
    left.put(0, 1, ".kkk./kmlmk/klkmk/kmkk./.kk..")
    left.put(4, 3, "kl/km")
    right = left.fliph()
    gem = C(24, 9)
    gem.hl(0, 23, 4, "l")
    gem.hl(0, 23, 5, "k")
    gem.put(7, 0, "....k..../...kyk.../..kyGgk../.kyGGGgk./kmGGGGgmk/.kgGGgok./..kgook../...kok.../....k....")
    return strip([left, gem, right])


# ==============================================================================================
# Jauge segmentée
# ==============================================================================================
FILLS = [
    ("y", "G", "G", "g", "g", "o"),      # 1 or (meilleure vie, record)
    ("e", "c", "c", "t", "t", "q"),      # 2 écho
    ("Z", "z", "z", "X", "X", "x"),      # 3 danger
    ("J", "j", "j", "U", "U", "u"),      # 4 marée
    ("p", "l", "l", "m", "m", "s"),      # 5 acier
]


@asset("gauge", 7, """gauge 56x10 = 7 images 8x10.
0 cadre : contour k arrondi, rail d'acier 1 px (m en haut, n en bas), auge b avec ombre k en haut ;
9-patch marges 3 ; le remplissage se pose en x 2, y 2, hauteur 6.
1-5 remplissages 8x6 (en haut de l'image, rangées 0-5) : 1 or · 2 écho · 3 danger · 4 marée · 5 acier ;
rangée 0 reflet, 1-2 base claire, 3-4 base, 5 ombre ; colonne 7 = bout lumineux (9-patch droite 1).
6 graduation 8x6 : colonne 7 en k (rangées 1-5), à répéter en mosaïque par-dessus le remplissage.""")
def gauge():
    fr = []
    c = C(8, 10)
    c.rect(1, 1, 6, 8, "b")
    c.ring(0, 0, 8, 10, "k", "k", cut=True)
    c.hl(1, 6, 1, "m")
    c.hl(1, 6, 8, "n")
    c.vl(1, 2, 7, "s")
    c.vl(6, 2, 7, "n")
    c.hl(2, 5, 2, "k")
    fr.append(c)
    for f in FILLS:
        c = C(8, 10)
        for y, col in enumerate(f):
            c.hl(0, 7, y, col)
        c.vl(7, 0, 5, f[0])
        c.px(7, 5, f[2])
        fr.append(c)
    t = C(8, 10)
    t.vl(7, 1, 5, "k")
    fr.append(t)
    return strip(fr)


@asset("colbar", 4, """colbar 24x6 = 4 images 6x6 (barres verticales de l'histogramme), 9-patch marges 2.
0 cadre (contour k, auge b, ombre k à gauche) · 1 écho (colonnes e c t q) · 2 or (y G g o) · 3 vide (n).""")
def colbar():
    fr = []
    c = C(6, 6)
    c.rect(1, 1, 4, 4, "b")
    c.ring(0, 0, 6, 6, "k", "k", cut=True)
    c.vl(1, 1, 4, "k")
    fr.append(c)
    for cols in (("e", "c", "t", "q"), ("y", "G", "g", "o"), ("s", "n", "n", "d")):
        c = C(6, 6)
        for i, col in enumerate(cols):
            c.vl(1 + i, 1, 4, col)
        c.hl(1, 4, 1, cols[0])
        c.ring(0, 0, 6, 6, "k", "k", cut=True)
        fr.append(c)
    return strip(fr)


# ==============================================================================================
# Médaillon, case, laurier, plaque de HUD
# ==============================================================================================
@asset("medal", 3, """medal 48x16 = 3 images 16x16 : médaillon de rang (le chiffre se pose au centre en font_5).
Disque contour k, anneau de métal (lumière haut-gauche, ombre bas-droite), creux b au centre.
0 acier · 1 or (meilleure vie) · 2 écho (cyan).""")
def medal():
    fr = []
    for L, M, D, H in (STEEL, GOLD, ("c", "t", "q", "e")):
        c = C(16, 16)
        disc(c, 7.5, 7.5, 7.6, "k")
        disc(c, 7.5, 7.5, 6.6, D)
        disc(c, 7.0, 7.0, 6.0, M)
        disc(c, 6.6, 6.6, 5.2, L)
        disc(c, 7.5, 7.5, 4.9, M)
        disc(c, 7.5, 7.5, 4.0, "k")
        disc(c, 7.5, 7.5, 3.4, "b")
        c.px(4, 3, H); c.px(3, 4, H); c.px(5, 2, H)
        fr.append(c)
    return strip(fr)


@asset("slot", 3, """slot 48x14 = 3 images 16x14, 9-patch marges 4 (cases de valeur : hauteur, éclats).
Creux k/b : ombre k en haut-gauche, lèvre m en bas-droite, contour k, coins coupés.
0 acier · 1 liseré or (G en haut, g en bas) · 2 liseré cyan (c / t).""")
def slot():
    fr = []
    for top, bot in (("m", "s"), ("G", "g"), ("c", "t")):
        c = C(16, 14)
        c.rect(1, 1, 14, 12, "b")
        c.ring(0, 0, 16, 14, "k", "k", cut=True)
        c.ring(1, 1, 14, 12, "k", top)
        c.hl(2, 13, 2, "k")
        c.px(14, 1, bot); c.px(1, 12, bot)
        c.hl(3, 12, 12, top)
        c.px(2, 12, bot); c.px(13, 12, bot)
        fr.append(c)
    return strip(fr)


@asset("laurel", 2, """laurel 32x24 = 2 images 16x24 : rameau de laurier or (à gauche du score record ; image 1 = miroir).
Feuilles G/y, nervures g, tige o, contour k.""")
def laurel():
    c = C(16, 24)
    # tige en arc
    stem = [(11, 22), (10, 21), (9, 20), (8, 19), (7, 18), (7, 17), (6, 16), (6, 15), (6, 14), (6, 13),
            (6, 12), (6, 11), (7, 10), (7, 9), (8, 8), (8, 7), (9, 6), (10, 5)]
    for x, y in stem:
        c.px(x, y, "o")
    # feuilles : paires le long de la tige (gauche = extérieur)
    leaf_l = "..yG/.yGg/yGg./Gg.."
    leaf_r = "Gy../gGy./.gGy/..gG"
    for (x, y) in ((2, 15), (2, 11), (3, 7), (5, 3)):
        c.put(x, y, leaf_l)
    for (x, y) in ((8, 13), (8, 9), (9, 5)):
        c.put(x, y, leaf_r)
    c.put(9, 1, ".y/yG/G.")
    c.outline("k")
    return strip([c, c.fliph()])


@asset("hud_plate", 2, """hud_plate 48x24 = 2 images 24x24, 9-patch marges 7 (plaques du HUD et des toasts).
0 sombre : fond b, bordure k / n / s (arête m en haut), mini-équerres acier aux coins, contour k.
1 or : idem, arête et équerres or (toasts de récompense).""")
def hud_plate():
    fr = []
    for metal in (STEEL, GOLD):
        L, M, D, H = metal
        c = C(24, 24)
        c.rect(1, 1, 22, 22, "b")
        c.ring(0, 0, 24, 24, "k", "k", cut=True)
        c.ring(1, 1, 22, 22, "s", "n")
        c.hl(2, 21, 1, "m")
        c.ring(2, 2, 20, 20, "k", "k")
        c.hl(3, 20, 3, "d")
        corner = C(6, 6)
        corner.put(0, 0, "kkkkk./k" + H + L + L + "k./k" + L + "kkk./k" + L + "k.../kk..../......")
        mirror4(c, corner)
        fr.append(c)
    return strip(fr)


# ==============================================================================================
# Boutons v3 : cadre de métal + face colorée biseautée, coins coupés à 45°
# ==============================================================================================
BTN3 = {
    #        face top  glint shadow edge   métal (lumière, ombre)
    "main": ("o", "a", "A", "R", "r", ("y", "g")),
    "alt":  ("s", "m", "l", "n", "d", ("l", "n")),
    "echo": ("c", "e", "W", "t", "q", ("e", "t")),
}


def oct_ring(c, x0, y0, x1, y1, tl, br, cut=2):
    """Anneau octogonal (coins coupés de `cut`)."""
    for x in range(x0 + cut, x1 - cut + 1):
        c.px(x, y0, tl); c.px(x, y1, br)
    for y in range(y0 + cut, y1 - cut + 1):
        c.px(x0, y, tl); c.px(x1, y, br)
    for i in range(1, cut):
        c.px(x0 + i, y0 + cut - i, tl)
        c.px(x1 - i, y0 + cut - i, br if i < cut / 2 else tl)
        c.px(x0 + i, y1 - cut + i, br if i >= cut / 2 else tl)
        c.px(x1 - i, y1 - cut + i, br)


def oct_fill(c, x0, y0, x1, y1, col, cut=2):
    for y in range(y0, y1 + 1):
        d = max(0, cut - (y - y0), cut - (y1 - y))
        for x in range(x0 + d, x1 - d + 1):
            c.px(x, y, col)


def button3(face, top, glint, shadow, edge, metal, pressed=False):
    c = C(48, 24)
    dy = 2 if pressed else 0
    # socle (épaisseur) : visible seulement au repos
    oct_fill(c, 0, dy, 47, 23, "k", 3)
    oct_fill(c, 1, dy + 1, 46, 22, metal[1], 2)       # cadre de métal (ombre)
    oct_fill(c, 1, dy + 1, 46, 22 - (0 if pressed else 2), metal[0], 2)
    # face
    fy1 = 19 if not pressed else 21
    oct_fill(c, 3, dy + 3, 44, fy1, "k", 1)
    oct_fill(c, 4, dy + 4, 43, fy1 - 1, face, 1)
    c.hl(5, 42, dy + 4, top)
    c.hl(4, 43, dy + 5, top)
    c.vl(4, dy + 5, fy1 - 2, top)
    c.vl(43, dy + 6, fy1 - 1, shadow)
    c.hl(5, 43, fy1 - 1, shadow)
    if not pressed:
        c.hl(5, 42, fy1 - 2, shadow)
        c.hl(6, 9, dy + 4, glint)
        c.px(5, dy + 5, glint)
    # épaisseur sous la face (au repos)
    if not pressed:
        c.hl(3, 44, 20, edge)
        c.hl(2, 45, 21, edge)
    # rivets du cadre
    for rx in (2, 45):
        c.px(rx, dy + 11, "k")
    return c


def button3_set(kind):
    face, top, glint, shadow, edge, metal = BTN3[kind]
    normal = button3(face, top, glint, shadow, edge, metal)
    pressed = button3(face, top, None, shadow, edge, metal, True)
    disabled = button3("n", "s", None, "d", "d", ("s", "n"), True)
    return strip([normal, pressed, disabled])


BTN3_DOC = """btn_{k} 144x24 = 3 images 48x24 : 0 normal · 1 enfoncé · 2 désactivé (v3 RPG).
9-patch marges gauche 8, droite 8, haut 8, bas 8. Octogone (coins coupés), contour k, cadre de métal 2 px
({m}), face {f} biseautée (haut {t} + reflet {g}, ombre {s}), épaisseur {e} sous la face au repos.
Enfoncé : tout descend de 2 px, plus d'épaisseur. Désactivé : face n, cadre acier sombre."""


@asset("btn_main", 3, BTN3_DOC.format(k="main", m="or y/g", f="o", t="a", g="A", s="R", e="r"))
def btn_main():
    return button3_set("main")


@asset("btn_alt", 3, BTN3_DOC.format(k="alt", m="acier l/n", f="s", t="m", g="l", s="n", e="d"))
def btn_alt():
    return button3_set("alt")


@asset("btn_echo", 3, BTN3_DOC.format(k="echo", m="e/t", f="c", t="e", g="W", s="t", e="q"))
def btn_echo():
    return button3_set("echo")
