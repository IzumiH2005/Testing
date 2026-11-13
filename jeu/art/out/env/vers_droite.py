#!/usr/bin/env python3
"""vers_droite.py : dérive la grille d'un mur DROIT depuis la grille tracée du mur GAUCHE, par une règle décidée
(pas un miroir : la lumière reste haut-gauche). Par rangée de chaque tuile de 16 px :
    x0 = k (contour de collision côté puits) ; x1 = chanfrein ÉCLAIRÉ (ou joint sur une rangée de joint) ;
    x2..x14 = colonnes 0..12 du mur gauche (motif de blocs décalé de 2 px) ; x15 = joint (vers la colonne extérieure).
Ton de face dominant de la rangée -> (chanfrein, joint) : Crypte s->(m,n), Fonderie 2->(3,1), Bibliothèque 6->(7,5).
Usage : python3 vers_droite.py grille_L.txt grille_R.txt "en-tête (lignes séparées par |)"
"""
import sys

TAB = {"s": ("m", "n"), "2": ("3", "1"), "6": ("7", "5")}

src, out, head = sys.argv[1], sys.argv[2], sys.argv[3]
h, g = open(src, encoding="utf-8").read().split("---\n")
rows = [r for r in g.split("\n") if r]
hl = [l for l in h.split("\n") if l and not l.startswith("#")]
res = []
for r in rows:
    o = ""
    for t in range(len(r) // 16):
        L = r[t * 16:(t + 1) * 16]
        face = max(TAB, key=lambda c: L.count(c))
        if L.count(face) == 0:  # rangée de joint pleine
            jj = max("n15", key=lambda c: L.count(c))
            o += "k" + jj + L[0:13] + jj
            continue
        ch, j = TAB[face]
        joint = L[0] == L[1] == L[2] == j
        o += "k" + (j if joint else ch) + L[0:13] + j
    res.append(o)
with open(out, "w", encoding="utf-8") as f:
    f.write("\n".join("# " + x for x in head.split("|")) + "\n" + "\n".join(hl) + "\n---\n" + "\n".join(res) + "\n")
print("droite", out)
