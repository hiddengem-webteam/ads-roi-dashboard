/**
 * Weekly Instagram reels pull: ranks a client's recent reels against the account's
 * own median, downloads the outperformers (video + audio track + contact sheet)
 * and writes a manifest for the reels review.
 *
 *   npx tsx scripts/pull-ig-reels.mts <client name as the Facebook Page is named> [YYYY-MM-DD] [--days 90] [--top 5] [--out DIR]
 *
 * Access (2026-10-21): the HiddenGem-Claude system user token (META_ACCESS_TOKEN in .env)
 * with instagram_basic + instagram_manage_insights. /me/accounts does not expand the IG
 * account for a system user, so the Page's own token resolves it; media and insights
 * are then read with the system user token. Reels with licensed audio carry no media_url,
 * so downloads go through yt-dlp from the permalink. Audio is extracted for identification
 * and the music ledger; nothing is ever written to Instagram.
 * Output: <out>/<date>/<client>/ with NN_<code>.mp4, NN_<code>_audio.m4a, NN_<code>_contact.jpg,
 *         manifest.json + manifest.md (every reel in the window, ranked).
 */
import fs from 'fs'; import path from 'path'; import { fileURLToPath } from 'url'; import { execFileSync } from 'child_process';
const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
for (const file of ['.env.local', '.env']) { const p = path.join(ROOT, file); if (!fs.existsSync(p)) continue;
  for (const raw of fs.readFileSync(p, 'utf8').split('\n')) { const l = raw.trim(); if (!l || l.startsWith('#')) continue; const i = l.indexOf('='); if (i < 0) continue; const k = l.slice(0, i).trim(); if (!(k in process.env)) process.env[k] = l.slice(i + 1).trim().replace(/^"(.*)"$/, '$1'); } }
const TOKEN = process.env.META_ACCESS_TOKEN!; const API = 'https://graph.facebook.com/v21.0';
if (!TOKEN) throw new Error('META_ACCESS_TOKEN missing in .env');
const args = process.argv.slice(2);
const opt = (name: string, dflt: string) => { const i = args.indexOf(name); return i >= 0 ? args.splice(i, 2)[1] : dflt; };
const OUT_BASE = opt('--out', path.join(ROOT, 'weekly', 'IG Reel Reviews', 'pulls'));
const DAYS = Number(opt('--days', '90')); const TOP = Number(opt('--top', '5'));
const CLIENT = args[0]; const RUN_DATE = args[1] ?? new Date().toISOString().slice(0, 10);
if (!CLIENT) throw new Error('usage: pull-ig-reels.mts <client> [date] [--days N] [--top N]');
const METRICS = 'views,reach,saved,shares,likes,comments,total_interactions,ig_reels_avg_watch_time,ig_reels_video_view_total_time';
async function get(url: string) { const b: any = await (await fetch(url)).json(); if (b.error) throw new Error(b.error.message); return b; }
async function getAll(url: string, stop?: (row: any) => boolean) { const out: any[] = []; let next = url; while (next) { const b = await get(next); out.push(...(b.data ?? [])); if (stop && b.data?.some(stop)) break; next = b.paging?.next ?? ''; } return out; }
const safe = (s: string) => s.replace(/[^\w.-]+/g, '_').slice(0, 60);
const median = (xs: number[]) => { const s = [...xs].sort((a, b) => a - b); const m = s.length >> 1; return s.length ? (s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2) : 0; };
function run(cmd: string, a: string[]) { try { return execFileSync(cmd, a, { stdio: ['ignore', 'pipe', 'pipe'] }).toString(); } catch (e: any) { throw new Error(`${cmd} failed: ${(e.stderr ?? e.message).toString().trim().split('\n').pop()}`); } }
(async () => {
  const pages = await getAll(`${API}/me/accounts?fields=id,name,access_token&limit=100&access_token=${TOKEN}`);
  const page = pages.find((p) => p.name.trim().toLowerCase() === CLIENT.trim().toLowerCase());
  if (!page) throw new Error(`no Facebook Page named "${CLIENT}" on this system user (have: ${pages.map((p) => p.name.trim()).sort().join(', ')})`);
  const ig = (await get(`${API}/${page.id}?fields=instagram_business_account{id,username,followers_count,media_count}&access_token=${page.access_token}`)).instagram_business_account;
  if (!ig) throw new Error(`Page "${page.name}" has no linked Instagram account`);
  const since = new Date(RUN_DATE); since.setDate(since.getDate() - DAYS);
  const media = await getAll(`${API}/${ig.id}/media?fields=id,shortcode,media_product_type,media_type,timestamp,permalink,caption,like_count,comments_count,media_url,thumbnail_url&limit=100&access_token=${TOKEN}`, (m) => new Date(m.timestamp) < since);
  const reels = media.filter((m) => m.media_product_type === 'REELS' && new Date(m.timestamp) >= since);
  console.log(`${page.name} -> @${ig.username} (${ig.followers_count} followers): ${media.length} media read, ${reels.length} reels in the last ${DAYS} days`);
  const rows: any[] = [];
  for (const r of reels) {
    let ins: Record<string, number> = {};
    try { const d = await get(`${API}/${r.id}/insights?metric=${METRICS}&access_token=${TOKEN}`); for (const m of d.data ?? []) ins[m.name] = Number(m.values?.[0]?.value ?? 0); } catch (e: any) { ins = { error: 1 }; }
    const code = r.shortcode ?? r.permalink.split('/').filter(Boolean).pop();
    rows.push({ id: r.id, code, date: r.timestamp.slice(0, 10), permalink: r.permalink, caption: (r.caption ?? '').replace(/\s+/g, ' ').trim(), has_media_url: Boolean(r.media_url), thumbnail_url: r.thumbnail_url ?? null,
      views: ins.views ?? 0, reach: ins.reach ?? 0, saved: ins.saved ?? 0, shares: ins.shares ?? 0, likes: ins.likes ?? r.like_count ?? 0, comments: ins.comments ?? r.comments_count ?? 0, interactions: ins.total_interactions ?? 0,
      avg_watch_s: (ins.ig_reels_avg_watch_time ?? 0) / 1000, insights_error: ins.error ? true : false });
  }
  const medViews = median(rows.map((r) => r.views)); const medReach = median(rows.map((r) => r.reach));
  for (const r of rows) { r.views_x_median = medViews ? r.views / medViews : 0; r.save_rate = r.views ? r.saved / r.views : 0; r.share_rate = r.views ? r.shares / r.views : 0; }
  rows.sort((a, b) => (b.views_x_median - a.views_x_median) || (b.reach - a.reach));
  const outDir = path.join(OUT_BASE, RUN_DATE, safe(CLIENT)); fs.mkdirSync(outDir, { recursive: true });
  console.log(`median views ${medViews}, median reach ${medReach}. Top ${TOP}:`);
  const picks = rows.slice(0, TOP);
  for (const [i, r] of picks.entries()) {
    const prefix = `${String(i + 1).padStart(2, '0')}_${r.code}`; r.rank = i + 1; r.files = []; r.notes = [];
    try {
      run('yt-dlp', ['-q', '--no-warnings', '--no-simulate', '-o', path.join(outDir, `${prefix}.%(ext)s`), r.permalink]);
      const vid = fs.readdirSync(outDir).find((f) => f.startsWith(prefix + '.') && !f.endsWith('.jpg') && !f.endsWith('.m4a'));
      if (!vid) throw new Error('yt-dlp wrote no file');
      const vp = path.join(outDir, vid); r.files.push(vid);
      const probe = run('ffprobe', ['-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height:format=duration', '-of', 'csv=p=0', vp]).trim().split(/[\n,]/);
      r.duration_s = Number(probe[probe.length - 1]); r.size = `${probe[0]}x${probe[1]}`;
      const hasAudio = run('ffprobe', ['-v', 'error', '-select_streams', 'a', '-show_entries', 'stream=codec_name', '-of', 'csv=p=0', vp]).trim();
      if (hasAudio) { run('ffmpeg', ['-v', 'error', '-y', '-i', vp, '-vn', '-c:a', 'copy', path.join(outDir, `${prefix}_audio.m4a`)]); r.files.push(`${prefix}_audio.m4a`); } else r.notes.push('no audio stream');
      const cols = 8, rowsN = Math.max(1, Math.ceil(Math.ceil(r.duration_s) / cols));
      run('ffmpeg', ['-v', 'error', '-y', '-i', vp, '-vf', `fps=1,scale=180:-1,tile=${cols}x${rowsN}`, path.join(outDir, `${prefix}_contact.jpg`)]); r.files.push(`${prefix}_contact.jpg`);
    } catch (e: any) { r.notes.push(e.message); }
    console.log(`  #${r.rank} ${r.date} ${r.views.toString().padStart(7)} views (${r.views_x_median.toFixed(1)}x) reach ${r.reach} saves ${r.saved} shares ${r.shares} ${r.duration_s ? r.duration_s.toFixed(1) + 's' : ''} ${r.permalink} ${r.notes.join('; ')}`);
  }
  fs.writeFileSync(path.join(outDir, 'manifest.json'), JSON.stringify({ client: CLIENT, page_id: page.id, ig_id: ig.id, username: ig.username, followers: ig.followers_count, run_date: RUN_DATE, window_days: DAYS, reels: rows.length, median_views: medViews, median_reach: medReach, rule: 'reels in window ranked by views over the account median, then reach', top: TOP, rows }, null, 1));
  const L = [`# IG reels pull: ${CLIENT} (@${ig.username}), ${RUN_DATE}`, '', `${ig.followers_count} followers. ${rows.length} reels in the last ${DAYS} days. Median views ${medViews}, median reach ${medReach}. Ranked by views over the account median, then reach; top ${TOP} downloaded.`, '',
    '| # | Date | Views | x median | Reach | Saves | Shares | Likes | Comments | Avg watch | Len | Audio | Caption | Link |', '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|'];
  for (const [i, r] of rows.entries()) L.push(`| ${i + 1} | ${r.date} | ${r.views} | ${r.views_x_median.toFixed(1)}x | ${r.reach} | ${r.saved} | ${r.shares} | ${r.likes} | ${r.comments} | ${r.avg_watch_s.toFixed(1)}s | ${r.duration_s ? r.duration_s.toFixed(0) + 's' : ''} | ${r.has_media_url ? 'own/cleared' : 'licensed?'} | ${r.caption.slice(0, 70).replace(/\|/g, '/')} | [reel](${r.permalink}) |`);
  L.push('', 'Audio column: Meta omits media_url on reels that carry copyrighted audio, so "licensed?" means the API withheld the file and the track is probably a licensed one; "own/cleared" means the file was served (original or royalty-free audio). Confirm by listening or fingerprinting before reuse.');
  fs.writeFileSync(path.join(outDir, 'manifest.md'), L.join('\n'));
  console.log(`\nwrote ${path.relative(ROOT, outDir)}/ (${rows.length} reels ranked, ${picks.length} downloaded)`);
})();
