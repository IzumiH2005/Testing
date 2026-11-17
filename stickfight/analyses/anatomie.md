# Anatomie du squelette : ce que chaque articulation peut faire, en 3D

Référence pour poser n'importe quel mouvement. Pour chaque articulation : ses degrés de liberté
réels, leurs amplitudes, les couplages (une articulation qui en entraîne une autre), ce qui se
voit de profil, et le canal du squelette qui la commande. Valeurs pour un adulte (AAOS et tables
cliniques, voir les sources) ; un combattant force un peu au-delà.

Repère : le personnage regarde vers +x (l'avant), y vers le haut, la profondeur vers la caméra
ou à l'opposé. « Côté caméra » = côté proche (N), « côté opposé » = côté loin (F).

## 1. Ce qu'on avait mal compris

Un membre n'a pas deux directions indépendantes (« avant-arrière » et « sur le côté »). L'épaule
et la hanche sont des **rotules** : le bras peut pointer dans n'importe quelle direction d'une
**zone** de l'espace (un cône déformé), et en plus tourner sur lui-même. Les limites ne sont pas
« ±90° sur chaque axe » : elles dépendent de la direction. Par exemple, le bras peut aller loin
derrière quand il est écarté sur le côté, mais presque pas quand il est le long du corps ; il peut
croiser devant le buste, pas derrière le dos.

Le coude et le genou sont des **charnières** : un seul plan de pliage. Ce plan, c'est la rotation
du segment au-dessus (l'humérus, le fémur) qui le choisit : c'est pour ça qu'on peut avoir le
coude vers le bas, vers l'extérieur ou vers l'arrière avec le même pliage.

## 2. Le tronc

| Articulation | Mouvement | Amplitude | Canal |
|---|---|---|---|
| Colonne lombaire + thoracique | flexion (se pencher en avant) / extension | 80° / 30° au total, répartis sur les deux os | `spineLow`, `chest` |
| | inclinaison sur le côté | 35° de chaque côté au total | `spineLow_p`, `chest_p` |
| | rotation (torsion) | 45° de chaque côté ; le squelette la répartit 20 % dans le bas du dos, 80 % dans le thorax | `torsion` (limité à ±45°) |
| Bassin (sur les hanches) | bascule avant / arrière, inclinaison, rotation | rotation 60° au plus, pieds posés | `root`, `root_p`, `torsionBassin` (±60°) |
| Cou | flexion / extension | 50° / 60° | `neck` |
| | inclinaison / rotation | 45° / 80° (la rotation ne se voit presque pas : tête ronde) | `neck_p`, `neck_r` |

Couplages : quand on tourne les épaules, le bassin suit d'environ la moitié (ou résiste, et
c'est le ressort d'un coup). Le regard reste sur la cible : le cou compense la torsion.

## 3. La ceinture scapulaire (omoplate et clavicule)

L'épaule n'est pas fixée au thorax : l'omoplate glisse. C'est elle qui donne de l'allonge à un
coup de poing et qui permet de hausser les épaules.

| Mouvement | Amplitude (déplacement de l'épaule) | Canal |
|---|---|---|
| Protraction (l'épaule avance) / rétraction (elle recule) | environ ±7 unités (≈ 7 cm) | `epauleN_av`, `epauleF_av` |
| Élévation (hausser) / abaissement | +7 / −3 unités | `epauleN_haut`, `epauleF_haut` |

Rythme scapulo-huméral : au-delà de 90° d'élévation du bras, l'omoplate tourne et monte avec lui
(environ 1° d'omoplate pour 2° de bras) : un bras levé au-dessus de la tête hausse l'épaule.

## 4. L'épaule (rotule) et le bras

Direction du bras (cône) :

| Mouvement | Amplitude |
|---|---|
| Flexion (bras devant, jusqu'à la verticale) | 180° |
| Extension (bras derrière, le long du corps) | 60° |
| Abduction (bras sur le côté, jusqu'à la verticale) | 180° (avec l'omoplate) |
| Adduction horizontale (bras qui croise devant le buste, à hauteur d'épaule) | 45 à 50° au-delà de l'avant |
| Abduction horizontale (bras qui part derrière, à hauteur d'épaule) | 30 à 45° au-delà du côté |
| Le bras ne passe jamais derrière le dos de l'autre côté | — |

Rotation sur son axe (avec le bras écarté à 90°) : 70° interne, 90° externe ; elle oriente le
coude. Canaux : `armN` (dans le plan), `armN_p` (vers la caméra = écarté pour le bras proche),
`armN_r` (rotation sur l'axe). Le squelette vérifie la direction du bras dans le cône ci-dessus
(`StickRig.amplitudes`), pas chaque canal séparément.

### 4 bis. Décrire l'épaule à l'instant T

Pour chaque pose clé, on écrit l'épaule avec **tous** ses axes, sinon la pose est bancale et la
profondeur fausse :

| Axe | Question | Canal |
|---|---|---|
| Élévation | à quelle hauteur est le coude (le long du corps, épaule, au-dessus) ? | `armN` et `armN_p` ensemble |
| Plan d'élévation | le bras est-il devant, sur le côté, ou sur le côté **et en arrière** (abduction horizontale) ? | rapport entre `armN` (avant-arrière) et `armN_p` (côté) |
| Rotation sur l'axe | où pointe l'avant-bras quand le coude plie (vers l'avant, le haut, le bas) ? | `armN_r` |
| Omoplate | l'épaule est-elle tirée en arrière, poussée en avant, haussée ? | `epauleN_av`, `epauleN_haut` |
| Coude | combien est-il plié ? | `foreN` |
| Écartement de l'épaule | le bras est-il décollé du buste sur le côté ? Jamais collé : 12° bras ballants (repos), 18 à 24° bras qui s'écartent, gardes : coudes décollés (ouverte : 24° devant, 20° derrière ; fermée : 18° et 16°), avant-bras ramenés vers le centre par la rotation | `armN_p` (+), `armF_p` (−), puis `armN_r` / `armF_r` |

Exemples vus sur un mannequin articulé (PoseIt) :

- **Bras sur le côté, avant-bras vers l'avant** : élévation à l'horizontale, plan sur le côté,
  rotation qui envoie l'avant-bras vers l'avant, coude à 90°. De profil : le bras disparaît
  (il pointe vers la caméra), l'avant-bras se voit en entier vers l'avant.
- **Armé d'un coup de poing** : le même bras, mais le plan part **en arrière** du côté (abduction
  horizontale 30 à 50° derrière), le coude un peu plus haut, l'omoplate tirée en arrière, le coude
  plus plié (110 à 130°). De profil : le coude dépasse derrière l'épaule, l'avant-bras revient vers
  l'avant, le poing près de la poitrine ou du menton.
- **Départ du direct** : l'omoplate revient en avant, le plan du bras passe de « côté et arrière »
  à « devant » (adduction horizontale), et **en même temps** le coude se déplie jusqu'au contact.
- **Crochet** : le buste tourne beaucoup plus, l'épaule avance encore plus (omoplate en avant), le
  plan du bras reste sur le côté et balaie vers l'avant, mais le coude **reste plié** (90° environ).

## 5. Le coude et l'avant-bras

| Mouvement | Amplitude | Canal |
|---|---|---|
| Flexion (charnière) | 0 à 150° | `foreN` |
| Hyperextension | 0 (5° au plus, pas chez nous) | — |
| Pronation / supination (rotation de l'avant-bras) | 80° / 80° | aucun : elle ne se voit pas sur un poing rond |
| Pliage de côté | **impossible** | — |

## 6. La hanche (rotule) et la jambe

| Mouvement | Amplitude |
|---|---|
| Flexion (genou vers la poitrine) | 120° genou plié, 90° jambe tendue |
| Extension (jambe derrière) | 20 à 30° |
| Abduction (jambe sur le côté) | 45° |
| Adduction (jambe qui croise devant l'autre) | 30° |
| Rotation interne / externe | 40° / 50° (oriente le genou et le pied) |

Canaux : `thighN`, `thighN_p`, `thighN_r`.

### 6 bis. Décrire la jambe à l'instant T

| Axe | Question | Canal |
|---|---|---|
| Flexion de hanche | la cuisse est-elle devant (genou levé), sous le bassin, derrière ? | `thighN` |
| Écartement | le pied est-il dans l'axe, écarté sur le côté, croisé devant l'autre ? (largeur de la garde) | `thighN_p` |
| Rotation de hanche | où pointent le genou et le pied : droit devant, vers l'extérieur, vers l'intérieur ? | `thighN_r` |
| Genou | combien est-il plié ? il pointe toujours dans la direction du pied | `shinN` |
| Cheville | talon posé ou levé (sur la plante) ? pied qui roule sur le côté ? | `footN` (automatique), `footN_p` |
| Bassin | penché d'un côté (hanche qui tombe), tourné ? | `root_p`, `torsionBassin` |
| Appui | quelle jambe porte le poids ? (genou plus plié, bassin au-dessus) | position du bassin |

**Écartement des jambes sur les côtés.** Les pieds ne sont jamais l'un derrière l'autre sur une
même ligne : vu de face, il y a un espace entre eux (un vrai bassin a deux hanches écartées). Les
jambes partent d'un seul point (apparence du personnage), donc cet écartement se règle dans chaque
pose par `thighN_p` (+) / `thighF_p` (−) : 5° pieds joints (garde-à-vous), 9° debout détendu
(repos), 13° et plus base large et ancrée, 16° gardes. Le pied qui passe en marchant ne croise pas
la ligne du milieu. Contrôle : vue de face (`--vues`).

Couplages à respecter :

- **Le genou suit le pied.** La rotation de hanche oriente les deux à la fois : un genou qui
  rentre pendant que le pied reste tourné vers l'extérieur abîme le genou, et ça se voit.
- **Garde de combat** : pieds écartés en largeur (pas sur une ligne), pied arrière tourné vers
  l'extérieur (rotation externe 30 à 45°), pied avant presque droit vers la cible.
- **Pivot du pied arrière** dans un coup : quand le bassin tourne vers la cible, le talon arrière
  se lève et part vers l'extérieur, la hanche arrière passe en rotation interne (le genou rentre
  vers l'avant), la jambe se tend : c'est la poussée.
- **Jambe d'appui** : genou plié au-dessus du pied, bassin au-dessus de l'appui.
- De profil, la rotation se lit par la longueur du pied (un pied tourné vers la caméra paraît
  court) et par la direction du genou.

## 7. Le genou, la cheville

| Articulation | Mouvement | Amplitude | Canal |
|---|---|---|---|
| Genou | flexion (charnière) | 0 à 150° | `shinN` |
| | rotation quand il est plié | 30° environ, invisible de profil | aucun |
| Cheville | flexion dorsale / plantaire | 20° / 50° | `footN` |
| | inversion / éversion (pied qui roule sur le côté) | 25° / 15° | `footN_p` |

## 8. Ce qui se voit de profil, et donc ce qu'il faut régler

- **Visible** : flexion de tout, raccourci des bras et des jambes quand ils s'écartent ou
  croisent (épaule, hanche), protraction et élévation de l'épaule (le point d'attache bouge un
  peu), inclinaison du buste (le buste raccourcit).
- **Invisible mais logique** : rotation du bras et de la cuisse (elle choisit le plan du coude et
  du genou, donc elle compte dès que le coude ou le genou plie), torsion du buste (elle se voit
  par les bras), pronation.

## Sources

- [WikEM, amplitudes articulaires](https://wikem.org/wiki/Joint_ROM_(Table))
- [Physiotutors, amplitudes passives de l'épaule](https://www.physiotutors.com/wiki/shoulder-passive-range-of-motion/)
- [ABMP, rythme scapulo-huméral](https://www-b.abmp.com/massage-and-bodywork-magazine/issues/marchapril-2021/scapulohumeral-rhythm)
- [Table d'amplitudes de l'épaule chez l'adulte sain (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC3785041/table/T2)
- [Valeurs normales d'amplitude (SNCC)](https://www.sncc.ca/resources/Documents/Dragon%20Boat/2024%20CCWCs/range%20of%20motion%20normal%20values.pdf)
- `RECHERCHE.md` (§ 2) pour les amplitudes déjà utilisées dans le plan.
