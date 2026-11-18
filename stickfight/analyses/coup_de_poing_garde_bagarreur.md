# Analyse : coup de poing depuis la garde ouverte du bagarreur (version garde réaliste)

Direct du bras arrière (**droit**, bras N, côté caméra), sans pas, depuis la garde réaliste
de `analyses/garde_ouverte_bagarreur.md` § 10 : poing droit au menton, coude bas contre les
côtes, poing gauche à hauteur de clavicule, talon arrière levé.

Demande de l'utilisateur : « Maintenant fais-lui donner un coup de poing ».

Animation : `anims/coup_de_poing_garde_bagarreur.json` (base `garde_ouverte_bagarreur`,
lacet +45), suivie de `garde_ouverte_idle_bagarreur`.

Cette fiche remplace l'ancienne (coup du coude levé). L'ancienne garde tenait le coude
arrière à l'horizontale sur le côté ; le coup ne faisait que ramener ce coude devant. La
nouvelle garde a le coude en bas et le poing au menton : le coup devient un **direct**, le
poing part en ligne droite du menton vers le menton adverse.

## 1. La logique du mouvement

C'est le coup sec du bagarreur : pas de recul, pas de pas, il frappe de là où il est. La
force vient du sol et de la rotation ; le bras n'est qu'un tuyau qui la transmet.

1. **Rien à armer, presque rien à prévenir.** Le poing est déjà au menton, chargé contre les
   côtes. Un vrai direct ne recule pas le poing (ça le télégraphie et ça ouvre le menton).
   L'anticipation, nécessaire pour que le départ se lise (bible A2), passe donc par le corps :
   il s'abaisse d'un rien (genoux), et le bassin et les épaules tournent de quelques degrés
   vers l'arrière. Le poing reste collé au menton.
2. **La jambe arrière pousse, la hanche part.** Le talon arrière est déjà levé : le poids est
   sur l'avant-pied. Le mollet et le quadriceps poussent, le genou arrière rentre vers
   l'avant et vers l'intérieur (rotation interne de hanche), le talon tourne vers l'extérieur.
   Le bassin tourne vers la cible **avant** les épaules ; le poids passe sur la jambe avant.
3. **Les épaules suivent, le poing part droit.** Quand le bassin est lancé, le tronc se
   détord et l'épaule droite avance. Le poing quitte le menton **en ligne droite** vers la
   cible : le coude ne s'écarte pas sur le côté (pas d'aile de poulet), il monte derrière le
   poing pour finir dans l'axe du bras. L'avant-bras tourne (pronation), le poing finit
   paume vers le bas.
4. **Le coude se tend en dernier.** Le triceps finit le travail : le bras est tendu (pas
   verrouillé) au contact, l'épaule droite devant, le bras dans le prolongement de la ligne
   des épaules.
5. **L'autre main ferme la porte.** Le poing gauche quitte la clavicule et **remonte à la
   joue gauche**, coude bas contre les côtes : quand le corps tourne, le côté gauche du
   visage devient le côté exposé. L'épaule gauche recule d'autant que la droite avance :
   c'est la même rotation.
6. **La tête reste derrière l'épaule.** Elle avance avec le corps, à niveau, le regard sur la
   cible ; le menton reste bas, abrité par l'épaule droite qui monte au contact. Le cou
   compense une partie de la rotation pour que le regard ne tourne pas avec les épaules.
7. **Retour par le même chemin.** Le poing revient au menton par la ligne d'aller, plus vite
   qu'un retour flottant : un bagarreur qui laisse traîner son bras se fait contrer.

## 2. Anatomie

| Partie | Articulations et axes | Muscles | Rôle |
|---|---|---|---|
| Jambe arrière (droite, N) | cheville : flexion plantaire qui s'accentue (pousse sur l'avant-pied) ; genou : légère flexion puis extension ; hanche : extension + **rotation interne** (genou qui rentre) | triceps sural, quadriceps, grand fessier, adducteurs | moteur : pousse le sol et lance la rotation du bassin |
| Jambe avant (gauche, F) | genou qui plie un peu plus ; hanche en rotation interne relative (le bassin tourne au-dessus) | quadriceps, moyen fessier | reçoit le poids, sert de pivot ; le genou absorbe |
| Bassin | rotation autour de la colonne (vers la cible), translation vers l'avant | fessiers, obliques | part **avant** les épaules |
| Tronc | détorsion (écart bassin-épaules qui se crée puis se referme) | obliques, grand dorsal | transmet la rotation au bras |
| Épaule droite (N) | flexion de 31° à ~104° ; adduction horizontale (le bras vient dans l'axe) ; rotation interne ; omoplate en protraction **sans** enrouler la ligne des épaules (règle 6) | deltoïde antérieur, grand pectoral, dentelé antérieur | pousse le bras vers la cible |
| Coude droit | extension de 127° à ~4° | triceps (anconé) | dernier segment de la chaîne |
| Avant-bras droit | pronation | rond pronateur, carré pronateur | poing paume vers le bas au contact |
| Épaule gauche (F) | flexion qui augmente un peu, rétraction de l'omoplate | rhomboïdes, trapèze moyen, deltoïde antérieur | recule avec la rotation, porte le poing à la joue |
| Coude gauche | flexion qui augmente (97° → ~135°) | biceps, brachial | poing à la joue |
| Cou | rotation inverse de celle des épaules, flexion stable | sterno-cléido-mastoïdien, splénius | tête à niveau, regard sur la cible |

D'où vient la force : sol → avant-pied arrière → genou et hanche arrière → bassin → tronc →
épaule droite → coude → poing. Chaque segment part quand le précédent est lancé.

## 3. Phases (60 images/s)

Bible § C, force 2 (direct) : anticipation 1-2 i24, trajet 0, contact tenu 1-2 i24, retour
2-4 i24, soit ×2,5 à 60 i/s, et ×1,5 sur l'anticipation et le retour pour un personnage lourd.
Le bagarreur est lourd mais le direct est son coup sec : on garde le bas de la fourchette.

| Images | Phase | Ce qui bouge |
|---|---|---|
| 0-4 | anticipation (4 i) | il se ramasse (y 87 → 86), bassin −12 → −15 et épaules −16 → −22 (torsion totale) vers l'arrière ; les poings ne bougent pas (poing N : 0,5 à 1,2 par image, entraîné par le buste) |
| 4-8 | poussée (4 i) | la jambe arrière pousse : `thighN_r` 0 → 6 (le genou rentre), le talon déjà levé ; le bassin part −15 → +6 ; les épaules restent à −18 (±4) : le tronc se tord ; les poings restent au menton et à la clavicule |
| 8-12 | trajet (4 i) | les épaules partent (−18 → 0 → 22 → 38 → 47), un temps après le bassin ; le poing N quitte le menton à 9 et file en ligne : écarts 5,2 / 10,0 / 13,4 / 18,4 (croissants, A bis 4) ; le coude 127 → 120 → 102 → 86 → 12, toujours en baisse (A bis 12) ; le poing F monte à la joue à 10 |
| 12 | contact | bras N tendu dans la ligne des épaules, poing au niveau du menton adverse, l'épaule N monte (−1) et abrite le menton |
| 12-15 | dépassement | le corps continue de 4° (torsion totale 47 → 51), le poing reste en place (écarts < 0,5) : le dépassement passe par le tronc, pas par le bras |
| 15-21 | tenue (6 i) | le coup reste lisible, léger retour du tronc (51 → 48) |
| 21-27 | retour du bras | le coude replie (12 → 96) par la même ligne ; le poing F redescend à la clavicule pendant que le poing N est encore loin du visage |
| 27-32 | retour au menton | coude 96 → 126, bassin et épaules reviennent (16 → −10) |
| 32-40 | retour en garde | derniers degrés de bassin et de torsion jusqu'à la garde exacte, `suivante` : idle de garde |

## 4. Poses clés, tous les axes

Lacet de l'animation : +45. Valeurs des canaux de l'animation ; ce qui n'est pas cité vient de
la garde (`poses/garde_ouverte_bagarreur.json`). Le cou compense une partie de la rotation :
`neck_r` = −0,6 × (torsionBassin + torsion + 16) sur chaque clé, le regard reste sur la cible.

**Image 0 (garde).** Voir la fiche de garde § 10. Poing N au menton (coude 127, bras 31,
plan +15, rotation +4), poing F à la clavicule (coude 97, bras 32, plan −18).

**Image 4 (ramassé).**
- Pieds et chevilles : inchangés, talon N levé ; genoux 14 / 30 (plient un peu).
- Bassin : y 86, x −0,5, torsionBassin −15 (recule de 3°).
- Buste : torsion −7, total −22 ; buste droit (spineLow 4, chest 4).
- Épaules : garde, `epaule*_av` ≤ 0.
- Bras : garde ; les poings suivent le buste.
- Tête : neck_r +3,6, regard sur la cible.

**Image 8 (poussée, le bassin a pris de l'avance).**
- Hanche N : flexion de garde (thighN −26), écartement de garde (plan +15), **rotation
  interne +6** (genou qui rentre), cheville tenue au sol par la cible de jambe (-36,7 ; 14,9) au lacet 45.
- Genou N 24 (s'ouvre pour pousser), cheville en flexion plantaire (talon levé).
- Jambe F : appui, genou 29, pied à plat.
- Bassin : torsionBassin +6, x 1,5, y 86,3.
- Buste : torsion −24, total −18 : les épaules n'ont pas encore bougé (écart de 4° avec
  l'image 4).
- Bras : garde. Tête : neck_r +1,2.

**Image 10 (trajet, mi-course).**
- Hanche N : rotation interne +9 ; bassin +12 ; buste torsion +10, total +22.
- Épaule N : élévation 38, plan +32 (le bras passe devant), rotation −20 (pronation en
  cours) ; omoplate en protraction mais `epauleN_av` = 0.
- Coude N : 102. Poing N à mi-chemin, sur la droite menton → cible.
- Épaule F : élévation 26, plan −12, rotation −10, `epauleF_av` −2 (elle recule) ; coude F
  144 : poing gauche à la joue.
- Tête : neck_r −22,8.

**Image 11.**
- Bassin +14, torsion +24, total +38.
- Bras N : élévation 48, plan +44, rotation −10, coude 86 ; `epauleN_haut` −2.
- Bras F : joue ; `epauleF_av` −2,5. Tête : neck_r −32,4.

**Image 12 (contact).**
- Jambe N : rotation interne +10, genou 17 (tendue sans verrouiller), talon levé ;
  cheville en place.
- Jambe F : genou 32, elle reçoit le poids ; bassin x 4, y 86.
- Bassin +15, buste torsion +32, total +47 ; buste droit.
- Épaule N : élévation 101 (bras à hauteur d'épaule, un peu au-dessus), plan +52 (dans
  l'axe de la cible), rotation +40 (poing paume en bas), `epauleN_haut` −1 (l'épaule
  monte contre le menton), `epauleN_av` 0.
- Coude N : 12 (tendu, pas verrouillé).
- Épaule F : élévation 26, plan −12, rotation −10, `epauleF_av` −3 ; coude F 144, poing F
  contre la joue gauche.
- Tête : neck_r −37,8 : à niveau (y 152), derrière l'épaule N.

**Image 15 (dépassement).** Bassin +16, torsion +35, bras N plan +56, bras F plan −8. Le reste
comme 12.

**Image 21 (fin de tenue).** Bassin +15, torsion +33, `epauleN_haut` −1,5 ; bras comme 12.

**Image 27 (retour).**
- Bassin +6, torsion +10, thighN_r +5 ; x 2,5, y 86,3.
- Bras N : élévation 47, plan +28, rotation −10, coude 96 (le poing revient par la ligne).
- Bras F : garde (coude 97) : le poing gauche est redescendu à la clavicule.
- `epauleF_av` −2. Tête : neck_r −19,2.

**Image 32 (poing au menton).**
- Bassin −6, torsion −4, thighN_r 0 ; x 1, y 86,6.
- Bras N : élévation 32, plan +16, rotation 0, coude 126 : poing au menton.
- Bras F : garde. Tête : neck_r −3,6.

**Image 40 : garde exacte.**

## 5. Ce qui se voit

- **Trois quarts (lacet 45, la vue du jeu).** Le poing part du menton et grandit vers la
  caméra en ligne ; la rotation se lit par le bassin qui tourne d'abord (image 8 : la ceinture
  tourne, les épaules non), puis par les épaules. Le poing gauche qui monte à la joue se voit
  au-dessus de l'épaule gauche.
- **Profil (lacet 90).** Le poing traverse l'écran à hauteur du menton, en ligne horizontale ;
  le bras tendu au contact prolonge la ligne des épaules ; la tête reste derrière. Le genou
  arrière qui rentre se lit par la cuisse qui pivote.
- **Face (lacet 0).** Le poing vient vers la caméra : on vérifie qu'il n'y a pas d'aile de
  poulet (coude dans l'axe, pas écarté sur le côté) et que la main gauche est bien à la joue,
  pas devant le visage.
- **Limite du rig.** Les chevilles sont tenues (cible de jambe) dans le plan de la vue du jeu
  (lacet 45). Dans les autres vues, la torsion du bassin fait pivoter les jambes autour de la
  colonne et la cheville arrière se décale (jusqu'à 15 au lacet 90). C'est un effet de caméra
  sur la rotation du bassin ; dans la vue du jeu, le pied ne glisse pas.

## 6. Références

- Fiche de garde : `analyses/garde_ouverte_bagarreur.md` § 10 (garde réaliste, poing au
  menton, coude bas, talon arrière levé).
- `analyses/coup_de_poing_rue.md` : même chaîne hanche → épaules → coude en dernier.
- Vidéo 1 (`etudes/01_strength_vs_speed/03_lancers_176_257.md`, V1 173-187) : coup depuis
  la garde, contact aligné épaule-poing, tenue lisible.
- Bible :
  - A bis 1 : la jambe arrière pousse, talon levé ;
  - A bis 3 : bassin une image avant l'épaule, épaule avant le poing (images 8, 9, 10) ;
  - A bis 4 : écarts du poing croissants jusqu'au contact ;
  - A bis 5 : trajet en 3 images (9-12) à 60 i/s ;
  - A bis 7 : dépassement puis tenue (12-15-21) ;
  - A bis 12 : le coude ne fait que se déplier jusqu'au contact ;
  - § C force 2 : durées.

## 7. Contrôles

Mesures au lacet total 0 sauf mention.

1. Coude N : 127 (0-8), puis 120, 102, 86, 12 (images 9-12), sans jamais remonter avant le
   contact.
2. Bassin avant épaules : à l'image 8, torsionBassin a déjà avancé de 21° quand la torsion
   totale n'a bougé que de 4° (−22 → −18). Les épaules partent à 9.
3. Poing N, écarts 3D par image entre 8 et 12 : 5,2 / 10,0 / 13,4 / 18,4, strictement
   croissants. Le poing ne recule pas pendant l'anticipation (déplacement < 1,5 par image).
4. Contact : poing N vers (72, 138, z −1) : |z| < 5, sur la ligne de frappe ; hauteur entre le
   menton et le centre de la tête (152) ; tête à niveau (y 152, ±1 sur tout le coup).
5. Poing F à la joue de 10 à 21 : vers (20, 131, z 13), au-dessus de la clavicule et sur le
   côté du visage, hors de la tête.
6. Rien ne traverse (`--verifier`) : aucune alerte « … qui se traversent » ni « … dans … ».
   Alertes admises (aucune n'est une traversée) : « bras proche confondu avec le corps » et
   « bras proche peu visible » en garde (0-9, 29-40), admises par la fiche de garde
   § 10, contrôle 9.
7. Chevilles, vue du jeu (lacet 45) : N à (−36,6 ±0,7 ; 15), F à (20,1 ; 8,6) sur tout le
   coup. Aucun point sous le sol (point le plus bas ≥ 6,9).
8. Stature : `epaule*_av` ≤ 0 tout du long, buste droit (spineLow et chest de la garde).
9. Images 0 et 40 identiques à la garde (raccord avec `garde_ouverte_idle_bagarreur`).
