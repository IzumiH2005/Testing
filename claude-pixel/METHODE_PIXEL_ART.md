# Méthode de pixel art — objets, personnages, créatures et décors (v23)

On construit d'abord, on détaille ensuite. Cette méthode réunit le dessin classique
(construction par volumes, ligne d'action, anatomie) et les règles du pixel art
(silhouette, valeurs, clusters, lignes propres, rampes, lumière). Depuis la v17, elle
commence par **la partie 0 : dessiner avant de pixelliser** (construction, lumière et
forme, design des valeurs et des formes, couleur, matières). Le pixel art n'est qu'un
style de rendu : un dessin mal construit ou mal éclairé reste amateur, même en pixels
propres.

**Comment l'utiliser :**
0. Avant tout : la **partie 0** (dessiner avant de pixelliser). Elle dit ce que les pixels
   doivent montrer ; les parties suivantes disent comment.
1. Relire les **règles impératives** avant chaque dessin.
2. Construire avec la **partie B** (objet), la **partie C** (personnage, créature) ou la
   **partie F** (tuiles, fonds, scène).
3. Poser les pixels avec le **pipeline A5**, puis finir avec **A6** (finition pro) ; tramage
   en **A7**, lignes en **A8**, vue du jeu en **A9**, leçons des maîtres en **A10**, geste
   du pro en **A11**.
4. Contrôler avec la planche (A5-11, `planche.py`, partie D) et, pour un décor, F6.
5. Pour progresser hors des projets : **partie G** (plan en quatre paliers, copies d'étude).

**Sommaire :**

| Partie | Sections |
|---|---|
| Règles impératives | 87 ordres courts, tirés des tests, des livres et des maîtres |
| **0. Dessiner avant de pixelliser** | 0-A diagnostic de la potion 64 · 0-B voir et construire · 0-C lumière et forme (zones) · 0-D design des valeurs · 0-E design des formes · 0-F perspective · 0-G couleur · 0-H bords · 0-I matières · 0-J méthode du pro · **0-K les neuf planches analysées** · 0-L recettes (potion en verre, sphère, fruit, pain, flamme, ruines, gemme) · 0-M plan d'entraînement · **0-N vision et conception (carnet, essais)** · **0-O astuces de pro** · **0-P inventer (SCAMPER, tableau morphologique)** · 0-Q geste · 0-R harmonies de couleur · 0-S métal et textures · **0-T perspective avancée et raccourcis** · **0-U anatomie animale** · **0-V mains, expressions, jeu d'acteur** · **0-W éclairages complexes** · **0-X effets naturels** · **0-Y stylisation** · **0-Z raconter en une image** · **0-AA dessiner une forme belle (design d'objet, grille de critique)** · **0-AB le sketching d'un illustrateur (rough, construction, esquisse, trait, polish, validation)** · **0-AC le sketch fini de pro (silhouette, trois poids de trait, recouvrements, lignes de forme)** |
| **A. Règles communes** | A1 travail · A2 lisibilité · A3 table par taille · A4 règles du dessin · A4b simplifier · A5 pipeline pixel (silhouette → contour → palette → lumière → matières → détails → nettoyage → contrôle) · A6 finition pro · **A7 tramage** · **A8 lignes et formes** · **A9 perspectives de jeu** · **A10 leçons des maîtres** · **A11 geste du pro (outils, souris)** |
| **B. Objets** | B0 intention · B0b projection · B1 cadre · B2 volumes · B3 forme iconique · B4 matière · B4b déclinaison par taille · B5 contrôle · **B6 recettes pas à pas (pierre, rocher, cristal, slime, livre)** |
| **C. Personnages** | C0 intention · C1 proportions · C2 pose · C3 volumes · C4 tête et visage · C5 vêtements (design) · C6 cheveux · C7 astuces de figure · C8 contrôle · C9 anatomie · C10 tailles (8 à 128 px) · C11 portrait anime · C12 visage Loomis + anime · C13 chibi pas à pas · C14 corps nu puis vêtements en calque · C15 créatures · C16 créatures complexes · C17 vêtements (plis, matières) |
| **E. Animation** | E0 méthode imposée image par image · E1 les 12 principes de *The Illusion of Life* · E2 techniques pixel (durées, espacement, smear, sous-pixel, pop, éclats, boucle) · E3 feuille de timing · E4 fichiers · E5 contrôles |
| **D. Outils** | `trace.py` · `px.py` · `contour.py` · `planche.py` · dossiers de tests |
| **F. Décors** | F0 intention · F1 hiérarchie de lecture · F2 tuiles (sans couture, variantes, autotiles blob 47 / Wang 16, plateformes, vue de dessus) · F3 fonds et parallaxe · F4 palette d'un lieu · F5 composition · F6 contrôle |
| **G. Progresser** | G0 principes · G1 plan en quatre paliers · G2 copies d'étude · G3 retours · G4 devenir pro |
| Fin | Résumé par type de dessin · **livres de référence** · sources web · historique des versions |

**Où trouver quoi (sujets répartis) :**

| Sujet | Sections |
|---|---|
| Yeux | C4 (œil en grand) · C10-D (1×1 à 3×3) · C10-J2 (32 px, portrait) · C11-A · C12-G · C13-C (chibi) |
| Couleur du contour | A5-6 · A6-C · C10-F · C11 (peau = trait chaud) · C13-D (selout) |
| Langage de formes | A4b (règle) · C5 (vêtements) · C15-A (créatures) |
| Cheveux, frange, sourcils | C6 · C10-J2 · C12-F · C13-D |
| Liquide, verre | **0-I** · **0-L-A** · A5-8b · B5 · C13-D |
| Lumière : terminateur, ombre propre, rebond, ombre portée | **0-C** (onglet Lumière, guide de volume) · A5-8 · A6-E |
| Deux familles, notan, étendue des valeurs | **0-D** · A6-J · A11-C |
| Construction, dessiner à travers, ellipses | **0-B** · **0-F** · B2 · C3 |
| Design des formes (grand-moyen-petit, droites et courbes) | **0-E** · A4b |
| Matières (mat, brillant, métal, verre, translucide, émissif) | **0-I** · A5-8b |
| Vêtements | C5 (design) · C13-B · C14 (calque sur corps nu) · C17 (plis, matières, recettes) |
| Rendu pro (rampes, AA, défauts) | A5-7 à A5-10 · **A6** |
| Jointures du corps | C2 · C3 · C14-A |
| Tramage (dithering) | A6-H (défaut) · **A7** · C17-F (fourrure) · F3 |
| Pentes, courbes, sous-pixel | A5-6 · A6-D · **A8** · E2-D |
| Anticrénelage (AA) | A5-10 · **A6-F** |
| Vue du jeu (profil, 3/4, iso) | B0b (objet) · C10-G · **A9** |
| Tuiles, fonds, parallaxe | **F2** · **F3** |
| Palette, harmonie | A5-7 · A6-A · A6-B · **F4** |
| Composition, point focal | A2 · A6-E · **F1** · **F5** |
| Apprendre, s'entraîner | **G** · livres de référence |
| Pierre, rochers, fissures, trous | A5-8 (creux inversés) · A5-8b · **B6-B** · **B6-C** |
| Cristal, halo, étincelles | A5-8b · C15-D · **B6-D** |
| Gélatine, slime | A5-8b (liquide) · **B6-E** |
| Ordre des étapes d'un objet | A6-I · **B6-A** |
| Méthodes des grands artistes | **A10** · G2 |
| Outils, souris, gestes | **A11** |
| Tests en cours de dessin (miroir, gris, yeux plissés) | A6-J · **A11-C** |
| Valeur d'abord, ombrer en gris | **0-D** · A6-A · **A10-F** |
| Apprendre le dessin, exercices | **0-M** · G |
| Vision, carnet, vignettes, créer une forme unique | **0-N** · 0-O · **0-P** |
| Geste, ligne d'action, courbes C et S | **0-Q** · C2 |
| Harmonies de couleur, accent | **0-R** · F4 · A6-A |
| Métal, bois, tissu, fourrure, feuillage | **0-S** · 0-I · C17 |
| Perspective à 1, 2, 3 points, raccourcis | **0-T** · 0-F · A9 |
| Quadrupèdes, oiseaux, insectes, pattes | **0-U** · C15 · C16 |
| Mains | **0-V-A** · C10-I |
| Expressions, jeu d'acteur | **0-V-B/C** · C10-E · C2 |
| Plusieurs lumières, nuit, lumière colorée | **0-W** · 0-C |
| Fumée, eau, explosion, étincelles | **0-X** · E7 · B6-D |
| Style d'un jeu, stylisation | **0-Y** · A10 |
| Récit, point d'intérêt, lignes directrices | **0-Z** · F5 · 0-O |
| Design d'une forme belle, proportions, jonctions, bouchon | **0-AA** · 0-E · 0-N |
| Sketching : rough, esquisse, trait, polish, calques, retourner la toile | **0-AB** · A11 |
| Sketch fini, poids du trait, lignes de forme, taille du dessin | **0-AC** · 0-H · A6-C |
| Grandes formes, langage des formes, point d'intérêt, contraste | **0-O** · 0-E · A2 |

**Sources (étiquettes) :** [Z] *Apprendre à tout dessiner avec Zephy* · [M] livre de dessin
manga · [I] planches d'anatomie fournies · [C] planches sur les cheveux fournies · [P]
planches fournies (cheveux, œil, arche, cristal, flamme, déclinaisons, projections) · [R]
recherches web (liens en fin de document) · [L] méthode Loomis et tutoriels de visage anime
· [A] analyse de portraits anime en pixel art fournis en exemple · [T1]…[T16] leçons de nos
propres tests (partie D) · [B] livres de pixel art et de peinture ([B1] *Pixel Logic*, [B2]
*Pixel Art for Game Developers*, [B3] *Make Your Own Pixel Art*, [B4] livres d'images,
[B5] *Color and Light*, [B6] livres japonais et livres d'artistes ; détail en fin de
document) · [P2] planches de tutoriels pas à pas
fournies (pierre, cristal, slime, livre, rochers ; B6) · [P3] neuf planches de tutoriels
fournies en v17 (potion, cristal, poire, sphère, livre, pain, portail, pierre, flamme ;
0-K) · [P4] planches fournies en v18 (slime, gemmes ; 0-K, 0-L-G) · [D] fondamentaux du dessin et de la peinture ([D1] Drawabox, [D2] Scott Robertson,
[D3] Proko, lumière et ombre, [D4] James Gurney, blog, [D5] Marco Bucci, [D6] Proko, groupes
de valeurs, [D7] Sinix, design des formes, [D8] droites et courbes, [D9] couleur, [D10]
bords, [D11]-[D15] vision, vignettes, conception et astuces de pro, [D16]-[D20]
créativité, geste, couleur, métal et textures, [D21]-[D28] perspective, anatomie animale,
mains, expressions, éclairages, effets, style, récit, [D29]-[D30] appeal et verre d'art ;
[T17] séance `fiole-unique`, [D31]-[D32] sketching d'illustrateur, [D33]-[D34] line art
fini, [T18] séance `fiole-bourgeon` ; liens en fin de document). Toutes les règles sont reformulées.

---

# Règles impératives (à relire avant chaque dessin)

Chaque règle est un ordre. Le détail et le « pourquoi » sont dans la section citée.

**Travail**
1. **Une étape = un fichier `.txt` + son `.png`, regardés à ×1 et agrandis** avant de
   continuer. Ce qui ne se lit pas à ×1 n'existe pas (R1).
2. **Décide chaque pixel toi-même.** Écris la grille à la main (1 caractère = 1 pixel) ou
   pose des primitives que tu as décidées. Un script ne calcule jamais une forme, une ombre
   ou un dégradé (R3, partie D).
3. **Garde chaque étape dans un fichier de commandes** (`cXX.txt`). Pour corriger, modifie
   les commandes et relance : ne retouche jamais l'image sans trace.
4. **Corrige à l'étape fautive.** Un détail ne rattrape pas une construction fausse (R2).
5. **Si l'utilisateur rejette une modification, reviens à la version d'avant** au lieu
   d'empiler des corrections.

**Ordre du personnage**
6. **Construis en calques de couleur** (rouge pose, bleu repères, vert volumes) avant tout
   pixel final (R4, C13-A).
7. **Dessine d'abord le corps nu**, mannequin lisse et sans détail sexuel, avec toutes ses
   jointures (C14-A). **Valide-le** en silhouette, ombres et ×1 avant le moindre vêtement.
8. **Habille ensuite, en calque** : le corps validé ne se retouche plus. Tu travailles
   seulement le tissu (C14-B).
9. **Puis le visage, puis les cheveux** (en calque aussi), puis les accessoires, le
   nettoyage et la planche (C13-B).

**Corps**
10. **Marque chaque jointure** : creux d'aisselle, pli du coude, poignet resserré, V de
    l'aine, rotule claire et ombre dessous, cheville resserrée.
    **Chibi : jamais d'épaule marquée** (toujours sous 64 px, et au-delà dès que la tête est
    grosse). Pas de bosse de deltoïde : le trait descend du cou en une pente régulière
    (1 px par rangée) jusqu'au bord du bras, qui pend collé au torse, séparé par un seul
    trait (C13-A). Seul un grand sprite aux proportions réalistes a un deltoïde (C14-A).
11. **Donne un geste** : bras levé avec un coude, jambes en contrapposto. Jamais de membres
    en colonnes raides.
12. **Remplis une rangée de plus sous les pieds** avant de poser le contour : sinon le
    contour mange la semelle.
13. **Fais la tête ronde ou en ovale de visage, jamais en œuf ni en V.** À peine plus haute
    que large, bords arrondis sur tout le tour ; le bas peut être un peu aplati (menton
    large et court, fermé en 2 ou 3 marches). Marches courtes vers le menton (0, 1, 1, 2,
    3 px), jamais un long biseau. **Ombre de la tête étroite** : 2 à 3 px côté ombre.

**Vêtements (C14)**
14. **Peins le tissu 1 px au-delà du bord du corps** : le tissu a une épaisseur.
15. **Contourne le calque seul** (`contour.py … CALQUE CONTRE`) : seul le bord du vêtement
    contre le vide ou la peau devient trait.
16. **Trace à la main les bords intérieurs** : séparation manche/torse, sangle, cadre de la
    sacoche. Le contour automatique ne les voit pas.
17. **Nettoie à la main chaque ourlet contre la peau** (`hline O`) : le contour y laisse des
    pixels clairs isolés.
18. **Le bord haut de l'écharpe (ou du col) sert de trait du menton.** Jamais deux traits
    collés.
19. **Mets les plis aux articulations** (coude, aisselle, aine, genou) et une **ligne de
    tension** depuis l'aisselle du bras levé vers la hanche opposée.
20. **Ombre le tissu en masses** : clair du côté de la lumière, sombre sous les manches, sous
    l'écharpe et en ourlet. Pas de pixels isolés.

**Lignes et pixels**
21. **Diagonales propres** : marches régulières (1-1, 2-2, 1-2-1…), aucun pixel doublé en
    « L » (A5-6).
22. **Aucun pixel de bruit** : un pixel seul d'une couleur n'a le droit d'exister que s'il
    dit quelque chose (reflet, coin, bouton).
23. **Une seule direction de lumière pour tout le jeu** (haut gauche par défaut) : reflets
    des yeux, des cheveux et du tissu du même côté.
24. **Pas de détail qui suit le contour sur 1 px** au contact de la peau : une mèche, une
    pointe de frange ou un ourlet d'une seule rangée devient tout noir. Fais-les au moins
    2 rangées de haut (3 px de large pour une pointe, C6-C).

**Contrôle**
25. **Finis par la planche** (`planche.py`) : ×1, ×2, gris, silhouette, fonds clair et sombre,
    miroir. Note au moins un défaut, corrige, revérifie (R5).

**Animation** (partie E)
26. **Découpe le mouvement en un nombre d'images fixé avant de dessiner**, dans une feuille
    de timing : rôle de chaque image (clé, passage, intervalle, tenue) et sa durée en ms (E0).
27. **Chaque image passe par TOUT le pipeline** (silhouette → contour → aplats → lumière →
    détails → contrôle) **et est validée avant la suivante.** Aucune étape sautée (E0-5).
28. **Applique les 12 principes** (E1) : anticipation avant, ralenti aux clés, dépassement
    et retour, chevauchement des pièces souples, volume constant, une action à la fois.
29. **Le ralenti se fait d'abord par la durée des images**, pas par plus de dessins ; les
    clés et l'impact tiennent 3 à 4 fois plus longtemps (E2-A).
30. **Contrôle la séquence** : bande, pelure d'oignon, GIF aux vraies durées. Note un défaut,
    corrige l'image fautive, refais la bande (E5).

**Tramage, lignes, vue (A7 à A9)**
31. **Ne trame que si les trois conditions sont réunies** : ton manquant, grande surface,
    matière qui l'accepte. Sinon, ajoute un ton ou fais une marche nette (A7-A).
32. **Trame seulement la limite, entre deux tons voisins**, en rampe 25 / 50 / 75 %. Le cœur
    de chaque ton reste plein (A7-B).
33. **Choisis la vue du jeu avant le premier sprite**, et une seule pour tout le monde du
    jeu. En isométrique, 2:1 partout (A9).

**Décors (partie F)**
34. **Le personnage et les dangers ont le plus fort contraste de l'écran.** Le décor reste en
    dessous ; le fond s'éclaircit, se désature et perd du contraste en s'éloignant (F1, F3).
35. **Teste chaque tuile en grille 3×3 et la carte dézoomée** : aucune couture, aucune
    grille visible. Pas de gros sujet unique au centre d'une tuile (F2-A, F6).
36. **Casse la répétition** par 1 à 3 variantes, des décors posés à la main et des
    éléments qui chevauchent la grille (F2-B).
37. **Agrandis seulement par un entier et garde une seule taille de pixel** dans toute la
    scène : pas de mixels (F3-C).

**Progresser (partie G)**
38. **Entre deux projets, fais une copie d'étude** : analyse, copie, refais de mémoire,
    réutilise une technique (G2).

**Recettes pas à pas (B6)**
39. **Garde le contour sombre et neutre jusqu'à ce que la lumière soit posée**, puis colore-le ;
    la teinte (glissement vers le froid) vient après les valeurs (B6-A).
40. **Sur une pierre ou un bloc ombré, efface le trait des arêtes intérieures** : les faces
    se séparent par la valeur, seul le contour extérieur reste (B6-C).
41. **Une fissure ou une gravure = trait sombre + lèvre claire d'1 px**, attachée à une
    arête, en « Y », et qui passe d'une face à l'autre (B6-C).
42. **Primitive d'abord, déformation ensuite** : cube ou prisme propre et ombré en 3 tons,
    puis coins cassés et sous-plans ; un rocher composé = 2-3 blocs de tailles différentes
    (B6-B).

**Leçons des maîtres et geste du pro (A10, A11)**
43. **La valeur avant la teinte** : valide les aplats et l'ombre en gris avant de toucher aux
    teintes. Une teinte ne corrige jamais une valeur fausse (A10-F, A6-A).
44. **Peu d'idées fortes** : sous 32 px, 2 ou 3 traits d'identité (coiffure, couleur
    dominante, accessoire). Tout autre détail doit prouver qu'il se lit à ×1 (A10-A).
45. **Regarde autrement à chaque étape, pas seulement à la fin** : miroir après la
    silhouette et après la lumière, gris après les aplats, yeux plissés avant la finition
    (A11-C).
46. **AA seulement sur une marche de 2 px ou plus**, un pixel par coin, à l'intérieur du
    contour, et chaque pixel d'AA survit au test de l'enlèvement (A6-F).
47. **Un trait = un geste décidé** : départ, arrivée et marches connus avant de tracer ;
    droites à l'outil ligne, courbes en segments prévus. Un trait raté s'annule et se
    refait (A11-A, A11-B).
48. **Petit mouvement = couleurs qui changent, pas silhouette qui bouge** : respiration,
    clignement et transfert de poids se font en sous-pixel (E2-D).

**Dessin, lumière et matière (partie 0)**
49. **Construis avant de dessiner** : chaque volume entier dans un calque de construction,
    partie cachée comprise ; les ellipses s'ouvrent en s'éloignant du niveau de l'œil
    (0-B, 0-F).
50. **Pose la lumière avant la première ombre** (onglet Lumière) et garde le guide à l'œil :
    le terminateur suit la forme, l'ombre est à l'opposé de la source (0-C).
51. **Deux familles d'abord** : dans chaque matière, une valeur de lumière et une valeur
    d'ombre, rien d'autre, tant que la vue Notan ne montre pas deux masses nettes (0-D).
52. **Le rebond reste dans l'ombre** : plus clair que l'ombre propre, toujours plus sombre
    que le demi-ton. Les points les plus sombres sont l'occlusion et le contact (0-C).
53. **Toute l'échelle des valeurs** : à 32 px et plus, de presque noir à presque blanc ; le
    plus fort contraste au point d'intérêt (0-D).
54. **La saturation culmine au demi-ton**, près du terminateur ; la lumière se désature vers
    la couleur de la source, l'ombre vire vers la couleur ambiante (0-G).
55. **L'éclat est le reflet de la source** : une forme qui épouse la courbure, du côté de la
    lumière, seulement sur une matière brillante (0-I).
56. **Le verre est transparent** : dessine ce qu'on voit au travers (contenu, paroi arrière),
    assombri et teinté ; ses reflets passent par-dessus le contenu ; un liquide s'éclaire
    du côté opposé à la lumière (0-I, 0-L-A).
57. **Une ombre portée ancre l'objet** : la plus sombre et la plus nette au contact, plus
    claire et plus large en s'éloignant, poussée à l'opposé de la lumière (0-C).
58. **Dessine des formes, pas des choses** : grand-moyen-petit, droites contre courbes,
    aucune tangente ni écart régulier ; les taches de lumière et d'ombre sont des formes
    choisies (0-E).
59. **Vise un niveau** : avant chaque dessin, choisis une œuvre pro et ce que tu en prends ;
    à la planche, compare côte à côte et écris l'écart (0-J).
60. **Le guide de volume aide, il ne dessine pas** : tu poses chaque pixel ; si tu t'écartes
    du guide (forme complexe, matière), écris pourquoi (0-C, règle 2).

**Vision et conception (0-N, 0-O)**
61. **Écris ta vision avant le premier trait**, une idée à la fois, dans le carnet : ce que
    tu vois, la structure, les formes de base, l'idée unique, ce qui la rend crédible (0-N).
62. **N'efface jamais une idée : barre-la et écris pourquoi.** Le carnet garde le chemin
    qui mène à la bonne forme (0-N-A).
63. **Essaie au moins trois silhouettes vraiment différentes**, petites, au calque de
    construction, avant de choisir ; écris le choix et ce qu'il reste à pousser (0-N-C).
64. **Pars de formes géométriques simples, puis transforme-les** : étirer, tordre, couper,
    combiner. La base géométrique est un repère, pas le résultat (0-N-B).
65. **Une forme inventée reste logique** : la forme suit la fonction, une créature tient
    sur un squelette plausible (0-N-B).
66. **Grandes formes calmes, détails groupés, un seul point d'intérêt** : la plus forte
    valeur, le bord le plus dur et la couleur la plus saturée s'y retrouvent (0-O).
67. **Cherche avant de choisir** : SCAMPER sur une forme connue, puis un tableau
    morphologique ; tire trois combinaisons très différentes pour les trois vignettes (0-P).
68. **Le geste en trois traits** : une ligne d'action, puis des C, des S et des droites ;
    un côté tendu face à un côté droit (0-Q).
69. **Une couleur domine, une soutient, une accentue** (environ 60 / 30 / 10) ; l'accent
    seulement au point d'intérêt (0-R).
70. **Une texture = quelques amas répétés, distribués irrégulièrement, dans le demi-ton** ;
    rien en pleine lumière ni dans l'ombre profonde (0-S).

**Perspective, anatomie, jeu, lumière, effets, style, récit (0-T à 0-Z)**
71. **Le recouvrement d'abord** : ce qui est devant cache ce qui est derrière ; dans un
    sprite, c'est l'indice de profondeur qui reste lisible. Pas de raccourci extrême sous
    32 px (0-T).
72. **Le pied fait l'animal** : plantigrade, digitigrade ou onguligrade ; le « genou à
    l'envers » est une cheville ; les pattes d'un insecte partent du thorax (0-U).
73. **L'aile est un bras, la main une moufle** : masses et groupes d'abord (plumes,
    doigts), détails au bord seulement à la fin (0-U, 0-V).
74. **Une émotion = sourcils, yeux, bouche, et tout le corps** ; une pose est un verbe ;
    on exagère pour une lecture immédiate (0-V).
75. **Plusieurs lumières : une principale, une de remplissage, des accents**, de
    températures opposées ; jamais deux de même force (0-W).
76. **Un effet en pixel art = paliers et amas, jamais de flou ni de semi-transparence** ;
    il reste plus simple que le sujet et ne cache pas le point d'intérêt (0-X).
77. **Un seul style par jeu, fixé dans une fiche de style** (contour, angles, ombrage,
    densité, palette, proportions) ; styliser, c'est simplifier et exagérer exprès (0-Y).
78. **Une image raconte une chose** : un point d'intérêt, l'instant clé, quelques indices ;
    le décor et l'usure racontent sans texte (0-Z).

**Design de la forme (0-AA)**
79. **La forme doit être belle en noir avant toute lumière** : le rendu sublime une forme, il
    ne la sauve pas (0-AA).
80. **Un langage dominant et un motif répété à trois échelles** : la panse, le bouchon et un
    détail se répondent (0-AA-B).
81. **Proportions franches, jamais 1:1 ; jonctions dessinées** (épaule, bague, lèvre, tige) :
    c'est aux jonctions que la forme devient belle (0-AA-B).
82. **Au moins 6 silhouettes dans 3 familles, notées avec la grille**, puis 3 variantes de
    chaque pièce (bouchon, jonction, pied) ; rien sous 20/30 ne passe (0-AA-D, 0-AA-E).

**Sketching (0-AB)**
83. **Sketcher calque par calque** : rough (geste, masses), construction, esquisse nettoyée,
    trait final, polish ; chaque passe sur un nouveau calque, celui du dessous baissé à 20-40 %
    (0-AB-A).
84. **Redessiner plutôt que gommer, retourner la toile souvent** ; on choisit les traits qui
    comptent et on ne décalque pas en aveugle (0-AB-B).
85. **Le dessin se juge à la fin du sketching, avant la couleur** : 22/30 au moins à la grille,
    et on s'arrête pour le montrer ; sinon on revient au rough ou à l'esquisse (0-AB-C).

**Sketch fini (0-AC)**
86. **Le trait seul doit ressembler à un sketch fini de pro** : l'idée se lit en silhouette
    noire, trois poids de trait appliqués partout, recouvrements nets, lignes de forme (0-AC).
87. **Dessiner un design d'objet à 64 px de haut au moins** ; une icône plus petite se
    redessine ensuite à sa taille depuis le sketch validé, jamais par réduction (0-AC-C).

---

# Partie 0 — Dessiner avant de pixelliser (v17) [D][P3][R]

Un pixel artist pro sait dessiner et peindre. Le pixel art n'est qu'un **style de rendu** :
la construction, la lumière, la matière et le design des valeurs viennent du dessin et de la
peinture. Les parties A à G apprennent le pixel. Cette partie apprend **ce que le pixel doit
montrer**. Elle se lit avant toutes les autres. Dans Claude Pixel, elle a ses outils :
calque de construction, **onglet Lumière** (direction, hauteur, guide de volume), vues
**Notan** et **Valeurs** sur la toile, détecteur « L'ombrage ne suit pas la lumière » et
porte « Le volume suit la lumière ».

## 0-A. Pourquoi nos dessins font débutant (diagnostic de la potion 64×64)

Comparée à l'étape 9 de la planche « Potion tutorial » [P3], la potion 64×64 de la séance
`potion-64` respecte les règles du pixel (aucun orphelin, rampes propres) mais rate le dessin :

| Ce qu'on a fait | Ce que fait la planche | Fondamental manqué |
|---|---|---|
| Panse bleu nuit opaque, liquide posé dessus | Verre bleu clair **transparent** : on voit le liquide à travers, et la paroi arrière | Matière (0-I) |
| Surface du liquide = une ligne horizontale | Surface = une **ellipse** en perspective, plus claire (son dessus reçoit la lumière) | Construction, perspective (0-B, 0-F) |
| Bande orange en haut, rouge partout, croissant sombre en bas | Lumière, demi-ton, terminateur courbe, ombre propre, rebond : la sphère **tourne** | Lumière et forme (0-C) |
| Valeurs serrées au milieu de l'échelle | De presque noir (contour) à blanc (éclat), deux familles nettes | Design des valeurs (0-D) |
| Éclat = barre verticale blanche | Éclat = **arc qui épouse la sphère** + 2 points, posé sur le verre | Spéculaire (0-I) |
| Rouge pur partout, même dans la lumière | Saturation au demi-ton, lumière rosée et claire, ombre vers le violet | Couleur (0-G) |
| Col long et étroit, bouchon en briques empilées | Col court et large, bouchon arrondi : un cylindre et une calotte | Proportions, primitives (0-B, 0-E) |
| Liseré cyan saturé sur un seul bord, sans raison | Contre-jour d'une autre teinte, sur tout le bord opposé à la lumière | Lumière secondaire (0-C) |
| Ni ombre portée ni contact | (Version finale : halo et étincelles, l'objet « existe ») | Ancrage (0-C) |

Conclusion : on posait des pixels propres sur un dessin qui n'était pas construit ni
éclairé. **Corriger le pixel ne corrige pas le dessin** (règle 4). D'où la v17 : construire,
éclairer, donner la matière, puis seulement pixelliser.

## 0-B. Voir et construire [D1][D2][L]

1. **Tout objet est un assemblage de primitives** : sphère, cylindre, boîte, cône, tore.
   Une potion = sphère (panse) + cylindre (col) + cylindre court ou calotte (bouchon). Une
   poire = petite sphère + grande sphère fondues. Un pain = cylindre couché aux bouts
   arrondis. Un portail = boîtes. Une flamme = une goutte qui ondule (geste en S).
2. **Dessiner à travers** (Drawabox) : chaque volume se dessine **entier**, sa face cachée
   comprise, dans le calque de construction. C'est ce qui donne la vraie ellipse du niveau
   du liquide, la paroi arrière d'un verre et l'emboîtement des pièces.
3. **Contours croisés** : des lignes qui courent **sur** la surface (équateur, méridiens,
   bandes) montrent comment elle tourne. En pixel art, ces lignes deviennent la surface du
   liquide, les bagues d'un col, les bandes d'ombre : une bande d'ombre est toujours **une
   courbe parallèle à un contour croisé**, jamais une ligne droite sur une forme ronde.
4. **Axe d'abord** : un objet symétrique se construit autour de son axe ; toutes ses
   ellipses ont leur petit axe **sur** cet axe.
5. **Mesurer au lieu de deviner** : compter en pixels sur la référence (« la panse fait
   3 cols de large, le bouchon 1 col de haut ») et reporter les rapports sur la toile.
6. **Recouvrement = profondeur** : ce qui est devant coupe le contour de ce qui est derrière
   (jonction en T). Une pièce devant a un contour complet, celle de derrière s'arrête
   contre elle.
7. **Le geste avant le détail** : une ligne d'action (C2) pour un personnage, un S pour une
   flamme, une courbe tendue pour un pain. Le contour suit le geste.

## 0-C. Lumière et forme : les zones de la lumière [D3][D4][B5]

Une seule source, placée **avant** la première ombre (onglet Lumière). Sur toute forme,
dans cet ordre de clarté :

| Zone | Ce que c'est | En pixels |
|---|---|---|
| **Éclat** (spéculaire) | Le reflet de la source elle-même, là où la surface renvoie la lumière vers l'œil | 1 à quelques px presque blancs, **une forme** qui épouse la courbure ; seulement sur une matière brillante |
| **Lumière** | Les plans tournés vers la source | Le ton clair de la rampe, en grande masse calme |
| **Demi-ton** | Les plans qui tournent, entre lumière et terminateur | Le ton moyen (la couleur locale), bande plus large sur une forme douce, fine sur une arête |
| **Terminateur** | La frontière lumière / ombre, là où la surface cesse de voir la source | Une **courbe** qui épouse la forme (arc d'ellipse sur une sphère), jamais une droite ni un cercle concentrique au bord |
| **Ombre propre** (cœur d'ombre) | La partie la plus sombre de l'ombre, juste après le terminateur, que le rebond n'atteint pas | Le ton sombre, bande le long du terminateur |
| **Lumière réfléchie** (rebond) | La lumière renvoyée par le sol ou les voisins dans l'ombre | Un ton **entre** l'ombre propre et le demi-ton, sur le bord d'ombre tourné vers le sol, teinté par la couleur du sol |
| **Occlusion** | Les creux et les contacts, où aucune lumière n'arrive | Les pixels les plus sombres de l'image (hors contour) |
| **Ombre portée** | La forme projetée sur le sol, à l'opposé de la source | Ellipse sous une sphère ; la plus sombre et la plus nette **au contact**, plus claire et plus large en s'éloignant |

Règles qui en découlent :
- **Deux familles** : tout ce qui voit la source (éclat, lumière, demi-ton) est plus clair
  que tout ce qui ne la voit pas (ombre propre, ombre, rebond), **dans une même matière**.
  Un rebond plus clair que le demi-ton casse la forme (règle 52). C'est ce que mesure la
  porte « Le volume suit la lumière » (part de la lumière plus sombre que l'ombre).
- **La forme du terminateur dit la forme de l'objet.** Sphère : arc d'ellipse. Cylindre :
  droite parallèle à l'axe. Boîte : une arête. Forme organique : une courbe qui ondule avec
  les bosses.
- **La hauteur de la lumière** règle la part éclairée : rasante = moitié dans l'ombre, haute =
  un mince croissant d'ombre. L'onglet Lumière montre l'effet sur le guide.
- **Bord du terminateur** : doux sur une forme ronde (une marche de demi-ton, un AA) ; dur
  sur une arête (saut direct de la lumière à l'ombre).
- **Le guide de volume** de l'onglet Lumière gonfle la silhouette (ou y inscrit une sphère,
  un cylindre) et colore ces zones par-dessus la toile. **Il ne dessine rien** : tu poses
  chaque pixel (règle 60). Il se trompe sur les formes complexes (creux, pièces qui se
  recouvrent) : découpe alors la forme en pièces et raisonne pièce par pièce.

## 0-D. Le design des valeurs [D5][D6]

1. **Plisser les yeux** (vue Notan) : l'image se réduit à deux grandes masses, lumière et
   ombre. Si elles sont morcelées, le volume ne se lit pas, quelle que soit la finition.
2. **Deux valeurs, puis trois** (Marco Bucci) : d'abord une valeur de lumière et une
   d'ombre par matière ; ensuite le demi-ton qui marque le passage. Le reste (rebond,
   éclat, occlusion) vient après et **ne casse jamais** les deux masses.
3. **Océans, lacs, rivières** (Proko) : une grande masse (l'océan) contient des formes
   moyennes de l'autre famille (lacs) et de petites (rivières). Pas de semis de petites
   taches de même taille.
4. **Toute l'échelle** : à 32 px et plus, un sprite pro va de presque noir (contour,
   occlusion) à presque blanc (éclat). L'onglet Lumière affiche l'**étendue** : sous 0,45, le
   dessin est terne.
5. **La valeur dit la lumière, la couleur dit la matière.** Une matière sombre en lumière
   peut être plus sombre qu'une matière claire à l'ombre : la règle des familles s'applique
   **matière par matière**, c'est ainsi que l'app la mesure.
6. **Le plus fort contraste au point d'intérêt** (A2), les contrastes faibles ailleurs.

## 0-E. Le design des formes [D7][D8]

1. **Grand, moyen, petit** (Sinix) : une forme domine, une moyenne la complète, une petite
   donne l'accent. Jamais trois formes de même taille (A4b).
2. **Droites contre courbes** : une courbe prend sa tension contre une droite. Un contour
   tout en courbes molles fait amateur ; une alternance (flanc tendu, bosse franche) fait
   pro. En pixels : une courbe tendue = un long palier puis des marches qui s'accélèrent
   (6-4-2-1-1), pas une suite de bosses égales.
3. **Pas de tangentes** (deux contours qui se frôlent), **pas d'écarts réguliers**, **pas de
   parallèles** inutiles : ils aplatissent l'image.
4. **Les taches se dessinent** : la tache de lumière, la forme de l'ombre portée, l'éclat,
   la surface du liquide sont des **formes** choisies (un croissant, une fenêtre, une
   goutte), pas des restes de remplissage.
5. **Silhouette lisible** (A2) : vides entre les pièces, pièce qui dépasse (marque-page du
   livre, flamme qui s'échappe, feuille de la poire).

## 0-F. Perspective utile au sprite [D1][D2]

- **Niveau de l'œil** : une icône d'objet est vue un peu d'en haut. On voit donc **le dessus**
  des ouvertures et des liquides : ce sont des ellipses.
- **Les ellipses s'ouvrent en s'éloignant du niveau de l'œil** : celle du goulot (près de
  l'œil) est plus fine que celle du niveau du liquide, plus fine que la base. Toutes ont
  leur petit axe sur l'axe de l'objet.
- **Moitié avant, moitié arrière** : la moitié avant d'une ellipse est plus marquée (plus
  sombre, plus nette) que la moitié arrière, vue à travers le verre ou cachée.
- **Boîte** : en vue de jeu, deux faces visibles + le dessus ; arêtes verticales
  verticales ; isométrique en 2:1 (A9).
- **Ce qui est loin rapetisse et pâlit** (F3-A) ; à l'échelle d'un objet, la face qui fuit
  est plus étroite que la face de devant.

## 0-G. Couleur [B5][D9]

1. **Trois couleurs se mélangent** sur une surface : la couleur locale (la matière), la
   couleur de la lumière (chaude ou froide) et la couleur ambiante (ciel, pièce) qui remplit
   l'ombre. **Lumière chaude → ombre froide**, et inversement : c'est la vraie raison du
   glissement de teinte (A6-A), pas une habitude.
2. **La saturation culmine au demi-ton**, près du terminateur. La lumière se désature vers
   la couleur de la source ; l'ombre perd en saturation et vire vers l'ambiante. Un rouge
   pur dans la lumière fait plastique et plat.
3. **Le rebond prend la couleur de ce qui le renvoie** (sol vert = rebond verdâtre).
4. **Diffusion sous la surface** (peau, gelée, cire, feuille, liquide coloré) : au bord du
   terminateur l'ombre devient **plus saturée et plus chaude**, et la matière s'éclaire à
   contre-jour (Gurney).
5. **Une couleur d'accent**, la plus saturée, seulement au point d'intérêt. Palette limitée
   (masque de gamme, F4).
6. **La variation de couleur vient en dernier** (planches : étape 7-8) : quelques taches de
   teinte voisine dans les grandes masses, **sans changer la valeur** (vérifier en gris).

## 0-H. Les bords [D10][R]

- **Dur** au point d'intérêt et sur les arêtes ; **doux** sur les formes rondes ; **perdu**
  là où deux valeurs se confondent (lumière forte contre fond clair).
- En pixels : bord dur = saut direct de tons ; bord doux = une marche intermédiaire ou un
  pixel d'AA (A6-F) ; bord perdu = contour éclairci (selout) ou interrompu côté lumière
  (A6-C, contour cassé).
- Varier les bords **relativement** : un seul type de bord partout aplatit l'image.

## 0-I. Matières : ce que chaque surface fait de la lumière [D3][B5][P3]

| Matière | Passage lumière/ombre | Éclat | Contraste | À faire |
|---|---|---|---|---|
| **Mat** (bois, tissu, pierre, pain) | large, doux | aucun ou très diffus | moyen | texture dans le demi-ton, lumière calme |
| **Brillant** (plastique, vernis, fruit lisse) | assez net | net, en forme, de la couleur de la source | fort | un grand reflet en forme + 1-2 points |
| **Métal** | presque pas de couleur locale : il reflète l'environnement | très net, très clair | extrême | ciel clair en haut, sol sombre en bas, ligne d'horizon nette ; ombres teintées par l'entourage |
| **Verre transparent** | on voit **à travers** | arc net qui suit la forme, par-dessus tout | les reflets font le volume | voir la recette 0-L-A |
| **Liquide coloré** (dans un verre) | la lumière le traverse | sur le verre, pas dans le liquide | moyen | surface en ellipse claire ; côté opposé à la lumière **plus clair** (lumière transmise) ; bulles = petits cercles clairs à bord sombre côté lumière |
| **Translucide** (gelée, cristal, peau, feuille) | doux, saturé au terminateur | net si la surface est lisse | moyen | contre-jour coloré, zone claire du côté opposé à la lumière, ombre saturée |
| **Émissif** (flamme, magie, lave) | **pas d'ombre propre** : la valeur monte vers le cœur | — | fort entre cœur et bord | couches de lueur (planche flamme), halo sur l'entourage, aucun contour sombre |

## 0-J. Méthode de travail du pro [D6][R][P3]

1. **Viser un niveau** : avant de dessiner, choisis une œuvre pro précise (une planche, un
   sprite de jeu) et écris ce que tu en prends (champ « Niveau visé » de la fiche). Importe-la
   en calque de référence (G2), à côté de la toile.
2. **Du général au particulier** : silhouette → construction → deux valeurs → trois valeurs →
   matière → finition. On ne passe à l'échelle suivante que si la précédente tient à ×1
   (les planches montrent chaque étape lisible seule).
3. **Toute la toile en même temps** : on ne finit pas un coin avant les autres ; chaque
   passe couvre tout l'objet.
4. **Comparer côte à côte**, à la même taille, souvent : référence, ×1, Notan, gris, miroir.
   Écrire l'écart (« ma surface de liquide est plate, la sienne est une ellipse »).
5. **Corriger la cause, pas le symptôme** : un volume qui ne tourne pas se corrige au
   terminateur, pas avec un éclat de plus.
6. **Finition des planches** : halo, étincelles en croix, ombre portée, contour d'accent :
   seulement quand le volume est juste.

## 0-K. Les planches de tutoriels analysées [P3][P4]

Fournies par l'utilisateur : potion (anonyme), cristal, sphère, livre, pierre et flamme
(style Rappenem), poire, pain (signé EMIL), portail en ruines (signé ELE). Les règles sont
reformulées ; les planches ne sont pas copiées dans le projet. En v18 s'ajoutent deux
planches [P4] : slime (style Rappenem, 6 étapes) et gemmes (signée sadface_rl, 12 étapes).

**Ce qu'elles font toutes :**
1. **Chaque étape se lit seule à ×1**, et une seule idée change d'une étape à la suivante.
2. **La construction précède la couleur** : trait de construction (cristal, livre, portail,
   pierre) ou masse plate (poire, pain, flamme). Le portail garde ses lignes de construction
   **par-dessus** la couleur jusqu'à l'étape 4.
3. **La lumière est dessinée** sur la planche (un point jaune et un cône) avant l'ombrage.
4. **Deux valeurs d'abord** (sphère 2, cristal 4, poire « shading », pain « shape »), puis
   les secondaires.
5. **Le contour devient couleur après la lumière** (« swap edge color », « colored
   outlines ») ; le pain et la flamme n'ont **aucun** contour sombre.
6. **Une deuxième lumière d'une autre teinte** (contre-jour, rebond coloré) arrive tard.
7. **La variation de couleur** arrive presque à la fin.
8. **La finition ancre et anime** : ombre portée (sphère, pain), halo, étincelles, braises.
9. **Toute l'échelle des valeurs** est utilisée dans la version finale.

**Ce que chacune apprend en plus :**

| Planche | Leçon propre |
|---|---|
| **Potion** (9) | Le niveau du liquide est une ellipse **dès le trait** (étape 1). Verre bleu clair, liquide vu au travers. « Swap edge color » : le trait du verre s'éclaircit, celui du liquide devient rouge sombre. Lumières (5) : grand croissant clair sur le haut du verre, côté lumière. Ombres secondaires (6) : bande violette en bas du liquide, côté ombre. Éclats (7) : points blancs sur le verre. Bulles et contre-jour (8). Fin (9) : contour d'accent doré, étincelles. |
| **Cristal** (9) | Esquisse libre puis trait nettoyé ; facettes tracées avant l'ombre ; contre-jour rose en bas à l'opposé (B6-D). |
| **Sphère** (9) | L'exercice de base : 2 valeurs → ombre et lumière secondaires → **terminateur et éclat** → **rebond et contour coloré** → fondu et AA → variation de couleur → **ombre portée** → finition. À refaire dans 8 directions de lumière (0-M). |
| **Poire** (4) | Masse plate sans contour → contour → ombrage **en plans** (facettes plates qui décrivent les deux sphères) → polissage (blush rouge, rebond violet en bas, éclat doux, variation). Penser en plans avant d'arrondir. |
| **Livre** (9) | Boîte en perspective → séparer couverture et pages → nettoyer → décor au trait **avant** la couleur → aplats → ombrage → lumières et ombres secondaires → contour coloré et glissement de teinte → finition (B6-F). |
| **Pain** (4) | Tache → formes (dessus clair, flanc sombre, entailles) → ombrage riche et chaud → polissage : liseré de lumière blanc-crème sur le haut, éclats, **ombre portée douce**. Aucun contour : les formes se séparent par la valeur. |
| **Portail** (9) | Boîtes isométriques **dessinées à travers** → pièces (marches, piliers, socle) → masses colorées avec construction visible → construction effacée → pierres et fissures → lianes et mousse qui **cassent** les boîtes → variations de lumière → portail émissif qui éclaire l'intérieur de l'arche. |
| **Pierre** (9) | Cube → arêtes cassées → ombrage → trait intérieur effacé → fissures → trous → lumières et contour coloré → couleur → finition (B6-C). |
| **Slime** (6) [P4] | Trait et couleur de base, yeux en simples arcs → ombrage de base en deux valeurs, lumière posée en haut à droite (point et cône) → ombres et lumières secondaires en **bandes courbes** qui suivent le dôme → contour coloré (bleu sombre) et éclats blancs **en forme d'arc** sur le haut → contre-jour cyan en bas à l'opposé (point et cône dessinés aussi) et variation violette → ombre portée bleutée et nettoyage (B6-E). |
| **Gemme** (12) [P4] | Forme de base : un octogone allongé à **double bord** (le sertissage) → aplat → **dégradé en bandes diagonales**, dans la direction de la lumière → bandes lissées, régulières → bande la plus claire près du coin éclairé → **petite trame** seulement entre deux bandes → ombre sur le bord intérieur opposé → fondre → trame légère → lumière subtile (rebond sur le bord bas) → quelques éclats blancs **parallèles aux bandes** → une étincelle en croix sur un coin. Marche avec ou sans bordure et à plusieurs tailles : à petite taille, on garde l'idée (la diagonale claire) et on supprime la trame. |
| **Flamme** (9) | Une goutte qui ondule (geste en S) → langues de tailles différentes → trois couches de lueur **vers l'intérieur** (le cœur, en bas, est le plus clair) → teinte plus sombre aux pointes → variation (rose et cyan près du cœur) → braises → nettoyage. Émissif : pas d'ombre propre, pas de contour. |

## 0-L. Recettes en pixels

### A. Potion en verre transparent (32 à 64 px) [P3]
1. **Construction** : axe ; panse = cercle ; col = cylindre (deux ellipses fines) ; bouchon =
   calotte ; **niveau du liquide = ellipse** entière (moitié arrière comprise) à 40-55 % de
   la hauteur de la panse.
2. **Trait** : contour 1 px sombre ; la moitié avant de l'ellipse du liquide est tracée, la
   moitié arrière l'est d'un ton plus clair (vue à travers le verre).
3. **Aplats** : verre vide = bleu clair désaturé (la couleur du fond vu à travers, teintée) ;
   liquide = sa couleur moyenne ; surface du liquide = un ton plus clair que le liquide.
4. **Deux familles** (lumière en haut à gauche) : liquide clair à gauche, sombre à droite et
   en bas, terminateur en arc ; verre : sa moitié droite un ton plus sombre.
5. **Modelé** : ombre propre du liquide le long du terminateur ; **le bas du liquide, côté
   opposé à la lumière, s'éclaircit** (lumière transmise qui ressort, saturée) ; occlusion
   sous le bouchon et au fond.
6. **Matière** : grand reflet en croissant sur le haut gauche du verre, qui suit le cercle,
   **par-dessus** le liquide ; 1 ou 2 points blancs ; reflet fin le long du bord droit (la
   paroi qui renvoie le fond).
7. **Contour coloré** : le trait du verre devient bleu sombre (ou violet), celui du liquide
   rouge sombre ; plus clair côté lumière.
8. **Contre-jour** : 1 px d'une autre teinte (rose, cyan) sur le bord bas droit.
9. **Variation et finition** : 2 ou 3 bulles (cercle clair, 1-2 px, ombre côté lumière), un
   reflet de surface sur l'ellipse, ombre portée en ellipse, étincelles si objet magique.

### B. La sphère d'étude (à refaire souvent) [P3][D3]
Toile 32×32, sphère de 24 px, 5 tons + contour. Dans l'ordre : 2 valeurs (terminateur en
arc) → demi-ton → ombre propre → éclat (2×2 + 1 px) → rebond (1-2 px le long du bas, côté
ombre) → contour coloré (clair en haut à gauche, sombre en bas à droite) → AA sur les
marches de 2 px → ombre portée en ellipse aplatie (rapport 4:1), poussée à l'opposé. La
porte « Le volume suit la lumière » doit passer sans justification.

### C. Fruit (poire, pomme) [P3]
Deux sphères fondues ; ombrage **en plans** d'abord (3 tons, facettes plates), puis
fondre ; blush d'une teinte voisine sur le côté lumière ; rebond violet ou froid en bas ;
éclat doux (2 tons) ; tige et feuille comme pièces qui dépassent ; taches de surface en
groupes de 2-3 dans le demi-ton.

### D. Pain, gâteau, matières molles [P3]
Pas de contour noir : le bord le plus sombre est la couleur d'ombre de la croûte. Dessus
clair, flanc sombre chaud, entailles = creux (sombres côté lumière, lèvre claire côté
opposé, B6-C) ; liseré de lumière crème le long du haut ; ombre portée douce (deux tons, le
plus sombre au contact).

### E. Flamme et matières émissives [P3]
Geste en S → langues de tailles différentes qui suivent le geste → couches de lueur
concentriques vers le cœur (le plus clair près de la base) → bords des pointes plus sombres
et plus rouges → 1 ou 2 notes de teinte inattendue (rose, cyan) près du cœur → braises
détachées qui suivent le flux. Halo : 1-2 tons à peine plus clairs que le fond autour
(B6-D). Aucune ombre propre.

### G. Gemme polie (icône, 16 à 48 px) [P4]
Octogone allongé, contour + sertissage d'1 px plus clair → aplat moyen → 3 à 5 bandes
**diagonales** parallèles, de la plus claire (coin éclairé) à la plus sombre (coin opposé),
de largeurs **inégales** (grand, moyen, petit) → trame 50 % d'1 px seulement à la frontière
de deux bandes, à partir de 32 px (A7) → bord intérieur opposé à la lumière d'un ton plus
sombre → rebond d'1 px sur le bord bas → 2 ou 3 éclats blancs alignés sur les bandes →
une étincelle en croix détachée sur le coin éclairé. Déclinaison à 8-12 px : 2 bandes, un
éclat, pas de trame (B4b).

### F. Architecture en ruines (décor isométrique) [P3]
Boîtes en 2:1 dessinées à travers → pièces (socle, marches, piliers, linteau) → masses
colorées, une valeur par face (dessus clair, face éclairée moyenne, face d'ombre sombre) →
construction effacée → pierres et fissures dans les faces moyennes → végétation qui
**déborde** des arêtes (mousse sur le dessus, lianes qui pendent) → lumière d'une source
émissive (portail) sur les faces qui la voient.

## 0-M. Apprendre le dessin à la souris : le plan d'entraînement [D1][D3][R]

Claude dessine à la souris : il peut apprendre le dessin, pas seulement le pixel. Entre deux
projets (partie G), dans cet ordre, une séance par exercice (`--id etude-…`, non commitée) :

1. **Sphère d'étude** (0-L-B) sous 8 directions de lumière et 3 hauteurs : la porte
   « Le volume suit la lumière » doit passer chaque fois.
2. **Cylindre et boîte** sous la même lumière : terminateur droit, arête dure.
3. **Sphère en 4 matières** : mat, brillante, métal, verre avec liquide (0-I).
4. **Notans** : 3 petites vignettes de 16×16 en deux valeurs avant chaque dessin.
5. **Copies d'étude des neuf planches** (G2, type « Étude ») : analyser, copier à côté,
   refaire de mémoire, noter l'écart. Les copies restent privées et créditées.
6. **Construction** : 10 objets du quotidien en primitives dessinées à travers, au calque de
   construction seulement.

## 0-N. Vision et conception : penser le dessin avant de le dessiner [D11][D12][D13][D14]

Un pro ne pose pas le premier trait au hasard. Il **sait ce qu'il veut**, puis il
**l'éprouve** : il écrit, dessine petit, rate, barre, recommence. Dans Claude Pixel, ce
travail a deux étapes juste après la fiche : **Vision** et **Essais**, avec un **carnet de
conception** dans l'onglet Méthode.

### A. Le carnet : écrire, barrer, recommencer
- **Une idée par ligne**, rangée dans une rubrique : *Ce que je vois*, *Structure /
  physionomie*, *Formes de base*, *Ce qui la rend unique*, *Pourquoi c'est crédible*,
  *Essai*, *Choix retenu*.
- **On n'efface jamais.** Une idée qui ne tient pas se **barre**, avec sa raison (« trop
  proche d'une potion banale », « illisible à ×1 », « le bouchon ne tiendrait pas »). Le
  carnet garde la trace du chemin : c'est ce chemin qui mène à une forme juste.
- **Pas tout d'un coup.** On écrit une idée, on la questionne (« pourquoi cette forme ? qu'est-ce
  qu'elle raconte ? »), on la précise ou on la barre, puis on passe à la suivante.

### B. Les cinq questions de la vision
1. **Ce que je vois** : l'impression d'ensemble en une phrase. Ce qu'on doit sentir en une
   seconde (« une fiole fragile et précieuse, presque vivante »).
2. **Structure / physionomie** :
   - **Objet** : de quoi il est fait, comment les pièces tiennent, comment on le tient, comment
     il s'ouvre, se remplit, se pose. **La forme suit la fonction** : un objet inventé reste
     crédible s'il pourrait servir (une fiole a un goulot pour verser, un fond pour tenir
     debout, un bouchon qui ferme).
   - **Créature** : un squelette tiré d'animaux réels (Terryl Whitlatch combine des
     squelettes existants pour qu'un animal inventé reste plausible), comment elle se tient,
     se déplace, mange, se défend, où elle vit.
   - **Personnage** : proportions, appuis, ce que le corps dit de sa vie (âge, métier, force).
3. **Formes de base** : les primitives de départ (sphère, cylindre, cône, boîte, tore) et
   **comment on va les déformer**. Une base géométrique simple peut devenir une forme
   remarquable : on étire, on tord, on coupe, on fait se rencontrer deux formes, on varie
   les tailles (grand, moyen, petit).
4. **Ce qui la rend unique** : **une** idée forte (une silhouette inattendue, une matière,
   un détail de récit), pas cinq. Les autres choix restent sobres pour la servir.
5. **Pourquoi c'est crédible** : poids, équilibre, usage, logique interne. Une forme
   originale sans logique fait « décor de carton ».

### C. Les essais : vignettes, effacer, recommencer [D11][D12]
- **Petit et vite** : au calque de construction, des silhouettes de 8 à 16 px de haut. Plus
  un essai est petit, plus on accepte de le jeter.
- **Au moins trois silhouettes vraiment différentes** ; pousser chaque essai (largeur,
  hauteur, rythme, asymétrie, vides) et **ne pas en faire deux de suite trop proches**.
  Les derniers essais sont souvent les meilleurs : quand on croit avoir fini, en faire un
  de plus.
- **Silhouette d'abord**, sans couleur : si elle ne se lit pas en noir, aucun détail ne la
  sauvera. Exagérer ce qui définit l'objet pour qu'il se lise de loin.
- **Retourner (miroir) et regarder à ×1** chaque vignette.
- **Choisir, puis varier** : retenir une vignette, écrire pourquoi, et noter ce qu'il faut
  encore pousser. S'écarter de la vignette en cours de route est permis : on l'écrit au
  carnet.
- **Perfectionner jusqu'au détail** : même un pixel d'un col ou d'une ombre se rejoue s'il
  ne sert pas la forme. Annuler et refaire un trait n'est pas un échec, c'est le métier.

### D. Exemple : une fiole à la forme unique (carnet type)
1. *Ce que je vois* : ~~une potion ronde classique avec un bouchon~~ — barrée : « c'est
   l'icône que tout le monde fait, rien ne la distingue ».
2. *Ce que je vois* : une fiole fragile, comme une goutte suspendue qui va tomber.
3. *Formes de base* : une goutte = sphère + cône ; le col = un cylindre fin.
4. *Structure* : ~~la pointe de la goutte en bas~~ — barrée : « elle ne tiendrait pas
   debout ». La pointe passe en haut et devient le col ; le fond reste rond et lesté.
5. *Ce qui la rend unique* : le col se tord d'un quart de tour, comme du verre soufflé
   encore chaud.
6. *Pourquoi c'est crédible* : le verre soufflé se tord vraiment ; la torsion reste au col,
   la panse garde son volume pour le liquide.
7. *Essai* 1 : col droit, lisible mais banal. *Essai* 2 : col très tordu, illisible à ×1.
   *Essai* 3 : torsion légère, une seule courbe en S : lisible et différent.
8. *Choix retenu* : essai 3. À pousser : la goutte un peu plus étroite en haut que la panse
   (grand, moyen, petit : panse, col, bouchon).

## 0-O. Astuces de pro : dessiner mieux, créer plus beau [D5][D10][D11][D12][D13][D14][D15]

**Les grandes formes d'abord.** On bloque d'abord la plus grande forme, puis on découpe vers
les plus petites. Les grandes formes restent simples et peu contrastées. Elles servent de
repos et font ressortir les petits détails. Une image où tout est détaillé paraît plate.

**L'économie de moyens.** Le moins d'information possible pour le plus d'effet : chaque
pixel doit servir la forme, la lumière ou l'idée. Ce n'est pas plus facile qu'un rendu
détaillé, c'est plus juste.

**Le langage des formes.** Le rond est doux et amical, le triangle dynamique et dangereux,
le carré stable et solide. Une forme **dominante** fixe la lecture, une **secondaire** y
ajoute de la nuance. Les designs mémorables mêlent souvent deux formes en tension (une
panse ronde avec un col anguleux).

**Contraste et variété.**
- Varier : grand/petit, droit/courbe, simple/détaillé, dur/doux, saturé/neutre.
- Répéter avec variation : un motif repris mais jamais identique crée un rythme. Une
  rupture de rythme attire l'œil : on la place au point d'intérêt.
- Laisser des zones de repos (lumière calme, aplat) autour des zones riches.
- Grouper les détails par 2-3 (A5-9), jamais en semis régulier.

**Le point d'intérêt.** Un seul : le plus fort contraste de valeur, le bord le plus dur, la
couleur la plus saturée et le détail le plus fin s'y retrouvent. Le reste de l'image le
sert.

**Pousser l'idée.** Exagérer ce qui définit le sujet (une fiole plus fine et plus haute, une
créature plus massive). Une forme timide se lit mal à petite taille.

**Regarder autrement, souvent.** Retourner l'image (miroir), la regarder en gris, plisser
les yeux, dézoomer à ×1, faire une pause. On voit alors ce que l'habitude cache (A11-C).

**Apprendre des maîtres.** Copier (en privé, crédité) les œuvres qu'on admire et noter
**pourquoi** elles marchent (G2). Garder une bibliothèque de références classées par
problème (verre, métal, feuillage, plis).

**Accepter le raté.** Les pros annulent, effacent et refont beaucoup. Un dessin juste vient
d'une suite de corrections, pas d'un premier jet parfait.

## 0-P. Inventer : des méthodes pour trouver des formes neuves [D16][D13][D14]

La créativité se travaille. Ces méthodes servent à l'étape **Vision** : chaque idée qu'elles
donnent va au carnet, rubrique **Variante**, puis se garde ou se barre.

### A. SCAMPER : questionner une forme connue
On part d'un objet connu (une fiole ronde) et on lui pose sept questions :

| Lettre | Question | Exemple sur une fiole |
|---|---|---|
| **S**ubstituer | Et si une pièce était faite d'autre chose ? | un bouchon en cristal, une panse en coquille |
| **C**ombiner | Et si on fondait deux objets ? | fiole + sablier : le liquide s'écoule d'une panse à l'autre |
| **A**dapter | Qu'est-ce qui, ailleurs, résout le même problème ? | une goutte de rosée, une graine, un fruit |
| **M**odifier | Et si on agrandissait, étirait, tordait une partie ? | un col très long et tordu, une panse aplatie |
| **P**roposer un autre usage | Et si l'objet servait aussi à autre chose ? | une fiole qui sert de lanterne |
| **É**liminer | Que se passe-t-il sans telle pièce ? | pas de bouchon : le liquide est tenu par une bulle de magie |
| **R**enverser | Et à l'envers, à l'intérieur dehors ? | la fiole en bas, le liquide qui monte vers le haut |

SCAMPER ne garantit rien : il donne des pistes. On en garde une ou deux, on teste en
vignette, on barre le reste.

### B. Le tableau morphologique : combiner les solutions
Lister les **parties** de l'objet en lignes et, pour chacune, 3 ou 4 **solutions** en
colonnes. Une combinaison = une ligne choisie par partie. Exemple :

| Partie | Solution 1 | Solution 2 | Solution 3 | Solution 4 |
|---|---|---|---|---|
| Panse | sphère | goutte | cœur | cristal taillé |
| Col | court et large | long et fin | tordu | double |
| Bouchon | liège | cristal | métal à anneau | cire scellée |
| Décor | aucun | cerclage de métal | étiquette | runes gravées |

On tire 3 combinaisons très différentes : ce sont les trois vignettes de l'étape **Essais**.

### C. Mélanger les références, pas les copier
- **Deux sources ou plus**, jamais une seule : une forme naturelle (coquillage, graine,
  insecte) + un objet fabriqué (verrerie, armure) donnent une forme neuve **et** crédible.
- Pour une créature : un squelette, une peau, un comportement tirés d'animaux réels
  différents (Whitlatch, 0-N-B).
- On prend un **principe** à chaque source (une courbe, une articulation, une matière), pas
  son apparence entière.

### D. Les contraintes aident
Une palette imposée, une taille fixe, une forme de départ unique : moins de choix forcent
des solutions plus inventives. La fiche (taille, couleurs, projection) fixe ces contraintes
avant la vision.

## 0-Q. Le geste : courbes en C, en S, et droites [D17]

- **Trois traits seulement** pour le geste : la courbe en **C**, la courbe en **S** et la
  **droite**. Rien de plus compliqué.
- **La ligne d'action d'abord** : la plus longue courbe qui traverse le sujet (de la tête aux
  pieds, du bouchon au fond d'une fiole). Tout le reste s'y accroche.
- **Courbe contre droite** : un côté tendu (C) face à un côté droit donne du rythme ; deux
  côtés courbes identiques donnent une forme molle (0-E).
- **Rythme** : des S qui s'enchaînent = calme et souple ; des zigzags = tension, danger.
- **En pixels** : un C = une suite de marches qui s'allongent puis raccourcissent (1-2-3-3-2-1) ;
  une droite = des marches égales ; un S = deux C opposés qui se rejoignent par leur marche
  la plus longue.
- Même un objet a un geste : une fiole qui « penche » un peu, une flamme qui monte en S, un
  pain légèrement cintré paraissent vivants.

## 0-R. Harmonies de couleur [D9][D18]

- **Palette limitée** : moins de teintes = plus d'unité et plus d'attention aux valeurs.
- **Une couleur domine**, une seconde la soutient, une **troisième sert d'accent**. Repère :
  environ 60 % / 30 % / 10 % de la surface.
- **Analogue** (teintes voisines) : calme, unité ; ajouter un accent pour vivre.
- **Complémentaire** (opposées) : contraste fort ; une domine, l'autre seulement en accent,
  près du point d'intérêt.
- **Complémentaire adjacente** (une teinte + les deux voisines de son opposée) : contraste
  plus doux, plus facile à tenir.
- **Varier sans ajouter de teinte** : éclaircir, assombrir, désaturer une teinte de la
  palette plutôt qu'en inventer une nouvelle.
- Le glissement de teinte des ombres et lumières (A6-A, 0-G) suit la **lumière** choisie :
  une harmonie se décide en même temps que la lumière.

## 0-S. Matières, suite : métal et textures [D19][D20]

### A. Métal
- **Le métal n'a presque pas de couleur propre** : il reflète son entourage. Décider
  l'entourage d'abord (ciel clair au-dessus, sol sombre en dessous).
- **Chrome / poli** : reflets **nets et durs**, contraste extrême, ombre presque noire,
  ligne d'horizon nette dans le reflet, contour net.
- **Brossé** : les reflets **s'étirent dans le sens du grain** (bandes longues au lieu de
  taches rondes), contraste moindre.
- **Usé** : arêtes plus claires là où on touche, creux plus sombres et ternes, quelques
  rayures (sombre + lèvre claire, B6-C).
- Le métal **reprend un peu la couleur** des objets voisins dans ses reflets.

### B. Textures en pixels
- **Une texture = quelques amas répétés**, de même forme, mais distribués de façon
  irrégulière. Pas de pixels isolés, qui font du bruit (A5-9).
- **Bois** : lignes presque parallèles mais ondulées, nœuds en ovales autour desquels les
  lignes s'écartent. Si le contexte dit « bois » (planche, manche), peu de texture suffit.
- **Tissu** : la texture se lit surtout par les plis (C17) ; usure = pièces, coutures,
  accrocs, plutôt qu'une trame partout.
- **Fourrure, herbe** : trop fines pour être dessinées brin à brin : on **suggère** par le
  contour (petites mèches qui dépassent) et quelques mèches dans le demi-ton.
- **Feuillage** : des amas en forme de feuille, d'œuf ou de boule, de taille et
  d'espacement réguliers dans une masse, éclairés comme une seule grande forme (0-C) :
  la masse d'abord, les feuilles ensuite.
- **La texture vit dans le demi-ton** : elle disparaît dans la pleine lumière et dans
  l'ombre profonde (A4, 0-D).

## 0-T. Perspective avancée et raccourcis [D1][D21]

### A. Trois indices de profondeur, à ne pas confondre
- **Diminution** : ce qui est loin est plus petit. Deux sujets censés avoir la même taille :
  le plus petit paraît plus loin.
- **Convergence** : les droites parallèles qui s'éloignent se rejoignent en un point de
  fuite.
- **Raccourci** : une forme **tournée vers l'œil** se tasse dans sa longueur. Le raccourci
  dépend de l'**orientation** de la forme ; la diminution, de sa **distance**.
- **Recouvrement** : le plus sûr des indices. Ce qui est devant cache ce qui est derrière
  (0-B-6). Dans un sprite, c'est souvent le seul qui reste lisible.

### B. Un, deux, trois points de fuite
- **Un point** : on voit une face de face, les fuyantes vont vers un seul point (couloir,
  route, objet vu de face). La plupart des icônes « de face » en sont une version
  aplatie.
- **Deux points** : on voit un coin de la boîte ; deux familles de fuyantes vont vers deux
  points sur la ligne d'horizon, les verticales restent verticales. C'est la vue des
  objets posés et des bâtiments en 3/4.
- **Trois points** : les verticales convergent aussi (vue très en plongée ou en
  contre-plongée) : effet de hauteur, de vertige, de puissance.
- **Pour un jeu**, on choisit une projection fixe (A9, règle 33) : de face, 3/4 de dessus ou
  isométrique 2:1. Les règles de perspective servent alors à **placer les ellipses, les
  pentes et les recouvrements**, pas à dessiner des fuyantes exactes.

### C. Raccourcis : la boîte qui vient vers nous
- **Une boîte dont les deux bouts ont presque la même taille** est peu raccourcie ; si le
  bout proche est **beaucoup plus grand**, le raccourci est fort.
- **Un membre en raccourci** (bras tendu vers le spectateur) : dessiner une suite de
  cylindres qui **se recouvrent**, le plus proche devant et plus gros ; la main paraît
  grande, l'avant-bras court. Les ellipses des coupes deviennent presque des cercles.
- **En pixels** : le raccourci se lit surtout par le recouvrement et par un contour plus
  épais ou plus sombre sur la pièce proche. Éviter les raccourcis extrêmes sous 32 px :
  ils deviennent illisibles ; préférer une pose de profil ou de 3/4 qui dit la même chose.

## 0-U. Anatomie animale et créatures [D13][D22]

### A. Les trois façons de marcher (le pied fait l'animal)
| Type | Exemples | Ce qui touche le sol | Ce qu'on voit |
|---|---|---|---|
| **Plantigrade** | humain, ours, raton | toute la plante du pied | talon au sol, pied long et plat |
| **Digitigrade** | chien, chat, loup, la plupart des oiseaux | les doigts | **le talon est haut** : le « genou à l'envers » est en fait la **cheville** |
| **Onguligrade** | cheval, cerf, vache | le bout du doigt (sabot) | jambe très longue et fine, la cheville encore plus haut |

- Le **vrai genou** d'un chien ou d'un cheval est **haut, près du ventre**, caché dans le
  corps. Dessiner un genou « humain » à mi-jambe fait faux tout de suite.
- **Pattes avant** : le coude est près du torse et plie **vers l'arrière** ; le poignet est le
  « genou » visible à l'avant.
- Ne pas plaquer le pied humain sur un animal : un ours qui marche sur la pointe des pieds
  paraît faux.

### B. Le quadrupède en volumes
- Trois masses : **cage thoracique** (grosse, en œuf), **bassin** (plus petit), **tête** ; le
  cou et la colonne les relient en une courbe (ligne d'action, 0-Q).
- Les pattes s'accrochent **sous** les masses (épaule sous la cage, hanche sous le bassin),
  pas sur les côtés comme des pieds de table.
- L'omoplate glisse sur la cage : quand une patte avant avance, l'épaule monte.
- Le poids se lit dans les appuis : la tête et la cage sont lourdes, deux pattes au sol au
  moins sous le centre de gravité.

### C. Oiseaux
- **L'aile est un bras** : épaule, coude, poignet, main. Les plumes s'organisent en
  **groupes** : **primaires** sur la main (longues, au bout), **secondaires** sur
  l'avant-bras, **tertiaires** près du corps, et les **couvertures** en rangées courtes qui
  recouvrent la base des plumes de vol.
- **Aile pliée** : les secondaires recouvrent les primaires ; l'aile forme une goutte posée
  contre le flanc.
- **Dessiner des masses, pas des plumes** : la silhouette de l'aile d'abord, les groupes
  ensuite, quelques plumes seulement au bord, comme détail final.
- Les pattes d'oiseau sont digitigrades : la « jambe » visible est le pied.

### D. Insectes et petites bêtes
- **Trois parties** : tête, **thorax**, abdomen. **Les six pattes et les ailes partent du
  thorax**, jamais de l'abdomen. Un thorax trop petit donne des pattes « collées ».
- Pattes **en segments coudés**, pas en bâtons. Abdomen = souvent la plus grosse masse,
  segmentée ou rayée.
- Construire sur un **axe** : trois ovales, puis les pattes en paires symétriques.
- Arachnides : deux parties et **huit** pattes ; ne pas les confondre.

### E. Inventer une créature crédible (rappel 0-N)
Un squelette tiré d'animaux réels, un type de pied cohérent avec son sol, une façon de
manger visible (bec, crocs, trompe), des marqueurs d'identité (C15). Combiner des
**principes** d'animaux différents, pas coller des morceaux.

## 0-V. Mains, expressions, jeu d'acteur [D23][D24]

### A. La main
- **La paume est une boîte** (un peu plus large en haut), **les doigts une moufle** avant
  d'être des doigts : on dessine d'abord la masse de la moufle, puis on la découpe en
  quatre.
- **Les jointures** forment des arcs, pas une ligne droite ; le majeur est le plus long.
- **Le pouce** part du bas de la paume : une sphère (sa base charnue) + un cylindre.
- **Bouts des doigts arrondis**, jamais en pointe.
- **Grouper les doigts** : une main vivante garde ses doigts en groupes ; on n'en sépare un
  que pour un geste (montrer, tenir).
- **Dessiner les vides** entre les doigts : ils donnent la forme des doigts.
- **En pixels** : sous 32 px, une main = une moufle de 2-3 px avec un pouce d'1 px (C10-I) ;
  le geste se lit par la silhouette de la moufle, pas par les doigts.

### B. Le visage qui joue
- **Trois zones suffisent** : sourcils, yeux, bouche. Les **sourcils** portent le plus
  d'émotion pour le moins de pixels.
- **Combiner** : sourcils bas et rentrés + bouche en arc vers le bas = colère ; intérieur des
  sourcils relevé + coins de bouche baissés = tristesse ; sourcils hauts + bouche ouverte =
  surprise ; yeux plissés + coins relevés = joie.
- **Asymétrie** : un vrai visage est rarement symétrique ; un sourcil plus haut que l'autre
  rend l'expression vivante.
- **La tête penche avec l'émotion** (baissée : tristesse, honte ; relevée : fierté, défi).
- **Lecture immédiate** : un joueur regarde un sprite une fraction de seconde. On exagère.
- Recettes au pixel : C10-E.

### C. Le corps qui joue
- **L'émotion vient de tout le corps** : posture, expression, accessoires, décor, couleur.
- **Pose = verbe** : choisir ce que fait le personnage (« guette », « hésite », « fonce »),
  pas « se tient debout ». La ligne d'action (0-Q) traduit ce verbe.
- **Silhouette lisible** : bras détachés du corps quand le geste compte (C2).
- **Accessoires qui racontent** : un outil dit un métier, une cicatrice une histoire (0-Y).

## 0-W. Éclairages complexes [D25][B5]

- **Une hiérarchie de lumières** : une lumière **principale** (la plus forte), une lumière
  de **remplissage** (faible, adoucit l'ombre), des **accents** (contre-jour, reflets). Jamais
  deux lumières de même force : elles se disputent et aplatissent la forme.
- **Opposer les températures** : principale chaude, contre-jour ou ambiance froide (ou
  l'inverse). C'est ce qui sépare les sources à l'œil.
- **Contre-jour (rim light)** : un liseré sur le bord opposé à la principale ; il **détache**
  le sujet du fond (B6, 0-C).
- **Valeurs d'abord** : poser l'éclairage en gris (notan) avant les couleurs, même avec
  plusieurs sources.
- **Lumière colorée** : un objet éclairé par une lumière colorée prend sa teinte dans la
  famille lumière ; son ombre tire vers la **complémentaire** ou vers l'ambiante.
- **Nuit** : ce qui émet de la lumière devient le point d'intérêt (lampe, fenêtre, feu) ;
  l'ambiance est sombre, froide et désaturée ; les lumières pratiques (lanterne,
  réverbère) donnent des contre-jours forts.
- **Sources proches** (bougie, torche) : la lumière tombe vite avec la distance ; forte
  différence entre la face proche et l'arrière ; halo autour de la source (B6-D).
- **Brume, fumée** : les lumières s'étalent en halo, les bords s'adoucissent, les couleurs
  pâlissent avec la distance (F3-A).
- **Dans l'app** : l'onglet Lumière règle la **principale** ; les lumières secondaires se
  raisonnent à la main et se notent au carnet.

## 0-X. Effets naturels : fumée, eau, feu, explosion, étincelles [D26][P3]

Les guides de particules travaillent souvent avec du flou et de la transparence. **En pixel
art, on traduit** : pas de pixels semi-transparents (règle 46) ; la transparence devient des
**paliers de valeur** et des amas, et le flou une **trame** ou une marche de ton.

- **Fumée, poussière, nuages** : des **boules** groupées, les plus denses au centre, plus
  petites et plus claires (ou plus sombres) vers l'extérieur ; tailles **variées** (grand,
  moyen, petit) ; éclairées comme un seul volume (0-C : dessus clair, dessous sombre). En
  animation, les boules grossissent, pâlissent et se séparent.
- **Eau qui coule, éclaboussure** : une forme principale (jet, langue) + des gouttes
  détachées de tailles différentes ; reflets nets et clairs sur le dessus ; la même forme
  qu'une fumée recolorée en bleu peut servir d'écume.
- **Surface d'eau** : quelques lignes claires horizontales, brisées, plus serrées au loin ;
  reflets étirés à la verticale sous les objets.
- **Feu** : planche flamme (0-K, 0-L-E) : geste en S, cœur clair à la base, pas d'ombre
  propre.
- **Explosion** : un **flash** clair qui grandit très vite et ne dure pas (sinon il devient
  une lampe), puis des cercles plus sombres vers l'extérieur ; ensuite fumée grise et
  noire qui rétrécit, se disloque et retombe ; **débris** et poussière la rendent
  crédible.
- **Étincelles, électricité** : une ligne principale, une seconde plus fine qui la croise,
  des branches au hasard ; un halo de 1-2 tons autour (B6-D).
- **Lisibilité** : un effet doit rester plus simple que le sujet qu'il accompagne, et ne
  jamais cacher le point d'intérêt.

## 0-Y. Stylisation et cohérence d'un style [D27]

- **Styliser = simplifier et exagérer exprès**, en gardant le sujet reconnaissable. On
  choisit ce qu'on garde (les traits d'identité, A10-F) et ce qu'on supprime.
- **Une base réaliste, une exagération contrôlée** : on part de la vraie structure (0-B,
  0-U), puis on pousse la forme ou la couleur dans une direction choisie (plus rond, plus
  anguleux, plus haut, plus saturé).
- **Styliser n'est pas moins de travail** : chaque simplification est une décision. Une
  stylisation mal faite paraît bon marché.
- **Un seul style pour tout le jeu** : fixer tôt une **fiche de style** et s'y tenir :
  - contour (noir, coloré, cassé, absent ; 1 ou 2 px) ;
  - angles (arrondis ou vifs) ;
  - ombrage (cel en 2-3 tons, ou modelé doux) ;
  - densité de détail par taille (A3) ;
  - palette et nombre de couleurs ; lumière (direction unique, règle 23) ;
  - proportions (nombre de têtes, C1).
- **Ne jamais mélanger des styles au hasard** dans une même scène : un objet en modelé doux
  à côté de personnages en cel saute aux yeux.
- **Dans l'app** : noter la fiche de style au carnet (rubrique *Ce que je vois* ou
  *Formes de base*) et la recopier d'un dessin à l'autre.

## 0-Z. Raconter en une image [D28]

- **Un seul point d'intérêt**, autour duquel tout s'organise (0-O). Trop de symboles
  qui se disputent noient le sens.
- **Guider l'œil** : le plus fort contraste, la lumière, les lignes directrices (route,
  bord, regard, alignement d'objets), les diagonales et les triangles pour le dynamisme.
- **Placement** : sur un tiers plutôt qu'au centre pour une scène (F5) ; au centre pour une
  icône.
- **Un point secondaire peut appuyer le récit**, sans jamais dominer le premier.
- **Le moment clé** : choisir l'instant le plus parlant (juste avant l'action, ou son
  sommet) et laisser des indices de ce qui s'est passé avant.
- **Le décor raconte** : usure, objets abandonnés, traces, architecture disent l'histoire et
  l'époque sans texte. Même un objet seul raconte : une fiole fêlée et réparée, un livre
  aux coins usés (B6-F).
- **Laisser deviner** : quelques indices bien choisis valent mieux qu'une explication ; le
  spectateur complète.
- **Dans l'app** : la rubrique *Ce qui la rend unique* du carnet porte souvent ce récit.

## 0-AA. Dessiner une forme belle : le design d'objet [D7][D29][D30][T17]

Le rendu sublime une forme, il ne la sauve pas. Avant toute lumière, la **silhouette et
ses pièces** doivent déjà être belles en noir sur blanc. C'est le niveau où se joue la
différence entre un débutant et un pro.

### A. Contre-exemple : la fiole de la séance `fiole-unique` [T17]
Rendu correct, design raté. Ce qui n'allait pas :
1. **Quatre langages qui ne se parlent pas** : panse ronde, col en tube droit, bouchon en pique
   triangulaire, pied en plaque. Aucune pièce ne répond à une autre.
2. **Proportions molles** : col aussi haut que la panse et de largeur constante. On lit un
   ballon de chimie, pas un objet précieux.
3. **Jonctions nues** : le col sort de la panse sans épaule ni bague, le goulot n'a pas de
   lèvre, le pied est posé sans tige. Or c'est aux jonctions que la forme devient belle.
4. **Bouchon non dessiné** : 3 px en pique sur une barre, illisible et sans rapport avec la
   panse.
5. **Asymétrie timide** : un col penché d'1 px se lit comme une erreur, pas comme une
   intention.
6. **Processus pauvre** : 3 vignettes de 15 px, trop petites pour designer, choisies « la moins
   mauvaise », sans critique de la beauté ni variantes des pièces.

### B. Les principes d'une belle forme
1. **Un langage dominant, un accent.** Rond dominant + une pointe, ou anguleux dominant + une
   courbe (0-O). Toutes les pièces parlent ce langage.
2. **Un motif répété à trois échelles.** La forme de la panse revient, plus petite, dans le
   bouchon, puis en détail (perle, gravure, pied). Exemple : panse en goutte → bouchon en
   goutte → petite goutte gravée sur le pied. C'est ce qui donne l'unité.
3. **Des proportions franches, jamais 1:1.** Panse : col : bouchon ≈ 3 : 1,5 : 1 (ou le nombre
   d'or, 1 : 1,6). Un col est soit court et trapu, soit long et très fin **exprès** ; jamais
   entre les deux.
4. **Les jonctions sont des moments de design.** Épaule qui s'arrondit, bague ou collerette au
   col, lèvre retournée au goulot, tige puis disque au pied. Ces petites bandes créent le
   rythme grand-petit-grand.
5. **Le contour a un rythme.** Lire le contour comme une phrase : longue courbe calme,
   pincement, évasement, petit détail, longue courbe. Jamais une suite de bosses égales.
6. **Une ligne de flux traverse l'objet.** De la pointe du bouchon au pied, une courbe en S ou
   en C (0-Q) organise tout. L'asymétrie est **franche** (au moins 2-3 px à 32 px) ou absente.
7. **Le bouchon est un objet à part entière.** C'est la « tête » de la fiole : il porte le
   motif en petit, il a sa silhouette, il se lit à ×1. Il se dessine en au moins 3 variantes.
8. **Le poids visuel est en bas**, ou une fragilité voulue (pied fin sous une panse lourde) et
   assumée.
9. **Peu de zones de détail.** Une ou deux (col et bouchon, par exemple) ; la panse reste calme
   pour porter la lumière et la matière.
10. **Une silhouette qui ne se confond pas.** Test : la poser à côté de trois silhouettes de
    potions génériques (ronde, conique, carrée). Si on hésite, on recommence.
11. **Pousser, puis revenir.** Exagérer jusqu'à « un peu trop », puis reculer d'un cran : la
    forme timide ne se lit pas en petit.
12. **L'appeal** (*The Illusion of Life*) : charme, simplicité, clarté, magnétisme. Une forme
    compliquée ou confuse n'a pas d'appeal, même bien rendue.

### C. Chercher dans la nature et chez les maîtres du verre [D30]
- **Prendre une structure, pas un décor.** Lalique tirait la **structure** de ses flacons de la
  nature (fougère, libellule, scarabée, serpent) : la forme entière vient de l'analogie.
- **Analogies fertiles pour une fiole** : goutte, bourgeon, graine, coquillage, larme de
  verre, fleur fermée, cœur, flamme, fiole d'alchimiste, flacon de parfum.
- **Deux sources au moins** (0-P-C) : une forme naturelle donne la silhouette, un objet fabriqué
  donne les jonctions (bague, lèvre, pied).

### D. La méthode de design (étapes Essais et Design des pièces)
1. **Silhouettes, beaucoup** : au moins **6** silhouettes pleines, dans au moins **3 familles**
   d'analogie différentes (ex. goutte, bourgeon, coquillage), à une taille où l'on peut
   designer : **au moins la moitié de la taille finale** (16 à 20 px de haut pour une toile de
   40), jamais 10 px.
2. **Critique écrite** de chaque silhouette avec la grille E. On garde les **2 meilleures**.
3. **Design des pièces** sur la meilleure : **3 bouchons, 3 jonctions (épaule, bague, lèvre),
   3 pieds**, dessinés côte à côte à la taille finale, au calque de construction. Chaque
   variante passe la grille ; on écrit le choix.
4. **Assembler** la silhouette finale à la taille finale, puis le test de la silhouette
   générique (B-10) et le miroir.
5. **Seulement ensuite**, construction en volumes, trait, lumière, matière.

### E. La grille de critique (1 à 5 par critère)
| Critère | Question |
|---|---|
| **Lisibilité** | À ×1, en noir, sait-on ce que c'est en une seconde ? |
| **Originalité** | Se distingue-t-elle de trois potions génériques ? |
| **Appeal** | Est-elle charmante, simple, claire, a-t-on envie de la regarder ? |
| **Cohérence** | Un langage dominant, un motif répété à trois échelles ? |
| **Rythme** | Proportions franches, jonctions dessinées, contour long-court-long ? |
| **Crédibilité** | Tient-elle debout, se bouche-t-elle, se tient-elle en main ? |

Une silhouette sous **20/30** ne passe pas à la suite. On écrit la note et la raison au carnet
(rubrique *Critique*).

## 0-AB. Le sketching d'un illustrateur, calque par calque [D31][D32][D1]

Un illustrateur ne pose pas son trait final d'un coup. Il passe par des esquisses de plus en
plus précises, chacune sur un **nouveau calque** au-dessus de la précédente, dont il **baisse
l'opacité** comme un papier calque. Le dessin se juge **à la fin du sketching**, quand le trait
est propre et poli, **avant** la couleur : si la forme n'est pas belle à ce moment-là, la suite
ne la sauvera pas (0-AA).

### A. Les étapes (dans Claude Pixel, chacune est une étape de la méthode)
| # | Étape | Calque | Ce qu'on fait | Ce qu'on ne fait pas |
|---|---|---|---|---|
| 1 | **Vignettes** | construction « vignettes » | beaucoup de silhouettes rapides, notées (0-AA-D) | aucun détail |
| 2 | **Design des pièces** | construction « pièces » | variantes du bouchon, des jonctions, du pied | aucun trait propre |
| 3 | **Rough** | construction « rough » (rouge) | à la taille finale : le geste (ligne de flux en S ou en C), les grandes masses, en traits longs et libres ; plusieurs passages superposés sont permis | pas de trait propre, pas de petit détail |
| 4 | **Construction** | construction « volumes » (bleu), rough à 30-40 % | axe, primitives entières dessinées à travers, ellipses, proportions mesurées | pas de détail |
| 5 | **Esquisse nettoyée** | construction « esquisse » (vert), dessous à 20-30 % | on **choisit** les traits qui comptent et on les **redessine** d'un geste sûr ; on corrige les proportions ; on intègre les pièces choisies ; on retourne la toile | pas de couleur ; on ne décalque pas en aveugle |
| 6 | **Trait final** | normal | le trait pixel-perfect qui suit l'esquisse nettoyée ; l'esquisse est un guide, pas un calque à copier : on la redessine en comprenant la structure | pas de couleur |
| 7 | **Polish du trait** | normal | courbes régulières (A5-6, A8), jonctions nettes, poids du trait (contour extérieur plus fort, traits intérieurs plus légers ou cassés), petits détails de forme (lèvre, bague, facettes) | pas de couleur |
| 8 | **Validation du dessin** | — | planche du trait : ×1, ×2, retourné, silhouette ; grille 0-AA-E sur 30 (22 au moins) ; comparaison avec l'œuvre visée ; **on s'arrête pour montrer le dessin à l'humain** | rien d'autre tant que le dessin n'est pas validé |

### B. Les gestes du sketching
- **Du grand au petit** : la masse entière d'abord, puis les pièces, puis les détails. On ne
  finit jamais une zone avant d'avoir posé tout l'objet.
- **Traits longs et décidés** dans le rough : un trait d'épaule à hanche (ou de bouchon à pied)
  plutôt que dix petits ; le geste se prépare avant (*ghosting*, A11-A).
- **Redessiner plutôt que gommer** : un trait faux se refait au-dessus, sur un nouveau calque
  si besoin. Les pros repassent leurs traits plusieurs fois avant qu'ils soient beaux.
- **Baisser l'opacité du calque du dessous** (20 à 40 %) avant chaque nouvelle passe : on voit
  le guide sans le confondre avec le trait en cours.
- **Une couleur par calque d'esquisse** (rouge, bleu, vert) : on sait toujours quelle passe on
  regarde.
- **Retourner la toile souvent** (bouton « Retourner » de l'onglet Lumière, section Sur la
  toile) : une erreur de pente ou de proportion saute aux yeux quand l'image est retournée.
- **Ne pas décalquer en aveugle** : redessiner à partir de l'esquisse oblige à comprendre la
  structure. Le dessin final peut s'écarter beaucoup du premier rough : c'est normal.
- **Choisir les traits qui comptent** : à petite taille, chaque trait coûte des pixels. Ce qui
  peut se dire par une valeur (une face, un pli) n'a pas besoin de trait (B6-C).
- **Poids du trait** : contour extérieur plus fort, détails intérieurs plus fins ou plus clairs.
  En pixels : contour plein et sombre, traits intérieurs d'un ton plus clair ou interrompus
  (0-H).

### C. Ce qui se juge à la validation
- La **silhouette** est-elle belle en noir et unique (0-AA-B) ?
- Les **proportions** sont-elles franches, les **jonctions** dessinées, le **motif** répété ?
- Le **trait** est-il régulier (aucun L, aucun jaggy), avec le bon poids ?
- **Retournée**, l'image tient-elle encore ?
- La note de la grille est-elle d'au moins **22/30** ? Sinon, on revient au rough ou à
  l'esquisse, pas au trait.

## 0-AC. Le sketch fini de pro : ce que le trait seul doit déjà montrer [D33][D34][T18]

**Le critère de validation :** sans couleur ni lumière, le trait seul doit ressembler à un
**sketch fini de professionnel**. Si on le montre tel quel, on doit croire à une planche de
concept art ou de design d'objet, pas à un brouillon.

### A. Contre-exemple : la fiole-bourgeon (séance `fiole-bourgeon`, 23/30) [T18]
- **L'idée ne se lit pas en silhouette** : en noir, c'est une carafe ronde sur un pied ; le
  calice n'est qu'un trait clair posé sur le verre.
- **Les sépales sont un motif imprimé**, pas une pièce de métal qui enlace la panse.
- **Le haut est maigre** : col long et fin, petit bouton, on lit une bougie sur une boule.
- **Tout est symétrique et figé.**
- **Le pied est deux barres empilées.**
- **33×48 est trop petit** pour qu'un trait ait trois poids, des lignes de forme et des
  recouvrements.

### B. Les huit critères du sketch fini
1. **L'idée se lit en silhouette noire.** Ce qui fait l'objet (le calice, les pétales, la
   vrille) change le contour : pointes, creux, vides, recouvrements. Un détail intérieur ne
   porte jamais l'idée seul.
2. **Trois poids de trait, appliqués partout** :
   - **fort** (2 px, ou 1 px du ton le plus sombre) : la silhouette, les contacts (là où une
     pièce touche une autre ou le sol), le côté ombre ;
   - **moyen** (1 px sombre) : les arêtes visibles à l'intérieur de la silhouette ;
   - **fin** (1 px d'un ton plus clair, ou interrompu) : les détails, les lignes de forme, les
     nervures.
   Un poids appliqué par endroits seulement donne un dessin déséquilibré.
3. **Des recouvrements nets** : la pièce de devant coupe le contour de celle de derrière ; au
   croisement, le trait de devant est continu et un peu plus fort (0-B-6, 0-T).
4. **Des lignes de forme** : quelques traits fins qui courent **sur** la surface (nervure d'un
   sépale, couture d'un pétale, bague, contour croisé) disent le volume sans ombre.
5. **Une hiérarchie des détails** : les détails se groupent au point d'intérêt (bouchon, col)
   et à une seconde zone ; la grande panse reste calme (0-O).
6. **Des formes secondaires et tertiaires dessinées** : grand, moyen, petit (0-AA-B), avec des
   vides intéressants entre les pièces.
7. **Du mouvement** : une ligne de flux et une asymétrie voulue (une feuille d'un seul côté,
   une pointe qui penche), sauf si l'objet doit être solennel.
8. **Des traits décidés et propres** : courbes régulières, jonctions fermées, aucun trait
   parasite, aucun pixel qui hésite.

### C. La taille du dessin
Un sketch fini a besoin de place pour ses trois poids de trait, ses lignes de forme et ses
recouvrements. Pour juger un design d'objet, dessiner à **64 px de haut au moins** (96 pour un
objet riche). Une icône plus petite se redessine ensuite **à sa taille**, à partir du sketch
validé, comme une déclinaison (B4b) : on ne réduit jamais une image.

### D. Contrôle à la validation (étape « Validation du dessin »)
- Silhouette noire : l'idée se lit-elle sans aucun trait intérieur ?
- Les trois poids sont-ils là, partout, et cohérents ?
- Chaque recouvrement est-il net ?
- Les lignes de forme disent-elles le volume ?
- Montré tel quel, passerait-il pour une planche de concept art ?

---

# Partie A — Règles communes

## A1. Règles de travail

- **R1. Une étape = une image regardée.** Chaque étape produit `etape_XX_nom.png`. On
  la regarde **à ×1 et agrandie** avant de passer à la suite. Ce qui ne se lit pas à ×1
  n'existe pas.
- **R2. Du grand au petit.** Construction, puis silhouette, couleur, lumière, et les détails
  en dernier. Un détail ne corrige jamais une erreur de construction : on revient à
  l'étape fautive.
- **R3. Décider avant de tracer.** Volumes, articulations et formes d'ombre sont écrits en
  données (coordonnées, tailles), ou posés pixel par pixel. Un script peut **remplir** une
  forme décidée. Il ne **décide** jamais de la forme : pas d'ombre calculée par formule,
  ni de dégradé automatique [T1].
- **R4. Un calque par concept.** Construction dans des couleurs vives (rouge pour la pose ou
  les axes, bleu pour les repères, vert pour les volumes), qui n'apparaissent jamais dans
  l'image finale. Le contour final se pose ensuite en ton sombre.
- **R5. Corriger en boucle.** À chaque étape, noter au moins un défaut, le corriger,
  revérifier.
- **R6. Penser en rapports.** On écrit « le col = 1/3 de la largeur du ventre », pas
  « 4 px » au hasard. Les pixels se calculent à partir des rapports.
- **R7. Deux variantes.** Pour la forme principale (pose, visage, silhouette d'un objet),
  faire au moins 2 essais et garder le meilleur.
- **R8. Peu de traits.** Une ligne par direction : on commence en « I » (droite), on
  arrondit en « C », on finit par quelques « S ».
- **R9. Format imposé ou libre.** Si une taille est imposée (16, 32, 64…), suivre la table
  A3. Sinon, choisir un grand canevas (128 à 256 px pour un personnage) et dessiner comme
  un illustrateur : le pixel est l'outil, pas une excuse pour simplifier.

## A2. Lisibilité [R]

- **La silhouette d'abord.** Un objet ou un personnage doit être reconnaissable **en noir
  plein**. Si la silhouette ne dit pas ce que c'est, aucune couleur ne le sauvera.
- **La valeur fait le travail, pas la teinte.** En niveaux de gris, chaque matière ou
  pièce doit avoir sa propre valeur. Deux matières voisines de même valeur se fondent
  [T3 : le fer et le bois du coffre].
- **3 valeurs avant les nuances.** Poser seulement sombre, moyen et clair, et vérifier à ×1
  que le volume se lit déjà.
- **Budget de contraste.** Le plus fort contraste et le plus de détails vont au **point
  d'intérêt** (visage, mains ; garde d'une épée, gemme, serrure). Le reste est plus calme.
  Partout pareil = rien ne ressort.
- **Une seule couleur saturée (l'accent).** Les autres couleurs sont plus douces.
- **Pas de détail d'1 px isolé** à petite taille : il devient du bruit. Mieux vaut une forme
  de 2 à 3 px qu'un trait fin.
- **Formes intérieures par la valeur.** À petite taille, les formes intérieures se marquent
  par un changement de ton, pas par un trait de contour qui casserait la silhouette.
- **Tester en situation.** Sur fond clair **et** sur fond sombre, et dans le contexte du jeu
  (case d'inventaire, tuile de sol, à côté d'autres sprites).

## A3. Table par taille [R]

| | 16×16 | 32×32 | 64×64 | 128 px et plus |
|---|---|---|---|---|
| Tons par matière | 2 à 3 | 3 à 4 | 4 à 5 | 5 et plus |
| Couleurs au total | ≤ 8 | ≤ 16 | ≤ 24 | libre |
| Contour | 1 px, un ou deux tons sombres | 1 px, selout | 1 px, selout, contour cassé | 1 à 2 px, épaisseur variable |
| Anticrénelage (AA) | non | rare, à l'intérieur | sur les grandes courbes | oui, à la main |
| Texture | non | 1 ou 2 touches | par groupes de 2 ou 3 | oui |
| Décalage de teinte | faible : la valeur suffit | moyen | fort | fort |
| Idée de détail | 1 seule | 1 ou 2 | 3 ou 4, hiérarchisées | libre |

- **Petit format :** chaque pixel est une décision. On exagère la partie qui fait
  reconnaître l'objet et on supprime le reste.
- **Grand format :** on garde toutes les règles du dessin. Les clusters deviennent des
  coups de pinceau : chaque amas de couleur décrit un plan (facette, pli, reflet).

## A4. Règles implicites du dessin [Z][M][I]

- **Dessiner à travers les volumes.** Tracer aussi les parties cachées (l'arrière d'une
  sphère, le bras derrière le torse), puis effacer. Les raccords tombent juste.
- **Une ligne de centre par masse.** Elle tourne avec la masse et dit son orientation.
  Les lignes de construction dépassent un peu de la forme.
- **Asymétrie plutôt que symétrie.** La symétrie stricte est réservée à un visage de face
  ou à un objet manufacturé vu de face (et même là, la lumière la casse).
- **Cohérence.** Une fois un choix fait (volume, lumière, style de contour), on l'applique
  partout.
- **Les détails suivent la surface.** Plis, bandes, motifs, joints suivent la courbure du
  volume, grâce au maillage : un motif plat posé sur un cylindre détruit le volume.
- **Peu de détails dans la lumière.** Texture et détails vont dans les tons moyens et près
  du terminateur.
- **Les accents les plus sombres vont dans les creux** (dessous, aisselle, intérieur des
  cheveux, trou de serrure), jamais sur ce qui est devant.
- **Chevauchement net.** Une forme devant une autre coupe son contour. Pas de raccord en
  « T » lisse, et pas de tangentes (deux contours qui se touchent juste).

## A4b. Simplifier les formes [R][P]

Simplifier, c'est **enlever et exagérer** : on retire ce qui ne se lit pas, et on grossit ce
qui fait reconnaître le sujet.

- **Enveloppe d'abord.** Une grande forme simple autour de tout le sujet (cercle, boîte,
  triangle, goutte). Elle donne les proportions et la silhouette avant le moindre détail.
- **Grand, moyen, petit.** Une forme domine (environ 70 % de l'image), une forme moyenne
  l'accompagne, et une petite zone porte le détail. Deux formes de même taille se battent.
  Exemples : le chapeau, le pied et l'anneau d'un champignon ; un grand cristal, un moyen
  et un petit, chacun avec un angle différent.
- **Langage de formes.** Rond = doux, gentil. Carré = solide, lourd. Triangle = rapide,
  dangereux. La forme dominante donne le caractère.
- **Sous-formes dans le même sens.** Une masse se découpe en sous-formes (langues d'une
  flamme, mèches, feuilles, plumes) qui suivent **un même mouvement**. Leur taille varie,
  pas leur direction générale.
- **Le plus petit détail nécessaire fixe la taille.** Se demander quel est le plus petit
  élément indispensable (les yeux, une serrure, une graine) et combien de pixels il lui
  faut. Choisir la taille à partir de là. Dans le doute, plus petit. Grossir la taille ne
  dispense pas de simplifier : on ne fait que repousser le problème.
- **Ce que chaque taille peut porter :**

| Taille | Ce qui tient |
|---|---|
| 8 px | la silhouette et 2 ou 3 masses de couleur, rien d'autre |
| 16 px | la catégorie (oiseau ou chat) et **un** détail d'identité |
| 32 px | une expression, l'équipement, 1 ou 2 détails |
| 48 à 64 px | la texture, plusieurs éléments, des détails hiérarchisés |

- **Redessiner à chaque taille, jamais réduire.** Une réduction garde des détails qui n'ont
  plus la place de se lire. On repart de la silhouette à la nouvelle taille.
- **Marqueurs d'identité.** Choisir 2 ou 3 marqueurs (une couleur, une forme forte, un
  accessoire) et les garder **à toutes les tailles**, quitte à les agrandir quand le reste
  rétrécit. Le reste disparaît avant eux.
- **Formes difficiles en marches nettes.** Une bosse molle ou une longue pente qui donne des
  escaliers irréguliers se redessine avec des cassures à 90° et 45°. Un arc fin et presque
  horizontal disparaît à petite taille : on l'épaissit ou on le supprime.
- **Chaque pixel fait double travail.** À petite taille, un pixel est une tache de peinture :
  il peut être à la fois contour, ombre et forme. Les formes deviennent des symboles (un œil
  = 1 px, une graine = 2 px).
- **Formes qui riment.** Les variantes d'un même objet ou d'un même set reprennent les mêmes
  formes (même courbe de chapeau, même angle de garde) : différentes, mais de la même
  famille.
- **Vide utile.** Les espaces vides (entre les cristaux, sous l'arche, entre les langues de
  feu) ont eux-mêmes une forme claire. Un vide informe est une erreur de silhouette.

## A5. Pipeline pixel (pour objets et personnages)

### 5. Silhouette
- Remplir toute la forme d'une seule couleur sombre et la regarder à ×1.
- Lisible ? Reconnaissable ? Les espaces vides (entre bras et torse, entre lame et garde)
  ont-ils une forme claire ?
- Si non, on revient à la construction.

### 6. Contour (lignes « pixel-perfect »)
- **1 px d'épaisseur.** Les segments se touchent seulement en diagonale : pas d'angle en
  « L », pas de pixel doublé.
- **Courbes :** la longueur des segments change régulièrement (5-3-2-1-1, jamais
  5-2-1-2-1). Les plus longs vont en haut, en bas et sur les côtés de la courbe.
- **Diagonales :** segments égaux, ou motif régulier (2-1-2-1). Une diagonale 1:1 (pixel par
  pixel) est la plus nette.
- **Symétrie :** un objet symétrique a une **largeur impaire** s'il a un élément central
  (serrure, gemme, lame) : il lui faut une colonne de centre. Vérifier pixel par pixel
  que les deux côtés sont le miroir l'un de l'autre [T3].
- **Selout [R] :** le contour prend un ton plus sombre et plus saturé de la couleur qu'il
  entoure. Il est plus clair du côté de la lumière et plus sombre du côté de l'ombre.
  L'effet compte surtout dès 32 px.
- **Hiérarchie :** le contour extérieur est le plus sombre. Les lignes intérieures entre
  grandes masses sont en ton moyen-sombre. Les détails (plis, joints, coutures) sont juste
  un cran plus sombres que leur fond, et souvent **cassés** (interrompus).
- Pas de contour au contact du sol ni entre une main et l'objet tenu.
- Contour cassé et irrégulier pour la fourrure, les cheveux, l'herbe.
- **Ordre selon la forme [P] :** objet dur ou taillé (cristal, arme, meuble) : trait propre
  d'abord, puis couleur. Forme molle ou organique (cheveux, flamme, feuillage) : masse de
  couleur d'abord, sous-formes, puis contour posé **à la fin** autour de la forme trouvée.
- **Épaisseur de trait [P] :** le trait le plus épais va en haut et à l'extérieur (paupière
  du haut, dessus d'un chapeau). Les traits du bas et de l'intérieur sont plus fins ou
  cassés.
- **Lignes secondaires en couleur [P] :** pli de paupière, bas de l'œil, joints fins : un ton
  coloré plus clair que le contour, jamais la couleur du contour.
- **Couleur du contour :** le ton le plus sombre du set, chaud ou froid, mais pas le noir
  pur. Le même pour tous les objets d'un set (le brun-bordeaux d'une carotte, d'un pain et
  d'un bol).

### 7. Palette et couleurs à plat
- **Palette d'abord :** poser les couleurs en carrés côte à côte et les ajuster avant de
  colorer.
- **Une rampe par matière**, triée par valeur (nombre de tons : table A3).
- **Décalage de teinte :**
  - lumière : plus claire, un peu moins saturée, la teinte tire vers le jaune ;
  - ombre : plus sombre, **plus saturée**, la teinte tire vers le rouge (couleurs chaudes)
    ou vers le bleu et le violet (couleurs froides) ;
  - jamais de noir ni de blanc purs pour ombrer ou éclairer, sauf l'éclat d'une surface
    brillante, qui peut être presque blanc.
- **Harmonie :** couleurs analogues (douces), complémentaires (une domine, l'autre est
  l'accent), ou triade. Chaudes = vitalité, froides = calme ou mystère.
- **Réutiliser** les tons d'une rampe dans une autre (l'ombre de l'or peut être le brun du
  bois) : la palette reste courte et cohérente.
- **Palette en chaîne [P] :** les rampes se relient en une seule suite de teintes voisines
  (bleu → cyan → vert pâle → crème → rose → rouge → violet → sombre). Chaque couleur sert
  à plusieurs endroits (le cyan du blanc de l'œil, le crème du reflet de l'iris).
- Remplir chaque zone avec le ton moyen, des grandes zones vers les petites.
- **Contrôle en gris :** chaque matière a sa valeur (A2).

### 8. Lumière et ombres (placées à la main)
- **Une seule source**, choisie à l'étape 0. Par défaut, en haut à gauche, devant.
- **Tracer d'abord le terminateur** (la limite lumière / ombre) sur chaque volume. Il suit
  le maillage. C'est une limite nette, qu'on valide avant de remplir.
- **Interdit : l'ombrage « coussin »** (des bandes sombres tout autour du bord). L'ombre se
  met du côté opposé à la lumière.
- **Les zones, avec une rampe de 5 tons (1 = le plus sombre) :**

| Zone | Où | Ton |
|---|---|---|
| Éclat | 1 à 3 px, surfaces brillantes seulement | 5 |
| Lumière directe | face tournée vers la source | 4 |
| Ton de base | demi-lumière | 3 |
| Ombre forte | bande étroite le long du terminateur, côté ombre | 1–2 |
| Ombre moyenne | le gros de l'ombre | 2 |
| Lumière réfléchie | fine bande au bord de l'ombre, côté sol | 2–3 |
| Ombre portée | sur le sol ou sur une autre pièce | 1–2 |
| Occlusion | creux où la lumière n'entre pas | 1 |

- **Ordre de pose :** ombre en aplat, ombre forte au terminateur, occlusion dans les creux,
  lumière, éclat.
- **Contraste :** tout ton de la zone éclairée est plus clair que tout ton de la zone
  d'ombre.
- **Nette ou douce :** les volumes anguleux (boîte, facette, pli marqué) ont une limite
  nette, en une marche. Les volumes ronds ont une limite adoucie par 1 ton
  intermédiaire, mais pas de dégradé large.
- **Interdit : le banding.** Deux limites de tons qui suivent le même escalier, ou des
  segments de même longueur, parallèles et alignés (même sans se toucher), font apparaître
  la grille. Décaler les limites et varier les longueurs.
- **Ombre portée au sol :** plus sombre au centre, plus claire vers l'extérieur. Pour une
  icône d'inventaire, elle est facultative.
- **Un ton par face [P] :** sur un volume à faces planes (bloc, cristal, arche), chaque face
  a **un seul ton** selon son orientation : dessus = le plus clair, face tournée vers la
  lumière = clair, face avant = moyen, dessous et intérieur = sombre.
- **Creux inversés [P] :** dans un creux (alvéole de gaufre, trou, intérieur d'une arche),
  l'ombre est sur la paroi **du côté de la lumière** et la paroi opposée est éclairée.
  C'est l'inverse d'une bosse.
- **Ombre d'un surplomb :** ce qui avance projette une ombre sur ce qui est dessous. La
  paupière assombrit le haut de l'iris et du blanc de l'œil ; la frange, le haut du front ;
  le chapeau, le haut du pied.
- **Deuxième lumière (contre-jour) [P], facultative :** une lumière plus faible, d'une
  teinte contrastée (souvent froide : violet, bleu), arrive de l'arrière. Elle pose une
  bande de 1 px sur les bords **opposés** à la lumière principale, jamais sur tout le
  contour. Elle détache le sujet du fond.
- **Objet qui émet de la lumière [P] (feu, magie, lampe) :** on ombre à l'envers. Le cœur
  est le plus clair (presque blanc), entouré de couches de plus en plus sombres ; les
  bords et les pointes sont les plus sombres. Le cœur est décalé vers la source (la base
  d'une flamme). Pas de contour sombre autour.

### 8b. Matières [R][T3]

| Matière | Contraste | Éclat | Règle clé |
|---|---|---|---|
| Métal poli (lame, armure) | très fort | net, 1 à 2 px, presque blanc | bandes de reflet nettes qui suivent la forme ; l'ombre reprend la couleur de l'environnement (ciel bleuté en haut, sol chaud en bas) ; on peut passer du sombre au très clair sans transition |
| Métal mat (fer forgé) | moyen | petits points (rivets) | bord éclairé clair, bord opposé sombre, pour un ruban un peu bombé |
| Or | fort | blanc chaud | rampe brun → orange → jaune → crème ; l'ombre tire vers le brun-rouge, jamais vers le gris |
| Gemme taillée | très fort | 2×2 px presque blanc, plus 1 px en face | facettes à limites nettes ; la facette **opposée** à la lumière est souvent claire (la lumière traverse) ; couleurs très saturées |
| Verre | faible sur le verre lui-même | 2×2 presque blanc + 1 px en face | on voit à travers : le contenu ou le fond reste visible ; un reflet en arc suit la forme ; le rebord (lèvre) en **tons de verre**, jamais une barre noire [T9] |
| Liquide | moyen | à la surface | surface = **lentille fine** de 2 px, plus claire, effilée aux bords (elle donne le volume) ; une surface trop large ou trop claire lit comme du lait ; point lumineux au fond, du côté opposé à la lumière (la lumière traverse) [T9] |
| Bois | moyen | aucun | fibres et joints dans le sens du bois, par groupes de 2 ou 3 ; chanfrein clair sous chaque joint |
| Cuir | moyen | faible, large | coutures en pointillés réguliers ; bords usés plus clairs |
| Tissu | doux | aucun | plis depuis les points de tension ; limites douces |
| Peau | doux | très faible | ombre rouge-violet ou brun-rose ; jamais de tramage |
| Pierre | moyen | aucun | facettes, fissures cassées, tramage possible comme texture |
| Pierre taillée (blocs, arche) | moyen | aucun | un ton par face ; joints **perpendiculaires** au bord (rayons sur un arc) ; mousse sur le dessus et dans les fentes |
| Cristal | très fort | 1 à 2 px blancs sur les arêtes et les pointes | prismes à pointe ; un ton par facette ; contour coloré (rouge sombre pour un cristal rouge) ; contre-jour froid possible |
| Feu, magie | — | le cœur entier | ombrage inversé (8) ; langues dans le même sens ; étincelles détachées |
| Nourriture cuite (pain, gaufre) | moyen | petits points sur les bosses | rampe chaude crème → orange → brun ; dessus brillant, côtés plus sombres ; motifs (graines, alvéoles) qui suivent la surface |
| Organique (champignon, plante) | moyen | doux, large | volumes ronds ; petites taches ou nervures qui suivent le maillage ; lumière réfléchie colorée dessous |

### 8c. Variation de couleur (après les valeurs) [P]
Une fois les valeurs justes, on varie les **teintes sans changer les valeurs** (contrôle en
gris : l'image ne doit pas bouger) :
- ombres vers le violet ou le bleu, lumières vers le jaune (rappel de l'étape 7) ;
- le long d'une forme longue, la teinte glisse : cheveux chauds en haut, rosés aux pointes ;
  flamme orange au centre, magenta aux bords, cœur blanc-cyan ;
- 1 ou 2 facettes d'une autre teinte sur un cristal ou une gemme.

### 9. Détails (en dernier)
- **Règle du tiers :** la texture et les détails couvrent environ 1/3 de la surface. Les
  2/3 restants sont calmes : l'œil complète.
- **Par 2 ou 3 :** un détail se répète en petits groupes (rivets, plis, mèches, fibres),
  jamais sur toute la surface. Varier la taille, l'inclinaison et l'espacement.
- **Raconter :** un ou deux détails qui disent quelque chose (une entaille, une étiquette,
  une usure).
- Finir par quelques accents du ton le plus sombre, seulement dans les creux.
- **Les motifs suivent la forme [P] :** joints en rayons sur un arc, stries courbes sur un
  cylindre (carotte), grille raccourcie par la perspective (gaufre), graines orientées
  selon la surface (pain).
- **La nature décide où vont les détails [P] :** mousse et poussière sur les dessus et dans
  les fentes ; herbe qui cache la base et ancre l'objet au sol ; usure sur les arêtes.
- **Particules [P] (étincelles, vapeur, éclats) :** 1 ou 2 px, par groupes de 2 ou 3,
  détachées de l'objet, de plus en plus petites en s'éloignant. Elles restent rares.
- **Éclats aux arêtes :** sur une surface taillée, l'éclat va là où deux faces se
  rencontrent et sur les pointes.

### 10. Nettoyage
- **Orphelins :** un pixel seul d'une couleur. Le garder seulement s'il est voulu (éclat,
  rivet). Sinon, le supprimer ou le grouper en amas de 2 à 3 px.
- **Anticrénelage (AA) [R] :**
  - d'abord se demander s'il est nécessaire, souvent non. Pas d'AA sous 32 px ;
  - la valeur du pixel d'AA dépend de la part du pixel que la ligne couvrirait : beaucoup
    couvert → proche du trait, peu couvert → proche du fond ;
  - pas de moyenne des deux couleurs (boue) : prendre un ton de la palette de valeur proche ;
  - plus le segment est long, plus la rangée d'AA est longue ;
  - l'AA reste **à l'intérieur** du contour extérieur, car le fond du jeu change ;
  - jamais d'AA automatique sur chaque angle.
- Supprimer tous les pixels de construction.
- Chaque pixel doit mériter sa place.

### 11. Contrôle final (obligatoire)
Produire une planche avec l'image à ×1, ×2 et agrandie, sur fond clair et sur fond sombre,
retournée en miroir, en silhouette noire, en niveaux de gris, et **en situation** (case
d'inventaire, tuile, à côté d'un autre sprite du même jeu).

Questions communes :
1. La silhouette se reconnaît-elle seule ?
2. Les matières se séparent-elles en gris ?
3. Le volume se lit-il, et la lumière vient-elle d'une seule source ?
4. Le point d'intérêt a-t-il le plus fort contraste ?
5. Reste-t-il des orphelins, du banding, de l'ombrage coussin, des « L » dans le contour ?
6. Y a-t-il une forme dominante, une moyenne et une petite (A4b) ? Les marqueurs d'identité
   se voient-ils à ×1 ?
7. L'objectif de l'étape 0 est-il atteint ?

Puis les questions propres à l'objet (B5) ou au personnage (C8).

**Bilan :** 3 points réussis, 3 points à améliorer. Les 3 points à améliorer deviennent les
objectifs du dessin suivant.

---

## A6. Finition pro [R][T14]
Ce qui sépare un sprite « correct » d'un sprite « pro ». Les bases sont dans A5 (contour 6,
palette 7, lumière 8, nettoyage 10) ; A6 ajoute les chiffres et les tests pour décider vite.
À relire au moment des couleurs, puis au contrôle final.

### A. Construire une rampe
1. Choisir le **ton moyen** d'abord : c'est le plus saturé de la rampe.
2. Vers l'ombre : chaque marche **baisse la luminosité**, **monte un peu la saturation** et
   **tourne la teinte vers le froid** (bleu, violet). Vers la lumière : la luminosité monte,
   la saturation **baisse**, la teinte tourne vers le **chaud** (jaune, orange).
3. Écart de teinte : **10 à 20° par marche** au plus. Une rampe dont la teinte ne bouge pas
   donne des ombres boueuses ; désaturer seul donne du gris sale.
4. **Ni 0 %, ni 100 %** de luminosité ou de saturation, sauf exprès (pupille, éclat de
   métal). Saturation forte + luminosité forte = couleur qui « crie ».
5. **Marches plus courtes près du blanc** : l'œil distingue moins les clairs.
6. **En gris, les marches sont égales** : aucun saut plus grand que les autres.
7. **Rampes partagées** : l'ombre de la peau peut être le ton moyen des cheveux, l'ombre du
   tissu rouge un violet déjà dans la palette. Le trait le plus sombre est le bas de la
   rampe la plus sombre (ici `O #2a1a2e`, un violet).
8. **Repère chiffré** [R] : environ **+5 % de saturation pour −10 % de luminosité** en
   descendant la rampe. Une palette de départ peut tourner la teinte d'environ 45° d'une
   rampe à l'autre (Slynyrd) pour couvrir le cercle sans doublon.
9. **Pas de glissement par habitude** : le glissement de teinte sert la lumière de la scène
   (soleil chaud → ombres froides). Sous une lumière froide, c'est l'inverse. On décide le
   sens, on ne l'applique pas par réflexe.
10. **En cas de doute, ombrer en gris** : poser les valeurs en gris, les valider, puis
    remplacer chaque gris par la couleur de même valeur.

### B. Budget de couleurs
- Nombre de tons par matière et de couleurs au total : **table A3**.
- **Test « une couleur de moins »** : retirer la couleur la moins utile et la remplacer par
  sa voisine. Si on ne voit pas la différence à ×1, elle reste retirée.
- **Petites pièces** (œil, bouton, boucle) : on les sépare par la **valeur**. **Grandes
  pièces** (cape, cheveux, corps) : on les module par la **teinte**.
- Deux couleurs de même valeur et de teinte voisine se lisent comme une seule : les
  fusionner, ou écarter franchement leur valeur.

### C. Contour : selout et couleur
- **Selout** : le contour prend le ton le plus sombre de la matière qu'il borde. Côté
  lumière, il s'éclaircit ou s'ouvre sur 1 à 3 px ; côté ombre, il reste au plus sombre.
- Le contour est **plus sombre que l'objet et que le fond** : il augmente le contraste,
  jamais il ne le réduit. Le contraste trait/remplissage reste à peu près constant.
- **Tout ou rien** : soit tout le sprite a un contour (même sélectif), soit aucun.
- **Lignes intérieures** : un ton plus sombre que la matière = séparation discrète ;
  beaucoup plus sombre = séparation forte. Une ligne entre deux pièces prend la couleur de
  la pièce la plus proche de l'œil (ou de la plus sombre, à l'ombre). Un pli léger : pas de
  ligne, ou le ton sombre de la matière, jamais `O`.
- **Fin de ligne** : une ligne intérieure **s'éteint** (dernier pixel un ton plus clair) au
  lieu de s'arrêter net ; trop fine, elle se coupe côté lumière.
- Un contour peut **entrer de 1 à 2 px** dans le sprite pour suggérer une séparation (bras
  devant le torse) sans tracer toute la ligne.
- **Fond sombre** : un trait foncé franc ; si le style impose un trait noir, mettre la
  couleur dans les lignes intérieures.

### D. Courbes et silhouette
- Rappel des marches : A5-6 (5-3-2-1-1, jamais 5-2-1-2-1 ; diagonale = segments égaux).
- **Ajouter un pixel** au bout d'une forme la rend pointue ; **en retirer un** l'arrondit.
  C'est le moyen le plus rapide de corriger une silhouette.
- **Pas de saillie d'1 px isolée** sur la silhouette (sauf pointe voulue) : une forme qui
  dépasse fait au moins 2 px.
- **Jaggy voulu** : une marche cassée exprès peut séparer deux mèches ou deux pièces. Elle
  reste seule et lisible, sinon c'est un défaut (H).

### E. Lumière qui fait « fini »
- **Terminateur net** : la limite lumière/ombre est franche (1 ton intermédiaire au plus).
  Un dégradé lent sur tout le volume donne une forme molle.
- **Reflet principal** : un seul petit cluster, sur le point le plus proche de la lumière.
- **Occlusion (AO)** : le ton le plus sombre seulement dans les creux et les contacts (sous
  le menton, aisselle, sous la ceinture, plis profonds, pieds au sol).
- **Lumière réfléchie colorée** : l'ombre prend un peu la teinte du sol ou de l'objet voisin
  (herbe → ombre un peu verte), jamais aussi claire que la lumière directe. Une ombre grise
  neutre fait « naïf ».
- **Ombre de bord** : le ton le plus sombre sur 1 px du bord opposé à la lumière arrondit
  le volume. Un seul côté, sinon c'est du coussin.
- **Contre-jour** (A5-8) : liseré clair d'1 px, avec parcimonie, pour une ambiance (feu,
  magie, nuit) ou un fond sombre.
- **Éclats en dernier**, seulement sur les matières brillantes (cheveux, cuir verni, métal,
  yeux). Matière mate (laine, peau) : pas d'éclat blanc.
- **Point d'intérêt** : la couleur la plus saturée et le plus fort contraste vont au visage
  (ou à l'élément clé). Le reste est un cran plus calme.

### F. Anticrénelage (AA)
Règles de base : A5-10. En plus :
- **Où** : seulement là où une courbe fait un escalier trop dur à ×1 (joue, épaule ronde,
  bord de cape). Jamais sur une droite, ni sur une pente régulière à 45° ou 2:1.
- **Longueur** : elle suit la marche (marche de 4 px → AA de 2 px ; de 2 px → 1 px), dans le
  sens de la pente.
- Trop d'AA rend flou : à ×1, le contour reste net.
- **Seulement sur des marches de 2 px ou plus** [R] : une marche d'1 px n'a pas besoin d'AA.
  Le nombre de pixels d'AA dépend de la longueur de la marche et des tons disponibles.
- **Dans les coins des marches, espacés** : un pixel d'AA par coin, jamais une rangée
  continue le long du bord (ce serait du banding).
- **Test de l'enlèvement** : retirer chaque pixel d'AA un par un. Si le bord n'est pas pire
  à ×1, il reste retiré.
- **Pas d'AA vers l'extérieur** quand le fond change (sprite de jeu) : l'AA mélange avec un
  fond qu'on ne connaît pas.
- **Tous les styles n'en veulent pas** : un style très graphique, à contour noir franc, peut
  s'en passer complètement.

### G. Penser en volumes
- Avant l'ombrage, réduire chaque pièce à un **volume simple** (boule, cylindre, boîte) et
  ombrer ce volume. Un ombrage qui suit le contour au lieu du volume aplatit.
- Un design « carton » (raide, symétrique, de face) se corrige par une **ligne d'action**,
  une asymétrie (mèche, accessoire) et l'**exagération** du trait de caractère.

### H. Les défauts à traquer (sept de base + quatre de Silber)
| Défaut | Ce que c'est | Correction |
|---|---|---|
| **Doubles (« L »)** | coin en L dans une ligne d'1 px : 3 pixels là où 2 suffisent | enlever le pixel du coin |
| **Jaggies** | escalier irrégulier : 3-1-2-1-3 au lieu d'une progression | marches régulières (2-2-2) ou qui changent doucement (3-2-1) |
| **Banding** | bandes de tons qui suivent le même bord avec les mêmes marches : on voit des lignes, pas une forme | décaler les marches, varier les longueurs, fondre une bande dans l'autre |
| **Ombrage coussin** | ombre tout autour, clair au centre : pas de source de lumière | une seule direction : le côté haut-gauche reste clair jusqu'au bord |
| **Orphelins** | pixel isolé sans voisin de même couleur | le supprimer, ou l'accrocher à un cluster |
| **Bruit** | trop de clusters de 1-2 px : texture qui grésille | regrouper en grandes taches ; un détail = un cluster lisible |
| **Dithering décoratif** | damier pour « faire un dégradé » sur un petit sprite | réservé aux textures (mailles, pierre, fourrure) ou aux grands aplats ; zéro par défaut sur un sprite de jeu (A7) |
| **Super pixels** [B2] | blocs de 2×2 ou 3×3 d'une même couleur : le dessin a été fait petit puis agrandi | redessiner à la taille finale, 1 pixel = 1 décision |
| **Ombrage « flash »** [B2] | lumière de face : centre clair, aucun côté d'ombre franc, volume écrasé | lumière haut-gauche, terminateur net (E) |
| **Trop de complexité** [B2] | trop de pièces, de couleurs et de détails pour la taille | test « une couleur de moins », enlever un détail sur deux (A4b) |
| **Pas de texture** [B2] | grands aplats lisses sur des matières qui en ont (pierre, bois) | 1 à 3 clusters de texture dans les tons moyens (A5-8b, A3) |

### I. Ordre de travail d'un pro
Aplats → valeurs vérifiées en gris → ombre propre (une direction) → AO dans les creux →
lumière et reflets → lumière réfléchie → contour sélectif → AA → nettoyage (H) → planche.
On ne passe pas à la suite tant que l'étape ne se lit pas à ×1.

### J. Contrôle et tests du pro (sur la planche A5-11)
| Test | Comment | Ce qu'on doit voir |
|---|---|---|
| **Plisser les yeux** | planche à ×1, yeux plissés | quelques grandes taches claires et sombres, pas de grésillement |
| **Gris** | colonne grise | chaque matière a sa valeur ; le point d'intérêt a le plus fort contraste |
| **Silhouette** | colonne noire | pose et coiffure se reconnaissent sans couleur |
| **Taille réelle** | ×1 sur fond clair et sombre | aucun détail ne devient bruit ; le contour tient sur les deux fonds |
| **Miroir** | colonne miroir | aucune pente ni proportion fausse ne saute aux yeux |
| **Teinte** | rampes côte à côte | les ombres virent au froid, les lumières au chaud |
| **Défauts** | agrandi ×4 | aucun des sept défauts (H) ; AA seulement sur les courbes dures ; contour cohérent |
| **Une couleur de moins** | retirer une couleur | si rien ne change, elle reste retirée |
| **En situation** | sprite sur le décor du jeu | il se détache du fond sans liseré forcé |

---

## A7. Tramage (dithering) [B1][B2][R]
Le tramage mélange deux tons voisins par un motif de pixels pour simuler un ton qui manque.
C'est un outil de **décor et de texture**, pas un raccourci d'ombrage. Sur un sprite de jeu,
la règle par défaut reste celle de A6-H : zéro tramage.

### A. Quand tramer (les trois conditions, toutes à la fois)
1. **Le ton intermédiaire manque** dans la palette, et l'ajouter coûterait trop (budget A6-B,
   contrainte de palette, 16 couleurs GBA).
2. **La surface est grande** : au moins 6 à 8 px de transition dans le sens du dégradé.
   Sur une zone plus petite, le motif se lit comme du bruit, pas comme un mélange.
3. **La matière l'accepte** : ciel, brume, pierre, sable, terre, tissu épais, fourrure à la
   limite d'ombre, métal rouillé. Jamais sur la peau, un visage ni un œil.

Si une condition manque, **ajouter un ton à la rampe** ou **marquer la limite par une marche
nette** (A6-E, terminateur net).

### B. Les motifs
| Motif | Couverture | Usage |
|---|---|---|
| Damier | 50 % | le mélange standard, au milieu d'une transition |
| Clairsemé | 25 % / 75 % | entrées et sorties de transition (1 pixel sur 4, puis 3 sur 4) |
| Bayer 4×4 (ordonné) | 0 à 100 % par seizièmes | longs dégradés : ciel, eau profonde, halo |
| Lignes (1 sur 2) | 50 % orienté | surface qui a un sens : bois, tissu rayé, pluie, scanlines |
| Tramage de texture | irrégulier, en petits clusters | pierre, sable, terre : un motif qui sert la matière |

- **Rampe de densité** : un dégradé tramé passe par 0 → 25 → 50 → 75 → 100 %. Un damier
  à 50 % partout ne fait qu'**un** ton de plus, pas un dégradé.
- **Seulement entre voisins** : on trame entre deux tons qui se suivent dans la rampe. Entre
  deux tons éloignés (clair et sombre), le damier grésille.
- **Le cœur reste plein** : on trame la **limite** entre deux tons sur 2 à 4 px. L'intérieur
  de chaque ton reste un aplat. Tout tramer donne une image agitée.
- **Un seul style par image** : ordonné **ou** texture, pas les deux mélangés sur une même
  scène.

### C. Défauts propres au tramage [B1]
- **Banding de tramage** : le motif forme des bandes droites et parallèles au bord. Décaler
  la limite, la faire suivre la forme du volume (courbe, pas règle).
- **Damier « posé »** : un rectangle de damier sans entrée ni sortie. Ajouter les zones à 25
  et 75 %, ou casser le bord du motif.
- **Tramage en mouvement** : sur un objet qui bouge ou défile, le damier scintille. Réservé
  aux plans fixes ou lents (fond, ciel), ou alors on aligne le motif sur la grille du monde.

### D. Contrôle
- **À ×1** : si on voit le damier, c'est du bruit. Si on voit un ton intermédiaire, c'est
  réussi.
- **Plisser les yeux** (A6-J) : le dégradé doit sembler continu.
- **Test « un ton de plus »** : remplacer le tramage par un aplat du ton manquant. Si c'est
  aussi beau et que le budget le permet, garder l'aplat.

## A8. Lignes et formes : ce qu'ajoutent les livres [B1][B3]
Complète A5-6 (contour) et A6-D (courbes).
- **Penser la ligne comme un vecteur** [B1] : avant de poser les pixels, se représenter la
  courbe lisse qu'on veut obtenir, puis choisir les marches qui la suivent. Le pixel suit
  l'intention, pas l'inverse.
- **Pentes propres à connaître par cœur** : 1:1 (45°), 2:1 (≈ 26,5°), 3:1, 1:2, 1:3. Ce
  sont les seules droites sans jaggies. Toute autre pente se rapproche de l'une d'elles ou
  alterne deux pentes voisines de façon régulière (2-1-2-1, jamais 2-1-1-3).
- **Une courbe = des marches qui changent dans un seul sens** jusqu'au sommet, puis dans
  l'autre (5-3-2-1-1, puis 1-1-2-3-5). Un retour en arrière fait une bosse.
- **Pixel « doublé » d'épaisseur** : un trait doit garder la même épaisseur visuelle tout du
  long. Un endroit plus épais attire l'œil comme un défaut, sauf s'il est voulu (A5-6,
  épaisseur de trait).
- **Formes avant lignes** [B3] : sculpter d'abord la masse en aplats (comme une pâte), puis
  la border. Le contour posé trop tôt fige une forme encore fausse.
- **Sous-pixel sur les formes fixes** [B1] : un ton intermédiaire d'1 px peut décaler
  visuellement un bord de moins d'un pixel (un œil qui regarde un peu à droite, une bouche
  qui sourit à peine). Même logique qu'en animation (E2-D), mais sur une image fixe.

## A9. Perspectives de jeu [B1][R]
B0b donne la projection d'**un objet**. A9 fixe celle de **tout le jeu**, à décider avant le
premier sprite, car elle commande le nombre de dessins.

| Vue | Ce qu'on voit | Lignes | Travail par personnage | Pour |
|---|---|---|---|---|
| **De profil** (side view) | une seule face | horizontales et verticales | 1 direction, retournée en miroir | plateforme, combat, runner |
| **Dessus 3/4** (type RPG) | le dessus et la face avant | horizontales et verticales ; les murs montrent leur face | 3 directions (face, dos, profil) + miroir | RPG, aventure, Pokémon-like |
| **Dessus strict** | seulement le dessus | grille | 1 sprite qu'on fait tourner | shoot, véhicules |
| **Isométrique** | dessus + deux faces | **2:1** (2 px en x pour 1 en y), jamais 30° vrais | 2 diagonales (face, dos) + miroir si symétrique | tactique, gestion, construction |

- **Une seule vue par jeu.** Personnages, décors, objets et icônes du monde partagent la même
  projection. Seules l'interface et les icônes d'inventaire peuvent avoir la leur.
- **Isométrique : 2:1 partout.** Les bords parallèles au sol suivent la ligne 2-2-2. Les
  verticales restent verticales. Un objet iso se construit à partir d'une boîte 2:1.
- **3/4 du dessus : les pieds sur une même rangée** (C10-G), l'ombre au sol pour poser le
  personnage, les murs du haut cachent un peu le personnage, ceux du bas jamais.
- **Hauteur ambiguë** (iso, 3/4) : une ombre portée sous tout ce qui saute ou vole, sinon on
  ne sait plus si l'objet est en l'air ou loin derrière.
- **Compter le travail avant de choisir** : une vue 3/4 avec 4 directions × marche ×
  attaque multiplie les images. Un jeu de profil est le choix le plus économe.
- **Isométrique en pratique** [R] : garder un **calque règle** avec une seule ligne 2:1
  propre (2-2-2) et copier ses marches au lieu de les recompter. Hauteurs et décalages en
  **multiples de 4 px** : les boîtes s'emboîtent sans demi-marche. Les pentes 1:1 vont
  avec les 2:1 (toits, rampes) ; aucune autre pente sur un même objet.

## A10. Leçons des maîtres [B6][R]
Ce que des artistes reconnus disent de leur façon de travailler, réduit à ce qui change un
dessin. Chaque leçon renvoie à la section où elle s'applique. Les noms servent à retrouver
la source, pas à imiter un style.

### A. Kazuko Shibuya (sprites des *Final Fantasy* des années 1980-1990)
- **Peu d'idées fortes.** À 16 ou 24 px de haut, un personnage tient sur 2 ou 3 traits
  d'identité : la coiffure (souvent le premier), une couleur dominante, un accessoire. Le
  reste se simplifie (A4b, C10-I).
- **Grosse tête, cheveux expressifs** : la tête fait près de la moitié du sprite ; la
  coiffure porte la personnalité, le visage reste minimal.
- **Plus grand = plus réaliste** : un monstre plusieurs fois plus grand que les héros a
  droit à plus de rendu et d'anatomie. Le niveau de détail suit la taille, pas l'importance
  (A3).
- **Dessiner pour l'écran d'arrivée.** Un écran à tube adoucissait les pixels ; un écran
  plat les montre tous. On vérifie donc chaque pixel à ×1 sur l'écran réel (A5-11).
- **Retenue en reprise** : quand on refait un sprite, on garde ce qui marchait et on
  n'ajoute pas de détail pour « moderniser ». Une limite (16 couleurs, une taille fixe) aide
  à décider.

### B. Mark Ferrari (fonds de *Loom*, *Monkey Island*, travaux de cycle de couleurs)
- **Le tramage se pose à la main, pixel par pixel**, pour suggérer une matière (brume,
  pierre, feuillage). Le motif automatique est l'exception (A7).
- **Plus la palette est grande, plus le fondu est doux** : avec peu de couleurs, on choisit
  la marche nette plutôt que de forcer un tramage.
- **Cycle de couleurs** : un fond peut s'animer (eau, cascade, feu, lumière qui tourne) en
  faisant tourner quelques couleurs de la palette, sans redessiner une image (E7, F3).

### C. Paul Robertson (animation : *Scott Pilgrim*, *Mercenary Kings*)
- **Apprendre en regardant** : des jeux d'arcade classiques et des films d'animation
  entiers, image par image. C'est la copie d'étude appliquée au mouvement (G2).
- **Garder les clés, tordre les intervalles** : les images de départ et d'arrivée restent
  propres ; seules les images du milieu s'étirent, se déforment ou se multiplient (smear,
  E2-C).
- **Des outils simples bien maîtrisés** valent mieux que des outils nouveaux : la vitesse
  vient de la répétition des mêmes gestes (A11).

### D. Henk Nieborg (*Lomax*, *Flink*, *Battle Axe*)
- **D'abord la résolution, puis les couleurs, puis les pixels** : la taille de l'écran et la
  palette sont fixées avant le premier trait, puis il pixelise directement à la taille
  finale, sans filtre ni réduction (A4b, F4).
- **La profondeur vient des plans** : plusieurs couches de parallaxe, chacune avec sa
  valeur et sa saturation (F3).
- **Textures par familles** : cratères, écorce, roche se construisent avec un petit
  vocabulaire de clusters répétés et variés, pas avec du bruit (A5-8b).

### E. Artistes d'aujourd'hui
- **Waneella** (scènes de ville animées) : grandes formes de base d'abord, détails ensuite,
  beaucoup de changements en chemin. Les scènes vivent par de petites boucles (lumières,
  passants, fumée) sur un fond fixe (F5, E2-I).
- **Toyoi Yuuta** (illustrations animées) : quelques éléments qui bougent sur une image
  fixe suffisent à faire vivre une illustration.
- **Raymond Schlitter (Slynyrd, *Pixelblog*)** : une palette se construit en rampes dont la
  teinte tourne régulièrement (A6-A) ; on ombre en gris d'abord si on hésite sur les
  valeurs.
- **Pedro Medeiros (saint11, *Celeste*)** : l'AA ne se pose que sur des marches de 2 px ou
  plus ; sa longueur dépend de la marche et des couleurs disponibles (A6-F).
- **Pixel Parmesan, Tiny Warrior Games** : chaque pixel d'AA doit survivre au test « je
  l'enlève, est-ce pire ? » ; l'AA automatique crée flou et banding.

### F. Ce qui revient chez tous
1. **La valeur avant la teinte** : une image juste en gris est presque finie ; une teinte ne
   rattrape jamais une valeur fausse.
2. **Les grandes masses avant les détails** : plan des valeurs (clair, moyen, sombre) en
   grandes formes, puis seulement les petites.
3. **Moins de clusters, plus gros** : le moins de clusters possible, pas de cluster d'un
   pixel sans rôle.
4. **Des transitions franches** : le pixel art préfère le passage net lumière/ombre au
   dégradé lent (A6-E).
5. **Regarder souvent autrement** : ×1, miroir, gris, yeux plissés, et une pause avant la
   finition (A11-C).

## A11. Le geste du pro : outils et souris [R]
Un pro ne dessine pas plus vite parce qu'il bouge plus vite, mais parce que chaque geste
est décidé avant d'être fait. Ces règles valent pour un humain à la souris et pour Claude,
qui dessine avec la souris virtuelle (`souris/`).

### A. Avant le geste
- **Savoir où va le trait** : point de départ, point d'arrivée, marches de la pente
  (A5-6). Si on ne peut pas le dire, on n'est pas prêt à tracer.
- **Le bon outil pour la forme** : une droite ou une pente régulière → l'outil ligne (ou
  clic, puis Maj + clic) ; une courbe → une suite de segments aux marches prévues (5-3-2-1) ;
  un aplat → rectangle ou pot ; quelques pixels isolés → des clics. Jamais de tracé à main
  levée pour une droite.
- **Crayon pixel-perfect** pour les traits à main levée : il retire les doubles des coins.

### B. Pendant le geste
- **Un trait = un geste continu**, sans hésitation au milieu. Un trait raté s'annule
  (Ctrl+Z) et se refait ; on ne le « rattrape » pas par-dessus.
- **Lent dans les virages, vif dans les droites** : la précision compte aux changements de
  marche et au point d'arrivée.
- **Pipette plutôt que palette** : on reprend la couleur sur le dessin (Alt + clic), ce qui
  garde les rampes cohérentes.
- **Zoom fixe pendant un passage**, aperçu ×1 toujours visible à côté.

### C. Entre deux gestes : regarder autrement
| Quand | Test | Pourquoi |
|---|---|---|
| après chaque trait | aperçu ×1 | ce qui ne se lit pas à ×1 n'existe pas (R1) |
| après la silhouette, puis après la lumière | **miroir** | l'œil s'habitue aux erreurs ; retourné, un côté penché ou une proportion fausse saute aux yeux |
| après les aplats, puis après la lumière | **gris** | les matières se séparent par la valeur ; une teinte ne corrige pas une valeur |
| avant la finition | **yeux plissés** | seules les grandes masses restent : on voit si le volume tient |
| avant la finition | **palette seule** | la palette se juge à part du dessin : rampes régulières, pas de doublon de valeur |
| avant la planche | **pause** | un regard reposé voit ce que l'œil habitué ne voit plus |

### D. Rythme d'un pro
- **Du grand au petit à chaque passage** : masses, puis pièces, puis pixels. On ne descend
  au pixel qu'une fois la masse juste.
- **Peu de gestes, tous utiles** : un pixel posé puis effacé trois fois est un pixel mal
  décidé. Mieux vaut regarder une seconde de plus.
- **Les mêmes gestes, toujours** : raccourcis appris, outils au même endroit. La vitesse
  vient de la répétition (A10-C).

---

# Partie B — Objets

## B0. Intention
Écrire en 3 à 5 lignes :
- **ce que c'est et à quoi ça sert** dans le jeu : icône d'inventaire, objet posé au sol,
  élément d'interface ;
- la **taille** (celle de la tuile ou de la case) et le nombre de couleurs (table A3) ;
- la **projection**, la même pour tout le set (tableau B0b) ;
- la lumière : en haut à gauche, comme les autres objets du jeu ;
- la matière principale et **l'accent** (la seule couleur saturée).

## B0b. Projection [P]

| Projection | On voit | Usage |
|---|---|---|
| De face (jeu de plateforme) | la face avant seule | icônes, jeux de côté |
| Vue de dessus « 3/4 » | le dessus **et** la face avant, pas les côtés | RPG vus de dessus, comme les jeux Pokémon : bâtiments, objets posés |
| De dessus pur | le dessus seul | cartes, toits |
| Isométrique | le dessus et deux côtés | lignes en pente 2:1 (2 px de côté pour 1 de haut) |
| Dimétrique 45° | le dessus en losange et deux côtés | carte tournée de 45° |
| Oblique | la face avant et un côté fuyant | décor, effet de profondeur simple |

- Une seule projection par jeu. Un objet en 3/4 à côté d'un objet de face casse le monde.
- Pour ce hack (moteur GBA vu de dessus) : objets du monde en **vue 3/4 de dessus**,
  icônes d'inventaire de face ou légèrement inclinées, toutes de la même façon.

## B1. Cadre et placement
- Garder 1 px de marge. L'objet remplit la case : une case vide autour rend l'icône faible.
- **Objets longs** (épée, bâton, flèche) : sur la **diagonale** de la case, pointe en haut
  à droite. La diagonale 1:1 donne le contour le plus propre et la plus grande longueur.
- Centrer **visuellement** (le centre de masse), pas seulement le cadre englobant.
- Fixer les rapports clés en données : par exemple col = 1/3 du ventre, poignée = 1/4 de la
  longueur d'une épée.

## B2. Volumes
- Décomposer l'objet en **formes primitives** : sphère, cylindre, cône, boîte, disque.
- Tracer pour chaque volume : son axe, une ligne de maillage, et le **terminateur** pour la
  lumière choisie.
- Une boîte vue un peu d'en haut montre son dessus (plus clair) et sa face avant.
- Un objet plat (lame, bouclier) a quand même une épaisseur : un biseau ou un bord de 1 px
  qui accroche la lumière.
- **Extrusion [P] :** pour donner de l'épaisseur à une forme (arche, anneau, roue) : tracer
  la face, la **dupliquer et la décaler** dans la direction de la profondeur, tracer la
  forme intérieure, couper ce qui est caché, puis ajouter les bouts de face intérieure
  visibles. On colore ensuite face par face (8).
- **Couches empilées [P] (burger, gâteau, pile) :** toutes les couches ont la même
  inclinaison d'ellipse. Leurs valeurs alternent (clair, sombre, clair) pour qu'elles se
  séparent même en gris.

## B3. Forme iconique
- **Exagérer ce qui fait reconnaître l'objet :** la garde d'une épée, le bouchon d'une
  potion, le chapeau d'un champignon, la serrure d'un coffre. Simplifier le reste.
- Comparer avec 2 ou 3 icônes du même objet que l'on connaît : quelle partie la rend
  lisible ?
- Faire 2 silhouettes (R7) et garder la plus claire à ×1.

## B4. Matière et lumière
- Choisir la rampe de chaque matière (A5 étape 7) et sa règle (tableau 8b).
- Placer le **point d'intérêt** : c'est là que vont l'éclat et le plus fort contraste.

## B4b. Décliner un objet en plusieurs tailles [R][P]
Exemple : une carotte en 8, 16 et 32 px.
- **8 px :** silhouette, 2 tons, feuillage en un seul amas.
- **16 px :** un éclat, 1 ou 2 stries, contour sombre.
- **32 px :** stries courbes qui suivent le cylindre, 4 tons, éclat allongé, feuillage en
  2 ou 3 lobes.
- Même angle, même couleur de contour, mêmes marqueurs à toutes les tailles. Le nombre
  d'idées augmente avec la taille (A3), mais l'identité ne change pas.

## B5. Contrôle propre aux objets
- L'objet se reconnaît-il en 1 seconde dans une case d'inventaire ?
- Va-t-il avec les autres objets du set (même vue, même lumière, même épaisseur de
  contour, même densité de détail) ?
- Les éléments centraux sont-ils vraiment centrés (largeur impaire) ?
- Les matières se distinguent-elles en gris ?
- Sur fond **sombre**, le contour côté ombre se fond : contour cassé et liseré de lumière
  de rebond net de ce côté. Toujours tester fond clair **et** fond sombre [T9].

## B6. Recettes pas à pas des planches [P2]
Tirées de cinq planches de tutoriels fournies : pierre, cristal, slime et livre (style
Rappenem), et rochers (formes de base → déformer → détails → polir). Elles suivent toutes le
même ordre, en 6 à 9 étapes, **une idée par étape** (R1, R2).

### A. L'ordre commun des planches
| # | Étape | Ce qu'on fait | Ce qu'on ne fait pas encore |
|---|---|---|---|
| 1 | **Forme de base** | primitive propre (cube, prismes, dôme, boîte), trait sombre neutre | aucun détail |
| 2 | **Déformer / séparer** | casser les angles, arrondir, séparer les pièces (couverture et pages) | aucune couleur |
| 3 | **Nettoyer le trait, poser les aplats** | trait propre, un aplat par matière | aucune ombre |
| 4 | **Ombrage de base** | une lumière, un ton par face (A5-8), terminateur net | aucun reflet fin |
| 5 | **Ombres et lumières secondaires** | sous-plans dans chaque grande face, AO, lumière de rebond | — |
| 6 | **Éclats et contour coloré** | éclats sur les arêtes et les pointes ; le trait noir devient la couleur sombre de chaque matière (selout) | — |
| 7 | **Contre-jour** | 2ᵉ lumière, opposée, d'une autre teinte, sur les bords du côté opposé | — |
| 8 | **Variation de couleur** | les ombres glissent vers le froid (bleu, violet) ou vers une teinte voisine ; quelques taches de teinte dans les grandes faces | — |
| 9 | **Détails et nettoyage** | marques, usure, étincelles, halo, ombre portée, chasse aux défauts (A6-H) | — |

Ce que cet ordre apprend :
- **Le contour reste sombre et neutre jusqu'à l'étape 6.** On le colore une fois la lumière
  posée, car c'est la lumière qui dit quel bord s'éclaircit (selout, A6-C).
- **La teinte se travaille après les valeurs** (étape 8) : les volumes doivent déjà se lire en
  quasi-monochrome. C'est A5-8c, appliqué systématiquement.
- **Les détails de surface (fissures, trous, décor) viennent après l'ombrage de base** : ils
  s'éclairent selon la face où ils se trouvent.
- **La lumière est dessinée** sur la planche (un point et un cône). Faire de même : poser un
  repère de lumière sur le calque de construction (R4) et le garder visible jusqu'à la fin.
  Les planches l'éclairent en haut à droite, ta méthode en haut à gauche : le côté est un
  choix, l'important est **un seul côté dans tout le jeu** (règle 23).

### B. Primitive, puis déformer (rochers, pierre) [P2]
1. **Formes de base** : un ou plusieurs blocs simples (cubes, dalles, cylindres aplatis),
   déjà ombrés en 3 tons : dessus clair, face éclairée moyenne, face opposée sombre.
2. **Déformer** : retirer des pixels aux coins pour les arrondir, rendre les arêtes
   irrégulières, pencher un peu les faces. Le rocher garde **les mêmes trois faces** et la
   même lumière : seul le bord change.
3. **Détails** : découper les grandes faces en **sous-plans** (cassures, facettes, strates),
   chacun avec son ton selon son orientation.
4. **Polir** : trous, points clairs, fissures fines, contour coloré, AA sur les grandes courbes.

- **Rocher composé** : 2 ou 3 blocs de tailles **différentes** (grand, moyen, petit, A4b)
  qui se chevauchent et se calent l'un contre l'autre, jamais alignés ni de même taille.
- **Strates** (rocher en couches, galets empilés) : des disques de plus en plus petits vers le
  haut, chaque couche avec son dessus clair et sa tranche sombre.

### C. Pierre taillée en 9 étapes [P2]
- **Arêtes plus rudes (2)** : écorner les coins du cube de 1 à 2 px, creuser une entaille en
  « Y » sur une arête. Une pierre n'a pas d'angle parfait.
- **Effacer le trait des arêtes intérieures (4)** : une fois les faces ombrées, les lignes
  entre les faces disparaissent. **Les faces se séparent par la valeur**, seul le contour
  extérieur reste. Une ligne intérieure sur une pierre la fait paraître dessinée, pas
  sculptée.
- **Fissures et rayures (5)** : un trait sombre **plus une lèvre claire d'1 px** du côté
  opposé à la lumière (le bord qui reçoit la lumière). Une fissure part d'une arête ou d'un
  coin, se divise en « Y », change de largeur, et **passe par-dessus les arêtes** d'une face
  à l'autre. Jamais au milieu d'une face sans attache, jamais deux fissures parallèles.
- **Trous et cratères (6)** : creux inversés (A5-8) : sombre du côté de la lumière, lèvre
  claire du côté opposé. Par groupes de 2 ou 3 de **tailles différentes**, surtout sur les
  faces moyennes et sombres ; le dessus éclairé reste calme (A4, peu de détails dans la
  lumière).
- **Couleur (8)** : une pierre grise n'est jamais d'un gris neutre. Les ombres tirent vers le
  bleu-violet, la lumière reste à peine chaude.

### D. Cristal en 9 étapes [P2]
- **Esquisse (1)** : 3 à 5 prismes de tailles différentes, chacun penché d'un angle différent,
  qui partent d'une même base (A4b, grand-moyen-petit).
- **Facettes (3)** : tracer les arêtes de chaque prisme **avant** l'ombrage : face avant,
  côté, pointe. Chaque facette aura un seul ton (A5-8).
- **Ombrage (4-5)** : la facette tournée vers la lumière est la plus claire ; une arête
  claire le long de chaque crête ; les prismes de derrière sont plus sombres que ceux de
  devant.
- **Éclats (6)** : 1 à 2 px presque blancs aux pointes et sur les crêtes ; contour coloré
  (rouge très sombre pour un cristal rouge).
- **Contre-jour (7)** : une lumière rose ou violette en bas à l'opposé : un liseré sur les
  facettes de ce côté. Il fait sentir que la lumière traverse le cristal.
- **Variation (8)** : les ombres glissent vers le magenta et le violet.
- **Halo et étincelles (9)** : pour un cristal magique, un halo de la couleur de la lumière
  émise, 1 ou 2 tons à peine plus clairs que le fond, en paliers ou tramé (A7) ; et 2 ou 3
  étincelles en croix (4 branches d'1 px autour d'un centre clair), détachées du sujet.

### E. Slime (matière gélatineuse) en 6 étapes [P2]
- **Forme** : un dôme au bas aplati (posé au sol), les yeux en simples arcs sombres.
- **Ombres secondaires (3)** : des bandes courbes qui suivent le dôme, plus sombres vers le bas.
- **Éclats (4)** : un **grand reflet en forme** (un arc ou une tache allongée qui suit le
  dôme) côté lumière, plus 1 ou 2 petits points. Une matière gélatineuse brille comme du
  verre.
- **Translucidité (5)** : la lumière traverse : une zone **plus claire en bas, du côté opposé
  à la lumière**, plus une 2ᵉ lumière (cyan) sur le bord bas. Même règle que le liquide
  (A5-8b).
- **Finition (6)** : ombre portée en ellipse sous le slime, un peu décalée du côté opposé à la
  lumière ; elle le pose au sol.

### F. Livre (objet fabriqué) en 9 étapes [P2]
- **Séparer la couverture des pages (2)** : la couverture déborde d'1 px autour des pages et
  a 2 px d'épaisseur ; le dos est arrondi. C'est ce débord qui dit « livre » et pas « boîte ».
- **Tranche des pages** : des lignes alternées claires et sombres, parallèles au dos.
- **Décorer au trait, avant la couleur (4)** : coins de métal, fermoir, marque-page. Objet dur
  = trait d'abord (A5-6, ordre selon la forme).
- **Un élément qui dépasse** : le marque-page (ruban d'une autre couleur, saturée) sort de la
  silhouette ; il casse la boîte et porte l'accent (A2).
- **Matières contrastées** : cuir mat (pas d'éclat blanc) contre métal brillant (éclats nets) ;
  la différence de brillance sépare les pièces autant que la couleur.
- **Contour coloré et glissement de teinte (8)**, puis **détails (9)** : symbole gravé sur la
  couverture (sombre + lèvre claire, comme une fissure), usure claire aux coins.

### G. Contrôle propre aux recettes
- Chaque étape est-elle **lisible seule** à ×1, comme sur les planches ?
- Le trait intérieur des faces dures a-t-il disparu après l'ombrage (pierre, rocher) ?
- Chaque fissure ou gravure a-t-elle sa **lèvre claire** ?
- Le contre-jour est-il d'une **autre teinte** que la lumière principale, et seulement sur les
  bords opposés ?
- Les ombres ont-elles glissé vers le froid à l'étape 8, sans changer les valeurs ?

---

# Partie C — Personnages

Construction d'un personnage, puis pipeline A5. L'anatomie (C9) s'applique à **chaque**
étape, pas seulement aux détails.

## C0. Intention
- Qui est le personnage, son attitude, un mot clé d'émotion (« calme », « menaçant »).
- La vue (face, 3/4, profil), la taille, le nombre de couleurs.
- Le style : nombre de têtes de haut (2 à 3 pour un chibi, 4 à 5 en RPG, 6 à 8 en
  semi-réaliste), et le style du visage (manga, RPG simple, semi-réaliste).
- 2 à 3 références, avec pour chacune **ce qu'on lui prend**. On combine, on ne copie pas.
- Un objectif prioritaire (la pose, le visage, la lumière…).

## C1. Proportions
- Hauteur totale avec 1 à 2 px de marge. Tête H = hauteur ÷ nombre de têtes. Dessiner à
  côté une **colonne de têtes** et lire les repères dessus.

  | Repère | Canon 7 têtes | Canon 8 têtes |
  |---|---|---|
  | Menton | 1 | 1 |
  | Épaules | ≈ 1,3 | ≈ 1,3 |
  | Tétons, aisselles | ≈ 2 | 2 |
  | Bas de la cage, coudes | ≈ 2,6 à 3 | 3 (nombril) |
  | Entrejambe, poignets | ≈ 3,7 à 4 | 4 (moitié) |
  | Bout des doigts | ≈ 4,6 (mi-cuisse) | ≈ 4,8 à 5 |
  | Genoux | ≈ 5,2 | ≈ 5,8 à 6 |
  | Chevilles | ≈ 6,7 | ≈ 7,6 |
  | Plante des pieds | 7 | 8 |

- Le canon de 8 têtes allonge surtout les jambes.
- Valable pour tous les styles : le pubis est au milieu du corps ; coudes au bas de la
  cage ; poignets au pubis ; genoux au milieu des jambes.
- Chibi de 3 têtes : 1 tête, 1 torse, 1 jambe ; les bras ont la longueur du torse.
- Largeurs : épaules d'homme ≈ 2 à 2,3 H, de femme ≈ 1,8 à 2 H.
- **Contrôle :** les bras ne sont pas trop courts (erreur la plus fréquente) ; les espaces
  vides (bras / torse, entre les jambes) ont une forme plausible.

## C2. Pose : ligne d'action et squelette
- **Une seule courbe** pour la ligne d'action (en C ou en S), jamais droite.
- Le torse est un rectangle déformable : ligne des épaules en haut, ligne du bassin en bas.
  En mouvement, elles s'inclinent : un côté est étiré, l'autre pincé.
- Placer les articulations **en données**, puis les relier en fil de fer.
- **Contrapposto :** côté de la jambe d'appui, la hanche monte et l'épaule descend. La
  cheville d'appui est sous la base du cou (ligne de gravité).
- En 3/4, le côté éloigné est plus étroit.
- 2 variantes (R7), puis **exagérer** la meilleure : une pose fidèle mais molle est pire
  qu'une pose exagérée.
- **Contrôle :** la pose tient debout ; chaque articulation plie dans son sens (C9-A) ; pas
  de pieds joints au garde-à-vous sauf si l'intention le demande [T1] ; les deux côtés
  évitent la symétrie et les parallèles.

## C3. Volumes (le mannequin)
Ordre obligatoire :
1. tête (sphère + plan du visage) et ligne de centre ;
2. cage thoracique (œuf ou boîte) et bassin (bol ou boîte), qui tournent et s'inclinent
   séparément, chacun avec sa croix de centre ;
3. **cercles d'articulations** : épaules (qui débordent de la cage), coudes, poignets,
   hanches, genoux (rotule devant), chevilles ;
4. cylindres effilés entre les cercles (cuisse plus large que le mollet, bras plus large
   que l'avant-bras ; l'avant-bras est en forme de bouteille) ;
5. cou en cylindre, qui part de l'arrière du crâne et entre dans le torse vers l'avant ;
6. mains en blocs, pieds en cales (≈ 1 tête de long).

Puis :
- **maillage :** une ligne verticale et une horizontale sur chaque masse, comme une ficelle
  nouée autour ; elles guident les détails et les ombres ;
- **cube, sphère ou cylindre :** le cube donne de la solidité, la sphère de la douceur.
  C'est un choix de style, à garder cohérent ;
- **angle difficile :** dessiner d'abord une boîte en perspective, puis placer les volumes
  dedans.

**Main (dès qu'elle dépasse 6 px) :**
1. paume en trapèze, plus large aux jointures qu'au poignet ;
2. 4 jointures sur un **arc** (le majeur le plus haut) ;
3. doigts en 3 phalanges de plus en plus courtes ; majeur le plus long, puis annulaire et
   index, puis auriculaire ;
4. pouce qui part **du côté du poignet**, relié par une masse charnue ; 2 phalanges
   visibles ; son bout arrive vers la base de l'index ;
5. contour qui enveloppe les cercles, articulations un peu gonflées ;
6. trait plus marqué dans l'ombre et aux superpositions.

## C4. Tête et visage
**Forme :** femme = menton plus haut, mâchoire ronde, cou fin ; homme = mâchoire anguleuse,
cou presque aussi large que la mâchoire ; personne âgée = visage plus long. Vérifier la
longueur du cou : un cou nu trop long était le principal défaut du test 1.

**De face :**
1. cercle du crâne et ligne de centre jusqu'au menton ;
2. mâchoire : deux lignes presque verticales puis en angle ; menton en petit segment plat ;
3. lignes horizontales : yeux à mi-hauteur de la tête (un peu plus bas en manga), bas du
   nez au bas du cercle, bouche au tiers entre nez et menton ;
4. yeux en amandes séparés d'une largeur d'œil ; paupière du haut plus épaisse ;
5. nez ≈ écart entre les yeux ; coins de la bouche à l'aplomb des pupilles ;
6. oreilles de la ligne des sourcils au bas du nez ;
7. cou depuis l'intérieur de la mâchoire, avec le V des sterno-cléido-mastoïdiens.

**En 3/4 (Loomis) :** sphère, puis cercle aplati sur le côté (l'oreille juste derrière
et sous son centre) ; ligne de centre **courbe** ; plan du visage en bloc sous la sphère ;
mâchoire depuis l'arrière du cercle latéral ; le côté éloigné est raccourci (œil du fond
plus étroit).

**Guides obligatoires :** ligne de centre, ligne des yeux, ligne du nez, ligne de la
bouche. Sans elles, la symétrie dérive.

**Placement selon le style :**
- semi-réaliste : 3 tiers égaux (cheveux → sourcils → bas du nez → menton) ;
- manga : yeux sous le milieu de la tête, nez entre ce milieu et le menton, oreilles en
  « C » entre la ligne des yeux et celle du nez.

**Yeux :** femme ≈ 1/6 de la hauteur de la tête, homme ≈ 1/8 ; largeur ≈ 1/4. Iris ovale,
pupille ≈ 1/4 de l'iris, haut de l'iris plus sombre ; reflet au même endroit sur les deux
yeux.

**Expressions :**

| Émotion | Sourcils | Yeux | Bouche |
|---|---|---|---|
| Colère | vers le nez | — | — |
| Tristesse, peur | vers les oreilles | peur : petites pupilles | — |
| Détermination | baissés | mi-clos | — |
| Surprise | levés | grands ouverts | — |
| Calme | — | — | petite |

**En pixels :**
- tête de 6 px ou moins : 1 px sombre par œil, pas de nez ;
- tête de 7 à 12 px : yeux de 1×2 ou 2×2 px, nez en 1 px d'ombre ;
- au-delà : on applique les rapports ci-dessus ;
- détail par taille (yeux, expressions, format GBA) : **C10**.

**Œil en grand (dès 32 px de tête) [P], dans l'ordre :**
1. trait : paupière du haut épaisse (2 à 3 px) avec un cil qui part au coin extérieur ;
   pli de paupière séparé au-dessus ; paupière du bas fine et cassée ;
2. iris en aplat sombre ; blanc de l'œil **jamais blanc** : bleu clair ou gris, plus
   sombre sous la paupière ;
3. iris sombre en haut (ombre de la paupière), clair en bas, avec un fin arc lumineux en
   bas (la lumière traverse) ;
4. pupille, puis reflet de 1 à 2 px presque blanc, du côté de la lumière ;
5. paupière du haut doublée à l'intérieur d'un ton coloré (son ombre sur l'œil) ;
6. pli et paupière du bas éclaircis en ton de peau rosé (lignes secondaires en couleur) ;
7. une touche de couleur froide en haut de l'iris pour la profondeur.

**Attrait [T1] :** le visage est **majoritairement dans la lumière**. Pas de visage coupé en
deux moitiés claire et sombre (effet masque), sauf intention dramatique.

## C5. Vêtements et design
> Rendu détaillé (plis, matières, motifs, recettes par vêtement) : **C17**.

- Les vêtements épousent les volumes, puis s'en écartent selon le tissu. Les plis partent
  des points de tension (épaules, coudes, taille, genoux).
- **Langage de formes :** voir A4b (rond = doux, carré = solide, triangle = dangereux).
  Une forme dominante par personnage.
- **Hiérarchie :** primaires (torse, jupe, cape, masse de cheveux), puis secondaires
  (manches, ceinture, col), puis tertiaires (boutons, bijoux). Varier les tailles, garder
  des zones calmes.

## C6. Cheveux [M][C][R][T13][T14]

### A. Construction
- Dessiner d'abord **la tête chauve**, puis une enveloppe de volume un peu plus grande que
  le crâne. Des cheveux tirés ou attachés épousent le crâne, à 1 ou 2 px.
- **Ligne des cheveux en premier.** Chez un adulte : cheveux → haut des yeux = yeux → nez.
  Un enfant a un front plus grand ; trop haute, la ligne fait paraître le front dégarni.
  Formes : arrondie, en M, plate. Une ligne qui recule part du M et finit en arc.
- **Point d'attache** (queue, chignon) : toutes les mèches tirées vont vers lui en suivant
  le crâne. Queue haute : l'attache se voit. Queue basse : les cheveux pendent vers elle.
  Couettes : derrière les oreilles, à la même hauteur, alignées avec les yeux.
- **Les cheveux ont du poids** : une mèche part du crâne, suit une courbe simple puis
  **pend à la verticale**. Cheveux longs : plus fins en haut, plus gonflés en bas ; ils
  suivent les épaules et la poitrine.
- La coiffure est le **premier signe d'identité** : sa silhouette doit différer de celle
  des autres personnages.

### B. Ordre de pose en pixels [P]
1. la masse entière en un aplat, comme un casque ;
2. la lumière sur la masse entière (arc de reflet qui suit le crâne, ombre sous la masse
   et à la raie) ;
3. découpage en 3 à 6 grandes touffes qui suivent toutes le même mouvement ;
4. contour autour des touffes, pointes ouvertes (E) ;
5. chaque touffe reçoit son clair et son sombre ;
6. variation de couleur (A5-8c) : chaud en haut, rosé ou violet vers les pointes et dans
   les ombres ;
7. l'arc de reflet se casse en tirets dans le sens des mèches ;
8. mèches libres et éclats en tout dernier.

### C. Touffes et mèches
- **Des touffes ou rubans, jamais des fils** : chaque touffe a son clair, son moyen et son
  sombre, avec 2 ou 3 lignes de mèche **continues** à l'intérieur (des pointillés = bruit).
- Une touffe qui coule fait **2 px de large** et s'affine vers une pointe de **1 px**.
- Regrouper le détail en **îlots** (front, raie, pointes) et laisser de grandes zones
  calmes. Aucun pixel orphelin.
- Courbes régulières : marches qui montent ou descendent (1-1-2-3, 3-2-1-1), jamais 1-3-1.
- **Pointe ou flick vers l'extérieur** : au moins **3 px de large à la base et 2 rangées**,
  sinon la règle de contour la rend tout trait (elle se lit comme une antenne). Elle finit
  sur 1 px de contour, pas sur un pixel de couleur isolé [T13][T14].
- **Frange** : profil dessiné à la main, une longueur par colonne, alternance longue /
  courte et une mèche centrale plus longue ou décalée. Mèches de côté : entre les yeux et
  les oreilles. Raie placée par rapport aux yeux.
- **Types** : pointes = les plus longues à l'arrière, hauteur en demi-cercle autour du
  crâne ; ondulé = des « S » autour d'une ligne verticale ; bouclé = demi-cercles plus
  petits vers les racines et les pointes ; spirale = cône qui se vrille ; tresse =
  3 bandes, des « Y », puis arrondir.
- **Plaqués en arrière** : la coiffure vient des lignes de mèche tirées vers l'arrière et du
  reflet ; la masse reste collée au crâne (1 px au-dessus du trait) [T13].
- **Favoris** : au niveau des tempes ; ils descendent vers la joue **1 px en retrait du bord
  du visage**, sans toucher l'oreille [T13].
- **Ahoge** (mèche rebelle) : 2 à 3 rangées au-dessus du crâne, courbée, d'un seul côté.
  Un seul.
- **Mèches libres** en dernier, comme accents, d'un seul côté de préférence (deux ou trois
  en petit format). Les mèches avant longues s'arrêtent **avant les mains** et ne croisent
  pas le bras [T14].

### D. Lumière et couleur
- **Rampe : 3 valeurs d'une teinte + 1 reflet.** Un seul ton sans reflet = casque en
  plastique. Glissement de teinte discret : ombres plus froides, clairs plus chauds (roux →
  bordeaux à l'ombre, orange au clair ; blond → ocre et jaune pâle). Cheveux foncés : reflet
  bleu ou violet désaturé, pas gris.
- Clairs : surtout des ombres. Moyens : tons moyens et ombres franches. Foncés : masse
  sombre, reflet facultatif.
- **Une seule source**, en haut et de face, sur un côté. Grande ombre du côté opposé et sous
  la masse. Arrière du crâne, nuque et dessous de l'attache dans l'ombre.
- **Ombre portée sous la frange** sur le front, et sous chaque touffe qui en recouvre une
  autre : elle décolle les cheveux du visage et donne les couches. Peau plus sombre et plus
  chaude, jamais noire. Sur une frange en biais, la limiter au haut des creux et sous les
  pointes, sinon on voit des rayures [T14].
- **Un reflet par touffe éclairée**, pas un par mèche : les reflets séparent les touffes.
- **Interdits** : l'ombrage coussin (y compris un liseré clair qui fait le tour de la tête)
  et le banding (A6-H). Remède : resserrer l'écart de valeurs, poser la limite au
  terminateur, ou casser la bande en touffes.

### E. Contour
- **Selout** : sur le haut éclairé, le trait prend le bas de la rampe des cheveux ; en bas
  et côté ombre, trait foncé pour protéger la silhouette.
- Masque des cheveux posé à la main, puis **trait automatique seulement contre le vide ou
  les vêtements**, jamais contre la peau. La **ligne des cheveux sur le front** se marque
  par le contraste cheveux/peau : une longue bande sombre au front se lit comme des
  sourcils ou un bandeau [T13][T14].
- Une mèche de 2 ou 3 px posée sur la peau devient tout trait : la recolorer à la main
  (cœur moyen, clair côté lumière, sombre côté ombre) [T13].
- Un **jaggy voulu** peut séparer deux touffes du contour (A6-D).
- L'ombrage **ne remplace jamais** un pixel de contour : vérifier qu'aucun trou n'apparaît
  dans le trait après avoir ombré [T14].
- **Pas d'AA** sous ~48 px de haut ; au-delà, un seul pixel intermédiaire sur les courbes
  douces, jamais tout autour.

### F. Style anime (ombrage cel)
On exagère les formes, on réduit les tons, on soigne le contour.
- **2 tons + 1 ombre profonde + 1 reflet**, limites franches (pas d'AA, pas de dégradé).
  L'ombre est **plus saturée** que la base, pas seulement plus foncée.
- **Pointe d'une mèche** : ton moyen ou clair sur la pointe, ombre profonde sur la colonne
  voisine côté ombre. Une colonne entière d'ombre au bout d'une mèche se lit comme une
  rayure [T14].
- **Couronne de reflet (angel ring)** : arc clair qui suit l'arrondi du crâne au premier
  tiers de la hauteur, en dents de scie (petits triangles vers le bas, alignés sur les
  touffes). Toujours au même endroit d'une image d'animation à l'autre. Sous 48 px, 3 à
  5 pixels suffisent.
- **Éclats les plus clairs** (blanc chaud) en tout dernier : 1 ou 2 clusters, côté lumière.

### G. Leçons des tests 13 et 14 (toile 32×39)
- Coupe au carré « seau » (côtés droits, bas plat) : courber les côtés et faire dépasser
  des pointes avant plus claires sur des cheveux de derrière plus sombres.
- Pour remettre le visage sous la frange, ne recopier **que les pixels non vides** du corps
  de base, sinon on efface la mâchoire et les cheveux de derrière.

### H. Contrôle
Ligne des cheveux à la bonne hauteur ; mèches vers le point d'attache ; pointes d'au moins
2 rangées finies sur 1 px ; arc de reflet ; une seule lumière, sans coussin ni banding ;
pas de trait noir contre le front ; pointes visibles, pas cachées derrière un bras [T2].

## C7. Astuces de figure [R]
- Le geste d'abord, l'anatomie par-dessus : si les muscles cassent la ligne d'action, on
  redessine les muscles, pas la pose.
- Sur un membre, un côté plutôt droit et l'autre courbe, puis ça s'inverse. Deux côtés
  courbes = saucisse molle.
- Lignes de rythme qui se croisent : une courbe d'un côté se continue plus bas de l'autre
  côté.
- Un bras tendu n'est jamais parfaitement droit.
- Les petits traits d'ombre suivent le sens des fibres du muscle.
- À partir de 64 px de haut, ombrer par **plans musculaires** : chaque grand muscle est une
  facette, claire si tournée vers la lumière.

## C8. Contrôle propre aux personnages
1. La pose exprime-t-elle l'intention ? Les proportions suivent-elles la colonne de têtes ?
2. Le visage est-il attirant et majoritairement éclairé ? Se lit-il à ×1, comme les mains ?
3. Chaque articulation est-elle plausible ? Le deltoïde dépasse-t-il la cage (sauf en
   chibi, où il n'y a pas d'épaule marquée : règle 10) ? Le cou
   part-il de derrière la mâchoire ? Le pouce part-il du poignet ?
4. Peut-on nommer les muscles qui font le contour de chaque membre (C9-H) ? Reste-t-il un
   bras « tube » ou un torse « rectangle » ?
5. Les cheveux passent-ils le contrôle C6-H ?
6. À côté de la référence, le dessin tient-il la comparaison ?

## C9. Anatomie de référence [I]
Simplifier la **forme**, jamais l'anatomie : chaque muscle visible se voit (bosse, plan,
creux) ou pousse le contour ou le vêtement.

### A. Articulations

| Articulation | Type | Mouvement | Erreur interdite |
|---|---|---|---|
| Épaule | rotule | tous les sens ; bras levé au-dessus de l'horizontale = l'omoplate et la clavicule montent | bras levé avec l'épaule restée basse |
| Coude | charnière | plie seulement vers l'avant, ~145° | coude plié en arrière ou sur le côté |
| Avant-bras | rotation | c'est l'avant-bras qui tourne la paume, pas le coude | paume retournée sans torsion |
| Poignet | ellipsoïde | beaucoup vers l'avant, moins vers l'arrière, peu sur les côtés | main à 90° sur le côté |
| Hanche | rotule emboîtée | avant beaucoup, arrière ~20°, côté ~45° | jambe en arrière très haut sans bascule du bassin |
| Genou | charnière | plie seulement vers l'arrière ; la rotule reste devant | genou plié vers l'avant |
| Cheville | charnière | haut ~20°, bas ~45° | pied à angle droit en pointe |
| Cou | 7 vertèbres | tourne ~80° de chaque côté | tête tournée à 180° |
| Taille | colonne souple | la cage et le bassin bougent l'un par rapport à l'autre | torse d'un seul bloc dans une pose dynamique |

### B. Longueurs
- Un os ne change jamais de longueur : en raccourci il paraît plus court, mais ses deux
  articulations gardent leur distance en 3D.
- Bras : épaule → coude ≈ coude → poignet. Main ≈ longueur du visage.
- Jambe : hanche → genou ≈ genou → cheville. Pied ≈ 1 tête.
- Bras le long du corps : coude à la taille, poignet à l'entrejambe, doigts à mi-cuisse.

### C. Raccords
- **Épaule :** le deltoïde couvre la tête de l'humérus et dépasse la cage ; le pectoral
  passe dessous ; les trapèzes descendent en pente du cou à l'épaule.
- **Hanche :** la jambe s'attache sur le côté du bassin ; la cuisse part en diagonale vers
  l'intérieur du genou.
- **Cou :** il part de derrière la mâchoire et sous les oreilles ; la nuque commence plus
  haut que la gorge.
- **Coude, genou, poignet, cheville :** plus étroits et osseux ; les muscles gonflent
  au-dessus et en dessous.

### D. Rythme du contour
Les bosses d'un membre ne sont jamais face à face à la même hauteur :
- cuisse : bombée haut dehors, bas dedans (vaste interne en goutte au-dessus du genou) ;
- mollet : haut dehors, plus bas dedans ;
- bras : deltoïde en haut dehors ; triceps derrière, plus haut que le biceps devant ;
- avant-bras : large près du coude (le brachio-radial part du bras), fin au poignet.

### E. Torse
- Cage = œuf plus haut que large, avec l'arc costal en V renversé. Bassin = bol plus petit.
  Entre les deux, la taille, souple.
- Face : pectoraux, grand droit (6 à 8 blocs), obliques, dentelé. Dos : trapèze en losange,
  grand dorsal en V, fessiers.
- La poitrine est posée **sur** la cage et suit son maillage.

### F. Homme / femme

| | Homme | Femme |
|---|---|---|
| Épaules | ≈ 2 à 2,3 têtes | ≈ 1,8 à 2 têtes, plus tombantes |
| Taille | peu marquée | marquée (sablier) |
| Bassin | étroit, plus haut | plus large ; hanches ≈ épaules |
| Cuisses | droites | plus en diagonale vers les genoux |
| Cou | ≈ largeur de la mâchoire | fin |
| Avant-bras | épais | plus fins, tendons moins marqués [T2] |

### G. Poids
- La ligne de gravité tombe du creux du cou sur le pied d'appui.
- Côté qui porte : hanche haute, jambe tendue, cuisse contractée. Côté libre : genou fléchi.
- Un objet lourd tenu d'une main fait pencher le torse du côté opposé.

### H. Carte des muscles

| Zone | Muscles | Ce qu'ils font au dessin |
|---|---|---|
| Cou | sterno-cléido-mastoïdien, trapèze | V de derrière l'oreille au creux du cou ; pente cou → épaule |
| Épaule | deltoïde | bosse qui dépasse de la cage ; finit en pointe au tiers du bras |
| Poitrine | grand pectoral | éventail du sternum, entre sous le deltoïde |
| Dos | trapèze, grand dorsal, érecteurs | V du dos ; deux colonnes le long de la colonne |
| Flanc | dentelé, obliques | dents sous l'aisselle ; bourrelet au-dessus du bassin |
| Bras | biceps, triceps | biceps rond devant ; triceps en fer à cheval, plus long, derrière |
| Avant-bras | brachio-radial, fléchisseurs, extenseurs | bosse en haut et dehors ; tendons vers le poignet |
| Cuisse | quadriceps, couturier, adducteurs | couturier en diagonale ; vaste interne juste au-dessus du genou |
| Jambe | jumeaux, soléaire, tibia | mollet plus haut dedans ; tibia presque droit devant |
| Cheville | malléoles | interne haute, externe basse |

- Un muscle **contracté** est plus court et plus rond ; un muscle **étiré** est plus long et
  plus plat. Dans chaque pose, un côté est pincé et l'autre étiré.
- Les muscles s'emboîtent comme des coins, jamais posés côte à côte comme des saucisses.

## C10. Personnages en pixel art, taille par taille [R]
Plus le personnage est petit, plus on **exagère** la tête et les yeux et plus on
**supprime** (nez, bouche, doigts, cou). On choisit la taille d'après ce qu'il faut lire :
à 16 px, une direction et une coiffure ; à 32 px, une expression ; à 64 px, un visage.

### A. Table par hauteur du personnage

| Hauteur | Têtes | Tête / hauteur | Yeux | Nez, bouche | Bras, mains | Couleurs |
|---|---|---|---|---|---|---|
| 8 px | 1,5 | 60 à 70 % | 1 px chacun | aucun | aucun ou 1 px | 3 à 4 |
| 16 px | 1,7 à 2 | 50 à 60 % | 1×1 ou 1×2 | aucun | bras 1 px, main = 1 px de peau | 5 à 8 |
| 20 à 24 px | 1,7 à 2,2 | 45 à 60 % | 1×2 | bouche rare (1 px) | bras 1 à 2 px | 8 à 13 |
| 32 px | 2 à 2,5 | 40 à 50 % | 2×3 : reflet 1 px **en haut** [T5] | nez = 1 px d'ombre, bouche 1 à 2 px | main = bloc 2×2, pouce 1 px | 10 à 14 |
| 48 px | 2,5 à 3,3 | 30 à 40 % | 3×2 à 3×3 : paupière, iris, pupille, reflet | nez par l'ombre, bouche 2 à 3 px | moufle + pouce | 12 à 16 |
| 64 px | 3 à 4 | 25 à 33 % | 4×3 et plus, avec blanc de l'œil | nez en plan d'ombre, lèvre du bas par son ombre | doigts en 2 masses | 14 à 20 |
| 96 px et plus | 4 à 6 | 15 à 25 % | recette « œil en grand » (C4) | narine, lèvres | doigts séparés | 16 (portrait GBA) |

- Style « héroïque » : tête sous 35 % ; c'est alors une capuche, une cape ou une arme qui
  porte la silhouette.
- Les yeux 2×2 avec reflet n'apparaissent qu'au-dessus de 16×24 ; en dessous, un reflet
  blanc rend le regard fou.
- Le blanc de l'œil n'existe qu'à partir de 3 px de large.
- Une seule mesure, cheveux compris : nombre de têtes ≈ 1 / part de la tête. Les deux
  colonnes doivent toujours concorder (corrigé au test 5).

### B. Format Pokémon GBA (notre ROM)
- **Sprite de dresseur sur la carte :** cellule 16×32 ; le personnage occupe ≈ 14×20 px,
  pieds sur la dernière rangée, vide au-dessus. Tête ≈ 60 % de la hauteur (≈ 1,6 tête),
  yeux 1×2 sombres, **pas de bouche ni de nez**, 13 à 14 couleurs.
- **Palette :** 16 couleurs dont l'index 0 transparent → 15 utiles. Répartition type :
  contour 1, peau 3, cheveux 3, vêtement principal 3, vêtement secondaire 2 à 3, yeux et
  détail 1 à 2, blanc 1.
- **Portrait ou sprite de combat :** 5 tons de peau, 9 pour le reste ; contour = la couleur
  la plus sombre. Palette sûre : 3 couleurs × 3 tons ; un objet sombre prend 2 tons +
  contour, un objet clair jusqu'à 5 ; les cheveux peuvent prendre un 4e ton.

### C. Placer le visage aux petites tailles
1. **La frange fixe la ligne des yeux** : les yeux se collent sous les cheveux, sur la
   moitié basse de la tête. Yeux bas et écartés = jeune et mignon ; plus hauts et serrés =
   plus âgé ou plus dur.
2. **Écart :** à 16 px, 2 px de peau entre les yeux (1 px fait loucher, 3 px élargit la
   face). Sous les yeux, 1 à 2 rangées de peau, puis le menton.
3. **Pas de cou** sous 32 px : la tête repose sur les épaules.
4. **3/4 :** tout le visage glisse vers le côté regardé ; l'œil du fond fait 1 px de moins
   ou touche le bord du visage ; dès 32 px, le nez est 1 px qui dépasse du contour.
5. **Profil :** un seul œil, 1 px en retrait du bord du visage ; l'oreille en 1 à 2 px de
   peau plus sombre au milieu de la tête.
6. **Dos :** aucun trait, les cheveux couvrent la tête ; on garde la même hauteur de tête.

### D. Recettes d'yeux, pixel par pixel
- **1×1 :** le ton le plus sombre de la palette (pas forcément noir).
- **1×2 vertical (standard GBA) :** 2 px sombres ; variante : haut sombre, bas couleur de
  l'iris.
- **2×2 :** rangée du haut sombre (paupière) ; en bas, 1 px d'iris + 1 px de reflet clair
  du côté de la lumière.
- **3×3 :** rangée du haut = paupière sombre qui déborde de 1 px vers l'extérieur (le cil) ;
  au milieu, pupille + iris + reflet ; en bas, 1 px d'iris clair ou de blanc bleuté.
- **4×4 et plus :** recette « œil en grand » de C4 ; pour un chibi 64 px, l'œil en
  5 rangées de C13-C.
- **Partout :** les deux yeux ont la même forme (sauf en 3/4), le reflet est **du même côté**
  sur les deux, et le noir pur est réservé aux pupilles.
- **Sourcils :** à 16 px, la frange les remplace ; dès 24 à 32 px, un trait de 2 à 3 px dans
  le ton sombre des cheveux, assez haut (plus haut = plus doux).

### E. Expressions au pixel
On ne touche **qu'aux sourcils, aux yeux et à la bouche** ; le reste de la tête est
recopié à l'identique, sinon l'animation tremble.

| Émotion | 16 px (yeux seuls) | 32 px et plus |
|---|---|---|
| Joie | yeux en ligne de 2×1 ou en « ^ » | bouche ouverte, joues 1 px rosé |
| Colère | yeux 1×1 + 1 px d'ombre au coin intérieur haut | sourcils en V, yeux plus petits |
| Tristesse | yeux 1 px plus bas | intérieur des sourcils levé, bouche courbée vers le bas |
| Surprise | yeux 2×2 | yeux agrandis, bouche ronde sombre |
| Fatigue, ennui | yeux 2×1 horizontaux | paupière à mi-hauteur de l'iris |

### F. Couleurs du personnage
- **3 tons par partie**, 6 à 12 couleurs pour un petit personnage. Une teinte dominante pour
  le personnage, une couleur d'accent.
- **Peau :** base pêche ; ombre vers le rose ou le rouge-violet ; ombre profonde vers le
  violet-bleu ; lumière vers le jaune. ≈ 20° de décalage de teinte par cran, **dans le même
  sens pour toutes les rampes**.
- **Contour :** jamais noir ; un brun-rouge ou violet très sombre. Contour extérieur plus
  sombre que le contour intérieur. Contre la peau, le trait prend l'ombre de la peau ou
  disparaît (selout).
- **Séparation :** membres proches plus clairs, membres éloignés plus sombres.
- **Lumière :** une direction fixe pour tout le projet ; le visage reste majoritairement
  éclairé (C4).

### G. Vue de dessus 3/4 (jeu type Pokémon)
- On voit le **haut des épaules** ; le torse passe un peu sous la tête.
- Sprite 1 tuile de large × 2 de haut ; les pieds sont toujours sur la même rangée.
- **Directions :** face d'abord, puis dos, puis profil ; l'autre profil = miroir, sauf
  détail asymétrique (sac, mèche, arme) qu'on redessine.
- Même hauteur et même épaisseur de membres dans toutes les directions : on fait tourner
  le personnage pour vérifier.
- Hauteurs fixes par type : enfant < femme < homme ; une personne âgée un peu voûtée.
- Deux personnages peuvent se chevaucher en hauteur, jamais en largeur.

### H. Animation
- Mannequin en aplats d'abord ; costume et équipement sur des calques séparés.
- **Marche :** pas, passage, autre pas, passage (3 images uniques) ; le corps monte de 1 px
  aux passages ; les pieds ne glissent pas ; 100 à 150 ms par image. Plus fluide : 6 images.
- **Attente :** respiration de 1 px (tête et épaules) ; on tient les poses extrêmes plus
  longtemps ; cheveux et reflets bougent par petits pas réguliers.
- Le rebond de tête est asymétrique (il monte plus vite qu'il ne descend).

### I. Mains, cheveux, identité
- **Mains :** grossies volontairement ; on les dessine avant de régler les chevauchements.
- **Cheveux en petit :** une masse unique, 2 à 3 mèches finissant en pointe de 1 px, un
  reflet en bande cassée (jamais une rangée régulière). La coiffure est le premier marqueur
  d'identité.
- **Identité :** une forme forte (coiffure, chapeau, cape), une couleur dominante, une
  asymétrie voulue. Silhouettes types : guerrier large, mage en trapèze (robe), archer fin,
  soigneur en tons pastel.
- **Test :** en noir uni, à ×1, on reconnaît le personnage et sa direction.

### J. Procédure
1. Taille et rôle → lire la table A (part de la tête, yeux, couleurs).
2. Mannequin en aplats : tête, torse, membres proches, membres éloignés, ligne de sol.
3. **Le visage tout de suite** : il fixe l'échelle (ligne des yeux, recette D).
4. Coiffure et vêtements, puis test de la silhouette noire.
5. Palette (F), contour et selout, lumière.
6. Expressions, directions, animation.
7. Contrôle K.

### J2. Leçons du test 5 (Lina en 16×32, 32, 64 et portraits 32/48/64) [T5]
- **Œil à 32 px :** 2×3 (pupille sombre, reflet 1 px en haut du côté de la lumière, ton de
  l'iris en bas). Un 2×2 avec le reflet en bas lit comme un œil blanc ou un regard endormi.
- **Corps à 64 px :** jamais un torse rectangle et des bras en tubes. Il faut taille,
  hanches, coudes et mollets (en chibi, l'épaule reste une simple pente : règle 10) : au moins 1 px de variation de largeur à chaque
  articulation.
- **Frange :** les pointes de mèches sombres au-dessus des yeux lisent comme des sourcils
  froncés. Ton sombre seulement sur les côtés, frange relevée, une seule rangée d'ombre
  portée sur le front. (Confirmé au test 9 : voir C13-D.)
- **Pointes de cheveux :** 2 à 3 grandes pointes par côté, pas un peigne régulier de
  pointes d'1 px.
- **Œil de portrait anime :** grand (6×6 à 48, 8×8 à 64), paupière du haut = contour + 1
  rangée de ton coloré, blanc bleuté, iris sombre en haut et clair en bas, reflet 2×2 en
  haut + 1 px en bas du côté opposé, paupière du bas cassée en ton de peau sombre, cil au
  coin extérieur. Sourcils fins, posés seulement là où la peau se voit entre les mèches.
- **Visage de portrait :** joues pleines jusqu'aux yeux, menton court ; un visage trop long
  vieillit le personnage. Joues roses en 2 à 3 px de large, sinon elles disparaissent.
- **Lueur à 64 px :** des anneaux de couleur unie font du banding ; tramer la limite entre
  deux tons et garder un cœur clair petit (≈ 30 % de la flamme).
- **Contrôle :** toujours revoir la planche à ×1 et ×2 côte à côte (`controle_x1.png`).

### K. Contrôle et erreurs fréquentes
1. La tête et les yeux respectent-ils la table A ? Pas de nez ni de bouche à 16 px ?
2. Les yeux sont-ils sous la frange, bien espacés, reflets du même côté ?
3. Courbes : au plus 2 longueurs de pente, pas d'écart de plus de 1 entre pentes voisines,
   un angle vif finit sur 1 px.
4. Anticrénelage : 1 à 2 px par coin au plus, jamais sur le contour extérieur d'un sprite
   de jeu.
5. Pas de banding, pas de pillow shading, pas de pixel orphelin sur le visage.
6. Lisible à ×1, en noir uni, et dans toutes les directions ?
7. Budget de couleurs tenu (15 + transparent sur GBA) ?

---

## C11. Portrait anime de qualité : ce qui fait la différence [A][T6]
Constat du test 6 : les beaux portraits anime en pixel art n'ont **pas plus de pixels** que
les nôtres (visage de 25 à 40 px de large, comme notre portrait 64). La différence vient
de 8 décisions. Chacune, prise seule, améliore nettement le dessin.

### A. Les 8 décisions
1. **Jamais de face parfaite ni de symétrie miroir.** Tête de 3/4, légèrement penchée.
   L'axe du visage est décalé vers le côté tourné. L'œil lointain est plus étroit (≈ 80 %),
   la joue lointaine se lit seulement par son contour, la mâchoire proche monte vers l'oreille.
   Un visage miroir paraît figé, même bien ombré.
2. **Construire en courbes, pas en pixels.** On trace d'abord les formes comme en
   croquis (visage, cou, buste, masse arrière des cheveux, mèches), puis on les passe en
   pixels à la taille voulue. Les courbes restent douces et la même construction sert
   pour toutes les tailles. Les détails du visage, eux, se refont à chaque taille (C10).
3. **Les cheveux sont des mèches, pas un casque.** Chaque mèche est un ruban qui part
   d'une racine (raie, bandeau) et finit en pointe. Il y a 8 à 12 mèches en 4 couches :
   - masse arrière sombre ;
   - mèches des côtés qui encadrent le visage ;
   - frange qui **passe sur les yeux** ;
   - 1 ou 2 accents : un épi sur le crâne et une mèche fine qui traverse le visage.
   Chaque mèche a son propre volume : plus claire du côté de la lumière, plus sombre de
   l'autre. Une grande mèche est partagée par un pli sombre. Le reflet est un **anneau
   cassé**, coupé par les bords des mèches, sur le côté éclairé de la sphère du crâne.
4. **Traits colorés et sélectifs.**
   - Contour extérieur : couleur la plus sombre de la palette (un violet-marine, pas du noir).
     Il s'éclaircit d'un ton côté lumière.
   - Bord d'une mèche sur ce qui est derrière : trait dans le ton le plus sombre des
     cheveux, seulement côté ombre (droite et bas) et sur la peau.
   - Contour du visage, du menton et du cou : trait **chaud** (rose-brun), jamais noir.
   - Plus le format est petit, moins il y a de traits intérieurs : à 64 px, côté droit
     seulement ; à 96 px, droite et bas.
5. **Peau claire et plate, ombres qui racontent.** Le visage reste à 80 % dans le ton
   clair. Les ombres sont :
   - l'ombre portée de la frange, décalée vers le bas et la droite, épaisse de ≈ 2 % ;
   - la joue côté ombre ;
   - le cou sous le menton : une bande nette, pas un dégradé.
   Pas de modelé « oreiller » autour du nez ni des yeux.
6. **Décalage de teinte (hue shift).** Les ombres glissent vers le violet ou le rose : peau
   rose → mauve → prune. Les lumières glissent vers le jaune ou le vert d'eau. Une même
   couleur sombre sert à plusieurs matières (ombre de peau, ombre de veste, haut de l'iris).
   Cela économise la palette et unifie l'image.
7. **L'œil anime, c'est le cil, l'iris et les reflets.**
   - Cil du haut épais : 1 px au coin intérieur, 2 px au milieu et à l'extérieur, 3 px au
     coin extérieur à 96 px, avec un crochet qui déborde vers l'extérieur et le bas.
   - Iris grand et ovale, plus haut que large, qui remplit presque l'ouverture. Le blanc ne
     se voit que sur les côtés ; il est bleuté et ombré d'1 px sous le cil à partir de 96 px.
   - Iris en 3 tons verticaux : sombre en haut (≈ 30 %, l'ombre du cil), ton chaud au
     milieu, clair en bas. Pupille sombre.
   - Reflets : 2×2 en haut du côté de la lumière sur les deux yeux, plus 1 px en bas de
     l'autre côté.
   - Paupière du bas : un petit trait au coin extérieur seulement.
   - Iris d'une couleur **complémentaire** des cheveux (ambre pour des cheveux bleu-vert).
     C'est l'accent du portrait.
8. **Expression par 3 leviers : cils, sourcils, bouche.**
   - Sourcils fins, posés **par-dessus** la frange (convention anime), plus épais côté nez.
   - Bouche petite et ouverte : une rangée sombre et 1 à 2 px de langue rose.
   - Clin d'œil : arc de cils vers le bas avec crochet.
   - Surprise : bouche en « o », sourcils relevés de 2 px.
   - Joues : une bande rose sous l'œil, sans hachures sous 128 px (à petite taille, des
     hachures lisent comme des griffures).

### B. Budget de 15 couleurs (portrait GBA, testé)

| Groupe | Tons | Notes |
|---|---|---|
| Contour | 1 | violet-marine, sert aussi de pupille et de cil |
| Cheveux | 4 | reflet, clair, base, ombre (trait intérieur = ombre) |
| Peau | 4 | clair, base, ombre rosée, trait chaud prune (aussi ombre de veste et haut d'iris) |
| Joues | 1 | rose franc |
| Iris | 2 | ton chaud, ton clair (aussi bandeau) |
| Blanc | 1 | bleuté (œil, col, reflets) |
| Vêtement | 2 | clair, base ; l'ombre reprend le trait chaud |

### C. Procédure (fichier `test6_portraits/portrait.py`)
1. Construction en unités 0..100 : sphère du crâne, contour du visage de 3/4, cou, buste.
2. Masse arrière des cheveux, puis mèches en rubans de l'arrière vers l'avant.
   Chaque mèche = une courbe et une largeur à la racine.
3. Passage en pixels à la taille voulue. Chaque pixel garde son étiquette (quelle forme),
   sa position sur la mèche (racine → pointe, gauche → droite) et sa position sur la
   sphère du crâne.
4. Ombrage par la forme : sphère pour la masse, cylindre pour chaque mèche, puis seuils
   vers 3 tons.
5. Reflet en anneau, ombres portées, traits intérieurs sélectifs, contour extérieur avec
   selout.
6. Nettoyage : un pixel sans voisin direct de sa couleur prend la couleur majoritaire
   autour (2 passes).
7. Visage refait à chaque taille : yeux, sourcils, nez (1 px d'ombre), bouche, joues.
8. Contrôle à ×1, puis comparaison côte à côte avec une référence.

### D. Erreurs vues au test 6
- Bandeau dessiné sous la frange : il est mangé par les mèches et fait des taches. Il se
  pose **après** la frange, fin (≈ 3,5 % de la taille), ton clair en haut.
- Bas de la masse arrière en dents de scie : désordre. Il faut 1 ou 2 grandes pointes par côté.
- Veste ombrée en bandes verticales : effet de blocs. L'ombre suit des courbes autour de
  l'épaule éclairée.
- Trop de traits de mèche à 64 px : bruit. Les traits se réduisent avec la taille.
- Mèche fine qui traverse la joue : elle se lit comme une cicatrice si elle croise le rose
  des joues. Elle doit s'arrêter au-dessus.

## C12. Construire le visage : Loomis + proportions anime [L][R][T7]

Le visage du test 6 était raté : une forme ronde dessinée à la main, bas du visage écrasé,
mâchoire molle, pas de menton. Le bon ordre : on **construit la tête en volume**, puis on
tire de ce volume le contour, la mâchoire, les ombres et la place des traits.

### A. La tête en deux pièces (Loomis)
1. **Une boule pour le crâne.** De côté, on la coupe à plat sur les deux faces : ces
   « plans de côté » sont des disques (≈ 70 % du rayon depuis le centre). La tempe, la
   pommette et l'oreille sont sur ce plan.
2. **L'axe du visage** : une ligne qui passe au milieu du front, du nez et du menton. Elle
   se courbe avec la boule quand la tête tourne ; c'est elle qui montre où regarde le visage.
3. **Les lignes en travers**, perpendiculaires à l'axe et courbées sur la boule : sourcils,
   yeux, base du nez, bouche, menton.
4. **La mâchoire** est la seconde pièce : du dessous de l'oreille (angle de la mâchoire,
   placé **en arrière**) jusqu'au menton, en ligne presque droite.

### B. Proportions anime (fille ou jeune garçon), rayon du crâne = 1
| Repère | Position |
|---|---|
| haut du crâne | −1 |
| sourcils | ≈ 0 (milieu de la boule) |
| ligne des yeux | ≈ +0,3 : un peu **sous** le milieu de la tête entière |
| base du nez | à mi-chemin des yeux au menton |
| bouche | au tiers entre le nez et le menton |
| menton | ≈ +1,45 à +1,5 |
| oreille | de la ligne des yeux à celle du nez |
| écart des yeux | centres à ≈ ±0,5 ; l'écart vaut ~ une largeur d'œil |
| cou | étroit (≈ 0,6 de rayon de large), planté sous le crâne, **derrière** le menton |

Menton étroit et pointu (forme en V). Garçon plus âgé ou homme : menton plus large et plus
bas, angle de mâchoire plus marqué. Chibi : la partie menton est moitié plus courte. **En
pixel art (et en chibi surtout), ne garde pas ce V : la tête se pixelise en rond ou en
ovale de visage simplifié** (règle impérative 13), menton large et à peine aplati.

### C. La vue de 3/4 (le cas qui rate le plus)
- Côté **lointain** : le contour descend du crâne, fait une petite **bosse de pommette**
  juste sous l'œil, puis file droit au menton. On ne voit pas l'angle de la mâchoire.
- Côté **proche** : le contour suit le crâne jusqu'à l'oreille, puis la mâchoire part de
  l'oreille et rejoint le menton en ligne longue.
- L'axe se déplace vers le côté lointain ; l'œil lointain est **plus étroit** (raccourci)
  et plus près du bord ; le nez dépasse vers le côté lointain.
- Le plan de côté proche est une **zone d'ombre nette** quand la lumière vient de l'autre
  côté : de la tempe à la pommette, puis à l'angle de mâchoire.
- Le cou est décalé vers l'arrière : de 3/4, il part sous l'oreille et la joue, pas sous le menton.

### D. En code (fichier `test6_portraits/tete.py`)
On place une douzaine de points en 3D (pommettes, angles de mâchoire, coins du menton, axe),
on tourne la tête (lacet, tangage, roulis) et on projette. **Contour du visage = enveloppe
convexe du cercle du crâne et des points de mâchoire** : la bosse de pommette côté lointain
et la ligne de mâchoire côté proche sortent toutes seules. Les yeux, le nez et la bouche
sont des points 3D projetés ; le raccourci de l'œil lointain vient de l'orientation de
sa surface. La planche `construction_tete.png` montre la tête chauve à 0°, 25° et 45°.

### E. Contrôle du visage
- Couvrir les cheveux : la tête chauve doit déjà être juste.
- Mesurer : yeux un peu sous le milieu, nez à mi-chemin, bouche au tiers.
- En 3/4 : bosse de pommette côté lointain, mâchoire droite côté proche, menton sur l'axe.
- Le cou ne part pas du menton.

### F. Erreurs vues au test 7 (et corrections)
- **Trop de petites mèches** : des rayures partout. Mieux vaut 6 à 8 grandes mèches de frange
  qui se chevauchent, avec un trait de séparation **seulement vers la pointe**.
- **Front dégarni** entre les mèches : la frange doit couvrir le front ; le peu de peau qui se
  voit dessous est à l'ombre.
- **Bandeau, sourcils épais** : du bruit sur la frange. Sourcils de 1 px, accessoires seulement
  s'ils servent le personnage.
- **Plan de côté en plaque carrée** sur la joue : en anime, une bande étroite le long de la
  mâchoire suffit.
- **Buste en dôme et cou interminable** : les épaules tombent depuis le cou ; le col arrive
  peu sous le menton ; le cou est fin.
- **Ombre de veste en bloc vertical** : la limite d'ombre suit le corps (en biais).
- **Contour de la peau** en trait chaud, pas en marine : le visage paraît plus doux.

### G. Vue de face : les mesures Loomis appliquées [T8]

Règles reprises de tutoriels Loomis et anime, puis vérifiées en comptant les pixels sur le
portrait 96 px.

1. **Trois tiers.** Racine des cheveux → sourcils, sourcils → base du nez, base du nez →
   menton. En anime, le tiers du bas peut être plus court, à environ 0,6 ou 0,7 du tiers du
   milieu, mais pas moins.
2. **Le sourcil est SUR la ligne des sourcils, et l'œil en dessous.** Le centre de l'œil se
   place à environ 45 % de la distance entre la ligne des sourcils et la base du nez. Si le
   haut de l'œil touche la ligne des sourcils, le sourcil se colle au cil et on obtient un
   double trait épais. C'était l'erreur du test 7.
3. **Un œil d'écart entre les deux yeux.** Le centre de chaque œil est donc à une largeur
   d'œil de l'axe. En réaliste, la tête fait cinq yeux de large. En anime, compter 4 yeux de
   large, en gardant au moins 3 à 4 px de peau entre le coin extérieur et les cheveux. Avec
   12 px d'œil pour 38 px de visage, les yeux touchaient les mèches.
4. **Bouche au tiers.** Elle se place au tiers de la distance entre le nez et le menton,
   plus près du nez. Vue de face, c'est un sourire symétrique : deux coins relevés et un
   trait court.
5. **Oreilles** entre la ligne des sourcils et celle du nez.
6. **Lumière de face.** La lumière vient d'en haut et un peu de face. Sinon, toute la moitié
   basse des cheveux tombe dans la teinte la plus sombre et fait une masse plate.
7. **Joues pleines jusqu'à la ligne du nez.** Pour un visage anime de face qui ne soit pas
   trop mince, la largeur à la ligne du nez vaut environ 85 % de la largeur à la ligne des
   yeux. Ensuite seulement, deux diagonales presque droites descendent vers un menton
   pointu. À la ligne de la bouche, il reste environ 65 %. Si la mâchoire se resserre dès
   les yeux, le visage devient un long « V » trop mince. C'était l'erreur du test 8, relevée
   par l'utilisatrice. Le crâne doit aussi être assez gros par rapport au carré de cheveux :
   à 96 px, le rayon est de 24, pas 22.
8. **Le trait du menton doit être continu.** Le nettoyage des pixels isolés ne doit pas
   toucher au trait chaud (4). Sinon, la diagonale de la mâchoire, faite de pixels en
   escalier, se transforme en pointillés.

Tailles d'œil retenues pour la vue de face : 11×12 à 96 px, 8×9 à 64 px et 6×7 à 48 px.

---

## C13. Chibi pas à pas : de la construction au sprite [T9]
Inspiré de la façon dont un dessinateur construit un chibi (croquis, repères, volumes, puis
encrage), et vérifié en dessinant « Pip » (alchimiste) en 32 puis en 64 px.
Tout ce qui est dans C1 à C12 reste valable ; C13 donne **l'ordre** et les
pièges propres au chibi.

### A. Proportions et construction (calques de couleur, R4)
- **2,5 à 3 têtes** de haut ; tête ≈ 40 % de la hauteur ; yeux sous le milieu de la tête ;
  mains et pieds petits et ronds ; pas de cou visible ou presque.
- **Tête ronde ou ovale de visage, pas en œuf** (règle 13). Sur chibi2, la première tête
  se fermait en 7 rangées (24, 22, 20, 18, 14, 10, 6 px) : un œuf. Corrigée en ovale doux :
  26 px sur 2 rangées, puis 24, 22, 20, 16, 10.
- **Pas d'épaule marquée** (règle 10) : torse en cloche ou en trapèze étroit sous la tête ;
  pente régulière du cou au bras, bras le long du torse séparé par un seul trait. Le
  deltoïde en escalier de la première version de chibi2 était laid.
- **Rouge = pose** : ligne d'action, axe de la tête, bâton des épaules et du bassin.
- **Bleu = repères** : ligne des yeux, axe du visage, ligne du menton, sol.
- **Vert = volumes** : cercle de la tête, haricot du torse, cylindres courts des membres,
  mains en moufles.
- On regarde ce calque seul : la pose et la masse doivent déjà raconter le personnage.

### B. Ordre de travail (64 px) — v10 : le corps d'abord
Ordre validé sur chibi2 (étapes 01 à 08). Une étape = un fichier de commandes
`cXX.txt` + `etapeXX_nom.txt` + son rendu.
1. **Construction** (A) : pose rouge, repères bleus, volumes verts (`etape01`).
2. **Silhouette du corps nu** à plat, contour pixel-perfect (A5-6) : tête ronde ou ovale de visage, torse,
   membres avec leurs jointures (C14-A), **sans épaule marquée** (pente cou → bras, règle 10).
   Une rangée de plus sous les pieds (`etape02`).
3. **Ombres du corps** : peau claire, moyenne, sombre ; ombre de tête étroite (`etape03`).
4. **Corps final validé** : planche du corps seul (silhouette, ×1, gris). On ne passe pas à
   la suite tant que les jointures ne sont pas justes (`etape04`).
5. **Vêtements en calque** (C14-B) : aplats 1 px hors du corps, ombres, puis contour du
   calque seul, puis bords intérieurs à la main (`etape05`).
6. **Visage** (C) : yeux, joues, bouche, sur la tête déjà finie (`etape06`).
7. **Cheveux en calque** : masse en casque, tirets de lumière, ombre côté opposé, frange
   en pointes d'au moins 2 rangées, puis contour du calque seul (`etape07`).
8. **Accessoires, nettoyage** (A5-10), puis **planche de contrôle** (`etape08`).

### C. L'œil chibi (64 px, au moins 4×3 avec du blanc)
Cinq rangées, de haut en bas :
1. **paupière courte** (pas toute la largeur) ;
2. **cil extérieur** qui dépasse de 1 px vers le dehors ;
3. **reflet blanc** du côté de la lumière ;
4. iris et pupille ;
5. rangée claire d'iris (lumière qui traverse en bas).

À 32 px, garder la recette 2×3 de C10-J2.

### D. Pièges vus sur Pip (et corrections)
- **Paupière plate sur toute la largeur** : le regard paraît fâché. Paupière courte + cil
  extérieur (C).
- **Taches sombres sous la frange** : elles lisent comme des sourcils froncés (déjà vu au
  test 5). Cette zone reste en peau, une seule rangée d'ombre portée.
- **Lunettes posées trop bas** : elles se confondent avec les yeux. Les monter sur le front,
  bien séparées.
- **Remplissage de zone trop large** (`rep` sur un grand rectangle) : il a transformé le bras
  et la fiole en cheveux. Remplissages en dernier, sur des zones serrées, et regarder
  l'image juste après.
- **Main qui avale l'objet tenu** : main étroite (2 masses de doigts + le pouce), objet qui
  dépasse ; vérifier en silhouette noire.
- **Surface du liquide trop claire** : on lit du lait. Une lentille fine de 2 px (A5-8b).
- **Nez** : pas de trait, seulement son plan d'ombre (1 à 2 px).
- **Contour** : selout du côté de la lumière, contour plein du côté de l'ombre (C10-F).
- **Budget** : 14 à 20 couleurs à 64 px (Pip : 15).

### E. À corriger au prochain chibi
- **Frange** encore un peu plate : 3 ou 4 pointes nettes de 2 à 3 rangées.
- **Main levée** : la manche s'arrête net au poignet ; ajouter un revers de 1 px plus clair.
- **Pieds** : bottes trop de face ; tourner la botte d'appui vers l'extérieur.

---

## C14. Corps nu d'abord, vêtements en calque [T10]
Testé sur chibi2 (explorateur qui salue). Idée : on règle **une seule fois** les
problèmes du corps (attaches, jointures, proportions), sur un mannequin nu. Ensuite on
l'habille comme une poupée : chaque vêtement est un calque posé par-dessus, et on ne
revérifie plus l'anatomie.

### A. Le mannequin nu (étapes 01 à 04)
- **Mannequin lisse**, sans aucun détail sexuel : c'est un support, pas un nu.
- **Jointures obligatoires**, chacune avec sa marque en pixels :

  | Jointure | Marque |
  |---|---|
  | Épaule | **chibi : aucune marque**, pente régulière du cou au bras, bras collé au torse avec 1 trait de séparation (règle 10). Grand sprite aux proportions réalistes seulement : rondeur du deltoïde, 1 px plus large que le bras |
  | Aisselle | creux d'1 px en peau sombre |
  | Coude | pli d'1 px du côté intérieur, léger angle |
  | Poignet | resserré d'1 px avant la main |
  | Aine | V de peau moyenne |
  | Genou | rotule claire, ombre d'1 px dessous |
  | Cheville | resserrée d'1 px avant le pied |

- **Ombres du corps** dans la même lumière que la tenue à venir (haut-gauche).
- **Valider** le corps seul en planche avant d'habiller. Les défauts trouvés plus tard se
  corrigent ici, puis on relance les étapes suivantes (les fichiers `cXX.txt` le permettent).

### B. Habiller en calque (étape 05)
1. **Aplats** : chaque vêtement dans sa couleur moyenne, **1 px au-delà du bord du corps**
   (épaisseur du tissu). Manche, torse, short, bottes, écharpe : une zone à la fois.
2. **Ombres du tissu** dans la même passe : clair du côté de la lumière (épaule, haut de la
   manche levée), sombre du côté opposé, sous la manche, sous l'écharpe, en ourlet.
3. **Plis** : aux articulations seulement (coude, aisselle, aine) ; le bras levé tire le
   tissu en une **ligne de tension** de l'aisselle vers la hanche opposée.
4. **Contour du calque seul** :
   `python3 contour.py in.txt out.txt LETTRES_DU_CALQUE LETTRES_DE_PEAU`. Seules les lettres
   du calque qui touchent le vide ou la peau deviennent trait ; le contour du corps déjà
   posé ne bouge pas.
5. **Bords intérieurs à la main** (second fichier `cXXb.txt`) : séparation manche/torse,
   sangle, cadre et rabat de la sacoche, boucle de ceinture.
6. **Nettoyage des ourlets** : un ourlet ou un revers d'une rangée contre la peau devient
   tout noir et laisse des pixels clairs isolés. Pose une `hline O` propre à la main.
7. **Col ou écharpe** : son bord haut **est** le trait du menton. Ne laisse jamais deux
   traits collés ; mets l'ombre portée **sous** l'écharpe (tissu sombre), pas un trait.

### C. Pièges vus sur chibi2 (et corrections)
- **Manche levée trop fine**, sans trait au-dessus : élargir les rangées, le contour du
  calque pose ensuite le trait.
- **Écharpe mangée par le contour** contre le cou : la monter d'une rangée pour que son
  bord haut devienne le menton.
- **Revers de bottes et ourlets du short** : pixels clairs isolés après contour → `hline O`.
- **Frange d'une rangée** : entièrement transformée en trait. Les mèches font au moins
  2 rangées (règle impérative 24).
- **Sacoche** : sans cadre tracé à la main, elle se fond dans le short (même valeur).

---

## C15. Créatures et monstres [T11]
Test 11 : trois créatures originales en 64×64, une par langage de
formes. Même pipeline que les personnages (construction R/B/G → silhouette → contour →
volumes → détails → planche), avec les points propres aux bêtes ci-dessous.

### A. Un langage de formes par créature (décidé à l'étape 01)
| Créature | Langage | Lecture voulue | Marqueurs (2–3) | Accent saturé |
|---|---|---|---|---|
| **Mousseron** (champignon-esprit) | rond | doux, ami | chapeau, pousse sur la tête, queue-feuille | joues roses |
| **Tisonard** (renard d'obsidienne) | triangle | rapide, dangereux | museau en coin, 3 épines, flamme de queue | flamme |
| **Moellon** (tortue de pierre) | carré | lourd, lent, solide | carapace en dalles, arcade lourde, pattes-piliers | cristaux |

Le langage décide **tout** : contour de la tête, forme des yeux (rond = gros œil brillant ;
triangle = amande inclinée ; carré = œil mi-clos sous une arcade), forme des pieds, même
le sommet des cristaux (chanfreinés, pas pointus, chez Moellon).

### B. Silhouette : refaire tant qu'elle forme un bloc
- **Tête et corps en un seul rectangle** (Tisonard v1) : illisible. Une tête plus petite
  en coin, un **poitrail profond** et une **taille creusée** séparent les masses.
- **Pattes en pieds de table** : verticales, de même largeur, collées. Coude la patte
  arrière (cuisse → jarret → pied), évase le pied, et laisse un vide entre les pattes.
- **Flamme en œuf** : une flamme a 2–3 langues de longueurs différentes.
- **Queue en rectangle, pieds en dalles** (Mousseron v1) : effilée pour la queue, arrondie
  pour les pieds.
- **Cristaux en bâtonnets** (Moellon v1) : prismes trapus de 4–6 px, en groupe.
- **Tête trop petite** sur une grosse carapace : elle disparaît à ×1. Agrandis-la jusqu'à
  ce que l'œil se lise sur la planche.
- Contrôle : **silhouette noire** de la planche. Si on ne reconnaît pas la bête, on refait
  l'étape 02, pas l'ombrage.

### C. Pattes lointaines
Les pattes du côté opposé sont **plus sombres d'un cran** (entièrement dans l'ombre). Si
une patte proche touche une patte lointaine de même valeur, pose un **bord `O` à la main**
entre les deux (Moellon : `vline O 46 41 47`). L'ombre portée du corps tombe en haut des
pattes (1–2 rangées sombres).

### D. Matières émissives (flamme, braise, cristal lumineux)
- **Ombrage inversé** : cœur clair (`f` presque blanc) **en bas au centre**, puis `F`, puis
  `e` sur les bords. La lumière vient de l'objet, pas de la lampe haut-gauche.
- **Contour rouge sombre `E`** au lieu de `O` : un contour violet éteint la flamme.
- La flamme **éclaire ce qui la touche** : la queue juste dessous prend la teinte claire.
- Un reflet de la braise peut revenir ailleurs (intérieur d'oreille `e`, iris `F`) : il relie
  l'accent au reste de la créature sans ajouter de couleur.

### E. Bords intérieurs à la main
`contour.py` ne trace que le bord avec le vide. Tout ce qui se recouvre doit recevoir un
trait posé à la main : arcade au-dessus de l'œil, prismes de cristal entre eux, orteils
(`vline O` sur les 2 rangées du pied), pli entre oreille et crâne, séparation des pattes.
Un trait **horizontal au milieu de la tête** se lit comme une bouche ouverte (Moellon v1) :
l'arcade se pose plus haut, l'œil juste dessous.

### F. Matières
- **Pierre** : dalles carrées séparées par des sillons d'un cran plus sombres, chaque
  dalle avec un biseau clair en haut-gauche ; ombre propre en bas-droite de la masse.
- **Obsidienne** : violets froids, lumière en `a/q` lavande (pas blanc), faces gauches des
  épines claires, faces droites sombres.
- **Végétal sur pierre** (mousse) : posé sur le dessus, il **drape** vers le bas du côté
  éclairé ; deux tons seulement, désaturés, pour ne pas voler l'accent.

### G. Palette et étapes
Une `palette.json` par créature (≤ 15 couleurs + transparent ; les trois finales en ont 13,
13 et 14). Étapes : construction → silhouette → contour → volumes et bords intérieurs →
détails (yeux, bouche, selout) → final → planche.

## C16. Créatures complexes : morts-vivants et élémentaires [T12]
Test 12 : trois créatures plus chargées en 64×64 : **Ossard**
(squelette guerrier), **Blêmoire** (liche en robe) et **Magmorne** (golem de magma). Même
pipeline que C15. Une créature complexe garde **une** silhouette lisible et **un** accent
saturé. La complexité vient des pièces qu'on assemble, pas du nombre de couleurs.

### A. Squelette (Ossard)
- **Os d'au moins 4 px de large** (bras, fémurs, tibias) en 64 px : un os de 2 px devient
  un trait de contour et disparaît. Les articulations sont des **nœuds** plus larges d'1 px.
- **Cage thoracique** : remplis-la d'abord avec une couleur de **cavité** sombre `d`, puis
  pose les côtes par-dessus en arcs clairs. Des côtes posées sur le vide se lisent comme
  des rayures.
- Garde la cage **plus étroite que les épaules** (x20–39 pour Ossard) : une cage qui touche
  les bras fait un bloc (v1).
- **Crâne** : rond, avec une mâchoire plus étroite en dessous. Les orbites sont des trous `K`
  avec une lueur verte au centre. Pose un selout sur le haut du crâne (bord clair à la place
  du `O`).
- **Doigts de 2 px** : le pixel côté lumière est en os, l'autre reste `O`.
- **Asymétrie par l'équipement** : une seule épaulière, une épée ébréchée, un pagne
  déchiré. Ces pièces rouillées (brun orangé) restent ternes pour ne pas voler l'accent.

### B. Liche en robe (Blêmoire)
- **La robe est une cloche**, pas une boîte : elle s'élargit rang par rang (v1 était
  carrée). Fais un ourlet en lambeaux, avec des pointes de longueurs différentes.
- **Capuche** : c'est une ouverture sombre `K` avec un galon clair autour. Le crâne y est
  enfoncé et seuls les yeux brillent vraiment.
- **Manches larges et bras levés en V** : le bras droit est 2 px plus haut que le gauche,
  ce qui casse la symétrie. Pose à la main le bord entre la manche et le corps. Raccorde
  la manche à l'épaule par des rangs pleins (v1 : la manche droite flottait).
- **Parties flottantes** : des orbes au-dessus des paumes et des étincelles qui tombent.
  Laisse **au moins 1 px de vide** entre la partie flottante et le corps. Sinon, elle se
  lit comme une excroissance.
- **Plis** de la robe : quelques lignes verticales d'un cran plus sombres, qui partent de
  la ceinture.

### C. Élémentaire de magma (Magmorne)
- **Construction en rochers** : une boule pour le torse, deux pour les épaules, une petite
  tête **enfoncée entre les épaules** (plus haute qu'elles d'à peine 7 px), des jambes
  courtes et des pieds larges.
- **Poings flottants** : l'avant-bras s'arrête et le poing flotte à côté, avec 2 px de vide
  entre les deux. Un poing est levé et l'autre est bas, ce qui crée l'asymétrie et le
  mouvement. Les doigts sont séparés par des lignes de lave.
- **Joints de lave à la place des bords intérieurs** : entre deux rochers, le trait posé à
  la main est en rouge sombre `x`, avec un pixel `o` plus vif au milieu des longs joints.
  Un `O` violet ici éteindrait la créature.
- **Cœur émissif** : centre presque blanc `w`, puis `y`, puis `o`, puis un bord `x`. Des
  fissures partent du cœur et rayonnent vers le bord du torse.
- **Volumes** : chaque rocher est une boule éclairée en haut à gauche (`s` clair, `m`
  moyen, `k` sombre). Une boule n'est pas ombrée comme les autres : on applique la même
  règle de lumière à chaque volume, puis les joints séparent les volumes.
- **Débris et braises** : de petits rochers de 2–3 px avec leur contour, et des braises
  d'**un seul pixel** sans contour.
- Palette courte (9 couleurs) : 4 tons de roche froids et 4 tons de lave chauds, plus `O`.
  Le contraste froid/chaud suffit.

### D. Règles communes
| Règle | Pourquoi |
|---|---|
| Émissif : cœur clair au centre, bords plus sombres | la lumière vient de l'objet |
| Un seul accent saturé (vert nécrotique, ou lave) | l'œil va droit à la menace |
| Parties flottantes séparées par du vide (≥ 1–2 px) | sinon elles collent au corps |
| Asymétrie par un bras levé ou une pièce d'armure | une pose symétrique est figée |
| Bords intérieurs posés à la main (manche/corps, rocher/rocher) | `contour.py` ne voit que le vide |
| Cavité sombre avant les détails (cage, capuche, orbites) | le détail clair se lit sur du sombre |

Couleurs : Ossard en a 15, Blêmoire 13 et Magmorne 9.

---

## C17. Vêtements : du simple au complexe [R]
Complète C5 (design) et C14 (calque sur corps nu). C14 dit **où** poser le vêtement ;
C17 dit **comment le rendre** : poids du tissu, plis, motifs, matières, puis des recettes
pièce par pièce. Lumière haut-gauche, trait `O`, rampes de A6.

### A. Les trois questions avant de poser un pixel
1. **D'où pend le tissu ?** Repérer les **points d'appui** : épaules, haut des bras, taille
   (ceinture), hanches. Le tissu s'y accroche, et tout le reste pend ou se tend depuis là.
2. **Où est-il tiré ou compressé ?** Les **points de tension** : aisselle, coude plié,
   genou plié, entrejambe, ceinture serrée, bras levé. Les plis **rayonnent** de ces
   points, comme des rayons d'un moyeu, et meurent en s'éloignant.
3. **Quel poids ?** Tissu lourd (laine, cuir, manteau) : **peu de plis, grands et
   arrondis**. Tissu léger (soie, coton fin) : **beaucoup de petits plis, fins et nets**.
   Vêtement moulant : petits plis en U aux articulations, presque rien ailleurs.

**Règle d'or :** on dessine **moins** de plis qu'on n'en voit. À 32 px, 1 à 3 plis par
pièce de vêtement, placés aux points de tension. Un pli qui n'explique rien est du bruit.

### B. Les sept plis (Bridgman) et leur recette pixel
| Pli | Où | Forme | Recette pixel |
|---|---|---|---|
| **Tuyau** (pipe) | tissu qui pend d'un point : bas de jupe, rideau, cape | cylindres verticaux qui s'élargissent vers le bas | bandes verticales : ton clair (côté lumière du tube) puis ton sombre ; bas de l'ourlet en vague (creux et bosses alternés) |
| **Zigzag** | tube plié ou compressé : manche retroussée, derrière du genou, bas de pantalon tassé sur la botte | V emboîtés, alternés gauche/droite | chevrons de 2-3 px en ton sombre, décalés d'une rangée à l'autre ; ne pas les aligner (banding) |
| **Spirale** | tissu enroulé autour d'un membre : manche moulante, bandage, jambière | diagonales parallèles qui tournent autour du cylindre | courtes diagonales sombres régulières, toutes dans le même sens ; plus serrées sur le bord (le cylindre tourne) |
| **Demi-nœud** (half-lock) | là où le tube change de direction : coude, genou, hanche | gros pli en forme de nœud à l'intérieur du coude | 1 cluster sombre en virgule du côté intérieur de l'articulation + 1 px clair au-dessus ; côté extérieur tendu, lisse |
| **Hamac** (diaper) | tissu tendu entre deux appuis : col bénitier, entrejambe, cape entre les épaules, écharpe | U ou V qui pendent | arcs en U sombres emboîtés, le plus profond au centre ; 1 ligne claire sur le haut de chaque arc |
| **Chute** (drop) | tissu qui tombe d'un appui unique : manche de toge, foulard, drapeau au repos | cône qui s'évase | un pli tuyau qui part en pointe de l'appui et s'ouvre ; ombre forte juste sous l'appui (AO) |
| **Inerte** | tissu posé au sol ou sur un objet | plis écrasés, irréguliers | clusters plats, peu de contraste, ombre portée sous le tissu |

Variante Proko utile au mouvement : **compression** (tissu tassé : accordéon de petits
plis courts, par ex. manche remontée sur l'avant-bras) et **drapeau** (tissu emporté par
le vent ou le mouvement : grandes vagues qui partent du point d'attache et vont dans le
sens opposé au mouvement).

### C. Dessiner un pli en pixels
- **Pas de trait pour un pli.** Un pli = une **ombre** (ton sombre de la matière) collée à
  une **lumière** (ton clair) du côté de la source. Le `O` est réservé au contour et aux
  vraies séparations de pièces.
- **Bords mixtes :** le côté du pli qui se creuse (vers l'ombre) est **dur** (passage
  direct clair → sombre) ; le côté qui remonte doucement est **doux** (un ton moyen
  intermédiaire, ou la marche s'allonge). Que des bords durs = tissu en carton ; que des
  bords doux = plastique fondu.
- **Le pli suit la forme :** sur un cylindre (bras, jambe), il est courbe ; sur le torse,
  il descend en diagonale depuis le point de tension. Jamais de pli parfaitement
  horizontal ou vertical sur un corps, sauf le tuyau d'une jupe.
- **Le pli casse le contour :** là où un pli important arrive au bord, la silhouette fait
  une petite encoche ou une bosse d'1 px. C'est ce qui rend le tissu « vrai » à petite
  taille.
- **Taille du sprite :**

  | Taille | Plis | Ourlets et coutures |
  |---|---|---|
  | 16 px | aucun pli : 2 tons (clair / sombre) par pièce suffisent | rien ; la ceinture est une rangée de couleur |
  | 24-32 px | 1-3 plis par pièce, aux articulations ; un pli = 2-3 px sombres | ourlet = 1 rangée plus sombre ; col en 2-3 px |
  | 48-64 px | plis tuyau, hamac et demi-nœud lisibles ; bords mixtes | ourlets, revers, coutures de 1 px (ton sombre, pointillés si piqûre) |
  | 96-128 px | tout le vocabulaire ; textures de matière (A6, C17-F) | boutons, boutonnières, piqûres, usure des bords |

### D. Recettes par vêtement (du plus simple au plus complexe)
**1. T-shirt / haut simple.**
Aplat 1 px hors du corps (C14-B). Ombre sous la poitrine et sur le côté opposé à la
lumière. Pli **hamac** léger sous le col si le col est large ; **demi-nœud** à
l'aisselle (1 virgule sombre). Ourlet de manche : 1 rangée sombre + encoche dans la
silhouette. Le bas du t-shirt ne fait **pas** une ligne droite : il suit le bassin
(légère courbe vers le bas au centre en 3/4).

**2. Pantalon.**
Les plis partent de l'**entrejambe** (hamac en V) et des **genoux** (demi-nœud derrière,
zigzag si la jambe est pliée). Jambe tendue : un long tuyau qui part de la hanche, ombre
sur le côté intérieur. Bas du pantalon : petit **zigzag** de compression s'il tombe sur la
chaussure (2-3 chevrons). Couture extérieure en 1 px sombre seulement à 64 px et plus.

**3. Short, jupe courte.**
Le bord bas est un **cylindre vu de biais** : l'ourlet est une courbe (ellipse), pas une
droite ; on voit l'intérieur sombre du tube sur 1 rangée côté ombre.

**4. Jupe = cônes.**
Dessiner la jupe comme **un grand cône** (de la taille à l'ourlet), puis découper en **cônes
plus petits** (les godets). Chaque petit cône a son côté clair (vers la lumière) et son
côté sombre ; les creux entre deux cônes sont les plus sombres (AO). L'ourlet ondule :
bosse sous chaque cône, creux entre deux. Jupe plissée : cônes réguliers et étroits,
bords durs ; jupe ample : peu de cônes, bords doux.

**5. Veste ou chemise par-dessus (superposition).**
Chaque couche = un calque (C14). Règles :
- la couche du dessus **projette une ombre** d'1 px sur celle du dessous (sous le col,
  sous le revers, au bord de la veste ouverte) ;
- la couche du dessus est **1 px plus large** que celle du dessous ;
- une veste ouverte montre la chemise en **bande verticale** au centre, plus claire si
  c'est la chemise, avec l'ombre de la veste sur ses bords ;
- un revers de col = un triangle clair (dessus du revers) + son ombre dessous.

**6. Ceinture, sangles, bretelles.**
Elles **serrent** : le tissu au-dessus et au-dessous fait de petits plis qui rayonnent
(hamac court de 2 px de chaque côté). Une sangle en diagonale : rangée claire dessus,
sombre dessous (chibi2 : `h` / `H`), et elle **enfonce** le tissu (1 px d'ombre de chaque
côté). Boucle : 2×2 à 3×3 px, ton métal le plus clair au coin haut-gauche.

**7. Écharpe, foulard, col roulé.**
Volume **épais** autour du cou : un tore. Le haut est clair, le dessous très sombre
(AO sur le menton et la poitrine). Les tours de l'écharpe font des **hamacs** ; le pan qui
tombe fait une **chute** (cône) avec un ourlet en bout (frange : 2-3 px clairs séparés
par du sombre). Le bord haut de l'écharpe sert de trait de menton (C14-B7).

**8. Cape, manteau long, robe.**
- **Silhouette d'abord** : une cape, c'est d'abord une forme (triangle, cloche, rideau).
  Faire la silhouette noire avant tout pli (A5-5).
- Points d'appui : les **épaules** (et l'attache au cou) ; les plis partent de là en
  **tuyaux** qui s'élargissent vers le bas. Entre les épaules dans le dos : un **hamac**.
- **Intérieur visible** : là où la cape se retourne, on voit la doublure (couleur
  différente, plus sombre ou complémentaire). Ça donne de l'épaisseur et de la couleur.
- **Ourlet** : ondulé (bosses sous les tuyaux), jamais une règle droite. Une cape en
  mouvement fait des **drapeaux** : grandes vagues opposées au mouvement.
- **Tissu lourd** (manteau de laine) : 2-4 plis seulement, bords doux ; **tissu léger**
  (voile, robe d'été) : plis nombreux et fins, bords durs.

**9. Armure.**
- **Plaques de métal** : chaque plaque est un volume simple (cylindre pour le bras, coque
  pour le torse). Contraste **fort** : noir profond à côté d'un reflet presque blanc.
  Reflet **petit et net** au point le plus proche de la lumière ; **contre-reflet** (une
  bande sombre au milieu de la zone claire, ou une bande claire dans l'ombre) pour faire
  « métal poli ». Peu de tons : 3-4 suffisent sous 32 px.
- **Plaques qui se chevauchent** (épaulières, jupe de plaques) : chaque plaque du dessus
  projette 1 px d'ombre sur celle du dessous ; bord du dessus = 1 px clair.
- **Rivets** : 1 px clair + 1 px sombre en diagonale (bas-droite) ; alignés et espacés
  régulièrement le long du bord.
- **Cotte de mailles** : un motif répétitif (damier, petits ronds ou « o » alternés)
  posé sur un ombrage déjà juste. Le motif s'assombrit dans l'ombre, et on le **coupe**
  dans les zones les plus sombres.
- **Exagérer le trait distinctif** : la pointe du casque, la grosse épaulière, le blason
  du bouclier. À petite taille, l'armure se reconnaît à une seule forme forte.
- **Armure de cuir** : voir F (mat, coutures, bords usés).

### E. Motifs (rayures, carreaux, imprimés)
- **Ordre :** aplat → ombrage complet du vêtement → **motif en dernier**, posé sur
  l'ombrage (ton clair du motif dans la lumière, ton sombre dans l'ombre).
- **Le motif suit la forme :** les rayures tournent avec le cylindre (droites au centre
  du bras, courbes et resserrées sur les bords). Dans un pli, la rayure se **casse** :
  elle s'arrête au creux et repart décalée.
- **Il disparaît dans l'ombre profonde :** dans les creux (AO), ne pas poser le motif.
- **Grande échelle à petite taille :** à 32 px, une rayure fait au moins 1 px et l'écart
  au moins 1 px ; un carreau fait au moins 2×2. Plus fin, le motif devient du bruit.
- **Ton du motif proche du fond** (1-2 marches de valeur) sauf si c'est le point
  d'intérêt : un motif très contrasté mange le volume.

### F. Matières
| Matière | Contraste | Reflet | Bords des plis | Signes particuliers |
|---|---|---|---|---|
| **Coton, toile** | moyen | large et doux | mixtes | ourlets visibles, plis moyens |
| **Laine, tricot** | faible | aucun reflet net | doux, arrondis | grosses formes, côtes en lignes verticales ; peluche au bord (silhouette légèrement bosselée) |
| **Cuir** | moyen-fort | moyen, assez large, à peine brillant | durs aux plis, cassures nettes | coutures en pointillés, bords usés plus clairs, plis peu nombreux et marqués |
| **Soie, satin** | très fort | **longs reflets fins** qui suivent chaque pli | très durs | beaucoup de petits plis, le clair et le sombre se touchent presque sans ton moyen |
| **Velours** | inversé | les **bords** et les plis sont plus clairs que le centre face à nous | doux | ton sombre et saturé au centre, liseré clair sur la silhouette |
| **Fourrure** | faible | — | — | ombrage lisse d'abord, puis on **taille** des touffes (triangles, mèches de 2-4 px) dans le contour et dans les limites d'ombre ; des touffes, pas des poils ; un peu de dither seulement à la limite |
| **Métal** | maximal | petit, net, presque blanc | — | contre-reflet, reflet du ciel en haut (froid) et du sol en bas (chaud) ; voir la recette 9 (armure) |

### G. Détails qui font « fini »
- **Col, poignets, ourlets** : 1 rangée plus sombre ou plus claire ; l'épaisseur du tissu
  se voit en **1 px de bord** à l'ouverture (on voit dedans, côté ombre).
- **Coutures** : seulement à partir de 48 px ; pointillés réguliers d'1 px, ton sombre de
  la matière, qui suivent la courbe.
- **Boutons** : 1 px (32 px) à 2×2 (64 px) ; un clair et un sombre. Alignés sur la
  ligne centrale qui suit la torsion du torse (C2).
- **Poches, rabats** : un rectangle déformé par le volume, son bord haut clair, son
  ombre portée dessous.
- **Usure** : bords plus clairs (cuir, jean), taches plus sombres aux genoux et coudes —
  une touche, pas un motif.

### H. Erreurs fréquentes (et corrections)
| Erreur | Pourquoi ça rate | Correction |
|---|---|---|
| Plis tracés en `O` | le vêtement paraît découpé, pas drapé | pli = ombre de la matière + lumière (C17-C) |
| Plis partout, tous pareils | bruit, banding | 1-3 plis, aux points de tension, de tailles différentes |
| Plis qui ne partent de rien | le tissu « flotte » | chaque pli remonte à un appui ou à une tension |
| Ourlet droit | le vêtement est en carton | ourlet en courbe (cylindre) ou en vague (tuyaux) |
| Vêtement collé au corps, même contour | on ne voit pas le tissu | 1 px au-delà du corps (C14-B1), encoches aux plis |
| Rayures droites sur un bras | aucun volume | rayures courbes, qui se resserrent sur les bords |
| Ombrage coussin sur chaque pièce | aucune lumière | même lumière haut-gauche pour tout le personnage |
| Couches sans ombre portée | les couches se confondent | 1 px d'ombre sous chaque couche du dessus |
| Même valeur pour deux pièces voisines | elles se fondent en gris | décaler les valeurs (A5-11, contrôle en gris) |

### I. Ordre de travail d'un vêtement
1. **Silhouette** du vêtement (forme noire), avec ses appuis et ses tensions marqués au
   croquis (points rouges).
2. **Aplat** 1 px hors du corps (C14-B1).
3. **Ombre propre** (côté opposé à la lumière) + **AO** (sous les couches, dans les creux).
4. **Plis** : du plus grand au plus petit, en partant des tensions (C17-B, C).
5. **Lumières** et reflets selon la matière (C17-F).
6. **Motif** s'il y en a un (C17-E).
7. **Contour du calque** (`contour.py`), puis **bords intérieurs à la main** (C14-B5).
8. **Détails** (C17-G), **nettoyage** (A6-H) et planche.

---

# Partie D — Outils et dossiers
Les scripts sont dans `methode_dessin/outils/`. Ils **ne décident rien** (R3) : ils posent
ce qui a été décidé à la main, ou rendent l'image pour la regarder (R1).

| Outil | Usage | Rôle |
|---|---|---|
| `trace.py` | `python3 trace.py in.txt\|NEW:64x64 out.txt cmds.txt` | pose des primitives décidées : `px C x y`, `hline C x1 x2 y`, `vline C x y1 y2`, `rect C x1 y1 x2 y2`, `frame`, `disc C cx cy r`, `ring`, `rows C y x1 x2 […]`, `rep A B x1 y1 x2 y2` (remplace A par B dans une zone, `*` = tout pixel plein ; à manier avec prudence, C13-D) |
| `px.py` | `python3 px.py etape_XX.txt 12 palette.json` | rend la grille texte (1 caractère = 1 pixel, `.` = vide) en `etape_XX.png` à ×1 et `etape_XX_vue.png` agrandi avec grille |
| `contour.py` | `python3 contour.py in.txt out.txt [CALQUE [CONTRE]] [--trait=O]` | règle mécanique de contour. Sans calque : tout pixel plein qui touche le vide devient trait. Avec `CALQUE` (ex. `tjJreEucChkHY`) : seules ces lettres, si elles touchent le vide ou une lettre de `CONTRE` (ex. la peau `slmS`), deviennent trait (C14-B) |
| `planche.py` | `python3 planche.py in.png out.png [situation.png]` | planche de contrôle (A5-11). Rangée 1 : ×1 et ×2 sur fond clair et sombre, miroir, silhouette, gris. Rangée 2 : ×4, image en situation si donnée, gris ×4 |

- Une étape = `cXX.txt` (commandes) → `etapeXX_nom.txt` → `.png` + `_vue.png`.
- **Lire une capture annotée** : sur une image `_vue`, une case = l'échelle du rendu (par
  exemple 12 px). Les cases colorées par l'utilisateur donnent donc les coordonnées
  exactes des pixels à changer.

**Dossiers de tests** (dans `methode_dessin/`, chacun avec ses notes) :
`test1_samourai` · `test2_samourai_v3` · `test3_objets` · `test4_objets_v4` ·
`test5_personnages` · `test6_portraits` (`tete.py`, `construction.py`, `portrait.py`) ·
`test9_chibi` · `test12_batiment` · `test13_chibi_template` (et `costume/`) ·
`test14_cheveux`. Les fichiers de Pip, de chibi2 et des créatures (C13 à C16) n'ont pas été
gardés : seules leurs leçons restent dans ce document.

---

# Partie E — Animation [R][T15]

Une animation, c'est une suite de dessins finis. Chaque image passe par **tout** le
pipeline A5. On ne gagne pas de temps en sautant des étapes : une image bâclée se voit
même à 80 ms, parce qu'elle fait « sauter » la silhouette.

## E0. Méthode imposée (dans cet ordre, sans rien sauter)

1. **Intention (B0) de l'animation.** En une phrase : ce qui bouge, pourquoi, et l'émotion
   (solennel, comique, nerveux…). Note la durée totale visée.
2. **Pose de départ et pose d'arrivée finies d'abord.** Ce sont deux dessins statiques
   complets (pipeline A5 + planche). L'animation relie deux images déjà validées.
3. **Découpe mentale du mouvement en un nombre d'images fixé à l'avance.** Écris la liste
   avant de dessiner : numéro, rôle (**clé**, **extrême**, **intermédiaire de passage**
   « breakdown », **intervalle** « in-between », **tenue**), ce qui change, durée en ms.
   C'est la **feuille de timing** (`ANIM_PLAN.md`). On ne rajoute pas d'image en cours de
   route sans mettre la feuille à jour.
4. **Ordre de dessin : pose à pose.** Clés d'abord, puis extrêmes, puis passages, puis
   intervalles. Les effets libres (flamme, étincelle, fumée) peuvent se faire « tout
   droit » (image après image), mais **dans un calque à part**.
5. **Pour CHAQUE image, applique le pipeline complet** : 01 silhouette → 02 contour →
   03 aplats → 04 lumière → 05 détails → contrôle. Un fichier `.txt` + `.png` par étape,
   regardé à ×1 et agrandi. **Valide l'image (E5-A) avant de passer à la suivante.**
   Une image non validée bloque la suivante.
6. **Partir de l'image validée précédente est permis** (copie de grille) **si et seulement
   si** on refait quand même les cinq étapes sur ce qui change : la silhouette de l'image
   se redessine, le contour se re-vérifie, la lumière se re-place. On ne déplace jamais un
   bloc d'ombre sans vérifier qu'il obéit encore à la lumière en haut à gauche.
7. **Contrôle de séquence (E5-B)** : bande de toutes les images côte à côte, pelure
   d'oignon, GIF aux vraies durées. Note au moins un défaut, corrige l'image fautive à son
   étape fautive, refais la bande.

## E1. Les 12 principes de *The Illusion of Life* (Thomas et Johnston), en règles pixel

| # | Principe | Règle impérative en pixel art |
|---|---|---|
| 1 | **Écrasement et étirement** (squash & stretch) | **Le volume ne change pas** : si un objet perd 2 px de haut, il gagne ~2 px de large. Écrase à l'impact, étire dans la vitesse. Les objets rigides (métal, bois) ne s'écrasent pas : c'est leur **mouvement** qui s'écrase (recul plus court, rebond). |
| 2 | **Anticipation** | Avant toute action, un **petit mouvement inverse** (recul, ramassement). Il prend **plus d'images que l'action elle-même** (ex. 3 images d'anticipation pour 1-2 d'action). |
| 3 | **Mise en scène** (staging) | **Une seule action principale à la fois.** La silhouette de chaque image clé doit se lire seule. Rien d'autre ne bouge pendant l'image clé. |
| 4 | **Tout droit / pose à pose** | Pose à pose pour la structure (E0-4). Tout droit seulement pour les effets organiques, dans un calque séparé. |
| 5 | **Continuité et chevauchement** (follow-through & overlapping) | **Rien ne s'arrête d'un coup.** Les parties souples (tissu, cheveux, pendentif, queue) s'arrêtent **1 à 3 images après** le corps, dépassent puis reviennent. L'action est finie quand l'élan est à zéro, pas quand la pièce principale est arrivée. |
| 6 | **Ralenti au départ et à l'arrivée** (slow in / slow out) | Espacement **serré près des clés, large au milieu**. En pixel art, deux leviers : la **distance** entre images, et la **durée** de chaque image (image plus longue = ralenti). |
| 7 | **Arcs** | Tout mouvement naturel suit une courbe. **Trace l'arc-guide** (calque à part) et place chaque position dessus. Un mouvement mécanique (rouleau sur rail) peut rester droit. |
| 8 | **Action secondaire** | Elle **appuie** l'action principale (éclat, poussière, petit rebond d'un ornement), **elle ne la cache jamais**. Elle commence après la principale ou sur son impact. |
| 9 | **Timing** | Le nombre d'images et leur durée **donnent le poids et l'humeur**. Peu d'images rapides = léger, nerveux. Beaucoup d'images lentes = lourd, solennel. Décide-le dans la feuille de timing, pas en dessinant. |
| 10 | **Exagération** | Pousse les poses clés **au-delà** du réel (dépassement de 2 à 4 px, écrasement visible). À 32 px, un mouvement de 1 px ne se voit presque pas : exagère ou n'anime pas. |
| 11 | **Dessin solide** | Chaque image respecte **volume, lumière et contour** comme un dessin statique (pipeline A5). Pelure d'oignon : la taille d'un objet ne doit pas « respirer » par erreur. |
| 12 | **Attrait** (appeal) | Formes claires, silhouette lisible, **asymétrie voulue**. Pas de « jumeaux » : deux côtés ne bougent jamais exactement en miroir et en même temps ; décale l'un d'une image ou change son amplitude. |

## E2. Techniques propres au pixel art

**A. Cadence et durées**
- Base : **12 images/s, soit ~83 ms par image** (« animer en deux »). Les jeux GBA tournent
  à 60 Hz : une image = un multiple de 16,7 ms (ex. 50, 67, 83, 100, 133 ms).
- **Chaque image a sa propre durée.** C'est l'outil principal du ralenti : on allonge les
  images près des clés au lieu d'ajouter des dessins.
- **Tenues** : l'image clé ou l'impact dure **3 à 4 fois** une image de mouvement (ex.
  250-300 ms contre 70-80 ms). La pose finale tient assez pour être lue.
- **Interface (UI)** : une apparition dure **200 à 500 ms** de mouvement ; au-delà, elle
  gêne le joueur. Une animation d'ouverture « cérémonielle » peut aller à ~1,5 s si elle
  n'est jouée qu'une fois.

**B. Espacement**
- Calcule l'espacement avant de dessiner (ex. ralenti à l'arrivée sur 30 px en 5 images :
  12, 8, 5, 3, 2). Écris-le dans la feuille de timing.
- **Dépassement** (overshoot) : la pièce va 2-4 px trop loin, revient de 1-2 px au-delà
  du bon point en sens inverse, puis se pose. Deux rebonds maximum.

**C. Image étirée** (smear)
- Pour un mouvement **plus rapide qu'une image**, dessine une seule image où la forme
  s'allonge dans le sens du mouvement (traînée de la couleur de base, sans détail).
- **Une seule image, jamais deux de suite**, et jamais sur une tenue.

**D. Sous-pixel**
- Pour un mouvement **plus petit qu'un pixel** (respiration, flottement), on ne déplace pas
  la silhouette : on **décale les couleurs** d'un demi-ton sur le bord (le pixel de bord
  passe du clair au moyen). Le contour reste fixe.
- **On change des couleurs au lieu de changer des positions** [R] : respiration, clignement,
  transfert de poids, tissu qui ondule. Le mouvement reste doux même à 16×16, à condition
  d'avoir au moins deux tons voisins sur la zone qui bouge.
- **Méthode** : poser les deux images clés, puis ajouter et retirer des pixels de ton
  intermédiaire d'une image à l'autre jusqu'à ce que le mouvement glisse. On regarde en GIF
  aux vraies durées à chaque essai.
- Une animation pixel détaillée (style arcade des années 1990) combine les deux : la
  silhouette bouge par pixels entiers sur les grandes actions, les détails par sous-pixels.

**E. Volume, pelure d'oignon, calques**
- Vérifie chaque image sur la précédente en transparence (pelure d'oignon). Compte les
  pixels d'un objet rigide : il ne doit pas changer de taille sans raison.
- Une **pièce = un calque** (rouleau gauche, rouleau droit, papier, médaillon, éclats).
  On compose l'image en empilant les calques ; on ne redessine pas ce qui ne bouge pas,
  mais on **revérifie** les raccords.

**F. Lumière qui reste vraie**
- La lumière vient **toujours d'en haut à gauche, quelle que soit la position**. Une pièce
  qui tourne garde son reflet en haut à gauche ; elle ne « porte » pas son reflet avec elle.
- Un objet **émissif** qui s'allume passe par une rampe : éteint (couleurs sombres) →
  première lueur (moyenne) → pic (plus clair que la pose finale, 1 image) → pose finale.
  Le pic plus clair que la fin = « pop » de lumière.

**G. Apparition d'un objet** (pop)
- Jamais d'un coup en taille finale : petit (≈ 40-60 %) → **trop grand** (110-120 %,
  1 image) → légèrement écrasé → taille finale. C'est l'écrasement-étirement appliqué à
  l'échelle.
- Aux petites tailles, une forme réduite **se redessine** (B4b) ; on ne réduit jamais
  par calcul.

**H. Éclats** (sparkle, glint)
- Un éclat vit en **4 à 6 états en escalier** : point → croix 3 px → croix 5 px (pic) →
  croix 3 px → point → rien. Pas d'éclat qui reste allumé.
- **Un éclat à la fois** à l'écran, posé sur la zone la plus claire (côté lumière).

**I. Boucle d'attente** (idle)
- Première et dernière image doivent s'enchaîner sans saut. Garde l'amplitude petite
  (1 px ou sous-pixel) et une durée longue (600 ms à 1 s par état).

**J. Ce qu'on interdit**
- Une image identique à la précédente (utilise une durée plus longue à la place).
- Un mouvement linéaire (même espacement partout) pour un objet vivant ou lancé.
- Plus d'une action principale en même temps.
- Des pixels qui « grouillent » : un pixel de détail qui change d'une image à l'autre
  sans raison (bruit d'animation).
- Une forme qui grandit ou rétrécit sans écrasement voulu.

## E3. Feuille de timing (modèle)

| Image | Rôle | Ce qui change | Principe | Durée |
|---|---|---|---|---|
| 01 | clé | pose de départ | mise en scène | 300 ms |
| 02 | anticipation | ramassement | anticipation, écrasement | 120 ms |
| 03 | passage | départ rapide | ralenti au départ | 67 ms |
| … | … | … | … | … |
| N | clé | pose finale | tenue | 600 ms+ |

## E4. Fichiers d'une animation

- `ANIM_PLAN.md` : intention, liste des images, espacements, durées.
- `fXX/` : un dossier par image avec `cXX_0N.txt` (commandes), `etape01…05_*.txt/.png`,
  `final.txt/.png`, et une ligne « validée » dans `ANIM_PLAN.md`.
- `bande.png` : toutes les images côte à côte (×1 et agrandi).
- `oignon.png` : chaque image sur la précédente en transparence.
- `anim.gif` : aux vraies durées, agrandi ×4 (sans lissage).
- `pieces/` : une pièce par fichier (`corps.txt`, `avant_bras_fXX.txt`…), voir E6-E.
- `ebauche.gif` : les clés en silhouette avec leurs durées, validé avant le pipeline (E7-A).
- `planche_sprites.png` : cellules de taille fixe, pivot au même pixel (E8-A).

## E5. Contrôles

**A. Par image (avant de passer à la suivante)**
- [ ] Les 5 étapes existent (`.txt` + `.png`) et ont été regardées.
- [ ] Contour fermé, pas de pixel doublé en L, pas de pixel de bruit.
- [ ] Lumière en haut à gauche sur **chaque** pièce, même déplacée.
- [ ] Volume des pièces rigides inchangé (compte des pixels) ou changement voulu noté.
- [ ] La silhouette correspond au rôle prévu dans la feuille de timing.

**B. Sur la séquence**
- [ ] Bande : les clés se lisent seules ; l'espacement suit le plan (serré aux clés).
- [ ] Pelure d'oignon : pas de « respiration » parasite, arcs respectés.
- [ ] GIF aux vraies durées, regardé au moins 3 fois en boucle et une fois à ×1.
- [ ] Anticipation présente, dépassement et retour présents, chevauchement des pièces
      souples présent.
- [ ] Une seule action principale par instant ; l'action secondaire ne la cache pas.
- [ ] Pas de jumeaux : les deux côtés diffèrent d'au moins une image ou d'un pixel
      d'amplitude.
- [ ] Au moins un défaut noté, corrigé à son étape, bande refaite.
- [ ] Calques nommés et dans l'ordre fixe (E6-B) ; `ref` et `pivot` non exportés.
- [ ] Pivot au même pixel dans toutes les images ; aucune image recadrée seule (E8-A).
- [ ] Taille de cellule GBA autorisée, objets OAM comptés, 16 couleurs respectées (E8-B).

**C. Leçons du premier essai (rouleau + joyau) [T15]**
- **Une pièce rigide se redessine entière, jamais décalée ligne par ligne.** Décaler des
  lignes une à une casse sa forme (pendentif « cisaillé » en F07).
- **Construis une image à la fois.** Générer plusieurs images d'un coup saute la validation
  E5-A ; chaque image se termine et se valide avant que la suivante commence.
- **Vérifie à la pelure d'oignon qu'aucune pièce n'apparaît d'un coup.** Une partie qui
  n'existe pas à l'image N et qui est entière à N+1 « saute » : donne-lui un bourgeon (1-2 px)
  à l'image N.
- **Un éclat clair posé sur de l'or clair se voit mal.** Juge-le dans le GIF, ou pose-le
  sur le bord, contre le fond sombre.

## E6. Composition en calques et assemblage [R][T16]

Une animation complexe ne se dessine pas d'un bloc : c'est un **assemblage de pièces**
empilées. Bien découpé, on ne redessine que ce qui bouge, et on corrige une pièce une
seule fois pour toutes les images.

**A. Quoi mettre sur un calque à part**
- **Un calque = une pièce qui bouge seule** (bras avant, arme, cape, tête, médaillon,
  éclats). Ce qui bouge toujours ensemble reste sur le même calque.
- **Ne découpe pas pour rien.** Trop de calques = raccords à vérifier partout. Un buste
  qui ne fait que respirer reste un seul calque.
- **Le trait (line art) sur son calque, les aplats dessous** tant que la pièce n'est pas
  validée. On fusionne seulement à l'étape 05 (détails), quand le contour intérieur doit
  être retouché à la main.
- **Un calque `ref`** (croquis, image source, arc-guide) : verrouillé, jamais exporté.
- **Un calque `pivot`** : 1 pixel de couleur repère au point d'ancrage (entre les pieds
  pour un personnage debout, au centre pour un objet qui tourne). Il ne bouge **jamais** ;
  on déplace les pièces par rapport à lui. Jamais exporté.

**B. Ordre d'empilement fixe (de l'arrière vers l'avant)**

| Rang | Calque | Contenu |
|---|---|---|
| 1 | `ref` | croquis, arc-guide (masqué à l'export) |
| 2 | `ombre` | ombre portée au sol |
| 3 | `arriere_*` | membres et pièces du côté loin (plus sombres, A-ombrage) |
| 4 | `corps` | tronc, tête |
| 5 | `avant_*` | membres et pièces du côté proche, arme tenue |
| 6 | `fx` | fumée, traînées, poussière (« tout droit ») |
| 7 | `eclat` | éclats, flash, lueur émissive |
| 8 | `pivot` | point d'ancrage (masqué à l'export) |

- **Nomme chaque calque** (`avant_bras`, `arriere_jambe`, pas « Calque 7 »). **Groupe**
  les calques d'un même ensemble (groupe `perso`, groupe `fx`).
- **Une pièce qui passe devant puis derrière** (bras qui fait le tour, épée qui tourne) :
  **deux calques** (`arme_avant`, `arme_arriere`), on vide l'un quand l'autre est rempli.
  On ne change jamais l'ordre des calques au milieu d'une animation.

**C. Cels liés et duplication**
- **Cel lié** (linked cel, Aseprite) : une pièce immobile pointe vers **un seul dessin**
  partagé par plusieurs images. Une retouche s'applique partout. Utilise-le pour le décor,
  le corps pendant que seul le bras bouge, un cadre d'UI.
- **Délie avant de modifier une seule image.** Sinon la retouche contamine toute la suite.
- **Duplique l'image validée précédente, puis ne touche que la pièce qui bouge** (E0-6).
  Les autres calques restent liés.

**D. Assembler une image**
1. Pose les cels fixes (liés).
2. Place la pièce mobile par rapport au **pivot** (déplacement compté en pixels, noté
   dans la feuille de timing).
3. **Redessine la pièce si elle change d'angle** (rotation, raccourci) : on ne déplace
   jamais un dessin qui devrait tourner (voir E7-D).
4. **Vérifie les raccords** (épaule/bras, poignet/arme) : pas de trou, pas de contour
   doublé. Un raccord se retouche **sur le calque de la pièce mobile**, jamais sur le
   corps lié.
5. Re-place la lumière en haut à gauche sur la pièce déplacée (E2-F).
6. Ajoute les effets sur `fx`/`eclat` en dernier.

**E. Avec nos outils texte**
- Une pièce = un fichier `piece_nom.txt` (`.` = transparent). L'image se compose par
  `stamp` successifs dans l'ordre du tableau B (le dernier tamponné passe devant) :
  ```
  stamp ombre.txt 10 30
  stamp arriere_bras.txt 14 12
  stamp corps.txt 12 8
  stamp avant_bras_f04.txt 18 13
  ```
- Le fichier `cXX_0N.txt` de chaque image est **la liste des calques et leurs positions** :
  c'est notre équivalent des cels liés (on réutilise le même `corps.txt`).

## E7. Flux de travail pro [R][T16]

**A. Ébauche d'abord, propre ensuite** (blocking)
- Dessine les **clés en silhouette grossière** (aplat d'une couleur) et règle leurs
  **durées** dans un GIF **avant** tout nettoyage. Si le mouvement ne marche pas en
  silhouette, aucun détail ne le sauvera.
- Ajoute les passages et intervalles en silhouette, revalide le GIF, **puis** seulement
  passe chaque image dans le pipeline 01-05.
- **Peu d'images fortes valent mieux que beaucoup d'images molles.** Un sprite de jeu
  vise **8 à 12 images/s** ; un cycle de 4 à 8 images suffit le plus souvent.

**B. Pelure d'oignon bien réglée**
- **1 à 2 images avant et après**, pas plus (au-delà, on ne voit plus rien).
- Couleurs distinctes pour avant (rouge) et après (bleu), opacité ~30 %.
- **Limite-la à l'étiquette en cours** (tag) pour ne pas voir la boucle voisine.

**C. Étiquettes et boucles**
- Un fichier par personnage, **une étiquette par boucle** (`idle`, `marche`, `attaque`,
  `degat`), avec son sens de lecture (avant, aller-retour). Chaque étiquette a sa propre
  feuille de timing.
- **Les boucles partagent le même pivot et la même taille de cellule** (E8-A) pour
  s'enchaîner sans saut.

**D. Rotation d'une pièce**
- **Ne tourne jamais un sprite déjà tourné.** Chaque rotation part de **l'original**
  (sinon les erreurs s'additionnent).
- Utilise un algorithme fait pour le pixel art (RotSprite, Clean Rotate), **puis
  nettoie à la main** : contour simple, pas de pixel orphelin, lumière remise en haut à
  gauche.
- Les angles de 90° et 180° sont exacts (miroir/rotation directe) ; 45° demande toujours
  un redessin partiel. **Les petits détails (yeux, boucles, gemmes) se redessinent**, ils
  ne survivent pas à la rotation.

**E. Cycle de marche**
- Quatre poses de base par pas : **contact** (talon au sol, jambes écartées), **descente**
  (corps au plus bas, genou plié), **passage** (jambe libre croise l'autre), **montée**
  (corps au plus haut). Deux pas = un cycle (8 images, ou 4 en version courte).
- Le corps monte et descend de **1 px** ; les bras sont **opposés** aux jambes et en
  retard d'une image (chevauchement).
- Rythme indicatif : **2 pas par seconde** (≈ 8 images × 60-70 ms).

**F. Attaque et impact**
1. **Préparation** (windup) : **2 images ou plus**, l'arme part en arrière, le corps se
   ramasse. Plus elle est longue, plus le coup paraît lourd.
2. **Action** : **1 image de smear** (2 au grand maximum), le geste entier tient dans la
   traînée.
3. **Impact** : l'image la plus forte. **Image d'impact** (formes simplifiées, contraste
   maximal) réservée aux coups puissants, 1 image.
4. **Flash** sur la cible : silhouette blanche (ou couleur claire de palette) pendant
   ~**2 images** (≈ 33 ms), **~4 pour un coup critique**.
5. **Arrêt sur image** (hitstop) : on fige attaquant et cible quelques images.
   **Varie-le selon le coup** (petit coup ≈ 50 ms, coup lourd ≈ 100-150 ms) : un arrêt
   identique partout devient mécanique.
6. **Récupération** : retour lent à la garde (2-3 images plus longues), cape et cheveux
   finissent après (chevauchement).

**G. Effets : fumée, explosion, poussière**
- Couleur : **du clair au sombre et vers le gris** au fil des images (chaud et vif au
  départ, désaturé à la fin).
- Forme : la masse **se fragmente**, les morceaux prennent **chacun leur trajectoire**,
  ralentissent et rétrécissent.
- Disparition : **on efface par morceaux** (trous qui grandissent), jamais en fondu ni
  d'un coup.
- Une explosion part d'un **flash blanc d'une image**, puis boule de feu, puis fumée qui
  monte.
- Toujours sur `fx`, dessiné « tout droit » (E0-4), avec la même règle d'éclat unique.

**H. Cycle de palette** (palette cycling)
- Pour l'eau, la lave, une lueur, un portail : on dessine **une seule image** avec une
  rampe de 3-6 indices, puis on **fait tourner les couleurs** de ces indices à chaque
  image. Mouvement gratuit, aucun pixel redessiné.
- Sur GBA, c'est une simple réécriture de la palette (16 couleurs) : idéal pour l'UI et
  les décors.

## E8. Export et contraintes GBA [R][T16]

**A. Planche de sprites** (sprite sheet)
- **Une seule taille de cellule pour toute l'animation**, prise sur **la plus grande
  boîte englobante** de toutes les images (dépassement et smear compris). **Ne recadre
  jamais une image seule** : le personnage « sauterait ».
- **Même pivot, au même pixel, dans chaque cellule.** La boîte de collision (hitbox) est
  définie **par rapport au pivot**, pas au coin de l'image.
- Export en **filtre au plus proche** (nearest), PNG sans perte, indexé.

**B. Tailles d'objet GBA** (OAM)
- La GBA affiche **128 objets** (OBJ) au maximum. Un objet n'a que ces tailles :

| Forme | Tailles |
|---|---|
| carré | 8×8, 16×16, 32×32, 64×64 |
| large | 16×8, 32×8, 32×16, 64×32 |
| haut | 8×16, 8×32, 16×32, 32×64 |

- Un sprite est fait de **tuiles 8×8** (mode de rangement 1D conseillé).
- **Choisis la taille de cellule d'après ce tableau** (ex. 32×32, 64×64) au moment de la
  feuille de timing, pas après.
- Une pièce plus grande se compose de **plusieurs objets** (métasprite) : chaque image
  coûte alors plusieurs entrées OAM. Compte-les.
- **Réutilise les tuiles identiques** entre images (corps lié, E6-C) : moins de mémoire
  vidéo.
- **16 couleurs par palette d'objet** (dont la transparence) : toute l'animation, effets
  compris, tient dans cette palette, ou les effets prennent une palette à part.
- Durées : **multiples de 16,7 ms** (une trame à 60 Hz), voir E2-A.

---

# Partie F — Décors, tuiles et scènes [B1][B2][R]

Les parties B et C dessinent un sujet seul. La partie F dessine **le monde où il vit** : les
tuiles qui se répètent, les fonds qui défilent, la scène entière. La règle de fond : **le
décor sert le joueur**. Un décor superbe qui cache le personnage ou un piège est raté.

## F0. Intention
Avant la première tuile, écrire :
- la **vue** (A9) et la **taille de tuile** (8, 16 ou 32 px ; la plus courante est 16) ;
- les **plans** : jouable (sol, murs, plateformes), décor de premier plan, fonds ;
- ce que le joueur doit **lire en un coup d'œil** : où marcher, où ça fait mal, où ça
  s'ouvre ;
- la **palette du lieu** (F4), décidée avant de dessiner, à côté de celle des personnages.

## F1. La hiérarchie de lecture d'une scène
Du plus contrasté au plus calme :
1. **Le personnage et les dangers** : le plus fort contraste et les couleurs les plus saturées
   du jeu. Rien dans le décor n'a le droit d'être plus voyant.
2. **Le plan jouable** (sol, murs, plateformes) : contraste moyen-fort, bords nets. Le
   dessus d'une plateforme se lit comme « on peut marcher ici » (bord clair, F2-D).
3. **Le premier plan décoratif** : sombre, peu détaillé, il ne passe **jamais** devant le
   personnage ni devant un piège.
4. **Les fonds** : de plus en plus clairs, désaturés et peu contrastés à mesure qu'ils
   s'éloignent (F3).

**Test** : passer la scène en gris (A6-J). Le personnage et les dangers doivent ressortir
en premier, le plan jouable ensuite. Si le fond attire l'œil avant le sol, le fond est trop
contrasté.

## F2. Tuiles [B2][R]

### A. Règles d'une tuile
- **Sans couture** : posée à côté d'elle-même, on ne voit ni le bord ni la jointure. Vérifier
  sur une grille 3×3 de la même tuile (mode tuilé d'Aseprite).
- **Pas de sujet unique qui remplit la tuile** : une grosse pierre au centre trahit la
  répétition au premier regard. Préférer des petits éléments répartis et décentrés.
- **Contraste interne faible** : un motif à fort contraste forme une grille visible. La
  texture d'une tuile de sol reste **dans 2 ou 3 tons voisins**.
- **Clusters cohérents** : les taches de texture ont des tailles proches dans toute la tuile
  (pas un amas de 6 px à côté de pixels isolés).
- **Lumière commune** : toutes les tuiles du jeu ont la même lumière (haut-gauche, règle 23).
  Le bord haut d'un bloc s'éclaire, le bas s'assombrit.
- **Le bas d'une tuile de mur est plus sombre** que le haut : ça pose la tuile au sol et
  éloigne le mur.

### B. Casser la répétition
- **Variantes** : pour une tuile qu'on aligne souvent (sol, mur), dessiner **1 à 3
  variantes** de même fonction, issues de la première par petites retouches. Une seule
  variante suffit souvent.
- **Décors posés par-dessus** (« decals ») : touffe d'herbe, fissure, caillou, flaque, posés
  sur un calque à part et placés à la main, pas sur chaque tuile.
- **Hors grille** : un élément qui chevauche deux tuiles (racine, gros rocher, lierre) casse
  la grille mieux que dix variantes.
- **Vérifier dézoomé** : garder une fenêtre de prévisualisation de la carte à ×1 pendant le
  dessin. La répétition se voit de loin, pas de près.

### C. Autotiles : blob 47 et Wang 16 [R]
Pour que les bords se posent seuls (sol qui s'arrondit, mur qui tourne), on dessine un jeu de
tuiles de transition.
| Système | Tuiles | Pour |
|---|---|---|
| **Wang 16 (coins)** | 16 | terrains vus de dessus : herbe/terre, eau/sable |
| **Blob 47 (coins + côtés)** | 47 | murs, plateformes, falaises, chemins d'1 tuile de large |

- **On ne dessine pas 47 tuiles**, on dessine **4 pièces** : coin extérieur, coin intérieur,
  bord droit, remplissage. Les 47 tuiles en sont des assemblages.
- **Un carré qui dépasse à chaque coin rentrant** = il manque la tuile de coin intérieur, pas
  un bug de code.
- **Commencer par un gabarit grossier** de toutes les tuiles et de leurs raccords, le tester
  sur une petite carte, puis seulement ajouter texture, ombres et lumière.
- Godot : `TileSet`, terrain en mode **« Match Corners and Sides »** pour le blob 47,
  « Match Corners » pour le Wang 16. Tiled : jeu de Wang de type « Mixed ».

### D. Plateformes de profil [R]
- **Le dessus (la « croûte »)** : 2 à 4 px d'une matière plus claire (herbe, mousse, neige,
  bord de pierre éclairé) qui dit « surface praticable ». Sa forme peut déborder un peu sur
  la face.
- **La face** : plus sombre, texture calme, s'assombrit vers le bas.
- **Les bords** : arrondis ou cassés, jamais un rectangle parfait ; coin haut éclairé.
- **Même hauteur de croûte partout** : c'est elle qui apprend au joueur où sont les sols.

### E. Tuiles vues de dessus (3/4) [R]
- **Sol** : texture la plus calme du jeu, car il occupe le plus de surface.
- **Murs** : on voit leur face avant (plus sombre) et leur dessus (plus clair). La face a
  une hauteur fixe dans tout le jeu (souvent 1 tuile).
- **Herbe et chemins** : transition en Wang 16 ; le bord de l'herbe déborde en touffes
  irrégulières sur la terre.
- **Ombre portée** des murs et des objets vers le bas-droite (lumière haut-gauche), sur 1 à
  3 px, dans un ton plus sombre et plus froid du sol.

## F3. Fonds et parallaxe [R]

### A. Perspective atmosphérique
Chaque plan qui s'éloigne :
- **perd de la saturation** (environ −20) ;
- **perd du contraste** (environ −15) ;
- **gagne de la luminosité** (environ +15) ;
- **glisse vers la teinte du ciel** en extérieur (bleu le jour, orange au couchant, violet la
  nuit) ; en **intérieur**, il **s'assombrit** au lieu de s'éclaircir.

Ces chiffres sont des points de départ à régler à l'œil. Ce qui compte : **chaque plan est
distinct du suivant en valeur**.

- **Moins de détails au loin** : un arbre lointain est une silhouette à 1 ou 2 tons ; un arbre
  proche a son feuillage en clusters.
- **Pas de contour sur les fonds** (ou un contour à peine plus sombre) : le contour est
  réservé à ce qui se joue.
- **Jamais sombre sur sombre** : un personnage sombre a un fond moyen ou clair derrière lui.

### B. Parallaxe
- **Facteur de défilement** : 0 = fixe (ciel, soleil), 1 = avance avec le monde (plan
  jouable), entre 0 et 1 = lointain, plus de 1 = premier plan.
- **2 à 4 couches suffisent.** Plus de couches, avec des éléments animés partout, fatigue
  l'œil et brouille la lecture.
- **Défilement au pixel près** : la couche la plus lointaine avance de 1 px par pas, chaque
  couche plus proche du nombre entier suivant. Des vitesses fractionnaires font trembler les
  pixels.
- **Chaque couche boucle** : sa largeur est un multiple de la largeur d'écran, et ses bords
  gauche et droit se raccordent (même test qu'une tuile, F2-A).
- **Le bas de chaque couche se cache** derrière la couche plus proche : pas de bord droit
  visible.

### C. Mise à l'échelle
- **Agrandir seulement par un entier** (×2, ×3, ×4). Un facteur de 2,5 rééchantillonne et
  rend les pixels de taille inégale.
- **Une seule taille de pixel par scène** : ne jamais mélanger un sprite agrandi ×2 et un
  décor à ×1 (« mixels »). Tout est dessiné à la même résolution.

## F4. Palette d'un lieu [B1][B5][R]
- **Une palette par lieu**, construite comme une famille : 3 à 5 rampes qui partagent leurs
  tons sombres (A6-A, rampes partagées).
- **Masque de gamme** [B5] : avant de choisir les couleurs d'un lieu, limiter la gamme à une
  zone de la roue chromatique (un triangle ou une forme). Toutes les couleurs du lieu en
  viennent : l'ambiance devient cohérente d'elle-même.
- **Les couleurs du personnage sont hors de la gamme du décor**, ou au moins plus saturées :
  il ressort sans contour forcé.
- **Couleur de la lumière** : elle teinte tout le lieu (soleil chaud, lune froide, torche
  orange). Les ombres prennent la couleur complémentaire, en plus doux.
- **Tester les personnages sur chaque palette de lieu** avant de valider le lieu (A6-J,
  « en situation »).

## F5. Composition d'une scène fixe (illustration, écran titre) [R]
- **Un seul point focal**, placé hors du centre (tiers de l'image) : le plus fort contraste,
  la couleur la plus saturée et le plus de détails y vont (A2, budget de contraste).
- **Trois plans de valeur** : premier plan sombre, plan moyen avec le sujet, fond clair. On
  doit lire la scène en 3 taches de gris.
- **Des lignes qui mènent** au point focal : chemin, rivière, rayon de lumière, regard d'un
  personnage.
- **Repos** : des zones calmes (ciel, mur nu) autour du point focal. Partout du détail =
  rien ne ressort.
- **Taille d'abord, pixels ensuite** : esquisser la composition en 3 tons sur un canevas
  réduit, la valider, puis seulement dessiner à la taille finale.

## F6. Contrôle propre aux décors
| Test | Comment | Ce qu'on doit voir |
|---|---|---|
| **Grille 3×3** | une tuile répétée 9 fois | aucune couture, aucune grille visible |
| **Carte dézoomée** | 20×12 tuiles à ×1 | pas de motif qui se répète en diagonale ou en rangée |
| **Gris** | la scène en gris | personnage et dangers d'abord, sol ensuite, fond en dernier |
| **Personnage posé** | le sprite sur chaque fond | il se lit sans liseré ; jamais sombre sur sombre |
| **Défilement** | GIF de la parallaxe | pas de tremblement, pas de couture à la boucle |
| **Autotile** | une forme en U, en L et en île | aucun carré de coin rentrant, aucun bord cassé |
| **Premier plan** | le jeu en mouvement | aucun élément de premier plan ne cache un piège |

---

# Partie G — Progresser : de débutant à pro [B][R]

Ce que disent les livres et les artistes sur la manière d'apprendre, traduit en plan de
travail.

## G0. Principes
- **Régularité plutôt qu'intensité** : 30 minutes par jour valent mieux que 5 heures le
  dimanche. Viser les **150 premières heures** le plus vite possible : c'est là que les bases
  deviennent des réflexes.
- **Petit d'abord** : maîtriser 8, 16 puis 32 px avant d'attaquer 64 et plus. À petite
  taille, chaque erreur se voit, et un dessin se finit en une séance.
- **Dessiner à la taille finale**, jamais en grand puis réduit (A4b).
- **Contraintes volontaires** : 4 couleurs, puis 8, puis 16. Une palette imposée (Lospec)
  force à travailler la valeur au lieu d'ajouter des couleurs.
- **Finir** : un dessin fini et imparfait apprend plus que trois dessins abandonnés.
- **Le dessin classique compte** : construction, anatomie, perspective, lumière (Loomis,
  Gurney, parties A4 et C9). Le pixel art ne remplace pas le dessin, il le contraint.

## G1. Le plan en quatre paliers
| Palier | Objectif | Exercices | Fini quand |
|---|---|---|---|
| **1. Le pixel** | lignes et formes propres | pentes 1:1, 2:1, 3:1 sans jaggies ; cercles de 8, 16, 32 px ; 10 objets 16×16 en 4 couleurs (A8) | une courbe propre du premier coup |
| **2. La lumière** | volume et valeur | sphère, cube, cylindre, cône sous une lumière haut-gauche, en 3 puis 5 tons ; même objet en pierre, métal, bois, tissu (A5-8b) | les volumes se lisent en gris |
| **3. Le sujet** | personnages, créatures, objets | un personnage 32 px en 4 directions ; une créature par langage de formes (C15-A) ; la même icône en 16, 32, 64 (B4b) | le sujet se reconnaît en silhouette |
| **4. Le monde** | décor, animation, scène | un tileset 16 px avec autotile (F2) ; un cycle de marche (E7) ; une scène en 3 plans avec parallaxe (F3) | un écran de jeu complet et lisible |

À chaque palier, appliquer toute la méthode (règles impératives, planche, sept défauts).

## G2. Étudier les maîtres (la copie d'étude) [B3][B4][R]
1. **Choisir** une pièce d'un artiste reconnu, de la taille du palier en cours.
2. **Analyser avant de copier** : compter les couleurs, noter la rampe, la direction de la
   lumière, où sont le contour, le selout, l'AA, le tramage. Écrire ces observations.
3. **Recopier pixel par pixel**, à côté de l'original.
4. **Refaire de mémoire**, sans l'original, puis comparer.
5. **Réutiliser** une seule technique apprise dans un dessin à soi, dans la semaine.

Les copies restent des exercices privés : on ne les publie pas comme son propre travail, et
on cite l'artiste d'origine si on les montre.

## G3. Retours et critique
- **Montrer tôt** : un retour sur une ébauche coûte moins cher qu'un retour sur un dessin fini.
- **Demander une chose précise** (« la lumière se lit-elle ? »), pas « c'est bien ? ».
- **Faire l'« edit »** : un artiste plus avancé retouche le dessin ; comparer avant et après,
  pixel par pixel, est la leçon la plus rapide qui existe.
- **Se critiquer soi-même avec la planche** (A6-J) avant de demander l'avis des autres.
- **Relire ses anciens dessins** tous les mois : les défauts qu'on voit maintenant mesurent le
  progrès.

## G4. Devenir pro (pour le jeu vidéo)
- **Un portfolio court et ciblé** : 6 à 10 pièces finies du type de travail visé (sprites
  animés, tilesets, scènes). Les pièces faibles retirent de la valeur.
- **Montrer en situation** : un sprite sur un décor, une animation en GIF aux vraies durées,
  un tileset monté en carte. Un studio veut voir que ça marche **dans un jeu**.
- **Un style cohérent sur un projet** : savoir tenir la même palette, la même lumière et la
  même taille de pixel sur des dizaines de pièces (A4, cohérence).
- **Savoir livrer** : planches de sprites alignées, pivot fixe, noms de fichiers propres,
  contraintes de la machine (E8). C'est ce qui distingue l'illustrateur du pixel artiste de
  jeu.
- **Les game jams** : un jeu fini en 48 h apprend la vitesse, le compromis et la lisibilité
  en jeu mieux que des semaines de dessins isolés.

---

# Résumé

**Tout dessin (partie 0) :** vision écrite et corrigée au carnet → au moins trois
vignettes, choix écrit → niveau visé (œuvre pro) → construction à travers (primitives
entières, ellipses) → trait → aplats de couleur locale → lumière posée, deux familles
(Notan) → modelé (demi-ton, ombre propre, rebond, occlusion, ombre portée) → matière →
éclats et contour coloré → contre-jour → variation de couleur → détails → planche avec
comparaison côte à côte.

**Objet :** intention, usage et projection → cadre (diagonale pour les objets longs) →
volumes et terminateur → simplification (A4b) → forme iconique → silhouette → contour →
palette → lumière selon la matière → variation de couleur → détails → nettoyage → contrôle
en situation.

**Personnage :** intention et références → proportions → pose → volumes → visage construit
(C12) → vêtements → cheveux (C6) → table par taille (C10) → (portrait anime : C11) →
silhouette → contour → palette → ombres à la main → détails → nettoyage → contrôle avec la
référence.

**Chibi (C13 + C14) :** croquis rouge (pose) → repères bleus → volumes verts → **corps nu**
(silhouette, jointures, pas d'épaule marquée, ombres) → **validation du corps** →
vêtements en calque (aplats 1 px hors du corps, ombres, plis, contour du calque, bords
intérieurs à la main) → visage → cheveux en calque → accessoires → nettoyage → planche.

**Créature (C15) :** langage de formes (rond / triangle / carré) et 2–3 marqueurs →
construction R/B/G → silhouette refaite tant qu'elle forme un bloc → contour → volumes
(pattes lointaines plus sombres, émissifs à ombrage inversé) → bords intérieurs à la main →
yeux selon le langage → selout → planche.

**Créature complexe (C16) :** silhouette assemblée de pièces (os, robe, rochers) → cavités
sombres d'abord → asymétrie (bras levé, armure) → parties flottantes séparées par du vide →
bords intérieurs à la main → un seul accent émissif → planche.

**Vêtement (C17) :** appuis et tensions → poids du tissu → silhouette → aplat 1 px hors
du corps → ombre et AO → 1-3 plis depuis les tensions (ombre + lumière, pas de trait) →
lumière selon la matière → motif qui suit la forme → contour du calque → détails.

**Finition pro (A6) :** rampes à teinte tournante → budget de couleurs → une seule lumière,
terminateur net → AO dans les creux → lumière réfléchie → selout → AA seulement sur les
courbes dures → chasse aux sept défauts → tests de la planche.

**Animation (E) :** intention et durée → poses de départ et d'arrivée finies → feuille de
timing (taille de cellule GBA, pivot) → découpe en calques (E6) → ébauche des clés en
silhouette et GIF (E7-A) → pour chaque image : pipeline 01-05 et validation → effets sur
`fx` → bande, pelure d'oignon, GIF → planche de sprites (E8).

**Tuile et décor (F) :** vue et taille de tuile → hiérarchie de lecture (personnage et
dangers en tête) → palette du lieu (masque de gamme) → gabarit grossier des tuiles et de
leurs raccords → test sur une petite carte → texture calme, lumière commune → variantes et
décors posés → autotile (4 pièces → 47 tuiles) → fonds en 2 à 4 couches, de plus en plus
clairs et désaturés → parallaxe au pixel près → contrôle F6.

**Objet en 9 étapes (B6) :** primitive → déformer et séparer les pièces → trait propre et
aplats → ombrage de base (un ton par face) → ombres et lumières secondaires → éclats et
contour coloré → contre-jour d'une autre teinte → glissement de teinte → détails (fissures
à lèvre claire, trous, halo, étincelles, ombre portée) et nettoyage.

**Tramage (A7) :** les trois conditions → limite seulement, entre tons voisins → rampe
25 / 50 / 75 % → un seul style par image → contrôle à ×1.

**Geste du pro (A10, A11) :** valeur avant teinte → peu d'idées fortes → le bon outil par
forme → un trait décidé → ×1 après chaque trait → miroir et gris à chaque étape → yeux
plissés et palette seule avant la finition → pause avant la planche.

**Progresser (G) :** 30 min par jour → paliers pixel, lumière, sujet, monde → une copie
d'étude entre deux projets → retours précis et « edits » → portfolio court, en situation.

Un concept à la fois, du grand au petit. Aucun pixel de détail tant que la structure n'est
pas juste.

---

# Livres de référence [B]

Ce que disent les livres sur le pixel art, et où leurs principes entrent dans cette méthode.
Les contenus sont résumés d'après les sommaires, présentations des éditeurs et critiques
publiques, puis reformulés. Pour le détail et les images, lire les livres eux-mêmes (version
officielle : sites des auteurs et des éditeurs, voir les sources).

| Étiquette | Livre | Pour quoi |
|---|---|---|
| **[B1]** | *Pixel Logic — A Guide to Pixel Art*, Michael Azzi (2019, éd. 2022, 242 p.) | la référence la plus complète sur la technique pure |
| **[B2]** | *Pixel Art for Game Developers*, Daniel Silber (CRC Press, 2015, 256 p.) | le pixel art pensé pour un jeu : tuiles, fonds, erreurs fréquentes |
| **[B3]** | *Make Your Own Pixel Art*, Jennifer Dawe et Matthew Humphries (No Starch Press, 2019, 200 p.) | l'apprentissage pas à pas, du premier pixel à l'animation |
| **[B4]** | Livres d'images : *The Unofficial Game Boy Advance Pixel Book* (Bitmap Books), *Pixelscapes* (Waneella), *The Masters of Pixel Art* | matière pour les copies d'étude (G2) |
| **[B5]** | *Color and Light*, James Gurney (2010) | couleur et lumière pour peintres, cité par les pixel artists (masque de gamme) |
| **[B6]** | Livres japonais et livres d'artistes (détail ci-dessous) | méthode des décors, copies d'étude, maîtres (A10) |
| Déjà cités | Loomis [L] ; Thomas et Johnston, *The Illusion of Life* (partie E) | construction du visage ; principes d'animation |

## [B1] Pixel Logic (Michael Azzi)
Un livre très visuel, une leçon par double page, organisé du trait au mouvement :
| Chapitre | Principe retenu | Où dans la méthode |
|---|---|---|
| 1. Le trait | lignes et courbes lisses ; marches régulières ; penser la ligne comme un vecteur avant de la pixeliser | A5-6, A6-D, **A8** |
| 2. Anticrénelage | AA seulement là où l'escalier est dur ; sa longueur suit la marche ; jamais sur une pente propre | A5-10, A6-F |
| 3. Couleurs | rampes à teinte tournante ; palettes pour sprites **et** pour décors | A6-A, **F4** |
| 4. Lisibilité | petit ou grand sprite : la silhouette et la valeur d'abord, un détail qui ne se lit pas est supprimé | A2, A3, A4b |
| 5. Tramage | dégradés tramés, surtout pour les fonds | **A7** |
| 6. Perspectives de jeu | profil, dessus, 3/4, isométrique 2:1 | B0b, **A9** |
| 7. Nettoyage | pixels orphelins ; banding parallèle, banding de tramage, banding d'AA | A6-H, **A7-C** |
| 8. Sous-pixel | décaler un bord de moins d'1 px par un ton intermédiaire, sur une image fixe ou animée | E2-D, **A8** |
| 9. Animation | timing, images clés, boucles | partie E |

Limite signalée par les critiques : peu de gestion fine de la couleur et des contraintes
matérielles. La méthode les couvre ailleurs (A6-A, E8).

## [B2] Pixel Art for Game Developers (Daniel Silber)
Écrit pour les développeurs qui dessinent leur propre jeu. Principes retenus :
- **Principes universels d'abord** : forme, valeur, lumière et ombre avant toute technique pixel
  (A2, A5-8).
- **Tuiles de fond** : une tuile qui contient un seul gros sujet trahit la répétition ; un
  motif trop contrasté aussi ; découper le décor en tranches réutilisables va plus vite et
  reste cohérent ; transitions d'herbe en 3 tuiles ; ranger le tileset pour l'éditeur de
  niveaux (**F2**).
- **Erreurs fréquentes** (chapitre dédié) : **banding** et « super pixels » (gros blocs carrés
  qui trahissent un dessin agrandi), **trop d'AA**, **trait de mauvaise qualité**, **palette
  faible**, **trop de complexité**, **ombrage « flash »** (lumière de face qui écrase le
  volume), **pas de texture**. Le tableau A6-H est complété en conséquence.

## [B3] Make Your Own Pixel Art (Dawe et Humphries)
Un livre d'initiation progressif. Principes retenus :
- **Outils** : un vrai logiciel de pixel art (Aseprite, Pro Motion, GraphicsGale), avec
  palette indexée, mode tuilé et pelure d'oignon.
- **Sculpter** : poser la masse en aplat, puis la creuser et l'ajouter pixel par pixel, comme
  une pâte (A8, formes avant lignes).
- **Ombrer, texturer, colorer** : dans cet ordre, sur des formes simples avant les sujets.
- **Émotion et mouvement** : une pose et une expression valent plus que des détails (C2,
  C10-E).
- **Esquisser d'abord** : petit croquis rapide avant le dessin final (F5, R7).
- **Et après** : continuer par la pratique quotidienne, les communautés et le partage (**G**).

## [B4] Livres d'images (étude)
Pas des cours, mais des **sources de copies d'étude** (G2) : pages de sprites GBA, scènes
d'artistes reconnus. On les lit avec la grille d'analyse de G2-2 (couleurs, rampes, lumière,
contour, tramage).

## [B5] Color and Light (James Gurney)
Un livre de peinture réaliste, dense et avancé. Ce que les pixel artists en retiennent :
- **Masque de gamme** : choisir une zone limitée de la roue des couleurs pour une image,
  pour une harmonie immédiate (F4).
- **La lumière a une couleur**, et l'ombre prend la couleur de ce qui l'éclaire indirectement
  (A6-E, lumière réfléchie).
- **La couleur est relative** : un ton paraît chaud ou froid, clair ou sombre selon ses
  voisins. On juge une couleur **en place**, jamais seule dans le sélecteur.

## [B6] Livres japonais et livres d'artistes
Résumés d'après les présentations des éditeurs. Ils servent aux copies d'étude (G2) et aux
leçons des maîtres (A10).

| Livre | Ce que c'est | Pour quoi |
|---|---|---|
| *ULTIMATE PIXEL CREW REPORT ピクセルアートではじめる背景の描き方* (Born Digital) | méthode de décor en pixel art : bases, making-of, composition, concept | décors et scènes (F1, F5) |
| *NEW PIXEL ART* (APO+, 33 artistes) | recueil d'artistes japonais d'aujourd'hui, avec leur façon de faire | copies d'étude, styles variés |
| *ゲームドット絵の匠* (Home-sha, 2018) | entretiens avec des pixel artists de jeux japonais classiques | métier, contraintes de machine (A10-A) |
| *Pixel Vistas* (Graphic-sha) | recueil de paysages en pixel art | décors, lumière d'un lieu (F4) |
| *水と手と目* Toyoi Yuuta (Graphic-sha, ISBN 978-4-7661-3746-0) | recueil d'illustrations, **pas** un manuel | copies d'étude, animation légère (A10-E) |
| *FF DOT: The Pixel Art of Final Fantasy* (Dark Horse) | les sprites des *Final Fantasy* classiques, dont ceux de Kazuko Shibuya | petits personnages, identité en peu de pixels (A10-A) |
| *Pixelscapes*, Waneella (Thames & Hudson) | scènes de ville animées | grandes formes puis détails, boucles (A10-E) |
| *Arcade Game Typography*, Toshi Omagari (Thames & Hudson) | les polices des jeux d'arcade, lettre par lettre | lettrage en pixels, interface |

Les livres s'achètent chez l'éditeur ou en librairie. Pas de copies piratées.

---

## [D] Fondamentaux du dessin et de la peinture (v17)
Cours et livres légitimes, cités pour leurs idées ; tout est reformulé.

| Étiquette | Source | Ce qu'on en prend |
|---|---|---|
| [D1] | [Drawabox, leçon 1 (ghosting)](https://drawabox.com/lesson/1/14/arc) · [leçon 2 (construction)](https://www.drawabox.com/lesson/2/3) | dessiner à travers, contours croisés, trait préparé (0-B) |
| [D2] | Scott Robertson et Thomas Bertling, *How to Draw* et *How to Render* (Design Studio Press) | perspective, ellipses, matières et réflexion (0-F, 0-I) |
| [D3] | [Proko, éléments de la lumière et de l'ombre](https://www.proko.com/course-lesson/elements-of-light-and-shadow/notes) · [lumière sur une sphère](https://www.proko.com/lesson/part-1-light-on-a-basic-sphere-and-intro-to-compression) | familles, terminateur, ombre propre, rebond, occlusion, ombre portée (0-C) |
| [D4] | [James Gurney, diffusion sous la surface](https://gurneyjourney.blogspot.com/2008/05/subsurface-scattering-ii.html) · [caustiques](https://gurneyjourney.blogspot.com/2010/07/caustic-reflections.html) · [transparence de l'eau](https://gurneyjourney.blogspot.com/2008/03/transparency-of-water.html) | translucidité, liquides, verre (0-G, 0-I) |
| [D5] | [Marco Bucci, deux valeurs puis trois](https://www.skillshare.com/en/classes/10-minutes-to-better-painting/1173043622) | séparer lumière et ombre, le demi-ton (0-D) |
| [D6] | [Proko, contrôle des valeurs](https://www.proko.com/course-lesson/value-control) · [concevoir des groupes de valeurs](https://www.proko.com/course-lesson/demo-designing-value-groups-level-1) | océans, lacs, rivières ; viser, comparer (0-D, 0-J) |
| [D7] | [Principes de design (grand-moyen-petit, d'après Sinix)](https://mayabeginner.readthedocs.io/en/latest/Design/L3_DesignPrinicplesPrimer.html) | hiérarchie des formes (0-E) |
| [D8] | [Droites et courbes](https://animatedspirit.com/straights-curves) | tension du contour (0-E) |
| [D9] | James Gurney, *Color and Light* (= [B5]) | couleur locale, lumière, ambiante ; saturation au demi-ton (0-G) |
| [D11] | [Proko, vignettes pour le concept art](https://www.proko.com/lesson/how-to-thumbnail-for-concept-art) · [explorer des variantes](https://www.proko.com/lesson/exploring-alternate-concept-designs) · [Concept Art Empire, vignettes (Feng Zhu, Design Cinema 75)](https://conceptartempire.com/intro-to-thumbnail-sketching/) | silhouettes rapides, pousser chaque essai, choisir puis varier (0-N-C) |
| [D12] | [Ctrl+Paint, les vignettes](https://www.ctrlpaint.com/blog/thumbnails-the-most-crucial-stage-of-your-painting) · [itération](https://www.ctrlpaint.com/videos/thumbnail-iteration) | petit et vite, jeter sans regret (0-N-C) |
| [D13] | [Creative Bloq, créatures crédibles](https://www.creativebloq.com/art/digital-art/pro-artists-reveal-how-they-design-imaginary-creatures-that-feel-believable) · [Terryl Whitlatch (ArtStation)](https://magazine.artstation.com/2016/09/profile-creature-design-legend-terryl-whitlatch/) · Terryl Whitlatch, *Science of Creature Design* et *Principles of Creature Design* | squelettes d'animaux réels, récit de la créature (0-N-B) |
| [D14] | [Creative Bloq, conseils de concept design](https://creativebloq.com/how-to/concept-design-tips-for-artists/2) · [The Rookies, design d'objets](https://blog.therookies.co/2019/08/11/prop-design-tips-for-newbie/) | la forme suit la fonction, lisibilité d'un objet (0-N-B) |
| [D15] | [Les grandes formes](https://drawpaintacademy.com/big-simple-shapes-and-colors/) · [langage des formes (21-draw)](https://www.21-draw.com/pl/why-is-shape-language-so-important/) · [rythme et répétition (The Noun Project)](https://blog.thenounproject.com/?p=7993) | grandes formes, économie, langage des formes, rythme (0-O) |
| [D16] | [SCAMPER (UBC Design Studio)](https://dstudio.ubc.ca/toolkit/techniques/scamper/) · [SCAMPER (Interaction Design Foundation)](https://ixdf.org/literature/topics/SCAMPER) · [DelftX, fiche SCAMPER](https://courses.edx.org/c4x/DelftX/DDA691x/asset/DDG_Scamper.pdf) | questionner une forme connue, tableau morphologique (0-P) |
| [D17] | [Proko, dessiner le geste](https://www.proko.com/course-lesson/how-to-draw-gesture/notes) · [Creative Bloq, le geste](https://www.creativebloq.com/art/traditional-art/gesture-drawing) | C, S, droite, ligne d'action, rythme (0-Q) |
| [D18] | [Palettes limitées (Clip Studio)](https://www.clipstudio.net/how-to-draw/archives/168546) · [palettes de couleurs (UNH)](https://it502.cs.unh.edu/tutorials/spring25/jlb1207/color_palettes.html) | dominante, soutien, accent ; analogues et complémentaires (0-R) |
| [D19] | [Creative Bloq, peindre le métal](https://creativebloq.com/3d/paint-different-metal-surfaces-10121080) · [KeyShot, métal brossé](https://www.keyshot.com/blog/how-to-render-brushed-metals-in-keyshot/) · [Muddy Colors, reflets](https://www.muddycolors.com/?p=46120) | chrome, brossé, usé (0-S-A) |
| [D20] | [Slynyrd, texture](https://www.slynyrd.com/blog/2018/2/15/pixelblog-2-texture) · [Slynyrd, arbres vus de dessus](https://slynyrd.com/blog/2023/5/22/pixelblog-44-top-down-trees) · [OpenGameArt, textures et tramage](https://opengameart.org/content/chapter-7-textures-and-dithering) · [Kenney, améliorer un dessin 2D](https://kenney.nl/learn/improving-2d-vector-art) | amas répétés, bois, fourrure suggérée, feuillage (0-S-B) |
| [D21] | [Proko, l'illusion de profondeur](https://www.proko.com/lesson/the-illusion-of-depth-perspective-details-and-overlapping-forms/) · [Proko, 5 astuces pour le volume](https://proko.com/course-lesson/5-tricks-to-make-your-drawings-look-3d) · [Drawabox, boîtes et raccourcis](https://drawabox.com/lesson/1/10) · [le raccourci (Art in Context)](https://artincontext.org/foreshortening/) | diminution, convergence, raccourci, recouvrement ; 1, 2, 3 points (0-T) |
| [D22] | [Line of Action, pattes d'animaux](https://www.line-of-action.com/fr/article/animal-leg-anatomy-cheat-sheet) · [« genoux à l'envers »](https://line-of-action.com/digitrade-animals-dont-have-backward-knees) · [Clip Studio, ailes](https://tips.clip-studio.com/en-us/articles/7950) · [Chris Wilson, ailes d'oiseau](https://chriswilsonstudio.com/how-to-draw-bird-wings/) · [UNL, morphologie des insectes](https://entomology.unl.edu/basic-insect-morphology/) · Ellenberger, Baum et Dittrich, *An Atlas of Animal Anatomy for Artists* | plantigrade, digitigrade, onguligrade ; ailes ; insectes (0-U) |
| [D23] | [Proko, structures simples de la main](https://www.proko.com/course-lesson/simple-structures-of-the-hands) · [David Rickert, grouper les doigts](https://davidrickert.substack.com/p/drawing-hands-3-finger-bundling) | paume en boîte, moufle, pouce, doigts groupés (0-V-A) |
| [D24] | [Clip Studio, visages expressifs](https://www.clipstudio.net/how-to-draw/archives/157239) · [Skillshare, expressions](https://www.skillshare.com/en/blog/how-to-draw-facial-expressions-a-guide/) · [Creative Bloq, un personnage tourmenté](https://www.creativebloq.com/advice/4-top-tips-for-drawing-an-anguished-character) | sourcils, yeux, bouche ; asymétrie ; tout le corps joue (0-V-B/C) |
| [D25] | [Proko, types de sources](https://proko.com/course-lesson/types-of-light-sources/notes) · [Muddy Colors, deux températures](https://www.muddycolors.com/?p=43890) · [Clip Studio, guide de l'éclairage](https://tips.clip-studio.com/en-us/articles/8810) · [Creative Bloq, lumière principale, remplissage, contre-jour](https://www.creativebloq.com/3d/how-to-use-key-fill-and-rim-lighting-in-3d-art) | hiérarchie des lumières, contre-jour, nuit (0-W) |
| [D26] | [Kenney, sprites de particules](https://www.kenney.nl/learn/drawing-particle-effect-sprites) · [Game Developer, explosions en 2D](https://www.gamedeveloper.com/art/2d-game-art-for-programmers-back-with-a-bang-) | fumée en boules, flash bref, débris, étincelles (0-X) |
| [D27] | [80.lv, la stylisation](https://80.lv/articles/stylization-in-video-games-a-deep-dive-analysis/) · [Unity, trouver le style d'un jeu](https://unity.com/blog/game-art-styles-guide) · [RocketBrush, réalisme et stylisation](https://rocketbrush.com/blog/realism-vs-stylization-art-in-games) | simplifier et exagérer exprès, fiche de style (0-Y) |
| [D28] | [Creative Bloq, raconter une histoire en une image](https://creativebloq.com/how-to/tell-a-story-in-an-image) · [Creative Bloq, récit par le décor](https://creativebloq.com/how-to/10-key-techniques-for-creating-environment-art-that-drives-visual-storytelling) · [Clip Studio, récit visuel](https://clipstudio.net/how-to-draw/archives/158243) | point d'intérêt, moment clé, indices (0-Z) |
| [D29] | [Le principe d'appeal (UIC)](https://www.evl.uic.edu/ralph/508S99/appeal.html) · [Animation Mentor, l'appeal](https://www.animationmentor.com/?p=4746) · Thomas et Johnston, *The Illusion of Life* | charme, simplicité, clarté ; ordre et intérêt (0-AA-B) |
| [D30] | [Musée Lalique](https://www.musee-lalique.com/en/?p=1957) · [Lalique, flacons de parfum (Rau Antiques)](https://rauantiques.com/blogs/canvases-carats-and-curiosities/master-of-glass-lalique-perfume-bottles) · [René Lalique, structure et nature](https://runningxlate.substack.com/p/rene-lalique) | la structure tirée de la nature, flacons comme objets d'art (0-AA-C) |
| [D31] | [City Lit, du post-it à l'impression](https://www.citylit.ac.uk/blog/illustration-from-post-it-to-print) · [CUNY, déroulé d'une illustration](https://openlab.citytech.cuny.edu/woolley-comd2313sp2018/files/2018/02/Illustration-Workflow-Handout.pdf) · [Cursa, de l'esquisse au trait (tablette)](https://cursa.app/en/page/digital-drawing-on-a-tablet-sketch-to-line-workflow-that-stays-clear-and-flexible) | vignettes, rough, esquisse affinée, trait, validation (0-AB-A) |
| [D32] | [Clip Studio, un trait vivant](https://www.clipstudio.net/how-to-draw/archives/155333) · [Clip Studio, le trait pour débutants](https://tips.clip-studio.com/en-us/articles/8771) · [Creative Bloq, 20 conseils d'esquisse](https://www.creativebloq.com/illustration/sketching-tips-beginners-81516497/2) · [Pixel Grimoire #7](https://medium.com/pixel-grimoire/how-to-start-making-pixel-art-7-e504bfa4ddf2) | redessiner, baisser l'opacité, retourner la toile, poids du trait, peu de traits en petit (0-AB-B) |
| [D33] | [Clip Studio, améliorer son line art](https://www.clipstudio.net/how-to-draw/archives/163108) · [Cursa, poids, effilés et angles](https://cursa.app/en/page/digital-drawing-on-a-tablet-clean-line-art-techniques-line-weight-tapers-and-corners) · [Proko, Jeff Watts et la qualité du trait](https://www.proko.com/lesson/jeff-watts-on-line-quality) | système de poids, traits décidés, recouvrements, nettoyage (0-AC-B) |
| [D34] | [Core77, poids du trait en design produit](https://core77.com/posts/99154/Sketching-Tutorial-How-To-Use-Line-Weight-In-Your-Sketches-2-Rules-n-2-Techniques) · [The Design Sketchbook, poids du trait](https://www.thedesignsketchbook.com/?p=37086) · [Lospec, contours en pixel art](https://lospec.com/articles/pixel-art-outlines) | trois poids (fin, moyen, fort), traits intérieurs d'un ton plus clair (0-AC-B) |
| [D10] | [Les bords en peinture](https://drawpaintacademy.com/edges/) · [Muddy Colors, bords](https://www.muddycolors.com/?p=8983) | bords durs, doux, perdus (0-H) |

Pour le verre en pixel art : [PixelJoint, transparence d'un verre](https://pixeljoint.com/forum/forum_posts.asp?TID=20953)
(on dessine les reflets extérieurs et la réfraction, pas une vraie transparence) ·
[itch.io, tutoriel potion de soin](https://itch.io/t/2667098/pixel-tutorial-health-potion)
(petits éclats sur la panse et le col).

# Sources web [R]

**Rendu général, couleurs, contour :**
[Derek Yu, bases](https://www.derekyu.com/makegames/pixelart.html)
· [Derek Yu, erreurs fréquentes](https://derekyu.com/makegames/pixelart2.html)
· [Slynyrd, palettes](https://www.slynyrd.com/blog/2018/1/10/pixelblog-1-color-palettes)
· [pixnote, ombrage](https://pixnote.net/en/learn/shading/)
· [pixnote, palette](https://pixnote.net/en/learn/color-palette/)
· [pixnote, selout](https://pixnote.net/en/learn/outlines/)
· [Lospec, contours](https://lospec.com/articles/pixel-art-outlines)
· [Lospec, contours et couleur](https://lospec.com/articles/pixel-art-outlines-part-2-using-color)
· [the-pixel.art, anticrénelage](https://the-pixel.art/articles/anti-aliasing/)
· [the-pixel.art, glissement de teinte](https://the-pixel.art/articles/hue-shifting-pixel-art-shading/)
· [the-pixel.art, design de personnage](https://the-pixel.art/articles/pixel-art-character-design/)
· [Logbook, banding et coussin](https://the-logbook-project.blogspot.com/2013/04/pixel-art-lessons-jiinchus-darkness.html)
· [androidarts](https://androidarts.com/pixtut/pixelart.htm)
· [Humbird0, créer des sprites](https://humbird0.com/makes/tutorials/create_sprites/content.htm)
· [MIT GDG, guide de style](https://gdg.mit.edu/style-guide)
· [clusters et AA](https://www.toolify.ai/ai-news/pixel-art-tutorial-mastering-clusters-and-antialiasing-3479126)
· [pixel-editor, théorie des couleurs](https://www.pixel-editor.com/articles/color-theory-for-pixel-art)
· [Pixel Grimoire #7](https://medium.com/pixel-grimoire/how-to-start-making-pixel-art-7-e504bfa4ddf2)
· [DEV Community, guide complet](https://dev.to/autosprites/from-zero-to-mastery-a-complete-pixel-art-guide-for-modern-game-developers-205i)

**Cheveux et fourrure :**
[Lospec, tutoriels cheveux](https://lospec.com/pixel-art-tutorials/tags/hair)
· [KawaiiHannah, ombre et lumière](https://kawaiihannah.com/pixelart/tutorials/shading-lighting/)
· [KawaiiHannah, cheveux sans contour](https://kawaiihannah.com/pixelart/tutorials/lineless-pixel-doll-hair/)
· [Slynyrd, visages et cheveux anime](https://slynyrd.com/blog/2020/7/28/pixelblog-29-anime-faces-and-hair)
· [Aseprite, visage anime d'après Slynyrd](https://community.aseprite.org/t/anime-face-based-off-slyndyrd/19607)
· [sprite-ai, pixel art anime](https://www.sprite-ai.art/blog/anime-pixel-art)
· [Clip Studio, cheveux en cel](https://tips.clip-studio.com/en-us/articles/11408)
· [Unity Toon Shader, angel ring](https://docs.unity3d.com/Packages/com.unity.toonshader@0.13/manual/AngelRing.html)
· [DodoIcons, fourrure](https://www.deviantart.com/dodoicons/art/Pixel-fur-shading-tutorial-513887367)
· [itch.io, fourrure](https://itch.io/t/2173926/pixel-tutorial-fur)

**Animation (partie E) :**
[Wikipédia, les 12 principes de l'animation](https://en.wikipedia.org/wiki/Twelve_basic_principles_of_animation)
· [Adobe, principes de l'animation](https://www.adobe.com/creativecloud/animation.html)
· [Clip Studio, maîtriser les 12 principes](https://tips.clip-studio.com/en-us)
· [80.lv, tutoriel de Pedro Medeiros](https://80.lv/)
· [Aseprite, « 32x32 Crane Kick »](https://community.aseprite.org/)
· [Tiny Warrior Games, animation sous-pixel](https://tinywarriorgames.com/)
· [CG Wire, images étirées](https://blog.cg-wire.com/)
· [GitHub, EaseSprite et outils pixel (ralenti par durée d'image)](https://github.com/topics/pixel-art)
· [borntofrappe, éclats « Spirited sparkles »](https://github.com/borntofrappe)
· [Brian Lemay, chevauchement](https://www.brianlemay.com/)

**Calques, flux pro, effets, GBA (E6-E8) [T16] :**
[Aseprite, bases](https://aseprite.org/docs/basics/)
· [Aseprite, cels liés](https://www.aseprite.org/docs/linked-cels/)
· [Aseprite, animation](https://aseprite.org/docs/animation/)
· [Aseprite (doc Mintlify), calques](https://mintlify.com/aseprite/aseprite/concepts/layers)
· [Aseprite (doc Mintlify), pelure d'oignon](https://mintlify.com/aseprite/aseprite/features/onion-skinning)
· [Aseprite, point d'ancrage](https://community.aseprite.org/t/set-the-anchor-of-a-sprite/14962)
· [emb33r, base pour séparer les articulations](https://emb33r.itch.io/aseprite-character-base-for-learning-how-to-separate-joints-when-making-an-anima)
· [PokéCommunity, tutoriel d'animation de sprite](https://www.pokecommunity.com/showthread.php?p=9990691)
· [Slynyrd #8, intro à l'animation](https://slynyrd.com/blog/2018/8/19/pixelblog-8-intro-to-animation)
· [Slynyrd #9, attaques au corps à corps](https://slynyrd.com/blog/2018/9/8/pixelblog-9-melee-attacks)
· [Slynyrd #53, coups de poing et de pied](https://www.slynyrd.com/blog/2024/11/25/pixelblog-53-punches-and-kicks)
· [Slynyrd #56, attaque vue de dessus](https://www.slynyrd.com/blog/2025/5/23/pixelblog-56-top-down-character-attack-animation)
· [Saint11, tutoriels](https://saint11.org/blog/pixel-art-tutorials/)
· [80.lv, Pedro Medeiros](https://80.lv/articles/pixel-animation-tutorial-by-pedro-medeiros)
· [sprite-ai, animation pixel](https://www.sprite-ai.art/blog/pixel-art-animation)
· [Divoom, animer du pixel art](https://divoom.com/blogs/app-guide/how-to-animate-pixel-art-divoom-display)
· [gamineai, hitstop, smear, impact](https://gamineai.com/blog/pixel-art-combat-fx-hitstop-smear-frames-impact-timing-2026)
· [Pinnguaq, effets d'animation](https://pinnguaq.com/learn/pixel-art/pixel-art-4-animation-effects-in-gimp/)
· [Tuts+, explosions](https://design.tutsplus.com/tutorials/how-to-animate-explosion-effects--cms-30960)
· [PixelJoint, fumée](https://pixeljoint.com/forum/printer_friendly_posts.asp?TID=16587)
· [r/PixelArtTutorials, décomposition d'une explosion](https://redlib.hbubli.cc/r/PixelArtTutorials/comments/1hkuqv1/breakdown_of_this_pixel_art_explosion_effect)
· [Aseprite, rotation sans tout refaire](https://community.aseprite.org/t/is-there-a-way-to-easily-rotate-objects-and-sprites-without-having-to-remake-them/7997)
· [Clean Rotate pour Aseprite](https://astropulse.itch.io/clean-rotate-for-aseprite)
· [Wikipédia, cycle de couleurs](https://en.wikipedia.org/wiki/Color_cycling)
· [80.lv, cycle de couleurs](https://80.lv/articles/color-cycling-from-the-90s-returns-with-html5)
· [loopsprite, alignement et pivot](https://loopsprite.pages.dev/slice/guide-sprite-alignment-pivot.html)
· [gamedev.net, planches de sprites](https://gamedev.net/forums/topic/613213-need-a-program-to-transfer-frames-to-an-animation-sheet)
· [gbadoc, sprites et OAM](https://gbadev-org.github.io/gbadoc/sprites.html)
· [agb, tailles d'objet](https://docs.rs/agb/latest/agb/display/object/enum.Size.html)
· [BlocksDS, sprites](https://blocksds.skylyrac.net/tutorial/basic/sprites/)
· [FEU, qu'est-ce que l'OAM](https://feuniverse.us/t/what-is-oam/6193)

**Livres (v14) [B] :**
[Pixel Logic, site officiel](https://pixellogicbook.com/post/131851328656/pixel-logic-is-an-in-depth-pixel-art-tutorial-book)
· [Pixel Logic, Gumroad](https://michafrar.gumroad.com/l/pixel-logic)
· [Pixel Logic, discussion Cosmigo](https://community.cosmigo.com/t/ebook-pixel-logic/319)
· [Pixel Art for Game Developers, Routledge](https://www.routledge.com/Pixel-Art-for-Game-Developers/Silber/9781482252309)
· [Pixel Art for Game Developers, O'Reilly (chapitre erreurs)](https://www.oreilly.com/library/view/pixel-art-for/9781482252316/chapter-51.html)
· [Pixel Art for Game Developers, notes de lecture](https://alexanderluna.github.io/books/pixel-art-for-game-developers.html)
· [Color and Light, Simon & Schuster](https://www.simonandschuster.co.uk/books/Color-and-Light/James-Gurney/James-Gurney-Art/9780740797712)
· [Color and Light, critique Parka Blogs](https://www.parkablogs.com/content/book-review-color-and-light-guide-realist-painter)

**Tramage (A7) :**
[the-pixel.art, tramage et Bayer](https://the-pixel.art/articles/dithering/)
· [pixnote, tramage](https://pixnote.net/en/learn/dithering/)
· [Divoom, quand tramer et quand arrêter](https://divoom.com/blogs/setup-ideas/pixel-art-dithering-when-to-use-and-stop)
· [Spearite, guide du tramage](https://spearite.com/blog/pixel-art-dithering-guide)
· [pixel-editor, tramage](https://www.pixel-editor.com/articles/pixel-art-dithering)
· [Wikipédia, tramage ordonné](https://en.wikipedia.org/wiki/Ordered_dithering)
· [Pixel Parmesan, anticrénelage](https://pixelparmesan.com/anti-aliasing-fundamentals-for-pixel-artists)

**Perspectives (A9) :**
[Slynyrd #3, projections 1](https://www.slynyrd.com/blog/2018/3/14/pixelblog-3-graphical-projections-1)
· [Slynyrd #4, projections 2](https://slynyrd.com/blog/2018/4/12/pixelblog-4-graphical-projection-part-2)
· [Pixel Parmesan, isométrique](https://pixelparmesan.com/fundamentals-of-isometric-pixel-art/)
· [Slynyrd #54, isométrique](https://www.slynyrd.com/blog/2025/1/23/pixelblog-54-isometric-pixel-art)
· [cxong, nombre de sprites par vue](https://cxong.github.io/2022/03/how-many-sprites-do-different-perspectives-need)

**Décors, tuiles, parallaxe (F) :**
[Slynyrd #23, parallaxe](https://www.slynyrd.com/blog/2019/11/12/pixelblog-23-parallax-scrolling)
· [Slynyrd #20, tuiles vues de dessus](https://www.slynyrd.com/blog/2019/8/27/pixelblog-20-top-down-tiles)
· [Slynyrd #28, tuiles de profil](https://slynyrd.com/blog/2020/5/21/pixelblog-28-side-view-tiles)
· [Slynyrd #43, tuiles vues de dessus 2](https://www.slynyrd.com/blog/2023/3/26/pixelblog-43-top-down-tiles-part-2)
· [DEV, Wang 16 contre blob 47](https://dev.to/hoanganhlam/wang-16-vs-blob-47-how-auto-tile-sets-actually-work-and-which-one-to-draw-538m)
· [neta.art, pourquoi 47 tuiles](https://neta.art/blog/autotile-47-tile-blob-rules)
· [jaconir, autotile Godot](https://jaconir.online/blogs/bitmask-autotile-guide)
· [Pinnguaq, tuiles avancées](https://pinnguaq.com/learn/pixel-art/pixel-art-3b-advanced-tiles-in-graphicsgale/)
· [sprite-ai, fonds](https://www.sprite-ai.art/blog/pixel-art-backgrounds)
· [Pixelated Kisses, composition](https://pixelatedkisses.com/blog/pixel-art-composition-rules.html)
· [Pixel Parmesan, théorie des couleurs](https://pixelparmesan.com/color-theory-for-pixel-artists-its-all-relative/)
· [GitHub, profondeur dans les scènes 2D](https://github.com/joeuk89/pixel-art/issues/65)

**Maîtres et geste du pro (A10, A11) :**
[Square Enix, Kazuko Shibuya et les Pixel Remaster](https://www.square-enix-games.com/en_GB/news/final-fantasy-pixel-remaster-kazuko-shibuya)
· [Wikipédia, Kazuko Shibuya](https://en.wikipedia.org/wiki/Kazuko_Shibuya)
· [GDC Vault, Mark Ferrari, *8 Bit & '8 Bitish' Graphics*](https://www.gdcvault.com/play/1023586)
· [Game Developer, 5 conseils d'animation 2D (Paul Robertson)](https://www.gamedeveloper.com/)
· [Bloop Animation, images étirées](https://www.bloopanimation.com/the-art-of-smear-frames/)
· [Lospec, tutoriels de Henk Nieborg](https://lospec.com/pixel-art-tutorials/author/henk-neiborg)
· [Retronator, Waneella](https://medium.com/retronator-magazine/the-mysterious-world-of-waneella-281d5b52a68)
· [pixivision, entretien avec Toyoi Yuuta](https://www.pixivision.net/en/a/2686)
· [Pixel Parmesan, bases de l'AA](https://pixelparmesan.com/anti-aliasing-fundamentals-for-pixel-artists)
· [MiniBoss, articles de Pedro Medeiros](https://blog.studiominiboss.com/pixelart)
· [Pixel Grimoire #2](https://medium.com/pixel-grimoire/how-to-start-making-pixel-art-2-bcd705cb04d7)
· [Slynyrd #41, isométrique](https://www.slynyrd.com/blog)
· [gamedev.net, palettes de couleurs](https://gamedev.net/tutorials/visual-arts/pixel-art-tutorial-basics-r5287)
· [Aseprite, flux de travail](https://www.aseprite.org/docs/workflow/)
· [Aseprite, stylet ou souris](https://community.aseprite.org/t/do-you-use-pen-input-to-control-aseprite-does-it-improve-your-work/4753)
· [PixelJoint, banding (Helm)](https://pixeljoint.com/forum/forum_posts.asp?TID=11299)

**Progresser (G) :**
[pixelart.school, feuille de route](https://pixelart.school/learn/how-to-learn-pixel-art)
· [pixnote, 15 astuces](https://pixnote.net/en/learn/tips/)
· [Quora, s'entraîner au pixel art](https://www.quora.com/How-can-you-practice-pixel-art)

---

# Historique des versions

- **v23 :** **0-AC le sketch fini de pro** : le trait seul doit passer pour une planche de
  concept art ; contre-exemple de la fiole-bourgeon [T18] ; huit critères (idée en silhouette,
  trois poids de trait, recouvrements nets, lignes de forme, hiérarchie des détails, formes
  secondaires, mouvement, traits décidés) ; dessiner un design à 64 px de haut au moins ;
  règles 86 et 87 ; sources [D33] et [D34]. Dans Claude Pixel : étape « Validation du dessin »
  avec les cases du sketch fini, alerte quand un objet v23 est dessiné sous 64 px.

- **v22 :** **0-AB le sketching d'un illustrateur** : vignettes, design des pièces, rough,
  construction, esquisse nettoyée, trait final, polish du trait, validation du dessin ; un
  calque par passe, celui du dessous baissé à 20-40 % ; redessiner plutôt que gommer ;
  retourner la toile ; poids du trait ; le dessin se juge à la fin du sketching, avant la
  couleur ; règles 83 à 85 ; sources [D31] et [D32]. Dans Claude Pixel : étapes v22 (rough,
  esquisse nettoyée, polish du trait, validation du dessin), bouton « Retourner la toile ».

- **v21 :** **0-AA dessiner une forme belle** : contre-exemple de la fiole de la séance
  `fiole-unique` [T17], douze principes (langage dominant, motif à trois échelles, proportions
  franches, jonctions dessinées, rythme du contour, ligne de flux, bouchon comme objet, poids,
  peu de zones de détail, test de la silhouette générique, pousser puis revenir, appeal),
  analogies de la nature et du verre d'art, méthode de design (6 silhouettes en 3 familles,
  grille de critique sur 30, 3 variantes par pièce) ; règles 79 à 82 ; sources [D29] et [D30].
  Dans Claude Pixel : étape **Design des pièces**, rubriques *Critique* et *Pièce* au carnet,
  carnet ouvert à toutes les étapes, justification des défauts restants à la planche, onglets
  sur plusieurs lignes, couleur exportée dans le regard.

- **v20 :** les manques comblés. **0-T** perspective avancée et raccourcis (diminution,
  convergence, raccourci, recouvrement ; 1, 2, 3 points ; membres en raccourci) ; **0-U**
  anatomie animale (plantigrade, digitigrade, onguligrade ; quadrupède en volumes ; ailes
  et groupes de plumes ; insectes) ; **0-V** mains, expressions, jeu d'acteur ; **0-W**
  éclairages complexes (hiérarchie, températures, contre-jour, nuit, lumière colorée,
  sources proches, brume) ; **0-X** effets naturels traduits en pixels (fumée, eau,
  explosion, étincelles) ; **0-Y** stylisation et fiche de style ; **0-Z** raconter en une
  image ; sources [D21] à [D28] ; règles impératives 71 à 78.

- **v19 :** **0-P inventer** (SCAMPER, tableau morphologique, mélange de références,
  contraintes) ; **0-Q geste** (C, S, droite, ligne d'action, rythme, en pixels) ; **0-R
  harmonies de couleur** (dominante, soutien, accent ; analogue, complémentaire,
  complémentaire adjacente) ; **0-S métal et textures** (chrome, brossé, usé ; bois, tissu,
  fourrure, feuillage) ; sources [D16] à [D20] ; règles impératives 67 à 70. Dans Claude
  Pixel : rubrique « Variante » au carnet, carnet résumé dans chaque regard de la souris.

- **v18 :** **0-N vision et conception** : carnet (une idée par ligne, rien ne s'efface,
  on barre avec la raison), cinq questions (vision, structure ou physionomie, formes de
  base, idée unique, crédibilité), essais en vignettes (au moins trois silhouettes, choix
  écrit), exemple d'une fiole à forme unique ; **0-O astuces de pro** (grandes formes,
  économie, langage des formes, contraste et rythme, point d'intérêt, pousser l'idée,
  regarder autrement, accepter le raté) ; planches slime et gemmes [P4] (0-K) et recette de
  la gemme (0-L-G) ; sources [D11] à [D15] ; règles impératives 61 à 66. Dans Claude
  Pixel : étapes **Vision** et **Essais** avant la construction, carnet de conception dans
  l'onglet Méthode, portes du carnet.

- **v17 :** **partie 0, dessiner avant de pixelliser**. Diagnostic de la potion 64×64 face
  à une planche pro (0-A) ; construction et dessin à travers (0-B) ; zones de la lumière :
  éclat, lumière, demi-ton, terminateur, ombre propre, rebond, occlusion, ombre portée
  (0-C) ; design des valeurs (deux familles, notan, étendue ; 0-D) ; design des formes
  (0-E) ; perspective utile (0-F) ; couleur (0-G) ; bords (0-H) ; matières (0-I) ; méthode
  du pro (0-J) ; analyse de neuf planches fournies [P3] (0-K) ; recettes (potion en verre,
  sphère d'étude, fruit, pain, flamme, ruines ; 0-L) ; plan d'entraînement (0-M) ; sources
  [D] ; règles impératives 49 à 60 ; règle 23 élargie. Dans Claude Pixel : **onglet
  Lumière** (direction, hauteur, forme, guide de volume sur la toile, repère de lumière),
  vues **Notan** et **Valeurs** sur la toile, détecteur « L'ombrage ne suit pas la
  lumière », porte « Le volume suit la lumière », étapes v17 (construction, deux familles,
  modelé, matière), regard de la souris avec valeurs et guide.

- **v16 :** **A10** leçons des maîtres (Kazuko Shibuya, Mark Ferrari, Paul Robertson, Henk
  Nieborg, Waneella, Toyoi Yuuta, Slynyrd, saint11, Pixel Parmesan) et ce qui revient chez
  tous ; **A11** geste du pro (le bon outil par forme, un trait = un geste décidé, tests en
  cours de dessin : miroir, gris, yeux plissés, palette seule, pause) ; A6-A complétée
  (repère saturation/luminosité, rotation de 45° entre rampes, pas de glissement de teinte
  par habitude, ombrer en gris) ; A6-F complétée (AA sur marches de 2 px ou plus, un pixel
  par coin, test de l'enlèvement) ; E2-D sous-pixel détaillé ; A9 isométrique en pratique
  (calque règle, multiples de 4) ; livres [B6] ; règles impératives 43 à 48 ; sommaire,
  index, sources et résumé mis à jour. Dans Claude Pixel : nouvelles cases et portes, détecteur
  d'AA isolé, souris plus fluide.
- **v15 :** **B6** recettes pas à pas tirées de cinq planches fournies [P2] : ordre commun
  en 9 étapes (contour neutre jusqu'à la lumière, teinte après les valeurs), primitive puis
  déformation (rochers, strates), pierre (arêtes cassées, trait intérieur effacé, fissures à
  lèvre claire, trous en groupes), cristal (facettes avant l'ombre, contre-jour coloré, halo,
  étincelles en croix), slime (grand reflet en forme, translucidité, ombre portée), livre
  (couverture qui déborde, décor au trait, ruban qui casse la silhouette, mat contre
  brillant) ; règles impératives 39 à 42 ; sommaire, index, sources et résumé mis à jour.
- **v14 :** apports des livres [B] (*Pixel Logic*, *Pixel Art for Game Developers*, *Make
  Your Own Pixel Art*, *Color and Light*, livres d'images). Nouvelles sections : **A7**
  tramage (conditions, motifs, rampe de densité, défauts), **A8** lignes et formes (pentes
  propres, ligne pensée en vecteur, sous-pixel fixe), **A9** perspectives de jeu ; **partie
  F** décors (hiérarchie de lecture, tuiles sans couture, variantes, autotiles blob 47 et
  Wang 16, plateformes, fonds et perspective atmosphérique, parallaxe au pixel près, palette
  de lieu et masque de gamme, composition, contrôles) ; **partie G** progresser (plan en
  quatre paliers, copies d'étude, retours, portfolio). A6-H complété des erreurs de Silber ;
  règles impératives 31 à 38 ; sommaire, index, résumé et sources mis à jour ; section
  « Livres de référence ».
- **v13 :** partie E complétée pour l'animation complexe : E6 composition en calques
  (pièces séparées, ordre d'empilement fixe, cels liés, pivot, assemblage par `stamp`),
  E7 flux de travail pro (ébauche en silhouette, pelure d'oignon, étiquettes, rotation,
  cycle de marche, attaque et impact avec flash et arrêt sur image, fumée et explosions,
  cycle de palette), E8 export et contraintes GBA (taille de cellule fixe, pivot, tailles
  OAM, métasprites, 16 couleurs) ; E4, E5 et résumé mis à jour.
- **v12 :** partie E « Animation » : méthode imposée image par image (feuille de timing,
  pipeline complet et validation pour chaque image), les 12 principes de *The Illusion of
  Life* traduits en règles pixel, techniques pixel (durées, tenues, espacement,
  dépassement, smear, sous-pixel, pop, éclats, boucle, UI), contrôles par image et par
  séquence ; règles impératives 26 à 30 ; test 15 (parchemin qui se déroule).
- **v11 :** nettoyage. A6 et A7 fusionnées en une seule A6 « Finition pro » ; C6, C6b et
  C6c fusionnées en une seule C6 « Cheveux » ; sommaire ajouté ; sources web réunies à la
  fin ; partie D corrigée (vrais dossiers, usages exacts) ; renvois corrigés ; listes de
  fichiers disparus retirées.
- **v10.6 :** finition pro chiffrée (rampe, budget couleur, contour, tests) ; cheveux anime
  (poids, flicks, ahoge, ombrage cel, angel ring, test 14).
- **v10.5 :** cheveux, astuces de pro (touffes, lumière, rampe, selout, test 13).
- **v10.4 :** C17 vêtements (plis de Bridgman, cônes, couches, matières) ; astuces de pro.
- **v10.2 :** C15 créatures et monstres (test 11).
- **v10.1 :** chibi sans épaule marquée ; tête ronde ou ovale, jamais en œuf.
- **v10 :** règles impératives ; C14 corps nu d'abord (test 10) ; `contour.py` en calque.
- **v9 :** C13 chibi pas à pas (test 9) ; leçons de la potion ; partie D.
