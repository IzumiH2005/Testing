# ÉCHO : bible artistique v2

Auteur : direction artistique pixel art. Statut : **référence opposable** pour tous les pixel artists.
Elle remplace `art/ART_SPEC.md` partout où les deux diffèrent.

**Ce que tout le monde doit lire :**
- la méthode `METHODE_PIXEL_ART` : règles impératives 1-30 et parties A (lisibilité, pipeline, finition), B (objets), C (personnages) et E (animation). Chaque décision ci-dessous cite sa section entre crochets, par exemple [A2], [C10] ou [E2-F] ;
- `studio/palette_v2.txt` : la palette unique ;
- `studio/art_tests/` : planches d'essai et mise en situation.

Toute décision a sa raison en une ligne. Si un asset contredit cette bible, c'est l'asset qui est faux.
Pour contester une règle, il faut une planche en situation qui prouve le contraire [A6-J « en situation »].

**Alignement avec `studio/GDD.md` v1.0.** La bible suit le GDD pour tout ce qui touche au gameplay : couloir de 128 px, hitbox, dimensions létales, 22 obstacles, biomes, boss, tenues. Elle ne fixe que leur dessin. Les points où la DA demande un changement au GDD sont listés au §15, pour arbitrage par le lead.

---

## 0. Décisions en un coup d'œil

| Sujet | v1 (prototype) | v2 (décision) | Raison |
|---|---|---|---|
| Écran logique | 192×352 (GDD : « ×3 sur 1080p », en réalité ×5,625, non entier) | **largeur fixe 180 px, hauteur 320 à 430 px** (« expand »), échelle entière | 1080/180 = ×6 exact. 192 donne ×5,625 (pixels inégaux) |
| Couloir jouable | 128 px (8 tuiles) entre les murs x 32 et 160 | **128 px conservés** (GDD) ; murs visibles de 26 px (180 = 26 + 128 + 26) | Aucun changement de physique ni de chunk ; seule la caméra se décale de 6 px |
| Héros | 16×16, silhouette 10×14 (GDD : visuel 8×12, hitbox 6×10) | **cellule 32×32, silhouette 18×21, hitbox du GDD 6×10 inchangée** | Classe 20-24 px de [C10]. À 16 px il manque yeux, mains et marge d'exagération |
| Tuile | 16×16 | **16×16** (mur) ; modules 32×16 et 32×32 (fond) | Règles de [A3] 16 px ; le module 2× du fond se lit comme plus lointain |
| Palette | 31 couleurs, une rampe « nuit » pour tout | **71 couleurs** en rampes à décalage de teinte, **bandes de luminance** par plan | Diagnostic n°1 : décor, murs et héros avaient la même valeur |
| Plans | 1 fond + murs | **5 plans** (P0 à P4) + particules | Profondeur inexistante en v1 |
| Lumière | aucune source | haut-gauche + sources émissives **peintes** + halos en paliers | [A5-8], [C15-D] |
| Biomes | 1 | **6** (B1-B6 du GDD) | Progression visuelle = récompense de la montée |

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
- **Le couloir jouable fait toujours 128 px** (8 tuiles, GDD §0), centré : x = 26 à 154 dans le viewport de 180.
- **Murs visibles de 26 px** : la colonne de tuile intérieure entière (16 px) + 10 px de la colonne extérieure (6 px rognés hors écran). Le monde garde ses murs en x 0→32 et 160→192 ; la caméra est décalée de 6 px.
- Toute largeur logique supplémentaire (195, 256) va dans **l'épaisseur des murs**, jamais dans le couloir. Le gameplay reste ainsi identique sur tous les appareils.
- La hauteur supplémentaire (320 → 430) sert à **voir plus haut** : on anticipe mieux les pièges.
- La caméra place le héros à 62 % de la hauteur, en partant du haut (GDD §0) : y = 248 sur une hauteur de 400.
- Zones sûres : **20 px en haut** (encoche, HUD) et **24 px en bas** (barre gestuelle). Aucun piège ni texte de tutoriel n'y entre.
- Mesures physiques à ×6 sur 1080×2400 :
  - le héros mesure 21 × 6 = 126 px physiques, soit 5,3 % de la hauteur (v1 : environ 3 %) ;
  - 1 px logique ≈ 2,2 dp. Une cible tactile de 48 dp vaut donc 22 px logiques, d'où des **boutons d'au moins 24 px de haut**.

### 2.4 Impact pour le code (à transmettre au lead)
- **Monde inchangé** : murs en x 0→32 et 160→192, chunks de 12 caractères, physique du GDD §2.2 intacte. Seuls changent la taille du viewport (180 de large, expand) et le décalage de caméra (x = 6).
- La ligne du GDD §0 « ×3 sur 1080p » est à remplacer par le tableau du §2.1 : 192×3 = 576, et 1080/192 = 5,625.
- **Accroche** : le centre du héros est à 6 px de la face du mur (GDD). Dans la cellule, le pivot x = 16 met donc la face du mur à x = 10 ; la main et le bord de cape débordent de 3 px sur le mur. Le héros est dessiné **au-dessus** des tuiles de mur.
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
  - En pose accrochée, la face du mur est à x = 10 de la cellule (6 px du pivot, GDD §0) et le bord de la silhouette à x = 7 : main et cape mordent 3 px sur le mur.
- **Hitbox : celle du GDD, 6×10, centrée sur le corps** (environ 12×16 sans capuche ni écharpe), soit environ 3 px de clémence par côté. Le GDD doit remplacer « visuel 8×12 » par « cellule 32×32, silhouette 18×21 » (§15).
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
| Épines (O1) | 16×16, profondeur 7 (GDD) | Triangle = danger [A4b] |
| Scie (O2, O4, O5) | cellule 24×24 : disque Ø12 (= hitbox r6) + dents jusqu'à Ø20 | Dents qui dépassent la hitbox : clémence visible (§9.1) |
| Scie orbitale (O7) | cellule 16×16 : disque Ø10 + dents jusqu'à Ø16 | Hitbox r5 du GDD |
| Émetteur laser (O8) | 8×8 (GDD) | Bouche dans la pierre |
| Faisceau | segment 16×8, 3 px utiles + bords `X` | |
| Éclat d'or | cellule 8×8, gemme 6×6 (GDD) ; grand éclat 10×10 dans 16×16 | Catégorie + 1 détail [A4b] |
| Phalène, grignon | cellule 16×16, visuel 12×10 | Hitbox du GDD au cœur |
| Bulle de power-up | 12×12 dans 16×16 | Contour `G` (GDD) |
| Pictogrammes d'onboarding | 16×16 en `w` | GDD §11 |
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
| 1 Crypte des Veilleurs | `n s m l` | `b d` | indigo 244 → 210° |
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
| Lanterne de Veilleur (B1), veilleuse (B2) : flamme froide | `W p l` + contour `m` | `l` | 6 images, 90 ms, boucle |
| Cristal (Jardin) | `W F f` + contour `v` | `f` | Cycle de palette 4 états, 250 ms [E7-H] |
| Laser (préavis, tir) | `W Z z` + contour `X` | `z` | Voir §9 |
| Écho | `W e c` + contour `q` | `c` | Scintillement 4 images |
| Or | `y G` + contour `o` (l'ombre de l'or) | `G` | Éclat 4-6 états, un à la fois [E2-H] |
| Marée | crête `J j` | `j` sur le bas d'écran | Cycle de palette 4 états |

   - **Les lanternes et veilleuses sont froides** (blanc-bleu) : la chaleur reste le privilège du héros et de l'or [A2 un seul accent saturé].
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
6. **Obscurité (O16, B4) :** un masque en **3 paliers durs** autour du héros (rayon 72 px, 96 avec la Lanterne) : 100 % visible, puis 50 %, puis noir `k`. Pas de dégradé ni de dither [A6-H].
   - Restent dessinés au-dessus du masque : lueurs de 1 px `x` des pièges, `z` du préavis, cristaux et **tout ce qui est cyan** (GDD).
7. **Le shader de rim light passe en P0** : il sert aussi au halo `c` du Burin (§8.4).

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
- **P4 :** au plus 10 % de la surface d'écran, **uniquement dans les 26 px des murs** ou en passage bref (moins de 0,5 s à l'écran). Jamais au-dessus du puits pendant une séquence de pièges.
- **Pas de « gros pixels » sur les plans lointains** : contrairement aux montagnes de Celeste, on garde la grille 1:1 partout, car un mélange de tailles de pixel ferait amateur à ×6. La distance se lit par la simplification, pas par l'agrandissement.
- **Particules d'ambiance** (1-2 px, groupes de 2-3 [A5-9]) :
  - vitesse propre + parallaxe du plan où elles vivent (P1 ou P2) ;
  - jamais en `z`, `c` ni `G` (couleurs réservées) ;
  - au plus 12 à l'écran.
- Tailles d'export des plans :
  - P0 et P1 : **256×256**, bouclables verticalement, débordant de 38 px de chaque côté pour les écrans larges ;
  - P2 : tuiles.

---

## 7. Biomes (6 étages, alignés sur GDD §6)

Les noms, les altitudes, les obstacles et les mécaniques propres sont ceux du GDD §6. La DA fixe la matière, les fonds, l'ambiance et la lumière.
- Les **règles** sont définitives : même échelle de Y pour tous les murs, couleurs réservées [A2, C16-D].
- Priorités art : B1 à B3 en P0 (vertical slice et lancement), B4 et B5 en P1, B6 en P2 (GDD §4.2 et §7.1).

Chaque biome livre :
- **8 tuiles de mur** de 16×16 : 4 de base qui se raccordent, 2 avec un détail, 1 rare, 1 « brèche secrète » (GDD §5.4 : 3 px `l` plus clairs, rien d'autre) ;
- **2 tuiles éclairées**, **4 modules 16×32** et **2 tuiles de transition** vers le biome suivant (voir plus bas) ;
- 1 P0, 1 P1, 4 tuiles P2, 4 silhouettes P4 ;
- 2 particules d'ambiance, 1 source de lumière, 1 carte de titre.

| # | Biome (altitude, prio) | Palette | Murs (détails des variantes) | Fond (P0 / P1 / P2) | Ambiance animée | Lumière | Obstacles du GDD : matière DA |
|---|---|---|---|---|---|---|---|
| B1 | **Crypte des Veilleurs** (0-150 m, P0) | `n s m l` / `b d`, mousse `v V` | Blocs taillés grand + 2 petits, rythme inversé, mousse sur les dessus, fissure en escalier, niche à reliquaire, rune éteinte (en `n`, **pas** en cyan) | P0 voûtes en ogive et vitrail éteint · P1 **statues de Veilleurs portant une lanterne** (silhouette en `d`, lanterne froide `p` de 2 px), urnes · P2 briques 32×16 + niches | Poussière qui tombe (`n`, 1 px), flammes de cierges froides, toile qui ondule | Lanternes des statues (froides) | O1 épines, O2 scie, O4/O5 rails, O8 laser ; boss le Sonneur (cloche) |
| B2 | **Fonderie froide** (150-350 m, P0) | `1 2 3 4` / `( )` | Plaques d'acier rivetées (2 rivets, groupe de 2-3 [A5-9]), tuyaux verticaux, grille, **condensation** en gouttes `4` de 1 px | P0 cuves éteintes géantes · P1 engrenages (rotation lente, 8 images à 4 fps), chaînes de levage · P2 tôles 32×32 | Vapeur froide qui monte, gouttes qui perlent (une à la fois [E2-H]) | Veilleuses `4` | O3 contrefort (pierre du biome, arête `l`, épines `X`), O9 herse (fentes `x` permanentes), O10 mâchoires (blocs en acier `2 3` + mâchoire `X`), O11 plaque friable (liseré pointillé `4`, fissures en 3 états), O20 grignon |
| B3 | **Bibliothèque engloutie** (350-600 m, P0) | `5 6 7 8` / `[ ]`, eau `0 9` | Étagères maçonnées, dos de livres (2 tons `6 7`, 1 dos `8` par groupe), coulures d'eau, coquillages | P0 nef noyée, colonnes sous l'eau · P1 rayonnages, pages en suspension · P2 pierre + ligne d'eau | Caustiques (cycle de palette `0 9`, 4 états, 200 ms [E7-H]), bulles `p`, pages qui flottent | Lampes de lecture `8 p` | O18 eau (surface `9` ondulée de 1 px, fond `0`, bulles `p`), O6 lustre, O12 éboulis de livres, O19 phalène de papier |
| B4 | **Jardin suspendu de cristal** (600-900 m, P1) | `B C D K` / `{ }`, végétal `v V f F` | Pierre mauve, lierre qui pend (sur les dessus puis coulure), racines, cristaux de décor éteints (`v V` seulement) | P0 terrasses suspendues en silhouette · P1 cristaux géants · P2 pierre + treillis | Lucioles `F` (2 px, jamais en `G`), feuilles qui tombent | **Cristaux rebondissants** : seuls émissifs verts (`f F` + cœur `W`, contour `v`) | O17 cristal rebondissant, O16 obscurité, O7 scie orbitale, O19 phalènes |
| B5 | **Clocher des vents** (900-1250 m, P1) | `L M N O` / `< >`, horizon `$`, cloches de fond `v V f` | Pierre prune, poutres de fer `M N`, cordes `O`, meurtrières qui laissent voir le ciel | P0 crépuscule par les arches (`$` à l'horizon) · P1 grandes cloches vert-de-gris qui oscillent, rouages d'horloge · P2 pierre + abat-sons | Plumes, cloches de fond | Ciel du couchant (P0 seulement) | O15 vent (traits `O` de 1 px, fanions muraux), O21 sentinelle (gargouille en pierre du biome, œil `x` → `z`), O13 dalle à fléchettes, O6 cloche-pendule |
| B6 | **Sommet céleste** (1250 m et plus, P2) | `P Q S T` / `^ ~`, aurore `v V` | Marbre argenté, incrustations `T w` (**pas d'or** : l'or reste collectible), colonnes brisées | P0 ciel étoilé + aurore (rubans `v`, crête `V` de 1 px, cycle de palette lent, 8 états à 400 ms) · P1 constellations en forme d'échos · P2 dalles | Étoiles scintillantes (4-6 états, une à la fois [E2-H]), étoiles filantes | Étoiles, aurore | O14 givre (surface `p`, reflet `w` de 1 px, étoiles de givre), O12 glaçon, O22 l'Ombre ; boss le Silence |

Décisions qui précisent le GDD :
- **Masses de pendule (O6) dans la rampe danger.** Le lustre (12×12) et la cloche (16×16) tuent : ils sont en `x X z` avec un cœur `Z` ; la chaîne non létale reste en `m` (GDD §4.1 « tout ce qui tue est dans la rampe danger »). Les cloches vert-de-gris ne vivent qu'en P1.
- **Pas de givre décoratif en B2.** Le givre est l'obstacle O14 de B6. Un même signe ne doit avoir qu'un sens [C16-D] : la Fonderie a de la condensation `4`.
- **Obstacles non létaux** (friable, givre, cristal, vent, eau) : teintes du biome + un liseré propre à chacun, comme le veut le GDD §4.1. Aucun magenta, aucun cyan.
- **Aurore de B6 en `v V`, pas en `f`.** Le GDD demande `f` en plan lointain, mais `f` (Y 0,39) sort de la bande P0 (Y ≤ 0,012) et passe au-dessus des murs : elle volerait la lecture [A2]. `v` (Y 0,06) est déjà une exception à la bande, tolérée parce que les rubans sont fins et n'occupent pas plus de 15 % du ciel. **À valider en situation** [A6-J].

### 7.1 Transitions entre biomes (GDD §6 « Transitions »)
- **Salle d'autel de 96 px** (6 tuiles) au début de chaque biome :
  - autel 32×32 en pierre du nouveau biome ;
  - **flamme cyan** de 8×16, 6 images : c'est le seul « décor » cyan admis, car l'autel *est* un objet d'écho.
- **Murs de la salle : 2 tuiles de transition dessinées par paire de biomes, et non le dither 2×2 sur 32 px demandé par le GDD.**
  - Raison : le tramage décoratif est l'un des 7 défauts [A6-H]. À ×6, un damier 2×2 se lit comme un tissu et crée une troisième valeur qui sort des bandes de luminance (§4.2).
  - La tuile basse est la pierre A envahie par les joints de B ; la tuile haute est la pierre B avec un dernier bloc de A. La teinte du fond change en 2 crans durs, sans dégradé.
- **Carte de titre (1,5 s)** :
  - nom du biome en `font_l` capitales `w` contour `k` (le GDD dit « police 8 px » : à ×6, un titre se lit mieux en police de titre) ; altitude en `font_s` `G` ;
  - entrée et sortie en glissement au pixel entier 12, 8, 5, 3, 2 [E2-B], **sans fondu alpha** ; posée dans la zone sûre haute, jamais sur le couloir.
- Le changement de biome est **une récompense** : jamais au milieu d'une séquence de pièges (GDD : il suit une arène de boss).

### 7.2 Boss (GDD §7.1)
- **Règles communes :**
  - les **runes** 16×16 sont des tuiles murales : éteinte = pierre du biome avec une gravure en ton d'ombre ; allumée = `G y` contour `o` (l'or = ce qu'on vise) ;
  - la **porte de Silence** ferme le couloir derrière le héros : rampe `u U j`, crête `J` de 1 px, 4 images de fermeture ;
  - un boss « sonné » (1 s) : 1 image de flash `w`, puis tremblement de 1 px ;
  - un boss qui se brise : 8 images de volutes qui vont du clair au sombre [E7-G] et lâchent 20 éclats d'or ;
  - seule l'**attaque qui a tué** passe dans la rampe écho (GDD §3.4), par échange de palette.
- **Le Sonneur (B1, P0) :**
  - cloche 48×48 (masse létale Ø40 pour le rayon 20 du GDD) en `x X z`, battant `Z`, sur un joug 64×16 en pierre `n s m` ;
  - onde-laser : segments 16×8 bouclables, préavis 0,6 s en pointillé `z` qui clignote à 10 Hz, puis bande de 5 px `X z Z z X`.
- **Boss P1** (même grammaire) :
  - Forgeron-Automate : 64×64, bras-mâchoires `X`, marque `z` au mur ;
  - Mère-Phalène : 32×24 dans une cellule de 32×32 ;
  - Œil de cristal : 48×48, faisceau en préavis pointillé de 0,5 s ;
  - Girouette : flèche géante `O` de 64×24, non létale, donc en teintes du biome.
- **Le Silence (B6, P2)** : la marée elle-même, avec une crête plus haute de 8 px et l'écume `J` animée. Pas de nouveau sprite de corps.

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

### 8.3 Fantômes, fantôme-guide et l'Ombre : échanges de palette, pas de nouveaux dessins
- **Fantômes (GDD §3.2) :** les images du héros, recolorées en temps réel dans la rampe écho par un shader de palette :
  - `h H i I` → `q t c e`, écharpe `r R o a A` → `q t t c e`, contour `k` → `q` (contour coloré d'émissif [C15-D]), yeux `w` → `e` ;
  - opacité 50 % (GDD) : les mélanges hors palette que crée la transparence sont **tolérés ici seulement**, parce qu'un fantôme est par nature translucide [A6-F] ;
  - il ne porte **aucun corail** : l'écho a perdu sa chaleur. C'est l'histoire du jeu racontée par la palette.
- **Fantôme-guide** de l'onboarding (GDD §11) : le même échange, à 70 % d'opacité, suivi d'une traînée `fx_echo_trail`.
- **Éclat d'écho** (GDD §5.1, posé sur chaque point de mort) : sprite 8×8 en `c e` contour `q`, 4 images de scintillement.
- **L'Ombre (O22) :** les images du héros dans la rampe silence : corps `u U`, contour `j`, yeux `Z`, traînée `j` de 3 images.
  - Le GDD dit 8×12 ; on garde la silhouette du héros (18×21 dans 32×32) et sa hitbox 6×10. La lecture voulue est « c'est moi, en négatif » : elle exige la même silhouette [C10-I].
- Raison commune : un seul jeu d'images à dessiner pour quatre usages, et une identité qui reste parfaite d'un usage à l'autre [E8-A].

### 8.4 Écharpe en calque séparé, effets de power-up
- **Chaque animation du héros s'exporte en deux bandes :** `player_<anim>.png` (corps et cape) et `player_<anim>_scarf.png` (écharpe seule), même cellule, même pivot [E6 couches, E8-A]. Le code les superpose.
- Usages :
  - **Plume** (GDD §5.2) : une 2e écharpe décalée d'une image, en `a A` ;
  - **Lanterne** : flamme `A` de 4×6 au bout de l'écharpe, 4 images ;
  - **Élan d'or** : traînée `g G` derrière le héros (particules, pas de calque) ;
  - tenue 8 « Voyageur des vents » : écharpe longue de 4 px de plus, dessinée une fois ;
  - piste Celeste (§14) : écharpe raccourcie d'un cran par vie perdue.
- **Burin** : halo `c` de 1 px = le shader de rim light (§5.3) appliqué à **tout** le contour (`k` → `c`). Aucun pixel ajouté hors de la silhouette.
- **Accalmie** : la crête de la marée passe de `j` à `J` et cesse d'onduler (échange de palette sur `tide_crest`).

### 8.5 Tenues (GDD §9.3), teintes de cape et fantômes
- **Règle :** une tenue = un échange de la palette de cape `h H i I` + un accessoire de 2 à 4 px sur un calque à part. La silhouette ne change pas ; l'écharpe reste dans `r R o a A` (GDD).
- **Le ton de base de la cape a un Y d'au moins 0,25** : c'est la bande des acteurs (§4.2), sinon le héros se perd dans le mur. Aucune cape n'emploie une rampe réservée (danger, écho, or), sauf l'exception notée ci-dessous.
- Corrections DA aux couleurs du GDD :

| Tenue | GDD | DA | Raison |
|---|---|---|---|
| 4 Forgeron froid | cape `3` | cape `3 4 p` (ombre, base, lumière) | `3` a un Y de 0,13 : c'est la lumière d'un mur, le héros disparaîtrait |
| 17 Veilleur de cendre | cape `d` | cape `m l p` + braises `a` | `d` (Y 0,017) est la couleur du fond : silhouette perdue |
| 18 Silence apprivoisé | cape `U` | cape `U j J`, base `j` (Y 0,27) | `U` est trop sombre ; exception thématique à la réserve « marée », admise parce que c'est la tenue du niveau 50 et que la cape ne pulse pas |
| 13 Ombre polie | yeux `c` | yeux `w` | Le cyan signifie « écho, inoffensif » ; sur le héros il mentirait |
| 21 Sans-faute | cape `w` | ombre `p`, base `w`, lumière `W` | Une rampe de 3 tons pour garder le volume |

- **Les 8 teintes de cape** suivent la même règle : 4 tons pris dans les rampes de biome ou de décor, base à Y ≥ 0,25.
- Les fantômes d'un joueur en tenue gardent la silhouette de la tenue, mais toujours recolorée en cyan (§8.3).

---

## 9. Pièges, ennemis et effets (alignés sur GDD §3 à §5)

### 9.1 Grammaire du danger (non négociable)
1. **Forme :** le danger est fait de triangles, de dents et de pointes [A4b]. L'inoffensif est fait de courbes et de pointes émoussées.
2. **Couleur :** uniquement `x X z Z` (+ `k`, + 1 gris métal `m`/`l` pour les fixations). Rien d'autre dans le jeu n'est magenta (GDD §4.1).
3. **Émission :** tout piège actif a un cœur `Z`/`W`. Tout piège temporisé a un **préavis** :
   - le GDD fixe le code : clignotement `z` à 10 Hz, jamais moins de 0,25 s ;
   - la DA fixe le dessin : chaque piège a 3 états peints, **éteint** (`X` sombre), **lueur** (`z`) et **actif** (`Z`/`W`) [E2-F]. Pendant le préavis, le code alterne lueur et éteint à 10 Hz, puis affiche 1 image de pic `W`, puis l'état actif ;
   - recommandation DA : au moins **0,4 s** de préavis dans les chunks `intro` (la herse du GDD est à 0,3 s, voir §15).
4. **Contour :** `k` plein sur les pièges, pour les rendre plus lisibles que tout le décor [A6-C : tout ou rien].
5. **Clémence visible :** le **cœur** du sprite (moyeu, corps, bloc) a exactement la taille de la hitbox du GDD. Les dents, ailes et pointes **dépassent de 1 à 4 px**. Le joueur meurt donc de ce qu'il voit nettement toucher (GDD §0), et un frôlé se lit comme un frôlé.
6. **Détail :** une seule idée par piège, au niveau de [A3] 16 px.

### 9.2 Version « gravée »
- **Échange de palette** : `x → q`, `X → t`, `z → c`, `Z → e`. **Contour `k` → `q`** : un piège gravé recule dans la lisibilité, puisqu'il n'est plus une menace [A2 budget].
- Chaque piège létal a une image `_echo` dessinée, car le GDD change sa forme :
  - épines → cristal accrochable (pointes émoussées d'1 px) ;
  - herse → pointes figées sorties ;
  - mâchoires → blocs fermés en pont ;
  - laser → ligne cyan permanente ;
  - scies, pendules et ennemis → même sprite recoloré, qui continue de bouger.
- **Glyphe gravé** : sceau de l'écho, 3×3 à 5×5, en `e`. Plus de pulsation ni de halo : un éclat lent (4-6 états, une fois toutes les 2-3 s [E2-H]). La tenue 20 « Graveur » le fait durer 1 s de plus.
- **Séquence de gravure (GDD §3.3, 1,51 s) : ce qui est dessiné, ce qui est codé.**

| t (s) | GDD | Art livré | Code |
|---|---|---|---|
| 0,00 | Hitstop 0,18 s, flash `W`, secousse de 4 px | `player_death` image 1 (flash `W`) | Hitstop, secousse |
| 0,18 | Le héros se brise en 6 pixels corail | `player_death` images 2-8 (6 éclats `o a`, volutes du clair au sombre [E7-G]) | Gravité des éclats |
| 0,63 | Onde cyan de rayon 0 → 40 px | `fx_engrave_wave.png` 480×80, 6 images (anneau de 2 px `e` / `c` / `t`, qui s'amincit) | Placement au point d'impact |
| 0,63-1,33 | Recoloration de haut en bas en 0,7 s | — | Masque vertical + échange de palette du §9.2, ligne de front en `e` de 1 px |
| 1,33 | Icône du codex | `codex_icon` 16×16 du piège | Coin haut droit, 1 s |
| après | Sceau sur le piège | `fx_engrave_seal.png` 64×16, 4 images (pop 50 → 115 % → écrasé → final [E2-G]) | — |

### 9.3 Spécifications par obstacle (dimensions de gameplay du GDD §4.3)

| Id | Obstacle | Cellule | Dessin | Images | Préavis / animation |
|---|---|---|---|---|---|
| O1 | Épines | 16×16 | Profondeur 7 (GDD), dents `X`, pointes `z`, lueur `x` de 1 px sur le mur | 1 + 4 (éclat qui court) | Éclat toutes les 2 s |
| O2 | Scie fixe | 24×24 | Disque Ø12 (= hitbox r6) + **6 dents** jusqu'à Ø20, moyeu `Z` | **4** à 50 ms (le GDD dit 2 à 12 fps, voir §15) | Bourdonnement (son) |
| O3 | Contrefort à épines | 16×32 et 16×48 | Pierre du biome, face accrochable `l`, épines de 5 px dessus et dessous | 1 | — |
| O4 / O5 | Scie sur rail | 24×24 + rail 16×16 ×3 | Scie de O2, rail pointillé `x` (1 px sur 2) | 4 | — |
| O6 | Pendule | 16×16 / 12×12 | Cloche (B5) ou lustre (B3) en `x X z`, chaîne `m` de 48 px en tuiles 8×8 | 2 (reflet) | Smear d'1 image au point bas [E2-C] |
| O7 | Scie orbitale | 16×16, pivot 8×8 | Disque Ø10 + dents jusqu'à Ø16 ; pivot en métal `m l`, non létal ; orbite pointillée `x` | 4 | — |
| O8 | Laser | émetteur 8×8, segment de faisceau 16×8 | Bouche `X` dans la pierre ; faisceau de 3 px (`z Z z`) + bords `X` | Émetteur 3 états ; faisceau préavis 1 (pointillé `z`) + actif 3 | Préavis du GDD : 0,55 à 0,7 s |
| O9 | Herse | 24×32 | Fentes `x` permanentes ; pointes à 4 px (préavis) puis à 24 px | 5 : rentrée · préavis · sortie 2 · rentrée | Préavis 0,3 s |
| O10 | Mâchoires | blocs 16×24 bouclables | Bloc en métal du biome, mâchoire `X` à dents | 3 | Tremblement de 1 px + 3 pixels de poussière `p` |
| O11 | Plaque friable | 16×32 | Pierre du biome, liseré pointillé `4`, rivets ; non létale | 4 : intacte · fissure 1 · fissure 2 · chute (débris) | — |
| O12 | Éboulis | 16×16 (bloc 12×12) | Pile de livres `6 7 8` (B3) ou glaçon `p w` (B6) **avec contour `x` et marque `z`** | 1 + marque de départ 8×4 ×2 | Préavis 0,6 s (poussière + marque `z` de 2 px) |
| O13 | Dalle à fléchettes | 16×16, fléchette 8×2 | Bouche qui s'allume en `z`, fléchette `X Z` | Dalle 2, fléchette 2 | La dalle s'enfonce d'1 px |
| O14 | Givre | 16×16 bouclable | Surface `p`, reflet `w` de 1 px, étoiles de givre ; non létal | 1 + étoile 4 images | Étoiles toutes les 0,5 s |
| O15 | Vent | trait 16×4 | Traits `O` de 1 px, fanions muraux 8×8 | Trait 3, fanion 4 | Traits à 2 px par image (GDD) |
| O16 | Obscurité | masque | Voir §5.6 | — | — |
| O17 | Cristal rebondissant | 16×16 | `f F` + cœur `W`, contour `v` ; non létal | 4 (cycle de palette) + rebond 3 | — |
| O18 | Eau | 16×16 bouclable | Surface `9` ondulée de 1 px, fond `0`, bulles `p` | Surface 4, bulle 3 | Cycle de palette 200 ms |
| O19 | Phalène de papier | 16×16 (visuel 12×10, hitbox 8×6) | Papier en `X z`, ailes à dents, ombre `x` de 1 px | **2** (GDD) + virage 1 | Battement à 8 fps |
| O20 | Grignon | 16×16 (visuel 12×10) | Automate `X`, pattes, yeux `z` qui regardent dans le sens de marche | 4 (marche) | — |
| O21 | Sentinelle | 16×16, projectile 8×8 (6×6 utile) | Gargouille en **pierre du biome** (non létale), œil `x` → `z` ; projectile `z Z` | Gargouille 3 (repos, charge, tir), projectile 2 | Charge visible sur l'œil |
| O22 | L'Ombre | 32×32 | Voir §8.3 | celles du héros | Traînée `j` |

### 9.4 Éléments positifs (GDD §5)

| Élément | Cellule | Dessin | Images |
|---|---|---|---|
| Éclat | 8×8 (gemme 6×6) | `g G y`, contour `o` | 6 (rotation + éclat) |
| Grand éclat | 16×16 (gemme 10×10) | Idem, plus une facette `W` | 4 à 4 fps (GDD) |
| Éclat d'écho | 8×8 | `c e`, contour `q` | 4 |
| Bulle de power-up | 16×16 (bulle 12×12) | Contour `G` (GDD), icône 8×8 dedans | 4 (flottement d'1 px + reflet) |
| Plume dorée | 16×16 | `g G y`, contour `o` | 6 (balancement) |
| Fragment de relique | 8×8 | Pierre `m l` + cœur `G` | 4 |
| Porte de défi | 16×24 | Cadre doré `g G`, intérieur `k` | 4 (scintillement) |
| Alcôve | 32×48 | Niche dans la pierre du biome | 1 |
| Éclat de lune | 16×16 | `w W` + contour `l` | 4 |

### 9.5 Effets de jeu

| FX | Taille × images | Règle |
|---|---|---|
| Poussière de glissade | 16×16 × 4 | Couleur `p`/`l` du biome, 1-2 px, groupes de 2-3 [A5-9] |
| Bouffée de saut | 16×16 × 4 | Du clair au sombre, effacement par morceaux [E7-G] |
| Impact sur le mur | 16×16 × 4 | 1 image de flash `w`, puis éclats |
| Volte | 16×16 × 3 | `G y` en temps normal ; **`c e` quand la volte vient d'une recharge cyan** (le joueur voit d'où vient sa volte) |
| Frôlé | 16×16 × 3 | Étincelle `w` de 3 px, rien d'autre (GDD : « sans rien ajouter à l'écran ») |
| Ramassage d'éclat | 16×16 × 5 | Pop [E2-G] + 4 étincelles `y` |
| Aimant | 16×16 × 3 | Petits arcs `G` |
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
- **Onboarding (GDD §11) : aucune phrase.** Pictogrammes 16×16 en `w` contour `k` (main qui tape, main tenue + barre de 0,28 s, main + flèche courbe, losange cyan + flèche de volte), **posés sur le mur côté héros**, jamais sur le couloir. Ils pulsent en 2 images et s'effacent par morceaux [E7-G].
- **Codex :** chaque fiche montre les **sprites du jeu** (pas de nouveaux dessins) animés dans une fenêtre 48×48 en pierre, état normal puis gravé.
- **Cadres de partage** (6) : 180×320, pierre de biome, coins en sceaux ; aucun élément dans la zone de capture du texte.
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

## 11. Liste complète des assets, en 11 familles (une par pixel artist)

Rappels :
- toutes les bandes sont horizontales [E8-A] et les cellules sont des multiples de 8 [E8-B] ;
- sources dans `art/src/<famille>/*.txt`, sorties dans `game/assets/<famille>/`, @8 et planches dans `art/out/<famille>/` ;
- P0 = indispensable au vertical slice et aux biomes B1 à B3 (GDD P0) ; P1 = lancement (B4, B5, méta) ; P2 = après le lancement (B6) ;
- chaque piège létal a son `_echo` (§9.2), compté sur la même ligne.

### F1 Héros : artiste « personnage »
Chaque animation existe en deux bandes : `player_<anim>.png` et `player_<anim>_scarf.png` (§8.4).

| Fichier | Taille | Images | Animation | Prio |
|---|---|---|---|---|
| `player_cling` (+ `_scarf`) | 128×32 | 4 | idle accroché, boucle | P0 |
| `player_slide` (+ `_scarf`) | 128×32 | 4 | glissade, boucle | P0 |
| `player_jump` (+ `_scarf`) | 96×32 | 3 | impulsion et montée | P0 |
| `player_apex` (+ `_scarf`) | 64×32 | 2 | sommet | P0 |
| `player_fall` (+ `_scarf`) | 64×32 | 2 | chute, boucle | P0 |
| `player_turn` (+ `_scarf`) | 128×32 | 4 | volte (1 smear) | P0 |
| `player_land` (+ `_scarf`) | 96×32 | 3 | impact sur le mur | P0 |
| `player_death` | 256×32 | 8 | flash, éclatement en 6 pixels corail (GDD §3.3) | P0 |
| `player_respawn` (+ `_scarf`) | 192×32 | 6 | réapparition | P0 |
| `pal_ghost`, `pal_shadow` | 16×2 | — | tables d'échange de palette (fantôme, Ombre) | P0 |
| `player_floor` (+ `_scarf`) | 128×32 | 4 | idle sur la dalle | P1 |
| `player_victory` (+ `_scarf`) | 256×32 | 8 | victoire | P1 |
| `outfit_<n>_acc` + `pal_outfit_<n>` | 32×32 par animation concernée | — | tenues 1-16 (P1), 17-24 (P2) | P1 |
| `pal_cape_<n>` | 4×1 | — | 8 teintes de cape | P1 |
| `player_idle_look` (+ `_scarf`) | 192×32 | 6 | variation d'idle | P2 |

### F2 Écho et gravure : artiste « FX émissifs »

| Fichier | Taille | Images | Animation | Prio |
|---|---|---|---|---|
| `fx_engrave_wave.png` | 480×80 | 6 | onde de gravure, rayon 0 → 40 | P0 |
| `fx_engrave_seal.png` | 64×16 | 4 | pop du sceau | P0 |
| `echo_shard.png` | 32×8 | 4 | éclat d'écho au point de mort | P0 |
| `fx_echo_recharge.png` | 64×16 | 4 | contact cyan : la volte se recharge | P0 |
| `fx_echo_trail.png` | 32×8 | 4 | traînée du fantôme-guide | P0 |
| `grave.png` | 64×16 | 4 | sceau gravé qui scintille | P1 |
| `fx_death_burst.png` | 192×32 | 6 | volutes séparées du corps, si le moteur les détache | P1 |

### F3 Pièges : artiste « objets mécaniques »

| Fichier | Taille | Images | Animation | Prio |
|---|---|---|---|---|
| `spikes` / `_echo` (O1) | 80×16 / 16×16 | 5 / 1 | éclat | P0 |
| `saw` / `_echo` (O2, O4, O5) | 96×24 / 24×24 | 4 / 1 | rotation | P0 |
| `saw_rail.png` | 48×16 | 3 tuiles | rail pointillé | P0 |
| `laser` / `_echo` (O8) | 24×8 / 8×8 | 3 / 1 | éteint, lueur, actif | P0 |
| `beam` / `_echo` | 64×8 / 16×8 | 4 / 1 | préavis 1, actif 3 | P0 |
| `buttress` / `_echo` (O3) | 32×48 | 2 / — | hauteurs 32 et 48 | P0 |
| `portcullis` / `_echo` (O9) | 120×32 / 24×32 | 5 / 1 | rentrée, préavis, sortie | P0 |
| `jaws` / `_echo` (O10) | 48×24 / 16×24 | 3 / 1 | tremblement, fermeture | P0 |
| `crumble.png` (O11) | 64×32 | 4 | fissures, chute | P0 |
| `rockfall_books` / `_echo` (O12) | 16×16 / 16×16 | 1 / 1 | + `rockfall_mark` 16×4 ×2 | P0 |
| `pendulum_chandelier` / `_echo` (O6) | 32×16 / 16×16 | 2 / 1 | + `chain.png` 8×8 | P0 |
| `pendulum_bell` / `_echo` (O6) | 32×16 / 16×16 | 2 / 1 | — | P1 |
| `orbit_saw` / `_echo` + `orbit_pivot` (O7) | 64×16 / 16×16 + 8×8 | 4 / 1 + 1 | rotation | P1 |
| `dart_tile`, `dart` / `_echo` (O13) | 32×16, 16×8 / 8×8 | 2, 2 / 1 | tir | P1 |
| `rockfall_ice` / `_echo` (O12, B6) | 16×16 | 1 / 1 | — | P2 |

### F4 Collectibles, power-ups et FX de mouvement : artiste « FX gameplay »

| Fichier | Taille | Images | Animation | Prio |
|---|---|---|---|---|
| `shard.png` | 48×8 | 6 | rotation + éclat | P0 |
| `shard_big.png` | 64×16 | 4 | scintillement à 4 fps | P0 |
| `shard_pop.png` | 80×16 | 5 | ramassage | P0 |
| `powerup_bubble.png` + `pu_burin`, `pu_plume`, `pu_calm` | 64×16 + 8×8 ×3 | 4 | flottement | P0 |
| `feather_gold.png` | 96×16 | 6 | balancement | P0 |
| `fx_dust_wall.png`, `fx_jump_puff.png`, `fx_land.png` | 64×16 chacun | 4 | — | P0 |
| `fx_turn.png` / `fx_turn_echo.png` | 48×16 | 3 | volte `G` / volte rechargée `c` | P0 |
| `fx_graze.png` | 48×16 | 3 | frôlé | P0 |
| `picto_tap`, `picto_hold`, `picto_turn`, `picto_echo` | 16×16 | 2, 4, 2, 2 | pictogrammes `w` de l'onboarding (GDD §11) | P0 |
| `pu_magnet`, `pu_lantern`, `pu_gold` + `fx_magnet` + `lantern_flame` | 8×8 ×3, 48×16, 32×8 | 1, 3, 4 | power-ups P1 | P1 |
| `relic_fragment.png`, `moon_shard.png` | 32×8, 64×16 | 4 | — | P1 |

### F5 Marée et matières : artiste « matières animées »

| Fichier | Taille | Images | Animation | Prio |
|---|---|---|---|---|
| `tide_crest.png` | 128×16 | 4 | crête + cycle de palette [E7-H] | P0 |
| `tide_body.png` | 32×32 | 1 | tuile (cycle `u U` dans le shader) | P0 |
| `tide_glow.png` | 32×16 | 1 | halo en 3 paliers, additif | P0 |
| `pal_tide_calm` | 4×1 | — | palette d'Accalmie (crête `J` figée) | P0 |
| `water_surface.png`, `water_body.png`, `bubble.png` (O18) | 64×16, 16×16, 24×8 | 4, 1, 3 | eau | P0 |
| `tide_motes.png`, `tide_warning.png` | 32×8, 64×16 | 4, 2 | particules, alerte | P1 |
| `crystal_bounce.png` (O17) | 64×16 + 48×16 | 4 + 3 | pulsation, rebond | P1 |
| `wind_streak.png`, `wind_flag.png` (O15) | 48×4, 32×8 | 3, 4 | vent | P1 |
| `dark_mask` (O16) | 3 disques (rayons 72 et 96) | — | masque en 3 paliers durs (§5.6) | P1 |
| `frost.png` (O14) | 16×16 + 32×8 | 1 + 4 | givre | P2 |

### F6 Murs, autels et architecture de jeu : artiste « tuiles » (B1 à B3 en P0, puis un biome par lot)
Pour chaque biome `<b>` (crypte, fonderie, biblio, jardin, clocher, sommet) :

| Fichier | Taille | Images | Contenu | Prio |
|---|---|---|---|---|
| `wall_<b>_L.png` / `wall_<b>_R.png` | 128×16 | 8 tuiles | mur gauche et mur **droit dessiné à part** (lumière), dont la brèche secrète | B1-B3 P0 |
| `wall_<b>_lit_L/R.png` | 32×16 | 2 | tuiles éclairées par une source | B1-B3 P0 |
| `wall_<b>_deco_L/R.png` | 64×32 | 4 modules 16×32 | lanterne, niche, cristal… | B1-B3 P0 |
| `wall_<b>_to_<b2>_L/R.png` | 32×16 | 2 | transition vers le biome suivant (§7.1) | B1-B3 P0 |
| `rune_<b>.png` | 32×16 | 2 | rune de boss éteinte / allumée | B1 P0 |
| `altar.png` + `altar_flame.png` | 32×32 + 48×16 | 1 + 6 | autel, flamme cyan | P0 |
| `floor_start.png` | 48×16 | 3 tuiles | dalle de départ | P0 |
| `alcove_<b>.png`, `challenge_door.png` | 32×48, 64×24 | 1, 4 | secrets (GDD §5.4) | P1 |
| `lantern_statue.png` | 64×32 | 4 modules 16×32 | statue de Veilleur à lanterne (B1) | P0 |

### F7 Fonds et parallaxe : artiste « décor »
Pour chaque biome `<b>` (B1 à B3 en P0, B4-B5 en P1, B6 en P2) :

| Fichier | Taille | Images | Contenu |
|---|---|---|---|
| `bg0_<b>.png` | 256×256 | 1 (+ cycle de palette pour le ciel et l'aurore) | P0 lointain, bouclable verticalement |
| `bg1_<b>.png` | 256×256 | 1 | P1 architecture, transparence |
| `bg2_<b>.png` | 128×32 | 4 tuiles 32×16/32×32 | paroi du puits |
| `bg2_<b>_deco.png` | 96×32 | 3 | fenêtre, niche, chaîne |
| `bg1_<b>_anim.png` | selon l'élément | 4-8 | engrenage, cloche, caustiques (P1 pour B1) |

### F8 Avant-plan, lumière et ambiance : artiste « atmosphère »

| Fichier | Taille | Images | Animation | Prio |
|---|---|---|---|---|
| `halo_s/m/l.png` | 32 / 48 / 64 carrés | 1 | 3 paliers par couleur de source | P0 |
| `shader_rim` + tables `pal_rim` | — | — | lumière de contour du héros **et halo du Burin** | P0 |
| `amb_<b>.png` | 48×8 | 2 particules × 3 images | particules d'ambiance du biome | B1-B3 P0 |
| `fg_<b>.png` | 128×64 | 4 silhouettes 32×64 | avant-plan P4 | P1 |

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
| `biome_card` | composition `font_l` + `font_s` | — | carte de titre (§7.1) | P0 |
| `codex_icon_<id>.png` | 16×16 | 1 | 22 icônes d'obstacle, tirées des sprites du jeu | P0 |
| `codex_card.png` | 64×80 (fenêtre 48×48) | 1 | fiche : sprites du jeu animés dans la fenêtre 48×48 | P1 |
| `toggle.png`, `slider.png` | 32×16 / 64×8 | 2 | — | P1 |
| `popup_reward.png` | 64×64 | 6 | pop | P1 |
| `share_frame_<n>.png` | 180×320 | 1 (le n°6 : 4) | 6 cadres de partage (GDD §9.1) | P1 |

### F10 Marque et méta : artiste « marque » (la DA relit chaque pixel)

| Fichier | Taille | Images | Animation | Prio |
|---|---|---|---|---|
| `logo.png` | 160×48 | 6 | détachement de l'écho | P0 |
| `icon.png` | 32×32 | 1 | — | P0 |
| `icon_48.png` | 48×48 | 1 | pour l'icône adaptative Android (export ×9 = 432) | P0 |
| `title_scene` | composition P0-P4 de B1 | — | — | P1 |
| Cadres de captures du store, 5 écrans ×6 | 1080×2400 | — | — | P1 |
| `splash.png` | 180×400 | 1 | — | P1 |

### F11 Ennemis et boss : artiste « créatures »

| Fichier | Taille | Images | Animation | Prio |
|---|---|---|---|---|
| `moth` / `_echo` (O19) | 48×16 / 16×16 | 3 / 1 | battement 2 + virage 1 | P0 |
| `gnawer` / `_echo` (O20) | 64×16 / 16×16 | 4 / 1 | marche | P0 |
| `boss_sonneur.png` | 192×48 | 4 | balancement 2, sonné 2 | P0 |
| `boss_sonneur_yoke.png` | 64×16 | 1 | joug | P0 |
| `boss_wave` / `_echo` | 64×8 / 16×8 | 4 / 1 | préavis 1, actif 3 | P0 |
| `boss_shatter.png` | 384×48 | 8 | bris en éclats | P0 |
| `silence_door.png` | 128×16 ×4 | 4 | fermeture de la porte de Silence | P0 |
| `sentinel` / `_echo` + `sentinel_shot` (O21) | 48×16 / 16×16 + 16×8 | 3 / 1 + 2 | repos, charge, tir | P1 |
| `boss_smith`, `boss_moth_mother`, `boss_eye`, `boss_vane` | 64×64, 32×32, 48×48, 64×24 | 4-6 chacun | boss B2 à B5 | P1 |
| `shadow_trail.png` (O22) | 24×8 | 3 | traînée `j` (le corps = échange de palette) | P2 |

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
| `situation_v1_v2.png` | Même scène à ×4 : à gauche la v1 (192 px, murs de 32, assets actuels), à droite la v2 (180 px, **couloir de 128 du GDD, murs visibles de 26 px**, palette v2, face du mur à x = 10 de la cellule du héros) |

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
   - en v1, le héros se perd dans la texture ;
   - refaite avec la mise en page du GDD : le héros accroché mord 3 px sur le mur et reste lisible ; les 26 px de mur suffisent à lire deux colonnes de pierre.
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

## 15. Écarts avec le GDD à arbitrer par le lead

| # | GDD v1.0 | Bible | Pourquoi |
|---|---|---|---|
| 1 | §0 : écran 192×352, « ×3 sur 1080p » | Viewport 180 de large en expand, ×6 sur 1080×2400 ; monde inchangé (murs 0→32 / 160→192), caméra décalée de −6 px | 1080/192 = 5,625 : pixels inégaux (§2.2). Et 192×3 = 576, pas 1080 : la ligne du GDD est fausse |
| 2 | §0 : héros « visuel 8×12 » | Cellule 32×32, silhouette 18×21, **hitbox 6×10 conservée** | [C10] : 8×12 ne porte ni regard, ni main, ni écharpe (§3.1). Si les tests montrent qu'on traverse visiblement des pièges, passer la hitbox à 8×12 |
| 3 | §4.1 : hitbox = visuel −1 px | Cœur du sprite = hitbox ; dents, ailes et pointes dépassent de 1 à 4 px (§9.1) | Clémence visible, sans toucher aux hitbox |
| 4 | O2 : scie 16×16, 2 images à 12 fps | Cellule 24×24, disque Ø12, dents jusqu'à Ø20, 4 images à 50 ms | Une scie à 2 images se lit comme un clignotement, pas comme une rotation [E2-A] |
| 5 | §6 : murs de transition en dither 2×2 sur 32 px | 2 tuiles de transition dessinées par paire de biomes | Tramage décoratif interdit [A6-H] |
| 6 | O16 : « fondu au noir sur 32 px en dither » | Masque en 3 paliers durs (§5.6) | Même raison |
| 7 | §6 : aurore de B6 en `f` | Aurore en `v`, crête `V` de 1 px | `f` sort de la bande de luminance des fonds (§7) |
| 8 | §9.3 : couleurs des tenues 4, 13, 17, 18, 21 | Corrigées au §8.5 | Cape de base à Y ≥ 0,25 ; cyan réservé |
| 9 | §9.3 : silhouette 8×12 pour les tenues | Silhouette 18×21, accessoire en calque | Suit l'écart n°2 |
| 10 | §4.1 : préavis ≥ 0,25 s ; herse à 0,3 s | Recommandation : ≥ 0,4 s dans les chunks `intro` | Le joueur doit voir le préavis avant d'apprendre à le compter |
| 11 | O14 givre (B6) et ambiance de B2 | Pas de givre décoratif en B2, condensation `4` | Un signe = un sens [C16-D] |
| 12 | §6 : carte de titre en police 8 px | `font_l` pour le nom | Lisibilité d'un titre à ×6 |
| 13 | O22 : l'Ombre en 8×12 | Silhouette du héros recolorée | « C'est moi, en négatif » [C10-I] |

---

## 16. Résumé pour le lead

- **Résolution :**
  - base 180×320, aspect « expand », échelle entière (1080×2400 → ×6 = 180×400 exact) ;
  - couloir de 128 px du GDD inchangé, murs visibles de 26 px, caméra décalée de −6 px, physique intacte ;
  - zones sûres de 20 px en haut et 24 px en bas.
- **Tailles :**
  - héros en cellule 32×32 (silhouette 18×21, classe 20-24 px de [C10], 11 couleurs), pivot (16,27), hitbox du GDD 6×10 ;
  - tuile de mur 16×16 ; modules 16×32 ; paroi de fond 32×16 ;
  - scie en cellule 24 (Ø12 + dents) ; éclat 6×6 ; boutons d'au moins 24 px de haut.
- **Palette v2 :**
  - 71 couleurs, superset compatible de la v1, rampes à 10-20° de décalage de teinte ;
  - bandes de luminance par plan (fond Y < 0,03, murs 0,03-0,13, acteurs > 0,25) ;
  - couleurs réservées : corail = héros, magenta = danger, cyan = écho, or = collectible, violet = marée ;
  - 6 rampes de biome à même échelle de valeur.
- **Lumière :** haut-gauche, sources peintes (émissif + halo additif en paliers + tuiles éclairées), lumière de contour de 1 px par shader, pas de glow WorldEnvironment.
- **Profondeur :** 5 plans P0-P4 à 0,10 / 0,30 / 0,60 / 1,00 / 1,40.
- **Biomes (GDD) :** Crypte des Veilleurs, Fonderie froide, Bibliothèque engloutie (P0) ; Jardin de cristal, Clocher des vents (P1) ; Sommet céleste (P2).
- **Familles d'assets (11) :** F1 Héros · F2 Écho et gravure · F3 Pièges · F4 Collectibles et power-ups · F5 Marée et matières · F6 Murs et autels · F7 Fonds · F8 Ambiance et lumière · F9 UI · F10 Marque · F11 Ennemis et boss.
