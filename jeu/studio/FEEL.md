# FEEL.md : game feel et juice d'ÉCHO

> Poste : designer game feel / juice. Cible : Godot 4.5.1, rendu `gl_compatibility`, écran logique 192×352,
> mise à l'échelle entière, physique à 60 Hz. Une **image** (« i ») = 1/60 s = 16,7 ms.
> Toutes les positions affichées sont **arrondies au pixel** (pas de sous-pixel pour les sprites, caméra arrondie).
> Palette : lettres de `jeu/tools/palette.txt` (ex. `G` = or #ffd23f, `c` = cyan écho #3fd0d4).

---

## 0. Les 6 règles qui gouvernent tout le document

1. **Le système d'abord, le vernis ensuite.** Le persona Milo le dit : « ne pas confondre polish et correction d'un
   mauvais système ». Les contrôles (section 2) sont corrigés avant tout effet.
   *Raison : un saut mou reste mou, avec ou sans particules.*
2. **Zéro latence sur les actions du joueur.** Saut, demi-tour et accroche répondent **dans l'image même** du tap.
   Pas d'arrêt sur image (hitstop) ni d'anticipation qui retarde un geste du joueur.
   *Raison : chez Swink, le game feel est d'abord un « contrôle en temps réel » ; un retard casse la causalité.*
3. **Plus l'événement est rare, plus il est fort.** Le saut (2 par seconde) est discret, la mort et la gravure
   (quelques fois par partie) sont spectaculaires. C'est aussi la règle Android pour les vibrations.
4. **Les couleurs ont un sens fixe.** Rouge-rose (`x X z Z`) = danger et rien d'autre. Cyan (`q t c e`) = écho et
   gravure. Or (`g G y`) = récompense. Corail (`r R o a`) = le héros. Les effets n'empruntent jamais la famille d'un autre.
   *Raison : le joueur lit le danger en 100 ms ; un effet rose sur un piège neutre le trompe.*
5. **Le pixel reste un pixel.** Pas de mise à l'échelle ni de rotation des sprites par calcul (méthode E2-G et E7-D) :
   l'écrasement-étirement est **dessiné** en images dédiées. Tremblement en pixels entiers, pas de rotation de caméra,
   pas de zoom en jeu.
6. **Lisibilité avant tout.** Budget d'effets simultanés, priorités, et option « Réduire les effets » (section 8).
   *Raison : Milo : « une interface qui attire l'attention sur tout ne hiérarchise rien ».*

---

## 1. Diagnostic du prototype actuel (`world.gd`)

| Point | Actuel | Problème | Correction (section) |
|---|---|---|---|
| Gravité | 700 px/s², identique en montée et en chute | Saut « flottant », sans poids | 2.2 |
| Tap | traité dans `_unhandled_input`, hors pas physique | Ordre d'exécution aléatoire, pas de buffer | 2.1 |
| Tap juste avant le mur | consommé comme **demi-tour** | Le joueur voulait rebondir : il repart à l'envers. Frustration n°1 probable | 2.5 |
| Glissade | 0 px/s pendant 0,22 s puis 14 px/s fixe | Rester au mur ne coûte rien (la marée monte de 9 à 30 px/s) | 2.3 |
| Laser | touche si \|dy\| < 8 px | Plus large que le corps du héros (6 px) : mort injuste | 2.6 |
| Tremblement | aléatoire chaque image, ±4 px, décroissance linéaire | Bruit blanc illisible, pas de direction | 3.1 |
| Arrêt sur image | 180 ms à la mort, rien ailleurs | Trop long, aucun réglage par événement | 3.2 |
| Particules | 1 px, fondu alpha | La méthode interdit le fondu (E2-G) ; aucun preset | 3.3 |
| Caméra | `lerp` 6/s sans zone morte | Glisse en continu pendant la glissade ; décalage d'1 px héros/caméra | 5 |
| Vibration | 70 ms à la mort, 30-40 ms en UI | Aucun retour au toucher pendant le jeu | 3.6 |
| Musique | une boucle fixe de 8 mesures | Aucune réaction à la hauteur, au danger, au flow | 7 |
| Écrasement-étirement | aucun | Héros rigide | 3.4 |

---

## 2. Contrôles

### 2.1 Entrée tactile

- Lire `InputEventScreenTouch` avec `pressed == true` (l'appui, **pas le relâchement** : gain de 60 à 120 ms).
  Garder l'émulation souris pour le bureau.
- Chaque appui est **mis en file** (`tap_queue.append(Time.get_ticks_msec())`) et consommé dans `_physics_process`.
  *Raison : un seul endroit modifie la physique, les replays d'écho restent déterministes.*
- Activer `input_devices/buffering/agile_event_flushing = true` dans `project.godot` (Android : événements traités
  plusieurs fois par image au lieu d'une).
- Deux doigts = deux taps valides. Pas de zone morte à l'écran : tout l'écran sous la barre de HUD (y > 40) est zone de tap.

### 2.2 Courbe de saut (rebond de mur à mur)

Objectif : **montée vive, apex court et suspendu, chute lourde**, en gardant le temps de traversée et le gain de
hauteur proches du prototype pour ne pas casser la génération de la tour (`tower.gd`).

| Constante | Actuel | Proposé | Pourquoi |
|---|---|---|---|
| `JUMP_VX` | 210 px/s | **232 px/s** | Traversée de 116 px en **31 i (0,52 s)** au lieu de 34 i : plus nerveux |
| `JUMP_VY` | −290 px/s | **−350 px/s** | Impulsion franche, le départ « claque » |
| `G_UP` (vy < 0) | 700 | **960 px/s²** | Montée courte : apex en **23 i (0,38 s)** |
| `APEX_BAND` / `APEX_MUL` | aucun | **\|vy\| < 30 px/s → gravité × 0,45** | Suspension de ~4 i à l'apex : le joueur « sent » le sommet et a le temps de décider (technique Celeste : demi-gravité sous 40 px/s) |
| `G_DOWN` (vy ≥ 0) | 700 | **1500 px/s²** | Chute lourde : 100 px de chute en 26 i au lieu de 32 |
| `MAX_FALL` | 330 | **300 px/s** | Reste lisible : 5 px par image maximum |

Résultat simulé (pas fixe de 60 Hz) : apex à **61 px** (3,8 m), arrivée au mur opposé à vy = +159 px/s,
**gain net 51 px par rebond** (actuel : 49 px). La tour reste jouable telle quelle.

```gdscript
func _gravity() -> float:
	var g := G_UP if vel.y < 0.0 else G_DOWN
	if absf(vel.y) < APEX_BAND:
		g *= APEX_MUL
	return g
# dans _step_player, en l'air :
vel.y = minf(vel.y + _gravity() * dt, MAX_FALL)
```

**Pas de saut à hauteur variable** (appui long) : le contrôle est à un doigt, et le tap en l'air sert au demi-tour.
*Raison : des arcs identiques rendent les échos lisibles et les pièges prévisibles ; l'expression du joueur passe par
le moment du saut et du demi-tour.*

### 2.3 Accroche et glissade

| Phase | Valeur | Pourquoi |
|---|---|---|
| Contact au mur | vitesse remise à 0, **accroche ferme 18 i (0,30 s)** à vy = 0 | Fenêtre de « rebond net » (section 6) |
| Glissade | vy passe de **12 à 48 px/s** en **90 i (1,5 s)**, courbe en carré (`lerp(12, 48, k*k)`) | Rester au mur devient une décision : à 48 px/s on perd plus vite que la marée ne monte au début |
| Glissade jusqu'au sol | pose au sol, plus de glissade | Inchangé |
| Rebond depuis le mur | toujours vers le mur opposé, pas de direction à choisir | Contrôle à un doigt |

Inspiration : Celeste fait passer la vitesse de glissade de 20 px/s au maximum de chute en 1,2 s (`WallSlideStartMax`,
`WallSlideTime`).

### 2.4 Demi-tour en l'air

| Paramètre | Valeur | Pourquoi |
|---|---|---|
| Effet | `vel.x = -vel.x` ; `vel.y = minf(vel.y, -220)` | Petit rebond de **25 px** (220² / 2×960) : il sert à esquiver, pas à grimper |
| Nombre | **1 par saut** (réarmé au contact d'un mur) | Ressource lisible |
| Verrou après un rebond | **5 i (83 ms)** après le départ du mur : tap ignoré pour le demi-tour | Évite le double tap involontaire (rebond du doigt) qui renverrait le héros au mur |
| Hitstop | **0** | Règle 0-2 |
| Tap sans demi-tour disponible | bufferisé comme saut (2.5) ; s'il expire : petit retour « refusé » (événement 7) | Le joueur comprend pourquoi rien ne s'est passé |

### 2.5 Buffer d'entrée, coyote time et ambiguïté du tap

| Mécanisme | Valeur | Règle |
|---|---|---|
| **Saut anticipé vers le mur** (prioritaire sur le demi-tour) | le héros arrivera au mur visé dans **≤ 4 i** (≈ 15 px à 232 px/s) | Le tap est gardé et devient un **rebond dès l'image du contact**. Le demi-tour n'est pas consommé |
| **Buffer d'entrée** | **7 i (117 ms)** | Tout tap qui ne produit rien (pas de demi-tour disponible, ou état READY pas encore prêt) reste valide 7 i. Celeste utilise 0,08 s à la manette ; le tactile a 50 à 100 ms de latence en plus, d'où 117 ms |
| **Distance de rebond** | **3 px** | Si le héros est à ≤ 3 px de la face du mur, un tap = rebond (Celeste : `WallJumpCheckDist = 3`) |
| **Coyote time de mur** | **6 i (100 ms)** | Si le mur disparaît sous le héros (trou, bloc qui s'effrite dans un biome futur) ou si la glissade le fait sortir d'un pan de mur, il peut encore rebondir pendant 6 i. Celeste : `JumpGraceTime = 0,1 s` |
| **Grâce de piège** | aucune | Pas de mort retardée : la hitbox réduite (2.6) suffit et reste prévisible |

Pseudo-code de décision (dans `_physics_process`, avant `_step_player`) :

```gdscript
func _consume_taps() -> void:
	var now := Engine.get_physics_frames()
	while tap_queue.size() > 0 and now - tap_queue[0] > BUFFER_FRAMES:
		tap_queue.pop_front()                      # taps périmés
	if tap_queue.is_empty():
		return
	if side != 0 or coyote_frames > 0:
		_jump(); tap_queue.pop_front(); return
	var frames_to_wall := _frames_to_wall()        # distance au mur visé / |vel.x| * 60
	if frames_to_wall <= 4 or _dist_to_wall() <= 3.0:
		return                                     # garder le tap : rebond au contact (_land le consommera)
	if turn_ok and now - jump_frame >= TURN_LOCK:
		_air_turn(); tap_queue.pop_front()
	# sinon : le tap attend (buffer) ; s'il expire sans effet -> Juice.fire(&"turn_deny")
```

Et dans `_land(s)` : `if not tap_queue.is_empty(): tap_queue.pop_front(); _jump()` (rebond dans l'image du contact,
l'effet « contact au mur » est joué quand même pendant 1 i).

### 2.6 Hitboxes (tolérances)

Silhouette du héros ≈ 10×14 px dans une cellule 16×16 (mesuré sur `game/assets/sprites/player.png`, 5 images de 16×16).

| Boîte | Actuel | Proposé | Écart avec le visuel |
|---|---|---|---|
| **Corps mortel du héros** (hurtbox) | 8×12 (`HALF = 4,6`) | **6×10** (`HURT_HALF = Vector2(3, 5)`), centrée sur le torse, 1 px plus bas que le centre de la cellule | 60 % × 71 % de la silhouette : l'écharpe, la capuche et les pieds ne tuent jamais |
| **Ramassage** (éclats, power-ups) | 18×20 | **18×20 + aimant** : un éclat à moins de **14 px** du centre file vers le héros à 180 px/s | 130 % à 150 % du visuel : ramasser est généreux |
| **Pics** | zone = profondeur 7 px × (h − 4) | profondeur **5 px** (pointes seules) × (h − 6) | Le socle des pics ne tue pas ; 3 px de marge en haut et en bas |
| **Scie** | distance < 6 px | **rayon mortel 5 px** pour un sprite de 7-8 px de rayon | Les dents qui dépassent ne tuent pas |
| **Laser** | \|dy\| < 8 px dès l'état 2 | \|dy\| < **HURT_HALF.y + 1 = 6 px** (demi-épaisseur du rayon : 1 px), et seulement après **3 i** d'état actif (montée de 50 ms) | Le rayon doit visiblement toucher le corps |
| **Marée** | pieds sous la surface + 5 px | **centre du héros** sous la surface + 2 px | On meurt quand on est « dedans », pas quand on l'effleure |

Règle générale : **ce qui tue est plus petit que ce qu'on voit, ce qui récompense est plus grand.**
Ces boîtes sont exprimées par rapport au **pivot** du sprite (méthode E8-A), pas au coin de l'image.

---

## 3. Le vocabulaire du juice (briques réutilisables)

### 3.1 Tremblement d'écran (screen shake)

Modèle : amplitude `A` (px), durée `D` (ms), décroissance **quadratique** `a(t) = A × (1 − t/D)²`, direction optionnelle.

- Nouveau décalage **toutes les 2 images** (30 Hz), pas chaque image : le bruit à 60 Hz devient une bouillie.
- Décalage = `round(a × r)` avec `r` aléatoire dans [−1, 1] (ou projeté sur la direction ±20°). En dessous de 0,5 px : 0.
- **Directionnel par défaut** (comme Celeste `DirectionalShake`) : l'écran bouge dans l'axe du choc. Plus lisible.
- **Jamais de rotation, jamais de zoom.** Amplitude maximale du jeu : **4 px** (2 % de la largeur).
- Cumul : on prend le **maximum** des tremblements en cours, jamais la somme.
- **Coup de caméra** (kick, technique Vlambeer) : décalage directionnel unique de 1 à 3 px qui revient en 6 i
  (`kick *= 0.6` par image, arrondi). Nijman décrit pour Nuclear Throne un recul de caméra de 6 px + 4 de tremblement par tir ;
  ÉCHO est un jeu de précision, on divise par deux.

| Niveau | A | D | Usage |
|---|---|---|---|
| S0 | 0 | 0 | sauts, contacts, éclats |
| S1 | 1 px | 100 ms | power-up, achat, chute au sol depuis haut |
| S2 | 2 px | 180 ms | gravure (directionnel vertical), record |
| S3 | 3 px | 250 ms | mort par piège |
| S4 | 4 px | 350 ms | mort sur la dernière vie |

### 3.2 Arrêt sur image (hitstop) et ralenti

- Le **monde** s'arrête (héros, pièges, marée, échos, `t_life`), mais **pas** l'UI, le son, le tremblement ni les particules d'impact.
  Implémenté par un compteur d'images, **pas** par `Engine.time_scale` (qui figerait aussi les tweens d'UI).
- Valeurs variées selon l'événement (la méthode E7-F : « un arrêt identique partout devient mécanique ») :
  **0 ms** pour toute action du joueur, **50 ms** (3 i) pour une prise de power-up, **100 ms** (6 i) pour une mort,
  jamais plus de 120 ms. Celeste fige 0,05 s au dash et 0,1 s sur les gros impacts.
- **Ralenti** : uniquement à la mort de la **dernière vie** (fin d'ascension) : ×0,35 pendant 400 ms, retour linéaire en 150 ms.
  Jamais de ralenti pendant que le joueur contrôle : il fausse le rythme appris et les replays d'écho.

### 3.3 Particules : presets

Règles de dessin : carrés de 1 ou 2 px, **positions arrondies**, **pas de fondu alpha** (méthode E2-G : on efface par
morceaux). Une particule **vieillit en descendant sa rampe de palette** (ex. `y → G → g → disparaît`) par tiers de vie ;
les 2×2 deviennent 1×1 à mi-vie. Les éclats lumineux suivent l'escalier de la méthode E2-H :
point → croix 3 px → croix 5 px → croix 3 px → point → rien (6 états de 2 i), **un seul éclat de ce type à l'écran**.

| Preset | Nombre | Couleurs (rampe) | Vitesse (px/s) | Émission | Vie (i) | Gravité (px/s²) | Freinage /i |
|---|---|---|---|---|---|---|---|
| `dust_wall` | 4 | `p → l → m` | 20-45 | cône ±35° opposé au mur | 12-20 | 60 | 0,90 |
| `spark_jump` | 3 | `a → o → R` | 25-40 | cône ±25° opposé au saut, depuis les pieds | 8-14 | 0 | 0,88 |
| `slide_dust` | 1 toutes les 6 i | `l → m` | 5-10 vers le bas | contre le mur, au niveau des mains | 14-20 | 40 | 0,95 |
| `turn_ring` | 6 | `w → p → l` | 40 | anneau (6 directions à 60°, ±10°) | 10 | 0 | 0,85 |
| `near_spark` | 3 | `w → a` | 30-60 | depuis le point du piège le plus proche, vers l'extérieur | 8-12 | 0 | 0,85 |
| `shard_pop` | 6 + 1 éclat-croix | `y → G → g` | 30-60 | cercle | 14-22 | 30 | 0,90 |
| `shard_set` | 10 | `y → G` | 50-80 | cercle + 1 éclat-croix | 18-26 | 0 | 0,90 |
| `elan_up` | 8 | `a → o` | 50 | anneau autour du héros | 14 | −20 | 0,88 |
| `death_shatter` | 8 chauds + 8 cyan | `o → R → r` / `e → c → t` | 40-90 | cercle ; les cyan **montent** (gravité −20), les chauds tombent | 24-40 | 120 / −20 | 0,92 |
| `engrave_rise` | 12 | `e → c → t → q` | 10-20 vers le haut | le long du contour du piège | 30-45 | −10 | 0,97 |
| `echo_wisp` | 1 toutes les 8 i | `c → t → q` | 0-5 | derrière chaque écho | 18 | −10 | 0,95 |
| `echo_relive` | 6 | `e → c → t` | 20-40 | point de mort de l'écho | 20 | −15 | 0,92 |
| `respawn_ring` | 6 | `p → c` | 35 | anneau au sol | 12 | 0 | 0,85 |
| `record_line` | 12 | `y → G → g` | 30-60 vers le haut | réparties sur la ligne de record (x de 40 à 152) | 24-32 | 20 | 0,93 |
| `tide_bubble` | 1 toutes les 10 i (×3 en danger) | `U → u` | 15-25 vers le haut | surface de la marée | 30-50 | 0 | 1,0 |
| `power_ring` | 8 | `y → a → o` | 70 | anneau | 16 | 0 | 0,88 |
| `ui_confetti` | 10 | `y`, `G`, `o`, `c` | 60-110 | cône vers le haut ±50° | 30 | 200 | 0,96 |
| `coin_fly` | 1 par éclat (max 12) | sprite éclat 8×8 | arc de Bézier vers le compteur | départ échelonné de 40 ms | 24-36 | n/a | n/a |

### 3.4 Écrasement-étirement (squash & stretch) : images dessinées

La méthode interdit de réduire ou d'agrandir un sprite par calcul. Les déformations sont des **images de la planche du
héros**, dessinées avec le pipeline complet. Silhouette de référence 10×14 ; règle du volume (E1-1) : −2 px dans l'axe
du choc = +2 px perpendiculaire. Celeste pousse à 0,6 × 1,4 en vectoriel ; à 10 px de large on reste à **±20 %**
(2 px), sinon la silhouette casse.

| Image | Taille silhouette | Durée | Moment |
|---|---|---|---|
| `wall_impact` | **8×16** (écrasé contre le mur) | 3 i (50 ms) | contact au mur |
| `wall_overshoot` | **11×13** | 2 i (33 ms) | après l'impact, puis pose d'accroche |
| `jump_stretch` | **8×16**, étiré dans l'axe du saut (diagonale), écharpe en traînée (smear autorisé, 1 seule image) | 3 i | départ du saut |
| `rise` (×2, boucle) | 10×14 | 5 i chacune | montée |
| `apex` | **11×13**, groupé | tenue tant que \|vy\| < 30 | apex |
| `fall` (×2) | **9×15**, étiré vers le bas | 5 i chacune | chute |
| `turn` (×3) | 12×12 (boule), puis 11×13, puis 10×14 | 2 i + 3 i + 3 i | demi-tour |
| `floor_land` | **12×12** | 4 i | pose au sol de départ |
| `slide` (×2) | 10×14, écharpe qui flotte vers le haut | 6 i chacune | glissade |
| `cling_idle` (×2) | 10×14, respiration en sous-pixel (E2-D) | 36 i chacune | accroché |
| `respawn_pop` (×4) | **6×8 (≈50 %)** → **11×15 (≈110 %)** → 10×13 → 10×14 | 3 i, 3 i, 4 i, 5 i | réapparition (méthode E2-G) |

**Écharpe** : elle suit le corps avec **2 images de retard** et dépasse de 1-2 px avant de revenir (E1-5).
**Anticipation sans latence** : la pose d'accroche est déjà ramassée (genoux pliés) ; c'est elle qui joue le rôle
d'anticipation. Le saut part dans l'image du tap, sur `jump_stretch`. La planche passe de 5 à **24 images** ; cellule
**16×16** gardée (tous les écrasements ci-dessus tiennent dedans), pivot fixe au centre du torse.

### 3.5 Sons : recettes synthétisables (`tools/sfx.py`)

Notation des fonctions existantes : `sweep(f0, f1, durée, forme, vol, duty)`, `noise(durée, vol, lp)`,
`notes([fréquences], durée_par_note, forme, vol, duty)`. Ajouter à `sfx.py` : `delay(sig, ms, gain)` (écho),
`am(sig, hz, profondeur)` (trémolo), et un générateur de **3 variantes** par son fréquent (graines différentes) pour
éviter la répétition. À l'exécution : variation de hauteur ±3 % (déjà dans `Sfx.play`).

| Son | Recette | Durée |
|---|---|---|
| `jump` | `sweep(300, 720, .07, square, .16, duty .25)` + `noise(.03, .05, .9)` décalé de 10 ms | 70 ms |
| `land` (×3) | `noise(.045, .22, .3)` + `sweep(110, 70, .06, tri, .18)` (le « toc ») | 60 ms |
| `slide` (boucle) | `am(noise(1.0, .06, .15), 12 Hz, .7)` ; volume ∝ vitesse de glissade | boucle 1 s |
| `turn` | `sweep(620, 1040, .06, square, .14, .125)` + `noise(.08, .05, .8)` | 80 ms |
| `turn_deny` | `sweep(180, 150, .05, tri, .10)` | 50 ms |
| `near_miss` | bruit dont le filtre passe de lp .9 à .3 en 110 ms (vol .12) + `notes([1568], .04, tri, .08)` à +30 ms | 110 ms |
| `shard` | `notes([1318.5, 1975.5], .05, square, .14, .25)` ; hauteur selon la chaîne (section 6.3) | 100 ms |
| `shard_set` | `notes([1318.5, 1568, 1975.5, 2637], .05, tri, .2)` + `delay(150 ms, .3)` | 350 ms |
| `elan_up` | arpège montant 3 notes dans la tonalité du biome, `square .25`, 55 ms/note, vol .14 + `noise` qui enfle 150 ms | 220 ms |
| `elan_cash` | ticks `notes([2637], .015, square, .08, .125)` répétés, +1 demi-ton par tick | 40 ms/tick |
| `elan_break` | `notes([659.25, 440], .08, tri, .10)` (doux, pas punitif) | 160 ms |
| `milestone` | `notes([880], .03, tri, .08)` + `notes([1760], .06, tri, .06)` | 90 ms |
| `record_near` | `am(notes([1318.5], .3, tri, .05), 8 Hz, .5)` | 300 ms |
| `record` | existant, raccourci à **≤ 600 ms** | 480 ms |
| `laser_charge` | `sweep(600, 1400, durée_de_charge, square, .05, .5)` ; volume selon distance (0 au-delà de 120 px) | 0,5-1 s |
| `saw_near` (boucle) | `am(sweep(90, 90, 1.0, square, .04, .5), 30 Hz, .5)` + bruit aigu lp .9 vol .02 ; seulement à < 80 px | boucle |
| `die` | `sweep(440, 70, .35, square, .25)` + `noise(.06, .3, .95)` (verre) + à +120 ms `sweep(200, 900, .35, tri, .10)` (l'âme qui devient écho) | 470 ms |
| `die_tide` | `sweep(220, 40, .5, tri, .25)` + `noise(.6, .15, .1)` | 600 ms |
| `engrave` | `noise(.15, .12, .7)` (le burin) puis `notes([523.25, 783.99, 1046.5], .15, tri, .25)` + `delay(150, .4)` + `delay(300, .16)` | 900 ms |
| `echo_spawn` | `sweep(523, 1046, .2, tri, .06)` + `delay(150, .4)` + `delay(300, .16)` | 500 ms |
| `echo_relive` | `notes([1046.5], .03, tri, .05)` + `delay(150, .35)` | 200 ms |
| `respawn` | `notes([392, 523.25, 784], .04, square, .14, .25)` + `noise(.05, .06, .5)` | 170 ms |
| `tide_rumble` (boucle) | `noise(1.0, .15, .05)` + `am(tri 55 Hz, 2 Hz, .5)` ; volume piloté par la distance | boucle |
| `heartbeat` | `sweep(70, 45, .07, tri, .3)` ×2 espacés de 140 ms | 210 ms |
| `biome` | 4 notes `tri` de 120 ms dans la nouvelle tonalité + nappe `tri` 1,2 s vol .08 | 1,7 s |
| `power_up` | `notes([659, 830, 988, 1318, 1661], .045, square, .14, .25)` + `delay(100, .3)` | 330 ms |
| `power_end` | `notes([988, 659], .09, square, .10, .5)` | 180 ms |
| `last_life` | `sweep(110, 110, .1, tri, .2)` ×2 espacés de 180 ms | 280 ms |
| `click` / `back` | existant / `sweep(700, 900, .03, square, .15, .25)` | 30 ms |
| `buy` | `notes([1318.5, 1760], .05, square, .16, .25)` + `noise(.01, .2, .95)` + ticks `elan_cash` | 150 ms |
| `deny` | existant + le bouton tremble | 160 ms |
| `tick` / `go` | `notes([880], .04, square, .12, .5)` / `notes([1760], .08, square, .12, .5)` | 40 / 80 ms |

Banques libres si l'équipe son préfère du sample : **Kenney** (packs audio en CC0, dont « Interface Sounds »,
« Impact Sounds », « Music Jingles »), **OpenGameArt** filtré sur CC0, **Freesound** filtré sur CC0, **jsfxr** pour
prototyper. Vérifier la licence **sur la page de chaque fichier** et la consigner dans `jeu/game/audio/LICENSES.md`.

### 3.6 Vibrations Android

Contraintes vérifiées :
- Godot : `Input.vibrate_handheld(duration_ms, amplitude)` ; amplitude 0 à 1 (ramenée à 1-255 côté Android,
  −1 = valeur par défaut). Permission `VIBRATE` à cocher dans le preset d'export, sinon aucun effet.
- Godot passe par une vibration « one-shot ». Le guide Android la déconseille pour les retours fins car elle
  « bourdonne » : l'actionneur continue de sonner 20 à 50 ms après la fin du signal. Un bon « clic » dure **10 à 20 ms**.
  Donc : **impulsions courtes uniquement**, jamais plus de 60 ms.
- Guide Android : la force suit l'importance et la rareté ; écart d'au moins **50 ms** entre deux impulsions pour qu'on
  les distingue ; écarts d'intensité d'un rapport **≥ 1,4** pour qu'on les perçoive. Entre « bourdonnant » et « rien », choisir rien.

| Niveau | Durée | Amplitude | Usage |
|---|---|---|---|
| H1 tic | 10 ms | 0,25 | UI, contact au mur (mode Complet seulement) |
| H2 tape | 15 ms | 0,45 | éclat, frôlement, demi-tour refusé |
| H3 coup | 30 ms | 0,70 | power-up, record, achat |
| H4 choc | 60 ms | 1,00 | mort |
| Motifs | H2 · 70 ms · H2 (double) ; H2 ×3 espacés de 150 ms (gravure, calés sur les 3 notes) | | |

Limiteur : **≥ 50 ms** entre deux vibrations, **≤ 4 par seconde**, une vibration plus forte remplace une plus faible en
attente. Option possible plus tard : petit plugin Android (v2) qui appelle `performHapticFeedback` avec les constantes
système (`CONFIRM`, `REJECT`, `CLOCK_TICK`), recommandées par Android pour la cohérence.

---

## 4. Catalogue des événements de feedback (39)

Légende : **Temps** = hitstop / ralenti. **S&S** = image d'écrasement-étirement (3.4). Particules : preset de 3.3.
Son : recette de 3.5. Haptique : niveau de 3.6 (« C » = seulement en mode Vibrations Complètes).
Flash du héros = paramètre `flash` du shader `skin` (couleur `w`).

### A. Mouvement

| # | Événement | Visuel | S&S | Caméra | Temps | Son | Haptique |
|---|---|---|---|---|---|---|---|
| 1 | **Premier saut** (départ d'ascension) | `spark_jump` ×2 + `dust_wall` ; texte « TAP » sort en 150 ms ; la marée s'éveille (bulles ×3 pendant 1 s) | `jump_stretch` | kick 1 px vers le haut | 0 | `start` puis `jump` | H2 |
| 2 | **Rebond** (saut depuis le mur) | `spark_jump` (3 px) + `dust_wall` (4 px) côté mur | `jump_stretch` 3 i | S0 | 0 | `jump` (±3 %) | aucune |
| 3 | **Contact au mur** | `dust_wall` 4 px ; si vy > 200 : 6 px | `wall_impact` 3 i → `wall_overshoot` 2 i | kick 1 px vers le mur si vitesse > 200 px/s | 0 | `land` (variante aléatoire) | H1 C (cooldown 150 ms) |
| 4 | **Rebond net** (rebond < 18 i après contact) | le `spark_jump` passe en or `a` ; 1 px d'éclat sur l'écharpe | idem 2 | S0 | 0 | `jump` à +2 demi-tons | aucune |
| 5 | **Glissade** | `slide_dust` toutes les 6 i ; écharpe en image `slide` | `slide` | zone morte (section 5) | 0 | `slide` en boucle, volume ∝ vitesse | aucune |
| 6 | **Demi-tour en l'air** | `turn_ring` 6 px ; 2 images rémanentes du héros en `p` (3 i chacune) | `turn` 3 images | S0 | 0 | `turn` | aucune |
| 7 | **Demi-tour refusé** (déjà utilisé, buffer expiré) | 2 px gris `m` qui tombent depuis le héros ; icône de demi-tour du HUD clignote `m` 2 fois en 200 ms | aucune | S0 | 0 | `turn_deny` | H2 C |
| 8 | **Pose au sol de départ** (glissade jusqu'en bas) | `dust_wall` ×2 de chaque côté | `floor_land` 4 i | S1 vertical si chute > 100 px | 0 | `land` grave (pitch 0,8) | H1 C |

### B. Danger et survie

| # | Événement | Visuel | S&S | Caméra | Temps | Son | Haptique |
|---|---|---|---|---|---|---|---|
| 9 | **Piège qui s'annonce** (laser en charge, scie qui entre dans l'écran) | laser : la ligne pointillée clignote 10 Hz (existant) + 1 px `Z` à l'émetteur ; scie : 2 étincelles `Z` par seconde sur le rail | aucune | S0 | 0 | `laser_charge` / `saw_near` selon distance | aucune |
| 10 | **Frôlement** (near-miss : hurtbox à ≤ 4 px d'une zone mortelle, sans la toucher, piège non gravé) | `near_spark` 3 px `w`/`a` au point le plus proche ; texte « FRÔLÉ » 1 fois par piège, 5×7 px, `a`, monte de 6 px en 30 i | aucune | S0 | 0 | `near_miss` | H2 |
| 11 | **Mort par piège** | voir séquence 4.1 : flash `w` 2 i, piège flash `Z` 2 i, `death_shatter` 16 px, anim `death` 5 images | aucune (anim `death`) | **S3** dans l'axe piège → héros | **hitstop 100 ms** | `die` + basse de la musique filtrée | **H4** à l'impact |
| 12 | **Mort par la marée** | le héros s'enfonce de 8 px en 18 i, silhouette qui passe en `u` puis `U` ; 8 `tide_bubble` ; pas de flash | aucune | S1 vertical | 0 (pas d'impact) | `die_tide` | H3 + H3 à 120 ms |
| 13 | **Marée : niveau 1** (surface à < 200 px sous le héros) | `tide_bubble` ×3 ; liseré de 2 px `U` en bas de l'écran si la marée est hors champ | aucune | biais caméra (section 5) | 0 | `tide_rumble` vol 0 → 0,08 | aucune |
| 14 | **Marée : niveau 2** (< 120 px) | bande tramée (damier 50 %) `u` de 8 px en bas de l'écran, pulsée à 80 bpm (2 i allumée / 2 i éteinte) | aucune | biais −16 px | 0 | `heartbeat` à 80 bpm, couche musicale « Silence » | aucune |
| 15 | **Marée : niveau 3** (< 60 px) | bande 12 px pulsée à 120 bpm ; bulles ×3 | aucune | biais max | 0 | `heartbeat` 120 bpm + passe-bas musique 1800 Hz | H1 sur chaque battement (C) |
| 16 | **Dernière vie** (début de la 4ᵉ vie) | icône de vie restante clignote `z` 3 fois (6 i allumé / 6 i éteint) ; l'écharpe du héros gagne 1 px de traîne `R` | aucune | S0 | 0 | `last_life` | H2 double |

#### 4.1 Séquence mort → gravure → réapparition (le cœur du jeu)

La gravure est **le moment le plus gratifiant du jeu** : c'est l'identité d'ÉCHO. Elle doit transformer la mort en progrès.

| t (ms) | Ce qui se passe |
|---|---|
| 0 | Contact. Monde figé **100 ms**. Héros en `w` pendant 2 i, puis couleurs normales figées. Le piège tueur flashe `Z` 2 i. Tremblement S3 directionnel. Son `die`. Vibration H4. Musique : passe-bas vers 500 Hz en 150 ms, −6 dB |
| 100 | Animation `death` (5 images × 83 ms). `death_shatter` : les parts chaudes tombent, les parts cyan montent (le héros devient écho) |
| 520 | Caméra glisse vers le piège en **350 ms** (sortie en douceur, cubique) |
| 870 | Bandes noires cinéma (`k`, 8 px en haut et en bas) entrent en 150 ms |
| 1020 | **Gravure, 900 ms** : son `engrave`. Le piège passe de `X/z` à `t/c` par **cycle de palette** en 4 paliers de 83 ms, balayé de bas en haut (1 rangée de pixels par image). 3 notes du carillon à +150, +300, +450 ms, chacune calée sur **H2** et sur un éclat-croix `e` sur le piège. `engrave_rise` 12 px. Tremblement S2 vertical sur la 3ᵉ note. Tampon « GRAVÉ » (police UI, `c`) : pop 50 % → 115 % (redessiné) → 100 % en 3 images |
| 1920 | Bandes noires sortent en 150 ms ; panneau « Vie perdue » entre en 250 ms |
| tap | Caméra redescend au départ en 400 ms (entrée-sortie douce) pendant que la marée recule (400 ms) |
| +400 | `respawn_pop` (4 images, 250 ms), `respawn_ring`, son `respawn`. Les échos apparaissent (événement 19). Taps ignorés pendant 300 ms (anti-tap accidentel), puis état READY |

**Accélération** : un tap pendant la séquence la joue ×2. Elle n'est jamais sautée entièrement les 3 premières fois
qu'un joueur la voit (apprentissage). La séquence n'est jamais rallongée par d'autres effets (règle de priorité, section 8).

### C. Récompenses et progression

| # | Événement | Visuel | S&S | Caméra | Temps | Son | Haptique |
|---|---|---|---|---|---|---|---|
| 17 | **Éclat ramassé** | `shard_pop` + anim `shard_pop` existante ; compteur HUD : le chiffre monte de 1 px pendant 4 i | aucune | S0 | 0 | `shard`, hauteur selon la chaîne (6.3) | H2 |
| 18 | **Grappe d'éclats complète** (tous les éclats d'un groupe) | `shard_set` + éclat-croix `y` | aucune | S0 | 0 | `shard_set` | H2 double |
| 19 | **Apparition d'un écho** (début de vie) | chaque écho apparaît par **tramage** en 4 paliers (25/50/75/100 %, matrice de Bayer 4×4) de 3 i, décalés de 100 ms entre échos ; jamais de fondu alpha | aucune | S0 | 0 | `echo_spawn` (1 par écho, pitch +2 demi-tons à chaque) | aucune |
| 20 | **Écho qui passe près du héros** (≤ 12 px) | 1 `echo_wisp` de plus ; pas d'autre effet | aucune | S0 | 0 | aucun | aucune |
| 21 | **Écho qui revit sa mort** (le replay atteint son piège gravé) | `echo_relive` 6 px ; le piège gravé émet un éclat-croix `e` | aucune | S0 | 0 | `echo_relive` | aucune |
| 22 | **Passage d'un piège gravé** (le héros traverse un piège neutralisé) | le piège gravé s'éclaire d'un palier de palette (`t → c`) pendant 4 i | aucune | S0 | 0 | `echo_relive` à −5 demi-tons, vol ×0,5 | aucune |
| 23 | **Palier de 25 m** | la plaque fait un éclat-croix (6 états) ; le chiffre de hauteur HUD fait un pop (redessiné 1 px plus haut, 4 i) | aucune | S0 | 0 | `milestone` | aucune |
| 24 | **Ligne de record en vue** | la ligne pointillée `G` défile (1 px par 4 i) ; texte « RECORD » clignote 2 Hz | aucune | S0 | 0 | `record_near` | aucune |
| 25 | **Record battu** (en jeu) | `record_line` 12 px sur la ligne ; la ligne passe en `y` 4 i puis disparaît par morceaux ; bannière « NOUVEAU RECORD » en haut (entrée 200 ms, tenue 1,2 s, sortie 200 ms) ; cadre de 2 px `G` sur les bords de l'écran pendant 2 i (pas de flash plein écran) | aucune | **S2** vertical | 0 (on ne coupe pas l'élan) | `record` ; musique −4 dB pendant 600 ms | H3 + H2 à 80 ms |
| 26 | **Montée de palier d'Élan** (section 6) | `elan_up` 8 px ; la traîne de l'écharpe gagne une image rémanente ; badge d'Élan pop (3 images) | aucune | kick 1 px vers le haut | 0 | `elan_up` | H2 |
| 27 | **Élan encaissé** (rupture hors mort, section 6) | les éclats gagnés volent vers le compteur (`coin_fly`) ; badge qui se vide par morceaux | aucune | S0 | 0 | `elan_cash` (1 tick par éclat) | H1 par tick, max 4 |
| 28 | **Élan perdu** (par la mort) | badge qui se fragmente en 4 morceaux `m` | aucune | S0 | 0 | `elan_break` | aucune |
| 29 | **Prise d'un power-up** | `power_ring` 8 px ; héros flashe `a` 2 i ; icône dans le HUD : pop 3 images | `turn` image 1 (boule) 3 i | **S1** + kick 2 px vers le haut | **hitstop 50 ms** | `power_up` | H3 + H2 à 70 ms |
| 30 | **Fin d'un power-up** | les 3 dernières secondes : icône qui clignote à 4 Hz ; à la fin, 4 px `m` | aucune | S0 | 0 | `tick` à −3 s, −2 s, −1 s puis `power_end` | H1 |

### D. Ascension et méta

| # | Événement | Visuel | S&S | Caméra | Temps | Son | Haptique |
|---|---|---|---|---|---|---|---|
| 31 | **Changement de biome** | bannière « nom du biome » (entrée 300 ms, tenue 1,2 s, sortie 250 ms) ; la palette du décor passe à la nouvelle sur **16 m** de tour (frontière tramée, pas de fondu) ; 6 motes de la couleur d'accent du biome | aucune | S0 | 0 | `biome` ; musique : bascule à la mesure suivante (7.3) | H2 |
| 32 | **Fin d'ascension** (mort de la 4ᵉ vie) | comme 11, puis **ralenti ×0,35 pendant 400 ms** ; les 4 tombes de l'ascension s'allument `c` une à une (150 ms d'écart) avant l'écran de résultat | aucune | **S4** | hitstop 100 ms + ralenti | `die` puis accord final (mineur, ou majeur si record) | H4 + H3 à 200 ms |
| 33 | **Écran de résultat** | la hauteur compte de 0 à la valeur en 600 ms (ease-out), chaque palier de 10 m = `tick` ; barres qui se remplissent ; `ui_confetti` si record | aucune | n/a | n/a | `tick` (pitch qui monte) + `record` si record | H3 si record |

### E. Interface, boutique, récompenses vidéo

| # | Événement | Visuel | S&S | Caméra | Temps | Son | Haptique |
|---|---|---|---|---|---|---|---|
| 34 | **Bouton d'UI** (appui) | le bouton descend de **1 px** et son ombre de 2 px disparaît, tenue min 3 i ; l'action part au **relâchement** (sauf le tap de jeu) | aucune | n/a | n/a | `click` à l'appui (retour : `back`) | H1 |
| 35 | **Achat réussi** | compteur d'éclats qui descend en 400 ms (1 `tick` / 50 ms max) ; l'objet acheté pop 50 % → 115 % → 100 % (3 images redessinées) ; `ui_confetti` | aucune | n/a | n/a | `buy` | H3 |
| 36 | **Achat refusé** | le bouton tremble horizontalement ±2 px, 2 allers-retours en 200 ms ; le prix flashe `z` 2 i | aucune | n/a | n/a | `deny` | H2 double |
| 37 | **Récompense vidéo reçue** | les éclats gagnés volent depuis le centre vers le compteur (`coin_fly`, départs échelonnés de 40 ms, arcs de 400-600 ms) ; +1 vie : le cœur de vie pop | aucune | n/a | n/a | `reward` puis 1 `elan_cash` par arrivée (+1 demi-ton à chaque, max 12) | H1 par arrivée (max 4) + H3 à la fin |
| 38 | **Pause / reprise** | pause : le monde gèle instantanément ; reprise : compte à rebours 3-2-1 (chiffres redessinés, pop 3 images, 400 ms chacun) avant de rendre la main | aucune | n/a | n/a | `tick` ×3 puis `go` | H1 sur « go » |
| 39 | **Série quotidienne** (streak) au lancement | flamme du HUD : 3 images de flamme qui grandit ; nombre qui pop | aucune | n/a | n/a | `notes` ascendantes, 1 note par jour de série (max 7) | H2 |

---

## 5. Caméra

Le héros monte : la caméra doit montrer **ce qui arrive au-dessus** et **la marée en dessous** quand elle menace.

| Paramètre | Valeur | Pourquoi |
|---|---|---|
| Position cible du héros (montée) | **60 %** de la hauteur depuis le haut (211 px visibles au-dessus) | On voit les pièges 1,3 s à l'avance à la vitesse de montée moyenne |
| Position cible (chute, glissade, vy > 60) | **50 %**, transition en 24 i | Montrer la marée quand on descend |
| Anticipation de montée (look-ahead) | `lead = clamp(-vy * 0.04, 0, 12)` px vers le haut | À pleine vitesse de montée, 12 px de plus en haut |
| Zone morte verticale | **±10 px** autour de la cible | La caméra ne rampe pas pendant la glissade lente ni pendant l'apex |
| Lissage | exponentiel : `k = 7` vers le haut, `k = 4` vers le bas (`cam += (cible - cam) * (1 - exp(-k*dt))`) | Monter vite, descendre doucement (descendre est une mauvaise nouvelle, on ne la brusque pas) |
| Accroche finale | si \|cible − cam\| < 0,5 px : `cam = cible` | Évite le « tremblement d'1 px » en fin de lissage |
| Arrondi | caméra calculée sur `round(pos.y)` du héros, puis `camera.position.y = round(cam) + shake_offset` | Héros et caméra arrondis à partir de la même valeur : pas de saut d'1 px relatif |
| Plancher | jamais plus bas que la vue de départ (existant) | |

**Annonce de la marée** (lien avec les événements 13-15) :
- Distance `d` = surface de la marée − pieds du héros.
- `d < 200 px` : biais de caméra vers le bas `bias = lerp(0, 24, (200 - d) / 140)`, **plafonné** pour que le héros
  reste à au moins **35 %** depuis le haut (on voit toujours ce qui arrive au-dessus).
- Marée hors champ mais à moins de 1,5 écran : **jauge de Silence** en bas de l'écran, barre de 2 px `U` dont la
  largeur est proportionnelle à la proximité (192 px = à l'écran), clignote à partir de 120 px.

**Coup de poing (punch)** : pas de zoom (l'échelle entière l'interdit). Remplacé par :
- le **kick** directionnel de 1 à 3 px (3.1) ;
- les **bandes noires** de 8 px pour les moments cinéma (gravure, fin d'ascension) ;
- un panoramique doux vers le piège gravé (350 ms) au lieu de la coupe sèche actuelle (`focus()`).

```gdscript
func _update_camera(dt: float) -> void:
	var py := roundf(pos.y)
	var ratio := 0.60 if (side == 0 and vel.y < 60.0) else 0.50
	cam_ratio = move_toward(cam_ratio, ratio, dt / 0.4)
	var lead := clampf(-vel.y * 0.04, 0.0, 12.0) if vel.y < 0.0 else 0.0
	var desired := py - _vh() * cam_ratio - lead + _tide_bias()
	desired = minf(desired, 56.0 - _vh())
	var diff := desired - cam_y
	if absf(diff) <= DEAD_ZONE:
		return
	var goal := desired - signf(diff) * DEAD_ZONE
	var k := 7.0 if diff < 0.0 else 4.0
	cam_y += (goal - cam_y) * (1.0 - exp(-k * dt))
	if absf(goal - cam_y) < 0.5:
		cam_y = goal
# chaque image : camera.position = Vector2(0, roundf(cam_y)) + Vector2(Juice.offset)
```

---

## 6. Élan : combo et flow

### 6.1 Principe

L'Élan récompense le **rythme** (rebondir vite, frôler, ramasser) sans donner de **puissance** de jeu.
*Raison : Milo rappelle que le feedback positif amplifie un état et crée un effet boule de neige. L'Élan ne rend
donc pas le héros plus rapide ni plus fort : il donne du son, de l'image et des éclats.*

| Gain de points | Points |
|---|---|
| Rebond net (rebond moins de 18 i après le contact) | +1 |
| Frôlement (événement 10) | +2 |
| Éclat ramassé | +1 |
| Demi-tour suivi d'un frôlement ou d'un éclat dans les 30 i | +1 |

| Rupture | Effet |
|---|---|
| Accroché au mur plus de **54 i (0,9 s)**, ou glissade de plus de **24 px** | **Encaissement** : `floor(points / 10)` éclats gagnés (événement 27), Élan remis à 0 |
| Mort | Élan **perdu** sans encaissement (événement 28) |

*Raison : l'encaissement crée un choix de risque (continuer à enchaîner pour plus, ou souffler et encaisser) ;
la perte à la mort donne de l'enjeu sans punir le joueur prudent.* Le taux de conversion est à valider avec le poste économie.

### 6.2 Paliers

| Palier | Points | Traîne de l'écharpe | Musique | Visuel du HUD |
|---|---|---|---|---|
| 0 | 0-4 | aucune | couches 0-1 | rien |
| I | 5 | 1 image rémanente | — | badge « I » `o` |
| II | 15 | 2 images | + couche Rythme | badge « II » |
| III | 30 | 3 images | + couche Mélodie | badge « III » `a` |
| IV | 50 | 4 images + 1 px d'éclat `a` toutes les 10 i | mélodie à l'octave | badge « IV » `y` qui scintille |

**Lisibilité de la traîne** : images rémanentes = silhouette du héros **en aplat** (pas de transparence),
couleurs `R` puis `r` puis `n` (de la plus récente à la plus vieille), espacées de **3 i**, dessinées **sous** les pièges.
Jamais en `z/Z`, jamais en cyan (réservé aux échos). Le badge est en haut à gauche, 1 seul chiffre romain, pas de
compteur qui défile en continu.

### 6.3 Chaîne d'éclats

Éclats ramassés à moins de **1,5 s** d'intervalle : chaque éclat monte d'un degré sur la **gamme pentatonique de la mineur**
(demi-tons : 0, 3, 5, 7, 10, 12, 15, 17), `pitch_scale = pow(2, st / 12.0)`. Au-delà du 8ᵉ, on reste sur le dernier.
*Raison : technique classique de récompense sonore, la gamme pentatonique ne sonne jamais faux par-dessus la musique.*

---

## 7. Musique adaptative

### 7.1 Couches verticales (stems)

Chaque biome a **5 couches** de même longueur (8 mesures), jouées **ensemble** et mixées selon l'état du jeu.
Godot 4.3+ fournit `AudioStreamSynchronized` (plusieurs flux synchronisés, volume réglable par flux) et
`AudioStreamInteractive` (transitions entre morceaux à la mesure) : pas besoin de middleware.

| Couche | Contenu | Entre quand | Sortie |
|---|---|---|---|
| 0 Bourdon | basse triangle + nappe | toujours (y compris au menu) | jamais |
| 1 Pouls | arpège carré 12,5 % (l'actuel) | premier saut | fin d'ascension |
| 2 Rythme | percussions : grosse caisse `sweep(150, 50, .12, tri)`, charleston `noise(.03, lp .9)`, caisse claire `noise(.12) + tri 180 Hz` | Élan ≥ II **ou** hauteur de vie > 50 m | Élan < II et hauteur < 50 m, sortie en 2 temps |
| 3 Mélodie | lead carré 25 %, thème d'ÉCHO avec écho à 3/4 de temps | Élan ≥ III **ou** à moins de 10 m du record | sortie en 2 temps |
| 4 Silence | ostinato grave dissonant (triton) + souffle | volume piloté par la distance de la marée (0 à 200 px → 0, à 60 px → plein) | suit la distance, lissé 0,3 s |

- Entrée d'une couche : fondu de **1 mesure** (courbe en carré, pas linéaire). Sortie : **2 temps**.
- Marée à < 60 px : **passe-bas** sur le bus Musique, 8000 → 1800 Hz (`AudioEffectLowPassFilter`).
- Mort : passe-bas → 500 Hz en 150 ms et −6 dB ; retour en 600 ms à la réapparition.
- Bus : `Master` → `Music`, `SFX`, `UI`. Pendant `record` et `biome`, `Music` −4 dB (ducking) 600 ms.

### 7.2 Tempo et tonalité par hauteur

On ne change **jamais** le tempo en cours de morceau (ça change la hauteur des sons).
Chaque biome a son tempo et sa tonalité, la tension monte d'un biome à l'autre.
Pour des boucles **exactes à l'échantillon** à 22 050 Hz sur 8 mesures (32 temps), le tempo doit diviser 42 336 000 :

| Biome | Tempo | Tonalité | Longueur de boucle |
|---|---|---|---|
| 1 | 96 bpm | la mineur (actuel) | 441 000 échantillons (20,0 s) |
| 2 | 100 bpm | ré mineur | 423 360 (19,2 s) |
| 3 | 108 bpm | mi phrygien | 392 000 (17,8 s) |
| 4 | 112 bpm | do# mineur | 378 000 (17,1 s) |
| 5+ | 120 bpm | fa# mineur | 352 800 (16,0 s) |

### 7.3 Changement de biome

Bascule horizontale (`AudioStreamInteractive`) **à la fin de la mesure en cours**, fondu enchaîné d'**1 mesure**.
Le son `biome` est joué sur le premier temps du nouveau morceau.

### 7.4 Production

- **Option A (recommandée, cohérente avec le prototype)** : étendre `tools/sfx.py` avec `music_stems(biome)` qui écrit
  `music_b{n}_s{0..4}.wav`. Même générateur, même seed, longueur exacte du tableau ci-dessus.
  Import Godot : compression **QOA** (environ 5 fois plus petit que le PCM brut ; 25 couches × 20 s restent sous ~4 Mo).
- **Option B** : boucles CC0 (OpenGameArt filtré CC0, Kenney Music Jingles pour les jingles, Freesound CC0).
  Il faut alors des **stems séparés** de même longueur : rare en banque libre, d'où l'option A.

---

## 8. Règles anti-surcharge

### 8.1 Priorités

| Priorité | Contenu | Règle |
|---|---|---|
| P0 | Information vitale : annonce des pièges (9), marée (13-15) | Jamais masquée, jamais atténuée par un autre effet |
| P1 | Mort, gravure, fin d'ascension (11, 12, 32, 4.1) | Coupe tout P3-P4 en cours ; un seul P1 à la fois |
| P2 | Record, power-up, biome, dernière vie | Une bannière à la fois (file d'attente, 400 ms d'écart) |
| P3 | Élan, éclats, frôlement | Coupés pendant un P1 |
| P4 | Saut, contact, poussière, glissade | Premiers sacrifiés quand le budget est plein |

### 8.2 Budgets

| Ressource | Budget |
|---|---|
| Particules à l'écran | **96** au total, **24** par événement ; au-delà, on retire d'abord les P4 les plus vieilles |
| Tremblement | 1 seul actif (maximum, jamais la somme), 4 px maximum ; **aucun tremblement P3-P4 pendant qu'un laser charge à l'écran** |
| Arrêt sur image | 1 à la fois, 120 ms maximum, 0 sur les actions du joueur |
| Voix sonores | 8 (pool actuel) ; **2 instances maximum du même son** ; délai minimal : `land` 40 ms, `shard` 30 ms, `jump` 50 ms |
| Vibrations | ≥ 50 ms d'écart, ≤ 4 par seconde |
| Flashs | **≤ 3 par seconde** (seuil d'accessibilité WCAG 2.3.1) ; **jamais de flash plein écran** : flash du héros, du piège, ou cadre de 2 px |
| Texte flottant | 1 à la fois (« FRÔLÉ » ne se répète pas sur le même piège) |
| Images rémanentes | 4 maximum |

### 8.3 Zone sacrée

Les **64 px au-dessus du héros** sont la zone de décision. Les particules y sont dessinées **sous** les pièges
(z-index), et aucune particule rose-rouge ou cyan n'y apparaît hors mort et gravure.

### 8.4 Options (écran Réglages)

| Option | Valeurs | Effet |
|---|---|---|
| **Effets visuels** | Complets (défaut) / Réduits / Minimum | Réduits : tremblements ×0,5 (les S1 disparaissent à l'arrondi), particules ×0,5, pas de ralenti, pas de traîne d'Élan. Minimum : aucun tremblement ni kick, particules ×0,25, aucun flash (remplacé par un contour de 1 px), arrêts sur image plafonnés à 50 ms (ils portent de l'information) |
| **Vibrations** | Off / Légères (défaut) / Complètes | Légères : seulement les événements marqués sans « C ». Complètes : tout. Off : rien |
| Son / Musique | existant | |

Valeurs par défaut : effets Complets, vibrations Légères (le guide Android : trop de vibrations fait couper l'option entière).

---

## 9. Spec technique (Godot 4.5, GDScript)

### 9.1 Fichiers

| Fichier | Rôle |
|---|---|
| `game/scripts/juice.gd` | autoload **`Juice`** : tremblement, kick, arrêt sur image, ralenti, particules (données), flashs, vibrations, table des événements |
| `game/scripts/fx_layer.gd` | `Node2D` enfant de `World` (z_index 6) qui dessine les particules de `Juice` dans l'espace du monde |
| `game/scripts/juice_presets.gd` | constantes : presets de particules (3.3), table des événements (section 4) |
| `game/scripts/music.gd` | couches et paramètres musicaux (section 7), branché sur `Sfx` |
| `tools/sfx.py` | nouvelles recettes (3.5), variantes, stems |

`Juice` a `process_mode = PROCESS_MODE_ALWAYS` et est déclaré **avant** `World` dans les autoloads, pour qu'il
décompte l'arrêt sur image avant que le monde ne simule.

### 9.2 Interface publique

```gdscript
extends Node
## Juice : tout le retour sensoriel d'ÉCHO. Les scripts de jeu appellent fire() ; le reste est interne.

signal freeze_changed(frozen: bool)

var offset := Vector2i.ZERO        # décalage caméra (tremblement + kick), lu par World
var fx_level := 2                  # 0 minimum, 1 réduit, 2 complet (Game.data)
var haptic_level := 1              # 0 off, 1 légères, 2 complètes

func fire(ev: StringName, pos := Vector2.ZERO, ctx := {}) -> void   # joue une ligne de la table EVENTS
func shake(amp_px: float, dur_ms: int, dir := Vector2.ZERO) -> void
func kick(dir: Vector2, px: float) -> void
func hitstop(ms: int) -> void
func slowmo(scale: float, ms: int) -> void
func world_dt(dt: float) -> float                                   # 0 si figé, dt × ralenti sinon
func is_frozen() -> bool
func burst(preset: StringName, pos: Vector2, dir := Vector2.ZERO, mul := 1.0) -> void
func trail(preset: StringName, pos: Vector2) -> void                # émission continue (glissade, échos)
func flash(mat: ShaderMaterial, frames: int, color := Color("#dfe6ff")) -> void
func haptic(ms: int, amp: float, full_only := false) -> void
func sfx(name: StringName, semitones := 0.0) -> void                # passe à Sfx avec limiteur et priorité
```

### 9.3 Table des événements (données, pas de code)

```gdscript
# juice_presets.gd
const EVENTS := {
	&"jump":       {sfx = &"jump", burst = [&"spark_jump", &"dust_wall"], prio = 4},
	&"wall_land":  {sfx = &"land", burst = [&"dust_wall"], hap = [10, 0.25, true], prio = 4},
	&"air_turn":   {sfx = &"turn", burst = [&"turn_ring"], prio = 4},
	&"turn_deny":  {sfx = &"turn_deny", hap = [15, 0.45, true], prio = 4},
	&"near_miss":  {sfx = &"near_miss", burst = [&"near_spark"], hap = [15, 0.45, false], prio = 3},
	&"shard":      {sfx = &"shard", burst = [&"shard_pop"], hap = [15, 0.45, false], prio = 3},
	&"death_trap": {sfx = &"die", burst = [&"death_shatter"], shake = [3, 250], stop = 100,
	                flash = 2, hap = [60, 1.0, false], prio = 1},
	&"power_up":   {sfx = &"power_up", burst = [&"power_ring"], shake = [1, 100], kick = 2,
	                stop = 50, flash = 2, hap = [30, 0.7, false], prio = 2},
	# ... une ligne par événement de la section 4
}
```

`fire()` lit la ligne, applique les facteurs d'option (8.4), vérifie la priorité (8.1) et les budgets (8.2).
`ctx` transporte la direction du choc (`ctx.dir`) et un éventuel décalage de hauteur (`ctx.semitones`).

### 9.4 Cœur de `juice.gd` (pseudo-code)

```gdscript
const FRAME_MS := 1000.0 / 60.0
var _freeze := 0
var _slow := 1.0
var _slow_left := 0.0
var _sh := {amp = 0.0, dur = 0.0, t = 0.0, dir = Vector2.ZERO}
var _kick := Vector2.ZERO
var _last_hap := -1000
var particles: Array[Dictionary] = []

func hitstop(ms: int) -> void:
	_freeze = maxi(_freeze, int(round(ms / FRAME_MS)))

func world_dt(dt: float) -> float:
	return 0.0 if _freeze > 0 else dt * _slow

func shake(amp_px: float, dur_ms: int, dir := Vector2.ZERO) -> void:
	amp_px *= [0.0, 0.5, 1.0][fx_level]
	var left: float = _sh.amp * pow(1.0 - _sh.t / maxf(_sh.dur, 0.001), 2.0)
	if amp_px >= left:
		_sh = {amp = amp_px, dur = dur_ms / 1000.0, t = 0.0, dir = dir.normalized()}

func _physics_process(dt: float) -> void:
	if _freeze > 0:
		_freeze -= 1
	if _slow_left > 0.0:
		_slow_left -= dt
		if _slow_left <= 0.0:
			_slow = 1.0
	# tremblement : nouveau tirage toutes les 2 images
	_sh.t = minf(_sh.t + dt, _sh.dur)
	var a: float = _sh.amp * pow(1.0 - _sh.t / maxf(_sh.dur, 0.001), 2.0)
	if Engine.get_physics_frames() % 2 == 0:
		var r := Vector2(randf_range(-1, 1), randf_range(-1, 1))
		if _sh.dir != Vector2.ZERO:
			r = _sh.dir.rotated(randf_range(-0.35, 0.35)) * randf_range(-1, 1)
		offset = Vector2i((r * a).round()) if a >= 0.5 else Vector2i.ZERO
	_kick *= 0.6
	if _kick.length() < 0.5:
		_kick = Vector2.ZERO
	offset += Vector2i(_kick.round())
	_step_particles(dt)              # les particules bougent même pendant l'arrêt sur image

func haptic(ms: int, amp: float, full_only := false) -> void:
	if haptic_level == 0 or (full_only and haptic_level < 2):
		return
	var now := Time.get_ticks_msec()
	if now - _last_hap < 50:
		return
	_last_hap = now
	Input.vibrate_handheld(ms, amp)
```

### 9.5 Intégration dans `world.gd`

```gdscript
func _physics_process(dt: float) -> void:
	var wdt := Juice.world_dt(dt)
	t_global += dt                       # décor : temps réel
	if wdt == 0.0:
		_update_camera_offset_only(); queue_redraw(); return
	_consume_taps()
	t_life += wdt                        # pièges et replays : temps du monde (déterministe)
	_step_player(wdt)
	...

# remplacer chaque Sfx.play/_burst/Game.vibrate du gameplay par un seul appel :
Juice.fire(&"wall_land", pos + Vector2(s * 5, 0), {dir = Vector2(s, 0), speed = absf(vel.x)})
```

Signaux à émettre pour la détection : `near_miss(trap)`, `elan_changed(tier)`, `record_broken()`,
`tide_level_changed(level)`, `echo_relived(i)`. Le frôlement se calcule dans `_check_hits()` : distance minimale
entre la hurtbox et la zone mortelle, mémorisée par piège ; à la sortie de la zone de 4 px sans contact, `fire(&"near_miss")`.

### 9.6 Ordre d'intégration conseillé

1. Contrôles (2.1 à 2.6) et caméra (5). **Faire tester avant tout effet.**
2. `juice.gd` + `fx_layer.gd`, migration des effets existants vers `fire()`.
3. Séquence mort → gravure (4.1) : c'est le moment signature.
4. Sons (3.5) et vibrations (3.6).
5. Élan (6) puis musique adaptative (7).
6. Options et budgets (8), passe de réglage sur 3 téléphones (bas, moyen, haut de gamme).

### 9.7 Tests d'acceptation

- [ ] Un tap à ≤ 4 i du mur produit un **rebond**, jamais un demi-tour (100 essais, 0 erreur).
- [ ] Délai tap → première image du saut ≤ 1 image physique + latence d'affichage (mesuré à la caméra 240 i/s : < 70 ms sur un téléphone moyen).
- [ ] Un rebond complet dure 31 i, apex à 61 ± 1 px (test automatique sur la physique).
- [ ] Aucun sprite ni caméra à une position non entière (assertion en debug).
- [ ] Aucun piège ne tue quand seule l'écharpe ou la capuche le touche (captures image par image).
- [ ] Jamais plus de 96 particules, 3 flashs par seconde, 4 vibrations par seconde (compteurs en debug).
- [ ] Les replays d'écho restent identiques avec et sans arrêts sur image (comparaison des enregistrements).
- [ ] En mode « Minimum », aucun décalage de caméra n'est jamais non nul.

---

## 10. Sources

- Steve Swink, *Game Feel* (2008) : définition « contrôle en temps réel d'objets virtuels dans un espace simulé, avec
  des interactions soulignées par le polish » ([Wikipedia : Game feel](https://en.wikipedia.org/wiki/Game_feel),
  [Liz England, critique du livre](https://lizengland.com/blog/review-game-feel-by-steve-swink/)).
- Persona Milo Hartmann : `game_feel_engine` (Swink : input, response, context, polish, timing, weight ; règle « ne pas
  confondre polish et correction d'un mauvais système »), `game_ui_feedback_engine` (boucle input → réponse → feedback →
  interprétation), `game_ui_attention_engine`, `design_principles.feedback` (boucles positives et effet boule de neige).
  Les bases `source_knowledge_base` et `source_knowledge_book` ne contiennent **rien** sur juice, screen shake, hitstop ou
  squash (recherche faite) : les valeurs viennent des sources ci-dessous.
- Méthode pixel art du commanditaire, partie E : 12 principes, cadence 60 Hz, tenues, pop d'apparition 40-60 % → 110-120 %,
  éclats en 6 états, flash 2 images (≈ 33 ms), hitstop 50 ms (petit) à 100-150 ms (lourd), effacement par morceaux.
- Celeste, code source du joueur publié par Noel Berry ([NoelFB/Celeste, Player.cs](https://github.com/NoelFB/Celeste)) :
  `JumpGraceTime = 0.1`, `HalfGravThreshold = 40`, `Gravity = 900`, `MaxFall = 160`, `WallJumpCheckDist = 3`,
  `WallSlideStartMax = 20` / `WallSlideTime = 1.2`, `Celeste.Freeze(.05f)` et `(.1f)`, étirement au saut `(.6, 1.4)`,
  écrasement à l'atterrissage jusqu'à `(1.6, .4)` selon la vitesse, retour à 1 à 1,75/s.
  Fil de Maddy Thorson sur les aides cachées (mars 2020) : [GameSpot](https://www.gamespot.com/articles/celeste-dev-explains-how-they-made-their-game-feel/1100-6474775/),
  [Gigazine](https://gigazine.net/gsc_news/en/20200317-celeste-action-feel-things), [Thread Reader](https://threadreaderapp.com/thread/1238338574220546049.html).
  Le buffer de saut de Celeste (0,08 s) vient de `Input.cs`, que je n'ai pas pu relire ici : valeur à considérer comme non vérifiée.
- Jan Willem Nijman (Vlambeer), *The Art of Screenshake* (2013) : 30 petits ajouts sur un jeu de tir terne ; recul de
  caméra et tremblement additionnés au tir dans Nuclear Throne ([Game Developer](https://gamedeveloper.com/design/vlambeer-co-founder-shares-advice-on-building-better-action-games),
  [recréation de DK Liao](https://dkliao.itch.io/the-art-of-screenshake-recreation/devlog/451576/quick-breakdown-of-all-the-effects)).
- Martin Jonasson et Petri Purho, *Juice It or Lose It* (GDC Europe 2012) : un casse-briques auquel on ajoute
  interpolations, écrasement-étirement, couleur, tremblement, particules et son ([GDC Vault](https://gdcvault.com/play/1016487/Juice-It-or-Lose)).
- Downwell (Ojiro Fumoto) : combo à rythme et retour tactile cités comme modèle ; étudié comme cas de « juiciness »
  ([Game Developer](https://gamedeveloper.com/design/elegance-not-simplicity-devs-weigh-in-on-i-downwell-s-i-irresistible-charm),
  [Wikipedia](https://en.wikipedia.org/wiki/Downwell_(video_game))). Aucune valeur chiffrée publique trouvée.
- Android : [Haptics design principles](https://developer.android.com/develop/ui/views/haptics/haptics-principles)
  (clic de 10 à 20 ms, actionneur qui sonne encore 20 à 50 ms, « buzzy » à éviter, force selon l'importance),
  [Custom haptic effects](https://developer.android.com/develop/ui/views/haptics/custom-haptic-effects) (écarts ≥ 50 ms,
  rapport d'intensité ≥ 1,4).
- Godot : `Input.vibrate_handheld(duration_ms, amplitude)`, amplitude ramenée à 1-255 sur Android, permission `VIBRATE`
  ([doc 4.3](https://docs.godotengine.org/en/4.3/classes/class_input.html)).
- Musique adaptative : couches verticales et reséquençage horizontal, transitions à la mesure, fondus en courbe
  ([Wikipedia : Adaptive music](https://en.wikipedia.org/wiki/Adaptive_music), [Bugnet](https://bugnet.io/blog/adaptive-music-a-beginners-guide)).
- Banques libres : [Kenney et autres, guide 2026](https://app.cinevva.com/guides/free-sound-effects-music),
  [OpenGameArt CC0](https://opengameart.org/content/cc0-bgm).
- Non consultables depuis cet environnement (réseau) : maddymakesgames.com, infovore.org, docs.godotengine.org (4.5).
  Les signatures Godot ont été vérifiées sur la doc 4.3 ; `AudioStreamSynchronized` et `AudioStreamInteractive` (4.3+)
  et l'import QOA sont à confirmer en 4.5.1 par le programmeur.
