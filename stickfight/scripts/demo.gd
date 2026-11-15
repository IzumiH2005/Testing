extends Control
## Démo des animations : un combattant seul ou le duo coup de pied /
## blocage. Le temps avance à 60 images par seconde, comme dans le jeu ; on
## peut figer, avancer et reculer image par image, ralentir, et afficher le
## squelette.
##
## Le repos est l'état par défaut ; la garde ne dure que tant que G est tenu.
##   → / ←  maintenus : marche détendue avant / arrière depuis le repos ;
##      relâchés, le combattant finit son pas et s'arrête au repos.
##   Maj + →  course ;  Ctrl + →  sprint (départ explosif, freinage en glissade).
##   G  maintenu : mise en garde (garde ouverte) ; avec →, marche en garde ;
##      ← ferme la garde (défensive) et recule ; → → (double
##      appui) dash avant, ← ← dash arrière ; ↓ maintenu, accroupi ;
##      ↓ + ←, garde basse (accroupi, garde fermée) ;
##      relâché, le combattant sort de la garde et revient au repos.
##   ↓  maintenu depuis le repos : accroupi, une main au sol ; relâché, il se
##      relève au repos.
##   ↑  depuis le repos : saut sur place ; ↑ + → saut avant, ↑ + ← saut arrière.
##   H  en garde : encaisser un coup bloqué (recul sur garde ; haut debout,
##      bas en garde basse) ; H léger, Maj + H moyen, Ctrl + H lourd ;
##      Ctrl + Maj + H : très gros coup, la garde est repoussée (les pieds
##      glissent loin ; en garde basse, recul lourd).
##   J  en garde : coup qui brise la garde (bras ouverts, vulnérable ;
##      en garde basse, recul lourd).
##   P  en garde : parade (dévie le coup ; varie selon le coup) ; P coup de
##      poing haut, Maj + P coup de pied haut, Ctrl + P coup moyen,
##      Ctrl + Maj + P coup bas. Pendant la fenêtre de contre d'une parade,
##      une autre parade peut l'annuler (la contre-attaque, elle, sera propre
##      à chaque personnage). Touches provisoires : les commandes finales
##      seront à la manette, façon Tekken (□ △ × ○ = 1 2 3 4).
##   1 à 7  au repos (ou en garde) : esquive détendue, sans garde, façon
##      « ultra instinct », qui finit au repos (varie selon le coup) ; 1 sway (direct au
##      visage), 2 slip (direct, la tête passe à côté), 3 baisse (crochet ou
##      circulaire à la tête), 4 retrait du ventre (crochet au corps),
##      5 pas de côté, pivot face caméra (coup de pied appuyé), 6 saut arrière (coup de pied
##      hache), 7 saut sur place (balayage). Pendant la fenêtre de contre
##      d'une parade ou d'une esquive, une esquive peut partir. Touches
##      provisoires, comme P.
##   B  blocage bas (en garde)   K  duo coup de pied direct + blocage bas
##   R  repos (remise à zéro)
##   Espace  pause    → / ←  image suivante / précédente (en pause)
##   L  ralenti ×4    D  squelette

const DUO := "res://anims/duo_blocage.json"
const HISTORY_MAX := 600
## Écart maximal, en images, entre les deux appuis sur → d'un dash.
const DOUBLE_APPUI := 14
## Images en garde fermée, sans ← ni action, avant qu'elle se rouvre.
const ROUVRIR := 10
## Images au début d'un départ de marche pendant lesquelles ↑ le change
## encore en saut (→ ou ← enfoncée un peu avant ↑).
const SAUT_TOLERANCE := 6
## Images minimales passées dans accroupi_repos_idle avant qu'une propulsion
## puisse partir (le fondu de retour de la propulsion précédente se termine).
const PROPULSION_DELAI := 4
const HELP := "→ ← marcher   Maj + → courir   Ctrl + → sprinter   ↓ accroupi   ↑ sauter (+ → / ← : avant / arrière)   Maj + ↑ saut boosté   ↓ puis → / ← propulsion (+ ↑ haute)   G tenu : garde (→ avancer, ← fermer et reculer, → → dash, ← ← backdash, ↓ accroupi, ↓ + ← garde basse, B blocage bas, T demi-tour, H / Maj + H / Ctrl + H coup bloqué, Ctrl + Maj + H garde repoussée, J garde brisée, P / Maj + P / Ctrl + P / Ctrl + Maj + P parade haute poing / haute pied / moyenne / basse)   1 à 7 esquive détendue sway / slip / baisse / retrait / côté / saut arrière / saut balayage   K duo   R repos   ·   Espace pause   ← → image par image   L ralenti   D squelette"

## Esquives des touches 1 à 7, dans l'ordre.
const ESQUIVES := ["sway", "slip", "baisse", "retrait", "cote", "saut_arriere", "saut_balayage"]

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
## Image (tick) du dernier appui sur →, pour reconnaître le double appui.
var last_fwd_press := -1000
var last_back_press := -1000
## Double appui sur → ou ← reçu, consommé à la prochaine image par _control_input.
var dash_req := false
var backdash_req := false
## T appuyé (demi-tour), consommé de la même façon.
var tour_req := false
## H appuyé : force du coup bloqué à encaisser ("" = aucun), consommé de même.
var coup_req := ""
## P appuyé : parade à jouer ("" = aucune), consommée de même.
var parade_req := ""
## 1 à 7 appuyé : esquive à jouer ("" = aucune), consommée de même.
var esquive_req := ""
## Images passées en garde basse sans ←, pour la rouvrir après ROUVRIR.
var gb_sans_recul := 0
## Centre de la caméra en solo (suit le bassin avec un peu de retard).
var cam_x := 8.0
## Vitesse lissée du bassin : la caméra regarde devant quand on court.
var cam_v := 0.0
var last_hip := 0.0


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
		cam_v = 0.0
		last_hip = 0.0
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
		cam_v += (hip - last_hip - cam_v) * 0.1
		last_hip = hip
		cam_x += (hip + 8.0 + 12.0 * cam_v - cam_x) * 0.08
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
	"sprint": {0: "sprint_arret_n", 14: "sprint_arret_f"},
}


## Clavier tenu, lu à chaque image :
## - depuis le repos, → / ← lancent la marche détendue ; relâchées, la marche
##   s'arrête à la prochaine image d'arrêt de la boucle (ARRETS) et revient au
##   repos ;
## - Maj + → depuis le repos lance la course (départ, boucle) ; relâchées,
##   elle freine à la prochaine pose d'appui (image 0 ou 20) et revient au repos ;
## - Ctrl + → depuis le repos lance le sprint ; relâchées, il freine en
##   glissade à la prochaine pose d'appui (image 0 ou 14) ;
## - ↓ tenu depuis le repos : accroupi détendu, une main posée au sol ;
##   relâché, il se relève au repos ;
## - ↑ depuis le repos : saut sur place ; ↑ + → saut avant, ↑ + ← saut arrière.
##   Chaque saut finit accroupi sur la pose d'amorti commune, puis enchaîne
##   la réception (reception) et le repos. ↑ dans les SAUT_TOLERANCE
##   premières images d'un départ de marche le change en saut avant / arrière
##   (en saut boosté si Maj est tenue, y compris pendant un départ de course) ;
## - Maj + ↑ depuis le repos : saut boosté (+ → / ← : avant / arrière). Les
##   jambes se contractent plus, il monte plus haut et retombe sur trois appuis
##   (main au sol), puis enchaîne la réception lourde et le repos ;
## - accroupi (↓ tenu) : → / ← propulsion rasante avant / arrière, ↑ + → / ←
##   propulsion haute. Elle repart de la pose accroupie main au sol et y
##   revient ; → / ← encore tenue après PROPULSION_DELAI images relance ;
## - G tenu met en garde (depuis le repos) : garde ouverte, prête à se battre ;
##   → y fait la marche en garde, qui s'arrête à l'image 0 de son cycle ;
## - ← en garde ouverte ferme la garde (garde défensive, comme on bloque en
##   reculant) puis recule en garde fermée ; sans ← ni action pendant
##   ROUVRIR images, la garde fermée se rouvre ;
## - G relâché, en garde (ouverte ou fermée), joue la sortie de garde ;
## - en garde, → → (deux appuis en moins de DOUBLE_APPUI images) lance le dash
##   avant, depuis l'arrêt ou dans les premières images de la marche en garde
##   lancée par le premier appui ; il revient en garde ouverte. ← ← lance le
##   dash arrière, qui ferme la garde ;
## - ↓ tenu en garde : accroupi, qui se relève en garde ouverte ;
## - ↓ + ← en garde : garde basse (accroupi, garde fermée), qui se relève en
##   garde fermée. Accroupi en garde ouverte, ← ferme la garde basse ; sans ←
##   pendant ROUVRIR images, elle se rouvre en accroupi ;
## - T en garde : demi-tour sur place, qui finit en garde ouverte tournée de
##   l'autre côté. Les flèches restent celles de l'écran : retourné, → recule
##   et ← avance.
func _control_input() -> void:
	var dash := dash_req
	var backdash := backdash_req
	var tour := tour_req
	dash_req = false
	backdash_req = false
	tour_req = false
	var coup := coup_req
	coup_req = ""
	var parade := parade_req
	parade_req = ""
	var esquive := esquive_req
	esquive_req = ""
	var f: Fighter = combat.fighters[0]
	var right := Input.is_physical_key_pressed(KEY_RIGHT)
	var left := Input.is_physical_key_pressed(KEY_LEFT)
	if f.facing < 0:
		var tmp := right
		right = left
		left = tmp
		var td := dash
		dash = backdash
		backdash = td
	var fwd := right
	var back := left and not fwd
	var guard := Input.is_physical_key_pressed(KEY_G)
	var run := Input.is_physical_key_pressed(KEY_SHIFT)
	var sprint := Input.is_physical_key_pressed(KEY_CTRL)
	var down := Input.is_physical_key_pressed(KEY_DOWN)
	var up := Input.is_physical_key_pressed(KEY_UP)
	var nom := f.anim_name()
	# Coup bloqué : recul sur garde, debout ou accroupi. Un recul peut en
	# interrompre un autre (série de coups bloqués).
	if coup != "":
		if nom in ["garde_basse", "garde_basse_fermer"] or nom.begins_with("recul_garde_bas_"):
			gb_sans_recul = 0
			f.play("recul_garde_bas_" + ("lourd" if coup in ["repousse", "brise"] else coup), 1)
			return
		if nom in ["garde_ouverte_idle", "garde_ouvrir", "garde_idle", "garde_fermer"] \
				or nom.begins_with("recul_garde_haut_") or nom == "garde_repoussee":
			f.play("garde_brisee" if coup == "brise" else "garde_repoussee" if coup == "repousse" \
					else "recul_garde_haut_" + coup, 1)
			return
	# Parade : depuis la garde debout, ou pendant la fenêtre de contre d'une
	# autre parade (une parade en enchaîne une autre, comme le ferait une
	# contre-attaque propre au personnage).
	if parade != "":
		if nom in ["garde_ouverte_idle", "garde_ouvrir", "garde_idle", "garde_fermer"] \
				or nom.begins_with("recul_garde_haut_") \
				or (nom.begins_with("parade_") and f.en_fenetre("contre")):
			f.play(parade, 2)
			return
	# Esquive : depuis le repos (esquive détendue, sans garde), la marche
	# détendue, la garde debout, ou pendant la fenêtre de contre d'une parade
	# ou d'une autre esquive. Elle se termine toujours dans idle_repos.
	if esquive != "":
		if nom in ["idle_repos", "garde_ouverte_idle", "garde_ouvrir", "garde_idle", "garde_fermer"] \
				or nom.begins_with("marche_detendue") \
				or nom.begins_with("recul_garde_haut_") \
				or ((nom.begins_with("parade_") or nom.begins_with("esquive_")) and f.en_fenetre("contre")):
			f.play(esquive, 2)
			return
	match nom:
		"idle_repos":
			if up and run:
				f.play("saut_booste_avant" if fwd else "saut_booste_arriere" if back
						else "saut_booste_neutre", 4)
			elif up:
				f.play("saut_avant" if fwd else "saut_arriere" if back else "saut_neutre", 4)
			elif guard:
				f.play("mise_en_garde", 4)
			elif fwd and sprint:
				f.play("sprint_depart", 6)
			elif fwd and run:
				f.play("course_depart", 6)
			elif fwd:
				f.play("marche_detendue_depart", 6)
			elif back:
				f.play("marche_detendue_arriere_depart", 6)
			elif down:
				f.play("accroupi_repos_entree", 4)
		"marche_detendue_depart", "marche_detendue_arriere_depart":
			if up and f.t < SAUT_TOLERANCE:
				var avant := nom == "marche_detendue_depart"
				if run:
					f.play("saut_booste_avant" if avant else "saut_booste_arriere", 3)
				else:
					f.play("saut_avant" if avant else "saut_arriere", 3)
		"course_depart":
			if up and f.t < SAUT_TOLERANCE:
				f.play("saut_booste_avant", 3)
		"accroupi_repos_idle":
			if not down:
				f.play("accroupi_repos_sortie", 3)
			elif (fwd or back) and f.t >= PROPULSION_DELAI:
				var cote := "avant" if fwd else "arriere"
				f.play("propulsion_" + cote + ("_haute" if up else ""), 3)
		"marche_detendue", "marche_detendue_arriere", "course", "sprint":
			var held: bool = {"marche_detendue": fwd, "marche_detendue_arriere": back,
					"course": fwd and run, "sprint": fwd and sprint}[nom]
			var phase := int(f.t) % int(f.anim.longueur)
			if not held and ARRETS[nom].has(phase):
				f.play(ARRETS[nom][phase], 0)
		"garde_ouverte_idle", "garde_ouvrir", "garde_idle", "garde_fermer":
			_guard_input(f, nom, guard, fwd, back, down, dash, backdash, tour)
		"accroupi_idle", "garde_basse_ouvrir":
			if not (down and guard):
				f.play("accroupi_sortie", 3 if nom == "accroupi_idle" else 5)
			elif back:
				gb_sans_recul = 0
				f.play("garde_basse_fermer", 0 if nom == "accroupi_idle" else 4)
		"garde_basse":
			gb_sans_recul = 0 if back else gb_sans_recul + 1
			if not (down and guard):
				f.play("garde_basse_sortie", 3)
			elif gb_sans_recul >= ROUVRIR:
				f.play("garde_basse_ouvrir", 0)
		"marche_avant", "marche_arriere":
			if dash and guard and nom == "marche_avant" and f.t < DOUBLE_APPUI:
				f.play("dash_avant", 4)
				return
			if backdash and guard and nom == "marche_arriere" and f.t < DOUBLE_APPUI:
				f.play("dash_arriere", 4)
				return
			var held := (fwd if nom == "marche_avant" else back) and guard
			if not held and int(f.t) % int(f.anim.longueur) == 0 and f.t > 0.0:
				f.play("garde_ouverte_idle" if nom == "marche_avant" else "garde_idle", 6)



## Garde ouverte (garde_ouverte_idle, garde_ouvrir) et garde fermée
## (garde_idle, garde_fermer) : mêmes jambes, seuls le buste et les bras
## changent, d'où des fondus courts entre les deux.
func _guard_input(f: Fighter, nom: String, guard: bool, fwd: bool, back: bool,
		down: bool, dash: bool, backdash: bool, tour: bool) -> void:
	var ouverte := nom in ["garde_ouverte_idle", "garde_ouvrir"]
	if not guard:
		f.play("sortie_de_garde", 6)
	elif down and back:
		gb_sans_recul = 0
		f.play("garde_basse_entree", 5 if ouverte else 3)
	elif down:
		f.play("accroupi_entree", 3 if ouverte else 5)
	elif dash:
		f.play("dash_avant", 4)
	elif backdash:
		f.play("dash_arriere", 4)
	elif tour:
		f.play("demi_tour", 0 if nom == "garde_ouverte_idle" else 4)
	elif fwd:
		f.play("marche_avant", 6)
	elif back:
		if ouverte:
			f.play("garde_fermer", 0 if nom == "garde_ouverte_idle" else 4)
		elif nom == "garde_idle" or f.t >= 4.0:
			f.play("marche_arriere", 4 if nom == "garde_fermer" else 6)
	elif nom == "garde_idle" and f.t >= ROUVRIR:
		f.play("garde_ouvrir", 0)


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
			elif not ev.echo:
				dash_req = tick - last_fwd_press <= DOUBLE_APPUI * slow
				last_fwd_press = tick
		KEY_LEFT:
			if paused:
				_step_back()
			elif not ev.echo:
				backdash_req = tick - last_back_press <= DOUBLE_APPUI * slow
				last_back_press = tick
		KEY_T:
			if not ev.echo:
				tour_req = true
		KEY_H:
			if not ev.echo:
				coup_req = ("repousse" if ev.shift_pressed else "lourd") if ev.ctrl_pressed \
						else "moyen" if ev.shift_pressed else "leger"
		KEY_J:
			if not ev.echo:
				coup_req = "brise"
		KEY_P:
			if not ev.echo:
				parade_req = ("parade_basse" if ev.shift_pressed else "parade_moyenne") \
						if ev.ctrl_pressed else "parade_haute_pied" if ev.shift_pressed \
						else "parade_haute_poing"
		KEY_1, KEY_2, KEY_3, KEY_4, KEY_5, KEY_6, KEY_7:
			if not ev.echo:
				esquive_req = "esquive_" + ESQUIVES[ev.keycode - KEY_1]
		KEY_L:
			slow = 4 if slow == 1 else 1
			_refresh()
		KEY_D:
			planche.debug = not planche.debug
			planche.queue_redraw()
		_:
			return
	accept_event()
