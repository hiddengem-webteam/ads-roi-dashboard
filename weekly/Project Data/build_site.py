"""Builds the weekly archive into <repo>/public/weekly/ from every dated .html in the three Weekly Checks folders.
The ROI dashboard (Next.js static export) copies public/ into out/, so these pages ship at /weekly/ on the same Netlify site.

  python3 "Project Data/build_site.py"

Output:
  public/weekly/index.html                 all review dates, newest first, three cards per date
  public/weekly/<slug>/<YYYY-MM-DD>.html   each weekly page as a full HTML document with a back link
  public/weekly/<slug>/latest.html         copy of the newest page per workflow
Redirects (/weekly/ad-spend -> latest, etc.) live in the repo's netlify.toml. Commit public/weekly after running this.
"""
import json, csv, collections, datetime, html, os, re, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_html import CSS, BENCH_CSS, wordmark, ROOT  # noqa: E402

SITE = os.path.join(os.path.dirname(ROOT), "public", "weekly")  # <repo>/public/weekly
BASE = "/weekly"  # URL prefix on the merged site
WORKFLOWS = [
    # slug, title, folder, filename suffix, csv suffix, one-line description
    ("ad-spend", "Ad spend check", "Ad Spends Checks/Weekly Checks", "-ad-spend-check.html", "-ad-spend-check.csv",
     "Live daily budget per client and campaign type, and what changed since last week."),
    ("pixel-domains", "Pixel domain check", "Meta Pixel Reviews/Weekly Checks", "-pixel-domain-check.html", "-pixel-domain-check.csv",
     "Which domains fire into each client's pixel, plus 28-day Purchase tracking."),
    ("client-benchmark", "Client benchmark", "Client Benchmark Reviews (advanced setups)/Weekly Checks", "-client-benchmark.html", "-client-benchmark.csv",
     "Advanced clients' Sales campaigns scored on 14-day ROAS, with one-line summaries."),
    # 2026-11-16 (Shawal): the step after the three checks; its sidecar is the post-review JSON, not a CSV
    ("post-review", "Post-review", "Post-Review/Weekly Checks", "-post-review.html", "-post-review.json",
     "What to change: budget shifts, creative asks, new-client launch checks and the Fix List tasks."),
]
DATE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})")

def esc(s): return html.escape(s, quote=False)

BACK_CSS = ".back{display:inline-flex;align-items:center;gap:6px;height:36px;padding:0 14px;border:1px solid var(--border-strong);border-radius:8px;background:var(--panel);color:var(--text-2);font:600 14px/20px 'Inter',sans-serif;box-shadow:var(--shadow-xs);white-space:nowrap;text-decoration:none;transition:background .1s linear,color .1s linear}.back:hover{background:var(--panel-2);color:var(--text);text-decoration:none}.back:focus-visible{outline:none;box-shadow:var(--focus)}.back .arr{font-weight:500}.masthead .right{display:flex;align-items:center;gap:16px;flex-wrap:wrap}.masthead .eyebrow:empty{display:none}"  # 2026-11-16 (Shawal): the back links are buttons, so people can find their way between the reports, the archive and the monthly dashboard

def wrap(page_html, back=True):
    """Turn an artifact-style page (title/link/style then body content) into a full document."""
    m = re.search(r"</style>\s*", page_html)
    head, body = (page_html[:m.end()], page_html[m.end():]) if m else ("", page_html)
    extra_css = BACK_CSS
    if back:
        body = body.replace('<div class="eyebrow">', f'<div class="right"><a class="back" href="{BASE}/"><span class="arr" aria-hidden="true">&#8592;</span>Weekly reviews</a><div class="eyebrow">', 1)
        body = body.replace('</div></div>\n<header class="title">', '</div></div></div>\n<header class="title">', 1)
    return ("<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
            "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1,viewport-fit=cover\">\n"
            "<meta name=\"robots\" content=\"noindex,nofollow\">\n"
            f"{head}<style>{extra_css}</style>\n</head>\n<body>\n{body}\n</body>\n</html>\n")

def headline(slug, csv_path):
    """Short status line for the index card, from the CSV sidecar."""
    if not os.path.exists(csv_path): return []
    if slug == "post-review":
        pr = json.load(open(csv_path, encoding="utf-8")); S = pr.get("sections", {})
        bad = sum(1 for x in S.get("new_clients", []) if x.get("status") in ("late", "blocked", "due"))
        return [("err", f"{len(S.get('flagged', []))} flagged"), ("brand", f"{len(S.get('scale', []))} scale"),
                ("warn", f"{len(S.get('frequency', []))} frequency"), ("warn" if bad else "gray", f"{bad} new clients to chase"),
                ("plain", f"{len(pr.get('tasks_added', []))} tasks added")]
    rows = list(csv.DictReader(open(csv_path, encoding="utf-8")))
    if slug == "ad-spend" and rows and "total_live" in rows[0]:
        live = [r for r in rows if r["source"] == "live"]
        total = sum(float(r["total_live"] or 0) for r in live)
        c = collections.Counter(r["status"] for r in rows)
        return [("plain", f"${total:,.0f}/day live"), ("warn", f"{c['up'] + c['down']} changed"), ("ok", f"{c['new']} new"),
                ("gray", f"{c['blocked']} blocked"), ("plain", f"{len(rows)} clients")]
    if slug in ("ad-spend", "pixel-domains"):
        c = collections.Counter(r["flag"] for r in rows)
        unit = "accounts" if slug == "ad-spend" else "pixel rows"
        return [("err", f"{c['critical']} critical"), ("warn", f"{c['warning']} warning"), ("ok", f"{c['match']} match"),
                ("gray", f"{c.get('blocker', 0)} blocked"), ("plain", f"{len(rows)} {unit}")]
    c = collections.Counter(r["state"] for r in rows)
    return [("err", f"{c['Flag to Shawal']} flag"), ("warn", f"{c['Review w/ HG AI']} review"), ("gray", f"{c['Monitor']} monitor"),
            ("ok", f"{c['Healthy']} healthy"), ("brand", f"{c['Scale w/ HG AI']} scale"),
            ("plain", f"{sum(1 for r in rows if r['state'] not in ('Under gate', 'Tracked in Discovery', 'No promo data') and not r['state'].startswith('Not scored'))} scored, {c['Under gate']} under gate")]

MD_PATHS = {
    "ad-spend": ("Ad Spends Checks/Weekly Checks", "-ad-spend-check.md"),
    "pixel-domains": ("Meta Pixel Reviews/Weekly Checks", "-pixel-domain-check.md"),
    "client-benchmark": ("Client Benchmark Reviews (advanced setups)/Weekly Checks", "-client-benchmark.md"),
}
def _md(slug, date):
    folder, suf = MD_PATHS[slug]
    fp = os.path.join(ROOT, folder, date + suf)
    return open(fp, encoding="utf-8").read() if os.path.exists(fp) else ""
def _prev(md):
    if not md: return None
    m = re.search(r"Previous report[^:\n]*:\s*([^\n]+)", md)
    if not m: return None
    t = m.group(1).strip().rstrip(".")
    return "none, first run" if "first run" in t.lower() or t.lower().startswith("none") else t

def _nice(d):
    return datetime.date.fromisoformat(d).strftime("%-d %b")

def sources_for(date):
    """One small line per week: only the data used ON TOP of the live Meta connector reads."""
    sp, px, bm = _md("ad-spend", date), _md("pixel-domains", date), _md("client-benchmark", date)
    items = []
    # 1. Ads Manager export used as fallback for accounts the connector cannot read
    m = re.search(r"CSV export (\d{4}-\d{2}-\d{2}) to (\d{4}-\d{2}-\d{2}) for (\d+) blocked accounts", sp)
    mb = re.search(r"for the (\d+) accounts the connector cannot read", bm)
    if m or mb:
        rng = f"{_nice(m.group(1))} to {_nice(m.group(2))}" if m else ""
        parts = []
        if m: parts.append(f"{m.group(3)} spend accounts")
        if mb: parts.append(f"{mb.group(1)} benchmark accounts")
        items.append(("warn", f"Ads Manager export {rng}".strip() + f" for {' and '.join(parts)}"))
    # 2. Meeting notes
    meets = re.findall(r"^### (.+?) — (\d{4}-\d{2}-\d{2}) — doc", bm, re.M)
    if meets:
        items.append(("brand", "Meeting notes: " + ", ".join(f"{t} {_nice(d)}" for t, d in meets)))
    elif bm:
        items.append(("gray", "Meeting notes: none found"))
    # 3. Monthly ROI data
    roi = re.search(r"Monthly ROI context from `Monthly ROI data/` \(([^)]*)\)", bm)
    if roi:
        months = [x.strip() for x in roi.group(1).split(",")]
        months.sort(key=lambda x: datetime.datetime.strptime(x, "%B %Y"))
        items.append(("brand", "Monthly ROI data: " + ", ".join(months)))
    # 4. HG AI reports
    hg = re.findall(r"^HG AI notes:\s*(.+)$", bm, re.M)
    if hg:
        used = [x for x in hg if "none" not in x.lower()]
        items.append(("brand", f"HG AI reports: {len(used)} client{'s' if len(used) != 1 else ''}") if used else ("gray", "HG AI reports: none"))
    # 5. previous week's sidecar, only when one was actually compared
    prevs = [_prev(x) for x in (sp, px, bm) if x]
    if prevs and any(p_ and p_ != "none, first run" for p_ in prevs):
        items.append(("gray", "Compared against the previous week's reports"))
    elif prevs:
        items.append(("gray", "First run, no previous week to compare"))
    if not items:
        return ""
    chips = "".join(f'<span class="src {k}"><span class="dot {k}"></span>{esc(t)}</span>' for k, t in items)
    return f'<div class="sources"><span class="src-label">Other data sources</span>{chips}</div>'

def week_badges(slug, csv_path):
    """Key numbers for a week's collapsed row: spend per day, critical pixels, flags and scale."""
    if not os.path.exists(csv_path) or slug == "post-review": return []
    rows = list(csv.DictReader(open(csv_path, encoding="utf-8")))
    if slug == "ad-spend":
        if rows and "total_live" in rows[0]:
            total = sum(float(r["total_live"] or 0) for r in rows if r["source"] == "live")
            return [("gray", f"Spend ${total:,.0f}/day")]
        n = collections.Counter(r["flag"] for r in rows)["critical"]
        return [("err" if n else "gray", f"{n} spend critical")]
    if slug == "pixel-domains":
        n = collections.Counter(r["flag"] for r in rows)["critical"]
        return [("err", f"{n} critical pixel{'s' if n != 1 else ''}") if n else ("ok", "No critical pixels")]
    c = collections.Counter(r["state"] for r in rows)
    f, sc = c["Flag to Shawal"], c["Scale w/ HG AI"]
    return [("err" if f else "gray", f"{f} flag{'s' if f != 1 else ''}"), ("brand", f"{sc} scale")]

def main():
    if os.path.isdir(SITE): shutil.rmtree(SITE)
    os.makedirs(SITE)
    by_date = collections.defaultdict(dict)  # date -> slug -> (href, headline)
    csvs = collections.defaultdict(dict)     # date -> slug -> CSV sidecar path
    latest = {}
    for slug, title, folder, suf, csv_suf, desc in WORKFLOWS:
        src_dir = os.path.join(ROOT, folder)
        out_dir = os.path.join(SITE, slug); os.makedirs(out_dir)
        dates = []
        for fn in sorted(os.listdir(src_dir)):
            m = DATE_RE.match(fn)
            if not (m and fn.endswith(suf)): continue
            date = m.group(1); dates.append(date)
            page = open(os.path.join(src_dir, fn), encoding="utf-8").read()
            open(os.path.join(out_dir, f"{date}.html"), "w", encoding="utf-8").write(wrap(page))
            by_date[date][slug] = (f"{BASE}/{slug}/{date}.html", headline(slug, os.path.join(src_dir, date + csv_suf)))
            csvs[date][slug] = os.path.join(src_dir, date + csv_suf)
        if dates:
            latest[slug] = dates[-1]
            shutil.copyfile(os.path.join(out_dir, f"{dates[-1]}.html"), os.path.join(out_dir, "latest.html"))
    # redirects (/weekly/<slug> -> latest) are declared in the repo's netlify.toml, not generated here
    # index: a filter bar (month) and one collapsible card per week, latest open
    weeks_html = []
    dates_desc = sorted(by_date, reverse=True)
    for i, date in enumerate(dates_desc):
        d = datetime.date.fromisoformat(date)
        label = d.strftime("%A %-d %B %Y"); week = f"W{d.isocalendar()[1]}"
        cards, badges = [], []
        for slug, title, folder, suf, csv_suf, desc in WORKFLOWS:
            if slug not in by_date[date]:
                if slug == "post-review" and date < "2026-11-16": continue  # the step started on 16 Nov 2026
                cards.append(f'<div class="card rcard muted" data-review="{slug}"><div class="card-body"><h3>{esc(title)}</h3><p class="sec-desc">Not run this week.</p></div></div>'); continue
            href, hl = by_date[date][slug]
            chips = "".join(
                (f'<span class="chip">{esc(t)}</span>' if k == "plain" else f'<span class="badge {k}"><span class="dot {k}"></span>{esc(t)}</span>')
                for k, t in hl)
            cards.append(f'''<a class="card rcard" href="{href}" data-review="{slug}"><div class="card-body">
<h3>{esc(title)}</h3><p class="sec-desc">{esc(desc)}</p>
<div class="hl">{chips}</div>
<div class="open">Open report &#8594;</div></div></a>''')
            badges += [f'<span class="badge {k}" data-review="{slug}"><span class="dot {k}"></span>{esc(t)}</span>'
                       for k, t in week_badges(slug, csvs[date][slug])]
        eyebrow = f"{week} · Latest" if i == 0 else week
        weeks_html.append(f'''<details class="card wk" id="{date}" data-month="{date[:7]}"{" open" if i == 0 else ""}>
<summary><span class="chev" aria-hidden="true"></span><span class="wmain"><span class="eb">{esc(eyebrow)}</span><span class="wtitle">{esc(label)}</span></span><span class="wbadges">{"".join(badges)}</span><span class="tact" aria-hidden="true"></span></summary>
<div class="wbody">
<div class="grid3">{"".join(cards)}</div>
{sources_for(date)}
</div>
</details>''')
    n_weeks = len(by_date)
    months = collections.OrderedDict()
    for date in dates_desc:
        months.setdefault(date[:7], []).append(date)
    month_opts = "".join(f'<option value="{ym}">{datetime.date.fromisoformat(ds[0]).strftime("%B %Y")} ({len(ds)})</option>' for ym, ds in months.items())
    if by_date:
        d0, d1 = datetime.date.fromisoformat(min(by_date)), datetime.date.fromisoformat(max(by_date))
        span = f"{d0.day} {d0:%b} – {d1.day} {d1:%b %Y}" if d0.year == d1.year else f"{d0.day} {d0:%b %Y} – {d1.day} {d1:%b %Y}"
    else:
        span = "No reviews yet"
    fbar = f"""<div class="fbar" id="fbar" role="search" aria-label="Filter reviews" hidden>
<div class="fld"><label for="f-month">Month</label><span class="sel"><select id="f-month"><option value="all">All months</option>{month_opts}</select></span></div>
<button type="button" class="btn" id="f-clear" hidden>Clear filters</button>
<p class="fsum" id="f-sum" aria-live="polite">{n_weeks} week{"s" if n_weeks != 1 else ""}</p>
<button type="button" class="btn" id="x-all">Expand all</button>
</div>"""
    index_css = """
.wlist{display:flex;flex-direction:column;gap:12px}
.wlist>.card+.card{margin-top:0}
.wk{scroll-margin-top:110px}
.wk>summary{list-style:none;cursor:pointer;display:grid;grid-template-columns:10px minmax(0,1fr) auto auto;grid-template-areas:"chev main badges act";gap:8px 18px;align-items:center;padding:16px 20px;transition:background .1s linear}
.wk>summary::-webkit-details-marker{display:none}
.wk>summary:hover{background:var(--panel-2)}
.wk>summary:focus-visible{box-shadow:inset var(--focus);border-radius:12px}
.wk[open]>summary{border-bottom:1px solid var(--border)}
.wk .chev{grid-area:chev;width:8px;height:8px;border-right:1.5px solid var(--text-3);border-bottom:1.5px solid var(--text-3);transform:rotate(-45deg);transition:transform .24s cubic-bezier(.2,0,0,1)}
.wk[open]>summary .chev{transform:rotate(45deg)}
.wk .wmain{grid-area:main;display:flex;flex-direction:column;min-width:0}
.wk .eb{margin:0}
.wk .wtitle{font:600 20px/30px 'Inter',sans-serif;letter-spacing:-.01em;color:var(--text)}
.wk .wbadges{grid-area:badges;display:flex;flex-wrap:wrap;gap:6px;justify-content:flex-end}
.wk .tact{grid-area:act;font:600 14px/20px 'Inter',sans-serif;color:var(--brand-text)}
.wk .tact::after{content:"Show"}
.wk[open] .tact::after{content:"Hide"}
.wbody{padding:20px;display:flex;flex-direction:column;gap:16px}
.grid3{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px}
.grid3>.card+.card{margin-top:0}
.rcard{display:block;color:inherit;text-decoration:none;box-shadow:none;transition:border-color .1s linear,background .1s linear}
.rcard:hover{text-decoration:none;border-color:var(--border-strong);background:var(--hover)}
.rcard:focus-visible{outline:none;box-shadow:var(--focus)}
.rcard .card-body{display:flex;flex-direction:column;gap:10px;height:100%}
.rcard .hl{display:flex;flex-wrap:wrap;gap:6px}
.rcard .open{margin-top:auto;font:600 14px/20px 'Inter',sans-serif;color:var(--brand-text)}
.rcard.muted{opacity:.6}
.sources{display:flex;flex-wrap:wrap;align-items:center;gap:6px 8px;margin:0}
.src-label{font:500 12px/18px 'Inter',sans-serif;color:var(--text-4);margin-right:2px}
.src{display:inline-flex;align-items:center;gap:6px;font:400 12px/18px 'Inter',sans-serif;color:var(--text-3);padding:2px 10px 2px 8px;border:1px solid var(--border);border-radius:9999px;background:var(--panel)}
.src .dot{width:6px;height:6px}
.genline{margin:24px 0 0}
@media (max-width:640px){.wk>summary{grid-template-columns:10px minmax(0,1fr);grid-template-areas:"chev main" ". badges";padding:14px 16px}.wk .wbadges{justify-content:flex-start}.wk .tact{display:none}.wbody{padding:16px}}
@media (prefers-reduced-motion: reduce){.wk .chev{transition:none}}
"""
    index_js = """
(function(){
  const bar=document.getElementById('fbar'); if(!bar) return;
  const mSel=document.getElementById('f-month');   // Review filter removed 2026-11-16 (Shawal)
  const clr=document.getElementById('f-clear'), sum=document.getElementById('f-sum'), xall=document.getElementById('x-all');
  const weeks=[...document.querySelectorAll('details.wk')], empty=document.getElementById('w-empty');
  const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
  const plural=(n,w)=>n+' '+w+(n===1?'':'s');
  const label=s=>s.options[s.selectedIndex].text.replace(/ \\(\\d+\\)$/,'');
  function xlabel(){ const vis=weeks.filter(w=>!w.hidden); xall.textContent=vis.length&&vis.every(w=>w.open)?'Collapse all':'Expand all'; }
  function apply(){
    const m=mSel.value, on=m!=='all';
    mSel.classList.toggle('on',on);
    let n=0;
    weeks.forEach(w=>{
      const s=m==='all'||w.dataset.month===m; w.hidden=!s; if(s) n++;
    });
    empty.hidden=n>0;
    const who=on?label(mSel):'';
    sum.innerHTML=on?'Showing <strong>'+plural(n,'week')+'</strong> of '+weeks.length+' · '+who:plural(weeks.length,'week');
    clr.hidden=!on; xlabel();
    try{const u=new URL(location.href);
      if(m==='all')u.searchParams.delete('month');else u.searchParams.set('month',m);
      u.searchParams.delete('review');
      history.replaceState(null,'',u);}catch(e){}
  }
  mSel.addEventListener('change',apply);
  clr.addEventListener('click',()=>{mSel.value='all';apply();mSel.focus();});
  xall.addEventListener('click',()=>{const vis=weeks.filter(w=>!w.hidden), open=!vis.every(w=>w.open); vis.forEach(w=>{w.open=open;}); xlabel();});
  weeks.forEach(w=>w.addEventListener('toggle',xlabel));
  const q=new URLSearchParams(location.search), has=(s,v)=>[...s.options].some(o=>o.value===v);
  if(has(mSel,q.get('month'))) mSel.value=q.get('month');
  bar.hidden=false; apply();
  // an old #YYYY-MM-DD link opens that week (widening the month filter if needed)
  const h=location.hash.slice(1), t=/^\\d{4}-\\d{2}-\\d{2}$/.test(h)&&document.getElementById(h);
  if(t){ if(t.hidden){mSel.value='all';apply();} t.open=true; xlabel(); t.scrollIntoView({behavior:reduce?'auto':'smooth',block:'start'}); }
})();
"""
    index = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="robots" content="noindex,nofollow">
<title>Meta Ads Weekly Reviews</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Roboto+Mono:wght@400;500&display=swap">
<style>{CSS}{BENCH_CSS}{index_css}{BACK_CSS}</style>
</head>
<body>
<div class="page">
<div class="masthead">{wordmark}<div class="right"><a class="back" href="/"><span class="arr" aria-hidden="true">&#8592;</span>Monthly ROI dashboard</a></div></div>
<header class="title"><h1>Meta Ads Weekly Reviews</h1><p class="lede">{esc(span)}</p></header>
{fbar}
<div class="wlist">{"".join(weeks_html) or '<div class="empty">No reviews yet.</div>'}</div>
<div class="empty" id="w-empty" hidden>No weeks match this filter.</div>
<p class="genline">Built from the dated reports in weekly/*/Weekly Checks. Served at /weekly/ by the ROI dashboard. Numbers on the cards come from each report's CSV sidecar.</p>
</div>
<script>{index_js}</script>
</body>
</html>
"""
    open(os.path.join(SITE, "index.html"), "w", encoding="utf-8").write(index)
    print(f"public/weekly built: {n_weeks} week(s), {sum(len(v) for v in by_date.values())} pages")

if __name__ == "__main__":
    main()
