#!/usr/bin/env python3
"""assemble.py : colle côte à côte les images 32x32 écrites à la main dans frames/<anim>.frames
et écrit la source px.py <anim>.txt (en-tête recopié + bande horizontale).

Il ne décide aucun pixel : il recopie les grilles telles quelles (méthode E6-E, cels).
Format de frames/<anim>.frames :
    # lignes d'en-tête (recopiées dans <anim>.txt)
    palette: ...
    == f1            (début d'une image ; « == f3 = f1 » réutilise une image déjà écrite)
    32 rangées de 32 caractères
Usage : python3 assemble.py <anim>  (depuis n'importe où)
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
W = H = 32

def main(anim):
    src = os.path.join(HERE, "frames", anim + ".frames")
    header, frames, order, cur = [], {}, [], None
    for raw in open(src, encoding="utf-8"):
        line = raw.rstrip("\n")
        if line.startswith("== "):
            parts = line[3:].split("=")
            name = parts[0].strip()
            order.append(name)
            if len(parts) > 1:
                frames[name] = list(frames[parts[1].strip()]); cur = None
            else:
                frames[name] = []; cur = name
            continue
        if cur is None:
            if line.strip():
                header.append(line)
            continue
        if line.strip() == "" and len(frames[cur]) in (0, H):
            continue
        frames[cur].append(line)
    for n in order:
        g = frames[n]
        if len(g) != H:
            sys.exit(f"{anim} {n}: {len(g)} rangées")
        for y, r in enumerate(g):
            if len(r) != W:
                sys.exit(f"{anim} {n} rangée {y}: {len(r)} px '{r}'")
    out = os.path.join(HERE, anim + ".txt")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(header) + "\n")
        f.write(f"size: {W*len(order)}x{H}\n---\n")
        for y in range(H):
            f.write("".join(frames[n][y] for n in order) + "\n")
    print("ok", out, len(order), "images")

if __name__ == "__main__":
    main(sys.argv[1])
