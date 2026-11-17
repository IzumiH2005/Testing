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
| « L'angle d'ouverture des épaules sur les côtés doit être un peu plus » | coudes sortis sur les côtés | bras / verticale ≥ 59° (N) et ≥ 43° (F) à toutes les clés (sortie « profil : … bras/verticale ») |
| « les avant-bras doivent être quasiment parallèles au sol lorsque les poings entrent en contact » | pente de chaque avant-bras entre −12° et +12° au contact | « pente » de resout_mains |
| « les coudes ne sont pas assez tournés vers l'intérieur » | les avant-bras pointent vers le centre (l'un vers l'autre) autant que le rig le permet, sans ramener les mains contre la poitrine | avant-bras F « vers l'avant » ≤ 45° (31-39°) ; l'avant-bras N, lui, pointe devant (79-90°) : c'est le prix de la lisibilité de profil (son coude part vers la caméra et en arrière pour se détacher du coude F) ; coudes tous deux devant le buste |
| « Les coudes devraient être légèrement en arrière au lieu d'aligner au buste je pense » | essayé (coudes à −2 puis −7) : les mains se retrouvent sous le menton, illisibles de profil ; remplacé par la demande suivante | — |
| « Finalement c'est la première version qui correspondait le plus […] utilise-la comme base » | on reprend la toute première version (mains loin devant la poitrine, coudes ouverts, poings joints) ; on n'y corrige que les traversées (mains en 3D, côte à côte en profondeur) et la stature (épaules qui avançaient au crac) | rendu comparé à la première version ; contrôles 4 et 5 |
| « Et si cette pose […] tu la faisais en 3/4 au lieu de profil […] sa tête est bien sûr tournée vers son adversaire » | pendant le craquage, buste tourné de 35° vers la caméra, cibles des mains tournées avec lui ; tête tournée d'autant dans l'autre sens | `torsion` −35, `neck_r` +35 aux clés 136-222 ; de profil coudes ≥ 14 l'un de l'autre |
| « même en vue de profil on doit vraiment avoir l'impression que ses mains se touchent et qu'il craque du poing » | de profil : deux boules distinctes au contact, deux avant-bras distincts, un appui puis un à-coup lisibles | distances de profil (contrôle 4 ter) |

**Limite du rig.** Les deux épaules sont au même point (pas de largeur d'épaules), le bras
fait 34 et l'avant-bras 32. Avec l'avant-bras horizontal, il ne peut pas pointer droit vers
l'autre main : il faudrait un coude à plus de 34 de l'épaule. Le mieux possible est 45-50°
entre l'avant-bras et l'axe gauche-droite (autant vers l'avant que vers le centre). Pour la
même raison, de profil les deux coudes sont tous les deux près de la ligne du tronc : on ne
peut pas les écarter beaucoup l'un de l'autre en restant de profil strict (une torsion de
±20° n'aidait pas). Ce qui marche : une torsion de −35° **avec** le coude N écarté vers
l'extérieur (≥ 28°) : il part alors en arrière et le coude F en avant (14,6 à 19,4 de profil).
Un coude N rentré vers l'intérieur (écartement négatif) fait croiser les avant-bras.

### 2.4 Géométrie retenue (de trois quarts, paume qui roule sur le poing, sans traversée)

**Mesures du rig qui décident de tout.** La tête a un rayon de 23 et le cou une longueur
nulle : le point d'épaule (commun aux deux bras) est 20 sous le centre de la tête, donc
**dans** le disque. C'est une limite du rig (stylisation : pas de cou), pas un choix de
pose. Les mains sont donc au sternum, 29 à 31 sous l'épaule, et loin devant.

**De trois quarts (idée de l'utilisateur).** De 104 à 136, le buste tourne de 35° vers la
caméra (`torsion` −35) et reste ainsi pendant tout le craquage ; la tête tourne d'autant
dans l'autre sens (`neck_r` +35) : le regard reste sur l'adversaire. Cette torsion est le
levier qui sépare les bras de profil : le coude N, écarté vers l'extérieur (28 à 37°),
part vers la caméra **et en arrière**, le coude F (22 à 29°) part vers l'avant. De profil,
les coudes sont à **14,6 à 19,4** l'un de l'autre (contre 7 à 10 avant : défaut n° 3).

**Le poing F en bas, la paume N qui roule dessus.** Centres relatifs à l'épaule, dans le
repère du buste (x devant, y haut, z profondeur, N côté caméra = z négatif), puis tournés
de 35° avec lui. Poing F (50, −29, 4) : avant-bras presque horizontal (pente −5 à −8°).
La paume N est **toujours au contact** : son centre est à 17,1 du centre du poing (deux
rayons), décalé de 6 vers la caméra, et posé sur un cercle autour du poing à un angle
`th` depuis la verticale (0 = juste au-dessus, + = vers l'avant, sur les jointures) :
- **posée** (`th` 15°) : la paume coiffe le poing, un peu en avant ;
- **appui** (`th` 0°) : la paume revient juste au-dessus et serre ;
- **crac** (`th` 38°) : la paume roule vers l'avant sur les jointures et les plie.
Ce roulement est le geste qu'on lit (défaut n° 4 : plus deux boules empilées comme une
batte ; défaut n° 2 : l'appui se voit).

**Les coudes.** Coude N au-dessus du coude F : 12 à 16 sous la paume au repos et au crac,
6 seulement à l'appui (le coude N **monte** pour serrer : c'est le geste visible de
l'appui), 6 devant l'épaule ; coude F 4 sous le poing, 24 devant l'épaule. Avant-bras F
quasi parallèle au sol, avant-bras N qui monte un peu vers la paume (+4°, +11° à l'appui)
puis horizontal au crac (−2°) : les avant-bras sont quasi parallèles au sol (demande de
l'utilisateur). Épaules ouvertes, coudes devant le buste.

**Les mains se touchent sans se traverser.** Centres à 16,9-17,2 en 3D à toutes les clés
(deux rayons = 17) ; de profil, centres à 13,4-16,4.

**Le craquement.** Le buste ne bouge pas (droit et constant : défaut n° 7). Il se lit par :
- l'**appui** (10 images, `acc`) : la paume revient au-dessus du poing et serre (le poing
  descend de 1,5 contre elle), les **deux mains reculent de 3,5** (4 au second) vers la
  poitrine, le coude N monte, les épaules montent de 4 (5) et reculent (−3), le menton se
  lève (`neck` −2, −3) : on inspire ;
- le **crac** (2 images, `dec`) : la paume roule vers l'avant (`th` 0 → 38°), le poing F
  remonte et recule de 1,5 (2) contre elle, le coude N tombe, les épaules tombent (−2, −3),
  la tête hoche (`neck` 9, 11), les genoux cèdent à peine (bassin −0,5, −0,8 : plus de
  plongeon, défaut n° 1) ;
- le **second craquement** est plus fort : appui plus haut, recul plus grand, hochement et
  chute des épaules plus marqués.

## 2 bis. Stature : la ligne des épaules

Le bagarreur est droit et sûr de lui, et il le reste pendant le geste : buste droit, poitrine
un peu bombée, **épaules droites ou en arrière** (`epaule*_av` entre −3 et −1), jamais
enroulées vers l'avant, même au craquement. L'effort ne passe pas par le dos qui s'arrondit
mais par :
- les épaules qui montent à la prise d'appui (et reculent : on inspire, poitrine sortie),
  puis tombent d'un coup sur le craquement ;
- les coudes qui s'écartent ;
- les genoux qui cèdent à peine (le bassin descend de 0,5 puis 0,8) ;
- le hochement de tête.

## 3. Les phases

Durées à 60 images par seconde.

| Images | Phase | Jambes | Haut du corps |
|---|---|---|---|
| 0-40 | départ | départ de la marche détendue | le buste se redresse, les épaules reculent (en 20 images) |
| 40-96 | marche | un cycle de marche détendue | buste droit, bras qui balancent, épaules qui tournent un peu |
| 96-148 | dernier pas et arrêt | arrêt en un pas | à partir de 104, les mains montent devant le sternum et le buste tourne de trois quarts (la tête reste sur l'adversaire) ; paume posée sur le poing à 136, tenue jusqu'à 148 |
| 148-158 | appui 1 (10 images, `acc`) | posées | la paume revient au-dessus du poing et serre, les mains reculent de 3,5, coude N qui monte, épaules qui montent et reculent, menton levé |
| 158-160 | crac 1 (2 images, `dec`) | genoux qui cèdent à peine (bassin −0,5) | à-coup : la paume roule vers l'avant sur les jointures, le poing remonte contre elle ; coude N et épaules qui tombent ; hochement |
| 160-180 | tenue puis relâche | | retour à la position posée |
| 180-190 | appui 2 (10 images, `acc`) | | idem appui 1, mains qui reculent de 4, épaules plus hautes |
| 190-192 | crac 2 (2 images, `dec`) | bassin −0,8 | à-coup plus fort ; hochement plus marqué ; buste toujours droit |
| 192-222 | tenue | | il regarde l'adversaire, menton qui remonte |
| 222-252 | retour au repos | | les mains se séparent et descendent, le buste reprend le repos |

## 4. Les poses clés, articulation par articulation

Repère : angles du squelette (voir `analyses/anatomie.md` § 4 bis et 6 bis).

Épaule : « bras / vert. » est l'angle réel du bras avec la verticale ; « plan » est l'angle
de l'avant-bras vu de dessus (0 = vers l'autre main, 90 = devant) ; les canaux du rig
(arm = élévation, fore = flexion du coude, _p = écartement du coude, _r = rotation) suivent.
Les omoplates sont `epaule*_haut` et `epaule*_av` (identiques des deux côtés).

| Pose | N : bras / vert., pente, plan | N : arm / fore / _p / _r | F : bras / vert., pente, plan | F : arm / fore / _p / _r | Omoplates (haut, av) | Mains 3D ; profil mains, coudes |
|---|---|---|---|---|---|---|
| Posée (136-148, 180, 214-222) | 62°, +4°, 81° | 58 / 65 / 28 / 53 | 43°, −8°, 39° | 38 / 57 / −22 / −37 | 0, −1 | 17,2 ; 15,5 ; 14,6 |
| Appui 1 (158) | 59°, +11°, 90° | 50 / 87 / 37 / 49 | 46°, −7°, 31° | 35 / 70 / −29 / −44 | +4, −3 | 17,1 ; 16,4 ; 19,4 |
| Crac 1 (160) | 68°, −2°, 79° | 65 / 56 / 28 / 65 | 43°, −5°, 36° | 36 / 64 / −25 / −38 | −2, −1 | 16,9 ; 13,5 ; 15,7 |
| Appui 2 (190) | 59°, +11°, 89° | 49 / 88 / 37 / 49 | 43°, −5°, 33° | 33 / 71 / −28 / −40 | +5, −3 | 17,0 ; 16,3 ; 19,1 |
| Crac 2 (192) | 68°, −2°, 79° | 65 / 57 / 28 / 65 | 44°, −5°, 34° | 37 / 67 / −27 / −40 | −3, −1 | 16,9 ; 13,4 ; 15,6 |

De profil (repère de l'épaule) : coude N 5 à 13 devant l'épaule et 13 à 18 sous elle ;
coude F 23-24 devant et 24-25 sous elle. Le coude N est plus haut et plus en arrière que le
coude F : deux bras distincts, deux avant-bras vers l'avant.

| Pose | Bassin, buste | Jambes | Tête |
|---|---|---|---|
| Posée | root −5, bas du dos 3, poitrine 2, torsion −35 (trois quarts) ; bassin 2,5 plus bas que debout | pieds à plat, écartés (N à −21, F à +21 du bassin ; pied N devant, celui du dernier pas), hanches écartées ±13°, genoux légèrement fléchis par la descente du bassin, chevilles neutres | cou 4, `neck_r` +35 : visage vers l'adversaire |
| Appui 1 | poitrine 1 (inspire), épaules +4 en haut, −3 en arrière | idem | cou −2 : menton levé |
| Crac 1 | poitrine 2, bassin −0,5, épaules −2 (tombent), −1 en arrière | genoux qui cèdent à peine | cou 9 : hochement ; le regard reste sur l'adversaire |
| Appui 2 | poitrine 1, épaules +5 en haut, −3 en arrière | idem posée | cou −3 |
| Crac 2 | poitrine 2, bassin −0,8, épaules −3 | genoux qui cèdent un peu plus | cou 11 |
| Fin (214-222) | comme posée | idem | cou 1 : menton qui remonte |

Le buste (root, bas du dos, torsion) est le même à toutes les clés du craquage : rien ne
penche en arrière (défaut n° 7). La poitrine varie de 1 (inspire) à 2.

Les angles des bras sont ceux que `tools/resout_mains.sh` trouve à chaque clé, avec le buste
de la clé, à partir des cibles de mains en 3D, des hauteurs et positions avant-arrière de
coudes imposées (`coude_dy`, `coude_dx`) et d'un écartement cherché dans [28, 45] (N) et
[20, 40] (F). Il repart de la solution de la clé précédente, pour que les bras ne changent
pas de branche entre deux clés.

Pas de `decalage` sur les bras : deux mains verrouillées l'une sur l'autre suivent le buste
sans retard.

## 5. Ce qui se voit de profil

- Le buste ouvert vers la caméra (trois quarts), la tête de profil vers l'adversaire.
- Devant le sternum, loin devant la tête : deux bras distincts (coudes à 15-19 l'un de
  l'autre), le coude N plus haut et en arrière, le coude F plus bas et devant ; deux
  avant-bras quasi horizontaux vers l'avant.
- Au bout : le poing F, et la paume N posée dessus, un peu en avant ; à l'appui elle revient
  au-dessus, au crac elle roule vers l'avant sur les jointures.
- L'appui : les mains reculent vers la poitrine, le coude N monte, les épaules montent et
  reculent, le menton se lève.
- Le crac : en 2 images, la paume roule, le poing remonte contre elle, le coude N et les
  épaules tombent, la tête hoche.
- Le buste droit et immobile, épaules en arrière : la ligne du dos ne s'enroule pas.

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

1. Pieds : aucun glissement (`--verifier`), mêmes appuis que la marche détendue. Les
   « jambes superposées » que signale le vérificateur pendant la marche (images 25-28,
   55-58, 83-85, 111-115) sont le croisement normal des jambes de profil au passage du pied
   (la marche détendue validée a les mêmes) : ce n'est pas une traversée en 3D.
2. Buste droit pendant la marche : épaules au-dessus du bassin (écart horizontal < 3) ;
   buste identique (root, bas du dos, torsion) à toutes les clés du craquage.
3. De face (`--vues`), mains au contact pendant le craquage, coudes devant le buste.
4. Rien ne se traverse (`--verifier`, contrôle en 3D) : mains à 16,8-17,5 l'une de
   l'autre à toutes les clés du craquage (deux rayons = 17), avant-bras qui ne se croisent
   pas.
4 bis. Avant-bras F entre −10° et 0° (pente) ; avant-bras N entre −5° et +12° ; paume à
   `th` 15° posée, 0° à l'appui, 38° au crac.
4 ter. De profil : poing et paume au contact (centres 13-17), coudes ≥ 14 l'un de l'autre,
   deux avant-bras distincts loin devant la tête ; poing F ≥ 28 sous l'épaule ; tête
   tournée vers l'adversaire.
4 quater. Le crac se lit par la main (roulement de 38°) plus que par les genoux : bassin
   −0,5 et −0,8 au plus.
5. Épaules jamais en avant : `epaule*_av` ≤ −1 et poitrine ≤ 2 pendant tout le craquage.
6. Dernière image identique au repos (pas de saut vers `idle_repos`).
7. « Trajet rapide handN 192 » au vérificateur : c'est l'à-coup voulu du crac (2 images).
