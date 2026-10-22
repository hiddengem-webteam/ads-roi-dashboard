#!/bin/bash
# Mux a music track into a silent reel master without re-rendering.
#   scripts/add-music.sh <video.mp4> <audio file> <out.mp4> [--start SEC] [--fade-in SEC] [--fade-out SEC] [--lufs -14]
# The track is started at --start (default 0), looped with a 1 s crossfade if it is
# shorter than the video, trimmed to the video length, faded in/out, loudness-normalised
# (EBU R128, default -14 LUFS for Instagram/Facebook) and encoded AAC 192k. Video stream is copied.
set -euo pipefail
VIDEO=$1; AUDIO=$2; OUT=$3; shift 3
START=0; FIN=0.5; FOUT=2.0; LUFS=-14
while [ $# -gt 0 ]; do case $1 in --start) START=$2; shift 2;; --fade-in) FIN=$2; shift 2;; --fade-out) FOUT=$2; shift 2;; --lufs) LUFS=$2; shift 2;; *) echo "unknown option $1" >&2; exit 2;; esac; done
VLEN=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$VIDEO")
ALEN=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$AUDIO")
AVAIL=$(python3 -c "print(max(0.0, $ALEN - $START))")
LOOPS=$(python3 -c "import math; print(max(1, math.ceil($VLEN / max(0.5, $AVAIL - 1))))")
FOUT_AT=$(python3 -c "print(max(0.0, $VLEN - $FOUT))")
# one -i per loop copy so acrossfade reads independent streams (asplit copies run in lockstep and starve it)
INPUTS=(); F=""
for i in $(seq 0 $((LOOPS-1))); do INPUTS+=(-i "$AUDIO"); F="$F[$i:a]atrim=start=$START,asetpts=PTS-STARTPTS[s$i];"; done
PREV="[s0]"
if [ "$LOOPS" -gt 1 ]; then for i in $(seq 1 $((LOOPS-1))); do F="$F$PREV[s$i]acrossfade=d=1:c1=tri:c2=tri[x$i];"; PREV="[x$i]"; done; fi  # BSD seq counts down for "seq 1 0"
F="$F${PREV}atrim=0:$VLEN,asetpts=PTS-STARTPTS,afade=t=in:st=0:d=$FIN,afade=t=out:st=$FOUT_AT:d=$FOUT,loudnorm=I=$LUFS:TP=-1.5:LRA=11[out]"
ffmpeg -v error -y "${INPUTS[@]}" -i "$VIDEO" -filter_complex "$F" -map "$LOOPS:v" -map "[out]" -c:v copy -c:a aac -b:a 192k -ar 48000 -movflags +faststart "$OUT"
OLEN=$(ffprobe -v error -select_streams a -show_entries stream=duration -of csv=p=0 "$OUT")
echo "$OUT  video ${VLEN}s  audio out ${OLEN}s  track ${ALEN}s from ${START}s  loops $LOOPS  fade in ${FIN}s out ${FOUT}s  $LUFS LUFS"
