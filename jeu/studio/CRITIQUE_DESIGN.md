# CRITIQUE_DESIGN.md : revue de Milo Hartmann

> Revue de design d'ÉCHO. Documents jugés : `GDD.md` v1.0, `FEEL.md`, `ECONOMY.md` et `CHUNK_FORMAT.md`. Code de référence : `game/scripts/world.gd`, `tower.gd` et `chunks.gd`.
> Méthode : persona Milo 1.2.0 (`design_review_checklist`, `theory_of_fun`, `dominance_analysis`, `complexity_filter`, `concept_to_production`). Chaque point suit la même structure : diagnostic, cause, intention, mécanisme, compromis, modes d'échec, test.
> Je juge, je ne réécris pas. Chaque correction indique **qui** modifie **quel document**.
> Simulations : `/tmp/claude-0/-home-user-Testing/8bb7e1e6-044c-5928-b326-6b9f703cc364/scratchpad/critique/sim.py` et `sim2.py`. Les mesures utilisent un pas fixe de 1/120 s et Euler semi-implicite. Le couloir va de x = 38 à x = 154 (116 px). Une rangée vaut 16 px.

---

## 0. Résumé exécutif

1. **Physique.** Je garde les **arcs du GDD**, qui sont aussi ceux du prototype et du `CHUNK_FORMAT`. J'y ajoute **la couche d'entrée et de clémence de FEEL** (lecture à l'appui, file de taps, buffer, coyote, hitboxes, hitstop court). Je refuse trois éléments de FEEL :
   - la gravité asymétrique ;
   - la glissade qui accélère ;
   - l'interdiction du saut à hauteur variable.

   Les chunks écrits avec la physique du GDD **restent valides**. Il faut seulement que le validateur traite l'Élan comme un intervalle et non comme une valeur.
2. **La promesse « ce qui t'a tué devient cyan » tient sur le papier.** `ECONOMY.md` la casse deux fois :
   - des effets d'écho non cyan (§2.3) ;
   - des tenues en cyan, magenta ou rouge (§2.1).
3. **L'économie a été écrite contre le prototype, pas contre le GDD.** Elle prévoit 3 types de pièges, 19 tenues, 8 reliques payées en éclats, 2 monnaies et une vidéo « +1 vie » en Tour du jour. Il faut **une seule source de vérité**.
4. **Il y a une collision de noms majeure.** « Élan » désigne le saut long dans le GDD et un combo dans FEEL §6. De plus, le GDD a déjà son propre combo, le « Rythme ». Cela donne **deux combos pour un seul jeu à un doigt**.
5. **Le P0 de 15 semaines industrialise des hypothèses non validées**, contre la règle d'or `concept_to_production` : « ne jamais industrialiser une hypothèse non validée ». Je propose un P0 serré d'environ 8,5 semaines, en deux portes de validation.

---

## 1. Arbitrage physique (priorité absolue)

### 1.1 Les deux jeux de valeurs comparés

| Paramètre | GDD §2.2 (= prototype `world.gd`, sauf l'Élan) | FEEL §2.2 à §2.4 |
|---|---|---|
| Pas de simulation | 120 Hz (§0) | Raisonné en « images » de 1/60 s (en-tête) |
| vx / vy initial | 210 / −290 | 232 / −350 |
| Gravité | 700 constante | 960 en montée, 1500 en descente, ×0,45 si \|vy\| < 30 |
| Chute max | 330 | 300 |
| Hauteur variable | **Élan** : g = 300 entre 0,10 et 0,28 s si vy < 0 | **Interdite** (« Pas de saut à hauteur variable », §2.2) |
| Volte | min(vy, −205), une par bond, rechargée par le cyan | min(vy, −220), verrou de 5 i (83 ms) |
| Mur | Accroche 0,22 s, puis glissade à 14 px/s | Accroche 0,30 s, puis glissade de 12 à 48 px/s sur 1,5 s (courbe en carré) |

### 1.2 Résultats de la simulation (pas de 1/120 s, couloir de 116 px)

**Tableau A : bond et Élan**

| Cas | Durée | Gain à l'impact | Rangées | Apex | vy à l'impact |
|---|---|---|---|---|---|
| GDD bond | 0,558 s | **51,2 px** | 3,20 | 58,9 px à 0,41 s | +101 |
| GDD Élan tenu 0,12 s | 0,558 | 54,2 | 3,38 | 60,9 | +94 |
| GDD Élan tenu 0,20 s | 0,558 | 67,3 | 4,21 | 70,2 | +61 |
| GDD Élan complet (≥ 0,28 s) | 0,558 | **76,8** | 4,80 | 77,7 | +31 |
| FEEL bond (120 Hz) | 0,500 | **57,0** | 3,57 | 62,7 à 0,39 s | +119 |
| FEEL bond (60 Hz, pour vérifier son texte) | 0,500 | 50,8 | 3,18 | 61,0 | +159 |

**Tableau B : volte (retour sur le même mur)**

| Volte à | GDD (gain) | FEEL (gain) |
|---|---|---|
| 0,1 s | 43,4 px (2,71 rg) | 50,0 (3,13) |
| 0,2 s | 69,8 (4,36) | 74,0 (4,62) |
| 0,3 s | **83,7 (5,23)** | 84,9 (5,31) |
| 0,4 s | 83,7 (5,23) | 77,8 (4,86) |
| 0,5 s | 69,6 (4,35), retour en 1,0 s | **impossible** : le héros a déjà touché le mur d'en face à 0,500 s |
| Élan + volte à 0,3 s | 91,3 (5,71) | sans objet |

**Tableau C : fenêtres de volte**

| Volte qui remonte de | GDD | FEEL |
|---|---|---|
| ≥ 72 px (≥ 4,5 rangées) | 0,217 → 0,483 s (**0,27 s** de large) | 0,19 → 0,425 s (0,23 s) |
| ≥ 80 px (≥ 5 rangées) | 0,27 → 0,43 s (0,167 s) | 0,24 → 0,38 s (0,14 s) |

**Tableau D : glissade selon le temps passé au mur**

| Au mur pendant | GDD | FEEL |
|---|---|---|
| 1,0 s | 10,9 px | 10,4 px |
| 1,7 s | 20,7 px (1,29 rg) | 31,7 px (1,98 rg) |
| 2,0 s | 24,9 px (1,56 rg) | 45,9 px (2,87 rg) |
| **2,3 s** (attente forcée maximale en B1, soit 0,6 × 3,8 s, GDD §8.4 et §8.6) | **29,1 px (1,82 rg)** | **60,3 px (3,77 rg)** |
| 3,0 s | 38,9 px | 93,9 px |

**Vitesse de montée** (bonds enchaînés avec une réaction de 0,15 s au mur) :
- GDD : 4,52 m/s au bond, 6,78 m/s à l'Élan ;
- FEEL : 5,49 m/s ;
- référence du GDD §8.7 : 3 m/s, attentes comprises.

### 1.3 Lecture du diagnostic

1. **Le temps de traversée et le gain sont presque identiques** : 0,56 s contre 0,50 s, et 51 px contre 57 px.
   - Les chiffres de FEEL (« apex 61 px, gain net 51 px », §2.2) **ne sont justes qu'à 60 Hz**. Mon passage à 60 Hz reproduit exactement apex 61,0 et gain 50,8.
   - Au pas réel du moteur, 120 Hz (GDD §0), le bond de FEEL gagne **+6 px**. FEEL n'est donc pas cohérent avec le moteur qu'il vise.
   - Le GDD n'est pas propre non plus : son §0 annonce un simulateur à 1/240 s, alors que le moteur tourne à 1/120 s. D'où 52 px dans le texte contre 51,2 px mesurés. L'écart est faible, mais il faut corriger le texte.
2. **La sensation « flottant contre net » est presque nulle sur 116 px.**
   - Le temps passé près de l'apex (\|vy\| < 40) est de **0,12 s dans les deux modèles**.
   - La bande d'apex ×0,45 de FEEL ne joue que sur \|vy\| < 30, soit environ 4 ticks.
   - FEEL accepte donc tout le coût de la gravité asymétrique (re-mesurer, re-valider, re-documenter) pour un bénéfice que le joueur ne percevra pas sur un arc de 0,5 s.
   - Persona, `game_feel` : « Ne pas confondre polish et correction d'un mauvais système ». Ici le système n'est pas mauvais. Il n'a pas besoin de cette correction.
3. **La volte de FEEL contredit son propre texte.**
   - FEEL §2.4 promet un « petit rebond de 25 px [qui] sert à esquiver, pas à grimper ». Le calcul 220² / (2 × 960) part d'une vitesse nulle.
   - La simulation donne +50 à +85 px, exactement comme dans le GDD.
   - De plus, la traversée de 0,50 s **tue la volte tardive** (0,5 s), que le GDD §2.2 justifie pour « laisser passer une scie ».
4. **La glissade de FEEL casse le budget d'attente.**
   - Pour une même attente forcée de 2,3 s, le héros perd 3,77 rangées au lieu de 1,82.
   - La formule 158/(v+14) du GDD §8.6, les minuteries des lasers et des mâchoires, et la règle 5 du CHUNK_FORMAT (« on ne peut pas attendre plus de ~2 s ») supposent toutes une glissade de 14 px/s.
   - FEEL justifie son choix par « rester au mur ne coûte rien (la marée monte de 9 à 30 px/s) » (§1). Ce diagnostic porte sur le **prototype**. Dans le GDD, c'est la marée plafonnée par biome (28 à 58 px/s) qui fait le mécanisme d'arrêt (Stopping Mechanism). Le problème que FEEL corrige n'existe plus.
5. **L'Élan n'est pas négociable.**
   - FEEL l'interdit au nom du « contrôle à un doigt ».
   - Or tenir le doigt posé n'est pas un deuxième input : c'est le prolongement du tap. Le conflit avec la volte n'existe pas, car la volte se déclenche à l'**appui** suivant, pas au maintien.
   - L'Élan est la seule décision verticale du jeu (GDD §2.1). Le supprimer ramène le jeu au prototype : une seule action par mur, ce que le `mastery_problem_detector` signale comme une maîtrise trop vite plafonnée.
6. **Compatibilité avec les rangées de 16 px.**
   - GDD : 3,2 rangées au bond, 4,8 à l'Élan et 5,2 à la volte optimale. Les trois hauteurs « canoniques » du GDD §2.3 (+3, +5, +5 à 6) tombent bien.
   - FEEL : 3,57 rangées au bond. Le héros arrive à mi-rangée, l'endroit le pire pour placer des épines à la tuile près.

**Correction à porter dans le GDD §2.3 : l'Élan est une rampe, pas un interrupteur.**

| Durée de maintien | 0,10 s | 0,13 s | 0,15 s | 0,18 s | 0,22 s | 0,25 s | ≥ 0,28 s |
|---|---|---|---|---|---|---|---|
| Gain | 51,2 | 55,6 | 58,4 | 63,7 | 69,7 | 73,9 | 76,8 |

Un joueur peut donc atterrir **n'importe où entre 51 et 77 px**. Le validateur (GDD §8.4) doit vérifier que la route reste sûre **pour tout l'intervalle**, ou bien qu'une sous-plage d'au moins 0,05 s de maintien reste sûre. Il ne doit pas tester seulement les deux bornes.

### 1.4 Valeurs finales recommandées (un seul jeu)

**Arcs : GDD, inchangés**

| Paramètre | Valeur |
|---|---|
| Pas de physique | 120 Hz, `physics_ticks_per_second = 120` |
| GRAV | 700 px/s² |
| JUMP_VX / JUMP_VY | 210 / −290 |
| MAX_FALL | 330 |
| TURN_VY | −205, appliqué en `vy = min(vy, −205)` ; une volte par bond, rechargée par le cyan (GDD §3.2) |
| Élan | zone morte 0,10 s ; g = 300 entre 0,10 et 0,28 s, seulement si vy < 0 |
| Accroche / glissade | 0,22 s, puis 14 px/s constante |

**Entrée et clémence : greffées de FEEL et unifiées en secondes**

| Règle | Valeur | Origine |
|---|---|---|
| Lecture du tap | à l'**appui** (`pressed == true`), mis en file et consommé dans `_physics_process` ; `input/agile_event_flushing = true` | FEEL §2.1 |
| Tap avant le mur, qui devient un bond | **0,08 s** (10 ticks, ≈ 17 px). Une seule fenêtre ; elle remplace les « 4 i » de FEEL | GDD §2.2 |
| Buffer général | **0,10 s** (12 ticks) | compromis entre 0,08 s (GDD) et 117 ms (FEEL) |
| Coyote de mur | 0,10 s | GDD = FEEL |
| Verrou anti-rebond du doigt après un bond | **0,05 s** (6 ticks), et non 83 ms : on garde la volte à 0,1 s du GDD (43 px), qui est utile | FEEL §2.4, réduit |
| Hurtbox | **6 × 10**, décalée de 1 px vers le bas ; dans le code `HALF = Vector2(3, 5)` au lieu de (4, 6) | GDD §0 |
| Épines | profondeur 5 px, zone de h − 6 | FEEL §2.6 |
| Scie | rayon létal 5 px | FEEL §2.6 |
| Laser | \|dy\| < **6 px**, létal seulement après 3 ticks actifs (le code dit 8, le CHUNK_FORMAT dit < 5) | FEEL §2.6 |
| Mort par la marée | centre du héros 2 px sous la crête | FEEL |
| Frôlé | ≤ 3 px | GDD §2.2 |
| Hitstop | 0 sur toute action du joueur ; **0,10 s à la mort** (et non 0,18 s) | FEEL §3.2 |

**Refusés** : gravité asymétrique, bande d'apex, vx 232 et vy −350, glissade accélérée, accroche de 0,30 s, TURN_VY −220, interdiction de la hauteur variable.

**Test A/B facultatif, après la tranche verticale seulement** : passer g_down à 900 (gravité plus lourde en descente).
- Effet mesuré : bond 49,1 px (−2 px, même rangée), Élan 76,6, volte à 0,5 s 64,7 px au lieu de 69,6.
- C'est le seul « crisp » compatible avec les chunks.
- Je l'ai testé en hybride (vy −310, g 760/1000, apex ×0,6). Il **déplace** les arcs : bond 55,7, Élan 79,8, volte 87,6. **Rejeté.**

**Casse-t-on les chunks déjà écrits ? Non.**
- Il n'existe encore aucun fichier dans `game/chunks/` ; les seuls chunks sont les exemples du GDD §8.1 et du CHUNK_FORMAT.
- Tous ont été pensés avec les arcs du prototype, qui sont conservés.
- Le seul changement qui touche les chunks est le passage à une hurtbox plus petite (6 × 10 au lieu de 8 × 12). Il ne fait qu'**élargir** les marges : tout chunk validé reste valide.

*Mode d'échec à surveiller* : la réduction de la zone morte de l'Élan.
- À 0,12 s, l'Élan complet tombe à 73,9 px.
- Toute retouche de la zone morte modifie donc la hauteur atteinte, et l'intervalle du validateur doit être recalculé.
- Je recommande de geler la zone morte à 0,10 s.

---

## 2. Cohérence entre documents : contradictions et arbitrage

Légende : **S** sévère (casse la promesse ou le code), **M** moyen, **m** mineur. La colonne « Corrige » donne le document à modifier, par son auteur.

### 2.1 GDD contre FEEL (physique et ressenti)

| # | Sujet | GDD | FEEL | Arbitrage | Corrige | Sév. |
|---|---|---|---|---|---|---|
| 1 | Unité de temps | 120 Hz (§0) ; simulateur à 1/240 s | « images » de 1/60 s | Tout en **secondes et ticks à 120 Hz**. FEEL convertit ses « i » ; le GDD §0 corrige la mention 1/240 | FEEL, GDD | M |
| 2 | Hauteur variable | Élan en P0, « ne jamais couper » (§13) | « Pas de saut à hauteur variable » (§2.2) | **Élan conservé** (voir §1.3, point 5) | FEEL | S |
| 3 | Arcs | 210 / −290 / 700 | 232 / −350 / 960 / 1500 / apex | Arcs du **GDD** (voir §1) | FEEL | S |
| 4 | Mur | 0,22 s puis 14 px/s | 0,30 s puis 12 → 48 px/s | **GDD** (le budget d'attente du §8.6 en dépend) | FEEL | S |
| 5 | Nom « Élan » | Saut long | Combo de flow (§6) | Le mot **Élan** reste au saut long. FEEL §6 est renommé et **fusionné avec le Rythme** du GDD §2.4 (voir §3.7) | FEEL, GDD | S |
| 6 | Deux combos | Rythme : moins de 0,30 s au mur ; paliers 10/20/30 | Élan-combo : 18 i ; paliers 5/15/30/50 ; encaissement après 0,9 s ou 24 px | **Un seul combo, « Rythme »** : paliers 10/20/30 ; chaîne cassée après 0,30 s d'accroche (= 0,22 s d'accroche + 0,08 s de glissade, cohérent avec le GDD) ; encaissement à la rupture, perdu à la mort | FEEL, GDD, ECONOMY | M |
| 7 | Volte | −205 | −220, « 25 px » | **−205**. La phrase « 25 px » est fausse (+50 à +85 px mesurés) | FEEL | M |
| 8 | Verrou de volte | aucun | 83 ms | **0,05 s** | FEEL | m |
| 9 | Tap avant le mur | 0,08 s ≈ 17 px | 4 i ≈ 15 px | **0,08 s** | FEEL | m |
| 10 | Buffer | 0,08 s | 7 i = 117 ms | **0,10 s** | les deux | m |
| 11 | Hitstop de mort | 0,18 s (§2.4, §3.3, code) | 100 ms | **0,10 s** | GDD | M |
| 12 | Séquence de mort | 1,51 s (§3.3) | ≈ 1920 ms, puis un tap, puis 300 ms de taps ignorés (§4.1) | **≤ 1,5 s jusqu'à l'écran de vie** ; gravure **passable d'un tap** après la 3ᵉ fois qu'on la voit (voir §3.6) | FEEL | M |
| 13 | Laser | < 5 | < 6 après 3 i | **< 6 après 3 ticks** | GDD §4.3 O8, CHUNK | m |
| 14 | Scie | 6 | rayon 5 | **5** | GDD | m |
| 15 | Frôlé | 3 px | 4 px | **3 px** | FEEL | m |
| 16 | Hitbox | 6 × 10 (doc), mais 8 × 12 dans le code (`HALF = Vector2(4,6)`) | 6 × 10 | **6 × 10**. Le code est à aligner (ticket pour le dev) | code | M |
| 17 | Palette | lettres de `palette_v2.txt` ; danger magenta ; [W] blanc | lettres de `tools/palette.txt` (x X z Z danger ; q t c e cyan) | **Une seule palette de référence.** FEEL cite les mêmes rôles avec d'autres lettres, ce qui obligerait le dev à traduire | FEEL ou ART | M |
| 18 | Musique | tempo par biome | 96 → 120 BPM selon la hauteur | Un seul modèle. En P0 : **une boucle par biome + une couche « marée »** (voir §5) | FEEL | m |

### 2.2 GDD contre CHUNK_FORMAT (et `chunks.gd`)

| # | Sujet | Écart | Arbitrage | Sév. |
|---|---|---|---|---|
| 19 | En-tête | Le GDD §8.1 écrit `h:` et `alt_min/alt_max` ; le CHUNK_FORMAT écrit `alt: 22-150`, sans `h` | `chunks.gd` lit **les deux** formes d'altitude et calcule la hauteur depuis la grille. Le CHUNK_FORMAT fait foi ; le GDD §8.1 retire `h:` | m |
| 20 | Tension | GDD : R, M, P. CHUNK ajoute I (introduction) et A (arène) | Ajouter I et A au GDD §8.2, et dire comment l'assembleur les traite (§8.3, étape 3 : I = créneau d'introduction) | m |
| 21 | Herse | `h` dans la légende du GDD, `H` dans le CHUNK (`VALID` de `chunks.gd` ne contient que `H`) | **`H`** | M (bug de chargement silencieux) |
| 22 | Symboles | Le CHUNK ajoute `C b : A R` | Les reporter dans la légende du GDD §8.1 | m |
| 23 | Marée | GDD et CHUNK : 10 + 0,35 t, avec un plafond par biome. Code : min(9 + 0,30 t, 30) + 0,02 × (best − 150) | **GDD**. Le terme en fonction du record est à retirer : il punit le progrès et rend la graine du jour inéquitable selon le joueur | M |
| 24 | Attente | CHUNK : « pas plus de ~2 s ». GDD §8.6 : budget de 3,8 s en B1, attente forcée ≤ 0,6 × budget = 2,3 s | Le CHUNK reprend la règle du GDD **par biome** (2,3 / 2,0 / 1,7 s …) | m |
| 25 | Hurtbox du laser | CHUNK : < 5 | 6 (voir #13) | m |

### 2.3 GDD contre ECONOMY (le plus grave)

`ECONOMY.md` a été rédigé contre le **prototype** : 3 pièges, `tower.gd` procédural, 4 « étages ». Il ne connaît pas les 22 obstacles, les 6 biomes, les chunks ni les tenues du GDD.

| # | Sujet | GDD | ECONOMY | Arbitrage | Sév. |
|---|---|---|---|---|---|
| 26 | Tenues | 24 silhouettes ; « Veilleur » de départ ; **l'écharpe reste dans la rampe corail** (§9.3) | 19 changements de palette ; « corail » de départ ; « echo » `#34e0e0`, « prune » `#e056fd`, « braise » `#ff4d2e`, « gardien » à liseré cyan | **GDD.** Interdire au héros le cyan (couleur de l'écho et du sûr), le magenta (danger) et le rouge vif. Cela découle de la règle 4 de FEEL | **S** |
| 27 | Effets d'écho | écho cyan à ±15° de teinte (§9.2) | améthyste, or, givre… recolorent l'écho **et le piège gravé** (§2.3) | **Supprimer.** La règle « ce qui t'a tué devient cyan » est **le jeu**. Un piège gravé en améthyste ne se lit plus comme sûr ; un piège gravé en or se confond avec les éclats | **S** |
| 28 | Reliques | 12, obtenues par fragments, ≤ 10 %, emplacements aux niveaux 5/15/30, « jamais payantes » (§9.4) | 8, **achetées en éclats**, ≤ 20 %, emplacements aux niveaux 8/25 ; Sablier (marée retardée de 2 à 4 s), Lanterne (+0,2 s d'alerte laser) | Garder le principe du GDD. Les éclats viennent jusqu'à 31 % de la pub, donc **la pub achète indirectement de la puissance**, ce qui contredit ECONOMY §5, point 7 (« ni relique »). Reliques en **P1**, par fragments uniquement | **S** |
| 29 | Noms | power-ups « Lanterne » et « Aimant » | reliques `r_lantern`, `r_magnet` ; tenue « lanterne » | Un nom = une chose. Renommer les reliques | M |
| 30 | « +1 vie » | une fois par ascension, **jamais en Tour du jour ni en défi** (§10.1) | autorisée en Tour du jour, le partage affichant « 5 vies » (§4.1, ligne 1) | **GDD.** Le Tour du jour est un classement social ; une vie payée en attention le fausse | **S** |
| 31 | Volume de pub | 4 placements, **6 vues par jour max** | 5 placements en P0, plafonds qui totalisent 15 par jour | **GDD : 3 placements en P0, 6 par jour** (voir §4) | M |
| 32 | Monnaies | une seule | Éclats + Prismes | **Une seule en P0.** Le Prisme répond à un risque (« la pub achète tout ») que le GDD traite déjà en ne vendant que des cosmétiques. Revoir en P1 si les mesures le justifient | M |
| 33 | XP | 200 + 60n, total 83 300 ; +10 par gravure, +25 par boss | 100 + 40(L−1), total 51 940 ; +5 par gravure, +10 par record | Une seule courbe. Je préfère **celle d'ECONOMY**, simulée sur 30 jours (niveau 50 vers J55-J60), à condition de la recaler sur les sources du GDD | M |
| 34 | Déblocages par niveau | 3 codex, 5 relique, 8 Zen, 10 hebdo | 3 traînées, 5 hebdo, 8 relique, 10 effets d'écho, 12 sanctuaire, 15 missions dures, 25 relique 2 | À refaire après la coupe du P0 (§5) | M |
| 35 | Taille des puits | §9.1 ≈ 18 000, mais §9.3 dit 11 700 ou 13 500 | ≈ 99 000 + 300 P | Le GDD est faux contre lui-même. ECONOMY donne environ 6 mois d'objectifs pour un jeu dont le P0 contient 2 biomes. Ramener le catalogue P0 à environ 15 000 éclats | M |
| 36 | Revenus par ascension | ≈ 90 | 0,30 × m + 12 | Formule d'ECONOMY (elle suit la hauteur), recalée pour que le joueur médian obtienne ≈ 90 | m |
| 37 | Missions et codex | 22 obstacles, 6 biomes | missions et codex 16 = 4 pièges × 4, « étages », modificateurs « Lasers seulement » | **À réécrire contre le GDD** | M |
| 38 | Défi hebdo | niveau 10, P1, 8 mutateurs | niveau 5, bronze/argent/or, 5 modificateurs dont « Sans demi-tour » | P1. « Sans demi-tour » rend impossibles les chunks `verbe: volte` : à interdire ou à filtrer à l'assemblage | M |
| 39 | Série du Tour du jour | 5 + 5 × série, plafond 35, remise à zéro | 10 + 5 × min(s, 8), divisée par 2 si un jour est manqué, gel hebdomadaire, rallumage payant | **ECONOMY** pour la clémence (moitié + gel). En revanche, **supprimer « rallumer la série »** pour 150 éclats ou une vidéo (voir §4.3) | M |
| 40 | `tower.gd` | remplacé par les chunks | ECONOMY §7 demande des changements dans `tower.gd` | Supprimer ECONOMY §7, ou le reporter sur `chunks.gd` et l'assembleur | m |
| 41 | Conversion du combo de FEEL | — | jamais chiffrée (FEEL §6.1 : « à valider avec le poste économie ») | Avec le combo unique (#6), le GDD fixe +2/+4/+6 aux paliers | m |
| 42 | Auteur | le GDD est signé « Milo » comme directeur, et ECONOMY aussi | — | Un relecteur ne peut pas valider ce qu'il a signé. Ce document juge les deux **sur pièces**, et la direction doit nommer un propriétaire par document | m |

### 2.4 Incohérences internes au GDD

| # | Écart | Correction |
|---|---|---|
| 43 | §13 annonce « 14 obstacles » en P0 ; la coupe de secours n°2 en garde 10. Ce n'est pas une contradiction, mais c'est le signe que le P0 n'est pas stable | Voir §5 |
| 44 | §9.1 : puits ≈ 18 000 ; §9.3 : 11 700 ou 13 500 | Recalculer |
| 45 | §3.4 : « 4 gravures directes (3 sans pub) ». Le décompte suppose la vidéo « +1 vie » ; or celle-ci n'existe pas en Tour du jour | Écrire « 3 gravures (4 avec la vie vidéo, hors Tour du jour) » |
| 46 | §2.3 : bond 0,554 s / +52 px, mesuré à 1/240 s | 0,558 s / +51 px à 120 Hz : mettre à jour avec les mesures de ce document |

---

## 3. Revue Milo du cœur du jeu

### 3.1 Boucles

| Boucle | Contenu | Verdict |
|---|---|---|
| **5 s** | Lire le mur d'en face, choisir bond, Élan ou volte, toucher, rebondir | **Bonne.** Trois réponses à une seule question (« où j'atterris ? »), avec un seul geste. C'est la compression que décrit Koster (ch. 7 et 8). |
| **1 min** | Une vie : monter, mourir, voir le piège graver, recommencer avec une route plus ouverte | **Excellente, c'est l'idée du jeu.** L'échec produit du progrès visible, donc pas de vie « pour rien ». |
| **5 min** | Une ascension (4 vies) : gérer ses gravures, décider des morts tactiques, battre son record | **Bonne, si les gravures restent rares** (3 par ascension, §3.4). |
| **1 jour** | Tour du jour, 3 missions, coffre, série | **Fonctionnelle mais générique.** Elle n'utilise pas l'écho. Le **partage du Tour du jour, qui montre où l'on est mort** (une carte des gravures, à la Wordle), est la seule boucle de jour propre à ÉCHO. C'est elle qu'il faut soigner, pas le calendrier. |

### 3.2 La promesse de l'écho tient-elle ?

**Oui, à trois conditions.**

1. **La couleur cyan est sacrée.** Elle ne sert ni aux tenues, ni à l'or des éclats, ni à des effets cosmétiques (voir #26 et #27). C'est la seule correction non négociable du dossier.
2. **La gravure doit être une décision, pas une remise.**
   - La « mort tactique » du GDD §3.2 est le meilleur choix du jeu : une vie contre un passage.
   - Elle ne vaut que si les vies sont rares. Chaque vie vidéo, chaque Burin, chaque bouclier `echo_shield` (ECONOMY, emplacement 6) dévalue cette décision.
   - `dominance_analysis` : si mourir sur le pire piège est toujours la bonne réponse, la décision devient un non-choix. Parade : la gravure ne vaut que pour **l'instance**. Le même type de piège plus haut reste létal, et les chunks P et M en contiennent plusieurs.
3. **La recharge cyan doit produire des routes.** Sinon le cyan ne fait que retirer de la difficulté.
   - Le validateur doit compter **au moins un chunk par biome où la seule route optimale passe par un cyan** (un fantôme ou un éclat d'écho).
   - Sans cela, la recharge est une règle qui ne paie pas son coût cognitif. `complexity_filter` : « Une nouvelle règle doit justifier son coût cognitif par un nouveau pattern, une nouvelle décision ou une nouvelle forme de maîtrise. »

**La règle du complice est le point faible.**
- Graver un givre, un cristal, un vent ou une paroi qu'on a touchés dans la seconde qui précède la mort : c'est juste, mais le joueur ne le **lit** pas. Il voit un objet changer sans avoir compris pourquoi.
- En P0, limitez-la **à la paroi friable (O11)**, le seul cas où la cause est évidente (« c'est le sol qui a cédé »).

### 3.3 Le jeu crée-t-il l'envie d'y revenir ? Pourquoi

Il y a quatre moteurs, classés par force :

1. **Le progrès dans l'échec.** La mort rapporte une gravure, un éclat d'écho et un fantôme : « encore une vie, ça va passer ». C'est le moteur le plus fort, et il est sain.
2. **La graine identique pour les 4 vies** (GDD §8.3). On apprend une tour, et pas un tirage au hasard. C'est le bon usage de l'aléatoire, « sur les entrées et pas sur les sorties » (persona).
3. **Le partage du Tour du jour.** Comparaison sociale et rendez-vous quotidien.
4. **La méta** (niveaux, tenues). C'est le moteur le plus faible et le plus coûteux. À ne pas surinvestir en P0.

**Le risque est l'ennui expert.** Le GDD §8.7 prévoit 8 à 12 minutes par ascension pour un expert. Au-delà de 1250 m, il faut que la tour **change** (P2 « remix »). Sans cela, l'heuristique du SKILL s'applique : « ennuyeux après quelques parties → stratégie dominante ».

### 3.4 Décisions intéressantes par seconde

- Rythme mesuré : un mur toutes les 0,56 s, plus environ 0,15 s de réaction. Cela fait **1,3 à 1,4 décision par seconde**, chacune à 3 options (bond, Élan, volte).
- S'y ajoute une décision de **timing**, analogique : la durée de l'Élan et l'instant de la volte. La fenêtre utile de la volte fait 0,27 s (Tableau C).
- C'est **dense mais lisible**, à condition que le chunk montre les deux murs à l'avance.
- La caméra place le héros à y = 220, donc 220 px visibles au-dessus, soit 13,75 rangées, soit environ 4 bonds d'avance. C'est suffisant.

**Point faible : les chunks R** (repos).
- Si un chunk R ne pose **aucune** question (D ≤ 1 et seulement des éclats), on enchaîne 4 à 5 bonds sans décision.
- Exigez que chaque chunk R ait **une** décision sans risque : par exemple un éclat accessible uniquement à l'Élan, ou un raccourci par la volte.

### 3.5 Stratégies dominantes (`dominance_analysis`)

| Candidat | Analyse | Parade |
|---|---|---|
| **Toujours tenir l'Élan** | +50 % de gain (76,8 contre 51,2 px), +50 % de vitesse (6,78 contre 4,52 m/s), coût nul. Il atterrit presque à l'apex (vy +31), donc plus précisément. **Meilleure réponse par défaut.** Les zones sûres réparties 40/40/20 (GDD §2.3) ne sont qu'une intention | Le validateur **compte** les verbes : dans tout chunk M ou P, la zone d'atterrissage de l'Élan complet (+4,8 rangées) doit être **létale au moins une fois sur trois** au-dessus de 150 m. Mesurer en playtest la part d'Élans complets : si elle dépasse 60 %, le jeu a un verbe de trop |
| Mort tactique systématique | Possible si le premier piège dur d'une ascension se grave toujours | La gravure ne vaut que pour l'instance (§3.2) ; 3 vies |
| Camper le mur | Coûte 14 px/s, et la marée monte | Le mécanisme d'arrêt est la marée : pas de changement |
| Suivre son fantôme | Résonance en P1 : c'est un défi, pas une domination | Rien |
| +1 vie vidéo systématique | ECONOMY en estime l'acceptation à 25 % : c'est donc une béquille, pas une domination | Une fois par ascension, hors Tour du jour |

### 3.6 Frustration

| Source | Gravité | Correction |
|---|---|---|
| Séquence de mort de 1,5 à 2,3 s, répétée environ 4 fois par ascension | **Élevée.** Elle rompt le « encore une » | ≤ 1,5 s jusqu'à l'écran de vie ; gravure accélérable au tap après 3 visionnages ; mort par la marée en 0,8 s (pas de gravure) |
| Volte perdue juste avant le mur | Élevée au prototype (GDD §2.2) | Fenêtre de 0,08 s qui transforme le tap en bond (§1.4) |
| Mourir d'un pixel | Moyenne | Hurtbox 6 × 10 ; laser < 6 après 3 ticks ; scie de rayon 5 |
| Mur de 0,6 × budget | Moyenne | Une barre de minuterie visible sur les lasers et les mâchoires (préavis de 0,7 s, CHUNK_FORMAT) |
| La glissade qui accélère (FEEL) | Elle aurait été élevée | Refusée |

### 3.7 Lisibilité sur téléphone

- L'écran logique fait 192 × 352, mis à l'échelle ×3 ou ×4 : c'est bon.
- La hurtbox de 6 × 10 sous le pouce : le pouce masque la moitié basse (GDD §2.1), et le héros est à 62 % de la hauteur. Bon choix.
- **Deux combos (Rythme et Élan-combo) avec badges, traînées et couches musicales** : trop de signaux pour un jeu à 1,4 décision par seconde.
  - FEEL §6.2 prévoit 4 paliers de traînée en `R/r/n`, sous les pièges.
  - Je garde **un seul combo** et **une seule traînée**, jamais en cyan, magenta ou rouge.
- `game_ui_modes` : « Éviter que le même input produise des actions totalement différentes sans signal contextuel clair ».
  - Le tap fait un bond au mur et une volte en l'air. C'est acceptable parce que **l'état est visible** (accroché ou en vol).
  - En revanche, l'indicateur « volte disponible » est indispensable. Je propose l'étincelle [G] ou [c] du GDD §2.4, **affichée en continu** sur le héros quand la volte est chargée, et pas seulement au moment de la volte.

### 3.8 Complexité à couper (`complexity_filter`)

| Règle | Coût | Rapporte | Décision |
|---|---|---|---|
| Combo Élan de FEEL (§6) | élevé : un second combo, des points, un encaissement | doublon du Rythme | **Fusionner** dans le Rythme |
| Règle du complice étendue (givre, cristal, vent) | moyen | lecture faible | **P0 : paroi friable seulement** |
| Résonance | moyen | défi pour experts | P1 (déjà prévu) |
| Prismes | élevé : 2 monnaies | garde-fou déjà assuré autrement | **Retirer du P0** |
| Reliques | élevé : puissance, emplacements, équilibrage | profondeur faible | **P1, par fragments** |
| Effets d'écho | — | **négatif** (ils cassent la promesse) | **Supprimer** |
| Traînées (10) | faible | cosmétique | P1 |
| Sanctuaire | élevé | faible | P2 |
| Musique adaptative à stems (FEEL §7) | élevé en production | moyen | P0 : une boucle par biome + une couche « marée » |

*Persona, `not_allowed`* : « confondre complexité et profondeur » ; « ajouter des mécaniques pour masquer un mauvais core loop ». Le cœur d'ÉCHO est bon : il n'a pas besoin d'être masqué.

---

## 4. Économie et monétisation

### 4.1 Désirable sans être nécessaire ?

| Placement | Désirable ? | Nécessaire ? | Verdict |
|---|---|---|---|
| +1 vie (hors Tour du jour) | oui : une 5ᵉ vie, c'est une gravure de plus | non | **Garder** |
| ×2 butin d'ascension | oui | non | **Garder** |
| ×2 coffre du jour | oui | non | **Garder** |
| Relance de mission | faible | non | P1 |
| Essai de tenue | faible, et il habitue à payer pour du cosmétique | non | P1, à tester en A/B |
| `echo_shield` | **dangereux** : il dévalue la gravure, cœur du jeu | il le deviendra si le jeu est réglé avec ce bouclier en tête | **Refuser** |
| `streak_rekindle` | il joue sur la peur de perdre (aversion à la perte) | — | **Refuser** (gel gratuit seulement) |

**P0 : 3 placements, plafond total de 6 vues par jour.**

### 4.2 1,96 vue par DAU est-il crédible ?

ECONOMY §4.1 calcule :
- +1 vie : 0,62 (2,5 offres × 25 %) ;
- ×2 butin : 0,76 (2,8 × 27 %) ;
- coffre : 0,40 ;
- relance : 0,10 ;
- essai de tenue : 0,08.

Total : 1,96.

**C'est optimiste.**
- Les 2,5 à 2,8 offres par DAU supposent 2,5 à 3 ascensions par jour **pour chaque DAU**. Or la moyenne d'un jeu casual inclut beaucoup de sessions uniques. Avec 1,8 ascension par jour, et après retrait de la relance et de l'essai, la somme tombe à ≈ 1,2-1,3.
- Le coffre à 0,40 par DAU suppose que 40 % des DAU ouvrent le coffre **et** regardent la vidéo.
- Le taux de 25 à 27 % d'acceptation est plausible pour la vie et le ×2. Les références publiques pour des vidéos récompensées bien placées se situent autour de 20 à 30 % d'acceptation par offre ; c'est une fourchette indicative, à mesurer.

**Fourchette réaliste : 1,2 à 1,6 vue par DAU.**
- Avec un eCPM effectif de 12,5 $ (pays à fort eCPM), l'ARPDAU vaut 0,015 à 0,020 $. Il faut alors **≈ 100 000 à 130 000 DAU** pour 2 000 $ par jour, et non 82 000.
- Avec le « mix réaliste » d'ECONOMY (7,75 $), on passe à 160 000 à 215 000 DAU.
- ECONOMY admet une LTV ≈ 0,16 $ par installation, donc **pas d'acquisition payante**. L'objectif de 2 000 $ par jour du BRIEF repose donc entièrement sur l'organique (partage, store).

Ce n'est pas un défaut de design, mais **la direction doit le savoir**. La seule réponse de design est la boucle de partage (§3.1). C'est une raison de plus pour la placer en tête du P0.

### 4.3 Éthique et risques Google Play / AdMob

| Risque | Source | Gravité | Correction |
|---|---|---|---|
| Vie vidéo dans un mode **classé** (Tour du jour) | ECONOMY §4.1, ligne 1 | Élevée (équité, image) | Interdire, comme le GDD §10.1 |
| La pub achète indirectement de la puissance (éclats → reliques Sablier ou Lanterne) | ECONOMY §2.4 + 31 % d'éclats venus de la pub | Élevée (contredit §5, point 7) | Reliques par fragments, en P1 |
| « Rallumer la série » contre une vidéo | ECONOMY §3.3 | Moyenne (motif de type dark pattern, aversion à la perte) | Supprimer ; garder la moitié + le gel gratuit |
| 15 vues par jour plafonnées | ECONOMY §4.1 | Moyenne (fatigue, et l'impression d'un jeu « à pubs ») | 6 par jour (GDD) |
| Programme Familles : un personnage mignon et une palette vive peuvent « attirer les enfants » | positionnement | Élevée si ce n'est pas tranché | **Décider « 13 ans et plus, non destiné aux enfants »** dans la console. AdMob : `tag_for_under_age_of_consent` selon le pays, contenu des annonces plafonné à **G/PG** |
| Consentement | ECONOMY §5 (UMP/TCF) | Moyenne | UMP pour l'EEE et le Royaume-Uni, **et** messages pour les réglementations des États américains (UMP les gère) ; formulaire Data safety : **identifiant publicitaire collecté et partagé** avec AdMob |
| Récompense non livrée en cas d'échec de la vidéo | — | Moyenne (avis négatifs) | Livrer la récompense si la vidéo échoue après le clic (une fois par jour) |
| Pub proposée après une mort, au moment de la frustration | +1 vie | Faible à moyenne | Bouton secondaire, jamais par défaut, masqué après 2 refus (ECONOMY le prévoit, c'est bien) |

Les garde-fous d'ECONOMY §5 sont **bons** : pas de loot box, pas d'interstitielle, notifications seulement sur opt-in, ton neutre. Le défaut est que le document les viole lui-même dans ses tableaux (#28, #30 et `streak_rekindle`).

---

## 5. Périmètre : un P0 plus serré

**Diagnostic.**
- Le P0 du GDD §13 représente 73 jours, soit environ 15 semaines. Il comprend 14 obstacles, 3 biomes, un boss, 90 chunks, 30 succès, un codex et 16 tenues.
- Il fabrique du contenu **avant** d'avoir validé le cœur. Règle d'or `concept_to_production` : « Ne jamais industrialiser une hypothèse non validée ».
- Le `prototype_mindset` interdit aussi d'« ajouter du contenu pour régler un problème systémique ».
- Or l'Élan, la recharge cyan et le budget d'attente sont **des hypothèses**.

**Proposition : 42 jours, soit environ 8,5 semaines, en deux portes (`production_gates`).**

| Rang (impact sur le plaisir et l'envie de revenir) | Lot | Jours |
|---|---|---|
| 1 | **Physique 120 Hz + couche d'entrée** (§1.4), Élan, volte, recharge cyan, hurtboxes | 4 |
| 2 | **Cœur de l'écho** : gravure, éclat d'écho, 3 fantômes, complice limité à la paroi friable, Burin | 3 |
| 3 | **Chunks** : chargeur (existe déjà), assembleur, validateur à intervalle d'Élan, robot sur 12 graines | 7 |
| — | **PORTE 1 (fin de la semaine 3)** : tranche verticale B1 avec 15 chunks. Test à l'aveugle sur 5 joueurs. Critères : « encore une » spontané chez au moins 4 sur 5 ; Élan complet < 60 % ; cyan utilisé comme route au moins une fois par ascension | — |
| 4 | **B1 Crypte + B2 Fonderie**, 9 obstacles (O1, O2, O3, O4, O5, O8, O9, O10, O11), environ 60 chunks | 13 (art compris) |
| 5 | **Ascension 0** (onboarding sans texte, fantôme-guide) | 3 |
| 6 | **Tour du jour + partage** façon Wordle (carte des gravures) + série clémente | 3 |
| 7 | **Méta minimale** : une monnaie ; 8 à 10 tenues (écharpe corail) ; 3 missions par jour ; niveaux 1-20 | 4 |
| 8 | **Pub** : 3 placements, UMP, Data safety | 2 |
| 9 | **Juice de base** : hitstop, secousse, séquence de mort ≤ 1,5 s, environ 12 sons, une boucle musicale par biome + couche « marée » | 3 |
| — | **PORTE 2** : test fermé Play Console sur 20 à 50 testeurs, 14 jours. Mesures : rétention à J1 et J7, vues par DAU, part de l'Élan | — |

**Total : 42 jours.**

**Repoussé en P1, par ordre de retour** :
1. B3 (avec O6, O12, O18, O19) ;
2. le boss Sonneur (P0 garde une arène de runes **sans** boss si le temps le permet) ;
3. Plume et Accalmie ;
4. codex ;
5. 30 succès ;
6. reliques (fragments) ;
7. défi hebdo ;
8. relance de mission par vidéo ;
9. traînées ;
10. Résonance ;
11. musique à stems ;
12. Zen.

**Repoussé en P2** : sanctuaire, Prismes (si les mesures le justifient), effets d'écho (uniquement des variantes **cyan**).

**Supprimé** : effets d'écho non cyan, `echo_shield`, `streak_rekindle`, combo Élan de FEEL (fusionné).

**Pourquoi c'est réaliste.**
- On garde les deux biomes que le GDD §13 garde déjà dans sa propre coupe de secours n°2.
- On retire surtout du **contenu de rétention secondaire** (codex, succès, reliques), dont l'effet sur le plaisir est nul tant que la boucle de 1 minute n'est pas prouvée.
- La règle n°3 du GDD (« ne jamais couper l'Élan ni la recharge cyan ») est respectée.

---

## 6. Verdict

### 6.1 Notes

| Document | Note | Pourquoi |
|---|---|---|
| **GDD.md** | **7 / 10** | Le cœur est très fort (écho, Élan, graine, budget d'attente chiffré, validateur), avec de vraies justifications. Défauts : un P0 surdimensionné, des chiffres de puits incohérents (§9.1 contre §9.3), une simulation à 1/240 s, deux combos en germe, et la règle du complice trop large. |
| **FEEL.md** | **6,5 / 10** | Excellent sur l'entrée tactile, la clémence, le hitstop à 0 sur les actions et les budgets anti-surcharge. Mais il **réécrit la physique** contre le GDD, avec des chiffres valables seulement à 60 Hz, une volte « 25 px » fausse, une glissade qui casse les chunks, l'interdiction de l'Élan et un second « Élan » qui est un combo. Il diagnostique le prototype et non le GDD. |
| **ECONOMY.md** | **5,5 / 10** | Travail sérieux : simulation sur 30 jours, constantes prêtes à coder, garde-fous éthiques. Mais il a été écrit contre le prototype, il **casse la règle du cyan** (tenues et effets d'écho), vend de la puissance par ricochet, autorise la vie vidéo en Tour du jour, et son 1,96 est optimiste. |
| **CHUNK_FORMAT.md** | **7,5 / 10** | Clair, testable, et `chunks.gd` le respecte. Écarts mineurs avec le GDD (`H`, I/A, `alt`, attente de 2 s, laser < 5). |

### 6.2 Top 10 des corrections obligatoires (par sévérité)

1. **Trancher la physique** (S).
   - Le §1.4 de ce document devient la référence.
   - FEEL §2.2 à §2.5 : retirer la gravité asymétrique, la glissade accélérée, l'accroche de 0,30 s, la volte à −220 et l'interdiction de la hauteur variable. Convertir tous les « i » en ticks à 120 Hz.
   - GDD §2.3 : remplacer les mesures à 1/240 s par celles à 120 Hz et ajouter la rampe de l'Élan.
   - Code : hitbox 6 × 10, laser 6, scie 5, hitstop 0,10 s.
2. **Sanctuariser le cyan** (S).
   - Supprimer les effets d'écho non cyan (ECONOMY §2.3).
   - Retirer ou recolorer les tenues « echo », « prune », « braise » et « gardien » (ECONOMY §2.1).
   - Écrire dans le GDD §9.3 la règle : « le héros n'utilise jamais cyan, magenta ou rouge vif ».
3. **Aucune vie vidéo en Tour du jour, et 6 vues par jour au maximum** (S).
   - ECONOMY §4.1 s'aligne sur le GDD §10.1.
   - Supprimer `echo_shield` et `streak_rekindle`.
4. **Une seule source de vérité pour l'économie** (S).
   - ECONOMY est réécrit contre le GDD : 22 obstacles, biomes, tenues à silhouette, XP, missions et codex.
   - ECONOMY §7 (`tower.gd`) disparaît.
   - Dans l'attente, **le GDD fait foi**.
5. **Reliques hors de portée de la pub** (S). Elles passent en P1, par fragments seulement, avec des effets ≤ 10 % et sans effet sur la marée ni sur les minuteries. Les noms `r_lantern` et `r_magnet` sont renommés.
6. **Un seul combo, le « Rythme »** (M).
   - FEEL §6 est renommé et fusionné : paliers 10/20/30 ; chaîne cassée après 0,30 s au mur ; encaissement +2/+4/+6.
   - Le mot « Élan » ne désigne plus que le saut long.
7. **Réduire le P0 à environ 42 jours, avec deux portes** (M) : voir §5. Le GDD §13 est réécrit par son auteur.
8. **Mettre le CHUNK_FORMAT au même niveau que le GDD** (M).
   - Le GDD §8.1 et §8.2 adopte `H`, `alt`, les tensions I et A, et les symboles C, b, :, A, R.
   - Le CHUNK_FORMAT adopte l'attente forcée par biome (0,6 × budget) et le laser à 6.
   - Le code retire le terme « record » de la vitesse de la marée.
9. **Contre-mesure à la domination de l'Élan** (M).
   - Le validateur traite l'Élan comme l'intervalle 51-77 px.
   - Quota : dans les chunks M et P au-dessus de 150 m, la zone de l'Élan complet est létale au moins une fois sur trois.
   - En playtest : si la part d'Élans complets dépasse 60 %, l'alerte est levée.
10. **Une mort courte et passable** (M).
    - Hitstop de 0,10 s ; écran de vie à 1,5 s maximum ; gravure accélérable au tap dès la 3ᵉ fois qu'on la voit ; mort par la marée en 0,8 s.
    - Règle du complice limitée à O11 en P0.
    - FEEL §4.1 s'aligne.

### 6.3 Ce qui est bon, et qu'il faut protéger

- La règle en 5 secondes du GDD §3.1.
- La graine identique pour les 4 vies.
- Le budget d'attente chiffré du §8.6.
- Le validateur headless avec une marge par biome.
- La lecture à l'appui et le hitstop à 0 sur les actions (FEEL).
- Les garde-fous éthiques d'ECONOMY §5, appliqués à la lettre.
- La série de jours divisée par 2 au lieu d'être remise à zéro (ECONOMY).

Le jeu a un vrai cœur. Le danger n'est pas qu'il soit mauvais. Le danger est qu'il soit **enterré sous trois documents qui ne se lisent pas entre eux**.

— Milo Hartmann
