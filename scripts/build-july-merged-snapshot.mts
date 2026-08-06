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

  if (period.metaAds) {
    const buf = fs.readFileSync(path.join(ROOT, 'public', period.metaAds));
    files.metaAds = new File([buf], 'Meta Ads.csv', { type: 'text/csv' });
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

  for (const client of period.clients) {
    if (client.ghl) {
      const buf = fs.readFileSync(path.join(ROOT, 'public', client.ghl));
      files.ghlFiles[client.name] = new File([buf], 'GHL data.csv', { type: 'text/csv' });
    }
    if (!client.pms) {
      // Platform has no PMS data for this client at all this period — nothing
      // to conflict with, so fill the gap from the xlsx source directly if we
      // have one (rather than leaving it blank when real booking data exists).
      const xlsxFolder = MANIFEST_TO_XLSX_SOURCE[client.name];
      const xlsxPath = xlsxFolder ? path.join(XLSX_SOURCE_DIR, xlsxFolder, 'PMS data.csv') : null;
      if (xlsxPath && fs.existsSync(xlsxPath)) {
        files.pmsFiles[client.name] = new File([fs.readFileSync(xlsxPath)], 'PMS data.csv', { type: 'text/csv' });
        mergeLog.push({ client: client.name, xlsxMatch: xlsxFolder, platformRows: 0, note: 'platform had no PMS data — used xlsx directly' });
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
