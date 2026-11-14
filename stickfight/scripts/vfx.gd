class_name Vfx
extends RefCounted
## Effets visuels dessinés à la main, en aplats, comme en pixel art :
## couleurs en nombre limité, pas de dégradé ni de transparence, chaque
## effet change d'image toutes les 2 images (« en deux ») pour garder un
## rythme sec. Tout dépend seulement de l'âge de l'effet : le même âge donne
## toujours le même dessin (rendus et tests reproductibles).
##
## Un effet : {type, pos: Vector2 (monde), age: int, dir: degrés (monde),
##             genre: "garde" | "coup", taille: facteur}
##
## etincelle  éclair de contact : flash blanc (0-1), étoile allongée dans la
##            direction du coup (2-3), anneau qui s'ouvre et traits (4-7),
##            éclats qui retombent (8-13).
## poussiere  petits nuages au sol quand un pied se pose ou glisse.

const PALETTES := {
	"garde": [Color("#ffffff"), Color("#d0ebff"), Color("#74c0fc"), Color("#1864ab")],
	"coup": [Color("#ffffff"), Color("#fff3bf"), Color("#ffa94d"), Color("#c2410c")],
}
const DUST := [Color("#f1e6e2"), Color("#cdbab5"), Color("#9f8b86")]
const LIFE := {"etincelle": 14, "poussiere": 18}

## Éclats : (écart d'angle en degrés, vitesse en unités par image, taille).
const SHARDS := [[-38.0, 2.6, 3.0], [-14.0, 3.4, 3.5], [8.0, 3.0, 3.0], [27.0, 2.4, 2.5],
	[52.0, 1.9, 2.5], [-62.0, 1.7, 2.0], [160.0, 1.3, 2.0], [-150.0, 1.5, 2.0]]
const STREAKS := [-55.0, -28.0, 0.0, 26.0, 50.0, 140.0, -135.0]


static func life(v: Dictionary) -> int:
	return LIFE.get(v.type, 12)


static func make(type: String, pos: Vector2, params := {}) -> Dictionary:
	var v := {"type": type, "pos": pos, "age": 0, "dir": float(params.get("dir", 0.0)),
		"genre": str(params.get("genre", "garde")), "taille": float(params.get("taille", 1.0))}
	return v


static func draw(ci: CanvasItem, v: Dictionary, origin: Vector2, scale: float) -> void:
	match v.type:
		"etincelle":
			_spark(ci, v, origin, scale)
		"poussiere":
			_dust(ci, v, origin, scale)


static func _dirv(deg: float) -> Vector2:
	return Vector2(cos(deg_to_rad(deg)), sin(deg_to_rad(deg)))


static func _scr(w: Vector2, origin: Vector2, scale: float) -> Vector2:
	return StickRig.to_screen(w, origin, scale)


## Étoile à 4 branches : 2 longues dans l'axe du coup, 2 courtes en travers.
static func _star(ci: CanvasItem, c: Vector2, dir: float, long: float, short: float, thick: float, col: Color, origin: Vector2, scale: float) -> void:
	var pts := PackedVector2Array()
	var radii := [long, short, long * 0.7, short]
	for k in 4:
		var a := dir + k * 90.0
		pts.append(_scr(c + _dirv(a) * radii[k], origin, scale))
		pts.append(_scr(c + _dirv(a + 45.0) * thick, origin, scale))
	ci.draw_colored_polygon(pts, col)


static func _ring(ci: CanvasItem, c: Vector2, r: float, w: float, col: Color, origin: Vector2, scale: float) -> void:
	ci.draw_arc(_scr(c, origin, scale), r * scale, 0.0, TAU, 28, col, maxf(1.0, w * scale), false)


static func _square(ci: CanvasItem, c: Vector2, s: float, col: Color, origin: Vector2, scale: float) -> void:
	var p := _scr(c, origin, scale)
	var h := s * scale / 2.0
	ci.draw_rect(Rect2(p - Vector2(h, h), Vector2(2 * h, 2 * h)), col)


static func _spark(ci: CanvasItem, v: Dictionary, origin: Vector2, scale: float) -> void:
	var pal: Array = PALETTES.get(v.genre, PALETTES.garde)
	var a: int = int(v.age) - int(v.age) % 2
	var k: float = v.taille
	var c: Vector2 = v.pos
	var d: float = v.dir
	if a == 0:
		# Image de flash : gros disque blanc cerclé, étoile pleine.
		ci.draw_circle(_scr(c, origin, scale), 13.0 * k * scale, pal[3])
		ci.draw_circle(_scr(c, origin, scale), 11.0 * k * scale, pal[1])
		_star(ci, c, d, 30.0 * k, 17.0 * k, 5.0 * k, pal[2], origin, scale)
		_star(ci, c, d, 24.0 * k, 12.0 * k, 3.5 * k, pal[0], origin, scale)
		ci.draw_circle(_scr(c, origin, scale), 7.0 * k * scale, pal[0])
	elif a == 2:
		_ring(ci, c, 15.0 * k, 3.0 * k, pal[2], origin, scale)
		_star(ci, c, d, 34.0 * k, 15.0 * k, 3.5 * k, pal[2], origin, scale)
		_star(ci, c, d, 28.0 * k, 10.0 * k, 2.0 * k, pal[0], origin, scale)
	elif a <= 6:
		var u := (a - 4) / 2.0  # 0 puis 1
		_ring(ci, c, (20.0 + 7.0 * u) * k, (2.5 - u) * k, pal[2] if u == 0 else pal[3], origin, scale)
		for s in STREAKS:
			var dv := _dirv(d + s)
			var r0 := (14.0 + 9.0 * u) * k
			var r1 := (26.0 + 8.0 * u) * k * (1.0 if absf(s) < 90.0 else 0.6)
			ci.draw_line(_scr(c + dv * r0, origin, scale), _scr(c + dv * r1, origin, scale), pal[1] if u == 0 else pal[2], maxf(1.0, (2.2 - u) * k * scale))
	else:
		for sh in SHARDS:
			var dv: Vector2 = _dirv(d + float(sh[0])) * float(sh[1]) * k
			var t := float(a)
			var p: Vector2 = c + dv * t + Vector2(0, -0.12) * t * t
			var size: float = sh[2] * k * (1.0 if a < 10 else 0.6)
			_square(ci, p, size + 1.2, pal[3], origin, scale)
			_square(ci, p, size, pal[1] if a < 10 else pal[2], origin, scale)


static func _dust(ci: CanvasItem, v: Dictionary, origin: Vector2, scale: float) -> void:
	var a: int = int(v.age) - int(v.age) % 2
	var k: float = v.taille
	var c: Vector2 = Vector2(v.pos.x, 0.0)
	var sens := 1.0 if _dirv(v.dir).x >= 0.0 else -1.0
	# Trois bouffées : deux qui fuient au ras du sol, une qui monte un peu.
	var puffs := [[sens * 1.0, 0.9, 1.0], [-sens * 1.0, 0.55, 0.8], [sens * 0.3, 0.3, 0.7]]
	for i in puffs.size():
		var pf: Array = puffs[i]
		var t := float(a)
		var x: float = c.x + pf[0] * (5.0 + t * 1.3 * pf[1]) * k
		var y: float = (2.0 + t * 0.35 + (1.0 if i == 2 else 0.0) * t * 0.3) * k
		var grow := clampf(t / 6.0, 0.0, 1.0)
		var shrink := clampf((float(LIFE.poussiere) - t) / 8.0, 0.0, 1.0)
		var r: float = (2.5 + 4.5 * grow) * shrink * pf[2] * k
		if r < 0.8:
			continue
		var p := _scr(Vector2(x, y), origin, scale)
		ci.draw_circle(p, (r + 1.0) * scale, DUST[2])
		ci.draw_circle(p, r * scale, DUST[1] if a >= 10 else DUST[0])
