#!/usr/bin/env python3
"""seed_font_l.py : amorce de font_l (grands chiffres et capitales, trait 2 px).

Chaque glyphe est dessiné à la main en squelette 1 px (ci-dessous), puis agrandi ×2 avec
l'algorithme Scale2x (EPX), qui arrondit les marches en diagonale au lieu de les épaissir.
La sortie (font_l.font) est la source éditable : elle se retouche pixel par pixel, et on ne
relance ce script que pour repartir de zéro (il écrase font_l.font).
"""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
SK = {  # caractère : (rangée de départ dans le squelette, rangées) ; capitales = rangées 0-5
 "A": (0, ".##./#..#/#..#/####/#..#/#..#"), "B": (0, "###./#..#/###./#..#/#..#/###."),
 "C": (0, ".###/#.../#.../#.../#.../.###"), "D": (0, "###./#..#/#..#/#..#/#..#/###."),
 "E": (0, "####/#.../###./#.../#.../####"), "F": (0, "####/#.../###./#.../#.../#..."),
 "G": (0, ".###/#.../#.../#.##/#..#/.###"), "H": (0, "#..#/#..#/####/#..#/#..#/#..#"),
 "I": (0, "###/.#./.#./.#./.#./###"), "J": (0, "...#/...#/...#/...#/#..#/.##."),
 "K": (0, "#..#/#.#./##../##../#.#./#..#"), "L": (0, "#.../#.../#.../#.../#.../####"),
 "M": (0, "#...#/##.##/#.#.#/#...#/#...#/#...#"), "N": (0, "#..#/##.#/#.##/#..#/#..#/#..#"),
 "O": (0, ".##./#..#/#..#/#..#/#..#/.##."), "P": (0, "###./#..#/#..#/###./#.../#..."),
 "Q": (0, ".##./#..#/#..#/#..#/#.#./.#.#"), "R": (0, "###./#..#/#..#/###./#.#./#..#"),
 "S": (0, ".###/#.../.##./...#/...#/###."), "T": (0, "###/.#./.#./.#./.#./.#."),
 "U": (0, "#..#/#..#/#..#/#..#/#..#/.##."), "V": (0, "#..#/#..#/#..#/#..#/.##./.##."),
 "W": (0, "#...#/#...#/#.#.#/#.#.#/##.##/#...#"), "X": (0, "#..#/#..#/.##./.##./#..#/#..#"),
 "Y": (0, "#.#/#.#/.#./.#./.#./.#."), "Z": (0, "####/...#/..#./.#../#.../####"),
 "0": (0, ".##./#..#/#.##/##.#/#..#/.##."), "1": (0, ".#./##./.#./.#./.#./###"),
 "2": (0, ".##./#..#/..#./.#../#.../####"), "3": (0, "###./...#/.##./...#/...#/###."),
 "4": (0, "#..#/#..#/####/...#/...#/...#"), "5": (0, "####/#.../###./...#/...#/###."),
 "6": (0, ".##./#.../###./#..#/#..#/.##."), "7": (0, "####/...#/..#./.#../.#../.#.."),
 "8": (0, ".##./#..#/.##./#..#/#..#/.##."), "9": (0, ".##./#..#/#..#/.###/...#/.##."),
 ".": (5, "#"), ",": (5, ".#/#."), ":": (2, "#/./#"),
 "!": (0, "#/#/#/#/./#"), "?": (0, ".##./#..#/..#./.#../..../.#.."),
 "-": (2, "###"), "+": (1, ".#./###/.#."), "/": (0, "...#/..#./..#./.#../.#../#..."),
 "%": (0, "#..#/...#/..#./.#../#.../#..#"), "×": (2, "#.#/.#./#.#"), "'": (0, "#/#"),
 "(": (0, ".#/#./#./#./#./.#"), ")": (0, "#./.#/.#/.#/.#/#."), "=": (2, "###/.../###"),
 "★": (1, "..#../#####/.###./.#.#./#...#"), "◆": (1, ".#./###/.#."),
 "▶": (1, "#../##./###/##./#.."), "·": (2, "#"), "…": (5, "#.#.#"),
 "«": (2, ".#.#/#.#./.#.#"), "»": (2, "#.#./.#.#/#.#."), "’": (0, ".#/#."), "–": (2, "####"),
}
# accents (pleine résolution, rangées 0-1 ; les capitales commencent rangée 3)
MARKS = {"acute": "..##/.##.", "grave": "##../.##.", "circ": ".##./#..#", "diaer": "##.##"}
COMPS = [("É", "E", "acute"), ("È", "E", "grave"), ("Ê", "E", "circ"), ("Ë", "E", "diaer"),
         ("À", "A", "grave"), ("Â", "A", "circ"), ("Ä", "A", "diaer"), ("Î", "I", "circ"),
         ("Ï", "I", "diaer"), ("Ô", "O", "circ"), ("Ö", "O", "diaer"), ("Û", "U", "circ"),
         ("Ù", "U", "grave"), ("Ü", "U", "diaer"), ("Ÿ", "Y", "diaer")]


def scale2x(rows):
    h, w = len(rows), len(rows[0])
    g = lambda x, y: rows[y][x] if 0 <= x < w and 0 <= y < h else "."
    out = [["."] * (2 * w) for _ in range(2 * h)]
    for y in range(h):
        for x in range(w):
            P = g(x, y); A = g(x, y - 1); B = g(x + 1, y); C = g(x - 1, y); D = g(x, y + 1)
            e = [P, P, P, P]
            if C == A and C != D and A != B: e[0] = A
            if A == B and A != C and B != D: e[1] = B
            if D == C and D != B and C != A: e[2] = C
            if B == D and B != A and D != C: e[3] = D
            out[2 * y][2 * x], out[2 * y][2 * x + 1] = e[0], e[1]
            out[2 * y + 1][2 * x], out[2 * y + 1][2 * x + 1] = e[2], e[3]
    return ["".join(r) for r in out]


lines = ["# Police font_l d'ÉCHO : grands chiffres et capitales (score, compte à rebours, titres).",
         "# Trait 2 px, capitales 12 px (rangées 3-14), chasse 10 (M et W : 12). Accents rangées 0-1.",
         "# Amorcée par seed_font_l.py (squelette 1 px dessiné à la main + Scale2x), puis retouchable ici.",
         "name: font_l", "cell: 10x16", "baseline: 14", "line: 16", "space: 4", "color: w", "upper_alias: 1"]
RAW = {  # retouches pleine résolution (le Scale2x arrondit trop les croix)
 "+": (6, "..##../..##../######/######/..##../..##.."),
 "×": (7, "##...##/.##.##./..###../.##.##./##...##"),
}
for ch, (top, sk) in SK.items():
    if ch in RAW:
        t, r = RAW[ch]
        lines.append(f"g {ch} {t} {r} adv={len(r.split('/')[0]) + 2}")
        continue
    rows = scale2x(sk.split("/"))
    w = len(rows[0])
    adv = 10 if w <= 8 else w + 2
    if ch in ".,:!'’()·" or w <= 4:
        adv = w + 2
    lines.append(f"g {ch} {3 + 2 * top} {'/'.join(rows)} adv={adv}")
for name, m in MARKS.items():
    lines.append(f"mark {name} 0 {m}")
for c, b, m in COMPS:
    lines.append(f"c {c} {b} {m}")
open(os.path.join(HERE, "font_l.font"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
print("font_l.font écrit")
