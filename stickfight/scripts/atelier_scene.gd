extends Control
## Scène de l'atelier : affiche la planche, les poignées des articulations, et
## transforme la souris et le clavier en modifications de pose (envoyées à
## l'atelier, qui garde l'état et l'historique).
##
## Poignées rondes : rotation de l'os qui finit à cette articulation.
## Poignées carrées : main et cheville (cinématique inverse), bassin (position).
## Ctrl + glisser la taille : incline le bassin (tout le tronc).

const HANDLES := [
	{"joint": "hip", "kind": "move", "id": "hip", "label": "Bassin (position)"},
	{"joint": "waist", "kind": "angle", "id": "spineLow"},
	{"joint": "shoulder", "kind": "angle", "id": "chest"},
	{"joint": "head", "kind": "angle", "id": "neck"},
	{"joint": "elbowF", "kind": "angle", "id": "armF"},
	{"joint": "handF", "kind": "ik", "id": "armF"},
	{"joint": "kneeF", "kind": "angle", "id": "thighF"},
	{"joint": "ankleF", "kind": "ik", "id": "legF"},
	{"joint": "elbowN", "kind": "angle", "id": "armN"},
	{"joint": "handN", "kind": "ik", "id": "armN"},
	{"joint": "kneeN", "kind": "angle", "id": "thighN"},
	{"joint": "ankleN", "kind": "ik", "id": "legN"},
]
const HIT_PX := 11.0
const COL_N := Color("#e8590c")
const COL_F := Color("#1971c2")
const COL_T := Color("#2f9e44")
const COL_SEL := Color("#ffe066")

var atelier  # scripts/atelier.gd
var planche: Planche
var overlay: Node2D
var hover := {}
var dragging := {}
var mouse_world := Vector2.ZERO


func _ready() -> void:
	focus_mode = Control.FOCUS_ALL
	clip_contents = true
	mouse_default_cursor_shape = Control.CURSOR_CROSS
	planche = Planche.new()
	add_child(planche)
	overlay = Node2D.new()
	add_child(overlay)
	overlay.draw.connect(_draw_overlay)
	resized.connect(_fit)
	_fit()


## La planche remplit la scène : 212 unités de haut (sol à 12 unités du bas),
## largeur selon les proportions de la fenêtre, centrée sur x = 0.
func _fit() -> void:
	if planche == null or size.y <= 0:
		return
	var h := 212.0
	var w := h * size.x / size.y
	planche.px_per_unit = size.y / h
	planche.view = Rect2(-w / 2.0, -12, w, h)
	refresh()


func refresh() -> void:
	if planche == null or atelier == null:
		return
	var figs := []
	if not atelier.ghost.is_empty():
		figs.append({"pose": atelier.ghost, "color": Color("#d98a8a")})
	figs.append({"pose": atelier.pose, "color": atelier.color, "far_shade": 0.78 if atelier.shade_far else 1.0})
	planche.grid = atelier.show_grid
	planche.debug = atelier.show_debug
	planche.figures = figs
	overlay.queue_redraw()


func _handle_pos(h: Dictionary) -> Vector2:
	var J: Dictionary = StickRig.solve(atelier.pose).joints
	return planche.world_to_px(J[h.joint])


func _pick(p: Vector2) -> Dictionary:
	var best := {}
	var best_d := HIT_PX
	# Les poignées de bout de membre passent devant (dernières dessinées).
	for i in range(HANDLES.size() - 1, -1, -1):
		var h: Dictionary = HANDLES[i]
		var d := _handle_pos(h).distance_to(p)
		if d < best_d:
			best_d = d
			best = h
	return best


func _gui_input(ev: InputEvent) -> void:
	if ev is InputEventMouseButton and ev.button_index == MOUSE_BUTTON_LEFT:
		if ev.pressed:
			grab_focus()
			var h := _pick(ev.position)
			if h.is_empty():
				return
			if h.kind == "angle" and h.id == "spineLow" and ev.ctrl_pressed:
				h = {"joint": "waist", "kind": "angle", "id": "root"}
			dragging = {"h": h, "start_world": planche.px_to_world(ev.position)}
			atelier.begin_edit("drag")
			atelier.select(h.kind, h.id)
		else:
			if not dragging.is_empty():
				dragging = {}
				atelier.end_edit()
		accept_event()
	elif ev is InputEventMouseMotion:
		mouse_world = planche.px_to_world(ev.position)
		if not dragging.is_empty():
			atelier.drag_to(dragging.h, mouse_world, dragging.start_world)
		else:
			var h := _pick(ev.position)
			if h != hover:
				hover = h
				overlay.queue_redraw()
		atelier.update_readout()
	elif ev is InputEventKey and ev.pressed:
		var step := 1.0
		if ev.shift_pressed:
			step = 5.0
		if ev.alt_pressed:
			step = 0.1
		var dir := Vector2.ZERO
		match ev.keycode:
			KEY_LEFT: dir = Vector2(-1, 0)
			KEY_RIGHT: dir = Vector2(1, 0)
			KEY_UP: dir = Vector2(0, 1)
			KEY_DOWN: dir = Vector2(0, -1)
			KEY_BRACKETLEFT:
				atelier.cycle_selection(-1)
				accept_event()
				return
			KEY_BRACKETRIGHT:
				atelier.cycle_selection(1)
				accept_event()
				return
		if dir != Vector2.ZERO:
			atelier.nudge(dir, step)
			accept_event()


func _draw_overlay() -> void:
	if atelier == null:
		return
	for h in HANDLES:
		var c := _handle_pos(h)
		var side: String = h.joint.right(1)
		var col := COL_N if side == "N" else (COL_F if side == "F" else COL_T)
		var is_sel: bool = atelier.sel.kind == h.kind and atelier.sel.id == h.id
		if h.id == "spineLow" and atelier.sel.id == "root":
			is_sel = true
		var r := 6.0
		if is_sel or h == hover:
			r = 8.0
		if h.kind == "angle":
			overlay.draw_circle(c, r + 1.5, Color.BLACK)
			overlay.draw_circle(c, r, COL_SEL if is_sel else col)
		else:
			overlay.draw_rect(Rect2(c - Vector2(r + 1.5, r + 1.5), Vector2(2 * r + 3, 2 * r + 3)), Color.BLACK)
			overlay.draw_rect(Rect2(c - Vector2(r, r), Vector2(2 * r, 2 * r)), COL_SEL if is_sel else col)
