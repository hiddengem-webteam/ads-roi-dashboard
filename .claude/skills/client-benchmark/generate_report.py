import csv, json, glob, os, re, collections, datetime
ROOT=os.path.join(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","..","..")),"weekly")  # <repo>/weekly
SP=os.path.dirname(os.path.abspath(__file__))
TODAY="2026-10-19"
PREV_DATE="2026-10-13"
OUT=f"{ROOT}/Client Benchmark Reviews (advanced setups)/Weekly Checks"
ADV={ # CRM "Clients - Onboarding" tab, Meta Ads = Advanced, read 2026-10-19: name -> (AM, account id, account name, connector)
 "FLOHOM":("Makenna","2100710320122219","FLOHOM Ads","live"),
 "Treetop Escapes":("Makenna","967636478877602","Treetop Escapes Ads","live"),
 "Paradise Pointe":("Makenna","1585826092078255","Paradise Pointe Ads","live"),
 "Asheville River Cabins":("Charlotte","615836588009747","Asheville River Cabins Ads","live"),
 "Green Springs Inn":("Alicia","1390516335151357","Green Springs Inn","live"),
 "Starlight Haven Hot Springs":("Charlotte","901138032027913","Starlight Haven Hot Springs","live"),
 "Starlight Haven Weiss Lake":("Charlotte","74756899","Starlight Haven Weiss Lake","live"),
 "Stay Saluda NC":("Makenna","1863632561215857","Stay Saluda Ads","live"),
 "Endless Stays":("Nicole","896372356081479","Endless Stays","live"),
 "Stay On 30A":("Charlotte","25640434272252212","Stay on 30a Ads","live"),
 "AwayFrames":("Alicia","2471256056603833","Awayframes Ad Account","live"),
 "Bison Ridge Retreat":("Chiara","950241787963535","Bison Ridge Retreat Ad Account","live"),
 "American River Resort":("Nicole","953162737054331","American River Resort","live"),
 "Tàberg Falls":("Alicia","827872700004659","Táberg Falls","live"),
 "Ponderosa Pines Resort":("Anna","1058846326445255","Ponderosa Pines Resort","live"),
 "The Outpost":("Anna","1530849534802936","The Outpost Grand Canyon","live"),
 "Selah Place":("Alicia","1275283434220508","Selah.place","live"),
 "Ridge & Falls":("Makenna","1313401330776046","Ridge & Falls ad account","live"),
 "Little River Landing":("Makenna","884285717873613","Little River Landing","live"),
 "North Star Lodge & Resort":("Charlotte","2003562593933799","North Star Lodge & Resort Ads","live"),
 "Walden Retreats":("Anna","973261794434226","Walden Retreats","live"),
}
# Advanced in the CRM but with no ad account in PROJECT.md section 5 (footer only)
ADV_UNMAPPED={"Treetop Hideaways":"Kristal","Glasscombe":"Charlotte","Cabin Collective":"Chiara","Casey Key Resort":"Alicia","Arca Roatan":"Anna"}
# Was Advanced on 2026-09-21, now Basic in the CRM: dropped from scope this run
ADV_DROPPED={"Sunapee Stays":"CRM Meta Ads column now Basic, was Advanced on 13 Oct; account 651114096215889 still runs $50/day and stays in the spend and pixel checks"}
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


# ---------- This month: direct revenue and promo codes from the HiddenGem AI platform ----------
# pms_mtd.json is the saved result of pms_mtd.sql (run through the Supabase
# connector against the HiddenGem AI project for this run date). One row per
# tenant: month-to-date direct revenue by booking date, the same day span of
# the previous month, and promo-code use where the PMS stores codes.
MTD_FILE=f"{SP}/pms_mtd.json"
MTD={}
if os.path.exists(MTD_FILE):
    for row in json.load(open(MTD_FILE,encoding="utf-8")):
        MTD[norm(row["name"])]=row
MTD_ALIAS={"flohom":"flohom","stayon30a":"stayon30a","staysaludanc":"staysaluda","awayframes":"awayframes",
           "northstarlodgeresort":"northstarlodgeresort","tbergfalls":"tbergfalls","staysouthenillinois":"staysouthernillinois"}
def mtd_for(client):
    n=MTD_ALIAS.get(norm(client),norm(client))
    if n in MTD: return MTD[n]
    for k,v in MTD.items():
        if k.startswith(n) or n.startswith(k): return v
    return None
def _d(iso): 
    d=datetime.date.fromisoformat(iso); return f"{d.day} {d.strftime('%b')}"
def month_line(client):
    m=mtd_for(client)
    if not m: return "This month: no PMS connection on the HiddenGem AI platform, so direct revenue and promo codes are not tracked here."
    span=f"booked {_d(m['month_start'])}–{_d(m['run_date'])}"; pspan=f"{_d(m['prev_start'])}–{_d(m['prev_end'])}"
    rev=float(m["mtd_rev"] or 0); prev=float(m["prev_rev"] or 0)
    pct=m.get("vs_prev_pct")
    trend=(f"{'+' if float(pct)>=0 else '−'}{abs(float(pct)):.0f}% vs {pspan} ({money(prev,0)} from {m['prev_bk']} bookings)" if pct not in (None,"") 
           else f"no direct revenue in {pspan} to compare against")
    if m["promo_source"]=="codes":
        promo=f"{m['promo_uses']} uses ({m['promo_codes']})" if m["promo_uses"] else "0 uses"
    elif m["promo_source"]=="count only":
        promo=f"{m['promo_uses']} uses (Hostaway does not store code names)"
    else:
        promo=f"not tracked by {m['provider']}"
    return f"This month ({span}): direct revenue {money(rev,0)} from {m['mtd_bk']} bookings, {trend} · promo codes: {promo}."
def mtd_csv(client):
    m=mtd_for(client)
    if not m: return ["","","","",""]
    return [f"{float(m['mtd_rev'] or 0):.0f}", str(m["mtd_bk"]), "" if m.get("vs_prev_pct") in (None,"") else str(m["vs_prev_pct"]), str(m["promo_uses"]), m.get("promo_codes") or ""]

# ---------- Weekly Meta Ads meeting notes (Gemini) ----------
# One entry per meeting doc found on the calendar since the previous run. Oldest first.
MEETINGS=[
 dict(title="Meta Ads Strategy", date="2026-10-14", doc_id="14s5-eW49GhSjyoeunooM1-kBX7O_Rr4X8pE_rS9WmhE", file=f"{SP}/meeting1.json"),
]
# How Gemini spells clients in the notes. Lower-case substrings.
ALIASES={
 "FLOHOM":["flohom","flow home","flo home"],
 "Tàberg Falls":["taberg","tabber","taber falls","tàberg","táberg","tipik falls","debug falls"],
 "Stay On 30A":["30a","stay on 38"],
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
 "Walden Retreats":["walden"],
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
    p=prev.get(key) or prev.get(rec["client"]+"||"+rec["name"])  # CSV rows last week, live rows this week: fall back to client + campaign name
    if p is None: return ("new",1 if rec["state"] in FLAGGED else 0,"New, not in the 13 Oct run")
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
HGAI_LINES={}
EXTRA_NOTES={
 "Selah Place":"Actions log: the BoF retargeting budget was raised on 13 Oct (planned move of the paused test's budget, Done; the spend check reads $30/day today), so this 14-day window is the first mostly on the higher budget. BoF 11.7x on 8 purchases sits below the 15x Scale line; the paused prospecting test's trailing spend (1.1x) is listed, not scored.",
 "Ridge & Falls":"Actions log: the lead-campaign relaunch with a fixed conversion event (planned 28 Sep) has still not happened; the 09/01 campaign is the live one and is in its fourth week at Flag ($3.51 CPL on 30 days, $2.76 on 14). October direct revenue is up on a very small base.",
 "Tàberg Falls":"Budgets were cut on 13 Oct (today $250/day: Giveaway $50, Leads $50, Lookalike $50, Broad $50, BoF $50), so this 14-day window is mostly on the cut budgets. The Broad prospecting campaign (3.9x on 2 purchases, $698) moves to Review; it is scored on the Retargeting bands (see footer).",
 "Paradise Pointe":"BoF 3.7x, third week at Review, frequency 5.7 and still the only Frequency-watch row. September ROI file: Meta recorded no revenue for 12 retargeting purchases; the purchase-value check (decision 26) is still open, so the live ROAS may understate.",
 "Asheville River Cabins":"14 Oct Strategy: Leshan's custom script in the Cloudbeds account recorded Facebook click IDs on reservations; sending them to Meta through CAPI needs host API access, which Shawal is requesting. The leads campaign slips from Scale to Healthy at $0.30 (band edge); BoF 43.1x holds.",
 "The Outpost":"The second BoF campaign (10/08, $10/day) runs beside the 08/29 one; both are under the $200 gate with 0 purchases in 14 days. Decision 30 (pause the old one) is still open.",
 "Walden Retreats":"The wedding-lead test (TOF Wedding Leads 10.8.26, $24/day) crosses the $100 gate for the first time at $10.07 CPL on 20 leads. Wedding enquiries are a different lead type from the email-list leads the CPL bands were set for, so read the Flag as a prompt to agree a wedding CPL target with Anna, not as a failure. The alt-audience variant (10.9.26) is paused. BoF 56.9x on $118, under the gate.",
 "North Star Lodge & Resort":"14 Oct Strategy: the full plugin, script and API set is installed (Leshan); BoF spend is low ($70 in 14 days) and no BoF reservation has come through yet, though clicks are visible in the platform.",
 "FLOHOM":"BoF 4.0x on 14 days (6 purchases) against 7.1x on 30 days: the last two weeks are the soft patch, and October direct revenue is 25% below September's same span. The [Myrtle Beach] lookalike slips to Monitor at 6.0x on 1 purchase.",
 "Treetop Escapes":"BoF 2.5x on 3 purchases in 14 days (7.1x on 30), first Review since the 28 Sep run (4.7x then). October direct revenue is up 25% on September's span, so bookings are arriving that the pixel does not credit to the campaign.",
 "Stay Saluda NC":"BoF 4.3x on 3 purchases with frequency 4.7 and climbing. The Saluda GHL hosts still fire the Inspired Retreats pixel (pixel check, week 5).",
 "Ponderosa Pines Resort":"BoF 7.6x on 14 days (15.2x on 30): a 14-day dip takes it from Scale to Monitor; frequency 3.1.",
 "American River Resort":"Both campaigns stopped between 15 and 19 Oct (spend check: $0/day live today). The lead campaign spent $551 in the window and is paused now, so nothing is scored. Confirm with Nicole whether this is a pause or an offboarding.",
 "Endless Stays":"BoF 3.1x, third week at Review. October direct revenue is $26k against $5.4k in September's same span (+381%), so direct bookings are landing outside the pixel's view; check the purchase event on the Hospitable booking flow.",
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
seen={(r["cid"] or (r["client"]+"||"+r["name"])) for r in records}|{(r["client"]+"||"+r["name"]) for r in records}
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
L.append(f"Run: 19 October 2026 (Monday), fifth run, compared against {PREVFILE}. Live reads through the Meta Marketing API with the HiddenGem-Claude system user, now the standing data path (`scripts/pull-campaign-insights.mts`, 09:37 to 09:38 PT); every account is live and the CSV export {rs} to {re_} was not needed for scoring. Scope: clients marked **Advanced** in the CRM \"Meta Ads\" column (Clients - Onboarding tab), re-read today: {len(ADV)+len(ADV_UNMAPPED)} clients, {len(ADV)} with an ad account. Sunapee Stays leaves scope (CRM now says Basic). Five Advanced clients in the CRM have no ad account yet. Only Lead Gen (MoF) and Sales/Retargeting (BoF) campaigns are scored; IG Discovery and Keyword (ToF) spend is shown for context only.\n")
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
    L.append("Removed since last week (flagged on 13 Oct, not scored today): "+"; ".join(f"{p['client']}: {p['campaign']} ({p['state']})" for p in removed)+".")
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
    L.append(month_line(c)+"\n")
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
L.append("- Data path: Marketing API v21.0 insights at campaign level through `scripts/pull-campaign-insights.mts` (purchases = omni_purchase, leads = lead, ROAS = purchase_roas, link clicks = inline_link_clicks), the same fields the claude.ai connector exposed. The connector is no longer used for this report (Shawal, 2026-10-19).")
L.append("- CTR on live rows is Meta's CTR (all clicks), not link CTR. The doc's click-rate lines are probably link CTR, so treat the CTR diagnostic as indicative.")
L.append("- Frequency and cost per booking are diagnostics only and do not change the state (decision 2026-09-21). From 2026-10-06 (Shawal) every Sales / Retargeting row shows its frequency, and any value above 5.0 is marked ⚠️ in that column and listed in the Frequency watch section; CSV rows use impressions / reach summed over ad sets, which overstates frequency where ad sets overlap.")
L.append("- Only campaigns live (ACTIVE) at run time are scored. Paused campaigns that spent inside the window are listed per client as \"Paused in window\" and never enter Action needed or the counts (decision 2026-09-23).")
L.append(f"- Unclassified campaigns: {', '.join(f'{c}: {n}' for c,n in unclassified) if unclassified else 'none'}.")
L.append(f"- Previous report: {PREVFILE}. Diff joined on campaign_id for live rows and client + campaign name for CSV rows. Diff counts: {sum(1 for r in records if r['diff']=='new')} new, {sum(1 for r in records if r['diff']=='still_open')} still open, {sum(1 for r in records if r['diff']=='fixed')} fixed, {sum(1 for r in records if r['diff']=='unchanged')} unchanged, {len(removed)} removed.")
L.append("- Scope changes vs 13 Oct: "+("; ".join(f"{c} dropped ({why})" for c,why in ADV_DROPPED.items()) if ADV_DROPPED else "none")+". Advanced in the CRM but with no ad account mapping in PROJECT.md section 5, not scored: "+", ".join(f"{c} (AM {am})" for c,am in ADV_UNMAPPED.items())+".")
L.append("- HG AI reports read from `HG AI Reports/` at the project root, dated since the previous run: "+(", ".join(HGAI) if HGAI else "none")+".")
L.append("- Selah Place's prospecting campaign (paused this week) is named with pipes in Meta (\"SP | Prospecting Test | LAL + Interests x Creative | 09-2026\"); shown here with slashes.")
L.append("- Meeting notes: every \"Meta Ads Strategy\", \"Meta Ads Sync\" or \"Meta Ads x HiddenGem AI Sync\" calendar event since the previous run that has a \"Notes by Gemini\" attachment, read via Drive. Client names are matched with an alias list (Flow Home = FLOHOM, Tabber / Tipik Falls / Debug Falls = Tàberg Falls, Sailor Place = Selah Place, Stay on 38 = Stay On 30A, Ashwood River Cabins = Asheville River Cabins).")
L.append("- This month line: direct booking revenue by booking date from the HiddenGem AI platform (pms_bookings, platform direct/OTA rules, tenants on a shared PMS account narrowed to their own properties), month to date at the run date, against the same day span of the previous month. Promo codes come from the booking payload: Guesty stores the code, Hostaway only a coupon id (counted, no names), Hospitable and Cloudbeds nothing. Pulled with pms_mtd.sql through the Supabase connector." + (" Clients without a PMS connection on the platform show no figures." if any(mtd_for(c) is None for c in ADV) else ""))
L.append(f"- Monthly ROI context from `Monthly ROI data/` ({', '.join(sorted({p for v in roi.values() for p in v}, key=lambda p:(p.split()[-1], p[:3] in ('Oct','Nov','Dec'), p[:3]=='Sep', p[:3]=='Aug')))}). Revenue there comes from the Client Performance Tracking sheet, not the pixel, so its ROAS is not comparable to the pixel ROAS above.")
open(f"{OUT}/{TODAY}-client-benchmark.md","w",encoding="utf-8").write("\n".join(L)+"\n")
with open(f"{OUT}/{TODAY}-client-benchmark.csv","w",newline="",encoding="utf-8") as fh:
    w=csv.writer(fh); w.writerow("run_date,client,am,ad_account_id,campaign_id,campaign,type,window_days,source,spend,results,governing_metric,governing_value,state,diagnostics,diff_status,weeks_open,notes,frequency,freq_flag,mtd_direct_revenue,mtd_direct_bookings,mtd_vs_prev_month_pct,mtd_promo_uses,mtd_promo_codes".split(","))
    for r in records:
        gm="cpl" if r["type"]==LEAD else "roas"
        w.writerow([TODAY,r["client"],r["am"],r["acct"],r["cid"],r["name"],r["type"],r["win"],r["src"],f"{r['spend']:.2f}",r["results"],gm,"" if r["govval"] is None else f"{r['govval']:.2f}",r["state"],r["diag"],r["diff"],r["weeks"],r["notes"],"" if r.get("freq") is None else f"{r['freq']:.2f}","yes" if r["freq_flag"] else ""]+mtd_csv(r["client"]))
print("records",len(records),"counts",dict(counts)); print("unclassified",unclassified)
