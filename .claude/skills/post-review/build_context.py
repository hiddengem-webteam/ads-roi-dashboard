"""Post-review context pack (2026-11-16, Shawal).

Joins everything the Monday post-review needs per client into one Markdown brief, so the
recommendations are written from one file instead of eight:

  python3 .claude/skills/post-review/build_context.py YYYY-MM-DD

Inputs (all for the same run date unless noted):
  weekly/Client Benchmark Reviews (advanced setups)/Weekly Checks/DATE-client-benchmark.{csv,md}
  weekly/Ad Spends Checks/Weekly Checks/DATE-ad-spend-check.csv
  weekly/Meta Pixel Reviews/Weekly Checks/DATE-pixel-domain-check.csv
  .claude/skills/post-review/ads.json        scripts/pull-ad-insights.mts DATE
  .claude/skills/post-review/crm.json        CRM 'Clients - Onboarding', written by the skill each run
  .claude/skills/client-benchmark/generate_report.py   ADV / ADV_UNMAPPED maps (client -> ad account)
  weekly/Post-Review/inputs/fixlist/{tasks,accounts}/*.json   Meta Ads Fix List dump (ArtifactData out_dir)
  video/specs/<slug>.json, <slug>-b.json     reels already scripted for the client (22 Oct batch)
Output: weekly/Post-Review/inputs/DATE-context.md (gitignored, rebuilt every run).
"""
import csv, json, glob, os, re, sys, datetime, collections

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
W = os.path.join(REPO, "weekly")
DATE = sys.argv[1] if len(sys.argv) > 1 else datetime.date.today().isoformat()
RUN = datetime.date.fromisoformat(DATE)
NEW_CLIENT_DAYS = 90       # "new client" = kickoff in the last 90 days (first 2-3 months get priority, Nov 2026 ownership reset)
LIVE_GRACE_DAYS = 7        # flag when campaigns are not live by CRM Funnel Build Due + 7 days (Shawal, 2026-11-16)
DAYS_PER_MONTH = 30.4      # CRM Ad Spend Range is a monthly budget

def norm(s): return re.sub(r"[^a-z0-9]", "", (s or "").lower().replace("à", "a").replace("á", "a"))
def f(x):
    try: return float(str(x).replace("$", "").replace(",", ""))
    except (TypeError, ValueError): return None
def money(v, d=0): return "—" if v is None else f"${v:,.{d}f}"
def pdate(s):
    s = re.sub(r"(\d)(st|nd|rd|th)", r"\1", (s or "").strip()).replace("Sept ", "Sep ")
    for fmt in ("%b %d, %Y", "%B %d, %Y", "%Y-%m-%d"):
        try: return datetime.datetime.strptime(s, fmt).date()
        except ValueError: pass
    return None
def short(s, n=170):
    s = re.sub(r"\s+", " ", s or "").strip()
    return s if len(s) <= n else s[:n - 1].rstrip() + "…"

# ---------- load
bench_dir = f"{W}/Client Benchmark Reviews (advanced setups)/Weekly Checks"
bench = list(csv.DictReader(open(f"{bench_dir}/{DATE}-client-benchmark.csv", encoding="utf-8")))
bench_md = open(f"{bench_dir}/{DATE}-client-benchmark.md", encoding="utf-8").read()
spend = {norm(r["client"]): r for r in csv.DictReader(open(f"{W}/Ad Spends Checks/Weekly Checks/{DATE}-ad-spend-check.csv", encoding="utf-8"))}
pixel = collections.defaultdict(list)
for r in csv.DictReader(open(f"{W}/Meta Pixel Reviews/Weekly Checks/{DATE}-pixel-domain-check.csv", encoding="utf-8")):
    pixel[norm(r["client"])].append(r)
ads = json.load(open(f"{HERE}/ads.json", encoding="utf-8"))
if ads.get("run_date") != DATE: print(f"warning: ads.json is from {ads.get('run_date')}, not {DATE}; rerun scripts/pull-ad-insights.mts {DATE}")
ads_by = {norm(k): v for k, v in ads["accounts"].items()}
crm_raw = json.load(open(f"{HERE}/crm.json", encoding="utf-8"))
crm = [dict(zip(crm_raw["cols"], r)) for r in crm_raw["rows"]]
crm_by = {norm(r["client"]): r for r in crm}
gen = open(f"{REPO}/.claude/skills/client-benchmark/generate_report.py", encoding="utf-8").read()
adv_block = gen[gen.index("ADV={"):gen.index("ADV_UNMAPPED")]
ADV = {norm(m.group(1)): (m.group(1), m.group(2), m.group(3)) for m in re.finditer(r'^\s*"([^"]+)":\("([^"]*)","(\d+)"', adv_block, re.M)}
# HiddenGem team logins, same rule as the benchmark (HG_TEAM / HG_EXACT in generate_report.py)
HG_TEAM = set(re.findall(r'"([^"]+)"', re.search(r"HG_TEAM=\{([^}]*)\}", gen).group(1)))
HG_EXACT = set(re.findall(r'"([^"]+)"', re.search(r"HG_EXACT=\{([^}]*)\}", gen).group(1)))
def is_hg(name):
    n = (name or "").lower().strip()
    return n in HG_EXACT or any(n == h or n.split(" ")[0] == h.split(" ")[0] for h in HG_TEAM)
_cp = f"{REPO}/.claude/skills/client-benchmark/creators.json"
CREATORS = json.load(open(_cp, encoding="utf-8")) if os.path.exists(_cp) else {}
# campaigns Shawal chose to leave as they are (DEFERRED in generate_report.py): never recommend stopping them
_dm = re.search(r"DEFERRED=\{(.*?)\n\}", gen, re.S)
DEFERRED = dict(re.findall(r'"(\d+)":"([^"]*)"', _dm.group(1))) if _dm else {}
def legacy_label(x):
    if x["id"] in DEFERRED: return f"deferred, leave as is: {DEFERRED[x['id']]}"
    who = CREATORS.get(x["id"], {}).get("name")
    return f"client-run, created by {who}" if who else "creator unknown (older than the 180-day activity log)"
fx = f"{W}/Post-Review/inputs/fixlist"
def _doc(p):
    d = json.load(open(p, encoding="utf-8")); d = d.get("data", d) if isinstance(d, dict) else d
    d["_id"] = os.path.splitext(os.path.basename(p))[0]; return d
fl_accounts = [_doc(p) for p in glob.glob(f"{fx}/accounts/*.json")]
fl_tasks = [_doc(p) for p in glob.glob(f"{fx}/tasks/*.json")]
alias = {}
for a in fl_accounts:
    for n in [a.get("name", "")] + list(a.get("aliases") or []): alias[norm(n)] = norm(a.get("name", ""))
def fl_key(name): return alias.get(norm(name), norm(name))
tasks_by = collections.defaultdict(list)
for t in fl_tasks: tasks_by[fl_key(t.get("account", ""))].append(t)
specs = {}
for p in sorted(glob.glob(f"{REPO}/video/specs/*.json")):
    try: s = json.load(open(p, encoding="utf-8"))
    except Exception: continue
    hook = " / ".join(s.get("beats", [{}])[0].get("lines", [])) if s.get("beats") else ""
    specs.setdefault(norm(s.get("client", "")), []).append((os.path.basename(p), hook))

# ---------- benchmark per-client blocks
blocks = {}
cur = None
for line in bench_md.split("\n"):
    if line.startswith("### "):
        cur = norm(line[4:].split(" — ")[0]); blocks[cur] = [line]
    elif line.startswith("## ") and cur: cur = None
    elif cur: blocks[cur].append(line)

# ---------- lists
SALES = ("Retargeting (BoF)", "Prospecting (MoF lookalike)", "Sales")
act_rows = [r for r in bench if r["type"] in SALES and r["state"] in ("Flag to Shawal", "Review w/ HG AI")]
scale_rows = [r for r in bench if r["type"] in SALES and r["state"] == "Scale w/ HG AI"]
freq_rows = [r for r in bench if r.get("freq_flag") == "yes"]
order = {"Flag to Shawal": 0, "Review w/ HG AI": 1}
act_rows.sort(key=lambda r: (order[r["state"]], -f(r["spend"])))
scale_rows.sort(key=lambda r: -f(r["spend"]))
freq_rows.sort(key=lambda r: -f(r["frequency"]))
lists = collections.OrderedDict()
for tag, rows in (("Flagged", act_rows), ("Scale", scale_rows), ("Frequency", freq_rows)):
    for r in rows: lists.setdefault(norm(r["client"]), (r["client"], r["am"], []))[2].append((tag, r))

# ---------- helpers
def crm_line(c):
    r = crm_by.get(c)
    if not r: return "CRM: no row found."
    rng = f(r["spend_range"])
    sp = spend.get(c); live = f(sp["total_live"]) if sp else None
    head = ""
    if rng and live is not None:
        mon = live * DAYS_PER_MONTH
        head = f"; live ${live:,.0f}/day ≈ {money(mon)}/month = {mon / rng * 100:.0f}% of range"
    elif live is not None: head = f"; live ${live:,.0f}/day ≈ {money(live * DAYS_PER_MONTH)}/month, no range set"
    return (f"CRM: {r['setup'] or r['meta_ads'] or '—'} · Ad Spend Range {r['spend_range'] or '—'}/month{head} · ROAS goal {r['roas_goal'] or '—'} · "
            f"PMS {r['pms'] or '—'} ({r['pms_conn'] or '—'}) · pixel {r['pixel_conn'] or '—'} · EMQ {r['emq'] or '—'}")
def structure_line(c):
    r = spend.get(c)
    if not r: return "Ad spend check: no row."
    parts = [("ToF giveaway", "tof_giveaway"), ("MoF leads", "mof_leads"), ("MoF LoL sales", "mof_sales_lol"), ("BoF sales", "bof_sales"), ("other", "other")]
    have = [f"{n} ${f(r[k]):,.0f}" for n, k in parts if (f(r[k]) or 0) > 0]
    missing = [n for n, k in parts[:4] if not (f(r[k]) or 0) > 0]
    s = f"Live budgets/day: {', '.join(have) or 'none'} (total ${f(r['total_live']) or 0:,.0f}; status {r['status']})"
    if missing: s += f". Not running: {', '.join(missing)}"
    if r.get("what_changed"): s += f". Changed: {short(r['what_changed'], 220)}"
    return s
def pixel_line(c):
    rows = pixel.get(c, [])
    if not rows: return "Pixel check: no row."
    out = []
    for r in rows:
        out.append(f"Pixel {r['pixel_id']}: domain flag {r['flag']}, Purchase {r.get('purchase_flag') or '—'} ({short(r.get('purchase_note'), 120)}); HG AI CAPI {r.get('hgai_capi') or '—'}")
    return " | ".join(out)
def ad_rows(c, campaign_ids=None, limit=8):
    a = ads_by.get(c)
    if not a: return ["(no ad pull for this client)"]
    out = []
    pool = [x for x in a["ads"] if (x.get("w14") or x.get("status") == "ACTIVE")]
    if campaign_ids: pool = [x for x in pool if x.get("campaign_id") in campaign_ids] or pool
    for x in pool[:limit]:
        w14, w7 = x.get("w14") or {}, x.get("w7") or {}
        # CTR of the 7 days before the last 7, from the 14-day totals minus the last 7
        pi, pc = (w14.get("impr", 0) - w7.get("impr", 0)), (w14.get("clicks", 0) - w7.get("clicks", 0))
        prev_ctr = pc / pi * 100 if pi > 500 else None
        trend = f"CTR {w7.get('link_ctr', 0):.2f}% last 7d vs {prev_ctr:.2f}% prior 7d" if prev_ctr is not None and w7 else ""
        tired = []
        if (w14.get("freq") or 0) > 4: tired.append(f"freq {w14['freq']:.1f}")
        if prev_ctr and w7.get("link_ctr") is not None and w7.get("impr", 0) > 500 and w7["link_ctr"] < prev_ctr * 0.75: tired.append("CTR down >25%")
        if (x.get("age_days") or 0) > 60: tired.append(f"{x['age_days']} days old")
        hook = f", hook {w14['hook']:.0f}%" if w14.get("hook") else ""
        out.append(f"- {x.get('name')} [{x.get('kind', '?')}, {x.get('status')}, created {x.get('created') or '?'}] in '{short(x.get('campaign'), 60)}': "
                   f"14d {money(w14.get('spend'))}, {w14.get('purch', 0):g} purch, ROAS {w14.get('roas', 0):.1f}x, freq {w14.get('freq', 0):.1f}{hook}; "
                   f"30d {money((x.get('w30') or {}).get('spend'))} ROAS {(x.get('w30') or {}).get('roas', 0):.1f}x. {trend}"
                   + (f" ⚠ {', '.join(tired)}" if tired else "")
                   + (f"\n    copy: \"{short(x.get('headline'), 60)}\" / \"{short(x.get('text'), 110)}\"" if x.get("headline") or x.get("text") else ""))
    if len(pool) > limit: out.append(f"- … {len(pool) - limit} more ads")
    return out
def task_lines(c, include_done=False):
    ts = [t for t in tasks_by.get(fl_key(c), []) if include_done or not t.get("done")]
    ts.sort(key=lambda t: (t.get("done", False), t.get("source", ""), t.get("order", 0)))
    return [f"- [{t['_id']}] {t.get('priority')}{' DONE' if t.get('done') else ''} ({t.get('source')}): {short(t.get('change'), 200)}" for t in ts]

# ---------- write
L = [f"# Post-review context, {DATE}", "",
     f"Lists from the client benchmark: {len(act_rows)} flagged (Action needed), {len(scale_rows)} scale, {len(freq_rows)} frequency watch. "
     f"Ad-level pull: {ads.get('windows')}. Fix List: {sum(1 for t in fl_tasks if not t.get('done'))} open tasks.", ""]
for c, (name, am, items) in lists.items():
    L += [f"## {name} (AM {am})", ""]
    for tag, r in items:
        L.append(f"**{tag}:** {r['campaign']} ({r['type']}) · 14d spend {money(f(r['spend']))} · {r['governing_metric']} {r['governing_value']} · state {r['state']} · freq {r['frequency'] or '—'} · "
                 f"{r['diff_status']}{' (' + r['weeks_open'] + ' weeks)' if r['weeks_open'] not in ('', '0') else ''} · diagnostics: {r['diagnostics'] or '—'}")
    L += ["", crm_line(c), "", structure_line(c), "", pixel_line(c), ""]
    L += ["Benchmark block:", ""] + [l for l in blocks.get(c, ["(no block)"]) if l.strip()] + [""]
    ids = {r["campaign_id"] for _, r in items}
    L += ["Ads in the listed campaigns, highest 14-day spend first:"] + ad_rows(c, ids) + [""]
    sp = specs.get(c) or specs.get(norm(name.replace("NC", "")))
    L.append("Reels already scripted (video/specs): " + ("; ".join(f"{fn}: \"{h}\"" for fn, h in sp) if sp else "none") + ".")
    L += ["", "Open Fix List tasks:"] + (task_lines(c) or ["- none"]) + [""]

# ---------- new clients
L += ["## New clients (CRM kickoff in the last 90 days, or no kickoff date)", "",
      f"Rule: campaigns should be live by Funnel Build Due + {LIVE_GRACE_DAYS} days. Access = the HG - ROI Dashboard system user can read the ad account and its pixel.", ""]
unmapped = re.search(r"ADV_UNMAPPED=\{([^}]*)\}", gen)
unmapped_names = {norm(n) for n in re.findall(r'"([^"]+)":', unmapped.group(1))} if unmapped else set()
n_new = 0
for r in crm:
    k = pdate(r["kickoff"])
    if k and (RUN - k).days > NEW_CLIENT_DAYS: continue
    if (r["setup"] or "").lower() == "no ads": continue
    c = norm(r["client"])
    due = pdate(r["funnel_due"]); deadline = due + datetime.timedelta(days=LIVE_GRACE_DAYS) if due else None
    a = ads_by.get(c)
    mapped = c in ADV
    if k and k > RUN: verdict = f"Not started: kickoff {k:%d %b}"
    elif a and (a.get("spend_7d") or 0) > 0:
        # HiddenGem's launch = first spend of a campaign a HiddenGem login created (activity log, 180 days), else one
        # created on or after kickoff. Older campaigns are the client's own or a previous agency's (Dunya Camp's
        # 'Fall step 2', The Preserve's Maddy Watson campaigns).
        def ours_(x):
            who = CREATORS.get(x["id"])
            if who: return is_hg(who.get("name"))
            return bool(k) and (x.get("created") or "") >= (k - datetime.timedelta(days=3)).isoformat()
        ours = [x for x in a.get("campaigns", []) if x.get("first_spend") and ours_(x)]
        launched = datetime.date.fromisoformat(min(x["first_spend"] for x in ours)) if ours else None
        legacy = [x for x in a.get("campaigns", []) if x.get("spend_7d") and x not in ours]
        timing = ""
        if launched and deadline:
            gap = (launched - deadline).days
            timing = f", {gap} days after the {deadline:%d %b} deadline" if gap > 0 else f", on time for the {deadline:%d %b} deadline"
        if launched: verdict = f"Live: ${a['spend_7d']:,.0f} spent in the last 7 days; HiddenGem campaigns first spent {launched:%d %b}{timing}"
        elif deadline and RUN > deadline: verdict = f"LATE: only client or previous-agency campaigns are spending; no HiddenGem campaign has spent, {(RUN - deadline).days} days past the {deadline:%d %b} deadline"
        elif deadline: verdict = f"Not live yet: only client or previous-agency campaigns are spending; HiddenGem deadline {deadline:%d %b} ({(deadline - RUN).days} days left)"
        else: verdict = f"Spending ${a['spend_7d']:,.0f} in 7 days, but no campaign created after kickoff has spent"
        if legacy: verdict += f". Client or previous-agency campaigns still spending: " + "; ".join(f"{x['name']} (${x['spend_7d']:,.0f} in 7d; {legacy_label(x)})" for x in legacy[:4])
    elif deadline and RUN > deadline: verdict = f"LATE: not live, {(RUN - deadline).days} days past the {deadline:%d %b} deadline"
    elif deadline: verdict = f"Not live yet, deadline {deadline:%d %b} ({(deadline - RUN).days} days left)"
    else: verdict = "Not live; no Funnel Build Due date in the CRM, so no deadline"
    L.append(f"### {r['client']} (AM {r['am'] or '—'})"); n_new += 1
    L.append(f"- CRM: kickoff {r['kickoff'] or '—'}, funnel due {r['funnel_due'] or '—'}, Meta Ads {r['meta_ads'] or '—'}, setup {r['setup'] or '—'}, "
             f"share Meta access {r['share_meta_access'] or '—'}, ad campaign setup {r['ad_campaign_setup'] or '—'}, range {r['spend_range'] or '—'}, ROAS goal {r['roas_goal'] or '—'}, "
             f"PMS {r['pms'] or '—'} ({r['pms_conn'] or '—'}), pixel {r['pixel_conn'] or '—'}")
    L.append(f"- Verdict: {verdict}")
    if a:
        acc = a["access"]
        pix = "; ".join(f"{p['name']} ({p['id']}) last fired {str(p.get('last_fired') or 'never')[:10]}" for p in a.get("pixels", [])) or "none visible"
        live_c = [x for x in a.get("campaigns", []) if x["status"] == "ACTIVE"]
        L.append(f"- Ad account {a['id']} ({a.get('name', '?')}): account access {acc['account']}, pixel access {acc['pixel']}; pixels: {pix}")
        L.append(f"- Active campaigns ({len(live_c)}): " + ("; ".join(f"{x['name']} (created {x['created']}, first spend {x.get('first_spend') or 'none in 90d'}{', $' + format(x['daily_budget'], ',.0f') + '/day' if x.get('daily_budget') else ''})" for x in live_c[:8]) or "none"))
    elif mapped: L.append("- Ad account mapped in the benchmark but not in the ad pull (rerun the pull).")
    else: L.append("- No ad account mapped (" + ("listed in ADV_UNMAPPED" if c in unmapped_names else "not in the benchmark's ADV map") + "), so access cannot be tested.")
    s = spend.get(c)
    if s: L.append(f"- Ad spend check: {structure_line(c)}")
    if pixel.get(c): L.append(f"- {pixel_line(c)}")
    if blocks.get(c):
        hg = [l for l in blocks[c] if l.startswith(("Meeting notes", "HG AI notes", "This month"))]
        L += [f"- {short(l, 400)}" for l in hg]
    L += ["- Open Fix List tasks:"] + ([f"  {t}" for t in task_lines(c)] or ["  - none"])
    if not any(norm(a_.get("name", "")) == c or c in [norm(x) for x in a_.get("aliases") or []] for a_ in fl_accounts):
        L.append("- Fix List: no accounts doc yet (tasks for this client would sort last).")
    L.append("")

out_dir = f"{W}/Post-Review/inputs"; os.makedirs(out_dir, exist_ok=True)
p = f"{out_dir}/{DATE}-context.md"
open(p, "w", encoding="utf-8").write("\n".join(L) + "\n")
print(f"wrote {os.path.relpath(p, REPO)}: {len(lists)} listed clients, {n_new} new clients, {len(L)} lines")
