# APK de numérisation

Application mobile de numérisation de documents (cible : Samsung A56) qui doit produire
un rendu « scanner de bureau » à partir d'une simple photo.

> Règle : tout le travail de ce projet se fait **exclusivement** dans ce dossier.

## État : prototype web (`web/`)

Une page web unique qui tourne entièrement dans le navigateur du téléphone (aucun envoi de données) :

1. **Photo** : appareil photo du téléphone ou import depuis la galerie (plusieurs pages possibles).
2. **Bords** : réseau DocAligner (IA) pour trouver les 4 coins. Si l'IA est coupée ou échoue, une
   détection classique prend le relais (score « papier », Otsu, enveloppe convexe). Les coins restent
   ajustables au doigt, avec une loupe.
3. **Redressement** : homographie et vraies proportions (méthode Zhang & He), aimantées A4 / Lettre.
4. **Orientation (IA)** : un classifieur remet automatiquement la page à l'endroit (0/90/180/270°).
5. **Page courbée (IA, bouton)** : UVDoc « déplie » les pages de livre ou froissées.
6. **Gomme (IA, bouton)** : les doigts sont repérés automatiquement (couleur de peau touchant le bord),
   on peut compléter au pinceau, puis MI-GAN reconstruit le papier à la place.
7. **Nettoyage** : « Magique » choisit seul. Page de texte : fond papier estimé puis divisé (fond blanc).
   Couverture ou page illustrée : l'éclairage est modélisé par une surface douce ajustée sur le seul papier,
   puis retiré (ombres et teinte de la lampe), sans délaver les couleurs. Les bouts de table ou de tissu
   visibles sur les bords sont repeints en papier. Rendus : Magique, Couleurs fidèles,
   Couleur douce, Niveaux de gris, Noir et blanc, Sans retouche.
8. **Texte (OCR)** : Tesseract.js 5 (réseau LSTM, français), fichiers servis depuis `web/ocr/`.
9. **PDF** : jsPDF, une page par scan, avec calque de texte invisible si l'OCR a été lancé (PDF cherchable).

Un bouton **IA** dans l'en-tête active ou coupe tous les modèles (choix mémorisé).

### Modèles IA (`web/ai/`, exécutés par onnxruntime-web en WebAssembly)

| Rôle | Modèle | Taille | Licence |
|---|---|---|---|
| Moteur | onnxruntime-web 1.22 | 11 Mo | MIT |
| Repérage des coins | DocAligner (heatmap, 256 px) | 4,8 Mo | Apache-2.0 |
| Orientation | PP-LCNet doc_ori (PaddleOCR) | 6,8 Mo | Apache-2.0 |
| Remise à plat | UVDoc | 31,7 Mo (3 morceaux) | Apache-2.0 |
| Gomme | MI-GAN (pipeline v2) | 28,1 Mo (2 morceaux) | MIT |

Chaque modèle n'est téléchargé qu'à sa première utilisation, puis reste en cache du navigateur.
Les gros fichiers sont découpés (< 15 Mo) et réassemblés en JavaScript. Ils portent l'extension
`.wasm` uniquement pour être servis comme fichiers binaires.

Temps mesurés (navigateur de bureau, 1 cœur) : coins 0,75 s, orientation 0,45 s,
remise à plat 2,2 s, gomme 2,9 s. Sur téléphone, compter 2 à 3 fois plus.

### Lancer en local

```bash
cd web && python3 -m http.server 8000
# puis ouvrir http://localhost:8000
```

### Limites de cette version

- La gomme reconstruit le papier : si un doigt cache du texte, ce texte ne peut pas être deviné.
- Pas encore testé sur le vrai téléphone (seulement dans Chromium).

## Prochaines étapes

- Tests sur le Samsung A56 et réglage des tailles d'entrée selon la vitesse.
- Emballer le tout en APK Android (CameraX + ONNX Runtime, même modèles).

## Licences des composants tiers

- onnxruntime-web : MIT (Microsoft) — voir `web/ai/onnxruntime.LICENSE.txt`
- DocAligner (DocsaidLab) : Apache-2.0 — voir `web/ai/docaligner.NOTICE.txt`
- PP-LCNet doc_ori (PaddleOCR / PaddlePaddle) : Apache-2.0
- UVDoc (Verhoeven et al.) : Apache-2.0
- MI-GAN (Picsart AI Research) : MIT — voir `web/ai/migan.LICENSE.txt`
- Tesseract.js et tesseract.js-core : Apache-2.0
- Données de langue `fra` (tessdata_best int) : Apache-2.0
- jsPDF : MIT (chargé depuis un CDN)
