extends SceneTree
## Génère anims/demi_tour.json : pivot sur place, de la garde ouverte à la
## même garde tournée de l'autre côté.
##
##   $GODOT --headless --path . -s res://tools/gen_demi_tour.gd
##
## Le demi-tour est un mouvement en profondeur : la 2D seule ne sait pas où
## passent les bras et les genoux quand la poitrine fait face à la caméra.
## On remonte donc la garde en 3D (chaque articulation reçoit une profondeur
## z, côté proche vers la caméra), on la fait tourner autour de l'axe
## vertical image par image, puis on projette et on relit la projection en
## angles 2D (avec étirement des os raccourcis). Une clé par image.
##
## Ce qui se passe :
##   - les chevilles ne bougent pas en x : le combattant pivote sur ses
##     appuis ; le talon de l'ancienne jambe arrière se pose, celui de
##     l'ancienne jambe avant se lève (elle devient la jambe arrière) ;
##   - les genoux sont recalculés en 3D (ils plient vers l'avant du bassin) ;
##   - le bassin glisse vers le milieu des appuis puis au-delà, là où la
##     garde retournée le place, en s'abaissant à l'anticipation et en se
##     soulevant au passage ;
##   - le haut du corps devance le bassin, la tête encore un peu plus ;
##   - les bras échangent leurs rôles (la main avant devient la main
##     arrière) et se rentrent vers le tronc au milieu du tour ;
##   - le sens affiché bascule quand la poitrine fait face à la caméra.

const BASE := "garde_ouverte"
const OUT := "res://anims/demi_tour.json"
const N := 22           # dernière image
const Z_HIP := 9.0      # demi-largeur du bassin
const Z_ELBOW := 12.0
const Z_HAND := 7.0
const LEAD_UP := 1.5    # avance du haut du corps sur le bassin (images)
const LEAD_HEAD := 1.0  # avance de la tête sur le buste
const TUCK_ARM := -8.0  # bras rentrés au milieu du tour
const TUCK_FORE := 16.0

var g: Dictionary       # pose de base
var s: Dictionary       # style


func _initialize() -> void:
	g = StickRig.load_pose("res://poses/%s.json" % BASE)
	s = StickRig.get_style(g.style)
	var cles := []
	for i in N + 1:
		cles.append(_key(i))
	var data := {
		"nom": "demi_tour",
		"boucle": false,
		"base": BASE,
		"suivante": "garde_ouverte_idle",
		"pieds_auto": false,
		"genere_par": "tools/gen_demi_tour.gd",
		"cles": cles,
	}
	var f := FileAccess.open(OUT, FileAccess.WRITE)
	f.store_string(_dump(data))
	f.close()
	print("écrit ", OUT, " (", cles.size(), " clés)")
	quit()


# ---------- Courbes ----------

static func _smooth(u: float) -> float:
	u = clampf(u, 0.0, 1.0)
	return u * u * (3.0 - 2.0 * u)


static func _interp(keys: Array, t: float) -> float:
	## keys = [[t, v], ...], lissage smoothstep entre deux points.
	if t <= keys[0][0]:
		return keys[0][1]
	for k in keys.size() - 1:
		var a: Array = keys[k]
		var b: Array = keys[k + 1]
		if t <= b[0]:
			return lerpf(a[1], b[1], _smooth((t - a[0]) / (b[0] - a[0])))
	return keys[-1][1]


## Rotation du bassin (degrés) : anticipation, tour, dépassement, retour.
static func theta(t: float) -> float:
	return _interp([[0.0, 0.0], [3.0, -8.0], [12.0, 190.0], [17.0, 179.0], [21.0, 180.0]], t)


## Hauteur du bassin : flexion d'élan, passage resté bas, amorti, retour.
static func hip_dy(t: float) -> float:
	return _interp([[0.0, 0.0], [3.0, -2.5], [8.0, -1.0], [14.0, -2.5], [19.0, 0.3], [22.0, 0.0]], t)


static func progress(th: float) -> float:
	return clampf(th / 180.0, 0.0, 1.0)


# ---------- 3D ----------

static func rot(v: Vector3, th: float) -> Vector3:
	var c := cos(deg_to_rad(th))
	var sn := sin(deg_to_rad(th))
	return Vector3(v.x * c - v.z * sn, v.y, v.x * sn + v.z * c)


## Genou par cinématique inverse à deux os en 3D, plié vers pole.
static func knee(S: Vector3, A: Vector3, l1: float, l2: float, pole: Vector3) -> Vector3:
	var d := A - S
	var L := clampf(d.length(), absf(l1 - l2) + 0.001, l1 + l2 - 0.001)
	var u := d.normalized()
	var a := (l1 * l1 - l2 * l2 + L * L) / (2.0 * L)
	var h := sqrt(maxf(l1 * l1 - a * a, 0.0))
	var w := (pole - u * pole.dot(u)).normalized()
	return S + u * a + w * h


# ---------- Une image ----------

func _key(i: int) -> Dictionary:
	var t := float(i)
	var th_hip := theta(t)
	# L'avance du haut du corps s'installe pendant l'anticipation (la première
	# image reste exactement la garde).
	var lead := _smooth(t / 3.0)
	var th_up := theta(t + LEAD_UP * lead)
	var th_head := theta(t + (LEAD_UP + LEAD_HEAD) * lead)
	var m := _smooth(progress(th_up))
	var sens := 1 if th_up < 90.0 else -1

	var J0: Dictionary = StickRig.solve(g).joints
	var hip0: Vector2 = J0.hip
	# Garde retournée : l'ancienne cheville avant devient l'arrière, d'où le
	# bassin d'arrivée.
	var dx_end := float(J0.ankleN.x) + float(J0.ankleF.x) - 2.0 * hip0.x
	var hx := dx_end * (1.0 - cos(deg_to_rad(th_hip))) / 2.0
	var H := Vector3(hip0.x + hx, hip0.y + hip_dy(t), 0.0)

	# Haut du corps dans le repère du buste (garde de face, +x = avant), bras
	# qui échangent leurs rôles et se rentrent au milieu du tour.
	var body := StickRig.clone_pose(g)
	body.x = 0.0
	body.y = 0.0
	var tuck := sin(PI * m)
	for pr in [["N", "F"], ["F", "N"]]:
		var me: String = pr[0]
		var other: String = pr[1]
		body.angles["arm" + me] = lerpf(StickRig.angle(g, "arm" + me), StickRig.angle(g, "arm" + other), m) + TUCK_ARM * tuck
		body.angles["fore" + me] = lerpf(StickRig.angle(g, "fore" + me), StickRig.angle(g, "fore" + other), m) + TUCK_FORE * tuck
	var B: Dictionary = StickRig.solve(body).joints
	var P := {}   # articulations 3D, côté « physique » (celui de la garde de départ)
	P.hip = H
	P.waist = H + rot(_v3(B.waist, 0.0), (th_hip + th_up) / 2.0)
	P.shoulder = H + rot(_v3(B.shoulder, 0.0), th_up)
	P.head = H + rot(_v3(B.head, 0.0), th_head)
	for side in ["N", "F"]:
		var zs := 1.0 if side == "N" else -1.0
		P["elbow" + side] = H + rot(_v3(B["elbow" + side], zs * Z_ELBOW), th_up)
		P["hand" + side] = H + rot(_v3(B["hand" + side], zs * Z_HAND), th_up)

	# Jambes : chevilles fixes en x, talons qui changent de rôle.
	var pole := rot(Vector3(1, 0, 0), th_hip)
	var mh := _smooth(progress(th_hip))
	var L: float = s.foot
	for side in ["N", "F"]:
		var other := "F" if side == "N" else "N"
		var zs := 1.0 if side == "N" else -1.0
		# Pied : tangage de la garde de départ vers celui du rôle d'arrivée.
		var phi0 := _pitch(J0, side)
		var phi1 := _pitch(J0, other)
		var phi := lerpf(phi0, phi1, mh)
		var toe_y := lerpf(float(J0["toe" + side].y), float(J0["toe" + other].y), mh)
		var ank_y := toe_y - L * sin(deg_to_rad(phi))
		var A := Vector3(float(J0["ankle" + side].x), ank_y, zs * Z_HIP * cos(deg_to_rad(th_hip)))
		var S := H + rot(Vector3(0, 0, zs * Z_HIP), th_hip)
		P["ankle" + side] = A
		P["knee" + side] = knee(S, A, s.thigh, s.shin, pole)
		var fw := rot(Vector3(cos(deg_to_rad(phi)), 0, 0), th_hip) * L
		P["toe" + side] = A + Vector3(fw.x, L * sin(deg_to_rad(phi)), fw.z)

	return _fit(i, P, sens)


static func _v3(v: Vector2, z: float) -> Vector3:
	return Vector3(v.x, v.y, z)


## Tangage du pied dans la garde (degrés, négatif = talon levé).
static func _pitch(J: Dictionary, side: String) -> float:
	var d: Vector2 = J["toe" + side] - J["ankle" + side]
	return rad_to_deg(atan2(d.y, d.x))


# ---------- Projection → angles 2D ----------

func _fit(i: int, P: Dictionary, f: int) -> Dictionary:
	# Étiquettes 2D : en sens -1, le côté proche est l'ancien côté loin.
	var lab := {"N": "N", "F": "F"} if f > 0 else {"N": "F", "F": "N"}
	var hip := Vector2(P.hip.x, P.hip.y)
	var ang := {}
	var et := {}
	var root := StickRig.angle(g, "root")
	ang.root = root
	var w := {"root": 90.0 - root}
	var pt := func(k: String) -> Vector2: return Vector2(P[k].x, P[k].y)
	var bone := func(id: String, parent: String, a: Vector2, b: Vector2, len_key: String, min_et: float) -> void:
		var bd: Dictionary = StickRig.bone(id)
		var d := b - a
		var wa: float = rad_to_deg(atan2(d.y, f * d.x)) if d.length() > 0.001 else float(w[parent]) + float(bd.rest)
		w[id] = wa
		ang[id] = StickRig.round2(float(bd.sign) * StickRig.norm180(wa - float(w[parent]) - float(bd.rest)))
		if len_key != "":
			var e := maxf(d.length() / float(s[len_key]), min_et)
			if absf(e - 1.0) > 0.005:
				et[id] = StickRig.round2(e)
	bone.call("spineLow", "root", hip, pt.call("waist"), "spineLow", 0.0)
	bone.call("chest", "spineLow", pt.call("waist"), pt.call("shoulder"), "chest", 0.0)
	bone.call("neck", "chest", pt.call("shoulder"), pt.call("head"), "", 0.0)
	for side in ["N", "F"]:
		var ph: String = lab[side]   # côté physique dessiné en « side »
		bone.call("arm" + side, "chest", pt.call("shoulder"), pt.call("elbow" + ph), "upperArm", 0.0)
		bone.call("fore" + side, "arm" + side, pt.call("elbow" + ph), pt.call("hand" + ph), "forearm", 0.0)
		bone.call("thigh" + side, "root", hip, pt.call("knee" + ph), "thigh", 0.0)
		bone.call("shin" + side, "thigh" + side, pt.call("knee" + ph), pt.call("ankle" + ph), "shin", 0.0)
		bone.call("foot" + side, "shin" + side, pt.call("ankle" + ph), pt.call("toe" + ph), "foot", 0.2)
	var fixe := {"x": StickRig.round2(hip.x), "y": StickRig.round2(hip.y)}
	for k in StickRig.angle_ids():
		fixe[k] = ang[k]
	var key := {"f": i, "facing": f, "courbe": "lin", "ancre": false, "fixe": fixe}
	if not et.is_empty():
		key.etire = et
	return key


# ---------- JSON compact (une clé par ligne) ----------

static func _dump(data: Dictionary) -> String:
	var lines := ["{"]
	for k in ["nom", "boucle", "base", "suivante", "pieds_auto", "genere_par"]:
		lines.append('  "%s": %s,' % [k, JSON.stringify(data[k])])
	lines.append('  "cles": [')
	var n: int = data.cles.size()
	for j in n:
		lines.append("    " + JSON.stringify(data.cles[j], "", false) + ("," if j < n - 1 else ""))
	lines.append("  ]")
	lines.append("}")
	return "\n".join(lines) + "\n"
