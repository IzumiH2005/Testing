# LEVELS B3 · Bibliothèque engloutie (350-600 m)

Ce document est le dossier de level design du biome 3. Les chunks se trouvent dans `jeu/game/chunks/b3/` : 36 fichiers, au format `studio/CHUNK_FORMAT.md`. Chaque chunk porte dans son en-tête `// Idée : …`, et sa route simulée en `//` sur les rangées d'atterrissage (rangées comptées depuis le bas, 1 = rangée du bas).

| Tension | Nombre | D | Rangées | Rôle |
|---|---|---|---|---|
| I (introduction) | 5 | 1-3 | 16 | `b3_entree` (autel `A`, l'eau seule), puis O18, O6, O12, O19 |
| R (repos) | 8 | 0-1 | 12-24 | souffle, eau sans danger, un `*` dans chacun des 8 R sauf `b3_r_bassin_profond` |
| M (montée) | 17 | 4-6 | 16-24 | une idée par chunk, 2 familles au plus |
| P (pic) | 6 | 7 | 16-24 | 3-5 contraintes en série, un `O` chacun |
| A (arène) | 0 | — | — | la Mère-Phalène n'est pas livrée ici (voir §6) |

Les D respectent la cible GDD 8.5 pour B3 : D moyen 4-5,5 (moyenne des M : 5,0), pics à 7.

---

## 1. Doctrine

### 1.1 Ce que B3 doit faire

B3 est le premier biome où **la physique change**. Dans l'eau, la gravité passe à 300 et la chute est plafonnée à 150 px/s : le même tap porte à **+114 px au lieu de +51**. Toute la doctrine en découle.

- **L'eau n'est pas un piège : c'est un verbe gratuit.** Elle donne au bond la portée d'un élan plein. Le biome apprend donc à **viser** avec un tap aquatique, pas à le subir.
- **L'eau est une hauteur imposée.** Sous l'eau, un bond dépasse l'accroche visée de 60 px. Dès que des épines bordent le bassin, le bond aquatique « trop long » tue. C'est la façon B3 d'imposer élan ou volte (`b3_m_bassin_coupe`, `b3_m_volte_noyee`, `b3_m_rangees_seches`).
- **Les trois nouveaux pièges sont trois horloges différentes.**
  - O6 lustre : horloge périodique **visible** (amplitude 50°, 2,2 s).
  - O12 éboulis : horloge **déclenchée par soi** (96 px sous le livre, 0,6 s de préavis).
  - O19 phalène : horloge **qui balaie** une rangée mur à mur (40 px/s).
- **Un chunk = une idée**, comme en B1. L'idée tient en une phrase et figure dans l'en-tête.

### 1.2 Progression sur 250 m

Les fenêtres `alt` sont réglées pour que chaque élément soit vu seul, puis avec un piège statique, puis avec l'eau, avant d'entrer dans un P.

| Mètres | Ce qui arrive | Chunks | Pourquoi là |
|---|---|---|---|
| 350 | l'eau, seule, depuis l'autel | `b3_entree` | Le premier tap du biome se fait dans l'eau : le joueur voit le saut doubler sans aucun danger. |
| 352-364 | repos secs et aquatiques | `b3_r_salle_lecture`, `b3_r_bassin_profond`, `b3_r_rayonnages`, `b3_r_bulles` | Comparer sec et mouillé dans les R avant toute contrainte. |
| 356 | **O18 eau** (intro officielle) | `b3_eau_tremplin` | Deux bassins séparés par de l'air sec : la différence se sent en sortant de l'eau. |
| 362-375 | eau + B1/B2 | `b3_m_marches_eau` → `rangees_seches`, `bassin_coupe`, `scie_noyee`, `laser_bassin`, `volte_noyee` | L'eau rencontre les pièges connus : épines, scie, laser. |
| 378 | **O6 lustre** | `b3_lustre_intro` | Une horloge visible, lisible depuis l'accroche. |
| 388-410 | lustre + épines, + lustre, + eau | `lustre_epines`, `deux_lustres`, `lustre_haut`, `lustre_bassin`, puis P `nef_des_lustres` (405), `grand_bassin` (410) | Premier P du biome à 405 m, quand eau et lustre ont été vus ≥ 3 fois. |
| 418 | **O12 éboulis** | `b3_eboulis_intro` | Le livre au-dessus de l'accroche : on le fait tomber, on attend, on monte. |
| 425-445 | éboulis + épines, + eau | `eboulis_elan`, `eboulis_epines`, `eboulis_bassin`, P `cascade_livres` (440), `avalanche` (445) | — |
| 448 | **O19 phalène** | `b3_phalene_intro` | La phalène balaie une rangée vide : on regarde, on traverse derrière elle. |
| 455-480 | phalène + épines, + eau, + lustre | `phalene_couloir`, `phalene_bassin`, `phalene_rive`, P `essaim` (475), M `lustre_phalene` (480) | — |
| 500-600 | tout le biome | P `scriptorium` (500) et tout le pool | Les 30 derniers mètres avant l'arène (+1 de D, GDD 8.5) tirent dans le pool complet. |

### 1.3 Le cycle M M P R

`tower.gd` assemble selon le cycle **M M P R** (≈ 40 m par cycle, GDD 8.2).

- **M M.** Deux idées différentes à la suite. Les 17 M portent 17 idées distinctes.
- **P.** C'est un examen qui combine des contraintes déjà vues. Aucun P n'est tirable avant 405 m (voir le tableau du pool plus bas). Le premier cycle (350-405 m) est donc fait d'intros, de M et de R : c'est voulu, c'est la « respiration » de −1,5 D des 20 premiers mètres (GDD 8.5).
- **R.** Il fait 12-24 rangées, avec D ≤ 1. Il pose une seule question sans danger : un `O` derrière un bassin, un `*` au cœur de l'eau, une bande d'épines qui cadre la route.

Pool disponible selon l'altitude (nombre de chunks tirables) :

| m | I | R | M | P |
|---|---|---|---|---|
| 352 | 1 | 1 | 0 | 0 |
| 360 | 1 | 3 | 0 | 0 |
| 370 | 1 | 5 | 4 | 0 |
| 380 | 2 | 6 | 6 | 0 |
| 400 | 1 | 7 | 10 | 0 |
| 410 | 0 | 7 | 10 | 2 |
| 440 | 1 | 8 | 13 | 3 |
| 460 | 1 | 8 | 15 | 4 |
| 480-600 | 0 | 8 | 17 | 5-6 |

Avant 362 m, aucun M n'est tirable : l'assembleur tombera sur sa règle de repli (GDD 8.3, étape 5 : R). C'est voulu, mais à confirmer par le lead (§6).

### 1.4 Combinaisons et règle des familles

- **Au plus 2 familles par chunk.** Les épines comptent comme famille « statique ».
- **Les combinaisons propres à B3** sont : eau + lustre, eau + éboulis, eau + phalène, lustre + phalène, éboulis + phalène.
- Ces paires utilisent déjà 2 familles. On ne peut donc pas y ajouter d'épines pour imposer l'élan ou la volte, et elles restent toutes au **bond** (voir §6, répartition des verbes).
- Les combinaisons du GDD sont présentes :
  - « éboulis + eau » : `b3_m_eboulis_bassin`, `b3_p_avalanche` ;
  - « phalène + pendule » : `b3_m_lustre_phalene` ;
  - « éboulis au-dessus d'un atterrissage élan » : `b3_m_eboulis_elan`, `b3_p_cascade_livres`.

---

## 2. Enseignement en 4 temps

Chaque élément suit la même progression :

1. **seul**, sans pression (intro) ;
2. **avec un statique**, les épines B1, qui imposent une hauteur ;
3. **avec un autre élément B3**, souvent l'eau ;
4. **dans un P**.

### O18 Eau (360 m)

| Temps | Chunk | Alt | Ce qu'il apprend |
|---|---|---|---|
| 1 | `b3_entree`, `b3_eau_tremplin` | 350, 356 | Le tap sous l'eau donne +114. On sort de l'eau très haut. |
| 2 | `b3_m_marches_eau`, `b3_m_rangees_seches`, `b3_m_bassin_coupe`, `b3_m_volte_noyee` | 362-375 | Le bond aquatique est trop long quand des épines bordent le bassin : on vise, on change de mur (volte), ou on sort au sec (élan). |
| 3 | `b3_m_scie_noyee`, `b3_m_laser_bassin`, puis `lustre_bassin`, `eboulis_bassin`, `phalene_bassin` | 370-460 | L'eau ralentit la chute : on attend une horloge accroché sous l'eau sans glisser vers la marée. |
| 4 | `b3_p_grand_bassin`, `b3_p_avalanche` | 410, 445 | Trois bassins en série, ou deux bassins sous deux livres. |

### O6 Lustre-pendule (380 m)

| Temps | Chunk | Alt | Ce qu'il apprend |
|---|---|---|---|
| 1 | `b3_lustre_intro` | 378 | Les accroches sont hors de portée de la masse (±37 px, 31-48 px sous l'ancre). On regarde le balancier. |
| 2 | `b3_m_lustre_epines`, `b3_m_lustre_haut` | 388, 395 | Une bande d'épines impose l'élan, et l'arrivée tombe sous le balancier. |
| 3 | `b3_m_deux_lustres` (phases opposées), `b3_m_lustre_bassin` | 392, 398 | Deux lustres, puis le bassin qui propulse droit dans la zone du lustre. |
| 4 | `b3_p_nef_des_lustres`, `b3_p_grand_bassin`, `b3_m_lustre_phalene` | 405-480 | Le lustre comme métronome d'un pic. |

### O12 Éboulis de livres (420 m)

| Temps | Chunk | Alt | Ce qu'il apprend |
|---|---|---|---|
| 1 | `b3_eboulis_intro` | 418 | Le danger se déclenche **au-dessus** de soi. On le déclenche, on attend 0,6 s, on monte. |
| 2 | `b3_m_eboulis_elan`, `b3_m_eboulis_epines` | 425, 428 | Livre plus épines : l'élan passe sous le livre déjà tombé, la volte change de mur avant la chute. |
| 3 | `b3_m_eboulis_bassin` | 430 | On le déclenche depuis l'eau, où il tombe à 180 px/s. |
| 4 | `b3_p_cascade_livres`, `b3_p_avalanche`, `b3_p_scriptorium` | 440-500 | Deux livres en série, puis avec l'eau, puis avec la phalène. |

### O19 Phalène de papier (450 m)

| Temps | Chunk | Alt | Ce qu'il apprend |
|---|---|---|---|
| 1 | `b3_phalene_intro` | 448 | Elle balaie une rangée : on part derrière elle. |
| 2 | `b3_m_phalene_couloir`, `b3_m_phalene_rive` | 455, 465 | Entre deux bandes d'épines, l'élan traverse sa rangée d'un trait. |
| 3 | `b3_m_phalene_bassin`, `b3_m_lustre_phalene` | 460, 480 | Au-dessus de l'eau, et après un lustre : deux horloges successives. |
| 4 | `b3_p_essaim` (2 phalènes en sens contraire), `b3_p_scriptorium` | 475, 500 | Préparation directe de la Mère-Phalène (essaim de 3). |

### Les verbes

| Verbe | Chunks | M + P seuls |
|---|---|---|
| bond | 24 (dont les 5 I et les 8 R) | 11 / 23 (48 %) |
| élan | 8 | 8 / 23 (35 %) |
| volte | 4 | 4 / 23 (17 %) |

Le brief visait 40/40/20. Sur les M et P, on obtient 48/35/17. L'écart vient de la règle des 2 familles (voir §1.4 et §6).

---

## 3. Table des chunks

Notation des obstacles : O1 épines, O5 scie sur rail vertical, O8 laser, O6 lustre, O12 livre, O18 bassin d'eau (une bande d'eau contiguë = 1), O19 phalène.

| id | T | D | verbe | alt | Rangées | Obstacles | Intention |
|---|---|---|---|---|---|---|---|
| `b3_entree` | I | 1 | bond | 350-358 | 16 | autel `A`, O18 | L'eau seule : le même tap porte deux fois plus haut. |
| `b3_eau_tremplin` | I | 2 | bond | 356-380 | 16 | O18 ×2 | Deux bassins séparés par de l'air sec. |
| `b3_lustre_intro` | I | 3 | bond | 378-400 | 16 | O6 | Lire le balancier depuis des accroches sûres. |
| `b3_eboulis_intro` | I | 2 | bond | 418-440 | 16 | O12 | Déclencher le livre, attendre, monter. |
| `b3_phalene_intro` | I | 2 | bond | 448-470 | 16 | O19 | Traverser derrière la phalène. |
| `b3_r_salle_lecture` | R | 0 | bond | 352-600 | 12 | — | Repos sec, `*` sur la route centrale. |
| `b3_r_bassin_profond` | R | 1 | bond | 360-600 | 16 | O18 | Longs bonds aquatiques ; `O` à la sortie haute. |
| `b3_r_rayonnages` | R | 0 | bond | 360-600 | 16 | — | Zigzag sec ; `O` décalé à gauche. |
| `b3_r_bulles` | R | 1 | bond | 364-600 | 12 | O18 | Bassin court, `*` au cœur de l'eau. |
| `b3_r_reliure` | R | 1 | bond | 370-600 | 16 | O1 | Une bande à gauche cadre la route ; `O` juste au-dessus. |
| `b3_r_bassin_haut` | R | 1 | bond | 380-600 | 16 | O18 | Eau en haut : on y entre au sec et on en sort très haut. |
| `b3_r_galerie` | R | 0 | bond | 400-600 | 24 | — | Longue galerie sèche, souffle avant les pics. |
| `b3_r_noyade_douce` | R | 1 | bond | 440-600 | 12 | O18 | Bassin jusqu'au plafond. |
| `b3_m_marches_eau` | M | 4 | bond | 362-600 | 16 | O18, O1 ×2 | Épines en escalier : le bond aquatique vise entre les marches. |
| `b3_m_rangees_seches` | M | 6 | élan | 366-600 | 20 | O18 ×2, O1 ×2 | Hors de l'eau, seul l'élan franchit les rangées sèches. |
| `b3_m_bassin_coupe` | M | 5 | volte | 368-600 | 16 | O18, O1 ×2 | L'épine plonge dans l'eau : volte avant la bande. |
| `b3_m_scie_noyee` | M | 4 | bond | 370-600 | 16 | O18, O5 | Partir de l'eau quand la scie remonte. |
| `b3_m_laser_bassin` | M | 4 | bond | 372-600 | 16 | O18, O8 | Attendre sous l'eau que le laser s'éteigne. |
| `b3_m_volte_noyee` | M | 5 | volte | 375-600 | 16 | O18, O1 | Volte obligatoire depuis l'eau. |
| `b3_m_lustre_epines` | M | 5 | élan | 388-600 | 16 | O6, O1 | Élan par-dessus la bande, arrivée sous le balancier. |
| `b3_m_deux_lustres` | M | 6 | bond | 392-600 | 16 | O6 ×2 | Phases opposées : l'un passe, l'autre libère. |
| `b3_m_lustre_haut` | M | 5 | élan | 395-600 | 16 | O6, O1 | Élan vers l'accroche haute quand la masse est loin. |
| `b3_m_lustre_bassin` | M | 5 | bond | 398-600 | 16 | O6, O18 | Le bassin propulse dans la zone du lustre. |
| `b3_m_eboulis_elan` | M | 6 | élan | 425-600 | 16 | O12 ×2, O1 | L'élan passe sous le livre déjà tombé. |
| `b3_m_eboulis_epines` | M | 6 | volte | 428-600 | 16 | O12, O1 ×2 | Volte sous le livre avant sa chute. |
| `b3_m_eboulis_bassin` | M | 4 | bond | 430-600 | 16 | O12, O18 | Déclencher le livre depuis l'eau. |
| `b3_m_phalene_couloir` | M | 5 | élan | 455-600 | 16 | O19, O1 ×2 | Élan pendant que la phalène est loin. |
| `b3_m_phalene_bassin` | M | 4 | bond | 460-600 | 16 | O19, O18 | Bond aquatique derrière la phalène. |
| `b3_m_phalene_rive` | M | 5 | élan | 465-600 | 16 | O19, O1 ×2 | Traverser la rangée de la phalène d'un trait. |
| `b3_m_lustre_phalene` | M | 6 | bond | 480-600 | 24 | O6, O19 | Deux horloges successives. |
| `b3_p_nef_des_lustres` | P | 7 | élan | 405-600 | 24 | O6, O1 ×4 | Quatre bandes alternées, rythme imposé par la masse. |
| `b3_p_grand_bassin` | P | 7 | bond | 410-600 | 24 | O6, O18 ×3 | D'eau en eau, passage calé sur le lustre. |
| `b3_p_cascade_livres` | P | 7 | volte | 440-600 | 16 | O12 ×2, O1 | Volte pour esquiver la chute en changeant de mur. |
| `b3_p_avalanche` | P | 7 | bond | 445-600 | 24 | O12 ×2, O18 ×2 | Déclencher les livres depuis l'eau sans s'arrêter dessous. |
| `b3_p_essaim` | P | 7 | élan | 475-600 | 24 | O19 ×2, O1 ×2 | Passer entre les croisements de deux phalènes. |
| `b3_p_scriptorium` | P | 7 | bond | 500-600 | 24 | O12 ×2, O19 | Déclencher, esquiver, traverser. |

`entree` vaut `L` pour la plupart des M et P (le moteur miroite le chunk pour une entrée R). `sortie` vaut `any` partout.

### Placement des éclats

- **`o` :** posés sur la route simulée (`annotate.py --snap`), ils dessinent l'arc juste du verbe demandé.
- **`O` :** un par P, et dans 6 M et 6 R. Toujours sur une route risquée, mais atteignable : marge 0, volte autorisée.
- **`*` (créneau power-up, GDD 8.2) :** un par R, sauf `b3_r_bassin_profond`, soit 7. Aucun `*` hors des R.

---

## 4. Raccourcis d'écho

L'écho grave un obstacle pour les runs suivants (GDD 3.2). En B3, deux règles s'ajoutent à celles de B1.

- **L'eau ne se grave pas.** Elle n'est pas létale. La règle du complice ne s'y applique pas non plus : elle ne figure pas dans la liste des éléments non létaux. L'eau reste donc une constante du biome : c'est elle qui donne sa portée au bond.
- **Les pièges B3 gravés deviennent des points de recharge de volte, au milieu du couloir.**
  - Un livre gravé reste figé en l'air.
  - Un lustre gravé reste une masse cyan qui continue de balancer : c'est une recharge mobile.
  - Une phalène gravée est cyan.
  - Toucher l'un d'eux recharge la volte : il ouvre donc des doubles voltes vers les `O`.

Gains mesurés par le simulateur. Le chunk est rejoué avec l'obstacle retiré, au verbe déclaré, sur toutes les entrées, phases au pas de 0,6 s. Le simulateur ne modélise pas la recharge cyan : les gains réels sont au moins ceux-ci.

| Chunk | Gravure | Avant → après (attente max, temps moyen) | Effet |
|---|---|---|---|
| `b3_m_laser_bassin` | laser | 0,90 → 0 s ; 2,01 → 1,86 s | Le chunk devient un R aquatique. |
| `b3_m_scie_noyee` | scie | 0,90 → 0 s ; 2,34 → 2,05 s | Plus aucune attente. |
| `b3_m_lustre_bassin` | lustre | 1,15 → 0 s ; 2,38 → 2,05 s | Le bassin propulse librement. |
| `b3_p_grand_bassin` | lustre | 0,65 → 0 s ; 2,89 → 2,79 s | Le pic devient une remontée d'eau continue ; le lustre cyan est au centre, sur la route du `O`. |
| `b3_p_scriptorium` | phalène | 1,40 → 0,05 s ; 4,52 → 4,11 s | La meilleure gravure du biome : les livres seuls ne forcent plus d'attente. |
| `b3_m_eboulis_elan` | bande R | 1,65 → 0 s ; 2,93 → 1,86 s | Le bond suffit de nouveau (2,61 s). |
| `b3_m_phalene_rive` | phalène | 1,70 → 0 s ; 2,05 → 1,86 s | L'élan reste nécessaire : les bandes demeurent. |
| `b3_m_lustre_phalene` | lustre | 1,70 → 1,05 s ; 4,69 → 4,39 s | Il ne reste que l'horloge phalène. |
| `b3_m_deux_lustres` | lustre bas | 1,50 → 1,50 s ; 3,32 → 2,93 s | L'autre lustre garde la pire attente. Il faut graver les deux. |
| `b3_p_essaim` | phalène haute | 1,70 → 1,70 s ; 4,38 → 4,00 s | La phalène basse garde la pire attente. Gravée, la haute devient la recharge du `O`. |
| `b3_m_rangees_seches`, `b3_p_cascade_livres`, `b3_m_eboulis_epines` | une bande d'épines | aucun gain de temps | Le chunk redevient faisable au bond (2/3 à 3/3 des entrées), mais plus lentement. La gravure rend le chunk plus sûr, pas plus rapide. |
| `b3_m_phalene_couloir`, `b3_p_nef_des_lustres` | phalène, lustre | ≈ 0 s | L'horloge n'était pas le goulot. Ce sont les bandes qui imposent l'élan. |

Routes qu'ouvre la recharge cyan (non simulées, à vérifier en jeu) :

| Chunk | Gravure | Grand éclat |
|---|---|---|
| `b3_p_nef_des_lustres` | lustre | Volte depuis R13, recharge sur la masse, seconde volte vers le `O` (rangée 18 côté R) sans repasser par le mur. |
| `b3_p_grand_bassin` | lustre | La masse au centre recharge entre les deux bassins hauts ; le `O` central se prend en plein vol. |
| `b3_p_cascade_livres` | livre haut | Le livre figé à droite sert d'appui pour le `O` collé au mur droit. |
| `b3_p_avalanche` | livre haut | Même principe : le `O` du bassin haut se prend en volte rechargée. |
| `b3_p_essaim` | phalène haute | Le `O` est sur sa rangée : gravée, elle est à la fois la porte et la recharge. |
| `b3_p_scriptorium` | phalène | Même chose : le `O` est sur la rangée de la phalène. |

---

## 5. Ce que le simulateur a vérifié, et comment

### 5.1 L'outil

Le simulateur est en Python. Il est écrit pour ce biome et se trouve hors du dépôt, dans le scratchpad de l'agent : `sim.py`, `check.py`, `verbs.py`, `routes.py`, `probe.py`, `annotate.py`, `echo.py`.

- **Physique : celle du GDD 2.3, au demi-tick (1/120 s).**

  | Arc | Valeur |
  |---|---|
  | bond sec | +51 px |
  | élan plein | +77 px |
  | volte à 0,3 s | +84 px |
  | élan + volte | +91 px |
  | bond dans l'eau (gravité 300, chute ≤ 150) | +114 px |

  `arcs.py` valide ces valeurs.
- **Géométrie.** Tuile de 16 px ; couloir x 32-160 ; accroche à x = 38 ou 154 ; hitbox 6 × 10 ; marge B3 de 3 px.
- **Pièges.**

  | Piège | Modèle |
  |---|---|
  | Épines | Bandes statiques. |
  | Laser (O8) | Période 3,1 s, préavis 0,7 s, 0,9 s actif. |
  | Scie sur rail | Aller-retour sinusoïdal. |
  | Lustre | Pendule de longueur 48 px et d'amplitude 50°. La masse atteint ±36,8 px en x et ancre + 31-48 px en y. |
  | Livre | Déclenché 96 px sous lui. Préavis 0,6 s, puis chute à 300 px/s, ou 180 px/s dans l'eau. |
  | Phalène | Balaie sa rangée mur à mur à 40 px/s, avec rebond. Une rangée de phalène n'est jamais une accroche sûre. |
- **Recherche.**
  - C'est un Dijkstra sur les états « accroché » (côté, hauteur, temps).
  - Il essaie les attentes de 0 à 1,7 s par pas de 0,05 s, chaque tenue d'élan, et des voltes à 0,12-0,45 s.
  - Il compte les collisions avec la marge, de façon vectorisée.
- **Entrées.** Les 3 hauteurs d'accroche d'entrée (16H−24, 16H−8, 16H+8) × toutes les phases des horloges, au pas de 0,1 s sur un cycle.

### 5.2 Le critère

Pour chaque chunk, `check.py` vérifie les points suivants :

1. **Format.** En-tête complet, 12 caractères par rangée, murs, 2 rangées propres en haut et en bas, jamais d'épines face à face, au plus 4 rangées d'épines d'affilée par côté, au plus un `*`, au moins une route `//`, `alt` dans 350-600.
2. **D.** Le D déclaré égale le D calculé : coûts GDD 4.2 par instance, +1 par type supplémentaire, +1 si volte. Deux familles au plus.
3. **Verbe minimal.** Le verbe déclaré réussit sur **100 %** des entrées × phases, avec une marge de 3 px. Le verbe inférieur échoue sur au moins une entrée ou phase.
4. **Attente forcée.** Elle est d'au plus 1,7 s, soit 0,6 × le budget B3 de 2,9 s (GDD 8.6).
5. **Éclats.** Les `o` sont sur la route exemple. Chaque `O` est atteignable avec une marge de 0 et la volte autorisée.

### 5.3 Résultats

Le passage complet couvre les 36 chunks, au pas de phase de 0,1 s.

- **0 erreur** sur les 36 chunks :
  - format conforme ;
  - D déclaré = D calculé partout ;
  - verbe déclaré à 100 % ;
  - attente forcée ≤ 1,7 s ;
  - tous les `O` atteignables.
- **Verbe minimal :** dans tous les chunks élan ou volte, le verbe inférieur échoue sur au moins une entrée ou phase. Il échoue même à 0 % dans `b3_m_phalene_rive`, `b3_p_essaim` et `b3_m_volte_noyee` (bond).
- **Une correction après le passage :** `b3_r_reliure`.
  - En entrée R, il imposait 1,7 s d'attente (glisser sous la bande gauche), ce qui est inacceptable pour un R.
  - Il est passé en `entree: L` : le miroir couvre l'autre côté. Son attente max est maintenant de 0,85 s.
- **Attentes à la limite (1,65-1,70 s).** Elles touchent `b3_m_rangees_seches`, `b3_m_eboulis_elan`, `b3_m_phalene_rive`, `b3_m_lustre_phalene` et `b3_p_essaim`. Elles ne concernent que la pire combinaison entrée × phase : les temps moyens restent de 2-4,5 s. Ce sont les chunks à surveiller si la marée est accélérée.
- **`o` sur la route.** Les `o` ont été posés sur la route d'une entrée donnée. La colonne « o » de `check.py` ne compte que ceux de la route exemple, d'où des scores de 0/3 à 4/4 selon l'entrée choisie. Aucun `o` n'est hors d'une route faisable.

La colonne « O atteint » compte les phases testées (une sur trois) où une route à marge 0, volte permise, ramasse le `O`.

| Chunk | T | Verbe | Réussites (entrées × phases) | Verbe inférieur | Attente max (s) | Temps moy / max (s) | O atteint |
|---|---|---|---|---|---|---|---|
| `b3_eau_tremplin` | I | bond | 6/6 | — | 0,00 | 1,86 / 2,23 | — |
| `b3_eboulis_intro` | I | bond | 6/6 | — | 0,20 | 2,67 / 2,99 | — |
| `b3_entree` | I | bond | 6/6 | — | 0,00 | 2,05 / 2,23 | — |
| `b3_lustre_intro` | I | bond | 186/186 | — | 1,45 | 2,91 / 4,24 | — |
| `b3_phalene_intro` | I | bond | 180/180 | — | 1,25 | 2,95 / 4,14 | — |
| `b3_r_bassin_haut` | R | bond | 6/6 | — | 0,00 | 2,23 / 2,23 | 1/1 |
| `b3_r_bassin_profond` | R | bond | 6/6 | — | 0,00 | 1,68 / 1,68 | 1/1 |
| `b3_r_bulles` | R | bond | 6/6 | — | 0,00 | 1,12 / 1,12 | — |
| `b3_r_galerie` | R | bond | 6/6 | — | 0,00 | 4,09 / 4,47 | 1/1 |
| `b3_r_noyade_douce` | R | bond | 6/6 | — | 0,00 | 1,12 / 1,12 | 1/1 |
| `b3_r_rayonnages` | R | bond | 6/6 | — | 0,00 | 2,61 / 2,79 | 1/1 |
| `b3_r_reliure` | R | bond | 3/3 | — | 0,85 | 3,07 / 3,64 | 1/1 |
| `b3_r_salle_lecture` | R | bond | 6/6 | — | 0,00 | 1,86 / 2,23 | — |
| `b3_m_bassin_coupe` | M | volte | 3/3 | elan 67 % | 0,00 | 1,05 / 1,15 | — |
| `b3_m_deux_lustres` | M | bond | 93/93 | — | 1,50 | 3,21 / 4,34 | — |
| `b3_m_eboulis_bassin` | M | bond | 3/3 | — | 1,40 | 2,80 / 3,63 | 1/1 |
| `b3_m_eboulis_elan` | M | élan | 3/3 | bond 67 % | 1,65 | 2,93 / 4,23 | — |
| `b3_m_eboulis_epines` | M | volte | 3/3 | elan 67 % | 0,00 | 1,14 / 1,22 | — |
| `b3_m_laser_bassin` | M | bond | 93/93 | — | 0,90 | 2,02 / 3,13 | — |
| `b3_m_lustre_bassin` | M | bond | 93/93 | — | 1,35 | 2,40 / 3,58 | 11/11 |
| `b3_m_lustre_epines` | M | élan | 93/93 | bond 67 % | 0,25 | 1,93 / 2,23 | — |
| `b3_m_lustre_haut` | M | élan | 93/93 | bond 81 % | 1,05 | 2,03 / 3,28 | — |
| `b3_m_lustre_phalene` | M | bond | 90/90 | — | 1,70 | 4,71 / 6,37 | 10/10 |
| `b3_m_marches_eau` | M | bond | 3/3 | — | 0,00 | 2,23 / 2,23 | 1/1 |
| `b3_m_phalene_bassin` | M | bond | 90/90 | — | 1,35 | 2,32 / 3,78 | — |
| `b3_m_phalene_couloir` | M | élan | 90/90 | bond 33 % | 1,35 | 2,51 / 3,63 | 10/10 |
| `b3_m_phalene_rive` | M | élan | 90/90 | bond 0 % | 1,70 | 2,01 / 6,69 | — |
| `b3_m_rangees_seches` | M | élan | 3/3 | bond 33 % | 1,70 | 3,72 / 6,69 | 1/1 |
| `b3_m_scie_noyee` | M | bond | 90/90 | — | 1,40 | 2,35 / 3,93 | — |
| `b3_m_volte_noyee` | M | volte | 3/3 | elan 67 % | 0,00 | 1,05 / 1,15 | — |
| `b3_p_avalanche` | P | bond | 3/3 | — | 0,70 | 3,21 / 4,05 | 1/1 |
| `b3_p_cascade_livres` | P | volte | 3/3 | elan 67 % | 0,00 | 1,13 / 1,20 | 1/1 |
| `b3_p_essaim` | P | élan | 90/90 | bond 0 % | 1,70 | 4,33 / 7,50 | 10/10 |
| `b3_p_grand_bassin` | P | bond | 93/93 | — | 0,85 | 2,92 / 3,64 | 11/11 |
| `b3_p_nef_des_lustres` | P | élan | 93/93 | bond 52 % | 0,75 | 3,06 / 3,74 | 11/11 |
| `b3_p_scriptorium` | P | bond | 90/90 | — | 1,40 | 4,51 / 6,31 | 6/10 |


### 5.4 Ce que le simulateur ne vérifie pas

- La recharge cyan après gravure, donc les routes du §4 en double volte.
- Le raccord entre chunks : la sortie d'un chunk n'est pas rejouée comme entrée du suivant, et l'horloge globale n'est pas partagée.
- La marée de Silence : l'attente est bornée à 1,7 s, mais la position de la crête n'est pas simulée.
- Les pièges `M` (mâchoires) et `C` (contrefort) : ils ne sont pas modélisés, donc aucun chunk B3 ne les utilise.
- Les phalènes sont modélisées en ligne droite mur à mur. Si le moteur leur donne une ondulation verticale, il faut rejouer les M et P qui en contiennent.

---

## 6. Problèmes rencontrés et recommandations au lead

### 6.1 Problèmes résolus en cours de route

- **Verbes surdéclarés.** Plusieurs chunks pensés « élan » ou « volte » se sont révélés faisables au bond : la glissade et les tenues partielles donnent beaucoup de hauteurs atteignables.
  - Ils ont été redéclarés au bond, ou retouchés : bande raccourcie dans `eboulis_elan`, `phalene_volte` remplacé par `phalene_rive`, `lustre_volte` devenu `lustre_haut` en élan.
- **Entrées `any`.** Avec des bandes d'épines asymétriques, l'entrée miroir cassait la route. Les M et P sont donc en `entree: L` (le moteur miroite).
- **`b3_m_marches_eau`.** L'entrée basse s'empalait sur la marche L. Les bandes sont décalées (L 9-11, R 6-7, rangées comptées depuis le bas).
- **Laser.** L'exemple de `CHUNK_FORMAT.md` (`L#........#L`) contredit sa propre légende (émetteur en col 1 ou 10). B3 utilise `#L~~~~~~~~L#`.

### 6.2 Recommandations (moteur, format, GDD)

1. **Répartition des verbes.** Avec « 2 familles au plus », les paires propres à B3 (eau, lustre, livre, phalène) ne peuvent pas recevoir d'épines, donc restent au bond. Proposition : ne pas compter les épines comme une famille quand elles servent seulement à imposer le verbe (une bande de 2-3 tuiles). Cela rendrait possible un « lustre + bassin » en élan.
2. **Premier cycle.** Aucun P n'est tirable avant 405 m, ni aucun M avant 362 m. Confirmer que l'assembleur se replie proprement sur R/I, ou baisser le seuil.
3. **Format.**
   - Le paramètre de déclenchement d'un livre (`b`) gagnerait un `trig=` : distance, et condition en x (même colonne ou tout le couloir).
   - Les paramètres par rangée (`; …`) ne permettent qu'un objet paramétré par rangée.
   - Une horloge globale (`phase` relative au chunk ou à la tour) est à préciser pour les lustres qui se suivent d'un chunk à l'autre.
   - Les lignes d'en-tête : `#` (exemple) et `//` (texte) cohabitent. B3 utilise `//`.
4. **Chaînes d'intros.** Un champ `apres: b3_lustre_intro` garantirait l'ordre intro → M, au lieu de compter sur les fenêtres `alt`.
5. **Règle des familles entre chunks.** Elle n'est pas définie (deux M lustre d'affilée ?). Une règle « pas deux fois la même famille principale dans un M M » aiderait.
6. **Arène.** La Mère-Phalène (GDD, B3, P1) n'est pas livrée. `b3_p_essaim` et `b3_p_scriptorium` en préparent le vocabulaire.
7. **Mâchoires et contreforts.** Ils sont à modéliser dans le simulateur B3 si le lead veut les y voir.
