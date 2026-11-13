# ÉCHO : document de conception (v0.1)

## Le concept en une phrase
Un grimpeur rebondit d'un mur à l'autre dans une tour piégée. Chaque vie perdue laisse un **écho**
qui **grave** le piège qui l'a tué : ce piège devient inoffensif pour les vies suivantes de la même ascension.

## La boucle
- **Une ascension = 4 vies sur la même tour** (même graine). La vie 1 découvre, les vies 2 à 4 montent
  plus haut parce que les pièges mortels sont désormais gravés (cyan, neutres).
- **Un seul geste** : taper fait sauter vers le mur opposé. Taper **en l'air** fait un demi-tour
  (le petit plus « innovant » : on peut feinter une scie ou attendre un laser sans toucher le mur).
- **La marée de Silence** monte par en dessous et accélère : impossible de camper.
- Score = **hauteur de la meilleure vie** de l'ascension. Les échos des vies précédentes (fantômes
  cyan, 3 max) rejouent leur trajet en même temps que vous.

## Pourquoi ça accroche (les leviers)
| Levier | Mécanique |
|---|---|
| « Encore une » | La mort est utile : elle rend la vie suivante plus facile, donc on veut voir la suite. |
| Progrès visible | Barres par vie dans le résumé, record en or dans le HUD, toast au record battu. |
| Rendez-vous quotidien | **Tour du jour** (même graine pour tout le monde) + **série** : bonus 5 + 5 × série (max 35 éclats). |
| Collection | 8 tenues (0 à 500 éclats). |
| Partage | Texte prêt à coller : une ligne par vie (☠ ▰▰▱…), façon Wordle. |

## Équilibrage vérifié
`tests/bot_test.gd` (robot à vision parfaite qui simule chaque saut) : 11 graines sur 12 sont franchies
jusqu'au temps limite (~1600 m en 4 min). Les tours sont donc toujours possibles, et la difficulté vient
du joueur, pas du générateur. Le robot « naïf » (taper sans regarder) meurt vers 18 m : un débutant
apprend vite la règle sans être bloqué.

## Monétisation : uniquement des vidéos récompensées choisies
Aucune pub imposée, aucune bannière. Deux emplacements :
1. **+1 vie** : proposé une fois par ascension, quand les 4 vies sont épuisées.
2. **×2 éclats** : sur l'écran de résumé.

Dans la v0.1 ces pubs sont **simulées** (écran de 3 s). L'interface `Ads.show_rewarded(placement, on_reward, on_cancel)`
est celle du futur plugin AdMob : il suffira de remplacer l'intérieur de `scripts/ads.gd`.

### Calcul de l'objectif 2000 / jour
Vidéo récompensée, pays riches (US, CA, UK, AU, DE, CH, Nordiques) : eCPM réaliste **10 à 25 $**.
On compte ~1,5 vidéo vue par joueur actif et par jour.

| Si l'objectif est… | ≈ en $ | Vidéos / jour (eCPM 15 $) | Joueurs actifs / jour |
|---|---|---|---|
| 2000 **FCFA** | ~3,3 $ | ~220 | **~150** |
| 2000 **CHF** | ~2 250 $ | ~150 000 | **~100 000** |

Hypothèse retenue pour la v0.1 : FCFA (à confirmer). Dans les deux cas, ce qui fait monter le chiffre est
la **rétention J1/J7** (tour du jour, série) et la part de joueurs en pays riches (fiche Store en anglais
d'abord, campagnes ciblées).

## Prompts Ludo AI (pour aller plus loin que le pixel art fait main)
Style commun à ajouter à chaque prompt :
> 2D pixel art, limited palette (deep night blue-violet stone, warm coral red hero, gold shards, cyan ghost echoes),
> top-left lighting, crisp 1px dark outline, no anti-aliasing, no brown, no off-white, transparent background.

1. **Icône Store 512×512** : « Tiny hooded climber with a long coral-red scarf mid-jump between two dark stone
   tower walls, a cyan ghost silhouette of himself trailing behind, purple glowing tide at the bottom, gold sparkle,
   bold readable silhouette, icon composition, centered ». 
2. **Image de présentation 1024×500** : « Vertical tower interior seen from the front, many floors of traps
   (wall spikes, spinning saw blades, red laser beams), some traps glowing cyan as if engraved and harmless,
   a small coral-scarf climber leaping, three cyan ghost echoes following his path, logo space on the left ».
3. **Feuille de personnage 16×16** : « 16x16 pixel sprite sheet, hooded climber with coral scarf, frames: idle
   clinging to wall, jump, air spin turn, death poof, horizontal strip, 6 frames ».
4. **Pièges 16×16** : « 16x16 pixel art traps sprite sheet: wall spikes, circular saw blade 2 frames, laser
   emitter off/warning/on, each also in a calm cyan engraved variant ».
5. **Fond de tour** : « Seamless vertical tileable background 192x352, distant dark tower interior with arches,
   faint moss, tiny purple windows, low contrast so gameplay reads on top ».

## Ce qui reste pour une sortie Play Store
1. Vrai AdMob : export Gradle + plugin Godot AdMob, permission Internet, ID d'app et d'unités.
2. Consentement (UMP / RGPD) obligatoire pour l'Europe.
3. Garder précieusement le keystore de publication (sans lui, aucune mise à jour possible).
4. Fiche Store EN/FR, captures (le dossier `tests/` sait déjà en produire), classement d'âge.
5. Test sur 10-20 joueurs : mesurer la hauteur moyenne de la vie 1 et de la vie 4, et la rétention J1.
