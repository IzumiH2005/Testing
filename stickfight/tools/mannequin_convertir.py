#!/usr/bin/env python3
"""Convertit les sources MakeHuman / MPFB2 (CC0) en un seul fichier compact
mannequin/humain.json : le corps seul (sans les géométries d'aide), en mètres,
repère Blender (z en haut, -y devant, +x = gauche du personnage), avec les os
du rig « game_engine » et les poids de skinning.

  python3 tools/mannequin_convertir.py base.obj rig.game_engine.json weights.game_engine.json
"""
import json, sys, os

obj, rigf, wf = sys.argv[1:4]
V, F, g = [], [], None
for l in open(obj):
    if l.startswith("v "):
        x, y, z = (float(t) for t in l.split()[1:4])
        V.append((x * 0.1, -z * 0.1, y * 0.1))
    elif l.startswith("g "):
        g = l.split()[1]
    elif l.startswith("f ") and g == "body":
        F.append([int(t.split("/")[0]) - 1 for t in l.split()[1:]])
garde = sorted({i for f in F for i in f})
neuf = {o: n for n, o in enumerate(garde)}
rig = json.load(open(rigf))
os_ = {b: {"parent": d.get("parent") or None,
           "tete": [round(c, 4) for c in d["head"]["default_position"]],
           "queue": [round(c, 4) for c in d["tail"]["default_position"]]} for b, d in rig.items()}
poids = {}
for b, lst in json.load(open(wf))["weights"].items():
    l2 = [[neuf[i], round(w, 3)] for i, w in lst if i in neuf and w >= 0.002]
    if l2 and b in rig:
        poids[b] = l2
out = {"licence": "CC0 1.0 (MakeHuman / MPFB2), voir mannequin/LICENCE.md",
       "unite": "m", "repere": "z en haut, -y devant, +x gauche du personnage",
       "sommets": [[round(c, 4) for c in V[o]] for o in garde],
       "faces": [[neuf[i] for i in f] for f in F], "os": os_, "poids": poids}
dst = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "mannequin", "humain.json")
json.dump(out, open(dst, "w"), separators=(",", ":"))
print(dst, len(out["sommets"]), "sommets", len(out["faces"]), "faces", len(poids), "os pondérés")
