#!/usr/bin/env bash
# Place les mains en 3D pour les clés qui portent "mains3d" (voir tools/resout_mains.gd).
# Réécrit le fichier d'animation donné. Variable GODOT = chemin du binaire Godot 4.3.
set -euo pipefail
here="$(cd "$(dirname "$0")/.." && pwd)"
f="$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
godot="${GODOT:-godot}"
args=(--path "$here" --headless -s res://tools/resout_mains.gd -- "$f")
if command -v xvfb-run >/dev/null; then xvfb-run -a "$godot" "${args[@]}"; else "$godot" "${args[@]}"; fi
