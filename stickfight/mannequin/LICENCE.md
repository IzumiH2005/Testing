# Mannequin 3D de référence

`humain.json` est tiré de MakeHuman / MPFB2 (maillage `base.obj`, rig `standard`
« game_engine » et ses poids), publiés sous licence **CC0 1.0** (domaine public) :
https://github.com/makehumancommunity/mpfb2 (fichier `LICENSE.ASSETS.md`).
Conversion : `tools/mannequin_convertir.py` (corps seul, mètres, poids ≥ 0,002).

Usage : `tools/mannequin.sh poses/x.json -o vues.png` pose le mannequin comme le
stickman (StickRig.solve) et le rend en trois vues, stickman superposé.
