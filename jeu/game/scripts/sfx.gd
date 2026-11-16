extends Node
## Sons : petits WAV synthétisés (tools/sfx.py) + musique (audio/music.ogg, boucle).
##
## La musique suit le jeu :
## - en partie, son tempo suit la vitesse de déplacement du héros (lissée) : 0,85 à 1,25 ;
##   le bus « Music » compense la hauteur (AudioEffectPitchShift) : le morceau accélère
##   sans devenir aigu ;
## - menu : volume un peu plus bas, tempo normal ;
## - pause : volume bas et son étouffé (passe-bas) ;
## - vie perdue / fin d'ascension : le tempo retombe et le volume baisse.

const NAMES := ["jump", "turn", "land", "shard", "die", "engrave", "click", "record", "reward", "laser", "start", "deny"]

## Ambiances de la musique (choisies par main.gd selon l'écran).
enum Mood { MENU, READY, PLAY, PAUSE, DEATH, SUMMARY }

const TEMPO_MIN := 0.85
const TEMPO_MAX := 1.25
## Vitesse moyenne du héros (px/s, lissée) qui donne TEMPO_MIN et TEMPO_MAX.
const SPEED_SLOW := 30.0
const SPEED_FAST := 230.0
## Temps de réponse (s) : vitesse moyenne, puis tempo (deux lissages : pas d'à-coups).
const SPEED_SMOOTH := 1.2
const TEMPO_SMOOTH := 0.8
## Variation maximale du tempo par seconde.
const TEMPO_RATE := 0.35
## Volumes (dB) par ambiance.
const VOL := {Mood.MENU: -9.0, Mood.READY: -8.0, Mood.PLAY: -7.0, Mood.PAUSE: -18.0, Mood.DEATH: -13.0, Mood.SUMMARY: -11.0}
const CUTOFF_OPEN := 20000.0
const CUTOFF_PAUSE := 900.0

var streams := {}
var players: Array = []
var music: AudioStreamPlayer
var mood: int = Mood.MENU
var speed_avg := 0.0       # vitesse lissée du héros
var tempo := 1.0           # tempo courant (pitch_scale du lecteur)
var _speed_in := 0.0       # dernière vitesse reçue (main.gd, chaque image)
var _vol := -9.0
var _cutoff := CUTOFF_OPEN
var _bus := -1
var _shift: AudioEffectPitchShift
var _lowpass: AudioEffectLowPassFilter
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
	_make_music_bus()
	music = AudioStreamPlayer.new()
	music.bus = "Music" if _bus >= 0 else "Master"
	music.volume_db = _vol
	add_child(music)
	if ResourceLoader.exists("res://audio/music.ogg"):
		var o: AudioStreamOggVorbis = load("res://audio/music.ogg")
		o.loop = true
		o.loop_offset = 0.0
		music.stream = o
	elif ResourceLoader.exists("res://audio/music.wav"):
		var m: AudioStreamWAV = load("res://audio/music.wav")
		m.loop_mode = AudioStreamWAV.LOOP_FORWARD
		m.loop_begin = 0
		m.loop_end = int(m.get_length() * m.mix_rate)
		music.stream = m
	update_music()

## Bus « Music » : compensation de hauteur (le tempo change, pas la note) + passe-bas pour la pause.
func _make_music_bus() -> void:
	_bus = AudioServer.get_bus_index("Music")
	if _bus < 0:
		AudioServer.add_bus()
		_bus = AudioServer.bus_count - 1
		AudioServer.set_bus_name(_bus, "Music")
		AudioServer.set_bus_send(_bus, "Master")
	_shift = AudioEffectPitchShift.new()
	_shift.pitch_scale = 1.0
	_shift.oversampling = 4
	_shift.fft_size = AudioEffectPitchShift.FFT_SIZE_1024
	AudioServer.add_bus_effect(_bus, _shift, 0)
	_lowpass = AudioEffectLowPassFilter.new()
	_lowpass.cutoff_hz = CUTOFF_OPEN
	AudioServer.add_bus_effect(_bus, _lowpass, 1)
	AudioServer.set_bus_effect_enabled(_bus, 1, false)

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

## Change l'ambiance de la musique (appelé par main.gd à chaque écran).
func set_mood(m: int) -> void:
	mood = m

## Vitesse du héros en px/s (appelé chaque image par main.gd pendant la partie).
func feed_speed(v: float) -> void:
	_speed_in = v

## Tempo visé pour une vitesse moyenne donnée (testable sans audio).
static func tempo_for_speed(v: float) -> float:
	var k := clampf((v - SPEED_SLOW) / (SPEED_FAST - SPEED_SLOW), 0.0, 1.0)
	k = k * k * (3.0 - 2.0 * k)  # courbe douce aux extrémités
	return lerpf(TEMPO_MIN, TEMPO_MAX, k)

func _target_tempo() -> float:
	match mood:
		Mood.PLAY:
			return tempo_for_speed(speed_avg)
		Mood.READY:
			return 0.95
		Mood.PAUSE:
			return tempo  # on fige le tempo
		Mood.DEATH:
			return TEMPO_MIN
		Mood.SUMMARY:
			return 0.92
	return 1.0

func _process(dt: float) -> void:
	if music == null:
		return
	# 1) vitesse moyenne du héros (lissage exponentiel)
	var v := _speed_in if mood == Mood.PLAY else 0.0
	if mood != Mood.PAUSE:
		speed_avg += (v - speed_avg) * (1.0 - exp(-dt / SPEED_SMOOTH))
	# 2) tempo : lissage + vitesse de variation bornée
	var goal := _target_tempo()
	var step := (goal - tempo) * (1.0 - exp(-dt / TEMPO_SMOOTH))
	step = clampf(step, -TEMPO_RATE * dt, TEMPO_RATE * dt)
	tempo = clampf(tempo + step, TEMPO_MIN, TEMPO_MAX)
	music.pitch_scale = tempo
	if _shift:
		_shift.pitch_scale = 1.0 / tempo
		# à tempo normal, pas de traitement (aucun artefact, moins de calcul)
		AudioServer.set_bus_effect_enabled(_bus, 0, absf(tempo - 1.0) > 0.01)
	# 3) volume et passe-bas, en douceur
	var vol_goal: float = VOL.get(mood, -9.0)
	_vol += (vol_goal - _vol) * (1.0 - exp(-dt / 0.35))
	music.volume_db = _vol
	if _lowpass:
		var c_goal := CUTOFF_PAUSE if mood == Mood.PAUSE else CUTOFF_OPEN
		_cutoff = exp(lerpf(log(_cutoff), log(c_goal), 1.0 - exp(-dt / 0.25)))
		_lowpass.cutoff_hz = _cutoff
		AudioServer.set_bus_effect_enabled(_bus, 1, _cutoff < CUTOFF_OPEN * 0.9)
