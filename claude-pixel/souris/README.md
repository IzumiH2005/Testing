# La souris

C'est la seule façon dont Claude touche à l'atelier. Un serveur local ouvre `app/index.html`
dans Chromium (Playwright). Il garde la page ouverte entre deux commandes et filme toute la
séance. Il ne transmet à la page que des événements de souris et de clavier. Pour lire
l'état, il passe par `window.claudePixel`, un objet gelé en lecture seule. Aucune commande
n'exécute de script dans la page. Pour dessiner, Claude doit donc viser la bonne case,
cliquer, puis regarder ce qu'il a fait.

## Démarrer, envoyer, finir

```sh
node souris/souris.mjs demarre --id potion   # ouvre l'atelier et commence à filmer
node souris/souris.mjs va 3 4                # une commande
node souris/souris.mjs - < gestes.txt        # une commande par ligne, s'arrête au premier refus
node souris/souris.mjs cibles fichier        # les éléments cliquables dont le nom contient « fichier »
node souris/souris.mjs fin                   # ferme la séance et range la vidéo
```

Options de `demarre` :

| Option | Effet |
|---|---|
| `--id nom` | nom de la séance, et donc de son dossier `seances/nom/` (sinon : date et heure) |
| `--tel` | écran de téléphone, 390×844, au lieu de 1280×800 |
| `--humain` | ouvre l'atelier en mode humain : les portes conseillent au lieu de bloquer |
| `--port n` | port local, 4917 par défaut (ou `SOURIS_PORT`) |

Dans un fichier de gestes, les lignes vides et celles qui commencent par `//` sont ignorées.
Pour relancer après avoir modifié `serveur.mjs`, tuez le serveur
(`pkill -f souris/serveur.mjs`) et attendez environ 3 secondes avant `demarre`. Sinon, la
commande répond « déjà lancée » ou la connexion est coupée.

## Viser

Toutes les commandes qui prennent une position acceptent trois formes :

| Forme | Exemple | Vise |
|---|---|---|
| `x y` ou `x,y` | `va 12 8` | le centre de la case (12, 8) du dessin, quel que soit le zoom |
| `@x y` | `va @640 300` | un point de l'écran, en pixels |
| `=nom` | `clic =menu-fichier` | le centre de l'élément marqué `data-cible="nom"` |

Si un élément est hors de l'écran, la commande est refusée et invite à faire défiler son
panneau (`defile =nom`).

## Le geste

La souris bouge comme une main, pas comme une téléportation :

- **Déplacement** : la durée suit la loi de Fitts (un trajet long prend un peu plus de temps,
  sans jamais traîner), avec un départ et une arrivée en douceur (profil à jerk minimal) et
  une légère courbe de poignet. Le curseur arrive exactement sur la cible.
- **Bouton tenu** : pas de courbe. Un glisser ou un trait à main levée (`appuie`, `va`,
  `relache`) va droit.
- **Trait** (`trace`) : rapide sur une marche droite, un temps à chaque changement de
  direction, plus lent sur les deux dernières cases pour poser la fin juste.
- **Pauses** : courtes après un clic, une touche ou un cran de molette, juste assez pour que
  l'app réponde.

## Les commandes

**Bouger**

| Commande | Effet |
|---|---|
| `va pos` | déplace le curseur, sans cliquer |
| `survole pos` | comme `va`, puis attend 0,9 s pour laisser apparaître une infobulle |
| `pas dx dy` | décale le curseur de quelques cases (`pas 1 0` : une case à droite) |

**Cliquer et dessiner**

| Commande | Effet |
|---|---|
| `clic [droit\|milieu] [pos]` | un clic, sur place ou après être allé à `pos` |
| `double [pos]` | un double clic |
| `trace a b c…` | bouton enfoncé de la case `a` à la dernière, en passant par chaque point. Le chemin entre deux points suit Bresenham **case par case**, de centre en centre : une diagonale ne frôle jamais le coin d'une case voisine |
| `glisse a b` | glisser-déposer de `a` à `b` (cases `x,y` ou points `@x,y`) : déplacer une sélection, un calque, une image |
| `appuie [gauche\|droit\|milieu]` | enfonce un bouton et le garde |
| `relache` | relâche les boutons tenus |
| `molette n` | n crans de molette (négatif : vers le haut). Avec `tiens ctrl`, c'est le zoom |
| `defile =nom` | tourne la molette au-dessus du panneau jusqu'à ce que l'élément soit visible |

**Clavier**

| Commande | Effet |
|---|---|
| `touche k` | une touche ou un raccourci : `touche b`, `touche ctrl+z`, `touche echap`, `touche tab` |
| `tape "texte"` | tape le texte dans le champ qui a le focus |
| `tiens k` / `lache k` | garde enfoncée ou relâche `maj`, `ctrl`, `alt` ou `cmd` (ligne droite, angle contraint…) |
| `choisis =nom "option"` | ouvre la liste déroulante d'un clic, descend aux flèches jusqu'à l'option, valide par Entrée |

Noms de touches : `ctrl`, `maj`, `alt`, `cmd`, `echap`, `entree`, `espace`, `suppr`,
`retour`, `tab`, `haut`, `bas`, `gauche`, `droite`, `debut`, `fin`, `pgup`, `pgdn`. Une lettre
seule s'écrit telle quelle.

**Voir et lire**

| Commande | Effet |
|---|---|
| `regarde` | photographie l'écran, une loupe de 15×15 cases autour du curseur et le dessin exporté (×1, ×2, grand), puis résume ce qu'il voit |
| `etat [porte]` | l'état complet en JSON : curseur, boutons, outil, couleurs, calque, étape, porte |
| `cibles [filtre]` | les éléments cliquables visibles et leur position à l'écran |
| `attends ms` | attend, au plus 5 000 ms |
| `fin` | ferme la séance et enregistre la vidéo |

## La règle : regarder avant le trait suivant

Après un clic, un trait ou un glissé **sur la toile**, toute nouvelle action sur la toile est
refusée tant que Claude n'a pas fait `regarde`. Le refus arrête le fichier de gestes à cette
ligne. Les clics dans l'interface (outils, couleurs, panneaux) restent libres.

`regarde` écrit dans `seances/<id>/regards/` :

| Fichier | Contenu |
|---|---|
| `NNN-ecran.png` | l'écran tel que filmé |
| `NNN-loupe.png` | 15×15 cases autour du curseur, numérotées, défauts encadrés en rouge |
| `NNN-dessin.png` | l'export réel (sans calque de construction), à ×1, ×2 et grand |
| `NNN.txt` | le résumé texte, celui que la commande affiche |

Le résumé donne : la case et la couleur sous le curseur, l'outil et les couleurs actives, le
calque et l'image, l'étape de la méthode (ou « méthode terminée »), ce qui manque pour valider
l'étape (`porte`), les défauts détectés (avec ceux qui sont près du curseur), les messages de
l'atelier et les erreurs de page.

## Ce que produit une séance

```
seances/<id>/
├── commandes.txt     chaque commande avec l'heure, et chaque refus (✗)
├── regards/          les regards numérotés (voir plus haut)
├── fichiers/         ce que l'atelier fait télécharger (.claude-pixel.json, PNG, GIF…)
└── seance.webm       la vidéo, avec la flèche du curseur, un cercle à chaque clic et le
                      bandeau de la commande en cours
```

La flèche, les cercles et le bandeau sont dessinés par-dessus la page pour la vidéo. Ils ne
reçoivent aucun événement et ne modifient pas l'atelier.

## Exemple : un trait, puis le contrôle

```
// couleur du contour, posée en C1, puis le crayon
clic =onglet-couleurs
clic =hex
touche ctrl+a
tape "#2a1a2e"
touche entree
clic =selecteur-c1
clic =outil-crayon
// le bord du bouchon, regard, puis le goulot
trace 4,4 10,4
regarde
trace 5,3 5,2 6,1 8,1 9,2 9,3
regarde
```
