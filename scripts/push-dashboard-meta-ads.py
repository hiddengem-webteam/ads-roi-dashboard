#!/usr/bin/env python3
"""Map a monthly Client Reporting export onto Pooja's client-dashboard table
`dashboard_meta_ads` (Supabase project vdonazmwxzucdxduzfhh) and optionally write it.

Mapping (derived from the September 2026 rows Pooja loaded, verified with --verify):
  Discovery row   = Followers bucket + New Leads bucket combined
    spend/impressions/profile_visits(linkClicks)  summed
    leads_followers = newLeads.leads, ig_bio_leads = followers.instagramTagLeads
    bookings_email_matched = followers.totalBookings + newLeads.totalBookings
    revenue = followers.bookingRevenue + newLeads.bookingRevenue
    cost_per_booking = spend / bookings, roas = revenue / spend
    avg_booking_value = followers.campaignAvgBookingValue
    pct_avg_booking_value = cost_per_booking / avg_booking_value   (fraction)
  Retargeting row = Retargeting bucket (only when it ran)
    bookings_fb_events = totalBookings, pct_avg_booking_value = pctOfBookingValue / 100
  blended_roas = client blendedRoas on both rows; comments = client note (Discovery row)

Usage:
  python3 scripts/push-dashboard-meta-ads.py --month 2026-10 --preview      # print rows, write CSV
  python3 scripts/push-dashboard-meta-ads.py --month 2026-09 --verify       # diff export vs DB
  python3 scripts/push-dashboard-meta-ads.py --month 2026-10 --write        # insert (refuses if month exists)
  python3 scripts/push-dashboard-meta-ads.py --month 2026-09 --write --replace   # delete month rows, re-insert
Reads POOJA_SUPABASE_URL / POOJA_SUPABASE_SECRET_KEY from .env.local.
"""
import argparse, csv, json, os, re, sys, urllib.request, urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXPORTS = {
    '2026-07': 'weekly/Monthly ROI data/July 2026 - Client Reporting.json',
    '2026-08': 'weekly/Monthly ROI data/August 2026 - Client Reporting.json',
    '2026-09': 'weekly/Monthly ROI data/September 2026 - Client Reporting.json',
    '2026-10': 'weekly/Monthly ROI data/October 2026 - Client Reporting.json',
}
# Export clientName -> Pooja's client_slug where simple slugify does not match.
SLUG_OVERRIDES = {
    'American River Resort': 'american-river',
    'Flohom': 'flohom',
    'North Star Lodge & Resort': 'north-star-lodge-resort',
    'Oak & Ember': 'oak-ember',
    'Ridge & Falls': 'ridge-falls',
    'Stay Southern Illinois': 'southern-illinois-cabins',
    'Tàberg Falls': 't-berg-falls',
    'Stay on 30a': 'stay-on-30a',
}

def slugify(name):
    if name in SLUG_OVERRIDES: return SLUG_OVERRIDES[name]
    s = name.lower().replace('&', ' ')
    s = re.sub(r'[^a-z0-9]+', '-', s).strip('-')
    return s

def load_env():
    env = {}
    p = os.path.join(ROOT, '.env.local')
    for line in open(p):
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            k, v = line.split('=', 1); env[k.strip()] = v.strip().strip('"').strip("'")
    url, key = env.get('POOJA_SUPABASE_URL'), env.get('POOJA_SUPABASE_SECRET_KEY')
    if not url or not key: sys.exit('POOJA_SUPABASE_URL / POOJA_SUPABASE_SECRET_KEY missing in .env.local')
    return url.rstrip('/'), key

def api(method, path, body=None, prefer=None):
    url, key = load_env()
    req = urllib.request.Request(f'{url}/rest/v1/{path}', method=method,
        data=json.dumps(body).encode() if body is not None else None)
    req.add_header('apikey', key); req.add_header('Authorization', f'Bearer {key}')
    req.add_header('Content-Type', 'application/json')
    if prefer: req.add_header('Prefer', prefer)
    with urllib.request.urlopen(req) as r:
        txt = r.read().decode()
        return json.loads(txt) if txt else None

def r2(x, nd=2):
    return None if x is None else round(float(x), nd)

def build_rows(month):
    year, mon = (int(x) for x in month.split('-'))
    exp = json.load(open(os.path.join(ROOT, EXPORTS[month])))
    rows = []
    for c in exp['clients']:
        slug = slugify(c['clientName']); camp = c['campaigns']
        f, n, rt = camp.get('followers'), camp.get('newLeads'), camp.get('retargeting')
        blended = r2(c.get('blendedRoas'))
        if f or n:
            f = f or {}; n = n or {}
            spend = r2((f.get('spend') or 0) + (n.get('spend') or 0))
            bookings = int((f.get('totalBookings') or 0) + (n.get('totalBookings') or 0))
            revenue = r2((f.get('bookingRevenue') or 0) + (n.get('bookingRevenue') or 0))
            cpb = r2(spend / bookings) if bookings else None
            abv = r2(f.get('campaignAvgBookingValue')) if f.get('campaignAvgBookingValue') else (r2(revenue / bookings) if bookings else None)
            rows.append(dict(client_slug=slug, year=year, month=mon, campaign_type='Discovery',
                spend=spend, impressions=int((f.get('impressions') or 0) + (n.get('impressions') or 0)),
                profile_visits=int((f.get('linkClicks') or 0) + (n.get('linkClicks') or 0)), cost_per_visit=None,
                leads_followers=int(n.get('leads') or 0) if n else None, cost_per_lead_follower=None,
                ig_bio_leads=int(f.get('instagramTagLeads') or 0), bookings_email_matched=bookings, bookings_fb_events=None,
                cost_per_booking=cpb, avg_booking_value=abv,
                pct_avg_booking_value=r2(cpb / abv, 4) if (cpb and abv) else None,
                revenue=revenue, roas=r2(revenue / spend) if (spend and revenue) else None,
                blended_roas=blended, comments=c.get('note')))
        if rt:
            rows.append(dict(client_slug=slug, year=year, month=mon, campaign_type='Retargeting',
                spend=r2(rt['spend']), impressions=int(rt.get('impressions') or 0), profile_visits=int(rt.get('linkClicks') or 0),
                cost_per_visit=None, leads_followers=None, cost_per_lead_follower=None, ig_bio_leads=None,
                bookings_email_matched=None, bookings_fb_events=int(rt.get('totalBookings') or 0),
                cost_per_booking=r2(rt.get('costPerBooking')), avg_booking_value=r2(rt.get('campaignAvgBookingValue')),
                pct_avg_booking_value=r2(rt['pctOfBookingValue'] / 100, 4) if rt.get('pctOfBookingValue') is not None else None,
                revenue=r2(rt.get('bookingRevenue') or 0), roas=r2(rt.get('roas')), blended_roas=blended, comments=None))
    return rows

COMPARE = ['spend','impressions','profile_visits','leads_followers','ig_bio_leads','bookings_email_matched',
           'bookings_fb_events','cost_per_booking','avg_booking_value','pct_avg_booking_value','revenue','roas','blended_roas','comments']

def fetch_month(month):
    year, mon = month.split('-')
    return api('GET', f'dashboard_meta_ads?select=*&year=eq.{int(year)}&month=eq.{int(mon)}&limit=1000')

def close(a, b, col):
    if a is None and b is None: return True
    if a is None or b is None: return (a or 0) == (b or 0) if col in ('revenue','ig_bio_leads','leads_followers','bookings_email_matched') else False
    if isinstance(a, str) or isinstance(b, str): return (a or '').strip() == (b or '').strip()
    tol = 0.02 if col in ('pct_avg_booking_value',) else 0.011 * max(1, abs(float(a)) if col in ('spend','revenue') else 1)
    return abs(float(a) - float(b)) <= max(tol, 0.0105)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--month', required=True)
    ap.add_argument('--preview', action='store_true'); ap.add_argument('--verify', action='store_true')
    ap.add_argument('--write', action='store_true'); ap.add_argument('--replace', action='store_true')
    a = ap.parse_args()
    rows = build_rows(a.month)
    out = os.path.join(ROOT, 'scratchpad', 'pooja'); os.makedirs(out, exist_ok=True)
    csvp = os.path.join(out, f'dashboard_meta_ads-{a.month}.csv')
    with open(csvp, 'w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    if a.preview:
        print(f'{len(rows)} rows for {a.month} ({len(set(r["client_slug"] for r in rows))} clients) -> {csvp}')
        print(f'{"client_slug":30s} {"type":11s} {"spend":>9s} {"impr":>8s} {"visits":>6s} {"leads":>6s} {"bkgs":>4s} {"revenue":>10s} {"roas":>6s} {"blend":>6s}  comment')
        for r in rows:
            b = r['bookings_email_matched'] if r['campaign_type']=='Discovery' else r['bookings_fb_events']
            print(f'{r["client_slug"]:30s} {r["campaign_type"]:11s} {r["spend"]:>9.2f} {r["impressions"]:>8d} {r["profile_visits"]:>6d} {str(r["leads_followers"] or ""):>6s} {b:>4d} {r["revenue"]:>10.2f} {str(r["roas"] or ""):>6s} {str(r["blended_roas"] or ""):>6s}  {(r["comments"] or "")[:60]}')
    if a.verify:
        db = {(r['client_slug'], r['campaign_type']): r for r in fetch_month(a.month)}
        ours = {(r['client_slug'], r['campaign_type']): r for r in rows}
        same = 0
        for k in sorted(set(db) | set(ours)):
            if k not in db: print('ONLY IN EXPORT', k); continue
            if k not in ours: print('ONLY IN DB    ', k, 'spend', db[k]['spend']); continue
            diffs = [(c, db[k][c], ours[k][c]) for c in COMPARE if not close(db[k][c], ours[k][c], c)]
            if diffs: print('DIFF', k); [print(f'      {c:24s} db={d!r:>12}  export={o!r}') for c, d, o in diffs]
            else: same += 1
        print(f'{same} rows identical; {len(db)} in DB, {len(ours)} in export')
    if a.write:
        existing = fetch_month(a.month)
        if existing and not a.replace:
            sys.exit(f'{len(existing)} rows already exist for {a.month}; use --replace to overwrite')
        if existing:
            year, mon = a.month.split('-')
            api('DELETE', f'dashboard_meta_ads?year=eq.{int(year)}&month=eq.{int(mon)}', prefer='return=minimal')
            print(f'deleted {len(existing)} existing rows for {a.month}')
        res = api('POST', 'dashboard_meta_ads', body=rows, prefer='return=representation')
        print(f'inserted {len(res)} rows for {a.month} (ids {min(r["id"] for r in res)}-{max(r["id"] for r in res)})')

if __name__ == '__main__':
    main()
