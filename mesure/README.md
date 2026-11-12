# Mesure

Carnet de travail pour pianiste : un métronome, les passages à monter en tempo et une semaine de pratique.
Même méthode que `marge-v2/`, appliquée à un autre sujet. On pose d'abord la marque et les couleurs (blanc propre, vermillon #aa361e, bleu canard #276674).
Ensuite, chaque composant unique est conçu seul, avec plusieurs itérations avant validation.

## Fichiers

- `index.html` : l'application. C'est un seul fichier et les données restent dans le navigateur (localStorage `mesure`).
- `composants.html` : la planche du système. On y trouve :
  - la direction, la couleur et ses contrastes mesurés ;
  - la typographie, avec les polices écartées et la raison de chaque rejet ;
  - le journal d'itérations des 9 composants ;
  - les composants Material restylés.

## Typographie

- **Bodoni Moda** (axe optique 6–96) : marque, titres, indications de tempo.
- **Atkinson Hyperlegible Next** : interface, chiffres, libellés. Les chiffres doivent rester lisibles de loin, depuis le banc.
- **Material Symbols Rounded** : icônes.

## Composants uniques

1. Marque
2. Bouton Lancer
3. Pulsation
4. Cadran de tempo
5. Échelle (progression en tempo)
6. Carte de passage
7. Pupitre
8. Régularité (semaine)
9. Navigation

## Clavier

- `Espace` : lancer ou arrêter le métronome.
- `+` et `-` : changer le tempo.
- `T` : taper le tempo.
- Règle de tempo : flèches, `Page↑` / `Page↓`, `Début` / `Fin`.

Ouvrir `index.html` dans un navigateur suffit, il n'y a ni installation ni build.
