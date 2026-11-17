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

Détail de chaque main :
- **Poing (F)** : doigts fermés, pouce par-dessus ; poignet droit ou en très légère flexion
  (le dos du poing regarde vers l'avant et le haut, les jointures sont sous la paume N) ;
  avant-bras en pronation partielle (pouce vers le haut et vers soi).
- **Main qui presse (N)** : doigts serrés, paume posée sur le dos des doigts du poing, le
  talon de la main sur les jointures ; poignet en extension (la paume regarde le poing, donc
  vers le bas et vers le côté loin) ; avant-bras en pronation.
- **Le pouce N** passe sous le poing ou reste le long de l'index : la main N forme une coque.

La force vient des **pectoraux et du deltoïde antérieur** (les deux bras qui se rapprochent,
adduction horizontale des épaules), relayés par les **fléchisseurs du poignet et des doigts**
de la main N (elle se referme sur le poing) et par les **extenseurs du poignet** du côté du
poing (le poing ne se laisse pas plier, il résiste). Les **triceps et biceps** se contractent
ensemble : les coudes ne bougent presque pas, ce sont des leviers rigides. Le tronc est gainé
(il ne bascule pas avec l'effort).

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

**Les mains se touchent, elles ne se traversent pas.** Chaque poing est une boule de rayon
8,5 et chaque avant-bras un trait de 15 d'épaisseur ; deux parties du corps ne passent jamais
l'une dans l'autre. Les deux mains se rejoignent **au milieu, devant la poitrine** : le poing F
un peu du côté loin (+7), la paume N du côté caméra (−7), posée devant et au-dessus des
phalanges (+7 devant, +6 au-dessus). Les centres sont à 16,7 l'un de l'autre, juste moins que
deux rayons (17) : contact franc, sans chevauchement.

**Coudes ouverts, avant-bras tournés vers l'intérieur et horizontaux.** Les deux bras sont
symétriques : coudes sortis sur les côtés (écartement 55 à 65°), à la hauteur des mains, et
avant-bras qui **pointent l'un vers l'autre**, parallèles au sol, comme deux leviers qui
poussent l'un contre l'autre. Le rig n'a pas de largeur d'épaules (bras de 34, avant-bras de
32, attachés au même point) : avec l'avant-bras horizontal, il ne peut pas pointer
exactement vers le centre ; il fait 45 à 50° avec l'axe gauche-droite (0 = pointé vers
l'autre main). Rapprocher les mains du corps l'ouvrirait plus, mais les collerait au buste.

Erreur à ne pas refaire : un bras loin sous l'épaule et un bras proche tendu devant. De
profil, le bras loin disparaît derrière le tronc et il reste un bras qui montre quelque chose
au lieu de deux mains qui se serrent.

**Le choc.** À la prise d'appui la paume N se décolle du poing (elle monte de 5 à 6 : un
écart de 20 entre les centres, visible de profil), puis revient le **frapper** sèchement au
craquement (la traînée de vitesse du moteur le souligne), et les deux mains poussent ensemble
devant et en bas. Les coudes passent alors un peu au-dessus des mains (avant-bras à −5°) :
c'est le coude qui appuie.

Cibles (centre du poing, relatives à l'épaule ; x devant, y haut, z profondeur) :
poing F (26, −20, 7), main N (33, −14, −7). Les angles des bras sont calculés en 3D par
`tools/resout_mains.sh` : main au centre de la cible, coude à la hauteur voulue par rapport à
la main (`coude_dy` : 0 = avant-bras horizontal, −3/−4 à l'appui, +3 au craquement),
l'écartement du coude étant cherché entre 40 et 90°. L'outil affiche pour chaque clé la pente
des avant-bras et leur angle vers l'avant.

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
| 96-148 | dernier pas et arrêt | arrêt en un pas | à partir de 104, les mains montent ; prêtes à 136 |
| 148-160 | prise d'appui | posées | épaules haussées et reculées, mains qui remontent un peu vers soi, poitrine qui inspire |
| 160-164 | craquement 1 | genoux qui cèdent un peu | poussée sèche : mains vers l'avant et le bas, coudes écartés, épaules qui tombent (sans avancer), hochement |
| 164-178 | tenue puis relâche | | retour à la position prête |
| 178-190 | prise d'appui 2 | | plus haute que la première |
| 190-194 | craquement 2 | genoux qui cèdent plus | plus fort : coudes plus écartés, épaules qui tombent plus, hochement plus marqué ; buste toujours droit |
| 194-212 | tenue | | il regarde l'adversaire, menton qui remonte |
| 212-250 | retour au repos | | les mains se séparent et descendent, le buste reprend le repos |

## 4. Les poses clés, articulation par articulation

Repère : angles du squelette (voir `analyses/anatomie.md` § 4 bis et 6 bis).

| Pose | Bassin, buste | Épaules (omoplates) | Bras proche N | Bras loin F | Tête |
|---|---|---|---|---|---|
| Marche sûre | root −5, bas du dos 3, poitrine 2 (buste droit) ; torsion ±4 avec les bras | reculées −2 | balancier de la marche, écarté 16° | idem, −16° | cou 4 (menton horizontal) |
| Prête | idem, torsion 0 | reculées −2 | paume contre le poing loin : élévation 36°, coude 113°, écarté 59°, rotation +51° ; avant-bras horizontal tourné vers le centre | poing devant le sternum : élévation 4°, coude 119°, écarté −54°, rotation −29° ; avant-bras horizontal tourné vers le centre | cou 4 |
| Prise d'appui | poitrine 0 (inspire) | haussées +3, reculées −3 | les deux mains 3 plus haut, 3 plus près ; la paume N se décolle (+5 à +6 en haut) ; coude écarté 64° | idem (sans le décollement) | cou 3 |
| Craquement | poitrine 2 (droit), genoux un peu pliés (bassin −1,5) | abaissées −2, reculées −1 | la paume frappe le poing, les deux mains 3 plus bas, 2 plus loin ; coude écarté 58°, un peu au-dessus de la main | idem, −53° | cou 10 (hochement) |
| Fin | repos | 0 | repos | repos | repos |

Les angles du tableau sont ceux que `tools/resout_mains.sh` trouve pour la pose prête ; il
les recalcule à chaque clé avec le buste de la clé (les mains bougent ensemble : même
décalage pour les deux cibles). Il repart de la solution de la clé précédente, pour que les
bras ne changent pas de branche entre deux clés.

Pas de `decalage` sur les bras : deux mains verrouillées l'une sur l'autre suivent le buste
sans retard. Avec un retard (même égal pour les deux bras), la poussée sèche des genoux et
des épaules les faisait glisser l'une dans l'autre pendant 3 ou 4 images.

## 5. Ce qui se voit de profil

- Les deux poings l'un contre l'autre devant la poitrine, la paume proche devant et au-dessus
  du poing loin ; les deux avant-bras horizontaux, superposés (ils vont vers le centre, donc
  paraissent raccourcis : le vérificateur signale « bras proche raccourci », c'est voulu).
- Le choc : la main proche se décolle et monte à la prise d'appui (un vide entre les deux
  mains), puis revient frapper le poing d'un coup.
- Le buste droit, épaules en arrière : la ligne du dos ne s'enroule pas.
- L'écartement des coudes ne se voit que de face et de trois quarts : de profil, le craquement
  se lit aussi par le haussement puis la chute des épaules, les genoux qui cèdent, le hochement et
  les mains qui poussent vers l'avant et le bas.

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
4. Rien ne se traverse (`--verifier`, contrôle en 3D) : mains à 16,2-16,7 l'une de l'autre
   au contact (deux rayons = 17), 19,5 à 20,5 à la prise d'appui, avant-bras qui ne se croisent pas,
   à chaque image.
4 bis. Avant-bras à 0° au contact, +5/+7° à l'appui, −5° au craquement, tournés vers le centre
   (45-50° vers l'avant) ; coudes écartés de 55 à 65°, symétriques (sortie de
   `tools/resout_mains.sh`).
5. Épaules jamais en avant : `epaule*_av` ≤ −1 et poitrine ≤ 2 pendant tout le craquage.
6. Dernière image identique au repos (pas de saut vers `idle_repos`).
