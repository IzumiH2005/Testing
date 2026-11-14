extends Control
## Démo des animations : un combattant seul ou le duo coup de pied /
## blocage. Le temps avance à 60 images par seconde, comme dans le jeu ; on
## peut figer, avancer et reculer image par image, ralentir, et afficher le
## squelette.
##
## Le repos est l'état par défaut ; la garde ne dure que tant que G est tenu.
##   → / ←  maintenus : marche détendue avant / arrière depuis le repos ;
##      relâchés, le combattant finit son pas et s'arrête au repos.
##   G  maintenu : mise en garde ; avec → / ←, marche en garde ; relâché,
##      le combattant sort de la garde et revient au repos.
##   B  blocage bas (en garde)   K  duo coup de pied direct + blocage bas
##   R  repos (remise à zéro)
##   Espace  pause    → / ←  image suivante / précédente (en pause)
##   L  ralenti ×4    D  squelette

const DUO := "res://anims/duo_blocage.json"
const HISTORY_MAX := 600
const HELP := "→ ← marcher   Maj + → courir   G tenu : garde (→ ← en garde, B blocage bas)   K duo   R repos   ·   Espace pause   ← → image par image   L ralenti   D squelette"

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
## Centre de la caméra en solo (suit le bassin avec un peu de retard).
var cam_x := 8.0


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
	var cx := cam_x
	if mode == "duo":
		cx = 61.0
	elif not history.is_empty():
		cx = float(_current().get("camx", cam_x))
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
		cam_x = 8.0
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
	if mode == "solo" and not paused:
		_control_input()  # en pause, → et ← servent à avancer image par image
	combat.step()
	var rec := combat.record()
	if mode == "solo":
		var hip: float = rec.fighters[0].pose.x
		cam_x += (hip + 8.0 - cam_x) * 0.08
		rec["camx"] = cam_x
	history.append(rec)
	if history.size() > HISTORY_MAX:
		history.pop_front()
	if mode == "duo" and combat.g > duo_len + 20:
		_duo()
		return
	_refresh()


## Images de la boucle de marche détendue où un arrêt peut commencer, et
## l'arrêt à jouer. Chaque arrêt part exactement de la pose de la boucle à
## cette image : au relâché, le combattant finit le pas en cours jusqu'à la
## prochaine de ces images (au plus une demi-boucle), sans fondu.
const ARRETS := {
	"marche_detendue": {28: "marche_detendue_arret_court", 0: "marche_detendue_arret_pas"},
	"marche_detendue_arriere": {24: "marche_detendue_arriere_arret_pas", 56: "marche_detendue_arriere_arret_deux_pas"},
	"course": {0: "course_arret_n", 20: "course_arret_f"},
}


## Clavier tenu, lu à chaque image :
## - depuis le repos, → / ← lancent la marche détendue ; relâchées, la marche
##   s'arrête à la prochaine image d'arrêt de la boucle (ARRETS) et revient au
##   repos ;
## - Maj + → depuis le repos lance la course (départ, boucle) ; relâchées,
##   elle freine à la prochaine pose d'appui (image 0 ou 20) et revient au repos ;
## - G tenu met en garde (depuis le repos) ; en garde, → / ← font la marche en
##   garde, qui s'arrête à l'image 0 de son cycle (pieds en position de garde) ;
##   G relâché, une fois revenu en garde_idle, joue la sortie de garde.
func _control_input() -> void:
	var f: Fighter = combat.fighters[0]
	var fwd := Input.is_physical_key_pressed(KEY_RIGHT)
	var back := Input.is_physical_key_pressed(KEY_LEFT) and not fwd
	var guard := Input.is_physical_key_pressed(KEY_G)
	var run := Input.is_physical_key_pressed(KEY_SHIFT)
	var nom := f.anim_name()
	match nom:
		"idle_repos":
			if guard:
				f.play("mise_en_garde", 4)
			elif fwd and run:
				f.play("course_depart", 6)
			elif fwd:
				f.play("marche_detendue_depart", 6)
			elif back:
				f.play("marche_detendue_arriere_depart", 6)
		"marche_detendue", "marche_detendue_arriere", "course":
			var held := fwd and run if nom == "course" else (fwd if nom == "marche_detendue" else back)
			var phase := int(f.t) % int(f.anim.longueur)
			if not held and ARRETS[nom].has(phase):
				f.play(ARRETS[nom][phase], 0)
		"garde_idle":
			if not guard:
				f.play("sortie_de_garde", 6)
			elif fwd:
				f.play("marche_avant", 6)
			elif back:
				f.play("marche_arriere", 6)
		"marche_avant", "marche_arriere":
			var held := (fwd if nom == "marche_avant" else back) and guard
			if not held and int(f.t) % int(f.anim.longueur) == 0 and f.t > 0.0:
				f.play("garde_idle", 6)


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
	if mode == "solo":
		_fit()
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
