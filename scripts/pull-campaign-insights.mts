/**
 * Weekly campaign pull for the client benchmark review, through the Meta
 * Marketing API with the HiddenGem-Claude system user token (META_ACCESS_TOKEN
 * in .env). Replaces the claude.ai Meta connector's ads_get_ad_entities calls
 * from 2026-10-19.
 *
 *   npx tsx scripts/pull-campaign-insights.mts [YYYY-MM-DD]
 *
 * Accounts come from the ADV map in .claude/skills/client-benchmark/generate_report.py
 * (entries with connector "live"), so the generator and this pull share one list.
 * For each account: every campaign (any status) with its objective and
 * effective_status, plus campaign-level insights for date_preset last_30d and
 * last_14d. Campaigns with no spend in a window are left out of that window.
 * Also reads each account's activity log (last 180 days) and writes creators.json:
 *   { campaign_id: { name, actor_id, created } } for every "create_campaign_group"
 *   event, so the generator can tell HiddenGem campaigns from client-run ones.
 * Writes .claude/skills/client-benchmark/live.psv, pipe-separated:
 *   client|acct|am|win|id|name|objective|status|spend|impr|cpm|ctr|clicks|cpc|freq|leads|cpl|purch|cpp|roas
 * (clicks = inline link clicks, cpc = cost per inline link click, leads = the
 * "lead" action, purch = omni_purchase, roas = omni_purchase purchase_roas).
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const SKILL = path.join(ROOT, '.claude', 'skills', 'client-benchmark');
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
if (!TOKEN) { console.error('[pull-campaign-insights] META_ACCESS_TOKEN is not set in .env'); process.exit(2); }

interface Adv { client: string; am: string; id: string }
function advMap(): Adv[] {
  const py = fs.readFileSync(path.join(SKILL, 'generate_report.py'), 'utf8');
  const block = py.slice(py.indexOf('ADV={'), py.indexOf('ADV_UNMAPPED'));
  const out: Adv[] = [];
  for (const m of block.matchAll(/^\s*"([^"]+)":\("([^"]*)","(\d+)","[^"]*","live"\)/gm)) out.push({ client: m[1], am: m[2], id: m[3] });
  return out;
}

async function get(url: string): Promise<any> {
  const res = await fetch(url);
  const body = await res.json() as any;
  if (body.error) throw new Error(`${body.error.code ?? ''} ${body.error.message}`);
  return body;
}
async function getAll(url: string): Promise<any[]> {
  const out: any[] = []; let next = url;
  while (next) { const b = await get(next); out.push(...(b.data ?? [])); next = b.paging?.next ?? ''; }
  return out;
}
const act = (list: any[] | undefined, type: string) => { const v = list?.find((a) => a.action_type === type)?.value; return v === undefined ? '' : String(v); };
const num = (v: any) => (v === undefined || v === null || v === '' ? '' : String(Number(v)));

async function main() {
  const adv = advMap();
  const lines: string[] = [];
  const t0 = new Date();
  const errors: string[] = [];
  const creators: Record<string, { name: string; actor_id: string; created: string; account: string; campaign: string }> = {};
  const since = new Date(new Date(RUN_DATE + 'T00:00:00Z').getTime() - 180 * 86400 * 1000).toISOString().slice(0, 10);
  for (const a of adv) {
    let camps: any[] = [];
    try {
      camps = await getAll(`${API}/act_${a.id}/campaigns?fields=id,name,objective,effective_status,stop_time&limit=200&access_token=${TOKEN}`);
    } catch (e: any) { errors.push(`${a.client} (${a.id}): ${e.message}`); console.log(`${a.client.padEnd(30)} ERROR ${e.message}`); continue; }
    const byId = new Map(camps.map((c) => [c.id, c]));
    let count = 0;
    for (const win of [30, 14]) {
      const fields = 'campaign_id,campaign_name,spend,impressions,cpm,ctr,inline_link_clicks,cost_per_inline_link_click,frequency,actions,cost_per_action_type,purchase_roas';
      let rows: any[] = [];
      try {
        rows = await getAll(`${API}/act_${a.id}/insights?level=campaign&date_preset=last_${win}d&fields=${fields}&limit=200&access_token=${TOKEN}`);
      } catch (e: any) { errors.push(`${a.client} (${a.id}) ${win}d: ${e.message}`); continue; }
      for (const r of rows) {
        if (!(Number(r.spend) > 0)) continue;
        const c = byId.get(r.campaign_id) ?? {};
        const leads = act(r.actions, 'lead');
        const purch = act(r.actions, 'omni_purchase') || act(r.actions, 'purchase');
        const cpl = act(r.cost_per_action_type, 'lead');
        const cpp = act(r.cost_per_action_type, 'omni_purchase') || act(r.cost_per_action_type, 'purchase');
        const roas = act(r.purchase_roas, 'omni_purchase') || act(r.purchase_roas, 'purchase');
        lines.push([a.client, a.id, a.am, win, r.campaign_id, (r.campaign_name ?? c.name ?? '').replace(/\|/g, '/'), c.objective ?? '', c.effective_status ?? '',
          num(r.spend), num(r.impressions), num(r.cpm), num(r.ctr), num(r.inline_link_clicks), num(r.cost_per_inline_link_click), num(r.frequency),
          num(leads), num(cpl), num(purch), num(cpp), num(roas)].join('|'));
        count++;
      }
    }
    try {
      const acts = await getAll(`${API}/act_${a.id}/activities?fields=event_time,event_type,actor_name,actor_id,object_type,object_id,object_name&since=${since}&limit=500&access_token=${TOKEN}`);
      for (const ev of acts) {
        if (ev.event_type !== 'create_campaign_group' || !ev.object_id) continue;
        creators[String(ev.object_id)] = { name: ev.actor_name ?? '', actor_id: String(ev.actor_id ?? ''), created: String(ev.event_time ?? '').slice(0, 10), account: a.id, campaign: ev.object_name ?? '' };
      }
    } catch (e: any) { errors.push(`${a.client} (${a.id}) activities: ${e.message}`); }
    console.log(`${a.client.padEnd(30)} ${a.id.padEnd(18)} ${camps.length} campaigns, ${count} window rows`);
  }
  fs.writeFileSync(path.join(SKILL, 'live.psv'), lines.join('\n') + '\n');
  fs.writeFileSync(path.join(SKILL, 'creators.json'), JSON.stringify(creators, null, 1));
  const names = [...new Set(Object.values(creators).map((c) => c.name))].sort();
  console.log(`campaign creators seen in the last 180 days: ${names.join(', ')}`);
  fs.writeFileSync(path.join(SKILL, 'live.meta.json'), JSON.stringify({ run_date: RUN_DATE, pulled_from: t0.toISOString(), pulled_to: new Date().toISOString(), accounts: adv.length, rows: lines.length, errors }, null, 1));
  console.log(`\n${adv.length} accounts, ${lines.length} rows, ${errors.length} errors. Wrote .claude/skills/client-benchmark/live.psv`);
  if (errors.length) console.log(errors.join('\n'));
}
main().catch((e) => { console.error(e); process.exit(1); });
