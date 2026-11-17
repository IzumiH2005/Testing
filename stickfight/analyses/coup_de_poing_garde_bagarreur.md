# Analyse : coup de poing depuis la garde ouverte du bagarreur

Coup du bras arrière (F, celui du coude levé), sans pas, depuis `poses/garde_ouverte_bagarreur.json`
(lacet −45, trois quarts dos). Demande de l'utilisateur : « juste un pivotement du buste pour
rapprocher le coude, et l'extension du coude pour donner le coup ». Animation :
`anims/coup_de_poing_garde_bagarreur.json`, suivie de `garde_ouverte_idle_bagarreur`.

## 1. La logique du mouvement

C'est le coup court du bagarreur : pas de recul, pas de pas, il frappe **de là où il est**. Toute
la force vient de la rotation du corps sur des pieds plantés, le bras ne fait que la transmettre.

1. **Le coude est déjà armé.** En garde, le coude arrière est levé sur le côté à hauteur
   d'épaule (rapport `etudes/postures_trois_quarts/rapport.md` § 2.2) : l'armé est fait. Il
   n'y a donc pas de grand recul, seulement un petit ressort (l'épaule arrière recule un peu,
   le corps se ramasse) pour que le départ se lise.
2. **Le pivot rapproche le coude.** Le bassin tourne vers la cible, puis les épaules, avec un
   temps de retard : l'épaule arrière avance, et le coude levé, porté par l'épaule, passe du
   côté du corps à devant le corps, toujours à hauteur d'épaule. Le bras se ferme vers l'avant
   (le coude se rapproche de la ligne du milieu).
3. **Le coude se déplie en dernier.** Quand le coude est devant, pointé vers la cible, le
   triceps déplie l'avant-bras : le poing part en ligne droite vers la tête adverse.
4. **L'autre côté fait le contraire.** L'épaule avant (N) recule d'autant que l'autre avance
   (c'est la même rotation). Le poing N reste au menton : c'est la garde pendant le coup.
5. **La tête ne pique pas.** Elle reste à niveau, le regard sur la cible ; elle avance un peu
   avec la rotation.
6. **Les pieds restent plantés.** Seule la jambe arrière pivote sur l'avant du pied : le genou
   arrière rentre vers l'avant (rotation de hanche), ce qui laisse le bassin tourner.

## 2. Anatomie

| Partie | Articulation | Muscles | Rôle |
|---|---|---|---|
| Jambe arrière (F) | hanche (rotation interne), genou, cheville | fessiers, adducteurs, mollet | pousse et pivote : le genou rentre, c'est le départ de la rotation |
| Jambe avant (N) | genou | quadriceps | reçoit le poids, reste pliée |
| Bassin | rotation sur les hanches | fessiers, obliques | tourne vers la cible **avant** les épaules |
| Tronc | rotation | obliques, grand dorsal | transmet ; l'écart bassin-épaules se crée puis se referme |
| Épaule de frappe (F) | flexion horizontale (adduction) ; omoplate qui revient au neutre | grand pectoral, deltoïde antérieur | ramène le coude levé de côté vers devant ; l'omoplate reste au neutre, l'allonge vient de la rotation des épaules |
| Coude de frappe | extension | triceps | se déplie en dernier, jusqu'au bras tendu |
| Épaule avant (N) | rétraction | rhomboïdes, trapèze | recule pendant que l'autre avance |
| Coude avant | flexion tenue | biceps | garde le poing au menton |
| Cou | stabilisation | muscles du cou | tête à niveau |

## 3. Les phases (60 images/s)

| Image | Phase | Ce qui se passe |
|---|---|---|
| 0 | garde | pose de garde, telle quelle |
| 0-5 | ressort | il se ramasse (bassin 1,5 plus bas), l'épaule arrière recule un peu, les épaules tournent un peu en arrière : le coude levé part légèrement en arrière |
| 5-8 | la hanche part | le genou arrière rentre, le bassin tourne vers la cible ; les épaules sont encore en arrière : écart maximal, le ressort est tendu |
| 8-10 | le coude se rapproche | les épaules suivent, l'épaule arrière avance ; le coude levé vient devant à hauteur d'épaule ; le coude est encore plié |
| 10-12 | extension, contact à 12 | le coude se déplie, le poing va droit vers la tête adverse ; épaule arrière devant, épaule avant derrière |
| 12-16 | dépassement | la rotation va un peu plus loin, l'épaule allonge encore d'un cran |
| 16-24 | tenue | la pose emportée dérive doucement |
| 24-48 | retour | le coude se replie, se relève sur le côté, les torsions reviennent : garde |

## 4. Chaque articulation, tous ses axes, à chaque clé

Torsions : `torsion` (épaules par rapport au bassin) et `torsionBassin` ; positif = côté N
devant, donc **négatif = épaule de frappe devant**. Bras F : `armF` (angle dans le plan, 0 =
le long du corps, 90 = devant à l'horizontale), `armF_p` (écartement sur le côté, négatif pour
le bras loin), `armF_r` (rotation), `foreF` (pli du coude).

| Clé | Bassin | Épaules (`torsion`) | Épaules absolues | Omoplate F (av / haut) | Bras F (armF, _p, _r, coude) | Bras N (armN, _p, _r, coude) ; omoplate N av | thighF_r | neck_r | Bassin x / y |
|---|---|---|---|---|---|---|---|---|---|
| 0 garde | 12 | 4 | 16 | 0 / −3 | −5, −80, −20, 100 | 31, 40, 40, 95 ; −1 | 15 | 0 | 0 / 84 |
| 5 ressort | 16 | 10 | 26 | −2 / −3 | −8, −85, −20, 102 | idem | 15 | −6 | −1 / 82,5 |
| 8 la hanche part | −5 | 30 | 25 (épaules restées en arrière) | −1 / −2 | −2, −80, −15, 100 | 25, 40, 40, 105 ; −1 | 0 | −5,4 | 1 / 83 |
| 10 coude devant | −12 | −12 | −24 | 0 / −1 | 68, −72, −50, 120 | 30, 45, 30, 125 ; −2 | −5 | 24 | 2,5 / 83 |
| 11 extension | −13,5 | −24 | −37,5 | 0 / −0,5 | 70, −68, −42, 85 | 30, 47,5, 30, 130 ; −2,5 | −7,5 | 32,1 | 3,25 / 83 |
| 12 contact | −15 | −35 | −50 | 0 / 0 | 107, −50, 0, 3 | 30, 50, 30, 135 ; −3 | −10 | 39,6 | 4 / 83 |
| 16 dépassement | −16 | −38 | −54 | 0 / 0 | 108, −52, 0, 0 | idem | −10 | 42 | 4,5 / 83 |
| 24 tenue | −15 | −35 | −50 | 0 / 0 | 104, −48, 0, 8 | idem | −10 | 39,6 | 4 / 83 |
| 34 retour | 0 | −10 | −10 | 0 / −2 | 50, −75, −40, 95 | 20, 45, 38, 115 ; −2 | 5 | 15,6 | 2 / 83,5 |
| 48 garde | 12 | 4 | 16 | 0 / −3 | −5, −80, −20, 100 | 31, 40, 40, 95 ; −1 | 15 | 0 | 0 / 84 |

Lecture de la colonne « épaules absolues » (`torsionBassin` + `torsion`) : de 5 à 8, le bassin
tourne (16 → −5) mais les épaules restent en arrière (26 → 25) : c'est le ressort. Elles
partent ensuite (−32 à 10, −50 au contact). `armF_p` suit cet angle absolu (−50 au contact)
pour que le bras tendu pointe **sur la ligne de frappe** et non à 45° de côté.

Bras N : le poing N passe du sternum (garde) **sous le menton, devant la joue (y ≈ 41 au
lacet total 0)** pendant le coup : le coude se plie (`foreN` 95 → 135) et s'écarte (`armN_p`
40 → 50), l'omoplate N recule (−1 → −3). `armN` reste à 30 : avec les épaules tournées à −50,
un `armN` plus bas enverrait le coude derrière le corps et rabattrait le poing dans la poitrine. C'est la
garde du visage pendant que l'autre bras frappe ; il revient au sternum au retour.

Jambes : pieds plantés. La jambe avant (N) est ancrée par l'outil (`ancre`) : sa cheville
garde sa place, la cuisse et le genou s'adaptent, `thighN_r` reste à −5, `thighN_p` 15. La
jambe arrière (F) pivote : `thighF_r` 15 → −10 (le genou rentre), `thighF_p` −15 ; sa cheville
est visée à sa place de garde (`vise legF`), le genou s'adapte (flexion entre 30 et 45).

Clés 10 et 11 (rythme) : le pivot ne va pas jusqu'au bout avant le dépliage (épaules à −24
à l'image 10, coude encore fermé à 120) ; la fin de la rotation et le dépliage se chevauchent
de 10 à 12 (bible A bis, chevauchement). Au lacet total 0, le poing avance de 27, 25, puis 16
et 18 : le dépliage accélère jusqu'au contact. À −45, le dépliage est raccourci par la vue
(il va en partie vers le fond) : à l'écran, les écarts décroissent régulièrement (28, 20, 13,
10), sans arrêt à la charnière entre le pivot et l'extension. Le poing monte sans cloche.

Retour (24 → 34) : le coude se replie et remonte sur le côté, le poing sort de la ligne de
frappe (z ≈ +16 vers l'image 28). C'est voulu : le bras reprend sa place de garde.

Cou : `neck` reste à 3 (la tête ne pique pas). `neck_r` compense 60 % de la rotation des
épaules, −0,6 × (épaules absolues − 16) : le regard reste vers la cible.

## 5. Ce qui se voit à lacet −45 (vue de jeu) et de profil

- Garde et ressort : le bras levé fait une barre vers l'arrière ; elle recule un peu.
- Pivot : la barre se raccourcit (le coude vient vers la caméra puis devant) ; l'épaule
  arrière passe devant la colonne.
- Contact : le bras F tendu vers la droite, à hauteur du menton adverse, devant la tête du
  bagarreur. Le poing N reste au menton.
- Au lacet total 0 (vue +45 de la planche), le bras tendu sort franchement devant ; le pivot se lit par le décalage
  des épaules.

## 6. Références

- Rapport des postures (`etudes/postures_trois_quarts/rapport.md`) § 2.2 : coude arrière levé.
- Vidéo 1 (V1 173-187) : coup lourd du rouge depuis la garde, contact aligné épaule-poing.
- `analyses/coup_de_poing_rue.md` : même chaîne (hanche, épaules, coude en dernier), sans le
  recul ici.
- Bible : A2 (anticipation, ici courte), A3 (chaîne et torsion), A bis (accélération jusqu'au
  contact, chevauchement : l'épaule part avant le coude).

## 7. Contrôles

1. Le coude F se déplie de 100 (image 8) à moins de 10 (image 12), sans revenir.
2. Le bassin tourne avant les épaules : à l'image 8, `torsionBassin` + `torsion` égale la
   valeur de l'image 5 à ±3 près, puis diminue.
3. Pendant le pivot, le coude F reste à hauteur d'épaule (± 10) : il ne plonge pas.
4. Au contact, le poing F est à hauteur du menton (entre l'épaule et le centre de la tête),
   sur la ligne de frappe (|z| < 5 au lacet total 0). Entre 10 et 12, le poing avance à
   chaque image et ses écarts augmentent (bible A bis 4) ; il reste à y 51–55 et |z| < 5
   (pas de cloche avant l'impact).
5. Rien ne traverse (`--verifier`) : le bras F ne passe pas dans la tête ni dans le bras N ;
   le poing et l'avant-bras N restent hors du tronc (le vérificateur ne contrôle pas bras
   contre tronc : à vérifier au calcul).
6. Les chevilles ne glissent pas (pieds plantés).
7. Stature (règle 6 du projet) : `epaule*_av` ≤ 0 tout du long. L'épaule F revient à 0 au
   contact (elle ne s'enroule pas vers l'avant) ; l'allonge du coup vient de la rotation des
   épaules, pas d'un dos qui s'arrondit. L'épaule N recule (−3). Le buste reste droit.
8. La pose de départ et la pose d'arrivée sont la garde exacte (raccord avec l'idle).
