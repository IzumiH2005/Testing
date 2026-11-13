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
	var normal := sb_tex(name, 0, 48, 8, cols[0], cols[1], Vector4(8, 5, 8, 7))
	var pressed := sb_tex(name, 1, 48, 8, cols[0].darkened(0.2), cols[1], Vector4(8, 7, 8, 5))
	var disabled := sb_tex(name, 2, 48, 8, A.P.n, cols[1], Vector4(8, 7, 8, 5))
	for sb in [normal, pressed, disabled]:
		if sb is StyleBoxTexture:
			(sb as StyleBoxTexture).texture_margin_top = 6
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

static func panel(echo := false) -> PanelContainer:
	var p := PanelContainer.new()
	var sb := sb_tex("ui/panel_echo" if echo else "ui/panel", 0, 24, 8,
		A.P.d, A.P.c if echo else A.P.m, Vector4(10, 9, 10, 10))
	p.add_theme_stylebox_override("panel", sb)
	p.mouse_filter = Control.MOUSE_FILTER_STOP
	return p

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
