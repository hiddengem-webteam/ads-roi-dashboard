/**
 * Creative review pull: ranks an account's Sales-campaign ads over the last
 * 30 days, downloads the top (and bottom) creatives, and writes a manifest.
 *
 *   npx tsx scripts/pull-creatives.mts <client name as in PROJECT.md section 5> [YYYY-MM-DD] [--out DIR]
 *
 * Rules (Shawal, 2026-10-19): Sales campaigns only (OUTCOME_SALES), ads with
 * at least $100 spend in the last 30 days, ranked by purchase ROAS then
 * purchases; top 3 and bottom 3. Images come from the creative's image_url,
 * videos from act_<id>/advideos (source) or, for Page reels, through a
 * page-scoped token (GET only; nothing is ever written to a Page).
 * Output: <out>/<date>/<client>/ with the media files and manifest.json + manifest.md.
 */
import fs from 'fs'; import path from 'path'; import { fileURLToPath } from 'url';
const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
for (const file of ['.env.local', '.env']) { const p = path.join(ROOT, file); if (!fs.existsSync(p)) continue;
  for (const raw of fs.readFileSync(p, 'utf8').split('\n')) { const l = raw.trim(); if (!l || l.startsWith('#')) continue; const i = l.indexOf('='); if (i < 0) continue; const k = l.slice(0, i).trim(); if (!(k in process.env)) process.env[k] = l.slice(i + 1).trim().replace(/^"(.*)"$/, '$1'); } }
const TOKEN = process.env.META_ACCESS_TOKEN!; const API = 'https://graph.facebook.com/v21.0';
const args = process.argv.slice(2); const outIdx = args.indexOf('--out');
const OUT_BASE = outIdx >= 0 ? args.splice(outIdx, 2)[1] : path.join(ROOT, 'weekly', 'Creative Reviews', 'pulls');
const CLIENT = args[0]; const RUN_DATE = args[1] ?? new Date().toISOString().slice(0, 10);
const MIN_SPEND = 100, TOP = 3;
function account(client: string): { id: string; am: string } {
  const md = fs.readFileSync(path.join(ROOT, 'weekly', 'Project Data', 'PROJECT.md'), 'utf8');
  for (const line of md.split('\n')) { if (!line.startsWith('|')) continue; const c = line.slice(1, -1).split('|').map((x) => x.trim()); if (c.length >= 5 && /^\d{6,}$/.test(c[3]) && c[0].toLowerCase() === client.toLowerCase()) return { id: c[3], am: c[1] }; }
  throw new Error(`client "${client}" not in PROJECT.md section 5`);
}
async function get(url: string) { const b: any = await (await fetch(url)).json(); if (b.error) throw new Error(b.error.message); return b; }
async function getAll(url: string) { const out: any[] = []; let next = url; while (next) { const b = await get(next); out.push(...(b.data ?? [])); next = b.paging?.next ?? ''; } return out; }
const act = (l: any[] | undefined, t: string) => Number(l?.find((a) => a.action_type === t)?.value ?? 0);
async function download(url: string, file: string) { const r = await fetch(url); if (!r.ok) throw new Error(`HTTP ${r.status}`); fs.writeFileSync(file, Buffer.from(await r.arrayBuffer())); return fs.statSync(file).size; }
const safe = (s: string) => s.replace(/[^\w.-]+/g, '_').slice(0, 60);
(async () => {
  const { id: acct, am } = account(CLIENT);
  const outDir = path.join(OUT_BASE, RUN_DATE, safe(CLIENT)); fs.mkdirSync(outDir, { recursive: true });
  const camps = await getAll(`${API}/act_${acct}/campaigns?fields=id,name,objective,effective_status&limit=200&access_token=${TOKEN}`);
  const sales = new Map(camps.filter((c) => c.objective === 'OUTCOME_SALES').map((c) => [c.id, c]));
  const ins = await getAll(`${API}/act_${acct}/insights?level=ad&date_preset=last_30d&fields=ad_id,ad_name,adset_name,campaign_id,campaign_name,spend,impressions,reach,frequency,ctr,inline_link_clicks,cost_per_inline_link_click,actions,action_values,purchase_roas&limit=500&access_token=${TOKEN}`);
  const rows = ins.filter((r) => sales.has(r.campaign_id)).map((r) => ({
    ad_id: r.ad_id, ad: r.ad_name, adset: r.adset_name, campaign: r.campaign_name, spend: Number(r.spend), impressions: Number(r.impressions), reach: Number(r.reach), frequency: Number(r.frequency), ctr: Number(r.ctr), clicks: Number(r.inline_link_clicks ?? 0), cpc: Number(r.cost_per_inline_link_click ?? 0),
    purchases: act(r.actions, 'omni_purchase'), value: act(r.action_values, 'omni_purchase'), roas: act(r.purchase_roas, 'omni_purchase'), add_to_cart: act(r.actions, 'omni_add_to_cart'), checkout: act(r.actions, 'omni_initiated_checkout'),
  }));
  const ranked = rows.filter((r) => r.spend >= MIN_SPEND).sort((a, b) => (b.roas - a.roas) || (b.purchases - a.purchases) || (b.spend - a.spend));
  const under = rows.filter((r) => r.spend < MIN_SPEND);
  const top = ranked.slice(0, TOP); const bottom = ranked.length > TOP ? ranked.slice(-TOP).reverse().filter((r) => !top.includes(r)) : [];
  console.log(`${CLIENT} (${acct}): ${sales.size} sales campaigns, ${rows.length} ads with spend in 30d, ${ranked.length} over $${MIN_SPEND}, ${under.length} under.`);
  const picks = [...top.map((r) => ({ ...r, rank: 'top' })), ...bottom.map((r) => ({ ...r, rank: 'bottom' }))];
  const manifest: any[] = [];
  for (const [i, r] of picks.entries()) {
    const ad = await get(`${API}/${r.ad_id}?fields=name,status,creative{id,name,image_url,thumbnail_url,video_id,object_story_spec,asset_feed_spec,effective_object_story_id}&access_token=${TOKEN}`);
    const c = ad.creative ?? {}; const oss = c.object_story_spec ?? {}; const ld = oss.link_data ?? {}; const vd = oss.video_data ?? {}; const afs = c.asset_feed_spec ?? {};
    const copy = { primary_text: ld.message ?? vd.message ?? afs.bodies?.[0]?.text ?? '', headline: ld.name ?? vd.title ?? afs.titles?.[0]?.text ?? '', description: ld.description ?? vd.link_description ?? afs.descriptions?.[0]?.text ?? '', link: ld.link ?? vd.call_to_action?.value?.link ?? afs.link_urls?.[0]?.website_url ?? '', cta: ld.call_to_action?.type ?? vd.call_to_action?.type ?? afs.call_to_action_types?.[0] ?? '' };
    const prefix = `${String(i + 1).padStart(2, '0')}_${r.rank}_${safe(r.ad)}`;
    const files: string[] = []; const urls: Record<string, string> = {}; let kind = 'other'; const notes: string[] = [];
    const videoId = c.video_id ?? vd.video_id ?? afs.videos?.[0]?.video_id;
    const cards = ld.child_attachments ?? [];
    try {
      if (videoId) {
        kind = 'video';
        let v = await get(`${API}/${videoId}?fields=source,length,from,permalink_url&access_token=${TOKEN}`);
        if (!v.source && v.from?.id) { const pt = (await get(`${API}/${v.from.id}?fields=access_token&access_token=${TOKEN}`)).access_token; if (pt) v = await get(`${API}/${videoId}?fields=source,length,from,permalink_url&access_token=${pt}`); notes.push(`video owned by Page ${v.from?.name}, read with a page-scoped token`); }
        if (v.source) { const f = `${prefix}.mp4`; const sz = await download(v.source, path.join(outDir, f)); files.push(f); urls[f] = v.source; notes.push(`${(v.length ?? 0).toFixed?.(1) ?? v.length}s, ${(sz / 1e6).toFixed(1)} MB`); }
        else notes.push('video source not available');
        const th = c.thumbnail_url ? (await get(`${API}/${c.id}?fields=thumbnail_url&thumbnail_width=1080&thumbnail_height=1080&access_token=${TOKEN}`)).thumbnail_url : null;
        if (th) { const f = `${prefix}_thumb.jpg`; await download(th, path.join(outDir, f)); files.push(f); urls[f] = th; }
      } else if (cards.length) {
        kind = 'carousel';
        for (const [j, card] of cards.entries()) { const u = card.picture ?? (card.image_hash ? (await get(`${API}/act_${acct}/adimages?hashes=["${card.image_hash}"]&fields=url&access_token=${TOKEN}`)).data?.[0]?.url : null); if (u) { const f = `${prefix}_card${j + 1}.jpg`; await download(u, path.join(outDir, f)); files.push(f); urls[f] = u; } }
        notes.push(`${cards.length} cards: ` + cards.map((x: any) => x.name ?? '').filter(Boolean).join(' | '));
      } else {
        kind = 'image';
        let u = c.image_url; if (!u && ld.image_hash) u = (await get(`${API}/act_${acct}/adimages?hashes=["${ld.image_hash}"]&fields=url&access_token=${TOKEN}`)).data?.[0]?.url;
        if (!u && afs.images?.[0]?.hash) u = (await get(`${API}/act_${acct}/adimages?hashes=["${afs.images[0].hash}"]&fields=url&access_token=${TOKEN}`)).data?.[0]?.url;
        if (u) { const f = `${prefix}.jpg`; await download(u, path.join(outDir, f)); files.push(f); urls[f] = u; } else notes.push('no image url on the creative');
      }
    } catch (e: any) { notes.push(`download error: ${e.message}`); }
    manifest.push({ rank: r.rank, position: i + 1, kind, files, urls, copy, notes, ...r });
    console.log(`  ${r.rank.padEnd(6)} ${kind.padEnd(8)} ROAS ${r.roas.toFixed(1)}x  ${String(r.purchases).padStart(3)} purch  $${r.spend.toFixed(0).padStart(5)}  CTR ${r.ctr.toFixed(2)}%  freq ${r.frequency.toFixed(1)}  ${r.ad.slice(0, 50)}  [${files.join(', ') || notes.join('; ')}]`);
  }
  fs.writeFileSync(path.join(outDir, 'manifest.json'), JSON.stringify({ client: CLIENT, account: acct, am, run_date: RUN_DATE, window: 'last_30d', min_spend: MIN_SPEND, rule: 'Sales campaigns only, ranked by purchase ROAS then purchases', ranked: ranked.length, under_min_spend: under.map((r) => ({ ad: r.ad, campaign: r.campaign, spend: r.spend })), ads: manifest }, null, 1));
  const L = [`# Creative pull: ${CLIENT}, ${RUN_DATE}`, '', `Account ${acct} (AM ${am}). Sales campaigns only, last 30 days, ads with at least $${MIN_SPEND} spend ranked by purchase ROAS then purchases. ${ranked.length} ads ranked, ${under.length} under the spend floor.`, '', '| # | Rank | Ad | Campaign | Kind | Spend | Purchases | Value | ROAS | CTR | Freq | Files |', '|---|---|---|---|---|---|---|---|---|---|---|---|'];
  for (const m of manifest) L.push(`| ${m.position} | ${m.rank} | ${m.ad} | ${m.campaign} | ${m.kind} | $${m.spend.toFixed(0)} | ${m.purchases} | $${m.value.toFixed(0)} | ${m.roas.toFixed(1)}x | ${m.ctr.toFixed(2)}% | ${m.frequency.toFixed(1)} | ${m.files.join(', ')} |`);
  L.push('', '## Copy', '');
  for (const m of manifest) L.push(`### ${m.position}. ${m.ad} (${m.rank})`, '', `Headline: ${m.copy.headline || '—'}`, '', `Primary text: ${m.copy.primary_text || '—'}`, '', `CTA: ${m.copy.cta || '—'} → ${m.copy.link || '—'}`, '', m.notes.length ? `Notes: ${m.notes.join('; ')}` : '', '');
  fs.writeFileSync(path.join(outDir, 'manifest.md'), L.join('\n'));
  console.log(`\nwrote ${path.relative(ROOT, outDir)}/ (${manifest.length} ads, manifest.json + manifest.md)`);
})().catch((e) => { console.error(e); process.exit(1); });
