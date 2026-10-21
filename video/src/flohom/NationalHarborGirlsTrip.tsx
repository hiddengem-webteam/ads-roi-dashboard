import React from "react";
import {
  AbsoluteFill,
  OffthreadVideo,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { loadFont } from "@remotion/google-fonts/Poppins";

const { fontFamily } = loadFont("normal", {
  weights: ["600", "700"],
  subsets: ["latin"],
});

// Reels for the Potomac (National Harbor) boats, built on the structure of the
// Myrtle Beach reel that won the 19 Oct creative review: occasion hook, rooftop
// at dusk, chef or spa add-on, interiors with guest count, promo close.
// v1: 11 shots with fades. v2 (21 Oct feedback: too many quick cuts): 6 shots,
// one clip per beat, hard cuts, ~3 s each, like the organic winners.

export const FPS = 30;

type Caption = { lines: string[]; sub?: string; size?: number };

export type Scene = {
  file: string;
  frames: number;
  trimBefore?: number;
  playbackRate?: number;
  caption: string;
  zoom?: number;
};

export type ReelProps = { scenes: Scene[]; transitionFrames: number };

const CAPTIONS: Record<string, Caption> = {
  hook: { lines: ["Girls Trip on", "the Water 🌊🥂"], sub: "National Harbor, MD", size: 78 },
  occasion: { lines: ["the perfect backdrop", "for birthdays and", "special moments ✨🎂"] },
  rooftop: { lines: ["sunset views from", "your private rooftop 🌅"] },
  addon: { lines: ["add-on a private chef", "or spa services ✨"] },
  interiors: { lines: ["ft. luxury interiors", "for up to 4 guests 👯‍♀️"] },
  close: { lines: ["Use code VIP100", "to Save $100! 👇"], size: 66 },
  // Share-CTA hook (Content Drive learnings, 21 Oct): the biggest reels in the Top
  // Performer sheet and FLOHOM's own reel 4 open with "send this to / who you bringing".
  sharehook: {
    lines: ["the first person that", "pops up when you hit", "share is who you're", "taking here 💕"],
    sub: "National Harbor, MD",
    size: 60,
  },
};

export const SCENES_V1: Scene[] = [
  { file: "hook_twilight", frames: 90, caption: "hook", zoom: 1.08 },
  { file: "girls_dance", frames: 33, caption: "occasion", zoom: 1.04 },
  { file: "girls_rooftop", frames: 75, caption: "occasion", zoom: 1.06 },
  { file: "deck_twilight", frames: 60, caption: "rooftop", zoom: 1.06 },
  { file: "cocktail_pour", frames: 54, trimBefore: 30, caption: "addon" },
  { file: "chef_stove", frames: 45, caption: "addon", zoom: 1.04 },
  { file: "spa_nails", frames: 45, caption: "addon", zoom: 1.04 },
  { file: "int_living", frames: 40, caption: "interiors", zoom: 1.06 },
  { file: "int_kitchen", frames: 40, caption: "interiors", zoom: 1.06 },
  { file: "int_bedroom", frames: 45, caption: "interiors", zoom: 1.06 },
  { file: "close_marina", frames: 100, caption: "close", zoom: 1.08 },
];

// Six beats, one shot each. girls_rooftop is a 2.77 s clip, slowed to 0.85x to hold 3.25 s.
export const SCENES_V2: Scene[] = [
  { file: "hook_twilight", frames: 105, caption: "hook", zoom: 1.08 },
  { file: "girls_rooftop", frames: 97, playbackRate: 0.85, caption: "occasion", zoom: 1.05 },
  { file: "deck_twilight", frames: 90, caption: "rooftop", zoom: 1.06 },
  { file: "chef_stove", frames: 90, caption: "addon", zoom: 1.05 },
  { file: "int_kitchen", frames: 90, caption: "interiors", zoom: 1.06 },
  { file: "close_marina", frames: 105, caption: "close", zoom: 1.08 },
];

// v3: v2 with the share-CTA hook instead of the title card. Same six shots, hard cuts,
// one people shot in six (Europe Luxury rule: people in 10-20% of shots, group-stay exception).
export const SCENES_V3: Scene[] = SCENES_V2.map((s) => (s.caption === "hook" ? { ...s, caption: "sharehook", frames: 120 } : s));

export const totalFrames = ({ scenes, transitionFrames }: ReelProps) =>
  scenes.reduce((n, s) => n + s.frames, 0) - transitionFrames * (scenes.length - 1);

const sceneStarts = (scenes: Scene[], t: number) =>
  scenes.reduce<number[]>((acc, _s, i) => {
    acc.push(i === 0 ? 0 : acc[i - 1] + scenes[i - 1].frames - t);
    return acc;
  }, []);

// Caption beats: first frame of the first scene using the key to the last frame of the last.
const captionRanges = (scenes: Scene[], t: number) => {
  const starts = sceneStarts(scenes, t);
  return Object.keys(CAPTIONS)
    .map((key) => {
      const idx = scenes.map((s, i) => (s.caption === key ? i : -1)).filter((i) => i >= 0);
      if (!idx.length) return null;
      const first = idx[0];
      const last = idx[idx.length - 1];
      return { key, from: starts[first], to: starts[last] + scenes[last].frames };
    })
    .filter((r): r is { key: string; from: number; to: number } => r !== null);
};

const Clip: React.FC<{ scene: Scene }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const scale = interpolate(frame, [0, scene.frames], [1, scene.zoom ?? 1], {
    extrapolateRight: "clamp",
  });
  return (
    <AbsoluteFill style={{ backgroundColor: "#06111f" }}>
      <OffthreadVideo
        src={staticFile(`flohom-nh/${scene.file}.mp4`)}
        trimBefore={scene.trimBefore}
        playbackRate={scene.playbackRate}
        muted
        style={{ width: "100%", height: "100%", objectFit: "cover", transform: `scale(${scale})` }}
      />
    </AbsoluteFill>
  );
};

const CaptionCard: React.FC<{ caption: Caption; from: number; to: number; hardCut: boolean }> = ({
  caption,
  from,
  to,
  hardCut,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < from || frame >= to) return null;
  const local = frame - from;
  // Reference reels (organic winners and the paid Myrtle Beach reel): the caption is
  // fully on from the first frame of its shot and cuts away with the shot. No entrance,
  // no fade. v1 keeps the spring pop and fade-out that go with its cross-fades.
  const pop = hardCut ? 1 : spring({ frame: local, fps, config: { damping: 14, stiffness: 160 } });
  const fadeOut = hardCut
    ? 1
    : interpolate(frame, [to - 8, to], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const size = caption.size ?? 58;
  return (
    <AbsoluteFill style={{ justifyContent: "flex-start", alignItems: "center", paddingTop: 560, opacity: fadeOut }}>
      <div
        style={{
          transform: `scale(${0.9 + 0.1 * pop})`,
          opacity: pop,
          textAlign: "center",
          fontFamily,
          color: "white",
          textShadow: "0 2px 6px rgba(0,0,0,0.55), 0 6px 24px rgba(0,0,0,0.45)",
          paddingLeft: 70,
          paddingRight: 70,
        }}
      >
        {caption.lines.map((line) => (
          <div key={line} style={{ fontSize: size, fontWeight: 700, lineHeight: 1.18 }}>
            {line}
          </div>
        ))}
        {caption.sub ? (
          <div style={{ fontSize: 40, fontWeight: 600, marginTop: 10, letterSpacing: 0.5 }}>{caption.sub}</div>
        ) : null}
      </div>
    </AbsoluteFill>
  );
};

export const NationalHarborGirlsTrip: React.FC<ReelProps> = ({ scenes, transitionFrames }) => {
  const hardCut = transitionFrames === 0;
  return (
    <AbsoluteFill style={{ backgroundColor: "#06111f" }}>
      <TransitionSeries>
        {scenes.flatMap((scene, i) => {
          const items = [
            <TransitionSeries.Sequence key={scene.file + i} durationInFrames={scene.frames}>
              <Clip scene={scene} />
            </TransitionSeries.Sequence>,
          ];
          if (!hardCut && i < scenes.length - 1) {
            items.push(
              <TransitionSeries.Transition
                key={`t${i}`}
                presentation={fade()}
                timing={linearTiming({ durationInFrames: transitionFrames })}
              />,
            );
          }
          return items;
        })}
      </TransitionSeries>
      {captionRanges(scenes, transitionFrames).map((r) => (
        <CaptionCard key={r.key} caption={CAPTIONS[r.key]} from={r.from} to={r.to} hardCut={hardCut} />
      ))}
    </AbsoluteFill>
  );
};
