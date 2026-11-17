# Analyse : victoire du bagarreur (stickman noir)

Animation de mise en scène jouée quand le bagarreur gagne le round (INVENTAIRE § 4, « mise en
scène : intro, victoire, provocation »). Il regarde vers la droite ; l'adversaire est au sol
devant lui. Départ : la garde ouverte (première image de `sortie_de_garde`). Fin : une pose
tenue (`boucle` false : le moteur garde la dernière image affichée, pas d'animation suivante).

Mesures du rig utilisées partout (style `epais` du bagarreur) : tête de rayon 23, cou de
longueur 0, centre de la tête à 20,2 au-dessus du point d'épaule (commun aux deux bras),
sommet du crâne à 43 au-dessus de ce point ; bras 34, avant-bras 32 (66 bras tendu).
Conventions : `arm*` positif = vers l'avant ; `neck` positif = flexion (menton vers la
poitrine), négatif = extension ; `neck_p` positif = oreille vers le côté N (caméra) ;
`neck_r` positif = visage vers la caméra.

## 1. La logique du mouvement

L'intro l'a montré : le bagarreur est droit, sûr de lui, il fait craquer ses poings avant de se
battre. Sa victoire est la suite logique du même personnage, sans exubérance (pas de saut, pas
de danse) : **le combat est fini, il relâche, il se fait craquer la nuque, puis il lève un
poing, menton haut, en regardant celui qu'il a battu.**

1. **Il sort de la garde.** Il n'a plus besoin de se protéger : il reprend tel quel le
   mouvement `sortie_de_garde` (60 images, pas levé compris, pieds qui finissent à ±21 du
   bassin), mais finit sur la stature du bagarreur (buste droit) et non sur le repos voûté
   du stickman.
2. **Il se fait craquer la nuque, d'un côté puis de l'autre.** Le même geste que les poings
   dans l'intro, sur une autre articulation. Seul, on se fait craquer la nuque surtout en
   **rotation jusqu'à la butée** combinée à une inclinaison oblique, **menton vers la
   clavicule** : la tête tourne, penche et descend vers une épaule, tire lentement jusqu'à la
   butée, puis un à-coup bref (le craquement), un petit rebond. Ce geste a une composante
   dans le plan du profil (la flexion : la tête descend et avance), c'est elle qui le rend
   lisible en jeu. Il **hausse l'épaule** du côté où il penche pendant la tension (il « coince »
   la tête), et elle **tombe** au craquement : comme le bras suit l'épaule, ça se voit.
3. **Il roule les épaules** : il les hausse puis les tire en arrière, et la poitrine sort.
4. **Il lève le poing.** Le poing du côté caméra monte devant lui, coude à un peu au-dessus de
   l'épaule et devant, avant-bras vertical, poing au-dessus du crâne : le geste « je suis le
   plus fort ». La poitrine s'ouvre, le menton monte. L'autre poing reste serré le long du
   corps, coude un peu décollé.
5. **Il tient la pose.** Respiration lente (épaules qui montent et descendent de 1), le poing
   levé qui se serre une fois (petite montée de 2). Rien d'autre ne bouge.

## 2. Anatomie

### 2.1 Le craquement de la nuque (recherches)

- Ce qui craque : les articulations entre les vertèbres du cou (articulations zygapophysaires,
  ou « facettes »), comme les doigts : en les étirant, la pression du liquide synovial chute,
  une cavité se forme d'un coup, c'est le bruit (Kawchuk et al., PLOS ONE 2015, montré sur les
  doigts ; le bruit des facettes cervicales lors d'une manipulation est étudié par Reggars et
  Pollard, J. Manipulative Physiol. Ther., 1995). Il faut une **mise en tension lente jusqu'à la butée**, puis un petit
  dépassement : le craquement est un à-coup bref, de faible amplitude (quelques degrés).
- Le geste, quand on le fait seul (sans manipulation) : **rotation** du cou jusqu'à la butée,
  combinée à une **inclinaison** et une **flexion** (menton vers la clavicule). Muscles qui inclinent : sterno-cléido-mastoïdien, scalènes, trapèze supérieur du
  côté vers lequel on penche ; du côté opposé, les mêmes muscles s'étirent. On baisse
  l'épaule opposée (trapèze supérieur qui se relâche, omoplate qui descend) pour étirer plus.
- Amplitudes (rig : `neck` −60..50, `neck_p` ±40, `neck_r` ±80) : tension : rotation 20°,
  inclinaison 20°, flexion du cou de 4 à 14 ; craquement : rotation et inclinaison 26°,
  flexion 26 (à-coup de 12° en 3 images : la tête descend et avance d'environ 4, c'est ce qui
  se lit de profil ; l'amplitude réelle est de quelques degrés, on l'exagère pour la
  lisibilité, comme le craquage des poings de l'intro).

### 2.2 Le poing levé (recherches)

- Le geste de triomphe (bras levé, menton haut, poitrine ouverte) est universel : Tracy et
  Matsumoto (PNAS, 2008) l'observent chez les judokas aux Jeux olympiques et paralympiques, y
  compris chez des athlètes aveugles de naissance. C'est un affichage de fierté, pas un geste
  appris.
- Lever le bras au-dessus de l'épaule : **flexion de l'épaule** (deltoïde antérieur, faisceau
  claviculaire du grand pectoral) et, au-delà de 90°, **rotation de l'omoplate vers le haut**
  (trapèze supérieur et inférieur, dentelé antérieur) : l'épaule monte un peu, c'est
  anatomique, pas un haussement d'épaule.
- Géométrie retenue (bras 34, avant-bras 32, épaule sous le centre de la tête) : bras levé
  devant à **35° au-dessus de l'horizontale** (le coude sort de la tête de profil : un bras
  plus vertical partirait du crâne), un peu sur le côté ; **avant-bras vertical** ; le coude
  plie donc d'environ 55° (biceps, brachial). Poing serré (fléchisseurs des doigts), poignet
  dans l'axe. Poing visé, relatif à l'épaule : 28 devant, 51 au-dessus (8 au-dessus du
  crâne), 15 vers la caméra (de face il est à côté de la tête, pas au-dessus).
- La tête bascule en arrière (extension du cou : muscles de la nuque, splénius, trapèze
  supérieur). La tête est un disque sans visage : le « menton haut » ne se lit que par le
  déplacement de la tête (3,5 pour 10°) ; la poitrine qui sort le complète.
- La poitrine s'ouvre : extension du haut du dos (érecteurs du rachis), omoplates rapprochées
  (rhomboïdes, trapèze moyen) côté bras baissé.

### 2.3 Le bras qui reste en bas

Bras le long du corps, décollé de 18° (`armF_p` −18, règle « jamais collé » de
`anatomie.md` § 4 bis), coude plié à 25° (poing serré, l'avant-bras se contracte), poing un
peu devant la hanche.

## 2 bis. Stature (règle 6)

Buste droit, poitrine bombée, épaules en arrière (`epaule*_av` ≤ 0) pendant toute
l'animation. Au poing levé, l'épaule N **monte** (rotation de l'omoplate, `epauleN_haut` +4)
mais ne passe pas devant (`epauleN_av` −1). Au craquement de nuque, l'épaule du côté où la
tête penche monte (+2) puis tombe (−2), l'autre descend (−3), sans jamais avancer.

## 3. Les phases

À 60 images par seconde. Longueur 264 images (4,4 s). Un seul fichier fait foi : la fiche ;
le générateur `tools/gen_victoire_bagarreur.py` reprend ces numéros d'images.

| Images | Phase | Jambes | Haut du corps | Tête |
|---|---|---|---|---|
| 0-60 | sortie de garde : clés 0-58 de `sortie_de_garde` telles quelles (le pied qui se lève, le bassin qui monte), clé 60 remplacée par la pose « Relâché » | pieds qui finissent à ±21,09 du bassin, bassin à 87,78 (hauteur du repos) | buste qui se redresse jusqu'à la stature du bagarreur ; poings qui descendent | cou 4 |
| 60-66 | temps | | | |
| 66-84 | tension nuque côté N (`dec` : il tire puis ralentit à la butée) | | épaule N qui monte (+2), épaule F qui descend (−3) | rotation et inclinaison vers N jusqu'à 20°, flexion du cou 4 → 14 |
| 84-87 | crac 1 (`dec`) | | épaule N qui tombe (−2) | flexion 26, rotation et inclinaison 26 |
| 87-91 | rebond (`acc-dec`) | | épaule N −1 | flexion 22, 24° |
| 91-104 | retour au centre (`acc-dec`) | | épaules à 0 | cou 4, 0°, 0° |
| 104-122 | tension côté F (`dec`) | | épaule N qui descend (−3, visible : le bras N descend avec), épaule F +2 | rotation et inclinaison vers F jusqu'à −20°, flexion 14 |
| 122-125 | crac 2 (`dec`) | | épaule N −4 | flexion 26, −26° |
| 125-129 | rebond | | épaule N −3 | flexion 22, −24° |
| 129-142 | retour (`acc-dec`) | | | cou 4 |
| 142-152 | il hausse les épaules (`acc-dec`) | | `epaule*_haut` +3 | |
| 152-162 | il les tire en arrière, la poitrine sort (`acc-dec`) | | `epaule*_haut` 0, `epaule*_av` −3, poitrine 0 | |
| 162-170 | temps, il regarde l'adversaire au sol (`acc-dec`) | | `epaule*_av` −2, poitrine 2 | cou 10 (la tête descend vers lui) |
| 170-186 | départ du poing (`acc`) | | poing N qui monte devant | menton qui remonte |
| 186-194 | arrivée sèche (`dec`) | genoux tendus, bassin +1 | poing levé, poitrine qui s'ouvre (torsion −8) | cou −10 |
| 194-200 | il serre (`acc-dec`) | | poing levé +2 puis retour | |
| 200-264 | tenue | | respiration : `epaule*_haut` +1 à 216 et 248, 0 à 232 et 264 | |

## 4. Les poses clés, articulation par articulation

Repère : angles du squelette (`analyses/anatomie.md` § 4 bis et 6 bis). N = côté caméra.

### Garde (0) : première image de `sortie_de_garde`

Reprise telle quelle (raccord exact). Les clés 0 à 58 de `sortie_de_garde` sont reprises sans
changement (pieds et bassin compris : aucun glissement n'est ajouté).

### Relâché (60)

| Partie | Axes |
|---|---|
| Pieds | à plat, ceux de la clé 60 de `sortie_de_garde` : N à −21,09, F à +21,09 du bassin, y 7,5 ; écart en profondeur 9 (`ecartement.jambes`, c'est lui qui fait foi) |
| Hanches | flexion ±(celle du repos), écartement `thigh*_p` ±5 (repos), rotation ±10 (repos) |
| Genoux | ceux du repos (7°) ; bassin à 87,78 |
| Bassin, buste | root −5, bas du dos 3, poitrine 2 (poitrine bombée), torsion 0 |
| Épaules (omoplates) | `epaule*_av` −2, `epaule*_haut` 0 |
| Bras N | `armN` 4 (le long du corps, un peu devant), `armN_p` 16, `armN_r` 0, `foreN` 18 |
| Bras F | `armF` 6, `armF_p` −16, `armF_r` 0, `foreF` 18 |
| Tête | `neck` 4, `neck_p` 0, `neck_r` 0 |

### Nuque, tension côté N (84)

Comme 60, plus : `neck` 14, `neck_p` +20 (oreille vers l'épaule N), `neck_r` +20 (visage qui
tourne vers l'épaule N), `epauleN_haut` +2, `epauleF_haut` −3.

### Crac 1 (87) et rebond (91)

87 : `neck` 26, `neck_p` +26, `neck_r` +26, `epauleN_haut` −2, `epauleF_haut` −3.
91 : `neck` 22, `neck_p` +24, `neck_r` +24, `epauleN_haut` −1.

### Côté F : tension (122), crac 2 (125), rebond (129)

122 : `neck` 14, `neck_p` −20, `neck_r` −20, `epauleN_haut` −3, `epauleF_haut` +2.
125 : `neck` 26, `neck_p` −26, `neck_r` −26, `epauleN_haut` −4.
129 : `neck` 22, `neck_p` −24, `neck_r` −24, `epauleN_haut` −3.

### Épaules haussées (152) puis tirées en arrière (162)

152 : `epaule*_haut` +3. 162 : `epaule*_haut` 0, `epaule*_av` −3, poitrine 0 (elle sort).

### Poing levé (194)

| Partie | Axes |
|---|---|
| Pieds, genoux | comme 60, genoux tendus ; bassin +1 (88,78) |
| Bassin, buste | root −6, bas du dos 2, poitrine −2 (le haut du dos s'étend : poitrine qui sort), torsion −8 (la poitrine s'ouvre un peu vers la caméra, côté bras levé) |
| Épaule N | élévation : bras devant, à environ 35° au-dessus de l'horizontale (`armN` ≈ 125) ; plan : devant et un peu vers la caméra (`armN_p` ≈ 15, au plus 25) ; rotation `armN_r` : celle qui met l'avant-bras vertical, dans le plan du bras (le poing ne revient pas vers le centre de la tête) ; omoplate : `epauleN_haut` +4, `epauleN_av` −1 |
| Coude N | plié d'environ 55° (`foreN` ≈ 55) : avant-bras vertical |
| Poing N | centre visé, relatif à l'épaule : (28 devant, 51 au-dessus, 15 vers la caméra). Les trois angles du bras N sont calculés par `tools/resout_mains.sh` (cible du poing ; coude imposé 32 sous le poing et 26 devant l'épaule ; écartement cherché entre 5 et 25°) ; les valeurs obtenues sont reportées ici après le calcul |
| Épaule F | `armF` 8 (le long du corps, un peu devant), `armF_p` −18, `armF_r` 0 ; omoplate `epauleF_haut` 0, `epauleF_av` −3 (rapprochée : poitrine ouverte) |
| Coude F | `foreF` 25 ; poing serré devant la hanche |
| Tête | `neck` −10 (menton qui monte : extension, la tête recule de 3,5, loin du bras), `neck_r` +8 (compense la torsion) |

### Il serre (197) et tenue (200-264)

197 : poing visé 2 plus haut, `epauleN_haut` +5. Tenue : pose 194 ; respiration 216 et 248
`epaule*_haut` +1, 232 et 264 : 0 ; le poing levé suit l'épaule.

## 5. Ce qui se voit de profil

- 0-60 : la garde qui se défait, le pied qui revient, le corps qui monte et se redresse :
  « c'est fini ».
- 66-129 : la tête qui tourne et descend vers l'avant, à-coup, rebond, deux fois. De profil
  on lit la **flexion** (le disque de la tête descend et avance de 4 d'un coup au
  craquement, 7 en tout depuis le neutre), et le **bras N** qui monte puis tombe avec son
  épaule au crac 1, qui descend au crac 2. L'inclinaison et la rotation, dans la
  profondeur, ne se lisent que de face et de trois quarts.
- 142-162 : les épaules (et les deux bras) qui montent puis reviennent, la poitrine qui sort.
- 170-194 : un bras qui monte devant, coude devant le visage puis au-dessus de l'épaule,
  poing au-dessus du crâne : silhouette lisible. Le coude reste hors du disque de la tête.
  L'autre bras reste le long du corps, devant la hanche.
- Le buste reste droit, la poitrine sort au poing levé.

## 6. Références

- Kawchuk G. N. et al., « Real-Time Visualization of Joint Cavitation », PLOS ONE, 2015
  (mécanisme de la cavitation, montré sur les doigts).
- Reggars J. W., Pollard H. P., « Analysis of zygapophyseal joint cracking during
  chiropractic manipulation », J. Manipulative Physiol. Ther., 1995 (craquement des facettes
  cervicales).
- Tracy J. L., Matsumoto D., « The spontaneous expression of pride and shame: Evidence for
  biologically innate nonverbal displays », PNAS, 2008 (bras levés, tête en arrière, poitrine
  ouverte après la victoire, chez des judokas voyants et aveugles).
- Strength vs Speed (`etudes/01_strength_vs_speed/`) : le « costaud » rouge garde la tête posée
  sur la ligne d'épaules et ses bras se lisent séparés (un devant, un derrière).
- Bible : poses tenues après un geste sec, contraste de vitesse ; mise en scène lisible.
- `analyses/intro_bagarreur.md` : même personnage, même stature, même logique de craquement
  (tension lente, à-coup bref).

## 7. Contrôles

1. Images 0-58 identiques à `sortie_de_garde` (raccord avec la garde, pas levé repris tel
   quel) ; pieds à la clé 60 identiques à ceux de `sortie_de_garde` 60 (aucun glissement).
2. Pieds : aucun glissement de 60 à 264 (mêmes cibles à toutes les clés).
3. Rien ne traverse rien (`--verifier`). En plus, mesuré en 3D sur la pose 194 et la tenue :
   de profil, coude N à au moins 28 du centre de la tête ; centre du poing N à au moins
   23 + 8,5 + 6 = 37,5 du centre de la tête ; de face, poing décalé d'au moins 15 de l'axe
   de la tête et coude hors du disque.
4. `epaule*_av` ≤ 0 à toutes les clés ; poitrine ≤ 2.
5. Craquements : tension en 18 images ; à-coup en 3 images avec un déplacement de profil du
   centre de la tête d'au moins 4 (mesuré entre 84 et 87, et 122 et 125) ; rebond de 4
   images ; deux craquements, un de chaque côté.
6. Poing levé (194) : centre du poing au moins 8 au-dessus du sommet du crâne ; avant-bras
   entre 75 et 105° par rapport au sol de profil ; coude devant l'épaule et au-dessus d'elle.
7. Tenue 200-264 : rien ne bouge de plus de 1,5 à part la respiration.
8. Trois vues : de face le poing levé est sur le côté N de la tête (contrôle 3) ; de trois
   quarts le coude ne passe pas derrière la tête.
