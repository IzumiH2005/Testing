# test18 — mannequin 3D comme base de dessin

Essai : poser un mannequin 3D articulé, le rendre de profil, puis dessiner le sprite
par-dessus **trait par trait** (un appel d'outil = un geste), comme un dessinateur sur PoseIt.

- `outils/poser.py` : rendu Cycles orthographique de profil (membres proches orange, loin bleus)
  + articulations projetées en pixels. Usage : `python3 -I outils/poser.py <action> <frame> <prefixe>`.
- `outils/trait.py` : ligne, px, rang, remplir, gomme, coller, annuler, voir.
- `frames/idle_01` : frame idle terminée. `frames/course_01` : course, en cours (arrêtée).
- Le modèle n'est pas versionné (13 Mo) : le placer dans `modele/`.

Modèle : *Mannequiny* 0.4.0, par Luciano Muñoz, publié par GDQuest, licence CC-BY 4.0 —
https://opengameart.org/node/184427

Bilan : l'idle est lisible ; la course reste raide (jambe proche en bande diagonale,
pas de genou ni de volume). Essai interrompu.
