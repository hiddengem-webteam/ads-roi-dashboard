// October 2026 figures from the "Client Performance Tracking" Google Sheet
// (each client tab's October 2026 row: "Direct Booking Revenue" + "🎉 New
// Leads"). A zero revenue here means the sheet's revenue cell wasn't filled —
// the page falls back to the dashboard value for revenue while still using the
// sheet's lead count. Pulled Nov 2 2026 (DRAFT: AMs were still filling the
// October rows; New Leads entered for only five clients so far — a zero lead
// count below means "not entered yet", not zero leads).
// Glasscombe's sheet revenue is in GBP (£5,291.87) and is left out until the
// currency rule is decided; the dashboard shows the AM tab's USD figure.
import type { ClientReportingFigures } from '@/components/september/septemberReportingSheetData';

export const OCTOBER_REPORTING_SHEET: Record<string, ClientReportingFigures> = {
  'American River Resort': { directBookingRevenue: 102665, newLeads: 353 },
  'Asheville River Cabins': { directBookingRevenue: 130942, newLeads: 0 },
  'Best Texas Travel': { directBookingRevenue: 13549, newLeads: 0 },
  'Bison Ridge Retreat': { directBookingRevenue: 7428, newLeads: 215 },
  'Cabin Collective': { directBookingRevenue: 14628, newLeads: 0 },
  'Columbia Gorge Getaways': { directBookingRevenue: 32145, newLeads: 196 },
  'Endless Stays': { directBookingRevenue: 37828, newLeads: 0 },
  'Evergreen Cabins': { directBookingRevenue: 40089, newLeads: 0 },
  'Home Base': { directBookingRevenue: 152039.65, newLeads: 0 },
  'Myrinn': { directBookingRevenue: 9560, newLeads: 0 },
  'North Star Lodge & Resort': { directBookingRevenue: 67013.95, newLeads: 0 },
  'Oak & Ember': { directBookingRevenue: 35670, newLeads: 1236 },
  'Red White & Blue Views': { directBookingRevenue: 15951, newLeads: 0 },
  'Starlight Haven Hot Springs': { directBookingRevenue: 137528.39, newLeads: 0 },
  'Starlight Haven Weiss Lake': { directBookingRevenue: 48161, newLeads: 0 },
  'Stay Southen Illinois': { directBookingRevenue: 15890, newLeads: 0 },
  'Stay on 30a': { directBookingRevenue: 325979.29, newLeads: 0 },
  'Stay with Branch': { directBookingRevenue: 5169, newLeads: 0 },
  'StayLuxe': { directBookingRevenue: 0, newLeads: 0 },
  'Sunapee Stays': { directBookingRevenue: 35204, newLeads: 0 },
  'The Outpost': { directBookingRevenue: 25755, newLeads: 0 },
  'Tuxedo Falls': { directBookingRevenue: 48086, newLeads: 958 },
};
