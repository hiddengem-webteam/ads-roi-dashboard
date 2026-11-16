// Account manager per client, as the dashboard shows and filters it (sidebar and Overview).
//
// Base list: whose July 2026 direct-booking spreadsheet each client's data came from (every client
// appears in exactly one AM's file). Added 2026-11-16 for clients that list was missing: the Master
// Meta Ads sheet's AM column (weekly ad spend check, 9 Nov 2026), and North Star Lodge & Resort from
// the CRM via the 9 Nov client benchmark. Nature Nooks and Stay with Branch (Kristal) and The Outpost
// (Ananya) follow the Master sheet since 2026-11-16 (Shawal); the CRM still listed The Outpost under Anna.
export const ACCOUNT_MANAGERS: Record<string, string> = {
  'Three Suns Cabins': 'Anna',
  'Stay Different': 'Anna',
  'The Outpost': 'Ananya',
  'Ponderosa Pines Resort': 'Anna',
  'Bison Ridge Retreat': 'Chiara',
  'Stay Southern Illinois': 'Chiara',
  'Hillside Amble': 'Chiara',
  'Paradise Pointe': 'Makenna',
  'Treetop Escapes': 'Makenna',
  'Stay Saluda': 'Makenna',
  'Inspired Retreats': 'Makenna',
  'Flohom': 'Makenna',
  'The Cohost Company': 'Makenna',
  'Stay with Branch': 'Kristal',
  'Asheville River Cabins': 'Charlotte',
  'Myrinn': 'Charlotte',
  'Home Base': 'Charlotte',
  'Stay on 30a': 'Charlotte',
  'Big Moon Ranch': 'Charlotte',
  'Sunapee Stays': 'Charlotte',
  'Dwell': 'Charlotte',
  'Starlight Haven Hot Springs': 'Charlotte',
  'Starlight Haven Weiss Lake': 'Charlotte',
  'Nature Nooks': 'Kristal',
  'Wanderin Star Farms': 'Alicia',
  'Hiawassee Glamping': 'Alicia',
  'Awayframes': 'Alicia',
  'Tàberg Falls': 'Alicia',
  'Reflections Resorts': 'Alicia',
  'Selah Place': 'Alicia',
  'Green Springs Inn': 'Alicia',
  'Away2PA': 'Alicia',
  'American River Resort': 'Nicole',
  'Evergreen Cabins': 'Nicole',
  'Parker Reserve': 'Nicole',
  'StayLuxe': 'Nicole',
  'Endless Stays': 'Nicole',
  'Red White & Blue Views': 'Nicole',
  'Best Texas Travel': 'Nicole',
  // Filled 2026-11-16 (Master Meta Ads sheet, 9 Nov; North Star from the CRM)
  'Cabin Collective': 'Chiara',
  'Columbia Gorge Getaways': 'Chiara',
  'Glasscombe': 'Charlotte',
  'Little River Landing': 'Makenna',
  'North Star Lodge & Resort': 'Charlotte',
  'Oak & Ember': 'Chiara',
  'Ridge & Falls': 'Makenna',
  'Tuxedo Falls': 'Chiara',
  'Walden Retreats': 'Anna',
};

/** Filter value for clients with no AM in the list. */
export const NO_AM = '__none';

export function accountManagerFor(client: string): string | undefined {
  return ACCOUNT_MANAGERS[client];
}

/** Does a client pass the AM filter ('' = everyone, NO_AM = clients with no AM listed)? */
export function matchesAm(client: string, am: string): boolean {
  if (!am) return true;
  const a = ACCOUNT_MANAGERS[client];
  return am === NO_AM ? !a : a === am;
}
