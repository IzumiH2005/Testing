# ÉCHO : bible artistique v2

Auteur : direction artistique pixel art. Statut : **référence opposable** pour tous les pixel artists.
Elle remplace `art/ART_SPEC.md` partout où les deux diffèrent.

**Ce que tout le monde doit lire :**
- la méthode `METHODE_PIXEL_ART` : règles impératives 1-30 et parties A (lisibilité, pipeline, finition), B (objets), C (personnages) et E (animation). Chaque décision ci-dessous cite sa section entre crochets, par exemple [A2], [C10] ou [E2-F] ;
- `studio/palette_v2.txt` : la palette unique ;
- `studio/art_tests/` : planches d'essai et mise en situation.

Toute décision a sa raison en une ligne. Si un asset contredit cette bible, c'est l'asset qui est faux.
Pour contester une règle, il faut une planche en situation qui prouve le contraire [A6-J « en situation »].

---

## 0. Décisions en un coup d'œil

| Sujet | v1 (prototype) | v2 (décision) | Raison |
|---|---|---|---|
| Écran logique | 192×352, mise à l'échelle non entière sur 1080 px | **largeur fixe 180 px, hauteur 320 à 430 px** (« expand »), échelle entière | 1080/180 = ×6 exact. 192 donne ×5,625 (pixels inégaux) |
| Puits jouable | 160 px entre les murs | **144 px** (9 tuiles) + murs de 18 px visibles | Le héros passe de 9 % à 14 % de la largeur jouable |
| Héros | 16×16, silhouette 10×14 | **cellule 32×32, silhouette 18×21** | Classe 20-24 px de [C10]. À 16 px il manque yeux, mains et marge d'exagération |
| Tuile | 16×16 | **16×16** (mur) ; modules 32×16 et 32×32 (fond) | Règles de [A3] 16 px ; le module 2× du fond se lit comme plus lointain |
| Palette | 31 couleurs, une rampe « nuit » pour tout | **71 couleurs** en rampes à décalage de teinte, **bandes de luminance** par plan | Diagnostic n°1 : décor, murs et héros avaient la même valeur |
| Plans | 1 fond + murs | **5 plans** (P0 à P4) + particules | Profondeur inexistante en v1 |
| Lumière | aucune source | haut-gauche + sources émissives **peintes** + halos en paliers | [A5-8], [C15-D] |
| Biomes | 1 | **6** | Progression visuelle = récompense de la montée |

---

## 1. Diagnostic : pourquoi le prototype a l'air amateur

Constat fait sur `ref_prototype.png` (15 écrans) et sur les sprites @8 de `art/out/`.

1. **Une seule bande de valeur pour tout.** Le fond en briques, les murs et la cape du héros vivent tous dans `n s m`.
   - Au test du plissement d'yeux et du gris, l'écran devient une soupe bleue [A2 « la valeur fait le travail », A6-J gris].
   - Le budget de contraste n'est pas concentré sur le point d'intérêt [A2 « budget de contraste »].
2. **Le héros est trop petit et sa silhouette ne change pas.**
   - Il occupe environ 5 % de la largeur d'écran. Sa silhouette 10×14 reste un « grain » bleu identique sur les 5 images [A2 silhouette d'abord, A4b « le plus petit détail nécessaire fixe la taille »].
   - À 16 px, [C10] n'autorise que « catégorie + 1 détail d'identité » : l'écharpe consomme tout le budget. Il ne reste ni main, ni regard, ni pose lisible.
3. **Les pièges ne parlent pas le langage du danger.**
   - La scie se lit comme un biscuit framboise : disque plein, points sombres, pas de moyeu, pas de dents triangulaires [B3 forme iconique, A4b triangle = danger].
   - Le laser est une boîte grise avec un point rouge.
   - Il n'y a ni préavis ni rampe d'émission [E2-F éteint → lueur → pic].
4. **Répétition sans hiérarchie.**
   - Briques identiques du haut en bas, 6 tuiles de mur presque jumelles.
   - Il manque le rapport grand/moyen/petit [A4b ~70 %], les détails narratifs placés par la nature [A5-9] et l'espace vide utile [A4b].
   - La fissure est une diagonale droite qui ne suit pas la pierre [A4 « les détails suivent la surface », A5-8b].
5. **Joints noirs `k` partout.** Le noir du contour de collision et du héros sert aussi aux joints de pierre, si bien que le plan de jeu n'a plus de contour propre [A5-6 hiérarchie des contours, A6-C].
6. **Aucune source de lumière, aucun émissif.** Pas de torches, de cristaux ou de halo, alors que le thème (échos lumineux, nuit) l'appelle [A5-8 émissifs, C15-D].
7. **Aucune profondeur.** Un seul fond, pas de parallaxe, pas d'avant-plan, pas de particules d'ambiance [A5-9 particules].
8. **Animations sans principes.**
   - 5 images sans anticipation, sans suite de mouvement de l'écharpe, sans tenue [E1 tableau].
   - Pas de durée variable par image, pas de feuille de timing [E2-A, E3, règles 26-30].
9. **Une interface générique et sans lien avec le monde.**
   - Panneaux plats bleu marine à filet clair, boutons de couleurs arbitraires (orange, sarcelle, bleu), logo cyan plat.
   - Le texte du tutoriel est posé au milieu du puits, sur la zone de jeu.
10. **Couleurs non réservées.** Le rouge du danger et le corail du héros sont voisins. Le cyan sert à la fois au décor (rune `t` du fond) et à l'écho : le joueur ne peut pas apprendre un code couleur [A2 « un seul accent saturé », C16-D].

---

## 2. Résolution et échelle

### 2.1 Décision
- **Viewport de base : 180×320.** Dans Godot 4.5 :
  - `display/window/stretch/mode = viewport` ;
  - `aspect = expand` ;
  - `scale_mode = integer` ;
  - filtre de texture `Nearest` ;
  - `rendering/2d/snap/snap_2d_transforms_to_pixel = true` et `snap_2d_vertices_to_pixel = true`.
- Le facteur d'échelle est le plus grand entier qui fait tenir 180×320. La place restante est **donnée au jeu** (« expand »), pas aux bandes noires :

| Écran | Facteur | Zone logique visible |
|---|---|---|
| 1080×2400 (cible, 20:9) | ×6 | **180×400** (remplissage exact) |
| 1080×2340 / 2280 | ×6 | 180×390 / 180×380 |
| 720×1600 | ×4 | 180×400 |
| 1440×3200 | ×8 | 180×400 |
| 1170×2532 (iPhone) | ×6 | 195×422 |
| 1536×2048 (tablette) | ×6 | 256×341 |

### 2.2 Pourquoi 180
- 1080 et 720 sont les largeurs Android dominantes ; 180 les divise (×6, ×4), ainsi que 1440 (×8).
- 192 (v1) ne divise ni 1080 ni 720. Les pixels y ont des tailles inégales, ce qui tue le pixel art ([D] outils, règle 25).
- Recherches : la règle « la base doit diviser la résolution physique pour remplir sans bandes » est confirmée par le forum Godot et le blog Bugnet. Pour du 20:9, les seules bases exactes en ×6 sont de la forme 180×400 (voir §14).
- Alternative examinée : **216×480 (×5)**. Elle donne 20 % de pixels en plus, mais le héros paraît 17 % plus petit à l'écran et ne remplit pas 720 de façon entière. Rejetée.

### 2.3 Règles de mise en page
- **Le puits jouable fait toujours 144 px** (9 tuiles de 16), centré.
- Toute largeur logique supplémentaire (195, 256) va dans **l'épaisseur des murs**, jamais dans le puits. Le gameplay reste ainsi identique sur tous les appareils.
- La hauteur supplémentaire (320 → 430) sert à **voir plus haut** : on anticipe mieux les pièges.
- La caméra place le héros à 62 % de la hauteur, en partant du haut.
- Zones sûres : **20 px en haut** (encoche, HUD) et **24 px en bas** (barre gestuelle). Aucun piège ni texte de tutoriel n'y entre.
- Mesures physiques à ×6 sur 1080×2400 :
  - le héros mesure 21 × 6 = 126 px physiques, soit 5,3 % de la hauteur (v1 : environ 3 %) ;
  - 1 px logique ≈ 2,2 dp. Une cible tactile de 48 dp vaut donc 22 px logiques, d'où des **boutons d'au moins 24 px de haut**.

### 2.4 Impact pour le code (à transmettre au lead)
- Murs : 18 px visibles de chaque côté (une colonne de tuile entière + 2 px de la suivante coupée par le bord). Puits : 144 px.
- La physique du saut horizontal est à recalibrer : distance 144 au lieu de 160, soit **×0,9** sur la vitesse horizontale pour garder le même temps de traversée.
- Aucun parallaxe sur un objet de collision [recherche Wayline : le parallaxe fausse la lecture des distances].

---

## 3. Tailles

### 3.1 Héros : 16×16 ne suffit pas
- Selon [C10], à 16 px on a 1,7-2 têtes, des yeux de 1×1, 5 à 8 couleurs, et l'on ne porte qu'une catégorie et un détail d'identité.
- Or le héros d'ÉCHO doit montrer simultanément :
  1. la direction du regard (lire vers où il va sauter) ;
  2. l'écharpe et sa suite de mouvement (identité + lecture de la vitesse) ;
  3. une main ou un pied contre le mur (état « accroché ») ;
  4. l'exagération de 2-4 px du squash & stretch [E1].
- Quatre informations ne tiennent pas dans 10×14 px.
- **Décision : classe 20-24 px de [C10].**
  - Silhouette **18×21** (bbox), capuche de 10 rangées, soit environ 48 % (dans la fourchette 45-60 %).
  - 2 têtes de haut. Yeux **1×2** (pas 2×2 : réservé au-dessus de 16×24, [C10]). **11 couleurs** (fourchette 8-13).
- **Cellule 32×32** (multiple de 8 [E8-B]) : marge pour l'écharpe qui flotte (jusqu'à 8 px), l'étirement (+3 px) et les smears.
  - Pivot unique **(16,27)**, au pied, sur toutes les images [E8-A].
  - En pose accrochée, le bord de la silhouette côté mur est à x=7.
- Style « héroïque » au sens de [C10] : c'est le **volume de la capuche + l'écharpe** qui porte la silhouette, pas les membres.
  - Chibi sans épaules marquées [C13 règles 10 et 13].

### 3.2 Grille des tailles (tout en px logiques)

| Élément | Taille | Lecture voulue |
|---|---|---|
| Tuile de mur de jeu | 16×16 | 2-3 tons par matière, une seule idée de détail, pas d'AA [A3] |
| Module de mur décoré (torche, cristal, niche) | 16×32 | Le « moyen » du rapport grand/moyen/petit [A4b] |
| Paroi de fond (P2) | 32×16 et 32×32 | Motif 2× plus gros, donc lu comme plus loin |
| Héros | cellule 32×32, silhouette 18×21 | Personnage [C10] 20-24 |
| Écho (fantôme) | cellule 32×32 | Même silhouette que le héros, contour coloré `q` |
| Pics muraux | 16×16 (profondeur 6 px) | Triangle = danger [A4b] |
| Scie | 32×32 (diamètre 24) | Plus grande que la tête du héros : menace lisible |
| Émetteur laser | 16×32 | Objet mural |
| Rayon | segment 8×16, épaisseur active 5 px | |
| Éclat d'or | cellule 16×16, gemme 9×11 | 16 px = catégorie + 1 détail [A4b] |
| Icônes HUD | 12×12 | Icônes de bouton : 16×16 |

---

## 4. Palette v2 (`studio/palette_v2.txt`)

### 4.1 Principes
- **Les rampes sont construites selon [A6-A] :**
  - le ton moyen est le plus saturé ;
  - vers l'ombre, plus sombre et teinte vers le froid (violet ou bleu) ;
  - vers la lumière, plus clair, moins saturé, teinte vers le chaud (cyan, jaune) ;
  - la teinte tourne de **10 à 20° par cran**, avec des crans plus courts près du blanc ;
  - les rampes sont partagées ou chaînées [A5-7]. Exemple : l'ombre de l'or est le corail `o`.
- **Pas de brun :**
  - aucune teinte 20-45° n'existe sous V 90 ;
  - l'or ne s'assombrit jamais, il glisse vers le corail ;
  - les biomes chauds (Clocher) sont **prune**, pas bruns.
- **Pas de blanc sale :** les blancs sont froids (`w` #e6f6ff, `I` #f2f6ff) ou purs (`W`).
- **Compatibilité :** les lettres de la v1 sont conservées (`k b d n s m l p w W q t c e r R o a x X z Z g G y v V u U`). Les anciennes sources se rendent sans erreur avec `palette: /home/user/Testing/jeu/studio/palette_v2.txt` ; seules les teintes changent.
- **Couleurs réservées** (règle de code couleur, inspirée de Downwell, §14) :
  - **corail `o`** = le héros ;
  - **magenta `x X z Z`** = ce qui tue ;
  - **cyan `q t c e`** = l'écho ;
  - **or `g G y`** = ce qui se ramasse ;
  - **violet `u U j J`** = la marée.
  - Aucun décor n'emploie ces rampes. Un lierre piégé reste magenta, pas vert.

### 4.2 Bandes de luminance (la règle n°1 de lisibilité)
Les valeurs sont des luminances relatives Y (WCAG), calculées et vérifiées.

| Plan | Y | Couleurs |
|---|---|---|
| P0 fond lointain | 0,004-0,012 | `k b ^ ( [ { <` |
| P1-P2 fond proche, paroi | 0,017-0,030 | `d ~ ) ] } >` |
| P3 murs de jeu | **ombre 0,032 · base 0,062 · lumière 0,128**, arête 0,32 sur 1 px seulement | `n s m l` (Crypte) et équivalents par biome |
| Acteurs (héros, pièges, échos, or, marée) | 0,25-0,92 pour leurs tons de base et de lumière | |

- **Tous les biomes partagent exactement la même échelle de Y pour les murs.** Seule la teinte change.
- Raison : la lisibilité du gameplay ne doit jamais dépendre du biome [A2]. Le biome change l'ambiance, pas la grammaire.

### 4.3 Rampes du noyau

| Rampe | Clés et hex (sombre → clair) | Teintes |
|---|---|---|
| Nuit (contour, fonds de la Crypte) | `k` #0e0a1a · `b` #17122a · `d` #23203d | 256 → 244° |
| Pierre de jeu (Crypte) | `n` #2f2c5c · `s` #39427b · `m` #46639f · `l` #719dca · `p` #abd1eb · `w` #e6f6ff · `W` #ffffff | 244 → 200° |
| Cape du héros | `h` #503d7a · `H` #8a83c7 · `i` #c7ccf0 · `I` #f2f6ff | 258 → 222° |
| Écharpe (chaleur) | `r` #751a38 · `R` #cc353f · `o` #ff7247 · `a` #ffba6b · `A` #fff0c7 | 340 → 44° |
| Danger | `x` #660e4c · `X` #b81661 · `z` #ff3874 · `Z` #ffb2c4 | 318 → 346° |
| Or | (`o`) · `g` #fa9e14 · `G` #ffd738 · `y` #fff9a8 | 36 → 56° |
| Écho | `q` #114161 · `t` #1787a3 · `c` #3fe0e0 · `e` #b8ffee | 204 → 166° |
| Silence (marée) | `u` #2c1752 · `U` #6a3499 · `j` #bd69db · `J` #f9c7ff | 262 → 294° |
| Végétal / cristal | `v` #174e52 · `V` #328a78 · `f` #53bd8b · `F` #9bebad | 184 → 134° |
| Eau, horizon | `0` #234a75 · `9` #448eb2 · `$` #854a6b | |

Pourquoi une cape lavande-glace et non bleue comme en v1 :
- elle est **3,8× plus contrastée** que les murs (`i` contre `m`) ;
- elle reste froide et nocturne ;
- elle laisse l'écharpe corail être le **seul accent chaud saturé** de l'écran [A2, C16-D].

### 4.4 Rampes de biome (4 tons de mur + 2 tons de fond)

| Biome | Ombre · base · lumière · arête | Fond lointain · proche | Teinte du mur |
|---|---|---|---|
| 1 Crypte des Échos | `n s m l` | `b d` | indigo 244 → 210° |
| 2 Fonderie froide | `1` #2a3341 · `2` #364957 · `3` #4a6973 · `4` #76a1a4 | `(` #0f1622 · `)` #192431 | acier 218 → 184° |
| 3 Bibliothèque engloutie | `5` #3a2a55 · `6` #483d7b · `7` #5a5cad · `8` #8a98cc | `[` #191229 · `]` #261f3b | encre 262 → 228° |
| 4 Jardin suspendu de cristal | `B` #452749 · `C` #5a396a · `D` #76569a · `K` #a191c9 | `{` #1f1025 · `}` #2e1c37 | mauve 292 → 258° |
| 5 Clocher des vents | `L` #452a39 · `M` #5f3b56 · `N` #825580 · `O` #b08eb6 | `<` #23101f · `>` #331a30 (+ `$` horizon) | prune 326 → 292° |
| 6 Sommet céleste | `P` #2c3149 · `Q` #3a475b · `S` #516777 · `T` #829fa7 | `^` #12142a · `~` #1e2139 | marbre argent 228 → 194° |

### 4.5 Contrastes vérifiés (ratios WCAG)

| Paire | Ratio | Lecture |
|---|---|---|
| Mur base `s` / fond proche `d` | 1,66 | Le mur se détache du fond sans crier |
| Mur lumière `m` / `d` | 2,64 | |
| Base de mur / fond proche, pour chacun des 5 autres biomes | 1,92-1,94 | Constant d'un biome à l'autre |
| Cape `H` / fond `d` | **4,57** | Héros sur le vide |
| Cape `H` / mur `s` | 2,75 | Héros contre le mur, plus le contour `k` |
| Lumière de cape `i` / mur `m` | 3,76 | |
| Contour `k` / mur `m` | 3,29 | Le contour sépare le héros du mur |
| Écharpe `o` / `d` | **5,76** | L'accent |
| Écharpe `o` / `s` | 3,46 | |
| Danger `z` / mur `s` | 2,71 | Plus `Z` en cœur émissif : `Z` / `m` = 3,5 |
| Écho `c` / mur `s` | **5,78** | |
| Or `G` / mur `s` | **6,71** | Le collectible est l'objet le plus visible après le héros |
| Crête de marée `j` / `b` | 5,37 | |
| Contour d'écho gravé `q` / mur `s` | 1,15 | Voulu : un piège gravé est inoffensif, donc il s'efface [A2] |
| `o` / `z` (corail / danger) | 1,28 | **Point de vigilance** (règle ci-dessous) |

- `o` et `z` ont presque la même luminance. Leur distinction repose sur trois choses :
  - la teinte (28° d'écart) ;
  - la forme (triangles, dents) ;
  - l'animation (pulsation d'émission).
- Règle : **aucun élément danger ne touche le héros en idle** dans les compositions d'UI ou de menu, et le danger a toujours un cœur `Z`/`W`.

### 4.6 Budgets [A3, A6-B]
- Héros : 11 couleurs. Écho : 6. Piège : 6 au maximum (4 danger + `k` + 1 métal). Tuile de mur : 5 (+ 2 pour la mousse).
- Fond : 3 par plan. Icône : 5. Écran complet : 40 couleurs au plus visibles en même temps.
- Test obligatoire « une couleur de moins » [A6-B] sur chaque asset.

---

## 5. Lumière

1. **Lumière clé : haut-gauche à 45°, partout et toujours** [règle 23, A5-8, E2-F].
   - Ombres portées en bas-droite. Arêtes éclairées : dessus et gauche. Le miroir du code (mur droit) ne retourne pas la lumière.
   - **Les tuiles du mur droit sont donc dessinées à part**, pas en miroir. C'est un écart volontaire avec la v1, qui faisait le miroir dans le code et inversait la lumière.
   - Le héros, lui, est retourné en miroir : un personnage tolère une lumière inversée, une architecture non (voir [A6-J miroir]).
2. **Sources locales peintes, pas calculées.** Chaque source a 3 couches :
   - (a) **Sprite émissif** à ombrage inversé : cœur `W`/clair au centre, bords saturés, **contour coloré** (jamais `k`) [A5-8 émissifs, C15-D].
   - (b) **Halo** : sprite séparé en mélange additif, 2-3 disques concentriques à bord dur, couleurs de la palette, opacité 12 / 22 / 35 %. Pas de dégradé, pas de flou, pas de tramage décoratif [A6-H].
   - (c) **Bassin de lumière sur le mur** : 2 tuiles « éclairées » par biome, avec les arêtes tournées vers la source montées d'un cran (`s` → `m`, `m` → `l`) dans un rayon de 1 tuile. La flamme éclaire ce qu'elle touche [C15-D].

| Source | Émissif | Halo | Animation |
|---|---|---|---|
| Torche à flamme froide (Crypte, Fonderie) | `W p l` + contour `m` | `l` | 6 images, 90 ms, boucle |
| Cristal (Jardin) | `W F f` + contour `v` | `f` | Cycle de palette 4 états, 250 ms [E7-H] |
| Laser (préavis, tir) | `W Z z` + contour `X` | `z` | Voir §8 |
| Écho | `W e c` + contour `q` | `c` | Scintillement 4 images |
| Or | `y G` + contour `o` (l'ombre de l'or) | `G` | Éclat 4-6 états, un à la fois [E2-H] |
| Marée | crête `J j` | `j` sur le bas d'écran | Cycle de palette 4 états |

   - **Les torches sont froides** (blanc-bleu) : la chaleur reste le privilège du héros et de l'or [A2 un seul accent saturé].
3. **Lumière de contour (rim light) du héros : 1 px, sans AA.**
   - Shader de CanvasItem : on teste l'alpha des 4 voisins (épaisseur de contour = 1 texel, cf. shader « 2D Rim Light » de godotshaders).
   - On **remplace** uniquement les pixels de contour `k` du côté de la source par une couleur de palette :
     - `z` près d'un laser en charge ;
     - `c` dans le halo d'un écho ;
     - `j` quand la marée est à moins d'un demi-écran.
   - Aucun pixel n'est ajouté hors de la silhouette, donc il n'y a jamais d'AA sale [A6-E « rim light avec parcimonie », A6-F].
4. **Light2D de Godot : autorisée seulement en P1** (optionnelle), avec :
   - le shader qui accroche `LIGHT_VERTEX`/`SHADOW_VERTEX` à la grille par `floor()` (doc Godot, « 2D lights and shadows ») ;
   - un filtre d'ombre `None` ;
   - une sortie postérisée en 3 paliers.
   - Le glow de `WorldEnvironment` est **interdit** : il floute et crée de l'AA hors palette.
5. **Ombre portée du héros sur le mur :** aucune. Le contour `k` suffit à 18 px, et une ombre doublerait la silhouette [A6-H doubles].

---

## 6. Profondeur : plans et parallaxe

La caméra ne monte que verticalement ; les vitesses sont donc des facteurs de défilement vertical.

| Plan | Contenu | Vitesse | Valeur Y | Saturation | Densité de détail |
|---|---|---|---|---|---|
| **P0 ciel / lointain** | Une grande forme par écran : voûte, vitrail éteint, ciel, aurore | **0,10** | 0,004-0,012 | S 40-56, teinte tirée vers le « ciel » du biome | Minimale : silhouettes, pas de contour interne |
| **P1 architecture moyenne** | Arches, colonnes, cuves, cloches, étagères | **0,30** | 0,008-0,020 | Moyenne | Formes moyennes, 1 détail par module |
| **P2 paroi du puits** | Briques et modules 32×16 ou 32×32, fenêtres, niches, chaînes | **0,60** | 0,012-0,025 | Faible | Motif répétitif calme, **jamais de ligne horizontale continue** (elle se lirait comme un rayon) |
| **P3 jeu** | Murs de collision, pièges, héros, éclats, marée | **1,00** | Bandes du §4.2 | Pleine | Maximale |
| **P4 avant-plan** | Chaînes, poutres, feuilles, piliers en silhouette pure `k` | **1,40** | ≤ 0,004 | Nulle | Silhouette seule, aucune texture |

- Le passage d'un plan au suivant suit la perspective atmosphérique :
  - contraste, saturation et densité de détail baissent avec la distance ;
  - la teinte glisse vers celle du ciel (Pixelblog 62 de Slynyrd, guide Sprite-AI, §14).
- **P4 :** au plus 10 % de la surface d'écran, **uniquement dans les 18 px des murs** ou en passage bref (moins de 0,5 s à l'écran). Jamais au-dessus du puits pendant une séquence de pièges.
- **Pas de « gros pixels » sur les plans lointains** : contrairement aux montagnes de Celeste, on garde la grille 1:1 partout, car un mélange de tailles de pixel ferait amateur à ×6. La distance se lit par la simplification, pas par l'agrandissement.
- **Particules d'ambiance** (1-2 px, groupes de 2-3 [A5-9]) :
  - vitesse propre + parallaxe du plan où elles vivent (P1 ou P2) ;
  - jamais en `z`, `c` ni `G` (couleurs réservées) ;
  - au plus 12 à l'écran.
- Tailles d'export des plans :
  - P0 et P1 : **256×256**, bouclables verticalement, débordant de 38 px de chaque côté pour les écrans larges ;
  - P2 : tuiles.

---

## 7. Biomes (6 étages)

**Aucun GDD n'existait au moment de la rédaction** (`studio/GDD.md` absent). Les biomes ci-dessous sont une proposition DA.
- Leur ordre et leurs noms s'alignent sur le GDD dès qu'il paraît.
- Les **règles** (même échelle de valeur, couleurs réservées) sont, elles, définitives.

Chaque biome livre :
- **8 tuiles de mur** de 16×16 : 4 de base qui se raccordent, 2 avec un détail, 1 rare, 1 de transition vers le biome suivant ;
- **2 tuiles éclairées** et **4 modules 16×32** ;
- 1 P0, 1 P1, 4 tuiles P2, 4 silhouettes P4 ;
- 2 particules d'ambiance et 1 source de lumière.

| # | Biome | Palette | Murs (détails des variantes) | Fond (P0 / P1 / P2) | Ambiance animée | Lumière | Piège signature |
|---|---|---|---|---|---|---|---|
| 1 | **Crypte des Échos** | `n s m l` / `b d`, mousse `v V` | Blocs taillés grand + 2 petits, rythme inversé, mousse sur les dessus, fissure en escalier, niche à reliquaire, rune éteinte (en `n`, **pas** en cyan) | P0 voûtes en ogive et vitrail éteint · P1 colonnes, chaînes, urnes · P2 briques 32×16 + niches | Poussière qui tombe (`n`, 1 px), flammes de cierges froides, toile qui ondule | Torches froides | Pics muraux |
| 2 | **Fonderie froide** | `1 2 3 4` / `( )` | Plaques d'acier rivetées (2 rivets, groupe de 2-3 [A5-9]), tuyaux verticaux, grille, givre sur les arêtes hautes (`p`) | P0 cuves éteintes géantes · P1 engrenages (rotation lente, 8 images à 4 fps), chaînes de levage · P2 tôles 32×32 | Vapeur gelée qui monte, givre qui scintille (`w`, un à la fois [E2-H]) | Torches froides, veilleuses `4` | Scies, lasers |
| 3 | **Bibliothèque engloutie** | `5 6 7 8` / `[ ]`, eau `0 9` | Étagères maçonnées, dos de livres (2 tons `6 7`, 1 dos `8` par groupe), coulures d'eau, coquillages | P0 nef noyée, colonnes sous l'eau · P1 rayonnages, pages en suspension · P2 pierre + ligne d'eau | Caustiques (cycle de palette `0 9`, 4 états, 200 ms [E7-H]), bulles, pages qui flottent | Lampes de lecture `8 p` | Lasers à travers l'eau (P2 : « pages-lames ») |
| 4 | **Jardin suspendu de cristal** | `B C D K` / `{ }`, végétal `v V f F` | Pierre mauve, lierre qui pend (sur les dessus puis coulure), racines, **cristaux émissifs** à facettes (un ton par facette, contour coloré [A5-8b]) | P0 terrasses suspendues en silhouette · P1 cristaux géants · P2 pierre + treillis | Lucioles `F` (2 px, jamais en `G`), feuilles qui tombent, cristaux qui pulsent | Cristaux | Ronces-épines (**en magenta**) |
| 5 | **Clocher des vents** | `L M N O` / `< >`, horizon `$`, cloches `v V f` | Pierre prune, poutres de fer `M N`, cordes `O`, meurtrières qui laissent voir le ciel | P0 crépuscule par les arches (`$` à l'horizon) · P1 grandes cloches vert-de-gris qui oscillent, rouages d'horloge · P2 pierre + abat-sons | Rafales (traits de 1 px `O`, 3 images), plumes, cloches | Ciel du couchant (P0 seulement) | Pendules-lames (P2) |
| 6 | **Sommet céleste** | `P Q S T` / `^ ~`, aurore `f F j J` | Marbre argenté, incrustations `T w` (**pas d'or** : l'or reste collectible), colonnes brisées | P0 ciel étoilé + aurore (cycle de palette lent, 8 états à 400 ms) · P1 constellations en forme d'échos · P2 dalles | Étoiles scintillantes (4-6 états, une à la fois [E2-H]), étoiles filantes | Étoiles, aurore | Lasers stellaires |

Transition entre biomes :
- une **arche de passage** de 180×32 sur le plan P3 ;
- les 2 dernières tuiles de transition de chaque biome mélangent les deux pierres ;
- la teinte de fond glisse sur une hauteur d'1 écran ;
- le changement de biome est **une récompense** : jamais au milieu d'une séquence de pièges.

---

## 8. Personnage

### 8.1 Silhouette et identité
- **Silhouette :**
  - dôme de capuche lavande, à la lumière haut-gauche ;
  - ouverture de visage `b` avec **deux yeux `w` de 1×2** ;
  - écharpe corail dont le bord haut fait la ligne du menton [C17-D7] ;
  - un bras levé qui agrippe ;
  - deux jambes séparées par un **vide utile** [A4b].
- **Marqueurs d'identité [C10-I] :** forme forte (dôme), couleur dominante (corail), asymétrie (bras levé + queue d'écharpe d'un seul côté).
  - Test : la silhouette pleine doit se reconnaître sur un fond clair, à ×1 [A6-J silhouette].
- **Construction [C14] :** corps nu d'abord (2 têtes), puis la couche cape, puis l'écharpe.
- **Écharpe [C17-D7] :**
  - tore autour du cou, plis en hamac ;
  - queue de 2 px de large et de **5 à 8 px** de long selon la vitesse ;
  - frange de 2 px ;
  - suite de mouvement **1 à 3 images en retard** sur le corps [E1] ;
  - jamais plus de 8 px hors du corps (limite de la cellule).
- **Pose de repos « ressort chargé » :** accroupi contre le mur, bras levé. L'**anticipation est déjà contenue dans l'idle**.
  - Au tap, on passe directement à l'étirement : le jeu ne doit jamais retarder l'entrée du joueur.
  - Exception assumée à « l'anticipation prend plus d'images que l'action » [E1], qui reste vraie pour tout ce qui n'est pas une commande du joueur.

### 8.2 Liste des animations (cellule 32×32, bandes horizontales, pivot (16,27))
Les durées sont par image. 12 fps de base ≈ 83 ms [E2-A] ; les tenues valent 3-4 fois la durée de base.

| Fichier | Images | Durées (ms) | Principes |
|---|---|---|---|
| `player_cling.png` (accroché, boucle) | 4 | 700 · 220 · 300 · 220 | Respiration de 1 px [C10-H], main fixe, retard de la queue d'écharpe [E2-I : 600 ms-1 s par état] |
| `player_slide.png` (glissade, boucle) | 4 | 90 ×4 | Bras qui frotte, écharpe vers le haut, + fx poussière |
| `player_jump.png` (impulsion, montée) | 3 | 50 · 70 · tenue | Img 1 étirement +3 px [E1 squash & stretch à volume constant], 2 groupé, 3 tenue de montée |
| `player_apex.png` | 2 | 100 · tenue | Lent au sommet [E2-B : 12, 8, 5, 3, 2], écharpe en suspens |
| `player_fall.png` (boucle) | 2 | 100 · 100 | Écharpe vers le haut, capuche gonflée |
| `player_turn.png` (demi-tour en l'air) | 4 | 40 · 33 (smear) · 50 · 60 | **Un seul smear** [E2-C], arc [E1], l'écharpe fait le tour une image après |
| `player_land.png` (impact sur le mur) | 3 | 60 (+ arrêt sur image de 50) · 70 · 90 | Écrasement de 2 px, rebond, retour à l'idle [E7-F] |
| `player_death.png` | 8 | 33 · 100 · 60 · 60 · 80 · 80 · 100 · 120 | 1 flash `W` [E7-F flash], 2 arrêt sur image (pose figée, contour `z`), 3 fêlures cyan, 4-6 éclatement en volutes du clair au sombre [E7-G], 7-8 effacement par morceaux, 1 px |
| `player_respawn.png` | 6 | 60 · 60 · 50 · 50 · 70 · 120 | Particules d'écho qui convergent, pop 50 % → 115 % → écrasé → final [E2-G], les couleurs reviennent de l'écharpe vers la cape |
| `player_victory.png` | 8 | 80 ×5 · 300 · 80 · 400 | Saut, bras levés, écharpe en grand arc, tenues finales |
| `player_idle_look.png` (variation rare) | 6 | 120 · 120 · 600 · 120 · 120 · 400 | Regard vers le haut (le sommet) ; joué une fois toutes les 6-9 s |
| `player_floor.png` (dalle de départ) | 4 | 600 · 150 · 600 · 150 | Debout, écharpe au vent |

- **Feuille de timing obligatoire avant tout dessin** [règle 26, E3], sous la forme : Image | Rôle | Ce qui change | Principe | Durée.
- Exemple validé : `art_tests/hero_idle.txt`. Son en-tête contient sa feuille de timing.

### 8.3 Écho (fantôme)
- Même silhouette que le héros, rendue entièrement dans la rampe écho :
  - **contour `q` coloré** (émissif [C15-D]) ;
  - corps `t`, lumière `c`, yeux `e`.
- `echo_ghost.png` : 4 images à 150 ms, flottement de 1 px et ondulation de l'écharpe.
- Il ne porte **aucun corail** : l'écho a perdu sa chaleur. C'est l'histoire du jeu racontée par la palette.

---

## 9. Pièges et effets

### 9.1 Grammaire du danger (non négociable)
1. **Forme :** le danger est fait de triangles, de dents et de pointes [A4b]. L'inoffensif est fait de courbes et de pointes émoussées.
2. **Couleur :** uniquement `x X z Z` (+ `k`, + 1 gris métal `m`/`l` pour les fixations). Rien d'autre dans le jeu n'est magenta.
3. **Émission :** tout piège actif a un cœur `Z`/`W` et une pulsation. Tout piège mobile ou intermittent a un **préavis** :
   - rampe éteint (`X` sombre) → lueur (`z`) → pic (`Z`, `W`, 1 image) → actif [E2-F] ;
   - **au moins 450 ms** de préavis en jeu (3-4 images tenues) ;
   - le préavis visuel commence toujours **avant** le danger effectif.
4. **Contour :** `k` plein sur les pièges, pour les rendre plus lisibles que tout le décor [A6-C : tout ou rien].
5. **Détail :** une seule idée par piège, au niveau de [A3] 16 px (pics, laser) ou 32 px (scie : 3-4 tons, contour sélectif autorisé à l'intérieur, 1-2 détails : moyeu et boulons).

### 9.2 Version « gravée » (piège neutralisé par un écho)
- **Échange de palette** : `x → q`, `X → t`, `z → c`, `Z → e`.
- **Contour `k` → `q`** : il recule dans la lisibilité, puisqu'il n'est plus une menace [A2 budget].
- Les pointes sont **émoussées d'1 px** : la forme cesse d'être un triangle.
- **Glyphe gravé** : sceau de l'écho, 3×3 à 5×5, en `e`.
- **Plus de pulsation ni de halo.** Un éclat lent (4-6 états, une fois toutes les 2-3 s [E2-H]).
- Animation de gravure, `fx_engrave.png` 32×32, 7 images :
  1. l'écho frappe ;
  2. flash `W` (33 ms) ;
  3. vague cyan qui parcourt le piège du point d'impact vers l'extérieur (3 images) ;
  4. le sceau apparaît (pop [E2-G]) ;
  5. retour au repos.
  - Total ≈ 520 ms.

### 9.3 Spécifications par piège

| Piège | Taille | Images | Animation |
|---|---|---|---|
| Pics muraux | 16×16, 6 px de profondeur, raccord vertical | 1 + 4 (éclat qui court le long des pointes) | Éclat toutes les 2 s |
| Pics rétractables | 16×16 | 7 : préavis 3 (fente qui rougeoie `X → z → Z`) · sortie 2 · rentrée 2 | 150 ms de préavis par image, 40 ms en sortie |
| Scie | 32×32, Ø24, 8 dents triangulaires, moyeu `m l` + 2 boulons | 4 (pas de 1/8 de tour : la symétrie à 8 dents boucle en 4) | 50 ms, plus étincelles `fx_saw_sparks` au contact d'un rail |
| Rail de scie | 16×16 × 3 (bout, milieu, coin) | 1 | |
| Émetteur laser | 16×32, bouche à droite, lentille | 9 : éteint 1 · charge 4 (rampe d'émission) · tir 2 (boucle) · refroidissement 2 | Charge 4 × 120 ms = 480 ms de préavis |
| Rayon | segment 8×16 | 5 : préavis 2 (ligne pointillée de 1 px `z`, clignote) · actif 3 (5 px : bords `X`, `z`, cœur `Z`/`W`) | 60 ms ; impact `beam_cap` 16×16 × 3 sur le mur d'en face |
| Presse (Fonderie, P2) | 32×32 | 6 | Préavis de 2 images de tremblement de 1 px |
| Pendule-lame (Clocher, P2) | 32×48 | 8 (arc) | Smear d'1 image au point bas |

### 9.4 Effets de jeu

| FX | Taille × images | Règle |
|---|---|---|
| Poussière de glissade | 16×16 × 4 | Couleur `p`/`l` du biome, 1-2 px, groupes de 2-3 [A5-9] |
| Bouffée de saut | 16×16 × 4 | Du clair au sombre, effacement par morceaux [E7-G] |
| Impact sur le mur | 16×16 × 4 | 1 image de flash `w`, puis éclats |
| Étincelle de demi-tour | 16×16 × 3 | Corail `a`/`A` (c'est le héros) |
| Ramassage d'éclat | 16×16 × 5 | Pop [E2-G] + 4 étincelles `y` |
| Traînée d'écho | 8×8 × 4 | Particules `c e` |

---

## 10. Interface

- **Même grille de pixels que le jeu.** L'UI est rendue dans le viewport de 180 px : pas de police ni d'icônes vectorielles, pas de ×2 qui mélangerait les tailles de pixel.
- **Matière :** les cadres sont **de la pierre de la tour**, pas des rectangles plats.
  - `panel.png` 24×24 en 9-slice, marges 8 :
    - fond `d` ;
    - bord en pierre taillée `n s m` avec arête `l` en haut à gauche ;
    - **coins en sceaux d'écho** `t` ;
    - contour `k`.
  - `panel_echo.png` pour la mort, la fin et l'offre de vidéo : bord `q t c`.
- **Boutons** : au moins 24 px de haut (48 dp), 9-slice 48×24 × 2 images (normal, enfoncé : -2 px et ombre réduite).
  - **Principal** ambre `R o a`, contour `k`. L'action porte la couleur du héros : agir, c'est lui.
  - **Secondaire** en pierre `n s m`.
  - **Vidéo récompensée** cyan `q t c e` avec l'icône écho. La seconde chance *est* un écho, donc la monétisation est expliquée par le monde.
- **Polices :**
  - `font_s` : cellule 6×10, capitales de 5×7 (existante, à reprendre avec accents complets) ;
  - `font_l` : **cellule 10×16**, chiffres et capitales pour le score, la hauteur et les titres. Dessinée exprès, **jamais un ×2 de `font_s`** ;
  - variante `_outline` avec contour `k` de 1 px pour tout texte posé sur le jeu.
- **Icônes :**
  - HUD en 12×12, 5 couleurs, contour `k`, lisibles à ×1 sur `b` [B5] ;
  - boutons en 16×16 ;
  - même lumière haut-gauche.
- **HUD :** bande haute de 20 px (zone sûre) avec, de gauche à droite :
  - pause ;
  - **4 lanternes de vie** (lanterne chaude allumée, puis lanterne écho éteinte) ;
  - hauteur en `font_l` ;
  - éclats.
  - Rien d'autre en partie, rien au centre du puits.
- **Tutoriel :** bandeau en bas d'écran (zone sûre + 40 px), jamais au milieu du puits ; la main `tap.png` (32×32 × 2 images) est posée sur le mur.
- **Animations d'écran :**
  - **pas de mise à l'échelle fractionnaire** du pixel art ;
  - les panneaux **glissent** au pixel entier selon un espacement amorti de 12, 8, 5, 3, 2 px [E2-B], avec un dépassement de 2 px [E2-B] (250-350 ms, [E2-A] UI 200-500 ms) ;
  - le pop d'un bouton ou d'une récompense est dessiné en images (50 % → 115 % → écrasé → final [E2-G]), pas calculé ;
  - le compteur d'éclats défile ;
  - les éclats ramassés volent vers le HUD.
- **Logo** `logo.png`, 160×48 :
  - « ÉCHO » en pierre taillée `n s m l` ;
  - un double décalé en écho `t c` qui se détache en 6 images (300 ms en boucle toutes les 4 s) ;
  - l'accent du É est l'écharpe corail.
- **Écran-titre :** scène en vrai pixel du héros accroché au pied de la tour, la marée en bas, le titre en haut, tous les plans P0-P4 du biome 1.

---

## 11. Liste complète des assets, en 10 familles (une par pixel artist)

Rappels :
- toutes les bandes sont horizontales [E8-A] et les cellules sont des multiples de 8 [E8-B] ;
- sources dans `art/src/<famille>/*.txt`, sorties dans `game/assets/<famille>/`, @8 et planches dans `art/out/<famille>/` ;
- P0 = indispensable au vertical slice (biome 1 complet), P1 = lancement, P2 = après le lancement ou si le GDD le retient.

### F1 Héros : artiste « personnage »

| Fichier | Taille | Images | Animation | Prio |
|---|---|---|---|---|
| `player_cling.png` | 128×32 | 4 | idle accroché, boucle | P0 |
| `player_slide.png` | 128×32 | 4 | glissade, boucle | P0 |
| `player_jump.png` | 96×32 | 3 | impulsion et montée | P0 |
| `player_apex.png` | 64×32 | 2 | sommet | P0 |
| `player_fall.png` | 64×32 | 2 | chute, boucle | P0 |
| `player_turn.png` | 128×32 | 4 | demi-tour en l'air (1 smear) | P0 |
| `player_land.png` | 96×32 | 3 | impact sur le mur | P0 |
| `player_death.png` | 256×32 | 8 | mort | P0 |
| `player_respawn.png` | 192×32 | 6 | réapparition | P0 |
| `player_floor.png` | 128×32 | 4 | idle sur la dalle | P1 |
| `player_victory.png` | 256×32 | 8 | victoire | P1 |
| `player_idle_look.png` | 192×32 | 6 | variation d'idle | P2 |

### F2 Écho et mort : artiste « FX émissifs »

| Fichier | Taille | Images | Animation | Prio |
|---|---|---|---|---|
| `echo_ghost.png` | 128×32 | 4 | flottement | P0 |
| `echo_dash.png` | 128×32 | 4 | l'écho fonce vers le piège | P0 |
| `fx_engrave.png` | 224×32 | 7 | gravure du piège | P0 |
| `grave.png` | 64×16 | 4 | sceau qui scintille | P1 |
| `fx_echo_trail.png` | 32×8 | 4 | traînée | P1 |
| `fx_death_burst.png` | 192×32 | 6 | volutes séparées, si le moteur les détache du corps | P1 |

### F3 Pièges : artiste « objets mécaniques »

| Fichier | Taille | Images | Animation | Prio |
|---|---|---|---|---|
| `spikes.png` / `spikes_echo.png` | 80×16 / 16×16 | 5 / 1 | éclat | P0 |
| `saw.png` / `saw_echo.png` | 128×32 / 32×32 | 4 / 1 | rotation | P0 |
| `laser.png` / `laser_echo.png` | 144×32 / 16×32 | 9 / 1 | éteint, charge, tir, refroidissement | P0 |
| `beam.png` | 40×16 | 5 | préavis, actif | P0 |
| `beam_cap.png` | 48×16 | 3 | impact | P0 |
| `spikes_retract.png` / `_echo` | 112×16 / 16×16 | 7 / 1 | préavis, sortie, rentrée | P1 |
| `saw_rail.png` | 48×16 | 3 tuiles | — | P1 |
| `fx_saw_sparks.png` | 64×16 | 4 | étincelles | P1 |
| `crusher.png` / `_echo` | 192×32 / 32×32 | 6 / 1 | presse | P2 |
| `pendulum.png` / `_echo` | 256×48 / 32×48 | 8 / 1 | pendule | P2 |

### F4 Collectibles et FX de mouvement : artiste « FX gameplay »

| Fichier | Taille | Images | Animation | Prio |
|---|---|---|---|---|
| `shard.png` | 96×16 | 6 | rotation (écrasement en x) + éclat | P0 |
| `shard_pop.png` | 80×16 | 5 | ramassage | P0 |
| `fx_dust_wall.png` | 64×16 | 4 | poussière de glissade | P0 |
| `fx_jump_puff.png` | 64×16 | 4 | bouffée | P0 |
| `fx_land.png` | 64×16 | 4 | impact | P0 |
| `fx_turn.png` | 48×16 | 3 | étincelle corail | P1 |
| `shard_big.png` | 144×24 | 6 | gros éclat de palier | P1 |
| `tap.png` | 64×32 | 2 | main du tutoriel | P1 |

### F5 Marée de Silence : artiste « matières animées »

| Fichier | Taille | Images | Animation | Prio |
|---|---|---|---|---|
| `tide_crest.png` | 128×16 | 4 | crête + cycle de palette [E7-H] | P0 |
| `tide_body.png` | 32×32 | 1 | tuile (cycle de palette `u U` dans le shader) | P0 |
| `tide_glow.png` | 32×16 | 1 | halo en 3 paliers, additif | P0 |
| `tide_motes.png` | 32×8 | 4 | particules montantes | P1 |
| `tide_warning.png` | 64×16 | 2 | alerte au bord de l'écran | P1 |

### F6 Murs de jeu : artiste « tuiles » (Crypte en P0, puis un biome par lot)
Pour chaque biome `<b>` (crypte, fonderie, biblio, jardin, clocher, sommet) :

| Fichier | Taille | Images | Contenu | Prio |
|---|---|---|---|---|
| `wall_<b>_L.png` / `wall_<b>_R.png` | 128×16 | 8 tuiles | mur gauche et mur **droit dessiné à part** (lumière) | Crypte P0, autres P1 |
| `wall_<b>_lit_L/R.png` | 32×16 | 2 | tuiles éclairées par une source | Crypte P0 |
| `wall_<b>_deco_L/R.png` | 64×32 | 4 modules 16×32 | torche, niche, cristal… | Crypte P0 |
| `torch.png` | 96×16 | 6 | flamme froide | P0 |
| `floor_start.png` | 48×16 | 3 tuiles | dalle de départ | P0 |
| `plaque.png` | 32×12 | 1 | plaque de hauteur | P1 |
| `gate_<b>.png` | 180×32 | 1 | arche de transition | P1 |
| `crystal.png` | 64×16 | 4 | cristal pulsant | P1 |

### F7 Fonds et parallaxe : artiste « décor »
Pour chaque biome `<b>` (Crypte en P0, les autres en P1) :

| Fichier | Taille | Images | Contenu |
|---|---|---|---|
| `bg0_<b>.png` | 256×256 | 1 (+ cycle de palette pour le ciel et l'aurore) | P0 lointain, bouclable verticalement |
| `bg1_<b>.png` | 256×256 | 1 | P1 architecture, transparence |
| `bg2_<b>.png` | 128×32 | 4 tuiles 32×16/32×32 | paroi du puits |
| `bg2_<b>_deco.png` | 96×32 | 3 | fenêtre, niche, chaîne |
| `bg1_<b>_anim.png` | selon l'élément | 4-8 | engrenage, cloche, caustiques (P2 pour la Crypte) |

### F8 Avant-plan, lumière et ambiance : artiste « atmosphère »

| Fichier | Taille | Images | Animation | Prio |
|---|---|---|---|---|
| `halo_s/m/l.png` | 32 / 48 / 64 carrés | 1 | 3 paliers par couleur de source | P0 |
| `amb_<b>.png` | 48×8 | 2 particules × 3 images | particules d'ambiance du biome | Crypte P0, autres P1 |
| `fg_<b>.png` | 128×64 | 4 silhouettes 32×64 | avant-plan P4 | P1 |
| `shader_rim` (palette et réglages à valider) | — | — | lumière de contour du héros | P1 |

### F9 Interface système : artiste « UI »

| Fichier | Taille | Images | Animation | Prio |
|---|---|---|---|---|
| `font_s.png` + `.fnt` | cellule 6×10 | — | — | P0 |
| `font_l.png` + `.fnt` | cellule 10×16 | — | — | P0 |
| `font_*_outline` | — | — | variantes contour | P0 |
| `panel.png`, `panel_echo.png` | 24×24 | — | 9-slice | P0 |
| `btn_main.png`, `btn_alt.png`, `btn_echo.png` | 48×24 | 2 | normal, enfoncé | P0 |
| `icons12.png` | 264×12 | 22 icônes | liste v1 + lanterne éteinte | P0 |
| `icons16.png` | 160×16 | 10 icônes de bouton | — | P0 |
| `hud_bar.png` | 180×20 | 1 | 9-slice horizontal | P0 |
| `ui_lantern.png` | 48×12 | 4 | allumée → s'éteint en écho | P0 |
| `toggle.png`, `slider.png` | 32×16 / 64×8 | 2 | — | P1 |
| `banner_tuto.png` | 64×24 | 1 | 9-slice | P1 |
| `popup_reward.png` | 64×64 | 6 | pop | P1 |

### F10 Marque et méta : artiste « marque » (la DA relit chaque pixel)

| Fichier | Taille | Images | Animation | Prio |
|---|---|---|---|---|
| `logo.png` | 160×48 | 6 | détachement de l'écho | P0 |
| `icon.png` | 32×32 | 1 | — | P0 |
| `icon_48.png` | 48×48 | 1 | pour l'icône adaptative Android (export ×9 = 432) | P0 |
| `title_scene` | composition P0-P4 du biome 1 | — | — | P1 |
| Cadres de captures du store, 5 écrans ×6 | 1080×2400 | — | — | P1 |
| `splash.png` | 180×400 | 1 | — | P1 |

---

## 12. Procédure imposée et grille de critique

### 12.1 Procédure (chaque asset, chaque artiste, dans cet ordre)
1. **Intention** en une phrase : quoi, pour qui, quelle lecture en 0,2 s [B0, C0].
   - **Projection** : vue de face, pour tout le jeu [B0b].
2. **Silhouette** en un ton, à la taille finale, testée à ×1 sur `b` et sur `p` [A5-5, B3].
   - Pour un personnage ou un piège : 2 silhouettes alternatives, on garde la plus iconique [B3].
3. **Valeurs** en 3 gris : clair / moyen / sombre, placés selon la lumière haut-gauche. Test du plissement d'yeux [A2, A6-J].
4. **Couleurs** : choisir la rampe dans `palette_v2.txt`, **dans la bande de luminance du plan** (§4.2) [A5-7]. Budget et test « une couleur de moins » [A6-B].
5. **Lumière et matière** :
   - terminateur net, un ton par face, un seul reflet ;
   - occlusion dans les creux, ombre sous les surplombs ;
   - émissifs en ombrage inversé [A5-8, A5-8b, A6-E].
6. **Contour** :
   - pixel-perfect, courbes en escalier 5-3-2-1-1 ;
   - `k` pour le jeu, coloré pour les émissifs et les gravés [A5-6, A6-C, A6-D].
7. **Détails** :
   - une idée par tuile de 16 px ;
   - placement en tiers, groupes de 2-3 ;
   - la nature décide (la mousse sur les dessus, les fissures suivent la pierre) [A5-9, A4].
8. **Finition [A6]** :
   - chasse aux 7 défauts (doubles et L, escaliers irréguliers, banding, ombrage « coussin », pixels orphelins, bruit, tramage décoratif) [A6-H] ;
   - aucun AA sous 32 px [A5-10, A6-F].
9. **Animation** (si elle existe) :
   - feuille de timing écrite d'abord [E3, règle 26] ;
   - blocking en silhouette à 8-12 fps [E7-A] ;
   - puis le pipeline complet **image par image** [règle 27, E0 1-7] ;
   - couches dans l'ordre ref / ombre / arrière / corps / avant / fx / éclat / pivot [E6] ;
   - vérification par pelure d'oignon [E2-E].
10. **Contrôle** :
    - par image [E5-A], puis la séquence en boucle [E5-B] ;
    - `planche.py` [règle 25] ;
    - **mise en situation** dans une capture du jeu (fond P2 + mur + héros) [A6-J].
11. **Export** : cellule unique, pivot constant, bande horizontale [E8].
    - Le nom de fichier suit le tableau du §11.
    - L'en-tête du `.txt` contient l'intention, la feuille de timing, le budget couleurs et **le défaut corrigé** à la relecture.
12. **Revue** : 3 réussites + 3 améliorations [A5-11], puis la grille ci-dessous.

### 12.2 Grille de critique (remplie par l'artiste, puis par la DA)
Chaque critère est noté de 0 à 3 :
- 0 = absent ;
- 1 = insuffisant ;
- 2 = correct ;
- 3 = professionnel.

| # | Critère | Test | Réf. |
|---|---|---|---|
| 1 | Silhouette lisible et iconique | Planche : silhouette sur fond clair, à ×1 | A2, B3, C10-I |
| 2 | Valeurs : 3 masses claires, point d'intérêt le plus contrasté | Planche en gris, plissement d'yeux | A2, A6-J |
| 3 | Bande de luminance du plan respectée | Pipette sur 5 pixels | §4.2 |
| 4 | Palette : rampe correcte, couleurs réservées respectées, budget | « Une couleur de moins » | A3, A6-A, A6-B |
| 5 | Lumière haut-gauche cohérente, un reflet, terminateur net | Comparaison avec le héros de référence | A5-8, A6-E |
| 6 | Contour : hiérarchie, pas de double, `k` ou coloré à bon escient | ×4 | A5-6, A6-C |
| 7 | Propreté : 0 orphelin, 0 jaggy, 0 banding, 0 coussin, 0 AA sous 32 px | ×4, pixel par pixel | A6-H, A5-10 |
| 8 | Hiérarchie de détail (grand / moyen / petit), espace vide utile | ×1 | A4b, A5-9 |
| 9 | Lecture **en situation** à ×1 sur le fond du biome, avec le héros | Capture composée | A6-J |
| 10 | Animation : timing varié, tenues, principes (anticipation, suite de mouvement, arcs) | GIF à vitesse réelle | E1, E2 |
| 11 | Séquence : boucle sans saut, pas de jumeaux, smear unique | Lecture en boucle ×10 | E5-B, E2-C |
| 12 | Export : taille, pivot, nom, en-tête du `.txt` complet | Script + lecture | E8 |

Seuils :
- **Validé : au moins 28/36, aucun 0, et 3/3 obligatoires sur les critères 1, 2 et 9** pour tout asset P3 (jeu).
- Décors : critères 3 et 9 à 3/3.
- Entre 20 et 27 : une itération. Sous 20 : on recommence depuis la silhouette.

---

## 13. Planches d'essai (dans `studio/art_tests/`)

| Fichier | Contenu |
|---|---|
| `hero_idle.txt` → `.png`, `@8.png`, `_planche.png` | Nouveau héros, 3 images d'idle accroché, cellule 32×32, 11 couleurs |
| `wall_crypte.txt` → `.png`, `@8`, `_planche` | 4 tuiles de mur gauche de la Crypte |
| `back_crypte.txt` → `.png` | Paroi P2 32×16 en 2 tons |
| `situation_v1_v2.png` | Même scène à ×4 : à gauche la v1 (192 px, assets actuels), à droite la v2 (180 px, palette v2) |

Ce que les planches ont montré et ce qui a été corrigé :
1. **Héros, version 1 :**
   - pointe de capuche de 1 px de large, qui se lisait comme une antenne (pixel isolé [A2]) : **remplacée par un dôme** ;
   - décrochement d'1 px dans le contour au niveau de l'œil : **aligné** ;
   - bras collé à la tête sans vide : **coude dégagé**.
2. **Héros, image 2 :** le décalage de la tête cassait l'épaule → contour retracé à la main, main fixe sur le mur (le point d'appui ne bouge pas).
3. **Mur, version 1 :**
   - arêtes `m` sur toute la largeur de chaque bloc, qui formaient une grille de lignes horizontales (lecture « laser », cf. la règle de la v1) : **arêtes raccourcies** (`l` puis `m` sur 3-5 px, puis `s`) ;
   - mousse de 2 px qui se lisait comme un pixel parasite : **coussin de 4 px + coulure**.
4. **Mise en situation :**
   - le héros v2 se repère immédiatement, le mur se sépare du fond, l'écharpe est le seul point chaud ;
   - en v1, le héros se perd dans la texture.
5. **Défauts restants, à traiter par les artistes F1 et F6 :**
   - le dôme de capuche est trop régulier : casser par un pli et une ombre de bord [A4 « pas de symétrie »] ;
   - la queue d'écharpe est encore raide : ajouter un pli en hamac [C17-D7] ;
   - le reflet `l` au coin de chaque bloc fait des points qui se répètent : ne le garder que sur 1 bloc sur 3 [A6-E « un reflet »] ;
   - la paroi P2 est trop régulière : ajouter les modules fenêtre, niche et chaîne et casser le rythme.

---

## 14. Références étudiées et ce qu'on en retient

| Jeu ou source | Ce qu'on prend | Source |
|---|---|---|
| **Downwell** | Code couleur radical (3-4 couleurs : joueur, danger, collectible), pixels ×3-4, puits central. D'où nos **couleurs réservées** | [liighteffog : « Downwell packs a lot into few pixels »](https://liighteffog.blogspot.com/2017/11/downwell-packs-lot-into-few-pixels.html), [Wikiwand Downwell](https://www.wikiwand.com/en/Downwell) |
| **Celeste** | L'**état de jeu se lit sur le personnage** (cheveux rouges = dash prêt, bleus = utilisé). Piste P2 : l'écharpe raccourcit d'un cran à chaque vie perdue (couche séparée [E6]) | [Celeste Wiki, Madeline](https://celestegame.fandom.com/wiki/Madeline) |
| Plans lointains (Celeste, Katana Zero) | Perspective atmosphérique : moins de contraste, de saturation et de détail avec la distance, teinte vers le ciel. **Pas** les gros pixels | [Slynyrd Pixelblog 62](https://www.slynyrd.com/blog/2026/5/27/pixelblog-62-landscape-backgrounds), [Sprite-AI, fonds](https://www.sprite-ai.art/blog/pixel-art-backgrounds), [Godot Forums 31996](https://godotforums.org/d/31996-are-these-backgrounds-too-much) |
| Parallaxe et gameplay | Aucun objet de collision en parallaxe | [Wayline, pièges du parallaxe](https://www.wayline.io/blog/parallax-scrolling-game-development-pitfalls) |
| Résolution mobile | Base qui divise la résolution physique ; 180×400 ×6 = 1080×2400 | [Forum Godot 94804](https://forum.godotengine.org/t/what-are-the-right-resolution-aspect-mode-and-scaling-for-pixel-art-games-for-mobile/94804), [Lunar Chippy devlog](https://lunar-chippy.itch.io/iron-village-prototype/devlog/705894/diary-11-so-you-want-a-resolution), [Bugnet](https://bugnet.io/blog/choosing-a-pixel-art-resolution-for-your-game), [Ziva, calculateur](https://ziva.sh/tools/pixel-perfect-resolution-calculator) |
| Lumière Godot | Accroche de `LIGHT_VERTEX` par `floor()`, filtre d'ombre None, rim light à 1 texel, glow recoloré | [Godot docs, 2D lights and shadows](https://docs.godotengine.org/en/stable/tutorials/2d/2d_lights_and_shadows.html), [godotshaders 2D Rim Light](https://godotshaders.com/shader/2d-rim-light/), [godotshaders Glow 2D](https://godotshaders.com/shader/glow-effect-2d/) |
| Leap Day (Nitrome) | Tour verticale à une touche : pièges très lisibles, une palette par jour (ici, par biome) | Connaissance générale, non revérifiée en ligne |
| Dead Cells | Silhouettes nettes, FX saturés sur fonds désaturés, lumière de contour sur les personnages | Connaissance générale |
| Blasphemous | Fonds sombres et denses, gameplay éclairé, morts très animées (la mort comme récompense de polish) | Connaissance générale |
| Hyper Light Drifter | Palette courte et très teintée (magenta et cyan), brume en plans | Connaissance générale |
| Owlboy | Parallaxe riche, lumière peinte, animation souple | Connaissance générale |
| Sword & Sworcery | Formes basse résolution, atmosphère par la silhouette d'avant-plan et la lumière | Connaissance générale |

Les palettes Lospec n'ont pas été consultées. La palette v2 a été construite et vérifiée par calcul (teinte, saturation, luminance, ratios de contraste), selon [A6-A].

---

## 15. Résumé pour le lead

- **Résolution :**
  - base 180×320, aspect « expand », échelle entière (1080×2400 → ×6 = 180×400 exact) ;
  - puits fixe de 144 px, le surplus va dans les murs ;
  - zones sûres de 20 px en haut et 24 px en bas ;
  - vitesse horizontale ×0,9.
- **Tailles :**
  - héros en cellule 32×32 (silhouette 18×21, classe 20-24 px de [C10], 11 couleurs), pivot (16,27) ;
  - tuile de mur 16×16 ; modules 16×32 ; paroi de fond 32×16 ;
  - scie Ø24 ; boutons d'au moins 24 px de haut.
- **Palette v2 :**
  - 71 couleurs, superset compatible de la v1, rampes à 10-20° de décalage de teinte ;
  - bandes de luminance par plan (fond Y < 0,03, murs 0,03-0,13, acteurs > 0,25) ;
  - couleurs réservées : corail = héros, magenta = danger, cyan = écho, or = collectible, violet = marée ;
  - 6 rampes de biome à même échelle de valeur.
- **Lumière :** haut-gauche, sources peintes (émissif + halo additif en paliers + tuiles éclairées), lumière de contour de 1 px par shader, pas de glow WorldEnvironment.
- **Profondeur :** 5 plans P0-P4 à 0,10 / 0,30 / 0,60 / 1,00 / 1,40.
- **Biomes :** Crypte, Fonderie froide, Bibliothèque engloutie, Jardin de cristal, Clocher des vents, Sommet céleste.
- **Familles d'assets (10) :** F1 Héros · F2 Écho et mort · F3 Pièges · F4 Collectibles et FX · F5 Marée · F6 Murs · F7 Fonds · F8 Ambiance et lumière · F9 UI · F10 Marque.
