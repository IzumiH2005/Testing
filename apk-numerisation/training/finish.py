"""Impression nette (sans réseau de neurones pour le rendu) : la page est réimprimée avec une palette
d'encres unies mesurées sur la photo, et des contours recalculés à haute définition.

Rien n'est inventé : chaque forme est le contour d'une zone de la photo, chaque couleur est une
couleur mesurée sur la photo (après correction de l'éclairage).

Étapes
  1. éclairage aplati : on mesure comment la lumière varie sur le fond (zones « papier » de l'IA 2)
     et on la divise, pour que le fond devienne parfaitement uni ;
  2. palette : les couleurs franches de la page (cœur des lettres et aplats, pas leurs bords)
     sont regroupées en quelques encres ; les couleurs « mélange » des bords sont écartées ;
  3. contours : chaque point haute définition prend l'encre la plus probable, calculée sur une
     version lissée et agrandie -> bords lisses au lieu de pixels ;
  4. poussières : les taches plus petites qu'un point de ponctuation sont retirées, ainsi que
     les défauts repérés par l'IA 2 ;
  5. illustrations (photos, dessins nuancés) : gardées telles quelles, juste éclairage corrigé.
"""
import os
import sys

import cv2
import numpy as np

SHARP = float(os.environ.get('SHARP', 0.7))
SMOOTH = float(os.environ.get('SMOOTH', 1.0))
SMOOTH_THIN = float(os.environ.get('SMOOTH_THIN', 0.25))
RIDGE = float(os.environ.get('RIDGE', 0.2))
PRES = float(os.environ.get('PRES', 0.3))


def _blur_masked(img, m, sigma):
    """Moyenne locale de img sur les seuls points m (convolution normalisée)."""
    k = (0, 0)
    num = cv2.GaussianBlur(img * m[..., None], k, sigma)
    den = cv2.GaussianBlur(m, k, sigma)
    return num, den


def flatten_light(ph, bgm, bg):
    """Divise la photo par l'éclairage mesuré sur le fond : le fond devient égal à bg partout.
    L'éclairage varie lentement : il est estimé sur une image réduite (rapide), puis agrandi.
    bgm : points autorisés à servir de fond (hors illustrations / défauts / couleur trop loin du fond).
    Le fond local est d'abord estimé par une médiane large (qui efface le texte), puis seuls les points
    proches de ce fond local servent à mesurer l'éclairage : une ombre ou une dérive de teinte est
    suivie, une lettre ou un aplat d'une autre couleur ne l'est jamais."""
    H, W = bgm.shape
    r = 256 / max(H, W)
    w, h = max(8, round(W * r)), max(8, round(H * r))
    allow = cv2.resize(bgm.astype(np.float32), (w, h), interpolation=cv2.INTER_AREA) > 0.9
    p = cv2.resize(ph, (w, h), interpolation=cv2.INTER_AREA).astype(np.float32)
    lab_p = srgb_to_lab(p)

    def fill(m):
        illum = np.zeros_like(p)
        have = np.zeros((h, w), bool)
        mf = m.astype(np.float32)
        for f in (0.015, 0.03, 0.06, 0.12, 0.3, 0.8):  # du plus fin au plus large
            num, den = _blur_masked(p, mf, f * 256)
            ok = (den > 0.15) & ~have
            illum[ok] = num[ok] / den[ok, None]
            have |= ok
        illum[~have] = bg
        return illum

    # fond local de départ : médiane large (le texte, fin, disparaît) sur les seuls points autorisés
    u8 = (np.clip(np.where(allow[..., None], p, bg), 0, 1) * 255 + 0.5).astype(np.uint8)
    est = cv2.medianBlur(cv2.medianBlur(u8, 21), 21).astype(np.float32) / 255
    for tol in (14.0, 9.0, 7.0):
        d = np.linalg.norm(lab_p - srgb_to_lab(est), axis=-1)
        m = allow & (d < tol)
        if m.sum() < 0.05 * m.size:
            break
        est = fill(m)
    illum = cv2.GaussianBlur(est, (0, 0), 1.0)
    illum = cv2.resize(illum, (W, H), interpolation=cv2.INTER_CUBIC)
    return np.clip(ph / np.maximum(illum, 1e-3) * bg, 0, 1.2)


def srgb_to_lab(x):
    return cv2.cvtColor(np.clip(x, 0, 1).astype(np.float32), cv2.COLOR_RGB2LAB)


def lab_to_srgb(x):
    return np.clip(cv2.cvtColor(x.reshape(-1, 1, 3).astype(np.float32), cv2.COLOR_LAB2RGB).reshape(-1, 3), 0, 1)


def find_palette(lab, cand, bg_lab, max_k=16, merge=11.0):
    """Encres franches de la page. lab (H,W,3), cand = points utilisables (cœur des formes)."""
    pts = lab[cand].reshape(-1, 3)
    rng = np.random.default_rng(0)
    if len(pts) > 60000:
        pts = pts[rng.choice(len(pts), 60000, replace=False)]
    pal = [bg_lab]
    if len(pts) > 200:
        crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 50, 0.2)
        _, lbl, cen = cv2.kmeans(pts.astype(np.float32), max_k, None, crit, 4, cv2.KMEANS_PP_CENTERS)
        cnt = np.bincount(lbl.ravel(), minlength=max_k)
        order = np.argsort(-cnt)
        groups = []  # (centre, effectif)
        for i in order:
            c, n = cen[i], cnt[i]
            # une encre franchement colorée (orange d'un drapeau, logo) peut être rare sur la page :
            # on la garde quand même, un tel point de couleur n'est pas du bruit de fond
            vivid = np.hypot(c[1], c[2]) > 35
            if n < (max(25, 0.0003 * len(pts)) if vivid else max(25, 0.0015 * len(pts))):
                continue
            for g in groups:
                if np.linalg.norm(g[0] - c) < merge:
                    g[0] = (g[0] * g[1] + c * n) / (g[1] + n)
                    g[1] += n
                    break
            else:
                groups.append([c.copy(), n])
        # recentre chaque encre sur la médiane de ses points (plus robuste que la moyenne)
        cents = np.array([g[0] for g in groups] + [bg_lab])
        d = ((pts[:, None] - cents[None]) ** 2).sum(-1)
        a = d.argmin(1)
        for j, g in enumerate(groups):
            sel = pts[(a == j) & (d[np.arange(len(pts)), a] < 15 ** 2)]
            if len(sel) > 30:
                g[0] = np.median(sel, 0)
        for c, n in groups:
            if np.linalg.norm(c - bg_lab) >= merge:
                pal.append(c)
    return np.array(pal, np.float32)


def drop_mixtures(pal, lab, cand):
    """Une couleur qui n'est qu'un mélange de deux encres (bord flou entre elles) n'est pas une encre :
    elle est géométriquement entre deux encres ET ne forme que des liserés minces (rien ne reste
    après une érosion). Un vrai aplat sombre sur fond clair (encadré) a un intérieur : il est gardé."""
    if len(pal) < 3:
        return pal, np.zeros(len(pal), bool)
    d = ((lab[..., None, :] - pal[None, None]) ** 2).sum(-1)
    near = d.argmin(-1)
    ker = np.ones((5, 5), np.uint8)
    keep, mid = [0], [False]
    for i in range(1, len(pal)):
        between = False
        for a in range(len(pal)):
            for b in range(len(pal)):
                if len({a, b, i}) < 3:
                    continue
                v = pal[b] - pal[a]
                t = float(np.dot(pal[i] - pal[a], v) / max(np.dot(v, v), 1e-6))
                if 0.15 < t < 0.85 and np.linalg.norm(pal[a] + t * v - pal[i]) < 6.0:
                    between = True
        if between:
            m = ((near == i) & cand).astype(np.uint8)
            core = cv2.erode(m, ker).sum()
            if core < 0.15 * max(1, m.sum()) or core < 40:
                continue
        keep.append(i)
        mid.append(between)
    return pal[keep], np.array(mid)


def clean_islands(lbl, K, long_side, pal=None, keep_de=30.0):
    dust = (0.0012 * long_side) ** 2      # plus petit qu'un point de ponctuation
    blob = (0.004 * long_side) ** 2       # taille max d'un défaut de remplissage dans une forme
    hole = (0.0009 * long_side) ** 2      # trou de fond dans une forme : seulement minuscule (on garde les « o »)
    H, W = lbl.shape
    ker = np.ones((3, 3), np.uint8)

    def small_box(j, x, y, w, h, a):
        # l'encre qui entoure n'est qu'une auréole autour de la marque (tache sur le papier), pas un
        # vrai cartouche : la marque n'est pas un contenu
        r = 4 * max(w, h)
        return (lbl[max(0, y - r):y + h + r, max(0, x - r):x + w + r] == j).sum() < 6 * a

    for k in range(K):
        n, cc, st, _ = cv2.connectedComponentsWithStats((lbl == k).astype(np.uint8), connectivity=8)
        lim = hole if k == 0 else blob
        for i in np.where(st[:, cv2.CC_STAT_AREA] < lim)[0]:
            if i == 0:
                continue
            x, y, w, h, a = st[i]
            x0, y0, x1, y1 = max(0, x - 2), max(0, y - 2), min(W, x + w + 2), min(H, y + h + 2)
            m = cc[y0:y1, x0:x1] == i
            ring = cv2.dilate(m.astype(np.uint8), ker).astype(bool) & ~m
            nb = np.bincount(lbl[y0:y1, x0:x1][ring], minlength=K)
            j = int(nb.argmax())
            if j == k:
                continue
            frac = nb[j] / max(1, nb.sum())
            if j == 0 and a < dust:            # poussière sur le fond
                lbl[y0:y1, x0:x1][m] = 0
            elif j != 0 and frac > 0.8 and (pal is None or a < dust or np.linalg.norm(pal[k] - pal[j]) < keep_de
                                             or small_box(j, x, y, w, h, a)):
                # enfermé dans une forme d'une seule encre, de couleur voisine : défaut de remplissage.
                # Une marque bien contrastée (accent, point, lettre dans un cartouche) est gardée.
                lbl[y0:y1, x0:x1][m] = j


def drop_soft_shapes(lbl, pal, G, px, min_sharp=0.22):
    """Retire les formes à bord mou (variation d'éclairage, auréole, ombre) : sur leur bord, la couleur
    change trop lentement par rapport à l'écart de couleur avec ce qui les entoure.
    G : ΔE par pixel photo (agrandi), px : pixels haute déf. par pixel photo."""
    K = len(pal)
    H, W = lbl.shape
    ker = np.ones((3, 3), np.uint8)
    ring_w = max(2, int(round(px)))
    kr = np.ones((2 * ring_w + 1, 2 * ring_w + 1), np.uint8)
    for k in range(1, K):
        n, cc, st, _ = cv2.connectedComponentsWithStats((lbl == k).astype(np.uint8), connectivity=8)
        for i in range(1, n):
            x, y, w, h, a = st[i]
            p = ring_w + 2
            x0, y0, x1, y1 = max(0, x - p), max(0, y - p), min(W, x + w + p), min(H, y + h + p)
            m = (cc[y0:y1, x0:x1] == i).astype(np.uint8)
            edge = (m - cv2.erode(m, ker)).astype(bool)
            ring = cv2.dilate(m, kr).astype(bool) & ~m.astype(bool)
            lab_ring = lbl[y0:y1, x0:x1][ring]
            if edge.sum() == 0 or len(lab_ring) == 0:
                continue
            nb = np.bincount(lab_ring, minlength=K)
            j = int(nb.argmax())
            contrast = np.linalg.norm(pal[k] - pal[j])
            if contrast > 22:  # écart franc : c'est un vrai tracé, même fin ou un peu flou
                continue
            # bord = maximum de netteté au voisinage du contour (le contour calculé peut être décalé d'un pixel)
            gm = cv2.dilate(G[y0:y1, x0:x1], kr)[edge]
            sharp = float(np.median(gm)) / max(contrast, 1e-3)
            if sharp < min_sharp:
                lbl[y0:y1, x0:x1][m.astype(bool)] = j


def merge_kin(lbl, pal, long_side, max_de=30.0):
    """Une lettre est d'une seule encre : un petit morceau d'une encre proche (bleu foncé sur un texte
    noir, à cause de l'arc-en-ciel de l'objectif) collé à une forme d'une autre encre prend l'encre de
    cette forme. Les encres franchement différentes (or et noir) ne sont jamais fusionnées."""
    K = len(pal)
    H, W = lbl.shape
    lim = (0.006 * long_side) ** 2
    ker = np.ones((3, 3), np.uint8)
    areas = {}
    for k in range(1, K):
        mk = (lbl == k).astype(np.uint8)
        if mk.any():
            areas[k] = cv2.connectedComponentsWithStats(mk, connectivity=8)
    tot = np.bincount(lbl.ravel(), minlength=K)
    for k, (n, cc, st, _) in areas.items():
        for i in np.where(st[:, cv2.CC_STAT_AREA] < lim)[0]:
            if i == 0:
                continue
            x, y, w, h, a = st[i]
            x0, y0, x1, y1 = max(0, x - 2), max(0, y - 2), min(W, x + w + 2), min(H, y + h + 2)
            m = cc[y0:y1, x0:x1] == i
            ring = cv2.dilate(m.astype(np.uint8), ker).astype(bool) & ~m
            nb = np.bincount(lbl[y0:y1, x0:x1][ring], minlength=K).astype(float)
            nb[k] = 0
            # seules les encres proches comptent (un morceau de lettre noire posé dans un encadré
            # turquoise touche surtout le turquoise, mais c'est au noir qu'il appartient)
            kin = np.array([0.0] + [nb[j] if np.linalg.norm(pal[k] - pal[j]) <= max_de else 0.0
                                    for j in range(1, K)])
            if kin.sum() == 0:
                continue
            j = int(np.argmax(kin))
            # on ne va que vers l'encre la plus présente de la page : jamais un bout de noir vers le bleu
            if kin[j] / kin.sum() < 0.8 or nb[j] / nb.sum() < 0.08 or j not in areas or tot[j] < tot[k]:
                continue
            ccj, stj = areas[j][1], areas[j][2]
            touch = np.unique(ccj[y0:y1, x0:x1][ring])
            touch = touch[touch > 0]
            if a < 0.5 * stj[touch, cv2.CC_STAT_AREA].sum():
                lbl[y0:y1, x0:x1][m] = j


def unify_clusters(lbl, pal, long_side, size=0.02, pad=0.015, max_de=36.0):
    """Une petite forme isolée (lettre, accent, point) posée sur un fond uni est imprimée d'une seule
    encre. Le flou et la compression JPEG colorent ses bords et ses parties fines (bleu clair au bord
    d'une lettre bleu nuit sur un cartouche turquoise, brun sombre dans le noir) : ces pixels prennent
    l'encre de la forme, choisie par la majorité des alentours (le mot, la ligne). Une encre n'est
    absorbée que si elle est proche de celle de la forme, ou située entre elle et le fond (liseré)."""
    K = len(pal)
    H, W = lbl.shape
    pd = round(pad * long_side)
    lim = (size * long_side) ** 2
    tot = np.bincount(lbl.ravel(), minlength=K)
    de = lambda a, b: float(np.linalg.norm(pal[a] - pal[b]))

    def seg(q, j, s):
        a, b, p = pal[j], pal[s], pal[q]
        v = b - a
        t = np.clip(np.dot(p - a, v) / max(np.dot(v, v), 1e-6), 0, 1)
        return float(np.linalg.norm(a + t * v - p))

    for s in [0] + [q for q in range(1, K) if tot[q] > 0.002 * H * W]:
        M = ((lbl != s) & (lbl != 0)) if s else (lbl != 0)
        n, cc, st, _ = cv2.connectedComponentsWithStats(M.astype(np.uint8), connectivity=8)
        for i in range(1, n):
            x, y, w, h, a = st[i]
            if a >= lim or a < 4:
                continue
            x0, y0, x1, y1 = max(0, x - 1), max(0, y - 1), min(W, x + w + 1), min(H, y + h + 1)
            m = cc[y0:y1, x0:x1] == i
            sub = lbl[y0:y1, x0:x1]
            c = np.bincount(sub[m], minlength=K)
            if (c > 0).sum() < 2:
                continue
            ring = cv2.dilate(m.astype(np.uint8), np.ones((3, 3), np.uint8)).astype(bool) & ~m
            if (sub[ring] == s).mean() < 0.6:
                continue
            X0, Y0, X1, Y1 = max(0, x - pd), max(0, y - pd), min(W, x + w + pd), min(H, y + h + pd)
            nb = np.bincount(lbl[Y0:Y1, X0:X1].ravel(), minlength=K)
            # l'encre de la forme : la plus répandue alentour parmi celles qui contrastent vraiment avec
            # le fond (une encre pâle de liseré ne peut pas être l'encre d'un accent)
            pres = [q for q in range(1, K) if c[q] > 0]
            dmax = max(de(q, s) for q in pres)
            j = max((q for q in pres if de(q, s) >= 0.6 * dmax), key=lambda q: nb[q])
            dj = de(j, s)
            # creux d'une lettre (intérieur d'un o) : pas un liseré, il garde sa couleur claire
            jm = (m & (sub == j)).astype(np.uint8)
            ff = np.pad(1 - jm, 1, constant_values=1)
            cv2.floodFill(ff, None, (0, 0), 2)
            hole = ff[1:-1, 1:-1] == 1
            fr = np.zeros_like(m)
            cov = 0.0
            for q in range(1, K):
                if q == j or c[q] == 0:
                    continue
                if de(q, j) <= max_de:
                    # une encre pâle très majoritaire n'est pas le bord d'une forme : quelques pixels
                    # plus foncés ne la recolorent pas (pli du dos, ombre d'un coin abîmé)
                    if de(q, s) < 0.6 * dmax and c[q] > 2 * c[j]:
                        continue
                    sub[m & (sub == q)] = j
                elif de(q, s) < dj and seg(q, j, s) < 0.5 * dj:
                    f = m & (sub == q) & ~hole
                    v = pal[s] - pal[j]
                    t = float(np.clip(np.dot(pal[q] - pal[j], v) / max(np.dot(v, v), 1e-6), 0, 1))
                    cov += f.sum() * (1 - t)
                    fr |= f
            core = (m & (sub == j)).astype(np.uint8)
            if fr.any() and cv2.connectedComponents(cv2.dilate(core, np.ones((3, 3), np.uint8)))[0] > 2:
                # cœur en plusieurs morceaux reliés par l'encre claire : trait fin (lettre d'un sceau),
                # la partie claire fait partie du trait, la retirer le couperait
                fr[:] = False
            if fr.sum() > 3 * core.sum():
                # surtout du « liseré » autour d'un petit cœur : une tache floue (salissure), pas une
                # lettre ; on la laisse aux règles des formes molles
                fr[:] = False
            if fr.any():
                # liseré : on garde autant de pixels d'encre que sa couverture réelle (lumière conservée),
                # en partant des plus proches du cœur de la forme ; le reste rejoint le fond
                core = m & (sub == j)
                if core.any():
                    d = cv2.distanceTransform((~core).astype(np.uint8), cv2.DIST_L2, 3)
                else:
                    d = -cv2.distanceTransform(np.pad(m, 1).astype(np.uint8), cv2.DIST_L2, 3)[1:-1, 1:-1]
                ys, xs = np.nonzero(fr)
                o = np.argsort(d[ys, xs], kind='stable')
                nk = int(round(cov))
                sub[ys[o[:nk]], xs[o[:nk]]] = j
                sub[ys[o[nk:]], xs[o[nk:]]] = s


def unify_kin(lbl, pal, long_side, max_de=36.0, pad=0.015, padx=0.04, size=0.02, dom=2.5):
    """Un mot est imprimé d'une seule encre : une lettre (ou un morceau) d'une encre proche (brun très
    sombre au milieu d'un texte bleu nuit) entourée, à l'échelle d'une ligne, de beaucoup plus de
    l'autre encre, prend cette encre. Les encres franchement différentes ne sont jamais mêlées."""
    K = len(pal)
    H, W = lbl.shape
    pd = round(pad * long_side)
    px = round(padx * long_side)   # une ligne de texte s'étend en largeur
    lim = (size * long_side) ** 2
    # seules les petites formes (lettres) votent : un grand dessin voisin ne colore pas le texte
    small = np.zeros(lbl.shape, bool)
    for q in range(1, K):
        n, cc, st, _ = cv2.connectedComponentsWithStats((lbl == q).astype(np.uint8), connectivity=8)
        ok = np.r_[False, st[1:, cv2.CC_STAT_AREA] < lim]
        small |= ok[cc]
    for k in range(1, K):
        kin = [j for j in range(1, K) if j != k and np.linalg.norm(pal[k] - pal[j]) <= max_de]
        if not kin:
            continue
        n, cc, st, _ = cv2.connectedComponentsWithStats((lbl == k).astype(np.uint8), connectivity=8)
        for i in range(1, n):
            x, y, w, h, a = st[i]
            if a >= lim:
                continue
            x0, y0, x1, y1 = max(0, x - px), max(0, y - pd), min(W, x + w + px), min(H, y + h + pd)
            nb = np.bincount(lbl[y0:y1, x0:x1][small[y0:y1, x0:x1]], minlength=K)
            m = cc[y0:y1, x0:x1] == i
            ring = cv2.dilate(m.astype(np.uint8), np.ones((3, 3), np.uint8)).astype(bool) & ~m
            rc = np.bincount(lbl[y0:y1, x0:x1][ring], minlength=K)
            # seulement une encre que le morceau touche, et qui n'est pas ce qui l'entoure (sinon le
            # morceau disparaîtrait dans le fond coloré : accent, point d'un i)
            cand = [q for q in kin if rc[q] < 0.6 * rc.sum()]
            if not cand:
                continue
            j = max(cand, key=lambda q: nb[q])
            if nb[j] < dom * nb[k]:
                continue
            # jamais vers une encre qui se confond davantage avec ce qui entoure le morceau (le point
            # d'un i ne doit pas pâlir jusqu'à disparaître)
            sr = int(np.argmax(rc))
            if np.linalg.norm(pal[j] - pal[sr]) < 0.75 * np.linalg.norm(pal[k] - pal[sr]):
                continue
            # le morceau borde une forme d'une encre encore plus proche de la sienne (ombre rouge sombre
            # d'un dessin rouge) : il appartient à cette forme, pas au texte
            dj = np.linalg.norm(pal[k] - pal[j])
            if not any(q > 0 and q != k and q != j and rc[q] > 0 and np.linalg.norm(pal[k] - pal[q]) < dj for q in range(K)):
                lbl[y0:y1, x0:x1][m] = j


def drop_fringes(lbl, K, rho):
    """Liseré coloré (aberration de l'objectif) : une forme mince d'une encre, coincée entre le bord
    d'une autre forme et le fond. Elle est rendue à ses voisines (la plus proche de chaque point)."""
    H, W = lbl.shape
    kd = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * rho + 1, 2 * rho + 1))
    ker = np.ones((3, 3), np.uint8)
    bad = np.zeros((H, W), bool)
    comps = {}
    for k in range(1, K):
        mk = (lbl == k).astype(np.uint8)
        if mk.any():
            n, cc, st, _ = cv2.connectedComponentsWithStats(mk, connectivity=8)
            comps[k] = (cc, st[:, cv2.CC_STAT_AREA], cv2.morphologyEx(mk, cv2.MORPH_OPEN, kd))
    for k, (cc, area, thick) in comps.items():
        n = len(area)
        ys, xs = np.nonzero(cc)
        ids = cc[ys, xs]
        x0s = np.full(n, W); y0s = np.full(n, H); x1s = np.zeros(n, int); y1s = np.zeros(n, int)
        np.minimum.at(x0s, ids, xs); np.minimum.at(y0s, ids, ys)
        np.maximum.at(x1s, ids, xs); np.maximum.at(y1s, ids, ys)
        for i in range(1, n):
            x0, y0 = max(0, x0s[i] - 2), max(0, y0s[i] - 2)
            x1, y1 = min(W, x1s[i] + 3), min(H, y1s[i] + 3)
            m = cc[y0:y1, x0:x1] == i
            if thick[y0:y1, x0:x1][m].mean() > 0.2:
                continue
            ring = cv2.dilate(m.astype(np.uint8), ker).astype(bool) & ~m
            nb = np.bincount(lbl[y0:y1, x0:x1][ring], minlength=K).astype(float)
            nb[k] = 0
            tot = nb.sum()
            if tot == 0:
                continue
            j = int(np.argmax(nb[1:])) + 1
            if not (nb[0] / tot > 0.2 and nb[j] / tot > 0.08) or j not in comps:
                continue
            # le liseré est plus petit que la forme qu'il borde (sinon c'est lui la forme)
            ccj, areaj, _ = comps[j]
            touch = np.unique(ccj[y0:y1, x0:x1][ring])
            touch = touch[touch > 0]
            if area[i] < 0.5 * areaj[touch].sum():
                bad[y0:y1, x0:x1] |= m
    if bad.any():
        src = (~bad).astype(np.uint8)
        _, idx = cv2.distanceTransformWithLabels(src, cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
        ys, xs = np.nonzero(src)
        lut = np.zeros(idx.max() + 1, np.uint8)
        lut[idx[ys, xs]] = lbl[ys, xs]
        lbl[bad] = lut[idx[bad]]


def drop_mix_blobs(lbl, pal, long_side, max_side=0.004):
    """Tache de mélange : au creux d'une lettre (coin intérieur d'un E), le flou mélange l'encre et le
    fond ; si la page a une encre de cette couleur intermédiaire (rouge sombre entre le rouge du fond et
    le noir), une petite tache de cette encre apparaît dans la lettre. Une petite forme dont l'encre est
    un mélange du fond et d'une encre voisine, et qui touche les deux, est rendue à ses voisines."""
    K = len(pal)
    H, W = lbl.shape
    lin = lab_to_srgb(pal)
    lin = np.where(lin <= 0.04045, lin / 12.92, ((np.clip(lin, 0, 1) + 0.055) / 1.055) ** 2.4) * 100
    lim = (max_side * long_side) ** 2
    ker = np.ones((3, 3), np.uint8)
    bad = np.zeros((H, W), bool)
    for k in range(1, K):
        mixes = []
        for j in range(1, K):
            if j == k:
                continue
            v = lin[j] - lin[0]
            vv = max(float(v @ v), 1e-6)
            d = lin[k] - lin[0]
            t = float(d @ v) / vv
            perp = float(np.linalg.norm(d - t * v))
            if 0.15 < t < 0.85 and perp < 0.25 * np.sqrt(vv):
                mixes.append(j)
        if not mixes:
            continue
        n, cc, st, _ = cv2.connectedComponentsWithStats((lbl == k).astype(np.uint8), connectivity=8)
        for i in np.where(st[:, cv2.CC_STAT_AREA] < lim)[0]:
            if i == 0:
                continue
            x, y, w, h, a = st[i]
            x0, y0, x1, y1 = max(0, x - 2), max(0, y - 2), min(W, x + w + 2), min(H, y + h + 2)
            m = cc[y0:y1, x0:x1] == i
            ring = cv2.dilate(m.astype(np.uint8), ker).astype(bool) & ~m
            nb = np.bincount(lbl[y0:y1, x0:x1][ring], minlength=K).astype(float)
            tot = max(nb.sum(), 1)
            if nb[0] / tot < 0.1:
                continue
            if max(nb[j] for j in mixes) / tot >= 0.2 and (nb[0] + sum(nb[j] for j in mixes)) / tot > 0.9:
                bad[y0:y1, x0:x1] |= m
    if bad.any():
        src = (~bad).astype(np.uint8)
        _, idx = cv2.distanceTransformWithLabels(src, cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
        ys, xs = np.nonzero(src)
        lut = np.zeros(idx.max() + 1, np.uint8)
        lut[idx[ys, xs]] = lbl[ys, xs]
        lbl[bad] = lut[idx[bad]]


def recolor_thin(lbl, pal, lab, min_proj=3.0):
    """Un trait fin coloré (filet doré, signature au stylo bleu) sort souvent gris foncé sur la photo :
    l'appareil lisse la couleur plus que la luminosité (et accentue les bords). Le trait est alors pris
    pour du noir. Indice qui reste : sa teinte penche, même un peu, vers celle de l'encre colorée qu'il
    touche, alors qu'un mélange noir + fond n'a que la teinte (faible) du fond.
    Morceau d'encre neutre qui touche une encre colorée et penche nettement vers elle -> cette encre."""
    Hh, Wh = lbl.shape
    H, W = lab.shape[:2]
    ch = np.hypot(pal[:, 1], pal[:, 2])
    bg_ab, Lb = pal[0, 1:], pal[0, 0]
    col = [j for j in range(1, len(pal)) if ch[j] > 12]
    if not col:
        return
    for _ in range(3):   # un morceau recoloré peut en rapprocher un autre (trait coupé en plusieurs bouts)
        if not _recolor_pass(lbl, pal, lab, col, min_proj, H, W, Hh, Wh, Lb, bg_ab, ch):
            break


def _recolor_pass(lbl, pal, lab, col, min_proj, H, W, Hh, Wh, Lb, bg_ab, ch):
    changed = False
    # proche de l'encre colorée (même dessin : lettres d'un sceau autour de son anneau, devise sous un
    # emblème, bout effilé d'un filet) ; le texte courant, lui, ne penche vers aucune encre colorée
    R = 0.03 * max(Hh, Wh)
    dil = {j: cv2.distanceTransform((lbl != j).astype(np.uint8), cv2.DIST_L2, 3) <= R for j in col}
    # dans le cadre d'un petit dessin coloré (fils d'une balance, détails d'un emblème) : boîte d'un
    # morceau de cette encre, agrandie de 1 % ; les grands cadres (bordure de page) ne comptent pas
    box = {}
    mg = round(0.01 * max(Hh, Wh))
    for j in col:
        nj, _, sj, _ = cv2.connectedComponentsWithStats((lbl == j).astype(np.uint8), connectivity=8)
        b = np.zeros((Hh, Wh), bool)
        for x, y, w, h, a in sj[1:]:
            if a >= 0.0003 * Hh * Wh and w * h <= 0.03 * Hh * Wh:
                b[max(y - mg, 0):y + h + mg, max(x - mg, 0):x + w + mg] = True
        box[j] = b
    for k in range(1, len(pal)):
        if ch[k] > 8 or pal[k, 0] > Lb - 20:
            continue
        mk = lbl == k
        n, cc, st, _ = cv2.connectedComponentsWithStats(mk.astype(np.uint8), connectivity=8)
        ys, xs = np.nonzero(mk)
        c = cc[ys, xs]
        px = lab[np.minimum(ys * H // Hh, H - 1), np.minimum(xs * W // Wh, W - 1)]
        t = np.clip((Lb - px[:, 0]) / (Lb - pal[k, 0]), 0, 1)[:, None]
        ex = px[:, 1:] - (bg_ab * (1 - t) + pal[k, 1:] * t)   # teinte en trop par rapport au mélange
        cnt = np.maximum(np.bincount(c, minlength=n), 1)
        ea = np.bincount(c, ex[:, 0], minlength=n) / cnt
        eb = np.bincount(c, ex[:, 1], minlength=n) / cnt
        small = st[:, cv2.CC_STAT_AREA] < 0.002 * Hh * Wh
        # entouré de fond (pas un texte posé sur un aplat coloré)
        ccd = cv2.dilate(cc.astype(np.float32), np.ones((3, 3), np.uint8)).astype(np.int32)
        ring = (ccd > 0) & ~mk
        rc = ccd[ring]
        bgf = np.bincount(rc, lbl[ring] == 0, minlength=n) / np.maximum(np.bincount(rc, minlength=n), 1)
        # point le plus foncé de la photo sous le morceau (5e centile, par morceau)
        o = np.lexsort((px[:, 0], c))
        first = np.searchsorted(c[o], np.arange(n))
        dark = px[o, 0][np.minimum(first + (0.05 * (cnt - 1)).astype(int), len(o) - 1)] if len(o) else np.zeros(n)
        best = np.zeros(n, np.int32)
        bestp = np.full(n, min_proj)
        for j in col:
            u = pal[j, 1:] - bg_ab
            u = u / max(np.linalg.norm(u), 1e-3)
            proj = ea * u[0] + eb * u[1]
            adj = np.bincount(c, dil[j][ys, xs], minlength=n) > 0
            # encre peu colorée (bleu nuit) : une petite pente de teinte ne prouve rien, on exige plus
            ok = adj & small & (proj > bestp) & (proj > 80.0 / ch[j])
            # 2e indice, pour un trait si fin que sa teinte s'est perdue : il est dans le cadre d'un petit
            # dessin de cette encre, entouré de fond, et la photo n'y est jamais plus foncée que cette
            # encre ne peut l'être (un vrai trait noir, même fin, descend plus bas)
            inb = np.bincount(c, box[j][ys, xs], minlength=n) >= 0.9 * cnt
            ok2 = small & inb & (bgf > 0.6) & (dark > pal[j, 0] - 8) & (proj > 0.5) & (best == 0)
            best[ok] = j
            bestp[ok] = proj[ok]
            best[ok2] = j
        best[0] = 0
        if best.any():
            nl = best[c]
            sel = nl > 0
            lbl[ys[sel], xs[sel]] = nl[sel]
            changed = True
    return changed


def faint_marks(lbl, pal, lab, max_ratio=0.3, max_dp=20.0):
    """Trace pâle imprimée en encre foncée : pli du papier, rayure, poussière claire. Une encre foncée
    vient d'un endroit foncé de la photo ; si la photo, sous ce petit morceau, reste presque de la
    couleur du fond (écart < 30 % de celui de l'encre, et < 20 en clarté), ce n'est pas de l'encre.
    Le texte fin, même flou sur la photo, garde plus de 40 % de son contraste. Le morceau prend
    l'encre qui l'entoure."""
    Hh, Wh = lbl.shape
    L = max(Hh, Wh)
    Lu = cv2.resize(np.ascontiguousarray(lab[..., 0]), (Wh, Hh), interpolation=cv2.INTER_LINEAR)
    bgL = pal[0, 0]
    for j in range(1, len(pal)):
        dI = bgL - pal[j, 0]
        if dI < 15:
            continue
        n, cc, st, _ = cv2.connectedComponentsWithStats((lbl == j).astype(np.uint8), connectivity=8)
        for i in range(1, n):
            x, y, w, h, a = st[i]
            if a > (0.015 * L) ** 2:
                continue
            m = cc[y:y + h, x:x + w] == i
            dP = bgL - np.percentile(Lu[y:y + h, x:x + w][m], 3)
            if dP > max_dp or dP > max_ratio * dI:
                continue
            p = 3
            X0, Y0, X1, Y1 = max(x - p, 0), max(y - p, 0), min(x + w + p, Wh), min(y + h + p, Hh)
            mm = (cc[Y0:Y1, X0:X1] == i).astype(np.uint8)
            lb = lbl[Y0:Y1, X0:X1]
            ring = (cv2.dilate(mm, np.ones((5, 5), np.uint8)) > mm) & (lb != j)
            lb[mm > 0] = np.bincount(lb[ring], minlength=1).argmax() if ring.any() else 0


def lone_marks(lbl, pal, r=0.012, speck=6e-6, faint=60e-6, de_faint=35.0):
    """Marque seule sur le fond, sans autre encre à moins de 1,2 % de la page :
      - minuscule (moins de 6e-6 de la page, plus petit qu'un chiffre) : poussière, tache ;
      - petit point rond et plein (moins de 1,8e-5, isolé, loin de tout mot) : tache d'encre ou de
        saleté ; un point imprimé (point final, point du i) est toujours collé à un mot ;
      - petite (moins de 6e-5) et faite presque uniquement d'encres proches du fond : pli, rayure,
        reflet. Un vrai signe isolé (numéro de page, puce) est net et tranche sur le fond.
    Elle devient du fond."""
    Hh, Wh = lbl.shape
    L = max(Hh, Wh)
    ink = lbl != 0
    # deux encres à moins de r l'une de l'autre se touchent une fois grossies de r/2
    near = cv2.distanceTransform((~ink).astype(np.uint8), cv2.DIST_L2, 3) <= r * L / 2
    n, cc = cv2.connectedComponents(near.astype(np.uint8), connectivity=8)
    ys, xs = np.nonzero(ink)
    c = cc[ys, xs]
    de = np.linalg.norm(pal - pal[0], axis=1)
    area = np.bincount(c, minlength=n)
    strong = np.bincount(c, de[lbl[ys, xs]] > de_faint, minlength=n)
    x0 = np.full(n, 1 << 30); x1 = np.zeros(n, np.int64); y0 = np.full(n, 1 << 30); y1 = np.zeros(n, np.int64)
    np.minimum.at(x0, c, xs); np.maximum.at(x1, c, xs); np.minimum.at(y0, c, ys); np.maximum.at(y1, c, ys)
    bw, bh = np.maximum(x1 - x0 + 1, 1), np.maximum(y1 - y0 + 1, 1)
    dot = (area < 3 * speck * L * L) & (np.maximum(bw, bh) <= 2.5 * np.minimum(bw, bh)) & (area >= 0.5 * bw * bh)
    kill = (area < speck * L * L) | dot | ((area < faint * L * L) & (strong < 0.1 * area))
    kill[0] = False
    if os.environ.get('DBG'):
        for i in np.nonzero(kill)[0]:
            yy, xx = ys[c == i], xs[c == i]
            print("  marque seule x=%.3f y=%.3f aire=%.1fe-6 forte=%.2f" % (xx.mean() / Wh, yy.mean() / Hh,
                  area[i] / L ** 2 * 1e6, strong[i] / area[i]), file=sys.stderr)
    lbl[ys[kill[c]], xs[kill[c]]] = 0


def light_rims(lbl, pal, lab, max_thick=0.0007, max_ratio=0.75, min_bg=0.8):
    """Liseré clair : l'accentuation du téléphone dessine un fin trait plus clair que le papier le long
    des lettres foncées, et un pli de la couverture fait un reflet clair. Sur la photo ce trait est à
    peine plus clair que le papier, alors qu'une encre claire l'est franchement. Un morceau d'encre plus
    claire que le fond, très mince (au plus 0,07 % du grand côté d'épaisseur), entouré de fond et dont
    la photo n'atteint pas les trois quarts de l'éclat de cette encre, redevient du fond."""
    Hh, Wh = lbl.shape
    L = max(Hh, Wh)
    Lu = None
    bgL = pal[0, 0]
    for j in range(1, len(pal)):
        dI = pal[j, 0] - bgL
        if dI < 8:
            continue
        mj = (lbl == j).astype(np.uint8)
        n, cc, st, _ = cv2.connectedComponentsWithStats(mj, connectivity=8)
        if n < 2:
            continue
        if Lu is None:
            Lu = cv2.resize(np.ascontiguousarray(lab[..., 0]), (Wh, Hh), interpolation=cv2.INTER_LINEAR)
        dt = cv2.distanceTransform(mj, cv2.DIST_L2, 3)
        for i in range(1, n):
            x, y, w, h, a = st[i]
            p = 3
            X0, Y0, X1, Y1 = max(x - p, 0), max(y - p, 0), min(x + w + p, Wh), min(y + h + p, Hh)
            mm = (cc[Y0:Y1, X0:X1] == i).astype(np.uint8)
            if dt[Y0:Y1, X0:X1][mm > 0].max() > max_thick * L:
                continue
            if np.percentile(Lu[Y0:Y1, X0:X1][mm > 0], 97) - bgL > max_ratio * dI:
                continue
            lb = lbl[Y0:Y1, X0:X1]
            ring = (cv2.dilate(mm, np.ones((5, 5), np.uint8)) > mm)
            if (lb[ring] == 0).mean() < min_bg:
                continue
            lb[mm > 0] = 0


def edge_debris(lbl):
    """Débris au bord de la photo (coin abîmé, tranche, poussière de la table) : la page imprimée n'a
    rien collé à son bord. Deux cas, sur les étiquettes haute définition :
      - morceau qui touche le bord sans s'en éloigner de plus de 6 % ni être grand ;
      - petit morceau à moins de 2 % du bord, seul (aucune autre encre à moins de 3 %) : un vrai signe
        dans la marge (point, numéro) a toujours des voisins.
    Il prend l'encre qui l'entoure (le fond, en général)."""
    Hh, Wh = lbl.shape
    L = max(Hh, Wh)
    ink = (lbl != 0).astype(np.uint8)
    n, cc, st, _ = cv2.connectedComponentsWithStats(ink, connectivity=8)
    x, y, w, h, a = st[:, 0], st[:, 1], st[:, 2], st[:, 3], st[:, 4]
    bmin = np.minimum(np.minimum(x, y), np.minimum(Wh - x - w, Hh - y - h))
    touch = (bmin <= 0.004 * L) & (a <= 0.003 * L * L)
    near = (bmin <= 0.02 * L) & (a <= (0.012 * L) ** 2)
    cand = touch | near
    cand[0] = False
    if not cand.any():
        return
    other = ink.copy()
    other[cand[cc]] = 0
    dist = cv2.distanceTransform(1 - other, cv2.DIST_L2, 3)
    for i in np.nonzero(cand)[0]:
        x0, y0, x1, y1 = x[i], y[i], x[i] + w[i], y[i] + h[i]
        m = cc[y0:y1, x0:x1] == i
        yy, xx = np.nonzero(m)
        yy, xx = yy + y0, xx + x0
        dmax = np.minimum(np.minimum(xx, Wh - 1 - xx), np.minimum(yy, Hh - 1 - yy)).max()
        if touch[i] and dmax <= 0.06 * L:
            pass
        elif near[i] and dmax <= 0.02 * L and dist[yy, xx].min() > 0.03 * L:
            pass
        else:
            continue
        p = 4
        X0, Y0, X1, Y1 = max(x0 - p, 0), max(y0 - p, 0), min(x1 + p, Wh), min(y1 + p, Hh)
        mm = (cc[Y0:Y1, X0:X1] == i).astype(np.uint8)
        ring = (cv2.dilate(mm, np.ones((5, 5), np.uint8)) > mm) & (cc[Y0:Y1, X0:X1] != i)
        lb = lbl[Y0:Y1, X0:X1]
        fill = np.bincount(lb[ring], minlength=1).argmax() if ring.any() else 0
        if fill != 0 and (lb[ring] == 0).mean() > 0.3:
            fill = 0
        lb[mm > 0] = fill


def _spur_ids(diff, op, r, depth=1.3, area=2.5, ccs=None, thick=2.0):
    """Morceaux de diff (= forme moins son ouverture op) qui sont des dents du contour : collés à la
    forme ouverte, peu profonds, petits, et posés sur une forme épaisse (demi-épaisseur >= thick·r ;
    dans un petit texte, un « picot » de cette taille est un vrai détail de lettre, et un petit blanc
    est l'espace entre deux lettres). Renvoie un booléen par composante (0 = fond, faux)."""
    n, cc, st = ccs if ccs is not None else cv2.connectedComponentsWithStats(diff, connectivity=8)[:3]
    dist = cv2.distanceTransform(1 - op, cv2.DIST_L2, 3)
    inner = cv2.dilate(cv2.distanceTransform(op, cv2.DIST_L2, 3),
                       cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4 * r + 1, 4 * r + 1)))
    dmax = np.zeros(n, np.float32)
    dmin = np.full(n, 1e9, np.float32)
    tk = np.zeros(n, np.float32)
    ys, xs = np.nonzero(diff)
    ids = cc[ys, xs]
    np.maximum.at(dmax, ids, dist[ys, xs])
    np.minimum.at(dmin, ids, dist[ys, xs])
    np.maximum.at(tk, ids, inner[ys, xs])
    cand = (st[:, 4] <= area * r * r) & (dmax <= depth * r) & (dmin <= 1.5) & (tk >= thick * r)
    cand[0] = False
    return cand


def smooth_spurs(lbl, r, depth=1.3, area=2.5):
    """Picots et encoches sur les contours : la photo (bruit JPEG, grain du papier) laisse des pointes
    d'encre d'un ou deux pixels collées aux lettres, et des petites morsures dans leurs bords. Une vraie
    impression a des contours nets et réguliers. Pour chaque encre (fond compris, ce qui traite les
    encoches) : ce qu'une ouverture de rayon r enlève et qui reste collé à la forme, peu profond
    (< depth·r) et petit (< area·r²), est rendu à l'encre qui l'entoure. Un petit morceau détaché
    (point du i, contre-forme d'un e) n'est pas collé à la forme ouverte : il est gardé."""
    Hh, Wh = lbl.shape
    kd = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))
    k3 = np.ones((3, 3), np.uint8)
    snap = lbl.copy()
    for k in np.unique(snap):
        mk = (snap == k).astype(np.uint8)
        op = cv2.morphologyEx(mk, cv2.MORPH_OPEN, kd)
        diff = (mk > op).astype(np.uint8)
        if not diff.any():
            continue
        n, cc, st, _ = cv2.connectedComponentsWithStats(diff, connectivity=8)
        cand = _spur_ids(diff, op, r, depth, area, (n, cc, st))
        for i in np.nonzero(cand)[0]:
            x0, y0, w, h = st[i, :4]
            X0, Y0, X1, Y1 = max(x0 - 2, 0), max(y0 - 2, 0), min(x0 + w + 2, Wh), min(y0 + h + 2, Hh)
            m = (cc[Y0:Y1, X0:X1] == i).astype(np.uint8)
            sb = snap[Y0:Y1, X0:X1]
            ring = (cv2.dilate(m, k3) > 0) & (sb != k)
            if not ring.any():
                continue
            lbl[Y0:Y1, X0:X1][m > 0] = np.bincount(sb[ring]).argmax()


COV = os.environ.get('COV', 'clip')
_on = lambda n: n not in os.environ.get('SKIP', '').split(',')


def conserve_ink(tb, pa, pb, lin_s, pal_lin, K, lo=0.42, hi=float(os.environ.get('COVHI', 0.56))):
    """Épaisseur juste : le flou de l'objectif déplace la lumière mais n'en crée ni n'en détruit. Dans un
    petit carré, la quantité d'encre vue par la photo (somme des parts d'encre, en lumière linéaire) est
    donc égale à la surface vraiment imprimée. On place le seuil de chaque carré pour que la surface
    réimprimée soit cette quantité : ni lettres grasses (texte flou), ni lettres maigres.
    Seulement pour les bords encre/fond ; le seuil reste entre lo et hi (les traits fins gardent la règle
    des sommets)."""
    if COV == 'off':
        return tb
    H, W = tb.shape
    s = max(12, round(0.02 * max(H, W)))
    gy, gx = (H + s - 1) // s, (W + s - 1) // s
    out = tb.copy()
    for k in range(1, K):
        P = (pa == 0) & (pb == k)
        if P.sum() < 50:
            continue
        v = pal_lin[k] - pal_lin[0]
        t = ((lin_s - pal_lin[0]) @ v) / max(float(v @ v), 1e-6)
        t = np.clip(t, -0.3 if COV == 'raw' else 0.0, 1.0)
        th = np.full((gy, gx), 0.5, np.float32)
        wt = np.zeros((gy, gx), np.float32)
        for i in range(gy):
            for j in range(gx):
                sl = (slice(i * s, (i + 1) * s), slice(j * s, (j + 1) * s))
                p = P[sl]
                if p.sum() < 8:
                    continue
                vals = tb[sl][p]
                n_now = int((vals >= 0.5).sum())
                if n_now < 6:
                    continue
                target = int(round(float(t[sl][p].sum())))
                vs = np.sort(vals)[::-1]
                target = min(max(target, 1), len(vs))
                th[i, j] = np.clip(vs[target - 1], lo, hi)
                wt[i, j] = n_now
        if not wt.any():
            continue
        # seuil lissé d'un carré à l'autre (pondéré par la quantité d'encre)
        num = cv2.GaussianBlur(th * wt, (3, 3), 0.8)
        den = cv2.GaussianBlur(wt, (3, 3), 0.8)
        thm = np.where(den > 1e-3, num / np.maximum(den, 1e-3), 0.5).astype(np.float32)
        thm = cv2.resize(thm, (W, H), interpolation=cv2.INTER_LINEAR)
        out[P] = tb[P] - thm[P] + 0.5
    return out


PHOTO_MAX_PAPER = 0.3
PAPER_MAX_CHROMA, PAPER_MIN_L = 40.0, 55.0  # au-delà : fond imprimé (rouge, noir...), pas du papier


def page_mode(sel, bg=None):
    """Choix automatique du traitement, d'après l'IA 2 (tri) :
    - 'reprint' : une feuille (papier + encres) -> réimpression nette en aplats ;
    - 'photo'   : une page presque entièrement imprimée (couverture, affiche, photo) : pas de papier
                  à reconstruire, des dégradés et des reflets partout -> on garde l'image redressée
                  et on l'améliore seulement (couleurs, contraste, bruit, netteté).
    Un « papier » trop saturé ou trop sombre (bg, RGB 0-1) est un fond imprimé d'aplat -> 'photo'.
    -> (mode, part de papier)"""
    paper = float((sel[..., 0] > 0.6).mean())
    if bg is not None:
        L, a, b = srgb_to_lab(np.asarray(bg, np.float32).reshape(1, 1, 3))[0, 0]
        if np.hypot(a, b) > PAPER_MAX_CHROMA or L < PAPER_MIN_L:
            return 'photo', paper
    return ('photo' if paper < PHOTO_MAX_PAPER else 'reprint'), paper


def enhance_photo(ph, out_long=2400):
    """Mode photo : image redressée améliorée, sans réimpression.
    1. balance des blancs : le blanc le plus clair et peu coloré de la page (lettres blanches, bande
       blanche) sert de référence -> la teinte de la lampe ou du jour est retirée ;
    2. niveaux : noirs un peu plus profonds, blanc de référence remis à 96 % ;
    3. bruit du capteur retiré en gardant les bords, puis netteté douce."""
    ph = ph.astype(np.float32)
    p = ph.reshape(-1, 3)
    L = p.mean(1)
    sat = (p.max(1) - p.min(1)) / np.maximum(p.max(1), 1e-3)
    w = (L > np.quantile(L, 0.97)) & (sat < 0.3)
    gain = np.ones(3, np.float32)
    if w.sum() > 0.002 * len(p):
        ref = np.median(p[w], 0)
        gain = np.clip(0.96 / np.maximum(ref, 1e-3), 0.75, 1.5).astype(np.float32)
        print('  balance des blancs sur', (ref * 255).round().astype(int), flush=True)
    out = np.clip(ph * gain, 0, 1)
    lo = np.quantile(out.reshape(-1, 3), 0.003, axis=0)
    lo = np.minimum(lo, 0.12)
    out = np.clip((out - lo) / np.maximum(1 - lo, 1e-3), 0, 1)
    H, W = out.shape[:2]
    k = out_long / max(H, W)
    if k < 1:
        out = cv2.resize(out, (round(W * k), round(H * k)), interpolation=cv2.INTER_AREA)
    u8 = (out * 255 + 0.5).astype(np.uint8)
    u8 = cv2.fastNlMeansDenoisingColored(u8, None, 4, 4, 7, 21)
    out = u8.astype(np.float32) / 255
    if k > 1:
        out = cv2.resize(out, (round(W * k), round(H * k)), interpolation=cv2.INTER_CUBIC)
    blur = cv2.GaussianBlur(out, (0, 0), max(1.0, 0.0006 * out_long))
    out = np.clip(out + 0.6 * (out - blur), 0, 1)
    return out.astype(np.float32)


def reprint_over_photo(ph, sel, out_long=2400):
    """Réimpression partielle (pages entièrement imprimées : couvertures, affiches).
    Le fond reste la photo améliorée (dégradés, bandes, motifs) ; seuls les éléments nets
    (texte, carrés, logos) sont réimprimés par-dessus en couleur unie, à bord franc.
    En cas de doute (reflet, rayure, bord flou), l'élément n'est pas touché : la photo reste."""
    I = enhance_photo(ph, out_long)
    H, W = I.shape[:2]; L0 = max(H, W)
    lab = srgb_to_lab(I)
    # fond local : médiane large calculée en petit (les éléments fins disparaissent, les dégradés restent)
    s = 600 / L0
    Is = cv2.resize(I, (round(W * s), round(H * s)), interpolation=cv2.INTER_AREA)
    k = int(0.035 * 600) | 1
    Bs = np.dstack([cv2.medianBlur((Is[..., c] * 255).astype(np.uint8), k) for c in range(3)]).astype(np.float32) / 255
    B = cv2.resize(cv2.GaussianBlur(Bs, (0, 0), 2), (W, H), interpolation=cv2.INTER_CUBIC)
    D = np.linalg.norm(lab - srgb_to_lab(B), axis=-1)
    S = cv2.resize(sel, (W, H), interpolation=cv2.INTER_LINEAR)
    G = np.hypot(*np.gradient(cv2.GaussianBlur(D, (0, 0), 1)))
    n, cc, st, _ = cv2.connectedComponentsWithStats((D > 22).astype(np.uint8), connectivity=8)
    k3, k5, k15 = np.ones((3, 3), np.uint8), np.ones((5, 5), np.uint8), np.ones((15, 15), np.uint8)
    cands = []
    for i in range(1, n):
        x, y, w, h, a = st[i]
        if a < 1e-5 * H * W or max(w, h) > 0.12 * L0:
            continue
        sl = (slice(max(0, y - 9), y + h + 9), slice(max(0, x - 9), x + w + 9))
        m = cc[sl] == i; u = m.astype(np.uint8); d = D[sl][m]
        q90 = max(np.quantile(d, 0.9), 1e-3)
        rim = (cv2.dilate(u, k3) > 0) & ~(cv2.erode(u, k3) > 0)
        sharp = np.median(G[sl][rim]) / q90
        ring = (cv2.dilate(u, k15) > 0) & ~(cv2.dilate(u, k5) > 0) & (cc[sl] == 0)
        noise = np.median(D[sl][ring]) if ring.any() else 0
        p = S[sl][m].mean(0)
        solid = a / (w * h)
        thin, long_ = min(w, h), max(w, h)
        if p[4] > 0.15:          # l'IA 2 y voit un défaut (rayure, tache, bord)
            continue
        if thin < 0.005 * L0 and long_ > 2.5 * thin:   # trait très fin isolé : rayure probable
            continue
        if not (sharp >= 0.12 or (solid > 0.85 and sharp >= 0.06 and thin > 0.01 * L0)):
            continue             # bord progressif : reflet ou dessin flou, on garde la photo
        core = m & (D[sl] > np.quantile(d, 0.6))
        ink0 = np.median(I[sl][core], 0)
        cands.append(dict(i=i, sl=sl, ink0=ink0, a=a, lab=srgb_to_lab(ink0[None, None].astype(np.float32))[0, 0],
                          cx=x + w / 2, cy=y + h / 2, h=h, noise=noise, sharp=sharp, solid=solid))
    # lignes : éléments voisins de même taille et même encre (une ligne de texte, une rangée de carrés)
    par = list(range(len(cands)))
    def find(u):
        while par[u] != u:
            par[u] = par[par[u]]; u = par[u]
        return u
    for u, e in enumerate(cands):
        for v in range(u + 1, len(cands)):
            f = cands[v]
            if 0.75 < f['h'] / e['h'] < 1.33 and abs(f['cy'] - e['cy']) < 0.5 * e['h'] and abs(f['cx'] - e['cx']) < 2.5 * e['h'] \
               and np.linalg.norm(f['lab'] - e['lab']) < 25:
                par[find(u)] = find(v)
    lines = {}
    for u, e in enumerate(cands):
        lines.setdefault(find(u), []).append(e)
    # décision par ligne entière (plus sûre qu'une lettre seule) : une ligne nette sur fond calme est
    # réimprimée en entier ; une ligne sous un reflet (fond agité, bords mous) reste en photo.
    # Élément isolé : réimprimé seulement si le fond autour est calme et le bord franc (ou forme pleine :
    # carré, puce) ; un débris de reflet isolé a un bord mou et reste en photo.
    elems = []
    for ln in lines.values():
        if len(ln) >= 3:
            if np.median([e['noise'] for e in ln]) <= 9 and np.median([e['sharp'] for e in ln]) >= 0.17:
                elems += ln
        else:
            elems += [e for e in ln if e['noise'] <= 9 and (e['sharp'] >= 0.17 or e['solid'] > 0.85)]
    elems = [[e['i'], e['sl'], e['ink0'], e['a']] for e in elems]
    # palette commune : des encres proches (même blanc, même jaune) deviennent une seule couleur
    elems.sort(key=lambda e: -e[3])
    pal = []
    for e in elems:
        le = srgb_to_lab(e[2][None, None].astype(np.float32))[0, 0]
        for c in pal:
            if np.linalg.norm(le - c[0]) < 20:
                e.append(c); c[1] += e[3]; break
        else:
            c = [le, e[3]]; pal.append(c); e.append(c)
    inks = []
    for c in pal:
        L_, a_, b_ = c[0]
        if L_ > 75 and np.hypot(a_, b_) < 18:     # encre presque blanche -> blanc pur
            c[0] = np.array([100, 0, 0], np.float32)
        inks.append(np.clip(lab_to_srgb(c[0].astype(np.float32))[0], 0, 1))
    pal_id = {id(c): j for j, c in enumerate(pal)}
    alpha = np.zeros((H, W), np.float32); inkimg = np.zeros((H, W, 3), np.float32)
    for i, sl, ink0, a, c in elems:
        ink = inks[pal_id[id(c)]]
        m = cc[sl] == i
        Bl = B[sl]; v = ink0 - Bl
        t = ((I[sl] - Bl) * v).sum(-1) / np.maximum((v * v).sum(-1), 1e-4)
        reg = cv2.dilate(m.astype(np.uint8), k5) > 0
        t = np.where(reg, np.clip(t, 0, 1), 0)
        upd = t > alpha[sl]
        alpha[sl][upd] = t[upd]
        inkimg[sl][upd] = np.broadcast_to(ink, inkimg[sl].shape)[upd]
    print('  réimpression partielle :', len(elems), 'éléments,', len(pal), 'encres',
          [(c * 255).round().astype(int).tolist() for c in inks], flush=True)
    a = cv2.GaussianBlur(alpha, (0, 0), 0.8)
    a = np.clip((a - 0.3) / 0.4, 0, 1); a = (a * a * (3 - 2 * a))[..., None]
    zone = cv2.GaussianBlur((cv2.dilate((alpha > 0.05).astype(np.uint8), np.ones((7, 7), np.uint8)) > 0)
                            .astype(np.float32), (0, 0), 2)[..., None]
    out = (I * (1 - zone) + B * zone) * (1 - a) + inkimg * a
    return np.clip(out, 0, 1).astype(np.float32)


def reprint_clean(ph, sel, bg, gain, out_long=2400, tau=9.0, return_debug=False):
    """ph : photo redressée (H,W,3) sRGB 0..1 ; sel : probas IA 2 (h,w,5) ; bg : couleur du fond (avec gain).
    -> page réimprimée (out_long px sur le grand côté), palette sRGB."""
    import time
    t0 = time.time()
    tick = lambda msg: print(f'  {msg} {time.time() - t0:.1f}s', flush=True)
    H, W = ph.shape[:2]
    S = cv2.resize(sel, (W, H), interpolation=cv2.INTER_LINEAR)
    p_bg, p_img, p_def = S[..., 0], S[..., 3], S[..., 4]
    bg_raw = np.clip(bg / np.maximum(gain, 1e-3), 0, 1).astype(np.float32)

    # 1. éclairage aplati (2 passes : la 2e n'utilise que les points dont la couleur ressemble vraiment
    #    au fond, pour qu'une grande lettre prise pour du fond ne fausse pas l'éclairage)
    ph = ph.astype(np.float32)
    # Masque du fond indépendant de l'IA : même teinte que le fond (rapport r:g:b) et luminosité
    # dans un rapport 0,45..1,6 (ombre ou reflet), ce qu'une lettre blanche sur rouge ou un texte noir
    # ne sont jamais. L'IA 2 ne sert qu'à écarter les illustrations et les défauts.
    def like_bg(img, ref):
        s_i = img.sum(-1, keepdims=True) + 1e-3
        s_r = ref.sum() + 1e-3
        d = img / s_i - ref / s_r
        ratio = s_i[..., 0] / s_r
        # l'éclairage change surtout la saturation (on s'éloigne ou se rapproche du gris, dans la même
        # teinte) ; un aplat d'une autre couleur (rose sur un fond bleu) change la teinte : on tolère
        # beaucoup le premier, peu le second
        u = ref / s_r - 1 / 3
        nu = float(np.linalg.norm(u))
        if nu < 0.03:
            ok = np.linalg.norm(d, axis=-1) < 0.08
        else:
            u = u / nu
            along = d @ u
            perp = np.linalg.norm(d - along[..., None] * u, axis=-1)
            ok = (np.abs(along) < 0.12) & (perp < 0.045)
        return ok & (ratio > 0.45) & (ratio < 1.6)
    allow = like_bg(ph, bg_raw) & (p_img < 0.5) & (p_def < 0.5)
    flat = flatten_light(ph, allow, bg_raw)
    dE = np.linalg.norm(srgb_to_lab(np.clip(flat, 0, 1)) - srgb_to_lab(bg_raw[None, None])[0, 0], axis=-1)
    bgm = allow & (dE < 10)
    bg_lab0 = srgb_to_lab(bg_raw[None, None])[0, 0]
    # balance des blancs mesurée APRÈS l'aplatissement : un blanc de la page doit devenir blanc neutre
    labf = srgb_to_lab(np.clip(flat, 0, 1))
    chroma = np.hypot(labf[..., 1], labf[..., 2])
    wref = (~bgm) & (labf[..., 0] > max(55, bg_lab0[0] + 10)) & (chroma < 14) & (p_def < 0.3)
    if wref.sum() > max(50, 0.002 * wref.size):
        ref = np.median(flat[wref], 0)
        gain = np.clip(ref.max() / np.maximum(ref, 1e-3), 0.8, 1.4) * min(1.6, 0.97 / ref.max())
    else:
        gain = np.asarray(gain, np.float32)
    flat = np.clip(flat * gain, 0, 1).astype(np.float32)
    bg = np.clip(bg_raw * gain, 0, 1).astype(np.float32)
    tick('éclairage')
    # grain du carton / bruit du capteur : lissage qui respecte les bords
    u8 = (flat * 255 + 0.5).astype(np.uint8)
    flat_d = cv2.fastNlMeansDenoisingColored(u8, None, 4, 4, 5, 15).astype(np.float32) / 255
    lab = srgb_to_lab(flat_d)
    bg_lab = srgb_to_lab(bg[None, None].astype(np.float32))[0, 0]

    tick('débruitage')
    # 2. palette, apprise sur le cœur des formes (faible variation locale), hors illustrations et défauts
    g = cv2.morphologyEx(lab[..., 0], cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8))
    ga = cv2.morphologyEx(np.abs(lab[..., 1]) + np.abs(lab[..., 2]), cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8))
    core = (g < 6) & (ga < 8) & (p_img < 0.5) & (p_def < 0.5)
    dbg = np.linalg.norm(lab - bg_lab, axis=-1)
    far = dbg > 10
    # traits fins (texte courant) : ils n'ont pas de « cœur » plat ; leur couleur est lue sur la ligne
    # de crête (point le plus éloigné du fond dans son voisinage), là où le flou la délave le moins
    ridge = (dbg >= cv2.dilate(dbg, np.ones((3, 3), np.uint8)) - 0.5) & (dbg > 25) & (p_img < 0.5) & (p_def < 0.5)
    pal = find_palette(lab, (core & far) | ridge, bg_lab, merge=10.0)
    # encres presque neutres -> exactement neutres (blanc pur, noir pur, gris) ; les blancs crème
    # d'un papier glacé (reflet) comptent aussi pour du blanc
    ch = np.hypot(pal[:, 1], pal[:, 2])
    neutral = (ch < 6) | ((pal[:, 0] > 85) & (ch < 11))
    neutral[0] = False
    pal[neutral, 1:] = 0
    keep = [0]
    for i in range(1, len(pal)):
        if all(np.linalg.norm(pal[i] - pal[j]) >= 12 for j in keep):
            keep.append(i)
    pal = pal[keep]
    pal, mid = drop_mixtures(pal, lab, core & (p_img < 0.5))
    K = len(pal)
    # netteté locale : un vrai élément imprimé a un bord franc ; une ombre, une tache d'éclairage
    # ou un pli ont un bord mou
    gx = cv2.Sobel(cv2.GaussianBlur(lab, (0, 0), 0.6), cv2.CV_32F, 1, 0, ksize=3) / 8
    gy = cv2.Sobel(cv2.GaussianBlur(lab, (0, 0), 0.6), cv2.CV_32F, 0, 1, ksize=3) / 8
    G = np.sqrt((gx ** 2 + gy ** 2).sum(-1))  # ΔE par pixel photo
    Gmax = cv2.dilate(G, np.ones((5, 5), np.uint8))

    tick('palette')
    # 3. attribution d'encre en haute définition. Le rendu est fait à 2x puis réduit (bords anti-crénelés).
    sc = out_long / max(H, W)
    Wh, Hh = round(W * sc * 2), round(H * sc * 2)
    # Le bord d'une forme est là où la photo est à mi-chemin entre les deux encres, mesuré en lumière
    # linéaire (le flou de l'objectif mélange la lumière, pas les valeurs Lab) : sinon les lettres claires
    # grossissent et les sombres maigrissent. Le flou rend aussi les traits fins moins contrastés : on rend
    # un peu de contraste local avant de choisir l'encre (les petites lettres restent pleines).
    def to_lin(x):
        x = np.clip(x, 0, 1)
        return np.where(x <= 0.04045, x / 12.92, ((x + 0.055) / 1.055) ** 2.4).astype(np.float32)
    def from_lin(x):
        x = np.clip(x, 0, 1)
        return np.where(x <= 0.0031308, x * 12.92, 1.055 * x ** (1 / 2.4) - 0.055).astype(np.float32)
    pal_lin = to_lin(lab_to_srgb(pal)) * 100
    pal_lin[0] = to_lin(bg) * 100
    lin = cv2.GaussianBlur(to_lin(flat_d) * 100, (0, 0), 0.6)
    lin_s = lin.copy()
    # même point de vue que lin_s (flou en lumière linéaire) : sinon un trait fin sombre paraît plus
    # sombre en Lab qu'en linéaire et son encre est refusée
    lab_s = srgb_to_lab(from_lin(lin_s / 100))
    lin = lin + SHARP * (lin - cv2.GaussianBlur(lin, (0, 0), 1.5))
    # tolérance : bruit propre à chaque paire d'encres ~ 13 % de leur écart
    tau_l = max(3.0, 0.13 * np.median([np.linalg.norm(pal_lin[a] - pal_lin[b])
                                        for a in range(K) for b in range(a + 1, K)] or [30]))
    dEk = np.sqrt(((lab[..., None, :] - pal[None, None]) ** 2).sum(-1)).transpose(2, 0, 1)
    near = dEk.argmin(0)
    # défauts repérés par l'IA 2 (pli, reflet, tache) dans une zone sans bord net : la forme qui les
    # entoure continue à travers (fond sur le fond, blanc dans une lettre blanche)
    unknown = (p_def > 0.5) & (Gmax < 6)
    best = np.full((Hh, Wh), -1e9, np.float32)
    lbl = np.zeros((Hh, Wh), np.uint8)
    best_t = np.full((Hh, Wh), -1e9, np.float32)
    lbl_t = np.zeros((Hh, Wh), np.uint8)
    r = max(2, round(0.003 * max(H, W)))
    kr = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))
    # a) présence : où chaque encre a le droit d'apparaître
    owns = [np.ones((H, W), bool)]
    for k in range(1, K):
        if mid[k]:
            # encre intermédiaire (ex. encadré rouge sombre entre le rouge du fond et le noir) :
            # seulement près de son propre aplat, jamais en liseré autour d'un autre tracé
            own = cv2.dilate(((near == k) & core).astype(np.uint8), kr)
            own = cv2.dilate(cv2.erode(own, kr), kr)
        else:
            # le point s'explique comme un mélange (flou) de l'encre k et d'une autre encre, avec k
            # majoritaire : un trait fin délavé reste reconnu, un liseré blanc/rouge ne devient pas jaune
            match = np.zeros(lin_s.shape[:2], bool)
            for j in range(K):
                if j == k:
                    continue
                v = pal_lin[k] - pal_lin[j]
                vv = max(float(v @ v), 1e-6)
                d = lin_s - pal_lin[j]
                t = (d @ v) / vv
                perp = ((d - t[..., None] * v) ** 2).sum(-1)
                ok = (t > PRES) & (t < 1.3) & (perp < (0.15 * np.sqrt(vv) + 2) ** 2) & ~match
                if ok.any():
                    # contrôle de teinte en Lab (en lumière linéaire un gris et un or terne se ressemblent)
                    mix = pal_lin[j] + np.clip(t[ok], 0, 1)[:, None] * v
                    mlab = srgb_to_lab(from_lin(mix / 100)[None])[0]
                    # encre neutre (noir, gris) : l'arc-en-ciel de l'objectif teinte ses bords en jaune ou
                    # en bleu -> on ne contrôle que la clarté, la teinte sera tranchée par les voisins
                    if np.hypot(pal[k, 1], pal[k, 2]) < 3:
                        ok[ok] = np.abs(lab_s[ok, 0] - mlab[:, 0]) < 12
                    else:
                        ok[ok] = np.linalg.norm(lab_s[ok] - mlab, axis=-1) < 12
                    match |= ok
            match = match.astype(np.uint8)
            n_, cc_, st_, _ = cv2.connectedComponentsWithStats(match, connectivity=8)
            okc = st_[:, cv2.CC_STAT_AREA] >= 4
            okc[0] = False
            own = cv2.dilate(okc[cc_].astype(np.uint8), kr)
        owns.append(own.astype(bool))
    # b) chaque point est un mélange de DEUX encres (le bord flou entre elles) : la paire est choisie par
    #    la direction de la couleur (un gris pâle de texte fin est sur la droite noir–papier, pas sur
    #    or–papier), la part de chaque encre par la position sur la droite (lumière linéaire, avec un peu
    #    de netteté rendue). Le contour passe là où la part vaut 1/2.
    def pick_pairs(extra=None):
        best_r = np.full((H, W), np.inf, np.float32)
        pa = np.zeros((H, W), np.int32)
        pb = np.zeros((H, W), np.int32)
        tb = np.zeros((H, W), np.float32)
        for a_ in range(K):
            for b_ in range(a_ + 1, K):
                v = pal_lin[b_] - pal_lin[a_]
                vv = max(float(v @ v), 1e-6)
                t = np.clip(((lin_s - pal_lin[a_]) @ v) / vv, 0, 1)
                res = ((lin_s - pal_lin[a_] - t[..., None] * v) ** 2).sum(-1)
                if a_ > 0:
                    res = res + 9.0          # à égalité, un bord encre/fond est le cas le plus courant
                if extra is not None:
                    res = res + extra[a_] + extra[b_]
                res[~(owns[a_] & owns[b_])] = np.inf
                m = res < best_r
                best_r[m] = res[m]
                pa[m] = a_
                pb[m] = b_
                ts = np.clip(((lin - pal_lin[a_]) @ v) / vv, -0.5, 1.5)
                tb[m] = ts[m]
        return pa, pb, tb
    pa, pb, tb = pick_pairs()
    # c) une lettre est d'une seule encre : un point pâle (bord, trait fin) dont la couleur hésite entre
    #    deux encres sombres (noir / bleu foncé / or terne, à cause du léger arc-en-ciel de l'objectif)
    #    prend l'encre PLEINE qui domine autour de lui. S'il n'y a aucune encre pleine autour (vrai trait
    #    fin isolé), sa couleur seule décide.
    win = (4 * r + 1, 4 * r + 1)
    # poids d'un point = sa part d'encre ^4 : les points pleins (couleur sûre) comptent beaucoup plus que
    # les points pâles (couleur douteuse), sans ignorer les petites lettres qui n'ont presque rien de plein
    solid = [cv2.boxFilter(np.where((pb == k) & (pa == 0), np.clip(tb, 0, 1) ** 4, 0).astype(np.float32),
                           -1, win, normalize=False) for k in range(K)]
    solid[0] = np.zeros((H, W), np.float32)
    tot = np.maximum(sum(solid), 1e-6)
    has = sum(solid) >= 2
    extra = [np.zeros((H, W), np.float32)]
    for k in range(1, K):
        gap = float(np.linalg.norm(pal_lin[k] - pal_lin[0]))
        extra.append(np.where(has, (0.3 * gap) ** 2 * (1 - solid[k] / tot), 0).astype(np.float32))
    pa, pb, tb = pick_pairs(extra)
    # d) auréole : le flou et la netteté de l'appareil font « déborder » le passage fond -> encre claire
    #    du côté opposé (un liseré plus sombre que le fond sous une lettre blanche, ou plus clair autour
    #    d'un texte noir). Un point pâle de ce genre, collé à une forme d'une encre située de l'autre
    #    côté du fond, est du fond : on le rattache à la paire fond / cette forme.
    dom = np.where(tb >= 0.5, pb, pa)
    k5 = np.ones((5, 5), np.uint8)
    for k in range(1, K):
        vk = pal_lin[k] - pal_lin[0]
        vkk = max(float(vk @ vk), 1e-6)
        pale = (pa == 0) & (pb == k) & (((lin_s - pal_lin[0]) @ vk) / vkk < 0.5)
        if not pale.any():
            continue
        for j in range(1, K):
            vj = pal_lin[j] - pal_lin[0]
            if j == k or float(vj @ vk) >= 0:
                continue
            halo = pale & cv2.dilate(((dom == j) & (pa == 0)).astype(np.uint8), k5).astype(bool)
            if halo.any():
                vjj = max(float(vj @ vj), 1e-6)
                pb[halo] = j
                tb[halo] = np.clip(((lin[halo] - pal_lin[0]) @ vj) / vjj, -0.5, 1.5)
                pale &= ~halo
    if os.environ.get('DBG'):
        np.save(os.environ['DBG']+'/owns.npy', np.stack(owns)); np.save(os.environ['DBG']+'/lins.npy', lin_s); np.save(os.environ['DBG']+'/labs.npy', lab_s); np.save(os.environ['DBG']+'/pal.npy', np.stack([pal, pal_lin])); np.save(os.environ['DBG']+'/extra.npy', np.stack(extra))
    # trait fin : le flou l'étale et sa part ne monte jamais à 1/2 -> les barres de E, F, T se cassent.
    # Un point qui est un sommet (plus couvert que ses deux voisins dans une direction) d'un tracé
    # encre/fond assez marqué est compté comme encre : le trait reste continu, d'un pixel photo de large.
    tp = np.pad(tb, 1, mode='edge')
    ridge = np.zeros((H, W), bool)
    for dy, dx in ((0, 1), (1, 0), (1, 1), (1, -1)):
        n1 = tp[1 + dy:1 + dy + H, 1 + dx:1 + dx + W]
        n2 = tp[1 - dy:1 - dy + H, 1 - dx:1 - dx + W]
        ridge |= (tb >= n1) & (tb >= n2) & (tb - 0.5 * (n1 + n2) > 0.06)
    ridge &= (pa == 0) & (pb > 0) & (tb > RIDGE) & (tb < 0.5)
    # pas de grain isolé : le sommet doit toucher un tracé (sommets + points déjà encrés) d'au moins 4 px
    #    et contenir au moins quelques points vraiment encrés : un tracé fait seulement de sommets pâles,
    #    sans aucun point plein, est un pli ou une rayure du papier, pas de l'encre
    inked = (pa == 0) & (pb > 0) & (tb >= 0.5)
    rc = cv2.connectedComponentsWithStats((ridge | inked).astype(np.uint8), connectivity=8)
    n_ink = np.bincount(rc[1][inked], minlength=rc[0])
    ridge = ((rc[2][:, cv2.CC_STAT_AREA] >= 4) & (n_ink >= 3))[rc[1]] & ridge
    if os.environ.get('DBG'):
        np.save(os.environ['DBG']+'/tb.npy', tb); np.save(os.environ['DBG']+'/ridge.npy', ridge); np.save(os.environ['DBG']+'/pab.npy', np.stack([pa,pb]))
    tb = conserve_ink(tb, pa, pb, lin_s, pal_lin, K)
    tb = np.where(ridge, np.maximum(tb, 0.62), tb)
    dom_f =np.where(tb >= 0.5, pb, pa).astype(np.uint8)   # encre choisie, à la résolution de la photo
    soft = np.clip((tb - 0.5) / 0.5 + 0.5, 0, 1)   # rampe douce autour de 1/2 -> contours lisses
    for k in range(K):
        pk = np.where(pb == k, soft, 0) + np.where(pa == k, 1 - soft, 0)
        pk = pk.astype(np.float32)
        up = cv2.resize(pk, (Wh, Hh), interpolation=cv2.INTER_CUBIC)
        # deux lissages : léger (garde les traits fins du texte courant) et fort (contours bien lisses
        # des grandes formes)
        up_t = cv2.GaussianBlur(up, (0, 0), SMOOTH_THIN * sc * 2)
        m = up_t > best_t
        best_t[m] = up_t[m]
        lbl_t[m] = k
        up = cv2.GaussianBlur(up, (0, 0), SMOOTH * sc * 2)
        m = up > best
        best[m] = up[m]
        lbl[m] = k
    del best, best_t
    # partie mince d'une forme (trait, empattement, petit blanc entre deux lettres) : ce qu'une ouverture
    # de rayon ~1,2 px photo efface. Là, on garde le lissage léger, ailleurs le fort.
    rho = max(1, round(1.2 * sc * 2))
    kd = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * rho + 1, 2 * rho + 1))
    thin = np.zeros((Hh, Wh), bool)
    for k in np.unique(lbl_t):
        mk = (lbl_t == k).astype(np.uint8)
        op = cv2.morphologyEx(mk, cv2.MORPH_OPEN, kd)
        diff = (mk > op).astype(np.uint8)
        if not diff.any():
            continue
        # seuls les vrais traits fins comptent : les petites dents du contour (que l'ouverture enlève
        # aussi) doivent recevoir le lissage fort, sinon le bord des lettres reste en escalier
        bad = _spur_ids(diff, op, rho)
        n, cc = cv2.connectedComponents(diff, connectivity=8)
        thin |= (cc > 0) & ~bad[cc]
    thin = cv2.dilate(thin.astype(np.uint8), np.ones((3, 3), np.uint8)).astype(bool)
    if os.environ.get('DBG'):
        np.save(os.environ['DBG']+'/lblt.npy', lbl_t); np.save(os.environ['DBG']+'/thin.npy', thin)
    lbl = np.where(thin, lbl_t, lbl).astype(np.uint8)
    del lbl_t, thin

    tick('contours')
    # 4. nettoyage des formes
    #    - poussière : îlot d'encre minuscule posé sur le fond -> fond ;
    #    - défaut de remplissage : îlot d'une autre encre (ou petit trou) à l'intérieur d'une forme
    #      -> pris par l'encre qui l'entoure (une lettre est remplie d'une seule encre).
    if unknown.any():
        unk = cv2.resize(unknown.astype(np.uint8), (Wh, Hh), interpolation=cv2.INTER_NEAREST)
        _, idx = cv2.distanceTransformWithLabels(unk, cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
        ys, xs = np.nonzero(unk == 0)
        lut = np.zeros(idx.max() + 1, np.uint8)
        lut[idx[ys, xs]] = lbl[ys, xs]
        lbl = np.where(unk > 0, lut[idx], lbl).astype(np.uint8)
        del idx
    if os.environ.get('DBG'):
        np.save(os.environ['DBG']+'/lbl0.npy', lbl)
    if _on('merge_kin'): merge_kin(lbl, pal, max(Hh, Wh))
    if _on('unify_clusters'): unify_clusters(lbl, pal, max(Hh, Wh))
    if _on('unify_kin'): unify_kin(lbl, pal, max(Hh, Wh))
    if _on('drop_fringes'): drop_fringes(lbl, K, rho)
    if _on('drop_mix_blobs'): drop_mix_blobs(lbl, pal, max(Hh, Wh))
    if _on('clean_islands'): clean_islands(lbl, K, max(Hh, Wh), pal)
    if os.environ.get('DBG'):
        np.save(os.environ['DBG']+'/lbl1.npy', lbl)
    if _on('drop_soft_shapes'): drop_soft_shapes(lbl, pal, cv2.resize(G, (Wh, Hh), interpolation=cv2.INTER_LINEAR), 2 * sc)
    if _on('recolor_thin'): recolor_thin(lbl, pal, lab)
    if _on('faint_marks'): faint_marks(lbl, pal, lab)
    if _on('light_rims'): light_rims(lbl, pal, lab)
    if _on('edge_debris'): edge_debris(lbl)
    if _on('lone_marks'): lone_marks(lbl, pal)
    if _on('smooth_spurs'): smooth_spurs(lbl, rho)
    if os.environ.get('DBG'):
        np.save(os.environ['DBG']+'/lbl2.npy', lbl)
    tick('nettoyage')
    pal_rgb = lab_to_srgb(pal).astype(np.float32)
    pal_rgb[0] = bg
    out = pal_rgb[lbl]
    dom_v = cv2.resize(lbl, (W, H), interpolation=cv2.INTER_NEAREST)   # encres vraiment imprimées
    del lbl
    # 5. illustrations et objets hors page. On compare la photo à sa version « encres unies » : à
    #    l'intérieur d'une lettre ou d'un aplat l'écart est nul (une seule encre l'explique), dans une
    #    photo ou un dessin en dégradé il reste grand partout. Les bords entre encres sont ignorés (un bord
    #    mal placé d'un pixel n'est pas une illustration).
    labr = pal[dom_f]
    E = np.linalg.norm(cv2.GaussianBlur(labr, (0, 0), 2) - cv2.GaussianBlur(lab, (0, 0), 2), axis=-1)
    bd = np.zeros((H, W), np.uint8)
    bd[:, 1:] |= dom_f[:, 1:] != dom_f[:, :-1]
    bd[1:, :] |= dom_f[1:, :] != dom_f[:-1, :]
    inner = (cv2.dilate(bd, np.ones((5, 5), np.uint8)) == 0).astype(np.float32)
    sg = max(H, W) / 150
    dens = cv2.GaussianBlur(((E > 14) * inner).astype(np.float32), (0, 0), sg) / \
        np.maximum(cv2.GaussianBlur(inner, (0, 0), sg), 0.05)
    n, cc, st, _ = cv2.connectedComponentsWithStats((dens > 0.3).astype(np.uint8))
    mg = max(3, round(0.012 * max(H, W)))
    flat_up = None
    if os.environ.get('DBG'):
        np.save(os.environ['DBG']+'/dom.npy', dom_f); np.save(os.environ['DBG']+'/lab.npy', lab)
        np.save(os.environ['DBG']+'/dens.npy', dens)
    ill = np.zeros((H, W), np.float32)
    gone = np.zeros((H, W), np.uint8)
    for i in range(1, n):
        x, y, w, h, a = st[i]
        if a < 0.002 * H * W:
            # petite illustration très colorée (drapeau, logo) : gardée si elle est loin du bord
            m = cc == i
            vivid = np.median(np.hypot(lab[..., 1][m], lab[..., 2][m])) > 45
            if not (vivid and a > 0.0003 * H * W and x > mg and y > mg and x + w < W - mg and y + h < H - mg):
                continue
        m = (cc == i).astype(np.uint8)
        edge = x <= mg or y <= mg or x + w >= W - mg or y + h >= H - mg
        if edge and a < 0.08 * H * W:
            # objet qui entre par le bord de la photo (doigt, table, coin abîmé) : hors de la page.
            # On le recouvre de l'encre qui l'entoure (le fond, en général).
            m = cv2.dilate(m, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * mg + 1, 2 * mg + 1)))
            ring = cv2.dilate(m, np.ones((2 * mg + 1, 2 * mg + 1), np.uint8)) > m
            fill = np.bincount(dom_f[ring], minlength=K).argmax()
            mu = cv2.resize(cv2.GaussianBlur(m.astype(np.float32), (0, 0), 1.5), (Wh, Hh))[..., None]
            out = out * (1 - mu) + pal_rgb[fill] * mu
            gone |= m
            continue
        ill = np.maximum(ill, cv2.dilate(m, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * mg + 1,) * 2)))
    # objet étranger qui entre par le bord (doigt, pouce, coin de table, bout d'une autre feuille) en
    # aplat uni : l'IA ne le voit pas comme une illustration car il a une seule couleur. Il se trahit
    # par sa couleur : une encre qu'on ne trouve presque QUE dans des formes collées au bord. Une vraie
    # encre de la page (texte, cadre, bandeau) apparaît aussi à l'intérieur. Un bandeau imprimé à fond
    # perdu longe tout un côté : il est gardé.
    L0 = max(H, W)
    tb_ = max(2, round(0.004 * L0))
    text_ink = np.zeros(K, bool)
    text_ink[1:] = np.abs(pal[1:, 0] - pal[0, 0]) > 35   # encres bien contrastées (texte, traits)
    for k in range(1, K):
        mk = ((dom_f == k) & (gone == 0)).astype(np.uint8)
        tot = int(mk.sum())
        if tot < 0.0005 * H * W:
            continue
        nk, ck, sk, _ = cv2.connectedComponentsWithStats(mk, connectivity=8)
        x, y, w, h, a = sk[:, 0], sk[:, 1], sk[:, 2], sk[:, 3], sk[:, 4]
        tl, tt, tr, tbm = x <= tb_, y <= tb_, x + w >= W - tb_, y + h >= H - tb_
        touch = tl | tt | tr | tbm
        touch[0] = False
        if not touch.any() or a[touch].sum() < 0.8 * tot:
            continue
        # longueur de bord occupée : un doigt ou un coin n'en couvre qu'une partie
        span = np.maximum(np.where(tl | tr, h / H, 0), np.where(tt | tbm, w / W, 0))
        sel_ = touch & (a >= 0.0005 * H * W) & (span < 0.75)
        if not sel_.any():
            continue
        m0 = sel_[ck].astype(bool)
        # petite marge seulement (le liseré de l'objet) ; les lettres qui le touchent restent
        md = cv2.dilate(m0.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * tb_ + 1,) * 2)) > 0
        m = m0 | (md & ~text_ink[dom_f])
        # liseré de l'objet classé dans une encre foncée : petits morceaux presque entiers dans la marge
        md2 = cv2.dilate(m0.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4 * tb_ + 1,) * 2)) > 0
        nr, cr = cv2.connectedComponents(((dom_f != 0) & ~m).astype(np.uint8), connectivity=8)
        inside = np.bincount(cr[md2], minlength=nr) >= 0.9 * np.bincount(cr.ravel(), minlength=nr)
        inside[0] = False
        m = (m | inside[cr]).astype(np.uint8)
        ring = cv2.dilate(m, np.ones((2 * mg + 1, 2 * mg + 1), np.uint8)) > m
        fill = np.bincount(dom_f[ring & (dom_f != k)], minlength=K).argmax()
        mu = cv2.resize(cv2.GaussianBlur(m.astype(np.float32), (0, 0), 1.5), (Wh, Hh))[..., None]
        out = out * (1 - mu) + pal_rgb[fill] * mu
        gone |= m
        ill[m > 0] = 0
    # bandes collées au bord de la photo (table, ombre, tranche du papier) : un élément qui touche le
    # bord et ne s'en éloigne pas de plus de 4 % est hors de la page -> recouvert par l'encre voisine.
    # Les objets déjà recouverts ci-dessus (doigt) n'en font plus partie : le reste de la table sous le
    # doigt redevient une simple bande.
    band = max(4, round(0.04 * max(H, W)))
    n2, cc2 = cv2.connectedComponents(((dom_f != 0) & (gone == 0)).astype(np.uint8), connectivity=8)
    yy, xx = np.nonzero(cc2)
    c2 = cc2[yy, xx]
    db = np.minimum(np.minimum(xx, W - 1 - xx), np.minimum(yy, H - 1 - yy))   # distance au bord
    dmin = np.full(n2, 1 << 30)
    dmax = np.zeros(n2, np.int64)
    np.minimum.at(dmin, c2, db)
    np.maximum.at(dmax, c2, db)
    out_pg = (dmin <= max(2, round(0.004 * max(H, W)))) & (dmax <= band)
    out_pg[0] = False
    strip = out_pg[cc2].astype(np.uint8)
    if strip.any():
        strip = cv2.dilate(strip, np.ones((5, 5), np.uint8))
        ring = cv2.dilate(strip, np.ones((9, 9), np.uint8)) > strip
        fill = np.bincount(dom_f[ring], minlength=K).argmax()
        mu = cv2.resize(cv2.GaussianBlur(strip.astype(np.float32), (0, 0), 1), (Wh, Hh))[..., None]
        out = out * (1 - mu) + pal_rgb[fill] * mu
        gone |= strip
    # éclats perdus d'un aplat : une encre peu contrastée (aplat, pas du texte) dont la masse est un grand
    # bloc, mais qui laisse aussi de petits morceaux isolés loin de tout autre contenu (bord déchiré,
    # pli, reflet) -> ce ne sont pas des éléments imprimés, on les recouvre par le fond voisin.
    content = ((dom_v != 0) & (gone == 0)).astype(np.uint8)
    far = max(4, round(0.03 * L0))
    # zones « image » de l'IA 2 qui ne touchent pas le bord (une zone collée au bord = hors page, coin déchiré)
    n4, cc4, st4, _ = cv2.connectedComponentsWithStats((p_img > 0.5).astype(np.uint8), connectivity=8)
    x4, y4, w4, h4 = st4[:, 0], st4[:, 1], st4[:, 2], st4[:, 3]
    keep4 = (x4 > tb_) & (y4 > tb_) & (x4 + w4 < W - tb_) & (y4 + h4 < H - tb_)
    keep4[0] = False
    pic = keep4[cc4]
    faint = np.zeros(K, bool)
    faint[1:] = np.linalg.norm(pal[1:] - pal[0], axis=1) < 15
    for k in range(1, K):
        if text_ink[k]:
            continue
        mk = ((dom_v == k) & (gone == 0)).astype(np.uint8)
        nk, ck, sk, _ = cv2.connectedComponentsWithStats(mk, connectivity=8)
        if nk < 3:
            continue
        a = sk[:, 4].copy(); a[0] = 0
        if a.max() < 0.5 * a.sum():
            continue
        small = (a > 0) & (a < 0.02 * a.max()) & (a < 0.001 * H * W)
        # voisins valables : contenu bien visible (pas les autres éclats de cette encre, ni les encres
        # presque de la couleur du fond, qui ne sont que des plis ou des ombres)
        host = (content & ~small[ck] & ~faint[dom_v]) | (ill > 0) | pic   # photos : contenu aussi
        for i in np.nonzero(small)[0]:
            x, y, w, h = sk[i, :4]
            x0, y0, x1, y1 = max(0, x - far), max(0, y - far), min(W, x + w + far), min(H, y + h + far)
            me = (ck[y0:y1, x0:x1] == i).astype(np.uint8)
            near = cv2.dilate(me, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * far + 1,) * 2))
            if (host[y0:y1, x0:x1] & near).any():
                continue
            m = np.zeros((H, W), np.uint8)
            m[y0:y1, x0:x1] = cv2.dilate(me, np.ones((3, 3), np.uint8))
            mu = cv2.resize(cv2.GaussianBlur(m.astype(np.float32), (0, 0), 1), (Wh, Hh))[..., None]
            out = out * (1 - mu) + pal_rgb[0] * mu
            gone |= m
            content[m > 0] = 0
            host[m > 0] = 0
    if ill.any():
        # une illustration repérée par l'écart s'étend à toute la zone « image » de l'IA 2 qui la contient
        # (la rose, dont les tons sont proches d'une encre, suit la main et les feuilles)
        n3, cc3 = cv2.connectedComponents((p_img > 0.5).astype(np.uint8))
        hit = np.bincount(cc3[ill > 0], minlength=n3)
        tot3 = np.bincount(cc3.ravel(), minlength=n3)
        grow = (hit > 0.05 * (ill > 0).sum()) | (hit > 0.2 * tot3)
        grow[0] = False
        ill = np.maximum(ill, grow[cc3].astype(np.float32))
        # dans l'illustration, la photo corrigée est recollée ; les points qui ont déjà la couleur d'une
        # encre qui entoure l'illustration (l'aplat rose autour de la fleur, le fond) gardent l'encre unie,
        # avec un passage progressif (écart < 4 : encre, > 10 : photo)
        im8 = (ill > 0).astype(np.uint8)
        ring = cv2.dilate(im8, np.ones((2 * mg + 1, 2 * mg + 1), np.uint8)) > im8
        share = np.bincount(dom_f[ring], minlength=K) / max(ring.sum(), 1)
        keep_ink = np.nonzero(share > 0.1)[0]
        lab1 = cv2.GaussianBlur(lab, (0, 0), 1)
        resid = np.sqrt(((lab1[..., None, :] - pal[keep_ink][None, None]) ** 2).sum(-1).min(-1))
        w = np.clip((resid - 4) / 6, 0, 1)
        w = cv2.GaussianBlur(ill, (0, 0), sg / 2) * cv2.GaussianBlur(w, (0, 0), 1)
        img_m = cv2.resize(w, (Wh, Hh))[..., None]
        flat_up = cv2.resize(flat_d, (Wh, Hh), interpolation=cv2.INTER_CUBIC)
        out = out * (1 - img_m) + flat_up * img_m
    # 6. reliure : une colonne régulière de marques semblables, sur toute la hauteur d'un bord
    #    (anneaux de spirale, trous de perforation), n'est pas du contenu. Une ligne de texte près
    #    du bord est trop courte ou trop irrégulière pour passer ces tests ; un cadre est trop long.
    #    On compte aussi les marques déjà retirées par les règles d'avant, sinon la colonne a des trous.
    content = (dom_v != 0).astype(np.uint8)
    nb, cb, sb, cnb = cv2.connectedComponentsWithStats(content, connectivity=8)
    for side in ('l', 'r', 't', 'b'):
        if side in 'lr':
            pos = cnb[:, 0] / W; along = cnb[:, 1]; ln = sb[:, 3]; wd = sb[:, 2]; S, T = H, W
        else:
            pos = cnb[:, 1] / H; along = cnb[:, 0]; ln = sb[:, 2]; wd = sb[:, 3]; S, T = W, H
        inn = (pos < 0.06) if side in 'lt' else (pos > 0.94)
        cand = inn & (ln < 0.05 * S) & (wd < 0.06 * T) & (sb[:, 4] > 0.00002 * H * W)
        cand[0] = False
        idx = np.nonzero(cand)[0]
        if len(idx) < 6:
            continue
        idx = idx[np.argsort(along[idx])]
        a_ = along[idx]; L = max(1.0, float(np.median(ln[idx])))
        sp = np.diff(a_); ms = max(1.0, float(np.median(sp)))
        k = np.round(sp / ms)
        reg = np.mean((k >= 1) & (np.abs(sp - k * ms) < 0.3 * ms))  # espacement régulier
        ext = (a_[-1] - a_[0]) / S                                  # couvre presque tout le bord
        sim = np.median(np.abs(ln[idx] - L)) / L                    # marques de même taille
        if not (reg >= 0.7 and ext > 0.7 and sim < 0.25):
            continue
        m = np.isin(cb, idx).astype(np.uint8)
        m = cv2.dilate(m, np.ones((3, 3), np.uint8))
        mu = cv2.resize(cv2.GaussianBlur(m.astype(np.float32), (0, 0), 1), (Wh, Hh))[..., None]
        out = out * (1 - mu) + pal_rgb[0] * mu
        gone |= m
        print(f'  reliure ({side}) : {len(idx)} marques retirées', flush=True)
    # 7. aplats en dégradé (bandeau bleu qui pâlit) : la palette d'encres unies les découpe en taches.
    #    On les repère sur la photo débarrassée du texte (filtre médian) : une zone lisse, distincte du
    #    papier, grande. Un dégradé qui pâlit jusqu'au blanc se voit en morceaux : les morceaux qui se
    #    chevauchent forment un seul bandeau (enveloppe convexe). Dedans : le dégradé lissé de la photo,
    #    puis le texte réimprimé par-dessus avec sa propre encre (couverture mesurée sur la photo).
    kmed = int(0.012 * L0) | 1
    medf = cv2.medianBlur((np.clip(flat_d, 0, 1) * 255 + 0.5).astype(np.uint8), kmed).astype(np.float32) / 255
    labm = srgb_to_lab(medf)
    dpap = np.linalg.norm(labm - bg_lab, axis=-1)
    gm = np.linalg.norm(cv2.morphologyEx(labm, cv2.MORPH_GRADIENT, np.ones((5, 5), np.uint8)), axis=-1)
    pm = cv2.morphologyEx((dpap > 5).astype(np.uint8), cv2.MORPH_OPEN, np.ones((kmed, kmed), np.uint8))
    pm[(gone > 0) | (ill > 0)] = 0
    npn, cpn, spn, _ = cv2.connectedComponentsWithStats(pm)
    big = [i for i in range(1, npn) if spn[i, 4] > 0.006 * H * W]
    grp = {i: i for i in big}
    def root(i):
        while grp[i] != i: i = grp[i]
        return i
    for a_ in big:
        for b_ in big:
            if a_ < b_:
                xa, ya, wa, ha = spn[a_, :4]; xb, yb, wb, hb = spn[b_, :4]
                ox = min(xa + wa, xb + wb) - max(xa, xb); oy = min(ya + ha, yb + hb) - max(ya, yb)
                # deux morceaux d'un même bandeau : même bande horizontale (ou verticale), et qui se touchent
                if (oy > 0.5 * min(ha, hb) and ox > -0.02 * W) or (ox > 0.5 * min(wa, wb) and oy > -0.02 * H):
                    grp[root(b_)] = root(a_)
    panels = np.zeros((H, W), np.uint8)
    for r_ in {root(i) for i in big}:
        ids = [i for i in big if root(i) == r_]
        mg_ = np.isin(cpn, ids).astype(np.uint8)
        pts = cv2.findNonZero(mg_)
        hull = np.zeros((H, W), np.uint8); cv2.fillConvexPoly(hull, cv2.convexHull(pts), 1)
        x, y, w, h = cv2.boundingRect(pts)
        if hull.sum() < 0.012 * H * W or x <= tb_ or y <= tb_ or x + w >= W - tb_ or y + h >= H - tb_:
            continue
        inner_ = cv2.erode(hull, np.ones((kmed, kmed), np.uint8)) > 0
        if not inner_.any() or np.median(gm[inner_]) > 5 or mg_.sum() < 0.3 * hull.sum():
            continue   # trop texturé : une photo, pas un dégradé
        # un vrai dégradé : aucune encre unie ne le couvre seule (sinon la palette le rend déjà bien :
        # lettres claires sur fond de couleur, sceau doré, aplat uni), et sa forme est un rectangle
        cnt1 = np.bincount(dom_v[mg_ > 0].ravel())
        if cnt1.max() > 0.7 * cnt1.sum() or hull.sum() < 0.85 * w * h or (ill[y:y + h, x:x + w] > 0).mean() > 0.05:
            continue
        # le liseré du bandeau déborde parfois du dégradé détecté (côté pâle) : les traits fins juste
        # autour, entièrement dans cette marge, en font partie -> le bandeau s'étend jusqu'à eux
        rb = max(3, round(0.03 * L0))
        zone = cv2.dilate(hull, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * rb + 1,) * 2))
        y0, y1, x0, x1 = max(0, y - rb), min(H, y + h + rb), max(0, x - rb), min(W, x + w + rb)
        cnt_ = (((dom_v != 0) & (gone == 0) & (ill == 0))[y0:y1, x0:x1]).astype(np.uint8)
        nf, cf, sf, _ = cv2.connectedComponentsWithStats(cnt_, connectivity=8)
        ins = np.bincount(cf[zone[y0:y1, x0:x1] > 0], minlength=nf) == sf[:, 4]
        out_ = np.bincount(cf[hull[y0:y1, x0:x1] == 0], minlength=nf) > 0.5 * sf[:, 4]
        thin = np.minimum(sf[:, 2], sf[:, 3]) <= max(3, 0.006 * L0)
        fr = ins & out_ & thin
        fr[0] = False
        if fr.any():
            fy, fx = np.nonzero(fr[cf])
            pts = np.concatenate([pts.reshape(-1, 2), np.stack([fx + x0, fy + y0], 1)]).astype(np.int32)
        # un bandeau est un rectangle (coins arrondis) : son côté pâle se fond dans le papier sur la
        # photo, on le complète d'après les bords qu'on voit
        x, y, w, h = cv2.boundingRect(pts)
        rr = max(2, min(round(0.015 * L0), w // 4, h // 4))
        hull = np.zeros((H, W), np.uint8)
        cv2.rectangle(hull, (x + rr, y), (x + w - 1 - rr, y + h - 1), 1, -1)
        cv2.rectangle(hull, (x, y + rr), (x + w - 1, y + h - 1 - rr), 1, -1)
        for cx_, cy_ in ((x + rr, y + rr), (x + w - 1 - rr, y + rr), (x + rr, y + h - 1 - rr), (x + w - 1 - rr, y + h - 1 - rr)):
            cv2.circle(hull, (cx_, cy_), rr, 1, -1)
        panels |= cv2.dilate(hull, np.ones((kmed // 2 | 1, kmed // 2 | 1), np.uint8))   # inclut le liseré du bandeau
    if panels.any():
        pmask = panels > 0
        Lf = lab[..., 0]
        # texte = nettement plus sombre (ou plus clair) que le dégradé local
        dark = (np.abs(labm[..., 0] - Lf) > 12) & pmask
        # le dégradé : surface lisse (polynôme de degré 2) ajustée sur le fond du bandeau, sans le texte
        field = medf.copy()
        keep = pmask & ~cv2.dilate(dark.astype(np.uint8), np.ones((9, 9), np.uint8)).astype(bool)
        npz, cpz = cv2.connectedComponents(panels)
        for j in range(1, npz):
            mj = cpz == j
            yy, xx = np.nonzero(mj & keep)
            if len(xx) < 100:
                continue
            sel = np.linspace(0, len(xx) - 1, min(len(xx), 20000)).astype(int)
            xs, ys = xx[sel] / W, yy[sel] / H
            A = np.stack([np.ones_like(xs), xs, ys, xs * xs, xs * ys, ys * ys], 1)
            coef, *_ = np.linalg.lstsq(A, medf[yy[sel], xx[sel]], rcond=None)
            Y, X = np.nonzero(mj)
            xs, ys = X / W, Y / H
            smp = medf[yy[sel], xx[sel]]
            field[Y, X] = np.clip(np.stack([np.ones_like(xs), xs, ys, xs * xs, xs * ys, ys * ys], 1) @ coef,
                                  np.percentile(smp, 2, 0), np.percentile(smp, 98, 0))   # pas d'extrapolation folle
        field = np.clip(field, 0, 1)
        fL = srgb_to_lab(np.clip(field, 0, 1))[..., 0]
        # le texte, mesuré contre le dégradé lisse : l'intérieur des grosses lettres compte aussi
        dark = ((fL - Lf) > 12) & pmask
        # le liseré du bandeau (sur son pourtour) appartient au fond, pas au texte
        rim = pmask & ~(cv2.erode(panels, np.ones((kmed, kmed), np.uint8)) > 0)
        nd, cd_, sd_, _ = cv2.connectedComponentsWithStats(dark.astype(np.uint8))
        rim_n = np.bincount(cd_[rim], minlength=nd)
        dark &= ~np.isin(cd_, np.nonzero(rim_n > 0.3 * sd_[:, 4])[0][1:] if nd > 1 else [])
        # le texte d'un bandeau est imprimé avec l'encre la plus sombre de la page
        darkest = int(np.argmin(pal[:, 0]))
        cov = np.zeros((H, W), np.float32)
        inkc = np.zeros((H, W, 3), np.float32)
        nt, ct, stt, _ = cv2.connectedComponentsWithStats(cv2.dilate(dark.astype(np.uint8), np.ones((3, 3), np.uint8)))
        for j in range(1, nt):
            x, y, w, h = stt[j, :4]
            sl = (slice(y, y + h), slice(x, x + w)); mj = ct[sl] == j
            k = darkest
            fm = float(np.median(fL[sl][mj]))
            c = np.clip((fL[sl] - Lf[sl]) / max(1.0, fm - pal[k, 0]), 0, 1)
            cov[sl][mj] = c[mj]; inkc[sl][mj] = pal_rgb[k]
        up = lambda a: cv2.resize(a, (Wh, Hh), interpolation=cv2.INTER_CUBIC)
        cu = np.clip((up(cov) - 0.5) * 2.2 + 0.5, 0, 1)[..., None]     # bords nets mais lisses
        ink_up = cv2.resize(inkc, (Wh, Hh), interpolation=cv2.INTER_NEAREST)
        pan = up(field) * (1 - cu) + ink_up * cu
        pu = cv2.resize(cv2.GaussianBlur(panels.astype(np.float32), (0, 0), 1), (Wh, Hh))[..., None]
        out = out * (1 - pu) + pan * pu
        print(f'  dégradés : {cv2.connectedComponents(panels)[0] - 1} zone(s)', flush=True)
    # 8. contrôle avant impression : chaque morceau de contenu est vérifié, puis SEUL ce qui est
    #    validé est imprimé ; tout le reste de la page redevient papier.
    #    Près du bord de la feuille, deux choses ne sont pas du contenu :
    #    - un trait fin, clair, parallèle au bord (ombre de la tranche, pli de la couverture) ;
    #      un vrai cadre est foncé, il passe ;
    #    - une tache claire et clairsemée collée au bord (coin abîmé, déchirure).
    keep_ = ((dom_v != 0) & (gone == 0)).astype(np.uint8)
    nk, ck, sk, _ = cv2.connectedComponentsWithStats(keep_, connectivity=8)
    thin_px = max(3, 0.006 * L0)
    rej = np.zeros(nk, bool)
    for i in range(1, nk):
        x, y, w, h, a = sk[i]
        bd = min(x, y, W - x - w, H - y - h) / min(H, W)
        if bd > 0.09:
            continue
        sl = (slice(y, y + h), slice(x, x + w))
        inkL = float(np.median(pal[dom_v[sl][ck[sl] == i], 0]))
        if inkL < 60:
            continue                     # encre foncée : texte, cadre, logo -> gardé
        near_lr = min(x, W - x - w) / min(H, W) <= 0.09
        near_tb = min(y, H - y - h) / min(H, W) <= 0.09
        parallel = (near_lr and w <= thin_px and h > 3 * w) or (near_tb and h <= thin_px and w > 3 * h)
        sparse = bd < 0.02 and a < 0.2 * w * h and max(w, h) > 0.02 * L0
        if parallel or sparse:
            rej[i] = True
    if rej.any():
        m = rej[ck].astype(np.uint8)
        gone |= m
        print(f'  contrôle : {int(rej.sum())} morceau(x) hors contenu près du bord', flush=True)
    # le contenu validé : encres gardées, illustrations, bandeaux en dégradé
    kept = ((dom_v != 0) & (gone == 0)).astype(np.uint8)
    kept |= panels
    kept |= ((ill > 0) & (gone == 0)).astype(np.uint8)
    near = cv2.resize(cv2.dilate(kept, np.ones((5, 5), np.uint8)), (Wh, Hh), interpolation=cv2.INTER_NEAREST) > 0
    off = cv2.GaussianBlur((~near).astype(np.float32), (0, 0), 1)[..., None]
    out = out * (1 - off) + pal_rgb[0] * off
    if os.environ.get('DBG'):
        np.save(os.environ['DBG'] + '/final_dom.npy', dom_v); np.save(os.environ['DBG'] + '/final_gone.npy', gone)
        np.save(os.environ['DBG'] + '/final_ill.npy', ill); np.save(os.environ['DBG'] + '/final_pal.npy', pal)
    # 9. papier presque blanc (blanc cassé, grisé ou crème léger) -> blanc de photocopie pur.
    #    Toute la page est recalée d'un même facteur : le papier devient blanc exact, les encres et
    #    les illustrations gardent leurs écarts. Un vrai papier de couleur (beige, rouge…) est gardé.
    pL, pa_, pb_ = srgb_to_lab(pal_rgb[0][None, None].astype(np.float32))[0, 0]
    if pL > 80 and np.hypot(pa_, pb_) < 8:
        wgain = 1.0 / np.maximum(pal_rgb[0], 1e-3)
        out = np.clip(out * wgain, 0, 1)
        pal_rgb = np.clip(pal_rgb * wgain, 0, 1)
        bg = np.ones(3, np.float32)
        print('  papier blanc : fond mis en blanc pur', flush=True)
    out = cv2.resize(out.astype(np.float32), (Wh // 2, Hh // 2), interpolation=cv2.INTER_AREA)
    if return_debug:
        return out, pal_rgb, bg, flat_d
    return out, pal_rgb, bg
