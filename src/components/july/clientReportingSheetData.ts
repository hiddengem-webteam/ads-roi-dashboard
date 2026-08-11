// July 2026 figures from the "Client Performance Tracking" Google Sheet
// (each client tab's July 2026 row: "Direct Booking Revenue" + "🎉 New Leads").
// Used ONLY by /july-client-reporting-sheet — /july keeps computing revenue
// from the frozen snapshot. Keys are dashboard client names (snapshot keys),
// which differ from some sheet tab names (FLOHOM → Flohom, Stay With Branch →
// Stay with Branch, Dwell Luxury Rentals → Dwell, Stay Southern Illinois →
// Stay Southen Illinois).
// Source sheet: 1VnojM0GKQV7RpAvqmrU3WsEFCkA9bMqU5uOtNu4NZaY (verified with
// Shawal, Aug 11 2026).

export interface ClientReportingFigures {
  directBookingRevenue: number;
  newLeads: number;
}

export const CLIENT_REPORTING_SHEET: Record<string, ClientReportingFigures> = {
  'Asheville River Cabins': { directBookingRevenue: 143049.76, newLeads: 1034 },
  'Away2PA': { directBookingRevenue: 100747.01, newLeads: 1317 },
  'Awayframes': { directBookingRevenue: 34056.72, newLeads: 248 },
  'Best Texas Travel': { directBookingRevenue: 27623.94, newLeads: 136 },
  'Big Moon Ranch': { directBookingRevenue: 1852.1, newLeads: 279 },
  'Bison Ridge Retreat': { directBookingRevenue: 35208.46, newLeads: 1426 },
  'Dwell': { directBookingRevenue: 21056.87, newLeads: 43 },
  'Endless Stays': { directBookingRevenue: 30754.14, newLeads: 520 },
  'Evergreen Cabins': { directBookingRevenue: 49553.72, newLeads: 1973 },
  'Flohom': { directBookingRevenue: 106303.34, newLeads: 2903 },
  'Green Springs Inn': { directBookingRevenue: 26664.03, newLeads: 886 },
  'Hiawassee Glamping': { directBookingRevenue: 13000, newLeads: 294 },
  'Hillside Amble': { directBookingRevenue: 4057, newLeads: 54 },
  'Home Base': { directBookingRevenue: 129300.16, newLeads: 939 },
  'Inspired Retreats': { directBookingRevenue: 5163, newLeads: 149 },
  'Myrinn': { directBookingRevenue: 9011.7, newLeads: 264 },
  'Paradise Pointe': { directBookingRevenue: 100287, newLeads: 1114 },
  'Parker Reserve': { directBookingRevenue: 9906.96, newLeads: 82 },
  'Ponderosa Pines Resort': { directBookingRevenue: 35719.99, newLeads: 1470 },
  'Red White & Blue Views': { directBookingRevenue: 9240.76, newLeads: 254 },
  'Reflections Resorts': { directBookingRevenue: 5696.05, newLeads: 233 },
  'Selah Place': { directBookingRevenue: 20085, newLeads: 527 },
  'Starlight Haven Hot Springs': { directBookingRevenue: 123894.88, newLeads: 1669 },
  'Starlight Haven Weiss Lake': { directBookingRevenue: 54733.57, newLeads: 717 },
  'Stay Different': { directBookingRevenue: 2159.18, newLeads: 81 },
  'Stay on 30a': { directBookingRevenue: 478699.05, newLeads: 1129 },
  'Stay Saluda': { directBookingRevenue: 17371, newLeads: 346 },
  'Stay Southen Illinois': { directBookingRevenue: 6600.23, newLeads: 1116 },
  'Stay with Branch': { directBookingRevenue: 74512.66, newLeads: 181 },
  'StayLuxe': { directBookingRevenue: 12937.18, newLeads: 57 },
  'Sunapee Stays': { directBookingRevenue: 47958.84, newLeads: 603 },
  'The Cohost Company': { directBookingRevenue: 72305, newLeads: 496 },
  'The Outpost': { directBookingRevenue: 9760.55, newLeads: 308 },
  'Three Suns Cabins': { directBookingRevenue: 13488.66, newLeads: 337 },
  'Treetop Escapes': { directBookingRevenue: 44179, newLeads: 646 },
  'Tàberg Falls': { directBookingRevenue: 111170, newLeads: 5520 },
  'Wanderin Star Farms': { directBookingRevenue: 11266.85, newLeads: 83 },
};
