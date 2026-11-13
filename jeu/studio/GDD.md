# ÉCHO — Game Design Document v1.0

> Directeur de jeu : Milo Hartmann. Cible : Android portrait, APK, pixel art 2D, Godot 4.5.1 (gl_compatibility, GDScript).
> Ce document remplace `jeu/DESIGN.md` (v0.1) pour tout ce qui touche au gameplay. Le prototype (`game/scripts/world.gd`, `tower.gd`) reste la référence physique de départ.
> Couleurs : toutes les teintes citées viennent de `studio/palette_v2.txt` (lettre entre crochets, ex. [o]). Pas de marron, pas de blanc sale.

## 0. Conventions et unités

| Grandeur | Valeur | Raison |
|---|---|---|
| Écran logique | 192 × 352 px, mise à l'échelle entière (×3 sur 1080p, ×4 sur 1440p) | Pixels nets, aucun flou de rééchantillonnage. |
| Tuile | 16 × 16 px = **1 mètre** | Le score en mètres se lit directement en tuiles, ce qui simplifie l'édition des chunks. |
| Murs | gauche x = 0 → 32, droit x = 160 → 192 | Repris du prototype (`WALL_L=32`, `WALL_R=160`). |
| Couloir jouable | 128 px (8 tuiles) ; le centre du héros vole sur 116 px (accroche à 6 px de la face) | Valeur prototype validée par le robot de test. |
| Héros | visuel 8 × 12 px ; **hitbox létale 6 × 10 px** (−1 px par côté) | Clémence : on meurt de ce qu'on voit nettement toucher. |
| Temps | secondes ; simulation à pas fixe 1/120 s (`physics_ticks_per_second = 120`) | Un saut de 0,55 s fait 66 pas : arcs stables et identiques d'un appareil à l'autre, donc même graine = même tour. |
| Vue | caméra verticale ; le héros est maintenu à y = 220 px (62 % de la hauteur), soit 220 px visibles au-dessus et 132 px en dessous | On voit plus haut que bas : on lit ce qui arrive. |

Les **chiffres physiques** de la section 2 viennent d'un simulateur d'arcs (pas de 1/240 s) écrit pour ce document à partir des constantes de `world.gd`. Ils sont reproductibles.

---

## 1. Piliers et fantasme du joueur

**Fantasme.** *« Je suis le dernier Veilleur. Je remonte la tour avant que le Silence ne l'efface. Chaque fois que je tombe, ma chute grave la tour en lumière, et la fois suivante, elle me porte. »*

| # | Pilier | Ce qu'il impose | Test de validation (playtest) |
|---|---|---|---|
| P1 | **Un doigt, mille nuances** | Tout se joue d'un doigt : poser, tenir, retaper. Aucune commande ne dépend de la zone touchée ni d'un geste (swipe). | Un joueur qui n'a jamais joué réussit son premier saut en moins de 3 s, sans texte. Un joueur au niveau 20 peut citer au moins 3 façons de franchir un même passage. |
| P2 | **La mort écrit la tour** | Chaque mort rend la tour plus praticable pour les vies suivantes : piège gravé, fantôme, éclat d'écho. Mourir est une information, jamais une simple punition. | Après sa première mort, 80 % des testeurs savent dire ce que signifie le cyan. |
| P3 | **Toujours monter** | La marée de Silence interdit d'attendre gratuitement. Toute attente (laser, herse) a un coût mesurable en pixels de marge. | Aucune vie médiane ne dure plus de 120 s. |
| P4 | **Une tour, une histoire** | 4 vies sur la même graine. Le récit d'une ascension tient en une ligne partageable (« 612 m, 3 gravures, Fonderie »). | 30 % des parties du jour 1 se terminent sur l'écran de partage ou sur une relance immédiate. |

**Ce qu'ÉCHO n'est pas.** Ce n'est pas un runner à réflexes purs, puisque l'écho et les autels récompensent la mémoire. Ce n'est pas non plus un jeu à collection, puisque les reliques ne changent jamais la difficulté de plus de 10 %.

---

## 2. Verbes et physique

### 2.1 Les trois verbes

| Verbe | Geste | Effet | Statut | Raison |
|---|---|---|---|---|
| **Bond** | Poser le doigt quand le héros est accroché | Saut vers le mur opposé : vx = ±210, vy = −290 | Prototype, conservé | C'est le cœur lisible du jeu : un tap, un mur. |
| **Volte** (demi-tour) | Poser le doigt en l'air | vx s'inverse, vy = −205. **Une seule volte par bond.** Elle se recharge en touchant du cyan. | Prototype, enrichi | Seul moyen de rester du même côté : c'est la décision de base « je change de mur ou pas ». |
| **Élan** (saut long) | **Garder** le doigt posé après le bond | Après une zone morte de 0,10 s, la gravité passe à 300 tant que vy < 0, jusqu'à 0,28 s après le décollage | **Nouveau, P0** | Il crée la décision verticale « j'atterris haut ou bas sur le mur d'en face », qui manquait au prototype. Il ne coûte aucun geste nouveau, puisque tenir est le prolongement naturel de poser. |
| **Glisse** | Ne rien faire, accroché | Le héros tient 0,22 s, puis glisse à 14 px/s | Prototype | Seul moyen d'attendre, et il coûte de la hauteur (Stopping Mechanism). |

**Verbes refusés.**
- Le *swipe* (dash latéral) : un swipe commence par un toucher, qui déclencherait déjà une volte. C'est donc ambigu pour un doigt.
- Le *double-tap* (super-saut) : il entre en conflit avec la volte, qui se déclenche à la pression, et il ajouterait 150 ms de latence d'attente.
- Le *tap gauche/droite* (zones d'écran) : il casserait P1 (« le doigt peut être n'importe où »), et en portrait le pouce masque la moitié basse.

### 2.2 Paramètres physiques (valeurs de référence P0)

| Paramètre | Valeur | Raison en une ligne |
|---|---|---|
| Gravité `GRAV` | 700 px/s² | Prototype. Elle donne un arc de 0,55 s, assez court pour le rythme, assez long pour la volte. |
| Bond `JUMP_VX / JUMP_VY` | 210 / −290 px/s | Prototype. Il couvre 116 px en 0,554 s. |
| Volte `TURN_VY` | −205 px/s | Testé à −130, −150, −170 et −205 : seul −205 garde une volte tardive (0,5 s) utile, avec un gain de +70 px. |
| Élan : zone morte | 0,10 s | Un tap rapide (≤ 0,08 s mesuré sur pouce) donne exactement le bond de base. Pas d'Élan accidentel. |
| Élan : gravité réduite | 300 px/s² entre 0,10 s et 0,28 s, et seulement si vy < 0 | Gain de +26 px maximum (+50 %) : visible sans casser les chunks. |
| Chute max `MAX_FALL` | 330 px/s | Prototype. On lit encore les pièges pendant une chute. |
| Accroche `GRIP_TIME` puis glissade `SLIDE` | 0,22 s, puis 14 px/s | Prototype. Accrocher est confortable, attendre longtemps coûte. |
| **Coyote** | 0,10 s après la rupture d'une paroi friable, la fin d'un segment de mur, un givre ou un cristal | La paroi qui cède ne doit pas « voler » le tap. Celeste utilise un ordre de grandeur comparable (5-6 frames). |
| **Buffer de bond** | Une pression dans les 0,08 s (≈ 17 px) **avant** de toucher un mur devient un bond, pas une volte | C'est le cas d'erreur le plus fréquent au prototype : volte gâchée juste avant l'impact. |
| Pression ignorée | Une pression en l'air, volte déjà utilisée et hors fenêtre de buffer, est ignorée (petit « tic » sonore, aucun effet) | Pas d'action fantôme ; le son confirme que l'entrée a été lue. |
| Hitbox létale | 6 × 10 px (visuel 8 × 12) | Clémence de 1 px par côté. |
| **Frôlé** | Passer à 3 px ou moins d'une hitbox létale sans la toucher | Donne +1 éclat, un ralenti de 0,08 s à ×0,5 et un « ting » aigu. Il récompense la prise de risque (boucle risque/récompense). |

### 2.3 Arcs mesurés (simulateur, couloir standard de 116 px)

| Cas | Durée de vol | Gain de hauteur à l'impact | Apex | Lecture |
|---|---|---|---|---|
| Bond de base | 0,554 s | **+52 px (3,3 tuiles)** | 59,5 px | Atterrit 3 tuiles plus haut. |
| Élan complet (tenir ≥ 0,28 s) | 0,554 s | **+78 px (4,9 tuiles)** | 79 px | Atterrit 5 tuiles plus haut. |
| Élan tenu 0,12 s | 0,554 s | +55 px | — | Tenir peu change peu : c'est progressif. |
| Élan tenu 0,20 s | 0,554 s | +68 px | — | |
| Tap de 0,08 s | 0,554 s | +52 px | — | Identique au bond : la zone morte fonctionne. |
| Volte à 0,1 s | retour en 0,21 s | +45 px | — | Volte « sèche » : remonte presque sur place. |
| Volte à 0,2 s | retour en 0,40 s | +70 px | — | |
| Volte à 0,3 s | retour en 0,60 s | **+85 px** | — | Volte optimale en hauteur. |
| Volte à 0,4 s | retour en 0,81 s | +84 px | — | |
| Volte à 0,5 s | retour en 1,01 s | +70 px | — | Volte tardive : longue, utile pour laisser passer une scie. |
| Élan + volte à 0,3 s | retour en 0,60 s | **+92 px** | — | Le plus haut gain possible sans cristal. |
| Couloir étroit 96 px | 0,40 s | +59 px (Élan +74) | — | Les rétrécissements accélèrent le rythme. |
| Couloir large 160 px | 0,71 s | +29 px (Élan +66) | — | Les élargissements rendent l'Élan presque obligatoire. |
| Cristal (vy −340) | 0,554 s | +80 px | — | Équivalent d'un Élan imposé. |
| Eau (g = 300) | 0,554 s | +114 px | — | Flottaison : deux fois la hauteur d'un bond. |

**Conséquence pour l'édition des chunks.** Depuis un mur, trois hauteurs d'atterrissage « canoniques » existent : **+3 tuiles (bond), +5 tuiles (Élan), +5 à +6 tuiles du même côté (volte)**. Les zones sûres sont réparties à environ **40 % bond, 40 % Élan, 20 % volte**, pour qu'aucun verbe ne devienne dominant.

### 2.4 Game feel (Swink : entrée, réponse, contexte, polish)

- **Bond.** Écrasement de 2 frames à l'impulsion (10 × 10 px), étirement de 3 frames en vol (6 × 14). Poussière de 3 px [p] côté mur. Son « tok » dont la hauteur monte avec le combo Rythme.
- **Élan.** L'écharpe [o] s'allonge de 2 px et une traînée de 4 frames [a] apparaît. Un souffle doux tant que la gravité réduite est active, ce qui rend visible l'effet du doigt tenu.
- **Volte.** Une étincelle [G] de 5 px au point de demi-tour et un « swish » inversé. Quand la volte est rechargée par du cyan, l'étincelle devient [c].
- **Mort.** Hitstop de 0,18 s, secousse de 4 px, puis gravure après 0,63 s (animation de 0,7 s, détaillée en section 3). Valeurs du prototype conservées.
- **Combo Rythme.** Il augmente de 1 à chaque bond enchaîné après moins de 0,30 s passées sur le mur, et revient à 0 après une accroche plus longue. Paliers 10/20/30 : +2/+4/+6 éclats et une note de carillon. Équivalent de la boucle risque/récompense de Downwell : aller vite rapporte, mais ne pas lire tue.

---

## 3. L'Écho : le système central

### 3.1 La règle en 5 secondes

> **« Ce qui t'a tué devient cyan. Le cyan ne tue pas. Le cyan recharge ta volte. »**

C'est tout ce que le joueur doit savoir. Il le découvre par l'usage (section 11) et un seul pictogramme le résume : un losange cyan [c] avec une flèche de volte.

### 3.2 Composants

| Composant | Règle exacte | Raison |
|---|---|---|
| **Gravure** | À la mort, l'instance de piège responsable (ou toute la bande d'épines, ou tout le laser) devient cyan [t/c/e] pour **le reste de l'ascension**. Elle n'a plus de hitbox létale. | C'est le cœur du jeu : chaque échec ouvre la tour. |
| **Recharge cyan** | Toucher en l'air n'importe quel élément cyan (piège gravé, éclat d'écho, fantôme) recharge la volte. Une seule recharge par élément et par bond. | Le cyan devient une ressource active, pas seulement un trou dans la difficulté. Il crée des routes nouvelles. |
| **Règle du complice** | Si un élément **non létal** (paroi friable, givre, cristal, vent) a été touché dans la seconde qui précède la mort, il est gravé aussi. Une paroi friable gravée devient solide, un givre gravé devient accrochable, un cristal gravé ne rebondit plus, une bande de vent gravée s'éteint. | On meurt souvent « à cause » d'un élément qui ne tue pas. Le graver est juste, et cela se comprend tout seul. |
| **Fantômes** | Jusqu'à 3 fantômes cyan à 50 % d'opacité rejouent les trajets des vies précédentes (prototype `MAX_ECHOES=3`). Ils sont traversables et rechargent la volte au contact. | Une mémoire visible : ils montrent où l'on est mort, et donc où il ne faut pas aller. |
| **Éclat d'écho** | À l'endroit de chaque mort apparaît un éclat d'écho : +3 éclats et la volte rechargée. | Il récompense le fait de repasser là où l'on a échoué. |
| **Mort tactique** | Rien n'empêche de « dépenser » la vie 1 pour graver le laser qui bloque. C'est voulu. | C'est une décision stratégique réelle : une vie contre un passage. |
| **Burin** (power-up, section 5) | Il absorbe un contact létal : le piège est gravé **sans mourir**. | C'est la version « récompense » de la gravure. |
| **Résonance** (P1) | Suivre son propre fantôme de près (≤ 12 px pendant ≥ 1 s) donne +1 éclat par seconde, jusqu'à +10 par vie. | Ce qui était une aide devient un défi de précision pour les experts. |

### 3.3 Séquence de gravure (feedback, 1,51 s au total)

1. **0,00 s** : contact. Hitstop 0,18 s, flash blanc pur [W] d'une frame sur le héros, secousse de 4 px.
2. **0,18 s** : le héros se brise en 6 pixels corail [o] qui tombent.
3. **0,63 s** : une onde cyan de rayon 0 à 40 px part du point d'impact. Le piège est recolorié de haut en bas sur 0,7 s, avec un son de verre qui se fige.
4. **1,33 s** : une icône du piège apparaît dans le codex (section 9.8), en petit coin haut droit, pendant 1 s.
5. **1,51 s** : l'écran de vie suivante s'affiche : « Vie 2/4 », bouton de redémarrage et bouton « Vidéo : +1 vie » si disponible (section 10.1).

### 3.4 Gardes-fous

- Le graphe d'une ascension comporte **au plus 4 gravures directes** (3 sans pub). Avec un Burin, on peut en ajouter, mais il y a au plus 2 Burins par ascension.
- Les **boss ne se gravent pas en entier** : seule l'attaque précise qui a tué devient cyan (un rocher, une onde), et seulement pour la tentative suivante.
- Les **ennemis gravés** (phalène, grignon, sentinelle) deviennent cyan, inoffensifs et rechargent la volte. Ils restent visibles, ce qui garde le monde vivant.
- En **Tour du jour**, les gravures restent actives (c'est le cœur du jeu). En **Défi « Sans écho »**, elles sont désactivées et le joueur est prévenu sur l'écran du défi.

---

## 4. Catalogue des obstacles (22)

### 4.1 Règles communes

- **Code couleur.** Tout ce qui tue est dans la rampe danger : [x] ombre, [X] base, [z] lumière et préavis, [Z] cœur. Rien d'autre n'utilise ces teintes. Tout ce qui est gravé passe dans la rampe écho [q t c e]. Les éléments non létaux (friable, givre, cristal, vent, eau) gardent les teintes du biome et portent un liseré distinctif.
- **Préavis.** Tout piège temporisé clignote en [z] à 10 Hz pendant son préavis, avec un son montant. Le préavis n'est jamais inférieur à 0,25 s.
- **Hitbox.** Sauf mention contraire, la hitbox létale est le visuel réduit de 1 px par côté. Collision boîte/boîte, ou cercle/boîte pour les scies.
- **Coût D.** C'est le poids du piège dans le budget de difficulté d'un chunk (section 8). La valeur indiquée est celle de base ; on ajoute +1 quand le piège tourne à vitesse maximale ou se combine en face.
- **Lecture des champs :** comportement · dimensions · timings · hitbox · télégraphe · gravé · 1re apparition · atome de compétence · combinaisons.

### 4.2 Vue d'ensemble

| ID | Nom | Famille | 1re apparition | D | Priorité |
|---|---|---|---|---|---|
| O1 | Épines | statique | 7 m (B1) | 1 | P0 |
| O2 | Scie fixe | statique | 14 m (B1) | 1 | P0 |
| O3 | Contrefort à épines | statique | 260 m (B2) | 2 | P0 |
| O4 | Scie sur rail horizontal | mobile | 35 m (B1) | 2 | P0 |
| O5 | Scie sur rail vertical | mobile | 90 m (B1) | 2 | P0 |
| O6 | Pendule (lustre / cloche) | mobile | 380 m (B3) | 3 | P0 |
| O7 | Scie orbitale | mobile | 700 m (B4) | 3 | P1 |
| O8 | Laser | temporisé | 22 m (B1) | 2 | P0 |
| O9 | Herse | temporisé | 160 m (B2) | 2 | P0 |
| O10 | Mâchoires | temporisé | 200 m (B2) | 3 | P0 |
| O11 | Plaque friable | réactif | 170 m (B2) | 1 | P0 |
| O12 | Éboulis (livres) | réactif | 420 m (B3) | 2 | P0 |
| O13 | Dalle à fléchettes | réactif | 1000 m (B5) | 3 | P1 |
| O14 | Givre | environnemental | 1260 m (B6) | 2 | P2 |
| O15 | Vent | environnemental | 910 m (B5) | 2 | P1 |
| O16 | Obscurité | environnemental | 640 m (B4) | 2 | P1 |
| O17 | Cristal rebondissant | environnemental | 610 m (B4) | 1 | P1 |
| O18 | Eau (flottaison) | environnemental | 360 m (B3) | 1 | P0 |
| O19 | Phalène de papier | ennemi | 450 m (B3) | 2 | P0 |
| O20 | Grignon (automate) | ennemi | 230 m (B2) | 2 | P0 |
| O21 | Sentinelle (gargouille) | ennemi | 950 m (B5) | 3 | P1 |
| O22 | L'Ombre | ennemi | 1300 m (B6) | 4 | P2 |

P0 compte **15 éléments** (O1, O2, O3, O4, O5, O6, O8, O9, O10, O11, O12, O18, O19, O20, plus la combinaison « épines en face »), contre 3 dans le prototype.

### 4.3 Fiches

#### O1 — Épines (statique)
- **Comportement :** une bande de pointes plaquée sur la face d'un mur. Variante « en face » à partir de 70 m : bandes sur les deux murs, décalées verticalement.
- **Dimensions :** profondeur 7 px (`SPIKE_DEPTH`), longueur 2 à 4 tuiles (32-64 px). Pas plus de 4 tuiles d'affilée par côté, pour qu'aucun mur ne soit infranchissable.
- **Timings :** aucun.
- **Hitbox :** 5 px de profondeur, sur la longueur moins 2 px à chaque extrémité.
- **Télégraphe :** dents [X] et pointe [z] ; une lueur [x] de 1 px déborde sur le mur, visible même en obscurité.
- **Gravé :** cristal cyan sur lequel on peut **s'accrocher**. Le toucher en l'air recharge la volte.
- **1re apparition :** 7 m (B1), seule, placée 4 tuiles au-dessus de l'atterrissage d'un bond : impossible à toucher sans le vouloir.
- **Atome :** choisir sa hauteur d'atterrissage (bond +3 / Élan +5 / volte).
- **Combinaisons :** épines en face (70 m) avec volte imposée ; épines + laser (fenêtre verticale réduite) ; épines au-dessus d'une plaque friable (B2).

#### O2 — Scie fixe (statique)
- **Comportement :** une scie qui tourne sur place, sur l'un des trois couloirs de vol x = 64, 96 ou 128.
- **Dimensions :** sprite 16 × 16 px, 2 frames de rotation à 12 fps.
- **Timings :** aucun.
- **Hitbox :** cercle de rayon 6 px.
- **Télégraphe :** dents [X], moyeu [Z], léger bourdonnement spatialisé (le volume monte quand on s'approche).
- **Gravé :** roue cyan immobile, traversable ; recharge.
- **1re apparition :** 14 m, au centre (x = 96), à mi-hauteur d'arc : le bond passe au-dessus, une volte trop tôt la touche.
- **Atome :** lire un arc (passer au-dessus ou en dessous d'un point).
- **Combinaisons :** deux scies fixes à x = 64 et x = 128, avec l'Élan pour passer au-dessus des deux ; scie + épines au point d'atterrissage.

#### O3 — Contrefort à épines (statique)
- **Comportement :** un bloc qui sort du mur sur 16 px. Sa face est accrochable ; ses dessus et dessous sont couverts d'épines. Il rétrécit localement le couloir à 112 px.
- **Dimensions :** 16 px de large, 32 à 48 px de haut.
- **Timings :** aucun.
- **Hitbox :** épines de 5 px dessus et dessous ; la face est sûre.
- **Télégraphe :** pierre du biome avec l'arête [l] éclairée, épines [X].
- **Gravé :** les épines deviennent cyan, et le bloc devient une simple marche.
- **1re apparition :** 260 m (B2).
- **Atome :** viser une petite cible (une face de 32 px) au lieu d'un mur entier.
- **Combinaisons :** contrefort + herse au-dessus ; deux contreforts en quinconce, qui forment un « escalier ».

#### O4 — Scie sur rail horizontal (mobile)
- **Comportement :** une scie qui fait un va-et-vient sinusoïdal sur un rail horizontal tendu entre les murs.
- **Dimensions :** scie de 16 × 16 px, amplitude de 34 à 52 px autour de x = 64, 96 ou 128.
- **Timings :** pulsation de 1,4 à 2,0 rad/s, plus d × 1,2 (d = difficulté locale de 0 à 1). Période de 2,3 à 4,5 s.
- **Hitbox :** cercle de rayon 6 px.
- **Télégraphe :** rail pointillé [x] (1 px sur 2) visible sur toute la course : on voit où la scie peut aller.
- **Gravé :** scie cyan qui continue de bouger (lisibilité du mouvement), inoffensive ; recharge.
- **1re apparition :** 35 m (B1).
- **Atome :** synchroniser son départ avec une phase (attendre la glisse ou partir tout de suite).
- **Combinaisons :** deux rails superposés en opposition de phase ; rail + laser (double horloge) ; rail + volte tardive (la scie passe pendant qu'on revient).

#### O5 — Scie sur rail vertical (mobile)
- **Comportement :** comme O4, mais le rail est vertical.
- **Dimensions :** amplitude de 18 à 30 px.
- **Timings :** pulsation de 1,4 à 2,0 rad/s, plus d × 1,2.
- **Hitbox :** cercle de rayon 6 px.
- **Télégraphe :** rail vertical pointillé.
- **Gravé :** scie cyan mobile ; recharge.
- **1re apparition :** 90 m (B1).
- **Atome :** choisir la hauteur de passage selon la phase (bond si la scie monte, Élan si elle descend).
- **Combinaisons :** rail vertical au centre + épines aux deux points d'atterrissage du bond, ce qui impose l'Élan.

#### O6 — Pendule (lustre en B3, cloche en B5)
- **Comportement :** une masse suspendue à une ancre au plafond du chunk qui se balance de mur à mur.
- **Dimensions :** ancre à x = 96, chaîne de 48 px, masse de 12 × 12 px (lustre) ou 16 × 16 px (cloche, en B5).
- **Timings :** amplitude ±50°, période 2,2 s (1,9 s en B5).
- **Hitbox :** cercle de rayon 5 px (lustre) ou 7 px (cloche) ; la chaîne n'est pas létale.
- **Télégraphe :** chaîne [m] visible ; un « tic » au point mort haut de chaque côté, qui permet de compter le rythme même sans regarder.
- **Gravé :** la masse devient cyan et continue de se balancer ; recharge. Utilisé comme « recharge mobile », il permet des doubles voltes.
- **1re apparition :** 380 m (B3).
- **Atome :** prédire une trajectoire courbe (contrairement aux rails, qui sont linéaires).
- **Combinaisons :** pendule + eau (vol long, donc plus d'exposition) ; deux pendules en opposition de phase.

#### O7 — Scie orbitale (mobile)
- **Comportement :** une ou deux scies tournent autour d'un pivot fixe (graine de cristal en B4, engrenage en B5).
- **Dimensions :** rayon d'orbite 24 px, scie de 12 × 12 px ; pivot de 8 × 8 px (non létal).
- **Timings :** 1,6 rad/s, soit une période de 3,9 s ; la variante à 2 scies est en opposition.
- **Hitbox :** cercle de rayon 5 px par scie.
- **Télégraphe :** cercle d'orbite pointillé [x] de 1 px.
- **Gravé :** la scie qui a tué devient cyan ; l'autre reste létale.
- **1re apparition :** 700 m (B4).
- **Atome :** passer dans le « trou » qui tourne.
- **Combinaisons :** orbitale + obscurité (seule la lueur des scies est visible) ; orbitale + cristal.

#### O8 — Laser (temporisé)
- **Comportement :** un émetteur sur chaque mur ; un faisceau horizontal traverse tout le couloir pendant la phase active.
- **Dimensions :** faisceau de 3 px d'épaisseur, 128 px de long ; émetteurs de 8 × 8 px.
- **Timings :** période de 2,8 à 3,4 s, moins 0,6 × d ; actif 0,85 + 0,25 × d s ; préavis 0,7 − 0,15 × d s (minimum 0,55 s).
- **Hitbox :** |dy| < 5 px entre le faisceau et le centre du héros (prototype : HALF.y + 2 = 8 ; réduit pour la clémence).
- **Télégraphe :** ligne pointillée [z] qui clignote à 10 Hz pendant le préavis, avec un sifflement montant.
- **Gravé :** une ligne cyan permanente, inoffensive. La traverser recharge la volte : c'est un « tremplin de volte » horizontal.
- **1re apparition :** 22 m (B1), après un repos de 5 m, avec un éclat juste derrière.
- **Atome :** attendre une phase (glisse contrôlée), c'est-à-dire gérer le temps contre la marée.
- **Combinaisons :** laser + épines ; deux lasers déphasés de 0,5 s ; laser + herse (double horloge, en B2).

#### O9 — Herse (temporisé)
- **Comportement :** une rangée de pointes sort horizontalement d'un mur, puis y rentre.
- **Dimensions :** 24 px de saillie (1,5 tuile), 32 px de haut.
- **Timings :** cycle de 2,4 s : 1,2 s rentrée, 0,3 s de préavis (pointes à 4 px avec cliquetis), 0,9 s sortie.
- **Hitbox :** pointes, réduites de 1 px.
- **Télégraphe :** fentes [x] dans le mur, visibles en permanence ; préavis à 4 px.
- **Gravé :** pointes cyan figées en position sortie : elles forment une marche accrochable par-dessous.
- **1re apparition :** 160 m (B2), juste après l'autel.
- **Atome :** s'accrocher **sous** un danger et partir au bon moment.
- **Combinaisons :** herse + plaque friable (on ne peut pas attendre) ; deux herses en face, déphasées.

#### O10 — Mâchoires (temporisé)
- **Comportement :** deux blocs sortent des murs et se referment au centre du couloir comme une presse.
- **Dimensions :** chaque bloc avance de 48 à 80 px ; hauteur 24 px. Au maximum, il reste 0 px d'écart, et le couloir est entièrement fermé.
- **Timings :** cycle de 3,0 s : ouvert 1,6 s, préavis 0,5 s (tremblement de 1 px et 3 pixels de poussière [p]), fermeture 0,15 s, fermé 0,45 s, réouverture 0,3 s.
- **Hitbox :** les blocs entiers, moins 2 px. **Être écrasé entre un bloc et le plafond est impossible** : les blocs n'écrasent que latéralement.
- **Télégraphe :** tremblement, poussière, et un grondement qui monte en grave.
- **Gravé :** les deux blocs deviennent cyan et restent fermés au milieu. Ils forment un plancher-pont accrochable sur les côtés.
- **1re apparition :** 200 m (B2).
- **Atome :** traverser une fenêtre temporelle **et** spatiale (passer au-dessus avant la fermeture).
- **Combinaisons :** mâchoires + Élan (passer au-dessus pendant la fermeture) ; mâchoires + grignon.

#### O11 — Plaque friable (réactif, non létal)
- **Comportement :** un segment de mur en tôle fine qui cède **0,35 s** après qu'on s'y accroche, puis revient **3 s** plus tard.
- **Dimensions :** 32 px de haut (2 tuiles).
- **Timings :** fissures en 3 étapes (0, 0,12 et 0,24 s), chute à 0,35 s ; coyote de 0,10 s après la rupture.
- **Hitbox :** non létale.
- **Télégraphe :** liseré pointillé [4] (acier clair de la Fonderie) et rivets visibles. Les fissures sont progressives.
- **Gravé (complice) :** plaque cyan solide et permanente.
- **1re apparition :** 170 m (B2).
- **Atome :** ne pas attendre, c'est-à-dire repartir vite (il entretient le combo Rythme).
- **Combinaisons :** friable + herse (impossible d'attendre la phase) ; friable + laser ; une colonne de plaques friables (escalier de vitesse).

#### O12 — Éboulis (réactif)
- **Comportement :** un bloc (une pile de livres en B3, un glaçon en B6) se détache du plafond quand le héros passe 96 px en dessous, et tombe dans un couloir de vol fixe.
- **Dimensions :** 12 × 12 px.
- **Timings :** 0,6 s de préavis (poussière qui tombe et marque lumineuse [z] de 2 px au point de départ), puis chute à 300 px/s.
- **Hitbox :** 10 × 10 px.
- **Télégraphe :** marque de départ et filet de poussière qui dessinent la colonne. Craquement sonore.
- **Gravé :** le bloc cyan reste figé en l'air : c'est un point de recharge de volte.
- **1re apparition :** 420 m (B3).
- **Atome :** réagir à un déclenchement provoqué par soi-même. On apprend que le danger se déclenche **au-dessus** de soi.
- **Combinaisons :** éboulis + eau (chute ralentie à 180 px/s dans l'eau) ; éboulis au-dessus d'un atterrissage Élan, qui impose le bond.

#### O13 — Dalle à fléchettes (réactif)
- **Comportement :** une dalle-gâchette sur un mur. Quand on s'y accroche, le mur **opposé** tire une fléchette horizontale à la hauteur de la dalle.
- **Dimensions :** dalle de 16 × 16 px ; fléchette de 8 × 2 px.
- **Timings :** tir 0,45 s après l'accroche, à 160 px/s ; la fléchette traverse le couloir en 0,8 s.
- **Hitbox :** 8 × 4 px (épaisseur augmentée pour la lisibilité).
- **Télégraphe :** la dalle s'enfonce de 1 px avec un clic ; la bouche du tireur s'allume en [z].
- **Gravé :** la fléchette devient un trait cyan figé ; la dalle ne tire plus.
- **1re apparition :** 1000 m (B5).
- **Atome :** savoir que partir vite, c'est survivre, et que bondir vers le tireur est dangereux mais que la volte esquive.
- **Combinaisons :** dalle + vent contraire (vol long, donc fléchette plus probable) ; dalle + sentinelle.

#### O14 — Givre (environnemental, non létal)
- **Comportement :** un segment de mur gelé. Pas d'accroche : le héros glisse à 90 px/s, mais il peut bondir.
- **Dimensions :** 32 à 96 px de haut.
- **Timings :** aucun.
- **Hitbox :** non létale.
- **Télégraphe :** surface [p] avec reflet [w] de 1 px. Petites étoiles de givre animées toutes les 0,5 s.
- **Gravé (complice) :** il devient accrochable (cyan).
- **1re apparition :** 1260 m (B6).
- **Atome :** décider en moins de 0,2 s (on perd 18 px de hauteur toutes les 0,2 s).
- **Combinaisons :** givre au-dessus d'épines (perte de hauteur mortelle) ; givre + vent.

#### O15 — Vent (environnemental)
- **Comportement :** une bande horizontale qui ajoute ±60 px/s à vx.
- **Dimensions :** 64 à 128 px de haut, sur toute la largeur.
- **Timings :** constant, ou alterné toutes les 3 s en arène de boss.
- **Effet mesuré :** vent favorable, vol de 0,43 s et gain de +60 px ; vent contraire, vol de 0,77 s et gain de +15 px (on arrive presque en chute).
- **Hitbox :** non létale.
- **Télégraphe :** traits de vent [O] animés à 2 px/frame, fanions sur les murs, sifflement stéréo dans le sens du vent.
- **Gravé (complice) :** la bande s'éteint pour l'ascension.
- **1re apparition :** 910 m (B5).
- **Atome :** corriger un arc à cause d'une force extérieure.
- **Combinaisons :** vent + volte (une volte contre le vent revient très vite) ; vent + rail.

#### O16 — Obscurité (environnemental)
- **Comportement :** hors d'un cercle de lumière de 72 px de rayon autour du héros, le décor est noir.
- **Dimensions :** le rayon passe à 96 px avec la Lanterne.
- **Restent visibles :** les lueurs des pièges (1 px [x], et [z] pendant le préavis), les cristaux, et **tout ce qui est cyan**. L'écho devient donc une carte.
- **Timings :** zones de 8 à 24 tuiles.
- **Hitbox :** non applicable.
- **Télégraphe :** fondu au noir sur 32 px en dither.
- **Gravé :** non applicable.
- **1re apparition :** 640 m (B4).
- **Atome :** jouer à l'oreille et à la mémoire. Les sons de piège y sont amplifiés de +3 dB.
- **Combinaisons :** obscurité + orbitale ; obscurité + fantômes (ils servent de guides).

#### O17 — Cristal rebondissant (environnemental, non létal)
- **Comportement :** un bloc sur un mur. Le toucher renvoie automatiquement le héros vers le mur opposé avec vy = −340 et vx inversé (gain de +80 px), même sans tap. Ce rebond ne consomme pas la volte.
- **Dimensions :** 16 × 16 px.
- **Timings :** il clignote 0,1 s après chaque rebond.
- **Hitbox :** non létale.
- **Télégraphe :** cristal [f F] avec cœur [W] et contour [v], et un « ding » cristallin.
- **Gravé (complice) :** il devient un mur cyan normal, sans rebond.
- **1re apparition :** 610 m (B4).
- **Atome :** anticiper un mouvement qu'on ne contrôle pas, c'est-à-dire prévoir la volte qui suit.
- **Combinaisons :** cristal vers des épines (il faut une volte de correction) ; chaîne de cristaux (« flipper »).

#### O18 — Eau (environnemental, non létal)
- **Comportement :** des bandes d'eau où la gravité vaut 300 px/s² et la chute maximale 150 px/s. Le bond y gagne +114 px.
- **Dimensions :** 64 à 160 px de haut.
- **Timings :** aucun ; des bulles montent à 20 px/s.
- **Hitbox :** non létale.
- **Télégraphe :** surface [9] ondulée de 1 px, fond [0], bulles [p]. Le son est étouffé.
- **Gravé :** non applicable.
- **1re apparition :** 360 m (B3).
- **Atome :** reprendre un rythme ralenti. L'Élan est inutile dans l'eau, il faut le désapprendre, ce qui renouvelle le contexte.
- **Combinaisons :** eau + pendule ; eau + éboulis ; sortie d'eau sous des épines.

#### O19 — Phalène de papier (ennemi)
- **Comportement :** elle vole de mur à mur à 40 px/s horizontalement, avec une oscillation verticale de ±8 px sur une période de 1,5 s, et fait demi-tour au contact du mur.
- **Dimensions :** sprite 10 × 8 px, battement de 2 frames.
- **Hitbox :** 8 × 6 px.
- **Télégraphe :** froissement de papier et une ombre [x] de 1 px.
- **Gravé :** la phalène devient cyan et inoffensive, et continue de voler : c'est une recharge mobile.
- **1re apparition :** 450 m (B3).
- **Atome :** traquer une cible mobile non périodique à l'échelle d'un bond.
- **Combinaisons :** phalène + pendule ; essaim de 3 phalènes (boss B3).

#### O20 — Grignon (ennemi)
- **Comportement :** un petit automate qui patrouille de haut en bas sur un mur, sur un segment de 48 à 96 px, à 24 px/s.
- **Dimensions :** 10 × 8 px.
- **Hitbox :** 8 × 6 px.
- **Télégraphe :** yeux [z] qui pointent dans le sens de marche ; cliquetis de pattes.
- **Gravé :** il devient cyan, inoffensif, et continue de patrouiller : c'est une recharge mobile sur le mur.
- **1re apparition :** 230 m (B2).
- **Atome :** atterrir là où le danger ne **sera** pas.
- **Combinaisons :** grignon + plaque friable ; grignon sur la face d'un contrefort.

#### O21 — Sentinelle (ennemi)
- **Comportement :** une gargouille murale. Quand le héros entre dans sa vue (64 px au-dessus ou en dessous, en ligne horizontale), elle charge 0,6 s puis tire un projectile vers la position **figée** du héros au moment du tir.
- **Dimensions :** 16 × 16 px ; projectile de 6 × 6 px, à 90 px/s.
- **Timings :** recharge de 2,5 s.
- **Hitbox :** projectile 4 × 4 px ; la gargouille n'est pas létale (c'est un mur).
- **Télégraphe :** l'œil passe de [x] à [z] pendant la charge, avec un sifflement aigu.
- **Gravé :** la gargouille cyan ne tire plus.
- **1re apparition :** 950 m (B5).
- **Atome :** bouger pour faire rater un tir visé (la volte comme esquive).
- **Combinaisons :** sentinelle + dalle à fléchettes ; deux sentinelles en face.

#### O22 — L'Ombre (ennemi, B6)
- **Comportement :** une silhouette sombre [u U] qui rejoue exactement ton trajet avec 2,0 s de retard. Si tu restes plus de 2 s au même endroit, elle te touche.
- **Dimensions :** 8 × 12 px.
- **Timings :** elle apparaît 3 s après l'entrée dans une zone d'Ombre (3 zones de 24 tuiles par B6).
- **Hitbox :** 6 × 10 px.
- **Télégraphe :** traînée [j] et un chuchotement qui suit.
- **Gravé :** l'Ombre se dissout pour la zone, et un fantôme cyan supplémentaire apparaît.
- **1re apparition :** 1300 m (B6).
- **Atome :** ne jamais rester ; le Rythme devient obligatoire.
- **Combinaisons :** Ombre + givre ; Ombre + herse (attendre est mortel).

### 4.4 Matrice de combinaisons autorisées (par paires, en un même écran de 22 tuiles)

| Combinaison | Autorisée dès | Interdite si |
|---|---|---|
| Deux temporisés (laser, herse, mâchoires, fléchettes) | B2, D ≥ 4 | Leurs fenêtres sûres se chevauchent moins de 0,4 s. |
| Mobile + temporisé | B1, 110 m | Le validateur trouve une marge inférieure à 4 px. |
| Environnemental + ennemi | B3 | L'environnement cache le télégraphe de l'ennemi (obscurité + phalène sans lueur). |
| Plus de 2 familles différentes | Jamais avant B4 | — |
| Élément jamais vu + autre piège | Jamais | Un élément nouveau apparaît toujours seul d'abord (chunk d'introduction). |

---

## 5. Éléments positifs

### 5.1 Éclats (monnaie douce)

| Objet | Valeur | Taille | Placement | Raison |
|---|---|---|---|---|
| Éclat | 1 | 6 × 6 px [g G y] | 75 % des intervalles entre pièges en contiennent ; en grappe de 3 sur un arc de bond | Prototype. Les grappes dessinent l'arc idéal : c'est un guide autant qu'une récompense. |
| Grand éclat | 5 | 10 × 10 px, scintillement à 4 fps | 1 tous les 40 m, **placé sur la route risquée** (frôlé, Élan au ras d'une scie) | Risque contre récompense explicite. |
| Éclat d'écho | 3 + recharge de volte | 8 × 8 px [c e] | Sur chaque point de mort précédent | Pilier P2. |
| Frôlé | 1 | — | Automatique (section 2.2) | Il récompense la maîtrise sans rien ajouter à l'écran. |
| Pluie d'éclats (événement) | ≈ 30 en 8 s | — | Section 7.2 | Pic de plaisir après un pic de tension. |

Les éclats ramassés **restent ramassés pour toute l'ascension** (prototype). Recommencer une vie ne permet donc pas de refarmer.

### 5.2 Power-ups (P0 : Burin, Plume, Accalmie ; P1 : Aimant, Lanterne, Élan d'or)

Ils sont ramassés au contact et s'activent immédiatement. Il n'y a **pas d'inventaire**, car un doigt ne doit gérer aucun menu. Au plus 1 power-up par chunk de repos, et environ 1 tous les 60 m. Leur choix est tiré de la graine. Leur icône est une bulle de 12 × 12 px avec un contour [G].

| Power-up | Effet exact | Durée | Lisibilité | Raison |
|---|---|---|---|---|
| **Burin** | Le prochain contact létal ne tue pas : le piège est **gravé**, puis 0,5 s d'invulnérabilité | Jusqu'à usage (max 2 par ascension) | Héros entouré d'un halo [c] de 1 px | Il transforme la règle d'écho en récompense, sans mort. |
| **Plume** | 2 voltes par bond au lieu d'une | 12 s | Écharpe dédoublée | Elle ouvre des routes de volte en zigzag. Elle apprend la volte aux joueurs qui l'évitent. |
| **Accalmie** | La marée recule de 48 px et s'arrête 6 s | Instantané + 6 s | La crête [j] de la marée se fige et pâlit | La seule respiration achetable dans un pic. |
| **Aimant** (P1) | Les éclats dans un rayon de 56 px sont attirés à 240 px/s | 15 s | Petits arcs [G] vers le héros | Il permet de jouer la route sûre sans perdre la récolte. |
| **Lanterne** (P1) | Rayon de lumière de 96 px au lieu de 72 en obscurité ; ailleurs, elle révèle les brèches secrètes à 64 px | 20 s | Flamme [A] sur l'écharpe | Une valeur qui dépend du contexte : on la garde pour B4. |
| **Élan d'or** (P1) | Chaque bond est un Élan complet sans tenir le doigt, et vx = 240 | 10 s | Traînée dorée continue | Une sensation de puissance ; vx 240 raccourcit le vol, donc la hauteur réelle vaut à peu près celle d'un Élan à 210. |

### 5.3 Autels (checkpoints)

- **Position :** une salle d'autel de 96 px (6 tuiles) au **début** de chaque biome (150, 350, 600, 900 et 1250 m), plus un autel intermédiaire au milieu de B5 et de B6 (1075 et 1450 m), car ces biomes sont longs.
- **Activation :** il suffit de passer devant. Une flamme cyan s'allume, la marée recule de 96 px et l'altitude est enregistrée.
- **Règle :** la vie suivante repart du **plus haut autel atteint**. C'est un **fait de jeu, pas un choix**. Raison : un choix (« repartir du bas pour farmer ») serait une fausse décision ; on la retire.
- **Effet sur les 4 vies :** les gravures au-dessus de l'autel restent utiles, celles d'en dessous deviennent un souvenir visible. Le score reste l'**altitude maximale de l'ascension**.

### 5.4 Objets rares et secrets

| Élément | Règle | Priorité |
|---|---|---|
| **Plume dorée** | 1 par biome, cachée hors de la route principale (Élan + volte requis, ou alcôve). Les 6 plumes débloquent la tenue « Veilleur d'or ». | P0 (B1 à B3) |
| **Fragment de relique** | 4 % de chance par chunk de repos (graine). 3 fragments forment une relique (section 9.4). | P1 |
| **Brèche secrète** | Un mur fissuré : 3 pixels [l] plus clairs, sans autre indice. On s'y accroche 2 fois dans la même vie, il s'ouvre sur une **alcôve** de 32 × 48 px qui contient un grand éclat ou une plume. 1 à 2 par biome. | P1 |
| **Salle de défi** | Une porte dorée de 16 × 24 px. Elle mène à un chunk court de 12 tuiles, de difficulté D + 2, avec la marée figée. Récompense : 25 éclats et un fragment de relique. En cas d'échec, on ressort sans perdre de vie. | P1 |
| **Éclat de lune** | Il n'existe qu'en Tour du jour : 1 caché par tour. Il compte pour un succès et une série. | P1 |

---

## 6. Biomes

Les palettes viennent de `studio/palette_v2.txt` : 4 tons de mur (ombre, base, lumière, arête) et 2 tons de fond par biome. Les rampes danger, écho, or et silence sont communes. Le héros, l'écharpe corail [o] et le cyan [c] gardent les mêmes valeurs partout. C'est la règle de lisibilité n°1 : les murs ont une luminance Y de 0,03 à 0,13, et tout ce qui compte pour le jeu a Y ≥ 0,25.

| # | Biome | Altitude | Thème | Palette (lettres, hex) | Pièges signature | Mécanique propre | Son |
|---|---|---|---|---|---|---|---|
| B1 | **Crypte des Veilleurs** | 0-150 m | Tombeaux des anciens Veilleurs, statues à lanterne | murs n #2f2c5c, s #39427b, m #46639f, arête l #719dca ; fonds b #17122a, d #23203d | épines, scie fixe, laser, scies sur rail | Aucune : on y apprend les 3 verbes et l'écho | Orgue grave en mineur, 80 BPM, réverbération longue |
| B2 | **Fonderie froide** | 150-350 m | Forges éteintes, acier bleu-sarcelle, vapeur froide | 1 #2a3341, 2 #364957, 3 #4a6973, arête 4 #76a1a4 ; fonds ( #0f1622, ) #192431 | herse, mâchoires, plaque friable, grignon, contrefort | **Plaques friables** : on ne peut pas attendre partout | Percussions métalliques, 96 BPM, chuintement de vapeur |
| B3 | **Bibliothèque engloutie** | 350-600 m | Rayonnages inondés, pages flottantes | 5 #3a2a55, 6 #483d7b, 7 #5a5cad, arête 8 #8a98cc ; fonds [ #191229, ] #261f3b ; eau 0 #234a75, 9 #448eb2 | eau, lustres-pendules, éboulis de livres, phalènes de papier | **Eau** : gravité 300, saut ×2 | Harpe et pad aquatique, 72 BPM, filtre passe-bas sous l'eau |
| B4 | **Jardin suspendu de cristal** | 600-900 m | Serre géante en ruine, cristaux vivants | B #452749, C #5a396a, D #76569a, arête K #a191c9 ; fonds { #1f1025, } #2e1c37 ; cristal v f F | cristal rebondissant, obscurité, scie orbitale, phalènes | **Obscurité + cristaux-lampes** : l'écho devient la carte | Carillons, 88 BPM, notes jouées par les rebonds |
| B5 | **Clocher des vents** | 900-1250 m | Beffroi en altitude, crépuscule | L #452a39, M #5f3b56, N #825580, arête O #b08eb6 ; fonds < #23101f, > #331a30 ; horizon $ #854a6b | vent, sentinelles, dalles à fléchettes, cloches-pendules | **Vent** : les arcs changent | Cloches, cordes, 104 BPM, vent stéréo |
| B6 | **Sommet céleste** | 1250 m et plus | Marbre de nuit argenté, ciel ouvert, aurore | P #2c3149, Q #3a475b, S #516777, arête T #829fa7 ; fonds ^ #12142a, ~ #1e2139 ; aurore f #53bd8b en plan lointain | givre, L'Ombre, remix de tous les pièges | **Givre + Ombre** : interdiction de rester | Chœur, 112 BPM, silence total pendant 0,5 s à chaque autel |

**Remix au-delà de 1600 m.** Les chunks de tous les biomes sont tirés avec D + 1 et la palette du Sommet. La marée garde son plafond B6. Raison : les experts ont une suite infinie, sans contenu nouveau à produire.

**Transitions.**
1. Le dernier chunk de chaque biome est une **arène de boss** (section 7).
2. Elle est suivie d'une **salle d'autel de 96 px** dont les murs sont peints en dither 2 × 2 sur 32 px entre les deux palettes.
3. Fondu musical de 2 s.
4. Carte de titre de 1,5 s (nom du biome en police pixel 8 px [w], altitude en [G]). Elle n'interrompt pas le contrôle.
5. Les 5 premiers mètres du biome suivant sont un **repos** où apparaît, seule, sa mécanique propre (chunk d'introduction).

---

## 7. Boss et événements

### 7.1 Boss (arènes de 24 tuiles, à un doigt)

**Règles communes.**
- L'arène occupe les 24 derniers mètres du biome. La **marée s'arrête au seuil**, et une porte de Silence [U] se referme derrière le héros.
- On gagne en **touchant 3 runes** [G] dans l'ordre. Une rune est une tuile murale de 16 × 16 px qui s'allume à un emplacement différent après chaque rune touchée, alternant les côtés.
- Une rune touchée fait « sonner » le boss : il est étourdi 1 s et ses attaques s'arrêtent.
- Après la 3e rune, le boss se brise en éclats (+20) et le prochain autel s'ouvre.
- Durée cible : 25 à 40 s. Une mort en arène grave l'**attaque précise** qui a tué, pour la tentative suivante seulement.
- Raison : les runes réutilisent les verbes existants (viser une hauteur sur un mur). Aucun nouveau contrôle n'est nécessaire, et chaque boss devient un examen de son biome.

| Boss | Biome | Pattern (avec télégraphes) | Ce qu'il examine | Priorité |
|---|---|---|---|---|
| **Le Sonneur** | B1 | Une cloche géante (pendule de 20 px de rayon, période 2,6 s) au centre. Toutes les 3 s, une onde-laser horizontale descend de 40 px, avec un préavis de 0,6 s. Runes à +4, +10 et +16 tuiles. | Laser et lecture d'arc | P0 |
| **Le Forgeron-Automate** | B2 | Deux bras-mâchoires frappent à la hauteur où le héros **était** 0,8 s plus tôt (marque [z] au mur). Des plaques friables entourent les runes 2 et 3. | Ne pas rester, Rythme | P1 |
| **La Mère-Phalène** | B3 | Une phalène de 32 × 24 px vole en huit et lâche un essaim de 3 phalènes toutes les 4 s. L'arène est inondée à 50 %. | Eau, cibles mobiles | P1 |
| **L'Œil de cristal** | B4 | Arène obscure. Un faisceau tourne à 0,9 rad/s depuis le centre ; il est létal, et son préavis est un pointillé de 0,5 s. Seuls les cristaux éclairent. | Obscurité, cristaux | P1 |
| **La Girouette** | B5 | Le vent alterne toutes les 3 s (flèche géante [O] en haut de l'écran 0,5 s avant chaque bascule). Deux sentinelles s'ajoutent après la rune 1. | Vent, esquive | P1 |
| **Le Silence** | B6 | La marée devient boss : elle monte à 60 px/s pendant 30 s. Chaque rune la fait reculer de 64 px. Les runes sont entourées de givre. | Tout ; finale de l'ascension | P2 |

### 7.2 Événements (au plus 1 par biome ; le créneau est fixé par la graine dans un chunk de repos)

| Événement | Déclencheur | Effet | Raison |
|---|---|---|---|
| **Pluie d'éclats** | Un chunk de repos marqué « EVT » | Pendant 8 s, des éclats tombent à 60 px/s sur les 3 couloirs (≈ 30). | Un pic de plaisir après un pic de tension (rythme M M P R). |
| **Poursuite de crue** | Une cloche à toucher, volontairement (opt-in) | La marée va ×1,8 plus vite pendant 12 s, et les éclats valent ×2 pendant ce temps. | Une prise de risque choisie, jamais imposée. |
| **Éclipse** (B4) | Graine | Toute la zone suivante de 16 tuiles est dans l'obscurité, mais les fantômes brillent ×2. | Elle met en valeur l'écho. |
| **Carillon** (B5) | Graine | Tous les pendules du chunk se synchronisent, et le chunk se traverse en rythme. | Variation de contexte sans contenu nouveau. |
| **Écho errant** (P1) | 1 par ascension, au plus | Un fantôme doré parcourt une route secrète ; le suivre mène à une alcôve. | Il enseigne les secrets par l'exemple. |

---

## 8. Structure d'une partie : chunks d'auteur assemblés

### 8.1 Le chunk

| Propriété | Valeur | Raison |
|---|---|---|
| Format | Fichier texte `game/chunks/<biome>/<id>.txt`. Une ligne = une rangée de 16 px ; 12 caractères (2 de mur, 8 jouables, 2 de mur) | Éditable dans n'importe quel éditeur, lisible dans un diff, cohérent avec l'art en pixel texte. Le chargeur GDScript tient en environ 150 lignes. |
| Hauteur | 12, 16 ou 24 rangées (12 = court, 16 = standard, 24 = arène ou grand pic) | Trois tailles suffisent à varier le rythme sans compliquer l'assemblage. |
| Jointures | 2 rangées tampon (mur plein, vide au centre) en haut et en bas de chaque chunk | Aucun piège ne chevauche deux chunks, donc aucun piège ne se retrouve injouable par accident. |
| Miroir | Chaque chunk peut être retourné gauche/droite (tirage de la graine) | Contenu ×2 gratuitement. |
| Aléatoire | La graine choisit le chunk, le miroir, la phase des minuteries (0 à 1 période) et l'emplacement des éclats parmi les créneaux marqués | L'aléatoire porte sur les entrées et les conditions, jamais sur les résultats. Une même action donne toujours le même effet. |

**Légende ASCII (extrait).**
`#` mur · `.` vide · `>` épines plantées sur le mur gauche (pointes vers la droite), `<` épines sur le mur droit · `S` scie fixe · `-` rail horizontal · `|` rail vertical · `L` émetteur laser · `h` herse · `M` mâchoire · `f` plaque friable · `~` eau · `P` ancre de pendule · `g` grignon · `m` phalène · `o` créneau d'éclat · `O` grand éclat · `*` créneau de power-up · `R` rune · `?` brèche secrète.

**En-tête obligatoire.**
```
id: b1_laser_intro   biome: B1   h: 16   D: 2   tension: M   entree: any   sortie: L
verbe: bond          intro: O8   alt_min: 22   alt_max: 150
```

**Exemple : `b1_laser_intro` (16 rangées, lu de haut en bas).**
```
##........##
##........##
##..o.o.o.##
##........##
##........##
L#........#L   <- laser : période 3,1 s, préavis 0,7 s
##........##
##........##
##>.......##   <- épines 1 tuile, sous le laser, à gauche
##........##
##...O....##   <- grand éclat sur l'arc d'Élan
##........##
##........##
##........##
##........##
##........##
```

### 8.2 Étiquettes et budget

- **D (1-10) :** la somme des coûts D des pièges (section 4.2), +1 par paire combinée, +1 si le chunk impose la volte.
- **Tension :** `R` repos (D ≤ 1, aucun piège nouveau, éclats et un créneau de power-up), `M` montée, `P` pic.
- **Cycle :** M → M → P → R, soit environ 40 m. Raison : la tension sans repos épuise, et le repos sans tension ennuie (Escalating Challenge et Dynamic Friction).
- **Entrée et sortie :** `L`, `R` ou `any`. C'est le côté du mur où le héros doit être accroché pour entrer ou sortir proprement. L'assembleur n'enchaîne que des côtés compatibles.
- **Verbe requis :** `bond`, `elan` ou `volte`. Un chunk qui exige un verbe n'apparaît qu'après le chunk d'introduction de ce verbe.

### 8.3 Assemblage (algorithme)

1. `rng = RandomNumberGenerator(seed)`. La graine est la même pour les 4 vies. En Tour du jour, c'est `daily_seed` (prototype, `game_state.gd`).
2. Pour chaque biome, on construit une file de créneaux selon le cycle M M P R jusqu'à l'altitude de l'arène.
3. **Altitudes d'introduction** (section 4.2) : on place d'abord le chunk `intro: Ox` de l'élément au créneau le plus proche.
4. Pour chaque créneau restant, on tire parmi les chunks qui respectent toutes ces conditions :
   - le biome correspond ;
   - la tension correspond ;
   - D est dans [D_cible − 1, D_cible + 1] ;
   - l'entrée est compatible ;
   - l'altitude est dans [alt_min, alt_max] ;
   - le chunk n'a pas servi dans les 8 derniers créneaux.
5. Si aucun chunk ne convient, on élargit à D ± 2, puis on prend un chunk R. Le cas est journalisé en mode debug, pour qu'on sache quel chunk écrire.

### 8.4 Garantie « pas de mur infranchissable »

- **Validateur hors ligne** (`tools/validate_chunks.gd`, exécuté en headless) :
  1. Pour chaque chunk, il essaie toutes les entrées (côté, phase de minuterie de 0 à 1 par pas de 0,05) et toutes les séquences de verbes à la résolution du demi-tick (1/120 s).
  2. Il doit trouver une route avec une **marge ≥ 4 px** en B1 et B2, ≥ 3 px en B3 et B4, et ≥ 2 px en B5 et B6.
  3. En B1, la route doit utiliser **uniquement des bonds**, sauf dans les chunks marqués `verbe: elan` ou `verbe: volte`.
- **Attente forcée maximale** : au plus 0,6 × le budget d'attente du biome (section 8.6).
- **Règles d'édition** : au plus 4 tuiles d'épines d'affilée par côté, jamais d'épines sur les deux murs à la même hauteur sur plus d'une tuile, toujours une route sans power-up.
- **Robot en jeu** (repris du prototype) : 12 graines par build. Objectif : 12/12 franchies jusqu'à 1250 m. Le prototype en franchissait 11/12 jusqu'à environ 1600 m, avec 3 pièges.

### 8.5 Courbe de difficulté

D_cible(m) = 2 + 6 × (m / 1250)^0,8. On y ajoute une dent de scie par biome : −1,5 sur les 20 premiers mètres (respiration) et +1 sur les 30 derniers avant l'arène.

| Biome | D moyen | D des pics | Espace entre pièges | Marge validateur | Chunks P0 / total visé |
|---|---|---|---|---|---|
| B1 Crypte | 2-3 | 4 | 7 → 6 tuiles | 4 px | 30 / 40 |
| B2 Fonderie | 3-4,5 | 6 | 6 → 5 tuiles | 4 px | 30 / 40 |
| B3 Bibliothèque | 4-5,5 | 7 | 5,5 → 5 tuiles | 3 px | 30 / 40 |
| B4 Jardin | 5-6,5 | 8 | 5 → 4,5 tuiles | 3 px | — / 40 |
| B5 Clocher | 6-7,5 | 9 | 4,5 → 4 tuiles | 2 px | — / 40 |
| B6 Sommet | 7-9 | 10 | 4 tuiles | 2 px | — / 30 |
| Remix au-delà de 1600 m | 9-10 | 10 | 4 tuiles | 2 px | réutilise tous les chunks |

L'espace entre pièges reprend la formule du prototype : lerp(7, 4, d) tuiles, plus 0 à 2 tuiles.

### 8.6 Marée de Silence et budget d'attente

- **Vitesse :** v(t) = 10 + 0,35 · t px/s, où t est le temps écoulé depuis le début de la vie. Elle est plafonnée selon le biome où se trouve le héros : **B1 28, B2 34, B3 40, B4 46, B5 52, B6 58 px/s**.
- **Départ :** la crête part 96 px sous l'autel (ou le sol) à chaque vie.
- **Rattrapage :** la crête n'est jamais à plus de 26 px sous le bord bas de l'écran (prototype), donc jamais à plus de 158 px sous le héros.
- **Budget d'attente** (temps qu'on peut passer accroché depuis la distance maximale, glissade de 14 px/s comprise) : 158 / (v + 14).

| | B1 | B2 | B3 | B4 | B5 | B6 |
|---|---|---|---|---|---|---|
| Budget d'attente au plafond | 3,8 s | 3,3 s | 2,9 s | 2,6 s | 2,4 s | 2,2 s |

Raison : ce chiffre unique relie la marée aux minuteries. La pire attente de laser (actif + préavis ≈ 1,65 s) ou de mâchoires (≈ 1,4 s) reste toujours inférieure à 0,6 × le budget d'attente.

### 8.7 Durées cibles

| Profil | Durée d'une vie | Altitude atteinte (meilleure vie) | Durée d'une ascension (4 vies) |
|---|---|---|---|
| Novice (J1) | 40-60 s | 80-200 m (fin de B1, début de B2) | 2,5-4 min |
| Médian (J7) | ≈ 75 s | 350-650 m (B3, entrée de B4) | 4-6 min |
| Expert | 120-180 s | 1250 m et plus | 8-12 min |

- **Progression de référence :** 3 m/s (48 px/s), attentes comprises.
- **Temps de traversée de chaque biome à 3 m/s :** B1 50 s, B2 67 s, B3 83 s, B4 100 s, B5 117 s.

---

## 9. Méta-progression

### 9.1 Économie (sources, convertisseurs, puits)

| Rôle | Éléments | Valeurs indicatives (joueur médian) |
|---|---|---|
| **Sources** | Éclats ramassés, frôlés, combos Rythme, boss (+20), missions, coffre du jour, série du Tour du jour | ≈ 90 éclats par ascension ; missions ≈ 115 par jour ; coffre 30 par jour ; série 5 + 5 × série (plafond 35) |
| **Convertisseurs** | Vidéo récompensée ×2 sur le gain de l'ascension ; vidéo ×2 sur le coffre ; fragments de relique (3 font une relique) | Au plus 1 ×2 par ascension, au plus 6 par jour |
| **Puits** | Tenues (section 9.3), teintes de cape (8 × 150), cadres de partage (6 × 100) | ≈ 18 000 éclats au total, soit environ 30 jours d'un joueur médian sans pub et 20 jours avec |
| **Boucle qui se renforce** | Mieux jouer → plus haut → plus d'éclats et d'XP → tenues visibles et partage | Elle est **uniquement cosmétique**, donc il n'y a pas d'emballement de puissance. |
| **Friction** | Les éclats ramassés ne se refarment pas pendant une ascension ; le Zen donne ×0,25 ; il n'existe aucun achat d'éclats | Elle empêche de farmer par la répétition triviale. |

### 9.2 Niveaux (1-50)

- **XP nécessaire** pour passer du niveau n au niveau n+1 : 200 + 60·n. Il faut 83 300 XP au total pour atteindre le niveau 50, soit environ 140 ascensions médianes.
- **Gain d'XP** = mètres de la meilleure vie + 10 par gravure + 25 par boss + XP des missions.

| Niveau | Déblocage | Raison |
|---|---|---|
| 2 | Missions quotidiennes | Un objectif à court terme dès la 2e session. |
| 3 | Codex des pièges | Le joueur a déjà gravé 3 à 5 pièges : le codex a du contenu. |
| 5 | Emplacement de relique 1 | La première relique arrive quand les verbes sont maîtrisés. |
| 8 | Mode Zen | Une pratique sans pression, une fois la règle de la marée comprise. |
| 10 | Défi hebdomadaire et chaîne hebdo | Le joueur connaît B1 et B2, donc les mutateurs ont un sens. |
| 12 | Bestiaire | Il a croisé grignons et phalènes. |
| 15 | Emplacement de relique 2 | |
| 20 | Tenue « Veilleur de cendre » et cadre de partage animé | Prestige visible. |
| 30 | Emplacement de relique 3 | |
| 40 | Variante de traînée d'écho (motif, pas couleur : losanges, étoiles, notes) | La teinte de l'écho reste cyan ±15°, pour la lisibilité. |
| 50 | Tenue « Silence apprivoisé » et titre « Gardien du Sommet » | Prestige final. |

### 9.3 Tenues (24) : effets visuels uniquement

Deux contraintes de lisibilité : l'écharpe reste dans la rampe corail [r R o a A] (seule la forme change), et la silhouette reste de 8 × 12 px.

| # | Tenue | Effet visuel | Obtention |
|---|---|---|---|
| 1 | Veilleur | Cape lavande [H] | Départ |
| 2 | Novice de la Crypte | Capuche pointue | 50 éclats |
| 3 | Lanternier | Petite lanterne [A] à la ceinture, lueur de 2 px | 100 |
| 4 | Forgeron froid | Cape [3], étincelles [4] à l'atterrissage | 150 |
| 5 | Archiviste | Pages qui volent derrière la cape | 250 |
| 6 | Jardinier | Feuilles [V f] à chaque bond | 350 |
| 7 | Sonneur | Petit son de cloche à la volte | 450 |
| 8 | Voyageur des vents | Écharpe 4 px plus longue | 600 |
| 9 | Plongeur | Bulles en sortie d'eau | 700 |
| 10 | Astronome | Étoiles [G] dans la traînée d'Élan | 850 |
| 11 | Masque de verre | Visage cristal [F] | 1 000 |
| 12 | Chevalier d'écume | Cape [J], écume à la mort | 1 200 |
| 13 | Ombre polie | Contour [u], yeux [c] | 1 500 |
| 14 | Prisme | Cape qui tourne sur 3 teintes froides toutes les 0,5 s | 2 000 |
| 15 | Couronne de nuit | Couronne [G] de 3 px | 2 500 |
| 16 | Veilleur d'or | Liseré [G] et traînée dorée | Les 6 plumes dorées |
| 17 | Veilleur de cendre | Cape [d] et braises [a] | Niveau 20 |
| 18 | Silence apprivoisé | Cape [U] et crête [j] animée | Niveau 50 |
| 19 | Gardien du jour | Soleil pixel sur le dos | Série de 30 jours |
| 20 | Graveur | Ciseau dans le dos ; ses gravures brillent 1 s de plus | 50 gravures (succès) |
| 21 | Sans-faute | Cape blanche froide [w] | Atteindre 600 m sans mourir |
| 22 | Mille-voltes | Plumes [i] aux épaules | 1 000 voltes |
| 23 | Défi de saison A | Variable | Chaîne hebdo, saison 1 |
| 24 | Défi de saison B | Variable | Chaîne hebdo, saison 2 |

Total des tenues achetables : 11 700 éclats. Avec les teintes de cape et les cadres de partage, les puits atteignent ≈ 13 500 éclats. Le chiffre « ≈ 18 000 » de la section 9.1 inclut les tenues de saison futures.

### 9.4 Reliques (12) : légères, jamais payantes

- **Obtention :** 3 fragments, un succès précis ou une chaîne hebdo. **Jamais par vidéo, jamais par achat.**
- **Emplacements :** aux niveaux 5, 15 et 30.
- **Limites :** chaque effet est un effet de côté ou vaut ≤ 10 %. Les reliques sont **désactivées en Tour du jour et en Défi**, donc les classements restent équitables.

| Relique | Effet | Pourquoi ce n'est pas du pay-to-win |
|---|---|---|
| Bourse usée | +10 % d'éclats | Économie seulement. |
| Clochette | Les préavis sonnent 0,05 s plus tôt (son seulement) | Information, pas puissance. |
| Sablier fêlé | Marée −5 % | Elle vaut ≈ 0,15 s de budget d'attente en B1. |
| Écharpe tissée | Fenêtre de buffer 0,10 s au lieu de 0,08 s | Confort d'entrée. |
| Cœur d'écho | L'éclat d'écho rapporte 5 au lieu de 3 | Économie. |
| Boussole | Une flèche indique le prochain power-up hors de l'écran | Information. |
| Carte du cartographe | Les brèches secrètes scintillent à 48 px | Exploration. |
| Pierre de lune | +1 fragment de relique garanti par semaine | Méta seulement. |
| Ancre | Les plaques friables tiennent 0,40 s au lieu de 0,35 s | +14 %, mais sur un seul élément. |
| Lentille | Obscurité : rayon +8 px | +11 %, sur un seul biome. |
| Grimoire | +10 % d'XP | Méta seulement. |
| Fil d'Ariane | Le fantôme le plus récent est 20 % plus opaque | Lisibilité. |

### 9.5 Missions

- **Quotidiennes :** 3 par jour (facile, moyenne, difficile). Récompenses de 20, 35 et 60 éclats, plus 50, 80 et 120 XP. **Une relance par jour via une vidéo choisie.**
- **Liste de missions (extrait) :**
  - atteindre 150 m ;
  - graver 2 pièges différents ;
  - faire 10 frôlés ;
  - finir une vie sans utiliser la volte au-delà de 50 m ;
  - atteindre le palier Rythme 20 ;
  - ramasser 3 grands éclats ;
  - battre le Sonneur ;
  - traverser 40 m d'eau ;
  - faire 25 Élans complets ;
  - utiliser un Burin ;
  - activer 2 autels dans une ascension ;
  - finir le Tour du jour ;
  - recharger 5 voltes sur du cyan ;
  - passer 3 lasers sans attendre ;
  - toucher 3 phalènes gravées.
- **Hebdomadaires :** une **chaîne de 5** missions de plus en plus difficiles. Chaque étape débloque la suivante. Récompense finale : un fragment de relique, 150 éclats et une tenue de saison (toutes les 8 semaines).

### 9.6 Succès (30)

| # | Succès | Condition |
|---|---|---|
| 1 | Premier pas | Faire 1 bond |
| 2 | Volte-face | Réussir une volte qui évite un piège (frôlé en volte) |
| 3 | Prendre son élan | Faire un Élan complet |
| 4 | La mort écrit | Graver un premier piège |
| 5 | Graveur | 50 gravures |
| 6 | Archiviste du danger | Graver 10 pièges différents |
| 7 | Crypte franchie | Atteindre 150 m |
| 8 | Acier froid | Atteindre 350 m |
| 9 | Encre et eau | Atteindre 600 m |
| 10 | Lumière de verre | Atteindre 900 m |
| 11 | Sous les cloches | Atteindre 1250 m |
| 12 | Au-delà | Atteindre 1600 m |
| 13 | Sans faute | 600 m sans mourir |
| 14 | Une seule vie | Battre le Sonneur à la vie 1 |
| 15 | Rythme parfait | Palier Rythme 30 |
| 16 | Frôleur | 20 frôlés dans une vie |
| 17 | Résonance | Suivre son fantôme pendant 5 s |
| 18 | Recharge en chaîne | 3 recharges cyan dans un même bond (avec Plume) |
| 19 | Plumassier | Les 6 plumes dorées |
| 20 | Chasseur de brèches | Ouvrir 10 brèches secrètes |
| 21 | Sonneur réduit au silence | Battre le Sonneur |
| 22 | Tous les gardiens | Battre les 6 boss |
| 23 | Fidèle | Série de 7 jours au Tour du jour |
| 24 | Gardien du jour | Série de 30 jours |
| 25 | Top 10 % | Tour du jour dans le top 10 % |
| 26 | Moine | 30 min cumulées en Zen |
| 27 | Mutant | Finir 5 défis hebdo |
| 28 | Burin d'or | Survivre à 2 contacts dans une ascension grâce au Burin |
| 29 | À contre-courant | Gagner +60 px avec une volte contre le vent |
| 30 | Sans écho | Atteindre 350 m en défi « Sans écho » |

### 9.7 Tour du jour et défis spéciaux

- **Tour du jour :** une graine mondiale (`daily_seed`), les reliques désactivées, **1 ascension classée** et des essais libres non classés ensuite.
  - Série : 5 + 5 × série éclats, plafonnés à 35 (prototype).
  - Écran de partage façon Wordle, en texte pur : `ÉCHO #312 — 612 m`, puis une ligne par vie en blocs `▮` (10 m chacun), une marque `✕` à la mort, et le nombre de gravures. Sans spoiler de la tour.
- **Défi hebdomadaire (P1) :** une graine fixe et 1 à 2 **mutateurs**, avec un classement propre.

| Mutateur | Effet |
|---|---|
| Miroir | Tout est inversé ; aucun miroir aléatoire. |
| Crue | Marée ×1,3 et éclats ×1,5. |
| Sans écho | Pas de gravure, fantômes visibles. |
| Une vie | 1 vie, autels désactivés. |
| Tout gravé | Un type de piège (tiré) commence gravé. |
| Plume perpétuelle | 2 voltes par bond en permanence. |
| Nuit totale | Obscurité dans tous les biomes. |
| Pendules | Tous les mobiles deviennent des pendules. |

- **Défis spéciaux (P2) :** des événements saisonniers de 7 jours avec une tour unique (chunks dédiés) et une tenue à la clé.

### 9.8 Codex des pièges et bestiaire

- **Codex :** une fiche par obstacle (22). **3 étoiles** :
  1. vu ;
  2. gravé au moins une fois ;
  3. maîtrisé, c'est-à-dire franchi 50 fois sans y mourir.

  Chaque fiche montre une animation de 48 × 48 px en boucle avec le télégraphe, son atome en une phrase et sa version gravée. Raison : il rend visible la courbe d'apprentissage (Theory of Fun), et la 3e étoile pousse à revisiter.
- **Bestiaire :** ennemis et boss, avec une phrase de lore chacun, le nombre de gravures et le meilleur temps contre chaque boss. Il se débloque au premier contact visuel.
- **Classements :** Google Play Games Services (P1). Classements pour le Tour du jour, le Défi et la meilleure altitude (tout temps).

---

## 10. Modes de jeu

| Mode | Règles | Déblocage | Justification |
|---|---|---|---|
| **Ascension** | 4 vies, graine aléatoire, autels, reliques actives | Départ | C'est le cœur du jeu : la boucle d'écho complète. |
| **Tour du jour** | Graine mondiale, 1 essai classé, reliques désactivées, partage | Départ (après la première ascension) | Le rendez-vous quotidien et la viralité. Le prototype le valide déjà. |
| **Défi hebdo** (P1) | Graine fixe et mutateurs, classement | Niveau 10 | Il renouvelle le contexte pour les experts (nouvelle contrainte sans nouveau contenu). |
| **Zen** (P1) | Pas de marée, vies infinies, gravures actives, éclats ×0,25, XP ×0,5, aucun classement | Niveau 8 | Pratique et découverte des biomes hauts. Le ×0,25 empêche que ce soit la meilleure façon de farmer. |

### 10.1 Monétisation (rappel des contraintes, sans changement de cible)

- **Uniquement des vidéos récompensées, choisies par le joueur** (AdMob). Aucune interstitielle, aucune bannière.
- **Quatre placements :**
  1. +1 vie, une fois par ascension, proposée sur l'écran de mort, **jamais en Tour du jour ni en Défi** ;
  2. ×2 sur les éclats de fin d'ascension ;
  3. relance d'une mission quotidienne ;
  4. ×2 sur le coffre du jour.
- **Objectif :** 1,5 à 2 vues par joueur actif quotidien (DAU). Ciblage marketing sur les pays à fort eCPM, de 10 à 25 $ (voir `jeu/DESIGN.md`).
- Raison : la récompense vidéo ne touche jamais au classement, et ne donne jamais de puissance permanente.

---

## 11. Onboarding sans texte (teaching engine)

**Principe.** Chaque élément suit la même séquence :
1. introduction sûre ;
2. expérimentation ;
3. échec peu coûteux ;
4. renforcement ;
5. nouvelle contrainte ;
6. combinaison.

Aucune phrase n'apparaît à l'écran. Il n'y a que des **pictogrammes de 16 × 16 px** [w] ; chacun s'efface dès que le geste est réussi une fois.

**Première ascension de la vie du joueur (« Ascension 0 »).** Les 60 premiers mètres sont fixes, faits main et sans graine. Les **2 premières morts avant 40 m ne coûtent pas de vie**, mais elles gravent quand même : on montre la règle sans la punir. La marée ne démarre qu'après le 3e bond.

| Altitude | Ce qui est enseigné | Mise en scène | Étape |
|---|---|---|---|
| 0-7 m | Bond | Le héros est accroché au mur gauche. Le pictogramme « main qui tape » pulse toutes les 1 s jusqu'au premier tap. Une grappe de 3 éclats dessine l'arc. | Introduction sûre |
| 7-14 m | Le magenta tue | Épines de 2 tuiles **au-dessus** de l'atterrissage : on les voit sans pouvoir les toucher. | Introduction sûre |
| 14-22 m | Lire un arc | Scie fixe au centre, à mi-hauteur : le bond passe au-dessus. Le tap répété (volte prématurée) la touche. | Expérimentation |
| 22-30 m | Élan | Épines exactement à l'atterrissage du bond (+3 tuiles), zone libre à +5. Un **fantôme-guide** cyan pré-enregistré montre l'Élan ; pictogramme « main tenue » avec une barre qui se remplit en 0,28 s. | Introduction sûre, puis échec peu coûteux |
| 30-40 m | Volte | Le mur d'en face est couvert d'épines sur 4 tuiles (au bond comme à l'Élan). La seule zone sûre est du même côté, à +5. Le fantôme-guide fait la volte ; pictogramme « main + flèche courbe ». | Introduction sûre, puis échec peu coûteux |
| 40-50 m | Attendre (glisse) | Laser seul, période de 3,2 s, un grand éclat derrière. La marée est visible en bas, lente (10 px/s). | Nouvelle contrainte |
| 50-60 m | Le cyan recharge | Un **éclat d'écho** pré-placé en plein vol. Le toucher recharge la volte et permet une 2e volte qui mène à un grand éclat. | Renforcement |
| Première mort | La gravure | Séquence de la section 3.3 jouée au ralenti ×0,5 la première fois seulement (1,2 s de plus). | Échec peu coûteux |
| Vie suivante | Le cyan est sûr | Quand le héros approche à 64 px de son premier piège gravé, celui-ci pulse 2 fois. Le fantôme de la vie précédente passe à travers. | Renforcement |
| 70 m et plus | Combinaison | Retour à l'assemblage normal par graine, avec épines en face à 70 m. | Combinaison |

**Introduction des éléments ultérieurs.** Chaque nouvel obstacle arrive par un **chunk `intro`** de D ≤ 2 : l'élément est seul, avec une route sûre visible et un grand éclat qui récompense la route qui l'utilise. Les biomes enseignent leur mécanique propre dans leurs 5 premiers mètres (section 6).

**Indicateurs de playtest.**
- ≥ 90 % des joueurs passent 22 m sans aide.
- ≥ 80 % utilisent la volte volontairement avant 60 m.
- ≥ 70 % font un Élan complet avant 40 m.
- La durée médiane de l'Ascension 0 est inférieure à 4 min.

---

## 12. Checklist Milo appliquée au GDD

### 12.1 Questions de revue

| Axe | Question | Réponse pour ÉCHO |
|---|---|---|
| Boucle centrale | Que fait le joueur après 20 minutes ? | Il choisit entre trois hauteurs d'atterrissage (bond, Élan, volte) sous la contrainte d'une marée, et il **planifie ses vies** (mort tactique, route par le cyan). |
| | Pourquoi cette action est-elle intéressante ? | Chaque tap engage 0,55 s d'arc irréversible ; la volte et le cyan offrent une correction limitée. |
| | Quelle décision la précède ? | Où atterrir, quand partir (phase), suivre la route sûre ou celle du grand éclat. |
| | Quel feedback la suit ? | Son au tap, écrasement, poussière, frôlé (ralenti), combo Rythme, gravure. |
| Économie | Sources, convertisseurs, puits ? | Section 9.1. |
| | Quelle boucle se renforce ? | Maîtrise → altitude → éclats et XP → cosmétique. Elle est purement cosmétique, donc sans emballement. |
| | Où est la friction ? | Pas de refarm dans une ascension, Zen ×0,25, et la marée qui monte. |
| Émergence | Quelles interactions produisent des états non prévus ? | Cyan + Plume (chaînes de recharges), pendule gravé (recharge mobile), cristal + volte, éboulis gravé en l'air. Elles sont voulues et bornées par la règle d'une recharge par élément et par bond. |
| | Le système reste-t-il lisible ? | Oui : 4 familles de couleur seulement (danger, écho, or, silence), et des luminances séparées (section 6). |
| | Stratégies dominantes ? | « Toujours l'Élan » : contrée par les zones sûres réparties 40/40/20 et par les dangers placés à +5. « Spammer le tap » : le robot naïf meurt vers 18 m (prototype). « Attendre en bas » : la marée et le budget d'attente l'interdisent. |
| Progression | Qu'est-ce qui change vraiment ? | Le contexte : un biome = une mécanique propre (eau, vent, obscurité…) qui modifie les arcs. Pas la puissance. |
| | Crée-t-elle de nouvelles décisions ? | Oui : l'eau rend l'Élan inutile, le vent rend la volte puissante, l'obscurité donne de la valeur aux fantômes. |
| Niveau | Mission et espace ont-ils été pensés séparément ? | Oui : étiquettes (tension, D, verbe) d'un côté, géométrie ASCII de l'autre. L'assembleur relie les deux. |
| | Le niveau enseigne-t-il par usage ? | Oui : chunks `intro`, Ascension 0, grappes d'éclats sur l'arc idéal. |
| | Les obstacles révèlent-ils les clés ? | Oui : chaque obstacle a un atome, et la compétence est la clé (une herse s'ouvre au timing). |
| Sens | Que signifie chaque mécanique ? | La marée est l'oubli, la gravure est la mémoire, l'autel est le souvenir sauvé. |
| | Incohérence entre mécanique et fiction ? | Le seul point douteux est que les autels font « revivre » plus haut. La fiction répond : le Veilleur renaît là où sa flamme brûle encore. |
| Apprentissage | Quel pattern apprendre ? | Les hauteurs canoniques (+3, +5, volte) et les horloges des pièges. |
| | Quel feedback corrige le modèle mental ? | La gravure montre exactement ce qui a tué, et le fantôme montre où l'on était. |
| | Quelle stratégie devient naturelle après 30 minutes ? | Bond et Élan en rythme, volte réservée aux urgences. |
| | Et quand elle est maîtrisée ? | B3 (eau) la casse, B5 (vent) la tord, B6 (Ombre) interdit l'attente. Le Défi hebdo ajoute une contrainte, et la Résonance un défi de précision. |
| | La complexité crée-t-elle un nouveau champ de maîtrise ? | Oui : recharges cyan en chaîne, frôlés, Rythme 30 (le plafond expert). |

### 12.2 Filtre de complexité (chaque règle paie-t-elle son coût ?)

| Règle ajoutée | Ce qu'elle apprend | Possibilité nouvelle | Verdict |
|---|---|---|---|
| Élan | Doser l'intention verticale | Deux hauteurs depuis un seul geste | **Gardée** (P0) |
| Recharge cyan | Utiliser ses morts | Routes de volte multiples | **Gardée** (P0) |
| Complice | Une cause indirecte reste une cause | Graver le non-létal | **Gardée** (P0) : aucun geste en plus |
| Rythme | Ne pas s'attarder | Récompense de vitesse | **Gardée** (P0) : feedback seulement |
| Résonance | Suivre une ligne | Défi de précision | P1 : utile seulement aux experts |
| Inventaire de power-ups | — | Choisir quand activer | **Refusée** : nécessite un deuxième bouton |
| Dash par swipe | — | — | **Refusée** (section 2.1) |

### 12.3 Risques et parades

| Risque | Probabilité | Impact | Parade |
|---|---|---|---|
| L'Élan rend le tap « mou » (latence perçue) | Moyenne | Fort | Le bond part **à la pression**, et l'Élan ne modifie que la gravité après 0,10 s. Aucune entrée n'est différée. À tester dès la semaine 1. |
| Les autels banalisent les 4 vies | Moyenne | Moyen | La marée repart, le score est l'altitude max, et les gravures sous l'autel ne servent plus. Un mutateur « Une vie » pour les puristes. |
| Assemblage injuste (mur infranchissable) | Faible | Très fort | Validateur headless sur chaque chunk, 2 rangées tampon, robot sur 12 graines à chaque build. |
| Volume de contenu trop grand pour 1 programmeur | Forte | Fort | Chunks en ASCII (environ 15 min chacun), miroir ×2, remix au-delà de 1600 m, P0 limité à 3 biomes. |
| Lisibilité en pixel art (pièges perdus dans le décor) | Moyenne | Fort | Bandes de luminance de la palette v2 (murs Y ≤ 0,13, jeu Y ≥ 0,25), rampe danger réservée, test en niveaux de gris. |
| Le cyan rend le jeu trop facile | Moyenne | Moyen | Au plus 4 gravures directes et 2 Burins par ascension, et le boss n'est jamais gravé en entier. |
| Rétention J7 faible (benchmark hypercasual de 5 à 10 %, médiane < 4 %) | Forte | Fort | Méta hybrid-casual : missions, série, chaîne hebdo, codex. Viser J1 ≥ 35 % et J7 ≥ 10 %. |
| Pubs perçues comme intrusives | Faible | Fort | Vidéos uniquement choisies, aucune dans les modes classés, au plus 6 par jour. |
| Performances sur Android d'entrée de gamme | Moyenne | Moyen | gl_compatibility, 192 × 352 en logique, au plus 40 nœuds animés à l'écran, pas de shader en P0 (obscurité par masque de tuiles). |
| Pas de simulation de 120 Hz trop coûteux | Faible | Moyen | Physique maison simple (AABB et cercles), sans moteur physique. Profiler sur un appareil cible en semaine 2. |

---

## 13. Priorisation (un programmeur GDScript, art en pixel texte)

### P0 — « Ascension complète » (≈ 73 jours de travail, soit environ 15 semaines)

Le P0 est déjà nettement plus riche que le prototype : 3 verbes contre 2, 14 obstacles contre 3, 3 biomes contre 1, un boss, des power-ups, des autels et une méta complète.

| Lot | Contenu | Estimation |
|---|---|---|
| Physique | Pas fixe à 120 Hz, Élan, coyote, buffer, hitbox 6 × 10, frôlé, combo Rythme | 4 j |
| Écho | Recharge cyan, complice, éclat d'écho, gravure des ennemis, Burin | 4 j |
| Chunks | Chargeur ASCII, assembleur (graine, miroir, étiquettes), validateur headless, robot sur 12 graines | 9 j |
| Obstacles (14) | O1, O2, O3, O4, O5, O6, O8, O9, O10, O11, O12, O18, O19, O20 | 12 j |
| Biomes (3) | B1 Crypte, B2 Fonderie, B3 Bibliothèque : tuiles, fonds, transitions, autels | 7 j (art compris) |
| Boss | Le Sonneur (B1) et la règle des runes réutilisable | 4 j |
| Power-ups | Burin, Plume, Accalmie | 2 j |
| Contenu | 90 chunks (30 par biome, introductions comprises) | 10 j |
| Positifs | Grand éclat, éclat d'écho, plumes dorées B1 à B3, pluie d'éclats | 2 j |
| Onboarding | Ascension 0, pictogrammes, fantôme-guide | 3 j |
| Méta | Niveaux 1-50, tenues 1-16, missions quotidiennes, 30 succès (locaux), codex | 6 j |
| Modes et pub | Ascension, Tour du jour et partage (adaptation du prototype) ; AdMob récompensé (+1 vie, ×2) | 4 j |
| Polish et tests | Game feel, sons, équilibrage de la marée, tests sur appareil | 6 j |

### P1 — « Tour entière » (≈ 10 semaines)

- Biomes B4 Jardin et B5 Clocher.
- Obstacles O7, O13, O15, O16, O17 et O21.
- Boss du Forgeron, de la Mère-Phalène, de l'Œil et de la Girouette.
- Power-ups Aimant, Lanterne et Élan d'or.
- Reliques et fragments.
- Brèches, alcôves et salle de défi.
- Résonance.
- Chaîne hebdo, Défi hebdo à mutateurs, Zen et bestiaire.
- Google Play Games (classements et succès en ligne).
- Tenues 17 à 22 et événements Éclipse, Carillon et Écho errant.
- 80 chunks supplémentaires.

### P2 — « Sommet et saisons »

- Biome B6 Sommet céleste.
- Givre (O14), l'Ombre (O22) et le boss du Silence.
- Remix au-delà de 1600 m.
- Défis spéciaux saisonniers et tenues de saison (23, 24).
- Variantes de traînée d'écho.
- Éclat de lune du Tour du jour.
- 30 chunks supplémentaires.

**Coupes de secours, dans l'ordre :**
1. Si le P0 dérape, le boss du Sonneur passe en P1. L'arène reste, avec runes seules.
2. Ensuite, B3 passe en P1 (et avec lui O6, O12, O18 et O19). On garde 10 obstacles et 2 biomes, ce qui reste plus riche que le prototype.
3. Ne jamais couper l'Élan ni la recharge cyan : ce sont eux qui donnent au jeu sa profondeur.

---

## 14. Sources

Les analyses tierces ont été consultées par recherche web. Deux pages (maddymakesgames.com, thumbsticks.com) n'ont pas pu être ouvertes directement dans la session : elles sont citées d'après leurs extraits de recherche. Les valeurs de coyote de Celeste, données à 5-6 frames selon les sources, ne sont qu'un ordre de grandeur.

**Prototype et studio**
- `jeu/DESIGN.md` v0.1, `jeu/game/scripts/world.gd`, `tower.gd`, `game_state.gd` : constantes physiques, marée, pièges, Tour du jour, robot de test.
- `jeu/studio/BRIEF.md` (contraintes), `jeu/studio/palette_v2.txt` (palettes des biomes et des rampes de gameplay).
- Persona Milo Hartmann : `design_review_checklist`, `theory_of_fun_layer`, `teaching_engine`, `game_feel_engine` ; patterns Escalating Challenge, Escalating Complexity, Dynamic Friction, Stopping Mechanism.

**Downwell (un bouton, risque/récompense, combos)**
- GDC Vault, Ojiro Fumoto, « Polishing the Boots: Designing Downwell » — https://www.gdcvault.com/play/1023533/Polishing-the-Boots-Designing-Downwell
- TouchArcade, 02/06/2016 — https://toucharcade.com/2016/06/02/watch-downwell-developer-ojiro-fumoto-talk-about-how-he-designed-his-fantastic-platformer/
- Game Developer, « Designing Downwell around one key mechanic » — https://gamedeveloper.com/design/video-designing-i-downwell-i-around-one-key-mechanic
- Game Developer, « Elegance, not simplicity… Downwell » — https://gamedeveloper.com/design/elegance-not-simplicity-devs-weigh-in-on-i-downwell-s-i-irresistible-charm
- PC Gamer, « The compulsive chain combos of Downwell » — https://www.pcgamer.com/au/the-compulsive-chain-combos-of-downwell
- Kill Screen, « The tricky brilliance of Downwell's gunboots » — https://www.killscreen.com/the-tricky-brilliance-of-downwells-gunboots/
- Thumbsticks, GDC 2016, Fumoto (extrait de recherche) — https://www.thumbsticks.com/gdc-2016-ojiro-fumoto-on-polishing-downwells-gun-boots/

**Leap Day (plateforme à un doigt, chunks faits main)**
- TouchArcade, test du 26/05/2016 — https://toucharcade.com/2016/05/26/leap-day-review-jump-for-joy/
- Pocket Gamer, « Leap Day: one thumb platforming… » — https://www.pocketgamer.com/articles/070129/leap-day-one-thumb-platforming-dished-up-by-a-sadist/
- PocketGamer.biz, interview Nitrome : chunks faits main, environ 2000 chunks, plus de 70 pièges, checkpoints — https://www.pocketgamer.biz/interview/63249/leap-day/
- Wikipédia, Super Leap Day — https://wikipedia.com/wiki/Super_Leap_Day

**Spelunky et génération par blocs d'auteur**
- Darius Kazemi, « Spelunky's Procedural Space » (salles de 10 × 8, grille de 4 × 4, chemin garanti) — https://tinysubversions.com/2009/09/spelunkys-procedural-space/index.html
- Boing Boing, 09/12/2013, sur la génération des niveaux de Spelunky — https://boingboing.net/2013/12/09/how-spelunkys-levels-are-gen.html
- Game Maker's Toolkit, « How and Why Spelunky Makes its Own Levels » (vidéo).
- 80.lv, bonnes pratiques de la procgen commerciale — https://80.lv/articles/game-developer-on-best-practices-for-procgen-in-commercial-games
- Game Developer, « How procedural level design works in Eldritch » — https://gamedeveloper.com/design/video-how-procedural-level-design-works-in-i-eldritch-i-

**Celeste (clémence : coyote, buffer, hitbox)**
- Gigazine, 17/03/2020, résumé du fil de Maddy Thorson — https://gigazine.net/gsc_news/en/20200317-celeste-action-feel-things
- Blizzard Watch, 13/03/2020 — https://blizzardwatch.com/2020/03/13/celeste-developer-game-feel/
- GameSpot, « Celeste dev explains how they made their game feel » — https://www.gamespot.com/articles/celeste-dev-explains-how-they-made-their-game-feel/1100-6474775/
- Maddy Thorson, « Celeste & Forgiveness » (extrait de recherche) — https://maddymakesgames.com/articles/celeste_and_forgiveness/

**Atomes de compétence et théorie du fun**
- Daniel Cook, « The Chemistry of Game Design » (2007) — https://www.gamedeveloper.com/pc/feature-the-chemistry-of-game-design-
- Raph Koster, « An atomic theory of fun game design » — https://www.raphkoster.com/?p=4090
- Raph Koster, *A Theory of Fun for Game Design* ; Steve Swink, *Game Feel* (via la persona).

**Rétention et marché**
- Juego Studio, rétention hypercasual (J1 20-30 %, J7 5-10 %, J30 < 2 %) — https://www.juegostudio.com/blog/how-to-increase-user-retention-and-increase-your-games-lifetime
- MWM, glossaire de la rétention à N jours — https://mwm.ai/glossary/n-day-retention
- GameAnalytics, benchmarks mobile et PC 2026 (J7 médian < 4 %) — https://gameindustrylibrary.com/documents/gameanalytics-mobile-and-pc-game-benchmarks-in-2026-sponsored-by-pwn-games
- Appodeal, Mobile Casual Benchmarks 2025 (l'hybrid-casual dépasse l'hypercasual en rétention) — https://gameindustrylibrary.com/documents/mobile-casual-benchmarks-report-2025

**Vidéo récompensée**
- Unity, « How to level up your rewarded video monetization » — https://unity.com/blog/how-to-level-up-your-rewarded-video-monetization
- AppSamurai, bonnes pratiques de placement des vidéos (opt-in) — https://appsamurai.com/blog/best-practices-of-video-ad-placement-in-mobile-games/
- Business of Apps, vidéo récompensée — https://businessofapps.com/ads/rewarded-video

**À traiter avec prudence**
- Geometry Dash, mode entraînement à checkpoints : aucune source primaire fiable trouvée. L'idée des autels vient surtout des checkpoints de Leap Day.
