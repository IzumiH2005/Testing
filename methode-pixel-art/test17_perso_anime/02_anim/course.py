"""Course en 8 images : contact, descente, passage, poussée, puis l'autre jambe."""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rig import *

DY = [0, 1, 0, -1, 0, 1, 0, -1]
# cheville (par rapport à la hanche) et angle du pied, pour une jambe, phase 0 = contact devant
JAMBE = [((6.5, 10.5), -20), ((3.0, 10.5), 0), ((-1.0, 11.5), 0), ((-5.0, 11.5), 35),
         ((-7.5, 8.5), 55), ((-6.0, 4.5), 85), ((1.5, 6.0), 30), ((6.5, 8.5), -10)]
# bras proche : coude et main, phase 0 = bras en arrière (jambe proche devant)
BRAS = [((5.5, 27), (3.5, 31)), ((6.5, 27.5), (5.5, 31.5)), ((8, 28), (9, 31)), ((9.5, 27.5), (12.5, 28.5)),
        ((10.5, 27), (14, 25.5)), ((9.5, 27.5), (12.5, 28.5)), ((8, 28), (9, 31)), ((6.5, 27.5), (5.5, 31.5))]

def image_course(i):
    C = canevas()
    dy = DY[i]
    pf = (i + 4) % 8
    cape(C, (7, 18.5), 48 + 5 * math.sin(i * math.pi / 2), 20, 2.4, -i * math.pi / 4, dy, largeur=(2.0, 4.6))
    # bras loin (derrière le buste), en opposition au bras proche
    e, m = BRAS[pf]
    bras(C, (13, 22), (e[0] + 4, e[1]), (m[0] + 4, m[1]), 'loin', dy)
    a, ang = JAMBE[pf]
    jambe(C, (11, 35 + dy), (11 + a[0], 35 + dy + a[1]), ang, 'loin')
    a, ang = JAMBE[i]
    jambe(C, (8.5, 35 + dy), (8.5 + a[0], 35 + dy + a[1]), ang, 'proche')
    # penché vers l'avant : bas du buste en place, haut du buste +1, tête +2
    coller(C, BUSTE, 0, dy, rows=(28, 37))
    coller(C, BUSTE, 1, dy, rows=(17, 27))
    coller(C, BUSTE, 2, dy, rows=(0, 16))
    e, m = BRAS[i]
    bras(C, (9, 22), (e[0]+1, e[1]), (m[0]+1, m[1]), 'proche', dy)
    return boucher(C)

if __name__ == '__main__':
    from px import image, ecrire
    from PIL import Image
    os.makedirs('course', exist_ok=True)
    ims = []
    for i in range(8):
        g = image_course(i)
        ecrire(f'course/course_{i}.txt', g, f'Course, image {i}')
        ims.append(g)
    Z = 6
    pl = Image.new('RGBA', (CW * Z * 8, CH * Z), (60, 52, 80, 255))
    for i, g in enumerate(ims):
        im = image(g, None, Z); pl.paste(im, (i * CW * Z, 0), im)
    pl.save('course_planche_x6.png')
    fr = [image(g, '#3c3450', 4) for g in ims]
    fr[0].save('course_x4.gif', save_all=True, append_images=fr[1:], duration=80, loop=0, disposal=2)
