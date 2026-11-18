"""Les 3 IA de la réimpression.

IA 1 « œil du papier » (PaperNet)  : regarde la photo entière (256x256) et donne
    - la vraie couleur du papier (sans l'éclairage, les taches, la saleté),
    - l'aspect qu'aurait le papier nu sur la photo (carte 64x64 : lumière, ombres, teinte de lampe).
IA 2 « trieur » (SelectNet)         : pour chaque point (page réduite à 512 px), dit si c'est du papier,
    du texte/trait, un aplat de couleur ou une image, et si c'est un défaut à ne pas réimprimer
    (tache, pli, usure, doigt, bout de table, reflet).
IA 3 « imprimante » (PrintNet)      : pour chaque point en pleine résolution, donne la quantité
    d'encre Cyan, Magenta, Jaune et Noir à déposer (0 à 100 %).
La page finale est ensuite « imprimée » : couleur du papier x filtres des 4 encres.
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


class PaperNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.e1 = cbr(3, 16, 2)                                  # 128
        self.e2 = nn.Sequential(cbr(16, 32, 2), cbr(32, 32))     # 64
        self.e3 = nn.Sequential(cbr(32, 64, 2), cbr(64, 64))     # 32
        self.e4 = nn.Sequential(cbr(64, 96, 2), cbr(96, 96))     # 16
        self.e5 = nn.Sequential(cbr(96, 128, 2), cbr(128, 128))  # 8
        self.head = nn.Sequential(nn.Linear(256, 96), nn.ReLU(inplace=True), nn.Linear(96, 3))
        self.d4 = cbr(128 + 96, 64)
        self.d3 = cbr(64 + 64, 48)
        self.d2 = nn.Sequential(cbr(48 + 32, 32), nn.Conv2d(32, 3, 3, 1, 1))

    def forward(self, x):  # x [B,3,256,256] sRGB 0..1
        e2 = self.e2(self.e1(x))
        e3 = self.e3(e2)
        e4 = self.e4(e3)
        e5 = self.e5(e4)
        g = torch.cat([e5.mean((2, 3)), e5.amax((2, 3))], 1)
        paper = torch.sigmoid(self.head(g))
        up = lambda t: F.interpolate(t, scale_factor=2.0, mode="bilinear", align_corners=False)
        d = self.d4(torch.cat([up(e5), e4], 1))
        d = self.d3(torch.cat([up(d), e3], 1))
        E = torch.sigmoid(self.d2(torch.cat([up(d), e2], 1)))  # [B,3,64,64]
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
    """Sortie : couverture C, M, J, N (0..1) en chaque point."""
    def __init__(self):
        super().__init__()
        self.net = UNet(11, 4, [16, 32, 48, 64])

    def forward(self, photo, paperE, sel):  # sel = probabilités de l'IA 2 agrandies à la même taille
        return torch.sigmoid(self.net(torch.cat([photo, normalize(photo, paperE), sel], 1)))
