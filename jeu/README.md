# ÉCHO

Jeu mobile Android en pixel art : un grimpeur rebondit de mur en mur dans une tour piégée.
Chaque vie perdue laisse un écho qui neutralise le piège responsable. Conception : [DESIGN.md](DESIGN.md).

## Essayer le jeu (téléphone Android)
1. Sur le téléphone, ouvrir ce dépôt sur GitHub (branche `ccr-cf4637c9-gcz8o6`), aller dans `jeu/build/`,
   ouvrir `echo.apk` puis **Download raw file**.
2. Ouvrir le fichier téléchargé. Android demande d'autoriser l'installation depuis le navigateur : accepter.
3. Lancer **écho-mounbole** (c'est le nom affiché sous l'icône ; le jeu s'appelle toujours ÉCHO).

Commandes : taper n'importe où = sauter vers l'autre mur. Taper en l'air = demi-tour. Bouton retour = pause / retour.

### Choisir son niveau de départ
Dans le menu, sous **ASCENSION LIBRE**, les flèches **← →** choisissent le niveau (biome) où commence l'ascension :
1 Crypte des Veilleurs (0 m), 2 Fonderie froide (150 m), 3 Bibliothèque noyée (350 m), 4 Jardin de cristal (600 m),
5 Clocher des vents (900 m), 6 Sommet céleste (1250 m). Le héros part accroché à l'autel d'entrée du biome ; le décor
du menu défile dans ce biome. Le choix est sauvegardé. La hauteur compte depuis le sol de la tour.
La **tour du jour** part toujours du sol (même épreuve pour tout le monde).

### Musique
`game/audio/music.ogg` (OGG Vorbis 96 kb/s, 2,5 Mo, 3 min 37, en boucle). Le **tempo suit la vitesse du grimpeur** :
vitesse moyenne lissée (1,2 s) → tempo de 0,85 (accroché, immobile) à 1,25 (enchaînement de sauts), lui-même lissé
(0,8 s, 0,35 par seconde au plus) pour éviter les à-coups. Le bus « Music » compense la hauteur (AudioEffectPitchShift) :
le morceau accélère sans devenir aigu. Hors jeu : menu à volume réduit et tempo normal ; pause étouffée (passe-bas)
et très basse ; vie perdue : le tempo retombe à 0,85 ; résumé : 0,92, volume réduit. Réglages : `scripts/sfx.gd`.
Le morceau n'est pas une création du projet : avant une publication sur le Play Store, il faut en avoir les droits.

### Icône
Pixel art 54 × 54 (grimpeur à l'écharpe qui quitte le mur, son écho cyan derrière lui, murs de la tour, marée de
Silence, éclats d'or), généré par `tools/icone.py` à partir du sprite `art/src/hero/player_jump.txt`.
Le preset d'export utilise `game/assets/icon/` (192 classique, adaptative 432 avant-plan / fond / monochrome) ;
`art/out/icone/` contient aussi toutes les densités `mipmap-*`, l'icône Store 512 et la planche de contrôle.

Les pubs sont **simulées** dans cette version (écran de 3 s, rien n'est affiché ni payé).

## Organisation
| Dossier | Contenu |
|---|---|
| `game/` | Projet Godot 4.5 (ouvrir `game/project.godot`). |
| `game/scripts/` | `main.gd` (écrans, déroulé), `world.gd` (jeu), `tower.gd` (génération), `ui_kit.gd` (UI pixel), `ads.gd` (pubs), `game_state.gd` (sauvegarde, textes FR/EN), `sfx.gd`. |
| `game/tests/` | `shot_driver.gd` (captures de tous les écrans), `bot_test.gd` (robot qui vérifie que les tours sont franchissables). Exclus de l'APK. |
| `art/` | Cahier des charges graphique, sources pixel `.txt` (1 caractère = 1 pixel), planches de contrôle. |
| `tools/` | `px.py` (rend une grille en PNG), `planche.py`, `font.py` (police bitmap), `sfx.py` (sons synthétisés), `icone.py` (icône de l'app), `palette.txt`. |
| `build/` | `echo.apk` prêt à installer. |

## Reconstruire
```bash
G=/chemin/vers/Godot_v4.5.1
cd game
$G --headless --import
$G --headless --export-release "Android" ../build/echo.apk   # keystore via GODOT_ANDROID_KEYSTORE_RELEASE_*
# captures d'écran de contrôle :
xvfb-run -a $G --path . --rendering-driver opengl3 -- --shots=/tmp/shots
# robot d'équilibrage :
$G --headless --path . -s tests/bot_test.gd
```
