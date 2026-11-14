# Recherche : proportions, amplitudes, animation de combat

Notes qui ont servi à construire le modèle, avec leurs sources.

## 1. Proportions relevées sur les vidéos de référence

Mesures prises image par image sur les deux vidéos fournies, en prenant le
diamètre de la tête comme unité.

| | Vidéo A | Vidéo B |
|---|---|---|
| Hauteur totale | ≈ 3,8 têtes | ≈ 5,4 têtes |
| Épaisseur du trait | ≈ 0,34 tête | ≈ 0,36 tête |
| Tête | disque plein, posé sur le tronc sans cou visible | idem |
| Mains, pieds | simples bouts ronds du trait | idem |

D'où le style `epais` du rig : tête de 46, trait de 15 (≈ 0,33 tête), pas de
cou, la tête « mord » de 12 % de son rayon sur le haut du tronc. Le tronc est
coupé en deux os (bas du dos, poitrine) pour pouvoir arrondir le dos en garde.
Le style `fin` garde des proportions plus humaines (≈ 5,5 têtes).

## 2. Amplitudes articulaires (degrés)

Valeurs de référence pour un adulte, utilisées comme limites du rig. Le rig
garde un peu de marge au-delà des valeurs « normales » d'examen, parce qu'un
combattant force ses amplitudes (coup de pied haut, garde très repliée).

| Articulation | Mouvement | Référence | Limite du rig |
|---|---|---|---|
| Épaule | flexion (bras devant) / extension (derrière) | 180 / 60 | −60 … 180 |
| Coude | flexion | 140–150 | 0 … 150 |
| Hanche | flexion (genou devant) / extension | 120 (CDC : 127–136) / 20–30 | −30 … 140 |
| Genou | flexion | 135–150 | 0 … 150 |
| Cheville | flexion dorsale / plantaire | 20 / 50 | −50 … 20 |
| Colonne lombaire, thoracique | flexion / extension, réparties sur deux os | — | −25 … 45 chacun |
| Cou | flexion / extension | 50 / 60 | −60 … 50 |

Sources :
- [Enlyte : tableau des amplitudes articulaires](https://enlyte.com/print/pdf/node/33601)
- [WikEM : Joint ROM (table)](https://wikem.org/wiki/Joint_ROM_(Table))
- [CDC : Normal Joint Range of Motion Study](https://archive.cdc.gov/www_cdc_gov/ncbddd/jointrom/index.html)

## 3. Comment sont animés les jeux de combat

- **Tekken est en grande partie animé à la main.** Les animateurs posent des
  images clés et règlent le timing image par image. La capture de mouvement
  sert pour certains personnages : les coups de Lidia ont été capturés sur
  Tatsuya Naka, un pratiquant de karaté. Harada a précisé qu'elle n'est pas
  utilisée pour tout le monde.
  ([Siliconera](https://www.siliconera.com/?p=877792),
  [portfolio d'un animateur Tekken](https://twine.net/kentoon))
- **L'approche courante est hybride** : une base en capture, puis une reprise
  à la main pour exagérer les poses et resserrer le timing. La capture brute
  paraît molle en combat, parce que le joueur a besoin de lire le coup
  instantanément.
  ([MoCap Online](https://mocaponline.com/blogs/mocap-news/combat-animation-games-guide),
  [Creative Bloq, Spine](https://www.creativebloq.com/3d/3d-animation/creating-the-john-wick-inspired-mocap-for-spine-and-why-unreal-engine-5-isnt-always-best))
- **L'exagération est voulue** : une préparation (anticipation) courte mais
  lisible, un impact sur une pose très étirée, un retour plus lent. La
  silhouette doit se lire en une image.
  ([Pixune](https://pixune.com/blog/role-of-exaggerated-animation-in-fighting-games/))
- **L'arrêt sur impact (hit-stop)** fige les deux personnages quelques
  images au moment du contact. C'est ce qui donne le poids du coup, plus que
  l'animation elle-même.

### Ce que ça implique pour ce projet

Un stickman n'a ni visage ni vêtements : **tout passe par la silhouette et le
timing**. D'où les choix du modèle :

- une précision au centième de degré, et des poses enregistrées en JSON lisible
  pour pouvoir les retoucher et les comparer ;
- des amplitudes humaines activables, pour rester crédible par défaut et
  pouvoir exagérer volontairement ;
- un outil de rendu en ligne de commande, pour enchaîner rapidement « modifier
  un angle, regarder » sans rouvrir l'éditeur ;
- l'animation, à venir, sera faite de poses clés à la main avec un timing en
  images, comme pour Tekken, plutôt qu'en capture.
