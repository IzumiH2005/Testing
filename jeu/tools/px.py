#!/usr/bin/env python3
"""px.py : rend une grille de pixels écrite à la main en PNG.

Format d'un fichier .txt :

    # commentaire
    palette: shared            (optionnel : charge tools/palette.txt)
    size: 16x16                (obligatoire)
    frames: 1                  (optionnel, nombre d'images côte à côte dans la grille)
    = X #0b0b1a                (optionnel : couleur locale, 1 caractère -> hex)
    ---
    ....XXXX........
    ...X####X.......
    (une ligne = une rangée de pixels, 1 caractère = 1 pixel, '.' = transparent)

Chaque pixel est décidé par l'auteur : ce script ne fait que traduire la grille.

Usage : python3 px.py fichier.txt [sortie.png]
  -> écrit sortie.png (×1) et sortie@8.png (agrandi ×8, pour vérifier).
"""
import sys
import os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))


def load_palette(path):
    pal = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("="):
                line = line[1:].strip()
            parts = line.split()
            if len(parts) >= 2 and len(parts[0]) == 1 and parts[1].startswith("#"):
                pal[parts[0]] = parts[1]
    return pal


def hex_to_rgba(h):
    h = h.lstrip("#")
    if len(h) == 6:
        h += "ff"
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4, 6))


def parse(path):
    pal = {}
    size = None
    rows = []
    in_grid = False
    with open(path, encoding="utf-8") as f:
        for raw in f:
            line = raw.rstrip("\n")
            if not in_grid:
                s = line.strip()
                if s == "---":
                    in_grid = True
                    continue
                if not s or s.startswith("#"):
                    continue
                if s.startswith("palette:"):
                    name = s.split(":", 1)[1].strip()
                    p = os.path.join(HERE, "palette.txt") if name == "shared" else name
                    pal.update(load_palette(p))
                elif s.startswith("size:"):
                    w, h = s.split(":", 1)[1].strip().lower().split("x")
                    size = (int(w), int(h))
                elif s.startswith("="):
                    parts = s[1:].split()
                    pal[parts[0]] = parts[1]
            else:
                if line.strip() == "" and not rows:
                    continue
                rows.append(line)
    # retire les lignes vides de fin
    while rows and rows[-1].strip() == "":
        rows.pop()
    if size is None:
        raise SystemExit(f"{path}: 'size: WxH' manquant")
    w, h = size
    if len(rows) != h:
        raise SystemExit(f"{path}: {len(rows)} rangées, {h} attendues")
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    for y, row in enumerate(rows):
        if len(row) != w:
            raise SystemExit(f"{path}: rangée {y + 1} fait {len(row)} px, {w} attendus : '{row}'")
        for x, c in enumerate(row):
            if c in ". ":
                continue
            if c not in pal:
                raise SystemExit(f"{path}: caractère '{c}' (rangée {y + 1}, col {x + 1}) absent de la palette")
            img.putpixel((x, y), hex_to_rgba(pal[c]))
    return img


def main():
    src = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.splitext(src)[0] + ".png"
    img = parse(src)
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    img.save(out)
    big = img.resize((img.width * 8, img.height * 8), Image.NEAREST)
    big.save(os.path.splitext(out)[0] + "@8.png")
    print(f"ok {out} {img.width}x{img.height}")


if __name__ == "__main__":
    main()
