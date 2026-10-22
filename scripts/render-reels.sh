#!/bin/bash
# Render every client reel spec, add its music track, and export the Instagram delivery file.
#   scripts/render-reels.sh [slug ...]      (no args = every spec in video/specs)
# Expects video/specs/<slug>.json with optional "music": "<path to audio>" and "music_start": <sec>.
set -euo pipefail
cd "$(dirname "$0")/.."
node scripts/build-reel-specs.mjs >/dev/null
SLUGS=("$@"); [ ${#SLUGS[@]} -eq 0 ] && SLUGS=($(ls video/specs/*.json | xargs -n1 basename | sed 's/\.json$//'))
mkdir -p video/out/clients
for s in "${SLUGS[@]}"; do
  spec="video/specs/$s.json"
  (cd video && npx remotion render "Reel-$s" "out/clients/$s.mp4" 2>&1 | grep -v "^    at \|\[chrome\]" | tail -1)
  music=$(python3 -c "import json;print(json.load(open('$spec')).get('music',''))")
  start=$(python3 -c "import json;print(json.load(open('$spec')).get('music_start',0))")
  if [ -n "$music" ] && [ -f "$music" ]; then
    scripts/add-music.sh "video/out/clients/$s.mp4" "$music" "video/out/clients/$s-music.mp4" --start "$start" | cut -c1-100
    scripts/ig-export.sh "video/out/clients/$s-music.mp4" "video/out/clients/$s-IG.mp4"
  else
    scripts/ig-export.sh "video/out/clients/$s.mp4" "video/out/clients/$s-IG.mp4"
  fi
done
