import csv, json, glob, os, re, collections, datetime
ROOT=os.path.join(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","..","..")),"weekly")  # <repo>/weekly
SP=os.path.dirname(os.path.abspath(__file__))
TODAY="2026-11-02"
PREV_DATE="2026-10-26"
OUT=f"{ROOT}/Client Benchmark Reviews (advanced setups)/Weekly Checks"
ADV={ # CRM "Clients - Onboarding" tab, Meta Ads = Advanced, read 2026-11-02 (unchanged from 2026-10-26): name -> (AM, account id, account name, connector)
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
 "Glasscombe":("Charlotte","2030318804465316","Glasscombe","live"),
 "Cabin Collective":("Chiara","2194562394139883","Cabin Collective","live"),
 "Sunapee Stays":("Charlotte","651114096215889","Sunapee Stays Ads Account","live"),
}
# Advanced in the CRM but with no ad account in PROJECT.md section 5 (footer only)
ADV_UNMAPPED={"Treetop Hideaways":"Kristal","Casey Key Resort":"Alicia","Arca Roatan":"Anna","Gooseberry Lodges":"Alicia","Dunya Camp":"Chiara","Nine Pines Retreat":"Nicole","Lundy Farm":"Charlotte"}
# Was Advanced on 2026-09-21, now Basic in the CRM: dropped from scope this run
ADV_DROPPED={}
# Sunapee Stays reads Basic in the CRM since 19 Oct but Shawal (2026-10-26) keeps it in the advanced reporting, so it is in ADV above
ADV_OVERRIDE={"Sunapee Stays":"CRM Meta Ads column reads Basic since 19 Oct; kept as Advanced at Shawal's request (2026-10-26)"}
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
DISC="Discovery (ToF + MoF leads)"  # one bucket row per client: giveaway + lead spend scored on promo-code ROAS (Meta Ads Strategy 2026-10-28; built 2026-10-30)
def lead_state(cpl,leads,spend):
    # 2026-10-28 Meta Ads Strategy (Dustin, Shawal): cost per lead is too subjective to flag on; lead campaigns are
    # judged through the Discovery bucket's promo-code ROAS. The only direct flag left is the tracking check
    # Shawal asked to keep: spend over the gate with zero leads means the Lead event is broken, not that the ad is bad.
    if leads in (None,0): return "Flag to Shawal","0 leads on spend over the gate: tracking check, not a performance call"
    return "Tracked in Discovery","CPL is a diagnostic only; the ROAS state is on this client's Discovery row"
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
ORDER={"Flag to Shawal":0,"Review w/ HG AI":1,"Monitor":2,"Healthy":3,"Scale w/ HG AI":4,"Under gate":5,"Tracked in Discovery":6,"No promo data":7}
UNSCORED=("Under gate","Tracked in Discovery","No promo data")
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
def is_hg(name):
    n=(name or "").lower().strip()
    return any(n==h or n.split(" ")[0]==h.split(" ")[0] for h in HG_TEAM)
CREATORS={}
if os.path.exists(f"{SP}/creators.json"):
    CREATORS=json.load(open(f"{SP}/creators.json",encoding="utf-8"))
client_run=collections.defaultdict(list)

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
 dict(title="Meta Ads Strategy", date="2026-10-28", doc_id="1PZCCkySabRZwn7_CUglqupOKUp6FUglJexarX709VKA", file=f"{SP}/meeting1.json"),
]
# How Gemini spells clients in the notes. Lower-case substrings.
ALIASES={
 "FLOHOM":["flohom","flow home","flo home"],
 "Tàberg Falls":["taberg","tabber","taber falls","tàberg","táberg","tipik falls","debug falls","tab fel","tab fell"],
 "Stay On 30A":["30a","stay on 38"],
 "Starlight Haven Hot Springs":["starlight","hot springs","starlight haven"],
 "Starlight Haven Weiss Lake":["starlight","weiss"],
 "Stay Saluda NC":["saluda"],
 "American River Resort":["american river"],
 "Asheville River Cabins":["asheville","ashwood river"],
 "Green Springs Inn":["green springs"],
 "Treetop Escapes":["treetop","tree top","tree tops"],
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
    if p is None: return ("new",1 if rec["state"] in FLAGGED else 0,f"New, not in the {_d(PREV_DATE)} run")
    ps=p["state"]; pw=int(p.get("weeks_open") or 0)
    if rec["state"]=="Tracked in Discovery": return ("retired" if ps in FLAGGED else "unchanged",0,(f"CPL state retired (28 Oct decision), was {ps}; see the Discovery row" if ps in FLAGGED else "Unchanged" if ps==rec["state"] else f"Was {ps}, CPL no longer scored"))
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
 "Stay On 30A":"BoF slips from Scale to Healthy at 13.3x on 9 purchases ($2,132 in 14 days; CPC $1.95, cost per booking $237, frequency 3.8), while the HiddenGem Pixel lookalike holds Scale at 17.3x on 5 purchases ($2,860). Discovery row enters at Healthy, 12.3x: the ToF giveaway plus the leads campaign cost $4,508 in 30 days and WELCOME100 bookings brought $55.2k; the EARLY BIRD DIRECT (×27, $142k), VIP100 (×16, $41.9k) and WELCOMEBACK15 codes are shown but not counted as sign-up codes. Leads $1.49 on 1,005 leads, CPL now a diagnostic. 28 Oct Strategy: the platform's campaign attribution (Hinge) is being built on this account first and Shawal is to audit its September attribution for discrepancies. Pixel check: 70 Purchase in 28 days, all server-side from Guesty, against 65 online bookings.",
 "Tàberg Falls":"Two new Action rows. The lookalike prospecting campaign drops from Monitor (8.0x) to Review at 2.1x on a single purchase ($827 in 14 days) the week its budget doubled from $50 to $100/day; 30 days read 4.0x on 4 purchases, so the audience has cooled rather than broken. The Discovery row flags at 0.4x: $3,381 of giveaway and lead spend in 30 days against one coupon booking ($1,240) in Hostaway, while the leads campaign delivered 2,689 leads at $0.57. Either the sign-up codes are not being redeemed or Hostaway is not recording the coupon on those bookings; Alicia to check a few recent WELCOME bookings in Hostaway before the row is read as a performance problem. BoF 12.0x Healthy on 6 purchases ($886, also doubled to $100/day). The paused Broad prospecting test spent $13 in the window. 28 Oct Strategy: Tàberg is on the list for the platform's promo-code attribution rollout.",
 "Endless Stays":"BoF 4.2x on one purchase ($1,094 in 14 days, cost per booking $1,094; 3.3x on 3 purchases over 30), fifth week at Review and the largest Review spend on the list. Leads $0.90 on 1,656 leads. The Discovery row cannot be scored (Hospitable stores no promo code), so $3,755 of 30-day giveaway and lead spend has no revenue read at all; this is the biggest blind spot the new buckets expose. Pixel check: 13 Purchase in 28 days, all from the HG AI CAPI, against 13 online bookings, so the pixel is complete but the bookings themselves are few.",
 "Paradise Pointe":"Strongest account this week. BoF 25.0x Scale on 15 purchases ($702; 15.1x last week), but frequency 5.85 keeps it the only Frequency-watch row, and the pixel check shows browser Purchases at 148% of online bookings (a confirmation page that fires on reload), so the pixel ROAS is overstated; the Discovery row says the same thing from the PMS side at 49.6x: $1,503 of giveaway and lead spend against 66 WELCOME100 and WELCOME10 bookings worth $74.6k in 30 days. Lookalike 12.7x Healthy on 10 purchases (up from Monitor). Leads $1.02 on 735 leads. This month +57% on October's same two days.",
 "FLOHOM":"Lookalike up from Healthy to Scale at 19.8x on 15 purchases ($693 in 14 days); Myrtle Beach lookalike 8.2x Healthy on 1 purchase ($275); BoF 5.3x Monitor on 6 purchases, unchanged. Discovery row enters at Scale, 27.9x: $726 of giveaway and lead spend against 22 coupon bookings ($20.3k) in Hostaway, which stores no code names, so every coupon booking counts (caveat). Leads $0.56 on 760 leads. Pixel check: booking-engine traffic on book.flohom.com fell 90% from 31 Oct while Purchases kept arriving server-side from Hostaway's CAPI (100 in 28 days against 103 online bookings); Makenna to check the booking page pixel. 28 Oct Strategy: FLOHOM is on the promo-code attribution rollout list.",
 "Treetop Escapes":"BoF up from Healthy to Scale at 19.7x on 9 purchases ($560 in 14 days), frequency 3.3. Discovery row Healthy at 12.0x: $1,807 of giveaway and lead spend against WELCOME100 ×17 and WELCOME10 ×2 bookings worth $21.6k. Leads $0.79 on 1,146 leads. 28 Oct Strategy: on the promo-code attribution rollout list.",
 "Ponderosa Pines Resort":"BoF 10.5x Healthy on 16 purchases ($563; 9.4x last week), frequency 2.5. Leads $1.06 on 564 leads. Discovery row has no promo data (Newbook stores no code) on $1,802 of 30-day spend. Pixel check caveat: browser Purchases are 1.66x the PMS bookings (313 Purchase against 125 bookings in 28 days), so the pixel ROAS here is inflated by the Newbook confirmation firing more than once per booking; Anna to fix the confirmation event. This month +47%.",
 "Starlight Haven Hot Springs":"Both campaigns in good shape: BoF 24.2x Scale on 9 purchases ($280), leads $0.32 on 2,848 leads. No promo data (ResNexus) for the Discovery row on $1,657 of spend.",
 "Starlight Haven Weiss Lake":"BoF 19.5x Scale on 24 purchases ($626). Leads $1.11 on 676 leads (CPL state retired). No promo data (ResNexus) on $749.",
 "AwayFrames":"Budget went from $30 to $200/day on 29 Oct (spend check), so the account is in its first week at scale. The new MoF lookalike (10/29) has $203 in 14 days and no purchase yet, which the rules read as Flag; it is four days old, so treat it as a tracking check to re-read next week rather than a verdict. BoF crosses the gate for the first time at 19.9x on 7 purchases ($376) and enters Scale (frequency 4.3). Discovery row Review at 2.8x: $1,445 of giveaway and lead spend against 3 coupon bookings ($4,059) in Hostaway. Leads $1.58 on 350 leads. Pixel check: 24 Purchase in 28 days, all server-side, against 20 online bookings; the HG AI CAPI toggle is OFF while its ledger still shows sends to 28 Oct, so Hostaway's CAPI is now the sender.",
 "Stay Saluda NC":"BoF Fixed: from Flag (1.7x) to Healthy at 8.1x on 6 purchases ($425 in 14 days; 7.1x on 11 purchases over 30), although frequency 4.3 is still high. Discovery row Healthy at 8.9x: $1,499 of giveaway and lead spend against ENJOY10 ×12 and WELCOME10 ×6 bookings worth $13.3k. Leads $0.94 on 632 leads. This month +89% on October's same two days. 28 Oct Strategy: on the promo-code attribution rollout list. Pixel: the Saluda GHL hosts still fire the Inspired Retreats pixel (week 7).",
 "Little River Landing":"Discovery row flags at 0.2x: $1,874 of giveaway and lead spend in 30 days ($65/day on the giveaway) against one WELCOME10 booking ($393). Leads $1.57 on 95 leads on $5/day. BoF under the gate, 2.2x on 1 purchase ($179). The pixel check is ❌ here too (3 Purchase in 28 days against 11 online bookings, HG AI CAPI OFF), so the $15/day BoF is optimising on a quarter of the real bookings. Next action (Makenna / Leshan): turn the HG AI CAPI on for the tenant and check sign-up code redemption in Guesty.",
 "Asheville River Cabins":"BoF slips from Healthy to Monitor at 7.9x on 7 purchases ($417 in 14 days; 20.6x on 30 days), CPM $20. Leads $0.33 on 889 leads. No promo data for the Discovery row ($1,455 of spend): the 28 Oct notes say Leshan has integrated Cloudbeds to show promo-code data, but the platform's Cloudbeds bookings still carry no code field in the query this report uses, so Leshan to confirm where the Cloudbeds coupon lands (also applies to Glasscombe and North Star). 28 Oct Strategy: Asheville named as one of the advanced clients to get a formal budget range and ROAS goal (five times was the example). Pixel: still browser-only, 0 server events, the one CAPI-silent row left.",
 "Ridge & Falls":"Discovery row flags at 0.0x: $1,656 of giveaway and lead spend in 30 days and no booking with a sign-up code; the one coded booking was HELLO10 ($463), which is not in the sign-up list (WELCOME, ENJOY, SIGNUP, GIVEAWAY). Shawal to say whether HELLO10 is Ridge & Falls' sign-up code; if so the row reads 0.3x, still a Flag. Leads $2.22 on 67 leads ($149 on $5/day; CPL state retired). BoF 19.2x on 6 purchases but under the gate ($174). Pixel check: 19 server Purchase against 11 online bookings, the HG AI CAPI plus a second sender; one should be switched off.",
 "Selah Place":"HiddenGem's BoF drops from Monitor (7.5x) to Review at 3.9x on 6 purchases ($420 in 14 days), frequency 4.5. Discovery row Healthy at 10.3x: $1,003 of giveaway and lead spend against 19 coupon bookings ($10.3k) in Hostaway. Leads $0.61 on 410 leads. The client (Nathan Jay Herrington) now runs four campaigns of their own, listed below and not scored: the new 'SP / Willow / Sales / Top-5 Audiences / 11-2026' at $135/day since 28 Oct reads 1.2x on 7 purchases ($705), the VIP List lead campaign $1.77 on 376 leads, the paused Pre-Sales test 0.2x. Account spend is $245/day, of which HiddenGem's three campaigns are $70. Pixel check: the HG AI CAPI and Hostaway's CAPI both send a server Purchase per booking (80 server Purchase against 44 bookings), so pixel ROAS across the account is roughly doubled; one sender should be switched off.",
 "Sunapee Stays":"Leads $2.04 on 147 leads ($299; CPL state retired, was Review). BoF 4.2x on 1 purchase, under the gate ($140). No promo data (OwnerRez) on $1,205 of Discovery spend. Pixel: reclassified this week, the HG AI CAPI sends every booking (42 of 42).",
 "Green Springs Inn":"Discovery row Healthy at 15.0x: $904 of giveaway and lead spend against 29 coupon bookings ($13.5k) in Hostaway. Leads $1.45 on 206 leads (CPL state retired, was Review week 6). BoF 5.9x on 2 purchases, under the gate ($141).",
 "The Outpost":"Only the 10/08 BoF campaign spent in the window ($148, 2 purchases, 4.1x), under the gate; the 08/29 one carries a $10 budget but did not spend. No promo data (Newbook) on $899 of Discovery spend. Pixel check: Purchase capture 35% (17 server Purchase against 49 online bookings), browser never fires Purchase.",
 "Bison Ridge Retreat":"Leads $2.13 on 70 leads ($149; CPL state retired, was Review). BoF 0 purchases on $71, under the gate. No promo data on $749 of Discovery spend (no PMS in the platform). Pixel: the server side went silent this week; sheet says browser only.",
 "Walden Retreats":"HiddenGem's leads campaign $1.30 on 207 leads (CPL state retired, was Review); BoF 5.7x on 1 purchase, under the gate ($141). No promo data (ResNexus) on $546. The client's own wedding campaigns are listed below and not scored: 'TOF Wedding Leads 10.8.26' $17.56 on 29 leads and the new 'MOF Wedding Leads 10.27.26' (Lindsey Cooke, $5/day) with 1 lead so far.",
 "North Star Lodge & Resort":"Last week's tracking Flag clears on a technicality: the 10/02 lead campaign now has 1 lead on $107 ($106.66 CPL), so the zero-lead check no longer fires, and a second lead campaign (10/26, $34, 9 leads at $3.79) has started. BoF under the gate ($70, 1 purchase). No promo data (Cloudbeds; see the Asheville note on where Cloudbeds coupons land). Pixel check this week: the Cloudbeds booking engine fired the account pixel once all week and the HG BM pixel is dead since 26 Oct, Purchase capture 37% of 94 online bookings and the HG AI send looks stalled since 3 Oct, so the BoF has little to optimise on until the engine pixel is reinstalled (Charlotte / Leshan).",
 "American River Resort":"Ads off since 15 Oct: paused, not offboarded. The lead campaign's trailing spend ($271, 204 leads at $1.33) is listed as paused and nothing is scored; the Discovery row shows $679 of trailing 30-day spend with no promo data (Arctic PMS, not in the platform).",
 "Glasscombe":"Both under the gate: leads $0.30 on 315 leads ($93), BoF 0 purchases on $69. No promo data (Cloudbeds) on $483. The platform's month-to-date reads $0 after two days of November.",
 "Cabin Collective":"Leads cross the $100 gate at $1.25 on 89 leads ($111), now Tracked in Discovery; BoF 82x on 6 purchases but under the gate ($109). No promo data (OwnerRez) on $223. Master sheet Status still Not Live although the account has spent since 20 Oct.",
}
def hgai_line(client):
    n=norm(client); hits=[b for b in HGAI if norm(b).find(n[:8])>=0 or n.find(norm(b.split(" - ")[0][11:]))>=0]
    if client in HGAI_LINES: return HGAI_LINES[client]+(f" (file: {hits[0]})" if hits else "")
    if hits: return f"HG AI notes: report on file ({', '.join(hits)}), not summarised."
    return "HG AI notes: no HG AI reports this week (none filed since 26 Oct)."

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
        return dict(base,results="—",gov="promo ROAS —",govval=None,state="No promo data",diag="—",notes=f"{money(spend,0)} in 30 days across {', '.join(names)}; {why}, so sign-up revenue cannot be measured and the bucket is not scored")
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
    if spend<DISC_GATE: state="Under gate"; notes.append(f"spend {money(spend)} < ${DISC_GATE} gate")
    elif bk==0: state="Flag to Shawal"; notes.append("no sign-up promo bookings in 30 days")
    else:
        state,_=roas_state(roas,bk)
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
L.append(f"Run: 2 November 2026 (Monday), seventh run, compared against {PREVFILE}. Live reads through the Meta Marketing API with the HiddenGem-Claude system user, the standing data path (`scripts/pull-campaign-insights.mts`, 07:36 to 07:38 PT); every account is live and the CSV export {rs} to {re_} was not needed for scoring. Scope: clients marked **Advanced** in the CRM \"Meta Ads\" column (Clients - Onboarding tab), re-read today: {len(ADV)+len(ADV_UNMAPPED)} clients, {len(ADV)} with an ad account, unchanged from 26 Oct (Sunapee Stays stays in at Shawal's request although the CRM reads Basic). Seven Advanced clients in the CRM have no ad account yet. First Monday run with the Discovery bucket rows (giveaway + lead spend scored on sign-up promo-code revenue, 28 Oct decision, built 30 Oct), so every Discovery row reads New and the Lead Gen rows that were Flag or Review on cost per lead read \"CPL state retired\". Only Lead Gen (MoF) and Sales/Retargeting (BoF) campaigns are scored; IG Discovery and Keyword (ToF) spend is shown for context and inside the Discovery row.\n")
L.append("| Advanced clients | Live reads | From CSV | Rows scored | Under spend gate | Flag to Shawal | Review w/ HG AI | Monitor | Healthy | Scale w/ HG AI | Frequency over 5 | Tracked in Discovery | No promo data |")
L.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
L.append(f"| {len(ADV)} (+{len(ADV_UNMAPPED)} unmapped) | {sum(1 for v in ADV.values() if v[3]=='live')} | {sum(1 for v in ADV.values() if v[3]=='csv')} | {len(scored)} | {counts['Under gate']} | {counts['Flag to Shawal']} | {counts['Review w/ HG AI']} | {counts['Monitor']} | {counts['Healthy']} | {counts['Scale w/ HG AI']} | {len(freq_watch)} | {counts['Tracked in Discovery']} | {counts['No promo data']} |\n")
L.append("States come from the Decision Making table in the Benchmarks doc, applied per bucket since the 28 Oct Meta Ads Strategy meeting. Every state is a ROAS state: Sales / Retargeting / Prospecting campaigns on 14-day pixel ROAS ($200 gate); the Discovery bucket (giveaway + lead campaigns of a client, one row) on 30-day sign-up promo-code ROAS from the PMS ($200 gate). Bands: above 15x Scale, 8–15x Healthy, 5–8x Monitor, 2–5x Review, under 2x Flag, inclusive on the lower bound. Lead Gen campaigns show their CPL as a diagnostic and are marked Tracked in Discovery; the only direct Lead Gen flag is the tracking check (spend over the $100 gate with zero leads). Clients whose PMS does not store promo codes get No promo data on the Discovery row.\n")

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
L.append("Sales, Retargeting and Prospecting campaigns first, then Discovery buckets, then Lead Gen tracking checks. Within each, Flag to Shawal before Review w/ HG AI, highest spend first.\n")
L.append("| Client | AM | Campaign | Type | Spend / window | Governing metric | State | Status vs last week |")
L.append("|---|---|---|---|---|---|---|---|")
act=[r for r in records if r["state"] in ("Flag to Shawal","Review w/ HG AI")]
def act_key(r): return (0 if r["type"] in SALES else (1 if r["type"]==DISC else 2), ORDER[r["state"]], -r["spend"])  # 2026-09-23: sales/retargeting on top; 2026-10-30: Discovery buckets next, lead tracking checks last
for r in sorted(act,key=act_key): L.append(srow(r))
if removed:
    L.append("")
    L.append("Removed since last week (flagged on 26 Oct, not scored today): "+"; ".join(f"{p['client']}: {p['campaign']} ({p['state']})" for p in removed)+".")
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
    L.append(f"ToF (Discovery / Keyword) spend, scored inside the Discovery bucket row: {money(tof,0)} over {'30 days' if src=='live' else f'{csv_days} days (export)'}.\n")
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
L.append("- Discovery bucket (from 2026-10-30, Meta Ads Strategy 2026-10-28): one row per client combining the 30-day spend of every HiddenGem ToF (giveaway, keyword) and Lead Gen campaign that spent in the window, paused ones included, against the 30-day revenue of direct bookings carrying a sign-up promo code (WELCOME*, ENJOY*, SIGNUP*, GIVEAWAY*) from the HiddenGem AI platform (pms_mtd.sql). Other codes (VIP, WELCOMEBACK, RETURNING, EARLY BIRD, agent or influencer codes) are listed in the row but not counted. Hostaway stores only a coupon id, so every coupon booking counts there. Scored on the Sales ROAS bands with a $200 gate until the Benchmarks doc gets a Discovery band. Clients on a PMS that stores no promo code (Hospitable, Cloudbeds, OwnerRez, Newbook, Lodgify, Uplisting) are marked No promo data and not scored.")
L.append("- Lead Gen CPL is no longer a state (28 Oct). It stays in the Governing metric column as a diagnostic, the Lead Gen investigate lines still apply, and the one direct flag left is the tracking check: spend over the $100 gate with zero leads. Rows that were Flag or Review on CPL last week read \"CPL state retired\" in the diff rather than Fixed.")
L.append("- Blended 30d line per client: 30-day spend of every HiddenGem campaign against pixel purchase value (Sales rows, spend × ROAS) plus sign-up promo revenue. Not de-duplicated; it is the blended view Dustin asked to keep alongside the buckets, so a budget shift between buckets that lowers the blend is visible.")
L.append("- Data path: Marketing API v21.0 insights at campaign level through `scripts/pull-campaign-insights.mts` (purchases = omni_purchase, leads = lead, ROAS = purchase_roas, link clicks = inline_link_clicks), the same fields the claude.ai connector exposed. The connector is no longer used for this report (Shawal, 2026-10-19).")
L.append("- CTR on live rows is Meta's CTR (all clicks), not link CTR. The doc's click-rate lines are probably link CTR, so treat the CTR diagnostic as indicative.")
L.append("- Frequency and cost per booking are diagnostics only and do not change the state (decision 2026-09-21). From 2026-10-06 (Shawal) every Sales / Retargeting row shows its frequency, and any value above 5.0 is marked ⚠️ in that column and listed in the Frequency watch section; CSV rows use impressions / reach summed over ad sets, which overstates frequency where ad sets overlap.")
L.append("- Only campaigns live (ACTIVE) at run time are scored. Paused campaigns that spent inside the window are listed per client as \"Paused in window\" and never enter Action needed or the counts (decision 2026-09-23).")
L.append("- Client-run campaigns (created by a non-HiddenGem login per the account activity log, listed under the client, never scored): "+("; ".join(f"{c}: {', '.join(z['name']+' ('+z['creator']+')' for z in zs)}" for c,zs in client_run.items()) if client_run else "none")+". Creators are known for campaigns created in the last 180 days; older campaigns are scored as usual.")
L.append(f"- Unclassified campaigns: {', '.join(f'{c}: {n}' for c,n in unclassified) if unclassified else 'none'}.")
L.append(f"- Previous report: {PREVFILE}. Diff joined on campaign_id for live rows and client + campaign name for CSV rows. Diff counts: {sum(1 for r in records if r['diff']=='new')} new, {sum(1 for r in records if r['diff']=='still_open')} still open, {sum(1 for r in records if r['diff']=='fixed')} fixed, {sum(1 for r in records if r['diff']=='unchanged')} unchanged, {len(removed)} removed.")
L.append("- Scope changes vs 26 Oct: none (same 24 accounts); "+("; ".join(f"{c} kept in scope ({why})" for c,why in ADV_OVERRIDE.items()))+("; "+"; ".join(f"{c} dropped ({why})" for c,why in ADV_DROPPED.items()) if ADV_DROPPED else "")+". Advanced in the CRM but with no ad account mapping in PROJECT.md section 5, not scored: "+", ".join(f"{c} (AM {am})" for c,am in ADV_UNMAPPED.items())+". Gooseberry Lodges also appeared on the Master Meta Ads sheet this week, still with no account ID.")
L.append("- HG AI reports read from `HG AI Reports/` at the project root, dated since the previous run: "+(", ".join(HGAI) if HGAI else "none")+".")
L.append("- Selah Place's prospecting campaign (paused this week) is named with pipes in Meta (\"SP | Prospecting Test | LAL + Interests x Creative | 09-2026\"); shown here with slashes.")
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
