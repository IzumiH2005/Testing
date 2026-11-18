# Analyse : gauche-droite (jab puis direct) depuis la garde réaliste du bagarreur

Enchaînement de deux coups droits, sans pas, depuis la garde réaliste de
`analyses/garde_ouverte_bagarreur.md` § 10 : d'abord le **jab** du bras avant (gauche, bras F,
côté opposé à la caméra), puis le **direct** du bras arrière (droit, bras N, côté caméra).

> **État : EN COURS, non validé par le critique.** Commité seulement pour pouvoir reprendre
> dans une autre session, à la demande de l'utilisateur.
> - Fait : clés posées et corrigées sur le mannequin (poing F fixé à la joue de f13 à f22, dans le
>   repère de la tête : main (−15, −22, 23), coude rentré ; bassin plus bas et plus avancé sur le
>   direct, y 85 et x +2,6 à f17). Vérificateur sans traversée. L'utilisateur a vu le GIF v2.
> - Reste : réviser cette fiche (11 défauts du critique : axes des jambes par clé, nommage des
>   vues, sens de `armX_r`, citation A bis 5, durée du retour, force du jab, regard ; nouvelles
>   valeurs ci-dessus ; raccord de l'image 39, jamais affichée en jeu), la refaire valider, puis
>   `tools/critique.sh anims/gauche_droite_bagarreur.json DOSSIER --de 0 --a 39 --vue
>   -40,40,160,140` et boucler jusqu'au VALIDÉ.
> - Les clés se posent sur le mannequin avec `tools/cles_vers_poses.gd` puis `tools/mannequin.sh`.
> - `coup_de_poing_garde_bagarreur` (fiche et anim) est aussi en cours, non validé : à remplacer
>   par cette animation ou à restaurer.

Demande de l'utilisateur : « Et fais une gauche puis une droite ».

Animation : `anims/gauche_droite_bagarreur.json` (39 images, base `garde_ouverte_bagarreur`,
lacet +45), suivie de `garde_ouverte_idle_bagarreur`.

Cette animation remplace le direct seul (`coup_de_poing_garde_bagarreur`) : le direct en
est la seconde moitié, mieux chargé, parce que le jab qui le précède tord déjà le corps dans
le sens qui le lance.

Conventions : torsion **totale** = torsionBassin (tb) + torsion du buste (t). Négatif : les
épaules tournent épaule avant (F) vers la cible, épaule arrière (N) en arrière ; positif :
l'inverse. Garde : tb −12, t −4, total −16.

## 1. La logique du mouvement

1. **Le jab sert à quelque chose.** Il mesure la distance, cache la droite et, surtout,
   **charge** le direct : pour allonger le bras avant, l'épaule avant avance et l'épaule
   arrière recule. Le corps finit le jab tordu à −42, soit 26° plus « fermé » que la garde :
   c'est l'armé du direct, gagné sans recul visible du poing droit.
2. **Le jab part de la clavicule, sans armer.** Le poing gauche est déjà devant. Il part en
   ligne droite vers le menton adverse ; le coude ne s'écarte pas, il se met dans l'axe et se
   tend en dernier. Le bassin tourne un peu (−12 → −16) : un jab est un coup de bras et
   d'épaule, la hanche avant l'accompagne sans le lancer. Le genou avant se fléchit d'un
   rien (le poids passe un peu devant).
3. **Pendant le jab, la droite reste au menton.** Le poing N ne fait que suivre le buste
   (déplacement ≤ 5 par image, venu de la rotation), il protège le menton.
4. **L'épaule avant monte au contact du jab** (`epauleF_haut` +1 → +3) : elle abrite le
   menton du côté exposé.
5. **La gauche revient à la joue, pas à la clavicule.** Pendant le direct, le corps tourne de
   l'autre côté : c'est maintenant le côté gauche du visage qui est exposé. Le poing gauche
   rentre donc par la ligne d'aller, puis se pose à la joue gauche, coude bas, et y reste
   jusqu'au retour.
6. **Le direct commence par le bassin, pendant que la gauche rentre.** Le bassin part vers la
   cible (tb −10 → +6) quand les épaules sont encore tournées à −40 : le tronc se tord, il
   emmagasine. Puis les épaules suivent et le poing droit part en ligne, de plus en plus vite,
   le coude se tend en dernier (comme le direct seul, voir § 1 de
   `coup_de_poing_garde_bagarreur.md` dans sa version de garde réaliste).
7. **La jambe arrière pousse.** Talon déjà levé ; le genou arrière rentre (rotation interne
   de hanche, `thighN_r` −2 → +10), il se tend un peu (genou 10,5 → 7), le talon monte encore.
   La hanche avant tourne en sens inverse du bassin (`thighF_r` suit −tb) : c'est le bassin
   qui tourne sur un pied avant fixe.
8. **La tête reste à niveau et derrière l'épaule qui frappe.** Le cou compense une partie de
   la rotation, le regard reste sur la cible.
9. **Retour par le même chemin.** Le poing droit revient au menton par sa ligne, la gauche
   redescend de la joue à la clavicule, bassin et buste reviennent à la garde.

## 2. Anatomie

| Partie | Articulations et axes | Muscles | Rôle |
|---|---|---|---|
| Épaule gauche (F), jab | flexion 32 → 90 ; adduction horizontale (plan −17,5 → −38 : le bras vient dans l'axe) ; rotation −9,7 → +15 (pronation de la chaîne, poing paume en bas) ; omoplate en protraction, `epauleF_haut` +3 | deltoïde antérieur, grand pectoral (faisceau claviculaire), dentelé antérieur | pousse le poing gauche vers la cible |
| Coude gauche, jab | extension 97 → 18, puis flexion 18 → 130 (joue) | triceps ; biceps et brachial au retour | se tend en dernier, se replie vite |
| Épaule droite (N), jab | ne bouge pas (rotation et plan de garde), entraînée par le buste | — | garde le poing au menton |
| Épaule droite (N), direct | flexion 31 → 98,5 ; plan +14,6 → +45,5 (le bras vient dans l'axe de la cible) ; rotation +3,7 → −34 (pronation) ; `epauleN_haut` −3 → −1 au contact | deltoïde antérieur, grand pectoral, dentelé antérieur | pousse le bras vers la cible |
| Coude droit, direct | extension 127 → 14 | triceps | dernier segment de la chaîne |
| Épaule gauche (F), direct | élévation 43, plan −28,5, rotation +6,5 (joue) ; `epauleF_av` 0 → −3 (l'omoplate recule) | rhomboïdes, trapèze moyen, deltoïde antérieur | recule avec la rotation, tient le poing à la joue |
| Bassin | rotation −12 → −16 (jab), puis −16 → +16 (direct) ; translation x 0 → 6,8 | fessiers, obliques | part **avant** les épaules dans le direct |
| Tronc | jab : t −4 → −26 ; direct : t −40 → +35 | obliques, grand dorsal | transmet la rotation, se tord avant le direct |
| Jambe arrière (N) | cheville : flexion plantaire qui s'accentue (talon levé de 14,8 à 17,3) ; genou 10,5 → 7 ; hanche : rotation interne −2 → +10 | triceps sural, quadriceps, grand fessier, adducteurs | moteur du direct |
| Jambe avant (F) | genou 25 → 33 au contact du direct ; hanche en rotation relative inverse du bassin (+7,6 au jab, −19,7 au direct) | quadriceps, moyen fessier | pivot, reçoit le poids |
| Cou | rotation : neck_r = −0,6 × (tb + t + 16) | sterno-cléido-mastoïdien, splénius | tête à niveau, regard sur la cible |

D'où vient la force :
- jab : épaule avant → coude → poing, avec un quart de tour du buste ;
- direct : sol → avant-pied arrière → genou et hanche arrière → bassin → tronc (déjà tordu par
  le jab) → épaule droite → coude → poing.

## 3. Phases (60 images/s)

Bible § C : jab force 1-2, direct force 2 (anticipation 1-2 i24, trajet 0, tenue 1-2 i24,
retour 2-4 i24, ×2,5 à 60 i/s). Le jab n'a qu'une anticipation de 3 images (il doit rester
sec) ; le direct n'a pas d'anticipation propre : le retour du jab **est** son armé.

| Images | Phase | Ce qui bouge |
|---|---|---|
| 0-3 | il se pose (3 i) | il se ramasse d'un rien (y 87 → 86,6), torsion totale −16 → −13 (légère ouverture), les poings ne bougent pas (≤ 1,1 par image) |
| 3-6 | jab, trajet (3 i) | torsion −13 → −23 → −33 → −40 ; poing F, écarts 6,4 / 13,1 / 13,3 ; coude F 97 → 90 → 66 → 18 |
| 6 | contact du jab | bras F tendu dans l'axe, poing F à (69,4 ; 139 ; z −0,8), `epauleF_haut` +3 |
| 6-9 | tenue du jab (3 i) | le buste continue de 2° (−40 → −42), le poing dérive de 2,3 en z |
| 9-13 | retour de la gauche + armé du direct | coude F 18 → 50 → 96 → 104 → 130 (joue) ; **le bassin part** (tb −16 → −10 → +6) alors que les épaules restent à −40 / −34 |
| 13-17 | direct, trajet (4 i) | torsion −34 → −18 → +22 → +38 → +47 ; poing N, écarts 5,9 / 11,7 / 14,8 / 16,8 ; coude N 127 → 124 → 106 → 78 → 14 |
| 17 | contact du direct | bras N tendu dans l'axe, poing N à (74,5 ; 137,8 ; z −1,9), `epauleN_haut` −1, `epauleF_av` −3 |
| 17-22 | dépassement et tenue (5 i) | le corps continue de 4° (47 → 51) puis revient (48) ; le poing reste à ≤ 3 par image |
| 22-28 | retour du bras droit | coude N 14 → 106 par la ligne ; le poing F quitte la joue vers la clavicule |
| 28-33 | retour au menton | coude N 106 → 127, torsion +16 → −10 |
| 33-39 | retour en garde | derniers degrés de bassin et de buste jusqu'à la garde, `suivante` : idle de garde |

## 4. Poses clés, tous les axes

Lacet de l'animation : +45. Ce qui n'est pas cité vient de la garde
(`poses/garde_ouverte_bagarreur.json` : spineLow 4, chest 4, neck 3, thighN −26, thighF 14,
thighN_p 15, thighF_p −15, `epauleF_av` −1, `epauleN_av` 0, `epauleF_haut` 1,
`epauleN_haut` −3). Bras notés élévation / plan / rotation / coude. Genoux : valeurs mesurées
sur la pose échantillonnée. Le cou suit `neck_r` = −0,6 × (tb + t + 16) sur chaque clé.

**Image 0 (garde).** Fiche de garde § 10. Bras F 32 / −17,5 / −9,7 / 97 (poing à la
clavicule), bras N 31,3 / +14,6 / +3,7 / 127 (poing au menton). Genoux N 9,7, F 24,8.
`thighN_r` −2, `thighF_r` +5.

**Image 3 (il se pose).**
- Pieds : en place, talon N levé (cheville N à 14,8 au-dessus du sol au lacet 45).
- Genoux : N 10,5, F 25 ; hanches : `thighN_r` −2, `thighF_r` +2,9.
- Bassin : tb −11, x −0,3, y 86,6. Buste : t −2, total −13. Buste droit.
- Épaules de garde, bras de garde. Tête : neck_r −1,8.

**Image 4 (le poing gauche part de la clavicule).**
- Bassin tb −13, x 0,5 ; buste t −10, total −23.
- Bras F : 39 / −12,5 / +12 / 89,5 (le coude ne s'ouvre presque pas : le poing part droit,
  l'avant-bras tourne).
- Bras N : garde. Genou F 24,7, `thighF_r` +5,1. Tête : neck_r +4,2.

**Image 5.**
- Bassin −15, x 1,2 ; buste −18, total −33.
- Bras F : 56 / −28 / +14 / 66,5 ; `epauleF_haut` +2.
- `epauleN_av` −1 (l'épaule arrière recule avec la rotation). Genou F 25,9, `thighF_r` +7,2. Tête : neck_r +10,2.

**Image 6 (contact du jab).**
- Bassin −16, x 1,75, y 86,6 ; buste −24, total −40 ; buste droit.
- Épaule F : élévation 90 (bras à hauteur d'épaule), plan −38 (dans l'axe de la cible),
  rotation +15 (poing paume en bas), `epauleF_haut` +3 (l'épaule monte contre le menton),
  `epauleF_av` −1. Coude F 18 (tendu, pas verrouillé).
- Bras N : garde, poing au menton (24,8 ; 127,4 ; z −21,1), `epauleN_av` −1.
- Hanche F : `thighF_r` +7,6, genou F 23,8 ; jambe N : genou 10, `thighN_r` −2.
- Tête : neck_r +14,4, à niveau (y 152,4).

**Image 9 (fin de tenue du jab).** Buste −26, total −42, x 2,2. Bras et jambes comme 6.

**Image 11 (la gauche revient, le bassin part).**
- Bassin −10 (+6° depuis 9), x 2, y 86,7 ; buste −30, total −40 : les épaules n'ont pas
  bougé, le tronc se tord.
- `thighN_r` +2 (le genou arrière commence à rentrer), genou N 10,5 ; `thighF_r` +2,2.
- Bras F : 49 / −34,5 / +16 / 95,5 (retour par la ligne) ; `epauleF_haut` +2.
- Bras N : garde. Tête : neck_r +14,4.

**Image 13 (gauche à la joue, bassin lancé).**
- Bassin +6, x 3, y 86,8 ; buste −40, total −34.
- `thighN_r` +6, genou N 11 ; `thighF_r` −14.
- Bras F (joue) : 43 / −28,5 / +6,5 / 130,5, poing à (31,7 ; 140 ; z −5,7). `epauleF_haut` +1.
- Bras N : garde. Tête : neck_r +10,8.

**Image 14 (le poing droit part).**
- Bassin +10, x 5, y 87 ; buste −28, total −18 ; `thighN_r` +8, genou N 10.
- Bras N : 34,5 / +4,5 / −13,5 / 123,5. Bras F : joue. Tête : neck_r +1,2.

**Image 15.**
- Bassin +12, x 5, y 86,6 ; buste +10, total +22 ; `thighN_r` +9, genou N 9 ; genou F 32.
- Bras N : 38,5 / +27,5 / −32 / 106. `epauleF_av` −1. Tête : neck_r −22,8.

**Image 16.**
- Bassin +14, x 5,6 ; buste +24, total +38 ; `thighN_r` +10, genou N 8.
- Bras N : 55,5 / +35,5 / −33 / 78. `epauleF_av` −2, `epauleN_haut` −2. Tête : neck_r −32,4.

**Image 17 (contact du direct).**
- Jambe N : rotation interne +10, genou 7, talon levé (cheville à 16,4 du sol).
- Jambe F : genou 32,7, `thighF_r` −19,7, pied à plat.
- Bassin +15, x 6,4, y 86,5 ; buste +32, total +47 ; buste droit.
- Épaule N : élévation 98,5, plan +45,5, rotation −34, `epauleN_haut` −1, `epauleN_av` 0.
  Coude N 14.
- Épaule F : joue (43 / −28,5 / +6,5 / 130,5), `epauleF_av` −3.
- Tête : neck_r −37,8, à niveau (y 152,3), derrière l'épaule N.

**Image 20 (dépassement).** Bassin +16, buste +35, total +51, x 6,8 ; `epauleF_av` −3,
`epauleN_haut` −3 (l'épaule redescend). Bras comme 17.

**Image 22 (fin de tenue).** Bassin +15, buste +33, total +48 ; jambes comme 17 ;
`epauleF_av` −2.

**Image 28 (retour).**
- Bassin +6, buste +10, total +16, x 6, y 86,8 ; `thighN_r` +5, genou N 8.
- Bras N : 38,5 / +27,5 / −32 / 106 (même angle qu'à l'aller, image 15).
- Bras F : 37,5 / −23 / −1,6 / 113,7 (de la joue vers la clavicule). `epauleF_av` −1.

**Image 33 (poing au menton).** Bassin −6, buste −4, total −10, x 1,5 ; `thighN_r` 0 ;
bras N et F de garde.

**Image 39 : garde exacte.**

## 5. Ce qui se voit

Définition des vues (lacet **total** = lacet de l'animation + lacet de la caméra) :
- **vue du jeu** : lacet 45 (trois quarts) ;
- **profil** : lacet total 0, la cible est à droite de l'écran ; c'est là que se lisent les
  hauteurs et les lignes de frappe ;
- **face** : lacet total 90, le personnage regarde la caméra ; c'est là que se lisent les
  coudes (aile de poulet) et la largeur.

- **Vue du jeu.** La gauche part de la clavicule et s'allonge ; les épaules se ferment ; la
  gauche rentre à la joue pendant que la ceinture tourne déjà (11-13) ; puis la droite part du
  menton vers la caméra et la cible. Le genou arrière qui rentre et le talon qui monte se lisent
  sur la jambe proche.
- **Profil.** Les deux poings traversent l'écran presque à l'horizontale, à hauteur du menton
  adverse (139 pour le jab, 137,8 pour le direct ; tête à 152). La tête ne bouge pas en
  hauteur.
- **Face.** Le coude du bras qui frappe reste sur l'axe épaule-poing au contact (1,0 pour le
  jab, 0,8 pour le direct) : pas d'aile de poulet. La gauche à la joue est sur le côté du
  visage, pas devant.

**Limites du rig, connues.**
- Le bassin n'avance que de 6,8 au plus : le pied avant est fixe et la hanche ne peut pas
  passer plus loin sans décoller le pied. Un vrai direct transfère un peu plus le poids ; ici
  il se lit par la rotation et le genou avant qui plie (25 → 33).
- Le genou arrière ne descend qu'à 7 au contact : plus tendu, la cheville arrière décolle de
  sa place.
- Le moteur re-résout une jambe « posée » (cheville presque immobile entre deux clés, moins de
  0,35) par une IK plane qui ignore l'écartement et la rotation de hanche ; le genou saute
  alors d'environ 5°. Les clés sont réglées pour que la cheville arrière bouge de plus de 0,35
  entre deux clés, sauf à la dernière image (39), toujours re-résolue : le genou N y vaut
  12,2 au lieu de 9,7. C'est la même résolution que l'idle de garde qui suit : le raccord se
  fait sans saut.

## 6. Références

- Fiche de garde : `analyses/garde_ouverte_bagarreur.md` § 10.
- `analyses/coup_de_poing_garde_bagarreur.md` : le direct seul (même chaîne, même contact).
- `analyses/coup_de_poing_rue.md` : chaîne hanche → épaules → coude en dernier.
- Vidéo 2 (`etudes/02_rai_zen_armagon/02_corps_a_corps_1.md`, jab 859) : jab court, une image
  d'élan, pas de traînée sur les coups courts.
- Vidéo 1 (`etudes/01_strength_vs_speed/03_lancers_176_257.md`, V1 173-187) : coup depuis la
  garde, contact aligné épaule-poing, tenue lisible.
- Bible :
  - A bis 1 : la jambe arrière pousse, talon levé ;
  - A bis 3 : bassin avant les épaules, épaules avant le poing (images 11-15) ;
  - A bis 4 : écarts du poing croissants jusqu'au contact ;
  - A bis 5 : trajet court à 60 i/s (3 images pour le jab, 4 pour le direct) ;
  - A bis 7 : dépassement puis tenue ;
  - A bis 12 : le coude ne fait que se déplier jusqu'au contact ;
  - § C forces 1-2 : durées.

## 7. Contrôles

Mesures au profil (lacet total 0) sauf mention.

1. **Coudes.** F : 97, 90, 66, 18 (images 3-6), sans remonter avant le contact. N : 127
   jusqu'à 13, puis 124, 106, 78, 14 (14-17), sans remonter.
2. **Rotation du bras qui frappe, monotone.** armF_r : −9,7 → +12 → +14 → +15 (contact) →
   +16 → +6,5 (joue). armN_r : +3,7 → −13,5 → −32 → −33 → −34 (contact).
3. **Écarts du poing par image.** Jab : 6,4 / 13,1 / 13,3. Direct : 5,9 / 11,7 / 14,8 / 16,8.
   Le poing qui ne frappe pas bouge de ≤ 5 par image, seulement entraîné par le buste.
4. **Bassin avant les épaules (direct).** De 9 à 13, tb passe de −16 à +6 (+22°) quand la
   torsion totale passe de −42 à −34 (+8°).
5. **Contacts.** Jab : poing F à (69,4 ; 139 ; z −0,8). Direct : poing N à (74,5 ; 137,8 ;
   z −1,9). |z| ≤ 3 : sur la ligne de frappe. Coude à ≤ 1 de l'axe épaule-poing en face.
6. **Tenue.** Jab : 3 images, le poing dérive de 2,3. Direct : 5 images, dérive totale 4,6
   (le dépassement passe par le tronc).
7. **Tête.** y entre 152,3 et 152,9 sur tout l'enchaînement.
8. **Poing gauche à la joue (13-22)** : y 140 ± 0,5, à environ 4 de la surface de la tête
   (rayon 16,5), hors de la tête.
9. **Rien ne traverse** (`--verifier`) : aucune alerte « … qui se traversent » ni « … dans … ».
   Alertes admises : « bras proche confondu avec le corps » et « bras proche peu visible » en
   garde (comme la fiche de garde § 10, contrôle 9), et « trajet rapide » sur le poing qui
   frappe ou qui revient (16-17, 11-12) : c'est la vitesse voulue.
10. **Genoux** (pose échantillonnée) : N 9,7 → 10,5 → 10 (jab) → 11 → 9 → 8 → 7 (contact) → 8 →
    10 ; aucun saut de plus de 1,5 entre deux images, sauf l'image 39 (12,2, voir § 5).
11. **Hanche avant opposée au bassin** : `thighF_r` +7,6 quand tb −16 ; −19,7 quand tb +15.
12. **Pieds, vue du jeu (lacet 45).** Pointe du pied N à x −33,0 à −33,9, y 6,6 à 8,2 ;
    cheville N de y 14,8 à 17,3 (le talon monte au direct). Cheville F à (20 ± 1 ; 8 ± 0,8).
    Aucun point sous le sol (point le plus bas ≥ 6,6). Face : cheville N dérive de 4,4 au plus.
13. **Stature** : `epaule*_av` ≤ 0 tout du long, buste droit (spineLow et chest de la garde).
14. **Images 0 et 39** : la garde (à la résolution du pied posé près, § 5).
