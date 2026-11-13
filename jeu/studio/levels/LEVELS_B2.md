# LEVELS B2 : Fonderie froide (150-350 m)

La mécanique du biome est la **plaque friable (O11)** : on ne peut jamais attendre. B2 réapprend au joueur la patience de B1, mais seulement sur des appuis choisis.

Chunks : `jeu/game/chunks/b2/` (32). Simulateur : scratchpad de l'agent, `sim.py`.

## 1. Progression sur 200 m

| Altitude | Phase | Contenu |
|---|---|---|
| 150-155 | Entrée | `b2_entree` : une plaque craque sous la main dès l'arrivée, sans danger. |
| 158-175 | O9 herse | Intro à 160 m, puis l'échelle. |
| 168-185 | O11 friable | Intro à 170 m, puis la course et la volte. |
| 198-215 | O10 mâchoires | Intro à 200 m, puis le pont et les épines. |
| 228-245 | O20 grignon | Intro à 230 m, puis la ronde et la combinaison grignon + friable. |
| 258-275 | O3 contrefort | Intro à 260 m, puis la marche et le laser. |
| 280-350 | Pics | Six chunks P en D6, chacun une serrure à deux mécaniques. |

Les M sont ouverts jusqu'à 345 m pour que le cycle puisse les tirer en fin de biome. Leur borne basse suit toujours l'intro de leur obstacle.

## 2. Cycle M M P R

- Après chaque intro, on enchaîne deux M (développement puis combinaison), un P, puis un R.
- Les R ont un D de 0 ou 1, pas d'attente utile, et servent d'autels ou de brèches.
- Les P sont placés à 280 m ou plus : aucun pic n'est servi avant que les 5 obstacles soient introduits.

## 3. Enseignement en 4 temps

| Obstacle | Intro | Développement | Twist | Conclusion |
|---|---|---|---|---|
| O9 herse | herse_intro : atterrir sous la herse, partir quand elle rentre | herse_echelle : deux herses, partir dès que la première rentre est un piège | herse_contretemps / herse_scie : deux horloges, une seule fenêtre de vol | pic_herses (volte, mur qui mord), pic_fonderie |
| O11 friable | friable_intro : rester, c'est retomber d'une marche | friable_course : la plaque est un appât posé sur des épines | friable_laser : le laser oblige à attendre, la plaque l'interdit ; friable_volte | pic_friable_rail (l'étau) |
| O10 mâchoires | machoires_intro : traverser la gueule en vol | machoires_pont : deux mâchoires en opposition | machoires_epines : ni dessous ni dessus, une seule fenêtre | pic_machoires, pic_fonderie |
| O20 grignon | grignon_intro : lire le demi-tour | grignon_ronde : un cycle de 6 s qu'on ne peut pas attendre | grignon_friable, grignon_scie (la scie couvercle) | pic_grignons |
| O3 contrefort | contrefort_intro : viser une face | contrefort_marche : l'escalier d'un seul mur (volte) | contrefort_laser : le balcon d'attente | pic_contrefort_scie (la serrure) |

## 4. Combinaisons nouveau × ancien

| Combinaison | Chunks |
|---|---|
| Friable × épines | friable_course, friable_volte |
| Friable × laser | friable_laser |
| Friable × rails | pic_friable_rail |
| Friable × grignon | grignon_friable |
| Herse × épines | herse_contretemps, pic_herses |
| Herse × scie fixe | herse_scie |
| Herse × mâchoire | pic_fonderie |
| Mâchoire × épines | machoires_epines, pic_machoires |
| Grignon × scie | grignon_scie |
| Grignon × épines | pic_grignons |
| Contrefort × épines | contrefort_marche |
| Contrefort × laser | contrefort_laser |
| Contrefort × rails | pic_contrefort_scie |

## 5. Tableau des chunks

Attente : attente forcée maximale mesurée par le sim, sur la pire entrée.

| id | T | D | verbe | alt | obstacles | attente | intention |
|---|---|---|---|---|---|---|---|
| b2_entree | I | 1 | bond | 150-152 | O11 | 0 | Une plaque craque sans danger : « ne reste pas ». |
| b2_herse_intro | I | 2 | bond | 158-175 | O9 | 1.25 | Atterrir sous la herse et partir quand elle rentre. |
| b2_friable_intro | I | 1 | bond | 168-185 | O11 | 0 | Un mur entièrement friable ; rester coûte une marche. |
| b2_machoires_intro | I | 3 | bond | 198-215 | O10 | 1.15 | Traverser une gueule en vol. |
| b2_grignon_intro | I | 2 | elan | 228-245 | O20 | 0.20 | Lire le demi-tour du garde. |
| b2_contrefort_intro | I | 2 | elan | 258-275 | O3 | 1.15 | Choisir la face du contrefort selon la hauteur. |
| b2_repos_breche | R | 0 | bond | 165-345 | - | 0 | Repos avec brèche. |
| b2_repos_soufflet | R | 1 | bond | 180-345 | O11 | 0 | Repos, une plaque pour rappel. |
| b2_repos_galerie | R | 1 | elan | 160-345 | O1 | 0.90 | Repos en élan, épines légères. |
| b2_repos_cheminee | R | 1 | bond | 190-345 | O1 | 1.15 | Cheminée calme. |
| b2_repos_coulee | R | 1 | elan | 200-345 | O1 | 1.40 | Coulée avec autel. |
| b2_repos_vitrail | R | 0 | bond | 210-345 | - | 0 | Repos vitrail, éclats. |
| b2_repos_sommet | R | 1 | bond | 320-350 | O11 | 0 | Sortie du biome. |
| b2_herse_echelle | M | 3 | bond | 175-345 | O9 | 1.45 | Partir trop tôt fait arriver sous la seconde herse. |
| b2_herse_contretemps | M | 4 | elan | 180-345 | O1,O9 | 2.00 | Partir assez tôt, pas dès qu'elle rentre. |
| b2_herse_scie | M | 5 | elan | 185-345 | O4,O9 | 1.05 | Deux horloges, une fenêtre de vol. |
| b2_friable_course | M | 3 | elan | 175-345 | O1,O11 | 0 | Les plaques sont des appâts posés sur des épines. |
| b2_friable_volte | M | 4 | volte | 185-345 | O1,O11 | 0 | La volte remplace l'appui qui cède. |
| b2_friable_laser | M | 4 | bond | 240-345 | O8,O11 | 1.15 | Attendre le laser sur le seul pied solide. |
| b2_machoires_pont | M | 4 | bond | 205-345 | O10 | 1.95 | Deux mâchoires en opposition : le pont qui bat. |
| b2_machoires_epines | M | 5 | elan | 215-345 | O1,O10 | 1.85 | Ni dessous ni dessus : une seule fenêtre. |
| b2_grignon_ronde | M | 3 | elan | 235-345 | O20 | 0 | Une ronde trop longue pour être attendue. |
| b2_grignon_friable | M | 4 | elan | 235-345 | O11,O20 | 0.20 | Le garde chasse vers la plaque. |
| b2_grignon_scie | M | 4 | elan | 240-345 | O2,O20 | 1.35 | La scie couvre l'arc qui survolait la ronde. |
| b2_contrefort_marche | M | 5 | volte | 265-345 | O1,O3 | 0 | L'escalier d'un seul mur. |
| b2_contrefort_laser | M | 5 | elan | 265-345 | O3,O8 | 1.85 | Le balcon où attendre le faisceau. |
| b2_pic_machoires | P | 6 | volte | 290-345 | O1,O10 | 0.60 | L'escalier passe dans la gueule. |
| b2_pic_herses | P | 6 | volte | 280-345 | O1,O9 | 1.20 | Grimper un mur qui mord en alternance. |
| b2_pic_grignons | P | 6 | volte | 285-345 | O1,O20 | 0.20 | Monter le mur des gardes. |
| b2_pic_fonderie | P | 6 | elan | 300-350 | O9,O10 | 0.85 | Deux élans longs, chacun à travers un piège. |
| b2_pic_contrefort_scie | P | 6 | elan | 295-345 | O3,O5 | 1.75 | La serrure : une seule rangée libre entre les rails. |
| b2_pic_friable_rail | P | 6 | elan | 300-345 | O5,O11 | 1.70 | L'étau : trois paliers sûrs entre pistons et plaques. |

Totaux :

- Par tension : I 6, R 7, M 13, P 6.
- Par verbe : bond 13 (41 %), élan 14 (44 %), volte 5 (16 %).

## 6. Ce que le sim a vérifié

La passe complète sur `b2/` (32 fichiers) est **OK sur les 32 chunks**. Pour chaque chunk :

- Toutes les routes passent pour les entrées L/R et y0 ∈ {24, 8, −8, −24}, sur toutes les phases d'horloge échantillonnées.
- D déclaré = D calculé.
- Verbe déclaré = verbe minimal.
- Attente forcée ≤ 2,0 s.
- La route commentée est rejouée sur toutes les phases.
- Tous les `o` sont sur l'arc de la route commentée.
- Rangées de raccord propres.
- Aucune note `wip`.

Pour chaque `O`, j'ai vérifié une variante risquée, notée dans le chunk.

Patch du sim : un départage par compteur dans le heap (bug de comparaison de tuples).

## 7. Interprétations et symboles manquants (à trancher par le lead)

- **Laser** : posé en col 1 et col 10. La herse en `warn` est traitée comme létale.
- **Mâchoires** : la géométrie (col 2 et col 9) est supposée.
- **Grignon** : aucun paramètre de phase ni de direction n'existe.
- **Phases** : elles sont relatives au chunk.
- **Notation** : `h` et `H` sont ambigus.
- **Herse** : elle compte par unités de 2 rangées, donc une bande de 4 rangées = 2 instances, ce qui pèse sur D.
- **Formule de D** :
  - +1 si la volte est imposée ;
  - les plaques friables ne comptent pas par instance ;
  - le rail horizontal compte comme un type distinct (O4) du rail vertical (O5).
- **Mâchoires intro** : elle est en D3, au-dessus du plafond I. C'est le coût minimal du type.
- **Volte** : elle ne se force qu'avec un mur d'épines en face. Les 4 chunks volte D5-6 partagent donc ce gabarit, et le volte reste à 16 % (cible 20 %).
- **O par pivot tardif** : dans contrefort_marche, pic_machoires, pic_herses et pic_grignons, le O s'atteint par un pivot tardif sur la route sûre, et non par une route séparée.
- **Échos** : ils sont notés dans chaque chunk. Les plaques gravées deviennent solides, les scies gravées rechargent la volte.
