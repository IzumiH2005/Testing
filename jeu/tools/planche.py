#!/usr/bin/env python3
"""planche.py : planche de contrôle d'un sprite (règle impérative 25).

Produit une seule image avec : ×1, ×2, ×4, niveaux de gris (valeurs),
silhouette, sur fond clair, sur fond sombre, miroir, et sur le fond du jeu.

Usage : python3 planche.py sprite.png [sortie.png]
"""
import sys
import os
from PIL import Image, ImageOps

BG_DARK = (22, 22, 49, 255)      # fond du jeu (palette 'b')
BG_LIGHT = (223, 230, 255, 255)  # clair froid
BG_MID = (63, 69, 128, 255)


def on_bg(img, color, scale):
    im = img.resize((img.width * scale, img.height * scale), Image.NEAREST)
    bg = Image.new("RGBA", im.size, color)
    bg.alpha_composite(im)
    return bg


def gray(img):
    g = ImageOps.grayscale(img.convert("RGB")).convert("RGBA")
    g.putalpha(img.getchannel("A"))
    return g


def silhouette(img):
    s = Image.new("RGBA", img.size, (0, 0, 0, 0))
    a = img.getchannel("A")
    black = Image.new("RGBA", img.size, (11, 11, 26, 255))
    s.paste(black, mask=a)
    return s


def main():
    src = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.splitext(src)[0] + "_planche.png"
    img = Image.open(src).convert("RGBA")
    S = 4 if max(img.size) <= 64 else 2
    tiles = [
        on_bg(img, BG_DARK, 1),
        on_bg(img, BG_DARK, 2),
        on_bg(img, BG_DARK, S),
        on_bg(gray(img), BG_MID, S),
        on_bg(silhouette(img), BG_LIGHT, S),
        on_bg(img, BG_LIGHT, S),
        on_bg(ImageOps.mirror(img), BG_DARK, S),
    ]
    pad = 8
    W = sum(t.width for t in tiles) + pad * (len(tiles) + 1)
    H = max(t.height for t in tiles) + pad * 2
    sheet = Image.new("RGBA", (W, H), (40, 40, 60, 255))
    x = pad
    for t in tiles:
        sheet.alpha_composite(t, (x, pad))
        x += t.width + pad
    # ×2 de la planche pour la lecture
    sheet = sheet.resize((sheet.width * 2, sheet.height * 2), Image.NEAREST)
    sheet.save(out)
    print(f"ok {out}")


if __name__ == "__main__":
    main()
