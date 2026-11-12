# Crête

Un slider qui marche sur le sentier. Au lieu d'une droite, la piste suit le profil de dénivelé d'une randonnée fictive, la Boucle de l'Ourse (24 km). On glisse le long de la crête, et chaque point répond : altitude, pente, D+ restant, heure de passage.

## Fichiers

- `index.html` : la planche complète et autonome. Elle contient le composant en état de marche, l'idée, la direction, la typographie, ce qui vient de Material, le mouvement, le clavier et les itérations, avec les images de travail intégrées.

## Direction

La carte topo, pas le tableau de bord. Trois palettes ont été comparées (balisage, aube, topo) et la topo a gagné :

- bleu balise `#1F5CFF` pour la partie parcourue, rayée de courbes de niveau tous les 100 m ;
- `#EEF2FF` pour la partie à venir ;
- losange jaune `#FFD21A` pour la poignée, comme une balise ;
- encre marine `#0B1430` sur blanc franc.

Les pentes reprennent le code des pistes de ski : verte en dessous de 10 %, bleue de 10 à 20 %, rouge de 20 à 30 %, noire au-delà. Un ruban sous le profil montre tout le parcours. La couleur n'est jamais seule : une flèche et le pourcentage l'accompagnent, et le lecteur d'écran annonce la piste. La pente affichée est celle des 400 m à venir.

## Typographie

- **Krona One** pour la marque : large comme un horizon, avec un circonflexe qui fait sommet.
- **National Park** pour l'interface : elle est dessinée d'après la signalétique des parcs nationaux, donc faite pour être lue dehors.
- **Material Symbols Sharp 500** pour les icônes.

## Material

Le composant reprend l'anatomie du slider M3 :

- piste active et piste inactive ;
- poignée verticale de 4 px qui s'affine à 2 px quand on la tient ;
- 6 px d'espace autour de la poignée ;
- indicateur de valeur ;
- repères d'arrêt, sur lesquels la poignée s'aimante ;
- state layers ;
- cibles de 48 px ;
- rôle `slider` avec `aria-valuetext`.

La forme, elle, est propre au projet : losanges, coins de 4 à 6 px.

## Mouvement

Tout repose sur des ressorts amortis qu'on peut interrompre. Pendant le glisser, la poignée colle au doigt. La bulle d'altitude suit avec un léger retard et penche dans le sens du mouvement. Sur un arrêt, l'aimant tire la poignée d'un coup sec, le losange gonfle puis se pose, et le téléphone vibre brièvement. Avec « réduire les animations », tout saute directement à la cible.

## Clavier

| Touches | Effet |
|---|---|
| Flèches | 100 m |
| Maj + flèches | 1 km |
| Page ↑ / Page ↓ | arrêt suivant / précédent |
| Début / Fin | départ / arrivée |

Les boutons ‹ › nomment leur destination.

## Vérifié

À 320, 360, 390 et 412 px, en clair et en sombre :

- aucun débordement ;
- aucune erreur ;
- cibles ≥ 48 px ;
- clavier ;
- valeurs ARIA ;
- mouvement réduit.
