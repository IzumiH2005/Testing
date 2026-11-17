# Analyse : garde ouverte du bagarreur

Remplacement propre au bagarreur (INVENTAIRE § 3 et § 4 : « sa garde ouverte et son repos »)
de la garde ouverte commune (`analyses/gardes.md`). Fichiers : `poses/garde_ouverte_bagarreur.json`
(la pose) et `anims/garde_ouverte_idle_bagarreur.json` (la boucle). La garde commune et les
animations qui en partent ne changent pas.

Demandes de l'utilisateur :

- « c'est un combattant de rue, donc sa garde ouverte ne doit pas être trop scolaire, et ses
  jambes ne doivent pas être trop écartées » ;
- « le pied en arrière peut être tourné légèrement vers l'écran (le genou et la jambe) au lieu
  que ce soit juste le talon qui touche le sol » : hanche arrière en rotation +15 (le genou et
  la jambe viennent vers la caméra) ;
- sur le rendu de cette pose vue à lacet −45 : « cette pose et cet angle de vue, je le trouve
  parfait ». La pose porte donc `lacet` −45 : en jeu, le bagarreur se tient de trois quarts
  dos, l'épaule arrière vers la caméra. Ce choix est celui de l'utilisateur ; ses conséquences
  sur la lecture (bras avant raccourci à l'écran) sont traitées au § 3.

## 1. Intention

La garde commune est une garde de boxe d'école : fente longue (72 entre les chevilles de
profil), bassin très bas (72), buste penché, menton rentré, deux poings serrés au menton. Elle
dit « boxeur appliqué ».

Le bagarreur n'a pas appris en salle. Sa garde dit « vas-y, approche » :

- **debout, plus haut qu'un boxeur** : bassin à 84 (garde commune 72, repos 87,8). Il ne
  s'accroupit pas, il est sûr de lui (règle 6 : buste droit, poitrine ouverte, épaules en
  arrière) ;
- **appuis courts** : un petit pas de marche (52 entre les chevilles de profil), pas une fente.
  Il peut avancer ou cogner sans se replacer ; dans la rue on ne garde pas une distance de
  ring ;
- **plus de face** : bassin tourné de 12°, épaules de 16°. La poitrine se montre ;
- **mains dépareillées, poings fermés** : c'est la garde du costaud de la bible (§ 3 « Les
  bras » : « un poing collé sous le menton et l'autre bras en équerre »), rendue moins
  appliquée :
  - le poing avant est bas et long, à hauteur du sternum, avant-bras presque horizontal, coude
    ouvert : il tient la distance, il peut repousser, attraper ou partir en direct ;
  - le poing arrière est sous le menton, juste devant la mâchoire sans la toucher, coude
    décollé du corps ;
  - les deux poings sont à 15 de hauteur l'un de l'autre : ce n'est pas un mur, il y a un trou
    au milieu, c'est ça qui fait « bagarreur » et non « boxeur » ;
- **menton horizontal**, pas rentré : il regarde l'adversaire droit dans les yeux.

Ce qui reste de la logique d'une garde (`gardes.md` § 1) :

- stable : base en longueur (52) et en largeur (27 de face), genoux souples ;
- prêt à partir : talon arrière levé, mollet arrière chargé ;
- la main arrière couvre la mâchoire, la main avant est entre lui et l'adversaire.

On garde ces trois fonctions, avec moins de technique et plus d'attitude.

## 2. Anatomie

Flexions données dans les unités du rig : `shin*` est la flexion du genou par rapport à la
cuisse (0 = jambe tendue), `fore*` celle du coude par rapport au bras (0 = bras tendu).

| Partie | Ce qui travaille | Pourquoi |
|---|---|---|
| Pied avant | à plat, cheville presque neutre (`footN` 5,5), pointe vers l'adversaire | il porte un peu plus de la moitié du poids |
| Pied arrière | sur l'avant-pied, cheville en flexion plantaire (`footF` 10), talon 5,3 au-dessus du talon avant ; mollet (triceps sural) en tension | la poussée vers l'avant part de là |
| Genou avant | fléchi de 38° (quadriceps en tenue légère) | genou souple, au-dessus de la cheville, pas devant la pointe |
| Genou arrière | fléchi de 25° | jambe arrière en ressort, ni tendue ni accroupie |
| Hanche avant | flexion 27,6°, écartement 12°, rotation −5° (pointe vers la cible) | le pas avant |
| Hanche arrière | en extension de 11° (cuisse qui part en arrière), écartement −15°, rotation +15° (genou et jambe tournés vers la caméra) | le pas arrière, court ; la jambe arrière se tourne vers l'écran, le pied n'est pas qu'un talon posé |
| Bassin | tourné de 12° (hanche avant devant), presque pas de bascule (`root` −2) | plus de face qu'un boxeur, le poids au milieu |
| Tronc | droit (`spineLow` 4, `chest` 4), torsion 4 en plus du bassin : épaules à 16° | stature droite (règle 6) |
| Omoplates | rapprochées (`epauleN_av` −1, `epauleF_av` 0), à peine haussées (+1) | poitrine ouverte, pas recroquevillée |
| Cou | fléchi de 3 seulement | menton horizontal, regard droit |
| Bras avant (N) | deltoïde antérieur et biceps en tenue : bras levé de 31° devant, écarté de 40°, rotation 40° ; coude fléchi de 95° | poing devant le sternum, à 37 devant l'épaule, coude sorti de la silhouette ; bras plié, pas tendu |
| Bras arrière (F) | bras levé de 43°, écarté de −45°, rotation −28° ; coude fléchi de 114° | poing devant la mâchoire, plus haut que le poing avant, coude décollé |

## 3. La pose, articulation par articulation

Repère : torsions positives, le côté proche (N) vient vers l'avant. Rotation de hanche
positive, le genou part vers la caméra. Écartement : `*N_p` +, `*F_p` −. Les deux bras se
lèvent dans le plan **devant** (vers l'adversaire), ouverts sur le côté ; aucun bras ne part
en arrière.

| Articulation | Axes | Valeurs |
|---|---|---|
| Corps entier | orientation à l'écran (`lacet`) | −45 : trois quarts dos (choix de l'utilisateur) |
| Bassin | hauteur, bascule (`root`), rotation (`torsionBassin`) | y 84, `root` −2, `torsionBassin` 12 |
| Colonne | `spineLow`, `chest`, torsion | 4, 4, `torsion` 4 |
| Omoplate N | avant, haut | `epauleN_av` −1, `epauleN_haut` 1 |
| Omoplate F | avant, haut | `epauleF_av` 0, `epauleF_haut` 1 |
| Cou | flexion, rotation | `neck` 3, `neck_r` 0 |
| Épaule N | élévation (plan devant), écartement, rotation | `armN` 31,46, `armN_p` 40, `armN_r` 40 |
| Coude N | flexion | `foreN` 95,21 |
| Épaule F | élévation (plan devant), écartement, rotation | `armF` 42,63, `armF_p` −45, `armF_r` −28 |
| Coude F | flexion | `foreF` 113,91 |
| Hanche N (avant) | flexion, écartement, rotation | `thighN` 26, `thighN_p` 15, `thighN_r` −5 |
| Genou N | flexion | `shinN` 35,95 |
| Cheville N | flexion | `footN` 5,48 : pied à plat |
| Hanche F (arrière) | flexion, écartement, rotation | `thighF` −11,1 (extension), `thighF_p` −15, `thighF_r` +15 (genou vers la caméra) |
| Genou F | flexion | `shinF` 33,12 |
| Cheville F | flexion | `footF` 10 : flexion plantaire, talon levé |

Positions qui en résultent, sans le lacet (plan de profil, bassin au sol, x vers l'adversaire) :

- bassin (0 ; 84), épaule (3,2 ; 129,9), tête (6,2 ; 149,8) ;
- coude N (19,1 ; 107,4), poing N (40 ; 108) : 37 devant l'épaule, 22 sous elle ; le bras
  avant est plié (coude 95), il ne pointe pas comme un direct ;
- coude F (10,4 ; 111,5), poing F (35,9 ; 126,5) : 6,3 d'écart entre les contours du poing et
  de la tête (rayons 8,5 et 23) ; coude F 4 plus haut que le coude N : les deux coudes se
  séparent ;
- poing F 18,5 au-dessus du poing N : les poings sont dépareillés ;
- genou N (20,4 ; 49,1) au-dessus de la cheville N (16 ; 8,1) ;
- genou F (−8,3 ; 44,8) au-dessus et en avant de la cheville F (−35,9 ; 13,3), pointe F
  (−28,5 ; 8,7) ;
- 52 entre les chevilles ; point le plus bas 0,52.

Repères de la bible (§ 3 « Penché, large, bas », H ≈ 173) : le rapide a 0,47 H entre les
pieds, le costaud 0,72 H. Le bagarreur est à 0,30 H, à la demande de l'utilisateur. La
stabilité vient de la largeur de face et des genoux souples, pas de la longueur.

### Ce qui se lit dans chaque vue

Le `lacet` de la pose s'ajoute à celui de la vue : « profil » du jeu = −45 ; les vues de
contrôle sont prises à lacet total 90 (face), 45, 0 (vrai profil) et −45 (vue de jeu).

- **Face** (90) : les deux coudes sortent de la silhouette du tronc ; les cuisses s'écartent
  (`thigh*_p` ±15) et ne se recouvrent pas ; le poing arrière est devant le menton, le poing
  avant plus bas, devant le sternum.
- **Vrai profil** (0) : debout, petit pas, buste vertical ; poing avant devant le sternum,
  poing arrière devant la mâchoire, les deux coudes séparés.
- **Vue de jeu** (−45, trois quarts dos) : l'épaule arrière et le dos viennent vers la
  caméra ; la jambe arrière est tournée vers l'écran (genou et tibia visibles, pas seulement le
  talon) ; la silhouette dit « approche ».
  - Le bras avant part vers l'adversaire et un peu en profondeur : à l'écran il ne montre que
    54 % de sa longueur (alerte du vérificateur « bras proche raccourci »). C'est l'effet de
    l'angle choisi par l'utilisateur, pas d'un bras caché : le poing N (23 ; 108) reste devant
    le tronc, séparé du poing F (14 ; 126,5) de 18,5 en hauteur.
  - Le bras arrière passe devant le tronc à l'écran (alerte « bras loin confondu avec le
    corps ») : on le lit par le poing devant la mâchoire et le coude décollé. Ces deux alertes
    sont acceptées pour cet angle ; elles restent interdites aux autres angles.

## 4. La boucle `garde_ouverte_idle_bagarreur` (96 i)

A8 : une pose tenue reste vivante, sans le sautillement du boxeur. Le bagarreur se balance
d'avant en arrière sur ses appuis plantés :

| Image | Ce qui se passe | Amplitudes (en plus de la pose) |
|---|---|---|
| 0 | pose de base | — |
| 10 | la main avant « appelle » (vite) : l'avant-bras se déplie, le poids part devant | x +2,2, y −1,2, torsion +2,5, `armN` +4, `foreN` −22 |
| 26 | poids devant, la main revient lentement | x +3,5, y −0,6, torsion +5, `armN` +1, `foreN` −4 |
| 38 | passage, il expire | x +0,5, y −2,2, torsion +1, `chest` +0,8 |
| 50 | poids derrière, il inspire, les épaules montent | x −3,5, y −0,6, torsion −5, `epaule*_haut` +1,5, `chest` −0,6 |
| 62 | le menton monte : il toise l'adversaire | x −3, y −0,8, torsion −4, `neck` −5, `epaule*_haut` +0,8 |
| 74 | passage, le menton redescend | x −0,5, y −2,2, torsion −1, `neck` −1, `chest` +0,5 |
| 86 | retour | x +1, y −0,6, torsion +0,5 |
| 96 | = image 0 | — |

- Transfert de poids : bassin ±3,5 en x, −2,2 en y aux passages ; il se lit à l'écran.
- Torsion des épaules ±5, en retard sur le bassin (décalage 3 images).
- Chevauchement : bassin, puis torsion et thorax (3), bras N (6-7), bras F (7-8), cou (5).
- L'appel de la main : le coude N s'ouvre jusqu'à 82° vers l'image 26 (le bras montre alors
  ≤ 80 % de sa longueur de profil) ; il ne devient jamais un bras tendu.
- Les chevilles restent plantées (ancre) : seul le bassin bouge, les jambes se replient.
- Les pieds gardent les angles de la pose (`pieds_auto` false) : le calcul automatique des
  pieds raisonne dans le plan de profil et ne tient pas compte du `lacet` de la pose ; il
  faisait passer les pointes sous le sol.
- La boucle est fermée, l'image 0 est égale à la dernière.

## 5. Raccords

Les transitions communes (`mise_en_garde`, `garde_fermer`, `garde_ouvrir`, `sortie_de_garde`,
`marche_avant`…) partent de la garde commune et y arrivent. Pour le bagarreur il faudra les
remplacer ou les adapter, en tenant compte du `lacet` −45 de cette garde. Ce sera une étape à
part.

## 6. Règles et références

- `BIBLE_ANIMATION.md` :
  - A6, une pose = une idée lisible en silhouette : « approche » ;
  - A8, rien ne s'arrête tout à fait : d'où la boucle ;
  - § 3 « Les bras » : garde du costaud, un poing sous le menton, l'autre bras en avant ;
  - § 3 « Penché, large, bas » et § 12 : posture du costaud presque verticale, ici aussi ;
  - V1 (`etudes/01_strength_vs_speed/`, 136-152) : le costaud en garde, buste droit.
- `CLAUDE.md` du projet, règle 6 : buste droit, `epaule*_av` ≤ 0, ici −1 et 0.
- Règle 5 : le poing arrière près du visage sans le toucher ; le bras avant ne croise pas
  l'autre bras.

## 7. Contrôles chiffrés

1. Chevilles (sans lacet) : 45 à 55 d'écart en x ; talon arrière 3 à 7 au-dessus du talon
   avant ; point le plus bas entre −0,5 et 1.
2. De face : chevilles écartées d'au moins 20 ; cuisses qui ne se recouvrent pas.
3. Bassin entre 82 et 86 ; épaule entre 127 et 132.
4. Buste : `root` + `spineLow` + `chest` ≤ 8 vers l'avant ; `epaule*_av` ≤ 0.
5. De face : chaque coude à plus de 15 de l'axe du tronc.
6. Les deux poings à au moins 15 l'un de l'autre en hauteur ; de face, le poing N plus bas.
7. Poing F : distance au centre de la tête moins 31,5 entre 2 et 8 (contact interdit).
8. Genou arrière au-dessus de la cheville arrière, `footF` > 0, `thighF_r` > 0 (jambe arrière
   tournée vers l'écran).
9. Bras avant de profil : ≤ 75 % de sa longueur dans la pose, ≤ 80 % pendant l'appel.
10. Vue de jeu : écart à l'écran entre le poing F et le bras N d'au moins 6.
11. Boucle : bassin d'au moins ±3 en x, torsion d'au moins ±4.
12. `--verifier` sur la boucle : aucune traversée, aucun pied qui glisse, rien sous le sol, la
    boucle fermée ; seules alertes admises, à cet angle : « bras proche raccourci » et « bras
    loin confondu avec le corps » (§ 3).
