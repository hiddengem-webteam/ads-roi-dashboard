/**
 * Ad-level pull for the Monday post-review (/post-review), through the Meta
 * Marketing API with the HG - ROI Dashboard system user token (META_ACCESS_TOKEN
 * in .env). Added 2026-11-16: the weekly pulls stop at campaign level, and the
 * post-review's creative calls need to know which ads are tired.
 *
 *   npx tsx scripts/pull-ad-insights.mts [YYYY-MM-DD] [--clients "Name A|Name B"]
 *
 * Accounts come from the ADV map in .claude/skills/client-benchmark/generate_report.py
 * (entries marked "live"), the same list the benchmark pull uses.
 * Per account:
 *   - access: act_<id> (name, account_status) and act_<id>/adspixels (id, name,
 *     last_fired_time). An error here is the post-review's access flag: the
 *     system user cannot read the account or its pixel.
 *   - campaigns: objective, effective_status, created_time, start_time, budgets.
 *   - spend by campaign and day for the last 90 days: each campaign's first_spend,
 *     last_spend and spend_7d, plus the account's first_spend_90d and spend_7d, used
 *     for the new-client "is it live, and since when" check.
 *   - ad insights for last_7d, last_14d and last_30d (spend > 0 only).
 *   - every ACTIVE ad with its created_time and creative (kind, headline, primary text).
 * Writes .claude/skills/post-review/ads.json.
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const SKILL = path.join(ROOT, '.claude', 'skills', 'post-review');
const args = process.argv.slice(2);
const ci = args.indexOf('--clients');
const ONLY = ci >= 0 ? new Set(args.splice(ci, 2)[1].split('|').map((s) => s.trim().toLowerCase())) : null;
const RUN_DATE = args[0] ?? new Date().toISOString().slice(0, 10);
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
    if (!(key in process.env)) process.env[key] = line.slice(eq + 1).trim().replace(/^"(.*)"$/, '$1');
  }
}
const TOKEN = process.env.META_ACCESS_TOKEN;
if (!TOKEN) { console.error('[pull-ad-insights] META_ACCESS_TOKEN is not set in .env'); process.exit(2); }

interface Adv { client: string; am: string; id: string }
function advMap(): Adv[] {
  const py = fs.readFileSync(path.join(ROOT, '.claude', 'skills', 'client-benchmark', 'generate_report.py'), 'utf8');
  const block = py.slice(py.indexOf('ADV={'), py.indexOf('ADV_UNMAPPED'));
  const out: Adv[] = [];
  for (const m of block.matchAll(/^\s*"([^"]+)":\("([^"]*)","(\d+)","[^"]*","live"\)/gm)) out.push({ client: m[1], am: m[2], id: m[3] });
  return out;
}

async function get(url: string): Promise<any> {
  const res = await fetch(url);
  const body = (await res.json()) as any;
  if (body.error) throw new Error(`${body.error.code ?? ''} ${body.error.message}`.trim());
  return body;
}
async function getAll(url: string): Promise<any[]> {
  const out: any[] = []; let next = url;
  while (next) { const b = await get(next); out.push(...(b.data ?? [])); next = b.paging?.next ?? ''; }
  return out;
}
const n = (v: any) => (v === undefined || v === null || v === '' ? 0 : Number(v));
const act = (list: any[] | undefined, ...types: string[]) => {
  for (const t of types) { const v = list?.find((a) => a.action_type === t)?.value; if (v !== undefined) return Number(v); }
  return 0;
};
const r2 = (v: number) => Math.round(v * 100) / 100;

function metrics(r: any) {
  const spend = n(r.spend), impr = n(r.impressions), clicks = n(r.inline_link_clicks);
  const purch = act(r.actions, 'omni_purchase', 'purchase');
  const value = act(r.action_values, 'omni_purchase', 'purchase');
  const v3s = act(r.actions, 'video_view');
  const thru = act(r.video_thruplay_watched_actions, 'video_view');
  return {
    spend: r2(spend), impr, reach: n(r.reach), freq: r2(n(r.frequency)), clicks,
    link_ctr: impr ? r2((clicks / impr) * 100) : 0, cpm: r2(n(r.cpm)),
    purch, value: r2(value), roas: spend ? r2(value / spend) : 0,
    leads: act(r.actions, 'lead', 'onsite_conversion.lead_grouped'),
    hook: impr && v3s ? r2((v3s / impr) * 100) : null, // 3-second plays per impression, video ads only
    thru: thru || null,
  };
}

function creativeInfo(c: any) {
  if (!c) return { kind: 'unknown', headline: '', text: '' };
  const oss = c.object_story_spec ?? {}; const ld = oss.link_data ?? {}; const vd = oss.video_data ?? {}; const afs = c.asset_feed_spec ?? {};
  const video = c.video_id ?? vd.video_id ?? afs.videos?.[0]?.video_id;
  const kind = video ? 'video' : (ld.child_attachments?.length ? 'carousel' : (afs.images?.length > 1 ? 'flexible' : 'image'));
  const headline = ld.name ?? vd.title ?? afs.titles?.[0]?.text ?? c.title ?? '';
  const text = ld.message ?? vd.message ?? afs.bodies?.[0]?.text ?? c.body ?? '';
  return { kind, headline: String(headline).slice(0, 120), text: String(text).replace(/\s+/g, ' ').slice(0, 220) };
}

async function main() {
  const adv = advMap().filter((a) => !ONLY || ONLY.has(a.client.toLowerCase()));
  const t0 = new Date();
  const runMs = new Date(RUN_DATE + 'T00:00:00Z').getTime();
  const errors: string[] = [];
  const accounts: Record<string, any> = {};
  const insFields = 'ad_id,ad_name,adset_name,campaign_id,campaign_name,spend,impressions,reach,frequency,inline_link_clicks,cpm,actions,action_values,video_thruplay_watched_actions';
  for (const a of adv) {
    const rec: any = { id: a.id, am: a.am, access: { account: 'ok', pixel: 'ok' }, pixels: [], campaigns: [], first_spend_90d: null, spend_7d: 0, ads: [] };
    accounts[a.client] = rec;
    try {
      const info = await get(`${API}/act_${a.id}?fields=name,account_status,disable_reason,currency&access_token=${TOKEN}`);
      rec.name = info.name; rec.account_status = info.account_status; // 1 = active, 2 = disabled, 3 = unsettled, 7/8/9 = review or closed states
      if (info.account_status !== 1) rec.access.account = `account_status ${info.account_status}${info.disable_reason ? `, disable_reason ${info.disable_reason}` : ''}`;
    } catch (e: any) { rec.access.account = `error: ${e.message}`; errors.push(`${a.client} account: ${e.message}`); console.log(`${a.client.padEnd(30)} NO ACCESS ${e.message}`); continue; }
    try {
      rec.pixels = (await getAll(`${API}/act_${a.id}/adspixels?fields=id,name,last_fired_time,is_unavailable&access_token=${TOKEN}`))
        .map((p) => ({ id: p.id, name: p.name, last_fired: p.last_fired_time ?? null, unavailable: !!p.is_unavailable }));
      if (!rec.pixels.length) rec.access.pixel = 'no pixel visible to the system user';
    } catch (e: any) { rec.access.pixel = `error: ${e.message}`; errors.push(`${a.client} pixels: ${e.message}`); }
    try {
      rec.campaigns = (await getAll(`${API}/act_${a.id}/campaigns?fields=id,name,objective,effective_status,created_time,start_time,daily_budget,lifetime_budget&limit=200&access_token=${TOKEN}`))
        .map((c) => ({ id: c.id, name: c.name, objective: c.objective, status: c.effective_status, created: String(c.created_time ?? '').slice(0, 10), start: String(c.start_time ?? '').slice(0, 10), daily_budget: c.daily_budget ? n(c.daily_budget) / 100 : null }));
    } catch (e: any) { errors.push(`${a.client} campaigns: ${e.message}`); }
    try {
      // campaign x day spend for 90 days: when each campaign first and last spent (a launch date, unlike created_time)
      const days = await getAll(`${API}/act_${a.id}/insights?level=campaign&date_preset=last_90d&time_increment=1&fields=campaign_id,spend&limit=500&access_token=${TOKEN}`);
      const spent = days.filter((d) => n(d.spend) > 0).map((d) => ({ id: String(d.campaign_id), date: d.date_start as string, spend: n(d.spend) }));
      const cut = new Date(runMs - 7 * 86400e3).toISOString().slice(0, 10);
      const per = new Map<string, { first: string; last: string; s7: number }>();
      for (const d of spent) {
        const p = per.get(d.id) ?? { first: d.date, last: d.date, s7: 0 };
        if (d.date < p.first) p.first = d.date;
        if (d.date > p.last) p.last = d.date;
        if (d.date >= cut) p.s7 += d.spend;
        per.set(d.id, p);
      }
      for (const c of rec.campaigns) { const p = per.get(c.id); if (p) Object.assign(c, { first_spend: p.first, last_spend: p.last, spend_7d: r2(p.s7) }); }
      rec.first_spend_90d = spent.map((d) => d.date).sort()[0] ?? null;
      rec.spend_7d = r2(spent.filter((d) => d.date >= cut).reduce((s, d) => s + d.spend, 0));
    } catch (e: any) { errors.push(`${a.client} daily spend: ${e.message}`); }
    const byAd = new Map<string, any>();
    for (const win of [7, 14, 30]) {
      try {
        const rows = await getAll(`${API}/act_${a.id}/insights?level=ad&date_preset=last_${win}d&fields=${insFields}&limit=200&access_token=${TOKEN}`);
        for (const r of rows) {
          if (!(n(r.spend) > 0)) continue;
          const ad = byAd.get(r.ad_id) ?? { id: r.ad_id, name: r.ad_name, adset: r.adset_name, campaign_id: r.campaign_id, campaign: r.campaign_name };
          ad[`w${win}`] = metrics(r);
          byAd.set(r.ad_id, ad);
        }
      } catch (e: any) { errors.push(`${a.client} ad insights ${win}d: ${e.message}`); }
    }
    try {
      const active = await getAll(`${API}/act_${a.id}/ads?fields=id,name,adset{name},campaign_id,effective_status,created_time,creative{id,title,body,video_id,object_story_spec,asset_feed_spec}&effective_status=${encodeURIComponent('["ACTIVE"]')}&limit=50&access_token=${TOKEN}`);
      const camp = new Map(rec.campaigns.map((c: any) => [c.id, c.name]));
      for (const x of active) {
        const ad = byAd.get(x.id) ?? { id: x.id, name: x.name, adset: x.adset?.name ?? '', campaign_id: x.campaign_id, campaign: camp.get(x.campaign_id) ?? '' };
        Object.assign(ad, { status: x.effective_status, created: String(x.created_time ?? '').slice(0, 10), ...creativeInfo(x.creative) });
        byAd.set(x.id, ad);
      }
    } catch (e: any) { errors.push(`${a.client} active ads: ${e.message}`); }
    for (const ad of byAd.values()) {
      ad.status ??= 'NOT_ACTIVE';
      ad.age_days = ad.created ? Math.round((runMs - new Date(ad.created + 'T00:00:00Z').getTime()) / 86400e3) : null;
    }
    rec.ads = [...byAd.values()].sort((x, y) => (y.w14?.spend ?? 0) - (x.w14?.spend ?? 0) || (y.w30?.spend ?? 0) - (x.w30?.spend ?? 0));
    const live = rec.ads.filter((x: any) => x.status === 'ACTIVE').length;
    console.log(`${a.client.padEnd(30)} ${a.id.padEnd(18)} ${rec.campaigns.length} campaigns, ${rec.ads.length} ads (${live} active), 7d spend $${rec.spend_7d}${rec.access.pixel !== 'ok' ? `  pixel: ${rec.access.pixel}` : ''}`);
  }
  fs.mkdirSync(SKILL, { recursive: true });
  const out = { run_date: RUN_DATE, pulled_from: t0.toISOString(), pulled_to: new Date().toISOString(), windows: 'last_7d, last_14d, last_30d (Meta presets, ending the day before the run)', accounts, errors };
  fs.writeFileSync(path.join(SKILL, 'ads.json'), JSON.stringify(out));
  console.log(`\n${adv.length} accounts, ${errors.length} errors. Wrote .claude/skills/post-review/ads.json`);
  if (errors.length) console.log(errors.join('\n'));
}
main().catch((e) => { console.error(e); process.exit(1); });
