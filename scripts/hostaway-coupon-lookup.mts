/**
 * Resolve Hostaway coupon codes for a list of guest emails (or Hostaway reservation
 * IDs). Prints only reservation id, guest email, total and coupon code; credentials
 * never leave the process.
 *
 *   npx tsx scripts/hostaway-coupon-lookup.mts <email-or-reservationId,...> [arrivalStart] [arrivalEnd]
 *
 * Needs HOSTAWAY_FLOHOM_ACCOUNT_ID and HOSTAWAY_FLOHOM_CLIENT_SECRET in .env.local
 * (the same account_id / client_secret the HiddenGem AI platform stores for the tenant).
 */
import fs from 'fs'; import path from 'path'; import { fileURLToPath } from 'url';
const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
for (const file of ['.env.local', '.env']) { const p = path.join(ROOT, file); if (!fs.existsSync(p)) continue;
  for (const raw of fs.readFileSync(p, 'utf8').split('\n')) { const l = raw.trim(); if (!l || l.startsWith('#')) continue; const i = l.indexOf('='); if (i < 0) continue; const k = l.slice(0, i).trim(); if (!(k in process.env)) process.env[k] = l.slice(i + 1).trim().replace(/^"(.*)"$/, '$1'); } }
const ACCOUNT = process.env.HOSTAWAY_FLOHOM_ACCOUNT_ID, SECRET = process.env.HOSTAWAY_FLOHOM_CLIENT_SECRET;
if (!ACCOUNT || !SECRET) { console.error('Set HOSTAWAY_FLOHOM_ACCOUNT_ID and HOSTAWAY_FLOHOM_CLIENT_SECRET in .env.local'); process.exit(2); }
const API = 'https://api.hostaway.com/v1';
const wanted = (process.argv[2] ?? '').split(',').map((s) => s.trim().toLowerCase()).filter(Boolean);
if (!wanted.length) { console.error('Pass guest emails or reservation ids as a comma-separated list'); process.exit(2); }
const arrivalStart = process.argv[3] ?? '2026-07-01', arrivalEnd = process.argv[4] ?? '2027-12-31';
(async () => {
  const tok: any = await (await fetch(`${API}/accessTokens`, { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded', 'Cache-control': 'no-cache' }, body: new URLSearchParams({ grant_type: 'client_credentials', client_id: ACCOUNT, client_secret: SECRET, scope: 'general' }) })).json();
  if (!tok.access_token) { console.error('token request failed:', tok.error ?? tok.message ?? 'unknown'); process.exit(1); }
  const h = { Authorization: `Bearer ${tok.access_token}`, 'Cache-control': 'no-cache' };
  // Coupon definitions, for id -> code mapping if the reservation only carries an id.
  const coupons: any = await (await fetch(`${API}/coupons?limit=500`, { headers: h })).json();
  const byId = new Map<string, any>(); for (const c of coupons.result ?? []) byId.set(String(c.id), c);
  console.log(`coupon definitions on account: ${byId.size}`);
  for (const c of byId.values()) console.log(`  def ${c.id}  code=${c.name ?? c.code ?? '?'}  ${c.type ?? ''} ${c.value ?? ''}`);
  // Resolve emails to reservation ids by paging the reservation list for the arrival window.
  const ids: string[] = wanted.filter((w) => /^\d+$/.test(w));
  const emails = wanted.filter((w) => !/^\d+$/.test(w));
  if (emails.length) {
    for (let offset = 0; ; offset += 100) {
      const page: any = await (await fetch(`${API}/reservations?limit=100&offset=${offset}&arrivalStartDate=${arrivalStart}&arrivalEndDate=${arrivalEnd}`, { headers: h })).json();
      const list: any[] = page.result ?? []; if (!list.length) break;
      for (const r of list) if (emails.includes(String(r.guestEmail ?? '').toLowerCase())) ids.push(String(r.id));
      if (list.length < 100) break;
    }
    console.log(`resolved ${ids.length} reservations for ${emails.length} emails`);
  }
  for (const id of ids) {
    const r: any = await (await fetch(`${API}/reservations/${id}`, { headers: h })).json();
    const res = r.result ?? {};
    const couponKeys = Object.entries(res).filter(([k, v]) => /coupon/i.test(k) && v !== null && v !== undefined);
    const def = byId.get(String(res.reservationCouponId ?? res.couponId ?? ''));
    console.log(`${id}  ${res.guestEmail ?? '-'}  total=${res.totalPrice}  ${couponKeys.map(([k, v]) => `${k}=${JSON.stringify(v)}`).join(' ')}  ${def ? `-> code ${def.name ?? def.code}` : ''}`);
    if (res.reservationCouponId) {
      const rc: any = await (await fetch(`${API}/reservationCoupons/${res.reservationCouponId}`, { headers: h })).json();
      if (rc.result) console.log(`    reservationCoupon: ${JSON.stringify(rc.result)}`);
    }
  }
})();
