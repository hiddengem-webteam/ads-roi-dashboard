---
workflow: general-video
flow: automation
storyboard: no
message: "Your girls' trip, on the water at National Harbor, from $63 per person per night, code VIP100 saves $100"
destination: instagram-reels
aspect: 1080x1920
language: en
audience: cold lookalike (MoF) women planning a group trip in the DC/MD/VA area
length: 15-20s
angle: occasion hook (girls' trip) in the Myrtle Beach reel structure
---

## Intent

One Instagram/Facebook reel for FLOHOM (floating suites / houseboats), built for the
Potomac boats at National Harbor, MD, following recommendation 1 of the
"Creative review - FLOHOM - 2026-10-19" doc: copy the structure of the winning
Myrtle Beach reel (AD2 - MoF - Myrtle Beach - Reel - 09/17/26, 11.7x ROAS,
3.74% CTR) for a different location. Structure: occasion hook card over a
dusk/sunset waterfront shot, rooftop at dusk, one add-on scene (chef or spa),
interiors with the guest count, promo-code close. Captions on every scene so it
works muted. Feel: warm, celebratory, real footage, no stock-video look.

## Assets

- clips/*.mp4 (staged from Drive "Reels Components / Reel Automation / Organized Clips /
  National Harbor-Girls Group") — National Harbor girls-group footage; hook, rooftop,
  interiors and close are cut from these.
- clips/addons/* (staged from Drive "Organized Clips / Add-Ons General") — private chef and
  spa/massage clips; one is the add-on scene.
- Reference only, not placed: the Myrtle Beach reel (Drive, creative-review folder),
  used for caption placement, size and the scene order.

## Customizations

- Hard cuts, no transitions, matching the reference reel.
- Caption identity matches the reference: white heavy rounded sans, dark drop shadow,
  centred in the upper third, one short line pair per scene, one emoji at most.
- Captions pop in per scene (spring-pop entrance), hold, and cut with the shot.
- Close card: "Use code VIP100 to Save $100!" over the lit boat at night.

## Notes

- Copy from the review doc, kept verbatim where it is a claim: "$63 per person per night",
  "for 4 to 6 guests", "code VIP100", "Save $100". Do not invent amenities.
- The primary text in Ads Manager carries the group-chat hook; the reel itself opens
  with the occasion card.
- No music bed: HeyGen BGM needs a signed-in heygen CLI and the local MusicGen
  fallback is not installed on this machine. The clips are silent except the add-on
  clips, whose sound is muted. Music is to be added in Ads Manager or supplied as a file.
- Autonomous run (flow: automation, storyboard: no): decisions are stated in the
  hand-off, the one kept question is render approval.
