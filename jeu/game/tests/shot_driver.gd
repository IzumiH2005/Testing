extends Node
## Pilote de captures d'écran automatiques (développement uniquement).
## Lancement : godot --path . -- --shots=/chemin/sortie

var out := ""
var main: Node
var n := 0

func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	main = get_parent()
	for a in OS.get_cmdline_user_args():
		if a.begins_with("--shots="):
			out = a.substr(8)
	DirAccess.make_dir_recursive_absolute(out)
	_run()

func shot(name: String) -> void:
	await RenderingServer.frame_post_draw
	var img := get_viewport().get_texture().get_image()
	n += 1
	img.save_png("%s/%02d_%s.png" % [out, n, name])

func wait(s: float) -> void:
	await get_tree().create_timer(s, true, false, true).timeout

## petit robot : saute dès qu'il est accroché depuis un moment, fait parfois un demi-tour
func bot(seconds: float, turn_every := 0) -> void:
	var w = main.world
	var t := 0.0
	var k := 0
	while t < seconds and main.scr == main.Scr.PLAY:
		await get_tree().physics_frame
		t += 1.0 / 60.0
		if w.state == w.S.READY:
			w.tap()
		elif w.state == w.S.PLAY and w.side != 0 and w.grip > 0.12:
			w.tap()
			k += 1
			if turn_every > 0 and k % turn_every == 0:
				await wait(0.12)
				w.tap()

func _run() -> void:
	Game.data.tuto_done = false
	Game.data.tuto_turn_done = false
	Game.data.shards = 240
	await wait(1.2)
	await shot("menu")
	main.start_run(true)
	await wait(0.6)
	await shot("ready")
	main.world.tap()
	await wait(0.25)
	await shot("first_jump")
	await bot(2.0)
	await shot("play_a")
	await bot(3.0, 3)
	await shot("play_b")
	# attendre une mort
	var guard := 0.0
	while main.scr == main.Scr.PLAY and guard < 40.0:
		await bot(1.0)
		guard += 1.0
	await wait(0.3)
	await shot("life_lost")
	await wait(0.6)
	main._continue_life()
	await wait(0.2)
	await bot(4.0)
	await shot("life2_echo")
	main.show_pause()
	await wait(0.3)
	await shot("pause")
	main._resume()
	main.lives_used = main.lives_total - 1
	guard = 0.0
	while main.scr == main.Scr.PLAY and guard < 40.0:
		await bot(1.0)
		guard += 1.0
	await wait(0.3)
	await shot("offer")
	if main.scr == main.Scr.OFFER:
		main.extra_used = true
		main._end_run()
	await wait(0.4)
	await shot("summary")
	main.show_skins()
	await wait(0.3)
	await shot("skins")
	main.show_settings()
	await wait(0.3)
	await shot("settings")
	main.show_records()
	await wait(0.3)
	await shot("records")
	Ads.show_rewarded("test", func(): pass)
	await wait(0.5)
	await shot("ad")
	await wait(3.5)
	main.show_menu()
	await wait(0.5)
	await shot("menu_after")
	get_tree().quit()
