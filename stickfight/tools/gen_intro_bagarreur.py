#!/usr/bin/env python3
"""Génère anims/intro_bagarreur.json (voir analyses/intro_bagarreur.md).

Jambes : départ + un cycle + arrêt en un pas de la marche détendue, recollés bout à bout.
Haut du corps : buste droit, épaules reculées, puis craquage du poing une fois arrêté.

    GODOT=… python3 tools/gen_intro_bagarreur.py   (lance tools/resout_mains.sh)
"""
import json
import subprocess
import math
import os

ICI = os.path.dirname(os.path.abspath(__file__))
ANIMS = os.path.join(ICI, "..", "anims")


def charge(nom):
    with open(os.path.join(ANIMS, nom + ".json")) as f:
        return json.load(f)


def ease(u, courbe):
    if courbe == "acc-dec":
        return 0.5 - 0.5 * math.cos(math.pi * u)
    if courbe == "dec":
        return 1 - (1 - u) ** 2
    if courbe == "acc":
        return u ** 2
    return u


def mix(a, b, u):
    return {k: round(a[k] + (b[k] - a[k]) * u, 2) for k in a}


# Repos (poses/repos.json) : haut du corps.
REPOS = {"root": -11, "spineLow": 6, "chest": 9, "neck": 8, "torsion": 0,
         "epauleN_av": 0, "epauleF_av": 0, "epauleN_haut": 0, "epauleF_haut": 0}
# Buste droit, poitrine ouverte, épaules reculées, menton horizontal.
SUR = {"root": -5, "spineLow": 3, "chest": 2, "neck": 4, "torsion": 0,
       "epauleN_av": -2, "epauleF_av": -2, "epauleN_haut": 0, "epauleF_haut": 0}
BRAS_REPOS = {"armN": -10, "foreN": 10, "armF": 8, "foreF": 8,
              "armN_p": 12, "armF_p": -12, "armN_r": 0, "armF_r": 0}
# Mains en place devant le sternum : la paume N posée sur les phalanges du poing F,
# chaque main de son côté en profondeur, sans se traverser (voir l'analyse § 4).
# Cibles du centre des poings, relatives à l'épaule (x devant, y haut, z profondeur,
# N côté caméra = z négatif) ; les angles sont résolus par tools/resout_mains.sh.
MAIN_F = (22, -22, 3)
MAIN_N = (37, -19, -3)
# Coudes ouverts sur les côtés : l'écartement est cherché dans cette plage pour que
# les avant-bras soient horizontaux (coude à la hauteur de la main).
ECART = [40, 75]
# Angles de cette position (sortie de resout_mains, clé 148) : sert au trajet 104 → 136.
PRETE = {"armN": 35.5, "foreN": 101.7, "armF": -0.4, "foreF": 123.7,
         "armN_p": 46.7, "armF_p": -49.9, "armN_r": 52.5, "armF_r": -33.6}


def tronc(f):
    """Haut du corps (sans les bras) pendant la marche."""
    u = min(1.0, f / 20.0)
    return mix(REPOS, SUR, ease(u, "acc-dec"))


def bras_marche(fx):
    """Bras de la marche : balancier un peu plus ample, bras décollés à 16°."""
    return {"armN": round(fx["armN"] * 1.15, 2), "foreN": fx["foreN"] + 4,
            "armF": round(fx["armF"] * 1.15, 2), "foreF": fx["foreF"] + 4,
            "armN_p": 16, "armF_p": -16, "armN_r": 0, "armF_r": 0}


def main():
    dep = charge("marche_detendue_depart")
    cyc = charge("marche_detendue")
    arr = charge("marche_detendue_arret_pas")

    # Jambes et bassin : trois morceaux recollés (décalage en temps et en x).
    morceaux = []
    t0, x0 = 0, 0.0
    for d, longueur in ((dep, 40), (cyc, 56), (arr, 52)):
        for k in d["cles"]:
            f = t0 + k["f"]
            if morceaux and f == morceaux[-1][0]:
                continue
            morceaux.append((f, k, x0))
        t0 += longueur
        x0 = x0 + (46.94 if d is dep else 103.41 if d is cyc else 0)
    X = round(46.94 + 103.41 + 46.94, 2)  # bassin à l'arrêt
    Y = 87.78
    pieds = {"legN": [X - 21.09, 7.5], "legF": [X + 21.09, 7.5]}

    cles = []
    DEBUT_MAINS, MAINS_PRETES = 104, 136
    bras_debut = None
    for f, k, dx in morceaux:
        fx = k["fixe"]
        cle = {"f": f, "fixe": {"x": round(fx["x"] + dx, 2), "y": fx["y"]}, "vise": {}}
        for m, (vx, vy) in k["vise"].items():
            cle["vise"][m] = [round(vx + dx, 2), vy]
        haut = tronc(f)
        if f <= DEBUT_MAINS:
            b = bras_marche(fx)
            # contre-rotation des épaules avec le balancier (épaule proche devant quand
            # le bras proche est devant)
            haut["torsion"] = round(0.25 * (b["armN"] - b["armF"]) / 2, 2)
            if f == DEBUT_MAINS or bras_debut is None or f < DEBUT_MAINS:
                bras_debut = b
        else:
            u = ease(min(1.0, (f - DEBUT_MAINS) / (MAINS_PRETES - DEBUT_MAINS)), "acc-dec")
            b = mix(bras_debut, PRETE, u)
            t_debut = round(0.25 * (bras_debut["armN"] - bras_debut["armF"]) / 2, 2)
            haut["torsion"] = round(t_debut * (1 - u), 2)
        cle["fixe"].update(haut)
        cle["fixe"].update(b)
        if f >= MAINS_PRETES:
            break
        cles.append(cle)

    # Craquage : clés à partir de 136, mains placées par vise (repère local absolu).
    def craque(f, dy_bassin=0.0, haut=None, mains=(0, 0), n_plus=(0, 0), coude_dy=0,
               courbe=None, p=None):
        """mains : décalage des deux mains ensemble ; n_plus : décalage de la main N en
        plus (elle quitte le poing puis revient le frapper) ; coude_dy : hauteur des coudes
        par rapport aux mains (0 = avant-bras horizontaux)."""
        h = dict(SUR)
        h.update(haut or {})
        dxm, dym = mains
        c = {"f": f, "fixe": {"x": X, "y": round(Y - 2.5 + dy_bassin, 2)}, "vise": dict(pieds)}
        c["fixe"].update(h)
        c["fixe"].update({"thighN_p": 13, "thighF_p": -13})
        c["mains3d"] = {"N": [MAIN_N[0] + dxm + n_plus[0], MAIN_N[1] + dym + n_plus[1], MAIN_N[2]],
                        "F": [MAIN_F[0] + dxm, MAIN_F[1] + dym, MAIN_F[2]],
                        "coude_dy": coude_dy, "ecart": ECART}
        if courbe:
            c["courbe"] = courbe
        if p:
            c["p"] = p
        return c

    # Stature : la ligne des épaules reste droite ou en arrière (epaule_av ≤ 0) et le
    # buste ne s'enroule pas. L'effort se lit par les épaules qui montent puis tombent,
    # les coudes qui s'écartent, les genoux qui cèdent et le hochement de tête.
    APPUI1 = {"chest": 0, "neck": 3, "epauleN_haut": 3, "epauleF_haut": 3,
              "epauleN_av": -3, "epauleF_av": -3}
    CRAC1 = {"chest": 2, "neck": 10, "epauleN_haut": -2, "epauleF_haut": -2,
             "epauleN_av": -1, "epauleF_av": -1}
    APPUI2 = {"chest": -1, "neck": 2, "epauleN_haut": 5, "epauleF_haut": 5, "root": -6,
              "epauleN_av": -3, "epauleF_av": -3}
    CRAC2 = {"chest": 2, "neck": 12, "epauleN_haut": -3, "epauleF_haut": -3,
             "epauleN_av": -1, "epauleF_av": -1}
    FIN = {"neck": 1}  # menton qui remonte, regard sur l'adversaire

    cles += [
        craque(136),
        craque(148, courbe="acc-dec"),
        # appui : les mains remontent vers soi, la paume quitte le poing (écart visible)
        craque(158, haut=APPUI1, mains=(-3, 3), n_plus=(2, 7), coude_dy=-3, courbe="acc", p=3),
        # craquement : la paume revient frapper le poing et les deux poussent devant et en bas
        craque(162, dy_bassin=-1.5, haut=CRAC1, mains=(2, -3), n_plus=(-0.5, -0.5), coude_dy=3, courbe="dec"),
        craque(168, dy_bassin=-1.2, haut=CRAC1, mains=(2, -2.5), n_plus=(-0.5, -0.5), coude_dy=3, courbe="acc-dec"),
        craque(180, haut={"neck": 4}, courbe="acc-dec"),
        craque(190, haut=APPUI2, mains=(-4, 4), n_plus=(3, 9), coude_dy=-4, courbe="acc", p=3),
        craque(194, dy_bassin=-2.5, haut=CRAC2, mains=(3, -4), n_plus=(-0.5, -0.5), coude_dy=3, courbe="dec"),
        craque(202, dy_bassin=-2.0, haut=CRAC2, mains=(3, -3.5), n_plus=(-0.5, -0.5), coude_dy=3, courbe="acc-dec"),
        craque(214, haut=FIN, courbe="acc-dec"),
        craque(222, haut=FIN, courbe="acc-dec"),
    ]
    # Retour au repos : les mains se séparent puis descendent.
    fin = {"f": 252, "fixe": {"x": X, "y": Y}, "vise": dict(pieds)}
    fin["fixe"].update(REPOS)
    fin["fixe"].update(BRAS_REPOS)
    cles.append(fin)

    anim = {
        "nom": "intro_bagarreur",
        "boucle": False,
        "longueur": 252,
        "base": "repos",
        "suivante": "idle_repos",
        # pas de retard sur les bras : les deux mains l'une sur l'autre suivent le buste,
        # sinon la poussée sèche les fait glisser l'une dans l'autre
        "decalage": {"chest": 2, "neck": 4},
        "ecartement": {"jambes": 9},
        "cles": cles,
    }
    out = os.path.join(ANIMS, "intro_bagarreur.json")
    with open(out, "w") as f:
        json.dump(anim, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(out, len(cles), "clés")
    # Mains en 3D (profondeur comprise) : remplace "mains3d" par les angles des bras.
    subprocess.run([os.path.join(ICI, "resout_mains.sh"), out], check=True)


if __name__ == "__main__":
    main()
