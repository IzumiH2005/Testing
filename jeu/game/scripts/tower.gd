class_name Tower
extends RefCounted
## Génère une tour déterministe à partir d'une graine.
## Coordonnées monde : y vers le bas, le dessus de la dalle de départ est à y = 0.
## 1 mètre = 1 tuile = 16 px.

const TILE := 16
const WALL_L := 32.0      # bord intérieur du mur gauche
const WALL_R := 160.0     # bord intérieur du mur droit
const SPIKE_DEPTH := 7.0

enum { SPIKES, SAW, LASER }

var seed_value: int
var rng := RandomNumberGenerator.new()
var traps: Array = []     # Dictionnaires, triés du bas vers le haut
var shards: Array = []    # {id, pos:Vector2}
var deco: Dictionary = {} # rangée (int, négative vers le haut) -> {"back": [indices de tuiles], "wall_l": i, "wall_r": i}
var cursor_y := -112.0    # prochain piège (px) ; les 7 premiers mètres sont libres
var generated_to := 0.0

func _init(s: int) -> void:
	seed_value = s
	rng.seed = s

func meters_at(y: float) -> int:
	return int(floor(-y / TILE))

## Garantit que la tour est générée jusqu'à y (valeur négative, plus haut = plus petit).
func ensure(y_top: float) -> void:
	while cursor_y > y_top - 400.0:
		_place_next()

func _difficulty(y: float) -> float:
	return clampf(float(meters_at(y)) / 260.0, 0.0, 1.0)

func _place_next() -> void:
	var y := cursor_y
	var m := meters_at(y)
	var d := _difficulty(y)
	var id := traps.size()
	# choix du type, pondéré par la hauteur
	var w_spk := 5.0
	var w_saw := 3.0 if m > 6 else 0.0
	var w_las := 3.0 if m > 22 else 0.0
	var pick := rng.randf() * (w_spk + w_saw + w_las)
	var trap := {"id": id, "y": y}
	var span := 0.0
	if pick < w_spk:
		var tiles := 2 + (rng.randi_range(0, 1) if m < 40 else rng.randi_range(0, 2))
		var side := -1 if rng.randf() < 0.5 else 1
		# un même mur ne doit pas être couvert deux fois de suite trop près
		trap.merge({"type": SPIKES, "side": side, "h": float(tiles * TILE)})
		span = tiles * TILE
		# à partir de 70 m : parfois des pics en face, décalés
		if m > 70 and rng.randf() < 0.35 + 0.25 * d:
			traps.append(trap)
			var off := float((tiles + 2 + rng.randi_range(0, 1)) * TILE)
			var t2 := {"id": traps.size(), "y": y - off, "type": SPIKES, "side": -side,
				"h": float((2 + rng.randi_range(0, 1)) * TILE)}
			trap = t2
			span += off
	elif pick < w_spk + w_saw:
		var lanes := [64.0, 96.0, 128.0]
		var cx: float = lanes[rng.randi_range(0, 2)]
		var mode := 0
		if m > 35 and rng.randf() < 0.4 + 0.4 * d:
			mode = 1  # va-et-vient horizontal
		elif m > 90 and rng.randf() < 0.35:
			mode = 2  # va-et-vient vertical
		var amp := 0.0
		var spd := 0.0
		if mode == 1:
			cx = 96.0
			amp = rng.randf_range(34.0, 52.0)
			spd = rng.randf_range(1.4, 2.0) + d * 1.2
		elif mode == 2:
			amp = rng.randf_range(18.0, 30.0)
			spd = rng.randf_range(1.6, 2.4) + d
		trap.merge({"type": SAW, "x": cx, "mode": mode, "amp": amp, "spd": spd,
			"phase": rng.randf() * TAU})
		span = 24.0 + amp * (1.0 if mode == 2 else 0.0)
	else:
		var period := rng.randf_range(2.8, 3.4) - d * 0.6
		trap.merge({"type": LASER, "side": -1 if rng.randf() < 0.5 else 1,
			"period": period, "on": 0.85 + d * 0.25, "warn": 0.7 - d * 0.15,
			"phase": rng.randf() * period})
		span = 16.0
	traps.append(trap)
	# éclats entre ce piège et le suivant
	var gap := lerpf(7.0, 4.0, d) * TILE + rng.randf_range(0.0, 2.0) * TILE
	var next_y := y - span - gap
	if rng.randf() < 0.75:
		var n := 1 if rng.randf() < 0.7 else 3
		var sx := rng.randf_range(56.0, 136.0)
		var sy := (y - span + next_y) * 0.5
		for i in n:
			shards.append({"id": shards.size(), "pos": Vector2(sx, sy - i * 12.0)})
	cursor_y = next_y

## Position de la scie au temps t (temps de la vie en cours).
static func saw_pos(trap: Dictionary, t: float) -> Vector2:
	var base := Vector2(trap.x, trap.y)
	match int(trap.mode):
		1:
			return base + Vector2(sin(t * trap.spd + trap.phase) * trap.amp, 0)
		2:
			return base + Vector2(0, sin(t * trap.spd + trap.phase) * trap.amp)
	return base

## État du laser : 0 éteint, 1 préavis, 2 actif.
static func laser_state(trap: Dictionary, t: float) -> int:
	var p: float = fmod(t + trap.phase, trap.period)
	var on_start: float = trap.period - trap.on
	if p >= on_start:
		return 2
	if p >= on_start - trap.warn:
		return 1
	return 0

## Décor déterministe d'une rangée (indépendant de la séquence des pièges).
func deco_for_row(row: int) -> Dictionary:
	if deco.has(row):
		return deco[row]
	var r := RandomNumberGenerator.new()
	r.seed = hash(Vector2i(seed_value, row))
	var back := []
	for i in 10:
		var v := r.randi_range(0, 3)
		var roll := r.randf()
		if roll < 0.012:
			v = 4   # fenêtre
		elif roll < 0.024:
			v = 6   # niche à rune
		elif roll < 0.034:
			v = 5   # chaîne
		back.append(v)
	var wl := r.randi_range(0, 3)
	var wr := r.randi_range(0, 3)
	if r.randf() < 0.10: wl = 4
	elif r.randf() < 0.06: wl = 5
	if r.randf() < 0.10: wr = 4
	elif r.randf() < 0.06: wr = 5
	var dd := {"back": back, "wl": wl, "wr": wr}
	deco[row] = dd
	return dd
