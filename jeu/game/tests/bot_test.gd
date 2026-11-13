extends SceneTree
## Robot validateur : recherche en faisceau sur la vraie physique (Tower + Hz) pour vérifier
## que les tours assemblées sont franchissables. Signale les mètres où il reste bloqué.
## godot --headless --path . -s tests/bot_test.gd [-- --seeds=5 --goal=300]

const GRAV := 700.0
const GRAV_ELAN := 300.0
const GRAV_WATER := 300.0
const JUMP_VX := 210.0
const JUMP_VY := -290.0
const TURN_VY := -205.0
const SLIDE := 14.0
const GRIP_TIME := 0.22
const MAX_FALL := 330.0
const MAX_FALL_WATER := 150.0
const HIT := Vector2(3, 5)
const HALF_Y := 6.0
const CLING_OFF := 6.0
const DT := 1.0 / 120.0

const WAITS := [0.0, 0.12, 0.3, 0.55, 0.9, 1.4, 2.0]
const HOLDS := [false, true]
const VOLTES := [-1.0, 0.12, 0.25, 0.38, 0.5]
const BEAM := 8

var tower: Tower
var empty := {}

func _ents(y: float) -> Array:
	var out := []
	for e in tower.near(y - 160.0, y + 60.0):
		if String(e.kind) in Hz.LETHAL and e.kind != "rockfall":
			out.append(e)
	return out

func _dead(p: Vector2, t: float, ents: Array) -> bool:
	var box := Rect2(p - HIT, HIT * 2.0)
	for e in ents:
		if absf(float(e.y0) - p.y) > 140.0 and absf(float(e.y1) - p.y) > 140.0 and not (p.y > float(e.y0) and p.y < float(e.y1)):
			continue
		if Hz.test(e, t, empty, tower, box) == 2:
			return true
	return false

func _friable(side: int, y: float) -> bool:
	for e in tower.near(y - 1.0, y + 1.0):
		if e.kind == "friable" and int(e.side) == side and y >= float(e.y0) - 2.0 and y <= float(e.y1) + 2.0:
			return true
	return false

## Attente au mur puis bond. Renvoie {} si mort, sinon le nouvel état d'accroche.
func sim(s: Dictionary, wait: float, hold: bool, volte: float) -> Dictionary:
	var p: Vector2 = s.p
	var side: int = s.side
	var t: float = s.t
	var ents := _ents(p.y)
	if wait > 0.3 and _friable(side, p.y):
		return {}
	# attente
	var w := 0.0
	var grip := 0.0
	while w < wait:
		w += DT
		t += DT
		grip += DT
		if not s.floor and grip > GRIP_TIME:
			p.y = minf(p.y + SLIDE * DT, -HALF_Y)
		if _dead(p, t, ents):
			return {}
	# bond
	var v := Vector2(JUMP_VX * -side, JUMP_VY)
	var air := 0.0
	var turned := false
	while air < 2.5:
		air += DT
		t += DT
		if not turned and volte > 0.0 and air >= volte:
			turned = true
			v.x = -v.x
			v.y = minf(v.y, TURN_VY)
		var water := tower.is_water(p.y)
		var g := GRAV_WATER if water else GRAV
		if hold and air >= 0.10 and air <= 0.28 and v.y < 0.0:
			g = minf(g, GRAV_ELAN)
		v.y = minf(v.y + g * DT, MAX_FALL_WATER if water else MAX_FALL)
		p += v * DT
		if _dead(p, t, ents):
			return {}
		if p.y >= -HALF_Y:
			return {}  # retour au sol : inutile
		var fl := tower.wall_face(-1, p.y) + CLING_OFF
		var fr := tower.wall_face(1, p.y) - CLING_OFF
		if p.x <= fl and v.x < 0.0:
			p.x = fl
			return {"p": p, "side": -1, "t": t, "floor": false}
		if p.x >= fr and v.x > 0.0:
			p.x = fr
			return {"p": p, "side": 1, "t": t, "floor": false}
	return {}

func run_seed(seed_v: int, goal: int) -> Dictionary:
	tower = Tower.new(seed_v)
	tower.ensure(-goal * 16.0 - 400.0)
	var beam := [{"p": Vector2(Tower.WALL_L + CLING_OFF, -HALF_Y), "side": -1, "t": 0.0, "floor": true}]
	var best_y := 0.0
	var steps := 0
	while not beam.is_empty() and steps < 600:
		steps += 1
		var nxt := {}
		for s in beam:
			for w in WAITS:
				for h in HOLDS:
					for vt in VOLTES:
						var r := sim(s, w, h, vt)
						if r.is_empty():
							continue
						if r.p.y > s.p.y + 32.0:
							continue
						var key := "%d_%d" % [r.side, int(r.p.y / 6.0)]
						if not nxt.has(key) or nxt[key].t > r.t:
							nxt[key] = r
		var arr := nxt.values()
		arr.sort_custom(func(a, b): return a.p.y < b.p.y)
		beam = arr.slice(0, BEAM)
		if not beam.is_empty():
			best_y = minf(best_y, beam[0].p.y)
			if Tower.meters_at(best_y) >= goal:
				break
	var m := Tower.meters_at(best_y)
	var chunk := ""
	for c in tower.placed:
		if m >= int(c.m0) and m < int(c.m0) + int(c.h):
			chunk = "%s (m0=%d)" % [c.id, c.m0]
	return {"m": m, "chunk": chunk, "steps": steps}

func _initialize() -> void:
	var root := "res://chunks"
	for a in OS.get_cmdline_user_args():
		if a.begins_with("--root="):
			root = a.substr(7)
	ChunkLib.load_all(root)
	for er in ChunkLib.errors:
		print("CHUNK : ", er)
	var seeds := 5
	var goal := 300
	for a in OS.get_cmdline_user_args():
		if a.begins_with("--seeds="):
			seeds = int(a.substr(8))
		elif a.begins_with("--goal="):
			goal = int(a.substr(7))
	var fails := 0
	for i in seeds:
		var sd := 1000 + i * 7919
		var t0 := Time.get_ticks_msec()
		var r := run_seed(sd, goal)
		var ok: bool = r.m >= goal
		if not ok:
			fails += 1
		print("graine %d : %s %d m en %d bonds (%d ms)%s" % [sd, "OK" if ok else "BLOQUÉ à", r.m, r.steps,
			Time.get_ticks_msec() - t0, "" if ok else " — chunk " + r.chunk])
	print("RÉSULTAT : %d/%d tours franchissables jusqu'à %d m" % [seeds - fails, seeds, goal])
	quit(1 if fails > 0 else 0)
