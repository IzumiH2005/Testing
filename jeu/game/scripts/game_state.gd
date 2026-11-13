extends Node
## État global : sauvegarde, réglages, langue, monnaie, skins, série quotidienne.

const SAVE_PATH := "user://save.json"

# Skins : remplacent les couleurs de l'écharpe (r, R, o). Prix en éclats.
const SKINS := [
	{"id": "corail", "name_fr": "CORAIL", "name_en": "CORAL", "price": 0, "c": ["751a38", "cc353f", "ff7247"]},
	{"id": "jade", "name_fr": "JADE", "name_en": "JADE", "price": 60, "c": ["1f4a3a", "2e8a5e", "5fd08a"]},
	{"id": "azur", "name_fr": "AZUR", "name_en": "AZURE", "price": 90, "c": ["1a2a6a", "2f5fd0", "6fa8ff"]},
	{"id": "soleil", "name_fr": "SOLEIL", "name_en": "SUN", "price": 140, "c": ["8a4a00", "e0a200", "ffd23f"]},
	{"id": "lilas", "name_fr": "LILAS", "name_en": "LILAC", "price": 200, "c": ["4a2a7a", "8a5ad0", "c49aff"]},
	{"id": "neige", "name_fr": "NEIGE", "name_en": "SNOW", "price": 280, "c": ["3f4580", "9fb0e0", "dfe6ff"]},
	{"id": "braise", "name_fr": "BRAISE", "name_en": "EMBER", "price": 380, "c": ["5c0f2e", "b0174a", "ff3d6e"]},
	{"id": "echo", "name_fr": "ÉCHO", "name_en": "ECHO", "price": 500, "c": ["0e4a5c", "1a8a9e", "3fd0d4"]},
]

var data := {
	"shards": 0,
	"best_free": 0,
	"daily": {},            # "AAAA-MM-JJ" -> meilleure hauteur
	"streak": 0,
	"last_daily": "",       # dernier jour joué en mode quotidien
	"daily_bonus_day": "",  # dernier jour où le bonus quotidien a été donné
	"skins": ["corail"],
	"skin": "corail",
	"lang": "",
	"sound": true,
	"music": true,
	"vibration": true,
	"tuto_done": false,
	"tuto_turn_done": false,
	"runs": 0,
	"total_m": 0,
}

var lang := "fr"

func _ready() -> void:
	load_data()
	if data.lang == "":
		var l := OS.get_locale_language()
		data.lang = "fr" if l == "fr" else "en"
	lang = data.lang
	get_tree().set_auto_accept_quit(true)
	get_tree().set_quit_on_go_back(false)

# ---------------------------------------------------------------- sauvegarde

func load_data() -> void:
	if not FileAccess.file_exists(SAVE_PATH):
		return
	var f := FileAccess.open(SAVE_PATH, FileAccess.READ)
	if f == null:
		return
	var parsed = JSON.parse_string(f.get_as_text())
	if typeof(parsed) == TYPE_DICTIONARY:
		for k in parsed.keys():
			data[k] = parsed[k]

func save() -> void:
	var f := FileAccess.open(SAVE_PATH, FileAccess.WRITE)
	if f:
		f.store_string(JSON.stringify(data))

# ---------------------------------------------------------------- jour / graine

func today() -> String:
	var d := Time.get_date_dict_from_system()
	return "%04d-%02d-%02d" % [d.year, d.month, d.day]

func today_short() -> String:
	var d := Time.get_date_dict_from_system()
	return "%02d/%02d" % [d.day, d.month]

func daily_seed() -> int:
	var d := Time.get_date_dict_from_system()
	return int(d.year) * 10000 + int(d.month) * 100 + int(d.day)

func daily_best() -> int:
	return int(data.daily.get(today(), 0))

func yesterday() -> String:
	var t := Time.get_unix_time_from_system() - 86400.0
	var d := Time.get_date_dict_from_unix_time(int(t))
	return "%04d-%02d-%02d" % [d.year, d.month, d.day]

## Appelé au début d'une ascension quotidienne. Renvoie le bonus d'éclats du jour (0 si déjà donné).
func start_daily() -> int:
	var t := today()
	if data.last_daily != t:
		if data.last_daily == yesterday():
			data.streak = int(data.streak) + 1
		else:
			data.streak = 1
		data.last_daily = t
	var bonus := 0
	if data.daily_bonus_day != t:
		data.daily_bonus_day = t
		bonus = 5 + 5 * mini(int(data.streak), 6)
		data.shards = int(data.shards) + bonus
	save()
	return bonus

func streak_alive() -> int:
	# série affichée : 0 si le joueur a raté hier et pas encore joué aujourd'hui
	if data.last_daily == today() or data.last_daily == yesterday():
		return int(data.streak)
	return 0

## Enregistre un résultat. Renvoie true si record.
func submit(daily: bool, height: int) -> bool:
	data.runs = int(data.runs) + 1
	data.total_m = int(data.total_m) + height
	var rec := false
	if daily:
		var t := today()
		if height > int(data.daily.get(t, 0)):
			data.daily[t] = height
			rec = true
	else:
		if height > int(data.best_free):
			data.best_free = height
			rec = true
	save()
	return rec

func add_shards(n: int) -> void:
	data.shards = int(data.shards) + n
	save()

# ---------------------------------------------------------------- skins

func skin_def(id: String) -> Dictionary:
	for s in SKINS:
		if s.id == id:
			return s
	return SKINS[0]

func current_skin() -> Dictionary:
	return skin_def(data.skin)

func owns(id: String) -> bool:
	return id in data.skins

func buy(id: String) -> bool:
	var s := skin_def(id)
	if owns(id):
		data.skin = id
		save()
		return true
	if int(data.shards) >= int(s.price):
		data.shards = int(data.shards) - int(s.price)
		data.skins.append(id)
		data.skin = id
		save()
		return true
	return false

# ---------------------------------------------------------------- réglages

func set_lang(l: String) -> void:
	lang = l
	data.lang = l
	save()

func vibrate(ms: int) -> void:
	if data.vibration:
		Input.vibrate_handheld(ms)

# ---------------------------------------------------------------- textes

const T := {
	"daily": ["TOUR DU JOUR", "DAILY TOWER"],
	"free": ["ASCENSION LIBRE", "FREE CLIMB"],
	"best": ["RECORD", "BEST"],
	"today_best": ["MEILLEUR DU JOUR", "TODAY'S BEST"],
	"tap_jump": ["TAPE POUR SAUTER", "TAP TO JUMP"],
	"tap_turn": ["EN L'AIR : TAPE POUR\nFAIRE DEMI-TOUR", "IN THE AIR: TAP TO\nTURN BACK"],
	"tap_start": ["TAPE POUR GRIMPER", "TAP TO CLIMB"],
	"life_lost": ["VIE PERDUE", "LIFE LOST"],
	"engraved": ["TON ÉCHO A GRAVÉ\nCE PIÈGE", "YOUR ECHO ENGRAVED\nTHIS TRAP"],
	"tide_got": ["LE SILENCE\nT'A RATTRAPÉ", "THE SILENCE\nCAUGHT YOU"],
	"lives_left": ["VIES RESTANTES", "LIVES LEFT"],
	"continue": ["CONTINUER", "CONTINUE"],
	"extra_life": ["+1 VIE", "+1 LIFE"],
	"no_thanks": ["NON MERCI", "NO THANKS"],
	"summary": ["ASCENSION TERMINÉE", "CLIMB OVER"],
	"height": ["HAUTEUR", "HEIGHT"],
	"shards": ["ÉCLATS", "SHARDS"],
	"new_record": ["NOUVEAU RECORD !", "NEW RECORD!"],
	"double": ["×2 ÉCLATS", "×2 SHARDS"],
	"again": ["REJOUER", "PLAY AGAIN"],
	"share": ["PARTAGER", "SHARE"],
	"menu": ["MENU", "MENU"],
	"copied": ["COPIÉ ! COLLE-LE\nOÙ TU VEUX", "COPIED! PASTE IT\nANYWHERE"],
	"skins": ["ÉCHARPES", "SCARVES"],
	"settings": ["RÉGLAGES", "SETTINGS"],
	"sound": ["SONS", "SOUND"],
	"music": ["MUSIQUE", "MUSIC"],
	"vibration": ["VIBRATIONS", "VIBRATION"],
	"language": ["LANGUE", "LANGUAGE"],
	"on": ["OUI", "ON"],
	"off": ["NON", "OFF"],
	"back": ["RETOUR", "BACK"],
	"equip": ["PORTER", "WEAR"],
	"worn": ["PORTÉE", "WORN"],
	"buy": ["ACHETER", "BUY"],
	"paused": ["PAUSE", "PAUSED"],
	"resume": ["REPRENDRE", "RESUME"],
	"quit": ["ABANDONNER", "GIVE UP"],
	"streak": ["SÉRIE", "STREAK"],
	"days": ["JOURS", "DAYS"],
	"day_bonus": ["BONUS DU JOUR", "DAILY BONUS"],
	"ad_title": ["PUBLICITÉ", "ADVERTISEMENT"],
	"ad_mock": ["(SIMULATION : LA VRAIE\nPUB ADMOB VIENDRA ICI)", "(MOCK: THE REAL ADMOB\nAD WILL PLAY HERE)"],
	"ad_reward": ["RÉCOMPENSE DANS", "REWARD IN"],
	"records": ["RECORDS", "RECORDS"],
	"best_free": ["RECORD LIBRE", "FREE BEST"],
	"runs": ["ASCENSIONS", "CLIMBS"],
	"total": ["MÈTRES GRIMPÉS", "METERS CLIMBED"],
	"life": ["VIE", "LIFE"],
	"echo_tip": ["TES ÉCHOS SE SOUVIENNENT\nDES PIÈGES QUI T'ONT TUÉ", "YOUR ECHOES REMEMBER\nTHE TRAPS THAT KILLED YOU"],
	"not_enough": ["PAS ASSEZ D'ÉCLATS", "NOT ENOUGH SHARDS"],
	"share_tower": ["TOUR DU", "TOWER OF"],
	"share_free": ["ASCENSION LIBRE", "FREE CLIMB"],
	"ascension": ["ASCENSION", "CLIMB"],
	"tagline": ["LA TOUR SE SOUVIENT", "THE TOWER REMEMBERS"],
	"tap_continue": ["TAPE POUR CONTINUER", "TAP TO CONTINUE"],
	"out_of_lives": ["PLUS DE VIES", "OUT OF LIVES"],
	"extra_q": ["UNE VIDÉO POUR\nUNE 5E VIE ?", "WATCH A VIDEO\nFOR A 5TH LIFE?"],
	"last_days": ["7 DERNIERS JOURS", "LAST 7 DAYS"],
	"doubled": ["DOUBLÉ !", "DOUBLED!"],
}

func t(key: String) -> String:
	if not T.has(key):
		return key.to_upper()
	return T[key][0 if lang == "fr" else 1]
