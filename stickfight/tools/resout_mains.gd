extends SceneTree
## Place les mains en 3D (profondeur comprise) et écrit les angles des bras.
##
## `vise` ne règle que x et y : la profondeur de la main dépend alors de la rotation du
## bras, et deux mains qui doivent se toucher finissent l'une dans l'autre. Ici, une clé
## qui porte
##     "mains3d": {"N": [dx, dy, dz], "F": [dx, dy, dz],
##                 "coude_dy": 0, "coude_dx": -3, "ecart": [40, 60]}   (facultatifs ;
##                  coude_dy et coude_dx acceptent aussi [N, F])
## (cible du centre du poing, relative à l'épaule, x devant, y haut, z profondeur,
## N côté caméra = z négatif) reçoit dans "fixe" les angles arm, fore et arm_r qui y
## mènent. Sans "coude_dy", l'écartement du coude est celui de la clé (armN_p / armF_p).
## Avec "coude_dy", le coude est placé à cette hauteur par rapport à la main (0 = avant-bras
## horizontal) et l'écartement est cherché dans "ecart" (valeur absolue, en degrés).
## "mains3d" est retiré et gardé dans "_mains3d" (relancer l'outil la réutilise). Chaque
## clé est résolue avec son propre buste ; les bras repartent de la solution de la clé
## précédente, pour ne pas changer de branche d'une clé à l'autre.
##
##     tools/resout_mains.sh anims/x.json
## Bornes : élévation −60..100, coude 40..160, rotation −80..80 (limite du rig).

const LO := [-60.0, 40.0, -80.0, 0.0]
const HI := [100.0, 160.0, 80.0, 90.0]


func _p3(sol: Dictionary, k: String) -> Vector3:
	return Vector3(sol.joints[k].x, sol.joints[k].y, float(sol.prof.get(k, 0.0)))


var coude_dx = null  # position avant-arrière du coude par rapport à l'épaule (+ = devant)


func _err(pose: Dictionary, side: String, tgt: Vector3, coude) -> float:
	var sol := StickRig.solve(pose)
	var h := _p3(sol, "hand" + side)
	var e := 4.0 * h.distance_to(tgt)  # la main d'abord : le contact prime sur les coudes
	if coude != null:
		e += absf(sol.joints["elbow" + side].y - h.y - float(coude))
	if coude_dx != null:
		e += absf(sol.joints["elbow" + side].x - sol.joints["shoulderN"].x - float(coude_dx))
	return e


func _resout(pose: Dictionary, side: String, tgt: Vector3, depart: Array, coude, ecart: Array) -> Array:
	var sg_p := 1.0 if side == "N" else -1.0
	var ch := ["arm" + side, "fore" + side, "arm" + side + "_r", "arm" + side + "_p"]
	var lo := LO.duplicate()
	var hi := HI.duplicate()
	var n := 3
	if coude != null:
		n = 4
		lo[3] = float(ecart[0])
		hi[3] = float(ecart[1])
	var rng := RandomNumberGenerator.new()
	rng.seed = 7
	var best := INF
	var bestv := []
	var regle := func(c: int, val: float) -> void:
		pose.angles[ch[c]] = val * sg_p if c == 3 else val
	for essai in 41:
		if essai > 0 and best < 0.3:
			break
		var v := []
		for c in n:
			if essai == 0 and depart.size() >= n:
				v.append(clampf(depart[c], lo[c], hi[c]))
			else:
				v.append(rng.randf_range(lo[c], hi[c]))
			regle.call(c, v[c])
		var cur := _err(pose, side, tgt, coude)
		var pas := 16.0
		while pas > 0.05:
			var mieux := false
			for c in n:
				for sg in [-1.0, 1.0]:
					var nv: float = v[c] + sg * pas
					if nv < lo[c] or nv > hi[c]:
						continue
					regle.call(c, nv)
					var e := _err(pose, side, tgt, coude)
					if e < cur:
						cur = e
						v[c] = nv
						mieux = true
					else:
						regle.call(c, v[c])
			if not mieux:
				pas /= 2.0
		if cur < best:
			best = cur
			bestv = v.duplicate()
	for c in n:
		regle.call(c, snappedf(bestv[c], 0.1))
	return [ch, bestv, best, n, sg_p]


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
		var m: Dictionary = k._mains3d
		var pose: Dictionary = an.cles[i].pose.duplicate(true)
		var S := _p3(StickRig.solve(pose), "shoulderN")
		for side in ["N", "F"]:
			if not m.has(side):
				continue  # une seule main placée : l'autre garde les angles de la clé
			var d: Array = m[side]
			var cd = m.get("coude_dy")
			if cd is Array:
				cd = cd[0] if side == "N" else cd[1]
			coude_dx = m.get("coude_dx")
			if coude_dx is Array:
				coude_dx = coude_dx[0] if side == "N" else coude_dx[1]
			var r := _resout(pose, side, S + Vector3(d[0], d[1], d[2]), prec[side],
				cd, m.get("ecart", [0, 90]))
			prec[side] = r[1]
			for c in r[3]:
				var val: float = r[1][c] * (r[4] if c == 3 else 1.0)
				k.fixe[r[0][c]] = snappedf(val, 0.1)
			if k.has("vise"):
				k.vise.erase("arm" + side)
			if r[2] > 2.0:
				printerr("clé %d : main %s : écart pondéré %.1f (main ×4 + coudes)" % [int(k.f), side, r[2]])
		var sol := StickRig.solve(pose)
		var J: Dictionary = sol.joints
		var aN := _p3(sol, "handN") - _p3(sol, "elbowN")
		var aF := _p3(sol, "handF") - _p3(sol, "elbowF")
		# pente : avant-bras par rapport au sol (+ = main plus haute que le coude) ;
		# vers l'avant : angle de l'avant-bras avec l'axe gauche-droite, vu de dessus
		# (0 = pointé vers l'autre main, 90 = pointé devant)
		print("clé %d : mains à %.1f, pente %+.0f°/%+.0f°, vers l'avant %.0f°/%.0f°, écart %.0f/%.0f, traversées %s (marge %.1f)" % [int(k.f),
			_p3(sol, "handN").distance_to(_p3(sol, "handF")),
			rad_to_deg(atan2(aN.y, Vector2(aN.x, aN.z).length())),
			rad_to_deg(atan2(aF.y, Vector2(aF.x, aF.z).length())),
			rad_to_deg(atan2(absf(aN.x), absf(aN.z))), rad_to_deg(atan2(absf(aF.x), absf(aF.z))),
			pose.angles.get("armN_p", 0.0), pose.angles.get("armF_p", 0.0),
			AT._traversees(sol), AT._derniere_marge])
		# de profil (x, y) : ce que voit le joueur
		var pr := func(a: String, b: String) -> float:
			return Vector2(J[a].x - J[b].x, J[a].y - J[b].y).length()
		var Sh := _p3(sol, "shoulderN")
		var abd := func(sd: String) -> float:
			var e := _p3(sol, "elbow" + sd) - Sh
			return rad_to_deg(atan2(Vector2(e.x, e.z).length(), -e.y))
		print("   profil : mains %.1f, coudes %.1f, coudes x %.0f/%.0f y %.0f/%.0f ; bras/verticale %.0f°/%.0f°" % [
			pr.call("handN", "handF"), pr.call("elbowN", "elbowF"),
			J.elbowN.x - Sh.x, J.elbowF.x - Sh.x,
			J.elbowN.y - Sh.y, J.elbowF.y - Sh.y, abd.call("N"), abd.call("F")])
	var f := FileAccess.open(chemin, FileAccess.WRITE)
	f.store_string(JSON.stringify(data, " ", false) + "\n")
	quit()
