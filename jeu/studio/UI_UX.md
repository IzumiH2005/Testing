# ÉCHO — Interface et expérience joueur (UI_UX v1)

> Document de conception UI/UX. Il complète `ART_BIBLE.md` (le style), `FEEL.md` (le ressenti), `GDD.md` (les règles) et `ECONOMY.md` (les chiffres).
> **En cas de conflit**, ce document fait foi pour la **mise en page, les textes et les états**. L'ART_BIBLE fait foi pour le **dessin**. FEEL fait foi pour les **durées des effets en jeu**.
> Toutes les cotes sont en **pixels logiques** (1 px = 1 pixel de la texture du jeu avant agrandissement entier). Les couleurs sont des **lettres de `palette_v2.txt`**.
> Les maquettes sont dans `studio/ui_mockups/` (180×400, à l'échelle 1, avec une copie ×4 pour la lecture).

---

## 0. Les décisions en un coup d'œil

| # | Décision | Raison |
|---|---|---|
| D1 | Écran de référence **180×400**, conçu pour **180 de large** et **320 à 422 de haut** | L'ART_BIBLE (base 180×320, `aspect=expand`, ×6 sur 1080×2400) fait foi ; le 192×352 du brief et de `project.godot` est périmé (arbitrage A1). |
| D2 | **Tout ce qui se touche vit dans les 60 % bas de l'écran.** Le haut est réservé à la lecture. | En portrait, d'une main, le pouce atteint le bas sans réajuster la prise. |
| D3 | Le HUD tient en **une bande haute de 20 px** et **deux colonnes de 14 px dans les murs**. Rien dans le puits, sauf un « bandeau bas » sous le héros. | Le puits est l'espace de jeu. Ce qui est sous le héros est déjà franchi, donc on peut y écrire. |
| D4 | Les infos de HUD sont **contextuelles** : Rythme, volte, marée et bonus n'apparaissent que lorsqu'ils servent. | Concilier « rien d'autre en partie » (ART_BIBLE) et « HUD riche » (brief). |
| D5 | Le **premier lancement n'a aucun texte** jusqu'à la fin de l'Ascension 0. Langue automatique, consentement pub reporté après l'Ascension 0. | Les 60 premières secondes servent à grimper, pas à lire. Aucune pub n'est demandée avant le consentement, donc c'est conforme. |
| D6 | Un bouton agit **au relâchement**, jamais à l'appui. Un glisser de plus de 6 px annule. | Évite les achats et les abandons accidentels pendant un défilement (FEEL §boutons). |
| D7 | Sur l'écran de fin d'ascension, **REJOUER est actif à 300 ms** et un tap ailleurs **accélère** le comptage. | « Une raison de rejouer en 1 s » : on ne fait jamais attendre la relance. |
| D8 | Les pubs sont toujours un **bouton cyan d'écho, plus petit que l'action principale**, avec la récompense écrite dessus. Sans minuteur. Absentes si aucune vidéo n'est chargée. | Garde-fous 1 à 5 d'ECONOMY : le choix doit être libre et lisible. |
| D9 | La fin d'ascension montre **une seule** information de progression, **la plus proche**. | ECONOMY §5 : une seule cible, sinon aucune ne compte. |
| D10 | Le danger dans l'UI se lit par **forme + mouvement + couleur** (croix, tremblement, `z`). La couleur seule ne porte jamais un sens. | Accessibilité daltonisme (Material : « never color alone »). |
| D11 | Quatre polices : **5 px** (chiffres, badges), **7 px** (capitales d'interface), **8 px** (texte courant en casse mixte), **grande** 10×16 (titres, altitude). | Le 5×7 en capitales ne suffit pas aux phrases longues (codex, confidentialité). |
| D12 | Le combo s'appelle **Rythme** (paliers 10/20/30, GDD). **Élan** reste le saut long, doigt tenu. | Un mot = un concept. FEEL utilise « Élan » pour le combo : à corriger (arbitrage A2). |

---

## 1. Écran, grille et zones sûres

### 1.1 Résolution et agrandissement

Réglages Godot 4.5 (`project.godot`) :

```
display/window/size/viewport_width = 180
display/window/size/viewport_height = 320
display/window/stretch/mode = "viewport"
display/window/stretch/aspect = "expand"
display/window/stretch/scale_mode = "integer"
rendering/textures/canvas_textures/default_texture_filter = 0   # Nearest
rendering/2d/snap/snap_2d_transforms_to_pixel = true
rendering/2d/snap/snap_2d_vertices_to_pixel = true
display/window/handheld/orientation = 1                          # portrait
```

| Écran physique | Échelle | Écran logique | Remarque |
|---|---|---|---|
| 1080×2400 (cible) | ×6 | **180×400** | Maquettes de référence. |
| 720×1600 | ×4 | 180×400 | Le pire cas pour la taille des cibles (voir §1.4). |
| 1080×1920 | ×6 | 180×320 | Le plus court supporté : tout doit tenir. |
| 1440×3200 | ×8 | 180×400 | — |
| 1170×2532 (iPhone) | ×6 | 195×422 | 15 px de plus, donnés aux murs. |
| 1536×2048 (tablette) | ×6 | 256×341 | Colonne de menu centrée sur 180 px ; HUD ancré aux bords. |

### 1.2 Notations utilisées partout

- `H` = hauteur logique de l'écran (320 à 422 ; 400 sur les maquettes).
- `It` = encart haut **mesuré** (encoche, trou de caméra) = `ceil(safe_area.position.y / échelle)`. Il vaut 0 sur les maquettes et 0 à 16 px en pratique.
- `B` = **bas utile** = `H − max(24, ceil(encart_bas / échelle))`. Il vaut 376 sur les maquettes. Les 24 px sous `B` restent à la barre gestuelle : décor seulement, jamais de cible.
- Une cote « `y 36` » est **ancrée en haut** : on y ajoute `It`.
- Une cote « `y B−40` » est **ancrée en bas** : elle vaut 336 sur les maquettes et 256 sur un écran de 320.
- `x` est toujours compté depuis le bord gauche de la **colonne de 180 px**. Sur un écran plus large, la colonne est centrée (`offset = (largeur − 180) / 2`), sauf pour le HUD, qui est ancré aux bords réels.

Code de calcul, à mettre une seule fois dans `ui_root.gd` (autoload `UIRoot`) :

```gdscript
var scale_i := int(get_window().size.x / 180)          # échelle entière réelle
var sa := DisplayServer.get_display_safe_area()
var It := ceili(float(sa.position.y) / scale_i)
var bot_inset := ceili(float(get_window().size.y - sa.end.y) / scale_i)
var H := int(get_viewport().get_visible_rect().size.y)
var B := H - max(24, bot_inset)
```

### 1.3 Grille

- **Marges** : 8 px à gauche et à droite, soit une zone de contenu de 164 px (x 8 → 171).
- **Pas vertical** : 4 px. Toutes les hauteurs et tous les écarts sont des multiples de 4, sauf les textes (lignes de 10 et 12 px).
- **Écart entre deux cibles** : au moins 4 px, soit au moins 8 dp dans le pire cas (§1.4).
- **Hauteurs** des éléments :

| Élément | Hauteur |
|---|---|
| Bouton principal | 32 px |
| Bouton standard | 24 px |
| Bouton icône | 28×28 |
| Onglet | 20 px (cible étendue à 24 par 2 px invisibles en haut et en bas) |
| Ligne de liste | 28 px |
| Carte de boutique | 48×56 |

### 1.4 Taille des cibles (48 dp) en pixels logiques

| Appareil | Densité | 48 dp en px physiques | Échelle | **48 dp en px logiques** |
|---|---|---|---|---|
| 1080×2400, 420 dpi | 2,625 | 126 | ×6 | 21 |
| 1080×2400, 480 dpi | 3,0 | 144 | ×6 | 24 |
| 720×1600, 320 dpi | 2,0 | 96 | ×4 | **24** (pire cas) |
| 1440×3200, 560 dpi | 3,5 | 168 | ×8 | 21 |

**Règle : toute cible fait au moins 24×24 px logiques.** Une icône visible plus petite (12 ou 16 px) reçoit une zone de toucher invisible de 24×24 (ou plus) centrée sur elle, par un `Control` parent de `custom_minimum_size = Vector2(24, 24)`.
Raison : 24 px valent 48 dp dans le pire cas et 55 dp sur la cible 1080p.

### 1.5 Carte des zones en partie (180×400, `It = 0`)

```
 x: 0      18                                    162    180
y 0 ┌──────────────────────── HUD 20 px ────────────────────┐  bande haute : lecture seule (sauf pause)
y20 ├──────┬─────────────────────────────────────────┬──────┤
    │ MUR  │                                         │ MUR  │  ← y 20-40 : un tap n'est PAS un bond
y40 │ col. │          PUITS 144 px                   │ col. │
    │ G    │   (aucun élément d'UI, jamais)          │ D    │
    │ 14px │                                         │ 14px │  colonnes de mur : volte, bonus (G) ;
    │      │   zone sacrée : 64 px au-dessus         │      │  Rythme (D) ; marée (G, en bas)
y184│      │   ░░░░░ du héros (y 184-248) ░░░░░      │      │
y248│      │            ◆ HÉROS (62 % de H)          │      │
    │      │                                         │      │
y320├──────┤   BANDEAU BAS  x 20-159, y B−56..B−41   ├──────┤  bannières, tutoriel, toasts : un seul à la fois
y376├──────┴─────────────────────────────────────────┴──────┤  B
y400└──────────── barre gestuelle (24 px) ──────────────────┘
```

Raison du bandeau bas : sous le héros, le terrain est déjà franchi. Le texte n'y cache aucun piège à venir.

---

## 2. Flux complet

### 2.1 Diagramme

```
 [Lancement]
     │ 1er lancement ?
     ├── oui ──► SPLASH 900 ms ──► ASCENSION 0 (aucun texte, 60 m faits main)
     │                                  │ mort ──► GRAVURE (ralenti ×0,5) ──► ENTRE DEUX VIES ──┐
     │                                  │◄────────────────────────────────────────────────────┘
     │                                  │ 4e vie perdue ou 60 m atteints
     │                                  ▼
     │                             FIN D'ASCENSION (1re fois : version courte)
     │                                  ▼
     │                             CONSENTEMENT (formulaire UMP de Google, seulement EEE/RU/CH)
     │                                  ▼
     └── non ──► SPLASH 600 ms ──► HUB (titre)
                                    │
     ┌───────────┬────────────┬─────┼───────────┬───────────┬───────────┬──────────┐
     ▼           ▼            ▼     ▼           ▼           ▼           ▼          ▼
  BOUTIQUE    JOURNAL      CODEX  SUCCÈS     NIVEAUX    RÉGLAGES   TOUR DU JOUR  GRIMPER
 (tenues,    (missions,   (fiches)          (la tour   (+ confi-   (fiche du    │
  traînées,   calendrier,                    des        dentialité) jour)       │
  effets)     série)                         niveaux)                 │GRIMPER  │
                                                                      ▼         ▼
                                                         ┌──────── PARTIE (HUD) ◄──── REPRENDRE ──┐
                                                         │  bouton pause, retour, perte de focus ──► PAUSE
                                                         │  mort
                                                         ▼
                                                    GRAVURE (1,9 s, accélérable)
                                                         │ vies restantes > 0 ?
                                         oui ◄───────────┴──────────► non
                                          ▼                            ▼
                                   ENTRE DEUX VIES             OFFRE +1 VIE ? (si éligible §3.7)
                                   (tap = repartir             │ vidéo vue ──► PARTIE (repart de l'altitude max)
                                    de l'autel)                │ non merci / pas de vidéo
                                          │                     ▼
                                          └──► PARTIE     FIN D'ASCENSION ──► REJOUER ──► PARTIE
                                                               │──► ×2 (vidéo) ──► FIN (butin doublé)
                                                               │──► PARTAGER (feuille système)
                                                               └──► MAISON ──► HUB
```

### 2.2 Bouton Retour Android (geste prédictif)

Godot 4.5 : `NOTIFICATION_WM_GO_BACK_REQUEST`, avec `application/config/quit_on_go_back = false`.

| Écran | Retour fait |
|---|---|
| Partie | Ouvre la Pause. |
| Pause | Reprendre, avec le compte à rebours. |
| Gravure | Accélère ×2 ; un 2e appui passe à « Entre deux vies ». |
| Entre deux vies | Rien (on attend un tap). Raison : évite de quitter par erreur. |
| Offre +1 vie | « Non merci ». |
| Fin d'ascension | Hub. |
| Sous-écran du hub | Hub. |
| Fiche ouverte (codex, carte) | Ferme la fiche. |
| Hub | 1er appui : toast « ENCORE UNE FOIS POUR QUITTER » (2 s) ; 2e appui dans les 2 s : quitter. |

### 2.3 Transitions entre écrans (communes)

Tout mouvement se fait **au pixel entier**, **sans fondu alpha**. Les disparitions passent par une trame de Bayer 4×4 (`dither.png`, voir §5.14).

| Transition | Mouvement | Durée | Courbe | Son | Haptique |
|---|---|---|---|---|---|
| Ouvrir un sous-écran depuis le hub | Le nouvel écran entre par la droite. Décalages par image : 180→120→72→40→18→6→0, puis dépassement −2, puis 0. | 300 ms (7 pas de 2 images + 2 images) | ease-out « au pixel » (tableau ci-dessus) | `ui_open` | H1 |
| Revenir au hub | Mouvement miroir vers la droite : 0→6→18→40→72→120→180. | 250 ms | ease-in | `back` | H1 |
| Panneau modal | Il monte de 30 px : décalages 30→18→10→5→2→0, puis dépassement −2, puis 0. Chaque pas tient 3 images (50 ms). | 300 ms | amorti 12/8/5/3/2 (ART_BIBLE) | `ui_open` | H1 |
| Fond d'un modal | Trame `k` à 25 %, puis 50 % (2 pas de 50 ms). | 100 ms | paliers | — | — |
| Fermer un modal | Il descend de 30 px en 4 pas (2, 5, 10, 13 px), puis la trame s'efface. | 200 ms | ease-in | `back` | — |
| Hub → Partie | Barre haute : monte de 28 px. Boutons du bas : descendent de 120 px. La caméra continue sans coupure. | 250 ms | ease-in | `go` | H2 |
| Partie → Fin d'ascension | Trame `k` jusqu'à 50 %, puis entrée du panneau de fin par le bas. | 300 ms | amorti | `ui_open` | — |

Implémentation : un seul `UIK.slide(node, from_offset, steps:Array[int], frames_per_step:int)` qui pilote un `Tween` à pas discrets (`tween_property(...).set_trans(Tween.TRANS_LINEAR)` sur une valeur entière, une étape par pas). **Pas d'interpolation continue** sur une position d'UI.
**En mode Effets minimum**, toute transition devient une trame en 2 pas de 50 ms, sans mouvement.

---

## 3. Écrans

> Format de chaque fiche : **But** (une ligne), **Mise en page** (cotes en px logiques), **Hiérarchie**, **Éléments et états**, **Textes FR / EN**, **Gestes**, **Transitions**, **Sons et haptique**.
> États standard d'un bouton (§5.2) : *normal*, *pressé*, *désactivé*, *nouveau*. Seules les différences sont écrites dans les fiches.

### 3.1 Premier lancement (sans texte)

**But :** faire grimper le joueur en moins de 3 s après l'icône, sans un mot à lire.

**Séquence**

| t | Ce qui se passe | Détail |
|---|---|---|
| 0 | Écran de démarrage Godot | `k` uni, `icon.png` 32×32 centré (x 74, y `H/2 − 16`). Réglage `boot_splash/bg_color = #0e0a1a`, `boot_splash/image = splash.png` (180×400). |
| ≈ 600 ms | Splash | Logo 160×48 à x 10, y `H/2 − 60`. Le double en écho se détache (6 images, 300 ms). Langue choisie silencieusement : `OS.get_locale_language() == "fr"` → FR, sinon EN. |
| 900 ms | Fondu tramé | Le logo s'efface en trame, 4 pas de 50 ms. La caméra est déjà au pied de la tour. **Aucun bouton « jouer »** : le héros attend accroché au mur. |
| 900 ms + | Invite du premier bond | Main `tap.png` 32×32 × 2 images (400 ms par image) posée **sur le mur** à côté du héros, à x 18, y = y_héros − 8. Bandeau tutoriel (§5.13) au bas : pictogramme `tuto16` « tap » 16×16, pas de texte. |
| 1er tap | Le héros bondit | La main disparaît (2 images). La caméra suit. Le jeu commence. |

**Pictogrammes contextuels** (GDD §onboarding). Chaque pictogramme s'affiche **dans le bandeau bas**, en 16×16, couleur `w`, sur `panel` 64×24 :

| Mètre | Pictogramme | Disparaît quand |
|---|---|---|
| 0 | tap (bond) | 1er bond |
| ≈ 12 | doigt tenu + flèche longue (Élan) | 1er Élan réussi, ou 3 essais |
| ≈ 22 | tap en l'air (Volte) | 1re volte |
| ≈ 40 | mur + flèche bas (Glisse) | 1re glisse de 0,5 s |
| à la 1re mort | aucun : la gravure se montre seule, au ralenti ×0,5 | — |

Un pictogramme reste au plus 6 s, puis revient (2 pulsations) après 3 s d'inaction. Il ne bloque jamais le jeu : pas de pause.

**Consentement pub.** Le formulaire UMP (Google User Messaging Platform) est **natif et en texte**. On l'appelle **après** l'écran de fin de l'Ascension 0, au premier passage vers le hub, et seulement si `ConsentInformation.getConsentStatus() == REQUIRED`. Avant, `requestConsentInfoUpdate` tourne en tâche de fond, et **aucune pub n'est chargée**.
Raison : l'Ascension 0 ne propose aucune pub (`extra_life` exige ≥ 30 m hors tutoriel), donc reporter le formulaire ne prive de rien et garde la première minute sans texte.

**Sons et haptique.** Splash : `logo_echo` (300 ms, doux). Premier bond : son du jeu, H1. Aucun son d'interface.

---

### 3.2 Hub (écran-titre)

**But :** relancer une ascension en 1 tap et montrer la prochaine chose à gagner.

**Mise en page** (180×400 ; voir `ui_mockups/hub.png`)

| Élément | x | y | l × h | Ancrage |
|---|---|---|---|---|
| Fond : scène-titre (héros au pied de la tour, marée en bas, plans P0-P4) | 0 | 0 | 180×H | plein |
| Zone Niveau (cible) | 4 | 4 | 64×24 | haut |
| ↳ badge de niveau `xp_badge` | 6 | 6 | 20×20 | — |
| ↳ « NIV 12 » (`font_5`, `w`) | 30 | 8 | — | — |
| ↳ barre XP `bar` (remplissage `j`) | 30 | 18 | 36×4 | — |
| Zone Monnaies (cible) | 104 | 4 | 72×24 | haut |
| ↳ éclats : nombre `font_7` `G` aligné à droite sur x 159, icône `shard` 12×12 | 164 | 6 | — | — |
| ↳ prismes : nombre `font_5` `e` aligné à droite sur x 159, icône `prism` | 164 | 18 | 12×8 visibles | — |
| Logo | 10 | 36 | 160×48 | haut |
| « RECORD 612 M » (`font_7` ; « RECORD » en `l`, chiffres en `G`) | centré | 90 | — | haut |
| Série : flamme 12×12 + « SÉRIE 5 J » (`font_7`, `a`) | centré | 102 | — | haut |
| **Carte Prochain objectif** (§5.10) | 8 | B−144 | 164×28 | bas |
| Rangée d'icônes : 5 boutons 28×28, icône 16×16 | 8, 42, 76, 110, 144 | B−108 | 28×28 | bas |
| Bouton **TOUR DU JOUR** (`btn_alt`, icône calendrier) | 24 | B−72 | 132×24 | bas |
| Bouton **GRIMPER** (`btn_main`, icône ▶) | 24 | B−40 | 132×32 | bas |

Rangée d'icônes, de gauche à droite : **Boutique** (écharpe), **Journal** (parchemin), **Codex** (livre), **Succès** (trophée), **Réglages** (engrenage).
Raison de l'ordre : les plus utilisés (boutique, missions) sont près du pouce droit **et** gauche. Les réglages sont au bord.

Vérification sur 320 de haut (`B = 296`) : carte objectif y 152-179, et la série finit à y 111. Il reste 41 px libres : ça tient.

**Hiérarchie** : 1. GRIMPER → 2. Prochain objectif → 3. Tour du jour → 4. icônes → 5. monnaies et niveau → 6. logo et record.

**États**

| Élément | État | Rendu |
|---|---|---|
| GRIMPER | normal | `btn_main` ; libellé `font_7` `k` ; pulse « respire » de 1 px vers le haut toutes les 2 s (désactivé en Effets réduits) |
| GRIMPER | 1er lancement du jour | Badge `badge_new` (7×7) à x 151, y B−42 |
| TOUR DU JOUR | non joué | `btn_alt` ; libellé « TOUR DU JOUR #312 » ; badge nouveau |
| TOUR DU JOUR | joué | Icône coche `check` ; libellé « TOUR #312 · 612 M » ; pas de badge |
| TOUR DU JOUR | verrouillé (avant la 1re ascension complète) | Bouton masqué, pas grisé. Raison : rien à expliquer pendant le tutoriel. |
| Icône (5) | nouveau | `badge_new` en x+21, y−2 (déborde de 2 px) quand il y a du nouveau : tenue abordable, mission finie à encaisser, fiche de codex débloquée, succès obtenu. Jamais pour une pub. |
| Icône | verrouillée | Le Journal est verrouillé avant le niveau 2 (ECONOMY). Icône `lock` 12×12 par-dessus, `s`. Un tap ouvre le toast « JOURNAL AU NIVEAU 2 ». |
| Prochain objectif | voir §5.10 | — |
| Série | 0 jour | Ligne masquée |
| Série | gel utilisé aujourd'hui | Flamme en `c` (glace) au lieu de `o` |

**Textes**

| Clé | FR | EN |
|---|---|---|
| `hub_play` | GRIMPER | CLIMB |
| `hub_daily` | TOUR DU JOUR #%d | DAILY TOWER #%d |
| `hub_daily_done` | TOUR #%d · %d M | TOWER #%d · %d M |
| `hub_record` | RECORD %d M | BEST %d M |
| `hub_streak` | SÉRIE %d J | STREAK %d D |
| `hub_level` | NIV %d | LV %d |
| `toast_quit` | ENCORE UNE FOIS POUR QUITTER | AGAIN TO QUIT |
| `toast_locked_lvl` | %s AU NIVEAU %d | %s AT LEVEL %d |

**Gestes** : tap sur les cibles. Pas de glisser. Un tap sur le fond ne fait rien. Raison : un tap sur le fond qui lance la partie produit des départs involontaires.

**Transitions** : à l'arrivée depuis la fin d'ascension, le logo arrive par trame (4 pas de 50 ms), les boutons du bas montent de 30 px (amorti 12/8/5/3/2), la barre haute descend de 12 px. Total 300 ms. Le compteur d'éclats roule s'il a changé (§5.8).

**Sons et haptique** : musique du titre en boucle. Boutons : `click` + H1 au relâchement. GRIMPER : `go` + H2.

---

### 3.3 Partie (HUD)

Spécification complète au §4. Résumé : bande haute de 20 px, colonnes de mur de 14 px, bandeau bas sous le héros, rien dans le puits.

---

### 3.4 Mort et gravure

**But :** montrer que la mort sert (le piège est gravé) en moins de 2 s, puis rendre la main.

**Séquence** (FEEL §gravure, inchangée ; seul l'habillage UI est ajouté ici)

| t (ms) | Jeu (FEEL) | UI (ce document) |
|---|---|---|
| 0 | Hitstop 100 ms, H3 | La lanterne de la vie perdue joue son extinction : `ui_lantern` images 2→3, 2 × 83 ms. |
| 520 | Panoramique 350 ms vers le piège | — |
| 870 | Bandes noires 8 px en haut et en bas | Les bandes `k` recouvrent le HUD. Raison : le spectacle prime, le HUD est inutile 1 s. |
| 1020 | Tampon « GRAVÉ » | `stamp_frame` 64×24 × 5 images (pop : 50 % → 115 % → écrasé → final, 5 × 50 ms), centré sur le piège. Texte `font_l_outline`, `c` : « GRAVÉ » / « ETCHED ». |
| 1920 | — | Le panneau **Vie perdue** monte (§3.5). |

Un tap pendant la séquence la passe en ×2 (la gravure dure alors 960 ms). La séquence n'est jamais sautée pendant les 3 premières morts de la vie du joueur (FEEL).
**Effets minimum** : pas de panoramique ni de tampon animé. Le tampon s'affiche tel quel 600 ms.

---

### 3.5 Entre deux vies (« Vie perdue »)

**But :** dire ce qui a été gagné par cette mort et repartir d'un tap.

**Mise en page** : `panel_echo` 164×88 à x 8, y B−124 → B−37 (bas de l'écran, sous le héros).

| Élément | x | y (rel. panneau) | Style |
|---|---|---|---|
| Titre « VIE PERDUE » | centré | 8 | `font_7`, `c` |
| Altitude de cette vie « 218 M » | centré | 20 | `font_l`, `w` |
| Ligne gravure : icône du piège 12×12 + « SCIE GRAVÉE » + « +2 » + éclat 12×12 | 12 | 40 | `font_7`, `e` ; +2 en `G` |
| Lanternes restantes (4 × 12×12, pas 13 px) | 64 | 54 | allumée / éteinte |
| Invite « TOUCHE POUR REPRENDRE » | centré | 70 | `font_7`, `l`, clignote 1 Hz (600 ms allumé / 400 ms éteint) |

En dessous du panneau, hors du panneau, à y B−32 : « DEPUIS L'AUTEL 150 M » (`font_5`, `l`).

**Variantes de la ligne gravure** :
- Plusieurs pièges gravés : « 2 PIÈGES GRAVÉS ».
- Mort sans gravure (chute dans la marée) : « LA MARÉE T'A REPRIS », en `j`.

**Quasi-réussite** : si l'altitude de cette vie est à 10 % ou moins du record, une ligne s'ajoute à y 30 du panneau, en `font_8` `a` : « Record à 12 m ! ». Le panneau grandit alors de 12 px.

**États** : l'invite n'est **active qu'à +400 ms**. Avant, un tap est ignoré.
Raison : le joueur tapait pour grimper au moment de la mort. Sans ce délai, ce tap relancerait sans qu'il ait lu.

**Gestes** : un tap n'importe où (sauf la pause) fait repartir.
- Le héros réapparaît à l'autel le plus haut, avec 1 s d'invulnérabilité clignotante.
- Le panneau descend de 30 px en 200 ms.
- Le HUD réapparaît par trame en 100 ms.

**Sons et haptique** :
- entrée du panneau : `ui_open`, sans haptique (H3 vient d'être joué) ;
- tap pour repartir : `go` + H2 ;
- dernière vie restante : la dernière lanterne clignote `z` 3 fois et joue `warn`, avec forme + couleur.

| Clé | FR | EN |
|---|---|---|
| `life_lost` | VIE PERDUE | LIFE LOST |
| `engraved_one` | %s GRAVÉE / %s GRAVÉ | %s ETCHED |
| `engraved_n` | %d PIÈGES GRAVÉS | %d TRAPS ETCHED |
| `tide_took` | LA MARÉE T'A REPRIS | THE TIDE TOOK YOU |
| `tap_resume` | TOUCHE POUR REPRENDRE | TAP TO GO ON |
| `from_altar` | DEPUIS L'AUTEL %d M | FROM ALTAR %d M |
| `near_record_life` | Record à %d m ! | %d m from your best! |

Le genre FR du nom du piège (SCIE → GRAVÉE, PENDULE → GRAVÉ) est porté par la fiche du piège : champ `fem: bool`.

---

### 3.6 Pause

**But :** s'arrêter sans perdre sa partie, régler le son, et ne pas abandonner par erreur.

**Déclencheurs** :
- bouton pause du HUD ;
- Retour Android ;
- perte de focus de l'application (`NOTIFICATION_APPLICATION_FOCUS_OUT`) ;
- appel entrant.

Raison : sur mobile, une interruption sans pause automatique coûte une vie, ce que le joueur vit comme injuste.

**Mise en page** : fond tramé `k` à 50 % sur le jeu figé. `panel` 148×176 à x 16, y B−185 → B−9.

| Élément | x (rel.) | y (rel.) | l × h | Style |
|---|---|---|---|---|
| « PAUSE » | centré | 8 | — | `font_7`, `l` |
| Altitude actuelle « 412 M » | centré | 20 | — | `font_l`, `w` |
| Missions en cours : 3 lignes | 10 | 40 | 128×30 | `font_5` `l`, chiffres `w` ; mission finie = coche `check` |
| 4 bascules 28×28 : son, musique, vibrations, effets | 10, 44, 78, 112 (écart 6) | 76 | 28×28 | `btn_alt`, icône 16×16 ; désactivé = icône barrée `s` |
| **REPRENDRE** (`btn_main`) | 10 | 108 | 128×32 | — |
| **ABANDONNER** (`btn_alt`) | 10 | 144 | 128×24 | — |

Le panneau fait 176 px de haut (dernier bouton à y 144 + 24 px + 8 px de marge). Sur 320, il occupe y 111 → 287 : ça tient.

**Abandon en 2 temps, sans modal** :
- 1er tap : le libellé devient « SÛR ? TOUCHE ENCORE », le bouton passe en `panel_echo` et tremble ±1 px 2 fois.
- 2e tap dans les 3 s : fin d'ascension (la meilleure vie compte).
- Après 3 s, le libellé revient.

Raison : une confirmation sur place coûte 0 écran, et l'erreur demande deux gestes délibérés.

**Reprendre** : compte à rebours 3-2-1 de 400 ms chacun.
- Chiffres `countdown.png` 24×32, centrés à y `0,45 × H`.
- Sons `tick`, puis `go` sur 1. H1 à chaque chiffre.
- Le jeu reprend à la fin du « 1 ».
- En Effets minimum : chiffres sans pop, même durée.

**Gestes** : Retour = Reprendre. Un tap hors du panneau ne fait rien. Raison : un tap réflexe ne doit pas relancer le jeu.

| Clé | FR | EN |
|---|---|---|
| `pause` | PAUSE | PAUSE |
| `resume` | REPRENDRE | RESUME |
| `give_up` | ABANDONNER | GIVE UP |
| `give_up_sure` | SÛR ? TOUCHE ENCORE | SURE? TAP AGAIN |

---

### 3.7 Offre « +1 vie » (`extra_life`)

**But :** proposer une seconde chance comme un **choix libre**, une seule fois, sans pression.

**Conditions d'affichage** (toutes requises) :
- 4e vie perdue ;
- altitude max ≥ 30 m ;
- pas déjà proposée dans cette ascension ;
- mode Ascension libre (jamais en Tour du jour ni en Défi) ;
- vidéo **déjà chargée** ;
- moins de 2 refus **consécutifs** (au 2e refus, l'offre se cache pour 5 ascensions) ;
- consentement UMP obtenu ou non requis.

Sinon : on passe directement à la fin d'ascension, sans écran vide.

**Mise en page** : `panel_echo` 164×124 à x 8, y B−132 → B−9. Le fond est le jeu figé, sous une trame à 50 %.

| Élément | x (rel.) | y (rel.) | l × h | Style |
|---|---|---|---|---|
| Lanterne `ui_lantern` en écho (image 3) | 76 | 8 | 12×12 | — |
| « UNE LANTERNE DE PLUS ? » | centré | 24 | — | `font_7`, `c` |
| « Regarde une vidéo pour repartir de 812 m. » (2 lignes) | 8 | 38 | 148×24 | `font_8`, `w` |
| **▶ +1 VIE** (`btn_echo`, icône vidéo 16×16) | 8 | 66 | 148×24 | texte `k` sur face `c` |
| **NON MERCI** (`btn_alt`) | 8 | 94 | 148×24 | texte `w` |

**Règles éthiques visibles** :
- Les deux boutons ont **la même taille**. Le refus est **au plus près du pouce** (en bas).
- **Pas de compte à rebours**, pas d'animation pressante, pas de son en boucle.
- La récompense (« +1 VIE », « repartir de 812 m ») est écrite **avant** de voir la vidéo.

Raison : un refus aussi facile que l'acceptation garde la confiance, et la confiance garde le joueur (garde-fous ECONOMY 1-4).

**Après la vidéo** :
- Récompense obtenue : toast « +1 VIE », lanterne rallumée (images 3→0 en 4 × 83 ms), `buy` + H3, puis on repart de l'altitude max.
- Vidéo fermée trop tôt : toast « VIDÉO INTERROMPUE · PAS DE VIE », puis fin d'ascension. L'offre ne revient pas.
- Erreur de chargement : toast « PAS DE VIDÉO DISPONIBLE », puis fin d'ascension.

| Clé | FR | EN |
|---|---|---|
| `offer_title` | UNE LANTERNE DE PLUS ? | ONE MORE LANTERN? |
| `offer_body` | Regarde une vidéo pour repartir de %d m. | Watch a video to start again at %d m. |
| `offer_yes` | +1 VIE | +1 LIFE |
| `offer_no` | NON MERCI | NO THANKS |
| `ad_cut` | VIDÉO INTERROMPUE · PAS DE VIE | VIDEO STOPPED · NO LIFE |
| `ad_none` | PAS DE VIDÉO DISPONIBLE | NO VIDEO AVAILABLE |

---

### 3.8 Fin d'ascension (récapitulatif)

**But :** montrer le résultat en 600 ms, donner une raison précise de rejouer, et laisser rejouer en moins de 1 s.

**Mise en page** (180×400 ; voir `ui_mockups/fin.png`). Fond : jeu figé sous une trame à 50 %, puis `panel` plein écran 172×(B−4) à x 4, y 4.

| Élément | x | y | l × h | Style |
|---|---|---|---|---|
| Titre « ASCENSION TERMINÉE » (en Tour du jour : « TOUR #312 ») | centré | 10 | — | `font_7`, `l` |
| **Altitude** « 812 M » (comptée) | centré | 22 | ≤ 60×16 | `font_l`, `w` |
| Étiquette record : « NOUVEAU RECORD ! » (`G`, pop) ou « RECORD 840 M » (`l`) | centré | 42 | — | `font_7` |
| Barres des 4 vies : lanterne 12×12 + barre `bar` 128×6 + mètres `font_5` | 8 / 24 / 155 | 56, 68, 80, 92 | 164×12 chaque | barre `c` = vie ; trait 1 px `G` = record ; points `e` = gravures |
| **Quasi-réussite** (une ligne, §8.3) | centré | 108 | — | `font_8`, `a` |
| Bloc butin : `panel_inset` | 8 | 122 | 164×48 | — |
| ↳ « ÉCLATS » + nombre qui roule + icône | 8 / 156 (droite) | +6 | — | `font_7` `l` ; nombre `G` |
| ↳ « XP » + barre de niveau 96×4 + « NIV 12 » | 8 / 40 / 140 | +20 | — | barre `j` ; libellé `font_5` |
| ↳ « GRAVURES 3 » + « +6 » | 8 / 156 | +34 | — | `font_7` `e` ; `G` |
| **Prochain objectif** (§5.10) | 8 | 178 | 164×28 | — |
| **×2 ▶** (`btn_echo`) | 8 | B−104 | 78×24 | butin ≥ 15 seulement, une fois |
| **PARTAGER** (`btn_alt`, icône partage) | 94 | B−104 | 78×24 | — |
| **MAISON** (`btn_alt`, icône 16×16) | 8 | B−72 | 32×32 | — |
| **REJOUER** (`btn_main`, icône rejouer) | 48 | B−72 | 124×32 | — |

Remarque : B−72 + 32 = B−40. Les 40 px libres sous REJOUER sont voulus : sur 320 de haut, le bloc remonte de 80 px sans chevauchement (butin y 122-169, ×2 à y 192, et la carte objectif passe sous le butin à y 174, réduite à 16 px de haut).

**Chronologie** (une tape n'importe où, hors bouton, = tout finir tout de suite)

| t (ms) | Action | Son | Haptique |
|---|---|---|---|
| 0 | Le panneau monte (amorti 300 ms) | `ui_open` | — |
| 300 | **REJOUER et MAISON deviennent actifs** | — | — |
| 300-900 | L'altitude compte de 0 à 812, en ease-out quartique | `tick` tous les 10 m (au plus 12/s) | — |
| 900 | Record : bannière « NOUVEAU RECORD ! » pop (4 images de 50 ms), cadre 2 px `G` sur le panneau pendant 2 images, `ui_confetti` | `record` | H3 |
| 900-1500 | Barres des vies : remplissage de gauche à droite, 150 ms par barre, décalé de 150 ms | `tick` doux | — |
| 1500-1900 | Éclats : compteur qui roule ; 8 à 12 éclats volent vers le compteur du hub (`coin_fly`, départs décalés de 40 ms) | `coin` × n (hauteur montante) | H1 au dernier |
| 1900-2300 | XP : la barre se remplit. Si niveau gagné : pop du badge, « NIVEAU 13 ! » en `G` | `levelup` | H3 |
| 2300 | Quasi-réussite et prochain objectif apparaissent par trame (100 ms) | — | — |
| 2400 | Si une mission s'est finie : toast « MISSION FINIE · +40 » (au plus 1 toast ; les autres sont fusionnés : « 2 MISSIONS FINIES · +65 ») | `mission` | H2 |

- Durée totale : **2,4 s**, réduite à 0 par un tap.
- **REJOUER** à t ≥ 300 ms : la relance applique tous les gains d'un coup, sans animation, puis enchaîne la transition Fin → Partie (250 ms).
- Le premier passage (Ascension 0) dure 1,5 s : pas de barres de vies ni de butin détaillé, seulement altitude + éclats + « GRIMPER ».

**×2 ▶ (`double_loot`)** :
- Visible si butin ≥ 15 éclats, si une vidéo est chargée et si le consentement est réglé.
- Après la vidéo : le nombre d'éclats recompte du total au double en 400 ms. Le bouton devient « DOUBLÉ ✓ » désactivé.
- Raison de sa taille (78 contre 124 px) : il est secondaire face à REJOUER (garde-fou 2).

**PARTAGER** : texte et image (§3.14). En Ascension libre, le texte est « ÉCHO — 812 m », sans grille.

| Clé | FR | EN |
|---|---|---|
| `end_title` | ASCENSION TERMINÉE | CLIMB OVER |
| `end_record_new` | NOUVEAU RECORD ! | NEW BEST! |
| `end_record` | RECORD %d M | BEST %d M |
| `end_shards` | ÉCLATS | SHARDS |
| `end_xp` | XP | XP |
| `end_graves` | GRAVURES %d | ETCHED %d |
| `end_double` | ×2 | ×2 |
| `end_doubled` | DOUBLÉ | DOUBLED |
| `end_share` | PARTAGER | SHARE |
| `end_replay` | REJOUER | CLIMB AGAIN |
| `end_level_up` | NIVEAU %d ! | LEVEL %d! |
| `toast_mission` | MISSION FINIE · +%d | MISSION DONE · +%d |
| `toast_missions` | %d MISSIONS FINIES · +%d | %d MISSIONS DONE · +%d |

---

### 3.9 Boutique (tenues, traînées, effets d'écho)

**But :** voir une tenue sur le héros avant de l'acheter et l'équiper en 2 taps.

**Mise en page**

| Élément | x | y | l × h | Style |
|---|---|---|---|---|
| Retour (icône 16×16, cible 24×24) | 4 | 4 | 24×24 | `btn_alt` |
| Titre « BOUTIQUE » | centré | 11 | — | `font_7`, `l` |
| Éclats et prismes (comme au hub) | 104 | 4 | 72×24 | — |
| **Aperçu** : socle `shop_pedestal` 64×16, héros animé (grimpe en boucle 1,2 s), traînée ou effet d'écho rejoué toutes les 3 s | 0 | 32 | 180×88 | fond `b` |
| Onglets × 3 | 9, 63, 117 | 124 | 54×20 | `tab` |
| Grille 3 colonnes, cartes 48×56, écart 6, pas vertical 62 | 12, 66, 120 | 148 + 62·n | 48×56 | `card` (§5.9) |
| Zone de défilement de la grille | 8 | 148 | 164×(B−44−148) | `ScrollContainer`, vertical seulement |
| **Bouton d'action** | 12 | B−36 | 156×28 | selon l'état (ci-dessous) |

Sur 400 de haut : 3 rangées visibles (9 cartes). Sur 320 : 1,5 rangée, et la demi-carte visible montre qu'on peut défiler.

**Onglets** : TENUES / TRAÎNÉES / ÉCHOS.
- TRAÎNÉES s'ouvre au niveau 3 et ÉCHOS au niveau 10 (ECONOMY).
- Avant cela, l'onglet porte un cadenas et le libellé « NIV 3 ». Un tap ouvre le toast « TRAÎNÉES AU NIVEAU 3 ».

**États d'une carte et bouton d'action correspondant**

| État de la carte | Rendu de la carte | Bouton d'action (après sélection) |
|---|---|---|
| Équipée | Cadre `G` 1 px + coche 12×12 en haut à droite | « PORTÉE » `btn_alt` désactivé |
| Possédée | Normal, pas de prix | « PORTER » `btn_main` |
| Achetable (assez d'éclats) | Prix `font_5` `G` + mini-éclat | « ACHETER · 400 ◆ » `btn_main` |
| Trop chère | Prix en `l` | « IL MANQUE 120 ◆ » `btn_alt` désactivé, plus un toast au tap : « GAGNE-LES EN GRIMPANT ». Jamais de lien vers une pub. Raison : garde-fou 6. |
| Prix en prismes | Prix `font_5` `e` + mini-prisme | « ACHETER · 3 ◇ » |
| Verrouillée par niveau | Silhouette `s`, cadenas, « NIV 25 » | « AU NIVEAU 25 » désactivé |
| Verrouillée par succès | Silhouette, trophée 12×12 | « SUCCÈS : FIDÈLE » désactivé ; un tap ouvre la fiche du succès |
| Essai pub possible (`skin_trial`) | En plus du prix : petit ▶ `c` 6×6 en bas à gauche | Deux boutons côte à côte : « ESSAYER ▶ » `btn_echo` 72×28 et « ACHETER · 400 ◆ » `btn_main` 80×28 |
| En essai | Bandeau « ESSAI 2/3 » `font_5` `c` | « ACHETER · 400 ◆ » |
| Nouvelle | `badge_new` en x+42, y−2 ; le badge disparaît une fois la carte vue 1 s | — |

**Achat** (FEEL) :
- Le compteur d'éclats descend en 400 ms (roulement).
- La carte fait un pop (4 images), `ui_confetti` se joue au-dessus de l'aperçu.
- Son `buy`, H3. La tenue est **équipée automatiquement**.
- Toast « BRAISE EST À TOI » / « BRAISE IS YOURS ».

Raison de l'équipement automatique : on achète pour porter, et cela économise un tap.

**Refus** : tremblement ±2 px, 2 allers-retours en 200 ms, le prix clignote `z` 2 fois, son `deny`, H2 double. Plus le toast « IL MANQUE 120 ◆ ». Le message ne passe donc pas que par la couleur.

**Confirmation** : aucune pour les éclats ; pour un achat en prismes, le bouton passe à « SÛR ? 3 ◇ » au 1er tap.
Raison : les prismes sont rares (ECONOMY : « les prismes prouvent »), donc une erreur coûterait cher.

**Gestes** :
- tap sur une carte : sélection et aperçu immédiat ;
- glisser vertical : défilement (seuil 6 px, après quoi le tap est annulé) ;
- glisser horizontal sur l'aperçu : fait tourner le héros, gauche/droite, en 2 images.

**Sons** : sélection `tab_soft` + H1 ; onglet `tab` + H1.

| Clé | FR | EN |
|---|---|---|
| `shop` | BOUTIQUE | SHOP |
| `tab_outfits` | TENUES | OUTFITS |
| `tab_trails` | TRAÎNÉES | TRAILS |
| `tab_echoes` | ÉCHOS | ECHOES |
| `shop_worn` | PORTÉE | WORN |
| `shop_wear` | PORTER | WEAR |
| `shop_buy` | ACHETER · %d | BUY · %d |
| `shop_missing` | IL MANQUE %d | NEED %d MORE |
| `shop_earn` | GAGNE-LES EN GRIMPANT | EARN THEM BY CLIMBING |
| `shop_at_level` | AU NIVEAU %d | AT LEVEL %d |
| `shop_try` | ESSAYER | TRY |
| `shop_trial` | ESSAI %d/3 | TRIAL %d/3 |
| `shop_yours` | %s EST À TOI | %s IS YOURS |
| `shop_sure` | SÛR ? %d | SURE? %d |

---

### 3.10 Niveaux et récompenses (« La tour des niveaux »)

**But :** voir ce que le prochain niveau ouvre et pourquoi l'XP compte.

**Mise en page**

| Élément | x | y | l × h | Style |
|---|---|---|---|---|
| Retour, titre « NIVEAUX », monnaies | comme la boutique | — | — | — |
| Carte du niveau actuel `panel_inset` | 8 | 32 | 164×40 | — |
| ↳ badge 20×20, « NIVEAU 12 » | 8 / 32 | +10 | — | `font_7` `w` |
| ↳ barre XP 120×6 + « 860 / 540 XP » | 32 / 32 | +22 / +30 | — | barre `j` ; `font_5` `l` |
| Liste verticale (la tour) : une ligne par niveau, 28 px, **du haut (niveau le plus haut) vers le bas** | 8 | 80 → B | 164×28 | — |
| ↳ nœud `level_node` 16×16 sur un fil vertical 2 px `n` (x 15) | 8 | +6 | 16×16 | passé `c`, actuel `G` qui pulse, futur `s` |
| ↳ « 13 » `font_7` | 30 | +9 | — | — |
| ↳ récompense : icône 16×16 + « 95 ◆ » ou « TRAÎNÉES » | 52 | +6 | — | `font_7` |
| ↳ déblocage majeur (niv 2, 3, 5, 8, 10, 12, 15, 25, 50) | — | — | — | Ligne en `panel_echo`, libellé `c`, hauteur 36 |

À l'ouverture, la liste défile pour mettre le niveau actuel à `y = 0,6 × H`. La tour monte, comme dans le jeu.

**Encaissement** : les récompenses de niveau sont **créditées d'office**, à la fin d'ascension, avec le pop du niveau.
Raison : un « réclamer » sur une récompense déjà gagnée est une friction sans valeur.

**Gestes** : glisser vertical. Un tap sur une ligne de déblocage ouvre un toast d'explication (ex. « À 10 : EFFETS D'ÉCHO DANS LA BOUTIQUE »).

| Clé | FR | EN |
|---|---|---|
| `levels` | NIVEAUX | LEVELS |
| `level_n` | NIVEAU %d | LEVEL %d |
| `xp_of` | %d / %d XP | %d / %d XP |
| `unlock_missions` | MISSIONS | MISSIONS |
| `unlock_trails` | TRAÎNÉES | TRAILS |
| `unlock_weekly` | DÉFI DE LA SEMAINE | WEEKLY CHALLENGE |
| `unlock_relic` | RELIQUE | RELIC |
| `unlock_echofx` | EFFETS D'ÉCHO | ECHO EFFECTS |
| `unlock_sanctuary` | SANCTUAIRE | SANCTUARY |
| `unlock_hard` | MISSIONS DIFFICILES | HARD MISSIONS |
| `unlock_crown` | LA COURONNE | THE CROWN |

---

### 3.11 Journal : missions, calendrier, série

**But :** voir les 3 tâches du jour, encaisser ce qui est fini et savoir quand revenir.

**Mise en page**

| Élément | x | y | l × h | Style |
|---|---|---|---|---|
| Retour, titre « JOURNAL », monnaies | — | 4 | — | — |
| **Série** : flamme 16×16 + « SÉRIE 5 JOURS » + gel « GEL PRÊT » (glace 12×12 `c`) | 8 | 32 | 164×24 | `font_7` `a` ; gel `font_5` `c` |
| **Calendrier** : 7 cases `cal_cell` 20×28, écart 3 | 11 + 23·i | 60 | 20×28 | §5.11 |
| Missions × 3 : `panel_inset` | 8 | 96, 142, 188 | 164×40 | — |
| ↳ difficulté : 1 à 3 pastilles 4×4 | +6 | +6 | — | facile `l`, moyenne `a`, difficile `o` + forme (rond, losange, triangle) |
| ↳ texte, 2 lignes au plus | +16 | +4 | 108×24 | `font_8` `w` |
| ↳ barre de progression 108×4 + « 140/300 M » | +16 | +30 | — | barre `G` ; `font_5` `l` |
| ↳ récompense « 40 ◆ 30 XP » | +128 | +6 | — | `font_5` `G` / `j` |
| ↳ **Relance** (niv ≥ 15) : bouton 24×24 `btn_echo`, icône ↻▶ | +136 | +14 | 24×24 | — |
| **Bonus 3/3** : coffre `chest` 32×32 + « 3/3 : 30 ◆ + 1 ◇ » | 8 | 234 | 164×40 | — |
| « NOUVELLES MISSIONS DANS 6 H » | centré | 278 | — | `font_5` `l` |

Total : y 288. Ça tient sur 400 et défile sur 320 (`ScrollContainer`).

**États d'une mission**

| État | Rendu |
|---|---|
| En cours | Normal |
| Finie, gain encaissé | Cadre `G`, coche 12×12, texte en `l` |
| Remplacée (relance utilisée) | Nouvelle mission qui entre par la droite en 250 ms |

Les gains des missions sont crédités **à la fin de l'ascension** où elles se finissent : pas de bouton « réclamer ».

**Coffre bonus** :
- Il est **visible avec son contenu écrit** à l'avance. Ce n'est pas une loot box (garde-fou 7).
- Quand les 3 missions sont finies : `chest` joue les images 0-1 (secousse, 2 × 83 ms, en boucle toutes les 2 s) et un `badge_new` apparaît.
- Un tap ouvre le coffre (images 2-7, 500 ms), puis `popup_reward` montre exactement ce qui était écrit. Son `chest`, H3.
- Raison de ce tap : c'est le seul « réclamer » volontaire du jeu, gardé pour le plaisir de l'ouverture.

**Relance** : `mission_reroll`. Un tap ouvre un mini-modal :
- « CHANGER CETTE MISSION ? » ;
- [▶ VIDÉO] `btn_echo` et [ANNULER] `btn_alt`, 2 × 74×24.

Une fois par jour par mission.

**Calendrier** : il avance d'une case **par jour joué**. Le gain de la case du jour est crédité à la 1re ascension du jour, avec un toast.
Le bonus pub `bonus_chest` est un bouton ▶ 16×16 sur la case du jour déjà encaissée : « ×2 ▶ ».

**Série** : jour manqué → série ÷ 2 (ECONOMY). « RALLUMER » apparaît sur la ligne de série (bouton `btn_alt` 72×24, à droite) seulement le jour du retour, avec deux choix dans un mini-modal : « 150 ◆ » ou « ▶ VIDÉO » (P1, `streak_rekindle`).

| Clé | FR | EN |
|---|---|---|
| `journal` | JOURNAL | JOURNAL |
| `streak_days` | SÉRIE %d JOURS | %d-DAY STREAK |
| `freeze_ready` | GEL PRÊT | FREEZE READY |
| `freeze_used` | GEL UTILISÉ | FREEZE USED |
| `bonus_33` | 3/3 : %d + %d | 3/3: %d + %d |
| `new_missions_in` | NOUVELLES MISSIONS DANS %d H | NEW MISSIONS IN %dH |
| `reroll_q` | CHANGER CETTE MISSION ? | SWAP THIS MISSION? |
| `video` | VIDÉO | VIDEO |
| `cancel` | ANNULER | CANCEL |
| `rekindle` | RALLUMER | REKINDLE |
| Exemples de missions | Grimpe 300 m en une vie. / Grave 3 scies. / Atteins Rythme 20. | Climb 300 m in one life. / Etch 3 saws. / Reach Rhythm 20. |

---

### 3.12 Succès

**But :** voir les 30 défis à long terme et le suivant à portée de main.

**Mise en page** :
- En-tête standard, titre « SUCCÈS 12/30 ».
- Lignes `panel_inset` 164×28, écart 4, à partir de y 32.
- Tri : obtenus non vus, puis **les 3 plus proches d'être finis** (cadre `a`), puis en cours, puis obtenus.

Raison : la ligne du haut est toujours une cible atteignable.

| Élément d'une ligne | x (rel.) | y (rel.) | Style |
|---|---|---|---|
| Icône 16×16 (verrouillé : silhouette `s`) | 6 | 6 | — |
| Nom | 28 | 4 | `font_7` `w` (secret : « ??? ») |
| Condition ou progression « 4/7 JOURS » + barre 80×3 | 28 | 16 | `font_5` `l` ; barre `G` |
| Récompense « 50 ◆ » ou « 1 ◇ » | 132 | 10 | `font_5` |

**Obtenu en jeu** : toast dans le bandeau bas « SUCCÈS : FIDÈLE », icône trophée, `achievement`, H2. Il est différé à la fin de la vie si un danger est à l'écran (priorité P3 de FEEL).

| Clé | FR | EN |
|---|---|---|
| `achievements` | SUCCÈS %d/%d | ACHIEVEMENTS %d/%d |
| `secret` | ??? | ??? |
| `toast_achievement` | SUCCÈS : %s | ACHIEVEMENT: %s |

---

### 3.13 Codex des pièges

**But :** comprendre chaque piège et suivre sa maîtrise (vu, gravé, maîtrisé).

**Grille** :
- En-tête standard, titre « CODEX 9/22 ».
- 4 colonnes de cases `codex_cell` 36×40, écart 6 : x 9, 51, 93, 135 ; y 32 + 46·n.
- Les fiches sont groupées par biome, avec un intertitre `font_7` `l` de 12 px.

| État de la case | Rendu |
|---|---|
| Inconnu | Cadre `n`, silhouette `k` sur `b`, « ? » `font_7` `s` |
| Vu | Sprite du piège à l'image 0, couleurs vraies ; 1 étoile pleine sur 3 |
| Gravé | Sprite **gravé** (échange `x→q` etc.) ; 2 étoiles |
| Maîtrisé (évité 50 fois) | Cadre `G` ; 3 étoiles |
| Nouveau | `badge_new` en x+31, y−2 |

Étoiles : `star` 5×5 × 3, en bas de la case, x +6 / +15 / +24, y +33.

**Fiche** : écran poussé.

| Élément | x | y | l × h | Style |
|---|---|---|---|---|
| Nom « SCIE » | centré | 8 | — | `font_7` `w` |
| Animation 48×48 du piège (boucle), sur fond de mur | 66 | 22 | 48×48 | — |
| Bascule « NORMAL / GRAVÉ » (2 onglets 54×20), visible dès le gravé | 36 | 74 | 108×20 | `tab` |
| 3 étoiles 8×8 + légendes « VU · GRAVÉ · 37/50 » | centré | 100 | — | `font_5` `l` |
| Description (3-4 lignes) | 8 | 116 | 164×48 | `font_8` `w` |
| « COMMENT LE PASSER » (débloqué à ★2) | 8 | 170 | 164×36 | intertitre `font_7` `c`, texte `font_8` |
| Stats « VU 14 · GRAVÉ 3 · ÉVITÉ 37 » | centré | B−20 | — | `font_5` `l` |

**Gestes** : glisser horizontal sur la fiche = fiche précédente ou suivante (seuil 24 px). Retour = grille.

| Clé | FR | EN |
|---|---|---|
| `codex` | CODEX %d/%d | CODEX %d/%d |
| `seen` | VU | SEEN |
| `etched` | GRAVÉ | ETCHED |
| `mastered` | MAÎTRISÉ | MASTERED |
| `how_to` | COMMENT LE PASSER | HOW TO PASS IT |
| `stats_line` | VU %d · GRAVÉ %d · ÉVITÉ %d | SEEN %d · ETCHED %d · DODGED %d |

---

### 3.14 Tour du jour et partage

**But :** le rendez-vous quotidien : même tour pour tous, un essai classé, puis un partage façon Wordle.

**Fiche du Tour** (écran poussé depuis le bouton du hub) :

| Élément | x | y | l × h | Style |
|---|---|---|---|---|
| « TOUR #312 » | centré | 8 | — | `font_l` `c` |
| « Même tour pour tout le monde aujourd'hui. Reliques désactivées. » | 8 | 30 | 164×24 | `font_8` `w` |
| Aperçu : bande de 16 px avec les 3 biomes du jour en pastilles 16×16 | 8 | 60 | 164×16 | — |
| Statut : « ESSAI CLASSÉ DISPONIBLE » (`G`) ou « TON ESSAI : 612 M » (`w`) + rang P1 « TOP 18 % » | centré | 84 | — | `font_7` |
| Grille de partage (aperçu, si déjà joué) | 8 | 100 | 164×40 | `font_7` |
| **GRIMPER** (essai classé) ou **ESSAI LIBRE** (`btn_alt`, non classé) | 24 | B−40 | 132×32 | — |
| **PARTAGER** (si joué) | 24 | B−72 | 132×24 | `btn_alt` |
| « PROCHAIN TOUR DANS 6 H » | centré | B−8 | — | `font_5` `l`, dans la marge basse : non interactif |

**Texte partagé** (`DisplayServer.clipboard_set` + feuille système `Intent.ACTION_SEND` via plugin) :

```
ÉCHO #312 — 612 m
▮▮▮▮▮▮✕ ▮▮▮▮✕ ▮▮▮▮▮▮▮▮✕ ▮▮✕
3 gravures
```

Le texte compte un `▮` par 25 m de chaque vie, et non par 10 m comme dans le GDD.
Raison : 10 m donnent jusqu'à 145 caractères par vie, ce qui est illisible dans un message. Avec 25 m, on obtient 4 lignes de moins de 40 caractères (arbitrage A11).
EN : `ECHO #312 — 612 m` … `3 etched`.

**Image partagée** (P1) : `share_card` 180×100 rendue dans un `SubViewport`, avec le logo, le numéro, l'altitude en `font_l`, les 4 barres de vie, puis agrandie ×4 (720×400).

| Clé | FR | EN |
|---|---|---|
| `daily_title` | TOUR #%d | TOWER #%d |
| `daily_body` | Même tour pour tout le monde aujourd'hui. Reliques désactivées. | Same tower for everyone today. Relics are off. |
| `daily_ranked_ready` | ESSAI CLASSÉ DISPONIBLE | RANKED TRY READY |
| `daily_your_try` | TON ESSAI : %d M | YOUR TRY: %d M |
| `daily_free` | ESSAI LIBRE | FREE TRY |
| `daily_next` | PROCHAIN TOUR DANS %d H | NEXT TOWER IN %dH |
| `share_graves` | %d gravures | %d etched |

---

### 3.15 Réglages et confidentialité

**But :** régler confort et accessibilité en moins de 10 s, et accéder au consentement pub à tout moment.

**Mise en page** (en-tête standard, titre « RÉGLAGES » ; liste qui défile à partir de y 32)

| Rangée | y (rel. liste) | Contrôle | Valeurs |
|---|---|---|---|
| EFFETS | 0 | intitulé `font_7` `l` (10 px) + **segments 3 × 54×24** à x 9 | COMPLETS · RÉDUITS · MINIMUM |
| VIBRATIONS | 38 | idem | AUCUNE · LÉGÈRES · FORTES |
| SON | 76 | intitulé à gauche (x 8, y +7) + `slider` 96×24 (piste 96×4, curseur 8×12) à x 60 + icône muet 24×24 à x 160 | 0 à 10 |
| MUSIQUE | 104 | idem | 0 à 10 |
| LANGUE | 132 | intitulé + segments 2 × 54×24 | FRANÇAIS · ENGLISH |
| MAIN DU POUCE (P1) | 170 | segments 2 × 54×24 | DROITE · GAUCHE |
| NOTIFICATIONS | 208 | intitulé + `toggle` 32×16 (cible 48×24) à x 132 | OFF par défaut |
| CONFIDENTIALITÉ | 236 | `btn_alt` 164×24, icône bouclier | ouvre le formulaire UMP |
| POLITIQUE DE CONFIDENTIALITÉ | 264 | `btn_alt` 164×24 | ouvre l'URL dans le navigateur |
| CRÉDITS | 292 | `btn_alt` 164×24 | écran simple, défilement lent |
| version « v0.4.2 · ID 7F3A » | 324 | `font_5` `s` | — |

**« MAIN DU POUCE »** (P1) inverse en miroir les colonnes de mur du HUD et la position du bouton pause. Raison : un gaucher couvre le coin opposé.

**Effets du réglage EFFETS** (relie `Juice.fx_level`) :
- **COMPLETS** (2) : tout.
- **RÉDUITS** (1) :
  - tremblements ÷ 2, sans tremblement de caméra à la mort ;
  - pas de « respiration » des boutons ;
  - parallaxe des menus à 50 % ;
  - flashs remplacés par un cadre de 1 px.
- **MINIMUM** (0) :
  - aucun tremblement ni flash ni slow-mo ;
  - transitions en trame 2 pas sans mouvement ;
  - compteurs posés directement avec un seul `tick` ;
  - gravure en tampon fixe ;
  - pas de confettis.

Le **danger reste télégraphié** à 100 % dans tous les modes. Raison : le préavis est du jeu, pas de l'effet.

**Confidentialité (UMP)** :
- Si `ConsentInformation.getPrivacyOptionsRequirementStatus() == REQUIRED` : bouton « CONFIDENTIALITÉ » → `UserMessagingPlatform.showPrivacyOptionsForm`.
- Sinon, le bouton est masqué et seule la politique reste.

Sous le bouton, en `font_8` `l` : « Choisis si les pubs peuvent être personnalisées. » / « Choose whether ads can be personalised. »
Le jeu ne vise **pas les moins de 13 ans** (ECONOMY garde-fou 10) : `tag_for_under_age_of_consent` reste false, avec une classification IARC 12+.

**Notifications** : opt-in. L'interrupteur demande la permission Android 13 (`POST_NOTIFICATIONS`) au premier passage à ON. Au plus 1 par jour, à 18 h locale : « La Tour #313 t'attend. » / « Tower #313 is waiting. »

**Retour immédiat** : chaque segment pressé joue `toggle` et applique tout de suite.
- Vibrations : un retour H2 de démonstration (sauf « AUCUNE »).
- Son : `tick` au volume choisi à chaque cran.

Pas de bouton « Enregistrer » : sauvegarde à chaque changement (`GameState.save()`).

| Clé | FR | EN |
|---|---|---|
| `settings` | RÉGLAGES | SETTINGS |
| `fx` | EFFETS | EFFECTS |
| `fx_full` / `fx_reduced` / `fx_min` | COMPLETS / RÉDUITS / MINIMUM | FULL / REDUCED / MINIMAL |
| `vib` | VIBRATIONS | VIBRATION |
| `vib_off` / `vib_light` / `vib_full` | AUCUNE / LÉGÈRES / FORTES | OFF / LIGHT / STRONG |
| `sound` / `music` | SON / MUSIQUE | SOUND / MUSIC |
| `language` | LANGUE | LANGUAGE |
| `thumb` | MAIN DU POUCE | THUMB SIDE |
| `right` / `left` | DROITE / GAUCHE | RIGHT / LEFT |
| `notifications` | NOTIFICATIONS | NOTIFICATIONS |
| `privacy` | CONFIDENTIALITÉ | PRIVACY |
| `privacy_hint` | Choisis si les pubs peuvent être personnalisées. | Choose whether ads can be personalised. |
| `privacy_policy` | POLITIQUE DE CONFIDENTIALITÉ | PRIVACY POLICY |
| `credits` | CRÉDITS | CREDITS |
| `notif_daily` | La Tour #%d t'attend. | Tower #%d is waiting. |

« POLITIQUE DE CONFIDENTIALITÉ » fait 28 caractères × 6 = 168 px : **trop long pour 164 − 24 (icône)**. Le bouton affiche donc « POLITIQUE DE CONFID. » (20 car.). Règle générale au §6.4.

---

## 4. HUD en partie

### 4.1 Principe

**Le HUD ne masque jamais le jeu.**
- Il occupe la bande haute de 20 px, qui affiche du mur en dessous de toute façon.
- Il occupe aussi deux colonnes de 14 px **dans les murs** (x 2-15 et x 164-177). Les murs font 18 px à 180 de large.
- Le puits (x 18-161) ne reçoit que le « bandeau bas » (§4.4), sous le héros.

Raison : le joueur lit le puits au-dessus du héros. Tout ce qui s'y trouve coûte une mort.

### 4.2 Bande haute (y `It` à `It+19`)

Fond : `hud_bar` 180×20.
- `k` plein sur les rangées 0 à 15 ;
- trame de Bayer `k` à 50 % sur les rangées 16-17, à 25 % sur les rangées 18-19.

Raison : séparer le HUD du jeu sans ligne dure ni alpha.

| Élément | x | y | Taille | Style | Toujours visible ? |
|---|---|---|---|---|---|
| Pause (icône `pause` 12×12) | 4 | 4 | cible 28×28 (x 0-27, y 0-27) | `l` ; pressé `w` | oui |
| **Altitude** « 412 » + « M » | 22 (aligné à gauche) | 2 | chiffres `font_l` 10×16, « M » `font_7` | `w`, contour `k` | oui |
| Écart au record « −28 » (sous l'altitude, quand on est à moins de 50 m du record) | 22 | 18 | `font_5` | `a` | contextuel |
| **Lanternes de vie** × 4 | 80, 93, 106, 119 | 4 | 12×12 | `ui_lantern` images 0-1 (allumée, flamme qui alterne à 3 i/s), 3 (éteinte, écho `c`) | oui |
| **Éclats** de l'ascension : nombre aligné à droite sur x 161 + icône | 137-161 / 164 | 5 / 4 | `font_7` + 12×12 | `G`, contour `k` | oui |

**Lanternes = vies et échos** :
- Allumée (chaude `a A o`) = vie restante.
- Éteinte en cyan (`q t c`) = vie déjà perdue, donc **un écho posé dans la tour**.

On lit d'un coup d'œil « vies restantes » **et** « échos laissés ». Raison : le brief demande les deux, et un seul objet porte le lien de cause.

**Sous la lanterne de la vie en cours**, un pas de 1 px `a` clignote (500 ms) pendant les 2 premières secondes de chaque vie.

### 4.3 Colonnes de mur (contextuelles)

Chaque objet apparaît par un pop (3 images de 50 ms : 6×6 → 14×14 → 12×12) et disparaît par trame (2 × 50 ms).

| Élément | Colonne | x | y | Taille | Apparaît quand | Rendu |
|---|---|---|---|---|---|---|
| **Volte** | G | 3 | 28 | 12×12 | après la 1re volte de la vie du joueur, et ensuite toujours pendant un saut | Disponible : icône `volte` en `i` sur halo `H`. Utilisée : contour `n`, intérieur `k`. Refusée : clignote `m` 2 fois (FEEL). |
| **Bonus actif** (Plume, Accalmie, Aimant, Lanterne, Élan d'or) | G | 3 | 46 | 12×12 + barre de temps 12×2 à y 60 | pendant l'effet | Icône dans sa bulle `G`. La barre se vide de droite à gauche (`G`, puis `z` sur les 3 dernières secondes **et** clignotement à 4 Hz). |
| **Burins** | G | 3 | 66 | 12×12 + « ×2 » `font_5` à y 79 | si ≥ 1 burin | Icône burin, halo `c` |
| **Rythme** | D | 165 | 28 | 12×12 icône + nombre `font_5` à y 42 + 3 pastilles 2×2 à y 50 | Rythme ≥ 3 | Note `w`, nombre `w`. Pastilles : vide `n`, pleine `G` à 10/20/30. Au palier : pop 3 images, carillon, H1, cadre de mur 1 px `G` pendant 2 images. Rupture : le nombre tombe de 4 px en 3 images, puis disparaît (sans son de punition). |
| **Marée proche** | G | 3 | B−40 | 12×12 icône vague + distance « 14 » `font_5` à B−26 | marée **hors écran et à moins de 20 m** | Vague `U` sur `u`, flèche bas `j`. Sous 6 m : tout passe en `j` et pulse à 2 Hz, son `tide_near` 1 fois. Dès que la marée est à l'écran, l'indicateur se cache : la marée **est** l'information. |

**Ordre de priorité si la colonne gauche déborde** (sur 320 de haut, B−40 = 256) : on cache d'abord les burins, puis le bonus garde sa place.

**Marée (FEEL)**, en complément :
- liseré `U` 2 px au bas de l'écran ;
- bande tramée `u` de 8 px à 80 bpm, puis de 12 px à 120 bpm ;
- jauge de Silence 2 px `U` en bas.

Tout cela reste **sous `B`**, dans la marge gestuelle (décor seulement).

### 4.4 Bandeau bas (dans le puits, sous le héros)

- Une seule « case » d'affichage, x 20-159 (140 px), y B−56 → B−41 (16 px). Sur 400 : y 320-335. Le héros est à y 248, donc 72 px au-dessus.
- File de priorité FEEL : P0 tutoriel > P1 record > P2 biome > P3 succès et mission > P4 « FRÔLÉ ×3 ».
- **Une seule bannière à la fois, 400 ms d'écart.** Une bannière de priorité supérieure coupe la courante, qui sort en 2 images.

| Type | Composant | Entrée / tenue / sortie | Texte | Son |
|---|---|---|---|---|
| Record battu | `banner` image « or » | 200 / 1200 / 200 ms | NOUVEAU RECORD ! / NEW BEST! (`font_7` `k` sur `G`) | `record`, H3 |
| Biome | `banner` image « pierre » | 300 / 1200 / 250 ms | LA FONDERIE FROIDE / THE COLD FOUNDRY (`font_7` `w`) | `biome` |
| Autel atteint | `banner` pierre | 200 / 800 / 200 ms | AUTEL 350 M / ALTAR 350 M | `altar`, H2 |
| Mission finie | `toast` | 200 / 1200 / 200 ms | MISSION FINIE / MISSION DONE | `mission`, H2 |
| Pictogramme tutoriel | `banner_tuto` 64×24 (déborde de 8 px vers le haut) | 200 / jusqu'à l'action / 200 ms | aucun | — |

Entrée : montée de 16 px (amorti 8/5/2/1 au pixel). Sortie : trame en 2 pas.

**« FRÔLÉ »** (`a`, `font_7_outline`) n'est **pas** dans le bandeau.
- Il apparaît **à côté du piège frôlé**, côté mur, 400 ms, en montant de 6 px.
- Il n'apparaît jamais dans la zone sacrée (64 px au-dessus du héros). Dans ce cas, il est décalé dans la colonne de mur la plus proche.

### 4.5 Ce que le HUD ne montre pas, et pourquoi

| Absent | Raison |
|---|---|
| Missions | Visibles en pause et à la fin. Lire en grimpant coûte une mort. |
| Total d'éclats du compte | Seul le gain de l'ascension motive pendant la partie. |
| Niveau et XP | Méta, hors partie. |
| Minimap | Le puits fait 9 tuiles : tout est visible. |
| Compte à rebours de la marée | La marée se voit (bande à l'écran) ou s'annonce (indicateur). |

### 4.6 Gestes en partie

- **Tap ou appui n'importe où** à y > `It + 40` : contrôle du héros (GDD §2).
- Entre y `It+20` et `It+40` : **ignoré**. Raison : on ne bondit pas en visant la pause.
- Dans la bande haute, seule la pause répond.
- Deuxième doigt : ignoré par l'UI.
- Retour Android : pause.

### 4.7 Implémentation Godot

- `HUD` est un `CanvasLayer` (layer 10). Tous ses `Control` ont `mouse_filter = IGNORE`, sauf `PauseButton`.
- Les nombres utilisent des `Label` avec `LabelSettings` (police bitmap) et des chiffres de chasse fixe.
- La mise à jour se fait par signaux, jamais dans `_process` : `altitude_changed(m)` (au mètre entier), `lives_changed(n)`, `shards_changed(n)`, `rythme_changed(n, tier)`, `volte_state(s)`, `powerup_started(id, dur)`, `tide_distance(m)`.
- Les colonnes de mur sont des `VBoxContainer` ancrés à gauche et à droite de **l'écran réel**, décalés de `(largeur − 180) / 2` pour suivre le mur de la colonne de jeu.

