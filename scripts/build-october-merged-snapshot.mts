// Builds the frozen October 2026 snapshot — the MANUAL pipeline (AM sheets
// authoritative for bookings/promo, like July–September).
//
// Sources:
//   • PMS      — public/data/periods/october-2026/xlsx-source/<client>/
//                (from scripts/convert-october-xlsx.mts over the seven AM
//                workbooks in Monthly Data/2026-10 October).
//   • Meta Ads — Monthly Data/2026-10 October/Monthly-Report (11).csv (Ads
//                Manager export, Oct 1–31, AD SET level → aggregated to campaign
//                level here; the blank-account grand-total row is the checksum).
//   • GHL      — none this month: the platform sync secret is rejected (401),
//                so no per-client GHL contact CSVs. GHL lead counts come from
//                scripts/sync-ghl-lead-counts.mts instead.
//   • Promo    — data/promo-codes.csv
//
// SCOPE (per Shawal, Oct 2026): only clients visible in the Meta ads report
// get analyzed. AM tabs for clients absent from the report (Raven Rock, no
// October spend) are skipped. Dunya Camp (kickoff Oct 22, client-run
// campaigns) is left unmapped like Edenwood NC was in September.
//
// Usage: npx tsx scripts/build-october-merged-snapshot.mts

import fs from 'fs';
import path from 'path';
import Papa from 'papaparse';
import { processAllData, UploadedFilesMap } from '../src/lib/analysis/processor';

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
const PERIOD_ID = 'october-2026';
const XLSX_SOURCE = path.join(ROOT, 'public', 'data', 'periods', PERIOD_ID, 'xlsx-source');
const PLATFORM_CLIENTS = path.join(ROOT, 'public', 'data', 'periods', PERIOD_ID, 'clients');
const REPORT_PATH = path.join(ROOT, 'Monthly Data', '2026-10 October', 'Monthly-Report (11).csv');

// Account names exactly as they appear in the October export (Meta renamed
// most accounts with an "Ads" suffix between September and October).
const REPORT_ACCOUNT_TO_CLIENT: Record<string, string> = {
  '@staywithbranch': 'Stay with Branch',
  'American River Resort Ads': 'American River Resort',
  'Asheville River Cabins Ads': 'Asheville River Cabins',
  'Away2Pa Ads': 'Away2PA',
  'Awayframes Ads': 'Awayframes',
  'Best Texas Travel Ads': 'Best Texas Travel',
  'Bison Ridge Retreat Ads': 'Bison Ridge Retreat',
  'Cabin Collective Ads': 'Cabin Collective',
  'Columbia Gorge Getaways Ads': 'Columbia Gorge Getaways',
  'Endless Stays Ads': 'Endless Stays',
  'Evergreen Cabins Ads': 'Evergreen Cabins',
  'FLOHOM Ads': 'Flohom',
  'Glasscombe Ads': 'Glasscombe',
  'Green Springs Inn Ads': 'Green Springs Inn',
  'Hiawassee Glamping Ads': 'Hiawassee Glamping',
  'Home Base Ads': 'Home Base',
  'Inspired Retreats Ads 2.0': 'Inspired Retreats',
  'Little River Landing Ads': 'Little River Landing',
  'Myrinn - Ad Account 2.0': 'Myrinn',
  'Nature Nooks Ads': 'Nature Nooks',
  'North Star Lodge & Resort Ads': 'North Star Lodge & Resort',
  'Oak & Ember Ads': 'Oak & Ember',
  'Paradise Pointe Ads': 'Paradise Pointe',
  'Parker Reserve Ads': 'Parker Reserve',
  'Ponderosa Pines Resort Ads': 'Ponderosa Pines Resort',
  'Red White & Blue Views Ads': 'Red White & Blue Views',
  'Ridge & Falls Ads': 'Ridge & Falls',
  'Selah.place Ads': 'Selah Place',
  'Southern Illinois Cabins Ads': 'Stay Southen Illinois',
  'Starlight Haven Hot Springs': 'Starlight Haven Hot Springs',
  'Starlight Haven Weiss Lake - 74756899': 'Starlight Haven Weiss Lake',
  'Stay Luxe Ads': 'StayLuxe',
  'Stay Saluda Ads': 'Stay Saluda',
  'Stay on 30a Ads': 'Stay on 30a',
  'Sunapee Stays Ads': 'Sunapee Stays',
  'The Cohost Company Ads': 'The Cohost Company',
  'The Outpost Grand Canyon Ads': 'The Outpost',
  'Three Suns Cabins Ads': 'Three Suns Cabins',
  'Treetop Escapes Ads': 'Treetop Escapes',
  'Tuxedo Falls Ads': 'Tuxedo Falls',
  'Walden Retreats Ads': 'Walden Retreats',
  'Táberg Falls Ads': 'Tàberg Falls',
  'TÃ¡berg Falls Ads': 'Tàberg Falls', // mojibake variant
};

function csvCell(v: unknown): string {
  const s = v === null || v === undefined ? '' : String(v);
  if (/[",\n]/.test(s)) return '"' + s.replace(/"/g, '""') + '"';
  return s;
}

/** FLOHOM: Makenna's workbook carries a FLOHOM tab (Hostaway export with site coupon names). */
function checkFlohomPms(): void {
  if (!fs.existsSync(path.join(XLSX_SOURCE, 'Flohom', 'PMS data.csv'))) {
    console.warn('Flohom: no converted AM tab in xlsx-source — Flohom will be ads-only.');
  }
}

async function main() {
  checkFlohomPms();

  const files: UploadedFilesMap = { metaAds: null, promoCodes: null, pmsFiles: {}, ghlFiles: {} };

  // ── Meta ads: ad-set rows → campaign-level aggregation ─────────────────────
  const parsed = Papa.parse<Record<string, string>>(fs.readFileSync(REPORT_PATH, 'utf8'), {
    header: true,
    skipEmptyLines: true,
    transformHeader: (h) => h.replace(/^﻿/, '').trim(),
  });
  const num = (v: string | undefined) => (v && v.trim() ? Number(v) : 0);
  type Agg = { spend: number; clicks: number; leads: number; impressions: number; purchases: number; conv: number };
  const byCampaign = new Map<string, Agg & { client: string; campaign: string }>();
  let grandTotal = 0, mappedSpend = 0;
  const skipped = new Set<string>();
  for (const r of parsed.data) {
    const account = (r['Account name'] ?? '').trim();
    const campaign = (r['Campaign name'] ?? '').trim();
    const spend = num(r['Amount spent (USD)']);
    if (!account) { grandTotal += spend; continue; } // export grand-total row
    let client = REPORT_ACCOUNT_TO_CLIENT[account];
    if (!client && account === 'HiddenGem Marketing' && /outpost/i.test(campaign)) client = 'The Outpost';
    if (!client) { skipped.add(account); continue; }
    const key = `${client}\u0000${campaign}`;
    const e = byCampaign.get(key) ?? { client, campaign, spend: 0, clicks: 0, leads: 0, impressions: 0, purchases: 0, conv: 0 };
    e.spend += spend;
    e.clicks += num(r['Link clicks']);
    e.leads += num(r['Leads']);
    e.impressions += num(r['Impressions']);
    e.purchases += num(r['Purchases']);
    e.conv += num(r['Purchases conversion value']);
    byCampaign.set(key, e);
    mappedSpend += spend;
  }

  const rows: string[] = ['Account name,Campaign name,Amount spent,Link clicks,Leads,Impressions,Purchases,Purchases conversion value'];
  for (const e of byCampaign.values()) {
    rows.push([e.client, e.campaign, e.spend, e.clicks, e.leads, e.impressions, e.purchases, e.conv].map(csvCell).join(','));
  }
  files.metaAds = new File([rows.join('\n') + '\n'], 'Meta Ads.csv', { type: 'text/csv' });
  const sharedDir = path.join(ROOT, 'public', 'data', 'periods', PERIOD_ID, 'shared');
  fs.mkdirSync(sharedDir, { recursive: true });
  fs.writeFileSync(path.join(sharedDir, 'Meta Ads.csv'), rows.join('\n') + '\n', 'utf8');
  console.log(`Meta ads: ${byCampaign.size} campaigns from ${parsed.data.length} ad-set rows; mapped $${mappedSpend.toFixed(2)} vs export total $${grandTotal.toFixed(2)}; skipped accounts: ${[...skipped].join(', ') || 'none'}`);

  const promoPath = path.join(ROOT, 'data', 'promo-codes.csv');
  if (fs.existsSync(promoPath)) {
    files.promoCodes = new File([fs.readFileSync(promoPath)], 'Promo codes.csv', { type: 'text/csv' });
    fs.copyFileSync(promoPath, path.join(ROOT, 'public', 'data', 'periods', PERIOD_ID, 'shared', 'Promo codes.csv'));
  }

  // ── PMS: only clients visible in the Meta report (scope rule) ──────────────
  const inScope = new Set([...byCampaign.values()].map((e) => e.client));
  const clients: { name: string; pms: string; ghl: string }[] = [];
  const skippedPms: string[] = [];
  for (const name of fs.readdirSync(XLSX_SOURCE).sort()) {
    const pmsFile = path.join(XLSX_SOURCE, name, 'PMS data.csv');
    if (!fs.existsSync(pmsFile)) continue;
    if (!inScope.has(name)) { skippedPms.push(name); continue; }
    files.pmsFiles[name] = new File([fs.readFileSync(pmsFile)], 'PMS data.csv', { type: 'text/csv' });

    const ghlFile = path.join(PLATFORM_CLIENTS, name, 'GHL data.csv');
    let ghlPath = '';
    if (fs.existsSync(ghlFile)) {
      files.ghlFiles[name] = new File([fs.readFileSync(ghlFile)], 'GHL data.csv', { type: 'text/csv' });
      ghlPath = `/data/periods/${PERIOD_ID}/clients/${name}/GHL data.csv`;
    }
    clients.push({ name, pms: `/data/periods/${PERIOD_ID}/xlsx-source/${name}/PMS data.csv`, ghl: ghlPath });
  }
  if (skippedPms.length) console.log(`PMS tabs skipped (not in Meta report): ${skippedPms.join(', ')}`);

  const data = await processAllData(files);
  const withPms = Object.values(data.clients).filter((c) => c.pmsAnalysis).length;
  const withFb = Object.values(data.clients).filter((c) => c.facebookStats).length;
  console.log(`Processed ${Object.keys(data.clients).length} clients (${withPms} with PMS, ${withFb} with Meta ads), ${data.flags.length} flags.`);

  const period = {
    id: PERIOD_ID,
    label: 'October 2026',
    metaAds: `/data/periods/${PERIOD_ID}/shared/Meta Ads.csv`,
    promoCodes: `/data/periods/${PERIOD_ID}/shared/Promo codes.csv`,
    clients,
  };
  const outDir = path.join(ROOT, 'public', 'data', 'snapshots');
  fs.mkdirSync(outDir, { recursive: true });
  fs.writeFileSync(path.join(outDir, 'october-2026.json'), JSON.stringify({ period, data }, null, 2), 'utf8');
  console.log(`Wrote ${path.join(outDir, 'october-2026.json')}`);
}

main().catch((err) => { console.error('October snapshot failed:', err); process.exit(1); });
