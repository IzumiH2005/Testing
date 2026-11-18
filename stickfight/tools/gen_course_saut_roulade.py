#!/usr/bin/env python3
"""Génère anims/course_saut_roulade.json (voir analyses/course_saut_roulade.md).

Course (cycles de anims/sprint.json), appel sur le pied loin, vol en parabole au-dessus
d'un trou avec bras en moulinet et jambes qui pédalent, réception sur une plateforme
plus haute (+45), roulade avant et relevé.

    python3 tools/gen_course_saut_roulade.py
"""
import json
import math
import os

ICI = os.path.dirname(os.path.abspath(__file__))
ANIMS = os.path.join(ICI, "..", "anims")

D = 342.89            # avance d'un cycle de sprint
A = 542.0             # cheville du pied d'appel (F)
BORD0 = A + 15        # fin du sol de course
P = A + 315           # bord de la plateforme
H = 45.0              # hauteur de la plateforme
G = 7.5               # demi-trait : cheville posée à G au-dessus du sol

# Vol : 49 → 100, k = f − 49. Il ne se pose pas sur les pieds : les mains touchent à 100 et il
# plonge directement dans la roulade.
F0, F1 = 49, 100
X0, VX = 591.0, 8.9
GR = 0.13625
Y0, YC = 89.0, 92.0                     # bassin au décollage et quand les mains touchent
VY0 = (YC - Y0) / (F1 - F0) + GR * (F1 - F0)
PIEDS = 1049.0                          # repère de la plateforme (les mains se posent devant)


def r2(v):
    return round(v, 2)


# ---------- cinématique directe 2D (même convention que le rig, profil) ----------
L = dict(spineLow=22, chest=24, arm=34, fore=32, thigh=41, shin=42, foot=10)


def _d(a):
    return math.cos(math.radians(a)), math.sin(math.radians(a))


def fk(a):
    """Points (dx, dy, rayon) relatifs au bassin."""
    rw = 90 - a["root"]
    slw = rw - a.get("spineLow", 0)
    chw = slw - a.get("chest", 0)
    nw = chw - a.get("neck", 0)
    pts = [(0, 0, G)]
    wa = (L["spineLow"] * _d(slw)[0], L["spineLow"] * _d(slw)[1])
    sh = (wa[0] + L["chest"] * _d(chw)[0], wa[1] + L["chest"] * _d(chw)[1])
    hd = (sh[0] + 20.2 * _d(nw)[0], sh[1] + 20.2 * _d(nw)[1])
    pts += [(wa[0], wa[1], G), (sh[0], sh[1], G), (hd[0], hd[1], 23)]
    for s in "NF":
        w = chw + 180 + a.get("arm" + s, 0)
        p = math.cos(math.radians(a.get("arm" + s + "_p", 0)))  # bras sorti sur le côté : plus court de profil
        e = (sh[0] + L["arm"] * p * _d(w)[0], sh[1] + L["arm"] * p * _d(w)[1])
        w2 = w + a.get("fore" + s, 0)
        h = (e[0] + L["fore"] * p * _d(w2)[0], e[1] + L["fore"] * p * _d(w2)[1])
        pts += [(e[0], e[1], G), (h[0], h[1], 8.5)]
        w = rw + 180 + a.get("thigh" + s, 0)
        k = (L["thigh"] * _d(w)[0], L["thigh"] * _d(w)[1])
        w2 = w - a.get("shin" + s, 0)
        an = (k[0] + L["shin"] * _d(w2)[0], k[1] + L["shin"] * _d(w2)[1])
        w3 = w2 + 90 + a.get("foot" + s, 0)
        to = (an[0] + L["foot"] * _d(w3)[0], an[1] + L["foot"] * _d(w3)[1])
        pts += [(k[0], k[1], G), (an[0], an[1], G), (to[0], to[1], G)]
    return pts


def y_contact(a, sol=H, jeu=0.3):
    """Hauteur du bassin pour que le point le plus bas du corps touche le sol."""
    return sol + jeu + max(r - dy for dx, dy, r in fk(a))


# ---------- clés ----------
def cle(f, fixe, vise=None, courbe=None, ancre=None, nom=None, p=None):
    c = {"f": f}
    if nom:
        c["nom"] = nom
    c["fixe"] = {k: (r2(v) if isinstance(v, float) else v) for k, v in fixe.items()}
    if vise:
        c["vise"] = {k: [r2(v[0]), r2(v[1])] for k, v in vise.items()}
    if courbe:
        c["courbe"] = courbe
    if p:
        c["p"] = p
    if ancre is not None:
        c["ancre"] = ancre
    return c


def course(sprint):
    """0-41 : un cycle et demi de sprint ; l'avant-dernier pas s'abaisse un peu."""
    out = []
    for f in range(42):
        k = json.loads(json.dumps(sprint["cles"][f % 28]))
        dx = D * (f // 28)
        k["f"] = f
        k["fixe"]["x"] = r2(k["fixe"]["x"] + dx)
        for leg in k["vise"]:
            k["vise"][leg][0] = r2(k["vise"][leg][0] + dx)
        # avant-dernier appui (N, 28-41) : bassin abaissé jusqu'à 3, pour préparer l'appel
        if f >= 30:
            k["fixe"]["y"] = r2(k["fixe"]["y"] - min(3.0, (f - 29) * 0.5))
        out.append(k)
    # la jambe loin vient se poser un peu plus loin devant (dernier pas long) : A au lieu de 536
    out[41]["vise"]["legF"] = [A - 4, 14.0]
    out[40]["vise"]["legF"] = [r2(out[40]["vise"]["legF"][0] + 3), out[40]["vise"]["legF"][1]]
    return out


TRONC_APPEL = {"spineLow": 8, "chest": 6}


def appel():
    """42-49 : le pied F posé en A, le bassin passe dessus et monte ; le genou N monte."""
    # f : x, y, root, neck, armN, foreN, armF, foreF, cheville F, cuisse/tibia N
    t = [
        (42, A - 28, 79.5, 14, -20, 78, 98, -48, 52, (A, 10.0), None),
        (43, A - 17, 78.5, 12, -18, 60, 95, -36, 55, (A, 9.0), (25, 125)),
        (44, A - 6, 78.0, 10, -16, 35, 90, -18, 60, (A, 8.7), (45, 125)),
        (45, A + 5, 79.0, 8, -14, 0, 80, 6, 60, (A, 8.7), (62, 118)),
        (46, A + 16, 81.5, 7, -13, -25, 70, 34, 52, (A + 0.5, 9.5), (76, 108)),
        (47, A + 27, 84.5, 6, -12, -40, 60, 62, 44, (A + 2, 12.0), (86, 100)),
        (48, A + 38, 87.0, 5, -11, -48, 50, 90, 38, (A + 4.5, 15.5), (92, 95)),
    ]
    out = []
    for f, x, y, root, neck, aN, fN, aF, fF, ankF, legN in t:
        fx = {"x": float(x), "y": y, "root": root, "neck": neck, "armN": aN, "foreN": fN,
              "armF": aF, "foreF": fF, "armN_p": 15, "armF_p": -15}
        fx.update(TRONC_APPEL)
        vise = {"legF": ankF}
        if legN is None:
            vise["legN"] = (A - 47, 64.0)
        else:
            fx["thighN"], fx["shinN"] = legN
        out.append(cle(f, fx, vise, ancre=False, nom="appel : pied loin posé" if f == 42 else None))
    return out


def lisse(u):
    return u * u * (3 - 2 * u)


def bras_p(a, signe):
    """Bras sorti sur le côté dans la moitié arrière du cercle (−30° à −150°)."""
    s = math.sin(math.radians(a))
    w = min(1.0, max(0.0, (-s - 0.2) / 0.3))
    return signe * r2(15 + 35 * lisse(w))


def phase_bras(k, n=F1 - F0):
    """Avancement des moulinets, ralenti au sommet (k ≈ 25) : vitesse 1 − 0,45·bosse."""
    pas = 0.05
    tot = acc = 0.0
    u = 0.0
    while u < n - 1e-9:
        v = 1 - 0.45 * math.exp(-((u + pas / 2 - 25.5) / 7.0) ** 2)
        tot += v * pas
        if u < k - 1e-9:
            acc += v * pas
        u += pas
    return acc / tot


def interp(cles, k):
    """Interpolation par morceaux lissée entre (k, valeur)."""
    for (k0, v0), (k1, v1) in zip(cles, cles[1:]):
        if k0 <= k <= k1:
            u = lisse((k - k0) / (k1 - k0))
            return v0 + (v1 - v0) * u
    return cles[-1][1]


# Jambes en vol (k → cuisse, tibia) : N fait un cycle, F un cycle et demi
JAMBES = {
    "thighN": [(0, 92), (10, 40), (17, -18), (26, 10), (34, 60), (40, 40), (46, -8), (51, -15)],
    "shinN": [(0, 95), (10, 60), (17, 70), (26, 115), (34, 95), (40, 80), (46, 60), (51, 50)],
    "thighF": [(0, -24), (8, 10), (16, 62), (24, 30), (30, -22), (36, 40), (41, 20), (46, -18), (51, -25)],
    "shinF": [(0, 25), (8, 105), (16, 110), (24, 50), (30, 75), (36, 105), (41, 90), (46, 80), (51, 70)],
    "footN": [(0, 0), (40, 0), (51, -30)],
    "footF": [(0, 0), (40, 0), (51, -30)],
}
# Le tronc bascule vers l'avant à la descente : il plonge, la tête passe devant, les mains visent la plateforme
TRONC = {
    "root": [(0, 4), (12, 5), (25, 8), (34, 10), (40, 16), (46, 34), (51, 60)],
    "spineLow": [(0, 8), (25, 6), (44, 10), (51, 14)],
    "chest": [(0, 6), (25, 4), (44, 8), (51, 12)],
    "neck": [(0, -11), (25, -10), (40, -12), (46, 0), (51, 25)],
}
# Moulinets : angles continus décroissants (−360 = un tour)
BRAS = {"armN": (-55.0, -300.0), "armF": (115.0, -290.0)}


def vol():
    out = []
    for f in range(F0 + 1, F1):
        k = f - F0
        fx = {"x": X0 + VX * k, "y": Y0 + VY0 * k - GR * k * k}
        for ch, pts in list(JAMBES.items()) + list(TRONC.items()):
            fx[ch] = interp(pts, k)
        u = phase_bras(k)
        for ch, (a0, a1) in BRAS.items():
            a = a0 + (a1 - a0) * u
            fx[ch] = a
            fx[ch + "_p"] = bras_p(a, 1 if ch == "armN" else -1)
            fx["fore" + ch[3]] = 30 + 12 * math.sin(math.radians(a))
        out.append(cle(f, fx, courbe="lin", ancre=False,
                       nom="sommet" if f == 74 else ("le bord passe sous lui" if f == 77 else None)))
    return out


def decolle():
    """49 : dernière image au sol, pointe du pied F encore posée."""
    fx = {"x": X0, "y": Y0, "root": 4, "spineLow": 8, "chest": 6, "neck": -11,
          "armN": -55, "foreN": 45, "armF": 115, "foreF": 34, "armN_p": bras_p(-55, 1), "armF_p": -15,
          "thighN": 92, "shinN": 95}
    return cle(F0, fx, {"legF": (A + 8, 19.5)}, courbe="lin", ancre=False, nom="décollage")


# Réception et roulade : angles de la roulade, bassin posé par contact (fk)
def norm(a):
    return (a + 180) % 360 - 180


def ik_jambe(a, s, cheville):
    """Cuisse, tibia, pied (à plat) pour que la cheville s soit en `cheville` (relatif au bassin)."""
    rw = 90 - a["root"]
    dx, dy = cheville
    dd = min(math.hypot(dx, dy), L["thigh"] + L["shin"] - 0.5)
    th = math.degrees(math.acos((L["thigh"] ** 2 + L["shin"] ** 2 - dd ** 2) / (2 * L["thigh"] * L["shin"])))
    k = 180 - th
    al = math.degrees(math.acos((L["thigh"] ** 2 + dd ** 2 - L["shin"] ** 2) / (2 * L["thigh"] * dd)))
    phi = math.degrees(math.atan2(dy, dx))
    w = phi + al                       # genou vers l'avant (w2 = w − k)
    t = norm(w - rw - 180)
    w2 = w - k
    return {"thigh" + s: r2(t), "shin" + s: r2(k), "foot" + s: r2(norm(-90 - w2))}


def chevilles(a):
    pts = fk(a)
    return pts[7][:2], pts[12][:2]  # cheville N, cheville F


def ik_bras(a, s, cible):
    """Épaule et coude pour amener la main sur `cible` (relative au bassin), coude plié vers l'arrière."""
    pts = fk(a)
    sh = pts[2][:2]
    p = math.cos(math.radians(a.get("arm" + s + "_p", 0)))
    l1, l2 = L["arm"] * p, L["fore"] * p
    dx, dy = cible[0] - sh[0], cible[1] - sh[1]
    d = min(math.hypot(dx, dy), l1 + l2 - 0.01)
    al = math.degrees(math.acos((l1 * l1 + d * d - l2 * l2) / (2 * l1 * d)))
    inter = math.degrees(math.acos((l1 * l1 + l2 * l2 - d * d) / (2 * l1 * l2)))
    chw = 90 - a["root"] - a.get("spineLow", 0) - a.get("chest", 0)
    w = math.degrees(math.atan2(dy, dx)) - al
    arm = w - chw - 180
    ref = a["arm" + s]
    arm += 360 * round((ref - arm) / 360)
    return {"arm" + s: r2(arm), "fore" + s: r2(180 - inter)}


def y_haut(a, sol=H, jeu=0.3):
    """Contact du haut du corps seul (tronc, tête, bras) : les jambes sont en IK."""
    pts = fk(a)
    haut = pts[:4] + pts[4:6] + pts[9:11]
    return sol + jeu + max(r - dy for dx, dy, r in haut)


def lin(cles, f):
    for (f0, v0), (f1, v1) in zip(cles, cles[1:]):
        if f0 <= f <= f1:
            return v0 + (v1 - v0) * (f - f0) / (f1 - f0)
    return cles[-1][1] if f > cles[-1][0] else cles[0][1]


def doux(cles, f):
    for (f0, v0), (f1, v1) in zip(cles, cles[1:]):
        if f0 <= f <= f1:
            return v0 + (v1 - v0) * lisse((f - f0) / (f1 - f0))
    return cles[-1][1] if f > cles[-1][0] else cles[0][1]


# Haut du corps, de l'amorti au repos : (image, valeurs). Les bras gardent leur tour (−360 = devant-bas).
HAUT = [
    (100, dict(root=60, spineLow=14, chest=12, neck=25, armN=-300, foreN=20, armF=-290, foreF=20)),
    (102, dict(root=92, spineLow=22, chest=20, neck=45, armN=-282, foreN=30, armF=-296, foreF=30)),
    (106, dict(root=155, spineLow=25, chest=25, neck=50, armN=-228, foreN=60, armF=-262, foreF=85)),
    (111, dict(root=205, spineLow=25, chest=25, neck=45, armN=-305, foreN=80, armF=-318, foreF=80)),
    (116, dict(root=255, spineLow=22, chest=20, neck=40, armN=-298, foreN=60, armF=-308, foreF=60)),
    (121, dict(root=300, spineLow=18, chest=16, neck=30, armN=-288, foreN=40, armF=-300, foreF=40)),
    (124, dict(root=318, spineLow=16, chest=14, neck=22, armN=-282, foreN=30, armF=-296, foreF=30)),
    (127, dict(root=336, spineLow=14, chest=12, neck=10, armN=-290, foreN=40, armF=-310, foreF=45)),
    (130, dict(root=362, spineLow=12, chest=12, neck=-8, armN=-300, foreN=55, armF=-340, foreF=60)),
    (133, dict(root=382, spineLow=12, chest=12, neck=-20, armN=-312, foreN=70, armF=-366, foreF=62)),
]
# Jambes en angles pendant la roulade (les pieds quittent le sol à 105, reviennent à 123)
JROUL = [
    (106, dict(thighN=112, shinN=118, thighF=88, shinF=90, footN=-20, footF=-20)),
    (111, dict(thighN=130, shinN=142, thighF=110, shinF=118, footN=-20, footF=-20)),
    (116, dict(thighN=132, shinN=144, thighF=104, shinF=118, footN=-10, footF=-10)),
    (121, dict(thighN=126, shinN=140, thighF=100, shinF=115, footN=0, footF=0)),
]
PROF = [(100, (15, 8)), (101, (16, 12)), (105, (28, 12)), (121, (28, 12)), (128, (20, 9)), (135, (12, 7))]
J = 135          # première image reprise du sprint (clé 20 : fin d'appui F, N lancée devant)
KJ = 20
LONG = 178



def reception_roulade(corr, pieds_moteur=None):
    out = []
    # 100 : les mains touchent la plateforme, les pieds sont encore en l'air derrière : il plonge
    xc = X0 + VX * (F1 - F0)
    pieds = PIEDS
    BX = [(100, xc), (101, xc + 7), (102, xc + 12.5), (103, xc + 17), (104, xc + 21), (106, pieds + 25),
          (111, pieds + 46), (116, pieds + 66), (121, pieds + 80)]

    def haut(f):
        a = {ch: doux([(k, v[ch]) for k, v in HAUT], f) if f >= 121 else lin([(k, v[ch]) for k, v in HAUT], f)
             for ch in HAUT[0][1]}
        ap, tp = lin([(k, v[0]) for k, v in PROF], f), lin([(k, v[1]) for k, v in PROF], f)
        a.update(armN_p=ap, armF_p=-ap, thighN_p=tp, thighF_p=-tp)
        return a

    # 100-104 : les bras plient et amortissent, le menton rentre, l'épaule descend vers la plateforme ;
    # les jambes, en l'air, commencent à se replier
    jcl = [(100, JPLONGE[0]), (103, JPLONGE[1])] + JROUL
    y_prec, vy = YC, -(VY0 - 2 * GR * (F1 - F0))
    for f in range(F1, 124):
        a = haut(f)
        for ch in JROUL[0][1]:
            a[ch] = lin([(k, v[ch]) for k, v in jcl], f)
        x = lin(BX + [(124, pieds + 88)], f)
        if f == F1:
            y = YC
        elif f <= 104:
            # l'épaule descend vers la plateforme en ralentissant (les bras freinent)
            y = max(Y_PLONGE[f - 101], SOL_TRONC(a))
        elif f <= 109:
            y = SOL_TRONC(a)
        else:
            y = y_contact(a)
        y += corr.get(f, 0)
        nom = {100: "les mains touchent, il plonge", 106: "sur l'épaule", 111: "sur le dos", 116: "les reins",
               121: "les pieds arrivent"}.get(f)
        out.append(cle(f, dict(a, x=x, y=y), courbe="lin", ancre=False, nom=nom))
    # 124 → J : il se relève dans l'élan. N se pose sous le bassin (127), les deux jambes poussent,
    # le bassin accélère (2,7 → 11,8 par image) en montant ; N décolle à 129 et se lance devant,
    # F pousse jusqu'au bout et quitte la plateforme : on reprend le sprint à la clé 20.
    a123 = out[-1]["fixe"]
    cn, cf = chevilles(a123)
    x123, y123 = a123["x"], a123["y"]
    pN0, pF = (r2(x123 + cn[0]), H + G), (r2(x123 + cf[0]), H + G)
    if pieds_moteur:
        pN0, pF = (pieds_moteur[0], H + G), (pieds_moteur[1], H + G)
    pN = (min(pN0[0], pF[0] - 24), H + G)
    S = sprint_cle(KJ, pF[0])                 # clé 20 posée de façon que F quitte l'endroit où il est planté
    xJ = S["fixe"]["x"]
    t = J - 123
    acc = 2 * (xJ - x123 - 2.7 * t) / t ** 2
    PY = [(123, y123), (124, y123 + 1), (127, H + 41), (130, H + 63), (133, H + 75.5), (J, S["fixe"]["y"])]
    vN = (S["vise"]["legN"][0] - xJ, S["vise"]["legN"][1] - S["fixe"]["y"])
    vF = S["vise"]["legF"]
    HAUT[:] = [h for h in HAUT if h[0] != J] + [(J, {k: S["fixe"][k] for k in HAUT[0][1]})]

    def X(f):
        return x123 + 2.7 * (f - 123) + acc * (f - 123) ** 2 / 2
    for f in range(124, J):
        a = haut(f)
        u = f - 123
        x, y = X(f), doux(PY, f) + corr.get(f, 0)
        nom = {127: "les deux pieds sous lui, il pousse", 130: "N part devant", 133: "F pousse"}.get(f)
        if f < 127:                        # N finit de descendre : il touche à 127
            w = (f - 123) / 4
            qN = (pN0[0] + (pN[0] - pN0[0]) * w, H + G + 7 * (1 - w))
        elif f <= 128:
            qN = pN
        else:                              # N décolle et passe sous le bassin, genou devant
            w = (f - 129) / (J - 129)
            rx = (pN[0] + 1 - X(129)) * (1 - w) + vN[0] * w
            ry = lin([(129, H + G + 4 - doux(PY, 129)), (132, -52), (J, vN[1])], f)
            qN = (x + rx, y + ry)
        if f <= 132:
            qF = pF
        else:                              # talon qui monte, puis pointe qui quitte
            w = (f - 132) / (J - 132)
            qF = (pF[0] + (vF[0] - pF[0]) * w, pF[1] + (vF[1] - pF[1]) * w * w)
        for sd, pd, plat in (("N", qN, f <= 128), ("F", qF, f <= 132)):
            if plat:
                a["foot" + sd] = ik_jambe(a, sd, (pd[0] - x, pd[1] - y))["foot" + sd]
        out.append(cle(f, dict(a, x=x, y=y), {"legN": qN, "legF": pF if f <= 132 else qF}, courbe="lin",
                       ancre=False, nom=nom))
    out += parcours(J, KJ, pF[0] - SPRINT["cles"][20]["vise"]["legF"][0])
    return out


RAYON = {"head": 23.0}
SPRINT = None


def sprint_cle(k, pf_x):
    return sk(k, pf_x - SPRINT["cles"][20]["vise"]["legF"][0], H)


def sk(k, dx, dy):
    """Clé k du sprint (k peut dépasser 27) décalée de (dx, dy), tour complet ajouté au tronc et retiré
    aux bras (angles continus après la roulade)."""
    c = json.loads(json.dumps(SPRINT["cles"][k % 28]))
    dx = dx + SPRINT["avance"] * (k // 28)
    H_ = dy
    fx = c["fixe"]
    fx["x"] = r2(fx["x"] + dx); fx["y"] = r2(fx["y"] + H_)
    fx["root"] = r2(fx["root"] + 360)
    for ch in ("armN", "armF"):
        fx[ch] = r2(fx[ch] - 360)
    for leg in c["vise"]:
        c["vise"][leg] = [r2(c["vise"][leg][0] + dx), r2(c["vise"][leg][1] + H_)]
    c.pop("nom", None)
    c["ancre"] = False
    return c


def sk_frac(k, dx, dy):
    """Clé du sprint à un instant fractionnaire (interpolation linéaire, angles déjà continus)."""
    k0 = int(math.floor(k)); u = k - k0
    a, b = sk(k0, dx, dy), sk(k0 + 1, dx, dy)
    fx = {c: a["fixe"][c] + (b["fixe"][c] - a["fixe"][c]) * u for c in a["fixe"]}
    rel = {leg: tuple(a["vise"][leg][i] - a["fixe"][xy] + (b["vise"][leg][i] - b["fixe"][xy]
                                                           - a["vise"][leg][i] + a["fixe"][xy]) * u
                      for i, xy in ((0, "x"), (1, "y"))) for leg in a["vise"]}
    return fx, rel


GPARC = 0.36      # gravité des bonds du parcours (px / image²)
VX = 12.25        # vitesse du sprint (px / image)
DECOR = []


def bond(f0, k0, dx, dy, n, dy2, formes, penche, noms):
    """Bond entre la fin d'appui F (clé k0 ≡ 20, image f0, déjà posée) et la pose du pied N (clé k0 + 8,
    image f0 + n) : vol parabolique de n images au lieu de 8. Renvoie les clés f0+1 … f0+n-1, et le
    décalage (dx2, dy2) du sprint qui reprend à la clé k0 + 8."""
    A = sk(k0, dx, dy)["fixe"]
    x0, y0 = A["x"], A["y"]
    brut = SPRINT["avance"] * ((k0 + 8) // 28) + SPRINT["cles"][(k0 + 8) % 28]["fixe"]["x"] \
        - SPRINT["avance"] * (k0 // 28) - SPRINT["cles"][k0 % 28]["fixe"]["x"]
    dx2 = dx + VX * n - brut
    y1 = sk(k0 + 8, dx2, dy2)["fixe"]["y"]
    vy = (y1 - y0) / n + GPARC * n / 2
    out = []
    for i in range(1, n):
        s_ = i / n
        fx, rel = sk_frac(k0 + 8 * s_, dx, dy)
        x, y = x0 + VX * i, y0 + vy * i - GPARC * i * i / 2
        fx = dict(fx, x=x, y=y, root=fx["root"] + penche * math.sin(math.pi * s_))
        vise = {}
        for leg, pts in formes.items():
            # écart à la course « étirée » : nul au départ et à l'arrivée, imposé aux instants donnés
            ecarts = [(0.0, (0, 0))]
            for sp, (rx, ry) in pts:
                _, rb = sk_frac(k0 + 8 * sp, dx, dy)
                ecarts.append((sp, (rx - rb[leg][0], ry - rb[leg][1])))
            ecarts.append((1.0, (0, 0)))
            ox = doux([(t, e[0]) for t, e in ecarts], s_)
            oy = doux([(t, e[1]) for t, e in ecarts], s_)
            vise[leg] = (x + rel[leg][0] + ox, y + rel[leg][1] + oy)
        for leg in rel:
            vise.setdefault(leg, (x + rel[leg][0], y + rel[leg][1]))
        out.append(cle(f0 + i, fx, vise, courbe="lin", ancre=False, nom=noms.get(i)))
    return out, dx2, x0


HW = 210           # hauteur du mur à grimper au-dessus de la plateforme (≈ 2 m : plus haut que lui)
ERR_ESC = {}       # écart main mesuré dans le moteur pendant l'escalade
ESC = {}           # images de l'escalade (pour la mesure)


def escalade(out, f, k, dx, dy):
    """Mur haut : appel sur F (clé k-1 ≡ 20, image f-1), pied N posé sur la face, il pousse, les mains
    attrapent le bord, traction, rétablissement (bras tendus, genou N puis pied F sur le dessus), puis
    il se relève et repart en accélérant. Les clés sont d'abord pensées « telles que rendues », puis les
    canaux retardés (RETARD) sont recopiés quelques images plus tôt."""
    T = dy + HW
    A = sk(k - 1, dx, dy)
    x0 = A["fixe"]["x"]
    xw = x0 + 78                              # face du mur
    fA = f - 1
    # poses rendues aux instants clés (i = images depuis l'appel). Bras : angles avant l'IK.
    P = [
        (0, dict(x=x0, y=A["fixe"]["y"], root=A["fixe"]["root"], spineLow=12, chest=12, neck=-26,
                 armN=-317, foreN=90, armF=-373, foreF=60)),
        (4, dict(x=xw - 58, y=dy + 92, root=374, spineLow=10, chest=8, neck=-20,
                 armN=-185, foreN=30, armF=-215, foreF=30)),
        (7, dict(x=xw - 50, y=dy + 102, root=368, spineLow=8, chest=6, neck=-24,
                 armN=-160, foreN=20, armF=-170, foreF=20)),
        (11, dict(x=xw - 42, y=dy + 120, root=366, spineLow=8, chest=6, neck=-20,
                  armN=-160, foreN=20, armF=-165, foreF=20)),
        (14, dict(x=xw - 38, y=dy + 113, root=364, spineLow=8, chest=6, neck=-14,
                  armN=-160, foreN=20, armF=-165, foreF=20)),
        (20, dict(x=xw - 28, y=T - 50, root=370, spineLow=10, chest=8, neck=-12,
                  armN=-215, foreN=110, armF=-220, foreF=110)),
        (23, dict(x=xw - 18, y=T - 12, root=388, spineLow=10, chest=8, neck=-20,
                  armN=-250, foreN=90, armF=-255, foreF=90)),
        (26, dict(x=xw - 4, y=T + 20, root=408, spineLow=10, chest=8, neck=-25,
                  armN=-275, foreN=40, armF=-280, foreF=40)),
        (29, dict(x=xw + 12, y=T + 46, root=412, spineLow=10, chest=8, neck=-30,
                  armN=-285, foreN=20, armF=-290, foreF=20)),
        (33, dict(x=xw + 28, y=T + 52, root=398, spineLow=12, chest=10, neck=-30,
                  armN=-310, foreN=50, armF=-300, foreF=50)),
    ]
    NI = 36                                    # dernière image de l'escalade ; i = NI+1 : clé ≡ 0 du sprint
    RATE0, NR = 0.5, 24                        # reprise : la course accélère de demi-vitesse à pleine vitesse
    kr = k - 1 + 8                             # clé ≡ 0 (pose du pied N) à l'image fA + NI + 1
    dxr = (xw + 44) - sk(kr, 0, T)["fixe"]["x"]

    def phase(g):                              # g images après la reprise (g peut être < 0)
        if g <= 0:
            return kr + RATE0 * g
        if g >= NR:
            return kr + NR * (RATE0 + 1) / 2 + (g - NR)
        return kr + RATE0 * g + (1 - RATE0) * g * g / (2 * NR)

    fxe, rele = sk_frac(phase(-1), dxr, T)
    P.append((NI, {ch: fxe[ch] for ch in P[0][1]}))
    sF = tuple(A["vise"]["legF"])
    sN = tuple(A["vise"]["legN"])
    pN = (xw - 12, dy + 52)                    # pied N sur la face
    tN = (xw - 28, T + 14)                     # genou N sur le dessus, tibia qui dépasse au-dessus du vide
    pF2 = (xw + 30, T + G + 0.3)               # pied F posé sur le dessus
    eN = (fxe["x"] + rele["legN"][0], fxe["y"] + rele["legN"][1])
    eF = (fxe["x"] + rele["legF"][0], fxe["y"] + rele["legF"][1])
    JN = [(0, sN), (3, (xw - 50, dy + 40)), (7, pN), (14, pN), (17, (xw - 12, dy + 100)), (20, (xw - 12, dy + 140)),
          (23, (xw - 14, T - 40)), (26, (xw - 26, T - 10)), (29, tN), (32, tN), (34, (xw + 30, T + 30)), (NI, eN)]
    JF = [(0, sF), (4, (x0 - 10, dy + 46)), (8, (xw - 50, dy + 44)), (12, (xw - 30, dy + 70)), (15, (xw - 12, dy + 86)),
          (19, (xw - 12, dy + 86)), (24, (xw - 12, T - 60)), (28, (xw - 10, T + 30)), (31, pF2), (NI - 1, pF2),
          (NI, eF)]
    plant = {"N": (xw + 9, T + G + 0.3), "F": (xw + 2, T + G + 0.3)}
    U = [(9, 0), (12, 1), (29, 1), (32, 0)]

    def pose(i):
        return {ch: doux([(t, v[ch]) for t, v in P], i) for ch in P[0][1]}

    R = {}
    for i in range(1, NI + 1):
        a = pose(i)
        u = doux(U, i)
        if u > 0:
            pts = fk(a)
            for s, ih in (("N", 5), ("F", 10)):
                libre = pts[ih][:2]
                ex, ey = ERR_ESC.get((fA + i, s), (0, 0))
                c = (plant[s][0] - a["x"] - ex, plant[s][1] - a["y"] - ey)
                c = (libre[0] + (c[0] - libre[0]) * u, libre[1] + (c[1] - libre[1]) * u)
                a.update(ik_bras(a, s, c))
        vise = {leg: (doux([(t, p[0]) for t, p in JJ], i), doux([(t, p[1]) for t, p in JJ], i))
                for leg, JJ in (("legN", JN), ("legF", JF))}
        R[fA + i] = (a, vise)
        if 12 <= i <= 29:
            ESC[fA + i] = plant
    noms = {1: "appel : il fonce vers le mur", 7: "pied sur la face du mur", 12: "les mains attrapent le bord",
            20: "traction", 25: "rétablissement, bras tendus", 29: "genou sur le dessus", 33: "il se relève"}
    for i in range(1, NI + 1):
        a, vise = R[fA + i]
        out.append(cle(fA + i, a, vise, courbe="lin", ancre=False, nom=noms.get(i)))
    fR = fA + NI + 1
    for g in range(NR):
        fx, rel = sk_frac(phase(g), dxr, T)
        vise = {leg: (fx["x"] + rel[leg][0], fx["y"] + rel[leg][1]) for leg in rel}
        out.append(cle(fR + g, fx, vise, courbe="lin", ancre=False,
                       nom="il repart en courant sur le mur" if g == 0 else None))
    # canaux retardés : la valeur rendue à l'image f s'écrit dans la clé f - r
    K = {c["f"]: c["fixe"] for c in out}
    for ch, r in RETARD.items():
        for fr in range(fA + 1, fA + NI + 1):
            K[fr - r][ch] = r2(R[fr][0][ch])
        for fr in range(fR - r, fR):
            K[fr][ch] = r2(sk_frac(phase(fr + r - fR - r), dxr, T)[0][ch])
    return fR + NR, int(round(phase(NR))), dxr, xw


def parcours(f, k, dx):
    """Après la relance : sprint, haie (muret), trou franchi en foulée, descente vers un niveau bas."""
    global DECOR
    out, dy = [], H

    def courir(nb, nom=None):
        nonlocal f, k
        for i in range(nb):
            c = sk(k, dx, dy); c["f"] = f
            if i == 0 and nom:
                c["nom"] = nom
            out.append(c); f += 1; k += 1

    courir(1, "il repart en sprint")
    courir(28)                                     # jusqu'à la fin d'appui F suivante (clé ≡ 20)
    # 1. le muret : haie franchie jambe N tendue devant, jambe F repliée qui passe par-dessus
    n = 24
    b, dx2, x0 = bond(f - 1, k - 1, dx, dy, n, dy,
                      {"legN": [(0.3, (62, -30)), (0.55, (60, -36)), (0.75, (45, -55))],
                       "legF": [(0.25, (-50, -38)), (0.5, (-22, -16)), (0.75, (-8, -26))]}, 16,
                      {1: "appel : il attaque le muret", 12: "au-dessus du muret"})
    xm = x0 + VX * n * 0.5
    muret = (xm - 18, xm + 18, H + 55)
    out += b; f += n - 1; k += 7; dx = dx2
    courir(20, "réception jambe N")
    courir(1)
    # 2. le trou : grande foulée, jambe N haute devant, jambe F tendue derrière
    n = 14
    b, dx2, x0 = bond(f - 1, k - 1, dx, dy, n, dy,
                      {"legN": [(0.5, (42, -40))], "legF": [(0.45, (-62, -48))]}, 6,
                      {1: "il s'élance au-dessus du trou", 7: "en foulée"})
    trou = (x0 - 26, x0 + VX * n + 21.8 - 16)
    out += b; f += n - 1; k += 7; dx = dx2
    courir(20, "réception de l'autre côté")
    courir(1)
    # 3. le mur : il le grimpe et repart en courant sur le dessus
    f, k, dx, xw = escalade(out, f, k, dx, dy)
    dy = dy + HW
    courir(3)
    # 4. la descente : il saute du haut du mur vers le niveau bas et amortit
    n, bas = 32, -40
    b, dx2, x0 = bond(f - 1, k - 1, dx, dy, n, bas,
                      {"legN": [(0.4, (32, -55)), (0.8, (30, -68))], "legF": [(0.4, (-48, -45)), (0.8, (-14, -42))]},
                      -6, {1: "il saute du bord", 12: "il descend"})
    bord = x0 - 26
    out += b; f += n - 1; k += 7; dx, dy = dx2, bas
    d0 = len(out)
    courir(30, "réception en bas, il amortit")
    for i, c in enumerate(out[d0:d0 + 10]):        # amorti : le bassin descend puis remonte
        c["fixe"]["y"] = r2(c["fixe"]["y"] - 16 * math.sin(math.pi * i / 10))
    fin = out[-1]["fixe"]["x"] + 400
    DECOR = [[-200, BORD0, 0], [P, trou[0], H], [trou[1], xw, H], [xw, bord, H + HW], [muret[0], muret[1], muret[2]],
             [bord, fin, bas]]
    return out


def SOL_TRONC(a, sol=H, jeu=0.3):
    """Hauteur du bassin pour que le tronc ou la tête (sans bras ni jambes) touche le sol."""
    return sol + jeu + max(r - dy for dx, dy, r in fk(a)[:4])


def mesure_moteur(chemin):
    """Point le plus bas (bord du trait) de chaque image, mesuré par le moteur (anim.sh --print)."""
    import re
    import subprocess
    sortie = subprocess.run([os.path.join(ICI, "anim.sh"), chemin, "--print"], capture_output=True,
                            text=True).stdout
    bas, chev, mains = {}, {}, {}
    for ligne in sortie.splitlines():
        m = re.match(r"\s*(\d+) course_saut_roulade@", ligne)
        if not m:
            continue
        pts = re.findall(r"(\w+)\((-?[\d.]+),(-?[\d.]+)\)", ligne)
        bas[int(m.group(1))] = min(float(y) - RAYON.get(n, G) for n, x, y in pts)
        d = {n: float(x) for n, x, y in pts}
        chev[int(m.group(1))] = (r2(d["ankleN"]), r2(d["ankleF"]))
        dy = {n: float(y) for n, x, y in pts}
        mains[int(m.group(1))] = {"N": (d["handN"], dy["handN"]), "F": (d["handF"], dy["handF"])}
    return bas, chev, mains


def ecrire(cles, sprint):
    anim = {
        "nom": "course_saut_roulade", "boucle": False, "longueur": len(cles), "base": "repos",
        "decalage": sprint["decalage"], "ecartement": {"jambes": 7},
        "filtres": {"trainee": False, "fantomes": False, "etirement": False},
        "decor": {"sol": DECOR},
        "cles": cles,
    }
    out = os.path.join(ANIMS, "course_saut_roulade.json")
    with open(out, "w") as f:
        json.dump(anim, f, indent=1, ensure_ascii=False)
        f.write("\n")
    return out


# Jambes en l'air pendant que les mains amortissent : tendues derrière (plongeon) puis repliées
JPLONGE = [dict(thighN=-15, shinN=50, thighF=-25, shinF=70, footN=-30, footF=-30),
           dict(thighN=50, shinN=85, thighF=35, shinF=95, footN=-25, footF=-25)]
Y_PLONGE = [103, 112, 120, 126]   # bassin 101 à 104 : il passe par-dessus les mains, sans à-coup
ERR_MAIN_ANCIEN = {(100, 'N'): (0.5, -0.3), (100, 'F'): (0.1, 0.1), (101, 'N'): (0.7, -0.7), (101, 'F'): (0.6, -0.6),
            (102, 'N'): (1.1, -1.0), (102, 'F'): (1.0, -1.0), (103, 'N'): (1.6, -1.4), (103, 'F'): (1.4, -1.4),
            (104, 'N'): (2.2, -1.7), (104, 'F'): (2.0, -1.9)}
ERR_MAIN = {}
RETARD = {"chest": 1, "neck": 2, "armN": 1, "foreN": 3, "armF": 1, "foreF": 3}   # décalage hérité du sprint


def planter_mains(cles, pieds):
    """Les mains se posent devant les pieds et n'y bougent plus de 100 à 104.
    Le moteur rend chaque canal avec un retard (decalage) : la valeur voulue à l'image f
    s'écrit dans la clé f - retard."""
    K = {c["f"]: c["fixe"] for c in cles}
    plant = {"N": pieds + 23, "F": pieds + 17}
    u = {98: 0.3, 99: 0.65, 100: 1, 101: 1, 102: 1, 103: 1, 104: 1, 105: 1, 106: 0.0, 107: 0.0, 108: 0.0}
    voulu = {}
    for f in range(98, 109):
        a = dict(K[f])
        for ch, r in RETARD.items():
            a[ch] = K[f - r][ch]
        pts = fk(a)
        for s, ih in (("N", 5), ("F", 10)):
            libre = pts[ih][:2]
            ex, ey = ERR_MAIN.get((f, s), (0, 0))   # écart mesuré une fois dans Godot (1 à 2 px)
            cible = (plant[s] - a["x"] - ex, H + G + 0.3 - a["y"] - ey)
            cible = (libre[0] + (cible[0] - libre[0]) * u[f], libre[1] + (cible[1] - libre[1]) * u[f])
            if u[f] < 1:                   # la main quitte le sol en montant, elle ne balaie pas la plateforme
                cible = (cible[0], max(cible[1], H + G + 4 + (14 if f > 105 else 0) - a["y"]))
            voulu[(f, s)] = ik_bras(a, s, cible)
    for (f, s), j in voulu.items():
        K[f - RETARD["arm" + s]]["arm" + s] = j["arm" + s]
        K[f - RETARD["fore" + s]]["fore" + s] = j["fore" + s]


def main():
    """Le contact au sol de la roulade est d'abord calculé en 2D (fk), puis recalé sur la mesure du
    moteur (le bras sorti sur le côté ne se projette pas exactement comme dans fk) : 3 passes."""
    global SPRINT
    sprint = SPRINT = json.load(open(os.path.join(ANIMS, "sprint.json")))
    corr, pm = {}, None
    for passe in range(6):
        cles = course(sprint) + appel() + [decolle()] + vol() + reception_roulade(corr, pm)
        planter_mains(cles, PIEDS + 22)
        out = ecrire(cles, sprint)
        if passe == 5 or not os.environ.get("GODOT"):
            break
        bas, chev, mains = mesure_moteur(out)
        for f in range(100, 106):          # mains plantées : on recale l'écart du moteur (1 à 2 px)
            for sd, dx in (("N", 23), ("F", 17)):
                mx, my = mains[f][sd]
                ex, ey = ERR_MAIN.get((f, sd), (0, 0))
                ERR_MAIN[(f, sd)] = (ex + mx - (PIEDS + 22 + dx), ey + my - (H + G + 0.3))
        for f, plant in ESC.items():        # mains sur le bord du mur : même recalage
            for sd in "NF":
                mx, my = mains[f][sd]
                ex, ey = ERR_ESC.get((f, sd), (0, 0))
                ERR_ESC[(f, sd)] = (ex + mx - plant[sd][0], ey + my - plant[sd][1])
        pm = chev[123]
        for f in range(F1, J):
            ecart = H + 0.3 - bas.get(f, H + 0.3)
            if 105 <= f <= 123:
                corr[f] = corr.get(f, 0) + ecart      # roule sur le dos : toujours au contact (avant 110 les jambes poussent, le bassin est en l air)
            elif ecart > 0:
                corr[f] = corr.get(f, 0) + ecart      # ailleurs : seulement remonter
    print(out, len(cles), "clés")


if __name__ == "__main__":
    main()
