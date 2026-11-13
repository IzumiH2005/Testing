class_name Tower
extends RefCounted
## Tour d'une ascension : assemble des chunks d'auteur (GDD 8.3) à partir d'une graine
## et les traduit en entités de jeu.
## Coordonnées monde : y vers le bas, le dessus du sol de départ est à y = 0.
## 1 mètre = 1 tuile = 16 px. La rangée de mètre m couvre y ∈ [-(m+1)·16, -m·16].

const TILE := 16
const WALL_L := 32.0      # face intérieure du mur gauche
const WALL_R := 160.0     # face intérieure du mur droit
const SPIKE_DEPTH := 7.0
const BUTTRESS_W := 16.0
const BUCKET := 64.0

## Biomes : altitude de début (m). Au-delà de B3, pas encore de chunks dédiés : remix.
const BIOMES := [
	{"id": "B1", "start": 0, "cap": 28.0},
	{"id": "B2", "start": 150, "cap": 34.0},
	{"id": "B3", "start": 350, "cap": 40.0},
	{"id": "B4", "start": 600, "cap": 46.0},
	{"id": "B5", "start": 900, "cap": 52.0},
	{"id": "B6", "start": 1250, "cap": 58.0},
]
const CYCLE := ["M", "M", "P", "R"]
const POWERS := ["burin", "plume", "accalmie"]

var seed_value: int
var rng := RandomNumberGenerator.new()
var ents: Array = []          # toutes les entités (Dictionary), id = index
var shards: Array = []        # {id, pos, big}
var water := {}               # mètre -> true
var altars: Array = []        # {id, y, m, biome}
var placed: Array = []        # {id, m0, h, mirror, biome, tension, D}
var deco := {}
var cursor_m := 0             # prochain mètre libre
var _buckets := {}            # int -> Array d'ids
var _recent: Array = []
var _cycle_i := 0
var _biome_i := -1
var _intros_left: Array = []
var _arena_done := {}
var _last_power_m := -999
var _burins := 0
var _uid := 0

func _init(s: int) -> void:
	seed_value = s
	rng.seed = s

static func meters_at(y: float) -> int:
	return int(floor(-y / TILE))

static func biome_index(m: int) -> int:
	var b := 0
	for i in BIOMES.size():
		if m >= BIOMES[i].start:
			b = i
	return b

func biome_at(y: float) -> String:
	return BIOMES[biome_index(meters_at(y))].id

## Plafond de vitesse de la marée selon le biome (GDD 8.6).
func tide_cap(y: float) -> float:
	return BIOMES[biome_index(meters_at(y))].cap

## Garantit que la tour est assemblée jusqu'à y (négatif, plus haut = plus petit).
func ensure(y_top: float) -> void:
	while -float(cursor_m * TILE) > y_top - 400.0:
		_place_next()

# ------------------------------------------------------------------ assemblage

func _d_target(m: int) -> float:
	var d := 2.0 + 6.0 * pow(float(m) / 1250.0, 0.8)
	var bi := biome_index(m)
	var b0: int = BIOMES[bi].start
	var b1: int = BIOMES[bi + 1].start if bi + 1 < BIOMES.size() else 99999
	if m - b0 < 20:
		d -= 1.5
	elif b1 - m < 30:
		d += 1.0
	if m > 1600:
		d += 1.0
	return d

func _pool(biome: String) -> Array:
	var out := []
	for c in ChunkLib.all():
		if c.biome == biome:
			out.append(c)
	return out

func _has_altar(c: Dictionary) -> bool:
	for r in c.rows:
		if "A" in r:
			return true
	return false

func _enter_biome(bi: int) -> void:
	_biome_i = bi
	_cycle_i = 0
	var bid: String = BIOMES[bi].id
	var pool := _pool(bid)
	_intros_left.clear()
	var entry := {}
	for c in pool:
		if c.tension == "I":
			if entry.is_empty() and _has_altar(c):
				entry = c
			else:
				_intros_left.append(c)
	_intros_left.sort_custom(func(a, b): return a.alt_min < b.alt_min)
	if not entry.is_empty():
		_put(entry)
	else:
		_put(_synthetic_altar(bid))

func _synthetic_altar(bid: String) -> Dictionary:
	var rows := PackedStringArray()
	var params := []
	for i in 6:
		rows.append("##...A....##" if i == 3 else "##........##")
		params.append({})
	return {"id": "autel_" + bid.to_lower(), "biome": bid, "tension": "I", "D": 0, "entree": "any",
		"sortie": "any", "verbe": "bond", "intro": "", "alt_min": 0, "alt_max": 99999, "poids": 1.0,
		"rows": rows, "params": params, "h": 6, "src": "synthétique"}

func _place_next() -> void:
	var bi := biome_index(cursor_m)
	if bi != _biome_i:
		_enter_biome(bi)
		return
	var bid: String = BIOMES[bi].id
	var pool := _pool(bid)
	var remix := pool.is_empty()
	if remix:
		pool = ChunkLib.all()
	var next_start: int = BIOMES[bi + 1].start if bi + 1 < BIOMES.size() else 99999
	# arène de boss en fin de biome
	if not _arena_done.has(bid):
		for c in pool:
			if c.tension == "A" and c.biome == bid and cursor_m + c.h >= next_start - 2:
				_arena_done[bid] = true
				_put(c)
				return
	# introductions dues
	if not _intros_left.is_empty() and cursor_m >= int(_intros_left[0].alt_min) - 4:
		_put(_intros_left.pop_front())
		return
	var tension: String = CYCLE[_cycle_i % CYCLE.size()]
	_cycle_i += 1
	var dt := _d_target(cursor_m) + (1.0 if remix else 0.0)
	var pick := _choose(pool, tension, dt, 1.0, not remix)
	if pick.is_empty():
		pick = _choose(pool, tension, dt, 2.0, not remix)
	if pick.is_empty():
		pick = _choose(pool, "R", dt, 99.0, not remix)
	if pick.is_empty():
		pick = _choose(pool, "", dt, 99.0, false)
	if pick.is_empty():
		_recent.clear()
		pick = _choose(pool, "", dt, 99.0, false)
	if pick.is_empty():
		pick = _synthetic_altar(bid)
		pick.rows[3] = "##........##"
		if OS.is_debug_build():
			print("Tower : aucun chunk pour ", bid, " ", tension, " m=", cursor_m)
	_put(pick)

func _choose(pool: Array, tension: String, dt: float, tol: float, use_alt: bool) -> Dictionary:
	var cands := []
	var total := 0.0
	for c in pool:
		if c.tension == "I" or c.tension == "A":
			continue
		if tension != "" and c.tension != tension:
			continue
		if absf(float(c.D) - dt) > tol:
			continue
		if use_alt and (cursor_m < int(c.alt_min) or cursor_m > int(c.alt_max)):
			continue
		if c.id in _recent:
			continue
		cands.append(c)
		total += float(c.poids)
	if cands.is_empty():
		return {}
	var r := rng.randf() * total
	for c in cands:
		r -= float(c.poids)
		if r <= 0.0:
			return c
	return cands.back()

var _exit_side := "L"

func _put(c: Dictionary) -> void:
	var mirror := false
	var ent: String = c.entree
	if ent == "L" or ent == "R":
		if _exit_side == "L" or _exit_side == "R":
			mirror = ent != _exit_side
		else:
			mirror = rng.randf() < 0.5
	else:
		mirror = rng.randf() < 0.5
	var sortie: String = c.sortie
	if sortie == "L" or sortie == "R":
		_exit_side = ChunkLib.flip_side(sortie) if mirror else sortie
	else:
		_exit_side = "any"
	var rows: PackedStringArray = ChunkLib.mirrored_rows(c) if mirror else c.rows
	var m0 := cursor_m
	placed.append({"id": c.id, "m0": m0, "h": c.h, "mirror": mirror, "biome": BIOMES[biome_index(m0)].id,
		"tension": c.tension, "D": c.D})
	_recent.append(c.id)
	if _recent.size() > 8:
		_recent.pop_front()
	_extract(c, rows, m0)
	cursor_m += int(c.h)

# ------------------------------------------------------------------ extraction des entités

func _row_m(h: int, i: int, m0: int) -> int:
	return m0 + (h - 1 - i)

static func row_top(m: int) -> float:
	return -float(m + 1) * TILE

static func row_mid(m: int) -> float:
	return -(float(m) + 0.5) * TILE

static func col_mid(col: int) -> float:
	return float(col) * TILE + 8.0

func _add(e: Dictionary) -> Dictionary:
	e["id"] = ents.size()
	ents.append(e)
	var y0: float = e.get("ry0", e.get("y0", 0.0))
	var y1: float = e.get("ry1", e.get("y1", 0.0))
	for b in range(int(floor(y0 / BUCKET)), int(floor(y1 / BUCKET)) + 1):
		if not _buckets.has(b):
			_buckets[b] = []
		_buckets[b].append(e.id)
	return e

## Entités dont l'étendue verticale touche [y_top, y_bot].
func near(y_top: float, y_bot: float) -> Array:
	var seen := {}
	var out := []
	for b in range(int(floor(y_top / BUCKET)), int(floor(y_bot / BUCKET)) + 1):
		if _buckets.has(b):
			for id in _buckets[b]:
				if not seen.has(id):
					seen[id] = true
					out.append(ents[id])
	return out

func _merged(params: Array, i0: int, i1: int) -> Dictionary:
	var p := {}
	for i in range(i1, i0 - 1, -1):
		p.merge(params[i], true)
	# priorité à la rangée du haut (i0)
	p.merge(params[i0], true)
	return p

func _phase(p: Dictionary) -> float:
	return float(p.phase) if p.has("phase") else rng.randf()

func _extract(c: Dictionary, rows: PackedStringArray, m0: int) -> void:
	var h: int = c.h
	var params: Array = c.params
	var used := {}  # "i,col" déjà consommé
	var bid: String = BIOMES[biome_index(m0)].id
	var arena := {}
	if c.tension == "A":
		arena = {"kind": "arena", "boss": bid, "y0": row_top(m0 + h - 1), "y1": -float(m0) * TILE, "runes": []}
	for i in h:
		var row: String = rows[i]
		var m := _row_m(h, i, m0)
		var p: Dictionary = params[i]
		var y_mid := row_mid(m)
		if "~" in row:
			water[m] = true
		# laser : un seul faisceau par rangée
		if row[0] == "L" or row[1] == "L" or row[10] == "L" or row[11] == "L":
			var period := ChunkLib.pf(p, "period", 3.1)
			_add({"kind": "laser", "y": y_mid, "y0": y_mid - 6, "y1": y_mid + 6, "period": period,
				"on": ChunkLib.pf(p, "on", 0.9), "warn": maxf(0.25, ChunkLib.pf(p, "warn", 0.7)),
				"phase": _phase(p) * period})
		for col in W():
			var ch: String = row[col]
			var key := "%d,%d" % [i, col]
			if used.has(key):
				continue
			match ch:
				">", "<", "C", "H", "f":
					# bande verticale : rangées consécutives du même caractère dans cette colonne
					var j := i
					while j + 1 < h and rows[j + 1][col] == ch:
						j += 1
						used["%d,%d" % [j, col]] = true
					var side := -1 if col < 6 else 1
					if ch == ">":
						side = -1
					elif ch == "<":
						side = 1
					var y0 := row_top(_row_m(h, i, m0))
					var y1 := row_top(_row_m(h, j, m0)) + TILE
					var bp := _merged(params, i, j)
					match ch:
						">", "<":
							_add({"kind": "spikes", "side": side, "y0": y0, "y1": y1})
						"C":
							_add({"kind": "buttress", "side": side, "y0": y0, "y1": y1})
						"H":
							_add({"kind": "herse", "side": side, "y0": y0, "y1": y1,
								"period": ChunkLib.pf(bp, "period", 2.4), "out": ChunkLib.pf(bp, "out", 0.9),
								"warn": maxf(0.25, ChunkLib.pf(bp, "warn", 0.3)), "phase": _phase(bp) * ChunkLib.pf(bp, "period", 2.4)})
						"f":
							_add({"kind": "friable", "side": side, "y0": y0, "y1": y1})
				"M":
					if col < 6:
						var j2 := i
						while j2 + 1 < h and rows[j2 + 1][col] == "M":
							j2 += 1
							used["%d,%d" % [j2, col]] = true
						var bp2 := _merged(params, i, j2)
						var per := ChunkLib.pf(bp2, "period", 3.0)
						_add({"kind": "jaws", "y0": row_top(_row_m(h, i, m0)), "y1": row_top(_row_m(h, j2, m0)) + TILE,
							"period": per, "phase": _phase(bp2) * per})
						# les M du mur droit appartiennent au même piège
						for k in range(i, j2 + 1):
							for cc in range(6, 12):
								if rows[k][cc] == "M":
									used["%d,%d" % [k, cc]] = true
				"S":
					_add_saw(rows, params, i, col, m0, h, used)
				"P":
					var ln := ChunkLib.pf(p, "len", 48.0)
					var anc := Vector2(col_mid(col), row_top(m))
					_add({"kind": "pendulum", "anchor": anc, "len": ln, "amp": deg_to_rad(ChunkLib.pf(p, "amp", 50.0)),
						"period": ChunkLib.pf(p, "period", 2.2), "phase": _phase(p), "r": ChunkLib.pf(p, "r", 5.0),
						"y0": anc.y - 8, "y1": anc.y + ln + 12, "ry0": anc.y - 8, "ry1": anc.y + ln + 12})
				"g":
					var a := i
					var b := i
					while a - 1 >= 0 and rows[a - 1][col] in [":", "g"]:
						a -= 1
					while b + 1 < h and rows[b + 1][col] in [":", "g"]:
						b += 1
					var ya := row_top(_row_m(h, a, m0)) + 4.0
					var yb := row_top(_row_m(h, b, m0)) + TILE - 4.0
					_add({"kind": "grignon", "side": -1 if col < 6 else 1, "ya": ya, "yb": yb,
						"start": y_mid, "spd": ChunkLib.pf(p, "spd", 24.0), "y0": ya - 6, "y1": yb + 6})
				"m":
					_add({"kind": "moth", "y": y_mid, "x0": col_mid(col), "spd": ChunkLib.pf(p, "spd", 40.0),
						"dir": int(ChunkLib.pf(p, "dir", 1.0 if rng.randf() < 0.5 else -1.0)),
						"y0": y_mid - 14, "y1": y_mid + 14})
				"b":
					_add({"kind": "rockfall", "x": col_mid(col), "y": y_mid, "y0": y_mid - 8, "y1": y_mid + 8,
						"ry1": y_mid + 400.0})
				"o":
					if rng.randf() < 0.72:
						shards.append({"id": shards.size(), "pos": Vector2(col_mid(col), y_mid), "big": false})
				"O":
					shards.append({"id": shards.size(), "pos": Vector2(col_mid(col), y_mid), "big": true})
				"*":
					if m - _last_power_m >= 45:
						_last_power_m = m
						var choices := POWERS.duplicate()
						if _burins >= 2:
							choices.erase("burin")
						var pw: String = choices[rng.randi_range(0, choices.size() - 1)]
						if pw == "burin":
							_burins += 1
						_add({"kind": "power", "power": pw, "pos": Vector2(col_mid(col), y_mid),
							"y0": y_mid - 8, "y1": y_mid + 8})
				"A":
					var al := _add({"kind": "altar", "y": y_mid, "m": m, "x": col_mid(col), "biome": bid,
						"y0": y_mid - 24, "y1": y_mid + 8})
					altars.append(al)
				"R":
					var ru := _add({"kind": "rune", "side": -1 if col < 6 else 1, "y": y_mid,
						"y0": y_mid - 8, "y1": y_mid + 8, "order": 0})
					if not arena.is_empty():
						arena.runes.append(ru.id)
				"?":
					_add({"kind": "secret", "side": -1 if col < 6 else 1, "y": y_mid, "y0": y_mid - 8, "y1": y_mid + 8})
	if not arena.is_empty():
		# runes dans l'ordre de hauteur (du bas vers le haut)
		arena.runes.sort_custom(func(a, b): return ents[a].y > ents[b].y)
		for k in arena.runes.size():
			ents[arena.runes[k]].order = k
		_add(arena)

func W() -> int:
	return ChunkLib.W

func _add_saw(rows: PackedStringArray, params: Array, i: int, col: int, m0: int, h: int, used: Dictionary) -> void:
	var row: String = rows[i]
	var p: Dictionary = params[i]
	var m := _row_m(h, i, m0)
	var base := Vector2(col_mid(col) + ChunkLib.pf(p, "dx", 0.0), row_mid(m) + ChunkLib.pf(p, "dy", 0.0))
	var axis := 0
	var a := 0.0
	var b := 0.0
	# rail horizontal
	var l := col
	var r := col
	while l - 1 >= 2 and row[l - 1] in ["-", "S"]:
		l -= 1
	while r + 1 <= 9 and row[r + 1] in ["-", "S"]:
		r += 1
	if r > l:
		axis = 1
		a = col_mid(l)
		b = col_mid(r)
		for cc in range(l, r + 1):
			used["%d,%d" % [i, cc]] = true
	else:
		var t := i
		var d := i
		while t - 1 >= 0 and rows[t - 1][col] in ["|", "S"]:
			t -= 1
		while d + 1 < h and rows[d + 1][col] in ["|", "S"]:
			d += 1
		if d > t:
			axis = 2
			a = row_mid(_row_m(h, t, m0))
			b = row_mid(_row_m(h, d, m0))
			for k in range(t, d + 1):
				used["%d,%d" % [k, col]] = true
			p = _merged(params, t, d)
	var spd := ChunkLib.pf(p, "spd", 1.7)
	var e := {"kind": "saw", "c": base, "axis": axis, "a": a, "b": b, "spd": spd, "phase": _phase(p) * TAU,
		"r": ChunkLib.pf(p, "r", 6.0)}
	if axis == 2:
		e.y0 = minf(a, b) - 10.0
		e.y1 = maxf(a, b) + 10.0
	else:
		e.y0 = base.y - 10.0
		e.y1 = base.y + 10.0
	_add(e)

# ------------------------------------------------------------------ requêtes géométriques

func is_water(y: float) -> bool:
	return water.has(meters_at(y))

## Face accrochable du mur `side` à la hauteur y : x de la face (contreforts compris).
func wall_face(side: int, y: float) -> float:
	for e in near(y - 1.0, y + 1.0):
		if e.kind == "buttress" and e.side == side and y >= e.y0 and y <= e.y1:
			return WALL_L + BUTTRESS_W if side < 0 else WALL_R - BUTTRESS_W
	return WALL_L if side < 0 else WALL_R

## Décor déterministe d'une rangée (indépendant de la séquence des pièges).
func deco_for_row(row: int) -> Dictionary:
	if deco.has(row):
		return deco[row]
	var r := RandomNumberGenerator.new()
	r.seed = hash(Vector2i(seed_value, row))
	var back := []
	for i in 8:
		var v := r.randi_range(0, 3)
		if i > 0 and v == back[i - 1]:
			v = (v + 1 + r.randi_range(0, 2)) % 4
		back.append(v)
	if posmod(row, 3) == 0:
		var roll := r.randf()
		var col := r.randi_range(0, 7)
		if roll < 0.20:
			back[col] = 4
		elif roll < 0.42:
			back[col] = 5
		elif roll < 0.55:
			back[col] = 6
	var wl := r.randi_range(0, 3)
	var wr := r.randi_range(0, 3)
	if r.randf() < 0.10: wl = 4
	elif r.randf() < 0.06: wl = 5
	if r.randf() < 0.10: wr = 4
	elif r.randf() < 0.06: wr = 5
	var dd := {"back": back, "wl": wl, "wr": wr}
	deco[row] = dd
	return dd
