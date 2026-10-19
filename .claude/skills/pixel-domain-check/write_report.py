"""Writes the dated pixel domain check .md and .csv from pixel_pull.json.

The per-pixel flags, expected domains and notes are authored by Claude in
ROWS below each week (the judgement part of the audit); events, hosts,
browser/server split and the week-over-week diff are computed here.
"""
import json, csv, os, glob, datetime, collections
SP=os.path.dirname(os.path.abspath(__file__))
ROOT=os.path.abspath(os.path.join(SP,"..","..",".."))
OUT=os.path.join(ROOT,"weekly","Meta Pixel Reviews","Weekly Checks")
TODAY="2026-10-19"
pull=json.load(open(os.path.join(SP,"pixel_pull.json"),encoding="utf-8"))
px={p["id"]:p for p in pull["pixels"]}
CLIENTS_ON_SHEET=44; NOT_LIVE=1; OFFBOARDED_EXCLUDED=["Canopy at Moody Moon Ridge"]
WINDOW="12 to 19 Oct"

M,W,C,B="match","warning","critical","blocker"
ROWS=[
 dict(client="American River Resort",pid="2862601447415133",name="American River Resort - Meta Pixel",acct="953162737054331",flag=M,exp="americanriverresort.com",src="inferred",
  notes="Clean. Both ad campaigns stopped on about 15 Oct (spend check: $0/day), the pixel still fires from the site, bio and GHL funnel; 11,549 events (−23%), browser and server half each, 129 Lead."),
 dict(client="Asheville River Cabins",pid="1634367080775220",name="Asheville River Cabins Meta Pixel",acct="615836588009747",flag=W,exp="ashevillerivercabins.com + Cloudbeds",src="inferred",
  notes="Week 5: domains clean (Cloudbeds booking engine is the largest host; 45 Purchase, 248 Lead this week). Sheet says 'CAPI Setup (HG Ai)' but the pixel is browser-only: 0 of 23,188 events server-side. New minor host wordpress-1016560-5306423.cloudwaysapps.com (12 events) is the site's WordPress staging on Cloudways, accepted as a dev host. 14 Oct Strategy: Leshan's click-ID script is live in the Cloudbeds account; sending through CAPI needs host API access, which Shawal is requesting. Next action (Charlotte / Shawal): get the Cloudbeds API access so the HG AI CAPI can send, and correct the sheet until it does."),
 dict(client="Away2PA",pid="772693422494226",name="Away 2PA Meta Pixel",acct="603977626130795",flag=M,exp="away2pa.com | awaytopa.com",src="inferred",
  notes="Clean. 26,612 events (−9%), browser and server half each, 14 Purchase, 341 Lead. OwnerRez booking engine present."),
 dict(client="Awayframes",pid="773898245792839",name="Awayframes - Meta Pixel",acct="2471256056603833",flag=M,exp="awayframes.com",src="inferred",
  notes="Domains clean, but 28% of this week's events (localhost 2,531, 127.0.0.1 348) are dev traffic firing the live pixel ID, plus two Netlify previews (awayframes.netlify.app, blobs-check--awayframes.netlify.app): an HG site build in progress. Accepted as HG dev, not flagged. 10,413 events (+52%, mostly that dev traffic), 90 Lead, 6 Purchase, 33% server. Ask Leshan to disable the pixel on localhost before the site goes live."),
 dict(client="Best Texas Travel",pid="4108409325970216",name="Best Texas - Meta Pixel",acct="1982551189319458",flag=M,exp="besttexastravel.com",src="inferred",
  notes="Clean. 20,540 events (+60%), the book. booking-engine subdomain is 92% of it; 51% server. No standard Purchase or Lead events in the week, only the booking-engine custom events."),
 dict(client="Big Moon Ranch",pid="1208874174466414",name="Big Moon Ranch - Meta Pixel",acct="758851247064974",flag=W,exp="bigmoonranch.com | staybigmoonranch.com",src="inferred",
  notes="Week 3: client offboarded 28 Sep but the HG BM pixel is still installed on bigmoonranch.com, 10,280 events this week (+23%) and 51% server-side, so the HG AI CAPI connection is still sending too. Still on the Master sheet. Next action (Charlotte): remove the pixel from the site, disconnect the CAPI connection, and take the row off the sheet (decision 25)."),
 dict(client="Bison Ridge Retreat",pid="1241959234316508",name="Bison Ridge - Meta Pixel",acct="950241787963535",flag=M,exp="bisonridgeretreat.com",src="inferred",
  notes="Clean. 6,749 events (+23%), half server, 95 Lead. Event Data pixel 1617239586052069 still attached and dead."),
 dict(client="Columbia Gorge Getaways",pid="595257656540749",name="CGG Pixel",acct="490940113157881",flag=W,exp="columbiagorgegetaways.com | columbiagorgeglamping.com",src="inferred",
  notes="Week 5: unchanged. Fires only from the Wix static host (604) and the GHL funnel go.columbiagorgeglamping.com (401), never from the main site, browser only; 16 Lead, 22 SubmitApplication. Two live pixels on one client. Next action (Chiara): put the primary pixel on the GHL funnel pages and retire this one, or record it as the funnel pixel."),
 dict(client="Columbia Gorge Getaways",pid="700947282709400",name="Columbia Gorge Getaways Pixel",acct="490940113157881",flag=M,exp="columbiagorgegetaways.com + ResNexus",src="inferred",
  notes="Clean. Main site plus ResNexus booking engine; 8,819 events (−31%), half server, 4 Purchase."),
 dict(client="Endless Stays",pid="876508505381758",name="Endless Stays Meta Pixel",acct="896372356081479",flag=M,exp="stayendless.com + Hospitable",src="inferred",
  notes="Clean. 42,848 events (+9%), half server, 934 Lead, 4 Purchase. Hospitable booking engine present (730 events)."),
 dict(client="Evergreen Cabins",pid="1474685406530880",name="Evergreen Cabins Meta Pixel",acct="453808647114273",flag=M,exp="evergreencabins.co + Hospitable",src="inferred",
  notes="Clean. 41,544 events (−7%), 29% server, 7 Purchase, 111 Lead. distinctdestinations.co (2 events last week) did not recur."),
 dict(client="FLOHOM",pid="139231105894533",name="FLO2 Conversion",acct="2100710320122219",flag=W,exp="flohom.com | goflohom.com",src="inferred",
  notes="Week 2: sheet says 'CAPI Setup (HG Ai)' but only 20 of 26,589 events were server-side, so the CAPI connection is effectively silent. Domains clean (site, book., GHL subdomains, 3 HG dev events); 257 Lead. Next action (Makenna / Leshan): check the HG AI CAPI connection for FLOHOM (decision 32)."),
 dict(client="Green Springs Inn",pid="1602971745164199",name="Green Springs Inn Event Data",acct="1390516335151357",flag=W,exp="greenspringsinn.com + Holiday Future",src="inferred",
  notes="Week 5: unchanged. Receives booking-engine events only (book.greenspringsinn.com, 23,668) and the same events land on the GSI Wix pixel (23,597 from the same host), so bookings are double-counted across the two pixels. Next action (Alicia): remove the booking-engine snippet from one pixel (decision 11)."),
 dict(client="Green Springs Inn",pid="1098954801239133",name="GSI - Wix Pixel",acct="1390516335151357",flag=M,exp="greenspringsinn.com | staygreenspringsinn.com + Holiday Future",src="inferred",
  notes="Clean on its own: site, booking engine, GHL subdomains; 36,051 events (−4%), half server. 7 events from invalid.invalid are a malformed referrer, noise. See the Event Data row for the double count."),
 dict(client="Hiawassee Glamping",pid="1149628220675980",name="Hiawassee Meta Pixel",acct="4219624811692502",flag=M,exp="hiawasseeglamping.com",src="inferred",
  notes="Clean. 17,494 events (−19%), half server, 215 Lead, 3 Purchase. Event Data pixel still dead."),
 dict(client="Home Base",pid="1467511861488785",name="Home Base Bnb - Meta Pixel",acct="3224125791099903",flag=M,exp="homebasebnbs.com | stayhomebase.com + Guesty",src="inferred",
  notes="Clean. 8,853 events (−16%), half server, 118 Purchase (the platform shows 171 direct bookings month to date, a strong month) and 52 Lead. homebase.rentamira.com did not recur; 50 events from 127.0.0.1 are dev."),
 dict(client="Inspired Retreats",pid="1547510566197386",name="Inspired Retreats Meta Pixel",acct="1494841894957652",flag=C,exp="stayinspiredretreats.com",src="inferred",
  notes="CROSS-CONTAMINATION, week 5, NOT fixed: go.staysaluda.com (521), links.staysaluda.com (328) and bio.staysaluda.com (180) fired this pixel on every day of the window, 1,029 events or 20% of its 5,213, at the same daily rate as before the 28 Sep and 7 Oct fixes (60 to 90 a day on go.). 50% of the pixel's events arrive server-side. Saluda's own pixel is clean, so the leak is one-way. Next action (Shawal / Leshan): the page-snippet and GHL pixel-events paths have been ruled out, so open the HG AI CAPI connector for Stay Saluda and the GHL sub-account's Facebook Conversions API integration and check which pixel ID each sends to; one of them carries 1547510566197386."),
 dict(client="Little River Landing",pid="1816709606431185",name="Little River Landing Meta Pixel",acct="884285717873613",flag=M,exp="staylittleriver.com",src="inferred",
  notes="Clean, third clean week after the North Star leak closed. 2,511 events (−9%), half server, 74 Lead. Netlify previews did not recur."),
 dict(client="Myrinn",pid="1943632852972363",name="Myrinn - Meta Pixel",acct="1668286333836716",flag=M,exp="staywithmyrinn.com",src="inferred",
  notes="Clean. 7,005 events (+16%), half server, 70 Lead. One sanitised over-long referrer, noise."),
 dict(client="Nature Nooks",pid="844302611320158",name="Nature Nooks - Meta Pixel",acct="1796752774213285",flag=M,exp="naturenooksacadia.com",src="inferred",
  notes="Clean. 3,087 events (−4%), half server, 174 Lead. Sheet says browser only; the server side is live, so the sheet understates the setup."),
 dict(client="North Star Resort & Lodge",pid="3440147309499983",name="North Star Lodge Killington - Meta Pixel",acct="2003562593933799",flag=W,exp="northstarkillington.com + GHL + Cloudbeds",src="inferred",
  notes="Week 5: the attached pixel carries the main site (624), the GHL funnel (174) and a trickle of Cloudbeds (12); 12 Purchase. Server events 12 of 822 (1%): the full plugin, script and API set is installed per the 14 Oct Strategy call, but CAPI volume has not followed yet. Funnel still split with the HG BM pixel below. Next action (Charlotte / Leshan): decision 9, pick the canonical pixel; confirm the CAPI connection is sending."),
 dict(client="North Star Resort & Lodge",pid="1904436107168032",name="Northstar Meta Pixel",acct="2003562593933799",flag=W,exp="northstarkillington.com + Cloudbeds",src="inferred",
  notes="Week 5: the HiddenGem BM pixel, not attached to the ad account, carries the Cloudbeds booking engine (1,201 of 1,410) and part of the GHL funnel, browser only; 10 Purchase, 19 Lead. The booking engine still only fires this pixel, so the attached pixel sees almost no purchases. Decision 9 open."),
 dict(client="Oak & Ember",pid="1729106025177871",name="Oak & Ember - Meta Pixel",acct="831762063342909",flag=M,exp="stayoakandember.com + Hospitable",src="inferred",
  notes="Clean. 23,977 events (+169%): the GHL funnel go.stayoakandember.com went from nothing to 5,398 events and the site doubled; 443 SubmitApplication, 100 Lead, half server. Event Data pixel still dead."),
 dict(client="Paradise Pointe",pid="707016175006193",name="Paradise Pointe - Pixel",acct="1585826092078255",flag=W,exp="stayparadisepointe.com",src="inferred",
  notes="Week 2: sheet says 'CAPI Setup (HG Ai)' but only 22 of 42,343 events were server-side; the CAPI connection is effectively silent. Domains clean; events −30% week on week; 71 Purchase, 3,521 InitiateCheckout, 305 Lead. The purchase-value check (decision 26) is still open. Next action (Makenna / Leshan): check the HG AI CAPI connection (decision 32)."),
 dict(client="Parker Reserve",pid="1188475652520634",name="Parker Reserve - Pixel",acct="1002927148609804",flag=W,exp="parkerreserve.com",src="inferred",
  notes="Week 5: parkerhouseohio.com down to 20 events (0.5%), still unconfirmed. Canva and Firebase strays did not recur. 3,756 events, half server. Next action (Kristal): confirm parkerhouseohio.com is a Parker property or remove the pixel from it."),
 dict(client="Ponderosa Pines Resort",pid="1293211539656211",name="Ponderosa Pines Resort - Meta Pixel",acct="1058846326445255",flag=M,exp="ponderosapinesresort.com + Newbook",src="inferred",
  notes="Clean. 29,434 events (−14%), 51% server, 64 Purchase, 585 Lead. Site, bio, Wix static host, Newbook booking engine."),
 dict(client="Ponderosa Pines Resort",pid="1743173753375733",name="Ponderosa Pines Resort's Pixel",acct="1058846326445255",flag=W,exp="ponderosapinesresort.com",src="inferred",
  notes="Week 2: the client-owned pixel, attached to the ad account, still fires PageView only from www.ponderosapinesresort.com (6,500 events, browser only), so page views are double-counted with the HG pixel above. Next action (Anna): confirm which pixel the ads use and remove the other from the site (decision 33)."),
 dict(client="Raven Rock Mountain",pid="1359649962298380",name="Raven Rock Meta Pixel",acct="1065186195582056",flag=W,exp="ravenrockmountain.com | stayravenrockmountain.com",src="inferred",
  notes="Week 5: domains clean (site plus links. and info. subdomains), 3,067 events, 7 Purchase, but the pixel is still NOT shared to ad account 1065186195582056 (the account lists zero pixels). Sheet says CAPI; 7 server events. Client is Not Live on the sheet. Next action (Anna): share the pixel to the account before any campaign relaunch."),
 dict(client="Red White & Blue Views",pid="1625871301864243",name="Red White & Blue - Meta Pixel",acct="1419930382946246",flag=M,exp="redwhiteandblueviews.com",src="inferred",
  notes="Clean. 38,856 events (−44% from 69,647: the book. booking-engine volume halved week on week), half server. Booking-engine custom events only, no standard Purchase."),
 dict(client="Ridge & Falls",pid="1332286819018269",name="Ridge & Falls - Meta Pixel",acct="1313401330776046",flag=W,exp="ridgeandfalls.com",src="inferred",
  notes="Week 2: server (CAPI) events still near zero, 6 of 3,342. Domains clean (site, GHL funnel), 71 Lead, 6 Purchase. The lead-campaign relaunch (actions log) has not happened. Next action (Makenna / Leshan): check the HG AI CAPI connection (decision 32)."),
 dict(client="Selah Place",pid="1235173718368839",name="Selah.Place Event Data",acct="1275283434220508",flag=M,exp="selah.place + Holiday Future",src="inferred",
  notes="Clean. 69,872 events (−41%; the holidayfuture booking engine is 86% of it), 48% server. New reserve.selah.place host (578) is the client's own booking subdomain, accepted. Booking-engine custom events only."),
 dict(client="Selah Place",pid="3327546500757583",name="LinkTree",acct="1275283434220508",flag=W,exp="selah.place | linktr.ee",src="inferred",
  notes="Week 5: unchanged. Second pixel still installed on www.selah.place (1,809 events), so page views are double-counted; 20 events from linktr.ee itself. Next action (Alicia): remove this pixel from the site, keep it on Linktree only."),
 dict(client="Starlight Haven - Hot Springs",pid="766226461367996",name="Starlight Haven Pixel - ResNexus",acct="901138032027913",flag=M,exp="visitstarlight.com + ResNexus",src="inferred",
  notes="Clean. One pixel shared by both Starlight accounts (this row: Hot Springs) and shared into Taberg's account, browser only as the sheet says. resnexus.com is the largest host; 36,985 events (−1%), 83 Purchase, 1,221 Lead."),
 dict(client="Starlight Haven - Weiss Lake",pid="766226461367996",name="Starlight Haven Pixel - ResNexus",acct="74756899",flag=M,exp="visitstarlight.com + ResNexus",src="inferred",
  notes="Clean. Same pixel as Hot Springs (this row: Weiss Lake); see that row for the figures."),
 dict(client="Stay on 30a",pid="1464927198465632",name="Stay on 30a - Meta Pixel",acct="25640434272252212",flag=M,exp="stayon30a.com | stayson30a.com",src="inferred",
  notes="Clean. 56,024 events (+4%), half server, 19 Purchase, 515 Lead. Dev hosts and the Guesty booking engine did not recur. links.stayson30a.com spelling still unconfirmed."),
 dict(client="Stay Saluda NC",pid="4250460185185664",name="Stay Saluda - Meta Pixel",acct="1863632561215857",flag=M,exp="staysaluda.com",src="inferred",
  notes="Clean on its own pixel. 20,585 events (−14%), half server, 489 Lead, 1 Purchase. The Saluda GHL hosts also fire the Inspired Retreats pixel (see that row)."),
 dict(client="Stay Southern Illinois",pid="1328561309169535",name="Southern Illinois Cabins - Meta Pixel",acct="1661949078036229",flag=W,exp="southernilcabins.com | staysouthernillinois.com | shawneeforestcabins.com | woodlandcabins.net | newvillagevacationhomes.com + OwnerRez",src="inferred",
  notes="Week 5: unchanged. Sister brand sites still fire into this pixel: shawneeforestcabins.com (4,725), woodlandcabins.net (1,945), newvillagevacationhomes.com (56), 16% of 42,721 events; 35 Purchase, 153 Lead, half server. Next action (Chiara): confirm the three sister brands belong to the client so the row can close."),
 dict(client="Stay With Branch",pid="1107997340818783",name="Branch",acct="1269399754049770",flag=W,exp="staywithbranch.com | gostaywithbranch.com + Guesty",src="inferred",
  notes="Week 2: server (CAPI) events silent, 0 of 2,567. Domains clean (site, Guesty booking engine, GHL subdomains); 77 SubmitApplication, 7 InitiateCheckout, no Purchase. Next action (Kristal / Leshan): check the HG AI CAPI connection (decision 32)."),
 dict(client="StayLuxe",pid="4293491110916917",name="StayLuxe Meta Pixel",acct="25033578722931437",flag=M,exp="stayluxe.vacations | gostayluxevacations.com + Uplisting",src="inferred",
  notes="Clean. 1,196 events (+7%), half server, 19 Lead. Low volume matches the $20/day budget."),
 dict(client="Sunapee Stays",pid="471248637966769",name="sunapeestays's Pixel",acct="651114096215889",flag=W,exp="sunapeestays.com",src="sheet",
  notes="Week 2: sheet says 'CAPI Setup (HG Ai)' but only 10 of 7,905 events were server-side. Domains clean; 10 Purchase, 70 CompleteRegistration, 29 Lead. CRM now lists the client as Basic (benchmark scope change), the pixel check continues. Next action (Charlotte / Leshan): check the HG AI CAPI connection (decision 32)."),
 dict(client="Taberg Falls",pid="964214909847907",name="Taberg Falls - Meta Pixel",acct="827872700004659",flag=M,exp="tabergfalls.com",src="inferred",
  notes="Clean. 63,707 events (−18%, in line with the 13 Oct budget cut), 40% server, 2,446 Lead, 9 Purchase; 9 localhost events are dev. The account still lists five other clients' pixels (FLOHOM, Paradise Pointe, Starlight Haven, The Cohost Company, Treetop Escapes), decision 13."),
 dict(client="The Cohost Company",pid="638998632168952",name="The Cohost Company Meta Pixel",acct="9141035462679902",flag=M,exp="thecohostcompany.com | gocohostcompany.com",src="inferred",
  notes="Clean. 9,463 events (−1%), 214 Lead, 7 Purchase. 7 server events (sheet says 'Full Tracking (AI Site)', not CAPI, so not flagged, as last week). localhost 2 is dev."),
 dict(client="The Outpost",pid="1691591692267740",name="HG - The Outpost Grand Canyon Event Data",acct="1530849534802936",flag=W,exp="outpostgrandcanyon.com",src="inferred",
  notes="Week 5: the HiddenGem-managed pixel still receives only link-in-bio events (895, about 130 a day; 85 Lead, half server). Site and booking engine fire the client-owned pixel below; the funnel is split. Decision 10 open. Next action (Anna): pick one pixel and install it on the site too."),
 dict(client="The Outpost",pid="734783866381382",name="Outpost Grand Canyon",acct="1530849534802936",flag=W,exp="outpostgrandcanyon.com + Newbook",src="inferred",
  notes="Week 5: client-BM pixel, browser only, carries the site (793) and the Newbook booking engine (2,820); 6 booking_confirmation, 72 add_booking, no standard Purchase. See the row above."),
 dict(client="Three Suns Cabins",pid="691977289952800",name="Three Suns Cabins - Pixel",acct="1210218584137342",flag=W,exp="threesunscabins.com",src="inferred",
  notes="Week 5: still no events from the main website, only the link-in-bio page (258, about 40 a day); 10 Purchase arrived server-side (CAPI), 19 SubmitApplication. The pixel base code is missing from threesunscabins.com. Next action (Anna): install the pixel on the site; confirm the domain."),
 dict(client="Treetop Escapes",pid="1178838797064774",name="Treetop Escapes - Pixel",acct="967636478877602",flag=M,exp="staytreetopescapes.com + Guesty",src="inferred",
  notes="Clean. 49,160 events (+10%), 46% server, 1,168 Lead, 11 Purchase. michigan.guestybookings.com (14) is the Guesty booking engine for the uniquestays account, accepted. Pixel also shared into Taberg's account."),
 dict(client="Tuxedo Falls",pid="1561325308991270",name="Tuxedo Falls - Ad Account's Pixel",acct="2077151009889326",flag=W,exp="tuxedofalls.com",src="inferred",
  notes="Week 5: ZERO events, silent since 1 Sep (7 weeks). The ad account's only attached pixel is empty while the real tracking runs on 'Website' 1839806973541001 below. Next action (Chiara): share the Website pixel to the ad account and retire this one (decision 18)."),
 dict(client="Tuxedo Falls",pid="1839806973541001",name="Website",acct="2077151009889326",flag=W,exp="tuxedofalls.com + ResNexus + GHL",src="inferred",
  notes="Week 4: live pixel carrying the site (9,603), ResNexus (4,144) and the GHL funnel (1,990); 15,945 events (−25%), 8 Purchase, browser only, still NOT shared to ad account 2077151009889326. Decision 18."),
 dict(client="Walden Retreats",pid="505477285266646",name="Walden Retreat's Data",acct="973261794434226",flag=M,exp="waldenretreats.com + ResNexus",src="inferred",
  notes="Clean. 20,139 events (+29%), half server, 99 Purchase, 171 Lead, plus the wedding funnel's custom events (1,490 'Wedding page view', 52 'Wedding Inquiry Form (click)'). spacecrafted.com (18) is the site builder's host, accepted."),
 dict(client="Glasscombe",pid="1369498611461163",name="Aero Camp Pixel",acct="",flag=W,exp="glasscombe.com + Cloudbeds",src="inferred",
  notes="New row: Glasscombe joined the Master sheet on 15 Oct. Its pixel is named 'Aero Camp Pixel', owned by business 'Glasscombe' (806512758639975) and shared into the HG BM; it fires from www.glasscombe.com (5,429), bio.glasscombe.com (2,247), the Cloudbeds booking engine us2.cloudbeds.com (2,107) and reserve.glasscombe.com (45); 13,160 events, 39% server-side (CAPI live), 5 Purchase, 433 Lead. No ad account in the client map yet, so it is not attached to anything Claude can see. Next action (Charlotte): confirm this is the pixel the ads will use and add the ad account ID to PROJECT.md section 5; the domain is inferred from the brand name."),
]

# ---------- compute ----------
def events_of(pid): return px[pid]["total_events"] if pid in px else 0
def hosts_of(pid):
    if pid not in px: return []
    return [h for h,v in sorted(px[pid]["hosts"].items(), key=lambda kv:-kv[1]["count"])]
def server_of(pid):
    p=px.get(pid); return "Y" if p and p["server_events"]>0 else "N"
prevfiles=sorted(f for f in glob.glob(os.path.join(OUT,"*-pixel-domain-check.csv")) if os.path.basename(f)[:10]<TODAY)
PREV=os.path.basename(prevfiles[-1]) if prevfiles else None
prev={}
if prevfiles:
    for r in csv.DictReader(open(prevfiles[-1],encoding="utf-8")): prev[(r["pixel_id"],r["client"])]=r
FLAGGED=(W,C,B)
for r in ROWS:
    r["events"]=events_of(r["pid"]); r["hosts"]=hosts_of(r["pid"]); r["server"]=server_of(r["pid"])
    p=prev.get((r["pid"],r["client"])) or next((v for (pid,c),v in prev.items() if pid==r["pid"] and c.startswith(r["client"][:10])),None)
    if p is None: r["diff"],r["weeks"]="new",(1 if r["flag"] in FLAGGED else 0); continue
    pw=int(p.get("weeks_open") or 0)
    if p["flag"] in FLAGGED and r["flag"] in FLAGGED: r["diff"],r["weeks"]="still_open",pw+1
    elif p["flag"] in FLAGGED and r["flag"] not in FLAGGED: r["diff"],r["weeks"]="fixed",0
    elif p["flag"] not in FLAGGED and r["flag"] in FLAGGED: r["diff"],r["weeks"]="new",1
    else: r["diff"],r["weeks"]="unchanged",0
seen={(r["pid"],r["client"]) for r in ROWS}
removed=[v for k,v in prev.items() if k not in seen and not any(k[0]==r["pid"] and k[1].startswith(r["client"][:10]) for r in ROWS)]
ROWS.sort(key=lambda r:(r["client"],r["pid"]))
distinct={r["pid"] for r in ROWS}
total_events=sum(px[p]["total_events"] for p in distinct if p in px)
counts=collections.Counter(r["flag"] for r in ROWS)
ICON={M:"✅",W:"⚠️",C:"❌",B:"🔴"}
fixed=[r for r in ROWS if r["diff"]=="fixed"]
new_flags=[r for r in ROWS if r["diff"]=="new" and r["flag"] in FLAGGED]

# ---------- md ----------
L=[]
L.append(f"# Meta Pixel Domain Check, {TODAY}\n")
L.append(f"**Date:** {TODAY} · **Clients on sheet:** {CLIENTS_ON_SHEET} ({CLIENTS_ON_SHEET-len(OFFBOARDED_EXCLUDED)} checked) · **Pixel rows reviewed:** {len(ROWS)} ({len(distinct)} distinct pixels) · **Receiving events correctly:** {counts[M]} ✅ · **Critical:** {counts[C]} ❌ · **Warnings:** {counts[W]} ⚠️ · **Blocked:** {counts[B]} 🔴 · **Total events, last 7 days:** {total_events:,}\n")
L.append(f"Fifth run (Monday). Compared against the {PREV[:10]} report. Read through the Meta Marketing API with the HiddenGem-Claude system user, now the standing data path (`scripts/pull-pixel-stats.mts`, {WINDOW}, window ending 09:42 PT): each pixel's 7-day host breakdown with per-day counts, event totals and browser/server split. Canopy at Moody Moon Ridge is offboarded and no longer checked; Glasscombe gets its first row. Expected domains are still the inferred set from the first run (see footer). Checked against the actions log in PROJECT.md section 9.\n")
HDR="| Client | Pixel Name | Pixel ID | Events (last 7d) | Domains Seen | Expected Domain(s) | Match | Notes/Issues |\n|---|---|---|---|---|---|---|---|"
def trow(r): return f"| {r['client']} | {r['name']} | {r['pid']} | {r['events']:,} | {', '.join(r['hosts']) if r['hosts'] else 'none'} | {r['exp']} | {ICON[r['flag']]} | {r['notes']} |"
L.append("## Critical issues (❌ and 🔴)\n")
crit=[r for r in ROWS if r["flag"] in (C,B)]
if crit:
    L.append("**The Saluda → Inspired Retreats leak is in its fifth week and neither fix has changed it; no pixel is blocked now that Canopy is out of scope:**\n")
    for i,r in enumerate(crit,1):
        L.append(f"{i}. **{r['client']} ({r['name']}, {r['pid']}).** {r['notes']}\n")
    L.append(HDR)
    for r in crit: L.append(trow(r))
    L.append("")
else: L.append("None.\n")
L.append("## Warnings (⚠️)\n")
warn=[r for r in ROWS if r["flag"]==W]
nw=[r for r in warn if r["diff"]=="new"]; cw=[r for r in warn if r["diff"]!="new"]
L.append(f"{len(nw)} new this week, {len(cw)} carried over from {PREV[:10]}. New rows first, then still-open rows.\n")
L.append("**CAPI is still effectively silent on six clients the sheet marks as 'CAPI Setup (HG Ai)'** (Asheville 0, Stay With Branch 0, Ridge & Falls 6, Sunapee 10, FLOHOM 20, Paradise Pointe 22 server events out of thousands). Nothing changed on any of them since 13 Oct; decision 32 is still with the AMs and Leshan.\n")
L.append("**Glasscombe gets its first row.** The client joined the Master sheet on 15 Oct; its pixel is live with CAPI but carries the name 'Aero Camp Pixel' and there is no ad account in the client map yet.\n")
L.append(HDR)
for r in nw+cw: L.append(trow(r))
L.append("")
L.append("## Fixed since last week\n")
if fixed:
    L.append(HDR)
    for r in fixed: L.append(trow(r))
else:
    L.append("None. Every flag from 13 Oct carries over. The one row that left the report is Canopy at Moody Moon Ridge (🔴 last week), dropped because the client is offboarded, not because it was fixed.")
L.append("")
L.append("## All pixels (alphabetical by client)\n")
L.append("| Client | Pixel Name | Pixel ID | Events (last 7d) | Domains Seen | Expected Domain(s) | Match | Notes/Issues |")
L.append("|---|---|---|---|---|---|---|---|")
for r in ROWS:
    L.append(f"| {r['client']} | {r['name']} | {r['pid']} | {r['events']:,} | {', '.join(r['hosts']) if r['hosts'] else '—'} | {r['exp']} | {ICON[r['flag']]} | {r['notes']} |")
L.append("")
silent=[r for r in ROWS if r["events"]==0 and r["flag"]!=B]
notsheet=[p for p in pull["pixels"] if not p.get("skipped") and p["id"] not in distinct and p["id"]!="861460105842405"]
L.append("## Footer\n")
L.append(f"- Clients on sheet: {CLIENTS_ON_SHEET} ({CLIENTS_ON_SHEET-NOT_LIVE-1} Live, {NOT_LIVE} Not Live, 1 offboarded and excluded: {', '.join(OFFBOARDED_EXCLUDED)}). Big Moon Ranch is offboarded too but still on the sheet, so it keeps its row. Pixel rows: {len(ROWS)} ({len(distinct)} distinct pixels; Starlight Haven's pixel serves both accounts, Columbia Gorge, Green Springs, North Star, Ponderosa, Selah, The Outpost and Tuxedo Falls have two rows each, Glasscombe is new).")
L.append(f"- Pixels found: {len(distinct)}. With events: {len([p for p in distinct if events_of(p)>0])}. Silent: {len(silent)} ({', '.join(r['name'] for r in silent)}). Blocked: {counts[B]}.")
L.append(f"- Total events across all pixels, {WINDOW}: {total_events:,} (each shared pixel counted once, from the API's event totals, comparable with last week's 994,294).")
L.append("- Server events column: Y = at least one server (CAPI) event inside the 7-day window; the notes give the share. Browser-only by design per the sheet: Starlight Haven, The Outpost (client pixel), Columbia Gorge Getaways (CGG Pixel), Ponderosa's second pixel. Sheet says CAPI but the server side is silent or near-silent: Asheville (0), Stay With Branch (0), Ridge & Falls (6), Sunapee (10), FLOHOM (20), Paradise Pointe (22). The Cohost Company (7 server events) is marked 'Full Tracking (AI Site)', not CAPI, so it is not flagged.")
L.append(f"- Ad accounts listed through the API: {len(pull['clients'])} client accounts, 0 listing errors; the only read error was Canopy's pixel (no system-user access, client offboarded). Raven Rock Mountain still has zero pixels attached. Táberg Falls' account still lists five other clients' pixels. Fifteen attached pixels never fired in the window (Event Data and test pixels), listed in the notes where relevant.")
L.append("- Pixels in the HG BM that belong to no sheet client and fired in the last 28 days: "+", ".join(sorted(f"{p['name']} ({p['total_events']:,})" for p in notsheet if p['total_events']>0))+". Cabin Collective (CRM Advanced, no ad account yet) already has two live pixels on cabincollectivebb.com, one browser-only with Wix and OwnerRez hosts and one with CAPI; worth settling before its account launches. Never fired or dead: "+", ".join(sorted(p['name'] for p in notsheet if p['total_events']==0))+".")
L.append(f"- Previous report compared against: {PREV}. Diff joined on pixel ID. Rows removed since last week: "+("; ".join(f"{v['client']} ({v['pixel_id']}, was {v['flag']})" for v in removed) if removed else "none")+".")
L.append("- Expected domains: every row is still `inferred` from the brand name plus observed traffic (first run), except Sunapee Stays (`sheet`). Inferred domains that contain the client's brand name are treated as confirmed; the ⚠️ for inference applies only where it does not (parkerhouseohio.com, the Southern Illinois sister brands, links.stayson30a.com). Confirm with Shawal and flip `source` to `confirmed` in `expected-domains.csv`.")
L.append("- Data path from this week: the claude.ai Meta connector is not used; `pixel_pull.json` in the skill folder is the whole Meta read (listings, hosts per hour, event totals, browser/server split). EMQ is not pulled on this path.")
open(os.path.join(OUT,f"{TODAY}-pixel-domain-check.md"),"w",encoding="utf-8").write("\n".join(L)+"\n")
with open(os.path.join(OUT,f"{TODAY}-pixel-domain-check.csv"),"w",newline="",encoding="utf-8") as fh:
    w=csv.writer(fh); w.writerow("run_date,client,pixel_id,pixel_name,ad_account_id,events_7d,server_events,domains_seen,expected_domains,expected_source,flag,diff_status,weeks_open,notes".split(","))
    for r in ROWS:
        w.writerow([TODAY,r["client"],r["pid"],r["name"],r["acct"],r["events"],r["server"],"|".join(r["hosts"]),r["exp"].replace(" | ","|"),r["src"],r["flag"],r["diff"],r["weeks"],r["notes"]])
print("rows",len(ROWS),"distinct",len(distinct),"counts",dict(counts),"total",total_events,"removed",[(v['client']) for v in removed])
print("diff",collections.Counter(r["diff"] for r in ROWS))
