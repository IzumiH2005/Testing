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
		"spineLow": 22.0, "chest": 24.0,
		"upperArm": 34.0, "forearm": 32.0,
		"thigh": 41.0, "shin": 42.0,
		"foot": 10.0,      # pied : petit crochet du trait, de la cheville vers l'avant
	},
	"fin": {
		"label": "Fin (petite tête, trait léger)",
		"head": 33.0, "headSink": 0.0, "stroke": 11.0, "hand": 7.0, "neck": 3.0,
		"spineLow": 27.0, "chest": 27.0,
		"upperArm": 30.0, "forearm": 28.0,
		"thigh": 44.0, "shin": 44.0,
		"foot": 8.0,
	},
}

## Bassin : son angle incline tout le tronc (les jambes n'en dépendent pas).
## Le bassin porte l'orientation de tout le tronc dans l'espace (pas une
## articulation) : un corps qui roule ou tombe tête en bas dépasse 90°.
const ROOT := {"id": "root", "rest": 90.0, "sign": -1.0, "lim": Vector2(-720, 720), "label": "Bascule du bassin"}

## Hiérarchie des os, parents avant enfants. rest = angle de repos relatif au
## parent (degrés, sens trigonométrique, y vers le haut) ; sign = conversion
## angle sémantique → trigonométrique ; lim = amplitude articulaire humaine
## (AAOS, voir RECHERCHE.md), en angle sémantique.
const BONES := [
	{"id": "spineLow", "parent": "root",     "len": "spineLow", "rest": 0.0,   "sign": -1.0, "lim": Vector2(-25, 45),  "label": "Bas du dos"},
	{"id": "chest",    "parent": "spineLow", "len": "chest",    "rest": 0.0,   "sign": -1.0, "lim": Vector2(-25, 45),  "label": "Poitrine"},
	{"id": "neck",     "parent": "chest",    "len": "neck",     "rest": 0.0,   "sign": -1.0, "lim": Vector2(-60, 50),  "label": "Cou / tête"},
	{"id": "armF",     "parent": "chest",    "len": "upperArm", "rest": 180.0, "sign": 1.0,  "lim": Vector2(-180, 180), "label": "Épaule (loin)"},
	{"id": "foreF",    "parent": "armF",     "len": "forearm",  "rest": 0.0,   "sign": 1.0,  "lim": Vector2(0, 150),   "label": "Coude (loin)"},
	{"id": "armN",     "parent": "chest",    "len": "upperArm", "rest": 180.0, "sign": 1.0,  "lim": Vector2(-180, 180), "label": "Épaule (proche)"},
	{"id": "foreN",    "parent": "armN",     "len": "forearm",  "rest": 0.0,   "sign": 1.0,  "lim": Vector2(0, 150),   "label": "Coude (proche)"},
	{"id": "thighF",   "parent": "root",     "len": "thigh",    "rest": 180.0, "sign": 1.0,  "lim": Vector2(-30, 140), "label": "Hanche (loin)"},
	{"id": "shinF",    "parent": "thighF",   "len": "shin",     "rest": 0.0,   "sign": -1.0, "lim": Vector2(0, 150),   "label": "Genou (loin)"},
	{"id": "footF",    "parent": "shinF",    "len": "foot",     "rest": 90.0,  "sign": 1.0,  "lim": Vector2(-50, 65),  "label": "Cheville (loin)"},
	{"id": "thighN",   "parent": "root",     "len": "thigh",    "rest": 180.0, "sign": 1.0,  "lim": Vector2(-30, 140), "label": "Hanche (proche)"},
	{"id": "shinN",    "parent": "thighN",   "len": "shin",     "rest": 0.0,   "sign": -1.0, "lim": Vector2(0, 150),   "label": "Genou (proche)"},
	{"id": "footN",    "parent": "shinN",    "len": "foot",     "rest": 90.0,  "sign": 1.0,  "lim": Vector2(-50, 65),  "label": "Cheville (proche)"},
]

## Troisième dimension (« 2D et demie ») : la vue reste de profil, mais chaque
## os peut sortir du plan de l'écran. On ne voit que la projection : un os qui
## pointe vers la caméra raccourcit, et l'ordre de dessin suit la profondeur.
##   <os>_p         profondeur de l'os : rotation hors du plan, en degrés,
##                  positive = vers la caméra (comme pose.z négatif). Elle se
##                  transmet aux os enfants, comme les angles dans le plan.
##   torsion        rotation du buste autour de la colonne (épaules), relative
##                  au bassin ; positif = l'épaule proche passe devant
##   torsionBassin  rotation du bassin autour de la colonne (hanches)
##   lacet          tout le corps tourne autour de la verticale ; positif = il
##                  se tourne vers la caméra (vue de trois quarts)
## Avec tout à 0, le dessin est exactement celui du profil plat.
const TWISTS := [
	# Torsion du tronc entre bassin et épaules : 45° de chaque côté au total,
	# répartie 20 % dans le bas du dos (lombaires), 80 % dans le thorax.
	{"id": "torsion", "lim": Vector2(-45, 45), "label": "Torsion des épaules"},
	# Rotation du bassin sur les hanches (les pieds restent posés) : 60°.
	{"id": "torsionBassin", "lim": Vector2(-60, 60), "label": "Torsion du bassin"},
	{"id": "lacet", "lim": Vector2(-180, 180), "label": "Corps tourné vers la caméra"},
	# Omoplate (ceinture scapulaire) : déplacement de l'épaule, en unités.
	{"id": "epauleN_av", "lim": Vector2(-7, 7), "label": "Épaule proche : avance (+) / recule (−)"},
	{"id": "epauleF_av", "lim": Vector2(-7, 7), "label": "Épaule loin : avance (+) / recule (−)"},
	{"id": "epauleN_haut", "lim": Vector2(-3, 7), "label": "Épaule proche : haussée (+) / abaissée (−)"},
	{"id": "epauleF_haut", "lim": Vector2(-3, 7), "label": "Épaule loin : haussée (+) / abaissée (−)"},
]
const SCAPULA := ["epauleN_av", "epauleF_av", "epauleN_haut", "epauleF_haut"]
const PROF := "_p"
## Rotation d'un membre autour de son propre axe (bras : rotation de
## l'humérus, cuisse : rotation du fémur). Elle oriente le plan dans lequel le
## coude ou le genou se plie : coude vers le bas, vers l'extérieur, vers
## l'arrière. Positif = le coude (genou) part vers la caméra.
const ROT := "_r"
## Coude, genou : charnières. Ils ne plient que dans un plan (celui que donne
## la rotation du segment parent) : pas de profondeur propre.
const CHARNIERES := ["foreN", "foreF", "shinN", "shinF"]
## Limites des canaux 3D (degrés), par « canal:os sans côté ». Profondeur du
## bras : vers la caméra = abduction (bras écarté du corps, jusqu'à 90°), à
## l'opposé = adduction (bras qui passe devant le buste, 40°). Cuisse :
## abduction 45°, adduction 30°. Rotation du bras ±80°, de la cuisse ±45°.
## Buste et bassin : inclinaison latérale ±30°. Cheville : ±25°.
const LIM_3D := {
	"_p:arm": Vector2(-90, 90), "_p:thigh": Vector2(-30, 45), "_p:root": Vector2(-30, 30),
	"_p:spineLow": Vector2(-30, 30), "_p:chest": Vector2(-30, 30), "_p:neck": Vector2(-40, 40),
	"_p:foot": Vector2(-25, 25), "_r:arm": Vector2(-80, 80), "_r:thigh": Vector2(-45, 45),
	"_r:neck": Vector2(-80, 80),
}

## Chaînes à deux os pour la cinématique inverse.
const LIMBS := {
	"armN": {"upper": "armN", "lower": "foreN", "base": "shoulderN", "tip": "handN", "label": "Bras proche"},
	"armF": {"upper": "armF", "lower": "foreF", "base": "shoulderF", "tip": "handF", "label": "Bras loin"},
	"legN": {"upper": "thighN", "lower": "shinN", "base": "hipN", "tip": "ankleN", "label": "Jambe proche"},
	"legF": {"upper": "thighF", "lower": "shinF", "base": "hipF", "tip": "ankleF", "label": "Jambe loin"},
}

## Paires proche / loin, pour échanger les côtés.
const SIDE_PAIRS := [["armN", "armF"], ["foreN", "foreF"], ["thighN", "thighF"], ["shinN", "shinF"], ["footN", "footF"],
	["epauleN_av", "epauleF_av"], ["epauleN_haut", "epauleF_haut"]]


static func bone(id: String) -> Dictionary:
	if id == "root":
		return ROOT
	for b in BONES:
		if b.id == id:
			return b
	for t in TWISTS:
		if t.id == id:
			return t
	if id.ends_with(PROF) or id.ends_with(ROT):
		var base_id := id.trim_suffix(PROF).trim_suffix(ROT)
		var b0 := bone(base_id)
		if not b0.is_empty():
			var lim: Vector2 = LIM_3D.get(id.right(2) + ":" + base_id.rstrip("NF"), Vector2(-90, 90))
			return {"id": id, "lim": lim, "label": ("Rotation : " if id.ends_with(ROT) else "Profondeur : ") + str(b0.label)}
	return {}


static func angle_ids() -> Array:
	var ids := ["root"]
	for b in BONES:
		ids.append(b.id)
	for t in TWISTS:
		ids.append(t.id)
	ids.append("root" + PROF)
	for b in BONES:
		if not b.id in CHARNIERES:
			ids.append(b.id + PROF)
	for b in BONES:
		if b.id.begins_with("arm") or b.id.begins_with("thigh") or b.id == "neck":
			ids.append(b.id + ROT)
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
	var basis := {}
	var base3 := {}
	var deg := func(a: float) -> float: return deg_to_rad(a)
	var RZ := func(a: float) -> Basis: return Basis(Vector3(0, 0, 1), deg.call(a))
	var RY := func(a: float) -> Basis: return Basis(Vector3(0, 1, 0), deg.call(a))
	var RX := func(a: float) -> Basis: return Basis(Vector3(1, 0, 0), deg.call(a))
	var root_w: float = ROOT.rest + ROOT.sign * angle(p, "root")
	basis["root"] = RY.call(angle(p, "lacet")) * RZ.call(root_w) * RY.call(angle(p, "root" + PROF)) * RX.call(-angle(p, "torsionBassin"))
	tip["root"] = Vector3.ZERO
	for b in BONES:
		# Charnière (coude, genou) : aucune profondeur propre.
		var prof_os: float = 0.0 if b.id in CHARNIERES else angle(p, b.id + PROF)
		var B: Basis = basis[b.parent] * RZ.call(b.rest + b.sign * angle(p, b.id)) * RY.call(prof_os)
		if b.id.begins_with("arm") or b.id.begins_with("thigh"):
			B = B * RX.call(angle(p, b.id + ROT))
		if b.id == "spineLow":
			B = B * RX.call(-0.2 * angle(p, "torsion"))
		if b.id == "chest":
			B = B * RX.call(-0.8 * angle(p, "torsion"))
		if b.id == "neck":
			B = B * RX.call(-angle(p, "neck" + ROT))
		basis[b.id] = B
		var o3: Vector3 = tip[b.parent]
		if b.id.begins_with("arm"):
			# Omoplate : l'épaule avance (vers l'avant du thorax) ou monte.
			var side: String = b.id.substr(3)
			var Bc: Basis = basis["chest"]
			o3 = o3 + (-Bc.y) * angle(p, "epaule%s_av" % side) + Bc.x * angle(p, "epaule%s_haut" % side)
			base3[b.id] = o3
		tip[b.id] = o3 + B.x * bone_len(p, s, b.id)
	# Angle projeté de chaque os (pour la cinématique inverse, qui reste dans le plan).
	world["root"] = rad_to_deg(atan2(basis["root"].x.y, basis["root"].x.x))
	for b in BONES:
		var v: Vector3 = basis[b.id].x
		world[b.id] = rad_to_deg(atan2(v.y, v.x)) if Vector2(v.x, v.y).length() > 1e-6 else world[b.parent] + b.rest
	var r: float = s.head / 2.0
	var head_dist: float = r * (1.0 - s.get("headSink", 0.0))
	var head3: Vector3 = tip["neck"] + basis["neck"].x * head_dist

	var f := facing(p)
	var origin := Vector2(float(p.x), float(p.y))
	var W := func(v: Vector3) -> Vector2: return origin + Vector2(f * v.x, v.y)
	var pts3 := {
		"hip": tip["root"], "waist": tip["spineLow"], "shoulder": tip["chest"], "neckTop": tip["neck"], "head": head3,
		"elbowN": tip["armN"], "handN": tip["foreN"], "elbowF": tip["armF"], "handF": tip["foreF"],
		"kneeN": tip["thighN"], "ankleN": tip["shinN"], "toeN": tip["footN"],
		"kneeF": tip["thighF"], "ankleF": tip["shinF"], "toeF": tip["footF"],
	}
	var joints := {}
	var prof := {}
	for k in pts3:
		joints[k] = W.call(pts3[k])
		prof[k] = float(pts3[k].z)
	# Les membres partent d'un seul point du tronc : ils en sont le prolongement.
	# Seule l'omoplate déplace un peu l'épaule (7 unités au plus, moins que la
	# demi-épaisseur du trait : le bras reste attaché au buste).
	for side in ["N", "F"]:
		joints["shoulder" + side] = W.call(base3["arm" + side])
		joints["hip" + side] = joints.hip
		prof["shoulder" + side] = float(base3["arm" + side].z)
		prof["hip" + side] = prof.hip
	return {"joints": joints, "prof": prof, "basis": basis, "world": world, "style": s, "facing": f, "head_r": r}


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


# ---------- Pieds ----------
# Le pied part de la cheville vers l'avant. On le règle par son angle « absolu »
# phi dans le repère du personnage : 0 = à plat vers l'avant, négatif = pointe
# vers le bas (sur la pointe, pied tendu), positif = pointe relevée (talon).

## Angle absolu du pied (degrés, repère du personnage).
static func foot_phi(p: Dictionary, side: String) -> float:
	var sol := solve(p)
	return float(sol.world["foot" + side])


## Oriente le pied à l'angle absolu phi (dans les amplitudes de la cheville).
static func set_foot(p: Dictionary, side: String, phi: float, limits := true) -> void:
	var sol := solve(p)
	var b := bone("foot" + side)
	var a := norm180((phi - float(sol.world["shin" + side]) - b.rest) * b.sign)
	p.angles["foot" + side] = clamp_angle("foot" + side, a) if limits else a


## Le pied du stickman est un seul segment, de la cheville à la pointe : sur
## la plante (talon levé), il représente l'avant-pied, et l'angle mesuré
## additionne la cheville (20° de flexion dorsale) et les orteils repliés
## (jusqu'à 70°). D'où la limite à 65° de la cheville dans BONES.
## Flexion maximale de la cheville (pointe vers le tibia), en degrés.
const MAX_DORSI := 30.0

## Le pied ne passe jamais sous le sol : si la pointe s'enfonce, le pied
## pivote autour de la cheville jusqu'à poser la pointe (talon levé).
## Si le pied posé à plat demanderait une cheville pliée au-delà de
## MAX_DORSI (tibia très incliné vers l'arrière, comme la jambe arrière de la
## garde), le talon se lève : le pied pivote autour de la pointe, qui reste
## au sol, et la jambe suit la cheville.
static func ground_feet(p: Dictionary) -> void:
	var s := get_style(p.get("style", "epais"))
	var L: float = s.foot
	if L <= 0.0:
		return
	var g: float = s.stroke / 2.0
	for side in ["N", "F"]:
		var sol := solve(p)
		var ank: Vector2 = sol.joints["ankle" + side]
		var toe: Vector2 = sol.joints["toe" + side]
		if toe.y < g - 0.01:
			var h := clampf((ank.y - g) / L, -1.0, 1.0)
			set_foot(p, side, -rad_to_deg(asin(h)), false)
			toe = solve(p).joints["toe" + side]
		if angle(p, "foot" + side) > MAX_DORSI + 0.01 and toe.y < g + 0.5:
			var T := Vector2(toe.x, g)
			var f: float = sol.facing
			var base := clone_pose(p)
			# Bissection sur l'angle du pied phi (pointe au sol en T) : la
			# cheville se place en T - L·dir(phi), la jambe la rejoint, et on
			# cherche phi tel que la cheville soit pliée de MAX_DORSI.
			var lo := -85.0
			var hi := 0.0
			var q := base
			for it in 16:
				var phi := (lo + hi) / 2.0
				var A := T - Vector2(f * cos(deg_to_rad(phi)), sin(deg_to_rad(phi))) * L
				q = reach(base, "leg" + side, A)
				set_foot(q, side, phi, false)
				if angle(q, "foot" + side) > MAX_DORSI:
					hi = phi
				else:
					lo = phi
			p.angles["thigh" + side] = q.angles["thigh" + side]
			p.angles["shin" + side] = q.angles["shin" + side]
			p.angles["foot" + side] = q.angles["foot" + side]


## Pieds d'une pose isolée (sans trajectoire) : à plat si la cheville est au
## sol, sinon relâchés (pointe légèrement tendue) ; jamais sous le sol.
static func auto_feet(p: Dictionary) -> Dictionary:
	var q := clone_pose(p)
	var s := get_style(q.get("style", "epais"))
	if s.foot <= 0.0:
		return q
	var g: float = s.stroke / 2.0
	for side in ["N", "F"]:
		var sol := solve(q)
		var h: float = sol.joints["ankle" + side].y - g
		if h < 0.8:
			set_foot(q, side, 0.0, false)
		else:
			q.angles["foot" + side] = -15.0
	ground_feet(q)
	return q


## Cinématique inverse à deux os (loi des cosinus) : le bout du membre va vers
## la cible (coordonnées du monde). Des deux sens de pliage possibles, garde
## celui qui respecte les amplitudes, puis le plus proche de la pose actuelle.
## coude = "haut", "bas", "avant" ou "arriere" : impose le côté où pointe le
## coude (ou le genou), vu à l'écran, sans tenir compte des amplitudes. En
## profil, un bras tourné (coude écarté, poing à l'oreille) se dessine comme
## un coude plié « à l'envers » : c'est ce que permet ce choix.
static func reach(p: Dictionary, limb_id: String, target: Vector2, limits := true, coude := "") -> Dictionary:
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
		if coude != "":
			# Position du coude dans le repère local (x vers l'avant, y vers le haut).
			var dir := {"haut": Vector2(0, 1), "bas": Vector2(0, -1), "avant": Vector2(1, 0), "arriere": Vector2(-1, 0)}
			pen += -e.dot(dir.get(coude, Vector2.ZERO)) * 10.0
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
	# Avec de la profondeur (os hors du plan, torsion, lacet), le calcul à plat
	# n'est plus exact : on corrige les deux angles par petits pas, en mesurant
	# le bout du membre sur la projection réelle.
	if _hors_plan(q):
		q = _affine(q, limb, target, limits, [limb.upper, limb.lower])
		# Hors de portée (le membre pointe en partie vers la caméra ou à
		# l'opposé) : on laisse aussi la profondeur du premier os se corriger,
		# comme un vrai bras qui se tend vers une cible devant lui.
		if solve(q).joints[limb.tip].distance_to(target) > 1.0:
			q = _affine(q, limb, target, limits, [limb.upper, limb.lower, limb.upper + PROF])
	return q


static func _hors_plan(p: Dictionary) -> bool:
	for k in p.angles:
		if (k in ["torsion", "torsionBassin", "lacet"] or str(k).ends_with(PROF) or str(k).ends_with(ROT)) and absf(float(p.angles[k])) > 0.01:
			return true
	return false


## Descente de gradient sur les deux angles du membre : le bout projeté va
## vers la cible. Garde le sens de pliage de départ (on part de la solution
## à plat, et les pas restent petits).
static func _affine(p: Dictionary, limb: Dictionary, target: Vector2, limits: bool, ids: Array) -> Dictionary:
	# Gauss-Newton amorti : jacobien numérique du bout du membre (projeté) par
	# rapport aux angles, quelques itérations suffisent (bien plus rapide que
	# la recherche pas à pas, qui appelait solve des centaines de fois).
	var q := clone_pose(p)
	var tip: String = limb.tip
	var bout := func(pp: Dictionary) -> Vector2: return solve(pp).joints[tip]
	var cur: Vector2 = bout.call(q)
	for it in 12:
		var r: Vector2 = target - cur
		if r.length_squared() < 0.05:
			break
		var cols := []
		for id in ids:
			var t := clone_pose(q)
			t.angles[id] = float(t.angles.get(id, 0.0)) + 0.5
			cols.append((bout.call(t) - cur) / 0.5)
		# Moindres carrés amortis : (JᵀJ + λI) δ = Jᵀ r, résolu par descente
		# sur chaque colonne (2 ou 3 inconnues).
		var n := ids.size()
		var A := []
		var b := []
		for a in n:
			var row := []
			for c in n:
				row.append(cols[a].dot(cols[c]) + (0.05 if a == c else 0.0))
			A.append(row)
			b.append(cols[a].dot(r))
		var dlt := _resout(A, b)
		var q2 := clone_pose(q)
		for k in n:
			var id: String = ids[k]
			var v: float = float(q2.angles.get(id, 0.0)) + clampf(float(dlt[k]), -25.0, 25.0)
			if limits:
				v = clamp_angle(id, v)
			q2.angles[id] = v
		var c2: Vector2 = bout.call(q2)
		if c2.distance_squared_to(target) >= cur.distance_squared_to(target):
			break
		q = q2
		cur = c2
	if limits:
		for v in amplitudes(q):
			if str(v.id) == str(limb.upper):
				return p
	for id in ids:
		q.angles[id] = round2(float(q.angles.get(id, 0.0)))
	return q


## Petit système linéaire (Gauss), n ≤ 3.
static func _resout(A: Array, b: Array) -> Array:
	var n := b.size()
	var M := []
	for i in n:
		M.append(A[i].duplicate() + [b[i]])
	for c in n:
		var piv := c
		for r in range(c + 1, n):
			if absf(M[r][c]) > absf(M[piv][c]):
				piv = r
		var tmp = M[c]; M[c] = M[piv]; M[piv] = tmp
		if absf(M[c][c]) < 1e-9:
			return b.map(func(_x): return 0.0)
		for r in n:
			if r != c:
				var k: float = M[r][c] / M[c][c]
				for cc in range(c, n + 1):
					M[r][cc] -= k * M[c][cc]
	var x := []
	for i in n:
		x.append(M[i][n] / M[i][i])
	return x


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
	var start_joint := {"spineLow": "hip", "chest": "waist", "neck": "shoulder", "armN": "shoulderN", "armF": "shoulderF",
		"foreN": "elbowN", "foreF": "elbowF", "thighN": "hipN", "thighF": "hipF", "shinN": "kneeN", "shinF": "kneeF",
		"footN": "ankleN", "footF": "ankleF"}
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
	for t in TWISTS:
		if not t.id in SCAPULA:
			q.angles[t.id] = -float(q.angles.get(t.id, 0.0))
	for suf in [PROF, ROT]:
		for pr in SIDE_PAIRS:
			var a: String = pr[0] + suf
			var b: String = pr[1] + suf
			var tmp2 = q.angles.get(a, 0.0)
			q.angles[a] = q.angles.get(b, 0.0)
			q.angles[b] = tmp2
	return q


## Mélange deux poses (t entre 0 et 1), angle par angle, par le plus court chemin.
## Côté opposé d'un os (armN ↔ armF…), ou l'os lui-même s'il est central.
static func other_side(id: String) -> String:
	if id.ends_with(PROF):
		return other_side(id.trim_suffix(PROF)) + PROF
	if id.ends_with(ROT):
		return other_side(id.trim_suffix(ROT)) + ROT
	for pr in SIDE_PAIRS:
		if id == pr[0]:
			return pr[1]
		if id == pr[1]:
			return pr[0]
	return id


## Canal qui porte la même information dans la pose miroir, et son signe :
## [canal, signe]. Voir mirror_pose.
static func mirror_channel(c: String) -> Array:
	if c == "x" or c == "y" or c == "z":
		return [c, 1.0]
	if c.begins_with("etire:"):
		return ["etire:" + other_side(c.substr(6)), 1.0]
	if c in SCAPULA:
		return [other_side(c), 1.0]
	return [other_side(c), 1.0 if (c.begins_with("foot") and not c.ends_with(PROF)) else -1.0]


## Même dessin, décrit depuis l'autre côté : sens inversé, proche et loin
## échangés, chaque angle changé de signe (tous les repos valent 0 ou 180,
## donc le symétrique d'un angle relatif est son opposé). Seuls les pieds
## ne suivent pas le miroir : ils pointent toujours vers l'avant. C'est la
## pose d'un personnage vu exactement de face ou de dos, au moment où il se
## retourne : ce qui était proche passe derrière.
static func mirror_pose(p: Dictionary) -> Dictionary:
	var q := clone_pose(p)
	q.facing = -int(facing(p))
	for id in angle_ids():
		var mc := mirror_channel(id)
		q.angles[id] = float(mc[1]) * angle(p, mc[0])
	if p.has("etire"):
		var e := {}
		for k in p.etire:
			e[other_side(k)] = float(p.etire[k])
		q.etire = e
	return q


static func lerp_pose(a: Dictionary, b: Dictionary, t: float) -> Dictionary:
	if facing(a) != facing(b):
		b = mirror_pose(b)
	var q := clone_pose(a)
	q.x = lerpf(float(a.x), float(b.x), t)
	q.y = lerpf(float(a.y), float(b.y), t)
	if a.has("z") or b.has("z"):
		q.z = lerpf(float(a.get("z", 0.0)), float(b.get("z", 0.0)), t)
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


## Amplitudes des rotules (épaule, hanche) : la direction du bras ou de la
## cuisse doit rester dans la zone qu'atteint un vrai corps (voir
## analyses/anatomie.md). Renvoie [{id, label}] des articulations hors zone.
static func amplitudes(p: Dictionary) -> Array:
	var out := []
	var sol := solve(p)
	var B: Dictionary = sol.basis
	for side in ["N", "F"]:
		var sg := -1.0 if side == "N" else 1.0
		var nom := "proche" if side == "N" else "loin"
		# Repère du thorax : avant, haut, dehors (côté du membre).
		var Bc: Basis = B["chest"]
		var d: Vector3 = B["arm" + side].x
		var fw := d.dot(-Bc.y)
		var up := d.dot(Bc.x)
		var ou := d.dot(Bc.z * sg)
		# Angle entre le bras et la verticale basse (bras pendant = 0).
		var depuis_bas := rad_to_deg(acos(clampf(-up, -1.0, 1.0)))
		if absf(up) < 0.85 and Vector2(fw, ou).length() > 0.2:
			var az := rad_to_deg(atan2(ou, fw))
			# Croisé devant : vers l'avant (pas un bras derrière le corps, déjà
			# traité plus bas) et plus de 55° vers l'intérieur.
			if az < -55.0 and az > -125.0:
				out.append({"id": "arm" + side, "label": "bras %s croisé trop loin devant le buste" % nom})
			# Vers l'arrière : jusqu'à 60° depuis le bras pendant (extension),
			# ou jusqu'à 40° derrière le côté quand le bras est écarté.
			elif az > 130.0 and depuis_bas > 62.0:
				out.append({"id": "arm" + side, "label": "bras %s trop loin derrière" % nom})
		if fw < -0.3 and ou < -0.3 and up > -0.9:
			out.append({"id": "arm" + side, "label": "bras %s derrière le dos, de l'autre côté" % nom})
		# Hanche, dans le repère du bassin.
		var Br: Basis = B["root"]
		var t: Vector3 = B["thigh" + side].x
		var fl := rad_to_deg(atan2(t.dot(-Br.y), t.dot(-Br.x)))
		var ab := rad_to_deg(asin(clampf(t.dot(Br.z * sg), -1.0, 1.0)))
		# Flexion de hanche genou plié : 135° (passive, jusqu'à 140).
		if fl > 136.0:
			out.append({"id": "thigh" + side, "label": "cuisse %s trop fléchie" % nom})
		elif fl < -35.0:
			out.append({"id": "thigh" + side, "label": "cuisse %s trop loin derrière" % nom})
		if ab > 50.0:
			out.append({"id": "thigh" + side, "label": "cuisse %s trop écartée" % nom})
		elif ab < -35.0:
			out.append({"id": "thigh" + side, "label": "cuisse %s croisée trop loin" % nom})
	return out


## Articulations hors amplitude humaine : [{id, label, value, lim}].
static func violations(p: Dictionary) -> Array:
	var out := []
	for id in angle_ids():
		var v := angle(p, id)
		var b := bone(id)
		# Rotules et orientation (épaule, bassin) : l'angle se lit modulo 360.
		if id.begins_with("arm") and not id.ends_with(PROF) and not id.ends_with(ROT):
			v = norm180(v)
		if v < b.lim.x or v > b.lim.y:
			out.append({"id": id, "label": b.label, "value": v, "lim": b.lim})
	return out


# ---------- Dessin ----------

## Primitives de dessin, de l'arrière vers l'avant, en coordonnées du monde
## (y vers le haut). far_shade < 1 assombrit les membres lointains.
static func primitives(p: Dictionary, color := Color("#111111"), far_shade := 1.0) -> Array:
	var sol := solve(p)
	var J: Dictionary = sol.joints
	var Z: Dictionary = sol.prof
	var s: Dictionary = sol.style
	var far := color if is_equal_approx(far_shade, 1.0) else Color(color.r * far_shade, color.g * far_shade, color.b * far_shade, color.a)
	var w: float = s.stroke
	# Ordre de dessin : profondeur réelle du segment (positive = loin) plus un
	# décalage de base qui donne l'ordre du profil plat (bras loin, jambe loin,
	# tronc, tête, jambe proche, bras proche). Tant qu'aucun os ne sort du
	# plan, l'ordre reste exactement celui-là.
	var items := []
	var seg := func(a: String, b: String, base: float, c: Color, part: String) -> void:
		items.append({"z": base + (Z[a] + Z[b]) / 2.0, "type": "path", "points": [J[a], J[b]], "width": w, "color": c, "part": part})
	for side in ["F", "N"]:
		var c := far if side == "F" else color
		var ba := 30.0 if side == "F" else -30.0
		var bl := 20.0 if side == "F" else -20.0
		seg.call("hip", "knee" + side, bl, c, "leg" + side)
		var lower := ["knee" + side, "ankle" + side]
		if s.foot > 0.0:
			lower.append("toe" + side)
		items.append({"z": bl + (Z["knee" + side] + Z["ankle" + side]) / 2.0, "type": "path", "points": lower.map(func(k): return J[k]),
			"width": w, "color": c, "part": "leg" + side})
		seg.call("shoulder" + side, "elbow" + side, ba, c, "arm" + side)
		seg.call("elbow" + side, "hand" + side, ba, c, "arm" + side)
		if s.hand > w / 2.0:
			items.append({"z": ba + Z["hand" + side] - 0.01, "type": "circle", "c": J["hand" + side], "r": s.hand, "color": c, "part": "hand" + side})
	var torso := [J.hip, J.waist, J.shoulder]
	if s.neck > 0.0:
		torso.append(J.neckTop)
	items.append({"z": (Z.hip + Z.shoulder) / 2.0, "type": "path", "points": torso, "width": w, "color": color, "part": "torso"})
	items.append({"z": Z.head - 1.0, "type": "circle", "c": J.head, "r": sol.head_r, "color": color, "part": "head"})
	# Tri stable, du plus loin au plus proche.
	for i in items.size():
		items[i].rang = i
	items.sort_custom(func(a, b): return a.z > b.z or (a.z == b.z and a.rang < b.rang))
	return items


## Monde (y vers le haut) → écran Godot (y vers le bas).
## origin = position écran du point (0, 0) du monde ; scale = pixels par unité.
static func to_screen(v: Vector2, origin: Vector2, scale: float) -> Vector2:
	return origin + Vector2(v.x, -v.y) * scale


## Profondeur (pose.z, négatif = vers la caméra) : vue en perspective, le
## personnage grossit et descend sur le sol quand il s'approche de la caméra,
## rapetisse et remonte quand il s'en éloigne. Le dessin est mis à l'échelle
## k autour du point du sol sous le bassin (pivot), puis décalé de lift.
const DEPTH_FOCALE := 300.0
const DEPTH_SOL := 0.3

static func depth(p: Dictionary) -> Dictionary:
	var z := float(p.get("z", 0.0))
	return {"k": DEPTH_FOCALE / (DEPTH_FOCALE + z), "lift": z * DEPTH_SOL, "pivot": Vector2(float(p.x), 0.0)}


## Point du monde → point dessiné, profondeur comprise.
static func depth_point(p: Dictionary, v: Vector2) -> Vector2:
	var dz := depth(p)
	return dz.pivot + (v - dz.pivot) * float(dz.k) + Vector2(0.0, dz.lift)


## Dessine une pose sur n'importe quel CanvasItem (à appeler depuis _draw).
## Traits à bouts et jointures ronds : segments + disques aux articulations.
## grow : élargit tous les traits (liseré dessiné sous la silhouette).
static func draw_pose(ci: CanvasItem, p: Dictionary, origin: Vector2, scale: float, color := Color("#111111"), far_shade := 1.0, grow := 0.0) -> void:
	var dz := depth(p)
	var k: float = dz.k
	var o: Vector2 = origin + to_screen(dz.pivot, Vector2.ZERO, scale) * (1.0 - k) + Vector2(0.0, -dz.lift * scale)
	scale *= k
	for pr in primitives(p, color, far_shade):
		if pr.type == "path":
			var w: float = (pr.width + grow) * scale
			var pts := PackedVector2Array()
			for v in pr.points:
				pts.append(to_screen(v, o, scale))
			for i in range(pts.size() - 1):
				ci.draw_line(pts[i], pts[i + 1], pr.color, w, true)
			for v in pts:
				ci.draw_circle(v, w / 2.0, pr.color)
		else:
			ci.draw_circle(to_screen(pr.c, o, scale), (pr.r + grow / 2.0) * scale, pr.color)


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
