import csv, json, glob, os, re, collections, datetime
ROOT="/Users/shawal/Desktop/Meta Ads Analysis - 21:09:26"
SP=os.path.dirname(os.path.abspath(__file__))
TODAY="2026-09-21"
OUT=f"{ROOT}/Client Benchmark Reviews (advanced setups)/Weekly Checks"
ADV={ # CRM Meta Ads = Advanced (Clients - Onboarding tab), name -> (AM, account id, account name, connector)
 "FLOHOM":("Makenna","2100710320122219","FLOHOM Ads","live"),
 "Treetop Escapes":("Makenna","967636478877602","Treetop Escapes Ads","live"),
 "Paradise Pointe":("Makenna","1585826092078255","Paradise Pointe Ads","csv"),
 "Asheville River Cabins":("Charlotte","615836588009747","Asheville River Cabins Ads","live"),
 "Green Springs Inn":("Alicia","1390516335151357","Green Springs Inn","live"),
 "Starlight Haven Hot Springs":("Charlotte","901138032027913","Starlight Haven Hot Springs","live"),
 "Starlight Haven Weiss Lake":("Charlotte","74756899","Starlight Haven Weiss Lake","live"),
 "Stay Saluda NC":("Makenna","1863632561215857","Stay Saluda Ads","live"),
 "Endless Stays":("Nicole","896372356081479","Endless Stays","csv"),
 "Stay On 30A":("Charlotte","25640434272252212","Stay on 30a Ads","live"),
 "AwayFrames":("Alicia","2471256056603833","Awayframes Ad Account","live"),
 "Bison Ridge Retreat":("Chiara","950241787963535","Bison Ridge Retreat Ad Account","csv"),
 "American River Resort":("Nicole","953162737054331","American River Resort","live"),
 "Canopy at Moody Moon":("Alicia","1293707265980102","The Canopy At Moody Moon Ridge","live"),
 "Tàberg Falls":("Alicia","827872700004659","Táberg Falls","live"),
 "Ponderosa Pines Resort":("Anna","1058846326445255","Ponderosa Pines Resort","csv"),
}
def f(x):
    try: return float(x)
    except: return None
def money(v,d=2): return "—" if v is None else (f"${v:,.{d}f}")
def x(v): return "—" if v is None else f"{v:.1f}x"
def pct(v): return "—" if v is None else f"{v:.2f}%"

# ---------- classification ----------
def ctype(obj,name):
    n=name.lower()
    if obj=="OUTCOME_LEADS" or (obj is None and re.search(r"\blead",n)): return "Lead Gen (MoF)"
    if obj=="OUTCOME_SALES" or (obj is None and re.search(r"bof|retarget|sales",n)):
        if re.search(r"bof|retarget",n): return "Retargeting (BoF)"
        if re.search(r"mof|lookalike",n): return "Sales (MoF lookalike)"
        return "Sales"
    if obj in ("OUTCOME_TRAFFIC","OUTCOME_ENGAGEMENT") or re.search(r"discovery|giveaway|keyword|tof|follow",n): return "ToF"
    return "UNCLASSIFIED"
LEAD, SALES = "Lead Gen (MoF)", ("Retargeting (BoF)","Sales (MoF lookalike)","Sales")
def cpl_state(cpl,leads,spend):
    if leads in (None,0): return "Flag to Shawal","no leads"
    if cpl<0.30: return "Scale w/ HG AI",""
    if cpl<0.50: return "Healthy",""
    if cpl<1.00: return "Monitor",""
    if cpl<2.50: return "Review w/ HG AI",""
    return "Flag to Shawal",""
def roas_state(roas,purch):
    if purch in (None,0) or roas is None: return "Flag to Shawal","no purchases"
    if roas>15: return "Scale w/ HG AI",""
    if roas>=8: return "Healthy",""
    if roas>=5: return "Monitor",""
    if roas>=2: return "Review w/ HG AI",""
    return "Flag to Shawal",""
ORDER={"Flag to Shawal":0,"Review w/ HG AI":1,"Monitor":2,"Healthy":3,"Scale w/ HG AI":4,"Under gate":5}
def diags(t,cpc,cpm,ctr,cpp,freq):
    d=[]
    if t==LEAD:
        if cpc is not None and cpc>0.30: d.append(f"CPC {money(cpc)} > $0.30")
        if cpm is not None and cpm>14.84: d.append(f"CPM {money(cpm)} > $14.84")
        if ctr is not None and ctr<3.03: d.append(f"CTR {pct(ctr)} < 3.03%")
    else:
        if cpc is not None and cpc>0.62: d.append(f"CPC {money(cpc)} > $0.62")
        if cpm is not None and cpm>16.50: d.append(f"CPM {money(cpm)} > $16.50")
        if ctr is not None and ctr<2.0: d.append(f"CTR {pct(ctr)} < 2%")
        if cpp is not None and cpp>90: d.append(f"cost/booking {money(cpp)} > $90")
        if freq is not None and freq>3.0: d.append(f"freq {freq:.1f} > 3.0")
    return "; ".join(d) if d else "within lines"

# ---------- live data ----------
live=collections.defaultdict(lambda: collections.defaultdict(dict))  # client -> id -> win -> row
for line in open(f"{SP}/live.psv",encoding="utf-8"):
    p=line.rstrip("\n").split("|")
    if len(p)<20: continue
    client,acct,am,win,cid,name,obj,status=p[:8]
    spend,impr,cpm,ctr,clicks,cpc,freq,leads,cpl,purch,cpp,roas=[f(v) for v in p[8:20]]
    live[client][cid][int(win)]=dict(name=name,obj=obj,status=status,spend=spend,impr=impr,cpm=cpm,ctr=ctr,clicks=clicks,cpc=cpc,freq=freq,leads=leads,cpl=cpl,purch=purch,cpp=cpp,roas=roas)

# ---------- csv fallback ----------
csvfile=sorted(glob.glob(f"{ROOT}/Weekly CSV Reports/*_meta-ads-report.csv"))[-1]
rows=list(csv.DictReader(open(csvfile,encoding="utf-8-sig")))
rs,re_=rows[0]["Reporting starts"],rows[0]["Reporting ends"]
csv_days=(datetime.date.fromisoformat(re_)-datetime.date.fromisoformat(rs)).days+1
csvagg=collections.defaultdict(lambda: collections.defaultdict(float))
for r in rows:
    if not r["Account name"]: continue
    k=(r["Account name"],r["Campaign name"])
    for c in ["Amount spent (USD)","Impressions","Link clicks","Purchases","Purchases conversion value","Leads"]:
        csvagg[k][c]+=f(r[c]) or 0

# ---------- ROI context ----------
def norm(s): return re.sub(r"[^a-z0-9]","",s.lower())
roi={}
for fn in sorted(glob.glob(f"{ROOT}/Monthly ROI data/*.json")):
    d=json.load(open(fn))
    for c in d["clients"]:
        roi.setdefault(norm(c["clientName"]),{})[d["period"]]=c
def roi_for(client):
    n=norm(client); alias={"stayonsaludanc":"staysaluda","staysaludanc":"staysaluda","stayon30a":"stayon30a"}
    n=alias.get(n,n)
    for k in roi:
        if k==n or k.startswith(n) or n.startswith(k): return roi[k]
    return {}
def roi_line(client):
    r=roi_for(client)
    if not r: return "Monthly ROI: no record in the Monthly ROI data files."
    parts=[]
    for period in sorted(r, key=lambda p: ("July" in p, "Aug" in p)):  # July then August
        c=r[period]; camp=c.get("campaigns") or {}
        rt=camp.get("retargeting") or {}; nl=camp.get("newLeads") or {}
        blended=c.get("blendedRoas", c.get("roas"))
        seg=f"{period.split()[0]}: spend {money(c.get('overallMetaAdSpend'),0)}, {c.get('totalBookingsAttributedToMeta') or 0} Meta-attributed bookings, blended ROAS {x(blended)}"
        if rt: seg+=f", retargeting ROAS {x(rt.get('roas'))}"
        if nl and nl.get("costPerLead") is not None: seg+=f", CPL {money(nl.get('costPerLead'))} on {nl.get('leads')} leads"
        parts.append(seg)
    return "Monthly ROI: "+" · ".join(parts)+"."


# ---------- Weekly Meta Ads meeting notes (Gemini) ----------
# One entry per meeting doc found on the calendar since the previous run. Oldest first.
MEETINGS=[
 dict(title="Meta Ads Strategy", date="2026-09-16", doc_id="1Hoq1JUk1tFxSCUeYexeEELfVSZwTq7eJ2Pi_NvVDF4A", file=f"{SP}/meeting1.json"),
 dict(title="Meta Ads Sync",     date="2026-09-17", doc_id="1oMlKzZdFQxYCXKMiFnaG-2ews_EkudXgG0zivvI2l1c", file=f"{SP}/meeting2.json"),
]
# How Gemini spells clients in the notes. Lower-case substrings.
ALIASES={
 "FLOHOM":["flohom","flow home","flo home"],
 "Tàberg Falls":["taberg","tabber","taber falls","tàberg","táberg"],
 "Stay On 30A":["30a"],
 "Canopy at Moody Moon":["canopy","moody moon"],
 "Starlight Haven Hot Springs":["starlight","hot springs"],
 "Starlight Haven Weiss Lake":["starlight","weiss"],
 "Stay Saluda NC":["saluda"],
 "American River Resort":["american river"],
 "Asheville River Cabins":["asheville"],
 "Green Springs Inn":["green springs"],
 "Treetop Escapes":["treetop","tree top"],
 "Paradise Pointe":["paradise pointe","paradise point"],
 "Endless Stays":["endless"],
 "AwayFrames":["awayframes","away frames"],
 "Bison Ridge Retreat":["bison"],
 "Ponderosa Pines Resort":["ponderosa"],
}
def clean(t):
    t=re.sub(r"\[([^\]]*)\]\([^)]*\)",r"\1",t)
    t=re.sub(r"\*+","",t); t=t.replace("\\[","[").replace("\\]","]")
    t=re.sub(r"\s*\(\d\d:\d\d:\d\d\)","",t)          # drop timestamps
    return re.sub(r"[ \t]+"," ",t).strip()
def section(raw,title,stop_titles):
    m=re.search(r"^#+ \*\*"+re.escape(title)+r"\*\*.*?$",raw,re.M)
    if not m: return ""
    rest=raw[m.end():]
    ends=[x.start() for t in stop_titles for x in [re.search(r"^#+ \*\*"+re.escape(t)+r"\*\*",rest,re.M)] if x]
    return rest[:min(ends)] if ends else rest
meetings=[]
for M in MEETINGS:
    if not os.path.exists(M["file"]): continue
    raw=json.load(open(M["file"]))["fileContent"]
    mfull=re.search(r"^# \*\*.*Full notes",raw,re.M); full=raw[mfull.start():] if mfull else raw
    mtr=re.search(r"^# \*\*.*Transcript\*\*",full,re.M); body=full[:mtr.start()] if mtr else full
    summ=re.sub(r"\n\s*\n+","\n",clean(section(body,"Summary",["Decisions","Next steps","Details"])))
    dec=[clean(l) for l in section(body,"Decisions",["Next steps"]).splitlines() if l.strip().startswith("-")]
    nxt=[clean(l) for l in section(body,"Next steps",["Details"]).splitlines() if l.strip().startswith("-")]
    details=clean(section(body,"Details",[]))
    sents=[x.strip(" -") for x in re.split(r"(?<=[.!?])\s+",details) if x.strip()]
    meetings.append(dict(M,summary=summ,decisions=dec,next=nxt,sents=sents))
def mentions(client):
    keys=set(ALIASES.get(client,[]))|{client.lower()}
    out=[]
    for m in meetings:
        hits=[x for x in m["sents"] if any(k in x.lower() for k in keys)]
        if hits: out.append((m["date"],m["title"],hits[:3]))
    return out

# ---------- score ----------
records=[]; unclassified=[]; paused_by_client=collections.defaultdict(list)
for client,(am,acct,acctname,src) in ADV.items():
    tof_spend=0.0
    if src=="live":
        for cid,wins in live[client].items():
            r30=wins.get(30); r14=wins.get(14)
            base=r30 or r14
            t=ctype(base["obj"],base["name"])
            if t=="ToF": tof_spend+=(r30 or {}).get("spend") or 0; continue
            if t=="UNCLASSIFIED": unclassified.append((client,base["name"])); continue
            if base["status"]!="ACTIVE":
                # decision 2026-09-23: only live campaigns are scored; paused ones are listed, not judged
                rr=r30 if t==LEAD else (r14 or r30)
                paused_by_client[client].append(dict(name=base["name"],type=t,win=30 if t==LEAD else 14,spend=rr["spend"] or 0,
                    results=f"{int(rr['leads'] or 0)} leads" if t==LEAD else f"{int(rr['purch'] or 0)} purchases",
                    gov=f"CPL {money(rr['cpl'])}" if t==LEAD else f"ROAS {x(rr['roas'])}"))
                continue
            if t==LEAD:
                r=r30; win=30; gate=100
                if r is None: continue
                gov=f"CPL {money(r['cpl'])}"; govval=r["cpl"]; results=f"{int(r['leads'] or 0)} leads"
                state,why=cpl_state(r["cpl"],r["leads"],r["spend"])
                extra=f"14d CPL {money(r14['cpl'])}" if r14 and r14.get("cpl") is not None else ""
            else:
                r=r14; win=14; gate=200
                if r is None: continue
                gov=f"ROAS {x(r['roas'])}"; govval=r["roas"]; results=f"{int(r['purch'] or 0)} purchases"
                state,why=roas_state(r["roas"],r["purch"])
                extra=f"30d ROAS {x(r30['roas'])}, {int(r30['purch'] or 0)} purchases" if r30 and r30.get("roas") is not None else ""
            if r["spend"]<gate: state="Under gate"; why=f"spend {money(r['spend'])} < ${gate} gate"
            dg=diags(t,r["cpc"],r["cpm"],r["ctr"],r["cpp"],r["freq"])
            notes=[]
            if why: notes.append(why)
            if extra: notes.append(extra)
            records.append(dict(client=client,am=am,acct=acct,cid=cid,name=r["name"],type=t,win=win,src="live",spend=r["spend"],results=results,gov=gov,govval=govval,state=state,diag=dg,notes="; ".join(notes),status=r["status"]))
    else:
        for (a,cname),v in csvagg.items():
            if a!=acctname: continue
            t=ctype(None,cname); spend=v["Amount spent (USD)"]
            if t=="ToF": tof_spend+=spend; continue
            if t=="UNCLASSIFIED": unclassified.append((client,cname)); continue
            impr,clicks,purch,val,leads=v["Impressions"],v["Link clicks"],v["Purchases"],v["Purchases conversion value"],v["Leads"]
            cpc=spend/clicks if clicks else None; cpm=spend/impr*1000 if impr else None; ctr=clicks/impr*100 if impr else None
            if t==LEAD:
                win=csv_days; gate=100; cpl=spend/leads if leads else None
                gov=f"CPL {money(cpl)}"; govval=cpl; results=f"{int(leads)} leads"; state,why=cpl_state(cpl,leads,spend); cpp=None
            else:
                win=csv_days; gate=200; roas=val/spend if spend else None; cpp=spend/purch if purch else None
                gov=f"ROAS {x(roas)}"; govval=roas; results=f"{int(purch)} purchases"; state,why=roas_state(roas,purch)
            if spend<gate: state="Under gate"; why=f"spend {money(spend)} < ${gate} gate"
            dg=diags(t,cpc,cpm,ctr,cpp,None)+"; CTR here is link CTR from the export"
            notes=[f"source: CSV export {rs} to {re_} ({csv_days} days, not the {14 if t!=LEAD else 30}-day window), not live; provisional, export has no status column"]
            if why: notes.append(why)
            records.append(dict(client=client,am=am,acct=acct,cid="",name=cname,type=t,win=win,src="csv",spend=spend,results=results,gov=gov,govval=govval,state=state,diag=dg,notes="; ".join(notes),status="unknown"))
    ADV[client]=(am,acct,acctname,src,tof_spend)

# ---------- report ----------
by_client=collections.defaultdict(list)
for r in records: by_client[r["client"]].append(r)
client_spend={c:sum(r["spend"] for r in rs) for c,rs in by_client.items()}
for c in ADV:
    client_spend.setdefault(c,0.0)
order=sorted(ADV, key=lambda c:-client_spend[c])
scored=[r for r in records if r["state"]!="Under gate"]
counts=collections.Counter(r["state"] for r in records)
def srow(r,first=True):
    return f"| {r['client']} | {r['am']} | {r['name']} | {r['type']} | {money(r['spend'],0)} / {r['win']}d | {r['gov']} | {r['state']} | New (first run) |"
L=[]
L.append(f"# Client Benchmark Review (advanced setups) — {TODAY}\n")
L.append(f"Run: 21 September 2026. Live reads via the Meta connector; CSV export {rs} to {re_} for the 4 accounts the connector cannot read. Scope: clients marked **Advanced** in the CRM \"Meta Ads\" column (Clients - Onboarding tab). Only Lead Gen (MoF) and Sales/Retargeting (BoF) campaigns are scored; IG Discovery and Keyword (ToF) spend is shown for context only.\n")
L.append("| Advanced clients | Live reads | From CSV | Campaigns scored | Under spend gate | Flag to Shawal | Review w/ HG AI | Monitor | Healthy | Scale w/ HG AI |")
L.append("|---|---|---|---|---|---|---|---|---|---|")
L.append(f"| {len(ADV)} | {sum(1 for v in ADV.values() if v[3]=='live')} | {sum(1 for v in ADV.values() if v[3]=='csv')} | {len(scored)} | {counts['Under gate']} | {counts['Flag to Shawal']} | {counts['Review w/ HG AI']} | {counts['Monitor']} | {counts['Healthy']} | {counts['Scale w/ HG AI']} |\n")
L.append("States come from the Decision Making table in the Benchmarks doc. Lead Gen: CPL under $0.30 Scale, $0.30–0.50 Healthy, $0.50–1.00 Monitor, $1.00–2.50 Review, $2.50+ Flag, 30-day window, $100 gate. Sales/Retargeting: ROAS above 15x Scale, 8–15x Healthy, 5–8x Monitor, 2–5x Review, under 2x Flag, 14-day window, $200 gate. Band edges are inclusive on the lower bound.\n")

if meetings:
    L.append("## Weekly Meta Ads meetings since last run (Notes by Gemini)\n")
    L.append("Source: \"Notes by Gemini\" docs attached to the calendar events, read via Drive. Summary, decisions and next steps as Gemini wrote them; client-specific sentences are pulled into each client's section below. Transcript not used.\n")
    for m in meetings:
        L.append(f"### {m['title']} — {m['date']} — doc `{m['doc_id']}`\n")
        for para in m["summary"].split("\n"):
            if para.strip(): L.append(para.strip()+"\n")
        if m["decisions"]:
            L.append("Decisions:"); L.extend(m["decisions"]); L.append("")
        if m["next"]:
            L.append("Next steps:"); L.extend(m["next"]); L.append("")
else:
    L.append("## Weekly Meta Ads meetings since last run\n\nNo \"Notes by Gemini\" doc found on the Meta Ads Strategy or Meta Ads Sync events.\n")

L.append("## Action needed\n")
L.append("Flag to Shawal first, then Review w/ HG AI. Within a state, highest spend first.\n")
L.append("| Client | AM | Campaign | Type | Spend / window | Governing metric | State | Status vs last week |")
L.append("|---|---|---|---|---|---|---|---|")
act=[r for r in records if r["state"] in ("Flag to Shawal","Review w/ HG AI")]
for r in sorted(act,key=lambda r:(ORDER[r["state"]],-r["spend"])): L.append(srow(r))
L.append("")
L.append("## Scale candidates\n")
L.append("| Client | AM | Campaign | Type | Spend / window | Governing metric | State | Status vs last week |")
L.append("|---|---|---|---|---|---|---|---|")
sc=[r for r in records if r["state"]=="Scale w/ HG AI"]
for r in sorted(sc,key=lambda r:-r["spend"]): L.append(srow(r))
if not sc: L.append("| — | | | | | | | |")
L.append("")
L.append("## Per client, ordered by scored MoF + BoF spend\n")
for c in order:
    am,acct,acctname,src,tof=ADV[c]
    L.append(f"### {c} — AM {am} — account {acctname} ({acct}) — {'live read' if src=='live' else 'CSV export, provisional'}\n")
    L.append(f"ToF (Discovery / Keyword) spend, not scored: {money(tof,0)} over {'30 days' if src=='live' else f'{csv_days} days (export)'}.\n")
    rs_=by_client.get(c,[])
    if not rs_:
        L.append("No live Lead Gen or Sales campaigns with spend in the window.\n")
    else:
        L.append("| Campaign | Type | Window | Spend | Results | Governing metric | State | Diagnostics vs investigate lines | Notes | Change vs last week |")
        L.append("|---|---|---|---|---|---|---|---|---|---|")
        for r in sorted(rs_,key=lambda r:(ORDER[r["state"]],-r["spend"])):
            L.append(f"| {r['name']} | {r['type']} | {r['win']}d | {money(r['spend'],0)} | {r['results']} | {r['gov']} | {r['state']} | {r['diag']} | {r['notes']} | First run |")
        L.append("")
    for pz in paused_by_client.get(c,[]):
        L.append(f"Paused in window, not scored: {pz['name']} ({pz['type']}), {money(pz['spend'],0)} / {pz['win']}d, {pz['results']}, {pz['gov']}. Live campaigns only are scored (decision 2026-09-23).\n")
    L.append(roi_line(c)+"\n")
    ms=mentions(c)
    if ms:
        for d,t,hits in ms: L.append(f"Meeting notes ({t} {d}): "+" ".join(hits))
    else:
        L.append("Meeting notes: not mentioned in this week's meetings.")
    L.append("")
    L.append("HG AI notes: none dropped in yet.\n")
L.append("## Footer\n")
L.append(f"- Windows: Lead Gen last 30 days, Sales/Retargeting last 14 days (live). CSV accounts use the export period {rs} to {re_} ({csv_days} days) and are provisional.")
L.append("- Gates: $100 Lead Gen, $200 Sales/Retargeting. Campaigns under the gate are listed but not judged.")
L.append("- Classification: by campaign objective (OUTCOME_LEADS → Lead Gen; OUTCOME_SALES → Sales, split into Retargeting (BoF) or MoF lookalike by name; OUTCOME_TRAFFIC / OUTCOME_ENGAGEMENT → ToF, not scored). CSV accounts have no objective column, so classification there is by name.")
L.append("- Sales campaigns with an MoF or lookalike prefix are scored on the Retargeting ROAS bands because they optimise for purchases. The Benchmarks doc has no separate band for prospecting sales campaigns; confirm or add one.")
L.append("- CTR on live rows is Meta's CTR (all clicks), not link CTR. The doc's click-rate lines are probably link CTR, so treat the CTR diagnostic as indicative.")
L.append("- Frequency and cost per booking are diagnostics only and do not change the state (decision 2026-09-21).")
L.append("- Only campaigns live (ACTIVE) at run time are scored. Paused campaigns that spent inside the window are listed per client as \"Paused in window\" and never enter Action needed or the counts (decision 2026-09-23).")
L.append(f"- Unclassified campaigns: {', '.join(f'{c}: {n}' for c,n in unclassified) if unclassified else 'none'}.")
L.append("- Previous report: none, first run.")
L.append("- Meeting notes: every \"Meta Ads Strategy\" or \"Meta Ads Sync\" calendar event since the previous run that has a \"Notes by Gemini\" attachment, read via Drive. Client names are matched with an alias list (Flow Home = FLOHOM, Tabber = Tàberg Falls).")
L.append(f"- Monthly ROI context from `Monthly ROI data/` ({', '.join(sorted({p for v in roi.values() for p in v}))}). Revenue there comes from the Client Performance Tracking sheet, not the pixel, so its ROAS is not comparable to the pixel ROAS above.")
open(f"{OUT}/{TODAY}-client-benchmark.md","w",encoding="utf-8").write("\n".join(L)+"\n")
with open(f"{OUT}/{TODAY}-client-benchmark.csv","w",newline="",encoding="utf-8") as fh:
    w=csv.writer(fh); w.writerow("run_date,client,am,ad_account_id,campaign_id,campaign,type,window_days,source,spend,results,governing_metric,governing_value,state,diagnostics,diff_status,weeks_open,notes".split(","))
    for r in records:
        gm="cpl" if r["type"]==LEAD else "roas"
        w.writerow([TODAY,r["client"],r["am"],r["acct"],r["cid"],r["name"],r["type"],r["win"],r["src"],f"{r['spend']:.2f}",r["results"],gm,"" if r["govval"] is None else f"{r['govval']:.2f}",r["state"],r["diag"],"first_run",1 if r["state"] in ("Flag to Shawal","Review w/ HG AI") else 0,r["notes"]])
print("records",len(records),"counts",dict(counts)); print("unclassified",unclassified)
