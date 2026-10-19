# Creative review: FLOHOM, 19 October 2026 (test run)

Scope: Sales campaigns only (BoF retargeting and the two MoF lookalike campaigns), ads with at least $100 spend in the last 30 days, ranked by purchase ROAS then purchases. 9 ads qualified; 14 more ran under the $100 floor. Creatives, copy and the ranking table are in the Drive folder "Meta Ads - Top Performers / 2026-10-19 FLOHOM" and in `weekly/Creative Reviews/pulls/2026-10-19/FLOHOM/` (not committed).

## Ranking

| # | Ad | Campaign | Format | Spend | Purch | ROAS | CTR | Freq |
|---|---|---|---|---|---|---|---|---|
| 1 | BoF - Price Anchor - Static Image | MoF Lookalike 07/29 | static image | $230 | 3 | 12.0x | 2.65% | 3.2 |
| 2 | AD2 - MoF - Myrtle Beach - Reel | [Myrtle Beach] MoF Lookalike 09/17 | 17 s reel | $354 | 3 | 11.7x | 3.74% | 2.5 |
| 3 | BoF - Review - Carousel | MoF Lookalike 07/29 | 8-card carousel | $122 | 2 | 11.4x | 2.28% | 2.8 |
| 4 | BoF - Price Anchor - Looping Video | BoF Retargeting | 3.4 s loop | $122 | 0 | 0.0x | 2.55% | 2.2 |
| 5 | BoF - Price Anchor - Carousel | MoF Lookalike 07/29 | 6-card carousel | $242 | 0 | 0.0x | 2.07% | 2.5 |
| 6 | BoF - Price Anchor - Static Image | BoF Retargeting | static image | $132 | 1 | 4.7x | 2.29% | 2.9 |

Read the ROAS with care: the top three each sit on 2 or 3 purchases, so one booking moves an ad several places. The two zero-purchase ads are the firmer signal, since $122 and $242 bought nothing.

## What the winners share

1. **The $63 per person per night anchor on a dusk waterfront shot.** Ad 1 is a single frame: logo, the price line in caps, a strip of proof points (Girls' Trips, Private Waterfront, MD/VA/SC/NJ), the houseboat lit up at the National Harbor. Nothing else. It reads in one second in the feed.
2. **The Myrtle Beach reel is the only ad with a story.** Hook card "Girls Trip on the Water, North Myrtle Beach" over a sunset marina, then rooftop drinks, a birthday toast at sunset, the private chef and spa add-ons, a nail-tech scene, interiors "for 4 to 6 guests", fire pit, and a closing "Use code VIP100 to save $100" card. Captions on every scene, so it works muted. Highest CTR of the set (3.74%) and the biggest average order ($1,378).
3. **Social proof in the carousel.** Ad 3's cards are guest reviews with five stars over rooftop and city-light photos. It converts at the same rate as the price anchor on a third of the spend.

## What the losers share

- **Ad 4, the looping video, is the static price anchor with a few seconds of water movement.** No hook, no change of scene, nothing a still image does not already do. $122 for zero purchases. Retire this format across the account; the same clip in the 07/21 batch sits under the floor with $50 and nothing to show either.
- **Ad 5, the price-anchor carousel, repeats the same frame six times.** Every card carries the identical "Save $100" headline and a near-identical dusk shot with the price line. A carousel earns its swipe when each card adds something; this one asks for six swipes to say one thing. $242 for zero purchases is the worst result in the set.
- **Ad 6 is ad 1 in the retargeting campaign** (same file, same copy) at 4.7x. The creative is fine; the retargeting audience has seen the price anchor since July. Frequency is 2.9 there and 3.2 in the lookalike campaign, so both placements are due a refresh.

## Copy

All six ads run the same primary text and the same "Save $100 🌊" headline. The only thing being tested is the format. The Myrtle Beach reel is the single exception, with a group-trip hook ("The group chat has been talking about this trip for months. Time to actually book it.") and it is the strongest ad on CTR.

## Recommendations for the next cadence

1. **Make two or three more 15 to 20 second reels in the Myrtle Beach structure for the Potomac boats**: occasion hook (girls' trip, birthday, anniversary), rooftop at dusk, one add-on scene (chef or spa), interiors with the guest count, promo-code close. Captions on every scene.
2. **Retire the looping videos** and the price-anchor carousel. Keep the static price anchor, but refresh the photo and move the proof strip (rooftop, chef, locations) into the image for the retargeting audience that has seen the current one for three months.
3. **Rebuild carousels around reviews or a tour**, one idea per card: card 1 the price anchor, then rooftop, chef, bedroom, a review, the code. Do not repeat the headline on every card.
4. **Test copy, not just format.** Three headline variants to run against "Save $100": the price anchor ("From $63 per person per night"), the occasion ("Your girls' trip, on the water"), and a review quote. Keep the VIP100 code in the primary text.
5. **Split copy by audience.** Lookalike (cold) ads need the "what is this" line (a private floating suite on the water); the retargeting ads can lead with the code and a date nudge.
6. **Fewer ads per ad set.** 14 ads got under $100 in 30 days; Meta is concentrating spend on three or four and starving the rest. Launch four to five per ad set so each gets a fair read.

## Process notes from the test

- Pull script: `npx tsx scripts/pull-creatives.mts FLOHOM 2026-10-19`. Images and carousel cards come from the creative; videos come from the ad account's video library or, for Page reels, through a read-only page-scoped token.
- Video files cannot go to Drive through the connector (file bytes would pass through the model). Zapier's Google Drive "Upload File" action takes a file URL and is enabled but needs Shawal's one-time authorization; Google Drive for desktop on Shawal's Mac would make the upload a plain file copy.
- Next clients once the upload path is settled: Stay on 30a, Tàberg Falls, Paradise Pointe (after its purchase-value fix), The Cohost Company.
