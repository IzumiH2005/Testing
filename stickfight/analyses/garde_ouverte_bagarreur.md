# Analyse : garde ouverte du bagarreur

Cette garde remplace, pour le bagarreur seul, la garde ouverte commune (`analyses/gardes.md`) :
INVENTAIRE § 3 et § 4, « sa garde ouverte et son repos ».

- Fichiers : `poses/garde_ouverte_bagarreur.json` (la pose) et
  `anims/garde_ouverte_idle_bagarreur.json` (la boucle).
- La garde commune et les animations qui en partent ne changent pas.

**Garde de droitier, vue de trois quarts face.** Le personnage regarde vers la droite.

- Le côté gauche est devant : jambe gauche et poing gauche. Dans le rig, c'est F, le côté loin
  de la caméra.
- Le côté droit est derrière : jambe droite et bras droit au coude levé. Dans le rig, c'est N,
  le côté proche, côté caméra.
- La poitrine est tournée vers la caméra.
- Voir § 9 pour la révision qui a fixé cette lecture.

Demandes de l'utilisateur :

- « c'est un combattant de rue, donc sa garde ouverte ne doit pas être trop scolaire, et ses
  jambes ne doivent pas être trop écartées » ;
- « le pied en arrière peut être tourné légèrement vers l'écran (le genou et la jambe) au lieu
  que ce soit juste le talon qui touche le sol » : la jambe arrière est tournée, le genou et le
  tibia se voient (§ 3) ;
- sur le rendu de cette pose : « cette pose et cet angle de vue, je le trouve parfait ».
  - Le dessin ne change pas.
  - Il était d'abord décrit à lacet −45 (trois quarts dos). L'utilisateur a ensuite demandé
    « la pose ne doit plus être de dos » : la même image est maintenant décrite à lacet +45,
    trois quarts face (§ 9).

## 1. Intention

> Remplacé par le § 10 (garde réaliste) pour la position des bras, des jambes et la hauteur du bassin.

La garde commune est une garde de boxe d'école. Elle dit « boxeur appliqué » :

- fente longue : 72 entre les chevilles de profil ;
- bassin très bas : 72 ;
- buste penché, menton rentré ;
- deux poings serrés au menton.

Le bagarreur n'a pas appris en salle. Sa garde dit « vas-y, approche ».

- **Debout, plus haut qu'un boxeur** : bassin à 84 (garde commune 72, repos 87,8). Il ne
  s'accroupit pas, il est sûr de lui. Règle 6 : buste droit, poitrine ouverte, épaules en
  arrière.
- **Appuis courts** : un petit pas de marche (52 entre les chevilles de profil), pas une
  fente. Il peut avancer ou cogner sans se replacer : dans la rue, on ne garde pas une
  distance de ring.
- **Plus de face** : bassin tourné de 12°, épaules de 16°. La poitrine se montre, et à lacet
  +45 elle est tournée vers la caméra.
- **Mains dépareillées, poings fermés.** C'est la garde du costaud de la bible (§ 3 « Les
  bras » : « un poing collé sous le menton et l'autre bras en équerre »), rendue moins
  appliquée :
  - le poing avant (gauche, F) est bas et long, à hauteur du sternum, avant-bras presque
    horizontal, coude ouvert. Il tient la distance, il peut repousser, attraper ou partir en
    direct ;
  - le bras arrière (droit, N) a le coude levé sur le côté (§ 8). Il est armé pour le coup
    court ;
  - il y a un trou au milieu, ce n'est pas un mur : c'est ce qui fait « bagarreur » et non
    « boxeur ».
- **Menton horizontal**, pas rentré : il regarde l'adversaire droit dans les yeux.

Ce qui reste de la logique d'une garde (`gardes.md` § 1) :

- stable : base en longueur (52) et en largeur (27 de face), genoux souples ;
- prêt à partir : talon arrière levé, mollet arrière chargé ;
- la main avant est entre lui et l'adversaire, le bras arrière est armé.

On garde ces trois fonctions, avec moins de technique et plus d'attitude.

## 2. Anatomie

> Remplacé par le § 10 (garde réaliste) pour la position des bras, des jambes et la hauteur du bassin.

Flexions données dans les unités du rig : `shin*` est la flexion du genou par rapport à la
cuisse (0 = jambe tendue), `fore*` celle du coude par rapport au bras (0 = bras tendu).

| Partie | Ce qui travaille | Pourquoi |
|---|---|---|
| Pied avant (gauche, F) | à plat, cheville presque neutre (`footF` 5,5), pointe vers l'adversaire | il porte un peu plus de la moitié du poids |
| Pied arrière (droit, N) | sur l'avant-pied, cheville en flexion plantaire (`footN` 10), talon 5,3 au-dessus du talon avant ; mollet (triceps sural) en tension | la poussée vers l'avant part de là |
| Genou avant | fléchi de 38° (quadriceps en tenue légère) | genou souple, au-dessus de la cheville, pas devant la pointe |
| Genou arrière | fléchi de 25° | jambe arrière en ressort, ni tendue ni accroupie |
| Hanche avant (F) | flexion 27,6°, écartement 12°, rotation 5 (pointe vers la cible) | le pas avant |
| Hanche arrière (N) | extension de 11° (cuisse qui part en arrière), écartement 15°, rotation −15 (genou et tibia tournés, visibles à l'écran) | le pas arrière, court ; la jambe arrière tournée, le pied n'est pas qu'un talon posé |
| Bassin | tourné de 12° (hanche avant devant), presque pas de bascule (`root` −2) | plus de face qu'un boxeur, le poids au milieu |
| Tronc | droit (`spineLow` 4, `chest` 4), torsion 4 en plus du bassin : épaules à 16° | stature droite (règle 6) |
| Omoplates | rapprochées (`epauleF_av` −1, `epauleN_av` 0) ; épaule avant haussée de 1, épaule du bras levé baissée de 3 | poitrine ouverte, pas recroquevillée |
| Cou | fléchi de 3 seulement | menton horizontal, regard droit |
| Bras avant (gauche, F) | deltoïde antérieur et biceps en tenue : bras levé de 31° devant, écarté de 40°, rotation 40° ; coude fléchi de 95° | poing devant le sternum, à 37 devant l'épaule, coude sorti de la silhouette ; bras plié, pas tendu |
| Bras arrière (droit, N) | deltoïde moyen : bras écarté de 80° sur le côté (`armN_p` 80), presque pas d'élévation devant (`armN` −5), rotation 20 ; coude fléchi de 100° | coude levé sur le côté à hauteur d'épaule, avant-bras qui tombe vers le bas-avant (§ 8) |

## 3. La pose, articulation par articulation

> Les valeurs de ce paragraphe et du § 8 sont remplacées par le § 10 (garde réaliste).

**Repère du rig**

- Torsions : `torsion` et `torsionBassin` positifs = le côté proche (N) vient vers l'avant.
  Ici le côté gauche (F) est devant, donc les deux sont négatifs.
- Écartement : `*N_p` positif et `*F_p` négatif écartent du corps. `_p` positif = vers la
  caméra.
- Le bras avant se lève dans le plan **devant**, vers l'adversaire, ouvert sur le côté. Le bras
  arrière se lève **sur le côté**.

| Articulation | Axes | Valeurs |
|---|---|---|
| Corps entier | orientation à l'écran (`lacet`) | +45 : trois quarts face |
| Bassin | hauteur, bascule (`root`), rotation (`torsionBassin`) | y 84, `root` −2, `torsionBassin` −12 |
| Colonne | `spineLow`, `chest`, torsion | 4, 4, `torsion` −4 |
| Omoplate F (avant) | avant, haut | `epauleF_av` −1, `epauleF_haut` 1 |
| Omoplate N (arrière) | avant, haut | `epauleN_av` 0, `epauleN_haut` −3 |
| Cou | flexion, rotation | `neck` 3, `neck_r` 0 |
| Épaule F (avant) | élévation (plan devant), écartement, rotation | `armF` 31,46, `armF_p` −40, `armF_r` −40 |
| Coude F | flexion | `foreF` 95,21 |
| Épaule N (arrière) | élévation, écartement, rotation | `armN` −5, `armN_p` 80, `armN_r` 20 |
| Coude N | flexion | `foreN` 100 |
| Hanche F (avant) | flexion, écartement, rotation | `thighF` 26, `thighF_p` −15, `thighF_r` 5 |
| Genou F | flexion | `shinF` 35,95 |
| Cheville F | flexion | `footF` 5,48 : pied à plat |
| Hanche N (arrière) | flexion, écartement, rotation | `thighN` −11,1 (extension), `thighN_p` 15, `thighN_r` −15 |
| Genou N | flexion | `shinN` 33,12 |
| Cheville N | flexion | `footN` 10 : flexion plantaire, talon levé |

**Positions qui en résultent, sans le lacet** (plan de profil, bassin au sol, x vers
l'adversaire)

- Bassin (0 ; 84), épaule (3,2 ; 129,9), tête (6,2 ; 149,8).
- Poing F (avant) : (40 ; 108), soit 37 devant l'épaule et 22 sous elle. Le bras avant est
  plié (coude 95), il ne pointe pas comme un direct.
- Bras N (arrière) : coude levé sur le côté, à hauteur d'épaule ; le poing est près de
  l'épaule, devant elle.
- Genou F (20,4 ; 49,1), au-dessus de la cheville F (16 ; 8,1).
- Genou N (−8,3 ; 44,8), au-dessus et en avant de la cheville N (−35,9 ; 13,3) ; pointe N
  (−28,5 ; 8,7).
- 52 entre les chevilles ; point le plus bas 0,52.

**Repères de la bible** (§ 3 « Penché, large, bas », H ≈ 173)

- Le rapide a 0,47 H entre les pieds, le costaud 0,72 H.
- Le bagarreur est à 0,30 H, à la demande de l'utilisateur.
- La stabilité vient de la largeur de face et des genoux souples, pas de la longueur.

### Ce qui se lit dans chaque vue

Le `lacet` de la pose s'ajoute à celui de la vue. On juge la pose à lacet total 90 (face),
45 (vue de jeu, celle de la pose seule) et 0 (vrai profil).

- `--vues` ajoute +90, +45 et +0 au lacet de la pose : avec la pose à +45, ses trois lignes
  montrent 135, 90 et 45.
- Le vrai profil se rend avec `tools/rendu.sh … --set lacet=0`.

- **Face** (90) :
  - les deux coudes sortent de la silhouette du tronc ;
  - les cuisses s'écartent (`thigh*_p` ±15) et ne se recouvrent pas ;
  - le coude droit levé est sur le côté ; le poing gauche est devant, plus bas, devant le
    sternum.
- **Vrai profil** (0) : debout, petit pas, buste vertical ; poing avant devant le sternum,
  coude arrière levé.
- **Vue de jeu** (+45, trois quarts face) :
  - la poitrine vient vers la caméra ;
  - le bras droit, au coude levé, fait une barre vers l'arrière à hauteur d'épaule, côté
    caméra ;
  - la jambe arrière est tournée : le genou et le tibia se voient, pas seulement le talon ;
  - la silhouette dit « approche ».
  - Le bras avant (gauche, F) part vers l'adversaire, côté loin de la caméra. À l'écran, il
    ne montre que 54 % de sa longueur (alerte du vérificateur « bras loin raccourci »).
    C'est l'effet de l'angle, pas un bras caché : le poing reste devant le tronc. Cette alerte
    est acceptée à cet angle.

## 4. La boucle `garde_ouverte_idle_bagarreur` (96 i)

> Les déplacements du bassin (`x`, `y`) des clés 38 à 74 sont remplacés par le § 10 (balancement asymétrique).

A8 : une pose tenue reste vivante, sans le sautillement du boxeur. Le bagarreur se balance
d'avant en arrière sur ses appuis plantés.

| Image | Ce qui se passe | Amplitudes (en plus de la pose) |
|---|---|---|
| 0 | pose de base | — |
| 10 | la main avant « appelle » (vite) : l'avant-bras se déplie, le poids part devant | x +2,2, y −1,2, torsion −2,5, `armF` +4, `foreF` −22 |
| 26 | poids devant, la main revient lentement | x +3,5, y −0,6, torsion −5, `armF` +1, `foreF` −4 |
| 38 | passage, il expire | x +0,5, y −2,2, torsion −1, `chest` +0,8 |
| 50 | poids derrière, il inspire, les épaules montent | x −3,5, y −0,6, torsion +5, `epaule*_haut` +1,5, `chest` −0,6 |
| 62 | le menton monte : il toise l'adversaire | x −3, y −0,8, torsion +4, `neck` −5, `epaule*_haut` +0,8 |
| 74 | passage, le menton redescend | x −0,5, y −2,2, torsion +1, `neck` −1, `chest` +0,5 |
| 86 | retour | x +1, y −0,6, torsion −0,5 |
| 96 | = image 0 | — |

Les torsions sont négatives quand l'épaule avant (F) avance.

- **Transfert de poids** : bassin ±3,5 en x, −2,2 en y aux passages ; il se lit à l'écran.
- **Torsion des épaules** : ±5, en retard sur le bassin (décalage 3 images).
- **Chevauchement** : le bassin part d'abord, puis la torsion et le thorax (3 images), le bras
  F (6-7), le bras N (7-8) et le cou (5).
- **L'appel de la main** : le coude F s'ouvre jusqu'à 82° vers l'image 26. Le bras montre alors
  au plus 80 % de sa longueur de profil ; il ne devient jamais un bras tendu.
- **Ancre** : les chevilles restent plantées. Seul le bassin bouge, les jambes se replient.
- **Pieds** : ils gardent les angles de la pose (`pieds_auto` false).
  - Le calcul automatique des pieds raisonne dans le plan de profil et ne tient pas compte du
    `lacet` de la pose.
  - Il faisait passer les pointes sous le sol.
- **Boucle fermée** : l'image 0 est égale à la dernière.

## 5. Raccords

Les transitions communes (`mise_en_garde`, `garde_fermer`, `garde_ouvrir`, `sortie_de_garde`,
`marche_avant`…) partent de la garde commune et y arrivent.

- Pour le bagarreur, il faudra les remplacer ou les adapter, en tenant compte du `lacet` +45 de
  cette garde.
- Ce sera une étape à part.

## 6. Règles et références

- `BIBLE_ANIMATION.md` :
  - A6, une pose = une idée lisible en silhouette : « approche » ;
  - A8, rien ne s'arrête tout à fait : d'où la boucle ;
  - § 3 « Les bras » : garde du costaud, un bras en avant, l'autre armé ;
  - § 3 « Penché, large, bas » et § 12 : posture du costaud presque verticale, ici aussi ;
  - V1 (`etudes/01_strength_vs_speed/`, 136-152) : le costaud en garde, buste droit.
- `CLAUDE.md` du projet, règle 6 : buste droit, `epaule*_av` ≤ 0, ici −1 et 0.
- Règle 5 : les poings ne touchent ni la tête ni le tronc ; le bras avant ne croise pas l'autre
  bras.

## 7. Contrôles chiffrés

1. Chevilles (sans lacet) :
   - 45 à 55 d'écart en x ;
   - talon arrière 3 à 7 au-dessus du talon avant ;
   - point le plus bas entre −0,5 et 1.
2. De face : chevilles écartées d'au moins 20 ; cuisses qui ne se recouvrent pas.
3. Bassin entre 82 et 86 ; épaule entre 127 et 132.
4. Buste : `root` + `spineLow` + `chest` ≤ 8 vers l'avant ; `epaule*_av` ≤ 0.
5. De face : chaque coude à plus de 15 de l'axe du tronc.
6. Genou arrière au-dessus de la cheville arrière ; `footN` > 0 (talon levé) ;
   `thighN_r` = −15 (jambe arrière tournée).
7. Bras avant de profil : ≤ 75 % de sa longueur dans la pose, ≤ 80 % pendant l'appel.
8. Boucle : bassin d'au moins ±3 en x, torsion d'au moins ±4.
9. `--verifier` sur la boucle :
   - aucune traversée, aucun pied qui glisse, rien sous le sol, la boucle fermée ;
   - seule alerte admise, à cet angle : « bras loin raccourci » (§ 3).
10. `lacet` > 0 : le bagarreur ne se tient jamais de dos.

## 8. Révision : coude arrière levé sur le côté

D'après `etudes/postures_trois_quarts/rapport.md` § 2.2 (V1 100 et 120, R2 1456), le bras
arrière (droit, N) passe en coude levé sur le côté.

| Réglage | Valeur | Effet |
|---|---|---|
| `armN` | −5 | |
| `armN_p` | 80 | abduction d'environ 80° |
| `armN_r` | 20 | avant-bras qui tombe vers le bas-avant |
| `foreN` | 100 | |

- À lacet +45, le bras haut fait une barre vers l'arrière à hauteur d'épaule, côté caméra, et
  le poing sort de la tête.
- Le bras avant ne change pas.
- L'épaule du bras levé (droite, N) est un peu baissée (`epauleN_haut` −3), à la demande de
  l'utilisateur. C'est le bras le plus proche de la caméra.
- Le vérificateur ne relève aucune traversée sur l'idle.
- Le bras avant raccourci (< 55 %) est voulu : le trois quarts se lit par un bras court et un
  bras à plat (rapport § 2.1).

## 9. Révision : la pose ne doit plus être de dos

**Ce qui n'allait pas**

La pose était décrite à lacet −45 (trois quarts dos), avec le côté droit devant, poing droit
et jambe droite. Le bras de frappe au coude levé était donc le bras gauche, côté loin de la
caméra.

L'utilisateur a relevé l'incohérence : le corps et les jambes se lisaient comme un personnage
vu de dos, et le coup partait derrière le corps. Sa demande : « la pose ne doit plus être de
dos ».

**Ce qui a été fait : un miroir à travers le plan de l'écran** (z → −z)

- Les réglages N et F sont échangés (bras, jambes, omoplates, `_p`, `_r`).
- Changent de signe : chaque profondeur (`_p`), chaque rotation (`_r`), `torsion`,
  `torsionBassin`, `neck_r` et `lacet` (−45 → +45).
- Les angles dans le plan (élévation, coudes, genoux, chevilles) et les déplacements des
  omoplates ne changent pas.
- Le même miroir est appliqué à la boucle (`plus`, `decalage`) et au coup de poing (`fixe`,
  `vise legF` → `vise legN`).

**Résultat**

- Le dessin est **identique** : rendu de la pose identique au pixel près. Toutes les images de
  la boucle et du coup sont identiques au trait près : les écarts de gris restent sous 60, ce
  n'est que l'anticrénelage.
- Ce que l'utilisateur avait validé à l'œil ne bouge donc pas. Ce qui change, c'est ce que le
  dessin représente :
  - un droitier vu de trois quarts face, poitrine vers la caméra ;
  - jambe gauche et poing gauche devant ;
  - bras droit au coude levé, côté caméra.
- Le coup de poing part du bras droit et passe devant le corps.
- Le vérificateur ne relève toujours aucune traversée.
  - Son contrôle « peu visible » ne mesure que le bras proche (N).
  - Avant le miroir, il portait sur le poing de garde au menton : alerte aux images 12-26 du
    coup.
  - Il porte maintenant sur le bras de frappe : images 9-10 et 30-40 (fiche coup § 7.6).
  - Le poing de garde, passé côté loin, n'est plus mesuré.

## 10. Révision : garde réaliste réglée sur le mannequin 3D

**Ce qui n'allait pas**

Posé sur le mannequin 3D (`tools/mannequin.py`, corps MakeHuman CC0 sous le stickman), la
garde du § 8 ne tenait pas debout :
- le coude arrière levé à l'horizontale, sur le côté, n'est pas une garde : il ouvre les
  côtes et le menton, et aucun boxeur ni bagarreur ne le tient ;
- le bras avant, très ouvert (`armF_p` −40, `armF_r` −40), mettait le coude dehors ;
- jambe arrière : le genou fléchi à 33° avec un pied presque à plat donnait une cheville
  cassée, et le talon arrière ne se lisait pas.

L'utilisateur a corrigé la pose sur le mannequin, vue par vue, jusqu'à la juger
satisfaisante, puis demandé de la reporter sur le stick et de l'animer.

**La garde**

Le principe est celui d'une garde de rue réelle : les coudes protègent les côtes, les poings
protègent le visage, rien ne pend.
- Poing arrière (N, droit, côté caméra) **au menton**, coude bas contre les côtes, sous
  l'épaule. C'est le bras qui frappe : il part de là, chargé, sans rien à remonter.
- Poing avant (F, gauche) **à hauteur de clavicule**, devant, coude bas et dans l'axe, bras
  plié à 97°. C'est le bras qui mesure la distance et appelle l'adversaire (§ 4).
- Jambe arrière presque tendue, tibia incliné vers l'avant (30°), talon levé : le poids est
  sur l'avant-pied arrière, prêt à pousser.
- Jambe avant plus droite qu'au § 3 (genou 22° au lieu de 36°). Le bassin remonte de 3.
  Sinon la pointe arrière ne touche pas le sol.

**Réglages**

| Articulation | Axes | Avant (§ 3 et 8) | Après |
|---|---|---|---|
| Bassin | hauteur | y 84 | **y 87** |
| Épaule N (arrière) | élévation, écartement, rotation | −5, 80, 20 | **31,3, 14,6, 3,7** |
| Coude N | flexion | 100 | **127,2** |
| Épaule F (avant) | élévation, écartement, rotation | 31,46, −40, −40 | **32, −17,5, −9,7** |
| Coude F | flexion | 95,21 | **96,9** |
| Hanche N | flexion, rotation | −11,1, −15 | **−26, −2** |
| Genou N | flexion | 33,12 | **4** |
| Cheville N | flexion | 10 | **−16** (pied raide, voir plus bas) |
| Hanche F | flexion | 26 | **14** |
| Genou F | flexion | 35,95 | **22** |
| Cheville F | flexion | 5,48 | **5,5** |

Inchangés : torsions (−4, −12), `lacet` +45, buste (`root` −2, `spineLow` 4, `chest` 4),
`neck` 3, omoplates (`epauleN_haut` −3, `epauleF_av` −1), écartement des hanches (±15),
`thighF_r` 5.

**Pourquoi `footN` est négatif alors que le talon est levé**

`footN` est l'angle du pied par rapport au tibia. Le tibia arrière est incliné de 30° vers
l'avant ; avec `footN` −16 le pied plonge de 43° vers la pointe. La cheville est en flexion
plantaire (angle tibia-pied d'environ 106°). Le talon est à 6,6 au-dessus du sol et la
pointe au sol. Sur le mannequin, les orteils se cassent à plat au sol (articulation
métatarso-phalangienne), comme un vrai pied en appui sur l'avant-pied.

`thighN_r` passe de −15 à −2 : la rotation externe de la jambe arrière mettait le genou en
dedans du pied sur le mannequin. Pied et genou sont maintenant dans le même axe.

**Anatomie de la nouvelle garde**

| Partie | Articulations et axes | Muscles qui tiennent la pose |
|---|---|---|
| Bras N (arrière) | épaule fléchie de 31°, ramenée en adduction (écartement 14,6), rotation 3,7 ; coude fléchi à 127 | grand pectoral et grand dorsal serrent le coude contre les côtes ; deltoïde antérieur porte le bras ; biceps et brachial tiennent le coude plié, poing au menton |
| Bras F (avant) | épaule fléchie de 32° dans le plan devant, peu écartée (−17,5), rotation −9,7 ; coude à 97 | deltoïde antérieur et grand pectoral (faisceau claviculaire) portent le bras devant ; biceps et brachial tiennent le coude ; bras souple, prêt à appeler |
| Jambe N (arrière) | hanche en extension (−26), rotation −2 ; genou presque tendu (4) ; cheville en flexion plantaire (~106°) | triceps sural chargé : le poids passe par l'avant-pied ; quadriceps tient le genou ; c'est elle qui pousse le corps vers l'avant au départ d'un coup |
| Jambe F (avant) | hanche fléchie de 14, écartée (−15), rotation 5 ; genou à 22 ; pied à plat | quadriceps et fessiers portent l'essentiel du poids ; le genou souple absorbe le balancement |
| Buste | droit, poitrine légèrement bombée (règle 6) | érecteurs du rachis ; omoplates basses (trapèze inférieur) |

D'où part la force : la jambe arrière pousse sur l'avant-pied, la hanche tourne, le buste
suit ; le poing arrière, déjà au menton et chargé contre les côtes, n'a rien à remonter.

**Positions qui en résultent, sans le lacet**

- Bassin (0 ; 87), épaules (2,9 ; 129,9) et (2,3 ; 134), tête (6,2 ; 152,8).
- Bas du cercle de tête vers y 133 : le menton du stick est à la hauteur des épaules.
- Poing N (30,4 ; 127,5) : collé sous le menton. Coude N (14 ; 100,1) : 30 sous l'épaule.
- Poing F (43,2 ; 120,3) : devant, à hauteur de clavicule, 13 sous la tête. Coude F
  (18,8 ; 104,8). C'est fidèle au mannequin validé : sur lui, le cercle de tête du stick
  couvre tête et cou.
- Genou N (−17,9 ; 50,8) : au-dessus et en avant de la cheville N. Genou F (12,9 ; 49).
- Cheville N (−38,9 ; 14,9), pointe N (−32 ; 8,1). Cheville F (10,3 ; 8,2), pointe F (20,2 ; 8,5).
- 49 entre les chevilles. Point le plus bas 0,62.
- De face (lacet 90) : chevilles à 31 l'une de l'autre ; coudes à 12 (N) et 6 (F) de l'axe
  du tronc.

**Ce qui se lit dans chaque vue**

- Face : avant-bras arrière vertical, avant-bras avant incliné vers l'axe, devant le haut du tronc, poings sous le menton, coudes
  serrés. Les pieds sont écartés.
- Trois quarts (+45) : le poing arrière collé sous le menton, côté caméra ; le bras avant
  sort devant, plié, poing à hauteur de clavicule. Jambe avant fléchie, jambe arrière longue, talon levé.
- Profil : le bras avant montre l'avant-bras qui monte vers la clavicule ; le bras arrière est
  court, collé au corps. Il est voulu (voir les contrôles).

**La boucle**

Elle garde le § 4 : balancement avant-arrière sur appuis plantés, main avant qui appelle,
menton qui monte. Les jambes se replient seules (`ancre`) pour garder les chevilles.

Le balancement devient **asymétrique**, surtout vers l'avant. Avec une jambe arrière presque
tendue, reculer le bassin raccourcit la distance hanche-cheville arrière et l'ancre replie le
genou : à x −3,5 il revenait à 30°, la jambe cassée que la révision corrige. Le recul se lit
donc par la torsion (+5, +4), les épaules qui montent et le menton, pas par le bassin.

| Clé | `x` | `y` |
|---|---|---|
| 10 | +2,2 | −1,2 |
| 26 | +3,5 | −0,6 |
| 38 | +0,5 | −1 (au lieu de −2,2) |
| 50 | −0,8 (au lieu de −3,5) | 0 (au lieu de −0,6) |
| 62 | −0,6 (au lieu de −3) | −0,2 (au lieu de −0,8) |
| 74 | 0 (au lieu de −0,5) | −1 (au lieu de −2,2) |
| 86 | +1 | −0,6 |

Genou arrière entre 5 et 18 sur toutes les clés. Point le plus bas entre −0,5 et 0,6.

**Coup de poing**

`coup_de_poing_garde_bagarreur` est écrit en valeurs absolues sur l'ancienne garde (coude
levé, y 84). Il n'est plus raccord. Il sera repris dans sa propre fiche, avec un armé qui
part du poing au menton.

**Contrôles du § 7 remplacés**

- 3. Bassin entre 85 et 89 ; épaule entre 128 et 135. Poing N ≥ 126 (sous le menton) ;
  poing F entre 118 et 123 (clavicule).
- 6 bis. Genou arrière ≤ 18 sur toute la boucle.
- 8. Boucle : bassin d'au moins +3 vers l'avant et −0,5 vers l'arrière en x ; torsion
  d'au moins ±4.
- 5. De face : coudes entre 4 et 18 de l'axe du tronc (serrés, mais pas dedans) ; aucune
  traversée bras-tronc au vérificateur.
- 6. Genou arrière au-dessus et en avant de la cheville arrière ; talon arrière 4 à 9
  au-dessus du sol, pointe au sol ; `thighN_r` entre −5 et 0.
- 9. Alertes admises sur la boucle :
  - « bras loin raccourci » (§ 3) ;
  - « bras proche confondu avec le corps » et « bras proche peu visible ». Le bras arrière
    est replié contre les côtes, poing au menton, côté caméra : il passe devant le tronc à
    toutes les vues. C'est la garde demandée. Contrôle : le poing N reste visible en bosse
    sous le menton à toutes les images (l'avant-bras ne peut pas se détacher d'une silhouette
    pleine à cet angle).
  - « epauleN_haut hors amplitude » : −3 est la valeur demandée par l'utilisateur (§ 8).
- Les autres contrôles du § 7 restent.

## 11. Révision : la garde lisible au tour de caméra (pas de 2°)

**Ce qui n'allait pas.** La garde du § 10 était juste de profil, mais le tour de caméra
(`--tour 2`, vues absolues) montrait deux défauts :
- de face (90°), les deux poings se cachaient sous la tête, près de l'axe : on ne lisait
  plus la garde ;
- à la vue du jeu (45°), tout le bras arrière se fondait dans le tronc : un seul bras visible.

**Méthode.** Les poings sont placés en 3D avec `mains3d` (cibles relatives à l'épaule, pose à
lacet 0, x devant, y haut, z profondeur, N côté caméra = z négatif), puis on regarde face,
trois quarts, profil et le tour complet dans les deux sens.

| Essai | Poing N | Poing F | Résultat |
|---|---|---|---|
| e1 | (19, −12, −15) | (37, −10, 11) | de face lisible ; à 45° le poing N tombe sur l'axe (x + z ≈ 4) : bras arrière invisible |
| e2 | (28, −12, −7) | (37, −10, 11) | à 45° le poing N sort ; de profil il est caché derrière l'avant-bras F |
| e3 | (26, −14, −7) | (38, −5, 11) | même défaut de profil : le poing N est sur la ligne de l'avant-bras F |
| **e4** | **(23, −4, −8)** | **(38, −10, 11)** | retenu |

**Pourquoi e4.** C'est la garde de boxe classique : le poing arrière **monte au menton** (y −4
sous l'épaule, juste sous la tête) et le poing avant reste **devant, à hauteur de clavicule**.
Comme le poing arrière est plus haut que la ligne de l'avant-bras avant, il ne se cache plus
derrière lui de profil. À 45°, sa projection (x + z ≈ 15) le sort de l'axe du tronc, et
son coude, écarté de 40° côté caméra, fait une bosse au bord du torse.

**Angles retenus** (coudes : `coude_dy` −20/−15, `coude_dx` 2/12, écart 12 à 40°) :
`armN` 28,7, `foreN` 136,2, `armN_r` 19,4, `armN_p` 40 ; `armF` 18,1, `foreF` 100,
`armF_r` 15,3, `armF_p` −28,9. Le reste de la pose (jambes, bassin, buste, épaules) ne
change pas.

**Ce qu'on lit à chaque vue**
- **Face (90°)** : les deux poings de part et d'autre du menton ; le coude arrière s'ouvre
  côté caméra et le coude avant reste près des côtes.
- **Trois quarts (45°, jeu)** : le poing arrière fait une bosse au menton, le coude arrière
  une bosse au bord du torse, et le bras avant est plié vers l'adversaire. On voit deux bras.
- **Profil (0°)** : deux poings étagés. Le poing arrière est au menton, le poing avant est
  plus bas et plus loin devant.
- **Tour de 2° en 2°, dans les deux sens**, sur les 9 clés de la boucle : « lisible à tous
  les angles ». Aucun moignon et aucune main sur la tête.

**Contrôles**
- Vérificateur : aucune traversée (marge 7,5 à la résolution).
- Les alertes admises sont celles du § 10.
- Poing N à environ 126 (sous le menton) ; poing F à environ 120.
- La boucle d'attente garde ses offsets (`plus`). L'« appel » du bras avant (images 10 et 26)
  reste lisible.
