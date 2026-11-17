#!/usr/bin/env python3
"""Génère anims/victoire_bagarreur.json (voir analyses/victoire_bagarreur.md).

0-60 : sortie de garde (clés de anims/sortie_de_garde.json, raccord exact avec la garde),
puis craquement de la nuque des deux côtés, épaules roulées, poing levé et tenue.

    python3 tools/gen_victoire_bagarreur.py
"""
import json
import os
import subprocess

ICI = os.path.dirname(os.path.abspath(__file__))
ANIMS = os.path.join(ICI, "..", "anims")

# Repos du bagarreur (stature : buste droit, poitrine bombée, épaules en arrière).
SUR = {"root": -5, "spineLow": 3, "chest": 2, "neck": 4, "torsion": 0, "neck_p": 0, "neck_r": 0,
       "epauleN_av": -2, "epauleF_av": -2, "epauleN_haut": 0, "epauleF_haut": 0}
BRAS = {"armN": -6, "foreN": 18, "armF": 6, "foreF": 18,
        "armN_p": 16, "armF_p": -16, "armN_r": 0, "armF_r": 0}
X, Y = 0.0, 87.78
PIEDS = {"legN": [-10.0, 7.5], "legF": [10.0, 7.5]}

# Poing levé : cibles relatives à l'épaule (x devant, y haut, z profondeur, N = z négatif).
POING_N = json.loads(os.environ.get("PN", "[8, 64, -8]"))
POING_F = json.loads(os.environ.get("PF", "[6, -52, 10]"))


def cle(f, haut=None, bras=None, dy=0.0, courbe=None, p=None, mains=None):
    c = {"f": f, "fixe": {"x": X, "y": round(Y + dy, 2)}, "vise": dict(PIEDS)}
    h = dict(SUR)
    h.update(haut or {})
    b = dict(BRAS)
    b.update(bras or {})
    c["fixe"].update(h)
    c["fixe"].update(b)
    c["fixe"].update({"thighN_p": 6, "thighF_p": -6})
    if mains:
        c["mains3d"] = mains
    if courbe:
        c["courbe"] = courbe
    if p:
        c["p"] = p
    return c


def main():
    sortie = json.load(open(os.path.join(ANIMS, "sortie_de_garde.json")))
    cles = [k for k in sortie["cles"] if k["f"] < 60]
    # la sortie de garde finit au repos du stickman ; on la fait finir sur la stature du
    # bagarreur (clé 60 ci-dessous) avec les pieds ramenés sous lui
    cles[0]["courbe"] = "acc-dec"
    LEVE = {"mains3d": None}
    poing = {"N": POING_N, "F": POING_F, "coude_dy": [-26, 30], "ecart": [10, 40]}
    cles += [
        cle(60, courbe="acc-dec"),
        cle(64, courbe="acc", p=2),
        # nuque côté caméra : tension lente, épaule loin qui descend
        cle(86, {"neck_p": -22, "neck_r": 5, "epauleF_haut": -3}, courbe="dec"),
        cle(89, {"neck_p": -26, "neck_r": 6, "epauleF_haut": -3}, courbe="acc-dec"),
        cle(93, {"neck_p": -24, "neck_r": 5, "epauleF_haut": -3}, courbe="acc-dec"),
        cle(106, courbe="acc", p=2),
        cle(126, {"neck_p": 22, "neck_r": -5, "epauleN_haut": -3}, courbe="dec"),
        cle(129, {"neck_p": 26, "neck_r": -6, "epauleN_haut": -3}, courbe="acc-dec"),
        cle(133, {"neck_p": 24, "neck_r": -5, "epauleN_haut": -3}, courbe="acc-dec"),
        # épaules roulées en haut et en arrière
        cle(142, {"epauleN_haut": 3, "epauleF_haut": 3, "epauleN_av": -3, "epauleF_av": -3}, courbe="acc-dec"),
        cle(152, courbe="acc-dec"),
        cle(160, {"neck": 10}, courbe="acc", p=2),
        # poing levé
        cle(184, {"root": -6, "spineLow": 2, "chest": -2, "neck": -10, "torsion": -8, "neck_r": 8,
                  "epauleN_haut": 4, "epauleN_av": -1, "epauleF_av": -3},
            {"armF_p": -18}, dy=1, courbe="dec", mains=poing),
        cle(188, {"root": -6, "spineLow": 2, "chest": -2, "neck": -10, "torsion": -8, "neck_r": 8,
                  "epauleN_haut": 5, "epauleN_av": -1, "epauleF_av": -3},
            {"armF_p": -18}, dy=1, courbe="acc-dec", mains=dict(poing, N=[POING_N[0], POING_N[1] + 2, POING_N[2]])),
    ]
    tenue = {"root": -6, "spineLow": 2, "chest": -2, "neck": -10, "torsion": -8, "neck_r": 8,
             "epauleN_haut": 4, "epauleN_av": -1, "epauleF_av": -3}
    for f, souffle in ((194, 0), (212, 1), (230, 0), (248, 1), (260, 0)):
        h = dict(tenue)
        h["epauleN_haut"] = 4 + souffle
        h["epauleF_haut"] = souffle
        cles.append(cle(f, h, {"armF_p": -18}, dy=1, courbe="acc-dec", mains=poing))
    anim = {"nom": "victoire_bagarreur", "boucle": False, "longueur": 260, "base": "repos",
            "decalage": {"neck": 3}, "ecartement": {"jambes": 9}, "cles": cles}
    out = os.path.join(ANIMS, "victoire_bagarreur.json")
    with open(out, "w") as f:
        json.dump(anim, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(out, len(cles), "clés")
    subprocess.run([os.path.join(ICI, "resout_mains.sh"), out], check=True)


if __name__ == "__main__":
    main()
