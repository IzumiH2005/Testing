#!/usr/bin/env python3
"""gen_traps.py : assemble les sources .txt des pièges (F3) et créatures (F11) d'ÉCHO.

Les grilles sont dessinées à la main dans les fichiers traps_*.py voisins (chaînes de caractères).
Ce script ne fait que :
  - assembler les images d'une bande côte à côte (cellule unique, pivot constant, E8) ;
  - appliquer l'échange de palette des versions gravées (x->q, X->t, z->c, Z->e, k->q) ;
  - rastériser les deux formes qui tournent (scie, lustre) puis laisser la retouche à la main
    (les pixels corrigés sont listés dans les grilles "fix") ;
  - écrire les .txt (en-tête : intention, timing, budget, défaut corrigé) puis appeler px.py / planche.py.

Usage : python3 art/src/traps/traps_assets.py [nom ...]
"""
import os
import sys
import shutil
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
PAL = os.path.join(ROOT, "studio", "palette_v2.txt")
ASSETS = os.path.join(ROOT, "game", "assets", "traps")
OUT = os.path.join(ROOT, "art", "out", "traps")
TOOLS = os.path.join(ROOT, "tools")

ECHO = {"x": "q", "X": "t", "z": "c", "Z": "e", "k": "q", "W": "e", "w": "e"}


def G(s):
    """Chaîne multiligne -> liste de lignes (les lignes vides de début/fin sont ignorées)."""
    rows = [r for r in s.strip("\n").split("\n")]
    rows = [r.rstrip() for r in rows]
    return rows


def pad(rows, w, h, ox=0, oy=0):
    """Place la grille dans une cellule w×h, coin haut-gauche en (ox, oy)."""
    out = [["."] * w for _ in range(h)]
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            if ch != "." and ch != " " and 0 <= x + ox < w and 0 <= y + oy < h:
                out[y + oy][x + ox] = ch
    return ["".join(r) for r in out]


def over(base, top, ox=0, oy=0):
    """Superpose top sur base ('.' de top = transparent)."""
    b = [list(r) for r in base]
    for y, r in enumerate(top):
        for x, ch in enumerate(r):
            if ch not in ". " and 0 <= y + oy < len(b) and 0 <= x + ox < len(b[0]):
                b[y + oy][x + ox] = ch
    return ["".join(r) for r in b]


def recolor(rows, m=ECHO):
    return ["".join(m.get(ch, ch) for ch in r) for r in rows]


def hstack(frames):
    h = len(frames[0])
    for f in frames:
        assert len(f) == h, "hauteurs différentes"
    return ["".join(f[y] for f in frames) for y in range(h)]


def norm(rows, w, h):
    rows = [r.ljust(w, ".")[:w] for r in rows]
    while len(rows) < h:
        rows.append("." * w)
    return rows[:h]


def write(name, header, frames, cw, ch, render=True):
    frames = [norm(f, cw, ch) for f in frames]
    grid = hstack(frames)
    w = cw * len(frames)
    path = os.path.join(HERE, name + ".txt")
    with open(path, "w") as f:
        for line in header.strip("\n").split("\n"):
            f.write("# " + line.strip() + "\n" if line.strip() else "#\n")
        f.write(f"palette: {PAL}\n")
        f.write(f"size: {w}x{ch}\n")
        f.write(f"frames: {len(frames)}\n")
        f.write("---\n")
        for r in grid:
            f.write(r + "\n")
    if render:
        png = os.path.join(ASSETS, name + ".png")
        subprocess.run([sys.executable, os.path.join(TOOLS, "px.py"), path, png], check=True)
        big = os.path.join(ASSETS, name + "@8.png")
        shutil.move(big, os.path.join(OUT, name + "@8.png"))
        subprocess.run([sys.executable, os.path.join(TOOLS, "planche.py"), png,
                        os.path.join(OUT, name + "_planche.png")], check=True,
                       stdout=subprocess.DEVNULL)
    return path


REGISTRY = {}


def asset(fn):
    REGISTRY[fn.__name__] = fn
    return fn


