// Merges the platform-synced PMS data (authoritative revenue/check-in dates,
// already cross-checked against the live GHL/platform API) with the manually
// compiled xlsx export's coupon/discount/source fields (which the platform
// export doesn't have) — per decision: platform data for ROI, xlsx data only
// for promo-code attribution. Produces the July snapshot the /july page reads.
//
// Deliberately does NOT touch public/data/periods/july-2026/clients/ (the
// platform sync's own directory) — reads it read-only, merges in memory, and
// feeds the merged result straight into processAllData().
//
// Usage: npx tsx scripts/build-july-merged-snapshot.mts

import fs from 'fs';
import path from 'path';
import Papa from 'papaparse';
import { parsePMSData } from '../src/lib/parsers/pmsData';
import { processAllData, UploadedFilesMap } from '../src/lib/analysis/processor';
import { normalizeEmail } from '../src/lib/utils';

class NodeFileReader {
  onload: ((ev: { target: { result: string } }) => void) | null = null;
  onerror: ((err: unknown) => void) | null = null;
  result: string | null = null;
  readAsText(blob: Blob) {
    blob.text().then((text) => {
      this.result = text;
      this.onload?.({ target: { result: text } });
    }).catch((err) => this.onerror?.(err));
  }
}
// @ts-expect-error polyfill
globalThis.FileReader = NodeFileReader;

const ROOT = path.resolve(import.meta.dirname, '..');
const PERIOD_ID = 'july-2026';
const CLIENTS_DIR = path.join(ROOT, 'public', 'data', 'periods', PERIOD_ID, 'clients');
const XLSX_SOURCE_DIR = path.join(ROOT, 'public', 'data', 'periods', PERIOD_ID, 'xlsx-source');
const SHARED_DIR = path.join(ROOT, 'public', 'data', 'periods', PERIOD_ID, 'shared');

// Manually verified manifest-client-name → xlsx-source-folder-name mapping.
// Hardcoded rather than fuzzy-matched: after an xlsx sheet name accidentally
// collided with (and overwrote) a platform-synced folder earlier due to
// macOS's case-insensitive filesystem, an auditable explicit list is safer
// than a generic algorithm for this specific, small, one-time merge.
const MANIFEST_TO_XLSX_SOURCE: Record<string, string> = {
  'Tàberg Falls': 'Tàberg Falls',
  'Home Base': 'HomeBase',
  'Treetop Escapes': 'Treetop Escapes',
  'Red White & Blue Views': 'Red White & Blue Views',
  'Asheville River Cabins': 'Asheville',
  'Myrinn': 'Myrinn',
  'Inspired Retreats': 'Inspired Retreats',
  'Away2PA': 'Away2PA',
  'Stay Saluda': 'Stay Saluda',
  'Best Texas Travel': 'Best Texas Travel',
  'Stay on 30a': 'Stay on 30a',
  'Selah Place': 'Selah Place',
  'Stay Southen Illinois': 'Stay Southern Illinois',
  'Three Suns Cabins': 'Three Suns Cabins',
  'Green Springs Inn': 'Green Springs Inn',
  'Flohom': 'FLOHOM',
  'Paradise Pointe': 'Paradise Pointe',
  'Parker Reserve': 'Parker Reserve',
  'The Cohost Company': 'The Cohost Company',
  'Evergreen Cabins': 'Evergreen Cabins',
  'Awayframes': 'Awayframes',
  'Reflections Resorts': 'Reflections Resorts',
};

function csvCell(v: unknown): string {
  const s = v === null || v === undefined ? '' : String(v);
  if (/[",\n]/.test(s)) return '"' + s.replace(/"/g, '""') + '"';
  return s;
}
function rowsToCSV(headers: string[], rows: unknown[][]): string {
  return [headers, ...rows].map((r) => r.map(csvCell).join(',')).join('\n') + '\n';
}

interface ManifestClient { name: string; pms?: string; ghl?: string; }
interface ManifestPeriod { id: string; label: string; metaAds?: string; promoCodes?: string; clients: ManifestClient[]; }
interface Manifest { periods: ManifestPeriod[]; }

async function main() {
  const manifest: Manifest = JSON.parse(
    fs.readFileSync(path.join(ROOT, 'public', 'data', 'manifest.json'), 'utf8'),
  );
  const period = manifest.periods.find((p) => p.id === PERIOD_ID);
  if (!period) throw new Error(`Period ${PERIOD_ID} not found`);

  const files: UploadedFilesMap = { metaAds: null, promoCodes: null, pmsFiles: {}, ghlFiles: {} };

  // Starlight Haven Weiss Lake / Hot Springs Meta campaigns, July 1–31 2026
  // (manually provided — not in the platform's Meta Ads.csv since these two
  // accounts aren't synced there at all). Appended to the base Meta Ads CSV
  // so they flow through the same classifyCampaign()/aggregateFacebookStats()
  // pipeline as every other client.
  const STARLIGHT_META_ROWS: [string, string, number, number, number, number, number, number][] = [
    ['Starlight Haven Weiss Lake', 'Website Retargeting Campaign - 03/03/26', 1538.49, 2484, 4, 118290, 41, 23329.84],
    ['Starlight Haven Weiss Lake', 'New Leads Campaign - 03/03/26', 614.69, 2133, 826, 78608, 1, 185.69],
    ['Starlight Haven Weiss Lake', 'ToF Keyword Engagement - 07/29/26', 9.42, 36, 0, 670, 0, 0],
    ['Starlight Haven Hot Springs', 'New Leads Campaign - 03/03/26', 922.07, 4439, 2813, 144797, 2, 1164.89],
    ['Starlight Haven Hot Springs', 'Discovery Campaign - Giveaway - 12/16/2025', 616.11, 1825, 0, 52562, 0, 0],
    ['Starlight Haven Hot Springs', 'Website Retargeting Campaign - 03/03/26', 613.27, 1693, 7, 63882, 16, 10500.17],
    ['Starlight Haven Hot Springs', 'ToF Keyword Engagement - 07/31/26', 8.16, 45, 0, 673, 0, 0],
  ];
  const META_ADS_HEADERS = ['Account name', 'Campaign name', 'Amount spent', 'Link clicks', 'Leads', 'Impressions', 'Purchases', 'Purchases conversion value'];

  // July campaigns for the xlsx-only clients, from the manually exported Meta
  // "Monthly Report" (the platform's Meta Ads.csv only covers its own synced
  // ad accounts). Account names are rewritten to exact dashboard client names
  // via this explicit map — never fuzzy-matched (same auditability rationale
  // as MANIFEST_TO_XLSX_SOURCE). Accounts in the report but deliberately NOT
  // mapped: platform-synced clients (already covered — would double-count),
  // both Starlights (hardcoded above), The Canopy At Moody Moon Ridge /
  // Reflections Resorts (per instruction), and off-dashboard accounts
  // (VillaDestino, CGG, Austin Surf Lodge, American River Resort, Oak &
  // Ember, Nature Nooks, Edenwood NC, Tuxedo Falls).
  const MONTHLY_REPORT_ACCOUNT_TO_CLIENT: Record<string, string> = {
    'Wanderin Star Farms New Ad Account': 'Wanderin Star Farms',
    // Added Aug 11 per Shawal: ARR joins the dashboard. Its sheet tab is a
    // discounts ledger (no booking revenue), so the client is Meta-ads +
    // reporting-sheet only — no PMS rows.
    'American River Resort': 'American River Resort',
    'Nature Nooks Ad Account': 'Nature Nooks',
    'Hiawassee Glamping': 'Hiawassee Glamping',
    'Stay Different Ads': 'Stay Different',
    'The Outpost Grand Canyon': 'The Outpost',
    'Ponderosa Pines Resort': 'Ponderosa Pines Resort',
    'Bison Ridge Retreat Ad Account': 'Bison Ridge Retreat',
    '@staywithbranch': 'Stay with Branch',
    'Big Moon Ranch': 'Big Moon Ranch',
    'Sunapee Stays Ads Account': 'Sunapee Stays',
    'Dwell Luxury Rentals Ads': 'Dwell',
    'Stay Luxe Ads': 'StayLuxe',
    'Endless Stays': 'Endless Stays',
  };

  function monthlyReportRows(): unknown[][] {
    const reportPath = path.join(ROOT, 'July 2026 PMS Data', 'Meta Monthly Report - July 2026.csv');
    if (!fs.existsSync(reportPath)) {
      console.warn('Meta Monthly Report CSV not found — skipping xlsx-only clients’ ad data');
      return [];
    }
    const parsed = Papa.parse<Record<string, string>>(fs.readFileSync(reportPath, 'utf8'), {
      header: true,
      skipEmptyLines: true,
    });
    const num = (v: string | undefined) => (v && v.trim() ? Number(v) : 0);
    const rows: unknown[][] = [];
    for (const r of parsed.data) {
      const account = (r['Account name'] ?? '').trim();
      const campaign = (r['Campaign name'] ?? '').trim();
      let client = MONTHLY_REPORT_ACCOUNT_TO_CLIENT[account];
      // The Outpost also ran three campaigns under the agency's shared
      // "HiddenGem Marketing" account — routed by campaign name.
      if (!client && account === 'HiddenGem Marketing' && /outpost/i.test(campaign)) {
        client = 'The Outpost';
      }
      if (!client) continue;
      const spend = num(r['Amount spent (USD)']);
      const cpm = num(r['CPM (cost per 1,000 impressions)']);
      // The report has CPM instead of raw impressions: impressions = spend / CPM × 1000.
      const impressions = cpm > 0 ? Math.round((spend / cpm) * 1000) : 0;
      rows.push([client, campaign, spend, num(r['Link clicks']), num(r['Leads']), impressions, num(r['Purchases']), num(r['Purchases conversion value'])]);
    }
    return rows;
  }

  if (period.metaAds) {
    const baseBuf = fs.readFileSync(path.join(ROOT, 'public', period.metaAds));
    const extraRows = [...STARLIGHT_META_ROWS, ...monthlyReportRows()];
    const extraCsv = rowsToCSV(META_ADS_HEADERS, extraRows).split('\n').slice(1).join('\n');
    const combined = baseBuf.toString('utf8').replace(/\n?$/, '\n') + extraCsv;
    files.metaAds = new File([combined], 'Meta Ads.csv', { type: 'text/csv' });
  }

  // Promo codes: prefer the CRM-provided sheet dropped into July's xlsx data folder.
  const promoCodesSrc = path.join(ROOT, 'July 2026 PMS Data', 'CRM - HiddenGem Media - Client Promo Codes.csv');
  if (fs.existsSync(promoCodesSrc)) {
    const buf = fs.readFileSync(promoCodesSrc);
    files.promoCodes = new File([buf], 'Promo codes.csv', { type: 'text/csv' });
    // Also persist into shared/ so it's part of the period's normal manifest-driven data.
    fs.mkdirSync(SHARED_DIR, { recursive: true });
    fs.writeFileSync(path.join(SHARED_DIR, 'Promo codes.csv'), buf);
  }

  const mergeLog: Record<string, unknown>[] = [];

  // Clients where the platform PMS data and the xlsx export overlap so little
  // (or the platform figure was independently confirmed wrong) that merging
  // them would double-count. For these, the xlsx export is used exclusively —
  // platform PMS data is ignored entirely. Evergreen Cabins: platform's 34
  // rows ($51,885.29) vs xlsx's 49 rows ($62,289.95, confirmed correct).
  // Stay Southen Illinois: platform's 121 rows ($79,360.01) are stays
  // checking in during July across this client's ~34 cabins; the account
  // manager's sheet (11 rows, $6,600.23) scopes to reservations booked
  // during July instead — user chose the booked-in-July scope explicitly.
  // Away2PA: platform's 27 rows total $201,667 vs the AM sheet's 23 rows
  // at $86,385 — user confirmed ~86K is correct (Aug 2026), platform
  // roi-export overstates this client, so the AM sheet wins outright.
  // Awayframes: same pattern — platform+merge gave $62,138.81, user
  // confirmed ~34K; the AM sheet's 17 rows ($34,466.13) win outright.
  // Best Texas Travel: platform gave $152K; the AM sheet's own totals row
  // says $27,623.94 across 41 bookings — user confirmed ~27K correct.
  // Flohom: platform+merge gave $248K/198 bookings; the AM sheet's 153
  // rows total $114,182.04 — user confirmed ~114K correct.
  // Green Springs Inn: platform+merge gave $59,668.39/122 bookings; the AM
  // sheet's 87 rows total $26,998.76 — user confirmed ~26K correct.
  // Home Base: platform+merge gave $143,424.99/31 bookings; the AM sheet's
  // 43 rows total $138,923.48 — user confirmed ~138K correct.
  const USE_XLSX_EXCLUSIVELY = new Set([
    'Evergreen Cabins',
    'Stay Southen Illinois',
    'Away2PA',
    'Awayframes',
    'Best Texas Travel',
    'Flohom',
    'Green Springs Inn',
    'Home Base',
    // Inspired Retreats: platform gave $3,368.45/5 bookings; the AM sheet's
    // 2 rows total $5,163.69 — user confirmed ~5K correct.
    'Inspired Retreats',
    // Myrinn: platform+add-all-merge gave $26,833.59/25 bookings; the AM
    // sheet's 12 rows total $12,494.08 — user confirmed ~12K correct.
    // (Supersedes the earlier add-all-rows merge exception for this client.)
    'Myrinn',
    // Paradise Pointe: platform+merge gave $258,118.51/217 bookings; the AM
    // sheet's 89 rows total $100,192.38 — user confirmed ~100K correct.
    'Paradise Pointe',
    // Batch of AM-confirmed totals (user, Aug 2026) — in every case the AM
    // sheet total matched the confirmed figure exactly and the platform
    // (or platform+merge) figure did not:
    'Selah Place', // $21,795.23 (platform+merge gave $19,702.30)
    'Stay on 30a', // $529,070.56 (platform+merge gave $819,037.97)
    'Stay Saluda', // $17,371.79 (platform+merge gave $12,550.97)
    'Tàberg Falls', // $127,465.25 (platform gave $51,847.60)
    'The Cohost Company', // $72,305.78 (platform+merge gave $63,244.54)
    'Treetop Escapes', // $44,179.45 (platform+merge gave $477,657.44)
    'Three Suns Cabins', // $13,488.66 payout basis (platform+merge gave $24,683.09)
  ]);

  for (const client of period.clients) {
    if (client.ghl) {
      const buf = fs.readFileSync(path.join(ROOT, 'public', client.ghl));
      files.ghlFiles[client.name] = new File([buf], 'GHL data.csv', { type: 'text/csv' });
    }
    if (!client.pms || USE_XLSX_EXCLUSIVELY.has(client.name)) {
      // Platform has no PMS data for this client at all this period — nothing
      // to conflict with, so fill the gap from the xlsx source directly if we
      // have one (rather than leaving it blank when real booking data exists).
      const xlsxFolder = MANIFEST_TO_XLSX_SOURCE[client.name];
      const xlsxPath = xlsxFolder ? path.join(XLSX_SOURCE_DIR, xlsxFolder, 'PMS data.csv') : null;
      if (xlsxPath && fs.existsSync(xlsxPath)) {
        files.pmsFiles[client.name] = new File([fs.readFileSync(xlsxPath)], 'PMS data.csv', { type: 'text/csv' });
        mergeLog.push({
          client: client.name,
          xlsxMatch: xlsxFolder,
          platformRows: 0,
          note: USE_XLSX_EXCLUSIVELY.has(client.name)
            ? 'forced xlsx-exclusive override — platform PMS data ignored for this client'
            : 'platform had no PMS data — used xlsx directly',
        });
      }
      continue;
    }

    const platformBuf = fs.readFileSync(path.join(ROOT, 'public', client.pms));
    const platformFile = new File([platformBuf], 'PMS data.csv', { type: 'text/csv' });
    const platformParsed = await parsePMSData(platformFile);

    const xlsxFolder = MANIFEST_TO_XLSX_SOURCE[client.name];
    const xlsxPath = xlsxFolder ? path.join(XLSX_SOURCE_DIR, xlsxFolder, 'PMS data.csv') : null;

    if (!xlsxPath || !fs.existsSync(xlsxPath)) {
      // No enrichment available — use the platform file as-is.
      files.pmsFiles[client.name] = platformFile;
      mergeLog.push({ client: client.name, xlsxMatch: xlsxFolder ?? null, enriched: 0, platformRows: platformParsed.rows.length });
      continue;
    }

    const xlsxBuf = fs.readFileSync(xlsxPath);
    const xlsxFile = new File([xlsxBuf], 'PMS data.csv', { type: 'text/csv' });
    const xlsxParsed = await parsePMSData(xlsxFile);

    const xlsxByEmail = new Map<string, typeof xlsxParsed.rows[number]>();
    for (const row of xlsxParsed.rows) {
      const key = normalizeEmail(row.email);
      if (key) xlsxByEmail.set(key, row);
    }

    const platformEmails = new Set(platformParsed.rows.map((row) => normalizeEmail(row.email)).filter(Boolean));

    let enrichedCount = 0;
    const mergedRows = platformParsed.rows.map((row) => {
      const key = normalizeEmail(row.email);
      const enrichment = key ? xlsxByEmail.get(key) : undefined;
      if (!enrichment) return row;
      enrichedCount++;
      return {
        ...row,
        couponName: enrichment.couponName || row.couponName,
        couponDiscount: enrichment.couponDiscount || row.couponDiscount,
        source: enrichment.source || row.source,
      };
    });

    // A confirmed-promo-code xlsx guest who isn't in the platform's booking
    // list at all would otherwise have their promo revenue silently dropped
    // (enrichment only overlays existing platform rows). Per decision, add
    // these as new bookings — but ONLY when a coupon name is present, i.e.
    // guests we've manually confirmed used a code. Uncoded xlsx-only rows
    // are NOT added; platform stays authoritative for everything else.
    //
    // Myrinn is an explicit exception (per instruction): its xlsx rows are
    // scoped by BOOKING date, not check-in date, and ALL of them — coded or
    // not — should count toward July regardless of overlap with platform.
    const addAllRows = client.name === 'Myrinn';
    let addedCount = 0;
    for (const row of xlsxParsed.rows) {
      const key = normalizeEmail(row.email);
      if (!addAllRows && !row.couponName) continue;
      if (key && platformEmails.has(key)) continue; // already enriched above
      mergedRows.push(row);
      addedCount++;
    }

    const outHeaders = ['Guest', 'Email', 'Revenue', 'Check-in date', 'Coupon name', 'Coupon discount', 'Source'];
    const outRows = mergedRows.map((r) => [r.guest, r.email, r.revenue, r.checkIn, r.couponName, r.couponDiscount, r.source]);
    const mergedCsv = rowsToCSV(outHeaders, outRows);
    files.pmsFiles[client.name] = new File([mergedCsv], 'PMS data.csv', { type: 'text/csv' });

    mergeLog.push({
      client: client.name,
      xlsxMatch: xlsxFolder,
      platformRows: platformParsed.rows.length,
      xlsxRows: xlsxParsed.rows.length,
      enriched: enrichedCount,
      addedAsNewBookings: addedCount,
    });
  }

  // Clients with no platform sync at all (no manifest entry, no Meta Ads, no
  // GHL) whose July bookings exist only in the account managers' xlsx exports.
  // Added PMS-only per decision — ad data can be layered in later per client.
  // Display names are chosen to match the CRM promo sheet's client names so
  // promo-code attribution resolves (e.g. the xlsx tab "Wanderin Stars" is
  // "Wanderin Star Farms" in the promo sheet).
  const XLSX_ONLY_CLIENTS: Record<string, string> = {
    'Wanderin Star Farms': 'Wanderin Stars',
    'Hiawassee Glamping': 'Hiawassee Glamping',
    'Stay Different': 'Stay Different',
    'The Outpost': 'The Outpost',
    'Ponderosa Pines Resort': 'Ponderosa Pines Resort',
    'Bison Ridge Retreat': 'Bison Ridge Retreat',
    'Hillside Amble': 'Hillside Amble',
    'Stay with Branch': 'Branch',
    'Big Moon Ranch': 'Big Moon Ranch',
    'Sunapee Stays': 'Sunapee',
    'Dwell': 'Dwell',
    'StayLuxe': 'StayLuxe',
    'Endless Stays': 'Endless Stays',
    // ARR's sheet tab is a discounts ledger with no booking amounts, so this
    // PMS file holds ONLY the 4 WELCOME20 uses (revenue back-computed from
    // the 20% discount: paid = 4 × discount) — per Shawal (Aug 11), those
    // four go to the Followers campaign. Full booking revenue lives in the
    // client reporting sheet, not here.
    'American River Resort': 'American River Resort',
    // Added Aug 11 from the Nature Nooks tab Alicia added to her live sheet
    // ($19,986.13 — matches the client reporting sheet exactly).
    'Nature Nooks': 'Nature Nooks',
  };
  for (const [name, xlsxFolder] of Object.entries(XLSX_ONLY_CLIENTS)) {
    const pmsPath = path.join(XLSX_SOURCE_DIR, xlsxFolder, 'PMS data.csv');
    if (!fs.existsSync(pmsPath)) {
      mergeLog.push({ client: name, xlsxMatch: xlsxFolder, note: 'SKIPPED — xlsx-source PMS file missing' });
      continue;
    }
    files.pmsFiles[name] = new File([fs.readFileSync(pmsPath)], 'PMS data.csv', { type: 'text/csv' });
    period.clients.push({
      name,
      pms: `/data/periods/${PERIOD_ID}/xlsx-source/${xlsxFolder}/PMS data.csv`,
    });
    mergeLog.push({ client: name, xlsxMatch: xlsxFolder, note: 'xlsx-only client — PMS data only, no platform/Meta/GHL yet' });
  }

  // Starlight Haven Hot Springs / Weiss Lake: registered on the platform (real
  // tenant ids, GHL contacts pulled live) but not in the manifest — no Meta Ads
  // campaigns, so no Retargeting attribution is possible, but GHL lead matching
  // (Instagram/Facebook tag → PMS email) works independent of ad spend. PMS
  // comes from a full multi-month reservation export, pre-filtered to July by
  // "Reserved On" (booking date) — see the one-off filtering step that produced
  // xlsx-source/Starlight Haven .../PMS data.csv.
  const STARLIGHT_CLIENTS = ['Starlight Haven Hot Springs', 'Starlight Haven Weiss Lake'];
  for (const name of STARLIGHT_CLIENTS) {
    const pmsPath = path.join(XLSX_SOURCE_DIR, name, 'PMS data.csv');
    const ghlPath = path.join(CLIENTS_DIR, name, 'GHL data.csv');
    if (fs.existsSync(pmsPath)) {
      files.pmsFiles[name] = new File([fs.readFileSync(pmsPath)], 'PMS data.csv', { type: 'text/csv' });
    }
    if (fs.existsSync(ghlPath)) {
      files.ghlFiles[name] = new File([fs.readFileSync(ghlPath)], 'GHL data.csv', { type: 'text/csv' });
    }
    period.clients.push({
      name,
      pms: `/data/periods/${PERIOD_ID}/xlsx-source/${name}/PMS data.csv`,
      ghl: `/data/periods/${PERIOD_ID}/clients/${name}/GHL data.csv`,
    });
    mergeLog.push({ client: name, note: 'new client, no manifest/platform PMS — added directly from Starlight reservation export' });
  }

  console.log('Merge summary:');
  for (const entry of mergeLog) console.log(' ', JSON.stringify(entry));

  const data = await processAllData(files);

  // GHL lead-count corrections from the team's July QA pass (Aug 11 2026).
  // The platform's GHL tag-based counts were wrong for these clients (tags
  // over/under-counted, or GHL never synced at all); the team supplied the
  // verified counts. Only totalGHLLeads is overridden — email-match lists
  // stay as computed.
  const GHL_LEAD_OVERRIDES: Record<string, { instagram?: number; facebook?: number }> = {
    'Stay with Branch': { instagram: 149 },
    'Asheville River Cabins': { instagram: 283 },
    'Myrinn': { instagram: 242 },
    'Starlight Haven Hot Springs': { instagram: 82 },
    'Starlight Haven Weiss Lake': { instagram: 49 },
    'Big Moon Ranch': { instagram: 196, facebook: 459 },
    'Home Base': { instagram: 212 },
    'Stay on 30a': { instagram: 308 },
  };
  for (const [name, o] of Object.entries(GHL_LEAD_OVERRIDES)) {
    const client = data.clients[name];
    if (!client?.pmsAnalysis) {
      console.warn(`GHL override skipped — no pmsAnalysis for ${name}`);
      continue;
    }
    if (o.instagram !== undefined) client.pmsAnalysis.instagram.totalGHLLeads = o.instagram;
    if (o.facebook !== undefined) client.pmsAnalysis.facebook.totalGHLLeads = o.facebook;
  }

  console.log(`\nProcessed ${Object.keys(data.clients).length} clients, ${data.flags.length} flags.`);

  const outDir = path.join(ROOT, 'public', 'data', 'snapshots');
  fs.mkdirSync(outDir, { recursive: true });
  fs.writeFileSync(path.join(outDir, `${PERIOD_ID}.json`), JSON.stringify({ period, data }, null, 2), 'utf8');
  console.log(`Wrote ${path.join(outDir, `${PERIOD_ID}.json`)}`);
}

main().catch((err) => {
  console.error('Merge/snapshot failed:', err);
  process.exit(1);
});
