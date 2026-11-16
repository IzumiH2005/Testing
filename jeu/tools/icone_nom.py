#!/usr/bin/env python3
"""icone_nom.py : icône de l'application = son nom, « ÉCHO » sur « MOUNBOLE ».

Grille de 108 × 108 pixels d'art (1 px = 1 dp de l'icône adaptative), agrandie au plus proche
voisin. Les lettres viennent des polices du jeu (font_l pour ÉCHO, font_7 pour MOUNBOLE), dans
le style du logo du menu : lettres w, ombre cyan décalée, contour k. Le texte tient dans la zone
sûre (cercle de 66 dp). Remplace les fichiers écrits par icone.py.

Usage : python3 tools/icone_nom.py
"""
import os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
JEU = os.path.dirname(HERE)
UI = os.path.join(JEU, "game", "assets", "ui")
N = 108
PAL = {}
for line in open(os.path.join(HERE, "palette.txt"), encoding="utf-8"):
    p = line.split()
    if len(p) >= 2 and len(p[0]) == 1 and p[1].startswith("#"):
        PAL[p[0]] = p[1]


def rgba(c, a=255):
    h = PAL[c].lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)


def charger_police(nom):
    chars = {}
    for line in open(os.path.join(UI, nom + ".fnt"), encoding="utf-8"):
        if line.startswith("char "):
            d = dict(kv.split("=") for kv in line.split()[1:])
            chars[int(d["id"])] = {k: int(v) for k, v in d.items()}
    return Image.open(os.path.join(UI, nom + ".png")).convert("RGBA"), chars


def masque_texte(texte, nom, espace=1):
    img, chars = charger_police(nom)
    largeur = sum(chars[ord(ch)]["xadvance"] + espace for ch in texte) - espace
    hauteur = max(c["yoffset"] + c["height"] for c in chars.values())
    m = Image.new("L", (largeur, hauteur), 0)
    x = 0
    for ch in texte:
        c = chars[ord(ch)]
        g = img.crop((c["x"], c["y"], c["x"] + c["width"], c["y"] + c["height"])).split()[3]
        m.paste(g, (x + c["xoffset"], c["yoffset"]), g)
        x += c["xadvance"] + espace
    bb = m.getbbox()
    return m.crop(bb)


def poser(dest, masque, x, y, couleur):
    dest.paste(Image.new("RGBA", masque.size, couleur), (x, y), masque)


def dilate(m):
    out = Image.new("L", (m.width + 2, m.height + 2), 0)
    for dx in range(3):
        for dy in range(3):
            if abs(dx - 1) + abs(dy - 1) <= 1:
                out.paste(255, (dx, dy), m)
    return out


def bloc(masque, face="w", ombre="c"):
    """Lettre style logo : contour k, ombre cyan +1 +1, face."""
    w, h = masque.width + 3, masque.height + 3
    b = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    union = Image.new("L", (masque.width + 1, masque.height + 1), 0)
    union.paste(255, (0, 0), masque)
    union.paste(255, (1, 1), masque)
    poser(b, dilate(union), 0, 0, rgba("k"))
    poser(b, masque, 2, 2, rgba(ombre))
    poser(b, masque, 1, 1, rgba(face))
    return b


def premier_plan(mono=False):
    fg = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    haut = masque_texte("ÉCHO", "font_l", espace=1)
    bas = masque_texte("MOUNBOLE", "font_7", espace=0)
    if mono:
        haut_b, bas_b = Image.new("RGBA", haut.size, rgba("w")), Image.new("RGBA", bas.size, rgba("w"))
        haut_b.putalpha(haut)
        bas_b.putalpha(bas)
    else:
        haut_b, bas_b = bloc(haut), bloc(bas, face="p", ombre="t")
    total = haut_b.height + 4 + bas_b.height
    y0 = (N - total) // 2
    fg.alpha_composite(haut_b, ((N - haut_b.width) // 2, y0))
    fg.alpha_composite(bas_b, ((N - bas_b.width) // 2, y0 + haut_b.height + 4))
    return fg


def arriere_plan():
    bg = Image.new("RGBA", (N, N), rgba("b"))
    px = bg.load()
    c = (N - 1) / 2
    for y in range(N):
        for x in range(N):
            r = ((x - c) ** 2 + (y - c) ** 2) ** 0.5
            if r < 26 or (r < 31 and (x + y) % 2 == 0):
                px[x, y] = rgba("d")
    return bg


def grand(img, k):
    return img.resize((img.width * k, img.height * k), Image.NEAREST)


def main():
    fg, bg, mono = premier_plan(), arriere_plan(), premier_plan(mono=True)
    legacy = bg.copy()
    legacy.alpha_composite(fg)
    legacy = legacy.crop((18, 18, 90, 90)).resize((48, 48), Image.NEAREST)  # zone visible 72 dp
    legacy = Image.new("RGBA", (72, 72))
    vis = bg.copy()
    vis.alpha_composite(fg)
    legacy = vis.crop((18, 18, 90, 90))  # 72 × 72
    og = os.path.join(JEU, "game", "assets", "icon")
    grand(fg, 4).save(os.path.join(og, "icon_fg_432.png"))
    grand(bg, 4).save(os.path.join(og, "icon_bg_432.png"))
    grand(mono, 4).save(os.path.join(og, "icon_mono_432.png"))
    l192 = grand(legacy, 3).resize((192, 192), Image.NEAREST)
    l192.save(os.path.join(og, "icon_192.png"))
    l192.save(os.path.join(JEU, "game", "icon.png"))
    out = os.path.join(JEU, "art", "out", "icone")
    os.makedirs(out, exist_ok=True)
    grand(legacy, 8).resize((512, 512), Image.NEAREST).save(os.path.join(out, "icon_store_512.png"))
    # planche : masque rond et carré arrondi, puis tailles réelles
    sheet = Image.new("RGBA", (432 * 2 + 48, 432 + 230), rgba("k"))
    v = grand(vis.crop((18, 18, 90, 90)), 6)
    from PIL import ImageDraw
    for i, rond in enumerate((True, False)):
        m = Image.new("L", (432, 432), 0)
        d = ImageDraw.Draw(m)
        if rond:
            d.ellipse((0, 0, 431, 431), fill=255)
        else:
            d.rounded_rectangle((0, 0, 431, 431), radius=110, fill=255)
        sheet.paste(v, (16 + i * 448, 16), m)
    x = 16
    for s in (48, 72, 96, 144, 192):
        sheet.alpha_composite(l192.resize((s, s), Image.BOX), (x, 432 + 32))
        x += s + 16
    sheet.save(os.path.join(out, "planche.png"))


if __name__ == "__main__":
    main()
