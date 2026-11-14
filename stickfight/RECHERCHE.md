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
| Mains | simples bouts ronds du trait | idem |
| Pieds | petit crochet arrondi vers l'avant, à peine plus long que le trait est épais ; à plat au sol, sur la pointe en poussée | idem |

D'où le style `epais` du rig : tête de 46, trait de 15 (≈ 0,33 tête), pas de
cou, la tête « mord » de 12 % de son rayon sur le haut du tronc, pied de 10
(une fois et demie à peine le trait, pour rester un simple crochet). Le tronc est
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

## 4. Animer le blocage bas, la garde et le repos

### Le geste réel

- **Gedan barai (karaté)** : l'avant-bras descend en diagonale pour chasser
  vers le bas et sur le côté un coup visant le ventre ou plus bas. Le bras
  part d'en haut (armé près de l'épaule opposée) pour prendre de la vitesse,
  et le corps ne se baisse pas.
  ([The Martial Way](https://www.themartialway.com.au/gedan-barai-lower-block/),
  [Black Belt Wiki](https://blackbeltwiki.com/?p=5634))
- **Parade du teep (boxe thaï)** : contre un pied direct, on ne bloque pas de
  face, on frappe le pied ou le tibia de la main pour le dévier vers le bas ;
  l'attaquant perd l'équilibre vers l'avant.
  ([Evolve University](https://evolve-university.com/blog/the-3-best-ways-to-defend-a-muay-thai-push-kick/))

D'où le blocage du projet : les deux mains montent un peu (armé, f4), puis
s'abattent ensemble sur le tibia juste derrière la cheville (contact f8,
133 ms). Le défenseur reste droit, le bassin bouge de moins de 2 unités.

### Les 12 principes (Thomas et Johnston, *The Illusion of Life*)

Résumé des principes : [EVL, Université de l'Illinois (PDF)](https://www.evl.uic.edu/datsoupi/251/docs/12AnimationPrinciples.pdf),
[CG Wire](https://blog.cg-wire.com/12-principles-animation/).
Comment ils sont appliqués ici :

| Principe | Application |
|---|---|
| Squash and stretch | Clé « écrasé » juste après le contact : la jambe du coup de pied se plie sous la frappe, les mains du défenseur s'enfoncent de quelques unités ; canal `etire` pour allonger un os |
| Anticipation | Le blocage arme les mains vers le haut avant de frapper vers le bas ; la mise en garde tasse le corps avant le pas ; le coup de pied charge en reculant le bassin de 1,5 |
| Mise en scène (staging) | Tout est de profil, chaque pose clé doit se lire en silhouette ; au contact, les deux corps s'écartent pour que la main et le pied soient sur fond vide |
| Pose à pose | Animation par clés nommées, le mouvement entre elles est calculé |
| Continuité et chevauchement | `decalage` : tête, avant-bras et bras arrière suivent avec 1 à 12 images de retard |
| Ralentis (slow in / slow out) | Courbes `acc`, `dec`, `acc-dec` par segment ; `dec` après un contact pour que la pose d'impact reste lisible |
| Arcs | Courbe `auto` (spline) ; trajectoires vérifiées sur la stroboscopie |
| Action secondaire | Poussière sous les pieds qui glissent, respiration et transfert de poids dans les idles |
| Timing | Blocage en 8 images, coup de pied en 17 : l'attaque est lisible, la défense rapide |
| Exagération | Pied rabattu bien plus bas qu'en réalité après le blocage, arrêt sur impact |
| Dessin solide | Proportions et amplitudes humaines de la partie 1 et 2 |
| Charisme (appeal) | Garde compacte, tête rentrée, poings hauts |

### Astuces des jeux de combat

- **Arrêt sur impact (hit-stop)** : 7 images où les deux combattants sont
  figés et tremblent, pendant que l'étincelle éclate. Le poids du coup vient
  de cette pause. ([Sonic Hurricane, Impact Freeze](https://sonichurricane.com/?p=1043))
- **Démarrage, actif, récupération** : un coup se découpe en images de
  démarrage, images actives et images de récupération. Ici la défense doit
  être active quand le pied arrive, d'où le calage des deux animations sur
  le même événement `contact`.
  ([Critical Points, frame data](https://critpoints.net/2023/02/20/frame-data-patterns-that-game-designers-should-know))
- **Secousse de caméra** courte et amortie au contact.
- **Fondu court** (3 à 4 images) entre deux animations pour ne jamais sauter
  de pose.

### Astuces d'animation en pixel art

- **Animer « en deux »** : les effets changent d'image toutes les 2 images,
  ce qui donne un rythme sec et lisible. Option `pas` pour faire pareil sur
  le corps.
- **Images étalées (smears)** : l'avant-bras qui frappe est étalé sur
  l'espace balayé depuis l'image précédente, plus une traînée effilée.
  ([Game Developer, 5 tips for 2D game animation](https://gamedeveloper.com/art/5-tips-for-making-great-animations-for-2d-games),
  [RebusFarm, smear frames](https://rebusfarm.net/blog/smear-frames-in-animation-how-animators-create-fast-and-dynamic-motion))
- **Aplats, palette courte, pas de transparence** : l'étincelle utilise
  4 couleurs (bleu pour une parade, orange pour un coup reçu), la poussière 3.
- **Idle de combat** : un rebond régulier sur les jambes, les épaules et les
  poings qui suivent en décalé, pour que le personnage ait l'air prêt à
  bouger sans attirer l'œil. ([Slynyrd, Pixelblog 52 : Idle Fighting Stance](https://www.slynyrd.com/blog/2024/9/26/pixelblog-52-idle-fighting-stance),
  [AnimSchool, Breathing Life into Idle Animations](https://blog.animschool.edu/2024/06/14/breathing-life-into-idle-animations))
- **Boucle d'idle qui ne se voit pas** : périodes différentes pour chaque
  partie du corps (grâce aux décalages) et paliers irréguliers dans le repos.

