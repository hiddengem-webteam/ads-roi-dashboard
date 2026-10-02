// September 2026 figures from the "Client Performance Tracking" Google Sheet
// (each client tab's September 2026 row: "Direct Booking Revenue" + "🎉 New
// Leads"). Used ONLY by /september. A zero revenue here means the sheet's
// revenue cell wasn't filled — the page falls back to the dashboard value
// for revenue while still using the sheet's lead count. Pulled Oct 2 2026.
export interface ClientReportingFigures {
  directBookingRevenue: number;
  newLeads: number;
}

export const SEPTEMBER_REPORTING_SHEET: Record<string, ClientReportingFigures> = {
  'American River Resort': { directBookingRevenue: 151552.08, newLeads: 826 },
  'Asheville River Cabins': { directBookingRevenue: 138183.02, newLeads: 1502 },
  'Away2PA': { directBookingRevenue: 121483.87, newLeads: 1258 },
  'Awayframes': { directBookingRevenue: 17492.76, newLeads: 235 },
  'Best Texas Travel': { directBookingRevenue: 9823.91, newLeads: 206 },
  'Bison Ridge Retreat': { directBookingRevenue: 23655.74, newLeads: 398 },
  'Columbia Gorge Getaways': { directBookingRevenue: 21072.78, newLeads: 271 },
  'Endless Stays': { directBookingRevenue: 25675.5, newLeads: 630 },
  'Evergreen Cabins': { directBookingRevenue: 42384.49, newLeads: 2782 },
  'Flohom': { directBookingRevenue: 0, newLeads: 2660 },
  'Green Springs Inn': { directBookingRevenue: 33499.23, newLeads: 376 },
  'Hiawassee Glamping': { directBookingRevenue: 14390, newLeads: 736 },
  'Home Base': { directBookingRevenue: 62759.8, newLeads: 386 },
  'Inspired Retreats': { directBookingRevenue: 51165.6, newLeads: 641 },
  'Myrinn': { directBookingRevenue: 15984.92, newLeads: 352 },
  'Nature Nooks': { directBookingRevenue: 0, newLeads: 444 },
  'North Star Lodge & Resort': { directBookingRevenue: 6000, newLeads: 500 },
  'Oak & Ember': { directBookingRevenue: 16995.59, newLeads: 557 },
  'Paradise Pointe': { directBookingRevenue: 135788.51, newLeads: 2458 },
  'Parker Reserve': { directBookingRevenue: 9416.54, newLeads: 100 },
  'Ponderosa Pines Resort': { directBookingRevenue: 59336, newLeads: 2060 },
  'Red White & Blue Views': { directBookingRevenue: 9467.37, newLeads: 409 },
  'Selah Place': { directBookingRevenue: 21123.75, newLeads: 617 },
  'Starlight Haven Hot Springs': { directBookingRevenue: 121636.87, newLeads: 1841 },
  'Starlight Haven Weiss Lake': { directBookingRevenue: 49377.94, newLeads: 783 },
  'Stay Saluda': { directBookingRevenue: 20881.71, newLeads: 917 },
  'Stay Southen Illinois': { directBookingRevenue: 16714.29, newLeads: 463 },
  'Stay on 30a': { directBookingRevenue: 429436.69, newLeads: 1380 },
  'Stay with Branch': { directBookingRevenue: 1169, newLeads: 293 },
  'StayLuxe': { directBookingRevenue: 0, newLeads: 56 },
  'Sunapee Stays': { directBookingRevenue: 39757.41, newLeads: 315 },
  'The Cohost Company': { directBookingRevenue: 93512.1, newLeads: 591 },
  'The Outpost': { directBookingRevenue: 34759, newLeads: 277 },
  'Three Suns Cabins': { directBookingRevenue: 16317.55, newLeads: 221 },
  'Treetop Escapes': { directBookingRevenue: 33156.3, newLeads: 2714 },
  'Tuxedo Falls': { directBookingRevenue: 35190, newLeads: 466 },
  'Tàberg Falls': { directBookingRevenue: 60818.75, newLeads: 5616 },
};
