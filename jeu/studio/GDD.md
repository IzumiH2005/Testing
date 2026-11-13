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
5. **1,51 s** : l'écran de vie suivante s'affiche : « Vie 2/4 », bouton de redémarrage et bouton « Vidéo : +1 vie » si disponible (section 10.4).

### 3.4 Gardes-fous

- Le graphe d'une ascension comporte **au plus 4 gravures directes** (3 sans pub). Avec un Burin, on peut en ajouter, mais il y a au plus 2 Burins par ascension.
- Les **boss ne se gravent pas en entier** : seule l'attaque précise qui a tué devient cyan (un rocher, une onde), et seulement pour la tentative suivante.
- Les **ennemis gravés** (phalène, grignon, sentinelle) deviennent cyan, inoffensifs et rechargent la volte. Ils restent visibles, ce qui garde le monde vivant.
- En **Tour du jour**, les gravures restent actives (c'est le cœur du jeu). En **Défi « Sans écho »**, elles sont désactivées et le joueur est prévenu sur l'écran du défi.
