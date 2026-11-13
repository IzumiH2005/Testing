"""Scènes composées pour la mise en situation (voir situation.py)."""
from situation import scene, put, hero, save, WL, WR

ALL = {}


def sc(fn):
    ALL[fn.__name__] = fn
    return fn


@sc
def s1_spikes_saw_laser():
    img = scene(240)
    # épines gauche (image d'éclat 3) y 16-64, droite (repos) y 32-80 : ancrage (WL, y) et (WR-16, y) retourné
    for i, y in enumerate(range(16, 64, 16)):
        put(img, "spikes", 16, 3 if i == 1 else 0, WL, y)
    for y in range(32, 80, 16):
        put(img, "spikes", 16, 0, WR - 16, y, flip=True)
    # rail horizontal + scie au centre p=(96, 104) : ancrage p-(12,12)
    for x in range(56, 136, 16):
        put(img, "saw_rail", 16, 0, x, 104 - 8)
    put(img, "saw_rail", 16, 2, 40, 104 - 8)
    put(img, "saw_rail", 16, 2, 136, 104 - 8)
    put(img, "saw", 24, 1, 96 - 12, 104 - 12)
    # laser actif à y=140, préavis à y=164
    for yy, st in ((140, 2), (164, 1)):
        put(img, "laser", 8, st, WL, yy - 4)
        put(img, "laser", 8, st, WR - 8, yy - 4, flip=True)
        for x in range(WL + 8, WR - 8, 16):
            put(img, "beam", 16, 1 if st == 2 else 0, x, yy - 4)
    # échos : épines gravées gauche, scie gravée, laser gravé
    for y in range(184, 232, 16):
        put(img, "spikes_echo", 16, 0, WL, y)
    put(img, "saw_echo", 24, 0, 120 - 12, 200 - 12)
    put(img, "laser_echo", 8, 0, WL, 220 - 4)
    put(img, "laser_echo", 8, 0, WR - 8, 220 - 4, flip=True)
    for x in range(WL + 8, WR - 8, 16):
        put(img, "beam_echo", 16, 0, x, 220 - 4)
    hero(img, WR - 32, 96, flip=True)
    hero(img, WL, 60)
    save(img, "1_epines_scie_laser")


def s2_body(img):
    # contrefort h32 à gauche (y0=24), h48 à droite (y0=40) : ancrage (bx, y0-5)
    put(img, "buttress", 16, 0, WL, 24 - 5)
    put(img, "buttress", 16, 1, WR - 16, 40 - 5, flip=True)
    # herse gauche sortie y0=112..144 (32), herse droite en préavis y0=112..128
    put(img, "portcullis", 24, 2, WL, 112)
    put(img, "portcullis", 24, 1, WR - 24, 112, flip=True, ch=16)
    # mâchoires : mid=176, ext=40 à gauche (préavis), ext=40 à droite
    mid, ext = 176, 40
    for x in range(WL, WL + ext - 16, 16):
        put(img, "jaws", 16, 0, x, mid - 12)
    put(img, "jaws", 16, 2, WL + ext - 16, mid - 12)
    for x in range(WR - 16, WR - ext, -16):
        put(img, "jaws", 16, 0, x, mid - 12, flip=True)
    put(img, "jaws", 16, 1, WR - ext, mid - 12, flip=True)
    # échos : herse gravée gauche, pont de mâchoires
    put(img, "portcullis_echo", 24, 0, WL, 208)
    for x in range(WL, WR, 16):
        put(img, "jaws_echo", 16, 0, x, 252 - 12)
    hero(img, WR - 32, 76, flip=True)
    hero(img, WL + 16, 200)


@sc
def s2_crypte():
    img = scene(272)
    s2_body(img)
    save(img, "2_contrefort_herse_machoires_crypte")


@sc
def s2_fonderie():
    from situation import FONDERIE
    img = scene(272, FONDERIE)
    s2_body(img)
    save(img, "2_contrefort_herse_machoires_fonderie")


@sc
def s3_crumble_books_chandelier():
    import math
    img = scene(256)
    # friables : gauche (repos y0=16..48, fissure 2 y0=64..96), droite (chute y0=32)
    for y in (16, 32):
        put(img, "crumble", 16, 0, WL - 4, y, ch=16)
    for y in (64, 80):
        put(img, "crumble", 16, 2, WL - 4, y, ch=16)
    put(img, "crumble", 16, 3, WR - 12, 32, flip=True)
    # éboulis : marque au sol (préavis) puis livres qui tombent
    for x, ry in ((72, 120), (120, 104)):
        put(img, "rockfall_mark", 16, 1, x - 8, 150 + 6, ch=4)
        put(img, "rockfall_books", 16, 0, x - 8, ry - 8)
    put(img, "rockfall_books_echo", 16, 0, 96 - 8, 140 - 8)
    # lustre-pendule : pivot (96,160), longueur 64, angle 35° ; chaîne tous les 8 px
    th = math.radians(35)
    px, py, L = 96, 160, 64
    for d in range(0, L - 8, 8):
        put(img, "chain", 8, 0, px + math.sin(th) * d - 4, py + math.cos(th) * d - 4)
    pos = (px + math.sin(th) * L, py + math.cos(th) * L)
    put(img, "pendulum_chandelier", 16, 2, pos[0] - 8, pos[1] - 8)
    put(img, "pendulum_chandelier_echo", 16, 0, 60 - 8, 230 - 8)
    hero(img, WR - 32, 60, flip=True)
    hero(img, WL, 196)
    save(img, "3_friable_livres_lustre")


@sc
def s4_f11_sonneur():
    import math
    img = scene(288)
    mid = 120
    put(img, "boss_sonneur_yoke", 64, 0, 96 - 32, mid - 56 - 13)
    th = math.radians(30)
    bx, by = 96 + math.sin(th) * 44, mid - 56 + math.cos(th) * 44
    for d in range(4, 24, 8):
        put(img, "chain", 8, 0, 96 + math.sin(th) * d - 4, mid - 56 + math.cos(th) * d - 4)
    put(img, "boss_sonneur", 48, 0, bx - 24, by - 24)
    # onde : préavis à y=150, active à y=176, gravée à y=272
    for x in range(WL, WR, 16):
        put(img, "boss_wave", 16, 0, x, 150 - 3)
        put(img, "boss_wave", 16, 2, x, 176 - 3)
        put(img, "boss_wave_echo", 16, 0, x, 272 - 3)
    # F11 : phalènes et grignons sur la face du mur
    put(img, "moth", 16, 0, 70 - 8, 210 - 8)
    put(img, "moth", 16, 1, 112 - 8, 222 - 8)
    put(img, "moth_echo", 16, 0, 140 - 8, 250 - 8)
    put(img, "gnawer", 16, 0, WL + 4 - 8, 200 - 8)
    put(img, "gnawer", 16, 1, WR - 4 - 8, 236 - 8, flip=True)
    put(img, "gnawer_echo", 16, 0, WL + 4 - 8, 250 - 8)
    hero(img, WL, 16)
    hero(img, WR - 32, 220, flip=True)
    save(img, "4_f11_sonneur")
