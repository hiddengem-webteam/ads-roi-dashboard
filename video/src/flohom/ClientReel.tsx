import React from "react";
import { AbsoluteFill, OffthreadVideo, interpolate, staticFile, useCurrentFrame } from "remotion";
import { Sequence } from "remotion";
import { loadFont } from "@remotion/google-fonts/Poppins";

const { fontFamily } = loadFont("normal", { weights: ["600", "700"], subsets: ["latin"] });

// Spec-driven reel: the approved FLOHOM v2/v3 style (six-ish shots, ~3 s each, hard cuts,
// static captions on from frame one) parametrised per client from video/specs/<slug>.json.
export type Beat = {
  file: string; // video/public/<slug>/<file>.mp4
  seconds: number;
  trimBefore?: number; // frames
  playbackRate?: number;
  lines: string[];
  sub?: string;
  size?: number;
  zoom?: number;
};
export type ReelSpec = { slug: string; client: string; dir?: string; fps?: number; beats: Beat[]; music?: string; music_start?: number }; // dir: clip folder under video/public (defaults to slug)

export const specFrames = (spec: ReelSpec) =>
  spec.beats.reduce((n, b) => n + Math.round(b.seconds * (spec.fps ?? 30)), 0);

const Caption: React.FC<{ beat: Beat }> = ({ beat }) => {
  const size = beat.size ?? 58;
  return (
    <AbsoluteFill style={{ justifyContent: "flex-start", alignItems: "center", paddingTop: 560 }}>
      <div
        style={{
          textAlign: "center",
          fontFamily,
          color: "white",
          textShadow: "0 2px 6px rgba(0,0,0,0.55), 0 6px 24px rgba(0,0,0,0.45)",
          paddingLeft: 70,
          paddingRight: 70,
        }}
      >
        {beat.lines.map((line) => (
          <div key={line} style={{ fontSize: size, fontWeight: 700, lineHeight: 1.18 }}>
            {line}
          </div>
        ))}
        {beat.sub ? (
          <div style={{ fontSize: 40, fontWeight: 600, marginTop: 10, letterSpacing: 0.5 }}>{beat.sub}</div>
        ) : null}
      </div>
    </AbsoluteFill>
  );
};

const Shot: React.FC<{ beat: Beat; slug: string; frames: number }> = ({ beat, slug, frames }) => {
  const frame = useCurrentFrame();
  const scale = interpolate(frame, [0, frames], [1, beat.zoom ?? 1.06], { extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ backgroundColor: "#06111f" }}>
      <OffthreadVideo
        src={staticFile(`${slug}/${beat.file}.mp4`)}
        trimBefore={beat.trimBefore}
        playbackRate={beat.playbackRate}
        muted
        style={{ width: "100%", height: "100%", objectFit: "cover", transform: `scale(${scale})` }}
      />
      <Caption beat={beat} />
    </AbsoluteFill>
  );
};

export const ClientReel: React.FC<ReelSpec> = (spec) => {
  const fps = spec.fps ?? 30;
  let at = 0;
  return (
    <AbsoluteFill style={{ backgroundColor: "#06111f" }}>
      {spec.beats.map((b, i) => {
        const frames = Math.round(b.seconds * fps);
        const from = at;
        at += frames;
        return (
          <Sequence key={i} from={from} durationInFrames={frames}>
            <Shot beat={b} slug={spec.dir ?? spec.slug} frames={frames} />
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};
