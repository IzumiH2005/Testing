class_name A
extends RefCounted
## Chargement tolérant des images : renvoie null si l'image n'existe pas encore
## (le jeu dessine alors une forme de remplacement).

static var _cache := {}

static func tex(name: String) -> Texture2D:
	if _cache.has(name):
		return _cache[name]
	var path := "res://assets/%s.png" % name
	var t: Texture2D = null
	if ResourceLoader.exists(path):
		t = load(path)
	_cache[name] = t
	return t

static func font() -> Font:
	if _cache.has("__font"):
		return _cache["__font"]
	var f: Font = null
	if ResourceLoader.exists("res://assets/ui/font.fnt"):
		f = load("res://assets/ui/font.fnt")
	if f == null:
		f = ThemeDB.fallback_font
	_cache["__font"] = f
	return f

static func font_size() -> int:
	return 10 if ResourceLoader.exists("res://assets/ui/font.fnt") else 8

## Palette du jeu (mêmes valeurs que tools/palette.txt).
const P := {
	"k": Color("0b0b1a"), "b": Color("161631"), "d": Color("222246"), "n": Color("2f3060"),
	"s": Color("3f4580"), "m": Color("5763a3"), "l": Color("7385c4"), "p": Color("9fb0e0"),
	"w": Color("dfe6ff"), "W": Color("ffffff"),
	"q": Color("0e4a5c"), "t": Color("1a8a9e"), "c": Color("3fd0d4"), "e": Color("a8fff0"),
	"r": Color("7a1f3d"), "R": Color("c4384f"), "o": Color("ff7a59"), "a": Color("ffc46b"),
	"x": Color("5c0f2e"), "X": Color("b0174a"), "z": Color("ff3d6e"), "Z": Color("ffb3c6"),
	"g": Color("e0a200"), "G": Color("ffd23f"), "y": Color("fff3a8"),
	"v": Color("2e6b5a"), "V": Color("4fa37a"), "u": Color("4a2a7a"), "U": Color("8a5ad0"),
}
