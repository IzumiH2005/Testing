#!/usr/bin/env python3
"""Génère anims/coup_de_pied_retourne.json (fiche : analyses/coup_de_pied_retourne.md).

Coup de pied retourné du bagarreur depuis sa garde ouverte : demi-tour sur le pied F planté
(lacet 45 -> 180), armé du genou N, frappe du talon N vers +x à lacet ~186, puis le tour se
termine (lacet -> 405 ≡ 45) et le pied N se repose à sa place de garde.
Chaque clé est écrite en entier (état complet), à partir de la garde.
"""
import json
import os

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)

GARDE = json.load(open(os.path.join(RACINE, "poses", "garde_ouverte_bagarreur.json")))
G = dict(GARDE["angles"], x=GARDE["x"], y=GARDE["y"])

PIED_F = [21.8, 8.5]       # cheville F : plantée toute l'animation
PIED_N = [-29.5, 13.5]     # cheville N en garde

# bras serrés au visage pendant le tour
BRAS_TOUR = dict(epauleN_av=-1, epauleF_av=-1)  # bras de la garde, omoplates tenues


def etat(**k):
    e = dict(G)
    e.update(k)
    return e


# (image, nom, état, cheville N (None = laissée à l'IK des angles), courbe)
CLES = [
    (0, "garde", etat(), PIED_N, "acc"),
    (6, "transfert sur le pied avant, la tête part",
     etat(lacet=60, x=12, y=81, root=4, torsion=-15, neck_r=-25, **BRAS_TOUR,
          thighN_p=5, thighF_p=-5), PIED_N, "acc"),
    (15, "demi-tour, la tête cherche la cible, genou N armé",
     etat(lacet=165, x=18, y=82, root=12, torsion=-20, torsionBassin=0, neck=5, neck_r=40,
          **BRAS_TOUR, thighN=90, shinN=125, footN=20, thighN_p=0, thighF_p=0,
          thighN_r=0, thighF_r=0), None, "lin"),
    (19, "armé : talon devant la fesse, dos à la cible",
     etat(lacet=180, x=18, y=82, root=25, torsion=-10, torsionBassin=0, neck=0, neck_r=40,
          **BRAS_TOUR, thighN=100, shinN=130, footN=20, thighN_p=0, thighF_p=0,
          thighN_r=0, thighF_r=0), None, "acc"),
    (22, "contact : talon dans la cible",
     etat(lacet=186, x=16, y=80, root=60, torsion=0, torsionBassin=0, neck=-30, neck_r=40,
          **dict(BRAS_TOUR, armF_p=-50), thighN=-22, shinN=5, footN=20,
          thighN_p=0, thighF_p=0, thighN_r=0, thighF_r=0), None, "lin"),
    (26, "tenue",
     etat(lacet=186, x=16, y=80, root=58, torsion=0, torsionBassin=0, neck=-30, neck_r=40,
          **dict(BRAS_TOUR, armF_p=-50), thighN=-20, shinN=10, footN=20,
          thighN_p=0, thighF_p=0, thighN_r=0, thighF_r=0), None, "acc-dec"),
    (32, "rappel : le genou revient, le tour continue",
     etat(lacet=250, x=16, y=82, root=25, torsion=-10, torsionBassin=0, neck=0, neck_r=20,
          **BRAS_TOUR, thighN=80, shinN=125, footN=10, thighN_p=0, thighF_p=0,
          thighN_r=0, thighF_r=0), None, "acc-dec"),
    (40, "fin du tour, pied N reposé",
     etat(lacet=380, x=6, y=82, root=5, torsion=-6, neck_r=0, **BRAS_TOUR), PIED_N, "dec"),
    (54, "garde", etat(lacet=405), PIED_N, "lin"),
]


def r2(v):
    return round(v, 2)


def main():
    cles = []
    for f, nom, e, pn, courbe in CLES:
        c = {"f": f, "nom": nom, "fixe": {k: r2(v) for k, v in e.items()},
             "vise": {"legF": PIED_F}, "courbe": courbe, "ancre": False}
        if pn is not None:
            c["vise"]["legN"] = pn
        cles.append(c)
    anim = {"nom": "coup_de_pied_retourne", "boucle": False, "longueur": 54,
            "base": "garde_ouverte_bagarreur", "suivante": "garde_ouverte_idle_bagarreur",
            "pieds_auto": True,
            "note": "Coup de pied retourné depuis la garde ouverte du bagarreur : tour complet sur "
                    "le pied avant, frappe du talon arrière. Analyse : "
                    "analyses/coup_de_pied_retourne.md.",
            "cles": cles}
    out = os.path.join(RACINE, "anims", "coup_de_pied_retourne.json")
    with open(out, "w") as fh:
        json.dump(anim, fh, ensure_ascii=False, indent=1)
    print(out)


if __name__ == "__main__":
    main()
