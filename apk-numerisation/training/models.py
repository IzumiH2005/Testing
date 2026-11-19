"""Les 3 IA de la réimpression.

IA 1 « œil du papier » (PaperNet)  : regarde la photo entière (256x256) et donne
    - la vraie couleur du papier (sans l'éclairage, les taches, la saleté),
    - l'aspect qu'aurait le papier nu sur la photo (carte 64x64 : lumière, ombres, teinte de lampe).
IA 2 « trieur » (SelectNet)         : pour chaque point (page réduite à 512 px), dit si c'est du papier,
    du texte/trait, un aplat de couleur ou une image, et si c'est un défaut à ne pas réimprimer
    (tache, pli, usure, doigt, bout de table, reflet).
IA 3 « imprimante » (PrintNet)      : pour chaque point en pleine résolution, donne la quantité
    d'encre Blanche (couvrante), Cyan, Magenta, Jaune et Noir à déposer (0 à 100 %).
La page finale est ensuite « imprimée » : couleur du fond, recouverte de blanc là où il faut,
puis filtres des 4 encres.
"""
import torch
import torch.nn as nn
import torch.nn.functional as F


def cbr(i, o, s=1):
    return nn.Sequential(nn.Conv2d(i, o, 3, s, 1, bias=False), nn.BatchNorm2d(o), nn.ReLU(inplace=True))


def lin(x):
    return torch.where(x <= 0.04045, x / 12.92, ((x.clamp(min=0) + 0.055) / 1.055) ** 2.4)


def enc(x):
    x = x.clamp(0, 1)
    return torch.where(x <= 0.0031308, 12.92 * x, 1.055 * (x.clamp(min=1e-6)) ** (1 / 2.4) - 0.055)


def normalize(photo, paperE):
    """Divise la photo par l'aspect du papier nu : le papier devient blanc, l'encre garde sa force."""
    n = lin(photo) / lin(paperE).clamp(min=2e-3)
    return enc(n)


# ---- MobileNetV3-Large (Howard et al. 2019), même structure que torchvision (licence BSD-3)
#      pour pouvoir charger ses poids pré-entraînés sur ImageNet sans dépendre de torchvision.
def _div8(v):
    n = max(8, int(v + 4) // 8 * 8)
    return n + 8 if n < 0.9 * v else n


def _cna(i, o, k=1, s=1, g=1, act=nn.Hardswish):
    L = [nn.Conv2d(i, o, k, s, (k - 1) // 2, groups=g, bias=False), nn.BatchNorm2d(o, eps=0.001, momentum=0.01)]
    if act:
        L.append(act(inplace=True))
    return nn.Sequential(*L)


class _SE(nn.Module):
    def __init__(self, c, q):
        super().__init__()
        self.fc1, self.fc2 = nn.Conv2d(c, q, 1), nn.Conv2d(q, c, 1)

    def forward(self, x):
        return x * F.hardsigmoid(self.fc2(F.relu(self.fc1(x.mean((2, 3), keepdim=True)))))


class _IR(nn.Module):
    def __init__(self, i, k, e, o, se, act, s):
        super().__init__()
        L = [] if e == i else [_cna(i, e, act=act)]
        L.append(_cna(e, e, k, s, e, act))
        if se:
            L.append(_SE(e, _div8(e // 4)))
        L.append(_cna(e, o, act=None))
        self.block, self.res = nn.Sequential(*L), s == 1 and i == o

    def forward(self, x):
        y = self.block(x)
        return x + y if self.res else y


_MBV3 = [(16, 3, 16, 16, 0, "RE", 1), (16, 3, 64, 24, 0, "RE", 2), (24, 3, 72, 24, 0, "RE", 1),
         (24, 5, 72, 40, 1, "RE", 2), (40, 5, 120, 40, 1, "RE", 1), (40, 5, 120, 40, 1, "RE", 1),
         (40, 3, 240, 80, 0, "HS", 2), (80, 3, 200, 80, 0, "HS", 1), (80, 3, 184, 80, 0, "HS", 1),
         (80, 3, 184, 80, 0, "HS", 1), (80, 3, 480, 112, 1, "HS", 1), (112, 3, 672, 112, 1, "HS", 1),
         (112, 5, 672, 160, 1, "HS", 2), (160, 5, 960, 160, 1, "HS", 1), (160, 5, 960, 160, 1, "HS", 1)]


class MobileNetV3(nn.Module):
    def __init__(self):
        super().__init__()
        L = [_cna(3, 16, 3, 2)]
        L += [_IR(i, k, e, o, se, nn.ReLU if a == "RE" else nn.Hardswish, s) for i, k, e, o, se, a, s in _MBV3]
        L.append(_cna(160, 960))
        self.features = nn.Sequential(*L)


class PaperNet(nn.Module):
    """IA 1. Base : MobileNetV3-Large pré-entraîné sur ImageNet (il sait déjà distinguer
    couleurs, matières et éclairages), spécialisé ici pour retrouver la couleur du papier."""

    def __init__(self, pretrained=None):
        super().__init__()
        bb = MobileNetV3()
        if pretrained:
            sd = {k: v for k, v in torch.load(pretrained).items() if k.startswith("features.")}
            bb.load_state_dict(sd)
        self.f = bb.features
        self.register_buffer("mean", torch.tensor([0.485, 0.456, 0.406]).view(1, 3, 1, 1))
        self.register_buffer("std", torch.tensor([0.229, 0.224, 0.225]).view(1, 3, 1, 1))
        self.head = nn.Sequential(nn.Linear(1920, 192), nn.ReLU(inplace=True), nn.Linear(192, 3))
        self.r = _cna(960, 96, act=nn.ReLU)
        self.d4 = cbr(96 + 112, 64)
        self.d3 = cbr(64 + 40, 48)
        self.d2 = nn.Sequential(cbr(48 + 24, 32), nn.Conv2d(32, 3, 3, 1, 1))

    def forward(self, x):  # x [B,3,256,256] sRGB 0..1
        h, keep = (x - self.mean) / self.std, {}
        for i, m in enumerate(self.f):
            h = m(h)
            if i in (3, 6, 12):
                keep[i] = h                                    # 64, 32, 16 px
        g = torch.cat([h.mean((2, 3)), h.amax((2, 3))], 1)     # 8 px, 960 canaux
        paper = torch.sigmoid(self.head(g))
        up = lambda t: F.interpolate(t, scale_factor=2.0, mode="bilinear", align_corners=False)
        d = self.d4(torch.cat([up(self.r(h)), keep[12]], 1))
        d = self.d3(torch.cat([up(d), keep[6]], 1))
        E = torch.sigmoid(self.d2(torch.cat([up(d), keep[3]], 1)))  # [B,3,64,64]
        return paper, E


class UNet(nn.Module):
    def __init__(self, cin, cout, ch):
        super().__init__()
        self.inc = nn.Sequential(cbr(cin, ch[0]), cbr(ch[0], ch[0]))
        self.downs = nn.ModuleList([nn.Sequential(cbr(ch[i], ch[i + 1], 2), cbr(ch[i + 1], ch[i + 1]))
                                    for i in range(len(ch) - 1)])
        self.ups = nn.ModuleList([nn.Sequential(cbr(ch[i + 1] + ch[i], ch[i]), cbr(ch[i], ch[i]))
                                  for i in reversed(range(len(ch) - 1))])
        self.out = nn.Conv2d(ch[0], cout, 1)

    def forward(self, x):
        skips = [self.inc(x)]
        for d in self.downs:
            skips.append(d(skips[-1]))
        y = skips.pop()
        for u in self.ups:
            s = skips.pop()
            y = F.interpolate(y, size=s.shape[-2:], mode="bilinear", align_corners=False)
            y = u(torch.cat([y, s], 1))
        return self.out(y)


class SelectNet(nn.Module):
    """Sortie : 4 logits (papier, texte, aplat, image) + 1 logit défaut."""
    def __init__(self):
        super().__init__()
        self.net = UNet(6, 5, [24, 40, 64, 96, 128])

    def forward(self, photo, paperE):  # tous deux [B,3,H,W] sRGB
        return self.net(torch.cat([photo, normalize(photo, paperE)], 1))


def sel_probs(logits):
    return torch.cat([torch.softmax(logits[:, :4], 1), torch.sigmoid(logits[:, 4:5])], 1)


class PrintNet(nn.Module):
    """Sortie : couverture C, M, J, N et blanc couvrant (0..1) en chaque point."""
    def __init__(self):
        super().__init__()
        self.net = UNet(11, 5, [16, 32, 48, 64])

    def forward(self, photo, paperE, sel):  # sel = probabilités de l'IA 2 agrandies à la même taille
        return torch.sigmoid(self.net(torch.cat([photo, normalize(photo, paperE), sel], 1)))
