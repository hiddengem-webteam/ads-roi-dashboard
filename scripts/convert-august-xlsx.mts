// Converts the six AM August 2026 workbooks (downloaded from the Drive
// "August 2026" folder) into per-client PMS CSVs the dashboard pipeline
// understands. The AMs standardized on "Revenue" + "Discount Code" columns
// (per Shawal, Sep 2026), so detection is header-name based with a small set
// of legacy synonyms. Output: public/data/periods/august-2026/xlsx-source/.
//
// Special tabs handled separately:
//   • American River Resort — discounts-only ledger (no booking amounts):
//     promo uses are extracted like July (revenue back-computed from the 20%
//     new-guest discount); full revenue lives in the client reporting sheet.
//   • Sunapee Stays — main table + "Promo code usage" side table.
//
// Usage: npx tsx scripts/convert-august-xlsx.mts

import ExcelJS from 'exceljs';
import fs from 'fs';
import path from 'path';

const ROOT = path.resolve(import.meta.dirname, '..');
const SRC = path.join(ROOT, 'August 2026 PMS Data');
const OUT = path.join(ROOT, 'public', 'data', 'periods', 'august-2026', 'xlsx-source');

const FILES = ['Chiara August.xlsx', 'Makenna August.xlsx', 'Nicole August.xlsx', 'Anna August.xlsx', 'Charlotte August.xlsx', 'Alicia August.xlsx'];

// Tab name → canonical dashboard client name (identity when omitted).
const TAB_TO_CLIENT: Record<string, string> = {
  'Stay Southern Illinois': 'Stay Southen Illinois',
  'Stayon30a': 'Stay on 30a',
  'StaywithBranch': 'Stay with Branch',
  'HomeBase': 'Home Base',
  'BigMoonRanch': 'Big Moon Ranch',
  'Evergreen Cabins Updated': 'Evergreen Cabins',
  'StayLuxe - Updated': 'StayLuxe',
  'Endless Stays - Updated': 'Endless Stays',
  'Red White & Blue Views - Update': 'Red White & Blue Views',
  'Best Texas Travel - Updated': 'Best Texas Travel',
  'FLOHOM': 'Flohom',
  'Hiawassee': 'Hiawassee Glamping',
  'Starlight Haven HS': 'Starlight Haven Hot Springs',
  'Starlight Haven WL': 'Starlight Haven Weiss Lake',
  'Sunapee Stays': 'Sunapee Stays',
};
const SKIP_TABS = new Set([
  // ARR's old discounts-only ledger — superseded Sep 2 by a real per-booking
  // "American River Resort" tab (Invoice/Customer/Email/Revenue/Discount Code)
  // that the generic path handles. Guard kept in case the ledger returns.
  'American River Resort - Updated',
  'Sheet14', // scratch tab in Nicole's workbook (formula objects, no client)
]);

function cellVal(v: unknown): unknown {
  if (v && typeof v === 'object' && !(v instanceof Date)) {
    const o = v as Record<string, unknown>;
    // hyperlink cells can nest: { text: { richText: [...] }, hyperlink } —
    // unwrap recursively until a primitive falls out
    if ('result' in o) return cellVal(o.result);
    if ('richText' in o) return (o.richText as { text: string }[]).map((t) => t.text).join('');
    if ('text' in o) return cellVal(o.text);
  }
  return v;
}

function asDate(v: unknown): string {
  if (v instanceof Date) return v.toISOString().slice(0, 10);
  const s = String(v ?? '').trim();
  if (/^\d{4}-\d{2}-\d{2}/.test(s)) return s.slice(0, 10);
  const m = s.match(/^(\d{1,2})\/(\d{1,2})\/(\d{2,4})/);
  if (m) {
    const y = m[3].length === 2 ? '20' + m[3] : m[3];
    return `${y}-${m[1].padStart(2, '0')}-${m[2].padStart(2, '0')}`;
  }
  const d = new Date(s);
  return isNaN(d.getTime()) ? '' : d.toISOString().slice(0, 10);
}

function csvCell(v: unknown): string {
  const s = v === null || v === undefined ? '' : String(v);
  if (/[",\n]/.test(s)) return '"' + s.replace(/"/g, '""') + '"';
  return s;
}

interface ColMap { guest: number[]; email: number; revenue: number; date: number; code: number; discount: number }

function detectCols(hdr: string[]): ColMap | null {
  const H = hdr.map((h) => h.trim().toLowerCase());
  const find = (...names: string[]) => {
    for (const n of names) {
      const i = H.findIndex((h) => h === n);
      if (i >= 0) return i;
    }
    return -1;
  };
  const revenue = find('revenue', 'total paid');
  if (revenue < 0) return null;

  // guest: single column or first+last pair
  const guestSingle = find('guest', 'guest name', 'name', 'customer');
  const first = find('first name', 'guest first name', 'guest_first_name');
  const last = find('last name', 'guest last name', 'guest_last_name');
  const email = H.findIndex((h) => /email/.test(h) && !/platform/.test(h));
  let guest: number[] = guestSingle >= 0 ? [guestSingle] : first >= 0 ? (last >= 0 ? [first, last] : [first]) : [];
  if (guest.length === 0 && email >= 0) guest = [email]; // e.g. Big Moon Ranch: email-only sheet
  if (guest.length === 0) return null;
  const date = find(
    'check-in', 'check-in date', 'start date', 'arrival',
    'booked', 'booked on', 'booked at', 'booking_date', 'booking date',
    'reserved on', 'reservation date', 'creation date', 'datecreated',
  );
  const code = find('discount code', 'coupon name');
  const discount = find('coupon discount', 'guest_discount', 'guest discount', 'discounts', 'promotionstotal', 'discount');
  return { guest, email, revenue, date, code, discount };
}

const NOT_A_CODE = /^(no coupon|no promo|none|n\/a|na|-+|0)$/i;

async function main() {
  fs.rmSync(OUT, { recursive: true, force: true });
  fs.mkdirSync(OUT, { recursive: true });
  const report: Record<string, { rows: number; revenue: number; coded: number; codes: Record<string, number> }> = {};

  for (const file of FILES) {
    const wb = new ExcelJS.Workbook();
    await wb.xlsx.readFile(path.join(SRC, file));
    for (const ws of wb.worksheets) {
      const tab = ws.name.trim();
      if (SKIP_TABS.has(tab)) {
        if (tab === 'American River Resort - Updated') {
          report['American River Resort'] = await convertAmericanRiverResort(ws);
        }
        continue;
      }
      const client = TAB_TO_CLIENT[tab] ?? tab;

      // header row = first row (within 3) whose cells include 'Revenue'/'Total paid'
      let hdrRowIdx = 0;
      let cols: ColMap | null = null;
      for (let r = 1; r <= Math.min(3, ws.rowCount); r++) {
        const hdr = (ws.getRow(r).values as unknown[]).map((x) => String(cellVal(x) ?? ''));
        const mapped = detectCols(hdr);
        if (mapped) { hdrRowIdx = r; cols = mapped; break; }
      }
      if (!cols) { console.warn(`SKIP ${file} / ${tab} — no Revenue column found`); continue; }

      const outRows: unknown[][] = [];
      let total = 0, count = 0, coded = 0, discounted = 0;
      const codes: Record<string, number> = {};

      for (let r = hdrRowIdx + 1; r <= ws.rowCount; r++) {
        const vals = (ws.getRow(r).values as unknown[]).map(cellVal);
        const guest = cols.guest.map((i) => String(vals[i] ?? '').trim()).filter(Boolean).join(' ');
        const revenue = Number(vals[cols.revenue] ?? NaN);
        let code = cols.code >= 0 ? String(vals[cols.code] ?? '').trim() : '';
        if (!code || NOT_A_CODE.test(code)) code = '';
        code = code.toUpperCase();
        // Hiawassee's Sep 2 sheet drag-filled WELCOME50 into WELCOME51…58 (plus
        // a WELCOM50 typo) — every one is a −$50 discount, all the same code.
        if (client === 'Hiawassee Glamping') code = code.replace(/^WELCOME?5\d$/, 'WELCOME50');
        // ARR's Sep 2 tab: WELCOME20 drag-filled on a filtered view became
        // WELCOME21…WELCOME213 on the ~194 marked bookings (scattered rows,
        // strictly incrementing) — ARR's only registry code is WELCOME20.
        if (client === 'American River Resort') code = code.replace(/^WELCOME\d+$/, 'WELCOME20');
        // skip pivot/summary/empty/totals rows: a real guest contains letters
        // (SUM rows carry 0s or blanks in the guest column)
        if (!guest || !/[a-z]/i.test(guest) || (!Number.isFinite(revenue) && !code)) continue;
        if (!Number.isFinite(revenue)) continue;
        const email = cols.email >= 0 ? String(vals[cols.email] ?? '').trim() : '';
        const date = cols.date >= 0 ? asDate(vals[cols.date]) : '';
        const discount = cols.discount >= 0 ? Math.abs(Number(vals[cols.discount] ?? 0) || 0) : 0;
        outRows.push([guest, email, revenue, date, code, discount || '', '']);
        total += revenue; count++;
        if (code) { coded++; codes[code] = (codes[code] ?? 0) + 1; }
        if (discount > 0) discounted++;
      }

      // When a tab records discount amounts but never fills the code column
      // (e.g. Hiawassee: 14× −$50 with an empty "Discount Code" column), drop
      // the Coupon name column entirely so the pipeline's discount-amount
      // attribution matches the registry (WELCOME50 = $50 off) instead of
      // trusting an unused column.
      const dropCodeCol = coded === 0 && discounted > 0;
      const header = dropCodeCol
        ? 'Guest,Email,Revenue,Check-in date,Coupon discount,Source'
        : 'Guest,Email,Revenue,Check-in date,Coupon name,Coupon discount,Source';
      const lines = [header, ...outRows.map((r) => (dropCodeCol ? [...r.slice(0, 4), ...r.slice(5)] : r).map(csvCell).join(','))];
      if (dropCodeCol) console.log(`${client}: no codes but ${discounted} discounted rows — using amount-based attribution`);

      const dir = path.join(OUT, client);
      fs.mkdirSync(dir, { recursive: true });
      fs.writeFileSync(path.join(dir, 'PMS data.csv'), lines.join('\n') + '\n', 'utf8');
      report[client] = { rows: count, revenue: Math.round(total * 100) / 100, coded, codes };
    }
  }

  for (const [client, r] of Object.entries(report).sort()) {
    console.log(`${client}: ${r.rows} rows, $${r.revenue.toLocaleString('en-US')} | coded: ${r.coded} ${JSON.stringify(r.codes)}`);
  }
  console.log(`\n${Object.keys(report).length} clients written to ${OUT}`);
}

main().catch((err) => { console.error(err); process.exit(1); });
