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

---

## 5. Bibliothèque de composants pixel

> Tous les fichiers vont dans `game/assets/ui/`, avec leur source `.txt` dans `art/src/ui/` (format `tools/px.py`, `palette: /home/user/Testing/jeu/studio/palette_v2.txt`).
> Lumière en haut à gauche. Contour `k` de 1 px partout, sauf mention contraire.
> Les images d'un même fichier sont **côte à côte horizontalement**.
> Dans Godot, chaque image est une `AtlasTexture` (région) servie à un `StyleBoxTexture`.

### 5.1 Panneaux (9-slice)

| Fichier | Taille | Marges 9-slice | Couleurs | Usage |
|---|---|---|---|---|
| `panel.png` | 24×24 | 8 / 8 / 8 / 8 | fond `d` ; bord de pierre `n s m` (3 px) ; arête `l` 1 px en haut à gauche ; coins = sceau d'écho `t` 3×3 ; contour `k` | Panneaux standard (pause, fin) |
| `panel_echo.png` | 24×24 | 8 | fond `d` ; bord `q t c` ; coins `e` ; contour `k` | Mort, offre de pub, abandon, déblocages |
| `panel_inset.png` | 24×24 | 6 | fond `b` ; bord intérieur creusé : `k` en haut à gauche, `n` en bas à droite ; pas de contour externe | Blocs dans un panneau : butin, missions, lignes de liste |

- Le centre (8×8) est **uni** : l'étirement ne crée aucun motif.
- `content_margin` = 8 pour `panel` et `panel_echo`, 6 pour `panel_inset`.

### 5.2 Boutons (9-slice, 3 images)

| Fichier | Taille | Images | Marges | Couleurs | Texte |
|---|---|---|---|---|---|
| `btn_main.png` | 144×24 (3 × 48×24) | 0 normal, 1 pressé, 2 désactivé | g/d 8, h 6, b 8 | face `o`, haut de face `a` (2 rangées), ombre `R` (2 px), bord sombre `r`, contour `k` | `font_7` **`k`** (contraste 7,2 sur `o`) |
| `btn_alt.png` | 144×24 | idem | idem | face `s`, haut `m`, ombre `n`, contour `k` | `font_7` `w` (8,5) |
| `btn_echo.png` | 144×24 | idem | idem | face `c`, haut `e`, ombre `t`, bord `q`, contour `k` | `font_7` **`k`** (12,0 sur `c`) |

**Changement par rapport à l'ART_BIBLE** : la face du bouton vidéo est `c`, pas `t`.
Raison : un texte `w` sur `t` n'atteint que 3,77:1, sous le seuil de 4,5:1 du petit texte.

| État | Image | Contenu | Règle |
|---|---|---|---|
| Normal | 0 | Libellé à y 7 (sur 24) | Ombre de 2 px sous la face. |
| Pressé | 1 | La face descend de 2 px, l'ombre disparaît, le libellé descend de 2 px | Tenu ≥ 3 images (50 ms) même sur un tap très bref. **L'action part au relâchement** si le doigt est encore dans la cible élargie de 4 px. |
| Désactivé | 2 | Face `n`, haut `s`, pas d'ombre, libellé `m` | **Toujours accompagné d'une raison lisible** : cadenas, « IL MANQUE 120 », « AU NIVEAU 25 ». Un tap joue `deny` + H1 et affiche un toast d'explication. |
| Nouveau | 0 + `badge_new` | Badge 7×7 en haut à droite, débordant de 2 px | Disparaît au 1er tap ou après 1 s de vue. |
| Respiration (GRIMPER seulement) | 0 | Le bouton monte de 1 px pendant 2 images toutes les 2 s | Coupée en Effets réduits et minimum. |

Implémentation : `UIK.button(text, kind, ico, min_w)` existe déjà.
- Passer l'action de `pressed` à `button_up` + vérification `get_global_rect().grow(4).has_point(...)`.
- Ou plus simple : `action_mode = BaseButton.ACTION_MODE_BUTTON_RELEASE` (déjà le défaut de Godot), avec le son joué sur `button_up`, pas sur `button_down`. Voir arbitrage A9.

**Tailles d'usage** :

| Bouton | Taille |
|---|---|
| Principal | 124-156 × 32 |
| Standard | 72-164 × 24 |
| Icône | 28×28, avec une icône 16×16 centrée et le `btn_alt` étiré |

### 5.3 Onglets et segments

| Fichier | Taille | Images | Marges | Couleurs |
|---|---|---|---|---|
| `tab.png` | 72×20 (3 × 24×20) | 0 inactif, 1 actif, 2 pressé | 6 | Inactif : face `d`, bord `n`, texte `l`. Actif : face `s`, haut `m`, filet 2 px `a` en bas, texte `w`. Pressé : face `n`. |

- **Segments** (réglages) : on aligne plusieurs `tab` de 24 px de haut (même source, étirée), avec bord commun.
- Sélection = image 1. Elle porte aussi une **coche 12×12** devant le libellé. Raison : la sélection ne se lit pas qu'à la couleur.

### 5.4 Barres

| Fichier | Taille | Contenu |
|---|---|---|
| `bar.png` | 40×6 | 5 cases de 8×6 : 0 cadre (contour `k`, fond `b`) ; 1 remplissage XP `j` (haut `J`) ; 2 progression `G` (haut `y`) ; 3 écho `c` (haut `e`) ; 4 alerte `z` (haut `Z`) |

- Le cadre est un 9-slice de marge 2. Le remplissage est un `TextureProgressBar` en mode étiré.
- Hauteurs utilisées : 2, 3, 4 et 6 px. Les barres de 2-3 px n'ont pas de cadre.
- Animation de remplissage : **au pixel**, 1 px par image au plus (vitesse plafonnée à 60 px/s). La fin est soulignée par un éclat `W` de 1×hauteur au bout, pendant 2 images.

### 5.5 Badges

| Fichier | Taille | Images | Couleurs | Règle |
|---|---|---|---|---|
| `badge_new.png` | 28×7 (4 × 7×7) | 0-3 : pulse (7×7, 7×7 avec reflet `y`, 5×5, 7×7), 150 ms par image, puis pause de 1,4 s | rond `G`, « ! » `k` 1×4, contour `k` | Or = « gain disponible ». Jamais magenta (le magenta est le danger). |
| `hud_pip.png` | 4×2 (2 × 2×2) | vide `n` ; plein `G` | — | Paliers du Rythme |
| `diff_pips.png` | 12×4 (3 × 4×4) | rond `l` ; losange `a` ; triangle `o` | contour `k` | Difficulté des missions, lisible par la forme |

### 5.6 Icônes 12×12 (`icons12.png`, 288×12, 24 icônes)

Règles : 5 couleurs au plus, contour `k`, lumière en haut à gauche, silhouette lisible en `k` seul.

| # | Nom | Couleurs principales | Usage |
|---|---|---|---|
| 0 | `pause` | `l w` | HUD |
| 1 | `shard` (éclat) | `g G y` + `o` en ombre | Monnaie |
| 2 | `prism` | `t c e` + reflet `Z` | Monnaie rare |
| 3 | `xp` (étoile à 4 branches) | `j J` | XP |
| 4 | `volte` | `H i I` | HUD |
| 5 | `rythme` (note) | `w l` | HUD |
| 6 | `tide` (vague + flèche) | `u U j` | HUD |
| 7 | `burin` | `m l` + halo `c` | Bonus |
| 8 | `plume` | `i I` | Bonus |
| 9 | `calm` (Accalmie, sablier) | `f F` | Bonus |
| 10 | `magnet` | `R o` + `l` | Bonus P1 |
| 11 | `lantern_pu` | `a A` | Bonus P1 |
| 12 | `elan_gold` | `g G` | Bonus P1 |
| 13 | `lock` | `m l` | Verrou |
| 14 | `check` | `f F` | Fait, sélectionné |
| 15 | `cross` | `z Z` + forme en X | Erreur, refus |
| 16 | `video` (▶ dans un rond) | `t c e` | Pub |
| 17 | `flame` | `o a A` | Série |
| 18 | `ice` | `c e` | Gel de série |
| 19 | `trophy` | `g G y` | Succès |
| 20 | `grave` (stèle + sceau) | `s m` + `c` | Gravures |
| 21 | `altar` | `m l` + `a` | Autel |
| 22 | `arrow_down` | `l w` | Indicateurs |
| 23 | `chest_mini` | `G` + `n s` | Coffre bonus |

Équivalences avec `UIK.Ico` (prototype) :

| `UIK.Ico` | `icons12` |
|---|---|
| `LIFE`, `LIFE_USED` | `ui_lantern` |
| `SHARD` | 1 |
| `PAUSE` | 0 |
| `LOCK` | 13 |
| `CHECK` | 14 |
| `FLAME` | 17 |
| `TROPHY` | 19 |
| `VIDEO` | 16 |

Les icônes de boutons (`PLAY`, `SHARE`, `GEAR`, `HOME`, `SOUND_*`, `VIBRATION`, `BACK`, `CALENDAR`) passent en 16×16.

### 5.7 Icônes 16×16 (`icons16.png`, 256×16, 16 icônes)

| # | Nom | Couleurs principales | Usage |
|---|---|---|---|
| 0 | `play` (▶) | `k` sur bouton `o` | Grimper |
| 1 | `replay` (flèche circulaire) | `k` | Rejouer |
| 2 | `home` (porte de la tour) | `w m` | Maison |
| 3 | `share` | `w l` | Partager |
| 4 | `video` | `k` sur bouton `c` | Pubs |
| 5 | `shop` (écharpe) | `R o a` | Boutique |
| 6 | `journal` (parchemin) | `i H` + `a` | Missions |
| 7 | `codex` (livre + œil) | `m l` + `c` | Codex |
| 8 | `trophy` | `g G y` | Succès |
| 9 | `gear` | `m l w` | Réglages |
| 10 | `daily` (calendrier « 312 ») | `w l` + `c` | Tour du jour |
| 11 | `back` (flèche gauche) | `w` | Retour |
| 12 | `sound` (haut-parleur ; la barre de « coupé » est ajoutée en code par l'image 2 de `toggle`) | `w l` | Son |
| 13 | `music` (croche) | `w l` | Musique |
| 14 | `vibration` (téléphone + ondes) | `w l` | Vibrations |
| 15 | `shield` | `w l` + `c` | Confidentialité |

**État « coupé »** des bascules de pause : une barre diagonale `z` de 2 px **et** l'icône passe en `s`. Raison : double codage, forme + valeur.

### 5.8 Compteurs qui roulent

- Chiffres de **chasse fixe** dans toutes les polices : 5 px de dessin, 6 px d'avance en `font_7`, 10 en `font_l`, 4 en `font_5`.
- Chaque chiffre est un `Control` de taille cellule, avec `clip_contents = true`.
- Quand un chiffre change, l'ancien monte et le nouveau arrive du bas : décalages 10 → 5 → 2 → 0 en `font_7`, ou 16 → 8 → 3 → 0 en `font_l`, à 1 pas toutes les 2 images (100 ms au total).
- Les chiffres de droite changent d'abord ; il n'y a pas de cascade au-delà de 12 changements par seconde.
- **Comptage long** (fin d'ascension) : `tween_method` de 0 à N, en `TRANS_QUART` + `EASE_OUT`, en 600 ms ; `tick` tous les 10 unités, au plus 12 par seconde.
- **Gain** : le nombre passe en `y` pendant 2 images, puis revient à `G`.
- **Perte** (achat) : le nombre passe en `l` pendant 2 images, puis revient.
- Effets minimum : valeur posée directement, 1 `tick`.

### 5.9 Cartes (boutique, récompenses)

| Fichier | Taille | Images | Marges | Couleurs |
|---|---|---|---|---|
| `card.png` | 96×24 (4 × 24×24) | 0 normale (`panel_inset` + bord `n`) ; 1 sélectionnée (bord `w` 1 px + coins `a`) ; 2 équipée (bord `G` 1 px) ; 3 verrouillée (fond `k`, bord `n`, trame `d`) | 6 | — |

**Carte de boutique** 48×56 :
- vignette 32×32 à (8, 4) : le **héros réel** dans la tenue, image 0 de l'idle, rendu par un `SubViewport` 32×32 partagé, mis en cache en `ImageTexture` ;
- nom `font_5` à y 40 (11 caractères au plus) ;
- prix à y 48.

**Carte de récompense** (`popup_reward`, fin d'ascension, coffre, niveau) : 64×64.
- Rayons animés en 6 images, 83 ms par image, en boucle, couleurs `G y` sur `d`.
- L'objet 32×32 est au centre ; le libellé en `font_7` est en dessous.
- Elle arrive par un pop : 40 % → 115 % → écrasé (ART_BIBLE E2-G), **dessiné en images, jamais réduit par calcul**.
- Elle se ferme d'un tap n'importe où après 400 ms.

### 5.10 Carte « Prochain objectif » (composant clé)

- Taille 164×28, `panel_inset`, bord 1 px `a`.
- Icône 16×16 à (6, 6) ; texte `font_8` `w` à (28, 4) sur 1 ou 2 lignes ; mini-barre 108×3 `G` à (28, 21) ; récompense `font_5` `G` à droite.
- Un tap ouvre l'écran concerné.

**Choix de l'objectif** (fonction `NextGoal.pick()`) : on retient le candidat au **plus petit reste relatif**, `reste / cible`.

| Candidat | Texte FR | Texte EN |
|---|---|---|
| Record | Record : encore 28 m | Best: 28 m to go |
| Mission la plus avancée | Grave 1 scie de plus · 40 ◆ | Etch 1 more saw · 40 ◆ |
| Niveau | Niveau 13 dans 140 XP · traînées | Level 13 in 140 XP · trails |
| Tenue la moins chère non possédée | Braise dans 60 ◆ | Ember in 60 ◆ |
| Coffre bonus 3/3 | Une mission avant le coffre | One mission to the chest |
| Palier du Défi (P1) | Argent : encore 40 m | Silver: 40 m to go |

**Exclusions** :
- tout ce qui demande une pub ;
- tout ce qui coûte des prismes ;
- tout reste > 60 %, sauf s'il n'existe pas d'autre candidat.

Raison : l'objectif doit être atteignable en une ascension, ce que le joueur ressent comme « juste une de plus ».

### 5.11 Cases de calendrier

| Fichier | Taille | Images | Contenu |
|---|---|---|---|
| `cal_cell.png` | 60×28 (3 × 20×28) | 0 à venir (`panel_inset`, chiffre `s`) ; 1 aujourd'hui (bord `a` qui pulse à 1 Hz) ; 2 obtenue (fond `n`, coche `f`) | Chiffre du jour `font_5` en haut ; icône de récompense 12×12 au centre ; montant `font_5` en bas |

La case 7 (120 + 3 ◇) a un coffre 12×12 et un bord `G` en permanence.

### 5.12 Toasts

- `toast.png` 24×16 en 9-slice (marge 6), fond `k`, bord `n`, arête `m`.
- Icône 12×12 à gauche + texte `font_7` ; largeur = contenu + 20 ; au plus 140 px.
- Position : le bandeau bas en partie (§4.4) ; dans les menus, y B−24, centré.
- Durées : 200 / 1600 / 200 ms. File de 3 au plus ; deux toasts du même type fusionnent (« 2 MISSIONS FINIES »).
- Un toast n'est **jamais interactif**. Raison : un toast qu'on doit toucher est un bouton caché.

### 5.13 Tutoriel

| Fichier | Taille | Images | Couleurs | Usage |
|---|---|---|---|---|
| `banner_tuto.png` | 64×24 | 1 | `panel` en version courte, fond `d`, bord `n s` | Support des pictogrammes |
| `tuto16.png` | 96×32 | 6 pictogrammes × 2 images | `w` + `l`, contour `k` | Rangée 0 = pose A, rangée 1 = pose B. 0 tap ; 1 tenir (doigt + arc long) ; 2 volte (tap en l'air) ; 3 glisse ; 4 danger (triangle + dents) ; 5 autel |
| `tap.png` | 64×32 (2 × 32×32) | 2 | `i I` + contour `k` | Existant. Main posée sur le mur. |

Les 2 images de `tuto16` alternent à 400 ms.

### 5.14 Effets d'interface

| Fichier | Taille | Images | Usage |
|---|---|---|---|
| `dither.png` | 16×4 | 4 motifs de Bayer 4×4 : 25, 50, 75, 100 % `k` | Fondus tramés et fonds de modal (shader `ui_dither.gdshader` qui échantillonne le motif selon `step`) |
| `stamp_frame.png` | 320×24 (5 × 64×24) | pop 50 % → 115 % → écrasé → final → final + éclat `e` | Cadre du tampon GRAVÉ ; le texte est posé en `font_l_outline` |
| `chest.png` | 256×32 (8 × 32×32) | 0-1 secousse ; 2-4 ouverture (couvercle, lueur `G`, pic `W` 1 image) ; 5-6 ouvert lueur ; 7 ouvert final | Coffre bonus et case 7 |
| `popup_reward.png` | 384×64 (6 × 64×64) | rayons | §5.9 |
| `shard_mini.png` | 24×6 (4 × 6×6) | rotation | `coin_fly` (au plus 12 à la fois) |
| `confetti.png` | 24×3 (8 × 3×3) | 4 couleurs (`G o c j`) × 2 orientations | `ui_confetti`, 24 particules, 700 ms, gravité 200 px/s² |
| `countdown.png` | 216×32 (3 chiffres × 3 images de 24×32) | pop | Reprise après pause |
| `xp_badge.png` | 40×20 (2 × 20×20) | normal ; montée de niveau (bord `G` + reflet `y`) | Hub, niveaux |
| `level_node.png` | 64×16 (4 × 16×16) | passé `c` ; actuel `G` ; futur `s` ; déblocage majeur (sceau `e`) | Tour des niveaux |
| `codex_cell.png` | 108×40 (3 × 36×40) | inconnu ; vu ; maîtrisé (bord `G`) | Codex |
| `star5.png` | 10×5 (2 × 5×5) | vide `n` ; pleine `G` | Codex grille |
| `star8.png` | 24×8 (3 × 8×8) | vide ; pleine ; pop | Fiche du codex |
| `toggle.png` | 96×16 (3 × 32×16) | off (rail `n`, bouton `m` à gauche) ; on (rail `f`, bouton `w` à droite, coche dans le bouton) ; barre « coupé » 16×16 | Notifications, sourdines |
| `slider.png` | 24×12 | rail 8×4 9-slice (`n` / rempli `l`) + curseur 8×12 × 2 (normal `m l`, pressé `l w`) | Son, musique |
| `shop_pedestal.png` | 64×16 | 1 | Socle de pierre `n s m l` de l'aperçu |
| `hud_bar.png` | 180×20 | 1 | §4.2 |
| `ui_lantern.png` | 48×12 (4 × 12×12) | 0 allumée, 1 flamme alternée, 2 extinction (fumée `l`), 3 éteinte en écho `q t c` | Vies |
| `banner.png` | 96×16 (2 × 48×16) | or (`G` / `y`, contour `k`) ; pierre (`s m`, contour `k`) — 9-slice, marge 6 | Bannières en jeu |
| `biome16.png` | 96×16 (6 × 16×16) | un médaillon par biome | Tour du jour (P1) |
| `share_card.png` | 180×100 | fond + cadre ; le texte est rendu en code | Image de partage (P1) |
| `focus_ring.png` | 8×8 | 9-slice marge 3, `c` 1 px, coins `e` | Focus clavier / manette / contrôle par contacteur (P2) |

---

## 6. Polices pixel

### 6.1 Les quatre polices

| Police | Fichier | Cellule | Hauteur capitale | Avance | Casse | Usage | Couleur de base |
|---|---|---|---|---|---|---|---|
| **5 px** | `font_5.png/.fnt` | 5×8 | 5 | 4 (chiffres 4) | capitales + chiffres + symboles | Badges, prix sur cartes, petits compteurs, légendes ≤ 20 caractères | `w` |
| **7 px** | `font_7.png/.fnt` (= `font_s` actuel, complété) | 6×10 | 7 | 6 (chiffres 6) | capitales + chiffres + symboles | **Tous les boutons, titres, HUD texte** | `w` |
| **8 px** | `font_8.png/.fnt` | 7×12 | 7 (ascendantes 8, x-height 5, descendantes 2) | 4 à 6, proportionnelle | **casse mixte** | Phrases : codex, missions, offres, confidentialité, quasi-réussite | `w` |
| **Grande** | `font_l.png/.fnt` | 10×16 | 12 | 10 (chiffres 10) | capitales + chiffres | Altitude, titres de résultat, tampon | `w` |
| Contours | `font_5_outline`, `font_7_outline`, `font_l_outline` | +2 px | — | identique | — | **Tout texte posé sur le jeu** (HUD, FRÔLÉ, tampon) | contour `k` 1 px, coins inclus |

`font_8` n'a pas de version avec contour. Raison : elle n'est jamais posée sur le jeu, seulement sur un panneau.

**Taille réelle à l'écran** (1080×2400, ×6, 420 dpi) :
- capitale de `font_5` : 30 px physiques = 11,4 dp ;
- capitale de `font_7` : 42 px = 16 dp, soit l'œil d'un texte de 22 sp ;
- `font_l` : 72 px.

Tout est donc **au-dessus** du texte minimal de 12 sp de Material, même `font_5`.

**Caractères par ligne** dans la zone de 164 px :

| Police | Caractères par ligne |
|---|---|
| `font_5` | 41 |
| `font_7` | 27 |
| `font_8` | ≈ 33 (moyenne de 5 px) |
| `font_l` | 16 |

### 6.2 Jeu de glyphes (toutes polices, sauf mention)

- `A-Z`, `0-9`, espace, et la ponctuation `. , : ; ! ? ' " - + / % ( ) # × < > = _ * ·`.
- **Accents FR** : `À Â Ä Æ Ç É È Ê Ë Î Ï Ô Ö Œ Ù Û Ü Ÿ`. Les glyphes suivants **manquent aujourd'hui** dans `font.txt` : `Ä Æ Ö Œ Ü Ÿ`.
- **Typographie FR** : `« »` (5×5), apostrophe `’` (1×2), points de suspension `…` (une seule cellule), tiret demi-cadratin `–` et cadratin `—`.
- **Symboles du jeu** : `◆` éclat (5×5 en `font_5`/`font_7`), `◇` prisme, `▶`, `↻`, `↑ ↓ ← →`, `▮` et `✕` (partage), `★ ☆`, `∞`.
- `font_8` reçoit en plus les **minuscules** `a-z` et `à â ä æ ç é è ê ë î ï ô ö œ ù û ü ÿ`.
  - x-height 5, ascendantes 8, descendantes 2.
  - Accents sur les rangées 0-1 de la cellule (même règle que les capitales : aigu et grave **en diagonale** sur 2 rangées).
- **Espaces** :
  - normale = 3 px (`font_7`, `font_l` : 4) ;
  - **espace fine insécable** U+202F = 1 px, placée avant `! ? : ; »` et après `«` ;
  - insécable U+00A0 = 3 px.

  Le code de localisation remplace automatiquement « ␣! » par « U+202F! » en FR. Raison : la règle typographique française est respectée et la largeur reste maîtrisée.
- **Tailles du `.fnt`** : `lineHeight` 10 / 12 / 16 / 8, `base` = rangée de pied de capitale.
- **Crénage** : aucun en `font_5`/`font_7`/`font_l` (chasse quasi fixe). En `font_8`, 6 paires négatives de 1 px : `Te To Ta Ve Vo Ya`.

### 6.3 Production

`tools/font.py` lit `art/src/ui/font.txt` et sort `font.png` + `.fnt`. À étendre :

1. Accepter les clés `cell:`, `baseline:`, `advance:` par glyphe (`== a advance=4`) ;
2. Produire la variante `_outline` automatiquement (dilatation 1 px en `k`, 8 voisins) ;
3. Un fichier source par police : `font_5.txt`, `font_7.txt` (renommer `font.txt`), `font_8.txt`, `font_l.txt`.

**Contrôle** : une planche `font_check.png` qui affiche, pour chaque police, la pangramme FR « VOIX AMBIGUË D’UN CŒUR QUI AU ZÉPHYR PRÉFÈRE LES JATTES DE KIWIS » et la pangramme EN.

### 6.4 Règles de longueur des textes

- Chaque clé a un **budget en pixels**, noté dans `strings.csv` (colonne `max_px`). Un test automatique mesure FR et EN avec la police réelle (`Font.get_string_size`) et échoue au-delà.
- Budgets types :

| Élément | Budget |
|---|---|
| Bouton de 132 px | 116 px (19 caractères `font_7`) |
| Bouton de 78 px avec icône | 46 px (7 caractères) |
| Segment de 54 px | 48 px (8 caractères) |

- **Pas de texte dans les images** : tout passe par les polices (localisation et taille de l'APK).

---

## 7. Liste des assets UI demandés à l'équipe art

> **Total : 52 fichiers**, dont 41 P0, 8 P1 et 3 P2.
> « Existant » signifie : à reprendre en palette v2 et aux tailles ci-dessous.

| # | Fichier | Taille totale | Images (taille unitaire) | Prio | État |
|---|---|---|---|---|---|
| 1 | `font_5.png` + `.fnt` | ≈ 160×40 | cellule 5×8 | P0 | nouveau |
| 2 | `font_5_outline.png` + `.fnt` | ≈ 224×50 | cellule 7×10 | P0 | généré |
| 3 | `font_7.png` + `.fnt` | ≈ 192×50 | cellule 6×10 | P0 | existant (`font.png`), à compléter : `Ä Æ Ö Œ Ü Ÿ « » ’ … – — ◆ ◇ ▶ ↻ ↑ ↓ ← → ▮ ✕ ★ ☆` |
| 4 | `font_7_outline` | ≈ 256×60 | cellule 8×12 | P0 | généré |
| 5 | `font_8.png` + `.fnt` | ≈ 224×72 | cellule 7×12, casse mixte | P0 | nouveau |
| 6 | `font_l.png` + `.fnt` | ≈ 160×64 | cellule 10×16 | P0 | nouveau |
| 7 | `font_l_outline` | ≈ 192×72 | cellule 12×18 | P0 | généré |
| 8 | `panel.png` | 24×24 | 1 | P0 | existant, à refaire en v2 |
| 9 | `panel_echo.png` | 24×24 | 1 | P0 | nouveau |
| 10 | `panel_inset.png` | 24×24 | 1 | P0 | nouveau |
| 11 | `btn_main.png` | 144×24 | 3 × 48×24 | P0 | existant (2 images), +1 image désactivée |
| 12 | `btn_alt.png` | 144×24 | 3 × 48×24 | P0 | nouveau |
| 13 | `btn_echo.png` | 144×24 | 3 × 48×24 | P0 | nouveau |
| 14 | `tab.png` | 72×20 | 3 × 24×20 | P0 | nouveau |
| 15 | `bar.png` | 40×6 | 5 × 8×6 | P0 | nouveau |
| 16 | `badge_new.png` | 28×7 | 4 × 7×7 | P0 | nouveau |
| 17 | `hud_pip.png` | 4×2 | 2 × 2×2 | P0 | nouveau |
| 18 | `diff_pips.png` | 12×4 | 3 × 4×4 | P0 | nouveau |
| 19 | `icons12.png` | 288×12 | 24 × 12×12 | P0 | existant (`icons.png`, 21), à refaire |
| 20 | `icons16.png` | 256×16 | 16 × 16×16 | P0 | nouveau |
| 21 | `hud_bar.png` | 180×20 | 1 | P0 | nouveau |
| 22 | `ui_lantern.png` | 48×12 | 4 × 12×12 | P0 | nouveau |
| 23 | `banner.png` | 96×16 | 2 × 48×16 | P0 | nouveau |
| 24 | `toast.png` | 24×16 | 1 | P0 | nouveau |
| 25 | `banner_tuto.png` | 64×24 | 1 | P0 | nouveau (P1 dans l'ART_BIBLE, remonté : le tutoriel est P0) |
| 26 | `tuto16.png` | 96×32 | 6 × 2 × 16×16 | P0 | nouveau |
| 27 | `tap.png` | 64×32 | 2 × 32×32 | P0 | existant (dans `sprites/`), à déplacer dans `ui/` |
| 28 | `stamp_frame.png` | 320×24 | 5 × 64×24 | P0 | nouveau |
| 29 | `card.png` | 96×24 | 4 × 24×24 | P0 | nouveau |
| 30 | `shop_pedestal.png` | 64×16 | 1 | P0 | nouveau |
| 31 | `chest.png` | 256×32 | 8 × 32×32 | P0 | nouveau |
| 32 | `popup_reward.png` | 384×64 | 6 × 64×64 | P0 | nouveau (P1 dans l'ART_BIBLE ; requis par les niveaux P0) |
| 33 | `shard_mini.png` | 24×6 | 4 × 6×6 | P0 | nouveau |
| 34 | `dither.png` | 16×4 | 4 × 4×4 | P0 | nouveau |
| 35 | `xp_badge.png` | 40×20 | 2 × 20×20 | P0 | nouveau |
| 36 | `cal_cell.png` | 60×28 | 3 × 20×28 | P0 | nouveau |
| 37 | `codex_cell.png` | 108×40 | 3 × 36×40 | P0 | nouveau |
| 38 | `star5.png` | 10×5 | 2 × 5×5 | P0 | nouveau |
| 39 | `toggle.png` | 96×16 | 3 × 32×16 | P0 | nouveau |
| 40 | `slider.png` | 24×12 | rail + 2 curseurs | P0 | nouveau |
| 41 | `logo.png` | 960×48 | 6 × 160×48 | P0 | existant, à refaire (F10) |
| 42 | `countdown.png` | 216×32 | 9 × 24×32 | P1 | nouveau (P0 de secours : `font_l` sans pop) |
| 43 | `confetti.png` | 24×3 | 8 × 3×3 | P1 | nouveau |
| 44 | `star8.png` | 24×8 | 3 × 8×8 | P1 | nouveau |
| 45 | `level_node.png` | 64×16 | 4 × 16×16 | P1 | nouveau (P0 de secours : `star5`) |
| 46 | `biome16.png` | 96×16 | 6 × 16×16 | P1 | nouveau |
| 47 | `share_card.png` | 180×100 | 1 | P1 | nouveau |
| 48 | `splash.png` | 180×400 | 1 | P1 | nouveau (F10) |
| 49 | `icon_adaptive_fg.png` + `_bg` | 108×108 (×4 à l'export = 432) | 2 | P1 | nouveau (F10, icône Android adaptative) |
| 50 | `focus_ring.png` | 8×8 | 1 | P2 | nouveau |
| 51 | `font_check.png` | — | planche de contrôle | P2 | généré |
| 52 | `store_frames` | 1080×1920 × 5 | cadres de captures | P2 | F10 |

Les **sprites de jeu** utilisés par l'UI ne sont pas comptés ici (pièges pour le codex 48×48, héros en tenues, `fx_engrave`, etc.). Ils sont listés dans l'ART_BIBLE F1-F9.

---

## 8. Récompenses : l'addiction éthique

### 8.1 Principes

1. **Toujours un gain.** Même une ascension de 8 m rapporte 14 éclats, de l'XP et une barre qui avance. L'écran de fin ne dit jamais « ÉCHEC ».
2. **Le gain se compte, il ne se cache pas.** Chaque nombre compte de 0 à sa valeur (§5.8). Un tap montre tout de suite le total. Raison : le joueur qui veut rejouer ne doit pas subir notre spectacle (constat Vampire Survivors : les joueurs demandent l'accélération).
3. **Une seule cible à la fois**, la plus proche (§5.10), visible au hub, en fin d'ascension et en pause.
4. **La relance en 1 s.** REJOUER est actif à 300 ms, au même endroit que GRIMPER (bas de l'écran, pouce), et dans la même couleur.
5. **La pub est un choix.**
   - Bouton cyan, plus petit que l'action principale, récompense écrite dessus.
   - Pas de minuteur, pas de deuxième demande dans la même ascension.
   - Jamais au lancement, jamais pendant le jeu.
6. **Pas de hasard payant.** Les coffres montrent leur contenu avant d'être ouverts. Aucune animation de machine à sous.
7. **Pas de punition visible.** Une rupture de Rythme ne joue aucun son négatif. Une série perdue est **divisée par 2**, pas remise à zéro, et l'écran le dit positivement : « SÉRIE 3 J (GARDÉE À MOITIÉ) ».

### 8.2 Le comptage animé de fin (rappel §3.8)

La chronologie fait 2,4 s au total : altitude (600 ms), puis record, puis vies, puis éclats, puis XP, puis objectif.
Chaque étape a son son, et la hauteur du son monte avec la valeur : `tick` + 1 demi-ton par tranche de 100 m, au plus +12.
Raison : l'oreille sent le progrès avant que l'œil ait lu.

### 8.3 Quasi-réussite : choix de la phrase (une seule)

On teste dans l'ordre et on garde la première phrase qui s'applique. Elle s'affiche en `font_8` `a`.

| Condition | FR | EN |
|---|---|---|
| Record battu | Nouveau record : +34 m ! | New best: +34 m! |
| Record manqué de ≤ 15 % | Plus que 12 m pour ton record | Only 12 m short of your best |
| Défi : palier manqué de ≤ 15 % (P1) | Argent à 18 m près | 18 m from silver |
| Prochain autel manqué de ≤ 20 m | Le prochain autel était à 9 m | Next altar was 9 m away |
| Mission manquée d'1 unité | Encore 1 scie à graver | 1 more saw to etch |
| Biome suivant à ≤ 30 m | La Fonderie commence à 21 m | The Foundry starts 21 m higher |
| Sinon | Ta meilleure vie : la 3e (218 m) | Your best life: #3 (218 m) |

**Rapprochement record.** Pendant la partie, quand on est à moins de 50 m du record, l'écart s'affiche sous l'altitude (« −28 », `a`). La **ligne de record** dans le monde (FEEL n°25) est visible.
Raison : la quasi-réussite se vit en jouant, pas seulement après.

### 8.4 Ce qui est interdit (liste de contrôle pour la revue)

- Un compte à rebours sur une offre ou un bouton.
- Un bouton « non » plus petit, plus pâle ou décalé que le bouton « oui » d'une pub.
- Une pub sans récompense annoncée, ou une pub qui démarre seule.
- Un texte de culpabilisation (« Tu abandonnes déjà ? »).
- Une récompense qui expire si on ne revient pas, sauf la série, qui est divisée et non perdue.
- Une notification sans opt-in, ou plus d'une par jour.
- Une monnaie premium achetable (prismes) : aucune dans P0-P2.

---

## 9. Accessibilité

### 9.1 Cibles

- Au moins **24×24 px logiques** pour toute cible, soit 48 dp dans le pire cas (§1.4).
- Écart d'au moins 4 px entre cibles.
- Les cibles d'action fréquentes (GRIMPER, REJOUER, REPRENDRE) font **32 px** de haut, soit 64 dp au pire.
- Toutes les actions de navigation sont dans les **60 % bas**. Le seul contrôle en haut est la pause (cible 28×28), doublée par le bouton Retour.

### 9.2 Contraste (WCAG 2.x, calculé sur palette_v2)

| Paire (texte / fond) | Ratio | Usage | Verdict |
|---|---|---|---|
| `w` / `d` | 14,1 | Texte courant sur panneau | AAA |
| `w` / `k` | 17,6 | HUD, toasts | AAA |
| `l` / `d` | 5,5 | Texte secondaire | AA |
| `l` / `b` | 6,4 | Texte secondaire sur encart | AA |
| `G` / `d` | 11,2 | Éclats, gains | AAA |
| `a` / `d` | 9,3 | Quasi-réussite, série | AAA |
| `c` / `d` | 9,6 | Textes d'écho | AAA |
| `e` / `d` | 13,8 | Gravure | AAA |
| `j` / `d` | 4,6 | XP | AA (petit texte limite : réservé aux nombres ≥ `font_7`) |
| `z` / `d` | 4,5 | Erreur, prix trop cher | AA limite : **toujours doublé** par une forme (croix, tremblement) |
| `k` / `o` | 7,2 | Libellé du bouton principal | AAA |
| `w` / `s` | 8,5 | Libellé du bouton secondaire | AAA |
| `k` / `c` | 12,0 | Libellé du bouton vidéo | AAA |
| `w` / `t` | 3,8 | — | **Refusé** : n'est plus utilisé (§5.2) |
| `m` / `d` | 2,6 | Libellé désactivé | Exempté par WCAG ; toujours doublé d'un cadenas ou d'une raison |

Les éléments non textuels (icônes du HUD sur `k`) sont tous ≥ 3:1. L'icône la plus faible est `U` / `u` = 1,9 ; c'est pourquoi la vague de la marée a une crête `j` (4,6 sur `u`).

### 9.3 Mode effets réduits (rappel du §3.15)

Trois niveaux : COMPLETS, RÉDUITS, MINIMUM.

**Détection automatique au premier lancement** :
- si `animator_duration_scale == 0` (option Android « supprimer les animations ») → MINIMUM ;
- s'il vaut moins de 1 → RÉDUITS.

Lecture via un plugin Android ou `OS.execute` non disponible : la valeur par défaut est COMPLETS, et le réglage est proposé dès le premier passage au hub (P1).

Dans tous les modes, **les flashs restent sous 3 par seconde** et ne couvrent jamais tout l'écran (FEEL).

### 9.4 Daltonisme : le danger ne se lit pas qu'à la couleur

| Information | Couleur | Doublée par |
|---|---|---|
| Piège dangereux | magenta `x X z Z` | Triangles et dents, pulsation, préavis ≥ 450 ms (ART_BIBLE) |
| Piège gravé (inoffensif pour le héros fantôme) | cyan `q t c e` | Pointes émoussées, sceau, pas de pulsation |
| Erreur d'UI | `z` | Croix `cross`, tremblement ±2 px, son `deny`, haptique double |
| Bonus qui expire | `z` sur la barre | Clignotement 4 Hz |
| Dernière vie | `z` | 3 clignotements + son `warn` |
| Sélection | `w` / `a` | Coche 12×12 |
| Difficulté | `l` / `a` / `o` | Rond / losange / triangle |
| Équipé | `G` | Coche + libellé PORTÉE |

**Test obligatoire** : passer les maquettes et 3 captures de jeu au simulateur deutéranopie, protanopie et tritanopie (filtre Machado 2009). Critère : chaque ligne du tableau reste lisible.
Point de vigilance de l'ART_BIBLE : `o` et `z` ont presque la même luminance (ratio 1,28). **Aucun élément de danger ne touche le héros dans l'UI** (ex. pas de croix `z` à côté de la vignette de l'écharpe).

### 9.5 Autres

- **Sans limite de temps** dans l'UI : aucune offre, aucun écran ne se ferme seul, sauf les toasts, qui ne contiennent jamais d'action.
- **Haptique** : réglable (aucune, légères, fortes). Elle n'est jamais la seule porteuse d'une information.
- **Son** : tout signal sonore utile a un équivalent visuel. Exemples : le « tic » du pendule a un repère `m` au point mort haut (GDD) ; l'approche de la marée a son indicateur de colonne.
- **Une main** : toutes les actions marchent au pouce droit **ou** gauche (option « main du pouce », P1).
- **Lecteur d'écran** (P2) : Godot 4.5 intègre AccessKit. Il faut renseigner `accessibility_name` sur chaque bouton icône (« Boutique », « Pause »…) et `accessibility_description` sur les compteurs.
- **Lisibilité** : aucune police sous 5 px de capitale. Le texte posé sur le jeu a toujours un contour.

---

## 10. Textes : règles communes

- Les clés vivent dans `game/data/strings.csv` (colonnes `key, fr, en, max_px, police`), importées comme `Translation` Godot (`tr()`).
  Raison : `GameState.t()` renvoie aujourd'hui des paires `[fr, en]` codées en dur, ce qui empêche une 3e langue et le test de longueur.
- **Capitales** pour l'interface (`font_5`, `font_7`, `font_l`) ; **casse de phrase** pour les phrases (`font_8`).
- **Tutoiement en FR.** Phrases courtes, sans jargon, avec des verbes d'action : GRIMPER, REJOUER, PORTER.
- **Nombres** : séparateur de milliers = espace fine en FR (« 1 250 »), virgule en EN (« 1,250 »). L'unité « M » est collée avec une espace fine en FR et une espace normale en EN.
- **Pluriels** : clés `_one` / `_n` (§3.5).
- Les noms propres de la tour (biomes, pièges, tenues) sont traduits.

| Biome | FR | EN |
|---|---|---|
| 1 | LA CRYPTE | THE CRYPT |
| 2 | LA FONDERIE FROIDE | THE COLD FOUNDRY |
| 3 | LA BIBLIOTHÈQUE ENGLOUTIE | THE SUNKEN LIBRARY |
| 4 | LE JARDIN SUSPENDU | THE HANGING GARDEN |

« LA BIBLIOTHÈQUE ENGLOUTIE » fait 25 caractères = 150 px en `font_7` : elle tient dans la bannière de 140 px avec `font_5` (100 px). Règle : le nom d'un biome passe en `font_5` s'il dépasse 22 caractères.

---

## 11. Liste d'implémentation priorisée

### P0 — nécessaire pour la première version publique

| # | Tâche | Dépend de | Estimation |
|---|---|---|---|
| 1 | Passer `project.godot` en 180×320 `expand`, écrire `UIRoot` (calcul de `It`, `B`, colonne centrée) | arbitrage A1 | 0,5 j |
| 2 | Polices `font_5`, `font_7` complétée, `font_8`, `font_l` + contours ; extension de `font.py` | assets 1-7 | 2 j (art) + 0,5 j (outil) |
| 3 | Thème Godot `ui_theme.tres` : panneaux, boutons 3 états, onglets, barres, toasts ; `UIK.button` passe à l'action au relâchement | assets 8-24 | 1 j |
| 4 | `UIK.slide` (pas discrets), `dither` shader, compteur qui roule | 34 | 1 j |
| 5 | HUD : bande haute (pause, altitude, lanternes, éclats) + colonnes de mur (volte, bonus, Rythme, marée) + bandeau bas avec file de priorité | 19-23 | 2 j |
| 6 | Premier lancement sans texte : splash, pictogrammes, main sur le mur, UMP reporté | 25-27 | 1 j |
| 7 | Gravure : extinction de lanterne, tampon, bandes ; panneau « Vie perdue » | 28 | 1 j |
| 8 | Pause (bascules, abandon en 2 temps, compte à rebours, pause automatique) | — | 0,5 j |
| 9 | Offre +1 vie (toutes les conditions §3.7) et ×2 en fin d'ascension | AdMob | 1 j |
| 10 | Fin d'ascension complète (chronologie §3.8, accélération par tap, REJOUER à 300 ms) + `NextGoal` | 29, 31-33, 35 | 2 j |
| 11 | Hub (rangée d'icônes, badges, carte objectif, Tour du jour) | 16, 20, 35 | 1 j |
| 12 | Boutique, onglet TENUES (états de cartes, aperçu, achat et refus) | 29-30 | 1,5 j |
| 13 | Journal : missions + calendrier + série + coffre bonus | 18, 31, 36 | 1,5 j |
| 14 | Niveaux (liste simple, `star5` en guise de nœuds) | — | 0,5 j |
| 15 | Codex (grille + fiche, animation 48×48) | 37-38 | 1 j |
| 16 | Succès (liste triée) | — | 0,5 j |
| 17 | Tour du jour : fiche, partage texte | — | 0,5 j |
| 18 | Réglages : effets, vibrations, son, musique, langue, notifications, confidentialité UMP | 39-40 | 1 j |
| 19 | `strings.csv` FR/EN + test de longueur automatique | 2 | 0,5 j |
| 20 | Bouton Retour Android sur tous les écrans (§2.2) | — | 0,25 j |

**Total P0 : ≈ 20 jours de développement**, plus les assets.

### P1 — dans les 4 semaines après le lancement

- Onglets TRAÎNÉES et ÉCHOS de la boutique, avec essai pub (`skin_trial`).
- Tour des niveaux illustrée (`level_node`).
- Image de partage (`share_card`).
- Rangs Google Play Games dans la fiche du Tour.
- Défi hebdo (fiche + paliers dans `NextGoal`).
- Option « main du pouce ».
- Rallumer la série (`streak_rekindle`).
- Bouclier d'écho (`echo_shield`).
- `countdown.png`, `confetti`, `star8`, `biome16`.
- Détection d'« animations supprimées » Android.
- Splash et icône adaptative définitifs.

### P2 — confort et finitions

- AccessKit (noms accessibles), `focus_ring` et navigation manette ou contacteur.
- Mode Zen (fiche).
- Captures du store.
- Planche `font_check`.
- 3e langue (le CSV la permet).
- Statistiques détaillées par piège dans le codex.

---

## 12. Points à arbitrer par le lead

| # | Sujet | Options | Recommandation |
|---|---|---|---|
| A1 | Résolution | 192×352 `keep_width` (brief, `project.godot`) ; 180×320 `expand` (ART_BIBLE) | **180×320 expand.** Échelle ×6 entière sur 1080p et plus de hauteur visible sur les écrans 20:9. |
| A2 | Nom du combo | « Élan » dans FEEL (paliers I-IV à 5/15/30/50) ; « Rythme » dans le GDD (10/20/30) | **Rythme, 10/20/30.** Élan reste le saut long ; corriger FEEL. |
| A3 | Déblocages par niveau | GDD ; ECONOMY | **ECONOMY** (niv 2 missions, 3 traînées, 5 défi, 10 effets d'écho, 15 difficiles…). |
| A4 | Catalogue | 24 ou 19 tenues ; 12 ou 8 reliques ; 22 fiches de codex à 3 étoiles ou 40 entrées ; deux listes de 30 succès | L'UI supporte n'importe quel nombre (grilles qui défilent). Il faut **une** liste. Codex : 22 pièges à 3 étoiles (P0), le reste en P1. |
| A5 | Physique | 60 Hz (FEEL) ; 120 Hz (GDD) | Sans effet sur l'UI, mais les durées « en images » de ce document supposent un **affichage** à 60 Hz. |
| A6 | Couleurs | Les hex d'ECONOMY et des `SKINS` de `game_state.gd` sortent de palette_v2 | Remapper sur palette_v2 : éclats `G g`, prismes `c e` + `Z`, XP `j J`. |
| A7 | Pubs P0 | 4 emplacements (GDD) ; 5 (ECONOMY) | L'UI de ce document couvre les 5. On peut couper `skin_trial` en P1 sans casser l'interface. |
| A8 | Formule de série | GDD ; ECONOMY | L'UI affiche seulement « SÉRIE n J » + gel ; elle ne dépend pas de la formule. Choisir ECONOMY. |
| A9 | Action des boutons | `ui_kit.gd` joue le son et agit sur `pressed` ; FEEL demande l'action au relâchement | **Au relâchement**, son au relâchement, enfoncement visuel à l'appui. |
| A10 | HUD | ART_BIBLE : « rien d'autre en partie » ; brief : Rythme, volte, marée, bonus | **Contextuel dans les murs** (§4.3) : rien n'apparaît tant que ça ne sert pas. |
| A11 | Partage | `▮` par 10 m (GDD) | **Par 25 m.** Avec 10 m, une vie de 1 450 m fait 145 caractères. |
| A12 | Face du bouton vidéo | `t` (ART_BIBLE) | **`c` avec texte `k`.** Contraste 12:1 au lieu de 3,8:1. |
| A13 | Bannières en jeu | En haut (FEEL) | **Bandeau bas, sous le héros** : le haut du puits montre les pièges à venir. |
| A14 | Consentement UMP | Au lancement ; après l'Ascension 0 | **Après l'Ascension 0** (aucune pub n'est chargée avant). À valider avec le juridique. |
| A15 | Icônes | 22 en 12×12 et 10 en 16×16 (ART_BIBLE) | 24 + 16 (§5.6-5.7). |

---

## 13. Maquettes

Toutes en 180×400 (`It = 0`, `B = 376`), avec une copie ×4 (`*_x4.png`) pour la lecture. Les textes sont rendus avec les glyphes de `art/src/ui/font.txt` (capitales 5×7 seulement) : les phrases en `font_8` y sont donc en capitales.

| Fichier | Contenu |
|---|---|
| `ui_mockups/hub.png` | Hub : barre haute, logo (bloc), record, série, carte objectif, rangée d'icônes, Tour du jour, GRIMPER |
| `ui_mockups/hud.png` | Partie : bande haute, colonnes de mur (volte, bonus, Rythme, marée), bandeau bas, zone sacrée en pointillé |
| `ui_mockups/fin.png` | Fin d'ascension : altitude, record, 4 barres de vie, quasi-réussite, butin, objectif, ×2 / PARTAGER, MAISON / REJOUER |

Les maquettes sont des **plans de placement**, pas de l'art final. Les blocs gris-bleu marquent la place des dessins à venir.

---

## 14. Sources

- Documents internes : `studio/BRIEF.md`, `GDD.md`, `ECONOMY.md`, `FEEL.md`, `ART_BIBLE.md`, `palette_v2.txt` ; prototype `game/scripts/ui_kit.gd`, `main.gd`, `game_state.gd`, `project.godot` ; `art/src/ui/font.txt` ; `tools/px.py`, `tools/font.py`.
- Material Design 3 : cibles de 48 dp, contrastes 4,5:1 et 3:1, « never color alone », mouvement réduit, retour prédictif Android.
- Analyses d'écrans de fin et de HUD mobiles (recherche web) :
  - Downwell (HUD minimal, combo comme difficulté implicite) ;
  - Alto's Odyssey (3 objectifs, critiques des objectifs à la chance) ;
  - Archero (contre-exemple : résurrection avec minuteur de 5 s) ;
  - Vampire Survivors (demandes d'accélération des coffres) ;
  - Dead Cells mobile (HUD hors des pouces) ;
  - Slay the Spire mobile (cibles trop petites) ;
  - Crossy Road (rétention avant monétisation).
- Deux pages n'ont pas pu être lues (bugnet.io, gamedeveloper.com : hôtes bloqués par le réseau de la session) ; leurs constats viennent des extraits de recherche.
