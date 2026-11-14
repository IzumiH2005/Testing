@tool
class_name Planche
extends Node2D
## Une « planche » : fond gris, grille, sol, une ou plusieurs figures.
## Sert à la fois à l'atelier (scène interactive) et à l'outil de rendu en
## ligne de commande, pour que les deux montrent exactement la même chose.
##
## view = rectangle du monde affiché : position = coin bas-gauche (y vers le
## haut), size = largeur et hauteur en unités du monde.

const BG := Color("#9a9a9a")
const GROUND := Color("#d9c7c3")
const GRID := Color(0, 0, 0, 0.08)
const GRID_STRONG := Color(0, 0, 0, 0.2)
const DEBUG_COLORS := {"N": Color("#e8590c"), "F": Color("#1971c2"), "T": Color("#2f9e44")}
const DEBUG_BONES := [
	["hip", "waist", "T"], ["waist", "shoulder", "T"], ["shoulder", "neckTop", "T"], ["neckTop", "head", "T"],
	["shoulder", "elbowN", "N"], ["elbowN", "handN", "N"], ["hip", "kneeN", "N"], ["kneeN", "ankleN", "N"],
	["shoulder", "elbowF", "F"], ["elbowF", "handF", "F"], ["hip", "kneeF", "F"], ["kneeF", "ankleF", "F"],
]

@export var view := Rect2(-120, -12, 240, 212):
	set(v):
		view = v
		queue_redraw()
@export var px_per_unit := 3.0:
	set(v):
		px_per_unit = v
		queue_redraw()
@export var grid := true:
	set(v):
		grid = v
		queue_redraw()
@export var debug := false:
	set(v):
		debug = v
		queue_redraw()
@export var caption := "":
	set(v):
		caption = v
		queue_redraw()

## [{pose: Dictionary, color: Color, far_shade: float}], de l'arrière vers l'avant.
var figures: Array = []:
	set(v):
		figures = v
		queue_redraw()


func size_px() -> Vector2:
	return view.size * px_per_unit


## Position écran du point (0, 0) du monde.
func origin_px() -> Vector2:
	return Vector2(-view.position.x, view.position.y + view.size.y) * px_per_unit


func world_to_px(v: Vector2) -> Vector2:
	return StickRig.to_screen(v, origin_px(), px_per_unit)


func px_to_world(p: Vector2) -> Vector2:
	var o := origin_px()
	return Vector2((p.x - o.x) / px_per_unit, -(p.y - o.y) / px_per_unit)


func _draw() -> void:
	var sz := size_px()
	draw_rect(Rect2(Vector2.ZERO, sz), BG)
	if grid:
		var step := 10
		var x0 := int(ceil(view.position.x / step)) * step
		var x := x0
		while x <= view.position.x + view.size.x:
			var a := world_to_px(Vector2(x, 0)).x
			draw_line(Vector2(a, 0), Vector2(a, sz.y), GRID_STRONG if x % 50 == 0 else GRID, 1.0)
			x += step
		var y := int(ceil(view.position.y / step)) * step
		while y <= view.position.y + view.size.y:
			var b := world_to_px(Vector2(0, y)).y
			draw_line(Vector2(0, b), Vector2(sz.x, b), GRID_STRONG if y % 50 == 0 else GRID, 1.0)
			y += step
	var g := world_to_px(Vector2.ZERO).y
	if g < sz.y:
		draw_rect(Rect2(0, g, sz.x, sz.y - g), GROUND)
	for fig in figures:
		StickRig.draw_pose(self, fig.pose, origin_px(), px_per_unit, fig.get("color", Color("#111111")), fig.get("far_shade", 1.0))
		if debug:
			_draw_debug(fig.pose)
	if caption != "":
		draw_string(ThemeDB.fallback_font, Vector2(8, 18), caption, HORIZONTAL_ALIGNMENT_LEFT, -1, 13, Color("#222222"))


func _draw_debug(p: Dictionary) -> void:
	var J: Dictionary = StickRig.solve(p).joints
	for b in DEBUG_BONES:
		draw_line(world_to_px(J[b[0]]), world_to_px(J[b[1]]), DEBUG_COLORS[b[2]], 2.0, true)
	for k in J:
		var c := world_to_px(J[k])
		draw_circle(c, 3.5, Color.BLACK)
		draw_circle(c, 2.5, Color.WHITE)
