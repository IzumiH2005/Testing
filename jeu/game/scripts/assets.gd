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

## Palette du jeu (palette v2 : studio/palette_v2.txt).
const P := {
	"k": Color("0e0a1a"), "b": Color("17122a"), "d": Color("23203d"), "n": Color("2f2c5c"),
	"s": Color("39427b"), "m": Color("46639f"), "l": Color("719dca"), "p": Color("abd1eb"),
	"w": Color("e6f6ff"), "W": Color("ffffff"), "h": Color("503d7a"), "H": Color("8a83c7"),
	"i": Color("c7ccf0"), "I": Color("f2f6ff"), "r": Color("751a38"), "R": Color("cc353f"),
	"o": Color("ff7247"), "a": Color("ffba6b"), "A": Color("fff0c7"), "x": Color("660e4c"),
	"X": Color("b81661"), "z": Color("ff3874"), "Z": Color("ffb2c4"), "g": Color("fa9e14"),
	"G": Color("ffd738"), "y": Color("fff9a8"), "q": Color("114161"), "t": Color("1787a3"),
	"c": Color("3fe0e0"), "e": Color("b8ffee"), "u": Color("2c1752"), "U": Color("6a3499"),
	"j": Color("bd69db"), "J": Color("f9c7ff"), "v": Color("174e52"), "V": Color("328a78"),
	"f": Color("53bd8b"), "F": Color("9bebad")
}
