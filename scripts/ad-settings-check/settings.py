"""Setup and enhancement checks for the daily Meta ad review (imported by scripts/ad-copy-check/daily.py).

Read-only. It never writes to Meta and it prints nothing, because the repo and its Actions logs are public.
Built on 2026-11-18 from the 17 Nov reviews of The Preserve and Arca:
  - All 17 Preserve RT ads sat in an ad set that had been paused since 12 Nov, so $0 was spent.
  - Arca's BoF ads carried Se-lah's product catalog through the promo-code metadata.
  - Arca's BoF ad set targeted Honduras only, while the account's other ad sets targeted the US.
  - Enhancements were still opted in (relevant comments, site links, destination screenshot, multi-advertiser).

Contract (agreed with the daily.py session on 2026-11-18):
    check_settings(act, ads, get, get_all) -> list of findings
    act      "act_123"
    ads      the ads daily.py collected (new, edited, or switched on), each with id, name, created_time,
             updated_time, status, effective_status, adset{id,name,effective_status},
             campaign{id,name,effective_status} and
             creative{..., degrees_of_freedom_spec, creative_sourcing_spec, contextual_multi_ads}
    get      get(path, params) -> dict, rate-limit aware (check.get)
    get_all  get_all(path, params) -> list, follows paging (check.get_all)
    finding  {"ad_id", "ad", "campaign", "adset", "kind", "severity", "detail"}
             severity is "urgent" (ads customers see are wrong, or ads aren't running), "warning" or "note".
             detail is one plain sentence: what's wrong and where to fix it.

Shawal's recorded decisions this module follows (memory files, Nov 2026):
  - Advantage+ audience is left ON on BoF and engager-lead ad sets (12 Nov): a note at most.
  - translate_voiceover OPT_IN is the Ads Manager default on about half of all ads: a note.
  - Enhancement opt-ins are never urgent (The Preserve's were left on, 17 Nov).
  - call_ads_configuration, http links and the 20_s_calls metric are false alarms: not checked here.
  - Dunya Camp's legacy funnel (Step 2 / Step 3 / fall winter purchase) and Selah's client-run "SP |"
    campaigns aren't HiddenGem's: skipped.
"""
import csv
import glob
import json
import os
import re
import time
from collections import defaultdict
from urllib.parse import urlparse

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HG_BUSINESS_ID = "158693423705448"

# Campaigns that belong to the client, not HiddenGem (don't review their setup).
NOT_HG_CAMPAIGNS = {
    "act_629838998232110": re.compile(r"step\s*2|step\s*3|fall winter purchase", re.I),  # Dunya legacy funnel
}
NOT_HG_ANY_ACCOUNT = re.compile(r"^\s*SP\s*\|")  # Selah's own "SP | ..." campaigns

# Feature keys in creative_features_spec and how they read in Ads Manager.
FEATURE_LABELS = {
    "inline_comment": "relevant comments",
    "translate_voiceover": "voice translation",
    "text_translation": "text translation",
    "image_text_translation": "image text translation",
    "video_filtering": "video filters",
    "image_touchups": "visual touch-ups",
    "image_enhancement": "image enhancement",
    "image_brightness_and_contrast": "brightness and contrast",
    "image_animation": "image animation",
    "image_templates": "image templates",
    "image_uncrop": "image expansion",
    "image_background_gen": "generated backgrounds",
    "video_uncrop": "video expansion",
    "video_auto_crop": "video auto-crop",
    "video_highlight": "video highlights",
    "video_highlights": "video highlights",
    "video_to_image": "video to image",
    "carousel_to_video": "carousel to video",
    "multi_photo_to_video": "photos to video",
    "add_text_overlay": "text overlays",
    "text_optimizations": "text improvements",
    "description_automation": "auto descriptions",
    "enhance_cta": "enhanced CTA",
    "generate_cta": "generated CTA",
    "music": "music",
    "audio": "music",
    "video_voiceover": "AI voiceover",
    "adapt_to_placement": "adapt to placement",
    "media_type_automation": "media type automation",
    "media_order": "media order",
    "reveal_details_over_time": "reveal details over time",
    "show_summary": "summaries",
    "show_destination_blurbs": "destination blurbs",
    "profile_card": "profile card",
    "site_extensions": "site links",
    "local_store_extension": "store locations",
    "creative_stickers": "stickers",
    "advantage_plus_creative": "Advantage+ creative",
    "pac_relaxation": "flexible placement assets",
    "cv_transformation": "visual transformations",
    "feed_caption_optimization": "caption optimization",
    "ig_video_native_subtitle": "auto subtitles",
}
# Opt-ins that add products or change what the ad says: a warning, not a note.
PRODUCT_FEATURES = {"product_extensions", "product_browsing", "standard_enhancements_catalog", "catalog_feed_tag",
                    "product_metadata_automation", "dynamic_partner_content"}
COPY_CHANGING = {"text_optimizations", "add_text_overlay", "description_automation", "generate_cta",
                 "enhance_cta", "advantage_plus_creative", "video_voiceover", "image_background_gen"}
# Opt-ins that mean nothing on their own or that Shawal treats as defaults.
IGNORE_FEATURES = {"standard_enhancements"}           # legacy flag, the API rejects setting it
NOTE_ONLY = {"translate_voiceover"}                    # Ads Manager default on ~half of all ads

LINK_IN_BIO = re.compile(r"\blink in (?:our |my )?bio\b", re.I)
NEUTRAL_HOSTS = ("instagram.com", "facebook.com", "fb.me", "m.me", "linktr.ee", "wa.me", "whatsapp.com")

# per-run caches (the module is imported once per daily.py run)
_account, _adsets, _camp_spend, _adset_spend, _pixel_hosts, _catalog = {}, {}, {}, {}, {}, {}
_domains = None


# ---------------- helpers ----------------
def _safe(fn, default):
    try:
        return fn()
    except Exception:
        if os.environ.get("AD_SETTINGS_DEBUG"):
            raise
        return default


def _host(url):
    try:
        h = urlparse(url if "//" in url else "https://" + url).hostname or ""
    except Exception:
        return ""
    return h.lower()[4:] if h.lower().startswith("www.") else h.lower()


def _root(host):
    parts = host.split(".")
    if len(parts) >= 3 and parts[-2] in ("co", "com", "org", "net") and len(parts[-1]) == 2:
        return ".".join(parts[-3:])
    return ".".join(parts[-2:])


def _feat_label(k):
    return FEATURE_LABELS.get(k, k.replace("_", " "))


def _join(items):
    items = list(items)
    if len(items) <= 1:
        return "".join(items)
    return ", ".join(items[:-1]) + " and " + items[-1]


def _usd(cents):
    return "${:,.2f}".format((cents or 0) / 100.0)


def _not_hg(act, campaign_name):
    if NOT_HG_ANY_ACCOUNT.search(campaign_name or ""):
        return True
    rx = NOT_HG_CAMPAIGNS.get(act)
    return bool(rx and rx.search(campaign_name or ""))


def _expected_domains():
    """account id -> set of root domains the client owns, and root domain -> clients (for other-client links)."""
    global _domains
    if _domains is not None:
        return _domains
    acct_client = {}
    files = sorted(glob.glob(os.path.join(REPO, "weekly", "Ad Spends Checks", "Weekly Checks", "*-ad-spend-check.csv")))
    if files:
        for r in csv.DictReader(open(files[-1], encoding="utf-8")):
            acct_client["act_" + r["ad_account_id"].strip()] = r["client"].strip()
    client_roots, root_clients = defaultdict(set), defaultdict(set)
    path = os.path.join(REPO, "weekly", "Meta Pixel Reviews", "expected-domains.csv")
    if os.path.exists(path):
        for r in csv.DictReader(open(path, encoding="utf-8")):
            client = r["client"].strip()
            for d in (r.get("expected_domains") or "").split("|") + (r.get("accepted_extra_hosts") or "").split("|"):
                d = d.strip().lower()
                if d and "." in d and not d.startswith("127.") and not any(d.endswith(n) for n in NEUTRAL_HOSTS):
                    client_roots[client].add(_root(d))
                    if d in (r.get("expected_domains") or "").lower().split("|"):
                        root_clients[_root(d)].add(client)
    _domains = (acct_client, client_roots, root_clients)
    return _domains


def _finding(ad, kind, severity, detail, adset_name=None):
    return {"ad_id": ad["id"], "ad": ad.get("name", ""), "campaign": (ad.get("campaign") or {}).get("name", ""),
            "adset": adset_name if adset_name is not None else (ad.get("adset") or {}).get("name", ""),
            "kind": kind, "severity": severity, "detail": detail}


# ---------------- account reads (cached) ----------------
def _account_info(act, get):
    if act not in _account:
        _account[act] = _safe(lambda: get(act, {"fields": "name,business{id,name}"}), {})
    return _account[act]


def _account_adsets(act, get_all):
    if act not in _adsets:
        _adsets[act] = _safe(lambda: get_all(f"{act}/adsets", {
            "fields": "id,name,campaign_id,campaign{name},status,effective_status,created_time,start_time,end_time,"
                      "targeting,promoted_object", "limit": 200}), [])
    return _adsets[act]


def _lifetime_spend(obj_id, cache, get):
    """Lifetime spend in cents, or None when the read fails."""
    if obj_id not in cache:
        def read():
            r = get(f"{obj_id}/insights", {"fields": "spend", "date_preset": "maximum"})
            rows = r.get("data", []) if isinstance(r, dict) else r
            return int(round(sum(float(x.get("spend", 0) or 0) for x in rows) * 100))
        cache[obj_id] = _safe(read, None)
    return cache[obj_id]


def _pixel_host_share(pixel_id, get):
    """{host: events} over the last 7 days for one pixel (single request, buckets summed)."""
    if pixel_id not in _pixel_hosts:
        def read():
            now = int(time.time())
            r = get(f"{pixel_id}/stats", {"aggregation": "host", "start_time": now - 7 * 86400, "end_time": now})
            tot = defaultdict(int)
            for b in (r.get("data", []) if isinstance(r, dict) else r):
                for x in b.get("data", []):
                    tot[_host(x.get("value", ""))] += int(x.get("count", 0) or 0)
            return dict(tot)
        _pixel_hosts[pixel_id] = _safe(read, None)
    return _pixel_hosts[pixel_id]


def _catalog_info(cat_id, get):
    if cat_id not in _catalog:
        _catalog[cat_id] = _safe(lambda: get(cat_id, {"fields": "name,product_count,business{id,name}"}), {})
    return _catalog[cat_id]


def _countries(targeting):
    g = (targeting or {}).get("geo_locations") or {}
    out = set(g.get("countries") or [])
    for k in ("regions", "cities", "zips", "geo_markets", "subcities", "neighborhoods", "places"):
        for x in g.get(k) or []:
            if x.get("country"):
                out.add(x["country"])
            elif x.get("country_code"):
                out.add(x["country_code"])
    return out


def _geo_label(targeting):
    g = (targeting or {}).get("geo_locations") or {}
    names = [_cn(c) for c in (g.get("countries") or [])]
    names += [x.get("name", "") for x in (g.get("regions") or [])]
    names += [x.get("name", "") for x in (g.get("cities") or [])]
    names = [n for n in names if n]
    return _join(names[:5]) + (" and more" if len(names) > 5 else "") if names else "no locations"


COUNTRY_NAMES = {"US": "the US", "CA": "Canada", "HN": "Honduras", "MX": "Mexico", "GB": "the UK", "CR": "Costa Rica",
                 "BZ": "Belize", "DO": "the Dominican Republic", "JM": "Jamaica", "BS": "the Bahamas", "PR": "Puerto Rico"}


def _cn(code):
    return COUNTRY_NAMES.get(code, code)


# ---------------- creative checks (per ad, grouped per ad set) ----------------
def _creative_findings(act, ads, get):
    acct = _account_info(act, get)
    acct_biz = ((acct.get("business") or {}).get("id")) or ""
    acct_client, client_roots, root_clients = _expected_domains()
    client = acct_client.get(act)
    own_roots = client_roots.get(client, set()) if client else set()

    grouped = defaultdict(list)      # (adset_id, kind, severity, detail) -> ads
    for ad in ads:
        cr = ad.get("creative") or {}
        adset_id = (ad.get("adset") or {}).get("id", "")

        def add(kind, sev, detail):
            grouped[(adset_id, kind, sev, detail)].append(ad)

        # enhancements
        feats = ((cr.get("degrees_of_freedom_spec") or {}).get("creative_features_spec") or {})
        opted = sorted(k for k, v in feats.items() if (v or {}).get("enroll_status") == "OPT_IN" and k not in IGNORE_FEATURES)
        prod = [k for k in opted if k in PRODUCT_FEATURES]
        copy_change = [k for k in opted if k in COPY_CHANGING]
        css = cr.get("creative_sourcing_spec") or {}
        rest = [k for k in opted if k not in PRODUCT_FEATURES and k not in COPY_CHANGING
                and not (k == "site_extensions" and css.get("site_links_spec"))]   # reported as SITE_LINKS below
        if prod:
            add("PRODUCT_ADDITIONS", "warning",
                "Product additions are on ({}); turn them off in the ad under Ad creative, catalog items.".format(
                    _join(_feat_label(k) for k in prod)))
        if copy_change:
            add("ENHANCEMENTS", "warning",
                "Enhancements that change the ad's wording or look are on ({}); turn them off in the ad under "
                "Advantage+ creative.".format(_join(sorted({_feat_label(k) for k in copy_change}))))
        if rest:
            add("ENHANCEMENTS", "note",
                "Enhancements are on ({}); turn them off in the ad under Advantage+ creative if they should be off.".format(
                    _join(sorted({_feat_label(k) for k in rest}))))

        links = [x.get("site_link_title", "") for x in (css.get("site_links_spec") or [])]
        if links:
            shown = ['"{}"'.format(t) for t in links[:4]]
            listed = ", ".join(shown) + (" and {} more".format(len(links) - 4) if len(links) > 4 else "")
            if len(links) <= 4:
                listed = _join(shown)
            add("SITE_LINKS", "note", "{} site link{} ({}) show under the ad; remove them in the ad under Site links.".format(
                len(links), "" if len(links) == 1 else "s", listed))
        if ((css.get("destination_screenshot_spec") or {}).get("enroll_status")) == "OPT_IN":
            add("DESTINATION_SCREENSHOT", "note",
                "A screenshot of the landing page is added to the ad; turn off the destination screenshot enhancement.")
        if ((cr.get("contextual_multi_ads") or {}).get("enroll_status")) == "OPT_IN":
            add("MULTI_ADVERTISER", "warning",
                "Multi-advertiser ads is on, so the ad can show next to other businesses' ads; untick it at the "
                "bottom of the ad setup.")

        # catalog carried by the promo-code metadata (or a product set)
        afs = cr.get("asset_feed_spec") or {}
        cat_ids = set()
        pm = afs.get("promotional_metadata") or {}
        if pm.get("product_catalog_id"):
            cat_ids.add(str(pm["product_catalog_id"]))
        for cid in cat_ids:
            info = _catalog_info(cid, get)
            biz = info.get("business") or {}
            name = info.get("name") or cid
            if biz.get("id") and acct_biz and biz["id"] != acct_biz and biz["id"] != HG_BUSINESS_ID:
                add("OTHER_CLIENT_CATALOG", "urgent",
                    'The ad carries the catalog "{}" owned by the business "{}", not this client\'s; remove the promo '
                    "code or catalog setting in the ad (or rebuild the ad without it).".format(name, biz.get("name", biz["id"])))
            else:
                add("PROMO_CATALOG", "note",
                    'A product catalog ("{}") is attached through the promo-code setting; remove it if no products '
                    "should show.".format(name))

        # copy: link in bio
        oss = cr.get("object_story_spec") or {}
        data = oss.get("video_data") or oss.get("link_data") or {}
        texts = [data.get("message"), data.get("title"), data.get("name"), data.get("link_description"),
                 data.get("description"), cr.get("body"), cr.get("title")]
        texts += [t.get("text") for k in ("bodies", "titles", "descriptions") for t in (afs.get(k) or [])]
        if any(t and LINK_IN_BIO.search(t) for t in texts):
            add("LINK_IN_BIO", "warning",
                'The ad copy says "link in bio", but an ad has no bio; point people to the button instead '
                '(for example "Tap Book now").')

        # link domain: another client's domain is urgent
        cta = data.get("call_to_action") or {}
        link = ((cta.get("value") or {}).get("link")) or data.get("link") or ""
        for u in afs.get("link_urls") or []:
            link = link or u.get("website_url", "")
        host = _host(link)
        if host and not any(host.endswith(n) for n in NEUTRAL_HOSTS):
            root = _root(host)
            owners = root_clients.get(root, set())
            if client and owners and client not in owners and root not in own_roots:
                add("LINK_OTHER_CLIENT", "urgent",
                    "The ad links to {}, which is {}'s domain, not this client's; fix the website URL in the ad.".format(
                        host, _join(sorted(owners))))

    out = []
    for (adset_id, kind, sev, detail), group in grouped.items():
        rep = group[0]
        n = len({a["id"] for a in group})
        suffix = " ({} ad{} in this ad set.)".format(n, "" if n == 1 else "s") if n > 1 else ""
        f = _finding(rep, kind, sev, detail.rstrip(".") + "." + suffix if suffix else detail)
        f["ad_ids"] = sorted({a["id"] for a in group})
        out.append(f)
    return out


# ---------------- ad set and campaign checks ----------------
def _delivery_findings(act, ads, get, get_all):
    out = []
    all_sets = _account_adsets(act, get_all)
    by_campaign = defaultdict(list)
    for s in all_sets:
        by_campaign[s.get("campaign_id")].append(s)
    rep_for_campaign, rep_for_adset = {}, {}
    for a in ads:
        c, s = a.get("campaign") or {}, a.get("adset") or {}
        if c.get("id") and not _not_hg(act, c.get("name")):
            rep_for_campaign.setdefault(c["id"], a)
            if s.get("id"):
                rep_for_adset.setdefault(s["id"], a)

    now = time.time()
    for cid, rep in rep_for_campaign.items():
        camp = rep.get("campaign") or {}
        if camp.get("effective_status") != "ACTIVE":
            continue
        sets = by_campaign.get(cid, [])
        running = [s for s in sets if s.get("effective_status") == "ACTIVE"]
        if sets and not running:
            spend = _lifetime_spend(cid, _camp_spend, get)
            names = (_join('"{}"'.format(s.get("name", "")) for s in sets) if len(sets) <= 3 else
                     ", ".join('"{}"'.format(s.get("name", "")) for s in sets[:3]) + " and {} more".format(len(sets) - 3))
            never = spend == 0
            out.append(_finding(rep, "CAMPAIGN_NOT_DELIVERING", "urgent" if never or spend is None else "warning",
                                'Campaign "{}" is on, but its ad set{} {} {} paused, so none of its ads are running{}; '
                                "switch the ad set on in Ads Manager if it should be live{}.".format(
                                    camp.get("name", ""), "" if len(sets) == 1 else "s", names,
                                    "is" if len(sets) == 1 else "are all",
                                    " and it has never spent" if never else
                                    (" ({} spent before it was paused)".format(_usd(spend)) if spend else ""),
                                    "" if never else ", or ignore this if the pause is on purpose"),
                                adset_name=", ".join(s.get("name", "") for s in sets)))
            continue
        # active ad sets that have never spent although they are more than two days old
        for s in running:
            if s["id"] not in rep_for_adset:
                continue
            try:
                created = time.mktime(time.strptime(s["created_time"][:19], "%Y-%m-%dT%H:%M:%S"))
            except Exception:
                continue
            if now - created < 2 * 86400:
                continue
            try:
                if s.get("start_time") and time.mktime(time.strptime(s["start_time"][:19], "%Y-%m-%dT%H:%M:%S")) > now - 86400:
                    continue          # scheduled to start later, or started in the last day
            except Exception:
                pass
            spend = _lifetime_spend(s["id"], _adset_spend, get)
            if spend == 0:
                out.append(_finding(rep_for_adset[s["id"]], "ADSET_NO_SPEND", "urgent",
                                    'Ad set "{}" is on but has spent $0 since it was created on {}; check its delivery '
                                    "column in Ads Manager (audience too small, ads in review or rejected, or a payment "
                                    "issue).".format(s.get("name", ""), s["created_time"][:10]), adset_name=s.get("name", "")))

    # a new or edited ad sitting in a paused ad set while the campaign runs other ad sets
    for a in ads:
        c, s = a.get("campaign") or {}, a.get("adset") or {}
        if _not_hg(act, c.get("name")) or c.get("effective_status") != "ACTIVE":
            continue
        sets = by_campaign.get(c.get("id"), [])
        if s.get("effective_status") != "ACTIVE" and any(x.get("effective_status") == "ACTIVE" for x in sets) \
                and a.get("status") == "ACTIVE":
            out.append(_finding(a, "AD_IN_PAUSED_ADSET", "warning",
                                'The ad is switched on but sits in the paused ad set "{}" while the campaign runs other '
                                "ad sets, so it won't deliver; move it or switch the ad set on.".format(s.get("name", ""))))
    return out


def _targeting_findings(act, ads, get, get_all):
    out = []
    all_sets = [s for s in _account_adsets(act, get_all) if s.get("effective_status") == "ACTIVE"]
    names = {}
    for a in ads:
        s = a.get("adset") or {}
        if s.get("id") and not _not_hg(act, (a.get("campaign") or {}).get("name")):
            names.setdefault(s["id"], a)
    sets_by_id = {s["id"]: s for s in _account_adsets(act, get_all)}
    acct_client, _, _ = _expected_domains()
    client_known = act in acct_client

    for sid, rep in names.items():
        s = sets_by_id.get(sid)
        if not s:
            continue
        t = s.get("targeting") or {}
        # Advantage+ audience on a retargeting ad set: deferred decision (12 Nov), a note only
        ca = [x.get("name", "") for x in (t.get("custom_audiences") or [])]
        aa = ((t.get("targeting_automation") or {}).get("advantage_audience"))
        lookalike = any("lookalike" in n.lower() or "lal" in n.lower().split() for n in ca)
        if ca and aa == 1 and not lookalike:
            out.append(_finding(rep, "ADV_AUDIENCE_RETARGETING", "note",
                                'Advantage+ audience is on in the retargeting ad set "{}", so its audiences ({}) are only '
                                "suggestions; left on by choice on 12 Nov, so no change needed unless that's reopened.".format(
                                    s.get("name", ""), _join(ca[:3])), adset_name=s.get("name", "")))
        # geo outlier: misses a country that every other active ad set in the account targets
        others = [x for x in all_sets if x["id"] != sid and not _not_hg(act, (x.get("campaign") or {}).get("name"))]
        if len(others) >= 2 and s.get("effective_status") in ("ACTIVE", "PAUSED", "CAMPAIGN_PAUSED", "ADSET_PAUSED"):
            mine = _countries(t)
            common = None
            for x in others:
                cs = _countries(x.get("targeting"))
                common = cs if common is None else common & cs
            missing = sorted((common or set()) - mine)
            if mine and missing:
                out.append(_finding(rep, "GEO_OUTLIER", "warning",
                                    'Ad set "{}" targets {} but leaves out {}, which every other live ad set in the account '
                                    "targets; check its locations under Audience.".format(
                                        s.get("name", ""), _geo_label(t), _join(_cn(c) for c in missing)),
                                    adset_name=s.get("name", "")))
    return out


def _tracking_findings(act, ads, get, get_all):
    """Landing pages where the ad set's pixel barely fires (one pixel stats call per pixel per run)."""
    out = []
    sets_by_id = {s["id"]: s for s in _account_adsets(act, get_all)}
    seen = set()
    for a in ads:
        s = sets_by_id.get((a.get("adset") or {}).get("id"))
        px = ((s or {}).get("promoted_object") or {}).get("pixel_id")
        if not px or _not_hg(act, (a.get("campaign") or {}).get("name")):
            continue
        cr = a.get("creative") or {}
        oss = cr.get("object_story_spec") or {}
        data = oss.get("video_data") or oss.get("link_data") or {}
        link = (((data.get("call_to_action") or {}).get("value") or {}).get("link")) or data.get("link") or ""
        host = _host(link)
        if not host or any(host.endswith(n) for n in NEUTRAL_HOSTS) or (s["id"], host) in seen:
            continue
        seen.add((s["id"], host))
        hosts = _pixel_host_share(px, get)
        if not hosts:
            continue
        total = sum(hosts.values())
        here = hosts.get(host, 0)          # exact host only: go.example.com is a different page from example.com
        if total >= 200 and here <= max(2, total // 500):
            top = sorted(hosts.items(), key=lambda kv: -kv[1])[:2]
            out.append(_finding(a, "LANDING_PAGE_UNTRACKED", "warning",
                                'The ads in "{}" send people to {}, where the ad set\'s pixel logged {} event{} in 7 days '
                                "(most events come from {}); check the pixel is installed on that page or link to a "
                                "tracked page.".format(s.get("name", ""), host, here, "" if here == 1 else "s",
                                                       _join(h for h, _ in top)),
                                adset_name=s.get("name", "")))
    return out


# ---------------- entry point ----------------
def check_settings(act, ads, get, get_all):
    if not act.startswith("act_"):
        act = "act_" + act
    ads = [a for a in ads if not _not_hg(act, (a.get("campaign") or {}).get("name"))]
    if not ads:
        return []
    findings = []
    for part in (lambda: _creative_findings(act, ads, get),
                 lambda: _delivery_findings(act, ads, get, get_all),
                 lambda: _targeting_findings(act, ads, get, get_all),
                 lambda: _tracking_findings(act, ads, get, get_all)):
        findings += _safe(part, [])
    order = {"urgent": 0, "warning": 1, "note": 2}
    findings.sort(key=lambda f: (order.get(f["severity"], 9), f["kind"], f["adset"]))
    return findings
