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
  --hover:#fafafa;
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
  --hover:#171717;
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
  --hover:#171717;
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
/* whole-section toggles (01, 03, 04): the heading opens and closes the section */
.stgl>summary{list-style:none;cursor:pointer;display:block;margin:0 -14px;padding:12px 14px;border-radius:12px;transition:background .1s linear}
.stgl>summary::-webkit-details-marker{display:none}
.stgl>summary:hover{background:var(--hover)}
.stgl>summary:focus-visible{box-shadow:var(--focus)}
.stgl[open]>summary{margin-bottom:16px}
.stgl .shead{display:flex;align-items:center;gap:14px}
.stgl .shead h2{font:600 30px/38px 'Inter',sans-serif;letter-spacing:-.02em;margin:0;text-wrap:balance}
.stgl .chev{flex:none;width:10px;height:10px;border-right:2px solid var(--text-3);border-bottom:2px solid var(--text-3);transform:rotate(-45deg);margin:0 2px;transition:transform .24s cubic-bezier(.2,0,0,1)}
.stgl[open]>summary .chev{transform:rotate(45deg)}
.stgl .tact{margin-left:auto;flex:none;display:inline-flex;align-items:center;height:36px;padding:0 14px;border:1px solid var(--border-strong);border-radius:8px;background:var(--panel);box-shadow:var(--shadow-xs);font:600 14px/20px 'Inter',sans-serif;color:var(--text-2)}
.stgl .tact::after{content:"Show"}
.stgl[open] .tact::after{content:"Hide"}
.stgl .sec-desc{display:block;margin:6px 0 0 28px}
.stgl .smeta{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0 0 28px}
.sec.stgl{margin-bottom:28px}
.sec.stgl[open]{margin-bottom:48px}
.stgl .fbar{margin-bottom:16px}
@media (max-width:640px){.stgl .shead h2{font-size:24px;line-height:32px}.stgl .sec-desc,.stgl .smeta{margin-left:0}}
@media (prefers-reduced-motion: reduce){.stgl .chev{transition:none}}
/* stat band */
.band{display:grid;grid-template-columns:repeat(var(--n,8),minmax(0,1fr));margin:0 0 48px}
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
  const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
  // section and list toggles: remember each viewer's open / closed choice
  document.querySelectorAll('details.tgl[id],details.stgl[id]').forEach(d=>{
    const key='bench.tgl.'+d.id;
    try{const v=localStorage.getItem(key); if(v==='open') d.open=true; else if(v==='closed') d.open=false;}catch(e){}
    d.addEventListener('toggle',()=>{try{localStorage.setItem(key,d.open?'open':'closed');}catch(e){}});
  });
  const bar=document.getElementById('fbar'), dataEl=document.getElementById('bench-data'), sec=document.getElementById('sec-clients');
  if(!bar||!dataEl) return;
  const D=JSON.parse(dataEl.textContent);
  const amSel=document.getElementById('f-am'), clSel=document.getElementById('f-client');
  const clr=document.getElementById('f-clear'), sum=document.getElementById('f-sum'), xall=document.getElementById('x-all');
  const cards=[...document.querySelectorAll('.cards>details[data-client]')];
  const ams=[...new Set(D.clients.map(c=>c.a).filter(Boolean))].sort();
  const plural=(n,w)=>n+' '+w+(n===1?'':'s');
  const esc=s=>s.replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  function fillClients(){
    const am=amSel.value, cur=clSel.value;
    while(clSel.options.length>1) clSel.remove(1);
    D.clients.filter(c=>am==='all'||c.a===am).forEach(c=>clSel.add(new Option(c.n,c.n)));
    clSel.value=[...clSel.options].some(o=>o.value===cur)?cur:'all';
  }
  const match=(c,a)=>(amSel.value==='all'||a===amSel.value)&&(clSel.value==='all'||c===clSel.value);
  function xlabel(){ const vis=cards.filter(c=>!c.hidden); xall.textContent=vis.length&&vis.every(c=>c.open)?'Collapse all':'Expand all'; }
  // the filter narrows the client cards in this section only
  function apply(){
    const am=amSel.value, cl=clSel.value, on=am!=='all'||cl!=='all';
    amSel.classList.toggle('on',am!=='all'); clSel.classList.toggle('on',cl!=='all');
    let nc=0; cards.forEach(c=>{const s=match(c.dataset.client,c.dataset.am); c.hidden=!s; if(s){nc++; if(cl!=='all') c.open=true;}});
    const who=[am!=='all'?esc(am):'',cl!=='all'?esc(cl):''].filter(Boolean).join(' · ');
    sum.innerHTML=on?'Showing <strong>'+plural(nc,'client')+'</strong> of '+cards.length+' · '+who:plural(cards.length,'client')+' across '+ams.length+' account managers';
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
  if(D.clients.some(c=>c.n===q.get('client'))) clSel.value=q.get('client');
  bar.hidden=false;
  apply();
  if(sec&&(amSel.value!=='all'||clSel.value!=='all')) sec.open=true;   // a shared filtered link lands on the cards
  // a client name or an overview row opens that client's card (clearing a filter that hides it)
  function openCard(id,scroll){
    const d=document.getElementById(id); if(!d) return;
    if(sec) sec.open=true;
    if(d.hidden){ amSel.value='all'; fillClients(); clSel.value='all'; apply(); }
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
  xall.addEventListener('click',()=>{const vis=cards.filter(c=>!c.hidden), open=!vis.every(c=>c.open); vis.forEach(c=>{c.open=open;}); xlabel();});
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
<header class="title"><h1>{esc(h1)}</h1><p class="lede">{lede}</p>{f'<div class="meta">{chips_html}</div>' if chips_html else ""}</header>
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
# Shared layout for the ad spend and pixel pages (2026-11-16, Shawal: "for ad spend and pixel review
# pages - follow same practices"). Same structure as the client benchmark page: title and date window
# only, a stat band, 01 Overview (one row per client, highest live $/day first), 02 collapsible lists,
# 03 per-client cards behind the account manager / client filter, 04 notes. Reuses BENCH_CSS and the
# BENCH_JS filter, with its own localStorage prefix per page.
# =====================================================================
SPEND_JS = BENCH_JS.replace("'bench.tgl.'", "'spend.tgl.'")
PIXEL_JS = BENCH_JS.replace("'bench.tgl.'", "'pixel.tgl.'")
REVIEW_CSS = """
.ccard .cspend{min-width:110px}
.ccard .month{grid-template-columns:repeat(auto-fit,minmax(150px,1fr))}
.ctable td.dom{min-width:170px;max-width:260px;white-space:normal;font-size:13px;line-height:19px;color:var(--text-3);word-break:break-word}
.ctable td.pid{white-space:normal;min-width:200px}
.ctable td.pid .mono{display:block;font-size:12px;line-height:18px;color:var(--text-4)}
.ccard .tof strong{color:var(--text-2);font-weight:600}
.nbody .np+.np{margin-top:10px}
"""

def _attr(s): return html.escape((s or "").strip(), quote=True)
def _f(x):
    try: return float(x or 0)
    except ValueError: return 0.0
def _money(v): return f"${v:,.0f}"
def _signed(v): return ("+" if v >= 0 else "−") + f"${abs(v):,.0f}"
def _plural(n, w): return f"{n} {w}{'' if n == 1 else 's'}"
def _span(a, b):
    return f"{a.day} {a:%b} – {b.day} {b:%b %Y}" if a.year == b.year else f"{a.day} {a:%b %Y} – {b.day} {b:%b %Y}"
def _norm(s): return re.sub(r"[^a-z0-9]", "", (s or "").lower())
def _cap(s): s = (s or "").strip(); return s[:1].upper() + s[1:]

def _stoggle(sid, n, eyebrow, title, desc, meta, inner):
    return f"""<details class="sec stgl" id="sec-{sid}">
<summary><span class="eb">{n} · {esc(eyebrow)}</span><span class="shead"><span class="chev" aria-hidden="true"></span><h2>{esc(title)}</h2><span class="tact" aria-hidden="true"></span></span><span class="sec-desc">{desc}</span><span class="smeta">{meta}</span></summary>
{inner}
</details>"""
def _sec_top(n, eyebrow, title, desc):
    return f'<div class="sec-top"><div><span class="eb">{n} · {esc(eyebrow)}</span><h2>{esc(title)}</h2><p class="sec-desc">{desc}</p></div></div>'
def _toggle(tid, title, desc, meta, inner):
    return f"""<details class="card tgl" id="sec-{tid}">
<summary><span class="chev" aria-hidden="true"></span><span class="ttxt"><span class="trow"><h3>{esc(title)}</h3><span class="tmeta">{meta or badge("gray","None")}</span></span><span class="sec-desc">{desc}</span></span><span class="tact" aria-hidden="true"></span></summary>
{inner}
</details>"""
def _overview(trs, last_hdr, empty="No clients."):
    return (f'<div class="tablewrap"><table id="ovw"><thead><tr><th>Client</th><th>AM</th><th>Summary</th><th>Status</th><th class=num>{esc(last_hdr)}</th></tr></thead>'
            f'<tbody>{"".join(trs) or f"<tr><td colspan=5>{esc(empty)}</td></tr>"}</tbody></table></div>')
def _ovw_row(c, summary, states, value):
    summ = f'<span class="clamp" title="{_attr(re.sub(r"[`*]", "", summary))}">{inline(summary)}</span>' if summary else "—"
    return (f'<tr data-client="{_attr(c["name"])}" data-am="{_attr(c["am"])}" data-href="#{c["id"]}">'
            f'<td class=first><a href="#{c["id"]}">{esc(c["name"])}</a></td><td class=nowrap>{esc(c["am"]) or "—"}</td>'
            f'<td class=sum>{summ}</td><td class=st><span class=stl>{states}</span></td><td class="num spend">{value}</td></tr>')
def _card(c, sub_html, states, value, value_sub, inner):
    return f"""<details class="card ccard" id="{c["id"]}" data-client="{_attr(c["name"])}" data-am="{_attr(c["am"])}">
<summary><span class="chev" aria-hidden="true"></span><span class="cmain"><span class="cname">{esc(c["name"])}</span><span class="csub">{sub_html}</span></span><span class="cstates">{states}</span><span class="cspend">{value}<small>{esc(value_sub)}</small></span></summary>
{inner}
</details>"""
def _filter(clients):
    am_counts = collections.Counter(c["am"] for c in clients if c["am"])
    am_opts = "".join(f'<option value="{_attr(a)}">{esc(a)} ({n})</option>' for a, n in sorted(am_counts.items()))
    cl_opts = "".join(f'<option value="{_attr(c["name"])}">{esc(c["name"])}</option>' for c in sorted(clients, key=lambda c: c["name"].lower()))
    fbar = f"""<div class="fbar" id="fbar" role="search" aria-label="Filter client detail" hidden>
<div class="fld"><label for="f-am">Account manager</label><span class="sel"><select id="f-am"><option value="all">All account managers</option>{am_opts}</select></span></div>
<div class="fld"><label for="f-client">Client</label><span class="sel"><select id="f-client"><option value="all">All clients</option>{cl_opts}</select></span></div>
<button type="button" class="btn" id="f-clear" hidden>Clear filters</button>
<p class="fsum" id="f-sum" aria-live="polite">{_plural(len(clients), "client")} across {len(am_counts)} account managers</p>
<button type="button" class="btn" id="x-all">Expand all</button>
</div>"""
    data = json.dumps({"clients": [{"n": c["name"], "a": c["am"]} for c in sorted(clients, key=lambda c: c["name"].lower())]}, ensure_ascii=False).replace("</", "<\\/")
    return fbar, f'<script type="application/json" id="bench-data">{data}</script>'
def _notes(blocks):
    """blocks: list of (heading, html) for section 04."""
    return '<div class="card"><div class="nbody">' + "".join(f"<div><h4>{esc(h)}</h4>{b}</div>" for h, b in blocks if b) + "</div></div>"
def _ul(items): return '<ul class="nl">' + "".join(f"<li>{inline(b)}</li>" for b in items) + "</ul>" if items else ""
def _tiles(tiles): return '<div class="month">' + "".join(stat(l, v, h) for l, v, h in tiles) + "</div>"
GENLINE = '<p class="genline">HiddenGem Marketing · weekly Meta Ads review · generated {run} from the saved report and CSV sidecar.</p>'

def _spend_by_client():
    """Same-date ad spend CSV: client -> (AM, live $/day). The pixel page uses it for the AM filter and the spend order."""
    p = f"{ROOT}/Ad Spends Checks/Weekly Checks/{DATE}-ad-spend-check.csv"
    if not os.path.exists(p): return {}
    out = {}
    for r in csv.DictReader(open(p, encoding="utf-8")):
        v = r.get("total_live") if "total_live" in r else r.get("actual_daily_budget")
        out[_norm(r["client"])] = (r.get("am", "") or "", _f(v) if (v or "") != "" else None)
    return out

# =====================================================================
# 1. AD SPEND CHECK
# =====================================================================
STATUS = {"up":("brand","Up"),"down":("warn","Down"),"new":("ok","New"),"same":("gray","Same"),"unchanged":("gray","Same"),"reshuffled":("brand","Reshuffled"),
          "blocked":("err","Blocked"),"first run":("gray","First run"),"first_run":("gray","First run"),"removed":("gray","Removed")}
def status_badge(c):
    k,l=STATUS.get(c.strip().lower(),("gray",c.strip())); return badge(k,l)
def status_group(c): return "same" if c.strip().lower() in ("same","unchanged","first run","first_run") else "changed"
FLAGWORD = {"critical":("err","Critical"),"warning":("warn","Warning"),"match":("ok","Match"),"blocker":("gray","Blocked")}
FLAG_ORDER = ("critical","blocker","warning","match")
def flagword_badge(f): k,l=FLAGWORD.get(f,("gray",f or "—")); return badge(k,l)

def _campaigns(cell):
    out = []
    for part in [p.strip() for p in (cell or "").split("; ") if p.strip()]:
        m = re.match(r"^(.*) \$([\d,.]+)$", part)
        out.append((m.group(1), _f(m.group(2).replace(",", ""))) if m else (part, None))
    return sorted(out, key=lambda x: -(x[1] or 0))

def build_spend_v2(md, rows):
    S = sections(md)
    live = [r for r in rows if r["source"] == "live"]; blocked = [r for r in rows if r["source"] != "live"]
    tot = lambda k: sum(_f(r[k]) for r in live)
    total, spent = tot("total_live"), tot("spend_7d")
    has_prev = any(r["prev_total"] for r in live); prev = sum(_f(r["prev_total"]) for r in live if r["prev_total"])
    cnt = collections.Counter(r["status"] for r in rows)
    CHG = ("up", "down", "new", "reshuffled"); changed = sum(cnt[k] for k in CHG)
    hint = (f"vs ${prev:,.0f} last run ({_signed(total - prev)})" if has_prev else "first run")
    chg_hint = ", ".join(f"{cnt[k]} {k}" for k in CHG if cnt[k]) or "none"
    tiles = [("Clients checked", str(len(rows)), f"{len(live)} live reads, {len(blocked)} blocked", None),
             ("Total live $/day", _money(total), hint, None),
             ("Spent last 7 days", _money(spent), f"${spent/7:,.0f} per day", None),
             ("ToF Giveaway", _money(tot("tof_giveaway")), "per day", None),
             ("MoF Leads", _money(tot("mof_leads")), "per day", None),
             ("MoF Sales LoL", _money(tot("mof_sales_lol")), "per day", None),
             ("BoF Sales", _money(tot("bof_sales")), "per day", None)]
    if tot("other"): tiles.append(("Other", _money(tot("other")), "per day", None))
    tiles.append(("Changed", str(changed), chg_hint, "brand"))
    band = "".join(stat(l, v, h, dot=d) for l, v, h, d in tiles)

    clients = sorted(({"name": r["client"], "am": r["am"], "r": r} for r in rows), key=lambda c: (-_f(c["r"]["total_live"]), c["name"].lower()))
    for i, c in enumerate(clients): c["id"] = f"client-{i}"
    card_id = {c["name"]: c["id"] for c in clients}
    href = lambda cell: (f"#{card_id[cell.strip()]}" if cell.strip() in card_id else None)
    TYPES = [("tof_giveaway", "ToF"), ("mof_leads", "Leads"), ("mof_sales_lol", "LoL"), ("bof_sales", "BoF"), ("other", "Other")]
    def mix(r): return " · ".join(f"{l} {_money(_f(r[k]))}" for k, l in TYPES if _f(r[k])) or "No active campaigns"

    # 01 overview
    otr = []
    for c in clients:
        r = c["r"]; st = r["status"]
        if r["source"] != "live": summ = "Account not readable this run."
        elif st in ("up", "down", "reshuffled") and r["what_changed"]: summ = _cap(r["what_changed"])
        elif st == "new": summ = "New this run. " + mix(r) + "."
        else: summ = mix(r) + "."
        val = "n/a" if r["source"] != "live" else _money(_f(r["total_live"]))
        otr.append(_ovw_row(c, summ, status_badge(st.replace("_", " ")), val))

    # 02 lists
    ch_t = tables(S.get("Changes since last week", []))
    if ch_t and len(ch_t[0]) > 1:
        ch_rows = [r[:6] + [_cap(r[6])] + r[7:] if len(r) > 6 else r for r in ch_t[0][1:]]
        ch = render_table("changes", ["Client", "AM", "Last week", "This week", "Change", "Status", "What changed"], ch_rows,
                          ["first", "text", "num", "num", "num", "badge", "notes"], flag_col=5, flag_map=status_group, badge_fn=status_badge, first_href=href)
        sc = collections.Counter(r[5].strip() for r in ch_rows if len(r) > 5)
        ch_meta = "".join(badge(STATUS.get(s.lower(), ("gray",))[0], f"{n} {s.lower()}") for s, n in sc.items())
    else:
        ps = paras(S.get("Changes since last week", [])); ch = f'<div class="empty">{inline(ps[0]) if ps else "No budget changes."}</div>'; ch_meta = ""
    zero = [r for r in live if _f(r["total_live"]) == 0]
    zt = render_table("zero", ["Client", "AM", "Spent 7d", "Status vs last week"],
                      [[r["client"], r["am"], _money(_f(r["spend_7d"])), r["status"].replace("_", " ")] for r in zero],
                      ["first", "text", "num", "badge"], badge_fn=status_badge, first_href=href) if zero else '<div class="empty">Every live account has an active budget.</div>'
    lists = (_toggle("changes", "Changes since last run", "Clients whose live daily budget or campaign mix moved, largest change first, with the campaigns behind it.", ch_meta, ch)
             + _toggle("zero", "Accounts at $0/day", "Mapped accounts with no active campaign budget at run time (paused, waiting to launch, or ads off).", badge("gray", _plural(len(zero), "account")) if zero else "", zt))
    if blocked:
        bt = render_table("blocked", ["Client", "AM", "Account", "Error"], [[r["client"], r["am"], r["ad_account_id"], r["campaigns"]] for r in blocked],
                          ["first", "text", "mono", "notes"], first_href=href)
        lists += _toggle("blocked", "Blocked accounts", "Accounts the API could not read this run; their rows carry n/a.", badge("err", _plural(len(blocked), "account")), bt)

    # 03 per client
    chtml = []
    for i, c in enumerate(clients):
        r = c["r"]; ok = r["source"] == "live"
        tl = [(l2, _money(_f(r[k])), "per day") for k, l2 in (("tof_giveaway", "ToF Giveaway"), ("mof_leads", "MoF Leads"), ("mof_sales_lol", "MoF Sales LoL"), ("bof_sales", "BoF Sales"), ("other", "Other")) if k != "other" or _f(r[k])]
        tl.append(("Spent last 7 days", _money(_f(r["spend_7d"])), f"${_f(r['spend_7d'])/7:,.0f} per day"))
        if r["prev_total"]:
            tl.append(("Last run", _money(_f(r["prev_total"])), f"{_signed(_f(r['change']))} this run" if _f(r["change"]) else "no change"))
        camps = _campaigns(r["campaigns"]) if ok else []
        ct = (render_table(f"c{i}", ["Campaign", "Daily budget"], [[n, _money(b) if b is not None else "—"] for n, b in camps], ["first", "num"])
              if camps else f'<div class="empty">{"Account not readable this run." if not ok else "No active campaigns at run time."}</div>')
        wc = f'<div class="tof"><strong>What changed.</strong> {inline(_cap(r["what_changed"]))}</div>' if r["what_changed"] else ""
        inner = (_tiles(tl) if ok else "") + wc + ct
        sub = f'AM {esc(c["am"]) or "—"} · account <span class="mono">{esc(r["ad_account_id"])}</span>'
        chtml.append(_card(c, sub, status_badge(r["status"].replace("_", " ")), "n/a" if not ok else _money(_f(r["total_live"])), "per day", inner))
    fbar, data = _filter(clients)

    # 04 notes
    pre = paras(S["_pre"]); rl = run_line(S)
    tab = next((p_ for p_ in pre if p_.startswith("Meta Ad Spends tab:")), "")
    notes = _notes([("Run", "".join(f'<p class="np">{inline(p_)}</p>' for p_ in (rl, tab) if p_)),
                    ("Method and scope", _ul(bullets(S["Footer"])))])
    body = f"""
{data}
<div class="card band" style="--n:{len(tiles)}">{band}</div>
{_stoggle("overview", "01", "Overview", "Live budget by client", "Every client in the map, highest live daily budget first, with what changed since the last run or the budget by campaign type. Click a row for the client's campaigns.", badge("gray", _plural(len(clients), "client")), f'<div class="card">{_overview(otr, "Live $/day")}</div>')}
<section class="sec" id="lists">
{_sec_top("02", "Lists", "Changes and idle accounts", "Open a list to see its rows.")}
<div class="stack">{lists}</div>
</section>
{_stoggle("clients", "03", "Per client", "Client detail", "Every client, in the overview's order. Filter by account manager or client, then open a card for the budget by campaign type, the 7-day spend and the live campaigns.", badge("gray", _plural(len(clients), "client")), fbar + f'<div class="cards">{"".join(chtml)}</div>')}
{_stoggle("notes", "04", "Notes", "Run and method notes", "When the budgets were read, the Meta Ad Spends tab update, and how campaigns are bucketed.", badge("gray", _plural(len(bullets(S["Footer"])), "note")), notes)}
{GENLINE.format(run=RUN)}
"""
    w0, w1 = _d - datetime.timedelta(days=7), _d - datetime.timedelta(days=1)
    lede = f"Live budgets on {_d.day} {_d:%b %Y} · spend {_span(w0, w1)}"
    return page(f"Ad spend check {WEEK}", "", "Ad Spend Check", esc(lede), [], body, js=SPEND_JS, css=BENCH_CSS + REVIEW_CSS)

def build_spend_legacy(md, rows):
    """Reports up to 2026-10-13: documented sheet budget vs live, with Match / Warning / Critical flags."""
    S = sections(md)
    cnt = collections.Counter(r["flag"] for r in rows)
    live = [r for r in rows if r["sheet_status"] == "Live"]
    documented = sum(_f(r["sheet_daily_budget"]) for r in live)
    liveread = [r for r in rows if r["source"] == "live"]
    confirmed = sum(_f(r["actual_daily_budget"]) for r in liveread); doc_same = sum(_f(r["sheet_daily_budget"]) for r in liveread)
    n_csv = sum(1 for r in rows if r["source"] == "csv")
    tiles = [("Clients on sheet", str(len(rows)), f"{len(live)} live, {len(rows)-len(live)} not live or paused", None),
             ("Live connector reads", str(len(liveread)), f"{n_csv} from the CSV export, {cnt.get('blocker',0)} blocked", None),
             ("Documented live $/day", _money(documented), "Master sheet, Live rows", None),
             ("Confirmed live $/day", _money(confirmed), f"vs {_money(doc_same)} documented for the same accounts", None),
             ("Critical", str(cnt["critical"]), "over 25% off, or spend on a dark account", "err"),
             ("Warning", str(cnt["warning"]), "10 to 25% off, or a sheet note", "warn"),
             ("Match", str(cnt["match"]), "within 10% or $5", "ok"),
             ("Blocked", str(cnt.get("blocker", 0)), "unreadable and absent from the export", "gray")]
    band = "".join(stat(l, v, h, dot=d) for l, v, h, d in tiles)
    clients = sorted(({"name": r["client"], "am": r["am"], "r": r} for r in rows), key=lambda c: (-_f(c["r"]["actual_daily_budget"]), c["name"].lower()))
    for i, c in enumerate(clients): c["id"] = f"client-{i}"
    card_id = {c["name"]: c["id"] for c in clients}
    href = lambda cell: (f"#{card_id[cell.strip()]}" if cell.strip() in card_id else None)
    otr = [_ovw_row(c, one_liner(c["r"]["notes"]) or "—", flagword_badge(c["r"]["flag"]),
                    _money(_f(c["r"]["actual_daily_budget"])) if c["r"]["actual_daily_budget"] != "" else "—") for c in clients]
    it_rows = tables(S["Issues, action needed"])[0][1:]
    it = render_table("issues", ["Client", "AM", "Flag", "Sheet $/day", "Actual $/day", "Status vs last week", "Next action"], it_rows,
                      ["first", "text", "badge", "num", "num", "nowrap", "notes"], flag_col=2, flag_map=flag_sym, first_href=href)
    ic = collections.Counter(flag_sym(r[2]) for r in it_rows if len(r) > 2)
    imeta = "".join(badge(k, f"{ic[k]} {l}") for k, l in (("err", "critical"), ("warn", "warning"), ("gray", "blocked")) if ic[k])
    fixed_lines = S.get("Fixed since last week", []); ft = tables(fixed_lines)
    fmeta = badge("ok", _plural(len(ft[0]) - 1, "row")) if ft and len(ft[0]) > 1 else ""
    notsheet = paras(S.get("Not on the sheet", []))
    lists = (_toggle("issues", "Issues, action needed", "Critical rows first, then warnings. Each row carries a next action for the account manager.", imeta, it)
             + _toggle("fixed", "Fixed since last week", "Rows flagged last week that match this week.", fmeta, fixed_html(S))
             + (_toggle("notsheet", "Active accounts with no Master sheet row", "Accounts with spend that the sheet does not list yet.", "", f'<div class="card-body"><p class="np">{inline(notsheet[0])}</p></div>') if notsheet else ""))
    chtml = []
    for i, c in enumerate(clients):
        r = c["r"]
        tl = [("Sheet $/day", _money(_f(r["sheet_daily_budget"])) if r["sheet_daily_budget"] != "" else "—", f"Master sheet, {r['sheet_status'] or '—'}"),
              ("Actual $/day", _money(_f(r["actual_daily_budget"])) if r["actual_daily_budget"] != "" else "—", f"source: {r['source']}"),
              ("Spent last 7 days", _money(_f(r["spend_7d"])) if r["spend_7d"] != "" else "—", "")]
        st = {"new": "New flag", "still_open": f"Still open, week {r['weeks_open']}", "fixed": "Fixed", "unchanged": "Unchanged", "first_run": "First run"}.get(r["diff_status"], r["diff_status"])
        inner = _tiles(tl) + f'<dl class="kv"><dt>Vs last week</dt><dd>{esc(st) or "—"}</dd><dt>Notes</dt><dd>{inline(r["notes"]) or "—"}</dd></dl>'
        sub = f'AM {esc(c["am"]) or "—"} · account <span class="mono">{esc(r["ad_account_id"])}</span>'
        chtml.append(_card(c, sub, flagword_badge(r["flag"]), _money(_f(r["actual_daily_budget"])) if r["actual_daily_budget"] != "" else "—", "actual per day", inner))
    fbar, data = _filter(clients)
    rl = run_line(S)
    notes = _notes([("Run", f'<p class="np">{inline(rl)}</p>' if rl else ""), ("Method and scope", _ul(bullets(S["Footer"])))])
    body = f"""
{data}
<div class="card band" style="--n:{len(tiles)}">{band}</div>
{_stoggle("overview", "01", "Overview", "Sheet budget vs live", "Every client on the Master sheet, highest live daily budget first, with the flag and the opening line of its note. Click a row for the detail.", badge("gray", _plural(len(clients), "client")), f'<div class="card">{_overview(otr, "Actual $/day")}</div>')}
<section class="sec" id="lists">
{_sec_top("02", "Lists", "Issues and fixes", "Open a list to see its rows.")}
<div class="stack">{lists}</div>
</section>
{_stoggle("clients", "03", "Per client", "Client detail", "Every client, in the overview's order. Filter by account manager or client, then open a card for the sheet and live budgets and the note.", badge("gray", _plural(len(clients), "client")), fbar + f'<div class="cards">{"".join(chtml)}</div>')}
{_stoggle("notes", "04", "Notes", "Run and method notes", "When the budgets were read and how the flags are set.", badge("gray", _plural(len(bullets(S["Footer"])), "note")), notes)}
{GENLINE.format(run=RUN)}
"""
    lede = f"Sheet vs live budgets on {_d.day} {_d:%b %Y}"
    return page(f"Ad spend check {WEEK}", "", "Ad Spend Check", esc(lede), [], body, js=SPEND_JS, css=BENCH_CSS + REVIEW_CSS)

def build_spend():
    md=open(f"{ROOT}/Ad Spends Checks/Weekly Checks/{DATE}-ad-spend-check.md",encoding="utf-8").read()
    rows=list(csv.DictReader(open(f"{ROOT}/Ad Spends Checks/Weekly Checks/{DATE}-ad-spend-check.csv",encoding="utf-8")))
    if rows and "total_live" in rows[0] and "status" in rows[0]: return build_spend_v2(md, rows)
    return build_spend_legacy(md, rows)

# =====================================================================
# 2. PIXEL DOMAIN CHECK
# =====================================================================
PFLAG = {"critical": ("err", "Purchase critical"), "warning": ("warn", "Purchase warning")}
DIFFWORD = {"new": "New", "fixed": "Fixed", "unchanged": "Unchanged", "first_run": "First run", "removed": "Removed"}
def _diffword(r):
    if r.get("diff_status") == "still_open": return f"Still open, week {r.get('weeks_open') or '?'}"
    return DIFFWORD.get(r.get("diff_status", ""), r.get("diff_status", "") or "—")

def pixel_table(tid, prs, purchase_era):
    """One tbody per pixel: numbers on one row, the notes under it (same pattern as the benchmark's campaign table)."""
    hdr = ["Pixel", "Events (7d)"] + (["Purchase (28d, b / s)"] if purchase_era else []) + ["Domains seen", "Expected", "Match", "Vs last week"]
    th = "".join(f'<th{" class=num" if h == "Events (7d)" else ""}>{esc(h)}</th>' for h in hdr)
    bodies = []
    for r in prs:
        ev = int(_f(r["events_7d"]))
        pur = ""
        if purchase_era:
            p28 = int(_f(r.get("purchase_28d"))); pb = r.get("purchase_28d_browser") or 0; ps_ = r.get("purchase_28d_server") or 0
            pcell = f"{p28:,} ({pb}b / {ps_}s)" if p28 else "0"
            pur = f'<td class=nowrap data-l="Purchase (28d, b / s)">{pcell}</td>'
        tds = (f'<td class=pid>{esc(r["pixel_name"])}<span class="mono">{esc(r["pixel_id"])}</span></td>'
               f'<td class=num data-l="Events (7d)">{ev:,}</td>{pur}'
               f'<td class=dom data-l="Domains seen">{esc(r["domains_seen"].replace("|", ", ")) or "none"}</td>'
               f'<td class=dom data-l="Expected">{esc(r["expected_domains"].replace("|", ", "))}{" <span class=mono>(" + esc(r["expected_source"]) + ")</span>" if r.get("expected_source") else ""}</td>'
               f'<td class=nowrap data-l="Match">{flagword_badge(r["flag"])}</td><td class=status data-l="Vs last week">{esc(_diffword(r))}</td>')
        det = f'<tr class=cdet><td colspan={len(hdr)}><div class=cdl><p><span>Notes</span>{inline(r["notes"])}</p></div></td></tr>' if r["notes"].strip() else ""
        bodies.append(f'<tbody><tr class=crow>{tds}</tr>{det}</tbody>')
    return f'<div class="tablewrap"><table class="ctable" id="{tid}"><thead><tr>{th}</tr></thead>{"".join(bodies)}</table></div>'

def build_pixel():
    md = open(f"{ROOT}/Meta Pixel Reviews/Weekly Checks/{DATE}-pixel-domain-check.md", encoding="utf-8").read()
    S = sections(md)
    rows = list(csv.DictReader(open(f"{ROOT}/Meta Pixel Reviews/Weekly Checks/{DATE}-pixel-domain-check.csv", encoding="utf-8")))
    purchase_era = bool(rows) and "purchase_flag" in rows[0]
    spend = _spend_by_client()
    cnt = collections.Counter(r["flag"] for r in rows)
    seen = set(); tot = 0
    for r in rows:
        if r["pixel_id"] in seen: continue
        seen.add(r["pixel_id"]); tot += int(_f(r["events_7d"]))
    m_cs = re.search(r"\*\*Clients on sheet:\*\*\s*([^·]+?)\s*·", md)
    cs_txt = m_cs.group(1).strip() if m_cs else str(len({r["client"] for r in rows}))
    m2 = re.match(r"^(\d+)\s*(.*)$", cs_txt); cs_n, cs_sub = (m2.group(1), m2.group(2).strip()) if m2 else (cs_txt, "")
    if cs_sub.startswith("(") and cs_sub.endswith(")") and cs_sub.count("(") == 1: cs_sub = cs_sub[1:-1]
    pflags = collections.Counter(r.get("purchase_flag", "") for r in rows) if purchase_era else collections.Counter()
    tiles = [("Clients on sheet", cs_n, cs_sub or "matched to at least one pixel", None),
             ("Pixel rows", str(len(rows)), f"{len(seen)} distinct pixels", None),
             ("Events, last 7 days", f"{tot:,}", "each shared pixel counted once", None),
             ("Critical", str(cnt["critical"]), "another client's domain on the pixel", "err"),
             ("Warning", str(cnt["warning"]), "silent, split, duplicate or unconfirmed", "warn"),
             ("Match", str(cnt["match"]), "only the client's own hosts", "ok"),
             ("Blocked", str(cnt.get("blocker", 0)), "no pixel found or unreadable", "gray")]
    if purchase_era: tiles.append(("Purchase flags", str(pflags["critical"] + pflags["warning"]), f"{pflags['critical']} critical, {pflags['warning']} warning, 28 days", "warn"))
    band = "".join(stat(l, v, h, dot=d) for l, v, h, d in tiles)

    # clients: pixel rows grouped by client, ordered by the client's live $/day (same order as the ad spend page)
    by = collections.OrderedDict()
    for r in rows: by.setdefault(r["client"], []).append(r)
    clients = []
    for name, prs in by.items():
        am, usd = spend.get(_norm(name), ("", None))
        worst = min(prs, key=lambda r: FLAG_ORDER.index(r["flag"]) if r["flag"] in FLAG_ORDER else 9)
        ev = sum(int(_f(r["events_7d"])) for r in {r["pixel_id"]: r for r in prs}.values())
        judged = next((r for r in prs if r.get("purchase_flag") not in ("", "see", None)), prs[0]) if purchase_era else None
        clients.append({"name": name, "am": am, "usd": usd, "prs": prs, "worst": worst, "events": ev, "judged": judged})
    clients.sort(key=lambda c: (c["usd"] is None, -(c["usd"] or 0), c["name"].lower()))
    for i, c in enumerate(clients): c["id"] = f"client-{i}"
    card_id = {c["name"]: c["id"] for c in clients}
    href = lambda cell: (f"#{card_id[cell.strip()]}" if cell.strip() in card_id else None)
    am_of = {c["name"]: c["am"] for c in clients}
    def states(c):
        fl = collections.Counter(r["flag"] for r in c["prs"])
        out = "".join(badge(FLAGWORD[f][0], (f"{fl[f]} " if fl[f] > 1 else "") + FLAGWORD[f][1]) for f in FLAG_ORDER if fl[f])
        j = c["judged"]
        if j is not None and j.get("purchase_flag") in PFLAG: out += badge(*PFLAG[j["purchase_flag"]])
        return out

    # 01 overview
    otr = [_ovw_row(c, one_liner(c["worst"]["notes"]) or "—", states(c), _money(c["usd"]) if c["usd"] is not None else "—") for c in clients]

    # 02 lists
    def issue_table(tid, sel):
        trs = [[r["client"], am_of.get(r["client"], "") or "—", r["pixel_id"], f'{int(_f(r["events_7d"])):,}', FLAGWORD.get(r["flag"], ("", r["flag"]))[1], _diffword(r), r["notes"]] for r in sel]
        return render_table(tid, ["Client", "AM", "Pixel ID", "Events (7d)", "Match", "Vs last week", "Notes" if tid == "fixed" else "Issue and next action"], trs,
                            ["first", "text", "mono", "num", "badge", "status", "notes"], badge_fn=lambda s: badge({"Critical": "err", "Blocked": "gray", "Warning": "warn", "Match": "ok"}.get(s, "gray"), s), first_href=href) if trs else '<div class="empty">None this week.</div>'
    crit = [r for r in rows if r["flag"] in ("critical", "blocker")]; warn = [r for r in rows if r["flag"] == "warning"]
    crit_paras = [p for p in paras(S.get("Critical issues (❌ and 🔴)", [])) if not re.match(r"^\d+\. ", p)]
    cmeta = "".join(badge(k, f"{n} {l}") for k, l, n in (("err", "critical", cnt["critical"]), ("gray", "blocked", cnt.get("blocker", 0))) if n)
    wnew = sum(1 for r in warn if r["diff_status"] == "new")
    wmeta = (badge("warn", _plural(len(warn), "warning")) + (badge("gray", f"{wnew} new") if wnew else "")) if warn else ""
    lists = (_toggle("crit", "Critical and blocked", inline(crit_paras[0]) if crit_paras else "Another client's domain firing into the pixel, or no readable pixel.", cmeta, issue_table("crit", crit))
             + _toggle("warn", "Warnings", "Silent or low-volume pixels, split funnels, double counting, pixels not shared to the ad account, and expected domains to confirm.", wmeta, issue_table("warn", warn)))
    if "Purchase check (last 28 days)" in S:
        pl = S["Purchase check (last 28 days)"]; pt = tables(pl)
        if pt:
            # compact: the pixel ID, 7-day count and last Purchase are in the client card
            phdr = ["Client", "AM", "Purchase 28d (b / s)", "PMS online 28d", "Capture", "Flag", "Why"]
            prow = [[r[0], am_of.get(r[0].strip(), "") or "—", r[2], r[5], r[6], r[9], r[10]] for r in pt[0][1:] if len(r) >= 11]
            ptab = render_table("purchase", phdr, prow, ["first", "text", "nowrap", "num", "nowrap", "badge", "notes"], flag_col=5, flag_map=flag_sym, first_href=href)
        else: ptab = '<div class="empty">No client flagged on Purchase this week.</div>'
        pmeta = "".join(badge(k, f"{n} {l}") for k, l, n in (("err", "critical", pflags["critical"]), ("warn", "warning", pflags["warning"])) if n)
        lists += _toggle("purchase", "Purchase check, last 28 days", "Purchase events against the PMS online bookings of the same 28 days, for clients with a Sales budget. Critical first.", pmeta, ptab)
    fixed = [r for r in rows if r["diff_status"] == "fixed"]
    if fixed:
        ftab = issue_table("fixed", fixed)
    else:
        fps = paras(S.get("Fixed since last week", [])); ftab = f'<div class="empty">{inline(fps[0]) if fps else "Nothing fixed since last week."}</div>'
    lists += _toggle("fixed", "Fixed since last week", "Pixel rows flagged last week that are clean this week, with what changed.", badge("ok", _plural(len(fixed), "row")) if fixed else "", ftab)

    # 03 per client
    chtml = []
    for i, c in enumerate(clients):
        prs = c["prs"]; j = c["judged"]; inner = ""
        if purchase_era and j is not None:
            p28 = int(_f(j.get("purchase_28d"))); onl = j.get("pms_online_bookings_28d", "")
            cap = f"{p28/_f(onl)*100:.0f}% capture" if onl not in ("", None) and _f(onl) > 0 else "no PMS bookings to compare"
            inner += _tiles([("Purchase, 28 days", f"{p28:,}", f"{j.get('purchase_28d_browser') or 0} browser / {j.get('purchase_28d_server') or 0} server"),
                             ("Purchase, 7 days", str(int(_f(j.get("purchase_7d")))), f"last {j.get('purchase_last') or '—'}"),
                             ("PMS online bookings, 28 days", onl if onl not in ("", None) else "—", cap),
                             ("Sales budget", _money(_f(j.get("sales_budget_per_day"))) if j.get("sales_budget_per_day") not in ("", None) else "—", "per day, BoF + LoL"),
                             ("HG AI CAPI", j.get("hgai_capi") or "—", "platform Conversions API")])
            if j.get("purchase_flag") in PFLAG and j.get("purchase_note"):
                inner += f'<div class="tof"><strong>Purchase check: {esc(PFLAG[j["purchase_flag"]][1].split()[1])}.</strong> {inline(j["purchase_note"])}</div>'
        inner += pixel_table(f"p{i}", prs, purchase_era)
        n_px = len({r["pixel_id"] for r in prs})
        sub = f'AM {esc(c["am"]) or "—"} · {_plural(n_px, "pixel")}' + (f' · {_money(c["usd"])}/day live' if c["usd"] is not None else "")
        chtml.append(_card(c, sub, states(c), f'{c["events"]:,}', "events, 7 days", inner))
    fbar, data = _filter(clients)

    # 04 notes: the week in brief (prose from the report) and the method
    brief = [p for p in paras(S.get("Warnings (⚠️)", [])) if not p[:1].isdigit()] + crit_paras[1:]
    notes = _notes([("This week", "".join(f'<p class="np">{inline(p)}</p>' for p in brief)), ("Method and scope", _ul(bullets(S["Footer"])))])
    body = f"""
{data}
<div class="card band" style="--n:{len(tiles)}">{band}</div>
{_stoggle("overview", "01", "Overview", "Pixel status by client", "Every client with a pixel row, highest live daily budget first (the ad spend check's order), with the domain flags, the Purchase flag and the opening line of the worst row's note. Click a row for the client's pixels.", badge("gray", _plural(len(clients), "client")), f'<div class="card">{_overview(otr, "Live $/day")}</div>')}
<section class="sec" id="lists">
{_sec_top("02", "Lists", "Issues, Purchase check and fixes" if purchase_era else "Issues and fixes", "Open a list to see its rows.")}
<div class="stack">{lists}</div>
</section>
{_stoggle("clients", "03", "Per client", "Client detail", "Every client, in the overview's order. Filter by account manager or client, then open a card for the Purchase numbers and each pixel's events, domains and notes.", badge("gray", _plural(len(clients), "client")), fbar + f'<div class="cards">{"".join(chtml)}</div>')}
{_stoggle("notes", "04", "Notes", "This week and method notes", "What moved this week, and how pixels, domains and Purchase volume are judged.", badge("gray", _plural(len(bullets(S["Footer"])), "note")), notes)}
{GENLINE.format(run=RUN)}
"""
    w0 = _d - datetime.timedelta(days=7)
    lede = f"Events {_span(w0, _d)}" + (" · Purchase over 28 days" if purchase_era else "")
    return page(f"Pixel domain check {WEEK}", "", "Pixel Domain Check", esc(lede), [], body, js=PIXEL_JS, css=BENCH_CSS + REVIEW_CSS)

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
    old=re.match(r"^none dropped in[^.]*\.\s*",t,flags=re.I)   # notes format before 26 Oct
    if old:
        t=t[old.end():]
        if not re.search(r"\d+(?:\.\d+)?x\b|\$[\d,]+|purchase|CPL|\bleads?\b",t): return ""   # a meeting aside, not a weekly read
    sents=[x for x in re.split(r"(?<=[.!?])\s+(?=[A-Z(\"$])",t) if x]
    if not sents: return ""
    out=sents[0]
    if len(out)<50 and len(sents)>1: out+=" "+sents[1]
    for k in FLAG: out=out.replace(k,"")
    out=re.sub(r"\(\s+",  "(", re.sub(r"\s+\)", ")", out))
    return out[:1].upper()+out[1:]

SHORT_TYPE = {"Retargeting (BoF)":"BoF","Lead Gen (MoF)":"Lead Gen","Prospecting (MoF lookalike)":"Lookalike","Sales (MoF lookalike)":"Lookalike","Sales":"Sales"}
STATE_SHORT = {"Flag to Shawal":"Flag","Review w/ HG AI":"Review","Monitor":"Monitor","Healthy":"Healthy","Scale w/ HG AI":"Scale"}
def rows_summary(crows):
    """One line from a client's CSV rows: each scored campaign's metric and state, worst first."""
    order={s:i for i,s in enumerate(SCORED_ORDER)}
    scored=sorted([r for r in crows if r["state"] in order],key=lambda r:(order[r["state"]],-float(r["spend"] or 0)))
    parts=[]
    for r in scored[:3]:
        v=r.get("governing_value") or ""
        if r.get("governing_metric")=="cpl": m=f"${float(v):.2f} CPL" if v else "no leads"
        else: m=f"{float(v):.1f}x ROAS" if v else "0 purchases"
        parts.append(f"{SHORT_TYPE.get(r['type'],r['type'])} {m}, {STATE_SHORT[r['state']]}")
    if scored[3:]: parts.append(f"+{len(scored)-3} more")
    if parts: return "; ".join(parts)+"."
    gate=sum(1 for r in crows if r["state"]=="Under gate")
    return f"All {gate} campaign{'s' if gate!=1 else ''} under the spend gate." if gate else ""

def state_badges(states):
    """One badge per scored state a client has this week, worst first; '2 Healthy' when repeated."""
    c=collections.Counter(states)
    out=[badge(STATE[s], (f"{c[s]} " if c[s]>1 else "")+s) for s in SCORED_ORDER if c[s]]
    if out: return "".join(out)
    return badge("gray","Under gate") if c["Under gate"] else badge("gray","Not scored")

def client_table(tid, hdr_row, trs):
    """Per-client campaign table: the numbers on one row, diagnostics and notes on a line under it.
    One <tbody> per campaign so hover and dividers treat the pair as one; stacks into labelled fields on phones."""
    keys=["campaign","type","window","spend","results","governing","frequency","state","diagnostics","notes","change"]
    pos={k:next((i for i,h in enumerate(hdr_row) if h.strip().lower().startswith(k)),None) for k in keys}
    has_f=pos["frequency"] is not None
    hdr=["Campaign","Type","Window","Spend","Results","Governing metric"]+(["Frequency"] if has_f else [])+["State","Change vs last week"]
    th="".join(f'<th{" class=num" if h in ("Spend","Results","Governing metric","Frequency") else ""}>{esc(h)}</th>' for h in hdr)
    def num(c):
        return badge("warn"," ".join(c.replace("⚠️"," ").split())) if "⚠️" in c else inline(c)
    bodies=[]   # columns found by header name: reports before 2026-10-06 have no Frequency column
    for r in trs:
        get=lambda k:(r[pos[k]] if pos[k] is not None and pos[k]<len(r) else "")
        camp,typ,win,spend,res,gov,freq,st,diag,notes,chg=(get(k) for k in keys)
        tds=(f'<td class=first>{inline(camp)}</td>'
             f'<td class=type data-l="Type">{inline(typ)}</td>'
             f'<td class=nowrap data-l="Window">{inline(win)}</td>'
             f'<td class=num data-l="Spend">{inline(spend)}</td>'
             f'<td class="num res" data-l="Results">{inline(res)}</td>'
             f'<td class="num gov" data-l="Governing metric">{inline(gov)}</td>'
             +(f'<td class=num data-l="Frequency">{num(freq)}</td>' if has_f else '')+
             f'<td class=nowrap data-l="State">{state_badge(st.strip())}</td>'
             f'<td class=status data-l="Change vs last week">{inline(chg)}</td>')
        det=[(l,v) for l,v in (("Diagnostics",diag),("Notes",notes)) if v.strip() and v.strip()!="—"]
        dh="".join(f"<p><span>{l}</span>{inline(v)}</p>" for l,v in det)
        bodies.append(f'<tbody data-flag="{flag_state(st)}"><tr class=crow>{tds}</tr>'+(f'<tr class=cdet><td colspan={len(hdr)}><div class=cdl>{dh}</div></td></tr>' if det else "")+'</tbody>')
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
    rows_by_client=collections.defaultdict(list)
    for r in rows: rows_by_client[r["client"]].append(r)
    has_blended=any(p.startswith("Blended 30d") for c in clients for p in c["ps"])
    if not has_blended:   # reports before 30 Oct: no all-campaign 30-day spend line
        for c in clients: c["spend"]=round(sum(float(r["spend"] or 0) for r in rows_by_client[c["name"]]))
    for c in clients:
        if not c["summary"]: c["summary"]=rows_summary(rows_by_client[c["name"]])
    spend_hdr,spend_sub=("Spend, 30 days","spend, 30 days") if has_blended else ("Spend in scoring windows","spend, scoring windows")
    # Lead Gen campaigns carried a CPL state until the 28 Oct / 4 Nov rule changes
    lead_era=any(r["type"].startswith("Lead Gen") and r["state"] in SCORED_ORDER for r in rows)
    has_freq=bool(rows) and "freq_flag" in rows[0]
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
        +stat("Flag to Shawal",str(cnt["Flag to Shawal"]),"CPL $2.50+ or no leads; ROAS under 2x" if lead_era else "Under 2x or no purchases",dot="err",key="flag")
        +stat("Review w/ HG AI",str(cnt["Review w/ HG AI"]),"CPL $1.00–2.50; ROAS 2–5x" if lead_era else "2 to 5x",dot="warn",key="review")
        +stat("Monitor",str(cnt["Monitor"]),"CPL $0.50–1.00; ROAS 5–8x" if lead_era else "5 to 8x",dot="gray",key="monitor")
        +stat("Healthy",str(cnt["Healthy"]),"CPL $0.30–0.50; ROAS 8–15x" if lead_era else "8 to 15x",dot="ok",key="healthy")
        +stat("Scale w/ HG AI",str(cnt["Scale w/ HG AI"]),"CPL under $0.30; ROAS above 15x" if lead_era else "Above 15x",dot="brand",key="scale")
        +(stat("Frequency over 5",str(sum(1 for r in rows if r.get("freq_flag")=="yes")),"Refresh creative",dot="warn",key="freq") if has_freq else ""))
    n_tiles=8 if has_freq else 7

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
    overview=(f'<div class="tablewrap"><table id="ovw" data-ftable><thead><tr><th>Client</th><th>AM</th><th>Summary</th><th>State</th><th class=num>{spend_hdr}</th></tr></thead>'
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
        if tbls: tbl=client_table(tid,tbls[0][0],tbls[0][1:])
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
<summary><span class="chev" aria-hidden="true"></span><span class="cmain"><span class="cname">{esc(name)}</span><span class="csub">AM {esc(am)} · {esc(acct_name)} <span class="mono">{esc(acct_id)}</span></span></span><span class="cstates">{src_badge}{state_badges(states_by_client.get(name,[]))}</span><span class="cspend">{spend}<small>{spend_sub}</small></span></summary>
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
    notes_meta=badge("gray", m_lbl)+badge("gray", f"{len(foot)} method notes")
    notes_inner=f"""<div class="nbody">
<div><h4>Weekly Meta Ads meetings since last run</h4><p class="sec-desc">Notes by Gemini attached to the calendar events, read via Drive. Summary, decisions and next steps as Gemini wrote them; client-specific sentences are also pulled into each client's card. Transcript not used.</p>{meet_block}</div>
<div><h4>How states are assigned</h4><p class="np">{inline(states_para[0]) if states_para else "—"}</p></div>
<div><h4>Method and scope</h4><ul class="nl">{"".join(f"<li>{inline(b)}</li>" for b in foot)}</ul></div>
</div>"""

    # ---------- filter bar for the client detail section (filters the client cards only; shown by the script)
    am_counts=collections.Counter(c["am"] for c in clients if c["am"])
    am_opts="".join(f'<option value="{attr(a)}">{esc(a)} ({n})</option>' for a,n in sorted(am_counts.items()))
    cl_opts="".join(f'<option value="{attr(n)}">{esc(n)}</option>' for n in sorted((c["name"] for c in clients),key=str.lower))
    fbar=f"""<div class="fbar" id="fbar" role="search" aria-label="Filter client detail" hidden>
<div class="fld"><label for="f-am">Account manager</label><span class="sel"><select id="f-am"><option value="all">All account managers</option>{am_opts}</select></span></div>
<div class="fld"><label for="f-client">Client</label><span class="sel"><select id="f-client"><option value="all">All clients</option>{cl_opts}</select></span></div>
<button type="button" class="btn" id="f-clear" hidden>Clear filters</button>
<p class="fsum" id="f-sum" aria-live="polite">{len(clients)} clients across {len(am_counts)} account managers</p>
<button type="button" class="btn" id="x-all">Expand all</button>
</div>"""
    data=json.dumps({"clients":[{"n":c["name"],"a":c["am"]} for c in sorted(clients,key=lambda c:c["name"].lower())]},ensure_ascii=False).replace("</","<\\/")

    def sec_top(n, eyebrow, title, desc, actions=""):
        return f'<div class="sec-top"><div><span class="eb">{n} · {esc(eyebrow)}</span><h2>{esc(title)}</h2><p class="sec-desc">{desc}</p></div>{actions}</div>'
    def stoggle(sid, n, eyebrow, title, desc, meta, inner):
        """A whole section that opens and closes from its own heading."""
        return f"""<details class="sec stgl" id="sec-{sid}">
<summary><span class="eb">{n} · {esc(eyebrow)}</span><span class="shead"><span class="chev" aria-hidden="true"></span><h2>{esc(title)}</h2><span class="tact" aria-hidden="true"></span></span><span class="sec-desc">{desc}</span><span class="smeta">{meta}</span></summary>
{inner}
</details>"""
    n_all=len(clients)+len(unmapped)
    ovw_meta=badge("gray",f"{n_all} clients")+(badge("gray",f"{len(unmapped)} without an ad account") if unmapped else "")
    body=f"""
<script type="application/json" id="bench-data">{data}</script>
<div class="card band" style="--n:{n_tiles}">{band}</div>
{stoggle("overview","01","Overview","One-liner summary (advanced clients)",("Every CRM-Advanced client, highest 30-day ad spend first (all HiddenGem campaigns). State shows this week's scored Sales campaigns, worst first; the summary is the opening line of the client's notes. Click a row for the full detail." if has_blended else "Every CRM-Advanced client, highest spend first (scored campaigns: Lead Gen over 30 days, Sales over 14 days). State shows this week's scored campaigns, worst first; the summary lists them. Click a row for the full detail."),ovw_meta,f'<div class="card">{overview}</div>')}
<section class="sec" id="lists">
{sec_top("02","Campaign lists","Action needed, scale and frequency" if fkey else "Action needed and scale","Lead Gen (CPL) and Sales (ROAS) campaigns. Open a list to see its rows." if lead_era else "Sales-objective campaigns only. Open a list to see its rows.")}
<div class="stack">
{toggle("act","Action needed","Flag to Shawal before Review w/ HG AI, highest spend first.",tmeta("act",act_rows,6,"states"),act)}
{toggle("scale","Scale candidates","Campaigns above the Scale line. Full context goes to HG AI, which picks where budget goes.",tmeta("scale",sc_rows,6,"count","brand"),sc)}
{toggle("freq","Frequency watch","14-day frequency above 5.0. Frequency does not change the ROAS state; this is the list to refresh creative or widen the audience on.",tmeta("freq",frows,7,"count","warn"),fw) if fkey else ""}
</div>
</section>
{stoggle("clients","03","Per client","Client detail","Every client with an ad account, in the overview's order. Filter by account manager or client, then open a card for this month's bookings, the campaign table, monthly ROI and notes.",badge("gray",f"{len(clients)} clients"),fbar+f'<div class="cards">{"".join(chtml)}</div>')}
{stoggle("notes","04","Notes","Meeting summary and report notes","This week's Meta Ads meeting notes, how states are assigned, and the method behind the numbers.",notes_meta,f'<div class="card">{notes_inner}</div>')}
<p class="genline">HiddenGem Marketing · weekly Meta Ads review · generated {RUN} from the saved report and CSV sidecar.</p>
"""
    # Header: the 14-day scoring window only. The pulls use Meta's last_14d preset, which ends the day before the run.
    w0,w1=_d-datetime.timedelta(days=30 if lead_era else 14),_d-datetime.timedelta(days=1)
    span=(f"{w0.day} {w0:%b} – {w1.day} {w1:%b %Y}" if w0.year==w1.year else f"{w0.day} {w0:%b %Y} – {w1.day} {w1:%b %Y}")
    return page(f"Client benchmark {WEEK}","","Meta Ads Weekly Review",esc(span),[],body,js=BENCH_JS,css=BENCH_CSS)


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
