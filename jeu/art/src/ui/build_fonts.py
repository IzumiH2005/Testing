#!/usr/bin/env python3
"""build_fonts.py : polices bitmap d'ÉCHO (palette v2) -> PNG + BMFont texte (.fnt).

Source (.font, éditable à la main) :
    name: font_5            nom des fichiers de sortie
    cell: 5x8               largeur max x hauteur de ligne (doc)
    baseline: 6             rangée (0 = haut) de la dernière rangée des capitales
    line: 8                 lineHeight du .fnt
    space: 3                chasse de l'espace (U+0020) ; U+00A0 = space, U+202F = 1
    color: w                lettre de palette_v2 du remplissage
    upper_alias: 1          (option) a-z et minuscules accentuées pointent vers les capitales
    mark NOM TOP rangées    signe diacritique (rangées séparées par '/', '#' = pixel)
    g CAR TOP rangées [adv=N]   glyphe : TOP = rangée de départ dans la ligne
    c CAR BASE MARQUE [dx=N]    composé : glyphe BASE + MARQUE centrée (+ décalage dx)
    k A B -1                kerning

CAR : un caractère, ou U+XXXX. Tous les pixels sont décidés à la main dans la source ;
ce script ne fait qu'assembler la planche, le .fnt et la variante contour.
Variante contour (--outline) : dilatation 1 px sur 8 voisins en k (#0e0a1a), remplissage w.

Usage : python3 build_fonts.py            (construit toutes les polices *.font du dossier)
"""
import os
import sys
import glob
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
JEU = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(JEU, "tools"))
from px import load_palette, hex_to_rgba  # noqa: E402

PAL = load_palette(os.path.join(JEU, "studio", "palette_v2.txt"))
OUT_GAME = os.path.join(JEU, "game", "assets", "ui")
OUT_ART = os.path.join(JEU, "art", "out", "ui")

LOWER = {chr(c): chr(c).upper() for c in range(ord("a"), ord("z") + 1)}
for lo in "éèêëàâäçîïôöûùüÿæœ":
    LOWER[lo] = lo.upper()


def tok_char(t):
    if t.startswith("U+") and len(t) > 2:
        return chr(int(t[2:], 16))
    if t == "SPACE":
        return " "
    return t


def parse(path):
    meta, marks, glyphs, comps, kern = {}, {}, {}, [], []
    order = []
    with open(path, encoding="utf-8") as f:
        for n, raw in enumerate(f, 1):
            s = raw.strip()
            if not s or s.startswith("#"):
                continue
            parts = s.split()
            if parts[0] == "mark":
                marks[parts[1]] = (int(parts[2]), parts[3].split("/"))
            elif parts[0] == "g":
                ch = tok_char(parts[1])
                rows = parts[3].split("/")
                w = len(rows[0])
                if any(len(r) != w for r in rows):
                    raise SystemExit(f"{path}:{n} glyphe '{ch}' : largeurs inégales")
                adv = None
                for p in parts[4:]:
                    if p.startswith("adv="):
                        adv = int(p[4:])
                glyphs[ch] = (int(parts[2]), rows, adv)
                order.append(ch)
            elif parts[0] == "c":
                dx = 0
                for p in parts[4:]:
                    if p.startswith("dx="):
                        dx = int(p[3:])
                comps.append((tok_char(parts[1]), tok_char(parts[2]), parts[3], dx))
            elif parts[0] == "k":
                kern.append((tok_char(parts[1]), tok_char(parts[2]), int(parts[3])))
            elif ":" in s:
                k, v = s.split(":", 1)
                meta[k.strip()] = v.split("#")[0].strip()
            else:
                raise SystemExit(f"{path}:{n} ligne inconnue : {s}")
    # composés : base + marque (la marque remplace les rangées vides au-dessus de la base)
    for ch, base, mk, dx in comps:
        top, rows, adv = glyphs[base]
        mtop, mrows = marks[mk]
        w = len(rows[0])
        mw = len(mrows[0])
        mx = (w - mw) // 2 + dx
        newtop = min(top, mtop)
        h = max(top + len(rows), mtop + len(mrows)) - newtop
        grid = [["."] * w for _ in range(h)]
        for y, r in enumerate(rows):
            for x, c in enumerate(r):
                if c == "#":
                    grid[top - newtop + y][x] = "#"
        for y, r in enumerate(mrows):
            for x, c in enumerate(r):
                if c == "#":
                    grid[mtop - newtop + y][mx + x] = "#"
        glyphs[ch] = (newtop, ["".join(r) for r in grid], adv)
        order.append(ch)
    return meta, glyphs, order, kern


def render(meta, glyphs, order, kern, outline=False):
    fill = hex_to_rgba(PAL[meta.get("color", "w")])
    kcol = hex_to_rgba(PAL["k"])
    line = int(meta["line"])
    base = int(meta["baseline"])
    space = int(meta.get("space", 3))
    o = 1 if outline else 0
    # rangement : glyphes de gauche à droite, 1 px d'écart, largeur de planche 128
    pad = 1
    items = []
    for ch in order:
        top, rows, adv = glyphs[ch]
        w, h = len(rows[0]) + 2 * o, len(rows) + 2 * o
        items.append((ch, top, rows, adv, w, h))
    W = 128 if not outline else 160
    x = y = 0
    rowh = 0
    pos = {}
    for ch, top, rows, adv, w, h in items:
        if x + w > W:
            x = 0
            y += rowh + pad
            rowh = 0
        pos[ch] = (x, y)
        x += w + pad
        rowh = max(rowh, h)
    H = y + rowh
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    lines = []
    for ch, top, rows, adv, w, h in items:
        gx, gy = pos[ch]
        pix = {(xx, yy) for yy, r in enumerate(rows) for xx, c in enumerate(r) if c == "#"}
        if outline:
            ring = set()
            for (xx, yy) in pix:
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        ring.add((xx + dx, yy + dy))
            for (xx, yy) in ring - pix:
                img.putpixel((gx + xx + 1, gy + yy + 1), kcol)
        for (xx, yy) in pix:
            img.putpixel((gx + xx + o, gy + yy + o), fill)
        a = adv if adv is not None else len(rows[0]) + 1
        lines.append((ch, f"x={gx} y={gy} width={w} height={h} xoffset={-o} yoffset={top - o} xadvance={a} page=0 chnl=15"))
    # espaces : normal, insécable, fine insécable
    for ch, a in ((" ", space), (" ", space), (" ", 1)):
        if ch not in glyphs:
            lines.append((ch, f"x=0 y=0 width=0 height=0 xoffset=0 yoffset=0 xadvance={a} page=0 chnl=15"))
    have = {c for c, _ in lines}
    if meta.get("upper_alias") == "1":
        for lo, up in LOWER.items():
            if lo not in have and up in glyphs:
                lines.append((lo, dict(lines)[up]))
    return img, lines, W, H, line, base


def write(meta, img, lines, W, H, line, base, kern, suffix=""):
    name = meta["name"] + suffix
    os.makedirs(OUT_GAME, exist_ok=True)
    os.makedirs(OUT_ART, exist_ok=True)
    img.save(os.path.join(OUT_GAME, name + ".png"))
    img.resize((W * 8, H * 8), Image.NEAREST).save(os.path.join(OUT_ART, name + "@8.png"))
    have = {c for c, _ in lines}
    kl = [(a, b, v) for a, b, v in kern if a in have and b in have]
    # alias minuscules du kerning (police à capitales seules)
    out = [
        f'info face="{name}" size={line} bold=0 italic=0 charset="" unicode=1 stretchH=100 smooth=0 aa=1 padding=0,0,0,0 spacing=1,1 outline={1 if suffix else 0}',
        f"common lineHeight={line} base={base + 1} scaleW={W} scaleH={H} pages=1 packed=0",
        f'page id=0 file="{name}.png"',
        f"chars count={len(lines)}",
    ]
    for ch, rest in sorted(lines, key=lambda t: ord(t[0])):
        out.append(f"char id={ord(ch)} {rest}")
    if kl:
        out.append(f"kernings count={len(kl)}")
        for a, b, v in kl:
            out.append(f"kerning first={ord(a)} second={ord(b)} amount={v}")
    with open(os.path.join(OUT_GAME, name + ".fnt"), "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    return name


def text_strip(fontname, text, bg="b"):
    """Rend une ligne de texte avec un .fnt construit (pour la planche de contrôle)."""
    fnt = os.path.join(OUT_GAME, fontname + ".fnt")
    atlas = Image.open(os.path.join(OUT_GAME, fontname + ".png"))
    chars, kern, lh = {}, {}, 10
    for l in open(fnt, encoding="utf-8"):
        p = dict(t.split("=", 1) for t in l.split()[1:] if "=" in t)
        if l.startswith("char "):
            chars[int(p["id"])] = {k: int(v) for k, v in p.items() if k != "id" or True}
        elif l.startswith("kerning "):
            kern[(int(p["first"]), int(p["second"]))] = int(p["amount"])
        elif l.startswith("common"):
            lh = int(p["lineHeight"])
    W = 4 + sum(chars.get(ord(c), chars[32])["xadvance"] for c in text) + 4
    img = Image.new("RGBA", (W, lh + 4), hex_to_rgba(PAL[bg]))
    x, prev = 2, None
    for c in text:
        g = chars.get(ord(c))
        if g is None:
            g = chars[ord("?")] if ord("?") in chars else chars[32]
        if prev is not None:
            x += kern.get((prev, ord(c)), 0)
        if g["width"]:
            crop = atlas.crop((g["x"], g["y"], g["x"] + g["width"], g["y"] + g["height"]))
            img.alpha_composite(crop, (x + g["xoffset"], 2 + g["yoffset"]))
        x += g["xadvance"]
        prev = ord(c)
    return img


def main():
    built = []
    for src in sorted(glob.glob(os.path.join(HERE, "*.font"))):
        meta, glyphs, order, kern = parse(src)
        for outline in (False, True):
            if outline and meta.get("outline", "1") != "1":
                continue
            img, lines, W, H, line, base = render(meta, glyphs, order, kern, outline)
            n = write(meta, img, lines, W, H, line, base, kern, "_outline" if outline else "")
            built.append(n)
            print(f"ok {n}: {len([1 for c, _ in lines])} entrées, atlas {W}x{H}")
        # alias historique : font.png / font.fnt = font_7 (assets.gd charge ui/font.fnt)
        if meta["name"] == "font_7":
            img, lines, W, H, line, base = render(meta, glyphs, order, kern, False)
            meta2 = dict(meta, name="font")
            write(meta2, img, lines, W, H, line, base, kern)
    # planche de contrôle
    samples = {
        "font_5": ["SCORE 1234567890 X2 +15", "ÉCLATS À GAGNER ! ÇA ? «OK» …", "◆◇▶↻↑↓←→▮✕★☆∞ 50% (3/7)"],
        "font_7": ["MEILLEUR 98 765 · NIVEAU 12", "ÉCHO RÉCOMPENSE ÀÂÄ ÊËÈ ÎÏ ÔÖ ÛÙÜ Ÿ Ç Æ Œ", "«REJOUER» … – — ◆◇▶↻↑↓←→▮✕★☆∞"],
        "font_8": ["Toujours plus haut. Votre écho grimpe !", "Défi du jour : rejoignez la vague", "àâäéèêëîïôöùûüÿç œæ « Tôt » 3/7 … — ◆★"],
        "font_l": ["0123456789", "ÉCHO MEILLEUR", "+15 X2 ★ 99%"],
    }
    rows = []
    for f in ("font_5", "font_7", "font_8", "font_l"):
        for suf in ("", "_outline"):
            for t in samples[f]:
                bg = "b" if not suf else "m"
                rows.append(text_strip(f + suf, t, bg))
    W = max(r.width for r in rows)
    H = sum(r.height + 1 for r in rows)
    sheet = Image.new("RGBA", (W, H), hex_to_rgba(PAL["k"]))
    y = 0
    for r in rows:
        sheet.alpha_composite(r, (0, y))
        y += r.height + 1
    sheet.resize((W * 3, H * 3), Image.NEAREST).save(os.path.join(OUT_ART, "planche_fonts.png"))
    print("planche_fonts.png", W * 3, H * 3)


if __name__ == "__main__":
    main()
