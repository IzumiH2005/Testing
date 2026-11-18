#!/usr/bin/env python3
"""Remplit web/animateur.html avec les poses et les animations du jeu, pour le publier.
  $GODOT --headless --path . -s tools/anims_vers_animateur.gd -- /tmp/anims.json
  python3 tools/remplir_animateur.py /tmp/anims.json sortie.html
Le fichier d'entrée peut être la sortie brute du script Godot ou sa forme compacte."""
import glob, json, os, sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def compacte(a):
    if "k" in a:
        return a
    cles = []
    for c in a["cles"]:
        k = {"f": c["f"], "x": round(c["x"], 2), "y": round(c["y"], 2),
             "a": {n: round(v, 2) for n, v in c["angles"].items() if round(v, 2) != 0}}
        if c.get("courbe", "auto") != "auto": k["c"] = c["courbe"]
        if c.get("p", 2) != 2: k["p"] = c["p"]
        if c.get("plate"): k["pl"] = 1
        if c.get("facing", 1) != 1: k["fa"] = c["facing"]
        cles.append(k)
    return {"L": a["longueur"], "b": a["boucle"], "k": cles}


anims = {n: compacte(a) for n, a in json.load(open(sys.argv[1])).items()}
poses = {}
for f in glob.glob(os.path.join(RACINE, "poses", "*.json")):
    p = json.load(open(f))
    if "angles" in p:
        poses[os.path.basename(f)[:-5]] = {"x": p.get("x", 0), "y": p.get("y", 0),
                                           "facing": p.get("facing", 1), "angles": p["angles"]}
d = json.dumps({"poses": poses, "anims": anims}, separators=(",", ":"), ensure_ascii=False)
h = open(os.path.join(RACINE, "web", "animateur.html")).read()
a, b = h.index("/*DONNEES*/") + 11, h.index("/*FIN*/")
open(sys.argv[2], "w").write(h[:a] + d + h[b:])
print(sys.argv[2], len(poses), "poses,", len(anims), "animations")
