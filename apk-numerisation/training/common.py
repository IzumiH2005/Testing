"""Outils communs : espaces de couleur et modèle d'imprimante CMJN (synthèse soustractive).

Le principe d'une vraie imprimante couleur :
  - on part d'une feuille (sa couleur = « papier »),
  - on dépose 4 encres transparentes : Cyan, Magenta, Jaune, Noir (K),
  - chaque encre laisse passer une partie de la lumière (sa « transmission » par canal R, V, B),
  - une encre posée à c % filtre : 1 - c * (1 - transmission),
  - les encres se superposent en se multipliant (filtres empilés),
  - couleur imprimée = couleur du papier x produit des filtres (en lumière linéaire).

L'IA « imprimante » prédit, pour chaque point, la quantité de chaque encre (0 à 100 %).
L'image finale est ensuite calculée exactement avec cette formule.
"""
import numpy as np
import torch

# Couleurs des encres de quadrichromie (sRGB à 100 %), converties en transmission linéaire.
INKS_SRGB = np.array([
    [0, 174, 239],    # Cyan
    [236, 0, 140],    # Magenta
    [255, 242, 0],    # Jaune
    [16, 16, 16],     # Noir (K)
], dtype=np.float64) / 255.0
INK_NAMES = ["C", "M", "J", "N"]


def srgb2lin(x):
    x = np.asarray(x, dtype=np.float32)
    return np.where(x <= 0.04045, x / 12.92, ((np.maximum(x, 0) + 0.055) / 1.055) ** 2.4).astype(np.float32)


def lin2srgb(x):
    x = np.clip(np.asarray(x, dtype=np.float32), 0, 1)
    return np.where(x <= 0.0031308, 12.92 * x, 1.055 * np.power(x, 1 / 2.4) - 0.055).astype(np.float32)


def t_srgb2lin(x):
    return torch.where(x <= 0.04045, x / 12.92, ((x.clamp(min=0) + 0.055) / 1.055) ** 2.4)


def t_lin2srgb(x):
    x = x.clamp(0, 1)
    return torch.where(x <= 0.0031308, 12.92 * x, 1.055 * x.clamp(min=1e-8) ** (1 / 2.4) - 0.055)


INK_T = srgb2lin(INKS_SRGB)  # (4,3) transmission linéaire de chaque encre à 100 %


def render_np(cov):
    """cov (...,4) couverture 0..1 -> transmission linéaire (...,3)."""
    t = np.ones(cov.shape[:-1] + (3,), np.float32)
    for i in range(4):
        t *= 1.0 - cov[..., i:i + 1] * (1.0 - INK_T[i])
    return t


def render_t(cov):
    """cov [B,4,H,W] -> transmission linéaire [B,3,H,W] (même formule, pour l'entraînement)."""
    T = torch.as_tensor(INK_T, dtype=cov.dtype, device=cov.device)
    out = None
    for i in range(4):
        f = 1.0 - cov[:, i:i + 1] * (1.0 - T[i].view(1, 3, 1, 1))
        out = f if out is None else out * f
    return out


# --- « RIP » : conversion couleur -> quantités d'encre (table 3D précalculée) ---
_LUT = None


def build_lut(n=33, iters=1500):
    """Pour chaque couleur cible (transmission sRGB codée sur une grille n^3), cherche les
    4 couvertures d'encre qui la reproduisent le mieux, en préférant le noir pour les gris
    (remplacement du gris par le noir, comme le font les pilotes d'imprimante)."""
    g = torch.linspace(0, 1, n)
    r, gg, b = torch.meshgrid(g, g, g, indexing="ij")
    tgt = torch.stack([r, gg, b], -1).reshape(-1, 3)
    z = torch.zeros(tgt.shape[0], 4, requires_grad=True)
    with torch.no_grad():
        z[:] = -2.0
    opt = torch.optim.Adam([z], lr=0.05)
    T = torch.as_tensor(INK_T, dtype=torch.float32)
    for it in range(iters):
        cov = torch.sigmoid(z)
        t = torch.ones(tgt.shape[0], 3)
        for i in range(4):
            t = t * (1 - cov[:, i:i + 1] * (1 - T[i]))
        err = ((t_lin2srgb(t) - tgt) ** 2).sum(1)
        cost = 1e-4 * cov.sum(1) + 4e-3 * cov[:, :3].min(1).values
        loss = (err + cost).sum()
        opt.zero_grad()
        loss.backward()
        opt.step()
    cov = torch.sigmoid(z).detach()
    cov[cov < 0.004] = 0
    cov[cov > 0.996] = 1
    return cov.reshape(n, n, n, 4).permute(3, 0, 1, 2).contiguous()  # [4,R,G,B]


def get_lut(path=None):
    global _LUT
    if _LUT is None:
        import os
        path = path or os.path.join(os.path.dirname(__file__), "rip_lut.pt")
        if os.path.exists(path):
            _LUT = torch.load(path)
        else:
            _LUT = build_lut()
            torch.save(_LUT, path)
    return _LUT


def rip(t_lin):
    """t_lin (H,W,3) transmission linéaire voulue -> couverture (H,W,4) via la table."""
    lut = get_lut()
    s = torch.from_numpy(lin2srgb(t_lin))
    H, W, _ = s.shape
    grid = (s[..., [2, 1, 0]] * 2 - 1).view(1, 1, H, W, 3)  # x=B (dernier axe), y=G, z=R
    out = torch.nn.functional.grid_sample(lut[None], grid, mode="bilinear", align_corners=True)
    return out[0, :, 0].permute(1, 2, 0).numpy().astype(np.float32)


# --- noms de couleurs en français (pour l'affichage de la couleur du papier) ---
def color_name_fr(rgb255):
    import colorsys
    r, g, b = [c / 255 for c in rgb255]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    if s < 0.08 or (l > 0.9 and s < 0.25 and max(r, g, b) - min(r, g, b) < 0.035):
        if l > 0.9:
            return "blanc"
        if l > 0.7:
            return "gris clair"
        return "gris" if l > 0.35 else "noir"
    hue = h * 360
    names = [(15, "rouge"), (40, "orange"), (65, "jaune"), (160, "vert"), (200, "turquoise"),
             (255, "bleu"), (290, "violet"), (335, "rose"), (360, "rouge")]
    base = next(n for lim, n in names if hue < lim)
    if base == "orange" and l > 0.75:
        base = "crème" if s < 0.6 else "pêche"
    if base == "jaune" and l > 0.85 and s < 0.6:
        base = "crème"
    if l > 0.82:
        return base + (" très clair" if l > 0.9 else " clair")
    if l < 0.3:
        return base + " foncé"
    return base
