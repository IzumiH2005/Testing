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

## Murs par biome (B1 Crypte, B2 Fonderie)

### `wall_<biome>_L/R.png` — 128×16, 8 tuiles

| Index | Crypte | Fonderie | Fréquence |
|---|---|---|---|
| 0 | grand bloc + 2 petits | grande tôle + 2 rivets | base, tirage uniforme 0-3 |
| 1 | rythme inversé | deux tôles soudées | base |
| 2 | bloc étroit + long | tôle étroite + large | base |
| 3 | 3 assises | 3 bandes | base |
| 4 | mousse | tuyau vertical à brides | 10 % (comme `tower.gd`) |
| 5 | fissure en escalier | grille d'aération | 6 % |
| 6 | niche-reliquaire (rare) | manomètre (rare) | ≤ 1 toutes les 40 rangées, jamais 2 fois à l'écran |
| 7 | **brèche** = tuile 0 + 3 px clairs | **brèche** = tuile 0 + 3 px `4` | **uniquement** devant un passage secret, jamais au hasard |

### `wall_<biome>_lit_L/R.png` — 32×16, 2 tuiles

- Tuile 0 se pose **juste au-dessus** d'une source de lumière (module de décor 0) : arêtes basses éclairées.
- Tuile 1 se pose **juste en dessous** : arêtes hautes éclairées.
- Ne pas les utiliser ailleurs.

### `wall_<biome>_deco_L/R.png` — 64×32, 4 modules de 16×32

| Module | Crypte | Fonderie |
|---|---|---|
| 0 | lanterne froide (**source** : lit 0 au-dessus, lit 1 en dessous) | veilleuse en cage (**source**, même règle) |
| 1 | niche en ogive + urne | tuyau + volant de vanne |
| 2 | corniche + 3 bougies | haute grille + gouttes |
| 3 | plaque d'épitaphe | plaque emboutie |

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

Luminances visées :

| Plan | Y |
|---|---|
| P0 | 0.004-0.012 |
| P1 | 0.008-0.020 |
| P2 | 0.012-0.025 |
| Murs | autour de 0.06 |

Le héros et les pièges restent toujours plus clairs que les murs.

## Reste à faire côté décor

- bg0 et bg1 de la Fonderie et de la Bibliothèque. La maquette Fonderie a été jugée sur un aplat `k`.
- Murs et bg2 de la Bibliothèque. L'autel et la transition d'entrée sont déjà faits.
- Le bord des bandes bg2 est franc à x64/x128 : prévoir un pilier de bord ou laisser le code assombrir la dernière colonne.
