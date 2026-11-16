"""HTML report builder for the three weekly Meta Ads reviews.
Styled from the HiddenGem Media design system (claude.ai/artifact/GXb4YMfP8uFmoTPhnWujSk):
Inter + Roboto Mono, neutral canvas, brand blue #0066DE for accents, semantic badges, no emoji.
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
  color-scheme:light;
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
  color-scheme:dark;
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
.masthead .eyebrow{font:500 12px/18px 'Roboto Mono',ui-monospace,monospace;letter-spacing:.04em;text-transform:uppercase;color:var(--text-4)}
header.title{display:flex;flex-direction:column;gap:8px;margin-bottom:24px}
h1{font:600 30px/38px 'Inter',sans-serif;letter-spacing:-.02em;margin:0;text-wrap:balance}
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
.fbar[hidden],.fbar [hidden],.tgl [hidden],.cards>[hidden]{display:none!important}
td.camp{min-width:180px}
td.type{min-width:110px}
td.status{min-width:140px;font-size:13px;line-height:19px;color:var(--text-3)}
.tgl thead th,.tgl tbody td{padding-left:12px;padding-right:12px}
.tgl thead th:first-child,.tgl tbody td:first-child{padding-left:20px}.tgl thead th:last-child,.tgl tbody td:last-child{padding-right:20px}
.tgl td.first{white-space:normal;min-width:120px}
td.first a{color:inherit}td.first a:hover{color:var(--brand-text)}
/* client benchmark: filter bar */
.fbar{position:sticky;top:12px;z-index:10;display:flex;flex-wrap:wrap;align-items:flex-end;gap:12px 16px;padding:14px 18px;margin:0 0 20px;background:var(--panel);border:1px solid var(--border);border-radius:12px;box-shadow:0 4px 12px -2px rgba(10,13,18,.10),var(--shadow-xs)}
.fld{display:flex;flex-direction:column;gap:4px;min-width:0}
.fld label{font:500 12px/18px 'Inter',sans-serif;color:var(--text-3)}
.sel{position:relative;display:block}
.sel::after{content:"";position:absolute;right:14px;top:50%;width:7px;height:7px;border-right:1.5px solid var(--text-3);border-bottom:1.5px solid var(--text-3);transform:translateY(-70%) rotate(45deg);pointer-events:none}
.sel select{appearance:none;-webkit-appearance:none;width:100%;min-width:220px;font:500 14px/20px 'Inter',sans-serif;color:var(--text);background:var(--panel);border:1px solid var(--border-strong);border-radius:8px;padding:8px 36px 8px 12px;cursor:pointer;box-shadow:var(--shadow-xs)}
.sel select:hover{border-color:var(--text-4)}
.sel select:focus-visible{outline:none;border-color:var(--brand);box-shadow:var(--focus)}
.sel select.on{border-color:var(--brand);background:var(--brand-bg);color:var(--brand-text)}
.btn{appearance:none;display:inline-flex;align-items:center;gap:6px;min-height:38px;padding:0 14px;border:1px solid var(--border-strong);border-radius:8px;background:var(--panel);color:var(--text-2);font:500 14px/20px 'Inter',sans-serif;cursor:pointer;box-shadow:var(--shadow-xs)}
.btn:hover{background:var(--panel-2);color:var(--text)}
.btn:focus-visible{outline:none;box-shadow:var(--focus)}
.fsum{margin:0 0 0 auto;align-self:center;font-size:13px;line-height:19px;color:var(--text-3);text-align:right}
.fsum strong{color:var(--text);font-weight:600}
.cards{display:flex;flex-direction:column;gap:16px}
.cards>.card+.card{margin-top:0}
.cards>.card{scroll-margin-top:110px}
@media (max-width:640px){.fbar{position:static;padding:12px 14px}.fld{flex:1 1 140px}.sel select{min-width:0}.fsum{margin:0;width:100%;text-align:left}}
/* client benchmark: collapsible table sections */
.tgl>summary{list-style:none;cursor:pointer;display:flex;gap:12px;align-items:flex-start;padding:16px 20px;transition:background .15s}
.tgl>summary::-webkit-details-marker{display:none}
.tgl>summary:hover{background:var(--panel-2)}
.tgl>summary:focus-visible{outline:none;box-shadow:inset var(--focus)}
.tgl[open]>summary{border-bottom:1px solid var(--border)}
.tgl .chev{flex:none;width:8px;height:8px;margin-top:10px;border-right:1.5px solid var(--text-3);border-bottom:1.5px solid var(--text-3);transform:rotate(-45deg);transition:transform .15s}
.tgl[open]>summary .chev{transform:rotate(45deg)}
.tgl .ttxt{display:flex;flex-direction:column;gap:4px;min-width:0;flex:1}
.tgl .trow{display:flex;align-items:center;gap:8px 12px;flex-wrap:wrap}
.tgl .tmeta{display:flex;align-items:center;gap:6px;flex-wrap:wrap}
.tgl .tcount{font-size:12px;line-height:18px;color:var(--text-4)}
.tgl .sec-desc{margin:0}
.tgl .tact{flex:none;margin-top:4px;font:500 13px/20px 'Inter',sans-serif;color:var(--brand-text)}
.tgl .tact::after{content:"Show"}
.tgl[open] .tact::after{content:"Hide"}
@media (max-width:640px){.tgl>summary{padding:14px 16px}.tgl .tact{display:none}}
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

# Client benchmark only: AM / client filter (stats, the three toggle tables, client cards; state kept in ?am=&client=)
# and remembered open/closed state of the toggle sections (per viewer, localStorage).
BENCH_JS = """
(function(){
  const bar=document.getElementById('fbar'), dataEl=document.getElementById('bench-data');
  if(!bar||!dataEl) return;
  const D=JSON.parse(dataEl.textContent);
  const amSel=document.getElementById('f-am'), clSel=document.getElementById('f-client');
  const clr=document.getElementById('f-clear'), sum=document.getElementById('f-sum');
  const cards=[...document.querySelectorAll('.cards>.card[data-client]')];
  const tables=[...document.querySelectorAll('table[data-ftable]')];
  const LBL=[['flag','err','Flag to Shawal'],['review','warn','Review w/ HG AI'],['monitor','gray','Monitor'],['healthy','ok','Healthy'],['scale','brand','Scale w/ HG AI']];
  const NOT_SCORED=s=>s==='Under gate'||s==='Tracked in Discovery'||s==='No promo data'||s.startsWith('Not scored');
  const ams=[...new Set(D.clients.map(c=>c.a))].sort();
  const stats={};
  document.querySelectorAll('[data-stat]').forEach(el=>{const v=el.querySelector('.value'),h=el.querySelector('.hint');stats[el.dataset.stat]={v,h,v0:v.textContent,h0:h?h.innerHTML:''};});
  const badge=(k,t)=>'<span class="badge '+k+'"><span class="dot '+k+'"></span>'+t+'</span>';
  const plural=(n,w)=>n+' '+w+(n===1?'':'s');
  const esc=s=>s.replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  function fillClients(){
    const am=amSel.value, cur=clSel.value;
    while(clSel.options.length>1) clSel.remove(1);
    D.clients.filter(c=>am==='all'||c.a===am).forEach(c=>clSel.add(new Option(c.n,c.n)));
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
  function apply(){
    const am=amSel.value, cl=clSel.value, on=am!=='all'||cl!=='all';
    amSel.classList.toggle('on',am!=='all'); clSel.classList.toggle('on',cl!=='all');
    tables.forEach(t=>{
      const rows=[...t.tBodies[0].rows], vis=rows.filter(r=>match(r.dataset.client,r.dataset.am));
      rows.forEach(r=>{r.hidden=!vis.includes(r);});
      t.hidden=!vis.length; const e=t.parentElement.querySelector('.empty'); if(e) e.hidden=!!vis.length;
      meta(t,vis,rows.length,on);
    });
    let nc=0; cards.forEach(c=>{const s=match(c.dataset.client,c.dataset.am); c.hidden=!s; if(s) nc++;});
    const R=D.rows.filter(r=>match(r[0],r[1])), n={};
    R.forEach(r=>{n[r[2]]=(n[r[2]]||0)+1;});
    const set=(k,v,h)=>{const s=stats[k]; if(!s) return; s.v.textContent=on?v:s.v0; if(s.h&&h!==undefined) s.h.innerHTML=on?h:s.h0;};
    const ctx=R.filter(r=>r[2].startsWith('Not scored')).length;
    set('clients',String(nc),(am!=='all'?esc(am)+"'s clients, ":'')+'of '+D.clients.length+' with an ad account');
    set('scored',String(R.filter(r=>!NOT_SCORED(r[2])).length),(n['Under gate']||0)+' more under the spend gate'+(ctx?', '+ctx+' Lead Gen and Discovery rows for context':''));
    [['flag','Flag to Shawal'],['review','Review w/ HG AI'],['monitor','Monitor'],['healthy','Healthy'],['scale','Scale w/ HG AI']].forEach(([k,s])=>set(k,String(n[s]||0)));
    set('freq',String(R.filter(r=>r[3]).length));
    const who=[am!=='all'?esc(am):'',cl!=='all'?esc(cl):''].filter(Boolean).join(' · ');
    sum.innerHTML=on?'Showing <strong>'+plural(nc,'client')+'</strong> of '+cards.length+' · '+who:plural(cards.length,'client')+' across '+ams.length+' account managers';
    clr.hidden=!on;
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
  // toggle sections: remember each viewer's open / closed choice
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

def page(title, eyebrow, h1, lede, chips, body, js=""):
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

def build_bench():
    md=open(f"{ROOT}/Client Benchmark Reviews (advanced setups)/Weekly Checks/{DATE}-client-benchmark.md",encoding="utf-8").read()
    S=sections(md)
    rows=list(csv.DictReader(open(f"{ROOT}/Client Benchmark Reviews (advanced setups)/Weekly Checks/{DATE}-client-benchmark.csv",encoding="utf-8")))
    cnt=collections.Counter(r["state"] for r in rows)
    clients={r["client"] for r in rows}
    # 'Not scored (discovery)' / 'Not scored (lead gen)' rows (4 Nov 2026 rule) are context, not scored
    def not_scored(s): return s in ("Under gate","Tracked in Discovery","No promo data") or s.startswith("Not scored")
    scored=sum(1 for r in rows if not not_scored(r["state"]))
    ctx_rows=sum(1 for r in rows if r["state"].startswith("Not scored"))
    ct0=tables(S["_pre"]); hdrv=dict(zip(ct0[0][0],ct0[0][1])) if ct0 and len(ct0[0])>1 else {}
    adv_raw=hdrv.get("Advanced clients","—"); m_adv=re.match(r"(\d+)\s*\(\+(\d+) unmapped\)",adv_raw)
    adv_val=m_adv.group(1) if m_adv else adv_raw; adv_extra=f", {m_adv.group(2)} Advanced without an ad account" if m_adv else ""
    stats=(stat("Advanced clients",adv_val,f"{hdrv.get('Live reads','—')} live reads, {hdrv.get('From CSV','—')} from the CSV export{adv_extra}",key="clients")
        +stat("Rows scored",str(scored),f"{cnt['Under gate']} more under the spend gate"+(f", {cnt['Tracked in Discovery']} lead rows tracked in Discovery, {cnt['No promo data']} Discovery rows without promo data" if cnt.get("Tracked in Discovery") or cnt.get("No promo data") else "")+(f", {ctx_rows} Lead Gen and Discovery rows for context" if ctx_rows else ""),key="scored")
        +stat("Flag to Shawal",str(cnt["Flag to Shawal"]),"ROAS under 2x or no purchases",dot="err",key="flag")
        +stat("Review w/ HG AI",str(cnt["Review w/ HG AI"]),"ROAS 2 to 5x",dot="warn",key="review")
        +stat("Monitor",str(cnt["Monitor"]),"ROAS 5 to 8x",dot="gray",key="monitor")
        +stat("Healthy",str(cnt["Healthy"]),"ROAS 8 to 15x",dot="ok",key="healthy")
        +stat("Scale w/ HG AI",str(cnt["Scale w/ HG AI"]),"ROAS above 15x",dot="brand",key="scale")
        +stat("Frequency over 5",str(sum(1 for r in rows if r.get("freq_flag")=="yes")),"Sales/Retargeting campaigns to refresh creative on; state unchanged",dot="warn",key="freq"))
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
    # client cards, in report order: name -> AM and anchor, for the filter and the client links in the tables
    pkey=[k for k in S if k.startswith("Per client")][0]
    card_list=[]
    for l in S[pkey]:
        if l.startswith("### "):
            parts=[p.strip() for p in l[4:].split(" — ")]
            card_list.append((parts[0], parts[1].replace("AM ","") if len(parts)>1 else ""))
    card_id={n:f"client-{i}" for i,(n,_) in enumerate(card_list)}
    def attr(s): return html.escape(s.strip(), quote=True)
    def who(r): return f' data-client="{attr(r[0])}" data-am="{attr(r[1])}"'
    def href(c): return f"#{card_id[c.strip()]}" if c.strip() in card_id else None

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

    def tmeta(tid, trows, state_col, mode, kind="gray"):
        """Badges in a toggle's header; the filter script rewrites them with the same format."""
        if mode=="states":
            c=collections.Counter(r[state_col].strip() for r in trows)
            h="".join(badge(STATE[s], f"{c[s]} {s}") for s in ("Flag to Shawal","Review w/ HG AI","Monitor","Healthy","Scale w/ HG AI") if c[s])
        else:
            h=badge(kind, f"{len(trows)} campaign{'s' if len(trows)!=1 else ''}") if trows else ""
        return f'<span class="tmeta" data-meta-for="{tid}" data-meta="{mode}" data-kind="{kind}" data-unit="campaign">{h or badge("gray","None")}</span>'
    def toggle(tid, title, desc, meta, inner, open_=False):
        return f"""<section>
<details class="card tgl" id="sec-{tid}"{" open" if open_ else ""}>
<summary><span class="chev" aria-hidden="true"></span><span class="ttxt"><span class="trow"><h2>{esc(title)}</h2>{meta}</span><span class="sec-desc">{desc}</span></span><span class="tact" aria-hidden="true"></span></summary>
{inner}
</details>
</section>"""

    # per client
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
        blend=[p for p in ps if p.startswith("Blended 30d")]
        month=[p for p in ps if p.startswith("This month")]
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
        chtml.append(f"""<div class="card" id="client-{i}" data-client="{attr(name)}" data-am="{attr(am)}">
<div class="card-head"><div><h3>{esc(name)}</h3><div class="sub">AM {esc(am)} · {esc(acct_name)} <span class="mono">{esc(acct_id)}</span></div></div>{src_badge}</div>
{month_strip(month[0]) if month else ""}
<div class="tof">{inline(tof[0]) if tof else ""}</div>
{f'<div class="tof">{inline(blend[0])}</div>' if blend else ""}
{tbl}
{kv}
</div>""")
    states_para=[p for p in paras(S["_pre"]) if p.startswith("States come from")]
    # filter bar: shown by the script (useless without it); options rendered here so the page reads right before it runs
    am_counts=collections.Counter(a for _,a in card_list)
    am_opts="".join(f'<option value="{attr(a)}">{esc(a)} ({n})</option>' for a,n in sorted(am_counts.items()))
    cl_opts="".join(f'<option value="{attr(n)}">{esc(n)}</option>' for n,_ in sorted(card_list,key=lambda x:x[0].lower()))
    fbar=f"""<div class="fbar" id="fbar" role="search" aria-label="Filter this review" hidden>
<div class="fld"><label for="f-am">Account manager</label><span class="sel"><select id="f-am"><option value="all">All account managers</option>{am_opts}</select></span></div>
<div class="fld"><label for="f-client">Client</label><span class="sel"><select id="f-client"><option value="all">All clients</option>{cl_opts}</select></span></div>
<button type="button" class="btn" id="f-clear" hidden>Clear filters</button>
<p class="fsum" id="f-sum" aria-live="polite">{len(card_list)} clients across {len(am_counts)} account managers</p>
</div>"""
    data=json.dumps({"clients":[{"n":n,"a":a} for n,a in sorted(card_list,key=lambda x:x[0].lower())],
                     "rows":[[r["client"],r["am"],r["state"],1 if r.get("freq_flag")=="yes" else 0] for r in rows]},ensure_ascii=False).replace("</","<\\/")
    body=f"""
{fbar}
<script type="application/json" id="bench-data">{data}</script>
<div class="stats cols-4">{stats}</div>
<div class="alert info"><div class="t">How states are assigned</div><p>{inline(states_para[0]) if states_para else ""}</p></div>
<section>
  <div class="sec-head"><div><h2>Weekly Meta Ads meetings since last run</h2><p class="sec-desc">Notes by Gemini attached to the calendar events, read via Drive. Summary, decisions and next steps as Gemini wrote them; client-specific sentences are pulled into each client's card below. Transcript not used.</p></div></div>
  <div class="card">{"".join(mhtml)}</div>
</section>
{toggle("act","Action needed","Sales, Retargeting and Prospecting campaigns first, then Discovery buckets, then Lead Gen tracking checks. Within each, Flag to Shawal before Review w/ HG AI, highest spend first.",tmeta("act",act_rows,6,"states"),act)}
{toggle("scale","Scale candidates","Campaigns above the Scale line. Full context goes to HG AI, which picks where budget goes.",tmeta("scale",sc_rows,6,"count","brand"),sc)}
{toggle("freq","Frequency watch","Sales, Retargeting and Prospecting campaigns whose 14-day frequency is above 5.0. Frequency does not change the ROAS state; this is the list to refresh creative or widen the audience on.",tmeta("freq",frows,7,"count","warn"),fw)}
<section>
  <div class="sec-head"><div><h2>Per client</h2><p class="sec-desc">Ordered by scored MoF and BoF spend, highest first. ToF spend is judged inside the client's Discovery bucket row; the Blended 30d line is the all-campaign view, not de-duplicated. Click a client name in the tables above to jump to its card.</p></div></div>
  <div class="cards">{"".join(chtml)}</div>
</section>
{footer(bullets(S["Footer"]))}
"""
    lede="Scores each CRM-Advanced client's three buckets on ROAS against the Benchmarks doc decision table: Discovery (giveaway + lead campaigns, sign-up promo-code revenue), Prospecting (lookalike sales, pixel) and Retargeting (pixel), with monthly ROI context and this week's meeting notes."
    rl=run_line(S); m2=re.search(r"CSV export (\d{4}-\d{2}-\d{2}) to (\d{4}-\d{2}-\d{2}) for the (\d+) accounts",rl)
    chips=[f"Run {RUN}","Discovery: 30-day window, promo-code ROAS, $200 gate","Sales/Retargeting/Prospecting: 14-day window, pixel ROAS, $200 gate","Lead Gen: CPL diagnostic, $100 tracking gate"]+([f"CSV export {m2.group(1)} to {m2.group(2)} for {m2.group(3)} accounts"] if m2 else [])+[compare_chip(S)]
    return page(f"Client benchmark {WEEK}","Weekly Meta Ads review · Client benchmark, advanced setups","Client benchmark review",lede,[esc(c) for c in chips],body,js=BENCH_JS)

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
