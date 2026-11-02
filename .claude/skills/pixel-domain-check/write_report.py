"""Writes the dated pixel domain check .md and .csv from pixel_pull.json.

The per-pixel flags, expected domains and notes are authored by Claude in
ROWS below each week (the judgement part of the audit); events, hosts,
browser/server split and the week-over-week diff are computed here.
"""
import json, csv, os, glob, datetime, collections
SP=os.path.dirname(os.path.abspath(__file__))
ROOT=os.path.abspath(os.path.join(SP,"..","..",".."))
OUT=os.path.join(ROOT,"weekly","Meta Pixel Reviews","Weekly Checks")
TODAY="2026-11-02"
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
CLIENTS_ON_SHEET=46; NOT_LIVE=2; OFFBOARDED_EXCLUDED=["Canopy at Moody Moon Ridge"]
WINDOW="26 Oct to 2 Nov"

M,W,C,B="match","warning","critical","blocker"
ROWS=[
 dict(client="American River Resort",pid="2862601447415133",name="American River Resort - Meta Pixel",acct="953162737054331",flag=M,exp="americanriverresort.com",src="inferred",
  notes="Clean. Ads off since 15 Oct (paused, not offboarded). The pixel still fires from the site and bio: 5,826 events (−25%, third week without ad traffic), half server, 8 SubmitApplication, no Lead or Purchase in the week; the GHL funnel host go.americanriverresort.com did not fire at all."),
 dict(client="Asheville River Cabins",pid="1634367080775220",name="Asheville River Cabins Meta Pixel",acct="615836588009747",flag=W,exp="ashevillerivercabins.com + Cloudbeds",src="inferred",
  notes="Week 7: domains clean (Cloudbeds booking engine 17,725, site 9,228, bio 682, GHL 583); 62 Purchase, 175 Lead, 28,391 events (−17%). Sheet says 'CAPI Setup (HG Ai)' but the pixel is still browser-only: 0 of 28,391 events server-side, and the HG AI CAPI has never sent for this tenant (no PMS connection; Cloudbeds API access is with Leshan). This is the one 'CAPI silent' row that stays open: unlike the five rows reclassified this week, nothing at all reaches the pixel server-side, so every Purchase depends on the browser. 219 browser Purchase in 28 days, no PMS row to compare. Next action (Charlotte / Shawal): get the Cloudbeds API access so the HG AI CAPI can send, and correct the sheet until it does."),
 dict(client="Away2PA",pid="772693422494226",name="Away 2PA Meta Pixel",acct="603977626130795",flag=M,exp="away2pa.com | awaytopa.com",src="inferred",
  notes="Clean. 23,526 events (+5%), half server, 12 Purchase, 288 Lead. OwnerRez booking engine present (599). Purchase 28d: 65 (18 browser / 47 server) against 32 PMS online bookings; the HG AI CAPI sent 34, so the server side is the platform and the browser Purchases are OwnerRez confirmations that do not share an event_id with it (not deduplicated). Within the 1.5x over-count line."),
 dict(client="Awayframes",pid="773898245792839",name="Awayframes - Meta Pixel",acct="2471256056603833",flag=M,exp="awayframes.com",src="inferred",
  notes="Clean. 18,202 events (+248%) after the budget went from $30 to $200/day on 29 Oct (new MoF lookalike campaign, all campaigns to $50): 650 Lead (76 last week), 11 Purchase, 41% server. book.awayframes.com carried 1,718 events, 1,402 of them in the last 14 hours of the window, worth a glance that the booking page is not looping. Two Netlify previews (9 events) are HG dev. Purchase 28d: 24, all server, against 20 PMS online bookings. The HG AI CAPI toggle reads OFF for Awayframes although its ledger sent 15 in the window (last 28 Oct), so the server Purchases now come from Hostaway's own CAPI; nothing lost yet, but one sender should be chosen (Alicia / Leshan)."),
 dict(client="Best Texas Travel",pid="4108409325970216",name="Best Texas - Meta Pixel",acct="1982551189319458",flag=W,exp="besttexastravel.com + Holiday Future",src="inferred",
  notes="Week 2: the River Road Cabins hosts are still firing this pixel every day: bookings.riverroadcabins.com 9,577, riverroadcabins.com 2,025, riverroadcabins.holidayfuture.com 112, together 11,714 or 33% of the week's 35,107 (37% last week). River Road Cabins is not a HiddenGem client; it runs the same Holiday Future booking engine, so it still looks like a sister property of the same owner, unconfirmed. Own domains clean: book. 21,956 (the besttexastravel.holidayfuture.com host has moved onto this subdomain), site 580, bio 699; 113 Lead, 5 Purchase, half server. Purchase 28d: 22, all server, against 26 PMS online bookings (85%); HG AI CAPI on, 27 sent. Next action (Nicole): confirm River Road Cabins belongs to the client and whether its bookings should count toward Best Texas Travel's ads; if not, remove the pixel from riverroadcabins.com and its booking engine."),
 dict(client="Big Moon Ranch",pid="1208874174466414",name="Big Moon Ranch - Meta Pixel",acct="758851247064974",flag=W,exp="bigmoonranch.com | staybigmoonranch.com",src="inferred",
  notes="Week 5: client offboarded 28 Sep but the HG BM pixel is still installed on bigmoonranch.com, 5,753 events this week (−36%) and 53% server-side, so a CAPI connection is still sending too (the HG AI tenant has no pixel assigned, so it is not the platform). Still on the Master sheet. Next action (Charlotte): remove the pixel from the site, disconnect the CAPI connection, and take the row off the sheet (decision 25)."),
 dict(client="Bison Ridge Retreat",pid="1241959234316508",name="Bison Ridge - Meta Pixel",acct="950241787963535",flag=M,exp="bisonridgeretreat.com",src="inferred",
  notes="Clean on domains. 4,510 events (−27%), 73 Lead, no Purchase. Change this week: the server side went from about half of events to zero (0 of 4,510). The sheet says 'Browser Events Only' so the row is not flagged, but something that was sending server events (GHL or the HG AI site, not the platform CAPI, which has never sent for this tenant) stopped on or before 26 Oct; worth knowing what it was. Event Data pixel 1617239586052069 still attached and dead."),
 dict(client="Cabin Collective",pid="1654110122884436",name="Cabin Collective BB Meta Pixel (New)",acct="2194562394139883",flag=M,exp="cabincollectivebb.com + OwnerRez",src="inferred",
  notes="Clean, second week. 11,726 events (+66%), half server, 169 Lead, 28 Purchase (7 days). Hosts: cabincollectivebb.com 9,758, the HG landing page on Netlify 823, OwnerRez booking engine 906, bio 206, the Bluehost staging host zdg.bfk.mybluehost.me 6 and an 'hf-page' pseudo-host (8, an HG test page). Purchase 28d: 47 (31 browser / 16 server) against 34 PMS online bookings; the HG AI CAPI has no pixel assigned for this tenant, so the server events come from OwnerRez. The old 'Cabin Collective BB Pixel' 1338006181525466 is still attached and dead since 15 Oct. Sheet Status still reads Not Live although $30/day has run since 20 Oct, which also keeps the Purchase check at n/a. Next action (Chiara): set the sheet row to Live and detach the dead pixel."),
 dict(client="Columbia Gorge Getaways",pid="595257656540749",name="CGG Pixel",acct="490940113157881",flag=W,exp="columbiagorgegetaways.com | columbiagorgeglamping.com",src="inferred",
  notes="Week 7: unchanged. Fires only from the Wix static host (529) and the GHL funnel go.columbiagorgeglamping.com (328), never from the main site, browser only; 14 Lead, 16 SubmitApplication. Two live pixels on one client. Next action (Chiara): put the primary pixel on the GHL funnel pages and retire this one, or record it as the funnel pixel."),
 dict(client="Columbia Gorge Getaways",pid="700947282709400",name="Columbia Gorge Getaways Pixel",acct="490940113157881",flag=M,exp="columbiagorgegetaways.com + ResNexus",src="inferred",
  notes="Clean. Main site plus ResNexus booking engine; 6,988 events (−9%), 48% server, 2 Purchase in the week. Purchase 28d: 50 (25 browser / 25 server, the ResNexus pairs), but only 2 since 27 Oct after 48 in the three weeks before; no PMS in the platform to compare. Worth asking whether bookings really slowed or the ResNexus confirmation stopped firing (Chiara)."),
 dict(client="Endless Stays",pid="876508505381758",name="Endless Stays Meta Pixel",acct="896372356081479",flag=M,exp="stayendless.com + Hospitable",src="inferred",
  notes="Clean. 31,558 events (−4%), half server, 775 Lead, 134 SubmitApplication, 1 Purchase in the week. join.stayendless.com (4,531) is the client's own lead-magnet subdomain; Hospitable booking engine present (102). Purchase 28d: 13, all server, against 13 PMS online bookings (HG AI CAPI on, 14 sent): the platform is the only Purchase sender and the booking confirmation page carries no browser Purchase."),
 dict(client="Evergreen Cabins",pid="1474685406530880",name="Evergreen Cabins Meta Pixel",acct="453808647114273",flag=M,exp="evergreencabins.co + Hospitable",src="inferred",
  notes="Clean. 29,884 events (−25%), 28% server, 9 Purchase, 97 Lead, 260 SubmitApplication. Purchase 28d: 39, all server, against 38 PMS online bookings (HG AI CAPI on, 40 sent); browser never fires Purchase."),
 dict(client="FLOHOM",pid="139231105894533",name="FLO2 Conversion",acct="2100710320122219",flag=M,exp="flohom.com | goflohom.com",src="inferred",
  notes="Reclassified from ⚠️ (week 3 'CAPI effectively silent'): the 25 server events are 24 Purchase plus one other, which is what a Purchase-only Conversions API sends. The HG AI CAPI is OFF for FLOHOM, so the sender is Hostaway's own CAPI; Purchase 28d 100 (9 browser / 91 server) against 103 PMS online bookings (97%). Nothing in the account changed; the test did. Domains clean: book. 16,534, site 13,889, GHL subdomains; 31,742 events (+24%), 194 Lead, 27 Purchase. One thing to watch: book.flohom.com fell from 3,000 to 4,000 events a day to about 350 a day from 31 Oct while Purchases kept arriving server-side, so either booking-page traffic dropped or the browser pixel on the booking engine changed (Makenna)."),
 dict(client="Glasscombe",pid="1369498611461163",name="Aero Camp Pixel",acct="2030318804465316",flag=M,exp="glasscombe.com + Cloudbeds",src="inferred",
  notes="Clean, second week. www.glasscombe.com 5,132, the Cloudbeds engine us2.cloudbeds.com 2,690, bio 2,652, reserve. 17; 13,517 events (−16%), 40% server, 504 Lead, 4 Purchase. Purchase 28d: 13 (4 browser / 9 server) against 13 PMS online bookings (HG AI CAPI on, 7 sent; the rest is Cloudbeds). Pixel still named 'Aero Camp Pixel'; cosmetic."),
 dict(client="Green Springs Inn",pid="1602971745164199",name="Green Springs Inn Event Data",acct="1390516335151357",flag=W,exp="greenspringsinn.com + Holiday Future",src="inferred",
  notes="Week 7: unchanged. Receives booking-engine events only (book.greenspringsinn.com, 33,324) and the same events land on the GSI Wix pixel (32,988 from the same host), so bookings are double-counted across the two pixels; 34 Purchase here this week. Purchase 28d: 173 (87 browser / 86 server) against 81 PMS online bookings: the booking engine fires a browser Purchase and the HG AI CAPI (on, 82 sent) a server one for the same bookings, and they do not share an event_id, hence 2x. Next action (Alicia): remove the booking-engine snippet from one pixel (decision 11)."),
 dict(client="Green Springs Inn",pid="1098954801239133",name="GSI - Wix Pixel",acct="1390516335151357",flag=M,exp="greenspringsinn.com | staygreenspringsinn.com + Holiday Future",src="inferred",
  notes="Clean on its own: site, booking engine, GHL subdomains; 45,299 events (+2%), half server, 20 Purchase, 133 Lead. New this week: a GSI site build on Cloudflare Pages (gsi-site-6k2.pages.dev 63, pr-sprint-5.gsi-site-6k2.pages.dev 40) plus localhost and 127.0.0.1 (12) on 29 to 31 Oct, an HG dev site carrying the live pixel; accepted as HG dev, but drop the pixel from the preview builds before launch (Leshan). See the Event Data row for the double count."),
 dict(client="Hiawassee Glamping",pid="1149628220675980",name="Hiawassee Meta Pixel",acct="4219624811692502",flag=M,exp="hiawasseeglamping.com",src="inferred",
  notes="Clean. 10,863 events (−38% on an unchanged $30/day; site traffic fell from 2,000 to 1,300 a day), half server, 146 Lead, 6 Purchase. Purchase 28d: 20, all server, against 18 PMS online bookings (HG AI CAPI on, 21 sent). Event Data pixel still dead."),
 dict(client="Home Base",pid="1467511861488785",name="Home Base Bnb - Meta Pixel",acct="3224125791099903",flag=M,exp="homebasebnbs.com | stayhomebase.com + Guesty",src="inferred",
  notes="Clean. 6,774 events (−28%), half server, 51 Purchase, 53 Lead; staging.homebasebnbs.com (4) is the client's own staging. Purchase 28d: 177, all server, against 26 PMS online bookings but 217 direct bookings: the HG AI CAPI (on, 121 sent) sends every direct booking including the 179 owner and manual entries, in batches (37 on 12 Oct, 31 on 14 Oct, 29 on 30 Oct). Not an over-count by the rule, but the BoF campaign is optimising on Purchases no ad could have driven; decision 26's purchase-value question applies here too."),
 dict(client="Inspired Retreats",pid="1547510566197386",name="Inspired Retreats Meta Pixel",acct="1494841894957652",flag=C,exp="stayinspiredretreats.com",src="inferred",
  notes="CROSS-CONTAMINATION, week 7, NOT fixed: go.staysaluda.com (510), links.staysaluda.com (194) and bio.staysaluda.com (177) fired this pixel on every day of the window, 881 events or 19% of its 4,612, the same share as the previous six weeks. 50% of the pixel's events arrive server-side. Saluda's own pixel is clean, so the leak is one-way. No Purchase in 28 days against 6 PMS online bookings with $5/day on BoF, and the HG AI CAPI is OFF for the tenant, so the Purchase check fails too. Next action (Shawal / Leshan): the page-snippet and GHL pixel-events paths have been ruled out, so open the HG AI CAPI connector for Stay Saluda and the GHL sub-account's Facebook Conversions API integration and check which pixel ID each sends to; one of them carries 1547510566197386."),
 dict(client="Little River Landing",pid="1816709606431185",name="Little River Landing Meta Pixel",acct="884285717873613",flag=M,exp="staylittleriver.com",src="inferred",
  notes="Clean on domains, fifth clean week; the two Netlify hosts (8 events) are HG dev. 2,465 events (+19%), 48% server, 64 Lead, 1 Purchase. Purchase 28d: 3, all server, against 11 PMS online bookings with $15/day on BoF, the case that started the Purchase check on 30 Oct and still ❌: the HG AI CAPI is OFF (one send ever, 30 Sep), the browser never fires Purchase, and the 3 server Purchases come from Guesty. Next action (Makenna / Leshan): turn the HG AI CAPI on for the tenant or get the Guesty booking engine to fire Purchase in the browser."),
 dict(client="Myrinn",pid="1943632852972363",name="Myrinn - Meta Pixel",acct="1668286333836716",flag=M,exp="staywithmyrinn.com",src="inferred",
  notes="Clean. 4,387 events (−28%), half server, 72 Lead, 2 Purchase. Purchase 28d: 5, all server, against 5 PMS online bookings (HG AI CAPI on, 5 sent)."),
 dict(client="Nature Nooks",pid="844302611320158",name="Nature Nooks - Meta Pixel",acct="1796752774213285",flag=M,exp="naturenooksacadia.com",src="inferred",
  notes="Clean. 2,626 events (−20%), half server, 134 Lead, no Purchase (no Sales budget, Streamline PMS not in the platform). Sheet says browser only; the server side is live."),
 dict(client="North Star Resort & Lodge",pid="3440147309499983",name="North Star Lodge Killington - Meta Pixel",acct="2003562593933799",flag=W,exp="northstarkillington.com + GHL + Cloudbeds",src="inferred",
  notes="Week 7, worse: the Cloudbeds booking engine fired this pixel once all week (hotels.cloudbeds.com 1 event on 27 Oct) and the HG BM pixel below not at all, so booking-engine pages have carried no pixel since 19 Oct. The attached pixel otherwise carries the site (541) and the GHL funnel (262); 836 events (−12%), 36 Lead, 1 Purchase, 1 server event. Purchase 28d: 35, all server, against 94 PMS online bookings (37%), and only 1 in the last 7 days after 34 in the prior three weeks; the HG AI CAPI is on (35 sent in 28 days, 1 in 7) but its last_sent reads 3 Oct, so the platform send looks stalled too. Next action (Charlotte / Leshan): reinstall the canonical pixel in the Cloudbeds engine and check the HG AI CAPI connection for the tenant; decision 9 still open."),
 dict(client="North Star Resort & Lodge",pid="1904436107168032",name="Northstar Meta Pixel",acct="2003562593933799",flag=W,exp="northstarkillington.com + Cloudbeds",src="inferred",
  notes="Week 7: the HiddenGem BM pixel, not attached to the ad account, is now dead: 13 events, all from the GHL funnel in the first hour of the window, last fired 26 Oct 16:23 UTC. It carried 25 browser Purchase from the Cloudbeds engine up to 19 Oct and nothing since. If the account pixel above is made canonical in Cloudbeds this row can be retired."),
 dict(client="Oak & Ember",pid="1729106025177871",name="Oak & Ember - Meta Pixel",acct="831762063342909",flag=M,exp="stayoakandember.com + Hospitable",src="inferred",
  notes="Clean. 19,676 events (−18%): the GHL funnel go.stayoakandember.com 3,998, 296 SubmitApplication, 104 Lead, half server; 14 events from 127.0.0.1 on 30 Oct are dev. No Purchase in 28 days with $5/day on BoF and a Hospitable PMS the platform has only limited access to, so capture cannot be judged; the booking confirmation carries no Purchase event either way (Chiara). Event Data pixel still dead."),
 dict(client="Paradise Pointe",pid="707016175006193",name="Paradise Pointe - Pixel",acct="1585826092078255",flag=M,exp="stayparadisepointe.com",src="inferred",
  notes="Reclassified from ⚠️ (week 3 'CAPI effectively silent'): the 23 server events in the week are exactly the 23 server Purchases, a Purchase-only Conversions API. The HG AI CAPI is OFF for the tenant, so the sender is Guesty; Purchase 28d 276 (167 browser / 109 server) against 113 PMS online bookings (129 direct). The browser Purchases alone exceed online bookings (148%), which is the pattern of a confirmation page that fires on reload; within the 1.5x over-count line but the purchase-value question (decision 26) is still open. Domains clean; 32,192 events (−4%), 361 Lead, 47 Purchase."),
 dict(client="Parker Reserve",pid="1188475652520634",name="Parker Reserve - Pixel",acct="1002927148609804",flag=W,exp="parkerreserve.com",src="inferred",
  notes="Week 7: parkerhouseohio.com steady at 16 events (0.6%), still unconfirmed. 2,842 events (+5%), half server, 3 Purchase, 10 SubmitApplication. Purchase 28d: 4, all server (HG AI CAPI on, 6 sent), against 8 PMS online bookings; no Sales budget ($10/day giveaway only). Next action (Kristal): confirm parkerhouseohio.com is a Parker property or remove the pixel from it."),
 dict(client="Ponderosa Pines Resort",pid="1293211539656211",name="Ponderosa Pines Resort - Meta Pixel",acct="1058846326445255",flag=M,exp="ponderosapinesresort.com + Newbook",src="inferred",
  notes="Clean on domains. 21,120 events (−17%), 51% server, 76 Purchase, 574 Lead; site, bio, two Wix static hosts, Newbook booking engine. Purchase 28d: 313 (208 browser / 105 server) against 125 PMS online bookings: the browser alone is 1.66x the bookings, so the Newbook confirmation fires Purchase more than once per booking (reloads, or a thank-you page that fires on every visit) and the HG AI CAPI (on, 7 sent since 23 Oct) adds a server copy. Flagged in the Purchase check as an over-count. Next action (Anna): fire Purchase once per booking on the Newbook confirmation."),
 dict(client="Ponderosa Pines Resort",pid="1743173753375733",name="Ponderosa Pines Resort's Pixel",acct="1058846326445255",flag=W,exp="ponderosapinesresort.com",src="inferred",
  notes="Week 4: the client-owned pixel, attached to the ad account, still fires PageView only from www.ponderosapinesresort.com (4,635 events, browser only), so page views are double-counted with the HG pixel above. Next action (Anna): confirm which pixel the ads use and remove the other from the site (decision 33)."),
 dict(client="Raven Rock Mountain",pid="1359649962298380",name="Raven Rock Meta Pixel",acct="1065186195582056",flag=W,exp="ravenrockmountain.com | stayravenrockmountain.com",src="inferred",
  notes="Week 7: domains clean (site 2,151, links. and info. subdomains), 2,482 events (−28%), 4 Purchase, 30 SubmitApplication, but the pixel is still NOT shared to ad account 1065186195582056 (the account lists zero pixels). Purchase 28d: 17, all server (HG AI CAPI on, 20 sent), against 16 PMS online bookings, so tracking is ready when ads restart. Client Not Live on the sheet. Next action (Anna): share the pixel to the account before any campaign relaunch."),
 dict(client="Red White & Blue Views",pid="1625871301864243",name="Red White & Blue - Meta Pixel",acct="1419930382946246",flag=M,exp="redwhiteandblueviews.com",src="inferred",
  notes="Clean on domains. 23,569 events (+3%), 47% server, 1 Purchase, 86 Lead. The book. booking-engine host is back at 21,725 after two weeks of decline, but in spikes: 5,211 on 30 Oct and 9,434 on 1 Nov against about 1,400 on other days, which looks like a crawler or a page loop rather than guests (Nicole / Leshan to glance at the engine). Purchase 28d: 5, all server (HG AI CAPI on, 8 sent), against 8 PMS online bookings; the booking engine fires no browser Purchase."),
 dict(client="Ridge & Falls",pid="1332286819018269",name="Ridge & Falls - Meta Pixel",acct="1313401330776046",flag=M,exp="ridgeandfalls.com",src="inferred",
  notes="Reclassified from ⚠️ (week 3 'CAPI effectively silent'): the 7 server events in the week are the 7 server Purchases, a Purchase-only Conversions API, and the HG AI CAPI is on (11 sent in 28 days). Domains clean (site 2,405, GHL funnel 1,109, GHL sites host 109); 3,637 events (+7%), 72 Lead, 7 Purchase. Purchase 28d: 19, all server, against 11 PMS online bookings: 11 from the platform and about 8 more from a second server sender (Boom / Guesty), which the Purchase check flags as an over-count. Next action (Makenna / Leshan): keep one server sender for Ridge & Falls."),
 dict(client="Selah Place",pid="1235173718368839",name="Selah.Place Event Data",acct="1275283434220508",flag=M,exp="selah.place + Holiday Future",src="inferred",
  notes="Clean on domains. 105,076 events (−37% from the 167k spike; the holidayfuture booking engine fell from 145k to 83k), 48% server, 871 Lead, 59 Purchase. reserve.selah.place (8,779) is the client's own booking subdomain. Purchase 28d: 99 (19 browser / 80 server) against 44 PMS online bookings: the HG AI CAPI (on, 44 sent) and Hostaway's CAPI both send a server Purchase per booking with different event_ids, so Meta counts each booking about twice; flagged in the Purchase check as an over-count. A third pixel in the client's own business ('Wix Pixel for fc9ae0e6…', 375795251002998) fired once from www.selah.place on 27 Oct. Next action (Alicia / Leshan): keep one server sender for Selah."),
 dict(client="Selah Place",pid="3327546500757583",name="LinkTree",acct="1275283434220508",flag=W,exp="selah.place | linktr.ee",src="inferred",
  notes="Week 7: the second pixel is still installed on www.selah.place (3,265 of its 3,274 events), so page views are double-counted; 2 events from linktr.ee itself. Next action (Alicia): remove this pixel from the site, keep it on Linktree only."),
 dict(client="Starlight Haven - Hot Springs",pid="766226461367996",name="Starlight Haven Pixel - ResNexus",acct="901138032027913",flag=M,exp="visitstarlight.com + ResNexus",src="inferred",
  notes="Clean. One pixel shared by both Starlight accounts (this row: Hot Springs) and shared into Taberg's account, browser only as the sheet says. resnexus.com is the largest host (20,529); 31,463 events (−7%), 80 Purchase, 1,358 Lead; shop.visitstarlight.com (2) is new and the client's own. Purchase 28d: 318, all browser (ResNexus confirmations); no PMS in the platform to compare."),
 dict(client="Starlight Haven - Weiss Lake",pid="766226461367996",name="Starlight Haven Pixel - ResNexus",acct="74756899",flag=M,exp="visitstarlight.com + ResNexus",src="inferred",
  notes="Clean. Same pixel as Hot Springs (this row: Weiss Lake); see that row for the figures."),
 dict(client="Stay on 30a",pid="1464927198465632",name="Stay on 30a - Meta Pixel",acct="25640434272252212",flag=M,exp="stayon30a.com | stayson30a.com",src="inferred",
  notes="Clean. 54,982 events (+6%), half server, 22 Purchase, 464 Lead. Two Netlify previews (38) are HG dev. Purchase 28d: 70, all server, against 65 PMS online bookings (124 direct): the HG AI CAPI is OFF, so Guesty's CAPI is the sender, and it is sending a few owner or manual entries too. links.stayson30a.com spelling still unconfirmed."),
 dict(client="Stay Saluda NC",pid="4250460185185664",name="Stay Saluda - Meta Pixel",acct="1863632561215857",flag=M,exp="staysaluda.com",src="inferred",
  notes="Clean on its own pixel. 18,303 events (−3%), 46% server, 492 Lead, 5 Purchase. Purchase 28d: 16, all server, against 28 PMS online bookings (57%); the HG AI CAPI is OFF, so Guesty is the sender and the browser never fires Purchase. The Saluda GHL hosts also fire the Inspired Retreats pixel (see that row)."),
 dict(client="Stay Southern Illinois",pid="1328561309169535",name="Southern Illinois Cabins - Meta Pixel",acct="1661949078036229",flag=W,exp="southernilcabins.com | staysouthernillinois.com | shawneeforestcabins.com | woodlandcabins.net | newvillagevacationhomes.com + OwnerRez",src="inferred",
  notes="Week 7: unchanged. Sister brand sites still fire into this pixel: shawneeforestcabins.com (4,069), woodlandcabins.net (1,881), newvillagevacationhomes.com (39), 16% of 37,651 events; 57 Purchase, 89 Lead, half server. Purchase 28d: 174 (75 browser / 99 server) against 76 PMS online bookings: OwnerRez fires a browser Purchase and the HG AI CAPI (on, 23 sent) plus OwnerRez's own CAPI send server copies; within the 1.5x line on the deduplicated count. Next action (Chiara): confirm the three sister brands belong to the client so the row can close."),
 dict(client="Stay With Branch",pid="1107997340818783",name="Branch",acct="1269399754049770",flag=M,exp="staywithbranch.com | gostaywithbranch.com + Guesty",src="inferred",
  notes="Reclassified from ⚠️ (week 3 'CAPI effectively silent'): the server side of this pixel only ever carried Purchase (2 in 28 days, both from the HG AI CAPI, which is on and sent 3), and it sent nothing this week because the PMS shows no online booking since 22 Oct. Domains clean (site 831, Guesty booking engine 764, GHL subdomains); 2,055 events (−17%), 46 SubmitApplication, no Lead or Purchase. The Purchase check flags the stop separately."),
 dict(client="StayLuxe",pid="4293491110916917",name="StayLuxe Meta Pixel",acct="25033578722931437",flag=M,exp="stayluxe.vacations | gostayluxevacations.com + Uplisting",src="inferred",
  notes="Clean. 2,352 events (+36%), half server, 25 Lead, 18 SubmitApplication. book.gostayluxevacations.com (16) is the client's own booking subdomain. No Purchase in 28 days and the PMS shows no online booking either; the HG AI CAPI is on but has never sent (last 9 Aug). Low volume matches the $20/day budget."),
 dict(client="Sunapee Stays",pid="471248637966769",name="sunapeestays's Pixel",acct="651114096215889",flag=M,exp="sunapeestays.com",src="sheet",
  notes="Reclassified from ⚠️ (week 3 'CAPI effectively silent'): the 7 server events in the week are the 7 server Purchases, and the HG AI CAPI is on and sent 45 in 28 days against the pixel's 42 server Purchase and 42 PMS online bookings (100%). The platform is doing its job; the earlier test counted page events the platform never sends. Domains clean; 8,238 events (+22%), 28 Lead, 8 Purchase, 87 CompleteRegistration, 71 Schedule."),
 dict(client="Taberg Falls",pid="964214909847907",name="Taberg Falls - Meta Pixel",acct="827872700004659",flag=M,exp="tabergfalls.com",src="inferred",
  notes="Clean. 51,631 events (+1%), 40% server, 2,071 Lead, 5 Purchase; 8 events from hiddengem.media (an HG-hosted preview) and 7 from www.facebook.com are minor. Purchase 28d: 30, all server, against 38 PMS online bookings (79%); the HG AI CAPI is OFF, so Hostaway's CAPI is the sender. The account still lists five other clients' pixels (FLOHOM, Paradise Pointe, Starlight Haven, The Cohost Company, Treetop Escapes), decision 13."),
 dict(client="The Cohost Company",pid="638998632168952",name="The Cohost Company Meta Pixel",acct="9141035462679902",flag=M,exp="thecohostcompany.com | gocohostcompany.com",src="inferred",
  notes="Clean. 8,546 events (+2%), 182 Lead, 2 Purchase; the campaigns were recreated under 'MDS -' names this week. 2 server events, both Purchase. Purchase 28d: 24, all server, against 40 PMS online bookings (60%); the HG AI CAPI is OFF, so Guesty is the sender. Sheet says 'Full Tracking (AI Site)', not CAPI."),
 dict(client="The Outpost",pid="1691591692267740",name="HG - The Outpost Grand Canyon Event Data",acct="1530849534802936",flag=W,exp="outpostgrandcanyon.com",src="inferred",
  notes="Week 7: the HiddenGem-managed pixel still receives only link-in-bio events (1,039, about 150 a day; 118 Lead, 121 SubmitApplication, half server). Site and booking engine fire the client-owned pixel below; the funnel is split. Decision 10 open. Next action (Anna): pick one pixel and install it on the site too."),
 dict(client="The Outpost",pid="734783866381382",name="Outpost Grand Canyon",acct="1530849534802936",flag=W,exp="outpostgrandcanyon.com + Newbook",src="inferred",
  notes="Week 7: client-BM pixel carries the site (562) and the Newbook booking engine (2,220); 2,981 events (−11%), 8 Purchase, 6 server events (the server Purchases). Purchase 28d: 17, all server (HG AI CAPI on, 19 sent since 23 Oct), against 49 PMS online bookings (35%), flagged in the Purchase check: the Newbook confirmation fires no browser Purchase and the platform only sends bookings with an email or phone that are under 7 days old when synced. See the row above."),
 dict(client="Three Suns Cabins",pid="691977289952800",name="Three Suns Cabins - Pixel",acct="1210218584137342",flag=W,exp="threesunscabins.com",src="inferred",
  notes="Week 7: still no events from the main website, only the link-in-bio page (189, about 27 a day); 4 Purchase arrived server-side, 20 SubmitApplication. Purchase 28d: 28, all server (HG AI CAPI on, 29 sent), against 27 PMS online bookings, so the platform covers Purchases, but the pixel base code is still missing from threesunscabins.com. Next action (Anna): install the pixel on the site; confirm the domain."),
 dict(client="Treetop Escapes",pid="1178838797064774",name="Treetop Escapes - Pixel",acct="967636478877602",flag=M,exp="staytreetopescapes.com + Guesty",src="inferred",
  notes="Clean. 37,344 events (−7%), 46% server, 1,138 Lead, 16 Purchase; the Guesty booking engine (uniquestays.guestybookings.com, 44) is back after a quiet week. Pixel also shared into Taberg's account. Purchase 28d: 49 (6 browser / 43 server) against 42 PMS online bookings; the HG AI CAPI is OFF, so Guesty is the sender."),
 dict(client="Tuxedo Falls",pid="1561325308991270",name="Tuxedo Falls - Ad Account's Pixel",acct="2077151009889326",flag=W,exp="tuxedofalls.com",src="inferred",
  notes="Week 7: ZERO events, silent since 1 Sep (9 weeks). The ad account's only attached pixel is empty while the real tracking runs on 'Website' 1839806973541001 below. Next action (Chiara): share the Website pixel to the ad account and retire this one (decision 18)."),
 dict(client="Tuxedo Falls",pid="1839806973541001",name="Website",acct="2077151009889326",flag=W,exp="tuxedofalls.com + ResNexus + GHL",src="inferred",
  notes="Week 6: live pixel carrying the site (11,168), ResNexus (5,727) and the GHL funnel (3,877 plus 209 on the GHL sites host); 21,163 events (−6%), 5 Purchase, 141 SubmitApplication, browser only, still NOT shared to ad account 2077151009889326. Purchase 28d: 24, all browser (ResNexus confirmations), no PMS in the platform. Decision 18."),
 dict(client="Walden Retreats",pid="505477285266646",name="Walden Retreat's Data",acct="973261794434226",flag=M,exp="waldenretreats.com + ResNexus",src="inferred",
  notes="Clean. 16,729 events (−18%), 42% server, 55 Purchase, 144 Lead, 1,417 InitiateCheckout. 16 events from hiddengem.media (HG-hosted preview, Leshan to drop the pixel) and 20 from 127.0.0.1 on 2 Nov are dev. Purchase 28d: 273 (195 browser / 78 server), but all 53 of this week's Purchases were browser-side: the server sender (not the HG AI platform, which has no pixel for Walden) stopped after 26 Oct. ResNexus confirmations still fire in the browser, so nothing is lost yet; no PMS in the platform to compare."),
 dict(client="Gooseberry Lodges",pid="",name="(no pixel found)",acct="",flag=B,exp="gooseberrylodges.com (inferred, unconfirmed)",src="inferred",
  notes="New on the Master sheet this week (Live, no attribution tier filled in). The client is not in the client map (no ad account ID in PROJECT.md section 5) and no pixel named for it appears in the HG BM owned or shared listings, so nothing could be read. Next action (Shawal): add the ad account ID to the client map and confirm the pixel and website domain; until then the row is a blocker, not a finding about the pixel."),
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
L.append(f"**Date:** {TODAY} · **Clients on sheet:** {CLIENTS_ON_SHEET} ({CLIENTS_ON_SHEET-len(OFFBOARDED_EXCLUDED)} checked) · **Pixel rows reviewed:** {len(ROWS)} ({len(distinct)} distinct pixels) · **Receiving events correctly:** {counts[M]} ✅ · **Critical:** {counts[C]} ❌ · **Warnings:** {counts[W]} ⚠️ · **Blocked:** {counts[B]} 🔴 · **Total events, last 7 days:** {total_events:,}\n")
L.append(f"Seventh run (Monday). Compared against the {PREV[:10]} report. Read through the Meta Marketing API with the HiddenGem-Claude system user (`scripts/pull-pixel-stats.mts`, {WINDOW}, window ending 07:23 PT): each pixel's 7-day host breakdown with per-day counts, event totals, browser/server split, and the 28-day Purchase split. First Monday report with the Purchase check (added 30 Oct). Gooseberry Lodges joined the Master sheet and gets a blocker row until its ad account is mapped. Five 'CAPI effectively silent' warnings are reclassified this week: on those pixels the server side carries Purchase only, which is what the HG AI and PMS-native Conversions APIs send, so the server share of all events was the wrong test; Asheville stays open because nothing at all reaches it server-side. Canopy at Moody Moon Ridge is offboarded and not checked. Expected domains are still the inferred set from the first run (see footer). Checked against the actions log in PROJECT.md section 9.\n")
HDR="| Client | Pixel Name | Pixel ID | Events (last 7d) | Purchase (28d, browser / server) | Domains Seen | Expected Domain(s) | Match | Notes/Issues |\n|---|---|---|---|---|---|---|---|---|"
def trow(r): return f"| {r['client']} | {r['name']} | {r['pid']} | {r['events']:,} | {pcell(r)} | {', '.join(r['hosts']) if r['hosts'] else 'none'} | {r['exp']} | {ICON[r['flag']]} | {r['notes']} |"
L.append("## Critical issues (❌ and 🔴)\n")
crit=[r for r in ROWS if r["flag"] in (C,B)]
if crit:
    L.append("**The Saluda → Inspired Retreats leak is in its seventh week at the same share of events, and Gooseberry Lodges cannot be read until its ad account is in the client map:**\n")
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
L.append("**What moved this week.** North Star got worse: the Cloudbeds booking engine fired the account pixel once all week and the HG BM pixel is now dead, so booking-engine purchases have not reached Meta since 19 Oct and the HG AI CAPI send for the tenant looks stalled too. Best Texas Travel's pixel still fires from River Road Cabins (33% of events), second week, unconfirmed. Everything else in this table is carried over unchanged.\n")
L.append("**Reclassified, not fixed in the account:** FLOHOM, Paradise Pointe, Sunapee Stays, Ridge & Falls and Stay With Branch leave this table because their server events are Purchase events only (24 of 25, 23 of 23, 7 of 7, 7 of 7, and 2 in 28 days), which is how a Purchase-only Conversions API looks; whether enough Purchases arrive is now judged in the Purchase check below. Decision 32 closes for them. Asheville River Cabins stays: 0 server events of any kind, and the HG AI CAPI has never sent for the tenant.\n")
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
L.append(f"- Clients on sheet: {CLIENTS_ON_SHEET} ({CLIENTS_ON_SHEET-NOT_LIVE-1} Live, {NOT_LIVE} Not Live, 1 offboarded and excluded: {', '.join(OFFBOARDED_EXCLUDED)}). Big Moon Ranch is offboarded too but still on the sheet, so it keeps its row. Pixel rows: {len(ROWS)} ({len(distinct)} distinct pixels; Starlight Haven's pixel serves both accounts, Columbia Gorge, Green Springs, North Star, Ponderosa, Selah, The Outpost and Tuxedo Falls have two rows each; Gooseberry Lodges has a blocker row with no pixel).")
L.append(f"- Pixels found: {len(distinct)}. With events: {len([p for p in distinct if events_of(p)>0])}. Silent: {len(silent)} ({', '.join(r['name'] for r in silent)}). Blocked: {counts[B]}.")
L.append(f"- Total events across all pixels, {WINDOW}: {total_events:,} (each shared pixel counted once, from the API's event totals, comparable with last week's 954,806).")
L.append("- Server events column: Y = at least one server (CAPI) event inside the 7-day window; the notes give the share. Browser-only by design per the sheet: Starlight Haven, The Outpost (client pixel), Columbia Gorge Getaways (CGG Pixel), Ponderosa's second pixel. From this week a server side that carries Purchase only is treated as a working Purchase-only CAPI (HG AI platform, Hostaway, Guesty, OwnerRez), not as silent; the HG AI CAPI column in the Purchase check says whether the platform is the sender. Sheet says CAPI but nothing reaches the pixel server-side: Asheville River Cabins (0). Bison Ridge's server side stopped this week (sheet says browser only, so not flagged).")
L.append(f"- Ad accounts listed through the API: {len(pull['clients'])} client accounts, 0 listing errors, 0 read errors. Raven Rock Mountain still has zero pixels attached. Táberg Falls' account still lists five other clients' pixels. Gooseberry Lodges has no account in the client map, so nothing was listed for it. Attached pixels that never fired in the window (Event Data, test and retired pixels) are listed in the notes where relevant.")
L.append("- Pixels in the HG BM that belong to no sheet client and fired in the last 28 days: "+", ".join(sorted(f"{p['name']} ({p['total_events']:,})" for p in notsheet if p['total_events']>0))+". Hillside Amble, Cowan Creek, Edenwood and Stay Different run ads without a Master sheet row (section 5 note); a 'Wix Pixel' in Selah's business fired once from www.selah.place. Never fired or dead: "+", ".join(sorted(p['name'] for p in notsheet if p['total_events']==0))+".")
L.append(f"- Previous report compared against: {PREV}. Diff joined on pixel ID. Rows removed since last week: "+("; ".join(f"{v['client']} ({v['pixel_id']}, was {v['flag']})" for v in removed) if removed else "none")+".")
L.append("- Expected domains: every row is still `inferred` from the brand name plus observed traffic (first run), except Sunapee Stays (`sheet`); Gooseberry Lodges' domain is a guess from the brand name with no traffic behind it. Inferred domains that contain the client's brand name are treated as confirmed; the ⚠️ for inference applies only where it does not (parkerhouseohio.com, the Southern Illinois sister brands, links.stayson30a.com). Confirm with Shawal and flip `source` to `confirmed` in `expected-domains.csv`.")
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
