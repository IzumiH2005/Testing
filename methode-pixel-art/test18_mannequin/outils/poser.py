"""Rendu d'une pose du mannequin, vue de profil orthographique.

Usage : python3 -I poser.py <action> <frame> <sortie_prefixe> [--rot bone=x,y,z ...]
Produit :
  <prefixe>_ref.png    grand rendu (x10) : membres proches clairs, membres loin sombres
  <prefixe>_px.png     même rendu ramené à la taille sprite (silhouette pour calquer)
  <prefixe>_os.json    articulations projetées en coordonnées pixel sprite
"""
import bpy, sys, os, json, math
from mathutils import Euler

ICI = os.path.dirname(os.path.abspath(__file__))
BLEND = os.path.join(ICI, '..', 'modele', 'mannequiny-0.4.0.blend')
W, H = 48, 56          # canevas sprite
TAILLE = 46            # hauteur du perso en pixels (debout)
Z = 10                 # zoom du rendu de référence
CENTRER = True

args = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
action, frame, sortie = args[0], int(args[1]), args[2]
rots = {}
if '--rot' in args:
    for a in args[args.index('--rot') + 1:]:
        b, v = a.split('='); rots[b] = [math.radians(float(x)) for x in v.split(',')]

bpy.ops.wm.open_mainfile(filepath=BLEND)
sc = bpy.context.scene
arm = bpy.data.objects['root']; corps = bpy.data.objects['body.001']
arm.animation_data_create(); arm.animation_data.action = bpy.data.actions[action]
sc.frame_set(frame)
for b, r in rots.items():
    pb = arm.pose.bones[b]; pb.rotation_mode = 'XYZ'; pb.rotation_euler = Euler(r)
bpy.context.view_layer.update()

# deux matériaux : côté proche (.l, face caméra) clair, côté loin (.r) sombre, tronc moyen
def mat(nom, c):
    m = bpy.data.materials.new(nom); m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    e = nt.nodes.new('ShaderNodeEmission'); e.inputs[0].default_value = c
    o = nt.nodes.new('ShaderNodeOutputMaterial'); nt.links.new(e.outputs[0], o.inputs[0])
    return m
mats = [mat('tronc', (.45, .45, .45, 1)), mat('proche', (1, .45, .12, 1)), mat('loin', (.08, .12, .35, 1))]
me = corps.data; me.materials.clear()
for m in mats: me.materials.append(m)
gidx = {g.index: g.name for g in corps.vertex_groups}
for p in me.polygons:
    sl = sr = 0.0
    for vi in p.vertices:
        for g in me.vertices[vi].groups:
            n = gidx[g.group]
            if n.endswith('.l'): sl += g.weight
            elif n.endswith('.r'): sr += g.weight
    p.material_index = 1 if sr > max(sl, .5) else 2 if sl > max(sr, .5) else 0  # .r = proche

# caméra orthographique côté -X, regard vers +X : le perso regarde vers la droite
cam = bpy.data.objects.get('cam_profil') or bpy.data.objects.new('cam_profil', bpy.data.cameras.new('cam_profil'))
if cam.name not in sc.collection.objects: sc.collection.objects.link(cam)
cam.data.type = 'ORTHO'
haut = 1.8 * H / TAILLE           # le perso (1.8 m) occupe TAILLE px sur H
cam.data.ortho_scale = haut * max(W, H) / H
py = (arm.matrix_world @ arm.pose.bones['pelvis'].head).y if CENTRER else 0
cam.location = (-10, py, haut / 2 - 0.12); cam.rotation_euler = (math.pi / 2, 0, -math.pi / 2)
sc.camera = cam
r = sc.render; r.engine = 'CYCLES'; sc.cycles.device = 'CPU'
sc.cycles.samples = 4; sc.cycles.use_denoising = False
sc.view_settings.view_transform = 'Standard'
r.filter_size = 0.01
r.film_transparent = True; r.resolution_x, r.resolution_y = W * Z, H * Z
r.image_settings.file_format = 'PNG'; r.image_settings.color_mode = 'RGBA'
for o in sc.objects:
    if o.type not in ('MESH', 'ARMATURE', 'CAMERA'): o.hide_render = True
arm.hide_render = True
r.filepath = os.path.abspath(sortie + '_ref.png'); bpy.ops.render.render(write_still=True)

# articulations projetées (coordonnées pixel sprite)
from bpy_extras.object_utils import world_to_camera_view
pts = {}
for pb in arm.pose.bones:
    if not arm.data.bones[pb.name].use_deform or any(k in pb.name for k in ('thumb', 'ring', 'middle', 'index')): continue
    for bout, v in (('', pb.head), ('_fin', pb.tail)):
        co = world_to_camera_view(sc, cam, arm.matrix_world @ v)
        pts[pb.name + bout] = [round(co.x * W, 1), round((1 - co.y) * H, 1)]
json.dump(pts, open(sortie + '_os.json', 'w'), indent=0)

from PIL import Image
im = Image.open(sortie + '_ref.png')
im.resize((W, H), Image.BOX).save(sortie + '_px.png')
