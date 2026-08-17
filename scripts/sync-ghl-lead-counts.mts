// Pulls per-month lead counts straight from the GHL API for the three
// standard lead tags, per client, and stores them for the dashboard:
//
//   meta ads lead  — leads from Meta lead ads
//   instagram lead — IG bio clicks / organic IG traffic
//   facebook lead  — FB bio clicks / organic FB traffic
//
// Counts come from POST /contacts/search with a tag filter + dateAdded range
// (pageLimit 1; only the `total` is read, so this is fast and cheap — no
// contact data is stored). Date windows use US Eastern offsets to match how
// the GHL UI displays "Created" times. NOTE: never use GHL's UI "In month"
// smart-list filter as a reference — it matches that month in ANY year.
//
// Credentials come from ghl-credentials.local.json (gitignored; local dev) or
// the GHL_CREDENTIALS_JSON env var (Netlify builds — scope it to Builds).
// With neither present the script SKIPS quietly (exit 0) so environments
// without GHL access still build; the last committed counts file keeps
// serving. Output goes to public/data/ghl-lead-counts.json, which IS
// committed/deployed — it holds only aggregate counts, no contact data.
//
// Runs locally via `npm run sync:ghl` and on every production build via
// `prebuild`, which the 4-hourly scheduled rebuild re-triggers — so deployed
// GHL numbers refresh on the same cadence as the platform data.
//
// Usage: npx tsx scripts/sync-ghl-lead-counts.mts

import fs from 'fs';
import path from 'path';

const ROOT = path.resolve(import.meta.dirname, '..');

const TAGS = ['meta ads lead', 'instagram lead', 'facebook lead'] as const;

// Credential clientName → dashboard/manifest client name, for the few that
// don't match by loose normalization.
const NAME_ALIASES: Record<string, string> = {
  'Stay Saluda NC': 'Stay Saluda',
  'Stay Southern Illinois': 'Stay Southen Illinois',
  "Wanderin' Star Farms": 'Wanderin Star Farms',
};
const SKIP_CLIENTS = new Set(['HiddenGem Test']);

interface Cred { clientName: string; apiKey: string; locationId: string }

const MONTHS: Record<string, number> = {
  january: 1, february: 2, march: 3, april: 4, may: 5, june: 6,
  july: 7, august: 8, september: 9, october: 10, november: 11, december: 12,
};

// US Eastern offset per month (2026 DST: mid-March through Oct is EDT/-4).
function easternOffset(month: number): string {
  return month >= 4 && month <= 10 ? '-04:00' : '-05:00';
}

function monthWindow(periodId: string): { gte: string; lt: string } | null {
  const m = periodId.match(/^([a-z]+)-(\d{4})$/);
  if (!m || !(m[1] in MONTHS)) return null;
  const month = MONTHS[m[1]];
  const year = Number(m[2]);
  const nextMonth = month === 12 ? 1 : month + 1;
  const nextYear = month === 12 ? year + 1 : year;
  const pad = (n: number) => String(n).padStart(2, '0');
  return {
    gte: `${year}-${pad(month)}-01T00:00:00.000${easternOffset(month)}`,
    lt: `${nextYear}-${pad(nextMonth)}-01T00:00:00.000${easternOffset(nextMonth)}`,
  };
}

const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));

async function tagCount(cred: Cred, tag: string, window: { gte: string; lt: string }): Promise<number | null> {
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
          filters: [
            { field: 'tags', operator: 'eq', value: [tag] },
            { field: 'dateAdded', operator: 'range', value: window },
          ],
        }),
      });
      if (res.status === 429) { await sleep(1500 * attempt); continue; }
      if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
      const data = (await res.json()) as { total?: number };
      return data.total ?? 0;
    } catch (err) {
      if (attempt === 3) {
        console.warn(`  ${cred.clientName} · ${tag}: ${err}`);
        return null;
      }
      await sleep(500 * attempt);
    }
  }
  return null;
}

function normName(s: string): string {
  return s.toLowerCase().replace(/[^a-z0-9]/g, '');
}

function loadCreds(): Cred[] | null {
  const localPath = path.join(ROOT, 'ghl-credentials.local.json');
  if (fs.existsSync(localPath)) return Object.values(JSON.parse(fs.readFileSync(localPath, 'utf8')));
  if (process.env.GHL_CREDENTIALS_JSON) return Object.values(JSON.parse(process.env.GHL_CREDENTIALS_JSON));
  return null;
}

async function main() {
  const creds = loadCreds();
  if (!creds) {
    console.warn('No GHL credentials (ghl-credentials.local.json or GHL_CREDENTIALS_JSON) — skipping lead-count sync.');
    return;
  }
  const manifest = JSON.parse(fs.readFileSync(path.join(ROOT, 'public', 'data', 'manifest.json'), 'utf8'));

  // Resolve credential names to manifest names where possible so the
  // dashboard can look counts up by the client name it renders.
  const manifestNames = new Map<string, string>();
  for (const p of manifest.periods) for (const c of p.clients) manifestNames.set(normName(c.name), c.name);

  const periods: string[] = manifest.periods.map((p: { id: string }) => p.id);
  const out: {
    generatedAt: string;
    tags: string[];
    periods: Record<string, Record<string, Record<string, number | null>>>;
  } = { generatedAt: new Date().toISOString(), tags: [...TAGS], periods: {} };
  for (const id of periods) out.periods[id] = {};

  for (const cred of creds) {
    if (SKIP_CLIENTS.has(cred.clientName)) continue;
    const displayName =
      NAME_ALIASES[cred.clientName] ?? manifestNames.get(normName(cred.clientName)) ?? cred.clientName;
    process.stdout.write(`${displayName} ... `);
    for (const periodId of periods) {
      const window = monthWindow(periodId);
      if (!window) continue;
      const [meta, ig, fb] = await Promise.all(TAGS.map((t) => tagCount(cred, t, window)));
      out.periods[periodId][displayName] = {
        'meta ads lead': meta,
        'instagram lead': ig,
        'facebook lead': fb,
      };
      await sleep(80);
    }
    console.log('done');
  }

  const outPath = path.join(ROOT, 'public', 'data', 'ghl-lead-counts.json');
  fs.writeFileSync(outPath, JSON.stringify(out, null, 2), 'utf8');
  console.log(`\nWrote ${outPath} — ${creds.length - SKIP_CLIENTS.size} clients × ${periods.length} periods`);
}

main().catch((err) => {
  // Never fail the build over lead counts — the previous counts file (if any)
  // keeps serving until the next successful sync.
  console.error('GHL lead-count sync failed (non-fatal):', err);
});
