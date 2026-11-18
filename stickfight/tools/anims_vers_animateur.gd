extends SceneTree
# Exporte les clés résolues (pose complète de chaque clé) de toutes les animations,
# pour les ouvrir dans web/animateur.html.
#   $GODOT --headless --path . -s tools/anims_vers_animateur.gd -- <sortie.json>
func _initialize():
	var argv := OS.get_cmdline_user_args()
	var out := {}
	var d := DirAccess.open("res://anims")
	for f in d.get_files():
		if not f.ends_with(".json"):
			continue
		var nom := f.get_basename()
		var a = StickAnim.load_named(nom)
		if a.is_empty():
			continue
		var cles := []
		for k in a.cles:
			var p: Dictionary = k.pose
			cles.append({"f": k.f, "courbe": k.courbe, "p": k.p, "plate": k.plate,
				"x": p.get("x", 0.0), "y": p.get("y", 0.0), "facing": p.get("facing", 1), "angles": p.get("angles", {})})
		out[nom] = {"longueur": a.longueur, "boucle": a.boucle, "cles": cles}
	var fa = FileAccess.open(argv[0], FileAccess.WRITE)
	fa.store_string(JSON.stringify(out))
	quit()
