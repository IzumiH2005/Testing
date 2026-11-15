extends SceneTree
## Génère anims/esquive_cote.json : esquive d'un coup appuyé (pied poussé)
## par un pivot sur le pied avant qui met la poitrine face à la caméra.
##
##   $GODOT --headless --path . -s res://tools/gen_esquive_cote.gd
##
## Comme le demi-tour, c'est un mouvement en profondeur : la garde ouverte est
## remontée en 3D (z négatif = vers la caméra), tournée image par image autour
## de l'axe vertical, projetée, puis relue en angles 2D (os raccourcis étirés).
##
## Ce qui se passe :
##   - le pied avant reste planté et tourne sur la plante (talon qui se lève
##     un peu au passage) ; tout le reste tourne autour de ce point d'un quart
##     de tour, poitrine vers la caméra (« face écran ») ;
##   - la jambe arrière balaie un arc derrière lui (loin de la caméra), pied
##     soulevé au milieu de l'arc, un peu en retard sur le bassin ;
##   - le bassin s'abaisse et se retrouve en retrait, hors de la ligne du coup :
##     le pied adverse passe devant son ventre ;
##   - le haut du corps devance le bassin et s'incline un peu loin du coup ;
##   - les bras lâchent la garde : mains basses, écartées pour l'équilibre,
##     puis retour en garde ouverte par le même pivot à l'envers.
##
## La perspective est calculée articulation par articulation (même focale et
## même remontée au sol que StickRig.depth). La clé porte une petite
## profondeur z pour que le combat le dessine derrière l'attaquant ; les
## points sont pré-compensés pour que cette profondeur ne déforme pas le dessin.

const BASE := "garde_ouverte"
const OUT := "res://anims/esquive_cote.json"
const N := 34           # dernière image
const CONTACT := 12     # le pied adverse passe devant le ventre
const Z_HIP := 9.0      # demi-largeur du bassin
const LEAD_UP := 1.5    # avance du haut du corps sur le bassin (images)
const LEAD_HEAD := 1.0  # avance de la tête sur le buste
const LAG_REAR := 1.5   # retard de la jambe arrière
const LIFT_REAR := 9.0  # hauteur du pied arrière au milieu de l'arc
const STEP_SIDE := 34.0 # face caméra, le pied arrière se pose de côté...
const STEP_IN := 0.5    # ... et moins loin derrière (fraction de l'arc gardée)
const Z_TRI := 0.3      # profondeur de tri portée par la clé (fraction du bassin)

var g: Dictionary       # pose de base
var s: Dictionary       # style
var J0: Dictionary      # articulations de la garde
var C: Vector3          # axe du pivot : plante du pied avant
var shift: Vector3      # recentrage du bassin entre les appuis, face caméra


func _initialize() -> void:
	g = StickRig.load_pose("res://poses/%s.json" % BASE)
	s = StickRig.get_style(g.style)
	J0 = StickRig.solve(g).joints
	C = Vector3(float(J0.toeN.x), 0.0, -Z_HIP)
	# Face caméra, le bassin se place au-dessus du milieu des deux appuis.
	var an_end := _front_ankle(-90.0, _pitch(J0, "N"))
	var af_end := _rear_ankle(-90.0)
	var h_end := around(_v3(J0.hip, 0.0), -90.0)
	shift = (an_end + af_end) / 2.0 - h_end
	shift.y = 0.0
	var cles := []
	for i in N + 1:
		cles.append(_key(i))
	var data := {
		"nom": "esquive_cote",
		"boucle": false,
		"base": BASE,
		"suivante": "garde_ouverte_idle",
		"pieds_auto": false,
		"genere_par": "tools/gen_esquive_cote.gd",
		"evenements": [
			{"f": CONTACT, "type": "contact"},
			{"f": 3, "type": "fenetre", "nom": "esquive", "n": 15},
			{"f": 21, "type": "fenetre", "nom": "contre", "n": 10},
		],
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


## Rotation (degrés, négatif = poitrine vers la caméra) : petit armé, quart de
## tour, léger dépassement, tenue pendant le passage du coup, retour.
static func theta(t: float) -> float:
	return _interp([[0.0, 0.0], [2.0, 4.0], [9.0, -86.0], [12.0, -92.0], [18.0, -88.0], [28.0, -4.0], [32.0, 0.0]], t)


## Hauteur du bassin : il s'abaisse en tournant, reste bas, remonte.
static func hip_dy(t: float) -> float:
	return _interp([[0.0, 0.0], [2.0, -2.5], [8.0, -10.0], [13.0, -9.0], [19.0, -9.0], [27.0, -2.0], [32.0, 0.0]], t)


## Inclinaison latérale du buste, loin du coup (degrés).
static func lean(t: float) -> float:
	return _interp([[0.0, 0.0], [3.0, 0.0], [10.0, 9.0], [18.0, 8.0], [27.0, 0.0]], t)


## Bras : 0 = garde ouverte, 1 = bras relâchés écartés.
static func arms(t: float) -> float:
	return _interp([[0.0, 0.0], [2.0, 0.15], [8.0, 1.0], [19.0, 1.0], [29.0, 0.1], [33.0, 0.0]], t)


## Talon avant levé pendant que le pied tourne sur la plante (degrés).
static func heel(t: float) -> float:
	return _interp([[0.0, 0.0], [5.0, -14.0], [10.0, -4.0], [19.0, -4.0], [24.0, -12.0], [30.0, 0.0]], t)


# ---------- 3D ----------

static func rot(v: Vector3, th: float) -> Vector3:
	var c := cos(deg_to_rad(th))
	var sn := sin(deg_to_rad(th))
	return Vector3(v.x * c - v.z * sn, v.y, v.x * sn + v.z * c)


## Rotation autour de l'axe vertical qui passe par la plante du pied avant.
func around(v: Vector3, th: float) -> Vector3:
	return C + rot(v - C, th)


## Inclinaison latérale (autour de l'axe avant du buste) : le haut part en -z.
static func tilt(v: Vector3, deg: float) -> Vector3:
	var c := cos(deg_to_rad(deg))
	var sn := sin(deg_to_rad(deg))
	return Vector3(v.x, v.y * c + v.z * sn, v.z * c - v.y * sn)


## Articulation intermédiaire par cinématique inverse à deux os en 3D.
static func knee(S: Vector3, A: Vector3, l1: float, l2: float, pole: Vector3) -> Vector3:
	var d := A - S
	var L := clampf(d.length(), absf(l1 - l2) + 0.001, l1 + l2 - 0.001)
	var u := d.normalized()
	var a := (l1 * l1 - l2 * l2 + L * L) / (2.0 * L)
	var h := sqrt(maxf(l1 * l1 - a * a, 0.0))
	var w := (pole - u * pole.dot(u)).normalized()
	return S + u * a + w * h


static func _v3(v: Vector2, z: float) -> Vector3:
	return Vector3(v.x, v.y, z)


## Tangage du pied dans la garde (degrés, négatif = talon levé).
static func _pitch(J: Dictionary, side: String) -> float:
	var d: Vector2 = J["toe" + side] - J["ankle" + side]
	return rad_to_deg(atan2(d.y, d.x))


## Cheville avant : la plante reste posée, le pied tourne autour d'elle.
func _front_ankle(th: float, phi: float) -> Vector3:
	var L: float = s.foot
	var toe := Vector3(float(J0.toeN.x), float(J0.toeN.y), -Z_HIP)
	var fw := rot(Vector3(L * cos(deg_to_rad(phi)), 0.0, 0.0), th)
	return toe - Vector3(fw.x, L * sin(deg_to_rad(phi)), fw.z)


## Cheville arrière (au sol) : arc autour du pivot qui se resserre et
## s'écarte sur le côté, pour finir en appuis de face (largeur d'épaules).
func _rear_ankle(th: float) -> Vector3:
	var p := _smooth(absf(th) / 90.0)
	var r := rot(Vector3(float(J0.ankleF.x), 0.0, Z_HIP) - Vector3(C.x, 0.0, C.z), th)
	r *= lerpf(1.0, STEP_IN, p)
	return Vector3(C.x, float(J0.ankleF.y), C.z) + r + Vector3(STEP_SIDE * p, 0.0, 0.0)


# ---------- Une image ----------

func _key(i: int) -> Dictionary:
	var t := float(i)
	var th := theta(t)
	var lead := _smooth(t / 3.0)
	var th_up := theta(t + LEAD_UP * lead)
	var th_head := theta(t + (LEAD_UP + LEAD_HEAD) * lead)
	var th_rear := theta(t - LAG_REAR)
	var ln := lean(t)
	var m := arms(t)

	var hip0: Vector2 = J0.hip
	var H := around(_v3(hip0, 0.0), th) + shift * _smooth(absf(th) / 90.0) + Vector3(0.0, hip_dy(t), 0.0)

	# Haut du corps dans le repère du buste (bassin à l'origine, +x = avant,
	# -z = côté proche).
	var body := StickRig.clone_pose(g)
	body.x = 0.0
	body.y = 0.0
	var B: Dictionary = StickRig.solve(body).joints
	var P := {}
	P.hip = H
	P.waist = H + rot(tilt(_v3(B.waist, 0.0), ln * 0.5), (th + th_up) / 2.0)
	var sh := tilt(_v3(B.shoulder, 0.0), ln)
	P.shoulder = H + rot(sh, th_up)
	P.head = H + rot(tilt(_v3(B.head, 0.0), ln * 1.2), th_head)

	# Bras : de la garde (dans le plan du buste) aux mains basses écartées.
	var relax := {"N": Vector3(4.0, 8.0, -30.0), "F": Vector3(-4.0, 13.0, 30.0)}
	var pole_r := {"N": Vector3(-1.0, -0.2, -0.7), "F": Vector3(-1.0, -0.2, 0.7)}
	for side in ["N", "F"]:
		var hand_g := _v3(B["hand" + side], 0.0)
		var elbow_g := _v3(B["elbow" + side], 0.0)
		var target: Vector3 = hand_g.lerp(relax[side], m)
		var pole: Vector3 = (elbow_g - _v3(B.shoulder, 0.0)).normalized().lerp(pole_r[side].normalized(), m)
		var sh0 := _v3(B.shoulder, 0.0)
		var el := knee(sh0, target, s.upperArm, s.forearm, pole)
		var dir := (target - sh0)
		var hd := sh0 + dir.normalized() * minf(dir.length(), s.upperArm + s.forearm - 0.01)
		# Le bras suit l'inclinaison du buste.
		P["elbow" + side] = H + rot(tilt(el, ln), th_up)
		P["hand" + side] = H + rot(tilt(hd, ln), th_up)

	# Jambes.
	var L: float = s.foot
	var pole_k := rot(Vector3(1, 0, 0), th)
	# Pied avant : la plante reste au sol, le pied tourne avec le bassin.
	var phiN := _pitch(J0, "N") + heel(t)
	var toeN := Vector3(float(J0.toeN.x), float(J0.toeN.y), -Z_HIP)
	var AN := _front_ankle(th, phiN)
	# Pied arrière : arc derrière lui, soulevé au milieu.
	var phiF := _pitch(J0, "F")
	var lift := LIFT_REAR * sin(PI * clampf(absf(th_rear) / 90.0, 0.0, 1.0))
	var AF := _rear_ankle(th_rear) + Vector3(0.0, lift, 0.0)
	var fwF := rot(Vector3(L * cos(deg_to_rad(phiF)), 0.0, 0.0), th_rear)
	var toeF := AF + Vector3(fwF.x, L * sin(deg_to_rad(phiF)), fwF.z)
	for pr in [["N", AN, toeN, -1.0], ["F", AF, toeF, 1.0]]:
		var side: String = pr[0]
		var A: Vector3 = pr[1]
		var S := H + rot(Vector3(0, 0, float(pr[3]) * Z_HIP), th)
		P["ankle" + side] = A
		P["toe" + side] = pr[2]
		P["knee" + side] = knee(S, A, s.thigh, s.shin, pole_k)

	return _fit(i, _project(P, H, _smooth(absf(th) / 90.0)))


# ---------- Perspective par articulation ----------

func _project(P: Dictionary, H: Vector3, amount: float) -> Dictionary:
	## Chaque point reçoit la perspective de sa propre profondeur, autour du
	## sol sous le bassin (dosée par amount : nulle en garde, pleine face
	## caméra) ; puis on retire la transformation que le combat appliquera à
	## toute la figure pour la profondeur de tri de la clé.
	var px := H.x
	var zk := StickRig.round2(maxf(H.z, 0.0) * Z_TRI)
	var fig := StickRig.depth({"x": px, "z": zk})
	var out := {"_z": zk}
	for k in P:
		var v: Vector3 = P[k]
		var d := StickRig.depth({"x": px, "z": v.z * amount})
		var w := Vector2(px, 0.0) + (Vector2(v.x, v.y) - Vector2(px, 0.0)) * float(d.k) + Vector2(0.0, d.lift)
		out[k] = fig.pivot + (w - Vector2(0.0, fig.lift) - fig.pivot) / float(fig.k)
	return out


# ---------- Projection → angles 2D ----------

func _fit(i: int, P: Dictionary) -> Dictionary:
	var hip: Vector2 = P.hip
	var ang := {}
	var et := {}
	var root := StickRig.angle(g, "root")
	ang.root = root
	var w := {"root": 90.0 - root}
	var bone := func(id: String, parent: String, a: Vector2, b: Vector2, len_key: String, min_et: float) -> void:
		var bd: Dictionary = StickRig.bone(id)
		var d := b - a
		var wa: float = rad_to_deg(atan2(d.y, d.x)) if d.length() > 0.001 else float(w[parent]) + float(bd.rest)
		w[id] = wa
		ang[id] = StickRig.round2(float(bd.sign) * StickRig.norm180(wa - float(w[parent]) - float(bd.rest)))
		if len_key != "":
			var e := maxf(d.length() / float(s[len_key]), min_et)
			if absf(e - 1.0) > 0.005:
				et[id] = StickRig.round2(e)
	bone.call("spineLow", "root", hip, P.waist, "spineLow", 0.0)
	bone.call("chest", "spineLow", P.waist, P.shoulder, "chest", 0.0)
	bone.call("neck", "chest", P.shoulder, P.head, "", 0.0)
	for side in ["N", "F"]:
		bone.call("arm" + side, "chest", P.shoulder, P["elbow" + side], "upperArm", 0.0)
		bone.call("fore" + side, "arm" + side, P["elbow" + side], P["hand" + side], "forearm", 0.0)
		bone.call("thigh" + side, "root", hip, P["knee" + side], "thigh", 0.0)
		bone.call("shin" + side, "thigh" + side, P["knee" + side], P["ankle" + side], "shin", 0.0)
		bone.call("foot" + side, "shin" + side, P["ankle" + side], P["toe" + side], "foot", 0.2)
	var fixe := {"x": StickRig.round2(hip.x), "y": StickRig.round2(hip.y)}
	if absf(float(P._z)) > 0.0:
		fixe.z = P._z
	for k in StickRig.angle_ids():
		fixe[k] = ang[k]
	var key := {"f": i, "facing": 1, "courbe": "lin", "ancre": false, "fixe": fixe}
	if not et.is_empty():
		key.etire = et
	return key


# ---------- JSON compact (une clé par ligne) ----------

static func _dump(data: Dictionary) -> String:
	var lines := ["{"]
	for k in ["nom", "boucle", "base", "suivante", "pieds_auto", "genere_par", "evenements"]:
		lines.append('  "%s": %s,' % [k, JSON.stringify(data[k])])
	lines.append('  "cles": [')
	var n: int = data.cles.size()
	for j in n:
		lines.append("    " + JSON.stringify(data.cles[j], "", false) + ("," if j < n - 1 else ""))
	lines.append("  ]")
	lines.append("}")
	return "\n".join(lines) + "\n"
