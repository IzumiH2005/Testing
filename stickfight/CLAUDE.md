# Règles du projet stickfight

## Avant de créer ou de refaire une animation

1. **Analyse du mouvement d'abord, écrite.** Avant de toucher à une pose, écrire
   `analyses/<nom_de_l_animation>.md` (modèle : `analyses/coup_de_poing_rue.md`) :
   - l'intention et la logique de chaque partie du mouvement (pourquoi on recule, pourquoi on
     tourne, à quoi sert l'autre bras…) ;
   - l'anatomie : quelles articulations bougent, quels muscles travaillent, d'où vient la force
     et comment elle passe d'un segment à l'autre ;
   - les phases, et pour chacune la position de chaque partie du corps (pieds, genoux, bassin et
     sa torsion, buste et sa torsion, épaules, coudes, poings, tête, regard) ;
   - ce qui se voit de profil et comment le rig le montre (torsion, cibles, coude imposé) ;
   - les références des vidéos étudiées (`etudes/`) et les règles de `BIBLE_ANIMATION.md` qui
     s'appliquent ;
   - les contrôles chiffrés à vérifier.
   Faire des recherches (anatomie, biomécanique, sport) quand le mouvement n'est pas évident.
2. **Construire pose par pose, comme un mannequin.** Poser la première clé, la vérifier, la
   corriger, puis seulement passer à la suivante. Vérifier en texte (`tools/anim.sh … --verifier`)
   et regarder une seule petite image par groupe de clés (`--cles --scale 1`).
3. **Logique avant esthétique.** Une pose qui « rend bien » mais qu'un vrai corps ne prendrait
   pas est fausse : un armé doit pouvoir se déplier vers la cible, la tête ne tombe pas sans
   raison, l'autre bras et l'autre épaule réagissent à la rotation du corps.
4. Ne pas changer l'apparence des personnages (style, épaisseur, couleurs) sans qu'on le demande.
