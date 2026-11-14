#!/usr/bin/env bash
# Lance tools/anim.gd avec Godot (variable GODOT = chemin du binaire Godot 4.3).
# Sans écran, passe par xvfb-run. Les options sont décrites dans tools/anim.gd.
# En plus : --gif f.gif et --video f.mp4 (avec ffmpeg) ; --lent n ralentit n fois.
#   GIF : 50 i/s (les navigateurs ne savent pas afficher 60 i/s en GIF).
#   MP4 : 60 i/s exactes.
set -euo pipefail
here="$(cd "$(dirname "$0")/.." && pwd)"
godot="${GODOT:-godot}"
gif="" video="" lent=1
pass=()
while [ $# -gt 0 ]; do
  case "$1" in
    --gif) gif="$2"; shift 2 ;;
    --video) video="$2"; shift 2 ;;
    --lent) lent="$2"; shift 2 ;;
    *) pass+=("$1"); shift ;;
  esac
done
tmp=""
if [ -n "$gif$video" ]; then
  tmp="$(mktemp -d)"
  trap 'rm -rf "$tmp"' EXIT
  pass+=(--images "$tmp")
fi
args=(--path "$here" --audio-driver Dummy --rendering-driver opengl3 -s res://tools/anim.gd -- "${pass[@]}")
if [ -z "${DISPLAY:-}" ] && command -v xvfb-run >/dev/null; then
  xvfb-run -a "$godot" "${args[@]}"
else
  "$godot" "${args[@]}"
fi
rate=$(( 60 / lent ))
[ "$rate" -lt 1 ] && rate=1
if [ -n "$video" ]; then
  ffmpeg -loglevel error -y -framerate "$rate" -i "$tmp/frame_%04d.png" -c:v libx264 -pix_fmt yuv420p -r 60 "$video"
  echo "Vidéo : $video"
fi
if [ -n "$gif" ]; then
  ffmpeg -loglevel error -y -framerate "$rate" -i "$tmp/frame_%04d.png" \
    -vf "fps=50,split[a][b];[a]palettegen=max_colors=64:stats_mode=full[p];[b][p]paletteuse=dither=none" "$gif"
  echo "GIF : $gif"
fi
