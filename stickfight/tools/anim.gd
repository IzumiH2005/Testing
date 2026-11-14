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
		"suivre": [], "vue": [], "scale": 2.0, "debug": false, "print": false, "boucles": 1}
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
			"--debug", "--print":
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
	var y1 := 0.0
	for r in recs:
		for fig in r.fighters:
			var J: Dictionary = StickRig.solve(fig.pose).joints
			for k in J:
				x0 = minf(x0, J[k].x)
				x1 = maxf(x1, J[k].x)
				y1 = maxf(y1, J[k].y)
	x0 -= 30.0
	x1 += 30.0
	var h := maxf(212.0, y1 + 50.0)
	return Rect2(floorf(x0 / 10.0) * 10.0, -12.0, ceilf((x1 - x0) / 10.0) * 10.0, h)


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
		sel.append(recs[g])
		g += a.pas
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
