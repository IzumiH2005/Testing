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
##   {"f": 29, "type": "onde", "articulation": "pieds", "dir": -90, "taille": 1.4}  (posée au sol sous l'articulation ;
##       "pieds" = milieu des deux chevilles, valable pour tous les effets)
##   {"f": 28, "type": "choc", "articulation": "hip", "dir": 10, "taille": 1}
##   {"f": 0, "type": "eclat", "n": 10, "couleur": "#ff4d4d"}  (le corps entier
##       s'entoure d'un liseré coloré qui s'amincit : armure, coup encaissé)
##   {"f": 8, "type": "contact"}  (repère de synchronisation, ne fait rien)
##   {"f": 9, "type": "fenetre", "nom": "contre", "n": 20}  (fenêtre ouverte de f
##       à f + n − 1 : ici, après une parade ou une esquive, la contre-attaque
##       propre au personnage peut annuler la fin de l'animation ; "esquive"
##       marque les images où le corps est hors de la trajectoire ; voir
##       Fighter.en_fenetre)
## Effets calculés (voir Filtres pour le détail) :
##   {"f": 29, "type": "impact", "forme": "etincelles", "articulation": "handF", "dir": 0, "taille": 1, "couleur": "#ffd43b"}
##   {"f": 29, "type": "zoom", "force": 1.3, "n": 15, "articulation": "handF"}
##   {"f": 29, "type": "ecran", "mode": "delave", "n": 4, "force": 0.6}
##   {"f": 29, "type": "image_impact", "version": "complete", "articulation": "handF"}
##   {"f": 29, "type": "secousse", "mode": "coup", "amp": 0.08, "n": 10}
##   {"f": 20, "type": "fantomes", "n": 8} / {"f": 20, "type": "flou", "n": 4}
## Les angles « dir » sont donnés dans le repère du personnage (0 = devant,
## -90 = vers le bas) et retournés s'il regarde à gauche.

var fighters: Array = []
var vfx: Array = []
var g := 0
var hitstop := 0
## Images écoulées depuis le début de l'arrêt sur image en cours.
var hitstop_age := 0
## Pendant un arrêt, la traînée reste quelques images, les fantômes moins.
const TRAINEE_ARRET := 2
const FANTOMES_ARRET := 2
## Secousses de caméra en cours : [{mode, amp, n, age, pas, decroissance}].
var secousses: Array = []
## Zooms en cours : [{force, n, age, focus}].
var zooms: Array = []
## Filtres plein écran en cours : [{mode, n, age, debut, force, couleur, focus}].
var ecrans: Array = []
## Effets calculés (impacts, poussière) : voir Filtres.effet.
var effets: Array = []
## [{g, acteur, anim, fondu}]
var programme: Array = []
## Faux : aucun effet calculé (pour comparer avec et sans).
var filtres_actifs := true


func add(f: Fighter) -> Fighter:
	fighters.append(f)
	return f


## Combat décrit par un fichier « duo » :
## {"nom", "longueur", "acteurs": [{"x", "facing", "couleur", "anim", "t0",
##   "programme": [{"g": 30, "anim": "...", "fondu": 4} | {"contact": 52, "anim": "..."}
##                 | {"g": 52, "couche": "armure_encaisse"}]}]}
## « contact » cale l'animation pour que son événement contact tombe à
## l'image globale donnée. « couche » superpose une réaction à l'animation
## en cours sans l'interrompre (voir Fighter.couche).
static func from_duo(data: Dictionary) -> Combat:
	var c := Combat.new()
	for i in data.acteurs.size():
		var a: Dictionary = data.acteurs[i]
		var f := Fighter.new(float(a.get("x", 0.0)), int(a.get("facing", 1)), Color(str(a.get("couleur", "#111111"))))
		f.play(str(a.anim), 0, float(a.get("t0", 0.0)))
		c.add(f)
		for e in a.get("programme", []):
			var gg := int(e.get("g", 0))
			if e.has("couche"):
				c.programme.append({"g": gg, "acteur": i, "couche": str(e.couche)})
				continue
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
		hitstop_age += 1
	else:
		hitstop_age = 0
		for f in fighters:
			for ev in f.step():
				fired.append([f, ev])
	for v in vfx:
		v.age += 1
	vfx = vfx.filter(func(v): return v.age < Vfx.life(v))
	for e in effets:
		e.age += 1
	effets = effets.filter(func(e): return e.age < Filtres.vie(e))
	for lst in [secousses, zooms, ecrans]:
		for e in lst:
			e.age += 1
	secousses = secousses.filter(func(e): return e.age < int(e.n))
	zooms = zooms.filter(func(e): return e.age < int(e.n))
	ecrans = ecrans.filter(func(e): return e.age < int(e.debut) + int(e.n))
	if hitstop == 0 and g % 2 == 0:
		for f in fighters:
			if not f.trace.is_empty():
				for p in Filtres.glissades(f.to_world(f.local_pose()), f.trace[0], f.anim):
					effets.append(Filtres.effet("dome", p, 0.0))
	for pair in fired:
		_handle(pair[0], pair[1])
	g += 1
	start_programmed()


## Démarre les animations programmées pour l'image courante (l'image 0 de
## l'animation est donc bien affichée à l'image g prévue).
func start_programmed() -> void:
	for e in programme:
		if e.g == g:
			if e.has("couche"):
				couche(fighters[e.acteur], e.couche)
			else:
				fighters[e.acteur].play(e.anim, e.fondu)


## Superpose une couche de réaction et traite tout de suite ses événements
## de l'image 0 (l'arrêt sur impact commence à cette image).
func couche(f: Fighter, nom: String) -> void:
	for ev in f.couche(nom):
		_handle(f, ev)


func _world_dir(f: Fighter, d: float) -> float:
	return d if f.facing > 0 else 180.0 - d


func _handle(f: Fighter, ev: Dictionary) -> void:
	match str(ev.type):
		"hitstop":
			hitstop = maxi(hitstop, int(ev.get("n", 6)))
			f.shake_n = int(ev.get("n", 6))
			f.shake_amp = float(ev.get("tremble", 0.0))
		"eclat":
			f.eclat_n = int(ev.get("n", 10))
			f.eclat_len = f.eclat_n
			f.eclat_color = Color(str(ev.get("couleur", "#ff4d4d")))
		"secousse":
			var amp := float(ev.get("force", 2.0))
			if ev.has("amp"):
				amp = float(ev.amp) * Filtres.H
			secousses.append({"mode": str(ev.get("mode", "lineaire")), "amp": amp, "n": int(ev.get("n", 6)),
				"age": 0, "pas": int(ev.get("pas", 2)), "decroissance": float(ev.get("decroissance", 0.75))})
		"impact":
			effets.append(Filtres.effet(str(ev.get("forme", "etoile")), _pos(f, ev),
				_world_dir(f, float(ev.get("dir", 0.0))), float(ev.get("taille", 1.0)),
				Color(str(ev.get("couleur", "#ffffff")))))
		"zoom":
			zooms.append({"force": float(ev.get("force", 1.3)), "n": int(ev.get("n", 15)), "age": 0, "focus": _pos(f, ev)})
		"ecran":
			ecrans.append({"mode": str(ev.get("mode", "blanc")), "n": int(ev.get("n", 2)), "age": 0, "debut": 0,
				"force": float(ev.get("force", 0.6)), "couleur": str(ev.get("couleur", "#ffffff")), "focus": _pos(f, ev)})
		"image_impact":
			var version := str(ev.get("version", "complete"))
			var focus := _pos(f, ev)
			var total := 0
			for e in Filtres.sequence_impact(version):
				var e2: Dictionary = e.duplicate()
				e2.age = 0
				e2.focus = focus
				e2.force = float(e.get("force", 0.6))
				ecrans.append(e2)
				total = maxi(total, int(e.debut) + int(e.n))
			if version == "complete":
				zooms.append({"force": float(ev.get("zoom", 1.3)), "n": int(ev.get("n_zoom", 18)), "age": -total, "focus": focus})
			# Les corps restent figés pendant la séquence (elle remplace l'arrêt sur image).
			hitstop = maxi(hitstop, total + int(ev.get("tenue", 0)))
		"fantomes":
			f.fantomes_n = int(ev.get("n", 8))
		"flou":
			f.flou_n = int(ev.get("n", 4))
		"etincelle", "poussiere", "vitesse", "onde", "choc":
			var pos := _pos(f, ev)
			vfx.append(Vfx.make(str(ev.type), pos, {"dir": _world_dir(f, float(ev.get("dir", 0.0))),
				"genre": ev.get("genre", "garde"), "taille": ev.get("taille", 1.0)}))


## Position d'un événement : articulation du combattant (« pieds » = milieu
## des deux chevilles), plus un décalage « dec » dans son repère.
func _pos(f: Fighter, ev: Dictionary) -> Vector2:
	var J: Dictionary = StickRig.solve(f.to_world(f.local_pose())).joints
	var art := str(ev.get("articulation", "hip"))
	var pos: Vector2 = (J.ankleN + J.ankleF) / 2.0 if art == "pieds" else J.get(art, J.hip)
	var dec = ev.get("dec", [0, 0])
	return pos + Vector2(f.facing * float(dec[0]), float(dec[1]))


## Décalage de la caméra : somme des secousses en cours.
func camera_offset() -> Vector2:
	var v := Vector2.ZERO
	for sc in secousses:
		v += Filtres.secousse(sc)
	return v


## Zoom en cours (le plus fort) : {k, focus}.
func camera_zoom() -> Dictionary:
	var best := {"k": 1.0, "focus": Vector2.ZERO}
	for z in zooms:
		if int(z.age) < 0:
			continue
		var k := Filtres.zoom(z)
		if k > float(best.k):
			best = {"k": k, "focus": z.focus}
	return best


## Tout ce qu'il faut pour dessiner l'image courante.
func record() -> Dictionary:
	var figs := []
	for f in fighters:
		var fl: Dictionary = f.filtres() if filtres_actifs else {"pose": f.world_pose(), "trainees": [], "fantomes": [], "flou": []}
		# Les corps sont figés pendant l'arrêt : les effets de vitesse s'éteignent.
		if hitstop > 0 and hitstop_age >= TRAINEE_ARRET:
			fl.trainees = []
		if hitstop > 0 and hitstop_age >= FANTOMES_ARRET:
			fl.fantomes = []
			fl.flou = []
		figs.append({"pose": fl.pose, "color": f.color, "smears": f.smears(),
			"trainees": fl.trainees, "fantomes": fl.fantomes, "flou": fl.flou,
			"anim": f.anim_name(), "t": f.t,
			"eclat": float(f.eclat_n) / float(f.eclat_len), "eclat_color": f.eclat_color})
	var ecr := []
	for e in ecrans:
		if int(e.age) >= int(e.debut):
			var e2: Dictionary = e.duplicate()
			e2.age = int(e.age) - int(e.debut)
			ecr.append(e2)
	return {"g": g, "cam": camera_offset(), "zoom": camera_zoom(), "ecrans": ecr, "hitstop": hitstop,
		"fighters": figs, "vfx": vfx.duplicate(true), "effets": effets.duplicate(true)}


# ---------- Dessin ----------

static func draw_record(ci: CanvasItem, rec: Dictionary, origin: Vector2, scale: float, far_shade := 1.0) -> void:
	var sz: Vector2 = ci.size_px() if ci.has_method("size_px") else ci.get_viewport_rect().size
	# Zoom : on agrandit autour du point visé, qui reste où il est à l'écran.
	var zm: Dictionary = rec.get("zoom", {"k": 1.0, "focus": Vector2.ZERO})
	if float(zm.k) != 1.0:
		var fs := StickRig.to_screen(zm.focus, origin, scale)
		origin = fs + (origin - fs) * float(zm.k)
		scale *= float(zm.k)
	var o: Vector2 = origin + rec.cam * scale * Vector2(1, -1)
	for ec in rec.get("ecrans", []):
		if ec.mode == "impact":
			Filtres.draw_image_impact(ci, rec, o, scale, sz, ec.focus)
			return
		if ec.mode == "blanc":
			Filtres.draw_ecran(ci, ec, sz)
			return
	for v in rec.vfx:
		Vfx.draw(ci, v, o, scale, "derriere")
	# Le plus loin de la caméra d'abord (profondeur z, voir StickRig.depth).
	# Tri stable : à profondeur égale, l'ordre des acteurs est gardé.
	var figs: Array = []
	for i in rec.fighters.size():
		figs.append([float(rec.fighters[i].pose.get("z", 0.0)), i, rec.fighters[i]])
	figs.sort_custom(func(a, b): return a[0] > b[0] or (a[0] == b[0] and a[1] < b[1]))
	figs = figs.map(func(e): return e[2])
	for fig in figs:
		# Éclat d'armure : liseré épais, puis de plus en plus fin, puis rien.
		for gh in fig.get("fantomes", []):
			StickRig.draw_pose(ci, gh.pose, o, scale, Filtres.pale(fig.color, gh.alpha), 1.0)
		for tr in fig.get("trainees", []):
			if not tr.proche:
				Filtres.draw_trainee(ci, tr, o, scale, fig.color)
		for gh in fig.get("flou", []):
			StickRig.draw_pose(ci, gh.pose, o, scale, Filtres.pale(fig.color, gh.alpha), 1.0)
		var ec: float = fig.get("eclat", 0.0)
		if ec > 0.0:
			StickRig.draw_pose(ci, fig.pose, o, scale, fig.eclat_color, 1.0, 3.0 + 9.0 * ec)
		for sm in fig.smears:
			if not sm.proche:
				_draw_smear(ci, sm, o, scale, fig.color)
		StickRig.draw_pose(ci, fig.pose, o, scale, fig.color, far_shade)
		for sm in fig.smears:
			if sm.proche:
				_draw_smear(ci, sm, o, scale, fig.color)
		for tr in fig.get("trainees", []):
			if tr.proche:
				Filtres.draw_trainee(ci, tr, o, scale, fig.color)
	for v in rec.vfx:
		Vfx.draw(ci, v, o, scale, "devant")
	for e in rec.get("effets", []):
		Filtres.draw_effet(ci, e, o, scale)
	for ec in rec.get("ecrans", []):
		Filtres.draw_ecran(ci, ec, sz)


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
