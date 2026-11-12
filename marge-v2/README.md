# Marge v2

Carnet de lecture : étagère, compteur de pages, citations et carnet de lecture.
C'est une refonte de `marge/` avec les mêmes couleurs (blanc propre, gris, cobalt #3850d3).
Cette fois, chaque composant unique a été conçu seul, avec plusieurs itérations avant validation.

## Fichiers

- `index.html` : l'application. Un seul fichier, les données restent dans le navigateur (localStorage `marge-v2`).
- `composants.html` : la planche du système. On y trouve :
  - la direction, la couleur et ses contrastes mesurés, la typographie, avec les 13 polices écartées et pourquoi ;
  - le journal d'itérations des 9 composants ;
  - les composants Material restylés.

## Typographie

- **Piazzolla** (axe optique 8–30) : marque, titres, citations.
- **Schibsted Grotesk** : outil, chiffres, libellés.
- **Material Symbols Sharp** : icônes.

## Composants uniques

1. Marque
2. Bouton
3. Couverture générée
4. Étagère
5. Compteur
6. Citation
7. Traits (note)
8. Encre (calendrier)
9. Index (navigation)

Ouvrir `index.html` dans un navigateur suffit, il n'y a ni installation ni build.
