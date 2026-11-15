# Stickfight

Base d'un jeu de combat de stickmen dans Godot. Cette première étape
fournit le **modèle** : un stickman riggé, des poses réglables au dixième de
degré, un atelier pour les composer à la souris ou au clavier, et un outil de
rendu en ligne de commande pour itérer sans ouvrir l'éditeur.

Le style vise celui des vidéos de référence : grosse tête ronde, trait gras à
bouts ronds, et un petit pied en crochet arrondi au bout de chaque jambe
(os `footN`, `footF`, articulés à la cheville). Les proportions mesurées
sur ces vidéos, les amplitudes articulaires et les notes sur l'animation de
combat sont dans [RECHERCHE.md](RECHERCHE.md). La liste des animations à
produire par personnage (communes et propres, d'après Tekken 8) est dans
[INVENTAIRE.md](INVENTAIRE.md).

## Lancer

1. Installer [Godot 4.3](https://godotengine.org/download/) (version standard,
   pas .NET).
2. Ouvrir `stickfight/project.godot` dans Godot, puis lancer le projet (F5).
   La scène principale est l'atelier.

## L'atelier

La planche est à gauche, le panneau de réglages à droite.

| Geste | Effet |
|---|---|
| Glisser une poignée **ronde** | Fait tourner l'os qui finit à cette articulation (coude → épaule, genou → hanche, épaule → poitrine, tête → cou, taille → bas du dos) |
| Glisser une poignée **carrée** (main, cheville) | Cinématique inverse : le bras ou la jambe suit la souris |
| Glisser le **bassin** (carré vert) | Déplace tout le corps ; avec « Pieds fixés », les jambes se replient pour garder les chevilles en place |
| **Ctrl** + glisser la taille | Bascule le bassin (tout le tronc s'incline) |
| Flèches | Ajuste l'élément sélectionné de 1 (Maj : 5, Alt : 0,1) ; sur un angle, ← → tournent ; sur une main ou une cheville, les quatre flèches la déplacent |
| `[` `]` | Articulation précédente ou suivante |
| Ctrl+Z, Ctrl+Y | Annuler, rétablir |
| Ctrl+S | Enregistrer la pose |

Couleurs des poignées : orange = membres proches (devant le tronc), bleu =
membres lointains (derrière), vert = tronc. Jaune = sélection.

Le panneau donne chaque angle avec un curseur et un champ numérique (deux
décimales). Il offre aussi :

- **Pieds fixés** : les pieds restent plantés pendant qu'on modifie le reste.
- **Amplitudes humaines** : bloque chaque articulation dans son amplitude
  réelle.
- **Fantôme** : garde la pose actuelle en rose derrière la figure pour comparer
  avant et après.
- **Retourner**, **Échanger proche / loin**, **Poser au sol**, **Neutre**.
- L'enregistrement dans `poses/<nom>.json`, et le JSON de la pose, modifiable
  et réapplicable.

## Rendu en ligne de commande

`tools/rendu.sh` dessine une ou plusieurs poses en PNG avec le même code de
dessin que l'atelier. C'est l'outil pour itérer finement : changer un angle,
regarder, recommencer.

```sh
export GODOT=/chemin/vers/Godot_v4.3-stable_linux.x86_64   # sinon « godot » du PATH
tools/rendu.sh poses/garde.json -o /tmp/garde.png --debug --grid
tools/rendu.sh poses/garde.json --set foreN+=3 --set chest-=2 -o /tmp/essai.png
tools/rendu.sh poses/garde.json --reach armN=40,140 --pin --save
tools/rendu.sh poses/garde.json poses/repos.json -o /tmp/compare.png
tools/rendu.sh poses/repos.json poses/garde.json --overlay -o /tmp/onion.png
tools/rendu.sh poses/garde.json --print     # angles, articulations, amplitudes dépassées
```

Toutes les options sont décrites en tête de `tools/rendu.gd`. Sans affichage,
le script passe par `xvfb-run`.

## Le modèle

- **Repère** : x vers l'avant du personnage, y vers le haut, sol à y = 0,
  unités ≈ cm. Un personnage debout mesure environ 180. La conversion vers le
  repère de Godot (y vers le bas) se fait seulement au dessin.
- **Os** (`scripts/stick_rig.gd`) : bassin → bas du dos → poitrine → cou ;
  deux bras (épaule, coude) et deux jambes (hanche, genou, cheville) attachés à
  la poitrine et au bassin.
- **Angles** : en degrés, mesurés depuis la position de repos (debout, bras le
  long du corps). Le signe est sémantique : positif = flexion ou vers l'avant.
  Le même nombre veut donc dire la même chose pour la jambe proche et la jambe
  lointaine, et les limites d'amplitude s'écrivent comme dans un tableau
  médical.
- **Proche / loin** : les membres proches (N) sont dessinés devant le tronc,
  les lointains (F) derrière.
- **Cinématique inverse** : analytique, deux os, par la loi des cosinus. Des
  deux solutions (coude en haut ou en bas), le solveur garde celle qui respecte
  les amplitudes, puis celle qui bouge le moins.
- **Styles** : `epais` (grosse tête, trait gras, celui des vidéos) et `fin`.
  Les longueurs de chaque style sont dans `STYLES`.

Format d'une pose (`poses/*.json`) :

```json
{
  "nom": "garde", "style": "epais", "x": 0, "y": 72.13, "facing": 1,
  "angles": { "root": 2, "spineLow": 6, "chest": 4, "neck": 6,
              "armF": 65.29, "foreF": 137.75, "armN": 38.96, "foreN": 112.7,
              "thighF": -3.82, "shinF": 62.5, "footF": 11.96,
              "thighN": 58.31, "shinN": 61.79, "footN": 5.48 }
}
```

`x`, `y` = position du bassin ; `facing` = 1 (regarde à droite) ou −1.

## Animations

Le dossier `anims/` contient des animations par poses clés, jouées à
60 images par seconde (le format complet est décrit en tête de
`scripts/stick_anim.gd`).

| Animation | Durée | Contenu |
|---|---|---|
| `idle_repos` | 260 i, en boucle | Debout détendu : respiration lente, léger transfert de poids, deux paliers pour que la boucle ne se devine pas |
| `mise_en_garde` | 40 i | Du repos à la garde : anticipation (le corps se tasse), pas en avant, pied arrière qui glisse, poussière à chaque appui ; enchaîne sur `garde_ouverte_idle` |
| `garde_ouverte_idle` | 96 i, en boucle | Garde ouverte, la garde par défaut quand G est tenu (prêt à se battre) : mains plus avancées et plus écartées, poing avant à hauteur d'épaule, buste plus droit ; respiration lente, bras qui suivent avec retard |
| `garde_idle` | 112 i, en boucle | Garde fermée, défensive (quand il bloque ou s'apprête à bloquer) : poings serrés devant le visage, rebond sur les jambes, poings qui suivent avec 5 à 9 images de retard |
| `garde_fermer` | 8 i | Garde ouverte → garde fermée : les mains remontent vite devant le visage, menton rentré, léger tassement ; puis `garde_idle` |
| `garde_ouvrir` | 12 i | Garde fermée → garde ouverte : les mains se relâchent et repartent devant ; puis `garde_ouverte_idle` |
| `blocage_bas` | 44 i | Les mains descendent frapper le pied d'un coup visant le ventre, sans se baisser : armé (f4), contact (f8, arrêt sur impact 7 i, étincelle, secousse), écrasé, tenue, retour en garde |
| `coup_de_pied_ventre` | 56 i | Pied direct (teep) de la jambe avant, pour le duo : pas glissé, genou armé, contact (f17), pied rabattu vers le bas par le blocage, reprise de distance |
| `duo_blocage` | 110 i | Les deux ensemble : les contacts sont calés sur la même image globale |
| `armure_encaisse` | 19 i, couche | Armure (Power Crush) : encaisser sans broncher. Ce n'est pas une animation qui remplace la courante mais une **couche** posée par-dessus : le combattant continue ce qu'il faisait (marche, garde, coup). À l'impact, le buste est déjà tassé de 2,5 en arrière et de 1,5 vers le bas, la tête part en avant, les bras se serrent ; arrêt sur impact 11 i pendant lequel il tremble, puis tout revient en 19 i. Les pieds au sol ne bougent pas (la jambe est recalculée pour garder la cheville en place). Le corps s'entoure d'un liseré rouge qui s'éteint en 16 i, étincelle rouge au ventre, secousse |
| `duo_armure` | 150 i | B marche en garde, encaisse le pied direct de A sous armure sans s'arrêter, puis se pose en garde ouverte ; A, dont le coup a rebondi, recule en backdash |
| `projection_cassee` | 38 i, avance 6 | Celui dont la projection est cassée : grand pas glissé depuis la garde, les deux mains saisissent le col (contact f8), il commence à tirer, puis ses bras sont chassés vers le haut (f14), le buste part en arrière et les pieds glissent ; il se rattrape en garde |
| `casse_projection` | 38 i, recule 11 | Celui qui casse : saisi au repos (f8), tiré vers l'avant, les mains montent entre les bras adverses et les avant-bras les chassent vers le haut (f14, arrêt 6 i, étincelle de parade) ; il glisse en arrière, les bras retombent, `idle_repos` |
| `duo_projection_cassee` | 90 i | Ctrl + K : les deux ensemble, à 125 de distance, saisie et casse calées sur la même image |
| `direct` | 22 i, avance 12 | Direct du bras avant, provisoire, pour le duo : pas glissé, contact au visage (f6, arrêt 6 i), retour en garde |
| `pied_bas` | 30 i | Coup de pied bas de la jambe avant dans le tibia, provisoire, pour le duo : charge, genou armé (f7), contact (f10), tenu, retour en garde |
| `etre_pare_haut` | 46 i, recule 37 | Être paré vers le haut (après `parade_haute_poing` ou `parade_haute_pied`) : réaction réutilisable, jouée à l'image qui suit le contact avec un fondu depuis la pose du coup. Le bras est chassé au-dessus de la tête, le buste s'ouvre en arrière, il est repoussé : le pied arrière décolle et se pose loin (f13), l'avant glisse ; le bras retombe, il reste ouvert, bras bas, pendant la fenêtre de contre de la parade, puis ramène le pied avant en garde |
| `etre_pare_bas` | 44 i, recule 21 | Être paré au milieu ou en bas (après `parade_moyenne` ou `parade_basse`) : même usage. La jambe est chassée, il sautille en arrière sur l'appui, la jambe repliée, les bras battent l'air (f4) ; le pied retombe (f8), il absorbe, ouvert, bras bas, puis se remet en garde sur place |
| `touche_tete_leger` | 22 i, recule 10 | Touché à la tête par un coup léger. Contact dès l'image 1 (arrêt sur impact 6 i, tremblement 1,3, étincelle de coup sur la tête) : la tête part en arrière, la garde s'ouvre ; le buste suit la tête (f4) et les bras retombent, ouverts ; les pieds glissent d'un pas, la tête revient (f9), puis les mains remontent et `garde_idle`. Marche depuis la garde (fondu 1, la garde est cassée) comme depuis le repos (fondu 3, les bras sont déjà bas) |
| `touche_tete_lourd` | 36 i, recule 29 | Touché à la tête par un coup lourd. Contact dès l'image 1 (arrêt sur impact 10 i, tremblement 2, secousse, grosse étincelle de coup) : la tête est arrachée en arrière, le buste se cambre, le bras avant s'envole vers le haut et l'arrière retombe ; le pied arrière décolle (f5) et se pose loin derrière (f10, poussière), l'avant traîne pour le rejoindre (f16) pendant que la tête retombe en avant ; les genoux absorbent, bras ballants, puis les mains remontent et `garde_idle` |
| `touche_ventre_leger` | 24 i, recule 12 | Touché au ventre, léger. Contact dès l'image 1 (arrêt sur impact 6 i, étincelle de coup à la taille) : le bassin part en arrière, le buste se plie et la tête vient en avant ; les mains se referment bas vers le ventre (f5), le pied avant recule pendant que le buste se redresse, mains serrées contre le corps, puis elles remontent en diagonale vers la garde et `garde_idle` |
| `touche_ventre_lourd` | 46 i, recule 33 | Plié en deux. Contact dès l'image 1 (arrêt sur impact 10 i, tremblement 2, secousse, grosse étincelle à la taille) : le buste se plie d'un coup, les deux pieds glissent en arrière (poussière), plié en deux les mains serrées sur le ventre ; le pied arrière décolle et se replace (f12-16), il reste plié, vulnérable, jusqu'à f26, puis se redresse, mains contre la poitrine, le pied avant revient, les mains remontent et `garde_idle` |
| `touche_jambe` | 32 i, recule 6 | Touché à la jambe (coup bas dans le tibia). Contact dès l'image 1 (arrêt sur impact 7 i, tremblement 1,4, étincelle sur le tibia) : le pied avant est chassé en arrière et décolle à peine, les genoux plient, le buste tombe en avant et la tête aussi ; les mains s'ouvrent pour l'équilibre (f5), le pied se repose (f9, poussière), il se relève en remontant les mains serrées contre le corps, puis `garde_idle` |
| `touche_accroupi` | 21 i, recule 11 | Touché accroupi : depuis `accroupi_idle` ou `garde_basse` (fondu 1). Contact dès l'image 1 (arrêt sur impact 6 i, étincelle de coup à l'épaule) : le buste et la tête partent en arrière, la garde s'ouvre ; les deux pieds glissent ensemble (f4, poussière) sans se relever, les bras rejetés vers le bas ; il rebondit en avant, les genoux absorbent (f9), les mains remontent par le haut, puis `accroupi_idle` |
| `sonne` | 64 i, en boucle | Sonné, titubant : à jouer après un contre ou une garde brisée (fondu 10 depuis la réaction), puis `garde_idle` avec un fondu de 14 quand il se reprend. Genoux pliés, buste tassé, tête qui pend, bras ballants bas. Le poids part en arrière et la tête bascule (f14), il titube en avant : le pied avant décolle et se repose un peu devant (f24-30), il plonge sur les genoux (f40), puis le pied avant revient à sa place (f50). Pieds et bassin reviennent exactement au départ, la boucle ne dérive pas |
| `chute_arriere` | 48 i, puis `au_sol` | Propulsé en arrière par un coup lourd, il retombe sur le dos. Impact (f1, hitstop 12) : poitrine enfoncée, bras qui s'envolent. Arraché du sol (f6), la jambe avant fouette ; il bascule en arrière en vol (f14) et rentre le menton avant le sol (f22). Le dos frappe le sol (f26, secousse et poussière), petit rebond des jambes (f31), les talons touchent (f38), puis la pose `au_sol` (f48), environ 90 px derrière son point de départ |
| `fauche` | 34 i, puis `au_sol` | Jambes balayées, il tombe sur le dos presque sur place (environ 15 px en arrière). Impact (f1, hitstop 9) : le pied avant est arraché vers le haut, les bras s'envolent. Les deux jambes partent (f5), il passe à l'horizontale en l'air, jambes hautes (f10), et le dos frappe le sol à plat (f14, secousse et poussière). Rebond des jambes (f19), talons au sol (f25), puis la pose `au_sol` (f34) |
| `effondrement` | 68 i, reste à plat ventre | Coup au ventre qui coupe les jambes : il s'effondre vers l'avant sans jamais basculer en arrière. Impact (f1, hitstop 12) : plié en deux, il recule en titubant ; les genoux lâchent et frappent le sol (f22, secousse et poussière), il reste affaissé à genoux (f32). Les bras cèdent (f34-36), le buste plonge (f38), les mains glissent sous lui et le visage et la poitrine touchent le sol, fesses encore en l'air (f44, secousse) ; les jambes s'étendent en glissant derrière (f50-61), puis la pose `au_sol_ventre` (f68), qu'il garde |
| `au_sol` | 160 i, en boucle | Sur le dos, sonné, après `chute_arriere` ou `fauche`. Deux respirations lentes par boucle : à l'inspiration, les épaules et la tête se soulèvent un peu et la main posée sur le ventre remonte (f28, f108). Le talon de la jambe pliée glisse vers les fesses pendant la première (le genou monte, f60-80) et repart pendant la seconde (f140). Le pied reste au sol, la boucle revient exactement à la pose `au_sol` |
| `touche_au_sol` | 36 i, puis `au_sol` | Couché sur le dos, frappé au ventre. Impact (f1, hitstop 10, secousse) : écrasé contre le sol, le menton rentre et les bras s'écartent. Le choc se propage (f6) : les épaules et les jambes décollent, les bras se replient ; il retombe à plat (f12, poussière) avec un petit rebond (f16), puis s'affaisse dans la pose `au_sol` (f36). Presque pas de glissement : le coup écrase vers le bas |
| `frappe_au_sol` | 58 i, puis `garde_idle` | Piétinement du talon sur un adversaire couché, depuis la garde. Le pied arrière se ramène (pas rassemblé, f11), le genou avant monte haut, pied sous le genou (f18), puis le talon descend presque à la verticale, le buste au-dessus (f22, contact) et appuie (f28). Le pied remonte, repasse au-dessus de l'adversaire et se repose devant lui (f40), le pied arrière recule (f48) : retour en garde à peu près à la place de départ, pour ne pas finir debout sur lui |
| `releve` | 52 i, puis `garde_idle` | Relevé normal depuis `au_sol` (couché sur le dos). Le bras loin descend au sol derrière lui (f4), il se redresse en appui sur la main (f9) et s'assoit, le pied loin ramené contre lui (f17). Il pousse sur la main et les pieds, le bassin passe au-dessus des pieds (f24), accroupi (f30), le pied arrière recule (f36) et il se remet en garde (f42, poussière) un peu plus loin que sa tête, du côté des pieds |
| `releve_roulade` | 44 i, puis `garde_idle` | Relevé en roulade arrière (tech roll) depuis `au_sol`. Genoux à la poitrine, mains près des oreilles (f5), le bassin passe au-dessus des épaules, jambes par-dessus la tête et mains qui poussent (f10), les pieds touchent derrière la tête (f15, poussière), à quatre pattes (f18), accroupi (f23), il se redresse (f29) et se remet en garde (f35, poussière) environ 100 px plus loin, du côté de sa tête, donc loin de l'adversaire |
| `duo_pare_haut` | 100 i | Alt + K : A lance un direct, B le pare vers le haut (fenêtre de contre), A est repoussé |
| `duo_pare_bas` | 110 i | Alt + Maj + K : A lance le pied direct, B le pare au milieu, A est repoussé en sautillant |
| `duo_touche_tete` | 80 i | Y : A lance un direct, B en garde le prend au visage |
| `duo_touche_tete_repos` | 80 i | Maj + Y : le même, B au repos (fondu de 3 i qui le met en position de garde pendant l'impact) |
| `duo_touche_tete_lourd` | 90 i | Ctrl + Y : B en garde prend le direct en coup lourd (le coup du duo reste le direct, en attendant les coups du personnage 1) |
| `duo_touche_ventre` | 100 i | O : A lance le coup de pied direct, B en garde le prend au ventre (léger) |
| `duo_touche_ventre_lourd` | 110 i | Maj + O : A lance le coup de pied direct, B en garde le prend en plein ventre et se plie en deux |
| `duo_touche_jambe` | 80 i | I : A lance un coup de pied bas, B en garde le prend dans le tibia |
| `duo_touche_accroupi` | 90 i | Maj + I : A lance le coup de pied direct, B accroupi le prend à l'épaule |
| `duo_sonne` | 200 i | N : A lance un direct, B le prend en coup lourd (`touche_tete_lourd`), enchaîne sur `sonne` (g52) puis se remet en garde (g180) |
| `duo_chute_arriere` | 150 i | C : A lance un coup de pied au ventre, B est propulsé (`chute_arriere`) et reste au sol (`au_sol`) |
| `duo_fauche` | 110 i | Maj + C : A lance un coup de pied bas, B est fauché (`fauche`) et reste au sol (`au_sol`) |
| `duo_effondrement` | 160 i | Ctrl + C : A lance un coup de pied au ventre, B s'effondre (`effondrement`) et reste à plat ventre |
| `duo_touche_au_sol` | 120 i | Ctrl + Maj + C : B est couché sur le dos, A s'approche et lui écrase le ventre du talon (`frappe_au_sol`), B encaisse (`touche_au_sol`) |
| `duo_releve` | 230 i | Alt + C : B prend un coup de pied au ventre, tombe sur le dos (`chute_arriere`), reste au sol (`au_sol`) puis se relève en garde (`releve`) |
| `duo_releve_roulade` | 225 i | Alt + Maj + C : même chute que `duo_releve`, puis B se relève par une roulade arrière (`releve_roulade`), loin de A |
| `sortie_de_garde` | 60 i | De la garde ouverte au repos, sur place : le poids bascule en arrière, le pied avant revient en se posant par la pointe, puis le pied arrière repasse devant et le bassin remonte ; les mains retombent le long du corps, le bras du pied qui avance passe devant (contrepoids) ; enchaîne sur `idle_repos` |
| `marche_detendue` | 56 i, en boucle, avance 76 | Marche normale depuis le repos, sans garde : bras ballants en opposition des jambes, bassin qui monte et descend sur chaque appui |
| `marche_detendue_depart` | — | Du repos à la boucle : transfert de poids, premier pas plus court |
| `marche_detendue_arret_court`, `_arret_pas` | — | Arrêts au repos depuis l'un ou l'autre pied de la boucle (pied ramené à côté de l'autre, ou un dernier pas freiné) |
| `marche_detendue_arriere` | 64 i, en boucle, recule 48 | Recul détendu : pas plus courts, la pointe se pose avant le talon, le buste reste droit |
| `marche_detendue_arriere_depart`, `_arret_pas`, `_arret_deux_pas` | — | Départ et arrêts au repos du recul détendu |
| `course` | 40 i, en boucle, avance 160 | Course à vitesse moyenne : appui de 14 images (amorti, talon qui se lève), 6 images de vol, bras pliés en opposition, buste penché qui plonge à l'amorti |
| `course_depart` | 66 i | Du repos à la boucle : anticipation (petit recul, on s'abaisse, les bras s'arment), puis trois appuis qui accélèrent ; finit exactement sur l'image 0 de la boucle |
| `course_arret_n`, `_arret_f` | 56 et 58 i | Freinage depuis l'appui N (image 0) ou F (image 20) : buste qui part en arrière, pied posé loin devant, genoux qui amortissent, bras vers l'avant pour l'équilibre, puis retour au repos |
| `sprint` | 28 i, en boucle, avance 243 | Course à pleine vitesse, exagérée : buste couché à ~43°, tête rentrée, foulée longue et vol de 8 images, genou qui monte haut devant, talon qui fouette jusqu'aux fesses derrière, bras pliés qui balaient large ; lignes de vitesse derrière le bassin |
| `sprint_depart` | 50 i | Du repos au sprint : anticipation courte et profonde (le bassin tombe, le buste plonge, les bras s'arment), poussée explosive avec poussière, trois appuis bas qui accélèrent, buste couché à ~55° qui se relève jusqu'à l'inclinaison de la boucle ; finit sur l'image 0 de la boucle |
| `sprint_arret_n`, `_arret_f` | 46 et 54 i | Freinage en glissade depuis l'appui N (image 0) ou F (image 14) : le pied de devant se plante jambe presque tendue et glisse ~40 cm dans une gerbe de poussière, le bassin s'assied, le buste bascule en arrière, les deux bras partent devant ; en `_n` le pied arrière traîne sur la pointe, en `_f` il fait un pas de rattrapage devant ; retour au repos |
| `marche_arriere` | 30 i, en boucle, recule 14 | En garde fermée (← en garde ferme d'abord la garde). Plus lente et prudente : la jambe avant pousse, le bassin recule, le pied arrière se pose loin (la hanche ne s'étend pas au-delà de 30°, d'où ce bassin qui part avant le pied), puis le pied avant se ramène en glissant |
| `marche_avant` | 28 i, en boucle, avance 18 | En garde ouverte, pas chassé : le pied avant s'avance au ras du sol (4 de haut), le poids passe dessus, le talon arrière se lève et le pied arrière glisse ; les mains suivent avec retard |
| `dash_avant` | 28 i, avance 72 | Pas chassé avant rapide depuis la garde (double appui sur →) : le corps se tasse 3 images, le pied arrière pousse dans un petit nuage de poussière, vol rasant buste penché, le pied avant se plante loin devant, le pied arrière chasse au ras du sol pour retrouver l'écart de garde, puis petit rebond et retour en `garde_ouverte_idle` |
| `dash_arriere` | 28 i, recule 50 | Pas chassé arrière rapide depuis la garde (double appui sur ←) : le poids passe sur l'avant, la jambe avant pousse, petit vol bas, le pied arrière se pose loin et le buste part en arrière sous l'élan, le pied avant revient en glissant, rebond puis `garde_idle` ; la garde se ferme pendant le recul |
| `accroupi_entree` | 12 i, recule 12 | Depuis la garde ouverte ou fermée (↓ maintenu) : le pied arrière glisse vers l'avant sur la pointe, le bassin descend et recule pour que le genou arrière reste décollé du sol, le buste se penche, petit écrasement puis `accroupi_idle` |
| `accroupi_idle` | 96 i, en boucle | Accroupi en garde ouverte : respiration lente (le bassin s'abaisse et le dos se voûte à l'expiration), garde haute qui suit avec retard |
| `accroupi_sortie` | 16 i, avance 12 | ↓ relâché : appui bref, poussée des jambes, le pied arrière recule à sa place de garde, puis `garde_ouverte_idle` |
| `garde_basse` | 96 i, en boucle | Garde basse : accroupi comme `accroupi_idle`, garde fermée. Le buste se penche plus, les avant-bras se dressent devant le visage, coudes posés près du genou avant pour couvrir le ventre. Même respiration, les bras suivent avec retard |
| `garde_basse_entree` | 12 i, recule 12 | Depuis la garde (↓ + ← maintenus) : même descente qu'`accroupi_entree`, les poings remontent devant le visage pendant l'écrasement, puis `garde_basse` |
| `garde_basse_fermer` | 8 i | Accroupi en garde ouverte, ← : le buste se penche et les bras se referment devant le visage, puis `garde_basse` |
| `garde_basse_ouvrir` | 12 i | 10 images sans ← en garde basse : le buste se redresse et la garde se rouvre, puis `accroupi_idle` |
| `garde_basse_sortie` | 16 i, avance 12 | ↓ relâché : même relevé qu'`accroupi_sortie`, la garde reste fermée, puis `garde_idle` |
| `recul_garde_haut_leger` | 15 i, recule 5 | H en garde : coup bloqué debout. Contact dès l'image 1 (arrêt sur impact 5 i, tremblement, étincelle de garde devant la main avant) : les bras sont repoussés vers le visage, le buste se tasse en arrière et la tête suit avec retard, les deux pieds glissent ensemble sans se lever, puis le buste se redresse et `garde_idle` |
| `recul_garde_haut_moyen` | 21 i, recule 10 | Maj + H : même chose, arrêt 7 i, secousse, recul et tassement plus marqués |
| `recul_garde_haut_lourd` | 28 i, recule 18 | Ctrl + H : arrêt 10 i, grosse secousse, le bassin s'écrase et le buste part loin en arrière avant de revenir |
| `recul_garde_bas_leger` | 15 i, recule 4 | H en garde basse : coup bloqué accroupi, mêmes temps que le recul haut, les avant-bras encaissent devant le visage et les pieds glissent ensemble, puis `garde_basse` |
| `recul_garde_bas_moyen` | 21 i, recule 8 | Maj + H en garde basse |
| `recul_garde_bas_lourd` | 28 i, recule 14 | Ctrl + H en garde basse |
| `garde_repoussee` | 48 i, recule 48 | Ctrl + Maj + H en garde : très gros coup bloqué. Contact à l'image 1 (arrêt 12 i, grosse étincelle, secousse), les poings écrasés sur le visage ; le corps est chassé en arrière pendant que les pieds tiennent encore, puis les deux pieds décrochent et glissent en soulevant de la poussière. Pendant le freinage le buste se penche contre la poussée et la jambe arrière s'étire ; le pied arrière accroche en premier, le haut du corps continue sur son élan vers l'avant, puis le pied arrière se décolle et revient se poser pour retrouver la garde, puis `garde_idle` |
| `garde_brisee` | 62 i, recule 36 | J en garde : coup qui brise la garde. Contact à l'image 1 (arrêt 14 i, étincelle, secousse) : la garde est arrachée, la tête part en arrière ; les bras s'ouvrent en V et le buste se cambre, le pied avant traîne pendant que le pied arrière décolle et se pose loin derrière pour rattraper l'équilibre. Les genoux absorbent, les bras retombent bas et écartés, la tête pend : c'est la fenêtre vulnérable, où un nouveau coup bloqué est ignoré. Puis il se reprend : bras remontés en garde, le pied avant recule et se pose, puis `garde_idle` |
| `parade_haute_poing` | 34 i | P en garde : dévie un coup de poing visant le visage. L'avant-bras avant monte en biais (f3) et rencontre le poing à l'image 5 (arrêt 6 i, étincelle verte de parade) en le chassant vers le haut ; le bras suit le geste au-dessus de la tête, le buste à peine en retrait, puis la main redescend en garde et `garde_idle` |
| `parade_haute_pied` | 40 i | Maj + P : dévie un coup de pied haut (tempe, mâchoire). Contact plus tard (f7) et plus lourd (arrêt 8 i, grosse étincelle, secousse) : le buste cède en arrière, le bassin recule de quelques unités, l'avant-bras balaie la jambe vers le haut et loin au-dessus de la tête, puis il se replace |
| `parade_moyenne` | 36 i | Ctrl + P : dévie un coup au ventre. La main avant descend devant le plexus, le buste se penche un peu en avant au contact (f5, arrêt 7 i) et l'avant-bras chasse le coup vers le bas et sur le côté, puis remonte en garde |
| `parade_basse` | 36 i | Ctrl + Maj + P : dévie un coup bas (tibia). Le combattant fléchit les genoux (le talon arrière se lève), la main avant descend frapper le pied à l'image 6 (arrêt 7 i) et le rabat vers le sol, l'autre main protège le visage, puis il se relève en garde |
| `esquive_sway` | 30 i | 1 au repos : contre un direct au visage. Esquive détendue, sans garde, façon « ultra instinct » : le buste se penche juste assez en arrière, au dernier moment (f4), le bassin recule de 3, la tête passe hors de portée au contact (f7). Les bras restent pendants, le regard ne quitte pas l'adversaire ; il tient la pose un instant, puis revient calmement au repos et `idle_repos` |
| `esquive_slip` | 26 i | 2 : contre un direct. Un simple déport de la tête sur le côté, genoux à peine fléchis, le corps glissé vers la caméra (z −10), mains basses : le poing passe à côté de la tête, derrière elle à l'écran (f6). Très court, sans un geste de trop |
| `esquive_baisse` | 33 i | 3 : contre un crochet ou un circulaire à la tête. Il se plie aux hanches, genoux fléchis (bassin −27), le buste part en avant sous la trajectoire (f8), les bras pendent devant ; il se redresse sans hâte jusqu'au repos |
| `esquive_cote` | 34 i | 4 : contre un coup de pied appuyé. Pivot sur la plante du pied avant, qui reste cloué au sol : le corps fait un quart de tour complet et se retrouve entièrement de face (f10 à f20), jambes légèrement écartées, pointes un peu ouvertes, bras décollés du corps, détendus. La jambe arrière décrit un arc derrière lui et se pose de côté, le bassin s'abaisse à peine, hors de la ligne. Le pied adverse passe devant son ventre (f12, il est dessiné derrière l'attaquant) ; retour par le même pivot, puis `idle_repos`. Généré par `tools/gen_esquive_cote.gd` |
| `esquive_saut_arriere` | 30 i, recule 26 | 5 : contre un coup de pied hache (descendant). Se baisser serait inutile : petit saut en arrière, bras ballants, qui laisse le talon frapper le sol devant lui (f12) ; réception souple, debout, au repos |
| `esquive_saut_balayage` | 26 i | 6 : contre un balayage. Petit saut sur place, genoux remontés juste ce qu'il faut, la jambe adverse passe sous les pieds (f10) ; réception souple, bras pendants, `idle_repos` |
| `accroupi_repos_entree` | 28 i, recule 3 | Depuis le repos (↓ maintenu), sans passer par la garde : les genoux cèdent, la main avant part devant et se pose au sol devant le pied avant, le pied arrière monte sur la pointe, petit tassement sur la main puis `accroupi_repos_idle` |
| `accroupi_repos_idle` | 104 i, en boucle | Accroupi détendu, une main au sol : respiration lente (le dos se voûte à l'expiration), le bras libre suit avec retard. La main et les pieds restent fixes |
| `accroupi_repos_sortie` | 30 i, avance 3 | ↓ relâché : appui sur la main, poussée qui la décolle, le buste se relève, léger dépassement puis `idle_repos` |
| `saut_neutre` | 69 i, recule 16 | ↑ depuis le repos : flexion et bras en arrière, puis extension, les bras lancés vers le haut, et le talon quitte le sol avant la pointe. En vol, le centre de gravité suit une parabole exacte (g = 0,2725 par image²), les genoux remontent, puis les jambes se tendent vers le sol. Contact sur la pointe du pied avant, le second pied 2 images plus tard, talons qui retombent, amorti sans rebond jusqu'à la pose basse commune, puis `reception` |
| `saut_avant` | 72 i, avance 87 | ↑ + → : même mécanique, avec une poussée plus inclinée vers l'avant et les genoux groupés plus haut. Le pied avant touche le premier, devant le centre de gravité, ce qui le freine |
| `saut_arriere` | 70 i, recule 92 | ↑ + ← : la poussée part en arrière, le buste se redresse et les bras équilibrent vers l'avant. Le pied arrière touche le premier, puis le pied avant se pose |
| `reception` | 19 i, avance 17 | Commune aux trois sauts : depuis la pose basse d'amorti, le bassin remonte au-dessus des pieds et le buste se redresse jusqu'au repos, puis `idle_repos` |
| `saut_booste_neutre` | 95 i, recule 10 | Maj + ↑ : anticipation plus profonde et plus longue (le bassin descend à 53 au lieu de 67, les bras partent loin derrière), contraction des jambes puis extension explosive. Le bassin monte 35 plus haut qu'au saut normal. Retombée sur la pointe du pied avant, le second pied, puis la main avant se pose : appui sur trois points, onde de choc au sol et secousse, puis `reception_lourde` |
| `saut_booste_avant` | 92 i, avance 140 | Maj + ↑ + → : même charge, poussée inclinée vers l'avant, genoux groupés haut ; le pied avant touche le premier et freine |
| `saut_booste_arriere` | 92 i, recule 134 | Maj + ↑ + ← : poussée en arrière, bras qui équilibrent vers l'avant, le pied arrière touche le premier |
| `reception_lourde` | 38 i, avance 3 | Commune aux trois sauts boostés : depuis l'appui main au sol, la main pousse et se décolle, le bassin remonte et le buste se redresse jusqu'au repos, puis `idle_repos` |
| `propulsion_avant` | 60 i, avance 232 | Accroupi (↓ tenu) puis → : le poids passe sur la main, les jambes se contractent, puis poussée explosive à ras du sol, buste penché à 45°. Pointe du pied, second pied, main posée, amorti jusqu'à la pose accroupie, puis `accroupi_repos_idle` |
| `propulsion_avant_haute` | 75 i, avance 225 | ↑ + → depuis l'accroupi : même charge, poussée plus verticale, vol en cloche (le bassin monte à 105), genoux groupés |
| `propulsion_arriere` | 59 i, recule 150 | ← depuis l'accroupi : le poids recule sur le pied avant, la main se lève, poussée en arrière à ras du sol, le pied arrière se pose le premier |
| `propulsion_arriere_haute` | 73 i, recule 157 | ↑ + ← depuis l'accroupi : même chose en cloche |
| `demi_tour` | 22 i, recule 13 | T en garde : pivot sur place, de la garde ouverte à la même garde tournée de l'autre côté. Petite anticipation à contre-sens, le haut du corps devance le bassin (la tête encore plus), passage de face mains rentrées devant le visage, léger dépassement puis retour ; les chevilles restent sur place, le talon de l'ancienne jambe arrière se pose et celui de l'autre se lève. Puis `garde_ouverte_idle`, retourné |

Une clé part d'une pose (`poses/`), applique des réglages (`plus`, `fixe`,
`vise` pour placer une main ou un pied en cinématique inverse), et choisit la
courbe du segment qui suit (`auto`, `lin`, `acc`, `dec`, `acc-dec`,
`palier`). Les pieds qui ne bougent pas entre deux clés restent plantés, et
le `decalage` retarde la tête et les avant-bras de quelques images
(chevauchement).

Les **pieds** se calculent tout seuls à partir des jambes (`_bake_feet`
dans `scripts/stick_anim.gd`) ; les clés n'ont pas à les régler. Pour chaque
image, selon la hauteur et la vitesse de la cheville :

- au sol et immobile : pied **à plat** ;
- au sol en glissade vers l'avant : pointe relevée (16°), le talon glisse ;
- cheville un peu levée, presque à la verticale de la pointe : appui **sur la
  pointe** (poussée, pied qui traîne) ;
- en l'air : la pointe s'abaisse au décollage puis remonte avant la pose, et
  la pose suivante commence par **le talon** (+14° qui retombe à plat en
  4 images) ; la cheville ne tourne pas plus de 11° par image.

Ensuite, dans toutes les poses (animations, fondus, atelier) : un pied ne
passe jamais sous le sol, et si poser un pied à plat demandait de plier la
cheville au-delà de 30°, **le talon se lève** (le pied pivote sur sa
pointe et la jambe suit). C'est ce qui lève le talon arrière en garde.

Le **sens** se règle par clé : `"facing": -1` retourne le personnage à
partir de cette clé (il se transmet aux suivantes), `"miroir": true` reprend
la clé précédente vue de l'autre côté. Entre deux clés de sens différents,
la pose passe par le miroir (proche et loin échangés) ; le sens affiché est
celui de la clé qui commence le segment. Une animation qui finit retournée
retourne le combattant. `"pieds_auto": false` en tête d'animation coupe le
calcul automatique des pieds : leurs angles viennent alors des clés.

`demi_tour` est généré par `tools/gen_demi_tour.gd` (une clé par image) : la
garde est remontée en 3D (profondeur de chaque articulation), tournée autour
de l'axe vertical, projetée, puis relue en angles 2D avec étirement des os
raccourcis ; les genoux sont recalculés en 3D. `esquive_cote` suit le même
principe (`tools/gen_esquive_cote.gd`) : quart de tour autour de la plante du
pied avant, avec une perspective calculée articulation par articulation ;
la pointe du pied avant est recalée après projection pour qu'il ne glisse pas.
Les autres esquives sont écrites par un script Python hors dépôt : chaque clé
compense l'inclinaison du tronc sur les bras (ils pendent) et sur le cou (le
regard reste à l'horizontale).

```sh
$GODOT --headless --path . -s res://tools/gen_demi_tour.gd
$GODOT --headless --path . -s res://tools/gen_esquive_cote.gd
```

Les esquives n'ont pas de garde, ni pendant ni après : elles partent du repos
(`repos`) et finissent dans `idle_repos`. Le style est celui d'un combattant
détendu, façon « ultra instinct » : le corps bouge le moins possible et le
plus tard possible, les bras pendent, la tête reste droite et le regard fixe
l'adversaire.

**Profondeur.** Une clé peut donner `z` (dans `fixe` ou `plus`) : la
profondeur du combattant, négative vers la caméra. `StickRig.depth` en tire
une échelle (300 / (300 + z)) et un léger décalage vers le bas (z × 0,3) :
un combattant à z −40 paraît plus grand et plus bas, donc plus près. Le
combat dessine d'abord le combattant le plus loin. Le slip s'en sert ;
`esquive_cote` porte une petite profondeur positive pour passer derrière
l'attaquant, ses points étant pré-compensés pour ne pas être déformés. Le miroir et
les fondus conservent z.

Une boucle qui fait avancer le personnage déclare son `avance` (en unités
par cycle) : chaque cycle reprend décalé d'autant, et le combattant
(`scripts/fighter.gd`) reporte ce déplacement dans sa position. Quand une
animation en remplace une autre, le bassin reste où il est arrivé.

Événements : `contact` (repère de synchronisation), `hitstop` (arrêt sur
impact global, la figure qui l'émet tremble), `etincelle`, `poussiere`,
`vitesse` (lignes de vitesse derrière le bassin), `onde` (onde de choc au
sol ; `"articulation": "pieds"` la centre entre les deux chevilles),
`choc` (onde d'air dans la direction `dir`), `secousse` (caméra),
`fenetre` (intervalle d'images nommé : `"nom": "contre"` marque, après une
parade ou une esquive, le moment où une contre-attaque peut annuler la fin
de l'animation ; `"nom": "esquive"` marque les images où le corps est hors
de la trajectoire du coup ; `Fighter.en_fenetre(nom)` le teste). L'étincelle a trois
genres : `garde` (coup bloqué, bleu), `coup` (touché, orange), `parade`
(coup dévié, vert d'eau) et `armure` (coup encaissé sous armure, rouge).
`eclat` (`"n"` images, `"couleur"`) entoure tout le corps d'un liseré
coloré qui s'amincit jusqu'à disparaître, sans compter les images d'arrêt
sur impact.

Une animation marquée `"couche": true` se joue **par-dessus** l'animation
courante (`Fighter.couche(nom)`, `Combat.couche(f, nom)`) : pour chaque
angle, on ajoute l'écart entre l'image de la couche et sa dernière image
(la couche peut donc commencer déjà déformée et doit finir sur sa pose de
base). Les cuisses, tibias et pieds ne sont pas ajoutés : un pied posé au
sol reste à sa place, la jambe se replie pour le suivre.

Les effets (`scripts/vfx.gd`) suivent la méthode pixel art du dépôt
(`methode-pixel-art/`) : aplats sans tramage, rampes à décalage de teinte
(lumière chaude, ombre froide, trait plus sombre), lumière en haut à gauche,
flash d'une seule image à l'impact, chaque dessin tenu plus longtemps à
mesure que l'effet ralentit, disparition par trous et jamais en fondu.

- **Poussière** (32 i) : cinq bouffées de quatre boules ombrées (trait,
  ombre, corps, reflet) qui jaillissent, gonflent, montent, puis passent du
  blanc chaud au gris froid et se défont boule par boule.
- **Onde** (30 i) : flash plat au sol, dôme d'air qui se brise, front en
  bande épaisse (bord blanc, bande bleutée derrière) qui s'élargit en
  ralentissant, second anneau plus lent, mur de poussière soulevé sur le
  front, cailloux en parabole et, pour les gros impacts, fissures. La moitié
  du fond de l'anneau passe derrière les jambes, en plus mince.
- **Choc** (22 i) : flash en disque et étoile perpendiculaire au vol, cône
  d'air, puis trois anneaux en perspective laissés sur place le long de la
  trajectoire, qui se brisent par trous.

Un **duo** (`anims/duo_*.json`) place plusieurs combattants et leur programme :
`{"contact": 33, "anim": "blocage_bas", "fondu": 3}` démarre l'animation pour
que son événement `contact` tombe à l'image 33, `{"g": 60, "couche":
"armure_encaisse"}` pose une couche à l'image 60.

### Démo

`scenes/demo.tscn` (ouvrir la scène puis F6) joue les animations en direct :

Le repos est l'état par défaut ; la garde ne dure que tant que G est tenu.

| Touche | Effet |
|---|---|
| → ou ← maintenu | Depuis le repos : marche détendue avant ou arrière ; relâché, le pas en cours se termine et le combattant s'arrête au repos. La caméra suit |
| Maj + → maintenus | Depuis le repos : départ de course puis course ; relâchés, le combattant freine au prochain appui et revient au repos |
| Ctrl + → maintenus | Depuis le repos : départ de sprint puis sprint ; relâchés, freinage en glissade au prochain appui et retour au repos. La caméra regarde devant en proportion de la vitesse |
| ↓ maintenu | Depuis le repos : accroupi détendu, une main posée au sol ; relâché, le combattant se relève au repos |
| ↑ | Depuis le repos : saut sur place ; ↑ + → saut avant, ↑ + ← saut arrière (↑ reste accepté dans les 6 premières images d'un départ de marche). Réception, puis retour au repos |
| Maj + ↑ | Saut boosté sur place ; avec → ou ←, saut boosté avant ou arrière (accepté aussi au début d'un départ de marche ou de course). Atterrissage sur trois appuis, réception lourde, puis repos |
| ↓ tenu, puis → ou ← | Propulsion rasante avant ou arrière depuis l'accroupi ; avec ↑ en plus, propulsion haute. Le combattant revient accroupi |
| G maintenu | Mise en garde (garde ouverte) ; avec →, marche en garde ; ← ferme la garde (défensive) puis recule, et la garde se rouvre après 10 images sans ← ; → → ou ← ← (double appui rapide) : dash avant ou arrière ; ↓ maintenu : accroupi en garde ; ↓ + ← : garde basse (accroupi, garde fermée), et ← ferme aussi la garde quand on est déjà accroupi ; elle se rouvre après 10 images sans ←, et se relève en garde fermée quand ↓ est relâché ; G relâché, sortie de garde et retour au repos |
| T | Demi-tour (en garde) : le combattant se retrouve tourné de l'autre côté. Les flèches restent celles de l'écran : retourné, → recule et ← avance |
| B | Blocage bas (en garde) |
| H, Maj + H, Ctrl + H | Encaisser un coup bloqué léger, moyen ou lourd (en garde : recul sur garde debout, ou accroupi en garde basse). Un recul peut en interrompre un autre |
| Ctrl + Maj + H | Très gros coup bloqué en garde : garde repoussée, les pieds glissent loin (en garde basse : recul lourd) |
| J | Coup qui brise la garde : garde brisée, bras ouverts et vulnérable (en garde basse : recul lourd) |
| P, Maj + P, Ctrl + P, Ctrl + Maj + P | Parade en garde : coup de poing haut, coup de pied haut, coup moyen, coup bas. Pendant la fenêtre de contre d'une parade, une nouvelle parade peut l'annuler (à la place de la contre-attaque, qui sera propre à chaque personnage) |
| 1 à 6 | Esquive détendue (au repos, en marche ou en garde), une par type de coup : 1 sway (direct au visage), 2 slip (direct), 3 se baisser (crochet ou circulaire à la tête), 4 pas de côté, pivot face caméra (coup de pied appuyé), 5 saut arrière (coup de pied hache), 6 saut sur place (balayage). Sans garde, bras pendants, elle finit toujours au repos. Elle peut aussi partir pendant la fenêtre de contre d'une parade ou d'une autre esquive. Touches provisoires, comme P |
| U | Armure : encaisse un coup sans broncher, par-dessus ce qu'il fait (repos, marche, garde, course…) |
| K, Maj + K, Ctrl + K, Alt + K, Alt + Maj + K | Duo coup de pied / blocage, coup de pied encaissé sous armure, projection cassée, direct paré en haut, pied paré au milieu (en boucle) |
| Y, Maj + Y, Ctrl + Y | Duo direct pris au visage : B en garde, au repos, coup lourd (en boucle) |
| O, Maj + O | Duo coup de pied direct pris au ventre, B en garde : léger / plié en deux (en boucle) |
| I, Maj + I | Duo touché : coup de pied bas pris dans le tibia, B en garde / pied direct pris accroupi (en boucle) |
| N | Duo sonné : B prend un direct lourd, titube sonné pendant deux boucles, puis se remet en garde (en boucle) |
| C, Maj + C, Ctrl + C, Ctrl + Maj + C | Duo chute : B prend un coup de pied au ventre, est propulsé et retombe sur le dos / B est fauché par un coup de pied bas, les jambes partent et il tombe à plat ; puis il reste au sol (en boucle) / B prend le coup de pied au ventre, recule en titubant, tombe à genoux puis face contre terre et reste à plat ventre / A s'approche et écrase du talon le ventre de B, couché sur le dos |
| Alt + C | Duo relevé : B tombe sur le dos après un coup de pied au ventre, reste au sol, puis se relève et se remet en garde |
| Alt + Maj + C | Duo relevé en roulade : même chute, puis B roule en arrière par-dessus ses épaules et se remet en garde plus loin |
| R | Repos (remise à zéro) |
| Espace | Pause ; en pause, ← → reculent ou avancent d'une image |
| L | Ralenti ×4 |
| D | Squelette coloré |

### Régler une animation en ligne de commande

`tools/anim.sh` simule l'animation (ou le duo) avec le code du jeu et la
rend en images :

```sh
tools/anim.sh anims/blocage_bas.json -o /tmp/planche.png --de 0 --a 24
tools/anim.sh anims/blocage_bas.json --strobe /tmp/strobe.png --suivre handN,handF,head
tools/anim.sh anims/duo_blocage.json -o /tmp/duo.png --pas 2 --cols 7
tools/anim.sh anims/garde_idle.json --print          # articulations image par image
tools/anim.sh anims/duo_blocage.json --gif /tmp/duo.gif --video /tmp/duo.mp4
tools/anim.sh anims/duo_blocage.json --gif /tmp/lent.gif --lent 3
tools/anim.sh anims/marche_avant.json --strobe /tmp/marche.png --boucles 2
```

La planche contact montre chaque image numérotée ; la stroboscopie superpose
toutes les images avec la trajectoire des articulations suivies (un point
par image : des points serrés = lent, espacés = rapide), ce qui permet de
vérifier les arcs et l'espacement. `--print` sert à vérifier au dixième près
qu'un pied ne glisse pas ou qu'une main touche bien le pied adverse.

## Fichiers

```
project.godot
scenes/atelier.tscn       scène principale
scenes/demo.tscn          démo des animations
scripts/stick_rig.gd      squelette : FK, IK, amplitudes, dessin, JSON
scripts/planche.gd        fond, grille, sol, figures (partagé atelier / rendu)
scripts/atelier.gd        état, historique, panneau de réglages
scripts/atelier_scene.gd  poignées, souris, clavier
scripts/stick_anim.gd     animation par clés : courbes, pieds plantés, décalages
scripts/fighter.gd        un combattant : animation, fondus, traînées
scripts/combat.gd         plusieurs combattants, arrêt sur impact, effets, duo
scripts/vfx.gd            effets en pixel art : étincelle, poussière, onde, choc
scripts/demo.gd           scène de démo
tools/rendu.gd, rendu.sh  rendu PNG d'une pose
tools/anim.gd, anim.sh    planche, stroboscopie, GIF, vidéo d'une animation
tools/gen_demi_tour.gd    génère anims/demi_tour.json (rotation 3D projetée)
tools/gen_esquive_cote.gd génère anims/esquive_cote.json (pivot face caméra)
poses/                    neutre, neutre-fin, repos, garde (fermée), garde_ouverte, au_sol, au_sol_ventre
anims/                    animations et duos
```

## Suite prévue

1. Timeline dans l'atelier : pelure d'oignon, déplacement des clés, réglage
   des courbes sans passer par le JSON.
2. Coups de poing (jab, direct) et coup de pied bas, avec boîtes de coup et
   de vulnérabilité attachées aux os.
3. Contrôle au clavier ou à la manette : déplacements, garde, blocage selon
   la hauteur du coup reçu.
4. Réactions aux coups reçus et enchaînements.
