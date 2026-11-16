/**
 * Mailtrap sending for HiddenGem reports (2026-11-16). Follows the HiddenGem email rule:
 * Mailtrap only, never Gmail or another service; domain precedence checked before every send.
 *
 *   1. hiddengem.media (id 1270195) when DNS-verified and compliant -> reports@hiddengem.media, any recipient
 *   2. demomailtrap.co (id 1270193) while it is in demo state -> reports@demomailtrap.co, owner only
 *      (a demo domain rejects the whole send if any other recipient is on it)
 *   3. otherwise fail, and the caller prints the content instead of rerouting
 *
 * Token: MAIL_TRAP_API_KEY (or MAILTRAP_API_TOKEN) in the repo-root .env.
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

export const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
const ACCOUNT_ID = 2819434;
export const OWNER = 'shawal@hiddengem.media';

export function loadEnv() {
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
}
function token(): string {
  loadEnv();
  const t = process.env.MAIL_TRAP_API_KEY || process.env.MAILTRAP_API_TOKEN;
  if (!t) throw new Error('MAIL_TRAP_API_KEY is not set in .env');
  return t;
}

export interface Sender { from: string; domain: string; ownerOnly: boolean; note: string }

/** Domain precedence check. Throws with the domain states when neither domain can send. */
export async function pickSender(): Promise<Sender> {
  const res = await fetch(`https://mailtrap.io/api/accounts/${ACCOUNT_ID}/sending_domains`, { headers: { Authorization: `Bearer ${token()}` } });
  if (!res.ok) throw new Error(`Mailtrap sending_domains HTTP ${res.status}: ${(await res.text()).slice(0, 300)}`);
  const body: any = await res.json();
  const list: any[] = Array.isArray(body) ? body : (body.data ?? []);
  const hg = list.find((d) => d.domain_name === 'hiddengem.media');
  const demo = list.find((d) => d.domain_name === 'demomailtrap.co');
  if (hg?.dns_verified && hg?.compliance_status === 'compliant') return { from: 'reports@hiddengem.media', domain: 'hiddengem.media', ownerOnly: false, note: 'hiddengem.media is verified: any recipient allowed' };
  if (demo && demo.compliance_status === 'demo') return { from: 'reports@demomailtrap.co', domain: 'demomailtrap.co', ownerOnly: true, note: `hiddengem.media is ${hg?.compliance_status ?? 'missing'}; sent from the demo domain, owner only` };
  throw new Error(`No sending domain available: hiddengem.media ${hg?.compliance_status ?? 'missing'}, demomailtrap.co ${demo?.compliance_status ?? 'missing'}`);
}

export interface Mail { to: string[]; subject: string; html: string; text: string; category: string; attachments?: { filename: string; content: string; type: string }[] }

export async function sendMail(m: Mail): Promise<{ ids: string[]; sender: Sender }> {
  const sender = await pickSender();
  const to = m.to.map((s) => s.trim().toLowerCase());
  if (sender.ownerOnly && to.some((t) => t !== OWNER)) throw new Error(`The demo domain can only send to ${OWNER}; refusing to send to ${to.join(', ')}`);
  const res = await fetch('https://send.api.mailtrap.io/api/send', {
    method: 'POST',
    headers: { Authorization: `Bearer ${token()}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      from: { email: sender.from, name: 'HG Meta Ads Reports' },
      to: to.map((email) => ({ email })),
      subject: m.subject, html: m.html, text: m.text, category: m.category,
      ...(m.attachments?.length ? { attachments: m.attachments.map((a) => ({ ...a, disposition: 'attachment' })) } : {}),
    }),
  });
  const out: any = await res.json().catch(() => ({}));
  if (!res.ok || !out.success) throw new Error(`Mailtrap send HTTP ${res.status}: ${JSON.stringify(out).slice(0, 400)}`);
  return { ids: out.message_ids ?? [], sender };
}

/** Shared email styling (light only: email clients ignore prefers-color-scheme inconsistently). Gold = HG design system gem yellow. */
export const EMAIL = {
  ink: '#0A0A0A', text2: '#3F3F46', text3: '#71717A', line: '#E4E4E7', panel: '#FAFAFA', gold: '#FFD60A', goldInk: '#8A7100',
  red: '#B42318', redBg: '#FEF3F2', amber: '#8A5A00', amberBg: '#FFFAEB', green: '#067647', greenBg: '#ECFDF3', grayBg: '#F4F4F5',
  font: "-apple-system,BlinkMacSystemFont,'Segoe UI',Inter,Roboto,Helvetica,Arial,sans-serif",
};
export const escHtml = (s: string) => String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
