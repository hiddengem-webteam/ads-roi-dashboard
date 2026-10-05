// Converts the seven AM September 2026 workbooks (Drive folder
// 1UsYxCWHtKkyPNvieqSCIBkXhAhoPDfik) into per-client PMS CSVs. Same approach
// as scripts/convert-august-xlsx.mts: header-synonym detection restricted to
// the contiguous header block around the Revenue column (ARR's September tab
// is a discounts ledger and a booking table side by side — the block guard
// picks the booking table).
//
// FLOHOM has no AM tab this month — its PMS csv is generated from the live
// HG AI roi-export by scripts/build-september-merged-snapshot.mts instead.
//
// Usage: npx tsx scripts/convert-september-xlsx.mts

import ExcelJS from 'exceljs';
import fs from 'fs';
import path from 'path';

const ROOT = path.resolve(import.meta.dirname, '..');
const SRC = path.join(ROOT, 'September 2026 PMS Data');
const OUT = path.join(ROOT, 'public', 'data', 'periods', 'september-2026', 'xlsx-source');

const FILES = ['Chiara September.xlsx', 'Nicole September.xlsx', 'Makenna September.xlsx', 'Kristal September.xlsx', 'Charlotte September.xlsx', 'Anna September.xlsx', 'Alicia September.xlsx'];

// Tab name → canonical dashboard client name, applied AFTER stripping the
// "- Updated"/"-Update" suffixes the AMs append.
const TAB_TO_CLIENT: Record<string, string> = {
  'Stay Southern Illinois': 'Stay Southen Illinois',
  'Stayon30a': 'Stay on 30a',
  'HomeBase': 'Home Base',
  'Taberg Falls': 'Tàberg Falls',
  'Hiawassee': 'Hiawassee Glamping',
  'FLOHOM': 'Flohom',
};
const SKIP_TABS = new Set<string>([]);

function cellVal(v: unknown): unknown {
  if (v && typeof v === 'object' && !(v instanceof Date)) {
    const o = v as Record<string, unknown>;
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
  // priority order matters: a tab can carry both "Revenue" and "Total"
  let revenue = -1;
  for (const n of ['revenue', 'total paid', 'total price', 'total']) {
    revenue = H.findIndex((h) => h === n);
    if (revenue >= 0) break;
  }
  if (revenue < 0) return null;

  // Restrict detection to the contiguous header block containing the Revenue
  // column so a side table (ARR's discounts ledger, Tuxedo's package list)
  // can't hijack the guest/email columns.
  let lo = revenue, hi = revenue;
  while (lo - 1 >= 1 && H[lo - 1]) lo--;
  while (hi + 1 < H.length && H[hi + 1]) hi++;
  const inBlock = (i: number) => i >= lo && i <= hi;
  const find = (...names: string[]) => {
    for (const n of names) {
      const i = H.findIndex((h, idx) => h === n && inBlock(idx));
      if (i >= 0) return i;
    }
    return -1;
  };

  // 'code' last: Oak & Ember's hostaway export has no guest column, only a
  // HOST-xxx booking reference named "code"
  const guestSingle = find('guest', 'guest name', 'name', 'customer', 'client', 'code');
  const first = find('first name', 'guest first name', 'guest_first_name');
  const last = find('last name', 'guest last name', 'guest_last_name');
  const email = H.findIndex((h, idx) => /email/.test(h) && !/platform/.test(h) && inBlock(idx));
  let guest: number[] = guestSingle >= 0 ? [guestSingle] : first >= 0 ? (last >= 0 ? [first, last] : [first]) : [];
  if (guest.length === 0 && email >= 0) guest = [email];
  if (guest.length === 0) return null;
  const date = find(
    'check-in', 'check-in date', 'checkin_date', 'checkin date', 'start date', 'arrival',
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
      const rawTab = ws.name.trim();
      if (SKIP_TABS.has(rawTab)) continue;
      // strip "- Updated" / "-Update" style suffixes, collapse double spaces
      const tab = rawTab.replace(/\s*-\s*Updated?$/i, '').replace(/\s{2,}/g, ' ').trim();
      const client = TAB_TO_CLIENT[tab] ?? tab;

      let hdrRowIdx = 0;
      let cols: ColMap | null = null;
      for (let r = 1; r <= Math.min(3, ws.rowCount); r++) {
        const hdr = (ws.getRow(r).values as unknown[]).map((x) => String(cellVal(x) ?? ''));
        const mapped = detectCols(hdr);
        if (mapped) { hdrRowIdx = r; cols = mapped; break; }
      }
      if (!cols) { console.warn(`SKIP ${file} / ${rawTab} — no Revenue column found`); continue; }

      const outRows: unknown[][] = [];
      let total = 0, count = 0, coded = 0, discounted = 0;
      const codes: Record<string, number> = {};

      // Tuxedo Falls appends a promo-use list below the booking table (per
      // Shawal, Oct 2026): rows with a guest name + code but NO revenue. Those
      // markers tag the matching main-table booking with the code; the marker
      // rows themselves stay excluded (no revenue to double count).
      const promoMarkers = new Map<string, { name: string; code: string }>();
      const norm = (s: string) => s.toLowerCase().replace(/[^a-z]/g, '');
      if (client === 'Tuxedo Falls' && cols.code >= 0) {
        for (let r = hdrRowIdx + 1; r <= ws.rowCount; r++) {
          const vals = (ws.getRow(r).values as unknown[]).map(cellVal);
          const name = String(vals[1] ?? '').trim();
          const mCode = String(vals[cols.code] ?? '').trim().toUpperCase();
          const rev = Number(vals[cols.revenue] ?? NaN);
          if (name && /[a-z]/i.test(name) && mCode && !NOT_A_CODE.test(mCode) && !Number.isFinite(rev)) {
            promoMarkers.set(norm(name), { name, code: mCode });
          }
        }
        if (promoMarkers.size) console.log(`Tuxedo Falls: ${promoMarkers.size} promo-use marker rows found`);
      }
      const consumedMarkers = new Set<string>();

      for (let r = hdrRowIdx + 1; r <= ws.rowCount; r++) {
        const vals = (ws.getRow(r).values as unknown[]).map(cellVal);
        const guest = cols.guest.map((i) => String(vals[i] ?? '').trim()).filter(Boolean).join(' ');
        const revenue = Number(vals[cols.revenue] ?? NaN);
        let code = cols.code >= 0 ? String(vals[cols.code] ?? '').trim() : '';
        // "WELCOME50 (-$50)" style: code with inline discount amount
        let inlineDiscount = 0;
        const dm = code.match(/^(.*?)\s*\(\s*-?\s*\$?\s*([\d,]+(?:\.\d+)?)\s*\)\s*$/);
        if (dm) { code = dm[1].trim(); inlineDiscount = Number(dm[2].replace(/,/g, '')) || 0; }
        if (!code || NOT_A_CODE.test(code)) code = '';
        code = code.toUpperCase();
        // Sheets drag-fill protection (seen in August: WELCOME50→WELCOME58 at
        // Hiawassee, WELCOME20→WELCOME213 at ARR): normalize incremented
        // variants of each client's sole registry code back to it.
        if (client === 'Hiawassee Glamping') code = code.replace(/^WELCOME?5\d$/, 'WELCOME50');
        if (client === 'American River Resort') code = code.replace(/^WELCOME\d+$/, 'WELCOME20');
        // Sunapee Sept: WELCOME10 drag-filled into WELCOME11…WELCOME20
        if (client === 'Sunapee Stays') code = code.replace(/^WELCOME(1\d|20)$/, 'WELCOME10');
        // promo-use marker from the list below the table: tag the matching
        // booking. Only a real booking row (finite revenue) consumes a marker —
        // the marker rows themselves also pass through here and must not.
        if (Number.isFinite(revenue) && promoMarkers.has(norm(guest))) {
          if (!code) code = promoMarkers.get(norm(guest))!.code;
          consumedMarkers.add(norm(guest));
        }
        // skip pivot/summary/empty/totals rows: a real guest contains letters
        if (!guest || !/[a-z]/i.test(guest) || (!Number.isFinite(revenue) && !code)) continue;
        if (!Number.isFinite(revenue)) continue;
        const email = cols.email >= 0 ? String(vals[cols.email] ?? '').trim() : '';
        const date = cols.date >= 0 ? asDate(vals[cols.date]) : '';
        const discount = cols.discount >= 0 ? Math.abs(Number(vals[cols.discount] ?? 0) || 0) : inlineDiscount;
        outRows.push([guest, email, revenue, date, code, discount || '', '']);
        total += revenue; count++;
        if (code) { coded++; codes[code] = (codes[code] ?? 0) + 1; }
        if (discount > 0) discounted++;
      }

      // Markers whose guest has no booking row this month (they booked in a
      // prior month with the code): keep them as zero-revenue uses so the use
      // count matches the AM's list, without inventing revenue.
      for (const [key, m] of promoMarkers) {
        if (consumedMarkers.has(key)) continue;
        outRows.push([`${m.name} (prior-month booking)`, '', 0, '', m.code, '', '']);
        coded++; codes[m.code] = (codes[m.code] ?? 0) + 1;
      }

      // No codes but discount amounts recorded → drop the code column so
      // amount-based attribution matches the registry (August: Hiawassee).
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
