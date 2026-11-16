# Clé de signature d'écho-mounbole

`echo-mounbole.keystore` signe l'app Android `com.echotour.mounbole`. Toutes les versions
suivantes doivent être signées avec cette même clé, sinon Android refuse la mise à jour.
La clé et `identifiants.txt` (alias, mot de passe) ne sont pas dans le dépôt : le propriétaire
les garde à part et les recopie dans ce dossier avant un export.

Export :

    export GODOT_ANDROID_KEYSTORE_RELEASE_PATH=$PWD/jeu/signature/echo-mounbole.keystore
    export GODOT_ANDROID_KEYSTORE_RELEASE_USER=mounbole
    export GODOT_ANDROID_KEYSTORE_RELEASE_PASSWORD=<mot_de_passe>
    godot --headless --path jeu/game --export-release Android ../build/echo-mounbole.apk

Augmenter `version/code` dans `export_presets.cfg` à chaque nouvelle version.
L'ancienne app (`echo.apk`, `com.echotour.game`) est une app séparée : les deux coexistent.
