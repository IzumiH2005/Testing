extends SceneTree
## Place les mains en 3D (profondeur comprise) et écrit les angles des bras.
##
## `vise` ne règle que x et y : la profondeur de la main dépend alors de la rotation du
## bras, et deux mains qui doivent se toucher finissent l'une dans l'autre. Ici, une clé
## qui porte
##     "mains3d": {"N": [dx, dy, dz], "F": [dx, dy, dz]}
## (cible du centre du poing, relative à l'épaule, z = profondeur ; écartement du coude
## pris dans armN_p / armF_p de la clé) reçoit dans "fixe" les angles arm, fore et arm_r
## qui y mènent ; "mains3d" est retiré et la cible gardée dans "_mains3d" (relancer
## l'outil la réutilise). Chaque clé est résolue avec son propre buste.
##
##     tools/resout_mains.sh anims/x.json
## Les bras gardent la même branche d'une clé à l'autre (départ = clé précédente).
## Bornes : élévation −60..100, coude 40..160, rotation −180..180.

const LO := [-60.0, 40.0, -180.0]
const HI := [100.0, 160.0, 180.0]


func _p3(sol: Dictionary, k: String) -> Vector3:
	return Vector3(sol.joints[k].x, sol.joints[k].y, float(sol.prof.get(k, 0.0)))


func _err(pose: Dictionary, side: String, tgt: Vector3) -> float:
	return _p3(StickRig.solve(pose), "hand" + side).distance_to(tgt)


## Descente depuis `depart` (la solution de la clé précédente, pour que les bras ne
## changent pas de branche d'une clé à l'autre) ; tirages au hasard seulement si elle
## n'atteint pas la cible.
func _resout(pose: Dictionary, side: String, tgt: Vector3, depart: Array) -> Array:
	var ch := ["arm" + side, "fore" + side, "arm" + side + "_r"]
	var rng := RandomNumberGenerator.new()
	rng.seed = 7
	var best := INF
	var bestv := []
	for essai in 31:
		if essai > 0 and best < 0.3:
			break
		var v := []
		for c in 3:
			v.append(depart[c] if essai == 0 and not depart.is_empty() else rng.randf_range(LO[c], HI[c]))
			pose.angles[ch[c]] = v[c]
		var cur := _err(pose, side, tgt)
		var pas := 16.0
		while pas > 0.05:
			var mieux := false
			for c in 3:
				for sg in [-1.0, 1.0]:
					var nv: float = v[c] + sg * pas
					if nv < LO[c] or nv > HI[c]:
						continue
					pose.angles[ch[c]] = nv
					var e := _err(pose, side, tgt)
					if e < cur:
						cur = e
						v[c] = nv
						mieux = true
					else:
						pose.angles[ch[c]] = v[c]
			if not mieux:
				pas /= 2.0
		if cur < best:
			best = cur
			bestv = v.duplicate()
	for c in 3:
		pose.angles[ch[c]] = snappedf(bestv[c], 0.1)
	return [ch, bestv, best]


func _initialize() -> void:
	var chemin: String = OS.get_cmdline_user_args()[0]
	var data: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(chemin))
	var cles: Array = data.cles
	for k in cles:
		if k.has("mains3d"):
			k["_mains3d"] = k.mains3d
			k.erase("mains3d")
	var an := StickAnim.build(data)
	var AT = load("res://tools/anim.gd")
	var prec := {"N": [], "F": []}
	for i in cles.size():
		var k: Dictionary = cles[i]
		if not k.has("_mains3d"):
			continue
		var pose: Dictionary = an.cles[i].pose.duplicate(true)
		var S := _p3(StickRig.solve(pose), "shoulderN")
		for side in ["N", "F"]:
			var d: Array = k._mains3d[side]
			var r := _resout(pose, side, S + Vector3(d[0], d[1], d[2]), prec[side])
			prec[side] = r[1]
			for c in 3:
				k.fixe[r[0][c]] = snappedf(r[1][c], 0.1)
				if k.has("vise"):
					k.vise.erase("arm" + side)
			if r[2] > 0.5:
				printerr("clé %d : main %s à %.1f de sa cible" % [int(k.f), side, r[2]])
		var sol := StickRig.solve(pose)
		print("clé %d : mains à %.1f, traversées %s (marge %.1f)" % [int(k.f),
			_p3(sol, "handN").distance_to(_p3(sol, "handF")), AT._traversees(sol), AT._derniere_marge])
	var f := FileAccess.open(chemin, FileAccess.WRITE)
	f.store_string(JSON.stringify(data, " ", false) + "\n")
	quit()
