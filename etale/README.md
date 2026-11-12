# Étale

Landing page mobile d'abord pour une app de nage en mer : elle dit à quelle heure la mer se calme (l'étale) sur votre plage. La page sert de liste d'attente pour la bêta.
La méthode est celle de `marge-v2/` et `mesure/`. On pose d'abord la marque et les couleurs : blanc froid, marine #183d62, eau aqua #a7e8ea et orange bouée #ff6f36.
Ensuite, chaque composant unique est conçu seul, avec plusieurs itérations avant validation.

## Fichiers

- `index.html` : la landing page. C'est un seul fichier, sans dépendance hors Google Fonts.
- `composants.html` : la planche du système. On y trouve :
  - la direction en six décisions ;
  - la couleur et ses contrastes mesurés en clair et en sombre ;
  - la typographie, avec les polices écartées et la raison de chaque rejet ;
  - le journal d'itérations des 9 composants, avec les planches de travail ;
  - les composants Material restylés.

## Typographie

- **Anybody** (axe de largeur 50–150) :
  - étirée à 150 % en graisse 300 pour la marque et les titres, c'est la mer étale ;
  - serrée à 56 % pour les heures, les mesures et les mots d'accent.
- **Sofia Sans** : texte et interface.
- **Material Symbols Outlined** (graisse 300) : icônes.

## Composants uniques

1. Marque, avec l'accent couché du É.
2. Bouton bouée.
3. Titre à deux largeurs.
4. Carte du jour.
5. Courbe de marée, un slider.
6. Règle du froid : une minute par degré.
7. Signaux.
8. Tarif, présenté comme un annuaire des marées.
9. Inscription et dock mobile.

## Clavier

- Courbe de marée :
  - flèches : ±5 min ;
  - `Page↑` / `Page↓` : ±1 h ;
  - `Début` / `Fin`.
- Règle du froid : flèches.
- Carrousel des témoignages : boutons précédent et suivant, ou défilement au clavier.

Ouvrir `index.html` dans un navigateur suffit, il n'y a ni installation ni build.
