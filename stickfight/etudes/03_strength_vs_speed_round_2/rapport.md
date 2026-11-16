# Étude : « Strength vs Speed, Round 2 » (Stick Nodes)

Vidéo de 4 min 42 s à 24 i/s (6 779 images), même animateur et mêmes personnages que la vidéo 1.
Étude faite sans agents : survol de toute la vidéo (une image sur douze), puis planches image par
image des passages qui montrent la profondeur (`planches/`). Les numéros sont ceux de la vidéo,
comptés à partir de 0.

## Ce qui est nouveau par rapport à la vidéo 1

La caméra bouge beaucoup plus (gros plans, plans inclinés, travellings), et surtout les corps
tournent : on voit des poses de trois quarts et de face, des membres qui passent derrière l'autre
personnage, des genoux levés vers la caméra. Les gros plans sont de la mise en scène (un poing ou
une tête qui remplit l'écran) et ne nous concernent pas ; tout le reste se traduit avec notre
squelette en 3D.

## 1. La profondeur se voit par le raccourci, jamais par un écart à l'écran

- **Directs du bleu, 1490-1496.** Entre deux coups, les deux poings sont devant le visage, coudes
  pliés et écartés du buste, et les deux avant-bras ont des longueurs différentes : l'un vient vers
  la caméra, l'autre part derrière. Au contact (1492, 1495), le bras de frappe est tendu à
  l'horizontale, pleine longueur, et le bras libre est replié contre le visage, son coude dépasse
  devant le buste. Les épaules ne s'écartent jamais : tout part d'un seul point.
- **Genou levé vers la caméra, 4006-4010 et 5992-6008.** Le bleu, tourné de trois quarts, monte le
  genou : la cuisse paraît très courte (elle pointe vers nous), puis la jambe se déplie de côté en
  reprenant toute sa longueur. Le raccourci dit « vers nous » sans aucune perspective.
- **Corps de trois quarts (5988-6010).** Les deux jambes sont écartées en A et les deux bras
  dépassent de part et d'autre du buste : on lit un corps tourné, pas un profil.

## 2. L'ordre de dessin raconte qui est devant

- **Bras qui passe derrière l'adversaire, 1959-1963.** Le crochet du rouge passe derrière la tête
  du bleu (traînée en arc qui s'enroule), puis son bras passe devant le buste du bleu pendant la
  saisie : les deux corps s'entremêlent. Un seul membre change de couche à la fois.
- **Crochets au corps à corps, 1500-1511.** Le bras qui frappe passe devant ou derrière le corps
  adverse selon le côté qui frappe ; l'éclat d'impact est toujours dessiné devant tout.
- Chez un même personnage, le bras du fond reste derrière le buste sauf quand il frappe : il passe
  alors devant, sur l'image du contact.

## 3. Le reste confirme la bible

- Contact en une image, traînée d'une image, bras libre replié, corps qui avance au contact.
- Coups de pied (3994-3998) : jambe de frappe horizontale, jambe d'appui verticale, bras ouverts en
  contrepoids, buste penché à l'opposé.
- Aucune largeur d'épaule ni de hanche, membres d'un seul trait.

## 4. Traduction pour notre squelette

| Ce que fait l'animateur | Canal |
|---|---|
| Buste qui tourne à l'armé et au contact | `torsion` 20 à 30° (pas plus : au-delà, les bras tournent avec le buste et se raccourcissent) |
| Bassin qui suit en retard | `torsionBassin` environ la moitié de `torsion` |
| Bras libre qui vient devant pendant que le buste tourne | profondeur du bras (`armF_p`) dans le sens opposé à la torsion, pour qu'il reste lisible |
| Genou levé vers la caméra | `thighN_p` 40 à 60° sur l'image du genou levé, 0 quand la jambe se déplie |
| Corps de trois quarts | `lacet` 30 à 50°, jamais 90° sur une pose clé (le corps se réduit à un trait) |
| Bras qui passe derrière la tête ou l'adversaire | profondeur négative sur une ou deux images seulement |
