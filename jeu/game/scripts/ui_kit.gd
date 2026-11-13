class_name UIK
extends RefCounted
## Fabrique d'éléments d'interface pixel (police bitmap, cadres et boutons 9-slice, icônes).

enum Ico { LIFE, LIFE_USED, SHARD, PLAY, SHARE, VIDEO, GEAR, SOUND_ON, SOUND_OFF, BACK, TROPHY,
	CALENDAR, LOCK, CHECK, PAUSE, FLAME, VIBRATION, HOME, SKULL, CROWN, SCARF }

static var _theme: Theme

static func theme() -> Theme:
	if _theme:
		return _theme
	var th := Theme.new()
	var f := A.font()
	if f is FontFile:
		f.fixed_size = 10
		f.fixed_size_scale_mode = TextServer.FIXED_SIZE_SCALE_INTEGER_ONLY
	th.default_font = f
	th.default_font_size = A.font_size()
	th.set_color("font_color", "Label", A.P.w)
	th.set_constant("line_spacing", "Label", 1)
	_theme = th
	return th

static func sb_tex(name: String, frame: int, frame_w: int, margin: int, fallback: Color, border: Color, content := Vector4(6, 4, 6, 4)) -> StyleBox:
	var tx := A.tex(name)
	if tx:
		var s := StyleBoxTexture.new()
		s.texture = tx
		s.region_rect = Rect2(frame * frame_w, 0, frame_w, tx.get_height())
		s.texture_margin_left = margin
		s.texture_margin_right = margin
		s.texture_margin_top = margin
		s.texture_margin_bottom = margin
		s.content_margin_left = content.x
		s.content_margin_top = content.y
		s.content_margin_right = content.z
		s.content_margin_bottom = content.w
		s.axis_stretch_horizontal = StyleBoxTexture.AXIS_STRETCH_MODE_STRETCH
		s.axis_stretch_vertical = StyleBoxTexture.AXIS_STRETCH_MODE_STRETCH
		return s
	var fl := StyleBoxFlat.new()
	fl.bg_color = fallback
	fl.border_color = border
	fl.set_border_width_all(1)
	fl.content_margin_left = content.x
	fl.content_margin_top = content.y
	fl.content_margin_right = content.z
	fl.content_margin_bottom = content.w
	return fl

static func icon(i: int) -> Texture2D:
	var tx := A.tex("ui/icons")
	if tx == null:
		var im := Image.create(12, 12, false, Image.FORMAT_RGBA8)
		im.fill(A.P.p)
		return ImageTexture.create_from_image(im)
	var at := AtlasTexture.new()
	at.atlas = tx
	at.region = Rect2(i * 12, 0, 12, 12)
	return at

static func icon_rect(i: int, scale := 1) -> TextureRect:
	var r := TextureRect.new()
	r.texture = icon(i)
	r.custom_minimum_size = Vector2(12, 12) * scale
	r.stretch_mode = TextureRect.STRETCH_SCALE
	r.mouse_filter = Control.MOUSE_FILTER_IGNORE
	return r

static func label(text: String, color: Color = A.P.w, size := 1, align := HORIZONTAL_ALIGNMENT_CENTER) -> Label:
	var l := Label.new()
	l.text = text
	l.horizontal_alignment = align
	l.add_theme_color_override("font_color", color)
	l.add_theme_font_size_override("font_size", A.font_size() * size)
	l.mouse_filter = Control.MOUSE_FILTER_IGNORE
	return l

## kind : "main" (ambre), "alt" (pierre), "echo" (cyan, vidéo récompensée)
static func button(text: String, kind := "main", ico := -1, min_w := 120) -> Button:
	var b := Button.new()
	b.text = text
	b.focus_mode = Control.FOCUS_NONE
	b.custom_minimum_size = Vector2(min_w, 24)
	var name := "ui/btn_" + kind
	var fb := {"main": [A.P.o, A.P.k, A.P.k], "alt": [A.P.s, A.P.k, A.P.w], "echo": [A.P.t, A.P.k, A.P.k]}
	var cols: Array = fb.get(kind, fb.main)
	var normal := sb_tex(name, 0, 48, 8, cols[0], cols[1], Vector4(9, 6, 9, 8))
	var pressed := sb_tex(name, 1, 48, 8, cols[0].darkened(0.2), cols[1], Vector4(9, 8, 9, 6))
	var disabled := sb_tex(name, 2, 48, 8, A.P.n, cols[1], Vector4(9, 8, 9, 6))
	b.add_theme_stylebox_override("normal", normal)
	b.add_theme_stylebox_override("hover", normal)
	b.add_theme_stylebox_override("pressed", pressed)
	b.add_theme_stylebox_override("hover_pressed", pressed)
	b.add_theme_stylebox_override("disabled", disabled)
	b.add_theme_stylebox_override("focus", StyleBoxEmpty.new())
	var fc: Color = cols[2]
	if kind == "main":
		fc = A.P.k
	elif kind == "echo":
		fc = A.P.k
	b.add_theme_color_override("font_color", fc)
	b.add_theme_color_override("font_hover_color", fc)
	b.add_theme_color_override("font_pressed_color", fc)
	b.add_theme_color_override("font_hover_pressed_color", fc)
	b.add_theme_color_override("font_disabled_color", A.P.m)
	b.add_theme_constant_override("h_separation", 4)
	if ico >= 0:
		b.icon = icon(ico)
	b.pressed.connect(func(): Sfx.play("click"))
	return b

static func icon_button(ico: int, kind := "alt") -> Button:
	var b := button("", kind, ico, 24)
	b.custom_minimum_size = Vector2(24, 24)
	b.add_theme_constant_override("icon_max_width", 12)
	b.icon_alignment = HORIZONTAL_ALIGNMENT_CENTER
	return b

## kind : "pierre" (neutre), "echo" (cyan), "danger" (magenta), "record" (or)
const FRAME_KINDS := ["pierre", "echo", "danger", "record"]

static func panel(kind := "pierre") -> PanelContainer:
	var p := PanelContainer.new()
	var fi := maxi(0, FRAME_KINDS.find(kind))
	var sb := sb_tex("ui/frame", fi, 32, 13, A.P.d, A.P.m, Vector4(13, 12, 13, 12))
	p.add_theme_stylebox_override("panel", sb)
	p.mouse_filter = Control.MOUSE_FILTER_STOP
	return p

static func font_n(name: String) -> Font:
	var path := "res://assets/ui/%s.fnt" % name
	if ResourceLoader.exists(path):
		return load(path)
	return A.font()

## Bandeau-titre en ruban. kind : 0 acier · 1 or · 2 danger · 3 écho
static func title_plate(text: String, kind := 0, ico := -1) -> PanelContainer:
	var p := PanelContainer.new()
	var tx := A.tex("ui/title_plate")
	var sb := StyleBoxTexture.new()
	sb.texture = tx
	sb.region_rect = Rect2(kind * 48, 0, 48, 22)
	sb.texture_margin_left = 14
	sb.texture_margin_right = 14
	sb.content_margin_left = 16
	sb.content_margin_right = 16
	sb.content_margin_top = 4
	sb.content_margin_bottom = 8
	p.add_theme_stylebox_override("panel", sb)
	p.custom_minimum_size = Vector2(0, 22)
	p.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var h := hbox(4)
	if ico >= 0:
		h.add_child(icon_rect(ico))
	var col: Color = [A.P.W, A.P.k, A.P.W, A.P.k][kind]
	var l := label(text, col)
	h.add_child(l)
	p.add_child(h)
	return p

static func _atlas(name: String, r: Rect2) -> AtlasTexture:
	var at := AtlasTexture.new()
	at.atlas = A.tex(name)
	at.region = r
	return at

static func _nine(name: String, r: Rect2, ml: int, mt: int, mr: int, mb: int) -> NinePatchRect:
	var n := NinePatchRect.new()
	n.texture = A.tex(name)
	n.region_rect = r
	n.patch_margin_left = ml
	n.patch_margin_top = mt
	n.patch_margin_right = mr
	n.patch_margin_bottom = mb
	n.mouse_filter = Control.MOUSE_FILTER_IGNORE
	return n

## Séparateur orné : volute, filet, gemme centrale, filet, volute.
static func divider(width := 120) -> Control:
	var h := HBoxContainer.new()
	h.add_theme_constant_override("separation", 0)
	h.mouse_filter = Control.MOUSE_FILTER_IGNORE
	h.custom_minimum_size = Vector2(width, 9)
	h.size_flags_horizontal = Control.SIZE_SHRINK_CENTER
	var l := _nine("ui/divider", Rect2(0, 0, 24, 9), 10, 0, 0, 0)
	l.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	h.add_child(l)
	var g := TextureRect.new()
	g.texture = _atlas("ui/divider", Rect2(31, 0, 9, 9))
	g.mouse_filter = Control.MOUSE_FILTER_IGNORE
	h.add_child(g)
	var r := _nine("ui/divider", Rect2(48, 0, 24, 9), 0, 0, 10, 0)
	r.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	h.add_child(r)
	return h

## Jauge segmentée. fill : 1 or · 2 écho · 3 danger · 4 marée · 5 acier. Se remplit en `dur` s après `delay`.
static func gauge(w: int, ratio: float, fill := 2, delay := 0.0, dur := 0.5) -> Control:
	var c := Control.new()
	c.custom_minimum_size = Vector2(w, 10)
	c.mouse_filter = Control.MOUSE_FILTER_IGNORE
	c.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	var fr := _nine("ui/gauge", Rect2(0, 0, 8, 10), 3, 3, 3, 3)
	fr.size = Vector2(w, 10)
	c.add_child(fr)
	var fw := maxi(2, int(round((w - 4) * clampf(ratio, 0.0, 1.0))))
	var f := _nine("ui/gauge", Rect2(fill * 8, 0, 8, 6), 0, 0, 1, 0)
	f.position = Vector2(2, 2)
	f.size = Vector2(fw, 6)
	c.add_child(f)
	var t := TextureRect.new()
	t.texture = _atlas("ui/gauge", Rect2(48, 0, 8, 6))
	t.stretch_mode = TextureRect.STRETCH_TILE
	t.position = Vector2(2, 2)
	t.size = Vector2(fw - 2, 6)
	t.mouse_filter = Control.MOUSE_FILTER_IGNORE
	f.clip_contents = true
	c.add_child(t)
	if dur > 0.0:
		f.size.x = 0.0
		t.size.x = 0.0
		f.visible = false
		var tw := c.create_tween()
		tw.tween_interval(delay)
		tw.tween_callback(func(): f.visible = true)
		tw.tween_method(func(v: float):
			f.size.x = round(v)
			t.size.x = maxf(0.0, round(v) - 2.0), 1.0, float(fw), dur).set_trans(Tween.TRANS_CUBIC).set_ease(Tween.EASE_OUT)
	return c

## Médaillon numéroté. kind : 0 acier · 1 or · 2 écho
static func medal(n: int, kind := 0) -> Control:
	var c := Control.new()
	c.custom_minimum_size = Vector2(16, 16)
	c.mouse_filter = Control.MOUSE_FILTER_IGNORE
	c.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	var r := TextureRect.new()
	r.texture = _atlas("ui/medal", Rect2(kind * 16, 0, 16, 16))
	r.mouse_filter = Control.MOUSE_FILTER_IGNORE
	c.add_child(r)
	var l := label(str(n), [A.P.p, A.P.G, A.P.c][kind])
	l.add_theme_font_override("font", font_n("font_5"))
	l.add_theme_font_size_override("font_size", 8)
	l.position = Vector2(0, 4)
	l.size = Vector2(16, 8)
	c.add_child(l)
	return c

## Case de valeur (creux). kind : 0 acier · 1 or · 2 cyan
static func slot(content: Control, kind := 0) -> PanelContainer:
	var p := PanelContainer.new()
	var sb := sb_tex("ui/slot", kind, 16, 4, A.P.b, A.P.k, Vector4(5, 3, 5, 2))
	p.add_theme_stylebox_override("panel", sb)
	p.mouse_filter = Control.MOUSE_FILTER_IGNORE
	p.add_child(content)
	return p

## Plaque sombre du HUD / des toasts. kind : 0 acier · 1 or
static func plate(kind := 0) -> PanelContainer:
	var p := PanelContainer.new()
	var sb := sb_tex("ui/hud_plate", kind, 24, 7, A.P.b, A.P.k, Vector4(6, 4, 6, 4))
	p.add_theme_stylebox_override("panel", sb)
	p.mouse_filter = Control.MOUSE_FILTER_IGNORE
	return p

static func laurel(right := false) -> TextureRect:
	var r := TextureRect.new()
	r.texture = _atlas("ui/laurel", Rect2(16 if right else 0, 0, 16, 24))
	r.mouse_filter = Control.MOUSE_FILTER_IGNORE
	r.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	return r

static func vbox(sep := 4) -> VBoxContainer:
	var v := VBoxContainer.new()
	v.add_theme_constant_override("separation", sep)
	v.alignment = BoxContainer.ALIGNMENT_CENTER
	v.mouse_filter = Control.MOUSE_FILTER_IGNORE
	return v

static func hbox(sep := 4) -> HBoxContainer:
	var h := HBoxContainer.new()
	h.add_theme_constant_override("separation", sep)
	h.alignment = BoxContainer.ALIGNMENT_CENTER
	h.mouse_filter = Control.MOUSE_FILTER_IGNORE
	return h

static func spacer(h: int) -> Control:
	var c := Control.new()
	c.custom_minimum_size = Vector2(0, h)
	c.mouse_filter = Control.MOUSE_FILTER_IGNORE
	return c

static func full(c: Control) -> Control:
	c.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	return c
