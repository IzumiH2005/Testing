#!/usr/bin/env python3
"""font.py : convertit une police écrite à la main (font.txt) en font.png + font.fnt (BMFont texte).

Format de font.txt :
    cell: 6x10        (largeur max de cellule x hauteur ; la hauteur est celle de chaque glyphe)
    baseline: 8       (rangée de la ligne de base, 0 = haut)
    color: w          (caractère de palette partagée pour les glyphes)
    == A              (nom du glyphe : un caractère, ou SPACE)
    .###.             (10 lignes, même largeur pour toutes ; '#' = pixel, '.' = vide)
    ...

Chaque pixel est dessiné à la main : le script ne fait qu'assembler la planche et le fichier .fnt.
Usage : python3 font.py font.txt dossier_sortie/
"""
import sys
import os
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from px import load_palette, hex_to_rgba, HERE  # noqa: E402


def parse(path):
    meta = {}
    glyphs = []
    cur = None
    with open(path, encoding="utf-8") as f:
        for raw in f:
            line = raw.rstrip("\n").rstrip()
            if line.startswith("== "):
                name = line[3:].strip()
                ch = " " if name == "SPACE" else name
                if len(ch) != 1:
                    raise SystemExit(f"glyphe invalide : '{name}'")
                cur = [ch, []]
                glyphs.append(cur)
                continue
            if cur is None:
                s = line.strip()
                if not s or s.startswith("#"):
                    continue
                k, v = s.split(":", 1)
                meta[k.strip()] = v.split("<-")[0].strip()
                continue
            if line.strip() == "":
                continue
            cur[1].append(line.strip())
    cw, ch_ = (int(x) for x in meta["cell"].lower().split("x"))
    for name, rows in glyphs:
        if len(rows) != ch_:
            raise SystemExit(f"glyphe '{name}' : {len(rows)} lignes, {ch_} attendues")
        w = len(rows[0])
        for r in rows:
            if len(r) != w:
                raise SystemExit(f"glyphe '{name}' : largeurs inégales")
            if set(r) - set("#."):
                raise SystemExit(f"glyphe '{name}' : caractère inconnu dans '{r}'")
    return meta, glyphs, cw, ch_


def main():
    src, outdir = sys.argv[1], sys.argv[2]
    meta, glyphs, cw, chh = parse(src)
    pal = load_palette(os.path.join(HERE, "palette.txt"))
    color = hex_to_rgba(pal[meta.get("color", "w")])
    base = int(meta.get("baseline", chh - 2))
    per_row = 16
    rows_n = (len(glyphs) + per_row - 1) // per_row
    W, H = per_row * (cw + 1), rows_n * (chh + 1)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    lines = []
    for i, (name, rows) in enumerate(glyphs):
        gx, gy = (i % per_row) * (cw + 1), (i // per_row) * (chh + 1)
        gw = len(rows[0])
        for y, r in enumerate(rows):
            for x, c in enumerate(r):
                if c == "#":
                    img.putpixel((gx + x, gy + y), color)
        lines.append(
            f"char id={ord(name)} x={gx} y={gy} width={gw} height={chh} "
            f"xoffset=0 yoffset=0 xadvance={gw + 1} page=0 chnl=15"
        )
    os.makedirs(outdir, exist_ok=True)
    img.save(os.path.join(outdir, "font.png"))
    fnt = [
        f'info face="Echo" size={chh} bold=0 italic=0 charset="" unicode=1 stretchH=100 smooth=0 aa=1 padding=0,0,0,0 spacing=1,1',
        f"common lineHeight={chh + 1} base={base + 1} scaleW={W} scaleH={H} pages=1 packed=0",
        'page id=0 file="font.png"',
        f"chars count={len(lines)}",
    ] + lines
    with open(os.path.join(outdir, "font.fnt"), "w", encoding="utf-8") as f:
        f.write("\n".join(fnt) + "\n")
    big = img.resize((W * 6, H * 6), Image.NEAREST)
    big.save(os.path.join(outdir, "font@6.png"))
    print(f"ok {len(glyphs)} glyphes -> {outdir}")


if __name__ == "__main__":
    main()
