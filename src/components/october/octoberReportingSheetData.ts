// October 2026 figures from the "Client Performance Tracking" Google Sheet
// (each client tab's October 2026 row: "Direct Booking Revenue" + "🎉 New
// Leads"). A zero revenue here means the sheet's revenue cell wasn't filled —
// the page falls back to the dashboard value for revenue while still using the
// sheet's lead count. Pulled Nov 3 2026: every client tab has its October
// revenue and 38 have New Leads. Four tabs have no New Leads column at all
// (Starlight Haven Weiss Lake, Home Base, Stay on 30a, Stay with Branch —
// retargeting-only clients), so their lead count is 0 and the card stays blank.
// Glasscombe's sheet revenue is in GBP (£5,291.87) and is left out, as in
// previous months; the dashboard shows the AM tab's USD figure, the lead count
// is the sheet's. StayLuxe had no direct bookings in October (per Kristal).
import type { ClientReportingFigures } from '@/components/september/septemberReportingSheetData';

export const OCTOBER_REPORTING_SHEET: Record<string, ClientReportingFigures> = {
  'American River Resort': { directBookingRevenue: 102665, newLeads: 353 },
  'Asheville River Cabins': { directBookingRevenue: 130942, newLeads: 1595 },
  'Away2PA': { directBookingRevenue: 120501, newLeads: 1098 },
  'Awayframes': { directBookingRevenue: 18718, newLeads: 477 },
  'Best Texas Travel': { directBookingRevenue: 13549, newLeads: 212 },
  'Bison Ridge Retreat': { directBookingRevenue: 7428, newLeads: 215 },
  'Cabin Collective': { directBookingRevenue: 14628, newLeads: 68 },
  'Columbia Gorge Getaways': { directBookingRevenue: 32145, newLeads: 196 },
  'Endless Stays': { directBookingRevenue: 37828, newLeads: 2097 },
  'Evergreen Cabins': { directBookingRevenue: 40089, newLeads: 2016 },
  'Flohom': { directBookingRevenue: 122751, newLeads: 1014 },
  'Glasscombe': { directBookingRevenue: 0, newLeads: 85 },
  'Green Springs Inn': { directBookingRevenue: 37513, newLeads: 397 },
  'Hiawassee Glamping': { directBookingRevenue: 19270, newLeads: 565 },
  'Home Base': { directBookingRevenue: 152039.65, newLeads: 0 },
  'Inspired Retreats': { directBookingRevenue: 34871, newLeads: 553 },
  'Little River Landing': { directBookingRevenue: 3332, newLeads: 176 },
  'Myrinn': { directBookingRevenue: 9560, newLeads: 346 },
  'Nature Nooks': { directBookingRevenue: 2273, newLeads: 345 },
  'North Star Lodge & Resort': { directBookingRevenue: 67013.95, newLeads: 150 },
  'Oak & Ember': { directBookingRevenue: 35670, newLeads: 1236 },
  'Paradise Pointe': { directBookingRevenue: 133353, newLeads: 1762 },
  'Parker Reserve': { directBookingRevenue: 6954, newLeads: 95 },
  'Ponderosa Pines Resort': { directBookingRevenue: 44698, newLeads: 1351 },
  'Red White & Blue Views': { directBookingRevenue: 15951, newLeads: 380 },
  'Ridge & Falls': { directBookingRevenue: 4834, newLeads: 399 },
  'Selah Place': { directBookingRevenue: 22460, newLeads: 685 },
  'Starlight Haven Hot Springs': { directBookingRevenue: 137528.39, newLeads: 1762 },
  'Starlight Haven Weiss Lake': { directBookingRevenue: 48161, newLeads: 0 },
  'Stay on 30a': { directBookingRevenue: 325979.29, newLeads: 0 },
  'Stay Saluda': { directBookingRevenue: 18656, newLeads: 920 },
  'Stay Southen Illinois': { directBookingRevenue: 15890, newLeads: 376 },
  'Stay with Branch': { directBookingRevenue: 5169, newLeads: 0 },
  'StayLuxe': { directBookingRevenue: 0, newLeads: 85 },
  'Sunapee Stays': { directBookingRevenue: 35204, newLeads: 304 },
  'The Cohost Company': { directBookingRevenue: 60252, newLeads: 635 },
  'The Outpost': { directBookingRevenue: 25755, newLeads: 249 },
  'Three Suns Cabins': { directBookingRevenue: 15366, newLeads: 166 },
  'Treetop Escapes': { directBookingRevenue: 42401, newLeads: 2425 },
  'Tuxedo Falls': { directBookingRevenue: 48086, newLeads: 958 },
  'Tàberg Falls': { directBookingRevenue: 48795, newLeads: 4335 },
  'Walden Retreats': { directBookingRevenue: 80000, newLeads: 339 },
};
