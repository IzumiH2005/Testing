# Analyse : garde ouverte et garde fermée

Deux postures de combat qui partagent les mêmes jambes (INVENTAIRE § 2, règle 6) : seuls le buste,
la tête et les bras changent. Le personnage regarde vers la droite, la jambe et le bras **proches**
(N) sont devant (garde « avant proche »).

Contrainte de production : `poses/garde.json` et `poses/garde_ouverte.json` servent de base à des
dizaines d'animations (marches, blocages, coups, transitions). On ne déplace pas les pieds de
profil (positions de chevilles conservées) ; on règle la profondeur, les rotations, le talon, le
tronc, la tête et les bras.

## 1. La logique de la garde

Une garde répond à trois besoins à la fois :

1. **Être stable dans toutes les directions.** Les pieds forment une base en largeur *et* en
   longueur. Des pieds sur une même ligne (vue de face, l'un derrière l'autre) font tomber sur
   le côté au premier coup.
2. **Pouvoir partir tout de suite.** Genoux pliés, poids réparti, talon arrière levé : la jambe
   arrière est un ressort déjà chargé (c'est elle qui pousse, voir `coup_de_poing_rue.md`).
3. **Protéger les cibles.** Le menton derrière l'épaule avant et le poing arrière, les coudes
   devant les côtes, le corps de trois quarts pour offrir moins de surface.

Différence entre les deux :

- **Garde ouverte** (prêt à se battre) : la main avant est avancée vers l'adversaire, elle mesure
  la distance et menace (jab). Le corps est plus de profil, plus mobile.
- **Garde fermée** (pour bloquer) : les deux poings remontent devant le visage, les avant-bras
  font un mur vertical, les coudes se serrent contre les côtes, le menton rentre, les épaules
  montent. Le buste se ferme et se tasse un peu : on encaisse.

## 2. Anatomie

| Partie | Ce qui travaille | Pourquoi |
|---|---|---|
| Pieds | appui sur toute la plante devant, sur l'avant-pied derrière | le talon arrière levé charge le mollet : départ immédiat |
| Genoux | quadriceps en tension légère, flexion ≈ 20-30° | amortir et pousser ; un genou tendu se bloque |
| Hanches | rotation : pied avant presque vers la cible, pied arrière vers l'extérieur | la base en trois quarts, le genou suit le pied |
| Bassin | tourné de ≈ 30° (hanche avant devant) | profil de combat, prépare la rotation des coups |
| Tronc | léger penché avant (≈ 10°), épaules ≈ 5° de plus que le bassin | poids vers l'avant sans tomber, menton protégé |
| Omoplates | haussées (+2 à +4), légèrement en avant | l'épaule avant cache le menton |
| Cou | fléchi : menton rentré, regard sous les sourcils | protéger la mâchoire |
| Bras avant | ouverte : coude ≈ 80°, main à hauteur de menton, devant ; fermée : coude ≈ 130°, poing à la tempe | menace ou mur |
| Bras arrière | poing à la joue, coude ≈ 130°, coude devant les côtes | protège le menton et le foie |

## 3. Chaque articulation, tous ses axes

Repère : torsions positives = côté proche (avant) vers l'avant. Rotation de hanche positive =
genou vers la caméra.

| Axe | Garde ouverte | Garde fermée |
|---|---|---|
| Pied avant | à plat, pointe vers la cible (rotation de hanche −5°) | idem |
| Pied arrière | sur la plante, talon levé, pointe vers l'extérieur (−35°) | idem |
| Écartement (largeur) | cuisses ±13° (net ±10° avec la largeur de hanche, voir anatomie § 6 bis) : pieds écartés d’environ la largeur des épaules | idem |
| Genoux | pliés, au-dessus des pieds | idem, un peu plus (on se tasse de 2) |
| Bassin | rotation +25 | +22 |
| Buste (torsion) | +8 | +4 (plus de face : les deux bras devant) |
| Penché | dos 7, thorax 8 | dos 8, thorax 9 |
| Omoplates | haussées +2, avant +2 en avant | haussées +4, en avant +1 |
| Cou | 12 (menton rentré) | 14 |
| Bras avant | devant, à peine écarté vers le centre, coude bas, avant-bras vers la cible ; coude ≈ 80° | levé devant le visage, coude serré sous le poing ; ≈ 135° |
| Bras arrière | poing à la joue, coude devant les côtes ; ≈ 128° | poing à la tempe ; ≈ 138° |

Vue de face (contrôle) : pieds écartés, mains devant l'axe du corps (pas sur les côtés), coudes
rentrés. Trois quarts : la main avant est devant le menton, sur la ligne vers la cible. Profil :
la silhouette lit « prêt » (ouverte) ou « fermé » (mur des avant-bras devant le visage).

## 4. Respiration et vie (les boucles `garde_*_idle`)

Un combattant n'est jamais immobile (bible, A1 : pas de pose figée).

- **Ouverte** : un petit rebond sur les plantes, deux par cycle (genoux qui plient de 1 à 2
  unités), la main avant qui avance et recule légèrement (elle « tâte » la distance), les
  épaules qui suivent la respiration, la tête qui reste stable (le regard ne bouge pas).
  Chevauchement : tronc, puis cou, puis bras (décalages déjà en place).
- **Fermée** : tendu, peu de mouvement : respiration courte, poings qui se resserrent, très
  léger balancement du poids d'une jambe à l'autre.

## 5. Contrôles

1. `--verifier` sur les deux boucles et sur les animations qui partent de ces poses : pas de
   nouvelle alerte d'amplitude, pas de pied qui glisse, pas de « sous le sol ».
2. Vues `--vues` : de face, les pieds sont écartés et les mains devant l'axe.
3. Positions des chevilles de profil inchangées (±2) par rapport aux anciennes poses.
4. La boucle se referme sans saut (image 0 = dernière image).
