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
3. **Suivre la méthode.** Relire les 48 règles impératives avant chaque dessin. Remplir la
   fiche d'intention honnêtement. Ne cocher une case que si c'est vrai sur le dessin, et
   jamais seulement pour ouvrir une porte.
4. **Corriger tout de suite.** Un défaut signalé près du curseur se corrige avant le trait
   suivant. Si le détecteur se trompe, il faut l'écrire, avec la raison, dans la planche.
5. **Planche honnête.** Les réponses de l'étape 11 décrivent ce qui est réellement réussi et
   ce qui reste à améliorer, y compris ce qui n'a pas été vérifié.
6. **Une séance par dessin.** Utiliser `--id <nom-du-dessin>`. La séance se termine par
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
