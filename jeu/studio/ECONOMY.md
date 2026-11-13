# ÉCHO : économie, rétention, monétisation

Auteur : Milo Hartmann (économie et rétention). Version 1, 13/11/2026.
Périmètre : monnaies, contenu à débloquer, boucles quotidiennes et hebdomadaires, niveaux, succès, vidéos récompensées, revenus, éthique, constantes prêtes à coder.
Fichiers de code concernés (le lead ou le dev les modifie, pas moi) : `game/scripts/game_state.gd`, `ads.gd`, `main.gd`, `world.gd`, `tower.gd`, plus un nouveau `economy.gd`.

---

## 0. Les décisions en bref

| Décision | Pourquoi (une ligne) |
|---|---|
| Deux monnaies : **Éclats** (courante) et **Prismes** (rare, cyan) | Avec une seule monnaie, la pub finit par tout acheter. Le Prisme garantit que le haut de gamme se gagne en jouant. |
| Les Prismes ne viennent **jamais** d'une pub et ne sont **jamais** vendus | C'est le garde-fou anti pay-to-win et anti dark pattern (préparation du Digital Fairness Act). |
| Gain en jeu **proportionnel à la hauteur** : 0,30 × m + 12 par ascension | Détecteur de maîtrise : le joueur qui monte haut doit gagner plus que celui qui stagne. |
| Toute récompense vidéo a une **alternative en jouant** (éclats ou temps) | La pub accélère, elle ne débloque jamais rien d'exclusif. |
| Série divisée par 2 au lieu d'une remise à zéro, plus 1 gel gratuit par semaine | La remise à zéro après un jour manqué est un dark pattern cité par la consultation DFA. Elle fait aussi fuir les joueurs. |
| Calendrier de connexion à 7 cases qui **n'avance que les jours joués** et ne se remet jamais à zéro | Même raison : aucune perte, aucune pression. |
| Reliques actives seulement en Ascension libre, **désactivées en Tour du jour** | La graine partagée doit rester équitable pour le partage façon Wordle. |
| P0 : 5 emplacements vidéo, **1,96 vue par DAU et par jour** | C'est au-dessus de la moyenne casual (~1,5) sans être agressif, et chaque vue est un vrai choix. |
| Scénario central : **0,0245 $ par DAU et par jour**. Pour 2000 $/jour il faut **~82 000 DAU** | eCPM effectif de 12,5 $ (mix pays riches, perte de consentement et taux de remplissage inclus). |

---

## 1. Monnaies

### 1.1 Les trois ressources

| Ressource | Rôle | Couleur à l'écran | Sources | Puits |
|---|---|---|---|---|
| **Éclats** | Monnaie courante, tangible : on la ramasse dans la tour | Or chaud `#ffd166` sur cyan `#34e0e0` | Ramassage, bonus de hauteur, gravures, missions, calendrier, série, défi hebdo, succès, niveaux, pubs | Tenues, traînées, effets, reliques, sanctuaire, relances payantes |
| **Prismes** | Monnaie rare, gagnée seulement par la maîtrise et la régularité | Cyan clair `#7fe9ff`, reflet magenta `#ff5ac8` | Missions difficiles, bonus 3/3, calendrier (cases 3 et 7), paliers de niveau, défi hebdo argent/or, succès, codex | Cosmétiques épiques et légendaires, reliques niveau 2 et 3 |
| **XP** | Progression du compte (intangible), ne se dépense pas | Barre lilas `#b388ff` | Hauteur, gravures, records, missions | Aucun : elle débloque des fonctions par paliers |

Règle de lisibilité : toute l'économie s'explique en 5 minutes. « Les éclats achètent, les prismes prouvent, l'XP ouvre des portes. »

### 1.2 Gains en jeu (par ascension)

**Formule cible : `éclats ≈ 0,30 × hauteur_max_m + 12`.**

| Composante | Valeur | Commentaire |
|---|---|---|
| Ramassage | ≈ 0,25 éclat par mètre | Nouvelle génération (voir §10) : 0,35/m générés, environ 70 % ramassés |
| Bonus de hauteur | `floor(hauteur / 20)` | Paie la maîtrise et non le temps passé |
| Prime de fin d'ascension | 6 | Une ascension ratée rapporte quand même quelque chose |
| Reliquat d'écho | +2 par piège gravé (environ 3 par ascension, donc ~6) | Transforme la mort en petit gain : elle devient de l'information |

Aujourd'hui, le jeu génère environ 0,126 éclat par mètre (75 % de chance × 1,6 éclat moyen par section de 9,5 m). C'est trop peu pour un catalogue d'environ 99 000 éclats. La nouvelle génération multiplie le flux de ramassage par environ 2.

### 1.3 Flux par minute de jeu (joueur moyen actif, sans pub)

| Jour | Min/jour | Hauteur max | Durée d'une ascension | Éclats en jeu/min | Méta (missions, calendrier…) /min | **Total/min** |
|---|---|---|---|---|---|---|
| J1 | 15 | 120 m | 3,5 min | 13,7 | 34,7 | 48 |
| J3 | 12 | 170 m | 3,5 min | 17,7 | 33,8 | 51 |
| J7 | 12 | 230 m | 3,7 min | 21,9 | 72 (jour du coffre hebdo) | 94 |
| J14 | 11 | 300 m | 3,9 min | 25,8 | 71 (défi hebdo) | 97 |
| J30 | 10 | 380 m | 4,5 min | 28,0 | 22,5 | 51 |
| Moyenne J1-J30 | 11,1 | | | 24 | 42 | **66** (75 avec le profil pub moyen) |

Puits par minute : le catalogue complet coûte ~99 000 éclats et ~300 prismes, ce qui représente environ 1 300 minutes de jeu au rythme moyen, soit 4 à 5 mois à 10 min par jour. La partie cosmétique seule (~38 600 éclats) demande environ 48 jours. Il reste donc **toujours une serrure visible** devant le joueur, ce qui suit la règle « voir la serrure avant la clé ».

Puits secondaires (faibles, ils évitent l'inflation de fin de catalogue) :
- relance de mission au-delà de la gratuite : 60 éclats ;
- rallumer une série : 150 éclats ;
- reliques niveaux 2 et 3 ;
- sanctuaire.

### 1.4 Équilibrage sur 30 jours (simulation, profil pub moyen)

Profil pub moyen : ×2 butin accepté sur 30 % des résumés, coffre bonus 45 % des jours.

| Jour | Min | Asc. | Haut. max | Jeu | Pubs | Méta | Éclats du jour | **Éclats cumulés** | **Prismes cumulés** | XP cumulée | **Niveau** |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 15 | 4,3 | 120 | 206 | 71 | 520 | 796 | **796** | 6 | 654 | **5** |
| 2 | 12 | 3,4 | 145 | 188 | 70 | 370 | 628 | 1 425 | 8 | 1 272 | 7 |
| 3 | 12 | 3,4 | 170 | 212 | 82 | 405 | 698 | **2 123** | 11 | 1 969 | **9** |
| 5 | 12 | 3,3 | 200 | 237 | 98 | 465 | 801 | 3 594 | 17 | 3 494 | 12 |
| 7 | 12 | 3,2 | 230 | 262 | 133 | 865 | 1 260 | **5 625** | 29 | 5 189 | **15** |
| 10 | 12 | 3,0 | 260 | 273 | 100 | 375 | 748 | 7 797 | 34 | 7 879 | 18 |
| 14 | 11 | 2,8 | 300 | 284 | 139 | 780 | 1 203 | **11 540** | 49 | 11 630 | **23** |
| 21 | 11 | 2,5 | 335 | 284 | 139 | 1 140 | 1 563 | 17 695 | 73 | 18 322 | 29 |
| 30 | 10 | 2,2 | 380 | 280 | 98 | 225 | 602 | **25 205** | **102** | 26 924 | **35** |

Totaux sur 30 jours :

| Profil | Jeu | Pubs | Méta | Total éclats | Part des pubs |
|---|---|---|---|---|---|
| Sans pub | 8 037 | 0 | 14 015 | **22 052** | 0 % |
| Pub moyen | 8 037 | 3 153 | 14 015 | **25 205** | 13 % |
| Pub maximum (tous les plafonds) | 8 037 | 9 687 | 14 015 | **31 738** | 31 % |

Prismes : 102 sur 30 jours dans les trois profils, puisqu'une pub ne donne jamais de prisme. Le niveau 50 tombe vers J55-J60.

Lecture : même en regardant toutes les pubs, le joueur ne va qu'environ **44 % plus vite**. Sans pub, il atteint les mêmes jalons avec 1 à 3 jours de retard, et les prismes ne bougent pas.

### 1.5 Ce qui se débloque (joueur **sans pub**, achats raisonnables)

| Jour | Niveau | Fonctions ouvertes | Achats typiques | Pourquoi ce rythme |
|---|---|---|---|---|
| **J1** | 5 | Missions (niv 2), traînées (niv 3), défi hebdo (niv 5) | Tenue Jade (250) + traînée Poussière d'or (300) | Deux achats dès la première session : la boucle « gagner → dépenser → se voir » est apprise tout de suite |
| **J3** | 9 | Slot de relique 1 (niv 8) | Azur (300) + Lilas (400) | Petits plaisirs réguliers pendant la fenêtre critique J1-J3 |
| J5 | 12 | Sanctuaire (niv 12) | 1re relique (Bourse ou Aimant, 600-800) | Premier choix stratégique, pas seulement esthétique |
| **J7** | 15 | Missions difficiles et relance (niv 15) | Soleil (900, rare) + Bulles cyan (500) + effet Améthyste (600, effets ouverts au niv 10) | La première rare tombe le jour de la première grosse case du calendrier |
| **J14** | 23 | | Premier épique : Spectre (2500 + 10 P) | L'épique apparaît comme objectif dès J5 ; on l'atteint en 2 semaines |
| J21 | 29 | Slot de relique 2 (niv 25, atteint vers J16) | Une relique au niveau 2 | |
| **J30** | 35 | | ~9-10 tenues, 5-6 traînées, 3 effets, 2 reliques niveau 2. Tisseur d'étoiles (60 P) accessible vers J28 | La moitié du catalogue reste à prendre : objectifs pour les mois 2 à 4 |

---

## 2. Contenu à débloquer

Couleurs : pas de marron, pas de blanc cassé ou sale. Les blancs utilisés sont des blancs glacés nets (`#e8f6ff`) toujours associés à un cyan.

### 2.1 Tenues (écharpe et palette du héros), 19 au total

Les identifiants actuels sont conservés : corail, jade, azur, soleil, lilas, neige, braise, echo. Tout ce qui a déjà été acheté reste acquis.

| # | id | Nom FR / EN | Rareté | Prix | Couleurs (principale / accent) |
|---|---|---|---|---|---|
| 1 | corail | Corail / Coral | Commune | 0 (départ) | `#ff6f61` / `#ffd166` |
| 2 | jade | Jade / Jade | Commune | 250 | `#2ec4a6` / `#b8f2e6` |
| 3 | azur | Azur / Azure | Commune | 300 | `#3a86ff` / `#a0d2ff` |
| 4 | lilas | Lilas / Lilac | Commune | 400 | `#b388ff` / `#e6d4ff` |
| 5 | menthe | Menthe / Mint | Commune | 500 | `#7be0ad` / `#e0fff0` |
| 6 | prune | Prune / Plum | Commune | 600 | `#8e44ad` / `#e056fd` |
| 7 | soleil | Soleil / Sun | Rare | 900 | `#ffbe0b` / `#fff3b0` |
| 8 | braise | Braise / Ember | Rare | 1 100 | `#ff4d2e` / `#ffb347` |
| 9 | neige | Neige / Snow | Rare | 1 300 | `#e8f6ff` / `#7fd6ff` |
| 10 | echo | Écho / Echo | Rare | 1 500 | `#34e0e0` / `#0b3c5d` |
| 11 | orage | Orage / Storm | Rare | 1 800 | `#5b5fef` / `#f4f142` |
| 12 | spectre | Spectre / Wraith | Épique | 2 500 + 10 P | `#9ad7ff` / `#5a3cff`, écharpe translucide animée |
| 13 | nebuleuse | Nébuleuse / Nebula | Épique | 3 000 + 12 P | `#3d1a78` / `#ff5ac8`, points d'étoiles |
| 14 | lanterne | Lanterne / Lantern | Épique | 3 500 + 15 P | `#ffd166` / `#ff7b00`, halo de lumière |
| 15 | vitrail | Vitrail / Stained glass | Épique | 4 000 + 20 P | `#ff3d7f` / `#3ae0ff` / `#ffe14d` |
| 16 | gardien | Gardien du Silence / Silence Keeper | Légendaire | Succès « 1000 m » | `#0d1b3d` / `#34e0e0` |
| 17 | couronne | Couronne d'échos / Crown of Echoes | Légendaire | Niveau 50 | `#ffd700` / `#b388ff` |
| 18 | tisseur | Tisseur d'étoiles / Star Weaver | Légendaire | 60 P | `#1a1f6b` / `#9df9ff` |
| 19 | pelerin | Pèlerin / Pilgrim | Légendaire | 4 défis hebdo **or**, puis 80 P en boutique pour tous à partir du 3e mois | `#3b2a8f` / `#ffcf4d` |

Répartition : 6 communes, 5 rares, 4 épiques, 4 légendaires. Aucune tenue n'est temporaire ni réservée à une période : le Pèlerin finit par entrer en boutique, ce qui évite le FOMO.

### 2.2 Traînées (sillage pendant le saut), 10

Débloquées au niveau 3.

| id | Nom FR / EN | Prix |
|---|---|---|
| t_none | Aucune / None | 0 |
| t_gold | Poussière d'or / Gold dust | 300 |
| t_bubbles | Bulles cyan / Cyan bubbles | 500 |
| t_feathers | Plumes / Feathers | 700 |
| t_sparks | Étincelles / Sparks | 900 |
| t_fireflies | Lucioles / Fireflies | 1 200 |
| t_runes | Runes / Runes | 1 600 + 5 P |
| t_comet | Comète / Comet | 2 200 + 8 P |
| t_aurora | Aurore boréale / Northern lights | 3 000 + 12 P |
| t_twin | Ombre jumelle / Twin shadow | Succès « Chaque vie plus haute » |

### 2.3 Effets d'écho (apparence du piège gravé et de l'écho), 6

Débloqués au niveau 10.

| id | Nom FR / EN | Prix |
|---|---|---|
| e_cyan | Cyan / Cyan | 0 |
| e_amethyst | Améthyste / Amethyst | 600 |
| e_frost | Givre / Frost | 1 000 |
| e_gold | Or / Gold | 1 800 + 5 P |
| e_stars | Constellation / Constellation | 2 800 + 10 P |
| e_glyphs | Glyphes anciens / Ancient glyphs | Codex complet |

### 2.4 Reliques (talents légers), 8

Elles ne sont pas pay-to-win :
- bonus de 20 % maximum, surtout sur l'économie ;
- actives seulement en **Ascension libre** et désactivées en Tour du jour (graine partagée) ;
- jamais vendues ni données par une pub.

Emplacements : 1 au niveau 8, 2 au niveau 25.

| id | Nom FR / EN | Niv 1 | Niv 2 | Niv 3 | Effet (niv 1 / 2 / 3) |
|---|---|---|---|---|---|
| r_purse | Bourse / Purse | 600 | 1 500 + 5 P | 3 000 + 12 P | +10 / 15 / 20 % d'éclats ramassés |
| r_memory | Mémoire / Memory | 700 | 1 500 + 5 P | 3 000 + 12 P | +10 / 15 / 20 % d'XP |
| r_magnet | Aimant / Magnet | 800 | 1 500 + 5 P | 3 000 + 12 P | Rayon de ramassage +3 / 5 / 7 px |
| r_hourglass | Sablier / Hourglass | 900 | 1 500 + 5 P | 3 000 + 12 P | Le Silence démarre 2 / 3 / 4 s plus tard (vie 1 uniquement) |
| r_lantern | Lanterne / Lantern | 900 | 1 500 + 5 P | 3 000 + 12 P | Alerte laser allongée de +0,10 / 0,15 / 0,20 s |
| r_foresight | Écho prévoyant / Foresight | 1 000 | 1 500 + 5 P | 3 000 + 12 P | L'écho clignote 1,0 / 1,5 / 2,0 m avant le piège qui l'a tué |
| r_trophy | Trophée / Trophy | 800 | 1 500 + 5 P | 3 000 + 12 P | Un grand éclat garanti à 150 m / 120 m / 100 m |
| r_cartographer | Cartographe / Cartographer | 700 | 1 500 + 5 P | 3 000 + 12 P | Chaque gravure donne +2 / +3 / +4 éclats de plus |

Total : 6 400 (niv 1) + 12 000 + 40 P (niv 2) + 24 000 + 96 P (niv 3). C'est le puits de long terme principal.

### 2.5 Sanctuaire (décor du menu) : optionnel, P2, avec une V1 minimale en P1

Justification : il rend la progression visible et sert de puits pour les mois 3 à 6. Mais il coûte 16 objets en art. **V1 (P1)** : une simple étagère de trophées remplie par les succès, sans achat. **V2 (P2)** : 16 décors achetables. Fonction ouverte au niveau 12.

| id | Décor | Prix |
|---|---|---|
| s_lamp | Lampe d'écho | 200 |
| s_plant | Fougère cyan | 300 |
| s_banner | Bannière lilas | 400 |
| s_bell | Cloche du Silence | 500 |
| s_rug | Tapis géométrique (indigo et or) | 600 |
| s_fountain | Fontaine d'écho | 800 |
| s_map | Carte de la tour | 900 |
| s_crystal | Cristal flottant | 1 000 |
| s_shelf | Étagère à reliques | 1 200 |
| s_window | Vitrail rond | 1 400 |
| s_orrery | Orrerie | 1 600 |
| s_statue | Statue du héros | 1 800 |
| s_aquarium | Bassin de lucioles | 2 000 |
| s_portal | Arche de cristal | 2 400 |
| s_stars | Plafond étoilé | 2 700 |
| s_throne | Siège du Gardien | 3 000 |

Total : 20 800 éclats.

### 2.6 Codex : 40 entrées, gratuit, rempli en jouant

| Catégorie | Entrées | Condition | Récompense de catégorie complète |
|---|---|---|---|
| Pièges (pic, scie, scie mobile, laser) | 16 = 4 × (vu, mort, gravé ×10, gravé ×50) | Statistiques | 10 P |
| Étages ou biomes (selon le level design) | 4 | Atteindre l'étage | 5 P |
| Pages du Silence (lore) | 16 | Une page rare apparaît environ tous les 250 m d'ascension cumulée, jamais deux fois la même | 15 P |
| Personnages et lieux | 4 | Événements (1er record, 1er défi or, etc.) | 5 P |
| **Codex complet** | 40 | | Effet « Glyphes anciens » + 10 P |

Le codex donne du sens à la mort (« gravé ×50 »), conformément à la boucle de maîtrise de Koster.

---

## 3. Boucles de rétention

### 3.1 Session : une ascension de 3 à 5 minutes

```
Choisir le mode (libre / Tour du jour) → 4 vies → graver ses morts → hauteur max
→ Résumé : éclats (+ ×2 en option) → missions qui avancent → XP et niveau
→ Boutique : la serrure la plus proche est mise en avant (« plus que 120 éclats ») → rejouer
```

- Durée cible : 3,5 min au début, 4,5 min à J30 (la marée et la hauteur augmentent). La règle « 4 vies » borne naturellement la session.
- Fin d'ascension : afficher **une** information de progression, la plus proche de l'objectif. Exemples : mission à 80 %, tenue à 120 éclats, niveau à 60 XP. Raison : un seul « presque » motive, cinq saturent.

### 3.2 Jour : 3 missions quotidiennes et la Tour du jour

- **Tirage** : 1 facile + 1 moyenne + 1 difficile, renouvelé à minuit heure locale. Avant le niveau 15, la difficile est remplacée par une 2e moyenne.
  Raison : le débutant ne doit pas voir une mission impossible.
- **Récompenses** :

  | Difficulté | Récompense |
  |---|---|
  | Facile | 25 éclats + 20 XP |
  | Moyenne | 40 éclats + 30 XP |
  | Difficile | 70 éclats + 50 XP + 1 P |
  | Bonus 3/3 | 30 éclats + 1 P |

- **Relance** : 1 gratuite par jour. Ensuite, au choix, vidéo ou 60 éclats (2 fois maximum).
- **Missions de hauteur adaptatives** (champ `scale`) : la cible vaut `max(cible, arrondi10(meilleure_hauteur × scale))`, plafonnée par `cap`. Raison : l'expert reste mis au défi (détecteur de maîtrise).
- **Tour du jour** : graine partagée, une ascension classée par jour (les suivantes ne comptent pas). Bonus de série = `10 + 5 × min(série, 8)`, donc de 15 à 50 éclats.
  - Un jour manqué divise la série par 2 (arrondi inférieur, minimum 1) au lieu de la remettre à 0.
  - 1 gel automatique gratuit par semaine : le premier jour manqué de la semaine ne coûte rien.

#### Les 30 missions types

Portée : `day` = cumul dans la journée, `run` = dans une ascension, `life` = dans une seule vie.

| # | id | Diff. | FR | EN | Condition (stat, portée, cible) |
|---|---|---|---|---|---|
| 1 | m_climb_300 | F | Grimpe 300 m au total | Climb 300 m in total | climb_m, day, 300 |
| 2 | m_shards_25 | F | Ramasse 25 éclats | Collect 25 shards | shards_picked, day, 25 |
| 3 | m_turns_10 | F | Fais 10 demi-tours | Make 10 turnarounds | turns, day, 10 |
| 4 | m_daily_play | F | Joue la Tour du jour | Play the Daily Tower | daily_played, day, 1 |
| 5 | m_asc_3 | F | Termine 3 ascensions | Finish 3 ascents | ascents, day, 3 |
| 6 | m_engrave_5 | F | Grave 5 pièges | Engrave 5 traps | engraves, day, 5 |
| 7 | m_life1_60 | F | Atteins 60 m avec ta première vie | Reach 60 m on your first life | life1_m, run, 60 |
| 8 | m_jumps_150 | F | Fais 150 rebonds | Make 150 wall jumps | jumps, day, 150 |
| 9 | m_saw_pass_10 | F | Passe 10 scies | Pass 10 saws | saws_passed, day, 10 |
| 10 | m_beat_prev_3 | M | Dépasse la hauteur de ta vie précédente 3 fois | Beat your previous life's height 3 times | life_beats_prev, day, 3 |
| 11 | m_climb_800 | M | Grimpe 800 m au total | Climb 800 m in total | climb_m, day, 800 |
| 12 | m_shards_60 | M | Ramasse 60 éclats | Collect 60 shards | shards_picked, day, 60 |
| 13 | m_turns_25 | M | Fais 25 demi-tours | Make 25 turnarounds | turns, day, 25 |
| 14 | m_life_150 | M | Monte à 150 m en une seule vie | Reach 150 m in a single life | life_m, life, 150 (scale 0,6 ; cap 400) |
| 15 | m_laser_pass_8 | M | Passe 8 lasers | Pass 8 lasers | lasers_passed, day, 8 |
| 16 | m_no_tide | M | Termine une ascension de 80 m+ sans être rattrapé par le Silence | Finish an 80 m+ ascent without being caught by the Silence | run_no_tide_m, run, 80 |
| 17 | m_engrave_types | M | Grave un pic, une scie et un laser dans la même ascension | Engrave a spike, a saw and a laser in one ascent | engrave_types, run, 3 |
| 18 | m_last_life_best | M | Fais ta meilleure vie avec la 4e | Make your 4th life your best one | last_life_best, run, 1 |
| 19 | m_grand_shard_2 | M | Ramasse 2 grands éclats | Collect 2 grand shards | grand_shards, day, 2 |
| 20 | m_daily_beat | M | Fais mieux qu'hier sur la Tour du jour | Beat yesterday's Daily Tower score | daily_beat, day, 1 (repli si pas joué hier : daily_m ≥ 100) |
| 21 | m_asc_250 | D | Atteins 250 m en une ascension | Reach 250 m in one ascent | run_m, run, 250 (scale 0,8 ; cap 800) |
| 22 | m_life1_150 | D | Atteins 150 m avec ta première vie | Reach 150 m on your first life | life1_m, run, 150 (scale 0,5 ; cap 500) |
| 23 | m_turns_life_15 | D | Fais 15 demi-tours dans une seule vie | Make 15 turnarounds in a single life | turns_life, life, 15 |
| 24 | m_shards_run_30 | D | Ramasse 30 éclats en une ascension | Collect 30 shards in one ascent | shards_run, run, 30 (scale 0,10 ; cap 120) |
| 25 | m_life_200 | D | Monte à 200 m en une seule vie | Reach 200 m in a single life | life_m, life, 200 (scale 0,7 ; cap 600) |
| 26 | m_each_higher | D | Que chaque vie monte plus haut que la précédente | Make each life climb higher than the last | each_life_higher, run, 1 |
| 27 | m_climb_2000 | D | Grimpe 2000 m au total | Climb 2000 m in total | climb_m, day, 2000 |
| 28 | m_record | D | Bats ton record | Beat your best height | record, day, 1 |
| 29 | m_biome_2 | D | Atteins le 2e étage de la tour | Reach the tower's 2nd floor | biome, run, 2 (repli tant qu'il n'y a pas de biomes : run_m ≥ 300) |
| 30 | m_saws_20 | D | Passe 20 scies mobiles | Pass 20 moving saws | moving_saws_passed, day, 20 |

Réalisation moyenne mesurée en simulation : environ 115 éclats par jour via les missions.

### 3.3 Semaine : défi hebdo, calendrier, série

**Défi hebdo** (fonction ouverte au niveau 5) : du lundi 00:00 au dimanche 23:59, heure locale. La tour du défi a une graine fixe et un modificateur de la semaine, pris en rotation :
1. Sans demi-tour ;
2. Marée rapide (×1,3) ;
3. 3 vies ;
4. Lasers seulement ;
5. Éclats doublés mais pièges plus serrés.

Tentatives illimitées. Ce qui compte, c'est la meilleure hauteur.

| Palier | Hauteur | Récompense |
|---|---|---|
| Bronze | 150 m | 100 éclats |
| Argent | 300 m | 200 éclats + 3 P |
| Or | 500 m | 350 éclats + 5 P (compte pour le Pèlerin) |

Raison : trois paliers, pour que le débutant ait du bronze et l'expert de l'or. Les paliers sont cumulatifs.

**Calendrier de connexion** : 7 cases. On avance d'une case par jour **joué** (au moins une ascension terminée), jamais par simple ouverture de l'appli. Il n'y a jamais de remise à zéro.

| Case | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| Éclats | 20 | 30 | 40 | 50 | 60 | 80 | 120 |
| Prismes | 0 | 0 | 1 | 0 | 0 | 0 | 3 |

Cycle complet : 400 éclats + 4 P. La vidéo « coffre bonus » double les **éclats** de la case du jour, jamais les prismes.

**Série de la Tour du jour** : bonus `10 + 5 × min(série, 8)`.

| Série | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8+ |
|---|---|---|---|---|---|---|---|---|
| Bonus (éclats) | 15 | 20 | 25 | 30 | 35 | 40 | 45 | 50 |

- Un jour manqué : la série est divisée par 2.
- Le gel gratuit (1 par semaine) absorbe le premier oubli.
- Au-delà, on peut « rallumer la série » pour 150 éclats ou une vidéo (1 fois par semaine).
- Le partage façon Wordle affiche la série.

### 3.4 Long terme : niveaux 1 à 50

**XP par ascension** = hauteur max en m + 5 par piège gravé + 10 si nouveau record (missions en plus).
**XP pour passer du niveau L à L+1** = `100 + 40 × (L − 1)`. Niveau maximum : 50.

| Niveau | 5 | 10 | 15 | 20 | 25 | 30 | 40 | 50 |
|---|---|---|---|---|---|---|---|---|
| XP cumulée | 640 | 2 340 | 5 040 | 8 740 | 13 440 | 19 140 | 33 540 | **51 940** |
| Jour moyen d'atteinte | J1 | J4 | J7 | J11 | J16 | J22 | ~J40 | ~J57 |

**Récompense de niveau** : `30 + 5 × L` éclats, plus 3 P tous les 5 niveaux (soit 7 840 éclats et 30 P du niveau 2 au niveau 50).

| Niveau | Ce qui s'ouvre | Raison |
|---|---|---|
| 2 | Missions quotidiennes | Une seule nouveauté à la fois après le tutoriel |
| 3 | Traînées | Deuxième axe cosmétique dès la 1re session |
| 5 | Défi hebdo | Fin de J1 : promesse pour la semaine |
| 8 | Slot de relique 1 | Premier choix de « build » vers J3 |
| 10 | Effets d'écho | |
| 12 | Sanctuaire (étagère de trophées en V1) | |
| 15 | Missions difficiles + relance | Le joueur a la maîtrise nécessaire (~230 m) |
| 25 | Slot de relique 2 | |
| 50 | Tenue Couronne d'échos | Objectif de prestige à 2 mois |

### 3.5 Succès (30)

| # | id | FR | EN | Condition (stat ≥ cible) | Récompense |
|---|---|---|---|---|---|
| 1 | a_first | Premier pas | First step | ascents ≥ 1 | 20 |
| 2 | a_h50 | 50 mètres | 50 meters | best_m ≥ 50 | 30 |
| 3 | a_h100 | Cent mètres | One hundred | best_m ≥ 100 | 50 |
| 4 | a_h150 | Au-dessus des nuages | Above the clouds | best_m ≥ 150 | 80 |
| 5 | a_h250 | Vertige | Vertigo | best_m ≥ 250 | 120 + 2 P |
| 6 | a_h400 | Haute voltige | High wire | best_m ≥ 400 | 200 + 3 P |
| 7 | a_h600 | Sommet lointain | Distant summit | best_m ≥ 600 | 300 + 5 P |
| 8 | a_h800 | Au-delà du Silence | Beyond the Silence | best_m ≥ 800 | 400 + 8 P |
| 9 | a_h1000 | Gardien du Silence | Silence Keeper | best_m ≥ 1000 | Tenue Gardien + 10 P |
| 10 | a_engrave_10 | Graveur | Engraver | engraves_total ≥ 10 | 40 |
| 11 | a_engrave_100 | Mémoire de pierre | Stone memory | engraves_total ≥ 100 | 150 + 2 P |
| 12 | a_engrave_500 | Mille cicatrices | A thousand scars | engraves_total ≥ 500 | 400 + 5 P |
| 13 | a_types_run | Trois leçons | Three lessons | engrave_types (run) ≥ 3 | 60 |
| 14 | a_turns_100 | Volte-face | About-face | turns_total ≥ 100 | 50 |
| 15 | a_turns_1000 | Danseur de murs | Wall dancer | turns_total ≥ 1000 | 250 + 3 P |
| 16 | a_shards_1k | Poche pleine | Full pocket | shards_earned_total ≥ 1000 | 80 |
| 17 | a_shards_10k | Trésor d'écho | Echo treasure | shards_earned_total ≥ 10000 | 300 + 5 P |
| 18 | a_runs_10 | Habitué | Regular | ascents ≥ 10 | 60 |
| 19 | a_runs_100 | Pèlerin de la tour | Tower pilgrim | ascents ≥ 100 | 250 + 3 P |
| 20 | a_runs_500 | Inlassable | Relentless | ascents ≥ 500 | 500 + 8 P |
| 21 | a_daily_7 | Rendez-vous | Appointment | daily_days ≥ 7 | 100 + 2 P |
| 22 | a_daily_30 | Rituel | Ritual | daily_days ≥ 30 | 300 + 5 P |
| 23 | a_streak_8 | Flamme vive | Bright flame | streak ≥ 8 | 150 + 2 P |
| 24 | a_weekly_gold | Or hebdo | Weekly gold | weekly_gold ≥ 1 | 200 + 3 P |
| 25 | a_no_tide_200 | Plus vite que le Silence | Outrun the Silence | run_no_tide_m ≥ 200 | 150 + 2 P |
| 26 | a_life1_300 | D'une traite | In one go | life1_m ≥ 300 | 250 + 3 P |
| 27 | a_each_higher | Toujours plus haut | Ever higher | each_life_higher ≥ 1 | Traînée Ombre jumelle |
| 28 | a_codex_half | Archiviste | Archivist | codex ≥ 20 | 200 + 3 P |
| 29 | a_missions_100 | Fidèle au poste | Dutiful | missions_done ≥ 100 | 300 + 5 P |
| 30 | a_level_25 | Vétéran | Veteran | level ≥ 25 | 250 + 5 P |

Total : 5 240 éclats + 84 P (plus 2 objets), répartis à peu près ainsi :
- environ 200 éclats à J1 ;
- environ 80 par jour jusqu'à J7 ;
- environ 50 par jour jusqu'à J14 ;
- environ 30 par jour ensuite (déjà compris dans la simulation).

Les succès 1 à 4, 10, 14 et 18 tombent presque tous lors de la 1re session : le joueur découvre ainsi le système sans le chercher.

---

## 4. Vidéos récompensées (uniquement choisies par le joueur)

Interface existante : `Ads.show_rewarded(placement, on_reward, on_cancel)`. Hypothèse : 1 vue = 1 vidéo vue jusqu'au bout et récompensée.

### 4.1 Les 7 emplacements

| # | Emplacement | Déclencheur | Valeur | Plafond/jour | Offres/DAU × acceptation = **vues/DAU** | Impact sur l'équilibre | Risque de lassitude et parade | Priorité |
|---|---|---|---|---|---|---|---|---|
| 1 | `extra_life` +1 vie | Les 4 vies sont épuisées et l'ascension a dépassé 30 m. 1 fois par ascension | Une 5e vie (≈ +25 % de hauteur, +15 éclats) | 5 | 2,5 × 25 % = **0,62** | Faible. En Tour du jour, le partage affiche « 5 vies » et le classement le signale | Moyen. Après 2 refus de suite, l'offre est masquée pour le reste de la session | **P0** |
| 2 | `double_loot` ×2 butin | Écran de résumé, si le butin de l'ascension est ≥ 15 | Double les éclats **en jeu** de l'ascension (pas la méta) | 5 | 2,8 × 27 % = **0,76** | +3 153 éclats sur 30 j (13 %), +9 687 au maximum (31 %) | Faible à moyen. Bouton secondaire, jamais le bouton principal | **P0** |
| 3 | `bonus_chest` coffre bonus | Case du calendrier du jour | Double les éclats de la case (20 à 120), jamais les prismes | 1 | 0,40 | +~200 éclats par cycle de 7 jours | Faible. Une seule fois par jour | **P0** |
| 4 | `mission_reroll` relance | Après la relance gratuite du jour | Nouvelle mission de même difficulté (sinon 60 éclats) | 2 | **0,10** | Quasi nul | Faible | **P0** |
| 5 | `skin_trial` essai | Fiche d'une tenue ou traînée verrouillée | Porter l'objet pendant 3 ascensions | 2 | **0,08** | Nul sur le flux. Pousse à l'achat en éclats, donc renforce le puits | Faible | **P0** |
| 6 | `echo_shield` bouclier | Début d'une Ascension libre (jamais en Tour du jour ni en défi) | Le premier piège touché ne coûte pas de vie | 3 | ~3 × 15 % = 0,45 | Moyen : le joueur monte plus haut, donc gagne plus d'éclats et d'XP | Moyen. Un écran de plus avant de jouer : à tester en A/B | P1 |
| 7 | `streak_rekindle` rallumer | Retour après un jour manqué et gel déjà utilisé | Rend la série d'avant (sinon 150 éclats) | 1 par semaine | ~0,02 | Nul | Faible (rare) | P1 |

**Recommandation P0 : emplacements 1 à 5, soit 0,62 + 0,76 + 0,40 + 0,10 + 0,08 = 1,96 vue par DAU et par jour.**
Avec le P1 : environ 2,43. Raison : les P0 sont greffés sur des moments qui existent déjà (fin de vies, résumé, calendrier) et ne demandent ni écran ni décision supplémentaires.

Repères :
- Unity : 23,8 % d'engagement sur les offres entre niveaux, et plus de 60 % des joueurs intéressés par les vidéos récompensées. Nos taux de 25-27 % sont donc dans la norme.
- Le ×2 butin et la vie en plus sont les deux emplacements les plus rentables du genre.

### 4.2 Revenus

**eCPM rewarded Android par pays** (synthèse des rapports 2024-2026 ; voir les sources) :

| Pays | eCPM $ | Part du mix | Contribution $ |
|---|---|---|---|
| États-Unis | 16,5 | 45 % | 7,43 |
| Royaume-Uni | 11,0 | 12 % | 1,32 |
| Canada | 13,0 | 10 % | 1,30 |
| Australie | 13,5 | 8 % | 1,08 |
| Allemagne | 11,0 | 12 % | 1,32 |
| Suisse | 12,0 | 3 % | 0,36 |
| Nordiques (estimation) | 10,0 | 10 % | 1,00 |
| **eCPM brut pondéré** | | | **13,80** |

Corrections appliquées :
- **Consentement** : on suppose que 30 % des utilisateurs EU/UK/CH refusent les pubs personnalisées et que leur eCPM baisse d'environ 40 %, soit −0,48 $.
- **Taux de remplissage** : 95 %.
- Résultat : **eCPM effectif 12,66 $, arrondi à 12,5 $**.

**Formule** : ARPDAU = vues/DAU × eCPM / 1000. DAU nécessaire = objectif / ARPDAU.

| Scénario | Vues/DAU | eCPM eff. | ARPDAU | 2000 FCFA (≈ 3,3 $) | 2000 $ | 2000 CHF (≈ 2250 $) | 2000 € (≈ 2300 $) |
|---|---|---|---|---|---|---|---|
| Pessimiste | 1,4 | 8 $ | 0,0112 $ | 295 DAU | 178 572 | 200 893 | 205 358 |
| **Central** | **1,96** | **12,5 $** | **0,0245 $** | **135 DAU** | **81 633** | **91 837** | **93 878** |
| Optimiste (P0 + P1, bon engagement) | 2,8 | 18 $ | 0,0504 $ | 66 DAU | 39 683 | 44 643 | 45 635 |
| Mix réaliste (50 % pays riches, 50 % reste du monde) | 1,96 | 7,75 $ | 0,0152 $ | 218 DAU | 131 666 | 148 124 | 151 416 |

Change supposé : 1 € ≈ 1,15 $ et 1 CHF ≈ 1,125 $. À revérifier le jour du calcul. Les ARPDAU du marché pour un casual sans achat intégré (0,01 à 0,05 $) encadrent le scénario central.

**Ce que ça demande en acquisition** (nombre de jours actifs par installation sur 180 jours, courbe de rétention interpolée) :

| Profil de rétention J1 / J7 / J30 | Jours actifs par installation | Installations/jour pour ~90 000 DAU (objectif CHF ou €) |
|---|---|---|
| Objectif ÉCHO : 35 / 12 / 4 % | 6,45 | ~13 950 |
| Plancher acceptable : 28 / 8 / 2,5 % | 4,51 | ~19 970 |
| Médiane GameAnalytics : 22 / 3,7 / 0,75 % | 2,31 | ~38 900 |

Lecture honnête pour le lead :
- **2000 FCFA par jour est atteignable vite** : environ 135 DAU, soit à peu près 25 installations par jour avec une bonne rétention.
- **2000 CHF, € ou $ par jour** exige environ 80 000 à 95 000 DAU, c'est-à-dire un succès de vitrine Play Store (mise en avant, viralité du partage Wordle) ou de l'acquisition payante. Celle-ci n'est rentable que si le LTV par installation (≈ 6,45 × 0,0245 ≈ 0,16 $) dépasse le CPI. Or le CPI casual en pays riches dépasse largement 0,16 $ : **l'UA payante n'est pas rentable** avec ce modèle. La croissance doit venir de l'organique et du partage.
- Le levier le plus fort n'est pas la pub, c'est la **rétention J7/J30**. Passer de 8 à 12 % à J7 vaut plus que deux emplacements de pub supplémentaires.

---

## 5. Garde-fous éthiques et conformité

1. **Aucune pub imposée, aucune bannière, aucun interstitiel.** Le joueur clique toujours lui-même.
2. Le bouton vidéo est **toujours secondaire** (style echo, contour) et ne remplace jamais « Rejouer » ou « Continuer ».
3. La récompense est affichée **avant** la vidéo (« Regarder une vidéo : +1 vie ») et toujours donnée si la vidéo est vue jusqu'au bout. Si la vidéo est coupée, on l'explique sans pénalité.
4. Pas de faux minuteur, pas de faux bouton fermer, pas de compte à rebours qui pousse à accepter. L'offre +1 vie attend sans limite de temps.
5. Pas de vidéo disponible : le bouton est **masqué**, rien n'est perdu. `Ads.is_ready()` doit vraiment interroger AdMob.
6. Plafonds quotidiens par emplacement (§4.1). Après 2 refus de suite de +1 vie, l'offre disparaît pour la session.
7. Les pubs ne donnent **ni prismes, ni objet exclusif, ni relique**. Tout se gagne en jouant. Les pubs pèsent au plus 31 % des éclats.
8. **Pas de loot box** : le contenu des coffres et des cases est connu à l'avance.
9. Pas de remise à zéro punitive : calendrier sans reset, série divisée par 2 avec gel gratuit. Les contenus « limités » reviennent en boutique (Pèlerin).
10. Notifications seulement sur opt-in, 1 par jour maximum, ton neutre (« La Tour du jour t'attend »), jamais de « tu vas perdre ta série ».
11. Les prix sont toujours affichés en éclats ou prismes avec le reste à gagner (« encore 120 éclats »). Il n'y a pas d'achat en argent réel, donc pas de monnaie qui masque un coût réel (préparation DFA).
12. **Consentement** : SDK UMP de Google avec CMP certifié IAB TCF (obligatoire en EEE/UK depuis le 16/01/2024 et en Suisse depuis le 31/07/2024). Bouton « Confidentialité » dans les réglages pour revenir sur son choix.
13. **Audience et Google Play Families** : déclarer une audience 13+ dans la Play Console. Raison : le pixel art « mignon » peut être jugé attirant pour les enfants.
    - Si Google classe le jeu « mixte » : âge demandé de façon neutre, puis pour les moins de 13 ans `setTagForChildDirectedTreatment(true)` et `max_ad_content_rating = G`, uniquement des SDK auto-certifiés Families, et vidéo fermable après 5 s.
    - Dans tous les cas : `max_ad_content_rating` au plus `PG` pour tout le monde.

---

## 6. Constantes prêtes à coder

Fichier proposé : `game/scripts/economy.gd`, chargé en autoload `Eco` ou via `const Eco = preload(...)`. Toutes les valeurs du document y sont reprises. Les textes sont en paires [FR, EN], comme la table `T` de `game_state.gd`.

```gdscript
# economy.gd : constantes d'économie d'ÉCHO (source : jeu/studio/ECONOMY.md)
extends Node

const ECO_VERSION := 1

# ---------- Gains en jeu ----------
const RUN := {
	"pickup_cluster_weights": [[1, 40], [3, 45], [5, 15]],  # [taille, poids %], 1 groupe par section
	"grand_shard_value": 5,
	"grand_shard_every_m": 60,
	"height_bonus_div": 20,        # bonus = floor(hauteur_m / 20)
	"run_end_bonus": 6,
	"engrave_bonus": 2,            # +2 éclats par piège gravé
	"xp_per_m": 1,
	"xp_per_engrave": 5,
	"xp_record": 10,
	"lore_page_every_m": 250,      # m d'ascension cumulée
}

# ---------- Niveaux ----------
const LEVEL := {
	"max": 50,
	"xp_base": 100,                # XP(L -> L+1) = xp_base + xp_step * (L - 1)
	"xp_step": 40,
	"reward_shards_base": 30,      # éclats au niveau L = base + per_level * L
	"reward_shards_per_level": 5,
	"reward_prisms_every": 5,
	"reward_prisms": 3,
	"unlocks": {2: "missions", 3: "trails", 5: "weekly", 8: "relic_slot_1", 10: "echo_fx",
		12: "sanctuary", 15: "hard_missions", 25: "relic_slot_2", 50: "skin_couronne"},
}

# ---------- Quotidien ----------
const DAILY := {
	"streak_base": 10,             # bonus Tour du jour = base + step * min(serie, cap)
	"streak_step": 5,
	"streak_cap": 8,
	"streak_miss_divisor": 2,      # jour manqué : serie = max(1, serie / 2)
	"streak_free_freeze_per_week": 1,
	"streak_rekindle_cost": 150,
	"calendar": [[20, 0], [30, 0], [40, 1], [50, 0], [60, 0], [80, 0], [120, 3]],  # [éclats, prismes]
	"calendar_needs_finished_ascent": true,
	"missions_per_day": 3,
	"hard_mission_min_level": 15,
	"free_rerolls": 1,
	"reroll_cost": 60,
	"max_paid_rerolls": 2,
}

const MISSION_REWARD := {
	0: {"shards": 25, "xp": 20, "prisms": 0},   # facile
	1: {"shards": 40, "xp": 30, "prisms": 0},   # moyenne
	2: {"shards": 70, "xp": 50, "prisms": 1},   # difficile
	"all3": {"shards": 30, "xp": 0, "prisms": 1},
}

# scope : "day" = cumul journée, "run" = une ascension, "life" = une vie
# scale/cap : cible = clamp(arrondi10(best_free * scale), target, cap)
const MISSIONS := [
	{"id": "m_climb_300", "tier": 0, "stat": "climb_m", "scope": "day", "target": 300, "t": ["Grimpe 300 m au total", "Climb 300 m in total"]},
	{"id": "m_shards_25", "tier": 0, "stat": "shards_picked", "scope": "day", "target": 25, "t": ["Ramasse 25 éclats", "Collect 25 shards"]},
	{"id": "m_turns_10", "tier": 0, "stat": "turns", "scope": "day", "target": 10, "t": ["Fais 10 demi-tours", "Make 10 turnarounds"]},
	{"id": "m_daily_play", "tier": 0, "stat": "daily_played", "scope": "day", "target": 1, "t": ["Joue la Tour du jour", "Play the Daily Tower"]},
	{"id": "m_asc_3", "tier": 0, "stat": "ascents", "scope": "day", "target": 3, "t": ["Termine 3 ascensions", "Finish 3 ascents"]},
	{"id": "m_engrave_5", "tier": 0, "stat": "engraves", "scope": "day", "target": 5, "t": ["Grave 5 pièges", "Engrave 5 traps"]},
	{"id": "m_life1_60", "tier": 0, "stat": "life1_m", "scope": "run", "target": 60, "t": ["Atteins 60 m avec ta première vie", "Reach 60 m on your first life"]},
	{"id": "m_jumps_150", "tier": 0, "stat": "jumps", "scope": "day", "target": 150, "t": ["Fais 150 rebonds", "Make 150 wall jumps"]},
	{"id": "m_saw_pass_10", "tier": 0, "stat": "saws_passed", "scope": "day", "target": 10, "t": ["Passe 10 scies", "Pass 10 saws"]},
	{"id": "m_beat_prev_3", "tier": 1, "stat": "life_beats_prev", "scope": "day", "target": 3, "t": ["Dépasse la hauteur de ta vie précédente 3 fois", "Beat your previous life's height 3 times"]},
	{"id": "m_climb_800", "tier": 1, "stat": "climb_m", "scope": "day", "target": 800, "t": ["Grimpe 800 m au total", "Climb 800 m in total"]},
	{"id": "m_shards_60", "tier": 1, "stat": "shards_picked", "scope": "day", "target": 60, "t": ["Ramasse 60 éclats", "Collect 60 shards"]},
	{"id": "m_turns_25", "tier": 1, "stat": "turns", "scope": "day", "target": 25, "t": ["Fais 25 demi-tours", "Make 25 turnarounds"]},
	{"id": "m_life_150", "tier": 1, "stat": "life_m", "scope": "life", "target": 150, "scale": 0.6, "cap": 400, "t": ["Monte à %d m en une seule vie", "Reach %d m in a single life"]},
	{"id": "m_laser_pass_8", "tier": 1, "stat": "lasers_passed", "scope": "day", "target": 8, "t": ["Passe 8 lasers", "Pass 8 lasers"]},
	{"id": "m_no_tide", "tier": 1, "stat": "run_no_tide_m", "scope": "run", "target": 80, "t": ["Termine une ascension de 80 m+ sans être rattrapé par le Silence", "Finish an 80 m+ ascent without being caught by the Silence"]},
	{"id": "m_engrave_types", "tier": 1, "stat": "engrave_types", "scope": "run", "target": 3, "t": ["Grave un pic, une scie et un laser dans la même ascension", "Engrave a spike, a saw and a laser in one ascent"]},
	{"id": "m_last_life_best", "tier": 1, "stat": "last_life_best", "scope": "run", "target": 1, "t": ["Fais ta meilleure vie avec la 4e", "Make your 4th life your best one"]},
	{"id": "m_grand_shard_2", "tier": 1, "stat": "grand_shards", "scope": "day", "target": 2, "t": ["Ramasse 2 grands éclats", "Collect 2 grand shards"]},
	{"id": "m_daily_beat", "tier": 1, "stat": "daily_beat", "scope": "day", "target": 1, "fallback": {"stat": "daily_m", "target": 100}, "t": ["Fais mieux qu'hier sur la Tour du jour", "Beat yesterday's Daily Tower score"]},
	{"id": "m_asc_250", "tier": 2, "stat": "run_m", "scope": "run", "target": 250, "scale": 0.8, "cap": 800, "t": ["Atteins %d m en une ascension", "Reach %d m in one ascent"]},
	{"id": "m_life1_150", "tier": 2, "stat": "life1_m", "scope": "run", "target": 150, "scale": 0.5, "cap": 500, "t": ["Atteins %d m avec ta première vie", "Reach %d m on your first life"]},
	{"id": "m_turns_life_15", "tier": 2, "stat": "turns_life", "scope": "life", "target": 15, "t": ["Fais 15 demi-tours dans une seule vie", "Make 15 turnarounds in a single life"]},
	{"id": "m_shards_run_30", "tier": 2, "stat": "shards_run", "scope": "run", "target": 30, "scale": 0.10, "cap": 120, "t": ["Ramasse %d éclats en une ascension", "Collect %d shards in one ascent"]},
	{"id": "m_life_200", "tier": 2, "stat": "life_m", "scope": "life", "target": 200, "scale": 0.7, "cap": 600, "t": ["Monte à %d m en une seule vie", "Reach %d m in a single life"]},
	{"id": "m_each_higher", "tier": 2, "stat": "each_life_higher", "scope": "run", "target": 1, "t": ["Que chaque vie monte plus haut que la précédente", "Make each life climb higher than the last"]},
	{"id": "m_climb_2000", "tier": 2, "stat": "climb_m", "scope": "day", "target": 2000, "t": ["Grimpe 2000 m au total", "Climb 2000 m in total"]},
	{"id": "m_record", "tier": 2, "stat": "record", "scope": "day", "target": 1, "t": ["Bats ton record", "Beat your best height"]},
	{"id": "m_biome_2", "tier": 2, "stat": "biome", "scope": "run", "target": 2, "fallback": {"stat": "run_m", "target": 300}, "t": ["Atteins le 2e étage de la tour", "Reach the tower's 2nd floor"]},
	{"id": "m_saws_20", "tier": 2, "stat": "moving_saws_passed", "scope": "day", "target": 20, "t": ["Passe 20 scies mobiles", "Pass 20 moving saws"]},
]

# ---------- Hebdo ----------
const WEEKLY := {
	"min_level": 5,
	"reset_weekday": 1,            # lundi 00:00 heure locale
	"tiers": [
		{"id": "bronze", "m": 150, "shards": 100, "prisms": 0},
		{"id": "silver", "m": 300, "shards": 200, "prisms": 3},
		{"id": "gold", "m": 500, "shards": 350, "prisms": 5},
	],
	"modifiers": ["no_turn", "fast_tide", "three_lives", "lasers_only", "dense_double"],
	"fast_tide_mult": 1.3,
}

# ---------- Succès ----------
const ACHIEVEMENTS := [
	{"id": "a_first", "stat": "ascents", "target": 1, "shards": 20, "prisms": 0, "t": ["Premier pas", "First step"]},
	{"id": "a_h50", "stat": "best_m", "target": 50, "shards": 30, "prisms": 0, "t": ["50 mètres", "50 meters"]},
	{"id": "a_h100", "stat": "best_m", "target": 100, "shards": 50, "prisms": 0, "t": ["Cent mètres", "One hundred"]},
	{"id": "a_h150", "stat": "best_m", "target": 150, "shards": 80, "prisms": 0, "t": ["Au-dessus des nuages", "Above the clouds"]},
	{"id": "a_h250", "stat": "best_m", "target": 250, "shards": 120, "prisms": 2, "t": ["Vertige", "Vertigo"]},
	{"id": "a_h400", "stat": "best_m", "target": 400, "shards": 200, "prisms": 3, "t": ["Haute voltige", "High wire"]},
	{"id": "a_h600", "stat": "best_m", "target": 600, "shards": 300, "prisms": 5, "t": ["Sommet lointain", "Distant summit"]},
	{"id": "a_h800", "stat": "best_m", "target": 800, "shards": 400, "prisms": 8, "t": ["Au-delà du Silence", "Beyond the Silence"]},
	{"id": "a_h1000", "stat": "best_m", "target": 1000, "shards": 0, "prisms": 10, "item": "gardien", "t": ["Gardien du Silence", "Silence Keeper"]},
	{"id": "a_engrave_10", "stat": "engraves_total", "target": 10, "shards": 40, "prisms": 0, "t": ["Graveur", "Engraver"]},
	{"id": "a_engrave_100", "stat": "engraves_total", "target": 100, "shards": 150, "prisms": 2, "t": ["Mémoire de pierre", "Stone memory"]},
	{"id": "a_engrave_500", "stat": "engraves_total", "target": 500, "shards": 400, "prisms": 5, "t": ["Mille cicatrices", "A thousand scars"]},
	{"id": "a_types_run", "stat": "engrave_types_run", "target": 3, "shards": 60, "prisms": 0, "t": ["Trois leçons", "Three lessons"]},
	{"id": "a_turns_100", "stat": "turns_total", "target": 100, "shards": 50, "prisms": 0, "t": ["Volte-face", "About-face"]},
	{"id": "a_turns_1000", "stat": "turns_total", "target": 1000, "shards": 250, "prisms": 3, "t": ["Danseur de murs", "Wall dancer"]},
	{"id": "a_shards_1k", "stat": "shards_earned_total", "target": 1000, "shards": 80, "prisms": 0, "t": ["Poche pleine", "Full pocket"]},
	{"id": "a_shards_10k", "stat": "shards_earned_total", "target": 10000, "shards": 300, "prisms": 5, "t": ["Trésor d'écho", "Echo treasure"]},
	{"id": "a_runs_10", "stat": "ascents", "target": 10, "shards": 60, "prisms": 0, "t": ["Habitué", "Regular"]},
	{"id": "a_runs_100", "stat": "ascents", "target": 100, "shards": 250, "prisms": 3, "t": ["Pèlerin de la tour", "Tower pilgrim"]},
	{"id": "a_runs_500", "stat": "ascents", "target": 500, "shards": 500, "prisms": 8, "t": ["Inlassable", "Relentless"]},
	{"id": "a_daily_7", "stat": "daily_days", "target": 7, "shards": 100, "prisms": 2, "t": ["Rendez-vous", "Appointment"]},
	{"id": "a_daily_30", "stat": "daily_days", "target": 30, "shards": 300, "prisms": 5, "t": ["Rituel", "Ritual"]},
	{"id": "a_streak_8", "stat": "streak", "target": 8, "shards": 150, "prisms": 2, "t": ["Flamme vive", "Bright flame"]},
	{"id": "a_weekly_gold", "stat": "weekly_gold", "target": 1, "shards": 200, "prisms": 3, "t": ["Or hebdo", "Weekly gold"]},
	{"id": "a_no_tide_200", "stat": "run_no_tide_m", "target": 200, "shards": 150, "prisms": 2, "t": ["Plus vite que le Silence", "Outrun the Silence"]},
	{"id": "a_life1_300", "stat": "life1_m", "target": 300, "shards": 250, "prisms": 3, "t": ["D'une traite", "In one go"]},
	{"id": "a_each_higher", "stat": "each_life_higher", "target": 1, "shards": 0, "prisms": 0, "item": "t_twin", "t": ["Toujours plus haut", "Ever higher"]},
	{"id": "a_codex_half", "stat": "codex", "target": 20, "shards": 200, "prisms": 3, "t": ["Archiviste", "Archivist"]},
	{"id": "a_missions_100", "stat": "missions_done", "target": 100, "shards": 300, "prisms": 5, "t": ["Fidèle au poste", "Dutiful"]},
	{"id": "a_level_25", "stat": "level", "target": 25, "shards": 250, "prisms": 5, "t": ["Vétéran", "Veteran"]},
]

# ---------- Catalogue ----------
# rarity : 0 commune, 1 rare, 2 épique, 3 légendaire ; unlock : "" = achat, sinon condition
const SKINS := [
	{"id": "corail", "rarity": 0, "shards": 0, "prisms": 0, "unlock": "", "c": ["#ff6f61", "#ffd166"], "t": ["Corail", "Coral"]},
	{"id": "jade", "rarity": 0, "shards": 250, "prisms": 0, "unlock": "", "c": ["#2ec4a6", "#b8f2e6"], "t": ["Jade", "Jade"]},
	{"id": "azur", "rarity": 0, "shards": 300, "prisms": 0, "unlock": "", "c": ["#3a86ff", "#a0d2ff"], "t": ["Azur", "Azure"]},
	{"id": "lilas", "rarity": 0, "shards": 400, "prisms": 0, "unlock": "", "c": ["#b388ff", "#e6d4ff"], "t": ["Lilas", "Lilac"]},
	{"id": "menthe", "rarity": 0, "shards": 500, "prisms": 0, "unlock": "", "c": ["#7be0ad", "#e0fff0"], "t": ["Menthe", "Mint"]},
	{"id": "prune", "rarity": 0, "shards": 600, "prisms": 0, "unlock": "", "c": ["#8e44ad", "#e056fd"], "t": ["Prune", "Plum"]},
	{"id": "soleil", "rarity": 1, "shards": 900, "prisms": 0, "unlock": "", "c": ["#ffbe0b", "#fff3b0"], "t": ["Soleil", "Sun"]},
	{"id": "braise", "rarity": 1, "shards": 1100, "prisms": 0, "unlock": "", "c": ["#ff4d2e", "#ffb347"], "t": ["Braise", "Ember"]},
	{"id": "neige", "rarity": 1, "shards": 1300, "prisms": 0, "unlock": "", "c": ["#e8f6ff", "#7fd6ff"], "t": ["Neige", "Snow"]},
	{"id": "echo", "rarity": 1, "shards": 1500, "prisms": 0, "unlock": "", "c": ["#34e0e0", "#0b3c5d"], "t": ["Écho", "Echo"]},
	{"id": "orage", "rarity": 1, "shards": 1800, "prisms": 0, "unlock": "", "c": ["#5b5fef", "#f4f142"], "t": ["Orage", "Storm"]},
	{"id": "spectre", "rarity": 2, "shards": 2500, "prisms": 10, "unlock": "", "c": ["#9ad7ff", "#5a3cff"], "t": ["Spectre", "Wraith"]},
	{"id": "nebuleuse", "rarity": 2, "shards": 3000, "prisms": 12, "unlock": "", "c": ["#3d1a78", "#ff5ac8"], "t": ["Nébuleuse", "Nebula"]},
	{"id": "lanterne", "rarity": 2, "shards": 3500, "prisms": 15, "unlock": "", "c": ["#ffd166", "#ff7b00"], "t": ["Lanterne", "Lantern"]},
	{"id": "vitrail", "rarity": 2, "shards": 4000, "prisms": 20, "unlock": "", "c": ["#ff3d7f", "#3ae0ff"], "t": ["Vitrail", "Stained glass"]},
	{"id": "gardien", "rarity": 3, "shards": 0, "prisms": 0, "unlock": "ach:a_h1000", "c": ["#0d1b3d", "#34e0e0"], "t": ["Gardien du Silence", "Silence Keeper"]},
	{"id": "couronne", "rarity": 3, "shards": 0, "prisms": 0, "unlock": "level:50", "c": ["#ffd700", "#b388ff"], "t": ["Couronne d'échos", "Crown of Echoes"]},
	{"id": "tisseur", "rarity": 3, "shards": 0, "prisms": 60, "unlock": "", "c": ["#1a1f6b", "#9df9ff"], "t": ["Tisseur d'étoiles", "Star Weaver"]},
	{"id": "pelerin", "rarity": 3, "shards": 0, "prisms": 80, "unlock": "weekly_gold:4", "shop_after_days": 60, "c": ["#3b2a8f", "#ffcf4d"], "t": ["Pèlerin", "Pilgrim"]},
]

const TRAILS := [
	{"id": "t_none", "shards": 0, "prisms": 0, "unlock": "", "t": ["Aucune", "None"]},
	{"id": "t_gold", "shards": 300, "prisms": 0, "unlock": "", "t": ["Poussière d'or", "Gold dust"]},
	{"id": "t_bubbles", "shards": 500, "prisms": 0, "unlock": "", "t": ["Bulles cyan", "Cyan bubbles"]},
	{"id": "t_feathers", "shards": 700, "prisms": 0, "unlock": "", "t": ["Plumes", "Feathers"]},
	{"id": "t_sparks", "shards": 900, "prisms": 0, "unlock": "", "t": ["Étincelles", "Sparks"]},
	{"id": "t_fireflies", "shards": 1200, "prisms": 0, "unlock": "", "t": ["Lucioles", "Fireflies"]},
	{"id": "t_runes", "shards": 1600, "prisms": 5, "unlock": "", "t": ["Runes", "Runes"]},
	{"id": "t_comet", "shards": 2200, "prisms": 8, "unlock": "", "t": ["Comète", "Comet"]},
	{"id": "t_aurora", "shards": 3000, "prisms": 12, "unlock": "", "t": ["Aurore boréale", "Northern lights"]},
	{"id": "t_twin", "shards": 0, "prisms": 0, "unlock": "ach:a_each_higher", "t": ["Ombre jumelle", "Twin shadow"]},
]

const ECHO_FX := [
	{"id": "e_cyan", "shards": 0, "prisms": 0, "unlock": "", "t": ["Cyan", "Cyan"]},
	{"id": "e_amethyst", "shards": 600, "prisms": 0, "unlock": "", "t": ["Améthyste", "Amethyst"]},
	{"id": "e_frost", "shards": 1000, "prisms": 0, "unlock": "", "t": ["Givre", "Frost"]},
	{"id": "e_gold", "shards": 1800, "prisms": 5, "unlock": "", "t": ["Or", "Gold"]},
	{"id": "e_stars", "shards": 2800, "prisms": 10, "unlock": "", "t": ["Constellation", "Constellation"]},
	{"id": "e_glyphs", "shards": 0, "prisms": 0, "unlock": "codex:40", "t": ["Glyphes anciens", "Ancient glyphs"]},
]

# cost[i] = [éclats, prismes] pour passer au niveau i+1 ; val[i] = effet au niveau i+1
const RELICS := {
	"slots_at_level": [8, 25],
	"active_in_daily": false,
	"active_in_weekly": false,
	"list": [
		{"id": "r_purse", "cost": [[600, 0], [1500, 5], [3000, 12]], "val": [0.10, 0.15, 0.20], "t": ["Bourse", "Purse"]},
		{"id": "r_memory", "cost": [[700, 0], [1500, 5], [3000, 12]], "val": [0.10, 0.15, 0.20], "t": ["Mémoire", "Memory"]},
		{"id": "r_magnet", "cost": [[800, 0], [1500, 5], [3000, 12]], "val": [3, 5, 7], "t": ["Aimant", "Magnet"]},
		{"id": "r_hourglass", "cost": [[900, 0], [1500, 5], [3000, 12]], "val": [2.0, 3.0, 4.0], "t": ["Sablier", "Hourglass"]},
		{"id": "r_lantern", "cost": [[900, 0], [1500, 5], [3000, 12]], "val": [0.10, 0.15, 0.20], "t": ["Lanterne", "Lantern"]},
		{"id": "r_foresight", "cost": [[1000, 0], [1500, 5], [3000, 12]], "val": [1.0, 1.5, 2.0], "t": ["Écho prévoyant", "Foresight"]},
		{"id": "r_trophy", "cost": [[800, 0], [1500, 5], [3000, 12]], "val": [150, 120, 100], "t": ["Trophée", "Trophy"]},
		{"id": "r_cartographer", "cost": [[700, 0], [1500, 5], [3000, 12]], "val": [2, 3, 4], "t": ["Cartographe", "Cartographer"]},
	],
}

const SANCTUARY := [
	["s_lamp", 200], ["s_plant", 300], ["s_banner", 400], ["s_bell", 500],
	["s_rug", 600], ["s_fountain", 800], ["s_map", 900], ["s_crystal", 1000],
	["s_shelf", 1200], ["s_window", 1400], ["s_orrery", 1600], ["s_statue", 1800],
	["s_aquarium", 2000], ["s_portal", 2400], ["s_stars", 2700], ["s_throne", 3000],
]

const CODEX_REWARD := {"traps": 10, "floors": 5, "pages": 15, "people": 5, "full": 10}  # prismes

# ---------- Vidéos récompensées ----------
const ADS := {
	"extra_life": {"p0": true, "cap_day": 5, "per_run": 1, "min_run_m": 30, "hide_after_refusals": 2},
	"double_loot": {"p0": true, "cap_day": 5, "min_loot": 15, "mult": 2, "run_shards_only": true},
	"bonus_chest": {"p0": true, "cap_day": 1, "mult": 2, "prisms_doubled": false},
	"mission_reroll": {"p0": true, "cap_day": 2, "alt_cost": 60},
	"skin_trial": {"p0": true, "cap_day": 2, "runs": 3},
	"echo_shield": {"p0": false, "cap_day": 3, "free_mode_only": true},
	"streak_rekindle": {"p0": false, "cap_week": 1, "alt_cost": 150},
	"max_ad_content_rating": "PG",
	"never_gives_prisms": true,
}
```

Note : `%d` dans les missions adaptatives est remplacé par la cible calculée (`t[lang] % cible`).

---

## 7. Changements de code nécessaires (pour le dev)

| Fichier | Changement | Raison |
|---|---|---|
| `tower.gd` | Remplacer « 75 % de chance, 1 ou 3 éclats » par « 1 groupe par section : 1 (40 %), 3 (45 %), arc de 5 (15 %) » + un grand éclat (valeur 5) tous les ~60 m | Passer de ~0,126 à ~0,35 éclat généré par mètre |
| `world.gd` | Compter les stats d'ascension : `turns`, `jumps`, `saws_passed`, `moving_saws_passed`, `lasers_passed`, `life_m[]`, `life1_m`, `turns_life`, `engrave_types`, `grand_shards`, `tide_deaths`. Appliquer reliques (sauf Tour du jour et défi) et `echo_shield` | Les missions et les succès en dépendent |
| `game_state.gd` | Nouveaux champs : `prisms`, `xp`, `level`, `missions{day, list, progress, rerolls}`, `calendar_idx`, `calendar_last_day`, `streak_freeze_week`, `weekly{week, best, tiers}`, `ach{}`, `stats{}` cumulées, `trails[]`, `trail`, `echo_fx[]`, `fx`, `relics{id: niveau}`, `relic_slots[]`, `codex{}`, `sanctuary[]`, `ads_today{placement: n}`, `skin_trial{id, runs}`. Migration : conserver `skins`/`shards`. `start_daily()` : remplacer `5 + 5 × mini(streak, 6)` par la formule `DAILY`, et la remise à 1 par la division par 2 + gel | Nouvelle économie et série non punitive |
| `ads.gd` | `is_ready()` doit interroger le vrai SDK. Compteur **par emplacement** (`ads_today`) avec les plafonds `ADS`. Intégration UMP avant la 1re requête. `on_cancel` ne retire jamais rien | Plafonds, consentement, honnêteté |
| `main.gd` | Résumé : ×2 butin (bouton secondaire) + une seule jauge « la plus proche ». Écrans nouveaux : Missions, Calendrier, Défi hebdo, Codex, Reliques (onglet de Tenues). Offre +1 vie : seuil 30 m et masquage après 2 refus | Boucles §3 |
| nouveau `economy.gd` | Le bloc §6 | Une seule source de vérité pour l'équilibrage |

Ordre de priorité :
1. **P0** : économie de base (ramassage, formule de fin d'ascension), missions, calendrier, série non punitive, niveaux, 19 tenues, traînées, 5 pubs P0, UMP.
2. **P1** : succès, défi hebdo, effets d'écho, reliques, étagère de trophées, codex, pubs P1.
3. **P2** : sanctuaire complet.

---

## 8. Mesures à suivre après le lancement (pour régler les constantes)

- Rétention J1, J7 et J30. Seuils d'alerte : J1 < 28 %, J7 < 8 %.
- Vues par DAU, par emplacement. Si le ×2 butin dépasse 45 % d'acceptation, la récompense est trop forte ou le gain en jeu trop faible.
- Délai médian jusqu'au 1er achat (cible : J1) et jusqu'au 1er épique (cible : J12-J16).
- Solde moyen d'éclats non dépensés. S'il dépasse 3 000, il y a inflation : ajouter des puits ou réduire les sources méta.
- Taux de complétion de chaque mission. Une mission sous 30 % : trop dure, la reclasser. Au-dessus de 95 % : trop facile.

---

## 9. Sources

**Livres de la persona**
- E. Adams & J. Dormans, *Game Mechanics: Advanced Game Design*, ch. 4 (économies internes : sources, drains, converters, traders) et ch. 6 (feedback).
- R. Koster, *A Theory of Fun for Game Design*, 2e éd., en particulier ch. 10 (éthique) et la boucle de maîtrise.

**eCPM et monétisation publicitaire**
- Appodeal, *Mobile eCPM Report Q4 2024* : appodeal.com/the-mobile-ecpm-report-updated-q4-2024-view (PDF : appodeal.com/wp-content/uploads/2025/03/Quarterly_Mobile_eCPM_Report_-_Q4_2024.pdf)
- MAF, *Mobile ads eCPM* (AU 13,80 ; CH 12,20 ; US 15,15) : maf.ad/en/blog/mobile-ads-ecpm/
- RevenueLab, *AdMob eCPM benchmarks 2026* : revenuelab.fyi/blog/admob-ecpm-benchmarks-2026
- Playwire, *AdMob eCPM benchmarks* : playwire.com/blog/admob-ecpm-benchmarks-what-publishers-should-expect
- TopOn, rapport 2025 H1 (rewarded Android −7 % sur un an) : mores.toponad.com
- Unity, *Rewarded ad systems* (23,8 % d'engagement entre niveaux, plus de 60 % des joueurs intéressés) : unity.com/blog/rewarded-ad-systems
- PocketGamer.biz, *Unity: global rewarded ad engagement rose by 32 % in 2023* : pocketgamer.biz/unity-global-rewarded-ad-engagement-rose-by-32-in-2023
- Core Loops, *Ad revenue in mobile games* (formule ARPDAU) : coreloopsconsulting.substack.com/p/ad-revenue-in-mobile-games
- Unity, *What is ARPDAU* : unity.com/blog/what-is-arpdau

**Rétention**
- GameAnalytics, *2025 Mobile Gaming Benchmarks* : investgame.net/wp-content/uploads/2025/02/2025-GameAnalytics-Mobile-Gaming-Benchmarks.pdf ; synthèse : gamedevreports.substack.com/p/gameanalytics-mobile-gaming-benchmarks
- GameAnalytics 2026 (mobile et PC), synthèse : gamedevreports.substack.com/p/gameanalytics-mobile-and-pc-game
- Appodeal, *Mobile Casual Benchmarks Report 2025* : gameindustrylibrary.com/documents/mobile-casual-benchmarks-report-2025

**Conformité**
- Google Play, programme Families et SDK auto-certifiés : support.google.com/googleplay/android-developer/answer/9893335, /answer/12918983, /answer/9283445
- AdMob, publicités pour les enfants et contenu : support.google.com/admob/answer/6223431
- AdMob et RGPD, SDK UMP : developers.google.com/admob/android/privacy/gdpr ; CMP certifié (EEE/UK 16/01/2024, Suisse 31/07/2024) : support.google.com/admob/answer/14189727 et /answer/13554116
- Digital Fairness Act : twobirds.com/en/insights/2025/eu-–-consultation-on-the-digital-fairness-act ; Osborne Clarke, *Digital Fairness Act in a Nutshell* (PDF) ; galaxus.de (lignes directrices UE sur les microtransactions) ; pocketgamer.biz (consultation DFA)

**Limite de la recherche** : les pages web ont été lues via des synthèses de recherche. La lecture complète de certaines pages a été bloquée par le réseau du bac à sable (par exemple blog.playio.co, non autorisé). Les eCPM varient de ±30 % selon la source et le trimestre : il faut recaler §4.2 avec les vraies données AdMob après 2 semaines de production.

**Simulation** : script Python sur 30 jours (hors livrable). Paramètres : ceux du §6. Joueur moyen actif : 15 puis 10 min par jour, hauteur max de 120 m à J1 jusqu'à 380 m à J30.
