/**
 * Purchase value check: for each account, last N days, daily purchases vs
 * purchase conversion value from the Marketing API, to catch the Paradise
 * Pointe pattern (purchases recorded with no value). Prints a table; no files.
 *
 *   npx tsx scripts/purchase-value-check.mts [days=45] [acct,acct,...]
 */
import fs from 'fs'; import path from 'path'; import { fileURLToPath } from 'url';
const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
for (const file of ['.env.local', '.env']) { const p = path.join(ROOT, file); if (!fs.existsSync(p)) continue;
  for (const raw of fs.readFileSync(p, 'utf8').split('\n')) { const l = raw.trim(); if (!l || l.startsWith('#')) continue; const i = l.indexOf('='); if (i < 0) continue; const k = l.slice(0, i).trim(); if (!(k in process.env)) process.env[k] = l.slice(i + 1).trim().replace(/^"(.*)"$/, '$1'); } }
const TOKEN = process.env.META_ACCESS_TOKEN!; const API = 'https://graph.facebook.com/v21.0';
const DAYS = Number(process.argv[2] ?? 45);
const DEFAULT: Record<string, string> = { 'Awayframes': '2471256056603833', 'FLOHOM': '2100710320122219', 'Ridge & Falls': '1313401330776046', 'Inspired Retreats': '1494841894957652', 'Little River Landing': '884285717873613', 'Stay on 30a': '25640434272252212', 'Paradise Pointe': '1585826092078255', 'Stay Saluda NC': '1863632561215857', 'Treetop Escapes': '967636478877602', 'Taberg Falls': '827872700004659', 'The Cohost Company': '9141035462679902' };
const accts = process.argv[3] ? Object.fromEntries(process.argv[3].split(',').map((a) => [a, a])) : DEFAULT;
const until = new Date(); const since = new Date(until.getTime() - DAYS * 86400 * 1000);
const d = (x: Date) => x.toISOString().slice(0, 10);
const tr = encodeURIComponent(JSON.stringify({ since: d(since), until: d(until) }));
async function getAll(url: string) { const out: any[] = []; let next = url; while (next) { const b: any = await (await fetch(next)).json(); if (b.error) throw new Error(b.error.message); out.push(...(b.data ?? [])); next = b.paging?.next ?? ''; } return out; }
const num = (list: any[] | undefined, t: string) => Number(list?.find((a) => a.action_type === t)?.value ?? 0);
(async () => {
  console.log(`Window ${d(since)} to ${d(until)} (${DAYS} days). purchases = omni_purchase actions; value = omni_purchase action_values.\n`);
  console.log(`${'Client'.padEnd(22)} ${'purch'.padStart(6)} ${'value'.padStart(10)} ${'avg'.padStart(8)}  ${'days w/ purch'.padStart(13)} ${'0-value days'.padStart(12)} ${'purch on 0-value days'.padStart(21)}  pixel vs onsite  campaigns with purchases but no value`);
  for (const [name, id] of Object.entries(accts)) {
    try {
      const days = await getAll(`${API}/act_${id}/insights?level=account&time_increment=1&time_range=${tr}&fields=date_start,spend,actions,action_values&limit=100&access_token=${TOKEN}`);
      let p = 0, v = 0, dp = 0, dz = 0, pz = 0, pix = 0, pixv = 0, onsite = 0;
      const zeroDays: string[] = [];
      for (const r of days) { const c = num(r.actions, 'omni_purchase'); const val = num(r.action_values, 'omni_purchase'); p += c; v += val; pix += num(r.actions, 'offsite_conversion.fb_pixel_purchase'); pixv += num(r.action_values, 'offsite_conversion.fb_pixel_purchase'); onsite += num(r.actions, 'onsite_web_purchase') + num(r.actions, 'onsite_web_app_purchase'); if (c > 0) { dp++; if (val === 0) { dz++; pz += c; zeroDays.push(r.date_start.slice(5)); } } }
      const camps = await getAll(`${API}/act_${id}/insights?level=campaign&time_range=${tr}&fields=campaign_name,actions,action_values&limit=200&access_token=${TOKEN}`);
      const bad = camps.filter((c) => num(c.actions, 'omni_purchase') > 0 && num(c.action_values, 'omni_purchase') === 0).map((c) => `${c.campaign_name} (${num(c.actions, 'omni_purchase')})`);
      const partial = camps.filter((c) => num(c.actions, 'omni_purchase') > 0 && num(c.action_values, 'omni_purchase') > 0).map((c) => `${c.campaign_name.slice(0, 40)}: ${num(c.actions, 'omni_purchase')} purch, $${num(c.action_values, 'omni_purchase').toFixed(0)}`);
      console.log(`${name.padEnd(22)} ${String(p).padStart(6)} ${('$' + v.toFixed(0)).padStart(10)} ${(p ? '$' + (v / p).toFixed(0) : '-').padStart(8)}  ${String(dp).padStart(13)} ${String(dz).padStart(12)} ${String(pz).padStart(21)}  pixel ${pix}/$${pixv.toFixed(0)} onsite ${onsite}  ${bad.length ? bad.join('; ') : '-'}`);
      if (zeroDays.length) console.log(`${''.padEnd(22)} zero-value days: ${zeroDays.join(', ')}`);
      if (partial.length) console.log(`${''.padEnd(22)} with value: ${partial.join(' | ')}`);
    } catch (e: any) { console.log(`${name.padEnd(22)} ERROR ${e.message}`); }
  }
})();
