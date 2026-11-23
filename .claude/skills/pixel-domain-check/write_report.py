"""Writes the dated pixel domain check .md and .csv from pixel_pull.json.

The per-pixel flags, expected domains and notes are authored by Claude in
ROWS below each week (the judgement part of the audit); events, hosts,
browser/server split and the week-over-week diff are computed here.
"""
import json, csv, os, glob, datetime, collections
SP=os.path.dirname(os.path.abspath(__file__))
ROOT=os.path.abspath(os.path.join(SP,"..","..",".."))
OUT=os.path.join(ROOT,"weekly","Meta Pixel Reviews","Weekly Checks")
TODAY="2026-11-23"
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
CLIENTS_ON_SHEET=len(SHEET) or 48; NOT_LIVE=sum(1 for v in SHEET.values() if not v["status"].lower().startswith("live")); OFFBOARDED_EXCLUDED=["Canopy at Moody Moon Ridge","The Cohost Company"]
NOT_CHECKED=["Nine Pines Retreats"]  # on the sheet (Not Live); ad account 1671947624532383 created 18 Nov, $0 spent, not in the client map yet (23 Nov)
WINDOW="16 Nov to 23 Nov"
OFF_SHEET=["Dunya Camp","The Preserve"]
OFFBOARDED_TODAY=[]  # The Cohost Company left the checks on 23 Nov (offboarded 16 Nov)
DUNYA_ACCT_NOTE="Second reads the same morning: the host breakdowns for Away2PA, Best Texas Travel, Walden Retreats and Wanderin Star came back empty on the first pass, the event totals for Tuxedo Falls' main pixel and Dunya Camp came back partial, and Walden's browser/server split came back empty; each was re-read and the fuller figure kept."

M,W,C,B="match","warning","critical","blocker"
ROWS=[
 dict(client="American River Resort",pid="2862601447415133",name="American River Resort - Meta Pixel",acct="953162737054331",flag=M,exp="americanriverresort.com",src="inferred",
  notes="Clean. Ads off since 15 Oct (paused, not offboarded). 4,110 events (−19%), half server, no Lead or Purchase; the site still fires and the GHL hosts sent 8 events."),
 dict(client="Asheville River Cabins",pid="1634367080775220",name="Asheville River Cabins Meta Pixel",acct="615836588009747",flag=W,exp="ashevillerivercabins.com + Cloudbeds",src="inferred",
  notes="Week 10: domains clean (Cloudbeds engine 11,547, site 6,838, GHL 446, bio 342); 19,192 events (−16%), 121 Lead, 52 Purchase in the week. Still 0 server events while the sheet says 'CAPI Setup (HG Ai)': the HG AI CAPI has never sent for this tenant (no PMS connection), so all 250 Purchases in 28 days are browser-side. Next action (Charlotte / Leshan): get the Cloudbeds API access so the HG AI CAPI can send, and correct the sheet until it does."),
 dict(client="Away2PA",pid="772693422494226",name="Away 2PA Meta Pixel",acct="603977626130795",flag=M,exp="away2pa.com | awaytopa.com",src="inferred",
  notes="Clean on domains (away2pa.com 26,735, bio.awaytopa.com 3,228, OwnerRez 812; the host breakdown came back empty on the first read and was re-read). 30,819 events (−36%), half server, 404 Lead, 39 Purchase. Purchase 28d: 121 (37 browser / 84 server) against 45 PMS online bookings: 84 server Purchases against 48 sent by the HG AI CAPI, so a second server sender is active too. Over-count in the Purchase check, week 2. Next action (Alicia / Leshan): keep one server sender for Away2PA."),
 dict(client="Arca Boutique Hotel",pid="691002320103417",name="ArcaRoatan_pixel",acct="1003623765640520",flag=W,exp="arcaroatan.com + Cloudbeds",src="inferred",
  notes="New row: the ArcaRoatan_pixel is attached to the Arca ad account (by 20 Nov; pixel 947609368616575 is AdRoll's and is ignored). 7,553 events, 40% server. Hosts are only the Cloudbeds booking engine (hotels. 5,614, us1. 80) and the HG GHL funnel go.arcaroatan.com 1,763: the main site arcaroatan.com fires nothing, while the BoF retargeting ads link to it. 187 Lead, 8 Purchase. Purchase 28d: 23 (15 browser / 8 server) against 25 PMS online bookings (92%); the HG AI CAPI went on 18 Nov (8 sent). Next action (Anna): install the pixel base code on arcaroatan.com so site visitors join the retargeting audience."),
 dict(client="Awayframes",pid="773898245792839",name="Awayframes - Meta Pixel",acct="2471256056603833",flag=M,exp="awayframes.com",src="inferred",
  notes="Clean (site 2,686, bio 284, book. 130, an HG Netlify preview 13). 3,160 events (−84%): the ad account has been UNSETTLED (payment needed) since 16 Nov, so no ads delivered all week. 20 Lead, 5 Purchase. Purchase 28d: 32, all server, against 30 PMS online bookings (107%); the HG AI CAPI is OFF, so Hostaway's CAPI is the sender."),
 dict(client="Best Texas Travel",pid="4108409325970216",name="Best Texas - Meta Pixel",acct="1982551189319458",flag=M,exp="besttexastravel.com | riverroadcabins.com + Holiday Future",src="confirmed",
  notes="Clean (River Road Cabins is the client's own brand, Shawal 16 Nov): book.besttexastravel.com 17,039, bookings.riverroadcabins.com 13,219, riverroadcabins.com 1,917, site 1,227, bio 583, Holiday Future 209 (host breakdown re-read after an empty first pass). 29,534 events (−13%), 64% server, 96 Lead, 10 Purchase. Purchase 28d: 32, all server, against 37 PMS online bookings (86%; HG AI CAPI on, 36 sent)."),
 dict(client="Big Moon Ranch",pid="1208874174466414",name="Big Moon Ranch - Meta Pixel",acct="758851247064974",flag=W,exp="bigmoonranch.com | staybigmoonranch.com",src="inferred",
  notes="Week 8: client offboarded 28 Sep, but the HG BM pixel is still on bigmoonranch.com: 5,957 events (+11%), half server, so a CAPI connection still sends too. Still on the Master sheet. Next action (Charlotte): remove the pixel from the site, disconnect the CAPI connection and take the row off the sheet (decision 25)."),
 dict(client="Bison Ridge Retreat",pid="1241959234316508",name="Bison Ridge - Meta Pixel",acct="950241787963535",flag=M,exp="bisonridgeretreat.com",src="inferred",
  notes="Clean (site 4,985, bio 824, link. 177). 6,073 events (+17%), half server, 112 Lead. No Purchase in 28 days with $5/day on BoF and no PMS in the platform; at the 18 Nov Meta Ads Strategy meeting the team agreed the property manager will not connect a PMS, so the account runs without Purchase tracking."),
 dict(client="Cabin Collective",pid="1654110122884436",name="Cabin Collective BB Meta Pixel (New)",acct="2194562394139883",flag=M,exp="cabincollectivebb.com + OwnerRez",src="inferred",
  notes="Clean, fifth week: site 9,270, OwnerRez 918, the HG landing page on Netlify 661, bio 241, Bluehost staging 4. 11,128 events (−8%), half server, 134 Lead, 34 Purchase (8 last week). Purchase 28d: 88 (37 browser / 51 server) against 33 PMS online bookings: since 16 Nov the HG AI CAPI (14 sent) and OwnerRez both send server Purchases, 1.5x bookings, the over-count flagged last week. The sheet still reads Not Live, so the Purchase check stays n/a. Next action (Chiara / Leshan): keep one server sender, set the sheet row to Live and detach the dead 'Cabin Collective BB Pixel' 1338006181525466."),
 dict(client="Columbia Gorge Getaways",pid="595257656540749",name="CGG Pixel",acct="490940113157881",flag=W,exp="columbiagorgegetaways.com | columbiagorgeglamping.com",src="inferred",
  notes="Week 10: unchanged. Fires only from the Wix static host (444) and the GHL funnel go.columbiagorgeglamping.com (334), never from the main site, browser only; 11 Lead. Two live pixels on one client. Next action (Chiara): put the primary pixel on the GHL funnel pages and retire this one, or record it as the funnel pixel."),
 dict(client="Columbia Gorge Getaways",pid="700947282709400",name="Columbia Gorge Getaways Pixel",acct="490940113157881",flag=M,exp="columbiagorgegetaways.com + ResNexus",src="inferred",
  notes="Clean. Main site 4,281 and the ResNexus engine 680; 5,014 events (−22%), 44% server, 3 Purchase. Purchase 28d: 21 (13 browser / 8 server); no PMS in the platform to compare."),
 dict(client="Endless Stays",pid="876508505381758",name="Endless Stays Meta Pixel",acct="896372356081479",flag=M,exp="stayendless.com + Hospitable",src="inferred",
  notes="Clean on domains (site 25,086, join. 2,884, bio 1,207, Hospitable 204, GHL 10, 2 from a Google Ads referrer). 29,673 events (−22%), half server, 437 Lead, 5 Purchase. Purchase 28d: 15, all server, against 18 PMS online bookings (83%); the HG AI CAPI (on, 18 sent) is the only Purchase sender and the booking confirmation fires no browser Purchase."),
 dict(client="Evergreen Cabins",pid="1474685406530880",name="Evergreen Cabins Meta Pixel",acct="453808647114273",flag=M,exp="evergreencabins.co + Hospitable",src="inferred",
  notes="Clean (site 24,271, bio 1,720, Hospitable 272, links. 82, GHL API 10). 26,475 events (+1%), 29% server, 72 Lead, 5 Purchase. Purchase 28d: 30, all server, against 29 PMS online bookings (HG AI CAPI on, 31 sent)."),
 dict(client="FLOHOM",pid="139231105894533",name="FLO2 Conversion",acct="2100710320122219",flag=M,exp="flohom.com | goflohom.com",src="inferred",
  notes="Clean. 23,729 events (−11%), 158 Lead, 16 Purchase in the week; site 11,862, book.flohom.com 10,823 (mostly gallery_interaction), bio 843, links. 77, 1 event each from an HG SiteGround staging host and the GHL funnel. Purchase 28d: 83 (8 browser / 75 server) against 87 PMS online bookings (95%); the HG AI CAPI is OFF, so Hostaway's CAPI is the sender. Pixel also shared into Taberg's account."),
 dict(client="Glasscombe",pid="1369498611461163",name="Aero Camp Pixel",acct="2030318804465316",flag=M,exp="glasscombe.com + Cloudbeds",src="inferred",
  notes="Clean. 16,103 events (+19%), 40% server, 408 Lead, 17 Purchase in the week (8 the week before); site 7,176, Cloudbeds 2,995, bio 1,974, reserve. 26. Purchase 28d: 40 (12 browser / 28 server) against 23 PMS online bookings; the server side is 1.2x bookings (HG AI CAPI on, 21 sent). Budget up $20/day this week."),
 dict(client="Green Springs Inn",pid="1602971745164199",name="Green Springs Inn Event Data",acct="1390516335151357",flag=W,exp="greenspringsinn.com + Holiday Future",src="inferred",
  notes="Week 10: unchanged. Receives booking-engine events only (book.greenspringsinn.com, 28,598), the same host that fires the Wix pixel, so bookings are counted on both pixels; 24 Purchase here this week. Purchase 28d: 149 (74 browser / 75 server) against 81 PMS online bookings, 1.8x. Next action (Alicia): remove the booking-engine snippet from one pixel (decision 11)."),
 dict(client="Green Springs Inn",pid="1098954801239133",name="GSI - Wix Pixel",acct="1390516335151357",flag=M,exp="greenspringsinn.com | staygreenspringsinn.com + Holiday Future",src="inferred",
  notes="Clean on its own: booking engine 28,115, site 9,166, GHL subdomains 397, GHL API 12. 38,178 events (+8%), 48% server, 105 Lead, 17 Purchase. The Cloudflare Pages preview traffic is gone this week. Purchase 28d: 79, all server (HG AI CAPI on, 84 sent), against 81 PMS online bookings (98%). See the Event Data row for the double count."),
 dict(client="Hiawassee Glamping",pid="1149628220675980",name="Hiawassee Meta Pixel",acct="4219624811692502",flag=M,exp="hiawasseeglamping.com",src="inferred",
  notes="Clean (site 6,492, bio 703, links. 24, GHL API 8). 7,269 events (−17%), half server, 102 Lead, no Purchase this week. Purchase 28d: 10, all server, against 9 PMS online bookings (HG AI CAPI on, 11 sent); the last Purchase was 15 Nov and the PMS has no direct booking since either (month to date −83%), so the pixel is not missing bookings."),
 dict(client="Home Base",pid="1467511861488785",name="Home Base Bnb - Meta Pixel",acct="3224125791099903",flag=M,exp="homebasebnbs.com | stayhomebase.com + Guesty",src="inferred",
  notes="Clean (site 6,928, bio 580, go. 408, Guesty engine 24, host. and staging. 18). 8,046 events (−16%), half server, 97 Lead, 26 Purchase. Purchase 28d: 115 (1 browser / 114 server) against 37 online and 145 direct PMS bookings: the HG AI CAPI (on, 75 sent) sends every direct booking, owner and manual entries included, so the BoF campaign optimises partly on bookings no ad could have driven. Within the over-count rule, which is judged on direct bookings."),
 dict(client="Inspired Retreats",pid="1547510566197386",name="Inspired Retreats Meta Pixel",acct="1494841894957652",flag=M,exp="stayinspiredretreats.com",src="inferred",
  notes="Domain row held at Shawal's 16 Nov call (Saluda hosts blocked, row withdrawn), but the block has not stopped them: Stay Saluda's GHL hosts reached this pixel every day of this window at the same rate as before, go.staysaluda.com 505 (26 to 107 a day, 16 to 23 Nov), links.staysaluda.com 164 and bio.staysaluda.com 152, 821 events or 19% of 4,230 (972 the week before). They send PageView only; the 223 Lead come from Inspired Retreats' own hosts. Stay Saluda's own pixel receives the same hosts, so Saluda's GHL funnel pages carry both pixel IDs. As the actions log asks, this goes to Shawal before the row is flagged again; the likely fix is to remove the Inspired Retreats pixel ID from the Saluda GHL pages (Makenna). Purchase: 1 server Purchase (10 Nov) in 28 days against 6 PMS online bookings with $5/day on BoF; see the Purchase check."),
 dict(client="Little River Landing",pid="1816709606431185",name="Little River Landing Meta Pixel",acct="884285717873613",flag=M,exp="staylittleriver.com",src="inferred",
  notes="Clean on domains, eighth clean week: site 2,288, GHL funnel 409, two HG Netlify previews 6. 2,710 events (+34%), half server, 50 Lead, no Purchase this week. Purchase 28d: 3, all server, the last on 12 Nov, against 9 PMS online bookings (33%) with $40/day on Sales (BoF $20 plus the 13 Nov lookalike $20). The HG AI CAPI is OFF (one send ever, 30 Sep), the browser never fires Purchase and the few server Purchases come from Guesty. Next action (Makenna / Leshan): turn the HG AI CAPI on for the tenant or get the Guesty booking engine to fire Purchase in the browser."),
 dict(client="Myrinn",pid="1943632852972363",name="Myrinn - Meta Pixel",acct="1668286333836716",flag=M,exp="staywithmyrinn.com",src="inferred",
  notes="Clean (site 4,180, links. 178). 4,378 events (−8%), half server, 30 Lead, 1 Purchase. Purchase 28d: 5, all server, against 5 PMS online bookings (HG AI CAPI on, 5 sent)."),
 dict(client="Nature Nooks",pid="844302611320158",name="Nature Nooks - Meta Pixel",acct="1796752774213285",flag=M,exp="naturenooksacadia.com",src="inferred",
  notes="Clean (site 274, bio 25). 303 events (−29%), third week with all campaigns paused ($0/day). No Purchase; the Purchase check is n/a while ads are off. At the 18 Nov Meta Ads Strategy meeting the team agreed Purchase tracking cannot be set up for Nature Nooks (no compatible PMS) and will proceed without it."),
 dict(client="North Star Resort & Lodge",pid="3440147309499983",name="North Star Lodge Killington - Meta Pixel",acct="2003562593933799",flag=W,exp="northstarkillington.com + GHL + Cloudbeds",src="inferred",
  notes="Week 10: the Cloudbeds engine fired 14 events this week (13 last week), so a few booking pages carry the pixel but most still do not. Site 595, GHL funnel 210; 842 events (−18%), 27 Lead, 15 Purchase, all server from the HG AI CAPI (15 sent in 7 days). Purchase 28d: 36 against 56 PMS online bookings (64%); against the 35 'Website/Booking Engine' bookings the server Purchases match about one for one. Next action (Charlotte / Leshan): reinstall the account pixel in the Cloudbeds engine so the browser Purchase fires again (decision 9)."),
 dict(client="North Star Resort & Lodge",pid="1904436107168032",name="Northstar Meta Pixel",acct="2003562593933799",flag=W,exp="northstarkillington.com + Cloudbeds",src="inferred",
  notes="Week 10: dead. Zero events, last fired 26 Oct, now outside the 28-day window. Not attached to the ad account. Next action (Charlotte): retire it once the account pixel above is the one installed in Cloudbeds (decision 9)."),
 dict(client="Oak & Ember",pid="1729106025177871",name="Oak & Ember - Meta Pixel",acct="831762063342909",flag=M,exp="stayoakandember.com + Hospitable",src="inferred",
  notes="Clean (site 11,946, GHL funnel 2,702, Hospitable 28). 14,847 events (−13%), half server, 60 Lead. No Purchase in 28 days with $5/day on BoF: the Hospitable account is not connected to the platform, so nothing sends a Purchase."),
 dict(client="Paradise Pointe",pid="707016175006193",name="Paradise Pointe - Pixel",acct="1585826092078255",flag=M,exp="stayparadisepointe.com",src="inferred",
  notes="Clean (site 31,448, go. 1,037, bio 504; 6 from a local build, 3 from the HG Netlify build, 9 from Facebook referrers). 33,109 events (flat), 317 Lead, 46 Purchase. Purchase 28d: 192 (92 browser / 100 server) against 103 PMS online bookings; the larger side is 0.75x direct bookings, so no over-count. The HG AI CAPI is OFF and Guesty is the server sender. Decision 26 (purchase value) still open."),
 dict(client="Parker Reserve",pid="1188475652520634",name="Parker Reserve - Pixel",acct="1002927148609804",flag=W,exp="parkerreserve.com",src="inferred",
  notes="Week 10: parkerhouseohio.com 78 events (2.3%), still unconfirmed; 4 from a Firebase storage host. 3,445 events (+45%), half server, 1 Purchase. Purchase 28d: 7, all server (HG AI CAPI on, 10 sent), against 12 PMS online bookings (58%); no Sales budget ($10/day giveaway only). Next action (Nicole): confirm parkerhouseohio.com is a Parker property or remove the pixel from it."),
 dict(client="Ponderosa Pines Resort",pid="1293211539656211",name="Ponderosa Pines Resort - Meta Pixel",acct="1058846326445255",flag=M,exp="ponderosapinesresort.com + Newbook",src="inferred",
  notes="Clean on domains: site 15,664, bio 2,130, Wix static 1,757, Newbook 32. 19,646 events (−12%), half server, 343 Lead, 50 Purchase. Purchase 28d: 327 (213 browser / 114 server) against 119 PMS online bookings: the browser alone is 1.8x, so the Newbook confirmation still fires Purchase more than once per booking, and the HG AI CAPI (on, 13 sent) adds a server copy. Over-count in the Purchase check, week 4; the $40/day MoF lookalike (13 Nov) optimises on this signal. Next action (Anna): make the Newbook confirmation fire Purchase once per booking."),
 dict(client="Ponderosa Pines Resort",pid="1743173753375733",name="Ponderosa Pines Resort's Pixel",acct="1058846326445255",flag=W,exp="ponderosapinesresort.com",src="inferred",
  notes="Week 7: the client-owned pixel attached to the ad account still fires PageView only from www.ponderosapinesresort.com (4,395 events, browser only), so page views are double-counted with the HG pixel above. Next action (Anna): confirm which pixel the ads use and remove the other from the site (decision 33)."),
 dict(client="Raven Rock Mountain",pid="1359649962298380",name="Raven Rock Meta Pixel",acct="1065186195582056",flag=W,exp="ravenrockmountain.com | stayravenrockmountain.com",src="inferred",
  notes="Week 10: domains clean (site 3,004, links. 443, info. 272; 2,197 of them on 21 Nov alone); 3,735 events (+200%), 3 Purchase, but the pixel is still NOT shared to ad account 1065186195582056 (the account lists zero pixels). Purchase 28d: 10, all server (HG AI CAPI on, 12 sent), against 10 PMS online bookings. Client Not Live, $0/day. Next action (Anna): share the pixel to the account before any campaign relaunch."),
 dict(client="Red White & Blue Views",pid="1625871301864243",name="Red White & Blue - Meta Pixel",acct="1419930382946246",flag=M,exp="redwhiteandblueviews.com",src="inferred",
  notes="Clean on domains: the book. booking-engine host 19,726 (mostly gallery_interaction), bio 735, site 173, GHL 211, Holiday Future 12. 20,868 events (−21%), half server, 70 Lead, no Purchase this week. Purchase 28d: 11, all server, against 12 PMS online bookings (HG AI CAPI on, 11 sent); the last Purchase was 13 Nov and the PMS has no direct booking in the last 7 days either."),
 dict(client="Ridge & Falls",pid="1332286819018269",name="Ridge & Falls - Meta Pixel",acct="1313401330776046",flag=M,exp="ridgeandfalls.com",src="inferred",
  notes="Clean (site 2,232, GHL funnel 837, GHL sites host 89). 3,177 events (−5%), 59 Lead, 12 Purchase. Purchase 28d: 30, all server, against 15 online and 18 direct PMS bookings, 1.7x: the HG AI CAPI (on, 18 sent) and a second server sender both send each booking. Over-count in the Purchase check, week 4. Next action (Makenna / Leshan): keep one server sender for Ridge & Falls."),
 dict(client="Selah Place",pid="1235173718368839",name="Selah.Place Event Data",acct="1275283434220508",flag=M,exp="selah.place + Holiday Future",src="inferred",
  notes="Clean on domains. 153,150 events (+6%): the Holiday Future engine 128,550 (mostly gallery_interaction), reserve. 11,201, site 8,226, bio 2,853, Wix static 2,033, blackwalnut.selah.place 95. 21 Purchase in the week. Purchase 28d: 180 (40 browser / 140 server) against 49 PMS online bookings, server 2.9x: the HG AI CAPI (on, 55 sent) and Hostaway's CAPI each send every booking with different event_ids. Over-count in the Purchase check, week 4. Next action (Alicia / Leshan): keep one server sender for Selah."),
 dict(client="Selah Place",pid="1786742402537824",name="Selah | Black Walnut",acct="1275283434220508",flag=W,exp="blackwalnut.selah.place",src="inferred",
  notes="Week 3: the client's Black Walnut pixel fired 460 events (−71%), 300 of them on the morning of 23 Nov after the client's three Black Walnut BF Pre-Booking / Pre-Sale campaigns went live (spend check, 23 Nov). 10 Lead, no Purchase since 7 Nov. blackwalnut.selah.place still fires the main Selah pixel too (95 events), so Black Walnut visits are counted on two pixels. Next action (Alicia): agree with the client which pixel stays on blackwalnut.selah.place now the campaigns are back."),
 dict(client="Selah Place",pid="3327546500757583",name="LinkTree",acct="1275283434220508",flag=W,exp="selah.place | linktr.ee",src="inferred",
  notes="Week 10: the second pixel is still installed on www.selah.place (2,840 of its 2,871 events), so page views are double-counted; 29 events from linktr.ee itself. Next action (Alicia): remove this pixel from the site, keep it on Linktree only."),
 dict(client="Starlight Haven - Hot Springs",pid="766226461367996",name="Starlight Haven Pixel - ResNexus",acct="901138032027913",flag=M,exp="visitstarlight.com + ResNexus",src="inferred",
  notes="Clean. One pixel shared by both Starlight accounts (this row: Hot Springs) and shared into Taberg's account, browser only as the sheet says. ResNexus 17,354, site 6,915, book. 2,691, GHL 625; 27,659 events (−17%), 1,221 Lead, 80 Purchase. Purchase 28d: 339, all browser; no PMS in the platform."),
 dict(client="Starlight Haven - Weiss Lake",pid="766226461367996",name="Starlight Haven Pixel - ResNexus",acct="74756899",flag=M,exp="visitstarlight.com + ResNexus",src="inferred",
  notes="Clean. Same pixel as Hot Springs (this row: Weiss Lake); see that row for the figures."),
 dict(client="Stay on 30a",pid="1464927198465632",name="Stay on 30a - Meta Pixel",acct="25640434272252212",flag=M,exp="stayon30a.com | stayson30a.com",src="inferred",
  notes="Clean (site 56,609, links.stayson30a.com 2,458). 59,322 events (+8%), half server, 411 Lead, 29 Purchase. Purchase 28d: 79, all server, against 78 PMS online bookings (101%); the HG AI CAPI is OFF, so Guesty is the sender."),
 dict(client="Stay Saluda NC",pid="4250460185185664",name="Stay Saluda - Meta Pixel",acct="1863632561215857",flag=M,exp="staysaluda.com",src="inferred",
  notes="Clean on its own pixel (site 19,098, go. 1,518, links. 410, bio 375). 21,363 events (−5%), 46% server, 424 Lead, 2 Purchase. Purchase 28d: 22, all server, against 30 PMS online bookings (73%); the HG AI CAPI is OFF, so Guesty is the sender and the browser never fires Purchase. Its GHL hosts still fire the Inspired Retreats pixel too (see that row)."),
 dict(client="Stay Southern Illinois",pid="1328561309169535",name="Southern Illinois Cabins - Meta Pixel",acct="1661949078036229",flag=M,exp="southernilcabins.com | staysouthernillinois.com | shawneeforestcabins.com | woodlandcabins.net + OwnerRez",src="confirmed",
  notes="Clean (brands confirmed 9 Nov): site 12,549, shawneeforestcabins.com 2,629, woodlandcabins.net 2,258, OwnerRez 2,802, GHL 717; newvillagevacationhomes.com 26 still unconfirmed. 25,356 events (−11%), half server, 57 Lead, 47 Purchase. Purchase 28d: 159 (71 browser / 88 server) against 74 PMS online bookings; the server side is 1.2x (HG AI CAPI on, 17 sent, plus OwnerRez)."),
 dict(client="Stay With Branch",pid="1107997340818783",name="Branch",acct="1269399754049770",flag=M,exp="staywithbranch.com | gostaywithbranch.com + Guesty",src="inferred",
  notes="Clean (site 619, Guesty engine 396, GHL 397). 1,416 events (+5%), 72 Lead, no server events because there was no booking to send: the PMS shows no direct booking in 28 days."),
 dict(client="StayLuxe",pid="4293491110916917",name="StayLuxe Meta Pixel",acct="25033578722931437",flag=M,exp="stayluxe.vacations | gostayluxevacations.com + Uplisting",src="inferred",
  notes="Clean (site 1,189, bio 547, Booked Directly engine 294). Event totals read in full this week: 2,043 events, half server, 68 Lead. Purchase 28d: 1 (7 Nov) against 1 PMS online booking; low volume matches the $20/day budget."),
 dict(client="Sunapee Stays",pid="471248637966769",name="sunapeestays's Pixel",acct="651114096215889",flag=M,exp="sunapeestays.com",src="sheet",
  notes="Clean (site 4,741, go. 100). 4,863 events (−19%), 16 Lead, 9 Purchase. Purchase 28d: 23, all server, against 24 PMS online bookings (96%; HG AI CAPI on, 26 sent)."),
 dict(client="Taberg Falls",pid="964214909847907",name="Taberg Falls - Meta Pixel",acct="827872700004659",flag=M,exp="tabergfalls.com",src="inferred",
  notes="Clean (site 39,144, bio 11,668; 4 from hiddengem.media, 2 from the HG Netlify landing page). 51,069 events (+2%), 40% server, 1,708 Lead, 5 Purchase. Purchase 28d: 27, all server, against 31 PMS online bookings (87%); the HG AI CAPI is OFF, so Hostaway's CAPI is the sender. Budget up $100/day this week ('TF / Speed Plan / Clean build')."),
 dict(client="The Outpost",pid="1691591692267740",name="HG - The Outpost Grand Canyon Event Data",acct="1530849534802936",flag=W,exp="outpostgrandcanyon.com",src="inferred",
  notes="Week 10: the HiddenGem-managed pixel still receives only link-in-bio events (777; 76 Lead, half server). Site and booking engine fire the client-owned pixel below; the funnel is split. Decision 10 open. Next action (Anna): pick one pixel and install it on the site too."),
 dict(client="The Outpost",pid="734783866381382",name="Outpost Grand Canyon",acct="1530849534802936",flag=W,exp="outpostgrandcanyon.com + Newbook",src="inferred",
  notes="Week 10: the client-BM pixel carries the Newbook booking engine (1,967) and the site (308); 2,379 events (−10%), 6 Purchase, server side Purchase only. Purchase 28d: 17, all server (HG AI CAPI on, 19 sent), against 31 PMS online bookings (55%): the Newbook confirmation fires no browser Purchase. See the row above."),
 dict(client="Three Suns Cabins",pid="691977289952800",name="Three Suns Cabins - Pixel",acct="1210218584137342",flag=W,exp="threesunscabins.com",src="inferred",
  notes="Week 10: still nothing from the main website, only the link-in-bio page (154); 157 events, 3 Purchase server-side. Purchase 28d: 18, all server (HG AI CAPI on, 21 sent), against 21 PMS online bookings, so the platform covers Purchases, but the pixel base code is still missing from threesunscabins.com. Next action (Anna): install the pixel on the site."),
 dict(client="Treetop Escapes",pid="1178838797064774",name="Treetop Escapes - Pixel",acct="967636478877602",flag=M,exp="staytreetopescapes.com + Guesty",src="inferred",
  notes="Clean (site 24,800, go. 2,102, bio 552, Guesty 26, an HG Netlify preview 6). 27,604 events (−27%), 45% server, 405 Lead, 10 Purchase. Pixel also shared into Taberg's account. Purchase 28d: 60 (12 browser / 48 server) against 44 PMS online bookings; the server side (Guesty; the HG AI CAPI is OFF) is 1.0x direct bookings."),
 dict(client="Tuxedo Falls",pid="1839806973541001",name="Tuxedo Falls - Main Pixel",acct="2077151009889326",flag=M,exp="tuxedofalls.com + ResNexus + GHL",src="inferred",
  notes="Fixed: the live pixel (renamed from 'Website' to 'Tuxedo Falls - Main Pixel') is now attached to ad account 2077151009889326 and shared into the HG BM, the sharing step of decision 18. Site 5,801, ResNexus 1,691, GHL funnel 909 plus 43 on GHL hosts; 8,493 events (−59% after the 12 and 13 Nov spike; the first event-total read came back partial at 726 and was re-read), browser only, 8 Lead, 1 Purchase. Purchase 28d: 24, all browser (ResNexus confirmations), the last on 17 Nov; no PMS in the platform. The old 'Tuxedo Falls - Ad Account's Pixel' 1561325308991270 is still attached and silent since 1 Sep. Next action (Chiara): detach it."),
 dict(client="Walden Retreats",pid="505477285266646",name="Walden Retreat's Data",acct="973261794434226",flag=M,exp="waldenretreats.com + ResNexus",src="inferred",
  notes="Clean on domains: site 10,233, ResNexus 6,508, bio 1,046, the Spacecrafted site-builder host 270, hiddengem.media 12 (host breakdown and browser/server split re-read after an empty first pass). 17,059 events (+14%), 53% server, 168 Lead. Purchase 28d: 271 (188 browser / 83 server), 102 in the last 7 days with spikes of 46 on 16 Nov and 32 on 21 Nov. The HG AI CAPI has sent nothing (no PMS connection), so the server copies come from another sender, and there is no PMS to check the count against. BoF retargeting back on at $10/day this week. Next action (Anna): check ResNexus for the bookings made on 16 and 21 Nov; if there are far fewer than 46 and 32, the confirmation page fires Purchase more than once."),
 dict(client="Dunya Camp",pid="229378313100169",name="Dunya Camp Pixel",acct="629838998232110",flag=M,exp="dunyacamp.com + LuxuryRes booking engine",src="inferred",
  notes="Clean, second week (not on the Master sheet). 43,722 events (−21%; the first event-total read came back partial and was re-read), half server from a non-HG sender (the HG AI tenant has no PMS and has sent nothing). Hosts: dunyacamp.com 24,906, the LuxuryRes engine 15,866, the HG GHL funnel go.dunyacamp.com 2,325 (186 last week; the HG build switched on 16 Nov), HG Netlify 18, Showit 4. The legacy funnel's custom 'Step 1' (7,870) and 'Step 2' (8,219) events still fire. Purchase 28d: 24 (12 browser / 12 server), 4 on 18 Nov and none since; no PMS to compare."),
 dict(client="The Preserve",pid="541451090721842",name="Preserve Properties's Pixel",acct="528888625350386",flag=W,exp="thepreserveri.com",src="inferred",
  notes="Week 2, with a new tracking fault: since 16 Nov www.thepreserveri.com fires Lead and CompleteRegistration on most page views. Lead went from 6 to 261 a day (9 to 15 Nov) to about 1,900 a day from 16 Nov and 5,500 to 9,700 a day from 20 Nov (23 Nov so far: 5,627 Lead on 4,629 page views); 26,291 of the last four days' Leads came from the main site. 164,381 events (+160%), almost all browser; 34,128 Lead and 33,013 CompleteRegistration in the week. Any campaign optimising on website Lead now learns on this signal and website-Lead CPL reads far too low. Other hosts as last week: bio 7,211, preservemembership.com 2,439, dbsteak.com 705, preserveaspot.com 117 (sister sites, still unconfirmed), the SynXis booking engine 9. Purchase 28d: 18, all server; no PMS in the platform. Next action (Alicia): find the tag added on 16 Nov that fires Lead and CompleteRegistration site-wide and limit it to real form submissions; confirm the three sister domains."),
 dict(client="Gooseberry Lodges",pid="3431371590511492",name="Gooseberry's Pixel",acct="701051796368186",flag=M,exp="gooseberrylodges.com + SiteMinder (direct-book.com)",src="inferred",
  notes="Clean, second week: site 3,372, bio (GHL sign-up) 507, the SiteMinder engine direct-book.com 12. 4,009 events (+11%), browser only (no CAPI), 75 Lead, 11 Purchase. Purchase 28d: 47, all browser, 1 to 3 a day, so the booking confirmation fires; no PMS in the platform to check capture. The ad account's payment hold from 20 Nov is cleared."),
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
    if _c in OFFBOARDED_TODAY: _prim["pflag"],_prim["pnote"]="n/a",f"offboarded on 16 Nov, so it is out of the ad spend check and not judged; {_prim['p28']} Purchase in 28d"
    if _c in OFF_SHEET: _prim["pflag"],_prim["pnote"]="n/a",f"not on the Master sheet, so the Purchase check does not judge it; {_prim['p28']} Purchase in 28d"
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
L.append(f"Tenth run (Monday). Compared against the {PREV[:10]} report. Read through the Meta Marketing API with the HG - ROI Dashboard system user (`scripts/pull-pixel-stats.mts`, {WINDOW}, window ending 07:02 PT): each pixel's 7-day host breakdown with per-day counts, event totals, browser/server split, and the 28-day Purchase split. New this week: Arca Boutique Hotel's pixel row (ArcaRoatan_pixel, attached to the ad account by 20 Nov). Out this week: The Cohost Company (offboarded 16 Nov). Nine Pines Retreats (Not Live; ad account created 18 Nov, not in the client map yet) is still not checked; Canopy at Moody Moon Ridge is offboarded. Expected domains are still the inferred set from the first run except where the footer says otherwise. Checked against the actions log in PROJECT.md section 9, the 18 Nov Meta Ads Strategy notes and this week's spend check.\n")
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
L.append("**What moved this week.** Not closed after all: Stay Saluda's GHL hosts still reach the Inspired Retreats pixel every day of this window at the same rate (821 events, 19%) although Shawal blocked them on 16 Nov; the row is held at his 16 Nov call and raised with him before it is flagged again (actions log). New warning: The Preserve's site fires Lead and CompleteRegistration on most page views since 16 Nov (34,128 Lead in the week against 2,665), which corrupts any Lead-optimised campaign and the CPL. New row: Arca's pixel, clean on domains but missing from the main site arcaroatan.com. Fixed: Tuxedo Falls, whose live pixel is now attached to the ad account (decision 18's sharing step); the silent old pixel moves into its notes. Awayframes' events fell 84% with the account on a payment hold all week. Selah's Black Walnut pixel woke up on 23 Nov as the client's Black Walnut campaigns restarted. On the Purchase side: Cabin Collective now has two server senders (1.5x bookings, n/a while the sheet reads Not Live); Ponderosa, Ridge & Falls, Selah and Away2PA stay over-counted; Little River Landing and Inspired Retreats are still ❌ with Sales budgets running. Everything else is carried over.\n")
L.append("**Removed:** The Cohost Company (638998632168952, offboarded 16 Nov, out of the checks from this week; its pixel still fires 7,033 events a week and is still shared into Taberg's ad account) and Tuxedo Falls' silent 'Ad Account's Pixel' 1561325308991270, which no longer needs its own row now the live pixel is attached (see the Tuxedo notes).\n")
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
notsheet=[p for p in pull["pixels"] if not p.get("skipped") and p["id"] not in distinct and p["id"] not in ("861460105842405","638998632168952","1561325308991270")]
L.append("## Footer\n")
L.append(f"- Clients on sheet: {CLIENTS_ON_SHEET} ({CLIENTS_ON_SHEET-NOT_LIVE-len(OFFBOARDED_EXCLUDED)} Live, {NOT_LIVE} Not Live, {len(OFFBOARDED_EXCLUDED)} offboarded and excluded: {', '.join(OFFBOARDED_EXCLUDED)}), plus {', '.join(OFF_SHEET)}, which run ads without a Master sheet row (client map 16 Nov, Shawal). Big Moon Ranch is offboarded too but still on the sheet, so it keeps its row. Pixel rows: {len(ROWS)} ({len(distinct)} distinct pixels; Starlight Haven's pixel serves both accounts; Columbia Gorge, Green Springs, North Star, Ponderosa and The Outpost have two rows each; Selah Place has three: the Event Data pixel, LinkTree and the client's Black Walnut pixel). Not checked: Nine Pines Retreats (Not Live; its ad account 1671947624532383 was created on 18 Nov with $0 spent and is not in the client map yet; its HG AI tenant already sends CAPI Purchases to pixel 4120815361560941).")
L.append(f"- Pixels found: {len(distinct)}. With events: {len([p for p in distinct if events_of(p)>0])}. Silent: {len(silent)} ({', '.join(r['name'] for r in silent)}). Blocked: {counts[B]}.")
L.append(f"- Total events across all pixels, {WINDOW}: {total_events:,} (each shared pixel counted once, from the API's event totals after the second reads, comparable with last week's 901,154).")
L.append("- Server events column: Y = at least one server (CAPI) event inside the 7-day window; the notes give the share. Browser-only by design per the sheet: Starlight Haven, The Outpost (client pixel), Columbia Gorge Getaways (CGG Pixel), Ponderosa's second pixel. A server side that carries Purchase only is a working Purchase-only CAPI (HG AI platform, Hostaway, Guesty, OwnerRez), not silent; the HG AI CAPI column in the Purchase check says whether the platform is the sender. Sheet says CAPI but nothing reaches the pixel server-side: Asheville River Cabins (0), week 10.")
L.append(f"- Ad accounts listed through the API: {len(pull['clients'])} client accounts in the pull, 0 listing errors, 0 read errors. "+DUNYA_ACCT_NOTE+" Raven Rock Mountain still has zero pixels attached. Táberg Falls' account still lists five other clients' pixels (FLOHOM, Paradise Pointe, Starlight Haven, Treetop Escapes, The Cohost Company). Attached pixels that never fired in the window (Event Data, test and retired pixels) are listed in the notes where relevant.")
L.append("- Pixels in the HG BM that belong to no sheet client and fired in the last 28 days: "+", ".join(sorted(f"{p['name']} ({p['total_events']:,})" for p in notsheet if p['total_events']>0))+". Hillside Amble, Cowan Creek, Edenwood and Stay Different run ads without a Master sheet row (section 5 note). Never fired or dead: "+", ".join(sorted(p['name'] for p in notsheet if p['total_events']==0))+".")
L.append(f"- Previous report compared against: {PREV}. Diff joined on pixel ID. Rows removed since last week: "+("; ".join(f"{v['client']} ({v['pixel_id']}, was {v['flag']})" for v in removed) if removed else "none")+".")
L.append("- Expected domains: every row is still `inferred` from the brand name plus observed traffic (first run), except Sunapee Stays (`sheet`), Stay Southern Illinois (`confirmed` 9 Nov; newvillagevacationhomes.com, 26 events this week, still unconfirmed) and Best Texas Travel (`confirmed` 16 Nov). Inferred domains that contain the client's brand name are treated as confirmed; the ⚠️ for inference applies only where it does not (parkerhouseohio.com, links.stayson30a.com, and The Preserve's preservemembership.com, dbsteak.com and preserveaspot.com). New inferred row this week: Arca Boutique Hotel (arcaroatan.com + Cloudbeds). Confirm with Shawal and flip `source` to `confirmed` in `expected-domains.csv`.")
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
