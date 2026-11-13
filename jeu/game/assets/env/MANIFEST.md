# MANIFEST — décor F6 (murs, autels) et F7 (fonds)

Sources : `art/src/env/*.txt` (chaque en-tête donne l'intention, le budget de couleurs et le défaut corrigé).
Rendus @8, planches de raccord et maquettes : `art/out/env/`. Palette : `studio/palette_v2.txt`.
Les fichiers d'origine `back.png`, `wall.png`, `floor.png` et `plaque.png` ne sont pas modifiés : tous les nouveaux fichiers ont leur propre nom.

## Conventions communes

- Tuile = 16×16. Les modules de décor font 16×32 (2 tuiles de haut).
- **Mur gauche `_L`** : la face côté puits est à droite. Colonne x14 = chanfrein d'ombre, x15 = `k` (contour de collision).
- **Mur droit `_R`** : x0 = `k`, x1 = chanfrein **éclairé**. Les `_R` ne sont pas des miroirs des `_L` : ils sont dérivés par `art/out/env/vers_droite.py`, et la lumière vient toujours d'en haut à gauche.
- Ligne 15 de chaque tuile = joint horizontal, donc tout se raccorde verticalement dans n'importe quel ordre (vérifié sur des colonnes de 22 tuiles, voir `raccords_*`).
- **Colonnes de mur** (monde de 192 px) :

  | Colonne | Tuiles |
  |---|---|
  | x0 (extérieure gauche) | `_R` |
  | x16 (intérieure gauche) | `_L` |
  | x160 (intérieure droite) | `_R` |
  | x176 (extérieure droite) | `_L` |

  Le `k` des colonnes extérieures tombe dans les 6 px rognés par la caméra. Le code peut assombrir la colonne extérieure pour calmer le mur.
- **Couleurs réservées** :
  - Aucune couleur réservée dans le décor, sauf la flamme d'autel (cyan) et les runes allumées (`G y o`, objet de jeu).
  - Ni brun ni bois.

## Murs par biome (B1 Crypte, B2 Fonderie, B3 Bibliothèque)

### `wall_<biome>_L/R.png` — 128×16, 8 tuiles

| Index | Crypte | Fonderie | Bibliothèque | Fréquence |
|---|---|---|---|---|
| 0 | grand bloc + 2 petits | grande tôle + 2 rivets | bloc haut + 2 petits | base, tirage uniforme 0-3 |
| 1 | rythme inversé | deux tôles soudées | rythme inversé | base |
| 2 | bloc étroit + long | tôle étroite + large | 3 assises décalées | base |
| 3 | 3 assises | 3 bandes | grand bloc nu | base |
| 4 | mousse | tuyau vertical à brides | étagère maçonnée (dos de livres) | 10 % (comme `tower.gd`) |
| 5 | fissure en escalier | grille d'aération | coulure d'eau + 1 goutte | 6 % |
| 6 | niche-reliquaire (rare) | manomètre (rare) | coquillage fossile (rare) | ≤ 1 toutes les 40 rangées, jamais 2 fois à l'écran |
| 7 | **brèche** = tuile 0 + 3 px clairs | **brèche** = tuile 0 + 3 px `4` | **brèche** = tuile 0 + 3 px `8` | **uniquement** devant un passage secret, jamais au hasard |

### `wall_<biome>_lit_L/R.png` — 32×16, 2 tuiles

- Tuile 0 se pose **juste au-dessus** d'une source de lumière (module de décor 0) : arêtes basses éclairées.
- Tuile 1 se pose **juste en dessous** : arêtes hautes éclairées.
- Ne pas les utiliser ailleurs.

### `wall_<biome>_deco_L/R.png` — 64×32, 4 modules de 16×32

| Module | Crypte | Fonderie | Bibliothèque |
|---|---|---|---|
| 0 | lanterne froide (**source** : lit 0 au-dessus, lit 1 en dessous) | veilleuse en cage (**source**, même règle) | lampe de lecture (**source**, même règle) |
| 1 | niche en ogive + urne | tuyau + volant de vanne | rayonnage maçonné à 2 étagères |
| 2 | corniche + 3 bougies | haute grille + gouttes | longue coulure d'eau |
| 3 | plaque d'épitaphe | plaque emboutie | livre ouvert en bas-relief |

Fréquence :
- 1 module toutes les 10 à 14 rangées environ par colonne intérieure.
- Jamais 2 modules à moins de 6 rangées dans la même colonne.
- Pas de module dans les colonnes extérieures, sauf le module 3 (très rare).
- Au plus une source (module 0) à l'écran par mur.

### `rune_<biome>_L/R.png` — 32×16

- Tuile 0 = rune éteinte, tuile 1 = rune allumée.
- Le bloc porteur est identique : on échange la tuile au moment de l'allumage.
- À placer là où le gameplay pose une rune.

### Transitions

Elles se posent de haut en bas : `… biome du haut / tuile 1 / tuile 0 / biome du bas …`, une fois par colonne à la frontière de biome. Les 4 colonnes doivent être alignées sur la même rangée.

| Fichier | Taille | Tuile 0 (basse) | Tuile 1 (haute) |
|---|---|---|---|
| `wall_crypte_to_fonderie_L/R.png` | 32×16 | crypte avec joints d'acier | tôles au-dessus d'un dernier bloc de crypte |
| `wall_fonderie_to_bibliotheque_L/R.png` | 32×16 | tôles avec joints de pierre violette | pierre de bibliothèque au-dessus d'une dernière tôle |

## Autels et sol

| Fichier | Taille | Contenu |
|---|---|---|
| `altar.png` | 32×32 | Autel de la Crypte |
| `altar_fonderie.png` | 32×32 | Palette-swap décidé (`s n m l` → `2 1 3 4`) |
| `altar_bibliotheque.png` | 32×32 | Palette-swap décidé (`s n m l` → `6 5 7 8`) |
| `altar_flame.png` | 48×16 | 6 images de 8×16, **90 ms** par image, en boucle ; commune à tous les biomes |
| `floor_start.png` | 48×16 | 3 tuiles : bout gauche, milieu (à répéter), bout droit |

- **Autels** : bas de l'autel sur le sol. La flamme se pose à (+12, −5) par rapport au coin haut-gauche de l'autel, c'est-à-dire dans la vasque.
- **Flamme** : seul décor cyan autorisé. Le corps est fixe, seule la pointe change.
- **Sol** (`floor_start`) : le sol de départ de la Crypte.

## Fonds (F7)

| Fichier | Taille | Plan | Parallaxe | Pose |
|---|---|---|---|---|
| `bg0_crypte.png` | 256×256 | P0 (le plus loin) | **0.10** | répété en X et en Y, plein cadre ; piliers, 2 baies en ogive, nervures de voûte |
| `bg1_crypte.png` | 256×256, transparent | P1 | **0.30** | répété en X et en Y par-dessus bg0 ; 2 statues encapuchonnées à lanterne, 2 urnes |
| `bg2_crypte.png` | 128×32 | P2 | **0.60** | voir ci-dessous |
| `bg2_crypte_deco.png` | 96×32, transparent | P2 | **0.60** | voir ci-dessous |
| `bg2_fonderie.png` | 128×32 | P2 | **0.60** | voir ci-dessous |
| `bg0_fonderie.png` | 256×256 | P0 | **0.10** | répété en X et Y ; poteaux d'acier, 2 cuves éteintes géantes (tuyaux en boucle haut/bas) |
| `bg1_fonderie.png` | 256×256, transparent | P1 | **0.30** | répété en X et Y ; 2 engrenages (image fixe), 2 chaînes de levage (période 8) |
| `bg0_bibliotheque.png` | 256×256 | P0 | **0.10** | répété en X et Y ; nef noyée : colonnes, arcs en plein cintre, haute fenêtre éteinte |
| `bg1_bibliotheque.png` | 256×256, transparent | P1 | **0.30** | répété en X et Y ; 2 rayonnages en silhouette, 3 pages en suspension |
| `bg2_bibliotheque.png` | 128×32 | P2 | **0.60** | voir ci-dessous |
| `bg2_bord.png` | 48×32 | P2 | **0.60** | piliers de bord des bandes, voir ci-dessous |

**`bg2_crypte.png`** :
- x0-31 : briques en 2 rangées de 16 (T0 en haut, T1 en bas).
- x32, x64, x96 : panneaux de 32×32, à savoir T2 (brique manquante), T3 (grande pierre) et T4 (fissure).
- Pose en 2 bandes de 32 px (x32-63 et x128-159), le centre du puits s'ouvrant sur P0/P1.
- Utiliser surtout T0/T1, et un panneau T2-T4 environ 1 fois sur 6.

**`bg2_crypte_deco.png`** :
- 3 modules de 32×32 : fenêtre en ogive (le centre est transparent et laisse voir P0), niche à urne, chaîne (période de 8 px, peut se répéter verticalement).
- Au plus 1 module par bande et par écran.

**`bg2_fonderie.png`** :
- 4 panneaux de 32×32 : tôle pleine, tôle coupée, tuyau horizontal, grille à lames.
- Pose en bandes comme pour la Crypte. Panneau 0 dominant, 3 au plus 1 fois par écran.

**`bg2_bibliotheque.png`** :
- 4 panneaux de 32×32 : blocs, ligne d'eau (pierre mouillée sous la ligne), arc aveugle en plein cintre, rangée de livres lointains.
- Pose en bandes comme pour la Crypte. Panneau 0 dominant, panneau 1 au plus 1 fois par écran.

**`bg2_bord.png`** (piliers de bord, 6 colonnes de 8×32, répétables verticalement, joints en lignes 15 et 31) :

| x dans la feuille | Biome | Côté | Pose dans le monde |
|---|---|---|---|
| 0-7 | Crypte | D (ferme la bande de gauche) | x56-63 |
| 8-15 | Crypte | G (ferme la bande de droite) | x128-135 |
| 16-23 | Fonderie | D | x56-63 |
| 24-31 | Fonderie | G | x128-135 |
| 32-39 | Bibliothèque | D | x56-63 |
| 40-47 | Bibliothèque | G | x128-135 |

- Le pilier se pose **par-dessus** la bande bg2 (même parallaxe 0.60), sur toute la hauteur. Opaque, 0 px transparent.

Luminances visées :

| Plan | Y |
|---|---|
| P0 | 0.004-0.012 |
| P1 | 0.008-0.020 |
| P2 | 0.012-0.025 |
| Murs | autour de 0.06 |

Le héros et les pièges restent toujours plus clairs que les murs.

## Reste à faire côté décor

- Animation des engrenages de `bg1_fonderie` : rotation en 8 images à 4 fps (bible) ; l'image livrée est la pose 0.
- Transition Bibliothèque → Jardin (non demandée pour l'instant).
- Le code n'est pas branché : `world_draw.gd` charge encore `env/wall`, `env/back` et `env/floor`.
