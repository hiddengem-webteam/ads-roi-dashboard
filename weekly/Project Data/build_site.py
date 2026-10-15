"""Builds the static site in ../site/ from every dated .html in the three Weekly Checks folders.

  python3 "Project Data/build_site.py"

Output:
  site/index.html                     all review dates, newest first, three cards per date
  site/<slug>/<YYYY-MM-DD>.html        each weekly page as a full HTML document with a back link
  site/<slug>/latest.html              copy of the newest page per workflow
  site/_redirects                      /ad-spend -> latest, etc.
Netlify publishes site/ as-is (netlify.toml, no build command), so run this before committing.
"""
import csv, collections, datetime, html, os, re, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_html import CSS, wordmark, ROOT  # noqa: E402

SITE = os.path.join(ROOT, "site")
WORKFLOWS = [
    # slug, title, folder, filename suffix, csv suffix, one-line description
    ("ad-spend", "Ad spend check", "Ad Spends Checks/Weekly Checks", "-ad-spend-check.html", "-ad-spend-check.csv",
     "Documented daily budget on the Master sheet vs the live budget in each ad account."),
    ("pixel-domains", "Pixel domain check", "Meta Pixel Reviews/Weekly Checks", "-pixel-domain-check.html", "-pixel-domain-check.csv",
     "Which domains fire into each client's Meta Pixel; cross-contamination, silent and split pixels."),
    ("client-benchmark", "Client benchmark", "Client Benchmark Reviews (advanced setups)/Weekly Checks", "-client-benchmark.html", "-client-benchmark.csv",
     "Lead Gen and Sales campaigns of CRM-Advanced clients scored against the Benchmarks doc."),
]
DATE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})")

def esc(s): return html.escape(s, quote=False)

def wrap(page_html, back=True):
    """Turn an artifact-style page (title/link/style then body content) into a full document."""
    m = re.search(r"</style>\s*", page_html)
    head, body = (page_html[:m.end()], page_html[m.end():]) if m else ("", page_html)
    extra_css = ".back{font:500 13px/20px 'Inter',sans-serif;color:var(--text-3);display:inline-flex;align-items:center;gap:6px}.back:hover{color:var(--text);text-decoration:none}.masthead .right{display:flex;align-items:center;gap:16px;flex-wrap:wrap}"
    if back:
        body = body.replace('<div class="eyebrow">', '<div class="right"><a class="back" href="/">&#8592; All reviews</a><div class="eyebrow">', 1)
        body = body.replace('</div></div>\n<header class="title">', '</div></div></div>\n<header class="title">', 1)
    return ("<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
            "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1,viewport-fit=cover\">\n"
            "<meta name=\"robots\" content=\"noindex,nofollow\">\n"
            f"{head}<style>{extra_css}</style>\n</head>\n<body>\n{body}\n</body>\n</html>\n")

def headline(slug, csv_path):
    """Short status line for the index card, from the CSV sidecar."""
    if not os.path.exists(csv_path): return []
    rows = list(csv.DictReader(open(csv_path, encoding="utf-8")))
    if slug in ("ad-spend", "pixel-domains"):
        c = collections.Counter(r["flag"] for r in rows)
        unit = "accounts" if slug == "ad-spend" else "pixel rows"
        return [("err", f"{c['critical']} critical"), ("warn", f"{c['warning']} warning"), ("ok", f"{c['match']} match"),
                ("gray", f"{c.get('blocker', 0)} blocked"), ("plain", f"{len(rows)} {unit}")]
    c = collections.Counter(r["state"] for r in rows)
    return [("err", f"{c['Flag to Shawal']} flag"), ("warn", f"{c['Review w/ HG AI']} review"), ("gray", f"{c['Monitor']} monitor"),
            ("ok", f"{c['Healthy']} healthy"), ("brand", f"{c['Scale w/ HG AI']} scale"),
            ("plain", f"{sum(1 for r in rows if r['state'] != 'Under gate')} scored, {c['Under gate']} under gate")]

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
    return f'<div class="sources"><span class="src-label">Data sources in addition to Meta MCP</span>{chips}</div>'

def main():
    if os.path.isdir(SITE): shutil.rmtree(SITE)
    os.makedirs(SITE)
    by_date = collections.defaultdict(dict)  # date -> slug -> (href, headline)
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
            by_date[date][slug] = (f"/{slug}/{date}.html", headline(slug, os.path.join(src_dir, date + csv_suf)))
        if dates:
            latest[slug] = dates[-1]
            shutil.copyfile(os.path.join(out_dir, f"{dates[-1]}.html"), os.path.join(out_dir, "latest.html"))
    # redirects
    open(os.path.join(SITE, "_redirects"), "w").write("".join(f"/{slug}  /{slug}/latest.html  302\n" for slug in latest))
    # index
    sections = []
    for date in sorted(by_date, reverse=True):
        d = datetime.date.fromisoformat(date)
        label = d.strftime("%A %-d %B %Y"); week = f"W{d.isocalendar()[1]}"
        cards = []
        for slug, title, folder, suf, csv_suf, desc in WORKFLOWS:
            if slug not in by_date[date]:
                cards.append(f'<div class="card rcard muted"><div class="card-body"><h3>{esc(title)}</h3><p class="sec-desc">Not run this week.</p></div></div>'); continue
            href, hl = by_date[date][slug]
            chips = "".join(
                (f'<span class="chip">{esc(t)}</span>' if k == "plain" else f'<span class="badge {k}"><span class="dot {k}"></span>{esc(t)}</span>')
                for k, t in hl)
            cards.append(f'''<a class="card rcard" href="{href}"><div class="card-body">
<h3>{esc(title)}</h3><p class="sec-desc">{esc(desc)}</p>
<div class="hl">{chips}</div>
<div class="open">Open report &#8594;</div></div></a>''')
        sections.append(f'''<section class="week" id="{date}" data-month="{date[:7]}">
<div class="sec-head"><div><h2>{esc(label)}</h2><p class="sec-desc">{week} · run date {date}</p></div></div>
{sources_for(date)}
<div class="grid3">{"".join(cards)}</div>
</section>''')
    if not sections:
        sections.append('<div class="empty">No reviews yet.</div>')
    n_weeks = len(by_date)
    first = min(by_date) if by_date else ""
    # ---- sidebar: months -> Mondays
    months = collections.OrderedDict()
    for date in sorted(by_date, reverse=True):
        months.setdefault(date[:7], []).append(date)
    side_items = []
    for i, (ym, dates) in enumerate(months.items()):
        d0 = datetime.date.fromisoformat(dates[0])
        label = d0.strftime("%B %Y"); n = len(dates)
        weeks = "".join(
            f'<li><a class="wk" href="#{dt}" data-week="{dt}">{datetime.date.fromisoformat(dt).strftime("%a %-d %b")}'
            f'<span class="wn">W{datetime.date.fromisoformat(dt).isocalendar()[1]}</span></a></li>' for dt in dates)
        side_items.append(
            f'<li class="mo"><button type="button" class="month" data-month="{ym}" aria-expanded="{"true" if i == 0 else "false"}" aria-controls="m-{ym}">'
            f'<svg class="chev" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m9 18 6-6-6-6"/></svg>'
            f'<span class="mlabel">{esc(label)}</span><span class="count">{n} week{"s" if n != 1 else ""}</span></button>'
            f'<ul class="weeks" id="m-{ym}"{"" if i == 0 else " hidden"}>{weeks}</ul></li>')
    sidebar = f'''<nav class="side" aria-label="Reviews by month">
<div class="side-title">Browse</div>
<ul class="months">
<li><button type="button" class="month all" data-month="all" aria-pressed="false"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg><span class="mlabel">All weeks</span><span class="count">{n_weeks}</span></button></li>
{"".join(side_items)}
</ul>
<div class="side-title" style="margin-top:20px">Latest</div>
<ul class="months latest-list">{"".join(f'<li><a class="wk" href="/{slug}/latest.html">{esc(title)}</a></li>' for slug, title, *_ in WORKFLOWS if slug in latest)}</ul>
</nav>'''
    index_css = """
.layout{display:grid;grid-template-columns:240px minmax(0,1fr);gap:40px;align-items:start}
.side{position:sticky;top:24px}
.side-title{font:500 12px/18px 'Inter',sans-serif;color:var(--text-4);padding:0 12px 6px}
.months{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:2px}
.month{appearance:none;width:100%;display:flex;align-items:center;gap:8px;padding:8px 12px;border:0;border-radius:8px;background:transparent;color:var(--text-2);font:500 14px/20px 'Inter',sans-serif;text-align:left;cursor:pointer;transition:background .15s,color .15s}
.month:hover{background:var(--panel-3);color:var(--text)}
.month:focus-visible{outline:none;box-shadow:var(--focus)}
.month[aria-expanded="true"],.month[aria-pressed="true"]{background:var(--brand-bg);color:var(--brand-text)}
.month .mlabel{flex:1}
.month .count{font:500 12px/18px 'Inter',sans-serif;color:var(--text-4)}
.month[aria-expanded="true"] .count,.month[aria-pressed="true"] .count{color:inherit;opacity:.8}
.month svg{flex:none;color:var(--text-4)}
.month[aria-expanded="true"] svg,.month[aria-pressed="true"] svg{color:inherit}
.chev{transition:transform .15s}
.month[aria-expanded="true"]:not(.collapsed) .chev{transform:rotate(90deg)}
.weeks{list-style:none;margin:2px 0 6px;padding:0 0 0 14px;display:flex;flex-direction:column;gap:2px;border-left:1px solid var(--border);margin-left:19px}
.wk{display:flex;align-items:center;justify-content:space-between;gap:8px;padding:6px 10px;border-radius:6px;color:var(--text-3);font:400 14px/20px 'Inter',sans-serif;text-decoration:none}
.wk:hover{background:var(--panel-3);color:var(--text);text-decoration:none}
.wk[aria-current="true"]{color:var(--brand-text);font-weight:500}
.wk .wn{font:500 12px/18px 'Roboto Mono',monospace;color:var(--text-4)}
.latest-list .wk{padding-left:12px}
.grid3{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px}
.rcard{display:block;color:inherit;text-decoration:none;transition:box-shadow .15s,border-color .15s}
.rcard:hover{text-decoration:none;border-color:var(--border-strong);box-shadow:0 4px 6px -1px rgba(10,13,18,.10),0 2px 4px -2px rgba(10,13,18,.06)}
.rcard:focus-visible{outline:none;box-shadow:var(--focus)}
.rcard .card-body{display:flex;flex-direction:column;gap:10px;height:100%}
.rcard .hl{display:flex;flex-wrap:wrap;gap:6px}
.rcard .open{margin-top:auto;font:500 14px/20px 'Inter',sans-serif;color:var(--brand-text)}
.rcard.muted{opacity:.6}
.week{scroll-margin-top:24px}
.sources{display:flex;flex-wrap:wrap;align-items:center;gap:6px 8px;margin:0 0 16px}
.src-label{font:500 12px/18px 'Inter',sans-serif;color:var(--text-4);margin-right:2px}
.src{display:inline-flex;align-items:center;gap:6px;font:400 12px/18px 'Inter',sans-serif;color:var(--text-3);padding:2px 10px 2px 8px;border:1px solid var(--border);border-radius:9999px;background:var(--panel)}
.src .dot{width:6px;height:6px}
.week+.week{border-top:1px solid var(--border);padding-top:28px}
.month-head{font:500 12px/18px 'Inter',sans-serif;color:var(--text-4);margin:0 0 12px}
@media (max-width:900px){
  .layout{grid-template-columns:1fr;gap:20px}
  .side{position:static;background:var(--panel);border:1px solid var(--border);border-radius:12px;padding:12px;box-shadow:var(--shadow-xs)}
}
"""
    index_js = """
(function(){
  const monthBtns=[...document.querySelectorAll('.month[data-month]')];
  const weekLinks=[...document.querySelectorAll('.wk[data-week]')];
  const sections=[...document.querySelectorAll('section.week')];
  const head=document.getElementById('month-head');
  function show(month){
    monthBtns.forEach(b=>{
      const isAll=b.dataset.month==='all';
      if(isAll){ b.setAttribute('aria-pressed', month==='all'?'true':'false'); return; }
      const on=b.dataset.month===month;
      b.setAttribute('aria-expanded', on?'true':'false');
      if(on) b.classList.remove('collapsed');
      const list=document.getElementById(b.getAttribute('aria-controls')); if(list) list.hidden=!on;
    });
    let n=0;
    sections.forEach(s=>{const v=month==='all'||s.dataset.month===month; s.hidden=!v; if(v)n++;});
    if(head){
      if(month==='all') head.textContent='All '+n+' week'+(n===1?'':'s');
      else { const d=new Date(month+'-01T00:00:00'); head.textContent=d.toLocaleString('en-GB',{month:'long',year:'numeric'})+' \u00b7 '+n+' week'+(n===1?'':'s'); }
    }
    try{localStorage.setItem('reviews.month',month);}catch(e){}
  }
  function current(week){ weekLinks.forEach(a=>a.setAttribute('aria-current', a.dataset.week===week?'true':'false')); }
  monthBtns.forEach(b=>b.addEventListener('click',()=>{
    const m=b.dataset.month;
    if(m!=='all' && b.getAttribute('aria-expanded')==='true'){
      // already selected: collapse or re-open its week list, keep the filter
      const list=document.getElementById(b.getAttribute('aria-controls'));
      const open=list && !list.hidden;
      if(list) list.hidden=open;
      b.classList.toggle('collapsed', open);
      return;
    }
    b.classList.remove('collapsed');
    show(m); current(null);
  }));
  weekLinks.forEach(a=>a.addEventListener('click',e=>{
    const w=a.dataset.week; show(w.slice(0,7)); current(w);
    const t=document.getElementById(w); if(t){ e.preventDefault(); history.replaceState(null,'','#'+w); t.scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth',block:'start'}); }
  }));
  let start=null;
  const h=location.hash.replace('#','');
  if(/^\d{4}-\d{2}-\d{2}$/.test(h) && document.getElementById(h)){ start=h.slice(0,7); show(start); current(h); document.getElementById(h).scrollIntoView(); return; }
  try{ const saved=localStorage.getItem('reviews.month'); if(saved && (saved==='all' || monthBtns.some(b=>b.dataset.month===saved))) start=saved; }catch(e){}
  if(!start){ const first=monthBtns.find(b=>b.dataset.month!=='all'); start=first?first.dataset.month:'all'; }
  show(start);
})();
"""
    index = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="robots" content="noindex,nofollow">
<title>Meta Ads weekly reviews</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Roboto+Mono:wght@400;500&display=swap">
<style>{CSS}{index_css}</style>
</head>
<body>
<div class="page">
<div class="masthead">{wordmark}<div class="eyebrow">Weekly Meta Ads review · Archive</div></div>
<header class="title"><h1>Meta Ads weekly reviews</h1>
<p class="lede">Every Monday's ad spend check, pixel domain check and client benchmark review. Pick a month on the left to see its weeks; each report compares against the previous week, so a flag that stays open shows how many weeks it has been open.</p>
<div class="meta"><span class="chip">{n_weeks} week{"s" if n_weeks != 1 else ""} on file</span><span class="chip">Since {first}</span><span class="chip">Internal, HiddenGem Marketing</span></div>
</header>
<div class="layout">
{sidebar}
<main>
<p class="month-head" id="month-head"></p>
{"".join(sections)}
<div class="foot"><p>Built from the dated reports in the project's Weekly Checks folders. Numbers on the cards come from each report's CSV sidecar.</p></div>
</main>
</div>
</div>
<script>{index_js}</script>
</body>
</html>
"""
    open(os.path.join(SITE, "index.html"), "w", encoding="utf-8").write(index)
    print(f"site built: {n_weeks} week(s), {sum(len(v) for v in by_date.values())} pages")

if __name__ == "__main__":
    main()
