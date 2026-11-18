#!/usr/bin/env python3
"""Mannequin 3D de référence (MakeHuman / MPFB, CC0) posé d'après le rig du stickman.

  tools/mannequin.sh poses/x.json -o mannequin.png [--sans-stick]

(mannequin.sh exporte la pose avec tools/pose3d.gd puis appelle ce script ;
une vue par lacet ajouté, comme anim.sh --vues : +90, +45, +0.) Chaque os du mannequin est
tourné pour suivre l'os correspondant du stickman : tronc, bassin et tête prennent le
repère complet de l'os (torsion comprise), bras et jambes prennent la direction des
segments et le plan de flexion du coude / genou. Le maillage suit par skinning
linéaire (poids MakeHuman). Rendu orthographique, une colonne par vue, stickman en
transparence par-dessus.
"""
import argparse, json, os
import numpy as np

ICI = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ICI, "..", "mannequin")

# Repère du mannequin (Blender, z en haut, -y devant, +x = gauche du personnage)
# vers le repère du stickman (x devant, y en haut, z négatif = côté caméra = côté N).
# Le côté N (proche) est porté par les os « _r », le côté F par les « _l ».
M2W = np.array([[0, -1, 0], [0, 0, 1], [1, 0, 0]], float)


def charger_mannequin():
    d = json.load(open(os.path.join(DATA, "humain.json")))
    rig = {b: {"parent": o["parent"], "head": {"default_position": o["tete"]},
               "tail": {"default_position": o["queue"]}} for b, o in d["os"].items()}
    return np.array(d["sommets"], float), d["faces"], rig, d["poids"]


def unit(v):
    n = np.linalg.norm(v)
    return v / n if n > 1e-9 else v


def repere_os(d, n):
    """Repère orthonormé : x le long de l'os, y la normale du plan de flexion."""
    x = unit(d)
    y = unit(n - x * np.dot(n, x))
    return np.stack([x, y, np.cross(x, y)], 1)


def poser(V, F, rig, W, vue, echelle):
    P = {k: np.array(v, float) for k, v in vue["points"].items()}
    Bs = {k: np.array(v, float) for k, v in vue["bases"].items()}  # lignes = x, y, z
    tete = {b: M2W @ np.array(rig[b]["head"]["default_position"]) for b in rig}
    queue = {b: M2W @ np.array(rig[b]["tail"]["default_position"]) for b in rig}
    R = {}
    # Tronc : repère complet (haut = B.x, devant = -B.y, gauche = B.z).
    repos = np.stack([[0, 1, 0], [1, 0, 0], [0, 0, 1]], 1).astype(float)
    def tronc(nom):
        b = Bs[nom]
        return np.stack([b[0], -b[1], b[2]], 1) @ repos.T
    R["Root"] = R["pelvis"] = tronc("root")
    R["spine_01"] = tronc("spineLow")
    R["spine_03"] = R["clavicle_l"] = R["clavicle_r"] = tronc("chest")
    from scipy.spatial.transform import Rotation, Slerp
    s = Slerp([0, 1], Rotation.from_matrix([R["spine_01"], R["spine_03"]]))
    R["spine_02"] = s(0.5).as_matrix()
    R["neck_01"] = R["head"] = tronc("neck")
    # Membres : direction des segments + plan de flexion.
    membres = [("upperarm", "lowerarm", "shoulder", "elbow", "hand", "arm"),
               ("thigh", "calf", "hip", "knee", "ankle", "thigh")]
    for cote_m, cote_s in (("r", "N"), ("l", "F")):
        for haut, bas, a, b, c, os_s in membres:
            hn, bn = f"{haut}_{cote_m}", f"{bas}_{cote_m}"
            d0h, d0b = queue[hn] - tete[hn], queue[bn] - tete[bn]
            n0 = np.cross(d0h, d0b)
            pa = P[a + cote_s] if a + cote_s in P else P[a]
            dh, db = P[b + cote_s] - pa, P[c + cote_s] - P[b + cote_s]
            n = np.cross(dh, db)
            if np.linalg.norm(n) < 0.05 * np.linalg.norm(dh) * np.linalg.norm(db):
                # Membre presque tendu : la normale du plan de flexion du rig.
                bz = Bs[os_s + cote_s][2]
                n = bz if np.dot(bz, np.cross(dh, Bs[os_s + cote_s][1])) >= 0 else -bz
            R[hn] = repere_os(dh, n) @ repere_os(d0h, n0).T
            R[bn] = repere_os(db, n) @ repere_os(d0b, n0).T
            if haut == "upperarm":
                R[f"hand_{cote_m}"] = R[bn]
        # Pied : cheville -> orteils, le plan du tibia garde la rotation.
        fn = f"foot_{cote_m}"
        # Le pied du stickman posé à plat a ses orteils à hauteur de cheville ; celui du
        # mannequin descend de ~17° vers la plante. On prend donc la direction à plat
        # (projetée à l'horizontale) comme repos, sinon chaque pied pique de 17° de trop.
        d0 = queue[f"ball_{cote_m}"] - tete[fn]
        d0[1] = 0.0
        d = P["toe" + cote_s] - P["ankle" + cote_s]
        R[fn] = _pied(R[f"calf_{cote_m}"], d0, d)
    # Os non pilotés : rotation du parent.
    def rot(b):
        while b not in R:
            b = rig[b]["parent"]
        return R[b]
    # Position des têtes d'os : chaîne depuis le bassin.
    pos = {}
    hanches = (tete["thigh_l"] + tete["thigh_r"]) / 2
    def tete_posee(b):
        if b in pos:
            return pos[b]
        par = rig[b].get("parent")
        if not par:
            pos[b] = P["hip"] + echelle * (tete[b] - hanches)
        else:
            pos[b] = tete_posee(par) + echelle * rot(par) @ (tete[b] - tete[par])
        return pos[b]
    Vw = (M2W @ V.T).T
    out = np.zeros_like(Vw)
    tot = np.zeros(len(Vw))
    for b, lst in W.items():
        if b not in rig or not lst:
            continue
        idx = np.array([i for i, _ in lst], int)
        w = np.array([x for _, x in lst])
        Rb = rot(b)
        out[idx] += w[:, None] * ((Rb @ (echelle * (Vw[idx] - tete[b])).T).T + tete_posee(b))
        tot[idx] += w
    ok = tot > 1e-6
    out[ok] /= tot[ok, None]
    return out, pos


def _pied(Rcalf, d0, d):
    """Pied : aligne cheville->orteils en gardant l'axe latéral du tibia."""
    lat_repos = np.array([0, 0, 1.0])
    lat = Rcalf @ lat_repos
    return repere_os(d, np.cross(lat, d) * -1) @ repere_os(d0, np.cross(lat_repos, d0) * -1).T


def dessiner(ax, Vp, F, vue, pos, stick=True):
    from matplotlib.collections import PolyCollection
    f = vue["facing"]
    X = Vp[:, 0] * f
    Y = Vp[:, 1]
    Z = Vp[:, 2]
    tris = []
    for q in F:
        tris.append(q)
    polys = [np.stack([X[q], Y[q]], 1) for q in tris]
    zf = np.array([Z[q].mean() for q in tris])
    nrm = []
    for q in tris:
        a, b, c = Vp[q[0]], Vp[q[1]], Vp[q[2]]
        nrm.append(unit(np.cross(b - a, c - a)))
    nrm = np.array(nrm)
    lum = unit(np.array([0.4 * f, 0.6, -0.7]))
    l = 0.35 + 0.6 * np.abs(nrm @ lum)
    ordre = np.argsort(-zf)  # le plus loin d'abord
    cols = np.stack([l * 0.93, l * 0.82, l * 0.72, np.ones_like(l)], 1)
    pc = PolyCollection([polys[i] for i in ordre], facecolors=cols[ordre], edgecolors=cols[ordre], linewidths=0.3)
    ax.add_collection(pc)
    if stick:
        P = {k: np.array(v) for k, v in vue["points"].items()}
        # Le stickman part d'un seul point pour les bras et pour les jambes ; on recale
        # chaque membre sur l'épaule / la hanche du mannequin pour comparer les angles.
        for cote, m in (("N", "r"), ("F", "l")):
            for racine, os_m, chaine in (("shoulder" + cote, "upperarm_" + m, ("elbow", "hand")),
                                         ("hip", "thigh_" + m, ("knee", "ankle", "toe"))):
                dec = pos[os_m] - P[racine]
                P[racine + "@" + cote] = P[racine] + dec
                for j in chaine:
                    P[j + cote] = P[j + cote] + dec
        segs = [("hip", "waist"), ("waist", "shoulder"), ("shoulder", "neckTop"),
                ("shoulderN@N", "elbowN"), ("elbowN", "handN"), ("shoulderF@F", "elbowF"), ("elbowF", "handF"),
                ("hip@N", "kneeN"), ("kneeN", "ankleN"), ("ankleN", "toeN"),
                ("hip@F", "kneeF"), ("kneeF", "ankleF"), ("ankleF", "toeF")]
        for a, b in segs:
            c = "#c92a2a" if b.endswith("N") else ("#1971c2" if b.endswith("F") else "#222")
            ax.plot([P[a][0] * f, P[b][0] * f], [P[a][1], P[b][1]], color=c, lw=3, alpha=0.75, solid_capstyle="round")
        h = P["head"]
        ax.add_patch(__import__("matplotlib").patches.Circle((h[0] * f, h[1]), vue["head_r"], fill=False, ec="#222", lw=2, alpha=0.6))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pose3d")
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--sans-stick", action="store_true")
    ap.add_argument("--cadre", help="zoom x0,x1,y0,y1 (ex. -60,60,-90,-40 pour les pieds)")
    a = ap.parse_args()
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    data = json.load(open(a.pose3d))
    V, F, rig, W = charger_mannequin()
    st = data["vues"][0]["style"]
    jambe_m = np.linalg.norm(np.array(rig["thigh_l"]["tail"]["default_position"]) - rig["thigh_l"]["head"]["default_position"]) \
        + np.linalg.norm(np.array(rig["calf_l"]["tail"]["default_position"]) - rig["calf_l"]["head"]["default_position"])
    echelle = (st["thigh"] + st["shin"]) / jambe_m
    noms = {90.0: "ligne « face » (lacet +90)", 45.0: "ligne « trois quarts » (+45)", 0.0: "ligne « profil » (+0)"}
    vues = data["vues"]
    fig, axs = plt.subplots(1, len(vues), figsize=(4.2 * len(vues), 6.5), dpi=110)
    axs = np.atleast_1d(axs)
    for ax, vue in zip(axs, vues):
        Vp, pos = poser(V, F, rig, W, vue, echelle)
        dessiner(ax, Vp, F, vue, pos, stick=not a.sans_stick)
        ax.set_aspect("equal")
        x0, x1, y0, y1 = [float(c) for c in a.cadre.split(",")] if a.cadre else (-75, 75, -95, 100)
        ax.set_xlim(x0, x1)
        ax.set_ylim(y0, y1)
        ax.axhline(-84, color="#999", lw=1)
        ax.set_title(f"{data['pose']}\n{noms.get(float(vue['lacet']), vue['lacet'])}", fontsize=9)
        ax.axis("off")
    fig.text(0.5, 0.02, "rouge : côté proche (N)   bleu : côté loin (F)   membres du stickman recalés sur les épaules et hanches du mannequin", ha="center", fontsize=8, color="#555")
    plt.tight_layout()
    plt.savefig(a.out)


if __name__ == "__main__":
    main()
