#!/usr/bin/env python3
"""apercu_police.py : aperçu de phrases test avec la police ÉCHO.

Ne dessine rien : lit font.fnt + font.png et recopie les glyphes déjà dessinés
côte à côte (avance = xadvance du .fnt), sur fond nuit 'b'.
Usage : python3 apercu_police.py [dossier_police] [sortie.png]
"""
import os
import sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "../../../game/assets/ui")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "apercu_police.png")

PHRASES = [
    "ÉCHO · TOUR DU 13/11 · 214 M",
    "JOUER",
    "REGARDER UNE VIDÉO : +1 ÉCHO",
    "RECORD ! ÇA MONTE.",
    "ÀÂÇÈÉÊËÎÏÔÙÛ ×3 (50%) <=> #1 _*_",
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "0123456789 .,:;!?'\"-+/",
]
BG = (22, 22, 49, 255)       # palette b
TINTS = [None, (255, 196, 107, 255), (63, 208, 212, 255)]  # w (tel quel), a, c : le code teinte


def load():
    chars, line_h = {}, 11
    for line in open(os.path.join(FONT_DIR, "font.fnt"), encoding="utf-8"):
        p = dict(kv.split("=", 1) for kv in line.split()[1:] if "=" in kv)
        if line.startswith("common"):
            line_h = int(p["lineHeight"])
        if line.startswith("char "):
            chars[chr(int(p["id"]))] = tuple(int(p[k]) for k in ("x", "y", "width", "height", "xadvance"))
    return Image.open(os.path.join(FONT_DIR, "font.png")).convert("RGBA"), chars, line_h


def text(sheet, chars, s, tint=None):
    w = sum(chars[c][4] for c in s)
    im = Image.new("RGBA", (max(w, 1), chars["A"][3]), (0, 0, 0, 0))
    x = 0
    for c in s:
        gx, gy, gw, gh, adv = chars[c]
        g = sheet.crop((gx, gy, gx + gw, gy + gh))
        if tint:
            col = Image.new("RGBA", g.size, tint)
            col.putalpha(g.getchannel("A"))
            g = col
        im.alpha_composite(g, (x, 0))
        x += adv
    return im


def main():
    sheet, chars, lh = load()
    blocks = []
    for tint in TINTS:
        for s in PHRASES:
            blocks.append(text(sheet, chars, s, tint))
    W = max(b.width for b in blocks) + 8
    H = len(blocks) * lh + 8
    img = Image.new("RGBA", (W, H), BG)
    for i, b in enumerate(blocks):
        img.alpha_composite(b, (4, 4 + i * lh))
    # ×1 à gauche (taille réelle) puis ×4 à droite
    big = img.resize((W * 4, H * 4), Image.NEAREST)
    out = Image.new("RGBA", (W + 8 + big.width, big.height), (40, 40, 60, 255))
    out.alpha_composite(img, (0, 0))
    out.alpha_composite(big, (W + 8, 0))
    out.save(OUT)
    print("ok", OUT)


if __name__ == "__main__":
    main()
