// Per-client AM notes for September 2026 (per Shawal, Oct 5 2026) — shown on
// each client's /september view and included in the client-reporting JSON
// export. Keys are canonical dashboard client names.
export const SEPTEMBER_CLIENT_NOTES: Record<string, string> = {
  'American River Resort': 'We had no promo code usages this month.',
  'Nature Nooks': 'We need the client to send the PMS data — bookings and revenue are understated in portfolio totals until it comes in.',
  'Inspired Retreats': 'The updated ad creatives helped increase performance overall (increased bookings, leads, followers). No bookings traced to ads via promo codes this month.',
  'Paradise Pointe': 'Meta did not record revenue for 12 retargeting purchases (week of Sep 15–21 and Sep 29–30); their value was added manually at the average booking value (12 × $1,170.59 = $14,047.08) and the ROAS updated.',
  'Little River Landing': 'Newly launched campaigns — $921.36 spent, no revenue from ads yet.',
  'North Star Lodge & Resort': 'Newly launched campaigns — $579.92 spent, no revenue from ads yet. Revenue shown is from the client reporting sheet; no booking-level data this month.',
  'Ridge & Falls': 'Newly launched campaigns — $1,036.47 spent, no revenue from ads yet (spend exceeds the $871.49 September direct revenue, as expected for a launch month).',
  'Red White & Blue Views': 'No revenue from ads this month.',
  'StayLuxe': 'No revenue from ads this month. Booking tab is empty — confirming with the AM that no data is missing.',
  'Stay Southen Illinois': 'Meta pixel reported more retargeting purchases (27) than the month’s total bookings (22), so ad-attributed revenue is capped at the booking total. AM to confirm whether bookings are missing from the sheet or the pixel is double-counting.',
};
