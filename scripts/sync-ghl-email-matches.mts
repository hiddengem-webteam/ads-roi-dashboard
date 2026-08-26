// Ads vs Organic email-match analysis — matches every PMS booking email
// against the client's GHL contacts (live API) and classifies matches with
// HYBRID logic (per Shawal, Aug 2026):
//
//   1. surviving lead tag wins:  "meta ads lead" → Ads,
//      "instagram lead"/"facebook lead" → Organic
//   2. otherwise the contact's attribution decides (GHL wipes lead tags when
//      a contact books — confirmed across Flohom/Treetop/GSI/Evergreen —
//      but attributionSource survives):
//        utm_source contains "meta" or session "Paid Social"  → Ads
//        utm_source "ig" or instagram referrer                → Organic (IG)
//        utm_source contains "facebook" or facebook referrer  → Organic (FB)
//
// A match only counts if the contact existed before the booking's check-in
// (a contact created after the stay can't be its lead). Contacts created by
// the booking itself (Zapier/PMS imports) carry no lead attribution and fall
// out naturally.
//
// Lookups are cached in data/.ghl-contact-cache.json (gitignored, 24h TTL) so
// the 4-hourly runs only re-query new emails. Output goes to
// public/data/ghl-email-matches.json — NOT committed (guest emails); Netlify
// builds regenerate it via prebuild using GHL_CREDENTIALS_JSON.
//
// Usage: npx tsx scripts/sync-ghl-email-matches.mts

import fs from 'fs';
import path from 'path';

const ROOT = path.resolve(import.meta.dirname, '..');
const CACHE_PATH = path.join(ROOT, 'data', '.ghl-contact-cache.json');
const CACHE_TTL_MS = 24 * 60 * 60 * 1000;
const CONCURRENCY = 6;

const NAME_ALIASES: Record<string, string> = {
  'Stay Saluda NC': 'Stay Saluda',
  'Stay Southern Illinois': 'Stay Southen Illinois',
  "Wanderin' Star Farms": 'Wanderin Star Farms',
};
const SKIP_CLIENTS = new Set(['HiddenGem Test']);

interface Cred { clientName: string; apiKey: string; locationId: string }
interface CachedContact {
  t: number; // fetchedAt epoch ms
  found: boolean;
  tags?: string[];
  dateAdded?: string;
  attr?: { utmSource?: string; sessionSource?: string; referrer?: string };
  lastAttr?: { utmSource?: string; sessionSource?: string; referrer?: string };
}
interface Booking { guest: string; email: string; revenue: number; checkIn: string }
interface MatchRow { guest: string; email: string; bookings: number; revenue: number; via: string; source?: 'instagram' | 'facebook' }

const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));

function loadCreds(): Cred[] | null {
  const localPath = path.join(ROOT, 'ghl-credentials.local.json');
  if (fs.existsSync(localPath)) return Object.values(JSON.parse(fs.readFileSync(localPath, 'utf8')));
  if (process.env.GHL_CREDENTIALS_JSON) return Object.values(JSON.parse(process.env.GHL_CREDENTIALS_JSON));
  return null;
}

function hostnameOf(url: string | undefined): string {
  if (!url) return '';
  try { return new URL(url).hostname.toLowerCase(); } catch { return String(url).toLowerCase(); }
}

async function fetchContact(cred: Cred, email: string): Promise<CachedContact> {
  for (let attempt = 1; attempt <= 3; attempt++) {
    try {
      const res = await fetch('https://services.leadconnectorhq.com/contacts/search', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${cred.apiKey}`,
          Version: '2021-07-28',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          locationId: cred.locationId,
          pageLimit: 1,
          filters: [{ field: 'email', operator: 'eq', value: email }],
        }),
      });
      if (res.status === 429) { await sleep(1500 * attempt); continue; }
      if (!res.ok) throw new Error(`${res.status}`);
      const c = ((await res.json()) as { contacts?: Record<string, unknown>[] }).contacts?.[0];
      if (!c) return { t: Date.now(), found: false };
      const pick = (o: unknown) => {
        const a = (o ?? {}) as Record<string, string | undefined>;
        return { utmSource: a.utmSource, sessionSource: a.sessionSource, referrer: a.referrer };
      };
      return {
        t: Date.now(),
        found: true,
        tags: (c.tags as string[]) ?? [],
        dateAdded: (c.dateAdded as string) ?? undefined,
        attr: pick(c.attributionSource),
        lastAttr: pick(c.lastAttributionSource),
      };
    } catch {
      await sleep(400 * attempt);
    }
  }
  // treat as transient miss; short cache so it retries soon
  return { t: Date.now() - CACHE_TTL_MS + 60 * 60 * 1000, found: false };
}

// Hybrid classification: lead tag first, then attribution.
function classify(c: CachedContact): { bucket: 'ads' | 'ig' | 'fb' | null; via: string } {
  const tags = c.tags ?? [];
  if (tags.includes('meta ads lead')) return { bucket: 'ads', via: 'tag: meta ads lead' };
  if (tags.includes('instagram lead')) return { bucket: 'ig', via: 'tag: instagram lead' };
  if (tags.includes('facebook lead')) return { bucket: 'fb', via: 'tag: facebook lead' };
  for (const [label, a] of [['attribution', c.attr], ['last attribution', c.lastAttr]] as const) {
    if (!a) continue;
    const utm = (a.utmSource ?? '').toLowerCase();
    const session = a.sessionSource ?? '';
    const ref = hostnameOf(a.referrer);
    if (utm.includes('meta') || session === 'Paid Social') return { bucket: 'ads', via: `${label}: ${utm.includes('meta') ? 'utm meta' : 'paid social'}` };
    if (utm === 'ig' || ref.includes('instagram')) return { bucket: 'ig', via: `${label}: ${utm === 'ig' ? 'utm ig' : 'instagram referrer'}` };
    if (utm.includes('facebook') || ref.includes('facebook')) return { bucket: 'fb', via: `${label}: ${utm.includes('facebook') ? 'utm facebook' : 'facebook referrer'}` };
  }
  return { bucket: null, via: '' };
}

function readBookings(periodId: string, clientDir: string): Booking[] {
  const f = path.join(ROOT, 'public', 'data', 'periods', periodId, 'clients', clientDir, 'PMS data.csv');
  if (!fs.existsSync(f)) return [];
  const lines = fs.readFileSync(f, 'utf8').trim().split('\n');
  return lines.slice(1).map((l) => {
    const c = l.split(',');
    return { guest: c[0] ?? '', email: (c[1] ?? '').toLowerCase().trim(), revenue: Number(c[2] ?? 0), checkIn: c[3] ?? '' };
  }).filter((b) => b.email.includes('@'));
}

async function mapPool<T, R>(items: T[], n: number, fn: (item: T) => Promise<R>): Promise<R[]> {
  const out: R[] = new Array(items.length);
  let idx = 0;
  await Promise.all(Array.from({ length: Math.min(n, items.length) }, async () => {
    while (idx < items.length) {
      const i = idx++;
      out[i] = await fn(items[i]);
    }
  }));
  return out;
}

async function main() {
  const creds = loadCreds();
  if (!creds) {
    console.warn('No GHL credentials — skipping email-match sync.');
    return;
  }
  const manifest = JSON.parse(fs.readFileSync(path.join(ROOT, 'public', 'data', 'manifest.json'), 'utf8'));
  const periods: string[] = manifest.periods.map((p: { id: string }) => p.id);

  const cache: Record<string, Record<string, CachedContact>> = fs.existsSync(CACHE_PATH)
    ? JSON.parse(fs.readFileSync(CACHE_PATH, 'utf8'))
    : {};

  const norm = (s: string) => s.toLowerCase().replace(/[^a-z0-9]/g, '');
  const manifestNames = new Map<string, string>();
  for (const p of manifest.periods) for (const c of p.clients) manifestNames.set(norm(c.name), c.name);

  const out: {
    generatedAt: string;
    logic: string;
    periods: Record<string, Record<string, unknown>>;
  } = {
    generatedAt: new Date().toISOString(),
    logic: 'hybrid: surviving GHL lead tag first, then attributionSource (utm/session/referrer); contact must predate check-in',
    periods: {},
  };
  for (const id of periods) out.periods[id] = {};

  for (const cred of creds) {
    if (SKIP_CLIENTS.has(cred.clientName)) continue;
    const displayName = NAME_ALIASES[cred.clientName] ?? manifestNames.get(norm(cred.clientName)) ?? cred.clientName;
    const locCache = (cache[cred.locationId] = cache[cred.locationId] ?? {});
    process.stdout.write(`${displayName} ... `);
    let queried = 0;

    for (const periodId of periods) {
      const bookings = readBookings(periodId, displayName);
      if (bookings.length === 0) continue;

      // group bookings per unique email
      const byEmail = new Map<string, Booking[]>();
      for (const b of bookings) {
        if (!byEmail.has(b.email)) byEmail.set(b.email, []);
        byEmail.get(b.email)!.push(b);
      }

      const emails = [...byEmail.keys()];
      await mapPool(emails, CONCURRENCY, async (email) => {
        const hit = locCache[email];
        if (hit && Date.now() - hit.t < CACHE_TTL_MS) return;
        locCache[email] = await fetchContact(cred, email);
        queried++;
        await sleep(30);
      });

      const ads: MatchRow[] = [];
      const organic: MatchRow[] = [];
      for (const [email, bks] of byEmail) {
        const c = locCache[email];
        if (!c?.found) continue;
        // direction: contact must exist before the earliest check-in (when both known)
        const firstCheckIn = bks.map((b) => b.checkIn).filter(Boolean).sort()[0];
        if (firstCheckIn && c.dateAdded && c.dateAdded.slice(0, 10) > firstCheckIn) continue;
        const { bucket, via } = classify(c);
        if (!bucket) continue;
        const row: MatchRow = {
          guest: bks[0].guest,
          email,
          bookings: bks.length,
          revenue: Math.round(bks.reduce((s, b) => s + b.revenue, 0) * 100) / 100,
          via,
        };
        if (bucket === 'ads') ads.push(row);
        else organic.push({ ...row, source: bucket === 'ig' ? 'instagram' : 'facebook' });
      }
      ads.sort((a, b) => b.revenue - a.revenue);
      organic.sort((a, b) => b.revenue - a.revenue);

      const sum = (rows: MatchRow[], k: 'bookings' | 'revenue') => Math.round(rows.reduce((s, r) => s + r[k], 0) * 100) / 100;
      if (ads.length || organic.length) {
        out.periods[periodId][displayName] = {
          ads: { matchedEmails: ads.length, bookings: sum(ads, 'bookings'), revenue: sum(ads, 'revenue'), matches: ads },
          organic: {
            matchedEmails: organic.length,
            bookings: sum(organic, 'bookings'),
            revenue: sum(organic, 'revenue'),
            instagram: organic.filter((r) => r.source === 'instagram').length,
            facebook: organic.filter((r) => r.source === 'facebook').length,
            matches: organic,
          },
        };
      }
    }
    console.log(`done (${queried} lookups)`);
    fs.writeFileSync(CACHE_PATH, JSON.stringify(cache), 'utf8'); // checkpoint per client
  }

  const outPath = path.join(ROOT, 'public', 'data', 'ghl-email-matches.json');
  fs.writeFileSync(outPath, JSON.stringify(out, null, 2), 'utf8');
  console.log(`\nWrote ${outPath}`);
}

main().catch((err) => {
  console.error('GHL email-match sync failed (non-fatal):', err);
});
