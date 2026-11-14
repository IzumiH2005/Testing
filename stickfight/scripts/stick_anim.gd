class_name StickAnim
extends RefCounted
## Animation par poses clés, à 60 images par seconde.
##
## Une animation (anims/<nom>.json) est une liste de clés posées sur des
## numéros d'image. Entre deux clés, chaque canal (angles, x, y, étirements)
## suit une courbe. Après l'interpolation, deux corrections :
##   - un pied qui a la même position dans deux clés successives reste
##     planté (cinématique inverse de la jambe), donc il ne glisse jamais ;
##   - un pied ne descend jamais sous le sol.
## Le « décalage » retarde certains canaux de quelques images : la tête ou
## les avant-bras suivent le mouvement avec un temps de retard
## (chevauchement, follow-through).
##
## Format :
## {
##   "nom": "blocage_bas", "boucle": false, "longueur": 40,
##   "base": "garde",                      pose de départ des clés (poses/garde.json)
##   "suivante": "garde_idle",             animation enchaînée à la fin
##   "decalage": {"neck": 2, "foreN": 1},  retard en images par canal
##   "cles": [
##     {"f": 0},                           la pose de base telle quelle
##     {"f": 4, "plus": {"chest": -3, "y": 1}, "courbe": "dec"},
##     {"f": 8, "pose": "blocage_contact", "vise": {"armN": [46, 90]}},
##     {"f": 12, "pose": "=", "vise_rel": {"armN": [0, -6]}}
##   ],
##   "evenements": [{"f": 8, "type": "hitstop", "n": 8}],
##   "trainees": [{"articulation": "handN", "coude": "elbowN", "de": 5, "a": 8}]
## }
##
## Une clé part de « pose » (nom de fichier dans poses/, « = » pour la clé
## précédente, absente = la base), puis applique dans l'ordre :
##   fixe     {canal: valeur}       valeur absolue (angles, x, y)
##   plus     {canal: delta}        valeur relative
##   etire    {os: facteur}         longueur de l'os × facteur
##   vise     {membre: [x, y]}      cinématique inverse vers un point (repère local)
##   vise_rel {membre: [dx, dy]}   idem, relatif à la position actuelle du bout
##   ancre    true / false / "N" / "F"  par défaut true : si le bassin bouge,
##            les jambes se replient pour garder les chevilles de la pose
##            de départ (sauf jambe touchée par fixe, plus ou vise).
## courbe : forme du segment qui part de cette clé.
##   auto     spline passant par les clés voisines (arcs fluides) ; une clé
##            qui est un extrême (aller-retour) a une tangente nulle
##   lin      vitesse constante
##   acc      départ lent, accélère (ease in) ; p = puissance (2 par défaut)
##   dec      départ vif, finit lentement (ease out)
##   acc-dec  lent aux deux bouts (slow in / slow out)
##   palier   garde la pose jusqu'à la clé suivante (hold)
## pas : n > 1 tient chaque image n images (animation « en deux », style pixel).
##
## Repère local : le personnage regarde vers +x, bassin de la base en x = 0.

const DIR := "res://anims/"
const POSE_DIR := "res://poses/"
const PLANT_EPS := 0.35
const LEG_CHANNELS := {"thighN": "N", "shinN": "N", "footN": "N", "thighF": "F", "shinF": "F", "footF": "F"}

static var _cache := {}


static func load_named(nom: String) -> Dictionary:
	if not _cache.has(nom):
		_cache[nom] = load_anim(DIR + nom + ".json")
	return _cache[nom]


static func clear_cache() -> void:
	_cache.clear()


static func load_anim(path: String) -> Dictionary:
	var data = JSON.parse_string(FileAccess.get_file_as_string(path))
	if not (data is Dictionary) or not data.has("cles"):
		push_error("Animation illisible : " + path)
		return {}
	return build(data)


static func _pose_file(nom: String) -> Dictionary:
	var path := nom if nom.ends_with(".json") else POSE_DIR + nom + ".json"
	return StickRig.load_pose(path)


## Transforme la description JSON en animation prête à échantillonner.
static func build(data: Dictionary) -> Dictionary:
	var a := {
		"nom": str(data.get("nom", "sans nom")),
		"boucle": bool(data.get("boucle", false)),
		"suivante": str(data.get("suivante", "")),
		"decalage": {},
		"evenements": data.get("evenements", []),
		"trainees": data.get("trainees", []),
		"cles": [],
		"etire_ids": [],
	}
	for k in data.get("decalage", {}):
		a.decalage[k] = float(data.decalage[k])
	var base_name := str(data.get("base", ""))
	var base := _pose_file(base_name) if base_name != "" else StickRig.neutral_pose()
	var prev := base
	var raw: Array = data.cles.duplicate()
	raw.sort_custom(func(x, y): return int(x.f) < int(y.f))
	for kd in raw:
		var pose := _resolve(kd, base, prev)
		prev = pose
		var J: Dictionary = StickRig.solve(pose).joints
		a.cles.append({
			"f": int(kd.f), "pose": pose,
			"courbe": str(kd.get("courbe", "auto")), "p": float(kd.get("p", 2.0)), "pas": maxi(1, int(kd.get("pas", 1))),
			"plate": bool(kd.get("plate", false)),
			"chevilles": {"N": J.ankleN, "F": J.ankleF},
		})
		for e in pose.get("etire", {}):
			if not e in a.etire_ids:
				a.etire_ids.append(e)
	var last: int = a.cles[-1].f
	a.longueur = int(data.get("longueur", last))
	var max_lag := 0.0
	for k in a.decalage:
		max_lag = maxf(max_lag, a.decalage[k])
	a.duree = float(a.longueur) if a.boucle else float(last) + max_lag
	return a


static func _side_of(channel: String) -> String:
	return LEG_CHANNELS.get(channel, "")


static func _apply_channel(p: Dictionary, k: String, v: float, rel: bool) -> void:
	if k in ["x", "y"]:
		p[k] = float(p[k]) + v if rel else v
	else:
		p.angles[k] = StickRig.angle(p, k) + v if rel else v


static func _vec(v) -> Vector2:
	return Vector2(float(v[0]), float(v[1]))


static func _resolve(kd: Dictionary, base: Dictionary, prev: Dictionary) -> Dictionary:
	var src := str(kd.get("pose", ""))
	var p: Dictionary
	if src == "":
		p = StickRig.clone_pose(base)
	elif src == "=":
		p = StickRig.clone_pose(prev)
	else:
		p = _pose_file(src)
	var J0: Dictionary = StickRig.solve(p).joints
	var touched := {"N": false, "F": false}
	for k in kd.get("fixe", {}):
		_apply_channel(p, k, float(kd.fixe[k]), false)
		if _side_of(k) != "":
			touched[_side_of(k)] = true
	for k in kd.get("plus", {}):
		_apply_channel(p, k, float(kd.plus[k]), true)
		if _side_of(k) != "":
			touched[_side_of(k)] = true
	if kd.has("etire"):
		var e: Dictionary = p.get("etire", {}).duplicate()
		for k in kd.etire:
			e[k] = float(kd.etire[k])
		p.etire = e
	elif src == "":
		p.erase("etire")
	var vise: Dictionary = kd.get("vise", {})
	var vise_rel: Dictionary = kd.get("vise_rel", {})
	var ancre = kd.get("ancre", true)
	for side in ["N", "F"]:
		var limb: String = "leg" + side
		if vise.has(limb):
			p = StickRig.reach(p, limb, _vec(vise[limb]))
		elif vise_rel.has(limb):
			p = StickRig.reach(p, limb, J0["ankle" + side] + _vec(vise_rel[limb]))
		elif not touched[side] and (ancre is bool and ancre or str(ancre) == side):
			p = StickRig.reach(p, limb, J0["ankle" + side])
	var J1: Dictionary = StickRig.solve(p).joints
	for side in ["N", "F"]:
		var limb: String = "arm" + side
		if vise.has(limb):
			p = StickRig.reach(p, limb, _vec(vise[limb]))
		elif vise_rel.has(limb):
			p = StickRig.reach(p, limb, J1["hand" + side] + _vec(vise_rel[limb]))
	p.nom = str(kd.get("nom", "f%d" % int(kd.f)))
	return p


# ---------- Échantillonnage ----------

static func _value(key: Dictionary, c: String) -> float:
	var p: Dictionary = key.pose
	if c == "x" or c == "y":
		return float(p[c])
	if c.begins_with("etire:"):
		return float(p.get("etire", {}).get(c.substr(6), 1.0))
	return StickRig.angle(p, c)


## Clé i (avec bouclage) et son temps, éventuellement décalé d'une longueur.
static func _key_time(a: Dictionary, i: int) -> float:
	var n: int = a.cles.size()
	var wraps := floori(float(i) / n)
	return float(a.cles[posmod(i, n)].f) + wraps * float(a.longueur)


static func _key(a: Dictionary, i: int) -> Dictionary:
	return a.cles[posmod(i, a.cles.size())]


## Tangente (unités par image) à la clé i, pour la courbe « auto ».
static func _tangent(a: Dictionary, i: int, c: String) -> float:
	var n: int = a.cles.size()
	if not a.boucle and (i <= 0 or i >= n - 1):
		return 0.0
	var k := _key(a, i)
	if k.plate:
		return 0.0
	var t0 := _key_time(a, i - 1)
	var t1 := _key_time(a, i)
	var t2 := _key_time(a, i + 1)
	var v0 := _value(_key(a, i - 1), c)
	var v1 := _value(k, c)
	var v2 := _value(_key(a, i + 1), c)
	var s0 := (v1 - v0) / maxf(t1 - t0, 1e-6)
	var s1 := (v2 - v1) / maxf(t2 - t1, 1e-6)
	if s0 * s1 <= 0.0:
		return 0.0  # extrême ou palier : on y arrive et on en repart lentement
	var m := (s0 * (t2 - t1) + s1 * (t1 - t0)) / (t2 - t0)
	# Pas de dépassement entre les clés (spline monotone, Fritsch-Carlson).
	var lim := 3.0 * minf(absf(s0), absf(s1))
	return clampf(m, -lim, lim)


static func _ease(courbe: String, u: float, pw: float) -> float:
	match courbe:
		"lin":
			return u
		"acc":
			return pow(u, pw)
		"dec":
			return 1.0 - pow(1.0 - u, pw)
		"acc-dec":
			return 0.5 * pow(2.0 * u, pw) if u < 0.5 else 1.0 - 0.5 * pow(2.0 * (1.0 - u), pw)
		"palier":
			return 0.0
	return u


## Indice de la clé qui commence le segment contenant t (t déjà ramené dans
## l'animation), et u dans [0, 1].
static func _segment(a: Dictionary, t: float) -> Dictionary:
	var n: int = a.cles.size()
	var i := 0
	while i < n - 1 and float(a.cles[i + 1].f) <= t:
		i += 1
	var k: Dictionary = a.cles[i]
	var has_next: bool = i < n - 1 or a.boucle
	if not has_next:
		return {"i": i, "u": 0.0, "end": true}
	var t0 := float(k.f)
	var t1 := _key_time(a, i + 1)
	var tt := t
	if k.pas > 1:
		tt = t0 + floorf((t - t0) / k.pas) * k.pas
	return {"i": i, "u": clampf((tt - t0) / maxf(t1 - t0, 1e-6), 0.0, 1.0), "end": false}


static func _wrap(a: Dictionary, t: float) -> float:
	if a.boucle:
		return fposmod(t, float(a.longueur))
	return clampf(t, float(a.cles[0].f), float(a.cles[-1].f))


static func _channel(a: Dictionary, c: String, t: float) -> float:
	if a.cles.size() == 1:
		return _value(a.cles[0], c)
	var seg := _segment(a, _wrap(a, t))
	var k0: Dictionary = a.cles[seg.i]
	var v0 := _value(k0, c)
	if seg.end:
		return v0
	var v1 := _value(_key(a, seg.i + 1), c)
	var u: float = seg.u
	if k0.courbe != "auto":
		return lerpf(v0, v1, _ease(k0.courbe, u, k0.p))
	# Hermite cubique, tangentes en unités par image.
	var dt := _key_time(a, seg.i + 1) - float(k0.f)
	var m0 := _tangent(a, seg.i, c) * dt
	var m1 := _tangent(a, seg.i + 1, c) * dt
	var u2 := u * u
	var u3 := u2 * u
	return (2.0 * u3 - 3.0 * u2 + 1.0) * v0 + (u3 - 2.0 * u2 + u) * m0 + (-2.0 * u3 + 3.0 * u2) * v1 + (u3 - u2) * m1


## Pose locale à l'instant t (en images, réel).
static func sample(a: Dictionary, t: float) -> Dictionary:
	var p := StickRig.clone_pose(a.cles[0].pose)
	var lag: Dictionary = a.decalage
	for c in StickRig.angle_ids():
		p.angles[c] = _channel(a, c, t - lag.get(c, 0.0))
	p.x = _channel(a, "x", t - lag.get("x", 0.0))
	p.y = _channel(a, "y", t - lag.get("y", 0.0))
	if not a.etire_ids.is_empty():
		var e := {}
		for b in a.etire_ids:
			e[b] = _channel(a, "etire:" + b, t - lag.get(b, 0.0))
		p.etire = e
	else:
		p.erase("etire")
	# Pieds plantés : même cheville dans les deux clés du segment.
	var seg := _segment(a, _wrap(a, t))
	var k0: Dictionary = a.cles[seg.i]
	var k1 := k0 if seg.end else _key(a, seg.i + 1)
	var s: Dictionary = StickRig.get_style(p.style)
	var ground: float = s.stroke / 2.0
	for side in ["N", "F"]:
		var A: Vector2 = k0.chevilles[side]
		var B: Vector2 = k1.chevilles[side]
		if A.distance_to(B) < PLANT_EPS:
			p = StickRig.reach(p, "leg" + side, A)
		else:
			var ank: Vector2 = StickRig.solve(p).joints["ankle" + side]
			if ank.y < ground:
				p = StickRig.reach(p, "leg" + side, Vector2(ank.x, ground))
	p.nom = "%s @%s" % [a.nom, str(snappedf(t, 0.01))]
	return p


## Événements dont l'image est dans ]t0, t1] (avec bouclage).
static func events_between(a: Dictionary, t0: float, t1: float) -> Array:
	var out := []
	if t1 <= t0:
		return out
	for e in a.evenements:
		var f := float(e.f)
		if a.boucle:
			var L := float(a.longueur)
			var n0 := floorf((t0 - f) / L)
			if f + (n0 + 1.0) * L <= t1:
				out.append(e)
		elif f > t0 and f <= t1:
			out.append(e)
	# Cas particulier : un événement à l'image 0 au tout premier pas.
	if t0 < 0.0 and not a.boucle:
		for e in a.evenements:
			if float(e.f) == 0.0 and not e in out:
				out.append(e)
	return out


## Première image marquée d'un événement de ce type (-1 si aucun).
static func event_frame(a: Dictionary, type: String) -> float:
	for e in a.evenements:
		if e.type == type:
			return float(e.f)
	return -1.0


## Traînées actives à l'instant t : [{articulation, coude}].
static func trails_at(a: Dictionary, t: float) -> Array:
	var out := []
	for tr in a.trainees:
		if t >= float(tr.de) and t <= float(tr.a):
			out.append(tr)
	return out
