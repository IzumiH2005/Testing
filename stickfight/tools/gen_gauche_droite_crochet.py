#!/usr/bin/env python3
"""Génère anims/gauche_droite_crochet_bagarreur.json (fiche : analyses/gauche_droite_crochet_bagarreur.md).

Un-deux-trois du bagarreur : le gauche-droite (images 0-17 reprises telles quelles de
anims/gauche_droite_bagarreur.json), puis un crochet du gauche au visage. Chaque clé du crochet
est écrite en entier (état complet). Les jambes ont été résolues pour que chevilles et pointes
restent à leur place de garde (pied avant à plat, talon arrière qui redescend).
"""
import json
import os

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)

GD = json.load(open(os.path.join(RACINE, "anims", "gauche_droite_bagarreur.json")))
CLES_GD = {c["f"]: c for c in GD["cles"]}

GARDE_N = dict(armN=31.3, armN_p=14.6, armN_r=3.7, foreN=127.2, epauleN_haut=-3, epauleN_av=0)


def cou(tb, t):
    """Le menton reste sur la cible : neck_r = -0,6 x (tb + t + 16)."""
    return round(-0.6 * (tb + t + 16), 1)


def cle(f, nom, tb, t, x, y, bras, jambes, courbe=None, **autres):
    fixe = dict(torsionBassin=tb, torsion=t, neck_r=cou(tb, t), x=x, y=y)
    fixe.update(bras)
    fixe.update(jambes)
    fixe.update(autres)
    c = {"f": f, "nom": nom, "fixe": fixe}
    if courbe:
        c["courbe"] = courbe
    return c


CROCHET = [
    cle(19, "le poing droit reste un instant au bout de la ligne",
        16, 35, 9.6, 85,
        dict(armF=39, armF_p=-0.5, armF_r=6.5, foreF=116, armN=98.5, armN_p=45.5, armN_r=-34,
             foreN=14, epauleF_av=-3, epauleF_haut=1, epauleN_haut=-1),
        {k: CLES_GD[20]["fixe"][k] for k in ("footF", "footN", "shinF", "shinN", "thighF", "thighF_p",
                                             "thighF_r", "thighN", "thighN_p", "thighN_r")},
        courbe="acc"),
    cle(22, "la droite revient sur sa ligne, la hanche repart, le coude gauche se lève",
        6, 26, 7, 85.3,
        dict(armN=38.5, armN_p=27.5, armN_r=-32, foreN=106, epauleN_haut=-3,
             armF=60, armF_p=-30, armF_r=-20, foreF=120, epauleF_av=-2, epauleF_haut=1),
        dict(thighF=23.4, thighF_p=-6.8, thighF_r=-7, shinF=39.7, footF=16.9,
             thighN=-30, thighN_p=9.5, thighN_r=6, shinN=9.1, footN=-26.3)),
    cle(24, "armé : poing droit au menton, coude gauche à hauteur d'épaule, épaules encore tournées",
        -5, 30, 6, 85.2,
        dict(GARDE_N, armF=78, armF_p=-40, armF_r=-40, foreF=115, epauleF_av=-1, epauleF_haut=1),
        dict(thighF=23, thighF_p=-12, thighF_r=4, shinF=41, footF=14.7,
             thighN=-26.2, thighN_p=14.9, thighN_r=2, shinN=11.9, footN=-21.7),
        courbe="acc"),
    cle(26, "la hanche gauche tire, les épaules suivent, le poing passe sur le côté",
        -18, -5, 5, 85,
        dict(GARDE_N, armF=93, armF_p=-65, armF_r=-60, foreF=75, epauleF_av=-1, epauleF_haut=2),
        dict(thighF=19.6, thighF_p=-15, thighF_r=9, shinF=38.8, footF=16.4,
             thighN=-21.9, thighN_p=20.6, thighN_r=-2, shinN=12.4, footN=-17.8),
        courbe="acc"),
    cle(28, "contact du crochet : coude à hauteur d'épaule, poing sur le côté du menton adverse",
        -30, -25, 4, 85,
        dict(GARDE_N, armF=96, armF_p=-85, armF_r=-74, foreF=48, epauleF_av=-1, epauleF_haut=2),
        dict(thighF=17.9, thighF_p=-17.5, thighF_r=13, shinF=40.2, footF=13.3,
             thighN=-22.1, thighN_p=24.5, thighN_r=-2, shinN=3.5, footN=-17.3),
        courbe="dec"),
    cle(31, "le corps finit sa rotation, le bras reste",
        -31, -27, 3.8, 85,
        dict(GARDE_N, armF=96, armF_p=-85, armF_r=-76, foreF=48, epauleF_av=-1, epauleF_haut=1),
        dict(thighF=17.6, thighF_p=-17.8, thighF_r=13.5, shinF=40.2, footF=13,
             thighN=-21.9, thighN_p=24.8, thighN_r=-2, shinN=3.1, footN=-17),
        courbe="acc-dec"),
    cle(35, "le bras gauche revient par le même arc, le coude se replie",
        -26, -20, 3.3, 85.3,
        dict(GARDE_N, armF=70, armF_p=-60, armF_r=-30, foreF=95, epauleF_av=-1, epauleF_haut=1),
        dict(thighF=16.9, thighF_p=-16.9, thighF_r=12, shinF=36, footF=14.2,
             thighN=-21.8, thighN_p=22.7, thighN_r=-2, shinN=6.6, footN=-16.1)),
    cle(40, "poing gauche revenu à la clavicule, le corps se détord",
        -18, -8, 2.5, 86,
        dict(GARDE_N, armF=32, armF_p=-17.5, armF_r=-9.7, foreF=96.9, epauleF_av=-1, epauleF_haut=1),
        dict(thighF=18.4, thighF_p=-16.1, thighF_r=10, shinF=34.5, footF=10.1,
             thighN=-21.8, thighN_p=19, thighN_r=-2, shinN=10.9, footN=-16.8)),
    {"f": 48, "nom": "garde", "fixe": dict(CLES_GD[39]["fixe"], torsionBassin=-12, torsion=-4, neck_r=0,
                                         **GARDE_N, armF=32, armF_p=-17.5, armF_r=-9.7, foreF=96.9,
                                         epauleF_av=-1, epauleF_haut=1)},
]


def main():
    cles = [c for c in GD["cles"] if c["f"] <= 17] + CROCHET
    anim = {"nom": "gauche_droite_crochet_bagarreur", "boucle": False, "longueur": 48,
            "base": GD["base"], "suivante": GD["suivante"], "pieds_auto": False,
            "note": "Un-deux-trois du bagarreur : gauche-droite (images 0-17 du gauche-droite) puis "
                    "crochet du gauche au visage, coude à hauteur d'épaule, la hanche gauche tire, "
                    "le pied avant reste planté. Analyse : analyses/gauche_droite_crochet_bagarreur.md.",
            "cles": cles}
    out = os.path.join(RACINE, "anims", "gauche_droite_crochet_bagarreur.json")
    with open(out, "w") as fh:
        json.dump(anim, fh, ensure_ascii=False, indent=1)
    print(out)


if __name__ == "__main__":
    main()
