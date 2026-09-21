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
        sections.append(f'''<section class="week" id="{date}">
<div class="sec-head"><div><h2>{esc(label)}</h2><p class="sec-desc">{week} · run date {date}</p></div></div>
<div class="grid3">{"".join(cards)}</div>
</section>''')
    if not sections:
        sections.append('<div class="empty">No reviews yet.</div>')
    n_weeks = len(by_date)
    first = min(by_date) if by_date else ""
    index_css = """
.grid3{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px}
.rcard{display:block;color:inherit;text-decoration:none;transition:box-shadow .15s,border-color .15s}
.rcard:hover{text-decoration:none;border-color:var(--border-strong);box-shadow:0 4px 6px -1px rgba(10,13,18,.10),0 2px 4px -2px rgba(10,13,18,.06)}
.rcard:focus-visible{outline:none;box-shadow:var(--focus)}
.rcard .card-body{display:flex;flex-direction:column;gap:10px;height:100%}
.rcard .hl{display:flex;flex-wrap:wrap;gap:6px}
.rcard .open{margin-top:auto;font:500 14px/20px 'Inter',sans-serif;color:var(--brand-text)}
.rcard.muted{opacity:.6}
.week+.week{border-top:1px solid var(--border);padding-top:28px}
.latest{display:flex;gap:8px;flex-wrap:wrap;margin:-8px 0 28px}
.latest a{font:500 13px/20px 'Inter',sans-serif;padding:6px 12px;border:1px solid var(--border);border-radius:8px;background:var(--panel);color:var(--text-2);box-shadow:var(--shadow-xs)}
.latest a:hover{background:var(--panel-2);text-decoration:none}
"""
    latest_links = "".join(f'<a href="/{slug}/latest.html">{esc(title)}: latest</a>' for slug, title, *_ in WORKFLOWS if slug in latest)
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
<p class="lede">Every Monday's ad spend check, pixel domain check and client benchmark review, newest first. Each report compares against the previous week, so a flag that stays open shows how many weeks it has been open.</p>
<div class="meta"><span class="chip">{n_weeks} week{"s" if n_weeks != 1 else ""} on file</span><span class="chip">Since {first}</span><span class="chip">Internal, HiddenGem Marketing</span></div>
</header>
<div class="latest">{latest_links}</div>
{"".join(sections)}
<div class="foot"><p>Built from the dated reports in the project's Weekly Checks folders. Numbers on the cards come from each report's CSV sidecar.</p></div>
</div>
</body>
</html>
"""
    open(os.path.join(SITE, "index.html"), "w", encoding="utf-8").write(index)
    print(f"site built: {n_weeks} week(s), {sum(len(v) for v in by_date.values())} pages")

if __name__ == "__main__":
    main()
