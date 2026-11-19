"""Générateur de données d'entraînement.

1. Fabrique une page PROPRE dont on connaît tout : couleur du papier, quantité de chaque encre
   en chaque point, et la nature de chaque point (papier, texte, aplat, image).
2. La « photographie » comme le ferait un téléphone : éclairage inégal et teinté, ombres, plis,
   taches, usure, doigts, bout de table, grain, flou, bruit, compression JPEG.
Les réseaux apprennent ensuite le chemin inverse : photo -> page propre.
"""
import glob
import io
import math
import os

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from common import lin2srgb, print_np, render_np, rip, srgb2lin

# ---------------------------------------------------------------- ressources
_FONTS = None


def fonts():
    global _FONTS
    if _FONTS is None:
        pats = ["/usr/share/fonts/truetype/**/*.ttf", "/usr/share/fonts/opentype/inter/*.otf"]
        fl = []
        for p in pats:
            fl += glob.glob(p, recursive=True)
        bad = ("emoji", "ipa", "wqy", "loma", "unifont", "noto", "lohit", "kacst", "mathjax")
        fl = [f for f in fl if not any(b in f.lower() for b in bad)]
        ok = []
        for f in sorted(fl):
            try:
                ImageFont.truetype(f, 20).getbbox("Aéx")
                ok.append(f)
            except Exception:
                pass
        _FONTS = ok
    return _FONTS


_PHOTOS = None


def photos():
    """Quelques vraies photos libres fournies avec scikit-image (pour la classe « image »)."""
    global _PHOTOS
    if _PHOTOS is None:
        _PHOTOS = []
        try:
            import skimage.data as d
            for n in ["astronaut", "coffee", "chelsea", "rocket", "immunohistochemistry",
                      "hubble_deep_field", "retina", "colorwheel", "cat"]:
                im = getattr(d, n)()
                if im.ndim == 3 and im.shape[2] >= 3:
                    _PHOTOS.append(np.ascontiguousarray(im[..., :3]))
        except Exception:
            pass
    return _PHOTOS


SYL = ("la le de ma mo ri re tu pa po vi ve sa si ne no ta te on an en in ou ai eu oi au "
       "che cha tion ment bre gra pre tre fleu mal lu ver ser ten sor cou mon dis par ment "
       "é è ê à ç ée és ère ance able eur ique elle").split()


def word(rng):
    n = rng.integers(1, 5)
    w = "".join(rng.choice(SYL) for _ in range(n))
    r = rng.random()
    if r < 0.12:
        w = w.capitalize()
    elif r < 0.16:
        w = w.upper()
    elif r < 0.22:
        w = str(rng.integers(1, 3000))
    if rng.random() < 0.1:
        w += rng.choice([",", ".", ";", ":", " -", "!", "?", "'"])
    return w


def sentence(rng, nwords):
    return " ".join(word(rng) for _ in range(nwords))


# ---------------------------------------------------------------- bruit lisse
def smooth_noise(rng, H, W, cells):
    g = rng.random((max(2, int(cells * H / max(H, W))) + 1, max(2, int(cells * W / max(H, W))) + 1))
    return cv2.resize(g.astype(np.float32), (W, H), interpolation=cv2.INTER_CUBIC)


def fractal(rng, H, W, octaves=4, base=3):
    out = np.zeros((H, W), np.float32)
    amp, tot = 1.0, 0.0
    for o in range(octaves):
        out += amp * smooth_noise(rng, H, W, base * 2 ** o)
        tot += amp
        amp *= 0.5
    out /= tot
    out -= out.min()
    return out / (out.max() + 1e-6)


# ---------------------------------------------------------------- couleurs
def rand_ink_color(rng, kind="any"):
    """Couleur d'encre tirée dans l'espace des encres (donc imprimable) -> transmission lin."""
    r = rng.random()
    if kind == "text" and r < 0.7 or kind == "black":
        cov = np.array([0, 0, 0, rng.uniform(0.85, 1.0)])
        if rng.random() < 0.3:
            cov[:3] = rng.uniform(0, 0.5, 3)
    elif kind == "pale":
        cov = rng.uniform(0, 0.35, 4) * (rng.random(4) < 0.6)
        cov[3] *= 0.3
    else:
        cov = rng.uniform(0, 1, 4) * (rng.random(4) < 0.55)
        if rng.random() < 0.5:  # couleurs franches : 1 ou 2 encres fortes
            cov = np.zeros(4)
            idx = rng.choice(3, size=rng.integers(1, 3), replace=False)
            cov[idx] = rng.uniform(0.5, 1.0, len(idx))
        cov[3] *= 0.6
    return render_np(cov.astype(np.float32)[None])[0]


def rand_paper(rng):
    """Couleur du papier (sRGB 0..1)."""
    r = rng.random()
    if r < 0.6:    # blanc ou presque (le cas le plus courant)
        v = rng.uniform(0.92, 1.0)
        return np.clip(v + rng.normal(0, 0.012, 3), 0, 1).astype(np.float32)
    import colorsys
    h = rng.random()
    if r < 0.88:   # pastel : rose clair, crème, bleu pâle...
        s, l = rng.uniform(0.15, 0.75), rng.uniform(0.8, 0.95)
    else:          # papier coloré franc ou foncé (couvertures)
        s, l = rng.uniform(0.2, 0.8), rng.uniform(0.25, 0.8)
    return np.array(colorsys.hls_to_rgb(h, l, s), np.float32)


# ---------------------------------------------------------------- page propre
class Page:
    def __init__(self, rng, H, W):
        self.rng, self.H, self.W = rng, H, W
        self.t = np.ones((H, W, 3), np.float32)       # transmission voulue (avant le RIP)
        self.cls = np.zeros((H, W), np.uint8)          # 0 papier 1 texte/trait 2 aplat 3 image
        self.w = np.zeros((H, W), np.float32)          # encre blanche couvrante
        self.bleed = False                             # fond coloré sur toute la page

    def put(self, alpha, col, cls, white=None):
        a = alpha[..., None]
        if np.ndim(col) == 1:
            col = np.asarray(col, np.float32)
            if white is None:  # du blanc sur un fond coloré : il faut l'encre blanche
                white = self.bleed and bool(np.all(col >= 0.999))
            col = col[None, None]
        if white:
            self.w = self.w * (1 - alpha) + alpha
        self.t = self.t * (1 - a) + col * a
        self.cls[alpha > 0.5] = cls

    # -- formes
    def shape_mask(self, x0, y0, x1, y1, kind=None):
        rng = self.rng
        m = np.zeros((self.H, self.W), np.uint8)
        kind = kind or rng.choice(["rect", "round", "ellipse", "leaf", "poly", "band"])
        x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
        if kind == "rect" or kind == "band":
            cv2.rectangle(m, (x0, y0), (x1, y1), 255, -1)
        elif kind == "ellipse":
            cv2.ellipse(m, ((x0 + x1) // 2, (y0 + y1) // 2), (max(1, (x1 - x0) // 2), max(1, (y1 - y0) // 2)), 0, 0, 360, 255, -1)
        elif kind in ("round", "leaf"):
            r = int(min(x1 - x0, y1 - y0) * rng.uniform(0.05, 0.5))
            cv2.rectangle(m, (x0, y0), (x1, y1), 255, -1)
            corners = [(x0, y0, 1, 1), (x1, y0, -1, 1), (x1, y1, -1, -1), (x0, y1, 1, -1)]
            sel = [0, 2] if kind == "leaf" else [0, 1, 2, 3]
            for i in sel:
                cx, cy, dx, dy = corners[i]
                cv2.rectangle(m, (min(cx, cx + dx * r), min(cy, cy + dy * r)),
                              (max(cx, cx + dx * r), max(cy, cy + dy * r)), 0, -1)
                cv2.circle(m, (cx + dx * r, cy + dy * r), r, 255, -1)
        else:
            n = rng.integers(3, 8)
            cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
            ang = np.sort(rng.uniform(0, 2 * np.pi, n))
            pts = np.stack([cx + (x1 - x0) / 2 * np.cos(ang) * rng.uniform(0.6, 1, n),
                            cy + (y1 - y0) / 2 * np.sin(ang) * rng.uniform(0.6, 1, n)], 1)
            cv2.fillPoly(m, [pts.astype(np.int32)], 255)
        m = cv2.GaussianBlur(m, (3, 3), 0.6)
        return m.astype(np.float32) / 255

    # -- texte
    def text(self, x, y, txt, size, col, font=None, angle=0.0, cls=1):
        rng = self.rng
        font = font or rng.choice(fonts())
        f = ImageFont.truetype(font, max(6, int(size)))
        bb = f.getbbox(txt)
        w, h = bb[2] - bb[0] + 4, bb[3] - bb[1] + 4
        if w <= 4 or h <= 4:
            return 0, 0
        im = Image.new("L", (w, h), 0)
        ImageDraw.Draw(im).text((2 - bb[0], 2 - bb[1]), txt, font=f, fill=255)
        if angle:
            im = im.rotate(angle, resample=Image.BICUBIC, expand=True)
        a = np.asarray(im, np.float32) / 255
        hh, ww = a.shape
        x, y = int(x), int(y)
        X0, Y0, X1, Y1 = max(0, x), max(0, y), min(self.W, x + ww), min(self.H, y + hh)
        if X1 <= X0 or Y1 <= Y0:
            return ww, hh
        full = np.zeros((self.H, self.W), np.float32)
        full[Y0:Y1, X0:X1] = a[Y0 - y:Y1 - y, X0 - x:X1 - x]
        self.put(full, col, cls)
        return ww, hh

    def paragraph(self, x, y, width, size, col, nlines, font=None, lead=1.35, align="left"):
        rng = self.rng
        font = font or rng.choice(fonts())
        f = ImageFont.truetype(font, max(6, int(size)))
        for li in range(nlines):
            if y > self.H:
                break
            words, cur = [], ""
            while True:
                w = word(self.rng)
                test = (cur + " " + w).strip()
                if f.getlength(test) > width:
                    break
                cur = test
                if li == nlines - 1 and rng.random() < 0.25:
                    break
            if not cur:
                break
            dx = 0
            if align == "center":
                dx = (width - f.getlength(cur)) / 2
            elif align == "right":
                dx = width - f.getlength(cur)
            self.text(x + dx, y, cur, size, col, font)
            y += size * lead
        return y

    # -- images
    def image_fill(self, H, W):
        rng = self.rng
        P = photos()
        if P and rng.random() < 0.4:
            src = P[rng.integers(len(P))]
            sh, sw = src.shape[:2]
            s = max(H / sh, W / sw) * rng.uniform(1.0, 2.0)
            im = cv2.resize(src, (max(W, int(sw * s)), max(H, int(sh * s))), interpolation=cv2.INTER_AREA)
            oy, ox = rng.integers(0, im.shape[0] - H + 1), rng.integers(0, im.shape[1] - W + 1)
            im = im[oy:oy + H, ox:ox + W].astype(np.float32) / 255
            if rng.random() < 0.5:
                im = im[:, ::-1]
            return srgb2lin(im)
        return self.illustration(H, W)[0]

    def illustration(self, H, W, transparent=False):
        """Illustration procédurale : fond nuancé, objets ombrés (fleurs, feuilles), traits gravés."""
        rng = self.rng
        k = rng.integers(3, 6)
        pal = np.stack([rand_ink_color(rng) for _ in range(k)])
        n = fractal(rng, H, W, 4, rng.uniform(2, 6))
        idx = n * (k - 1)
        i0 = np.floor(idx).astype(int).clip(0, k - 2)
        fr = (idx - i0)[..., None]
        img = pal[i0] * (1 - fr) + pal[i0 + 1] * fr
        alpha = np.ones((H, W), np.float32) if not transparent else np.zeros((H, W), np.float32)
        nobj = rng.integers(2, 9)
        for _ in range(nobj):
            col = rand_ink_color(rng)
            cx, cy = rng.uniform(0, W), rng.uniform(0, H)
            rx, ry = rng.uniform(0.04, 0.3) * W, rng.uniform(0.04, 0.3) * H
            m = np.zeros((H, W), np.uint8)
            if rng.random() < 0.5:
                cv2.ellipse(m, (int(cx), int(cy)), (int(rx), int(ry)), rng.uniform(0, 180), 0, 360, 255, -1)
            else:  # pétales / feuilles
                for p in range(rng.integers(3, 8)):
                    a = rng.uniform(0, 2 * np.pi)
                    cv2.ellipse(m, (int(cx + rx * 0.5 * np.cos(a)), int(cy + ry * 0.5 * np.sin(a))),
                                (int(rx * 0.6), int(ry * 0.3)), math.degrees(a), 0, 360, 255, -1)
            m = cv2.GaussianBlur(m, (0, 0), rng.uniform(0.5, 1.5)).astype(np.float32) / 255
            yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
            sh = 0.55 + 0.45 * np.clip(1 - (((xx - cx + rx * 0.3) / rx) ** 2 + ((yy - cy + ry * 0.3) / ry) ** 2) / 2, 0, 1)
            sh = sh * (0.85 + 0.3 * fractal(rng, H, W, 3, 8))
            shaded = np.clip(col[None, None] * sh[..., None] ** 1.5, 0, 1)
            img = img * (1 - m[..., None]) + shaded * m[..., None]
            alpha = np.maximum(alpha, m)
        if rng.random() < 0.7:  # traits fins, hachures (gravure)
            m = np.zeros((H, W), np.uint8)
            dark = rand_ink_color(rng, "black") if rng.random() < 0.6 else rand_ink_color(rng)
            for _ in range(rng.integers(3, 40)):
                pts = np.cumsum(rng.normal(0, max(H, W) * 0.05, (rng.integers(2, 6), 2)), 0)
                pts += [rng.uniform(0, W), rng.uniform(0, H)]
                cv2.polylines(m, [pts.astype(np.int32)], False, 255, int(rng.integers(1, 4)), cv2.LINE_AA)
            m = m.astype(np.float32) / 255
            img = img * (1 - m[..., None]) + dark[None, None] * m[..., None]
            if transparent:
                alpha = np.maximum(alpha, m)
        return img.astype(np.float32), alpha


def gen_clean(rng, long_side=1024):
    """-> cov (H,W,5) = C, M, J, N, blanc ; classes ; fond (transmission lin. ou None)."""
    bg = None
    ar = rng.choice([1.414, 1.414, 1.294, 1.5, 1.33, 1.6, 1.0, 1.2])
    H, W = long_side, int(long_side / ar)
    if rng.random() < 0.12:
        H, W = W, H
    pg = Page(rng, H, W)
    kind = rng.choice(["text", "cover", "cover", "mixed", "form"], p=[0.25, 0.2, 0.15, 0.25, 0.15])
    m = int(min(H, W) * rng.uniform(0.04, 0.1))
    F = fonts()
    serif = [f for f in F if "Serif" in f or "Caladea" in f or "Charter" in f] or F

    if kind == "cover":
        # aplat principal (parfois avec coins arrondis comme la couverture de Baudelaire)
        bleed = rng.random() < 0.5  # fond entièrement coloré (ex. couverture orange de « Rework ») :
        if bleed:                   # ce fond devient la « couleur du papier », le blanc est une encre
            pg.bleed = True
            bg = rand_ink_color(rng, "any")
        elif rng.random() < 0.8:
            x0, y0 = rng.uniform(-0.1, 0.4) * W, rng.uniform(0.25, 0.5) * H
            x1, y1 = rng.uniform(0.6, 1.1) * W, rng.uniform(0.7, 0.98) * H
            pg.put(pg.shape_mask(x0, y0, x1, y1), rand_ink_color(rng, "pale" if rng.random() < 0.5 else "any"), 2)
        if rng.random() < 0.85:  # illustration détourée
            ih, iw = int(H * rng.uniform(0.2, 0.5)), int(W * rng.uniform(0.3, 0.8))
            img, a = pg.illustration(ih, iw, transparent=rng.random() < 0.6)
            oy, ox = rng.integers(0, H - ih), rng.integers(0, W - iw)
            full = np.zeros((H, W), np.float32)
            full[oy:oy + ih, ox:ox + iw] = a
            col = np.ones((H, W, 3), np.float32)
            col[oy:oy + ih, ox:ox + iw] = img
            pg.put(full, col, 3, white=bleed and rng.random() < 0.6)
        y = m
        for _ in range(rng.integers(1, 4)):  # titres
            size = rng.uniform(0.04, 0.13) * H
            f = rng.choice(F)
            col = rand_ink_color(rng, "any" if rng.random() < 0.6 else "black")
            if bleed and rng.random() < 0.65:
                col = np.ones(3, np.float32)  # lettres blanches (encre blanche)
            txt = " ".join(word(rng) for _ in range(rng.integers(1, 3)))
            x = rng.uniform(m, W * 0.5)
            w, h = pg.text(x, y, txt, size, col, f)
            y += h + rng.uniform(0, 0.03) * H
        pg.text(rng.uniform(m, W * 0.5), rng.uniform(0, 0.08) * H, word(rng).upper(), rng.uniform(12, 30),
                rand_ink_color(rng, "black"), rng.choice(serif))
        if rng.random() < 0.6:  # texte en biais
            pg.text(rng.uniform(0.2, 0.6) * W, rng.uniform(0.3, 0.5) * H, sentence(rng, rng.integers(3, 7)),
                    rng.uniform(14, 34), rand_ink_color(rng, "black"), rng.choice(serif), angle=rng.uniform(-70, -20))
        for _ in range(rng.integers(0, 3)):  # petits logos / encadrés
            x, y = rng.uniform(0, 0.8) * W, rng.uniform(0.7, 0.95) * H
            w, h = rng.uniform(0.06, 0.2) * W, rng.uniform(0.03, 0.08) * H
            pg.put(pg.shape_mask(x, y, x + w, y + h, rng.choice(["rect", "round", "ellipse"])), rand_ink_color(rng), 2)
            pg.text(x + 3, y + 3, word(rng), h * 0.45, np.ones(3, np.float32) if rng.random() < 0.5 else rand_ink_color(rng, "black"))
        if rng.random() < 0.6:
            pg.paragraph(rng.uniform(0.3, 0.6) * W, rng.uniform(0.85, 0.95) * H, W * 0.4, rng.uniform(11, 18),
                         rand_ink_color(rng, "text"), 2, rng.choice(serif))
    else:
        if kind == "mixed" and rng.random() < 0.7:  # bandeau de titre
            bh = rng.uniform(0.06, 0.15) * H
            pg.put(pg.shape_mask(0, 0, W, bh, "band"), rand_ink_color(rng), 2)
            pg.text(m, bh * 0.2, sentence(rng, rng.integers(1, 4)), bh * 0.5,
                    np.ones(3, np.float32) if rng.random() < 0.6 else rand_ink_color(rng, "black"))
            y = bh + m
        else:
            y = m
            pg.text(m, y, sentence(rng, rng.integers(1, 5)), rng.uniform(22, 50), rand_ink_color(rng, "text"))
            y += rng.uniform(45, 80)
        ncol = 1 if kind != "mixed" else rng.integers(1, 4)
        colw = (W - 2 * m - (ncol - 1) * 20) / ncol
        body = rng.uniform(10, 22)
        bfont = rng.choice(F)
        tcol = rand_ink_color(rng, "text")
        for c in range(ncol):
            yy = y
            x = m + c * (colw + 20)
            while yy < H - m - 40:
                r = rng.random()
                if r < 0.12:  # image
                    ih = int(rng.uniform(0.1, 0.3) * H)
                    if yy + ih > H - m:
                        break
                    img = pg.image_fill(ih, int(colw))
                    full = np.zeros((pg.H, pg.W), np.float32)
                    full[int(yy):int(yy) + ih, int(x):int(x) + int(colw)] = 1
                    col = np.ones((pg.H, pg.W, 3), np.float32)
                    col[int(yy):int(yy) + ih, int(x):int(x) + int(colw)] = img
                    pg.put(full, col, 3)
                    yy += ih + 10
                elif r < 0.2:  # encadré coloré avec texte
                    bh = rng.uniform(0.05, 0.15) * H
                    pg.put(pg.shape_mask(x, yy, x + colw, yy + bh, rng.choice(["rect", "round"])),
                           rand_ink_color(rng, "pale"), 2)
                    pg.paragraph(x + 8, yy + 8, colw - 16, body, tcol, int(bh // (body * 1.4)), bfont)
                    yy += bh + 12
                elif r < 0.27 or kind == "form" and r < 0.5:  # traits / tableau
                    rows = rng.integers(1, 6)
                    lw = int(rng.integers(1, 3))
                    lc = rand_ink_color(rng, "text")
                    mk = np.zeros((pg.H, pg.W), np.uint8)
                    rh = body * 1.8
                    for k in range(rows + 1):
                        cv2.line(mk, (int(x), int(yy + k * rh)), (int(x + colw), int(yy + k * rh)), 255, lw)
                    if rng.random() < 0.6:
                        for k in range(rng.integers(2, 5)):
                            xx = int(x + colw * k / 3)
                            cv2.line(mk, (xx, int(yy)), (xx, int(yy + rows * rh)), 255, lw)
                    pg.put(mk.astype(np.float32) / 255, lc, 1)
                    for k in range(rows):
                        pg.text(x + 4, yy + k * rh + 3, sentence(rng, rng.integers(1, 4)), body * 0.9, tcol, bfont)
                    yy += rows * rh + 15
                else:
                    if rng.random() < 0.2:
                        pg.text(x, yy, sentence(rng, rng.integers(1, 5)), body * rng.uniform(1.2, 1.8),
                                rand_ink_color(rng, "text" if rng.random() < 0.6 else "any"))
                        yy += body * 2.4
                    yy = pg.paragraph(x, yy, colw, body, tcol, int(rng.integers(2, 10)), bfont,
                                      align=rng.choice(["left", "left", "center", "right"])) + body
    cov = np.concatenate([rip(pg.t), pg.w[..., None]], -1)
    return cov, pg.cls, bg


# ---------------------------------------------------------------- photo de téléphone
def lamp_gains(rng):
    """Teinte d'une lampe : chaude (jaune/orange) à froide (bleutée), parfois verdâtre."""
    t = rng.uniform(-1, 1) * (1.6 if rng.random() < 0.35 else 1.0)   # parfois très forte (néon, lumière du jour bleue)
    g = np.array([1 + 0.35 * t, 1.0, 1 - 0.45 * t], np.float32).clip(0.12, None)
    g[1] *= 1 + rng.normal(0, 0.06)
    return g / g.max()


def jpeg(img8, q):
    ok, enc = cv2.imencode(".jpg", img8[..., ::-1], [cv2.IMWRITE_JPEG_QUALITY, int(q)])
    return cv2.imdecode(enc, cv2.IMREAD_COLOR)[..., ::-1], enc.tobytes()


def degrade(rng, cov, cls, paper_srgb):
    H, W = cls.shape
    p_lin = srgb2lin(paper_srgb)
    R = print_np(p_lin[None, None], cov)                   # réflectance de la page propre
    defect = np.zeros((H, W), np.float32)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)

    # grain et fibres du papier
    R *= 1 + rng.uniform(0, 0.05) * (rng.random((H, W, 1)).astype(np.float32) - 0.5)
    R *= 1 + rng.uniform(0, 0.04) * (smooth_noise(rng, H, W, 60)[..., None] - 0.5)
    # usure (le papier réapparaît là où l'encre est partie), surtout près des bords
    if rng.random() < 0.55:
        edge = np.minimum(np.minimum(xx, W - 1 - xx), np.minimum(yy, H - 1 - yy)) / min(H, W)
        near = np.clip(1 - edge / rng.uniform(0.03, 0.15), 0, 1)
        sc = (fractal(rng, H, W, 5, 30) > rng.uniform(0.55, 0.75)).astype(np.float32)
        w = cv2.GaussianBlur(sc * near, (0, 0), 0.8) * rng.uniform(0.5, 1)
        R = R * (1 - w[..., None]) + w[..., None] * p_lin * rng.uniform(0.85, 1.05)
        defect = np.maximum(defect, (w > 0.15) * (cls == 0))
    # taches (café, eau, gras)
    for _ in range(rng.poisson(0.7)):
        cx, cy, r = rng.uniform(0, W), rng.uniform(0, H), rng.uniform(0.02, 0.2) * min(H, W)
        d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) / r
        d *= 0.75 + 0.5 * smooth_noise(rng, H, W, 6)
        a = np.clip(1 - d, 0, 1) ** 0.5
        if rng.random() < 0.5:
            a = a * 0.4 + np.exp(-((d - 0.95) / 0.06) ** 2)  # auréole
        tint = np.array(rng.choice([[0.75, 0.55, 0.3], [0.85, 0.8, 0.6], [0.6, 0.6, 0.6], [0.9, 0.85, 0.75]]), np.float32)
        s = rng.uniform(0.15, 0.6)
        R *= 1 - s * a[..., None] * (1 - tint)
        defect = np.maximum(defect, a * s > 0.04)
    # poussières, points
    for _ in range(rng.poisson(6)):
        cx, cy = int(rng.uniform(0, W)), int(rng.uniform(0, H))
        rr = int(rng.integers(1, 4))
        v = rng.choice([0.25, 0.5, 1.3])
        mk = np.zeros((H, W), np.uint8)
        cv2.circle(mk, (cx, cy), rr, 255, -1)
        mk = mk.astype(np.float32) / 255
        R = R * (1 - mk[..., None]) + mk[..., None] * R * v
        defect = np.maximum(defect, mk)
    # pli : ligne claire/sombre traversant la page
    crease = np.zeros((H, W), np.float32)
    if rng.random() < 0.35:
        a = rng.uniform(0, np.pi)
        c = rng.uniform(0.2, 0.8) * W * np.cos(a) + rng.uniform(0.2, 0.8) * H * np.sin(a)
        d = xx * np.cos(a) + yy * np.sin(a) - c
        crease = np.tanh(d / rng.uniform(1, 6)) * rng.uniform(0.03, 0.15)
        line = np.exp(-(d / rng.uniform(0.8, 2)) ** 2)
        R = R * (1 - line[..., None] * rng.uniform(0, 0.6)) + line[..., None] * p_lin * rng.uniform(0, 0.6)
        defect = np.maximum(defect, line > 0.3)

    # éclairage
    L = np.ones((H, W), np.float32)
    ga = rng.uniform(0, 2 * np.pi)
    L *= 1 + rng.uniform(0, 0.5) * ((xx / W - 0.5) * np.cos(ga) + (yy / H - 0.5) * np.sin(ga))
    L *= 1 - rng.uniform(0, 0.45) * (((xx / W - 0.5) ** 2 + (yy / H - 0.5) ** 2) * 2)
    L *= 1 + rng.uniform(0, 0.25) * (smooth_noise(rng, H, W, 3) - 0.5)
    L *= 1 + crease
    Lc = np.ones((H, W, 3), np.float32) * lamp_gains(rng)[None, None]
    if rng.random() < 0.45:  # ombre portée (téléphone, main)
        mk = np.zeros((H, W), np.uint8)
        n = rng.integers(3, 6)
        pts = np.stack([rng.uniform(-0.3, 1.3, n) * W, rng.uniform(-0.3, 1.3, n) * H], 1)
        side = rng.integers(4)
        pts[0] = [[0, 0], [W, 0], [W, H], [0, H]][side]
        cv2.fillPoly(mk, [pts.astype(np.int32)], 255)
        sm = cv2.GaussianBlur(mk.astype(np.float32) / 255, (0, 0), rng.uniform(4, 60))
        dark = rng.uniform(0.3, 0.75)
        stint = np.array([1 - 0.1 * rng.random(), 1, 1 + 0.15 * rng.random()], np.float32)
        Lc = Lc * (1 - sm[..., None] * dark * (2 - stint) / 1.0).clip(0.05, 2)
    L3 = L[..., None] * Lc
    photo = R * L3
    blank = p_lin[None, None] * L3

    # objets hors page : doigts, bout de table
    if rng.random() < 0.25:
        side = rng.integers(4)
        cx = [rng.uniform(0, W), W, rng.uniform(0, W), 0][side]
        cy = [0, rng.uniform(0, H), H, rng.uniform(0, H)][side]
        mk = np.zeros((H, W), np.uint8)
        fw = int(rng.uniform(0.04, 0.08) * min(H, W))
        cv2.ellipse(mk, (int(cx), int(cy)), (fw, int(fw * rng.uniform(1.5, 3))), rng.uniform(0, 180), 0, 360, 255, -1)
        mk = cv2.GaussianBlur(mk.astype(np.float32) / 255, (0, 0), 1.5)
        skin = srgb2lin(np.array(rng.choice([[0.95, 0.75, 0.62], [0.8, 0.58, 0.42], [0.55, 0.38, 0.27]]), np.float32))
        shade = 0.6 + 0.4 * smooth_noise(rng, H, W, 8)
        photo = photo * (1 - mk[..., None]) + mk[..., None] * skin * shade[..., None] * L3
        defect = np.maximum(defect, mk > 0.3)
    if rng.random() < 0.35:
        tex = srgb2lin(np.clip(rng.uniform(0.1, 0.9, 3)[None, None] *
                               (0.7 + 0.6 * fractal(rng, H, W, 4, 80)[..., None]), 0, 1))
        for s in rng.choice(4, size=rng.integers(1, 3), replace=False):
            bw = rng.uniform(0.003, 0.035) * [H, W, H, W][s]
            jag = bw * (0.5 + smooth_noise(rng, H, W, 20))
            mk = [yy < jag, xx > W - 1 - jag, yy > H - 1 - jag, xx < jag][s].astype(np.float32)
            photo = photo * (1 - mk[..., None]) + mk[..., None] * tex * L3
            defect = np.maximum(defect, mk)
    if rng.random() < 0.12:  # reflet
        cx, cy, r = rng.uniform(0, W), rng.uniform(0, H), rng.uniform(0.05, 0.25) * min(H, W)
        g = np.exp(-((xx - cx) ** 2 + (yy - cy) ** 2) / (2 * r * r)) * rng.uniform(0.2, 0.7)
        photo = photo + g[..., None]
        defect = np.maximum(defect, g > 0.15)

    # appareil photo : balance des blancs partielle, exposition, courbe, saturation
    gw = np.median(photo.reshape(-1, 3), 0) + 1e-4
    wb = (gw.mean() / gw) ** rng.uniform(0, 0.85)
    expo = (rng.uniform(0.8, 1.05) if rng.random() < 0.6 else rng.uniform(0.4, 0.8)) / (np.percentile((photo * wb).max(-1), 99) + 1e-4)

    def cam(x):
        y = lin2srgb(x * wb * expo)
        c = rng_c
        y = np.clip(y + c * (y - 0.5) * (1 - np.abs(2 * y - 1)), 0, 1)  # S
        lum = y.mean(-1, keepdims=True)
        return np.clip(lum + (y - lum) * sat, 0, 1)

    rng_c, sat = rng.uniform(-0.1, 0.35), rng.uniform(0.75, 1.3)
    photo_s = cam(photo)
    blank_s = cam(blank)

    # optique et capteur
    if rng.random() < 0.8:
        photo_s = cv2.GaussianBlur(photo_s, (0, 0), rng.uniform(0.3, 1.4))
    if rng.random() < 0.3:
        f = rng.uniform(0.5, 0.9)
        small = cv2.resize(photo_s, (int(W * f), int(H * f)), interpolation=cv2.INTER_AREA)
        photo_s = cv2.resize(small, (W, H), interpolation=cv2.INTER_LINEAR)
    photo_s = photo_s + rng.normal(0, rng.uniform(0.002, 0.025), (H, W, 1)) + \
        rng.normal(0, rng.uniform(0, 0.01), (H, W, 3))
    p8 = (np.clip(photo_s, 0, 1) * 255 + 0.5).astype(np.uint8)
    p8, jbytes = jpeg(p8, rng.uniform(55, 95))
    E = cv2.resize(blank_s, (64, 64), interpolation=cv2.INTER_AREA)
    return jbytes, E.astype(np.float32), defect.astype(np.uint8)


def make_sample(seed, long_side=1024):
    rng = np.random.default_rng(seed)
    paper = rand_paper(rng)
    cov, cls, bg = gen_clean(rng, long_side)
    if bg is not None:  # couleur du fond = aplat imprimé sur une feuille blanche
        white = np.clip(rng.uniform(0.92, 1.0) + rng.normal(0, 0.012, 3), 0, 1).astype(np.float32)
        paper = lin2srgb(srgb2lin(white) * bg)
    jbytes, E, defect = degrade(rng, cov, cls, paper)
    return dict(photo_jpg=jbytes, cov=(cov * 255 + 0.5).astype(np.uint8), cls=cls, defect=defect,
                E=E, paper=paper)


def save_sample(d, path):
    os.makedirs(path, exist_ok=True)
    open(os.path.join(path, "photo.jpg"), "wb").write(d["photo_jpg"])
    cv2.imwrite(os.path.join(path, "cov.png"), d["cov"][..., :4])  # 4 canaux C,M,J,N (stockés tels quels)
    cv2.imwrite(os.path.join(path, "w.png"), d["cov"][..., 4])     # encre blanche
    cv2.imwrite(os.path.join(path, "lab.png"), (d["cls"] + 4 * d["defect"]).astype(np.uint8))
    np.savez(os.path.join(path, "meta.npz"), E=d["E"], paper=d["paper"])
