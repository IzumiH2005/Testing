# Buée

Une barre de message en verre givré : on écrit comme avec le doigt sur une vitre embuée de bus, avec les lumières de la ville floues derrière. Chaque mouvement suit les douze principes d'animation de *The Illusion of Life* (Frank Thomas et Ollie Johnston).

## Fichiers

- `index.html` : la planche complète, autonome. Elle contient le composant, la direction, la typographie, les douze principes, ce qui vient de Material et les itérations, avec les images intégrées.

## Direction

Le verre est construit en couches :

- teinte à 58 % en clair et 60 % en sombre ;
- flou de 28 px avec une saturation de 1,6 ;
- grain SVG ;
- arête haute claire ;
- ombre interne basse ;
- ombre portée teintée.

Derrière, de grandes taches de couleur se mêlent à des ronds nets façon bokeh. Ce sont ces bords nets qui rendent le flou du verre lisible. Le fond reprend les couleurs d'une aube en clair (rose, bleu, menthe, jaune, lilas) et celles d'une ville de nuit en sombre.

Les contrastes ont été mesurés sur les pixels réellement rendus, en gardant le pire pixel au 2<sup>e</sup> centile : tous sont ≥ 5,3:1.

## Typographie

- **Edu SA Hand 700** pour la marque : un tracé régulier et penché, comme une trace de doigt. Elle est remplie avec le dégradé de la scène.
- **Parkinsans** pour l'interface : une grotesque ronde et douce, lisible sur un fond qui bouge.
- **Material Symbols Rounded 500** pour les icônes.

## Mouvement : les 12 principes

Le moteur est un vrai ressort (raideur, amortissement) qu'on peut interrompre : il garde sa vitesse quand la cible change.

1. **Écrasement et étirement** : le bouton s'écrase à l'appui. La bulle s'étire en vol et s'écrase à l'arrivée, à volume constant.
2. **Anticipation** : la barre plonge de 4 px et le bouton recule pendant 110 ms avant l'envoi.
3. **Mise en scène** : au focus, la scène se désature et le fil s'efface.
4. **Tout droit et pose à pose** : l'envoi est construit pose à pose. La dérive des lumières est calculée tout droit.
5. **Continuité et chevauchement** : le disque arrive avant l'icône. Les puces partent à 45 ms d'écart. Le champ dépasse sa taille puis se pose.
6. **Ralenti en entrée et en sortie** : il n'y a aucune interpolation linéaire.
7. **Arcs** : la bulle vole en courbe. Les icônes tournent autour du centre du bouton.
8. **Action secondaire** : un reflet essuie la barre. L'anneau du compteur se remplit.
9. **Timing** : les icônes sont légères (environ 160 ms) et la barre est lourde (environ 420 ms).
10. **Exagération** : un message trop long fait trembler le panneau d'environ 25 px.
11. **Dessin solide** : le verre a une épaisseur.
12. **Attrait** : pilules, typographie ronde, bulles qui pointent vers leur auteur.

Avec `prefers-reduced-motion`, les ressorts sautent à leur valeur finale, la scène s'arrête, les bulles apparaissent en simple fondu et l'erreur est annoncée au lieu de trembler.

## Tiré de Material 3

- **Champ** : anatomie du text field (56 dp, indicateur de 1 dp qui passe à 2 dp), avec un `<label>` visible.
- **Texte d'aide et compteur** : reliés par `aria-describedby`. Le compteur n'apparaît qu'à 70 % de la limite de 280 caractères.
- **Erreur** : le texte d'aide est remplacé par l'erreur avec une icône, le champ porte `aria-invalid` et une région live l'annonce.
- **Icône de fin** : elle change selon l'état (dictée sans texte, envoi avec texte).
- **Puces d'assistance** : 40 dp dans une cible de 48.
- **États** : couches d'état à 0,08 et 0,12, focus visible au clavier.
- **Motion** : on sépare le spatial et les effets. Seuls la position et l'échelle rebondissent.

## Clavier

- `Entrée` envoie ; `Maj` + `Entrée` ajoute une nouvelle ligne.
- `Entrée` ou `Espace` sur « + » ouvre le plateau, avec le focus sur la première puce.
- `← →` (ou `↑ ↓`) passent d'une puce à l'autre.
- `Échap` ferme le plateau et rend le focus au « + ».

Ouvrir `index.html` dans un navigateur : aucune installation n'est nécessaire.
