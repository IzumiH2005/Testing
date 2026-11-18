# Analyse : course, saut par-dessus le vide, réception en roulade

Demande : « une animation de course rapide puis de saut haut en l'air pour arriver sur l'autre
côté de la plateforme un peu plus haute, avec l'animation de ses bras et jambes qui se débattent
en l'air avant qu'il atterrisse en faisant une roulade pour se remettre sur pied ».

Personnage : le stickman générique (style `epais`, celui de `sprint` et `saut_avant`), pas le
bagarreur. Animation `anims/course_saut_roulade.json`, non bouclée, 60 i/s, environ 165 images
(2,75 s). Elle a un **décor** (nouveau dans le moteur, voir § 8) : sol à 0, un trou, une
plateforme 45 plus haute.

## 1. La logique du mouvement

Il court vite vers un trou. Pour franchir le trou **et** monter de 45, il doit transformer une
partie de sa vitesse horizontale en vitesse verticale. Tout le mouvement découle de là :

1. **Course** (2 foulées de sprint) : il arrive à environ 12 unités par image (≈ 7 m/s).
2. **Avant-dernier appui allongé, bassin abaissé** : c'est l'anticipation (bible A2). Un sauteur
   en longueur abaisse son centre de gravité de 5 à 8 cm sur l'avant-dernier pas pour pouvoir
   ensuite le pousser vers le haut sur un trajet plus long. Les deux bras partent en arrière en
   même temps (double balancier, comme au saut en hauteur ou en parkour) : ils vont lancer le
   corps vers le haut.
3. **Appel** (7 images au sol, 0,12 s, comme un sauteur en longueur) : le pied d'appel se pose
   loin devant le bassin, jambe presque tendue, et sert de **butoir** : la vitesse horizontale
   bascule en vitesse verticale (le bassin passe au-dessus du pied comme une perche qui pivote).
   Puis triple extension (hanche, genou, cheville) pendant que la jambe libre monte, genou en
   avant, et que les deux bras montent ensemble au-dessus de la tête. Le pied d'appel quitte le
   sol juste avant le bord.
4. **Vol** (44 images) : il n'a plus d'appui, il ne peut rien changer à sa trajectoire. Le pied
   d'appel l'a fait pivoter vers l'avant (le pied freine le bas du corps pendant que le haut
   continue) : sans rien faire, il tournerait et arriverait la tête la première. Ce qu'on voit
   comme « il se débat » est la réponse : il **court dans le vide** (ciseau, « hitch-kick » des
   sauteurs en longueur) et fait des **moulinets avec les bras**. Les membres qui tournent dans
   le même sens que la rotation parasite en absorbent le moment cinétique, et le tronc reste à peu
   près droit. Ce n'est pas une nage régulière : les deux bras n'ont pas la même amplitude, un
   bras est en retard, les jambes accélèrent puis ralentissent au sommet (règle 10, vitesses
   jamais régulières), ce qui donne l'effet « il se débat ».
5. **Préparation de la réception** (les 8 dernières images) : les jambes se rassemblent devant,
   les bras partent devant pour équilibrer et préparer les mains.
6. **Réception sur l'avant des pieds, amorti** (bible : contact étiré, écrasement, amorti) : il
   arrive avec ≈ 9,5 unités par image vers l'avant et ≈ 5 vers le bas. Les jambes amortissent la
   composante verticale, mais la composante horizontale doit être arrêtée (bible A4 : ce qui est
   lancé doit être arrêté). S'il bloquait les jambes, il tomberait en avant. D'où la roulade :
7. **Roulade avant sur l'épaule** (roulade de parkour) : il continue vers l'avant en se mettant
   en boule ; les mains touchent la plateforme pour guider (elles ne portent pas le poids), le
   menton rentre, le dos rond roule sur la diagonale épaule proche → hanche loin. Le cercle du dos
   transforme la vitesse en rotation, sans choc. La roulade ralentit le bassin à chaque image.
8. **Relevé** : il sort de la roulade accroupi, pieds sous le bassin, les bras devant comme
   contrepoids, la tête descend un peu (anticipation du relevé, bible « Se relever »), puis il
   se redresse en finissant de dissiper sa vitesse par un petit pas, et finit au repos.

## 2. Anatomie : ce qui bouge et d'où vient la force

- **Course** : grand fessier et ischio-jambiers (extension de hanche, griffé du pied au sol),
  ilio-psoas et droit fémoral (montée du genou), triceps sural (poussée de la cheville). Bras :
  deltoïde antérieur / postérieur, en opposition aux jambes.
- **Avant-dernier appui** : quadriceps et fessiers travaillent en **excentrique** (le genou plie
  davantage, 40° au lieu de 30), le bassin descend de ≈ 6.
- **Appel** : au pied posé, la jambe tendue encaisse (quadriceps excentrique, genou ≈ 145° → 125°
  d'angle intérieur, soit une flexion de 15 → 35°), puis **triple extension** concentrique :
  grand fessier (hanche), vaste et droit fémoral (genou), triceps sural (cheville en flexion
  plantaire, talon levé, poussée sur l'avant du pied). La jambe libre est lancée par
  l'ilio-psoas et le droit fémoral : sa cuisse monte au-delà de l'horizontale ; son élan s'ajoute
  à la poussée. Les deux bras montent ensemble (deltoïde antérieur, faisceau claviculaire du grand
  pectoral, trapèze supérieur qui hausse l'omoplate) : leur élan vers le haut ajoute de la vitesse
  verticale au moment exact de la poussée.
- **Vol** : alternance rapide ilio-psoas / grand fessier et ischio-jambiers (cuisses), quadriceps
  et ischio-jambiers (genoux). Les bras font des **circumductions** de l'épaule : grand dorsal et
  grand rond tirent le bras de devant vers le bas et l'arrière ; deltoïde et trapèze le remontent
  par l'arrière jusqu'au-dessus de la tête ; l'omoplate bascule (rotation vers le haut quand le
  bras passe au-dessus de 90°). Abdominaux et obliques gainent le tronc pour que les membres
  tournent autour de lui et pas l'inverse.
- **Réception** : quadriceps, fessiers et triceps sural en excentrique (ils freinent la chute,
  les genoux plient jusqu'à ≈ 115°), érecteurs du rachis tiennent le buste penché.
- **Roulade** : droit de l'abdomen et fléchisseurs de hanche enroulent le tronc (dos rond),
  sterno-cléido-mastoïdien et fléchisseurs du cou rentrent le menton (la tête ne doit jamais
  toucher), triceps et deltoïde tiennent les mains au contact puis cèdent. Les genoux restent
  ramenés (ischio-jambiers, ilio-psoas) pour garder un rayon petit (rouler vite, sans à-coup).
- **Relevé** : quadriceps et fessiers en concentrique, bras lancés devant (contrepoids, deltoïde
  antérieur) pour garder le centre de gravité au-dessus des pieds (bible A5).

## 3. Le décor et la trajectoire (calculs)

Repère local (x vers l'avant, bassin de la première clé en x = 0). Le saut est construit à
partir de la position du pied d'appel `A` (cheville F posée à l'image 42).

| Élément | Position |
|---|---|
| Sol de départ | y = 0, de x = −200 jusqu'au bord `E = A + 15` |
| Vide | de `E` à `P = A + 315` (3,15 m) |
| Plateforme | y = 45, de `P` à `P + 700` |

**Gravité** : g = 9,81 m/s² = 0,2725 unité par image² (même valeur que `saut_avant`).

**Vol** : décollage à l'image 49, bassin à ≈ 96 (jambe d'appel tendue, sur la pointe). Contact
à l'image 93 (T = 44), bassin à ≈ 45 + 80 = 125 (jambes presque tendues devant, talons au
contact). Δh = 29.

- vy0 = Δh / T + g·T / 2 = 29 / 44 + 0,2725 × 22 = 0,66 + 6,0 = **6,65** par image (≈ 4 m/s) ;
- sommet du bassin = vy0² / (2g) = **81** au-dessus du décollage, soit y ≈ 177 (les pieds à
  ≈ 95 du sol de départ au plus haut) : c'est un saut **haut**, comme demandé ;
- vitesse horizontale ≈ **9,5** par image (il perd ≈ 20 % de sa vitesse de course à l'appel,
  comme un vrai sauteur), soit 418 de vol pour le bassin ;
- bible § 9 « la montée freine, le sommet dure, la chute double » : on garde la parabole, mais le
  temps est étiré autour du sommet (gravité apparente réduite de 40 % sur les 10 images du
  haut), et la descente rattrape : les écarts verticaux vont ≈ 6,5 · 6,2 · … · 1 · 0,3 · 0 ·
  −0,3 · … · −5 · −6,5 · −7,5 ; le contact se fait à la descente la plus rapide.
- **Passage du bord de la plateforme** (x = P) : le bassin est à ≈ 29 images du décollage, à
  y ≈ 170 ; le point le plus bas du corps (pied en ciseau) à ≈ 90, soit 45 au-dessus de la
  plateforme. Il passe nettement.
- **Contact** : talons à ≈ A + 480, soit ≈ 165 après le bord P : on voit qu'il est bien de
  l'autre côté.

## 4. Les phases, partie par partie

### 4.1 Course (0-28) : une foulée complète de `sprint`

Clés de `sprint` 0 à 27 reprises telles quelles (appui N à 0, appui F à 14). Buste penché de
19°, tête relevée (cou −26), bras en opposition, coudes pliés 50-100°.

### 4.2 Avant-dernier appui (28-42), pied N

Pas plus long (≈ 14 images, cheville posée 30 devant le bassin au lieu de 22), bassin qui
descend de 79 à 74 au milieu de l'appui, puis remonte un peu. Le buste se redresse de 19 à 10°
(on ne saute pas haut penché). Les deux bras se rejoignent en arrière : le bras qui était devant
redescend, l'autre reste derrière ; à 40 les deux sont derrière (épaules −45 et −40°, coudes 70°).
Regard au loin, vers la plateforme (cou −20 → −10).

### 4.3 Appel (42-49), pied F

- **42, pose du pied** : cheville F posée 35 devant le bassin, genou presque tendu (15°), talon
  d'abord (le pied fait 14° de pointe relevée). Bassin à 76, tronc à 8°, bras tous deux derrière
  (épaules −50 / −45°). Jambe libre N : cuisse −15° (derrière), genou plié 100° (talon sous les
  fesses), elle commence à revenir.
- **45, compression** : le bassin est au-dessus du pied, genou d'appel à 35°, bassin à 73
  (le plus bas). La cuisse libre passe sous le bassin (20°, genou 115°). Les bras passent le long
  du corps vers l'avant (épaules +10°, coudes 40°), à leur vitesse maximale.
- **49, décollage** : jambe d'appel tendue derrière (cuisse −25°, genou 3°, cheville en flexion
  plantaire −40°, seule la pointe touche, juste avant le bord E). Jambe libre : cuisse à 95°
  (genou plus haut que la hanche), genou plié 95°, pied relâché sous le genou. Bras tous deux en
  l'air (épaules 155 / 150°, coudes 20°), omoplates haussées (+4). Tronc à 4°, poitrine
  légèrement ouverte (−3), tête neutre, regard vers la plateforme (cou −12). Le corps forme une
  diagonale du pied d'appel à la tête : la ligne de poussée.

### 4.4 Vol (49-93) : il court et moulinette dans le vide

Deux cycles de ciseau et demi (la jambe libre devient arrière, puis revient devant, puis les
deux se rejoignent). Le bras proche fait un tour et demi, le bras loin un tour un peu plus
petit, en retard de ≈ 3 images sur une demi-phase (ils ne sont pas parfaitement opposés : il se
débat).

- **49-58, montée** : la jambe libre N, haute, se déplie et descend vers l'arrière ; la jambe
  d'appel F, restée derrière, plie le genou et revient devant (talon près de la fesse). Les bras,
  en l'air, commencent leur tour vers l'avant puis le bas. Le tronc, poussé à pivoter vers
  l'avant par l'appel, passe de 4 à 10° puis ne bouge presque plus (les membres absorbent la
  rotation).
- **58-72, sommet** (le sommet dure, bible § 7 et § 9) : les membres ralentissent, les **deux
  genoux sont hauts** (cuisses 70 et 85°, genoux pliés 100 et 120°), les bras sont au-dessus de
  la tête, croisés en hauteur (proche à 170°, loin à 140°) : c'est le « groupé » du sommet, mais
  il continue de remuer (petites oscillations des pieds).
- **72-85, descente** : le ciseau reprend plus vite. La jambe N part loin derrière (cuisse −15°,
  genou 40°), F monte devant ; les bras finissent leur tour (le bras N passe derrière en bas puis
  remonte par l'arrière). Le tronc se penche à peine en arrière (2 à 0°).
- **85-93, préparation** : les deux jambes se rejoignent devant (cuisses 75-80°, genoux 20-25°,
  pieds à moins de 12 l'un de l'autre), le tronc se penche vers l'avant (root 20 → 28°) pour
  amener le poids sur les pieds au contact, les deux bras arrivent devant (épaules 70 / 80°,
  coudes 30°). La tête regarde la plateforme (cou 15°).

### 4.5 Réception (93-101)

- **93, contact étiré** : les deux pieds touchent ensemble, l'avant du pied d'abord (pied à plat
  en 2 images), jambes encore longues (cuisses 55°, genoux 25°), tronc 30°, bras devant.
- **96, écrasement** : bassin à 72 % de sa hauteur de contact (bible), genoux 110°, cuisses
  100°, tronc 45°, bras devant et bas (60 / 70°, coudes 20°).
- **101, mains posées** : il ne s'arrête pas, le bassin continue d'avancer et le poids passe
  devant les pieds. Tronc 80° (presque horizontal), genoux 140°, talons levés. Les deux mains se
  posent sur la plateforme ≈ 25 devant les pieds, en losange : la main proche un peu plus loin,
  coudes pliés 30°, bras écartés (proche +20°, loin −20° de profondeur). Menton rentré (cou
  45°), tête tournée vers le côté loin (`neck_p` −20) : l'épaule proche va toucher en premier.

### 4.6 Roulade (101-132)

Le tronc fait un tour complet vers l'avant : `root` croît sans s'arrêter de 80 à 340 (puis
349 = −11 + 360 au repos).

- **106, épaule au sol** : root 155, le bassin au-dessus des épaules, les genoux encore pliés
  (cuisses 100°, genoux 100°), les pieds quittent le sol. L'arrière de l'épaule proche touche
  (le haut du dos à la hauteur de la plateforme), la tête est rentrée, sur le côté, au-dessus de
  la plateforme. Les bras se plient, coudes vers l'extérieur.
- **114, roule sur le dos** : root 225, dos rond au contact, genoux ramenés sur la poitrine
  (cuisses 130°, genoux 140°), pieds en l'air au-dessus.
- **122, sur les fesses, les pieds passent** : root 285, le bas du dos au contact, les talons
  arrivent vers la plateforme, les bras partent devant les genoux.
- **128, pieds posés, accroupi** : root 325, pieds à plat sous le bassin (talons au sol), genoux
  135°, cuisses 120°, bras tendus devant (épaules 80°). Le centre de gravité est au-dessus des
  pieds (bible A5) : il ne retombe pas en arrière.

### 4.7 Relevé (128-165)

- **128-136** : la tête descend de 3 (anticipation du relevé) pendant que la vitesse finit de
  tomber ;
- **136-152** : il monte, le bassin passe de 50 à 82 au-dessus de la plateforme, avec les
  écarts de la bible « Se relever » (1, 2, 6, 12, 14, 15, 9, 2 sur des pas de 2 images) ; un
  petit pas avec la jambe proche pour finir de freiner (il avance encore de ≈ 20) ;
- **152-165** : il se pose au repos (pose `repos`, root 349 ≡ −11), bras qui retombent en
  dernier, avec un léger dépassement (la tête monte puis redescend de 1).

## 5. Chaque articulation, tous ses axes, à chaque clé

Conventions : angles « sémantiques » du rig (épaule + = bras devant, 180 = au-dessus ; hanche
+ = genou devant ; genou et coude = flexion ; cheville + = pointe relevée). Profondeur `_p` :
+ = vers la caméra (côté N), − = côté F. Rotation `_r` : + = coude (genou) tourné vers la
caméra. « Om. » = omoplate (`epaule*_av`, `epaule*_haut`). Les torsions sont faibles dans tout
le mouvement : c'est un mouvement dans le plan sagittal (la course et la roulade se font de
face, pas en tournant).

### 5.1 Tronc et tête

| Clé | root | spineLow | chest | neck | neck_p | torsion | torsionBassin |
|---|---|---|---|---|---|---|---|
| 0-27 sprint | 18-20 | 12 | 11-14 | −25 à −28 | 0 | ±0 | 0 |
| 35 avant-dernier | 12 | 8 | 6 | −18 | 0 | 0 | 0 |
| 42 pose pied | 8 | 6 | 4 | −14 | 0 | −4 (épaule N en arrière, bras N derrière) | +4 (hanche F devant) |
| 45 compression | 6 | 5 | 2 | −12 | 0 | 0 | +6 |
| 49 décollage | 4 | 3 | −3 | −12 | 0 | +3 | −8 (hanche N part devant avec le genou) |
| 63-70 sommet | 2 | 6 | 4 | −6 | 0 | ±6 (suit les bras) | ±5 (suit les jambes) |
| 78 descente | 0 | 4 | 3 | −4 | 0 | ±6 | ±5 |
| 90 préparation | 24 | 8 | 6 | 15 | 0 | 0 | 0 |
| 93 contact | 30 | 10 | 8 | 12 | 0 | 0 | 0 |
| 96 écrasement | 45 | 14 | 12 | 10 | 0 | 0 | 0 |
| 101 mains | 80 | 22 | 20 | 45 | −20 | −8 (épaule N descend vers le sol) | 0 |
| 106 épaule | 155 | 25 | 25 | 50 | −22 | −10 | 0 |
| 114 dos | 225 | 25 | 25 | 45 | −15 | −6 | 0 |
| 122 fesses | 285 | 22 | 20 | 35 | −8 | 0 | 0 |
| 128 accroupi | 325 | 15 | 12 | 10 | 0 | 0 | 0 |
| 136 tête basse | 330 | 14 | 12 | 18 | 0 | 0 | 0 |
| 152-165 repos | 349 (−11) | 6 | 9 | 8 | 0 | 0 | 0 |

`spineLow` et `chest` vont jusqu'à 25° dans la roulade : c'est le dos rond (flexion lombaire et
thoracique ensemble ≈ 50°, dans l'amplitude humaine). `neck` 45-50° : menton sur la poitrine.

### 5.2 Bras (élévation `arm`, profondeur `arm_p`, rotation `arm_r`, coude `fore`, omoplate)

| Clé | Bras proche N | Bras loin F | Om. N / F |
|---|---|---|---|
| 0-27 sprint | −50 ↔ 80, p 12, r 0, coude 50-100 | opposé | 0 / 0 |
| 40 bras derrière | −45, p 14, r −10 (coude vers l'arrière-dehors), coude 70 | −40, p −14, r 10, coude 70 | av −2 / −2 |
| 42 pose pied | −50, p 14, coude 60 | −45, p −14, coude 60 | av −3 / −3 |
| 45 compression | +10, p 12, coude 40 | +5, p −12, coude 40 | 0 / 0 |
| 49 décollage | 155, p 10, r 0, coude 20 | 150, p −10, coude 20 | haut +4 / +4, av +1 |
| 55 | 120 (descend devant), p 14, coude 30 | 175, p −10, coude 15 | +2 / +4 |
| 60 | 60, p 18, coude 40 | 130, p −12, coude 30 | 0 / +2 |
| 63-70 sommet | 170 (revenu au-dessus par l'arrière, voir 5.3), p 12, coude 30 | 140, p −14, coude 50 | +4 / +3 |
| 75 | 90, p 16, coude 30 | 175, p −10, coude 20 | +1 / +4 |
| 80 | −20, p 18, coude 25 | 90, p −16, coude 35 | −2 / +1 |
| 85 | −120 (derrière, en remontant), p 16, r −20, coude 20 | 0, p −16, coude 30 | +2 / 0 |
| 90 préparation | 70, p 14, coude 30 | 80, p −14, coude 30 | +1 / +1 |
| 93 contact | 75, p 14, coude 25 | 85, p −14, coude 25 | 0 / 0 |
| 96 écrasement | 60, p 16, coude 20 | 70, p −16, coude 20 | +1 / +1 |
| 101 mains | 75, p 20, r 15 (coude dehors), coude 30 | 60, p −20, r −15, coude 30 | +2 / +2 |
| 106 épaule | 120 (au-dessus de la tête, le long du sol), p 24, coude 70 | 90, p −22, coude 80 | 0 / 0 |
| 114 dos | 60, p 22, coude 80 | 60, p −22, coude 80 | 0 / 0 |
| 122 fesses | 70, p 16, coude 40 | 70, p −16, coude 40 | +1 / +1 |
| 128 accroupi | 80, p 14, coude 20 | 80, p −14, coude 20 | +1 / +1 |
| 165 repos | −10, p 12, coude 10 | 8, p −12, coude 8 | 0 / 0 |

**Le tour du bras (5.3)** : un moulinet « en crawl » : le bras descend devant, passe en bas,
remonte derrière, passe au-dessus de la tête, redescend devant. En angle d'épaule, c'est une
**décroissance continue** : 155 → 90 → 0 → −90 → −180 ≡ 180 → 155 … Physiquement c'est le bon
sens : en profil, regardant vers +x, la rotation parasite (tête vers l'avant et le bas) est
horaire ; un bras qui passe au-dessus vers l'avant et en dessous vers l'arrière tourne aussi
dans le sens horaire, il absorbe la rotation. Quand le bras passe derrière (−60 à −150), son
élévation par l'arrière dépasse l'extension pure de l'épaule (≈ 60°) : l'humérus passe alors
**sur le côté** (`arm_p` monte à 25-30) et l'omoplate tourne : le bras décrit en réalité un cône
en dehors du plan, ce qui se voit de face (le bras s'écarte du corps quand il est derrière).
Le bras N fait un tour et demi (49 → 63 : un demi-tour devant et vers le bas puis en remontée
par l'arrière ; 63 → 88 : un tour complet), le bras F un tour, avec une demi-phase de retard,
puis les deux finissent devant.

### 5.3 Jambes (hanche `thigh`, écartement `thigh_p`, rotation `thigh_r`, genou `shin`, cheville)

| Clé | Jambe proche N | Jambe loin F |
|---|---|---|
| 0-27 sprint | cycle du sprint, p 7 | idem, p −7 |
| 35 avant-dernier (appui N) | sous le bassin, cuisse 5, genou 40, pied à plat, p 6, r 0 | derrière puis revient, cuisse −20 → 30, genou 110, p −6 |
| 42 pose pied F | cuisse −15, genou 100 (talon sous les fesses), p 6 | appui : cuisse 25, genou 15, cheville +14 (talon d'abord), p −4, r 0 |
| 45 compression | cuisse 20, genou 115, p 6 | appui sous le bassin, cuisse 2, genou 35, pied à plat, p −4 |
| 49 décollage | cuisse 95, genou 95, cheville −15 (pied relâché), p 8, r 5 | cuisse −25, genou 3, cheville −40 (pointe), p −4 |
| 55 | cuisse 50, genou 30 (se déplie vers le bas), p 8 | cuisse −10, genou 120 (talon remonte), p −6 |
| 60 | cuisse −10, genou 60, p 8 | cuisse 50, genou 110 (genou monte devant), p −6 |
| 63-70 sommet | cuisse 70, genou 100, p 8 | cuisse 85, genou 120, p −8 |
| 75 | cuisse 30, genou 50 | cuisse 60, genou 120 |
| 80 | cuisse −15, genou 40, p 8 | cuisse 85, genou 80, p −6 |
| 85 | cuisse 30, genou 110 (revient devant plié) | cuisse 55, genou 40 |
| 90 préparation | cuisse 78, genou 22, cheville 0, p 5 | cuisse 75, genou 25, p −5 |
| 93 contact | cuisse 55, genou 25, avant du pied | cuisse 55, genou 25, avant du pied |
| 96 écrasement | cuisse 100, genou 110, pied à plat | cuisse 100, genou 110 |
| 101 mains | cuisse 120, genou 140, talon levé (−30) | idem |
| 106 épaule | cuisse 100, genou 100, pied quitte le sol, p 10 | cuisse 100, genou 95, p −10 |
| 114 dos | cuisse 130, genou 140 (genou sur la poitrine) | cuisse 130, genou 140 |
| 122 fesses | cuisse 115, genou 130 | cuisse 115, genou 130 |
| 128 accroupi | cuisse 120, genou 135, pied à plat | idem, pied 10 en retrait |
| 145 petit pas | N avance de ≈ 20, cuisse 25, genou 40 | appui, se redresse |
| 165 repos | pose `repos` | pose `repos` |

Écartement des jambes (vue de face) : 6 à 8° pendant la course et le vol (les genoux ne se
croisent jamais au milieu), 10° en réception (pieds largeur de hanches, plus stable), 10° dans
la roulade (genoux de part et d'autre de la tête quand ils sont sur la poitrine, pour que la
tête ne passe pas dans les genoux).

## 6. Ce qui se voit de profil, et comment le rig le montre

- **Le décor** : le bord du sol, le trou, la plateforme plus haute ; le personnage passe
  au-dessus du vide, le bord de la plateforme passe sous ses pieds avec de la marge.
- **L'appel** : la diagonale pied d'appel → tête, la jambe libre en avant genou haut et les deux
  bras en l'air ; il se lit immédiatement comme un saut.
- **Le ciseau** : de profil, la jambe proche est dessinée devant le tronc et la jambe loin
  derrière ; on voit les deux jambes s'échanger (une devant, une derrière), comme une course.
- **Les moulinets** : le bras proche passe devant le corps, au-dessus de la tête puis derrière ;
  le bras loin est derrière le tronc. Quand un bras est derrière le dos, il sort sur le côté
  (`arm_p`), donc de profil il raccourcit un peu : c'est voulu.
- **La réception** : contact jambes longues, puis écrasement net (en 3 images), mains au sol.
- **La roulade** : de profil, une roulade avant (silhouette en boule, dos rond, tête rentrée).
  La diagonale sur l'épaule se lit de face et de trois quarts (tête sur le côté, `neck_p`, bras
  écartés en losange). Le tronc fait un tour complet, sans arrêt ni retour en arrière.
- **Ce qui ne se voit pas** : la rotation des poignets, la répartition exacte du poids sur les
  mains. On ne la règle pas.

## 7. Références

- `BIBLE_ANIMATION.md` :
  - A1 (tenue, rafale, tenue) : la course est rapide, le sommet est une tenue, la roulade une
    rafale, la fin une tenue ;
  - A2 (anticipation) : avant-dernier appui abaissé, bras en arrière avant de monter ; la tête
    descend avant le relevé ;
  - A4 (ce qui est lancé est arrêté) : la vitesse horizontale finit dans la roulade et le petit
    pas ;
  - A5 (centre de gravité sur les appuis) : à l'appel, au contact, en sortie de roulade ;
  - § 7 « Saut et vol » (montée courte, suspension, descente qui accélère, groupé au sommet),
    « Atterrissage » (contact étiré, écrasement à 72 %, amorti, buste à 45°, poussière en
    anneau), « Se relever » (la tête descend avant de monter, écarts 1 · 2 · 6 · 12 · 14 · 15 ·
    9 · 2) ;
  - § 9 (la montée freine, le sommet dure, la chute double ; rotation rapide à la montée,
    presque nulle au sommet) ; règle 10 (vitesses jamais régulières).
- `etudes/01_strength_vs_speed/03_lancers_176_257.md` 242-246 : au sommet, genoux levés, bras
  au-dessus de la tête ; réception en trois temps (pieds, écrasement à 70 %, glissade) ;
  `01_entree_24_135.md` 24-36 : atterrissage contact / écrasement / amorti sur trois images.
- Animations existantes : `sprint` (cycle et vitesse), `saut_avant` / `reception` (valeurs de
  réception), `releve_roulade` (roulade arrière : ordre des contacts, genoux sur la poitrine,
  profondeur des cuisses ±12 et des bras ±28 pour que la tête passe entre les genoux).
- Biomécanique : saut en longueur (avant-dernier appui abaissé de 5 à 8 cm, appel de 0,11 à
  0,13 s, perte de 1 à 1,5 m/s de vitesse horizontale, ciseau « hitch-kick » pour contrer la
  rotation vers l'avant) ; parkour (réception sur l'avant des pieds, roulade sur la diagonale
  épaule → hanche opposée, mains qui guident sans porter).

## 8. Le décor dans le moteur

Nouveau champ de l'animation : `"decor": {"sol": [[x0, x1, h], …]}` (repère local). Hors des
segments, c'est le vide. Il sert :

- au rendu (`planche.gd`) : chaque segment est un bloc plein de sa hauteur jusqu'en bas ;
- aux pieds (`StickRig.ground_feet`, `auto_feet`, `StickAnim._bake_feet`) : la hauteur du sol
  sous la cheville remplace 0 ;
- au vérificateur : « sous le sol » et « pied qui glisse » avec la hauteur locale, plus un
  nouveau contrôle « traverse le décor » (une articulation dans un bloc, y compris par le côté
  du bord de la plateforme).

Sans `decor`, le comportement reste exactement le même (contrôle : `--verifier` et `--print`
identiques avant / après sur `sprint`, `saut_avant`, `releve_roulade`, `reception`).
L'animation n'est pas branchée dans le jeu (le combat n'a pas de plateforme) : c'est une
démonstration avec décor ; elle finit 45 plus haut et n'enchaîne sur rien.

## 9. Contrôles chiffrés (`--verifier` et mesures)

1. **Rien dans le décor** : aucune articulation (ni le bord du trait) sous la surface ni dans le
   bloc de la plateforme, à aucune image.
2. **Pieds plantés** : cheville N fixe (glissement < 1,5) sur l'avant-dernier appui ; cheville F
   fixe de 42 à 49 ; à 49 la pointe du pied d'appel est entre 3 et 20 avant le bord E.
3. **Vitesse horizontale du bassin** : 11,5 à 13 pendant la course ; 9 à 10 pendant tout le vol
   (constante à ± 0,3 : pas d'appui, pas de freinage) ; décroissante de 93 à la fin ; jamais
   négative.
4. **Trajectoire verticale** : sommet du bassin ≥ 75 au-dessus du bassin au décollage ; au
   moins 6 images au sommet avec |Δy| < 1,5 ; écarts de montée décroissants, écarts de descente
   croissants jusqu'au contact.
5. **Passage du bord** : quand le bassin passe au-dessus de x = P, le point le plus bas du corps
   est au moins 25 au-dessus de la plateforme.
6. **Contact** : les deux chevilles touchent la plateforme à la même image (± 1), au moins 120
   après le bord P ; à 96, bassin à 70-75 % de sa hauteur (au-dessus de la plateforme) du contact.
7. **Rotation du tronc** : en vol, root reste entre −5 et 30 ; |Δroot| ≤ 1 par image au sommet ;
   dans la roulade, root croît à chaque image (jamais de retour), de 80 à 340 en 27 à 31 images.
8. **La tête ne touche jamais la plateforme** : centre de la tête ≥ 45 + 23 − 3 (rayon de la tête,
   tolérance d'un trait qui l'effleure) pendant la roulade ; le haut du dos et les épaules, eux,
   touchent (point le plus bas à moins de 3 de la surface entre 106 et 122).
9. **Bras** : chaque bras fait au moins un tour complet (son angle décroît de plus de 360° en
   tout) entre 49 et 90 ; les deux bras ne sont jamais en opposition exacte (écart de phase
   différent de 180° ± 15 pendant au moins la moitié du vol).
10. **Centre de gravité** : à 45, 96 et 128, le bassin est au-dessus des appuis (entre talon et
    pointe, ou entre les mains et les pieds à 101) à ± 10.
11. **Rien ne se traverse** (`--verifier` en 3D) : surtout la tête et les genoux dans la
    roulade, les bras qui passent derrière le dos.
