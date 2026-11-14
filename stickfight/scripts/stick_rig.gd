class_name StickRig
extends RefCounted
## Squelette (rig) du stickman : cinématique directe, cinématique inverse,
## dessin. Tout est statique : une pose est un simple Dictionary, chargé
## depuis un fichier JSON de res://poses/.
##
## Repère du modèle : x vers l'avant (là où regarde le personnage), y vers le
## HAUT, unités ≈ centimètres, sol à y = 0. Un personnage debout mesure ≈ 180.
## Godot a y vers le bas : la conversion se fait seulement au dessin
## (voir to_screen), jamais dans les poses.
##
## Convention des angles de pose : chaque articulation porte un angle en degrés
## mesuré depuis la position de repos (debout, bras le long du corps). Le signe
## est « sémantique » : positif = flexion, ou vers l'avant.
##   - bassin, bas du dos, poitrine : positif = pencher vers l'avant
##   - cou : positif = baisser la tête vers l'avant
##   - épaule : positif = lever le bras devant soi (180 = bras à la verticale)
##   - coude : positif = plier
##   - hanche : positif = monter le genou devant soi
##   - genou : positif = plier (le tibia part vers l'arrière)
##   - cheville : positif = relever la pointe du pied
##
## « proche » (N) = membres côté caméra, dessinés devant le tronc.
## « loin » (F)   = membres de l'autre côté, dessinés derrière.
##
## Format d'une pose (JSON) :
##   { "nom": "garde", "style": "epais", "x": 0, "y": 55, "facing": 1,
##     "angles": { "root": 2, "spineLow": 6, ... } }

## Proportions relevées sur les vidéos de référence (voir RECHERCHE.md).
const STYLES := {
	"epais": {
		"label": "Épais (grosse tête, trait gras)",
		"head": 46.0,      # diamètre de la tête
		"headSink": 0.12,  # part du rayon de tête qui « mord » sur le haut du tronc
		"stroke": 15.0,    # épaisseur du trait
		"hand": 8.5,       # rayon du poing (≤ trait/2 = simple bout rond)
		"neck": 0.0,
		"spineLow": 33.0, "chest": 35.0,
		"upperArm": 34.0, "forearm": 32.0,
		"thigh": 30.0, "shin": 31.0,
		"foot": 0.0,       # 0 = pas de pied, la jambe finit en bout rond
	},
	"fin": {
		"label": "Fin (petite tête, trait léger)",
		"head": 33.0, "headSink": 0.0, "stroke": 11.0, "hand": 7.0, "neck": 3.0,
		"spineLow": 27.0, "chest": 27.0,
		"upperArm": 30.0, "forearm": 28.0,
		"thigh": 44.0, "shin": 44.0,
		"foot": 0.0,
	},
}

## Bassin : son angle incline tout le tronc (les jambes n'en dépendent pas).
const ROOT := {"id": "root", "rest": 90.0, "sign": -1.0, "lim": Vector2(-90, 90), "label": "Bascule du bassin"}

## Hiérarchie des os, parents avant enfants. rest = angle de repos relatif au
## parent (degrés, sens trigonométrique, y vers le haut) ; sign = conversion
## angle sémantique → trigonométrique ; lim = amplitude articulaire humaine
## (AAOS, voir RECHERCHE.md), en angle sémantique.
const BONES := [
	{"id": "spineLow", "parent": "root",     "len": "spineLow", "rest": 0.0,   "sign": -1.0, "lim": Vector2(-25, 45),  "label": "Bas du dos"},
	{"id": "chest",    "parent": "spineLow", "len": "chest",    "rest": 0.0,   "sign": -1.0, "lim": Vector2(-25, 45),  "label": "Poitrine"},
	{"id": "neck",     "parent": "chest",    "len": "neck",     "rest": 0.0,   "sign": -1.0, "lim": Vector2(-60, 50),  "label": "Cou / tête"},
	{"id": "armF",     "parent": "chest",    "len": "upperArm", "rest": 180.0, "sign": 1.0,  "lim": Vector2(-60, 180), "label": "Épaule (loin)"},
	{"id": "foreF",    "parent": "armF",     "len": "forearm",  "rest": 0.0,   "sign": 1.0,  "lim": Vector2(0, 150),   "label": "Coude (loin)"},
	{"id": "armN",     "parent": "chest",    "len": "upperArm", "rest": 180.0, "sign": 1.0,  "lim": Vector2(-60, 180), "label": "Épaule (proche)"},
	{"id": "foreN",    "parent": "armN",     "len": "forearm",  "rest": 0.0,   "sign": 1.0,  "lim": Vector2(0, 150),   "label": "Coude (proche)"},
	{"id": "thighF",   "parent": "root",     "len": "thigh",    "rest": 180.0, "sign": 1.0,  "lim": Vector2(-30, 140), "label": "Hanche (loin)"},
	{"id": "shinF",    "parent": "thighF",   "len": "shin",     "rest": 0.0,   "sign": -1.0, "lim": Vector2(0, 150),   "label": "Genou (loin)"},
	{"id": "footF",    "parent": "shinF",    "len": "foot",     "rest": 90.0,  "sign": 1.0,  "lim": Vector2(-50, 20),  "label": "Cheville (loin)"},
	{"id": "thighN",   "parent": "root",     "len": "thigh",    "rest": 180.0, "sign": 1.0,  "lim": Vector2(-30, 140), "label": "Hanche (proche)"},
	{"id": "shinN",    "parent": "thighN",   "len": "shin",     "rest": 0.0,   "sign": -1.0, "lim": Vector2(0, 150),   "label": "Genou (proche)"},
	{"id": "footN",    "parent": "shinN",    "len": "foot",     "rest": 90.0,  "sign": 1.0,  "lim": Vector2(-50, 20),  "label": "Cheville (proche)"},
]

## Chaînes à deux os pour la cinématique inverse.
const LIMBS := {
	"armN": {"upper": "armN", "lower": "foreN", "base": "shoulder", "tip": "handN", "label": "Bras proche"},
	"armF": {"upper": "armF", "lower": "foreF", "base": "shoulder", "tip": "handF", "label": "Bras loin"},
	"legN": {"upper": "thighN", "lower": "shinN", "base": "hip", "tip": "ankleN", "label": "Jambe proche"},
	"legF": {"upper": "thighF", "lower": "shinF", "base": "hip", "tip": "ankleF", "label": "Jambe loin"},
}

## Paires proche / loin, pour échanger les côtés.
const SIDE_PAIRS := [["armN", "armF"], ["foreN", "foreF"], ["thighN", "thighF"], ["shinN", "shinF"], ["footN", "footF"]]


static func bone(id: String) -> Dictionary:
	if id == "root":
		return ROOT
	for b in BONES:
		if b.id == id:
			return b
	return {}


static func angle_ids() -> Array:
	var ids := ["root"]
	for b in BONES:
		ids.append(b.id)
	return ids


static func get_style(style) -> Dictionary:
	if style is Dictionary:
		return style
	return STYLES.get(str(style), STYLES.epais)


static func norm180(a: float) -> float:
	a = fposmod(a + 180.0, 360.0) - 180.0
	return 180.0 if is_equal_approx(a, -180.0) else a


static func round2(v: float) -> float:
	return roundf(v * 100.0) / 100.0


## Hauteur du bassin pour que la pose neutre touche le sol.
static func standing_hip_y(style) -> float:
	var s := get_style(style)
	return s.thigh + s.shin + s.stroke / 2.0


static func neutral_pose(style_name := "epais") -> Dictionary:
	var angles := {}
	for id in angle_ids():
		angles[id] = 0.0
	return {"nom": "neutre", "style": style_name, "x": 0.0, "y": standing_hip_y(style_name), "facing": 1, "angles": angles}


## Longueur d'un os dans une pose : longueur du style × étirement éventuel
## (p.etire = {os: facteur}, pour le squash & stretch des images d'action).
static func bone_len(p: Dictionary, s: Dictionary, id: String) -> float:
	var b := bone(id)
	return float(s.get(b.get("len", ""), 0.0)) * float(p.get("etire", {}).get(id, 1.0))


static func clone_pose(p: Dictionary) -> Dictionary:
	return p.duplicate(true)


static func angle(p: Dictionary, id: String) -> float:
	return float(p.angles.get(id, 0.0))


static func facing(p: Dictionary) -> float:
	return -1.0 if float(p.get("facing", 1)) < 0.0 else 1.0


static func clamp_angle(id: String, v: float) -> float:
	var lim: Vector2 = bone(id).lim
	return clampf(v, lim.x, lim.y)


## Cinématique directe. Renvoie :
##   joints : positions des articulations dans le monde (x tient compte de facing)
##   world  : angle absolu de chaque os (degrés, repère du personnage, avant miroir)
##   style, facing, head_r
static func solve(p: Dictionary) -> Dictionary:
	var s := get_style(p.get("style", "epais"))
	var world := {}
	var tip := {}
	world["root"] = ROOT.rest + ROOT.sign * angle(p, "root")
	tip["root"] = Vector2.ZERO
	for b in BONES:
		var w: float = world[b.parent] + b.rest + b.sign * angle(p, b.id)
		world[b.id] = w
		var o: Vector2 = tip[b.parent]
		var l := bone_len(p, s, b.id)
		tip[b.id] = o + Vector2(cos(deg_to_rad(w)), sin(deg_to_rad(w))) * l

	var r: float = s.head / 2.0
	var hw: float = world["neck"]
	var head_dist: float = r * (1.0 - s.get("headSink", 0.0))
	var head: Vector2 = tip["neck"] + Vector2(cos(deg_to_rad(hw)), sin(deg_to_rad(hw))) * head_dist

	var f := facing(p)
	var origin := Vector2(float(p.x), float(p.y))
	var W := func(v: Vector2) -> Vector2: return origin + Vector2(f * v.x, v.y)
	var joints := {
		"hip": W.call(tip["root"]),
		"waist": W.call(tip["spineLow"]),
		"shoulder": W.call(tip["chest"]),
		"neckTop": W.call(tip["neck"]),
		"head": W.call(head),
		"elbowN": W.call(tip["armN"]), "handN": W.call(tip["foreN"]),
		"elbowF": W.call(tip["armF"]), "handF": W.call(tip["foreF"]),
		"kneeN": W.call(tip["thighN"]), "ankleN": W.call(tip["shinN"]), "toeN": W.call(tip["footN"]),
		"kneeF": W.call(tip["thighF"]), "ankleF": W.call(tip["shinF"]), "toeF": W.call(tip["footF"]),
	}
	return {"joints": joints, "world": world, "style": s, "facing": f, "head_r": r}


## Point le plus bas du dessin (en tenant compte de l'épaisseur du trait).
static func lowest_y(p: Dictionary) -> float:
	var sol := solve(p)
	var s: Dictionary = sol.style
	var lo := INF
	for k in sol.joints:
		if k == "head":
			continue
		var rr: float = maxf(s.hand, s.stroke / 2.0) if k in ["handN", "handF"] else s.stroke / 2.0
		lo = minf(lo, sol.joints[k].y - rr)
	return minf(lo, sol.joints["head"].y - sol.head_r)


## Décale la pose verticalement pour que son point le plus bas touche le sol.
static func plant(p: Dictionary) -> Dictionary:
	var q := clone_pose(p)
	q.y = float(q.y) - lowest_y(q)
	return q


## Cinématique inverse à deux os (loi des cosinus) : le bout du membre va vers
## la cible (coordonnées du monde). Des deux sens de pliage possibles, garde
## celui qui respecte les amplitudes, puis le plus proche de la pose actuelle.
static func reach(p: Dictionary, limb_id: String, target: Vector2, limits := true) -> Dictionary:
	var limb: Dictionary = LIMBS[limb_id]
	var q := clone_pose(p)
	var sol := solve(q)
	var s: Dictionary = sol.style
	var f: float = sol.facing
	var up := bone(limb.upper)
	var lo := bone(limb.lower)
	var l1 := bone_len(q, s, limb.upper)
	var l2 := bone_len(q, s, limb.lower)
	var base: Vector2 = sol.joints[limb.base]
	var t := Vector2((target.x - base.x) * f, target.y - base.y)  # repère local, avant miroir
	var d := t.length()
	if d < 1e-6:
		t = Vector2(0, -1)
		d = 1.0
	var dd := clampf(d, absf(l1 - l2) + 1e-6, l1 + l2 - 1e-6)
	var a_t := rad_to_deg(atan2(t.y, t.x))
	var cos_a := (l1 * l1 + dd * dd - l2 * l2) / (2.0 * l1 * dd)
	var alpha := rad_to_deg(acos(clampf(cos_a, -1.0, 1.0)))
	var parent_world: float = sol.world[up.parent]
	var goal := t / d * dd

	var best := {}
	for bend in [1.0, -1.0]:
		var w1: float = a_t + bend * alpha
		var e := Vector2(cos(deg_to_rad(w1)), sin(deg_to_rad(w1))) * l1
		var w2 := rad_to_deg(atan2(goal.y - e.y, goal.x - e.x))
		var a1 := norm180((w1 - parent_world - up.rest) * up.sign)
		var a2 := norm180((w2 - w1 - lo.rest) * lo.sign)
		var pen := 0.0
		if limits:
			pen += maxf(0.0, up.lim.x - a1) + maxf(0.0, a1 - up.lim.y)
			pen += maxf(0.0, lo.lim.x - a2) + maxf(0.0, a2 - lo.lim.y)
			pen *= 1000.0
		pen += absf(norm180(a1 - angle(q, limb.upper))) + absf(norm180(a2 - angle(q, limb.lower)))
		if best.is_empty() or pen < best.pen:
			best = {"a1": a1, "a2": a2, "pen": pen}
	var a1f := round2(best.a1)
	var a2f := round2(best.a2)
	if limits:
		a1f = clamp_angle(limb.upper, a1f)
		a2f = clamp_angle(limb.lower, a2f)
	q.angles[limb.upper] = a1f
	q.angles[limb.lower] = a2f
	return q


## Oriente un os pour qu'il pointe vers un point du monde (cinématique directe
## « à la souris »).
static func aim(p: Dictionary, bone_id: String, target: Vector2, limits := true) -> Dictionary:
	var q := clone_pose(p)
	var sol := solve(q)
	var b := bone(bone_id)
	if bone_id == "root":
		# Le bassin incline tout le tronc : on oriente la ligne bassin → taille.
		var vh: Vector2 = target - sol.joints.hip
		if vh.length() < 1e-6:
			return q
		var wh := rad_to_deg(atan2(vh.y, vh.x * sol.facing))
		var w_root: float = wh - (sol.world.spineLow - sol.world.root)
		var ar := round2(norm180((w_root - ROOT.rest) * ROOT.sign))
		q.angles.root = clamp_angle("root", ar) if limits else ar
		return q
	var start_joint := {"spineLow": "hip", "chest": "waist", "neck": "shoulder", "armN": "shoulder", "armF": "shoulder",
		"foreN": "elbowN", "foreF": "elbowF", "thighN": "hip", "thighF": "hip", "shinN": "kneeN", "shinF": "kneeF"}
	if not start_joint.has(bone_id):
		return q
	var o: Vector2 = sol.joints[start_joint[bone_id]]
	var v := Vector2((target.x - o.x) * sol.facing, target.y - o.y)
	if v.length() < 1e-6:
		return q
	var w := rad_to_deg(atan2(v.y, v.x))
	var a := round2(norm180((w - sol.world[b.parent] - b.rest) * b.sign))
	q.angles[bone_id] = clamp_angle(bone_id, a) if limits else a
	return q


## Échange les membres proches et lointains (utile pour alterner la garde).
static func swap_sides(p: Dictionary) -> Dictionary:
	var q := clone_pose(p)
	for pr in SIDE_PAIRS:
		var tmp = q.angles.get(pr[0], 0.0)
		q.angles[pr[0]] = q.angles.get(pr[1], 0.0)
		q.angles[pr[1]] = tmp
	return q


## Mélange deux poses (t entre 0 et 1), angle par angle, par le plus court chemin.
static func lerp_pose(a: Dictionary, b: Dictionary, t: float) -> Dictionary:
	var q := clone_pose(a)
	q.x = lerpf(float(a.x), float(b.x), t)
	q.y = lerpf(float(a.y), float(b.y), t)
	for k in b.angles:
		var va := angle(a, k)
		q.angles[k] = va + norm180(angle(b, k) - va) * t
	var ea: Dictionary = a.get("etire", {})
	var eb: Dictionary = b.get("etire", {})
	if not ea.is_empty() or not eb.is_empty():
		var e := {}
		for k in ea.keys() + eb.keys():
			e[k] = lerpf(float(ea.get(k, 1.0)), float(eb.get(k, 1.0)), t)
		q.etire = e
	return q


## Articulations hors amplitude humaine : [{id, label, value, lim}].
static func violations(p: Dictionary) -> Array:
	var out := []
	for id in angle_ids():
		var v := angle(p, id)
		var b := bone(id)
		if v < b.lim.x or v > b.lim.y:
			out.append({"id": id, "label": b.label, "value": v, "lim": b.lim})
	return out


# ---------- Dessin ----------

## Primitives de dessin, de l'arrière vers l'avant, en coordonnées du monde
## (y vers le haut). far_shade < 1 assombrit les membres lointains.
static func primitives(p: Dictionary, color := Color("#111111"), far_shade := 1.0) -> Array:
	var sol := solve(p)
	var J: Dictionary = sol.joints
	var s: Dictionary = sol.style
	var far := color if is_equal_approx(far_shade, 1.0) else Color(color.r * far_shade, color.g * far_shade, color.b * far_shade, color.a)
	var w: float = s.stroke
	var out := []
	var leg := func(side: String, c: Color) -> void:
		var pts := [J.hip, J["knee" + side], J["ankle" + side]]
		if s.foot > 0.0:
			pts.append(J["toe" + side])
		out.append({"type": "path", "points": pts, "width": w, "color": c, "part": "leg" + side})
	var arm := func(side: String, c: Color) -> void:
		out.append({"type": "path", "points": [J.shoulder, J["elbow" + side], J["hand" + side]], "width": w, "color": c, "part": "arm" + side})
		if s.hand > w / 2.0:
			out.append({"type": "circle", "c": J["hand" + side], "r": s.hand, "color": c, "part": "hand" + side})
	arm.call("F", far)
	leg.call("F", far)
	var torso := [J.hip, J.waist, J.shoulder]
	if s.neck > 0.0:
		torso.append(J.neckTop)
	out.append({"type": "path", "points": torso, "width": w, "color": color, "part": "torso"})
	out.append({"type": "circle", "c": J.head, "r": sol.head_r, "color": color, "part": "head"})
	leg.call("N", color)
	arm.call("N", color)
	return out


## Monde (y vers le haut) → écran Godot (y vers le bas).
## origin = position écran du point (0, 0) du monde ; scale = pixels par unité.
static func to_screen(v: Vector2, origin: Vector2, scale: float) -> Vector2:
	return origin + Vector2(v.x, -v.y) * scale


## Dessine une pose sur n'importe quel CanvasItem (à appeler depuis _draw).
## Traits à bouts et jointures ronds : segments + disques aux articulations.
static func draw_pose(ci: CanvasItem, p: Dictionary, origin: Vector2, scale: float, color := Color("#111111"), far_shade := 1.0) -> void:
	for pr in primitives(p, color, far_shade):
		if pr.type == "path":
			var w: float = pr.width * scale
			var pts := PackedVector2Array()
			for v in pr.points:
				pts.append(to_screen(v, origin, scale))
			for i in range(pts.size() - 1):
				ci.draw_line(pts[i], pts[i + 1], pr.color, w, true)
			for v in pts:
				ci.draw_circle(v, w / 2.0, pr.color)
		else:
			ci.draw_circle(to_screen(pr.c, origin, scale), pr.r * scale, pr.color)


# ---------- Fichiers ----------

static func load_pose(path: String) -> Dictionary:
	var txt := FileAccess.get_file_as_string(path)
	var data = JSON.parse_string(txt)
	if not (data is Dictionary) or not data.has("angles"):
		push_error("Pose illisible : " + path)
		return neutral_pose()
	return normalize(data)


## Complète une pose venue d'un JSON (angles manquants, facing entier).
static func normalize(data: Dictionary) -> Dictionary:
	var p := neutral_pose(str(data.get("style", "epais")))
	p.nom = str(data.get("nom", "sans nom"))
	p.x = float(data.get("x", 0.0))
	p.y = float(data.get("y", p.y))
	p.facing = -1 if float(data.get("facing", 1)) < 0.0 else 1
	for k in data.angles:
		p.angles[k] = float(data.angles[k])
	return p


static func to_json(p: Dictionary) -> String:
	var out := {"nom": p.nom, "style": p.style, "x": round2(float(p.x)), "y": round2(float(p.y)), "facing": int(p.facing), "angles": {}}
	for id in angle_ids():
		var v := round2(angle(p, id))
		out.angles[id] = int(v) if is_equal_approx(v, roundf(v)) else v
	return JSON.stringify(out, "  ", false) + "\n"


static func save_pose(p: Dictionary, path: String) -> Error:
	var f := FileAccess.open(path, FileAccess.WRITE)
	if f == null:
		return FileAccess.get_open_error()
	f.store_string(to_json(p))
	return OK
