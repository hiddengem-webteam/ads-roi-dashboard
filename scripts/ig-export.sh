#!/bin/bash
# Instagram / Ads Manager delivery pass, per the Content Drive docs "Uploading Highest Quality
# to IG" and the AI Content Creation SOP: 1080x1920, 30 fps, H.264 High, 15 Mbps constant
# bitrate, a subtle unsharp mask and 3-5% monochrome grain so IG's compression does not band
# smooth skies. Audio is copied if present.
#   scripts/ig-export.sh <in.mp4> <out.mp4> [--bitrate 15M] [--sharpen 0.3] [--grain 5] [--hevc]
set -euo pipefail
IN=$1; OUT=$2; shift 2
BR=15M; SHARP=0.3; GRAIN=5; CODEC=libx264; EXTRA="-profile:v high"
while [ $# -gt 0 ]; do case $1 in --bitrate) BR=$2; shift 2;; --sharpen) SHARP=$2; shift 2;; --grain) GRAIN=$2; shift 2;; --hevc) CODEC=libx265; EXTRA="-tag:v hvc1"; shift;; *) echo "unknown option $1" >&2; exit 2;; esac; done
HAS_AUDIO=$(ffprobe -v error -select_streams a -show_entries stream=codec_name -of csv=p=0 "$IN" | head -1)
AUDIO="-an"; [ -n "$HAS_AUDIO" ] && AUDIO="-c:a copy"
ffmpeg -v error -y -i "$IN" \
  -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,unsharp=5:5:${SHARP}:5:5:0,noise=c0s=${GRAIN}:c0f=t+u,format=yuv420p" \
  -c:v $CODEC $EXTRA -b:v $BR -minrate $BR -maxrate $BR -bufsize 30M -x264-params "nal-hrd=cbr" -g 60 -r 30 \
  $AUDIO -movflags +faststart "$OUT" 2>&1 | grep -v "x264-params" || true
# ffprobe prints format fields in its own order: duration, size, bit_rate
ffprobe -v error -show_entries format=duration,size,bit_rate -of csv=p=0 "$OUT" | awk -F, -v f="$OUT" '{printf "%s  %.1fs  %.1f MB  %.1f Mbps\n", f, $1, $2/1e6, $3/1e6}'
