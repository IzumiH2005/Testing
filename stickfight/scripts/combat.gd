class_name Combat
extends RefCounted
## Plusieurs combattants, le temps global, les effets et l'arrêt sur impact.
##
## À chaque step() :
##   1. si un arrêt sur impact est en cours, les poses restent figées (seul le
##      tremblement bouge), sinon chaque combattant avance d'une image ;
##   2. les événements franchis déclenchent effets, arrêts et secousses ;
##   3. les effets vieillissent (même pendant l'arrêt : l'étincelle éclate
##      pendant que les corps sont figés, comme dans les jeux de combat) ;
##   4. les animations programmées pour la nouvelle image démarrent.
##
## Événements d'animation reconnus (dans "evenements") :
##   {"f": 8, "type": "hitstop", "n": 8, "tremble": 1.5}
##   {"f": 8, "type": "etincelle", "articulation": "handN", "dec": [4, -3], "dir": -60, "genre": "garde", "taille": 1}
##   {"f": 8, "type": "secousse", "n": 6, "force": 2}
##   {"f": 14, "type": "poussiere", "articulation": "ankleN", "dir": 0}
##   {"f": 3, "type": "vitesse", "articulation": "hip", "dec": [-14, 22], "dir": 0}
##   {"f": 8, "type": "contact"}  (repère de synchronisation, ne fait rien)
## Les angles « dir » sont donnés dans le repère du personnage (0 = devant,
## -90 = vers le bas) et retournés s'il regarde à gauche.

var fighters: Array = []
var vfx: Array = []
var g := 0
var hitstop := 0
var cam_n := 0
var cam_len := 1
var cam_force := 0.0
## [{g, acteur, anim, fondu}]
var programme: Array = []


func add(f: Fighter) -> Fighter:
	fighters.append(f)
	return f


## Combat décrit par un fichier « duo » :
## {"nom", "longueur", "acteurs": [{"x", "facing", "couleur", "anim", "t0",
##   "programme": [{"g": 30, "anim": "...", "fondu": 4} | {"contact": 52, "anim": "..."}]}]}
## « contact » cale l'animation pour que son événement contact tombe à
## l'image globale donnée.
static func from_duo(data: Dictionary) -> Combat:
	var c := Combat.new()
	for i in data.acteurs.size():
		var a: Dictionary = data.acteurs[i]
		var f := Fighter.new(float(a.get("x", 0.0)), int(a.get("facing", 1)), Color(str(a.get("couleur", "#111111"))))
		f.play(str(a.anim), 0, float(a.get("t0", 0.0)))
		c.add(f)
		for e in a.get("programme", []):
			var gg := int(e.get("g", 0))
			if e.has("contact"):
				var an := StickAnim.load_named(str(e.anim))
				gg = int(e.contact) - int(StickAnim.event_frame(an, "contact"))
			c.programme.append({"g": gg, "acteur": i, "anim": str(e.anim), "fondu": int(e.get("fondu", 0))})
	c.start_programmed()
	return c


func step() -> void:
	for f in fighters:
		if f.shake_n > 0:
			f.shake_n -= 1
	var fired := []
	if hitstop > 0:
		hitstop -= 1
	else:
		for f in fighters:
			for ev in f.step():
				fired.append([f, ev])
	for v in vfx:
		v.age += 1
	vfx = vfx.filter(func(v): return v.age < Vfx.life(v))
	if cam_n > 0:
		cam_n -= 1
	for pair in fired:
		_handle(pair[0], pair[1])
	g += 1
	start_programmed()


## Démarre les animations programmées pour l'image courante (l'image 0 de
## l'animation est donc bien affichée à l'image g prévue).
func start_programmed() -> void:
	for e in programme:
		if e.g == g:
			fighters[e.acteur].play(e.anim, e.fondu)


func _world_dir(f: Fighter, d: float) -> float:
	return d if f.facing > 0 else 180.0 - d


func _handle(f: Fighter, ev: Dictionary) -> void:
	match str(ev.type):
		"hitstop":
			hitstop = maxi(hitstop, int(ev.get("n", 6)))
			f.shake_n = int(ev.get("n", 6))
			f.shake_amp = float(ev.get("tremble", 0.0))
		"secousse":
			cam_n = int(ev.get("n", 6))
			cam_len = cam_n
			cam_force = float(ev.get("force", 2.0))
		"etincelle", "poussiere", "vitesse":
			var J: Dictionary = StickRig.solve(f.to_world(f.local_pose())).joints
			var pos: Vector2 = J.get(str(ev.get("articulation", "hip")), J.hip)
			var dec = ev.get("dec", [0, 0])
			pos += Vector2(f.facing * float(dec[0]), float(dec[1]))
			vfx.append(Vfx.make(str(ev.type), pos, {"dir": _world_dir(f, float(ev.get("dir", 0.0))),
				"genre": ev.get("genre", "garde"), "taille": ev.get("taille", 1.0)}))


## Décalage de la caméra (secousse) : alterne, s'amortit.
func camera_offset() -> Vector2:
	if cam_n <= 0:
		return Vector2.ZERO
	var k := cam_force * float(cam_n) / float(cam_len)
	var s := 1.0 if cam_n % 2 == 0 else -1.0
	return Vector2(s * k, -s * k * 0.5)


## Tout ce qu'il faut pour dessiner l'image courante.
func record() -> Dictionary:
	var figs := []
	for f in fighters:
		figs.append({"pose": f.world_pose(), "color": f.color, "smears": f.smears(),
			"anim": f.anim_name(), "t": f.t})
	return {"g": g, "cam": camera_offset(), "hitstop": hitstop, "fighters": figs, "vfx": vfx.duplicate(true)}


# ---------- Dessin ----------

static func draw_record(ci: CanvasItem, rec: Dictionary, origin: Vector2, scale: float, far_shade := 1.0) -> void:
	var o: Vector2 = origin + rec.cam * scale * Vector2(1, -1)
	for fig in rec.fighters:
		for sm in fig.smears:
			if not sm.proche:
				_draw_smear(ci, sm, o, scale, fig.color)
		StickRig.draw_pose(ci, fig.pose, o, scale, fig.color, far_shade)
		for sm in fig.smears:
			if sm.proche:
				_draw_smear(ci, sm, o, scale, fig.color)
	for v in rec.vfx:
		Vfx.draw(ci, v, o, scale)


## Image « étalée » (smear) : l'avant-bras occupe tout l'espace balayé
## depuis l'image précédente, plus une traînée effilée derrière le poing.
static func _draw_smear(ci: CanvasItem, sm: Dictionary, o: Vector2, scale: float, col: Color) -> void:
	var S := func(v: Vector2) -> Vector2: return StickRig.to_screen(v, o, scale)
	var quad := PackedVector2Array([S.call(sm.coude0), S.call(sm.main0), S.call(sm.main1), S.call(sm.coude1)])
	if not Geometry2D.triangulate_polygon(quad).is_empty():
		ci.draw_colored_polygon(quad, col)
	var w := 15.0 * scale
	# Traînée : deux tronçons de plus en plus fins vers l'arrière.
	ci.draw_line(S.call(sm.main1), S.call(sm.main0), col, w * 0.9, true)
	ci.draw_circle(S.call(sm.main0), w * 0.45, col)
	ci.draw_line(S.call(sm.main0), S.call(sm.main_avant), col, w * 0.45, true)
