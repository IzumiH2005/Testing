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
            rt = (6.4 + 3.6 * (1 - u / 0.62)) if u < 0.62 else 0
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
    # 3 rayons sombres qui tournent avec la lame (lecture de la rotation au centre)
    for k in range(3):
        a = rot + k * 2 * math.pi / 3 + math.pi / 6
        for rr in (3.4,):
            hx, hy = round(C + rr * math.cos(a)), round(C + rr * math.sin(a))
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
ÉCHO - O2 scie gravée : même sprite recoloré (q t c e, contour q), bande 96x24 = 4 images de 24x24, 20 fps,
même ancrage que saw (p - (12,12)) : scies et ennemis gravés continuent de tourner.
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


# ======================================================================= 4. CONTREFORT (Fonderie : acier 1 2 3 4)
SPK_UP = G("""
...k...k...k..
..kzk.kzk.kzk.
.kzXxkzXxkzXxk
.kzXxxzXxxzXxk
.kxxxxxxxxxxxk
""")


def buttress_block(h):
    rows = []
    for r in range(h):
        if r == 0 or r == h - 1:
            rows.append("k" * 16)
            continue
        row = []
        for c in range(16):
            if c == 15:
                ch = "k"
            elif c == 14:
                ch = "4"            # arête accrochable (face côté couloir)
            elif c == 13:
                ch = "1"            # terminateur avant l'arête
            elif r == 1:
                ch = "4" if c < 2 else "3"
            elif r == h - 2:
                ch = "1"
            elif r % 16 == 0:
                ch = "1"            # joint de plaque
            elif r % 16 == 1:
                ch = "3"            # arête haute de la plaque suivante
            else:
                ch = "2"
            row.append(ch)
        rows.append("".join(row))
    rows = [list(r) for r in rows]
    for p0 in range(0, h - 8, 16):        # 2 rivets par plaque, groupe de 2 [A5-9]
        for cx in (3, 9):
            ry = p0 + 5
            if ry < h - 3:
                rows[ry][cx] = "4"
                rows[ry + 1][cx] = "1"
    return ["".join(r) for r in rows]


def buttress_frame(h):
    up = pad(SPK_UP, 16, 5)
    down = list(reversed(up))
    return up + buttress_block(h) + down


@asset
def buttress():
    write("buttress", """
ÉCHO - O3 contrefort à épines (Fonderie froide : acier 1 2 3 4), mur GAUCHE, cellule 16x58, 2 images.
  0 = hauteur 32 (rangées 0-41 utilisées), 1 = hauteur 48 (rangées 0-57). Ancrage : coin haut-gauche à (bx, y0-5), bx = WL.
Intention : un bloc d'acier accrochable (arête 4 sur la face côté couloir) hérissé de dents dessus et dessous.
Géométrie : épines de 5 px x 2-13 au-dessus (hz.gd Rect2(bx+2, y0-5, 12, 5)) et au-dessous (Rect2(bx+2, y1, 12, 5)).
Lumière haut-gauche : dessus 3 + coin 4, joints 1 sous chaque plaque, terminateur 1 avant l'arête ; dents z à gauche, x à droite.
Timing : statique (1 image par hauteur).
Budget : k 1 2 3 4 + x X z = 8 ; par masse : acier 5, épines 4 (k partagé). Détail : 2 rivets par plaque.
Défaut corrigé : dents de 4 px avec double contour kk entre deux dents ; passé à des dents de 3 px à contour k partagé.
""", [buttress_frame(32), buttress_frame(48)], 16, 58)


# ======================================================================= 5. HERSE (fentes x permanentes)
SPEAR = G("""
................kkk.....
kkkkkkkkkkkkkkkkzzzzkk..
zzzzzzzzzzzzzzzzzXXXzZZk
XXXXXXXXXXXXXXXXxXXXXXxk
kkkkkkkkkkkkkkkkxxxxkk..
................kkk.....
""")
SLOT = G("""
kkk
xxk
xxk
kkk
""")


def herse_frame(ext, glint=False):
    rows = ["." * 24 for _ in range(32)]
    for p in range(0, 32, 8):
        rows = over(rows, SLOT, 0, p + 2)
        if ext > 0:
            sp = [r[24 - ext:] for r in SPEAR]
            rows = over(rows, sp, 0, p + 1)
            if glint:
                rows = over(rows, ["W"], ext - 2, p + 3)
    return rows


@asset
def portcullis():
    write("portcullis", """
ÉCHO - O9 herse (lances murales), mur GAUCHE, cellule 24x32, 5 images. Motif de 8 px : la cellule se répète
(ou se coupe) verticalement de y0 à y1. Ancrage : coin haut-gauche à (hx, y0), hx = WL ; 1 lance par bande de 8 px.
Intention : des fentes qui couvent le danger (x permanentes) d'où jaillissent des lances jusqu'à 24 px.
Timing (E3) : img | rôle | change | principe | durée
  0 | rentrée (état 0) | fentes x seules | tenue | tant que l'état vaut 0
  1 | préavis (état 1) | pointes sorties de 4 px | anticipation | 0,3-0,4 s (le code clignote à 10 Hz)
  2 | sortie (état 2) | lances à 24 px + éclat W sur la pointe | extrême / impact | 1/12 s
  3 | sortie tenue (état 2) | lances à 24 px | tenue | reste de l'état 2
  4 | rentrée | lances à 12 px | amorti | 1/12 s au début de l'état 0, puis image 0
Hitbox (hz.gd Rect2(hx, y0+2, 24, y1-y0-4)) = images 2-3 ; l'image 4 n'est pas létale (le code l'affiche après).
Budget : k x X z Z (+ W de l'éclat) = 6.
Défaut corrigé : v1 fer de lance « bulbe » (bord 2-1-3, se lisait comme un bouton) ; fer en flèche 3-2-2 + barbes.
""", [herse_frame(0), herse_frame(4), herse_frame(24, True), herse_frame(24), herse_frame(12)], 24, 32)


@asset
def portcullis_echo():
    write("portcullis_echo", """
ÉCHO - O9 herse gravée : pointes figées sorties, 24x32, 1 image (échange x->q X->t z->c Z->e k->q).
Budget : q t c e = 4. Défaut corrigé : le W de l'éclat n'est pas repris (image 3, sans éclat).
""", [recolor(herse_frame(24))], 24, 32)


# ======================================================================= 6. MÂCHOIRES (acier 1 2 3 4 + mâchoire X)
def steel_body(w=16):
    rows = ["." * w, "." * w, "k" * w]
    rows.append("3" * w)
    for r in range(4, 20):
        rows.append("2" * (w - 1) + "1")
    rows.append("1" * w)
    rows.append("k" * w)
    rows += ["." * w, "." * w]
    g = [list(r) for r in rows]
    for cx in (4, 9):
        g[7][cx] = "4"; g[8][cx] = "1"
        g[16][cx] = "4"; g[17][cx] = "1"
    return ["".join(r) for r in g]


TOOTH = G("""
k...
zkk.
XzZk
xkk.
k...
""")


def jaw_head(shift=0, warn=False):
    body = steel_body(16)
    g = [list(r) for r in body]
    for r in range(2, 22):
        g[r][8] = "k"
        g[r][9] = "k" if r in (2, 21) else "z"
        g[r][10] = "k" if r in (2, 21) else "X"
        g[r][11] = "k" if r in (2, 21) else "x"
        for c in range(12, 16):
            g[r][c] = "."
    for c in range(0, 8):
        g[3][c] = "3"
    rows = ["".join(r) for r in g]
    t = TOOTH if not warn else [r.replace("z", "Z").replace("X", "z") for r in TOOTH]
    for k in range(4):
        rows = over(rows, t, 12, 2 + k * 5)
    if shift:
        rows = ["." * shift + r[:-shift] for r in rows]
    if warn:
        rows = over(rows, ["p"], 3, 0)
        rows = over(rows, ["p"], 6, 1)
        rows = over(rows, ["p"], 4, 23)
    return rows


@asset
def jaws():
    write("jaws", """
ÉCHO - O10 mâchoires (Fonderie : acier 1 2 3 4 + mâchoire X), mur GAUCHE, cellule 16x24, 3 images.
  0 = corps : bloc d'acier bouclable en x, à répéter derrière la tête de WL à WL+ext-16 ;
  1 = tête au repos (ouvert / fermeture / fermé) ; 2 = tête en préavis : 1 px plus loin (tremblement) + dents allumées + 3 poussières p.
Ancrage : tête coin haut-gauche à (WL+ext-16, mid-12) ; corps à (WL+16*i, mid-12). Rangées 2-21 = hitbox 20 px (mid-10..mid+10).
Mur droit : même image retournée, tête à (WR-ext, mid-12). Pour ext < 16, la tête sort du mur (le mur se dessine par-dessus).
Intention : un étau d'acier dont seule la gueule est magenta : on lit « ça écrase » par les dents, pas par la masse.
Timing (cycle de 3 s de hz.gd) : img | rôle | durée
  1 | ouvert | 1,6 s (tenue)
  2 | préavis (alterner 1/2 à 10 Hz = tremblement de 1 px) | 0,5 s (anticipation)
  1 | fermeture 0,15 s (le code déplace ext) puis fermé 0,45 s puis réouverture 0,3 s
Budget : acier k 1 2 3 4 + mâchoire z X x (+ Z au préavis, p poussière) = 8 par image au plus ; détail : 2 rivets groupés.
Défaut corrigé : dents carrées 2x2 du dessin de repli -> dents triangulaires de 5 px, 4 par mâchoire, pointe Z.
""", [steel_body(16), jaw_head(), jaw_head(1, True)], 16, 24)


@asset
def jaws_echo():
    b = steel_body(16)
    b = [r.replace("k", "q") for r in b]
    b = list(b)
    b[3] = "c" * 16
    b[20] = "t" * 16
    write("jaws_echo", """
ÉCHO - O10 mâchoires gravées : bloc fermé en pont, 16x24 bouclable en x de WL à WR, 1 image ; ancrage (x, mid-12).
Intention : les deux mâchoires soudées deviennent un pont accrochable : dessus c, dessous t, contour q.
Budget : q t c + acier 1 2 4 = 6. Défaut corrigé : sans dents (un pont n'a pas de gueule).
""", [b], 16, 24)



@asset
def buttress_echo():
    up = [r.replace("k", "q") for r in pad(SPK_UP, 16, 5)]
    up[0] = "." * 16                                      # pointes émoussées d'1 px
    up = recolor(up)
    f = up + buttress_block(32) + list(reversed(up))
    f2 = up + buttress_block(48) + list(reversed(up))
    write("buttress_echo", """
ÉCHO - O3 contrefort gravé : même bloc d'acier, épines en cristal émoussé d'1 px (q t c), 16x58, 2 images (h32, h48).
Même ancrage que buttress. Budget : acier k 1 2 3 4 + q t c = 8 (deux masses). Défaut corrigé : pointe k retirée -> plateau.
""", [f, f2], 16, 58)


# ======================================================================= 7. PLAQUE FRIABLE (non létale, acier + liseré 4)
def crumble_block():
    rows = []
    for r in range(16):
        if r == 0:
            rows.append(list("1kkk"))
            continue
        c1 = "3" if r == 1 else ("1" if r == 15 else "2")
        c2 = "4" if r % 2 == 0 else "2"
        rows.append(list("1" + c1 + c2 + "k"))
    for ry in (5, 11):
        rows[ry][1] = "4"
        rows[ry + 1][1] = "1"
    return ["".join(r) for r in rows]


def crumble_frame(stage):
    blk = crumble_block()
    g = [list(r) for r in blk]
    if stage >= 1:
        for x, y in ((1, 8), (2, 9)):
            g[y][x] = "k"
    if stage >= 2:
        for x, y in ((1, 2), (2, 3), (0, 9), (1, 10)):
            g[y][x] = "k"
    blk = ["".join(r) for r in g]
    if stage == 2:                       # la moitié basse a glissé d'1 px
        blk = blk[:9] + ["1..k"] + blk[9:15]
    rows = [r.ljust(16, ".") for r in blk + blk]
    if stage == 3:                       # chute : 3 morceaux qui tombent et s'écartent + 3 débris
        out = ["." * 16 for _ in range(32)]
        for b in (0, 16):
            out = over(out, [r[:4] for r in blk[0:6]], 1, b + 3)
            out = over(out, [r[:4] for r in blk[6:11]], 3, b + 9)
            out = over(out, [r[:4] for r in blk[11:16]], 2, b + 14)
            out = over(out, ["2"], 8, b + 7)
            out = over(out, ["3"], 7, b + 12)
            out = over(out, ["1"], 10, b + 15)
        rows = out
    return rows


@asset
def crumble():
    write("crumble", """
ÉCHO - O11 plaque friable (non létale), Fonderie : acier 1 2 3 4 + liseré pointillé 4, rivets. Mur GAUCHE.
Cellule 16x32, 4 images ; motif de 16 px répété (la cellule se coupe ou se répète de y0 à y1).
Ancrage : coin haut-gauche à (WL-4, y0) (= fx de world_draw) : la plaque occupe x 0-3, collée/encastrée dans la face du mur ;
les colonnes 4-15 servent aux morceaux qui tombent. Mur droit : image retournée, coin à (WR+4-16, y0).
Intention : une plaque qu'on lit « fragile » avant de l'agripper : liseré en pointillé (ni magenta, ni cyan, §7).
Timing (E3) : img | rôle | change | durée
  0 | intacte | liseré 4 pointillé, 2 rivets | tenue
  1 | fissure 1 | fêlure k en escalier | 1re moitié du tremblement (0,17 s ; le code tremble de 1 px)
  2 | fissure 2 | 2e fêlure + moitié basse descendue d'1 px | 2e moitié (0,18 s)
  3 | chute | 3 morceaux écartés + 3 débris | 1/8 s, puis rien pendant 3 s (le code peut glisser l'image vers le bas)
Budget : k 1 2 3 4 = 5 couleurs. Défaut corrigé : fêlure 2x2 en carré (bloc) -> escalier diagonal d'1 px.
""", [crumble_frame(i) for i in range(4)], 16, 32)


# ======================================================================= 8. ÉBOULIS DE LIVRES (Bibliothèque 6 7 8, contour x)
BOOKS = G("""
................
................
....xxxxxxxxx...
....x8777776x...
....x7zz7766x...
..xxxxxxxxxxxx..
..x877777777x...
..x7777zz776x...
..x666666666x...
..xxxxxxxxxxxxx.
...x8777777776x.
...x77777zz76x..
...x66666666x...
...xxxxxxxxxx...
................
................
""")


def books_clean():
    g = [list(r) for r in BOOKS]
    return ["".join(r) for r in g]


@asset
def rockfall_books():
    write("rockfall_books", """
ÉCHO - O12 éboulis de livres (Bibliothèque engloutie), cellule 16x16, 1 image. Ancrage : coin haut-gauche à (x-8, ry-8).
Intention : une pile de 3 livres qui tue : la matière est celle du biome (6 7 8), le contour x et la marque z disent « danger ».
Géométrie : masse x 2-14 / y 2-13 ; hitbox 10x10 de hz.gd (x-5, ry-5) = x 3-12, y 3-12 (dépassement 1-2 px, §9.1).
Lumière haut-gauche : coin 8 sur chaque dos, dessous 6 ; une seule marque zz sur le livre du milieu.
Timing : statique ; le préavis est rockfall_mark (0,6 s) + le tremblement de 1 px du code.
Budget : k x X z + 6 7 8 = 7 couleurs (contour X + liseré k, seule entorse au budget). Défauts corrigés : livres alignés (lecture « brique ») -> 3 largeurs décalées ; passe 2 : une étiquette zz par livre (le violet seul ne disait pas « danger » sur le fond) ;\n contour extérieur X + liseré k : la pile se détache du fond sombre.
""", [books_hot()], 16, 16)


def books_hot():
    """Passe 2 : contour extérieur en X (lecture danger à x1), séparations internes en x, puis liseré k."""
    g = [list(r) for r in books_clean()]
    H, W = len(g), len(g[0])
    def empty(x, y):
        return not (0 <= x < W and 0 <= y < H) or g[y][x] == "."
    out = [r[:] for r in g]
    for y in range(H):
        for x in range(W):
            if g[y][x] == "x" and any(empty(x + a, y + b) for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                out[y][x] = "X"
            elif g[y][x] == "." and any(not empty(x + a, y + b) for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                out[y][x] = "k"
    return ["".join(r) for r in out]


@asset
def rockfall_books_echo():
    m = {"x": "q", "z": "e", "8": "c", "7": "t", "6": "q"}
    write("rockfall_books_echo", """
ÉCHO - O12 éboulis gravé : même pile recolorée (8->c, 7->t, 6->q, x->q, z->e), 16x16, même ancrage.
Budget : q t c e = 4. Défaut corrigé : 6 et x tombent tous les deux sur q ; le séparateur reste lisible grâce à c au coin.
""", [recolor(books_clean(), m)], 16, 16)


@asset
def rockfall_mark():
    a = G("""
....p...........
........p.......
......p.........
.......zz.......
""")
    b = G("""
................
.....p.....p....
........p.......
.......ZZ.......
""")
    write("rockfall_mark", """
ÉCHO - O12 marque de départ de l'éboulis, cellule 16x4, 2 images. Ancrage : coin haut-gauche à (x-8, ry+6)
(juste sous la pile, à la place du carré X de world_draw).
Intention : préavis de 0,6 s : la poussière tombe et une marque zz de 2 px s'allume sous la pile.
Timing : 0 et 1 alternés à 10 Hz pendant le préavis (la poussière descend d'1 px, la marque passe z -> Z).
Budget : p z Z = 3. Défaut corrigé : 4 grains de poussière = bruit ; 3 grains au plus, en groupe de 2 + 1.
""", [a, b], 16, 4)


# ======================================================================= 9. LUSTRE-PENDULE (danger x X z, cœur Z)
LUSTRE = G("""
.......kk.......
..k....kk....k..
.kZk...kk...kZk.
.kzk..kZZk..kzk.
.kXk..kzzk..kXk.
kkkkkkkkkkkkkkkk
kzzzzzzzzzzzzzzk
kXXXXXXXXXXXXXxk
kxxxxxxxxxxxxxxk
.kXZzXXXXXXXXxk.
..kzXXXXXXXXxk..
...kXXXXXXxxk...
....kkxxxxkk....
......kkkk......
.......kk.......
................
""")


def lustre(glint):
    g = LUSTRE
    if glint == 1:   # le reflet a tourné : il passe au centre de la vasque, les flammes baissent
        g = [r for r in g]
        g[9] = ".kXXXXzZXXXXxk.".rjust(15).ljust(16, ".") if False else ".kXXXXzZXXXXXxk."
        g[10] = "..kXXXXzXXXXxk.."
        g = [r.replace("kZk", "kzk", 2) if i == 2 else r for i, r in enumerate(g)]
        g[3] = ".kXk..kZZk..kXk."
    return g


def smear():
    base = lustre(0)
    trail = [(r[2:] + "..") if 5 <= i <= 13 else "." * 16 for i, r in enumerate(base)]
    out = over([r.replace("k", "x").replace("z", "x").replace("Z", "X") for r in trail], base)
    return out


@asset
def pendulum_chandelier():
    write("pendulum_chandelier", """
ÉCHO - O6 lustre-pendule (Bibliothèque), cellule 16x16, 3 images. Ancrage : coin haut-gauche à pendulum_pos - (8,8) ;
le crochet (7-8, 0) touche la chaîne. Cercle létal de hz.gd r 5 autour de (8,8) = vasque x 3-12 / y 3-13.
Intention : une couronne de bougies qui balaie le couloir ; la vasque magenta est la masse qui tue.
Timing (E3) : img | rôle | change | principe | durée
  0 | reflet A | reflet Z en haut à gauche de la vasque, flammes Z | tenue | 1/2 période
  1 | reflet B | reflet glissé au centre, flamme centrale seule allumée | arc | 1/2 période
  2 | smear | traînée x de 2 px côté opposé au mouvement (retourner l'image selon le sens) | smear unique [E2-C] | 1 image au point bas
Bible : 32x16 (2 images) ; + 1 smear demandé au §11 O6, d'où 48x16.
Budget : k x X z Z = 5 couleurs. Défaut corrigé : vasque en demi-cercle à escaliers 1-2-1 (jaggy) -> 1-1-1-2-2.
""", [lustre(0), lustre(1), smear()], 16, 16)


@asset
def pendulum_chandelier_echo():
    write("pendulum_chandelier_echo", """
ÉCHO - O6 lustre gravé : même sprite recoloré (q t c e), 16x16, même ancrage ; il continue de se balancer.
Budget : q t c e = 4. Défaut corrigé : aucun.
""", [recolor(lustre(0))], 16, 16)


@asset
def chain():
    g = G("""
...lm...
..m..m..
..m..n..
...mn...
....m...
....l...
....m...
....n...
""")
    write("chain", """
ÉCHO - O6 chaîne de pendule, tuile 8x8 non létale en m (métal), répétée le long de la tige (48 px = 6 tuiles).
Ancrage : coin haut-gauche à (point de la tige) - (4,0) ; pas de rotation (les maillons restent verticaux, lecture voulue).
Intention : la tige ne tue pas : métal du mur m l n, aucun ton de danger (GDD §4.1).
Budget : n m l = 3. Défaut corrigé : maillon fermé en carré -> maillon ovale + maillon de profil (alternance).
""", [g], 8, 8)



# ======================================================================= 10. F11 : PHALÈNE DE PAPIER (X z, ombre x)
MOTH_UP = G("""
................
.k.k........k.k.
kzkzk......kXkXk
kzzzzk....kXXXXk
.kzzzzk..kXXXXk.
..kzzzXkkXXXxk..
...kkzXZZXxkk...
.....kXzzXk.....
.....kxXXxk.....
......kxxk......
.......kk.......
................
......xxxx......
""")
MOTH_DOWN = G("""
................
................
................
................
......kkkk......
......kZZk......
.kkkkkXzzXkkkkk.
kzzzzzXxxXXXXXxk
.kzzzzkXXkXXXxk.
..kzkzkxxkXkXk..
...k.k.kk.k.k...
................
.....xxxxxx.....
""")
MOTH_TURN = G("""
................
................
.......kk.......
......kzXk......
......kzXk......
.....kzzXXk.....
.....kzZZxk.....
.....kXzzXk.....
.....kxXXxk.....
......kxxk......
.......kk.......
................
.......xx.......
""")


@asset
def moth():
    write("moth", """
ÉCHO - O19 phalène de papier (F11), cellule 16x16, 3 images. Ancrage : coin haut-gauche à moth_pos - (8,8).
Hitbox hz.gd 8x6 (m.x-4, m.y-3) = x 4-11, y 5-10 : le corps et la naissance des ailes ; les ailes à dents dépassent de 2-4 px.
Intention : une feuille pliée qui bat des ailes ; le papier X z se découpe en dents, l'ombre x d'1 rangée la décolle du fond.
Vue de face, symétrique : pas besoin de la retourner selon le sens.
Timing (E3) : img | rôle | change | durée
  0 | ailes hautes | dents vers le haut, aile gauche z (lumière haut-gauche), droite X | 1/8 s (8 fps)
  1 | ailes basses | ailes à l'horizontale, dents vers le bas, ombre plus large | 1/8 s
  2 | virage | ailes repliées de profil (1 seule fois au demi-tour) | 1/8 s
Budget : k x X z Z = 5 couleurs. Défaut corrigé : v0 ailes en rectangles 3x6 (dessin de repli) -> dents découpées.
""", [MOTH_UP, MOTH_DOWN, MOTH_TURN], 16, 16)


@asset
def moth_echo():
    write("moth_echo", """
ÉCHO - O19 phalène gravée : image 0 recolorée (q t c e), 16x16, même ancrage ; le code peut aussi recolorer la bande.
Budget : q t c e = 4. Défaut corrigé : l'ombre x -> q reste détachée d'une rangée.
""", [recolor(MOTH_UP)], 16, 16)


# ======================================================================= 10. F11 : GRIGNON (automate X, yeux z)
GNAW_BODY = G("""
................
................
........k.k.....
.......kXkXk....
......kzzXXk....
.....kzzzXXxk...
.....kkkkkkkk...
.....kzzzzXxk...
.....kzXXXXxk...
.....kXXXXXxk...
.....kXXXXxxk...
......kXxxxk....
.......kkkk.....
................
................
................
""")


def gnawer_frame(i):
    g = [list(r) for r in GNAW_BODY]
    # œil z sur l'avant (en haut = sens de marche), 1 px de pupille k devant
    g[4][8] = "Z"     # œil : seul point Z du corps (le z se perdait dans la carapace z)
    g[4][7] = "X"
    g[3][8] = "k"
    # mandibules : ouvertes (0, 2) / fermées (1, 3)
    if i % 2 == 1:
        g[2][8] = "."
        g[2][10] = "."
        g[3][9] = "k"
    # pattes (côté mur, colonnes 3-4) : 3 pattes, phases décalées
    legs = {0: [(7, 3), (9, 4), (11, 3)], 1: [(6, 4), (9, 3), (10, 4)],
            2: [(7, 4), (8, 3), (11, 4)], 3: [(8, 3), (10, 4), (12, 4)]}[i]
    for y, x in legs:
        g[y][x] = "k"
        g[y][4] = "k"
    rows = ["".join(r) for r in g]
    if i in (1, 3):     # le corps se soulève d'1 px entre deux appuis
        rows = rows[1:] + ["." * 16]
    return rows


@asset
def gnawer():
    write("gnawer", """
ÉCHO - O20 grignon (F11), automate qui grimpe sur le mur, vue de profil, cellule 16x16, 4 images.
Ancrage : coin haut-gauche à grignon_pos - (8,8) ; mur gauche (g.x = WL+4) : la colonne 4 = face du mur, pattes en x 3-4.
Hitbox hz.gd 8x6 (g.x-4, g.y-3) = x 4-11, y 5-10 : la coque ; mandibules et pattes dépassent.
Sens : dessiné en MONTÉE (tête et œil z en haut = sens de marche). En descente : retourner verticalement ;
au mur droit : retourner horizontalement.
Timing (E3) : img | rôle | change | principe | durée
  0 | appui A | 3 pattes, mandibules ouvertes | contact | 1/8 s
  1 | passage | corps levé d'1 px, mandibules fermées | rebond | 1/8 s
  2 | appui B | pattes à l'autre phase, mandibules ouvertes | contact | 1/8 s
  3 | passage | corps levé, pattes ramenées | rebond | 1/8 s  (boucle 0-3, 8 fps à 24 px/s)
Budget : k x X z Z = 5 couleurs (œil Z). Défauts corrigés : yeux W du repli (blanc = héros/éclat) -> œil de danger ;
 passe 2 : l'œil z se perdait dans la carapace z -> œil Z cerné de X.
""", [gnawer_frame(i) for i in range(4)], 16, 16)


@asset
def gnawer_echo():
    write("gnawer_echo", """
ÉCHO - O20 grignon gravé : image 0 recolorée, 16x16, même ancrage. Budget : q t c = 3.
Défaut corrigé : aucun (l'œil c reste le point le plus clair).
""", [recolor(gnawer_frame(0))], 16, 16)


# ======================================================================= 10. F11 : LE SONNEUR (cloche 48x48, masse Ø40)
def bell(clap_dx=0, flash=False, dx=0):
    W = 48
    prof = {}
    # demi-largeur par rangée : anse, dôme, taille, évasement, lèvre
    for y in range(2, 6):
        prof[y] = 2
    dome = {6: 7, 7: 9, 8: 11, 9: 12, 10: 13, 11: 13}
    prof.update(dome)
    for y in range(12, 30):
        prof[y] = 13 + (y - 12) // 9
    flare = {30: 16, 31: 16, 32: 17, 33: 18, 34: 19, 35: 20, 36: 21, 37: 22, 38: 22, 39: 22}
    prof.update(flare)
    g = [["."] * W for _ in range(W)]
    cx = 24
    for y, hw in prof.items():
        for x in range(cx - hw, cx + hw):
            if y < 6 and abs(x - cx + 0.5) < 1:
                continue                         # trou de l'anse
            rel = (x - (cx - hw)) / (2 * hw)
            if y >= 37:
                ch = "z" if y == 37 else ("X" if y == 38 else "x")
            elif y in (14, 32):
                ch = "x"                         # deux cordons en relief
            elif y in (15, 33):
                ch = "z" if rel < 0.5 else "X"
            elif rel < 0.12:
                ch = "X"
            elif rel < 0.3:
                ch = "z"                         # bande de reflet (un seul reflet)
            elif rel < 0.68:
                ch = "X"
            else:
                ch = "x"
            g[y][x] = ch
    # reflet Z ponctuel sur le haut du dôme
    g[8][19] = "Z"
    g[9][18] = "Z"
    # battant sous la lèvre (Z), légèrement décalé par le balancement
    bx = cx + clap_dx
    for (x, y, ch) in [(bx - 1, 40, "Z"), (bx, 40, "Z"), (bx - 2, 41, "Z"), (bx - 1, 41, "W"), (bx, 41, "Z"),
                       (bx + 1, 41, "Z"), (bx - 1, 42, "Z"), (bx, 42, "Z"), (bx - 1, 43, "z"), (bx, 43, "z")]:
        g[y][x] = ch
    if flash:
        for y in range(W):
            for x in range(W):
                if g[y][x] != ".":
                    g[y][x] = "w"
    out = [r[:] for r in g]
    for y in range(W):
        for x in range(W):
            if g[y][x] == ".":
                for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if 0 <= nx < W and 0 <= ny < W and g[ny][nx] != ".":
                        out[y][x] = "k"
                        break
    rows = ["".join(r) for r in out]
    if dx:
        rows = ["." * dx + r[:-dx] for r in rows]
    return rows


@asset
def boss_sonneur():
    write("boss_sonneur", """
ÉCHO - Boss B1 le Sonneur, cellule 48x48, 4 images. Ancrage : coin haut-gauche à bell_pos() - (24,24).
Cercle létal r 20 de world.gd autour de (24,24) : la cloche couvre x 2-45 / y 1-44 (anse en haut, lèvre évasée en bas).
Intention : une masse de bronze-sang qui pendule ; la lèvre évasée et le battant Z disent « cloche » à x1 dans le couloir de 128.
Lumière haut-gauche : bande de reflet z à gauche, ombre x à droite, deux cordons en relief, un reflet Z sur le dôme.
Timing (E3) : img | rôle | change | principe | durée
  0 | balancement A | battant à gauche (-3 px) | traîne (suite de mouvement) | quand la cloche va vers la droite
  1 | balancement B | battant à droite (+3 px) | traîne | quand elle va vers la gauche
  2 | sonné : flash | silhouette pleine en w (1 image) | impact | 1/20 s
  3 | sonné : tremblement | image 0 décalée d'1 px, battant centré | vibration | alterner 3 et 0 à 20 Hz pendant 1 s
Budget : k x X z Z (+ W d'1 px dans le battant ; w pour le flash seul) = 6 par image.
Défaut corrigé : profil en trapèze (repli) -> dôme 7-9-11-12-13, taille droite, évasement 16..22 en escalier régulier.
""", [bell(-3), bell(3), bell(0, flash=True), bell(0, dx=1)], 48, 48)


@asset
def boss_sonneur_yoke():
    g = G("""
................................................................
................................................................
....kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk...
...kllmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmsk..
...kmmssssssssssnssssssssssssssssssssssssssssssssnsssssssssssnk..
...kmsssssssssssnssssssssssssssssssssssssssssssssnsssssssssssnk..
...kssssssssssssnssssssssssssssssssssssssssssssssnsssssssssssnk..
...knnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnk..
....kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk...
..........................kmmmmmmmmnk...........................
..........................kmssssssnk............................
...........................kmsssnk..............................
............................kmnk................................
.............................kk.................................
................................................................
................................................................
""")
    write("boss_sonneur_yoke", """
ÉCHO - joug du Sonneur, pierre de la Crypte n s m l, 64x16, 1 image, non létal.
Ancrage : coin haut-gauche à (96-32, mid-56-13) : le pivot (pixel 29-30, rangée 13) est le point d'attache de la corde.
Intention : une poutre de pierre lourde qui dit « la cloche est suspendue », sans couleur de danger.
Budget : k n s m l = 5. Défaut corrigé : aucun joint vertical au centre (évite une symétrie parfaite qui « fige »).
""", [g], 64, 16)


@asset
def boss_wave():
    warn = ["." * 16 for _ in range(8)]
    warn[3] = "zz..zz..zz..zz.."
    def act(core):
        r = ["." * 16 for _ in range(8)]
        r[1] = "X" * 16
        r[2] = "z" * 16
        r[3] = core
        r[4] = "z" * 16
        r[5] = "X" * 16
        return r
    a = act("Z" * 16)
    b = act("ZZZWZZZZZZZWZZZZ")
    c = act("WZZZZZZWZZZZZZZZ")
    b[1] = "XXXXXXXxXXXXXXXx"
    c[5] = "XXXxXXXXXXXxXXXX"
    write("boss_wave", """
ÉCHO - onde-laser du Sonneur, tuile 16x8 bouclable de WL à WR, 4 images. Ancrage : coin haut-gauche à (x, wave_y-3).
Bande létale de 5 px X z Z z X sur les rangées 1-5 (centre rangée 3 = wave_y ; world.gd tue à |y - wave_y| < 4).
Intention : la note de la cloche devenue trait ; le préavis pointillé annonce la hauteur avant qu'elle ne balaie.
Timing (E3) : img | rôle | change | durée
  0 | préavis (0,6 s) | tirets zz de 2 px sur 4, rangée 3 | le code clignote à 10 Hz
  1 | actif A | bande pleine | 1/20 s
  2 | actif B | 2 étincelles W, cran x en haut | 1/20 s
  3 | actif C | étincelles déplacées, cran x en bas | 1/20 s (boucle 1-2-3 pendant la descente)
Budget : x X z Z W = 5. Défaut corrigé : boucle de 2 images = jumeaux ; 3 images différentes, aucune symétrie.
""", [warn, a, b, c], 16, 8)


@asset
def boss_wave_echo():
    r = ["." * 16 for _ in range(8)]
    r[3] = "c" * 16
    r[4] = "qtqtqtqtqtqtqtqt"
    write("boss_wave_echo", """
ÉCHO - onde gravée (attaque qui a tué, GDD §3.4) : ligne cyan fine, 16x8 bouclable, même ancrage que boss_wave.
Budget : q t c = 3. Défaut corrigé : la bande de 5 px recolorée se lisait comme encore active ; réduite à 2 px.
""", [r], 16, 8)


if __name__ == "__main__":
    names = sys.argv[1:] or list(REGISTRY)
    for n in names:
        REGISTRY[n]()
        print("ok", n)
