# Inventaire des animations par personnage

Ce document fixe **combien d'animations** il faut par personnage, **lesquelles**, et dans
quel ordre on les fait.

**Budget : 100 à 120 animations par personnage, communes et propres comprises.** Nous
sommes deux à produire, tout à la main, donc on garde seulement ce qui sert vraiment au
combat en duel. Le reste est coupé (§ 6).

---

## 1. Comment on compte

**Une animation = une action que le joueur voit**, comme dans les décomptes des jeux de
combat. Les petites transitions d'une même action ne comptent pas à part :

- départ, boucle et arrêt d'une marche ;
- entrée, boucle et sortie d'une posture ;
- réception d'un saut.

Les fichiers sont donc plus nombreux que les animations. Aujourd'hui, 57 animations
communes sont faites, ce qui représente 80 fichiers dans `anims/`.

### Repères

| Jeu | Actions par personnage |
|---|---|
| Hollow Knight (personnage d'action, pas un jeu de combat) | 35 à 40 |
| Street Fighter 6 | 60 à 85 |
| Tekken 8 | 120 à 180 (movelist moyenne ≈ 145 coups, sans les communes) |
| **Nous** | **100 à 120, communes comprises** |

Le minimum pour un jeu de combat complet (SF6, Guilty Gear Strive, Tekken 8) tourne
autour de 50 à 70 actions :

| Catégorie | Actions |
|---|---|
| Déplacements | 10 à 12 |
| Défense et réactions | 10 à 15 |
| Normaux au sol | 12 à 18 |
| Aériens | 6 à 9 |
| Choppes et universelles | 4 à 6 |
| Spéciaux et super | 6 à 15 |
| Mise en scène | 3 à 5 |

Notre déplacement et notre défense dépassent déjà ces repères, parce que c'est là que le
style « stickman animé » se voit le plus. Ils sont faits, on les garde. Le reste est donc
serré au plus juste.

---

## 2. Règles à appliquer à toutes les attaques

Ce sont tes retours ; ils valent pour toute la suite.

1. **La garde se défait pendant l'attaque.**
   - Le bras qui ne frappe pas recule et sert de contrepoids : les épaules tournent.
   - La garde revient seulement pendant la récupération.
   - Ce retour *est* la fenêtre où l'on peut être puni.
2. **Chaîne du mouvement, des pieds vers le poing.** Le pied d'appui pivote, puis la hanche
   tourne, puis l'épaule, puis le bras ou la jambe. Pour un coup de pied :
   - le buste penche en arrière ;
   - le bras opposé balance ;
   - la hanche s'ouvre ;
   - le pied d'appui tourne sur la plante.
3. **La garde n'est affichée qu'au neutre.** Elle peut être basse ou relâchée selon le
   personnage.
4. **Trois phases par coup** : démarrage, actif, récupération, avec une anticipation lisible.
5. **Le repos est l'état par défaut, pas la garde.**
   - Le personnage se déplace depuis son repos, de façon détendue.
   - La garde n'apparaît que si le joueur la maintient.
   - Il en ressort dès qu'il la relâche.
6. **Deux gardes.**
   - G tenu donne la garde **ouverte** : prêt à se battre, mains avancées.
   - La garde **fermée** sert seulement à bloquer : poings devant le visage. On la prend en
     reculant (← en garde, comme dans Tekken), avant et après un blocage.
   - Les deux gardes ont les mêmes jambes : seuls le buste et les bras changent.
7. **Une animation à la fois.**
   - Chaque animation est faite pose par pose, puis vérifiée en planche et en stroboscopie.
   - Elle doit marcher dans toutes les situations où elle sert. Par exemple, une parade doit
     paraître naturelle contre un coup de poing comme contre un coup de pied, haut ou moyen.

---

## 3. Animations communes : 74

Faites une fois, partagées par tous les personnages. Un personnage peut en remplacer une par
sa propre version ; ce remplacement compte alors dans son budget propre (§ 4).

### 3.1 Postures : 7, toutes faites

| Animation | Fichiers |
|---|---|
| Repos (état par défaut) | `idle_repos` |
| Mise en garde (repos → garde) | `mise_en_garde` |
| Sortie de garde (garde → repos) | `sortie_de_garde` |
| Garde ouverte, respiration | `garde_ouverte_idle`, `garde_ouvrir` |
| Garde fermée, respiration | `garde_idle`, `garde_fermer` |
| Accroupi : entrée, respiration, sortie | `accroupi_entree`, `accroupi_idle`, `accroupi_sortie` |
| Accroupi depuis le repos, une main au sol | `accroupi_repos_*` |

### 3.2 Déplacements : 19, tous faits

| Animation | Fichiers |
|---|---|
| Marche détendue avant : départ, boucle, arrêt court, arrêt en un pas | `marche_detendue`, `marche_detendue_depart`, `marche_detendue_arret_*` |
| Marche détendue arrière : départ, boucle, arrêt en un pas, arrêt en deux pas | `marche_detendue_arriere*` |
| Marche avant en garde, marche arrière en garde | `marche_avant`, `marche_arriere` |
| Course : départ, boucle, arrêt depuis chaque pied | `course*` |
| Sprint : départ, boucle, freinage en glissade | `sprint*` |
| Pas chassé avant, pas chassé arrière | `dash_avant`, `dash_arriere` |
| Saut neutre, avant, arrière ; réception légère | `saut_*`, `reception` |
| Saut boosté neutre, avant, arrière ; réception lourde | `saut_booste_*`, `reception_lourde` |
| Propulsion avant et arrière, rasante ou haute (4) | `propulsion_*` |
| Demi-tour | `demi_tour` |

### 3.3 Défense : 26, toute faite

| Animation | Fichiers |
|---|---|
| Garde accroupie tenue : boucle, entrée, sortie, fermer, ouvrir | `garde_basse*` |
| Blocage bas debout | `blocage_bas` |
| Recul sur garde, haut et bas × léger, moyen, lourd (6) | `recul_garde_*` |
| Garde repoussée, garde brisée | `garde_repoussee`, `garde_brisee` |
| Parades : poing haut, pied haut, moyen, bas (4) ; fenêtre de contre | `parade_*` |
| Esquives : sway, slip, se baisser, pas de côté, saut arrière, saut sur place (6) | `esquive_*` |
| Armure (Power Crush), en couche | `armure_encaisse` |
| Casser une projection, projection cassée | `casse_projection`, `projection_cassee` |
| Être paré, haut et milieu (2) | `etre_pare_haut`, `etre_pare_bas` |

### 3.4 Réactions debout : 7, 5 faites

| Animation | Fichier prévu |
|---|---|
| Touché à la tête, léger (fait) | `touche_tete_leger` |
| Touché à la tête, lourd (la tête part, recul d'un pas) (fait) | `touche_tete_lourd` |
| Touché au ventre, léger (fait) | `touche_ventre_leger` |
| Plié en deux (ventre lourd) (fait) | `touche_ventre_lourd` |
| Touché à la jambe (fait) | `touche_jambe` |
| Touché accroupi | `touche_accroupi` |
| Sonné, titubant (après un contre ou une garde brisée, boucle courte) | `sonne` |

Les variantes « moyen » se font en jouant la légère plus fort, ou la lourde plus court ; on
n'en fait pas de fichier.

### 3.5 Chutes, au sol, relevés, KO : 8, à faire

| Animation | Fichier prévu |
|---|---|
| Propulsé en arrière, chute sur le dos | `chute_arriere` |
| Fauché (les jambes partent, tombe sur le dos) | `fauche` |
| Effondrement lent vers l'avant (crumple) | `effondrement` |
| Au sol sur le dos (boucle) | `au_sol` |
| Touché au sol | `touche_au_sol` |
| Relevé normal | `releve` |
| Relevé en roulade arrière (tech roll) | `releve_roulade` |
| Inconscient au sol (KO, boucle) | `ko_au_sol` |

Le KO lui-même n'a pas d'animation propre : c'est la chute qui l'a causé, puis `ko_au_sol`.
Le ralenti final est géré par le moteur.

### 3.6 En l'air et mur : 4, à faire

| Animation | Fichier prévu |
|---|---|
| Lancé en l'air (par un lanceur) | `lance` |
| Touché en l'air (jongle) | `touche_en_lair` |
| Retombée au sol avec rebond | `retombee` |
| Plaqué au mur, puis glisse au sol | `plaque_mur` |

### 3.7 Universelles : 3, à faire

| Animation | Fichier prévu |
|---|---|
| Saisie dans le vide (projection ratée) | `saisie_ratee` |
| Frapper un adversaire au sol | `frappe_au_sol` |
| Activation de la Heat, si on garde cette mécanique | `heat_activation` |

### Total des communes

| Bloc | Faites | À faire |
|---|---|---|
| 3.1 Postures | 7 | 0 |
| 3.2 Déplacements | 19 | 0 |
| 3.3 Défense | 26 | 0 |
| 3.4 Réactions debout | 5 | 2 |
| 3.5 Chutes, sol, relevés, KO | 0 | 8 |
| 3.6 En l'air et mur | 0 | 4 |
| 3.7 Universelles | 0 | 3 |
| **Total : 74** | **57** | **17** |

---

## 4. Animations propres à chaque personnage : 42

C'est sa movelist. Les boutons sont les mêmes pour tous, mais chaque personnage y met
**ses** coups. Quatre boutons, comme Tekken : □ = 1 poing gauche, △ = 2 poing droit,
× = 3 pied gauche, ○ = 4 pied droit.

| Catégorie | Contenu | Nombre |
|---|---|---|
| Boutons seuls | 1, 2, 3, 4 | 4 |
| Direction + bouton | 6 coups choisis : un lanceur, un coup bas, un coup qui avance, un coup lourd lent… | 6 |
| Accroupi et en se relevant | 3 coups accroupi (dont un balayage), 1 coup en se relevant | 4 |
| Suites de chaînes | les 2e et 3e coups de 2 ou 3 enchaînements | 6 |
| En courant, en saut | 1 coup en courant, 2 coups sautés | 3 |
| Spéciaux | les coups signature ; arme ou pouvoir ici pour les personnages qui en ont | 5 |
| Power Crush | 1 coup avec armure | 1 |
| Contre après parade | part dans la fenêtre `contre` des parades communes | 1 |
| Projections | 2 duos (celui qui saisit + celui qui subit) | 4 |
| Heat Smash et Rage Art | 1 Heat Smash, 1 Rage Art en duo (2) | 3 |
| Mise en scène | intro, victoire, provocation | 3 |
| Remplacements | sa garde ouverte et son repos | 2 |
| **Total** | | **42** |

Les suites de chaînes réutilisent les boutons seuls. Une chaîne `1,2,4` coûte donc seulement
2 animations de plus que le `1` :

- chaque coup peut finir seul (récupération courte) ;
- chaque coup peut aussi partir vers la suite (annulation).

**Armes et pouvoirs.** Pas de couche commune. Comme tous les coups d'un personnage lui sont
propres, un personnage à bâton fait simplement ses normaux avec le bâton, et un personnage à
pouvoir met ses pouvoirs dans ses 5 spéciaux. Ça reste dans les 42.

- Les effets (éclairs, cristaux, onde) se dessinent dans `vfx.gd` et ne comptent pas.
- Les réactions des victimes restent les communes.
- Un personnage très chargé peut prendre jusqu'à 10 animations de plus sur une seule
  catégorie (spéciaux ou chaînes). Il reste ainsi sous 120.

**Déjà là.** `direct` et `coup_de_pied_ventre` sont deux coups de test qui servent aux duos.
Le premier personnage les reprendra ou les refera selon les règles du § 2.

---

## 5. Le total

| | Animations |
|---|---|
| Communes | 74 (57 faites, 17 à faire) |
| Propres à un personnage | 42 |
| **Par personnage** | **116** |

Ce qu'il reste à produire :

- **1er personnage** : 22 communes + 42 propres = **64** ;
- **chaque personnage suivant** : **42** seulement, puisque les communes existent déjà ;
- **version jouable à 2 personnages** : 64 + 42 = **106**.

---

## 6. Ce qui a été coupé, et pourquoi

| Coupé | Avant | Raison |
|---|---|---|
| Couche objets et armes | 87 | Les armes sont propres à certains personnages et passent dans leurs coups (§ 4). Pas d'objets du décor. |
| Couche pouvoirs | 22 | Même chose : les pouvoirs sont des spéciaux. Les effets sont dans `vfx.gd`. |
| Plusieurs adversaires, foule | 5 | Le jeu est un duel. |
| Clinch et lutte debout | 15 | Un lutteur peut en faire une de ses 2 projections. |
| Combat au sol (monture, stomp…) | 13 → 1 | On garde une seule frappe au sol commune. |
| Murs et décor (traverser, balcon, étage, sol qui cède…) | 14 → 1 | On garde seulement le plaqué au mur. |
| En l'air (vrille, Tornado, culbute, plié en l'air…) | 12 → 3 | Un lancé, un touché, une retombée suffisent pour jongler. |
| KO | 6 → 1 | Le KO réutilise la chute qui l'a causé. |
| Réactions, chutes, au sol et relevés (positions, roulades, ramper…) | 24 + 22 → 14 | Les « moyens » se déduisent des légers et des lourds ; une seule position au sol, un relevé normal, un relevé rapide. |
| Projections communes | 13 → 1 | Les projections sont propres à chaque personnage, 2 chacun. |
| Postures restantes : essoufflée, aura de Heat, dos tourné | 3 | L'essoufflement et l'aura se font en couche ou en effet ; le demi-tour suffit pour le dos tourné. |
| Déplacements restants : roulades, saltos, mur, dash accroupi, petit saut, enjamber | 9 | Les esquives faites couvrent ces besoins ; un acrobate peut en mettre un dans ses spéciaux. |
| Heat (Dash, sortie, victime de l'onde) | 4 → 1 | La victime de l'onde réutilise `chute_arriere`. |
| Movelist façon Tekken | 175 → 42 | Taille d'un personnage de Street Fighter, pas de Tekken. |

---

## 7. Décisions prises

1. **2D pure.** Pas de pas de côté ni de profondeur. Le seul pivot (`esquive_cote`) est une
   esquive vue de face.
2. **Commandes à la manette, comme Tekken.** Quatre boutons d'attaque plus les directions,
   sur la manette PS5. On reprend les commandes des jeux de combat existants au lieu d'en
   inventer. Les touches du clavier de la démo sont provisoires. Le reste du game design est
   décidé plus tard.
3. **Chutes animées à la main**, sans physique de chiffon.
4. **Parades et contre-attaques.**
   - Seules les parades de base sont communes, une par type de coup : poing haut, pied haut,
     moyen, bas.
   - Les contre-attaques qui suivent une parade sont propres à chaque personnage.
   - La parade commune ouvre seulement une fenêtre `contre` où elles peuvent partir.
5. **2 personnages** pour la première version jouable.
6. **Budget de 100 à 120 animations par personnage**, communes comprises : 74 communes et
   42 propres.
7. **Armes, pouvoirs et objets** : pas de couche commune. Ils vivent dans les coups propres
   des personnages qui en ont.
8. **Duel seulement** : pas de foule ni d'adversaires multiples.

---

## 8. Ordre de production

| Phase | Contenu | Animations | État |
|---|---|---|---|
| 1. Socle de déplacement et de défense | postures, déplacements, défense | 52 | fait |
| 2. Encaisser | réactions debout (7), chutes, sol, relevés, KO (8) | 15 | en cours (5/15) |
| 3. Personnage 1, le cœur | boutons seuls, directions, accroupi, chaînes, course et saut | 23 | |
| 4. Jongles et mur | en l'air (3), plaqué au mur (1), testés avec le lanceur du personnage 1 | 4 | |
| 5. Personnage 1, le reste | projections, spéciaux, Power Crush, contre, Heat Smash, Rage Art, mise en scène, remplacements | 19 | |
| 6. Universelles | saisie ratée, frappe au sol, activation de la Heat | 3 | |
| 7. Personnage 2 | ses 42 animations propres | 42 | |

On s'arrête à la fin de chaque phase pour tester en jeu avant d'aller plus loin.

**En cours, phase 2.** Faits : `touche_tete_leger`, `touche_tete_lourd` (duos contre `direct`), `touche_ventre_leger` et `touche_ventre_lourd` (duos contre `coup_de_pied_ventre`), `touche_jambe` (duo contre `pied_bas`). La suivante : `touche_accroupi`.

---

## Sources

- Recherche partagée sur SF6, Guilty Gear Strive, Tekken 8 et Hollow Knight : actions minimales
  par catégorie, et décompte par jeu.
- [TekkenDocs, statistiques Tekken 8 (nombre de coups par personnage)](https://tekkendocs.com/t8/stats)
- [Iron Fist Insights, glossaire (tech roll, quickrise, Heat, Tornado…)](https://ironfistinsights.com/docs/glossary/)
