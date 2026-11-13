# LEVELS B1 · Crypte des Veilleurs (0-150 m)

Ce document est le dossier de level design du biome 1. Les chunks se trouvent dans `jeu/game/chunks/b1/` : 35 fichiers, au format `studio/CHUNK_FORMAT.md`. Chaque chunk porte dans son en-tête `//` son idée, sa route simulée, son O et son raccourci d'écho.

| Tension | Nombre | D | Rangées | Rôle |
|---|---|---|---|---|
| I (introduction) | 8 | 0-2 | 8-12 | `b1_start`, 3 verbes (bond est dans start), 5 obstacles |
| R (repos) | 8 | 0-1 | 6-12 | rythme, 1 seul `*` (`b1_r_niche`) |
| M (montée) | 12 | 2-3 | 12 | une idée par chunk, 1 ou 2 obstacles |
| P (pic) | 6 | 4 | 16 | 3-4 contraintes en série, sans temps mort |
| A (arène) | 1 | 4 | 24 | `b1_boss_sonneur` |

---

## 1. Doctrine

### 1.1 Ce que B1 doit faire

B1 apprend au joueur, sans aucun texte et dans cet ordre :

1. les quatre gestes : **bond**, **élan**, **volte**, puis **écho** ;
2. les cinq obstacles du biome : O1 épines, O2 scie fixe, O8 laser, O4 rail horizontal, O5 rail vertical.

Le prototype a été jugé « beaucoup trop simple ». La réponse retenue n'est **pas** de densifier les pièges. Elle tient en deux règles :

- **un chunk = une idée.** L'idée tient en une phrase et figure dans l'en-tête (`// Idée : …`) ;
- **une hauteur imposée.** Dans chaque M et chaque P, un bond « au hasard » perd. Le chunk fixe la hauteur d'au moins une accroche, ou le moment d'au moins un départ.

Pour chaque chunk, on se demande : « quelle erreur précise ce chunk punit-il ? ». Si la réponse est « aucune », le chunk est un R. Et un R n'a pas le droit d'être un M déguisé (D ≤ 1).

### 1.2 Progression sur 150 m

| Mètres | Ce qui arrive | Chunk d'intro | Pourquoi là |
|---|---|---|---|
| 0 | bond (sol, autel) | `b1_start` | Le premier tap est le jeu. Les éclats dessinent l'arc avant le premier saut. |
| 7 | O1 épines | `b1_i_o1_epines` | C'est l'obstacle le plus lisible : statique et visible de loin. |
| 14 | O2 scie fixe | `b1_i_o2_scie` | Elle est statique comme O1, mais en l'air : elle apprend la forme de l'arc. |
| 22 | O8 laser | `b1_i_o8_laser` | C'est la 1re horloge. On l'apprend accroché, donc sans pression. |
| 30 | **élan** | `b1_i_elan` | Les épines R4-R5 sont posées pile sur l'accroche du bond (+51). L'élan (+77) passe au-dessus. |
| 35 | O4 rail H | `b1_i_o4_rail` | C'est une horloge comme O8, mais elle **bouge**. Le joueur a déjà l'élan pour ajuster. |
| 50 | **volte** | `b1_i_volte` | Le mur d'en face est hérissé de k4 à k10. Le seul chemin est un demi-tour. |
| 64-70 | 1res combinaisons (M D2) | | quinconce, slalom, rail_bas, scies_seuil, scie_pivot |
| 70 | « épines en face » et M D3 | | tenaille, laser_garde, laser_rail, deux_rails, laser_volte |
| 90 | O5 rail V | `b1_i_o5_rail_v` | C'est le dernier élément, il arrive seul. Le timing vertical demande la volte. |
| 98 | combinaisons O5 | | colonne_garde, deux_colonnes |
| 100-110 | pics (P D4) | | gantelet, tir_croise, meules, double_tenaille ; horloge et pilier dès 110 |
| 124-150 | arène du Sonneur | `b1_boss_sonneur` | 3 runes, cloche, onde. |

L'**écho** n'a pas d'intro dédiée. Le moteur le donne au premier passage, et le format n'a pas de symbole d'éclat d'écho pré-placé (voir §6). Chaque M et chaque P indique donc ce que l'écho y rachète (`// Écho : …`). Le pattern est toujours le même : graver l'obstacle-horloge supprime une attente. Le premier écho utile est celui de `b1_i_o8_laser` (22 m).

### 1.3 Le cycle M M P R

`tower.gd` assemble selon le cycle **M M P R**, avec des tolérances de D de 1, 2 et 99.

- **M M.** Deux idées différentes sont posées à la suite. Le joueur ne « cueille » jamais deux fois la même idée, parce que les 12 M ont 12 idées distinctes.
- **P.** C'est un examen : il combine 3-4 contraintes déjà vues. Chaque P a un tableau des intros qu'il présuppose (§2). Les fenêtres `alt` interdisent qu'un P tombe avant ses intros.
- **R.** Il dure 6-12 rangées, avec D ≤ 1. Il n'est jamais vide : il pose **une** question sans danger (un crochet de volte, un `*` en haut d'un élan plein, un O caché derrière une bande). C'est là que le joueur se « réentraîne » au verbe que le P suivant exigera.
- **Fenêtres `alt`.**
  - Les M D2 commencent à 64 m. Les M D3 commencent à 70 m, et ceux qui utilisent O5 à 98 m.
  - Les P commencent à 100 m, et ceux qui contiennent deux horloges à 110 m.
  - On n'a donc jamais deux horloges dans un pic avant que O4 et O8 aient chacun été vus au moins 3 fois.

---

## 2. Enseignement en 4 temps

Chaque obstacle suit le même schéma.

1. **Seul** : l'intro (I), sans aucun autre danger.
2. **Seul, sous contrainte** : il apparaît dans un R ou un M où il est l'unique obstacle, mais où il impose cette fois une hauteur ou un moment.
3. **Combiné** : un M l'associe à un autre obstacle déjà maîtrisé.
4. **Examen** : un P le place dans une série de 3-4 contraintes.

### O1 Épines (7 m)

1. `b1_i_o1_epines`. La main se pose **sous** la bande R5-R6, en R3, et la voit à 8 px au-dessus. Le grand O est collé sous la bande : le rythme naturel le prend.
2. Le réentraînement passe par trois chunks :
   - `b1_r_balcon` : une bande au-dessus de l'accroche ;
   - `b1_r_puits` : L5-6 se survole, R9-10 impose un élan ;
   - `b1_i_elan` : la bande occupe pile l'accroche du bond.
3. Les combinaisons :
   - `b1_m_quinconce` : deux bandes en quinconce, entre les accroches ;
   - `b1_m_tenaille` : « épines en face », 1re fois à 70 m ;
   - avec O8 : `b1_m_laser_garde` et `b1_m_laser_volte` ;
   - avec O4 : `b1_m_rail_bas` ;
   - avec O5 : `b1_m_colonne_garde`.
4. Les examens :
   - `b1_p_double_tenaille` : 4 bandes, le mur libre change tous les 3 rangs ;
   - `b1_p_gantelet` : 3 bandes + scie ;
   - `b1_p_meules` et `b1_p_tir_croise`.

### O2 Scie fixe (14 m)

1. `b1_i_o2_scie`. La scie est posée **au-dessus** du sommet de l'arc naturel. On passe 6 px dessous et on voit sa taille.
2. `b1_m_scie_pivot`. Une seule scie, sur l'arc de retour : il faut tourner autour en volte.
3. `b1_m_slalom` : 2 scies, chacune punit une hauteur d'arrivée. `b1_m_scies_seuil` : un seuil franchi à l'élan.
4. `b1_p_gantelet` : scie et 3 bandes. `b1_p_tir_croise` : laser, épines, scie.

### O8 Laser (22 m)

1. `b1_i_o8_laser`. On attend accroché sous la ligne, on lit le cycle de 3,1 s, on part à l'extinction.
2. `b1_m_laser_garde`. Le laser est seul maître du timing ; la bande R9-10 interdit seulement de rattraper son retard en hauteur.
3. Les combinaisons :
   - `b1_m_laser_rail` : laser + O4, la « double horloge » ;
   - `b1_m_laser_volte` : laser + volte + épines.
4. Les examens :
   - `b1_p_tir_croise` ;
   - `b1_p_horloge` : rail + laser, cinq rangs d'écart ;
   - `b1_p_pilier` : O5 + laser ;
   - l'arène, où l'onde de la cloche est rendue par des lasers mur à mur.

### O4 Rail horizontal (35 m)

1. `b1_i_o4_rail`. La lame balaie k6 de c4 à c7, avec une période de 3,7 s. On traverse quand elle est à l'autre bout.
2. `b1_m_rail_bas`. Le rail impose le départ ; la bande L9-10 impose ensuite la hauteur.
3. `b1_m_deux_rails` : deux rails en opposition de phase. `b1_m_laser_rail` : rail + laser.
4. `b1_p_horloge` : rail + laser à grande échelle. `b1_p_meules` : 2 rails + 2 bandes.

### O5 Rail vertical (90 m)

1. `b1_i_o5_rail_v`. Une colonne au centre (c6, k3-k8, 3,7 s). La question n'est plus « où » mais « quand ».
2. `b1_m_colonne_garde`. La colonne et le mur droit fermé imposent de grimper en voltes à gauche.
3. `b1_m_deux_colonnes`. Deux colonnes en opposition de phase.
4. `b1_p_pilier`. Colonne + laser.

### Les verbes

| Verbe | Intro | Temps 2 (repos) | Temps 3-4 |
|---|---|---|---|
| bond | `b1_start` (0 m) | `b1_r_rythme` : le métronome, ≈ 0,56 s par saut | quinconce, laser_garde |
| élan | `b1_i_elan` (30 m) | `b1_r_niche` (`*` en haut d'un élan plein), `b1_r_deux_arcs`, `b1_r_puits` | slalom, rail_bas, scies_seuil, deux_rails, laser_rail ; P horloge, meules, tir_croise |
| volte | `b1_i_volte` (50 m) | `b1_r_crochets` (le crochet ne se ferme qu'en volte), `b1_r_cascade`, `b1_r_veille` | tenaille, scie_pivot, laser_volte, colonne_garde, deux_colonnes ; P gantelet, pilier, double_tenaille ; arène |
| écho | (moteur) | sans objet | une ligne `// Écho :` par M et par P (§4) |

---

## 3. Table des chunks

Colonne « alt » : la fenêtre en mètres. Colonne « obstacles » : `L4-6` désigne une bande d'épines sur le mur gauche, des rangées k4 à k6, comptées depuis le bas.

| id | T | D | verbe | alt | obstacles | intention (une ligne) |
|---|---|---|---|---|---|---|
| `b1_start` | I | 0 | bond | 0-0 | sol, autel A | Le premier tap est le jeu ; les éclats dessinent l'arc puis le retour. |
| `b1_i_o1_epines` | I | 1 | bond | 7-30 | R5-6 | On voit la bande 8 px au-dessus de sa main avant de devoir l'éviter. |
| `b1_i_o2_scie` | I | 1 | bond | 14-40 | O2 | La scie est au-dessus de l'arc naturel : on la voit tourner, on ne la touche pas. |
| `b1_i_o8_laser` | I | 2 | bond | 22-50 | O8 (3,1 s) | On attend accroché sous la ligne, on part à l'extinction. |
| `b1_i_elan` | I | 1 | élan | 30-60 | R4-5 | La bande est pile sur l'accroche du bond : l'arc des o montre l'élan. |
| `b1_i_o4_rail` | I | 2 | élan | 35-70 | O4 k6 c4-7 | On traverse le rang de la lame quand elle est à l'autre bout. |
| `b1_i_volte` | I | 2 | volte | 50-80 | R4-10 (fente k7 trop étroite) | Le mur d'en face est fermé : le crochet d'éclats enseigne le demi-tour. |
| `b1_i_o5_rail_v` | I | 2 | volte | 90-120 | O5 c6 k3-8 | La colonne se traverse forcément : il faut choisir le moment. |
| `b1_r_rythme` | R | 0 | bond | 60-150 | aucun | 4 o sur l'arc du bond : rendre le métronome audible. |
| `b1_r_crochets` | R | 0 | volte | 64-150 | aucun | Un crochet d'éclats qui ne se ferme qu'avec une volte. |
| `b1_r_niche` | R | 0 | élan | 60-150 | aucun, `*` k6 | Le seul `*` hors arène, en haut d'un élan plein ; le bond passe 20 px dessous. |
| `b1_r_balcon` | R | 1 | bond | 60-150 | R5-6 | Rappel d'O1 sans pression ; le O est collé sous la bande. |
| `b1_r_cascade` | R | 0 | volte | 64-150 | aucun | Monter un seul mur en voltes courtes ; le zigzag rate tout. |
| `b1_r_deux_arcs` | R | 0 | élan | 60-150 | aucun | Deux arcs dessinés : le bas (o) ou le haut (O), au prix du rythme. |
| `b1_r_puits` | R | 1 | élan | 70-150 | L5-6, R9-10 | Le 3e bond tombe dans R9 : il faut tenir un élan, une fois. |
| `b1_r_veille` | R | 1 | volte | 70-150 | R6-7 | Le repos propose un pari : le grand O derrière la bande, en volte tardive. |
| `b1_m_quinconce` | M | 2 | bond | 64-150 | R6-7, L9-10 | Faire confiance au rythme : les bandes sont entre les accroches. |
| `b1_m_slalom` | M | 2 | élan | 64-150 | O2 k5 c8, O2 k8 c3 | Chaque scie punit une hauteur d'arrivée ; on choisit la sienne. |
| `b1_m_rail_bas` | M | 2 | élan | 64-150 | O4 k6, L9-10 | La lame impose le départ, la bande impose la hauteur. |
| `b1_m_scies_seuil` | M | 2 | élan | 64-150 | O2 k6 c3 + c8 | Un seuil de deux lames franchi à l'élan ; le bond a son sommet dans la scie. |
| `b1_m_scie_pivot` | M | 2 | volte | 64-150 | O2 k7 (x=112) | Tourner autour de la scie : élan + volte qui la contourne par le haut. |
| `b1_m_tenaille` | M | 3 | volte | 70-150 | L4-6, R7-9 | 1res « épines en face » : le bond droit atterrit dans la mâchoire. |
| `b1_m_laser_garde` | M | 3 | bond | 70-150 | O8 k6, R9-10 | Le laser dit quand, la bande interdit de rattraper le retard. |
| `b1_m_laser_rail` | M | 3 | élan | 70-150 | O4 k6, O8 k9 | Double horloge : lame en bas, puis laser lu pendant le vol. |
| `b1_m_deux_rails` | M | 3 | élan | 70-150 | O4 k6 + k10 (phases 0 / 0,5) | Traverser en diagonale, toujours du côté vide. |
| `b1_m_laser_volte` | M | 3 | volte | 70-150 | R4-5, R9-10, O8 k7 | Le mur d'en face est interdit 2 fois : volte qui traverse k7 éteint. |
| `b1_m_colonne_garde` | M | 3 | volte | 98-150 | O5 c6 k4-9, R7-8 | La colonne coupe le couloir : voltes serrées entre mur et lame. |
| `b1_m_deux_colonnes` | M | 3 | volte | 98-150 | O5 c5 + c8 (opposition) | Deux portes verticales : entrer dans le couloir au bon moment. |
| `b1_p_gantelet` | P | 4 | volte | 100-150 | L4-6, R8-10, L12-14, O2 k7 | Escalier d'épines : chaque saut a une hauteur imposée, 0 attente. |
| `b1_p_tir_croise` | P | 4 | élan | 100-150 | R5-6, O8 k9, O2 k11, L12-13 | Attendre, viser, lire l'arc : l'ordre du biome en un chunk. |
| `b1_p_meules` | P | 4 | élan | 100-150 | O4 k6 + k11, L8-9, R13-14 | Trois élans pleins d'affilée ; les lames imposent le départ. |
| `b1_p_double_tenaille` | P | 4 | volte | 100-150 | R4-6, L7-9, R10-12, L13-14 | Le mur libre change tous les 3 rangs : voltes de durées différentes. |
| `b1_p_horloge` | P | 4 | élan | 110-150 | O4 k6, O8 k11 | Partir avec la lame donne la bonne phase du laser deux sauts plus haut. |
| `b1_p_pilier` | P | 4 | volte | 110-150 | O5 c6 k5-10, O8 k13 | Voltes du côté libre de la colonne, puis franchir le laser. |
| `b1_boss_sonneur` | A | 4 | volte | 124-150 | cloche (pendule r=20), 4 lasers mur à mur, 3 runes | Allumer 3 runes dans l'ordre de montée sous l'onde de la cloche. |

### Placement des éclats

- Les **`o`** tracent la route simulée. Pour chaque chunk, la recherche demande de **tous** les ramasser depuis l'entrée canonique (L, h≈8) ; la route trouvée est recopiée dans l'en-tête.
- Le **`O`** est toujours hors de la route des o : à moins de 16 px d'un danger, ou au prix d'une hauteur ou d'un moment différent. On a vérifié qu'il est atteignable seul.
- Les éclats de bord respectent les 2 rangées sûres : ils sont autorisés en k1-k2 et dans les 2 dernières rangées.

---

## 4. Raccourcis d'écho

L'écho grave un obstacle pour les runs suivants. En B1, la règle de design est simple : **graver l'horloge, c'est supprimer une attente**. Graver une bande d'épines rouvre un zigzag au bond.

| Chunk | Ce que l'écho rachète | Gain estimé (sim) |
|---|---|---|
| `b1_m_laser_garde` | graver le laser rend le chunk sans attente (il devient un R) | jusqu'à 4,5 s |
| `b1_m_slalom` | graver une scie supprime la contrainte de hauteur sur un mur | ≈ 1,5 s |
| `b1_m_rail_bas`, `b1_m_deux_rails` | graver une lame supprime le timing | ≈ 1 s |
| `b1_m_laser_rail`, `b1_p_horloge` | graver une horloge laisse une seule attente | attente divisée par 2 (jusqu'à 2,3 → 1 s) |
| `b1_p_tir_croise` | graver le laser enlève la seule attente | jusqu'à 3,2 s |
| `b1_p_meules` | graver une meule enlève une attente | ≈ 1,7 s |
| `b1_m_quinconce`, `b1_m_tenaille`, `b1_p_gantelet`, `b1_p_double_tenaille` | graver une bande rouvre le bond simple | 0 s, mais le chunk passe de D3-4 à D1-2 |
| `b1_m_colonne_garde`, `b1_m_deux_colonnes`, `b1_p_pilier` | graver une colonne double la largeur du couloir | 0-1 s |
| `b1_boss_sonneur` | graver un laser supprime une des deux attentes de l'onde | ≈ 1,5 s |

---

## 5. Ce que le simulateur a vérifié, et comment

### 5.1 L'outil

Le simulateur est un script Python (hors dépôt, dans le scratchpad de la session). Il reproduit `world.gd` et le GDD §2.2-2.3 :

- **intégration** : Euler semi-implicite, pas de 1/120 s ;
- **constantes** :
  - gravité 700 ;
  - bond vx ±210, vy −290 ; chute max 330 ;
  - volte vy = min(vy, −205), une fois par saut ;
  - élan : gravité 300 entre 0,10 et 0,28 s ;
- **accroche** : x = 38 et x = 154, glisse à 14 px/s après 0,22 s ;
- **héros** : boîte HALF = (4, 6), plus la marge B1 de 4 px.

L'élan n'est pas dans `world.gd` : il est modélisé d'après le GDD.

Les hitboxes sont celles de `hz.gd` :

| Élément | Hitbox |
|---|---|
| épines | x 32-37 / 155-160, y0+2 à y1−2 |
| scie | r = 6 |
| pendule | r du paramètre ; ancre en haut de rangée |
| laser | létal à \|dy\| < 8 |
| éclat (ramassage) | \|dx\| < 9, \|dy\| < 10 |
| rune | zone de contact y_mid ± 8 ; le simulateur tolère 14 |

Les arcs de référence sont mesurés depuis un mur, à hauteur h :

| Geste | Résultat |
|---|---|
| bond | accroche en face à **+51 px** ; sommet +59 vers c7 |
| élan plein (0,28 s) | **+77** |
| volte à 0,30 s | **+84 sur le même mur** |
| élan + volte (0,36 s) | ≈ **+97** |

### 5.2 Le critère

Pour chaque chunk, les entrées testées sont :

- les **deux côtés** (L et R, puisque le moteur miroite selon `_exit_side`) ;
- **h0 de −20 à +28 px, par pas de 4**, soit 13 hauteurs d'arrivée (h0 = hauteur de la main au-dessus du bas du chunk) ;
- **les phases** : 10 échantillons pour une horloge libre, une grille 5 × 5 pour deux horloges libres, et 20 instants d'arrivée répartis sur 12 s quand toutes les phases sont fixées dans le fichier.

Un chunk statique compte donc 26 entrées ; un chunk à horloges en compte 260 à 650.

Une entrée est **réussie** si une suite de gestes du **verbe déclaré** (ou d'un verbe plus simple) atteint l'accroche de sortie, à h ∈ [H−20, H+32), sans contact létal. Deux limites s'appliquent :

- une **attente ≤ 2,3 s par mur** (0,6 × le budget d'attente B1) ;
- la **marée à 28 px/s** : le héros entre avec 130 px d'avance, et le simulateur suit cette avance (`lag_min` dans les sorties).

La recherche est un Dijkstra sur les états (mur, hauteur, temps, avance sur la marée, éclats pris), qui minimise l'attente totale puis le nombre de sauts. Les gestes essayés depuis chaque accroche : bond, élan tenu 0,14 / 0,18 / 0,22 / 0,28 s, volte de 0,08 à 0,56 s (pas de 0,04), élan + volte (volte de 0,32 à 0,56 s), chacun après 0 à 2,3 s d'attente (glisse comprise). Elle est plafonnée à 6 000 nœuds, et à 30 000 pour l'arène.

En plus de la validation :

- **un lint** vérifie les contraintes du biome :
  - 12 caractères par rang ;
  - 2 rangées sûres en haut et en bas ;
  - jamais d'épines sur les deux murs au même rang ;
  - bandes de 2 à 4 rangs ;
  - pas d'épines en k3 ;
- **la route des o** : un solve depuis (L, h0 = 8) doit ramasser **tous** les `o`. Cette route est recopiée dans l'en-tête du chunk ;
- **le O et le `*`** : chacun doit être atteignable seul ;
- **l'arène** : les 3 runes sont des éclats obligatoires, dans l'ordre des hauteurs ;
- **le parseur Godot** : chaque fichier passe dans `ChunkLib.load_all()`, lancé en headless avec Godot 4.5.1 (`ChunkLib.errors` vide).

### 5.3 Résultats

**Bilan : 34 chunks de parcours validés, 0 échec sur toutes les entrées testées.** L'arène est traitée à part, plus bas.

Lecture des colonnes :

- **Entrées** : nombre d'entrées testées (côté × h0 × phase).
- **Attente max** : la plus longue attente cumulée sur la meilleure route d'une entrée (limite 2,3 s par mur).
- **Marge min** : le plus petit vide entre la boîte du héros et un danger actif sur la route des o (« – » : non relevé, ≥ 4 px).

| Chunk | T | Entrées | Échecs | Attente max (s) | Marge min (px) |
|---|---|---|---|---|---|
| b1_start | I | 1 | 0 | 0 | – |
| i_o1_epines | I | 26 | 0 | 4,5 | – |
| i_o2_scie | I | 26 | 0 | 3,2 | – |
| i_o8_laser | I | 260 | 0 | 1,2 | – |
| i_elan | I | 26 | 0 | 2,1 | – |
| i_o4_rail | I | 260 | 0 | 1,6 | – |
| i_volte | I | 26 | 0 | 0 | – |
| i_o5_rail_v | I | 260 | 0 | 0 | – |
| r_balcon | R | 26 | 0 | 4,5 | – |
| r_cascade | R | 26 | 0 | 0 | – |
| r_crochets | R | 26 | 0 | 0 | – |
| r_deux_arcs | R | 26 | 0 | 0 | – |
| r_niche | R | 26 | 0 | 0 | – |
| r_puits | R | 26 | 0 | 2,1 | – |
| r_rythme | R | 26 | 0 | 0 | – |
| r_veille | R | 26 | 0 | 0 | – |
| m_quinconce | M | 26 | 0 | 4,7 | 6,0 |
| m_slalom | M | 26 | 0 | 3,0 | 4,1 |
| m_laser_garde | M | 260 | 0 | 4,5 | 4,3 |
| m_rail_bas | M | 260 | 0 | 1,8 | – |
| m_tenaille | M | 26 | 0 | 0 | – |
| m_scie_pivot | M | 26 | 0 | 0 | – |
| m_laser_rail | M | 650 | 0 | 2,3 | 4,7 |
| m_colonne_garde | M | 260 | 0 | 0 | – |
| m_deux_rails | M | 520 | 0 | 1,7 | – |
| m_scies_seuil | M | 26 | 0 | 2,8 | 5,3 |
| m_laser_volte | M | 260 | 0 | 0,9 | – |
| m_deux_colonnes | M | 520 | 0 | 1,1 | – |
| p_gantelet | P | 26 | 0 | 0 | – |
| p_tir_croise | P | 260 | 0 | 3,2 | 4,1 |
| p_horloge | P | 650 | 0 | 2,1 | 4,7 |
| p_pilier | P | 650 | 0 | 0,1 | – |
| p_meules | P | 520 | 0 | 3,4 | – |
| p_double_tenaille | P | 26 | 0 | 0 | 4,6 |

L'attente max est cumulée sur tout le chunk, donc elle peut dépasser 2,3 s quand elle est répartie sur plusieurs murs (quinconce : 4,7 s sur 3 murs). La plus grosse attente d'un seul mur reste ≤ 2,3 s partout.

En tout, **6 085 entrées** ont été testées sur les 34 chunks.

**Autres contrôles :**

- **Route des o** : trouvée et recopiée dans l'en-tête des 34 chunks. Chaque rangée d'arrivée porte un commentaire `// kN : arrivée ...`.
- **O** : chaque O est atteignable. Pour les chunks à horloges, il l'est dans au moins 2 phases sur 4.
- **`*`** : le `*` de chaque R est atteignable.
- **Lint** : 0 violation sur les 35 fichiers.
- **Parseur Godot 4.5.1** : `ChunkLib.load_all()` charge 35 chunks B1 (A 1, I 8, M 12, P 6, R 8), avec `ChunkLib.errors` vide.

**Arène (b1_boss_sonneur).** Validation partielle, arrêtée sur demande du lead :

- **Critère.** Les 3 runes sont obligatoires (dans l'ordre des hauteurs). Les entrées sont L/R × h0 {−12, 8, 28} × 10 phases (instants d'arrivée 0, 2, …, 18 sur 20), soit 60 entrées.
- **Résultat :** **23 entrées résolues sur 23 testées**, 0 échec, attente 0 s, recherche de 3 300 à 28 500 nœuds :
  - L −12 : 10/10 ;
  - L 8 : 10/10 ;
  - L 28 : 3/3 (phases 2, 4, 8).
- **Non testées :** les 37 entrées restantes (fin de L 28 et tout le côté R).
- **Une impasse de l'outil, pas du niveau.** Une première passe avait 6 « échecs » (phases ≥ 12). Il s'agissait d'erreurs mémoire du solveur, qui copiait le chemin à chaque empilement. Avec un solveur allégé (chemin chaîné, élagage à l'empilement), ces 6 entrées passent toutes.
- **Le côté R n'est pas validé.** Le chunk qui précède l'arène peut finir des deux côtés (`sortie: any`), donc l'arène peut être abordée par la droite. Cette entrée **reste à valider** avant la sortie du jeu ; le dessin de l'arène n'est pas symétrique.

### 5.4 Ce que le simulateur ne vérifie pas

- **Le ressenti** : lisibilité du préavis, fenêtre de réaction humaine. Le simulateur joue parfait au 1/10 s près, sauf l'attente, qui est discrétisée de 0,1 à 0,15 s. La garantie que nous donnons à la place : chaque route garde **au moins 4 px** de vide entre la boîte du héros (8 × 12, celle du code) et tout danger actif ; le minimum observé sur les routes des o est 4,1 px (tir_croise, slalom).
- **Le raccord réel entre chunks.** Il est couvert indirectement : chaque chunk est validé pour toute hauteur d'entrée de −20 à +28 et des deux côtés.
- **L'onde mobile du boss**, qui est approchée par des lasers (§6).

---

## 6. Problèmes rencontrés et recommandations au lead

### 6.1 Problèmes résolus en cours de route

- **Scies fixes et chunks « bond seul ».**
  - Dans quinconce et scies_seuil, une scie fixe sur l'arc du bond faisait échouer toutes les entrées : avec le bond seul, la hauteur d'arrivée est imposée par le chunk précédent, donc on ne peut pas l'éviter.
  - Règle retenue : **un chunk au bond n'a que des épines ou des lasers**. Les scies arrivent avec l'élan, qui permet de choisir sa hauteur.
- **Arrivées hautes (h0 = 28).** rail_bas, laser_rail et deux_rails échouaient à h0 = 28. Leurs dangers ont été remontés d'un rang.
- **Slalom.** 12 dispositions de scies ont été balayées ; une seule passe pour toutes les entrées : k5 c8 / k8 c3, à l'élan.
- **laser_garde.** 4 variantes ont été balayées. Celle retenue : laser k6, allumé 0,7 s, bande R9-10.
- **Volte le long d'un seul mur.** Elle banalise les dangers posés sur le mur d'en face. colonne_garde, deux_colonnes et laser_volte en profitent.
  - Je l'assume comme idée (« grimper en volte entre mur et colonne »).
  - Les prochains chunks volte devraient aussi armer le mur de la volte.
- **Le O de meules.** En k8 c5, il n'était atteignable dans aucune phase. Déplacé en k8 c6, il est pris dans 2 phases sur 4 : il récompense bien le joueur qui attend le bon moment.
- **La fenêtre de l'élan (i_elan).** L'arc des o (L1 élan 0,28 -> R6) ne passe que pour h0 de 13 à 28 ; de 8 à 11, l'arrivée frôle la marge des épines R4-5. Les entrées basses (h0 < 13) passent par une route de secours simulée : glisser 2,1 s, bond sous la bande, puis élan court. Environ la moitié des hauteurs d'entrée ne voit donc l'élan qu'au-dessus d'elle. C'est noté dans le chunk ; une version future devrait remonter la bande d'un rang ou ajouter 2 rangées sûres en bas.
- **Mémoire du solveur sur l'arène.** Les solves longs (≈ 25 000 nœuds) saturaient la mémoire et passaient pour des échecs. Corrigé par un solveur allégé ; voir §5.3.
- **Le pendule de l'arène.**
  - À k23, il violait la règle des 2 rangées sûres au raccord ; il est passé en k22, avec len 124.
  - La route des runes échouait à cause du plafond de nœuds et d'une tolérance trop stricte sur la rune. Les deux ont été corrigés.

### 6.2 Recommandations (moteur, format, GDD)

1. **Culling du pendule** (moteur). `y1 = anc.y + ln + 12` ignore le rayon. Avec la cloche (r = 20), la lame peut être retirée alors qu'elle dépasse encore. Il faut `ln + r + 6`.
2. **`sortie: any`** (moteur). Il rend le miroir du chunk suivant aléatoire. C'est sans danger ici, parce que tout est validé des deux côtés, mais un autre biome qui ne valide qu'un côté sera piégé. Il faudrait le documenter dans CHUNK_FORMAT.
3. **Élan absent de `world.gd`.** Toute la moitié élan du biome repose sur le GDD : gravité 300 entre 0,10 et 0,28 s, tenue maximale. Si le moteur réel diffère de plus de ±5 px sur le +77, les chunks élan (2 I, 3 R, 5 M, 3 P) sont à revalider.
4. **Hitbox.** Le GDD donne un héros de 6×10, `world.gd` 8×12. Pour le laser, le GDD dit 5 et `hz.gd` 8. J'ai validé avec les valeurs **du code**, les plus sévères. Il faut trancher.
5. **Épines en k3.** Elles cassent l'entrée basse (h0 ≤ 0). Je les ai interdites en B1 ; c'est à ajouter à CHUNK_FORMAT.
6. **Format.**
   - L'exemple de laser de CHUNK_FORMAT (`L#........#L`) ne suit pas la légende (`L` en colonne 1 ou 10, mur `#` à l'extérieur) ; j'ai écrit `#L........L#`.
   - Il n'existe pas de symbole pour un éclat d'écho pré-placé, d'où l'absence d'un chunk d'intro de l'écho.
7. **Intros enchaînées.** Les fenêtres d'intro (7, 14, 22, 30, 35, 50 m) se suivent de près. Entre 7 et 67 m, l'assembleur ne posera presque que des I. C'est voulu (un élément neuf par 8-15 m), mais il faut vérifier dans `tower.gd` qu'un I ne remplace pas le R du cycle. Sinon, le premier repos réel arrive après 64 m.
8. **R peu tirés.** Avec une D cible ≈ 2,6 en fin de biome, les R (D ≤ 1) ne sont choisis qu'en repli, parce que leur tolérance est de 99. C'est correct pour le cycle, mais ils doivent rester **courts**, ce qui est le cas : 6-12 rangées.
9. **GDD §11 contre §4.2.** §11 place l'élan à 22-30 m, la volte à 30-40 m et le laser à 40-50 m ; §4.2 et le brief placent le laser à 22 m. J'ai suivi le brief : laser 22 m, élan 30 m, volte 50 m. Le « 60 premiers mètres faits main » de §11 n'est pas réalisé : ici, l'ordre est garanti par les fenêtres `alt` des I, pas par une séquence fixe.
10. **Arène.** Le format ne peut exprimer :
    - l'onde mobile de 40 px qui descend toutes les 3 s : elle est approchée par 2 paires de lasers déphasés ;
    - l'ordre des runes : imposé seulement par la géométrie, rune 1 en bas et rune 3 en haut ;
    - l'arrêt de la marée pendant le combat.

    Il faut une balise `boss:` ou un script dédié.
