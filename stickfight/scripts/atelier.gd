extends Control
## Atelier de poses : on attrape les articulations à la souris, on règle
## chaque angle au centième de degré, on enregistre la pose en JSON dans
## res://poses/. L'interface est construite ici, en code.

const SceneScript := preload("res://scripts/atelier_scene.gd")
const POSES_DIR := "res://poses"
const GROUPS := [
	["Tronc", ["root", "spineLow", "chest", "neck"]],
	["Bras proche", ["armN", "foreN"]],
	["Bras loin", ["armF", "foreF"]],
	["Jambe proche", ["thighN", "shinN", "footN"]],
	["Jambe loin", ["thighF", "shinF", "footF"]],
]
const UNDO_MERGE_MS := 700

var pose: Dictionary = StickRig.plant(StickRig.neutral_pose())
var ghost := {}
var color := Color("#111111")
var shade_far := false
var show_grid := true
var show_debug := false
var pin_feet := true
var limits := true
var sel := {"kind": "angle", "id": "armN"}

var undo_stack: Array = []
var redo_stack: Array = []
var _last_key := ""
var _last_ms := 0
var _edit_base := {}  # pose au début du geste en cours (pour « pieds fixés »)

var stage: Control
var rows := {}  # id -> {row, slider, spin, name}
var preset_btn: OptionButton
var style_btn: OptionButton
var name_edit: LineEdit
var json_edit: TextEdit
var readout: Label
var warn: Label
var status: Label
var btn_undo: Button
var btn_redo: Button
var btn_ghost_clear: Button
var _preset_paths: Array = []


func _ready() -> void:
	set_anchors_preset(Control.PRESET_FULL_RECT)
	_build_ui()
	_reload_presets()
	var start := POSES_DIR.path_join("garde.json")
	if FileAccess.file_exists(start):
		pose = StickRig.load_pose(start)
	_sync_all()


# ---------- Construction de l'interface ----------

func _build_ui() -> void:
	var bg := ColorRect.new()
	bg.color = Color("#1d1b1a")
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(bg)

	var root := HBoxContainer.new()
	root.set_anchors_preset(Control.PRESET_FULL_RECT)
	root.add_theme_constant_override("separation", 0)
	add_child(root)

	var left := VBoxContainer.new()
	left.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	left.add_theme_constant_override("separation", 4)
	root.add_child(left)

	stage = Control.new()
	stage.set_script(SceneScript)
	stage.atelier = self
	stage.size_flags_vertical = Control.SIZE_EXPAND_FILL
	stage.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	left.add_child(stage)

	var info := VBoxContainer.new()
	var m := MarginContainer.new()
	for side in ["left", "right", "bottom"]:
		m.add_theme_constant_override("margin_" + side, 10)
	m.add_child(info)
	left.add_child(m)
	readout = Label.new()
	readout.add_theme_font_size_override("font_size", 13)
	info.add_child(readout)
	warn = Label.new()
	warn.add_theme_color_override("font_color", Color("#ffd27a"))
	warn.autowrap_mode = TextServer.AUTOWRAP_WORD
	info.add_child(warn)
	var keys := Label.new()
	keys.text = "Ronds : rotation · carrés : main, cheville (IK), bassin (position) · Ctrl + taille : bassin · ←→ tourne (↑↓ aussi pour IK) · Maj ×5 · Alt ×0,1 · [ ] articulation suivante · Ctrl+Z / Ctrl+Y"
	keys.add_theme_font_size_override("font_size", 12)
	keys.add_theme_color_override("font_color", Color("#a8a29e"))
	keys.autowrap_mode = TextServer.AUTOWRAP_WORD
	info.add_child(keys)

	var scroll := ScrollContainer.new()
	scroll.custom_minimum_size = Vector2(400, 0)
	scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	root.add_child(scroll)
	var pm := MarginContainer.new()
	pm.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	for side in ["left", "right", "top", "bottom"]:
		pm.add_theme_constant_override("margin_" + side, 12)
	scroll.add_child(pm)
	var panel := VBoxContainer.new()
	panel.add_theme_constant_override("separation", 8)
	pm.add_child(panel)

	var title := Label.new()
	title.text = "STICKFIGHT · ATELIER"
	title.add_theme_font_size_override("font_size", 20)
	title.add_theme_color_override("font_color", Color("#f06464"))
	panel.add_child(title)

	# Pose de départ, gabarit, couleur.
	var r1 := HBoxContainer.new()
	panel.add_child(r1)
	preset_btn = OptionButton.new()
	preset_btn.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	preset_btn.tooltip_text = "Pose de départ (fichiers de res://poses)"
	preset_btn.item_selected.connect(_on_preset)
	r1.add_child(preset_btn)
	style_btn = OptionButton.new()
	style_btn.tooltip_text = "Gabarit (proportions)"
	for k in StickRig.STYLES:
		style_btn.add_item(k)
	style_btn.item_selected.connect(_on_style)
	r1.add_child(style_btn)
	var cp := ColorPickerButton.new()
	cp.color = color
	cp.custom_minimum_size = Vector2(40, 0)
	cp.tooltip_text = "Couleur du stickman"
	cp.color_changed.connect(_on_color)
	r1.add_child(cp)

	var r2 := HFlowContainer.new()
	panel.add_child(r2)
	btn_undo = _button(r2, "Annuler", undo)
	btn_redo = _button(r2, "Rétablir", redo)
	_button(r2, "Retourner", _on_facing)
	_button(r2, "Échanger proche / loin", _on_swap)
	_button(r2, "Poser au sol", _on_plant)
	_button(r2, "Neutre", _on_neutral)

	var r3 := HFlowContainer.new()
	panel.add_child(r3)
	_toggle(r3, "Pieds fixés", pin_feet, "pin_feet", "Les chevilles restent en place quand on bouge le bassin ou le tronc")
	_toggle(r3, "Amplitudes humaines", limits, "limits", "Bloque chaque articulation dans son amplitude réelle")
	_toggle(r3, "Grille", show_grid, "show_grid", "Carreaux de 10 cm, traits forts tous les 50 cm")
	_toggle(r3, "Os", show_debug, "show_debug", "Squelette coloré : vert tronc, orange proche, bleu loin")
	_toggle(r3, "Assombrir le loin", shade_far, "shade_far", "Membres lointains plus sombres, pour lire la profondeur")
	_button(r3, "Garder en fantôme", _on_ghost_keep)
	btn_ghost_clear = _button(r3, "Effacer le fantôme", _on_ghost_clear)
	btn_ghost_clear.disabled = true

	# Position et angles.
	panel.add_child(_heading("Position (cm)"))
	_row(panel, "x", "Bassin x", Vector2(-200, 200))
	_row(panel, "y", "Bassin y", Vector2(-50, 250))
	for g in GROUPS:
		panel.add_child(_heading(g[0] + " (degrés)"))
		for id in g[1]:
			var b := StickRig.bone(id)
			_row(panel, id, b.label, b.lim)

	# Nom, enregistrement, JSON.
	panel.add_child(_heading("Enregistrer"))
	var r4 := HBoxContainer.new()
	panel.add_child(r4)
	name_edit = LineEdit.new()
	name_edit.placeholder_text = "nom de la pose"
	name_edit.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	name_edit.text_changed.connect(func(t): pose.nom = t; _sync_json())
	r4.add_child(name_edit)
	_button(r4, "Enregistrer", _save)
	json_edit = TextEdit.new()
	json_edit.custom_minimum_size = Vector2(0, 220)
	json_edit.add_theme_font_size_override("font_size", 12)
	panel.add_child(json_edit)
	var r5 := HBoxContainer.new()
	panel.add_child(r5)
	_button(r5, "Copier", _on_copy)
	_button(r5, "Appliquer le JSON", _apply_json)
	status = Label.new()
	status.add_theme_color_override("font_color", Color("#a8a29e"))
	status.autowrap_mode = TextServer.AUTOWRAP_WORD
	panel.add_child(status)


func _heading(t: String) -> Label:
	var l := Label.new()
	l.text = t.to_upper()
	l.add_theme_font_size_override("font_size", 12)
	l.add_theme_color_override("font_color", Color("#a8a29e"))
	return l


func _button(parent: Control, text: String, cb: Callable) -> Button:
	var b := Button.new()
	b.text = text
	b.focus_mode = Control.FOCUS_NONE
	b.pressed.connect(cb)
	parent.add_child(b)
	return b


## Bouton bascule lié à une variable de l'atelier.
func _toggle(parent: Control, text: String, on: bool, prop: String, tip := "") -> Button:
	var b := Button.new()
	b.text = text
	b.toggle_mode = true
	b.button_pressed = on
	b.tooltip_text = tip
	b.focus_mode = Control.FOCUS_NONE
	b.toggled.connect(_on_toggle.bind(prop))
	parent.add_child(b)
	return b


func _on_toggle(v: bool, prop: String) -> void:
	set(prop, v)
	_sync_all()


func _on_color(c: Color) -> void:
	color = c
	stage.refresh()


func _on_facing() -> void:
	var flip := func(p: Dictionary) -> Dictionary:
		p.facing = -int(p.facing)
		return p
	_edit("facing", flip)


func _on_swap() -> void:
	_edit("swap", func(p: Dictionary) -> Dictionary: return StickRig.swap_sides(p))


func _on_plant() -> void:
	_edit("plant", func(p: Dictionary) -> Dictionary: return StickRig.plant(p))


func _on_neutral() -> void:
	var n := StickRig.plant(StickRig.neutral_pose(pose.style))
	n.nom = pose.nom
	_edit("neutral", func(_p): return n)


func _on_ghost_keep() -> void:
	ghost = StickRig.clone_pose(pose)
	btn_ghost_clear.disabled = false
	stage.refresh()


func _on_ghost_clear() -> void:
	ghost = {}
	btn_ghost_clear.disabled = true
	stage.refresh()


func _on_copy() -> void:
	DisplayServer.clipboard_set(json_edit.text)
	_status("JSON copié.")


func _row(parent: Control, id: String, label: String, lim: Vector2) -> void:
	var row := HBoxContainer.new()
	parent.add_child(row)
	var lab := Button.new()
	lab.text = label
	lab.flat = true
	lab.alignment = HORIZONTAL_ALIGNMENT_LEFT
	lab.custom_minimum_size = Vector2(150, 0)
	lab.clip_text = true
	lab.focus_mode = Control.FOCUS_NONE
	lab.tooltip_text = "%s · amplitude [%d, %d]" % [id, lim.x, lim.y]
	if id not in ["x", "y"]:
		lab.pressed.connect(_on_row_name.bind(id))
	row.add_child(lab)
	var slider := HSlider.new()
	slider.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	slider.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	slider.step = 0.01
	slider.focus_mode = Control.FOCUS_NONE
	row.add_child(slider)
	var spin := SpinBox.new()
	spin.step = 0.01
	spin.custom_minimum_size = Vector2(92, 0)
	spin.allow_greater = true
	spin.allow_lesser = true
	row.add_child(spin)
	slider.value_changed.connect(_on_value.bind(id))
	spin.value_changed.connect(_on_value.bind(id))
	rows[id] = {"row": row, "slider": slider, "spin": spin, "name": lab, "lim": lim}


func _on_row_name(id: String) -> void:
	select("angle", id)
	stage.grab_focus()


func _on_value(v: float, id: String) -> void:
	var lim: Vector2 = rows[id].lim
	var val := v
	if id not in ["x", "y"] and limits:
		val = clampf(v, lim.x, lim.y)
	var setter := func(p: Dictionary) -> Dictionary:
		if id in ["x", "y"]:
			p[id] = val
		else:
			p.angles[id] = val
		return p
	_edit("val:" + id, setter, _leg_of("angle", id))


# ---------- État, historique ----------

func _snapshot_if_needed(key: String) -> void:
	var now := Time.get_ticks_msec()
	if key != _last_key or now - _last_ms > UNDO_MERGE_MS or key == "":
		undo_stack.append(StickRig.clone_pose(pose))
		if undo_stack.size() > 300:
			undo_stack.pop_front()
		redo_stack.clear()
	_last_key = key
	_last_ms = now


## Applique une modification de pose (fn reçoit une copie et la renvoie),
## avec historique et « pieds fixés ».
func _edit(key: String, fn: Callable, keep_leg := "") -> void:
	_snapshot_if_needed(key)
	var before := StickRig.clone_pose(pose)
	var p: Dictionary = fn.call(StickRig.clone_pose(pose))
	if pin_feet and key not in ["facing", "swap", "plant", "neutral", "preset", "json"]:
		p = _pin(p, before, keep_leg)
	pose = p
	_sync_all()


## Recolle les chevilles là où elles étaient dans « ref », sauf la jambe qu'on
## est en train de modifier.
func _pin(p: Dictionary, ref: Dictionary, skip_leg: String) -> Dictionary:
	var J: Dictionary = StickRig.solve(ref).joints
	for leg in ["legN", "legF"]:
		if leg == skip_leg:
			continue
		var tip: String = StickRig.LIMBS[leg].tip
		var now: Dictionary = StickRig.solve(p).joints
		if now[tip].distance_to(J[tip]) > 0.005:
			p = StickRig.reach(p, leg, J[tip], limits)
	return p


func _leg_of(kind: String, id: String) -> String:
	if kind == "ik" and id.begins_with("leg"):
		return id
	if id.ends_with("N") and (id.begins_with("thigh") or id.begins_with("shin") or id.begins_with("foot")):
		return "legN"
	if id.ends_with("F") and (id.begins_with("thigh") or id.begins_with("shin") or id.begins_with("foot")):
		return "legF"
	return ""


func undo() -> void:
	if undo_stack.is_empty():
		return
	redo_stack.append(StickRig.clone_pose(pose))
	pose = undo_stack.pop_back()
	_last_key = ""
	_sync_all()


func redo() -> void:
	if redo_stack.is_empty():
		return
	undo_stack.append(StickRig.clone_pose(pose))
	pose = redo_stack.pop_back()
	_last_key = ""
	_sync_all()


func _shortcut_input(ev: InputEvent) -> void:
	if ev is InputEventKey and ev.pressed and ev.ctrl_pressed:
		if ev.keycode == KEY_Z and not ev.shift_pressed:
			undo()
			get_viewport().set_input_as_handled()
		elif ev.keycode == KEY_Y or (ev.keycode == KEY_Z and ev.shift_pressed):
			redo()
			get_viewport().set_input_as_handled()
		elif ev.keycode == KEY_S:
			_save()
			get_viewport().set_input_as_handled()


# ---------- Appelé par la scène ----------

func select(kind: String, id: String) -> void:
	sel = {"kind": kind, "id": id}
	_sync_selection()
	stage.refresh()
	update_readout()


func begin_edit(key: String) -> void:
	_snapshot_if_needed("")
	_last_key = key
	_edit_base = StickRig.clone_pose(pose)


func end_edit() -> void:
	_edit_base = {}
	_last_key = ""


func drag_to(h: Dictionary, w: Vector2, start_w: Vector2) -> void:
	var base: Dictionary = _edit_base if not _edit_base.is_empty() else pose
	var p := StickRig.clone_pose(pose)
	match h.kind:
		"move":
			p.x = StickRig.round2(float(base.x) + w.x - start_w.x)
			p.y = StickRig.round2(float(base.y) + w.y - start_w.y)
		"ik":
			p = StickRig.reach(p, h.id, w, limits)
		"angle":
			p = StickRig.aim(p, h.id, w, limits)
	if pin_feet:
		p = _pin(p, base, _leg_of(h.kind, h.id))
	pose = p
	_sync_all()


## Flèches : tourne l'angle sélectionné, ou déplace la main, la cheville ou le bassin.
func nudge(dir: Vector2, step: float) -> void:
	var key: String = "nudge:" + str(sel.id)
	match sel.kind:
		"angle":
			if dir.x == 0:
				return
			var id: String = sel.id
			var turn := func(p: Dictionary) -> Dictionary:
				var v := StickRig.round2(StickRig.angle(p, id) + dir.x * step)
				p.angles[id] = StickRig.clamp_angle(id, v) if limits else v
				return p
			_edit(key, turn, _leg_of("angle", id))
		"ik":
			var tip: String = StickRig.LIMBS[sel.id].tip
			var limb: String = sel.id
			var push := func(p: Dictionary) -> Dictionary:
				var t: Vector2 = StickRig.solve(p).joints[tip] + dir * step
				return StickRig.reach(p, limb, t, limits)
			_edit(key, push, _leg_of("ik", limb))
		"move":
			var move := func(p: Dictionary) -> Dictionary:
				p.x = StickRig.round2(float(p.x) + dir.x * step)
				p.y = StickRig.round2(float(p.y) + dir.y * step)
				return p
			_edit(key, move)


func cycle_selection(d: int) -> void:
	var ids := StickRig.angle_ids()
	var i := ids.find(sel.id) if sel.kind == "angle" else -1
	i = posmod(i + d, ids.size())
	select("angle", ids[i])


# ---------- Synchronisation de l'interface ----------

func _sync_all() -> void:
	for id in rows:
		var r: Dictionary = rows[id]
		var v: float = float(pose[id]) if id in ["x", "y"] else StickRig.angle(pose, id)
		var lim: Vector2 = r.lim
		r.slider.min_value = lim.x if limits or id in ["x", "y"] else -180
		r.slider.max_value = lim.y if limits or id in ["x", "y"] else 180
		r.slider.set_value_no_signal(v)
		r.spin.min_value = r.slider.min_value
		r.spin.max_value = r.slider.max_value
		r.spin.set_value_no_signal(v)
		var bad: bool = id not in ["x", "y"] and (v < lim.x or v > lim.y)
		r.name.add_theme_color_override("font_color", Color("#ffd27a") if bad else Color("#ecebea"))
	var si := StickRig.STYLES.keys().find(pose.style)
	if si >= 0:
		style_btn.select(si)
	if name_edit.text != pose.nom:
		name_edit.text = pose.nom
	btn_undo.disabled = undo_stack.is_empty()
	btn_redo.disabled = redo_stack.is_empty()
	var v := StickRig.violations(pose)
	if v.is_empty():
		warn.text = ""
	else:
		var parts := []
		for x in v:
			parts.append("%s %.2f° hors de [%d, %d]" % [x.label, x.value, x.lim.x, x.lim.y])
		warn.text = "Hors amplitude humaine : " + ", ".join(parts)
	_sync_selection()
	_sync_json()
	stage.refresh()
	update_readout()


func _sync_selection() -> void:
	for id in rows:
		var on: bool = sel.kind == "angle" and sel.id == id
		rows[id].name.add_theme_color_override("font_outline_color", Color("#ffe066"))
		rows[id].name.add_theme_constant_override("outline_size", 2 if on else 0)


func _sync_json() -> void:
	if json_edit != null and not json_edit.has_focus():
		json_edit.text = StickRig.to_json(pose)


func update_readout() -> void:
	var t := ""
	match sel.kind:
		"angle":
			t = "%s : %.2f°" % [StickRig.bone(sel.id).label, StickRig.angle(pose, sel.id)]
		"ik":
			var tip: String = StickRig.LIMBS[sel.id].tip
			var j: Vector2 = StickRig.solve(pose).joints[tip]
			t = "%s : (%.1f, %.1f) cm" % [StickRig.LIMBS[sel.id].label, j.x, j.y]
		"move":
			t = "Bassin : (%.1f, %.1f) cm" % [float(pose.x), float(pose.y)]
	var mw: Vector2 = stage.mouse_world
	t += "    souris (%.1f, %.1f)    sol : %.2f" % [mw.x, mw.y, StickRig.lowest_y(pose)]
	readout.text = t


func _status(t: String) -> void:
	status.text = t


# ---------- Poses de départ, fichiers ----------

func _reload_presets() -> void:
	preset_btn.clear()
	_preset_paths = []
	preset_btn.add_item("— pose de départ —")
	_preset_paths.append("")
	var files := Array(DirAccess.get_files_at(POSES_DIR))
	var order := ["neutre", "repos", "garde"]
	files = files.filter(func(f): return f.ends_with(".json"))
	var rank := func(f: String) -> int:
		var i := order.find(f.get_basename())
		return 99 if i < 0 else i
	files.sort_custom(func(a, b): return a < b if rank.call(a) == rank.call(b) else rank.call(a) < rank.call(b))
	for f in files:
		preset_btn.add_item(f.get_basename())
		_preset_paths.append(POSES_DIR.path_join(f))
	preset_btn.select(0)


func _on_preset(i: int) -> void:
	if i <= 0:
		return
	var p := StickRig.load_pose(_preset_paths[i])
	_edit("preset", func(_p): return p)
	preset_btn.select(0)
	_status("Chargé : " + _preset_paths[i])


func _on_style(i: int) -> void:
	var s: String = StickRig.STYLES.keys()[i]
	if s == pose.style:
		return
	var restyle := func(p: Dictionary) -> Dictionary:
		p.style = s
		return StickRig.plant(p)
	_edit("preset", restyle)


func _save() -> void:
	var nom := name_edit.text.strip_edges().to_lower().replace(" ", "-")
	if nom == "" or not nom.is_valid_filename():
		_status("Donne un nom de fichier valide à la pose.")
		return
	pose.nom = nom
	var path := POSES_DIR.path_join(nom + ".json")
	var err := StickRig.save_pose(pose, path)
	if err != OK:
		# Projet exporté : res:// est en lecture seule.
		DirAccess.make_dir_recursive_absolute("user://poses")
		path = "user://poses/" + nom + ".json"
		err = StickRig.save_pose(pose, path)
	if err == OK:
		_status("Enregistré : " + ProjectSettings.globalize_path(path))
		_reload_presets()
	else:
		_status("Échec de l'enregistrement (%s)." % error_string(err))
	_sync_json()


func _apply_json() -> void:
	var data = JSON.parse_string(json_edit.text)
	if not (data is Dictionary) or not data.has("angles"):
		_status("JSON illisible : il faut au moins un objet « angles ».")
		return
	var p := StickRig.normalize(data)
	json_edit.release_focus()
	_edit("json", func(_p): return p)
	_status("JSON appliqué.")
