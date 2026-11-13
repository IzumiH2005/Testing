# MANIFEST : game/assets/tide (F5 Marée et eau)

Sources : `art/src/tide/*.txt`, produites par `python3 art/src/tide/tide_assets.py [nom]`. Les grilles sont dessinées à la main.
Rendus ×8 et planches de contrôle : `art/out/tide/`. Vue en situation : `art/out/tide/situation_fx.png`.
Couleurs : palette_v2 seulement. Marée : u U j J. Eau O18 : 0 9 p.

| Fichier | Cellule | Images | Cadence | Pivot | Usage |
|---|---|---|---|---|---|
| tide_crest.png | 32×16 | 4 | 150 ms, en boucle | haut-gauche | Crête de la marée, tuile répétée en x (6 × 32 = 192). L'écume J et la crête j sont en haut ; la rangée 15 est en u et se raccorde à tide_body. Les images font défiler la crête de 8 px (boucle exacte). Poser la tuile à y = niveau de la marée − 5. |
| tide_body.png | 32×32 | 1 | — | haut-gauche | Corps de la marée, tuile répétée en x et en y, sous la crête. Le cycle u ↔ U se fait dans le shader. |
| tide_glow.png | 32×16 | 1 | — | haut-gauche | Halo en 3 paliers durs (j à 12 / 22 / 35 % d'opacité, intégrée au PNG). Mode **additif** (`CanvasItemMaterial.blend_mode = BLEND_MODE_ADD`). Son bas touche le haut de tide_crest. Tuile en x. |
| pal_tide.png | 4×1 | — | — | — | Palette de référence, dans l'ordre u U j J (entrée de l'échange de palette). |
| pal_tide_calm.png | 4×1 | — | — | — | Palette d'Accalmie u U J J : la crête passe de j à J. Pendant l'Accalmie, figer tide_crest sur son image courante. |
| water_surface.png | 16×16 | 4 | 200 ms, en boucle | haut-gauche, ligne d'eau en y = 1 | Surface O18 : ligne 9 qui ondule d'1 px, fond 0. Tuile en x. |
| water_body.png | 16×16 | 1 | — | haut-gauche | Eau profonde 0 avec 3 caustiques 9. Tuile en x et en y ; cycle 0/9 dans le shader (4 états, 200 ms). |
| bubble.png | 8×8 | 3 | images 0-1 : 300 ms en boucle pendant la montée ; image 2 : 80 ms à la surface | (4,4) | Bulle p avec un reflet w ; elle éclate en 4 points. |
| tide_motes.png (P1) | 8×8 | 4 | 120 ms, une fois | (4,8) | Particule qui monte de la marée (U → j → J → j). Remplace les points U dessinés en code. |
| tide_warning.png (P1) | 16×16 | 2 | 250 ms, en boucle | (8,16) | Double chevron « la marée monte », posé au bas de l'écran. |

Notes pour le moteur (aucun .gd n'a été modifié) : `world_draw.gd` lit encore `sprites/tide` (16×16, 2 images à 4 fps) et remplit le corps en u. Pour passer à F5, dessiner tide_glow (additif), puis tide_crest, puis tide_body en tuiles.
