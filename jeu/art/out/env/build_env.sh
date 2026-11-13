#!/bin/bash
# build_env.sh <nom> [L] : trace art/src/env/<nom>.txt -> grilles -> png x1 + @8 -> copie dans game/assets/env.
# Avec L : dérive aussi <nom sans _L>_R (vers_droite.py) et écrit sa grille comme source art/src/env/<..>_R.txt.
set -e
cd /home/user/Testing/jeu/art/out/env
n=$1
python3 trace_env.py ../../src/env/$n.txt grilles/$n.txt >/dev/null
python3 /home/user/Testing/jeu/tools/px.py grilles/$n.txt $n.png >/dev/null
cp $n.png ../../../game/assets/env/
if [ "$2" = "L" ]; then
  r=${n%_L}_R
  python3 vers_droite.py grilles/$n.txt grilles/$r.txt "ÉCHO - $r : mur DROIT, dérivé de $n par la règle de art/out/env/vers_droite.py (pas de miroir).|x0 contour de collision k ; x1 chanfrein ÉCLAIRÉ (la face regarde la lumière haut-gauche) ; x2-14 = blocs du mur gauche décalés de 2 px ;|x15 joint vers la colonne extérieure. Intention, budget et défauts : voir $n.txt (mêmes rôles de tuiles)." >/dev/null
  cp grilles/$r.txt ../../src/env/$r.txt
  python3 /home/user/Testing/jeu/tools/px.py grilles/$r.txt $r.png >/dev/null
  cp $r.png ../../../game/assets/env/
fi
echo "ok $n"
