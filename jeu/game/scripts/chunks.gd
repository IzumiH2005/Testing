class_name ChunkLib
extends RefCounted
## Charge et analyse les chunks d'auteur (`res://chunks/<biome>/*.txt`).
## Format : studio/CHUNK_FORMAT.md. Chaque chunk devient un dictionnaire :
## {id, biome, tension, D, entree, sortie, verbe, intro, alt_min, alt_max, poids, h,
##  rows: PackedStringArray (haut -> bas, 12 car.), params: Array[Dictionary] (par rangée)}

const W := 12
const VALID := "#.><CS-|LHMf~Pg:mboO*RA?"

static var _all: Array = []
static var _by_id := {}
static var errors: PackedStringArray = []

static func all() -> Array:
	if _all.is_empty():
		load_all()
	return _all

static func by_id(id: String) -> Dictionary:
	all()
	return _by_id.get(id, {})

static func load_all(root := "res://chunks") -> void:
	_all.clear()
	_by_id.clear()
	errors.clear()
	var d := DirAccess.open(root)
	if d == null:
		errors.append("dossier introuvable : " + root)
		return
	var biomes := d.get_directories()
	biomes.sort()
	for b in biomes:
		var sub := DirAccess.open(root + "/" + b)
		if sub == null:
			continue
		var files := sub.get_files()
		files.sort()
		for f in files:
			# à l'export, les .txt restent des .txt (include_filter) ; on ignore le reste
			if not f.ends_with(".txt"):
				continue
			var path := "%s/%s/%s" % [root, b, f]
			var c := parse(FileAccess.get_file_as_string(path), path)
			if not c.is_empty():
				_all.append(c)
				_by_id[c.id] = c

## Analyse le texte d'un chunk. Renvoie {} si le chunk est invalide (l'erreur est dans `errors`).
static func parse(text: String, src := "?") -> Dictionary:
	var c := {"id": src.get_file().get_basename(), "biome": "B1", "tension": "M", "D": 1,
		"entree": "any", "sortie": "any", "verbe": "bond", "intro": "", "alt_min": 0,
		"alt_max": 99999, "poids": 1.0, "rows": PackedStringArray(), "params": [], "src": src}
	var lines := text.replace("\r", "").split("\n")
	var mode := 0  # 0 en-tête, 1 grille, 2 fin
	var kv := RegEx.create_from_string("([A-Za-z_]+)\\s*:\\s*([^\\s]+)")
	for raw in lines:
		var line: String = raw
		if mode == 0:
			if line.strip_edges().begins_with("---"):
				mode = 1
				continue
			var cut := line.find("//")
			if cut >= 0:
				line = line.substr(0, cut)
			cut = line.find(" #")
			if cut >= 0:
				line = line.substr(0, cut)
			if line.strip_edges().begins_with("#"):
				continue
			for m in kv.search_all(line):
				_set_key(c, m.get_string(1).to_lower(), m.get_string(2))
		elif mode == 1:
			if line.strip_edges().begins_with("---"):
				mode = 2
				continue
			var cut2 := line.find("//")
			if cut2 >= 0:
				line = line.substr(0, cut2)
			var params := {}
			var semi := line.find(";")
			if semi >= 0:
				for tok in line.substr(semi + 1).strip_edges().split(" ", false):
					var eq: int = tok.find("=")
					if eq > 0:
						params[tok.substr(0, eq).strip_edges()] = tok.substr(eq + 1).strip_edges()
				line = line.substr(0, semi)
			line = line.strip_edges()
			if line.is_empty():
				continue
			if line.length() != W:
				errors.append("%s : rangée de %d car. (attendu %d) : '%s'" % [src, line.length(), W, line])
				line = (line + "............").substr(0, W)
			for ch in line:
				if not VALID.contains(ch):
					errors.append("%s : caractère inconnu '%s'" % [src, ch])
			c.rows.append(line)
			c.params.append(params)
	if c.rows.size() < 4:
		errors.append("%s : grille absente ou trop courte" % src)
		return {}
	c["h"] = c.rows.size()
	return c

static func _set_key(c: Dictionary, k: String, v: String) -> void:
	match k:
		"id": c.id = v
		"biome": c.biome = v.to_upper()
		"tension": c.tension = v.to_upper()
		"d": c.D = int(v)
		"entree", "entrée": c.entree = v.to_upper() if v.length() == 1 else v.to_lower()
		"sortie": c.sortie = v.to_upper() if v.length() == 1 else v.to_lower()
		"verbe": c.verbe = v.to_lower()
		"intro": c.intro = v.to_upper()
		"poids": c.poids = float(v)
		"alt":
			var p := v.split("-")
			c.alt_min = int(p[0])
			if p.size() > 1:
				c.alt_max = int(p[1])
		"alt_min": c.alt_min = int(v)
		"alt_max": c.alt_max = int(v)

## Grille et paramètres éventuellement retournés en miroir (gauche <-> droite).
static func mirrored_rows(c: Dictionary) -> PackedStringArray:
	var out := PackedStringArray()
	for r in c.rows:
		var s := ""
		for i in range(W - 1, -1, -1):
			var ch: String = r[i]
			if ch == ">":
				ch = "<"
			elif ch == "<":
				ch = ">"
			s += ch
		out.append(s)
	return out

static func flip_side(s: String) -> String:
	if s == "L":
		return "R"
	if s == "R":
		return "L"
	return s

static func pf(params: Dictionary, k: String, def: float) -> float:
	return float(params[k]) if params.has(k) else def
