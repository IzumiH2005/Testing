extends Node
## Sons : petits WAV synthétisés (tools/sfx.py) + boucle de musique.

const NAMES := ["jump", "turn", "land", "shard", "die", "engrave", "click", "record", "reward", "laser", "start", "deny"]
var streams := {}
var players: Array = []
var music: AudioStreamPlayer
var _next := 0

func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	for n in NAMES:
		var p := "res://audio/%s.wav" % n
		if ResourceLoader.exists(p):
			streams[n] = load(p)
	for i in 8:
		var a := AudioStreamPlayer.new()
		add_child(a)
		players.append(a)
	music = AudioStreamPlayer.new()
	music.volume_db = -6.0
	add_child(music)
	if ResourceLoader.exists("res://audio/music.wav"):
		var m: AudioStreamWAV = load("res://audio/music.wav")
		m.loop_mode = AudioStreamWAV.LOOP_FORWARD
		m.loop_begin = 0
		m.loop_end = int(m.get_length() * m.mix_rate)
		music.stream = m
	update_music()

func play(n: String, pitch := 1.0) -> void:
	if not Game.data.sound or not streams.has(n):
		return
	var a: AudioStreamPlayer = players[_next]
	_next = (_next + 1) % players.size()
	a.stream = streams[n]
	a.pitch_scale = pitch * randf_range(0.97, 1.03)
	a.play()

func update_music() -> void:
	if music.stream == null:
		return
	if Game.data.music and not music.playing:
		music.play()
	elif not Game.data.music and music.playing:
		music.stop()
