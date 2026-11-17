# Analyse : intro du bagarreur (stickman noir)

Mise en scène d'avant combat du bagarreur pieds-poings. Il entre en marchant vers l'adversaire,
**sûr de lui** (pas nonchalant), s'arrête et **fait craquer son poing** dans sa main. Le
personnage regarde vers la droite ; il part du repos et finit au repos (`suivante` :
`idle_repos`), la mise en garde se fait ensuite au signal du combat.

Fichiers : `anims/intro_bagarreur.json`, généré par `tools/gen_intro_bagarreur.py` (les jambes
reprennent la marche détendue : départ, un cycle, arrêt en un pas).

## 1. La logique du mouvement

Une intro dit qui est le personnage avant le premier coup. Le bagarreur est le combattant de
base, ni le plus rapide ni le plus fort, mais il ne doute pas. Trois idées :

1. **Il marche droit vers l'adversaire, sans se presser.** La différence avec la marche
   détendue n'est pas dans les jambes (même pas, même rythme) mais dans le haut du corps :
   - buste **droit**, poitrine ouverte (le bassin bascule moins en arrière, la colonne ne
     s'enroule plus) ;
   - épaules **tirées en arrière** (omoplates rétractées) : la poitrine sort ;
   - menton à l'horizontale, regard sur l'adversaire, la tête ne dodeline pas ;
   - bras un peu décollés du corps (16° au lieu de 12°) : il prend de la place ;
   - les épaules tournent un peu avec le balancier des bras (contre-rotation de la marche) :
     ça roule légèrement, sans rouler des mécaniques.
2. **Il prépare le geste pendant le dernier pas.** Les mains montent pendant que le pied se
   pose : le poing loin (main forte, côté arrière) se ferme devant la poitrine, la main proche
   vient le couvrir. Quand les pieds sont posés, les mains sont prêtes. Pas de temps mort.
3. **Il fait craquer son poing deux fois**, la seconde plus fort, en regardant l'adversaire.
   C'est un message, pas un échauffement : le geste est sec, puis tenu.

## 2. Anatomie du craquage de poing

### 2.1 Ce qui craque (recherches)

- Le bruit vient des **articulations métacarpo-phalangiennes** (MCP, les « jointures » à la
  base des doigts). Chaque MCP est fermée par une capsule remplie de liquide synovial. Quand on
  force l'articulation au-delà de sa course active, les surfaces s'écartent, le volume de la
  capsule augmente plus vite que le liquide ne peut le remplir, et une **cavité de gaz se
  forme d'un coup** : c'est elle qui fait le « crac » (IRM en temps réel de Kawchuk et al.,
  PLOS ONE 2015 ; l'ancienne idée était l'éclatement de la bulle, Unsworth 1971). Il faut
  ensuite 15 à 30 minutes avant de pouvoir refaire craquer la même jointure.
- Conséquence pour le geste : il faut **une force lente qui monte puis un relâchement
  brusque**. On serre, on pousse, la résistance cède d'un coup ; la poussée « tombe » de
  quelques millimètres au moment du crac. C'est ce qui donne le rythme : appui progressif,
  puis petit à-coup sec.

### 2.2 Comment on fait le geste « je vais te casser la figure »

Trois façons de faire craquer son poing avec l'autre main (guides pratiques, observation) :
1. le poing fermé, l'autre main **enveloppe le dos des doigts** (phalanges proximales) et
   presse : les MCP sont poussées en flexion forcée ;
2. on **pousse les jointures du poing dans la paume** de l'autre main, qui fait le mur ;
3. on prend le poing par-dessus et on le **roule** (la main qui couvre tourne autour du
   poing).

La version d'intimidation (cinéma, combat de rue) est un mélange de 1 et 2, faite **devant la
poitrine**, à la hauteur du sternum, coudes sortis : on montre l'outil (le poing) et la force.
C'est celle-là : le poing F est la main forte (la main qui frappe), la main N l'enveloppe par
devant et par-dessus et presse vers le bas et vers soi, pendant que le poing pousse vers
l'avant contre elle. Les deux forces se rencontrent sur les phalanges.

Sur le rig, une main est une boule (rayon 8,5) : ni doigts, ni paume, ni poignet. Ce qui
doit se voir n'est donc pas l'orientation de la paume mais **où est chaque boule et comment
elle bouge** :
- **poing F** : devant le bas du sternum, un peu du côté loin ; il ne bouge presque pas, il
  pousse vers l'avant au craquement ;
- **main N** : posée devant et au-dessus du poing F, du côté caméra, au contact (centres à 17,
  deux rayons) ; elle **roule** sur le poing (elle tourne autour de lui en gardant le contact)
  pendant l'appui, puis s'arrête net au craquement.

La force vient des **pectoraux et du deltoïde antérieur** (les deux bras qui se rapprochent,
adduction horizontale des épaules), relayés par les **fléchisseurs du poignet et des doigts**
de la main N (elle se referme sur le poing) et par les **extenseurs du poignet** du côté du
poing (le poing ne se laisse pas plier, il résiste). Les **triceps et biceps** se contractent
ensemble : les coudes ne bougent presque pas, ce sont des leviers rigides. Le tronc est gainé
(il ne bascule pas avec l'effort). Les omoplates restent serrées en arrière pendant que
les pectoraux tirent les bras l'un vers l'autre (rhomboïdes et trapèze moyen tiennent
l'omoplate, comme au développé couché) : c'est ce qui permet de garder les épaules reculées
(règle 6) pendant un effort de bras.

On fait craquer les articulations des doigts (métacarpo-phalangiennes) en forçant leur flexion :
la paume d'une main enveloppe le dos des doigts de l'autre poing et pousse.

| Partie | Articulation | Muscles | Rôle |
|---|---|---|---|
| Main qui pousse (proche) | poignet, doigts | fléchisseurs, paume | enveloppe les phalanges et appuie vers le bas et vers soi |
| Poing (loin) | doigts en flexion forcée | fléchisseurs | serré, il résiste : c'est la résistance qui fait craquer |
| Coudes | flexion 120° environ | biceps, triceps en co-contraction | restent pliés, poussent l'un contre l'autre |
| Épaules | abduction (coudes écartés), rotation interne | deltoïdes, pectoraux | les coudes s'écartent au moment de la poussée : c'est ce qu'on voit de face |
| Omoplates | élévation puis abaissement | trapèzes | les épaules montent pendant qu'on prend appui, retombent sur le craquement |
| Tronc | gainé, ne bouge presque pas | grands droits, érecteurs | le buste reste droit : c'est un geste de mains, pas de dos |
| Cou | petite flexion puis retour | | un hochement sec, puis le menton remonte |

Le poing qu'on craque est celui de la main forte, côté arrière en garde (loin, F) ; la main
proche (N) le couvre.

### 2.3 Les demandes de l'utilisateur et leur traduction

| Demande (mot pour mot) | Interprétation | Contrôle |
|---|---|---|
| « L'angle d'ouverture des épaules sur les côtés doit être un peu plus » | coudes sortis sur les côtés | bras / verticale ≥ 50° posée, ≥ 44° au crac (les coudes tombent) (sortie « profil : … bras/verticale ») |
| « les avant-bras doivent être quasiment parallèles au sol lorsque les poings entrent en contact » | pente de chaque avant-bras entre −12° et +12° au contact | « pente » de resout_mains |
| « les coudes ne sont pas assez tournés vers l'intérieur » | les avant-bras pointent vers le centre (l'un vers l'autre) autant que le rig le permet, sans ramener les mains contre la poitrine | « vers l'avant » ≤ 62° |
| « Les coudes devraient être légèrement en arrière au lieu d'aligner au buste je pense » | essayé (coudes à −2 puis −7) : les mains se retrouvent sous le menton, illisibles de profil ; remplacé par la demande suivante | — |
| « Finalement c'est la première version qui correspondait le plus […] utilise-la comme base » | on reprend la toute première version (mains loin devant la poitrine, coudes ouverts, poings joints) ; on n'y corrige que les traversées (mains en 3D, côte à côte en profondeur) et la stature (épaules qui avançaient au crac) | rendu comparé à la première version ; contrôles 4 et 5 |
| « Et si cette pose […] tu la faisais en 3/4 au lieu de profil […] sa tête est bien sûr tournée vers son adversaire » | pendant le craquage, buste tourné de 25° vers la caméra, cibles des mains tournées avec lui ; tête tournée d'autant dans l'autre sens | `torsion` −25, `neck_r` +25 aux clés 136-222 ; de profil centres des mains ≥ 10 et coudes ≥ 15 l'un de l'autre |
| « même en vue de profil on doit vraiment avoir l'impression que ses mains se touchent et qu'il craque du poing » | de profil : deux boules distinctes au contact, deux avant-bras distincts, un appui puis un à-coup lisibles | distances de profil (contrôle 4 ter) |

**Limite du rig.** Les deux épaules sont au même point (pas de largeur d'épaules), le bras
fait 34 et l'avant-bras 32. Avec l'avant-bras horizontal, il ne peut pas pointer droit vers
l'autre main : il faudrait un coude à plus de 34 de l'épaule. Le mieux possible est 45-50°
entre l'avant-bras et l'axe gauche-droite (autant vers l'avant que vers le centre). Pour la
même raison, de profil les deux coudes sont tous les deux près de la ligne du tronc : on ne
peut pas les écarter beaucoup l'un de l'autre (une torsion du buste de ±20° a été essayée :
elle n'aide pas, les coudes se rapprochent même).

### 2.4 Géométrie retenue (de trois quarts, paume posée sur le poing, sans traversée)

**Mesures du rig qui décident de tout.** La tête a un rayon de 23 et le cou une longueur
nulle : le point d'épaule (commun aux deux bras) est 20 sous le centre de la tête, donc
**dans** le disque. Des mains « 20 sous l'épaule » sont encore au menton (critique n° 7).
Les mains doivent donc être au sternum, environ 30 sous l'épaule, et loin devant.

**Bras le long du buste, un peu devant ; avant-bras vers l'avant.** C'est la vraie position
pour craquer ses poings devant soi : les coudes **bas et rentrés** (coudes vers l'intérieur,
demande de l'utilisateur), bras à 41-49° de la verticale, coudes 13-16 (N) et 22 (F) devant
l'épaule, 22-26 sous elle. Rien ne ressort derrière le dos (plus de « bosse »), pas d'aile
de face. Écartement des coudes fixé à 20° de chaque côté : les deux bras restent séparés en
profondeur et les avant-bras ne se croisent pas.

**Le poing F en bas, la paume N par-dessus.** Centres relatifs à l'épaule, dans le repère
du buste (x devant, y haut, z profondeur, N côté caméra = z négatif), puis tournés de 25°
avec lui : poing F (50, −29, 4), avant-bras horizontal (pente −6°) ; paume N (48, −13, −2),
posée sur le dessus du poing, avant-bras qui monte vers elle (pente +19 à +25°). De profil
on voit **deux avant-bras en V couché** qui se rejoignent sur deux boules l'une sur l'autre
(centres à 16-18 de profil) : une main posée sur un poing. Les mains sont 25 à 27 devant le
bord avant de la tête.

**Les mains se touchent sans se traverser.** Centres à 17,1-17,7 en 3D à toutes les clés
(deux rayons = 17).

**De trois quarts (idée de l'utilisateur).** De 104 à 136, le buste tourne de 25° vers la
caméra (`torsion` −25), la tête tourne d'autant dans l'autre sens (`neck_r` +25) : le regard
reste sur l'adversaire. La ligne des mains tourne avec la poitrine, ce qui sépare les deux
coudes de profil (7 à 10).

**Le craquement.** Le poing F ne bouge pas (avant-bras F horizontal, fixe). Il se lit par :
- l'**appui** (10 images, `acc`) : la paume serre (0,5 en arrière, 0,2 vers le bas), épaules
  qui montent de 2 et reculent (inspire), poitrine qui se creuse un peu ;
- le **crac** (2 images, `dec`) : la paume pousse le poing vers l'avant (3, puis 4 au second),
  le coude N s'ouvre (bras de 42 à 48°), les épaules tombent, les genoux cèdent, la tête
  hoche ;
- le **second craquement** est plus fort : poussée plus longue, bassin plus bas, hochement
  plus marqué.

## 2 bis. Stature : la ligne des épaules

Le bagarreur est droit et sûr de lui, et il le reste pendant le geste : buste droit, poitrine
un peu bombée, **épaules droites ou en arrière** (`epaule*_av` entre −3 et −1), jamais
enroulées vers l'avant, même au craquement. L'effort ne passe pas par le dos qui s'arrondit
mais par :
- les épaules qui montent à la prise d'appui (et reculent : on inspire, poitrine sortie),
  puis tombent d'un coup sur le craquement ;
- les coudes qui s'écartent ;
- les genoux qui cèdent un peu (le bassin descend de 1,5 puis 2,5) ;
- le hochement de tête.

## 3. Les phases

Durées à 60 images par seconde.

| Images | Phase | Jambes | Haut du corps |
|---|---|---|---|
| 0-40 | départ | départ de la marche détendue | le buste se redresse, les épaules reculent (en 20 images) |
| 40-96 | marche | un cycle de marche détendue | buste droit, bras qui balancent, épaules qui tournent un peu |
| 96-148 | dernier pas et arrêt | arrêt en un pas | à partir de 104, les mains montent devant le sternum et le buste tourne de trois quarts (la tête reste sur l'adversaire) ; paume posée sur le poing à 136, tenue jusqu'à 148 |
| 148-158 | appui 1 (10 images, `acc`) | posées | la paume serre le poing, épaules qui montent et reculent |
| 158-160 | crac 1 (2 images, `dec`) | genoux qui cèdent (bassin −1,5) | à-coup : la paume pousse le poing vers l'avant, coude N qui s'ouvre ; épaules qui tombent ; hochement |
| 160-180 | tenue puis relâche | | retour à la position posée |
| 180-190 | appui 2 (10 images, `acc`) | | la paume serre, épaules plus hautes, bassin qui se redresse |
| 190-192 | crac 2 (2 images, `dec`) | genoux qui cèdent plus (bassin −2,5) | à-coup plus fort ; hochement plus marqué ; buste toujours droit |
| 192-222 | tenue | | il regarde l'adversaire, menton qui remonte |
| 222-252 | retour au repos | | les mains se séparent et descendent, le buste reprend le repos |

## 4. Les poses clés, articulation par articulation

Repère : angles du squelette (voir `analyses/anatomie.md` § 4 bis et 6 bis).

Épaule : « bras / vert. » est l'angle réel du bras avec la verticale (abduction) ;
« plan » est l'angle de l'avant-bras vu de dessus (0 = vers le centre, 90 = devant) ; les
canaux du rig (arm, fore, _p, _r) suivent.

| Pose | N : bras / vert., pente, plan | N : arm / fore / _p / _r | F : bras / vert., pente, plan | F : arm / fore / _p / _r | Omoplates (haut, av) | Mains 3D ; profil mains, coudes |
|---|---|---|---|---|---|---|
| Posée (148) | 43°, +22°, 84° | 39 / 82 / 20 / 22 | 41°, −6°, 51° | 37 / 58 / −20 / −32 | 0, −1 | 17,2 ; 16,6 ; 9,0 |
| Appui 1 (158) | 42°, +22°, 83° | 36 / 85 / 20 / 20 | 42°, −6°, 50° | 35 / 58 / −20 / −34 | +2, −3 | 17,1 ; 16,5 ; 9,6 |
| Crac 1 (160) | 48°, +19°, 83° | 44 / 75 / 20 / 26 | 41°, −6°, 51° | 37 / 58 / −20 / −32 | −2, −1 | 17,6 ; 16,5 ; 7,4 |
| Appui 2 (190) | 41°, +22°, 83° | 34 / 85 / 20 / 20 | 43°, −7°, 50° | 34 / 57 / −20 / −35 | +2, −3 | 17,1 ; 16,7 ; 9,8 |
| Crac 2 (192) | 49°, +18°, 83° | 46 / 72 / 20 / 27 | 41°, −6°, 51° | 37 / 58 / −20 / −32 | −3, −1 | 17,7 ; 16,5 ; 7,1 |

De profil, le coude N est 13 à 16 devant l'épaule et le coude F 22 devant, tous deux 22 à 26
sous elle : deux bras qui descendent le long du buste, puis deux avant-bras vers l'avant.

| Pose | Bassin, buste | Jambes | Tête |
|---|---|---|---|
| Posée | root −5, bas du dos 3, poitrine 2, torsion −25 (trois quarts) ; bassin 2,5 plus bas que debout | pieds à plat, écartés (N à −21, F à +21 du bassin ; pied N devant, celui du dernier pas), hanches écartées ±13°, genoux légèrement fléchis par la descente du bassin, chevilles neutres | cou 4, `neck_r` +25 : visage vers l'adversaire |
| Appui 1 | poitrine 0 (inspire), épaules +2 en haut, −3 en arrière | idem | cou 3 |
| Crac 1 | poitrine 2, bassin −1,5, épaules −1 en avant (jamais devant) | genoux qui cèdent (flexion qui augmente de la descente du bassin) | cou 10 : hochement ; le regard reste sur l'adversaire (les yeux remontent) |
| Appui 2 | root −6, poitrine −1, épaules +2 en haut, −3 en arrière | idem posée | cou 2 |
| Crac 2 | poitrine 2, bassin −2,5 | genoux qui cèdent plus | cou 13 |

Au crac, le coude N s'ouvre (le bras N passe de 42 à 48° de la verticale) : c'est la
poussée de la paume qui donne l'à-coup ; le poing F reste en place. Le crac 2 est plus marqué que le crac 1 par
la hauteur d'appui, la chute des poings, la descente du bassin et le hochement.

Les angles du tableau sont ceux que `tools/resout_mains.sh` trouve pour la pose prête ; il
les recalcule à chaque clé avec le buste de la clé (les mains bougent ensemble : même
décalage appliqué à la seule paume N ; le poing F reste fixe). Il repart de la solution de la clé précédente, pour que les
bras ne changent pas de branche entre deux clés.

Pas de `decalage` sur les bras : deux mains verrouillées l'une sur l'autre suivent le buste
sans retard. Avec un retard (même égal pour les deux bras), la poussée sèche des genoux et
des épaules les faisait glisser l'une dans l'autre pendant 3 ou 4 images.

## 5. Ce qui se voit de profil

- Le buste un peu ouvert vers la caméra (trois quarts), la tête de profil vers l'adversaire.
- Devant le sternum, loin devant la tête : deux avant-bras en V couché, le poing en bas au
  bout d'un avant-bras horizontal, la paume posée dessus au bout d'un avant-bras qui monte ;
  deux boules l'une sur l'autre (centres à 16-18) : une main posée sur un poing.
- Les bras descendent le long du buste, coudes bas, rien derrière le dos.
- L'appui : les épaules qui montent et reculent.
- Le crac : en 2 images, la paume pousse le poing, le coude N s'ouvre, les épaules tombent,
  les genoux cèdent, la tête hoche.
- Le buste droit, épaules en arrière : la ligne du dos ne s'enroule pas.

## 6. Références

- Kawchuk G. N. et al., « Real-Time Visualization of Joint Cavitation », PLOS ONE, 2015
  (IRM ciné d'une MCP tirée jusqu'au craquement : formation d'une cavité, pas éclatement).
- Unsworth A., Dowson D., Wright V., « Cracking joints », Annals of the Rheumatic Diseases,
  1971 (hypothèse de l'éclatement de bulle, délai avant de pouvoir recraquer).
- Guides pratiques (wikiHow « Crack Your Knuckles », Livestrong) : poing enveloppé par l'autre
  main et pressé, ou jointures poussées dans la paume.

- Strength vs Speed, rouge 100-127 (`etudes/01_strength_vs_speed/planches/rouge_100_111_posture.png`) :
  le « costaud » n'est jamais en profil strict ; ses deux bras se lisent parce qu'un coude part
  derrière et l'autre devant, le buste un peu ouvert vers la caméra, la tête sur l'adversaire.
  C'est le principe du trois quarts retenu ici.
- Bible : § mise en scène (intro, victoire : poses tenues, lisibles), poses tenues après un
  geste sec (contraste de vitesse).
- Inventaire § 4 : intro dans les 3 animations de mise en scène du personnage.

## 7. Contrôles

1. Pieds : aucun glissement (`--verifier`), mêmes appuis que la marche détendue.
2. Buste droit pendant la marche : épaules au-dessus du bassin (écart horizontal < 3).
3. De face (`--vues`), mains au contact pendant le craquage, coudes bas, pas d'aile.
4. Rien ne se traverse (`--verifier`, contrôle en 3D) : mains à 16,8-18 l'une de
   l'autre à toutes les clés du craquage (deux rayons = 17), avant-bras qui ne se croisent
   pas (écartement des coudes ≥ 20°).
4 bis. Avant-bras F entre −12° et +12° (pente) ; avant-bras N qui monte (+15 à +25°) vers
   la paume posée sur le poing ; bras à 40-50° de la verticale, coudes devant l'épaule,
   rien derrière le dos.
4 ter. De profil : deux boules l'une sur l'autre au contact (centres 15-18), coudes
   ≥ 7 l'un de l'autre, deux avant-bras distincts loin devant la tête (mains ≥ 20 devant
   son bord) ; mains au sternum (≥ 28 sous l'épaule pour le poing F) ; tête tournée vers
   l'adversaire.
5. Épaules jamais en avant : `epaule*_av` ≤ −1 et poitrine ≤ 2 pendant tout le craquage.
6. Dernière image identique au repos (pas de saut vers `idle_repos`).
