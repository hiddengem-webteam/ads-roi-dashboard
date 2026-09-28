# Paradise Pointe — HG AI notes (2026-09-23)

Source: HG AI chat, Paradise Pointe client, "Can you check the ad performance on the retarget ads and see how its going recently - also lmk if we need to make any changes or increase spend etc." Screenshot saved by Shawal 2026-09-28.

## Short version
Meta is reporting a big drop in purchases credited to the BoF retargeting campaign over the last month, but direct bookings in the PMS didn't drop at all. Don't raise spend yet and don't cut it either. First find out whether fewer people are buying from these ads, or whether Meta is just seeing fewer of the purchases.

## Retargeting: last 31 days vs the 31 before
| Figure | 24 Jul–23 Aug | 24 Aug–23 Sep | Change |
|---|---|---|---|
| BoF Retargeting Website Visitors: spend | $1,333.02 | $1,503.60 | +13% |
| BoF: purchase value Meta credits to it | $26,937.09 | $6,347.16 | −76% |
| BoF: ROAS (Meta) | 20.21x | 4.22x | — |
| BoF: days Meta credited any purchase | 18 | 5 | — |
| MoF Retargeting Engagers: spend / value / ROAS | $667.30 / $386.55 / 0.58x | $747.50 / $397.74 / 0.53x | flat |
| Direct revenue from the PMS, by booking date | $133,979 (128 bookings) | $134,243 (125 bookings) | flat |

- Ad figures are Meta's own attribution; the latest window includes today, which isn't finished. Whole-account check 24 Aug–23 Sep: $2,976.65 spend, $6,744.90 purchase value, 2.27x, matches.
- "Days credited" counted from daily rows; BoF's first row in the earlier window is 28 Jul.

## What stands out
- Delivery didn't fall, credited purchases did. BoF spend went up; Meta credited purchases on most days through 20 Aug, since then only five (25 Aug, 2 Sep, 6 Sep, 13 Sep, 22 Sep).
- Direct revenue didn't follow: flat across the two windows. Our data can't tell whether other direct sources made up for lost retargeting sales, or whether Meta has stopped seeing purchases that are still happening.
- Worth checking: the channel label on direct bookings changed between the two windows. Earlier window "BE-API" had $121,265 and "website" $5,039; latest window "website" $115,452 and "BE-API" $8,006. Suggests direct bookings are now coming in, or being labelled, differently, and it shows up in the same window as the drop. Can't tell if the pixel or Conversions API setup changed, so it's a lead, not a diagnosis. If the booking path changed, the Purchase event may not fire on the new one.
- Ad cost against Meta-credited revenue on BoF went from 4.9% to 23.7%. Playbook alerts at 12% for sales campaigns, but judged on booking-engine revenue, not Meta's number, so a flag, not a verdict.
- MoF at 0.53x isn't a problem in itself; playbook judges lead campaigns on cost per lead and how many leads go on to book, not on ROAS.
- Calendar room isn't the constraint: next 30 days 1,041 of 1,428 open nights (73%), next 90 days 1,029 open (all channels). Two listings with nothing booked (Grand Getaway, Hill's Hideout, Nickajack and T-Tiny) are in-house counts.

## Recommendations
1. Check tracking before changing any budget. In Events Manager, compare daily Purchase events before and after 19–20 Aug; check what path now records "website" bookings; confirm Purchase fires with a value through both the pixel and the Conversions API. Ask whoever runs the booking site or Guesty whether the direct booking flow changed in late August.
2. Check BoF frequency in Ads Manager. If it's above about 3 per week, the playbook order is: add creative first (4–6 active ads, review-led ones included), then widen the audience (IG/FB engagers from the last 365 days, plus the GHL list), and trim budget only as a last resort.
3. Keep BoF spend where it is for now. Once tracking is confirmed, the playbook says extra money goes to prospecting before retargeting. Retargeting budget should only grow as the audience pool grows, in steps of no more than 20% every 3–4 days. No seed-lookalike prospecting campaign among the 3 active ones; that's where added fall spend would go. Point BoF creative at the open October-to-December dates too.

## Next best action
Run the Events Manager Purchase check and a test booking this week. The answer decides whether this is a tracking fix or a real performance problem.

## What it couldn't check
Frequency and reach, link clicks, Purchase event counts in Events Manager, whether the booking flow actually changed, MoF lead counts, or which direct bookings came from Meta according to the booking engine.
