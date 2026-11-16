# Bible d'animation de stickman

Ce document dit **comment animer** un stickman qui se bat pour que ce soit naturel, lisible
et cool. Il est tiré de l'étude image par image de vidéos de référence faites par de bons
animateurs. Chaque règle renvoie aux images qui la prouvent.

- `INVENTAIRE.md` dit **quelles** animations faire. Ce document dit **comment** les faire.
- Quand une règle d'ici contredit une animation existante, c'est l'animation qu'on corrige.
- Le document grossit à chaque nouvelle vidéo étudiée (§ 13). Une règle confirmée par
  plusieurs vidéos est marquée « confirmée ». Pour l'instant tout vient d'une seule vidéo.

## Vidéos étudiées

| N° | Vidéo | Format | Étude |
|---|---|---|---|
| 1 | « Strength vs Speed » (Stick Nodes) | 24 i/s, 494 images, 20 s | `etudes/01_strength_vs_speed/` |

Les numéros d'images cités plus bas, comme (176-180), sont ceux de la vidéo 1, comptés à
partir de 0.

## Unités

- **i24** : une image de la référence, à 24 images par seconde (42 ms).
- **i60** : une image de notre jeu, à 60 images par seconde. **1 i24 = 2,5 i60.**
- **H** : la hauteur du personnage debout. Dans la vidéo 1, H = 120 px et la tête fait
  27 px. Chez nous, H = 180 unités et la tête fait 46.
- Les distances sont données en H pour pouvoir passer d'un personnage à l'autre.

| i24 | 1 | 2 | 3 | 4 | 5 | 6 | 8 | 12 | 14 |
|---|---|---|---|---|---|---|---|---|---|
| i60 | 2 ou 3 | 5 | 7 ou 8 | 10 | 12 ou 13 | 15 | 20 | 30 | 35 |

---

## 1. Les douze règles

1. **Un coup, c'est deux dessins.** La pose armée, puis la pose de contact, sans dessin du
   bras à mi-chemin. Le trajet est montré par une traînée, pas par des intervalles (§ 4).
2. **Le temps va dans l'armé et dans la tenue, pas dans le trajet.** Un coup lourd, c'est
   12 i24 de préparation, 1 de frappe, 9 de récupération (§ 2).
3. **Le corps entier frappe.** Sur l'image du contact, tout le corps avance d'environ
   0,45 H et s'aligne du pied arrière au poing (§ 4).
4. **Un bras n'est jamais mou ni à moitié ouvert.** Il est soit replié serré, soit tendu
   à fond, soit jeté à l'opposé en contrepoids (§ 3).
5. **Le bras ne s'arrête pas sur la cible.** Il la traverse, puis continue son arc. Il ne
   revient pas par où il est venu, sauf pour un coup rapide (§ 4).
6. **Les poses sont penchées et larges.** Buste à 45° dans un armé, pieds écartés de
   0,5 à 0,8 H, bassin bas. Un personnage droit sur ses pieds n'a pas de force (§ 3).
7. **Un seul personnage rapide à la fois.** Pendant que l'un agit, l'autre tient sa pose
   ou glisse (§ 2).
8. **Les tenues vivent.** Une pose tenue dérive de 0,5 à 2 px par image ou se tasse d'un
   pixel à la fin. Seule la pose de fin de combat est totalement figée (§ 2).
9. **Le touché se plie autour du point d'impact** et la partie touchée part en premier ;
   la tête, les bras et les pieds suivent avec une image de retard (§ 7).
10. **Les vitesses ne sont jamais régulières.** Un départ double à chaque image, un arrêt
    divise par deux à chaque image, un saut s'étire au sommet (§ 8).
11. **Les effets marquent la force, et ils sont rares.** Traînée sur chaque coup ; secousse,
    arrêt sur image, flou et fantômes seulement sur les coups qui comptent (§ 9).
12. **Le caractère se lit dans le rythme.** Le costaud prépare longtemps et paie ses ratés ;
    le rapide frappe en 2 images sans prévenir (§ 10).

---

## 2. Rythme

### Tenues et rafales

Le combat alterne des **tenues** (rien ne bouge, ou presque) et des **rafales** (tout change
à chaque image). Il n'y a presque pas de mouvement « moyen ».

| Moment | Durée | Preuve |
|---|---|---|
| Pause entre deux actions pendant la mise en place | 12 à 15 i24 | 35-49, 65-79, 86-97, 113-127 |
| Armé d'un coup lourd, tenu | 4 à 5 i24 | 136-139, 176-180 |
| Tenue avant un coup final | 14 i24 | 411-424 |
| Tenue après un coup final | 14 i24 | 426-439 |
| Pose de fin d'un coup réussi | 4 à 7 i24 | 167-171, 205-208, 339-345 |
| Pose de fin d'un coup raté (bloqué, sans défense) | 5 à 6 i24 | 142-146, 224-229 |
| Respiration entre deux groupes de coups d'une rafale | 2 à 3 i24 | 294-297, 301-302 |

Pendant un échange, un personnage ne reste jamais immobile plus de 8 i24, et l'autre bouge
pendant ce temps (254-261, 322-327).

### Une tenue n'est pas un arrêt

- Pendant un armé tenu, la pose dérive de 1 à 2 px par image (176-180).
- Pendant la suspension avant le coup final, les deux corps glissent l'un vers l'autre de
  0,5 px par image (411-422).
- Pendant la tenue d'impact, le frappeur continue d'avancer de 1,3 px par image dans le
  touché (426-439).
- Une pose qui s'arrête dépasse sa position de 2 ou 3 px, revient, puis se tasse d'un
  pixel (83-85, 64-67). C'est ce qui donne le « claquement ».

### Rapport entre les phases d'un coup

| | Préparation | Frappe | Récupération | Cycle |
|---|---|---|---|---|
| Costaud, coup lourd | 12 i24 | 1 i24 | 9 i24 | ≈ 22 i24 |
| Costaud, direct | 2 à 4 i24 | 1 i24 | 3 à 4 i24 de tenue | 5 à 6 i24 |
| Rapide, coup d'une rafale | 0 | 1 i24 | 1 i24 de retrait | 2 i24 |
| Rapide, premier coup d'une rafale | 3 i24 | 1 i24 | 1 i24 | 5 i24 |

### Composer une rafale

- Seul le premier coup a un armé. Les suivants partent de la position de retrait (152-160).
- On groupe les coups : 3, puis 2, puis 1, avec 2 à 3 i24 de respiration entre les groupes
  (288-304).
- On change de hauteur et de forme à chaque coup : torse, ventre, par-dessus, crochet bas,
  crochet haut, marteau.
- Un coup sur deux ou trois est « appuyé » : contact tenu 2 i24 avec une secousse.
- Le dernier coup est précédé de 3 i24 de quasi-tenue (161-163) et c'est lui qui a le plus
  gros effet.

### Qui a l'initiative

L'initiative change toutes les 15 à 35 i24, toujours sur une tenue ou sur un raté. Un coup
raté ou une pose de fin trop longue est la porte par laquelle l'autre entre.

L'adversaire réagit en retard : il ne commence à bouger que 6 i24 après le premier
frémissement de l'attaquant (128 → 134), et il attend le dernier moment pour esquiver (les
têtes sont à 0,35 H l'une de l'autre en 139).

---

## 3. Poses

### La ligne du corps

- Chaque pose forte tient sur **une ligne simple** : une diagonale (charge, armé, fente), un
  C (plié sur un coup), un S (sonné), une barre horizontale (direct en extension).
- Les deux personnages ont des lignes **opposées** sur la même image : diagonale contre
  verticale (176-180), barre horizontale qui traverse une forme verticale (152, 156, 158),
  C fermé au-dessus d'une ligne couchée (142).
- Les deux têtes ne sont jamais à la même hauteur sur une image de contact.
- Dans une pose armée en l'air, les quatre membres partent dans quatre directions et aucun
  ne se superpose (136-138).

### Penché, large, bas

| Pose | Buste | Écart des pieds | Bassin |
|---|---|---|---|
| Debout, neutre (fin de combat) | vertical | pieds joints | haut |
| Garde du rapide | 20° vers l'avant | 0,47 H | 0,43 H du sol |
| Posture du costaud | presque vertical | 0,72 H | 0,40 H, genou arrière à 0,14 H du sol |
| Armé d'un coup lourd | 45° à 50°, d'un seul trait du pied arrière à la tête | 0,8 H | bas |
| Fente pendant une rafale | 0° à 30°, alterne à chaque coup | 0,8 H | 0,12 à 0,17 H plus bas que la garde |
| Charge | 60° à 70° | grandes foulées | bas, la pose fait 0,9 H de long |
| Contact d'un coup en fente | 80° à 90°, presque horizontal | 1 H et plus | bas |
| Coup lourd raté | 80°, tête plus basse que le bassin | — | haut, jambe avant tendue |

La jambe arrière est **tendue** dans presque toutes les poses d'attaque : elle prolonge la
ligne du buste. La jambe avant est pliée et porte le poids.

### Les bras

C'est le point le plus important, et le plus raté chez nous.

- **En garde** : coude fermé à 90° ou moins. Le rapide a un poing détaché devant le visage
  (à 0,2 H) et le coude arrière levé à l'horizontale. Le costaud a un poing collé sous le
  menton et l'autre bras en équerre (bras horizontal, avant-bras vertical vers le bas).
- **Armé d'un coup lourd** : le bras monte d'abord presque tendu vers l'arrière et le haut
  (175), puis le coude se ferme (176). Le poing finit **derrière la tête**, à une tête
  au-dessus de l'épaule. L'angle au coude est de 90° au plus, souvent moins : l'avant-bras
  est rabattu vers la tête, jamais ouvert vers le ciel.
- **Bras libre pendant l'armé** : replié serré contre la poitrine, poing sous le menton
  (176-180). Pendant une approche en courant, il est tendu vers la cible comme une visée
  (137-139), puis il se replie au moment où l'autre part : les deux bras s'échangent.
- **Juste avant de partir** : 1 i24 où le coude monte en pointe et où le poing recule
  encore (140, 181). Ce recul courbe la trajectoire.
- **Au contact** : bras tendu à fond, étiré à environ 1,4 fois sa longueur, pendant **une
  seule image** (141, 152). Tenu 2 i24 seulement sur un coup appuyé (201-202).
- **Bras libre au contact** : jeté à l'opposé. Tendu en arrière à l'horizontale (158, 288),
  ou jeté en l'air (182). Il sert alors d'armé au coup suivant.
- **Crochet** : le coude ne se tend jamais (100° au contact, 298). La traînée est un arc.
- Un bras ne pend que dans trois cas : après un atterrissage lourd (29-30), après un coup
  raté (142-146), ou quand le personnage est sonné.

### Étirer

Les membres changent de longueur. Un bras de frappe fait 1,4 fois sa taille au contact. La
jambe du coup de pied final est étirée jusqu'à 0,9 H (164). La jambe de départ d'un dash
peut doubler (217). L'étirement dure une image.

---

## 4. Le coup de poing

### Coup lourd du bras arrière (le nôtre : `coup_de_poing_rue`)

Référence : 173-187 (marteau au sol), 196-208 (cueillette), 128-146 (coup en courant).

| Phase | i24 | i60 | Ce qui se passe |
|---|---|---|---|
| Recul | 2 à 3 | 5 à 8 | Grand pas arrière (0,65 H). Le bras de frappe monte presque tendu vers l'arrière. |
| Fermeture | 1 | 2 ou 3 | Le coude se ferme, le poing vient derrière la tête. Le bras libre se colle à la poitrine. |
| Armé tenu | 4 à 5 | 10 à 12 | Buste à 45° d'un seul trait avec la jambe arrière. La pose dérive de 1 à 2 px par image. |
| Déclenchement | 1 | 2 ou 3 | La tête tombe de 0,1 H, le coude monte en pointe, le poing recule encore. Début de traînée. |
| Contact | 1 | 2 ou 3 | Le poing fait 0,9 à 1,4 H d'un coup. Le corps avance de 0,45 H. Bras tendu, étiré. Traînée complète. |
| Arrêt sur image | 1 | 2 ou 3 | Même dessin que le contact. Seule la caméra bouge. |
| Dépassement | 1 à 2 | 3 à 5 | Le bras continue son arc (jusqu'au sol, ou par-dessus la tête). Le buste a tourné. |
| Pose de fin | 4 à 7 | 10 à 18 | Pose déséquilibrée tenue, sur une jambe ou très penchée. |
| Retour | 4 à 5 | 10 à 12 | 2 i24 par pose. |

Ordre de départ des parties du corps : tête et buste, puis poussée de la jambe arrière, puis
pied avant qui se plante, puis épaule et coude qui montent, puis le bras, puis le buste qui
suit et tombe. **Le poing part en dernier** (128-142). La tête freine juste avant que le bras
parte (de 28 à 6 px par image en 140) : la vitesse passe du corps au bras.

Si le coup rate, le personnage est emporté : buste à 80°, tête sous le bassin, un bras qui
pend, pendant 5 à 6 i24 (142-146, 224-229).

### Direct

| Phase | i24 | Ce qui se passe |
|---|---|---|
| Avant | 0 à 1 | Coude fermé à fond, poing à moins d'une tête de l'épaule. |
| Contact | 1 | Bras tendu à l'horizontale. Le bassin avance de 0,2 à 0,3 H. Jambe arrière, buste et bras sur une diagonale. |
| Retrait | 1 | Le poing revient à la poitrine par le même chemin. Jamais derrière l'épaule. |

Le poing **traverse** la cible : il ressort de l'autre côté de la silhouette de l'adversaire
(152-160). On ne l'arrête pas à la surface.

### Autres coups de poing

- **Crochet** (298) : armé d'une image en tirant l'épaule en arrière et vers le bas. Le coude
  reste plié. Le corps se redresse au lieu de plonger.
- **Coup descendant, marteau** (304, 321) : poing levé au-dessus de l'épaule pendant 1 i24,
  puis le buste tombe à l'horizontale avec le bras. Pour le costaud, la jambe arrière monte
  à l'horizontale en contrepoids.
- **Moulinet** (233-238) : un seul tour de bras tendu donne deux contacts à 5 i24 d'écart.
  Le buste bascule de 25° en arrière à 70° en avant pour faire tourner le bras. Le tour sert
  d'armé au second coup.

### Avancer en frappant

L'attaquant avance de 0,1 à 0,25 H à chaque coup. Le touché ne recule que de 0,03 à
0,15 H. L'attaquant finit donc collé à l'adversaire, la tête sous la sienne (151-160).

---

## 5. Les coups de pied

- **Pas d'image de trajet non plus.** On passe de l'armé au contact (164, 266, 272).
- **Coup de pied au ventre, jambe arrière** (161-171) : 3 i24 de quasi-tenue où le pied
  arrière se rapproche de 0,15 H. Puis contact : jambe étirée, buste basculé à l'opposé (vers
  l'avant et le bas, tête à hauteur de hanche), jambe d'appui verticale. Arrêt de 2 i24.
  Ensuite la jambe ne redescend pas : elle se plie en L et reste en l'air 5 i24.
- **Balayage** (264-266) : la jambe traînante de la course sert d'armé (pliée à 90°
  derrière). Le bassin s'écrase à 0,3 H du sol, puis la jambe fouette sur 1,1 H en une image.
  Le buste part à l'opposé de 25 à 30°, les bras s'ouvrent en croix, le pied d'appui ne bouge
  pas.
- **Coup de pied sauté** (267-276) : 4 i24 de suspension au sommet, la jambe pend à la
  verticale 1 à 2 i24, puis elle balaie 90° en une image, tendue. Buste en arrière de 15°,
  bras serrés. Le genou se replie dès l'image suivante. Réception sur l'autre jambe, la jambe
  de frappe encore levée 2 i24.

---

## 6. Déplacements

### Départ de course ou de charge

- Le départ commence par **la tête**, les pieds ne bougent pas : 4 i24 de bascule où la tête
  fait 1, 3, 10, 22 px (128-131). La vitesse double à chaque image.
- Le corps passe par-dessus le pied avant avant de pousser : le pied reste planté 8 i24
  pendant que la tête parcourt 1 H.
- Pleine vitesse : 0,2 à 0,28 H par i24, soit 5 à 7 H par seconde. Buste à 60-70°.
- Aucun effet pendant une charge normale. La vitesse est dite par la pose.

### Dash du rapide (214-222)

- 3 i24 de plongée où la tête descend à 60 % de sa hauteur.
- Puis 1,4 H en **une** image, avec 2 copies floues derrière lui. Il traverse l'adversaire.
- Freinage : 39, 27, 6, 3 px.

### Vitesse extrême (357-410)

Le corps disparaît et il ne reste que des lignes de vitesse (§ 9). Le personnage sort d'un
côté et revient par ce même côté, à une hauteur et un angle différents à chaque passage.

### Saut et vol

- Montée en 2 i24 (0,36 H puis 0,27 H), suspension de 4 i24 à moins de 3 px d'écart,
  descente qui accélère (6, 12, 21 px).
- Au sommet, le corps se groupe : genoux hauts, bras sur la tête.
- Voir § 8 pour les tables d'espacement.

### Atterrissage (24-36)

Trois poses sur trois images consécutives, sans intervalle :

1. **Contact étiré** : bras à la verticale, jambes presque tendues, hauteur maximale.
2. **Écrasement** : bloc compact à 72 % de la hauteur de l'image précédente.
3. **Amorti** : buste à 45°, mains sur le genou.

Puis remontée à pas décroissants (7, 5, 3, 0,5 px) et recul de la tête de 3 px. Les bras ont
une image de retard sur le corps. Après un atterrissage lourd, on ne revient pas debout : la
pose finale reste à 86 % de la hauteur.

### Se relever (50-67)

- Deux frémissements de 1 à 3 px, tenus 2 i24 chacun, avant de partir.
- 9 i24 pour ramener les pieds sous le corps, sans monter (la tête ne prend que 4 px).
- Puis la montée en 6 i24 : 1, 2, 6, 12, 14, 15, 9, 2 px.
- Il se relève **en avançant** de 0,5 H vers l'adversaire.
- Un bras traîne derrière et ne rejoint le corps qu'à l'arrêt.
- Un petit pas de réajustement juste avant l'arrêt (pied soulevé une image).

### Prendre sa garde

- Rapide : 6 i24. Une d'anticipation, deux de mouvement, la pose, deux de rebond. Le poing
  arrive en dernier et fait son plus grand écart sur la dernière image (80-85).
- Costaud : 15 i24. Redressement lent, genou monté à hauteur de poitrine pendant 3 i24,
  puis frappe du pied au sol en une image avec une petite secousse. Les poings arrivent en
  place sur l'image où le pied touche (98-112).

---

## 7. Le touché

### Règle générale

Sur l'image du contact : la partie touchée part, le corps se plie autour du point d'impact,
et le reste traîne du côté opposé. Le plus grand déplacement est sur l'image du contact ou
la suivante. Ensuite la vitesse est divisée par 1,5 à 2 à chaque image.

| Coup reçu | Forme du corps | Déplacement | Suite |
|---|---|---|---|
| Poing au corps (152-160) | plié par-dessus le poing, pieds presque fixes | recul de 0,03 à 0,15 H, retour élastique de 2 à 6 px | la posture se dégrade à chaque coup : debout, voûté, à l'équerre, recroquevillé |
| Direct au torse ou à la tête (288, 310) | arc vers l'arrière, bras jetés en l'air | 0,3 à 0,45 H | le léger reste sonné en S 4 i24 ; le lourd reprend sa garde en 1 à 2 i24 |
| Marteau sur la tête (304) | V, tête en bas | — | — |
| Pied au ventre (164-171) | plié en portefeuille, bassin en arrière, tête et pieds en retard | 0,3 H à l'image du contact, puis 36, 22, 10, 10, 7, 8, 7 px | il glisse au ras du sol (pieds à 0,13 H), il ne s'envole pas |
| Coup lancé vers le haut (182-200) | part par le bassin, membres pendants, puis les jambes passent devant | monte à 1,4 H | un tour complet en 18 i24 |
| Grand coup en fente (201-205) | — | 0,7 H par image pendant 3 i24, puis arrêt en 1 image | réception pieds puis genou à terre |
| Passage à vitesse extrême (358-403) | la partie touchée part, tête et bras tendus traînent à l'horizontale | recul de 0,17 à 0,3 H | la tête s'enfonce de 0,15 H puis remonte en 1 à 2 i24 |

### Le poids

- Le lourd encaisse sans tomber et ne vole pas. Le léger s'envole et reste sonné.
- L'usure se montre par la récupération qui disparaît : après quelques coups, le personnage
  ne se redresse plus entre deux impacts (374 → 392, sa silhouette passe de 1 H à 0,6 H).
- La pose de réaction ne se répète jamais d'un coup à l'autre (360, 367, 384, 392).

### Recul amorti

Après un gros coup ou une poussée, le touché glisse 4 à 6 i24 à pas décroissants (32, 41,
33, 17, 4, 2 px), jambes écartées, une jambe tendue en frein (338-343).

### Transformer le recul

Un bon personnage ne « subit » pas longtemps : il atterrit sur un pied, s'accroupit 3 i24,
fait un grand pas arrière, et ce pas est déjà l'armé du coup suivant (169-175).

---

## 8. Tables d'espacement

Écarts d'une image à la suivante, en pixels de la vidéo 1 (H = 120 px). Pour nos unités,
multiplier par 1,5.

| Mouvement | Écarts par i24 | Preuve |
|---|---|---|
| Départ de charge (tête) | 0,7 · 2 · 5 · 11 · 22 · 29 · 30 | 129-135 |
| Départ en vitesse extrême | 3 · 10 · 37 · hors champ | 355-358 |
| Poing d'un coup lourd | 110 à 165 en une image | 141, 182, 201 |
| Poing d'un direct | 45 à 70 en une image | 288, 310 |
| Freinage après un dash | 39 · 27 · 6 · 3 | 219-222 |
| Recul après un coup | 37 · 24 · 22 · 17 · 15 · 12 · 6 | 366-372 |
| Glissade après une poussée | 32 · 41 · 33 · 17 · 4 · 2 | 338-343 |
| Lancé en l'air, montée | 65 · 53 · 38 · 7 | 182-185 |
| Lancé en l'air, sommet | 5 à 6 images presque immobiles | 186-191 |
| Lancé en l'air, chute | 6 · 12 · 32 · 70 | 196-200 |
| Projection horizontale | 82 · 81 · 63 · arrêt | 202-205 |
| Remontée après écrasement | 7 · 5 · 3 · 0,5 | 28-32 |
| Se relever (tête) | 1 · 2 · 6 · 12 · 14 · 15 · 9 · 2 · 0 · −1 | 56-67 |
| Chute contrôlée | 16 · 36 · 16 · 8 · 5 | 277-282 |

Ce qu'il faut en retenir :

- Un départ **double** (ou plus) à chaque image, sur 3 à 6 images.
- Un arrêt après un coup est **brutal** : une ou deux images. Un arrêt après une glissade
  divise par deux à chaque image.
- Un saut n'est pas une parabole régulière : la montée freine, le sommet dure, la chute
  double.
- La rotation en l'air n'est pas régulière non plus : 40° par image à la montée, presque 0
  au sommet, 15° par image à la chute.

---

## 9. Effets

Les effets de la vidéo 1 sont des dégradés et des transparences, pas des dessins. On peut
donc les **calculer** au lieu de les dessiner : à partir des positions du squelette à
l'image précédente et à l'image courante. Chaque effet ci-dessous donne ce qu'on voit, puis
ce que la fonction doit faire.

### 9.1 Traînée de membre (smear)

C'est l'allongement courbe qu'on voit derrière le poing du rouge en 140-141.

- **Ce qu'on voit** : une bande de la largeur du membre, qui suit le chemin parcouru par le
  poing ou le pied depuis l'image précédente. Elle a la couleur du personnage, opaque près
  du membre, transparente à l'autre bout. Elle est courbe, parce que le membre tourne autour
  de l'épaule ou de la hanche. Elle dure **une image** (deux pendant un arrêt sur image).
- **Longueur** : de 25 px pour un retrait à 150 px pour un balayage (0,2 à 1,25 H).
- **Elle apparaît aussi sur l'armé** quand il est rapide (303, 320), et sur le retrait.
- **Formes** : arc au-dessus du bras pour un coup par-dessus, croissant sous le bras pour
  un crochet, éventail qui part du sol pour un coup de pied, boucle presque fermée pour un
  retrait, trois quarts de cercle pour un marteau.
- **Fonction** : `trainee(os, pose_avant, pose_apres)`.
  - Elle se déclenche toute seule quand l'extrémité d'un membre bouge de plus de 0,3 H
    entre deux poses.
  - Elle échantillonne 8 à 12 positions de l'extrémité entre les deux poses, en
    interpolant les **angles** des os (pas les positions), ce qui donne l'arc.
  - Elle trace un ruban de la largeur du trait le long de ces points, opacité de 0 % au
    plus ancien à 100 % au plus récent.
  - Elle s'efface à l'image suivante.

### 9.2 Étirement du membre

- **Ce qu'on voit** : le bras ou la jambe de frappe est plus long sur l'image du contact
  (1,4 fois pour un bras, davantage pour une jambe), puis reprend sa taille.
- **Fonction** : un facteur d'étirement par os et par clé d'animation, appliqué au dessin
  seulement (le squelette ne change pas). Valeur par défaut 1, de 1,3 à 1,5 sur la clé de
  contact.

### 9.3 Images fantômes

- **Ce qu'on voit** : 1 à 3 copies pâles du corps entier aux positions précédentes, de plus
  en plus claires. Elles durent 1 à 4 images.
- **Quand** : seulement quand **tout le corps** se déplace très vite. Esquive (141-143),
  montée d'un lancé (182-185), dash (217-218), touché par un coup lourd (310, 315, 330),
  image d'impact final (426).
- **Jamais** pour un membre seul (c'est la traînée) et jamais au sommet d'un saut.
- **Fonction** : `fantomes(n, pas)` redessine le personnage avec les poses des n images
  précédentes, à 40 %, 25 %, 12 % d'opacité, sous le personnage.

### 9.4 Flou de mouvement

- **Ce qu'on voit** : les bords du personnage sont étirés dans le sens du déplacement.
- **Quand** : très rare. Quatre images sur toute la plage finale (357, 425, 440, 441) et
  les touchés des coups lourds. Toutes les autres images sont nettes, même à 37 px par image.
- **Fonction** : dessiner le personnage 4 à 6 fois le long du déplacement de l'image, avec
  une opacité faible. À réserver aux changements de régime : départ en vitesse extrême,
  image juste avant un impact final, expulsion.

### 9.5 Lignes de vitesse

- **Charge** (329-330) : deux traits horizontaux de 20 puis 80 px derrière les bras.
- **Vitesse extrême** (357-410) : une bande de 20 à 35 traits droits parallèles, de 1 à 2 px
  d'épaisseur, haute comme le corps (0,3 à 0,5 H). Les bouts sont en dents de scie. Couleur
  du personnage, queue plus claire. Elle passe **devant** l'adversaire.
- **Un passage dure 3 i24** : entrée (traits de 70 à 180 px au bord de l'écran), plein écran,
  queue pâle. On enlève la queue quand les passages se resserrent.
- **Le corps disparaît par étapes** : net, puis flou avec des lignes derrière lui, puis
  tache étirée, puis lignes seules. À l'arrivée, les lignes se résorbent en 3 i24.
- **Fonction** : `bande_vitesse(depart, arrivee, hauteur, phase)`, avec des longueurs tirées
  au hasard une fois pour toutes par trait.

### 9.6 Éclat d'impact

Réservé au coup final (426-433). Les autres coups n'ont **aucun** éclat.

- Étoile à pointes de 30 à 45 px, une image.
- Disque plein de 0,5 H, une image.
- Le disque grandit jusqu'à 0,67 H en pâlissant, sur 4 images.
- Une douzaine d'étincelles : traits de 20 à 45 px qui partent en rayons à 40-50 px par
  image, raccourcissent et finissent en points. 8 images au total.
- Couleur : celle du frappeur, plus claire et plus saturée.

### 9.7 Anneaux de choc et faisceau

Pour une expulsion (441-449) : le corps est remplacé par une barre pleine (20, 45, 10, 2,
1 px d'épaisseur) et des ellipses perpendiculaires à la trajectoire s'ouvrent (30, 110, 175,
230 px). Un second anneau naît 2 images après le premier. Les anneaux durent 9 images, plus
longtemps que le projectile. Notre effet `choc` fait déjà quelque chose de proche.

### 9.8 Secousse de caméra

Toujours **verticale**. Le décor descend sur l'image du contact, remonte d'environ 60 % à
l'image suivante, puis l'écart diminue en changeant de signe.

| Force | Écarts mesurés (px, H = 120) | En H | Durée |
|---|---|---|---|
| Coup léger d'une rafale, un coup sur deux | +1 à +2 | 0,015 | 1 i24 |
| Atterrissage, frappe du pied | +2, −2 ou +3, −2 | 0,02 | 2 i24 |
| Coup appuyé | +4 à +6, −2 à −4 | 0,04 | 2 à 4 i24 |
| Coup lourd, charge | +6 à +8, −4, +2 | 0,06 | 3 à 4 i24 |
| Marteau au sol | +13, −5, +3, −5, +2 | 0,11 | 8 i24 |
| Impact final | −10, +8, −5, +4, −3, 0, −2 | 0,08 | 8 i24 |
| Expulsion | +18, −14, +7, −3, +2, −2 | 0,15 | 6 i24 |

- Pas de secousse sur un coup dans le vide.
- La plus forte secousse va à l'expulsion, pas au contact.
- **Fonction** : `secousse(force)` avec la suite `force × (1, −0,6, 0,35, −0,2, 0,1)`.

### 9.9 Arrêt sur image

- Coup léger : aucun. Contact 1 i24, retrait 1 i24.
- Coup appuyé ou lourd : **2 i24** (5 i60) où les deux personnages gardent exactement le
  même dessin. Seule la caméra bouge, et la traînée reste affichée.
- Coup final : pas d'arrêt strict, mais 14 i24 de quasi-tenue avant et 14 après.

### 9.10 Quel effet pour quel coup

| | Traînée | Étirement | Secousse | Arrêt | Fantômes ou flou | Éclat |
|---|---|---|---|---|---|---|
| Coup léger | oui | oui | une fois sur deux, faible | non | non | non |
| Coup appuyé | oui | oui | moyenne | 2 i24 | non | non |
| Coup lourd | oui, longue | oui | forte | 2 i24 | sur le touché | non |
| Coup dans le vide | oui | oui | non | non | fantômes de celui qui esquive | non |
| Coup final | oui | oui | très forte | tenues de 14 i24 | les deux | oui |

---

## 10. Caractère : le costaud et le rapide

| | Costaud | Rapide |
|---|---|---|
| Formes | angles droits, verticales, bloc | diagonales continues |
| Écart des pieds en garde | 0,72 H | 0,47 H |
| Poing avant | collé sous le menton | détaché devant le visage |
| Mise en garde | 15 i24, avec frappe du pied | 6 i24 |
| Préparation d'un coup | 4 à 12 i24 | 0 |
| Cycle d'un coup | 5 à 6 i24, ou 22 pour un coup lourd | 2 i24 |
| Raté | bloqué 5 à 6 i24, emporté par son poids | presque rien |
| Encaisse | reste debout, garde reprise en 1 à 2 i24 | s'envole, sonné 4 i24 |
| Effets propres | secousses fortes, fantômes sur le touché | fantômes sur lui-même, lignes de vitesse |
| Esquive | n'esquive pas | au dernier moment, pieds fixes, 2 i24 |

Les deux ont à peu près la même hauteur de bassin. C'est le rapport des durées (1 à 3) qui
raconte la différence, pas la taille des coups.

---

## 11. Notre `coup_de_poing_rue` face à la référence

| Point | Chez nous aujourd'hui | Dans la référence |
|---|---|---|
| Armé, bras de frappe | avant-bras ouvert à la verticale, main en l'air | coude fermé, poing derrière la tête |
| Armé, bras libre | tendu devant, ouvert | replié serré contre la poitrine |
| Buste à l'armé | presque droit, renversé en arrière | 45° vers l'avant, d'un trait avec la jambe arrière |
| Jambes à l'armé | pieds à environ 0,45 H, bassin haut | grande fente de 0,8 H, bassin bas, jambe arrière tendue |
| Trajet du poing | plusieurs dessins intermédiaires | aucun, une traînée courbe |
| Corps au contact | avance de 30 unités (0,17 H) | avance de 0,45 H, aligné du pied au poing |
| Bras au contact | tendu, puis reste tendu | tendu une image, étiré 1,4 fois, puis continue son arc |
| Buste au contact | environ 40° | 80 à 90° |
| Bras libre au contact | devant le corps | jeté à l'opposé |
| Arrêt sur image | 9 i60 | 5 i60 (2 i24) |
| Secousse | aucune | verticale, 0,06 à 0,11 H |
| Fin | se rattrape et revient en garde | pose déséquilibrée tenue 4 à 7 i24 |
| Effet au contact | cônes et anneaux dessinés | aucun dessin : traînée, secousse, fantôme du touché |

À refaire en suivant le tableau de phases du § 4, une fois la traînée et l'étirement codés.

---

## 12. Liste de contrôle avant de valider une animation

1. La pose armée et la pose de contact sont-elles lisibles seules, en silhouette noire ?
2. Chaque pose forte tient-elle sur une ligne simple, penchée ?
3. Les pieds sont-ils assez écartés et le bassin assez bas ?
4. Y a-t-il un bras à moitié ouvert ou qui pend sans raison ?
5. Le bras libre fait-il le contraire du bras de frappe ?
6. Le trajet du coup tient-il en 2 ou 3 i60, sans dessin intermédiaire du membre ?
7. Le corps avance-t-il sur l'image du contact ?
8. Le membre traverse-t-il la cible, et continue-t-il après ?
9. Les durées respectent-elles le caractère (préparation, frappe, récupération) ?
10. Les tenues dérivent-elles un peu au lieu d'être figées ?
11. Le touché se plie-t-il autour du point d'impact, la partie touchée en premier ?
12. Les écarts d'un départ doublent-ils, ceux d'un arrêt se divisent-ils ?
13. Les effets sont-ils au bon niveau pour la force du coup (§ 9.10) ?
14. Sur la planche, voit-on les deux personnages avec des lignes opposées ?

---

## 13. Ce qui reste à apprendre

Une seule vidéo ne suffit pas pour ces points. À vérifier sur les suivantes :

- les coups de pied hauts et circulaires (un seul coup de pied haut ici, vu de loin) ;
- les blocages et les parades (aucun dans la vidéo 1 : on esquive ou on encaisse) ;
- les projections et les saisies (une seule empoignade, 331-337) ;
- les chutes au sol complètes et les relevés après un KO ;
- les armes et les pouvoirs ;
- l'alternance bras gauche et bras droit, illisible sur un personnage d'une seule couleur ;
- la poussière et les effets au sol (aucun dans la vidéo 1) ;
- ce qui change à 60 images par seconde : la vidéo 1 est à 24, et son côté sec vient en
  partie de là. Il faudra décider si nos coups tiennent leurs poses par paliers de 2 ou
  3 i60 pour garder ce côté sec.

### Lectures incertaines dans la vidéo 1

- L'angle exact du coude à l'armé : entre 60° et 90° selon les images (résolution 360p).
- Le sens dans lequel le rapide fait face pendant son freinage (219-222).
- Les membres pendant l'impact final (426-439), cachés par l'éclat.
- Un possible recadrage de caméra entre 163 et 164.
