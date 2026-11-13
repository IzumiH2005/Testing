extends Node2D
## Monde de jeu : simulation de la tour, du héros, des dangers, de la marée et des échos.
## Une « ascension » = plusieurs vies sur la même tour (même graine).
## Le dessin est délégué à world_draw.gd (nœud enfant `view`).

signal life_ended(info: Dictionary)
signal shard_taken(total: int)
signal height_changed(m: int)
signal first_jump
signal air_turn_used
signal combo_changed(n: int)
signal power_taken(kind: String)
signal altar_reached(biome: String, m: int)
signal boss_event(kind: String, n: int)

const TILE := 16
const WL := Tower.WALL_L
const WR := Tower.WALL_R

# --- physique (GDD 2.3 ; constantes à arbitrer par la critique de design)
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
const ELAN_DEAD := 0.10
const ELAN_END := 0.28
const COYOTE := 0.10
const BUFFER := 0.10
const TAP_LOCK := 0.05  ## anti double-tap (critique design)
const HALF := Vector2(4, 6)          # boîte visuelle / ramassage 8 × 12
const HIT := Vector2(3, 5)           # boîte létale 6 × 10
const CLING_OFF := 6.0
const MAX_ECHOES := 3
const RHYTHM := 0.30
const SLOWMO := 0.08

enum S { DEMO, READY, PLAY, DYING, WAIT }

var tower: Tower
var state := S.DEMO
var t_life := 0.0
var t_global := 0.0
var pos := Vector2.ZERO
var vel := Vector2.ZERO
var side := -1
var grip := 0.0
var cling_t := 0.0
var air_t := 0.0
var held := false
var coyote_t := 0.0
var buffer_t := 0.0
var last_press := -1.0
var turns := 0
var turn_anim := 0.0
var on_floor := true
var facing := 1
var in_water := false
var life_best := 0
var ascension_best := 0
var tide_y := 96.0
var tide_on := false
var cam_y := 0.0
var shake := 0.0
var hitstop := 0.0
var slowmo := 0.0
var combo := 0

# --- pouvoirs
var burins := 0
var burins_taken := 0
var invul := 0.0
var plume_t := 0.0
var calm_t := 0.0

# --- état persistant de l'ascension
var neutral := {}          # id d'entité -> temps figé de la gravure
var engraving := {}        # id -> temps restant de l'animation de gravure
var taken := {}            # id d'éclat -> true
var used := {}             # id d'entité ramassée (pouvoir) -> true
var altars_on := {}        # id d'autel -> true
var spawn_altar := -1      # id de l'autel de reprise (-1 = sol)
var bosses_done := {}      # id d'arène -> true
var shards_run := 0
var graves: Array = []
var rec := PackedFloat32Array()
var recordings: Array = []
var record_line := 0
var particles: Array = []
var floaters: Array = []   # textes flottants {p, txt, col, t, life}

# --- état par vie
var st := {}               # éboulis déclenchés : id -> t
var fr_start := {}         # plaque friable : id -> t de première prise
var fr_touch := {}         # plaque friable : id -> dernier contact
var frole_done := {}
var cyan_touch := {}
var boss := {}             # arène active (entité) ou {}
var boss_t := 0.0
var boss_stun := 0.0
var boss_hits := 0
var boss_runes: Array = []
var wave_y := 0.0
var wave_t := -1.0

var player: Sprite2D
var camera: Camera2D
var view: Node2D
var skin_mat: ShaderMaterial
var echo_nodes: Array = []

func _ready() -> void:
	view = preload("res://scripts/world_draw.gd").new()
	view.w = self
	add_child(view)
	camera = Camera2D.new()
	camera.anchor_mode = Camera2D.ANCHOR_MODE_FIXED_TOP_LEFT
	add_child(camera)
	camera.make_current()
	player = Sprite2D.new()
	player.centered = false
	player.texture = A.tex("sprites/player")
	if player.texture:
		player.hframes = 5
	skin_mat = ShaderMaterial.new()
	skin_mat.shader = load("res://shaders/skin.gdshader")
	player.material = skin_mat
	player.z_index = 5
	add_child(player)
	for i in MAX_ECHOES:
		var e := Sprite2D.new()
		e.centered = false
		e.texture = player.texture
		if e.texture:
			e.hframes = 5
		var m := ShaderMaterial.new()
		m.shader = load("res://shaders/echo.gdshader")
		e.material = m
		e.z_index = 4
		e.visible = false
		add_child(e)
		echo_nodes.append(e)
	setup_demo(Game.daily_seed())

func apply_skin() -> void:
	var s: Dictionary = Game.current_skin()
	skin_mat.set_shader_parameter("dst0", Color(s.c[0]))
	skin_mat.set_shader_parameter("dst1", Color(s.c[1]))
	skin_mat.set_shader_parameter("dst2", Color(s.c[2]))

func _vh() -> float:
	return get_viewport_rect().size.y

# ------------------------------------------------------------------ cycle de vie

func setup_demo(seed_v: int) -> void:
	tower = Tower.new(seed_v)
	state = S.DEMO
	player.visible = false
	for e in echo_nodes:
		e.visible = false
	cam_y = -_vh() + 40.0
	tide_y = 99999.0
	neutral.clear()
	graves.clear()
	taken.clear()
	altars_on.clear()

func start_ascension(seed_v: int, record_m: int) -> void:
	tower = Tower.new(seed_v)
	neutral.clear()
	engraving.clear()
	taken.clear()
	used.clear()
	altars_on.clear()
	bosses_done.clear()
	graves.clear()
	recordings.clear()
	floaters.clear()
	spawn_altar = -1
	shards_run = 0
	ascension_best = 0
	burins = 0
	burins_taken = 0
	record_line = record_m
	apply_skin()
	start_life()

func spawn_pos() -> Vector2:
	if spawn_altar >= 0:
		return Vector2(WL + CLING_OFF, float(tower.ents[spawn_altar].y))
	return Vector2(WL + CLING_OFF, -HALF.y)

func start_life() -> void:
	pos = spawn_pos()
	vel = Vector2.ZERO
	side = -1
	facing = 1
	on_floor = spawn_altar < 0
	grip = 0.0
	cling_t = 0.0
	air_t = 0.0
	held = false
	coyote_t = 0.0
	buffer_t = 0.0
	turns = 0
	t_life = 0.0
	life_best = Tower.meters_at(pos.y + HALF.y)
	tide_y = pos.y + 96.0
	tide_on = false
	combo = 0
	invul = 0.0
	plume_t = 0.0
	calm_t = 0.0
	slowmo = 0.0
	st.clear()
	fr_start.clear()
	fr_touch.clear()
	frole_done.clear()
	cyan_touch.clear()
	boss = {}
	wave_t = -1.0
	rec = PackedFloat32Array()
	tower.ensure(pos.y - 600.0)
	cam_y = _target_cam()
	state = S.READY
	player.visible = true
	skin_mat.set_shader_parameter("flash", 0.0)
	var n: int = mini(recordings.size(), MAX_ECHOES)
	for i in MAX_ECHOES:
		echo_nodes[i].visible = i < n
	_place_sprite(player, pos, 0, false)
	combo_changed.emit(0)

# ------------------------------------------------------------------ entrées

## Doigt posé.
func press() -> void:
	match state:
		S.READY:
			state = S.PLAY
			tide_on = true
			held = true
			_jump()
			first_jump.emit()
		S.PLAY:
			held = true
			if t_global - last_press < TAP_LOCK:
				return
			last_press = t_global
			if side != 0 or coyote_t > 0.0:
				_jump()
			elif _time_to_wall() < BUFFER:
				buffer_t = BUFFER
			elif turns > 0:
				_volte()
			else:
				buffer_t = BUFFER

## Doigt levé (fin de l'Élan).
func release() -> void:
	held = false

## Compatibilité : un tap = appui + relâché immédiat.
func tap() -> void:
	press()
	release()

func _time_to_wall() -> float:
	if absf(vel.x) < 1.0:
		return 99.0
	var d: float
	if vel.x < 0.0:
		d = pos.x - (tower.wall_face(-1, pos.y) + CLING_OFF)
	else:
		d = (tower.wall_face(1, pos.y) - CLING_OFF) - pos.x
	return maxf(0.0, d) / absf(vel.x)

func _jump() -> void:
	var dir := -side if side != 0 else (1 if pos.x < 96.0 else -1)
	if side != 0 and not on_floor:
		if cling_t < RHYTHM:
			combo += 1
			if combo == 10 or combo == 20 or combo == 30:
				var bonus := combo / 5
				_add_shards(bonus, pos + Vector2(0, -12))
				_floater(pos + Vector2(0, -18), "RYTHME x%d" % combo, A.P.G)
				Sfx.play("record")
		else:
			combo = 0
		combo_changed.emit(combo)
	vel = Vector2(JUMP_VX * dir, JUMP_VY)
	facing = dir
	side = 0
	on_floor = false
	air_t = 0.0
	coyote_t = 0.0
	buffer_t = 0.0
	turns = 2 if plume_t > 0.0 else 1
	cyan_touch.clear()
	Sfx.play("jump")
	_burst(pos + Vector2(-dir * 5, 4), 4, A.P.p, 30.0)

func _volte() -> void:
	turns -= 1
	vel.x = -vel.x
	vel.y = minf(vel.y, TURN_VY)
	facing = int(signf(vel.x))
	turn_anim = 0.22
	Sfx.play("turn")
	_burst(pos, 5, A.P.p, 40.0)
	air_turn_used.emit()

# ------------------------------------------------------------------ boucle

func _physics_process(dt_real: float) -> void:
	t_global += dt_real
	_update_particles(dt_real)
	for id in engraving.keys():
		engraving[id] -= dt_real
		if engraving[id] <= 0.0:
			engraving.erase(id)
	if hitstop > 0.0:
		hitstop -= dt_real
		view.queue_redraw()
		return
	var dt := dt_real
	if slowmo > 0.0:
		slowmo -= dt_real
		dt *= 0.5
	shake = maxf(0.0, shake - dt_real * 30.0)
	match state:
		S.DEMO:
			cam_y -= 14.0 * dt
			tower.ensure(cam_y - 200.0)
			t_life += dt
		S.READY:
			tower.ensure(cam_y - 200.0)
		S.PLAY:
			t_life += dt
			invul = maxf(0.0, invul - dt)
			plume_t = maxf(0.0, plume_t - dt)
			calm_t = maxf(0.0, calm_t - dt)
			_step_player(dt)
			_step_boss(dt)
			_step_tide(dt)
			_check_hits()
			_record()
			_step_echoes()
			cam_y = lerpf(cam_y, _target_cam(), clampf(dt * 6.0, 0.0, 1.0))
			tower.ensure(cam_y - 200.0)
		S.DYING, S.WAIT:
			_step_echoes()
	camera.position = Vector2(0, round(cam_y)) + Vector2(randf_range(-shake, shake), randf_range(-shake, shake)).round()
	view.queue_redraw()

func _target_cam() -> float:
	var vh := _vh()
	return minf(pos.y - vh * 0.62, 56.0 - vh)

# ------------------------------------------------------------------ héros

func _friable_at(s: int, y: float) -> Dictionary:
	for e in tower.near(y - 1.0, y + 1.0):
		if e.kind == "friable" and int(e.side) == s and y >= float(e.y0) - 2.0 and y <= float(e.y1) + 2.0:
			return e
	return {}

func _friable_broken(e: Dictionary) -> bool:
	if neutral.has(e.id) or not fr_start.has(e.id):
		return false
	var u: float = t_life - float(fr_start[e.id])
	return u >= 0.35 and u < 3.35

func _can_grip(s: int, y: float) -> bool:
	var f := _friable_at(s, y)
	return f.is_empty() or not _friable_broken(f)

func _step_player(dt: float) -> void:
	turn_anim = maxf(0.0, turn_anim - dt)
	coyote_t = maxf(0.0, coyote_t - dt)
	buffer_t = maxf(0.0, buffer_t - dt)
	in_water = tower.is_water(pos.y)
	if side != 0:
		cling_t += dt
		var face := tower.wall_face(side, pos.y)
		pos.x = face + CLING_OFF if side < 0 else face - CLING_OFF
		var f := _friable_at(side, pos.y)
		if not f.is_empty() and not neutral.has(f.id):
			fr_touch[f.id] = t_life
			if not fr_start.has(f.id) or t_life - float(fr_start[f.id]) >= 3.35:
				fr_start[f.id] = t_life
				Sfx.play("land")
			if _friable_broken(f):
				_burst(pos + Vector2(side * 5, 0), 6, A.P.s, 30.0)
				_detach()
				return
		if on_floor:
			vel = Vector2.ZERO
		else:
			grip += dt
			vel.y = SLIDE if grip > GRIP_TIME else 0.0
			pos.y += vel.y * dt
			if pos.y >= -HALF.y:
				pos.y = -HALF.y
				on_floor = true
	else:
		air_t += dt
		var g := GRAV_WATER if in_water else GRAV
		if held and air_t >= ELAN_DEAD and air_t <= ELAN_END and vel.y < 0.0:
			g = minf(g, GRAV_ELAN)
		var mf := MAX_FALL_WATER if in_water else MAX_FALL
		vel.y = minf(vel.y + g * dt, mf)
		pos += vel * dt
		var fl := tower.wall_face(-1, pos.y)
		var fr := tower.wall_face(1, pos.y)
		if pos.x <= fl + CLING_OFF and vel.x <= 0.0:
			pos.x = fl + CLING_OFF
			if _can_grip(-1, pos.y):
				_land(-1)
			else:
				vel.x = 0.0
		elif pos.x >= fr - CLING_OFF and vel.x >= 0.0:
			pos.x = fr - CLING_OFF
			if _can_grip(1, pos.y):
				_land(1)
			else:
				vel.x = 0.0
		if pos.y >= -HALF.y:
			pos.y = -HALF.y
			vel.y = 0.0
			on_floor = true
			if side == 0:
				side = -1 if pos.x < 96.0 else 1
	var m := Tower.meters_at(pos.y + HALF.y)
	if m > life_best:
		life_best = m
		if m > ascension_best:
			ascension_best = m
		height_changed.emit(m)
	_place_sprite(player, pos, _frame(), facing < 0)

func _detach() -> void:
	side = 0
	vel = Vector2.ZERO
	coyote_t = COYOTE
	air_t = 1.0
	turns = 0

func _land(s: int) -> void:
	side = s
	vel = Vector2.ZERO
	grip = 0.0
	cling_t = 0.0
	turns = 0
	facing = -s
	Sfx.play("land")
	_burst(pos + Vector2(s * 5, 0), 3, A.P.l, 25.0)
	if buffer_t > 0.0:
		_jump()

func _frame() -> int:
	if side != 0:
		return 1 if (grip > GRIP_TIME and not on_floor) else 0
	if turn_anim > 0.0:
		return 4
	return 2 if vel.y < 0.0 else 3

func _place_sprite(sp: Sprite2D, p: Vector2, f: int, flip: bool) -> void:
	if sp.texture:
		sp.frame = clampi(f, 0, 4)
	sp.flip_h = flip
	var x0 := p.x - CLING_OFF if not flip else p.x + CLING_OFF - 16.0
	if f >= 2:
		x0 = p.x - 8.0
	sp.position = Vector2(round(x0), round(p.y - 10.0))
	if sp == player:
		sp.modulate.a = 0.5 if (invul > 0.0 and int(t_global * 20.0) % 2 == 0) else 1.0

# ------------------------------------------------------------------ marée

func _step_tide(dt: float) -> void:
	if not tide_on:
		return
	var spd := minf(10.0 + 0.35 * t_life, tower.tide_cap(pos.y))
	if calm_t <= 0.0:
		tide_y -= spd * dt
	if not boss.is_empty():
		tide_y = maxf(tide_y, float(boss.y1) + 12.0)
	var bottom := cam_y + _vh() + 26.0
	if tide_y > bottom:
		tide_y = bottom

# ------------------------------------------------------------------ boss (règles communes GDD 7.1)

func _step_boss(dt: float) -> void:
	if boss.is_empty():
		for e in tower.near(pos.y - 8.0, pos.y + 8.0):
			if e.kind == "arena" and not bosses_done.has(e.id) and pos.y < float(e.y1) - 24.0 and pos.y > float(e.y0):
				_start_boss(e)
				break
		return
	boss_t += dt
	boss_stun = maxf(0.0, boss_stun - dt)
	# onde-laser toutes les 3 s : préavis 0,6 s puis descente de 40 px en 0,5 s
	if boss_stun <= 0.0:
		if wave_t < 0.0 and fmod(boss_t, 3.0) < dt:
			wave_t = 0.0
			wave_y = pos.y - 26.0
		if wave_t >= 0.0:
			wave_t += dt
			if wave_t > 1.1:
				wave_t = -1.0
	else:
		wave_t = -1.0

func _start_boss(e: Dictionary) -> void:
	boss = e
	boss_t = 0.0
	boss_stun = 0.0
	boss_hits = 0
	boss_runes.clear()
	for id in e.runes:
		boss_runes.append(tower.ents[id])
	if boss_runes.size() < 3:
		boss_runes.clear()
		var sides := [-1, 1, -1]
		var offs := [4, 10, 16]
		for k in 3:
			var y: float = float(e.y1) - offs[k] * TILE - 8.0
			boss_runes.append({"id": -10 - k, "kind": "rune", "side": sides[k], "y": y, "order": k})
	boss_event.emit("start", 0)
	_floater(Vector2(96, pos.y - 30), "LE SONNEUR", A.P.G)
	shake = 3.0

func bell_pos() -> Vector2:
	var mid: float = (float(boss.y0) + float(boss.y1)) * 0.5
	var th := deg_to_rad(55.0) * sin(TAU * boss_t / 2.6)
	return Vector2(96.0, mid - 56.0) + Vector2(sin(th), cos(th)) * 44.0

func wave_state() -> Vector2:
	## (y du faisceau, 0 préavis / 1 létal)
	if wave_t < 0.0:
		return Vector2(0, -1)
	if wave_t < 0.6:
		return Vector2(wave_y, 0)
	return Vector2(wave_y + 40.0 * clampf((wave_t - 0.6) / 0.5, 0.0, 1.0), 1)

func _boss_hits(box: Rect2) -> bool:
	if boss.is_empty() or boss_stun > 0.0:
		return false
	var b := bell_pos()
	var q := Vector2(clampf(b.x, box.position.x, box.end.x), clampf(b.y, box.position.y, box.end.y))
	if q.distance_to(b) < 20.0:
		return true
	var w := wave_state()
	return w.y == 1 and absf(w.x - pos.y) < 4.0

func _boss_rune() -> void:
	if boss.is_empty() or boss_hits >= boss_runes.size():
		return
	var r: Dictionary = boss_runes[boss_hits]
	if side == int(r.side) and absf(float(r.y) - pos.y) < 12.0:
		boss_hits += 1
		boss_stun = 1.0
		wave_t = -1.0
		shake = 4.0
		Sfx.play("record")
		Game.vibrate(40)
		_burst(Vector2(WL + 8 if int(r.side) < 0 else WR - 8, float(r.y)), 18, A.P.G, 70.0)
		boss_event.emit("rune", boss_hits)
		if boss_hits >= boss_runes.size():
			bosses_done[boss.id] = true
			_burst(bell_pos(), 40, A.P.G, 110.0)
			_add_shards(20, bell_pos())
			_floater(bell_pos(), "+20", A.P.G)
			boss_event.emit("won", 3)
			boss = {}

# ------------------------------------------------------------------ collisions

func _add_shards(n: int, at: Vector2) -> void:
	shards_run += n
	shard_taken.emit(shards_run)
	particles.append({"anim": "shard_pop", "p": at, "t": 0.0, "life": 0.32})

func _floater(p: Vector2, txt: String, col: Color) -> void:
	floaters.append({"p": p, "txt": txt, "col": col, "t": 0.0, "life": 1.0})

func _check_hits() -> void:
	var pick := Rect2(pos - HALF, HALF * 2.0)
	var box := Rect2(pos - HIT, HIT * 2.0)
	# éclats
	for s in tower.shards:
		if taken.has(s.id) or absf(s.pos.y - pos.y) > 12.0:
			continue
		var r := 7.0 if s.big else 5.0
		if pick.grow(r - 4.0).has_point(s.pos):
			taken[s.id] = true
			var v := 5 if s.big else 1
			Sfx.play("shard")
			_burst(s.pos, 10 if s.big else 6, A.P.G, 50.0)
			_add_shards(v, s.pos)
			if s.big:
				_floater(s.pos, "+5", A.P.G)
	# marée
	if pos.y + HALF.y > tide_y + 5.0:
		_die({"kind": "tide"})
		return
	_boss_rune()
	if invul <= 0.0 and _boss_hits(box):
		_die({"kind": "boss"})
		return
	for e in tower.near(pos.y - 120.0, pos.y + 120.0):
		match String(e.kind):
			"power":
				if not used.has(e.id) and pick.grow(4.0).has_point(e.pos):
					_take_power(e)
			"altar":
				if not altars_on.has(e.id) and pos.y < float(e.y) + 6.0:
					_activate_altar(e)
			"rockfall":
				if not st.has(e.id) and not neutral.has(e.id) and pos.y > float(e.y) and pos.y - float(e.y) <= 96.0:
					st[e.id] = t_life
		if not (String(e.kind) in Hz.LETHAL):
			continue
		if neutral.has(e.id):
			# un élément gravé touché en l'air recharge la volte
			if side == 0 and turns == 0 and not cyan_touch.has(e.id):
				if Hz.test(e, float(neutral[e.id]), st, tower, pick) >= 1:
					cyan_touch[e.id] = true
					turns = 1
					_burst(pos, 8, A.P.c, 40.0)
					_floater(pos + Vector2(0, -12), "VOLTE", A.P.c)
			continue
		var res := Hz.test(e, t_life, st, tower, box)
		if res == 2:
			if invul > 0.0:
				continue
			if burins > 0:
				burins -= 1
				invul = 0.5
				_engrave(e, t_life)
				_floater(pos + Vector2(0, -12), "BURIN", A.P.c)
				power_taken.emit("burin_used")
				continue
			_die({"kind": "trap", "trap": e})
			return
		elif res == 1 and not frole_done.has(e.id) and invul <= 0.0:
			frole_done[e.id] = true
			slowmo = SLOWMO
			Sfx.play("shard")
			_add_shards(1, pos)
			_floater(pos + Vector2(0, -12), "FRÔLÉ +1", A.P.y)

func _take_power(e: Dictionary) -> void:
	used[e.id] = true
	Sfx.play("reward")
	_burst(e.pos, 14, A.P.e, 60.0)
	match String(e.power):
		"burin":
			if burins_taken < 2:
				burins_taken += 1
				burins += 1
			_floater(e.pos, "BURIN", A.P.c)
		"plume":
			plume_t = 12.0
			if side == 0:
				turns = maxi(turns, 2)
			_floater(e.pos, "PLUME", A.P.p)
		"accalmie":
			calm_t = 6.0
			tide_y += 48.0
			_floater(e.pos, "ACCALMIE", A.P.U)
	power_taken.emit(String(e.power))

func _activate_altar(e: Dictionary) -> void:
	altars_on[e.id] = true
	if int(e.m) >= 20:
		spawn_altar = e.id
		recordings.clear()  # les échos ne valent que depuis le même point de départ
		for en in echo_nodes:
			en.visible = false
	tide_y += 96.0
	Sfx.play("record")
	Game.vibrate(30)
	_burst(Vector2(float(e.x), float(e.y)), 24, A.P.a, 70.0)
	_floater(Vector2(96, float(e.y) - 20.0), "AUTEL", A.P.a)
	altar_reached.emit(String(e.biome), int(e.m))

func _engrave(e: Dictionary, at_t: float) -> void:
	neutral[e.id] = at_t
	engraving[e.id] = 0.7
	Sfx.play("engrave")
	_burst(Hz.center(e, at_t, st, tower), 16, A.P.e, 60.0)

func _die(info: Dictionary) -> void:
	state = S.DYING
	hitstop = 0.10
	shake = 4.0
	Sfx.play("die")
	Game.vibrate(70)
	graves.append(pos)
	recordings.append(rec)
	info["height"] = life_best
	info["pos"] = pos
	if combo > 0:
		combo = 0
		combo_changed.emit(0)
	skin_mat.set_shader_parameter("flash", 1.0)
	particles.append({"anim": "death", "p": pos, "t": 0.0, "life": 0.6})
	_burst(pos, 14, A.P.c, 70.0)
	var t_death := t_life
	var accomplices := []
	for id in fr_touch:
		if t_death - float(fr_touch[id]) < 1.0:
			accomplices.append(tower.ents[id])
	var tw := create_tween()
	tw.tween_interval(0.18)
	tw.tween_callback(func(): player.visible = false)
	tw.tween_interval(0.45)
	if info.kind == "trap":
		var e: Dictionary = info.trap
		info["trap_kind"] = e.kind
		tw.tween_callback(func():
			_engrave(e, t_death)
			for a in accomplices:
				_engrave(a, t_death))
		tw.tween_interval(0.7)
	tw.tween_callback(func():
		state = S.WAIT
		life_ended.emit(info))

## Recentre la caméra sur une position (pour montrer le piège gravé).
func focus(y: float) -> void:
	cam_y = minf(y - _vh() * 0.5, 56.0 - _vh())

# ------------------------------------------------------------------ échos

func _record() -> void:
	if Engine.get_physics_frames() % 2 == 0:
		rec.append(pos.x)
		rec.append(pos.y)
		rec.append(float(_frame() + (8 if facing < 0 else 0)))

func _step_echoes() -> void:
	var n: int = mini(recordings.size(), MAX_ECHOES)
	var idx := int(t_life * 30.0)
	for i in n:
		var r: PackedFloat32Array = recordings[recordings.size() - 1 - i]
		var e: Sprite2D = echo_nodes[i]
		var count := r.size() / 3
		if idx < count:
			var f := int(r[idx * 3 + 2])
			_place_sprite(e, Vector2(r[idx * 3], r[idx * 3 + 1]), f % 8, f >= 8)
			e.material.set_shader_parameter("alpha", 0.55 - 0.12 * i)
			e.visible = state != S.READY or idx == 0
		else:
			e.visible = false

# ------------------------------------------------------------------ particules

func _burst(p: Vector2, n: int, col: Color, spd: float) -> void:
	for i in n:
		var a := randf() * TAU
		var v := Vector2(cos(a), sin(a)) * randf_range(spd * 0.3, spd)
		particles.append({"p": p, "v": v, "t": 0.0, "life": randf_range(0.25, 0.55), "c": col})

func _update_particles(dt: float) -> void:
	var keep := []
	for pt in particles:
		pt.t += dt
		if pt.t < pt.life:
			if pt.has("v"):
				pt.p += pt.v * dt
				pt.v *= 0.9
				pt.v.y += 40.0 * dt
			keep.append(pt)
	particles = keep
	var kf := []
	for f in floaters:
		f.t += dt
		f.p.y -= 18.0 * dt
		if f.t < f.life:
			kf.append(f)
	floaters = kf
