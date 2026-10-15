/**
 * Sync the repo's finalized numbers, weekly review rows and decisions into the
 * `roi` schema of the HGM Reporting Supabase project, so past months and past
 * decisions can be queried (by Claude or anyone with SQL) instead of re-read
 * from files.
 *
 *   npx tsx scripts/sync-roi-memory.mts              upsert over REST (needs env below)
 *   npx tsx scripts/sync-roi-memory.mts --dry-run    parse only, print row counts
 *   npx tsx scripts/sync-roi-memory.mts --emit-sql   print upsert SQL to stdout
 *   npx tsx scripts/sync-roi-memory.mts --emit-sql --seed
 *        slim SQL for a first load through the Supabase connector: no raw/campaigns
 *        JSON, no weekly CSV rows, weekly-report notes carry a pointer instead of
 *        the full text. A later full run (REST or --emit-sql) overwrites all of it.
 *
 * Env (.env.local): SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY for the HGM
 * Reporting project (ytewxihtllthqkvnmlex). The service role key is required
 * because the roi tables have RLS on with no anon policies.
 *
 * Sources (all in-repo, all idempotent upserts keyed as the tables define):
 *   weekly/Monthly ROI data/*.json                      -> roi.monthly_client_metrics, roi.notes (am-note)
 *   weekly/Ad Spends Checks/Weekly Checks/*.csv         -> roi.weekly_ad_spend_checks
 *   weekly/Meta Pixel Reviews/Weekly Checks/*.csv       -> roi.weekly_pixel_checks
 *   weekly/Client Benchmark Reviews (...)/Weekly Checks/*.csv -> roi.weekly_benchmark_rows
 *   weekly/Project Data/PROJECT.md  sections 6, 7, 8, 9 -> roi.notes (learning), roi.decisions, roi.run_log, roi.actions_log
 *   weekly/HG AI Reports/*.md                            -> roi.notes (hg-ai-report)
 *   weekly/<workflow>/Weekly Checks/*.md                 -> roi.notes (weekly-report, full text)
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import Papa from 'papaparse';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const WEEKLY = path.join(ROOT, 'weekly');
const MODE = process.argv.includes('--emit-sql') ? 'sql' : process.argv.includes('--dry-run') ? 'dry' : 'rest';
const SEED = process.argv.includes('--seed');

// Load .env.local / .env (real env vars take precedence, like Next).
for (const file of ['.env.local', '.env']) {
  const p = path.join(ROOT, file);
  if (!fs.existsSync(p)) continue;
  for (const raw of fs.readFileSync(p, 'utf8').split('\n')) {
    const line = raw.trim();
    if (!line || line.startsWith('#')) continue;
    const eq = line.indexOf('=');
    if (eq < 0) continue;
    const key = line.slice(0, eq).trim();
    const val = line.slice(eq + 1).trim().replace(/^"(.*)"$/, '$1');
    if (!(key in process.env)) process.env[key] = val;
  }
}

type Row = Record<string, unknown>;
type Batches = Record<string, Row[]>;

const num = (v: unknown): number | null => {
  if (v === null || v === undefined || v === '') return null;
  const n = Number(String(v).replace(/[$,]/g, ''));
  return Number.isFinite(n) ? n : null;
};
const int = (v: unknown): number | null => {
  const n = num(v);
  return n === null ? null : Math.round(n);
};
const str = (v: unknown): string | null => (v === null || v === undefined || v === '' ? null : String(v));

function listFiles(dir: string, re: RegExp): string[] {
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir).filter((f) => re.test(f)).sort().map((f) => path.join(dir, f));
}

function readCsv(file: string): Row[] {
  const text = fs.readFileSync(file, 'utf8').replace(/^﻿/, '');
  const parsed = Papa.parse<Row>(text, { header: true, skipEmptyLines: true });
  return parsed.data;
}

// ---------------------------------------------------------------- monthly
function monthly(b: Batches) {
  for (const file of listFiles(path.join(WEEKLY, 'Monthly ROI data'), /\.json$/)) {
    const d = JSON.parse(fs.readFileSync(file, 'utf8'));
    const rel = path.relative(ROOT, file);
    for (const c of d.clients ?? []) {
      b.monthly_client_metrics.push({
        period_id: d.periodId,
        period_label: d.period,
        client: c.clientName,
        note: str(c.note),
        revenue_source: str(c.revenueSource),
        total_direct_bookings: int(c.totalDirectBookings),
        total_direct_booking_revenue: num(c.totalDirectBookingRevenue),
        total_leads: int(c.totalLeads),
        leads_source: str(c.leadsSource),
        meta_ad_spend: num(c.overallMetaAdSpend),
        bookings_attributed_to_meta: int(c.totalBookingsAttributedToMeta),
        cost_per_meta_booking: num(c.costPerMetaAttributedBooking),
        avg_direct_booking_value: num(c.avgDirectBookingValue),
        meta_attributed_revenue: num(c.directBookingRevenueAttributedToMeta),
        meta_attributed_revenue_capped: c.metaAttributedRevenueCappedAtTotal ?? null,
        blended_roas: num(c.blendedRoas ?? c.roas),
        campaigns: SEED ? null : (c.campaigns ?? null),
        raw: SEED ? {} : c,
        source_file: rel,
      });
      if (c.note) {
        b.notes.push({
          id: `am-note:${d.periodId}:${c.clientName}`,
          kind: 'am-note',
          note_date: null,
          client: c.clientName,
          title: `${c.clientName} · ${d.period} note`,
          body: String(c.note),
          source_file: rel,
        });
      }
    }
  }
}

// ---------------------------------------------------------------- weekly csv
function weekly(b: Batches) {
  const specs: [string, string, RegExp, (r: Row) => Row][] = [
    ['weekly_ad_spend_checks', 'Ad Spends Checks/Weekly Checks', /-ad-spend-check\.csv$/, (r) => ({
      run_date: r.run_date, client: r.client, am: str(r.am), ad_account_id: str(r.ad_account_id) ?? '',
      // Two formats: up to 2026-10-13 sheet-vs-live (sheet_status, flag, diff_status, notes);
      // from 2026-10-15 the live ledger (total_live, status, what_changed, campaigns, per-type columns).
      sheet_status: str(r.sheet_status), sheet_daily_budget: num(r.sheet_daily_budget), actual_daily_budget: num(r.actual_daily_budget ?? r.total_live),
      spend_7d: num(r.spend_7d), source: str(r.source), flag: str(r.flag ?? r.status), diff_status: str(r.diff_status ?? r.status),
      weeks_open: int(r.weeks_open), notes: str(r.notes ?? (r.what_changed ? `${r.what_changed} | ${r.campaigns}` : r.campaigns)),
    })],
    ['weekly_pixel_checks', 'Meta Pixel Reviews/Weekly Checks', /-pixel-domain-check\.csv$/, (r) => ({
      run_date: r.run_date, client: r.client, pixel_id: str(r.pixel_id) ?? '', pixel_name: str(r.pixel_name),
      ad_account_id: str(r.ad_account_id), events_7d: int(r.events_7d), server_events: str(r.server_events),
      domains_seen: str(r.domains_seen), expected_domains: str(r.expected_domains), expected_source: str(r.expected_source),
      flag: str(r.flag), diff_status: str(r.diff_status), weeks_open: int(r.weeks_open), notes: str(r.notes),
    })],
    ['weekly_benchmark_rows', 'Client Benchmark Reviews (advanced setups)/Weekly Checks', /-client-benchmark\.csv$/, (r) => ({
      run_date: r.run_date, client: r.client, campaign: str(r.campaign) ?? '', am: str(r.am), ad_account_id: str(r.ad_account_id),
      campaign_id: str(r.campaign_id), type: str(r.type), window_days: int(r.window_days), source: str(r.source),
      spend: num(r.spend), results: str(r.results), governing_metric: str(r.governing_metric), governing_value: num(r.governing_value),
      state: str(r.state), diagnostics: str(r.diagnostics), diff_status: str(r.diff_status), weeks_open: int(r.weeks_open),
      notes: str(r.notes), frequency: num(r.frequency), freq_flag: str(r.freq_flag),
    })],
  ];
  for (const [table, folder, re, map] of specs) {
    // Primary-key collision inside one file (e.g. two rows for one campaign) keeps the last.
    const keyCols = CONFLICT[table].split(',').map((c) => c.trim());
    const byKey = new Map<string, Row>();
    for (const file of listFiles(path.join(WEEKLY, folder), re)) {
      for (const r of readCsv(file)) {
        if (!r.run_date || !r.client) continue;
        const row = { ...map(r), raw: SEED ? {} : r };
        byKey.set(JSON.stringify(keyCols.map((c) => row[c])), row);
      }
    }
    b[table].push(...byKey.values());
  }
}

// ---------------------------------------------------------------- PROJECT.md
function section(md: string, heading: RegExp): string {
  const lines = md.split('\n');
  const start = lines.findIndex((l) => heading.test(l));
  if (start < 0) return '';
  let end = lines.length;
  for (let i = start + 1; i < lines.length; i++) if (/^## /.test(lines[i])) { end = i; break; }
  return lines.slice(start + 1, end).join('\n');
}
function tableRows(block: string): string[][] {
  const rows: string[][] = [];
  for (const line of block.split('\n')) {
    if (!line.trim().startsWith('|')) continue;
    const cells = line.trim().slice(1, -1).split('|').map((c) => c.trim());
    if (cells.every((c) => /^-+$/.test(c))) continue;
    rows.push(cells);
  }
  return rows.slice(1); // drop header
}
const isoDate = (s: string): string | null => (/^\d{4}-\d{2}-\d{2}$/.test(s) ? s : null);

function projectMd(b: Batches) {
  const file = path.join(WEEKLY, 'Project Data', 'PROJECT.md');
  if (!fs.existsSync(file)) return;
  const md = fs.readFileSync(file, 'utf8');
  const rel = path.relative(ROOT, file);

  for (const [n, question, options, status] of tableRows(section(md, /^## 7\. Open decisions/))) {
    const number = int(n);
    if (number === null) continue;
    b.decisions.push({ number, question, options: str(options), status: str(status) });
  }
  for (const [date, workflow, mode, result, saved] of tableRows(section(md, /^## 8\. Run log/))) {
    if (!isoDate(date) || !workflow) continue;
    b.run_log.push({ run_date: date, workflow, mode: str(mode), result: str(result), saved: str(saved) });
  }
  for (const [date, client, change, by, check, state, next] of tableRows(section(md, /^## 9\. Actions log/))) {
    if (!isoDate(date) || !client || !change) continue;
    b.actions_log.push({ entry_date: date, client, change, reported_by: str(by), connector_check: str(check), state: str(state), next_run_expectation: str(next) });
  }
  const learnings = section(md, /^## 6\. Learnings/).split('\n').filter((l) => l.startsWith('- '));
  learnings.forEach((l, i) => {
    const body = l.slice(2).trim();
    const title = (body.match(/^\*\*(.+?)\*\*/) ?? [])[1] ?? body.slice(0, 80);
    b.notes.push({ id: `learning:${String(i + 1).padStart(3, '0')}`, kind: 'learning', note_date: null, client: null, title, body, source_file: rel });
  });
}

// ---------------------------------------------------------------- free text
function reportsAndNotes(b: Batches) {
  for (const file of listFiles(path.join(WEEKLY, 'HG AI Reports'), /\.md$/)) {
    const base = path.basename(file, '.md');
    const m = base.match(/^(\d{4}-\d{2}-\d{2})\s+(.+?)\s+-\s+HG AI$/);
    b.notes.push({
      id: `hg-ai-report:${base}`, kind: 'hg-ai-report', note_date: m?.[1] ?? null, client: m?.[2] ?? null,
      title: base, body: fs.readFileSync(file, 'utf8'), source_file: path.relative(ROOT, file),
    });
  }
  const workflows: [string, string][] = [
    ['Ad Spends Checks/Weekly Checks', 'ad-spend-check'],
    ['Meta Pixel Reviews/Weekly Checks', 'pixel-domain-check'],
    ['Client Benchmark Reviews (advanced setups)/Weekly Checks', 'client-benchmark'],
  ];
  for (const [folder, slug] of workflows) {
    for (const file of listFiles(path.join(WEEKLY, folder), new RegExp(`^\\d{4}-\\d{2}-\\d{2}-${slug}\\.md$`))) {
      const base = path.basename(file, '.md');
      b.notes.push({
        id: `weekly-report:${base}`, kind: 'weekly-report', note_date: base.slice(0, 10), client: null,
        title: base,
        body: SEED ? `Full text not loaded yet: see ${path.relative(ROOT, file)} in the repo, or run scripts/sync-roi-memory.mts with the service key.` : fs.readFileSync(file, 'utf8'),
        source_file: path.relative(ROOT, file),
      });
    }
  }
}

// ---------------------------------------------------------------- output
const CONFLICT: Record<string, string> = {
  monthly_client_metrics: 'period_id, client',
  weekly_ad_spend_checks: 'run_date, client, ad_account_id',
  weekly_pixel_checks: 'run_date, client, pixel_id',
  weekly_benchmark_rows: 'run_date, client, campaign',
  decisions: 'number',
  actions_log: 'entry_date, client, change',
  run_log: 'run_date, workflow',
  notes: 'id',
};
const JSONB = new Set(['campaigns', 'raw']);

function sqlLit(col: string, v: unknown): string {
  if (v === null || v === undefined) return 'null';
  if (JSONB.has(col)) return `'${JSON.stringify(v).replace(/'/g, "''")}'::jsonb`;
  if (typeof v === 'number') return String(v);
  if (typeof v === 'boolean') return v ? 'true' : 'false';
  return `'${String(v).replace(/'/g, "''")}'`;
}

function emitSql(b: Batches) {
  const out: string[] = [];
  for (const [table, rows] of Object.entries(b)) {
    if (!rows.length) continue;
    const cols = [...new Set(rows.flatMap((r) => Object.keys(r)))];
    const keyCols = CONFLICT[table].split(',').map((s) => s.trim());
    const setClause = cols.filter((c) => !keyCols.includes(c)).map((c) => `${c} = excluded.${c}`).concat(['synced_at = now()']).join(', ');
    // One statement per chunk of rows, chunk sized by bytes so large note bodies stay manageable.
    let chunk: string[] = []; let bytes = 0;
    const flush = () => {
      if (!chunk.length) return;
      out.push(`insert into roi.${table} (${cols.join(', ')}) values\n${chunk.join(',\n')}\non conflict (${CONFLICT[table]}) do update set ${setClause};`);
      chunk = []; bytes = 0;
    };
    for (const r of rows) {
      const tuple = `(${cols.map((c) => sqlLit(c, r[c])).join(', ')})`;
      if (bytes + tuple.length > 60_000) flush();
      chunk.push(tuple); bytes += tuple.length;
    }
    flush();
  }
  process.stdout.write(out.join('\n\n') + '\n');
}

async function upsertRest(b: Batches) {
  const url = process.env.SUPABASE_URL?.replace(/\/+$/, '');
  const key = process.env.SUPABASE_SERVICE_ROLE_KEY;
  if (!url || !key) {
    console.error('[sync-roi-memory] SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are not set in .env.local; nothing synced. Use --emit-sql to get SQL instead.');
    process.exit(2);
  }
  for (const [table, rows] of Object.entries(b)) {
    if (!rows.length) continue;
    const cols = [...new Set(rows.flatMap((r) => Object.keys(r)))];
    const normalized = rows.map((r) => Object.fromEntries(cols.map((c) => [c, r[c] ?? null])));
    for (let i = 0; i < normalized.length; i += 200) {
      const slice = normalized.slice(i, i + 200);
      const res = await fetch(`${url}/rest/v1/${table}?on_conflict=${encodeURIComponent(CONFLICT[table].replace(/\s/g, ''))}`, {
        method: 'POST',
        headers: {
          apikey: key, Authorization: `Bearer ${key}`, 'Content-Type': 'application/json',
          'Content-Profile': 'roi', Prefer: 'resolution=merge-duplicates,return=minimal',
        },
        body: JSON.stringify(slice),
      });
      if (!res.ok) {
        console.error(`[sync-roi-memory] ${table} rows ${i}-${i + slice.length}: ${res.status} ${await res.text()}`);
        process.exit(1);
      }
    }
    console.log(`[sync-roi-memory] roi.${table}: ${rows.length} rows upserted`);
  }
}

const batches: Batches = {
  monthly_client_metrics: [], weekly_ad_spend_checks: [], weekly_pixel_checks: [], weekly_benchmark_rows: [],
  decisions: [], actions_log: [], run_log: [], notes: [],
};
monthly(batches);
if (!SEED) weekly(batches);
projectMd(batches);
reportsAndNotes(batches);

if (MODE === 'dry') {
  for (const [t, rows] of Object.entries(batches)) console.log(`roi.${t.padEnd(24)} ${rows.length}`);
} else if (MODE === 'sql') {
  emitSql(batches);
} else {
  await upsertRest(batches);
}
