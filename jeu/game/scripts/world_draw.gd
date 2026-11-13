extends Node2D
## Rendu du monde (tour, dangers, éclats, marée, boss). Lit l'état de world.gd.
## Les sprites existants sont utilisés quand ils existent ; sinon primitives
## dans la palette (A.P) en attendant les assets de la bible v2.

const TILE := 16
const WL := Tower.WALL_L
const WR := Tower.WALL_R

var w  # world.gd

# teinte des murs par biome (B1 Crypte → B6 Sommet)
const BIOME_TINT := [Color(1, 1, 1), Color(1.0, 0.86, 0.9), Color(0.86, 0.92, 1.0),
	Color(0.85, 1.0, 0.95), Color(0.95, 0.88, 1.0), Color(0.9, 0.97, 1.0)]

func _draw() -> void:
	if w == null or w.tower == null:
		return
	var vh: float = w._vh()
	var top: float = w.cam_y - 16.0
	var bot: float = w.cam_y + vh + 16.0
	_draw_background(top, bot)
	_draw_water(top, bot)
	_draw_floor()
	_draw_marks(top, bot)
	var ents: Array = w.tower.near(top - 80.0, bot + 80.0)
	for e in ents:
		_draw_ent(e)
	if not w.boss.is_empty():
		_draw_boss()
	if w.state != w.S.DEMO:
		_draw_shards(top, bot)
	for g in w.graves:
		_frame("sprites/grave", 8, 0, g + Vector2(-4, -4), false, A.P.c)
	_draw_particles()
	_draw_floaters()
	_draw_tide(bot)

# ------------------------------------------------------------------ utilitaires

func _frame(name: String, sz: int, f: int, at: Vector2, flip: bool, fallback: Color, h: int = -1, mod := Color.WHITE) -> void:
	var tx := A.tex(name)
	if h < 0:
		h = sz
	if tx == null:
		draw_rect(Rect2(at.round(), Vector2(sz, h)), fallback * mod)
		return
	var src := Rect2(f * sz, 0, sz, h)
	var dst := Rect2(at.round(), Vector2(sz, h))
	if flip:
		dst = Rect2(at.round() + Vector2(sz, 0), Vector2(-sz, h))
	draw_texture_rect_region(tx, dst, src, mod)

func _blink(hz: float) -> bool:
	return int(w.t_global * hz) % 2 == 0

## Temps auquel dessiner l'entité, et couleur de rendu (cyan si gravée).
func _state(e: Dictionary) -> Array:
	if w.neutral.has(e.id):
		var fl: bool = w.engraving.has(e.id) and _blink(20.0)
		return [float(w.neutral[e.id]), not fl]
	return [w.t_life, false]

# ------------------------------------------------------------------ décor

func _draw_background(top: float, bot: float) -> void:
	var r0 := int(floor(top / TILE))
	var r1 := int(ceil(bot / TILE))
	var back := A.tex("env/back")
	var wall := A.tex("env/wall")
	for r in range(r0, r1 + 1):
		if r >= 0:
			continue
		var y := r * TILE
		var dd: Dictionary = w.tower.deco_for_row(r)
		var bi := Tower.biome_index(-r - 1)
		var tint: Color = BIOME_TINT[clampi(bi, 0, 5)]
		for i in 8:
			var x := WL + i * TILE
			if back:
				draw_texture_rect_region(back, Rect2(x, y, TILE, TILE), Rect2(dd.back[i] * TILE, 0, TILE, TILE), tint)
			else:
				draw_rect(Rect2(x, y, TILE, TILE), (A.P.d if (i + r) % 2 == 0 else A.P.b) * tint)
		if wall:
			var shade := Color(0.62, 0.62, 0.75) * tint
			draw_texture_rect_region(wall, Rect2(0, y, TILE, TILE), Rect2(((dd.wr + 1) % 4) * TILE, 0, TILE, TILE), shade)
			draw_texture_rect_region(wall, Rect2(16, y, TILE, TILE), Rect2(dd.wl * TILE, 0, TILE, TILE), tint)
			draw_texture_rect_region(wall, Rect2(WR + TILE, y, -TILE, TILE), Rect2(dd.wr * TILE, 0, TILE, TILE), tint)
			draw_texture_rect_region(wall, Rect2(WR + 2 * TILE, y, -TILE, TILE), Rect2(((dd.wl + 2) % 4) * TILE, 0, TILE, TILE), shade)
		else:
			draw_rect(Rect2(0, y, WL, TILE), (A.P.s if r % 2 == 0 else A.P.n) * tint)
			draw_rect(Rect2(WR, y, 192 - WR, TILE), (A.P.s if r % 2 == 0 else A.P.n) * tint)

func _draw_water(top: float, bot: float) -> void:
	var m0 := Tower.meters_at(bot)
	var m1 := Tower.meters_at(top)
	for m in range(m0, m1 + 1):
		if w.tower.water.has(m):
			var y := Tower.row_top(m)
			var c: Color = A.P.m
			c.a = 0.35
			draw_rect(Rect2(WL, y, WR - WL, TILE), c)
			if not w.tower.water.has(m + 1):
				var x := fposmod(w.t_global * 12.0, 8.0)
				var xx := WL + x
				while xx < WR:
					draw_rect(Rect2(xx, y, 4, 1), A.P.l)
					xx += 8.0

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
		var tw := font.get_string_size(txt, HORIZONTAL_ALIGNMENT_LEFT, -1, fs).x
		draw_string(font, Vector2(96 - tw * 0.5, y + 3).round(), txt, HORIZONTAL_ALIGNMENT_LEFT, -1, fs, A.P.k)
	if w.state != w.S.DEMO and w.record_line > 0:
		var ry: float = -w.record_line * TILE
		if ry > top and ry < bot:
			for x in range(int(WL), int(WR), 6):
				draw_rect(Rect2(x, ry, 3, 1), A.P.G)
			draw_string(font, Vector2(WL + 2, ry - 2), Game.t("best"), HORIZONTAL_ALIGNMENT_LEFT, -1, fs, A.P.G)
	if w.state != w.S.DEMO and w.ascension_best > w.life_best and w.ascension_best > 0:
		var ey: float = -w.ascension_best * TILE
		if ey > top and ey < bot:
			for x in range(int(WL) + 3, int(WR), 6):
				draw_rect(Rect2(x, ey, 2, 1), A.P.c)

# ------------------------------------------------------------------ entités

func _draw_ent(e: Dictionary) -> void:
	var s := _state(e)
	var t: float = s[0]
	var cy: bool = s[1]
	var hot: Color = A.P.c if cy else A.P.X
	var core: Color = A.P.t if cy else A.P.z
	match String(e.kind):
		"spikes":
			var left: bool = int(e.side) < 0
			var y := float(e.y0)
			while y < float(e.y1) - 1.0:
				var x := WL if left else WR - TILE
				var nm := "sprites/spikes_echo" if cy else "sprites/spikes"
				if A.tex(nm):
					_frame(nm, 16, 0, Vector2(x, y), not left, hot, 16)
				else:
					var xx := WL if left else WR - Tower.SPIKE_DEPTH
					for k in 3:
						var py := y + 2 + k * 5
						var tip := Vector2(xx + Tower.SPIKE_DEPTH, py + 2) if left else Vector2(xx, py + 2)
						var base := xx if left else xx + Tower.SPIKE_DEPTH
						draw_colored_polygon(PackedVector2Array([Vector2(base, py), tip, Vector2(base, py + 4)]), hot)
				y += TILE
		"buttress":
			var bx := WL if int(e.side) < 0 else WR - Tower.BUTTRESS_W
			draw_rect(Rect2(bx, e.y0, Tower.BUTTRESS_W, float(e.y1) - float(e.y0)), A.P.n)
			draw_rect(Rect2(bx, e.y0, Tower.BUTTRESS_W, 1), A.P.l)
			for k in 3:
				var px := bx + 2 + k * 4
				draw_colored_polygon(PackedVector2Array([Vector2(px, e.y0), Vector2(px + 2, float(e.y0) - 5), Vector2(px + 4, e.y0)]), hot)
				draw_colored_polygon(PackedVector2Array([Vector2(px, e.y1), Vector2(px + 2, float(e.y1) + 5), Vector2(px + 4, e.y1)]), hot)
		"friable":
			var fx := WL - 4 if int(e.side) < 0 else WR
			var broken := false
			var shaking := false
			if not cy and w.fr_start.has(e.id):
				var u: float = w.t_life - float(w.fr_start[e.id])
				broken = u >= 0.35 and u < 3.35
				shaking = u < 0.35
			if broken:
				for k in 4:
					draw_rect(Rect2(fx + (k % 2) * 2, float(e.y0) + k * 5, 2, 2), A.P.n)
			else:
				var ox := (1.0 if _blink(30.0) else -1.0) if shaking else 0.0
				var c: Color = A.P.t if cy else A.P.s
				draw_rect(Rect2(fx + ox, e.y0, 4, float(e.y1) - float(e.y0)), c)
				var yy := float(e.y0) + 3
				while yy < float(e.y1):
					draw_rect(Rect2(fx + ox + 1, yy, 2, 1), A.P.n)
					yy += 6
		"saw":
			var p := Hz.saw_pos(e, t)
			if int(e.axis) != 0 and not cy:
				if int(e.axis) == 1:
					var x := minf(e.a, e.b)
					while x <= maxf(e.a, e.b):
						draw_rect(Rect2(x, p.y, 2, 1), A.P.n)
						x += 4
				else:
					var y := minf(e.a, e.b)
					while y <= maxf(e.a, e.b):
						draw_rect(Rect2(p.x, y, 1, 2), A.P.n)
						y += 4
			var nm := "sprites/saw_echo" if cy else "sprites/saw"
			if A.tex(nm):
				_frame(nm, 16, 0 if cy else int(w.t_global * 16.0) % 2, p - Vector2(8, 8), false, hot)
			else:
				draw_circle(p, 7.0, hot)
				draw_circle(p, 3.0, core)
		"pendulum":
			var q := Hz.pendulum_pos(e, t)
			var a: Vector2 = e.anchor
			draw_line(a, q, A.P.c if cy else A.P.l, 1.0)
			draw_rect(Rect2(a - Vector2(2, 2), Vector2(4, 4)), A.P.n)
			draw_circle(q, float(e.r) + 1.0, hot)
			draw_circle(q, 2.0, core)
		"laser":
			var ls := Hz.laser_state(e, t)
			var y: float = e.y
			draw_rect(Rect2(WL, y - 3, 4, 6), A.P.n)
			draw_rect(Rect2(WR - 4, y - 3, 4, 6), A.P.n)
			if cy:
				for x in range(int(WL) + 4, int(WR) - 4, 4):
					draw_rect(Rect2(x, y, 2, 1), A.P.c)
			elif ls == 1:
				if _blink(10.0):
					draw_rect(Rect2(WL + 4, y, WR - WL - 8, 1), A.P.X)
			elif ls == 2:
				draw_rect(Rect2(WL + 4, y - 2, WR - WL - 8, 4), A.P.X)
				draw_rect(Rect2(WL + 4, y - (0 if _blink(20.0) else 1), WR - WL - 8, 1 + (0 if _blink(20.0) else 1)), A.P.Z)
		"herse":
			var hs := Hz.herse_state(e, t)
			var left: bool = int(e.side) < 0
			var ext := 24.0 if (hs == 2 or cy) else (4.0 if hs == 1 else 0.0)
			var y0 := float(e.y0) + 2.0
			var y1 := float(e.y1) - 2.0
			if hs == 1 and not cy and _blink(10.0):
				draw_rect(Rect2(WL if left else WR - 2, y0, 2, y1 - y0), A.P.X)
			if ext > 0.0:
				var yy := y0
				while yy < y1:
					var x0 := WL if left else WR
					var tip := WL + ext if left else WR - ext
					draw_line(Vector2(x0, yy + 1), Vector2(tip, yy + 1), hot, 2.0)
					yy += 5.0
		"jaws":
			var j := Hz.jaws(e, t)
			var mid: float = (float(e.y0) + float(e.y1)) * 0.5
			var ext: float = j.x
			if j.y == 1 and not cy and _blink(10.0):
				draw_rect(Rect2(WL, mid - 10, 3, 20), A.P.X)
				draw_rect(Rect2(WR - 3, mid - 10, 3, 20), A.P.X)
			ext = maxf(ext, 3.0)
			draw_rect(Rect2(WL, mid - 10, ext, 20), hot)
			draw_rect(Rect2(WR - ext, mid - 10, ext, 20), hot)
			for k in 4:
				var ty := mid - 8 + k * 5
				draw_rect(Rect2(WL + ext, ty, 2, 2), core)
				draw_rect(Rect2(WR - ext - 2, ty, 2, 2), core)
		"grignon":
			var g := Hz.grignon_pos(e, t)
			draw_rect(Rect2(g - Vector2(4, 3), Vector2(8, 6)), hot)
			draw_rect(Rect2(g + Vector2(-2, -1), Vector2(1, 1)), A.P.W)
			draw_rect(Rect2(g + Vector2(1, -1), Vector2(1, 1)), A.P.W)
		"moth":
			var m := Hz.moth_pos(e, t)
			var flap := 2.0 if _blink(12.0) else 0.0
			draw_rect(Rect2(m - Vector2(4, 3 - flap * 0.5), Vector2(3, 6 - flap)), hot)
			draw_rect(Rect2(m + Vector2(1, -3 + flap * 0.5), Vector2(3, 6 - flap)), hot)
			draw_rect(Rect2(m - Vector2(1, 2), Vector2(2, 4)), core)
		"rockfall":
			var ry := Hz.rock_y(e, t, w.st, w.tower.is_water(float(e.y)))
			var armed: bool = w.st.has(e.id) and ry <= float(e.y)
			var rx: float = float(e.x) + (1.0 if armed and _blink(30.0) else 0.0)
			draw_rect(Rect2(rx - 5, ry - 5, 10, 10), A.P.c if cy else A.P.s)
			draw_rect(Rect2(rx - 5, ry - 5, 10, 2), A.P.l)
			if armed:
				draw_rect(Rect2(rx - 1, ry + 6, 2, 2), A.P.X)
		"power":
			if w.used.has(e.id):
				return
			var p: Vector2 = e.pos + Vector2(0, roundf(sin(w.t_global * 2.5) * 2.0))
			var col: Color = {"burin": A.P.c, "plume": A.P.p, "accalmie": A.P.U}.get(String(e.power), A.P.y)
			draw_circle(p, 6.0, A.P.k)
			draw_arc(p, 6.0, 0, TAU, 16, col, 1.0)
			draw_rect(Rect2(p - Vector2(2, 2), Vector2(4, 4)), col)
		"altar":
			var on: bool = w.altars_on.has(e.id)
			var ax: float = float(e.x)
			var ay: float = float(e.y)
			draw_rect(Rect2(ax - 8, ay + 2, 16, 6), A.P.n)
			draw_rect(Rect2(ax - 6, ay - 6, 12, 8), A.P.s)
			var fl: Color = A.P.a if on else A.P.d
			draw_rect(Rect2(ax - 2, ay - 12 - (1 if on and _blink(6.0) else 0), 4, 6), fl)
		"rune":
			_draw_rune(e, false)

func _draw_rune(r: Dictionary, active: bool) -> void:
	var x := WL + 4 if int(r.side) < 0 else WR - 12
	var y: float = float(r.y) - 4
	var lit: bool = active
	var col: Color = A.P.G if lit else A.P.n
	draw_rect(Rect2(x, y, 8, 8), col)
	draw_rect(Rect2(x + 3, y + 1, 2, 6), A.P.k)
	draw_rect(Rect2(x + 1, y + 3, 6, 2), A.P.k)

func _draw_boss() -> void:
	var b: Vector2 = w.bell_pos()
	var mid: float = (float(w.boss.y0) + float(w.boss.y1)) * 0.5
	var anchor := Vector2(96.0, mid - 56.0)
	draw_line(anchor, b, A.P.l, 1.0)
	var stun: bool = w.boss_stun > 0.0
	var body: Color = A.P.c if stun else A.P.U
	draw_colored_polygon(PackedVector2Array([b + Vector2(-8, -14), b + Vector2(8, -14), b + Vector2(18, 12), b + Vector2(-18, 12)]), body)
	draw_rect(Rect2(b + Vector2(-18, 12), Vector2(36, 3)), A.P.u)
	draw_circle(b + Vector2(0, 16), 3.0, A.P.X if not stun else A.P.t)
	# runes : la prochaine est allumée
	for i in w.boss_runes.size():
		var r: Dictionary = w.boss_runes[i]
		if i < w.boss_hits:
			_draw_rune(r, true)
		elif i == w.boss_hits:
			_draw_rune(r, _blink(4.0))
	var ws: Vector2 = w.wave_state()
	if ws.y == 0 and _blink(10.0):
		draw_rect(Rect2(WL, ws.x, WR - WL, 1), A.P.X)
	elif ws.y == 1:
		draw_rect(Rect2(WL, ws.x - 2, WR - WL, 4), A.P.U)
		draw_rect(Rect2(WL, ws.x, WR - WL, 1), A.P.X)

# ------------------------------------------------------------------ objets, effets

func _draw_shards(top: float, bot: float) -> void:
	var f := int(w.t_global * 8.0) % 4
	for s in w.tower.shards:
		if s.pos.y < top or s.pos.y > bot or w.taken.has(s.id):
			continue
		var bob := roundf(sin(w.t_global * 3.0 + s.id) * 1.5)
		if s.big:
			var p: Vector2 = s.pos + Vector2(0, bob)
			draw_colored_polygon(PackedVector2Array([p + Vector2(0, -6), p + Vector2(5, 0), p + Vector2(0, 6), p + Vector2(-5, 0)]), A.P.G)
			draw_rect(Rect2(p - Vector2(1, 3), Vector2(2, 3)), A.P.y)
		else:
			_frame("sprites/shard", 8, f, s.pos + Vector2(-4, -4 + bob), false, A.P.G)

func _draw_particles() -> void:
	for pt in w.particles:
		if pt.has("anim"):
			var k: float = pt.t / pt.life
			if pt.anim == "shard_pop":
				_frame("sprites/shard_pop", 8, mini(3, int(k * 4.0)), pt.p - Vector2(4, 4), false, A.P.y)
			elif pt.anim == "death":
				_frame("sprites/death", 16, mini(4, int(k * 5.0)), pt.p - Vector2(8, 10), w.facing < 0, A.P.e)
			continue
		var c: Color = pt.c
		c.a = 1.0 - pt.t / pt.life
		draw_rect(Rect2(pt.p.round(), Vector2.ONE), c)

func _draw_floaters() -> void:
	var font := A.font()
	var fs := A.font_size()
	for f in w.floaters:
		var c: Color = f.col
		c.a = clampf(2.0 * (1.0 - f.t / f.life), 0.0, 1.0)
		var tw := font.get_string_size(f.txt, HORIZONTAL_ALIGNMENT_LEFT, -1, fs).x
		var x := clampf(f.p.x - tw * 0.5, WL + 1, WR - tw - 1)
		draw_string(font, Vector2(x, f.p.y).round() + Vector2(1, 1), f.txt, HORIZONTAL_ALIGNMENT_LEFT, -1, fs, Color(A.P.k, c.a))
		draw_string(font, Vector2(x, f.p.y).round(), f.txt, HORIZONTAL_ALIGNMENT_LEFT, -1, fs, c)

func _draw_tide(bot: float) -> void:
	var ty: float = w.tide_y
	if ty > bot + 20.0:
		return
	var tx := A.tex("sprites/tide")
	var f := int(w.t_global * 4.0) % 2
	var y := roundf(ty) - 6.0
	for i in 12:
		if tx:
			draw_texture_rect_region(tx, Rect2(i * TILE, y, TILE, TILE), Rect2(((f + i) % 2) * TILE, 0, TILE, TILE))
		else:
			draw_rect(Rect2(i * TILE, y + 4 + ((i + f) % 2), TILE, TILE), A.P.U)
	draw_rect(Rect2(0, y + TILE, 192, maxf(0.0, bot - y)), A.P.u)
	for i in 9:
		var bx := fmod(i * 37.0 + 11.0, 192.0)
		var by := fmod(i * 23.0 + w.t_global * (10.0 + i), 60.0)
		draw_rect(Rect2(bx, y + TILE + 60.0 - by, 1, 1), A.P.U)
