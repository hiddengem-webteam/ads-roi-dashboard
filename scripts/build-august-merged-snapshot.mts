// Builds the frozen August 2026 snapshot for /august — the MANUAL pipeline
// (per Shawal, Sep 2026: the automated platform PMS data had issues, so like
// July the account managers' sheets are authoritative for bookings/promo).
//
// Sources:
//   • PMS      — public/data/periods/august-2026/xlsx-source/<client>/ (from
//                scripts/convert-august-xlsx.mts over the six AM workbooks;
//                American River Resort is promo-uses-only, see converter notes)
//   • Meta Ads — the platform sync's august-2026 shared/Meta Ads.csv
//   • GHL      — the platform sync's august-2026 per-client GHL contact CSVs
//   • Promo    — data/promo-codes.csv (merged live from the CRM Google Sheet)
//
// Usage: npx tsx scripts/build-august-merged-snapshot.mts

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
const PERIOD_ID = 'august-2026';
const XLSX_SOURCE = path.join(ROOT, 'public', 'data', 'periods', PERIOD_ID, 'xlsx-source');
const PLATFORM_CLIENTS = path.join(ROOT, 'public', 'data', 'periods', PERIOD_ID, 'clients');
const PLATFORM_SHARED = path.join(ROOT, 'public', 'data', 'periods', PERIOD_ID, 'shared');

// xlsx-source client dir → platform client dir for GHL reuse, where names differ.
const GHL_DIR_ALIASES: Record<string, string> = {};

async function main() {
  const files: UploadedFilesMap = { metaAds: null, promoCodes: null, pmsFiles: {}, ghlFiles: {} };

  // Meta ads come EXCLUSIVELY from the manually exported Ads Manager Monthly
  // Report (August 2026/Meta ads - August 26.csv) — it covers every agency ad
  // account including the ones not connected to the platform (ARR, Tuxedo,
  // CGG, Oak & Ember, both Starlights). Account names are rewritten to exact
  // dashboard client names via this explicit map; unmapped accounts (Canopy,
  // VillaDestino, Edenwood, Cowan Creek, client-run Branch Berkeley Springs)
  // are deliberately left out.
  const REPORT_ACCOUNT_TO_CLIENT: Record<string, string> = {
    '@staywithbranch': 'Stay with Branch',
    'American River Resort': 'American River Resort',
    'Asheville River Cabins Ads': 'Asheville River Cabins',
    'Away2Pa': 'Away2PA',
    'Awayframes Ad Account': 'Awayframes',
    'Best Texas Travel Ad Account': 'Best Texas Travel',
    'Big Moon Ranch': 'Big Moon Ranch',
    'Bison Ridge Retreat Ad Account': 'Bison Ridge Retreat',
    'CGG': 'Columbia Gorge Getaways',
    'Endless Stays': 'Endless Stays',
    'Evergreen Cabins Ads': 'Evergreen Cabins',
    'FLOHOM Ads': 'Flohom',
    'Green Springs Inn': 'Green Springs Inn',
    'Hiawassee Glamping': 'Hiawassee Glamping',
    'Home Base bnbs': 'Home Base',
    'Inspired Retreats Ads 2.0': 'Inspired Retreats',
    'Myrinn - Ad Account 2.0': 'Myrinn',
    'Nature Nooks Ad Account': 'Nature Nooks',
    'Oak & Ember Ad Account': 'Oak & Ember',
    'Paradise Pointe Ads': 'Paradise Pointe',
    'Parker Reserve': 'Parker Reserve',
    'Ponderosa Pines Resort': 'Ponderosa Pines Resort',
    'Red White & Blue Views': 'Red White & Blue Views',
    'Selah.place': 'Selah Place',
    'Southern Illinois Cabins Ads': 'Stay Southen Illinois',
    'Starlight Haven Hot Springs': 'Starlight Haven Hot Springs',
    'Starlight Haven Weiss Lake - 74756899': 'Starlight Haven Weiss Lake',
    // 'Stay Different Ads' removed — client offboarded (per Shawal, Sep 3 2026)
    'Stay Luxe Ads': 'StayLuxe',
    'Stay Saluda Ads': 'Stay Saluda',
    'Stay on 30a Ads': 'Stay on 30a',
    'Sunapee Stays Ads Account': 'Sunapee Stays',
    'The Cohost Company Ads': 'The Cohost Company',
    'The Outpost Grand Canyon': 'The Outpost',
    'Three Suns Cabins Ad Account': 'Three Suns Cabins',
    'Treetop Escapes Ads': 'Treetop Escapes',
    'Tuxedo Falls - Ad Account': 'Tuxedo Falls',
    'Táberg Falls': 'Tàberg Falls',
    'TÃ¡berg Falls': 'Tàberg Falls', // mojibake variant in the export
  };

  const reportPath = path.join(ROOT, 'August 2026', 'Meta ads - August 26.csv');
  if (fs.existsSync(reportPath)) {
    const parsed = Papa.parse<Record<string, string>>(fs.readFileSync(reportPath, 'utf8'), {
      header: true,
      skipEmptyLines: true,
      transformHeader: (h) => h.replace(/^\ufeff/, '').trim(),
    });
    const num = (v: string | undefined) => (v && v.trim() ? Number(v) : 0);
    const rows: string[] = ['Account name,Campaign name,Amount spent,Link clicks,Leads,Impressions,Purchases,Purchases conversion value'];
    let mapped = 0, skipped = new Set<string>();
    for (const r of parsed.data) {
      const account = (r['Account name'] ?? '').trim();
      const campaign = (r['Campaign name'] ?? '').trim();
      if (!account) continue;
      let client = REPORT_ACCOUNT_TO_CLIENT[account];
      if (!client && account === 'HiddenGem Marketing' && /outpost/i.test(campaign)) client = 'The Outpost';
      if (!client) { skipped.add(account); continue; }
      const cells = [client, campaign, num(r['Amount spent (USD)']), num(r['Link clicks']), num(r['Leads']), num(r['Impressions']), num(r['Purchases']), num(r['Purchases conversion value'])];
      rows.push(cells.map((c) => (/[",\n]/.test(String(c)) ? '"' + String(c).replace(/"/g, '""') + '"' : String(c))).join(','));
      mapped++;
    }
    files.metaAds = new File([rows.join('\n') + '\n'], 'Meta Ads.csv', { type: 'text/csv' });
    console.log(`Meta ads: ${mapped} campaign rows mapped from the Monthly Report; skipped accounts: ${[...skipped].join(', ') || 'none'}`);
  } else {
    console.warn('Monthly Report CSV not found — falling back to the platform Meta Ads.csv.');
    const metaAdsPath = path.join(PLATFORM_SHARED, 'Meta Ads.csv');
    if (fs.existsSync(metaAdsPath)) files.metaAds = new File([fs.readFileSync(metaAdsPath)], 'Meta Ads.csv', { type: 'text/csv' });
  }

  const promoPath = path.join(ROOT, 'data', 'promo-codes.csv');
  if (fs.existsSync(promoPath)) {
    files.promoCodes = new File([fs.readFileSync(promoPath)], 'Promo codes.csv', { type: 'text/csv' });
  }

  const clients: { name: string; pms: string; ghl: string }[] = [];
  for (const name of fs.readdirSync(XLSX_SOURCE).sort()) {
    const pmsFile = path.join(XLSX_SOURCE, name, 'PMS data.csv');
    if (!fs.existsSync(pmsFile)) continue;
    files.pmsFiles[name] = new File([fs.readFileSync(pmsFile)], 'PMS data.csv', { type: 'text/csv' });

    const ghlDir = GHL_DIR_ALIASES[name] ?? name;
    const ghlFile = path.join(PLATFORM_CLIENTS, ghlDir, 'GHL data.csv');
    let ghlPath = '';
    if (fs.existsSync(ghlFile)) {
      files.ghlFiles[name] = new File([fs.readFileSync(ghlFile)], 'GHL data.csv', { type: 'text/csv' });
      ghlPath = `/data/periods/${PERIOD_ID}/clients/${ghlDir}/GHL data.csv`;
    }
    clients.push({ name, pms: `/data/periods/${PERIOD_ID}/xlsx-source/${name}/PMS data.csv`, ghl: ghlPath });
  }

  const data = await processAllData(files);
  const withPms = Object.values(data.clients).filter((c) => c.pmsAnalysis).length;
  const withFb = Object.values(data.clients).filter((c) => c.facebookStats).length;
  console.log(`Processed ${Object.keys(data.clients).length} clients (${withPms} with PMS, ${withFb} with Meta ads), ${data.flags.length} flags.`);

  const period = {
    id: PERIOD_ID,
    label: 'August 2026',
    metaAds: `/data/periods/${PERIOD_ID}/shared/Meta Ads.csv`,
    promoCodes: `/data/periods/${PERIOD_ID}/shared/Promo codes.csv`,
    clients,
  };
  const outDir = path.join(ROOT, 'public', 'data', 'snapshots');
  fs.mkdirSync(outDir, { recursive: true });
  fs.writeFileSync(path.join(outDir, 'august-2026.json'), JSON.stringify({ period, data }, null, 2), 'utf8');
  console.log(`Wrote ${path.join(outDir, 'august-2026.json')}`);
}

main().catch((err) => { console.error('August snapshot failed:', err); process.exit(1); });
