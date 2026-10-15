"""HTML report builder for the three weekly Meta Ads reviews.
Styled from the HiddenGem Media design system (claude.ai/artifact/GXb4YMfP8uFmoTPhnWujSk):
Inter + Roboto Mono, neutral canvas, brand blue #0066DE for accents, semantic badges, no emoji.
Each page is published as a claude.ai artifact; republish to the same URL (see PROJECT.md section 4.4).
"""
import csv, re, html, collections, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import sys
WORDMARK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "hg-wordmark.svg")
import datetime
# Usage: python3 build_html.py [YYYY-MM-DD]   (defaults to today). Reads the dated .md + .csv of each workflow, writes the dated .html beside them.
DATE = sys.argv[1] if len(sys.argv) > 1 else datetime.date.today().isoformat()
_d = datetime.date.fromisoformat(DATE); WEEK = f"W{_d.isocalendar()[1]}"; RUN = _d.strftime("%-d %B %Y")

# ---------------- design system ----------------
wordmark = open(WORDMARK, encoding="utf-8").read()
wordmark = wordmark.replace('fill="#0A0D12"', 'fill="currentColor"').replace('width="182" height="22"', 'class="wordmark" width="182" height="22" role="img" aria-label="HiddenGem"')

CSS = """
:root{
  --bg:#fafafa; --panel:#ffffff; --panel-2:#fafafa; --panel-3:#f5f5f5;
  --border:#e5e5e5; --border-strong:#d4d4d4;
  --text:#171717; --text-2:#404040; --text-3:#525252; --text-4:#737373;
  --brand:#0066de; --brand-text:#004faa; --brand-bg:#f6f9ff; --brand-border:#cee0ff;
  --ok-text:#15803d; --ok-dot:#16a34a; --ok-bg:#f0fdf4; --ok-border:#dcfce7;
  --warn-text:#a16207; --warn-dot:#ca8a04; --warn-bg:#fefce8; --warn-border:#fef9c3;
  --err-text:#b91c1c; --err-dot:#dc2626; --err-bg:#fef2f2; --err-border:#fee2e2;
  --gray-text:#525252; --gray-dot:#a3a3a3; --gray-bg:#f5f5f5; --gray-border:#e5e5e5;
  --shadow-xs:0 1px 2px 0 rgba(10,13,18,.05);
  --focus:0 0 0 4px rgba(0,102,222,.24);
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){
  --bg:#0a0a0a; --panel:#171717; --panel-2:#1f1f1f; --panel-3:#262626;
  --border:#262626; --border-strong:#404040;
  --text:#fafafa; --text-2:#d4d4d4; --text-3:#a3a3a3; --text-4:#a3a3a3;
  --brand:#2b7fff; --brand-text:#cee0ff; --brand-bg:rgba(0,102,222,.16); --brand-border:rgba(43,127,255,.35);
  --ok-text:#4ade80; --ok-dot:#22c55e; --ok-bg:rgba(34,197,94,.12); --ok-border:rgba(34,197,94,.3);
  --warn-text:#facc15; --warn-dot:#eab308; --warn-bg:rgba(234,179,8,.12); --warn-border:rgba(234,179,8,.3);
  --err-text:#f87171; --err-dot:#ef4444; --err-bg:rgba(239,68,68,.12); --err-border:rgba(239,68,68,.3);
  --gray-text:#d4d4d4; --gray-dot:#737373; --gray-bg:#262626; --gray-border:#404040;
  --shadow-xs:0 1px 2px 0 rgba(0,0,0,.4);
}}
:root[data-theme="dark"]{
  --bg:#0a0a0a; --panel:#171717; --panel-2:#1f1f1f; --panel-3:#262626;
  --border:#262626; --border-strong:#404040;
  --text:#fafafa; --text-2:#d4d4d4; --text-3:#a3a3a3; --text-4:#a3a3a3;
  --brand:#2b7fff; --brand-text:#cee0ff; --brand-bg:rgba(0,102,222,.16); --brand-border:rgba(43,127,255,.35);
  --ok-text:#4ade80; --ok-dot:#22c55e; --ok-bg:rgba(34,197,94,.12); --ok-border:rgba(34,197,94,.3);
  --warn-text:#facc15; --warn-dot:#eab308; --warn-bg:rgba(234,179,8,.12); --warn-border:rgba(234,179,8,.3);
  --err-text:#f87171; --err-dot:#ef4444; --err-bg:rgba(239,68,68,.12); --err-border:rgba(239,68,68,.3);
  --gray-text:#d4d4d4; --gray-dot:#737373; --gray-bg:#262626; --gray-border:#404040;
  --shadow-xs:0 1px 2px 0 rgba(0,0,0,.4);
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--text);font:400 16px/24px 'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;-webkit-font-smoothing:antialiased}
.page{max-width:1200px;margin:0 auto;padding-block:32px 64px;padding-inline:32px}
@media (max-width:640px){.page{padding-inline:16px;padding-block:20px 48px}}
a{color:var(--brand-text);text-decoration:none}a:hover{text-decoration:underline}
code,.mono{font-family:'Roboto Mono',ui-monospace,'SF Mono',Menlo,monospace;font-size:.9em}
.wordmark{display:block;color:var(--text);height:22px;width:auto}
.masthead{display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap;padding-bottom:20px;border-bottom:1px solid var(--border);margin-bottom:28px}
.masthead .eyebrow{font:500 12px/18px 'Roboto Mono',ui-monospace,monospace;letter-spacing:.04em;text-transform:uppercase;color:var(--text-4)}
header.title{display:flex;flex-direction:column;gap:8px;margin-bottom:24px}
h1{font:600 30px/38px 'Inter',sans-serif;letter-spacing:-.02em;margin:0;text-wrap:balance}
.lede{margin:0;color:var(--text-3);max-width:72ch}
.meta{display:flex;gap:8px;flex-wrap:wrap;margin-top:4px}
.chip{display:inline-flex;align-items:center;gap:6px;padding:2px 10px;border:1px solid var(--border);border-radius:9999px;background:var(--panel);font:500 12px/18px 'Inter',sans-serif;color:var(--text-3)}
.chip .mono{font-size:12px}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin-bottom:32px}
.stat{background:var(--panel);border:1px solid var(--border);border-radius:12px;padding:16px 18px;box-shadow:var(--shadow-xs);display:flex;flex-direction:column;gap:4px;min-width:0}
.stat .label{font:500 13px/18px 'Inter',sans-serif;color:var(--text-3);display:flex;align-items:center;gap:6px}
.stat .value{font:600 26px/32px 'Inter',sans-serif;letter-spacing:-.02em;font-variant-numeric:tabular-nums}
.stat .hint{font:400 12px/18px 'Inter',sans-serif;color:var(--text-4)}
.dot{width:8px;height:8px;border-radius:9999px;display:inline-block;flex:none}
.dot.ok{background:var(--ok-dot)}.dot.warn{background:var(--warn-dot)}.dot.err{background:var(--err-dot)}.dot.gray{background:var(--gray-dot)}.dot.brand{background:var(--brand)}
section{margin-bottom:36px}
.sec-head{display:flex;align-items:flex-end;justify-content:space-between;gap:16px;flex-wrap:wrap;margin-bottom:12px}
h2{font:600 20px/30px 'Inter',sans-serif;letter-spacing:-.01em;margin:0}
h3{font:600 16px/24px 'Inter',sans-serif;margin:0}
.sec-desc{margin:2px 0 0;color:var(--text-3);font-size:14px;line-height:20px;max-width:80ch}
.card{background:var(--panel);border:1px solid var(--border);border-radius:12px;box-shadow:var(--shadow-xs);overflow:hidden}
.card + .card{margin-top:16px}
.card-head{padding:16px 20px;border-bottom:1px solid var(--border);display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;align-items:center}
.card-head .sub{color:var(--text-3);font-size:14px;line-height:20px}
.card-body{padding:16px 20px}
.tablewrap{overflow-x:auto}
table{border-collapse:collapse;width:100%;font-size:14px;line-height:20px}
thead th{text-align:left;font:500 12px/18px 'Inter',sans-serif;color:var(--text-3);background:var(--panel-2);padding:10px 16px;border-bottom:1px solid var(--border);white-space:nowrap}
tbody td{padding:12px 16px;border-bottom:1px solid var(--border);vertical-align:top;color:var(--text-2)}
tbody tr:last-child td{border-bottom:0}
tbody tr:hover td{background:var(--panel-2)}
td.first{font-weight:500;color:var(--text);white-space:nowrap}
td.num,th.num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
td.mono{font-size:13px;white-space:nowrap;color:var(--text-3)}
td.notes{min-width:280px;max-width:560px;font-size:13px;line-height:19px;color:var(--text-3)}
td.domains{min-width:220px;max-width:360px;font-size:13px;line-height:19px;color:var(--text-3);word-break:break-word}
td.nowrap{white-space:nowrap}
.badge{display:inline-flex;align-items:center;gap:6px;padding:2px 8px 2px 7px;border-radius:9999px;font:500 12px/18px 'Inter',sans-serif;white-space:nowrap;border:1px solid}
.badge .dot{width:6px;height:6px}
.badge.ok{color:var(--ok-text);background:var(--ok-bg);border-color:var(--ok-border)}
.badge.warn{color:var(--warn-text);background:var(--warn-bg);border-color:var(--warn-border)}
.badge.err{color:var(--err-text);background:var(--err-bg);border-color:var(--err-border)}
.badge.gray{color:var(--gray-text);background:var(--gray-bg);border-color:var(--gray-border)}
.badge.brand{color:var(--brand-text);background:var(--brand-bg);border-color:var(--brand-border)}
.alert{border:1px solid;border-radius:12px;padding:16px 20px;display:flex;flex-direction:column;gap:8px;margin-bottom:16px}
.alert.err{background:var(--err-bg);border-color:var(--err-border)}
.alert.warn{background:var(--warn-bg);border-color:var(--warn-border)}
.alert.info{background:var(--brand-bg);border-color:var(--brand-border)}
.alert .t{font:600 14px/20px 'Inter',sans-serif;color:var(--text)}
.alert.err .t{color:var(--err-text)}.alert.warn .t{color:var(--warn-text)}.alert.info .t{color:var(--brand-text)}
.alert p{margin:0;font-size:14px;line-height:21px;color:var(--text-2)}
.alert ol{margin:0;padding-left:20px;font-size:14px;line-height:21px;color:var(--text-2);display:flex;flex-direction:column;gap:8px}
.seg{display:inline-flex;border:1px solid var(--border);border-radius:8px;background:var(--panel);box-shadow:var(--shadow-xs);overflow:hidden}
.seg button{appearance:none;border:0;background:transparent;font:500 13px/20px 'Inter',sans-serif;color:var(--text-3);padding:6px 12px;cursor:pointer;border-right:1px solid var(--border);transition:background .15s}
.seg button:last-child{border-right:0}
.seg button:hover{background:var(--panel-2)}
.seg button[aria-pressed="true"]{background:var(--panel-3);color:var(--text)}
.seg button:focus-visible{outline:none;box-shadow:var(--focus);position:relative;z-index:1}
.empty{padding:20px;color:var(--text-4);font-size:14px}
.kv{display:grid;grid-template-columns:140px 1fr;gap:8px 16px;font-size:14px;line-height:21px;padding:16px 20px;border-top:1px solid var(--border)}
.kv dt{color:var(--text-4);font-weight:500}.kv dd{margin:0;color:var(--text-2)}
@media (max-width:640px){.kv{grid-template-columns:1fr;gap:2px 0}.kv dt{margin-top:8px}.kv dt:first-child{margin-top:0}}
.tof{padding:12px 20px;border-bottom:1px solid var(--border);font-size:14px;color:var(--text-3)}
.meeting{padding:0}
.meeting + .meeting{border-top:1px solid var(--border)}
.meeting summary{list-style:none;cursor:pointer;display:flex;gap:12px;align-items:flex-start;padding:16px 20px;transition:background .15s}
.meeting summary::-webkit-details-marker{display:none}
.meeting summary:hover{background:var(--panel-2)}
.meeting summary:focus-visible{outline:none;box-shadow:inset var(--focus)}
.meeting .chev{flex:none;width:8px;height:8px;margin-top:8px;border-right:1.5px solid var(--text-4);border-bottom:1.5px solid var(--text-4);transform:rotate(-45deg);transition:transform .15s}
.meeting[open] .chev{transform:rotate(45deg)}
.meeting .mtxt{display:flex;flex-direction:column;gap:2px;min-width:0}
.meeting .mtitle{font:600 16px/24px 'Inter',sans-serif;color:var(--text)}
.meeting .when{font-size:13px;line-height:18px;color:var(--text-4)}
.meeting .mlead{font-size:14px;line-height:21px;color:var(--text-3);margin-top:4px;max-width:80ch}
.meeting .mbody{padding:0 20px 20px 40px}
.meeting p{margin:0 0 8px;font-size:14px;line-height:21px;color:var(--text-2);max-width:80ch}
.meeting .lbl{font:600 13px/18px 'Inter',sans-serif;color:var(--text);margin:12px 0 4px}
.meeting ul{margin:0;padding-left:20px;font-size:14px;line-height:21px;color:var(--text-2);max-width:80ch}
.meeting li{margin-bottom:4px}
.foot{border-top:1px solid var(--border);padding-top:20px;color:var(--text-4);font-size:13px;line-height:19px}
.foot ul{margin:0 0 12px;padding-left:18px}.foot li{margin-bottom:4px}
.foot p{margin:0}
.client-list{font-size:13px;line-height:19px;color:var(--text-3)}
@media (prefers-reduced-motion: reduce){*{transition:none!important}}
"""

JS = """
document.querySelectorAll('[data-filter-for]').forEach(seg=>{
  const tbl=document.getElementById(seg.dataset.filterFor);
  const rows=[...tbl.querySelectorAll('tbody tr')];
  const empty=tbl.parentElement.querySelector('.empty');
  seg.querySelectorAll('button').forEach(b=>b.addEventListener('click',()=>{
    seg.querySelectorAll('button').forEach(x=>x.setAttribute('aria-pressed',x===b?'true':'false'));
    const f=b.dataset.flag; let n=0;
    rows.forEach(r=>{const show=f==='all'||r.dataset.flag===f; r.hidden=!show; if(show)n++;});
    if(empty) empty.hidden=n>0;
  }));
});
"""

FLAG = {"✅":("ok","Match"),"⚠️":("warn","Warning"),"❌":("err","Critical"),"🔴":("gray","Blocked")}
STATE = {"Scale w/ HG AI":"brand","Healthy":"ok","Monitor":"gray","Review w/ HG AI":"warn","Flag to Shawal":"err","Under gate":"gray"}
STATE_KEY = {"Scale w/ HG AI":"scale","Healthy":"healthy","Monitor":"monitor","Review w/ HG AI":"review","Flag to Shawal":"flag","Under gate":"gate"}

def esc(s): return html.escape(s, quote=False)
def inline(s):
    s = esc(s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = s.replace("❌ and 🔴","critical and blocked").replace("(❌ and 🔴)","").replace("(⚠️)","")
    for k in FLAG: s = s.replace(k, "")
    return s.strip()
def badge(kind, label): return f'<span class="badge {kind}"><span class="dot {kind}"></span>{esc(label)}</span>'
def flag_badge(sym):
    k,l = FLAG.get(sym.strip(), ("gray", sym.strip())); return badge(k,l)
def state_badge(st): return badge(STATE.get(st,"gray"), st)

# ---------------- md parsing ----------------
def sections(md):
    out=collections.OrderedDict(); cur="_pre"; out[cur]=[]
    for line in md.splitlines():
        if line.startswith("## "): cur=line[3:].strip(); out[cur]=[]
        else: out[cur].append(line)
    return out
def tables(lines):
    """return list of tables, each list of rows (list of cells); first row header"""
    tbls=[]; cur=[]
    for l in lines+[""]:
        if l.strip().startswith("|"):
            cells=[c.strip() for c in l.strip().strip("|").split("|")]
            if all(re.fullmatch(r":?-+:?",c) for c in cells): continue
            cur.append(cells)
        else:
            if cur: tbls.append(cur); cur=[]
    return tbls
def paras(lines):
    ps=[]; cur=[]
    for l in lines+[""]:
        if l.strip() and not l.strip().startswith("|") and not l.startswith("#"):
            if re.match(r"^\d+\. ", l.strip()) and cur: ps.append(" ".join(cur)); cur=[]
            cur.append(l.strip())
        else:
            if cur: ps.append(" ".join(cur)); cur=[]
    return ps
def bullets(lines): return [l.strip()[2:] for l in lines if l.strip().startswith("- ")]

def render_table(tid, header, rows, kinds, flag_col=None, flag_map=None, first_col=True):
    """kinds: list per column of 'first','num','mono','notes','domains','badge','text','nowrap'"""
    th="".join(f'<th{" class=num" if k=="num" else ""}>{esc(h)}</th>' for h,k in zip(header,kinds))
    trs=[]
    for r in rows:
        r = r + [""]*(len(header)-len(r))
        attrs=""
        if flag_col is not None:
            attrs=f' data-flag="{flag_map(r[flag_col])}"'
        tds=[]
        for i,(c,k) in enumerate(zip(r,kinds)):
            if k=="badge": tds.append(f"<td class=nowrap>{flag_badge(c) if flag_map is not flag_state else state_badge(c)}</td>")
            elif k=="first": tds.append(f"<td class=first>{inline(c)}</td>")
            elif k=="num" and "⚠️" in c:
                fc=" ".join(c.replace("⚠️"," ").split()); tds.append(f"<td class=num>{badge('warn', fc)}</td>")
            elif k=="num": tds.append(f"<td class=num>{inline(c)}</td>")
            elif k=="mono": tds.append(f"<td class=mono>{inline(c)}</td>")
            elif k=="notes": tds.append(f"<td class=notes>{inline(c)}</td>")
            elif k=="domains": tds.append(f"<td class=domains>{inline(c).replace(', ',', <wbr>')}</td>")
            elif k=="nowrap": tds.append(f"<td class=nowrap>{inline(c)}</td>")
            else: tds.append(f"<td>{inline(c)}</td>")
        trs.append(f"<tr{attrs}>{''.join(tds)}</tr>")
    return f'<div class="tablewrap"><table id="{tid}"><thead><tr>{th}</tr></thead><tbody>{"".join(trs)}</tbody></table><div class="empty" hidden>No rows match this filter.</div></div>'

def flag_sym(c): return FLAG.get(c.strip(),("gray",))[0]
def flag_state(c): return STATE_KEY.get(c.strip(),"gray")

def seg(tid, options):
    btns="".join(f'<button type="button" data-flag="{v}" aria-pressed="{"true" if i==0 else "false"}">{esc(l)}</button>' for i,(v,l) in enumerate(options))
    return f'<div class="seg" role="group" aria-label="Filter rows" data-filter-for="{tid}">{btns}</div>'

def stat(label, value, hint="", dot=None):
    d=f'<span class="dot {dot}"></span>' if dot else ""
    return f'<div class="stat"><div class="label">{d}{esc(label)}</div><div class="value">{esc(value)}</div>{f"<div class=hint>{inline(hint)}</div>" if hint else ""}</div>'

def page(title, eyebrow, h1, lede, chips, body):
    chips_html="".join(f'<span class="chip">{c}</span>' for c in chips)
    return f"""<title>{esc(title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Roboto+Mono:wght@400;500&display=swap">
<style>{CSS}</style>
<div class="page">
<div class="masthead">{wordmark}<div class="eyebrow">{esc(eyebrow)}</div></div>
<header class="title"><h1>{esc(h1)}</h1><p class="lede">{lede}</p><div class="meta">{chips_html}</div></header>
{body}
</div>
<script>{JS}</script>
"""

def footer(bullets_, extra=""):
    lis="".join(f"<li>{inline(b)}</li>" for b in bullets_)
    return f'<div class="foot"><ul>{lis}</ul>{extra}<p>HiddenGem Marketing · weekly Meta Ads review · generated {RUN} from the saved report and CSV sidecar.</p></div>'

def fixed_html(S, kinds=None):
    """'Fixed since last week' is a paragraph on a first run and a table afterwards."""
    lines=S.get("Fixed since last week",[]); t=tables(lines)
    if t and len(t[0])>1:
        k=kinds or (["first"]+["text"]*(len(t[0][0])-2)+["notes"])
        return render_table("fixed",t[0][0],t[0][1:],k)
    ps=paras(lines)
    return f'<div class="card-body" style="color:var(--text-3);font-size:14px">{inline(ps[0]) if ps else "None."}</div>'
def compare_chip(S):
    for b in bullets(S.get("Footer",[])):
        if b.startswith("Previous report"):
            m=re.match(r"Previous report[^:]*:\s*([^\s.]+(?:\.[a-z]{3})?)",b)
            return f"Compared against {m.group(1)}" if m else re.split(r"\. ",b)[0]
    return "First run, no prior report"
def run_line(S):
    for p_ in paras(S.get("_pre",[])):
        if p_.startswith("Run:"): return p_
    return ""

# =====================================================================
# 1. AD SPEND CHECK
# =====================================================================
def build_spend():
    md=open(f"{ROOT}/Ad Spends Checks/Weekly Checks/{DATE}-ad-spend-check.md",encoding="utf-8").read()
    S=sections(md)
    rows=list(csv.DictReader(open(f"{ROOT}/Ad Spends Checks/Weekly Checks/{DATE}-ad-spend-check.csv",encoding="utf-8")))
    cnt=collections.Counter(r["flag"] for r in rows)
    live=[r for r in rows if r["sheet_status"]=="Live"]
    documented=sum(float(r["sheet_daily_budget"] or 0) for r in live)
    liveread=[r for r in rows if r["source"]=="live"]
    confirmed=sum(float(r["actual_daily_budget"] or 0) for r in liveread)
    doc_same=sum(float(r["sheet_daily_budget"] or 0) for r in liveread)
    all_actual=sum(float(r["actual_daily_budget"] or 0) for r in rows)
    n_csv=sum(1 for r in rows if r["source"]=="csv")
    stats=(stat("Clients on sheet",str(len(rows)),f"{len(live)} live, {len(rows)-len(live)} not live or paused")
        +stat("Live connector reads",str(len(liveread)),f"{n_csv} scored from the CSV export, {cnt.get('blocker',0)} blocked")
        +stat("Documented live $/day",f"${documented:,.0f}","Master sheet, Live rows")
        +stat("Confirmed live $/day",f"${confirmed:,.0f}",f"vs ${doc_same:,.0f} documented for the same {len(liveread)} accounts")
        +stat("Critical",str(cnt["critical"]),"over 25% off or spend on a dark account",dot="err")
        +stat("Warning",str(cnt["warning"]),"10 to 25% off, or a sheet note that changes the figure",dot="warn")
        +stat("Match",str(cnt["match"]),"within 10% or $5",dot="ok")
        +stat("Blocked",str(cnt.get("blocker",0)),"account unreadable by the connector and absent from the export",dot="gray"))
    issues=tables(S["Issues, action needed"])[0]
    it=render_table("issues",["Client","AM","Flag","Sheet $/day","Actual $/day","Status vs last week","Next action"],issues[1:],
        ["first","text","badge","num","num","nowrap","notes"],flag_col=2,flag_map=flag_sym)
    allrows=tables(S["All accounts"])[0]
    at=render_table("all",["Client","AM","Sheet status","Sheet $/day","Actual $/day","Match","Notes and issues"],allrows[1:],
        ["first","text","nowrap","num","num","badge","notes"],flag_col=5,flag_map=flag_sym)
    fixed_block=fixed_html(S)
    notsheet=paras(S["Not on the sheet"])
    body=f"""
<div class="stats">{stats}</div>
<section>
  <div class="sec-head"><div><h2>Issues, action needed</h2><p class="sec-desc">Critical rows first, then warnings. Each row carries a next action written for the account manager.</p></div></div>
  <div class="card">{it}</div>
</section>
<section>
  <div class="sec-head"><div><h2>Fixed since last week</h2></div></div>
  <div class="card">{fixed_block}</div>
</section>
<section>
  <div class="sec-head"><div><h2>All accounts</h2><p class="sec-desc">Every client on the Master sheet, alphabetical. {n_csv} accounts the connector cannot read are scored from the Ads Manager export; the source is named in the row.</p></div>{seg("all",[("all","All"),("err","Critical"),("warn","Warning"),("ok","Match")])}</div>
  <div class="card">{at}</div>
</section>
<section>
  <div class="alert warn"><div class="t">Active accounts with spend and no Master sheet row</div><p>{inline(notsheet[0])}</p></div>
</section>
{footer(bullets(S["Footer"]))}
"""
    lede="Compares the documented daily budget on the Master Meta Ads sheet against the live daily budget in each client's ad account. Every client on the sheet is checked, including Not Live and Paused."
    rl=run_line(S); m1=re.search(r"live reads ([^,)]+)",rl); m2=re.search(r"CSV export (\d{4}-\d{2}-\d{2}) to (\d{4}-\d{2}-\d{2}) for (\d+) blocked accounts",rl)
    chips=[f"Run {RUN}"]+([f"Live reads {m1.group(1).replace('–',' to ')}"] if m1 else [])+([f"CSV export {m2.group(1)} to {m2.group(2)} for {m2.group(3)} blocked accounts"] if m2 else [])+[compare_chip(S)]
    return page(f"Ad spend check {WEEK}","Weekly Meta Ads review · Ad spend check","Ad spend check",lede,[esc(c) for c in chips],body)

# =====================================================================
# 2. PIXEL DOMAIN CHECK
# =====================================================================
def build_pixel():
    md=open(f"{ROOT}/Meta Pixel Reviews/Weekly Checks/{DATE}-pixel-domain-check.md",encoding="utf-8").read()
    S=sections(md)
    rows=list(csv.DictReader(open(f"{ROOT}/Meta Pixel Reviews/Weekly Checks/{DATE}-pixel-domain-check.csv",encoding="utf-8")))
    cnt=collections.Counter(r["flag"] for r in rows)
    distinct={r["pixel_id"] for r in rows}
    seen=set(); tot=0
    for r in rows:
        if r["pixel_id"] in seen: continue
        seen.add(r["pixel_id"]); tot+=int(r["events_7d"] or 0)
    stats=(stat("Clients on sheet","42","all matched to at least one pixel")
        +stat("Pixel rows reviewed",str(len(rows)),f"{len(distinct)} distinct pixels; Starlight Haven's serves two accounts")
        +stat("Events, last 7 days",f"{tot:,}","shared pixel counted once")
        +stat("Critical",str(cnt["critical"]),"another client's domain firing into the pixel",dot="err")
        +stat("Warning",str(cnt["warning"]),"silent, split, duplicate or unconfirmed",dot="warn")
        +stat("Match",str(cnt["match"]),"events only from the client's own hosts",dot="ok")
        +stat("Blocked",str(cnt.get("blocker",0)),"no pixel found or unreadable",dot="gray"))
    crit_lines=S["Critical issues (❌ and 🔴)"]
    crit_paras=paras(crit_lines)
    # first para is the bold intro, then numbered items, then effect
    intro=crit_paras[0]; items=[p for p in crit_paras if re.match(r"^\d\. ",p)]; effect=[p for p in crit_paras[1:] if not re.match(r"^\d\. ",p)]
    NUM=re.compile(r"^\d\. ")
    items_html="".join(f"<li>{inline(NUM.sub('',p))}</li>" for p in items)
    crit_alert=f'<div class="alert err"><div class="t">{inline(intro).replace("<strong>","").replace("</strong>","")}</div><ol>{items_html}</ol>{"".join(f"<p>{inline(p)}</p>" for p in effect)}</div>'
    hdr=["Client","Pixel name","Pixel ID","Events (7d)","Domains seen","Expected domain(s)","Match","Notes and issues"]
    kinds=["first","text","mono","num","domains","domains","badge","notes"]
    ct=render_table("crit",hdr,tables(crit_lines)[0][1:],kinds,flag_col=6,flag_map=flag_sym)
    wt=render_table("warn",hdr,tables(S["Warnings (⚠️)"])[0][1:],kinds,flag_col=6,flag_map=flag_sym)
    at=render_table("all",hdr,tables(S["All pixels (alphabetical by client)"])[0][1:],kinds,flag_col=6,flag_map=flag_sym)
    fixed_block=fixed_html(S)
    body=f"""
<div class="stats">{stats}</div>
<section>
  <div class="sec-head"><div><h2>Critical issues</h2><p class="sec-desc">Cross-contamination: a host that belongs to another sheet client firing into this pixel, at any volume.</p></div></div>
  {crit_alert}
  <div class="card">{ct}</div>
</section>
<section>
  <div class="sec-head"><div><h2>Warnings</h2><p class="sec-desc">Silent or low-volume pixels, funnels split across two pixels, double counting, pixels not shared to the ad account, and expected domains that still need confirming.</p></div></div>
  <div class="card">{wt}</div>
</section>
<section>
  <div class="sec-head"><div><h2>Fixed since last week</h2></div></div>
  <div class="card">{fixed_block}</div>
</section>
<section>
  <div class="sec-head"><div><h2>All pixels</h2><p class="sec-desc">Alphabetical by client. Domains come from the pixel's own 7-day host breakdown in Meta; expected domains are from the expected-domains file, inferred from the brand name unless marked otherwise.</p></div>{seg("all",[("all","All"),("err","Critical"),("warn","Warning"),("ok","Match")])}</div>
  <div class="card">{at}</div>
</section>
{footer(bullets(S["Footer"]))}
"""
    lede="Verifies each client's Meta Pixel receives events only from that client's own site, link pages, GoHighLevel funnel and booking engine, and flags cross-contamination, silent pixels and split or duplicate setups."
    chips=[f"Run {RUN}","Rolling 7-day window","Sources: HiddenGem BM dataset listing, per-account listings, host and event totals",compare_chip(S)]
    return page(f"Pixel domain check {WEEK}","Weekly Meta Ads review · Pixel domain check","Pixel domain check",lede,[esc(c) for c in chips],body)

# =====================================================================
# 3. CLIENT BENCHMARK
# =====================================================================
def build_bench():
    md=open(f"{ROOT}/Client Benchmark Reviews (advanced setups)/Weekly Checks/{DATE}-client-benchmark.md",encoding="utf-8").read()
    S=sections(md)
    rows=list(csv.DictReader(open(f"{ROOT}/Client Benchmark Reviews (advanced setups)/Weekly Checks/{DATE}-client-benchmark.csv",encoding="utf-8")))
    cnt=collections.Counter(r["state"] for r in rows)
    clients={r["client"] for r in rows}
    scored=sum(1 for r in rows if r["state"]!="Under gate")
    ct0=tables(S["_pre"]); hdrv=dict(zip(ct0[0][0],ct0[0][1])) if ct0 and len(ct0[0])>1 else {}
    stats=(stat("Advanced clients",hdrv.get("Advanced clients","—"),f"{hdrv.get('Live reads','—')} live reads, {hdrv.get('From CSV','—')} from the CSV export")
        +stat("Campaigns scored",str(scored),f"{cnt['Under gate']} more listed under the spend gate")
        +stat("Flag to Shawal",str(cnt["Flag to Shawal"]),"CPL $2.50+ or no leads; ROAS under 2x or no purchases",dot="err")
        +stat("Review w/ HG AI",str(cnt["Review w/ HG AI"]),"CPL $1.00 to 2.50; ROAS 2 to 5x",dot="warn")
        +stat("Monitor",str(cnt["Monitor"]),"CPL $0.50 to 1.00; ROAS 5 to 8x",dot="gray")
        +stat("Healthy",str(cnt["Healthy"]),"CPL $0.30 to 0.50; ROAS 8 to 15x",dot="ok")
        +stat("Scale w/ HG AI",str(cnt["Scale w/ HG AI"]),"CPL under $0.30; ROAS above 15x",dot="brand")
        +stat("Frequency over 5",str(sum(1 for r in rows if r.get("freq_flag")=="yes")),"Sales/Retargeting campaigns to refresh creative on; state unchanged",dot="warn"))
    # meetings
    mkey=[k for k in S if k.startswith("Weekly Meta Ads meetings")][0]
    mlines=S[mkey]; meetings=[]; cur=None
    for l in mlines:
        if l.startswith("### "):
            cur={"head":l[4:].strip(),"lines":[]}; meetings.append(cur)
        elif cur is not None: cur["lines"].append(l)
    mhtml=[]
    for m in meetings:
        parts=[p.strip() for p in m["head"].split(" — ")]
        title,date=parts[0],parts[1]; doc=re.sub(r"[`doc ]","",parts[2]) if len(parts)>2 else ""
        ls=m["lines"]; summ=[]; dec=[]; nxt=[]; mode="s"
        for l in ls:
            t=l.strip()
            if not t: continue
            if t=="Decisions:": mode="d"; continue
            if t=="Next steps:": mode="n"; continue
            if mode=="s": summ.append(t)
            elif mode=="d" and t.startswith("- "): dec.append(t[2:])
            elif mode=="n" and t.startswith("- "): nxt.append(t[2:])
        sp="".join(f"<p>{inline(p)}</p>" for p in summ)
        dh=f'<div class="lbl">Decisions</div><ul>{"".join(f"<li>{inline(d)}</li>" for d in dec)}</ul>' if dec else ""
        nh=f'<div class="lbl">Next steps</div><ul>{"".join(f"<li>{inline(d)}</li>" for d in nxt)}</ul>' if nxt else ""
        lead = inline(summ[0]) if summ else ""
        rest = "".join(f"<p>{inline(p)}</p>" for p in summ[1:])
        mhtml.append(f'<details class="meeting"><summary><span class="chev" aria-hidden="true"></span><span class="mtxt"><span class="mtitle">{esc(title)}</span><span class="when">{esc(date)} · Notes by Gemini · doc <span class="mono">{esc(doc)}</span></span>{f"<span class=mlead>{lead}</span>" if lead else ""}</span></summary><div class="mbody">{rest}{dh}{nh}</div></details>')
    hdr=["Client","AM","Campaign","Type","Spend / window","Governing metric","State","Status vs last week"]
    kinds=["first","text","text","nowrap","num","num","badge","nowrap"]
    act=render_table("act",hdr,tables(S["Action needed"])[0][1:],kinds,flag_col=6,flag_map=flag_state)
    sc=render_table("scale",hdr,tables(S["Scale candidates"])[0][1:],kinds,flag_col=6,flag_map=flag_state)
    fkey=[k for k in S if k.startswith("Frequency watch")]
    fhdr=["Client","AM","Campaign","Type","Frequency","Spend / window","Governing metric","State"]
    fkinds=["first","text","text","nowrap","num","num","num","badge"]
    frows=[r for r in tables(S[fkey[0]])[0][1:] if r and r[0].strip()!="—"] if fkey and tables(S[fkey[0]]) else []
    fw=render_table("freq",fhdr,frows,fkinds,flag_col=7,flag_map=flag_state) if frows else '<div class="empty">No Sales or Retargeting campaign above a frequency of 5 this week.</div>'

    # per client
    pkey=[k for k in S if k.startswith("Per client")][0]
    plines=S[pkey]; clients_blocks=[]; cur=None
    for l in plines:
        if l.startswith("### "):
            cur={"head":l[4:].strip(),"lines":[]}; clients_blocks.append(cur)
        elif cur is not None: cur["lines"].append(l)
    chtml=[]
    chdr=["Campaign","Type","Window","Spend","Results","Governing metric","Frequency","State","Diagnostics vs investigate lines","Notes","Change vs last week"]
    ckinds=["first","nowrap","nowrap","num","num","num","num","badge","notes","notes","nowrap"]
    # reports before 2026-10-06 have no Frequency column
    old_chdr=chdr[:6]+chdr[7:]; old_ckinds=ckinds[:6]+ckinds[7:]
    for i,c in enumerate(clients_blocks):
        parts=[p.strip() for p in c["head"].split(" — ")]
        name=parts[0]; am=parts[1].replace("AM ",""); acct=parts[2].replace("account ",""); src=parts[3]
        m=re.match(r"(.*)\((\d+)\)$",acct); acct_name,acct_id=(m.group(1).strip(),m.group(2)) if m else (acct,"")
        src_badge=badge("ok","Live read") if src.startswith("live") else badge("warn","CSV export, provisional")
        ps=paras(c["lines"]); tbls=tables(c["lines"])
        tof=[p for p in ps if p.startswith("ToF")]; roi=[p for p in ps if p.startswith("Monthly ROI")]
        notes=[p for p in ps if p.startswith("Meeting notes")]; hg=[p for p in ps if p.startswith("HG AI notes")]
        nocamp=[p for p in ps if p.startswith("No Lead Gen") or p.startswith("No live Lead Gen")]
        pausedl=[p for p in ps if p.startswith("Paused in window")]
        tid=f"c{i}"
        if tbls and len(tbls[0][0])>=11: tbl=render_table(tid,chdr,tbls[0][1:],ckinds,flag_col=7,flag_map=flag_state)
        elif tbls: tbl=render_table(tid,old_chdr,tbls[0][1:],old_ckinds,flag_col=6,flag_map=flag_state)
        else: tbl=f'<div class="empty">{inline(nocamp[0]) if nocamp else "No scored campaigns."}</div>'
        def strip_lbl(p,lbl): return re.sub(r"^"+lbl+r"[^:]*:\s*","",p)
        MN=re.compile(r"^Meeting notes\s*")
        def fmt_note(n):
            n=MN.sub('',n).lstrip(':').strip()
            m=re.match(r"^\(([^)]*?) (\d{4}-\d{2}-\d{2})\):\s*(.*)$",n)
            return f"<strong>{esc(m.group(1))}, {esc(m.group(2))}.</strong> {inline(m.group(3))}" if m else inline(n)
        notes_html="".join(f"<dt>Meeting notes</dt><dd>{fmt_note(n)}</dd>" for n in notes) if notes else "<dt>Meeting notes</dt><dd>Not mentioned in this week's meetings.</dd>"
        PZ=re.compile(r"^Paused in window, not scored:\s*")
        paused_html="".join(f"<dt>Paused in window</dt><dd>{inline(PZ.sub('',pl))}</dd>" for pl in pausedl)
        kv=f"""<dl class="kv">
{paused_html}<dt>Monthly ROI</dt><dd>{inline(strip_lbl(roi[0],"Monthly ROI")) if roi else "—"}</dd>
{notes_html}
<dt>HG AI notes</dt><dd>{inline(strip_lbl(hg[0],"HG AI notes")[:1].upper()+strip_lbl(hg[0],"HG AI notes")[1:]) if hg else "—"}</dd>
</dl>"""
        chtml.append(f"""<div class="card" id="client-{i}">
<div class="card-head"><div><h3>{esc(name)}</h3><div class="sub">AM {esc(am)} · {esc(acct_name)} <span class="mono">{esc(acct_id)}</span></div></div>{src_badge}</div>
<div class="tof">{inline(tof[0]) if tof else ""}</div>
{tbl}
{kv}
</div>""")
    states_para=[p for p in paras(S["_pre"]) if p.startswith("States come from")]
    body=f"""
<div class="stats">{stats}</div>
<div class="alert info"><div class="t">How states are assigned</div><p>{inline(states_para[0]) if states_para else ""}</p></div>
<section>
  <div class="sec-head"><div><h2>Weekly Meta Ads meetings since last run</h2><p class="sec-desc">Notes by Gemini attached to the calendar events, read via Drive. Summary, decisions and next steps as Gemini wrote them; client-specific sentences are pulled into each client's card below. Transcript not used.</p></div></div>
  <div class="card">{"".join(mhtml)}</div>
</section>
<section>
  <div class="sec-head"><div><h2>Action needed</h2><p class="sec-desc">Sales and Retargeting campaigns first, then Lead Gen. Within each, Flag to Shawal before Review w/ HG AI, highest spend first.</p></div></div>
  <div class="card">{act}</div>
</section>
<section>
  <div class="sec-head"><div><h2>Scale candidates</h2><p class="sec-desc">Campaigns above the Scale line. Full context goes to HG AI, which picks where budget goes.</p></div></div>
  <div class="card">{sc}</div>
</section>
<section>
  <div class="sec-head"><div><h2>Frequency watch</h2><p class="sec-desc">Sales, Retargeting and MoF-lookalike campaigns whose 14-day frequency is above 5.0. Frequency does not change the ROAS state; this is the list to refresh creative or widen the audience on.</p></div></div>
  <div class="card">{fw}</div>
</section>
<section>
  <div class="sec-head"><div><h2>Per client</h2><p class="sec-desc">Ordered by scored MoF and BoF spend, highest first. ToF spend is shown for context and not scored.</p></div></div>
  {"".join(chtml)}
</section>
{footer(bullets(S["Footer"]))}
"""
    lede="Scores every Lead Gen (MoF) and Sales or Retargeting (BoF) campaign of each CRM-Advanced client against the Benchmarks doc decision table, with monthly ROI context and this week's meeting notes."
    rl=run_line(S); m2=re.search(r"CSV export (\d{4}-\d{2}-\d{2}) to (\d{4}-\d{2}-\d{2}) for the (\d+) accounts",rl)
    chips=[f"Run {RUN}","Lead Gen: 30-day window, $100 gate","Sales/Retargeting: 14-day window, $200 gate"]+([f"CSV export {m2.group(1)} to {m2.group(2)} for {m2.group(3)} accounts"] if m2 else [])+[compare_chip(S)]
    return page(f"Client benchmark {WEEK}","Weekly Meta Ads review · Client benchmark, advanced setups","Client benchmark review",lede,[esc(c) for c in chips],body)

if __name__ == "__main__":
    outs={
     f"{ROOT}/Ad Spends Checks/Weekly Checks/{DATE}-ad-spend-check.html": build_spend,
     f"{ROOT}/Meta Pixel Reviews/Weekly Checks/{DATE}-pixel-domain-check.html": build_pixel,
     f"{ROOT}/Client Benchmark Reviews (advanced setups)/Weekly Checks/{DATE}-client-benchmark.html": build_bench,
    }
    for p,fn in outs.items():
        h=fn(); open(p,"w",encoding="utf-8").write(h); print(p, len(h))
