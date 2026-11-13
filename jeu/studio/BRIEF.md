# BRIEF STUDIO : ÉCHO (à lire par chaque agent avant tout)

## Situation
Un prototype jouable existe (`jeu/game/`, Godot 4.5, GDScript). Le commanditaire l'a jugé **beaucoup trop simple** :
interface, assets, cartes, obstacles, gameplay. Il veut le niveau d'un **vrai jeu pro**, comme s'il avait été fait
par une grosse équipe complète. Pixel art **riche, animé, détaillé**, en suivant **entièrement** sa méthode.
Le studio est une équipe d'agents : chacun est un professionnel de son poste, fait les recherches nécessaires
(web, livres de référence de son métier) et produit un livrable écrit dans `jeu/studio/`.

## Ce qui ne change pas (contraintes du commanditaire)
- Jeu **mobile Android**, portrait, **2D pixel art**, installable en APK. Doit être **extrêmement addictif**.
- Concept retenu : **ÉCHO**. Une tour verticale. Le héros rebondit de mur en mur (contrôle à un doigt).
  Chaque vie perdue laisse un **écho** qui **grave** le piège qui l'a tué : ce piège devient inoffensif pour
  les vies suivantes de la même ascension (4 vies sur la même tour). La marée de « Silence » monte par en dessous.
  Tape en l'air = demi-tour. On peut enrichir, approfondir, ajouter, tant que l'identité (écho qui grave) reste le cœur.
- Mécaniques « un poil innovantes ».
- Revenus : **uniquement des vidéos récompensées choisies par le joueur** (AdMob), cible pays à fort eCPM
  (US, CA, UK, AU, DE, CH, nordiques). Objectif ~2000 / jour. Aucune pub imposée, aucune bannière.
- Couleurs : **pas de marron, pas de blanc sale**. Ambiance actuelle : nuit froide bleu-violet, chaleur sur le
  héros (écharpe corail) et l'or, cyan pour les échos. La direction artistique peut l'étendre (biomes).
- Langue des livrables : **français**, phrases claires et directes.

## Ressources
- Méthode pixel art du commanditaire (OBLIGATOIRE pour tout dessin, à lire en entier pour son poste) :
  `/root/.claude/uploads/8bb7e1e6-044c-5928-b326-6b9f703cc364/512a7bf0-METHODE_PIXEL_ART-2.md`
  (règles impératives l. 47-131, partie A l. 133-570, B objets 572+, C personnages 652+, C15 créatures 1523+,
  D outils 1849+, **E animation 1874-2220**).
- Persona **Milo Hartmann** (game mechanics, game feel, UI de jeu, économie, level design, pipeline de production) :
  `/root/.claude/uploads/8bb7e1e6-044c-5928-b326-6b9f703cc364/27a1790c-milo_hartmann_game_mechanics_persona_1_2_0_FULL_plus_production.json`
  (JSON de 580 Ko : lire les clés de haut niveau ; `source_knowledge_base` et `source_knowledge_book` sont
  énormes, y chercher avec grep/python ce dont on a besoin plutôt que tout charger).
- Code actuel : `jeu/game/scripts/` (`world.gd` gameplay, `tower.gd` génération, `main.gd` écrans,
  `ui_kit.gd`, `ads.gd`, `game_state.gd`). Doc actuelle : `jeu/DESIGN.md`, `jeu/art/ART_SPEC.md`.
- Outils pixel : `jeu/tools/px.py` (grille texte → PNG), `jeu/tools/planche.py` (planche de contrôle),
  `jeu/tools/palette.txt` (palette partagée actuelle).
- Captures du prototype actuel (pour voir ce qui déçoit) : `jeu/studio/ref_prototype.png`.
- Moteur : Godot 4.5.1, rendu gl_compatibility, écran logique actuel 192×352 (modifiable si justifié),
  mise à l'échelle entière.

## Règles du studio
- Chaque agent écrit **uniquement** dans les fichiers/dossiers que son brief lui attribue.
- Pas de git (le lead s'en charge).
- Être concret : chiffres, tailles en pixels, nombres d'images, timings, règles testables. Pas de généralités.
- Chaque décision importante : la raison en une ligne.
