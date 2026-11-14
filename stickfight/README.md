# Stickfight

Base d'un jeu de combat de stickmen dans Godot. Cette première étape
fournit le **modèle** : un stickman riggé, des poses réglables au dixième de
degré, un atelier pour les composer à la souris ou au clavier, et un outil de
rendu en ligne de commande pour itérer sans ouvrir l'éditeur.

Le style vise celui des vidéos de référence : grosse tête ronde, trait gras à
bouts ronds, pas de pieds ni de mains dessinés. Les proportions mesurées
sur ces vidéos, les amplitudes articulaires et les notes sur l'animation de
combat sont dans [RECHERCHE.md](RECHERCHE.md). La liste des animations à
produire par personnage (communes et propres, d'après Tekken 8) est dans
[INVENTAIRE.md](INVENTAIRE.md).

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

## Animations

Le dossier `anims/` contient des animations par poses clés, jouées à
60 images par seconde (le format complet est décrit en tête de
`scripts/stick_anim.gd`).

| Animation | Durée | Contenu |
|---|---|---|
| `idle_repos` | 260 i, en boucle | Debout détendu : respiration lente, léger transfert de poids, deux paliers pour que la boucle ne se devine pas |
| `mise_en_garde` | 40 i | Du repos à la garde : anticipation (le corps se tasse), pas en avant, pied arrière qui glisse, poussière à chaque appui ; enchaîne sur `garde_idle` |
| `garde_idle` | 112 i, en boucle | Garde vivante : rebond sur les jambes, poings qui suivent avec 5 à 9 images de retard |
| `blocage_bas` | 44 i | Les mains descendent frapper le pied d'un coup visant le ventre, sans se baisser : armé (f4), contact (f8, arrêt sur impact 7 i, étincelle, secousse), écrasé, tenue, retour en garde |
| `coup_de_pied_ventre` | 56 i | Pied direct (teep) de la jambe avant, pour le duo : pas glissé, genou armé, contact (f17), pied rabattu vers le bas par le blocage, reprise de distance |
| `duo_blocage` | 110 i | Les deux ensemble : les contacts sont calés sur la même image globale |
| `sortie_de_garde` | 60 i | De la garde au repos, sur place : le poids bascule en arrière, le pied avant revient en se posant par la pointe, puis le pied arrière repasse devant et le bassin remonte ; les mains retombent le long du corps, le bras du pied qui avance passe devant (contrepoids) ; enchaîne sur `idle_repos` |
| `marche_detendue` | 56 i, en boucle, avance 76 | Marche normale depuis le repos, sans garde : bras ballants en opposition des jambes, bassin qui monte et descend sur chaque appui |
| `marche_detendue_depart` | — | Du repos à la boucle : transfert de poids, premier pas plus court |
| `marche_detendue_arret_court`, `_arret_pas` | — | Arrêts au repos depuis l'un ou l'autre pied de la boucle (pied ramené à côté de l'autre, ou un dernier pas freiné) |
| `marche_detendue_arriere` | 64 i, en boucle, recule 48 | Recul détendu : pas plus courts, la pointe se pose avant le talon, le buste reste droit |
| `marche_detendue_arriere_depart`, `_arret_pas`, `_arret_deux_pas` | — | Départ et arrêts au repos du recul détendu |
| `marche_arriere` | 30 i, en boucle, recule 14 | En garde maintenue. Plus lente et prudente : la jambe avant pousse, le bassin recule, le pied arrière se pose loin (la hanche ne s'étend pas au-delà de 30°, d'où ce bassin qui part avant le pied), puis le pied avant se ramène en glissant |
| `marche_avant` | 28 i, en boucle, avance 18 | En garde maintenue, pas chassé : le pied avant s'avance au ras du sol (4 de haut), le poids passe dessus, le talon arrière se lève et le pied arrière glisse ; garde serrée qui suit avec retard |

Une clé part d'une pose (`poses/`), applique des réglages (`plus`, `fixe`,
`vise` pour placer une main ou un pied en cinématique inverse), et choisit la
courbe du segment qui suit (`auto`, `lin`, `acc`, `dec`, `acc-dec`,
`palier`). Les pieds qui ne bougent pas entre deux clés restent plantés, et
le `decalage` retarde la tête et les avant-bras de quelques images
(chevauchement).

Une boucle qui fait avancer le personnage déclare son `avance` (en unités
par cycle) : chaque cycle reprend décalé d'autant, et le combattant
(`scripts/fighter.gd`) reporte ce déplacement dans sa position. Quand une
animation en remplace une autre, le bassin reste où il est arrivé.

Événements : `contact` (repère de synchronisation), `hitstop` (arrêt sur
impact global, la figure qui l'émet tremble), `etincelle`, `poussiere`,
`secousse` (caméra). Les effets (`scripts/vfx.gd`) sont dessinés en aplats,
palette de 4 couleurs, et changent d'image toutes les 2 images.

Un **duo** (`anims/duo_*.json`) place plusieurs combattants et leur programme :
`{"contact": 33, "anim": "blocage_bas", "fondu": 3}` démarre l'animation pour
que son événement `contact` tombe à l'image 33.

### Démo

`scenes/demo.tscn` (ouvrir la scène puis F6) joue les animations en direct :

Le repos est l'état par défaut ; la garde ne dure que tant que G est tenu.

| Touche | Effet |
|---|---|
| → ou ← maintenu | Depuis le repos : marche détendue avant ou arrière ; relâché, le pas en cours se termine et le combattant s'arrête au repos. La caméra suit |
| G maintenu | Mise en garde ; avec → ou ←, marche en garde ; relâché, sortie de garde et retour au repos |
| B | Blocage bas (en garde) |
| K | Duo coup de pied / blocage (en boucle) |
| R | Repos (remise à zéro) |
| Espace | Pause ; en pause, ← → reculent ou avancent d'une image |
| L | Ralenti ×4 |
| D | Squelette coloré |

### Régler une animation en ligne de commande

`tools/anim.sh` simule l'animation (ou le duo) avec le code du jeu et la
rend en images :

```sh
tools/anim.sh anims/blocage_bas.json -o /tmp/planche.png --de 0 --a 24
tools/anim.sh anims/blocage_bas.json --strobe /tmp/strobe.png --suivre handN,handF,head
tools/anim.sh anims/duo_blocage.json -o /tmp/duo.png --pas 2 --cols 7
tools/anim.sh anims/garde_idle.json --print          # articulations image par image
tools/anim.sh anims/duo_blocage.json --gif /tmp/duo.gif --video /tmp/duo.mp4
tools/anim.sh anims/duo_blocage.json --gif /tmp/lent.gif --lent 3
tools/anim.sh anims/marche_avant.json --strobe /tmp/marche.png --boucles 2
```

La planche contact montre chaque image numérotée ; la stroboscopie superpose
toutes les images avec la trajectoire des articulations suivies (un point
par image : des points serrés = lent, espacés = rapide), ce qui permet de
vérifier les arcs et l'espacement. `--print` sert à vérifier au dixième près
qu'un pied ne glisse pas ou qu'une main touche bien le pied adverse.

## Fichiers

```
project.godot
scenes/atelier.tscn       scène principale
scenes/demo.tscn          démo des animations
scripts/stick_rig.gd      squelette : FK, IK, amplitudes, dessin, JSON
scripts/planche.gd        fond, grille, sol, figures (partagé atelier / rendu)
scripts/atelier.gd        état, historique, panneau de réglages
scripts/atelier_scene.gd  poignées, souris, clavier
scripts/stick_anim.gd     animation par clés : courbes, pieds plantés, décalages
scripts/fighter.gd        un combattant : animation, fondus, traînées
scripts/combat.gd         plusieurs combattants, arrêt sur impact, effets, duo
scripts/vfx.gd            étincelle et poussière en aplats
scripts/demo.gd           scène de démo
tools/rendu.gd, rendu.sh  rendu PNG d'une pose
tools/anim.gd, anim.sh    planche, stroboscopie, GIF, vidéo d'une animation
poses/                    neutre, neutre-fin, repos, garde
anims/                    animations et duos
```

## Suite prévue

1. Timeline dans l'atelier : pelure d'oignon, déplacement des clés, réglage
   des courbes sans passer par le JSON.
2. Coups de poing (jab, direct) et coup de pied bas, avec boîtes de coup et
   de vulnérabilité attachées aux os.
3. Contrôle au clavier ou à la manette : déplacements, garde, blocage selon
   la hauteur du coup reçu.
4. Réactions aux coups reçus et enchaînements.
