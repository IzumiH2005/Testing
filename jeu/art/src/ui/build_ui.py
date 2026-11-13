#!/usr/bin/env python3
"""build_ui.py : assets d'interface d'ÉCHO (famille F9, UI_UX §7), palette v2.

Deux étages, pour que chaque pixel reste éditable à la main :
  1. SEED   : chaque asset est dessiné ici par coordonnées explicites (lettres de palette_v2),
              ou lu depuis une source à la main (icons12.txt, icons16.txt), puis écrit comme
              grille texte au format tools/px.py dans art/src/ui/grids/<nom>.txt.
  2. RENDER : chaque grille est traduite en PNG (game/assets/ui/<nom>.png), copie @8 et
              planche de contrôle (art/out/ui/<nom>@8.png, <nom>_planche.png).

Une grille qui contient la ligne « # manuel » n'est plus jamais réécrite par le seed :
on peut donc la retoucher à la main puis relancer le script.

Usage : python3 build_ui.py            (seed + render de tout)
        python3 build_ui.py --render   (render seul des grilles existantes)
        python3 build_ui.py nom1 nom2  (seulement ces assets)
"""
import math
import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from px import load_palette, hex_to_rgba  # noqa: E402

PAL_PATH = os.path.join(ROOT, "studio", "palette_v2.txt")
PAL = load_palette(PAL_PATH)
GRIDS = os.path.join(HERE, "grids")
OUT_GAME = os.path.join(ROOT, "game", "assets", "ui")
OUT_ART = os.path.join(ROOT, "art", "out", "ui")
for d in (GRIDS, OUT_GAME, OUT_ART):
    os.makedirs(d, exist_ok=True)


# ----------------------------------------------------------------------------------------------
# Toile
# ----------------------------------------------------------------------------------------------
class C:
    def __init__(self, w, h, fill="."):
        self.w, self.h = w, h
        self.g = [[fill] * w for _ in range(h)]

    def px(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h and c is not None:
            self.g[y][x] = c

    def get(self, x, y):
        if 0 <= x < self.w and 0 <= y < self.h:
            return self.g[y][x]
        return "."

    def rect(self, x, y, w, h, c):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.px(xx, yy, c)

    def hl(self, x0, x1, y, c):
        for x in range(x0, x1 + 1):
            self.px(x, y, c)

    def vl(self, x, y0, y1, c):
        for y in range(y0, y1 + 1):
            self.px(x, y, c)

    def ring(self, x, y, w, h, tl, br=None, cut=False):
        """Anneau 1 px : haut+gauche en tl, bas+droite en br. cut = coins vides (arrondi)."""
        br = br or tl
        x1, y1 = x + w - 1, y + h - 1
        a = 1 if cut else 0
        self.hl(x + a, x1 - a, y, tl)
        self.vl(x, y + a, y1 - a, tl)
        self.hl(x + a, x1 - a, y1, br)
        self.vl(x1, y + a, y1 - a, br)
        if not cut:
            self.px(x1, y, br)  # coin haut-droit : côté ombre (lumière haut-gauche)
            self.px(x, y1, br)

    def put(self, x, y, rows, transparent="."):
        if isinstance(rows, str):
            rows = rows.split("/")
        for j, r in enumerate(rows):
            for i, ch in enumerate(r):
                if ch != transparent:
                    self.px(x + i, y + j, ch)

    def blit(self, o, x, y):
        for j in range(o.h):
            for i in range(o.w):
                if o.g[j][i] != ".":
                    self.px(x + i, y + j, o.g[j][i])

    def recolor(self, mapping):
        for row in self.g:
            for i, ch in enumerate(row):
                if ch in mapping:
                    row[i] = mapping[ch]

    def outline(self, col="k", skip="", diag=False):
        src = [r[:] for r in self.g]
        nb = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        if diag:
            nb += [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for y in range(self.h):
            for x in range(self.w):
                if src[y][x] != ".":
                    continue
                for dx, dy in nb:
                    xx, yy = x + dx, y + dy
                    if 0 <= xx < self.w and 0 <= yy < self.h:
                        s = src[yy][xx]
                        if s != "." and s not in skip:
                            self.g[y][x] = col
                            break

    def fliph(self):
        o = C(self.w, self.h)
        for y in range(self.h):
            o.g[y] = self.g[y][::-1]
        return o

    def copy(self):
        o = C(self.w, self.h)
        o.g = [r[:] for r in self.g]
        return o


def strip(frames):
    w = sum(f.w for f in frames)
    h = max(f.h for f in frames)
    o = C(w, h)
    x = 0
    for f in frames:
        o.blit(f, x, 0)
        x += f.w
    return o


def stack(rows):
    w = max(r.w for r in rows)
    o = C(w, sum(r.h for r in rows))
    y = 0
    for r in rows:
        o.blit(r, 0, y)
        y += r.h
    return o


BAYER4 = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]


def bayer(x, y, level):
    """level 0..16 : True si le pixel est allumé au taux level/16."""
    return BAYER4[y % 4][x % 4] < level


# ----------------------------------------------------------------------------------------------
# Écriture / rendu des grilles
# ----------------------------------------------------------------------------------------------
REGISTRY = {}   # nom -> (fonction, frames, en-tête descriptif)


def asset(name, frames=1, doc=""):
    def deco(fn):
        REGISTRY[name] = (fn, frames, doc)
        return fn
    return deco


def write_grid(name, canvas, frames, doc):
    path = os.path.join(GRIDS, name + ".txt")
    if os.path.exists(path) and "# manuel" in open(path, encoding="utf-8").read():
        print(f"  {name}: grille marquée « # manuel », seed ignoré")
        return
    lines = []
    for d in doc.strip().splitlines():
        lines.append("# " + d.strip())
    lines.append("# Grille générée par build_ui.py. Ajouter « # manuel » pour la figer et la retoucher.")
    lines.append("palette: " + PAL_PATH)
    lines.append(f"size: {canvas.w}x{canvas.h}")
    lines.append(f"frames: {frames}")
    lines.append("---")
    for r in canvas.g:
        lines.append("".join(r))
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def read_grid(name):
    path = os.path.join(GRIDS, name + ".txt")
    rows, size, frames, ing = [], None, 1, False
    for raw in open(path, encoding="utf-8"):
        line = raw.rstrip("\n")
        if not ing:
            s = line.strip()
            if s == "---":
                ing = True
            elif s.startswith("size:"):
                size = tuple(int(v) for v in s[5:].strip().split("x"))
            elif s.startswith("frames:"):
                frames = int(s[7:])
            continue
        rows.append(line)
    w, h = size
    rows = (rows + [""] * h)[:h]
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    bad = set()
    for y, r in enumerate(rows):
        for x, ch in enumerate(r[:w].ljust(w, ".")):
            if ch == ".":
                continue
            if ch not in PAL:
                bad.add(ch)
                continue
            img.putpixel((x, y), hex_to_rgba(PAL[ch]))
    if bad:
        raise SystemExit(f"{name}: lettres hors palette_v2 : {sorted(bad)}")
    return img, frames


def luma(c):
    r, g, b = [v / 255 for v in c[:3]]
    return 0.299 * r + 0.587 * g + 0.114 * b


def planche(name, img, frames):
    """×s sur b · ×s sur p · gris · silhouette. Les images sont séparées par 2 px."""
    w, h = img.size
    fw = w // frames
    s = max(1, min(4, 1100 // (w + 2 * frames)))
    if w * s < 200:
        s = max(s, min(8, 200 // w))
    gap = 2

    def spread(bg, mode):
        W = (fw + gap) * frames + gap
        o = Image.new("RGBA", (W, h + 2 * gap), hex_to_rgba(PAL[bg]))
        for i in range(frames):
            fr = img.crop((i * fw, 0, (i + 1) * fw, h))
            if mode == "grey":
                fr2 = Image.new("RGBA", fr.size, (0, 0, 0, 0))
                for y in range(h):
                    for x in range(fw):
                        c = fr.getpixel((x, y))
                        if c[3]:
                            v = int(luma(c) * 255)
                            fr2.putpixel((x, y), (v, v, v, 255))
                fr = fr2
            elif mode == "sil":
                fr2 = Image.new("RGBA", fr.size, (0, 0, 0, 0))
                for y in range(h):
                    for x in range(fw):
                        if fr.getpixel((x, y))[3]:
                            fr2.putpixel((x, y), hex_to_rgba(PAL["k"]))
                fr = fr2
            o.alpha_composite(fr, (gap + i * (fw + gap), gap))
        return o.resize((o.width * s, o.height * s), Image.NEAREST)

    parts = [spread("b", "n"), spread("p", "n"), spread("b", "grey"), spread("p", "sil")]
    W = max(p.width for p in parts)
    H = sum(p.height + 4 for p in parts) + 14
    sheet = Image.new("RGBA", (W, H), hex_to_rgba(PAL["k"]))
    try:
        from build_fonts import text_strip
        lab = text_strip("font_5", f"{name.upper()} {w}X{h} ({frames}) X{s}", "k")
        sheet.alpha_composite(lab, (0, 0))
    except Exception:
        pass
    y = 14
    for p in parts:
        sheet.alpha_composite(p, (0, y))
        y += p.height + 4
    sheet.save(os.path.join(OUT_ART, name + "_planche.png"))


def render(name):
    img, frames = read_grid(name)
    img.save(os.path.join(OUT_GAME, name + ".png"))
    img.resize((img.width * 8, img.height * 8), Image.NEAREST).save(os.path.join(OUT_ART, name + "@8.png"))
    planche(name, img, frames)
    return img, frames


# ----------------------------------------------------------------------------------------------
# Sources d'icônes à la main (icons12.txt, icons16.txt)
# ----------------------------------------------------------------------------------------------
def read_icons(path, size):
    """Blocs « == nom [outline=k|r|none] [noout=xy] » suivis de size rangées.
    Le contour est ajouté par dilatation 4-voisins (sauf outline=none)."""
    icons, cur, opts, rows = [], None, {}, []

    def flush():
        if cur is None:
            return
        c = C(size, size)
        for y, r in enumerate((rows + [""] * size)[:size]):
            if len(r) != size:
                print(f"  ! {os.path.basename(path)} {cur} rangée {y} : {len(r)} car.")
            for x, ch in enumerate(r[:size]):
                if ch != ".":
                    c.px(x, y, ch)
        ol = opts.get("outline", "k")
        if ol != "none":
            c.outline(ol, skip=opts.get("noout", ""))
            if ol != "k" and opts.get("outer", "") == "k":
                c.outline("k")
        icons.append((cur, c))

    for raw in open(path, encoding="utf-8"):
        line = raw.rstrip("\n")
        if line.startswith("#") or (not line.strip() and cur is None):
            continue
        if line.startswith("=="):
            flush()
            parts = line[2:].split()
            cur, rows = parts[0], []
            opts = dict(p.split("=", 1) for p in parts[1:])
            continue
        if line.strip():
            rows.append(line.strip())
    flush()
    return icons


ICONS12 = read_icons(os.path.join(HERE, "icons12.txt"), 12) if os.path.exists(os.path.join(HERE, "icons12.txt")) else []
ICONS16 = read_icons(os.path.join(HERE, "icons16.txt"), 16) if os.path.exists(os.path.join(HERE, "icons16.txt")) else []


def icon12(name):
    for n, c in ICONS12:
        if n == name:
            return c
    raise KeyError(name)


def icon16(name):
    for n, c in ICONS16:
        if n == name:
            return c
    raise KeyError(name)


from ui_assets import *  # noqa: E402,F401,F403  (les dessins, séparés pour la lisibilité)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    render_only = "--render" in sys.argv
    names = args or list(REGISTRY)
    for n in names:
        fn, frames, doc = REGISTRY[n]
        if not render_only:
            c = fn()
            write_grid(n, c, frames, doc)
        img, fr = render(n)
        print(f"ok {n}: {img.width}x{img.height} ({fr} images)")
    contact()


def contact():
    """Planche générale : tous les assets ×2 sur d, étiquetés."""
    from build_fonts import text_strip
    items = []
    for n in REGISTRY:
        p = os.path.join(OUT_GAME, n + ".png")
        if os.path.exists(p):
            items.append((n, Image.open(p).convert("RGBA")))
    W = 1200
    x = y = 0
    rowh = 0
    placed = []
    for n, im in items:
        s = 2 if im.width * 2 <= W else 1
        w, h = im.width * s, im.height * s + 12
        if x + w > W:
            x, y = 0, y + rowh + 6
            rowh = 0
        placed.append((n, im, s, x, y))
        x += w + 8
        rowh = max(rowh, h)
    sheet = Image.new("RGBA", (W, y + rowh + 6), hex_to_rgba(PAL["d"]))
    for n, im, s, x, y in placed:
        sheet.alpha_composite(text_strip("font_5", n.upper(), "d"), (x, y))
        sheet.alpha_composite(im.resize((im.width * s, im.height * s), Image.NEAREST), (x, y + 12))
    sheet.save(os.path.join(OUT_ART, "planche_ui.png"))
    print("planche_ui.png", sheet.size)


if __name__ == "__main__":
    main()
