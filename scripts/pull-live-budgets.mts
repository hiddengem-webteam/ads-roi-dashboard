/**
 * Live daily budget per campaign type for every client on the Master Meta Ads
 * sheet, read straight from the Meta Marketing API with the HiddenGem-Claude
 * system user token (META_ACCESS_TOKEN in .env, gitignored).
 *
 *   npx tsx scripts/pull-live-budgets.mts [YYYY-MM-DD]
 *
 * Writes weekly/Ad Spends Checks/Weekly Checks/<date>-ad-spend-by-type.csv
 * with one row per client:
 *   run_date, client, am, ad_account_id, tof_giveaway, mof_leads,
 *   mof_sales_lol, bof_sales, other, total_live, sheet_budget, diff, flag, campaigns
 * and prints the same table. The Monday ad spend check pushes these rows to
 * the "Meta Ad Spends" tab of the Master sheet (skill step 7b).
 *
 * Rules (same as the spend check and the benchmark generator):
 *   - only campaigns with effective_status ACTIVE and no stop_time in the past
 *   - campaign daily_budget, else the sum of its ACTIVE ad sets' daily_budget
 *     (both Starlight Haven accounts budget at ad set level)
 *   - the API returns budgets in cents
 *   - type by objective first, then name: ToF (traffic/engagement, giveaway,
 *     keyword, discovery), MoF leads (OUTCOME_LEADS), MoF sales LoL (sales
 *     with mof/lookalike/lol/broad in the name), BoF sales (sales with
 *     bof/retarget in the name), anything else "other"
 *   - client -> account map and AM from weekly/Project Data/PROJECT.md section 5
 *   - sheet_budget: .claude/skills/ad-spend-check/sheet-budgets.json if present
 *     ({"Client": 140, ...}, written by the skill from the Meta Ad Links tab at
 *     run time), else the newest *-ad-spend-check.csv (last Monday's reading)
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
  console.error('[pull-live-budgets] META_ACCESS_TOKEN is not set in .env; nothing pulled.');
  process.exit(2);
}

// ---------------------------------------------------------------- client map
interface Client { client: string; am: string; account: string; id: string; note: string }
function clientMap(): Client[] {
  const md = fs.readFileSync(path.join(WEEKLY, 'Project Data', 'PROJECT.md'), 'utf8');
  const start = md.indexOf('## 5. Client');
  const end = md.indexOf('### 5.1', start);
  const out: Client[] = [];
  for (const line of md.slice(start, end).split('\n')) {
    if (!line.startsWith('|')) continue;
    const cells = line.slice(1, -1).split('|').map((c) => c.trim());
    if (cells.length < 5 || !/^\d{6,}$/.test(cells[3])) continue;
    if (/offboarded/i.test(cells[4])) continue;
    out.push({ client: cells[0], am: cells[1] === '—' ? '' : cells[1], account: cells[2], id: cells[3], note: cells[4] });
  }
  return out;
}

// ---------------------------------------------------------------- sheet budgets (latest spend-check CSV)
function sheetBudgets(clients: Client[]): Map<string, number> {
  const m = new Map<string, number>();
  const live = path.join(ROOT, '.claude', 'skills', 'ad-spend-check', 'sheet-budgets.json');
  if (fs.existsSync(live)) {
    const byName = JSON.parse(fs.readFileSync(live, 'utf8')) as Record<string, number | string>;
    const norm = (x: string) => x.toLowerCase().replace(/[^a-z0-9]/g, '');
    const idx = new Map(Object.entries(byName).map(([k, v]) => [norm(k), v]));
    for (const c of clients) {
      const v = idx.get(norm(c.client));
      const n = Number(String(v ?? '').replace(/[$,]/g, ''));
      if (v !== undefined && String(v).trim() !== '' && Number.isFinite(n)) m.set(c.id, n);
    }
    console.log(`[pull-live-budgets] sheet budgets from sheet-budgets.json (${m.size} clients)`);
    return m;
  }
  const files = fs.readdirSync(OUT_DIR).filter((f) => /-ad-spend-check\.csv$/.test(f)).sort();
  if (!files.length) return m;
  console.log(`[pull-live-budgets] sheet budgets from ${files[files.length - 1]} (last Monday's reading; write sheet-budgets.json for today's)`);
  const text = fs.readFileSync(path.join(OUT_DIR, files[files.length - 1]), 'utf8');
  const rows = text.split('\n').slice(1);
  for (const r of rows) {
    // minimal CSV parse: fields we need sit before the quoted notes column
    const cells = r.match(/("([^"]|"")*"|[^,]*)(,|$)/g)?.map((c) => c.replace(/,$/, '').replace(/^"|"$/g, '').replace(/""/g, '"')) ?? [];
    if (cells.length < 7) continue;
    const id = cells[3]; const raw = (cells[5] ?? '').trim(); const budget = Number(raw);
    if (id && raw !== '' && Number.isFinite(budget)) m.set(id, budget);
  }
  return m;
}

// ---------------------------------------------------------------- Meta
type Bucket = 'tof_giveaway' | 'mof_leads' | 'mof_sales_lol' | 'bof_sales' | 'other';
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

const cents = (v?: string) => (v ? Number(v) / 100 : 0);
const today = new Date(RUN_DATE + 'T23:59:59Z');

async function main() {
  const clients = clientMap();
  const sheet = sheetBudgets(clients);
  const rows: string[][] = [];
  const header = ['run_date', 'client', 'am', 'ad_account_id', 'tof_giveaway', 'mof_leads', 'mof_sales_lol', 'bof_sales', 'other', 'total_live', 'sheet_budget', 'diff', 'flag', 'campaigns'];
  for (const c of clients) {
    const sums: Record<Bucket, number> = { tof_giveaway: 0, mof_leads: 0, mof_sales_lol: 0, bof_sales: 0, other: 0 };
    const detail: string[] = [];
    let err = '';
    try {
      for (const cp of await campaigns(c.id)) {
        if (cp.effective_status !== 'ACTIVE') continue;
        if (cp.stop_time && new Date(cp.stop_time) < today) continue; // old boosted posts stay ACTIVE forever
        let b = cents(cp.daily_budget);
        if (!b && cp.adsets?.data) b = cp.adsets.data.filter((a) => a.effective_status === 'ACTIVE').reduce((s, a) => s + cents(a.daily_budget), 0);
        if (!b) continue;
        const k = bucket(cp.objective, cp.name);
        sums[k] += b;
        detail.push(`${cp.name} $${b.toFixed(0)}`);
      }
    } catch (e) {
      err = (e as Error).message;
    }
    const total = Object.values(sums).reduce((a, b) => a + b, 0);
    const sb = sheet.get(c.id);
    const diff = sb === undefined ? null : total - sb;
    let flag = 'match';
    if (err) flag = 'blocker';
    else if (sb === undefined) flag = 'no sheet budget';
    else if (Math.abs(diff!) > Math.max(0.2 * sb, 15)) flag = 'critical';
    else if (Math.abs(diff!) > Math.max(0.1 * sb, 5)) flag = 'warning';
    rows.push([RUN_DATE, c.client, c.am, c.id, ...(['tof_giveaway', 'mof_leads', 'mof_sales_lol', 'bof_sales', 'other'] as Bucket[]).map((k) => sums[k].toFixed(2)),
      total.toFixed(2), sb === undefined ? '' : String(sb), diff === null ? '' : diff.toFixed(2), flag, err ? `ERROR: ${err}` : detail.join('; ')]);
    console.log(`${c.client.padEnd(30)} total $${total.toFixed(0).padStart(5)}  ToF $${sums.tof_giveaway.toFixed(0).padStart(4)}  Leads $${sums.mof_leads.toFixed(0).padStart(4)}  LoL $${sums.mof_sales_lol.toFixed(0).padStart(4)}  BoF $${sums.bof_sales.toFixed(0).padStart(4)}  ${sums.other ? `other $${sums.other.toFixed(0)}  ` : ''}sheet ${sb ?? '—'}  ${flag}${err ? ' ' + err : ''}`);
  }
  const csv = [header, ...rows].map((r) => r.map((v) => (/[",\n]/.test(v) ? `"${v.replace(/"/g, '""')}"` : v)).join(',')).join('\n') + '\n';
  const out = path.join(OUT_DIR, `${RUN_DATE}-ad-spend-by-type.csv`);
  fs.writeFileSync(out, csv, 'utf8');
  console.log(`\nWrote ${path.relative(ROOT, out)} (${rows.length} clients)`);
}
await main();
