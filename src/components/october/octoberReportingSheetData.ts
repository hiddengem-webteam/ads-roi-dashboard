// October 2026 figures from the "Client Performance Tracking" Google Sheet
// (each client tab's October 2026 row: "Direct Booking Revenue" + "🎉 New
// Leads"). A zero revenue here means the sheet's revenue cell wasn't filled —
// the page falls back to the dashboard value for revenue while still using the
// sheet's lead count. Pulled Nov 3 2026: every client tab now has its October
// revenue; New Leads is entered for 17 clients — a zero lead count below means
// "not entered yet", not zero leads (the Total Leads card stays blank).
// Glasscombe's sheet revenue is in GBP (£5,291.87) and is left out, as in
// previous months; the dashboard shows the AM tab's USD figure.
// StayLuxe had no direct bookings in October (confirmed by Kristal).
import type { ClientReportingFigures } from '@/components/september/septemberReportingSheetData';

export const OCTOBER_REPORTING_SHEET: Record<string, ClientReportingFigures> = {
  'American River Resort': { directBookingRevenue: 102665, newLeads: 353 },
  'Asheville River Cabins': { directBookingRevenue: 130942, newLeads: 0 },
  'Away2PA': { directBookingRevenue: 120501, newLeads: 0 },
  'Awayframes': { directBookingRevenue: 18718, newLeads: 477 },
  'Best Texas Travel': { directBookingRevenue: 13549, newLeads: 0 },
  'Bison Ridge Retreat': { directBookingRevenue: 7428, newLeads: 215 },
  'Cabin Collective': { directBookingRevenue: 14628, newLeads: 0 },
  'Columbia Gorge Getaways': { directBookingRevenue: 32145, newLeads: 196 },
  'Endless Stays': { directBookingRevenue: 37828, newLeads: 0 },
  'Evergreen Cabins': { directBookingRevenue: 40089, newLeads: 0 },
  'Flohom': { directBookingRevenue: 122751, newLeads: 1014 },
  'Green Springs Inn': { directBookingRevenue: 37513, newLeads: 0 },
  'Hiawassee Glamping': { directBookingRevenue: 19270, newLeads: 0 },
  'Home Base': { directBookingRevenue: 152039.65, newLeads: 0 },
  'Inspired Retreats': { directBookingRevenue: 34871, newLeads: 553 },
  'Little River Landing': { directBookingRevenue: 3332, newLeads: 176 },
  'Myrinn': { directBookingRevenue: 9560, newLeads: 0 },
  'Nature Nooks': { directBookingRevenue: 2273, newLeads: 345 },
  'North Star Lodge & Resort': { directBookingRevenue: 67013.95, newLeads: 0 },
  'Oak & Ember': { directBookingRevenue: 35670, newLeads: 1236 },
  'Paradise Pointe': { directBookingRevenue: 133353, newLeads: 1762 },
  'Parker Reserve': { directBookingRevenue: 6954, newLeads: 95 },
  'Ponderosa Pines Resort': { directBookingRevenue: 44698, newLeads: 0 },
  'Red White & Blue Views': { directBookingRevenue: 15951, newLeads: 0 },
  'Ridge & Falls': { directBookingRevenue: 4834, newLeads: 399 },
  'Selah Place': { directBookingRevenue: 22460, newLeads: 0 },
  'Starlight Haven Hot Springs': { directBookingRevenue: 137528.39, newLeads: 0 },
  'Starlight Haven Weiss Lake': { directBookingRevenue: 48161, newLeads: 0 },
  'Stay Saluda': { directBookingRevenue: 18656, newLeads: 920 },
  'Stay Southen Illinois': { directBookingRevenue: 15890, newLeads: 0 },
  'Stay on 30a': { directBookingRevenue: 325979.29, newLeads: 0 },
  'Stay with Branch': { directBookingRevenue: 5169, newLeads: 0 },
  'StayLuxe': { directBookingRevenue: 0, newLeads: 0 },
  'Sunapee Stays': { directBookingRevenue: 35204, newLeads: 0 },
  'The Cohost Company': { directBookingRevenue: 60252, newLeads: 635 },
  'The Outpost': { directBookingRevenue: 25755, newLeads: 0 },
  'Three Suns Cabins': { directBookingRevenue: 15366, newLeads: 0 },
  'Treetop Escapes': { directBookingRevenue: 42401, newLeads: 2425 },
  'Tuxedo Falls': { directBookingRevenue: 48086, newLeads: 958 },
  'Tàberg Falls': { directBookingRevenue: 48795, newLeads: 4335 },
  'Walden Retreats': { directBookingRevenue: 80000, newLeads: 0 },
};
