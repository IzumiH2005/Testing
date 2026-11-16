class_name Filtres
extends RefCounted
## Effets calculés (filtres) : rien n'est dessiné à la main, tout se déduit
## des poses du squelette aux images précédentes, ou d'un événement posé dans
## l'animation. Voir BIBLE_ANIMATION.md, § 10.
##
## Automatiques (à chaque image, pour chaque combattant) :
##   trainee     ruban derrière le poing ou le pied qui va vite (§ 10.1)
##   etirement   bras ou jambe allongés sur l'image où ils se détendent (§ 10.3)
##   fantomes    copies pâles du corps quand tout le corps va vite (§ 10.4)
##   poussiere   petits dômes laissés au sol par un pied qui glisse (§ 10.10)
## Une animation peut les régler ou les couper :
##   "filtres": {"trainee": false, "seuil_trainee": 20, "membres": ["handF"], "etirement": false,
##               "fantomes": false, "poussiere": false}
##
## Par événement (dans "evenements", voir Combat) :
##   {"f": 29, "type": "impact", "forme": "etoile", "articulation": "handF", "dir": 0, "taille": 1, "couleur": "#ffffff"}
##       formes : etoile, anneau, bouffee, etincelles, sphere, final (§ 10.6)
##   {"f": 29, "type": "zoom", "force": 1.3, "n": 15, "articulation": "handF"}  (§ 10.12)
##   {"f": 29, "type": "ecran", "mode": "blanc", "n": 2}  (§ 10.7, 10.8)
##       modes : impact (fond noir, silhouettes blanches, rayons), blanc,
##       delave, assombrir, teinte, flash ; "force" = opacité, "couleur"
##   {"f": 29, "type": "image_impact", "version": "complete", "articulation": "handF"}
##       la séquence entière du § 10.7 : noir, blanc, délavé, zoom
##   {"f": 29, "type": "secousse", "mode": "coup", "amp": 0.08, "n": 10}  (§ 10.11)
##       modes : coup, decroit ("decroissance": 0.75), grondement ;
##       amp en hauteur de personnage (H = 180) ; sans mode, l'ancienne secousse
##   {"f": 20, "type": "fantomes", "n": 8}   force les fantômes n images
##   {"f": 20, "type": "flou", "n": 4}       flou de mouvement n images

const H := 180.0
const BG := Color("#9a9a9a")

## Réglages par défaut des filtres automatiques (unités du monde, images à 60 i/s).
const AUTO := {
	"trainee": true,
	"seuil_trainee": 13.0,   # l'extrémité doit avancer d'au moins ça en une image
	"duree_trainee": 3,      # nombre d'images que couvre le ruban
	"membres": [],           # extrémités qui peuvent laisser une traînée (vide = toutes) : handN, handF, toeN, toeF
	"etirement": true,
	"seuil_etirement": 22.0,
	"etirement_max": 0.3,    # bras jusqu'à 1,3 fois sa longueur
	"fantomes": true,
	"seuil_fantomes": 16.0,  # le bassin doit avancer d'au moins ça en une image
	"poussiere": true,
	"seuil_poussiere": 2.5,  # pied posé qui glisse d'au moins ça en une image
}

const TIPS := {
	"handN": {"os": ["armN", "foreN"], "coude": "foreN", "proche": true},
	"handF": {"os": ["armF", "foreF"], "coude": "foreF", "proche": false},
	"toeN": {"os": ["thighN", "shinN"], "coude": "shinN", "proche": true},
	"toeF": {"os": ["thighF", "shinF"], "coude": "shinF", "proche": false},
}


static func reglage(anim: Dictionary, k: String):
	var f: Dictionary = anim.get("filtres", {})
	return f.get(k, AUTO[k])


# ---------- Calcul (pendant la simulation) ----------

## Rubans de traînée : [{proche, points: [Vector2], ages: [float], largeur}],
## du plus récent au plus ancien. poses = [actuelle, précédente, …] (monde).
static func trainees(poses: Array, anim: Dictionary) -> Array:
	var out := []
	if poses.size() < 2 or not reglage(anim, "trainee"):
		return out
	var seuil: float = reglage(anim, "seuil_trainee")
	var n: int = mini(int(reglage(anim, "duree_trainee")), poses.size() - 1)
	var sols := poses.map(func(p): return StickRig.solve(p))
	var w: float = sols[0].style.stroke
	var sol_g: float = sols[0].style.stroke * 2.0
	var membres: Array = reglage(anim, "membres")
	for tip in TIPS:
		if not sols[0].joints.has(tip) or (not membres.is_empty() and not tip in membres):
			continue
		# Un pied qui avance au ras du sol (un pas) ne laisse pas de traînée.
		if tip.begins_with("toe") and sols[0].joints[tip].y < sol_g:
			continue
		var pts: Array = [_bout(sols[0], tip)]
		var ages: Array = [0.0]
		for k in n:
			var a: Dictionary = poses[k + 1]
			var b: Dictionary = poses[k]
			if int(a.facing) != int(b.facing):
				break
			var d: float = sols[k].joints[tip].distance_to(sols[k + 1].joints[tip])
			if d < seuil:
				break
			# Entre deux images, on interpole les angles : l'extrémité décrit
			# un arc autour de l'épaule ou de la hanche, comme dans les références.
			var m := clampi(int(d / 6.0), 2, 10)
			for j in range(1, m + 1):
				var u := float(j) / m
				var q := StickRig.lerp_pose(b, a, u)
				pts.append(_bout(StickRig.solve(q), tip))
				ages.append(k + u)
		if pts.size() >= 3:
			# Le ruban a la largeur du poing (ou du trait pour un pied).
			var lg: float = 2.0 * float(sols[0].style.hand) if tip.begins_with("hand") else w
			out.append({"proche": TIPS[tip].proche, "points": pts, "ages": ages, "duree": float(n), "largeur": lg})
	return out


## Bout du membre : le devant du poing (dans le prolongement de l'avant-bras),
## pas le poignet ; la pointe du pied.
static func _bout(sol: Dictionary, tip: String) -> Vector2:
	var J: Dictionary = sol.joints
	if tip.begins_with("hand"):
		var side := tip.substr(4)
		var d: Vector2 = (J[tip] - J["elbow" + side]).normalized()
		return J[tip] + d * float(sol.style.hand)
	return J[tip]


## Étirement du membre qui se détend vite : renvoie la pose à dessiner.
static func etirement(pose: Dictionary, avant: Dictionary, anim: Dictionary) -> Dictionary:
	if avant.is_empty() or not reglage(anim, "etirement") or int(pose.facing) != int(avant.facing):
		return pose
	var seuil: float = reglage(anim, "seuil_etirement")
	var mx: float = reglage(anim, "etirement_max")
	var J1: Dictionary = StickRig.solve(pose).joints
	var J0: Dictionary = StickRig.solve(avant).joints
	var g: float = StickRig.get_style(pose.style).stroke
	var q := pose
	var copie := false
	for tip in TIPS:
		var info: Dictionary = TIPS[tip]
		var v: float = J1[tip].distance_to(J0[tip])
		if v < seuil:
			continue
		# Seulement un membre presque tendu (coude ou genou à moins de 30°),
		# et une jambe en l'air (un pied posé ne doit pas quitter le sol).
		if absf(StickRig.angle(pose, info.coude)) > 30.0:
			continue
		if tip.begins_with("toe") and J1["ankle" + tip.substr(3)].y < g * 1.5:
			continue
		var k := 1.0 + minf(mx, mx * (v - seuil) / seuil)
		if not copie:
			q = StickRig.clone_pose(pose)
			copie = true
		var e: Dictionary = q.get("etire", {}).duplicate()
		for o in info.os:
			e[o] = float(e.get(o, 1.0)) * k
		q.etire = e
	return q


## Fantômes : poses précédentes à dessiner pâles [{pose, alpha}].
static func fantomes(poses: Array, anim: Dictionary, force := false) -> Array:
	var out := []
	if poses.size() < 3:
		return out
	if not force:
		if not reglage(anim, "fantomes"):
			return out
		var d: float = Vector2(float(poses[0].x), float(poses[0].y)).distance_to(Vector2(float(poses[1].x), float(poses[1].y)))
		if d < float(reglage(anim, "seuil_fantomes")):
			return out
	# Une copie toutes les deux images, de plus en plus pâle.
	var alphas := [0.4, 0.25, 0.12]
	for i in alphas.size():
		var k := 2 * (i + 1)
		if k < poses.size():
			out.append({"pose": poses[k], "alpha": alphas[i]})
	return out


## Flou : copies intermédiaires entre l'image précédente et l'actuelle.
static func flou(poses: Array) -> Array:
	var out := []
	if poses.size() < 3:
		return out
	# Du plus loin (le plus pâle) au plus proche, dessinés sous le corps.
	for j in 4:
		var u := 1.0 - j / 4.0
		out.append({"pose": StickRig.lerp_pose(poses[0], poses[2], u), "alpha": 0.08 + 0.06 * j})
	return out


## Pieds posés qui glissent : positions où laisser un dôme de poussière.
static func glissades(pose: Dictionary, avant: Dictionary, anim: Dictionary) -> Array:
	var out := []
	if avant.is_empty() or not reglage(anim, "poussiere"):
		return out
	var J1: Dictionary = StickRig.solve(pose).joints
	var J0: Dictionary = StickRig.solve(avant).joints
	var g: float = StickRig.get_style(pose.style).stroke
	for side in ["N", "F"]:
		var a1: Vector2 = J1["ankle" + side]
		var a0: Vector2 = J0["ankle" + side]
		if a1.y < g and a0.y < g and absf(a1.x - a0.x) >= float(reglage(anim, "seuil_poussiere")):
			out.append(Vector2(a1.x, 0.0))
	return out


# ---------- Effets à durée de vie ----------

const VIE := {"etoile": 4, "anneau": 10, "bouffee": 9, "etincelles": 22, "sphere": 18, "final": 24, "dome": 30}


static func effet(forme: String, pos: Vector2, dir: float, taille := 1.0, couleur := Color.WHITE) -> Dictionary:
	return {"forme": forme, "pos": pos, "dir": dir, "taille": taille, "couleur": couleur, "age": 0,
		"graine": int(absf(pos.x) * 7.0 + absf(pos.y) * 13.0) % 997}


static func vie(e: Dictionary) -> int:
	return VIE.get(e.forme, 12)


## Secousse de caméra (décalage vertical, unités du monde) à l'âge donné.
## Le décor descend d'abord, puis remonte d'un peu moins, etc. ; une valeur
## est tenue 2 images (une image à 24 i/s ≈ 2,5 images à 60).
static func secousse(s: Dictionary) -> Vector2:
	var age: int = s.age
	if age >= int(s.n):
		return Vector2.ZERO
	var mode: String = s.mode
	if mode == "lineaire":
		# Ancienne secousse : amortie en ligne droite, sur les deux axes.
		var r := int(s.n) - age
		var k: float = float(s.amp) * float(r) / float(s.n)
		var sg := 1.0 if r % 2 == 0 else -1.0
		return Vector2(sg * k, -sg * k * 0.5)
	var pas: int = int(s.get("pas", 2))
	var i := age / pas
	var sg2 := -1.0 if i % 2 == 0 else 1.0
	var a: float = float(s.amp)
	match mode:
		"coup":
			var seq := [1.0, 0.6, 0.35, 0.2, 0.1]
			a *= seq[mini(i, seq.size() - 1)] if i < seq.size() else 0.0
		"decroit":
			a *= pow(float(s.get("decroissance", 0.75)), i)
		"grondement":
			pass
	return Vector2(0.0, sg2 * a)


## Facteur de zoom à l'âge donné : plein d'un coup, retour en douceur.
static func zoom(z: Dictionary) -> float:
	var u := clampf(float(z.age) / float(z.n), 0.0, 1.0)
	return 1.0 + (float(z.force) - 1.0) * (1.0 - u) * (1.0 - u)


## Séquence « image d'impact » (§ 10.7) : [{mode, debut, n, force}] et zoom.
static func sequence_impact(version: String) -> Array:
	if version == "courte":
		return [{"mode": "assombrir", "debut": 0, "n": 3, "force": 0.5},
			{"mode": "delave", "debut": 3, "n": 3, "force": 0.55}]
	return [{"mode": "impact", "debut": 0, "n": 3},
		{"mode": "blanc", "debut": 3, "n": 2},
		{"mode": "delave", "debut": 5, "n": 4, "force": 0.6}]


# ---------- Dessin ----------

static func _S(v: Vector2, o: Vector2, scale: float) -> Vector2:
	return StickRig.to_screen(v, o, scale)


## Couleur « transparente » posée sur le fond gris de la planche : pour les
## fantômes, une vraie transparence noircirait les articulations (traits
## superposés), alors on mélange avec le fond.
static func pale(col: Color, alpha: float) -> Color:
	return BG.lerp(col, alpha)


static func draw_trainee(ci: CanvasItem, tr: Dictionary, o: Vector2, scale: float, col: Color) -> void:
	var pts: Array = tr.points
	var ages: Array = tr.ages
	var n := pts.size()
	var dur: float = maxf(1.0, tr.duree)
	var w0: float = tr.largeur * scale
	var P := []
	for p in pts:
		P.append(_S(p, o, scale))
	# Une normale par point (moyenne des deux segments voisins) : les morceaux
	# du ruban partagent leurs bords, sans couture ni recouvrement.
	var N := []
	for i in n:
		var d := Vector2.ZERO
		if i > 0:
			d += (P[i] - P[i - 1]).normalized()
		if i < n - 1:
			d += (P[i + 1] - P[i]).normalized()
		N.append(Vector2(-d.y, d.x).normalized() if d.length() > 0.001 else Vector2.UP)
	var L := []
	var C := []
	for i in n:
		var u: float = clampf(float(ages[i]) / dur, 0.0, 1.0)
		# Épais et opaque près du membre, fin et transparent au bout.
		L.append(w0 * (1.0 - 0.75 * u) / 2.0)
		C.append(Color(col, 0.85 * (1.0 - u)))
	for i in n - 1:
		var a: Vector2 = P[i]
		var b: Vector2 = P[i + 1]
		if a.distance_to(b) < 0.01:
			continue
		# Deux triangles plutôt qu'un quadrilatère : dans un virage serré le
		# quadrilatère peut se croiser et ne plus se laisser trianguler.
		var p0: Vector2 = a + N[i] * L[i]
		var p1: Vector2 = b + N[i + 1] * L[i + 1]
		var p2: Vector2 = b - N[i + 1] * L[i + 1]
		var p3: Vector2 = a - N[i] * L[i]
		ci.draw_primitive(PackedVector2Array([p0, p1, p2]), PackedColorArray([C[i], C[i + 1], C[i + 1]]), PackedVector2Array())
		ci.draw_primitive(PackedVector2Array([p0, p2, p3]), PackedColorArray([C[i], C[i + 1], C[i]]), PackedVector2Array())


static func draw_effet(ci: CanvasItem, e: Dictionary, o: Vector2, scale: float) -> void:
	var t: float = float(e.age) / float(vie(e))
	var c: Vector2 = _S(e.pos, o, scale)
	var T: float = float(e.taille) * scale
	var col: Color = e.couleur
	var rng := RandomNumberGenerator.new()
	rng.seed = int(e.graine)
	var dirv := Vector2(cos(deg_to_rad(e.dir)), -sin(deg_to_rad(e.dir)))
	match e.forme:
		"etoile":
			# Étoile blanche à 8 branches, 0,3 H, une image à 24 i/s.
			var r: float = 0.15 * H * T
			_etoile(ci, c, r, r * 0.22, 8, rng.randf() * 0.4, Color(col, 1.0 - t * 0.5))
		"anneau":
			# Cercle fin qui reste sur place, s'ouvre un peu et pâlit.
			var r2: float = (0.2 + 0.1 * t) * H * T
			ci.draw_arc(c, r2, 0.0, TAU, 40, Color(Color("#d0d0d0"), 0.9 * (1.0 - t)), maxf(1.0, 2.5 * scale * (1.0 - t)), true)
		"bouffee":
			# Nuage qui part dans la direction dir (le dos du touché), grossit et pâlit.
			for i in 5:
				var ang := rng.randf_range(-0.6, 0.6)
				var dv := dirv.rotated(ang)
				var dist := (0.05 + 0.12 * t + rng.randf() * 0.04) * H * T
				var rr := (0.04 + 0.05 * t + rng.randf() * 0.02) * H * T
				ci.draw_circle(c + dv * dist, rr, Color(Color("#e6e6e6"), 0.75 * (1.0 - t)))
		"etincelles":
			_etincelles(ci, c, dirv, T, t, col, rng, 12, 0.35)
		"sphere":
			# Disque plein qui pâlit sans changer de taille, plus une onde grise brève.
			var r3: float = 0.2 * H * T
			var a3: float = 1.0 if e.age < 4 else 1.0 - (e.age - 4) / 14.0
			ci.draw_circle(c, r3, Color(col, 0.85 * a3))
			ci.draw_circle(c, r3 * 0.55, Color(Color.WHITE, 0.9 * a3))
			if e.age < 5:
				ci.draw_arc(c, (0.3 + 1.45 * e.age / 5.0) * H * T, 0.0, TAU, 64, Color(Color("#bdbdbd"), 0.6 * (1.0 - e.age / 5.0)), 3.0 * scale, true)
		"final":
			# Étoile, disque qui grandit en pâlissant, étincelles en rayons.
			# Étoile (1 image à 24 i/s), disque plein (1), puis il grandit en
			# pâlissant (4) : 6 images à 24 i/s, soit environ 15 à 60 i/s.
			if e.age < 3:
				_etoile(ci, c, 0.25 * H * T, 0.05 * H * T, 10, 0.0, Color.WHITE)
			elif e.age < 15:
				var u4 := float(e.age - 3) / 12.0
				ci.draw_circle(c, (0.25 + 0.08 * u4) * H * T, Color(col, 0.4 * (1.0 - u4)))
			_etincelles(ci, c, Vector2.ZERO, T * 2.0, t, col.lightened(0.3), rng, 14, 1.0)
		"dome":
			# Petit dôme de poussière posé au sol, qui pâlit sur place.
			var r5: float = 0.06 * H * T * (1.0 + 0.3 * t)
			ci.draw_circle(c, r5, Color(Color("#d8d4cf"), 0.8 * (1.0 - t)))


static func _etoile(ci: CanvasItem, c: Vector2, r: float, r_in: float, k: int, rot: float, col: Color) -> void:
	var pts := PackedVector2Array()
	for i in 2 * k:
		var rr := r if i % 2 == 0 else r_in
		var a := rot + PI * i / k
		pts.append(c + Vector2(cos(a), sin(a)) * rr)
	ci.draw_colored_polygon(pts, col)


## Étincelles : des tirets dans le sens du coup qui s'écartent, raccourcissent,
## puis ne sont plus que des points. dirv nul = dans toutes les directions.
static func _etincelles(ci: CanvasItem, c: Vector2, dirv: Vector2, T: float, t: float, col: Color, rng: RandomNumberGenerator, n: int, cone: float) -> void:
	for i in n:
		var dv: Vector2
		if dirv == Vector2.ZERO:
			dv = Vector2.RIGHT.rotated(TAU * i / n + rng.randf_range(-0.2, 0.2))
		else:
			dv = dirv.rotated(rng.randf_range(-cone, cone) * PI)
		var vit := rng.randf_range(0.6, 1.0)
		var dist := (0.08 + 0.45 * sqrt(t) * vit) * H * T * 0.5
		var p := c + dv * dist
		var a := 1.0 - t
		if t < 0.35:
			var lg := (0.05 + 0.05 * vit) * H * T * 0.5 * (1.0 - t / 0.35 * 0.6)
			ci.draw_line(p, p - dv * lg, Color(col, a), maxf(1.0, 1.6 * T / 2.0), true)
		else:
			ci.draw_circle(p, maxf(0.8, 1.2 * T / 2.0), Color(col, a))


## Filtres plein écran, dessinés par-dessus tout (sauf « impact », géré à part).
static func draw_ecran(ci: CanvasItem, ec: Dictionary, sz: Vector2) -> void:
	var u := clampf(float(ec.age) / maxf(1.0, float(ec.n)), 0.0, 1.0)
	var r := Rect2(Vector2.ZERO, sz)
	match ec.mode:
		"blanc":
			ci.draw_rect(r, Color.WHITE)
		"delave":
			ci.draw_rect(r, Color(Color.WHITE, float(ec.get("force", 0.6)) * (1.0 - u)))
		"assombrir":
			ci.draw_rect(r, Color(Color.BLACK, float(ec.get("force", 0.3))))
		"teinte":
			ci.draw_rect(r, Color(Color(str(ec.get("couleur", "#ffd43b"))), float(ec.get("force", 0.25))))
		"flash":
			ci.draw_rect(r, Color(Color(str(ec.get("couleur", "#ffffff"))), float(ec.get("force", 0.9)) * (1.0 - u)))


## Image d'impact : fond noir, traits radiaux, lueur au point de contact,
## silhouettes en blanc.
static func draw_image_impact(ci: CanvasItem, rec: Dictionary, o: Vector2, scale: float, sz: Vector2, focus: Vector2) -> void:
	ci.draw_rect(Rect2(Vector2.ZERO, sz), Color("#0d0d0d"))
	var c := _S(focus, o, scale)
	var rng := RandomNumberGenerator.new()
	rng.seed = 7
	var box := Rect2(Vector2.ZERO, sz)
	for i in 40:
		var a := TAU * i / 40.0 + rng.randf_range(-0.05, 0.05)
		var r0 := rng.randf_range(0.18, 0.35) * H * scale
		var dv := Vector2(cos(a), sin(a))
		# Le trait s'arrête au bord de l'image (rien ne déborde sur une planche).
		var fin := _bord(c, dv, box)
		if fin > r0:
			ci.draw_line(c + dv * r0, c + dv * fin, Color("#2b2b2b"), rng.randf_range(2.0, 7.0) * scale / 2.0, true)
	for fig in rec.fighters:
		StickRig.draw_pose(ci, fig.pose, o, scale, Color("#f1f1f1"), 1.0, 1.0)
	for k in 4:
		ci.draw_circle(c, (0.12 + 0.06 * k) * H * scale, Color(Color.WHITE, 0.55 - 0.12 * k))


## Distance du point c au bord du rectangle, dans la direction dv.
static func _bord(c: Vector2, dv: Vector2, r: Rect2) -> float:
	var t := INF
	if dv.x > 0.0001:
		t = minf(t, (r.end.x - c.x) / dv.x)
	elif dv.x < -0.0001:
		t = minf(t, (r.position.x - c.x) / dv.x)
	if dv.y > 0.0001:
		t = minf(t, (r.end.y - c.y) / dv.y)
	elif dv.y < -0.0001:
		t = minf(t, (r.position.y - c.y) / dv.y)
	return maxf(0.0, t)
