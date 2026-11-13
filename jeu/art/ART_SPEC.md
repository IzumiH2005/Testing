# ÉCHO : cahier des charges graphique (v1)

## Le jeu en 5 lignes
Une tour verticale vue de face. Le héros, un petit grimpeur encapuchonné avec une écharpe rouge-corail,
rebondit d'un mur à l'autre (un seul doigt). Des pièges (pics muraux, scies, lasers) barrent la montée,
et une marée de « Silence » violette monte par en dessous. Quand il meurt sur un piège, son **écho**
(un fantôme cyan) grave ce piège : le piège devient cyan et inoffensif pour les vies suivantes.
Ambiance : nuit froide, pierre bleu-violet, chaleur seulement sur le héros et les éclats d'or.

## Règles absolues
- **Palette unique** : `jeu/tools/palette.txt` (déclarer `palette: shared`). Aucune autre couleur, sauf
  une couleur locale `= X #hex` justifiée par écrit dans le commentaire du fichier (à éviter).
- **Pas de brun, pas de blanc sale.**
- Lumière **en haut à gauche** partout.
- Contour : `k` (quasi-noir bleuté) ou selout (contour coloré plus sombre que l'aplat).
- Les pièges utilisent la rampe **danger** (`x X z Z`). Leur version gravée utilise la rampe **écho**
  (`q t c e`). Le joueur utilise la rampe **chaude** (`r R o a`). Les éclats la rampe **or** (`g G y`).
  Le décor reste dans la rampe **nuit** (`k b d n s m l p`) + mousse/violet en accent, avec un contraste
  plus faible que les éléments de jeu (le décor ne doit jamais se confondre avec un piège).
- Méthode obligatoire : `/root/.claude/uploads/8bb7e1e6-044c-5928-b326-6b9f703cc364/512a7bf0-METHODE_PIXEL_ART-2.md`.
  Lire les **règles impératives** (l. 47-131), la partie **A** (l. 133-570) et la partie utile à ton lot.
  Chaque pixel est décidé à la main dans un `.txt` (1 caractère = 1 pixel).

## Outils
- `python3 jeu/tools/px.py src.txt sortie.png` : rend la grille (écrit aussi `sortie@8.png` agrandi ×8).
- `python3 jeu/tools/planche.py sortie.png` : planche de contrôle (×1, ×2, gris, silhouette, fonds, miroir).
  Regarder la planche avec l'outil Read (il affiche les images), noter au moins un défaut, corriger.
- Format `.txt` (voir l'en-tête de `px.py`) :
  ```
  palette: shared
  size: 80x16        <- pour une bande de 5 images de 16x16, la grille fait 80 de large
  ---
  ....kkkk........ (etc.)
  ```
- Sources : `jeu/art/src/<lot>/*.txt`. Sorties finales : `jeu/game/assets/<lot>/<nom>.png`.
  Les `@8.png` et planches vont dans `jeu/art/out/<lot>/` (pas dans `game/assets`).

## Échelle
Écran logique 192×352 px (affiché ×3 à ×6 sur téléphone). Tuile 16×16. Le puits entre les murs fait 160 px.
Le héros tient dans 16×16 (silhouette ≈ 10×14). Bandes d'animation **horizontales**, images de même taille.

---

## LOT 1 : `sprites` (héros, pièges, collectibles)
Sorties dans `jeu/game/assets/sprites/` :

| Fichier | Taille | Contenu |
|---|---|---|
| `player.png` | 80×16 (5 images 16×16) | 0 accroché au mur GAUCHE (mur à sa gauche, il regarde vers la droite, mains/pieds contre le bord gauche de l'image) · 1 accroché, variante de glissade (écharpe qui flotte vers le haut) · 2 saut montant (groupé, écharpe traîne en bas-gauche) · 3 saut descendant (étiré) · 4 vrille en l'air (rebond inversé) |
| `death.png` | 80×16 (5 images) | le héros se dissout en volutes cyan (rampe écho) : choc blanc → éclatement → volutes → presque rien → 1 pixel |
| `saw.png` | 32×16 (2 images) | scie circulaire danger, diamètre ≈ 14, 2 positions de dents pour la rotation |
| `saw_echo.png` | 16×16 | la même scie gravée : rampe écho, fissurée, immobile |
| `spikes.png` | 16×16 | rangée de pics fixés au mur GAUCHE, pointes vers la DROITE, occupent les 7 px de gauche, couvrent toute la hauteur (se répètent verticalement sans raccord visible) |
| `spikes_echo.png` | 16×16 | mêmes pics gravés (écho, pointes émoussées) |
| `laser.png` | 48×16 (3 images) | émetteur fixé au mur GAUCHE, bouche vers la droite : éteint · en charge (lueur) · actif |
| `laser_echo.png` | 16×16 | émetteur gravé (écho) |
| `beam.png` | 24×8 (3 images 8×8) | segment de rayon horizontal qui se répète : préavis (fin, pointillé) · actif · actif variante (scintillement) |
| `shard.png` | 32×8 (4 images 8×8) | éclat d'or qui tourne |
| `shard_pop.png` | 32×8 (4 images) | étincelle quand on le ramasse |
| `tide.png` | 32×16 (2 images 16×16) | crête de la marée de Silence (se répète horizontalement) : violet `u U` avec écume `z`/`Z`, le bas de la tuile est plein `u` (le reste de la marée est rempli en `u` par le code) |
| `grave.png` | 8×8 | sceau cyan posé là où un écho est mort |
| `tap.png` | 32×16 (2 images) | doigt qui tape (aide du tutoriel), rampe nuit claire `p w` + contour `k` |

Parties de la méthode : C10 (personnage à 16 px), C13 (chibi), C15 (créatures/émissif pour les volutes), B (objets), E (animation, feuille de timing pour `death`, `player`, `saw`).

## LOT 2 : `env` (décor de la tour)
Sorties dans `jeu/game/assets/env/` :

| Fichier | Taille | Contenu |
|---|---|---|
| `wall.png` | 96×16 (6 tuiles 16×16) | colonne de mur GAUCHE ; la face intérieure (côté puits) est le bord DROIT de la tuile, éclairée (lumière haut-gauche → face légèrement plus sombre que le dessus des pierres). 0-3 variantes de pierres qui se raccordent verticalement entre elles · 4 avec mousse `v V` · 5 avec fissure. Le mur droit = miroir dans le code. |
| `back.png` | 112×16 (7 tuiles) | fond intérieur de la tour, **faible contraste** (`b d n` surtout, `s` en lumière) : 0-3 briques qui se raccordent dans toutes les directions · 4 fenêtre en arc avec ciel nocturne et une étoile `w` · 5 chaîne qui pend · 6 niche avec rune gravée `t` |
| `floor.png` | 48×16 (3 tuiles) | dalle de départ : bord gauche · milieu (se répète) · bord droit |
| `plaque.png` | 32×12 | plaque de pierre clouée (le code écrit la hauteur dessus, laisser un champ central uni `s` de 20×6) |

Le décor doit rester derrière : contraste bas, pas de pixels isolés, pas de motif qui crée une ligne horizontale forte (elle se lirait comme un laser).

## LOT 3 : `ui` (interface, police, logo, icône)
Sorties dans `jeu/game/assets/ui/` :

| Fichier | Taille | Contenu |
|---|---|---|
| `font.txt` (source) → `font.png` + `font.fnt` | voir ci-dessous | police bitmap capitales |
| `panel.png` | 24×24 | cadre 9-slice (marges 8 px) : fond `d`, bord pierre `s m` + contour `k`, coin à rivets |
| `panel_echo.png` | 24×24 | même cadre en version écho (bord `t c`) pour les écrans de mort/fin |
| `btn_main.png` | 48×24 (2 images 24×24) | bouton principal ambre (`R o a`, contour `k`) : normal · enfoncé (décalé de 2 px vers le bas, ombre réduite). 9-slice marges 6 |
| `btn_alt.png` | 48×24 | bouton secondaire pierre (`n s m l`) |
| `btn_echo.png` | 48×24 | bouton « vidéo récompensée » cyan (`q t c e`) |
| `icons.png` | 252×12 (21 icônes 12×12) | 0 vie (petite flamme-lanterne chaude) · 1 vie utilisée (fantôme écho) · 2 éclat · 3 jouer ▶ · 4 partager · 5 vidéo · 6 réglages · 7 son on · 8 son off · 9 retour · 10 trophée · 11 calendrier · 12 cadenas · 13 coche · 14 pause · 15 flamme de série · 16 vibration · 17 maison · 18 crâne · 19 couronne · 20 écharpe |
| `logo.png` | 128×40 | mot « ÉCHO » : lettres en pierre claire (`l p w`), avec un double décalé en cyan (l'écho) derrière, accent sur le É |
| `icon.png` | 32×32 | icône de l'application : le héros (écharpe corail) qui saute devant son écho cyan, fond `b`/`u` |

### Police (`font.txt`)
Format lu par `jeu/tools/font.py` :
```
cell: 6x10        <- cellule ; l'œil de la lettre fait 5 px de large max, 7 px de haut
baseline: 8       <- rangée de la ligne de base (0 = haut). Rangées 0-1 : accents. Rangées 2-8 : capitales. Rangée 9 : jambage (virgule)
color: w          <- couleur unique des glyphes (le code teinte ensuite)
== A
.....
.....
.###.
#...#
#...#
#####
#...#
#...#
#...#
.....
== B
...
```
Chaque glyphe : 10 lignes, largeur libre de 1 à 5 (toutes les lignes d'un glyphe ont la même largeur ;
la largeur détermine l'avance). `#` = pixel, `.` = vide. Espacement de 1 px ajouté automatiquement.
Glyphes requis : `A-Z 0-9 . , : ; ! ? ' " - + / % ( ) # × < > = _ * É È Ê À Â Ç Ô Û Ù Î Ï Ë` et l'espace
(`== SPACE`, largeur 3). Style : lisible à ×1 sur fond sombre, angles nets, pas de fioriture.
