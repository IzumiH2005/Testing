# Inventaire des animations par personnage

Ce document fixe **combien d'animations** il faut par personnage et **lesquelles**,
avant de commencer la production. Il s'appuie sur Tekken 8, qui sert de référence,
et sur les deux vidéos de stickman analysées (clinch, sol, objets, pouvoirs, foule).

À valider avant de toucher aux animations : les questions ouvertes sont en § 7.

---

## 1. Les chiffres de Tekken 8

### Combien de coups par personnage

| Personnage | Coups (movelist) | Remarque |
|---|---|---|
| Yoshimitsu | 313 | le plus gros, beaucoup de postures |
| King | 217 | lutteur, beaucoup de projections et de chaînes de chopes |
| Hwoarang | 210 | 4 postures de jambes |
| Claudio | 102 | personnage simple |
| Shaheen | 91 | le plus petit |
| **Moyenne** | **≈ 145** | sur environ 40 personnages |
| **Total du jeu** | **≈ 6 200 à 6 400** | selon la façon de compter |

Comment ces chiffres sont comptés (TekkenDocs, d'après les movelists du wiki Wavu) :

- chaque coup d'une chaîne compte à part : `1,2,1` = 3 coups ;
- les projections comptent ;
- les variantes renforcées en Heat ne comptent pas toujours, d'où l'écart entre les sources ;
- les chaînes automatiques de 10 coups ne comptent pas.

### Ce que ces chiffres ne comptent pas

La movelist ne liste que ce que le joueur **déclenche**. Tout le reste est en plus :

- les animations communes du système : marcher, sauter, bloquer, se relever, etc. ;
- les **réactions** aux coups : être touché, lancé, plaqué au mur, mis au sol ;
- les **victimes** des projections, de la Heat Smash et de la Rage Art, qui sont des animations à deux ;
- les transitions d'entrée et de sortie des postures ;
- l'intro, les poses de victoire et de défaite, les provocations.

Un personnage de Tekken représente donc nettement plus d'animations que ses 145 coups.
Les communes sont faites une seule fois et partagées. Chaque personnage peut aussi
remplacer certaines communes par sa propre version (sa garde, sa marche, son intro).

### Mécaniques de Tekken 8 qui demandent des animations

| Mécanique | Ce qu'il faut animer |
|---|---|
| **Heat** (une fois par round) | activation (Heat Burst), Heat Dash, Heat Engager, Heat Smash |
| **Rage Art** | une attaque cinématique à deux, propre à chaque personnage |
| **Power Crush** | coup avec armure : on encaisse sans broncher |
| **Tornado** | la vrille en l'air qui prolonge un combo, une fois par combo |
| **Murs** | wall splat, wall bound, wall break, hard wall break (2 coups), balcony break |
| **Sol** | floor break, floor blast, bound (rebond au sol) |
| **Au sol** | tech roll, quickrise, roulades, coups en se relevant, rester au sol |
| **Projections** | casse avec 1, 2 ou 1+2, saisies de face, de côté et de dos |

Production chez Bandai Namco : capture de mouvement **retravaillée à la main**, pas pour
tous les personnages (les Mishima sont animés à la main), sous Maya et MotionBuilder, avec
plusieurs équipes. Nous animons tout à la main, en poses-clés : c'est notre force pour le
style « animation stickman », mais cela demande un inventaire strict.

---

## 2. Ce que montrent les deux vidéos

### Vidéo 1 : *StickFight – More practice* (noir contre rouge, puis d'autres combattants)

- **Pas de garde permanente.** Les combattants sont bas, penchés vers l'avant, les mains
  souvent basses. Ils se mettent en garde seulement à l'approche ou pour encaisser.
- **Tout le corps frappe.** Pour un coup de pied, le buste part en contrepoids, les bras
  balancent et le pied d'appui pivote.
- **Clinch et lutte.** Saisies, poussées et tirages au contact, genoux, amenées au sol.
- **Combat au sol.** Monture, coups au sol (ground-and-pound), écrasements au pied.
- **Chutes lourdes.** Les corps tombent à plat et s'empilent. Un combattant se relève
  pendant qu'un autre reste au sol.
- **Plusieurs adversaires** qui arrivent l'un après l'autre.
- Un peu de sang rouge.

### Vidéo 2 : bleu contre une foule de stickmen blancs

- **Objets du décor.** Il prend une chaise, frappe avec, se protège avec, puis s'assoit dessus.
- **Acrobaties.** Saltos, coups de pied sautés, déplacements flous très rapides.
- **Arme.** Un bâton lumineux qui tournoie et taille en arcs.
- **Pouvoirs.**
  - Télékinésie électrique.
  - Bouclier de cristal de glace qui arrête une balle.
  - Bloc de cristal lancé qui écrase un groupe d'ennemis.
- **Ennemis armés** : pistolet, couteau.
- **Foule.** Beaucoup d'ennemis en même temps, des corps qui volent, des débris.

### Règles à appliquer à toutes les attaques

Ce sont tes retours ; ils valent pour toute la suite :

1. **La garde se défait pendant l'attaque.** Le bras qui ne frappe pas recule et sert de
   contrepoids (les épaules tournent). La garde revient seulement pendant la récupération,
   et ce retour *est* la fenêtre où l'on peut être puni.
2. **Chaîne du mouvement, des pieds vers le poing.** Le pied d'appui pivote, puis la hanche
   tourne, puis l'épaule, puis le bras ou la jambe. Pour un coup de pied :
   - le buste penche en arrière ;
   - le bras opposé balance ;
   - la hanche s'ouvre ;
   - le pied d'appui tourne sur la plante.
3. **La garde n'est affichée qu'au neutre**, et elle peut être basse ou relâchée selon le
   personnage, comme dans les vidéos.
4. Chaque coup se découpe en **démarrage, actif, récupération**, avec une anticipation lisible.
5. Le coup de pied du duo de blocage actuel était un test. Il sera refait avec ces règles.

---

## 3. Animations communes (tous les personnages)

Faites une fois, partagées par tous. Un personnage peut remplacer n'importe laquelle
par sa propre version (marquées ✱ quand c'est presque toujours le cas).

### 3.1 Postures et repos — 10

| # | Animation | État |
|---|---|---|
| 1 | Repos (hors combat) | fait |
| 2 | Mise en garde (repos → garde) | fait |
| 3 | Garde, respiration ✱ | fait |
| 4 | Sortie de garde (garde → repos) | |
| 5 | Accroupi, respiration | |
| 6 | Debout → accroupi | |
| 7 | Accroupi → debout | |
| 8 | Garde essoufflée (vie basse) | |
| 9 | Garde en Rage / Heat (couche d'aura) | |
| 10 | Dos tourné, respiration | |

### 3.2 Déplacements — 26

| # | Animation |
|---|---|
| 1-2 | Marche avant ✱, marche arrière ✱ |
| 3-4 | Pas chassé avant (dash), pas chassé arrière (backdash) |
| 5-7 | Course : départ, boucle, freinage en glissade |
| 8 | Dash accroupi (avancer bas, comme un crouch dash) |
| 9-11 | Saut neutre, saut avant, saut arrière |
| 12-13 | Réception légère, réception lourde |
| 14 | Petit saut (passe au-dessus d'un coup bas) |
| 15 | Demi-tour (l'adversaire est passé derrière) |
| 16 | Se retourner depuis dos tourné |
| ~~17-19~~ | ~~Pas de côté~~ : retirés, le jeu est en 2D pure (§ 7) |
| 20-21 | Roulade avant, roulade arrière |
| 22-23 | Salto avant, salto arrière (esquive acrobatique, vidéo 2) |
| 24 | Rebond sur un mur (wall jump) |
| 25 | Course sur le mur (2 ou 3 pas) |
| 26 | Enjamber ou sauter par-dessus un adversaire au sol |

### 3.3 Défense — 20

| # | Animation | État |
|---|---|---|
| 1 | Garde haute tenue | |
| 2 | Garde accroupie tenue | |
| 3 | Blocage bas debout | fait |
| 4-9 | Recul sur garde léger, moyen, lourd × haut et bas | |
| 10 | Garde repoussée (gros coup bloqué, les pieds glissent) | |
| 11 | Garde brisée (bras ouverts, vulnérable) | |
| 12-13 | Parade haute, parade basse (dévier un coup) | |
| 14 | Esquive buste en arrière (sway) | |
| 15 | Esquive en se baissant sous un coup haut | |
| 16 | Esquive de la tête sur le côté (slip) | |
| 17 | Armure : encaisser sans broncher (Power Crush) | |
| 18 | Casser une projection (celui qui se dégage) | |
| 19 | Projection cassée (celui qui est repoussé) | |
| 20 | Être paré (déséquilibré après la parade adverse) | |

### 3.4 Réactions aux coups, debout — 24

| Zone | Animations | Nombre |
|---|---|---|
| Tête | légère, moyenne, lourde, par derrière | 4 |
| Ventre | léger, moyen, lourd, plié en deux | 4 |
| Jambes | légère, lourde (genou qui plie), fauché (tombe) | 3 |
| Accroupi touché | léger, lourd | 2 |
| États spéciaux (contres, gros coups) | vrille sur place, recul titubant, sonné (boucle), effondrement lent (crumple), tombe à genoux, pivote dos tourné, souffle coupé (boucle), recul glissé au sol, tête qui part en arrière | 9 |
| Projeté | propulsé loin, propulsé en vrille | 2 |

### 3.5 En l'air (jongles) — 12

| # | Animation |
|---|---|
| 1-2 | Lancé à la verticale, lancé en vrille |
| 3-4 | Touché en l'air léger, lourd |
| 5 | Culbute en l'air |
| 6 | Tornado (vrille horizontale qui prolonge le combo) |
| 7-8 | Rebond au sol sur le dos, sur le ventre (bound) |
| 9-10 | Retombée sur le dos, sur le ventre |
| 11 | Plié en deux en l'air |
| 12 | Écrasé vers le sol (frappé vers le bas) |

### 3.6 Murs, sol et décor — 14

| # | Animation |
|---|---|
| 1-2 | Plaqué au mur dos au mur, plaqué face au mur (wall splat) |
| 3 | Glisse le long du mur |
| 4 | Rebond sur le mur (wall bound) |
| 5 | Affalé assis contre le mur |
| 6-7 | Traverse le mur, traverse en force (hard wall break) |
| 8 | Bascule par-dessus une rambarde (balcony break) |
| 9 | Le sol cède (floor break) |
| 10 | Écrasé contre le sol (floor blast) |
| 11 | Percute un autre combattant (foule) |
| 12 | Rebond sur un objet du décor |
| 13 | Chute d'un étage |
| 14 | Se relever après la chute d'un étage |

### 3.7 Au sol et relevés — 22

| Groupe | Animations | Nombre |
|---|---|---|
| Positions au sol | sur le dos pieds vers l'adversaire, sur le dos pieds loin, sur le ventre × 2 | 4 |
| Chutes | en arrière, en avant, sur le côté | 3 |
| Touché au sol | sur le dos, sur le ventre | 2 |
| Relevés | normal depuis le dos, normal depuis le ventre, relevé rapide (quickrise), kip-up (relevé sauté) | 4 |
| Tech roll | sur le côté, en arrière | 2 |
| Roulades au sol | arrière, avant, de côté | 3 |
| Coups en se relevant | coup de pied bas, coup de pied moyen | 2 |
| Autres | se retourner au sol, ramper (blessé, vidéo 1) | 2 |

### 3.8 KO — 6

KO en arrière, KO effondré en avant, KO en vrille, KO contre le mur, KO qui glisse au sol,
inconscient au sol (boucle). Le ralenti final est géré par le moteur, il ne demande pas
d'animation.

### 3.9 Projections de base — 13

Une projection est un **duo** : une animation pour celui qui saisit, une pour celui qui subit.

| Projection | Animations |
|---|---|
| Saisie de face, type 1 | 2 |
| Saisie de face, type 2 | 2 |
| Saisie de côté gauche, de côté droit | 4 |
| Saisie de dos | 2 |
| Saisie accroupie (sur un adversaire baissé) | 2 |
| Saisie ratée (dans le vide) | 1 |

Dans Tekken, chaque personnage a ses propres projections. Celles-ci servent de lot par
défaut ; les personnages les remplacent ou en ajoutent (voir § 4).

### 3.10 Clinch et lutte debout (vidéo 1) — 15

| Duo | Animations |
|---|---|
| Entrer en clinch (saisir nuque ou col) | 2 |
| Clinch tenu (boucle, chacun pousse) | 2 |
| Genou en clinch | 2 |
| Coup court en clinch (coude, crochet) | 2 |
| Repousser hors du clinch | 2 |
| Amenée au sol (takedown) | 2 |
| Fauchage depuis le clinch | 2 |
| Se dégager seul | 1 |

### 3.11 Combat au sol (vidéo 1) — 13

| Duo | Animations |
|---|---|
| Monter sur l'adversaire (mount) | 2 |
| Frapper en monture (ground-and-pound) | 2 |
| Renverser celui qui est dessus | 2 |
| Écraser au pied (stomp) | 2 |
| Saisir une jambe depuis le sol (l'autre trébuche) | 2 |
| Coup de pied dans un adversaire au sol | 1 |
| Plonger sur un adversaire au sol | 1 |
| S'asseoir sur l'adversaire (provocation) | 1 |

### 3.12 Système (Heat, Rage) — 4

Activation de la Heat (onde de choc), victime repoussée par l'onde, Heat Dash, sortie de
Heat. La Heat Smash et la Rage Art sont propres à chaque personnage (§ 4).

### 3.13 Plusieurs adversaires (vidéo 2) — 5

Se retourner vite vers un deuxième ennemi, coup en arrière sans se retourner, coup de pied
écarté des deux côtés, pousser un ennemi sur un autre, tenir un ennemi comme bouclier.

### 3.14 Présentation — 6

Intro ✱, victoire ✱ × 2, défaite au temps, provocation ✱, attente à l'écran de sélection ✱.
Elles sont presque toujours remplacées par celles du personnage.

### Total du socle commun

| Bloc | Nombre |
|---|---|
| 3.1 Postures | 10 |
| 3.2 Déplacements | 26 |
| 3.3 Défense | 20 |
| 3.4 Réactions debout | 24 |
| 3.5 En l'air | 12 |
| 3.6 Murs, sol, décor | 14 |
| 3.7 Au sol et relevés | 22 |
| 3.8 KO | 6 |
| 3.9 Projections de base | 13 |
| 3.10 Clinch | 15 |
| 3.11 Combat au sol | 13 |
| 3.12 Système | 4 |
| 3.13 Plusieurs adversaires | 5 |
| 3.14 Présentation | 6 |
| **Total** | **190** |

### 3.15 Couche « objets et armes » (vidéo 2) — environ 87

**Objets** (15, communs à tous) :

- ramasser au sol, ramasser en hauteur, attraper au vol, lâcher ;
- lancer par-dessus l'épaule, de côté, à deux mains (objet lourd) ;
- porter un objet lourd (respiration, marche), poser ;
- frapper avec un objet en horizontal et en vertical ;
- se protéger avec un objet ;
- briser l'objet sur la cible ;
- s'asseoir sur une chaise.

**Armes : un lot par famille** (6 familles × environ 12 = 72) :

- les familles :
  - contondante courte (matraque, pied de chaise) ;
  - longue (bâton, lance : le bâton lumineux de la vidéo) ;
  - lame courte (couteau) ;
  - lame longue (sabre) ;
  - arme à feu (pistolet) ;
  - bouclier ;
- le lot de chaque famille :
  - garde et respiration avec l'arme ;
  - bras porteur pendant la marche ;
  - 3 coups de base ;
  - une chaîne de 3 ;
  - une attaque chargée ;
  - une parade ;
  - dégainer ;
  - ranger ;
  - être désarmé.

Un personnage « maître d'arme » ajoute ses propres coups par-dessus, comme un style à part
entière.

### 3.16 Couche « pouvoirs » (vidéo 2) — environ 22

| Groupe | Animations |
|---|---|
| Charge | canaliser (boucle), relâcher |
| Projectiles | à une main, à deux mains, rafale (boucle), frapper le sol (onde) |
| Bouclier | invoquer, tenir, encaisser un impact, dissiper |
| Télékinésie | saisir à distance, soulever et tenir, projeter, écraser vers le bas |
| Téléportation | disparaître, réapparaître |
| Transformation | activer l'aura |
| Victime | soulevée par télékinésie (boucle), électrocutée (boucle), gelée, brûlée, repoussée par une onde |

Les effets visuels (éclairs, cristaux, onde) sont à part : ils se dessinent dans `vfx.gd`,
pas dans le squelette.

**Socle commun complet : environ 300 animations** (190 + 87 + 22).

---

## 4. Animations propres à chaque personnage

C'est l'équivalent de la movelist Tekken. Mêmes boutons pour tous, mais chaque personnage
y met **ses** coups. Gabarit pour un personnage « moyen » (≈ 145 coups, comme la moyenne
Tekken) ; un personnage simple peut descendre vers 90, un personnage à postures monter
au-delà de 200.

| Catégorie | Exemples de commandes | Coups |
|---|---|---|
| Boutons seuls | 1, 2, 3, 4, 1+2, 3+4, 1+4, 2+3 | 8 |
| Directions + bouton | avant, avant-bas, bas, arrière-bas, arrière, arrière-haut, haut, avant-haut × 4 boutons | 24 |
| Accroupi et en se relevant | accroupi + bouton, en se relevant + bouton | 10 |
| En courant | avant-avant + bouton, course + bouton | 6 |
| En saut | haut + bouton, coups aériens | 5 |
| **Suites de chaînes** | les 2e, 3e et 4e coups des enchaînements | 35 |
| **Postures propres** | 1 à 3 postures : entrée, respiration, sortie, annulation, et leurs coups | 25 |
| Dos tourné | coups depuis le dos tourné | 6 |
| Après esquive | coups après un pas de côté, un salto ou une esquive | 4 |
| Sur un adversaire au sol | coups au sol | 3 |
| Projections propres | duos propres au personnage | 8 |
| Heat | Heat Engager (2), Heat Smash (1), coups renforcés en Heat (4) | 7 |
| Rage Art | attaque cinématique à deux | 1 |
| Power Crush | coups avec armure | 2 |
| Parades et contres propres | | 2 |
| **Total des coups** | | **≈ 146** |

**En animations**, cela fait un peu plus que les coups :

| | Nombre |
|---|---|
| Coups | ≈ 146 |
| Victimes des projections propres, de la Heat Smash et de la Rage Art | ≈ 12 |
| Transitions des postures (entrées et sorties supplémentaires) | ≈ 10 |
| Remplacements des communes (garde, marches, intro, victoires, provocation, sélection) | ≈ 8 |
| **Total propre au personnage** | **≈ 175** |

Une chaîne comme `1,2,4` donne 3 animations qui s'enchaînent :

- chaque coup peut finir seul (récupération courte) ;
- chaque coup peut aussi partir vers la suite (annulation) ;
- c'est ce qui permet aux bons joueurs de varier leurs combos.

---

## 5. Le total par personnage

| | Animations |
|---|---|
| Socle commun de combat (§ 3.1 à 3.14) | 190 |
| Couche objets et armes | ≈ 87 |
| Couche pouvoirs | ≈ 22 |
| **Communes, faites une fois** | **≈ 300** |
| Propres à un personnage moyen | ≈ 175 |
| **Disponibles pour un personnage moyen** | **≈ 475** |
| Sans armes ni pouvoirs | ≈ 365 |

Ce qu'il faut produire :

- **le 1er personnage** : ≈ 365 animations (socle de combat + ses coups), puis ≈ 110 pour
  les armes et les pouvoirs ;
- **chaque personnage suivant** : ≈ 175 seulement, puisque les communes existent déjà.

Pour comparer : Tekken ≈ 145 coups par personnage, nous ≈ 146 coups plus les couches de
clinch, de sol, d'objets et de pouvoirs que Tekken n'a pas.

---

## 6. Ordre de production proposé

| Phase | Contenu | Animations |
|---|---|---|
| 1. Socle jouable | Postures 5, marche et dash 4, saut 2, accroupi 2, défense 6, réactions 8, chute + au sol + relevé 6, KO 2, 1 projection (2), et 15 coups d'un premier personnage | ≈ 52 |
| 2. Combat Tekken | Jongles, murs, tech roll, chaînes, postures, Heat, Rage Art : on complète le socle et le 1er personnage | ≈ 280 de plus |
| 3. Vidéo 1 | Clinch, lutte, combat au sol, plusieurs adversaires | ≈ 33 |
| 4. Vidéo 2 | Objets, armes, pouvoirs, effets | ≈ 110 |
| 5. Personnage 2 | Ses ≈ 175 animations propres | 175 |

On s'arrête à la fin de chaque phase pour tester en jeu avant d'aller plus loin.

---

## 7. Décisions prises

1. **2D pure.** Pas de pas de côté ni de profondeur : les communes 3.2 #17-19 sont retirées
   (socle commun : 187). Les esquives (sway, se baisser, salto, roulade) remplacent le pas
   de côté.
2. **Boutons et game design** : décidés plus tard. Les animations ne dépendent pas du
   nombre de boutons.
3. **Chutes animées à la main** en duel. Physique de chiffon en option, seulement pour les
   corps projetés dans les scènes de foule.
4. **Objets** : presque tous les personnages auront quelques gestes d'objets ; certains
   s'y spécialiseront (comme un style de combat). À affiner plus tard.
5. **2 personnages** pour la première version jouable.

---

## 8. Première passe des communes

On ne fait pas tous les nombres d'un coup : juste assez par bloc pour un premier jeu
fluide. Chaque animation est faite **une à une**, pose par pose, vérifiée en planche et en
stroboscopie, et doit marcher dans toutes les situations où elle sert (une parade doit
paraître naturelle contre un coup de poing comme contre un coup de pied, haut ou moyen).

| Bloc | Animation | Fichier | État |
|---|---|---|---|
| Déplacements | Marche avant (boucle) | `marche_avant` | fait |
| Déplacements | Marche arrière (boucle) | `marche_arriere` | |
| Déplacements | Pas chassé avant (dash) | `dash_avant` | |
| Déplacements | Pas chassé arrière (backdash) | `dash_arriere` | |
| Postures | Debout → accroupi | `accroupi_entree` | |
| Postures | Accroupi, respiration (boucle) | `accroupi_idle` | |
| Postures | Accroupi → debout | `accroupi_sortie` | |
| Postures | Sortie de garde (garde → repos) | `sortie_de_garde` | |
| Déplacements | Saut neutre, avant, arrière | `saut_*` | |
| Déplacements | Réception légère | `reception` | |
| Déplacements | Demi-tour | `demi_tour` | |
| Défense | Garde haute tenue, garde accroupie tenue | `garde_haute`, `garde_basse` | |
| Défense | Recul sur garde haut et bas | `recul_garde_haut`, `recul_garde_bas` | |
| Défense | Parade haute, parade basse | `parade_haute`, `parade_basse` | |
| Défense | Esquive buste en arrière (sway), se baisser | `esquive_sway`, `esquive_baisse` | |
| Réactions | Tête légère, tête lourde | `touche_tete_*` | |
| Réactions | Ventre léger, plié en deux | `touche_ventre_*` | |
| Réactions | Jambe légère, fauché | `touche_jambe`, `fauche` | |
| Réactions | Accroupi touché, recul titubant, effondrement lent | | |
| En l'air | Lancé, touché en l'air, retombée sur le dos | | |
| Au sol | Chute arrière, chute avant, au sol (boucle), relevé, tech roll | | |
| KO | KO en arrière, inconscient au sol | | |
| Projections | Saisie de face (duo), saisie ratée | | |

Environ 45 animations. Le reste du socle vient en phase 2.

---

## Sources

- [TekkenDocs, statistiques Tekken 8 (nombre de coups par personnage)](https://tekkendocs.com/t8/stats)
- [Décompte 2026 : 6 210 coups sur 40 personnages](https://x.com/VolSkimmer/status/2018862362170937745)
- [Dotesports, movelist de King par catégories](https://dotesports.com/tekken/news/tekken-8-king-movelist-all-combos-and-moves)
- [Tekken Wiki, Wall Break](https://tekken.fandom.com/wiki/Wall_Break) et [Balcony Break](https://tekken.fandom.com/wiki/Balcony_Break)
- [Iron Fist Insights, glossaire (tech roll, quickrise, Heat, Tornado…)](https://ironfistinsights.com/docs/glossary/)
- [Tekken8.org, mécaniques du jeu](https://tekken8.org/mechanics/) (à recouper, certaines affirmations sont approximatives)
- [Entretien avec Harada sur la production des animations](https://www.fightersgeneration.com/news1/tekken7-harada-interview-march2020.htm)
- [Autodesk, Tekken 8 avec Maya et Unreal Engine](https://blogs.autodesk.com/media-and-entertainment/2025/01/28/tekken-8-legacy-meets-innovation-with-the-combined-power-of-maya-and-unreal-engine/)
- [Guinness, record du plus grand nombre de coups (Tekken Tag Tournament 2, pour le contexte)](https://www.guinnessworldrecords.com/world-records/109941-most-moves-in-a-fighting-videogame)
