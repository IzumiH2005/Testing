# Marge

Carnet de lecture : une étagère de livres, la page où l'on en est, des sessions chronométrées, des citations notées « dans la marge » et un calendrier d'encre des jours de lecture.

- `composants.html` : la planche des composants, conçus un par un avant l'intégration (direction, specs, démos avec états).
- `index.html` : le site intégré et fonctionnel (données dans le navigateur, localStorage).

## Couleur 60/30/10

- 60 % blanc propre `#fbfbfc` (surface, neutre très légèrement froid).
- 30 % nuances de blanc et de gris : `#ffffff`, `#f6f6f8`, `#f1f1f3`, `#ebebee`, `#e4e4e8`.
- 10 % bleu cobalt `#3850d3`, l'encre du stylo qui annote le livre (contraste 6,3:1 sur blanc).

Thème sombre généré depuis les mêmes rôles.

## Composants

Conçus pour le site (inspirés de la mécanique Material : rôles de couleur, state layers, cibles 48, focus visible) :
01 Bouton encre · 02 Tranche (livre sur l'étagère) · 03 Signet (progression) · 04 Compteur de page · 05 Minuteur de session · 06 Traits (note) · 07 Citation · 08 Calendrier d'encre · 09 Index (navigation en table des matières).

Repris de Material et seulement restylés : champ de texte outlined, onglets de filtre, dialog, snackbar.

Typographie : Newsreader (contenu des livres, chiffres) et Instrument Sans (interface).
