# Stickfight

Base d'un jeu de combat de stickmen dans Godot. Cette première étape
fournit le **modèle** : un stickman riggé, des poses réglables au dixième de
degré, un atelier pour les composer à la souris ou au clavier, et un outil de
rendu en ligne de commande pour itérer sans ouvrir l'éditeur.

Le style vise celui des vidéos de référence : grosse tête ronde, trait gras à
bouts ronds, pas de pieds ni de mains dessinés. Les proportions mesurées
sur ces vidéos, les amplitudes articulaires et les notes sur l'animation de
combat sont dans [RECHERCHE.md](RECHERCHE.md).

## Lancer

1. Installer [Godot 4.3](https://godotengine.org/download/) (version standard,
   pas .NET).
2. Ouvrir `stickfight/project.godot` dans Godot, puis lancer le projet (F5).
   La scène principale est l'atelier.

## L'atelier

La planche est à gauche, le panneau de réglages à droite.

| Geste | Effet |
|---|---|
| Glisser une poignée **ronde** | Fait tourner l'os qui finit à cette articulation (coude → épaule, genou → hanche, épaule → poitrine, tête → cou, taille → bas du dos) |
| Glisser une poignée **carrée** (main, cheville) | Cinématique inverse : le bras ou la jambe suit la souris |
| Glisser le **bassin** (carré vert) | Déplace tout le corps ; avec « Pieds fixés », les jambes se replient pour garder les chevilles en place |
| **Ctrl** + glisser la taille | Bascule le bassin (tout le tronc s'incline) |
| Flèches | Ajuste l'élément sélectionné de 1 (Maj : 5, Alt : 0,1) ; sur un angle, ← → tournent ; sur une main ou une cheville, les quatre flèches la déplacent |
| `[` `]` | Articulation précédente ou suivante |
| Ctrl+Z, Ctrl+Y | Annuler, rétablir |
| Ctrl+S | Enregistrer la pose |

Couleurs des poignées : orange = membres proches (devant le tronc), bleu =
membres lointains (derrière), vert = tronc. Jaune = sélection.

Le panneau donne chaque angle avec un curseur et un champ numérique (deux
décimales). Il offre aussi :

- **Pieds fixés** : les pieds restent plantés pendant qu'on modifie le reste.
- **Amplitudes humaines** : bloque chaque articulation dans son amplitude
  réelle.
- **Fantôme** : garde la pose actuelle en rose derrière la figure pour comparer
  avant et après.
- **Retourner**, **Échanger proche / loin**, **Poser au sol**, **Neutre**.
- L'enregistrement dans `poses/<nom>.json`, et le JSON de la pose, modifiable
  et réapplicable.

## Rendu en ligne de commande

`tools/rendu.sh` dessine une ou plusieurs poses en PNG avec le même code de
dessin que l'atelier. C'est l'outil pour itérer finement : changer un angle,
regarder, recommencer.

```sh
export GODOT=/chemin/vers/Godot_v4.3-stable_linux.x86_64   # sinon « godot » du PATH
tools/rendu.sh poses/garde.json -o /tmp/garde.png --debug --grid
tools/rendu.sh poses/garde.json --set foreN+=3 --set chest-=2 -o /tmp/essai.png
tools/rendu.sh poses/garde.json --reach armN=40,140 --pin --save
tools/rendu.sh poses/garde.json poses/repos.json -o /tmp/compare.png
tools/rendu.sh poses/repos.json poses/garde.json --overlay -o /tmp/onion.png
tools/rendu.sh poses/garde.json --print     # angles, articulations, amplitudes dépassées
```

Toutes les options sont décrites en tête de `tools/rendu.gd`. Sans affichage,
le script passe par `xvfb-run`.

## Le modèle

- **Repère** : x vers l'avant du personnage, y vers le haut, sol à y = 0,
  unités ≈ cm. Un personnage debout mesure environ 180. La conversion vers le
  repère de Godot (y vers le bas) se fait seulement au dessin.
- **Os** (`scripts/stick_rig.gd`) : bassin → bas du dos → poitrine → cou ;
  deux bras (épaule, coude) et deux jambes (hanche, genou, cheville) attachés à
  la poitrine et au bassin.
- **Angles** : en degrés, mesurés depuis la position de repos (debout, bras le
  long du corps). Le signe est sémantique : positif = flexion ou vers l'avant.
  Le même nombre veut donc dire la même chose pour la jambe proche et la jambe
  lointaine, et les limites d'amplitude s'écrivent comme dans un tableau
  médical.
- **Proche / loin** : les membres proches (N) sont dessinés devant le tronc,
  les lointains (F) derrière.
- **Cinématique inverse** : analytique, deux os, par la loi des cosinus. Des
  deux solutions (coude en haut ou en bas), le solveur garde celle qui respecte
  les amplitudes, puis celle qui bouge le moins.
- **Styles** : `epais` (grosse tête, trait gras, celui des vidéos) et `fin`.
  Les longueurs de chaque style sont dans `STYLES`.

Format d'une pose (`poses/*.json`) :

```json
{
  "nom": "garde", "style": "epais", "x": 0, "y": 55, "facing": 1,
  "angles": { "root": 2, "spineLow": 6, "chest": 4, "neck": 6,
              "armF": 65.29, "foreF": 137.75, "armN": 38.96, "foreN": 112.7,
              "thighF": -16.57, "shinF": 33.49, "footF": 0,
              "thighN": 58.31, "shinN": 61.79, "footN": 0 }
}
```

`x`, `y` = position du bassin ; `facing` = 1 (regarde à droite) ou −1.

## Fichiers

```
project.godot
scenes/atelier.tscn       scène principale
scripts/stick_rig.gd      squelette : FK, IK, amplitudes, dessin, JSON
scripts/planche.gd        fond, grille, sol, figures (partagé atelier / rendu)
scripts/atelier.gd        état, historique, panneau de réglages
scripts/atelier_scene.gd  poignées, souris, clavier
tools/rendu.gd, rendu.sh  rendu PNG en ligne de commande
poses/                    neutre, neutre-fin, repos, garde
```

## Suite prévue

1. Poses clés et interpolation dans le temps : une animation est une liste de
   poses avec des durées en images (60 i/s), et des courbes d'accélération par
   segment.
2. Lecteur d'animation dans l'atelier : pelure d'oignon, image par image,
   timing des phases (préparation, impact, retour).
3. Premiers coups (jab, direct, coup de pied bas) avec boîtes de coup et de
   vulnérabilité attachées aux os, arrêt sur impact (hit-stop).
4. Deux personnages, déplacements, garde, puis enchaînements.
