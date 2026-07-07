// Maps Facebook ad account names to canonical client names used in ROI sheet / promo codes

export const ACCOUNT_NAME_MAP: Record<string, string> = {
  'Starlight Haven Weiss Lake - 74756899': 'Starlight Haven Weiss Lake',
  'Starlight Haven Weiss Lake- 74756899': 'Starlight Haven Weiss Lake',
  'Hillside Amble Ads': 'Hillside Amble',
  'Inspired Retreats Ads 2.0': 'Inspired Retreats',
  'Inspired Retreats Ads': 'Inspired Retreats',
  '@staywithbranch': 'Stay With Branch',
  'Stay Different Ads': 'Stay Different',
  'Nature Nooks Ad Account': 'Nature Nooks',
  'Edenwood NC ': 'Edenwood NC',
  'Edenwood NC': 'Edenwood NC',
  'FLOHOM Ads': 'FLOHOM',
  'Branch Berkeley Springs': 'Stay With Branch',
  'The Cohost Company Ads': 'The Cohost Company',
  'Myrinn - Ad Account 2.0': 'Myrinn',
  'Pine Valley Cabins Georgia Ad Account': 'Pine Valley Cabins Georgia',
  'Treetop Escapes Ads': 'Treetop Escapes',
  'Stay on 30a Ads': 'Stay on 30a',
  'Roundhouse Residences Ads': 'Roundhouse Residences',
  'Asheville River Cabins Ads': 'Asheville River Cabins',
  'Stay Saluda Ads': 'Stay Saluda',
  'Wanderin Star Farms New Ad Account': 'Wanderin Star Farms',
  'Reflections Resort Ad': 'Reflections Resort',
  'Reflections Resort Ads': 'Reflections Resort',
  'Red White & Blue Views': 'Red White & Blue Views',
  'Home Base bnbs': 'Home Base BNBs',
  'Away2Pa': 'Away2PA',
  'Paradise Pointe Ads': 'Paradise Pointe',
  'Green Springs Inn': 'Green Springs Inn',
  'Hiawassee Glamping': 'Hiawassee Glamping',
  'Big Moon Ranch': 'Big Moon Ranch',
  'Endless Stays': 'Endless Stays',
  // Added for May 2026
  'Awayframes Ad Account': 'Awayframes',
  'Bison Ridge Retreat Ad Account': 'Bison Ridge Retreat',
  'Dwell Luxury Rentals Ads': 'Dwell Luxury Rentals',
  'Evergreen Cabins Ads': 'Evergreen Cabins',
  'Parker Reserve': 'Parker Reserve',
  'Stay Luxe Ads': 'Stay Luxe',
  'Three Suns Cabins Ad Account': 'Three Suns Cabins',
  'Táberg Falls': 'Táberg Falls',
  'Southern Illinois Cabins Ads': 'Southern Illinois Cabins',
  'The Outpost Grand Canyon': 'The Outpost Grand Canyon',
  'VillaDestinoItaly': 'VillaDestinoItaly',
  'Rock Ridge Resort': 'Rock Ridge Resort',
  'CGG': 'CGG',
  'Out of Bounds Retreats': 'Out of Bounds Retreats',
  'Selah.place': 'Selah.place',
  'Starlight Haven Hot Springs': 'Starlight Haven Hot Springs',
  'Starlight Haven Weiss Lake': 'Starlight Haven Weiss Lake',
  'Away2PA Direct': 'Away2PA',
};

export function resolveClientName(accountName: string): string {
  const trimmed = accountName.trim();
  if (ACCOUNT_NAME_MAP[trimmed]) return ACCOUNT_NAME_MAP[trimmed];
  // Try trimmed version (trailing spaces)
  for (const [key, value] of Object.entries(ACCOUNT_NAME_MAP)) {
    if (key.trim().toLowerCase() === trimmed.toLowerCase()) return value;
  }
  return trimmed;
}

// Platform / relay emails to exclude from matching
export const PLATFORM_EMAIL_PATTERNS = [
  'privaterelay.appleid.com',
  'hipcamp.com',
  'relay.firefox.com',
  'noreply.',
  'support@',
  'admin@',
  'info@booking',
  'guest@',
  'noreply@',
];

export function isPlatformEmail(email: string): boolean {
  if (!email) return false;
  const lower = email.toLowerCase();
  return PLATFORM_EMAIL_PATTERNS.some((p) => lower.includes(p));
}
