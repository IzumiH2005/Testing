extends SceneTree
## Exporte en JSON la pose 3D calculée par StickRig.solve() (points et repères des
## os), pour poser le mannequin 3D de référence (tools/mannequin.py).
##
##   godot --headless --path . -s res://tools/pose3d.gd -- poses/x.json [--lacet -90,-45,0] [-o out.json]
##     [--set armN=40,armN_p+=10]   (angles modifiés sans toucher au fichier : k=v ou k+=n)
##
## Une entrée par lacet total imposé (-90 = de face, -45 = trois quarts face, 0 = profil),
## repère du personnage : x vers l'avant, y vers le haut, z négatif = côté caméra.

func _initialize() -> void:
	var argv := OS.get_cmdline_user_args()
	var path := ""
	var out := ""
	var lacets := [-90.0, -45.0, 0.0]
	var sets := []
	var i := 0
	while i < argv.size():
		if argv[i] == "-o":
			i += 1
			out = argv[i]
		elif argv[i] == "--lacet":
			i += 1
			lacets = []
			for s in argv[i].split(","):
				lacets.append(float(s))
		elif argv[i] == "--set":
			i += 1
			sets.append_array(argv[i].split(","))
		else:
			path = argv[i]
		i += 1
	if not path.is_absolute_path():
		path = ProjectSettings.globalize_path("res://").path_join(path)
	var p0: Dictionary = StickRig.load_pose(path)
	for s in sets:
		var add: bool = s.contains("+=")
		var kv: PackedStringArray = s.split("+=" if add else "=")
		var k := kv[0].strip_edges()
		var v := float(kv[1])
		if add:
			v += float(p0.angles.get(k, 0.0))
		p0.angles[k] = v
	var vues := []
	for lac in lacets:
		var p: Dictionary = p0.duplicate(true)
		p.angles.lacet = lac
		var sol := StickRig.solve(p)
		var o := Vector2(float(p.x), float(p.y))
		var f: float = sol.facing
		var pts := {}
		for k in sol.joints:
			var j: Vector2 = sol.joints[k]
			pts[k] = [(j.x - o.x) * f, j.y - o.y, float(sol.prof[k])]
		var bases := {}
		for k in sol.basis:
			var b: Basis = sol.basis[k]
			bases[k] = [[b.x.x, b.x.y, b.x.z], [b.y.x, b.y.y, b.y.z], [b.z.x, b.z.y, b.z.z]]
		vues.append({"lacet": lac, "points": pts, "bases": bases, "head_r": sol.head_r,
			"style": sol.style, "facing": f})
	var txt := JSON.stringify({"pose": path.get_file(), "vues": vues}, " ")
	if out == "":
		print(txt)
	else:
		var fa := FileAccess.open(out, FileAccess.WRITE)
		fa.store_string(txt)
	quit(0)
