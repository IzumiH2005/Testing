"""Squelette léger : on garde la tête et le buste de la base (pixels Ludo), et on redessine
les membres qui bougent (jambes, bras, cape) à partir de points clés.
Repère : celui de la base (20x50), sol = rang 49. Le canevas ajoute une marge autour."""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))
from px import lire

ICI = os.path.dirname(os.path.abspath(__file__))
P = lambda n: lire(os.path.join(ICI, '..', '01_pieces', n + '.txt'))
BUSTE, CAPE0, MAINP, MAINL, JP0, JL0 = (P(n) for n in
    ('buste', 'cape', 'main_proche', 'main_loin', 'jambe_proche', 'jambe_loin'))

CW, CH, OX, OY = 48, 56, 18, 4          # canevas et position de la base dedans

def canevas():
    return [['.'] * CW for _ in range(CH)]

def coller(C, g, dx=0, dy=0, rows=None):
    for y, r in enumerate(g):
        if rows and not (rows[0] <= y <= rows[1]): continue
        for x, c in enumerate(r):
            if c != '.':
                X, Y = x + OX + dx, y + OY + dy
                if 0 <= X < CW and 0 <= Y < CH: C[Y][X] = c

# ---------- membres tracés ----------
def capsule(mask, a, b, r):
    """Marque les pixels à distance <= r du segment ab (coordonnées base)."""
    (x0, y0), (x1, y1) = a, b
    for Y in range(int(min(y0, y1) - r - 1), int(max(y0, y1) + r + 2)):
        for X in range(int(min(x0, x1) - r - 1), int(max(x0, x1) + r + 2)):
            px, py = X + .5, Y + .5
            dx, dy = x1 - x0, y1 - y0
            L = dx * dx + dy * dy
            t = 0 if L == 0 else max(0, min(1, ((px - x0) * dx + (py - y0) * dy) / L))
            if (px - x0 - t * dx) ** 2 + (py - y0 - t * dy) ** 2 <= r * r:
                mask[(X, Y)] = t

def ik(h, a, l1=5.5, l2=6.5, avant=1):
    """Genou entre la hanche h et la cheville a ; avant=1 plie le genou vers l'avant (droite)."""
    dx, dy = a[0] - h[0], a[1] - h[1]
    d = max(1e-6, min(math.hypot(dx, dy), l1 + l2 - 1e-3))
    c = (l1 * l1 + d * d - l2 * l2) / (2 * l1 * d)
    ang = math.atan2(dy, dx) - avant * math.acos(max(-1, min(1, c)))
    return (h[0] + l1 * math.cos(ang), h[1] + l1 * math.sin(ang))

COUL = {'proche': dict(peau='s', ombre='S', botte='K', bord='C'),
        'loin':   dict(peau='S', ombre='T', botte='B', bord='O')}

def jambe(C, h, a, pied, cote, dy=0):
    """h hanche, a cheville, pied = angle du pied en degrés (0 = à plat vers l'avant,
    + = pointe vers le bas). Peau du genou au haut de la botte, botte sous le genou."""
    k = ik(h, a)
    col = COUL[cote]
    m_cuisse, m_tibia, m_pied = {}, {}, {}
    capsule(m_cuisse, h, k, 2.0)
    capsule(m_tibia, k, a, 2.1)
    th = math.radians(pied)
    talon = (a[0] - 1.0 * math.cos(th), a[1] + 1.4 - 1.0 * math.sin(th))
    pointe = (a[0] + 4.4 * math.cos(th), a[1] + 1.4 + 4.4 * math.sin(th))
    capsule(m_pied, talon, pointe, 1.7)
    out = {}
    for (X, Y), t in m_cuisse.items(): out[(X, Y)] = col['peau']
    for (X, Y), t in m_tibia.items(): out[(X, Y)] = col['peau'] if t < 0.12 else col['botte']
    for (X, Y) in m_pied: out[(X, Y)] = col['botte']
    # ombrage : bord arrière (gauche) et dessous de semelle plus sombres
    res = {}
    for (X, Y), c in out.items():
        if c == col['peau'] and (X - 1, Y) not in out: c = col['ombre']
        if c == col['botte'] and ((X - 1, Y) not in out or ((X, Y + 1) not in out and (X, Y) in m_pied)):
            c = col['bord']
        res[(X, Y)] = c
    for (X, Y), c in res.items():
        Xc, Yc = X + OX, Y + OY + dy
        if 0 <= Xc < CW and 0 <= Yc < CH: C[Yc][Xc] = c
    return k

def bras(C, epaule, coude, main, cote, dy=0):
    """Manche (tunique) de l'épaule au coude, peau du coude à la main."""
    m1, m2 = {}, {}
    capsule(m1, epaule, coude, 1.6)
    capsule(m2, coude, main, 1.4)
    out = {}
    for k in m1: out[k] = 'E'
    for k in m2:
        if k not in out: out[k] = 's' if cote == 'proche' else 'S'
    res = {}
    for (X, Y), c in out.items():
        bordure = any((X + i, Y + j) not in out for i, j in ((-1, 0), (1, 0), (0, 1), (0, -1)))
        if c == 'E' and bordure: c = 'F'
        if c in 'sS' and (X - 1, Y) not in out: c = 'S' if cote == 'proche' else 'T'
        res[(X, Y)] = c
    for (X, Y), c in res.items():
        Xc, Yc = X + OX, Y + OY + dy
        if 0 <= Xc < CW and 0 <= Yc < CH: C[Yc][Xc] = c

def cape(C, ancre, angle, longueur, onde, phase, dy=0, largeur=(2.0, 3.6)):
    """Bande qui part du cou vers l'arrière. angle en degrés depuis la verticale
    (0 = pend, 90 = horizontale vers l'arrière). onde = amplitude de l'ondulation."""
    out = {}
    a = math.radians(angle)
    for i in range(int(longueur * 3)):
        t = i / (longueur * 3 - 1)
        # direction qui s'incurve : la cape tombe un peu plus vers son bout (gravité)
        aa = a * (1 - 0.35 * t)
        s = t * longueur
        cx = ancre[0] - s * math.sin(aa)
        cy = ancre[1] + s * math.cos(aa)
        w = onde * math.sin(phase + t * 5.0) * t
        nx, ny = math.cos(aa), math.sin(aa)       # normale
        cx += w * nx; cy += w * ny
        r = largeur[0] + (largeur[1] - largeur[0]) * t
        for k in range(-int(r * 2), int(r * 2) + 1):
            o = k / 2
            X, Y = int(math.floor(cx + o * nx)), int(math.floor(cy + o * ny))
            # côté corps (o > 0 : vers la droite/bas) dans l'ombre
            out[(X, Y)] = 'D' if o > r * 0.25 else 'o'
    # nettoyage : boucher les encoches d'un pixel, retirer les pixels isolés
    for _ in range(2):
        voisins = lambda X, Y: [out.get((X + i, Y + j)) for i, j in ((-1, 0), (1, 0), (0, -1), (0, 1))]
        ajout = {}
        xs = [k[0] for k in out]; ys = [k[1] for k in out]
        for X in range(min(xs) - 1, max(xs) + 2):
            for Y in range(min(ys) - 1, max(ys) + 2):
                v = [c for c in voisins(X, Y) if c]
                if (X, Y) not in out and len(v) >= 3: ajout[(X, Y)] = 'o' if v.count('o') >= v.count('D') else 'D'
        out.update(ajout)
        for k in [k for k in out if len([c for c in voisins(*k) if c]) <= 1]: del out[k]
    for (X, Y), c in out.items():
        Xc, Yc = X + OX, Y + OY + dy
        if 0 <= Xc < CW and 0 <= Yc < CH: C[Yc][Xc] = c

def boucher(C):
    """Pixels vides enfermés (entre cape et corps) : pris de la couleur voisine de gauche."""
    for y in range(1, CH - 1):
        for x in range(1, CW - 1):
            if C[y][x] == '.' and all(c != '.' for c in (C[y][x-1], C[y][x+1], C[y-1][x], C[y+1][x])):
                C[y][x] = C[y][x-1] if C[y][x-1] in 'oD' else C[y][x+1]
    return C
