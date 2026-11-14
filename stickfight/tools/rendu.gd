extends SceneTree
## Rendu d'une ou plusieurs poses en PNG, depuis la ligne de commande, pour
## itérer finement sur une posture (modifier un angle, regarder, recommencer).
##
##   tools/rendu.sh poses/garde.json -o /tmp/garde.png --debug --grid
##   tools/rendu.sh poses/garde.json --set foreN+=3 --set chest-=2 -o /tmp/essai.png
##   tools/rendu.sh poses/garde.json --reach armN=40,140 --save
##   tools/rendu.sh a.json b.json -o /tmp/compare.png         (côte à côte)
##   tools/rendu.sh a.json b.json --overlay -o /tmp/onion.png  (superposées)
##
## --set k=v     angle (ou x, y, facing, style), valeur absolue (négatif permis : root=-4)
## --set k+=n    relatif (k-=n pour retirer)
## --reach m=x,y cinématique inverse : bout du membre (armN, armF, legN, legF) vers (x, y)
## --pin         garde les chevilles là où elles étaient avant les --set (pieds plantés)
## --plant       pose posée au sol (point le plus bas à y = 0)
## --free        ignore les amplitudes articulaires
## --save        réécrit le premier fichier avec les modifications
## --print       affiche la pose et les positions des articulations
## --scale n     pixels par unité (3 par défaut)
##
## Les chemins relatifs partent du dossier du projet (stickfight/).

const OVERLAY_COLORS := ["#c92a2a", "#1971c2", "#2f9e44", "#e8590c"]


func _initialize() -> void:
	_run.call_deferred()


func _fail(msg: String) -> void:
	printerr(msg)
	quit(1)


func _abs(path: String) -> String:
	if path.begins_with("res://") or path.begins_with("user://") or path.is_absolute_path():
		return path
	return ProjectSettings.globalize_path("res://").path_join(path)


func _parse(argv: PackedStringArray) -> Dictionary:
	var a := {"files": [], "set": [], "reach": [], "out": "", "scale": 3.0, "debug": false, "grid": false,
		"plant": false, "save": false, "print": false, "overlay": false, "free": false, "pin": false}
	var i := 0
	while i < argv.size():
		var k := argv[i]
		match k:
			"-o", "--out":
				i += 1
				a.out = argv[i]
			"--set":
				i += 1
				a.set.append(argv[i])
			"--reach":
				i += 1
				a.reach.append(argv[i])
			"--scale":
				i += 1
				a.scale = float(argv[i])
			"--debug", "--grid", "--plant", "--save", "--print", "--overlay", "--free", "--pin":
				a[k.substr(2)] = true
			_:
				a.files.append(k)
		i += 1
	return a


func _apply_edits(pose: Dictionary, a: Dictionary) -> Dictionary:
	var p := StickRig.clone_pose(pose)
	var J0: Dictionary = StickRig.solve(p).joints
	var limits: bool = not a.free
	var re_set := RegEx.create_from_string("^([A-Za-z]+)([+-]?)=(.+)$")
	for s in a.set:
		var m := re_set.search(s)
		if m == null:
			push_error("--set attendu sous la forme nom=valeur, nom+=n ou nom-=n : " + s)
			return {}
		var k := m.get_string(1)
		var v := m.get_string(3)
		if k == "style":
			p.style = v
			continue
		var rel := m.get_string(2) != ""
		var n := float(v) * (-1.0 if m.get_string(2) == "-" else 1.0)
		if k in ["x", "y", "facing"]:
			p[k] = float(p[k]) + n if rel else n
		elif StickRig.bone(k).is_empty():
			push_error("Articulation inconnue : " + k)
			return {}
		else:
			p.angles[k] = StickRig.round2((StickRig.angle(p, k) + n) if rel else n)
	if a.pin:
		p = StickRig.reach(p, "legN", J0.ankleN, limits)
		p = StickRig.reach(p, "legF", J0.ankleF, limits)
	var re_reach := RegEx.create_from_string("^(armN|armF|legN|legF)=(-?[\\d.]+),(-?[\\d.]+)$")
	for s in a.reach:
		var m := re_reach.search(s)
		if m == null:
			push_error("--reach attendu sous la forme armN=x,y : " + s)
			return {}
		p = StickRig.reach(p, m.get_string(1), Vector2(float(m.get_string(2)), float(m.get_string(3))), limits)
	if a.plant:
		p = StickRig.plant(p)
	return p


func _report(p: Dictionary) -> String:
	var J: Dictionary = StickRig.solve(p).joints
	var lines := ["Pose « %s »  bassin (%.1f)" % [p.nom, float(p.y)]]
	var ang := []
	for k in StickRig.angle_ids():
		ang.append("%s=%s" % [k, str(StickRig.round2(StickRig.angle(p, k)))])
	lines.append("  angles : " + "  ".join(ang))
	var js := []
	for k in J:
		js.append("%s(%.1f,%.1f)" % [k, J[k].x, J[k].y])
	lines.append("  articulations : " + " ".join(js))
	var v := StickRig.violations(p)
	if not v.is_empty():
		var vs := []
		for x in v:
			vs.append("%s %s ∉ [%d,%d]" % [x.label, str(x.value), x.lim.x, x.lim.y])
		lines.append("  ⚠ hors amplitude : " + ", ".join(vs))
	lines.append("  point le plus bas : y = %.2f" % StickRig.lowest_y(p))
	return "\n".join(lines)


func _run() -> void:
	var a := _parse(OS.get_cmdline_user_args())
	if a.files.is_empty():
		_fail("Usage : tools/rendu.sh pose.json [...] [-o sortie.png] (voir l'en-tête de tools/rendu.gd)")
		return
	var poses := []
	for i in a.files.size():
		var path := _abs(a.files[i])
		if not FileAccess.file_exists(path):
			_fail("Fichier introuvable : " + path)
			return
		var p := StickRig.load_pose(path)
		var edits: Dictionary = a if (i == 0 or a.overlay) else {"set": [], "reach": [], "plant": a.plant, "pin": false, "free": a.free}
		p = _apply_edits(p, edits)
		if p.is_empty():
			quit(1)
			return
		poses.append(p)

	if a.print or a.out == "":
		for p in poses:
			print(_report(p))
	if a.save:
		var err := StickRig.save_pose(poses[0], _abs(a.files[0]))
		if err != OK:
			_fail("Écriture impossible : " + a.files[0])
			return
		print("Enregistré : " + a.files[0])
	if a.out == "":
		quit(0)
		return

	# Une planche par pose (ou une seule pour --overlay), côte à côte.
	var panel := Vector2(240, 212)
	var vp := SubViewport.new()
	vp.disable_3d = true
	vp.transparent_bg = false
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	var count := 1 if a.overlay else poses.size()
	vp.size = Vector2i(roundi(panel.x * a.scale) * count, roundi(panel.y * a.scale))
	root.add_child(vp)
	for i in count:
		var pl := Planche.new()
		pl.px_per_unit = a.scale
		pl.grid = a.grid
		pl.debug = a.debug
		pl.view = Rect2(float(poses[0 if a.overlay else i].x) - panel.x / 2.0, -12, panel.x, panel.y)
		pl.position = Vector2(roundi(panel.x * a.scale) * i, 0)
		if a.overlay:
			var figs := []
			var names := []
			for j in poses.size():
				var col := Color("#111111") if j == poses.size() - 1 else Color(OVERLAY_COLORS[j % 4])
				figs.append({"pose": poses[j], "color": col})
				names.append(poses[j].nom)
			pl.figures = figs
			pl.caption = " / ".join(names)
		else:
			pl.figures = [{"pose": poses[i], "color": Color("#111111")}]
			pl.caption = poses[i].nom
		vp.add_child(pl)

	for _f in 3:
		await RenderingServer.frame_post_draw
	var img := vp.get_texture().get_image()
	if img == null or img.is_empty():
		_fail("Rendu vide : lancer avec un affichage (xvfb-run) et --rendering-driver opengl3, pas --headless.")
		return
	var out := _abs(a.out)
	var err := img.save_png(out)
	if err != OK:
		_fail("Écriture impossible : " + out)
		return
	print("Rendu : " + out)
	quit(0)
