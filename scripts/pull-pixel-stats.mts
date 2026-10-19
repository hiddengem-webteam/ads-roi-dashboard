/**
 * Weekly pixel pull for the pixel domain check, through the Meta Marketing API
 * with the HiddenGem-Claude system user token (META_ACCESS_TOKEN in .env).
 * Replaces the claude.ai Meta connector path from 2026-10-19.
 *
 *   npx tsx scripts/pull-pixel-stats.mts [YYYY-MM-DD]
 *
 * Reads: PROJECT.md section 5 (client -> ad account, offboarded rows skipped)
 *        and 5.1 (client -> pixel ids).
 * Lists: HG BM 158693423705448 owned_pixels + client_pixels, and act_<id>/adspixels
 *        for every client account (what is attached where).
 * Pulls, for every pixel that fired in the last 28 days or is in the pixel map:
 *        /<pixel>/stats aggregation=host (7-day window ending now, paginated),
 *        event_total_counts, event_source (browser vs server).
 * Writes: .claude/skills/pixel-domain-check/pixel_pull.json (overwritten weekly)
 *         with per-pixel hosts (count, first/last hour, per-day counts), events,
 *         sources, attached accounts, and any error.
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const WEEKLY = path.join(ROOT, 'weekly');
const OUT = path.join(ROOT, '.claude', 'skills', 'pixel-domain-check', 'pixel_pull.json');
const RUN_DATE = process.argv[2] ?? new Date().toISOString().slice(0, 10);
const API = 'https://graph.facebook.com/v21.0';
const HG_BM = '158693423705448';

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
if (!TOKEN) { console.error('[pull-pixel-stats] META_ACCESS_TOKEN is not set in .env'); process.exit(2); }

interface Client { client: string; am: string; id: string; offboarded: boolean }
function clientMap(): { clients: Client[]; pixelMap: Map<string, string[]> } {
  const md = fs.readFileSync(path.join(WEEKLY, 'Project Data', 'PROJECT.md'), 'utf8');
  const start = md.indexOf('## 5. Client');
  const s51 = md.indexOf('### 5.1', start);
  const end = md.indexOf('## 6.', s51);
  const clients: Client[] = [];
  for (const line of md.slice(start, s51).split('\n')) {
    if (!line.startsWith('|')) continue;
    const c = line.slice(1, -1).split('|').map((x) => x.trim());
    if (c.length < 5 || !/^\d{6,}$/.test(c[3])) continue;
    clients.push({ client: c[0], am: c[1] === '—' ? '' : c[1], id: c[3], offboarded: /offboarded/i.test(c[4]) });
  }
  const pixelMap = new Map<string, string[]>();
  for (const line of md.slice(s51, end).split('\n')) {
    if (!line.startsWith('|')) continue;
    const c = line.slice(1, -1).split('|').map((x) => x.trim());
    if (c.length < 3) continue;
    const ids = [...c[1].matchAll(/→ (\d{10,})/g)].map((m) => m[1]);
    if (ids.length) pixelMap.set(c[0], ids);
  }
  return { clients, pixelMap };
}

async function get(url: string): Promise<any> {
  const res = await fetch(url);
  const body = await res.json() as any;
  if (body.error) throw new Error(`${body.error.code ?? ''} ${body.error.message}`);
  return body;
}
async function getAll(url: string): Promise<any[]> {
  const out: any[] = [];
  let next = url;
  while (next) {
    const body = await get(next);
    out.push(...(body.data ?? []));
    next = body.paging?.next ?? '';
  }
  return out;
}

interface Pixel {
  id: string; name: string; owner_business?: { id: string; name: string }; last_fired_time?: string;
  listed_in: string[]; attached_to: string[];
}
const PIXEL_FIELDS = 'id,name,last_fired_time,owner_business{id,name}';

async function main() {
  const { clients, pixelMap } = clientMap();
  const active = clients.filter((c) => !c.offboarded);
  const pixels = new Map<string, Pixel>();
  const add = (p: any, where: string, acct?: string) => {
    const cur = pixels.get(p.id) ?? { id: p.id, name: p.name, owner_business: p.owner_business, last_fired_time: p.last_fired_time, listed_in: [], attached_to: [] };
    if (p.last_fired_time && (!cur.last_fired_time || p.last_fired_time > cur.last_fired_time)) cur.last_fired_time = p.last_fired_time;
    if (!cur.owner_business && p.owner_business) cur.owner_business = p.owner_business;
    if (!cur.listed_in.includes(where)) cur.listed_in.push(where);
    if (acct && !cur.attached_to.includes(acct)) cur.attached_to.push(acct);
    pixels.set(p.id, cur);
  };
  const listingErrors: Record<string, string> = {};
  for (const edge of ['owned_pixels', 'client_pixels']) {
    try {
      for (const p of await getAll(`${API}/${HG_BM}/${edge}?fields=${PIXEL_FIELDS}&limit=100&access_token=${TOKEN}`)) add(p, `hg_${edge}`);
    } catch (e: any) { listingErrors[`hg_${edge}`] = e.message; }
  }
  const accountErrors: Record<string, string> = {};
  for (const c of active) {
    try {
      for (const p of await getAll(`${API}/act_${c.id}/adspixels?fields=${PIXEL_FIELDS}&limit=100&access_token=${TOKEN}`)) add(p, `act_${c.id}`, c.id);
    } catch (e: any) { accountErrors[c.id] = e.message; }
  }
  // direct reads for mapped pixels that no listing returned (client-business pixels not shared)
  const offboardedNames = new Set(clients.filter((c) => c.offboarded).map((c) => c.client));
  const mapped = new Set([...pixelMap.entries()].filter(([c]) => !offboardedNames.has(c)).flatMap(([, ids]) => ids));
  for (const id of mapped) {
    if (pixels.has(id)) continue;
    try { const p = await get(`${API}/${id}?fields=${PIXEL_FIELDS}&access_token=${TOKEN}`); add(p, 'direct'); }
    catch (e: any) { pixels.set(id, { id, name: '(not readable)', listed_in: ['direct'], attached_to: [] }); accountErrors[`pixel_${id}`] = e.message; }
  }

  const end = Math.floor(Date.now() / 1000);
  const start = end - 7 * 86400;
  const cutoff = new Date(Date.now() - 28 * 86400 * 1000).toISOString();
  const results: any[] = [];
  let n = 0;
  for (const p of [...pixels.values()].sort((a, b) => a.name.localeCompare(b.name))) {
    const recent = p.last_fired_time ? p.last_fired_time >= cutoff : false;
    const inMap = mapped.has(p.id);
    const r: any = { ...p, in_map: inMap, fired_28d: recent, hosts: {}, events: {}, sources: {}, total_events: 0, server_events: 0, error: '' };
    if (!recent && !inMap) { r.skipped = 'not fired in 28d and not mapped'; results.push(r); continue; }
    // Stats quirk (seen 2026-10-19): every stats response carries paging.next even when
    // the single bucket already covers the whole window; following it repeats the data
    // and inflates totals ~60x. Only page when a response is actually full (limit reached).
    const statsPages = async (agg: string): Promise<any[]> => {
      const out: any[] = [];
      let next = `${API}/${p.id}/stats?aggregation=${agg}&start_time=${start}&end_time=${end}&limit=500&access_token=${TOKEN}`;
      while (next) {
        const body = await get(next);
        const data = body.data ?? [];
        out.push(...data);
        next = data.length >= 500 ? (body.paging?.next ?? '') : '';
      }
      return out;
    };
    const errs: string[] = [];
    try {
      for (const b of await statsPages('host')) {
        const hour = String(b.start_time ?? '');
        const day = hour.slice(0, 10);
        for (const v of b.data ?? []) {
          const h = String(v.value ?? '').toLowerCase();
          const cur = r.hosts[h] ?? { count: 0, first: hour, last: hour, daily: {} };
          cur.count += Number(v.count ?? 0);
          if (hour < cur.first) cur.first = hour;
          if (hour > cur.last) cur.last = hour;
          cur.daily[day] = (cur.daily[day] ?? 0) + Number(v.count ?? 0);
          r.hosts[h] = cur;
        }
      }
    } catch (e: any) { errs.push(`host: ${e.message}`); }
    try {
      for (const b of await statsPages('event_total_counts')) for (const v of b.data ?? []) {
        const e = String(v.value ?? '');
        r.events[e] = (r.events[e] ?? 0) + Number(v.count ?? 0);
        r.total_events += Number(v.count ?? 0);
      }
    } catch (e: any) { errs.push(`event_total_counts: ${e.message}`); }
    try {
      for (const b of await statsPages('event_source')) for (const v of b.data ?? []) {
        const s = String(v.value ?? '');
        r.sources[s] = (r.sources[s] ?? 0) + Number(v.count ?? 0);
      }
      r.server_events = Object.entries(r.sources).filter(([k]) => /server|capi|conversions/i.test(k)).reduce((s, [, v]) => s + Number(v), 0);
    } catch (e: any) { errs.push(`event_source: ${e.message}`); }
    r.error = errs.join('; ');
    results.push(r);
    n++;
    console.log(`${String(n).padStart(3)} ${p.name.padEnd(45).slice(0, 45)} ${p.id} events ${r.total_events} hosts ${Object.keys(r.hosts).length}${r.error ? ' ERROR ' + r.error : ''}`);
  }
  const out = {
    run_date: RUN_DATE, pulled_at: new Date().toISOString(), window: { start: new Date(start * 1000).toISOString(), end: new Date(end * 1000).toISOString() },
    hg_bm: HG_BM, clients: active, offboarded: clients.filter((c) => c.offboarded).map((c) => c.client),
    pixel_map: Object.fromEntries(pixelMap), listing_errors: listingErrors, account_errors: accountErrors, pixels: results,
  };
  fs.writeFileSync(OUT, JSON.stringify(out, null, 1));
  const read = results.filter((r) => !r.skipped);
  console.log(`\n${pixels.size} pixels listed, ${read.length} read, ${read.filter((r) => r.error).length} errors, ${results.filter((r) => r.skipped).length} skipped. Account listing errors: ${Object.keys(accountErrors).length}. Wrote ${path.relative(ROOT, OUT)}`);
}
main().catch((e) => { console.error(e); process.exit(1); });
