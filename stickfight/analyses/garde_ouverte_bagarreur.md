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

- **debout, presque à hauteur de marche** : il ne s'accroupit pas, il est sûr de lui (règle 6 :
  buste droit, poitrine ouverte, épaules en arrière) ;
- **appuis courts** : un petit pas de marche, pas une fente ; il peut avancer ou cogner sans
  se replacer, comme dans la rue où l'on ne garde pas une distance de ring ;
- **plus de face** : bassin et épaules moins tournés qu'un boxeur. La poitrine se montre ;
- **mains relâchées et dépareillées** : la main avant est en avant, à hauteur de poitrine et
  d'épaule, mi-tendue ; elle tient la distance et peut repousser ou attraper. La main arrière
  est près de la mâchoire, mais pas collée, et le coude est décollé du corps. Ce n'est pas un
  mur ;
- **menton horizontal**, pas rentré : il regarde l'adversaire droit dans les yeux.

Ce qui reste de la logique d'une garde (`gardes.md` § 1) :

- stable : base en longueur et en largeur, genoux souples ;
- prêt à partir : talon arrière levé ;
- la main arrière couvre la mâchoire, la main avant est entre lui et l'adversaire.

On garde ces trois fonctions, avec moins de technique et plus d'attitude.

## 2. Anatomie

| Partie | Ce qui travaille | Pourquoi |
|---|---|---|
| Pieds | pied avant à plat ; pied arrière sur l'avant-pied, talon levé (≈ 4 au-dessus du talon avant) | le mollet arrière est chargé, la poussée part de là |
| Genoux | flexion légère, ≈ 10° avant et 15-20° arrière (quadriceps peu sollicités) | souples sans s'accroupir |
| Hanches | flexion avant ≈ 35° (cuisse avant inclinée vers l'avant), cuisse arrière presque verticale ; écartement ±9° ; rotation : pied avant vers la cible (−5°), pied arrière ouvert (−25°) | petit pas de marche, pas une fente |
| Bassin | tourné de 12° (hanche avant devant), presque pas de bascule (root −2) | plus de face qu'un boxeur, le poids au milieu |
| Tronc | droit (dos 4, thorax 4), torsion 4 en plus du bassin : les épaules sont à 16° | stature droite (règle 6) |
| Omoplates | rapprochées (`epauleN_av` −1, `epauleF_av` 0), à peine haussées (+1) | poitrine ouverte, pas recroquevillée |
| Cou | fléchi de 3 seulement | menton horizontal, regard droit |
| Bras avant (N) | deltoïde antérieur, biceps en tenue : bras levé devant à ≈ 33°, coude ≈ 99°, main à hauteur de poitrine haute | main qui mesure et menace |
| Bras arrière (F) | bras peu levé (≈ 24°), coude fermé (≈ 142°), main près de la mâchoire, coude décollé (−27°) | couvre le menton sans le coller |

## 3. La pose, articulation par articulation

Repère : torsions positives, le côté proche (N) vient vers l'avant. Rotation de hanche
positive, le genou part vers la caméra. Écartement : armN_p +, armF_p −.

| Articulation | Axes | Valeurs |
|---|---|---|
| Bassin | hauteur, bascule (`root`), rotation (`torsionBassin`) | y 82 (garde commune 72, repos 87,8), `root` −2, `torsionBassin` 12 |
| Colonne | `spineLow`, `chest`, torsion | 4, 4, `torsion` 4 |
| Omoplate N | avant, haut | `epauleN_av` −1, `epauleN_haut` 1 |
| Omoplate F | avant, haut | `epauleF_av` 0, `epauleF_haut` 1 |
| Cou | flexion, rotation | `neck` 3, `neck_r` 0 |
| Épaule N | élévation, plan, rotation | `armN` 33,5 (devant), `armN_p` 20 (coude décollé), `armN_r` 1 |
| Coude N | flexion | `foreN` 98,9 |
| Épaule F | élévation, plan, rotation | `armF` 24,4, `armF_p` −26,7 (coude écarté), `armF_r` −28 (avant-bras ramené vers le centre) |
| Coude F | flexion | `foreF` 142 |
| Hanche N (avant) | flexion, écartement, rotation | `thighN` 35,1, `thighN_p` 9, `thighN_r` −5 |
| Genou N | flexion | `shinN` 45,3 (genou au-dessus de la pointe) |
| Cheville N | flexion | `footN` 5,5 : pied à plat |
| Hanche F (arrière) | flexion, écartement, rotation | `thighF` 2,8, `thighF_p` −9, `thighF_r` −25 |
| Genou F | flexion | `shinF` 45,7 |
| Cheville F | flexion | `footF` 20 : sur l'avant-pied, talon levé |

Positions qui en résultent, de profil (repère du bassin au sol, x vers l'adversaire) :

- chevilles N (20 ; 8,2) et F (−25,9 ; 12,3) : 46 de long, contre 72 pour la garde commune et
  42 pour le pas du repos ;
- épaule (3,2 ; 128) : la garde commune est à 117, le repos à 134 ;
- tête (6 ; 148) ;
- main N (44 ; 119), au-dessous de l'épaule et 41 devant ;
- main F (24 ; 123), devant la mâchoire.

Vue de face : pieds écartés d'environ la largeur du bassin, sans ligne unique. Mains devant le
buste, la main avant décalée vers l'adversaire, les coudes sortis de la silhouette du tronc.
Trois quarts : la main avant est sur la ligne vers l'adversaire, la main arrière devant le
menton. Profil : le personnage se tient debout et fait un petit pas, le buste est vertical. La
main avant est en avant et la main arrière près du visage. Le personnage doit se lire « prêt à
cogner, détendu » et non « boxeur ».

## 4. La boucle `garde_ouverte_idle_bagarreur` (96 i)

Elle doit être vivante sans le petit sautillement de boxeur sur les plantes. Le bagarreur se
balance d'une jambe à l'autre :

- poids d'un pied à l'autre, une fois dans chaque sens par cycle : bassin ±1,5 en x et
  ≈ −1 en y au passage ;
- épaules qui roulent un peu : torsion ±3, en retard sur le bassin ;
- vers 12-24, la main avant « appelle » : elle s'ouvre vers l'avant, l'avant-bras se déplie
  de ≈ 10° puis revient ;
- vers 60, un petit mouvement de menton : la tête monte de 2 puis revient, il toise
  l'adversaire ;
- respiration : les épaules montent de 1 à l'inspiration ;
- chevauchement : bassin, puis tronc, puis cou, puis bras (décalages du fichier) ;
- la boucle est fermée, l'image 0 est égale à la dernière.

Les pieds ne glissent pas : les chevilles restent plantées, seul le bassin bouge.

## 5. Raccords

Les transitions communes (`mise_en_garde`, `garde_fermer`, `garde_ouvrir`, `sortie_de_garde`,
`marche_avant`…) partent de la garde commune et y arrivent. Pour le bagarreur, il faudra les
remplacer ou les adapter. Ce sera une étape à part, après la validation de cette garde.

## 6. Règles et références

- `BIBLE_ANIMATION.md` : A1, pas de pose figée (d'où la boucle). Silhouette lisible de profil.
- `CLAUDE.md` du projet, règle 6 : buste droit, `epaule*_av` ≤ 0, ici −1 et 0.
- Règle 5 : la main arrière près du visage sans le toucher. La main avant ne croise pas l'autre
  bras.

## 7. Contrôles chiffrés

1. Chevilles de profil : 40 à 50 d'écart en x. Talon arrière 3 à 6 au-dessus du talon avant.
   Point le plus bas entre −0,5 et 0,5.
2. Bassin entre 80 et 84. Épaule entre 126 et 130.
3. Buste : `root` + `spineLow` + `chest` ≤ 8 vers l'avant. `epaule*_av` ≤ 0.
4. Main N : 35 à 45 devant l'épaule, 5 à 15 sous l'épaule. Main F : 2 à 8 du contour de la
   tête, sans le traverser, et plus basse que l'œil.
5. Coudes hors de la silhouette du tronc de face : écartements N ≥ 18°, F ≤ −22°.
6. `--verifier` sur la boucle : aucune traversée, aucun pied qui glisse, rien sous le sol, la
   boucle fermée.
