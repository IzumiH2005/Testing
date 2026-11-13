class_name Hz
extends RefCounted
## Géométrie des dangers en fonction du temps de la vie (GDD 4.3).
## Tout est déterministe en t (chaque vie rejoue le même temps), sauf l'éboulis
## et la plaque friable dont l'état dépend du joueur (dictionnaire `st` par vie).

const WL := Tower.WALL_L
const WR := Tower.WALL_R
const FROLE := 3.0

# ------------------------------------------------------------------ cycles

## Laser : 0 éteint, 1 préavis, 2 allumé. Le préavis précède l'allumage.
static func laser_state(e: Dictionary, t: float) -> int:
	var u := fposmod(t + float(e.phase), float(e.period))
	if u < float(e.warn):
		return 1
	if u < float(e.warn) + float(e.on):
		return 2
	return 0

## Herse : 0 rentrée, 1 préavis, 2 sortie.
static func herse_state(e: Dictionary, t: float) -> int:
	var per: float = e.period
	var u := fposmod(t + float(e.phase), per)
	var rest := per - float(e.out) - float(e.warn)
	if u < rest:
		return 0
	if u < rest + float(e.warn):
		return 1
	return 2

## Mâchoires : avancée de chaque mâchoire depuis son mur (0 à 64 px) et phase.
## Cycle 3,0 s : ouvert 1,6 / préavis 0,5 / fermeture 0,15 / fermé 0,45 / réouverture 0,3.
static func jaws(e: Dictionary, t: float) -> Vector2:
	var per: float = e.period
	var k := per / 3.0
	var u := fposmod(t + float(e.phase), per) / k
	if u < 1.6:
		return Vector2(0.0, 0)
	if u < 2.1:
		return Vector2(1.0, 1)
	if u < 2.25:
		return Vector2(64.0 * (u - 2.1) / 0.15, 2)
	if u < 2.7:
		return Vector2(64.0, 2)
	return Vector2(64.0 * (1.0 - (u - 2.7) / 0.3), 2)

static func saw_pos(e: Dictionary, t: float) -> Vector2:
	var c: Vector2 = e.c
	if int(e.axis) == 0:
		return c
	var k := 0.5 + 0.5 * sin(float(e.spd) * t + float(e.phase))
	if int(e.axis) == 1:
		return Vector2(lerpf(e.a, e.b, k), c.y)
	return Vector2(c.x, lerpf(e.a, e.b, k))

static func pendulum_pos(e: Dictionary, t: float) -> Vector2:
	var th: float = float(e.amp) * sin(TAU * t / float(e.period) + float(e.phase) * TAU)
	return Vector2(e.anchor) + Vector2(sin(th), cos(th)) * float(e.len)

static func _pingpong(s: float, l: float) -> float:
	if l <= 0.0:
		return 0.0
	var u := fposmod(s, 2.0 * l)
	return u if u < l else 2.0 * l - u

static func grignon_pos(e: Dictionary, t: float) -> Vector2:
	var l: float = float(e.yb) - float(e.ya)
	var y: float = float(e.ya) + _pingpong(float(e.start) - float(e.ya) + float(e.spd) * t, l)
	var x := WL + 4.0 if int(e.side) < 0 else WR - 4.0
	return Vector2(x, y)

static func moth_pos(e: Dictionary, t: float) -> Vector2:
	var x0 := WL + 5.0
	var l := WR - WL - 10.0
	var x := x0 + _pingpong(float(e.x0) - x0 + float(e.dir) * float(e.spd) * t, l)
	return Vector2(x, float(e.y) + 8.0 * sin(TAU * t / 1.5))

## Éboulis : y courant (nan si pas encore déclenché).
static func rock_y(e: Dictionary, t: float, st: Dictionary, water: bool) -> float:
	if not st.has(e.id):
		return float(e.y)
	var dt := t - float(st[e.id]) - 0.6
	if dt <= 0.0:
		return float(e.y)
	return float(e.y) + dt * (180.0 if water else 300.0)

# ------------------------------------------------------------------ formes létales

## Formes létales de l'entité à l'instant t : Array de Rect2 ou de Vector3(x, y, rayon).
static func shapes(e: Dictionary, t: float, st: Dictionary, tower: Tower) -> Array:
	match String(e.kind):
		"spikes":
			var x0: float = WL if int(e.side) < 0 else WR - 5.0
			return [Rect2(x0, float(e.y0) + 2.0, 5.0, float(e.y1) - float(e.y0) - 4.0)]
		"buttress":
			var bx: float = WL if int(e.side) < 0 else WR - Tower.BUTTRESS_W
			return [Rect2(bx + 2.0, float(e.y0) - 5.0, Tower.BUTTRESS_W - 4.0, 5.0),
				Rect2(bx + 2.0, float(e.y1), Tower.BUTTRESS_W - 4.0, 5.0)]
		"saw":
			var p := saw_pos(e, t)
			return [Vector3(p.x, p.y, float(e.r))]
		"pendulum":
			var q := pendulum_pos(e, t)
			return [Vector3(q.x, q.y, float(e.r))]
		"laser":
			if laser_state(e, t) == 2:
				return [Rect2(WL, float(e.y) - 2.0, WR - WL, 4.0)]
		"herse":
			if herse_state(e, t) == 2:
				var hx: float = WL if int(e.side) < 0 else WR - 24.0
				return [Rect2(hx, float(e.y0) + 2.0, 24.0, float(e.y1) - float(e.y0) - 4.0)]
		"jaws":
			var j := jaws(e, t)
			if j.y == 2 and j.x > 3.0:
				var mid: float = (float(e.y0) + float(e.y1)) * 0.5
				return [Rect2(WL, mid - 10.0, j.x, 20.0), Rect2(WR - j.x, mid - 10.0, j.x, 20.0)]
		"grignon":
			var g := grignon_pos(e, t)
			return [Rect2(g.x - 4.0, g.y - 3.0, 8.0, 6.0)]
		"moth":
			var m := moth_pos(e, t)
			return [Rect2(m.x - 4.0, m.y - 3.0, 8.0, 6.0)]
		"rockfall":
			var ry := rock_y(e, t, st, tower.is_water(float(e.y)))
			if ry > float(e.y):
				return [Rect2(float(e.x) - 5.0, ry - 5.0, 10.0, 10.0)]
	return []

## 0 rien, 1 frôlé (≤ 3 px), 2 touché.
static func test(e: Dictionary, t: float, st: Dictionary, tower: Tower, box: Rect2) -> int:
	var best := 0
	for s in shapes(e, t, st, tower):
		if s is Rect2:
			if s.intersects(box):
				return 2
			if s.grow(FROLE).intersects(box):
				best = 1
		else:
			var c := Vector2(s.x, s.y)
			var q := Vector2(clampf(c.x, box.position.x, box.end.x), clampf(c.y, box.position.y, box.end.y))
			var d := q.distance_to(c)
			if d < s.z:
				return 2
			if d < s.z + FROLE:
				best = 1
	return best

## Centre visuel d'une entité (gravure, particules, caméra).
static func center(e: Dictionary, t: float, st: Dictionary, tower: Tower) -> Vector2:
	match String(e.kind):
		"spikes", "buttress", "herse", "friable":
			var x: float = WL + 6.0 if int(e.side) < 0 else WR - 6.0
			return Vector2(x, (float(e.y0) + float(e.y1)) * 0.5)
		"saw":
			return saw_pos(e, t)
		"pendulum":
			return pendulum_pos(e, t)
		"laser":
			return Vector2(96.0, float(e.y))
		"jaws":
			return Vector2(96.0, (float(e.y0) + float(e.y1)) * 0.5)
		"grignon":
			return grignon_pos(e, t)
		"moth":
			return moth_pos(e, t)
		"rockfall":
			return Vector2(float(e.x), rock_y(e, t, st, false))
	return Vector2(96.0, float(e.get("y", 0.0)))

const LETHAL := ["spikes", "buttress", "saw", "pendulum", "laser", "herse", "jaws", "grignon", "moth", "rockfall"]
