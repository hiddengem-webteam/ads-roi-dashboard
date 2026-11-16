"""Writes the dated pixel domain check .md and .csv from pixel_pull.json.

The per-pixel flags, expected domains and notes are authored by Claude in
ROWS below each week (the judgement part of the audit); events, hosts,
browser/server split and the week-over-week diff are computed here.
"""
import json, csv, os, glob, datetime, collections
SP=os.path.dirname(os.path.abspath(__file__))
ROOT=os.path.abspath(os.path.join(SP,"..","..",".."))
OUT=os.path.join(ROOT,"weekly","Meta Pixel Reviews","Weekly Checks")
TODAY="2026-11-16"
pull=json.load(open(os.path.join(SP,"pixel_pull.json"),encoding="utf-8"))
px={p["id"]:p for p in pull["pixels"]}
# Purchase check inputs (2026-10-30): PMS bookings and HG AI CAPI state saved by the run, rules in purchase_rules.py
import sys; sys.path.insert(0,SP)
from purchase_rules import judge
def _load(name,key="rows"):
    f=os.path.join(SP,name)
    return {r["name"]:r for r in json.load(open(f,encoding="utf-8"))[key]} if os.path.exists(f) else {}
PMS=_load("pms_direct_28d.json"); CAPI=_load("capi_status.json")
SHEET={r[0]:{"attribution":r[1],"status":r[2]} for r in json.load(open(os.path.join(SP,"sheet_status.json"),encoding="utf-8"))["rows"]} if os.path.exists(os.path.join(SP,"sheet_status.json")) else {}
_sp=sorted(glob.glob(os.path.join(ROOT,"weekly","Ad Spends Checks","Weekly Checks","*-ad-spend-check.csv")))
SPEND={r["client"]:r for r in csv.DictReader(open(_sp[-1],encoding="utf-8"))} if _sp else {}
def _f(x):
    try: return float(x or 0)
    except ValueError: return 0.0
CLIENTS_ON_SHEET=len(SHEET) or 47; NOT_LIVE=sum(1 for v in SHEET.values() if not v["status"].lower().startswith("live")); OFFBOARDED_EXCLUDED=["Canopy at Moody Moon Ridge"]
NOT_CHECKED=["Nine Pines Retreats"]  # on the sheet, no ad account, no ads running yet (Shawal, 2026-11-09); Gooseberry mapped 2026-11-16
WINDOW="9 Nov to 16 Nov"
OFF_SHEET=["Dunya Camp"]  # in the client map (2026-11-16, Shawal) but not on the Master sheet
DUNYA_ACCT_NOTE="Dunya Camp joined the client map after the pull; its account's pixel list (act_629838998232110/adspixels) hit Meta's per-account rate limit on two single ad-hoc reads, so its attached pixels are unknown this week."

M,W,C,B="match","warning","critical","blocker"
ROWS=[
 dict(client="American River Resort",pid="2862601447415133",name="American River Resort - Meta Pixel",acct="953162737054331",flag=M,exp="americanriverresort.com",src="inferred",
  notes="Clean. Ads off since 15 Oct (paused, not offboarded). 5,063 events (−1%), half server, no Lead or Purchase; the site still fires and the GHL funnel sent 34 events."),
 dict(client="Asheville River Cabins",pid="1634367080775220",name="Asheville River Cabins Meta Pixel",acct="615836588009747",flag=W,exp="ashevillerivercabins.com + Cloudbeds",src="inferred",
  notes="Week 9: domains clean (Cloudbeds booking engine 13,842, site 7,807, GHL 608, bio 406); 22,715 events (−1%), 202 Lead, 62 Purchase in the week. Still 0 server events while the sheet says 'CAPI Setup (HG Ai)': the HG AI CAPI has never sent for this tenant (no PMS connection; Cloudbeds API access is with Leshan), so all 258 Purchases in 28 days are browser-side. On 12 Nov the 26.4x BoF retargeting campaign was turned into 'MoF - Broad' and a new $20/day BoF retargeting campaign started, so the BoF campaign now learns from scratch on browser Purchases only. Next action (Charlotte / Leshan): get the Cloudbeds API access so the HG AI CAPI can send, and correct the sheet until it does."),
 dict(client="Away2PA",pid="772693422494226",name="Away 2PA Meta Pixel",acct="603977626130795",flag=M,exp="away2pa.com | awaytopa.com",src="inferred",
  notes="Clean on domains. 47,815 events (−35%) as last week's traffic surge eased, still well above October (away2pa.com 40,610, bio.awaytopa.com 5,276, OwnerRez 1,617); 612 Lead, 39 Purchase, half server. Purchase 28d: 101 (29 browser / 72 server) against 44 PMS direct bookings: server is now 1.6x bookings, past the 1.5x over-count line (1.44x last week), because the HG AI CAPI (on, 47 sent) and OwnerRez both send each booking without a shared event_id. Next action (Alicia / Leshan): keep one server sender for Away2PA."),
 dict(client="Awayframes",pid="773898245792839",name="Awayframes - Meta Pixel",acct="2471256056603833",flag=M,exp="awayframes.com",src="inferred",
  notes="Clean. 19,378 events (+8%), 572 Lead, 12 Purchase, 39% server. Two Netlify previews (18 events) are HG dev. Purchase 28d: 35, all server, against 30 PMS online bookings (117%); the HG AI CAPI is OFF (nothing sent since 28 Oct), so Hostaway's CAPI is the only sender and the browser never fires Purchase."),
 dict(client="Best Texas Travel",pid="4108409325970216",name="Best Texas - Meta Pixel",acct="1982551189319458",flag=M,exp="besttexastravel.com | riverroadcabins.com + Holiday Future",src="confirmed",
  notes="River Road Cabins is the client's own brand (Shawal, 16 Nov), so its hosts are expected and decision 37 is closed: bookings.riverroadcabins.com 19,262 (7,092 on 14 Nov alone), riverroadcabins.com 2,351 and riverroadcabins.holidayfuture.com 230, 65% of 33,754 events. Best Texas Travel's own hosts: book. 9,675 (half of last week), site 1,334, bio 607. Purchase 28d: 27, all server, against 30 PMS online bookings (90%; HG AI CAPI on, 30 sent)."),
 dict(client="Big Moon Ranch",pid="1208874174466414",name="Big Moon Ranch - Meta Pixel",acct="758851247064974",flag=W,exp="bigmoonranch.com | staybigmoonranch.com",src="inferred",
  notes="Week 7: client offboarded 28 Sep, but the HG BM pixel is still on bigmoonranch.com: 5,366 events (+3%), 51% server, so a CAPI connection is still sending too. Still on the Master sheet. Next action (Charlotte): remove the pixel from the site, disconnect the CAPI connection, and take the row off the sheet (decision 25)."),
 dict(client="Bison Ridge Retreat",pid="1241959234316508",name="Bison Ridge - Meta Pixel",acct="950241787963535",flag=M,exp="bisonridgeretreat.com",src="inferred",
  notes="Clean (site 4,243, bio 534, link. 320; 4 events from msn.com and an e-reader referrer are noise). 5,175 events (+3%), half server, 122 Lead, no Purchase. No Purchase in 28 days with $5/day on BoF and no PMS in the platform to compare: the booking confirmation carries no Purchase event (Chiara). The CRM moved Bison Ridge to Basic on 12 Nov; the Master sheet still lists it with $30/day live. Event Data pixel 1617239586052069 still attached with no events."),
 dict(client="Cabin Collective",pid="1654110122884436",name="Cabin Collective BB Meta Pixel (New)",acct="2194562394139883",flag=M,exp="cabincollectivebb.com + OwnerRez",src="inferred",
  notes="Clean, fourth week. 12,065 events (+5%), half server, 175 Lead, 8 Purchase; site 10,087, the HG landing page on Netlify 855, OwnerRez 807, bio 273, Bluehost staging 16. Purchase 28d: 59 (32 browser / 27 server) against 29 PMS online bookings. The pixel is now assigned in HG AI and the platform's CAPI sent its first 4 Purchases on 16 Nov, so from next week OwnerRez and the HG AI CAPI both send server Purchases; watch for an over-count. The old 'Cabin Collective BB Pixel' 1338006181525466 is still attached, dead since 15 Oct. Sheet Status still reads Not Live with $30/day running since 20 Oct, which keeps the Purchase check at n/a. Next action (Chiara): set the sheet row to Live and detach the dead pixel."),
 dict(client="Columbia Gorge Getaways",pid="595257656540749",name="CGG Pixel",acct="490940113157881",flag=W,exp="columbiagorgegetaways.com | columbiagorgeglamping.com",src="inferred",
  notes="Week 9: unchanged. Fires only from the Wix static host (474) and the GHL funnel go.columbiagorgeglamping.com (317), never from the main site, browser only; 11 Lead. Two live pixels on one client. Next action (Chiara): put the primary pixel on the GHL funnel pages and retire this one, or record it as the funnel pixel."),
 dict(client="Columbia Gorge Getaways",pid="700947282709400",name="Columbia Gorge Getaways Pixel",acct="490940113157881",flag=M,exp="columbiagorgegetaways.com + ResNexus",src="inferred",
  notes="Clean. Main site 4,695 and the ResNexus engine 1,619; 6,407 events (−14%), 39% server, 8 Purchase for the second week running. Purchase 28d: 22 (12 browser / 10 server); no PMS in the platform to compare."),
 dict(client="Endless Stays",pid="876508505381758",name="Endless Stays Meta Pixel",acct="896372356081479",flag=M,exp="stayendless.com + Hospitable",src="inferred",
  notes="Clean on domains. 38,132 events (−40%), back to the usual 3,500 to 5,500 a day after last week's 7 Nov spike; 610 Lead, 6 Purchase, half server; 3 events from 127.0.0.1 are a local build. Purchase 28d: 15, all server, against 18 PMS online bookings (83%); the HG AI CAPI (on, 18 sent) is the only Purchase sender and the booking confirmation fires no browser Purchase. A new $50/day MoF lookalike sales campaign started on 13 Nov."),
 dict(client="Evergreen Cabins",pid="1474685406530880",name="Evergreen Cabins Meta Pixel",acct="453808647114273",flag=M,exp="evergreencabins.co + Hospitable",src="inferred",
  notes="Clean. 26,235 events (−23%), 28% server, 84 Lead, 7 Purchase; 12 from the GHL API host, 2 from the site's Kinsta staging host. Purchase 28d: 39, all server, against 38 PMS online bookings (HG AI CAPI on, 40 sent); the browser never fires Purchase."),
 dict(client="FLOHOM",pid="139231105894533",name="FLO2 Conversion",acct="2100710320122219",flag=M,exp="flohom.com | goflohom.com",src="inferred",
  notes="Clean. 26,729 events (+7%), 166 Lead, 26 Purchase in the week; book.flohom.com 11,945 (4,408 of them on the morning of 16 Nov, mostly gallery_interaction), site 13,685; 1 event from an HG SiteGround staging host. Purchase 28d: 94 (11 browser / 83 server) against 98 PMS online bookings (96%); the HG AI CAPI is OFF and Hostaway's CAPI is the sender."),
 dict(client="Glasscombe",pid="1369498611461163",name="Aero Camp Pixel",acct="2030318804465316",flag=M,exp="glasscombe.com + Cloudbeds",src="inferred",
  notes="Clean. 13,535 events (+1%), 39% server, 344 Lead, 8 Purchase in the week (20 the week before). Purchase 28d: 34 (11 browser / 23 server) against 21 PMS online bookings; the server side is the HG AI CAPI (on, 17 sent) plus Cloudbeds, within the over-count line. Pixel still named 'Aero Camp Pixel'; cosmetic."),
 dict(client="Green Springs Inn",pid="1602971745164199",name="Green Springs Inn Event Data",acct="1390516335151357",flag=W,exp="greenspringsinn.com + Holiday Future",src="inferred",
  notes="Week 9: unchanged. Receives booking-engine events only (book.greenspringsinn.com, 26,069), the same host that fires the Wix pixel, so bookings are counted on both pixels; 34 Purchase here this week. Purchase 28d: 188 (94 browser / 94 server) against 88 PMS online bookings, about 2.1x. Next action (Alicia): remove the booking-engine snippet from one pixel (decision 11)."),
 dict(client="Green Springs Inn",pid="1098954801239133",name="GSI - Wix Pixel",acct="1390516335151357",flag=M,exp="greenspringsinn.com | staygreenspringsinn.com + Holiday Future",src="inferred",
  notes="Clean on its own: booking engine 25,424, site 8,745, GHL subdomains 545; 35,374 events (−15%), 48% server, 17 Purchase. The HG GSI site build on Cloudflare Pages still carries the live pixel (18 events from two pages.dev pull-request previews); drop it from preview builds before launch (Leshan). 6 events from www.aocr.org on one day are a referring page, negligible. Purchase 28d: 82, all server (HG AI CAPI on, 89 sent), against 88 PMS online bookings (93%). See the Event Data row for the double count."),
 dict(client="Hiawassee Glamping",pid="1149628220675980",name="Hiawassee Meta Pixel",acct="4219624811692502",flag=M,exp="hiawasseeglamping.com",src="inferred",
  notes="Clean. 8,770 events (−23%), half server, 132 Lead, 4 Purchase (1 last week). Purchase 28d: 14, all server, against 12 PMS online bookings (HG AI CAPI on, 15 sent)."),
 dict(client="Home Base",pid="1467511861488785",name="Home Base Bnb - Meta Pixel",acct="3224125791099903",flag=M,exp="homebasebnbs.com | stayhomebase.com + Guesty",src="inferred",
  notes="Clean. 9,571 events (+32%), half server, 50 Lead, 38 Purchase; the Guesty booking engine fired 313 events (36 last week) and the client's own host. and staging subdomains 30. Purchase 28d: 125 (1 browser / 124 server) against 38 online and 154 direct PMS bookings: the HG AI CAPI (on, 82 sent) sends every direct booking, owner and manual entries included, so the BoF campaign optimises partly on bookings no ad could have driven. Within the over-count rule, which is judged on direct bookings."),
 dict(client="Inspired Retreats",pid="1547510566197386",name="Inspired Retreats Meta Pixel",acct="1494841894957652",flag=M,exp="stayinspiredretreats.com",src="inferred",
  notes="Domain issue closed (Shawal, 16 Nov): the Stay Saluda GHL hosts on this pixel are blocked. This window's host stats still list go.staysaluda.com (595), bio.staysaluda.com (200) and links.staysaluda.com (177), 972 events or 21% of 4,597, so next week's run checks that they drop out. One server Purchase on 10 Nov (Guesty; the HG AI CAPI is OFF) against 5 PMS online bookings with $5/day on BoF; see the Purchase check."),
 dict(client="Little River Landing",pid="1816709606431185",name="Little River Landing Meta Pixel",acct="884285717873613",flag=M,exp="staylittleriver.com",src="inferred",
  notes="Clean on domains, seventh clean week: site 1,551, GHL funnel 467, 2 events from a local build; 2,026 events (−13%), half server, 51 Lead, 1 Purchase. Purchase 28d: 5, all server, against 11 PMS online bookings (45%), so the Purchase check moves from ❌ to ⚠️ on the count alone; nothing changed in the setup. The Sales budget rose to $40/day (BoF $20 plus a new $20 lookalike from 13 Nov) on the same weak signal: the HG AI CAPI is OFF (one send ever, 30 Sep), the browser never fires Purchase, and the few server Purchases come from Guesty. Next action (Makenna / Leshan): turn the HG AI CAPI on for the tenant or get the Guesty booking engine to fire Purchase in the browser."),
 dict(client="Myrinn",pid="1943632852972363",name="Myrinn - Meta Pixel",acct="1668286333836716",flag=M,exp="staywithmyrinn.com",src="inferred",
  notes="Clean. 4,780 events (+43%), half server, 52 Lead, 1 Purchase. Purchase 28d: 5, all server, against 5 PMS online bookings (HG AI CAPI on, 5 sent)."),
 dict(client="Nature Nooks",pid="844302611320158",name="Nature Nooks - Meta Pixel",acct="1796752774213285",flag=M,exp="naturenooksacadia.com",src="inferred",
  notes="Clean. 424 events (−64%), second week with all campaigns paused (Kristal, 4 Nov; account $0/day). No Purchase; the Purchase check is n/a while ads are off."),
 dict(client="North Star Resort & Lodge",pid="3440147309499983",name="North Star Lodge Killington - Meta Pixel",acct="2003562593933799",flag=W,exp="northstarkillington.com + GHL + Cloudbeds",src="inferred",
  notes="Week 9: the Cloudbeds engine fired 13 events on seven days (9 last week), so a few booking pages carry the pixel but most still do not. Site events halved (705 against 1,465), GHL funnel 298; 1,027 events (−44%), 41 Lead, 13 Purchase, all server from the HG AI CAPI (14 sent in 7 days). Purchase 28d: 27 against 76 PMS online bookings (36%), but 34 of the direct bookings are 'Default Corporate Client' and 11 'RCI' that most likely never pass a page with the pixel; against the 28 'Website/Booking Engine' bookings the server Purchases match about one for one. Next action (Charlotte / Leshan): reinstall the account pixel in the Cloudbeds engine so the browser Purchase fires again; decision 9 still open."),
 dict(client="North Star Resort & Lodge",pid="1904436107168032",name="Northstar Meta Pixel",acct="2003562593933799",flag=W,exp="northstarkillington.com + Cloudbeds",src="inferred",
  notes="Week 9: dead. Zero events this week, last fired 26 Oct; its last browser Purchases (Cloudbeds, up to 19 Oct) have now left the 28-day window. Not attached to the ad account. Next action (Charlotte): once the account pixel above is the one installed in Cloudbeds, retire this one and close decision 9."),
 dict(client="Oak & Ember",pid="1729106025177871",name="Oak & Ember - Meta Pixel",acct="831762063342909",flag=M,exp="stayoakandember.com + Hospitable",src="inferred",
  notes="Clean. 17,153 events (−21%), half server, 81 Lead; GHL funnel 3,210, Hospitable 90; a traffic spike on 14 and 15 Nov (4,134 and 3,193 site events). No Purchase in 28 days with $5/day on BoF and a Hospitable PMS the platform cannot read, so capture cannot be judged; the booking confirmation fires no Purchase event either way (Chiara)."),
 dict(client="Paradise Pointe",pid="707016175006193",name="Paradise Pointe - Pixel",acct="1585826092078255",flag=M,exp="stayparadisepointe.com",src="inferred",
  notes="Clean. 33,119 events (+3%), 312 Lead, 60 Purchase (39 last week); the server side is Purchase only (31); 3 events from a local build. Purchase 28d: 196 (96 browser / 100 server) against 107 PMS online bookings; the larger side is 0.9x direct bookings, so no over-count. The HG AI CAPI is OFF and Guesty is the server sender. Decision 26 (purchase value) still open."),
 dict(client="Parker Reserve",pid="1188475652520634",name="Parker Reserve - Pixel",acct="1002927148609804",flag=W,exp="parkerreserve.com",src="inferred",
  notes="Week 9: parkerhouseohio.com 98 events (4.1%, up from 44), still unconfirmed. 2,377 events (+3%), half server, 3 Purchase. Purchase 28d: 8, all server (HG AI CAPI on, 11 sent), against 13 PMS online bookings (62%); no Sales budget ($10/day giveaway only). Next action (Kristal): confirm parkerhouseohio.com is a Parker property or remove the pixel from it."),
 dict(client="Ponderosa Pines Resort",pid="1293211539656211",name="Ponderosa Pines Resort - Meta Pixel",acct="1058846326445255",flag=M,exp="ponderosapinesresort.com + Newbook",src="inferred",
  notes="Clean on domains: site 17,896, bio 2,439, Wix static 1,714 (475 last week), Newbook 58; 22,386 events (+7%), half server, 419 Lead, 90 Purchase. Purchase 28d: 350 (232 browser / 118 server) against 131 PMS online bookings: the browser alone is 1.8x, and this week's 89 Purchase events sit against 34 online bookings, so the Newbook confirmation still fires Purchase more than once per booking; the HG AI CAPI (on, 14 sent) adds a server copy. Over-count in the Purchase check, week 3. A new $40/day MoF lookalike sales campaign (13 Nov) now optimises on this inflated signal. Next action (Anna): make the Newbook confirmation fire Purchase once per booking."),
 dict(client="Ponderosa Pines Resort",pid="1743173753375733",name="Ponderosa Pines Resort's Pixel",acct="1058846326445255",flag=W,exp="ponderosapinesresort.com",src="inferred",
  notes="Week 6: the client-owned pixel attached to the ad account still fires PageView only from www.ponderosapinesresort.com (4,903 events, browser only), so page views are double-counted with the HG pixel above. Next action (Anna): confirm which pixel the ads use and remove the other from the site (decision 33)."),
 dict(client="Raven Rock Mountain",pid="1359649962298380",name="Raven Rock Meta Pixel",acct="1065186195582056",flag=W,exp="ravenrockmountain.com | stayravenrockmountain.com",src="inferred",
  notes="Week 9: domains clean (site 1,114, info. 66, links. 52); 1,246 events (−9%), 1 Purchase, but the pixel is still NOT shared to ad account 1065186195582056 (the account lists zero pixels). Purchase 28d: 11, all server (HG AI CAPI on, 12 sent), against 10 PMS online bookings, so tracking is ready when ads restart. Client Not Live, $0/day. Next action (Anna): share the pixel to the account before any campaign relaunch."),
 dict(client="Red White & Blue Views",pid="1625871301864243",name="Red White & Blue - Meta Pixel",acct="1419930382946246",flag=M,exp="redwhiteandblueviews.com",src="inferred",
  notes="Clean on domains. 26,444 events (−15%): the book. booking-engine host carried 24,811, mostly custom gallery_interaction events in spikes (6,014 on 12 Nov); bio 1,025, the GHL sites host 101. Half server, 3 Purchase. Purchase 28d: 13, all server (HG AI CAPI on, 13 sent), against 14 PMS online bookings (93%); the booking engine fires no browser Purchase."),
 dict(client="Ridge & Falls",pid="1332286819018269",name="Ridge & Falls - Meta Pixel",acct="1313401330776046",flag=M,exp="ridgeandfalls.com",src="inferred",
  notes="Clean (site 2,392, GHL funnel 849, GHL sites host 72, 2 from an HG Netlify preview); 3,334 events (−14%), 43 Lead, 4 Purchase. Purchase 28d: 22, all server, against 12 PMS online bookings, 1.8x: the HG AI CAPI (on, 12 sent) and a second server sender (Guesty or Boom) both send each booking. Over-count in the Purchase check, week 3. Next action (Makenna / Leshan): keep one server sender for Ridge & Falls."),
 dict(client="Selah Place",pid="1235173718368839",name="Selah.Place Event Data",acct="1275283434220508",flag=M,exp="selah.place + Holiday Future",src="inferred",
  notes="Clean on domains. 144,223 events (+17%): the Holiday Future engine 118,750 (mostly gallery_interaction), reserve. 11,033, site 8,713, bio 2,686, Wix static 2,191, blackwalnut.selah.place 618 (down to 1 a day on 15 and 16 Nov). 52 Purchase in the week. Purchase 28d: 176 (39 browser / 137 server) against 54 PMS online bookings, server 2.5x (2.4x last week): the HG AI CAPI (on, 53 sent) and Hostaway's CAPI each send every booking with different event_ids. Over-count in the Purchase check, week 3; a new $20/day MoF lookalike (13 Nov) now optimises on it too. Next action (Alicia / Leshan): keep one server sender for Selah."),
 dict(client="Selah Place",pid="1786742402537824",name="Selah | Black Walnut",acct="1275283434220508",flag=W,exp="blackwalnut.selah.place",src="inferred",
  notes="Week 2: the client's 'Selah | Black Walnut' pixel fired 1,606 events (+14%) from blackwalnut.selah.place, 99 Lead, no Purchase since 7 Nov. Traffic fell from 200 to 400 events a day to 2 and 18 on 15 and 16 Nov, after the client's two Black Walnut campaigns dropped out of the live campaign list (spend check, 16 Nov). The subdomain still fires the main Selah Event Data pixel as well, so Black Walnut visits are counted on two pixels. Next action (Alicia): agree with the client whether the main Selah pixel should stay on blackwalnut.selah.place (shared retargeting) or come off it, before the Black Walnut campaigns restart."),
 dict(client="Selah Place",pid="3327546500757583",name="LinkTree",acct="1275283434220508",flag=W,exp="selah.place | linktr.ee",src="inferred",
  notes="Week 9: the second pixel is still installed on www.selah.place (3,125 of its 3,145 events), so page views are double-counted; 20 events from linktr.ee itself. Next action (Alicia): remove this pixel from the site, keep it on Linktree only."),
 dict(client="Starlight Haven - Hot Springs",pid="766226461367996",name="Starlight Haven Pixel - ResNexus",acct="901138032027913",flag=M,exp="visitstarlight.com + ResNexus",src="inferred",
  notes="Clean. One pixel shared by both Starlight accounts (this row: Hot Springs) and shared into Taberg's account, browser only as the sheet says. ResNexus 21,344, site 8,213, book. 2,890, GHL 656; 33,146 events (flat), 1,341 Lead, 75 Purchase (105 last week). Purchase 28d: 338, all browser (ResNexus confirmations); no PMS in the platform to compare."),
 dict(client="Starlight Haven - Weiss Lake",pid="766226461367996",name="Starlight Haven Pixel - ResNexus",acct="74756899",flag=M,exp="visitstarlight.com + ResNexus",src="inferred",
  notes="Clean. Same pixel as Hot Springs (this row: Weiss Lake); see that row for the figures."),
 dict(client="Stay on 30a",pid="1464927198465632",name="Stay on 30a - Meta Pixel",acct="25640434272252212",flag=M,exp="stayon30a.com | stayson30a.com",src="inferred",
  notes="Clean. 54,893 events (−7%), half server, 447 Lead, 15 Purchase. An HG Netlify preview sent 6 and the Guesty engine 4. Purchase 28d: 66, all server, against 64 PMS online bookings (103%); the HG AI CAPI is OFF, so Guesty's CAPI is the sender. links.stayson30a.com spelling still unconfirmed."),
 dict(client="Stay Saluda NC",pid="4250460185185664",name="Stay Saluda - Meta Pixel",acct="1863632561215857",flag=M,exp="staysaluda.com",src="inferred",
  notes="Clean on its own pixel. 22,549 events (+8%), 46% server, 580 Lead, 4 Purchase (11 last week). Purchase 28d: 26, all server, against 34 PMS online bookings (76%); the HG AI CAPI is OFF, so Guesty is the sender and the browser never fires Purchase. A new $20/day MoF lookalike sales campaign started on 13 Nov. The Saluda GHL hosts also fire the Inspired Retreats pixel (see that row)."),
 dict(client="Stay Southern Illinois",pid="1328561309169535",name="Southern Illinois Cabins - Meta Pixel",acct="1661949078036229",flag=M,exp="southernilcabins.com | staysouthernillinois.com | shawneeforestcabins.com | woodlandcabins.net | newvillagevacationhomes.com + OwnerRez",src="confirmed",
  notes="Fixed by confirmation: Shawal confirmed on 9 Nov that shawneeforestcabins.com (3,097) and woodlandcabins.net (2,020) are the client's own brands, so the 18% of events they send are expected. newvillagevacationhomes.com (19 events) is the one host still unconfirmed, negligible. 28,638 events (−10%), half server, 65 Lead, 26 Purchase. Purchase 28d: 146 (63 browser / 83 server) against 68 PMS online bookings, within the 1.5x line."),
 dict(client="Stay With Branch",pid="1107997340818783",name="Branch",acct="1269399754049770",flag=M,exp="staywithbranch.com | gostaywithbranch.com + Guesty",src="inferred",
  notes="Clean (site 611, Guesty booking engine 366, GHL subdomains 369); 1,348 events (−30%), 22 Lead, no server events because there was no booking to send. Purchase 28d: 1 against 2 PMS online bookings; no direct booking since 22 Oct and no Sales budget."),
 dict(client="StayLuxe",pid="4293491110916917",name="StayLuxe Meta Pixel",acct="25033578722931437",flag=M,exp="stayluxe.vacations | gostayluxevacations.com + Uplisting",src="inferred",
  notes="Clean (site 1,156, bio 512, Booked Directly engine 277). The API's event totals came back partial this week (257 events against 1,953 in the host and browser/server breakdowns, +12%), so the Events column undercounts this pixel; the host figures are the reliable ones. Half server. Purchase 28d: 1 (7 Nov) against 1 PMS online booking; low volume matches the $20/day budget."),
 dict(client="Sunapee Stays",pid="471248637966769",name="sunapeestays's Pixel",acct="651114096215889",flag=M,exp="sunapeestays.com",src="sheet",
  notes="Clean. 5,981 events (+4%), 29 Lead, 4 Purchase. Purchase 28d: 21, all server, against 24 PMS online bookings (88%; HG AI CAPI on, 25 sent). Budget cut from $50 to $30/day this week."),
 dict(client="Taberg Falls",pid="964214909847907",name="Taberg Falls - Meta Pixel",acct="827872700004659",flag=M,exp="tabergfalls.com",src="inferred",
  notes="Clean. 49,855 events (−11%), 40% server, 1,785 Lead, 6 Purchase; 6 events from a localhost build. Purchase 28d: 28, all server, against 33 PMS online bookings (85%); the HG AI CAPI is OFF, so Hostaway's CAPI is the sender. The account still lists five other clients' pixels (decision 13)."),
 dict(client="The Cohost Company",pid="638998632168952",name="The Cohost Company Meta Pixel",acct="9141035462679902",flag=M,exp="thecohostcompany.com | gocohostcompany.com",src="inferred",
  notes="Clean. 7,914 events (−3%), 85 Lead, 8 Purchase; the server side is Purchase only; three HG Netlify previews sent 8. Purchase 28d: 21, all server, against 33 PMS online bookings (64%); the HG AI CAPI is OFF, so Guesty is the sender."),
 dict(client="The Outpost",pid="1691591692267740",name="HG - The Outpost Grand Canyon Event Data",acct="1530849534802936",flag=W,exp="outpostgrandcanyon.com",src="inferred",
  notes="Week 9: the HiddenGem-managed pixel still receives only link-in-bio events (835; 85 Lead, half server). Site and booking engine fire the client-owned pixel below; the funnel is split. Decision 10 open. Next action (Anna): pick one pixel and install it on the site too."),
 dict(client="The Outpost",pid="734783866381382",name="Outpost Grand Canyon",acct="1530849534802936",flag=W,exp="outpostgrandcanyon.com + Newbook",src="inferred",
  notes="Week 9: the client-BM pixel carries the Newbook booking engine (2,159) and the site (425); 2,636 events (−13%), 3 Purchase, server side Purchase only. Purchase 28d: 18, all server (HG AI CAPI on, 24 sent), against 37 PMS online bookings (49%): the Newbook confirmation fires no browser Purchase and the platform only sends bookings with an email or phone that are under 7 days old when synced. The old 08/29 BoF campaign is gone this week; one $10/day BoF remains. See the row above."),
 dict(client="Three Suns Cabins",pid="691977289952800",name="Three Suns Cabins - Pixel",acct="1210218584137342",flag=W,exp="threesunscabins.com",src="inferred",
  notes="Week 9: still nothing from the main website, only the link-in-bio page (210); 216 events, 6 Purchase server-side. Purchase 28d: 22, all server (HG AI CAPI on, 25 sent), against 24 PMS online bookings, so the platform covers Purchases, but the pixel base code is still missing from threesunscabins.com. Next action (Anna): install the pixel on the site; confirm the domain."),
 dict(client="Treetop Escapes",pid="1178838797064774",name="Treetop Escapes - Pixel",acct="967636478877602",flag=M,exp="staytreetopescapes.com + Guesty",src="inferred",
  notes="Clean. 37,698 events (+1%), 45% server, 885 Lead, 19 Purchase; the Guesty engine 28, an HG Netlify preview 6. Pixel also shared into Taberg's account. Purchase 28d: 58 (10 browser / 48 server) against 44 PMS online bookings; the HG AI CAPI is OFF, so Guesty is the sender. A new $20/day MoF lookalike (13 Nov) lifts the Sales budget to $60/day."),
 dict(client="Tuxedo Falls",pid="1561325308991270",name="Tuxedo Falls - Ad Account's Pixel",acct="2077151009889326",flag=W,exp="tuxedofalls.com",src="inferred",
  notes="Week 9: ZERO events, silent since 1 Sep (11 weeks). The ad account's only attached pixel is empty while the real tracking runs on 'Website' 1839806973541001 below. Next action (Chiara): share the Website pixel to the ad account and retire this one (decision 18)."),
 dict(client="Tuxedo Falls",pid="1839806973541001",name="Website",acct="2077151009889326",flag=W,exp="tuxedofalls.com + ResNexus + GHL",src="inferred",
  notes="Week 8: live pixel carrying the site (13,918), ResNexus (5,638) and the GHL funnel (1,080 plus 32 on the GHL sites host); 20,738 events (+74%, a spike on 12 and 13 Nov), 10 Purchase, browser only, still NOT shared to ad account 2077151009889326. Purchase 28d: 27, all browser (ResNexus confirmations), no PMS in the platform. Decision 18."),
 dict(client="Walden Retreats",pid="505477285266646",name="Walden Retreat's Data",acct="973261794434226",flag=M,exp="waldenretreats.com + ResNexus",src="inferred",
  notes="Clean on domains: site 10,278, ResNexus 3,390, bio 1,162, the Spacecrafted site-builder host 24. The local build traffic is gone (982 events from 127.0.0.1 last week, none now); 12 from hiddengem.media remain. 15,023 events (−17%), 44% server, 180 Lead. Purchase jumped: 85 in the week (33 last week), 22 on 15 Nov and 42 by 08:30 PT on 16 Nov, while the ResNexus host ran at about 2.4x its usual daily volume, and server Purchases are back (32 in 7 days after two weeks with none). Purchase 28d: 239 (190 browser / 49 server); no PMS in the platform to check them against, and the BoF campaign dropped out of the live list this week. Next action (Anna): check ResNexus for the bookings made on 15 and 16 Nov; if there are far fewer than 60, the confirmation page is firing Purchase more than once."),
 dict(client="Dunya Camp",pid="702976282491817",name="Dunya Camp website",acct="629838998232110",flag=B,exp="dunyacamp.com",src="inferred",
  notes="First row (client map 16 Nov, not on the Master sheet; $3,594 spent in the 30 days to 16 Nov). The only Dunya pixel visible to the system user is 'Dunya Camp website' in the client's business (4863743860323428), shared into the HG BM, and it is dead: last fired 21 Jul 2025, zero events in 28 days. The ad account's own pixel list could not be read: Meta returned its per-account rate limit (code 80004) on two single calls to act_629838998232110/adspixels about five minutes apart, and the Dunya business lists no pixels to the system user. The campaigns optimise on custom 'Step 2' / 'Step 3' events, so a live pixel exists somewhere. Expected domain dunyacamp.com is guessed from the brand name, CONFIRM. Next action (Chiara): tell us which pixel the Dunya ad sets optimise on and share it with the HiddenGem BM; the next run reads the account again."),
 dict(client="Gooseberry Lodges",pid="3431371590511492",name="Gooseberry's Pixel",acct="701051796368186",flag=M,exp="gooseberrylodges.com + SiteMinder (direct-book.com)",src="inferred",
  notes="First row (live on Meta since 27 Oct, mapped 16 Nov). Clean: site 3,110, bio (GHL sign-up) 423, the SiteMinder engine direct-book.com 4, which fires Purchase only. 3,610 events, browser only (no CAPI), 55 Lead, 4 Purchase. Purchase 28d: 49, all browser, 1 to 4 a day since 19 Oct, so the booking confirmation fires; no PMS in the platform to check capture. The HG AI tenant has CAPI switched on with this pixel assigned but no PMS connection, so it sends nothing. Pixel sits in the client's business (2675419955948428), attached to the ad account."),
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
    _p=px.get(r["pid"],{}); _q=_p.get("purchase_28d",{})
    r["events_28d"]=_p.get("total_events_28d",0); r["p28"]=_q.get("total",0); r["p28_b"]=_q.get("browser",0); r["p28_s"]=_q.get("server",0)
    r["p7"]=_p.get("purchase_7d",{}).get("total",0); r["p_last"]=(_q.get("last") or "")[:10]
    _pm=PMS.get(r["client"]); r["pms_online28"]=_pm["online28_bk"] if _pm else None; r["pms_direct28"]=_pm["direct28_bk"] if _pm else None
    _c=CAPI.get(r["client"]); r["hgai_capi"]=(("on" if _c["capi_enabled"] else "OFF")+f", {_c['capi_sent_28d']} sent 28d") if _c else "no tenant"
    _s=SPEND.get(r["client"]); r["sales_budget"]=_f(_s["bof_sales"])+_f(_s["mof_sales_lol"]) if _s else 0.0; r["total_live"]=_f(_s["total_live"]) if _s else 0.0
    r["status"]=(SHEET.get(r["client"],{}).get("status") or "").strip() or "not on sheet"
    r["live"]=r["status"].lower().startswith("live") and r["total_live"]>0
    p=prev.get((r["pid"],r["client"])) or next((v for (pid,c),v in prev.items() if pid==r["pid"] and c.startswith(r["client"][:10])),None)
    if p is None: r["diff"],r["weeks"]="new",(1 if r["flag"] in FLAGGED else 0); continue
    pw=int(p.get("weeks_open") or 0)
    if p["flag"] in FLAGGED and r["flag"] in FLAGGED: r["diff"],r["weeks"]="still_open",pw+1
    elif p["flag"] in FLAGGED and r["flag"] not in FLAGGED: r["diff"],r["weeks"]="fixed",0
    elif p["flag"] not in FLAGGED and r["flag"] in FLAGGED: r["diff"],r["weeks"]="new",1
    else: r["diff"],r["weeks"]="unchanged",0
# Purchase check per client, judged on the pixel with the most Purchases (purchase_rules.py)
_byc=collections.defaultdict(list)
for r in ROWS: _byc[r["client"]].append(r)
for _c,_rs in _byc.items():
    _rs.sort(key=lambda r:(-r["p28"],-r["events_28d"])); _prim=_rs[0]
    for r in _rs[1:]: r["pflag"],r["pnote"]="see",f"judged on {_prim['pid']}"+(f"; also carries {r['p28']} Purchase, check for double counting" if r["p28"] and _prim["p28"] else "")
    _prim["pflag"],_n=judge(_prim); _prim["pnote"]="; ".join(_n)
    if _c in OFF_SHEET: _prim["pflag"],_prim["pnote"]="n/a",f"not on the Master sheet and not in this week's spend check (mapped after it ran); {_prim['p28']} Purchase in 28d, not judged"
PI={"ok":"✅","warning":"⚠️","critical":"❌","n/a":"n/a","see":"↳"}
def pcell(r): return f"{r['p28']:,} ({r['p28_b']}b / {r['p28_s']}s)" if r["p28"] else "0"
seen={(r["pid"],r["client"]) for r in ROWS}
removed=[v for k,v in prev.items() if k not in seen and not any(k[0]==r["pid"] and k[1].startswith(r["client"][:10]) for r in ROWS)]
ROWS.sort(key=lambda r:(r["client"],r["pid"]))
distinct={r["pid"] for r in ROWS if r["pid"]}
total_events=sum(px[p]["total_events"] for p in distinct if p in px)
counts=collections.Counter(r["flag"] for r in ROWS)
ICON={M:"✅",W:"⚠️",C:"❌",B:"🔴"}
fixed=[r for r in ROWS if r["diff"]=="fixed"]
new_flags=[r for r in ROWS if r["diff"]=="new" and r["flag"] in FLAGGED]

# ---------- md ----------
L=[]
L.append(f"# Meta Pixel Domain Check, {TODAY}\n")
L.append(f"**Date:** {TODAY} · **Clients on sheet:** {CLIENTS_ON_SHEET} + {len(OFF_SHEET)} off-sheet ({CLIENTS_ON_SHEET-len(OFFBOARDED_EXCLUDED)-len(NOT_CHECKED)+len(OFF_SHEET)} checked) · **Pixel rows reviewed:** {len(ROWS)} ({len(distinct)} distinct pixels) · **Receiving events correctly:** {counts[M]} ✅ · **Critical:** {counts[C]} ❌ · **Warnings:** {counts[W]} ⚠️ · **Blocked:** {counts[B]} 🔴 · **Total events, last 7 days:** {total_events:,}\n")
L.append(f"Ninth run (Monday). Compared against the {PREV[:10]} report. Read through the Meta Marketing API with the HG - ROI Dashboard system user (`scripts/pull-pixel-stats.mts`, {WINDOW}, window ending 08:33 PT): each pixel's 7-day host breakdown with per-day counts, event totals, browser/server split, and the 28-day Purchase split. New this week: Gooseberry Lodges (ad account mapped 16 Nov, live on Meta since 27 Oct) and Dunya Camp (added to the client map on 16 Nov; runs ads without a Master sheet row). Nine Pines Retreats (Not Live, no ad account) is still not checked; Canopy at Moody Moon Ridge is offboarded and not checked. Expected domains are still the inferred set from the first run except where the footer says otherwise. Checked against the actions log in PROJECT.md section 9 and this week's spend check.\n")
HDR="| Client | Pixel Name | Pixel ID | Events (last 7d) | Purchase (28d, browser / server) | Domains Seen | Expected Domain(s) | Match | Notes/Issues |\n|---|---|---|---|---|---|---|---|---|"
def trow(r): return f"| {r['client']} | {r['name']} | {r['pid']} | {r['events']:,} | {pcell(r)} | {', '.join(r['hosts']) if r['hosts'] else 'none'} | {r['exp']} | {ICON[r['flag']]} | {r['notes']} |"
L.append("## Critical issues (❌ and 🔴)\n")
crit=[r for r in ROWS if r["flag"] in (C,B)]
if crit:
    if any(r["flag"]==B and r["client"]=="Dunya Camp" for r in crit): L.append("**Dunya Camp, new to the checks, has no readable live pixel yet.**\n")
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
L.append("**What moved this week.** Closed: the Stay Saluda → Inspired Retreats cross-contamination, which Shawal blocked on the pixel (16 Nov) and withdrew from this and the previous two reports. Fixed: Stay Southern Illinois, after Shawal confirmed shawneeforestcabins.com and woodlandcabins.net as the client's own brands (9 Nov). New rows: Gooseberry Lodges (clean, browser only) and Dunya Camp (see its row). Closed too: Best Texas Travel's River Road Cabins hosts (65% of its events), which Shawal confirmed as the client's own brand (16 Nov). Selah's Black Walnut traffic fell to almost nothing on 15 Nov when the client's Black Walnut campaigns stopped; the double-pixel setup is unchanged. On the Purchase side: Away2PA crossed the over-count line (server Purchases 1.6x bookings); Little River Landing moves from ❌ to ⚠️ on one more Purchase, with nothing fixed; Walden's Purchases jumped to 85 (42 by mid-morning on 16 Nov) with no PMS to check them against; Cabin Collective's HG AI CAPI sent its first Purchases on 16 Nov. Everything else in this table is carried over unchanged.\n")
L.append("**Removed:** none.\n")
L.append(HDR)
for r in nw+cw: L.append(trow(r))
L.append("")
L.append("## Fixed since last week\n")
if fixed:
    L.append(HDR)
    for r in fixed: L.append(trow(r))
else:
    L.append("None.")
L.append("")
L.append("## Purchase check (last 28 days)\n")
_prims=[r for r in ROWS if r["pflag"] in ("ok","warning","critical","n/a")]
_pc=collections.Counter(r["pflag"] for r in _prims)
L.append(f"Judged per client on the pixel with the most Purchase events, against the PMS bookings of the same 28 days (HiddenGem AI platform; 'online' excludes manual, owner, phone and walk-in entries) and the client's Sales budget. {_pc['ok']} ✅ · {_pc['warning']} ⚠️ · {_pc['critical']} ❌ · {_pc['n/a']} n/a. Rules in `purchase_rules.py`; the HG AI CAPI column is the platform's own Conversions API toggle and ledger count, so server Purchases above it come from another sender.\n")
PH="| Client | Pixel ID | Purchase 28d (browser / server) | Purchase 7d | Last Purchase | PMS online bookings 28d | Capture | Sales $/day | HG AI CAPI | Flag | Why |\n|---|---|---|---|---|---|---|---|---|---|---|"
def _cap(r):
    if r["pms_online28"] is None: return "no PMS"
    if r["pms_online28"]==0: return "0 bookings"
    return f"{r['p28']}/{r['pms_online28']} = {r['p28']/r['pms_online28']:.0%}"
def prow(r): return f"| {r['client']} | {r['pid']} | {pcell(r)} | {r['p7']} | {r['p_last'] or '—'} | {r['pms_online28'] if r['pms_online28'] is not None else '—'} | {_cap(r)} | ${r['sales_budget']:.0f} | {r['hgai_capi']} | {PI[r['pflag']]} | {r['pnote']} |"
_flagged=[r for r in _prims if r["pflag"] in ("critical","warning")]
_flagged.sort(key=lambda r:(0 if r["pflag"]=="critical" else 1, r["client"]))
if _flagged:
    L.append(PH)
    for r in _flagged: L.append(prow(r))
else: L.append("No client flagged.")
L.append("")
L.append("## All pixels (alphabetical by client)\n")
L.append(HDR)
for r in ROWS: L.append(trow(r))
L.append("")
silent=[r for r in ROWS if r["events"]==0 and r["flag"]!=B]
notsheet=[p for p in pull["pixels"] if not p.get("skipped") and p["id"] not in distinct and p["id"]!="861460105842405"]
L.append("## Footer\n")
L.append(f"- Clients on sheet: {CLIENTS_ON_SHEET} ({CLIENTS_ON_SHEET-NOT_LIVE-1} Live, {NOT_LIVE} Not Live, 1 offboarded and excluded: {', '.join(OFFBOARDED_EXCLUDED)}), plus {', '.join(OFF_SHEET)}, which runs ads without a Master sheet row and joined the client map on 16 Nov (Shawal). Big Moon Ranch is offboarded too but still on the sheet, so it keeps its row. Pixel rows: {len(ROWS)} ({len(distinct)} distinct pixels; Starlight Haven's pixel serves both accounts, Columbia Gorge, Green Springs, North Star, Ponderosa, The Outpost and Tuxedo Falls have two rows each; Selah Place has three: the Event Data pixel, LinkTree and the client's Black Walnut pixel). Not checked: Nine Pines Retreats, on the sheet with no ad account and no ads yet. Arca Boutique Hotel: mapped 16 Nov (ad account 1003623765640520), no pixel attached, no ads yet; not on the Master sheet, so no row.")
L.append(f"- Pixels found: {len(distinct)}. With events: {len([p for p in distinct if events_of(p)>0])}. Silent: {len(silent)} ({', '.join(r['name'] for r in silent)}). Blocked: {counts[B]}.")
L.append(f"- Total events across all pixels, {WINDOW}: {total_events:,} (each shared pixel counted once, from the API's event totals, comparable with last week's 960,152). StayLuxe's event totals came back partial this week (257 against 1,953 in its host breakdown), so this total undercounts by about 1,700.")
L.append("- Server events column: Y = at least one server (CAPI) event inside the 7-day window; the notes give the share. Browser-only by design per the sheet: Starlight Haven, The Outpost (client pixel), Columbia Gorge Getaways (CGG Pixel), Ponderosa's second pixel. From this week a server side that carries Purchase only is treated as a working Purchase-only CAPI (HG AI platform, Hostaway, Guesty, OwnerRez), not as silent; the HG AI CAPI column in the Purchase check says whether the platform is the sender. Sheet says CAPI but nothing reaches the pixel server-side: Asheville River Cabins (0), week 9.")
L.append(f"- Ad accounts listed through the API: {len(pull['clients'])} client accounts in the pull, 0 listing errors, 0 read errors. "+DUNYA_ACCT_NOTE+" Raven Rock Mountain still has zero pixels attached. Táberg Falls' account still lists five other clients' pixels. Nine Pines Retreats has no account in the client map (no ads yet). Attached pixels that never fired in the window (Event Data, test and retired pixels) are listed in the notes where relevant.")
L.append("- Pixels in the HG BM that belong to no sheet client and fired in the last 28 days: "+", ".join(sorted(f"{p['name']} ({p['total_events']:,})" for p in notsheet if p['total_events']>0))+". Hillside Amble, Cowan Creek, Edenwood and Stay Different run ads without a Master sheet row (section 5 note); a 'Wix Pixel' in Selah's business fired once from www.selah.place. Never fired or dead: "+", ".join(sorted(p['name'] for p in notsheet if p['total_events']==0))+".")
L.append(f"- Previous report compared against: {PREV}. Diff joined on pixel ID. Rows removed since last week: "+("; ".join(f"{v['client']} ({v['pixel_id']}, was {v['flag']})" for v in removed) if removed else "none")+".")
L.append("- Expected domains: every row is still `inferred` from the brand name plus observed traffic (first run), except Sunapee Stays (`sheet`) and Stay Southern Illinois (`confirmed` 9 Nov; newvillagevacationhomes.com, about 20 events a week, is still unconfirmed). Inferred domains that contain the client's brand name are treated as confirmed; the ⚠️ for inference applies only where it does not (parkerhouseohio.com, links.stayson30a.com). New inferred rows this week: Gooseberry Lodges and Dunya Camp. Confirm with Shawal and flip `source` to `confirmed` in `expected-domains.csv`.")
L.append("- Data path from this week: the claude.ai Meta connector is not used; `pixel_pull.json` in the skill folder is the whole Meta read (listings, hosts per hour, event totals, browser/server split). EMQ is not pulled on this path.")
open(os.path.join(OUT,f"{TODAY}-pixel-domain-check.md"),"w",encoding="utf-8").write("\n".join(L)+"\n")
with open(os.path.join(OUT,f"{TODAY}-pixel-domain-check.csv"),"w",newline="",encoding="utf-8") as fh:
    w=csv.writer(fh); w.writerow("run_date,client,pixel_id,pixel_name,ad_account_id,events_7d,server_events,domains_seen,expected_domains,expected_source,flag,diff_status,weeks_open,notes,events_28d,purchase_28d,purchase_28d_browser,purchase_28d_server,purchase_7d,purchase_last,pms_online_bookings_28d,pms_direct_bookings_28d,sales_budget_per_day,hgai_capi,purchase_flag,purchase_note".split(","))
    for r in ROWS:
        w.writerow([TODAY,r["client"],r["pid"],r["name"],r["acct"],r["events"],r["server"],"|".join(r["hosts"]),r["exp"].replace(" | ","|"),r["src"],r["flag"],r["diff"],r["weeks"],r["notes"],
                    r["events_28d"],r["p28"],r["p28_b"],r["p28_s"],r["p7"],r["p_last"],r["pms_online28"] if r["pms_online28"] is not None else "",r["pms_direct28"] if r["pms_direct28"] is not None else "",f"{r['sales_budget']:.0f}",r["hgai_capi"],r["pflag"],r["pnote"]])
print("rows",len(ROWS),"distinct",len(distinct),"counts",dict(counts),"total",total_events,"removed",[(v['client']) for v in removed])
print("diff",collections.Counter(r["diff"] for r in ROWS))
print("purchase",dict(_pc))
