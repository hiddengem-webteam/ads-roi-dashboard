"""Writes the dated pixel domain check .md and .csv from pixel_pull.json.

The per-pixel flags, expected domains and notes are authored by Claude in
ROWS below each week (the judgement part of the audit); events, hosts,
browser/server split and the week-over-week diff are computed here.
"""
import json, csv, os, glob, datetime, collections
SP=os.path.dirname(os.path.abspath(__file__))
ROOT=os.path.abspath(os.path.join(SP,"..","..",".."))
OUT=os.path.join(ROOT,"weekly","Meta Pixel Reviews","Weekly Checks")
TODAY="2026-11-09"
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
CLIENTS_ON_SHEET=47; NOT_LIVE=3; OFFBOARDED_EXCLUDED=["Canopy at Moody Moon Ridge"]
NOT_CHECKED=["Gooseberry Lodges","Nine Pines Retreats"]  # on the sheet, no ad account, no ads running yet (Shawal, 2026-11-09)
WINDOW="2 Nov to 9 Nov"

M,W,C,B="match","warning","critical","blocker"
ROWS=[
 dict(client="American River Resort",pid="2862601447415133",name="American River Resort - Meta Pixel",acct="953162737054331",flag=M,exp="americanriverresort.com",src="inferred",
  notes="Clean. Ads off since 15 Oct (paused, not offboarded). 5,123 events (−12%), half server, no Lead or Purchase; the site still fires and the GHL funnel sent 4 events."),
 dict(client="Asheville River Cabins",pid="1634367080775220",name="Asheville River Cabins Meta Pixel",acct="615836588009747",flag=W,exp="ashevillerivercabins.com + Cloudbeds",src="inferred",
  notes="Week 8: domains clean (Cloudbeds booking engine 14,104, site 7,708, GHL 590, bio 483); 23,025 events (−19%), 191 Lead, 76 Purchase in the week. Still 0 server events while the sheet says 'CAPI Setup (HG Ai)': the HG AI CAPI has never sent for this tenant (no PMS connection; Cloudbeds API access is with Leshan), so all 241 Purchases in 28 days are browser-side. Dustin raised the BoF budget from $30 to $50/day on 8 Nov. Next action (Charlotte / Leshan): get the Cloudbeds API access so the HG AI CAPI can send, and correct the sheet until it does."),
 dict(client="Away2PA",pid="772693422494226",name="Away 2PA Meta Pixel",acct="603977626130795",flag=M,exp="away2pa.com | awaytopa.com",src="inferred",
  notes="Clean on domains. 73,187 events (+211%): from 3 Nov away2pa.com went from about 1,200 to between 6,000 and 16,700 events a day and bio.awaytopa.com from about 130 to 1,000 to 3,100, with Lead up from 288 to 1,003 on an unchanged $40/day, so it reads as real traffic (an email or organic push), not a loop; worth asking Alicia what drove it. Half server, 32 Purchase; 8 events from the GHL API host. Purchase 28d: 76 (20 browser / 56 server) against 39 PMS online bookings: server is 1.44x bookings, just under the 1.5x over-count line, because the HG AI CAPI (on, 40 sent) and OwnerRez both send without a shared event_id."),
 dict(client="Awayframes",pid="773898245792839",name="Awayframes - Meta Pixel",acct="2471256056603833",flag=M,exp="awayframes.com",src="inferred",
  notes="Clean. 17,953 events (−1%), first full week at $200/day: 628 Lead, 5 Purchase, 40% server. Last week's book.awayframes.com burst is gone (159 events); the Netlify preview (7) is HG dev. Purchase 28d: 27, all server, against 23 PMS online bookings. The HG AI CAPI toggle is OFF and its ledger sent nothing in the last 7 days (13 in 28), so Hostaway's CAPI is now the only sender, which settles last week's one-sender question by default (Alicia / Leshan to confirm that was intended)."),
 dict(client="Best Texas Travel",pid="4108409325970216",name="Best Texas - Meta Pixel",acct="1982551189319458",flag=W,exp="besttexastravel.com + Holiday Future",src="inferred",
  notes="Week 3, share up: River Road Cabins hosts fired this pixel every day, bookings.riverroadcabins.com 12,018, riverroadcabins.com 1,914 and riverroadcabins.holidayfuture.com 727, together 14,659 or 40% of 36,191 events (33% last week). River Road Cabins is not a HiddenGem client and runs the same Holiday Future booking engine, so it still looks like a sister property of the same owner, unconfirmed. Own domains clean (book. 19,468, site 1,230, bio 631); 86 Lead, 7 Purchase, half server. Purchase 28d: 22, all server, against 27 PMS online bookings (81%); HG AI CAPI on, 27 sent. Next action (Nicole): confirm River Road Cabins belongs to the client and whether its visitors should feed Best Texas Travel's audiences; if not, remove the pixel from riverroadcabins.com and its booking engine."),
 dict(client="Big Moon Ranch",pid="1208874174466414",name="Big Moon Ranch - Meta Pixel",acct="758851247064974",flag=W,exp="bigmoonranch.com | staybigmoonranch.com",src="inferred",
  notes="Week 6: client offboarded 28 Sep, but the HG BM pixel is still on bigmoonranch.com: 5,230 events (−9%), 51% server, so a CAPI connection is still sending too. Still on the Master sheet. Next action (Charlotte): remove the pixel from the site, disconnect the CAPI connection, and take the row off the sheet (decision 25)."),
 dict(client="Bison Ridge Retreat",pid="1241959234316508",name="Bison Ridge - Meta Pixel",acct="950241787963535",flag=M,exp="bisonridgeretreat.com",src="inferred",
  notes="Clean. 5,029 events (+12%), 72 Lead, no Purchase. The server side is back at 49% after a week at zero, so last week's stop was temporary. No Purchase in 28 days with $5/day on BoF and no PMS in the platform to compare: the booking confirmation carries no Purchase event (Chiara). Event Data pixel 1617239586052069 still attached and dead."),
 dict(client="Cabin Collective",pid="1654110122884436",name="Cabin Collective BB Meta Pixel (New)",acct="2194562394139883",flag=M,exp="cabincollectivebb.com + OwnerRez",src="inferred",
  notes="Clean, third week. 11,527 events (−2%), half server, 204 Lead, 14 Purchase; site 9,276, the HG landing page on Netlify 1,020, OwnerRez 898, bio 254, Bluehost staging 28. Purchase 28d: 57 (34 browser / 23 server) against 32 PMS online bookings; the server side is OwnerRez, because the HG AI tenant still has no pixel assigned. The old 'Cabin Collective BB Pixel' 1338006181525466 is still attached, dead since 15 Oct. Sheet Status still reads Not Live with $30/day running since 20 Oct, which keeps the Purchase check at n/a. Next action (Chiara): set the sheet row to Live, assign the pixel in HG AI, and detach the dead pixel."),
 dict(client="Columbia Gorge Getaways",pid="595257656540749",name="CGG Pixel",acct="490940113157881",flag=W,exp="columbiagorgegetaways.com | columbiagorgeglamping.com",src="inferred",
  notes="Week 8: unchanged. Fires only from the Wix static host (525) and the GHL funnel go.columbiagorgeglamping.com (274), never from the main site, browser only; 6 Lead. Two live pixels on one client. Next action (Chiara): put the primary pixel on the GHL funnel pages and retire this one, or record it as the funnel pixel."),
 dict(client="Columbia Gorge Getaways",pid="700947282709400",name="Columbia Gorge Getaways Pixel",acct="490940113157881",flag=M,exp="columbiagorgegetaways.com + ResNexus",src="inferred",
  notes="Clean. Main site 5,291 and the ResNexus engine 2,039; 7,461 events (+7%), half server. Purchases are coming back: 8 this week after 2 the week before. The 28-day count fell to 18 (9 browser / 9 server) as the early-October burst left the window. No PMS in the platform to compare. 4 events from a Wix Google-reviews widget host are harmless."),
 dict(client="Endless Stays",pid="876508505381758",name="Endless Stays Meta Pixel",acct="896372356081479",flag=M,exp="stayendless.com + Hospitable",src="inferred",
  notes="Clean on domains. 63,120 events (+100%), but almost all of the rise is one PageView spike on 7 Nov (stayendless.com 20,167 that day against 3,000 to 5,500 on the others, bio. 3,063) with Lead flat at 718 (775 last week) on an unchanged $200/day: a one-day traffic burst or a bot, not a tracking change. Half server, 6 Purchase. Purchase 28d: 13, all server, against 16 PMS online bookings (81%); the HG AI CAPI (on, 16 sent) is the only Purchase sender and the booking confirmation fires no browser Purchase."),
 dict(client="Evergreen Cabins",pid="1474685406530880",name="Evergreen Cabins Meta Pixel",acct="453808647114273",flag=M,exp="evergreencabins.co + Hospitable",src="inferred",
  notes="Clean. 34,053 events (+14%), 28% server, 78 Lead, 10 Purchase; 22 from the GHL API host. Purchase 28d: 40, all server, against 38 PMS online bookings (HG AI CAPI on, 40 sent); the browser never fires Purchase."),
 dict(client="FLOHOM",pid="139231105894533",name="FLO2 Conversion",acct="2100710320122219",flag=M,exp="flohom.com | goflohom.com",src="inferred",
  notes="Clean. 24,935 events (−21%), 208 Lead, 12 Purchase. book.flohom.com is back at 900 to 1,950 events a day (8,720 in the week) after last week's drop to about 350 a day, so the booking-engine pixel is fine. Purchase 28d: 87 (11 browser / 76 server) against 88 PMS online bookings (99%); the HG AI CAPI is OFF and Hostaway's CAPI is the sender."),
 dict(client="Glasscombe",pid="1369498611461163",name="Aero Camp Pixel",acct="2030318804465316",flag=M,exp="glasscombe.com + Cloudbeds",src="inferred",
  notes="Clean. 13,352 events (−1%), 39% server, 346 Lead, 20 Purchase in the week (4 last week). Purchase 28d: 30 (9 browser / 21 server) against 20 PMS online bookings; the server side is the HG AI CAPI (on, 15 sent) plus Cloudbeds, within the over-count line. Pixel still named 'Aero Camp Pixel'; cosmetic."),
 dict(client="Green Springs Inn",pid="1602971745164199",name="Green Springs Inn Event Data",acct="1390516335151357",flag=W,exp="greenspringsinn.com + Holiday Future",src="inferred",
  notes="Week 8: unchanged. Receives booking-engine events only (book.greenspringsinn.com, 29,235), the same host that fires the Wix pixel, so bookings are counted on both pixels; 53 Purchase here this week. Purchase 28d: 188 (94 browser / 94 server) against 89 PMS online bookings, about 2.1x. Next action (Alicia): remove the booking-engine snippet from one pixel (decision 11)."),
 dict(client="Green Springs Inn",pid="1098954801239133",name="GSI - Wix Pixel",acct="1390516335151357",flag=M,exp="greenspringsinn.com | staygreenspringsinn.com + Holiday Future",src="inferred",
  notes="Clean on its own: booking engine 28,908, site 11,192, GHL subdomains; 41,737 events (−8%), half server, 173 Lead, 27 Purchase. The HG GSI site build on Cloudflare Pages still carries the live pixel (44 events from pages.dev previews); drop it from preview builds before launch (Leshan). Purchase 28d: 79, all server (HG AI CAPI on, 90 sent), against 89 PMS online bookings. See the Event Data row for the double count."),
 dict(client="Hiawassee Glamping",pid="1149628220675980",name="Hiawassee Meta Pixel",acct="4219624811692502",flag=M,exp="hiawasseeglamping.com",src="inferred",
  notes="Clean. 11,387 events (+5%), half server, 136 Lead, 1 Purchase. Purchase 28d: 14, all server, against 12 PMS online bookings (HG AI CAPI on, 15 sent). Only 1 PMS booking in the last 7 days, and month-to-date direct revenue is $810 against $12,407 at the same point in October; worth a word with the client (Alicia)."),
 dict(client="Home Base",pid="1467511861488785",name="Home Base Bnb - Meta Pixel",acct="3224125791099903",flag=M,exp="homebasebnbs.com | stayhomebase.com + Guesty",src="inferred",
  notes="Clean. 7,227 events (+7%), half server, 39 Lead, 34 Purchase. Purchase 28d: 189, all server, against 39 online and 187 direct PMS bookings: the HG AI CAPI (on, 123 sent) sends every direct booking, owner and manual entries included, so the BoF campaign optimises partly on bookings no ad could have driven. Within the over-count rule, which is judged on direct bookings."),
 dict(client="Inspired Retreats",pid="1547510566197386",name="Inspired Retreats Meta Pixel",acct="1494841894957652",flag=C,exp="stayinspiredretreats.com",src="inferred",
  notes="CROSS-CONTAMINATION, week 8, NOT fixed: go.staysaluda.com (571), links.staysaluda.com (204) and bio.staysaluda.com (193) fired this pixel on every day of the window, 968 events or 20% of 4,825, the same share as the previous seven weeks. Half of the pixel's events arrive server-side. Saluda's own pixel is clean, so the leak is one-way. No Purchase in 28 days against 5 PMS online bookings with $5/day on BoF, and the HG AI CAPI is OFF for the tenant. Next action (Shawal / Leshan): the page-snippet and GHL pixel-events paths are ruled out, so check the HG AI CAPI connector for Stay Saluda and the GHL sub-account's Facebook Conversions API integration for which pixel ID each sends to; one of them carries 1547510566197386."),
 dict(client="Little River Landing",pid="1816709606431185",name="Little River Landing Meta Pixel",acct="884285717873613",flag=M,exp="staylittleriver.com",src="inferred",
  notes="Clean on domains, sixth clean week: site 1,702, GHL funnel 613; 2,318 events (−6%), 48% server, 64 Lead, 1 Purchase. Purchase 28d: 4, all server, against 13 PMS online bookings with $15/day on BoF, still ❌ and unchanged: the HG AI CAPI is OFF (one send ever, 30 Sep), the browser never fires Purchase, and the few server Purchases come from Guesty. Next action (Makenna / Leshan): turn the HG AI CAPI on for the tenant or get the Guesty booking engine to fire Purchase in the browser."),
 dict(client="Myrinn",pid="1943632852972363",name="Myrinn - Meta Pixel",acct="1668286333836716",flag=M,exp="staywithmyrinn.com",src="inferred",
  notes="Clean. 3,338 events (−24%), half server, 48 Lead, 1 Purchase. Purchase 28d: 4, all server, against 4 PMS online bookings (HG AI CAPI on, 4 sent)."),
 dict(client="Nature Nooks",pid="844302611320158",name="Nature Nooks - Meta Pixel",acct="1796752774213285",flag=M,exp="naturenooksacadia.com",src="inferred",
  notes="Clean. 1,182 events (−55%) after Kristal paused all three campaigns on 4 Nov (account now $0/day). No Purchase; the Purchase check is n/a while ads are off."),
 dict(client="North Star Resort & Lodge",pid="3440147309499983",name="North Star Lodge Killington - Meta Pixel",acct="2003562593933799",flag=W,exp="northstarkillington.com + GHL + Cloudbeds",src="inferred",
  notes="Week 8, slightly better: site 1,465, GHL funnel 310, and the Cloudbeds engine fired 9 events on five days (1 last week), so a few booking pages carry the pixel again but most still do not. 1,833 events (+119%), 31 Lead, 9 Purchase, all server. Correction to last week: the HG AI CAPI is sending (26 Purchase in 28 days, 9 in the last 7); its last_sent field still reads 3 Oct but the ledger is current. Purchase 28d: 26 against 84 PMS online bookings (31%), but 34 of those are 'Default Corporate Client' and 22 'RCI' bookings that most likely never pass a page with the pixel; against the 25 'Website/Booking Engine' bookings the server Purchases match about one for one. Next action (Charlotte / Leshan): reinstall the account pixel in the Cloudbeds engine so the browser Purchase fires again; decision 9 still open."),
 dict(client="North Star Resort & Lodge",pid="1904436107168032",name="Northstar Meta Pixel",acct="2003562593933799",flag=W,exp="northstarkillington.com + Cloudbeds",src="inferred",
  notes="Week 8: dead. Zero events this week, last fired 26 Oct; it carried browser Purchases from the Cloudbeds engine until 19 Oct and nothing since. Not attached to the ad account. Next action (Charlotte): once the account pixel above is the one installed in Cloudbeds, retire this one and close decision 9."),
 dict(client="Oak & Ember",pid="1729106025177871",name="Oak & Ember - Meta Pixel",acct="831762063342909",flag=M,exp="stayoakandember.com + Hospitable",src="inferred",
  notes="Clean. 21,825 events (+11%), half server, 70 Lead; GHL funnel 3,969, Hospitable 26. No Purchase in 28 days with $5/day on BoF and a Hospitable PMS the platform cannot read, so capture cannot be judged; the booking confirmation fires no Purchase event either way (Chiara). Event Data pixel still dead."),
 dict(client="Paradise Pointe",pid="707016175006193",name="Paradise Pointe - Pixel",acct="1585826092078255",flag=M,exp="stayparadisepointe.com",src="inferred",
  notes="Clean. 32,191 events (flat), 265 Lead, 39 Purchase; the server side is Purchase only (20). Purchase 28d: 207 (116 browser / 91 server) against 101 PMS online bookings; browser is 1.15x bookings, down from 1.48x last week as the early-October reload burst left the window. The HG AI CAPI is OFF and Guesty is the server sender. Decision 26 (purchase value) still open."),
 dict(client="Parker Reserve",pid="1188475652520634",name="Parker Reserve - Pixel",acct="1002927148609804",flag=W,exp="parkerreserve.com",src="inferred",
  notes="Week 8: parkerhouseohio.com 44 events (1.9%), still unconfirmed. 2,308 events (−19%), half server, 3 Purchase. Purchase 28d: 5, all server (HG AI CAPI on, 8 sent), against 10 PMS online bookings; no Sales budget ($10/day giveaway only). Next action (Kristal): confirm parkerhouseohio.com is a Parker property or remove the pixel from it."),
 dict(client="Ponderosa Pines Resort",pid="1293211539656211",name="Ponderosa Pines Resort - Meta Pixel",acct="1058846326445255",flag=M,exp="ponderosapinesresort.com + Newbook",src="inferred",
  notes="Clean on domains: site 17,190, bio 2,945, Wix static 481, Newbook 72; 20,872 events (−1%), 51% server, 437 Lead, 115 Purchase. Purchase 28d: 327 (218 browser / 109 server) against 129 PMS online bookings: the browser alone is 1.69x, and this week's 115 Purchase events sit against 44 online bookings, so the Newbook confirmation still fires Purchase more than once per booking; the HG AI CAPI (on, 10 sent) adds a server copy. Over-count in the Purchase check, week 2. Next action (Anna): make the Newbook confirmation fire Purchase once per booking."),
 dict(client="Ponderosa Pines Resort",pid="1743173753375733",name="Ponderosa Pines Resort's Pixel",acct="1058846326445255",flag=W,exp="ponderosapinesresort.com",src="inferred",
  notes="Week 5: the client-owned pixel attached to the ad account still fires PageView only from www.ponderosapinesresort.com (4,761 events, browser only), so page views are double-counted with the HG pixel above. Next action (Anna): confirm which pixel the ads use and remove the other from the site (decision 33)."),
 dict(client="Raven Rock Mountain",pid="1359649962298380",name="Raven Rock Meta Pixel",acct="1065186195582056",flag=W,exp="ravenrockmountain.com | stayravenrockmountain.com",src="inferred",
  notes="Week 8: domains clean (site 1,301, info. 53, links. 17); 1,375 events (−45%), 2 Purchase, but the pixel is still NOT shared to ad account 1065186195582056 (the account lists zero pixels). Purchase 28d: 17, all server (HG AI CAPI on, 18 sent), against 15 PMS online bookings, so tracking is ready when ads restart. Client Not Live, $0/day. Next action (Anna): share the pixel to the account before any campaign relaunch."),
 dict(client="Red White & Blue Views",pid="1625871301864243",name="Red White & Blue - Meta Pixel",acct="1419930382946246",flag=M,exp="redwhiteandblueviews.com",src="inferred",
  notes="Clean on domains. 31,258 events (+33%): the book. booking-engine host carried 29,405, mostly custom gallery_interaction events, again in spikes (12,333 on 4 Nov against 700 to 5,200 on other days); the GHL sites host sent 127. Half server, 108 Lead, 5 Purchase. Purchase 28d: 9, all server (HG AI CAPI on, 12 sent), against 13 PMS online bookings (69%); the booking engine fires no browser Purchase."),
 dict(client="Ridge & Falls",pid="1332286819018269",name="Ridge & Falls - Meta Pixel",acct="1313401330776046",flag=M,exp="ridgeandfalls.com",src="inferred",
  notes="Clean (site 2,708, GHL funnel 1,052, GHL sites host 92); 3,879 events (+7%), 60 Lead, 7 Purchase. Purchase 28d: 25, all server, against 14 PMS online bookings, 1.79x: the HG AI CAPI (on, 14 sent) and a second server sender (Guesty or Boom) both send each booking. Over-count in the Purchase check, week 2. Next action (Makenna / Leshan): keep one server sender for Ridge & Falls."),
 dict(client="Selah Place",pid="1235173718368839",name="Selah.Place Event Data",acct="1275283434220508",flag=M,exp="selah.place + Holiday Future",src="inferred",
  notes="Clean on domains. 122,914 events (+17%): the Holiday Future engine 101,308 (mostly gallery_interaction), reserve. 8,398, site 8,300, Wix static 2,162, bio 2,098, and from 6 Nov blackwalnut.selah.place (324), the new Black Walnut property page, which also fires the new client pixel below. 955 Lead, 51 Purchase. Purchase 28d: 136 (29 browser / 107 server) against 45 PMS online bookings, server 2.4x: the HG AI CAPI (on, 47 sent) and Hostaway's CAPI each send every booking with different event_ids. Over-count in the Purchase check, week 2. Next action (Alicia / Leshan): keep one server sender for Selah."),
 dict(client="Selah Place",pid="1786742402537824",name="Selah | Black Walnut",acct="1275283434220508",flag=W,exp="blackwalnut.selah.place",src="inferred",
  notes="New this week, set up by the client: 'Selah | Black Walnut' sits in Selah's own business, is shared with HiddenGem and attached to the ad account. It fires from blackwalnut.selah.place since 6 Nov (1,263) plus 12 events from 127.0.0.1 on 5 Nov (the client's build); 1,404 events, 60% server, 42 Lead, 5 Purchase, 196 OfferView. All seven ad sets of the client's two new Black Walnut campaigns (created by Nathan Herrington on 5 and 7 Nov) optimise on this pixel, Lead and Purchase. The same subdomain also fires the main Selah Event Data pixel (324 events), so Black Walnut visits are counted on two pixels. Next action (Alicia): agree with the client whether the main Selah pixel should stay on blackwalnut.selah.place (shared retargeting) or come off it."),
 dict(client="Selah Place",pid="3327546500757583",name="LinkTree",acct="1275283434220508",flag=W,exp="selah.place | linktr.ee",src="inferred",
  notes="Week 8: the second pixel is still installed on www.selah.place (2,901 of its 2,928 events), so page views are double-counted; 21 events from linktr.ee itself. Next action (Alicia): remove this pixel from the site, keep it on Linktree only."),
 dict(client="Starlight Haven - Hot Springs",pid="766226461367996",name="Starlight Haven Pixel - ResNexus",acct="901138032027913",flag=M,exp="visitstarlight.com + ResNexus",src="inferred",
  notes="Clean. One pixel shared by both Starlight accounts (this row: Hot Springs) and shared into Taberg's account, browser only as the sheet says. ResNexus 20,943, site 8,311, book. 2,769, GHL 852; 33,160 events (+5%), 1,348 Lead, 105 Purchase. Purchase 28d: 346, all browser (ResNexus confirmations); no PMS in the platform to compare."),
 dict(client="Starlight Haven - Weiss Lake",pid="766226461367996",name="Starlight Haven Pixel - ResNexus",acct="74756899",flag=M,exp="visitstarlight.com + ResNexus",src="inferred",
  notes="Clean. Same pixel as Hot Springs (this row: Weiss Lake); see that row for the figures."),
 dict(client="Stay on 30a",pid="1464927198465632",name="Stay on 30a - Meta Pixel",acct="25640434272252212",flag=M,exp="stayon30a.com | stayson30a.com",src="inferred",
  notes="Clean. 59,184 events (+8%), half server, 500 Lead, 13 Purchase. Three Netlify previews (78) are HG dev; the Guesty engine sent 4. Purchase 28d: 70, all server, against 67 PMS online bookings; the HG AI CAPI is OFF, so Guesty's CAPI is the sender. links.stayson30a.com spelling still unconfirmed."),
 dict(client="Stay Saluda NC",pid="4250460185185664",name="Stay Saluda - Meta Pixel",acct="1863632561215857",flag=M,exp="staysaluda.com",src="inferred",
  notes="Clean on its own pixel. 20,913 events (+14%), 46% server, 454 Lead, 11 Purchase. Purchase 28d: 23, all server, against 29 PMS online bookings (79%, up from 57%); the HG AI CAPI is OFF, so Guesty is the sender and the browser never fires Purchase. The Saluda GHL hosts also fire the Inspired Retreats pixel (see that row)."),
 dict(client="Stay Southern Illinois",pid="1328561309169535",name="Southern Illinois Cabins - Meta Pixel",acct="1661949078036229",flag=W,exp="southernilcabins.com | staysouthernillinois.com | shawneeforestcabins.com | woodlandcabins.net | newvillagevacationhomes.com + OwnerRez",src="inferred",
  notes="Week 8: unchanged. Sister brand sites still fire into this pixel: shawneeforestcabins.com (3,293), woodlandcabins.net (2,128), newvillagevacationhomes.com (22), 17% of 31,808 events. New evidence: the client's own OwnerRez account books under 'Shawnee Forest Cabins' (32), 'Southern Illinois Cabins' (22) and 'Woodland Cabins' (19) in the last 28 days, so at least two of the three are the client's brands. 91 Lead, 31 Purchase, half server. Purchase 28d: 155 (66 browser / 89 server) against 73 PMS online bookings, within the 1.5x line. Next action (Shawal): confirm the sister brands so the row can close and the domains flip to confirmed."),
 dict(client="Stay With Branch",pid="1107997340818783",name="Branch",acct="1269399754049770",flag=M,exp="staywithbranch.com | gostaywithbranch.com + Guesty",src="inferred",
  notes="Clean (site 825, Guesty booking engine 628, GHL subdomains 457); 1,927 events (−6%), 2 Lead, no server events this week because there was no booking to send. Purchase 28d: 1 against 2 PMS online bookings; no direct booking since 22 Oct and no Sales budget."),
 dict(client="StayLuxe",pid="4293491110916917",name="StayLuxe Meta Pixel",acct="25033578722931437",flag=M,exp="stayluxe.vacations | gostayluxevacations.com + Uplisting",src="inferred",
  notes="Clean. 1,838 events (−22%), half server, 29 Lead. First Purchase since the Purchase check started: 1 on 7 Nov, the HG AI CAPI's first send for the tenant, against the 1 PMS online booking. Kristal refreshed the creatives this week. Low volume matches the $20/day budget."),
 dict(client="Sunapee Stays",pid="471248637966769",name="sunapeestays's Pixel",acct="651114096215889",flag=M,exp="sunapeestays.com",src="sheet",
  notes="Clean. 5,741 events (−30%), 28 Lead, 4 Purchase. Purchase 28d: 27, all server, against 27 PMS online bookings (100%; HG AI CAPI on, 30 sent). Direct bookings slowed: month-to-date $1,970 against $13,540 at the same point in October."),
 dict(client="Taberg Falls",pid="964214909847907",name="Taberg Falls - Meta Pixel",acct="827872700004659",flag=M,exp="tabergfalls.com",src="inferred",
  notes="Clean. 56,133 events (+9%), 40% server, 2,206 Lead, 11 Purchase. Purchase 28d: 31, all server, against 38 PMS online bookings (82%); the HG AI CAPI is OFF, so Hostaway's CAPI is the sender. The account still lists five other clients' pixels (decision 13)."),
 dict(client="The Cohost Company",pid="638998632168952",name="The Cohost Company Meta Pixel",acct="9141035462679902",flag=M,exp="thecohostcompany.com | gocohostcompany.com",src="inferred",
  notes="Clean. 8,160 events (−5%), 78 Lead, 5 Purchase; the server side is Purchase only. Purchase 28d: 19, all server, against 32 PMS online bookings (59%); the HG AI CAPI is OFF, so Guesty is the sender. The 'MDS -' campaigns were changed this week by two people outside the HiddenGem team (budgets cut on 3 and 4 Nov); see the spend check."),
 dict(client="The Outpost",pid="1691591692267740",name="HG - The Outpost Grand Canyon Event Data",acct="1530849534802936",flag=W,exp="outpostgrandcanyon.com",src="inferred",
  notes="Week 8: the HiddenGem-managed pixel still receives only link-in-bio events (907; 106 Lead, half server). Site and booking engine fire the client-owned pixel below; the funnel is split. Decision 10 open. Next action (Anna): pick one pixel and install it on the site too."),
 dict(client="The Outpost",pid="734783866381382",name="Outpost Grand Canyon",acct="1530849534802936",flag=W,exp="outpostgrandcanyon.com + Newbook",src="inferred",
  notes="Week 8: the client-BM pixel carries the Newbook booking engine (2,445) and the site (504); 3,026 events (+2%), 2 Purchase, server side Purchase only. Purchase 28d: 19, all server (HG AI CAPI on, 21 sent), against 41 PMS online bookings (46%): the Newbook confirmation fires no browser Purchase and the platform only sends bookings with an email or phone that are under 7 days old when synced. See the row above."),
 dict(client="Three Suns Cabins",pid="691977289952800",name="Three Suns Cabins - Pixel",acct="1210218584137342",flag=W,exp="threesunscabins.com",src="inferred",
  notes="Week 8: still nothing from the main website, only the link-in-bio page (187); 195 events, 8 Purchase server-side. Purchase 28d: 27, all server (HG AI CAPI on, 29 sent), against 27 PMS online bookings, so the platform covers Purchases, but the pixel base code is still missing from threesunscabins.com. Next action (Anna): install the pixel on the site; confirm the domain."),
 dict(client="Treetop Escapes",pid="1178838797064774",name="Treetop Escapes - Pixel",acct="967636478877602",flag=M,exp="staytreetopescapes.com + Guesty",src="inferred",
  notes="Clean. 37,193 events (flat), 46% server, 1,097 Lead, 16 Purchase; two Guesty engine hosts (14). Pixel also shared into Taberg's account. Purchase 28d: 52 (8 browser / 44 server) against 43 PMS online bookings; the HG AI CAPI is OFF, so Guesty is the sender."),
 dict(client="Tuxedo Falls",pid="1561325308991270",name="Tuxedo Falls - Ad Account's Pixel",acct="2077151009889326",flag=W,exp="tuxedofalls.com",src="inferred",
  notes="Week 8: ZERO events, silent since 1 Sep (10 weeks). The ad account's only attached pixel is empty while the real tracking runs on 'Website' 1839806973541001 below. Next action (Chiara): share the Website pixel to the ad account and retire this one (decision 18)."),
 dict(client="Tuxedo Falls",pid="1839806973541001",name="Website",acct="2077151009889326",flag=W,exp="tuxedofalls.com + ResNexus + GHL",src="inferred",
  notes="Week 7: live pixel carrying the site (7,136), ResNexus (3,318) and the GHL funnel (1,284 plus 38 on the GHL sites host); 11,916 events (−44%), 7 Purchase, browser only, still NOT shared to ad account 2077151009889326. Purchase 28d: 25, all browser (ResNexus confirmations), no PMS in the platform. Decision 18."),
 dict(client="Walden Retreats",pid="505477285266646",name="Walden Retreat's Data",acct="973261794434226",flag=M,exp="waldenretreats.com + ResNexus",src="inferred",
  notes="Clean on domains: site 11,928, ResNexus 2,659, bio 1,339. 18,175 events (+9%), 43% server, 203 Lead, 33 Purchase. HG dev traffic grew: 982 events from 127.0.0.1 (2 to 6 Nov) and 27 from hiddengem.media, a local build of the Walden site carrying the live pixel; drop it from dev builds (Leshan). Purchase 28d: 253 (187 browser / 66 server); all 31 Purchases this week were browser-side, the second week with no server Purchase (the server sender, not the HG AI platform, stopped after 26 Oct). ResNexus browser confirmations still fire, so nothing is lost yet. The client paused both of its own wedding-lead campaigns (2 and 5 Nov)."),
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
L.append(f"**Date:** {TODAY} · **Clients on sheet:** {CLIENTS_ON_SHEET} ({CLIENTS_ON_SHEET-len(OFFBOARDED_EXCLUDED)-len(NOT_CHECKED)} checked) · **Pixel rows reviewed:** {len(ROWS)} ({len(distinct)} distinct pixels) · **Receiving events correctly:** {counts[M]} ✅ · **Critical:** {counts[C]} ❌ · **Warnings:** {counts[W]} ⚠️ · **Blocked:** {counts[B]} 🔴 · **Total events, last 7 days:** {total_events:,}\n")
L.append(f"Eighth run (Monday). Compared against the {PREV[:10]} report. Read through the Meta Marketing API with the HiddenGem-Claude system user (`scripts/pull-pixel-stats.mts`, {WINDOW}, window ending 07:48 PT): each pixel's 7-day host breakdown with per-day counts, event totals, browser/server split, and the 28-day Purchase split. Gooseberry Lodges' blocker row is dropped: no ads are running yet (Shawal, 9 Nov). Nine Pines Retreats joined the Master sheet (Not Live, no ad account) and is not checked either. New row: the client-built 'Selah | Black Walnut' pixel. Canopy at Moody Moon Ridge is offboarded and not checked. Expected domains are still the inferred set from the first run (see footer). Checked against the actions log in PROJECT.md section 9 and this week's Meta activity logs.\n")
HDR="| Client | Pixel Name | Pixel ID | Events (last 7d) | Purchase (28d, browser / server) | Domains Seen | Expected Domain(s) | Match | Notes/Issues |\n|---|---|---|---|---|---|---|---|---|"
def trow(r): return f"| {r['client']} | {r['name']} | {r['pid']} | {r['events']:,} | {pcell(r)} | {', '.join(r['hosts']) if r['hosts'] else 'none'} | {r['exp']} | {ICON[r['flag']]} | {r['notes']} |"
L.append("## Critical issues (❌ and 🔴)\n")
crit=[r for r in ROWS if r["flag"] in (C,B)]
if crit:
    L.append("**The Saluda → Inspired Retreats leak is in its eighth week at the same share of events (20%):**\n")
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
L.append("**What moved this week.** New: Selah Place's client built a 'Selah | Black Walnut' pixel for the new Black Walnut property (live 6 Nov); the client's Black Walnut campaigns optimise on it, and blackwalnut.selah.place also fires the main Selah pixel. Best Texas Travel's River Road Cabins share rose from 33% to 40% (week 3). North Star is slightly better than reported last week: the Cloudbeds engine fired the account pixel on five days (9 events), and the HG AI CAPI is sending (9 Purchases in 7 days; last week's 'stalled' read came from a stale last_sent date). Everything else in this table is carried over unchanged.\n")
L.append("**Removed:** Gooseberry Lodges' blocker row (no ads running yet, Shawal 9 Nov; it was not a finding about a pixel).\n")
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
L.append(f"- Clients on sheet: {CLIENTS_ON_SHEET} ({CLIENTS_ON_SHEET-NOT_LIVE-1} Live, {NOT_LIVE} Not Live, 1 offboarded and excluded: {', '.join(OFFBOARDED_EXCLUDED)}). Big Moon Ranch is offboarded too but still on the sheet, so it keeps its row. Pixel rows: {len(ROWS)} ({len(distinct)} distinct pixels; Starlight Haven's pixel serves both accounts, Columbia Gorge, Green Springs, North Star, Ponderosa, The Outpost and Tuxedo Falls have two rows each; Selah Place has three: the Event Data pixel, LinkTree and the new Black Walnut pixel). Not checked: Gooseberry Lodges and Nine Pines Retreats, on the sheet with no ad account and no ads running yet.")
L.append(f"- Pixels found: {len(distinct)}. With events: {len([p for p in distinct if events_of(p)>0])}. Silent: {len(silent)} ({', '.join(r['name'] for r in silent)}). Blocked: {counts[B]}.")
L.append(f"- Total events across all pixels, {WINDOW}: {total_events:,} (each shared pixel counted once, from the API's event totals, comparable with last week's 872,016).")
L.append("- Server events column: Y = at least one server (CAPI) event inside the 7-day window; the notes give the share. Browser-only by design per the sheet: Starlight Haven, The Outpost (client pixel), Columbia Gorge Getaways (CGG Pixel), Ponderosa's second pixel. From this week a server side that carries Purchase only is treated as a working Purchase-only CAPI (HG AI platform, Hostaway, Guesty, OwnerRez), not as silent; the HG AI CAPI column in the Purchase check says whether the platform is the sender. Sheet says CAPI but nothing reaches the pixel server-side: Asheville River Cabins (0). Bison Ridge's server side is back at 49% after a week at zero.")
L.append(f"- Ad accounts listed through the API: {len(pull['clients'])} client accounts, 0 listing errors, 0 read errors. Raven Rock Mountain still has zero pixels attached. Táberg Falls' account still lists five other clients' pixels. Gooseberry Lodges and Nine Pines Retreats have no account in the client map (no ads yet), so nothing was listed for them. Attached pixels that never fired in the window (Event Data, test and retired pixels) are listed in the notes where relevant.")
L.append("- Pixels in the HG BM that belong to no sheet client and fired in the last 28 days: "+", ".join(sorted(f"{p['name']} ({p['total_events']:,})" for p in notsheet if p['total_events']>0))+". Hillside Amble, Cowan Creek, Edenwood and Stay Different run ads without a Master sheet row (section 5 note); a 'Wix Pixel' in Selah's business fired 3 times from www.selah.place. Never fired or dead: "+", ".join(sorted(p['name'] for p in notsheet if p['total_events']==0))+".")
L.append(f"- Previous report compared against: {PREV}. Diff joined on pixel ID. Rows removed since last week: "+("; ".join(f"{v['client']} ({v['pixel_id']}, was {v['flag']})" for v in removed) if removed else "none")+".")
L.append("- Expected domains: every row is still `inferred` from the brand name plus observed traffic (first run), except Sunapee Stays (`sheet`). Inferred domains that contain the client's brand name are treated as confirmed; the ⚠️ for inference applies only where it does not (parkerhouseohio.com, the Southern Illinois sister brands, links.stayson30a.com). Confirm with Shawal and flip `source` to `confirmed` in `expected-domains.csv`.")
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
