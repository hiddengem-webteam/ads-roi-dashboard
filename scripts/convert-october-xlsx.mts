// Converts the seven AM October 2026 workbooks (Drive folder
// 1j60vQGko77QVfzXVgZLxezNfBYmriyb4, downloaded to Monthly Data/2026-10 October)
// into per-client PMS CSVs. Same approach as the September converter (header
// synonyms inside the contiguous header block around the Revenue column), plus:
//   • "Promo Code" header accepted as the code column (Starlight x2, Bison Ridge)
//   • Hospitable exports with no code column (Anna: The Outpost, Ponderosa,
//     Walden) carry the code inside the "Guest discount" text, e.g.
//     "WELCOME10 - 2 nights ($47.50)" / "VIP10 (-$115.60)" / "Manager 25% ($74.75)":
//     the leading token is taken as the code when it looks like one (has a
//     digit, or is a registry code); manager discounts are ignored.
//   • pure numbers in the code column ("-83", "385", "25.74") are not codes
//   • Glasscombe (UK) dates are day-first
//
// Usage: npx tsx scripts/convert-october-xlsx.mts

import ExcelJS from 'exceljs';
import fs from 'fs';
import path from 'path';

const ROOT = path.resolve(import.meta.dirname, '..');
const SRC = path.join(ROOT, 'Monthly Data', '2026-10 October');
const OUT = path.join(ROOT, 'public', 'data', 'periods', 'october-2026', 'xlsx-source');

const FILES = ['Chiara October.xlsx', 'Nicole October.xlsx', 'Makenna October.xlsx', 'Kristal October.xlsx', 'Charlotte October.xlsx', 'Anna October.xlsx', 'Alicia October.xlsx'];

// Tab name → canonical dashboard client name, applied AFTER stripping the
// "- Updated"/"-Update" suffixes the AMs append.
const TAB_TO_CLIENT: Record<string, string> = {
  'Stayon30a': 'Stay on 30a',
  'HomeBase': 'Home Base',
  'Taberg Falls': 'Tàberg Falls',
  'Taberg': 'Tàberg Falls',
  'Columbia Gorge etaways': 'Columbia Gorge Getaways', // tab-name typo, Oct 2026
  'Hiawassee': 'Hiawassee Glamping',
  'FLOHOM': 'Flohom',
};
// Charlotte's "Redo Starlight Haven ..." tabs are all-source exports (OTA rows
// included, no Source column) and Kristal's "reservations (7).csv" is the raw
// Nature Nooks export behind the filtered Nature Nooks tab — neither is a client.
const SKIP_TABS = new Set<string>(['Redo Starlight Haven HS', 'Redo Starlight Haven WL', 'reservations (7).csv']);
const DAY_FIRST_CLIENTS = new Set<string>(['Glasscombe']);

// Registry codes (data/promo-codes.csv column 3), for recognising codes
// embedded in Hospitable "Guest discount" text.
const REGISTRY_CODES = new Set<string>(
  fs.readFileSync(path.join(ROOT, 'data', 'promo-codes.csv'), 'utf8').split(/\r?\n/).slice(1)
    .map((l) => (l.split(',')[2] ?? '').trim().toUpperCase()).filter(Boolean),
);
/** "WELCOME10 - 2 nights ($47.50)" → {code:'WELCOME10', discount:47.5}; "Manager 25% ($74.75)" → null. */
function codeFromDiscountText(v: unknown): { code: string; discount: number } | null {
  if (typeof v !== 'string') return null;
  const t = v.trim();
  if (!t || /^[\d.,$\-\s]+$/.test(t)) return null;
  // Anna's re-export (Nov 2026) puts the code last: "Walden Subscriber
  // Discount -$94.20 (WELCOME10)". Prefer a trailing "(CODE)" token.
  const trailing = t.match(/\(\s*([A-Za-z][A-Za-z0-9]*)\s*\)\s*$/);
  if (trailing) {
    const code = trailing[1].toUpperCase();
    if (!NOT_A_CODE.test(code) && (/\d/.test(code) || REGISTRY_CODES.has(code))) {
      const am = t.match(/-?\s*\$\s*([\d,]+(?:\.\d+)?)/);
      return { code, discount: am ? Number(am[1].replace(/,/g, '')) || 0 : 0 };
    }
  }
  const token = t.split(/[\s(/]/)[0].toUpperCase();
  if (!token || NOT_A_CODE.test(token)) return null;
  if (!/\d/.test(token) && !REGISTRY_CODES.has(token)) return null;
  const dm = t.match(/\(\s*-?\s*\$?\s*([\d,]+(?:\.\d+)?)\s*\)/);
  return { code: token, discount: dm ? Number(dm[1].replace(/,/g, '')) || 0 : 0 };
}

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

interface ColMap { guest: number[]; email: number; revenue: number; date: number; code: number; discount: number; source: number; status: number }

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
  const code = find('discount code', 'coupon name', 'promo code');
  const discount = find('coupon discount', 'guest_discount', 'guest discount', 'guest discount + code', 'discounts', 'promotionstotal', 'discount');
  const source = find('source', 'platform', 'listing site', 'channel', 'booking source', 'listing source');
  const status = find('status');
  return { guest, email, revenue, date, code, discount, source, status };
}

const NOT_A_CODE = /^(no coupon|no promo|none|n\/a|na|-+|0|-?\d+(?:\.\d+)?)$/i;
// The AM tabs are meant to list direct bookings only, but some October tabs
// are full PMS exports: Sunapee Stays and Stay Southern Illinois carry Airbnb /
// Vrbo / Booking.com rows, Asheville River Cabins and Tàberg carry cancelled
// bookings. Neither is direct revenue, so they are dropped here (counted in
// the summary line).
const OTA_SOURCE = /airbnb|vrbo|booking\.com|bookingcom|expedia|homeaway|tripadvisor|hotels\.com|agoda|google vacation/i;
const CANCELLED = /cancel/i;

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
      let otaRows = 0, otaRev = 0, cancelledRows = 0, cancelledRev = 0;
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
        const source = cols.source >= 0 ? String(vals[cols.source] ?? '').trim() : '';
        if (source && OTA_SOURCE.test(source)) { otaRows++; otaRev += revenue; continue; }
        const status = cols.status >= 0 ? String(vals[cols.status] ?? '').trim() : '';
        if (status && CANCELLED.test(status)) { cancelledRows++; cancelledRev += revenue; continue; }
        const email = cols.email >= 0 ? String(vals[cols.email] ?? '').trim() : '';
        let rawDate = cols.date >= 0 ? vals[cols.date] : '';
        if (DAY_FIRST_CLIENTS.has(client) && typeof rawDate === 'string') {
          const m = rawDate.match(/^(\d{1,2})\/(\d{1,2})\/(\d{4})/);
          if (m) rawDate = `${m[3]}-${m[2].padStart(2, '0')}-${m[1].padStart(2, '0')}`;
        }
        const date = cols.date >= 0 ? asDate(rawDate) : '';
        let discount = cols.discount >= 0 ? Math.abs(Number(vals[cols.discount] ?? 0) || 0) : inlineDiscount;
        // Hospitable exports (Anna's tabs): no code column, code lives in the
        // "Guest discount" text.
        if (!code && cols.code < 0 && cols.discount >= 0) {
          const parsed = codeFromDiscountText(vals[cols.discount]);
          if (parsed) { code = parsed.code; discount = parsed.discount; }
        }
        outRows.push([guest, email, revenue, date, code, discount || '', source]);
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
      if (otaRows) console.log(`${client}: dropped ${otaRows} OTA-sourced rows ($${otaRev.toFixed(2)})`);
      if (cancelledRows) console.log(`${client}: dropped ${cancelledRows} cancelled rows ($${cancelledRev.toFixed(2)})`);

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
