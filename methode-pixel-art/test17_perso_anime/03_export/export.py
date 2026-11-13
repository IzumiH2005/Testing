"""Planches pour un moteur : une ligne par animation, cases de 48x56, échelle 1, fond transparent.
Plus une planche de présentation (source Ludo, base relevée, les deux animations)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '02_anim'))
from PIL import Image
from px import image, lire
from rig import CW, CH
from repos import image_repos
from course import image_course

anims = {'repos': [image_repos(i) for i in range(6)], 'course': [image_course(i) for i in range(8)]}
for nom, fr in anims.items():
    pl = Image.new('RGBA', (CW * len(fr), CH), (0, 0, 0, 0))
    for i, g in enumerate(fr): pl.paste(image(g), (i * CW, 0))
    pl.save(f'{nom}_{CW}x{CH}.png')
# GIF côte à côte, même horloge (repos 6 images lentes, course 8 rapides) sur 1,92 s
Z = 4
frames = []
for t in range(24):
    im = Image.new('RGBA', (CW * 2 * Z, CH * Z), (60, 52, 80, 255))
    r = image(anims['repos'][(t // 4) % 6], None, Z); im.paste(r, (0, 0), r)
    c = image(anims['course'][t % 8], None, Z); im.paste(c, (CW * Z, 0), c)
    frames.append(im)
frames[0].save('demo_x4.gif', save_all=True, append_images=frames[1:], duration=80, loop=0)
# présentation
src = Image.open('../00_base/ludo_source.webp').convert('RGBA').resize((384, 384), Image.NEAREST)
base = image(lire('../00_base/base_brute.txt'), None, 6)
pres = Image.new("RGBA", (540 + 7 * CW * 3 + 10, 400), (60, 52, 80, 255))
blanc = Image.new('RGBA', src.size, (255, 255, 255, 255)); blanc.paste(src, (0, 0), src)
pres.paste(blanc, (8, 8))
pres.paste(base, (400, 40), base)
for i, g in enumerate(anims['repos'] + anims['course']):
    im = image(g, None, 3); pres.paste(im, (540 + (i % 7) * CW * 3, 20 + (i // 7) * CH * 3), im)
pres.save('presentation.png')
print('ok')
