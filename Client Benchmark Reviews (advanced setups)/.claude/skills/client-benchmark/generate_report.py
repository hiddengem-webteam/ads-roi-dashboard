import csv, json, glob, os, re, collections, datetime
ROOT=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","..","..",".."))
SP=os.path.dirname(os.path.abspath(__file__))
TODAY="2026-10-05"
PREV_DATE="2026-09-28"
OUT=f"{ROOT}/Client Benchmark Reviews (advanced setups)/Weekly Checks"
ADV={ # CRM "Clients - Onboarding" tab, Meta Ads = Advanced, read 2026-10-05: name -> (AM, account id, account name, connector)
 "FLOHOM":("Makenna","2100710320122219","FLOHOM Ads","live"),
 "Treetop Escapes":("Makenna","967636478877602","Treetop Escapes Ads","live"),
 "Paradise Pointe":("Makenna","1585826092078255","Paradise Pointe Ads","csv"),
 "Asheville River Cabins":("Charlotte","615836588009747","Asheville River Cabins Ads","csv"),
 "Green Springs Inn":("Alicia","1390516335151357","Green Springs Inn","live"),
 "Starlight Haven Hot Springs":("Charlotte","901138032027913","Starlight Haven Hot Springs","live"),
 "Starlight Haven Weiss Lake":("Charlotte","74756899","Starlight Haven Weiss Lake","live"),
 "Stay Saluda NC":("Makenna","1863632561215857","Stay Saluda Ads","live"),
 "Endless Stays":("Nicole","896372356081479","Endless Stays","csv"),
 "Stay On 30A":("Charlotte","25640434272252212","Stay on 30a Ads","live"),
 "AwayFrames":("Alicia","2471256056603833","Awayframes Ad Account","live"),
 "Bison Ridge Retreat":("Chiara","950241787963535","Bison Ridge Retreat Ad Account","csv"),
 "American River Resort":("Nicole","953162737054331","American River Resort","live"),
 "Tàberg Falls":("Alicia","827872700004659","Táberg Falls","live"),
 "Ponderosa Pines Resort":("Anna","1058846326445255","Ponderosa Pines Resort","csv"),
 "The Outpost":("Anna","1530849534802936","The Outpost Grand Canyon","live"),
 "Selah Place":("Alicia","1275283434220508","Selah.place","live"),
 "Sunapee Stays":("Charlotte","651114096215889","Sunapee Stays Ads Account","live"),
 "Ridge & Falls":("Makenna","1313401330776046","Ridge & Falls ad account","live"),
 "Little River Landing":("Makenna","884285717873613","Little River Landing","live"),
 "North Star Lodge & Resort":("Charlotte","2003562593933799","North Star Lodge & Resort Ads","live"),
}
# Advanced in the CRM but with no ad account in PROJECT.md section 5 (footer only)
ADV_UNMAPPED={"Treetop Hideaways":"Kristal","Walden Retreats":"Anna","Glasscombe":"Charlotte","Cabin Collective":"Chiara","Casey Key Resort":"Alicia","Arca Roatan":"—"}
# Was Advanced on 2026-09-21, now Basic in the CRM: dropped from scope this run
ADV_DROPPED={}  # no scope changes vs 2026-09-28; three new Advanced clients in the CRM (Cabin Collective, Casey Key Resort, Arca Roatan) have no ad account yet
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
csvstatus={}
for r in rows:
    if not r["Account name"]: continue
    k=(r["Account name"].strip(),r["Campaign name"])
    for c in ["Amount spent (USD)","Impressions","Reach","Link clicks","Purchases","Purchases conversion value","Leads"]:
        csvagg[k][c]+=f(r[c]) or 0
    d=(r.get("Campaign delivery") or "").strip().lower()
    csvstatus[k]="ACTIVE" if d=="active" or csvstatus.get(k)=="ACTIVE" else (d.upper() or "unknown")

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
    MONTHS=["January","February","March","April","May","June","July","August","September","October","November","December"]
    for period in sorted(r, key=lambda p: (p.split()[-1], next((i for i,m in enumerate(MONTHS) if p.startswith(m[:3])),99))):  # oldest month first
        c=r[period]; camp=c.get("campaigns") or {}
        rt=camp.get("retargeting") or {}; nl=camp.get("newLeads") or {}
        blended=c.get("blendedRoas", c.get("roas"))
        seg=f"{period.split()[0]}: spend {money(c.get('overallMetaAdSpend'),0)}, {c.get('totalBookingsAttributedToMeta') or 0} Meta-attributed bookings, blended ROAS {x(blended)}"
        if rt: seg+=f", retargeting ROAS {x(rt.get('roas'))}"
        if nl and nl.get("costPerLead") is not None: seg+=f", CPL {money(nl.get('costPerLead'))} on {nl.get('leads')} leads"
        parts.append(seg)
    out="Monthly ROI: "+" · ".join(parts)+"."
    last=max(r, key=lambda p: (p.split()[-1], next((i for i,m in enumerate(MONTHS) if p.startswith(m[:3])),99)))
    note=(r[last].get("note") or "").strip()
    if note: out+=f" Note in the {last.split()[0]} file: {note}"
    return out


# ---------- Weekly Meta Ads meeting notes (Gemini) ----------
# One entry per meeting doc found on the calendar since the previous run. Oldest first.
MEETINGS=[
 dict(title="Meta Ads Strategy", date="2026-10-01", doc_id="1Jy5fp33nsdX6kzkDLoSU-4abEvppm7is4zpoC84FNlo", file=f"{SP}/meeting1.json"),
]
# How Gemini spells clients in the notes. Lower-case substrings.
ALIASES={
 "FLOHOM":["flohom","flow home","flo home"],
 "Tàberg Falls":["taberg","tabber","taber falls","tàberg","táberg","tipik falls","debug falls"],
 "Stay On 30A":["30a","stay on 38"],
 "Canopy at Moody Moon":["canopy","moody moon"],
 "Starlight Haven Hot Springs":["starlight","hot springs","starlight haven"],
 "Starlight Haven Weiss Lake":["starlight","weiss"],
 "Stay Saluda NC":["saluda"],
 "American River Resort":["american river"],
 "Asheville River Cabins":["asheville","ashwood river"],
 "Green Springs Inn":["green springs"],
 "Treetop Escapes":["treetop","tree top"],
 "Paradise Pointe":["paradise pointe","paradise point"],
 "Endless Stays":["endless"],
 "AwayFrames":["awayframes","away frames"],
 "Bison Ridge Retreat":["bison"],
 "Ponderosa Pines Resort":["ponderosa"],
 "The Outpost":["outpost"],
 "Selah Place":["selah","sailor place"],
 "Sunapee Stays":["sunapee"],
 "Ridge & Falls":["ridge & falls","ridge and falls","ridge falls"],
 "Little River Landing":["little river"],
 "North Star Lodge & Resort":["north star","northstar"],
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
    if not os.path.exists(M["file"]):
        if M.get("note"): meetings.append(dict(M,summary=M["note"],decisions=[],next=[],sents=[]))
        continue
    raw=json.load(open(M["file"]))["fileContent"]
    mfull=re.search(r"^# \*\*.*Full notes",raw,re.M); full=raw[mfull.start():] if mfull else raw
    mtr=re.search(r"^# \*\*.*Transcript\*\*",full,re.M); body=full[:mtr.start()] if mtr else full
    summ=re.sub(r"\n\s*\n+","\n",clean(section(body,"Summary",["Decisions","Next steps","Details"])))
    dec=[clean(l) for l in section(body,"Decisions",["Next steps"]).splitlines() if l.strip().startswith("-")]
    nxt=[clean(l) for l in section(body,"Next steps",["Details"]).splitlines() if l.strip().startswith("-")]
    details=clean(section(body,"Details",[]))
    sents=[re.sub(r"\s+"," ",x.strip(" -\n")) for x in re.split(r"(?<=[.!?])\s+",details) if x.strip(" -\n")]
    meetings.append(dict(M,summary=summ,decisions=dec,next=nxt,sents=sents))
def mentions(client):
    keys=set(ALIASES.get(client,[]))|{client.lower()}
    out=[]
    for m in meetings:
        hits=[x for x in m["sents"] if any(k in x.lower() for k in keys)]
        if hits: out.append((m["date"],m["title"],hits[:3]))
    return out

# ---------- previous report (week-over-week diff) ----------
prev={}
prevfiles=sorted(x for x in glob.glob(f"{OUT}/*-client-benchmark.csv") if os.path.basename(x)[:10]<TODAY)
PREVFILE=os.path.basename(prevfiles[-1]) if prevfiles else None
if prevfiles:
    for r in csv.DictReader(open(prevfiles[-1],encoding="utf-8")):
        key=r["campaign_id"] or (r["client"]+"||"+r["campaign"])
        prev[key]=r
FLAGGED=("Flag to Shawal","Review w/ HG AI")
def diff_for(rec):
    key=rec["cid"] or (rec["client"]+"||"+rec["name"])
    p=prev.get(key)
    if p is None: return ("new",1 if rec["state"] in FLAGGED else 0,"New, not in the 28 Sep run")
    ps=p["state"]; pw=int(p.get("weeks_open") or 0)
    if ps in FLAGGED and rec["state"] in FLAGGED: return ("still_open",pw+1,f"Still open, week {pw+1}"+("" if ps==rec["state"] else f" (was {ps})"))
    if ps in FLAGGED and rec["state"] not in FLAGGED: return ("fixed",0,f"Fixed, was {ps}")
    if ps not in FLAGGED and rec["state"] in FLAGGED: return ("new",1,f"New flag, was {ps}")
    return ("unchanged",0,"Unchanged" if ps==rec["state"] else f"Was {ps}")

# ---------- HG AI reports dropped in since the previous run ----------
HGAI={}
for fn in sorted(glob.glob(f"{ROOT}/HG AI Reports/*.md")):
    b=os.path.basename(fn); d=b[:10]
    if d<PREV_DATE: continue
    HGAI[b]=fn
HGAI_LINES={
 "Paradise Pointe":"HG AI notes (23 Sep, carried from last week, no new file): Meta-credited BoF retargeting purchases fell 76% month over month (ROAS 20.2x to 4.2x, purchase days 18 to 5) while PMS direct revenue stayed flat at about $134k, and the direct-booking channel label switched from BE-API to website in the same window. Check Purchase tracking (Events Manager, pixel and CAPI, test booking) before changing budget; hold BoF spend, add creative and widen the audience if frequency is above 3.",
 "Stay Saluda NC":"HG AI notes (23 Sep, carried from last week, no new file): account ROAS 1.71x to 2.12x on the mix change, but BoF retargeting weakened in the second half of the month (6.07x to 2.40x, CTR down 14%) on flat spend. ToF was already scaled to about $25/day on 18 to 22 Sep, so fix the retargeting pool first (4 to 6 fresh review-led ads, add IG/FB engagers and the GHL list), keep ToF steps at 20% or less, and point creative at the open calendar (next 30 days 47% occupied).",
 "Tàberg Falls":"HG AI notes (23 Sep, carried from last week, no new file): hold off moving $50/day from the lookalike into retargeting and the giveaway. Both sales campaigns fell together in the last 15 days on flat spend (retargeting 11.2x to 3.7x, lookalike 4.8x to 3.2x), so the cause is shared (creative age, checkout, offer or tracking), not the lookalike. Check retargeting frequency and creative age first; if moving money now, trim the lookalike 20% into the giveaway and leave retargeting alone. Weekend nights to 18 Dec are 46% booked, December weekends 8%.",
}
EXTRA_NOTES={
 "Selah Place":"Actions log: the $100/day prospecting test was paused after 28 Sep (Done) and the account is back to ACTIVE and queryable, so the payment error is cleared; the planned move of that budget into the BoF retargeting campaign has not happened yet (BoF still $15/day).",
 "Ridge & Falls":"Actions log: the lead-campaign relaunch with a fixed conversion event (planned 28 Sep) has not happened; the 09/01 campaign is still the live one, so it is scored as is.",
 "Tàberg Falls":"Actions log: Shawal's 28 Sep restructure is live (new 'MoF - Broad (Acquire new customers) - 09/28/2026' at $50/day, Lookalike cut from $100 to $50/day). The Broad campaign is a prospecting Sales campaign scored on the Retargeting bands (decision 15); it crossed the $200 gate on about 2 Oct, so its first scored week is on 7 days of data.",
 "Paradise Pointe":"Shawal's 29 Sep change note: new 'MoF - LoL Sales Campaign - 09/28/26' at $50/day (account now $150/day); 1 Oct meeting: 3 purchases at about $40 each in its first days.",
 "Asheville River Cabins":"Account status: the connector lists ad account 615836588009747 as UNSETTLED (unpaid balance) and not queryable this week, so the account is scored from the CSV export. All three campaigns show Campaign delivery = not_delivering and the account spent $90 in 7 days against $80/day of budgets, so nothing is scored; the BoF campaign that was Scale (41.8x) last week is listed as paused in window until delivery resumes.",
 "Stay On 30A":"1 Oct meeting: named as a scaling candidate (as 'Stay on 38').",
}
def hgai_line(client):
    n=norm(client); hits=[b for b in HGAI if norm(b).find(n[:8])>=0 or n.find(norm(b.split(" - ")[0][11:]))>=0]
    if client in HGAI_LINES: return HGAI_LINES[client]+(f" (file: {hits[0]})" if hits else "")
    if hits: return f"HG AI notes: report on file ({', '.join(hits)}), not summarised."
    return "HG AI notes: none dropped in since the previous run."

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
            records.append(dict(client=client,am=am,acct=acct,cid=cid,name=r["name"],type=t,win=win,src="live",spend=r["spend"],results=results,gov=gov,govval=govval,state=state,diag=dg,notes="; ".join(notes),status=r["status"],freq=r["freq"]))
    else:
        for (a,cname),v in csvagg.items():
            if a!=acctname: continue
            t=ctype(None,cname); spend=v["Amount spent (USD)"]
            if t=="ToF": tof_spend+=spend; continue
            if t=="UNCLASSIFIED": unclassified.append((client,cname)); continue
            impr,clicks,purch,val,leads=v["Impressions"],v["Link clicks"],v["Purchases"],v["Purchases conversion value"],v["Leads"]
            st=csvstatus.get((a,cname),"unknown")
            if st!="ACTIVE":
                paused_by_client[client].append(dict(name=cname,type=t,win=csv_days,spend=spend,
                    results=f"{int(leads)} leads" if t==LEAD else f"{int(purch)} purchases",
                    gov=(f"CPL {money(spend/leads)}" if leads else "CPL —") if t==LEAD else (f"ROAS {x(val/spend)}" if spend else "ROAS —")))
                continue
            cpc=spend/clicks if clicks else None; cpm=spend/impr*1000 if impr else None; ctr=clicks/impr*100 if impr else None
            reach=v.get("Reach") or 0; freq=impr/reach if reach else None  # campaign frequency = impressions / reach summed over ad sets (approximate when audiences overlap)
            if t==LEAD:
                win=csv_days; gate=100; cpl=spend/leads if leads else None
                gov=f"CPL {money(cpl)}"; govval=cpl; results=f"{int(leads)} leads"; state,why=cpl_state(cpl,leads,spend); cpp=None
            else:
                win=csv_days; gate=200; roas=val/spend if spend else None; cpp=spend/purch if purch else None
                gov=f"ROAS {x(roas)}"; govval=roas; results=f"{int(purch)} purchases"; state,why=roas_state(roas,purch)
                if purch and not val: why=f"{int(purch)} purchases but no conversion value in the export, so ROAS reads 0.0x; check the Purchase value parameter before treating this as a performance Flag"
            if spend<gate: state="Under gate"; why=f"spend {money(spend)} < ${gate} gate"
            dg=diags(t,cpc,cpm,ctr,cpp,freq)+"; CTR here is link CTR from the export"
            notes=[f"source: CSV export {rs} to {re_} ({csv_days} days, not the {14 if t!=LEAD else 30}-day window), not live; provisional. Export carries Campaign delivery, so only active campaigns are scored"]
            if why: notes.append(why)
            records.append(dict(client=client,am=am,acct=acct,cid="",name=cname,type=t,win=win,src="csv",spend=spend,results=results,gov=gov,govval=govval,state=state,diag=dg,notes="; ".join(notes),status=st,freq=freq))
    ADV[client]=(am,acct,acctname,src,tof_spend)

for r in records:
    r["diff"],r["weeks"],r["difftxt"]=diff_for(r)
FREQ_FLAG=5.0  # Shawal, 2026-10-06: flag any Sales / Retargeting campaign whose frequency is above 5. Diagnostic + its own section; the ROAS state is unchanged.
for r in records:
    r["freq_flag"]=bool(r["type"] in SALES and r.get("freq") is not None and r["freq"]>FREQ_FLAG)
def freq_cell(r):
    if r["type"]==LEAD or r.get("freq") is None: return "—"
    return f"{r['freq']:.2f}"+(" ⚠️ > 5" if r["freq_flag"] else "")
freq_watch=sorted([r for r in records if r["freq_flag"]],key=lambda r:-r["freq"])
seen={(r["cid"] or (r["client"]+"||"+r["name"])) for r in records}
removed=[p for k,p in prev.items() if k not in seen and p["state"] in FLAGGED]

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
    return f"| {r['client']} | {r['am']} | {r['name']} | {r['type']} | {money(r['spend'],0)} / {r['win']}d | {r['gov']} | {r['state']} | {r['difftxt']} |"
L=[]
L.append(f"# Client Benchmark Review (advanced setups) — {TODAY}\n")
L.append(f"Run: 5 October 2026, third run, compared against {PREVFILE}. Live reads via the Meta connector (09:05 to 09:55 PT); CSV export {rs} to {re_} for the {sum(1 for v in ADV.values() if v[3]=='csv')} accounts the connector cannot read (Asheville River Cabins joins them this week, UNSETTLED). Scope: clients marked **Advanced** in the CRM \"Meta Ads\" column (Clients - Onboarding tab), re-read today: {len(ADV)+len(ADV_UNMAPPED)} clients, {len(ADV)} with an ad account. Scope unchanged since 28 Sep apart from three new Advanced clients in the CRM (Cabin Collective, Casey Key Resort, Arca Roatan) that have no ad account yet. Only Lead Gen (MoF) and Sales/Retargeting (BoF) campaigns are scored; IG Discovery and Keyword (ToF) spend is shown for context only.\n")
L.append("| Advanced clients | Live reads | From CSV | Campaigns scored | Under spend gate | Flag to Shawal | Review w/ HG AI | Monitor | Healthy | Scale w/ HG AI | Frequency over 5 |")
L.append("|---|---|---|---|---|---|---|---|---|---|---|")
L.append(f"| {len(ADV)} (+{len(ADV_UNMAPPED)} unmapped) | {sum(1 for v in ADV.values() if v[3]=='live')} | {sum(1 for v in ADV.values() if v[3]=='csv')} | {len(scored)} | {counts['Under gate']} | {counts['Flag to Shawal']} | {counts['Review w/ HG AI']} | {counts['Monitor']} | {counts['Healthy']} | {counts['Scale w/ HG AI']} | {len(freq_watch)} |\n")
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
L.append("Sales and Retargeting campaigns first, then Lead Gen. Within each, Flag to Shawal before Review w/ HG AI, highest spend first.\n")
L.append("| Client | AM | Campaign | Type | Spend / window | Governing metric | State | Status vs last week |")
L.append("|---|---|---|---|---|---|---|---|")
act=[r for r in records if r["state"] in ("Flag to Shawal","Review w/ HG AI")]
def act_key(r): return (0 if r["type"]!=LEAD else 1, ORDER[r["state"]], -r["spend"])  # decision 2026-09-23: sales/retargeting on top
for r in sorted(act,key=act_key): L.append(srow(r))
if removed:
    L.append("")
    L.append("Removed since last week (flagged on 28 Sep, not scored today): "+"; ".join(f"{p['client']}: {p['campaign']} ({p['state']})" for p in removed)+".")
L.append("")
L.append("## Scale candidates\n")
L.append("| Client | AM | Campaign | Type | Spend / window | Governing metric | State | Status vs last week |")
L.append("|---|---|---|---|---|---|---|---|")
sc=[r for r in records if r["state"]=="Scale w/ HG AI"]
for r in sorted(sc,key=act_key): L.append(srow(r))
if not sc: L.append("| — | | | | | | | |")
L.append("")
L.append("## Frequency watch (Sales / Retargeting above 5)\n")
L.append("Sales, Retargeting and MoF-lookalike campaigns whose 14-day frequency is above 5.0 (Shawal, 6 Oct 2026). Frequency does not change the ROAS state; this is the list to refresh creative or widen the audience on. The diagnostics column still notes anything above 3.0.\n")
L.append("| Client | AM | Campaign | Type | Frequency | Spend / window | Governing metric | State |")
L.append("|---|---|---|---|---|---|---|---|")
for r in freq_watch: L.append(f"| {r['client']} | {r['am']} | {r['name']} | {r['type']} | {r['freq']:.2f} | {money(r['spend'],0)} / {r['win']}d | {r['gov']} | {r['state']} |")
if not freq_watch: L.append("| — | | | | | | | |")
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
        L.append("| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |")
        L.append("|---|---|---|---|---|---|---|---|---|---|---|")
        for r in sorted(rs_,key=lambda r:(ORDER[r["state"]],-r["spend"])):
            L.append(f"| {r['name']} | {r['type']} | {r['win']}d | {money(r['spend'],0)} | {r['results']} | {r['gov']} | {freq_cell(r)} | {r['state']} | {r['diag']} | {r['notes']} | {r['difftxt']} |")
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
    L.append(hgai_line(c)+((" "+EXTRA_NOTES[c]) if c in EXTRA_NOTES else "")+"\n")
L.append("## Footer\n")
L.append(f"- Windows: Lead Gen last 30 days, Sales/Retargeting last 14 days (live). CSV accounts use the export period {rs} to {re_} ({csv_days} days) and are provisional.")
L.append("- Gates: $100 Lead Gen, $200 Sales/Retargeting. Campaigns under the gate are listed but not judged.")
L.append("- Classification: by campaign objective (OUTCOME_LEADS → Lead Gen; OUTCOME_SALES → Sales, split into Retargeting (BoF) or MoF lookalike by name; OUTCOME_TRAFFIC / OUTCOME_ENGAGEMENT → ToF, not scored). CSV accounts have no objective column, so classification there is by name.")
L.append("- Sales campaigns with an MoF or lookalike prefix are scored on the Retargeting ROAS bands because they optimise for purchases. The Benchmarks doc has no separate band for prospecting sales campaigns; confirm or add one.")
L.append("- CTR on live rows is Meta's CTR (all clicks), not link CTR. The doc's click-rate lines are probably link CTR, so treat the CTR diagnostic as indicative.")
L.append("- Frequency and cost per booking are diagnostics only and do not change the state (decision 2026-09-21). From 2026-10-06 (Shawal) every Sales / Retargeting row shows its frequency, and any value above 5.0 is marked ⚠️ in that column and listed in the Frequency watch section; CSV rows use impressions / reach summed over ad sets, which overstates frequency where ad sets overlap.")
L.append("- Only campaigns live (ACTIVE) at run time are scored. Paused campaigns that spent inside the window are listed per client as \"Paused in window\" and never enter Action needed or the counts (decision 2026-09-23).")
L.append(f"- Unclassified campaigns: {', '.join(f'{c}: {n}' for c,n in unclassified) if unclassified else 'none'}.")
L.append(f"- Previous report: {PREVFILE}. Diff joined on campaign_id for live rows and client + campaign name for CSV rows. Diff counts: {sum(1 for r in records if r['diff']=='new')} new, {sum(1 for r in records if r['diff']=='still_open')} still open, {sum(1 for r in records if r['diff']=='fixed')} fixed, {sum(1 for r in records if r['diff']=='unchanged')} unchanged, {len(removed)} removed.")
L.append("- Scope changes vs 28 Sep: "+("; ".join(f"{c} dropped ({why})" for c,why in ADV_DROPPED.items()) if ADV_DROPPED else "none; the CRM now lists 27 Advanced clients, three of them new (Cabin Collective, Casey Key Resort, Arca Roatan) and not yet launched")+". Advanced in the CRM but with no ad account mapping in PROJECT.md section 5, not scored: "+", ".join(f"{c} (AM {am})" for c,am in ADV_UNMAPPED.items())+".")
L.append("- HG AI reports read from `HG AI Reports/` at the project root, dated since the previous run: "+(", ".join(HGAI) if HGAI else "none")+".")
L.append("- Selah Place's prospecting campaign (paused this week) is named with pipes in Meta (\"SP | Prospecting Test | LAL + Interests x Creative | 09-2026\"); shown here with slashes.")
L.append("- Meeting notes: every \"Meta Ads Strategy\", \"Meta Ads Sync\" or \"Meta Ads x HiddenGem AI Sync\" calendar event since the previous run that has a \"Notes by Gemini\" attachment, read via Drive. Client names are matched with an alias list (Flow Home = FLOHOM, Tabber / Tipik Falls / Debug Falls = Tàberg Falls, Sailor Place = Selah Place, Stay on 38 = Stay On 30A, Ashwood River Cabins = Asheville River Cabins).")
L.append(f"- Monthly ROI context from `Monthly ROI data/` ({', '.join(sorted({p for v in roi.values() for p in v}, key=lambda p:(p.split()[-1], p[:3] in ('Oct','Nov','Dec'), p[:3]=='Sep', p[:3]=='Aug')))}). Revenue there comes from the Client Performance Tracking sheet, not the pixel, so its ROAS is not comparable to the pixel ROAS above.")
open(f"{OUT}/{TODAY}-client-benchmark.md","w",encoding="utf-8").write("\n".join(L)+"\n")
with open(f"{OUT}/{TODAY}-client-benchmark.csv","w",newline="",encoding="utf-8") as fh:
    w=csv.writer(fh); w.writerow("run_date,client,am,ad_account_id,campaign_id,campaign,type,window_days,source,spend,results,governing_metric,governing_value,state,diagnostics,diff_status,weeks_open,notes,frequency,freq_flag".split(","))
    for r in records:
        gm="cpl" if r["type"]==LEAD else "roas"
        w.writerow([TODAY,r["client"],r["am"],r["acct"],r["cid"],r["name"],r["type"],r["win"],r["src"],f"{r['spend']:.2f}",r["results"],gm,"" if r["govval"] is None else f"{r['govval']:.2f}",r["state"],r["diag"],r["diff"],r["weeks"],r["notes"],"" if r.get("freq") is None else f"{r['freq']:.2f}","yes" if r["freq_flag"] else ""])
print("records",len(records),"counts",dict(counts)); print("unclassified",unclassified)
