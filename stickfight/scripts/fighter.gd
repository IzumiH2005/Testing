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
		var cur := local_pose()
		var dx := float(cur.x)
		x += facing * dx
		if fondu > 0:
			cur.x = 0.0
			blend_from = cur
			blend_len = fondu
			blend_t = 0
	anim = StickAnim.load_named(nom)
	t = t0
	history.clear()


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
	if not anim.boucle and t >= anim.duree:
		var nxt: String = anim.suivante
		if nxt != "":
			var over: float = t - float(anim.duree)
			play(nxt, 0, over)
		else:
			t = anim.duree
	return evs


func local_pose() -> Dictionary:
	var p := StickAnim.sample(anim, t)
	if blend_len > 0 and not blend_from.is_empty():
		var u := float(blend_t) / blend_len
		u = u * u * (3.0 - 2.0 * u)
		p = StickRig.lerp_pose(blend_from, p, u)
		StickRig.ground_feet(p)
	return p


func to_world(p: Dictionary) -> Dictionary:
	var q := StickRig.clone_pose(p)
	q.x = x + facing * float(p.x)
	q.facing = facing
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
