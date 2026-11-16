"""HTML report builder for the three weekly Meta Ads reviews.
Styled from the HiddenGem Media design system (claude.ai/artifact/GXb4YMfP8uFmoTPhnWujSk, tokens.json; its generated
tokens.css is stale): Inter + Roboto Mono, white / #0A0A0A canvas, gem yellow #FFD60A fills with gold text
(#8A7100 light, #FFD935 dark), semantic badges, no emoji. Blue #0066DE was retired by the design system on 2026-10-22.
Each page is published as a claude.ai artifact; republish to the same URL (see PROJECT.md section 4.4).
"""
import csv, re, html, collections, os, json
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
  --bg:#ffffff; --panel:#ffffff; --panel-2:#fafafa; --panel-3:#f5f5f5;
  --border:#e5e5e5; --border-strong:#d4d4d4;
  --text:#171717; --text-2:#404040; --text-3:#525252; --text-4:#737373;
  --brand:#ffd60a; --brand-hover:#e0ba00; --on-brand:#0a0a0a; --brand-ring:#b89800;
  --brand-text:#8a7100; --brand-bg:#fffceb; --brand-border:#8a7100;
  --ok-text:#008138; --ok-dot:#00a544; --ok-bg:#f0fdf4; --ok-border:#dcfce7;
  --warn-text:#a36100; --warn-dot:#cd8900; --warn-bg:#fefce8; --warn-border:#fef9c2;
  --err-text:#bf000f; --err-dot:#e40014; --err-bg:#fef2f2; --err-border:#ffe2e2;
  --gray-text:#404040; --gray-dot:#a1a1a1; --gray-bg:#f5f5f5; --gray-border:#e5e5e5;
  --shadow-xs:0 0 2px #0000001f,0 1px 2px #00000024;
  --elev:0 0 2px #0000001f,0 8px 16px #00000024;
  --focus:0 0 0 2px #ffffff,0 0 0 4px #8a7100;
  color-scheme:light;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){
  --bg:#0a0a0a; --panel:#171717; --panel-2:#262626; --panel-3:#262626;
  --border:#262626; --border-strong:#404040;
  --text:#fafafa; --text-2:#e5e5e5; --text-3:#d4d4d4; --text-4:#a1a1a1;
  --brand:#ffd60a; --brand-hover:#ffd935; --on-brand:#0a0a0a; --brand-ring:#ffd60a;
  --brand-text:#ffd935; --brand-bg:#3b3000; --brand-border:#ffd935;
  --ok-text:#05df72; --ok-dot:#00c758; --ok-bg:#032e15; --ok-border:rgba(0,199,88,.3);
  --warn-text:#fac800; --warn-dot:#edb200; --warn-bg:#432004; --warn-border:rgba(237,178,0,.3);
  --err-text:#ff6568; --err-dot:#fb2c36; --err-bg:#460809; --err-border:rgba(251,44,54,.35);
  --gray-text:#e5e5e5; --gray-dot:#737373; --gray-bg:#262626; --gray-border:#404040;
  --shadow-xs:0 0 2px #0000003d,0 1px 2px #00000047;
  --elev:0 0 2px #0000003d,0 8px 16px #00000047;
  --focus:0 0 0 2px #0a0a0a,0 0 0 4px #ffd935;
  color-scheme:dark;
}}
:root[data-theme="dark"]{
  --bg:#0a0a0a; --panel:#171717; --panel-2:#262626; --panel-3:#262626;
  --border:#262626; --border-strong:#404040;
  --text:#fafafa; --text-2:#e5e5e5; --text-3:#d4d4d4; --text-4:#a1a1a1;
  --brand:#ffd60a; --brand-hover:#ffd935; --on-brand:#0a0a0a; --brand-ring:#ffd60a;
  --brand-text:#ffd935; --brand-bg:#3b3000; --brand-border:#ffd935;
  --ok-text:#05df72; --ok-dot:#00c758; --ok-bg:#032e15; --ok-border:rgba(0,199,88,.3);
  --warn-text:#fac800; --warn-dot:#edb200; --warn-bg:#432004; --warn-border:rgba(237,178,0,.3);
  --err-text:#ff6568; --err-dot:#fb2c36; --err-bg:#460809; --err-border:rgba(251,44,54,.35);
  --gray-text:#e5e5e5; --gray-dot:#737373; --gray-bg:#262626; --gray-border:#404040;
  --shadow-xs:0 0 2px #0000003d,0 1px 2px #00000047;
  --elev:0 0 2px #0000003d,0 8px 16px #00000047;
  --focus:0 0 0 2px #0a0a0a,0 0 0 4px #ffd935;
  color-scheme:dark;
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--text);font:400 16px/24px 'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;-webkit-font-smoothing:antialiased}
.page{max-width:1200px;margin:0 auto;padding-block:32px 64px;padding-inline:32px}
@media (max-width:640px){.page{padding-inline:16px;padding-block:20px 48px}}
a{color:var(--brand-text);text-decoration:none}a:hover{text-decoration:underline}
code,.mono{font-family:'Roboto Mono',ui-monospace,'SF Mono',Menlo,monospace;font-size:.9em}
.wordmark{display:block;color:var(--text);height:22px;width:auto}
.masthead{display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap;padding-bottom:20px;border-bottom:1px solid var(--border);margin-bottom:28px}
.masthead .eyebrow{font:500 12px/18px 'Roboto Mono',ui-monospace,monospace;letter-spacing:.14em;text-transform:uppercase;color:var(--text-4)}
header.title{display:flex;flex-direction:column;gap:8px;margin-bottom:24px}
h1{font:600 36px/44px 'Inter',sans-serif;letter-spacing:-.02em;margin:0;text-wrap:balance}
@media (max-width:640px){h1{font-size:30px;line-height:38px}}
.lede{margin:0;color:var(--text-3);max-width:72ch}
.meta{display:flex;gap:8px;flex-wrap:wrap;margin-top:4px}
.chip{display:inline-flex;align-items:center;gap:6px;padding:2px 10px;border:1px solid var(--border);border-radius:9999px;background:var(--panel);font:500 12px/18px 'Inter',sans-serif;color:var(--text-3)}
.chip .mono{font-size:12px}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));grid-auto-rows:1fr;gap:12px;margin-bottom:32px}
.stats.cols-4{grid-template-columns:repeat(4,minmax(0,1fr))}
@media (max-width:640px){.stats,.stats.cols-4{grid-template-columns:repeat(2,minmax(0,1fr))}}
.stat{background:var(--panel);border:1px solid var(--border);border-radius:12px;padding:16px 18px;box-shadow:var(--shadow-xs);display:flex;flex-direction:column;gap:4px;min-width:0}
.stat .label{font:500 13px/18px 'Inter',sans-serif;color:var(--text-3);display:flex;align-items:center;gap:6px}
.stat .value{font:600 26px/32px 'Inter',sans-serif;letter-spacing:-.02em;font-variant-numeric:tabular-nums;white-space:nowrap}
.stat .hint{font:400 12px/18px 'Inter',sans-serif;color:var(--text-4)}
.dot{width:8px;height:8px;border-radius:9999px;display:inline-block;flex:none}
.dot.ok{background:var(--ok-dot)}.dot.warn{background:var(--warn-dot)}.dot.err{background:var(--err-dot)}.dot.gray{background:var(--gray-dot)}.dot.brand{background:var(--brand);box-shadow:inset 0 0 0 1px var(--brand-ring)}
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
.badge.brand{color:var(--on-brand);background:var(--brand);border-color:var(--brand-hover)}
.badge.brand .dot{background:var(--on-brand);box-shadow:none}
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
.month{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:0;border-bottom:1px solid var(--border);background:var(--panel-2)}
.month .stat{border:0;border-radius:0;box-shadow:none;background:transparent;padding:14px 20px}
.month .stat+.stat{border-left:1px solid var(--border)}
.month .stat .value{font-size:20px;line-height:28px}
.month .stat .value .delta{font-size:14px;font-weight:500;margin-left:6px}
.month .stat .value .delta.ok{color:var(--ok-text)}.month .stat .value .delta.err{color:var(--err-text)}.month .stat .value .delta.gray{color:var(--text-4)}
.month .none{padding:12px 20px;font-size:14px;color:var(--text-4);grid-column:1/-1}
@media (max-width:640px){.month .stat+.stat{border-left:0;border-top:1px solid var(--border)}}
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

# Client benchmark page only: layout pieces (filter bar, stat band, sections, toggles, client cards). Tokens are in CSS above.
BENCH_CSS = """
[hidden]{display:none!important}
td.first a,.ccard a{color:inherit}
td.first a:hover{color:var(--brand-text)}
a:focus-visible,button:focus-visible,summary:focus-visible,select:focus-visible{outline:none;box-shadow:var(--focus);border-radius:8px}
/* section openers: mono eyebrow in gold text, display-sm title */
.sec{margin:0 0 56px}
.sec-top{display:flex;align-items:flex-end;justify-content:space-between;gap:12px 16px;flex-wrap:wrap;margin:0 0 16px}
.eb{display:block;font:500 12px/18px 'Roboto Mono',ui-monospace,monospace;letter-spacing:.14em;text-transform:uppercase;color:var(--brand-text);margin:0 0 6px}
.sec-top h2{font:600 30px/38px 'Inter',sans-serif;letter-spacing:-.02em;margin:0;text-wrap:balance}
.sec-top .sec-desc{margin-top:6px}
@media (max-width:640px){.sec{margin-bottom:44px}.sec-top h2{font-size:24px;line-height:32px}}
/* stat band */
.band{display:grid;grid-template-columns:repeat(8,minmax(0,1fr));margin:0 0 48px}
.band .stat{border:0;border-radius:0;box-shadow:none;background:transparent;padding:14px 12px 14px 14px;gap:2px}
.band .stat .label{font-size:12px;line-height:18px;white-space:nowrap}
.band .stat+.stat{border-left:1px solid var(--border)}
.band .stat .value{font-size:24px;line-height:32px}
.band .stat .hint{font-size:12px;line-height:16px}
@media (max-width:1000px){.band{grid-template-columns:repeat(4,minmax(0,1fr))}.band .stat:nth-child(4n+1){border-left:0}.band .stat:nth-child(n+5){border-top:1px solid var(--border)}}
@media (max-width:640px){.band{grid-template-columns:repeat(2,minmax(0,1fr))}.band .stat+.stat{border-left:0}.band .stat:nth-child(even){border-left:1px solid var(--border)}.band .stat:nth-child(n+3){border-top:1px solid var(--border)}}
/* filter bar */
.fbar{position:sticky;top:12px;z-index:10;display:flex;flex-wrap:wrap;align-items:flex-end;gap:12px 16px;padding:14px 18px;margin:0 0 20px;background:var(--panel);border:1px solid var(--border);border-radius:12px;box-shadow:var(--elev)}
.fld{display:flex;flex-direction:column;gap:6px;min-width:0}
.fld label{font:500 14px/20px 'Inter',sans-serif;color:var(--text-2)}
.sel{position:relative;display:block}
.sel::after{content:"";position:absolute;right:15px;top:50%;width:7px;height:7px;border-right:1.5px solid var(--text-3);border-bottom:1.5px solid var(--text-3);transform:translateY(-70%) rotate(45deg);pointer-events:none}
.sel select{appearance:none;-webkit-appearance:none;width:100%;min-width:240px;height:40px;font:500 14px/20px 'Inter',sans-serif;color:var(--text);background:var(--panel);border:1px solid var(--border-strong);border-radius:8px;padding:0 38px 0 14px;cursor:pointer;box-shadow:var(--shadow-xs);transition:border-color .1s linear,background .1s linear}
.sel select:hover{border-color:var(--text-4)}
.sel select.on{border-color:var(--brand-border);background:var(--brand-bg);color:var(--brand-text)}
.btn{appearance:none;display:inline-flex;align-items:center;justify-content:center;gap:6px;height:40px;padding:0 16px;border:1px solid var(--border-strong);border-radius:8px;background:var(--panel);color:var(--text-2);font:600 14px/20px 'Inter',sans-serif;cursor:pointer;box-shadow:var(--shadow-xs);transition:background .1s linear,color .1s linear}
.btn:hover{background:var(--panel-2);color:var(--text)}
.btn.sm{height:36px;padding:0 14px}
.fsum{margin:0 0 0 auto;align-self:center;font-size:14px;line-height:20px;color:var(--text-3);text-align:right}
.fsum strong{color:var(--text);font-weight:600}
@media (max-width:640px){.fbar{position:static;padding:12px 14px}.fld{flex:1 1 100%}.sel select{min-width:0}.fsum{margin:0;width:100%;text-align:left}}
/* tables */
thead th{color:var(--text-3)}
tbody tr:hover td{background:var(--panel-2)}
td.camp{min-width:180px}
td.type{min-width:110px}
td.status{min-width:140px;font-size:13px;line-height:19px;color:var(--text-3)}
.tgl thead th,.tgl tbody td,#ovw thead th,#ovw tbody td{padding-left:12px;padding-right:12px}
.tgl thead th:first-child,.tgl tbody td:first-child,#ovw thead th:first-child,#ovw tbody td:first-child{padding-left:20px}
.tgl thead th:last-child,.tgl tbody td:last-child,#ovw thead th:last-child,#ovw tbody td:last-child{padding-right:20px}
.tgl td.first,#ovw td.first{white-space:normal;min-width:130px}
#ovw td.sum{min-width:300px;color:var(--text-2)}
#ovw td.sum .clamp{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
#ovw td.st{white-space:nowrap}
#ovw td.spend{font-weight:600;color:var(--text)}
#ovw tr[data-href]{cursor:pointer}
#ovw tr.muted td{color:var(--text-4)}
#ovw tr.muted td.first{color:var(--text-3)}
#ovw tr.grp td,#ovw tr.grp:hover td{background:var(--panel-2);font:500 12px/18px 'Roboto Mono',ui-monospace,monospace;letter-spacing:.14em;text-transform:uppercase;color:var(--text-3);padding-top:8px;padding-bottom:8px}
.stl{display:flex;flex-wrap:wrap;gap:6px}
@media (max-width:640px){
  #ovw thead{display:none}
  #ovw,#ovw tbody{display:block}
  #ovw tbody tr{display:grid;grid-template-columns:minmax(0,1fr) auto;grid-template-areas:"name spend" "am am" "st st" "sum sum";gap:4px 12px;padding:14px 16px;border-bottom:1px solid var(--border)}
  #ovw tbody tr:last-child{border-bottom:0}
  #ovw tbody td{display:block;padding:0!important;border:0!important;min-width:0!important;background:transparent!important}
  #ovw td:nth-child(1){grid-area:name}#ovw td:nth-child(2){grid-area:am;font-size:13px;color:var(--text-4)}#ovw td:nth-child(2)::before{content:"AM "}
  #ovw td:nth-child(3){grid-area:sum;font-size:13px;line-height:19px}#ovw td:nth-child(4){grid-area:st;margin:4px 0 2px}#ovw td:nth-child(5){grid-area:spend}
  #ovw tbody tr.grp{display:block;padding:8px 16px;background:var(--panel-2)}
}
/* collapsible lists (section 2) and the notes toggle (section 4) */
.stack{display:flex;flex-direction:column;gap:12px}
.tgl>summary,.ccard>summary{list-style:none;cursor:pointer;transition:background .1s linear}
.tgl>summary::-webkit-details-marker,.ccard>summary::-webkit-details-marker{display:none}
.tgl>summary:hover,.ccard>summary:hover{background:var(--panel-2)}
.tgl>summary:focus-visible,.ccard>summary:focus-visible{box-shadow:inset var(--focus);border-radius:12px}
.tgl[open]>summary,.ccard[open]>summary{border-bottom:1px solid var(--border)}
.tgl .chev,.ccard .chev{flex:none;width:8px;height:8px;border-right:1.5px solid var(--text-3);border-bottom:1.5px solid var(--text-3);transform:rotate(-45deg);transition:transform .24s cubic-bezier(.2,0,0,1)}
.tgl[open]>summary .chev,.ccard[open]>summary .chev{transform:rotate(45deg)}
.tgl>summary{display:flex;gap:14px;align-items:flex-start;padding:18px 20px}
.tgl .chev{margin-top:9px}
.tgl .ttxt{display:flex;flex-direction:column;gap:4px;min-width:0;flex:1}
.tgl .trow{display:flex;align-items:center;gap:8px 12px;flex-wrap:wrap}
.tgl h3{font:600 20px/30px 'Inter',sans-serif;letter-spacing:-.01em;margin:0}
.tgl .tmeta{display:flex;align-items:center;gap:6px;flex-wrap:wrap}
.tgl .tcount{font-size:12px;line-height:18px;color:var(--text-4)}
.tgl .sec-desc{margin:0}
.tgl .tact{flex:none;margin-top:5px;font:600 14px/20px 'Inter',sans-serif;color:var(--brand-text)}
.tgl .tact::after{content:"Show"}
.tgl[open] .tact::after{content:"Hide"}
/* per-client cards (section 3) */
.cards{display:flex;flex-direction:column;gap:12px}
.cards>.card+.card{margin-top:0}
.cards>.card{scroll-margin-top:120px}
.ccard>summary{display:grid;grid-template-columns:8px minmax(0,1fr) auto auto;grid-template-areas:"chev main states spend";gap:6px 18px;align-items:center;padding:16px 20px}
.ccard .chev{grid-area:chev}
.ccard .cmain{grid-area:main;min-width:0}
.ccard .cstates{grid-area:states;display:flex;gap:6px;flex-wrap:wrap;justify-content:flex-end}
.ccard .cspend{grid-area:spend;text-align:right;min-width:92px;font:600 16px/24px 'Inter',sans-serif;font-variant-numeric:tabular-nums;color:var(--text)}
.ccard .cspend small{display:block;font:400 12px/16px 'Inter',sans-serif;color:var(--text-4)}
.ccard .cname{display:block;font:600 16px/24px 'Inter',sans-serif;color:var(--text)}
.ccard .csub{display:block;font-size:13px;line-height:18px;color:var(--text-4)}
@media (max-width:640px){.tgl>summary{padding:14px 16px}.tgl .tact{display:none}.ccard>summary{grid-template-columns:8px minmax(0,1fr) auto;grid-template-areas:"chev main spend" ". states states";padding:14px 16px}.ccard .cstates{justify-content:flex-start}}
/* client campaign table (inside each card) */
.ctable thead th,.ctable tbody td{padding-left:12px;padding-right:12px}
.ctable thead th:first-child,.ctable tbody td:first-child{padding-left:20px}
.ctable thead th:last-child,.ctable tbody td:last-child{padding-right:20px}
.ctable tbody td{border-bottom:0}
.ctable tbody+tbody tr:first-child td{border-top:1px solid var(--border)}
.ctable tbody:hover td{background:var(--panel-2)}
.ctable td.first{white-space:normal;min-width:190px}
.ctable td.res,.ctable td.gov{white-space:normal;min-width:92px}
.ctable tr.crow td{padding-bottom:8px}
.ctable tr.cdet td{padding-top:0;padding-bottom:14px}
.cdl{display:flex;flex-direction:column;gap:2px;font-size:13px;line-height:19px;color:var(--text-3);max-width:120ch}
.cdl p{margin:0}
.cdl span{font-weight:600;color:var(--text-2);margin-right:6px}
@media (max-width:640px){
  .ctable thead{display:none}
  .ctable,.ctable tbody,.ctable tr.cdet,.ctable tr.cdet td{display:block}
  .ctable tbody+tbody{border-top:1px solid var(--border)}
  .ctable tbody+tbody tr:first-child td{border-top:0}
  .ctable tr.crow{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:8px 12px;padding:14px 16px 8px}
  .ctable tr.crow td{display:block;padding:0!important;text-align:left;white-space:normal;min-width:0!important;background:transparent!important}
  .ctable tr.crow td.first{grid-column:1/-1}
  .ctable tr.crow td[data-l]::before{content:attr(data-l);display:block;font:400 11px/16px 'Inter',sans-serif;color:var(--text-4)}
  .ctable tr.cdet td{padding:0 16px 14px!important;background:transparent!important}
}
/* notes (section 4) */
.nbody{padding:20px;display:flex;flex-direction:column;gap:28px}
.nbody h4{font:600 16px/24px 'Inter',sans-serif;margin:0 0 4px}
.nbody .sec-desc{margin:0 0 12px}
.nbody p.np{margin:0;font-size:14px;line-height:21px;color:var(--text-2);max-width:90ch}
.nbody ul.nl{margin:0;padding-left:18px;font-size:14px;line-height:21px;color:var(--text-2);display:flex;flex-direction:column;gap:6px;max-width:100ch}
.mlist{border:1px solid var(--border);border-radius:8px;overflow:hidden}
.genline{margin:0;padding-top:20px;border-top:1px solid var(--border);color:var(--text-4);font-size:13px;line-height:19px}
@media (prefers-reduced-motion: reduce){.tgl .chev,.ccard .chev{transition:none}}
"""

# Client benchmark only: AM / client filter (stats, the three toggle tables, client cards; state kept in ?am=&client=)
# and remembered open/closed state of the toggle sections (per viewer, localStorage).
BENCH_JS = """
(function(){
  const bar=document.getElementById('fbar'), dataEl=document.getElementById('bench-data');
  if(!bar||!dataEl) return;
  const D=JSON.parse(dataEl.textContent);
  const ALL=D.clients.concat(D.unmapped);
  const amSel=document.getElementById('f-am'), clSel=document.getElementById('f-client');
  const clr=document.getElementById('f-clear'), sum=document.getElementById('f-sum'), xall=document.getElementById('x-all');
  const cards=[...document.querySelectorAll('.cards>details[data-client]')];
  const tables=[...document.querySelectorAll('table[data-ftable]')];
  const LBL=[['flag','err','Flag to Shawal'],['review','warn','Review w/ HG AI'],['monitor','gray','Monitor'],['healthy','ok','Healthy'],['scale','brand','Scale w/ HG AI']];
  const NOT_SCORED=s=>s==='Under gate'||s==='Tracked in Discovery'||s==='No promo data'||s.startsWith('Not scored');
  const ams=[...new Set(ALL.map(c=>c.a).filter(Boolean))].sort();
  const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
  const stats={};
  document.querySelectorAll('[data-stat]').forEach(el=>{const v=el.querySelector('.value'),h=el.querySelector('.hint');stats[el.dataset.stat]={v,h,v0:v.textContent,h0:h?h.innerHTML:''};});
  const badge=(k,t)=>'<span class="badge '+k+'"><span class="dot '+k+'"></span>'+t+'</span>';
  const plural=(n,w)=>n+' '+w+(n===1?'':'s');
  const esc=s=>s.replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  function fillClients(){
    const am=amSel.value, cur=clSel.value;
    while(clSel.children.length>1) clSel.removeChild(clSel.lastChild);
    [['With an ad account',D.clients],['Without an ad account',D.unmapped]].forEach(([label,list])=>{
      const l=list.filter(c=>am==='all'||c.a===am); if(!l.length) return;
      const g=document.createElement('optgroup'); g.label=label; l.forEach(c=>g.appendChild(new Option(c.n,c.n))); clSel.appendChild(g);
    });
    clSel.value=[...clSel.options].some(o=>o.value===cur)?cur:'all';
  }
  const match=(c,a)=>(amSel.value==='all'||a===amSel.value)&&(clSel.value==='all'||c===clSel.value);
  function meta(t,vis,tot,on){
    const box=document.querySelector('[data-meta-for="'+t.id+'"]'); if(!box) return;
    const unit=box.dataset.unit||'campaign'; let h='';
    if(box.dataset.meta==='states'){const c={};vis.forEach(r=>{c[r.dataset.flag]=(c[r.dataset.flag]||0)+1;});LBL.forEach(([k,kind,l])=>{if(c[k])h+=badge(kind,c[k]+' '+l);});}
    else if(vis.length) h=badge(box.dataset.kind||'gray',plural(vis.length,unit));
    if(!vis.length) h=badge('gray',on?'None for this filter':'None');
    if(on) h+='<span class="tcount">of '+plural(tot,unit)+' this week</span>';
    box.innerHTML=h;
  }
  function xlabel(){ if(!xall) return; const vis=cards.filter(c=>!c.hidden); xall.textContent=vis.length&&vis.every(c=>c.open)?'Collapse all':'Expand all'; }
  function apply(){
    const am=amSel.value, cl=clSel.value, on=am!=='all'||cl!=='all';
    amSel.classList.toggle('on',am!=='all'); clSel.classList.toggle('on',cl!=='all');
    tables.forEach(t=>{
      const rows=[...t.tBodies[0].rows].filter(r=>!r.hasAttribute('data-grp')), vis=rows.filter(r=>match(r.dataset.client,r.dataset.am));
      rows.forEach(r=>{r.hidden=!vis.includes(r);});
      t.querySelectorAll('tr[data-grp]').forEach(g=>{g.hidden=!vis.some(r=>r.hasAttribute('data-unmapped'));});
      t.hidden=!vis.length; const e=t.parentElement.querySelector('.empty'); if(e) e.hidden=!!vis.length;
      meta(t,vis,rows.length,on);
    });
    let nc=0; cards.forEach(c=>{const s=match(c.dataset.client,c.dataset.am); c.hidden=!s; if(s){nc++; if(cl!=='all') c.open=true;}});
    const nu=D.unmapped.filter(c=>match(c.n,c.a)).length;
    const R=D.rows.filter(r=>match(r[0],r[1])), n={};
    R.forEach(r=>{n[r[2]]=(n[r[2]]||0)+1;});
    const set=(k,v,h)=>{const s=stats[k]; if(!s) return; s.v.textContent=on?v:s.v0; if(s.h&&h!==undefined) s.h.innerHTML=on?h:s.h0;};
    set('clients',String(nc),'of '+D.clients.length+' with an ad account'+(nu?', +'+nu+' without':''));
    set('scored',String(R.filter(r=>!NOT_SCORED(r[2])).length),(n['Under gate']||0)+' under the spend gate');
    [['flag','Flag to Shawal'],['review','Review w/ HG AI'],['monitor','Monitor'],['healthy','Healthy'],['scale','Scale w/ HG AI']].forEach(([k,s])=>set(k,String(n[s]||0)));
    set('freq',String(R.filter(r=>r[3]).length));
    const who=[am!=='all'?esc(am):'',cl!=='all'?esc(cl):''].filter(Boolean).join(' · ');
    sum.innerHTML=on?'Showing <strong>'+plural(nc+nu,'client')+'</strong> of '+ALL.length+' · '+who:ALL.length+' Advanced clients across '+ams.length+' account managers';
    clr.hidden=!on; xlabel();
    try{const u=new URL(location.href);
      if(am==='all')u.searchParams.delete('am');else u.searchParams.set('am',am);
      if(cl==='all')u.searchParams.delete('client');else u.searchParams.set('client',cl);
      history.replaceState(null,'',u);}catch(e){}
  }
  amSel.addEventListener('change',()=>{fillClients();apply();});
  clSel.addEventListener('change',apply);
  clr.addEventListener('click',()=>{amSel.value='all';fillClients();clSel.value='all';apply();amSel.focus();});
  const q=new URLSearchParams(location.search);
  if(ams.includes(q.get('am'))) amSel.value=q.get('am');
  fillClients();
  if(ALL.some(c=>c.n===q.get('client'))) clSel.value=q.get('client');
  bar.hidden=false;
  apply();
  // a client name or overview row opens that client's card
  function openCard(id,scroll){
    const d=document.getElementById(id); if(!d) return;
    d.open=true; xlabel();
    if(scroll){ try{history.replaceState(null,'','#'+id);}catch(e){} d.scrollIntoView({behavior:reduce?'auto':'smooth',block:'start'}); d.querySelector('summary').focus({preventScroll:true}); }
  }
  document.addEventListener('click',e=>{
    const a=e.target.closest('a[href^="#client-"]');
    if(a){ e.preventDefault(); openCard(a.getAttribute('href').slice(1),true); return; }
    const tr=e.target.closest('tr[data-href]');
    if(tr && !window.getSelection().toString()) openCard(tr.dataset.href.slice(1),true);
  });
  if(/^#client-\\d+$/.test(location.hash)) openCard(location.hash.slice(1),true);
  cards.forEach(c=>c.addEventListener('toggle',xlabel));
  if(xall) xall.addEventListener('click',()=>{const vis=cards.filter(c=>!c.hidden), open=!vis.every(c=>c.open); vis.forEach(c=>{c.open=open;}); xlabel();});
  // section toggles: remember each viewer's open / closed choice
  document.querySelectorAll('details.tgl[id]').forEach(d=>{
    const key='bench.tgl.'+d.id;
    try{const v=localStorage.getItem(key); if(v==='open') d.open=true; else if(v==='closed') d.open=false;}catch(e){}
    d.addEventListener('toggle',()=>{try{localStorage.setItem(key,d.open?'open':'closed');}catch(e){}});
  });
})();
"""

FLAG = {"✅":("ok","Match"),"⚠️":("warn","Warning"),"❌":("err","Critical"),"🔴":("gray","Blocked")}
STATE = {"Scale w/ HG AI":"brand","Healthy":"ok","Monitor":"gray","Review w/ HG AI":"warn","Flag to Shawal":"err","Under gate":"gray","Tracked in Discovery":"gray","No promo data":"gray"}
STATE_KEY = {"Scale w/ HG AI":"scale","Healthy":"healthy","Monitor":"monitor","Review w/ HG AI":"review","Flag to Shawal":"flag","Under gate":"gate","Tracked in Discovery":"discovery","No promo data":"nodata"}

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

def render_table(tid, header, rows, kinds, flag_col=None, flag_map=None, first_col=True, badge_fn=None, row_attrs=None, first_href=None, table_attrs=""):
    """kinds: list per column of 'first','num','mono','notes','domains','badge','text','nowrap','camp','type','status'.
    row_attrs(row) -> extra <tr> attributes; first_href(cell) -> link target for the first column, or None."""
    th="".join(f'<th{" class=num" if k=="num" else ""}>{esc(h)}</th>' for h,k in zip(header,kinds))
    trs=[]
    for r in rows:
        r = r + [""]*(len(header)-len(r))
        attrs=""
        if flag_col is not None:
            attrs=f' data-flag="{flag_map(r[flag_col])}"'
        if row_attrs: attrs+=row_attrs(r)
        tds=[]
        for i,(c,k) in enumerate(zip(r,kinds)):
            if k=="badge": tds.append(f"<td class=nowrap>{badge_fn(c) if badge_fn else (flag_badge(c) if flag_map is not flag_state else state_badge(c))}</td>")
            elif k=="first":
                href=first_href(c) if first_href else None
                tds.append(f'<td class=first><a href="{href}">{inline(c)}</a></td>' if href else f"<td class=first>{inline(c)}</td>")
            elif k=="camp": tds.append(f"<td class=camp>{inline(c)}</td>")
            elif k=="type": tds.append(f"<td class=type>{inline(c)}</td>")
            elif k=="status": tds.append(f"<td class=status>{inline(c)}</td>")
            elif k=="num" and "⚠️" in c:
                fc=" ".join(c.replace("⚠️"," ").split()); tds.append(f"<td class=num>{badge('warn', fc)}</td>")
            elif k=="num": tds.append(f"<td class=num>{inline(c)}</td>")
            elif k=="mono": tds.append(f"<td class=mono>{inline(c)}</td>")
            elif k=="notes": tds.append(f"<td class=notes>{inline(c)}</td>")
            elif k=="domains": tds.append(f"<td class=domains>{inline(c).replace(', ',', <wbr>')}</td>")
            elif k=="nowrap": tds.append(f"<td class=nowrap>{inline(c)}</td>")
            else: tds.append(f"<td>{inline(c)}</td>")
        trs.append(f"<tr{attrs}>{''.join(tds)}</tr>")
    return f'<div class="tablewrap"><table id="{tid}"{table_attrs}><thead><tr>{th}</tr></thead><tbody>{"".join(trs)}</tbody></table><div class="empty" hidden>No rows match this filter.</div></div>'

def flag_sym(c): return FLAG.get(c.strip(),("gray",))[0]
def flag_state(c): return STATE_KEY.get(c.strip(),"gray")

def seg(tid, options):
    btns="".join(f'<button type="button" data-flag="{v}" aria-pressed="{"true" if i==0 else "false"}">{esc(l)}</button>' for i,(v,l) in enumerate(options))
    return f'<div class="seg" role="group" aria-label="Filter rows" data-filter-for="{tid}">{btns}</div>'

def stat(label, value, hint="", dot=None, key=None):
    d=f'<span class="dot {dot}"></span>' if dot else ""
    k=f' data-stat="{key}"' if key else ""
    return f'<div class="stat"{k}><div class="label">{d}{esc(label)}</div><div class="value">{esc(value)}</div>{f"<div class=hint>{inline(hint)}</div>" if hint else ""}</div>'

def page(title, eyebrow, h1, lede, chips, body, js="", css=""):
    chips_html="".join(f'<span class="chip">{c}</span>' for c in chips)
    return f"""<title>{esc(title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Roboto+Mono:wght@400;500&display=swap">
<style>{CSS}{css}</style>
<div class="page">
<div class="masthead">{wordmark}<div class="eyebrow">{esc(eyebrow)}</div></div>
<header class="title"><h1>{esc(h1)}</h1><p class="lede">{lede}</p><div class="meta">{chips_html}</div></header>
{body}
</div>
<script>{JS}{js}</script>
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
def build_spend_legacy(md, rows):
    """Pre-2026-10-15 format: documented sheet budget vs live, with Match / Warning / Critical flags."""
    S=sections(md)
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

# ---- 2026-10-15 onwards: live spend ledger, no sheet comparison ----
STATUS = {"up":("brand","Up"),"down":("warn","Down"),"new":("ok","New"),"same":("gray","Same"),"unchanged":("gray","Same"),
          "blocked":("err","Blocked"),"first run":("gray","First run"),"removed":("gray","Removed")}
def status_badge(c):
    k,l=STATUS.get(c.strip().lower(),("gray",c.strip())); return badge(k,l)
def status_group(c): return "same" if c.strip().lower() in ("same","unchanged","first run") else "changed"

def build_spend_v2(md, rows):
    S=sections(md)
    live=[r for r in rows if r["source"]=="live"]
    blocked=[r for r in rows if r["source"]!="live"]
    tot=lambda k: sum(float(r[k] or 0) for r in live)
    total=tot("total_live"); spent=tot("spend_7d")
    has_prev=any(r["prev_total"] for r in live)
    prev=sum(float(r["prev_total"] or 0) for r in live if r["prev_total"])
    cnt=collections.Counter(r["status"] for r in rows)
    if has_prev:
        d=total-prev; hint=f"vs ${prev:,.0f} last run ({'+' if d>=0 else '−'}${abs(d):,.0f})"
    else: hint="first run"
    changed=cnt["up"]+cnt["down"]+cnt["new"]
    stats=(stat("Clients checked",str(len(rows)),f"{len(live)} live reads, {len(blocked)} blocked")
        +stat("Total live $/day",f"${total:,.0f}",hint)
        +stat("Spent last 7 days",f"${spent:,.0f}",f"${spent/7:,.0f} per day across {len(live)} accounts")
        +stat("ToF Giveaway",f"${tot('tof_giveaway'):,.0f}","per day")
        +stat("MoF Leads",f"${tot('mof_leads'):,.0f}","per day")
        +stat("MoF Sales LoL",f"${tot('mof_sales_lol'):,.0f}","per day")
        +stat("BoF Sales",f"${tot('bof_sales'):,.0f}","per day")
        +(stat("Other",f"${tot('other'):,.0f}","per day") if tot("other") else "")
        +stat("Changed since last run",str(changed),f"{cnt['up']} up, {cnt['down']} down, {cnt['new']} new",dot="brand"))
    ch_lines=S.get("Changes since last week",[]); ch_t=tables(ch_lines)
    if ch_t and len(ch_t[0])>1:
        ch=render_table("changes",ch_t[0][0],ch_t[0][1:],["first","text","num","num","num","badge","notes"],flag_col=5,flag_map=status_group,badge_fn=status_badge)
    else:
        ps=paras(ch_lines); ch=f'<div class="card-body" style="color:var(--text-3);font-size:14px">{inline(ps[0]) if ps else "None."}</div>'
    led=tables(S["Live spend by client"])[0]
    lt=render_table("ledger",led[0],led[1:],["first","text","num","num","num","num","num","num","num","num","badge","notes"],flag_col=10,flag_map=status_group,badge_fn=status_badge)
    pre=paras(S["_pre"]); rl=run_line(S)
    m1=re.search(r"live reads ([^)]+?) through",rl)
    tab=next((p_ for p_ in pre if p_.startswith("Meta Ad Spends tab:")),"")
    chips=[f"Run {RUN}"]+([f"Live reads {m1.group(1).replace('–',' to ')}"] if m1 else [])+([tab.rstrip('.')] if tab else [])+[compare_chip(S)]
    body=f"""
<div class="stats">{stats}</div>
<section>
  <div class="sec-head"><div><h2>Changes since last run</h2><p class="sec-desc">Clients whose live daily budget moved, largest change first, with the campaigns behind it.</p></div></div>
  <div class="card">{ch}</div>
</section>
<section>
  <div class="sec-head"><div><h2>Live spend by client</h2><p class="sec-desc">Every client in the map, highest daily budget first. Spent 7d is the account's actual spend over the last 7 days.</p></div>{seg("ledger",[("all","All"),("changed","Changed"),("same","Unchanged")])}</div>
  <div class="card">{lt}</div>
</section>
{footer(bullets(S["Footer"]))}
"""
    lede="Live daily budget per client and per campaign type, read from each client's ad account through the Meta Marketing API, with the change since the previous run. The same rows are appended to the Meta Ad Spends tab of the Master Meta Ads sheet."
    return page(f"Ad spend check {WEEK}","Weekly Meta Ads review · Ad spend check","Ad spend check",lede,[esc(c) for c in chips],body)

def build_spend():
    md=open(f"{ROOT}/Ad Spends Checks/Weekly Checks/{DATE}-ad-spend-check.md",encoding="utf-8").read()
    rows=list(csv.DictReader(open(f"{ROOT}/Ad Spends Checks/Weekly Checks/{DATE}-ad-spend-check.csv",encoding="utf-8")))
    if rows and "total_live" in rows[0] and "status" in rows[0]: return build_spend_v2(md, rows)
    return build_spend_legacy(md, rows)

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
    m_cs=re.search(r"\*\*Clients on sheet:\*\*\s*(\d+)(?:\s*\((\d+) checked\))?",md)
    cs_n=m_cs.group(1) if m_cs else "42"; cs_sub=(f"{m_cs.group(2)} checked, offboarded excluded" if (m_cs and m_cs.group(2)) else "all matched to at least one pixel")
    stats=(stat("Clients on sheet",cs_n,cs_sub)
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
    # Reports up to 2026-10-26 have 8 columns; from 2026-10-30 a "Purchase (28d, browser / server)" column sits after Events (7d).
    hdr8=["Client","Pixel name","Pixel ID","Events (7d)","Domains seen","Expected domain(s)","Match","Notes and issues"]
    kinds8=["first","text","mono","num","domains","domains","badge","notes"]
    hdr9=hdr8[:4]+["Purchase (28d, b / s)"]+hdr8[4:]; kinds9=kinds8[:4]+["nowrap"]+kinds8[4:]
    def px_table(tid, lines):
        t=tables(lines)
        if not t: return '<div class="empty">None.</div>'
        nine=len(t[0][0])>=9
        return render_table(tid,hdr9 if nine else hdr8,t[0][1:],kinds9 if nine else kinds8,flag_col=7 if nine else 6,flag_map=flag_sym)
    ct=px_table("crit",crit_lines)
    wt=px_table("warn",S["Warnings (⚠️)"])
    at=px_table("all",S["All pixels (alphabetical by client)"])
    fixed_block=fixed_html(S, kinds=kinds9 if any(len(t[0])>=9 for t in tables(S.get("Fixed since last week",[]))) else None)
    purchase_block=""
    if "Purchase check (last 28 days)" in S:
        pl=S["Purchase check (last 28 days)"]; pt=tables(pl)
        pdesc=" ".join(paras(pl)[:1])
        if pt:
            phdr=["Client","Pixel ID","Purchase 28d (b / s)","Purchase 7d","Last Purchase","PMS online bookings 28d","Capture","Sales $/day","HG AI CAPI","Flag","Why"]
            pkinds=["first","mono","nowrap","num","nowrap","num","nowrap","num","nowrap","badge","notes"]
            ptab=render_table("purchase",phdr,pt[0][1:],pkinds,flag_col=9,flag_map=flag_sym)
        else: ptab='<div class="empty">No client flagged on Purchase this week.</div>'
        purchase_block=f"""
<section>
  <div class="sec-head"><div><h2>Purchase check, last 28 days</h2><p class="sec-desc">{inline(pdesc)}</p></div></div>
  <div class="card">{ptab}</div>
</section>"""
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
{purchase_block}
<section>
  <div class="sec-head"><div><h2>All pixels</h2><p class="sec-desc">Alphabetical by client. Domains come from the pixel's own 7-day host breakdown in Meta; expected domains are from the expected-domains file, inferred from the brand name unless marked otherwise.</p></div>{seg("all",[("all","All"),("err","Critical"),("warn","Warning"),("ok","Match")])}</div>
  <div class="card">{at}</div>
</section>
{footer(bullets(S["Footer"]))}
"""
    lede="Verifies each client's Meta Pixel receives events only from that client's own site, link pages, GoHighLevel funnel and booking engine, and flags cross-contamination, silent pixels and split or duplicate setups."
    chips=[f"Run {RUN}","Rolling 7-day window" + (", Purchase over 28 days" if purchase_block else ""),"Sources: HiddenGem BM dataset listing, per-account listings, host and event totals"+(", PMS bookings and CAPI state from the HiddenGem AI platform" if purchase_block else ""),compare_chip(S)]
    return page(f"Pixel domain check {WEEK}","Weekly Meta Ads review · Pixel domain check","Pixel domain check",lede,[esc(c) for c in chips],body)

# =====================================================================
# 3. CLIENT BENCHMARK
# =====================================================================
MONTH_RE=re.compile(r"^This month \((booked [^)]+)\): direct revenue (\$[\d,]+) from (\d+) bookings, (.+?) · promo codes: (.+?)\.?$")
def month_strip(p):
    """Three tiles from the generator's 'This month' line: revenue MTD, trend vs the previous month's same span, promo codes."""
    m=MONTH_RE.match(p.strip())
    if not m:
        return f'<div class="month"><div class="none">{inline(p)}</div></div>'
    span,rev,bk,trend,promo=m.groups()
    t=re.match(r"^([+−-])(\d+)% vs (.+?) \((\$[\d,]+) from (\d+) bookings\)$",trend)
    if t:
        sign,n,pspan,prev,pbk=t.groups(); kind="ok" if sign=="+" else "err"
        if int(n)==0: kind="gray"
        trend_val=f'<span class="delta {kind}">{esc(sign+n)}%</span>'; trend_hint=f"{esc(prev)} from {esc(pbk)} bookings, {esc(pspan)}"
        trend_label="vs previous month, same days"
    else:
        trend_val='<span class="delta gray">—</span>'; trend_hint=esc(trend); trend_label="vs previous month"
    pm=re.match(r"^(\d+) uses(?: \((.*)\))?$",promo)
    if pm:
        promo_val=f"{pm.group(1)} use{'s' if pm.group(1)!='1' else ''}"; promo_hint=pm.group(2) or "no codes applied"
    else:
        promo_val="—"; promo_hint=promo
    return ('<div class="month">'
        f'<div class="stat"><div class="label">Direct revenue this month</div><div class="value">{esc(rev)}</div><div class="hint">{esc(bk)} bookings, {esc(span)}</div></div>'
        f'<div class="stat"><div class="label">{trend_label}</div><div class="value">{trend_val}</div><div class="hint">{trend_hint}</div></div>'
        f'<div class="stat"><div class="label">Promo codes this month</div><div class="value">{esc(promo_val)}</div><div class="hint">{esc(promo_hint)}</div></div>'
        '</div>')

SCORED_ORDER = ("Flag to Shawal","Review w/ HG AI","Monitor","Healthy","Scale w/ HG AI")

def one_liner(text):
    """Opening line of a client's weekly notes, for the overview table."""
    t=re.sub(r"^HG AI notes[^:]*:\s*","",text.strip())
    t=re.sub(r"^no HG AI reports? this week(?: \([^)]*\))?\.\s*","",t,flags=re.I)
    sents=[x for x in re.split(r"(?<=[.!?])\s+(?=[A-Z(\"$])",t) if x]
    if not sents: return ""
    out=sents[0]
    if len(out)<50 and len(sents)>1: out+=" "+sents[1]
    for k in FLAG: out=out.replace(k,"")
    out=re.sub(r"\(\s+",  "(", re.sub(r"\s+\)", ")", out))
    return out[:1].upper()+out[1:]

def state_badges(states):
    """One badge per scored state a client has this week, worst first; '2 Healthy' when repeated."""
    c=collections.Counter(states)
    out=[badge(STATE[s], (f"{c[s]} " if c[s]>1 else "")+s) for s in SCORED_ORDER if c[s]]
    if out: return "".join(out)
    return badge("gray","Under gate") if c["Under gate"] else badge("gray","Not scored")

def client_table(tid, trs):
    """Per-client campaign table: the numbers on one row, diagnostics and notes on a line under it.
    One <tbody> per campaign so hover and dividers treat the pair as one; stacks into labelled fields on phones."""
    hdr=["Campaign","Type","Window","Spend","Results","Governing metric","Frequency","State","Change vs last week"]
    th="".join(f'<th{" class=num" if h in ("Spend","Results","Governing metric","Frequency") else ""}>{esc(h)}</th>' for h in hdr)
    def num(c):
        return badge("warn"," ".join(c.replace("⚠️"," ").split())) if "⚠️" in c else inline(c)
    bodies=[]
    for r in trs:
        r=r+[""]*(11-len(r))
        camp,typ,win,spend,res,gov,freq,st,diag,notes,chg=r[:11]
        tds=(f'<td class=first>{inline(camp)}</td>'
             f'<td class=type data-l="Type">{inline(typ)}</td>'
             f'<td class=nowrap data-l="Window">{inline(win)}</td>'
             f'<td class=num data-l="Spend">{inline(spend)}</td>'
             f'<td class="num res" data-l="Results">{inline(res)}</td>'
             f'<td class="num gov" data-l="Governing metric">{inline(gov)}</td>'
             f'<td class=num data-l="Frequency">{num(freq)}</td>'
             f'<td class=nowrap data-l="State">{state_badge(st.strip())}</td>'
             f'<td class=status data-l="Change vs last week">{inline(chg)}</td>')
        det=[(l,v) for l,v in (("Diagnostics",diag),("Notes",notes)) if v.strip() and v.strip()!="—"]
        dh="".join(f"<p><span>{l}</span>{inline(v)}</p>" for l,v in det)
        bodies.append(f'<tbody data-flag="{flag_state(st)}"><tr class=crow>{tds}</tr>'+(f'<tr class=cdet><td colspan=9><div class=cdl>{dh}</div></td></tr>' if det else "")+'</tbody>')
    return f'<div class="tablewrap"><table class="ctable" id="{tid}"><thead><tr>{th}</tr></thead>{"".join(bodies)}</table></div>'

def build_bench():
    md=open(f"{ROOT}/Client Benchmark Reviews (advanced setups)/Weekly Checks/{DATE}-client-benchmark.md",encoding="utf-8").read()
    S=sections(md)
    rows=list(csv.DictReader(open(f"{ROOT}/Client Benchmark Reviews (advanced setups)/Weekly Checks/{DATE}-client-benchmark.csv",encoding="utf-8")))
    cnt=collections.Counter(r["state"] for r in rows)
    # 'Not scored (discovery)' / 'Not scored (lead gen)' rows (4 Nov 2026 rule) are context, not scored
    def not_scored(s): return s in ("Under gate","Tracked in Discovery","No promo data") or s.startswith("Not scored")
    scored=sum(1 for r in rows if not not_scored(r["state"]))
    def attr(s): return html.escape(s.strip(), quote=True)
    def who(r): return f' data-client="{attr(r[0])}" data-am="{attr(r[1])}"'
    foot=bullets(S["Footer"])

    # ---------- per-client blocks, sorted by 30-day spend (all HiddenGem campaigns), highest first
    pkey=[k for k in S if k.startswith("Per client")][0]
    blocks=[]; cur=None
    for l in S[pkey]:
        if l.startswith("### "):
            cur={"head":l[4:].strip(),"lines":[]}; blocks.append(cur)
        elif cur is not None: cur["lines"].append(l)
    states_by_client=collections.defaultdict(list)
    for r in rows: states_by_client[r["client"]].append(r["state"])
    clients=[]
    for c in blocks:
        parts=[p.strip() for p in c["head"].split(" — ")]
        ps=paras(c["lines"])
        blend=[p for p in ps if p.startswith("Blended 30d")]
        m=re.search(r"spend \$([\d,]+)",blend[0]) if blend else None
        hg=[p for p in ps if p.startswith("HG AI notes")]
        clients.append({"name":parts[0],"am":parts[1].replace("AM ","") if len(parts)>1 else "","parts":parts,"lines":c["lines"],"ps":ps,
                        "spend":int(m.group(1).replace(",","")) if m else 0,"summary":one_liner(hg[0]) if hg else ""})
    clients.sort(key=lambda c:-c["spend"])
    for i,c in enumerate(clients): c["id"]=f"client-{i}"
    card_id={c["name"]:c["id"] for c in clients}
    def href(cell): return f"#{card_id[cell.strip()]}" if cell.strip() in card_id else None

    # Advanced in the CRM with no ad account mapped (named in the report footer)
    unmapped=[]
    for b in foot:
        m=re.search(r"no ad account mapping[^:]*:\s*(.+?)\.(?:\s|$)",b)
        if m:
            for n,a in re.findall(r"([^,()]+?) \(AM ([^)]+)\)",m.group(1)):
                unmapped.append({"name":n.strip(),"am":"" if a.strip() in ("—","-") else a.strip()})

    # ---------- stat band
    ct0=tables(S["_pre"]); hdrv=dict(zip(ct0[0][0],ct0[0][1])) if ct0 and len(ct0[0])>1 else {}
    adv_raw=hdrv.get("Advanced clients","—"); m_adv=re.match(r"(\d+)\s*\(\+(\d+) unmapped\)",adv_raw)
    adv_val=m_adv.group(1) if m_adv else adv_raw
    band=(stat("Advanced clients",adv_val,f"+{len(unmapped)} without an ad account" if unmapped else "with an ad account",key="clients")
        +stat("Campaigns scored",str(scored),f"{cnt['Under gate']} under the spend gate",key="scored")
        +stat("Flag to Shawal",str(cnt["Flag to Shawal"]),"Under 2x or no purchases",dot="err",key="flag")
        +stat("Review w/ HG AI",str(cnt["Review w/ HG AI"]),"2 to 5x",dot="warn",key="review")
        +stat("Monitor",str(cnt["Monitor"]),"5 to 8x",dot="gray",key="monitor")
        +stat("Healthy",str(cnt["Healthy"]),"8 to 15x",dot="ok",key="healthy")
        +stat("Scale w/ HG AI",str(cnt["Scale w/ HG AI"]),"Above 15x",dot="brand",key="scale")
        +stat("Frequency over 5",str(sum(1 for r in rows if r.get("freq_flag")=="yes")),"Refresh creative",dot="warn",key="freq"))

    # ---------- section 1: all clients
    otr=[]
    for c in clients:
        summ=f'<span class="clamp" title="{attr(re.sub(r"[`*]","",c["summary"]))}">{inline(c["summary"])}</span>' if c["summary"] else "—"
        otr.append(f'<tr data-client="{attr(c["name"])}" data-am="{attr(c["am"])}" data-href="#{c["id"]}">'
                   f'<td class=first><a href="#{c["id"]}">{esc(c["name"])}</a></td><td class=nowrap>{esc(c["am"])}</td>'
                   f'<td class=sum>{summ}</td><td class=st><span class=stl>{state_badges(states_by_client.get(c["name"],[]))}</span></td>'
                   f'<td class="num spend">{"$"+format(c["spend"],",") if c["spend"] else "—"}</td></tr>')
    if unmapped:
        otr.append(f'<tr class=grp data-grp><td colspan=5>Without an ad account · {len(unmapped)}</td></tr>')
        for u in unmapped:
            otr.append(f'<tr class=muted data-unmapped data-client="{attr(u["name"])}" data-am="{attr(u["am"])}">'
                       f'<td class=first>{esc(u["name"])}</td><td class=nowrap>{esc(u["am"]) or "—"}</td>'
                       f'<td class=sum>Advanced in the CRM, no ad account mapped yet, so nothing is scored.</td>'
                       f'<td class=st>{badge("gray","No ad account")}</td><td class=num>—</td></tr>')
    overview=(f'<div class="tablewrap"><table id="ovw" data-ftable><thead><tr><th>Client</th><th>AM</th><th>Summary</th><th>State</th><th class=num>Spend, 30 days</th></tr></thead>'
              f'<tbody>{"".join(otr)}</tbody></table><div class="empty" hidden>No clients match this filter.</div></div>')

    # ---------- section 2: campaign lists
    hdr=["Client","AM","Campaign","Type","Spend / window","Governing metric","State","Status vs last week"]
    kinds=["first","text","camp","type","num","num","badge","status"]
    act_rows=tables(S["Action needed"])[0][1:]; sc_rows=tables(S["Scale candidates"])[0][1:]
    act=render_table("act",hdr,act_rows,kinds,flag_col=6,flag_map=flag_state,row_attrs=who,first_href=href,table_attrs=" data-ftable")
    sc=render_table("scale",hdr,sc_rows,kinds,flag_col=6,flag_map=flag_state,row_attrs=who,first_href=href,table_attrs=" data-ftable")
    fkey=[k for k in S if k.startswith("Frequency watch")]
    fhdr=["Client","AM","Campaign","Type","Frequency","Spend / window","Governing metric","State"]
    fkinds=["first","text","camp","type","num","num","num","badge"]
    frows=[r for r in tables(S[fkey[0]])[0][1:] if r and r[0].strip()!="—"] if fkey and tables(S[fkey[0]]) else []
    fw=render_table("freq",fhdr,frows,fkinds,flag_col=7,flag_map=flag_state,row_attrs=who,first_href=href,table_attrs=" data-ftable") if frows else '<div class="empty">No Sales or Retargeting campaign above a frequency of 5 this week.</div>'
    def tmeta(tid, trows, state_col, mode, kind="gray", unit="campaign"):
        """Badges in a toggle's header; the filter script rewrites them in the same format."""
        if mode=="states":
            c=collections.Counter(r[state_col].strip() for r in trows)
            h="".join(badge(STATE[s], f"{c[s]} {s}") for s in SCORED_ORDER if c[s])
        else:
            h=badge(kind, f"{len(trows)} {unit}{'s' if len(trows)!=1 else ''}") if trows else ""
        return f'<span class="tmeta" data-meta-for="{tid}" data-meta="{mode}" data-kind="{kind}" data-unit="{unit}">{h or badge("gray","None")}</span>'
    def toggle(tid, title, desc, meta, inner):
        return f"""<details class="card tgl" id="sec-{tid}">
<summary><span class="chev" aria-hidden="true"></span><span class="ttxt"><span class="trow"><h3>{esc(title)}</h3>{meta}</span><span class="sec-desc">{desc}</span></span><span class="tact" aria-hidden="true"></span></summary>
{inner}
</details>"""

    # ---------- section 3: one collapsible card per client
    chdr=["Campaign","Type","Window","Spend","Results","Governing metric","Frequency","State","Diagnostics vs investigate lines","Notes","Change vs last week"]
    ckinds=["first","nowrap","nowrap","num","num","num","num","badge","notes","notes","nowrap"]
    old_chdr=chdr[:6]+chdr[7:]; old_ckinds=ckinds[:6]+ckinds[7:]   # reports before 2026-10-06 have no Frequency column
    def strip_lbl(p,lbl): return re.sub(r"^"+lbl+r"[^:]*:\s*","",p)
    MN=re.compile(r"^Meeting notes\s*"); PZ=re.compile(r"^Paused in window, not scored:\s*")
    def fmt_note(n):
        n=MN.sub('',n).lstrip(':').strip()
        m=re.match(r"^\(([^)]*?) (\d{4}-\d{2}-\d{2})\):\s*(.*)$",n)
        return f"<strong>{esc(m.group(1))}, {esc(m.group(2))}.</strong> {inline(m.group(3))}" if m else inline(n)
    chtml=[]
    for i,c in enumerate(clients):
        parts=c["parts"]; name=c["name"]; am=c["am"]
        acct=parts[2].replace("account ","") if len(parts)>2 else ""; src=parts[3] if len(parts)>3 else "live"
        m=re.match(r"(.*)\((\d+)\)$",acct); acct_name,acct_id=(m.group(1).strip(),m.group(2)) if m else (acct,"")
        src_badge="" if src.startswith("live") else badge("warn","CSV export, provisional")
        ps=c["ps"]; tbls=tables(c["lines"])
        tof=[p for p in ps if p.startswith("ToF")]; roi=[p for p in ps if p.startswith("Monthly ROI")]
        blend=[p for p in ps if p.startswith("Blended 30d")]; month=[p for p in ps if p.startswith("This month")]
        notes=[p for p in ps if p.startswith("Meeting notes")]; hg=[p for p in ps if p.startswith("HG AI notes")]
        nocamp=[p for p in ps if p.startswith("No Lead Gen") or p.startswith("No live Lead Gen")]
        pausedl=[p for p in ps if p.startswith("Paused in window")]
        tid=f"c{i}"
        if tbls and len(tbls[0][0])>=11: tbl=client_table(tid,tbls[0][1:])
        elif tbls: tbl=render_table(tid,old_chdr,tbls[0][1:],old_ckinds,flag_col=6,flag_map=flag_state)
        else: tbl=f'<div class="empty">{inline(nocamp[0]) if nocamp else "No scored campaigns."}</div>'
        notes_html="".join(f"<dt>Meeting notes</dt><dd>{fmt_note(n)}</dd>" for n in notes) if notes else "<dt>Meeting notes</dt><dd>Not mentioned in this week's meetings.</dd>"
        paused_html="".join(f"<dt>Paused in window</dt><dd>{inline(PZ.sub('',pl))}</dd>" for pl in pausedl)
        hgt=strip_lbl(hg[0],"HG AI notes") if hg else ""
        kv=f"""<dl class="kv">
{paused_html}<dt>Monthly ROI</dt><dd>{inline(strip_lbl(roi[0],"Monthly ROI")) if roi else "—"}</dd>
{notes_html}
<dt>HG AI notes</dt><dd>{inline(hgt[:1].upper()+hgt[1:]) if hg else "—"}</dd>
</dl>"""
        spend=f'${c["spend"]:,}' if c["spend"] else "—"
        chtml.append(f"""<details class="card ccard" id="{c["id"]}" data-client="{attr(name)}" data-am="{attr(am)}">
<summary><span class="chev" aria-hidden="true"></span><span class="cmain"><span class="cname">{esc(name)}</span><span class="csub">AM {esc(am)} · {esc(acct_name)} <span class="mono">{esc(acct_id)}</span></span></span><span class="cstates">{src_badge}{state_badges(states_by_client.get(name,[]))}</span><span class="cspend">{spend}<small>spend, 30 days</small></span></summary>
{month_strip(month[0]) if month else ""}
<div class="tof">{inline(tof[0]) if tof else ""}</div>
{f'<div class="tof">{inline(blend[0])}</div>' if blend else ""}
{tbl}
{kv}
</details>""")

    # ---------- section 4: meetings and report notes
    mkey=[k for k in S if k.startswith("Weekly Meta Ads meetings")][0]
    meetings=[]; cur=None
    for l in S[mkey]:
        if l.startswith("### "):
            cur={"head":l[4:].strip(),"lines":[]}; meetings.append(cur)
        elif cur is not None: cur["lines"].append(l)
    mhtml=[]
    for m in meetings:
        parts=[p.strip() for p in m["head"].split(" — ")]
        title,date=parts[0],parts[1]; doc=re.sub(r"[`doc ]","",parts[2]) if len(parts)>2 else ""
        summ=[]; dec=[]; nxt=[]; mode="s"
        for l in m["lines"]:
            t=l.strip()
            if not t: continue
            if t=="Decisions:": mode="d"; continue
            if t=="Next steps:": mode="n"; continue
            if mode=="s": summ.append(t)
            elif mode=="d" and t.startswith("- "): dec.append(t[2:])
            elif mode=="n" and t.startswith("- "): nxt.append(t[2:])
        dh=f'<div class="lbl">Decisions</div><ul>{"".join(f"<li>{inline(d)}</li>" for d in dec)}</ul>' if dec else ""
        nh=f'<div class="lbl">Next steps</div><ul>{"".join(f"<li>{inline(d)}</li>" for d in nxt)}</ul>' if nxt else ""
        lead=inline(summ[0]) if summ else ""
        rest="".join(f"<p>{inline(p)}</p>" for p in summ[1:])
        mhtml.append(f'<details class="meeting"><summary><span class="chev" aria-hidden="true"></span><span class="mtxt"><span class="mtitle">{esc(title)}</span><span class="when">{esc(date)} · Notes by Gemini · doc <span class="mono">{esc(doc)}</span></span>{f"<span class=mlead>{lead}</span>" if lead else ""}</span></summary><div class="mbody">{rest}{dh}{nh}</div></details>')
    meet_block=f'<div class="mlist">{"".join(mhtml)}</div>' if mhtml else '<p class="np">No Meta Ads meeting notes since the last run.</p>'
    states_para=[p for p in paras(S["_pre"]) if p.startswith("States come from")]
    nm=len(meetings)
    m_lbl=f"{nm} meeting" + ("s" if nm!=1 else "")
    notes_meta=f'<span class="tmeta">{badge("gray", m_lbl)}{badge("gray", f"{len(foot)} method notes")}</span>'
    notes_inner=f"""<div class="nbody">
<div><h4>Weekly Meta Ads meetings since last run</h4><p class="sec-desc">Notes by Gemini attached to the calendar events, read via Drive. Summary, decisions and next steps as Gemini wrote them; client-specific sentences are also pulled into each client's card. Transcript not used.</p>{meet_block}</div>
<div><h4>How states are assigned</h4><p class="np">{inline(states_para[0]) if states_para else "—"}</p></div>
<div><h4>Method and scope</h4><ul class="nl">{"".join(f"<li>{inline(b)}</li>" for b in foot)}</ul></div>
</div>"""

    # ---------- filter bar (shown by the script; useless without it)
    am_counts=collections.Counter(a for a in [c["am"] for c in clients]+[u["am"] for u in unmapped] if a)
    am_opts="".join(f'<option value="{attr(a)}">{esc(a)} ({n})</option>' for a,n in sorted(am_counts.items()))
    def opts(lst): return "".join(f'<option value="{attr(n)}">{esc(n)}</option>' for n in sorted((x["name"] for x in lst),key=str.lower))
    cl_opts=f'<optgroup label="With an ad account">{opts(clients)}</optgroup>'+(f'<optgroup label="Without an ad account">{opts(unmapped)}</optgroup>' if unmapped else "")
    n_all=len(clients)+len(unmapped)
    fbar=f"""<div class="fbar" id="fbar" role="search" aria-label="Filter this review" hidden>
<div class="fld"><label for="f-am">Account manager</label><span class="sel"><select id="f-am"><option value="all">All account managers</option>{am_opts}</select></span></div>
<div class="fld"><label for="f-client">Client</label><span class="sel"><select id="f-client"><option value="all">All clients</option>{cl_opts}</select></span></div>
<button type="button" class="btn" id="f-clear" hidden>Clear filters</button>
<p class="fsum" id="f-sum" aria-live="polite">{n_all} Advanced clients across {len(am_counts)} account managers</p>
</div>"""
    data=json.dumps({"clients":[{"n":c["name"],"a":c["am"]} for c in sorted(clients,key=lambda c:c["name"].lower())],
                     "unmapped":[{"n":u["name"],"a":u["am"]} for u in sorted(unmapped,key=lambda u:u["name"].lower())],
                     "rows":[[r["client"],r["am"],r["state"],1 if r.get("freq_flag")=="yes" else 0] for r in rows]},ensure_ascii=False).replace("</","<\\/")

    def sec_top(n, eyebrow, title, desc, actions=""):
        return f'<div class="sec-top"><div><span class="eb">{n} · {esc(eyebrow)}</span><h2>{esc(title)}</h2><p class="sec-desc">{desc}</p></div>{actions}</div>'
    body=f"""
{fbar}
<script type="application/json" id="bench-data">{data}</script>
<div class="card band">{band}</div>
<section class="sec" id="overview">
{sec_top("01","Overview","All clients","Every CRM-Advanced client, highest 30-day ad spend first (all HiddenGem campaigns). State shows this week's scored Sales campaigns, worst first; the summary is the opening line of the client's notes. Click a row for the full detail.")}
<div class="card">{overview}</div>
</section>
<section class="sec" id="lists">
{sec_top("02","Campaign lists","Action needed, scale and frequency","Sales-objective campaigns only. Open a list to see its rows; the counts follow the filter.")}
<div class="stack">
{toggle("act","Action needed","Flag to Shawal before Review w/ HG AI, highest spend first.",tmeta("act",act_rows,6,"states"),act)}
{toggle("scale","Scale candidates","Campaigns above the Scale line. Full context goes to HG AI, which picks where budget goes.",tmeta("scale",sc_rows,6,"count","brand"),sc)}
{toggle("freq","Frequency watch","14-day frequency above 5.0. Frequency does not change the ROAS state; this is the list to refresh creative or widen the audience on.",tmeta("freq",frows,7,"count","warn"),fw)}
</div>
</section>
<section class="sec" id="clients">
{sec_top("03","Per client","Client detail","Same order as the overview. Each card holds this month's bookings, the campaign table, monthly ROI and the client's notes.",'<button type="button" class="btn sm" id="x-all">Expand all</button>')}
<div class="cards">{"".join(chtml)}</div>
</section>
<section class="sec" id="notes">
{sec_top("04","Notes","Meeting summary and report notes","This week's Meta Ads meeting notes, how states are assigned, and the method behind the numbers.")}
{toggle("notes","Meta Ads meetings and notes","Gemini meeting summaries, the state rules and the report's method notes.",notes_meta,notes_inner)}
</section>
<p class="genline">HiddenGem Marketing · weekly Meta Ads review · generated {RUN} from the saved report and CSV sidecar.</p>
"""
    lede="Scores each CRM-Advanced client's Sales-objective Meta campaigns (Retargeting, Prospecting, Sales) on 14-day pixel ROAS against the Benchmarks doc decision table, with this month's bookings, monthly ROI and this week's meeting notes. Lead Gen and Discovery spend are shown for context."
    rl=run_line(S); m2=re.search(r"CSV export (\d{4}-\d{2}-\d{2}) to (\d{4}-\d{2}-\d{2}) for the (\d+) accounts",rl)
    chips=[f"Run {RUN}","Sales campaigns: 14-day pixel ROAS, $200 gate","Lead Gen and Discovery: context only"]+([f"CSV export {m2.group(1)} to {m2.group(2)} for {m2.group(3)} accounts"] if m2 else [])+[compare_chip(S)]
    return page(f"Client benchmark {WEEK}","Weekly Meta Ads review · Client benchmark","Client benchmark review",lede,[esc(c) for c in chips],body,js=BENCH_JS,css=BENCH_CSS)


if __name__ == "__main__":
    outs={
     f"{ROOT}/Ad Spends Checks/Weekly Checks/{DATE}-ad-spend-check.html": build_spend,
     f"{ROOT}/Meta Pixel Reviews/Weekly Checks/{DATE}-pixel-domain-check.html": build_pixel,
     f"{ROOT}/Client Benchmark Reviews (advanced setups)/Weekly Checks/{DATE}-client-benchmark.html": build_bench,
    }
    for p,fn in outs.items():
        try: h=fn()
        except FileNotFoundError as e:
            print(f"skipped {os.path.basename(p)}: no report for {DATE} ({os.path.basename(e.filename)})"); continue
        open(p,"w",encoding="utf-8").write(h); print(p, len(h))
