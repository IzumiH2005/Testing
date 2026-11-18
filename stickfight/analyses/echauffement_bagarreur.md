# Analyse : échauffement du bagarreur avant le combat

Demande de l'utilisateur : « une animation d'échauffement cette fois (genre il s'échauffe pour se
préparer à combattre) ».

Animation : `anims/echauffement_bagarreur.json`, générée par `tools/gen_echauffement_bagarreur.py`.
Base `garde_ouverte_bagarreur` (lacet +45, la vue du jeu), 100 images (1,7 s à 60 i/s), suivie
de `garde_ouverte_idle_bagarreur`. Elle commence et finit **exactement** sur la garde : on peut
la jouer à la place de la garde au repos, au début d'un round.

Ce qui n'est pas cité vient de la garde (`poses/garde_ouverte_bagarreur.json`) :
spineLow 4, chest 4, neck 3, root −2, torsionBassin (tb) −12, torsion (t) −4 (total −16),
`epauleF_av` −1, `epauleN_av` 0, `epauleF_haut` 1, `epauleN_haut` −3, bassin (0 ; 87).
Jambes : `thighN` −26 / `shinN` 4 / `footN` −16, `thighF` 14 / `shinF` 22 / `footF` 5,5,
`thighN_p` 15, `thighF_p` −15, `thighN_r` −2, `thighF_r` 5. Talon arrière déjà levé (cheville N
à 14,9, pointe à 8,1 ; pied avant à plat, pointe à 8,5).
Bras de garde (élévation / plan / rotation / coude) : N 28,7 / +40 / +19,4 / 136,2 (poing au
menton), F 18,1 / −28,9 / +15,3 / 100 (poing devant, à hauteur de clavicule).
Repère des poings (lacet 0, relatif à l'épaule N, x devant, y haut, z profondeur, N = z < 0) :
garde N (23 ; −4 ; −8), F (38 ; −10 ; 11). Rayon du poing 8,5.

## 1. La logique du mouvement

Un échauffement de combattant, juste avant le combat, n'est pas de la gymnastique : il veut
**se détendre, se mettre en confiance, régler sa distance**, sans quitter sa place ni se
fatiguer. Quatre idées, chacune une pose lisible (BIBLE A6), dans cet ordre :

1. **Il lâche la garde (images 0 à 14).** Les épaules tombent, il expire, les bras descendent
   sous leur poids (ils accélèrent, rien ne les retient), puis pendent, détendus, coudes à peine
   pliés, décollés des cuisses. Les pieds ne bougent pas : il garde sa base de combat.
2. **Il remonte la garde et cogne ses poings l'un contre l'autre (images 14 à 46).** Les bras
   remontent (mi-chemin à 20), garde reprise à 26, puis il carre le buste face à ses poings.
   Geste de confiance (« prêt »). Les deux poings se rencontrent devant le sternum,
   articulations contre articulations, avant-bras presque horizontaux, coudes écartés. Deux
   chocs. Les poings se touchent sans se traverser (centres à 17 = deux rayons, mesuré en 3D).
3. **Il lance deux jabs dans le vide (images 46 à 68),** pour régler la distance : le bras avant
   part de la garde, se tend, revient sur sa ligne. Valeurs du jab de `gauche_droite_bagarreur`
   (§ 4, image 6), mais **moins tordu** (total −32 au lieu de −40) : c'est un coup à vide. Le
   plan du bras est recalé sur cette torsion (poing visé en 3D sur la ligne de garde, plan −40
   trouvé par balayage). La droite reste au menton.
4. **Il se pose (images 68 à 100).** Une inspiration (épaules et poitrine qui montent puis
   redescendent), un hochement de tête, le menton rentre : « prêt ». L'image 100 est la garde au
   chiffre près, l'idle prend le relais.

Ce qu'il ne fait pas : **pas de sautillement** (essayé, puis retiré à la demande de
l'utilisateur), pas de craquement de nuque ni d'épaules roulées (déjà dans
`victoire_bagarreur`), pas de pas.

## 2. Anatomie

| Partie | Articulations et axes | Muscles | Rôle |
|---|---|---|---|
| Ceinture scapulaire, relâché | omoplate loin qui descend (`epauleF_haut` 1 → −3), la proche est déjà au plus bas (−3, limite du rig) ; poitrine 4 → 3, cou 3 → 5 | trapèzes supérieurs relâchés | « laisser tomber les épaules » |
| Épaules, bras ballants | élévation 28,7 / 18,1 → 5 / 5 ; plan → +12 / −12 (bras décollés, anatomie § 4 bis) ; rotation → 0 | aucun actif : la pesanteur | les bras pendent |
| Coudes, bras ballants | 136 / 100 → 23 | biceps et triceps relâchés | « bras morts » |
| Épaules, poings cognés | buste carré (total −8) ; plan : coudes écartés (ecart 30 à 45°) ; rotation qui ramène les avant-bras vers le centre | deltoïdes, pectoraux | met les poings face à face |
| Épaule F, jab | flexion → 90, plan −40 (recalé sur la torsion −32), rotation → +15, coude → 18,5, `epauleF_haut` +3 | deltoïde antérieur, grand pectoral, dentelé, triceps | allonge le bras avant |
| Cou, hochement | flexion 3 → 12 puis retour | fléchisseurs du cou | « prêt » |
| Jambes | celles de la garde tout du long (bassin qui descend de 0,4 au plus au lâcher, genoux qui plient d'un rien) | — | base de combat |

## 3. Phases (60 i/s)

| Images | Phase | Courbe | Pourquoi cette durée |
|---|---|---|---|
| 0 → 6 | les épaules lâchent, il expire | acc | départ lent, puis ça tombe |
| 6 → 14 | les bras tombent (poids) | acc puis dec | 8 images : une chute de bras réelle dure ~0,15 s |
| 14 → 20 | les bras remontent, mi-chemin | dec puis acc-dec | ce qui est tombé s'arrête (A4) avant de repartir |
| 20 → 26 | garde reprise | acc-dec | geste décidé, sans hâte |
| 26 → 28 | les poings se rapprochent, le buste se carre | acc | |
| 28 → 30 | premier choc | acc (arrive vite, s'arrête net, A7) | |
| 30 → 32 | tenue du choc | palier | contact lisible (A7) |
| 32 → 35 | les poings s'écartent de 10 | dec | rebond du choc |
| 35 → 37 | second choc | acc | |
| 37 → 39 | tenue | palier | |
| 39 → 46 | retour à la garde | dec | |
| 46 → 49 | premier jab : départ → bras tendu | dec | 3 images, rapide (A1) |
| 49 → 51 | le bras reste un instant | palier | A4 |
| 51 → 57 | retour, garde à 57 | acc-dec | retour 2 fois plus long que l'aller (A1) |
| 57 → 60 | second jab | dec | rythme « un… un » |
| 60 → 62 | tenue | palier | |
| 62 → 68 | retour, garde à 68 | acc-dec | |
| 68 → 76 | inspiration | acc-dec | il « respire » sa garde |
| 76 → 86 | hochement (menton rentre), il expire | dec | |
| 86 → 94 | retour exact à la garde | dec | |
| 94 → 100 | garde tenue | — | raccord idle |

**Décalage** : seulement `neck` 3. Aucun décalage sur les bras : il retarderait le jab et les
chocs, qui arriveraient coude plié et poings séparés. Garde atteinte à 94 et tenue jusqu'à 100 :
le cou lu à 100 est celui de 97, déjà à 3, le raccord reste exact.

## 4. Poses clés, tous les axes

Lacet +45. Bras notés élévation / plan / rotation / coude. Pour les clés posées par `mains3d`,
la cible des poings est donnée (repère de l'épaule N, lacet 0) ; les angles résultants sont
écrits dans le JSON par `tools/resout_mains.sh`.

Limites du rig rappelées : `epaule*_haut` −3 à +7, `epaule*_av` −7 à +7.

**Image 0 (garde).** Garde, rien ne change.

**Image 6 (épaules lâchées).** Bassin (0 ; 86,6). chest 3, neck 5. Omoplates : `epauleN_haut`
−3, `epauleF_haut` −3, `epauleN_av` 0, `epauleF_av` −1. Bras : encore la garde (le corps lâche
d'abord, les bras suivent). Jambes : garde.

**Image 14 (bras tombés).** Bassin (0 ; 86,4), mêmes buste et omoplates. Bras N : 5 / +12 / 0 /
23. Bras F : 5 / −12 / 0 / 23 (bras ballants, poings le long des cuisses, décollés).

**Image 20 (les bras remontent).** Bassin (0 ; 86,7). Omoplates `epauleF_haut` −2,
`epauleN_haut` −3. Bras N : 18 / +24 / +10 / 90 ; bras F : 14 / −20 / +8 / 80 (coudes décollés,
avant-bras qui montent).

**Image 26.** Garde exacte.

**Image 28 (les poings se rapprochent).** tb −12, t +2 (total −10) ; neck 4, neck_r −3,6.
Poings N (42 ; −12 ; −14,5), F (42 ; −12 ; 14,5) ; `coude_dy` [−4 ; −4], ecart [30 ; 45].
Omoplates : `epauleN_av` 0, `epauleF_av` 0, `epauleN_haut` −3, `epauleF_haut` 1.

**Image 30 (premier choc).** tb −12, **t +4 (total −8)** : il carre le buste pour cogner devant
le sternum. neck 4, neck_r −4,8, regard sur les poings. Poings N (42 ; −12 ; −8,5), F (42 ; −12 ;
8,5) : centres à 17 = deux rayons, face à face sur l'axe de profondeur. Omoplates comme 28.

**Image 32.** Identique à 30. **Image 35 (écart)** : poings N (42 ; −11 ; −13,5), F (42 ; −11 ;
13,5). **Images 37, 39** : comme 30. **Image 46** : garde exacte.

**Image 49 (premier jab tendu).** Bassin x +1,2, y 86,6 ; tb −12, t −20 (total −32) ; buste
droit. Bras F : 90 / −40 / +15 / 18,5 (poing sur la ligne de garde). `epauleF_haut` +3,
`epauleN_av` −1, `epauleF_av` 0. Bras N : garde. neck_r +9,6.

**Image 51.** Identique à 49. **Image 57** : garde. **Images 60 / 62** : comme 49. **Image 68** :
garde.

**Image 76 (inspiration).** Garde, `epauleN_haut` −1, `epauleF_haut` +3,5, chest 6.

**Image 86 (hochement).** Garde, neck 12 (le menton rentre), y 86,2.

**Images 94 et 100.** Garde exacte.

## 5. Ce qui se voit

| Vue | Ce qui doit se lire |
|---|---|
| Face (lacet 90) | les épaules qui tombent ; les deux bras pendent de chaque côté, décollés du buste ; au choc, les deux poings se touchent au milieu de la poitrine, coudes écartés en V |
| Trois quarts (45, jeu) | toute l'animation : la chute des bras, le choc des poings (ils se touchent sans se traverser), les jabs qui partent vers la droite de l'écran, le hochement |
| Profil (0) | le jab tendu à l'horizontale ; au choc, les deux poings superposés devant le sternum (un seul disque visible, c'est attendu) |

## 6. Références

- BIBLE A1 (contraste de vitesse : jab en 3 images, retour en 6), A4 (les bras qui tombent
  s'arrêtent avant de repartir), A6 (une idée par pose), A7 (le choc arrive vite et s'arrête
  net, tenue de 2 images).
- Anatomie § 4 bis (bras ballants).
- `gauche_droite_bagarreur.md` § 4, image 6 (valeurs du jab).
- Observation courante d'un boxeur sur le ring avant la cloche : épaules relâchées, poings
  cognés, un ou deux jabs dans le vide.
- Validé par l'utilisateur en version 5 (sans sautillement).

## 7. Contrôles

1. Image 0 et images 97 à 100 : tous les canaux égaux à ceux de la garde (écart 0), cou décalé
   compris.
2. Pieds : à toutes les images, chaque pointe à sa place de garde (écart ≤ 0,5 relevé au lacet
   45, 8 passes de correction).
3. Choc : distance 3D entre les centres des poings 17 ± 1 aux images 30 à 32 et 37 à 39 ; jamais
   moins de 16 entre 26 et 46.
4. `--verifier` : aucune traversée (mains, avant-bras, bras) ; seuls restent les avertissements
   « bras proche confondu » déjà présents dans la garde.
5. `--vues` sur les clés et `--tour 2` sur les images 14, 30, 49 : les deux poings visibles au
   choc à 45 et de face.
6. Jab à vide (49, 60) : poing F à moins de 2 de la ligne de garde, `foreF` ≤ 20.
7. Bras ballants (14) : aucune main ni avant-bras dans une cuisse ni l'un dans l'autre (plans
   ±12 au moins).
8. Omoplates dans les limites du rig (`epaule*_haut` ≥ −3) ; bagarreur : `epaule*_av` ≤ 0
   partout, buste droit (chest ≥ 3).
