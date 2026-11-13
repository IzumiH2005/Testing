"""pxlib.py : outils d'assemblage communs aux FX (F2, F4) et à la marée (F5) d'ÉCHO.

Rien ici ne calcule une forme : les grilles sont écrites à la main dans fx_assets.py
et tide_assets.py. Ce module :
  - pose une grille dans une cellule (pad, over), recolore (recolor), décale (shift) ;
  - assemble une bande horizontale (cellule unique, pivot constant) ;
  - écrit le .txt (en-tête = intention + timing) puis appelle tools/px.py et tools/planche.py ;
  - range ×1 dans game/assets/<dossier>, @8 et planche dans art/out/<dossier>.
"""
import os
import sys
import shutil
import subprocess

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
PAL = os.path.join(ROOT, "studio", "palette_v2.txt")
TOOLS = os.path.join(ROOT, "tools")

GOLD2ECHO = {"y": "e", "G": "c", "g": "t", "o": "q"}


def G(s):
    rows = s.strip("\n").split("\n")
    return [r.rstrip() for r in rows]


def blank(w, h):
    return ["." * w for _ in range(h)]


def pad(rows, w, h, ox=0, oy=0):
    return over(blank(w, h), rows, ox, oy)


def over(base, top, ox=0, oy=0):
    b = [list(r) for r in base]
    for y, r in enumerate(top):
        for x, ch in enumerate(r):
            if ch not in ". " and 0 <= y + oy < len(b) and 0 <= x + ox < len(b[0]):
                b[y + oy][x + ox] = ch
    return ["".join(r) for r in b]


def recolor(rows, m):
    return ["".join(m.get(ch, ch) for ch in r) for r in rows]


def wrapx(rows, dx):
    """Décalage horizontal bouclé (tuile qui défile)."""
    w = len(rows[0])
    dx %= w
    return [r[-dx:] + r[:-dx] if dx else r for r in rows]


def check(rows, w, h, name=""):
    assert len(rows) <= h, f"{name}: {len(rows)} rangées > {h}"
    for i, r in enumerate(rows):
        assert len(r) <= w, f"{name}: rangée {i} = {len(r)} px > {w} : {r}"


def norm(rows, w, h):
    rows = [r.ljust(w, ".")[:w] for r in rows]
    while len(rows) < h:
        rows.append("." * w)
    return rows[:h]


def hstack(frames):
    return ["".join(f[y] for f in frames) for y in range(len(frames[0]))]


class Writer:
    def __init__(self, src_dir, assets_dir, out_dir):
        self.src, self.assets, self.out = src_dir, assets_dir, out_dir

    def write(self, name, header, frames, cw, ch, local=None):
        for i, f in enumerate(frames):
            check(f, cw, ch, f"{name}[{i}]")
        frames = [norm(f, cw, ch) for f in frames]
        grid = hstack(frames)
        path = os.path.join(self.src, name + ".txt")
        with open(path, "w") as f:
            for line in header.strip("\n").split("\n"):
                f.write("# " + line.strip() + "\n" if line.strip() else "#\n")
            f.write(f"palette: {PAL}\n")
            for k, v in (local or {}).items():
                f.write(f"= {k} {v}\n")
            f.write(f"size: {cw * len(frames)}x{ch}\n")
            f.write(f"frames: {len(frames)}\n---\n")
            for r in grid:
                f.write(r + "\n")
        png = os.path.join(self.assets, name + ".png")
        subprocess.run([sys.executable, os.path.join(TOOLS, "px.py"), path, png], check=True,
                       stdout=subprocess.DEVNULL)
        shutil.move(os.path.join(self.assets, name + "@8.png"), os.path.join(self.out, name + "@8.png"))
        subprocess.run([sys.executable, os.path.join(TOOLS, "planche.py"), png,
                        os.path.join(self.out, name + "_planche.png")], check=True,
                       stdout=subprocess.DEVNULL)
        return png
