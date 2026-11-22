# Claude Pixel

*Un pixel à la fois.*

Claude Pixel est un éditeur de pixel art complet et responsive, publié en artifact. Il est
conçu pour apprendre le pixel art à Claude. Claude y dessine comme un humain, à la souris,
geste par geste, et regarde son travail après chaque trait. La méthode
`METHODE_PIXEL_ART.md` est intégrée. Elle découpe chaque dessin en étapes et empêche Claude
de passer à la suivante tant que l'étape en cours ne tient pas.

Projet personnel, non officiel, sans lien avec Anthropic.

## Ce qu'il y a dedans

- **Éditeur** :
  - Outils : crayon pixel-perfect, gomme, ligne, rectangle, ellipse, dégradé, pot, remplacer
    une couleur, pipette, sélections, baguette, déplacement.
  - Calques, dont un calque de construction qui n'est jamais exporté.
  - Animation : images, durées, étiquettes, pelure d'oignon, cels liés.
  - Tuiles, palettes et aperçus ×1 et ×2.
  - Exports : PNG, GIF, planche, palettes `.hex` et `.gpl`.
  - Fonctionne sur téléphone, tablette et ordinateur, en thème clair ou sombre.
- **Méthode** : elle commence par la partie 0, *dessiner avant de pixelliser* (construction,
  lumière et forme, valeurs, formes, couleur, matières, neuf planches pro analysées). Puis
  fiche d'intention, parcours par type de dessin (objet, personnage, créature, animation,
  décor, étude), portes d'étape, cases à cocher et planche de contrôle finale.
- **Vision et essais** : avant le premier trait, un carnet de conception. Claude y écrit une
  idée à la fois (ce qu'il voit, la structure, les formes de base, l'idée unique, ce qui la
  rend crédible), barre ce qui ne tient pas en disant pourquoi, essaie au moins trois
  silhouettes, puis écrit son choix.
- **Lumière** : un onglet pour poser la source (direction, hauteur) et afficher sur la toile
  un guide de volume (lumière, demi-ton, terminateur, ombre propre, rebond, ombre portée),
  avec le repère de lumière des planches. Vues Couleur, Valeurs et Notan. L'app mesure si
  l'ombrage suit la lumière (accord, deux familles, inversions, étendue) ; une porte bloque
  tant que le volume ne tourne pas. Le guide ne dessine rien.
- **Détecteurs** : « L », pixels orphelins, jaggies, ombrage en coussin, ombrage qui ne suit
  pas la lumière, pixels doublés, banding, etc. Ils sont signalés sur le dessin et dans la loupe.
- **Journal** : chaque action est enregistrée. Une séance se rejoue image par image, et
  l'atelier en tire un timelapse WebM.
- **Deux modes** :
  - *Humain* (par défaut) : les portes conseillent.
  - *Claude* (adresse terminée par `#claude`) : les portes bloquent. Les gestes arrivent
    par la souris virtuelle, et `window.claudePixel` expose l'état en lecture seule.

## Arborescence

```
claude-pixel/
├── README.md               ce fichier
├── SPEC.md                 la spécification validée
├── CLAUDE.md               règles de travail de Claude dans l'atelier
├── METHODE_PIXEL_ART.md    la méthode (v19), embarquée dans l'app (onglet Aide, règles, portes)
├── app/
│   ├── src/                modules JS, style.css, template.html
│   ├── build.mjs           assemble tout en un seul fichier
│   └── index.html          l'application entière, publiable telle quelle en artifact
├── souris/                 la souris virtuelle de Claude (voir souris/README.md)
├── seances/                les séances filmées : commandes, regards, fichiers, vidéo
└── tests/                  tests Node du cœur, des détecteurs, de la méthode et des exports
```

## Commandes

```sh
node app/build.mjs                       # reconstruit app/index.html après une modification de src/
node --test tests/*.test.cjs             # les tests (Node 20 ou plus, aucune dépendance)
node souris/souris.mjs demarre --id nom  # une séance filmée (Playwright et Chromium requis)
```

L'app n'a aucune dépendance. Seule la souris a besoin de Playwright.

## Séances

| Séance | Dessin | Résultat |
|---|---|---|
| `seances/potion/` | Potion de soin, objet 16×16, 8 couleurs | 11 étapes validées par les portes, aucun défaut détecté, environ 280 commandes, vidéo de 3 min 56 |
| `seances/potion-64/` | Potion de vie, objet 64×64, 16 couleurs | 11 étapes validées par les portes, environ 620 commandes, 86 regards, vidéo de 20 min (67 Mo). Un défaut reste signalé : 16 coins en L, de faux positifs justifiés dans la planche (le détecteur ne regarde pas l'épaisseur du trait) |

## Publication

L'artifact est publié à partir de `app/index.html`, sans doctype : le squelette est ajouté
à la publication. Il utilise la capacité `downloads` pour les exports.
