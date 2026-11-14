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
## vitesse    lignes de vitesse : traits horizontaux laissés sur place dans
##            l'arène ; le coureur s'en éloigne, ils se rétractent vers
##            l'arrière (dir = sens de la course, les traits partent à l'opposé).
## onde       onde de choc au sol (décollage ou atterrissage en force) : flash
##            blanc d'une image (0-1), anneau aplati qui s'élargit (2-15), en
##            passant du blanc au gris, puis se troue par morceaux ; quelques
##            éclats de sol sautent aux deux bouts. dir penche l'onde : elle
##            s'étend plus loin du côté de dir (−90 = symétrique).
## choc       ondes d'air laissées sur place au point de départ d'une
##            propulsion : trois croissants bombés vers dir (sens du vol), du
##            plus large au plus petit, qui s'ouvrent, s'amincissent et se
##            brisent pendant que le corps s'en éloigne.

const PALETTES := {
	"garde": [Color("#ffffff"), Color("#d0ebff"), Color("#74c0fc"), Color("#1864ab")],
	"coup": [Color("#ffffff"), Color("#fff3bf"), Color("#ffa94d"), Color("#c2410c")],
}
const DUST := [Color("#f1e6e2"), Color("#cdbab5"), Color("#9f8b86")]
const LIFE := {"etincelle": 14, "poussiere": 18, "vitesse": 10, "onde": 18, "choc": 14}
## Air comprimé : même famille que les lignes de vitesse (blanc froid → gris).
const AIR := [Color("#ffffff"), Color("#e9ecef"), Color("#adb5bd"), Color("#495057")]
## Ordre dans lequel les morceaux d'un trait s'effacent (des trous qui grandissent).
const HOLES := [5, 1, 9, 3, 7, 0, 10, 4, 8, 2, 11, 6]
## Éclats de sol de l'onde : (angle depuis l'horizontale, vitesse, taille), par groupe de 3.
const CHIPS := [[58.0, 2.3, 3.0], [40.0, 2.9, 2.5], [72.0, 1.7, 2.0]]
const SPEED := Color("#f8f9fa")
const SPEED_EDGE := Color("#495057")
## Traits : (hauteur relative, recul du départ, longueur).
const LINES := [[16.0, 6.0, 46.0], [2.0, 0.0, 62.0], [-14.0, 10.0, 38.0], [-30.0, 18.0, 28.0]]

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


## Calques : `draw` est appelé deux fois par image, avant les combattants
## (layer = "derriere") et après (layer = "devant"). Le choc passe entièrement
## derrière le corps ; l'onde met la moitié du fond de son anneau derrière
## les jambes et la moitié de devant par-dessus. Le reste est devant.
static func draw(ci: CanvasItem, v: Dictionary, origin: Vector2, scale: float, layer := "devant") -> void:
	if v.type == "choc":
		if layer == "derriere":
			_boom(ci, v, origin, scale)
		return
	if v.type == "onde":
		_wave(ci, v, origin, scale, layer)
		return
	if layer != "devant":
		return
	match v.type:
		"etincelle":
			_spark(ci, v, origin, scale)
		"poussiere":
			_dust(ci, v, origin, scale)
		"vitesse":
			_speed(ci, v, origin, scale)


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


## Traits fixes dans l'arène : la tête du trait (côté coureur) rattrape la
## queue, en deux images, jusqu'à disparaître.
static func _speed(ci: CanvasItem, v: Dictionary, origin: Vector2, scale: float) -> void:
	var a: int = int(v.age) - int(v.age) % 2
	var k: float = v.taille
	var back := -1.0 if _dirv(v.dir).x >= 0.0 else 1.0
	var u := float(a) / float(LIFE.vitesse)      # 0 → 0.8
	for ln in LINES:
		var y: float = v.pos.y + float(ln[0]) * k
		var x0: float = v.pos.x + back * float(ln[1]) * k
		var L: float = float(ln[2]) * k
		var head := x0 + back * L * u * 1.1      # la tête recule plus vite que la queue
		var tail := x0 + back * L * (1.0 + 0.25 * u)
		if absf(tail - head) < 3.0:
			continue
		var w := (2.2 - 1.2 * u) * k
		var p0 := _scr(Vector2(head, y), origin, scale)
		var p1 := _scr(Vector2(tail, y), origin, scale)
		ci.draw_line(p0, p1, SPEED_EDGE, maxf(1.0, (w + 1.4) * scale))
		ci.draw_line(p0, p1, SPEED, maxf(1.0, w * scale))


## Morceau i (sur n) déjà effacé quand la proportion « gone » est atteinte.
static func _erased(i: int, n: int, gone: float) -> bool:
	if gone <= 0.0:
		return false
	var rank := HOLES.find(int(i * 12.0 / n))
	return float(rank) < gone * 12.0


## Traits cerclés de sombre (comme les lignes de vitesse) : tous les bords
## d'abord, puis tous les cœurs clairs, pour que les morceaux jointifs
## forment un seul trait sans coutures. segs = [[a, b], ...] (monde).
static func _strokes(ci: CanvasItem, segs: Array, w: float, core: Color, edge: Color, origin: Vector2, scale: float) -> void:
	for pass_i in 2:
		for sg in segs:
			var p0 := _scr(sg[0], origin, scale)
			var p1 := _scr(sg[1], origin, scale)
			if pass_i == 0:
				ci.draw_line(p0, p1, edge, maxf(1.0, (w + 1.4) * scale))
				ci.draw_circle(p0, maxf(0.5, (w + 1.4) * scale / 2.0), edge)
				ci.draw_circle(p1, maxf(0.5, (w + 1.4) * scale / 2.0), edge)
			else:
				ci.draw_line(p0, p1, core, maxf(1.0, w * scale))
				ci.draw_circle(p0, maxf(0.5, w * scale / 2.0), core)
				ci.draw_circle(p1, maxf(0.5, w * scale / 2.0), core)


static func _wave(ci: CanvasItem, v: Dictionary, origin: Vector2, scale: float, layer := "devant") -> void:
	var back := layer == "derriere"
	var a: int = int(v.age) - int(v.age) % 2
	var k: float = v.taille
	var c := Vector2(v.pos.x, 1.0)
	var s := clampf(_dirv(v.dir).x, -1.0, 1.0)
	var reach := {1.0: 1.0 + 0.45 * s, -1.0: 1.0 - 0.45 * s}   # côté droit, côté gauche (monde)
	if a == 0:
		if back:
			return
		# Flash : galette blanche au sol et étoile plate, comme l'étincelle.
		var pts := PackedVector2Array()
		for i in 20:
			var th := TAU * i / 20.0
			var side := 1.0 if cos(th) >= 0.0 else -1.0
			pts.append(_scr(c + Vector2(cos(th) * 17.0 * k * reach[side], sin(th) * 4.5 * k), origin, scale))
		ci.draw_colored_polygon(pts, AIR[2])
		_star(ci, c + Vector2(0, 2.0 * k), 0.0, 30.0 * k, 11.0 * k, 3.0 * k, AIR[0], origin, scale)
		ci.draw_circle(_scr(c + Vector2(0, 2.0 * k), origin, scale), 5.0 * k * scale, AIR[0])
		return
	# Anneau aplati : s'ouvre vite puis ralentit.
	var u := float(a) / 16.0                   # 0.125 → 1
	var grow := 1.0 - (1.0 - u) * (1.0 - u)
	var rx := (22.0 + 58.0 * grow) * k
	var ry := rx * 0.2
	var w := (4.2 - 2.8 * u) * k
	var core: Color = AIR[0] if a <= 2 else (AIR[1] if a <= 8 else AIR[2])
	var gone := clampf((float(a) - 8.0) / 8.0, 0.0, 1.0)
	if a <= 14:
		var n := 24
		var segs := []
		for i in n:
			if _erased(i, n, gone):
				continue
			# Moitié du fond (au-dessus du centre à l'écran) : calque arrière.
			if (sin(TAU * (i + 0.5) / n) > 0.0) != back:
				continue
			var t0 := TAU * i / n
			var t1 := TAU * (i + 1) / n
			var q := []
			for th in [t0, t1]:
				var side := 1.0 if cos(th) >= 0.0 else -1.0
				q.append(c + Vector2(cos(th) * rx * reach[side], sin(th) * ry))
			segs.append(q)
		_strokes(ci, segs, w, core, AIR[3], origin, scale)
	if back:
		return
	# Éclats de sol aux deux bouts, en paraboles, de plus en plus petits.
	for side in [1.0, -1.0]:
		var m: float = reach[side]
		for ch in CHIPS:
			var t := float(a)
			var ang := deg_to_rad(float(ch[0]))
			var sp: float = float(ch[1]) * k * m
			var p := Vector2(c.x + side * (16.0 * k * m + cos(ang) * sp * t), c.y + sin(ang) * sp * t - 0.2 * t * t)
			if p.y < 0.0:
				continue
			var size: float = float(ch[2]) * k * (1.0 if a < 8 else 0.6)
			_square(ci, p, size + 1.2, DUST[2], origin, scale)
			_square(ci, p, size, DUST[0] if a < 8 else DUST[1], origin, scale)


static func _boom(ci: CanvasItem, v: Dictionary, origin: Vector2, scale: float) -> void:
	var a: int = int(v.age) - int(v.age) % 2
	var k: float = v.taille
	var d: float = v.dir
	var dv := _dirv(d)
	var c: Vector2 = v.pos
	if a == 0:
		# Flash : un seul croissant blanc, épais, au point de départ.
		var fl := []
		for i in 8:
			var b0 := d - 60.0 + 15.0 * i
			fl.append([c + _dirv(b0) * 20.0 * k, c + _dirv(b0 + 15.0) * 20.0 * k])
		_strokes(ci, fl, 7.0 * k, AIR[0], AIR[2], origin, scale)
		return
	# Trois croissants : le premier devant et large, les suivants plus en arrière
	# et plus petits ; chacun apparaît une image après le précédent.
	for j in 3:
		var aj := a - 2 * j
		if aj < 0:
			continue
		var uj := float(aj) / 12.0
		var r := (26.0 - 5.0 * j + 16.0 * uj) * k
		var cc := c - dv * (13.0 * j + 6.0 * uj) * k
		var span := 58.0 - 8.0 * j
		var w := (5.0 - 1.0 * j - 3.2 * uj) * k
		if w < 0.6:
			continue
		var core: Color = AIR[0] if aj <= 2 else (AIR[1] if aj <= 6 else AIR[2])
		var gone := clampf((float(aj) - 6.0) / 6.0, 0.0, 1.0)
		var n := 8
		var segs := []
		for i in n:
			if _erased(i, n, gone):
				continue
			var b0 := d - span + 2.0 * span * i / n
			var b1 := d - span + 2.0 * span * (i + 1) / n
			segs.append([cc + _dirv(b0) * r, cc + _dirv(b1) * r])
		_strokes(ci, segs, w, core, AIR[3], origin, scale)
