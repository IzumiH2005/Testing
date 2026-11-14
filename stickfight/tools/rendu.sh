#!/usr/bin/env bash
# Lance tools/rendu.gd avec Godot (variable GODOT = chemin du binaire Godot 4.3).
# Sans écran, passe par xvfb-run. Les options sont décrites dans tools/rendu.gd.
set -euo pipefail
here="$(cd "$(dirname "$0")/.." && pwd)"
godot="${GODOT:-godot}"
args=(--path "$here" --audio-driver Dummy --rendering-driver opengl3 -s res://tools/rendu.gd -- "$@")
if [ -z "${DISPLAY:-}" ] && command -v xvfb-run >/dev/null; then
  exec xvfb-run -a "$godot" "${args[@]}"
else
  exec "$godot" "${args[@]}"
fi
