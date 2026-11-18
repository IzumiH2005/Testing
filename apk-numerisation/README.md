# APK de numérisation

Application mobile de numérisation de documents (cible : Samsung A56) qui doit produire
un rendu « scanner de bureau » à partir d'une simple photo.

> Règle : tout le travail de ce projet se fait **exclusivement** dans ce dossier.

## État : prototype web (`web/`)

Une page web unique qui tourne entièrement dans le navigateur du téléphone (aucun envoi de données) :

1. **Photo** : appareil photo du téléphone ou import depuis la galerie (plusieurs pages possibles).
2. **Bords** : détection automatique de la feuille (score « papier » clair et peu coloré, seuil d'Otsu,
   plus grande zone, enveloppe convexe, quadrilatère d'aire maximale). Les coins restent ajustables au doigt, avec une loupe.
3. **Redressement** : homographie et rééchantillonnage bilinéaire. Les vraies proportions sont estimées
   à partir de la perspective (méthode Zhang & He) puis aimantées au format A4 / Lettre.
4. **Nettoyage** : estimation du fond papier sur une grille, division (retire ombres et teinte),
   niveaux, gamma et netteté. Rendus : Magique, Couleur douce, Niveaux de gris, Noir et blanc, Sans retouche.
5. **Texte (OCR)** : Tesseract.js 5 (réseau LSTM, français), fichiers servis depuis `web/ocr/`.
6. **PDF** : jsPDF, une page par scan, avec calque de texte invisible quand l'OCR a été lancé (PDF cherchable).

### Lancer en local

```bash
cd web && python3 -m http.server 8000
# puis ouvrir http://localhost:8000
```

### Limites de cette version

- Détection, redressement et nettoyage sont des algorithmes classiques (pas encore de réseau de neurones).
- Pas de correction des pages courbées (livres) ni d'effacement des doigts.

## Prochaines étapes

- Remplacer la détection par un petit réseau de segmentation (type DocAligner / U-Net léger).
- Ajouter le dépliage des pages courbées (type DocTr / UVDoc) et le retrait des doigts.
- Emballer le tout en APK Android (CameraX + ONNX Runtime / TFLite).

## Licences des composants tiers

- Tesseract.js et tesseract.js-core : Apache-2.0
- Données de langue `fra` (tessdata_best int) : Apache-2.0
- jsPDF : MIT (chargé depuis un CDN)
