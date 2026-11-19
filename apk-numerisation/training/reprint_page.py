"""Réimprime une page déjà redressée avec les 3 IA (version Python de référence).
   python reprint_page.py MODELS_DIR page.png sortie.png"""
import sys

import cv2
import numpy as np
import torch
import torch.nn.functional as F

from common import color_name_fr, print_t, srgb2lin, t_lin2srgb
from models import PaperNet, PrintNet, SelectNet, sel_probs

md, src, dst = sys.argv[1:4]
long_side = int(sys.argv[4]) if len(sys.argv) > 4 else 1280
torch.set_num_threads(4)


def load(cls, name):
    m = cls()
    m.load_state_dict(torch.load(f"{md}/{name}.pt"))
    return m.eval()


ph = cv2.imread(src)[..., ::-1].astype(np.float32) / 255
H, W = ph.shape[:2]
s = min(1.0, long_side / max(H, W))
ph = cv2.resize(ph, (round(W * s), round(H * s)), interpolation=cv2.INTER_AREA)
H, W = ph.shape[:2]
T = lambda a: torch.from_numpy(np.ascontiguousarray(a)).permute(2, 0, 1)[None].float()
with torch.no_grad():
    paper, E = load(PaperNet, "paper")(T(cv2.resize(ph, (256, 256), interpolation=cv2.INTER_AREA)))
    paper = paper[0].numpy()
    E = E[0].permute(1, 2, 0).numpy()
    rgb = (paper * 255).round().astype(int)
    print("fond", rgb, "#%02x%02x%02x" % tuple(rgb), color_name_fr(rgb))
    k = 512 / max(H, W)
    x5 = cv2.resize(ph, (round(W * k), round(H * k)), interpolation=cv2.INTER_AREA)
    E5 = cv2.resize(E, x5.shape[1::-1], interpolation=cv2.INTER_LINEAR)
    sel = sel_probs(load(SelectNet, "select")(T(x5), T(E5)))[0].permute(1, 2, 0).numpy()
    if len(sys.argv) > 5:
        vis = (np.stack([sel[..., 1], sel[..., 2], sel[..., 3]], -1) * 255).astype(np.uint8)
        vis[sel[..., 4] > 0.5] = [255, 0, 255]
        cv2.imwrite(sys.argv[5], vis[..., ::-1])
    Ef = cv2.resize(E, (W, H), interpolation=cv2.INTER_LINEAR)
    self = cv2.resize(sel, (W, H), interpolation=cv2.INTER_LINEAR)
    cov = load(PrintNet, "print")(T(ph), T(Ef), T(self))
    out = t_lin2srgb(print_t(srgb2lin(paper), cov))[0].permute(1, 2, 0).numpy()
cv2.imwrite(dst, (out[..., ::-1] * 255 + 0.5).astype(np.uint8))
print("encre moyenne C M J N blanc :", cov[0].mean((1, 2)).numpy().round(3))
