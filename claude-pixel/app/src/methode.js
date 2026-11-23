/* Claude Pixel — la méthode (METHODE_PIXEL_ART.md) en données et en portes.
 * Fiches d'intention (B0, C0, E0, F0, G2), étapes par type de projet, cases à cocher,
 * portes vérifiées par la machine. En mode « claude » une porte qui échoue bloque ;
 * en mode « humain » elle avertit seulement. */
(function (G) {
'use strict';
const AP = G.AP;

/* ---------- Fiches d'intention ---------- */
const CH = (cle, label, aide, o = {}) => Object.assign({ cle, label, aide, requis: true, type: 'texte' }, o);
const PROJ = ['de face', '3/4 de dessus', 'dessus pur', 'isométrique 2:1', 'dimétrique', 'oblique'];
const FICHES = {
  objet: [
    CH('quoi', 'Ce que c\'est', 'Un nom précis : « potion de soin », pas « objet ».'),
    CH('usage', 'À quoi il sert dans le jeu', 'Case d\'inventaire, objet posé au sol, icône… (B0)'),
    CH('couleurs', 'Nombre de couleurs prévu', 'Voir la table A3 pour la taille de la toile.', { type: 'nombre' }),
    CH('projection', 'Projection', 'Une seule par jeu (B0b, règle 33).', { type: 'choix', options: PROJ }),
    CH('lumiere', 'Lumière', 'Une seule source. Par défaut : haut gauche.', { type: 'choix', options: ['haut gauche', 'haut droite', 'dessus', 'autre (dire pourquoi)'] }),
    CH('matiere', 'Matière principale', 'Verre, métal, bois, pierre, tissu, gel… (A5-8b)'),
    CH('accent', 'Couleur d\'accent', 'La seule couleur saturée de l\'objet (B0).'),
    CH('vise', 'Niveau visé', 'Une œuvre pro précise et ce que tu en prends (0-J) : « planche potion, étape 9 : verre transparent, liquide vu au travers ».', { requis: false })
  ],
  personnage: [
    CH('qui', 'Qui', 'Nom, rôle, ce qu\'il fait dans le jeu (C0).'),
    CH('attitude', 'Attitude', 'Ce que dit la pose : fier, craintif, prêt à frapper…'),
    CH('emotion', 'Un mot d\'émotion', 'Un seul mot.'),
    CH('vue', 'Vue', 'Face, 3/4 ou profil.', { type: 'choix', options: ['face', '3/4', 'profil'] }),
    CH('couleurs', 'Nombre de couleurs prévu', 'Table A3.', { type: 'nombre' }),
    CH('proportions', 'Proportions', 'En nombre de têtes (C1).', { type: 'choix', options: ['chibi 2–3 têtes', 'RPG 4–5 têtes', 'semi-réaliste 6–8 têtes'] }),
    CH('visage', 'Style de visage', 'Yeux points, yeux anime, réaliste… (C4, C10-D)'),
    CH('references', '2–3 références et ce que tu prends de chacune', 'Ex. « Réf. 1 : la cape ; réf. 2 : la palette ». Images importées en calque de référence.'),
    CH('objectif', 'Un objectif prioritaire', 'Ce que ce dessin doit réussir avant tout.')
  ],
  creature: [
    CH('qui', 'Quelle créature', 'Nom, rôle, danger dans le jeu.'),
    CH('attitude', 'Attitude', 'Ce que dit la pose.'),
    CH('emotion', 'Un mot d\'émotion', 'Un seul mot.'),
    CH('langage', 'Langage de formes', 'Décidé maintenant, il dicte tête, yeux et pieds (C15-A).', { type: 'choix', options: ['rond (doux)', 'triangle (dangereux)', 'carré (lourd)'] }),
    CH('marqueurs', '2–3 marqueurs d\'identité', 'Ce qui fait reconnaître la créature à ×1.'),
    CH('accent', 'Couleur d\'accent', 'Une seule couleur saturée.'),
    CH('vue', 'Vue', 'Face, 3/4 ou profil.', { type: 'choix', options: ['face', '3/4', 'profil'] }),
    CH('couleurs', 'Nombre de couleurs prévu', 'Table A3.', { type: 'nombre' }),
    CH('objectif', 'Un objectif prioritaire', 'Ce que ce dessin doit réussir avant tout.')
  ],
  animation: [
    CH('quoi', 'Ce qui bouge', 'Le sujet et l\'action : « slime qui saute ».'),
    CH('pourquoi', 'Pourquoi il bouge', 'Ce que l\'action raconte dans le jeu (E0-1).'),
    CH('emotion', 'Un mot d\'émotion', 'Un seul mot.'),
    CH('duree', 'Durée totale (ms)', 'Fixée avant de dessiner.', { type: 'nombre' }),
    CH('boucle', 'Boucle ?', 'Une boucle revient à sa première image.', { type: 'choix', options: ['boucle', 'une fois'] }),
    CH('couleurs', 'Nombre de couleurs prévu', 'Table A3.', { type: 'nombre' })
  ],
  decor: [
    CH('vue', 'Vue du jeu', 'La même que les personnages (règle 33).', { type: 'choix', options: PROJ.concat(['profil (plateforme)']) }),
    CH('tuile', 'Taille de tuile', 'F0.', { type: 'choix', options: ['8', '16', '32'] }),
    CH('plans', 'Plans', 'Premier plan, plan jouable, fond… (F1)'),
    CH('lecture', 'Ce qui doit se lire d\'un coup d\'œil', 'Chemin, danger, sortie… (F1)'),
    CH('lieu', 'Palette du lieu', 'Heure, climat, ambiance, teinte dominante (F4).'),
    CH('vise', 'Niveau visé', 'Une œuvre pro précise et ce que tu en prends (0-J) : « tuiles de Celeste : croûte qui déborde, clusters gras ».', { requis: false })
  ],
  etude: [
    CH('oeuvre', 'Pièce étudiée', 'Titre et jeu.'),
    CH('artiste', 'Artiste à créditer', 'Les copies restent privées (G2).'),
    CH('technique', 'Technique à retenir', 'Ce que tu veux comprendre : selout, AA, rampes…')
  ]
};
FICHES.chibi = FICHES.personnage.map(c => c.cle === 'proportions' ? Object.assign({}, c, { options: ['chibi 2–3 têtes'] }) : c);

/* ---------- Questions de la planche (A5-11) ---------- */
const QUESTIONS = [
  'La silhouette se reconnaît-elle seule ?',
  'Les matières se séparent-elles en gris ?',
  'Le volume se lit-il, et la lumière vient-elle d\'une seule source ?',
  'Le point d\'intérêt a-t-il le plus fort contraste ?',
  'En notan (deux valeurs), lumière et ombre forment-elles deux grandes masses dont la frontière dessine le volume (0-C, 0-D) ?',
  'Reste-t-il des orphelins, du banding, de l\'ombrage coussin, des « L » dans le contour ?',
  'Y a-t-il une forme dominante, une moyenne et une petite (A4b) ? Les marqueurs d\'identité se voient-ils à ×1 ?',
  'L\'objectif de l\'étape 0 est-il atteint ?'
];
const QUESTIONS_TYPE = {
  objet: [ // B5
    'Se reconnaît-il en 1 s dans une case d\'inventaire ?',
    'Même vue, même lumière, même contour et même densité de détail que le reste du jeu ?',
    'Largeur impaire si l\'objet est symétrique (le centre tombe sur un pixel) ?',
    'Les matières se séparent-elles en gris ?',
    'Tient-il sur fond clair et sur fond sombre ?'
  ],
  personnage: [ // C8
    'La pose exprime-t-elle l\'intention ? Les proportions suivent-elles le nombre de têtes ?',
    'Le visage se lit-il à ×1 ?',
    'Les articulations sont-elles plausibles (aucun bras en tube) ?',
    'Les cheveux ont-ils une masse, des mèches d\'au moins 2 rangées, un reflet côté lumière ?',
    'Tient-il à côté de la référence ?'
  ],
  creature: [
    'Le langage de formes se voit-il en silhouette (tête, yeux, pieds) ?',
    'Les 2–3 marqueurs se voient-ils à ×1 ?',
    'Une seule couleur saturée ?',
    'La silhouette a-t-elle des vides (pas un bloc) ?'
  ],
  animation: [ // E5-B
    'Les clés se lisent-elles seules ?',
    'Aucune respiration parasite (pièces rigides qui tremblent) ?',
    'GIF regardé 3 fois aux vraies durées ?',
    'Anticipation, dépassement et chevauchement présents ?',
    'Une seule action principale, aucun jumeau (bras et jambes en miroir parfait) ?',
    'Au moins un défaut noté et corrigé ?',
    'Même pivot sur toutes les images ; calques ref et pivot non exportés ?'
  ],
  decor: [ // F6
    'Grille 3×3 : aucune couture, aucune grille visible ?',
    'Carte dézoomée 20×12 : la répétition ne saute pas aux yeux ?',
    'En gris : le plan jouable se lit, le fond est plus clair et moins contrasté ?',
    'Personnage posé : il a le plus fort contraste de l\'écran ?',
    'Autotile en U, L et îlot : tous les raccords tiennent ?'
  ],
  etude: [
    'L\'analyse est-elle écrite avant la copie (couleurs, rampe, lumière, contour, selout, AA, trame) ?',
    'La version de mémoire est-elle comparée à l\'original, écarts notés ?',
    'Quelle technique réutiliser cette semaine ?'
  ]
};
QUESTIONS_TYPE.chibi = QUESTIONS_TYPE.personnage;

/* Tests du pro (A6-J) : la vue de l'interface associée. */
const TESTS_PRO = [
  { id: 'plisser', nom: 'Plisser les yeux', vue: 'flou', voir: 'quelques grandes taches claires et sombres, pas de grésillement' },
  { id: 'notan', nom: 'Notan', vue: 'notan', voir: 'deux grandes masses (lumière, ombre) ; leur frontière est le terminateur et suit la forme (0-D)' },
  { id: 'guide', nom: 'Guide de volume', vue: 'guide', voir: 'ton ombrage place lumière, demi-ton, terminateur, ombre propre, rebond et ombre portée là où le guide les met, ou tu sais dire pourquoi pas (0-C)' },
  { id: 'gris', nom: 'Gris', vue: 'gris', voir: 'chaque matière a sa valeur ; le point d\'intérêt a le plus fort contraste' },
  { id: 'silhouette', nom: 'Silhouette', vue: 'silhouette', voir: 'pose et coiffure se reconnaissent sans couleur' },
  { id: 'reelle', nom: 'Taille réelle', vue: 'x1', voir: 'aucun détail ne devient bruit ; le contour tient sur les deux fonds' },
  { id: 'miroir', nom: 'Miroir', vue: 'miroir', voir: 'aucune pente ni proportion fausse ne saute aux yeux' },
  { id: 'teinte', nom: 'Teinte', vue: 'rampes', voir: 'les ombres virent au froid, les lumières au chaud' },
  { id: 'defauts', nom: 'Défauts ×4', vue: 'defauts', voir: 'aucun des défauts de A6-H ; AA seulement sur les courbes dures' },
  { id: 'moins', nom: 'Une couleur de moins', vue: 'moins', voir: 'si rien ne change, la couleur reste retirée' },
  { id: 'situation', nom: 'En situation', vue: 'situation', voir: 'il se détache du fond sans liseré forcé' }
];

const TABLE_A3 = {
  colonnes: ['16×16', '32×32', '64×64', '128 px et plus'],
  lignes: [
    ['Tons par matière', '2 à 3', '3 à 4', '4 à 5', '5 et plus'],
    ['Couleurs au total', '≤ 8', '≤ 16', '≤ 24', 'libre'],
    ['Contour', '1 px, un ou deux tons sombres', '1 px, selout', '1 px, selout, contour cassé', '1 à 2 px, épaisseur variable'],
    ['Anticrénelage (AA)', 'non', 'rare, à l\'intérieur', 'sur les grandes courbes', 'oui, à la main'],
    ['Texture', 'non', '1 ou 2 touches', 'par groupes de 2 ou 3', 'oui'],
    ['Décalage de teinte', 'faible : la valeur suffit', 'moyen', 'fort', 'fort'],
    ['Idée de détail', '1 seule', '1 ou 2', '3 ou 4, hiérarchisées', 'libre']
  ]
};
function colonneA3(doc) { const m = Math.max(doc.w, doc.h); return m <= 16 ? 0 : m <= 32 ? 1 : m <= 64 ? 2 : 3; }

/* ---------- Étapes ---------- */
const E = (id, titre, ref, faire, o = {}) => Object.assign({ id, titre, ref, faire, pasEncore: '', coches: [], portes: [], outils: [] }, o);
const C = (cle, txt) => ({ cle, txt });
const ETAPE_FICHE = (ref) => E('fiche', 'Fiche d\'intention et règles', ref, [
  'Remplis la fiche : chaque champ est une décision prise avant le premier pixel.',
  'Lis les 92 règles impératives (onglet Aide) et coche « lues ».',
  'Règle la toile à la taille finale : on ne dessine jamais en grand pour réduire (A4b).',
  'Choisis ou construis la palette : une rampe par matière (A6-A).',
  'Nomme 2 ou 3 idées fortes, pas plus : ce qu\'on doit reconnaître de loin (A10-F, règle 44).'
], { portes: ['fiche', 'regles'], pasEncore: 'Aucun pixel tant que la fiche n\'est pas remplie.' });
const ETAPE_PLANCHE = (ref) => E('planche', 'Contrôle final : la planche', ref, [
  'Ouvre l\'onglet Contrôle : ×1, ×2, agrandi, fond clair et sombre, miroir, silhouette, gris, en situation.',
  'Fais une pause, puis regarde d\'un œil neuf (A11-C) avant de passer les tests du pro (A6-J) un par un.',
  'Réponds aux 7 questions communes et aux questions propres au type.',
  'Bilan : 3 points réussis, 3 points à améliorer. Les 3 à améliorer deviennent les objectifs du prochain dessin.'
], { portes: ['planche', 'defauts'] });
const NETTOYAGE = ['L', 'jaggies', 'orphelins', 'bandes', 'coussin', 'bruit', 'trame', 'superpixels', 'budget', 'rampesGris', 'alpha'];

const ETAPES_V16 = {
  objet: [
    ETAPE_FICHE('B0 · B0b · A3'),
    E('forme', 'Forme de base', 'B6-A · B6-B', [
      'Pose la primitive (cube, cylindre, sphère, prisme) d\'un trait sombre et neutre, 1 px.',
      'Pose un repère de lumière (flèche haut-gauche) dans un calque de construction.',
      'Largeur impaire si l\'objet est symétrique.'
    ], { pasEncore: 'Pas de détail.', portes: ['nonVide', 'L'], outils: ['ligne', 'ellipse', 'rect'],
      coches: [C('primitive', 'La primitive se lit à ×1'), C('reperelum', 'Repère de lumière posé'), C('miroir', 'Vue miroir regardée : aucune pente fausse')] }),
    E('deformer', 'Déformer et séparer', 'B6-A · B6-B', [
      'Casse les coins, sépare les grandes pièces (bouchon, col, panse…).',
      'Un objet composé = 2-3 masses de tailles différentes (dominante, moyenne, petite ; A4b).'
    ], { pasEncore: 'Pas de couleur.', portes: ['L', 'jaggies'], coches: [C('masses', 'Une forme dominante, une moyenne, une petite')] }),
    E('aplats', 'Nettoyer le trait et poser les aplats', 'B6-A · A5-7', [
      'Trait pixel-perfect : aucun L, des marches régulières.',
      'Un aplat par matière, dans le ton moyen de sa rampe.',
      'Vérifie les valeurs en gris : chaque matière a la sienne.'
    ], { pasEncore: 'Pas d\'ombre.', portes: ['L', 'jaggies', 'budget', 'rampesGris'], coches: [C('gris', 'Les matières se séparent en gris')] }),
    E('ombre', 'Ombrage de base', 'B6-A · A5-8', [
      'Une seule lumière, haut-gauche. Un ton par face.',
      'Pose d\'abord le terminateur (limite ombre/lumière), net.',
      'Sur un bloc ombré, efface le trait des arêtes intérieures (règle 40).'
    ], { pasEncore: 'Pas de reflet fin.', portes: ['coussin', 'L'], outils: ['ombrage'], coches: [C('terminateur', 'Terminateur net, un côté d\'ombre franc'), C('grisOmbre', 'Ombre lue en gris : la forme tient sans couleur (règle 43)')] }),
    E('secondaires', 'Ombres et lumières secondaires', 'B6-A · A6-E', [
      'Sous-plans, occlusion ambiante dans les creux, lumière réfléchie (rebond) côté ombre.'
    ], { portes: ['coussin', 'bandes'], coches: [C('ao', 'AO dans les creux, rebond plus sombre que la lumière')] }),
    E('eclats', 'Éclats et contour coloré', 'B6-A · A6-C', [
      'Éclats spéculaires : 1-2 px du côté de la lumière.',
      'Selout : le contour prend la couleur sombre de la matière qu\'il borde, plus clair côté lumière.'
    ], { portes: ['orphelins', 'noirPur'], coches: [C('selout', 'Contour coloré (selout) posé maintenant, pas avant')] }),
    E('contrejour', 'Contre-jour', 'B6-A · B6-G', [
      'Une 2e lumière, opposée, d\'une autre teinte, fine (1 px sur le bord).'
    ], { coches: [C('autre', 'Le contre-jour a une autre teinte que la lumière principale')] }),
    E('teinte', 'Variation de couleur', 'B6-A · A5-8c', [
      'Les ombres virent au froid, les lumières au chaud, sans changer les valeurs.',
      'Vérifie en gris que rien n\'a bougé.'
    ], { portes: ['rampesGris'], coches: [C('froid', 'Ombres plus froides, valeurs inchangées en gris')] }),
    E('details', 'Détails et nettoyage', 'B6-A · A6-H · A5-10', [
      'Fissure ou gravure = trait sombre + lèvre claire d\'1 px, attachée à une arête (règle 41).',
      'Chasse les défauts : L, jaggies, orphelins, banding, coussin, bruit.',
      'Supprime les calques de construction de l\'export.'
    ], { portes: NETTOYAGE, coches: [C('levre', 'Fissures avec lèvre claire'), C('lisible', 'Chaque étape se lit à ×1'), C('aa', 'AA seulement sur les marches de 2 px ou plus, à l\'intérieur ; chaque pixel d\'AA passe le test de l\'enlèvement (règle 46)')] }),
    ETAPE_PLANCHE('A5-11 · B5 · B6-G')
  ],
  personnage: [
    ETAPE_FICHE('C0 · C1 · A3'),
    E('construction', 'Construction en calques de couleur', 'C13-A · R4 · C2', [
      'Calque rouge : la pose (ligne d\'action, squelette, geste, contrapposto).',
      'Calque bleu : repères (hauteur en têtes, épaules, bassin, sol).',
      'Calque vert : volumes (mannequin : tête, cage, bassin, membres).'
    ], { pasEncore: 'Aucun pixel final.', portes: ['construction'], coches: [C('geste', 'Un geste : coude, contrapposto, aucun membre en colonne'), C('tetes', 'La hauteur suit le nombre de têtes')] }),
    E('silhouette', 'Silhouette du corps nu', 'A5-5 · C14-A', [
      'Une seule couleur sombre. Regarde à ×1 : la pose doit se lire.',
      'Des vides clairs (entre bras et torse, entre les jambes).',
      'Remplis une rangée de plus sous les pieds (règle 12).'
    ], { pasEncore: 'Pas de vêtement, pas de détail.', portes: ['nonVide', 'silhouette1'], coches: [C('vides', 'Espaces négatifs lisibles'), C('pose', 'La pose se lit à ×1'), C('miroir', 'Vue miroir regardée : la pose ne penche pas')] }),
    E('contour', 'Contour', 'A5-6 · A6-D', [
      '1 px, aucun L. Courbes 5-3-2-1-1, jamais 5-2-1-2-1. Diagonales régulières.',
      'Tête ronde ou ovale, jamais en œuf (règle 13).'
    ], { portes: ['L', 'jaggies'] }),
    E('aplats', 'Palette et aplats', 'A5-7 · A6-A · C10-F', [
      'Une rampe par matière (peau, tissu, cheveux…), glissement de teinte.',
      'Vérifie le budget (A3) et les valeurs en gris.'
    ], { portes: ['budget', 'rampesGris', 'L'], coches: [C('gris', 'Les matières se séparent en gris')] }),
    E('lumiere', 'Lumière et ombres du corps', 'A5-8 · A6-E', [
      'Une source haut-gauche. Terminateur d\'abord. Pas de coussin.',
      'Marque chaque jointure (aisselle, coude, poignet, aine, genou, cheville ; C14-A).'
    ], { portes: ['coussin', 'bandes'], outils: ['ombrage'], coches: [C('jointures', 'Les 6 jointures sont marquées'), C('valide', 'Corps validé : silhouette, ombres, ×1'), C('grisOmbre', 'Ombres lues en gris (règle 43)')] }),
    E('vetements', 'Vêtements en calque', 'C14-B · C17', [
      'Nouveau calque. Tissu 1 px au-delà du bord du corps.',
      'Contour du calque seul ; bords intérieurs tracés à la main.',
      'Plis aux articulations, ligne de tension, ombres en masses.'
    ], { pasEncore: 'Le corps validé ne se retouche plus.', portes: ['L', 'orphelins'], coches: [C('epaisseur', 'Le tissu a une épaisseur (1 px au-delà)'), C('plis', 'Plis aux articulations')] }),
    E('visage', 'Visage puis cheveux', 'C4 · C6 · C10-C/D', [
      'Visage : yeux, sourcils, bouche lisibles à ×1.',
      'Cheveux en calque : une masse casque, puis mèches d\'au moins 2 rangées, reflet côté lumière.'
    ], { portes: ['L', 'orphelins'], coches: [C('visage', 'Le visage se lit à ×1'), C('meches', 'Mèches d\'au moins 2 rangées')] }),
    E('details', 'Détails et accessoires', 'A5-9', [
      'Règle du tiers, groupes de 2-3, chaque détail raconte quelque chose.',
      'Les accents les plus sombres dans les creux.'
    ], { portes: ['bruit', 'orphelins', 'budget'] }),
    E('nettoyage', 'Nettoyage', 'A5-10 · A6-F · A6-H', [
      'Orphelins, AA (aucun sous 32 px, et seulement à l\'intérieur du contour, sur les marches de 2 px ou plus ; règle 46).',
      'Yeux plissés, puis palette seule : les grandes masses tiennent (A11-C).',
      'Supprime les pixels de construction.'
    ], { portes: NETTOYAGE }),
    ETAPE_PLANCHE('A5-11 · C8')
  ],
  chibi: [
    ETAPE_FICHE('C13 · C0 · A3'),
    E('construction', 'Construction (rouge, bleu, vert)', 'C13-A', [
      '2,5 à 3 têtes. La tête fait environ 40 % de la hauteur.',
      'Tête ronde ou ovale, jamais en œuf. Aucune épaule marquée.'
    ], { pasEncore: 'Aucun pixel final.', portes: ['construction'], coches: [C('tetes', '2,5 à 3 têtes, tête ≈ 40 %')] }),
    E('silhouette', 'Silhouette du corps nu, pixel-perfect', 'C13-B · C14-A', [
      'Pas d\'épaule : le trait descend du cou en pente régulière (1 px par rangée) jusqu\'au bras collé au torse.',
      'Une rangée de plus sous les pieds.'
    ], { portes: ['nonVide', 'silhouette1', 'L'], coches: [C('epaule', 'Aucune épaule marquée')] }),
    E('ombres', 'Ombres du corps (3 tons de peau)', 'C13-B · C14-A', [
      '3 tons de peau, lumière haut-gauche.',
      'Jointures : aisselle (creux 1 px), coude (pli 1 px), poignet resserré, aine en V, rotule claire + ombre dessous, cheville resserrée.'
    ], { portes: ['coussin', 'L'], coches: [C('jointures', 'Les 6 jointures sont marquées')] }),
    E('corps', 'Corps final validé', 'C13-B · C14-A', [
      'Planche du corps seul (onglet Contrôle) : silhouette, ombres, ×1.',
      'Le corps validé ne se retouchera plus.'
    ], { portes: ['L', 'orphelins', 'coussin'], coches: [C('valide', 'Corps validé sur la planche')] }),
    E('vetements', 'Vêtements en calque', 'C14-B', [
      'Aplats 1 px au-delà du corps, ombres, contour du calque seul.'
    ], { portes: ['L', 'orphelins'], coches: [C('epaisseur', 'Le tissu dépasse d\'1 px')] }),
    E('visage', 'Visage', 'C13-C', ['L\'œil chibi en 64 px : au moins 4×3 avec du blanc.'], { coches: [C('oeil', 'Yeux lisibles à ×1')] }),
    E('cheveux', 'Cheveux en calque', 'C6 · C13-D', [
      'Une masse casque, puis frange en pointes d\'au moins 2 rangées (3 px de large).'
    ], { portes: ['L', 'orphelins'], coches: [C('meches', 'Pointes d\'au moins 2 rangées')] }),
    E('fin', 'Accessoires et nettoyage', 'C13-B · A5-10', ['Accessoires, puis chasse aux défauts.'], { portes: NETTOYAGE }),
    ETAPE_PLANCHE('A5-11 · C8')
  ],
  creature: [
    ETAPE_FICHE('C15 · C0 · A3'),
    E('silhouette', 'Silhouette selon le langage de formes', 'C15-A · C15-B', [
      'Rond = doux, triangle = dangereux, carré = lourd : il dicte tête, yeux, pieds.',
      'Refais la silhouette tant qu\'elle forme un bloc : il faut des vides.',
      'Pattes lointaines plus sombres et plus courtes (C15-C).'
    ], { portes: ['nonVide', 'silhouette1'], coches: [C('vides', 'Des vides : pas un bloc'), C('langage', 'Le langage de formes se voit')] }),
    E('contour', 'Contour', 'A5-6', ['1 px, aucun L, courbes régulières.'], { portes: ['L', 'jaggies'] }),
    E('aplats', 'Palette et aplats', 'A5-7 · C15-G', ['Une rampe par matière, un seul accent saturé.'], { portes: ['budget', 'rampesGris'] }),
    E('lumiere', 'Lumière', 'A5-8 · C15-D', [
      'Une source haut-gauche. Matière émissive : elle éclaire autour d\'elle et n\'a pas d\'ombre propre.'
    ], { portes: ['coussin', 'bandes'], coches: [C('grisOmbre', 'Ombres lues en gris (règle 43)')] }),
    E('bords', 'Bords intérieurs à la main', 'C15-E', ['Sépare les pièces qui se chevauchent par un trait posé à la main.'], { portes: ['L'] }),
    E('details', 'Détails et marqueurs', 'A5-9 · C15-F', ['Les 2-3 marqueurs d\'abord, le reste en groupes de 2-3.'], { portes: ['bruit', 'orphelins'] }),
    E('nettoyage', 'Nettoyage', 'A5-10 · A6-H', ['Chasse aux défauts.'], { portes: NETTOYAGE }),
    ETAPE_PLANCHE('A5-11 · C15')
  ],
  animation: [
    ETAPE_FICHE('E0 · E1'),
    E('poses', 'Poses de départ et de fin finies', 'E0-2', [
      'Image 1 et dernière image : chacune passe par tout le pipeline avant la suite.'
    ], { portes: ['nonVide', 'L', 'coussin'], coches: [C('finies', 'Les deux poses sont finies et validées')] }),
    E('timing', 'Feuille de timing', 'E0-3 · E3 · E2-A', [
      'Panneau Aperçu → Images : pour chaque image, rôle (clé, extrême, passage, intervalle, tenue), ce qui change, principe, durée en ms.',
      'Les clés et l\'impact tiennent 3 à 4 fois plus longtemps (règle 29).'
    ], { portes: ['timing'] }),
    E('poseapose', 'Pose à pose', 'E0-4 · E1', [
      'Clés → extrêmes → passages → intervalles. Effets dans un calque à part.',
      'Pelure d\'oignon pour placer chaque pièce.',
      'Petit mouvement (respiration, cheveux, flamme) : change les couleurs du bord, pas la silhouette (sous-pixel, E2-D, règle 48).'
    ], { portes: ['timing'], coches: [C('ordre', 'Clés, puis extrêmes, puis passages, puis intervalles')] }),
    E('pipeline', 'Tout le pipeline par image', 'E0-5 · E5-A', [
      'Chaque image : silhouette → contour → aplats → lumière → détails → contrôle, puis coche « validée ».',
      'Copier l\'image précédente est permis seulement si les 5 étapes sont refaites.'
    ], { portes: ['imagesValidees', 'Ltoutes'], coches: [C('contour', 'Contour fermé sans L ni bruit sur chaque image'), C('volume', 'Volume rigide constant')] }),
    E('sequence', 'Contrôle de la séquence', 'E5-B · E2', [
      'Bande, pelure d\'oignon, GIF aux vraies durées regardé 3 fois.',
      'Note au moins un défaut, corrige l\'image fautive, refais la bande.'
    ], { portes: ['imagesValidees'] }),
    ETAPE_PLANCHE('A5-11 · E5')
  ],
  decor: [
    ETAPE_FICHE('F0 · F1'),
    E('palette', 'Palette du lieu', 'F4 · F1', [
      'Plan jouable au milieu des valeurs ; fond plus clair et désaturé ; premier plan sombre.',
      'Le personnage et les dangers gardent le plus fort contraste (règle 34).'
    ], { portes: ['rampesGris'], coches: [C('hierarchie', 'Hiérarchie de contraste respectée')] }),
    E('tuile', 'Tuile de base', 'F2-A', [
      'Active le mode tuile (onglet Tuiles) : regarde la grille 3×3 en continu.',
      'Pas de sujet unique au centre. Faible contraste interne (2-3 tons). Lumière commune. Bas de mur plus sombre.'
    ], { portes: ['nonVide', 'tuileOn', 'raccords', 'orphelins', 'bruit'], coches: [C('centre', 'Aucun gros sujet au centre')] }),
    E('variantes', 'Casser la répétition', 'F2-B · F2-C', [
      '1 à 3 variantes, décors posés à la main, éléments qui chevauchent la grille.',
      'Autotile : teste les formes en U, L et îlot.'
    ], { portes: ['raccords'], coches: [C('variantes', '1 à 3 variantes')] }),
    E('carte', 'Carte et scène', 'F6 · F3', [
      'Peins une carte 20×12 dans l\'onglet Tuiles et regarde-la dézoomée.',
      'Agrandis seulement par un entier, une seule taille de pixel (règle 37).'
    ], { portes: ['carte'] }),
    ETAPE_PLANCHE('A5-11 · F6')
  ],
  etude: [
    ETAPE_FICHE('G2'),
    E('choisir', 'Choisir une pièce', 'G2', ['Importe-la dans un calque de référence. Crédite l\'artiste.'], { portes: ['reference'] }),
    E('analyser', 'Analyser avant de copier', 'G2', [
      'Compte les couleurs, décris la rampe, la lumière, le contour, le selout, l\'AA, la trame. Écris-le.'
    ], { portes: ['analyse'] }),
    E('copier', 'Copier pixel par pixel à côté', 'G2', ['À côté de l\'original, jamais par-dessus.'], { portes: ['nonVide'] }),
    E('memoire', 'Refaire de mémoire et comparer', 'G2', ['Cache la référence, refais, puis compare et note les écarts.'], { coches: [C('compare', 'Écarts notés')] }),
    E('reutiliser', 'Réutiliser une technique', 'G2', ['Note la technique à réutiliser dans la semaine.'], { portes: ['planche'] })
  ]
};

/* ---------- Méthode v17 : dessiner avant de pixelliser (partie 0) ----------
 * Les documents créés avant la v17 gardent leurs étapes (ETAPES_V16) : une séance
 * filmée se recharge toujours terminée. */
const PORTES_VOLUME = ['lumierePosee', 'volume', 'coussin', 'lumiere'];
const ETAPES_V17 = Object.assign({}, ETAPES_V16, {
  objet: [
    ETAPE_FICHE('B0 · B0b · A3 · 0-J'),
    E('construction', 'Construire en volumes (dessiner à travers)', '0-B · 0-F · B2', [
      'Dans un calque de construction : l\'axe de symétrie, puis chaque volume ENTIER, même sa partie cachée (sphère, cylindre, boîte).',
      'Les ellipses (ouverture, niveau du liquide, base) sont de vraies ellipses, alignées sur l\'axe ; plus elles sont loin du niveau de l\'œil, plus elles s\'ouvrent (0-F).',
      'Grand, moyen, petit : une masse domine (A4b). Compare les proportions à la référence.',
      'Pose ensuite la lumière (onglet Lumière) pour voir le guide sur la construction.'
    ], { pasEncore: 'Aucun pixel final : seulement le calque de construction.', portes: ['construction'], outils: ['ellipse', 'ligne', 'rect'],
      coches: [C('entier', 'Chaque volume est dessiné entier, partie cachée comprise'), C('ellipses', 'Les ellipses s\'ouvrent à mesure qu\'elles s\'éloignent du niveau de l\'œil'), C('proportions', 'Proportions comparées à la référence ou au guide grand/moyen/petit')] }),
    E('forme', 'Trait de la forme', 'B6-A · A5-6 · 0-E', [
      'Sur un calque normal, repasse la construction d\'un trait sombre et neutre, 1 px, pixel-perfect.',
      'Le trait suit le volume : des courbes tendues contre des droites (0-E), pas des bosses molles.',
      'Largeur impaire si l\'objet est symétrique.'
    ], { pasEncore: 'Pas de couleur, pas de détail.', portes: ['nonVide', 'L', 'jaggies'], outils: ['ligne', 'ellipse'],
      coches: [C('miroir', 'Vue miroir regardée : aucune pente fausse'), C('tendu', 'Courbes tendues, aucune bosse molle')] }),
    E('deformer', 'Déformer et séparer', 'B6-A · B6-B', [
      'Casse les coins, sépare les grandes pièces (bouchon, col, panse…).',
      'Ce qui est derrière (paroi arrière d\'un verre, face cachée) se dessine aussi s\'il se voit à travers.'
    ], { pasEncore: 'Pas de couleur.', portes: ['L', 'jaggies'], coches: [C('masses', 'Une forme dominante, une moyenne, une petite')] }),
    E('aplats', 'Couleur locale à plat', 'B6-A · A5-7 · 0-G', [
      'Un aplat par matière, dans le ton moyen de sa rampe (la couleur locale, sans lumière).',
      'Verre : la couleur de ce qu\'on voit au travers, un peu assombrie et teintée, pas une couleur opaque (0-I).',
      'Vérifie les valeurs en gris : chaque matière a la sienne.'
    ], { pasEncore: 'Pas d\'ombre.', portes: ['L', 'jaggies', 'budget', 'rampesGris'], coches: [C('gris', 'Les matières se séparent en gris')] }),
    E('lumiere', 'Placer la lumière, deux familles', '0-C · 0-D', [
      'Onglet Lumière : choisis la direction et la hauteur, puis affiche le guide.',
      'Dans chaque matière, DEUX valeurs seulement : la famille lumière et la famille ombre. Rien d\'autre.',
      'Le terminateur (frontière des deux) suit la forme : une courbe qui épouse le volume, à l\'opposé de la source.',
      'Vue Notan : deux grandes masses lisibles. Une lumière qui tombe dans l\'ombre, ou l\'inverse, est une faute.'
    ], { pasEncore: 'Pas de demi-ton, pas de reflet, pas d\'éclat.', portes: ['lumierePosee', 'volume', 'coussin', 'lumiere', 'L'], outils: ['ombrage'],
      coches: [C('notan', 'Vue Notan : deux masses claires, frontière qui suit la forme'), C('cote', 'L\'ombre est du côté opposé à la source, partout')] }),
    E('modele', 'Modelé : demi-ton, ombre propre, rebond, ombre portée', '0-C · A5-8 · A6-E', [
      'Demi-ton : une bande entre lumière et terminateur, plus large sur une forme douce, étroite sur une arête.',
      'Ombre propre : la plus sombre de l\'ombre, juste après le terminateur.',
      'Lumière réfléchie : plus claire que l\'ombre propre, TOUJOURS plus sombre que le demi-ton (règle 52).',
      'Occlusion : les creux et les contacts sont les points les plus sombres. Ombre portée au sol, plus nette près du contact.'
    ], { portes: PORTES_VOLUME.concat(['bandes']), coches: [C('rebond', 'Rebond plus sombre que la lumière, ombre propre visible'), C('portee', 'Ombre portée ou contact posé (ou raison écrite de s\'en passer)')] }),
    E('matiere', 'Matière : ce que la surface fait de la lumière', '0-I · A5-8b · B6', [
      'Mat (bois, tissu, pierre) : transitions larges, éclat faible ou absent.',
      'Brillant (métal, verre, vernis) : contraste fort, reflets nets qui épousent la forme, reflet de l\'environnement.',
      'Transparent (verre, eau) : on voit ce qui est derrière ; paroi arrière et contenu se dessinent ; l\'éclat est posé SUR le verre, par-dessus le contenu ; le liquide s\'éclaire du côté opposé à la lumière (la lumière le traverse).',
      'Translucide (gelée, peau, feuille, cristal) : lumière diffuse dans la matière, ombre saturée et chaude près du terminateur.'
    ], { portes: PORTES_VOLUME, coches: [C('matiere', 'La matière se reconnaît sans couleur (gris)')] }),
    E('eclats', 'Éclats et contour coloré', 'B6-A · A6-C', [
      'Éclats spéculaires : une FORME qui suit la courbure (arc, fenêtre, croissant), plus 1 ou 2 points, du côté de la lumière.',
      'Selout : le contour prend la couleur sombre de la matière qu\'il borde, plus clair côté lumière.'
    ], { portes: ['orphelins', 'noirPur', 'volume'], coches: [C('selout', 'Contour coloré (selout) posé maintenant, pas avant'), C('forme', 'Les éclats suivent la courbure de la surface')] }),
    E('contrejour', 'Contre-jour', 'B6-A · B6-G', [
      'Une 2e lumière, opposée, d\'une autre teinte, fine (1 px sur le bord), seulement sur les bords du côté ombre.'
    ], { coches: [C('autre', 'Le contre-jour a une autre teinte que la lumière principale')] }),
    E('teinte', 'Variation de couleur', 'B6-A · A5-8c · 0-G', [
      'Les ombres virent au froid, les lumières au chaud, sans changer les valeurs.',
      'La saturation la plus forte est dans le demi-ton et au bord du terminateur, pas dans la lumière (0-G).',
      'Vérifie en gris que rien n\'a bougé.'
    ], { portes: ['rampesGris', 'volume'], coches: [C('froid', 'Ombres plus froides, valeurs inchangées en gris')] }),
    E('details', 'Détails et nettoyage', 'B6-A · A6-H · A5-10', [
      'Détails dans le demi-ton et l\'ombre, la lumière reste calme (A4).',
      'Fissure ou gravure = trait sombre + lèvre claire d\'1 px, attachée à une arête (règle 41).',
      'Chasse les défauts : L, jaggies, orphelins, banding, coussin, bruit.',
      'Supprime les calques de construction de l\'export.'
    ], { portes: NETTOYAGE.concat(['volume']), coches: [C('levre', 'Fissures avec lèvre claire'), C('lisible', 'Chaque étape se lit à ×1'), C('aa', 'AA seulement sur les marches de 2 px ou plus, à l\'intérieur ; chaque pixel d\'AA passe le test de l\'enlèvement (règle 46)')] }),
    ETAPE_PLANCHE('A5-11 · B5 · B6-G · 0-J')
  ]
});
// Personnages, chibis, créatures : la lumière se pose et se mesure aussi.
for (const t of ['personnage', 'chibi', 'creature']) {
  ETAPES_V17[t] = ETAPES_V16[t].map(e => {
    if (!['lumiere', 'ombres'].includes(e.id)) return e;
    return Object.assign({}, e, {
      faire: ['Onglet Lumière : pose la direction et affiche le guide ; deux familles d\'abord (0-D), puis demi-ton, ombre propre et rebond (0-C).'].concat(e.faire),
      portes: [...new Set(['lumierePosee', 'volume'].concat(e.portes))],
      coches: e.coches.concat([C('notan', 'Vue Notan : deux masses claires')])
    });
  });
}
/* Vision et essais (0-N) : avant tout trait, écrire ce qu'on voit et l'éprouver. */
const RUBRIQUES = {
  vision: 'Ce que je vois', structure: 'Structure / physionomie', formes: 'Formes de base',
  unique: 'Ce qui la rend unique', logique: 'Pourquoi c\'est crédible', variante: 'Variante (SCAMPER, tableau)', essai: 'Essai', iteration: 'Itération', detail: 'Détail travaillé', passe: 'Passe de rendu', reference: 'Référence (avec sa source)', critique: 'Critique (note sur 30)', piece: 'Pièce (bouchon, jonction, pied)', choix: 'Choix retenu'
};
const AIDE_STRUCTURE = {
  objet: 'De quoi il est fait, comment ses pièces tiennent ensemble, comment on le tient ou l\'utilise (la forme suit la fonction).',
  personnage: 'Squelette, proportions en têtes, appuis, ce que le corps dit de sa vie (métier, âge, force).',
  chibi: 'Proportions 2,5 à 3 têtes, ce qu\'on exagère, ce qu\'on supprime.',
  creature: 'Squelette de quels animaux réels, type de pied (plantigrade, digitigrade, onguligrade), comment elle se tient, se déplace, mange, se défend (0-N, 0-U).',
  decor: 'Ce qui porte, ce qui est porté, ce qui pousse dessus, d\'où vient la lumière.',
  animation: 'Ce qui est rigide, ce qui est souple, d\'où part le mouvement.'
};
const ETAPE_VISION = (type) => E('vision', 'Vision : écrire ce que je vois', '0-N', [
  'Avant tout trait : écris dans le carnet ce que tu as en tête, une idée à la fois. On n\'efface rien : une idée qui ne tient pas se BARRE, avec la raison.',
  'Ce que je vois : l\'impression d\'ensemble, l\'ambiance, ce qu\'on doit sentir en 1 seconde.',
  'Structure : ' + (AIDE_STRUCTURE[type] || AIDE_STRUCTURE.objet),
  'Formes de base : de quelles primitives on part (sphère, cylindre, boîte, cône) et comment on les déforme ensuite.',
  'Ce qui la rend unique : UNE idée forte (une forme inattendue, une matière, un détail de récit), pas cinq.',
  'Pourquoi c\'est crédible : même un objet inventé a une logique (comment il tient, s\'ouvre, se remplit, vit).',
  'Variantes : passe la forme connue au SCAMPER et remplis un tableau morphologique (0-P) ; chaque piste va au carnet, puis se garde ou se barre.',
  'Style : rappelle la fiche de style du jeu (contour, angles, ombrage, densité, palette, proportions ; 0-Y) et, pour un être vivant, son type de pied et son squelette (0-U).'
], { pasEncore: 'Aucun pixel : on écrit et on se corrige.', portes: ['carnetVision'] });
const ETAPE_ESSAIS = () => E('essais', 'Essais : vignettes, effacer, recommencer', '0-N · 0-B', [
  'Dans un calque de construction, petit (8 à 16 px de haut) : au moins 3 silhouettes différentes de l\'idée. Pousse chaque essai : ne fais pas deux fois la même.',
  'Après chaque essai, une ligne « Essai » au carnet : ce qui marche, ce qui ne marche pas. Barre les idées que l\'essai a tuées.',
  'Vue miroir et ×1 sur chaque vignette : la silhouette se lit-elle ?',
  'Choisis une vignette et écris le « Choix retenu » : pourquoi celle-là, ce qu\'on va encore pousser.',
  'Efface ou masque les vignettes rejetées avant la construction.'
], { pasEncore: 'Pas de trait final ni de couleur.', portes: ['construction', 'carnetEssais'],
  coches: [C('trois', 'Au moins 3 silhouettes vraiment différentes essayées'), C('lisible', 'La vignette choisie se lit à ×1 et en miroir')] });
for (const t of ['objet', 'personnage', 'chibi', 'creature', 'decor', 'animation']) {
  const L = ETAPES_V17[t].slice(), i = L.findIndex(e => e.id === 'fiche');
  L.splice(i + 1, 0, ETAPE_VISION(t), ETAPE_ESSAIS());
  ETAPES_V17[t] = L;
}
/* ---------- Méthode v21 : le design de la forme d'abord (0-AA) ----------
 * Les essais demandent 6 silhouettes notées, et l'objet gagne l'étape « Design des pièces ». */
const ETAPE_ESSAIS21 = () => E('essais', 'Essais : silhouettes, critique, choix', '0-AA-D · 0-AA-E · 0-N', [
  'Au calque de construction : au moins 6 silhouettes pleines, dans au moins 3 familles d\'analogie (goutte, bourgeon, coquillage…), d\'au moins la moitié de la hauteur finale.',
  'Pour chacune, une ligne « Essai » (ce que c\'est) et une ligne « Critique » : note sur 30 avec la grille 0-AA-E (lisibilité, originalité, appeal, cohérence, rythme, crédibilité).',
  'Barre ce qui est sous 20/30. Garde les 2 meilleures, écris le « Choix retenu » et ce qu\'il faut encore pousser.',
  'Test : la meilleure à côté de trois potions génériques (ronde, conique, carrée). Si on hésite, recommence.'
], { pasEncore: 'Pas de trait final ni de couleur.', portes: ['construction', 'carnetEssais21'],
  coches: [C('familles', 'Au moins 6 silhouettes dans 3 familles différentes'), C('generique', 'La silhouette choisie ne se confond pas avec une potion générique'), C('lisible', 'La silhouette choisie se lit à ×1 et en miroir')] });
const ETAPE_PIECES = () => E('pieces', 'Design des pièces : bouchon, jonctions, pied', '0-AA-B · 0-AA-D', [
  'Sur la silhouette choisie, à la taille finale et au calque de construction : 3 bouchons, 3 jonctions (épaule, bague, lèvre), 3 pieds ou bases, côte à côte.',
  'Chaque variante va au carnet (rubrique « Pièce ») avec ce qu\'elle apporte ; barre celles qui cassent le langage.',
  'Le motif de la panse revient en petit dans le bouchon et dans un détail (trois échelles).',
  'Proportions franches (panse : col : bouchon ≈ 3 : 1,5 : 1, jamais 1:1), ligne de flux en S ou en C, asymétrie franche ou absente.',
  'Assemble la silhouette finale et regarde-la en miroir et à ×1.'
], { pasEncore: 'Pas de trait final ni de couleur.', portes: ['construction', 'carnetPieces'],
  coches: [C('motif', 'Un motif répété à trois échelles'), C('proportions', 'Proportions franches, jamais 1:1'), C('jonctions', 'Chaque jonction est dessinée (épaule, bague, lèvre, tige)'), C('bouchon', 'Le bouchon se lit à ×1 et porte le motif')] });
const ETAPES_V21 = Object.assign({}, ETAPES_V17);
for (const t of Object.keys(ETAPES_V21)) {
  ETAPES_V21[t] = ETAPES_V17[t].map(e => e.id === 'essais' ? ETAPE_ESSAIS21() : e);
  if (t === 'objet') {
    const L = ETAPES_V21[t].slice(), i = L.findIndex(e => e.id === 'essais');
    L.splice(i + 1, 0, ETAPE_PIECES());
    ETAPES_V21[t] = L;
  }
}
/* ---------- Méthode v22 : le sketching d'un illustrateur (0-AB) ----------
 * Rough, construction, esquisse nettoyée, trait, polish, puis validation du dessin
 * avant toute couleur. */
const ETAPES_V22 = Object.assign({}, ETAPES_V21);
{
  const V = ETAPES_V21.objet, par = id => V.find(e => e.id === id);
  const rough = E('rough', 'Rough : le geste et les grandes masses', '0-AB-A · 0-Q', [
    'Nouveau calque de construction « rough », teinte rouge. À la taille finale.',
    'D\'abord la ligne de flux (S ou C) du bouchon au pied, puis les grandes masses en traits longs et libres.',
    'Plusieurs passages superposés sont permis : on cherche, on ne nettoie pas.',
    'Intègre la silhouette et les pièces choisies aux étapes précédentes.'
  ], { pasEncore: 'Pas de trait propre, pas de petit détail.', portes: ['calquesConstr2'], outils: ['crayon', 'ligne', 'ellipse'],
    coches: [C('flux', 'Une ligne de flux traverse l\'objet'), C('masses', 'Les grandes masses sont posées, rien de fini')] });
  const construction = Object.assign({}, par('construction'), {
    titre: 'Construction sur le rough',
    faire: ['Baisse l\'opacité du rough à 30-40 %, puis nouveau calque de construction « volumes », teinte bleue.'].concat(par('construction').faire),
    portes: ['calquesConstr3', 'dessousBaisse']
  });
  const esquisse = E('esquisse', 'Esquisse nettoyée', '0-AB-A · 0-AB-B', [
    'Baisse les calques du dessous à 20-30 %. Nouveau calque de construction « esquisse », teinte verte.',
    'Choisis les traits qui comptent et redessine-les d\'un geste sûr : redessiner plutôt que gommer.',
    'Corrige les proportions, intègre le bouchon, les jonctions et le pied choisis.',
    'Retourne la toile (onglet Lumière, Sur la toile) : ce qui penche ou boite se corrige ici, pas au trait.'
  ], { pasEncore: 'Pas de couleur, pas de trait pixel-perfect.', portes: ['calquesConstr4', 'dessousBaisse'],
    coches: [C('retourne', 'Toile retournée : aucune pente ni proportion fausse'), C('choisis', 'Seuls les traits qui comptent sont gardés')] });
  const trait = Object.assign({}, par('forme'), {
    titre: 'Trait final', ref: '0-AB-A · A5-6 · 0-E',
    faire: ['Sur un calque normal, redessine l\'esquisse nettoyée en trait pixel-perfect : c\'est un guide, pas un calque à copier.',
      'Courbes tendues (marches qui s\'allongent ou raccourcissent régulièrement), droites aux marches égales.',
      'Largeur impaire si l\'objet est symétrique.']
  });
  const polish = E('polish', 'Polish du trait', '0-AB-A · A5-6 · A8 · 0-H', [
    'Régularise chaque courbe (aucun L, aucun jaggy), nettoie chaque jonction.',
    'Poids du trait : contour extérieur plein et sombre ; traits intérieurs d\'un ton plus clair ou interrompus.',
    'Ajoute les petits détails de forme : lèvre, bague, facettes du bouchon. Rien d\'autre.',
    'Retourne la toile et regarde à ×1 après chaque passe.'
  ], { pasEncore: 'Pas de couleur.', portes: ['nonVide', 'L', 'jaggies', 'orphelins'],
    coches: [C('poids', 'Contour plus fort que les traits intérieurs'), C('jonctions', 'Chaque jonction est nette et dessinée')] });
  const validation = E('validation', 'Validation du dessin (avant la couleur)', '0-AB-C · 0-AA-E', [
    'Planche du trait : ×1, ×2, retourné, silhouette (onglet Contrôle).',
    'Note la forme avec la grille 0-AA-E et écris-la au carnet (rubrique « Critique », « xx/30 ») : 22 au moins.',
    'Compare avec l\'œuvre visée et écris l\'écart.',
    'Arrête-toi et montre le dessin à l\'humain. Sous 22/30, reviens au rough ou à l\'esquisse, pas au trait.'
  ], { pasEncore: 'Aucune couleur tant que le dessin n\'est pas validé.', portes: ['critiqueDessin', 'L', 'jaggies'],
    coches: [C('planche', 'Trait regardé à ×1, ×2, retourné et en silhouette'), C('reference', 'Écart avec l\'œuvre visée écrit au carnet'), C('montre', 'Dessin montré à l\'humain avant la couleur')] });
  // v23 (0-AC) : le trait seul doit passer pour un sketch fini de pro
  validation.faire = validation.faire.concat(['Sketch fini (0-AC) : l\'idée se lit en silhouette noire ; trois poids de trait partout ; recouvrements nets ; lignes de forme qui disent le volume. Montré tel quel, il doit passer pour une planche de concept art.']);
  validation.portes = validation.portes.concat(['taille64']);
  validation.coches = [C('silhouetteIdee', 'L\'idée se lit en silhouette noire, sans trait intérieur'), C('poids', 'Trois poids de trait (fort, moyen, fin) appliqués partout'), C('recouvrements', 'Chaque recouvrement est net, lignes de forme présentes')].concat(validation.coches);
  const L = [];
  for (const e of V) {
    if (e.id === 'construction') { L.push(rough, construction, esquisse); continue; }
    if (e.id === 'forme') { L.push(trait); continue; }
    if (e.id === 'deformer') { L.push(polish, validation); continue; }
    L.push(e);
  }
  ETAPES_V22.objet = L;
}
/* ---------- Méthode v24 : itérer sur une forme de base (0-AD) ----------
 * On ne cherche plus six silhouettes différentes pour en choisir une : on part d'une forme
 * de base simple et on la pousse par itérations, chacune critiquée. Le décor devient un vrai
 * pipeline de tileset de plateforme (F2-F). */
const ETAPE_ITERATIONS = () => E('iterations', 'Itérations sur une forme de base', '0-AD · 0-AA-E', [
  'Pars d\'une forme de base simple (bloc, sphère, cylindre, rectangle aux coins cassés), à la taille finale, dans un calque de construction « v1 ».',
  'Itère sur la MÊME forme : chaque version dans un nouveau calque de construction (v2, v3…), celle du dessous baissée ou masquée. Une ou deux choses changent à chaque fois : proportions, coins, rythme du contour, une pièce, la place des masses.',
  'Après chaque version : une ligne « Itération » au carnet (ce qui change et pourquoi) et une « Critique » notée sur 30 avec la grille 0-AA-E. Ce qui n\'a pas marché se barre, avec la raison.',
  'Au moins 3 versions. Garde la meilleure et écris le « Choix retenu » : ce qu\'elle a gagné sur la v1 et ce qu\'il faut encore pousser.'
], { pasEncore: 'Pas de trait final ni de couleur. Pas de forme radicalement différente : on améliore la même.', portes: ['construction', 'carnetIterations'],
  coches: [C('base', 'Parti d\'une forme de base simple'), C('trois', 'Au moins 3 versions de la même forme, chacune critiquée'), C('mieux', 'La version retenue est mieux notée que la v1')] });
const ETAPES_V24 = {};
for (const t of Object.keys(ETAPES_V22)) ETAPES_V24[t] = ETAPES_V22[t].filter(e => e.id !== 'pieces').map(e => e.id === 'essais' ? ETAPE_ITERATIONS() : e);
ETAPES_V24.decor = [
  ETAPE_FICHE('F0 · F1 · F2-F'),
  ETAPE_VISION('decor'),
  ETAPE_ITERATIONS(),
  E('palette', 'Palette du lieu', 'F4 · F1', [
    'Plan jouable au milieu des valeurs ; fond plus clair et désaturé ; premier plan sombre.',
    'Une rampe par matière (croûte, terre ou pierre, détails), qui partagent leurs tons sombres. Peu de couleurs par texture : trop de tons rendent la texture floue (F2-F).',
    'Le personnage et les dangers gardent le plus fort contraste (règle 34).'
  ], { portes: ['rampesGris'], coches: [C('hierarchie', 'Hiérarchie de contraste respectée'), C('peu', '3 ou 4 tons par matière, pas plus')] }),
  E('gabarit', 'Gabarit en aplats et carte de test', 'F2-C · F2-F', [
    'Onglet Tuiles : mode tuile, taille de tuile de la fiche. Planche : bloc 3×3 (coins, bords, centre) en colonnes 1-3, coins rentrants en colonnes 4-5, plateformes et décors en dessous.',
    'Sur le calque normal (la carte de test ne montre que ce qui s\'exporte), pose chaque tuile en GRANDS APLATS (blocage de couleur) : croûte claire, face moyenne, bas plus sombre. Pas de texture.',
    'Peins tout de suite une carte de test (pinceau Terrain) en U, en L et en îlot : un carré qui dépasse dans un coin rentrant veut dire qu\'il manque la tuile de coin intérieur.',
    'Les bords ne sont jamais des rectangles parfaits : coins arrondis ou cassés, croûte qui déborde un peu sur la face.'
  ], { pasEncore: 'Pas de texture, pas de détail.', portes: ['tuileOn', 'construction', 'carteTerrain'], outils: ['rect', 'seau', 'crayon'],
    coches: [C('gabarit', 'Toutes les tuiles du gabarit sont posées en aplats'), C('carte', 'Carte de test en U, L et îlot sans trou ni carré qui dépasse')] }),
  E('centre', 'Tuile centrale en strates', 'F2-A · F2-F', [
    'Sur le calque normal : la tuile centrale d\'abord, comme une coupe de terrain. Grandes masses (strates, gros blocs), puis clusters moyens, puis quelques petits.',
    'Des clusters francs et de tailles proches ; des clusters clés répétés à plusieurs endroits, jamais collés entre eux (un contact coin à coin suffit).',
    'Les clusters passent par-dessus les bords et tournent autour de la tuile : décalage cyclique (onglet Calques) pour vérifier qu\'aucune couture ne se voit.',
    'Poids visuel égal partout dans la tuile : pas de gros sujet au centre, pas de coin vide.'
  ], { pasEncore: 'Pas encore les bords ni les coins.', portes: ['nonVide', 'raccords', 'orphelins', 'bruit'],
    coches: [C('strates', 'Grandes masses, puis clusters moyens, puis petits'), C('centre', 'Aucun gros sujet au centre, poids égal'), C('raccords', 'Décalée d\'une demi-tuile, la tuile ne montre aucune couture')] }),
  E('bords', 'Bords, coins et coins rentrants', 'F2-C · F2-D · F2-F', [
    'Le dessus d\'abord : la croûte (herbe, mousse, neige) se construit de bas en haut, du plus sombre au plus clair, en touffes qui débordent un peu ; une ombre entre la croûte et la face.',
    'Puis le bas (fissures, terre plus sombre) et les côtés (on repart du centre, on prolonge les clusters jusqu\'au bord). Avec une lumière zénithale, le côté droit est le miroir du gauche.',
    'Les coins partent des bords haut et bas : on fait tourner les fissures et la croûte autour du coin, et on éclaire l\'arête.',
    'Coins rentrants : le centre plus une ombre de transition sous la croûte, comme au bord haut. Vérifie tout sur la carte de test.'
  ], { pasEncore: 'Pas d\'éclat ni de décor.', portes: ['raccords', 'L', 'orphelins'],
    coches: [C('croute', 'Même hauteur de croûte partout'), C('coins', 'Coins arrondis ou cassés, arête du coin éclairée'), C('carte', 'Carte de test regardée : aucun raccord ne casse')] }),
  E('lumiere', 'Lumière et volume des blocs', 'F2-A · F2-D · 0-C', [
    'Onglet Lumière : la même lumière pour tout le jeu. Zénithale (haut) si les tuiles doivent se retourner en miroir.',
    'Le haut d\'un bloc s\'éclaire, la face s\'assombrit vers le bas, les creux et le dessous de la croûte sont les plus sombres (occlusion).',
    'Chaque cluster a sa lumière : arête claire du côté de la source, ombre propre de l\'autre. Pas d\'ombre coussin autour des clusters.',
    'Vue Notan : la croûte claire et le bloc sombre se lisent en deux masses.'
  ], { portes: ['lumierePosee', 'coussin', 'L'], outils: ['ombrage'],
    coches: [C('haut', 'Haut éclairé, bas plus sombre, dessous de croûte ombré'), C('clusters', 'Chaque cluster est éclairé du même côté')] }),
  E('variantes', 'Plateformes, variantes et décors', 'F2-B · F2-D · F2-F', [
    'Plateforme traversable : bout gauche, milieu, bout droit ; un appui dans le fond la rattache au décor.',
    '1 à 3 variantes des tuiles qu\'on aligne souvent (centre, bord haut), issues de la première par petites retouches.',
    'Décors posés par-dessus et hors grille : touffes, fleurs, cailloux, racines, qui cachent le dessus plat sans toucher aux collisions.'
  ], { portes: ['raccords', 'orphelins'], coches: [C('plateforme', 'Plateforme en trois pièces posée'), C('variantes', '1 à 3 variantes'), C('decors', 'Décors hors grille qui cassent la répétition')] }),
  E('carte', 'Carte et scène', 'F6 · F3 · F1', [
    'Peins une carte 20×12 dans l\'onglet Tuiles (terrain, plateformes, décors) et regarde-la dézoomée : la répétition se voit de loin.',
    'Passe-la en gris : le plan jouable se lit d\'abord ; la croûte dit « on peut marcher ici ».',
    'Agrandis seulement par un entier, une seule taille de pixel (règle 37).'
  ], { portes: ['carteTerrain', 'carte'], coches: [C('loin', 'Carte regardée dézoomée : pas de grille visible'), C('gris', 'En gris, le plan jouable se lit')] }),
  E('details', 'Détails et nettoyage', 'A6-H · A5-10', [
    'Quelques détails dans les zones calmes : fissure (trait sombre + lèvre claire), racine, éclat d\'une pierre. Le dessus reste lisible.',
    'Chasse les défauts : L, orphelins, banding, coussin, bruit. Les calques de construction ne s\'exportent pas.'
  ], { portes: NETTOYAGE.filter(p => p !== 'superpixels'), coches: [C('lisible', 'Lisible à ×1 sur la carte')] }),
  ETAPE_PLANCHE('A5-11 · F6')
];
/* ---------- Méthode v25 : chaque détail travaillé comme un dessin entier (0-AE) ----------
 * Un modèle (une tuile, un objet) ne se fait qu'une fois : chaque élément complexe (une pierre,
 * une motte, un pétale, une boucle, un œil) se traite comme un pixel art complet, à la loupe,
 * zone par zone, sans limite de temps. Chaque élément retravaillé laisse une ligne au carnet. */
const ETAPE_MICRO = (n, quoi) => E('micro', 'Micro-détails : chaque élément comme un dessin entier', '0-AE', [
  'Loupe : passe ' + quoi + ' zone par zone (8×8 ou 16×16). Chaque élément (une pierre, une motte, un brin, une fissure, un pétale, une boucle, un œil) se dessine comme un pixel art complet : silhouette lisible, sa propre lumière, 2 ou 3 tons, contour décidé, aucun pâté.',
  'Pour chaque élément, la même démarche que pour le dessin entier : la forme de base, puis une ou deux itérations jusqu\'à ce qu\'il soit juste. Pas de limite de temps : on ne fait ce modèle qu\'une fois.',
  'Après chaque élément retravaillé : une ligne « Détail » au carnet (ce que c\'est, ce qui clochait, ce qui a changé). ' + n + ' éléments au moins.',
  'Puis un regard d\'ensemble (×1, carte ou planche dézoomée) : le détail sert la lecture, il ne fait pas de bruit ; les clusters restent francs.'
], { pasEncore: 'Pas de nouvel élément : on perfectionne ceux qui existent.', portes: ['carnetDetails' + n],
  coches: [C('loupe', 'Chaque zone regardée à la loupe et retravaillée'), C('element', 'Chaque élément a sa silhouette, sa lumière et 2 ou 3 tons'), C('ensemble', 'Vu de loin, le détail ne fait pas de bruit')] });
const ETAPES_V25 = {};
for (const t of Object.keys(ETAPES_V24)) {
  const L = ETAPES_V24[t].slice();
  if (t === 'decor') {
    // la tuile centrale se perfectionne avant d'être recopiée dans les bords (MortMort, F2-F)
    L.splice(L.findIndex(e => e.id === 'centre') + 1, 0, ETAPE_MICRO(8, 'la tuile centrale'));
    const i = L.findIndex(e => e.id === 'details');
    L[i] = Object.assign({}, L[i], { portes: L[i].portes.concat(['carnetDetails16']), faire: ['Repasse les bords, les coins et la plateforme à la loupe comme la tuile centrale (0-AE) : une ligne « Détail » par élément retravaillé, 16 au total.'].concat(L[i].faire) });
  } else if (t !== 'animation' && t !== 'etude') {
    const i = L.findIndex(e => ['details', 'fin', 'nettoyage'].includes(e.id));
    if (i > 0) L.splice(i, 0, ETAPE_MICRO(8, 'tout le dessin'));
  }
  ETAPES_V25[t] = L;
}
/* ---------- Méthode v26 : rendu par passes et par unités, passe à la loupe zone par zone (0-AF) ----------
 * Leçons des planches pro [P5] : chaque unité (brique, pierre, feuille, planche) se dessine et
 * s'éclaire une par une ; des rampes riches (6 à 8 tons) ; des facettes ; des taches irrégulières ;
 * une matière secondaire ; six passes de rendu ; puis chaque zone de 8×8 ou 16×16 se retravaille
 * et se marque. */
const PASSES = [
  '1. Bandes de valeur : la tuile (ou l\'objet) en 2 ou 3 grands aplats (dessus, corps, pied sombre).',
  '2. Structure : dessine chaque unité une par une (brique, pierre, motte, feuille) — toutes de tailles et de formes différentes, joints irréguliers et cassés.',
  '3. Matière secondaire et usure : fissures, éclats, mousse ou herbe sur les faces qui regardent la lumière, transition qui coule entre deux matières.',
  '4. Ombres par unité : le bas de chaque unité, l\'occlusion dans les joints et sous les recouvrements ; le quasi-noir coloré seulement au fond des creux.',
  '5. Volume par unité : chaque unité en facettes (dessus clair, faces moyennes, dessous sombre) et des taches irrégulières de 2 à 6 px pour l\'usure ; la texture suit la forme (fil du bois, strates).',
  '6. Éclats : un liseré clair de 1 px sur l\'arête haute de chaque unité, quelques points sur les arêtes les plus exposées ; contraste final.'
];
const ETAPES_V26 = {};
for (const t of Object.keys(ETAPES_V25)) {
  ETAPES_V26[t] = ETAPES_V25[t].map(e => {
    if (e.id === 'micro') return Object.assign({}, e, {
      faire: e.faire.concat(['Passe à la loupe (onglet Méthode) : choisis la taille de zone, va de zone en zone ; chaque zone se retravaille entièrement puis se marque « retravaillée ».']),
      portes: e.portes.concat([t === 'decor' ? 'zonesTuile' : 'zonesToutes', 'tampons'])
    });
    if (t === 'decor' && e.id === 'centre') return Object.assign({}, e, {
      titre: 'Tuile centrale : six passes de rendu', ref: 'F2-A · F2-F · 0-AF',
      faire: ['Écris d\'abord la tuile en grille (1 caractère = 1 pixel) ou dessine-la passe par passe ; une ligne « Passe de rendu » au carnet après chaque passe.'].concat(PASSES, ['Raccords : les unités passent par-dessus les bords et tournent autour de la tuile. Poids visuel égal, pas de gros sujet au centre.']),
      portes: e.portes.concat(['carnetPasses'])
    });
    if (t === 'decor' && e.id === 'palette') return Object.assign({}, e, {
      faire: ['Une rampe par matière, de 6 à 8 tons, avec décalage de teinte (ombres vers le violet ou le bordeaux, lumières vers le jaune ou la menthe) ; un quasi-noir coloré partagé pour les creux et le contour (0-AF).'].concat(e.faire.filter(x => !/3 ou 4|Peu de couleurs/.test(x))),
      coches: [C('hierarchie', 'Hiérarchie de contraste respectée'), C('riche', '6 à 8 tons par matière, teinte décalée, quasi-noir coloré pour les creux')]
    });
    if (t === 'decor' && e.id === 'bords') return Object.assign({}, e, { faire: e.faire.concat(['Chaque bord et chaque coin repasse les six passes sur ce qu\'il ajoute : brins un par un, pierres de bord une par une, fissures avec lèvre claire (0-AF).']) });
    if (e.id === 'details') return Object.assign({}, e, { portes: [...new Set(e.portes.concat(['zonesToutes']))] });
    return e;
  });
}
/* ---------- Méthode v27 : ce qu'on voit en regardant un pro travailler (0-AG) ----------
 * Vidéo d'un pixel artist (cottage isométrique) : grille de projection, rough sale, esquisse codée
 * par pièce, trait pièce par pièce depuis le sol, aplats par orientation de plan, des dizaines de
 * passes de détail avec des couleurs essayées en place, la texture en dernier. */
const AJOUTS_V27 = {
  rough: ['Une grille de projection en fond (onglet Lumière, « Grille isométrique » pour un jeu en iso) : toutes les arêtes la suivent. Une ancienne version du dessin peut rester dessous, en transparence, comme référence.'],
  esquisse: ['Esquisse codée par pièce : une couleur franche par pièce (corps, toit ou bouchon, pied, ornements, matière secondaire). Chaque pièce doit se lire avant le trait (0-AG).'],
  forme: ['Trait propre pièce par pièce, en partant du contact avec le sol : la base, les appuis, puis les grands volumes, puis les pièces secondaires. L\'esquisse codée reste dessous, baissée.'],
  aplats: ['Dès les aplats, chaque plan prend la valeur de son orientation (dessus, face éclairée, face à l\'ombre) : le volume se lit avant toute ombre (0-AG).'],
  micro: ['Des dizaines de petites passes, une chose à la fois (une fenêtre, un volet, une pierre du socle, une fleur). Essaie les couleurs en place, sur le dessin : garde celle qui sert la lecture, barre l\'autre au carnet.'],
  matiere: ['La texture qui couvre une grande surface (tuiles, écorce, briques, pavés) se pose en dernier, quand la forme est juste ; ses rangées suivent la courbure du volume.'],
  eclats: ['À la fin, le trait sombre devient un contour coloré par matière ; on présente le dessin sur un petit socle de décor (herbe, ombre) qui le pose dans le monde.']
};
const ETAPES_V27 = {};
for (const t of Object.keys(ETAPES_V26)) ETAPES_V27[t] = ETAPES_V26[t].map(e => AJOUTS_V27[e.id] ? Object.assign({}, e, { faire: e.faire.concat(AJOUTS_V27[e.id]) }) : e);
/* ---------- Méthode v28 : des références documentées avant de dessiner (0-AH) ----------
 * Chercher comment le sujet est fait dans la réalité (structure, matière, usure, où pousse quoi)
 * et comment des pros le dessinent ; l'écrire au carnet avec la source, puis s'en servir. */
const ETAPES_V28 = {};
for (const t of Object.keys(ETAPES_V27)) ETAPES_V28[t] = ETAPES_V27[t].map(e => e.id !== 'vision' ? e : Object.assign({}, e, {
  titre: 'Vision et références : écrire ce que je vois, chercher ce qui existe',
  faire: e.faire.concat(['Références (0-AH) : cherche comment le sujet est fait dans la réalité (structure, matière, usure, ce qui pousse où, comment ça casse) et comment des pros le dessinent. Au moins 3 lignes « Référence » au carnet, chacune avec sa source et ce que tu en appliques ; une image de référence peut aller dans un calque de référence (jamais copiée).']),
  portes: e.portes.concat(['carnetReferences'])
}));
const METHODE_ACTUELLE = 28;
const ETAPES = ETAPES_V28;
const etapesDe = doc => {
  const v = (doc.meta && doc.meta.methode) || 0;
  return (v >= 28 ? ETAPES_V28 : v >= 27 ? ETAPES_V27 : v >= 26 ? ETAPES_V26 : v >= 25 ? ETAPES_V25 : v >= 24 ? ETAPES_V24 : v >= 22 ? ETAPES_V22 : v >= 21 ? ETAPES_V21 : v >= 17 ? ETAPES_V17 : ETAPES_V16)[typeDe(doc)];
};
/* Calques de construction qui contiennent des pixels, dans l'ordre de la pile. */
function calquesConstr(doc) {
  return doc.calques.filter(c => c.type === 'construction' && (doc.cels[c.id] || []).some(id => id && doc.celData[id].some(v => v >>> 24)));
}

const TYPES = {
  objet: { nom: 'Objet', ref: 'Partie B' },
  personnage: { nom: 'Personnage', ref: 'Partie C' },
  chibi: { nom: 'Chibi', ref: 'C13' },
  creature: { nom: 'Créature', ref: 'C15' },
  animation: { nom: 'Animation', ref: 'Partie E' },
  decor: { nom: 'Décor / tuiles', ref: 'Partie F' },
  etude: { nom: 'Étude de maître', ref: 'G2' }
};
const typeDe = doc => (ETAPES[doc.type] ? doc.type : 'objet');

function ficheIncomplete(doc) {
  const f = doc.meta.fiche || {}, manque = [];
  for (const c of FICHES[typeDe(doc)]) if (c.requis && !String(f[c.cle] ?? '').trim()) manque.push(c.label);
  return manque.length ? manque : false;
}
function nbEtapes(doc) { return etapesDe(doc).length; }
function etapeCourante(doc) { return etapesDe(doc)[Math.min(doc.meta.etape, nbEtapes(doc) - 1)]; }

/* Zones de la passe à la loupe : celles qui contiennent des pixels exportés. Pour un décor en
 * gabarit, l'étape « Micro-détails » ne demande que les zones de la tuile centrale. */
function zonesAFaire(doc, tuileSeule) {
  const t = (doc.meta.zones && doc.meta.zones.taille) || 16, px = AP.compose(doc, 0, 'export'), L = [];
  let x0 = 0, y0 = 0, x1 = doc.w, y1 = doc.h;
  if (tuileSeule && doc.tuile && doc.tuile.on && doc.w >= 3 * doc.tuile.tw && doc.h >= 3 * doc.tuile.th) { x0 = doc.tuile.tw; y0 = doc.tuile.th; x1 = 2 * x0; y1 = 2 * y0; }
  for (let zy = Math.floor(y0 / t); zy * t < y1; zy++) for (let zx = Math.floor(x0 / t); zx * t < x1; zx++) {
    let plein = false;
    for (let y = zy * t; y < Math.min(doc.h, zy * t + t) && !plein; y++) for (let x = zx * t; x < Math.min(doc.w, zx * t + t); x++) if (px[y * doc.w + x] >>> 24) { plein = true; break; }
    if (plein) L.push(t + ':' + zx + ',' + zy);
  }
  return L;
}

/* ---------- Portes ---------- */
const DET_PORTES = { lumiere: 'lumiere', L: 'L', jaggies: 'jaggies', orphelins: 'orphelins', bandes: 'bandes', coussin: 'coussin', bruit: 'bruit', trame: 'trame', superpixels: 'superpixels', budget: 'budget', noirPur: 'noirPur', rampesGris: 'rampesGris', raccords: 'raccords', alpha: 'alpha', tampons: 'tampons' };
function aDesPixels(doc, filtre) {
  for (const c of doc.calques) {
    if (filtre && !filtre(c)) continue;
    for (const id of doc.cels[c.id] || []) { if (!id) continue; const D = doc.celData[id]; for (let i = 0; i < D.length; i++) if (D[i] >>> 24) return true; }
  }
  return false;
}
function porte(id, at, cache) {
  const doc = at.doc, m = doc.meta, f = at.s.image | 0;
  const det = () => cache.det || (cache.det = AP.detecte(doc, f));
  if (DET_PORTES[id]) {
    const d = det().find(x => x.id === id);
    if (!d || d.niveau === 'conseil') return null;
    if (m.justifs[id]) return null;
    return d.titre + ' (' + d.ref + ')' + (d.pixels.length ? ' : ' + d.pixels.length + ' px' : '') + '. Corrige, ou justifie-le.';
  }
  switch (id) {
    case 'fiche': { const r = ficheIncomplete(doc); return r ? 'Fiche incomplète : ' + r.join(', ') : null; }
    case 'regles': return m.reglesLues ? null : 'Lis les 92 règles impératives et coche « lues ».';
    case 'nonVide': return AP.mesures(doc, f).opaques ? null : 'L\'image exportée est vide.';
    case 'construction': return aDesPixels(doc, c => c.type === 'construction') ? null : 'Dessine la construction dans au moins un calque de type « construction ».';
    case 'silhouette1': { const n = AP.mesures(doc, f).couleurs; return n <= 2 ? null : 'La silhouette se fait en une couleur sombre (2 au plus) : ' + n + ' couleurs.'; }
    case 'lumierePosee': return (doc.lumiere && doc.lumiere.posee) ? null : 'Pose la lumière dans l\'onglet Lumière (direction et hauteur), puis regarde le guide.';
    case 'volume': {
      if (m.justifs.volume) return null;
      const M = AP.VOLUME.mesure(AP.compose(doc, f, 'export'), doc.w, doc.h, AP.VOLUME.lumiereDe(doc));
      if (M.accord === null) return 'Aucune matière ombrée à mesurer : pose les deux familles (lumière, ombre) dans chaque matière.';
      const manque = [];
      if (M.accord < 0.5) manque.push('accord clarté/volume ' + M.accord.toFixed(2) + ' < 0,50');
      if (M.ecart !== null && M.ecart < 0.08) manque.push('lumière et ombre trop proches (' + M.ecart.toFixed(2) + ' < 0,08)');
      if (M.inverses !== null && M.inverses > 0.15) manque.push(Math.round(M.inverses * 100) + ' % de la lumière plus sombre que l\'ombre');
      return manque.length ? 'Volume (0-C) : ' + manque.join(', ') + '. Affiche le guide (onglet Lumière), corrige, ou justifie.' : null;
    }
    case 'carnetVision': {
      const c = m.carnet || [], vivantes = c.filter(e => !e.barre), manque = [];
      for (const r of ['vision', 'structure', 'formes', 'unique', 'logique']) if (!vivantes.some(e => e.rubrique === r)) manque.push('« ' + RUBRIQUES[r] + ' »');
      if (manque.length) return 'Carnet : écris au moins une idée pour ' + manque.join(', ') + '.';
      if (!c.some(e => e.barre)) return 'Carnet : barre au moins une idée en disant pourquoi. On ne tombe pas juste du premier coup (0-N).';
      return null;
    }
    case 'carnetEssais': {
      const c = m.carnet || [];
      const essais = c.filter(e => e.rubrique === 'essai').length, choix = c.filter(e => e.rubrique === 'choix' && !e.barre).length, barres = c.filter(e => e.barre).length;
      const manque = [];
      if (essais < 3) manque.push((3 - essais) + ' ligne(s) « Essai » de plus');
      if (!choix) manque.push('un « Choix retenu »');
      if (barres < 2) manque.push('au moins 2 idées barrées au total');
      return manque.length ? 'Carnet : ' + manque.join(', ') + '.' : null;
    }
    case 'carnetEssais21': {
      const c = m.carnet || [], n = r => c.filter(e => e.rubrique === r).length, manque = [];
      if (n('essai') < 6) manque.push((6 - n('essai')) + ' ligne(s) « Essai » de plus (6 silhouettes au moins)');
      if (n('critique') < 6) manque.push((6 - n('critique')) + ' « Critique » notée(s) de plus');
      if (!c.some(e => e.rubrique === 'choix' && !e.barre)) manque.push('un « Choix retenu »');
      if (c.filter(e => e.barre).length < 3) manque.push('au moins 3 idées barrées au total');
      return manque.length ? 'Carnet : ' + manque.join(', ') + '.' : null;
    }
    case 'carnetDetails6': case 'carnetDetails8': case 'carnetDetails12': case 'carnetDetails16': {
      const n = +id.slice('carnetDetails'.length), k = (m.carnet || []).filter(e => e.rubrique === 'detail' && !e.barre).length;
      return k >= n ? null : 'Carnet : ' + (n - k) + ' « Détail » de plus : chaque élément retravaillé à la loupe laisse une ligne (0-AE).';
    }
    case 'carnetReferences': {
      const k = (m.carnet || []).filter(e => e.rubrique === 'reference' && !e.barre).length;
      return k >= 3 ? null : 'Carnet : ' + (3 - k) + ' « Référence » de plus (comment c\'est fait en vrai, comment des pros le dessinent ; source et ce que tu en appliques, 0-AH).';
    }
    case 'carnetPasses': {
      const k = (m.carnet || []).filter(e => e.rubrique === 'passe' && !e.barre).length;
      return k >= 6 ? null : 'Carnet : ' + (6 - k) + ' « Passe de rendu » de plus (les six passes de 0-AF, une ligne chacune).';
    }
    case 'zonesTuile': case 'zonesToutes': {
      const Z = zonesAFaire(doc, id === 'zonesTuile'), f = (m.zones && m.zones.faites) || {};
      const reste = Z.filter(k => !f[k]);
      return reste.length ? 'Passe à la loupe : ' + reste.length + ' zone(s) sur ' + Z.length + ' à retravailler et marquer (zones de ' + ((m.zones && m.zones.taille) || 16) + ' px).' : null;
    }
    case 'carnetIterations': {
      const c = m.carnet || [], n = r => c.filter(e => e.rubrique === r).length, manque = [];
      const notees = c.filter(e => e.rubrique === 'critique' && /\d+(?:[.,]\d+)?\s*\/\s*30/.test(e.texte)).length;
      if (n('iteration') < 3) manque.push((3 - n('iteration')) + ' « Itération » de plus (3 versions au moins)');
      if (notees < 3) manque.push((3 - notees) + ' « Critique » notée(s) sur 30 de plus');
      if (!c.some(e => e.rubrique === 'choix' && !e.barre)) manque.push('un « Choix retenu »');
      return manque.length ? 'Carnet : ' + manque.join(', ') + '.' : null;
    }
    case 'calquesConstr2': case 'calquesConstr3': case 'calquesConstr4': {
      const n = +id.slice(-1), k = calquesConstr(doc).length;
      return k >= n ? null : 'Il faut ' + n + ' calques de construction dessinés (un par passe : vignettes, rough, volumes, esquisse) ; il y en a ' + k + '.';
    }
    case 'dessousBaisse': {
      const L = calquesConstr(doc); if (L.length < 2) return null;
      const dessous = L.slice(0, -1);
      return dessous.some(c => c.visible && c.opacite > 45) ? 'Baisse l\'opacité des passes précédentes (20 à 40 %) ou masque-les : « ' + dessous.filter(c => c.visible && c.opacite > 45).map(c => c.nom).join(' », « ') + ' ».' : null;
    }
    case 'taille64': {
      if (Math.max(doc.w, doc.h) >= 64 || m.justifs.taille64) return null;
      return 'Le dessin fait ' + doc.w + '×' + doc.h + ' : un design d\'objet se juge à 64 px de haut au moins (0-AC-C). Agrandis la toile et redessine, ou justifie.';
    }
    case 'critiqueDessin': {
      // la dernière critique qui porte une note sur 30 (une critique sans note, comme un écart écrit, ne compte pas)
      const re = /(\d+(?:[.,]\d+)?)\s*\/\s*30/;
      const c = (m.carnet || []).filter(e => e.rubrique === 'critique' && !e.barre && re.test(e.texte)), der = c[c.length - 1];
      const note = der && re.exec(der.texte);
      if (!note) return 'Écris au carnet la note du dessin (rubrique « Critique », sous la forme « 23/30 »).';
      const v = parseFloat(note[1].replace(',', '.'));
      return v >= 22 ? null : 'Le dessin est noté ' + v + '/30 : il faut 22 au moins. Reviens au rough ou à l\'esquisse.';
    }
    case 'carnetPieces': {
      const c = m.carnet || [], n = c.filter(e => e.rubrique === 'piece').length;
      return n >= 9 ? null : 'Carnet : ' + (9 - n) + ' « Pièce » de plus (3 bouchons, 3 jonctions, 3 pieds).';
    }
    case 'reference': return doc.calques.some(c => c.type === 'reference') ? null : 'Importe la pièce dans un calque de référence.';
    case 'tuileOn': return doc.tuile.on ? null : 'Active le mode tuile (onglet Tuiles).';
    case 'carteTerrain': return (doc.carte.terrain || []).filter(Boolean).length >= 12 ? null : 'Peins au moins 12 cases de terrain (onglet Tuiles, pinceau Terrain) : en U, en L et en îlot.';
    case 'carte': return (doc.carte.tuiles || []).filter(Boolean).length >= 12 ? null : 'Peins au moins 12 cases de carte dans l\'onglet Tuiles.';
    case 'analyse': return String(m.planche.analyse || '').trim().length >= 40 ? null : 'Écris l\'analyse (40 caractères au moins) dans l\'onglet Méthode.';
    case 'timing': {
      const manque = doc.images.map((im, i) => (!im.role || !im.change || !(im.ms > 0)) ? i + 1 : 0).filter(Boolean);
      if (doc.images.length < 2) return 'Une animation a au moins 2 images.';
      return manque.length ? 'Feuille de timing incomplète, image(s) ' + manque.join(', ') + ' : rôle, ce qui change et durée.' : null;
    }
    case 'imagesValidees': { const n = doc.images.map((im, i) => im.validee ? 0 : i + 1).filter(Boolean); return n.length ? 'Image(s) non validée(s) : ' + n.join(', ') + '.' : null; }
    case 'Ltoutes': {
      const bad = [];
      for (let i = 0; i < doc.images.length; i++) { const r = AP.detecte(doc, i).find(x => x.id === 'L'); if (r && !m.justifs.L) bad.push(i + 1); }
      return bad.length ? 'Des « L » restent sur les images ' + bad.join(', ') + '.' : null;
    }
    case 'planche': {
      const t = typeDe(doc), manque = [];
      QUESTIONS.forEach((q, i) => { if (!String(m.planche['q' + i] || '').trim()) manque.push('Q' + (i + 1)); });
      (QUESTIONS_TYPE[t] || []).forEach((q, i) => { if (!String(m.planche['t' + i] || '').trim()) manque.push('T' + (i + 1)); });
      for (const k of ['reussi', 'ameliorer']) if (!String(m.planche[k] || '').trim()) manque.push(k === 'reussi' ? '3 réussis' : '3 à améliorer');
      return manque.length ? 'Planche : réponds à ' + manque.join(', ') + '.' : null;
    }
    case 'defauts': {
      const r = det().filter(x => x.niveau !== 'conseil' && !m.justifs[x.id]);
      return r.length ? 'Défauts restants : ' + r.map(x => x.titre).join(', ') + '.' : null;
    }
  }
  return null;
}
const NOMS_PORTES = {
  fiche: 'Fiche remplie', regles: 'Règles lues', nonVide: 'Image non vide', construction: 'Construction en calque',
  silhouette1: 'Silhouette en 1-2 couleurs', reference: 'Calque de référence', tuileOn: 'Mode tuile', carte: 'Carte peinte', carteTerrain: 'Carte de test en terrain',
  analyse: 'Analyse écrite', timing: 'Feuille de timing', imagesValidees: 'Toutes les images validées', Ltoutes: 'Aucun L sur les images',
  planche: 'Planche remplie', defauts: 'Aucun défaut restant',
  carnetVision: 'Carnet : vision écrite et corrigée', carnetEssais: 'Carnet : essais et choix',
  carnetEssais21: 'Carnet : 6 silhouettes notées et un choix', carnetPieces: 'Carnet : 9 variantes de pièces', carnetIterations: 'Carnet : 3 itérations notées et un choix', carnetDetails8: 'Carnet : 8 détails travaillés', carnetPasses: 'Carnet : les six passes de rendu', carnetReferences: 'Carnet : 3 références documentées', zonesTuile: 'Passe à la loupe de la tuile centrale', zonesToutes: 'Passe à la loupe de tout le dessin', tampons: 'Aucun élément tamponné', carnetDetails16: 'Carnet : 16 détails travaillés', carnetDetails6: 'Carnet : 6 détails travaillés', carnetDetails12: 'Carnet : 12 détails travaillés',
  calquesConstr2: '2 calques d\'esquisse', calquesConstr3: '3 calques d\'esquisse', calquesConstr4: '4 calques d\'esquisse',
  dessousBaisse: 'Passes précédentes baissées', critiqueDessin: 'Dessin noté 22/30 au moins', taille64: 'Dessin à 64 px de haut au moins',
  lumierePosee: 'Lumière posée', volume: 'Le volume suit la lumière', lumiere: 'Ombrage du bon côté',
  L: 'Aucun « L »', jaggies: 'Pas de jaggies', orphelins: 'Pas d\'orphelin', bandes: 'Pas de banding', coussin: 'Pas d\'ombrage coussin',
  bruit: 'Pas de bruit', trame: 'Pas de trame décorative', superpixels: 'Pas de super pixels', budget: 'Budget de couleurs (A3)',
  noirPur: 'Pas de noir pur', rampesGris: 'Rampes lisibles en gris', raccords: 'Tuile sans couture', alpha: 'Pas de pixel semi-transparent'
};

/* État de chaque porte et case de l'étape courante. */
function etatEtape(at) {
  const doc = at.doc, e = etapeCourante(doc), cache = {}, m = doc.meta;
  const portes = e.portes.map(id => ({ id, nom: NOMS_PORTES[id] || id, manque: porte(id, at, cache) }));
  const coches = e.coches.map(c => ({ cle: e.id + '.' + c.cle, txt: c.txt, ok: !!m.coches[e.id + '.' + c.cle] }));
  return { etape: e, index: Math.min(m.etape, nbEtapes(doc) - 1), total: nbEtapes(doc), fini: m.etape >= nbEtapes(doc), portes, coches };
}
function verifieEtape(at) {
  const st = etatEtape(at), manque = [];
  for (const p of st.portes) if (p.manque) manque.push(p.manque);
  for (const c of st.coches) if (!c.ok) manque.push('Case non cochée : « ' + c.txt + ' »');
  return { ok: !manque.length, manque };
}

/* ---------- Les 92 règles, lues dans le texte de la méthode ---------- */
function extraitRegles(texte) {
  const lignes = texte.split('\n'), out = [];
  let i = lignes.findIndex(l => /^# Règles impératives/.test(l)), groupe = '';
  if (i < 0) return out;
  for (i++; i < lignes.length; i++) {
    const l = lignes[i];
    if (/^# /.test(l) || /^---/.test(l)) { if (out.length) break; else continue; }
    const g = l.match(/^\*\*([^*]+)\*\*\s*$/); if (g) { groupe = g[1]; continue; }
    const r = l.match(/^(\d+)\.\s+(.*)$/);
    if (r) { out.push({ n: +r[1], groupe, texte: r[2] }); continue; }
    if (out.length && /^\s+\S/.test(l)) out[out.length - 1].texte += ' ' + l.trim();
  }
  return out;
}

Object.assign(AP, {
  RUBRIQUES, FICHES, QUESTIONS, QUESTIONS_TYPE, TESTS_PRO, TABLE_A3, ETAPES, ETAPES_V16, ETAPES_V17, ETAPES_V21, ETAPES_V22, ETAPES_V24, ETAPES_V25, ETAPES_V26, ETAPES_V27, ETAPES_V28, METHODE_ACTUELLE, etapesDe, zonesAFaire, TYPES, NOMS_PORTES,
  colonneA3, ficheIncomplete, nbEtapes, etapeCourante, etatEtape, verifieEtape, extraitRegles, typeDe
});
if (typeof module !== 'undefined') module.exports = AP;
})(typeof window !== 'undefined' ? window : globalThis);
