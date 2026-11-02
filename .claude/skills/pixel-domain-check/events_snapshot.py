"""Ad-hoc pixel events snapshot: what every client pixel fired in the last 7 and
28 days, with the Purchase check (added 2026-10-30).

    python3 .claude/skills/pixel-domain-check/events_snapshot.py YYYY-MM-DD [--notes file.md]

Inputs (all next to this file unless stated):
  pixel_pull.json       scripts/pull-pixel-stats.mts output (7-day hosts/events, 28-day events, Purchase by source)
  pms_direct_28d.json   HG AI platform direct/online bookings per client, last 28 days (pms_direct_28d.sql)
  capi_status.json      HG AI platform CAPI toggle + ledger counts per client
  sheet_status.json     Master sheet Status + Attribution Tracking Setup per client
  newest weekly/Meta Pixel Reviews/Weekly Checks/*-pixel-domain-check.csv   client <-> pixel roster + domain flag
  newest weekly/Ad Spends Checks/Weekly Checks/*-ad-spend-check.csv        BoF / MoF Sales budgets

Writes weekly/Meta Pixel Reviews/Event Snapshots/<date>-pixel-events.md and .csv.

Purchase rules (per client, judged on the pixel with the most Purchases; see SKILL.md "Purchase check"):
  n/a   client Not Live on the sheet or $0/day live
  ❌    Live with a Sales budget and zero Purchase in 28d, or capture under 25% of PMS online bookings (PMS >= 5)
  ⚠️    Purchase 28d under 5 with a Sales budget; capture under 50%; Purchase stopped (0 in 7d after >= 3 in the prior 21);
        Purchase over-count (more than 1.5x PMS online bookings, PMS >= 5); zero Purchase without a Sales budget
  ✅    otherwise
"""
import json, csv, os, glob, sys, collections, datetime

SP = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(SP, "..", "..", ".."))
WEEKLY = os.path.join(ROOT, "weekly")
OUT = os.path.join(WEEKLY, "Meta Pixel Reviews", "Event Snapshots")
args = [a for a in sys.argv[1:] if not a.startswith("--")]
TODAY = args[0] if args else datetime.date.today().isoformat()
NOTES = None
if "--notes" in sys.argv:
    NOTES = open(sys.argv[sys.argv.index("--notes") + 1], encoding="utf-8").read().strip()


pull = json.load(open(os.path.join(SP, "pixel_pull.json"), encoding="utf-8"))
px = {p["id"]: p for p in pull["pixels"]}
pms = {r["name"]: r for r in json.load(open(os.path.join(SP, "pms_direct_28d.json"), encoding="utf-8"))["rows"]}
capi = {r["name"]: r for r in json.load(open(os.path.join(SP, "capi_status.json"), encoding="utf-8"))["rows"]}
sheet = {r[0]: {"attribution": r[1], "status": r[2]} for r in json.load(open(os.path.join(SP, "sheet_status.json"), encoding="utf-8"))["rows"]}

def newest(folder, suffix):
    fs = sorted(f for f in glob.glob(os.path.join(WEEKLY, folder, "Weekly Checks", "*" + suffix)) if os.path.basename(f)[:10] <= TODAY)
    return fs[-1] if fs else None
roster_file = newest("Meta Pixel Reviews", "-pixel-domain-check.csv")
spend_file = newest("Ad Spends Checks", "-ad-spend-check.csv")
roster = list(csv.DictReader(open(roster_file, encoding="utf-8"))) if roster_file else []
spend = {r["client"]: r for r in csv.DictReader(open(spend_file, encoding="utf-8"))} if spend_file else {}

# roster rows + any mapped pixel the roster does not know yet
rows = []
seen = set()
for r in roster:
    rows.append(dict(client=r["client"], pid=r["pixel_id"], name=r["pixel_name"], acct=r["ad_account_id"], domain_flag=r["flag"]))
    seen.add((r["client"], r["pixel_id"]))
for client, ids in pull["pixel_map"].items():
    if client in pull.get("offboarded", []): continue
    for pid in ids:
        if (client, pid) in seen or pid not in px: continue
        rows.append(dict(client=client, pid=pid, name=px[pid]["name"], acct=",".join(px[pid].get("attached_to", [])), domain_flag="new"))
        seen.add((client, pid))

# a roster row whose client name is not on the sheet (old combined naming such as
# "Starlight Haven (Hot Springs + Weiss Lake)") is dropped when the same pixel also has a sheet-named row
_pids_named = {r["pid"] for r in rows if r["client"] in sheet}
rows = [r for r in rows if r["client"] in sheet or r["pid"] not in _pids_named]

def fnum(x):
    try: return float(x or 0)
    except ValueError: return 0.0

for r in rows:
    p = px.get(r["pid"])
    r["found"] = p is not None and not p.get("skipped")
    r["events_7d"] = p["total_events"] if r["found"] else 0
    r["events_28d"] = p.get("total_events_28d", 0) if r["found"] else 0
    r["server_7d"] = p["server_events"] if r["found"] else 0
    ev28 = p.get("events_28d", {}) if r["found"] else {}
    r["lead_28d"] = ev28.get("Lead", 0)
    r["other_conv_28d"] = ", ".join(f"{k} {v}" for k, v in sorted(ev28.items(), key=lambda kv: -kv[1]) if k not in ("PageView", "Lead", "Purchase", "__missing_event") and v)[:120]
    q = p.get("purchase_28d", {}) if r["found"] else {}
    r["p28"], r["p28_b"], r["p28_s"] = q.get("total", 0), q.get("browser", 0), q.get("server", 0)
    r["p7"] = p.get("purchase_7d", {}).get("total", 0) if r["found"] else 0
    r["p_last"] = (q.get("last") or "")[:10]
    r["p_first"] = (q.get("first") or "")[:10]
    r["hosts"] = [h for h, v in sorted(p["hosts"].items(), key=lambda kv: -kv[1]["count"])] if r["found"] else []
    r["last_fired"] = (p.get("last_fired_time") or "")[:10] if p else ""
    sp = spend.get(r["client"])
    r["sales_budget"] = fnum(sp["bof_sales"]) + fnum(sp["mof_sales_lol"]) if sp else 0.0
    r["total_live"] = fnum(sp["total_live"]) if sp else 0.0
    st = sheet.get(r["client"], {})
    r["status"] = (st.get("status") or "").strip() or "not on sheet"
    r["attribution"] = st.get("attribution") or ""
    pm = pms.get(r["client"])
    r["pms_online28"] = pm["online28_bk"] if pm else None
    r["pms_direct28"] = pm["direct28_bk"] if pm else None
    r["pms_online7"] = pm["online7_bk"] if pm else None
    c = capi.get(r["client"])
    r["hgai_capi"] = ("on" if c["capi_enabled"] else "OFF") + f", {c['capi_sent_28d']} sent 28d" if c else "no tenant"

# Purchase judgement per client on the pixel with the most Purchases (ties: more events); rules in purchase_rules.py
sys.path.insert(0, SP)
from purchase_rules import judge, MIN_PURCHASE_28D, CAPTURE_CRIT, CAPTURE_WARN, OVERCOUNT, MIN_PMS as MIN_PMS_FOR_CAPTURE
by_client = collections.defaultdict(list)
for r in rows: by_client[r["client"]].append(r)
for client, rs in by_client.items():
    rs.sort(key=lambda r: (-r["p28"], -r["events_28d"]))
    prim = rs[0]
    for r in rs[1:]:
        r["pflag"], r["pnote"] = "see", f"judged on {prim['name']} ({prim['pid']})"
        if r["p28"] and prim["p28"]: r["pnote"] += f"; this pixel also carries {r['p28']} Purchase, check for double counting"
    prim["live"] = prim["status"].lower().startswith("live") and prim["total_live"] > 0
    prim["pflag"], notes = judge(prim)
    prim["pnote"] = "; ".join(notes)

rows.sort(key=lambda r: (r["client"], r["pid"]))
PI = {"ok": "✅", "warning": "⚠️", "critical": "❌", "n/a": "n/a", "see": "↳"}
DI = {"match": "✅", "warning": "⚠️", "critical": "❌", "blocker": "🔴", "new": "new"}
prims = [r for r in rows if r["pflag"] in ("ok", "warning", "critical", "n/a")]
pc = collections.Counter(r["pflag"] for r in prims)
distinct = {r["pid"] for r in rows if r["found"]}
tot7 = sum(px[p]["total_events"] for p in distinct)
tot28 = sum(px[p].get("total_events_28d", 0) for p in distinct)
totP = sum(px[p].get("purchase_28d", {}).get("total", 0) for p in distinct)
w28 = pull.get("window_28d", {})
def d(s): return s[:10] if s else "?"

def pcell(r): return f"{r['p28']:,} ({r['p28_b']}b / {r['p28_s']}s)" if r["p28"] else "0"
def cap(r):
    if r["pms_online28"] is None: return "no PMS"
    if r["pms_online28"] == 0: return f"0 bookings"
    return f"{r['p28']}/{r['pms_online28']} = {r['p28']/r['pms_online28']:.0%}"

L = []
L.append(f"# Meta Pixel Events Snapshot, {TODAY}\n")
L.append(f"**Date:** {TODAY} · **Pixel rows:** {len(rows)} ({len(distinct)} distinct pixels read) · **Clients judged on Purchase:** {len(prims)} · **Purchase check:** {pc['ok']} ✅ · {pc['warning']} ⚠️ · {pc['critical']} ❌ · {pc['n/a']} n/a · **Events, last 7 days:** {tot7:,} · **Events, last 28 days:** {tot28:,} · **Purchase events, last 28 days:** {totP:,}\n")
L.append(f"Ad-hoc run (not the Monday domain check). Meta Marketing API through the HiddenGem-Claude system user (`scripts/pull-pixel-stats.mts`, pulled {d(pull['pulled_at'])} {pull['pulled_at'][11:16]} UTC): 7-day hosts and event totals, plus the 28-day reads added today ({d(w28.get('start'))} to {d(w28.get('end'))}): all-event totals and Purchase split browser/server per hour. PMS bookings from the HiddenGem AI platform (`pms_direct_28d.sql`, same 28 days; 'online' excludes manual, owner, phone and walk-in entries, which never fire a pixel). HG AI CAPI column = the platform's own Conversions API toggle and how many Purchase events its ledger sent in 28 days; server Purchases above that number come from another sender (GHL, PMS-native CAPI, booking engine). Domain flag = the {os.path.basename(roster_file)[:10] if roster_file else 'n/a'} domain check. Sales $/day = BoF Sales + MoF Sales LoL from the {os.path.basename(spend_file)[:10] if spend_file else 'n/a'} spend check.\n")
if NOTES:
    L.append(NOTES + "\n")

PH = "| Client | Pixel | Purchase 28d (browser / server) | Purchase 7d | Last Purchase | PMS online bookings 28d | Capture | Sales $/day | HG AI CAPI | Flag | Why |\n|---|---|---|---|---|---|---|---|---|---|---|"
def prow(r): return f"| {r['client']} | {r['name']} ({r['pid']}) | {pcell(r)} | {r['p7']} | {r['p_last'] or '—'} | {r['pms_online28'] if r['pms_online28'] is not None else '—'} | {cap(r)} | ${r['sales_budget']:.0f} | {r['hgai_capi']} | {PI[r['pflag']]} | {r['pnote']} |"
L.append("## Purchase check: critical (❌)\n")
crit = [r for r in prims if r["pflag"] == "critical"]
if crit:
    L.append(PH); L += [prow(r) for r in crit]; L.append("")
else: L.append("None.\n")
L.append("## Purchase check: warnings (⚠️)\n")
warn = [r for r in prims if r["pflag"] == "warning"]
if warn:
    L.append(PH); L += [prow(r) for r in warn]; L.append("")
else: L.append("None.\n")
L.append("## Purchase check: all clients\n")
L.append(PH); L += [prow(r) for r in prims]; L.append("")

L.append("## Events fired, all pixels (alphabetical by client)\n")
L.append("| Client | Pixel Name | Pixel ID | Events 7d | Events 28d | Server share 7d | Lead 28d | Purchase 28d (b / s) | Other conversions 28d | Last fired | Hosts (7d) | Domain flag | Purchase flag |")
L.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for r in rows:
    share = f"{r['server_7d']/r['events_7d']:.0%}" if r["events_7d"] else "—"
    L.append(f"| {r['client']} | {r['name']} | {r['pid']} | {r['events_7d']:,} | {r['events_28d']:,} | {share} | {r['lead_28d']:,} | {pcell(r)} | {r['other_conv_28d'] or '—'} | {r['last_fired'] or 'never'} | {', '.join(r['hosts']) if r['hosts'] else 'none'} | {DI.get(r['domain_flag'], r['domain_flag'])} | {PI[r['pflag']]}{(' ' + r['pnote']) if r['pflag']=='see' else ''} |")
L.append("")
notsheet = [p for p in pull["pixels"] if not p.get("skipped") and p["id"] not in {r["pid"] for r in rows} and p["id"] != "861460105842405"]
silent = [r for r in rows if r["found"] and r["events_7d"] == 0]
L.append("## Footer\n")
L.append(f"- Pixel rows: {len(rows)} from the {os.path.basename(roster_file) if roster_file else 'n/a'} roster plus pixel-map additions; {len(distinct)} distinct pixels read, {len(silent)} silent in 7d ({', '.join(r['name'] for r in silent) or 'none'}), {len([r for r in rows if not r['found']])} not readable.")
L.append(f"- Totals count each shared pixel once: {tot7:,} events in 7 days, {tot28:,} in 28 days, {totP:,} Purchase in 28 days ({sum(px[p].get('purchase_28d',{}).get('browser',0) for p in distinct):,} browser, {sum(px[p].get('purchase_28d',{}).get('server',0) for p in distinct):,} server).")
L.append(f"- Purchase thresholds (purchase_rules.py): ❌ with a Sales budget: zero Purchase while the PMS has online bookings, capture under {CAPTURE_CRIT:.0%}, or under {MIN_PURCHASE_28D} Purchase with capture under {CAPTURE_WARN:.0%}; ⚠️ zero Purchase otherwise, under {MIN_PURCHASE_28D} Purchase with a Sales budget, capture under {CAPTURE_WARN:.0%}, over-count (the larger of browser or server Purchase above {OVERCOUNT}x the PMS direct bookings, since Meta deduplicates browser+server pairs), or stopped for 7 days. Capture is judged only when the PMS shows at least {MIN_PMS_FOR_CAPTURE} online bookings. Clients with no PMS in the platform (Asheville, Starlight Haven, Columbia Gorge, Nature Nooks, Oak & Ember, Tuxedo Falls, Walden, Bison Ridge, American River, Gooseberry) are judged on counts only.")
L.append("- Pixels with events in the HG BM that belong to no sheet client: " + (", ".join(sorted(f"{p['name']} ({p['total_events']:,} / 7d, {p.get('purchase_28d',{}).get('total',0)} Purchase 28d)" for p in notsheet if p["total_events"] > 0)) or "none") + ".")
norow = sorted(c for c in sheet if c not in by_client and c not in pull.get("offboarded", []))
L.append("- Sheet clients with no pixel row (no ad account or pixel mapped in PROJECT.md): " + (", ".join(norow) or "none") + ".")
L.append(f"- Account listing errors: {len(pull.get('account_errors', {}))}; pixel read errors: {len([p for p in pull['pixels'] if p.get('error')])}.")
os.makedirs(OUT, exist_ok=True)
open(os.path.join(OUT, f"{TODAY}-pixel-events.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
with open(os.path.join(OUT, f"{TODAY}-pixel-events.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow("run_date,client,pixel_id,pixel_name,ad_account_id,status,attribution,events_7d,events_28d,server_events_7d,lead_28d,purchase_28d,purchase_28d_browser,purchase_28d_server,purchase_7d,purchase_first,purchase_last,pms_online_bookings_28d,pms_direct_bookings_28d,sales_budget_per_day,hgai_capi,domain_flag,purchase_flag,purchase_note,hosts_7d".split(","))
    for r in rows:
        w.writerow([TODAY, r["client"], r["pid"], r["name"], r["acct"], r["status"], r["attribution"], r["events_7d"], r["events_28d"], r["server_7d"], r["lead_28d"], r["p28"], r["p28_b"], r["p28_s"], r["p7"], r["p_first"], r["p_last"], r["pms_online28"] if r["pms_online28"] is not None else "", r["pms_direct28"] if r["pms_direct28"] is not None else "", f"{r['sales_budget']:.0f}", r["hgai_capi"], r["domain_flag"], r["pflag"], r["pnote"], "|".join(r["hosts"])])
print(f"rows {len(rows)} distinct {len(distinct)} purchase flags {dict(pc)} tot7 {tot7:,} tot28 {tot28:,} purchases28 {totP}")
for r in prims:
    if r["pflag"] in ("critical", "warning"): print(f"  {PI[r['pflag']]} {r['client']:<30} {pcell(r):<22} pms {r['pms_online28']}  {r['pnote']}")
