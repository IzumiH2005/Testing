extends SceneTree
# Exporte des images d'une animation en poses JSON, pour les poser sur le mannequin.
#   $GODOT --headless --path . -s tools/cles_vers_poses.gd -- <anim> <dossier> <f1,f2,...>
#   puis : tools/mannequin.sh <dossier>/f13.json -o m13.png
func _initialize():
	var argv := OS.get_cmdline_user_args()
	if argv.size() < 3:
		push_error("usage : -- <anim> <dossier> <f1,f2,...>")
		quit(1)
		return
	var a = StickAnim.load_named(argv[0])
	DirAccess.make_dir_recursive_absolute(argv[1])
	for s in argv[2].split(","):
		var f := int(s)
		var p = StickAnim.sample(a, float(f))
		var chemin := argv[1].path_join("f%02d.json" % f)
		var fa = FileAccess.open(chemin, FileAccess.WRITE)
		fa.store_string(JSON.stringify(p, "\t"))
		print(chemin)
	quit()
