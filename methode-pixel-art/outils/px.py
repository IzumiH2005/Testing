"""px.py etape.txt [echelle] palette.json -> etape.png (×1) et etape_vue.png (grille)."""
import sys, os
from pxlib import *
src = sys.argv[1]; k = int(sys.argv[2]) if len(sys.argv) > 3 else 12
pal = load_palette(sys.argv[-1])
im = grid_to_image(load_grid(src), pal)
base = os.path.splitext(src)[0]
im.save(base + '.png')
vue(im, k).save(base + '_vue.png')
print(base + '.png', im.size)
