# Truchement

Prototype de visual novel Ren'Py (8.3.7). Environ 20 minutes par partie, 6 fins.

L'histoire complète, le sens caché et le tableau des fins sont dans [HISTOIRE.md](HISTOIRE.md).

## Jouer

1. Installer le SDK Ren'Py 8.3.x : https://www.renpy.org/latest.html
2. Dans le launcher, régler « Dossier des projets » sur le dossier parent de `vn-truchement/`.
3. Sélectionner **vn-truchement**, puis « Lancer le projet ».

Le code couleur se lit ainsi :
- bleu-gris : la langue du Nord (l'occupant) ;
- ocre : la langue de la vallée ;
- Ilan parle toujours la langue de celui à qui il s'adresse.

## Remplacer les portraits

Les images actuelles sont des placeholders étiquetés. Pour les remplacer, il suffit de déposer un PNG **du même nom** au même endroit : aucune ligne de code à modifier.

### Portraits (`game/images/persos/`)

Fond transparent, en buste, cadrage identique pour toutes les expressions d'un même personnage. Le jeu les met à l'échelle dans un cadre de 820 × 1000 px, posé en bas de l'écran.

| Fichier | Expression | Moment où on la voit |
|---|---|---|
| `mara_neutre.png` | neutre, fermée, épuisée | l'entrée, la plupart des répliques |
| `mara_inquiete.png` | inquiète | « Est-ce qu'on l'a frappé ? » |
| `mara_dure.png` | dure, froide | quand elle relève un mensonge |
| `mara_triste.png` | triste, retenue | l'aveu des coups, la fin |
| `mara_sourire.png` | petit sourire, presque complice | le tabac, « la voix a une opinion » |
| `mara_determinee.png` | déterminée | les lettres, les gants |
| `mara_surprise.png` | surprise, une fraction de seconde | quand Ilan dit « du tabac » (un indice) |
| `vey_neutre.png` | neutre, administratif | |
| `vey_las.png` | las, fatigué | son expression de base |
| `vey_agace.png` | agacé | les bottes, le générateur |
| `vey_rire.png` | rire | la plaisanterie, « du tabac ! » |
| `vey_grave.png` | grave, sérieux | le sac, les verdicts |
| `vey_emu.png` | ému, il retient quelque chose | la lettre d'Agathe |

Ilan, le narrateur, n'a pas de portrait : le joueur voit par ses yeux.

### Décors (`game/images/decors/`, 1920 × 1080)

| Fichier | Décor |
|---|---|
| `bg_poste.png` | Le poste-frontière la nuit : poêle, bureau, fenêtre sur la neige |
| `bg_poste_sombre.png` | Le même, lumière à moitié coupée (panne du générateur) |
| `bg_poste_aube.png` | Le même à l'aube, lumière froide |
| `bg_col.png` | Le sentier du col sous la neige, de nuit |
| `bg_cellule.png` | La cellule derrière le mur : pierre, lucarne à barreaux |

## Fichiers

- `game/script.rpy` : toute l'histoire et les fins.
- `game/personnages.rpy` : personnages, couleurs des langues, déclaration des images.
- `game/ecrans_truchement.rpy` : compte à rebours du dernier choix et Journal de la nuit.

## Crédits

Police Crimson Pro, par Jacques Le Bailly, sous licence SIL Open Font License (voir `game/fonts/OFL.txt`).
