/**
 * End-of-day Meta Ads Fix List email (2026-11-16, Shawal): the tasks ticked off today on the
 * Fix List artifact (https://claude.ai/artifact/5Zraak85dw6QaXeFWVJWJn), sent around 4:30 pm.
 *
 *   npx tsx scripts/send-fixlist-digest.mts --dump DIR [--names FILE] [--hours N] [--end ISO] [--dry-run]
 *
 * DIR is an ArtifactData out_dir dump of the artifact's `tasks` collection (DIR/tasks/<id>.json),
 * made by the session that runs this (the artifact database is only reachable through ArtifactData).
 * FILE maps doneBy user ids to names ({"u_...": "Shawal"}), from ArtifactData action "profiles".
 * Window: the hours since the previous digest, ending now (or --end): 24 hours, or 72 on a Monday so the
 * weekend is covered by a Monday-to-Friday schedule. A fixed calendar day would drop tasks ticked after the
 * 4:30 pm send. Sends through Mailtrap only (scripts/lib/mailtrap.mts).
 */
import fs from 'fs';
import path from 'path';
import { ROOT, OWNER, EMAIL as C, escHtml as esc, sendMail } from './lib/mailtrap.mts';

const args = process.argv.slice(2);
const flag = (k: string) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : undefined; };
const DRY = args.includes('--dry-run');
const DUMP = flag('--dump');
if (!DUMP) { console.error('usage: send-fixlist-digest.mts --dump DIR [--names FILE] [--hours N] [--end ISO] [--dry-run]'); process.exit(2); }
const TZ = 'America/Toronto';
const localDay = (iso: string) => new Intl.DateTimeFormat('en-CA', { timeZone: TZ, year: 'numeric', month: '2-digit', day: '2-digit' }).format(new Date(iso));
const END = flag('--end') ? new Date(flag('--end')!) : new Date();
const DATE = localDay(END.toISOString());
const weekday = new Intl.DateTimeFormat('en-US', { timeZone: TZ, weekday: 'short' }).format(END);
const HOURS = Number(flag('--hours') ?? (weekday === 'Mon' ? 72 : 24));
const START = new Date(END.getTime() - HOURS * 3600e3);
const inWindow = (iso?: string) => !!iso && new Date(iso) > START && new Date(iso) <= END;
const names: Record<string, string> = flag('--names') ? JSON.parse(fs.readFileSync(flag('--names')!, 'utf8')) : {};
const FIXLIST = 'https://claude.ai/artifact/5Zraak85dw6QaXeFWVJWJn';

const tdir = path.join(DUMP, 'tasks');
const tasks = fs.readdirSync(tdir).filter((f) => f.endsWith('.json')).map((f) => {
  const raw = JSON.parse(fs.readFileSync(path.join(tdir, f), 'utf8'));
  return { id: f.replace(/\.json$/, ''), ...(raw.data ?? raw) };
});
const done = tasks.filter((t: any) => t.done && inWindow(t.doneAt))
  .sort((a: any, b: any) => String(a.account).localeCompare(String(b.account)) || String(a.doneAt).localeCompare(String(b.doneAt)));
const added = tasks.filter((t: any) => inWindow(t.createdAt));
const open = tasks.filter((t: any) => !t.done);
const nice = new Date(DATE + 'T12:00:00Z').toLocaleDateString('en-GB', { weekday: 'long', day: 'numeric', month: 'short', timeZone: 'UTC' });
const who = (t: any) => names[t.doneBy] ?? (t.doneBy ? 'a teammate' : '');
const time = (iso: string) => new Intl.DateTimeFormat('en-US', { timeZone: TZ, hour: 'numeric', minute: '2-digit' }).format(new Date(iso));

const byAcct = new Map<string, any[]>();
for (const t of done) byAcct.set(t.account, [...(byAcct.get(t.account) ?? []), t]);
const openFix = open.filter((t: any) => t.priority === 'fix').length;
const since = new Intl.DateTimeFormat('en-US', { timeZone: TZ, weekday: 'short', hour: 'numeric', minute: '2-digit' }).format(START);
const status = `${done.length} done since ${since} · ${added.length} added · ${open.length} open (${openFix} fixes)`;

const rows = [...byAcct.entries()].map(([acct, ts]) => `<tr><td style="padding:12px 0 4px;font-size:13px;line-height:16px;font-weight:600;letter-spacing:.04em;text-transform:uppercase;color:${C.text3}">${esc(acct)} · ${ts.length}</td></tr>`
  + ts.map((t) => `<tr><td style="padding:8px 0;border-top:1px solid ${C.line};font-size:15px;line-height:22px;color:${C.text2}"><span style="color:${C.green};font-weight:600">✓</span> ${esc(t.change ?? '')}<div style="font-size:13px;line-height:18px;color:${C.text3}">${esc([t.priority, who(t), t.doneAt ? time(t.doneAt) : ''].filter(Boolean).join(' · '))}</div></td></tr>`).join('')).join('');

const html = `<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light only"><title>Fix List ${esc(nice)}</title></head>
<body style="margin:0;padding:0;background:#F4F4F5">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#F4F4F5"><tr><td align="center" style="padding:24px 12px">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:600px;background:#FFFFFF;border:1px solid ${C.line};border-radius:12px;font-family:${C.font}">
<tr><td style="padding:24px 24px 8px">
<div style="font-size:13px;line-height:16px;font-weight:600;color:${C.goldInk};letter-spacing:.04em;text-transform:uppercase">HiddenGem · Meta Ads Fix List</div>
<h1 style="margin:6px 0 4px;font-size:24px;line-height:30px;color:${C.ink};font-weight:600">Done, ${esc(nice)}</h1>
<div style="font-size:14px;line-height:20px;color:${C.text3}">${esc(status)}</div>
</td></tr>
<tr><td style="padding:8px 24px 8px"><table role="presentation" width="100%" cellpadding="0" cellspacing="0">
${rows || `<tr><td style="padding:12px 0;font-size:15px;line-height:22px;color:${C.text3}">Nothing was ticked off since ${esc(since)}.</td></tr>`}
</table></td></tr>
<tr><td style="padding:16px 24px 24px"><a href="${FIXLIST}" style="display:block;background:${C.gold};color:${C.ink};text-decoration:none;font-weight:600;font-size:16px;line-height:48px;text-align:center;border-radius:8px">Open the Fix List</a></td></tr>
</table></td></tr></table></body></html>`;
const text = [`Meta Ads Fix List, done (${nice})`, status, '',
  ...[...byAcct.entries()].flatMap(([acct, ts]) => [acct.toUpperCase(), ...ts.map((t) => `- ${t.change} (${[t.priority, who(t)].filter(Boolean).join(', ')})`), '']),
  done.length ? '' : `Nothing was ticked off since ${since}.`, `Fix List: ${FIXLIST}`].join('\n');

const out = path.join(ROOT, 'weekly', 'Post-Review', 'inputs', `${DATE}-fixlist-digest.html`);
fs.mkdirSync(path.dirname(out), { recursive: true });
fs.writeFileSync(out, html);
console.log(`${status}. Wrote ${path.relative(ROOT, out)}`);
if (DRY) { console.log('dry run: not sent'); process.exit(0); }
sendMail({ to: [OWNER], subject: `Fix List: ${done.length} task${done.length === 1 ? '' : 's'} done (${nice})`, html, text, category: 'fixlist-digest' })
  .then(({ ids, sender }) => console.log(`sent to ${OWNER} from ${sender.from}; message ${ids.join(', ')}`))
  .catch((e) => { console.error(`NOT SENT: ${e.message}`); console.log('\n' + text); process.exit(1); });
