# Studio Voix

Site fonctionnel en un seul fichier (`index.html`) qui transforme un texte en audio avec les voix de synthèse intégrées au navigateur (Web Speech API).

- **Créer** : texte (5 000 caractères max), exemples, choix de la voix, réglages (vitesse, hauteur, volume, pauses), lecture phrase par phrase.
- **Voix** : liste des voix de l'appareil, recherche, filtre par langue, aperçu séparé de la sélection.
- **Bibliothèque** : audios enregistrés dans le navigateur (localStorage), favoris, suppression avec annulation.

UI construite avec le skill Material Design, couleurs en 60/30/10 :
60 % blanc laiteux (surfaces), 30 % bleu pétrole (secondary-container), 10 % framboise (primary, actions principales).

Limite : l'audio est lu en direct par l'appareil, il n'y a pas de fichier MP3 à télécharger (il faudrait un modèle de voix côté serveur).

Ouvrir `index.html` dans Chrome, Edge ou Safari récent.
