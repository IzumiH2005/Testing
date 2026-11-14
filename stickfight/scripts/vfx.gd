class_name Vfx
extends RefCounted
## Effets visuels dessinés à la main, en aplats, comme en pixel art
## (methode-pixel-art, E7-G effets, E7-F impact, E2 timing, A6 rampes) :
## - couleurs en nombre limité, pas de dégradé ni de transparence ;
## - lumière en haut à gauche, rampes qui passent du clair au sombre puis
##   au gris en vieillissant (ombres froides, lumières chaudes) ;
## - chaque effet est une suite de DESSINS tenus chacun plusieurs images,
##   de plus en plus longtemps (ralenti à l'arrivée, table KEYS) ;
## - la masse se fragmente : chaque morceau a sa trajectoire, ralentit,
##   rétrécit ; on efface par morceaux (trous), jamais en fondu ;
## - tout dépend seulement de l'âge : même âge, même dessin.
##
## Un effet : {type, pos: Vector2 (monde), age: int, dir: degrés (monde),
##             genre: "garde" | "coup", taille: facteur}
##
## etincelle  éclair de contact : flash blanc (0-1), étoile allongée dans la
##            direction du coup (2-3), anneau qui s'ouvre et traits (4-7),
##            éclats qui retombent (8-13).
## poussiere  nuage de poussière au sol (pied qui se pose, glisse, pousse) :
##            5 bouffées en grappes de boules ombrées qui fuient au ras du
##            sol (surtout du côté de dir), montent un peu, ralentissent,
##            virent au gris et se défont boule par boule.
## vitesse    lignes de vitesse : traits horizontaux laissés sur place dans
##            l'arène ; le coureur s'en éloigne, ils se rétractent vers
##            l'arrière (dir = sens de la course, les traits partent à l'opposé).
## onde       onde de choc au sol (décollage ou atterrissage en force) :
##            image d'impact (galette blanche, rayons), puis un front d'air
##            épais qui court sur le sol en perspective, plus épais devant
##            que derrière, suivi d'un second anneau ; un dôme d'air se
##            soulève et se brise ; un mur de poussière roule avec le front ;
##            des cailloux sautent ; si taille ≥ 1,2 le sol se fend. dir
##            penche l'onde : elle va plus loin du côté de dir (−90 = symétrique).
## choc       bang d'air au point de départ d'une propulsion : flash, puis
##            trois anneaux en perspective, perpendiculaires au vol (dir),
##            laissés sur place et reliés en cône vers le corps qui s'en
##            éloigne ; ils s'ouvrent, s'amincissent, grisent et se brisent.

const PALETTES := {
	"garde": [Color("#ffffff"), Color("#d0ebff"), Color("#74c0fc"), Color("#1864ab")],
	"coup": [Color("#ffffff"), Color("#fff3bf"), Color("#ffa94d"), Color("#c2410c")],
}
const LIFE := {"etincelle": 14, "poussiere": 32, "vitesse": 10, "onde": 30, "choc": 22}
## Début de chaque dessin (âge en images) : tenues de plus en plus longues.
const KEYS := {
	"poussiere": [0, 2, 4, 6, 9, 12, 16, 20, 25, 30],
	"onde": [0, 2, 4, 6, 8, 11, 14, 18, 22, 26],
	"choc": [0, 2, 4, 6, 9, 12, 15, 19],
}

## Poussière : rampes [lumière, corps, ombre, trait], du plus jeune au plus
## vieux. La teinte part chaude (crème) et tourne au froid (mauve) dans les
## ombres ; en vieillissant tout descend d'un cran puis se désature.
const DUST_POP := [Color("#ffffff"), Color("#fbf3e6"), Color("#e3d3c2"), Color("#857479")]
const DUST_A := [Color("#fbf3e6"), Color("#e3d3c2"), Color("#b9a59a"), Color("#5e5260")]
const DUST_B := [Color("#e3d3c2"), Color("#b9a59a"), Color("#8f7f84"), Color("#4f4651")]
const DUST_C := [Color("#c9c2bf"), Color("#a29c9c"), Color("#7b7680"), Color("#4f4651")]
## Air comprimé : [cœur, clair, moyen, trait]. Blanc → bleu-gris froid.
const AIR := [Color("#ffffff"), Color("#dfe7f5"), Color("#a3b1cc"), Color("#4c5873")]
const AIR_OLD := [Color("#dfe7f5"), Color("#b8c1d1"), Color("#8b94a6"), Color("#4c5873")]
## Cailloux : [dessus éclairé, face, trait].
const ROCK := [Color("#e3d3c2"), Color("#9f8b86"), Color("#4f4651")]
const CRACK := Color("#3b3340")
const CRACK_LIP := Color("#f4ebe1")

## Ordre dans lequel les morceaux d'un trait s'effacent (des trous qui grandissent).
const HOLES := [5, 1, 9, 3, 7, 0, 10, 4, 8, 2, 11, 6]

## Bouffées : [côté (+1 = vers dir), vitesse, montée, taille, retard].
const PUFFS := [[1.0, 4.2, 0.6, 1.0, 0], [1.0, 2.2, 1.1, 0.75, 1], [-1.0, 2.6, 0.7, 0.8, 0],
	[-1.0, 1.0, 1.3, 0.6, 2], [0.15, 0.4, 1.6, 0.85, 1]]
## Boules d'une bouffée : [x, y (en rayons), rayon relatif, dérive x, dérive y]
## (la dérive écarte les morceaux quand la bouffée se défait).
const LOBES := [[0.0, 0.0, 1.0, 0.0, 0.4], [-0.78, -0.18, 0.68, -0.9, 0.1],
	[0.74, -0.22, 0.62, 0.9, 0.0], [0.12, 0.62, 0.55, 0.3, 0.9]]
## Ordre d'effacement des boules (la grosse en dernier).
const LOBE_ORDER := [3, 1, 2, 0]

## Onde : bouffées du mur de poussière, angle sur l'ellipse (degrés, 0 = droite,
## > 0 = moitié du fond) et taille.
const CROWN := [[0.0, 1.0], [180.0, 1.0], [-28.0, 0.8], [-152.0, 0.8], [26.0, 0.7],
	[154.0, 0.7], [-62.0, 0.6], [-118.0, 0.6]]
## Cailloux : [angle depuis l'horizontale, vitesse, taille, départ (rayon relatif)].
const CHIPS := [[62.0, 3.0, 3.2, 0.7], [38.0, 3.6, 2.6, 0.9], [76.0, 2.2, 2.2, 0.5],
	[24.0, 3.1, 2.0, 1.0], [52.0, 2.5, 1.6, 0.8]]
## Fissures : suites de points (angle degrés, rayon) dans le plan du sol.
const CRACKS := [
	[[0.0, 4.0], [-8.0, 12.0], [6.0, 19.0], [-4.0, 27.0]],
	[[180.0, 4.0], [190.0, 11.0], [174.0, 18.0], [184.0, 24.0]],
	[[-60.0, 4.0], [-48.0, 10.0], [-66.0, 16.0]],
	[[-125.0, 4.0], [-138.0, 11.0], [-120.0, 15.0]],
]

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
## (layer = "derriere") et après (layer = "devant"). Les anneaux (onde, choc)
## mettent leur moitié du fond derrière le corps et celle de devant par-dessus ;
## dôme, fissures et cône passent derrière ; le reste est devant.
static func draw(ci: CanvasItem, v: Dictionary, origin: Vector2, scale: float, layer := "devant") -> void:
	match v.type:
		"choc":
			_boom(ci, v, origin, scale, layer)
		"onde":
			_wave(ci, v, origin, scale, layer)
		"poussiere":
			if layer == "devant":
				_dust(ci, v, origin, scale)
		"etincelle":
			if layer == "devant":
				_spark(ci, v, origin, scale)
		"vitesse":
			if layer == "devant":
				_speed(ci, v, origin, scale)


## Âge du dessin affiché : le début de la tenue en cours (table KEYS).
static func _key(type: String, age: int) -> int:
	var keys: Array = KEYS[type]
	var k := 0
	for t in keys:
		if age >= int(t):
			k = int(t)
	return k


static func _dirv(deg: float) -> Vector2:
	return Vector2(cos(deg_to_rad(deg)), sin(deg_to_rad(deg)))


static func _scr(w: Vector2, origin: Vector2, scale: float) -> Vector2:
	return StickRig.to_screen(w, origin, scale)


## Ralenti à l'arrivée : 0 → 1, vite au départ puis de plus en plus lent.
static func _out(t: float, tau: float) -> float:
	return 1.0 - exp(-maxf(t, 0.0) / tau)


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


## Ellipse pleine dans le monde (rx en x, ry en y).
static func _oval(ci: CanvasItem, c: Vector2, rx: float, ry: float, col: Color, origin: Vector2, scale: float) -> void:
	var pts := PackedVector2Array()
	for i in 24:
		var th := TAU * i / 24.0
		pts.append(_scr(c + Vector2(cos(th) * rx, sin(th) * ry), origin, scale))
	ci.draw_colored_polygon(pts, col)


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


# --- Poussière ---------------------------------------------------------------

## Grappe de boules ombrées, dessinée en 4 passes sur TOUTES les boules (trait,
## ombre, corps, lumière) pour qu'elles se fondent en un seul nuage :
## lumière en haut à gauche, ombre froide en bas à droite, trait de 1.
## blobs = [[centre monde, rayon], ...] ; pal = [lumière, corps, ombre, trait].
static func _cloud(ci: CanvasItem, blobs: Array, pal: Array, origin: Vector2, scale: float) -> void:
	for pass_i in 4:
		for b in blobs:
			var c: Vector2 = b[0]
			var r: float = b[1]
			match pass_i:
				0:
					ci.draw_circle(_scr(c, origin, scale), (r + 1.0) * scale, pal[3])
				1:
					ci.draw_circle(_scr(c, origin, scale), r * scale, pal[2])
				2:
					if r >= 2.0:
						ci.draw_circle(_scr(c + Vector2(-0.14, 0.16) * r, origin, scale), r * 0.84 * scale, pal[1])
				3:
					if r >= 3.0:
						ci.draw_circle(_scr(c + Vector2(-0.34, 0.36) * r, origin, scale), r * 0.42 * scale, pal[0])


## Rampe de la poussière selon l'âge de la bouffée (t = 0 : image « pop »).
static func _dust_pal(t: float) -> Array:
	if t <= 0.0:
		return DUST_POP
	if t <= 5.0:
		return DUST_A
	if t <= 13.0:
		return DUST_B
	return DUST_C


## Une bouffée : boules d'un rayon r autour de c, qui s'écartent et
## disparaissent une à une quand `gone` monte (0 → 1).
static func _puff_blobs(c: Vector2, r: float, spread: float, gone: float, k: float) -> Array:
	var out := []
	for rank in LOBE_ORDER.size():
		var i: int = LOBE_ORDER[rank]
		if float(rank) < gone * LOBE_ORDER.size():
			continue
		var lb: Array = LOBES[i]
		var rr: float = r * float(lb[2]) * (1.0 - 0.25 * spread)
		var p := c + Vector2(float(lb[0]), float(lb[1])) * r + Vector2(float(lb[3]), float(lb[4])) * spread * 5.0 * k
		out.append([p.round(), maxf(0.0, roundf(rr * 2.0) / 2.0)])
	return out


static func _dust(ci: CanvasItem, v: Dictionary, origin: Vector2, scale: float) -> void:
	var T := float(_key("poussiere", int(v.age)))
	var k: float = v.taille
	var sens := 1.0 if _dirv(v.dir).x >= 0.0 else -1.0
	var n := PUFFS.size() if k >= 0.8 else 3
	# Les bouffées du fond d'abord (les plus hautes), celles de devant ensuite.
	for idx in [3, 1, 4, 2, 0]:
		if idx >= n:
			continue
		var pf: Array = PUFFS[idx]
		var t := T - float(pf[4])
		if t < 0.0:
			continue
		var late := clampf((t - 10.0) / 14.0, 0.0, 1.0)
		var r: float = float(pf[3]) * k * (2.5 + 6.5 * _out(t, 3.0)) * (1.0 - 0.4 * late)
		var x: float = v.pos.x + float(pf[0]) * sens * (3.0 * k + float(pf[1]) * k * 5.0 * _out(t, 5.0))
		var y: float = r * 0.7 + float(pf[2]) * k * 9.0 * _out(t, 9.0)
		var gone := clampf((t - 14.0) / 14.0, 0.0, 1.0)
		var blobs := _puff_blobs(Vector2(x, y), r, late, gone, k)
		_cloud(ci, blobs, _dust_pal(t), origin, scale)


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


# --- Traits d'air --------------------------------------------------------------

## Morceau i (sur n) déjà effacé quand la proportion « gone » est atteinte.
static func _erased(i: int, n: int, gone: float) -> bool:
	if gone <= 0.0:
		return false
	var rank := HOLES.find(int(i * 12.0 / n))
	return float(rank) < gone * 12.0


## Traits cerclés de sombre : tous les bords d'abord, puis tous les cœurs,
## pour que les morceaux jointifs forment un seul trait sans coutures.
## groups = [[segs, couleur du cœur], ...], segs = [[a, b, épaisseur], ...]
## (monde) ; les cœurs sont peints dans l'ordre des groupes.
static func _strokes2(ci: CanvasItem, groups: Array, edge: Color, origin: Vector2, scale: float, rim := 1.2) -> void:
	for pass_i in groups.size() + 1:
		var segs: Array = []
		var col := edge
		if pass_i == 0:
			for gr in groups:
				segs.append_array(gr[0])
		else:
			segs = groups[pass_i - 1][0]
			col = groups[pass_i - 1][1]
		for sg in segs:
			var p0 := _scr(sg[0], origin, scale)
			var p1 := _scr(sg[1], origin, scale)
			var w: float = (float(sg[2]) + (rim if pass_i == 0 else 0.0)) * scale
			ci.draw_line(p0, p1, col, maxf(1.0, w))
			ci.draw_circle(p0, maxf(0.5, w / 2.0), col)
			ci.draw_circle(p1, maxf(0.5, w / 2.0), col)


static func _strokes(ci: CanvasItem, segs: Array, core: Color, edge: Color, origin: Vector2, scale: float, rim := 1.2) -> void:
	_strokes2(ci, [[segs, core]], edge, origin, scale, rim)


## Segments d'un anneau d'air en perspective : ellipse de centre c, d'axes
## ax (vecteur, demi-grand axe) et ay (vecteur, demi-petit axe). La moitié où
## sin > 0 est « au fond » (calque arrière) et plus mince (facteur thin).
## Épaisseur w devant, effacement par trous selon gone.
static func _ring_segs(c: Vector2, ax: Vector2, ay: Vector2, w: float, thin: float, gone: float,
		back: bool, n := 28) -> Array:
	var segs := []
	for i in n:
		if _erased(i, n, gone):
			continue
		var mid := TAU * (i + 0.5) / n
		if (sin(mid) > 0.0) != back:
			continue
		var t0 := TAU * i / n
		var t1 := TAU * (i + 1) / n
		var ww := w * lerpf(1.0, thin, (sin(mid) + 1.0) / 2.0)
		segs.append([c + ax * cos(t0) + ay * sin(t0), c + ax * cos(t1) + ay * sin(t1), ww])
	return segs


## Anneau d'air simple (un ton).
static func _air_ring(ci: CanvasItem, c: Vector2, ax: Vector2, ay: Vector2, w: float, thin: float,
		gone: float, pal: Array, back: bool, origin: Vector2, scale: float, n := 28, core_i := 0) -> void:
	_strokes(ci, _ring_segs(c, ax, ay, w, thin, gone, back, n), pal[core_i], pal[3], origin, scale)


## Front d'onde en bande : bord extérieur clair et épais (le front), bande
## intérieure d'un ton plus sombre juste derrière, un seul trait autour.
static func _air_band(ci: CanvasItem, c: Vector2, ax: Vector2, ay: Vector2, w: float, thin: float,
		gone: float, pal: Array, back: bool, origin: Vector2, scale: float, n := 28, core_i := 0) -> void:
	var inner := 1.0 - 0.9 * w / maxf(ax.length(), 1.0)
	var outer := _ring_segs(c, ax, ay, w * 0.62, thin, gone, back, n)
	var band := _ring_segs(c, ax * inner, ay * inner, w * 0.75, thin, gone, back, n)
	_strokes2(ci, [[band, pal[2]], [outer, pal[core_i]]], pal[3], origin, scale)


# --- Onde de choc au sol -----------------------------------------------------

static func _wave(ci: CanvasItem, v: Dictionary, origin: Vector2, scale: float, layer := "devant") -> void:
	var back := layer == "derriere"
	var T := float(_key("onde", int(v.age)))
	var k: float = v.taille
	var c := Vector2(v.pos.x, 0.0)
	var s := clampf(_dirv(v.dir).x, -1.0, 1.0)
	var reach := 1.0 + 0.4 * absf(s)
	var shift := 0.3 * s                     # le centre de l'ellipse glisse vers dir
	var R := 92.0 * k
	if T == 0.0:
		if back:
			return
		# Image d'impact : galette blanche cerclée au sol, rayons qui jaillissent.
		var cc := c + Vector2(shift * 12.0 * k, 0.0)
		_oval(ci, cc, 34.0 * k * reach + 1.5, 8.5 * k + 1.5, AIR[3], origin, scale)
		_oval(ci, cc, 34.0 * k * reach, 8.5 * k, AIR[1], origin, scale)
		_oval(ci, cc, 24.0 * k * reach, 5.5 * k, AIR[0], origin, scale)
		for ang in [18.0, 50.0, 90.0, 130.0, 162.0]:
			var L := (16.0 + 14.0 * sin(deg_to_rad(ang))) * k
			var b := cc + Vector2(0, 2.0 * k)
			var tip := b + _dirv(ang) * L
			var side := _dirv(ang + 90.0) * 2.4 * k
			var pts := PackedVector2Array([_scr(b + side, origin, scale), _scr(tip, origin, scale), _scr(b - side, origin, scale)])
			ci.draw_colored_polygon(pts, AIR[0])
		_star(ci, cc + Vector2(0, 1.0 * k), 0.0, 46.0 * k * reach, 9.0 * k, 3.0 * k, AIR[0], origin, scale)
		return
	var g := _out(T, 6.0)
	var rx := (14.0 * k + R * g)
	var cc := c + Vector2(shift * rx, 0.0)
	var ax := Vector2(rx * reach, 0.0)
	var ay := Vector2(0.0, rx * 0.2)
	var u := clampf(T / 26.0, 0.0, 1.0)
	var pal: Array = AIR if T <= 8.0 else AIR_OLD
	var core_i := 0 if T <= 4.0 else 1
	# Fissures du sol (lourd seulement) : trait sombre + lèvre claire.
	if back and k >= 1.2:
		var cgone := clampf((T - 14.0) / 12.0, 0.0, 1.0)
		var grow := clampf(T / 4.0, 0.0, 1.0)
		var ci_n := 0
		for cr in CRACKS:
			var pts: Array = cr
			for j in pts.size() - 1:
				ci_n += 1
				if _erased(ci_n * 5 % 12, 12, cgone):
					continue
				var a0: Array = pts[j]
				var a1: Array = pts[j + 1]
				var r0 := float(a0[1]) * k * reach * grow
				var r1 := float(a1[1]) * k * reach * grow
				var p0 := c + Vector2(cos(deg_to_rad(float(a0[0]))) * r0, sin(deg_to_rad(float(a0[0]))) * r0 * 0.25)
				var p1 := c + Vector2(cos(deg_to_rad(float(a1[0]))) * r1, sin(deg_to_rad(float(a1[0]))) * r1 * 0.25)
				ci.draw_line(_scr(p0 + Vector2(0, -1.2), origin, scale), _scr(p1 + Vector2(0, -1.2), origin, scale), CRACK_LIP, maxf(1.0, 1.0 * scale))
				ci.draw_line(_scr(p0, origin, scale), _scr(p1, origin, scale), CRACK, maxf(1.0, 1.6 * scale))
	# Dôme d'air : la coque de l'onde se soulève puis se brise (3 dessins).
	if back and T <= 8.0:
		var dgone: float = [0.0, 0.0, 0.25, 0.5, 0.75][int(T / 2.0)]
		var dh := rx * (0.62 - 0.1 * T / 8.0)
		var segs := []
		var n := 18
		for i in n:
			if _erased(i, n, dgone):
				continue
			var t0 := PI * i / n
			var t1 := PI * (i + 1) / n
			var w := (4.0 - 0.35 * T) * k * (0.45 + 0.55 * sin(PI * (i + 0.5) / n))
			segs.append([cc + Vector2(cos(t0) * rx * reach * 1.04, sin(t0) * dh),
				cc + Vector2(cos(t1) * rx * reach * 1.04, sin(t1) * dh), w])
		_strokes(ci, segs, AIR[0] if T <= 2.0 else AIR[1], AIR[3], origin, scale, 1.0)
	# Second anneau : plus petit, plus mince, il suit le front et s'efface avant.
	if T >= 4.0 and T <= 18.0:
		var rx2 := rx * 0.68
		var g2 := clampf((T - 8.0) / 10.0, 0.0, 1.0)
		_air_ring(ci, c + Vector2(shift * rx2, 0.0), Vector2(rx2 * reach, 0.0), Vector2(0.0, rx2 * 0.2),
			(2.4 - 1.0 * u) * k, 0.55, g2, AIR_OLD, back, origin, scale, 24, 1)
	# Front : épais devant, mince au fond, de plus en plus mince et troué.
	var gone := clampf((T - 11.0) / 15.0, 0.0, 1.0)
	_air_band(ci, cc, ax, ay, (9.0 - 6.0 * u) * k, 0.45, gone, pal, back, origin, scale, 32, core_i)
	# Mur de poussière qui roule avec le front, en retard sur lui.
	var crown := []
	var dg := clampf((T - 10.0) / 16.0, 0.0, 1.0)
	for cw in CROWN:
		var ang := deg_to_rad(float(cw[0]))
		if (sin(ang) > 0.0) != back:
			continue
		var rr := rx * 0.9
		var base := c + Vector2(shift * rr + cos(ang) * rr * reach, sin(ang) * rr * 0.2)
		var r: float = float(cw[1]) * k * (3.0 + 7.0 * _out(T, 4.0)) * (1.0 - 0.35 * dg)
		var lift := k * 10.0 * _out(T, 6.0) * float(cw[1])
		crown.append([base + Vector2(0, r * 0.6 + lift), r, dg])
	for cw in crown:
		_cloud(ci, _puff_blobs(cw[0], cw[1], cw[2], cw[2], k), _dust_pal(T - 2.0), origin, scale)
	if back:
		return
	# Cailloux aux deux bouts, en paraboles : dessus clair, face, trait.
	for side in [1.0, -1.0]:
		var m: float = 1.0 + 0.35 * s * side
		for ch in CHIPS:
			var ang := deg_to_rad(float(ch[0]))
			var sp: float = float(ch[1]) * k * m
			var p := Vector2(c.x + side * (float(ch[3]) * 20.0 * k * m + cos(ang) * sp * T),
				sin(ang) * sp * T - 0.22 * T * T)
			if p.y < 0.0 or T > 20.0:
				continue
			var size: float = float(ch[2]) * k * (1.0 if T < 11.0 else 0.65)
			p = p.round()
			_square(ci, p, size + 2.0, ROCK[2], origin, scale)
			_square(ci, p, size, ROCK[1], origin, scale)
			_square(ci, p + Vector2(-size * 0.2, size * 0.25), size * 0.5, ROCK[0], origin, scale)


# --- Bang d'air (propulsion) ---------------------------------------------------

static func _boom(ci: CanvasItem, v: Dictionary, origin: Vector2, scale: float, layer := "devant") -> void:
	var back := layer == "derriere"
	var T := float(_key("choc", int(v.age)))
	var k: float = v.taille
	var dv := _dirv(v.dir)
	var pv := Vector2(-dv.y, dv.x)          # perpendiculaire au vol
	var c: Vector2 = v.pos
	if T == 0.0:
		# Image d'impact : disque d'air comprimé et lame blanche en travers du vol.
		if back:
			ci.draw_circle(_scr(c, origin, scale), 24.0 * k * scale, AIR[3])
			ci.draw_circle(_scr(c, origin, scale), 22.5 * k * scale, AIR[2])
			ci.draw_circle(_scr(c - dv * 3.0 * k, origin, scale), 17.0 * k * scale, AIR[1])
			ci.draw_circle(_scr(c - dv * 5.0 * k, origin, scale), 11.0 * k * scale, AIR[0])
		else:
			_star(ci, c, v.dir + 90.0, 60.0 * k, 14.0 * k, 4.5 * k, AIR[3], origin, scale)
			_star(ci, c, v.dir + 90.0, 55.0 * k, 11.0 * k, 3.0 * k, AIR[0], origin, scale)
		return
	# Cône : deux lignes qui relient le bord des anneaux vers le corps.
	if back and T <= 9.0:
		var R0 := (16.0 + 26.0 * _out(T, 4.0)) * k
		var tip := c + dv * 46.0 * k
		var cg: float = [0.0, 0.0, 0.0, 0.34, 0.67][int(T / 2.0)] if T < 10.0 else 1.0
		for sd in [1.0, -1.0]:
			var a: Vector2 = c + pv * R0 * sd
			var b: Vector2 = tip + pv * 7.0 * k * sd
			var segs := []
			for i in 6:
				if _erased(i, 6, cg):
					continue
				segs.append([a.lerp(b, i / 6.0), a.lerp(b, (i + 1) / 6.0), (2.2 - 1.6 * i / 6.0) * k])
			_strokes(ci, segs, AIR[1], AIR[3], origin, scale, 1.0)
	# Trois anneaux laissés sur place, du plus grand (départ) au plus petit.
	for j in 3:
		var t := T - 2.0 * j
		if t < 0.0:
			continue
		var cc := c + dv * 16.0 * j * k
		var R := ((15.0 - 3.0 * j) + (26.0 - 6.0 * j) * _out(t, 4.0)) * k
		var u := clampf(t / 16.0, 0.0, 1.0)
		var w := (7.5 - 1.2 * j) * k * (1.0 - 0.7 * u)
		var gone := clampf((t - 5.0) / 10.0, 0.0, 1.0)
		var pal: Array = AIR if t <= 4.0 else AIR_OLD
		var core_i := 0 if t <= 2.0 else 1
		_air_band(ci, cc, pv * R, dv * R * 0.3, w, 0.5, gone, pal, back, origin, scale, 24, core_i)
