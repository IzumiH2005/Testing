# Études de vidéos de référence

Chaque dossier contient l'analyse image par image d'une vidéo d'animation de stickman.
Les règles qu'on en tire sont rassemblées dans `../BIBLE_ANIMATION.md` ; ici se trouve le
détail qui les justifie.

| Dossier | Vidéo | Contenu |
|---|---|---|
| `01_strength_vs_speed/` | « Strength vs Speed » (Stick Nodes), 24 i/s, 494 images | 5 rapports, mesures par image, 10 planches zoomées |
| `03_strength_vs_speed_round_2/` | « Strength vs Speed, Round 2 » (Stick Nodes), 24 i/s, 6 779 images | rapport sur la profondeur, 5 planches |
| `02_rai_zen_armagon/` | « Rai and Zen vs Armagon » (Rai Lukasha, Stick Nodes), 24 i/s, 3 713 images | 6 rapports, 13 planches zoomées |

Dans chaque dossier :

- `NN_*.md` : un rapport par portion de la vidéo (journal image par image, découpage en
  phases, espacement, mécanique du corps, effets, rythme, leçons).
- `mesures.csv` (vidéo 1 seulement) : par image, la hauteur de la ligne de sol (282 au repos, tout écart est une
  secousse de caméra) et, pour chaque personnage, son centre et sa boîte englobante.
- `planches/` : quelques planches zoomées des moments clés.

**Attention aux unités dans les rapports de la vidéo 1.** Les rapports 02, 04 et 05 comptent
en « têtes » de 14 px, ce qui est faux : la tête mesure 27 px et le personnage 120 px.
Leurs distances en pixels sont justes ; leurs distances en têtes sont à diviser par deux.
La bible a tout converti en fraction de la hauteur du personnage (H).

Dans les rapports de la vidéo 2, H varie d'un plan à l'autre (de 97 à 150 px selon le zoom) ;
chaque rapport dit quelle valeur il a prise. Les rapports de la vidéo 2 disent, règle par règle,
ce qu'elle confirme, nuance ou contredit dans la bible (section 9 de chaque rapport).

Les vidéos elles-mêmes ne sont pas dans le dépôt.
