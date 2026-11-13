# ÉCHO

Jeu mobile Android en pixel art : un grimpeur rebondit de mur en mur dans une tour piégée.
Chaque vie perdue laisse un écho qui neutralise le piège responsable. Conception : [DESIGN.md](DESIGN.md).

## Essayer le jeu (téléphone Android)
1. Sur le téléphone, ouvrir ce dépôt sur GitHub (branche `ccr-cf4637c9-gcz8o6`), aller dans `jeu/build/`,
   ouvrir `echo.apk` puis **Download raw file**.
2. Ouvrir le fichier téléchargé. Android demande d'autoriser l'installation depuis le navigateur : accepter.
3. Lancer **ÉCHO**.

Commandes : taper n'importe où = sauter vers l'autre mur. Taper en l'air = demi-tour. Bouton retour = pause / retour.

Les pubs sont **simulées** dans cette version (écran de 3 s, rien n'est affiché ni payé).

## Organisation
| Dossier | Contenu |
|---|---|
| `game/` | Projet Godot 4.5 (ouvrir `game/project.godot`). |
| `game/scripts/` | `main.gd` (écrans, déroulé), `world.gd` (jeu), `tower.gd` (génération), `ui_kit.gd` (UI pixel), `ads.gd` (pubs), `game_state.gd` (sauvegarde, textes FR/EN), `sfx.gd`. |
| `game/tests/` | `shot_driver.gd` (captures de tous les écrans), `bot_test.gd` (robot qui vérifie que les tours sont franchissables). Exclus de l'APK. |
| `art/` | Cahier des charges graphique, sources pixel `.txt` (1 caractère = 1 pixel), planches de contrôle. |
| `tools/` | `px.py` (rend une grille en PNG), `planche.py`, `font.py` (police bitmap), `sfx.py` (sons synthétisés), `palette.txt`. |
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
