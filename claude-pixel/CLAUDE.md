# Claude Pixel : règles de travail

Ces règles s'ajoutent à celles du `CLAUDE.md` à la racine du dépôt. Tout ce qui concerne ce
projet reste dans `claude-pixel/`.

## Dessiner

1. **Seulement à la souris.** Un dessin de Claude passe par `souris/souris.mjs`, geste par
   geste. Il ne faut jamais écrire des pixels avec un script, ni toucher à l'app par
   `page.evaluate`, ni modifier un `.claude-pixel.json` à la main. `window.claudePixel` sert
   uniquement à lire.
2. **Regarder après chaque trait.** Après chaque trait, faire `regarde` et lire les trois
   images (écran, loupe, dessin) et le résumé avant de continuer. La souris refuse le trait
   suivant tant que ce n'est pas fait. Il ne faut pas enchaîner des `regarde` à vide pour
   contourner cette règle.
3. **Suivre la méthode.** Relire les 87 règles impératives et la partie 0 (dessiner avant de
   pixelliser) avant chaque dessin. Remplir la fiche d'intention honnêtement, avec le niveau
   visé : une œuvre pro précise et ce qu'on en prend. Ne cocher une case que si c'est vrai
   sur le dessin, et jamais seulement pour ouvrir une porte.
4. **Penser avant de dessiner, et designer avant de rendre.** Aux étapes Vision et Essais,
   écrire au carnet une idée à la fois et barrer ce qui ne tient pas en écrivant pourquoi.
   Dessiner au moins 6 silhouettes dans 3 familles, assez grandes pour designer, et les noter
   sur 30 avec la grille 0-AA-E. Pour un objet, dessiner ensuite 3 variantes de chaque pièce
   (bouchon, jonction, pied). La forme doit être belle en noir avant toute lumière (0-AA) :
   le rendu ne sauve pas un dessin raté. Le carnet est honnête : il garde les vraies
   hésitations.
   Puis sketcher comme un illustrateur (0-AB) : rough, construction, esquisse nettoyée, trait,
   polish, chacun sur un nouveau calque, celui du dessous baissé à 20-40 %. Redessiner plutôt
   que gommer, retourner la toile souvent. À l'étape « Validation du dessin », s'arrêter et
   montrer le dessin à l'humain avant toute couleur.
   Le critère de cette validation : le trait seul doit ressembler à un sketch fini de pro
   (0-AC) : l'idée se lit en silhouette noire, trois poids de trait appliqués partout,
   recouvrements nets, lignes de forme. Un design d'objet se dessine à 64 px de haut au moins.
5. **Dessiner, pas seulement pixelliser.** Construire chaque volume entier dans un calque de
   construction (ellipses comprises). Poser la lumière dans l'onglet Lumière avant la
   première ombre, regarder le guide de volume, poser d'abord deux familles (vue Notan),
   puis le modelé et la matière. Lire à chaque regard la ligne `volume` (accord, familles,
   inversions, étendue) et les panneaux « valeurs » et « guide » de l'image du dessin. Le
   guide ne dessine rien : chaque pixel reste posé à la souris.
6. **Corriger tout de suite.** Un défaut signalé près du curseur se corrige avant le trait
   suivant. Si le détecteur se trompe, il faut l'écrire, avec la raison, dans la planche.
7. **Planche honnête.** Les réponses de la dernière étape (la planche) décrivent ce qui est réellement réussi et
   ce qui reste à améliorer, y compris ce qui n'a pas été vérifié. Comparer côte à côte avec
   l'œuvre visée et écrire l'écart.
8. **Une séance par dessin.** Utiliser `--id <nom-du-dessin>`. La séance se termine par
   `fin`, qui enregistre la vidéo. On ne réécrit pas l'historique d'une séance : un raté
   reste dans la vidéo, et on le corrige à la souris.

## Préparer une séance

- Les répétitions se font avec un autre `--id`, et leurs dossiers ne sont pas commités.
- Tester les fichiers de gestes par petits morceaux (`souris - < fichier`). La commande
  s'arrête au premier refus, et le message dit pourquoi.
- Si la vue est trop étroite, un élément peut être hors de l'écran : faire `defile =nom`
  avant de cliquer.

## Modifier l'app

- Modifier `app/src/`, puis lancer `node app/build.mjs`. Ne jamais modifier
  `app/index.html` à la main.
- Après une modification, lancer `node --test tests/*.test.cjs`. Une nouvelle fonction du
  cœur, un nouveau détecteur ou un nouvel export vient avec son test.
- Tout élément cliquable reçoit un `data-cible` stable : c'est l'adresse de la souris.
- L'identité ne change pas :
  - Le nom est « Claude Pixel », la devise « Un pixel à la fois. ».
  - La marque est un « C » de 6×6 pixels, dont un pixel ambre (`#f2b84b`).
  - Le projet est personnel et non officiel. Ni logo ni couleurs d'Anthropic.
- Après une modification de `serveur.mjs`, relancer le serveur : `pkill -f
  souris/serveur.mjs`, attendre 3 s, puis `demarre`.

## Sources

La méthode cite des livres et des sites. N'utiliser que des sources légitimes. Pas de copies
piratées (archive.org, studylib, dokumen.pub, ebin.pub, pdfcoffee, anyflip, studypool).
