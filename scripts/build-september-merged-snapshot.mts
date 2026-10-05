// Builds the frozen September 2026 snapshot for /september — the MANUAL
// pipeline (AM sheets authoritative for bookings/promo, like July/August).
//
// Sources:
//   • PMS      — public/data/periods/september-2026/xlsx-source/<client>/
//                (from scripts/convert-september-xlsx.mts over the seven AM
//                workbooks). FLOHOM has no AM tab this month: its PMS csv is
//                generated here from the saved HG AI roi-export halves
//                (September 2026 PMS Data/roi-export-sept-{a,b}.json).
//   • Meta Ads — Sept Data/Monthly-Report (7).csv (Ads Manager export,
//                Sep 1–30, AD SET level → aggregated to campaign level here;
//                the blank-account grand-total row is used as a checksum).
//   • GHL      — the platform sync's september-2026 per-client GHL CSVs
//   • Promo    — data/promo-codes.csv (merged live from the CRM Google Sheet)
//
// SCOPE (per Shawal, Oct 2026): only clients visible in the Meta ads report
// get analyzed. AM tabs for clients absent from the report (e.g. Raven Rock
// Mountain) are skipped entirely.
//
// Usage: npx tsx scripts/build-september-merged-snapshot.mts

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
const PERIOD_ID = 'september-2026';
const XLSX_SOURCE = path.join(ROOT, 'public', 'data', 'periods', PERIOD_ID, 'xlsx-source');
const PLATFORM_CLIENTS = path.join(ROOT, 'public', 'data', 'periods', PERIOD_ID, 'clients');
const REPORT_PATH = path.join(ROOT, 'Sept Data', 'Monthly-Report (7).csv');
const FLOHOM_TENANT = '2a5a7022-03cb-4f9b-b4fd-2d650dbb2a1d';

// Account names exactly as they appear in the September export. Unmapped
// accounts are deliberately out (Edenwood NC is client-run; Canopy etc. gone).
const REPORT_ACCOUNT_TO_CLIENT: Record<string, string> = {
  '@staywithbranch': 'Stay with Branch',
  'American River Resort': 'American River Resort',
  'Asheville River Cabins Ads': 'Asheville River Cabins',
  'Away2Pa': 'Away2PA',
  'Awayframes Ad Account': 'Awayframes',
  'Best Texas Travel Ad Account': 'Best Texas Travel',
  'Bison Ridge Retreat Ad Account': 'Bison Ridge Retreat',
  'CGG': 'Columbia Gorge Getaways',
  'Endless Stays': 'Endless Stays',
  'Evergreen Cabins Ads': 'Evergreen Cabins',
  'FLOHOM Ads': 'Flohom',
  'Green Springs Inn': 'Green Springs Inn',
  'Hiawassee Glamping': 'Hiawassee Glamping',
  'Home Base bnbs': 'Home Base',
  'Inspired Retreats Ads 2.0': 'Inspired Retreats',
  'Little River Landing': 'Little River Landing',
  'Myrinn - Ad Account 2.0': 'Myrinn',
  'Nature Nooks Ad Account': 'Nature Nooks',
  'North Star Lodge & Resort Ads': 'North Star Lodge & Resort',
  'Oak & Ember Ad Account': 'Oak & Ember',
  'Paradise Pointe Ads': 'Paradise Pointe',
  'Parker Reserve': 'Parker Reserve',
  'Ponderosa Pines Resort': 'Ponderosa Pines Resort',
  'Red White & Blue Views': 'Red White & Blue Views',
  'Ridge & Falls ad account': 'Ridge & Falls',
  'Selah.place': 'Selah Place',
  'Southern Illinois Cabins Ads': 'Stay Southen Illinois',
  'Starlight Haven Hot Springs': 'Starlight Haven Hot Springs',
  'Starlight Haven Weiss Lake - 74756899': 'Starlight Haven Weiss Lake',
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
  'TÃ¡berg Falls': 'Tàberg Falls', // mojibake variant
};

function csvCell(v: unknown): string {
  const s = v === null || v === undefined ? '' : String(v);
  if (/[",\n]/.test(s)) return '"' + s.replace(/"/g, '""') + '"';
  return s;
}

/** FLOHOM PMS csv from the saved roi-export halves (live HG AI PMS data). */
function generateFlohomPms(): void {
  const dir = path.join(XLSX_SOURCE, 'Flohom');
  const halves = ['roi-export-sept-a.json', 'roi-export-sept-b.json']
    .map((f) => path.join(ROOT, 'September 2026 PMS Data', f));
  if (!halves.every((f) => fs.existsSync(f))) {
    console.warn('FLOHOM roi-export halves missing — Flohom will be ads-only.');
    return;
  }
  const lines = ['Guest,Email,Revenue,Check-in date,Coupon name,Coupon discount,Source'];
  let total = 0, n = 0;
  for (const f of halves) {
    const tenants = JSON.parse(fs.readFileSync(f, 'utf8')).tenants as Record<string, {
      direct_bookings?: { guest?: string; email?: string; revenue?: number; check_in?: string; coupon_code?: string; discount_amount?: number }[];
    }>;
    for (const bk of tenants[FLOHOM_TENANT]?.direct_bookings ?? []) {
      const rev = Number(bk.revenue ?? 0) || 0;
      lines.push([
        bk.guest ?? '', bk.email ?? '', rev, (bk.check_in ?? '').slice(0, 10),
        (bk.coupon_code ?? '').toUpperCase(), bk.discount_amount ? Math.abs(Number(bk.discount_amount)) : '', '',
      ].map(csvCell).join(','));
      total += rev; n++;
    }
  }
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, 'PMS data.csv'), lines.join('\n') + '\n', 'utf8');
  console.log(`Flohom (from HG AI roi-export): ${n} bookings, $${Math.round(total * 100) / 100}`);
}

async function main() {
  generateFlohomPms();

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
  // Manual adjustment (per Shawal, Oct 5 2026): Meta recorded 12 Paradise
  // Pointe purchases in Sep (10 in the 09/15–21 week, 2 in 09/29–30) with NO
  // conversion value on the "Website, IG & FB Engagers" ad set. Add them at
  // the September avg direct booking value (12 × $1,170.59 = $14,047.08).
  const pp = byCampaign.get('Paradise Pointe\u0000BoF - Sales Campaign - Retargeting Website Visitors');
  if (pp) {
    pp.conv += 12 * 1170.59;
    console.log('Manual adjustment: Paradise Pointe BoF RT conversion value +$14,047.08 (12 unvalued purchases × $1,170.59 avg booking).');
  } else {
    console.warn('Manual adjustment target not found: Paradise Pointe BoF RT campaign.');
  }

  const rows: string[] = ['Account name,Campaign name,Amount spent,Link clicks,Leads,Impressions,Purchases,Purchases conversion value'];
  for (const e of byCampaign.values()) {
    rows.push([e.client, e.campaign, e.spend, e.clicks, e.leads, e.impressions, e.purchases, e.conv].map(csvCell).join(','));
  }
  files.metaAds = new File([rows.join('\n') + '\n'], 'Meta Ads.csv', { type: 'text/csv' });
  console.log(`Meta ads: ${byCampaign.size} campaigns from ${parsed.data.length} ad-set rows; mapped $${mappedSpend.toFixed(2)} vs export total $${grandTotal.toFixed(2)}; skipped accounts: ${[...skipped].join(', ') || 'none'}`);

  const promoPath = path.join(ROOT, 'data', 'promo-codes.csv');
  if (fs.existsSync(promoPath)) {
    files.promoCodes = new File([fs.readFileSync(promoPath)], 'Promo codes.csv', { type: 'text/csv' });
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
    label: 'September 2026',
    metaAds: `/data/periods/${PERIOD_ID}/shared/Meta Ads.csv`,
    promoCodes: `/data/periods/${PERIOD_ID}/shared/Promo codes.csv`,
    clients,
  };
  const outDir = path.join(ROOT, 'public', 'data', 'snapshots');
  fs.mkdirSync(outDir, { recursive: true });
  fs.writeFileSync(path.join(outDir, 'september-2026.json'), JSON.stringify({ period, data }, null, 2), 'utf8');
  console.log(`Wrote ${path.join(outDir, 'september-2026.json')}`);
}

main().catch((err) => { console.error('September snapshot failed:', err); process.exit(1); });
