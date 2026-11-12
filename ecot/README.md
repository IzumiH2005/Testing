# Écot

Un composant unique, pas une page : il sert à partager une addition entre 2 et 6 personnes.
Une seule barre représente le total. On glisse les séparations entre les parts, et la somme reste exacte au centime près.
Même méthode que `marge-v2/` : on pose d'abord la direction et les couleurs, puis on conçoit le composant seul, avec des itérations.

## Fichiers

- `index.html` : le composant vivant, suivi de sa planche. On y trouve :
  - la direction riso et les encres, avec leurs contrastes mesurés ;
  - la typographie, avec les polices écartées et la raison de chaque rejet ;
  - ce qui vient de Material 3 ;
  - le journal d'itérations, avec les captures des pistes A, B et C.

## Direction

- **Impression riso** : papier blanc net, six encres fluo en aplat (rose, bleu, jaune, vert, violet, orange).
- **Contour** : chaque forme a un contour encre de 2 px. Il garantit au moins 3:1 contre le papier, même pour le jaune.
- **Effets** : trame de points dans les parts, décalage de calage rose derrière les gros chiffres.
- **Mode sombre** : les encres ne changent pas. Le papier et le trait s'inversent.

## Typographie

- **Bagel Fat One** : marque et total.
- **Recursive** :
  - `MONO 1` pour les montants, afin que les centimes restent alignés ;
  - `MONO 0` avec `CASL 0.4` pour le texte.
- **Material Symbols Rounded** (graisse 500) : icônes.

## Tiré de Material 3

- **Poignée** : la barre du slider Expressive, 4 dp avec 6 dp de vide de chaque côté. Elle s'amincit à 2 dp quand on la tient.
- **Piste** : 56 dp.
- **Indicateur de valeur** : bicolore, il montre les deux personnes concernées.
- **Saut** : un appui sur la piste déplace la séparation la plus proche.
- **États** : couches d'état à 0,08 et 0,10.
- **Cibles** : 48 dp.
- **Accessibilité** : chaque séparation est un `role=slider` avec un `aria-valuetext` qui lit les deux montants.

## Clavier

- Flèches : 0,10 €.
- `Maj` + flèche ou `Page↑` / `Page↓` : 1 €.
- `Début` / `Fin` : borne voisine.

Les calculs se font en centimes entiers. Les centimes restants d'une division égale vont aux premiers de la liste. Les changements de total sont répartis au prorata, par la méthode du plus fort reste.

Ouvrir `index.html` dans un navigateur suffit, il n'y a ni installation ni build.
