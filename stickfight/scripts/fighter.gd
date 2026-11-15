class_name Fighter
extends RefCounted
## Un combattant : une animation en cours, sa position dans l'arène, son
## sens, et ce qu'il faut pour les fondus et les traînées.
##
## Le temps avance d'une image par appel à step() (60 i/s). Pendant un arrêt
## sur impact, Combat n'appelle pas step() : la pose reste figée, seul le
## tremblement change.

var x := 0.0
var facing := 1
var color := Color("#111111")
var anim: Dictionary = {}
var t := 0.0
## Fondu depuis la pose affichée au moment du changement d'animation.
var blend_from: Dictionary = {}
var blend_len := 0
var blend_t := 0
## Tremblement pendant l'arrêt sur impact (images restantes, amplitude).
var shake_n := 0
var shake_amp := 0.0
## Poses locales des images précédentes (pour les traînées).
var history: Array = []
## Couches de réaction superposées à l'animation en cours, sans l'arrêter
## (armure : le coup est encaissé pendant que l'attaque ou la marche
## continue). [{anim, t, p0}] ; voir couche().
var couches: Array = []
## Éclat du corps (armure) : images restantes, durée, couleur.
var eclat_n := 0
var eclat_len := 1
var eclat_color := Color("#ff4d4d")


func _init(px := 0.0, pfacing := 1, pcolor := Color("#111111")) -> void:
	x = px
	facing = pfacing
	color = pcolor


func anim_name() -> String:
	return str(anim.get("nom", ""))


## Lance une animation. fondu = nombre d'images de transition depuis la pose
## actuelle (0 = coupe franche, quand la nouvelle commence là où l'autre finit).
## Le combattant reste où son bassin est arrivé : le déplacement local de
## l'animation qui s'arrête passe dans x, et la nouvelle repart de son
## propre repère (bassin de la base en 0).
func play(nom: String, fondu := 0, t0 := 0.0) -> void:
	blend_from = {}
	blend_len = 0
	if not anim.is_empty():
		# Sans les couches : elles continuent sur la nouvelle animation.
		var cur := local_pose(false)
		var dx := float(cur.x)
		x += facing * dx
		# L'animation finissait retournée (demi-tour) : le combattant change
		# de sens, et la pose de fondu est décrite dans ce nouveau sens.
		if StickRig.facing(cur) < 0.0:
			facing = -facing
			cur.facing = 1
		if fondu > 0:
			cur.x = 0.0
			blend_from = cur
			blend_len = fondu
			blend_t = 0
	anim = StickAnim.load_named(nom)
	t = t0
	history.clear()


## Superpose une animation de réaction (fichier marqué "couche": true) à
## l'animation en cours, qui continue. La couche n'ajoute que son écart à
## sa propre DERNIÈRE image (bassin, buste, cou, bras) : elle peut donc
## commencer déjà déformée (l'impact est instantané, et l'arrêt sur impact
## tient cette image) puis revenir à zéro ; les pieds posés restent
## où ils sont et les jambes s'y replient. Renvoie les événements de
## l'image 0 (arrêt sur impact, étincelle…), à traiter tout de suite.
func couche(nom: String) -> Array:
	var a := StickAnim.load_named(nom)
	couches.append({"anim": a, "t": 0.0, "p0": StickAnim.sample(a, float(a.duree))})
	return StickAnim.events_between(a, -1.0, 0.0)


## Vrai si l'image en cours est dans une fenêtre nommée de l'animation
## (événement {"type": "fenetre", "nom": nom, "f": a, "n": k} : images a à
## a + k − 1). Sert à savoir si une contre-attaque peut annuler la fin d'une
## parade ; la contre-attaque elle-même est propre à chaque personnage.
func en_fenetre(nom: String) -> bool:
	for e in anim.get("evenements", []):
		if str(e.get("type", "")) == "fenetre" and str(e.get("nom", "")) == nom:
			var a := float(e.get("f", 0))
			if t >= a and t < a + float(e.get("n", 0)):
				return true
	return false


## Avance d'une image. Renvoie les événements franchis.
func step() -> Array:
	if anim.is_empty():
		return []
	history.push_front(local_pose())
	if history.size() > 3:
		history.pop_back()
	var t0 := t
	t += 1.0
	if anim.boucle and float(anim.avance) != 0.0:
		var L := float(anim.longueur)
		var n := floorf(t / L) - floorf(t0 / L)
		if n != 0.0:
			var d: float = n * float(anim.avance)
			x += facing * d
			for h in history:
				h.x = float(h.x) - d
	if blend_len > 0:
		blend_t += 1
		if blend_t >= blend_len:
			blend_len = 0
			blend_from = {}
	var evs := StickAnim.events_between(anim, t0, t)
	for c in couches:
		evs.append_array(StickAnim.events_between(c.anim, c.t, c.t + 1.0))
		c.t += 1.0
	couches = couches.filter(func(c): return c.t < float(c.anim.duree))
	if eclat_n > 0:
		eclat_n -= 1
	if not anim.boucle and t >= anim.duree:
		var nxt: String = anim.suivante
		if nxt != "":
			var over: float = t - float(anim.duree)
			play(nxt, 0, over)
		else:
			t = anim.duree
	return evs


func local_pose(avec_couches := true) -> Dictionary:
	var p := StickAnim.sample(anim, t)
	if blend_len > 0 and not blend_from.is_empty():
		var u := float(blend_t) / blend_len
		u = u * u * (3.0 - 2.0 * u)
		p = StickRig.lerp_pose(blend_from, p, u)
		StickRig.ground_feet(p)
	if avec_couches and not couches.is_empty():
		p = _avec_couches(p)
	return p


const COUCHE_SANS := ["thighN", "shinN", "footN", "thighF", "shinF", "footF"]

func _avec_couches(p: Dictionary) -> Dictionary:
	var sol := StickRig.solve(p)
	var g: float = sol.style.stroke / 2.0
	var q := StickRig.clone_pose(p)
	for c in couches:
		var s := StickAnim.sample(c.anim, c.t)
		var s0: Dictionary = c.p0
		for k in s.angles:
			if not k in COUCHE_SANS:
				q.angles[k] = float(q.angles[k]) + float(s.angles[k]) - float(s0.angles[k])
		q.x = float(q.x) + float(s.x) - float(s0.x)
		q.y = float(q.y) + float(s.y) - float(s0.y)
	# Pieds posés : même cheville, même angle de pied qu'avant la couche.
	for side in ["N", "F"]:
		var ank: Vector2 = sol.joints["ankle" + side]
		if sol.joints["toe" + side].y < g + 1.0:
			var phi := StickRig.foot_phi(p, side)
			q = StickRig.reach(q, "leg" + side, ank)
			StickRig.set_foot(q, side, phi, false)
	return q


func to_world(p: Dictionary) -> Dictionary:
	var q := StickRig.clone_pose(p)
	q.x = x + facing * float(p.x)
	q.facing = facing * int(StickRig.facing(p))
	return q


## Pose dans l'arène, tremblement compris.
func world_pose() -> Dictionary:
	var q := to_world(local_pose())
	if shake_n > 0:
		q.x = float(q.x) + shake_amp * (1.0 if shake_n % 2 == 0 else -1.0)
	return q


## Point local (repère du personnage) → arène.
func point_to_world(v: Vector2) -> Vector2:
	return Vector2(x + facing * v.x, v.y)


## Traînées actives : formes en coordonnées de l'arène.
## [{proche: bool, coude0, main0, coude1, main1, main_avant}]
func smears() -> Array:
	var out := []
	if history.size() < 2:
		return out
	for tr in StickAnim.trails_at(anim, t):
		var art: String = tr.articulation
		var coude: String = tr.get("coude", "")
		var J1: Dictionary = StickRig.solve(world_pose()).joints
		var J0: Dictionary = StickRig.solve(to_world(history[0])).joints
		var Jm: Dictionary = StickRig.solve(to_world(history[1])).joints
		out.append({
			"proche": art.ends_with("N"),
			"coude0": J0.get(coude, J0[art]), "main0": J0[art],
			"coude1": J1.get(coude, J1[art]), "main1": J1[art],
			"main_avant": Jm[art],
		})
	return out
