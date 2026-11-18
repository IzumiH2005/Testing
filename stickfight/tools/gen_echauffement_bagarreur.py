#!/usr/bin/env python3
"""Génère anims/echauffement_bagarreur.json (voir analyses/echauffement_bagarreur.md).

Garde → épaules et bras lâchés → trois rebonds sur l'avant des pieds, bras secoués →
poings cognés deux fois → deux jabs à vide → garde exacte (suivie de l'idle).

    GODOT=… python3 tools/gen_echauffement_bagarreur.py

Les pieds des rebonds sont corrigés image clé par image clé : le script relit les
pointes (anim.sh --print) et ajuste footN / footF et l'avancée de la cheville arrière
jusqu'à ce que chaque pointe soit à sa place de garde (± 0,3).
Les poings cognés sont placés en 3D (resout_mains, buste au lacet 0) ; le poing du jab
est mis sur la ligne de garde en cherchant le plan du bras (sonde 3D).
"""
import json
import math
import os
import re
import subprocess
import tempfile

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.join(ICI, "..")
NOM = "echauffement_bagarreur"
SORTIE = os.path.join(RACINE, "anims", NOM + ".json")
GARDE = json.load(open(os.path.join(RACINE, "poses", "garde_ouverte_bagarreur.json")))
G = GARDE["angles"]
GY = GARDE.get("y", 87.0)

BRAS_G = {k: G[k] for k in ("armN", "foreN", "armN_r", "armN_p", "armF", "foreF", "armF_r", "armF_p")}
HAUT_G = {k: G.get(k, 0.0) for k in ("torsion", "torsionBassin", "chest", "neck", "neck_r",
                                     "epauleN_av", "epauleF_av", "epauleN_haut", "epauleF_haut")}


def godot():
    return os.environ.get("GODOT", "godot")


def lance(args):
    r = subprocess.run(args, cwd=RACINE, capture_output=True, text=True, env=dict(os.environ, GODOT=godot()))
    return r.stdout + r.stderr


def cle(f, haut=None, bras=None, x=0.0, y=GY, courbe=None, nom=None, **extra):
    fixe = {"x": round(x, 2), "y": round(y, 2)}
    h = dict(HAUT_G)
    h.update(haut or {})
    b = dict(BRAS_G)
    b.update(bras or {})
    fixe.update({k: round(v, 2) for k, v in h.items()})
    fixe.update({k: round(v, 2) for k, v in b.items()})
    c = {"f": f, "fixe": fixe}
    if nom:
        c["nom"] = nom
    if courbe:
        c["courbe"] = courbe
    c.update(extra)
    return c


# ---------- Phase 1 : il lâche ----------
LACHE = {"chest": 3, "neck": 5, "epauleF_haut": -3, "epauleN_av": 0, "epauleF_av": -1}


def ballants(foreN=23, foreF=23, elN=5, elF=5, pN=12, pF=-12):
    return {"armN": elN, "foreN": foreN, "armN_p": pN, "armN_r": 0,
            "armF": elF, "foreF": foreF, "armF_p": pF, "armF_r": 0}


# ---------- Phase 2 : rebonds ----------
MONTEE = 80.0   # bras à mi-chemin, image 80
BRAS80 = {"armN": 18, "armN_p": 24, "armN_r": 10, "foreN": 90,
          "armF": 14, "armF_p": -20, "armF_r": 8, "foreF": 80}


# Repères de profil à l'image 0 (anim.sh --print de la garde)
HANCHE_X = 0.0
POINTE = {"F": (26.8, 8.7), "N": (-33.9, 8.0)}
CHEV = {"F": (20.1, 8.6), "N": (-36.5, 15.1)}


def _pied(s):
    dx, dy = CHEV[s][0] - POINTE[s][0], CHEV[s][1] - POINTE[s][1]
    return math.hypot(dx, dy), math.atan2(dy, dx)


def _dist_hanche(y, ch):
    return math.hypot(ch[0] - HANCHE_X, y - ch[1])


def chevilles(y, h):
    """Chevilles visées sur le cercle de leur pointe ; rend {côté: (cheville, Δangle°)}."""
    out = {}
    # pied avant : talon levé de e
    L, b0 = _pied("F")
    e = 1.0 + 2.0 * h
    cy = CHEV["F"][1] + e
    cx = POINTE["F"][0] - math.sqrt(L * L - (cy - POINTE["F"][1]) ** 2)
    b = math.atan2(cy - POINTE["F"][1], cx - POINTE["F"][0])
    out["F"] = ((cx, cy), (math.degrees(b0 - b) + 180) % 360 - 180)
    # pied arrière : se redresse juste assez pour que hanche–cheville = garde − 0,3
    L, b0 = _pied("N")
    Dg = _dist_hanche(GY, CHEV["N"])
    cible = Dg - 0.3

    def ch(beta):
        return (POINTE["N"][0] + L * math.cos(beta), POINTE["N"][1] + L * math.sin(beta))
    beta = b0
    if _dist_hanche(y, ch(b0)) > cible:
        lo, hi = math.radians(60), b0   # dist croît avec beta sur cet intervalle
        for _ in range(50):
            m = (lo + hi) / 2
            if _dist_hanche(y, ch(m)) > cible:
                hi = m
            else:
                lo = m
        beta = lo
    out["N"] = (ch(beta), math.degrees(b0 - beta))
    return out


VOL = 0.4      # part du cycle en l'air
HAUT_VOL = 7.0 # hauteur du saut (px) : les pieds quittent le sol
DERNIER = 60   # le dernier saut part de là et retombe en garde (image 68)

# Appui détendu pendant les sauts : pieds rapprochés sous le bassin, sur l'avant du pied.
POINTE_R = {"F": (13.0, POINTE["F"][1]), "N": (-17.0, POINTE["N"][1])}


def _lisse(w):
    w = min(1.0, max(0.0, w))
    return w * w * (3 - 2 * w)


def detente(f):
    """0 = appui de garde, 1 = appui détendu. Change pendant le vol du premier et du dernier saut."""
    if f <= 20:
        return 0.0
    if f <= 20 + 20 * VOL:
        return _lisse((f - 20) / (20 * VOL))
    if f <= DERNIER:
        return 1.0
    return 1.0 - _lisse((f - DERNIER) / (20 * VOL))


def phase(f):
    """Rend (z en l'air, d enfoncement de l'amorti 0..1, a amplitude)."""
    u = ((f - 20) % 20) / 20.0
    if f > DERNIER + 20 * VOL:          # retombé en garde : un amorti puis il se pose
        a = max(0.0, 1.0 - (f - DERNIER - 20 * VOL) / 12.0)
        return 0.0, math.sin(math.pi * min(1.0, (f - DERNIER - 20 * VOL) / 10.0)), a
    if u < VOL:
        return HAUT_VOL * math.sin(math.pi * u / VOL), 0.0, 1.0
    return 0.0, math.sin(math.pi * (u - VOL) / (1 - VOL)), 1.0


def chevilles_detendues(h):
    out = {}
    L, b0 = _pied("F")
    TF = POINTE_R["F"]
    cy = TF[1] + (CHEV["F"][1] - POINTE["F"][1]) + 1.0 + 2.0 * h
    cx = TF[0] - math.sqrt(L * L - (cy - TF[1]) ** 2)
    b = math.atan2(cy - TF[1], cx - TF[0])
    out["F"] = ((cx, cy), (math.degrees(b0 - b) + 180) % 360 - 180)
    L, b0 = _pied("N")
    TN = POINTE_R["N"]
    beta = math.radians(152 - 14 * h)          # talon arrière un peu levé, plus à l'impulsion
    out["N"] = ((TN[0] + L * math.cos(beta), TN[1] + L * math.sin(beta)), math.degrees(b0 - beta))
    return out


def haut_detendu(ch):
    """Bassin à l'impulsion : jambes presque tendues (hanche–cheville = garde − 0,4)."""
    y = 1e9
    for s in "FN":
        D = _dist_hanche(GY, CHEV[s]) - 0.4
        dx = ch[s][0][0] - HANCHE_X
        y = min(y, ch[s][0][1] + math.sqrt(D * D - dx * dx))
    return y


def appui(f):
    """Rend (bassin sans le saut, z, chevilles {côté: (pos, Δangle)}, pointes visées en écart à la garde)."""
    z, d, a = phase(f)
    w = detente(f)
    h = 1.0 - d
    yg = 88.0 - 2.0 * d
    yg = 87.0 + (yg - 87.0) * a
    hg = 0.5 + ((yg - 86.0) / 2.0 - 0.5)
    chg = chevilles(yg, hg)
    chr_ = chevilles_detendues(h)
    yr = haut_detendu(chevilles_detendues(1.0)) - 2.5 * d
    y = (1 - w) * yg + w * yr
    ch, off = {}, {}
    for s in "FN":
        (gx, gy), ga = chg[s]
        (rx, ry), ra = chr_[s]
        ch[s] = (((1 - w) * gx + w * rx, (1 - w) * gy + w * ry), (1 - w) * ga + w * ra)
        off[s] = (w * (POINTE_R[s][0] - POINTE[s][0]), z)
    return y, z, ch, off, w, d, a


def rebond(f):
    u = ((f - 20) % 20) / 20.0
    y, z, ch, off, w, d, a = appui(f)
    amp = a if f > DERNIER else 1.0
    phib = 2 * math.pi * u - 2 * math.pi * 3 / 20.0
    s = math.sin(phib) * amp
    # bras ballants : à peine pliés, ils flottent avec le corps (l'avant-bras tombe à la réception)
    fl = 8 * math.sin(math.pi * ((u - 0.5) % 1.0)) * amp
    bras = ballants(10 + fl + 3 * s, 10 + fl - 3 * s, 6 + 2 * s, 6 - 2 * s, 15 + 9 * s, -15 + 9 * s)
    bras = {k: w * bras[k] + (1 - w) * ballants()[k] for k in bras}
    droit = dict(LACHE, chest=0.5, epauleN_haut=-2.5 + 1.5 * s, epauleF_haut=-2.5 - 1.5 * s,
                 epauleF_av=0, neck=2.5 + 2.5 * math.cos(2 * math.pi * (u - 0.75)))
    haut = {k: w * droit[k] + (1 - w) * LACHE.get(k, HAUT_G.get(k, 0.0)) for k in droit}
    if f > DERNIER + 20 * VOL:
        g = _lisse((f - DERNIER - 20 * VOL) / 12.0)
        bras = {k: (1 - g) * bras[k] + g * BRAS80[k] for k in bras}
        haut["epauleN_haut"] = (1 - g) * haut["epauleN_haut"] - 3 * g
        haut["epauleF_haut"] = (1 - g) * haut["epauleF_haut"] - 2 * g
        haut["chest"] = (1 - g) * haut["chest"] + g * LACHE["chest"]
    return y, z, ch, off, bras, haut


def cles_rebonds():
    out = []
    for f in range(20, 81):
        y, z, ch, off, bras, haut = rebond(f)
        u = ((f - 20) % 20) / 20.0
        nom = None
        if f <= DERNIER and u == 0:
            nom = "impulsion"
        elif f <= DERNIER and abs(u - VOL / 2) < 1e-9:
            nom = "haut du saut"
        elif abs(u - VOL) < 1e-9:
            nom = "réception" if f < DERNIER else "réception en garde"
        c = cle(f, haut, bras, y=y + z, courbe="lin", nom=nom)
        c["vise_rel"] = {"leg" + s: [round(ch[s][0][0] - CHEV[s][0], 3),
                                     round(ch[s][0][1] + z - CHEV[s][1], 3)] for s in "FN"}
        for s in "FN":
            c["fixe"]["foot" + s] = round(G["foot" + s] - ch[s][1], 2)
        c["_off"] = off
        out.append(c)
    return out


def ecart_pointe(f, s):
    if 20 <= f <= 80:
        return appui(f)[3][s]
    return (0.0, 0.0)


# ---------- Phase 3 : poings cognés ----------
CARRE = {"torsion": 4, "neck": 4, "neck_r": -4.8, "epauleN_av": 0, "epauleF_av": 0,
         "epauleN_haut": -3, "epauleF_haut": 1}


def mains(N, F):
    return {"N": N, "F": F, "coude_dy": [-4, -4], "ecart": [30, 45]}


def resout_chocs():
    """Résout les poings cognés au lacet 0 et rend {image: angles des bras}."""
    cibles = {88: ([42, -12, -14.5], [42, -12, 14.5]), 90: ([42, -12, -8.5], [42, -12, 8.5]),
              95: ([42, -11, -13.5], [42, -11, 13.5])}
    cl = []
    for f, (n, fa) in sorted(cibles.items()):
        h = dict(CARRE, torsion=2, neck_r=-3.6) if f == 88 else CARRE
        c = cle(f, dict(h, lacet=0))
        for k in BRAS_G:
            c["fixe"].pop(k)
        c["mains3d"] = mains(n, fa)
        cl.append(c)
    a = {"nom": "_tmp_chocs", "boucle": False, "longueur": 96, "base": "garde_ouverte_bagarreur",
         "pieds_auto": False, "cles": cl}
    chemin = os.path.join(RACINE, "anims", "_tmp_chocs.json")
    json.dump(a, open(chemin, "w"), indent=1)
    print(lance(["tools/resout_mains.sh", chemin]).strip().splitlines()[-6:])
    res = json.load(open(chemin))
    os.remove(chemin)
    return {c["f"]: {k: c["fixe"][k] for k in BRAS_G if k in c["fixe"]} for c in res["cles"]}


# ---------- Phase 4 : jab ----------
JAB_HAUT = {"torsionBassin": -12, "torsion": -20, "neck_r": 9.6, "epauleF_haut": 3,
            "epauleN_av": -1, "epauleF_av": 0}
JAB_BRAS = {"armF": 90, "foreF": 18.5, "armF_r": 15}


def sonde(pose):
    """Positions 3D au lacet 0 (x, y, z) des articulations d'une pose."""
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, dir=RACINE) as t:
        json.dump(pose, t)
    gd = os.path.join(RACINE, "tools", "_sonde_ech.gd")
    open(gd, "w").write('''extends SceneTree
func _initialize() -> void:
	var p: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(OS.get_cmdline_user_args()[0]))
	p.angles.lacet = 0.0
	var sol := StickRig.solve(p)
	for k in sol.joints:
		print("J %s %f %f %f" % [k, sol.joints[k].x, sol.joints[k].y, float(sol.prof.get(k, 0.0))])
	quit()
''')
    out = lance([godot(), "--path", ".", "--headless", "-s", "res://tools/_sonde_ech.gd", "--", t.name])
    os.remove(t.name)
    os.remove(gd)
    J = {}
    for m in re.finditer(r"^J (\w+) (\S+) (\S+) (\S+)$", out, re.M):
        J[m.group(1)] = tuple(float(v) for v in m.groups()[1:])
    return J


def plan_du_jab():
    g = sonde(GARDE)
    zg = g["handF"][2] - g["shoulderN"][2]
    meilleur = None
    for p in range(-50, -14, 2):
        pose = json.loads(json.dumps(GARDE))
        pose["angles"].update(JAB_HAUT)
        pose["angles"].update(JAB_BRAS)
        pose["angles"]["armF_p"] = p
        j = sonde(pose)
        z = j["handF"][2] - j["shoulderN"][2]
        if meilleur is None or abs(z - zg) < meilleur[1]:
            meilleur = (p, abs(z - zg), z)
    print("jab : plan %d, z %.1f (garde %.1f)" % (meilleur[0], meilleur[2], zg))
    return meilleur[0]


# ---------- Correction des pieds ----------
RE_J = re.compile(r"(\w+)\((-?[\d.]+),(-?[\d.]+)\)")


def articulations(anim):
    chemin = os.path.join(RACINE, "anims", NOM + ".json")
    json.dump(anim, open(chemin, "w"), indent=1, ensure_ascii=False)
    out = lance(["tools/anim.sh", chemin, "--print"])
    res = {}
    for ligne in out.splitlines():
        m = re.match(r"\s*(\d+) " + NOM + "@", ligne)
        if m:
            res[int(m.group(1))] = {k: (float(a), float(b)) for k, a, b in RE_J.findall(ligne)}
    return res


def corrige_pieds(anim, passes=8):
    J = articulations(anim)
    ref = {s: J[0]["toe" + s] for s in "NF"}
    for n in range(passes):
        pire = 0.0
        for c in anim["cles"]:
            if "vise_rel" not in c:
                continue
            j = J[c["f"]]
            for s, gain in (("F", 0.17), ("N", 0.10)):
                o = c.get("_off", {}).get(s, (0.0, 0.0))
                ex = j["toe" + s][0] - ref[s][0] - o[0]
                ey = j["toe" + s][1] - ref[s][1] - o[1]
                pire = max(pire, abs(ex), abs(ey))
                c["fixe"]["foot" + s] = round(c["fixe"]["foot" + s] - ey / gain, 2)
                v = c["vise_rel"]["leg" + s]
                v[0] = round(v[0] - ex, 3)
        print("pieds, passe %d : écart max %.2f" % (n, pire))
        J = articulations(anim)
    return J, ref


def main():
    chocs = resout_chocs()
    pj = plan_du_jab()
    jab = dict(JAB_BRAS, armF_p=pj)
    cl = [
        cle(0, nom="garde", courbe="acc"),
        cle(6, LACHE, y=86.6, courbe="acc", nom="les épaules lâchent, il expire"),
        cle(14, LACHE, ballants(), y=86.4, courbe="dec", nom="bras tombés, ballants"),
    ]
    cl += [cle(20, dict(LACHE, epauleF_haut=-2, epauleN_haut=-3), BRAS80, y=86.7, courbe="acc-dec",
               nom="les bras remontent")]
    cl += [
        cle(26, courbe="acc", nom="garde reprise"),
        cle(28, dict(CARRE, torsion=2, neck_r=-3.6), dict(chocs[88]), courbe="acc",
            nom="les poings se rapprochent"),
        cle(30, CARRE, dict(chocs[90]), courbe="palier", nom="premier choc"),
        cle(32, CARRE, dict(chocs[90]), courbe="dec"),
        cle(35, CARRE, dict(chocs[95]), courbe="acc", nom="les poings s'écartent"),
        cle(37, CARRE, dict(chocs[90]), courbe="palier", nom="second choc"),
        cle(39, CARRE, dict(chocs[90]), courbe="dec"),
        cle(46, courbe="dec", nom="garde"),
        cle(49, JAB_HAUT, jab, x=1.2, y=86.6, courbe="palier", nom="premier jab"),
        cle(51, JAB_HAUT, jab, x=1.2, y=86.6, courbe="acc-dec"),
        cle(57, courbe="dec", nom="garde"),
        cle(60, JAB_HAUT, jab, x=1.2, y=86.6, courbe="palier", nom="second jab"),
        cle(62, JAB_HAUT, jab, x=1.2, y=86.6, courbe="acc-dec"),
        cle(68, courbe="acc-dec", nom="garde"),
        cle(76, {"epauleN_haut": -1, "epauleF_haut": 3.5, "chest": 6}, courbe="acc-dec", nom="inspiration"),
        cle(86, {"neck": 12}, y=86.2, courbe="dec", nom="hochement : prêt"),
        cle(94, nom="garde"),
        cle(100, nom="garde tenue"),
    ]
    anim = {"nom": NOM, "boucle": False, "longueur": 100, "base": "garde_ouverte_bagarreur",
            "suivante": "garde_ouverte_idle_bagarreur", "pieds_auto": False,
            "decalage": {"neck": 3}, "cles": cl}
    J, ref = corrige_pieds(anim)
    pire = max(max(abs(J[f]["toe" + s][i] - ref[s][i]) for s in "NF" for i in (0, 1)) for f in J)
    print("pointes, toute l'animation : écart max %.2f" % pire)
    for c in anim["cles"]:
        c.pop("_off", None)
    json.dump(anim, open(SORTIE, "w"), indent=1, ensure_ascii=False)
    print("écrit", SORTIE)


if __name__ == "__main__":
    main()
