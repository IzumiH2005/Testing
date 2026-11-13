#!/usr/bin/env python3
"""Mise en situation des pièges sur le mur et le fond de la Crypte (§12.1 étape 10, A6-J).

Monde : 192 px de large, murs pleins x 0-31 et 160-191 (faces WL=32 / WR=160), fond P2 entre les deux.
Chaque piège est posé avec l'ancrage écrit dans MANIFEST.md, donc la planche vérifie aussi l'ancrage.
Sortie : art/out/traps/situation_<n>.png (×1 et ×3 côte à côte).
"""
import os
import sys
from PIL import Image, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
TESTS = os.path.join(ROOT, "studio", "art_tests")
ASSETS = os.path.join(ROOT, "game", "assets", "traps")
OUT = os.path.join(ROOT, "art", "out", "traps")
WL, WR = 32, 160


# Fonderie froide approchée par échange de palette du mur de la Crypte (n s m l b d -> 1 2 3 4 ( )).
FONDERIE = {(0x2f, 0x2c, 0x5c): (0x2a, 0x33, 0x41), (0x39, 0x42, 0x7b): (0x36, 0x49, 0x57),
            (0x46, 0x63, 0x9f): (0x4a, 0x69, 0x73), (0x71, 0x9d, 0xca): (0x76, 0xa1, 0xa4),
            (0x17, 0x12, 0x2a): (0x0f, 0x16, 0x22), (0x23, 0x20, 0x3d): (0x19, 0x24, 0x31)}


def swap(im, m):
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if (r, g, b) in m:
                px[x, y] = m[(r, g, b)] + (a,)
    return im


def scene(h, biome=None):
    wall = Image.open(os.path.join(TESTS, "wall_crypte.png")).convert("RGBA")
    back = Image.open(os.path.join(TESTS, "back_crypte.png")).convert("RGBA")
    if biome:
        wall, back = swap(wall, biome), swap(back, biome)
    img = Image.new("RGBA", (192, h), (14, 10, 26, 255))
    for y in range(0, h, 16):
        for x in range(WL, WR, 32):
            img.alpha_composite(back, (x, y))
    tiles = [wall.crop((i * 16, 0, i * 16 + 16, 16)) for i in range(4)]
    for j, y in enumerate(range(0, h, 16)):
        for col, x in enumerate((0, 16)):
            t = tiles[(j + col * 2) % 4]
            img.alpha_composite(t, (x, y))
            img.alpha_composite(ImageOps.mirror(t), (192 - 16 - x, y))
    return img


def frame(name, cw, f, ch=None):
    im = Image.open(os.path.join(ASSETS, name + ".png")).convert("RGBA")
    ch = ch or im.height
    return im.crop((f * cw, 0, f * cw + cw, ch))


def put(img, name, cw, f, x, y, flip=False, ch=None):
    fr = frame(name, cw, f, ch)
    if flip:
        fr = ImageOps.mirror(fr)
    img.alpha_composite(fr, (int(x), int(y)))


def hero(img, x, y, flip=False):
    h = Image.open(os.path.join(TESTS, "hero_idle.png")).convert("RGBA").crop((0, 0, 32, 32))
    if flip:
        h = ImageOps.mirror(h)
    img.alpha_composite(h, (int(x), int(y)))


def save(img, n):
    big = img.resize((img.width * 3, img.height * 3), Image.NEAREST)
    sheet = Image.new("RGBA", (img.width + big.width + 24, big.height + 16), (40, 40, 60, 255))
    sheet.alpha_composite(img, (8, 8))
    sheet.alpha_composite(big, (img.width + 16, 8))
    p = os.path.join(OUT, f"situation_{n}.png")
    sheet.save(p)
    print(p)


if __name__ == "__main__":
    import situations  # noqa
    for n in sys.argv[1:] or situations.ALL:
        situations.ALL[n]()
