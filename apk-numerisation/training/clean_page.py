"""Réimpression nette d'une page redressée : IA 1 (éclairage) + IA 2 (tri) + impression nette (finish.py).
   python clean_page.py MODELS_DIR page.png sortie.png [grand_côté_sortie]"""
import os
import sys
import time

import cv2
import numpy as np
import torch

from common import color_name_fr, measure_bg
from finish import page_mode, reprint_clean, reprint_over_photo
from models import PaperNet, SelectNet, sel_probs

md, src, dst = sys.argv[1:4]
out_long = int(sys.argv[4]) if len(sys.argv) > 4 else 2400
torch.set_num_threads(4)
t0 = time.time()


def load(cls, name):
    m = cls()
    m.load_state_dict(torch.load(f"{md}/{name}.pt"))
    return m.eval()


ph = cv2.imread(src)[..., ::-1].astype(np.float32) / 255
H, W = ph.shape[:2]
T = lambda a: torch.from_numpy(np.ascontiguousarray(a)).permute(2, 0, 1)[None].float()
with torch.no_grad():
    _, E = load(PaperNet, "paper")(T(cv2.resize(ph, (256, 256), interpolation=cv2.INTER_AREA)))
    E = E[0].permute(1, 2, 0).numpy()
    k = 512 / max(H, W)
    x5 = cv2.resize(ph, (round(W * k), round(H * k)), interpolation=cv2.INTER_AREA)
    E5 = cv2.resize(E, x5.shape[1::-1], interpolation=cv2.INTER_LINEAR)
    sel = sel_probs(load(SelectNet, "select")(T(x5), T(E5)))[0].permute(1, 2, 0).numpy()
bg, gain, how = measure_bg(x5, sel)
if os.environ.get("PAPER"):
    bg, how = np.array([float(v) for v in os.environ["PAPER"].split(",")], np.float32) / 255, "imposé"
mode, paper = page_mode(sel)
if os.environ.get("MODE"):
    mode = os.environ["MODE"]
print(f"mode {mode} · papier {paper:.0%} de la page", flush=True)
if mode == "photo":
    out = reprint_over_photo(ph, sel, out_long)  # fond = photo améliorée, éléments nets réimprimés
    cv2.imwrite(dst, (out[..., ::-1] * 255 + 0.5).clip(0, 255).astype(np.uint8))
    print("taille", out.shape[1], "x", out.shape[0], "· %.1f s" % (time.time() - t0))
    sys.exit(0)
out, pal, bg, flat = reprint_clean(ph, sel, bg, gain, out_long, return_debug=True)
if os.environ.get("FLAT"):
    cv2.imwrite(os.environ["FLAT"], (flat[..., ::-1] * 255 + 0.5).clip(0, 255).astype(np.uint8))
cv2.imwrite(dst, (out[..., ::-1] * 255 + 0.5).clip(0, 255).astype(np.uint8))
print("fond", (bg * 255).round().astype(int), "·", how)
for c in (pal * 255).round().astype(int):
    print("  encre", c, "#%02x%02x%02x" % tuple(c), color_name_fr(c))
print("taille", out.shape[1], "x", out.shape[0], "· %.1f s" % (time.time() - t0))
