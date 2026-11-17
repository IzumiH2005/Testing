extends SceneTree
## Rendu d'une animation (ou d'un « duo ») en planche contact, en
## stroboscopie ou en images, pour la régler image par image sans ouvrir
## l'éditeur.
##
##   tools/anim.sh anims/blocage_bas.json -o /tmp/planche.png --de 0 --a 24
##   tools/anim.sh anims/blocage_bas.json --strobe /tmp/strobe.png --suivre handN,handF,head
##   tools/anim.sh anims/duo_blocage.json -o /tmp/duo.png --pas 2 --cols 8
##   tools/anim.sh anims/garde_idle.json --images /tmp/img     (une image PNG par image)
##   tools/anim.sh anims/garde_idle.json --print               (articulations par image)
##   tools/anim.sh anims/garde_idle.json --gif /tmp/a.gif       (via anim.sh et ffmpeg)
##
## -o f.png      planche contact : une case par image, numérotée
## --de n --a n  intervalle d'images globales (0 et la fin par défaut)
## --pas n       une image sur n dans la planche ou la stroboscopie
## --cols n      cases par ligne (6 par défaut)
## --strobe f    toutes les images superposées (de bleu clair à rouge clair,
##               la dernière en noir) avec la trajectoire des articulations
##               suivies : un point par image, pour voir les arcs et l'espacement
## --suivre a,b  articulations suivies (handN, handF, head, ankleN, hip...)
## --images dir  une PNG par image (frame_0000.png...)
## --boucles n  une boucle est jouée n fois (1 par défaut)
## --vue x,y,l,h rectangle du monde affiché (sinon calculé)
## --scale n     pixels par unité (2 par défaut)
## --debug       squelette coloré par-dessus
## --print       positions des articulations, angles hors amplitude
## --verifier    contrôle en texte, sans image (voir _verifier) : poses clés,
##               images de trajet rapide, pieds qui glissent, poing caché,
##               déséquilibre, distance du poing à la tête adverse au contact,
##               membres qui se traversent (en 3D : mains, avant-bras, bras)
## --cles        planche des seules images clés (et du contact), pas toutes
## --vues        chaque image sous trois angles, une ligne par angle : de face,
##               de trois quarts, de profil (le corps tourne sur place, lacet
##               +90°, +45°, +0°) ; pour vérifier qu'aucun axe n'est oublié
##
## Une animation seule est jouée sans enchaîner sur « suivante ».

const TRACK_COLORS := ["#e8590c", "#1971c2", "#2f9e44", "#ae3ec9", "#f08c00", "#0c8599"]


func _initialize() -> void:
	_run.call_deferred()


func _fail(msg: String) -> void:
	printerr(msg)
	quit(1)


func _abs(path: String) -> String:
	if path.begins_with("res://") or path.is_absolute_path():
		return path
	return ProjectSettings.globalize_path("res://").path_join(path)


func _parse(argv: PackedStringArray) -> Dictionary:
	var a := {"file": "", "out": "", "strobe": "", "images": "", "de": -1, "a": -1, "pas": 1, "cols": 6,
		"suivre": [], "vue": [], "scale": 2.0, "debug": false, "print": false, "boucles": 1,
		"verifier": false, "cles": false, "vues": false}
	var i := 0
	while i < argv.size():
		var k := argv[i]
		match k:
			"-o", "--out":
				i += 1
				a.out = argv[i]
			"--strobe", "--images":
				i += 1
				a[k.substr(2)] = argv[i]
			"--de", "--a", "--pas", "--cols", "--boucles":
				i += 1
				a[k.substr(2)] = int(argv[i])
			"--scale":
				i += 1
				a.scale = float(argv[i])
			"--suivre":
				i += 1
				a.suivre = Array(argv[i].split(","))
			"--vue":
				i += 1
				a.vue = Array(argv[i].split(",")).map(func(s): return float(s))
			"--debug", "--print", "--verifier", "--cles", "--vues":
				a[k.substr(2)] = true
			_:
				a.file = k
		i += 1
	return a


## Simule et renvoie toutes les images (records) de 0 à la fin.
func _simulate(path: String, boucles := 1) -> Dictionary:
	var data = JSON.parse_string(FileAccess.get_file_as_string(path))
	if not (data is Dictionary):
		return {}
	var combat: Combat
	var total := 0
	var single := {}
	if data.has("acteurs"):
		combat = Combat.from_duo(data)
		total = int(data.get("longueur", 120))
	else:
		single = StickAnim.build(data)
		single.suivante = ""
		StickAnim._cache[single.nom] = single
		combat = Combat.new()
		var f := combat.add(Fighter.new(0.0, 1))
		f.play(single.nom)
		total = int(ceil(single.duree)) * (maxi(1, boucles) if single.boucle else 1)
		for e in single.evenements:
			if e.type == "hitstop":
				total += int(e.get("n", 0))
	var recs := []
	for g in total + 1:
		recs.append(combat.record())
		combat.step()
	return {"recs": recs, "single": single, "data": data}


func _default_view(recs: Array) -> Rect2:
	var x0 := INF
	var x1 := -INF
	var y0 := 0.0
	var y1 := 0.0
	for r in recs:
		for fig in r.fighters:
			var J: Dictionary = StickRig.solve(fig.pose).joints
			for k in J:
				var v := StickRig.depth_point(fig.pose, J[k])
				x0 = minf(x0, v.x)
				x1 = maxf(x1, v.x)
				y0 = minf(y0, v.y)
				y1 = maxf(y1, v.y)
	x0 -= 30.0
	x1 += 30.0
	# Un pas vers la caméra (profondeur) descend sous la ligne de sol.
	var bas := minf(-12.0, floorf(y0 - 10.0))
	var h := maxf(212.0, y1 + 50.0) - 12.0 - bas
	return Rect2(floorf(x0 / 10.0) * 10.0, bas, ceilf((x1 - x0) / 10.0) * 10.0, h)


func _caption(r: Dictionary) -> String:
	var parts := ["%d" % r.g]
	for fig in r.fighters:
		parts.append("%s %s" % [fig.anim, str(snappedf(fig.t, 0.01))])
	if r.hitstop > 0:
		parts.append("■ arrêt %d" % r.hitstop)
	return "  ".join(parts)


func _make_planche(view: Rect2, scale: float, debug: bool) -> Planche:
	var pl := Planche.new()
	pl.view = view
	pl.px_per_unit = scale
	pl.grid = true
	pl.debug = false
	return pl


func _set_record(pl: Planche, r: Dictionary, debug: bool) -> void:
	pl.figures = []
	pl.caption = _caption(r)
	pl.extra_draw = func(ci: Planche) -> void:
		Combat.draw_record(ci, r, ci.origin_px(), ci.px_per_unit)
		if debug:
			for fig in r.fighters:
				ci._draw_debug(fig.pose)
	pl.queue_redraw()


func _grab(vp: SubViewport) -> Image:
	for _f in 2:
		await RenderingServer.frame_post_draw
	return vp.get_texture().get_image()


func _report(r: Dictionary) -> String:
	var lines := []
	for fig in r.fighters:
		var J: Dictionary = StickRig.solve(fig.pose).joints
		var pts := []
		for k in ["hip", "shoulder", "head", "handN", "handF", "elbowN", "ankleN", "ankleF"]:
			pts.append("%s(%.1f,%.1f)" % [k, J[k].x, J[k].y])
		var v := StickRig.violations(fig.pose)
		var vs := ""
		if not v.is_empty():
			vs = "  ⚠ " + ", ".join(v.map(func(x): return "%s=%.1f" % [x.id, x.value]))
		lines.append("%3d %s@%.2f  %s%s" % [r.g, fig.anim, fig.t, " ".join(pts), vs])
	return "\n".join(lines)


func _run() -> void:
	var a := _parse(OS.get_cmdline_user_args())
	if a.file == "":
		_fail("Usage : tools/anim.sh anims/x.json [-o planche.png] [--strobe s.png] (voir tools/anim.gd)")
		return
	var sim := _simulate(_abs(a.file), a.boucles)
	if sim.is_empty():
		_fail("Fichier illisible : " + a.file)
		return
	var recs: Array = sim.recs
	var de: int = 0 if a.de < 0 else a.de
	var fin: int = recs.size() - 1 if a.a < 0 else mini(a.a, recs.size() - 1)
	var sel := []
	var g := de
	while g <= fin:
		if not a.cles or _est_cle(recs, g):
			sel.append(recs[g])
		g += (1 if a.cles else a.pas)
	if a.verifier:
		print(_verifier(recs.slice(de, fin + 1)))
	if a.vues:
		# Une ligne par angle de vue ; sans effets (ils ont été calculés de profil).
		var n0 := sel.size()
		var lignes := []
		for lac in [90.0, 45.0, 0.0]:
			for r in sel:
				var r2: Dictionary = r.duplicate(true)
				r2.vfx = []
				r2.effets = []
				r2.ecrans = []
				for fig in r2.fighters:
					fig.pose.angles.lacet = float(fig.pose.angles.get("lacet", 0.0)) + lac
					fig.trainees = []
					fig.smears = []
					fig.fantomes = []
					fig.flou = []
				lignes.append(r2)
		sel = lignes
		a.cols = n0
	if sel.is_empty():
		_fail("Aucune image dans l'intervalle.")
		return
	if a.print:
		for r in recs.slice(de, fin + 1):
			print(_report(r))
	var view: Rect2 = Rect2(a.vue[0], a.vue[1], a.vue[2], a.vue[3]) if a.vue.size() == 4 else _default_view(recs.slice(de, fin + 1))
	var scale: float = a.scale

	if a.out != "":
		var cols: int = mini(a.cols, sel.size())
		var rows := int(ceil(float(sel.size()) / cols))
		var cell := Vector2i(roundi(view.size.x * scale), roundi(view.size.y * scale))
		var vp := SubViewport.new()
		vp.disable_3d = true
		vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
		vp.size = Vector2i(cell.x * cols + (cols - 1) * 2, cell.y * rows + (rows - 1) * 2)
		root.add_child(vp)
		var bg := ColorRect.new()
		bg.color = Color("#5c5c5c")
		bg.size = Vector2(vp.size)
		vp.add_child(bg)
		for i in sel.size():
			var pl := _make_planche(view, scale, a.debug)
			pl.position = Vector2((i % cols) * (cell.x + 2), (i / cols) * (cell.y + 2))
			_set_record(pl, sel[i], a.debug)
			vp.add_child(pl)
		var img: Image = await _grab(vp)
		img.save_png(_abs(a.out))
		print("Planche : " + a.out)
		vp.queue_free()

	if a.strobe != "":
		var vp := SubViewport.new()
		vp.disable_3d = true
		vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
		var sc := scale * 1.5
		vp.size = Vector2i(roundi(view.size.x * sc), roundi(view.size.y * sc))
		root.add_child(vp)
		var pl := _make_planche(view, sc, false)
		var span := recs.slice(de, fin + 1)
		var tracks: Array = a.suivre
		pl.caption = "%s  images %d-%d, une sur %d" % [a.file.get_file(), de, fin, a.pas]
		pl.extra_draw = func(ci: Planche) -> void:
			var n := sel.size()
			for i in n:
				var u := float(i) / maxf(1.0, n - 1)
				var col := Color("#a5d8ff").lerp(Color("#ffa8a8"), u)
				col.a = 0.55
				if i == n - 1:
					col = Color("#111111")
				for fig in sel[i].fighters:
					StickRig.draw_pose(ci, fig.pose, ci.origin_px(), ci.px_per_unit, col)
			for ti in tracks.size():
				var tc := Color(TRACK_COLORS[ti % TRACK_COLORS.size()])
				for fi in span[0].fighters.size():
					var pts := PackedVector2Array()
					for r in span:
						pts.append(ci.world_to_px(StickRig.solve(r.fighters[fi].pose).joints[tracks[ti]]))
					if pts.size() > 1:
						ci.draw_polyline(pts, tc, 2.0, true)
					for p in pts:
						ci.draw_circle(p, 3.0, Color.BLACK)
						ci.draw_circle(p, 2.0, tc)
			# Clés de l'animation seule : anneaux sur les trajectoires.
			if not sim.single.is_empty():
				for k in sim.single.cles:
					var gk := -1
					for j in span.size():
						if absf(span[j].fighters[0].t - k.f) < 0.01:
							gk = j
							break
					if gk < 0:
						continue
					for ti in tracks.size():
						var p := ci.world_to_px(StickRig.solve(span[gk].fighters[0].pose).joints[tracks[ti]])
						ci.draw_arc(p, 6.0, 0, TAU, 16, Color.BLACK, 2.0)
		vp.add_child(pl)
		var img: Image = await _grab(vp)
		img.save_png(_abs(a.strobe))
		print("Stroboscopie : " + a.strobe)
		vp.queue_free()

	if a.images != "":
		DirAccess.make_dir_recursive_absolute(_abs(a.images))
		var vp := SubViewport.new()
		vp.disable_3d = true
		vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
		vp.size = Vector2i(roundi(view.size.x * scale) / 2 * 2, roundi(view.size.y * scale) / 2 * 2)
		root.add_child(vp)
		var pl := _make_planche(view, scale, a.debug)
		pl.grid = false
		vp.add_child(pl)
		var n := 0
		for r in recs.slice(de, fin + 1):
			_set_record(pl, r, a.debug)
			pl.caption = ""
			var img: Image = await _grab(vp)
			img.save_png(_abs(a.images).path_join("frame_%04d.png" % n))
			n += 1
		print("Images : %d dans %s" % [n, a.images])
	quit(0)


## Image clé : un combattant est sur une clé de son animation (première image
## où il l'atteint) ou sur son événement contact.
func _est_cle(recs: Array, g: int) -> bool:
	for i in recs[g].fighters.size():
		var fig: Dictionary = recs[g].fighters[i]
		var t := float(fig.t)
		if g > 0 and recs[g - 1].fighters[i].anim == fig.anim and float(recs[g - 1].fighters[i].t) == t:
			continue
		var an := StickAnim.load_named(str(fig.anim))
		if an.is_empty():
			continue
		for k in an.cles:
			if float(k.f) == t:
				return true
		if StickAnim.event_frame(an, "contact") == t:
			return true
	return false


## Contrôle en texte d'une animation ou d'un duo. Les seuils suivent
## BIBLE_ANIMATION.md : trajet rapide = plus de 12 unités par image.
func _verifier(recs: Array) -> String:
	var L := []
	var tips := ["handN", "handF", "toeN", "toeF"]
	var nf: int = recs[0].fighters.size()
	for i in nf:
		var nom := "ABCD"[i]
		L.append("== %s ==" % nom)
		var vites := {}
		for tp in tips:
			vites[tp] = []
		var glisse := []
		var alertes := {}
		var prev: Dictionary = {}
		for r in recs:
			var fig: Dictionary = r.fighters[i]
			var sol := StickRig.solve(fig.pose)
			var J: Dictionary = sol.joints
			var g0: float = sol.style.stroke / 2.0
			var tag := "%d (%s %d)" % [r.g, fig.anim, int(fig.t)]
			var warn := []
			# Poing proche caché dans la tête (même couleur : illisible). Le poing
			# loin derrière la tête est normal (garde) : on ne le signale pas.
			if J.handN.distance_to(J.head) < sol.head_r - float(sol.style.hand) * 0.5:
				warn.append("poing proche caché dans la tête")
			# Membre presque invisible : trop raccourci par la profondeur (il pointe
			# vers la caméra ou à l'opposé), il se fond dans le corps.
			for side in ["N", "F"]:
				for pair in [["arm", "shoulder", "elbow" + side, "hand" + side, "upperArm", "forearm"], ["jambe", "hip", "knee" + side, "ankle" + side, "thigh", "shin"]]:
					var vrai: float = float(sol.style[pair[4]]) + float(sol.style[pair[5]])
					var vu: float = J[pair[1]].distance_to(J[pair[2]]) + J[pair[2]].distance_to(J[pair[3]])
					if vu < 0.55 * vrai:
						warn.append("%s %s raccourci à moins de 55 %% de sa longueur" % ["bras" if pair[0] == "arm" else "jambe", "proche" if side == "N" else "loin"])
			# Membre confondu avec le corps : le coude (ou le genou) et la main (ou
			# la cheville) sont tous les deux dans le tronc ou la tête. Dans les
			# vidéos de référence, un membre qui passe devant le corps le croise,
			# et ses deux bouts dépassent de la silhouette.
			var tronc := [J.hip, J.waist, J.shoulder]
			var bande: float = float(sol.style.stroke) * 0.9
			var dedans := func(v: Vector2) -> bool:
				if v.distance_to(J.head) < sol.head_r:
					return true
				for i2 in tronc.size() - 1:
					if Geometry2D.get_closest_point_to_segment(v, tronc[i2], tronc[i2 + 1]).distance_to(v) < bande:
						return true
				return false
			for side in ["N", "F"]:
				if dedans.call(J["elbow" + side]) and dedans.call(J["hand" + side]):
					warn.append("bras %s confondu avec le corps" % ("proche" if side == "N" else "loin"))
			# Part visible du bras proche : points du bras hors de la tête et du
			# tronc. Sous 35 %, il se lit à peine (le coude doit dépasser).
			var vis := 0
			var tot := 0
			for segm in [[J.shoulder, J.elbowN], [J.elbowN, J.handN]]:
				for u in range(1, 11):
					var pt: Vector2 = segm[0].lerp(segm[1], u / 10.0)
					tot += 1
					if not dedans.call(pt):
						vis += 1
			# Un bras qui pend le long du corps (main sous la taille) est normal.
			if vis < 0.35 * tot and J.handN.y > J.waist.y:
				warn.append("bras proche peu visible (moins de 35 % hors du corps)")
			var jF := [J.hip, J.kneeF, J.ankleF]
			var pres := func(v: Vector2) -> bool:
				for i3 in 2:
					if Geometry2D.get_closest_point_to_segment(v, jF[i3], jF[i3 + 1]).distance_to(v) < bande:
						return true
				return false
			if pres.call(J.kneeN) and pres.call(J.ankleN):
				warn.append("jambes superposées")
			# Membres qui se traversent, en 3D (profondeur comprise) : deux parties
			# du corps peuvent se toucher, pas passer l'une dans l'autre. On compare
			# les avant-bras et les mains entre eux (trait = capsule, poing = boule).
			for t3 in _traversees(sol):
				warn.append(t3)
			for v in StickRig.amplitudes(fig.pose):
				warn.append(str(v.label))
			for v in StickRig.violations(fig.pose):
				if float(v.value) < float(v.lim.x) - 1.0 or float(v.value) > float(v.lim.y) + 1.0:
					warn.append("%s hors amplitude" % str(v.label))
			if StickRig.lowest_y(fig.pose) < -1.0:
				warn.append("sous le sol")
			# Déséquilibre : deux pieds au sol, bassin hors de la base d'appui.
			if J.ankleN.y < g0 + 2.0 and J.ankleF.y < g0 + 2.0:
				var lo := minf(J.ankleN.x, J.ankleF.x) - 8.0
				var hi := maxf(J.ankleN.x, J.ankleF.x) + 8.0
				# Seulement debout : un corps couché n'a pas d'appui à respecter.
				if (J.hip.x < lo or J.hip.x > hi) and J.hip.y > 45.0:
					warn.append("bassin hors des appuis")
			if not prev.is_empty():
				var J0: Dictionary = prev.J
				for tp in tips:
					var d: float = J[tp].distance_to(J0[tp])
					if d > 12.0:
						vites[tp].append("%d:%d" % [r.g, roundi(d)])
				for side in ["N", "F"]:
					var a1: Vector2 = J["ankle" + side]
					var a0: Vector2 = J0["ankle" + side]
					if a1.y < g0 + 1.0 and a0.y < g0 + 1.0 and absf(a1.x - a0.x) > 1.5 and r.hitstop == 0:
						glisse.append("%s%d" % [side, r.g])
			# Contact : distance des poings et des pieds à la tête et au buste adverses.
			var an := StickAnim.load_named(str(fig.anim))
			var cf := StickAnim.event_frame(an, "contact") if not an.is_empty() else -1.0
			var debut: bool = prev.is_empty() or prev.anim != fig.anim or float(prev.t) != float(fig.t)
			if cf >= 0.0 and float(fig.t) == cf and debut:
				for j in nf:
					if j == i:
						continue
					var Jb: Dictionary = StickRig.solve(r.fighters[j].pose).joints
					var best := ""
					var bd := INF
					for tp in tips:
						for cible in ["head", "shoulder", "waist"]:
							var d2: float = J[tp].distance_to(Jb[cible])
							if d2 < bd:
								bd = d2
								best = "%s → %s de %s" % [tp, cible, "ABCD"[j]]
					warn.append("contact : %s à %d" % [best, roundi(bd)])
			var contact := ""
			for w in warn:
				if w.begins_with("contact"):
					contact = "  ⚠ " + w
				else:
					if not alertes.has(w):
						alertes[w] = []
					alertes[w].append(r.g)
			if _est_cle(recs, recs.find(r)) or contact != "":
				var ang := "coudes %d/%d genoux %d/%d buste %d" % [roundi(StickRig.angle(fig.pose, "foreN")), roundi(StickRig.angle(fig.pose, "foreF")),
					roundi(StickRig.angle(fig.pose, "shinN")), roundi(StickRig.angle(fig.pose, "shinF")),
					roundi(StickRig.angle(fig.pose, "root") + StickRig.angle(fig.pose, "spineLow") + StickRig.angle(fig.pose, "chest"))]
				ang += "  torsion %d/%d  tête y %d" % [roundi(StickRig.angle(fig.pose, "torsion")), roundi(StickRig.angle(fig.pose, "torsionBassin")), roundi(J.head.y)]
				var prof := []
				for k in fig.pose.angles:
					if (str(k).ends_with(StickRig.PROF) or k == "lacet") and absf(float(fig.pose.angles[k])) > 0.5:
						prof.append("%s %d" % [k, roundi(float(fig.pose.angles[k]))])
				if not prof.is_empty():
					ang += "  profondeur " + " ".join(prof)
				# Longueur apparente de chaque membre (100 = de profil, à plat).
				var app := []
				for m in [["brasN", "shoulder", "elbowN", "handN", "upperArm", "forearm"], ["brasF", "shoulder", "elbowF", "handF", "upperArm", "forearm"],
						["jambeN", "hip", "kneeN", "ankleN", "thigh", "shin"], ["jambeF", "hip", "kneeF", "ankleF", "thigh", "shin"]]:
					var vrai2: float = float(sol.style[m[4]]) + float(sol.style[m[5]])
					var vu2: float = J[m[1]].distance_to(J[m[2]]) + J[m[2]].distance_to(J[m[3]])
					if vu2 < 0.97 * vrai2:
						app.append("%s %d %%" % [m[0], roundi(100.0 * vu2 / vrai2)])
				if not app.is_empty():
					ang += "  longueur vue " + " ".join(app)
				L.append("%s  %s  poingN(%d,%d)%s" % [tag, ang, roundi(J.handN.x), roundi(J.handN.y), contact])
			prev = {"J": J, "anim": fig.anim, "t": fig.t}
		for tp in tips:
			if not vites[tp].is_empty():
				L.append("trajet rapide %s : %s" % [tp, " ".join(vites[tp])])
		if not glisse.is_empty():
			L.append("pied qui glisse : " + " ".join(glisse))
		for w in alertes:
			L.append("⚠ %s : images %s" % [w, _plages(alertes[w])])
	return "\n".join(L)


## Points 3D d'une pose résolue (x, y de l'image, z = profondeur).
static func _p3(sol: Dictionary, k: String) -> Vector3:
	return Vector3(sol.joints[k].x, sol.joints[k].y, float(sol.prof.get(k, 0.0)))


## Distance la plus courte entre deux segments 3D.
static func _dist_seg(a0: Vector3, a1: Vector3, b0: Vector3, b1: Vector3) -> float:
	var pts := Geometry3D.get_closest_points_between_segments(a0, a1, b0, b1)
	return pts[0].distance_to(pts[1])


## Parties des deux bras qui passent l'une dans l'autre (tolérance : 15 % de
## l'épaisseur, le contact franc est permis). Renvoie aussi la plus petite
## marge (négative = enfoncement) dans _derniere_marge pour le réglage.
static var _derniere_marge := INF


static func _traversees(sol: Dictionary) -> Array:
	var out := []
	var w: float = float(sol.style.stroke) / 2.0
	var h: float = maxf(float(sol.style.hand), w)
	var eN := _p3(sol, "elbowN")
	var hN := _p3(sol, "handN")
	var eF := _p3(sol, "elbowF")
	var hF := _p3(sol, "handF")
	var sN := _p3(sol, "shoulderN")
	var sF := _p3(sol, "shoulderF")
	var tests := [
		["mains qui se traversent", hN.distance_to(hF), 2.0 * h],
		["avant-bras qui se traversent", _dist_seg(eN, hN, eF, hF), 2.0 * w],
		["main proche dans l'avant-bras loin", _dist_seg(eF, hF, hN, hN), h + w],
		["main loin dans l'avant-bras proche", _dist_seg(eN, hN, hF, hF), h + w],
		["avant-bras proche dans le bras loin", _dist_seg(eN, hN, sF.lerp(eF, 0.3), eF), 2.0 * w],
		["avant-bras loin dans le bras proche", _dist_seg(eF, hF, sN.lerp(eN, 0.3), eN), 2.0 * w],
	]
	_derniere_marge = INF
	for t in tests:
		var marge: float = float(t[1]) - float(t[2])
		_derniere_marge = minf(_derniere_marge, marge)
		if marge < -0.15 * float(t[2]):
			out.append(str(t[0]))
	return out


## [3, 4, 5, 9] → "3-5 9"
func _plages(gs: Array) -> String:
	var out := []
	var a: int = gs[0]
	var b: int = gs[0]
	for k in range(1, gs.size()):
		if gs[k] == b + 1:
			b = gs[k]
		else:
			out.append(str(a) if a == b else "%d-%d" % [a, b])
			a = gs[k]
			b = gs[k]
	out.append(str(a) if a == b else "%d-%d" % [a, b])
	return " ".join(out)
