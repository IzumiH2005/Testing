# Études de vidéos de référence

Chaque dossier contient l'analyse image par image d'une vidéo d'animation de stickman.
Les règles qu'on en tire sont rassemblées dans `../BIBLE_ANIMATION.md` ; ici se trouve le
détail qui les justifie.

| Dossier | Vidéo | Contenu |
|---|---|---|
| `01_strength_vs_speed/` | « Strength vs Speed » (Stick Nodes), 24 i/s, 494 images | 5 rapports, mesures par image, 10 planches zoomées |

Dans chaque dossier :

- `NN_*.md` : un rapport par portion de la vidéo (journal image par image, découpage en
  phases, espacement, mécanique du corps, effets, rythme, leçons).
- `mesures.csv` : par image, la hauteur de la ligne de sol (282 au repos, tout écart est une
  secousse de caméra) et, pour chaque personnage, son centre et sa boîte englobante.
- `planches/` : quelques planches zoomées des moments clés.

**Attention aux unités dans les rapports de la vidéo 1.** Les rapports 02, 04 et 05 comptent
en « têtes » de 14 px, ce qui est faux : la tête mesure 27 px et le personnage 120 px.
Leurs distances en pixels sont justes ; leurs distances en têtes sont à diviser par deux.
La bible a tout converti en fraction de la hauteur du personnage (H).

La vidéo elle-même n'est pas dans le dépôt.
