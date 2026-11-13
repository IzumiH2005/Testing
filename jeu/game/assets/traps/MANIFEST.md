# Pièges (F3) et créatures (F11) : MANIFEST

Sources : `art/src/traps/*.txt`. Générateur : `art/src/traps/traps_assets.py [nom…]`. Mises en situation : `art/src/traps/situation.py`.
Planches, @8 et mises en situation : `art/out/traps/`.

Conventions communes :
- Toutes les bandes sont horizontales. L'image `i` est en `x = i * cellule`.
- **Orientation** : tout est dessiné pour le **mur gauche** (face WL = 32). Pour le mur droit, on retourne horizontalement (`flip_h`) et on pose l'image en miroir (formule « droite » indiquée dans la ligne de l'asset).
- **Échos** (`*_echo`) : même cellule et même ancrage que le piège. Palette q t c e uniquement, sans magenta.
- Palette : `studio/palette_v2.txt`. Danger : x X z Z. Écho : q t c e. Il n'y a ni blanc sale ni brun : le blanc W ne sert qu'aux éclats d'1 à 3 px, et w qu'au flash du boss.

## À changer dans le code (`world_draw.gd`)

1. Les chemins de chargement passent de `"sprites/…"` à `"traps/…"`, par exemple `"traps/spikes"` et `"traps/saw_echo"`.
2. **Scie** : la cellule passe de 16 à **24**, avec 4 images à 20 fps et l'ancre à `p - Vector2(12, 12)`. Le code actuel dessine `16, …%2, p-(8,8)`.
3. Épines : on peut animer l'éclat (images 1-4) toutes les 2 s, en décalant la phase selon la tuile.
4. Les états 0/1/2 de hz.gd correspondent directement aux index d'image pour laser, herse, mâchoires et onde (voir le tableau).

## Tableau

| Fichier | Cellule | Images (état) | fps | Ancrage (coin haut-gauche) | Orientation |
|---|---|---|---|---|---|
| `spikes.png` 80×16 | 16×16 | 0 repos · 1 point W · 2 croix 3 · 3 croix 5 (pic) · 4 croix 3 déclin | 12 (éclat), sinon 0 tenu 2 s | `(WL, y)` par tuile de y0 à y1. Droite : `(WR-16, y)` retourné | mur G |
| `spikes_echo.png` | 16×16 | 0 plateau émoussé | – | idem | mur G |
| `saw.png` 96×24 | 24×24 | 0-3 rotation de 15° par image (boucle de 60°) | 20 | `p - (12,12)`, centre au pixel (12,12) | symétrique |
| `saw_echo.png` 96×24 | 24×24 | 0-3 (les scies gravées tournent aussi) | 20 | `p - (12,12)` | symétrique |
| `saw_rail.png` 48×16 | 16×16 | 0 rail H (rangée 7) · 1 rail V (colonne 7) · 2 butée | – | tuile centrée sur la trajectoire : `(x, p.y-8)` pour H, `(p.x-8, y)` pour V ; butée à `fin - (8,8)` | – |
| `laser.png` 24×8 | 8×8 | 0 éteint (état 0) · 1 lueur (état 1, alterner 0/1 à 10 Hz) · 2 actif (état 2) | état | `(WL, y-4)`. Droite : `(WR-8, y-4)` retourné | mur G |
| `laser_echo.png` | 8×8 | 0 bouche gravée | – | idem | mur G |
| `beam.png` 64×8 | 16×8 | 0 préavis en tirets (état 1, clignote à 10 Hz) · 1-2-3 actif en boucle (état 2) | 20 | tuiles `(x, y-4)` de WL+8 à WR-8 | – |
| `beam_echo.png` | 16×8 | 0 ligne cyan | – | idem | – |
| `buttress.png` 32×58 | 16×58 | 0 hauteur 32 (rangées 0-41) · 1 hauteur 48 (rangées 0-57) | – | `(bx, y0-5)`, bx = WL. Droite : `(WR-16, y0-5)` retourné | mur G |
| `buttress_echo.png` | 16×58 | 0 · 1, épines émoussées | – | idem | mur G |
| `portcullis.png` 120×32 | 24×32 | 0 rentrée (état 0) · 1 préavis à 4 px (état 1, 10 Hz) · 2 sortie et éclat (1/12 s) · 3 sortie tenue (état 2) · 4 rentrée à 12 px (1/12 s) | 12 | `(WL, y0)`, motif de 8 px répété ou coupé jusqu'à y1. Droite : `(WR-24, y0)` retourné | mur G |
| `portcullis_echo.png` | 24×32 | 0 lances sorties | – | idem | mur G |
| `jaws.png` 48×24 | 16×24 | 0 corps bouclable · 1 tête ouverte ou fermée · 2 tête en préavis (alterner 1/2 à 10 Hz) | état | tête `(WL+ext-16, mid-12)`, corps `(WL+16i, mid-12)`. Droite : miroir, tête `(WR-ext, mid-12)` | mur G |
| `jaws_echo.png` | 16×24 | 0 pont gravé, bouclable de WL à WR | – | `(x, mid-12)` | – |
| `crumble.png` 64×32 | 16×32 | 0 intacte · 1 fissure 1 · 2 fissure 2 · 3 chute (puis rien pendant 3 s) | ~6 (0,17 s / 0,18 s / 1/8 s) | `(WL-4, y0)`, motif de 16 px. Droite : `(WR+4-16, y0)` retourné | mur G (non létal, sans écho) |
| `rockfall_books.png` | 16×16 | 0 pile de 3 livres | – | `(x-8, ry-8)` | – |
| `rockfall_books_echo.png` | 16×16 | 0 | – | idem | – |
| `rockfall_mark.png` 32×4 | 16×4 | 0 poussière et zz · 1 poussière et ZZ (préavis de 0,6 s, alterner à 10 Hz) | 10 | `(x-8, ry+6)` | – |
| `pendulum_chandelier.png` 48×16 | 16×16 | 0 reflet A · 1 reflet B · 2 smear (1 image au point bas, retourner selon le sens) | 2 phases par période | `pendulum_pos - (8,8)` | – |
| `pendulum_chandelier_echo.png` | 16×16 | 0 | – | idem | – |
| `chain.png` | 8×8 | 0 maillon (n m l, non létal) | – | `(point de la tige) - (4,0)`, un maillon tous les 8 px, sans rotation | – |
| `moth.png` 48×16 | 16×16 | 0 ailes hautes · 1 ailes basses (boucle 0-1) · 2 virage (1 image au demi-tour) | 8 | `moth_pos - (8,8)` ; hitbox 8×6 = x 4-11, y 5-10 | vue de face |
| `moth_echo.png` | 16×16 | 0 | – | idem | – |
| `gnawer.png` 64×16 | 16×16 | 0 appui A · 1 passage · 2 appui B · 3 passage (boucle) | 8 | `pos - (8,8)` avec g.x = WL+4 ; colonne 4 = face du mur | mur G, **en montée**. Descente : `flip_v`. Mur droit : `flip_h` |
| `gnawer_echo.png` | 16×16 | 0 | – | idem | idem |
| `boss_sonneur.png` 192×48 | 48×48 | 0 balancement, battant à −3 (cloche qui va à droite) · 1 battant à +3 (va à gauche) · 2 flash w (1/20 s) · 3 tremblement +1 px (alterner 3/0 à 20 Hz pendant 1 s) | 20 en mode « sonné » | `bell_pos() - (24,24)` ; cercle létal r 20 autour du pixel (24,24). Le sprite ne tourne pas | – |
| `boss_sonneur_yoke.png` | 64×16 | 0 joug de pierre n s m l (non létal) | – | `(96-32, mid-56-13)` ; pivot au pixel (29-30, 13) | – |
| `boss_wave.png` 64×8 | 16×8 | 0 préavis pointillé (0,6 s, clignote à 10 Hz) · 1-2-3 actif en boucle | 20 | tuiles `(x, wave_y-3)` de WL à WR ; bande létale sur les rangées 1-5, centre en rangée 3 | – |
| `boss_wave_echo.png` | 16×8 | 0 ligne de 2 px c / qt | – | idem | – |
