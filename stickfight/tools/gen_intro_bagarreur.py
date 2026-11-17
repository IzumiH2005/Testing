#!/usr/bin/env python3
"""Génère anims/intro_bagarreur.json (voir analyses/intro_bagarreur.md).

Jambes : départ + un cycle + arrêt en un pas de la marche détendue, recollés bout à bout.
Haut du corps : buste droit, épaules reculées, puis craquage du poing une fois arrêté.

    python3 tools/gen_intro_bagarreur.py
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
# Bras de la clé 136 (sortie de resout_mains) : sert au trajet 104 → 136.
PRETE = {"armN": 38.7, "foreN": 82.2, "armF": 36.6, "foreF": 57.6, "armN_p": 20, "armF_p": -20, "armN_r": 21.9, "armF_r": -32.3}


MAIN_N = tuple(json.loads(os.environ.get("MN", "[48, -13, -2]")))
MAIN_F = tuple(json.loads(os.environ.get("MF", "[50, -29, 4]")))


# Coudes un peu sous les mains : avant-bras presque horizontaux (l'écartement s'ouvre pour ça).
COUDE_DY = float(os.environ.get("CD", -2))
COUDE_N = float(os.environ.get("CN", -16))  # paume par-dessus : avant-bras N qui monte vers elle


# Pendant le craquage, le buste tourne de trois quarts vers la caméra (idée de
# l'utilisateur) : les deux poings, côte à côte en profondeur, se séparent à l'écran. La
# tête reste tournée vers l'adversaire (neck_r compense).
TROIS_QUARTS = float(os.environ.get("T", -25))
SENS = float(os.environ.get("SENS", 1))


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
            haut["torsion"] = round(t_debut * (1 - u) + TROIS_QUARTS * u, 2)
            haut["neck_r"] = round(-TROIS_QUARTS * u, 2)
            haut["epauleN_av"] = haut["epauleF_av"] = round(-2 + u, 2)
        cle["fixe"].update(haut)
        cle["fixe"].update(b)
        if f >= MAINS_PRETES:
            break
        cles.append(cle)

    # Craquage : clés à partir de 136, mains placées en 3D par mains3d (repère de l'épaule).
    def craque(f, dy_bassin=0.0, haut=None, mains=(0, 0), coudes=35, courbe=None, p=None):
        h = dict(SUR)
        h.update({"epauleN_av": -1, "epauleF_av": -1})
        h.update(haut or {})
        # buste tourné de trois quarts vers la caméra, tête qui reste sur l'adversaire
        h["torsion"] = TROIS_QUARTS
        h["neck_r"] = -TROIS_QUARTS
        dxm, dym = mains
        c = {"f": f, "fixe": {"x": X, "y": round(Y - 2.5 + dy_bassin, 2)}, "vise": dict(pieds)}
        c["fixe"].update(h)
        c["fixe"].update({"thighN_p": 13, "thighF_p": -13, "armN_p": coudes, "armF_p": -coudes})
        # mains placées en 3D (tools/resout_mains.sh) : même endroit que la première version
        # (devant la poitrine, loin du buste), mais l'une à côté de l'autre en profondeur, au
        # contact, au lieu de l'une dans l'autre
        # les mains tournent avec le buste (même angle que la torsion, autour de la verticale)
        a = math.radians(SENS * TROIS_QUARTS)

        def tourne(m, dx=0.0, dy=0.0):
            x, z = m[0] + dx, m[2]
            return [round(x * math.cos(a) - z * math.sin(a), 2), m[1] + dy,
                    round(x * math.sin(a) + z * math.cos(a), 2)]
        # le poing F ne bouge pas ; la paume N (posée dessus) appuie et pousse
        c["mains3d"] = {"N": tourne(MAIN_N, dxm, dym), "F": tourne(MAIN_F),
                        "coude_dy": [COUDE_N, COUDE_DY], "coude_dx": [19, 19],
                        "ecart": [float(os.environ.get("EMIN", 20)), float(os.environ.get("EMAX", 40))]}
        if courbe:
            c["courbe"] = courbe
        if p:
            c["p"] = p
        return c

    # Stature (règle 6) : épaules droites ou en arrière, buste droit, même au craquement ;
    # l'effort se lit par les épaules qui montent puis tombent, les genoux, la tête.
    APPUI1 = {"chest": 0, "neck": 3, "epauleN_haut": 2, "epauleF_haut": 2,
              "epauleN_av": -3, "epauleF_av": -3}
    CRAC1 = {"chest": 2, "neck": 10, "epauleN_haut": -2, "epauleF_haut": -2}
    APPUI2 = {"chest": -1, "neck": 2, "epauleN_haut": 2, "epauleF_haut": 2, "root": -6,
              "epauleN_av": -3, "epauleF_av": -3}
    CRAC2 = {"chest": 2, "neck": 13, "epauleN_haut": -3, "epauleF_haut": -3}
    FIN = {"neck": 1}  # menton qui remonte, regard sur l'adversaire

    cles += [
        craque(136),
        craque(148, courbe="acc-dec"),
        craque(158, haut=APPUI1, mains=(-0.5, -0.2), courbe="acc", p=3),
        craque(160, dy_bassin=-1.5, haut=CRAC1, mains=(3, 0.5), courbe="dec"),
        craque(168, dy_bassin=-1.2, haut=CRAC1, mains=(2.5, 0.5), courbe="acc-dec"),
        craque(180, haut={"neck": 4}, courbe="acc-dec"),
        craque(190, haut=APPUI2, mains=(-0.5, -0.2), courbe="acc", p=3),
        craque(192, dy_bassin=-2.5, haut=CRAC2, mains=(4, 0.5), courbe="dec"),
        craque(202, dy_bassin=-2.0, haut=CRAC2, mains=(3.5, 0.5), courbe="acc-dec"),
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
        "decalage": {"chest": 2, "neck": 4},
        "ecartement": {"jambes": 9},
        "cles": cles,
    }
    out = os.path.join(ANIMS, "intro_bagarreur.json")
    with open(out, "w") as f:
        json.dump(anim, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(out, len(cles), "clés")
    subprocess.run([os.path.join(ICI, "resout_mains.sh"), out], check=True)


if __name__ == "__main__":
    main()
