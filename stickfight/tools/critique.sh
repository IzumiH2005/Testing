#!/usr/bin/env bash
# Prépare le dossier d'images que lit le critique (voir .claude/agents/critique-animation.md).
#   tools/critique.sh anims/x.json DOSSIER [--de a --a b] [--vue x,y,w,h]
# Produit dans DOSSIER :
#   cles_vues.png     chaque clé en trois vues (face, trois quarts, profil), sans effets
#   profil.png        tout le passage choisi, de profil, une image sur 4
#   profil_fin.png    le passage choisi, de profil, une image sur 2 (seulement avec --de/--a)
#   zoom.png          le passage choisi, cadré sur --vue (si donné), échelle 3
#   verifier.txt      sortie de --verifier
set -euo pipefail
here="$(cd "$(dirname "$0")/.." && pwd)"
anim="$1"; out="$2"; shift 2
de="" a="" vue=""
while [ $# -gt 0 ]; do
  case "$1" in
    --de) de="$2"; shift 2 ;;
    --a) a="$2"; shift 2 ;;
    --vue) vue="$2"; shift 2 ;;
    *) echo "option inconnue $1" >&2; exit 1 ;;
  esac
done
mkdir -p "$out"
A="$here/tools/anim.sh"
plage=()
[ -n "$de" ] && plage+=(--de "$de")
[ -n "$a" ] && plage+=(--a "$a")
"$A" "$anim" --verifier > "$out/verifier.txt" 2>&1 || true
"$A" "$anim" --cles --vues --scale 1 -o "$out/cles_vues.png" >/dev/null 2>&1
"$A" "$anim" "${plage[@]}" --pas 4 --cols 12 --scale 1 -o "$out/profil.png" >/dev/null 2>&1
if [ -n "$de" ]; then
  "$A" "$anim" "${plage[@]}" --pas 2 --cols 12 --scale 1 -o "$out/profil_fin.png" >/dev/null 2>&1
fi
if [ -n "$vue" ]; then
  "$A" "$anim" "${plage[@]}" --pas 2 --cols 8 --vue "$vue" --scale 3 -o "$out/zoom.png" >/dev/null 2>&1
fi
ls -1 "$out"
