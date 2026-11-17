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
| « même en vue de profil on doit vraiment avoir l'impression que ses mains se touchent et qu'il craque du poing » | de profil : deux boules distinctes au contact, deux avant-bras distincts, un appui puis un à-coup lisibles | distances de profil (contrôle 4 ter) |

**Limite du rig.** Les deux épaules sont au même point (pas de largeur d'épaules), le bras
fait 34 et l'avant-bras 32. Avec l'avant-bras horizontal, il ne peut pas pointer droit vers
l'autre main : il faudrait un coude à plus de 34 de l'épaule. Le mieux possible est 45-50°
entre l'avant-bras et l'axe gauche-droite (autant vers l'avant que vers le centre). Pour la
même raison, de profil les deux coudes sont tous les deux près de la ligne du tronc : on ne
peut pas les écarter beaucoup l'un de l'autre (une torsion du buste de ±20° a été essayée :
elle n'aide pas, les coudes se rapprochent même).

### 2.4 Géométrie retenue (première version, sans traversée)

**Les mains loin devant la poitrine.** C'est ce qui rendait la première version lisible : de
profil, les avant-bras sortent nettement du tronc et les poings joints sont bien devant le
sternum, à hauteur du bas de la poitrine. Centres des poings, relatifs à l'épaule (x devant,
y haut, z profondeur, N côté caméra = z négatif) : main N (25, −12, −8,5), poing F
(27, −15, +8,5).

**Les mains se touchent, elles ne se traversent pas.** Dans la première version, les deux
mains visaient le même point : elles étaient l'une dans l'autre. Ici elles sont côte à côte
en profondeur, distance 17,4 (deux rayons = 17) : contact franc, sans chevauchement. La
main N est un peu plus haute et un peu en retrait (3 plus haut, 2 en arrière) : c'est la
paume qui couvre le dessus du poing F. De profil, les centres sont à 3,6 : une seule masse de
poings joints au bout de deux avant-bras, comme dans la première version.

**Coudes ouverts, avant-bras presque horizontaux.** Chaque coude est cherché 6 sous sa main
(`coude_dy` −6) : avant-bras à +11° (la main un peu plus haute que le coude, poing levé
« je vais te casser la figure »). Les coudes s'ouvrent pour y arriver : bras à 58° (N) et
52° (F) de la verticale en position posée, 64-68° à l'appui (les coudes montent), 45-50° au
crac (ils tombent). Les coudes sont au niveau du tronc ou un peu devant (x 0 à +2).

**Le craquement, sans choc.** Les mains ne se quittent jamais (§ 2.1 : une force qui monte
lentement, puis la résistance qui cède). Le craquement se lit par :
- l'**appui** (10 images, puis 10, `acc`) : les poings remontent et reculent vers la poitrine
  de 3-4 (on serre en tirant), les coudes montent et s'ouvrent, les épaules montent et
  reculent (inspire) ;
- le **crac** (4 images, `dec`) : tout cède d'un coup : les poings partent devant et en bas
  (+6 et −8 depuis l'appui 1, +8 et −12 depuis l'appui 2), les coudes tombent, les épaules
  tombent, les genoux cèdent, la tête hoche ;
- le **second craquement** est plus fort (on recraque d'autres doigts) : appui plus haut,
  chute plus longue, bassin plus bas, hochement plus marqué.

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
| 96-148 | dernier pas et arrêt | arrêt en un pas | à partir de 104, les mains montent ; jointes à 136, posées à 148 |
| 148-158 | appui 1 (10 images, `acc`) | posées | poings qui remontent vers la poitrine, coudes et épaules qui montent |
| 158-162 | crac 1 (4 images, `dec`) | genoux qui cèdent (bassin −1,5) | à-coup : poings devant et en bas ; coudes et épaules qui tombent ; hochement |
| 162-180 | tenue puis relâche | | retour à la position posée |
| 180-190 | appui 2 (10 images, `acc`) | | poings plus haut, coudes plus ouverts, épaules plus hautes, bassin qui se redresse |
| 190-194 | crac 2 | genoux qui cèdent plus (bassin −2,5) | à-coup plus fort ; hochement plus marqué ; buste toujours droit |
| 194-222 | tenue | | il regarde l'adversaire, menton qui remonte |
| 222-252 | retour au repos | | les mains se séparent et descendent, le buste reprend le repos |

## 4. Les poses clés, articulation par articulation

Repère : angles du squelette (voir `analyses/anatomie.md` § 4 bis et 6 bis).

Épaule : « bras / vert. » est l'angle réel du bras avec la verticale (abduction) ;
« plan » est l'angle de l'avant-bras vu de dessus (0 = vers le centre, 90 = devant) ; les
canaux du rig (arm, fore, _p, _r) suivent.

| Pose | N : bras / vert., coude, pente, plan | N : arm / fore / _p / _r | F : bras / vert., coude, pente, plan | F : arm / fore / _p / _r | Omoplates (haut, av) | Mains (3D) ; profil |
|---|---|---|---|---|---|---|
| Posée (148) | 58°, coude 18 sous l'épaule, pente +11°, plan 50° | 3 / 128 / 58 / 16 | 52°, coude 21 sous l'épaule, pente +11°, plan 54° | 4 / 122 / −52 / −17 | 0, −1 | 17,4 ; profil mains 3,6, coudes 2,9 |
| Appui 1 (158) | 64°, coude 15 sous l'épaule, pente +11°, plan 46° | −4 / 135 / 64 / 10 | 58°, coude 18 sous l'épaule, pente +10°, plan 49° | −2 / 130 / −58 / −14 | +3, −3 | 17,3 ; profil mains 3,6, coudes 2,9 |
| Crac 1 (162) | 47°, coude 23 sous l'épaule, pente +11°, plan 58° | 3 / 118 / 47 / 16 | 45°, coude 24 sous l'épaule, pente +7°, plan 61° | 6 / 112 / −45 / −20 | −2, −1 | 17,4 ; profil mains 3,6, coudes 1,4 |
| Appui 2 (190) | 68°, coude 13 sous l'épaule, pente +11°, plan 43° | −6 / 138 / 68 / 7 | 62°, coude 16 sous l'épaule, pente +11°, plan 47° | −4 / 133 / −62 / −12 | +5, −3 | 17,3 ; profil mains 3,6, coudes 3,0 |
| Crac 2 (194) | 50°, coude 22 sous l'épaule, pente +5°, plan 57° | 6 / 115 / 50 / 23 | 51°, coude 21 sous l'épaule, pente −1°, plan 57° | 11 / 108 / −50 / −31 | −3, −1 | 17,4 ; profil mains 3,6, coudes 1,9 |

Les deux coudes sont à x = 0 à +4 de l'épaule (au niveau du tronc).

| Pose | Bassin, buste | Jambes | Tête |
|---|---|---|---|
| Posée | root −5, bas du dos 3, poitrine 2, torsion 0 ; bassin 2,5 plus bas que debout | pieds à plat, écartés (N à −21, F à +21 du bassin ; pied N devant, celui du dernier pas), hanches écartées ±13°, genoux légèrement fléchis par la descente du bassin, chevilles neutres | cou 4, regard sur l'adversaire |
| Appui 1 | poitrine 0 (inspire) | idem | cou 3 |
| Crac 1 | poitrine 2, bassin −1,5, épaules −1 en avant (jamais devant) | genoux qui cèdent (flexion qui augmente de la descente du bassin) | cou 10 : hochement ; le regard reste sur l'adversaire (les yeux remontent) |
| Appui 2 | root −6, poitrine −1 | idem posée | cou 2 |
| Crac 2 | poitrine 2, bassin −2,5 | genoux qui cèdent plus | cou 13 |

Les coudes : à l'appui ils montent (de 3 à 5) et s'ouvrent, au crac ils tombent de 8 et se
referment : c'est la chute qui donne l'à-coup. Le crac 2 est plus marqué que le crac 1 par
la hauteur d'appui, la chute des poings, la descente du bassin et le hochement.

Les angles du tableau sont ceux que `tools/resout_mains.sh` trouve pour la pose prête ; il
les recalcule à chaque clé avec le buste de la clé (les mains bougent ensemble : même
décalage pour les deux cibles). Les cibles des mains sont celles de la première version, décalées ensemble à chaque clé. Il repart de la solution de la clé précédente, pour que les
bras ne changent pas de branche entre deux clés.

Pas de `decalage` sur les bras : deux mains verrouillées l'une sur l'autre suivent le buste
sans retard. Avec un retard (même égal pour les deux bras), la poussée sèche des genoux et
des épaules les faisait glisser l'une dans l'autre pendant 3 ou 4 images.

## 5. Ce qui se voit de profil

- Les poings joints bien devant la poitrine, au bout de deux avant-bras presque horizontaux
  qui sortent du tronc : la silhouette de quelqu'un qui serre ses poings devant lui.
- De profil, la paume N et le poing F se recouvrent (centres à 3,6) : on voit une masse de
  poings joints. C'est ainsi dans la première version, que l'utilisateur a préférée ; le
  contact se lit de face et de trois quarts (deux boules côte à côte).
- L'appui : les poings qui remontent vers la poitrine, les coudes et les épaules qui montent.
- Le crac : un à-coup net vers l'avant et le bas, les épaules qui tombent, les genoux qui
  cèdent, la tête qui hoche.
- Le buste droit, épaules en arrière : la ligne du dos ne s'enroule pas.

## 6. Références

- Kawchuk G. N. et al., « Real-Time Visualization of Joint Cavitation », PLOS ONE, 2015
  (IRM ciné d'une MCP tirée jusqu'au craquement : formation d'une cavité, pas éclatement).
- Unsworth A., Dowson D., Wright V., « Cracking joints », Annals of the Rheumatic Diseases,
  1971 (hypothèse de l'éclatement de bulle, délai avant de pouvoir recraquer).
- Guides pratiques (wikiHow « Crack Your Knuckles », Livestrong) : poing enveloppé par l'autre
  main et pressé, ou jointures poussées dans la paume.

- Bible : § mise en scène (intro, victoire : poses tenues, lisibles), poses tenues après un
  geste sec (contraste de vitesse).
- Inventaire § 4 : intro dans les 3 animations de mise en scène du personnage.

## 7. Contrôles

1. Pieds : aucun glissement (`--verifier`), mêmes appuis que la marche détendue.
2. Buste droit pendant la marche : épaules au-dessus du bassin (écart horizontal < 3).
3. De face (`--vues`), mains jointes au centre pendant le craquage, coudes écartés.
4. Rien ne se traverse (`--verifier`, contrôle en 3D) : mains à 16,8-18 l'une de
   l'autre à toutes les images du craquage (deux rayons = 17), avant-bras qui ne se croisent
   pas.
4 bis. Avant-bras entre −12° et +12° (pente) aux clés de contact ; bras à ≥ 50° de la
   verticale en position posée et à l'appui, ≥ 44° au crac.
4 ter. De profil : avant-bras qui sortent du tronc (mains à ≥ 20 devant l'épaule) ; de face et
   de trois quarts, deux boules distinctes au contact.
5. Épaules jamais en avant : `epaule*_av` ≤ −1 et poitrine ≤ 2 pendant tout le craquage.
6. Dernière image identique au repos (pas de saut vers `idle_repos`).
