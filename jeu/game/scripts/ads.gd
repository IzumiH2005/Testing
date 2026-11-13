extends Node
## Publicités. v1 : SIMULATION (aucun SDK). L'interface est celle qu'utilisera le plugin AdMob :
##   Ads.show_rewarded(placement, on_reward, on_cancel)
## Placements : "extra_life" (+1 vie, 1 fois par ascension), "double_shards" (x2 éclats en fin d'ascension).
## Aucune pub imposée : le joueur choisit toujours.

signal ad_finished(placement: String, rewarded: bool)

const MOCK_SECONDS := 3
var _layer: CanvasLayer
var showing := false
var watched_today := 0

func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS

func is_ready(_placement: String) -> bool:
	return true

func show_rewarded(placement: String, on_reward: Callable, on_cancel: Callable = Callable()) -> void:
	if showing:
		return
	showing = true
	get_tree().paused = true
	_layer = CanvasLayer.new()
	_layer.layer = 100
	add_child(_layer)
	var root := UIK.full(Control.new())
	root.theme = UIK.theme()
	_layer.add_child(root)
	var bg := UIK.full(ColorRect.new())
	bg.color = A.P.k
	root.add_child(bg)
	var v := UIK.vbox(8)
	UIK.full(v)
	root.add_child(v)
	v.add_child(UIK.label(Game.t("ad_title"), A.P.p))
	v.add_child(UIK.icon_rect(UIK.Ico.VIDEO, 4))
	v.get_child(1).size_flags_horizontal = Control.SIZE_SHRINK_CENTER
	v.add_child(UIK.label(Game.t("ad_mock"), A.P.l))
	var cnt := UIK.label("", A.P.c)
	v.add_child(cnt)
	var close := UIK.button("X", "alt", -1, 24)
	close.position = Vector2(4, 4)
	root.add_child(close)
	var cancelled := [false]
	close.pressed.connect(func():
		cancelled[0] = true
		_close()
		ad_finished.emit(placement, false)
		if on_cancel.is_valid():
			on_cancel.call())
	for i in range(MOCK_SECONDS, 0, -1):
		if cancelled[0]:
			return
		cnt.text = "%s %d" % [Game.t("ad_reward"), i]
		await get_tree().create_timer(1.0, true).timeout
	if cancelled[0]:
		return
	_close()
	watched_today += 1
	Sfx.play("reward")
	ad_finished.emit(placement, true)
	on_reward.call()

func _close() -> void:
	showing = false
	get_tree().paused = false
	if _layer:
		_layer.queue_free()
		_layer = null
