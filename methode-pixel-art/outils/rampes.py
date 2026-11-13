"""rampes.py palette.json ramps.txt out.png : chaque rampe en couleur puis en gris, avec la
luminance, la teinte et la saturation de chaque ton (contrôle A6-A et A6-J « Teinte »)."""
import sys, colorsys
from PIL import Image, ImageDraw
from pxlib import load_palette
pal = load_palette(sys.argv[1])
lines = [l.split() for l in open(sys.argv[2]) if l.strip() and not l.startswith('#')]
S = 28
out = Image.new('RGB', (S * 10 + 120, len(lines) * (S * 2 + 6) + 6), (60, 58, 66))
d = ImageDraw.Draw(out)
for i, parts in enumerate(lines):
    name, chars = ' '.join(parts[:-1]), parts[-1]
    y = 6 + i * (S * 2 + 6)
    d.text((4, y + 4), name, fill=(230, 230, 230))
    info = []
    for j, c in enumerate(chars):
        r, g, b, _ = pal[c]
        L = round(0.299 * r + 0.587 * g + 0.114 * b)
        h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
        x = 120 + j * S
        d.rectangle([x, y, x + S - 1, y + S - 1], fill=(r, g, b))
        d.rectangle([x, y + S, x + S - 1, y + 2 * S - 1], fill=(L, L, L))
        info.append(f"{c}:L{L} h{round(h*360)} s{round(s*100)}")
    print(f"{name:14s}", '  '.join(info))
out.save(sys.argv[3])
