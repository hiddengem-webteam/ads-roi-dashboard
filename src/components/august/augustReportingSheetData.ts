// August 2026 figures from the "Client Performance Tracking" Google Sheet
// (each client tab's August 2026 row: "Direct Booking Revenue" + "🎉 New
// Leads"). Used ONLY by /august. A zero revenue here means the sheet's
// revenue cell wasn't filled — the page falls back to the AM booking total
// for revenue while still using the sheet's lead count. Refreshed Sep 2 2026.
export interface ClientReportingFigures {
  directBookingRevenue: number;
  newLeads: number;
}

export const AUGUST_REPORTING_SHEET: Record<string, ClientReportingFigures> = {
  'American River Resort': { directBookingRevenue: 373863.99, newLeads: 609 },
  'Asheville River Cabins': { directBookingRevenue: 129646.2, newLeads: 1446 },
  'Away2PA': { directBookingRevenue: 113688.97, newLeads: 2000 },
  'Awayframes': { directBookingRevenue: 24359.94, newLeads: 210 },
  'Best Texas Travel': { directBookingRevenue: 33550.78, newLeads: 214 },
  'Big Moon Ranch': { directBookingRevenue: 17672.55, newLeads: 160 },
  'Bison Ridge Retreat': { directBookingRevenue: 20258.99, newLeads: 647 },
  'Columbia Gorge Getaways': { directBookingRevenue: 27772, newLeads: 120 },
  'Endless Stays': { directBookingRevenue: 28709.87, newLeads: 775 },
  'Evergreen Cabins': { directBookingRevenue: 46760.76, newLeads: 2553 },
  'Flohom': { directBookingRevenue: 145070.34, newLeads: 2307 },
  'Green Springs Inn': { directBookingRevenue: 45103.51, newLeads: 360 },
  'Hiawassee Glamping': { directBookingRevenue: 6730, newLeads: 290 },
  'Home Base': { directBookingRevenue: 51303.79, newLeads: 446 },
  'Inspired Retreats': { directBookingRevenue: 36331.33, newLeads: 364 },
  'Myrinn': { directBookingRevenue: 9144.52, newLeads: 273 },
  'Nature Nooks': { directBookingRevenue: 11284.66, newLeads: 534 },
  'Oak & Ember': { directBookingRevenue: 36811.7, newLeads: 1112 },
  'Paradise Pointe': { directBookingRevenue: 122370.05, newLeads: 1645 },
  'Parker Reserve': { directBookingRevenue: 12757.1, newLeads: 82 },
  'Ponderosa Pines Resort': { directBookingRevenue: 47994.79, newLeads: 2040 },
  'Raven Rock Mountain': { directBookingRevenue: 8394.41, newLeads: 519 },
  'Red White & Blue Views': { directBookingRevenue: 20277.56, newLeads: 407 },
  'Reflections Resorts': { directBookingRevenue: 5442.16, newLeads: 66 },
  'Selah Place': { directBookingRevenue: 23096, newLeads: 700 },
  'Starlight Haven Hot Springs': { directBookingRevenue: 119716.12, newLeads: 1675 },
  'Starlight Haven Weiss Lake': { directBookingRevenue: 38401.12, newLeads: 817 },
  'Stay Saluda': { directBookingRevenue: 23074.5, newLeads: 626 },
  'Stay Southen Illinois': { directBookingRevenue: 19781.53, newLeads: 488 },
  'Stay on 30a': { directBookingRevenue: 511157.86, newLeads: 387 },
  'Stay with Branch': { directBookingRevenue: 2539, newLeads: 197 },
  'StayLuxe': { directBookingRevenue: 3801.96, newLeads: 80 },
  'Sunapee Stays': { directBookingRevenue: 73322.37, newLeads: 452 },
  'The Cohost Company': { directBookingRevenue: 67231.03, newLeads: 645 },
  'The Outpost': { directBookingRevenue: 30239.08, newLeads: 758 },
  'Three Suns Cabins': { directBookingRevenue: 15528.67, newLeads: 215 },
  'Treetop Escapes': { directBookingRevenue: 50028.46, newLeads: 3116 },
  'Tuxedo Falls': { directBookingRevenue: 104277, newLeads: 817 },
  'Tàberg Falls': { directBookingRevenue: 71085, newLeads: 7251 },
};
