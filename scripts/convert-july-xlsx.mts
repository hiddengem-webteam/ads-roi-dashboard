// One-off converter: turns the manually-compiled "July 2026 PMS Data/*.xlsx"
// workbooks (one sheet per client, wildly different export formats per
// account manager) into clean canonical "PMS data.csv" files per client,
// filtered to July 2026 check-in dates, written into
// public/data/periods/july-2026/clients/<name>/PMS data.csv.
//
// Reuses the REAL production parsePMSData() (same column-detection
// heuristics the live dashboard already relies on) rather than
// reimplementing per-sheet parsing — run through a File+FileReader polyfill
// since Papa.parse needs a browser FileReader for File input.
//
// Usage: npx tsx scripts/convert-july-xlsx.mts

import fs from 'fs';
import path from 'path';
import ExcelJS from 'exceljs';
import { parsePMSData } from '../src/lib/parsers/pmsData';

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
// @ts-expect-error - Node has no FileReader; polyfill enough for Papa.parse's FileStreamer path.
globalThis.FileReader = NodeFileReader;

const ROOT = path.resolve(import.meta.dirname, '..');
const SRC_DIR = path.join(ROOT, 'July 2026 PMS Data');
// Deliberately NOT public/data/periods/july-2026/clients/ — that's where the
// platform sync writes its own PMS data.csv per client, and macOS's default
// case-insensitive filesystem means "FLOHOM" and "Flohom" collide into the
// SAME directory. Writing here would silently overwrite the platform-synced
// (revenue/check-in authoritative) file. This is enrichment-only data (coupon/
// discount/source) that a separate merge step combines with the platform data.
const OUT_BASE = path.join(ROOT, 'public', 'data', 'periods', 'july-2026', 'xlsx-source');

// Sheets that aren't a real booking ledger for this period — skip explicitly.
// Myrinn is excluded: it has a manually-built override (scoped by booking date
// with a hand-verified guest list) that this generic per-sheet parse would
// otherwise clobber — see public/data/periods/july-2026/xlsx-source/Myrinn/.
const SKIP_SHEETS = new Set(['Starlight HS', 'Starlight WL', 'American River Resort ', 'Myrinn']);

function csvCell(v: unknown): string {
  const s = v === null || v === undefined ? '' : String(v);
  if (/[",\n]/.test(s)) return '"' + s.replace(/"/g, '""') + '"';
  return s;
}

function rowsToCSV(headers: string[], rows: unknown[][]): string {
  return [headers, ...rows].map((r) => r.map(csvCell).join(',')).join('\n') + '\n';
}

function excelDateToISO(v: unknown): string {
  if (v instanceof Date) return v.toISOString().slice(0, 10);
  return v === null || v === undefined ? '' : String(v);
}

// checkIn survives parsePMSData as whatever string was in the source cell —
// ISO ("2026-07-05"), US slash format ("07/31/2026"), a prose date
// ("Fri, Jul 10th 2026"), or an ISO datetime. Parse robustly rather than
// assuming one format everywhere across 6 different account managers' exports.
const MONTH_ABBR: Record<string, string> = {
  jan: '01', feb: '02', mar: '03', apr: '04', may: '05', jun: '06',
  jul: '07', aug: '08', sep: '09', oct: '10', nov: '11', dec: '12',
};

function isJuly2026(checkIn: string): boolean {
  if (!checkIn) return false;
  if (checkIn.startsWith('2026-07')) return true;
  const usMatch = checkIn.match(/^(\d{1,2})\/(\d{1,2})\/(\d{4})/);
  if (usMatch) {
    const [, mm, , yyyy] = usMatch;
    return yyyy === '2026' && mm === '07';
  }
  // "Fri, Jul 10th 2026" / "Jul 10, 2026" style
  const proseMatch = checkIn.match(/([a-zA-Z]{3,})[a-zA-Z]*\s+\d{1,2}(?:st|nd|rd|th)?,?\s+(\d{4})/);
  if (proseMatch) {
    const [, monthWord, yyyy] = proseMatch;
    const mm = MONTH_ABBR[monthWord.toLowerCase().slice(0, 3)];
    return mm === '07' && yyyy === '2026';
  }
  return false;
}

async function main() {
  const files = fs.readdirSync(SRC_DIR).filter((f) => f.endsWith('.xlsx'));
  const report: Record<string, unknown>[] = [];

  for (const file of files) {
    const wb = new ExcelJS.Workbook();
    await wb.xlsx.readFile(path.join(SRC_DIR, file));

    for (const ws of wb.worksheets) {
      const sheetName = ws.name;
      if (SKIP_SHEETS.has(sheetName)) {
        report.push({ file, sheet: sheetName, status: 'skipped (not a booking ledger)' });
        continue;
      }

      // Read all rows as arrays of cell values.
      const allRows: unknown[][] = [];
      ws.eachRow({ includeEmpty: false }, (row) => {
        const vals: unknown[] = [];
        row.eachCell({ includeEmpty: true }, (cell) => {
          const v = cell.value;
          vals.push(v && typeof v === 'object' && 'result' in v ? (v as { result: unknown }).result : v);
        });
        allRows.push(vals);
      });

      if (allRows.length === 0) {
        report.push({ file, sheet: sheetName, status: 'empty sheet — skipped' });
        continue;
      }

      // Find the real header row: skip a leading title-only row (<=1 non-empty cell).
      let headerIdx = 0;
      if (allRows[0].filter((v) => v !== null && v !== undefined && v !== '').length <= 1 && allRows.length > 1) {
        headerIdx = 1;
      }
      const headerRow = allRows[headerIdx].map((h) => (h === null || h === undefined ? '' : String(h).trim()));
      const dataRows = allRows.slice(headerIdx + 1).filter((r) => r.some((v) => v !== null && v !== undefined && v !== ''));

      if (dataRows.length === 0) {
        report.push({ file, sheet: sheetName, status: 'no data rows — skipped' });
        continue;
      }

      // Convert date cells to ISO strings so the downstream parser's checkIn field is filterable.
      const dataRowsIso = dataRows.map((r) => r.map((v) => (v instanceof Date ? excelDateToISO(v) : v)));

      const csv = rowsToCSV(headerRow, dataRowsIso);
      const csvFile = new File([csv], `${sheetName}.csv`, { type: 'text/csv' });

      let parsed;
      try {
        parsed = await parsePMSData(csvFile);
      } catch (err) {
        report.push({ file, sheet: sheetName, status: `parse error: ${err instanceof Error ? err.message : err}` });
        continue;
      }

      const totalRows = parsed.rows.length;
      const noDateRows = parsed.rows.filter((r) => !r.checkIn);
      // No usable date column at all (every row has an empty checkIn) — per
      // decision, trust that the account manager already scoped the sheet to
      // July and include everything rather than dropping the client entirely.
      const noDateColumnDetected = totalRows > 0 && noDateRows.length === totalRows;
      // Per decision: every row in every sheet is July data regardless of its
      // check-in/checkout/booking date — these sheets were each compiled by an
      // account manager specifically for July, so no date filter is applied.
      const julyRows = parsed.rows;
      void noDateColumnDetected; // kept only for the report's diagnostic field below
      const totalRevenue = julyRows.reduce((s, r) => s + r.revenue, 0);

      const clientName = sheetName.trim();
      const outDir = path.join(OUT_BASE, clientName);
      fs.mkdirSync(outDir, { recursive: true });

      const outHeaders = ['Guest', 'Email', 'Revenue', 'Check-in date', 'Coupon name', 'Coupon discount', 'Source'];
      const outRows = julyRows.map((r) => [r.guest, r.email, r.revenue, r.checkIn, r.couponName, r.couponDiscount, r.source]);
      fs.writeFileSync(path.join(outDir, 'PMS data.csv'), rowsToCSV(outHeaders, outRows), 'utf8');

      report.push({
        file,
        sheet: sheetName,
        status: 'ok',
        revenueColumn: parsed.revenueColumn,
        hasCouponColumn: parsed.hasCouponColumn,
        hasEmailColumn: parsed.hasEmailColumn,
        hasSourceColumn: parsed.hasSourceColumn,
        totalRowsParsed: totalRows,
        noDateColumnDetected,
        julyRows: julyRows.length,
        rowsWithNoDate: noDateRows.length,
        julyRevenue: Math.round(totalRevenue * 100) / 100,
      });
    }
  }

  console.log(JSON.stringify(report, null, 2));
  const outReportPath = path.join(ROOT, 'scripts', '.july-xlsx-conversion-report.json');
  fs.writeFileSync(outReportPath, JSON.stringify(report, null, 2), 'utf8');
  console.error(`\nReport written to ${outReportPath}`);
}

main().catch((err) => {
  console.error('Conversion failed:', err);
  process.exit(1);
});
