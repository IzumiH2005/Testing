# Héros, famille F1 : manifeste des bandes

Toutes les bandes ont la même forme : une seule rangée horizontale d'images de **32×32**. Le **pivot (16,27)** est sous les pieds. Le héros regarde vers la **DROITE** ; le moteur retourne le sprite quand il va à gauche.

Les sources texte sont dans `art/src/hero/<nom>.txt`, générées par `assemble.py` à partir de `art/src/hero/frames/<nom>.frames`. Les contrôles (@8, planches, pelures d'oignon, GIF, mises en situation) sont dans `art/out/hero/`.

Pour les poses accrochées, le **mur est à GAUCHE** :
- la surface du mur est en **x = 10** de la cellule (les pixels de mur vont jusqu'à x ≤ 9) ;
- la main et la cape débordent dans le mur jusqu'à **x = 7**.

**Hitbox létale conseillée** : 6×10 px, de x 13 à 18 et de y 15 à 24. Elle est centrée sur le corps, 1 px plus bas que le centre, ce qui donne un décalage de (−3, −12) depuis le pivot pour le coin haut-gauche. Elle est valable pour toutes les poses, sauf death et respawn, où il n'y a pas de collision.

| Fichier | Images | Durées (ms) / fps conseillés | Boucle | Pivot | x du mur | État du jeu |
|---|---|---|---|---|---|---|
| player_cling.png | 4 (128×32) | 700 · 220 · 300 · 220 | oui | (16,27) | 10 (main x7-9) | accroché immobile au mur |
| player_slide.png | 4 (128×32) | 90 ×4 (≈11 fps) | oui | (16,27) | 10 (main x7-9 en 1 et 3, x8-9 en 2 et 4) | glissade le long du mur |
| player_jump.png | 3 (96×32) | 50 · 70 · tenue | non (la dernière image est tenue) | (16,27) | voir note 1 | saut mural, phase montante |
| player_apex.png | 2 (64×32) | 100 · tenue | non (la dernière image est tenue) | (16,27) | n/a | sommet du saut (vitesse verticale ≈ 0) |
| player_fall.png | 2 (64×32) | 100 · 100 (10 fps) | oui | (16,27) | n/a | chute |
| player_turn.png | 4 (128×32) | 40 · 33 · 50 · 60 | non | (16,27) | n/a | demi-tour en l'air (voir note 2) |
| player_land.png | 3 (96×32) | 60 (+50 d'arrêt sur image côté moteur) · 70 · 90 | non, enchaîne sur cling | (16,27) | 10 (main x7-9) | réception contre le mur |
| player_death.png | 8 (256×32) | 33 · 100 · 60 · 60 · 80 · 80 · 100 · 120 | non (vide après la dernière image) | (16,27) | n/a | mort (contact danger) |
| player_respawn.png | 6 (192×32) | 60 · 60 · 50 · 50 · 70 · 120 | non, enchaîne sur cling | (16,27) | 10 (dernière image = cling 1) | réapparition à l'autel, contre le mur |

## Notes

1. **jump** : l'image 1 est encore tournée vers le mur, avec les jambes vers le bas et la gauche. Elle n'a pas de contact strict, mais le pied le plus à gauche est en x = 6.
2. **turn** :
   - la bande est dessinée de façon à **finir tournée vers la droite** : l'image 1 regarde encore vers la gauche, c'est l'image 2 de jump en miroir.
   - Le moteur applique **dès l'image 1** le retournement de la NOUVELLE direction : pour un demi-tour vers la gauche, toute la bande est affichée en miroir.
   - L'étincelle G du demi-tour relève de F4 et n'est pas dans cette bande.
3. **death** :
   - l'image 1 est un flash blanc W avec contour k ;
   - l'image 2 a un contour extérieur magenta z ;
   - les images 4 à 6 utilisent les couleurs d'écho e, c, t et q : le cyan monte, et 6 pixels corail tombent ;
   - l'image 8 se réduit à 1 px ;
   - après l'image 8, ne plus rien afficher.
4. **respawn** : les images 1 et 2 ne contiennent que des particules ; il n'y a pas de collision avant l'image 6.
5. **Bandes `_scarf` séparées** : non livrées en v1. L'écharpe est intégrée à chaque bande principale.

## Couleurs (palette v2)

- **Héros** : k b w h H i I o a R r, soit 11 couleurs.
- **Poussière de glissade** : p l.
- **Mort et réapparition** : W, z (image 2 de death seulement), e c t q.
- Aucun blanc sale, aucun marron.
