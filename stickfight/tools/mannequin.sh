#!/usr/bin/env bash
# Mannequin 3D de référence posé comme le stickman, en trois vues (face, trois quarts,
# profil), stickman superposé. Variable GODOT = binaire Godot 4.3. Python : numpy,
# scipy, matplotlib.
#   tools/mannequin.sh poses/garde_ouverte_bagarreur.json -o /tmp/garde.png [--sans-stick]
#     [--set armN=40,armN_p+=10]   (angles modifiés pour essayer, sans toucher à la pose)
set -euo pipefail
here="$(cd "$(dirname "$0")/.." && pwd)"
pose="$1"; shift
sets=()
rest=()
while [ $# -gt 0 ]; do
  if [ "$1" = "--set" ]; then sets=(--set "$2"); shift 2; else rest+=("$1"); shift; fi
done
tmp="$(mktemp --suffix=.json)"
trap 'rm -f "$tmp"' EXIT
case "$pose" in /*) ;; *) pose="$(pwd)/$pose" ;; esac
"${GODOT:-godot}" --headless --path "$here" -s res://tools/pose3d.gd -- "$pose" "${sets[@]}" -o "$tmp" >/dev/null
python3 "$here/tools/mannequin.py" "$tmp" "${rest[@]}"
