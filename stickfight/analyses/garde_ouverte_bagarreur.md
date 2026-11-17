# Analyse : garde ouverte du bagarreur

Remplacement propre au bagarreur (INVENTAIRE § 3 et § 4 : « sa garde ouverte et son repos »)
de la garde ouverte commune (`analyses/gardes.md`). Fichiers : `poses/garde_ouverte_bagarreur.json`
(la pose) et `anims/garde_ouverte_idle_bagarreur.json` (la boucle). La garde commune et les
animations qui en partent ne changent pas.

Demande de l'utilisateur : « c'est un combattant de rue, donc sa garde ouverte ne doit pas être
trop scolaire, et ses jambes ne doivent pas être trop écartées ».

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
| Hanche arrière | en extension de 14° (cuisse qui part en arrière), écartement −12°, rotation −25° (pied arrière ouvert) | le pas arrière, court |
| Bassin | tourné de 12° (hanche avant devant), presque pas de bascule (`root` −2) | plus de face qu'un boxeur, le poids au milieu |
| Tronc | droit (`spineLow` 4, `chest` 4), torsion 4 en plus du bassin : épaules à 16° | stature droite (règle 6) |
| Omoplates | rapprochées (`epauleN_av` −1, `epauleF_av` 0), à peine haussées (+1) | poitrine ouverte, pas recroquevillée |
| Cou | fléchi de 3 seulement | menton horizontal, regard droit |
| Bras avant (N) | deltoïde antérieur et biceps en tenue : bras levé de 43° devant, écarté de 40°, rotation 25° ; coude fléchi de 54° | poing bas et long, coude sorti de la silhouette |
| Bras arrière (F) | bras levé de 27°, écarté de −30°, rotation −28° ; coude fléchi de 129° (fermé) | poing replié sous le menton, coude décollé |

## 3. La pose, articulation par articulation

Repère : torsions positives, le côté proche (N) vient vers l'avant. Rotation de hanche
positive, le genou part vers la caméra. Écartement : `*N_p` +, `*F_p` −. Plans d'élévation :
les deux bras se lèvent dans le plan **devant** (vers l'adversaire), un peu ouverts sur le côté
(c'est l'écartement) ; aucun bras ne part en arrière.

| Articulation | Axes | Valeurs |
|---|---|---|
| Bassin | hauteur, bascule (`root`), rotation (`torsionBassin`) | y 84, `root` −2, `torsionBassin` 12 |
| Colonne | `spineLow`, `chest`, torsion | 4, 4, `torsion` 4 |
| Omoplate N | avant, haut | `epauleN_av` −1, `epauleN_haut` 1 |
| Omoplate F | avant, haut | `epauleF_av` 0, `epauleF_haut` 1 |
| Cou | flexion, rotation | `neck` 3, `neck_r` 0 |
| Épaule N | élévation (plan devant), écartement, rotation | `armN` 43,05, `armN_p` 40, `armN_r` 25 |
| Coude N | flexion | `foreN` 53,73 |
| Épaule F | élévation (plan devant), écartement, rotation | `armF` 26,86, `armF_p` −30, `armF_r` −28 |
| Coude F | flexion | `foreF` 129,04 |
| Hanche N (avant) | flexion, écartement, rotation | `thighN` 27,57, `thighN_p` 12, `thighN_r` −5 |
| Genou N | flexion | `shinN` 38,16 |
| Cheville N | flexion | `footN` 5,48 : pied à plat |
| Hanche F (arrière) | flexion, écartement, rotation | `thighF` −14,21 (extension), `thighF_p` −12, `thighF_r` −25 |
| Genou F | flexion | `shinF` 24,93 |
| Cheville F | flexion | `footF` 10 : flexion plantaire, talon levé |

Positions qui en résultent, de profil (repère du bassin au sol, x vers l'adversaire) :

- bassin (0 ; 84), épaule (3,2 ; 129,9), tête (6,2 ; 149,8) ;
- coude N (23,4 ; 110,2), poing N (54,8 ; 107,1) : 52 devant l'épaule, 23 sous elle ;
- coude F (8,6 ; 103,3), poing F (30 ; 122) : 36,6 du centre de la tête, soit 5,1 d'écart
  entre les contours (rayons 23 et 8,5) ;
- genou N (21,2 ; 49,2) au-dessus de la cheville N (16 ; 7,9) ;
- genou F (−10 ; 44,7) au-dessus et en avant de la cheville F (−35,9 ; 13,2), pointe F
  (−27,5 ; 8) ;
- 52 entre les chevilles (garde commune 72, pas du repos 42) ; point le plus bas 0,13.

Repères de la bible (§ 3 « Penché, large, bas », H ≈ 173 du sol au haut de la tête) : le
rapide a 0,47 H entre les pieds, le costaud 0,72 H. Le bagarreur est à 0,30 H : plus court que
les deux, à la demande de l'utilisateur. La stabilité vient de la largeur de face et des genoux
souples, pas de la longueur.

### Ce qui se lit dans chaque vue

- **Face** (lacet 90) : chevilles à −10,6 et 16,1, soit 27 de large, sans ligne unique. Coude N
  à −15,9 et coude F à 20,3 de l'axe : les deux coudes sortent de la silhouette du tronc. Le
  poing arrière est sous le menton, le poing avant plus bas, devant le sternum.
- **Trois quarts** (lacet 45) : le poing avant est sur la ligne vers l'adversaire, le poing
  arrière devant le menton. Les chevilles sont à 3,8 et −14 : les pieds se recouvrent presque
  parce que la ligne d'appui (avant-droite vers arrière-gauche) pointe vers la caméra à +45°.
  C'est la vue de l'axe des pieds, pas un défaut : à −45° les mêmes chevilles sont à 56 l'une
  de l'autre.
- **Profil** (lacet 0) : le personnage se tient debout et fait un petit pas, le buste est
  vertical. Le poing avant est bas et long, l'avant-bras presque horizontal ; le poing arrière
  est sous le menton. Le coude arrière est caché derrière le tronc de profil ; il se voit de
  face. La silhouette (A6) dit une seule chose : « approche », pas « boxeur ».

## 4. La boucle `garde_ouverte_idle_bagarreur` (96 i)

A8 : une pose tenue reste vivante. Elle doit l'être sans le petit sautillement de boxeur sur
les plantes. Le bagarreur se balance d'avant en arrière sur ses appuis plantés :

| Image | Ce qui se passe | Amplitudes (en plus de la pose) |
|---|---|---|
| 0 | pose de base | — |
| 14 | la main avant « appelle » : l'avant-bras se déplie, le poids part devant | x +1, y −0,5, torsion +1,5, `armN` +3, `foreN` −10 |
| 26 | poids devant, la main revient | x +1,5, y −0,3, torsion +3, `foreN` −2 |
| 38 | passage, il expire | x +0,2, y −1, `chest` +0,6 |
| 50 | poids derrière, il inspire, les épaules montent | x −1,5, y −0,3, torsion −3, `epaule*_haut` +1, `chest` −0,4 |
| 62 | le menton monte : il toise l'adversaire | x −1,2, torsion −2, `neck` −3, `epaule*_haut` +0,5 |
| 74 | passage, le menton redescend | x −0,2, y −1, `neck` −0,5 |
| 86 | retour | x +0,4, y −0,3 |
| 96 | = image 0 | — |

- Transfert de poids : bassin ±1,5 en x, −1 en y aux passages (le bassin descend un peu entre
  les deux pieds). Il se lit de profil.
- Torsion des épaules ±3, en retard sur le bassin (décalage 3 images).
- Chevauchement : bassin, puis torsion et thorax (3), bras N (6-7), bras F (7-8), cou (5).
- Les chevilles restent plantées (ancre) : seul le bassin bouge, les jambes se replient.
- La boucle est fermée, l'image 0 est égale à la dernière.

## 5. Raccords

Les transitions communes (`mise_en_garde`, `garde_fermer`, `garde_ouvrir`, `sortie_de_garde`,
`marche_avant`…) partent de la garde commune et y arrivent. Pour le bagarreur, il faudra les
remplacer ou les adapter. Ce sera une étape à part, après la validation de cette garde.

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

1. Chevilles de profil : 45 à 55 d'écart en x ; talon arrière 3 à 7 au-dessus du talon avant ;
   point le plus bas entre −0,5 et 0,5.
2. De face : chevilles écartées d'au moins 20.
3. Bassin entre 82 et 86 ; épaule entre 127 et 132.
4. Buste : `root` + `spineLow` + `chest` ≤ 8 vers l'avant ; `epaule*_av` ≤ 0.
5. De face : chaque coude à plus de 15 de l'axe du tronc.
6. De profil : les deux poings à au moins 15 l'un de l'autre en hauteur.
7. Poing F : distance au centre de la tête moins 31,5 entre 2 et 8 (contact interdit).
8. Genou arrière au-dessus de la cheville arrière, cheville arrière en flexion plantaire
   (`footF` > 0).
9. `--verifier` sur la boucle : aucune traversée, aucun pied qui glisse, rien sous le sol, la
   boucle fermée.
