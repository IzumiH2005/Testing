# Test 16 — Kit de niveau « Grotte des Échos cristallins » (plateformer)

## F0. Intention
- **Vue** (A9) : profil, jeu de plateforme. Une seule vue pour tout le kit.
- **Tuile** : 16×16 px. Écran de référence 320×180 (20 × 11,25 tuiles), affiché ×4.
- **Plans** :
  1. jouable : sol et murs en roche naturelle (autotile blob 47), dalles de ruine traversables ;
  2. décor posé : cristaux, rochers, colonne brisée, racines, touffes de mousse ;
  3. fonds : paroi lointaine avec la faille de lumière (fixe), piliers lointains (×0,25),
     ruines moyennes (×0,5) ;
  4. premier plan : roches sombres en haut et en bas de l'écran seulement (×1,25).
- **À lire en un coup d'œil** : où marcher = la croûte de mousse claire ; où ça fait mal = les
  épines de cristal magenta (seule couleur rose-rouge du lieu) ; où ça s'ouvre = la lumière.

## Direction artistique
Une grotte sous des ruines. Le jour entre par une faille en haut à gauche : **c'est la
source de lumière du jeu** (règle 23), chaude et pâle. Les ombres virent au bleu-violet.
Des cristaux turquoise poussent dans la roche et luisent doucement : ils sont la lumière
secondaire (contre-jour violet, halo). Le danger est un cristal malade, magenta.

- **Langage de formes** (A4b) : roche naturelle = formes molles et cassées ; ruines = rectangles
  et pierre taillée (un ton par face) ; cristaux = triangles (attirants) ; épines =
  triangles serrés et pointus vers le haut (danger).
- **Masque de gamme** (F4) : un triangle sur la roue qui couvre bleu-violet (roche, fonds),
  turquoise (cristaux) et vert-jaune (mousse). Le personnage (orange) et le danger
  (magenta) sont **hors du masque** : ils ressortent sans contour forcé.

## Hiérarchie de valeurs (F1), en luminance (0-255)
| Plan | Tons | Luminance |
|---|---|---|
| Personnage | orange, crème | 120-205, saturation 70-100 % |
| Danger | magenta, rose | 80-130, saturation 68-86 %, éclat 227 |
| Croûte de mousse (où marcher) | `h i j` | 94-166 |
| Roche jouable | `a`-`e` | 42-143 (face ~88) |
| Fonds | `1`-`6` | 18-79, sauf la faille (111-207) |
| Premier plan | `O a` | 24-42 |

## Palette (F4, A6-A)
`palette.json`, rampes dans `rampes.png`.
- Contour du lieu `O` #1a1426 : violet presque noir, jamais du noir pur, le même partout.
- Pierre `a b c d e` : marches de 23 à 28 en gris ; teinte 255° dans l'ombre → 338° (gris
  à peine rosé, chaud) dans la lumière ; saturation qui baisse vers le clair.
- Mousse `g h i j` : 142° → 68°, vers le jaune dans la lumière ; marches 34-37.
- Cristal `t u v w W` + contre-jour `x` (violet).
- Danger `r p q X`.
- Fonds `1`→`9` : du fond de la grotte à la faille (chaude, `8 9`).
- Personnage de test `k l n N s S y`.

## Ce que le kit contient
1. Autotile du sol : 4 pièces (îlot 32×32 + coins intérieurs 16×16), assemblées en 47 tuiles.
2. Variantes : 2 remplissages, 2 croûtes.
3. Dalles de ruine traversables (bout gauche, milieu ×2, bout droit).
4. Décors : grand cristal (B6-D, 9 étapes), petit cristal, rocher composé (B6-B), colonne
   brisée, racines pendantes, touffes de mousse ×3.
5. Danger : épines de cristal ×2.
6. Personnage de test d'échelle (16×24), seulement pour les tests « en situation ».
7. Fonds : paroi + faille, piliers lointains, ruines moyennes, premier plan.
8. Contrôles : grille 3×3, carte dézoomée, gris, autotile U/L/île, parallaxe en GIF, scène.
