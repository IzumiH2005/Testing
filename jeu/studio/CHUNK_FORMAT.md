# Format des chunks (contrat entre level design et moteur)

Fixé par le lead programmeur. Le chargeur `game/scripts/chunks.gd` lit **exactement** ce format.
Référence de design : `GDD.md` sections 4 (obstacles), 8 (chunks, budget, assemblage, courbe).

## Fichier
`jeu/game/chunks/<biome>/<id>.txt` (biome en minuscules : `b1`, `b2`, `b3`…). Encodage UTF-8.

```
id: b1_laser_intro
biome: B1
tension: M          # R repos, M montée, P pic, I introduction, A arène de boss
D: 2                # budget de difficulté 0-10 (GDD 8.2)
entree: any         # L, R ou any : côté où le héros est accroché en entrant
sortie: any
verbe: bond         # bond, elan ou volte (verbe minimal exigé)
intro: O8           # facultatif : ce chunk est l'introduction de cet obstacle
alt: 22-150         # altitude min-max (m) où le chunk peut être tiré
poids: 1.0          # facultatif, probabilité relative
---
##........##
L#........#L ; period=3.1 warn=0.7 on=0.9 phase=0.0
##>.......##
##........##
---
```
- Les lignes d'en-tête sont `clé: valeur`. Tout ce qui suit `//` sur une ligne est un commentaire.
- La grille est entre deux lignes `---`. **12 caractères par rangée**, lue de haut en bas. Une rangée = 16 px = 1 m.
- La hauteur du chunk = nombre de rangées (12, 16 ou 24 recommandé ; tout entier entre 6 et 32 accepté).
- Paramètres optionnels en fin de rangée après ` ; ` : `clé=valeur` séparés par des espaces.
  Ils s'appliquent à **tous** les éléments de cette rangée (et à la bande entière si l'élément s'étend sur plusieurs rangées : mettre les paramètres sur la **première** rangée de la bande, celle du haut).
- Colonnes : 0-1 mur gauche, 2-9 couloir (x = 32 à 160), 10-11 mur droit. Colonne c couvre x ∈ [16c, 16c+16].
- La rangée du bas d'un chunk touche la rangée du haut du chunk précédent (en dessous). Les **2 rangées du haut et
  les 2 du bas** doivent rester sans piège (règle de jointure, GDD 8.1) ; éclats autorisés.
- Le chunk peut être retourné en miroir par le moteur : écrire pour un côté, l'autre est gratuit.

## Légende
| Car. | Élément | Où | Règles / paramètres (défauts) |
|---|---|---|---|
| `#` | mur | col 0-1, 10-11 | Toujours `##` à gauche et à droite sauf émetteurs. |
| `.` | vide | couloir | |
| `>` | épines (O1) sur le mur gauche | col 2 | Rangées consécutives = une bande (2 à 4). Une bande est gravée en entier. |
| `<` | épines (O1) sur le mur droit | col 9 | idem |
| `C` | contrefort à épines (O3) | col 2 ou 9 | Bande de 2-3 rangées. Face accrochable, épines dessus/dessous. |
| `S` | scie fixe (O2) | couloir | Centre = centre de la tuile. `dx=` décalage en px (ex. `dx=8` pour être sur la ligne entre 2 tuiles). |
| `-` | rail horizontal (O4) | même rangée qu'un `S` | La scie va-et-vient entre les extrémités de la suite `-`/`S` contiguë. `spd=` rad/s (1.7), `phase=` 0-1 (aléatoire si absent). |
| `|` | rail vertical (O5) | même colonne qu'un `S` | idem, verticalement. |
| `L` | émetteur laser (O8) | col 1 ou col 10 (remplace un `#`) | Le faisceau traverse le couloir au centre de la rangée. `period=` (3.1) `on=` (0.9) `warn=` (0.7) `phase=` 0-1 (aléatoire si absent). |
| `H` | herse (O9) | col 2 ou 9 | Bande de 2 rangées. `period=` (2.4) `out=` (0.9) `warn=` (0.3) `phase=`. |
| `M` | mâchoires (O10) | col 2 **et** col 9 sur la même rangée | `period=` (3.0) `phase=`. |
| `f` | plaque friable (O11) | col 2 ou 9 | Bande de 2 rangées, non létale. |
| `~` | eau (O18) | n'importe quelle case du couloir | Toute rangée contenant au moins un `~` est entièrement sous l'eau. |
| `P` | ancre de pendule (O6) | couloir | `len=` longueur de chaîne px (48), `amp=` degrés (50), `period=` (2.2), `phase=`. |
| `g` | grignon (O20) | col 2 ou 9 | Position de départ ; `:` dans la même colonne = suite de cases de patrouille. `spd=` px/s (24). |
| `:` | chemin de patrouille | col 2 ou 9 | |
| `m` | phalène (O19) | couloir | Vole horizontalement de mur à mur. `spd=` (40), `dir=` 1 ou -1. |
| `b` | éboulis (O12) | couloir | Tombe dans sa colonne quand le héros passe 96 px en dessous. |
| `o` | créneau d'éclat | couloir | La graine choisit ~70 % des créneaux. Les placer **sur les arcs** (récompense la bonne route). |
| `O` | grand éclat (+5) | couloir | Toujours présent. |
| `*` | créneau de power-up | couloir | Max 1 par chunk, plutôt dans les chunks R. |
| `R` | rune de boss | col 2 ou 9 | Arènes seulement (tension A). |
| `A` | autel (checkpoint) | n'importe où sur la rangée | Uniquement dans les chunks `tension: I` d'entrée de biome. |
| `?` | brèche secrète | col 1 ou 10 | Alcôve bonus (P1). |

## Physique à respecter (GDD 2.3, couloir 8 tuiles)
Le héros accroché a son centre à x = 38 (gauche) ou 154 (droite). Depuis l'accroche :
- **Bond** : traverse en 0,55 s, atterrit **+3 rangées** plus haut (52 px), apex à +3,7 rangées au milieu.
- **Élan** (doigt tenu) : atterrit **+5 rangées** (78 px), apex +5 rangées.
- **Volte** (tap en l'air) : revient au **même mur** +3 à +5 rangées (45 px si volte à 0,1 s, 85 px à 0,3 s).
- **Glisse** : accroché, tient 0,22 s puis descend à 14 px/s.
- Hitbox létale du héros : 6 × 10 px. Laser : létal si |dy| < 5 px entre faisceau et centre du héros.
- Marée : 10 + 0,35·t px/s, plafond B1 28 / B2 34 / B3 40 px/s ⇒ on ne peut pas attendre plus de ~2 s à un endroit.

## Règles d'édition (dures)
1. Toujours une route sans power-up, faisable avec **le verbe déclaré** (en B1 et `verbe: bond` : uniquement des bonds).
2. Marge ≥ 4 px en B1-B2, ≥ 3 px en B3 entre la hitbox du héros et un danger sur la route prévue.
3. Max 4 rangées d'épines d'affilée par côté ; jamais d'épines sur les deux murs à la même rangée.
4. Un obstacle jamais vu apparaît seul dans son chunk `intro`.
5. Attente forcée ≤ 0,6 × budget d'attente (B1 2,3 s, B2 2,0 s, B3 1,7 s).
6. Écrire en commentaire `//` la **route prévue** sur les rangées d'atterrissage (ex. `// L1 bond -> R4`).
