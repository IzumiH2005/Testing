# Analyse : coup de pied retourné du bagarreur

Demande de l'utilisateur : « un simple coup de pied retourné ».

Coup de pied arrière en tournant (« spinning back kick », ushiro geri en karaté, dwi chagi en
taekwondo) depuis `poses/garde_ouverte_bagarreur.json` (lacet +45, trois quarts face, garde de
droitier : pied gauche devant = jambe F, pied droit derrière = jambe N, côté caméra).

Animation : `anims/coup_de_pied_retourne.json`, générée par
`tools/gen_coup_de_pied_retourne.py`, suivie de `garde_ouverte_idle_bagarreur`.

« Simple » : pas de saut, pas de pas d'élan. Il tourne sur le pied avant, frappe du talon droit
derrière lui, finit le tour et repose le pied droit à sa place de garde. Un tour complet : on
retombe exactement sur la garde.

## 1. La logique du mouvement

1. **Pourquoi tourner.** Le coup de pied arrière est le plus puissant des coups de pied : la
   jambe pousse dans l'axe, avec les fessiers, les ischio-jambiers et le quadriceps ensemble.
   Pour le donner vers un adversaire qui est devant, il faut lui présenter le dos : le corps
   tourne d'un demi-tour sur le pied avant. La rotation ajoute de la vitesse au talon.
2. **Sens de rotation.** On tourne du côté de la jambe qui frappe : l'épaule et la hanche
   droites (arrière, côté caméra) partent vers l'arrière, la poitrine passe face à la caméra
   (lacet 45 → 90), puis le dos se présente à l'adversaire (lacet 180). C'est le sens qui
   laisse la jambe arrière libre de partir.
3. **La tête mène.** La tête tourne en premier et cherche la cible par-dessus l'épaule droite
   (« spotting ») : on ne frappe pas à l'aveugle. Puis les épaules, puis le bassin, puis la
   jambe. C'est la chaîne de la rotation (tête → épaules → bassin → jambe).
4. **Le pied d'appui pivote.** Le pied avant (gauche) reste planté et tourne sur l'avant du
   pied : à la frappe, le talon d'appui pointe vers l'adversaire. Le bassin vient se placer
   au-dessus de ce pied avant la rotation (sinon il tomberait).
5. **L'armé.** Pendant le demi-tour, le genou droit monte devant la poitrine, le talon près
   de la fesse : la jambe est repliée, elle tourne avec le corps sans traîner. L'armé est fini
   quand le dos fait face à l'adversaire.
6. **La frappe.** Le talon part en ligne droite vers l'arrière, à hauteur du ventre adverse
   (y ≈ 95), la plante du pied vers la cible, orteils vers le sol. La hanche s'étend, le genou
   se déplie. Le buste penche vers l'avant (côté opposé à la cible) en contrepoids : tête,
   buste et jambe forment une ligne presque droite, en léger « T » avec la jambe d'appui.
   La hanche ne s'ouvre pas : le genou pointe vers le sol (sinon c'est un coup de pied
   latéral).
7. **Le retour.** Le genou se replie aussitôt (on ne laisse pas la jambe tendue à saisir), le
   corps continue de tourner dans le même sens, le buste se redresse, et le pied droit se
   repose derrière, à sa place de garde. Un tour complet (lacet 45 → 405 ≡ 45).
8. **Les bras.** Ils ne font rien de grand : poings serrés près du visage, coudes rentrés, ils
   tournent avec le buste et protègent la tête. À la frappe, quand le buste penche, les poings
   restent devant le visage (garde), le coude gauche (F) s'écarte un peu pour l'équilibre.
9. **Stature du bagarreur** (règle 6) : épaules jamais enroulées, `epaule*_av` ≤ 0. Même buste
   penché à la frappe, le dos reste droit (la flexion vient de la hanche d'appui, pas d'un dos
   rond) et les épaules restent en arrière.

## 2. Anatomie

| Partie | Articulation | Muscles | Rôle |
|---|---|---|---|
| Tête | rotation du cou (vers la droite, puis par-dessus l'épaule) | sterno-cléido-mastoïdien, splénius | mène la rotation, trouve la cible |
| Jambe d'appui (gauche, F) | cheville (pivot sur l'avant du pied), genou plié 25-35°, hanche : flexion 40-55° à la frappe, rotation | mollet, quadriceps, fessiers, rotateurs de hanche | porte tout le poids, pivote, donne la rotation |
| Bassin | rotation sur la hanche d'appui, puis bascule vers l'avant | fessiers, obliques | suit les épaules, se met en ligne avec la jambe qui frappe |
| Tronc | rotation (épaules en avance sur le bassin), puis flexion à partir de la hanche, dos droit | obliques, érecteurs du rachis (gainage) | transmet la rotation ; à la frappe, contrepoids |
| Jambe qui frappe (droite, N) — armé | hanche : flexion 90-100° ; genou : flexion 120-130° ; cheville : flexion (pied relevé) | psoas, droit fémoral, ischio-jambiers | replie la jambe contre le corps pendant le tour |
| Jambe qui frappe — frappe | hanche : extension (cuisse 15-25° derrière l'axe du bassin) ; genou : extension complète ; cheville relevée (on frappe du talon) | grand fessier, ischio-jambiers, quadriceps | pousse le talon en ligne droite vers l'arrière |
| Épaules / bras | épaules basses, omoplates neutres ou en arrière ; coudes pliés 110-130° | deltoïdes, biceps (tenue) | garde du visage, équilibre |

L'extension de hanche d'un vrai corps est limitée (≈ 20-30° derrière l'axe du bassin). Si la
jambe est à l'horizontale derrière, c'est parce que le bassin a basculé vers l'avant d'autant :
bassin penché ≈ 60-65°, cuisse ≈ 20-25° en extension par rapport au bassin.

## 3. Les phases (60 images/s)

| Image | Phase | Ce qui se passe |
|---|---|---|
| 0 | garde | pose de garde, telle quelle |
| 0-6 | transfert | le bassin glisse vers le pied avant (x 0 → ≈ 14) et descend un peu (y 84 → 81) ; la tête commence à tourner ; le pied arrière s'allège |
| 6-15 | demi-tour | lacet 45 → 165 ; la tête et les épaules en avance sur le bassin (torsion) ; le pied droit quitte le sol vers l'image 8, le genou monte ; le pied gauche pivote sur place |
| 15-19 | armé | lacet 165 → 180 ; genou droit devant la poitrine, talon près de la fesse ; le buste commence à pencher ; le regard sur la cible par-dessus l'épaule |
| 19-22 | frappe, contact à 22 | le talon part droit vers l'arrière ; hanche et genou s'étendent ; buste penché en contrepoids ; lacet 180 → 186 |
| 22-27 | tenue | dépassement léger puis tenue de la ligne |
| 27-35 | rappel | le genou se replie, le buste se redresse, la rotation continue (lacet 186 → 300) |
| 35-44 | fin du tour | lacet 300 → 400 ; le pied droit descend et se pose derrière, à sa place de garde (x ≈ −29,5) ; le bassin revient entre les pieds |
| 44-54 | garde | lacet 405 ; bassin x 0, y 84 ; bras en garde |

## 4. Chaque articulation, tous ses axes, à chaque clé

Conventions du rig : `root` positif = buste penché en avant ; `thigh*` relatif au bassin
(positif = genou devant, négatif = extension) ; `shin*` = flexion du genou ; `foot*` positif =
pointe relevée ; `lacet` positif = la poitrine tourne vers la caméra ; `torsion` = épaules par
rapport au bassin ; `neck_r` = rotation de la tête. Les chevilles sont placées par cinématique
inverse (`vise`) en coordonnées du monde ; les valeurs de genou ci-dessous sont celles
attendues.

| Clé | lacet | bassin x / y | root (buste) | torsion / torsionBassin | neck / neck_r (tête) | jambe F (appui) : cheville, genou, hanche | jambe N : cheville (monde), hanche, genou, cheville | bras N (armN, _p, foreN) / bras F (armF, _p, foreF) ; omoplates av |
|---|---|---|---|---|---|---|---|---|
| 0 garde | 45 | 0 / 84 | −2 | −4 / −12 | 3 / 0 | (21,8 ; 8,5), genou 36, hanche 26 | (−29,5 ; 13,5), 33 (genou), hanche −11 | −5, 80, 100 / 31, −40, 95 ; 0 / −1 |
| 6 transfert | 60 | 12 / 81 | 4 | −15 / −12 | 3 / tourne de 25 vers la droite | plantée, genou 40 | plantée, pied arrière qui s'allège | coudes rentrés : 20, 40, 120 / 40, −30, 120 ; ≤ 0 |
| 15 demi-tour | 165 | 18 / 82 | 12 | −20 / 0 | 5 / tête 40 en avance (cible par-dessus l'épaule) | plantée, genou 35 | levée : hanche 90, genou 125 (armé presque fini) | idem, poings au visage |
| 19 armé | 180 | 18 / 82 | 25 | −10 / 0 | 0 / tête vers la cible (+x), par-dessus l'épaule | plantée, genou 35 | hanche 100, genou 130, talon devant la fesse, cheville relevée 20 | idem |
| 22 contact | 186 | 16 / 80 | 60 | 0 / 0 | −30 (relève la tête pour garder la cible) / vers la cible | plantée, genou 30, hanche ≈ 55 | talon à (≈ 105 ; 95) : hanche −22, genou 5, cheville relevée 20 ; genou vers le sol | poings au visage, coude F un peu écarté (armF_p −50) |
| 26 tenue | 186 | 16 / 80 | 58 | 0 / 0 | idem | idem | idem, genou 10 | idem |
| 32 rappel | 250 | 16 / 82 | 25 | −10 / 0 | 0 / revient vers l'avant | plantée | hanche 80, genou 125 | idem |
| 40 pied posé | 380 | 6 / 82 | 5 | −6 / −12 | 3 / 0 | plantée | cheville à (−29,5 ; 13,5) : posée | garde |
| 54 garde | 405 | 0 / 84 | −2 | −4 / −12 | 3 / 0 | (21,8 ; 8,5) | (−29,5 ; 13,5) | garde exacte |

Le pied d'appui F garde la même cheville du début à la fin (planté) : seul le corps tourne
au-dessus.

## 5. Ce qui se voit à lacet +45 (vue de jeu) et de profil

- **Transfert** : il penche un peu vers le pied avant, la tête part à droite.
- **Demi-tour** : la poitrine passe face à la caméra (lacet 90), les bras serrés devant ; le
  genou droit monte. Puis on voit son flanc, il regarde vers la droite par-dessus l'épaule.
- **Armé** : de profil, il regarde vers la gauche avec la tête tournée vers la droite, genou
  droit replié devant le ventre : une silhouette ramassée sur une jambe.
- **Contact** : silhouette en ligne : la jambe droite tendue à l'horizontale vers la droite
  (vers l'adversaire), talon devant, buste penché vers la gauche, tête relevée qui regarde la
  cible ; la jambe d'appui verticale. C'est le dessin qui doit se lire immédiatement de profil.
- **Retour** : la jambe se replie, il finit le tour (on voit son dos, lacet 270) et retombe
  en garde.

## 6. Références

- Biomécanique du coup de pied arrière en tournant (taekwondo, dwi dollyo chagi / dwi
  chagi) : rotation menée par la tête et les épaules, armé du genou contre la poitrine,
  extension simultanée de la hanche et du genou ; le contrepoids du buste.
- `analyses/anatomie.md` : amplitudes de hanche (extension ≈ 30°), de genou, rotation du cou.
- `analyses/garde_ouverte_bagarreur.md` : garde de départ et d'arrivée.
- Bible :
  - A2 : anticipation (transfert du poids, la tête qui part) ;
  - A3 : chaîne (tête → épaules → bassin → jambe) ;
  - A bis : accélération jusqu'au contact, chevauchement (la rotation finit pendant que la
    jambe se déplie déjà).

## 7. Contrôles

1. Le pied d'appui F ne glisse pas : sa cheville reste à ±0,5 de (21,8 ; 8,5) de 0 à 54.
2. Avant que le pied droit quitte le sol (image 8), le bassin est au-dessus du pied d'appui à
   ±8 près en x (équilibre).
3. La tête mène : de 6 à 19, la tête est tournée plus loin que les épaules, et les épaules
   plus loin que le bassin, dans le sens de la rotation.
4. Au contact (22) : la cheville N est à y 85-105, à plus de 75 devant le bassin vers +x ; le
   genou N tendu (≤ 10) ; la cuisse en extension par rapport au bassin entre −15 et −30 ;
   l'écart vertical entre la hanche et la cheville N < 20 (jambe presque horizontale).
5. De 19 à 22, la cheville N avance vers +x à chaque image et ses écarts augmentent.
6. Le genou N reste vers le sol au contact (pas de hanche ouverte de côté).
7. `epaule*_av` ≤ 0 à toutes les images ; le buste penche par la hanche, pas par le dos
   (`spineLow`, `chest` ≤ 15).
8. Rien ne traverse (`--verifier`) : jambe dans jambe à l'armé, poings dans la tête, bras dans
   le tronc pendant le tour.
9. Images 0 et 54 = garde exacte (lacet 405 ≡ 45 : même dessin).
10. Le pied droit se repose exactement à sa place de garde (−29,5 ; 13,5) et ne glisse plus
    ensuite.
