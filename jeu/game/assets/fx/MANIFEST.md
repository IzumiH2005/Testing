# MANIFEST : game/assets/fx (F2 Écho et gravure · F4 Collectibles et FX · autel)

Sources : `art/src/fx/*.txt`, produites par `python3 art/src/fx/fx_assets.py [nom]`. Les grilles sont dessinées à la main.
Rendus ×8 et planches de contrôle : `art/out/fx/`. Vue en situation : `art/out/fx/situation_fx.png`.
Toutes les couleurs viennent de palette_v2. Bandes horizontales, une cellule par image, pivot constant.
Pivot (x,y) en pixels, mesuré depuis le coin haut-gauche de la cellule.

## F4 : collectibles et power-ups
| Fichier | Cellule | Images | Cadence | Pivot | Usage |
|---|---|---|---|---|---|
| shard.png | 8×8 | 6 | 8 fps, en boucle | (4,4) | Petit éclat d'or (g G y, contour o) : rotation, puis éclat. Remplace `sprites/shard` (4×8) : prendre `f = int(t*8) % 6`. |
| shard_big.png | 16×16 | 4 | 4 fps, en boucle | (8,8) | Gros éclat (gemme 10×10, facette W) qui scintille. Remplace le polygone actuel. |
| shard_pop.png | 16×16 | 5 | 40·50·60·70·80 ms, une fois | (8,8) | Ramassage : pop, puis 4 étincelles y. |
| powerup_bubble.png | 16×16 | 4 | 4 fps, en boucle | (8,8) | Bulle 12×12 (contour G) avec reflet, flottement d'1 px intégré. Poser l'icône en (4, 4+dy) avec dy = 0,0,1,1. |
| pu_burin.png / pu_plume.png / pu_calm.png | 8×8 | 1 | — | (4,4) | Icônes dans la bulle : burin c e, plume w p, accalmie J j U. |
| feather_gold.png | 16×16 | 6 | 6 fps, en boucle | (8,8) | Plume dorée qui se balance en aller-retour. |
| pu_magnet.png / pu_lantern.png / pu_gold.png (P1) | 8×8 | 1 | — | (4,4) | Icônes P1 : aimant, lanterne, pluie d'or. |
| fx_magnet.png (P1) | 16×16 | 3 | 10 fps, en boucle | (8,6) | Arcs G de l'aimant autour du héros. |
| lantern_flame.png (P1) | 8×8 | 4 | 10 fps, en boucle | (4,8) | Flamme de la lanterne (A a o, contour r). |
| relic_fragment.png (P1) | 8×8 | 4 | 6 fps, en boucle | (4,4) | Fragment de relique : pierre m l, cœur G. |
| moon_shard.png (P1) | 16×16 | 4 | 4 fps, en boucle | (8,8) | Éclat de lune : w W, contour l. |

## F4 : FX de mouvement et particules
| Fichier | Cellule | Images | Cadence | Pivot | Usage |
|---|---|---|---|---|---|
| fx_dust_wall.png | 16×16 | 4 | 12 fps, en boucle pendant la glissade | (0,12) | Poussière p/l. Mur à GAUCHE de la cellule ; `flip_h` pour le mur droit. |
| fx_jump_puff.png | 16×16 | 4 | 50·70·90·110 ms, une fois | (8,9) | Bouffée de saut, du clair (w) au sombre (m), effacée par morceaux. |
| fx_land.png | 16×16 | 4 | 40·60·80·100 ms, une fois | (0,7) | Impact sur le mur : 1 image de flash w, puis éclats p → l → m. Mur à gauche ; `flip_h` pour le mur droit. |
| fx_turn.png | 16×16 | 3 | 50·70·90 ms, une fois | (8,8) | Volte normale (y G g o). |
| fx_turn_echo.png | 16×16 | 3 | 50·70·90 ms, une fois | (8,8) | Volte rechargée par l'écho (e c t q), même dessin que fx_turn. |
| fx_graze.png | 16×16 | 3 | 30·50·50 ms, une fois | (8,8) | Frôlé : étincelle w de 3 px, rien d'autre. |
| fx_spark.png | 8×8 | 5 | 60 ms, une fois | (3.5,3.5) | Étincelle générique : point → croix 3 → croix 5 → croix 3 → point. |
| picto_tap.png | 16×16 | 2 | 400·300 ms, en boucle | (8,16) | Onboarding : main qui tape (même main que `sprites/tap`). |
| picto_hold.png | 16×16 | 4 | 70 ms par image, puis tenir l'image 3 | (8,16) | Main tenue, avec une barre de 0,28 s qui se remplit. |
| picto_turn.png | 16×16 | 2 | 350 ms, en boucle | (8,16) | Main et flèche courbe (volte). |
| picto_echo.png | 16×16 | 2 | 350 ms, en boucle | (8,16) | Losange d'écho et flèche de volte. |

## F2 : écho et gravure
| Fichier | Cellule | Images | Cadence | Pivot | Usage |
|---|---|---|---|---|---|
| fx_engrave_wave.png | 80×80 | 6 | 40·50·60·70·80·90 ms, une fois | (40,40) | Onde de gravure de rayon 0 → 40 (anneau e/c/t qui s'amincit), placée au point d'impact (t = 0,63 s). Remplace le clignotement à 20 Hz. |
| fx_engrave_seal.png | 16×16 | 4 | 50·60·60 ms, puis tenir l'image 3 | (7.5,7.5) | Pop du sceau d'écho sur le piège gravé. |
| grave.png (P1) | 16×16 | 4 | 2400·80·100·80 ms, en boucle | (7.5,7.5) | Sceau gravé qui lance un éclat lent. Remplace `sprites/grave` (8 px). |
| echo_shard.png | 8×8 | 4 | 8 fps, en boucle | (4,4) | Éclat d'écho au point de mort (e c t, cœur W, contour q). Pour un fantôme, appliquer une opacité de 50 % avec `modulate`. |
| fx_echo_recharge.png | 16×16 | 4 | 50·50·60·90 ms, une fois | (7.5,7.5) | Contact cyan : les particules convergent, flash, puis anneau. |
| fx_echo_trail.png | 8×8 | 4 | 60 ms, une fois ; émettre toutes les 2 images | (4,4) | Traînée du fantôme-guide (c e → t). |
| fx_death_burst.png (P1) | 32×32 | 6 | 33·80·90·100·110·120 ms, une fois | (16,16) | Volutes détachées du corps : flash W, puis I → i → H → h, effacées par morceaux. |

## Autel
| Fichier | Cellule | Images | Cadence | Pivot | Usage |
|---|---|---|---|---|---|
| altar.png | 32×32 | 2 (états) | — | (16,32) | Image 0 : autel éteint. Image 1 : autel allumé (glyphe e/W, vasque q/t, dessus éclairés). Remplace le rectangle d/a actuel. |
| altar_flame.png | 8×16 | 6 | 10 fps, en boucle | (4,16) | Flamme cyan, affichée seulement quand l'autel est allumé. Coin haut-gauche à (+12, −5) depuis le coin haut-gauche de l'autel. |

## Notes pour le moteur (aucun .gd n'a été modifié)
- `world_draw.gd` lit encore `sprites/shard` (4 images) et dessine en code le gros éclat, la bulle, l'autel et l'onde. Ces fichiers sont prêts à les remplacer.
- Aucun halo n'est intégré à ces sprites. Les halos additifs restent ceux de F8 (`halo_s/m/l`).
