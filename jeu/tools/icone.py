#!/usr/bin/env python3
"""icone.py : icône de l'application (pixel art) à toutes les tailles Android.

Composition (palette v2, studio/palette_v2.txt) : l'intérieur de la tour (deux murs de pierre,
fond de nuit, marée de Silence violette en bas), le grimpeur à l'écharpe corail qui quitte le mur
gauche (image 1 de art/src/hero/player_jump.txt, recopiée pixel pour pixel) et, derrière lui,
son écho cyan décalé vers le bas : le souvenir de la vie précédente. Deux éclats d'or.

Tout est dessiné sur une grille de 54 × 54 pixels d'art (= 108 dp d'une icône adaptative,
soit 2 dp par pixel d'art), puis agrandi au plus proche voisin (aucun lissage).
Seuls les 36 pixels centraux sont visibles après le masque du lanceur : le héros tient
dans la zone sûre (33 px), les murs et la marée débordent volontairement.

Usage : python3 tools/icone.py   (depuis jeu/ ou n'importe où)
Écrit :
  game/icon.png                         192 × 192 (icône du projet, repli)
  game/assets/icon/icon_192.png         icône classique (launcher_icons/main_192x192)
  game/assets/icon/icon_fg_432.png      premier plan adaptatif (transparent)
  game/assets/icon/icon_bg_432.png      arrière-plan adaptatif (opaque)
  game/assets/icon/icon_mono_432.png    monochrome adaptatif (Android 13, icônes à thème)
  art/out/icone/mipmap-*/...            toutes les densités (mdpi à xxxhdpi), pour un export Gradle
  art/out/icone/icon_store_512.png      fiche Play Store
  art/out/icone/planche.png             planche de contrôle (tailles réelles + masques rond et carré)
"""
import os
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
JEU = os.path.dirname(HERE)
N = 54  # grille d'art de l'icône adaptative (108 dp)


def load_palette(path):
    pal = {}
    for line in open(path, encoding="utf-8"):
        p = line.split()
        if len(p) >= 2 and len(p[0]) == 1 and p[1].startswith("#"):
            pal[p[0]] = p[1]
    return pal


PAL = load_palette(os.path.join(JEU, "studio", "palette_v2.txt"))


def rgba(c):
    h = PAL[c].lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (255,)


def hero_frame(anim="player_jump", frame=0):
    txt = open(os.path.join(JEU, "art", "src", "hero", anim + ".txt"), encoding="utf-8").read()
    rows = txt.split("---\n", 1)[1].splitlines()[:32]
    return [r[frame * 32:(frame + 1) * 32] for r in rows]


# Échos : la cape et l'écharpe passent dans la rampe écho (cyan réservé aux souvenirs).
ECHO = {"k": "q", "h": "q", "H": "t", "i": "c", "I": "e", "r": "q", "R": "t", "o": "c", "a": "e",
        "A": "e", "b": "q", "w": "e"}


def put(img, x, y, c):
    if 0 <= x < img.width and 0 <= y < img.height:
        img.putpixel((x, y), rgba(c))


def background(n=N):
    """Fond opaque : nuit, deux murs de briques, marée de Silence. n pair, centré comme la grille 54."""
    img = Image.new("RGBA", (n, n), rgba("b"))
    o = (n - N) // 2  # décalage si la grille est plus grande (icône Store)
    # halo de fond au centre (d), arche discrète
    for y in range(n):
        for x in range(n):
            dx, dy = x - (n / 2 - 0.5), y - (n * 0.42)
            if dx * dx * 1.4 + dy * dy < (n * 0.30) ** 2:
                put(img, x, y, "d")
    # fenêtre violette lointaine (petite, haut centre)
    for (x, y) in [(0, 0), (1, 0), (0, 1), (1, 1), (0, 2), (1, 2)]:
        put(img, o + 20 + x, o + 6 + y, "u")
    # murs : face intérieure gauche à x = 14, droite à x = 39 (grille 54)
    lw, rw = o + 14, o + 39
    for y in range(n):
        row = (y - o) // 4
        for x in range(n):
            if x < lw or x > rw:
                inner = x - lw if x < lw else rw - x  # négatif vers l'extérieur
                # briques de 7 × 4, joints décalés d'une rangée à l'autre
                xx = (x - o + (3 if row % 2 else 0)) if x < lw else (o + N - 1 - x + (3 if row % 2 else 0))
                joint = (y - o) % 4 == 3 or xx % 7 == 6
                c = "n" if joint else "s"
                if not joint and (y - o) % 4 == 0:
                    c = "m"  # lumière du haut sur chaque brique
                if inner == -1:
                    c = "l" if x < lw else "m"  # arête éclairée (lumière en haut à gauche)
                elif inner == -2:
                    c = "m" if x < lw else "s"
                put(img, x, y, c)
    # marée de Silence : crête ondulée + corps violet
    for x in range(n):
        crest = o + 45 + (1 if (x // 3) % 2 else 0)
        for y in range(crest, n):
            c = "U" if y == crest else ("j" if y == crest + 1 and x % 5 == 0 else "u")
            put(img, x, y, c)
    for x in range(o + 15, o + 39, 4):
        put(img, x, o + 43 + (x // 4) % 2, "U")  # bulles de Silence
    return img


def sprite(img, rows, ox, oy, recolor=None):
    for y, r in enumerate(rows):
        for x, c in enumerate(r):
            if c == ".":
                continue
            if recolor:
                c = recolor.get(c, "t")
            put(img, ox + x, oy + y, c)


def shard(img, x, y):
    for dx, dy, c in [(0, -1, "y"), (-1, 0, "G"), (0, 0, "y"), (1, 0, "g"), (0, 1, "g")]:
        put(img, x + dx, y + dy, c)


def foreground(n=N, mono=False):
    img = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    o = (n - N) // 2
    hero = hero_frame("player_jump", 0)
    # boîte du héros dans sa cellule : colonnes 6-31, rangées 3-27 -> centré, un peu haut
    hx, hy = o + 9, o + 11
    if mono:
        sprite(img, hero, hx, hy, recolor={c: "W" for c in "kKhHiIrRoaAbwW"})
        return img
    sprite(img, hero, hx - 8, hy + 8, recolor=ECHO)      # l'écho, en retard sur le héros
    sprite(img, hero, hx, hy)
    shard(img, o + 37, o + 15)
    shard(img, o + 33, o + 10)
    return img


def compose(n):
    img = background(n)
    img.alpha_composite(foreground(n))
    return img


def big(img, k):
    return img.resize((img.width * k, img.height * k), Image.NEAREST)


def crop_center(img, size):
    o = (img.width - size) // 2
    return img.crop((o, o, o + size, o + size))


def main():
    out_game = os.path.join(JEU, "game", "assets", "icon")
    out_art = os.path.join(JEU, "art", "out", "icone")
    os.makedirs(out_game, exist_ok=True)
    os.makedirs(out_art, exist_ok=True)

    bg, fg, mono = background(), foreground(), foreground(mono=True)
    full = compose(N)
    # icône classique : les 48 px centraux (le lanceur la montre en entier), ×4 = 192
    legacy = crop_center(full, 48)

    big(fg, 8).save(os.path.join(out_game, "icon_fg_432.png"))
    big(bg, 8).save(os.path.join(out_game, "icon_bg_432.png"))
    big(mono, 8).save(os.path.join(out_game, "icon_mono_432.png"))
    big(legacy, 4).save(os.path.join(out_game, "icon_192.png"))
    big(legacy, 4).save(os.path.join(JEU, "game", "icon.png"))

    # toutes les densités (adaptatif 108 dp = 54 px d'art × k ; classique 48 dp)
    dens = {"mdpi": 1, "hdpi": 1.5, "xhdpi": 2, "xxhdpi": 3, "xxxhdpi": 4}
    for name, f in dens.items():
        d = os.path.join(out_art, "mipmap-" + name)
        os.makedirs(d, exist_ok=True)
        k = int(f * 2)  # 108 dp × f = 54 × 2f
        big(fg, k).save(os.path.join(d, "icon_foreground.png"))
        big(bg, k).save(os.path.join(d, "icon_background.png"))
        big(mono, k).save(os.path.join(d, "icon_monochrome.png"))
        s = int(48 * f)
        if float(f).is_integer():
            big(legacy, int(f)).save(os.path.join(d, "icon.png"))
        else:  # 72 px : ×3 puis réduction par moyenne de blocs 2 × 2 (pas de flou étalé)
            big(legacy, 3).resize((s, s), Image.BOX).save(os.path.join(d, "icon.png"))
    big(compose(64), 8).save(os.path.join(out_art, "icon_store_512.png"))

    # planche de contrôle : masques rond / carré arrondi à 432, puis tailles réelles 48 à 192
    sheet = Image.new("RGBA", (432 * 3 + 64, 432 + 260), rgba("k"))
    ad = big(compose(N), 8)
    for i, shape in enumerate(["circle", "squircle", "legacy"]):
        x0 = 16 + i * (432 + 16)
        if shape == "legacy":
            sheet.alpha_composite(big(legacy, 9).crop((0, 0, 432, 432)), (x0, 16))
            continue
        vis = ad.crop((72, 72, 360, 360)).resize((432, 432), Image.NEAREST)  # zone visible 72 dp
        m = Image.new("L", (432, 432), 0)
        dr = ImageDraw.Draw(m)
        if shape == "circle":
            dr.ellipse((0, 0, 431, 431), fill=255)
        else:
            dr.rounded_rectangle((0, 0, 431, 431), radius=110, fill=255)
        sheet.paste(vis, (x0, 16), m)
    x = 16
    for s in (48, 72, 96, 144, 192):
        p = os.path.join(out_art, "mipmap-" + {48: "mdpi", 72: "hdpi", 96: "xhdpi", 144: "xxhdpi", 192: "xxxhdpi"}[s], "icon.png")
        sheet.alpha_composite(Image.open(p).convert("RGBA"), (x, 432 + 40))
        x += s + 24
    sheet.save(os.path.join(out_art, "planche.png"))
    print("ok icônes ->", out_game, "et", out_art)


if __name__ == "__main__":
    main()
