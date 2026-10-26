/**
 * Weekly ad spend check: the live daily budget per client and per campaign
 * type, read straight from the Meta Marketing API with the HiddenGem-Claude
 * system user token (META_ACCESS_TOKEN in .env, gitignored). No comparison
 * against the Master sheet's documented budget (dropped 2026-10-15, Shawal):
 * the report is a spend ledger plus the week-over-week change.
 *
 *   npx tsx scripts/ad-spend-check.mts [YYYY-MM-DD]
 *
 * Writes to weekly/Ad Spends Checks/Weekly Checks/:
 *   <date>-ad-spend-check.csv   one row per client:
 *     run_date, client, am, ad_account_id, source, tof_giveaway, mof_leads,
 *     mof_sales_lol, bof_sales, other, total_live, spend_7d, prev_total,
 *     change, status, what_changed, campaigns
 *   <date>-ad-spend-check.md    the report (header, changes, ledger, footer);
 *                               build_html.py renders it, the skill pushes the
 *                               rows to the Master sheet's "Meta Ad Spends" tab
 *                               and then fills in the "Meta Ad Spends tab:" line.
 *
 * Rules (shared with the benchmark generator):
 *   - only campaigns with effective_status ACTIVE and no stop_time in the past
 *   - campaign daily_budget, else the sum of its ACTIVE ad sets' daily_budget
 *     (both Starlight Haven accounts budget at ad set level)
 *   - the API returns budgets in cents
 *   - type by objective first, then name: ToF (traffic/engagement, giveaway,
 *     keyword, discovery), MoF leads (OUTCOME_LEADS), MoF sales LoL (sales
 *     with mof/lookalike/lol/broad in the name), BoF sales (sales with
 *     bof/retarget in the name), anything else "other"
 *   - spend_7d is the account's insights `spend` for date_preset last_7d
 *   - client -> account map and AM from weekly/Project Data/PROJECT.md
 *     section 5; rows whose Connector cell says Offboarded are skipped
 *   - previous run: the newest *-ad-spend-check.csv (or the older
 *     *-ad-spend-by-type.csv) dated before the run date; totals come from
 *     total_live or, in the pre-2026-10-15 format, actual_daily_budget
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const WEEKLY = path.join(ROOT, 'weekly');
const OUT_DIR = path.join(WEEKLY, 'Ad Spends Checks', 'Weekly Checks');
const RUN_DATE = process.argv[2] ?? new Date().toISOString().slice(0, 10);
const API = 'https://graph.facebook.com/v21.0';

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
const TOKEN = process.env.META_ACCESS_TOKEN;
if (!TOKEN) {
  console.error('[ad-spend-check] META_ACCESS_TOKEN is not set in .env; nothing pulled.');
  process.exit(2);
}

// ---------------------------------------------------------------- client map
interface Client { client: string; am: string; account: string; id: string; note: string }
function clientMap(): { clients: Client[]; offboarded: string[] } {
  const md = fs.readFileSync(path.join(WEEKLY, 'Project Data', 'PROJECT.md'), 'utf8');
  const start = md.indexOf('## 5. Client');
  const end = md.indexOf('### 5.1', start);
  const clients: Client[] = [];
  const offboarded: string[] = [];
  for (const line of md.slice(start, end).split('\n')) {
    if (!line.startsWith('|')) continue;
    const cells = line.slice(1, -1).split('|').map((c) => c.trim());
    if (cells.length < 5 || !/^\d{6,}$/.test(cells[3])) continue;
    if (/offboarded/i.test(cells[4])) { offboarded.push(cells[0]); continue; }
    clients.push({ client: cells[0], am: cells[1] === '—' ? '' : cells[1], account: cells[2], id: cells[3], note: cells[4] });
  }
  return { clients, offboarded };
}

// ---------------------------------------------------------------- csv helpers
function parseCsv(text: string): string[][] {
  const rows: string[][] = []; let row: string[] = []; let f = ''; let q = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (q) { if (c === '"') { if (text[i + 1] === '"') { f += '"'; i++; } else q = false; } else f += c; }
    else if (c === '"') q = true;
    else if (c === ',') { row.push(f); f = ''; }
    else if (c === '\n') { row.push(f); rows.push(row); row = []; f = ''; }
    else if (c !== '\r') f += c;
  }
  if (f || row.length) { row.push(f); rows.push(row); }
  return rows.filter((r) => r.length > 1);
}
const csvCell = (v: string) => (/[",\n]/.test(v) ? `"${v.replace(/"/g, '""')}"` : v);
function parseCampaigns(s: string): Map<string, number> {
  const m = new Map<string, number>();
  for (const part of s.split('; ')) {
    const mm = part.match(/^(.*) \$(\d+(?:\.\d+)?)$/);
    if (mm) m.set(mm[1], Number(mm[2]));
  }
  return m;
}

// ---------------------------------------------------------------- previous run
interface Prev { file: string; totals: Map<string, number>; names: Map<string, string>; campaigns: Map<string, Map<string, number>> | null }
function previousRun(): Prev | null {
  const files = fs.readdirSync(OUT_DIR)
    .filter((f) => /-ad-spend-(check|by-type)\.csv$/.test(f) && f.slice(0, 10) < RUN_DATE)
    .sort();
  if (!files.length) return null;
  const file = files[files.length - 1];
  const [header, ...rows] = parseCsv(fs.readFileSync(path.join(OUT_DIR, file), 'utf8'));
  const idx = Object.fromEntries(header.map((h, i) => [h, i]));
  const totalCol = idx.total_live ?? idx.actual_daily_budget;
  const totals = new Map<string, number>();
  const names = new Map<string, string>();
  const campaigns = idx.campaigns === undefined ? null : new Map<string, Map<string, number>>();
  for (const r of rows) {
    const id = r[idx.ad_account_id];
    const t = Number(r[totalCol]);
    if (id && Number.isFinite(t) && r[totalCol] !== '') totals.set(id, t);
    if (id) names.set(id, r[idx.client] ?? id);
    if (campaigns && id && !/^ERROR/.test(r[idx.campaigns])) campaigns.set(id, parseCampaigns(r[idx.campaigns]));
  }
  return { file, totals, names, campaigns };
}

// ---------------------------------------------------------------- Meta
type Bucket = 'tof_giveaway' | 'mof_leads' | 'mof_sales_lol' | 'bof_sales' | 'other';
const BUCKETS: Bucket[] = ['tof_giveaway', 'mof_leads', 'mof_sales_lol', 'bof_sales', 'other'];
const BUCKET_LABEL: Record<Bucket, string> = { tof_giveaway: 'ToF Giveaway', mof_leads: 'MoF Leads', mof_sales_lol: 'MoF Sales LoL', bof_sales: 'BoF Sales', other: 'Other' };
function bucket(objective: string | undefined, name: string): Bucket {
  const n = name.toLowerCase();
  if (objective === 'OUTCOME_LEADS' || /\blead/.test(n)) return 'mof_leads';
  if (objective === 'OUTCOME_SALES' || /bof|retarget|sales/.test(n)) {
    if (/bof|retarget/.test(n)) return 'bof_sales';
    if (/mof|lookalike|lol|broad|prospect/.test(n)) return 'mof_sales_lol';
    return 'bof_sales';
  }
  if (objective === 'OUTCOME_TRAFFIC' || objective === 'OUTCOME_ENGAGEMENT' || /discovery|giveaway|keyword|tof|follow|engage|traffic/.test(n)) return 'tof_giveaway';
  return 'other';
}

interface Campaign { id: string; name: string; objective?: string; effective_status: string; daily_budget?: string; stop_time?: string; adsets?: { data: { effective_status: string; daily_budget?: string }[] } }
async function campaigns(accountId: string): Promise<Campaign[]> {
  const fields = 'id,name,objective,effective_status,daily_budget,stop_time,adsets.limit(100){effective_status,daily_budget}';
  let url = `${API}/act_${accountId}/campaigns?fields=${encodeURIComponent(fields)}&effective_status=${encodeURIComponent('["ACTIVE"]')}&limit=200&access_token=${TOKEN}`;
  const out: Campaign[] = [];
  while (url) {
    const res = await fetch(url);
    const body = await res.json() as { data?: Campaign[]; paging?: { next?: string }; error?: { message: string } };
    if (body.error) throw new Error(body.error.message);
    out.push(...(body.data ?? []));
    url = body.paging?.next ?? '';
  }
  return out;
}
async function spend7d(accountId: string): Promise<number | null> {
  try {
    const res = await fetch(`${API}/act_${accountId}/insights?fields=spend&date_preset=last_7d&access_token=${TOKEN}`);
    const body = await res.json() as { data?: { spend?: string }[]; error?: { message: string } };
    if (body.error) return null;
    const s = Number(body.data?.[0]?.spend ?? '0');
    return Number.isFinite(s) ? s : null;
  } catch { return null; }
}

const cents = (v?: string) => (v ? Number(v) / 100 : 0);
const today = new Date(RUN_DATE + 'T23:59:59Z');
const money = (n: number) => `$${n.toLocaleString('en-US', { maximumFractionDigits: 0 })}`;
const signed = (n: number) => (n > 0 ? `+${money(n)}` : n < 0 ? `−${money(-n)}` : '$0');
const ptTime = (d: Date) => new Intl.DateTimeFormat('en-US', { timeZone: 'America/Los_Angeles', hour: '2-digit', minute: '2-digit', hour12: false }).format(d);
const longDate = (iso: string) => new Date(iso + 'T12:00:00Z').toLocaleDateString('en-GB', { timeZone: 'UTC', day: 'numeric', month: 'long', year: 'numeric' });
const weekday = (iso: string) => new Date(iso + 'T12:00:00Z').toLocaleDateString('en-US', { timeZone: 'UTC', weekday: 'long' });

interface Row {
  c: Client; sums: Record<Bucket, number>; total: number; detail: Map<string, number>; err: string; spend7d: number | null;
  prevTotal: number | null; change: number | null; status: string; whatChanged: string;
}

async function main() {
  const { clients, offboarded } = clientMap();
  const prev = previousRun();
  const t0 = new Date();
  const rows: Row[] = [];
  for (const c of clients) {
    const sums: Record<Bucket, number> = { tof_giveaway: 0, mof_leads: 0, mof_sales_lol: 0, bof_sales: 0, other: 0 };
    const detail = new Map<string, number>();
    let err = '';
    try {
      for (const cp of await campaigns(c.id)) {
        if (cp.effective_status !== 'ACTIVE') continue;
        if (cp.stop_time && new Date(cp.stop_time) < today) continue; // old boosted posts stay ACTIVE forever
        let b = cents(cp.daily_budget);
        if (!b && cp.adsets?.data) b = cp.adsets.data.filter((a) => a.effective_status === 'ACTIVE').reduce((s, a) => s + cents(a.daily_budget), 0);
        if (!b) continue;
        sums[bucket(cp.objective, cp.name)] += b;
        detail.set(cp.name, (detail.get(cp.name) ?? 0) + b);
      }
    } catch (e) {
      err = (e as Error).message;
    }
    const sp = err ? null : await spend7d(c.id);
    const total = Object.values(sums).reduce((a, b) => a + b, 0);
    // week over week
    let prevTotal: number | null = null; let change: number | null = null; let status = 'first_run'; let whatChanged = '';
    if (err) status = 'blocked';
    else if (prev) {
      if (!prev.totals.has(c.id)) status = 'new';
      else {
        prevTotal = prev.totals.get(c.id)!;
        change = total - prevTotal;
        status = change > 0.005 ? 'up' : change < -0.005 ? 'down' : 'unchanged';
        const pc = prev.campaigns?.get(c.id);
        if (status !== 'unchanged') {
          if (pc) {
            const parts: string[] = [];
            for (const [name, b] of detail) {
              if (!pc.has(name)) parts.push(`added ${name} ${money(b)}`);
              else if (Math.abs(pc.get(name)! - b) > 0.005) parts.push(`${name} ${money(pc.get(name)!)} to ${money(b)}`);
            }
            for (const [name, b] of pc) if (!detail.has(name)) parts.push(`removed ${name} ${money(b)}`);
            whatChanged = parts.join('; ');
          } else whatChanged = 'total only; the previous run did not record campaigns';
        }
      }
    }
    rows.push({ c, sums, total, detail, err, spend7d: sp, prevTotal, change, status, whatChanged });
    console.log(`${c.client.padEnd(30)} total $${total.toFixed(0).padStart(5)}  ToF $${sums.tof_giveaway.toFixed(0).padStart(4)}  Leads $${sums.mof_leads.toFixed(0).padStart(4)}  LoL $${sums.mof_sales_lol.toFixed(0).padStart(4)}  BoF $${sums.bof_sales.toFixed(0).padStart(4)}  ${sums.other ? `other $${sums.other.toFixed(0)}  ` : ''}7d $${(sp ?? 0).toFixed(0).padStart(5)}  ${status}${change ? ' ' + signed(change) : ''}${err ? ' ' + err : ''}`);
  }
  const t1 = new Date();

  // ---------------------------------------------------------------- csv
  const header = ['run_date', 'client', 'am', 'ad_account_id', 'source', ...BUCKETS, 'total_live', 'spend_7d', 'prev_total', 'change', 'status', 'what_changed', 'campaigns'];
  const campaignsText = (r: Row) => (r.err ? `ERROR: ${r.err}` : [...r.detail].map(([n, b]) => `${n} $${b.toFixed(0)}`).join('; '));
  const csvRows = rows.map((r) => [RUN_DATE, r.c.client, r.c.am, r.c.id, r.err ? 'blocked' : 'live',
    ...BUCKETS.map((k) => r.sums[k].toFixed(2)), r.total.toFixed(2), r.spend7d === null ? '' : r.spend7d.toFixed(2),
    r.prevTotal === null ? '' : r.prevTotal.toFixed(2), r.change === null ? '' : r.change.toFixed(2), r.status, r.whatChanged, campaignsText(r)]);
  const csv = [header, ...csvRows].map((r) => r.map(csvCell).join(',')).join('\n') + '\n';
  fs.writeFileSync(path.join(OUT_DIR, `${RUN_DATE}-ad-spend-check.csv`), csv, 'utf8');

  // ---------------------------------------------------------------- md
  const live = rows.filter((r) => !r.err);
  const blocked = rows.filter((r) => r.err);
  const totalLive = live.reduce((s, r) => s + r.total, 0);
  const byType = Object.fromEntries(BUCKETS.map((k) => [k, live.reduce((s, r) => s + r.sums[k], 0)])) as Record<Bucket, number>;
  const spentRows = live.filter((r) => r.spend7d !== null);
  const spent7 = spentRows.reduce((s, r) => s + (r.spend7d ?? 0), 0);
  const prevTotalAll = live.reduce((s, r) => s + (r.prevTotal ?? 0), 0);
  const changed = rows.filter((r) => ['up', 'down', 'new'].includes(r.status)).sort((a, b) => Math.abs(b.change ?? b.total) - Math.abs(a.change ?? a.total));
  const ledger = [...rows].sort((a, b) => b.total - a.total || a.c.client.localeCompare(b.c.client));
  const statusWord: Record<string, string> = { up: 'Up', down: 'Down', new: 'New', unchanged: 'Same', blocked: 'Blocked', first_run: 'First run' };
  const removed = prev ? [...prev.totals.keys()].filter((id) => !clients.some((c) => c.id === id)) : [];
  const n = rows.length;
  const up = rows.filter((r) => r.status === 'up').length, down = rows.filter((r) => r.status === 'down').length, nnew = rows.filter((r) => r.status === 'new').length;

  const L: string[] = [];
  L.push(`# Ad spend check — ${RUN_DATE}`, '');
  L.push(`Run: ${longDate(RUN_DATE)} (${weekday(RUN_DATE)}; live reads ${ptTime(t0)}–${ptTime(t1)} PT through the Meta Marketing API with the HiddenGem-Claude system user). ${prev ? `Compared against ${prev.file}.` : 'First run, no prior report.'}`, '');
  L.push('Meta Ad Spends tab: not pushed yet.', '');
  L.push('| Clients | Live reads | Blocked | Total live $/day | ToF Giveaway | MoF Leads | MoF Sales LoL | BoF Sales | Other | Spent last 7 days |');
  L.push('|---|---|---|---|---|---|---|---|---|---|');
  L.push(`| ${n} | ${live.length} | ${blocked.length} | ${money(totalLive)} | ${BUCKETS.map((k) => money(byType[k])).join(' | ')} | ${money(spent7)} |`, '');

  L.push('## Changes since last week', '');
  if (!prev) L.push('First run, no prior report.', '');
  else if (!changed.length && !removed.length) L.push(`No budget changes since ${prev.file.slice(0, 10)}.`, '');
  else {
    L.push('| Client | AM | Last week $/day | This week $/day | Change | Status | What changed |');
    L.push('|---|---|---|---|---|---|---|');
    for (const r of changed) L.push(`| ${r.c.client} | ${r.c.am || '—'} | ${r.prevTotal === null ? '—' : money(r.prevTotal)} | ${money(r.total)} | ${r.change === null ? '—' : signed(r.change)} | ${statusWord[r.status]} | ${(r.whatChanged || (r.status === 'new' ? 'not in the previous run' : '')).replace(/\|/g, '/')} |`);
    for (const id of removed) L.push(`| ${prev.names.get(id) ?? id} | — | ${money(prev.totals.get(id)!)} | — | — | Removed | no longer in the client map (offboarded or remapped) |`);
    L.push('');
  }

  L.push('## Live spend by client', '');
  L.push('Sorted by total live $/day, highest first. Spent 7d is the account\'s actual spend over the last 7 days.', '');
  L.push('| Client | AM | Total $/day | ToF Giveaway | MoF Leads | MoF Sales LoL | BoF Sales | Other | Spent 7d | vs last week | Status | Campaigns |');
  L.push('|---|---|---|---|---|---|---|---|---|---|---|---|');
  for (const r of ledger) {
    const vs = r.err ? '—' : r.status === 'new' ? 'new' : r.change === null ? '—' : signed(r.change);
    L.push(`| ${r.c.client} | ${r.c.am || '—'} | ${r.err ? 'n/a' : money(r.total)} | ${BUCKETS.map((k) => (r.err ? '—' : money(r.sums[k]))).join(' | ')} | ${r.spend7d === null ? '—' : money(r.spend7d)} | ${vs} | ${statusWord[r.status]} | ${campaignsText(r).replace(/\|/g, '/')} |`);
  }
  L.push('');

  L.push('## Footer', '');
  L.push(`- Clients checked: ${n}, from the client map in PROJECT.md section 5.${offboarded.length ? ` Offboarded, not checked: ${offboarded.join(', ')}.` : ''}`);
  L.push(`- Live reads: ${live.length} through the Marketing API. Blocked: ${blocked.length}${blocked.length ? ` (${blocked.map((r) => r.c.client).join(', ')})` : ''}.`);
  L.push(`- Total live $/day: ${money(totalLive)} (${BUCKETS.filter((k) => byType[k] > 0).map((k) => `${BUCKET_LABEL[k]} ${money(byType[k])}`).join(', ')})${prev ? `, vs ${money(prevTotalAll)} for the same accounts last run` : ''}. Spent in the last 7 days: ${money(spent7)} across ${spentRows.length} accounts (${money(spent7 / 7)}/day).`);
  L.push(`- Changes: ${up} up, ${down} down, ${nnew} new, ${rows.filter((r) => r.status === 'unchanged').length} unchanged${removed.length ? `, ${removed.length} removed` : ''}.`);
  L.push(`- Previous report: ${prev ? prev.file : 'none, first run'}`);
  L.push('- Budgets come from the API in cents and are divided by 100; a campaign with no campaign-level budget is summed from its active ad sets; campaigns past their stop time are ignored. Types by objective first, then name.');
  L.push('');
  fs.writeFileSync(path.join(OUT_DIR, `${RUN_DATE}-ad-spend-check.md`), L.join('\n'), 'utf8');

  console.log(`\n${n} clients, ${live.length} live reads, ${blocked.length} blocked. Total live ${money(totalLive)}/day; ${up} up, ${down} down, ${nnew} new. Spent 7d ${money(spent7)}.`);
  console.log(`Wrote weekly/Ad Spends Checks/Weekly Checks/${RUN_DATE}-ad-spend-check.csv and .md`);
}
await main();
