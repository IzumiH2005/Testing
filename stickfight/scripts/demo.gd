extends Control
## Démo des animations : un combattant seul (repos, mise en garde, blocage
## bas) ou le duo coup de pied / blocage. Le temps avance à 60 images par
## seconde, comme dans le jeu ; on peut figer, avancer et reculer image par
## image, ralentir, et afficher le squelette.
##
##   R  repos         G  mise en garde      B  blocage bas (depuis la garde)
##   K  duo coup de pied direct + blocage bas (rejoué en boucle)
##   Espace  pause    → / ←  image suivante / précédente (en pause)
##   L  ralenti ×4    D  squelette

const DUO := "res://anims/duo_blocage.json"
const HISTORY_MAX := 600
const HELP := "R repos   G mise en garde   B blocage bas   K duo   ·   Espace pause   ← → image par image   L ralenti   D squelette"

var planche: Planche
var help: Label
var combat: Combat
var mode := "solo"
var duo_len := 0
## Images déjà jouées (records de Combat), pour revenir en arrière en pause.
var history: Array = []
## Image affichée dans l'historique quand on recule ; -1 = image en cours.
var cursor := -1
var paused := false
var slow := 1
var tick := 0


func _ready() -> void:
	focus_mode = Control.FOCUS_ALL
	clip_contents = true
	planche = Planche.new()
	planche.grid = false
	planche.extra_draw = _draw_scene
	add_child(planche)
	help = Label.new()
	help.text = HELP
	help.add_theme_color_override("font_color", Color("#222222"))
	help.add_theme_font_size_override("font_size", 14)
	add_child(help)
	resized.connect(_fit)
	_solo("idle_repos", 0)
	grab_focus.call_deferred()


## 212 unités de haut, largeur selon la fenêtre ; centré sur la scène jouée.
func _fit() -> void:
	if planche == null or size.y <= 0:
		return
	var h := 212.0
	var w := h * size.x / size.y
	var cx := 61.0 if mode == "duo" else 8.0
	planche.px_per_unit = size.y / h
	planche.view = Rect2(cx - w / 2.0, -12, w, h)
	help.position = Vector2(12, size.y - 30)
	planche.queue_redraw()


func _restart_history() -> void:
	history = [combat.record()]
	cursor = -1
	_refresh()


## Un seul combattant : garde la même pose et enchaîne avec un fondu.
func _solo(nom: String, fondu: int) -> void:
	if mode != "solo" or combat == null:
		mode = "solo"
		combat = Combat.new()
		combat.add(Fighter.new(0.0, 1))
		combat.fighters[0].play(nom)
		_fit()
		_restart_history()
		return
	combat.fighters[0].play(nom, fondu)
	cursor = -1


func _duo() -> void:
	var data = JSON.parse_string(FileAccess.get_file_as_string(DUO))
	if not (data is Dictionary):
		push_error("Duo illisible : " + DUO)
		return
	mode = "duo"
	duo_len = int(data.get("longueur", 110))
	combat = Combat.from_duo(data)
	_fit()
	_restart_history()


func _physics_process(_delta: float) -> void:
	if paused:
		return
	tick += 1
	if tick % slow != 0:
		return
	_advance()


func _advance() -> void:
	combat.step()
	history.append(combat.record())
	if history.size() > HISTORY_MAX:
		history.pop_front()
	if mode == "duo" and combat.g > duo_len + 20:
		_duo()
		return
	_refresh()


func _current() -> Dictionary:
	if cursor >= 0:
		return history[cursor]
	return history[-1]


func _refresh() -> void:
	var r := _current()
	var parts := ["%s" % ("duo" if mode == "duo" else "solo")]
	for fig in r.fighters:
		parts.append("%s %d" % [fig.anim, int(fig.t)])
	if r.hitstop > 0:
		parts.append("arrêt sur impact %d" % r.hitstop)
	if paused:
		parts.append("PAUSE")
	if slow > 1:
		parts.append("ralenti ×%d" % slow)
	planche.caption = "   ".join(parts)
	planche.queue_redraw()


func _draw_scene(ci: Planche) -> void:
	var r := _current()
	Combat.draw_record(ci, r, ci.origin_px(), ci.px_per_unit)
	if ci.debug:
		for fig in r.fighters:
			ci._draw_debug(fig.pose)


func _step_back() -> void:
	if cursor < 0:
		cursor = history.size() - 1
	cursor = maxi(0, cursor - 1)
	_refresh()


func _step_forward() -> void:
	if cursor >= 0 and cursor < history.size() - 1:
		cursor += 1
		if cursor == history.size() - 1:
			cursor = -1
		_refresh()
	else:
		cursor = -1
		_advance()


func _gui_input(ev: InputEvent) -> void:
	if not (ev is InputEventKey and ev.pressed):
		return
	match ev.keycode:
		KEY_R:
			_solo("idle_repos", 10)
		KEY_G:
			_solo("mise_en_garde", 4)
		KEY_B:
			_solo("blocage_bas", 4)
		KEY_K:
			_duo()
		KEY_SPACE:
			paused = not paused
			if not paused:
				cursor = -1
			_refresh()
		KEY_RIGHT:
			if paused:
				_step_forward()
		KEY_LEFT:
			if paused:
				_step_back()
		KEY_L:
			slow = 4 if slow == 1 else 1
			_refresh()
		KEY_D:
			planche.debug = not planche.debug
			planche.queue_redraw()
		_:
			return
	accept_event()
