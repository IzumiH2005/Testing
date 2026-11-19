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
            if n < max(25, 0.0015 * len(pts)):
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


def clean_islands(lbl, K, long_side):
    dust = (0.0012 * long_side) ** 2      # plus petit qu'un point de ponctuation
    blob = (0.004 * long_side) ** 2       # taille max d'un défaut de remplissage dans une forme
    hole = (0.0009 * long_side) ** 2      # trou de fond dans une forme : seulement minuscule (on garde les « o »)
    H, W = lbl.shape
    ker = np.ones((3, 3), np.uint8)
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
            elif j != 0 and frac > 0.8:        # enfermé dans une forme d'une seule encre
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
            ink = nb[1:].sum()
            if ink == 0:
                continue
            j = int(np.argmax(nb[1:])) + 1
            # on ne va que vers l'encre la plus présente de la page : jamais un bout de noir vers le bleu
            if nb[j] / ink < 0.8 or nb[j] / nb.sum() < 0.08 or j not in areas or tot[j] < tot[k]:
                continue
            if np.linalg.norm(pal[k] - pal[j]) > max_de:
                continue
            ccj, stj = areas[j][1], areas[j][2]
            touch = np.unique(ccj[y0:y1, x0:x1][ring])
            touch = touch[touch > 0]
            if a < 0.5 * stj[touch, cv2.CC_STAT_AREA].sum():
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
    tb = np.where(ridge, 0.62, tb)
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
        thin |= (mk > cv2.morphologyEx(mk, cv2.MORPH_OPEN, kd))
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
    merge_kin(lbl, pal, max(Hh, Wh))
    drop_fringes(lbl, K, rho)
    clean_islands(lbl, K, max(Hh, Wh))
    if os.environ.get('DBG'):
        np.save(os.environ['DBG']+'/lbl1.npy', lbl)
    drop_soft_shapes(lbl, pal, cv2.resize(G, (Wh, Hh), interpolation=cv2.INTER_LINEAR), 2 * sc)
    tick('nettoyage')
    pal_rgb = lab_to_srgb(pal).astype(np.float32)
    pal_rgb[0] = bg
    out = pal_rgb[lbl]
    del lbl
    # 5. illustrations : seulement là où les encres unies n'expliquent pas la photo (dégradés, photos),
    #    sur une zone assez grande ; la photo corrigée y est recollée avec un bord doux
    lab_b = cv2.GaussianBlur(lab, (0, 0), 1.5)
    resid = np.sqrt(((lab_b[..., None, :] - pal[None, None]) ** 2).sum(-1).min(-1))
    ill = (resid > 12).astype(np.uint8)
    kk = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))
    ill = cv2.morphologyEx(ill, cv2.MORPH_OPEN, kk)            # les bords de lettres (minces) partent
    ill = cv2.morphologyEx(ill, cv2.MORPH_CLOSE, kk)
    n, cc, st, _ = cv2.connectedComponentsWithStats(ill)
    big = np.zeros(n, bool)
    big[1:] = st[1:, cv2.CC_STAT_AREA] > 0.004 * H * W
    ill = big[cc] & (p_img > 0.3)
    if ill.any():
        img_m = cv2.resize(cv2.GaussianBlur(ill.astype(np.float32), (0, 0), 2), (Wh, Hh))
        flat_up = cv2.resize(flat_d, (Wh, Hh), interpolation=cv2.INTER_CUBIC)
        out = out * (1 - img_m[..., None]) + flat_up * img_m[..., None]
    out = cv2.resize(out.astype(np.float32), (Wh // 2, Hh // 2), interpolation=cv2.INTER_AREA)
    if return_debug:
        return out, pal_rgb, bg, flat_d
    return out, pal_rgb, bg
