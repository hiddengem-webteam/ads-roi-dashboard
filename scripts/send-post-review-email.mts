/**
 * Monday post-review email (2026-11-16, Shawal): a short summary that links to the full
 * post-review page on the weekly site. Email clients cannot run toggles, so the email
 * carries the top actions, one line per listed client and the AM messages; the page
 * (attached, and linked when WEEKLY_SITE_URL is set in .env) carries the detail.
 *
 *   npx tsx scripts/send-post-review-email.mts YYYY-MM-DD [--dry-run]
 *
 * Reads  weekly/Post-Review/Weekly Checks/DATE-post-review.json (+ .html to attach)
 * Writes weekly/Post-Review/Weekly Checks/DATE-post-review-email.html (what was sent)
 * Sends through Mailtrap only (scripts/lib/mailtrap.mts), to shawal@hiddengem.media.
 */
import fs from 'fs';
import path from 'path';
import { ROOT, OWNER, EMAIL as C, escHtml as esc, sendMail, loadEnv } from './lib/mailtrap.mts';

const args = process.argv.slice(2);
const DRY = args.includes('--dry-run');
const DATE = args.find((a) => /^\d{4}-\d{2}-\d{2}$/.test(a)) ?? new Date().toISOString().slice(0, 10);
if (args.includes('--check')) {  // preflight before the run's data pulls (HiddenGem email rule)
  const { pickSender } = await import('./lib/mailtrap.mts');
  try { const s = await pickSender(); console.log(`Mailtrap ok: will send from ${s.from} (${s.note})`); process.exit(0); }
  catch (e: any) { console.error(`Mailtrap cannot send: ${e.message}`); process.exit(1); }
}
const DIR = path.join(ROOT, 'weekly', 'Post-Review', 'Weekly Checks');
const pr = JSON.parse(fs.readFileSync(path.join(DIR, `${DATE}-post-review.json`), 'utf8'));
loadEnv();
const SITE = (process.env.WEEKLY_SITE_URL ?? '').replace(/\/+$/, '');
const PAGE = SITE ? `${SITE}/weekly/post-review/${DATE}.html` : '';
const nice = new Date(DATE + 'T12:00:00Z').toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric', timeZone: 'UTC' });

const S = pr.sections ?? {};
const flagged: any[] = S.flagged ?? [], scale: any[] = S.scale ?? [], freq: any[] = S.frequency ?? [], fresh: any[] = S.new_clients ?? [];
const late = fresh.filter((x) => ['late', 'blocked', 'due'].includes(x.status));  // new clients to chase this week
const newTasks: string[] = pr.tasks_added ?? [];

// **bold** and `code` only, like the weekly pages
const md = (s: string) => esc(s).replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>').replace(/`(.+?)`/g, '<code style="font-family:Menlo,monospace;font-size:13px">$1</code>');
const TONE: Record<string, [string, string, string]> = {
  flag: [C.red, C.redBg, 'Flag'], review: [C.amber, C.amberBg, 'Review'], scale: [C.goldInk, '#FFF9DB', 'Scale'], freq: [C.amber, C.amberBg, 'Frequency'],
  late: [C.red, C.redBg, 'Late'], blocked: [C.red, C.redBg, 'Blocked'], due: [C.amber, C.amberBg, 'Due soon'], live: [C.green, C.greenBg, 'Live'], 'not-started': [C.text3, C.grayBg, 'Not started'], watch: [C.text3, C.grayBg, 'Watch'],
};
const pill = (k: string) => { const [fg, bg, label] = TONE[k] ?? [C.text3, C.grayBg, k]; return `<span style="display:inline-block;padding:1px 8px;border-radius:999px;background:${bg};color:${fg};font-size:12px;line-height:18px;font-weight:600;white-space:nowrap">${esc(label)}</span>`; };
const button = (href: string, label: string) => href
  ? `<table role="presentation" cellpadding="0" cellspacing="0" width="100%"><tr><td style="padding:4px 0 0"><a href="${esc(href)}" style="display:block;background:${C.gold};color:${C.ink};text-decoration:none;font-weight:600;font-size:16px;line-height:48px;text-align:center;border-radius:8px">${esc(label)}</a></td></tr></table>`
  : `<p style="margin:4px 0 0;font-size:14px;line-height:20px;color:${C.text3}">The full review with toggles is attached (${esc(DATE)}-post-review.html) and goes live on the weekly site at /weekly/post-review/ after the next push.</p>`;
const h2 = (t: string, n: number) => `<tr><td style="padding:28px 0 8px;font-size:13px;line-height:16px;font-weight:600;letter-spacing:.04em;text-transform:uppercase;color:${C.text3}">${esc(t)} · ${n}</td></tr>`;

// one line per client: name, state, next step. Numbers and the reasoning stay on the page.
function itemRow(x: any, kind: string) {
  const first = [...(x.budget ?? []), ...(x.creative ?? []), ...(x.next ?? [])][0] ?? x.read ?? '';
  return `<tr><td style="padding:8px 0;border-top:1px solid ${C.line};font-size:15px;line-height:22px;color:${C.text2}">
<strong style="color:${C.ink}">${esc(x.client)}</strong> ${pill(x.status ?? kind)} ${md(first)}
</td></tr>`;
}
const section = (title: string, rows: any[], kind: string) => rows.length ? h2(title, rows.length) + rows.map((x) => itemRow(x, kind)).join('') : '';

const top: any[] = (pr.top_actions ?? []).slice(0, 6);
const statusLine = [
  `${flagged.length} flagged`, `${scale.length} scale`, `${freq.length} frequency`,
  `${late.length} new client${late.length === 1 ? '' : 's'} to chase`,
  `${newTasks.length} task${newTasks.length === 1 ? '' : 's'} added to the Fix List`,
].join(' · ');

const html = `<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light only"><title>Meta Ads post-review ${esc(nice)}</title></head>
<body style="margin:0;padding:0;background:#F4F4F5">
<div style="display:none;max-height:0;overflow:hidden">${esc(pr.summary ?? '')}</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#F4F4F5"><tr><td align="center" style="padding:24px 12px">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:600px;background:#FFFFFF;border:1px solid ${C.line};border-radius:12px;font-family:${C.font}">
<tr><td style="padding:24px 24px 8px">
<div style="font-size:13px;line-height:16px;font-weight:600;color:${C.goldInk};letter-spacing:.04em;text-transform:uppercase">HiddenGem · Meta Ads</div>
<h1 style="margin:6px 0 4px;font-size:24px;line-height:30px;color:${C.ink};font-weight:600">Post-review, ${esc(nice)}</h1>
<div style="font-size:14px;line-height:20px;color:${C.text3}">${esc(statusLine)}</div>
<p style="margin:14px 0 16px;font-size:16px;line-height:24px;color:${C.text2}">${md(pr.summary ?? '')}</p>
${button(PAGE, 'Open the full review')}
</td></tr>
<tr><td style="padding:0 24px 24px"><table role="presentation" width="100%" cellpadding="0" cellspacing="0">
${top.length ? h2('Do this week', top.length) + top.map((t, i) => `<tr><td style="padding:8px 0;border-top:1px solid ${C.line};font-size:15px;line-height:22px;color:${C.ink}"><strong>${i + 1}. ${esc(t.client)}:</strong> ${md(t.text)}</td></tr>`).join('') : ''}
${section('Flagged', flagged, 'flag')}
${section('Scale candidates', scale, 'scale')}
${section('Frequency watch', freq, 'freq')}
${section('New clients to chase', late, 'watch')}
${(pr.am_messages ?? []).length ? h2('Messages to AMs (creatives)', pr.am_messages.length) + pr.am_messages.map((m: any) => `<tr><td style="padding:10px 0;border-top:1px solid ${C.line}"><div style="font-size:15px;line-height:22px;color:${C.ink};font-weight:600">To ${esc(m.am)} <span style="font-weight:400;color:${C.text3};font-size:13px">${esc((m.clients ?? []).join(', '))}</span></div><div style="margin-top:6px;padding:12px 14px;background:${C.panel};border:1px solid ${C.line};border-radius:8px;font-size:15px;line-height:22px;color:${C.text2};white-space:pre-wrap">${esc(m.message)}</div></td></tr>`).join('') : ''}
<tr><td style="padding:24px 0 0">${button(PAGE, 'Open the full review')}</td></tr>
<tr><td style="padding:16px 0 0;font-size:12px;line-height:18px;color:${C.text3}">Built from the ${esc(DATE)} ad spend, pixel and benchmark checks, the ad-level Meta pull, the CRM and the Fix List. Tasks live in the Meta Ads Fix List.</td></tr>
</table></td></tr>
</table></td></tr></table></body></html>`;

const text = [
  `Meta Ads post-review, ${nice}`, statusLine, '', pr.summary ?? '', '', PAGE ? `Full review: ${PAGE}` : 'Full review attached.', '',
  ...(top.length ? ['DO THIS WEEK', ...top.map((t, i) => `${i + 1}. ${t.client}: ${t.text}`), ''] : []),
  ...[['FLAGGED', flagged], ['SCALE', scale], ['FREQUENCY', freq], ['NEW CLIENTS', fresh]].flatMap(([t, rows]: any) => rows.length ? [t, ...rows.map((x: any) => `- ${x.client}: ${x.read}`), ''] : []),
  ...((pr.am_messages ?? []).length ? ['MESSAGES TO AMS', ...pr.am_messages.flatMap((m: any) => [`To ${m.am}:`, m.message, ''])] : []),
].join('\n').replace(/\*\*|`/g, '');

fs.writeFileSync(path.join(DIR, `${DATE}-post-review-email.html`), html);
console.log(`wrote weekly/Post-Review/Weekly Checks/${DATE}-post-review-email.html (${html.length} bytes)`);
if (DRY) { console.log('dry run: not sent'); process.exit(0); }

const pagePath = path.join(DIR, `${DATE}-post-review.html`);
const attachments = fs.existsSync(pagePath) ? [{ filename: `${DATE}-post-review.html`, content: fs.readFileSync(pagePath).toString('base64'), type: 'text/html' }] : [];
sendMail({ to: [OWNER], subject: `Meta Ads post-review, ${nice}: ${flagged.length} flagged, ${scale.length} scale, ${late.length} new clients to chase`, html, text, category: 'post-review', attachments })
  .then(({ ids, sender }) => console.log(`sent to ${OWNER} from ${sender.from} (${sender.note}); message ${ids.join(', ')}`))
  .catch((e) => { console.error(`NOT SENT: ${e.message}`); console.log('\n' + text); process.exit(1); });
