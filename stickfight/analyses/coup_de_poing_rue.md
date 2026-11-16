# Analyse : coup de poing de rue

Direct du bras arrière avec élan, porté à la tête, depuis la garde ouverte. Force 4 sur
l'échelle de la bible (§ C). Le personnage regarde vers la droite ; le bras qui frappe est le
bras **proche** (N), du côté de la caméra, pour qu'on le voie.

## 1. La logique du mouvement

Un coup de poing de rue n'est pas un jab : on veut frapper **fort**, quitte à prévenir. Toute la
force vient du corps entier, pas du bras. Le bras ne fait que transmettre au poing ce que les
jambes et le tronc ont produit. D'où trois idées :

1. **Reculer pour avoir de la place et de la distance à parcourir.** Le pied avant recule : le
   poids passe sur la jambe de ce côté, qui devient la jambe arrière, celle qui poussera. Le bras
   du même côté devient le bras arrière, celui qui frappera (même côté que la jambe qui pousse).
2. **Tourner le corps comme on remonte un ressort.** Le bassin tourne un peu vers l'arrière, les
   épaules tournent plus que le bassin. L'épaule du bras de frappe part en arrière, le coude
   aussi. Le muscle du tronc s'étire entre le bassin et les épaules : c'est le ressort.
3. **Tout relâcher dans l'ordre, du sol vers le poing.** La jambe arrière pousse, le bassin
   revient et dépasse, les épaules suivent avec un temps de retard, l'épaule de frappe avance,
   et le coude se déplie en dernier. Chaque segment part quand le précédent est lancé.

Pendant ce temps, **l'autre côté fait le contraire** : quand l'épaule de frappe avance, l'épaule
avant recule d'autant (c'est la même rotation), et le bras avant se replie contre le menton.
C'est à la fois l'équilibre de la rotation et la garde.

**La tête ne baisse pas.** Elle reste à peu près à la même hauteur, le regard sur la cible. Elle
avance avec le corps, mais elle ne pique pas vers le bas.

## 2. Anatomie : ce qui bouge et ce qui donne la force

| Partie | Articulation | Muscles | Rôle |
|---|---|---|---|
| Jambe arrière | cheville, genou, hanche | mollet, quadriceps, fessiers | pousse le sol : le talon décolle, le genou et la hanche se tendent. C'est le moteur (chez les boxeurs, la force au sol est surtout sous le pied arrière pour ce coup) |
| Bassin | rotation autour de la colonne | fessiers, adducteurs, obliques | tourne vers la cible ; il part **avant** les épaules |
| Tronc | rotation et légère flexion | obliques, grand dorsal | transmet la rotation ; l'écart bassin-épaules se referme |
| Épaule de frappe | protraction et flexion | grand pectoral, deltoïde antérieur, dentelé antérieur | pousse l'épaule et le bras vers la cible |
| Coude de frappe | extension | triceps | se déplie en dernier, jusqu'au bras tendu au contact |
| Poing | flexion des doigts, poignet bloqué | fléchisseurs de l'avant-bras | serré à l'armé et au contact |
| Épaule avant | rétraction | rhomboïdes, trapèze | recule pendant que l'autre avance |
| Coude avant | flexion | biceps | se replie : le poing avant revient au menton |
| Jambe avant | genou | quadriceps | reçoit le poids, plie un peu pour absorber |
| Cou | stabilisation | muscles du cou | garde la tête à niveau, le regard sur la cible |

## 3. Les phases, partie par partie

Durées à 60 images par seconde.

### Garde (0)
Garde ouverte : pied proche devant, poids au milieu, mains devant.

### Petite anticipation (0-3)
Il se ramasse un peu : genoux légèrement plus pliés. C'est le premier niveau d'anticipation.

### Recul (3-12)
- Le pied avant (proche) se soulève et recule loin derrière ; il se pose sur la pointe.
- Le poids part sur cette jambe, qui est maintenant la jambe arrière, genou plié.
- Le pied loin, qui devient le pied avant, se pose à plat.
- Le bras proche part en arrière, le coude commence à se plier.

### Armé (12-24), tenu
- **Bassin** tourné vers l'arrière d'environ 30° : la hanche proche recule (`torsionBassin` −30).
- **Épaules** tournées plus loin, environ 60° : l'épaule proche est derrière la colonne
  (`torsion` −60). L'écart bassin-épaules (30°) est le ressort.
- **Buste** légèrement en arrière (le poids est sur la jambe arrière), environ 10 à 15°.
- **Bras de frappe** : coude tiré en arrière, avant-bras complètement replié (≈ 145°), poing
  serré près de la joue, devant l'épaule, sous le menton.
- **Bras avant** : tendu à moitié vers la cible (coude ≈ 30 à 45°), il mesure la distance.
- **Tête** à niveau, regard sur la cible : le cou compense l'inclinaison du buste.
- **Jambes** : genou arrière plié et chargé, pied avant à plat.
- Pendant la tenue, la pose dérive un peu (il se ramasse encore), elle n'est jamais figée.

### Dernier cran (24-26)
Il s'enfonce d'un ou deux pixels et la torsion va encore un peu plus loin. Troisième niveau
d'anticipation, juste avant de partir.

### Frappe (26-29) : trois images, écarts du poing croissants
- **27** : la jambe arrière pousse (talon qui décolle), le bassin revient (`torsionBassin` −30 →
  0). Les épaules sont encore tournées : l'écart est au maximum. Le bras est encore armé.
- **28** : le bassin continue (+20), les épaules suivent (`torsion` −60 → 0), l'épaule de frappe
  avance, le coude passe devant et commence à se déplier (≈ 100°). Le bras avant commence à se
  replier, l'épaule avant à reculer. Le pied avant avance pour recevoir le poids.
- **29, contact** : bassin +30, épaules +50 (l'épaule de frappe devant, l'épaule avant
  derrière). Coude tendu, poing sur la cible. Pied arrière, bassin, épaule et poing sur une
  même ligne. Bras avant replié contre le menton (coude ≈ 120 à 140°). Tête à niveau, juste
  derrière l'épaule de frappe. Genou avant plié, il reçoit le poids.

### Dépassement (29-35) et tenue (35-46)
La rotation continue un peu (épaules +65) et le buste avance encore une ou deux images après le
bras. Le bras de frappe se relâche en continuant vers le bas. Le pied arrière traîne puis
décolle. On tient la pose emportée, en la laissant dériver.

### Retour (46-72)
Le pied arrière passe devant et se pose, l'autre recule, les torsions reviennent à 0, garde.

## 4. Ce qui se voit de profil

- Les torsions du bassin et des épaules se voient par le décalage des hanches et des épaules
  (canaux `torsionBassin` et `torsion`) et par la portée des bras : l'épaule qui avance donne de
  l'allonge au poing.
- La rotation du poing (paume vers le bas au contact) ne se voit pas : on l'ignore.
- Le poing armé doit rester lisible : près de la joue, mais pas caché dans la tête.

## 5. Références

- Vidéo 1, coups lourds du rouge (V1 173-187, 196-208) : armé tenu, déclenchement, contact
  aligné du pied arrière au poing.
- Vidéo 2, coup au corps de Rai (V2 806-819) : le corps entier avance, le poing reste planté.
- Bible : A2 (anticipation), A3 (chaîne et torsion), A4 (ce qui arrête le coup), A bis 1 à 7
  (jambe arrière, accélération jusqu'au contact, niveaux d'anticipation, chevauchement), § C
  (force 4).

## 6. Contrôles (avec `--verifier`)

1. L'angle du coude de frappe décroît de l'armé au contact (≈ 145 → 100 → 0).
2. Les écarts du poing augmentent jusqu'au contact.
3. Le bassin revient une image avant les épaules (torsions aux images 27 et 28).
4. La tête ne pique pas : l'angle du cou reste à 15° ou moins vers l'avant, et la tête ne
   descend qu'avec le corps (fente plus basse que la garde), pas en se penchant.
5. Au contact, le poing est à moins de 25 unités du centre de la tête adverse.
6. Le poing armé n'est pas caché dans la tête.
