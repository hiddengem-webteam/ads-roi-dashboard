import csv, json, glob, os, re, collections, datetime
ROOT=os.path.join(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","..","..")),"weekly")  # <repo>/weekly
SP=os.path.dirname(os.path.abspath(__file__))
TODAY="2026-11-16"
PREV_DATE="2026-11-09"
OUT=f"{ROOT}/Client Benchmark Reviews (advanced setups)/Weekly Checks"
ADV={ # CRM "Clients - Onboarding" tab, Meta Ads = Advanced, read 2026-11-16 (Bison Ridge now Basic; Gooseberry Lodges, Dunya Camp and Arca Boutique Hotel mapped 2026-11-16, Shawal): name -> (AM, account id, account name, connector)
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
 "American River Resort":("Nicole","953162737054331","American River Resort","live"),
 "Tàberg Falls":("Alicia","827872700004659","Táberg Falls","live"),
 "Ponderosa Pines Resort":("Anna","1058846326445255","Ponderosa Pines Resort","live"),
 "The Outpost":("Anna","1530849534802936","The Outpost Grand Canyon","live"),
 "Selah Place":("Alicia","1275283434220508","Selah.place","live"),
 "Ridge & Falls":("Makenna","1313401330776046","Ridge & Falls ad account","live"),
 "Little River Landing":("Makenna","884285717873613","Little River Landing","live"),
 "North Star Lodge & Resort":("Charlotte","2003562593933799","North Star Lodge & Resort Ads","live"),
 "Walden Retreats":("Anna","973261794434226","Walden Retreats","live"),
 "Glasscombe":("Charlotte","2030318804465316","Glasscombe","live"),
 "Cabin Collective":("Chiara","2194562394139883","Cabin Collective","live"),
 "Sunapee Stays":("Charlotte","651114096215889","Sunapee Stays Ads Account","live"),
 "Gooseberry Lodges":("Alicia","701051796368186","Gooseberry Ad Account","live"),
 "Dunya Camp":("Chiara","629838998232110","Dunya Camp","live"),
 "Arca Boutique Hotel":("Anna","1003623765640520","Arca Ad account","live"),
}
# Advanced in the CRM but with no ad account in PROJECT.md section 5 (footer only)
ADV_UNMAPPED={"Treetop Hideaways":"Kristal","Casey Key Resort":"—","Nine Pines Retreat":"Nicole","Lundy Farm":"Charlotte","The Preserve":"Alicia","Kimpton Mas Olas Resort":"Charlotte"}
# Was Advanced on 2026-09-21, now Basic in the CRM: dropped from scope this run
ADV_DROPPED={"Bison Ridge Retreat":"Basic in the CRM since 12 Nov"}
# Sunapee Stays reads Basic in the CRM since 19 Oct but Shawal (2026-10-26) keeps it in the advanced reporting, so it is in ADV above
ADV_OVERRIDE={}  # Sunapee Stays read Basic 19 Oct to 9 Nov and was kept by override (2026-10-26); the CRM reads Advanced again on 16 Nov
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
        if re.search(r"mof|lookalike",n): return "Prospecting (MoF lookalike)"
        return "Sales"
    if obj in ("OUTCOME_TRAFFIC","OUTCOME_ENGAGEMENT") or re.search(r"discovery|giveaway|keyword|tof|follow",n): return "ToF"
    return "UNCLASSIFIED"
LEAD, SALES = "Lead Gen (MoF)", ("Retargeting (BoF)","Prospecting (MoF lookalike)","Sales")
DISC="Discovery (ToF + MoF leads)"  # one bucket row per client: giveaway + lead spend against promo-code revenue (Meta Ads Strategy 2026-10-28; built 2026-10-30); context only since 2026-11-04
# 2026-11-04 (Shawal): only Sales-objective campaigns (Retargeting, Prospecting, Sales) carry a state. Lead Gen rows and
# the Discovery bucket rows stay in the report for context (CPL, leads, promo ROAS) but never enter Action needed,
# Scale candidates or the counts. Reason: the Discovery promo ROAS misreads clients whose PMS drops the code name
# (Hostaway) and launch-month accounts, and cost per lead was already retired as a state on 28 Oct.
NS_LEAD="Not scored (lead gen)"; NS_DISC="Not scored (discovery)"
def lead_state(cpl,leads,spend):
    return NS_LEAD,"only Sales-objective campaigns are scored (Shawal, 4 Nov 2026); leads and CPL shown for context"
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
ORDER={"Flag to Shawal":0,"Review w/ HG AI":1,"Monitor":2,"Healthy":3,"Scale w/ HG AI":4,"Under gate":5,NS_LEAD:6,NS_DISC:7,"Tracked in Discovery":8,"No promo data":9}
UNSCORED=("Under gate",NS_LEAD,NS_DISC,"Tracked in Discovery","No promo data")
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

# ---------- campaign creators (client-run campaigns are listed, never scored; Shawal 2026-10-19) ----------
# creators.json comes from pull-campaign-insights.mts (activity log, last 180 days).
# A campaign whose creator is not on the HiddenGem team is client-run. Unknown creator = scored as usual.
HG_TEAM={"hiddengem-claude","shawal nazir","dustin baker","gillian conley","leshan patterson","ananya arora","makenna moran","nicole","alicia","charlotte","chiara","kristal","anna","vicky","lily","lucca","pooja","aidan","brandon","kyle","anhtuan","henry"}
HG_EXACT={"john martin"}  # Shawal's second Meta profile (Shawal, 2026-11-16); exact match only, so other Johns are not treated as HiddenGem
def is_hg(name):
    n=(name or "").lower().strip()
    return n in HG_EXACT or any(n==h or n.split(" ")[0]==h.split(" ")[0] for h in HG_TEAM)
CREATORS={}
if os.path.exists(f"{SP}/creators.json"):
    CREATORS=json.load(open(f"{SP}/creators.json",encoding="utf-8"))
client_run=collections.defaultdict(list)
# Campaigns deliberately left as they are, listed under the client but never scored (spend still counts in the Blended 30d line).
DEFERRED={
 "120256376163180405":"optimises on Dunya Camp's custom 'Step 2' event, not Purchase, so purchase ROAS does not apply; part of the older custom-event funnel left as is (Shawal, 12 Nov 2026)",
 "120247876023700405":"optimises on Dunya Camp's custom 'Step 3' event; part of the older custom-event funnel left as is (Shawal, 12 Nov 2026)",
}
deferred=collections.defaultdict(list)

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
 dict(title="Meta Ads Sync", date="2026-11-11", doc_id="1Nf-776jbXwMmez7LsipGwzQ0Ft8U-dAGpe7mfNkJiu8", file=f"{SP}/meeting1.json"),
 dict(title="Meta Ads Strategy", date="2026-11-11", doc_id="1hD7LB51qRrElHamNsw7yOW20Zd-cOs5a5LJvceuaQdU", file=f"{SP}/meeting2.json"),
]
# How Gemini spells clients in the notes. Lower-case substrings.
ALIASES={
 "FLOHOM":["flohom","flow home","flo home"],
 "Tàberg Falls":["taberg","tabber","taber falls","tàberg","táberg","tipik falls","debug falls","tab fel","tab fell"],
 "Stay On 30A":["30a","stay on 38","stay on 3a"],
 "Starlight Haven Hot Springs":["starlight","hot springs","starlight haven"],
 "Starlight Haven Weiss Lake":["starlight","weiss"],
 "Stay Saluda NC":["saluda","stay saluted"],
 "American River Resort":["american river"],
 "Asheville River Cabins":["asheville","ashwood river"],
 "Green Springs Inn":["green springs"],
 "Treetop Escapes":["treetop","tree top","tree tops"],
 "Paradise Pointe":["paradise pointe","paradise point"],
 "Endless Stays":["endless"],  # "Endless Days" (11 Nov) matches
 "AwayFrames":["awayframes","away frames","waveframes"],
 "Bison Ridge Retreat":["bison"],
 "Ponderosa Pines Resort":["ponderosa"],
 "The Outpost":["outpost"],
 "Selah Place":["selah","sailor place"],
 "Sunapee Stays":["sunapee"],
 "Ridge & Falls":["ridge & falls","ridge and falls","ridge falls"],
 "Little River Landing":["little river"],
 "North Star Lodge & Resort":["north star","northstar"],
 "Walden Retreats":["walden"],
 "Glasscombe":["glasscombe","glasscom"],
 "Gooseberry Lodges":["gooseberry"],
 "Dunya Camp":["dunya"],
 "Arca Boutique Hotel":["arca"],
 "Cabin Collective":["cabin collective"],
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
    if p is None: return ("new",1 if rec["state"] in FLAGGED else 0,f"New, not in the {_d(PREV_DATE)} run")
    ps=p["state"]; pw=int(p.get("weeks_open") or 0)
    if rec["state"] in (NS_LEAD,NS_DISC): return ("retired" if ps in FLAGGED else "unchanged",0,(f"No longer scored (4 Nov decision: Sales-objective campaigns only), was {ps}" if ps in FLAGGED else "Unchanged" if ps==rec["state"] else f"Was {ps}, not scored since 4 Nov"))
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
 "Stay On 30A":"BoF moves up from Healthy (14.7x) to Scale at 15.3x on 6 purchases ($2,062 in 14 days), just over the Scale line, frequency 4.3. The LoL lookalike holds Healthy at 11.6x on 6 purchases ($2,743; 13.9x last week). Budget unchanged at $500/day. Direct revenue month to date $167.0k, +12% on the same days of October; EARLY BIRD DIRECT ×14, VIP100 ×9 and WELCOME100 ×8 carry the coded bookings.",
 "Tàberg Falls":"Lookalike up from Monitor (6.0x) to Healthy at 10.0x on 8 purchases ($1,381), its third week at $100/day. BoF slips inside Monitor from 7.3x to 5.3x on 4 purchases ($1,392), frequency 3.2; one more week down puts it in Review. Discovery read (context only) 0.7x: $3,019 of giveaway and lead spend in 30 days against one Hostaway coupon booking ($2,008), so last week's question for Alicia (does the sign-up code work on the booking engine?) is still open. Direct revenue month to date −20% on October.",
 "Endless Stays":"BoF eases from Flag (0 purchases on $1,034) to Review at 4.1x on 2 purchases ($961 in 14 days), open seven weeks. On 13 Nov Shawal cut BoF from $75 to $50 and moved $50/day into a new lookalike (0 purchases on $140 in three days, under the gate). Month-to-date direct revenue is $39.8k, +105% on October (19 bookings), while the pixel's Purchases arrive server-side only (HG AI CAPI), so attribution, not demand, is the open question.",
 "AwayFrames":"The 10/29 lookalike is Fixed: from Flag (1.9x) to Healthy at 9.3x on 5 purchases ($686), its third week. BoF up from Monitor (7.3x) to Healthy at 10.2x on 7 purchases ($698), frequency 4.5. Both clear the 7x target set for Awayframes at the 11 Nov Strategy meeting. Direct revenue month to date $26.1k, +222% on October. Discovery read 0.0x: no Hostaway coupon booking in 30 days on $2,482 of giveaway and lead spend.",
 "Paradise Pointe":"The LoL lookalike stays Scale at 20.8x on 15 purchases ($864), now at $100/day after Shawal doubled it on 12 and 13 Nov. BoF slips from 15.0x to 13.2x, Healthy, on 9 purchases ($681); its frequency of 5.45 is the highest in the review (Frequency watch, week 3). Discovery read (context only) 51.0x: WELCOME100 ×71 ($78.2k) in 30 days on $1,571. Direct revenue month to date +22% on October.",
 "Treetop Escapes":"BoF slips from Scale (18.1x) to Healthy at 13.5x on 10 purchases ($553), frequency 3.7, still well above the 5x target from the 11 Nov Strategy meeting. The new 13 Nov lookalike ($20/day, funded by cutting the lead campaign from $30 to $10) has 1 purchase on $53, under the gate. Direct revenue month to date flat on October ($28.2k). Discovery read (context only) 9.9x: WELCOME100 ×15 on $1,747.",
 "Ponderosa Pines Resort":"BoF holds Monitor at 7.5x on 13 purchases ($552). Read it as an upper bound: the pixel check still shows the Newbook confirmation firing about 1.8 browser Purchases per booking. The new 13 Nov lookalike ($40/day) has 1 purchase on $101, under the gate. Leads $1.31 on 440. Direct revenue month to date +9% on October. No promo data (Newbook stores no code).",
 "Starlight Haven Hot Springs":"BoF holds Scale at 18.3x on 9 purchases ($275), up from 15.5x. On 12 Nov the lead campaign's interest and lookalike ad sets were paused and Broad US Engagers raised to $30; leads $0.32 on 2,815.",
 "FLOHOM":"BoF is Fixed: from Review (3.7x) to Healthy at 10.0x on 7 purchases ($706). The Myrtle Beach lookalike drops from Healthy (8.2x) to Review at 3.3x on 1 purchase ($282), a new Action row; the main lookalike slips from Healthy (12.0x) to Monitor at 6.2x on 7 purchases ($704). Direct revenue month to date $39.0k, −37% on October (49 bookings against 67), better than last week's −66%. Budget $140/day.",
 "Stay Saluda NC":"BoF slips from Scale (20.1x) to Healthy at 14.4x on 9 purchases ($420), frequency 4.6, still twice the 7x target set at the 11 Nov Strategy meeting. The new 13 Nov lookalike ($20/day) has 1 purchase on $54, under the gate. Discovery read (context only) 9.7x: ENJOY10 ×16 and WELCOME10 ×3 on $1,494. Direct revenue month to date +51% on October.",
 "Asheville River Cabins":"The 06/08 campaign that scored Scale as BoF retargeting (26.4x) was renamed 'MoF - Broad - 06/08/26' with no audience on 12 Nov (Shawal), so it now reads as Prospecting. Its 26.2x on 21 purchases ($556) is mostly retargeting history; the next two weeks show what the broad audience does. Retargeting restarted as 'BoF - Website Retargeting Campaign - 12/11/26' (Website Visitors 180D, value optimisation) at $20/day from 13 Nov: 1 purchase on $63, under the gate. All Purchases are browser-side: Leshan said on 11 Nov that the Cloudbeds API is not enabled on Asheville's account, so the HG AI CAPI cannot send yet.",
 "Little River Landing":"BoF stays Flag, week 2: 1.4x on 1 purchase ($220 in 14 days). Tracking is still the first fix: 5 Purchase in 28 days against 11 PMS online bookings (45%) with the HG AI CAPI off (pixel check). On 13 Nov BoF went to $20 and a $20 lookalike was added (0 purchases on $49), so the Sales budget is $40/day before the CAPI is on. Discovery read 0.2x on $1,937.",
 "Starlight Haven Weiss Lake":"BoF holds Scale at 17.6x on 23 purchases ($644), down from 26.2x. The lead campaign's interest and lookalike ad sets were paused on 12 Nov in favour of Broad US Engagers; leads $1.15 on 655.",
 "Selah Place":"HiddenGem's BoF jumps from Monitor (5.6x) to Scale at 17.0x on 14 purchases ($412), frequency 4.1. Read it with care: the pixel's server Purchases still run about 2.5x the PMS bookings (HG AI CAPI plus Hostaway's CAPI). The new 13 Nov lookalike ($20/day) is under the gate. The client paused both Black Walnut campaigns and one Willow ad set on 14 Nov, so the account is $345/day, $100 of it HiddenGem's four campaigns.",
 "Ridge & Falls":"BoF holds Scale at 22.9x on 12 purchases ($211), frequency 5.34 (Frequency watch, week 2). The ROAS is inflated: the pixel receives about 1.8 server Purchases per PMS booking (two senders). Direct revenue month to date $3.1k from 8 bookings. Discovery read 0.0x: HELLO10 ×4 and STAY10 ×1 are not sign-up codes.",
 "Sunapee Stays":"BoF under the gate, 0 purchases on $114; Charlotte cut the account from $50 to $30/day on 10 Nov. Month-to-date direct revenue $3.9k against $20.1k on the same days of October (−81%).",
 "Green Springs Inn":"BoF under the gate at 35.9x on 9 purchases ($139). Discovery read (context only) 16.7x on 29 Hostaway coupon bookings (no code names). Direct revenue month to date +22% on October.",
 "Gooseberry Lodges":"First week in the review (mapped 16 Nov). BoF under the gate, 0 purchases on $140 in 14 days, at $25/day since Alicia's 12 Nov increase. The pixel is browser-only and Little Hotelier has no API, so the HG AI platform cannot see bookings (11 Nov Sync); Alicia plans to meet Shawal about raising spend toward $100/day. Leads $1.55 on 86.",
 "The Outpost":"Only the 10/08 BoF is live: 3.2x on 1 purchase ($134), under the gate. Shawal paused the old 08/29 BoF on 12 Nov, which closes decision 30. Direct revenue month to date −49% on October. Pixel: Purchase capture 49% of 37 online bookings.",
 "North Star Lodge & Resort":"BoF under the gate at 10.0x on 2 purchases ($70). The 10/02 lead campaign still has 1 lead on $49 in 30 days while 10/26 has 56 at $1.81, so pausing the older one is still open (Charlotte). Direct revenue month to date −30% on October. Pixel: Purchase capture 36% of 76 online bookings; the Cloudbeds browser Purchase is still mostly missing.",
 "Glasscombe":"BoF under the gate at 44.0x on 3 purchases ($70); leads $0.30 on 481. Direct revenue month to date $7.1k, +209% on October.",
 "Cabin Collective":"BoF under the gate at 19.5x on 2 purchases ($147). The HG AI CAPI sent its first Purchases this morning (16 Nov). Direct revenue month to date −38% on October. Master sheet still reads Not Live.",
 "Walden Retreats":"HiddenGem's BoF was paused on 14 Nov (Ananya) at the client's request over an issue with the VIP promo code, while it read 34.8x on 9 purchases ($120, under the gate); the account runs only the giveaway and the lead campaign at $20/day until it restarts. The pixel recorded 85 Purchase in 7 days with no PMS to check against (pixel check).",
 "American River Resort":"Ads off since 15 Oct: paused, not offboarded. Nothing scored.",
 "Dunya Camp":"First week in the review (mapped 16 Nov; $818 spent in the last 7 days). HiddenGem's three-campaign build (Charlotte: giveaway 30 Oct, lead and BoF 13 Nov) was switched on only this morning (Chiara), so none of it has spend in the window. The spend so far is the older funnel: 'Fall step 2' and 'Retargeting - Sales - Step 3' optimise on custom events and are deferred (12 Nov), and the client's own 'fall winter purchase 2026' (Sangeetha Ramkumar, 7 Oct) reads 13.9x. The Blended 30d line counts the deferred campaigns. No PMS connection, and no live pixel visible to HiddenGem (pixel check).",
 "Arca Boutique Hotel":"Mapped 16 Nov. The first campaign, a $10/day giveaway, was created this morning (Ananya); nothing spent yet. Cloudbeds is connected: direct revenue month to date $71.2k from 21 bookings.",
}
def hgai_line(client):
    n=norm(client); hits=[b for b in HGAI if norm(b).find(n[:8])>=0 or n.find(norm(b.split(" - ")[0][11:]))>=0]
    if client in HGAI_LINES: return HGAI_LINES[client]+(f" (file: {hits[0]})" if hits else "")
    if hits: return f"HG AI notes: report on file ({', '.join(hits)}), not summarised."
    return "HG AI notes: no HG AI reports this week (none filed since 23 Sep)."

# ---------- Discovery bucket (Meta Ads Strategy 2026-10-28; built 2026-10-30) ----------
# Dustin and Shawal agreed the internal view is three buckets: Discovery (giveaway + lead campaigns, judged on the
# revenue from sign-up promo codes), Prospecting (lookalike sales campaigns, pixel ROAS) and Retargeting (pixel ROAS).
# One Discovery row per client: 30-day spend of every HiddenGem ToF + Lead Gen campaign that spent in the window
# (paused ones included, because the promo bookings in the window came from them too) against the 30-day revenue of
# direct bookings that carry a sign-up code (pms_mtd.sql, promo30_* columns). Scored on the Sales ROAS bands until the
# Benchmarks doc gets a Discovery band. Codes that are not sign-up codes (VIP, WELCOMEBACK, RETURNING, EARLY BIRD,
# agent or influencer codes) are listed but not counted. Hostaway stores only a coupon id, so there every coupon booking
# counts, with that caveat in the row.
DISC_CODE=re.compile(r"^(WELCOME\d*|ENJOY\d*|SIGNUP\d*|SIGN-UP\d*|GIVEAWAY\d*)$")
DISC_GATE=200  # 30-day spend gate, same dollar gate as Sales
client_tot=collections.defaultdict(lambda: {"spend":0.0,"pixel":0.0,"promo":0.0})
def _codes(m):
    out=[]
    for c in (m.get("promo30_codes") or "").split(";"):
        if not c: continue
        code,n,rev=c.rsplit("|",2); out.append((code,int(n),float(rev)))
    return out
def discovery_record(client,am,acct,spend,names):
    if not names: return None
    m=mtd_for(client)
    base=dict(client=client,am=am,acct=acct,cid=f"discovery::{acct}",name=f"Discovery bucket ({len(names)} campaign{'s' if len(names)!=1 else ''}: giveaway + leads)",type=DISC,win=30,src="live",spend=spend,status="ACTIVE",freq=None,promo_rev=0.0)
    if not m or m.get("promo_source")=="unavailable":
        why=("no PMS connection on the HiddenGem AI platform" if not m else f"{m['provider']} does not store promo codes on the booking")
        return dict(base,results="—",gov="promo ROAS —",govval=None,state=NS_DISC,diag="—",notes=f"{money(spend,0)} in 30 days across {', '.join(names)}; {why}, so sign-up revenue cannot be measured. Context only: Discovery is not scored (Shawal, 4 Nov 2026)")
    codes=_codes(m)
    if m["promo_source"]=="codes":
        disc=[c for c in codes if DISC_CODE.match(c[0])]; other=[c for c in codes if not DISC_CODE.match(c[0])]
        bk=sum(n for _,n,_ in disc); rev=sum(r for _,_,r in disc)
        diag=(", ".join(f"{c} ×{n} {money(r,0)}" for c,n,r in disc) or "no sign-up code bookings in 30 days")
        if other: diag+="; not counted (not sign-up codes): "+", ".join(f"{c} ×{n} {money(r,0)}" for c,n,r in other)
    else:
        bk=int(m.get("promo30_bk") or 0); rev=float(m.get("promo30_rev") or 0)
        diag=f"{bk} coupon bookings; Hostaway stores no code names, so every coupon booking is counted (may include past-guest codes)"
    roas=rev/spend if spend else None
    notes=[f"{money(spend,0)} in 30 days across {', '.join(names)}, against direct bookings booked {_d(m['d30_start'])}–{_d(m['run_date'])} with a sign-up code"]
    state=NS_DISC  # 2026-11-04: context only, no state; the promo ROAS stays in the row for reading
    if bk==0: notes.append("no sign-up promo bookings in 30 days")
    notes.append("context only: Discovery is not scored (Shawal, 4 Nov 2026; Hostaway drops code names, so this read understates Tàberg, AwayFrames, Selah, Green Springs and FLOHOM)")
    return dict(base,results=f"{bk} promo bookings, {money(rev,0)}",gov=f"promo ROAS {x(roas)}",govval=roas,state=state,diag=diag,notes="; ".join(notes),promo_rev=rev)
def blended_line(client):
    t=client_tot.get(client)
    if not t or t["spend"]<=0: return "Blended 30d: no HiddenGem campaign spend in the window."
    total=t["pixel"]+t["promo"]; roas=total/t["spend"]
    return (f"Blended 30d (every HiddenGem campaign): spend {money(t['spend'],0)}; pixel purchase value {money(t['pixel'],0)} + sign-up promo revenue {money(t['promo'],0)} = {money(total,0)}, "
            f"ROAS {x(roas)}. Not de-duplicated: a booking can carry both a pixel purchase and a promo code; the HG AI attribution matching (Leshan, from 28 Oct) is what removes that overlap.")

# ---------- score ----------
records=[]; unclassified=[]; paused_by_client=collections.defaultdict(list)
for client,(am,acct,acctname,src) in ADV.items():
    tof_spend=0.0; disc_spend=0.0; disc_names=[]
    if src=="live":
        for cid,wins in live[client].items():
            r30=wins.get(30); r14=wins.get(14)
            base=r30 or r14
            t=ctype(base["obj"],base["name"])
            cr=CREATORS.get(str(cid))
            r30s=(r30 or {}).get("spend") or 0
            if not (cr and not is_hg(cr.get("name"))):
                tot=client_tot[client]; tot["spend"]+=r30s
                if t in SALES and r30 and r30.get("roas") is not None: tot["pixel"]+=r30s*r30["roas"]
                if t in ("ToF",LEAD) and r30s>0: disc_spend+=r30s; disc_names.append(base["name"]+("" if base["status"]=="ACTIVE" else " (paused)"))
            if str(cid) in DEFERRED and t!="ToF":
                rr=r14 or r30
                deferred[client].append(dict(name=base["name"],type=t,why=DEFERRED[str(cid)],spend=rr["spend"] or 0,win=14 if r14 else 30,
                    results=f"{int(rr['purch'] or 0)} purchases",gov=f"ROAS {x(rr['roas'])}"))
                continue
            if cr and not is_hg(cr.get("name")) and t!="ToF":
                if t=="UNCLASSIFIED": t="Other"
                rr=r30 if t==LEAD else (r14 or r30)
                client_run[client].append(dict(name=base["name"],type=t,status=base["status"],creator=cr["name"],created=cr["created"],win=30 if t==LEAD else 14,spend=rr["spend"] or 0,
                    results=f"{int(rr['leads'] or 0)} leads" if t==LEAD else f"{int(rr['purch'] or 0)} purchases",
                    gov=f"CPL {money(rr['cpl'])}" if t==LEAD else f"ROAS {x(rr['roas'])}"))
                continue
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
                gov=f"CPL {money(r['cpl'])} (diagnostic)"; govval=r["cpl"]; results=f"{int(r['leads'] or 0)} leads"
                state,why=lead_state(r["cpl"],r["leads"],r["spend"])
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
        drec=discovery_record(client,am,acct,disc_spend,disc_names)
        if drec:
            records.append(drec); client_tot[client]["promo"]=drec.get("promo_rev") or 0.0
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
                gov=f"CPL {money(cpl)} (diagnostic)"; govval=cpl; results=f"{int(leads)} leads"; state,why=lead_state(cpl,leads,spend); cpp=None
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
scored=[r for r in records if r["state"] not in UNSCORED]
counts=collections.Counter(r["state"] for r in records)
def srow(r,first=True):
    return f"| {r['client']} | {r['am']} | {r['name']} | {r['type']} | {money(r['spend'],0)} / {r['win']}d | {r['gov']} | {r['state']} | {r['difftxt']} |"
L=[]
L.append(f"# Client Benchmark Review (advanced setups) — {TODAY}\n")
L.append(f"Run: 16 November 2026 (Monday), ninth run, compared against {PREVFILE}. Live reads through the Meta Marketing API with the HG - ROI Dashboard system user, the standing data path (`scripts/pull-campaign-insights.mts`, 08:44 to 08:50 PT); every account read live and the CSV export {rs} to {re_} was not needed for scoring. Scope: clients marked **Advanced** in the CRM \"Meta Ads\" column (Clients - Onboarding tab), re-read today: {len(ADV)+len(ADV_UNMAPPED)} clients, {len(ADV)} with an ad account. Bison Ridge Retreat reads Basic since 12 Nov and drops out; Gooseberry Lodges, Dunya Camp and Arca Boutique Hotel were mapped today (Shawal), so their rows are new; Sunapee Stays reads Advanced again. {len(ADV_UNMAPPED)} Advanced clients in the CRM have no ad account shared with HiddenGem yet (The Preserve and Kimpton Mas Olas Resort among them). Scoring as since 4 Nov: Sales-objective campaigns only (Retargeting, Prospecting, Sales, on 14-day pixel ROAS); Lead Gen rows and the Discovery bucket row stay in each client's table for context with no state. Changes made in the accounts since last Monday come from each account's Meta activity log (most of the 12 and 13 Nov changes were Shawal's, under his second profile John Martin), and ROAS is read against this week's pixel check where duplicate Purchases inflate it or missing Purchases deflate it.\n")
L.append("| Advanced clients | Live reads | From CSV | Rows scored | Under spend gate | Flag to Shawal | Review w/ HG AI | Monitor | Healthy | Scale w/ HG AI | Frequency over 5 | Not scored (lead gen) | Not scored (discovery) |")
L.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
L.append(f"| {len(ADV)} (+{len(ADV_UNMAPPED)} unmapped) | {sum(1 for v in ADV.values() if v[3]=='live')} | {sum(1 for v in ADV.values() if v[3]=='csv')} | {len(scored)} | {counts['Under gate']} | {counts['Flag to Shawal']} | {counts['Review w/ HG AI']} | {counts['Monitor']} | {counts['Healthy']} | {counts['Scale w/ HG AI']} | {len(freq_watch)} | {counts[NS_LEAD]} | {counts[NS_DISC]} |\n")
L.append("States come from the Decision Making table in the Benchmarks doc and apply to Sales-objective campaigns only (Shawal, 4 Nov 2026): Retargeting, Prospecting and Sales campaigns on 14-day pixel ROAS with a $200 gate. Bands: above 15x Scale, 8–15x Healthy, 5–8x Monitor, 2–5x Review, under 2x or zero purchases Flag, inclusive on the lower bound. Lead Gen rows (leads, CPL) and the Discovery bucket row (giveaway + lead spend against 30-day sign-up promo-code revenue from the PMS) are listed under each client for context and carry no state.\n")

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
L.append("Sales-objective campaigns only (Retargeting, Prospecting, Sales; Shawal, 4 Nov 2026). Flag to Shawal before Review w/ HG AI, highest spend first.\n")
L.append("| Client | AM | Campaign | Type | Spend / window | Governing metric | State | Status vs last week |")
L.append("|---|---|---|---|---|---|---|---|")
act=[r for r in records if r["state"] in ("Flag to Shawal","Review w/ HG AI")]
def act_key(r): return (0 if r["type"] in SALES else (1 if r["type"]==DISC else 2), ORDER[r["state"]], -r["spend"])  # 2026-09-23: sales/retargeting on top; 2026-10-30: Discovery buckets next, lead tracking checks last
for r in sorted(act,key=act_key): L.append(srow(r))
if removed:
    L.append("")
    L.append(f"Removed since last week (flagged on {_d(PREV_DATE)}, not scored today): "+"; ".join(f"{p['client']}: {p['campaign']} ({p['state']})" for p in removed)+".")
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
    L.append(f"ToF (Discovery / Keyword) spend, context only (inside the Discovery bucket row): {money(tof,0)} over {'30 days' if src=='live' else f'{csv_days} days (export)'}.\n")
    L.append(blended_line(c)+"\n")
    L.append(month_line(c)+"\n")
    rs_=by_client.get(c,[])
    if not rs_:
        L.append("No live Lead Gen, Sales or Discovery campaigns with spend in the window.\n")
    else:
        L.append("| Campaign | Type | Window | Spend | Results | Governing metric | Frequency | State | Diagnostics vs investigate lines | Notes | Change vs last week |")
        L.append("|---|---|---|---|---|---|---|---|---|---|---|")
        for r in sorted(rs_,key=lambda r:(ORDER[r["state"]],-r["spend"])):
            L.append(f"| {r['name']} | {r['type']} | {r['win']}d | {money(r['spend'],0)} | {r['results']} | {r['gov']} | {freq_cell(r)} | {r['state']} | {r['diag']} | {r['notes']} | {r['difftxt']} |")
        L.append("")
    for pz in paused_by_client.get(c,[]):
        L.append(f"Paused in window, not scored: {pz['name']} ({pz['type']}), {money(pz['spend'],0)} / {pz['win']}d, {pz['results']}, {pz['gov']}. Live campaigns only are scored (decision 2026-09-23).\n")
    for dz in deferred.get(c,[]):
        L.append(f"Deferred, not scored: {dz['name']} ({dz['type']}), {money(dz['spend'],0)} / {dz['win']}d, {dz['results']}, {dz['gov']}. It {dz['why']}.\n")
    for cz in client_run.get(c,[]):
        L.append(f"Client-run, not scored: {cz['name']} ({cz['type']}, {cz['status'].lower()}), created by {cz['creator']} on {cz['created']}, {money(cz['spend'],0)} / {cz['win']}d, {cz['results']}, {cz['gov']}. Campaigns created by someone outside HiddenGem are listed for visibility only (Shawal, 2026-10-19).\n")
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
L.append("- Prospecting (MoF lookalike) sales campaigns are scored on the Retargeting ROAS bands because they optimise for purchases. The Benchmarks doc has no separate band for prospecting; Dustin floated a 3x floor on 28 Oct, not yet adopted.")
L.append("- Scope (Shawal, 2026-11-04): only Sales-objective campaigns carry a state. Lead Gen rows and the Discovery bucket row are context only; they never enter Action needed, Scale candidates or the counts. Rows that were Flag or Review last week on CPL or promo ROAS read \"No longer scored\" in the diff.")
L.append("- Discovery bucket (from 2026-10-30, Meta Ads Strategy 2026-10-28; context only since 2026-11-04): one row per client combining the 30-day spend of every HiddenGem ToF (giveaway, keyword) and Lead Gen campaign that spent in the window, paused ones included, against the 30-day revenue of direct bookings carrying a sign-up promo code (WELCOME*, ENJOY*, SIGNUP*, GIVEAWAY*) from the HiddenGem AI platform (pms_mtd.sql). Other codes (VIP, WELCOMEBACK, RETURNING, EARLY BIRD, agent or influencer codes) are listed in the row but not counted. Hostaway stores only a coupon id, so every coupon booking counts there. The promo ROAS is printed for reading only. Clients on a PMS that stores no promo code (Hospitable, Cloudbeds, OwnerRez, Newbook, Lodgify, Uplisting) show no promo data.")
L.append("- Lead Gen CPL is not a state (28 Oct) and, since 4 Nov, neither is the zero-leads tracking check. CPL stays in the Governing metric column as a diagnostic and the Lead Gen investigate lines still apply.")
L.append("- Blended 30d line per client: 30-day spend of every HiddenGem campaign against pixel purchase value (Sales rows, spend × ROAS) plus sign-up promo revenue. Not de-duplicated; it is the blended view Dustin asked to keep alongside the buckets, so a budget shift between buckets that lowers the blend is visible.")
L.append("- Data path: Marketing API v21.0 insights at campaign level through `scripts/pull-campaign-insights.mts` (purchases = omni_purchase, leads = lead, ROAS = purchase_roas, link clicks = inline_link_clicks), the same fields the claude.ai connector exposed. The connector is no longer used for this report (Shawal, 2026-10-19).")
L.append("- CTR on live rows is Meta's CTR (all clicks), not link CTR. The doc's click-rate lines are probably link CTR, so treat the CTR diagnostic as indicative.")
L.append("- Frequency and cost per booking are diagnostics only and do not change the state (decision 2026-09-21). From 2026-10-06 (Shawal) every Sales / Retargeting row shows its frequency, and any value above 5.0 is marked ⚠️ in that column and listed in the Frequency watch section; CSV rows use impressions / reach summed over ad sets, which overstates frequency where ad sets overlap.")
L.append("- Only campaigns live (ACTIVE) at run time are scored. Paused campaigns that spent inside the window are listed per client as \"Paused in window\" and never enter Action needed or the counts (decision 2026-09-23).")
L.append("- Client-run campaigns (created by a non-HiddenGem login per the account activity log, listed under the client, never scored): "+("; ".join(f"{c}: {', '.join(z['name']+' ('+z['creator']+')' for z in zs)}" for c,zs in client_run.items()) if client_run else "none")+". Creators are known for campaigns created in the last 180 days; older campaigns are scored as usual.")
L.append(f"- Unclassified campaigns: {', '.join(f'{c}: {n}' for c,n in unclassified) if unclassified else 'none'}.")
L.append(f"- Previous report: {PREVFILE}. Diff joined on campaign_id for live rows and client + campaign name for CSV rows. Diff counts: {sum(1 for r in records if r['diff']=='new')} new, {sum(1 for r in records if r['diff']=='still_open')} still open, {sum(1 for r in records if r['diff']=='fixed')} fixed, {sum(1 for r in records if r['diff']=='unchanged')} unchanged, {len(removed)} removed.")
L.append("- Scope changes vs 9 Nov (Shawal, 16 Nov): Gooseberry Lodges, Dunya Camp and Arca Boutique Hotel mapped and added; Sunapee Stays reads Advanced in the CRM again, so its override is gone"+("; ".join(f"{c} kept in scope ({why})" for c,why in ADV_OVERRIDE.items()))+("; "+"; ".join(f"{c} dropped ({why})" for c,why in ADV_DROPPED.items()) if ADV_DROPPED else "")+". Advanced in the CRM but with no ad account mapping in PROJECT.md section 5, not scored: "+", ".join(f"{c} (AM {am})" for c,am in ADV_UNMAPPED.items())+". Gooseberry Lodges (no ads running yet, Shawal 9 Nov) and Nine Pines Retreats are on the Master Meta Ads sheet without an account ID.")
L.append("- HG AI reports read from `HG AI Reports/` at the project root, dated since the previous run: "+(", ".join(HGAI) if HGAI else "none")+".")
L.append("- Selah Place's campaigns are named with pipes in Meta (\"SP | Willow | Sales | Top-5 Audiences | 11-2026\"); shown here with slashes.")
L.append("- Meeting notes: every \"Meta Ads Strategy\", \"Meta Ads Sync\" or \"Meta Ads x HiddenGem AI Sync\" calendar event since the previous run that has a \"Notes by Gemini\" attachment, read via Drive. Client names are matched with an alias list (Flow Home = FLOHOM, Tabber / Tipik Falls / Debug Falls = Tàberg Falls, Sailor Place = Selah Place, Stay on 38 = Stay On 30A, Ashwood River Cabins = Asheville River Cabins).")
L.append("- This month line: direct booking revenue by booking date from the HiddenGem AI platform (pms_bookings, platform direct/OTA rules, tenants on a shared PMS account narrowed to their own properties), month to date at the run date, against the same day span of the previous month. Promo codes come from the booking payload: Guesty stores the code, Hostaway only a coupon id (counted, no names), Hospitable and Cloudbeds nothing. Pulled with pms_mtd.sql through the Supabase connector." + (" Clients without a PMS connection on the platform show no figures." if any(mtd_for(c) is None for c in ADV) else ""))
L.append(f"- Monthly ROI context from `Monthly ROI data/` ({', '.join(sorted({p for v in roi.values() for p in v}, key=lambda p:(p.split()[-1], p[:3] in ('Oct','Nov','Dec'), p[:3]=='Sep', p[:3]=='Aug')))}). Revenue there comes from the Client Performance Tracking sheet, not the pixel, so its ROAS is not comparable to the pixel ROAS above.")
OUT_W=os.environ.get("BENCH_OUT",OUT)  # set BENCH_OUT to render a preview somewhere other than the archive
open(f"{OUT_W}/{TODAY}-client-benchmark.md","w",encoding="utf-8").write("\n".join(L)+"\n")
with open(f"{OUT_W}/{TODAY}-client-benchmark.csv","w",newline="",encoding="utf-8") as fh:
    w=csv.writer(fh); w.writerow("run_date,client,am,ad_account_id,campaign_id,campaign,type,window_days,source,spend,results,governing_metric,governing_value,state,diagnostics,diff_status,weeks_open,notes,frequency,freq_flag,mtd_direct_revenue,mtd_direct_bookings,mtd_vs_prev_month_pct,mtd_promo_uses,mtd_promo_codes".split(","))
    for r in records:
        gm="cpl_diagnostic" if r["type"]==LEAD else ("promo_roas" if r["type"]==DISC else "roas")
        w.writerow([TODAY,r["client"],r["am"],r["acct"],r["cid"],r["name"],r["type"],r["win"],r["src"],f"{r['spend']:.2f}",r["results"],gm,"" if r["govval"] is None else f"{r['govval']:.2f}",r["state"],r["diag"],r["diff"],r["weeks"],r["notes"],"" if r.get("freq") is None else f"{r['freq']:.2f}","yes" if r["freq_flag"] else ""]+mtd_csv(r["client"]))
print("records",len(records),"counts",dict(counts)); print("unclassified",unclassified)
