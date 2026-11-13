extends SceneTree
## Robot planificateur (vision parfaite) : vérifie que les tours générées sont franchissables.
## godot --headless --path . -s tests/bot_test.gd

const GRAV := 700.0
const JUMP_VX := 210.0
const JUMP_VY := -290.0
const TURN_VY := -205.0
const SLIDE := 14.0
const GRIP_TIME := 0.22
const MAX_FALL := 330.0
const HALF := Vector2(4, 6)
const CLING_OFF := 6.0
const WL := 32.0
const WR := 160.0
const DT := 1.0 / 60.0

var tower: Tower

func hit(p: Vector2, t: float) -> String:
	var box := Rect2(p - HALF, HALF * 2.0)
	for tr in tower.traps:
		if absf(tr.y - p.y) > 90.0:
			continue
		match int(tr.type):
			Tower.SPIKES:
				var x0: float = WL if tr.side < 0 else WR - Tower.SPIKE_DEPTH
				if Rect2(x0, tr.y - tr.h + 2.0, Tower.SPIKE_DEPTH, tr.h - 4.0).intersects(box):
					return "spikes"
			Tower.SAW:
				var c := Tower.saw_pos(tr, t)
				var q := Vector2(clampf(c.x, box.position.x, box.end.x), clampf(c.y, box.position.y, box.end.y))
				if q.distance_to(c) < 6.0:
					return "saw"
			Tower.LASER:
				if Tower.laser_state(tr, t) == 2 and absf(tr.y - p.y) < HALF.y + 2.0:
					return "laser"
	return ""

## simule un saut depuis (p, side) au temps t, demi-tour à la frame k (-1 = jamais).
## renvoie [ok, pos_atterrissage, side, t_atterrissage]
func sim_jump(p: Vector2, side: int, t: float, k: int) -> Array:
	var v := Vector2(JUMP_VX * -side, JUMP_VY)
	var f := 0
	while f < 200:
		f += 1
		t += DT
		if f == k:
			v.x = -v.x
			v.y = minf(v.y, TURN_VY)
		v.y = minf(v.y + GRAV * DT, MAX_FALL)
		p += v * DT
		var ns := 0
		if p.x <= WL + CLING_OFF:
			p.x = WL + CLING_OFF
			ns = -1
		elif p.x >= WR - CLING_OFF:
			p.x = WR - CLING_OFF
			ns = 1
		if p.y >= -HALF.y:
			return [false, p, 0, t]
		if hit(p, t) != "":
			return [false, p, 0, t]
		if ns != 0:
			# doit survivre accroché 0.3 s
			var q := p
			var tt := t
			for i in 18:
				tt += DT
				if i * DT > GRIP_TIME:
					q.y += SLIDE * DT
				if hit(q, tt) != "":
					return [false, p, 0, t]
			return [true, p, ns, t]
	return [false, p, 0, t]

func run(seed_v: int, max_t := 240.0) -> Dictionary:
	tower = Tower.new(seed_v)
	var p := Vector2(WL + CLING_OFF, -HALF.y)
	var side := -1
	var t := 0.0
	var grip := 0.0
	var tide := 70.0
	var best := 0
	var jumps := 0
	var turns := 0
	var plan_k := -2
	while t < max_t:
		tower.ensure(p.y - 400.0)
		# accroché : choisir
		var options := [-1, 10, 14, 18, 22, 28]
		var chosen := -2
		var bestup := 1e9
		for k in options:
			var r := sim_jump(p, side, t, k)
			if r[0]:
				# préfère le plus haut atterrissage
				if r[1].y < bestup:
					bestup = r[1].y
					chosen = k
		if chosen != -2:
			# exécuter le saut choisi (sans revérifier)
			var v := Vector2(JUMP_VX * -side, JUMP_VY)
			var f := 0
			jumps += 1
			if chosen > 0:
				turns += 1
			while true:
				f += 1
				t += DT
				if f == chosen:
					v.x = -v.x
					v.y = minf(v.y, TURN_VY)
				v.y = minf(v.y + GRAV * DT, MAX_FALL)
				p += v * DT
				var spd := minf(9.0 + t * 0.30, 30.0) + maxf(0.0, best - 150.0) * 0.02
				tide -= spd * DT
				var h := hit(p, t)
				if h != "":
					return {"best": best, "cause": h, "t": t, "jumps": jumps, "turns": turns}
				if p.y + HALF.y > tide + 5.0:
					return {"best": best, "cause": "tide", "t": t, "jumps": jumps, "turns": turns}
				if p.x <= WL + CLING_OFF:
					p.x = WL + CLING_OFF; side = -1; break
				if p.x >= WR - CLING_OFF:
					p.x = WR - CLING_OFF; side = 1; break
				if p.y >= -HALF.y:
					p.y = -HALF.y; break
			grip = 0.0
			best = maxi(best, tower.meters_at(p.y + HALF.y))
			if tide > p.y + 26.0 + 352.0 * 0.38:
				tide = p.y + 26.0 + 352.0 * 0.38
		else:
			# attendre
			t += DT
			grip += DT
			if grip > GRIP_TIME:
				p.y = minf(p.y + SLIDE * DT, -HALF.y)
			var spd2 := minf(9.0 + t * 0.30, 30.0) + maxf(0.0, best - 150.0) * 0.02
			tide -= spd2 * DT
			var h2 := hit(p, t)
			if h2 != "":
				return {"best": best, "cause": "wait-" + h2, "t": t, "jumps": jumps, "turns": turns}
			if p.y + HALF.y > tide + 5.0:
				return {"best": best, "cause": "tide(wait)", "t": t, "jumps": jumps, "turns": turns}
	return {"best": best, "cause": "timeout", "t": t, "jumps": jumps, "turns": turns}

func _initialize() -> void:
	var tot := 0
	for s in [20261113, 20261114, 20261115, 20261116, 20261117, 1, 2, 3, 4, 5, 6, 7]:
		var r := run(s)
		tot += int(r.best)
		print("%9d  %4d m  %-12s t=%5.1f  sauts=%d  demi-tours=%d" % [s, r.best, r.cause, r.t, r.jumps, r.turns])
	print("moyenne ", tot / 12)
	quit()
