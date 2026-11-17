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
l'une dans l'autre. La paume N est **posée sur** les phalanges du poing F : un peu devant
(+9), un peu au-dessus (+9) et chacune de son côté en profondeur (N côté caméra −5, F +6).
Les centres sont à 16,8 l'un de l'autre, juste moins que deux rayons (17) : contact franc, pas
de vide, pas de chevauchement. Comme chaque main reste de son côté, les deux avant-bras
arrivent chacun de son coude sans se croiser.

Cibles (centre du poing, relatives à l'épaule ; x devant, y haut, z profondeur) :
poing F (24, −20, 6), main N (33, −11, −5). Les angles des bras qui y mènent sont calculés
en 3D par `tools/resout_mains.sh` (`vise` ne règle que x et y : la profondeur venait de la
rotation des bras, et les mains finissaient l'une dans l'autre).

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
| Prête | idem, torsion 0 | reculées −2 | main posée sur le poing loin : élévation 19°, coude 116°, écarté 35°, rotation +16° | poing devant le sternum : élévation −8° (coude sous l'épaule), coude 123°, écarté −35°, rotation −10° | cou 4 |
| Prise d'appui | poitrine 0 (inspire) | haussées +3, reculées −3 | les deux mains 3 plus haut, 3 plus près | idem | cou 3 |
| Craquement | poitrine 2 (droit), genoux un peu pliés (bassin −1,5) | abaissées −2, reculées −1 | les deux mains 5 plus bas, 3 plus loin ; coudes écartés à 45° | idem, −45° | cou 10 (hochement) |
| Fin | repos | 0 | repos | repos | repos |

Les angles du tableau sont ceux que `tools/resout_mains.sh` trouve pour la pose prête ; il
les recalcule à chaque clé avec le buste de la clé (les mains bougent ensemble : même
décalage pour les deux cibles). Il repart de la solution de la clé précédente, pour que les
bras ne changent pas de branche entre deux clés.

Pas de `decalage` sur les bras : deux mains verrouillées l'une sur l'autre suivent le buste
sans retard. Avec un retard (même égal pour les deux bras), la poussée sèche des genoux et
des épaules les faisait glisser l'une dans l'autre pendant 3 ou 4 images.

## 5. Ce qui se voit de profil

- La main proche posée sur le poing loin, un peu devant et au-dessus de lui, devant le
  sternum ; les coudes sous les épaules.
- Le buste droit, épaules en arrière : la ligne du dos ne s'enroule pas.
- L'écartement des coudes ne se voit que de face et de trois quarts : de profil, le craquement
  se lit par le haussement puis la chute des épaules, les genoux qui cèdent, le hochement et
  les mains qui poussent vers l'avant et le bas.

## 6. Références

- Bible : § mise en scène (intro, victoire : poses tenues, lisibles), poses tenues après un
  geste sec (contraste de vitesse).
- Inventaire § 4 : intro dans les 3 animations de mise en scène du personnage.

## 7. Contrôles

1. Pieds : aucun glissement (`--verifier`), mêmes appuis que la marche détendue.
2. Buste droit pendant la marche : épaules au-dessus du bassin (écart horizontal < 3).
3. De face (`--vues`), mains jointes au centre pendant le craquage, coudes écartés.
4. Rien ne se traverse (`--verifier`, contrôle en 3D) : mains à 16,8 l'une de l'autre
   (contact, deux rayons = 17), avant-bras qui ne se croisent pas, à chaque image.
5. Épaules jamais en avant : `epaule*_av` ≤ −1 et poitrine ≤ 2 pendant tout le craquage.
6. Dernière image identique au repos (pas de saut vers `idle_repos`).
