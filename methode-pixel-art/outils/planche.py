"""planche.py in.png out.png [situation.png] : planche de contrôle (A5-11).
Rangée 1 : ×1 et ×2 sur fond clair et sombre, miroir, silhouette, gris.
Rangée 2 : ×4, situation si donnée, gris ×4."""
import sys
from PIL import Image, ImageOps
from pxlib import *
im = Image.open(sys.argv[1]).convert('RGBA')
sit = Image.open(sys.argv[3]).convert('RGBA') if len(sys.argv) > 3 else None
LIGHT, DARK, PAD = (214, 210, 200, 255), (22, 20, 30, 255), 8
row1 = [on_bg(im, LIGHT), on_bg(im, DARK), on_bg(scale(im, 2), LIGHT), on_bg(scale(im, 2), DARK),
        on_bg(ImageOps.mirror(im), DARK), on_bg(silhouette(im), LIGHT), on_bg(gray(im), DARK)]
row2 = [on_bg(scale(im, 4), DARK)]
if sit: row2.append(sit)
row2.append(on_bg(scale(gray(im), 4), DARK))
W = max(sum(i.width for i in row1), sum(i.width for i in row2)) + PAD * 9
H = max(i.height for i in row1) + max(i.height for i in row2) + PAD * 3
out = Image.new('RGBA', (W, H), (60, 58, 66, 255))
x = PAD
for i in row1:
    out.alpha_composite(i, (x, PAD)); x += i.width + PAD
x, y = PAD, max(i.height for i in row1) + PAD * 2
for i in row2:
    out.alpha_composite(i, (x, y)); x += i.width + PAD
out.save(sys.argv[2]); print(sys.argv[2], out.size)
