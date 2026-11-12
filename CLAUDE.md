# Règles du dépôt

Ce dépôt est un dépôt de **test** qui regroupe plusieurs mini-projets indépendants.

## Règle n°1 : un dossier par projet

- Chaque mini-projet vit **dans son propre dossier** à la racine du dépôt (ex. `mon-projet/`).
- Aucun fichier d'un projet ne doit être placé à la racine ni dans le dossier d'un autre projet.
- Les projets ne partagent ni code, ni dépendances, ni configuration : chacun est autonome
  (son propre `package.json`, `requirements.txt`, README, etc. si nécessaire).
- Avant de créer ou modifier quoi que ce soit, identifier le dossier du projet concerné.
  S'il s'agit d'un nouveau projet, créer un nouveau dossier dédié.

Seuls les fichiers qui concernent le dépôt entier (ce `CLAUDE.md`, le `README.md`,
un éventuel `.gitignore` global) restent à la racine.
