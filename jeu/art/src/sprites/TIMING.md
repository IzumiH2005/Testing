# ÉCHO, lot 1 : feuilles de timing des sprites

Durées en millisecondes, multiples de ~16,7 ms (60 Hz). « tenue » = l'image reste affichée
tant que l'état dure (pas de boucle). Les images sont numérotées de 0, de gauche à droite.

## player.png (5 images 16×16, regard vers la DROITE ; miroir horizontal pour l'autre mur)

Ce ne sont pas une seule boucle mais des états. Intention : un petit grimpeur léger et nerveux,
qui colle au mur puis bondit ; le corps est vif, l'écharpe arrive toujours une image en retard
(chevauchement).

| État du jeu | Images | Rôle | Durée |
|---|---|---|---|
| Accroché, immobile | 0 | clé, tenue | tenue |
| Glisse le long du mur | 1 | clé, tenue (l'écharpe remonte) | tenue ; en entrant dans la glissade, montrer 0 pendant 50 ms puis 1 |
| Saut, vitesse verticale vers le haut | 2 | clé (groupé, anticipation du rebond) | tenue tant que vy < 0 |
| Sommet du saut (option) | 4 | passage (vrille) | 83 ms, une seule fois, quand vy change de signe ; sinon ne pas l'utiliser |
| Rebond inversé (tap en l'air / changement de sens) | 4 | image étirée de vrille | 100 ms, puis 2 ou 3 selon vy |
| Saut, vitesse verticale vers le bas | 3 | clé (étiré) | tenue tant que vy > 0 |
| Arrivée sur un mur | 0 | impact | tenue ; ne pas intercaler d'autre image (le contact doit être sec) |

Rappels pour le code :
- Mur DROIT = image miroir (flipX). Le décalage d'ancrage s'inverse aussi (voir le rapport).
- Images 0 et 1 : ancrage au bord gauche (x = 0 est le contact avec le mur), pieds en y = 15.
- Images 2, 3, 4 : ancrage au centre (8, 8).

## death.png (5 images 16×16)

Intention : le héros s'éteint et se défait en volutes d'écho ; une mort douce, pas gore.
Durée totale ≈ 750 ms. Ne boucle pas : rester sur « rien » ensuite (et poser grave.png).

| Image | Rôle | Ce qui change | Durée |
|---|---|---|---|
| 0 | clé, impact | choc blanc : silhouette du héros en blanc froid `w`/`W` | 100 ms (tenue d'impact) |
| 1 | extrême | éclatement : la silhouette se fend en morceaux cyan | 117 ms |
| 2 | passage | volutes qui montent | 150 ms |
| 3 | intervalle | presque rien : 3 petites volutes | 167 ms |
| 4 | clé finale | 1 pixel `e` qui s'éteint | 217 ms |

## saw.png (2 images 16×16) : boucle

Intention : rotation mécanique continue, nerveuse. Les deux images décalent les dents d'une
demi-dent : en boucle, l'œil lit une rotation.

| Image | Durée |
|---|---|
| 0 | 50 ms |
| 1 | 50 ms |

Boucle 0, 1, 0, 1… (100 ms par tour visuel). Plus lent (67 ms) si la scie est « au repos ».
`saw_echo.png` : immobile, pas d'animation.

## laser.png (3 images 16×16) + beam.png (3 images 8×8)

Cycle de piège décidé par le code (durées conseillées) :

| Phase | laser.png | beam.png | Durée conseillée |
|---|---|---|---|
| Éteint | 0 | (rien) | selon le niveau (ex. 1200 ms) |
| Préavis | 1 | 0 (pointillé fin), répété sur toute la largeur | 600 ms ; faire clignoter beam 0 : 100 ms affiché / 67 ms caché |
| Actif | 2 | 1 et 2 en alternance | 67 ms chacune, en boucle, pendant toute la phase active |

## shard.png (4 images 8×8) : boucle

Rotation de l'éclat d'or. Image 0 = face pleine (tenue plus longue : ralenti sur la face).

| Image | Durée |
|---|---|
| 0 | 200 ms |
| 1 | 100 ms |
| 2 | 100 ms (tranche) |
| 3 | 100 ms |

## shard_pop.png (4 images 8×8) : une fois

Éclat qui monte en escalier puis s'éteint (E2-H). Durée totale 300 ms.

| Image | Durée |
|---|---|
| 0 | 50 ms (point + anneau) |
| 1 | 67 ms (croix, pic) |
| 2 | 83 ms (croix éclatée) |
| 3 | 100 ms (dernières étincelles) |

## tide.png (2 images 16×16) : boucle

Crête de la marée qui ondule. Lent et lourd.

| Image | Durée |
|---|---|
| 0 | 333 ms |
| 1 | 333 ms |

Astuce : décaler l'image de départ d'une tuile sur deux (0,1,0,1… / 1,0,1,0…) pour casser la
répétition.

## tap.png (2 images 16×16) : boucle

| Image | Rôle | Durée |
|---|---|---|
| 0 | doigt levé (tenue) | 450 ms |
| 1 | doigt qui touche (impact + anneau) | 200 ms |

## grave.png, saw_echo.png, spikes.png, spikes_echo.png, laser_echo.png

Images fixes, pas de timing.
