extends Node2D
## Monde de jeu : tour, héros, pièges, marée, échos. Une « ascension » = plusieurs vies sur la même tour.

signal life_ended(info: Dictionary)
signal shard_taken(total: int)
signal height_changed(m: int)
signal first_jump
signal air_turn_used

const TILE := 16
const WL := Tower.WALL_L
const WR := Tower.WALL_R
const GRAV := 700.0
const JUMP_VX := 210.0
const JUMP_VY := -290.0
const TURN_VY := -205.0
const SLIDE := 14.0
const GRIP_TIME := 0.22
const MAX_FALL := 330.0
const HALF := Vector2(4, 6)          # demi-boîte de collision du héros
const CLING_OFF := 6.0               # centre du héros depuis la face du mur
const MAX_ECHOES := 3

enum S { DEMO, READY, PLAY, DYING, WAIT }

var tower: Tower
var state := S.DEMO
var t_life := 0.0          # temps de la vie en cours (anime les pièges)
var t_global := 0.0        # temps réel (animations décoratives)
var pos := Vector2.ZERO
var vel := Vector2.ZERO
var side := -1             # mur auquel on est accroché (-1 gauche, 1 droit), 0 en l'air
var grip := 0.0
var turn_ok := false
var turn_anim := 0.0
var on_floor := true
var facing := 1
var life_best := 0
var ascension_best := 0
var tide_y := 80.0
var tide_on := false
var cam_y := 0.0
var shake := 0.0
var hitstop := 0.0

var neutral := {}          # id de piège -> true (gravé par un écho)
var engraving := {}        # id -> temps restant de l'animation de gravure
var taken := {}            # id d'éclat -> true (ramassé pendant l'ascension)
var shards_run := 0
var graves: Array = []     # positions des morts
var rec := PackedFloat32Array()
var recordings: Array = [] # enregistrements des vies précédentes
var echo_nodes: Array = []
var record_line := 0       # record à battre (m)
var particles: Array = []

var player: Sprite2D
var camera: Camera2D
var view_h := 352.0
var skin_mat: ShaderMaterial

func _ready() -> void:
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

func start_ascension(seed_v: int, record_m: int) -> void:
	tower = Tower.new(seed_v)
	neutral.clear()
	engraving.clear()
	taken.clear()
	graves.clear()
	recordings.clear()
	shards_run = 0
	ascension_best = 0
	record_line = record_m
	apply_skin()
	start_life()

func start_life() -> void:
	pos = Vector2(WL + CLING_OFF, -HALF.y)
	vel = Vector2.ZERO
	side = -1
	facing = 1
	on_floor = true
	grip = 0.0
	turn_ok = false
	t_life = 0.0
	life_best = 0
	tide_y = 70.0
	tide_on = false
	rec = PackedFloat32Array()
	cam_y = _target_cam()
	state = S.READY
	player.visible = true
	skin_mat.set_shader_parameter("flash", 0.0)
	var n: int = mini(recordings.size(), MAX_ECHOES)
	for i in MAX_ECHOES:
		echo_nodes[i].visible = i < n
	_update_player_sprite(0)

func _vh() -> float:
	return get_viewport_rect().size.y

func tap() -> void:
	match state:
		S.READY:
			state = S.PLAY
			tide_on = true
			_jump()
			first_jump.emit()
		S.PLAY:
			if side != 0:
				_jump()
			elif turn_ok:
				turn_ok = false
				vel.x = -vel.x
				vel.y = minf(vel.y, TURN_VY)
				facing = int(signf(vel.x))
				turn_anim = 0.22
				Sfx.play("turn")
				_burst(pos, 5, A.P.p, 40.0)
				air_turn_used.emit()

func _jump() -> void:
	var dir := -side if side != 0 else 1
	vel = Vector2(JUMP_VX * dir, JUMP_VY)
	facing = dir
	side = 0
	on_floor = false
	turn_ok = true
	Sfx.play("jump")
	_burst(pos + Vector2(-dir * 5, 4), 4, A.P.p, 30.0)

# ------------------------------------------------------------------ simulation

func _physics_process(dt: float) -> void:
	t_global += dt
	_update_particles(dt)
	for id in engraving.keys():
		engraving[id] -= dt
		if engraving[id] <= 0.0:
			engraving.erase(id)
	if hitstop > 0.0:
		hitstop -= dt
		queue_redraw()
		return
	shake = maxf(0.0, shake - dt * 30.0)
	match state:
		S.DEMO:
			cam_y -= 14.0 * dt
			tower.ensure(cam_y - 200.0)
		S.READY:
			t_life += dt * 0.0
			tower.ensure(cam_y - 200.0)
		S.PLAY:
			t_life += dt
			_step_player(dt)
			_step_tide(dt)
			_check_hits()
			_record()
			_step_echoes()
			cam_y = lerpf(cam_y, _target_cam(), clampf(dt * 6.0, 0.0, 1.0))
			tower.ensure(cam_y - 200.0)
		S.DYING, S.WAIT:
			_step_echoes()
	camera.position = Vector2(0, round(cam_y)) + Vector2(randf_range(-shake, shake), randf_range(-shake, shake)).round()
	queue_redraw()

func _target_cam() -> float:
	var vh := _vh()
	var c := pos.y - vh * 0.62
	return minf(c, 56.0 - vh)

func _step_player(dt: float) -> void:
	turn_anim = maxf(0.0, turn_anim - dt)
	if side != 0:
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
		vel.y = minf(vel.y + GRAV * dt, MAX_FALL)
		pos += vel * dt
		# murs
		if pos.x <= WL + CLING_OFF:
			pos.x = WL + CLING_OFF
			_land(-1)
		elif pos.x >= WR - CLING_OFF:
			pos.x = WR - CLING_OFF
			_land(1)
		# sol de départ
		if pos.y >= -HALF.y:
			pos.y = -HALF.y
			vel.y = 0.0
			on_floor = true
	var m := tower.meters_at(pos.y + HALF.y)
	if m > life_best:
		life_best = m
		if m > ascension_best:
			ascension_best = m
		height_changed.emit(m)
	_update_player_sprite(_frame())

func _land(s: int) -> void:
	side = s
	vel = Vector2.ZERO
	grip = 0.0
	turn_ok = false
	facing = -s
	Sfx.play("land")
	_burst(pos + Vector2(s * 5, 0), 3, A.P.l, 25.0)

func _frame() -> int:
	if side != 0:
		return 1 if (grip > GRIP_TIME and not on_floor) else 0
	if turn_anim > 0.0:
		return 4
	return 2 if vel.y < 0.0 else 3

func _update_player_sprite(f: int) -> void:
	_place_sprite(player, pos, f, facing < 0)

func _place_sprite(sp: Sprite2D, p: Vector2, f: int, flip: bool) -> void:
	if sp.texture:
		sp.frame = clampi(f, 0, 4)
	sp.flip_h = flip
	# image dessinée accrochée au mur gauche, mains en x=0 : on aligne le bord du sprite sur la face du mur
	var x0 := p.x - CLING_OFF if not flip else p.x + CLING_OFF - 16.0
	if f >= 2:
		x0 = p.x - 8.0   # images en vol : ancrage au centre
	sp.position = Vector2(round(x0), round(p.y - 8.0 - 2.0))

func _step_tide(dt: float) -> void:
	if not tide_on:
		return
	var spd := minf(9.0 + t_life * 0.30, 30.0) + maxf(0.0, ascension_best - 150.0) * 0.02
	tide_y -= spd * dt
	var bottom := cam_y + _vh() + 26.0
	if tide_y > bottom:
		tide_y = bottom

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

# ------------------------------------------------------------------ collisions

func _check_hits() -> void:
	var box := Rect2(pos - HALF, HALF * 2.0)
	# éclats
	for s in tower.shards:
		if taken.has(s.id):
			continue
		if absf(s.pos.y - pos.y) < 10.0 and absf(s.pos.x - pos.x) < 9.0:
			taken[s.id] = true
			shards_run += 1
			Sfx.play("shard")
			_burst(s.pos, 6, A.P.G, 50.0)
			particles.append({"anim": "shard_pop", "p": s.pos, "t": 0.0, "life": 0.32})
			shard_taken.emit(shards_run)
	# marée
	if pos.y + HALF.y > tide_y + 5.0:
		_die({"kind": "tide"})
		return
	# pièges
	for tr in tower.traps:
		if absf(tr.y - pos.y) > 90.0:
			continue
		if neutral.has(tr.id):
			continue
		var hit := false
		match int(tr.type):
			Tower.SPIKES:
				var x0: float = WL if tr.side < 0 else WR - Tower.SPIKE_DEPTH
				var zone := Rect2(x0, tr.y - tr.h + 2.0, Tower.SPIKE_DEPTH, tr.h - 4.0)
				hit = zone.intersects(box)
			Tower.SAW:
				var c := Tower.saw_pos(tr, t_life)
				var q := Vector2(clampf(c.x, box.position.x, box.end.x), clampf(c.y, box.position.y, box.end.y))
				hit = q.distance_to(c) < 6.0
			Tower.LASER:
				hit = Tower.laser_state(tr, t_life) == 2 and absf(tr.y - pos.y) < HALF.y + 2.0
		if hit:
			_die({"kind": "trap", "trap": tr})
			return

func _die(info: Dictionary) -> void:
	state = S.DYING
	hitstop = 0.18
	shake = 4.0
	Sfx.play("die")
	Game.vibrate(70)
	graves.append(pos)
	recordings.append(rec)
	info["height"] = life_best
	info["pos"] = pos
	skin_mat.set_shader_parameter("flash", 1.0)
	particles.append({"anim": "death", "p": pos, "t": 0.0, "life": 0.6})
	_burst(pos, 14, A.P.c, 70.0)
	var tw := create_tween()
	tw.tween_interval(0.18)
	tw.tween_callback(func(): player.visible = false)
	tw.tween_interval(0.45)
	if info.kind == "trap":
		var id: int = info.trap.id
		tw.tween_callback(func():
			neutral[id] = true
			engraving[id] = 0.7
			Sfx.play("engrave")
			var tp := _trap_center(info.trap)
			_burst(tp, 16, A.P.e, 60.0))
		tw.tween_interval(0.7)
	tw.tween_callback(func():
		state = S.WAIT
		life_ended.emit(info))

func _trap_center(tr: Dictionary) -> Vector2:
	match int(tr.type):
		Tower.SPIKES:
			return Vector2(WL + 4 if tr.side < 0 else WR - 4, tr.y - tr.h * 0.5)
		Tower.SAW:
			return Tower.saw_pos(tr, t_life)
	return Vector2(96, tr.y)

## Recentre la caméra sur une position (pour montrer le piège gravé).
func focus(y: float) -> void:
	cam_y = minf(y - _vh() * 0.5, 56.0 - _vh())

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

# ------------------------------------------------------------------ dessin

func _draw() -> void:
	var vh := _vh()
	var top := cam_y - 16.0
	var bot := cam_y + vh + 16.0
	_draw_background(top, bot)
	_draw_floor()
	_draw_marks(top, bot)
	_draw_traps(top, bot)
	if state != S.DEMO:
		_draw_shards(top, bot)
	for g in graves:
		_draw_frame("sprites/grave", 8, 0, g + Vector2(-4, -4), false, A.P.c)
	_draw_particles()
	_draw_tide(bot)

func _draw_frame(name: String, w: int, f: int, at: Vector2, flip: bool, fallback: Color, h: int = -1, mod := Color.WHITE) -> void:
	var tx := A.tex(name)
	if h < 0:
		h = w
	if tx == null:
		draw_rect(Rect2(at.round(), Vector2(w, h)), fallback * mod)
		return
	var src := Rect2(f * w, 0, w, h)
	var dst := Rect2(at.round(), Vector2(w, h))
	if flip:
		dst = Rect2(at.round() + Vector2(w, 0), Vector2(-w, h))
	draw_texture_rect_region(tx, dst, src, mod)

func _draw_background(top: float, bot: float) -> void:
	var r0 := int(floor(top / TILE))
	var r1 := int(ceil(bot / TILE))
	var back := A.tex("env/back")
	var wall := A.tex("env/wall")
	for r in range(r0, r1 + 1):
		if r >= 0:
			continue
		var y := r * TILE
		var dd := tower.deco_for_row(r)
		for i in 8:
			var x := WL + i * TILE
			if back:
				draw_texture_rect_region(back, Rect2(x, y, TILE, TILE), Rect2(dd.back[i] * TILE, 0, TILE, TILE))
			else:
				draw_rect(Rect2(x, y, TILE, TILE), A.P.d if (i + r) % 2 == 0 else A.P.b)
		if wall:
			var shade := Color(0.62, 0.62, 0.75)
			draw_texture_rect_region(wall, Rect2(0, y, TILE, TILE), Rect2(((dd.wr + 1) % 4) * TILE, 0, TILE, TILE), shade)
			draw_texture_rect_region(wall, Rect2(16, y, TILE, TILE), Rect2(dd.wl * TILE, 0, TILE, TILE))
			draw_texture_rect_region(wall, Rect2(WR + TILE, y, -TILE, TILE), Rect2(dd.wr * TILE, 0, TILE, TILE))
			draw_texture_rect_region(wall, Rect2(WR + 2 * TILE, y, -TILE, TILE), Rect2(((dd.wl + 2) % 4) * TILE, 0, TILE, TILE), shade)
		else:
			draw_rect(Rect2(0, y, WL, TILE), A.P.s if r % 2 == 0 else A.P.n)
			draw_rect(Rect2(WR, y, 192 - WR, TILE), A.P.s if r % 2 == 0 else A.P.n)

func _draw_floor() -> void:
	var fl := A.tex("env/floor")
	for i in 12:
		var x := i * TILE
		if fl:
			var f := 0 if i == 0 else (2 if i == 11 else 1)
			draw_texture_rect_region(fl, Rect2(x, 0, TILE, TILE), Rect2(f * TILE, 0, TILE, TILE))
			draw_texture_rect_region(fl, Rect2(x, TILE, TILE, TILE), Rect2(f * TILE, 0, TILE, TILE), Color(0.5, 0.5, 0.65))
		else:
			draw_rect(Rect2(x, 0, TILE, 2 * TILE), A.P.s)

func _draw_marks(top: float, bot: float) -> void:
	var font := A.font()
	var fs := A.font_size()
	# plaques tous les 25 m
	var m0 := int(floor(-bot / TILE / 25.0)) * 25
	var m1 := int(ceil(-top / TILE / 25.0)) * 25
	var pl := A.tex("env/plaque")
	for mm in range(maxi(m0, 25), m1 + 1, 25):
		var y := -mm * TILE
		var at := Vector2(80, y - 6)
		if pl:
			draw_texture(pl, at)
		else:
			draw_rect(Rect2(at, Vector2(32, 12)), A.P.s)
		var txt := "%d M" % mm
		var w := font.get_string_size(txt, HORIZONTAL_ALIGNMENT_LEFT, -1, fs).x
		draw_string(font, Vector2(96 - w * 0.5, y + 3).round(), txt, HORIZONTAL_ALIGNMENT_LEFT, -1, fs, A.P.k)
	# ligne du record
	if state != S.DEMO and record_line > 0:
		var ry := -record_line * TILE
		if ry > top and ry < bot:
			for x in range(int(WL), int(WR), 6):
				draw_rect(Rect2(x, ry, 3, 1), A.P.G)
			draw_string(font, Vector2(WL + 2, ry - 2), Game.t("best"), HORIZONTAL_ALIGNMENT_LEFT, -1, fs, A.P.G)
	# meilleure vie de l'ascension (ligne écho)
	if state != S.DEMO and ascension_best > life_best and ascension_best > 0:
		var ey := -ascension_best * TILE
		if ey > top and ey < bot:
			for x in range(int(WL) + 3, int(WR), 6):
				draw_rect(Rect2(x, ey, 2, 1), A.P.c)

func _draw_traps(top: float, bot: float) -> void:
	for tr in tower.traps:
		if tr.y < top - 80.0 or tr.y > bot + 80.0:
			continue
		var gone: bool = neutral.has(tr.id)
		var flicker: bool = engraving.has(tr.id) and int(t_global * 20.0) % 2 == 0
		var echo := gone and not flicker
		match int(tr.type):
			Tower.SPIKES:
				var n := int(tr.h / TILE)
				var left: bool = tr.side < 0
				for i in n:
					var y: float = tr.y - (i + 1) * TILE
					var x := WL if left else WR - TILE
					if echo:
						_draw_frame("sprites/spikes_echo", 16, 0, Vector2(x, y), not left, A.P.t, 16)
					else:
						if A.tex("sprites/spikes"):
							_draw_frame("sprites/spikes", 16, 0, Vector2(x, y), not left, A.P.z, 16)
						else:
							var xx := x if left else WR - Tower.SPIKE_DEPTH
							draw_rect(Rect2(xx, y + 1, Tower.SPIKE_DEPTH, TILE - 2), A.P.X)
			Tower.SAW:
				var c := Tower.saw_pos(tr, t_life) if not echo else Tower.saw_pos(tr, 0.0)
				if int(tr.mode) != 0 and not echo:
					_draw_rail(tr)
				if echo:
					_draw_frame("sprites/saw_echo", 16, 0, c - Vector2(8, 8), false, A.P.t)
				else:
					var f := int(t_global * 16.0) % 2
					if A.tex("sprites/saw"):
						_draw_frame("sprites/saw", 16, f, c - Vector2(8, 8), false, A.P.z)
					else:
						draw_circle(c, 7.0, A.P.X)
						draw_circle(c, 3.0, A.P.z)
			Tower.LASER:
				var left: bool = tr.side < 0
				var ex := WL if left else WR - TILE
				var st := Tower.laser_state(tr, t_life)
				if echo:
					_draw_frame("sprites/laser_echo", 16, 0, Vector2(ex, tr.y - 8), not left, A.P.t)
					continue
				_draw_frame("sprites/laser", 16, st, Vector2(ex, tr.y - 8), not left, A.P.X)
				if st == 1 and int(t_global * 10.0) % 2 == 0:
					_draw_beam(tr.y, 0, left)
				elif st == 2:
					_draw_beam(tr.y, 1 + int(t_global * 20.0) % 2, left)

func _draw_rail(tr: Dictionary) -> void:
	var a := Tower.saw_pos(tr, (PI * 0.5 - tr.phase) / tr.spd)
	var b := Tower.saw_pos(tr, (PI * 1.5 - tr.phase) / tr.spd)
	if int(tr.mode) == 1:
		for x in range(int(minf(a.x, b.x)), int(maxf(a.x, b.x)) + 1, 4):
			draw_rect(Rect2(x, tr.y, 2, 1), A.P.n)
	else:
		for y in range(int(minf(a.y, b.y)), int(maxf(a.y, b.y)) + 1, 4):
			draw_rect(Rect2(tr.x, y, 1, 2), A.P.n)

func _draw_beam(y: float, f: int, left: bool) -> void:
	var bm := A.tex("sprites/beam")
	var x0 := WL + 16.0 if left else WL
	var x1 := WR if left else WR - 16.0
	if bm == null:
		var h := 1.0 if f == 0 else 3.0
		draw_rect(Rect2(x0, y - h * 0.5, x1 - x0, h), A.P.z if f > 0 else A.P.X)
		return
	var x := x0
	while x < x1:
		var w := minf(8.0, x1 - x)
		draw_texture_rect_region(bm, Rect2(x, y - 4, w, 8), Rect2(f * 8, 0, w, 8))
		x += 8.0

func _draw_shards(top: float, bot: float) -> void:
	var f := int(t_global * 8.0) % 4
	for s in tower.shards:
		if taken.has(s.id) or s.pos.y < top or s.pos.y > bot:
			continue
		var bob := roundf(sin(t_global * 3.0 + s.id) * 1.5)
		_draw_frame("sprites/shard", 8, f, s.pos + Vector2(-4, -4 + bob), false, A.P.G)

func _draw_particles() -> void:
	for pt in particles:
		if pt.has("anim"):
			var k: float = pt.t / pt.life
			if pt.anim == "shard_pop":
				_draw_frame("sprites/shard_pop", 8, mini(3, int(k * 4.0)), pt.p - Vector2(4, 4), false, A.P.y)
			elif pt.anim == "death":
				_draw_frame("sprites/death", 16, mini(4, int(k * 5.0)), pt.p - Vector2(8, 10), facing < 0, A.P.e)
			continue
		var a: float = 1.0 - pt.t / pt.life
		var c: Color = pt.c
		c.a = a
		draw_rect(Rect2(pt.p.round(), Vector2.ONE), c)

func _draw_tide(bot: float) -> void:
	if tide_y > bot + 20.0:
		return
	var tx := A.tex("sprites/tide")
	var f := int(t_global * 4.0) % 2
	var y := roundf(tide_y) - 6.0
	for i in 12:
		if tx:
			draw_texture_rect_region(tx, Rect2(i * TILE, y, TILE, TILE), Rect2(((f + i) % 2) * TILE, 0, TILE, TILE))
		else:
			draw_rect(Rect2(i * TILE, y + 4 + ((i + f) % 2), TILE, TILE), A.P.U)
	draw_rect(Rect2(0, y + TILE, 192, maxf(0.0, bot - y)), A.P.u)
	# bulles qui montent dans le Silence
	for i in 9:
		var bx := fmod(i * 37.0 + 11.0, 192.0)
		var by := y + TILE + fmod(i * 23.0 + t_global * (10.0 + i), 60.0)
		draw_rect(Rect2(bx, y + TILE + 60.0 - (by - y - TILE), 1, 1), A.P.U)
