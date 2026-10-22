# Advanced-setup clients: one reel each (2026-10-22)

One Remotion reel per advanced-setup account from the 2026-10-19 benchmark report, built the same way as the approved FLOHOM v2: 5-6 shots of 3-4 s, hard cuts, static Poppins captions from frame one, hook card with location, close with the direct-booking offer. Each reel's hook and music come from that client's best organic reel of the last 90 days (pull under `pulls/2026-10-22/`, ranked against the account median by `scripts/pull-ig-reels.mts`). Clips are the client's own Drive footage, staged and normalised to 1080x1920/30 fps in `video/public/<slug>/` (gitignored).

Build: `video/specs/<slug>.json` → `scripts/build-reel-specs.mjs` → `Reel-<slug>` composition (`video/src/flohom/ClientReel.tsx`) → `scripts/render-reels.sh <slug>` (render, `add-music.sh`, `ig-export.sh`).

Shared assumptions to check before any of these go live: promo codes and offers were taken from the client's current ads (manifest copy) or the reel captions; where a code looked wrong it was left out. Music is the commercial track Shazam identified on the source reel, so every track is class `licensed` in the ledger and Ads Manager review is the gate.

## Status

| Client | Reel | Notes |
|---|---|---|
| Asheville River Cabins | `asheville-river-cabins-IG.mp4` | 6 beats, 19.0 s |
| AwayFrames | `awayframes-IG.mp4` | 5 beats, 18.0 s |
| Bison Ridge Retreat | `bison-ridge-retreat-IG.mp4` | 6 beats, 19.0 s |
| Endless Stays | `endless-stays-IG.mp4` | 6 beats, 19.0 s |
| Green Springs Inn | `green-springs-inn-IG.mp4` | 5 beats, 18.7 s |
| Little River Landing | `little-river-landing-IG.mp4` | 6 beats, 19.5 s |
| North Star Lodge & Resort | `north-star-lodge-resort-IG.mp4` | 6 beats, 16.2 s |
| Paradise Pointe | `paradise-pointe-IG.mp4` | 6 beats, 19.0 s |
| Ponderosa Pines Resort | `ponderosa-pines-resort-IG.mp4` | 6 beats, 19.0 s |
| Selah Place | `selah-place-IG.mp4` | 6 beats, 19.0 s |
| Starlight Haven Weiss Lake | `starlight-haven-weiss-lake-IG.mp4` | 6 beats, 19.0 s |
| Starlight Haven Hot Springs | `starlight-haven-IG.mp4` | 6 beats, 19.0 s |
| Stay on 30a | `stay-on-30a-IG.mp4` | 6 beats, 19.0 s |
| Stay Saluda | `stay-saluda-IG.mp4` | 6 beats, 19.0 s |
| Taberg Falls | `taberg-falls-IG.mp4` | 6 beats, 19.0 s |
| The Outpost | `the-outpost-IG.mp4` | 6 beats, 19.0 s |
| Treetop Escapes | `treetop-escapes-IG.mp4` | 6 beats, 19.0 s |
| Walden Retreats | `walden-retreats-IG.mp4` | 6 beats, 19.0 s |
| Ridge & Falls | not built | Drive clips not downloadable (see Blocked) |
| American River Resort | not built | Drive clips not downloadable (see Blocked) |

## Blocked: Drive folders that need link-sharing

Anonymous download (`drive.usercontent.google.com/download?id=…`) only works for files inside a folder shared with "anyone with the link"; the Drive connector can list these folders but cannot hand over video content. These came back HTTP 400 / "not shared":

- **Ridge & Falls** root `1Mst4lR2mvDWIwIP0dJjHpf5m3cahGhUD` (Black Diamond, Dreamer, Firefly, Moonlight cabins). Hook ready: "Unfortunately, this getaway ruined all other getaways for me…" (pickleball, pool, sauna; Menlo GA; code STAY10). Music identified: Babydoll (Jamie Miller).
- **American River Resort** root `1_6bgQnUbBi74L9V979Tc2VD2D8ZeonPD` (General, Destination). Hook ready: "Whitewater Rafting Retreat, Coloma CA / sleep steps from the river". Music identified: Stargazing (Myles Smith). No ads in the account yet.
- **North Star Lodge & Resort** root `1A8zMD8LlA823RxZQV9IEMRkj1ic65-CH`: only the 3 Twilight clips were downloadable, so the reel reuses them split in halves. General, Wide and Josh CF folders need sharing for a proper cut.
- **Green Springs Inn** root `14A3Bl6XANUtdoKbUt7gD1izdnv-6I2XY`: only the 5 drone clips (NEW Drone Edited) came through; no interiors.
- **AwayFrames** `1-K25s57uSk1THd2pwdzyuF4BnjV3H9Q4`: 4 of 10 staged clips were corrupt on download (CF winter content); the reel uses the 5 clean General clips, all summer.

Once shared, re-stage with the scratch `stage_clips.py` (or re-pull by ID) and render with `scripts/render-reels.sh <slug>`.

## Reels

### Asheville River Cabins (`asheville-river-cabins`)

- Hook source: IG reel [Db83Vu7hEEt](https://www.instagram.com/reel/Db83Vu7hEEt/) 8,584 views, 4.1x median; caption lead: "Comment ARC below and get $50 off your 1st stay with us! 📍Asheville River Cabins - Asheville, NC A sneak peek…"
- Music: Midnight Sun (Zara Larsson), from the same reel. Licensed; Ads Manager outcome pending.
- 6 beats, 19.0 s:
  1. `02_Twilight_6` (3.5 s): "Girls Trip in / North Carolina 🥂" sub: Asheville, NC · 2 hrs from Charlotte
  2. `04_Kyle_LGC_8` (3.0 s): "a cabin for you and / your best friends"
  3. `10_Amenities_9` (3.0 s): "afternoons on the / French Broad River 🛶"
  4. `01_Twilight_8` (3.0 s): "end the day in / the sauna 🧖‍♀️"
  5. `03_Twilight_4` (3.0 s): "and mornings / like this ☀️"
  6. `06_Enhanced_1` (3.5 s): "Use code VIP50 / for $50 off 👇"
- Clips:
  - `02_Twilight_6` ← Looking Glass Cabins / Twilight-6.mp4 (Drive `1AY6WkZOoT19zgOWuDWeANvPTPnUMAzf1`)
  - `04_Kyle_LGC_8` ← Looking Glass Cabins / Kyle-LGC-8.mp4 (Drive `1V8Pyn0DYa7WHKZY1Lkh9DSHdJx5K_LA1`)
  - `10_Amenities_9` ← Looking Glass Cabins / Amenities-9.mp4 (Drive `17yi-x_R2ALFMgZnzqOLjmWIitcDbppGN`)
  - `01_Twilight_8` ← Looking Glass Cabins / Twilight-8.mp4 (Drive `1CrdkOyHXMxwwQ8Xer1p8BXCP4o2S53lY`)
  - `03_Twilight_4` ← Looking Glass Cabins / Twilight-4.mp4 (Drive `1t0vvQ1SrXOZV2APJSSZwyL340W9ol_3Z`)
  - `06_Enhanced_1` ← Looking Glass Cabins / Enhanced-1.mp4 (Drive `15XjsmebIRYIMQhDXpbSIoFcKJn9QT06P`)
- Files: `video/out/clients/asheville-river-cabins.mp4` (silent master), `asheville-river-cabins-music.mp4`, `asheville-river-cabins-IG.mp4` (delivery).

### AwayFrames (`awayframes`)

- Hook source: IG reel [DbL8SY8hAvI](https://www.instagram.com/reel/DbL8SY8hAvI/) 5,369 views, 7.2x median; caption lead: "👇Booking Details |📍30 min from Yellowstone National Park A design-forward A-frame escape where modern architec…"
- Music: Wings (feat. sped up nightcore) [Sped Up Version] (Birdy), from the same reel. Licensed; Ads Manager outcome pending.
- 5 beats, 18.0 s:
  1. `08_AwayFramesGeneral_Clip3` (3.5 s): "idaho date idea: / an A-frame in the woods 🌲" sub: Island Park, 30 min from Yellowstone
  2. `09_AwayFramesGeneral_Clip1` (3.5 s): "private hot tub / under the pines ♨️"
  3. `07_AwayFramesGeneralClip10` (3.5 s): "wake up to / this view 🌅"
  4. `03_AwayFramesGeneral_Clip19` (3.5 s): "cozy nights in, / just the two of you"
  5. `10_AwayFramesGeneral_Clip32` (4.0 s): "book direct & save $100 / on your stay 🌲" sub: link in bio
- Clips:
  - `08_AwayFramesGeneral_Clip3` ← General / AwayFramesGeneral-Clip3.mp4 (Drive `1JmZCnpGi4380sThjF2TJBgPAvs-UEYlq`)
  - `09_AwayFramesGeneral_Clip1` ← General / AwayFramesGeneral-Clip1.mp4 (Drive `1iW-L4VBg_mFK1eX7YjVOFnmrpEpFhiPx`)
  - `07_AwayFramesGeneralClip10` ← General / AwayFramesGeneralClip10.mp4 (Drive `1i3_46k-KCMFoC8hSkm0tLZnpqbe989Mj`)
  - `03_AwayFramesGeneral_Clip19` ← General / AwayFramesGeneral-Clip19.mp4 (Drive `1yS82qvIeoMJpygtSqkrCo5BTkzkeqAoI`)
  - `10_AwayFramesGeneral_Clip32` ← General / AwayFramesGeneral-Clip32.mp4 (Drive `1Kam-XGcL6gAh8GpNbE2Pw5mnkozZSGj1`)
- Files: `video/out/clients/awayframes.mp4` (silent master), `awayframes-music.mp4`, `awayframes-IG.mp4` (delivery).

### Bison Ridge Retreat (`bison-ridge-retreat`)

- Hook source: IG reel [DbL8SPshn8e](https://www.instagram.com/reel/DbL8SPshn8e/) 21,235 views, 10.9x median; caption lead: "👇 Booking Details 📍 Whitefish, MT 🌐 Book through the link in our bio and SAVE $100 on your first stay. At Biso…"
- Music: Good Times & Tan Lines (Zach Top), from the same reel. Licensed; Ads Manager outcome pending.
- 6 beats, 19.0 s:
  1. `19_Bison_Ridge_Retreat_General_Aug2026_CF_C` (3.5 s): "cozy cabin getaway 🏔️" sub: Whitefish, Montana
  2. `15_Cabins_SpringSummer35` (3.0 s): "fire pit nights under / the mountains 🔥"
  3. `05_Bison_Ridge_Retreat_General_Aug2026_CF_C` (3.0 s): "a kitchen worth / cooking in"
  4. `07_Bison_Ridge_Retreat_General_Aug2026_CF_C` (3.0 s): "and a bed you won't / want to leave"
  5. `16_Fall_8_1_mp4_general` (3.0 s): "fall in Montana / looks like this 🍂"
  6. `11_Bison_Ridge_Retreat_General_Aug2026_CF_C` (3.5 s): "Book direct & / save $100 👇"
- Clips:
  - `19_Bison_Ridge_Retreat_General_Aug2026_CF_C` ← Cabins - Fall / Bison Ridge Retreat-General-Aug2026-CF-Clip20 (1).mp4 (Drive `1L1bg9yd8RP_tXiG5DN4CNM2iA0sXbx-k`)
  - `15_Cabins_SpringSummer35` ← Cabins - Spring/Summer / Cabins-SpringSummer35.mp4 (Drive `1B21m_8eK1vPEPHjmsub24P3v0lO_xiYN`)
  - `05_Bison_Ridge_Retreat_General_Aug2026_CF_C` ← Cabins - Fall / Bison Ridge Retreat-General-Aug2026-CF-Clip22 (1).mp4 (Drive `1NKEeYRXc6byx-9bFJkn3vNGFzagftfiY`)
  - `07_Bison_Ridge_Retreat_General_Aug2026_CF_C` ← The Lodge - Fall / Bison Ridge Retreat-General-Aug2026-CF-Clip6.MP4 (Drive `1yxWb3SvmF6oljE0mkeq7BLhoTHwz5Fre`)
  - `16_Fall_8_1_mp4_general` ← The Lodge - Fall / Fall_8 (1).mp4 - general.mp4 (Drive `1cthDuAwj7grEqMggSmYTh0z4y4uyhE__`)
  - `11_Bison_Ridge_Retreat_General_Aug2026_CF_C` ← Cabins - Fall / Bison Ridge Retreat-General-Aug2026-CF-Clip18 (1).mp4 (Drive `1PpuwmZQrTmxfjev0qfD-dRp8beXmgxjZ`)
- Files: `video/out/clients/bison-ridge-retreat.mp4` (silent master), `bison-ridge-retreat-music.mp4`, `bison-ridge-retreat-IG.mp4` (delivery).

### Endless Stays (`endless-stays`)

- Hook source: IG reel [DcCA845BcYl](https://www.instagram.com/reel/DcCA845BcYl/) 495,002 views, 284.8x median; caption lead: "👇 Booking Details 📍Poconos, PA Comment PLAYCATION & we’ll send you the direct link to book your stay! 🌐 Book y…"
- Music: Celebration (Kool & The Gang), from the same reel. Licensed; Ads Manager outcome pending.
- 6 beats, 19.0 s:
  1. `10_ES_AI_BeachDreamHouse_Clip17` (3.5 s): "insane group / getaway 🌴" sub: Seminole, FL
  2. `05_ES_AI_BeachDreamHouse_Clip33` (3.0 s): "private pool for / the whole crew"
  3. `02_ES_AI_BeachDreamHouse_Clip29` (3.0 s): "movie nights in / your own theater 🍿"
  4. `08_ES_AI_BeachDreamHouse_Clip28` (3.0 s): "dinner outside, / every night"
  5. `04_ES_AI_BeachDreamHouse_Clip10` (3.0 s): "and a court to / settle the score 🏀"
  6. `01_ES_AI_BeachDreamHouse_Clip4` (3.5 s): "Use code ESTAYS10 / for 10% off 👇"
- Clips:
  - `10_ES_AI_BeachDreamHouse_Clip17` ← Beach Dream House / ES-AI-BeachDreamHouse-Clip17.mp4 (Drive `1yayZD4SgahU2dOcPd0V1dn4foOhy81oX`)
  - `05_ES_AI_BeachDreamHouse_Clip33` ← Beach Dream House / ES-AI-BeachDreamHouse-Clip33.mp4 (Drive `1Lfe2rBcxWZ2SEEAk_NTsbisCjvuM8DWy`)
  - `02_ES_AI_BeachDreamHouse_Clip29` ← Beach Dream House / ES-AI-BeachDreamHouse-Clip29.mp4 (Drive `1A8vVfc8BoSuro7LoyzallERY9Q7F1yY9`)
  - `08_ES_AI_BeachDreamHouse_Clip28` ← Beach Dream House / ES-AI-BeachDreamHouse-Clip28.mp4 (Drive `1ABnRgg1Qlq0zMKXVo-MQ1dZJuOy_9veW`)
  - `04_ES_AI_BeachDreamHouse_Clip10` ← Beach Dream House / ES-AI-BeachDreamHouse-Clip10.mp4 (Drive `19eo3FTSrrksnearVOLMNmoBxu9FIQzcf`)
  - `01_ES_AI_BeachDreamHouse_Clip4` ← Beach Dream House / ES-AI-BeachDreamHouse-Clip4.mp4 (Drive `1HoXLPEUrHdwsNTl9MSsy1OmHkXVphbvE`)
- Files: `video/out/clients/endless-stays.mp4` (silent master), `endless-stays-music.mp4`, `endless-stays-IG.mp4` (delivery).

### Green Springs Inn (`green-springs-inn`)

- Hook source: IG reel [Ddj3L1MSfCd](https://www.instagram.com/reel/Ddj3L1MSfCd/) 3,621 views, 3.7x median; caption lead: "Needing an escape with your partner in the mountains? ✨ Comment “Recharge” and we’ll send you 10% off your fir…"
- Music: About You (The 1975), from the same reel. Licensed; Ads Manager outcome pending.
- 5 beats, 18.7 s:
  1. `01_DJI_0096` (3.2 s, 0.8x): "not to flirt or anything, / but..." sub: Ashland, Oregon
  2. `04_DJI_0072` (4.0 s, 0.8x): "i'd totally stay in a cozy / cabin in the woods with you 🌲"
  3. `02_DJI_0073` (3.4 s, 0.8x): "& talk all night / on the porch ✨"
  4. `03_DJI_0094` (3.1 s, 0.8x): "just trees, quiet / & the two of us 🌲"
  5. `05_DJI_0075` (5.0 s, 0.8x): "book direct & save 10% / code VIP10 🌲" sub: link in bio
- Clips:
  - `01_DJI_0096` ← NEW Drone Edited / DJI_0096.mov (Drive `1XMqckrRj70vKgZGE_bpzVtUmRx5g8Fdg`)
  - `04_DJI_0072` ← NEW Drone Edited / DJI_0072.mov (Drive `10bkntcCF6bd_L9bkFRchAevfK9rtI3d6`)
  - `02_DJI_0073` ← NEW Drone Edited / DJI_0073.mov (Drive `1JaPABHgmSw9JYgmXZFLhK5_wRP0xVRCU`)
  - `03_DJI_0094` ← NEW Drone Edited / DJI_0094.mov (Drive `1IwjQ7UM-IvuPI8haR92FtclwH64ijLEz`)
  - `05_DJI_0075` ← NEW Drone Edited / DJI_0075.mov (Drive `1evHaHUe85YQ-psKNf3WMTKw5ZY6eQ6Ys`)
- Files: `video/out/clients/green-springs-inn.mp4` (silent master), `green-springs-inn-music.mp4`, `green-springs-inn-IG.mp4` (delivery).

### Little River Landing (`little-river-landing`)

- Hook source: IG reel [DeH6QGTh_6f](https://www.instagram.com/reel/DeH6QGTh_6f/) 679 views, 2.5x median; caption lead: "👇 Booking Details📍 Cedar Bluff, AL Tag your lakeside crew 🌊 Comment ’RECHARGE’ and save 10% off your stay! Why…"
- Music: Chill lang (Choithrams), from the same reel. Licensed; Ads Manager outcome pending.
- 6 beats, 19.5 s:
  1. `06_LRL_12` (4.0 s): "we should be at this / lakefront resort instead of / whatever adult thing / we have to do today" sub: Cedar Bluff, AL
  2. `07_LRL_3` (3.0 s): "lake days with / your crew 🌊"
  3. `08_LRL_38` (3.0 s): "kayaks right off / the dock 🛶"
  4. `01_LRL_31` (3.0 s): "dinner with this view"
  5. `09_LRL_32` (3.0 s): "rooms steps from / the water"
  6. `03_LRL_1` (3.5 s): "Use code STAY10 / & save 10% 👇"
- Clips:
  - `06_LRL_12` ← Reel Automation / LRL-12.mp4 (Drive `128d-1l9sq73cpuKq7Sxt-RK4ZRRvitqg`)
  - `07_LRL_3` ← Reel Automation / LRL-3.mp4 (Drive `1PFPMPCWUGZPZvnhwC3YwvjtBHhj_B0qx`)
  - `08_LRL_38` ← Reel Automation / LRL-38.mp4 (Drive `1nySEgL6L4XwrqIX97gU_ejFLPdnFQ7Fd`)
  - `01_LRL_31` ← Reel Automation / LRL-31.mp4 (Drive `1EYV67nHACVT9QUZIDYu7eLenxvHBWjI1`)
  - `09_LRL_32` ← Reel Automation / LRL-32.mp4 (Drive `1alx35gtv7WInaOR2XpkvFi25vfb8qzai`)
  - `03_LRL_1` ← Reel Automation / LRL-1.mp4 (Drive `1dCzvcjXVK1aZWG5yGlR0wI6DbYpmD2_X`)
- Files: `video/out/clients/little-river-landing.mp4` (silent master), `little-river-landing-music.mp4`, `little-river-landing-IG.mp4` (delivery).

### North Star Lodge & Resort (`north-star-lodge-resort`)

- Hook source: IG reel [Ddoh3EDhO9r](https://www.instagram.com/reel/Ddoh3EDhO9r/) 1,090 views, 2.5x median; caption lead: "👇 Booking Details 📍 Killington, VT 🌐 Book through the link in our bio and save 10% on stays of 2 nights or mor…"
- Music: Fade into You (Mazzy Star), from the same reel. Licensed; Ads Manager outcome pending.
- 6 beats, 16.2 s:
  1. `03_Twilight_CF_Clip4V2` (3.0 s, 0.85x): "$50/person per night / 2 mins from the slopes ⛷️" sub: Killington, Vermont
  2. `01_Twilight_CF_Clip6` (3.0 s, 0.85x): "outdoor pool / for après-ski ♨️"
  3. `02_Twilight_CF_Clip3` (3.0 s, 0.85x): "wine by the pool / at sunset 🍷"
  4. `03_Twilight_CF_Clip4V2` (2.8 s, 0.85x): "sleeps 4, / ski-trip ready 🎿"
  5. `01_Twilight_CF_Clip6` (2.8 s, 0.85x): "ski in the morning, / swim at sunset"
  6. `02_Twilight_CF_Clip3` (1.6 s, 0.85x): "book direct & save 10% / on 2+ nights 🎿"
- Clips:
  - `03_Twilight_CF_Clip4V2` ← Twilight / Twilight-CF-Clip4V2.mp4 (Drive `1b41nS8OmrdYUYvZXam4oPVHtSjjZIo0x`)
  - `01_Twilight_CF_Clip6` ← Twilight / Twilight-CF-Clip6.mp4 (Drive `1MP7MCqJY_xV3ZQOiQQFfRBhxg6WA2_Ih`)
  - `02_Twilight_CF_Clip3` ← Twilight / Twilight-CF-Clip3.mp4 (Drive `1myhWnC3vMspovzKJKYM2sj8dLjWuvH7R`)
- Files: `video/out/clients/north-star-lodge-resort.mp4` (silent master), `north-star-lodge-resort-music.mp4`, `north-star-lodge-resort-IG.mp4` (delivery).

### Paradise Pointe (`paradise-pointe`)

- Hook source: IG reel [DbL8Tnrp4wF](https://www.instagram.com/reel/DbL8Tnrp4wF/) 10,152 views, 4.3x median; caption lead: "👇Booking Details📍Bryant, AL 🫶Share this with your family and start planning your next getaway! 🌐Book through t…"
- Music: This Is How We Roll (feat. Luke Bryan) (Florida Georgia Line), from the same reel. Licensed; Ads Manager outcome pending.
- 6 beats, 19.0 s:
  1. `09_General_20` (3.5 s): "I'm not saying you should / take your kids here, but… 😏" sub: Bryant, AL
  2. `02_General_25` (3.0 s): "an indoor pool / that stays open 🏊"
  3. `04_General_26` (3.0 s): "farm friends to / feed in the morning 🐐"
  4. `10_General_36` (3.0 s): "kayaks on the lake / all afternoon 🛶"
  5. `07_General_5` (3.0 s): "and a lodge to / come home to 🔥"
  6. `06_General_35` (3.5 s): "Book direct & / save $100 👇"
- Clips:
  - `09_General_20` ← General / General-20.mp4 (Drive `1W3pNQY7UJXwfqHhctBzKHCevUWQQRqr_`)
  - `02_General_25` ← General / General-25.mp4 (Drive `1iR-a8C7DweVWx5YSmBT6UKv9UoEHROUV`)
  - `04_General_26` ← General / General-26.mp4 (Drive `1jNM5PU1EoepXMFCIoine6G8e5l4-ci0a`)
  - `10_General_36` ← General / General-36.mp4 (Drive `1aTcLva3AiWCQJfzg6U5b9RsL9wY5HEaj`)
  - `07_General_5` ← General / General-5.mp4 (Drive `1k8PDF9O4aqQ4kCDynjNp3yQ6a20XQnBq`)
  - `06_General_35` ← General / General-35.mp4 (Drive `192hQyOqiLRIsYBoO4ZAt1W5qs5TBIx82`)
- Files: `video/out/clients/paradise-pointe.mp4` (silent master), `paradise-pointe-music.mp4`, `paradise-pointe-IG.mp4` (delivery).

### Ponderosa Pines Resort (`ponderosa-pines-resort`)

- Hook source: IG reel [Dbd_wYuyj9S](https://www.instagram.com/reel/Dbd_wYuyj9S/) 233,925 views, 38.0x median; caption lead: "👇 Booking Details📍Ponderosa Pines Resort | Parks, AZ 🌐 Book through the link in our bio (Save 20%) — calendar…"
- Music: august (Taylor Swift), from the same reel. Licensed; Ads Manager outcome pending.
- 6 beats, 19.0 s:
  1. `07_PRC_24` (3.5 s): "as low as $57 / per person per night" sub: Parks, AZ · en route to the Grand Canyon
  2. `02_PRC_6` (3.0 s): "hot tub in the pines 🫧"
  3. `04_PRC_3` (3.0 s): "cold plunge, / then warm back up ❄️"
  4. `01_PRC_16` (3.0 s): "wake up to this view"
  5. `06_PRC_14` (3.0 s): "nights that end / like this ✨"
  6. `08_PRC_13` (3.5 s): "Use code VIP10 / & save 10% 👇"
- Clips:
  - `07_PRC_24` ← Peaked Roof Cabin / PRC-24.mp4 (Drive `12tpzkHvngLWyiq8MOWQ8AKEHONMXHBNo`)
  - `02_PRC_6` ← Peaked Roof Cabin / PRC-6.mp4 (Drive `1LRjCXtRJZtsfJOTaee5OUXU6-GnObrbN`)
  - `04_PRC_3` ← Peaked Roof Cabin / PRC-3.mp4 (Drive `1AJ45sZccsZ0FFkfID8-ybNupAP0_50Rs`)
  - `01_PRC_16` ← Peaked Roof Cabin / PRC-16.mp4 (Drive `1iiw5h5jctLEGqOiV2grMCXhqO1PNb9PY`)
  - `06_PRC_14` ← Peaked Roof Cabin / PRC-14.mp4 (Drive `1PIC_5SbtzTV8lsWvvCOueln5S_FOCTXo`)
  - `08_PRC_13` ← Peaked Roof Cabin / PRC-13.mp4 (Drive `15FaCVF6Iq6I03ybUnu6HpHuciRAr-oY4`)
- Files: `video/out/clients/ponderosa-pines-resort.mp4` (silent master), `ponderosa-pines-resort-music.mp4`, `ponderosa-pines-resort-IG.mp4` (delivery).

### Selah Place (`selah-place`)

- Hook source: IG reel [DcO46DxBW2M](https://www.instagram.com/reel/DcO46DxBW2M/) 77,924 views, 62.7x median; caption lead: "👇 Booking Details📍 Athens, TX — East Texas Comment “recharge” and we’ll send you 10% off your first stay. At S…"
- Music: Days Like These (Luke Combs), from the same reel. Licensed; Ads Manager outcome pending.
- 6 beats, 19.0 s:
  1. `03_Clip27` (3.5 s): "Nature Escape / for Two ❤️" sub: Athens, TX · 1 hr from Dallas
  2. `08_Clip28` (3.0 s): "a villa on the water, / all yours"
  3. `01_SunnyMorning_CF_Clip5` (3.0 s): "hot tub under / the trees 🫧"
  4. `06_Clip19` (3.0 s): "a fire that makes / you slow down 🔥"
  5. `10_Clip6` (3.0 s): "and nowhere / you need to be"
  6. `07_Clip32` (3.5 s): "Use code VIP10 / for 10% off 👇"
- Clips:
  - `03_Clip27` ← Villa Sunny Morning / Clip27.mp4 (Drive `14NiYlx26pYD40aw44sL7TzaxQi8ci0nN`)
  - `08_Clip28` ← Villa Sunny Morning / Clip28.mp4 (Drive `1SyKhDIdu1EYhfSUMTXuCuqLOQvS1Au2C`)
  - `01_SunnyMorning_CF_Clip5` ← Villa Sunny Morning / SunnyMorning-CF-Clip5.mp4 (Drive `1TkCoCalnzROwpr1lrvZ3aYABWzt588Ml`)
  - `06_Clip19` ← Villa Sunny Morning / Clip19.mp4 (Drive `1-_BiyV-yGYmeWX5Ah031EZedZz9_JfkK`)
  - `10_Clip6` ← Villa Sunny Morning / Clip6.mp4 (Drive `1yfVvUaY1m6JKw1MPI2RNuCnaNvza2ged`)
  - `07_Clip32` ← Villa Sunny Morning / Clip32.mp4 (Drive `1M3SCFL_-xDAkQk1zqQEp9yyoJUSB3IvE`)
- Files: `video/out/clients/selah-place.mp4` (silent master), `selah-place-music.mp4`, `selah-place-IG.mp4` (delivery).

### Starlight Haven Weiss Lake (`starlight-haven-weiss-lake`)

- Hook source: IG reel [Db3t0buBRv7](https://www.instagram.com/reel/Db3t0buBRv7/) 4,606 views, 4.7x median; caption lead: "👇Booking Details📍Weiss Lake | Alabama Book direct through the link in bio to SAVE on your first lakeside escap…"
- Music: Until I Found You (Em Beihold Version) (Stephen Sanchez & Em Beihold), from the same reel. Licensed; Ads Manager outcome pending.
- 6 beats, 19.0 s:
  1. `02_General8` (3.5 s): "a lakeside escape / for two 🌅" sub: Weiss Lake, Alabama
  2. `01_General11` (3.0 s): "sunset from your / own hot tub 🫧"
  3. `04_General7` (3.0 s): "an A-frame built / for date nights 🌹"
  4. `09_General16` (3.0 s): "mornings out / on the water 🛶"
  5. `05_General6` (3.0 s): "soak. slow down. / stay a while."
  6. `10_General12` (3.5 s): "Use code STAR23 / for 10% off 👇"
- Clips:
  - `02_General8` ← Weiss Lake / General8.mp4 (Drive `1ulT1SzOmoh7hxHMWManjOpDyoBlIrA7x`)
  - `01_General11` ← Weiss Lake / General11.mp4 (Drive `1wmnQ15E-hsNtKdo9zUMzphqg_WZBEvW_`)
  - `04_General7` ← Weiss Lake / General7.mp4 (Drive `1iNTBa-P3sRb2HAOYqZ_Ri3kCV0WaSzsS`)
  - `09_General16` ← Weiss Lake / General16.mp4 (Drive `1w7My9UU_qq9YoTpHN1lnDG5BxkAHd247`)
  - `05_General6` ← Weiss Lake / General6.mp4 (Drive `13-wGYCwrbllGkYmanADR-aoU68e_Oz4I`)
  - `10_General12` ← Weiss Lake / General12.mp4 (Drive `14X_gUGT_YUUqZl4pMJJFpP3_UDNXDPa1`)
- Files: `video/out/clients/starlight-haven-weiss-lake.mp4` (silent master), `starlight-haven-weiss-lake-music.mp4`, `starlight-haven-weiss-lake-IG.mp4` (delivery).

### Starlight Haven Hot Springs (`starlight-haven`)

- Hook source: IG reel [Db3t0buBRv7](https://www.instagram.com/reel/Db3t0buBRv7/) 4,606 views, 4.7x median; caption lead: "👇Booking Details📍Weiss Lake | Alabama Book direct through the link in bio to SAVE on your first lakeside escap…"
- Music: Until I Found You (Em Beihold Version) (Stephen Sanchez & Em Beihold), from the same reel. Licensed; Ads Manager outcome pending.
- 6 beats, 19.0 s:
  1. `04_Starlight_Haven_Hot_Springs_AI_Clip3` (3.5 s): "a cabin weekend / for two 🌲❤️" sub: Hot Springs, Arkansas
  2. `02_Starlight_Haven_Hot_Springs_General_Augu` (3.0 s): "your private cabin / in the pines"
  3. `08_General10` (3.0 s): "hot tub on the deck 🫧"
  4. `01_Starlight_Haven_Hot_Springs_AI_Clip2` (3.0 s): "movie nights by / the fire 🔥"
  5. `07_Starlight_Haven_Hot_Springs_General_Augu` (3.0 s): "and a sauna to / end the day 🧖"
  6. `09_General1` (3.5 s): "Use code STAR23 / for 10% off 👇"
- Clips:
  - `04_Starlight_Haven_Hot_Springs_AI_Clip3` ← 2026/Hot Springs / Starlight Haven-Hot Springs-AI-Clip3.mp4 (Drive `1rKU5T82m8U3Q0p-VGjNHnaSln-6Ua6nq`)
  - `02_Starlight_Haven_Hot_Springs_General_Augu` ← 2026/Hot Springs/August 2026 / Starlight Haven-Hot Springs-General-August2026-CF-Clip6.mp4 (Drive `1xV3x63h15D5MqW9GnFyQ5_YVyNPriFOd`)
  - `08_General10` ← *Reel Automation Clips/Hot Springs / General10.mp4 (Drive `1_lvWY2oxxbNPH2lGHNIMhiLJ1ttIHE1D`)
  - `01_Starlight_Haven_Hot_Springs_AI_Clip2` ← 2026/Hot Springs / Starlight Haven-Hot Springs-AI-Clip2.mp4 (Drive `1aYcbJzE66-T4tjIM0VzOwUgAolINC7pa`)
  - `07_Starlight_Haven_Hot_Springs_General_Augu` ← 2026/Hot Springs/August 2026 / Starlight Haven-Hot Springs-General-August2026-CF-Clip41.mp4 (Drive `1hEwUfIbYItYoARXYwq5WXNaJQ8ddCmmR`)
  - `09_General1` ← *Reel Automation Clips/Hot Springs / General1.mp4 (Drive `113SzQ6hUg3Ule7hdr62CfJ4bMZIVYhSl`)
- Files: `video/out/clients/starlight-haven.mp4` (silent master), `starlight-haven-music.mp4`, `starlight-haven-IG.mp4` (delivery).

### Stay on 30a (`stay-on-30a`)

- Hook source: IG reel [DdcIyKehDeE](https://www.instagram.com/reel/DdcIyKehDeE/) 8,546 views, 2.5x median; caption lead: "Comment the keyword ‘SUNSET’ to get $100 off your stay! 📍Find us along 30A, FL With Stay on 30A, every detail…"
- Music: The Sweet Escape (feat. Akon) (Gwen Stefani), from the same reel. Licensed; Ads Manager outcome pending.
- 6 beats, 19.0 s:
  1. `05_StayOn30a_AI_will_zimm_BarefootBliss_Cli` (3.5 s): "insane group / getaway 🌊" sub: 30A, Florida
  2. `04_StayOn30a_AI_will_zimm_BarefootBliss_Cli` (3.0 s): "a private pool, / steps from the sand"
  3. `08_StayOn30a_AI_will_zimm_BarefootBliss_Cli` (3.0 s): "your own boardwalk / to the beach 🏖️"
  4. `02_StayOn30a_AI_will_zimm_BarefootBliss_Cli` (3.0 s): "sunset dinners / on the porch"
  5. `09_StayOn30a_AI_will_zimm_BarefootBliss_Cli` (3.0 s): "and sunsets like this / every night"
  6. `06_StayOn30a_AI_will_zimm_BarefootBliss_Cli` (3.5 s): "Use code VIP100 / to Save $100! 👇"
- Clips:
  - `05_StayOn30a_AI_will_zimm_BarefootBliss_Cli` ← Barefoot Bliss / StayOn30a-AI-@will_zimm_-BarefootBliss-Clip13.mp4 (Drive `1dKXCoiB5hU2rLsy3Rn_N1xlm9MN_mSTW`)
  - `04_StayOn30a_AI_will_zimm_BarefootBliss_Cli` ← Barefoot Bliss / StayOn30a-AI-@will_zimm_-BarefootBliss-Clip7.mp4 (Drive `1gPX8SoSyVnbpGrl-UAaM4a7b5abwuyAf`)
  - `08_StayOn30a_AI_will_zimm_BarefootBliss_Cli` ← Barefoot Bliss / StayOn30a-AI-@will_zimm_-BarefootBliss-Clip23.mp4 (Drive `1XH_2-Oe11eXrYRkq-rTpJHrx2K3KA9vp`)
  - `02_StayOn30a_AI_will_zimm_BarefootBliss_Cli` ← Barefoot Bliss / StayOn30a-AI-@will_zimm_-BarefootBliss-Clip3.mp4 (Drive `1PnYAb4OiFMsN7WIkkmfxyeBNAhLpJvV0`)
  - `09_StayOn30a_AI_will_zimm_BarefootBliss_Cli` ← Barefoot Bliss / StayOn30a-AI-@will_zimm_-BarefootBliss-Clip6.mp4 (Drive `1ajLFvCzbr_SwHssG7LvQPw8q9fKA8Pxh`)
  - `06_StayOn30a_AI_will_zimm_BarefootBliss_Cli` ← Barefoot Bliss / StayOn30a-AI-@will_zimm_-BarefootBliss-Clip19.mp4 (Drive `1BhzMp1nAQtIfy1YNVwmZe0Su6z79SnDb`)
- Files: `video/out/clients/stay-on-30a.mp4` (silent master), `stay-on-30a-music.mp4`, `stay-on-30a-IG.mp4` (delivery).

### Stay Saluda (`stay-saluda`)

- Hook source: IG reel [DbmA14zBnwb](https://www.instagram.com/reel/DbmA14zBnwb/) 3,975 views, 3.8x median; caption lead: "👇Booking Details📍Saluda, NC 🫶Share this cozy cabin escape with who you’re bringing! 🌐Book through the link in…"
- Music: Reason I Sing (Acoustic) (Phil Wickham), from the same reel. Licensed; Ads Manager outcome pending.
- 6 beats, 19.0 s:
  1. `08_SunnyMorning_3` (3.5 s): "a cozy cabin escape / in the Blue Ridge 🏔️" sub: Saluda, NC
  2. `04_SunnyMorning_5` (3.0 s): "morning coffee by / the fire pit ☕"
  3. `01_Twilight_19` (3.0 s): "mountain views from / the bed 🌄"
  4. `07_SunnyMorning_11` (3.0 s): "dinner for everyone / at one table"
  5. `09_SunnyMorning_6` (3.0 s): "and a deck made / for doing nothing"
  6. `02_Twilight_18` (3.5 s): "Use code VIP10 / for 10% off 👇"
- Clips:
  - `08_SunnyMorning_3` ← Mountain Retreats Sunny Morning / SunnyMorning-3.mp4 (Drive `1-thI5Sa7Sz6yGWWdl-NNxjq5QSdzu47L`)
  - `04_SunnyMorning_5` ← Mountain Retreats Sunny Morning / SunnyMorning-5.mp4 (Drive `1rLJXKh5ZA4Kg4Xn9VoDevxYtzRfg38Gj`)
  - `01_Twilight_19` ← Mountain Retreats Twilight / Twilight-19.mp4 (Drive `1OpwRTBpaxj2a0fzPSz0VQxI_EYK4_SDD`)
  - `07_SunnyMorning_11` ← Mountain Retreats Sunny Morning / SunnyMorning-11.mp4 (Drive `1qJ-WoWPlQ2Do44LF0yxhOXqirQe7B8bH`)
  - `09_SunnyMorning_6` ← Mountain Retreats Sunny Morning / SunnyMorning-6.mp4 (Drive `1KeYEf98ZjzReNZbwLQWUexaIIP3qVPh3`)
  - `02_Twilight_18` ← Mountain Retreats Twilight / Twilight-18.mp4 (Drive `1c8AlFoLKLjbG9haWXL_qH4sAAA6Vpesq`)
- Files: `video/out/clients/stay-saluda.mp4` (silent master), `stay-saluda-music.mp4`, `stay-saluda-IG.mp4` (delivery).

### Taberg Falls (`taberg-falls`)

- Hook source: IG reel [DcJvV3IhroU](https://www.instagram.com/reel/DcJvV3IhroU/) 192,789 views, 36.8x median; caption lead: "👇 Booking Details📍 Taberg, NY ✨Six private mirror villas. A river, a creek, and waterfalls right outside your…"
- Music: Cinnamon Girl (Lana Del Rey), from the same reel. Licensed; Ads Manager outcome pending.
- 6 beats, 19.0 s:
  1. `10_TabergFalls_SpringSummer73` (3.5 s): "you. me. date weekend. / this mirror getaway? 🪞" sub: Taberg, NY
  2. `05_TabergFalls_SpringSummer55` (3.0 s): "a river, a creek and / waterfalls outside your door 🌊"
  3. `08_TabergFalls_SpringSummer33` (3.0 s): "wake up in a / glass-walled villa ☀️"
  4. `04_TabergFalls_SpringSummer68` (3.0 s): "your own hot tub, / nobody around 🫧"
  5. `02_Ta_berg_Falls_General_Property_Twilight_` (3.0 s): "and the night sky / from your deck ✨"
  6. `01_Ta_berg_Falls_General_Property_Twilight_` (3.5 s): "Use code VIP100 / to Save $100! 👇"
- Clips:
  - `10_TabergFalls_SpringSummer73` ← Spring-Summer / TabergFalls-SpringSummer73.mp4 (Drive `1qFuKNa3Wglr2GJestVgRUrLKHb-PchF-`)
  - `05_TabergFalls_SpringSummer55` ← Spring-Summer / TabergFalls-SpringSummer55.mp4 (Drive `1Ng-_WkmWIAC5ktTlYVwv7NyzDXEP_lXy`)
  - `08_TabergFalls_SpringSummer33` ← Spring-Summer / TabergFalls-SpringSummer33.mp4 (Drive `1uK0VSy_5IoERo23cShkDopAUXhSmUVuf`)
  - `04_TabergFalls_SpringSummer68` ← Spring-Summer / TabergFalls-SpringSummer68.mp4 (Drive `1SUM2jQJ2brmE3XMY3fsGC5ywBJSmIpVq`)
  - `02_Ta_berg_Falls_General_Property_Twilight_` ← Twilight / Tàberg Falls-General Property-Twilight-AI-Clip11.mp4 (Drive `1WWECz1MuwHu_CGJhERvnuybICWM8Y6-F`)
  - `01_Ta_berg_Falls_General_Property_Twilight_` ← Twilight / Tàberg Falls-General Property-Twilight-AI-Clip8.mp4 (Drive `1u39Ji7QfptPKjx2DEIVvLJSAudf9Phs5`)
- Files: `video/out/clients/taberg-falls.mp4` (silent master), `taberg-falls-music.mp4`, `taberg-falls-IG.mp4` (delivery).

### The Outpost (`the-outpost`)

- Hook source: IG reel [Dbd9yhIh7Fd](https://www.instagram.com/reel/Dbd9yhIh7Fd/) 99,931 views, 91.3x median; caption lead: "👇 Booking Details 📍 The Outpost | Valle, AZ 🌐 Book through the link in our bio to claim your Grand Canyon base…"
- Music: Chemtrails Over the Country Club (Lana Del Rey), from the same reel. Licensed; Ads Manager outcome pending.
- 6 beats, 19.0 s:
  1. `01_TheOutpost_AI_General_Twilight_Clip1` (3.5 s): "your Grand Canyon / basecamp 🏜️" sub: Valle, AZ · 25 min from the Canyon
  2. `03_The_Outpost_General_AI_Clip2` (3.0 s): "dinner under the / desert sky 🌅"
  3. `05_The_Outpost_General_AI_Clip7` (3.0 s): "an Airstream that's / all yours 🚐"
  4. `07_TheOutpost_General_LightWinter_CF_Clip39` (3.0 s): "sauna, then stars 🧖‍♀️"
  5. `09_TheOutpost_General_LightWinter_CF_Clip17` (3.0 s): "the quiet you came for"
  6. `02_TheOutpost_AI_General_Twilight_Clip2` (3.5 s): "Use code WELCOME10 / & save on your stay 👇"
- Clips:
  - `01_TheOutpost_AI_General_Twilight_Clip1` ← General Property/Twilight / TheOutpost-AI-General-Twilight-Clip1.mp4 (Drive `18WHGzFIgI6r00HOOg80HodhdY0TZi_5v`)
  - `03_The_Outpost_General_AI_Clip2` ← July 2026 / The Outpost-General-AI-Clip2.mp4 (Drive `14EyCsjOBP2qw08n9zcnGqX6KT1U7kpVp`)
  - `05_The_Outpost_General_AI_Clip7` ← July 2026 / The Outpost-General-AI-Clip7.mp4 (Drive `1zyHm3ENDpgSPie1Lx_wlkhzDWb43OTsN`)
  - `07_TheOutpost_General_LightWinter_CF_Clip39` ← General Property/Light Winter / TheOutpost-General-LightWinter-CF-Clip39.mp4 (Drive `1obABrp2tksHso5OvPexj4t7dcusT5uEx`)
  - `09_TheOutpost_General_LightWinter_CF_Clip17` ← General Property/Light Winter / TheOutpost-General-LightWinter-CF-Clip17.mp4 (Drive `1WSKxi-IDnrDs42DBTm3GG2FZ_AM0ShIj`)
  - `02_TheOutpost_AI_General_Twilight_Clip2` ← General Property/Twilight / TheOutpost-AI-General-Twilight-Clip2.mp4 (Drive `17iQAyaSCKeYXcmDM8zLMmceLM2rnMLY_`)
- Files: `video/out/clients/the-outpost.mp4` (silent master), `the-outpost-music.mp4`, `the-outpost-IG.mp4` (delivery).

### Treetop Escapes (`treetop-escapes`)

- Hook source: IG reel [DbT_RCWh-lW](https://www.instagram.com/reel/DbT_RCWh-lW/) 27,249 views, 16.0x median; caption lead: "👇Booking Details 📍Lookout Mountain, GA Tag the person you’d bring to this dreamy retreat in the treetops🌳❤️ ✨B…"
- Music: Dance With Me (Bruno Mars), from the same reel. Licensed; Ads Manager outcome pending.
- 6 beats, 19.0 s:
  1. `01_Twilight_7` (3.5 s): "you + me, a treehouse / in the mountains 🌲" sub: Lookout Mountain, GA
  2. `04_SunnyMorning_7` (3.0 s): "a private walkway to / your own treehouse"
  3. `03_Twilight_3` (3.0 s): "evenings by the fire 🔥"
  4. `06_SunnyMorning_9` (3.0 s): "a sauna up in / the canopy 🧖‍♀️"
  5. `05_SunnyMorning_6` (3.0 s): "and absolutely / nowhere to be"
  6. `02_Twilight_10` (3.5 s): "Book direct & / save $100 👇"
- Clips:
  - `01_Twilight_7` ← Autumn Blaze Twilight / Twilight-7.mp4 (Drive `1UCHI26JP6lbEuKpyRrMirwo63r0eLMUz`)
  - `04_SunnyMorning_7` ← Autumn Blaze Sunny Morning / SunnyMorning-7.mp4 (Drive `1sxxKObg8TiB-M3rjIs2y534LyZbt4cSE`)
  - `03_Twilight_3` ← Autumn Blaze Twilight / Twilight-3.mp4 (Drive `1R5B2eZIeh9CLVYbH_qQlPuLHv94wLIjR`)
  - `06_SunnyMorning_9` ← Autumn Blaze Sunny Morning / SunnyMorning-9.mp4 (Drive `1cobnlW9HwTAJaKv7c41XOF2wT1-3MYuY`)
  - `05_SunnyMorning_6` ← Autumn Blaze Sunny Morning / SunnyMorning-6.mp4 (Drive `1N2yz1SAfBYgzjwbRMZoPCjgcYuXuc0Nr`)
  - `02_Twilight_10` ← Autumn Blaze Twilight / Twilight-10.mp4 (Drive `1VN57cg69zy4kP0yvoCDML7Rd1GRgcjey`)
- Files: `video/out/clients/treetop-escapes.mp4` (silent master), `treetop-escapes-music.mp4`, `treetop-escapes-IG.mp4` (delivery).

### Walden Retreats (`walden-retreats`)

- Hook source: IG reel [DeR8R-Rp4YQ](https://www.instagram.com/reel/DeR8R-Rp4YQ/) 1,862 views, 1.3x median; caption lead: "👇 Booking Details 📍 Walden Retreats | Johnson City, TX 🌐 Book through the link in our bio A stay at Walden isn…"
- Music: Chemtrails Over the Country Club (Lana Del Rey), from the same reel. Licensed; Ads Manager outcome pending.
- 6 beats, 19.0 s:
  1. `07_Exterior_CF_Clip31` (3.5 s): "you could book a hotel, / or you could just…" sub: Johnson City, TX · Hill Country
  2. `02_Exterior_Twilight_CF_Clip3` (3.0 s): "a tent with a fire pit / and a view ⛺"
  3. `01_Interior_Twilight_CF_Clip1` (3.0 s): "soak under / the stars ✨"
  4. `09_Interior_CF_Clip17` (3.0 s): "breakfast in bed 🥐"
  5. `04_Exterior_CF_Clip14` (3.0 s): "and the Hill Country / at your door"
  6. `05_Exterior_CF_Clip19` (3.5 s): "Use code VIP10 / & save 10% 👇"
- Clips:
  - `07_Exterior_CF_Clip31` ← Luxury Tents / Exterior-CF-Clip31.mp4 (Drive `1Fz_F6bB47Pb6C69GlKr1aIE6MpoxDEOc`)
  - `02_Exterior_Twilight_CF_Clip3` ← Luxury Tents / Exterior-Twilight-CF-Clip3.mp4 (Drive `1TzRJci08V83u9XG9N04mw1UqnJjgYiky`)
  - `01_Interior_Twilight_CF_Clip1` ← Luxury Tents / Interior-Twilight-CF-Clip1.mp4 (Drive `1rCAAD_m2n6atmDqhEqunaETfu5C2dL0C`)
  - `09_Interior_CF_Clip17` ← Luxury Tents / Interior-CF-Clip17.mp4 (Drive `1n_iG4jquUz3fl55Et4Ga1krEImVVwYv8`)
  - `04_Exterior_CF_Clip14` ← Luxury Tents / Exterior-CF-Clip14.mp4 (Drive `1IZVW2_Zzn1H8fAuKTzDcRvIJXRBVky-2`)
  - `05_Exterior_CF_Clip19` ← Luxury Tents / Exterior-CF-Clip19.mp4 (Drive `11ppGmUq9B9ew5rjojPecK9tYSGIL-lVS`)
- Files: `video/out/clients/walden-retreats.mp4` (silent master), `walden-retreats-music.mp4`, `walden-retreats-IG.mp4` (delivery).

