# Bible d'animation de stickman

Ce document dit **comment animer** un stickman qui se bat pour que ce soit naturel, lisible
et cool. Il est tiré de l'étude image par image de vidéos de référence faites par de bons
animateurs. Chaque règle renvoie aux images qui la prouvent.

- `INVENTAIRE.md` dit **quelles** animations faire. Ce document dit **comment** les faire.
- Quand une règle d'ici contredit une animation existante, c'est l'animation qu'on corrige.
- Le document grossit à chaque nouvelle vidéo étudiée (§ 15).
- **Confirmée** : vue dans plusieurs vidéos. **V1** ou **V2** : vue dans une seule.
  **Selon le registre** : les vidéos font des choix différents, voir § 0.

## Vidéos étudiées

| N° | Vidéo | Format | Style | Étude |
|---|---|---|---|---|
| V1 | « Strength vs Speed » (Stick Nodes) | 24 i/s, 494 images, 20 s | duel à mains nues, cadre fixe, effets très sobres | `etudes/01_strength_vs_speed/` |
| V2 | « Rai and Zen vs Armagon » (Rai Lukasha, Stick Nodes) | 24 i/s, 3 713 images, 2 min 35 | deux héros contre un boss, mains nues, sabre, faux, pouvoirs, caméra mobile, effets chargés | `etudes/02_rai_zen_armagon/` |

Les numéros d'images sont ceux de chaque vidéo, comptés à partir de 0 : « V1 176 » est
l'image 176 de la vidéo 1.

## Unités

- **i24** : une image de la référence, à 24 images par seconde (42 ms).
- **i60** : une image de notre jeu, à 60 images par seconde. **1 i24 = 2,5 i60.**
- **H** : la hauteur du personnage debout. V1 : H = 120 px. V2 : H = 97 à 115 px en plan
  large (elle change avec le zoom). Chez nous : H = 180 unités, tête de 46.
- Les distances sont données en H pour pouvoir passer d'un personnage à l'autre.

| i24 | 1 | 2 | 3 | 4 | 5 | 6 | 8 | 12 | 14 |
|---|---|---|---|---|---|---|---|---|---|
| i60 | 2 ou 3 | 5 | 7 ou 8 | 10 | 12 ou 13 | 15 | 20 | 30 | 35 |

---

## 0. Deux registres

Les deux vidéos ne se contredisent pas : elles jouent dans deux registres différents.

| | Registre sobre (V1) | Registre spectaculaire (V2) |
|---|---|---|
| Effets sur un coup normal | traînée seule | traînée, plus une bouffée ou une étoile sur chaque contact |
| Éclat d'impact | coup final seulement | presque chaque contact |
| Secousse de caméra | 1 à 8 i24, jusqu'à 0,15 H | 3 à 25 i24, jusqu'à 0,23 H |
| Flou, fantômes | rares | fréquents chez le boss et sur les charges |
| Caméra | fixe | travellings, zooms, recadrages sur les contacts |
| Image d'impact noire puis blanche | jamais | 3 ou 4 fois par combat, sur les coups décisifs |

**Notre choix.** Un jeu de combat montre des centaines de coups : le registre spectaculaire
partout fatigue l'œil et cache l'action. On prend donc :

- **les normaux, les déplacements et la défense en registre sobre**, plus un petit éclat de
  contact sur chaque coup qui touche (les jeux de combat en ont tous un, et V2 le confirme) ;
- **les spéciaux, le Heat Smash, le Rage Art et le KO en registre spectaculaire** ;
- entre les deux, **les coups lourds** prennent une secousse plus forte et parfois un zoom.

Cette échelle est détaillée au § 9.10.

---

## 1. Les douze règles

1. **Un coup court, c'est deux dessins** : la pose armée, puis la pose de contact, sans
   dessin du membre à mi-chemin. Un coup **ample** (coup de pied haut, uppercut, coup chargé)
   a 1 à 3 images de trajet, toujours recouvertes d'une traînée. Confirmée (§ 4).
2. **Le temps va dans la préparation et dans la tenue, pas dans le trajet.** Confirmée. La
   préparation est soit un armé tenu (V1 : 4 à 12 i24), soit une garde tenue avant d'attaquer
   (V2 au sabre : 5 à 11 i24, puis un armé de 1 à 3 i24) (§ 2).
3. **Le corps entier frappe.** Sur le contact, la fente atteint 0,8 à 1,2 H et tout le corps
   avance d'environ 0,45 H. Confirmée. Exception : avec une arme longue, c'est l'arme qui
   porte et le corps reste à distance (§ 4, § 10).
4. **Un bras n'est jamais mou ni à moitié ouvert.** Il est replié serré, tendu à fond, ou
   jeté à l'opposé. Confirmée (§ 3).
5. **Un coup ne s'arrête pas en surface.** Soit il traverse et continue son arc (V1, sabre et
   faux de V2), soit il reste planté 4 à 8 i24 pendant que la cible réagit (coups au corps de
   V2). Il ne revient jamais aussitôt par où il est venu, sauf pour un direct rapide.
6. **Les poses sont penchées, larges et basses.** Buste à 45° à l'armé, pieds écartés de 0,8 à
   1,2 H, bassin bas. Confirmée ; V2 va encore plus loin (jusqu'à 1,6 H) (§ 3).
7. **Un seul personnage rapide à la fois.** Confirmée, même avec deux attaquants : l'autre
   sort du cadre ou se fige (§ 2).
8. **Les tenues vivent.** Une pose tenue dérive de 0,5 à 2 px par image, ou c'est la lumière,
   les particules ou la caméra qui bougent pendant qu'elle reste figée. Confirmée (§ 2).
9. **Le touché se plie autour du point d'impact**, la partie touchée part en premier, la tête,
   les bras et les pieds suivent. Confirmée (§ 7).
10. **Les vitesses ne sont jamais régulières.** Un départ double à chaque image, un arrêt
    divise par deux, un saut s'étire au sommet. Confirmée. Seuls les effets cycliques
    (rafale, pouvoir maintenu) ont un rythme régulier (§ 8).
11. **La force d'un coup se dit par une échelle d'effets**, du plus léger au plus décisif : on
    ajoute des effets à mesure que le coup compte. Les plus forts (image d'impact noire puis
    blanche) restent rares (§ 0, § 9).
12. **Le caractère se lit dans le rythme.** Le costaud prépare longtemps et paie ses ratés ;
    le rapide frappe sans prévenir. Confirmée (§ 12).

---

## 2. Rythme

### Tenues et rafales

Le combat alterne des **tenues** (rien ne bouge, ou presque) et des **rafales** (tout change
à chaque image). Il n'y a presque pas de mouvement « moyen ». Confirmée.

| Moment | Durée | Preuve |
|---|---|---|
| Pause entre deux actions, mise en place | 12 à 15 i24 | V1 35-49, 113-127 |
| Armé d'un coup lourd, tenu | 4 à 10 i24 | V1 176-180 ; V2 2967-2974, 3120-3129 |
| Garde tenue avant une attaque au sabre | 5 à 11 i24 | V2 1372-1378, 1508-1512 |
| Charge d'un coup d'énergie (poing allumé, figé) | 9 i24 | V2 1797-1805 |
| Tenue avant un coup final | 7 à 14 i24 | V1 411-424 ; V2 3172-3178 |
| Tenue de la pose de contact après un gros coup | 11 à 14 i24 | V1 426-439 ; V2 1811-1821 |
| Coup au corps planté pendant que la cible réagit | 4 à 8 i24 | V2 761-766, 812-819 |
| Pose de fin d'un coup réussi | 4 à 7 i24 | V1 167-171, 339-345 |
| Pose de fin d'un coup raté (sans défense) | 5 à 6 i24 | V1 142-146, 224-229 |
| Blocage | 4 à 9 i24, toujours plus long que le coup arrêté | V2 (§ 6) |
| Lutte, poing contre poing, saisie | 25 à 94 i24 | V2 920-961, 1250-1343, 2640-2659 |

Pendant un échange, un personnage ne reste jamais immobile plus de 8 i24 sans que l'autre
bouge (V1 254-261).

### Faire vivre une tenue

- La pose dérive de 0,5 à 2 px par image (V1 176-180, 411-422).
- Une pose qui s'arrête dépasse de 2 ou 3 px, revient, puis se tasse d'un pixel (V1 83-85).
- Pendant une longue tenue, on fige le corps qui agit et on fait vivre le reste : les
  cheveux, la ceinture, la queue du monstre, les particules (V2 920-961, 1279-1290).
- On peut aussi faire battre un cycle d'effets : V2 tient un poing contre poing 94 i24 avec
  une pulsation toutes les 8 i24 (lueur, anneau et gerbe, grand anneau, brume, retombée),
  une caméra qui tremble de ± 0,01 H à chaque image et un zoom lent de + 20 % (V2 1250-1343).
- Une tenue chargée peut rester figée si la lumière change (V2 1797-1805 : la scène
  s'assombrit pendant la charge).

### Uns et deux

L'action est animée en uns (une pose par image). Les moments lents (fin de lutte,
épuisement) passent en deux (une pose tenue 2 i24) (V2 1014-1031). Chez nous : poses tenues
par paliers de 5 i60 dans les moments lents.

### Rapport entre les phases d'un coup

| | Préparation | Trajet | Contact tenu | Récupération |
|---|---|---|---|---|
| Costaud, coup lourd (V1) | 12 i24 | 0 | 1 à 2 | 9 i24 |
| Costaud, direct (V1) | 2 à 4 | 0 | 1 | 3 à 4 de tenue |
| Rapide, coup de rafale (V1) | 0 | 0 | 1 | 1 de retrait |
| Coup au corps (V2) | 3 à 4 | 0 | 4 à 8 (planté) | 2 à 3 |
| Coup ample, pied haut ou uppercut (V2) | 2 à 3 | 1 à 3 | 1 | 3 |
| Coupe au sabre (V2) | garde 5 à 11, armé 1 à 3 | 0 (arc) | 1 | dépassement 5 à 8 |
| Coup chargé (V2) | 9 | 1 | 11 | — |

### Composer une rafale

Deux façons, toutes deux bonnes :

- **En groupes** (V1 288-304) : 3 coups, puis 2, puis 1, avec 2 à 3 i24 de respiration entre
  les groupes. Seul le premier coup a un armé.
- **En métronome** (V2 3130-3166) : un contact toutes les 4 i24 (10 i60), dix fois de suite,
  bras et hauteurs alternés, avec une secousse entretenue. On finit par deux coups à 2 i24
  d'écart quand l'adversaire décroche.

Dans les deux cas : hauteur et forme changent à chaque coup, et le dernier coup est précédé
d'une quasi-tenue et porte le plus gros effet.

### Qui a l'initiative

Elle change toutes les 15 à 35 i24, toujours sur une tenue ou un raté. L'adversaire réagit en
retard et esquive au dernier moment : il est déjà en l'air quand l'arc apparaît (V1 139-141 ;
V2 1442-1444).

### Deux attaquants contre un (V2)

Utile pour les mises en scène, pas pour le duel :

- un seul frappe à la fois ; l'autre sort du cadre ou se fige en pose basse ;
- celui qui entre passe au-dessus (saute-mouton) ou en dessous de l'autre, jamais à la même
  hauteur ; ils se chevauchent 4 à 10 i24 (V2 2063-2067, 2122, 2163-2167) ;
- chacun a sa couleur d'effet (jaune pour Rai, violet pour Zen).

---

## 3. Poses

### La ligne du corps

- Chaque pose forte tient sur **une ligne simple** : une diagonale (charge, armé, fente), un
  C (plié sur un coup), un S (sonné), une barre horizontale (direct en extension).
- Les deux personnages ont des lignes **opposées** sur la même image : diagonale contre
  verticale, barre horizontale qui traverse une forme verticale (V1 152, 176-180).
- Les deux têtes ne sont jamais à la même hauteur sur une image de contact.
- Dans une pose armée en l'air, les quatre membres partent dans quatre directions (V1 136).

### Penché, large, bas

| Pose | Buste | Écart des pieds | Bassin |
|---|---|---|---|
| Debout, neutre (fin de combat) | vertical | joints | haut |
| Garde du rapide (V1) | 20° vers l'avant | 0,47 H | 0,43 H du sol |
| Posture du costaud (V1) | presque vertical | 0,72 H | 0,40 H |
| Garde au sabre (V2) | droit | 1 H, fente basse | bas, sabre pointé vers l'adversaire |
| Armé d'un coup lourd | 45° à 50°, d'un trait avec la jambe arrière | 0,8 H | bas |
| Armé d'un coup chargé (V2) | penché | 0,9 H | 0,3 H du sol, poing à la hanche |
| Contact d'un coup en fente | 80° à 90° | 1 à 1,6 H | bas |
| Coup lourd raté (V1) | 80°, tête sous le bassin | — | haut |

La jambe arrière est **tendue** dans presque toutes les poses d'attaque : elle prolonge la
ligne du buste. La jambe avant est pliée et porte le poids.

### Les bras

C'est le point le plus important, et le plus raté chez nous.

- **En garde** : coude fermé à 90° ou moins. Le rapide a un poing détaché devant le visage et
  le coude arrière levé à l'horizontale. Le costaud a un poing collé sous le menton et l'autre
  bras en équerre.
- **Armé d'un coup lourd** : le bras monte presque tendu vers l'arrière et le haut (V1 175),
  puis le coude se ferme (V1 176). Le poing finit **derrière la tête**, à une tête au-dessus
  de l'épaule. L'avant-bras est rabattu vers la tête, jamais ouvert vers le ciel.
- **Armé d'un coup chargé** : poing **à la hanche**, en pose accroupie (V2 1797-1805).
- **Juste avant de partir** : 1 i24 où le coude monte en pointe et où le poing recule encore
  (V1 140, 181). Ce recul courbe la trajectoire.
- **Au contact** : bras tendu à fond. V1 l'étire à environ 1,4 fois sa longueur pendant une
  image ; V2 ne montre pas d'étirement lisible en 360p.
- **Bras libre, selon le style** :
  - jeté à l'opposé au contact, tendu en arrière ou en l'air (V1 158, 182, 288 ; V2 812) :
    c'est le contrepoids d'un coup isolé ;
  - replié serré contre la poitrine, poing près de la tête (V1 176-180 pendant l'armé ;
    V2 3130-3166 pendant toute une rafale) : c'est l'armé du coup suivant.
- **Crochet** : le coude ne se tend jamais (100° au contact, V1 298).
- Un bras ne pend que dans trois cas : après un atterrissage lourd, après un coup raté, ou
  quand le personnage est sonné ou épuisé.

### Étirer

Les membres changent de longueur sur une image : bras de frappe à 1,4 fois (V1), jambe du
coup de pied final jusqu'à 0,9 H (V1 164), jambe de départ d'un dash doublée (V1 217), corps
qui esquive par un saut étiré à 1,3 fois (V2 1442-1444).

---

## 4. Le coup de poing

### Coup lourd du bras arrière (le nôtre : `coup_de_poing_rue`)

Références : V1 173-187, 196-208, 128-146 ; V2 806-819.

| Phase | i24 | i60 | Ce qui se passe |
|---|---|---|---|
| Recul | 2 à 3 | 5 à 8 | Grand pas arrière (0,65 H). Le bras de frappe monte presque tendu vers l'arrière. |
| Fermeture | 1 | 2 ou 3 | Le coude se ferme, le poing vient derrière la tête. Le bras libre se colle à la poitrine. |
| Armé tenu | 4 à 5 | 10 à 12 | Buste à 45° d'un seul trait avec la jambe arrière. La pose dérive de 1 à 2 px par image. |
| Déclenchement | 1 | 2 ou 3 | La tête tombe de 0,1 H, le coude monte en pointe, le poing recule encore. Début de traînée. |
| Contact | 1 | 2 ou 3 | Le poing fait 0,9 à 1,4 H d'un coup. Le corps avance de 0,45 H. Bras tendu. Traînée complète. |
| Tenue de contact | 1 à 4 | 3 à 10 | Même dessin, ou poing planté qui pousse. Caméra qui secoue. |
| Dépassement | 1 à 2 | 3 à 5 | Le bras continue son arc. Le buste a tourné. |
| Pose de fin | 4 à 7 | 10 à 18 | Pose déséquilibrée tenue, sur une jambe ou très penchée. |
| Retour | 4 à 5 | 10 à 12 | 2 i24 par pose. |

Ordre de départ : tête et buste, poussée de la jambe arrière, pied avant planté, épaule et
coude, puis le bras, puis le buste qui suit. **Le poing part en dernier** (V1 128-142). La tête
freine juste avant que le bras parte : la vitesse passe du corps au bras.

Si le coup rate, le personnage est emporté : buste à 80°, tête sous le bassin, 5 à 6 i24
(V1 142-146, 224-229).

### Direct

| Phase | i24 | Ce qui se passe |
|---|---|---|
| Avant | 0 à 1 | Coude fermé à fond, poing à moins d'une tête de l'épaule. |
| Contact | 1 | Bras tendu. Le bassin avance de 0,2 à 0,3 H. Jambe arrière, buste et bras sur une diagonale. |
| Retrait | 1 | Le poing revient à la poitrine. Jamais derrière l'épaule. |

Le poing **traverse** la cible : il ressort de l'autre côté de la silhouette (V1 152-160), et
la bouffée d'impact sort dans le dos du touché (V2 813, 1811-1815).

### Coup au corps planté (V2)

Pour un coup au ventre ou un coup qui pousse : le poing reste enfoncé 4 à 8 i24 pendant que
la cible se plie et recule (V2 761-766, 812-819). On s'en sert à la place d'un arrêt sur
image.

### Uppercut (V2 869-873)

Trois images de trajet, chacune recouverte d'un croissant blanc opaque et épais ; la traînée
dure 4 i24 (3 avant le contact, 1 après). Le bras continue son arc au-dessus de la tête.

### Coup chargé (V2 1797-1821)

| Phase | i24 | Ce qui se passe |
|---|---|---|
| Charge | 9 | Pose accroupie figée, poing allumé à la hanche. La scène s'assombrit de 15 %. |
| Trajet | 1 | Bras à mi-course, flamme le long du bras. |
| Extension | 1 | Bras tendu, flamme de 0,85 H. |
| Image d'impact | 2 | Une image noire, une image blanche (§ 9.7). |
| Contact | 11 | Pose de contact tenue, étincelles, secousse longue. |

### Autres coups de poing

- **Crochet** (V1 298) : armé d'une image en tirant l'épaule en arrière. Le corps se
  redresse au lieu de plonger.
- **Marteau** (V1 304, 321) : poing au-dessus de l'épaule 1 i24, puis le buste tombe avec le
  bras. Le costaud lève la jambe arrière en contrepoids.
- **Moulinet** (V1 233-238) : un tour de bras tendu donne deux contacts à 5 i24 d'écart.

### Avancer en frappant

L'attaquant avance de 0,1 à 0,25 H à chaque coup ; le touché ne recule que de 0,03 à 0,15 H.
L'attaquant finit collé à l'adversaire (V1 151-160).

---

## 5. Les coups de pied

- **Coup de pied court ou qui pousse** : aucune image de trajet, de l'armé au contact (V1 164,
  266, 272).
- **Coup de pied haut** (V2 760, 772) : genou serré contre le torse 2 i24, puis 1 image où la
  jambe est remplacée par un éventail, puis le contact jambe à la verticale. La jambe reste en
  l'air 1 i24, redescend pliée en 3 i24, réception sur un pied.
- **Coup de pied latéral** (V2) : buste parti à environ 70° à l'opposé de la jambe, un bras
  levé derrière, l'autre bas. Le pied reste planté 6 i24.
- **Coup de pied au ventre, jambe arrière** (V1 161-171) : 3 i24 de quasi-tenue, puis contact,
  buste basculé à l'opposé, jambe d'appui verticale. La jambe reste en l'air pliée 5 i24.
- **Balayage** (V1 264-266) : la jambe traînante sert d'armé, le bassin s'écrase à 0,3 H du
  sol, la jambe fouette sur 1,1 H en une image. Le pied d'appui ne bouge pas.
- **Coup de pied sauté** (V1 267-276) : 4 i24 de suspension au sommet, puis la jambe balaie
  90° en une image. Réception sur l'autre jambe.
- **Coup de genou** (V2 848, 1705) : l'image s'éclaircit 1 i24 et une onde sort dans le dos
  du touché.

---

## 6. Défense (V2)

V1 n'avait aucune défense : on y esquive ou on encaisse. V2 en montre beaucoup.

### Blocage

- **Le blocage type est un X des avant-bras**, croisés devant le visage ou devant le ventre.
  Il se fait debout, à genoux ou couché (V2 760-1043).
- Il est tenu **4 à 9 i24**, toujours plus longtemps que le coup qu'il arrête.
- Sur un coup lourd : le bloqueur recule en fente basse, une ellipse de poussière (0,8 H)
  sous ses pieds pendant 4 i24, et 2 ou 3 anneaux gris de 0,4 H au point de contact pendant
  3 i24 (V2 915, 1474).
- **Blocage sous poussée** : tant que l'attaquant pousse, le bloqueur glisse en arrière en
  fente très basse (1 H d'écart), avec des étincelles à chaque image (V2 2323-2352).
- **Contre le sabre** : sabre vertical tenu devant soi (V2 1552).

### Parade

- **Parade à l'avant-bras** : le bras dévie le coup sur le côté, éclat au point de contact
  (V2 1497, 1503).
- **Parade-saisie** : la paume attrape le poing et le tient 4 i24 ; l'attaquant se replie
  ensuite voûté en 3 i24 (V2).

### Esquive

- **Au dernier moment**, pieds fixes, seul le buste part : 1 i24 d'anticipation, 2 i24 pour
  descendre de 0,4 H (V1 140-142). Contre le sabre, on change de silhouette à chaque coupe :
  recul du buste de 0,2 H, puis plongée sous l'arc, 1 à 2 i24 par position (V2 1404-1412).
- **Par un saut** : décollage en 1 i24, corps étiré à 1,3 fois avec le bas flou ; le
  personnage est déjà au-dessus de l'arc sur l'image où l'arc apparaît (V2 1442-1444).
- **Esquive qui frappe** : le genou levé pour sauter un balayage percute la tête de
  l'adversaire baissé ; une seule pose sert les deux (V2).

### Rebond sur un blocage

Bloquer un coup de pied en X, rester 5 i24 accroupi sur la jambe adverse, puis partir en coup
de pied sauté (V2).

### Saisie, projection, lutte

- **Saisie** : tenue 8 à 10 i24 avec un léger tangage (V2 1694-1704). Saisie à la gorge :
  25 à 27 i24 (V2 2640-2659, 2988).
- **Se libérer d'une saisie** : frapper le bras qui tient, avec l'armé le plus long (8 i24).
- **Projection** : pivot de 3 i24, puis la victime parcourt 1,2 H en une image, roule 3 i24 et
  laisse une ligne de poussière qui reste 6 i24 (V2 1719-1729).
- **Lutte** : une tenue d'environ 40 i24 où seuls la ceinture et les cheveux bougent, les
  corps dérivent de 1 à 2 px ; elle se casse d'un coup, par une poussée de 5 i24 (V2 920-961).

---

## 7. Déplacements

### Départ de course ou de charge

- Le départ commence par **la tête**, pieds fixes : 4 i24 où la tête fait 1, 3, 10, 22 px
  (V1 128-131). La vitesse double à chaque image.
- Pleine vitesse : 0,2 à 0,28 H par i24. Buste à 60-70°.
- Charge très rapide : la silhouette est remplacée 1 i24 par des hachures horizontales de sa
  couleur (V2 1534), ou le corps se dissout en essaim de petites copies (V2 1140).

### Dash (V1 214-222)

3 i24 de plongée, puis 1,4 H en **une** image avec 2 copies floues, puis freinage 39, 27, 6,
3 px.

### Vitesse extrême

Le corps disparaît et il ne reste que des lignes de vitesse (V1 357-410) ou une traînée noire
floue de 1 à 2 H (V2 2599-2628). L'attaquant n'est montré net qu'une fois au milieu et à la
fin. Chaque passage laisse sur la victime un trait de la couleur du coup (§ 9.5).

### Saut et vol

- Montée en 2 i24, suspension de 4 i24, descente qui accélère (V1 267-276).
- Au sommet, le corps se groupe : genoux hauts, bras sur la tête.
- Un personnage en l'air au loin est dessiné grisé ; il reprend son noir en revenant au
  premier plan (V2 2320).

### Atterrissage (V1 24-36)

Trois poses sur trois images consécutives : contact étiré (bras en l'air), écrasement à 72 %
de la hauteur, amorti (buste à 45°, mains sur le genou). Remontée 7, 5, 3, 0,5 px. Après un
atterrissage lourd, une ellipse ou un anneau de poussière aux pieds (V2 1363).

### Se relever

- Normal (V1 50-67) : deux frémissements, 9 i24 pour ramener les pieds sous le corps, montée
  en 6 i24 (1, 2, 6, 12, 14, 15, 9, 2 px), en avançant de 0,5 H vers l'adversaire.
- Avant de monter, la tête **descend** pendant 6 i24 : c'est l'anticipation du relevé. Les
  bras arrivent en garde en dernier (V2 312-335).
- Lourd (V2) : 8 i24 au sol, puis 3 i24 : à quatre pattes, accroupi, debout.
- **Relevé-attaque** (V2 1240) : après 8 i24 au sol, le personnage jaillit directement en
  plongeon horizontal (4 i24), sans passer par la pose debout.
- Épuisé (V2) : environ 9 i24, il finit voûté, tête basse, sans garde. Un relevé raté :
  12 i24 pour se lever, 3 i24 debout, effondrement en 9 i24.

### Prendre sa garde

- Rapide : 6 i24, le poing arrive en dernier et fait son plus grand écart sur la dernière
  image (V1 80-85).
- Costaud : 15 i24, genou monté puis frappe du pied au sol avec une petite secousse ; les
  poings arrivent en place sur l'image où le pied touche (V1 98-112).

---

## 8. Le touché

### Règle générale (confirmée)

Sur l'image du contact : la partie touchée part, le corps se plie autour du point d'impact,
et le reste traîne du côté opposé. Le plus grand déplacement est sur l'image du contact ou la
suivante, puis la vitesse est divisée par 1,5 à 2 à chaque image.

| Coup reçu | Forme du corps | Déplacement | Suite |
|---|---|---|---|
| Poing au corps | plié par-dessus le poing | 0,03 à 0,15 H, retour élastique | la posture se dégrade à chaque coup |
| Direct à la tête | arc vers l'arrière, bras jetés | 0,3 à 0,45 H | le léger reste sonné en S 4 i24 ; le lourd reprend sa garde en 1 à 2 i24 |
| Marteau sur la tête | V, tête en bas | — | — |
| Pied au ventre | plié en portefeuille | 0,3 H puis glissade | glisse au ras du sol, ne s'envole pas |
| Coup lancé vers le haut | part par le bassin, membres pendants | monte à 1,4 H | un tour en 18 i24 |
| Projection debout (V2 988-1006) | fente basse, bras en X | 2 H sur 19 i24 (pas : 58, 70, 19, 38, 13, 13, 13, 6 px) | reste à genoux 15 i24 |
| Expulsion (V2 2556-2579) | — | à la verticale | tombe sur la tête, y reste 2 i24, s'effondre en boule en 7 i24 |

### Le poids

- Le lourd encaisse sans tomber les coups de poing ; un coup de genou peut quand même le
  renverser (V2 848).
- L'usure se montre par la récupération qui disparaît : après quelques coups, le personnage
  ne se redresse plus entre deux impacts (V1 374-392).
- La pose de réaction ne se répète jamais d'un coup à l'autre.

### Transformer le recul

Un bon personnage ne subit pas longtemps : il atterrit sur un pied, s'accroupit 3 i24, fait
un grand pas arrière, et ce pas est déjà l'armé du coup suivant (V1 169-175 ; V2 3028-3043).

---

## 9. Tables d'espacement

Écarts d'une image à la suivante, en pixels de la vidéo (H = 120 px en V1). Pour nos unités,
multiplier par 1,5.

| Mouvement | Écarts par i24 | Preuve |
|---|---|---|
| Départ de charge (tête) | 0,7 · 2 · 5 · 11 · 22 · 29 · 30 | V1 129-135 |
| Départ en vitesse extrême | 3 · 10 · 37 · hors champ | V1 355-358 |
| Poing d'un coup lourd | 110 à 165 en une image | V1 141, 182, 201 |
| Freinage après un dash | 39 · 27 · 6 · 3 | V1 219-222 |
| Recul après un coup | 37 · 24 · 22 · 17 · 15 · 12 · 6 | V1 366-372 |
| Glissade après une projection | 58 · 70 · 19 · 38 · 13 · 13 · 13 · 6 | V2 993-1006 |
| Lancé en l'air, montée | 65 · 53 · 38 · 7 | V1 182-185 |
| Lancé en l'air, sommet | 5 à 6 images presque immobiles | V1 186-191 |
| Lancé en l'air, chute | 6 · 12 · 32 · 70 | V1 196-200 |
| Projection horizontale | 82 · 81 · 63 · arrêt | V1 202-205 |
| Se relever (tête) | 1 · 2 · 6 · 12 · 14 · 15 · 9 · 2 · 0 · −1 | V1 56-67 |
| Travelling qui suit une rafale | 7 · 6 · 6 · 5 · 4 · 4 · 2 · 1 | V2 3130-3140 |

- Un départ **double** à chaque image, sur 3 à 6 images.
- Un arrêt après un coup est **brutal** ; un arrêt après une glissade divise par deux.
- Un saut n'est pas une parabole régulière : la montée freine, le sommet dure, la chute double.
- La rotation en l'air n'est pas régulière : rapide à la montée, presque nulle au sommet.

---

## 10. Effets

Les effets des deux vidéos sont des dégradés, des transparences et des formes simples. On peut
donc les **calculer** au lieu de les dessiner, à partir des positions du squelette à l'image
précédente et à l'image courante. Chaque effet ci-dessous donne ce qu'on voit, puis ce que la
fonction doit faire.

### 10.1 Traînée de membre (smear)

- **Ce qu'on voit** : une bande qui suit le chemin parcouru par le poing, le pied ou l'arme
  depuis l'image précédente. Elle est courbe, parce que le membre tourne autour de l'épaule ou
  de la hanche.
- **Couleur** : celle du personnage pour un membre nu ; celle de l'**objet** pour une arme
  (acier blanc, faux rouge, fourreau noir bordé d'or) ; celle de son énergie pour un coup
  chargé (V2 1361, 1566, 1625, 2360).
- **Opacité** : de transparente (bout le plus ancien) à opaque (près du membre). Pour un
  uppercut ou une arme lourde, elle peut être pleine et opaque (V2 869-873, 2360).
- **Durée** : 1 image pour un membre nu (V1) ; 2 à 4 images pour une arme ou un coup ample
  (V2). En s'effaçant, elle **perd d'abord sa moitié la plus ancienne et s'amincit**, puis
  n'est plus qu'un trait (V2 1361-1363).
- **Longueur** : de 0,2 H (retrait) à 2 H (coupe au sabre).
- **Formes** : arc au-dessus du bras pour un coup par-dessus, croissant sous le bras pour un
  crochet ou un uppercut, éventail qui part du sol ou du genou pour un coup de pied, boucle
  pour un retrait. Griffes : 3 ou 4 traits fins parallèles (V2 1563-1596).
- **Fonction** : `trainee(os, pose_avant, pose_apres, style)`.
  - Elle se déclenche toute seule quand l'extrémité d'un membre bouge de plus de 0,3 H entre
    deux images.
  - Elle échantillonne 8 à 12 positions entre les deux poses en interpolant les **angles** des
    os (pas les positions), ce qui donne l'arc.
  - Elle trace un ruban de la largeur du membre le long de ces points, opacité de 0 % au plus
    ancien à 100 % au plus récent.
  - Elle s'efface en 1 image, ou en 2 à 4 avec le style « arme » (on coupe la moitié la plus
    ancienne et on amincit à chaque image).

### 10.2 Arcs d'arme (V2)

| Coupe | Forme | Taille | Preuve |
|---|---|---|---|
| Rotation, armé, moulinet | éventail autour de la main, rayon = longueur de la lame, strié en rayons | 50° à 150° | V2 1379-1390 |
| Coupe verticale ou montante | croissant | 0,8 à 2 H, 0,1 à 0,27 H d'épaisseur au milieu | V2 1361, 1443, 1474 |
| Coupe horizontale | ellipse fermée qui passe derrière puis devant la cible | 2 H × 0,3 H | V2 1417, 1496 |
| Arme lourde (faux) | croissant plein et opaque | 1,5 à 2 H, 0,15 à 0,2 H d'épaisseur, 3 images | V2 2360, 2455 |
| Arme qui tourne seule | nœud papillon de deux éventails en dents de scie, qui saute de 90° par image | — | V2 2322-2352 |

- Le bord d'attaque est blanc opaque (2 à 3 px), l'intérieur translucide.
- **Sur l'image du contact, la lame n'est souvent pas dessinée** : l'arc la remplace, ou la
  lame est déjà dans sa pose de fin (V2 1417, 1444).
- L'arc peut toucher un adversaire hors de portée de la lame : un arc de 2,2 H touche à 1,5 H
  (V2 1496, 1503).

### 10.3 Étirement du membre

Le membre de frappe est plus long sur l'image du contact (1,4 fois en V1), puis reprend sa
taille. **Fonction** : un facteur d'étirement par os et par clé d'animation, appliqué au dessin
seulement (le squelette ne change pas).

### 10.4 Fantômes et flou

- **Fantômes** : 1 à 3 copies pâles du corps entier aux positions précédentes (40 %, 25 %,
  12 %), sous le personnage, 1 à 4 images. Pour les déplacements de tout le corps : esquive,
  montée d'un lancé, dash (V1 141-143, 182-185, 217).
- **Flou du corps entier** : 1 à 3 images sur les attaques lancées et les projections ; un
  corps projeté alterne flou et net une image sur deux pendant 4 à 5 images (V2 1536-1541,
  1686-1688). Un bras seul peut aussi être flou sur un coup très rapide (V2 1430-1434).
- **Aura** : un liseré de 1 à 2 px autour du corps, plus un fantôme translucide qui traîne 1 à
  2 images derrière, et qui reste 4 images au point de départ d'un dash (V2 3070-3082).
- **Fonctions** : `fantomes(n)` redessine le personnage avec les poses des n images
  précédentes ; `flou(n)` le redessine 4 à 6 fois le long du déplacement de l'image avec une
  opacité faible.

### 10.5 Lignes de vitesse

- **Charge** (V1 329-330) : deux traits horizontaux derrière les bras.
- **Vitesse extrême** (V1 357-410) : une bande de 20 à 35 traits parallèles, haute comme le
  corps, aux bouts en dents de scie, de la couleur du personnage, qui passe **devant**
  l'adversaire. Un passage dure 3 i24 : entrée, plein écran, queue pâle.
- **Coupures laissées par une rafale invisible** (V2 2599-2628) : chaque passage laisse sur la
  victime un trait droit rouge de 1 à 2 px et environ 1 H, pendant 1 à 2 images.
- **Fonction** : `bande_vitesse(depart, arrivee, hauteur, phase)`, longueurs tirées au hasard
  une fois pour toutes par trait.

### 10.6 Éclats d'impact

| Éclat | Forme | Durée | Quand |
|---|---|---|---|
| Bouffée | nuage de 0,25 H qui sort **dans le dos** du touché | 3 i24 | coups au corps (V2 813) |
| Anneau de fumée | cercle fin gris de 0,4 à 0,6 H, laissé au point d'impact | 3 à 4 i24 | coups à la tête, blocages lourds (V2) |
| Étoile | étoile blanche de 0,3 H | 1 i24 | chaque coup d'une rafale (V2 3130-3166) |
| Boule d'impact | disque granuleux de 0,3 à 0,4 H, qui **reste sur place** et pâlit | 3 à 4 i24 | coups d'énergie ; en rafale, deux boules se chevauchent |
| Étoile de lame | étoile à 8 branches de 0,3 H, puis 8 à 10 rayons, puis tirets qui s'écartent et montent | 1 + 1 + 4 à 5 i24 | coupe qui touche (V2 1418-1425) |
| Choc métal | étoile rouge, ≈ 10 gouttes sombres et tirets jaunes | étincelles 4 i24, gouttes 6 i24 | griffe contre sabre (V2 1566-1572) |
| Cône de fumée | cône blanc de 1,5 H qui sort du dos du touché, se tord en anneaux | 5 i24 | coup chargé (V2) |
| Sphère d'énergie | 0,8 à 1 H, pleine 1 à 2 i24, puis pâlit **sans changer de taille** ; onde grise de 3,5 H | 6 à 7 i24 ; onde 2 i24 | coup chargé (V2) |
| Éclat final | étoile, disque plein de 0,5 H qui grandit et pâlit, une douzaine d'étincelles en rayons qui finissent en points | 8 i24 | coup final (V1 426-433 ; V2 3184-3191) |

Les étincelles sont des tirets de 0,05 à 0,1 H dans le sens du coup : tirets pendant 3 i24,
puis points pendant 5 à 7 i24. Couleur : celle de l'énergie du frappeur.

### 10.7 Image d'impact (V2)

Pour un coup **décisif** seulement : trois ou quatre fois par combat (V2 986, 1808, 2358, 2515,
2556, 2975, 3179).

1. **Armé tenu** 7 à 10 i24. Pour un coup chargé, la scène s'assombrit de 15 % pendant ce
   temps.
2. **Image noire**, 1 i24 : fond noir, personnages en blanc flou, une quarantaine de traits
   radiaux sombres, une boule blanche au point de contact.
3. **Image blanche**, 1 i24 : l'écran entier.
4. **Image délavée**, 1 i24 : l'image normale surexposée (environ + 60 % de luminosité), la
   caméra resserrée d'environ 1,3 fois sur le contact.
5. Retour aux couleurs, **pose de contact tenue** 10 à 11 i24 pendant que les étincelles et la
   caméra bougent.

On ne dessine pas le contact en couleurs normales : le noir et le blanc le cachent. Version
courte pour un coup secondaire : 1 i24 sombre (luminosité moitié), 1 i24 surexposée, sans
blanc (V2 1826-1827).

**Fonction** : un filtre plein écran avec trois modes (`inverse`, `blanc`, `delave`) et une
teinte de scène (`assombrir`, `desaturer`, `teinter`).

### 10.8 Lumière et couleur de scène (V2)

- **Pouvoir activé** : 1 i24 de flash plein écran à la couleur du pouvoir, puis 2 i24 de
  teinte qui s'efface (V2 1513-1515).
- **Lutte de force** : décor désaturé et assombri pendant toute la lutte, seule la lumière du
  pouvoir garde sa couleur ; les couleurs reviennent en 5 i24 (V2 2517-2563).
- **Coup final** : image teintée (assombrie, jaune) pendant 3 i24 (V2).
- **Onde de pouvoir plein écran** (V2 84-167) : l'écran rougit pendant 12 i24, puis quatre
  écrans d'une image chacun (blanc avec la silhouette hachurée, négatif, rouge uni, rouge
  sombre avec vignette), une image floue, et la teinte rouge reste 50 i24 avant de revenir au
  gris en 18 i24.
- **Après un gros contact** : voile de brume grise sur tout le décor pendant 1 i24 (V2).
- Chaque personnage a **sa couleur d'énergie** sur ses traînées, éclats, particules et lignes
  de vitesse.

### 10.9 Énergie (V2)

- **Poing allumé** : boule de 0,1 à 0,25 H qui grandit en 4 i24 pendant l'armé ; la flamme
  change de forme à chaque image pour que l'armé tenu reste vivant.
- **Lame enchantée** : bande de flamme de 0,6 H, environ 3 fois la largeur de la lame, bords en
  dents de scie ; elle sert de traînée permanente et s'éteint en 3 i24.
- **Particules** : une trentaine de pétales de 4 à 8 px qui flottent sans gravité pendant
  environ 15 i24 après le coup.
- **Rayon** : cône translucide de 4 H qui s'élargit de 0,1 à 0,3 H, une salve toutes les
  4 i24 ; un rayon continu reste vivant par une boursouflure qui le parcourt toutes les 5 i24 ;
  il s'éteint en 2 i24 (fuseau, trait, rien) (V2 2196-2211).
- **Arme qui apparaît** : elle pousse depuis la main en tournant, sa longueur multipliée par
  1,5 à chaque image sur 5 à 6 images ; la partie tranchante n'apparaît qu'à l'arrêt de la
  rotation (V2 2246-2279).

### 10.10 Poussière au sol (V2)

- **Glissade** : une rangée de petits dômes gris (0,1 à 0,15 H) posés au sol tout le long de
  la trace, qui naissent sous le corps et restent derrière lui 7 à 13 i24, plus une gerbe de
  virgules blanches vers le haut (8 i24) (V2 993-1006, 1936-1947).
- **Impact lourd ou blocage lourd** : une ellipse blanche plate d'environ 0,8 H sous les pieds,
  4 i24 (V2 915).
- **Coup qui écrase ou projette** : un anneau de 1,5 à 2,5 H sur 2 i24 avec des volutes au sol.
- **Pouvoir** : la poussière soulevée reste en tapis environ 45 i24 et marque l'endroit.

Notre `vfx.gd` fait déjà une poussière (`poussiere`) et une onde au sol (`onde`) : il faut les
comparer à ces mesures.

### 10.11 Secousse de caméra

Toujours **verticale**, et elle change de sens à chaque image. Confirmée.

| Force | Amplitude | Durée | Preuve |
|---|---|---|---|
| Coup léger d'une rafale | 0,015 H | 1 i24 | V1 152-160 |
| Atterrissage, frappe du pied | 0,02 H | 2 i24 | V1 26, 108 |
| Coup appuyé | 0,04 à 0,06 H | 2 à 4 i24 | V1 272, 292 |
| Coup qui touche (V2) | 0,05 à 0,13 H | 3 à 5 i24 | V2 761, 772, 1418-1421 |
| Coup lourd, impact final | 0,08 à 0,11 H | 8 i24 | V1 321, 426 |
| Coup chargé, contact tenu | 0,15 H, qui décroît | 13 à 19 i24 | V2 1811-1825 |
| Expulsion, projection | 0,15 à 0,23 H, décroissance d'environ 0,75 par image | 6 à 25 i24 | V1 441 ; V2 988-1012, 3181-3191 |
| Rafale | 0,07 à 0,08 H, relancée à chaque contact | toute la rafale | V2 3130-3166 |
| Pouvoir maintenu (grondement) | 0,12 H, sans décroissance, arrêt net à la fin | toute sa durée | V2 2196-2213 |
| Longue tenue de contact | 0,01 H à chaque image | toute la tenue | V2 1260-1339 |

- La plus forte secousse va à l'expulsion, pas au contact. Confirmée.
- Le premier écart va vers le bas en V1 ; en V2 il part dans un sens ou dans l'autre, et le
  deuxième écart est parfois plus grand que le premier.
- Pas de secousse sur un coup dans le vide, sauf pour un pouvoir maintenu (grondement).
- **Fonction** : `secousse(force, duree, decroissance)`. Par défaut, la suite
  `force × (1, −0,6, 0,35, −0,2, 0,1)` pour un coup ; décroissance de 0,75 par image pour une
  projection ; décroissance nulle pour un grondement.

### 10.12 Caméra (V2)

V1 a un cadre fixe. V2 fait bouger la caméra en permanence :

- **Travelling** qui suit l'attaquant pendant une rafale, et qui freine (7, 6, 6, 5, 4, 4, 2,
  1 px par image) (V2 3130-3140).
- **Zoom avant d'environ 1,3 fois** en une image sur le contact d'un coup important, puis
  retour progressif sur 6 i24 (V2 1474) ou retour à l'image suivante.
- **Zoom lent** de + 20 % pendant une longue tenue (V2 1250-1343), ou de 1,4 fois pendant que
  l'action est figée 10 i24 (V2 60-79).
- **Travelling** : départ qui accélère sur 10 à 12 i24, freinage sur 6 à 8 i24 (V2 560-763).
- Pendant un dialogue ou une mise en place, la caméra est **totalement fixe** (V2 612-727).
- La caméra suit un projeté vers le haut : le sol descend d'environ 0,5 H par image dans le
  cadre (V2 2173-2183).
- **Fin de combat** : coupe directe sur la pose de victoire, tenue au moins 25 i24, dérive de
  caméra qui ralentit puis s'arrête (V2 2640-2659).

Pour nous : la caméra d'un jeu de combat 2D suit les deux personnages. On garde la secousse,
le zoom de 1,3 fois sur les coups décisifs et la caméra qui suit un lancé ; le reste est pour
les mises en scène (intro, Rage Art, victoire).

### 10.13 Arrêt sur image

- **V1** : 2 i24 où les deux personnages gardent exactement le même dessin, seule la caméra
  bouge (coups appuyés et lourds).
- **V2** : jamais d'arrêt strict. Il est remplacé par un coup planté qui pousse (4 à 8 i24),
  par une pose tenue pendant que les effets changent, par l'image d'impact noire puis
  blanche, ou par un **ralenti** de 10 à 12 i24 (Rai et Zen suspendus en l'air, V2 108-119).
- **Pour nous** : un jeu de combat a besoin d'un arrêt sur image (hitstop) pour que le joueur
  sente le coup et puisse enchaîner. On le garde (2 i24, soit 5 i60, pour un coup appuyé), mais
  pendant ce temps on laisse vivre les éclats, la traînée et la caméra, comme en V2.

### 10.14 Quel effet pour quel coup

| | Traînée | Éclat | Secousse | Arrêt | Flou, fantômes | Zoom | Image d'impact |
|---|---|---|---|---|---|---|---|
| Coup léger | oui | petite étoile ou bouffée | une fois sur deux, 0,015 H | non | non | non | non |
| Coup appuyé | oui | bouffée ou anneau | 0,05 H, 3 i24 | 5 i60 | non | non | non |
| Coup lourd | oui, longue | anneau, étincelles | 0,1 H, 5 i24 | 5 i60 | sur le touché | parfois | non |
| Coup bloqué | non | anneaux gris, poussière au sol | 0,05 H | 5 i60 | non | non | non |
| Coup dans le vide | oui | non | non | non | fantômes de celui qui esquive | non | non |
| Spécial, coup chargé | oui, couleur d'énergie | sphère, cône, étincelles | 0,15 H, 13 à 19 i24 | tenue de contact | oui | 1,3 fois | version courte |
| Heat Smash, Rage Art, KO | oui | éclat final | 0,2 H, longue | tenue de contact | oui | 1,3 fois | complète |

---

## 11. Armes (V2)

- **Garde au sabre** : fente d'environ 1 H, sabre d'une main pointé vers l'adversaire, tenue
  5 à 11 i24 avant l'attaque (V2 1372-1378).
- **Armé** : 1 à 3 i24 seulement (V2 1416, 1501-1502).
- **Après la coupe**, le sabreur **traverse** et finit 5 à 8 i24 plus loin en pose basse, dos à
  la cible (V2 1418-1425, 1537).
- **Arme longue** : le porteur ne fait pas le pas de 0,45 H au contact ; il garde environ
  1,5 H de distance, buste droit, bras tendu. La portée vient du manche (V2 2360, 2455).
- **Moulinet déflecteur** : une ellipse verticale fine de 1,2 H devant le corps ; chaque
  projectile dévié laisse un gribouillis de sa couleur, 0,2 H, 2 à 4 i24 (V2 2403-2431).
- Les arcs sont décrits au § 10.2.

---

## 12. Caractère : le costaud et le rapide

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
| Esquive | n'esquive pas | au dernier moment, pieds fixes, 2 i24 |

C'est le rapport des durées (1 à 3) qui raconte la différence, pas la taille des coups (V1).
V2 confirme : le boss prépare peu mais frappe lourd et encaisse sans tomber ; les héros volent
à chaque coup reçu.

---

## 13. Notre `coup_de_poing_rue` face aux références

| Point | Chez nous aujourd'hui | Dans les références |
|---|---|---|
| Armé, bras de frappe | avant-bras ouvert à la verticale, main en l'air | coude fermé, poing derrière la tête |
| Armé, bras libre | tendu devant, ouvert | replié serré contre la poitrine |
| Buste à l'armé | presque droit, renversé en arrière | 45° vers l'avant, d'un trait avec la jambe arrière |
| Jambes à l'armé | pieds à environ 0,45 H, bassin haut | fente de 0,8 à 1 H, bassin bas, jambe arrière tendue |
| Trajet du poing | plusieurs dessins intermédiaires | aucun, une traînée courbe |
| Corps au contact | avance de 30 unités (0,17 H) | avance de 0,45 H, aligné du pied au poing |
| Bras au contact | tendu, puis reste tendu | tendu, puis continue son arc ou reste planté en poussant |
| Buste au contact | environ 40° | 80 à 90° |
| Bras libre au contact | devant le corps | jeté à l'opposé |
| Arrêt sur image | 9 i60 | 5 i60, avec les effets qui continuent de vivre |
| Secousse | aucune | verticale, 0,1 H, 5 i24 |
| Fin | se rattrape et revient en garde | pose déséquilibrée tenue 4 à 7 i24 |
| Effet au contact | cônes et anneaux dessinés | bouffée qui sort dans le dos, anneau de fumée, étincelles |

À refaire en suivant le tableau de phases du § 4, une fois la traînée et l'étirement codés.

---

## 14. Liste de contrôle avant de valider une animation

1. La pose armée et la pose de contact sont-elles lisibles seules, en silhouette noire ?
2. Chaque pose forte tient-elle sur une ligne simple, penchée ?
3. Les pieds sont-ils assez écartés et le bassin assez bas ?
4. Y a-t-il un bras à moitié ouvert ou qui pend sans raison ?
5. Le bras libre fait-il le contraire du bras de frappe, ou arme-t-il le coup suivant ?
6. Le trajet tient-il en 0 image (coup court) ou en 1 à 3 images avec traînée (coup ample) ?
7. Le corps avance-t-il sur l'image du contact (sauf arme longue) ?
8. Le coup traverse-t-il la cible, ou reste-t-il planté en poussant ?
9. Les durées respectent-elles le caractère (préparation, frappe, récupération) ?
10. Les tenues vivent-elles (dérive, effets, caméra) ?
11. Le touché se plie-t-il autour du point d'impact, la partie touchée en premier ?
12. Les écarts d'un départ doublent-ils, ceux d'un arrêt se divisent-ils ?
13. Les effets sont-ils au bon niveau pour la force du coup (§ 10.14) ?
14. Sur la planche, voit-on les deux personnages avec des lignes opposées ?

---

## 15. Ce qui reste à apprendre

- Les **coups de pied circulaires** vus de près (V2 en montre, mais en plan large et en 360p).
- Les **projections** de près : V2 en montre deux, rapides et peu lisibles.
- Les **chutes au sol** complètes et le KO vu de près.
- L'**alternance bras gauche et bras droit**, illisible sur un personnage d'une seule couleur.
- Une référence de **vrai jeu de combat** (hitstop, recul sur garde, enchaînements) : les deux
  vidéos sont des films, pas des jeux.
- Ce qui change à **60 images par seconde** : les deux vidéos sont à 24, et leur côté sec vient
  en partie de là. Il faudra décider si nos coups tiennent leurs poses par paliers de 2 ou
  3 i60.

### Lectures incertaines

- L'angle exact du coude à l'armé : entre 60° et 90° (V1, 360p).
- L'étirement du bras au contact : lisible en V1, pas en V2.
- Les membres pendant les impacts cachés par les éclats (V1 426-439 ; V2 1250-1343).
- À qui est le sang en V2 1431-1435 et 1566-1607.
- Les mesures de secousse de V2 mélangent secousse et zoom sur les images de recadrage.
