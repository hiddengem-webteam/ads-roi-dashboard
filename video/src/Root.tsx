import { Composition } from "remotion";
import { ClientReel, specFrames } from "./flohom/ClientReel";
import { SPECS } from "./flohom/specs.generated";
import {
  FPS,
  NationalHarborGirlsTrip,
  SCENES_V1,
  SCENES_V2,
  SCENES_V3,
  totalFrames,
} from "./flohom/NationalHarborGirlsTrip";

const v1 = { scenes: SCENES_V1, transitionFrames: 8 };
const v2 = { scenes: SCENES_V2, transitionFrames: 0 };
const v3 = { scenes: SCENES_V3, transitionFrames: 0 };

// One composition per client spec in video/specs/*.json (run scripts/build-reel-specs.mjs after editing).
const specs = SPECS;

export const RemotionRoot: React.FC = () => {
  return (
    <>
      {/* npx remotion render FLOHOM-NH-GirlsTrip out/flohom-nh-girls-trip.mp4 */}
      <Composition
        id="FLOHOM-NH-GirlsTrip"
        component={NationalHarborGirlsTrip}
        durationInFrames={totalFrames(v1)}
        fps={FPS}
        width={1080}
        height={1920}
        defaultProps={v1}
      />
      {/* npx remotion render FLOHOM-NH-GirlsTrip-v2 out/flohom-nh-girls-trip-v2.mp4 */}
      <Composition
        id="FLOHOM-NH-GirlsTrip-v2"
        component={NationalHarborGirlsTrip}
        durationInFrames={totalFrames(v2)}
        fps={FPS}
        width={1080}
        height={1920}
        defaultProps={v2}
      />
      {/* npx remotion render FLOHOM-NH-GirlsTrip-v3 out/flohom-nh-girls-trip-v3.mp4 */}
      <Composition
        id="FLOHOM-NH-GirlsTrip-v3"
        component={NationalHarborGirlsTrip}
        durationInFrames={totalFrames(v3)}
        fps={FPS}
        width={1080}
        height={1920}
        defaultProps={v3}
      />
      {specs.map((spec) => (
        <Composition
          key={spec.slug}
          id={`Reel-${spec.slug}`}
          component={ClientReel}
          durationInFrames={specFrames(spec)}
          fps={spec.fps ?? 30}
          width={1080}
          height={1920}
          defaultProps={spec}
        />
      ))}
    </>
  );
};
