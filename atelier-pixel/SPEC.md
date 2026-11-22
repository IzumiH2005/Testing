# Atelier Pixel : spécification (à valider avant tout code)

Statut : **proposition**. Rien n'est construit tant que cette spec n'est pas validée.

## 0. En une phrase

Un éditeur de pixel art complet, responsive et professionnel, publié en artifact, où Claude
**dessine à la souris, geste par geste**, regarde après chaque trait et se corrige tout de
suite. La méthode `METHODE_PIXEL_ART.md` est intégrée à la fois comme aide et comme
garde-fou : elle découpe le travail en étapes et bloque le passage tant qu'une étape ne
tient pas. Chaque séance est enregistrée et se revoit en vidéo.

## 1. Deux usages, une même application

| | Toi (humain) | Claude |
|---|---|---|
| Où | l'artifact publié, sur téléphone, tablette ou ordinateur | une copie locale de la même page, pilotée par un navigateur sans écran |
| Comment | souris, stylet, doigts, clavier | une **souris virtuelle** et un clavier virtuel, rien d'autre |
| Méthode | portes d'étape conseillées, désactivables | portes d'étape **toujours bloquantes** |
| Résultat | ton dessin, exportable | le dessin **et** la vidéo de la séance, que tu revois dans l'artifact |

Le même fichier `app/index.html` sert aux deux. Le mode Claude s'active par l'adresse
(`?mode=claude`) et ajoute un curseur visible, le journal strict et les contrôles d'intégrité.

## 2. Ce que les meilleurs éditeurs ont, et qu'on reprend

Recherche faite sur Aseprite, Pro Motion NG, Pyxel Edit, Pixelorama, Piskel, Resprite,
Pixquare, Pixel Artistry, PixelLab (liste Lospec en point de départ).

### 2.1 Outils de dessin
- **Crayon pixel-perfect** (supprime les « L » pendant le trait, comme Aseprite), taille
  1 px par défaut, pinceaux carrés ou ronds de 1 à 8 px, pinceau personnalisé pris dans une
  sélection.
- **Gomme**, même réglages.
- **Ligne** avec aperçu, affichage de la pente (« 2:1 », « 3:1 ») et **pentes propres
  forcées** au choix (A8) ; Maj + clic trace depuis le dernier point (geste Aseprite) ;
  angle parfait au choix (Pixquare).
- **Rectangle, ellipse** pleins ou creux ; ellipses construites en marches régulières (A5-6),
  avec les cercles propres de 8, 16, 32 px de G1.
- **Pot de peinture** contigu ou global, tolérance 0 par défaut.
- **Pipette** (Alt, ou appui long au doigt) ; clic droit = couleur secondaire.
- **Encre d'ombrage** (Shading ink d'Aseprite, Shading de Pixelorama) : clic gauche monte
  d'un ton dans la rampe, clic droit descend. Mode simple et mode glissement de teinte.
- **Verrou alpha** : on ne peint que sur les pixels déjà opaques du calque (indispensable
  pour ombrer une silhouette sans déborder).
- **Tramage** : motifs 25 / 50 / 75 % et Bayer 4×4, appliqués par le crayon (A7-B).
- **Remplacer une couleur** partout dans le calque ou l'image.
- **Symétrie** horizontale, verticale ou les deux, axes déplaçables (Pixelorama).
- **Sélection** rectangle, lasso, baguette magique ; déplacer, copier, retourner,
  **rotation RotSprite** (toujours depuis l'original, E7) puis nettoyage à la main.
- **Décalage cyclique** du calque (wrap) pour travailler les raccords de tuile.

### 2.2 Palette et couleur
- Mode **indexé** (palette imposée) ou RVB ; un clic sur une couleur de la palette change
  tous ses pixels si on le demande.
- **Constructeur de rampe** (A6-A) : nombre de tons, rotation de teinte (environ 20° par
  ton, C10-F), courbe de saturation et de luminosité, **rampes qui partagent leurs tons
  sombres**. L'outil propose, tu valides chaque couleur.
- **Budget de couleurs** par taille (A3, C10-A, C11-B) : compteur visible, alerte au dépassement.
- **Masque de gamme** (F4) sur une roue chromatique.
- Vue **gris** de la palette : contrôle que les tons d'une rampe se séparent en valeur.
- Import d'une palette Lospec par copier-coller des codes hex ou par fichier `.hex` ou `.gpl`.
  Le chargement direct depuis le site est bloqué par la page.
- **Cycle de palette** (E7) en aperçu.

### 2.3 Calques et construction
- Calques avec visibilité, verrou, opacité, mode de fusion normal, groupes, renommage.
- **Calques de construction** rouge (pose), bleu (repères), vert (volumes) de C13-A,
  jamais exportés, masqués automatiquement aux étapes finales.
- **Pile fixe d'animation** E6 proposée d'un clic : `ref, ombre, arriere_*, corps, avant_*,
  fx, eclat, pivot`. Les calques `ref` et `pivot` ne sont jamais exportés.
- **Image de référence** à côté du canevas ou en calque semi-transparent.
- **Fenêtre d'aperçu** permanente à ×1 et ×2. Elle répond à la règle 1 : « ce qui ne se
  lit pas à ×1 n'existe pas ».

### 2.4 Animation (partie E)
- Images avec **durée propre en ms**, option multiples de 16,7 ms (GBA, E2-A) ; tenues.
- **Étiquettes** (tags) et boucles avant, arrière, aller-retour.
- **Cels liés** (E6).
- **Pelure d'oignon** de 1 à 2 images, rouge avant et bleu après, environ 30 %, limitée à
  l'étiquette (E7).
- **Feuille de timing** éditable (E3) : colonnes Image, Rôle, Ce qui change, Principe,
  Durée. Elle se remplit avant de dessiner et sert de garde-fou (règle 26).
- Lecture aux vraies durées, bande d'images, ébauche en silhouette (E7-A).

### 2.5 Tuiles et décors (partie F)
- **Mode tuilé** : on dessine sur une tuile et on voit la grille 3×3 en direct (F2-A).
- **Tilemap** : un jeu de tuiles et une carte. Modifier une tuile met la carte à jour (Pyxel Edit).
- **Autotile** : 4 pièces dessinées à la main sont assemblées en blob 47 ou Wang 16. L'outil
  assemble, il ne dessine rien (partie D).
- **Aperçu de parallaxe** de 2 à 4 couches, vitesses entières et contrôle de couture (F3).
- **Carte dézoomée** 20×12 tuiles à ×1 (F6).

### 2.6 Export
- PNG à ×1 ou agrandi par un entier seulement (F3-C) ; GIF ; vidéo WebM.
- **Planche de sprites** : cellule fixe prise sur la plus grande boîte, même pivot, données
  JSON à côté ; tailles OAM GBA proposées (E8).
- Fichier projet `.atelier` (tout le document plus le journal), palette `.hex` ou `.gpl`.
- Les fichiers se donnent par la fenêtre d'enregistrement de claude.ai. Les liens de
  téléchargement classiques sont bloqués dans un artifact.

### 2.7 Mobile et tactile (Resprite, Pixquare, Procreate)
- **Téléphone** : canevas plein écran, barre d'outils en bas, panneaux qui montent du bas.
  **Tablette** : outils sur un côté, calques et palette repliables.
  **Ordinateur** : outils à gauche, panneaux à droite, timeline en bas.
- 1 doigt dessine ; 2 doigts déplacent et zooment ; tape à 2 doigts annule, tape à 3 doigts
  rétablit ; appui long = pipette.
- **Mode stylet** : seul le stylet dessine et les doigts naviguent (rejet de la paume).
- **Curseur de précision** (pavé de geste à la Pixquare) : le doigt pilote un curseur décalé
  et un bouton pose le pixel. C'est la seule façon d'être précis au pixel sur un téléphone.
- Touches Maj, Alt et Ctrl à l'écran, maintenues d'un tap.
- Cibles tactiles d'au moins 48 px, thème clair et sombre, interface en français.

## 3. Ce qui rend l'atelier unique : Claude dessine vraiment

### 3.1 Le principe
Aujourd'hui je pose des primitives par code (`trace.py`). Dans l'atelier, **je n'ai plus
d'accès direct aux pixels**. Je n'ai que ce qu'aurait un artiste :

- une souris : position, boutons gauche, droit et milieu, molette ;
- un clavier : raccourcis et touches de modification ;
- mes yeux : une capture après chaque geste.

Je dois donc choisir un outil, une couleur et un calque, viser, appuyer, glisser, relâcher,
puis regarder, comme on le ferait devant l'écran.

### 3.2 La souris virtuelle : commande `souris`
Un petit serveur local (Node + Playwright, déjà installés) ouvre l'atelier dans Chromium et
garde la page ouverte entre deux commandes. La commande `souris` lui envoie un geste à la fois.

| Commande | Ce qu'elle fait |
|---|---|
| `souris va 12 8` | amène le curseur sur la case (12, 8) du canevas ; sur l'écran : `va @640 300` |
| `souris pas 1 0` | déplace d'une case, pour un ajustement fin |
| `souris appuie [gauche\|droit\|milieu]` / `souris relache` | presse ou relâche le bouton |
| `souris clic`, `souris double` | clic simple ou double |
| `souris trace 12,8 13,8 14,9 …` | un seul trait main levée, bouton tenu, qui passe par ces cases |
| `souris glisse 3,3 10,7` | appuie, glisse et relâche : ligne, rectangle, déplacement de sélection |
| `souris molette -3` | zoom ou défilement |
| `souris tiens maj` / `souris lache maj` | maintient une touche de modification |
| `souris touche b`, `souris touche ctrl+z` | raccourci clavier |
| `souris survole @x y` | survol, pour lire une info-bulle |
| `souris regarde` | les yeux, voir 3.3 |
| `souris etat` | lecture seule : outil, couleur, calque, étape, case sous le curseur |

Pendant un trait (bouton tenu), `regarde` montre l'**aperçu avant de relâcher**, et
`touche echap` annule le trait sans rien poser. On peut ainsi viser, vérifier, puis
confirmer ou renoncer.

### 3.3 Les yeux : ce que renvoie `souris regarde`
Des images que je lis en mode vision :
1. **L'écran entier**, tel que tu le verrais.
2. **Une loupe** de 15×15 cases autour du curseur, très agrandie, avec la grille, les
   numéros de cases et le curseur en croix. C'est elle qui permet de viser au pixel.
3. **Le dessin à ×1 et à ×2**, pour juger la lecture réelle.
4. Un **texte court** : case sous le curseur, couleur, outil, calque, étape, et les défauts
   détectés près du curseur (voir 4.3).

### 3.4 Ce qui m'oblige à travailler comme un artiste
- **Aucune commande ne pose de pixels en masse.** Le serveur refuse tout script qui modifie
  la page. Il ne transmet que des événements de souris et de clavier, plus des lectures.
- **Regarder avant de recommencer** : après chaque trait relâché, `souris appuie` est refusé
  tant que je n'ai pas fait `regarde`. Un trait raté se voit donc au trait suivant au plus
  tard, et je l'annule ou le corrige tout de suite.
- **Contrôle d'intégrité** : à chaque porte d'étape, l'atelier rejoue tout le journal des
  gestes sur un document vierge et compare le résultat pixel par pixel. Un pixel arrivé
  autrement que par un geste rend la séance « non conforme », et c'est écrit dans la vidéo.
- **Une seule taille de trait à la fois** : `trace` est un trait continu, pas une liste de
  formes. Un remplissage passe par le pot de peinture, avec un clic.

### 3.5 Adaptation des règles 1 à 3 de la méthode
Les règles impératives 1 à 3 supposent un dessin écrit en fichiers de commandes
(`cXX.txt`). Dans l'atelier :
- **règle 1** (une étape = un fichier regardé à ×1) devient : une étape = un **jalon**
  (instantané PNG plus planche), regardé à ×1 avant la porte ;
- **règle 2** (décide chaque pixel) devient littérale : chaque pixel vient d'un de mes gestes ;
- **règle 3** (garder la trace) : le journal des gestes **est** la trace. Pour corriger, on
  annule et on redessine, et tout reste dans le journal.

Le reste de la méthode s'applique tel quel.

## 4. La méthode intégrée

### 4.1 Fiche d'intention (étape 0, obligatoire en mode Claude)
Avant le premier pixel, un formulaire :
- sujet et usage ;
- taille de toile ;
- vue et projection (A9, B0b) ;
- côté de la lumière ;
- budget de couleurs, prérempli depuis A3, C10-A ou C11-B selon la taille ;
- **type de travail** : objet, personnage, chibi, créature, vêtement, tuile, scène, animation.

Le type choisit le **parcours d'étapes** :

| Type | Parcours (sections de la méthode) |
|---|---|
| Objet | B6-A en 9 étapes : forme de base → déformer → trait et aplats → ombrage de base → secondaires → éclats et selout → contre-jour → variation de teinte → détails et nettoyage → planche |
| Personnage | C0 → proportions → pose → volumes → visage (C12) → vêtements → cheveux → silhouette → contour → palette → ombres → détails → nettoyage → planche |
| Chibi | C13-B + C14 : construction R/B/G → corps nu → ombres du corps → **validation du corps** → vêtements en calque → visage → cheveux en calque → accessoires → nettoyage → planche |
| Créature | C15 et C16 : langage de formes → construction → silhouette refaite tant qu'elle forme un bloc → contour → volumes → bords intérieurs → yeux → selout → planche |
| Vêtement | C17-I : appuis et tensions → poids → silhouette → aplat 1 px hors du corps → ombre et AO → plis → lumière → motif → contour du calque → détails |
| Tuile, décor | F : vue et taille → hiérarchie → palette du lieu → gabarit → petite carte → texture → variantes → autotile → fonds → parallaxe → contrôle F6 |
| Animation | E0 : intention → poses de départ et d'arrivée finies → feuille de timing → découpe en calques → ébauche en silhouette → chaque image passe par tout le pipeline → séquence |

### 4.2 Portes d'étape
Chaque étape affiche ce qu'on fait et ce qu'on **ne fait pas encore** (colonnes de B6-A).
- **Outils limités par étape.** À l'étape silhouette, une seule couleur. Avant la lumière,
  pas d'encre d'ombrage. Pas de nouvelle couleur hors budget. Le contour reste neutre
  jusqu'à l'étape selout (règle 39).
- **Pour passer la porte** :
  1. les détecteurs automatiques de l'étape ne signalent rien de bloquant ;
  2. j'ai regardé la planche de l'étape ;
  3. j'ai répondu à la checklist de l'étape, tirée de la méthode (A5-11, B5, C8, C10-K,
     C13, E5, F6…) ;
  4. le contrôle d'intégrité passe.
- Un jalon est enregistré à chaque porte : PNG, planche et réponses. Ce sont les chapitres
  de la vidéo.
- **Revenir à l'étape fautive** (règle 4) se fait d'un clic. Les étapes suivantes sont
  invalidées et devront repasser leur porte.

### 4.3 Détecteurs de défauts (A6-H)
Ils **signalent, ils ne corrigent jamais**. Chaque signalement est un repère sur le canevas,
avec la règle et la correction tirées du doc.

| Défaut | Détection |
|---|---|
| Doubles en « L » | coin de 3 pixels dans un trait d'1 px |
| Jaggies | suite de longueurs de marches irrégulière sur une courbe ou une diagonale |
| Banding | bandes de tons parallèles au même bord, avec les mêmes marches |
| Ombrage coussin, ombrage « flash » | répartition des tons qui suit le contour sans direction de lumière |
| Orphelins, bruit | pixels isolés, part des clusters de 1 à 2 px |
| Tramage décoratif | damier hors des conditions de A7-A, plusieurs styles de trame |
| Super pixels | blocs répétés de 2×2 ou 3×3 qui trahissent un agrandissement |
| Trop de couleurs | compte face au budget ; test « une couleur de moins » |
| Valeurs | tons d'une rampe trop proches en gris ; matières qui se confondent en gris |
| Contour noir pur | contour en noir pur (C10-F) |
| Taille | règles de C10-A : pas de cou sous 32 px, 2 px entre les yeux à 16 px… |
| Tuile | couture en 3×3, motif qui se répète sur la carte dézoomée (F6) |

### 4.4 Planche (A5-11, A6-J)
Une vue qui montre en une fois : ×1, ×2, agrandi, gris, silhouette, fonds clair, moyen et
sombre, miroir, en situation (case d'inventaire, tuile, à côté d'un autre sprite), tuile
3×3, carte dézoomée, bande d'animation, pelure d'oignon, GIF aux vraies durées. En fin de
dessin, un **bilan** de 3 points réussis et 3 points à améliorer (A5-11).

### 4.5 Aide
- Le doc entier est intégré, avec recherche plein texte et sommaire. Une copie du fichier
  vit dans `atelier-pixel/` : aucun partage avec `methode-pixel-art/`.
- Un **panneau contextuel** montre les sections et les règles impératives de l'étape en
  cours, et les tableaux utiles (table par taille, recettes d'yeux, plis de Bridgman…).
- Chaque détecteur et chaque porte renvoie à la section du doc concernée.

## 5. Enregistrement et vidéo

- **Journal** de chaque séance : tous les gestes horodatés (position, bouton, touche), les
  changements d'outil, de couleur et de calque, les annulations, les portes passées.
- **Lecteur intégré** dans l'artifact :
  - lecture en accéléré (×1 à ×64) et barre de défilement ;
  - curseur fantôme et cercle à chaque clic ;
  - chapitres aux portes d'étape ;
  - **corrections marquées en rouge** sur la frise, aux annulations et aux traits effacés.
- **Vidéos**, deux formes :
  1. la vidéo brute de la séance, filmée par le navigateur de Claude (Playwright) ;
  2. un timelapse WebM ou GIF exporté depuis le lecteur.
- **Pour que tu les regardes** : chaque séance est enregistrée dans `atelier-pixel/seances/`
  et publiée avec l'artifact. L'onglet « Séances de Claude » les liste et les rejoue. La
  vidéo t'est aussi envoyée directement dans la conversation.

## 6. Architecture

```
atelier-pixel/
├── README.md
├── SPEC.md                 ce fichier
├── CLAUDE.md               règles de travail de Claude dans l'atelier (protocole 3 et 4)
├── METHODE_PIXEL_ART.md    copie du doc, source de l'aide
├── app/
│   └── index.html          l'application entière (HTML, CSS et JS sans framework, canevas 2D)
├── souris/
│   ├── serveur.mjs         navigateur Playwright persistant, filme la séance
│   └── souris.mjs          la commande `souris`
├── seances/                journaux, jalons et vidéos des séances de Claude
└── tests/                  tests des outils, des détecteurs et du rejeu
```

- Une seule page HTML, sans dépendance réseau sauf deux bibliothèques épinglées sur cdnjs
  (rendu du Markdown de l'aide, encodeur GIF), ou écrites en interne si besoin.
- Brouillon enregistré dans le navigateur (localStorage, en secours), et fichiers `.atelier`
  à enregistrer et rouvrir. Rien de partagé entre visiteurs dans cette version.
- Capacité d'artifact utilisée : `downloads`, pour les exports.

## 7. Plan de construction

| Phase | Contenu | Validation |
|---|---|---|
| 1. Noyau | canevas, zoom, grille, crayon pixel-perfect, gomme, ligne, formes, pot, pipette, palette, calques, annuler, aperçu ×1, responsive de base | captures téléphone, tablette, ordinateur |
| 2. Souris et enregistrement | serveur, commande `souris`, loupe, aperçu avant relâche, verrou « regarder d'abord », journal, lecteur, vidéo, contrôle d'intégrité | je dessine une potion 16×16 à la souris, tu regardes la vidéo |
| 3. Méthode | fiche d'intention, parcours, portes, détecteurs, planche, aide contextuelle, constructeur de rampe, budget | un objet complet en 9 étapes (B6) |
| 4. Outils pro | encre d'ombrage, verrou alpha, tramage, symétrie, sélections, RotSprite, remplacer une couleur, indexé, masque de gamme | un personnage chibi 32 px (C13 + C14) |
| 5. Animation | images, durées, étiquettes, oignon, cels liés, feuille de timing, export planche et GIF, OAM GBA | un cycle d'attente de 4 images (E7) |
| 6. Tuiles et décors | mode tuilé, tilemap, autotile, parallaxe, carte dézoomée | un tileset 16 px avec autotile |
| 7. Finition mobile | gestes, mode stylet, curseur de précision, touches à l'écran | tests tactiles émulés |

Chaque phase est publiée, commitée et poussée. Tu peux corriger le tir à chaque phase.

## 8. Limites honnêtes

- Le dessin de Claude reste plus lent qu'avec `trace.py` : c'est le prix du geste. Une
  potion 16×16 demande environ 100 à 200 gestes.
- La précision vient de la loupe et de la case visée. Je ne « sens » pas la main, je vise des cases.
- Les détecteurs sont des heuristiques : un signalement peut être faux. La porte me demande
  alors de justifier mon choix par écrit au lieu de l'ignorer.
- Je ne pilote pas l'artifact publié sur claude.ai (il faut être connecté). Je travaille
  sur la copie locale identique, puis je publie les séances avec l'artifact.
