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
		if not _spr("fx/echo_shard", 8, 8, int(w.t_global * 8.0) % 4, g + Vector2(-4, -4), false, false, Color(1, 1, 1, 0.75)):
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

const BIOME_ENV := ["crypte", "fonderie", "bibliotheque", "", "", ""]
const DECO_PERIOD := 12

func _env_name(bi: int) -> String:
	var n: String = BIOME_ENV[clampi(bi, 0, 5)]
	if n != "" and A.tex("env/wall_%s_L" % n):
		return n
	return ""

func _draw_background(top: float, bot: float) -> void:
	_draw_layers(top, bot)
	var r0 := int(floor(top / TILE))
	var r1 := int(ceil(bot / TILE))
	var wall := A.tex("env/wall")
	for r in range(r0, r1 + 1):
		if r >= 0:
			continue
		var y := r * TILE
		var m := -r - 1
		var dd: Dictionary = w.tower.deco_for_row(r)
		var bi := Tower.biome_index(m)
		var env := _env_name(bi)
		if env != "":
			_draw_wall_row(r, y, m, bi, env, dd)
			continue
		var tint: Color = BIOME_TINT[clampi(bi, 0, 5)]
		if wall:
			var shade := Color(0.62, 0.62, 0.75) * tint
			draw_texture_rect_region(wall, Rect2(0, y, TILE, TILE), Rect2(((dd.wr + 1) % 4) * TILE, 0, TILE, TILE), shade)
			draw_texture_rect_region(wall, Rect2(16, y, TILE, TILE), Rect2(dd.wl * TILE, 0, TILE, TILE), tint)
			draw_texture_rect_region(wall, Rect2(WR + TILE, y, -TILE, TILE), Rect2(dd.wr * TILE, 0, TILE, TILE), tint)
			draw_texture_rect_region(wall, Rect2(WR + 2 * TILE, y, -TILE, TILE), Rect2(((dd.wl + 2) % 4) * TILE, 0, TILE, TILE), shade)
		else:
			draw_rect(Rect2(0, y, WL, TILE), (A.P.s if r % 2 == 0 else A.P.n) * tint)
			draw_rect(Rect2(WR, y, 192 - WR, TILE), (A.P.s if r % 2 == 0 else A.P.n) * tint)

## Module de décor commençant à la rangée r dans la colonne intérieure c (0 = gauche, 1 = droite), ou -1.
func _deco_at(r: int, c: int) -> int:
	var off := posmod(hash(Vector2i(w.tower.seed_value, 7 + c)), DECO_PERIOD)
	if posmod(r + off, DECO_PERIOD) != 0 or r >= -2:
		return -1
	var block := int(floor(float(r + off) / DECO_PERIOD))
	var h := posmod(hash(Vector3i(w.tower.seed_value, r, c)), 3) + 1
	return 0 if posmod(block, 2) == 0 else h

## Index de tuile pour la rangée r, colonne c : remplace le tirage par une tuile éclairée autour d'une source.
func _wall_lit(r: int, c: int) -> int:
	if _deco_at(r + 1, c) == 0:
		return 0
	if _deco_at(r - 2, c) == 0:
		return 1
	return -1

func _draw_wall_row(r: int, y: float, m: int, bi: int, env: String, dd: Dictionary) -> void:
	var shade := Color(0.7, 0.7, 0.78)
	var tl := A.tex("env/wall_%s_L" % env)
	var tr := A.tex("env/wall_%s_R" % env)
	var il: int = dd.wl
	var ir: int = dd.wr
	var rare := posmod(hash(Vector2i(w.tower.seed_value * 31, r)), 40) == 0
	if rare:
		il = 6
	# transition vers le biome suivant (tuile 0 = dernière rangée, tuile 1 = première du biome du haut)
	var trans := ""
	var ti := 0
	if bi + 1 < Tower.BIOMES.size() and m == int(Tower.BIOMES[bi + 1].start) - 1:
		trans = env
		ti = 0
	elif bi > 0 and m == int(Tower.BIOMES[bi].start):
		trans = _env_name(bi - 1)
		ti = 1
	if trans != "":
		var nxt: String = BIOME_ENV[clampi(bi + (1 if ti == 0 else 0), 0, 5)]
		var tt_l := A.tex("env/wall_%s_to_%s_L" % [trans, nxt])
		var tt_r := A.tex("env/wall_%s_to_%s_R" % [trans, nxt])
		if tt_l and tt_r:
			draw_texture_rect_region(tt_r, Rect2(0, y, TILE, TILE), Rect2(ti * TILE, 0, TILE, TILE), shade)
			draw_texture_rect_region(tt_l, Rect2(16, y, TILE, TILE), Rect2(ti * TILE, 0, TILE, TILE))
			draw_texture_rect_region(tt_r, Rect2(WR, y, TILE, TILE), Rect2(ti * TILE, 0, TILE, TILE))
			draw_texture_rect_region(tt_l, Rect2(WR + TILE, y, TILE, TILE), Rect2(ti * TILE, 0, TILE, TILE), shade)
			return
	# colonnes extérieures (assombries)
	draw_texture_rect_region(tr, Rect2(0, y, TILE, TILE), Rect2(((ir + 1) % 4) * TILE, 0, TILE, TILE), shade)
	draw_texture_rect_region(tl, Rect2(WR + TILE, y, TILE, TILE), Rect2(((dd.wl + 2) % 4) * TILE, 0, TILE, TILE), shade)
	# colonnes intérieures
	var cols := [[16, tl, il, "L"], [WR, tr, ir, "R"]]
	for c in 2:
		var x: int = cols[c][0]
		var tex: Texture2D = cols[c][1]
		var idx: int = cols[c][2]
		var side: String = cols[c][3]
		var lit := _wall_lit(r, c)
		var lt := A.tex("env/wall_%s_lit_%s" % [env, side])
		if lit >= 0 and lt:
			draw_texture_rect_region(lt, Rect2(x, y, TILE, TILE), Rect2(lit * TILE, 0, TILE, TILE))
		else:
			draw_texture_rect_region(tex, Rect2(x, y, TILE, TILE), Rect2(idx * TILE, 0, TILE, TILE))
		# module de décor 16×32 : il couvre les rangées r et r+1 ; on le dessine sur la rangée du bas (r+1) pour passer par-dessus.
		var dm := _deco_at(r - 1, c)
		var dt := A.tex("env/wall_%s_deco_%s" % [env, side])
		if dm >= 0 and dt and Tower.biome_index(m + 1) == bi:
			draw_texture_rect_region(dt, Rect2(x, y - TILE, TILE, 2 * TILE), Rect2(dm * TILE, 0, TILE, 2 * TILE))

## Plans de fond (bg0 0.10, bg1 0.30, bg2 0.60), découpés par biome.
func _draw_layers(top: float, bot: float) -> void:
	var back := A.tex("env/back")
	var y_lo := minf(bot, 0.0)
	if top >= y_lo:
		return
	for bi in Tower.BIOMES.size():
		var s0: float = -float(Tower.BIOMES[bi].start) * TILE
		var s1: float = -INF if bi + 1 >= Tower.BIOMES.size() else -float(Tower.BIOMES[bi + 1].start) * TILE
		var a := maxf(top, s1)
		var b := minf(y_lo, s0)
		if a >= b:
			continue
		var env: String = BIOME_ENV[bi]
		var bg0 := A.tex("env/bg0_%s" % env) if env != "" else null
		if bg0:
			_layer(bg0, 0.10, Vector2(64, 0), 256.0, a, b, -1)
			var bg1 := A.tex("env/bg1_%s" % env)
			if bg1:
				_layer(bg1, 0.30, Vector2(32, 0), 256.0, a, b, -1)
		else:
			_old_back(back, bi, a, b)
		var bg2 := A.tex("env/bg2_%s" % env) if env != "" else null
		if bg2:
			for band in 2:
				_layer(bg2, 0.60, Vector2(WL + band * 96, 0), 32.0, a, b, band, env)

func _old_back(back: Texture2D, bi: int, a: float, b: float) -> void:
	var tint: Color = BIOME_TINT[clampi(bi, 0, 5)] * Color(0.55, 0.55, 0.62)
	for r in range(int(floor(a / TILE)), int(ceil(b / TILE))):
		var y0 := maxf(r * TILE, a)
		var y1 := minf((r + 1) * TILE, b)
		if y1 <= y0:
			continue
		var dd: Dictionary = w.tower.deco_for_row(r)
		for i in 8:
			var x := WL + i * TILE
			if back:
				draw_texture_rect_region(back, Rect2(x, y0, TILE, y1 - y0), Rect2(dd.back[i] * TILE, y0 - r * TILE, TILE, y1 - y0), tint)
			else:
				draw_rect(Rect2(x, y0, TILE, y1 - y0), (A.P.d if (i + r) % 2 == 0 else A.P.b) * tint)

## Pose un plan en parallaxe entre a et b (coordonnées monde).
## band < 0 : texture pleine largeur 128 (src.x = décalage). band >= 0 : bande de 32 px de bg2 avec choix de panneau.
func _layer(tex: Texture2D, p: float, at: Vector2, h: float, a: float, b: float, band: int, env := "") -> void:
	var base: float = w.cam_y * (1.0 - p)
	var k0 := int(floor((a - base) / h))
	var k1 := int(floor((b - base) / h))
	var deco := A.tex("env/bg2_%s_deco" % env) if band >= 0 else null
	for k in range(k0, k1 + 1):
		var uy := base + k * h
		var y0 := maxf(uy, a)
		var y1 := minf(uy + h, b)
		if y1 <= y0:
			continue
		var sy := y0 - uy
		if band < 0:
			var ty := fposmod(uy - base, float(tex.get_height()))
			draw_texture_rect_region(tex, Rect2(WL, y0, WR - WL, y1 - y0), Rect2(at.x, ty + sy, WR - WL, y1 - y0))
		else:
			var hh := posmod(hash(Vector3i(w.tower.seed_value, k, band + 3)), 60)
			var sx := 0
			if env == "crypte":
				sx = 0 if hh >= 10 else (1 + hh % 3) * 32
			else:
				sx = 0 if hh >= 18 else (1 + hh % 3) * 32
			draw_texture_rect_region(tex, Rect2(at.x, y0, 32, y1 - y0), Rect2(sx, sy, 32, y1 - y0))
			if deco and hh >= 54:
				draw_texture_rect_region(deco, Rect2(at.x, y0, 32, y1 - y0), Rect2((hh % 3) * 32, sy, 32, y1 - y0))
			# pilier de bord (ferme la bande côté puits)
			var bord := A.tex("env/bg2_bord")
			var bx: int = {"crypte": 0, "fonderie": 16, "bibliotheque": 32}.get(env, -1)
			if bord and bx >= 0:
				var px := at.x + (24 if band == 0 else 0)
				draw_texture_rect_region(bord, Rect2(px, y0, 8, y1 - y0), Rect2(bx + band * 8, sy, 8, y1 - y0))
			else:
				var ex := at.x + (31 if band == 0 else 0)
				draw_rect(Rect2(ex, y0, 1, y1 - y0), Color(0, 0, 0, 0.45))

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
	var fs := A.tex("env/floor_start")
	var fl := fs if fs else A.tex("env/floor")
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

## Sprite d'une bande : cellule cw×ch, image f, miroirs horizontal / vertical, rognage en hauteur.
func _spr(name: String, cw: int, ch: int, f: int, at: Vector2, fh := false, fv := false, mod := Color.WHITE, hcut := -1) -> bool:
	var tx := A.tex(name)
	if tx == null:
		return false
	var h := ch if hcut < 0 else mini(hcut, ch)
	if h <= 0:
		return true
	var src := Rect2(f * cw, 0 if not fv else ch - h, cw, h)
	var pos := at.round()
	var size := Vector2(cw, h)
	if fh:
		pos.x += cw
		size.x = -cw
	if fv:
		pos.y += h
		size.y = -h
	draw_texture_rect_region(tx, Rect2(pos, size), src, mod)
	return true

## Nom du sprite de piège (version écho si gravé et si elle existe).
func _tn(base: String, cy: bool) -> String:
	if cy and A.tex("traps/" + base + "_echo"):
		return "traps/" + base + "_echo"
	return "traps/" + base

func _draw_ent(e: Dictionary) -> void:
	var s := _state(e)
	var t: float = s[0]
	var cy: bool = s[1]
	var hot: Color = A.P.c if cy else A.P.X
	var core: Color = A.P.t if cy else A.P.z
	var tg: float = w.t_global
	match String(e.kind):
		"spikes":
			var left: bool = int(e.side) < 0
			var y := float(e.y0)
			while y < float(e.y1) - 1.0:
				var x := WL if left else WR - TILE
				var ph := fposmod(tg + y * 0.031, 2.0) * 12.0
				var f := 1 + int(ph) if ph < 4.0 and not cy else 0
				if not _spr(_tn("spikes", cy), 16, 16, f, Vector2(x, y), not left, false, Color.WHITE, int(float(e.y1) - y)):
					var xx := WL if left else WR - Tower.SPIKE_DEPTH
					for k in 3:
						var py := y + 2 + k * 5
						var tip := Vector2(xx + Tower.SPIKE_DEPTH, py + 2) if left else Vector2(xx, py + 2)
						var base := xx if left else xx + Tower.SPIKE_DEPTH
						draw_colored_polygon(PackedVector2Array([Vector2(base, py), tip, Vector2(base, py + 4)]), hot)
				y += TILE
		"buttress":
			var left: bool = int(e.side) < 0
			var bx := WL if left else WR - Tower.BUTTRESS_W
			var hh: float = float(e.y1) - float(e.y0)
			var drawn := false
			if absf(hh - 32.0) < 1.0 or absf(hh - 48.0) < 1.0:
				drawn = _spr(_tn("buttress", cy), 16, 58, 0 if hh < 40.0 else 1, Vector2(bx, float(e.y0) - 5.0), not left, false, Color.WHITE, int(hh) + 10)
			if not drawn:
				draw_rect(Rect2(bx, e.y0, Tower.BUTTRESS_W, hh), A.P.n)
				draw_rect(Rect2(bx, e.y0, Tower.BUTTRESS_W, 1), A.P.l)
				for k in 3:
					var px := bx + 2 + k * 4
					draw_colored_polygon(PackedVector2Array([Vector2(px, e.y0), Vector2(px + 2, float(e.y0) - 5), Vector2(px + 4, e.y0)]), hot)
					draw_colored_polygon(PackedVector2Array([Vector2(px, e.y1), Vector2(px + 2, float(e.y1) + 5), Vector2(px + 4, e.y1)]), hot)
		"friable":
			var left: bool = int(e.side) < 0
			var fx := WL - 4 if left else WR + 4 - 16
			var f := 0
			var ox := 0.0
			if not cy and w.fr_start.has(e.id):
				var u: float = w.t_life - float(w.fr_start[e.id])
				if u < 0.17:
					f = 1
				elif u < 0.35:
					f = 2
					ox = 1.0 if _blink(30.0) else 0.0
				elif u < 0.475:
					f = 3
				elif u < 3.35:
					f = -1
			if f >= 0 and A.tex("traps/crumble"):
				var mod := Color(0.6, 1.4, 1.4) if cy else Color.WHITE
				var y := float(e.y0)
				while y < float(e.y1) - 1.0:
					_spr("traps/crumble", 16, 32, f, Vector2(fx + ox, y), not left, false, mod, int(float(e.y1) - y))
					y += 32.0
			elif f >= 0:
				var c: Color = A.P.t if cy else A.P.s
				var gx := WL - 4 if left else WR
				draw_rect(Rect2(gx + ox, e.y0, 4, float(e.y1) - float(e.y0)), c)
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
			if not _spr(_tn("saw", cy), 24, 24, int(tg * 20.0) % 4, p - Vector2(12, 12)):
				draw_circle(p, 7.0, hot)
				draw_circle(p, 3.0, core)
		"pendulum":
			var q := Hz.pendulum_pos(e, t)
			var a: Vector2 = e.anchor
			if A.tex("traps/chain") and not cy:
				var n := int(a.distance_to(q) / 8.0)
				for k in n:
					_spr("traps/chain", 8, 8, 0, a.lerp(q, float(k) / float(maxi(n, 1))) - Vector2(4, 0))
			else:
				draw_line(a, q, A.P.c if cy else A.P.l, 1.0)
			draw_rect(Rect2(a - Vector2(2, 2), Vector2(4, 4)), A.P.n)
			var u := fposmod(t / float(e.period) + float(e.phase), 1.0)
			var low := absf(cos(TAU * u)) > 0.97
			var f := 2 if low and not cy else int(u * 4.0) % 2
			if not _spr(_tn("pendulum_chandelier", cy), 16, 16, 0 if cy else f, q - Vector2(8, 8), cos(TAU * u) < 0.0):
				draw_circle(q, float(e.r) + 1.0, hot)
				draw_circle(q, 2.0, core)
		"laser":
			var ls := Hz.laser_state(e, t)
			var y: float = e.y
			var mf := 0 if cy else (2 if ls == 2 else (int(tg * 10.0) % 2 if ls == 1 else 0))
			if _spr(_tn("laser", cy), 8, 8, mf, Vector2(WL, y - 4)):
				_spr(_tn("laser", cy), 8, 8, mf, Vector2(WR - 8, y - 4), true)
				var bf := -1
				if cy:
					bf = 0
				elif ls == 1 and _blink(10.0):
					bf = 0
				elif ls == 2:
					bf = 1 + int(tg * 20.0) % 3
				if bf >= 0:
					var x := WL + 8
					while x < WR - 8:
						_spr(_tn("beam", cy), 16, 8, bf, Vector2(x, y - 4), false, false, Color.WHITE)
						x += 16
			else:
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
		"herse":
			var hs := Hz.herse_state(e, t)
			var left: bool = int(e.side) < 0
			var f := 0
			if cy:
				f = 0
			elif hs == 1:
				f = 1 if _blink(10.0) else 0
			elif hs == 2:
				f = 3
			var hx := WL if left else WR - 24
			if A.tex("traps/portcullis"):
				var y := float(e.y0)
				while y < float(e.y1) - 1.0:
					_spr(_tn("portcullis", cy), 24, 32, f, Vector2(hx, y), not left, false, Color.WHITE, int(float(e.y1) - y))
					y += 32.0
			elif hs == 2 or cy:
				var yy := float(e.y0) + 2.0
				while yy < float(e.y1) - 2.0:
					var x0 := WL if left else WR
					var tip := WL + 24.0 if left else WR - 24.0
					draw_line(Vector2(x0, yy + 1), Vector2(tip, yy + 1), hot, 2.0)
					yy += 5.0
		"jaws":
			var j := Hz.jaws(e, t)
			var mid: float = (float(e.y0) + float(e.y1)) * 0.5
			var ext: float = maxf(j.x, 3.0)
			if cy and A.tex("traps/jaws_echo"):
				var x := WL
				while x < WR:
					_spr("traps/jaws_echo", 16, 24, 0, Vector2(x, mid - 12))
					x += 16
			elif A.tex("traps/jaws"):
				var hf := 2 if (j.y == 1 and _blink(10.0)) else 1
				var x := WL
				while x + 16.0 <= WL + ext - 16.0:
					_spr("traps/jaws", 16, 24, 0, Vector2(x, mid - 12))
					_spr("traps/jaws", 16, 24, 0, Vector2(WR + WL - x - 16.0, mid - 12), true)
					x += 16.0
				_spr("traps/jaws", 16, 24, hf, Vector2(WL + ext - 16.0, mid - 12))
				_spr("traps/jaws", 16, 24, hf, Vector2(WR - ext, mid - 12), true)
			else:
				draw_rect(Rect2(WL, mid - 10, ext, 20), hot)
				draw_rect(Rect2(WR - ext, mid - 10, ext, 20), hot)
		"grignon":
			var g := Hz.grignon_pos(e, t)
			var up: bool = Hz.grignon_pos(e, t + 0.02).y <= g.y
			if not _spr(_tn("gnawer", cy), 16, 16, 0 if cy else int(tg * 8.0) % 4, g - Vector2(8, 8), int(e.side) > 0, not up):
				draw_rect(Rect2(g - Vector2(4, 3), Vector2(8, 6)), hot)
		"moth":
			var m := Hz.moth_pos(e, t)
			if not _spr(_tn("moth", cy), 16, 16, 0 if cy else int(tg * 8.0) % 2, m - Vector2(8, 8)):
				draw_rect(Rect2(m - Vector2(4, 3), Vector2(8, 6)), hot)
		"rockfall":
			var ry := Hz.rock_y(e, t, w.st, w.tower.is_water(float(e.y)))
			var armed: bool = w.st.has(e.id) and ry <= float(e.y)
			var rx: float = float(e.x) + (1.0 if armed and _blink(30.0) else 0.0)
			if _spr(_tn("rockfall_books", cy), 16, 16, 0, Vector2(rx - 8, ry - 8)):
				if armed and not cy:
					_spr("traps/rockfall_mark", 16, 4, int(tg * 10.0) % 2, Vector2(float(e.x) - 8, ry + 6))
			else:
				draw_rect(Rect2(rx - 5, ry - 5, 10, 10), A.P.c if cy else A.P.s)
				if armed:
					draw_rect(Rect2(rx - 1, ry + 6, 2, 2), A.P.X)
		"power":
			if w.used.has(e.id):
				return
			var bf := int(w.t_global * 4.0) % 4
			var icon: String = {"burin": "fx/pu_burin", "plume": "fx/pu_plume", "accalmie": "fx/pu_calm"}.get(String(e.power), "")
			if icon != "" and _spr("fx/powerup_bubble", 16, 16, bf, e.pos - Vector2(8, 8)):
				_spr(icon, 8, 8, 0, e.pos - Vector2(8, 8) + Vector2(4, 4 + [0, 0, 1, 1][bf]))
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
			var at := Vector2(ax - 16, ay + 8 - 32)
			var abi := Tower.biome_index(int(e.m))
			var alt_env: String = {1: "env/altar_fonderie", 2: "env/altar_bibliotheque"}.get(abi, "")
			if alt_env != "" and A.tex(alt_env):
				draw_texture(A.tex(alt_env), at, Color(1, 1, 1) if on else Color(0.7, 0.7, 0.8))
				if on:
					_spr("env/altar_flame", 8, 16, int(w.t_global / 0.09) % 6, at + Vector2(12, -5))
				return
			if _spr("fx/altar", 32, 32, 1 if on else 0, at):
				if on:
					_spr("fx/altar_flame", 8, 16, int(w.t_global * 10.0) % 6, at + Vector2(12, -5))
				return
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
	var stun: bool = w.boss_stun > 0.0
	if A.tex("traps/boss_sonneur"):
		var n := int(anchor.distance_to(b) / 8.0)
		for k in n:
			_spr("traps/chain", 8, 8, 0, anchor.lerp(b, float(k) / float(maxi(n, 1))) - Vector2(4, 0))
		_spr("traps/boss_sonneur_yoke", 64, 16, 0, Vector2(96 - 32, mid - 56 - 13))
		var going_right: bool = cos(TAU * w.boss_t / 2.6) > 0.0
		var f := (3 if _blink(20.0) else 0) if stun else (0 if going_right else 1)
		_spr("traps/boss_sonneur", 48, 48, f, b - Vector2(24, 24))
	else:
		draw_line(anchor, b, A.P.l, 1.0)
		var body: Color = A.P.c if stun else A.P.U
		draw_colored_polygon(PackedVector2Array([b + Vector2(-8, -14), b + Vector2(8, -14), b + Vector2(18, 12), b + Vector2(-18, 12)]), body)
	# runes : la prochaine est allumée
	for i in w.boss_runes.size():
		var r: Dictionary = w.boss_runes[i]
		if i < w.boss_hits:
			_draw_rune(r, true)
		elif i == w.boss_hits:
			_draw_rune(r, _blink(4.0))
	var ws: Vector2 = w.wave_state()
	if A.tex("traps/boss_wave") and ws.y >= 0:
		var wf := -1
		if ws.y == 0 and _blink(10.0):
			wf = 0
		elif ws.y == 1:
			wf = 1 + int(w.t_global * 20.0) % 3
		if wf >= 0:
			var x := WL
			while x < WR:
				_spr("traps/boss_wave", 16, 8, wf, Vector2(x, ws.x - 3))
				x += 16
		return
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
		if s.big and _spr("fx/shard_big", 16, 16, int(w.t_global * 4.0) % 4, s.pos + Vector2(-8, -8 + bob)):
			continue
		if not s.big and _spr("fx/shard", 8, 8, int(w.t_global * 8.0 + s.id) % 6, s.pos + Vector2(-4, -4 + bob)):
			continue
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
			if pt.anim == "shard_pop" and A.tex("fx/shard_pop"):
				_spr("fx/shard_pop", 16, 16, mini(4, int(k * 5.0)), pt.p - Vector2(8, 8))
			elif pt.anim == "shard_pop":
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
	var crest := A.tex("tide/tide_crest")
	if crest:
		var y := roundf(ty) - 6.0
		var calm: bool = w.calm_t > 0.0
		var f := 0 if calm else int(w.t_global / 0.15) % 4
		for i in 6:
			_spr("tide/tide_glow", 32, 16, 0, Vector2(i * 32, y - 16), false, false, Color(0.75, 1.0, 1.0) if calm else Color.WHITE)
			_spr("tide/tide_crest", 32, 16, f, Vector2(i * 32, y))
		var yy := y + 16.0
		while yy < bot:
			for i in 6:
				_spr("tide/tide_body", 32, 32, 0, Vector2(i * 32, yy))
			yy += 32.0
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
