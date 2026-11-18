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
   - pour chaque pose clé, chaque articulation décrite avec **tous ses axes** à cet instant
     (épaule : élévation, plan devant/côté/arrière, rotation, omoplate ; coude ; hanche : flexion,
     écartement, rotation, appui ; genou ; cheville), voir `analyses/anatomie.md` § 4 bis et 6 bis ;
   - ce qui se voit de profil et comment le rig le montre (torsion, cibles, coude imposé) ;
   - les références des vidéos étudiées (`etudes/`) et les règles de `BIBLE_ANIMATION.md` qui
     s'appliquent ;
   - les contrôles chiffrés à vérifier.
   Faire des recherches (anatomie, biomécanique, sport) quand le mouvement n'est pas évident.
2. **Poser chaque pose clé en trois vues, profil en dernier.** On place d'abord la pose vue de
   face, puis de trois quarts, pour vérifier qu'aucun axe n'est oublié (largeur des pieds, bras
   sur le côté ou en arrière, rotation du coude, torsion), et seulement ensuite on revient de
   profil : `tools/anim.sh anims/x.json --cles --vues -o vues.png --scale 1` (une ligne par vue :
   face, trois quarts face, profil, puis la vue du jeu). Les vues sont **absolues** (lacet total,
   quel que soit le lacet de la pose) : **profil = 0°** (regard à droite ; 180° regard à gauche),
   **face = +90°**, **trois quarts face = +45°**, trois quarts dos = −45°, dos = −90° (lacet positif = le corps se tourne vers la caméra). Dans
   l'éditeur, caméra = lacet visé − lacet de la pose. Pour une pose seule :
   `tools/rendu.sh … --set lacet=90`, puis `lacet=45`, puis `lacet=0`.
   **Tour de caméra, dans les deux sens.** Une vue fixe cache des axes : de face on voit
   la profondeur sans voir comment l'avant-bras est plié ni sa rotation. Une fois la pose
   posée, faire tourner la caméra **par pas de 2°** depuis la vue de départ jusqu'au tour
   complet, de la gauche vers la droite **puis** de la droite vers la gauche, et vérifier qu'à
   chaque angle la pose reste lisible et logique (on comprend la pliure de chaque membre,
   aucune main qui traverse la tête) : `tools/anim.sh anims/x.json --cles --tour 2 -o t.png
   --scale 0.5` (deux planches par clé, `t_<image>_plus.png` et `t_<image>_moins.png`, plus un
   relevé en texte des angles où un segment se voit en moignon ou une main passe sur la tête ;
   ces angles-là se regardent de près). Dans l'éditeur : glisser la scène de 2° en 2° dans un
   sens, puis dans l'autre.
3. **Construire pose par pose, comme un mannequin.** Poser la première clé, la vérifier, la
   corriger, puis seulement passer à la suivante. Vérifier en texte (`tools/anim.sh … --verifier`)
   et regarder une seule petite image par groupe de clés (`--cles --scale 1`).
4. **Logique avant esthétique.** Une pose qui « rend bien » mais qu'un vrai corps ne prendrait
   pas est fausse : un armé doit pouvoir se déplier vers la cible, la tête ne tombe pas sans
   raison, l'autre bras et l'autre épaule réagissent à la rotation du corps.
5. **Rien ne traverse rien.** Deux parties du corps peuvent se toucher, jamais passer l'une
   dans l'autre (bras dans bras, main dans main, poing dans la tête ou le tronc…). Quand deux
   mains travaillent ensemble (craquer un poing, saisir), elles se touchent juste assez, dans la
   bonne position : la paume posée sur le poing, pas confondue avec lui. Le vérificateur le
   contrôle en 3D (`--verifier` : « … qui se traversent »).
6. **Ligne des épaules et stature du personnage.** Chaque personnage a une stature qui se garde
   dans toutes ses animations. Le bagarreur est droit et sûr de lui : buste droit, poitrine
   légèrement bombée, ligne des épaules droite ou un peu en arrière (`epaule*_av` ≤ 0), jamais
   enroulée vers l'avant, même sur un effort (on lit l'effort par les épaules qui montent puis
   tombent, les coudes, la tête, pas par un dos qui s'arrondit).
7. **C'est l'utilisateur qui juge.** Après chaque itération, préparer les images avec
   `tools/critique.sh anims/x.json DOSSIER --de a --a b --vue x,y,w,h` (clés en trois vues,
   profil, zoom, vérificateur) et les **montrer directement à l'utilisateur**, avec les
   contrôles chiffrés et ce qui a changé. C'est lui qui dit si c'est acceptable ; on ne commite
   une animation qu'avec son accord. L'agent critique (`.claude/agents/critique-animation.md`)
   valide la **fiche d'analyse** (étape 1) avant qu'on pose les clés ; il ne juge plus le
   résultat en images (sauf si l'utilisateur le demande), pour éviter des boucles d'itérations
   sans fin sur des défauts que l'utilisateur juge acceptables.
8. Ne pas changer l'apparence des personnages (style, épaisseur, couleurs) sans qu'on le demande.
