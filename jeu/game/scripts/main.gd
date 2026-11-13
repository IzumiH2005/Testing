extends Node
## Chef d'orchestre : écrans (menu, jeu, vie perdue, fin d'ascension, écharpes, réglages, records, pause).

const LIVES := 4
const WorldScript := preload("res://scripts/world.gd")

enum Scr { MENU, PLAY, LOST, OFFER, SUMMARY, SKINS, SETTINGS, RECORDS, PAUSE }

var world: Node2D
var ui: CanvasLayer
var root: Control
var hud: Control
var screen: Control
var scr := Scr.MENU

var daily := true
var seed_v := 0
var lives_total := LIVES
var lives_used := 0
var extra_used := false
var life_heights: Array = []
var start_record := 0
var record_beaten := false
var accept_at := 0.0
var doubled := false
var last_shards := 0

var hud_h: Label
var hud_best: Label
var hud_lives: HBoxContainer
var hud_shards: Label
var hint: Label
var toast_l: Label
var _hint_tw: Tween
var _toast_tw: Tween

func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	randomize()
	world = WorldScript.new()
	world.process_mode = Node.PROCESS_MODE_PAUSABLE
	add_child(world)
	world.life_ended.connect(_on_life_ended)
	world.first_jump.connect(_on_first_jump)
	world.air_turn_used.connect(_on_air_turn)
	world.height_changed.connect(_on_height)
	world.shard_taken.connect(func(n): hud_shards.text = str(n))

	ui = CanvasLayer.new()
	ui.layer = 10
	add_child(ui)
	root = UIK.full(Control.new())
	root.theme = UIK.theme()
	root.mouse_filter = Control.MOUSE_FILTER_IGNORE
	ui.add_child(root)
	_build_hud()
	toast_l = UIK.label("", A.P.G)
	toast_l.set_anchors_and_offsets_preset(Control.PRESET_TOP_WIDE)
	toast_l.position.y = 70
	toast_l.modulate.a = 0.0
	root.add_child(toast_l)
	show_menu()
	for a in OS.get_cmdline_user_args():
		if a.begins_with("--shots="):
			var d: Node = load("res://tests/shot_driver.gd").new()
			add_child(d)

func _process(_dt: float) -> void:
	if scr == Scr.PLAY or scr == Scr.PAUSE:
		hud_h.text = "%d M" % world.life_best

# =================================================================== entrées

func _unhandled_input(ev: InputEvent) -> void:
	var pressed := false
	if ev is InputEventMouseButton and ev.pressed and ev.button_index == MOUSE_BUTTON_LEFT:
		pressed = true
	elif ev is InputEventKey and ev.pressed and not ev.echo and ev.keycode in [KEY_SPACE, KEY_ENTER, KEY_UP]:
		pressed = true
	elif ev is InputEventKey and ev.pressed and ev.keycode == KEY_ESCAPE:
		_back()
		return
	if not pressed:
		return
	match scr:
		Scr.PLAY:
			world.tap()
			get_viewport().set_input_as_handled()
		Scr.LOST:
			_continue_life()
			get_viewport().set_input_as_handled()

func _notification(what: int) -> void:
	match what:
		NOTIFICATION_WM_GO_BACK_REQUEST:
			_back()
		NOTIFICATION_APPLICATION_PAUSED, NOTIFICATION_APPLICATION_FOCUS_OUT:
			if scr == Scr.PLAY and world.state == world.S.PLAY:
				show_pause()

func _back() -> void:
	match scr:
		Scr.PLAY:
			show_pause()
		Scr.PAUSE:
			_resume()
		Scr.SKINS, Scr.SETTINGS, Scr.RECORDS, Scr.SUMMARY:
			Sfx.play("click")
			show_menu()
		Scr.MENU:
			get_tree().quit()

# =================================================================== HUD

func _build_hud() -> void:
	hud = UIK.full(Control.new())
	hud.mouse_filter = Control.MOUSE_FILTER_IGNORE
	root.add_child(hud)
	var m := MarginContainer.new()
	m.set_anchors_and_offsets_preset(Control.PRESET_TOP_WIDE)
	m.mouse_filter = Control.MOUSE_FILTER_IGNORE
	for k in ["left", "right", "top"]:
		m.add_theme_constant_override("margin_" + k, 4)
	hud.add_child(m)
	var row := UIK.hbox(4)
	row.alignment = BoxContainer.ALIGNMENT_BEGIN
	m.add_child(row)
	var left := UIK.vbox(1)
	left.alignment = BoxContainer.ALIGNMENT_BEGIN
	row.add_child(left)
	hud_h = UIK.label("0 M", A.P.W, 2, HORIZONTAL_ALIGNMENT_LEFT)
	left.add_child(hud_h)
	hud_best = UIK.label("", A.P.G, 1, HORIZONTAL_ALIGNMENT_LEFT)
	left.add_child(hud_best)
	var sp := Control.new()
	sp.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	sp.mouse_filter = Control.MOUSE_FILTER_IGNORE
	row.add_child(sp)
	var right := UIK.vbox(2)
	right.alignment = BoxContainer.ALIGNMENT_BEGIN
	row.add_child(right)
	hud_lives = UIK.hbox(1)
	hud_lives.alignment = BoxContainer.ALIGNMENT_END
	right.add_child(hud_lives)
	var sh := UIK.hbox(2)
	sh.alignment = BoxContainer.ALIGNMENT_END
	right.add_child(sh)
	sh.add_child(UIK.icon_rect(UIK.Ico.SHARD))
	hud_shards = UIK.label("0", A.P.G, 1, HORIZONTAL_ALIGNMENT_RIGHT)
	sh.add_child(hud_shards)
	var pause := UIK.icon_button(UIK.Ico.PAUSE)
	pause.pressed.connect(show_pause)
	row.add_child(pause)
	hint = UIK.label("", A.P.w)
	hint.set_anchors_and_offsets_preset(Control.PRESET_CENTER_BOTTOM)
	hint.grow_horizontal = Control.GROW_DIRECTION_BOTH
	hint.position = Vector2(0, 250)
	hint.size.x = 192
	hint.add_theme_color_override("font_outline_color", A.P.k)
	hint.add_theme_constant_override("outline_size", 0)
	hud.add_child(hint)
	hud.visible = false

func _refresh_lives() -> void:
	for c in hud_lives.get_children():
		c.queue_free()
	for i in lives_total:
		hud_lives.add_child(UIK.icon_rect(UIK.Ico.LIFE_USED if i < lives_used else UIK.Ico.LIFE))

func _show_hint(txt: String, col: Color = A.P.w) -> void:
	hint.text = txt
	hint.add_theme_color_override("font_color", col)
	hint.size = Vector2(192, 0)
	hint.position = Vector2(0, 236)
	if _hint_tw:
		_hint_tw.kill()
	hint.modulate.a = 1.0
	_hint_tw = create_tween().set_loops()
	_hint_tw.tween_property(hint, "modulate:a", 0.35, 0.5)
	_hint_tw.tween_property(hint, "modulate:a", 1.0, 0.5)

func _hide_hint() -> void:
	if _hint_tw:
		_hint_tw.kill()
		_hint_tw = null
	hint.modulate.a = 0.0

func toast(txt: String, col: Color = A.P.G) -> void:
	toast_l.text = txt
	toast_l.add_theme_color_override("font_color", col)
	if _toast_tw:
		_toast_tw.kill()
	toast_l.modulate.a = 1.0
	toast_l.position.y = 70
	_toast_tw = create_tween()
	_toast_tw.tween_interval(1.4)
	_toast_tw.tween_property(toast_l, "modulate:a", 0.0, 0.5)

# =================================================================== écrans : outils

func _clear_screen() -> void:
	if screen:
		screen.queue_free()
		screen = null

## Écran superposé : fond assombri + panneau centré. Renvoie la boîte verticale du panneau.
func _overlay(dim := 0.6, echo := false, width := 168) -> VBoxContainer:
	_clear_screen()
	screen = UIK.full(Control.new())
	screen.mouse_filter = Control.MOUSE_FILTER_STOP
	root.add_child(screen)
	root.move_child(toast_l, -1)
	var bg := UIK.full(ColorRect.new())
	bg.color = Color(A.P.k, dim)
	bg.mouse_filter = Control.MOUSE_FILTER_IGNORE
	screen.add_child(bg)
	var cc := UIK.full(CenterContainer.new())
	cc.mouse_filter = Control.MOUSE_FILTER_IGNORE
	screen.add_child(cc)
	var p := UIK.panel(echo)
	p.custom_minimum_size.x = width
	cc.add_child(p)
	var v := UIK.vbox(5)
	p.add_child(v)
	return v

func _title(v: Container, txt: String, col: Color = A.P.W, ico := -1) -> void:
	var h := UIK.hbox(4)
	if ico >= 0:
		h.add_child(UIK.icon_rect(ico))
	h.add_child(UIK.label(txt, col))
	v.add_child(h)
	var line := ColorRect.new()
	line.color = A.P.n
	line.custom_minimum_size = Vector2(0, 1)
	line.mouse_filter = Control.MOUSE_FILTER_IGNORE
	v.add_child(line)

func _center(c: Control) -> Control:
	c.size_flags_horizontal = Control.SIZE_SHRINK_CENTER
	return c

# =================================================================== menu

func show_menu() -> void:
	get_tree().paused = false
	scr = Scr.MENU
	hud.visible = false
	world.setup_demo(Game.daily_seed())
	_clear_screen()
	screen = UIK.full(Control.new())
	screen.mouse_filter = Control.MOUSE_FILTER_IGNORE
	root.add_child(screen)
	root.move_child(toast_l, -1)
	# voile en dégradé : lisibilité du menu sur la tour qui défile
	var grad := Gradient.new()
	grad.set_color(0, Color(A.P.k, 0.75))
	grad.set_color(1, Color(A.P.k, 0.15))
	grad.add_point(0.5, Color(A.P.k, 0.35))
	var gt := GradientTexture2D.new()
	gt.gradient = grad
	gt.fill_from = Vector2(0, 1)
	gt.fill_to = Vector2(0, 0)
	gt.width = 4
	gt.height = 64
	var veil := UIK.full(TextureRect.new())
	veil.texture = gt
	veil.stretch_mode = TextureRect.STRETCH_SCALE
	veil.mouse_filter = Control.MOUSE_FILTER_IGNORE
	screen.add_child(veil)

	var m := UIK.full(MarginContainer.new())
	m.mouse_filter = Control.MOUSE_FILTER_IGNORE
	for k in ["left", "right"]:
		m.add_theme_constant_override("margin_" + k, 10)
	m.add_theme_constant_override("margin_top", 6)
	m.add_theme_constant_override("margin_bottom", 10)
	screen.add_child(m)
	var v := UIK.vbox(4)
	v.alignment = BoxContainer.ALIGNMENT_BEGIN
	m.add_child(v)

	# barre du haut : éclats et série
	var top := UIK.hbox(3)
	v.add_child(top)
	top.add_child(UIK.icon_rect(UIK.Ico.SHARD))
	top.add_child(UIK.label(str(Game.data.shards), A.P.G, 1, HORIZONTAL_ALIGNMENT_LEFT))
	var sp := Control.new()
	sp.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	sp.mouse_filter = Control.MOUSE_FILTER_IGNORE
	top.add_child(sp)
	var st := Game.streak_alive()
	top.add_child(UIK.label(str(st), A.P.o if st > 0 else A.P.m, 1, HORIZONTAL_ALIGNMENT_RIGHT))
	var fl := UIK.icon_rect(UIK.Ico.FLAME)
	if st == 0:
		fl.modulate = Color(1, 1, 1, 0.4)
	top.add_child(fl)

	v.add_child(UIK.spacer(18))
	var logo_tx := A.tex("ui/logo")
	if logo_tx:
		var lg := TextureRect.new()
		lg.texture = logo_tx
		lg.stretch_mode = TextureRect.STRETCH_KEEP
		lg.mouse_filter = Control.MOUSE_FILTER_IGNORE
		v.add_child(_center(lg))
		var tw := create_tween().set_loops()
		tw.tween_property(lg, "position:y", lg.position.y - 2, 1.2).set_trans(Tween.TRANS_SINE)
		tw.tween_property(lg, "position:y", lg.position.y, 1.2).set_trans(Tween.TRANS_SINE)
		tw.bind_node(lg)
	else:
		v.add_child(UIK.label("ÉCHO", A.P.c, 3))
	v.add_child(UIK.label(Game.t("tagline"), A.P.p))

	var grow := Control.new()
	grow.size_flags_vertical = Control.SIZE_EXPAND_FILL
	grow.mouse_filter = Control.MOUSE_FILTER_IGNORE
	v.add_child(grow)

	# tour du jour
	var bd := UIK.button(Game.t("daily"), "main", UIK.Ico.CALENDAR, 150)
	bd.pressed.connect(func(): start_run(true))
	v.add_child(_center(bd))
	var dinfo := "%s · %s %d M" % [Game.today_short(), Game.t("best"), Game.daily_best()]
	v.add_child(UIK.label(dinfo, A.P.p))
	if Game.data.daily_bonus_day != Game.today():
		var nxt := 5 + 5 * mini(int(Game.data.streak) + 1 if Game.data.last_daily == Game.yesterday() else 1, 6)
		var bh := UIK.hbox(2)
		bh.add_child(UIK.label("%s +%d" % [Game.t("day_bonus"), nxt], A.P.G))
		bh.add_child(UIK.icon_rect(UIK.Ico.SHARD))
		v.add_child(bh)
		var tw2 := create_tween().set_loops()
		tw2.tween_property(bh, "modulate:a", 0.5, 0.6)
		tw2.tween_property(bh, "modulate:a", 1.0, 0.6)
		tw2.bind_node(bh)
	v.add_child(UIK.spacer(6))
	# ascension libre
	var bf := UIK.button(Game.t("free"), "alt", UIK.Ico.PLAY, 150)
	bf.pressed.connect(func(): start_run(false))
	v.add_child(_center(bf))
	v.add_child(UIK.label("%s %d M" % [Game.t("best"), int(Game.data.best_free)], A.P.l))
	v.add_child(UIK.spacer(10))

	var icons := UIK.hbox(10)
	v.add_child(icons)
	var b1 := UIK.icon_button(UIK.Ico.SCARF)
	b1.pressed.connect(show_skins)
	icons.add_child(b1)
	var b2 := UIK.icon_button(UIK.Ico.TROPHY)
	b2.pressed.connect(show_records)
	icons.add_child(b2)
	var b3 := UIK.icon_button(UIK.Ico.GEAR)
	b3.pressed.connect(show_settings)
	icons.add_child(b3)
	v.add_child(UIK.spacer(4))
	v.add_child(UIK.label(Game.t("echo_tip"), A.P.m))

# =================================================================== partie

func start_run(is_daily: bool) -> void:
	_clear_screen()
	daily = is_daily
	seed_v = Game.daily_seed() if daily else randi() % 1000000 + 1
	start_record = Game.daily_best() if daily else int(Game.data.best_free)
	record_beaten = false
	lives_total = LIVES
	lives_used = 0
	extra_used = false
	doubled = false
	life_heights.clear()
	world.start_ascension(seed_v, start_record)
	scr = Scr.PLAY
	hud.visible = true
	hud_shards.text = "0"
	hud_best.text = "%s %d M" % [Game.t("best"), start_record] if start_record > 0 else ""
	_refresh_lives()
	Sfx.play("start")
	_show_hint(Game.t("tap_jump") if not Game.data.tuto_done else Game.t("tap_start"))
	if daily:
		var bonus := Game.start_daily()
		if bonus > 0:
			toast("%s +%d · %s %d" % [Game.t("day_bonus"), bonus, Game.t("streak"), int(Game.data.streak)])

func _on_first_jump() -> void:
	_hide_hint()
	if not Game.data.tuto_done:
		Game.data.tuto_done = true
		Game.save()
	if not Game.data.tuto_turn_done:
		await get_tree().create_timer(0.9).timeout
		if scr == Scr.PLAY and not Game.data.tuto_turn_done and world.state == world.S.PLAY:
			_show_hint(Game.t("tap_turn"), A.P.c)
			await get_tree().create_timer(5.0).timeout
			if not Game.data.tuto_turn_done and scr == Scr.PLAY:
				_hide_hint()

func _on_air_turn() -> void:
	if not Game.data.tuto_turn_done:
		Game.data.tuto_turn_done = true
		Game.save()
		_hide_hint()

func _on_height(m: int) -> void:
	if start_record > 0 and not record_beaten and m > start_record:
		record_beaten = true
		Sfx.play("record")
		Game.vibrate(40)
		toast(Game.t("new_record"))

func _on_life_ended(info: Dictionary) -> void:
	lives_used += 1
	life_heights.append(int(info.height))
	_refresh_lives()
	if lives_used < lives_total:
		_show_lost(info)
	elif not extra_used:
		_show_offer()
	else:
		_end_run()

func _show_lost(info: Dictionary) -> void:
	scr = Scr.LOST
	_hide_hint()
	var trap: bool = info.kind == "trap"
	var v := _overlay(0.45, trap)
	_title(v, Game.t("life_lost"), A.P.z, UIK.Ico.SKULL)
	v.add_child(UIK.label(Game.t("engraved") if trap else Game.t("tide_got"), A.P.c if trap else A.P.U))
	v.add_child(UIK.label("%s %d M" % [Game.t("height"), int(info.height)], A.P.w))
	var lv := UIK.hbox(2)
	for i in lives_total:
		lv.add_child(UIK.icon_rect(UIK.Ico.LIFE_USED if i < lives_used else UIK.Ico.LIFE))
	v.add_child(lv)
	v.add_child(UIK.label("%s : %d" % [Game.t("lives_left"), lives_total - lives_used], A.P.p))
	v.add_child(UIK.spacer(2))
	var tap := UIK.label(Game.t("tap_continue"), A.P.W)
	v.add_child(tap)
	var tw := create_tween().set_loops()
	tw.tween_property(tap, "modulate:a", 0.3, 0.45)
	tw.tween_property(tap, "modulate:a", 1.0, 0.45)
	tw.bind_node(tap)
	screen.gui_input.connect(func(e: InputEvent):
		if e is InputEventMouseButton and e.pressed:
			_continue_life())
	accept_at = Time.get_ticks_msec() / 1000.0 + 0.45

func _continue_life() -> void:
	if scr != Scr.LOST or Time.get_ticks_msec() / 1000.0 < accept_at:
		return
	_clear_screen()
	scr = Scr.PLAY
	world.start_life()
	Sfx.play("start")
	_show_hint(Game.t("tap_start"))

func _show_offer() -> void:
	scr = Scr.OFFER
	_hide_hint()
	var v := _overlay(0.55, true)
	_title(v, Game.t("out_of_lives"), A.P.e, UIK.Ico.LIFE_USED)
	v.add_child(UIK.label(Game.t("extra_q"), A.P.w))
	v.add_child(UIK.label("%s %d M" % [Game.t("ascension"), world.ascension_best], A.P.p))
	v.add_child(UIK.spacer(2))
	var b := UIK.button(Game.t("extra_life"), "echo", UIK.Ico.VIDEO, 130)
	v.add_child(_center(b))
	b.pressed.connect(func():
		Ads.show_rewarded("extra_life", func():
			extra_used = true
			lives_total += 1
			_refresh_lives()
			scr = Scr.LOST
			accept_at = 0.0
			_continue_life(), Callable()))
	var n := UIK.button(Game.t("no_thanks"), "alt", -1, 130)
	n.pressed.connect(func():
		extra_used = true
		_end_run())
	v.add_child(_center(n))

func _end_run() -> void:
	_hide_hint()
	get_tree().paused = false
	var h: int = world.ascension_best
	var rec := Game.submit(daily, h)
	last_shards = world.shards_run
	Game.add_shards(last_shards)
	world.state = world.S.WAIT
	_show_summary(h, rec)

func _show_summary(h: int, rec: bool) -> void:
	scr = Scr.SUMMARY
	hud.visible = false
	var v := _overlay(0.7, false, 172)
	if rec and h > 0:
		_title(v, Game.t("new_record"), A.P.G, UIK.Ico.CROWN)
		Sfx.play("record")
	else:
		_title(v, Game.t("summary"), A.P.W, UIK.Ico.FLAME)
	v.add_child(UIK.label(("%s %s" % [Game.t("share_tower"), Game.today_short()]) if daily else Game.t("share_free"), A.P.p))
	var big := UIK.label("%d M" % h, A.P.G if rec else A.P.W, 3)
	v.add_child(big)
	# barres par vie
	var mx := 1
	for x in life_heights:
		mx = maxi(mx, int(x))
	for i in life_heights.size():
		var row := UIK.hbox(3)
		row.add_child(UIK.icon_rect(UIK.Ico.SKULL))
		var bar := ColorRect.new()
		var w := maxi(2, int(90.0 * int(life_heights[i]) / mx))
		bar.custom_minimum_size = Vector2(w, 4)
		bar.color = A.P.G if int(life_heights[i]) == h else A.P.t
		bar.size_flags_vertical = Control.SIZE_SHRINK_CENTER
		bar.mouse_filter = Control.MOUSE_FILTER_IGNORE
		var holder := Control.new()
		holder.custom_minimum_size = Vector2(92, 8)
		holder.mouse_filter = Control.MOUSE_FILTER_IGNORE
		bar.position = Vector2(0, 2)
		holder.add_child(bar)
		row.add_child(holder)
		row.add_child(UIK.label("%3d" % int(life_heights[i]), A.P.w, 1, HORIZONTAL_ALIGNMENT_RIGHT))
		v.add_child(row)
	var sh := UIK.hbox(3)
	sh.add_child(UIK.icon_rect(UIK.Ico.SHARD))
	var shl := UIK.label("+%d" % last_shards, A.P.G)
	sh.add_child(shl)
	v.add_child(sh)
	if last_shards > 0 and not doubled:
		var bx := UIK.button(Game.t("double"), "echo", UIK.Ico.VIDEO, 130)
		v.add_child(_center(bx))
		bx.pressed.connect(func():
			Ads.show_rewarded("double_shards", func():
				doubled = true
				Game.add_shards(last_shards)
				shl.text = "+%d" % (last_shards * 2)
				bx.disabled = true
				bx.text = Game.t("doubled")
				toast(Game.t("doubled"))))
	var again := UIK.button(Game.t("again"), "main", UIK.Ico.PLAY, 130)
	again.pressed.connect(func(): start_run(daily))
	v.add_child(_center(again))
	var row2 := UIK.hbox(6)
	var bs := UIK.button(Game.t("share"), "alt", UIK.Ico.SHARE, 76)
	bs.pressed.connect(func(): _share(h))
	row2.add_child(bs)
	var bm := UIK.button(Game.t("menu"), "alt", UIK.Ico.HOME, 76)
	bm.pressed.connect(show_menu)
	row2.add_child(bm)
	v.add_child(row2)

func _share(h: int) -> void:
	var head := "ÉCHO · " + (("%s %s" % [Game.t("share_tower"), Game.today_short()]) if daily else Game.t("share_free"))
	var lines := [head]
	var mx := 1
	for x in life_heights:
		mx = maxi(mx, int(x))
	for x in life_heights:
		var n := int(round(8.0 * int(x) / mx))
		lines.append("☠ " + "▰".repeat(n) + "▱".repeat(8 - n) + " %d M" % int(x))
	lines.append("▲ %d M" % h)
	DisplayServer.clipboard_set("\n".join(lines))
	toast(Game.t("copied"), A.P.c)

# =================================================================== pause

func show_pause() -> void:
	if scr != Scr.PLAY:
		return
	scr = Scr.PAUSE
	get_tree().paused = true
	var v := _overlay(0.6)
	_title(v, Game.t("paused"), A.P.W, UIK.Ico.PAUSE)
	var r := UIK.button(Game.t("resume"), "main", UIK.Ico.PLAY, 130)
	r.pressed.connect(_resume)
	v.add_child(_center(r))
	var q := UIK.button(Game.t("quit"), "alt", UIK.Ico.HOME, 130)
	q.pressed.connect(func():
		get_tree().paused = false
		if world.life_best > 0 or lives_used > 0:
			life_heights.append(world.life_best)
		_end_run())
	v.add_child(_center(q))

func _resume() -> void:
	_clear_screen()
	get_tree().paused = false
	scr = Scr.PLAY

# =================================================================== écharpes

func show_skins() -> void:
	scr = Scr.SKINS
	var v := _overlay(0.55, false, 176)
	_title(v, Game.t("skins"), A.P.W, UIK.Ico.SCARF)
	var sh := UIK.hbox(3)
	sh.add_child(UIK.icon_rect(UIK.Ico.SHARD))
	sh.add_child(UIK.label(str(Game.data.shards), A.P.G))
	v.add_child(sh)
	var grid := GridContainer.new()
	grid.columns = 2
	grid.add_theme_constant_override("h_separation", 4)
	grid.add_theme_constant_override("v_separation", 4)
	grid.mouse_filter = Control.MOUSE_FILTER_IGNORE
	v.add_child(grid)
	for s in Game.SKINS:
		grid.add_child(_skin_card(s))
	var back := UIK.button(Game.t("back"), "alt", UIK.Ico.BACK, 110)
	back.pressed.connect(show_menu)
	v.add_child(_center(back))

func _skin_card(s: Dictionary) -> Control:
	var owned := Game.owns(s.id)
	var worn: bool = Game.data.skin == s.id
	var b := UIK.button("", "main" if worn else "alt", -1, 76)
	b.custom_minimum_size = Vector2(76, 46)
	var h := UIK.hbox(3)
	UIK.full(h)
	b.add_child(h)
	var prev := TextureRect.new()
	var ptx := A.tex("sprites/player")
	if ptx:
		var at := AtlasTexture.new()
		at.atlas = ptx
		at.region = Rect2(0, 0, 16, 16)
		prev.texture = at
		var mat := ShaderMaterial.new()
		mat.shader = load("res://shaders/skin.gdshader")
		mat.set_shader_parameter("dst0", Color(s.c[0]))
		mat.set_shader_parameter("dst1", Color(s.c[1]))
		mat.set_shader_parameter("dst2", Color(s.c[2]))
		prev.material = mat
	else:
		var im := Image.create(16, 16, false, Image.FORMAT_RGBA8)
		im.fill(Color(s.c[1]))
		prev.texture = ImageTexture.create_from_image(im)
	prev.custom_minimum_size = Vector2(32, 32)
	prev.stretch_mode = TextureRect.STRETCH_SCALE
	prev.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	prev.mouse_filter = Control.MOUSE_FILTER_IGNORE
	h.add_child(prev)
	var col := UIK.vbox(1)
	h.add_child(col)
	var txt_c: Color = A.P.k if worn else A.P.w
	col.add_child(UIK.label(s.name_fr if Game.lang == "fr" else s.name_en, txt_c, 1, HORIZONTAL_ALIGNMENT_LEFT))
	var info := UIK.hbox(2)
	info.alignment = BoxContainer.ALIGNMENT_BEGIN
	if worn:
		info.add_child(UIK.icon_rect(UIK.Ico.CHECK))
	elif owned:
		info.add_child(UIK.label(Game.t("equip"), A.P.c, 1, HORIZONTAL_ALIGNMENT_LEFT))
	else:
		info.add_child(UIK.icon_rect(UIK.Ico.SHARD))
		var afford := int(Game.data.shards) >= int(s.price)
		info.add_child(UIK.label(str(s.price), A.P.G if afford else A.P.m, 1, HORIZONTAL_ALIGNMENT_LEFT))
	col.add_child(info)
	b.pressed.connect(func():
		if Game.owns(s.id):
			Game.buy(s.id)
			world.apply_skin()
			show_skins()
		elif Game.buy(s.id):
			Sfx.play("reward")
			world.apply_skin()
			show_skins()
		else:
			Sfx.play("deny")
			toast(Game.t("not_enough"), A.P.z))
	return b

# =================================================================== réglages

func show_settings() -> void:
	scr = Scr.SETTINGS
	var v := _overlay(0.55, false, 168)
	_title(v, Game.t("settings"), A.P.W, UIK.Ico.GEAR)
	_toggle_row(v, "sound", UIK.Ico.SOUND_ON if Game.data.sound else UIK.Ico.SOUND_OFF)
	_toggle_row(v, "music", UIK.Ico.SOUND_ON if Game.data.music else UIK.Ico.SOUND_OFF)
	_toggle_row(v, "vibration", UIK.Ico.VIBRATION)
	var row := UIK.hbox(4)
	row.add_child(UIK.label(Game.t("language"), A.P.w, 1, HORIZONTAL_ALIGNMENT_LEFT))
	row.get_child(0).size_flags_horizontal = Control.SIZE_EXPAND_FILL
	var lb := UIK.button("FR" if Game.lang == "fr" else "EN", "alt", -1, 44)
	lb.pressed.connect(func():
		Game.set_lang("en" if Game.lang == "fr" else "fr")
		show_settings())
	row.add_child(lb)
	v.add_child(row)
	v.add_child(UIK.spacer(4))
	var back := UIK.button(Game.t("back"), "alt", UIK.Ico.BACK, 110)
	back.pressed.connect(show_menu)
	v.add_child(_center(back))
	v.add_child(UIK.label("V0.1 · ÉCHO", A.P.n))

func _toggle_row(v: Container, key: String, ico: int) -> void:
	var row := UIK.hbox(4)
	row.add_child(UIK.icon_rect(ico))
	var l := UIK.label(Game.t(key), A.P.w, 1, HORIZONTAL_ALIGNMENT_LEFT)
	l.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	row.add_child(l)
	var on: bool = Game.data[key]
	var b := UIK.button(Game.t("on") if on else Game.t("off"), "main" if on else "alt", -1, 44)
	b.pressed.connect(func():
		Game.data[key] = not Game.data[key]
		Game.save()
		Sfx.update_music()
		if key == "vibration":
			Game.vibrate(30)
		show_settings())
	row.add_child(b)
	v.add_child(row)

# =================================================================== records

func show_records() -> void:
	scr = Scr.RECORDS
	var v := _overlay(0.55, false, 172)
	_title(v, Game.t("records"), A.P.G, UIK.Ico.TROPHY)
	_stat(v, Game.t("best_free"), "%d M" % int(Game.data.best_free))
	_stat(v, Game.t("today_best"), "%d M" % Game.daily_best())
	_stat(v, Game.t("streak"), "%d %s" % [Game.streak_alive(), Game.t("days")])
	_stat(v, Game.t("runs"), str(Game.data.runs))
	_stat(v, Game.t("total"), "%d M" % int(Game.data.total_m))
	v.add_child(UIK.spacer(2))
	v.add_child(UIK.label(Game.t("last_days"), A.P.p))
	# histogramme des 7 dernières tours du jour
	var days := []
	var now := Time.get_unix_time_from_system()
	var mx := 1
	for i in range(6, -1, -1):
		var d := Time.get_date_dict_from_unix_time(int(now - 86400.0 * i))
		var key := "%04d-%02d-%02d" % [d.year, d.month, d.day]
		var val := int(Game.data.daily.get(key, 0))
		mx = maxi(mx, val)
		days.append([d.day, val])
	var chart := UIK.hbox(4)
	chart.alignment = BoxContainer.ALIGNMENT_CENTER
	for dd in days:
		var col := UIK.vbox(1)
		col.alignment = BoxContainer.ALIGNMENT_END
		var hh := int(30.0 * int(dd[1]) / mx)
		var holder := Control.new()
		holder.custom_minimum_size = Vector2(14, 30)
		holder.mouse_filter = Control.MOUSE_FILTER_IGNORE
		var bar := ColorRect.new()
		bar.color = A.P.c if int(dd[1]) > 0 else A.P.n
		bar.size = Vector2(10, maxi(1, hh))
		bar.position = Vector2(2, 30 - maxi(1, hh))
		bar.mouse_filter = Control.MOUSE_FILTER_IGNORE
		holder.add_child(bar)
		col.add_child(holder)
		col.add_child(UIK.label("%02d" % int(dd[0]), A.P.m))
		chart.add_child(col)
	v.add_child(chart)
	v.add_child(UIK.spacer(2))
	var back := UIK.button(Game.t("back"), "alt", UIK.Ico.BACK, 110)
	back.pressed.connect(show_menu)
	v.add_child(_center(back))

func _stat(v: Container, k: String, val: String) -> void:
	var row := UIK.hbox(4)
	var l := UIK.label(k, A.P.p, 1, HORIZONTAL_ALIGNMENT_LEFT)
	l.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	row.add_child(l)
	row.add_child(UIK.label(val, A.P.W, 1, HORIZONTAL_ALIGNMENT_RIGHT))
	v.add_child(row)
