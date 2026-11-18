#!/usr/bin/env python3
"""Read-only typo and consistency check for the live ads in Meta ad accounts.

Built on 2026-11-18 after "PRSERVE150" (headline) shipped next to "PRESERVE150"
(video and primary text) on The Preserve's retargeting ads. It never writes to Meta.

Usage (from the repo root):
  python3 -I scripts/ad-copy-check/check.py --out <dir> act_123:"Client Name" [act_456:"Other Client" ...]
  add --no-video to skip the on-screen text pass (faster, no downloads)

What it flags, per live ad (campaign, ad set and ad all active):
  CODE_NEAR_MISS   a promo code one or two letters off another code (PRSERVE150 vs PRESERVE150, VIP00 vs VIP100)
  CODE_MISMATCH    headline, text, description and video don't name the same code
  CODE_NOT_IN_LIST code not in data/promo-codes.csv for the client (info: the sheet is incomplete)
  SPELLING         lowercase word not in the dictionary but one letter off a real word; or a capitalised
                   word one letter off a brand term used elsewhere in the account
  PLACEHOLDER      [brackets], {{tokens}} in copy, TBD/XXX/lorem, "WordTM" instead of a trademark sign
  FORMAT           double spaces, space before punctuation, repeated words
  AMOUNT_MISMATCH  headline and text give different $ or % amounts
  HANDLE           @handle in copy that isn't an Instagram account used by the ads
  IDENTITY         ad posts from an Instagram account or Page that differs from the rest of the account
  SWAPPED_TEXT     description is long and longer than the primary text (likely swapped fields)
  NO_UTM           creative has no url_tags
  VIDEO_*          the same code / spelling checks on the video's on-screen text (OCR, check frames by eye:
                   script fonts misread, e.g. "luxury" -> "huxury")
Output: <out>/<account>.json and <out>/report.md
"""
import argparse, csv, json, os, re, subprocess, sys, time, urllib.parse, urllib.request
from collections import Counter, defaultdict

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
API = "https://graph.facebook.com/v21.0/"
OCR_BIN = os.path.expanduser("~/.local/bin/hg-vision-ocr")
LIVE_AD = {"ACTIVE", "IN_PROCESS", "PENDING_REVIEW", "WITH_ISSUES", "PREAPPROVED"}
CR_FIELDS = ("id,name,object_story_spec,asset_feed_spec,url_tags,title,body,"
             "instagram_user_id,effective_object_story_id")

def env_value(name):
    """Environment first (GitHub Actions secrets), then the repo-root .env.local / .env."""
    if os.environ.get(name):
        return os.environ[name]
    for f in (".env.local", ".env"):
        path = os.path.join(REPO, f)
        if os.path.exists(path):
            m = re.search(r'^' + re.escape(name) + r'=(.+)$', open(path, encoding="utf-8").read(), re.M)
            if m:
                return m.group(1).strip().strip('"')
    return None

def token():
    t = env_value("META_ACCESS_TOKEN")
    if not t:
        raise SystemExit("META_ACCESS_TOKEN is not set")
    return t

TOKEN = None
def get(path, params=None, tries=8):
    params = dict(params or {}, access_token=TOKEN)
    url = path if path.startswith("http") else API + path + "?" + urllib.parse.urlencode(params)
    for i in range(tries):
        try:
            return json.load(urllib.request.urlopen(url, timeout=120))
        except urllib.error.HTTPError as e:
            body = json.load(e)
            err = body.get("error", {})
            if err.get("code") in (17, 4, 80004, 613) or err.get("error_subcode") == 2446079:
                wait = 60
                try:
                    usage = json.loads(e.headers.get("x-business-use-case-usage") or "{}")
                    for v in usage.values():
                        wait = max(wait, 60 * int(v[0].get("estimated_time_to_regain_access", 1)))
                except Exception:
                    pass
                print(f"   rate limited, waiting {wait}s", file=sys.stderr, flush=True)
                time.sleep(min(wait, 600))
                continue
            raise RuntimeError(json.dumps(err)[:400])
    raise RuntimeError("gave up after rate limits")

def get_all(path, params):
    out, r = [], get(path, params)
    while True:
        out += r.get("data", [])
        nxt = r.get("paging", {}).get("next")
        if not nxt:
            return out
        r = get(nxt)

# ---------- text helpers ----------
def _load_words():
    for path in (os.environ.get("DICT_PATH"), "/usr/share/dict/words", "/usr/share/dict/american-english-large",
                 "/usr/share/dict/american-english"):
        if path and os.path.exists(path):
            return set(w.strip().lower() for w in open(path, encoding="utf-8", errors="ignore"))
    print("   no word list found: spelling rules off", file=sys.stderr)
    return set()
WORDS = _load_words()
COMMON_OK = set("""email emails inbox wifi airbnb vrbo pov getaway getaways cozy favorite favorites hottub
hottubs jacuzzi glamping treehouse treehouses ebike ebikes instagram tiktok facebook youtube online
dm dms bnb bnbs vibe vibes staycation booking bookings booked rebook checkout checkin weekender
lakefront lakeside riverfront oceanfront mountainside hillside fireside firepit firepits sauna
saunas spa spas kayak kayaks kayaking paddleboard paddleboards hiking biking skiing snowshoeing
wineries brewery breweries lol omg wow okay ok ai app apps website websites url signup sign
fall's winter's today's tonight's mini minis saltwater oceanview
starlink pickleball cornhole smores s'mores
paid said made went gone took taken gave given felt kept left met sent spent built bought brought caught taught thought found held led slept knew known grew grown drew drawn flew flown threw thrown wrote written ate eaten saw seen began begun chose chosen drove driven rode ridden rose risen woke woken wore worn stood understood sold told won sang sung swam swum sat lit hid hidden forgot forgotten became came ran lay laid slid spun stuck struck hung dug fed fled sped
feet teeth geese children women men mice skyline skylines waterslide waterslides glamp glamps firepit lakehouse treetop treetops sunset sunsets""".split())
SUFFIXES = ["s", "es", "ed", "d", "ing", "ly", "er", "ers", "est"]

CONTRACTIONS = ("'s", "'d", "'re", "'ll", "'ve", "'m", "n't")
BRAND_TERMS = set()   # filled per account: words the account's copy capitalises (Hobbit, Preserve, ...)

def stems(wl):
    yield wl
    for s in SUFFIXES:
        if wl.endswith(s) and len(wl) - len(s) >= 3:
            base = wl[:-len(s)]
            yield base
            yield base + "e"                      # hiking -> hike
            if len(base) >= 4 and base[-1] == base[-2]:
                yield base[:-1]                   # planning -> plan, sipping -> sip
    for s, r in (("ies", "y"), ("ied", "y"), ("ier", "y"), ("iest", "y"), ("ily", "y")):
        if wl.endswith(s):
            yield wl[:-len(s)] + r                # stories -> story, memories -> memory

def in_dict(w):
    wl = w.lower().replace("’", "'").strip("'")
    for c in CONTRACTIONS:
        if wl.endswith(c):
            wl = wl[:-len(c)]
            break
    if len(wl) < 4 or wl in COMMON_OK or wl in BRAND_TERMS or not WORDS:
        return True
    return any(s in WORDS or s in COMMON_OK for s in stems(wl))

def lev(a, b, cap=3):
    if abs(len(a) - len(b)) > cap:
        return cap + 1
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]

_near_cache = {}
def near_dict(w):
    """A dictionary word one edit away (cheap candidate generation)."""
    wl = w.lower()
    if wl in _near_cache:
        return _near_cache[wl]
    letters = "abcdefghijklmnopqrstuvwxyz"
    splits = [(wl[:i], wl[i:]) for i in range(len(wl) + 1)]
    cands = set()
    for L, R in splits:
        if R:
            cands.add(L + R[1:])
            for c in letters:
                cands.add(L + c + R[1:])
        if len(R) > 1:
            cands.add(L + R[1] + R[0] + R[2:])
        for c in letters:
            cands.add(L + c + R)
    hit = sorted(c for c in cands if len(c) >= 4 and any(s in WORDS for s in stems(c)))
    _near_cache[wl] = hit[0] if hit else None
    return _near_cache[wl]

CODE_RE = re.compile(r"\b([A-Z][A-Z]{1,}[A-Z0-9]*\d[A-Z0-9]*)\b")
AMOUNT_RE = re.compile(r"\$\s?\d[\d,]*|\b\d{1,3}\s?%")
HANDLE_RE = re.compile(r"(?<![\w.])@([A-Za-z0-9_.]{3,30}[A-Za-z0-9_])")
WORD_RE = re.compile(r"[A-Za-z][A-Za-z'’]+")

def codes_in(t):
    return [c for c in CODE_RE.findall(t or "") if not re.fullmatch(r"\d+[A-Z]*|[A-Z]{1,2}\d{2,}[A-Z]?", c)
            or c.startswith("VIP")]

def placeholders(t):
    hits = re.findall(r"\[[^\]]{1,40}\]|\{\{[^}]*\}\}|\bTBD\b|\bXXX+\b|\blorem\b|\b[A-Za-z]{3,}TM\b", t or "", re.I)
    return [h for h in hits if not re.fullmatch(r"\[\s*\]", h)]

def format_issues(t):
    out = []
    for line in (t or "").split("\n"):
        core = line.strip()
        if re.search(r"\S {2,}\S", core):
            out.append("double space: " + repr(re.search(r".{0,20}\S {2,}\S.{0,20}", core).group(0)))
        m = re.search(r"\w \s*([,.!?;:])(?=\s|$)", core)
        if m and not re.search(r"\.\.\.", core):
            out.append("space before punctuation: " + repr(core[max(0, m.start() - 15):m.end() + 5]))
    for m in re.finditer(r"\b(\w{2,})\s+\1\b", t or "", re.I):
        if m.group(1).lower() not in ("that", "had", "very", "so"):
            out.append("repeated word: " + repr(m.group(0)))
    return out

# ---------- creative parsing ----------
def parse(cr):
    oss = cr.get("object_story_spec") or {}
    vd = oss.get("video_data") or {}
    ld = oss.get("link_data") or {}
    afs = cr.get("asset_feed_spec") or {}
    d = {}
    d["titles"] = [x for x in ([vd.get("title")] if vd.get("title") else [ld.get("name")] if ld.get("name")
                   else [t.get("text", "") for t in afs.get("titles", [])]) if x]
    d["bodies"] = [x for x in ([vd.get("message")] if vd.get("message") else [ld.get("message")] if ld.get("message")
                   else [t.get("text", "") for t in afs.get("bodies", [])]) if x]
    d["descs"] = [x for x in ([vd.get("link_description")] if vd.get("link_description") else
                  [ld.get("description")] if ld.get("description") else
                  [t.get("text", "") for t in afs.get("descriptions", [])]) if x]
    cta = vd.get("call_to_action") or ld.get("call_to_action") or {}
    d["cta"] = cta.get("type") or ",".join(afs.get("call_to_action_types", []))
    d["link"] = (cta.get("value") or {}).get("link") or ld.get("link") or \
        ",".join(x.get("website_url", "") for x in afs.get("link_urls", []))
    d["videos"] = [vd["video_id"]] if vd.get("video_id") else [v.get("video_id") for v in afs.get("videos", []) if v.get("video_id")]
    d["page"] = oss.get("page_id")
    d["ig"] = oss.get("instagram_user_id") or oss.get("instagram_actor_id") or cr.get("instagram_user_id")
    d["utm"] = cr.get("url_tags")
    d["uses_existing_post"] = not oss and bool(cr.get("effective_object_story_id"))
    return d

# ---------- promo list ----------
def promo_codes():
    path = os.path.join(REPO, "data", "promo-codes.csv")
    out, cur = defaultdict(set), None
    for r in list(csv.reader(open(path, encoding="utf-8-sig")))[1:]:
        if r and r[0].strip():
            cur = r[0].strip()
        if cur and len(r) > 2 and r[2].strip():
            out[cur].add(r[2].strip().replace(" ", "").upper())
    return out

def client_codes(all_codes, client):
    key = client.lower().replace("the ", "")
    for k, v in all_codes.items():
        kk = k.lower().replace("the ", "")
        if key in kk or kk in key:
            return v
    return set()

# ---------- video OCR ----------
def ensure_ocr():
    if os.path.exists(OCR_BIN):
        return True
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ocr.swift")
    os.makedirs(os.path.dirname(OCR_BIN), exist_ok=True)
    return subprocess.run(["swiftc", "-O", src, "-o", OCR_BIN]).returncode == 0

def ocr_video(vid, cache):
    vdir = os.path.join(cache, "videos")
    fdir = os.path.join(cache, "frames", vid)
    odir = os.path.join(cache, "ocr")
    for d in (vdir, fdir, odir):
        os.makedirs(d, exist_ok=True)
    otxt = os.path.join(odir, vid + ".txt")
    if not os.path.exists(otxt):
        mp4 = os.path.join(vdir, vid + ".mp4")
        if not os.path.exists(mp4):
            src = get(vid, {"fields": "source"}).get("source")
            if not src:
                return None
            urllib.request.urlretrieve(src, mp4)
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", mp4, "-vf", "fps=4,scale=720:-2",
                        "-q:v", "3", os.path.join(fdir, "f%04d.jpg")], check=False)
        with open(otxt, "w") as fh:
            subprocess.run([OCR_BIN, fdir], stdout=fh, check=False)
    lines = []
    for l in open(otxt, encoding="utf-8"):
        if "\t" in l:
            f, t = l.rstrip("\n").split("\t", 1)
            lines.append((f, t))
    return lines

# ---------- analysis (shared with daily.py) ----------

def build_context(context_ads, client, all_codes, ig_lookup=True):
    """Account-level facts the per-ad checks compare against (built from all live ads in the account)."""
    ig_ids = Counter(a["_p"]["ig"] for a in context_ads if a["_p"]["ig"])
    pages = Counter(a["_p"]["page"] for a in context_ads if a["_p"]["page"])
    ig_names = {}
    for ig in ig_ids:
        try:
            ig_names[ig] = get(ig, {"fields": "username"}).get("username") if ig_lookup else None
        except Exception:
            ig_names[ig] = None
    vocab, codes_seen = Counter(), Counter()
    BRAND_TERMS.clear()
    for a in context_ads:
        p = a["_p"]
        for t in p["titles"] + p["bodies"] + p["descs"]:
            for w in WORD_RE.findall(t.replace("’", "'")):
                if w[0].isupper() and not in_dict(w):
                    vocab[w.lower()] += 1
    # a capitalised term used 3+ times is treated as a brand/place name; near-miss variants are still caught
    BRAND_TERMS.update(k for k, n in vocab.items() if n >= 3)
    for a in context_ads:
        p = a["_p"]
        for t in p["titles"] + p["bodies"] + p["descs"]:
            for c in codes_in(t):
                codes_seen[c] += 1
    return {"client": client, "ig_ids": ig_ids, "ig_names": ig_names,
            "known_handles": {h.lower() for h in ig_names.values() if h},
            "main_ig": ig_ids.most_common(1)[0][0] if ig_ids else None,
            "main_page": pages.most_common(1)[0][0] if pages else None,
            "vocab": vocab, "codes_seen": codes_seen, "known": client_codes(all_codes, client)}

def ocr_codes(ads, cache):
    """macOS-only on-screen text pass (Vision). Results need checking by eye: script fonts misread."""
    video_codes = {}
    vids = sorted({v for a in ads for v in a["_p"]["videos"]})
    print(f"   OCR on {len(vids)} videos", flush=True)
    for v in vids:
        try:
            lines = ocr_video(v, cache)
        except Exception as e:
            print(f"   video {v}: {e}", file=sys.stderr)
            lines = None
        if lines is None:
            continue
        frames, first = Counter(), {}
        for f, t in lines:
            frames[t.strip()] += 1
            first.setdefault(t.strip(), f)
        codes = Counter()
        for t, n in frames.items():
            # join "STAY 10" split by OCR, but not "SAVE 10%"
            for c in codes_in(re.sub(r"\b([A-Z]{3,})\s(\d{2,3})\b(?!\s?%)", r"\1\2", t)):
                codes[c] += n
        words = Counter()
        for t, n in frames.items():
            for w in WORD_RE.findall(t):
                if w.islower() and len(w) >= 4 and not in_dict(w) and near_dict(w):
                    words[(w, near_dict(w), first[t])] += n
        video_codes[v] = {"codes": dict(codes), "suspect_words": [(w, s, f, n) for (w, s, f), n in words.items() if n >= 3],
                          "frames_dir": os.path.join(cache, "frames", v)}
    return video_codes

def analyse(ads, ctx, video_codes=None):
    """Rule-based findings for each ad (each ad needs "_p" from parse(), "_campaign" and "_adset")."""
    video_codes = video_codes or {}
    client, known, all_code_seen, vocab = ctx["client"], ctx["known"], ctx["codes_seen"], ctx["vocab"]
    known_handles, ig_names, main_ig, main_page = ctx["known_handles"], ctx["ig_names"], ctx["main_ig"], ctx["main_page"]
    findings = []
    WL = {"headline": "headline", "text": "primary text", "description": "description", "video": "video"}
    WK = {"headline": "headline", "text": "primary_text", "description": "description", "video": "video"}
    def flag(a, kind, detail, sev="high", quote="", fix="", where="other"):
        # detail is one plain sentence for the email; quote/fix are the "Now" / "Should be" lines
        findings.append({"ad_id": a["id"], "ad": a["name"], "campaign": a.get("_campaign"), "adset": a.get("_adset"),
                         "kind": kind, "severity": sev, "detail": detail, "quote": quote, "fix": fix, "where": where})
    def first(where):
        for k in ("headline", "text", "description", "video"):
            if k in where:
                return k
        return "text"
    for a in ads:
        p = a["_p"]
        fields = [("headline", t) for t in p["titles"]] + [("text", t) for t in p["bodies"]] + [("description", t) for t in p["descs"]]
        # codes
        ad_codes = defaultdict(set)
        for where, t in fields:
            for c in codes_in(t):
                ad_codes[c].add(where)
        for v in p["videos"]:
            for c in (video_codes.get(v) or {}).get("codes", {}):
                ad_codes[c].add("video")
        pool = set(all_code_seen) | known
        for c, where in ad_codes.items():
            # a code on the client's list is never "the typo"; otherwise the listed or more common code wins
            near = [] if c in known else sorted(
                k for k in pool if k != c and lev(c, k) <= 2 and len(k) >= 5 and
                (k in known or all_code_seen.get(k, 0) > all_code_seen.get(c, 0)))
            if near:
                flag(a, "CODE_NEAR_MISS", f"The promo code {c} in the {' and '.join(WL[w] for w in sorted(where))} looks like a typo of {near[0]}.",
                     quote=c, fix=near[0], where=WK[first(where)])
            elif known and c not in known and "video" not in where:
                flag(a, "CODE_NOT_IN_LIST", f"{c} isn't in the promo-code list for {client} (the list has {', '.join(sorted(known))}); "
                     f"confirm the code works and add it to the list.", "info", where=WK[first(where)])
        if len(ad_codes) > 1:
            text_codes = {c for c, w in ad_codes.items() if w - {"video"}}
            if len(text_codes) > 1 or (text_codes and {c for c, w in ad_codes.items() if "video" in w} - text_codes):
                flag(a, "CODE_MISMATCH", "The ad uses more than one promo code: " +
                     "; ".join(f"{c} in the {' and '.join(WL[x] for x in sorted(w))}" for c, w in ad_codes.items()) + ".", "medium")
        # amounts
        ha = {re.sub(r"\s", "", m) for t in p["titles"] for m in AMOUNT_RE.findall(t)}
        ba = {re.sub(r"\s", "", m) for t in p["bodies"] for m in AMOUNT_RE.findall(t)}
        if ha and ba and not (ha & ba):
            flag(a, "AMOUNT_MISMATCH", f"The headline says {', '.join(sorted(ha))} but the primary text says {', '.join(sorted(ba))}.",
                 "medium", where="headline")
        # spelling, placeholders, format
        for where, t in fields:
            for w in WORD_RE.findall(t.replace("’", "'")):
                if in_dict(w):
                    continue
                if w.islower() or w.isupper() and len(w) > 3 and not CODE_RE.fullmatch(w):
                    s = near_dict(w)
                    if s:
                        flag(a, "SPELLING", f"Possible typo in the {WL[where]}.", "medium", quote=w, fix=s, where=WK[where])
                elif w[0].isupper():
                    sim = [k for k, n in vocab.items() if k != w.lower() and n > vocab[w.lower()] and lev(w.lower(), k) == 1 and len(k) >= 5]
                    if sim:
                        flag(a, "SPELLING", f"\"{w}\" in the {WL[where]} looks like a misspelling of a name used elsewhere in the account.",
                             "medium", quote=w, fix=sim[0].capitalize(), where=WK[where])
            for h in placeholders(t):
                fixed = h[1:-1] if h.startswith("[") else (h[:-2] + "™" if h.endswith("TM") else "")
                flag(a, "PLACEHOLDER", f"Template leftover in the {WL[where]}.", "medium", quote=h, fix=fixed, where=WK[where])
            for f in format_issues(t):
                flag(a, "FORMAT", f"{f.split(':')[0].capitalize()} in the {WL[where]}.", "low",
                     quote=f.split(":", 1)[1].strip().strip("'") if ":" in f else "", where=WK[where])
            for h in HANDLE_RE.findall(t):
                if known_handles and h.lower().rstrip(".") not in known_handles:
                    near = [k for k in known_handles if lev(h.lower(), k) <= 2]
                    target = near[0] if near else (ig_names.get(main_ig) or sorted(known_handles)[0])
                    flag(a, "HANDLE", f"The {WL[where]} tells people to follow @{h}, but the ads run from @{target}.",
                         "high" if near else "medium", quote=f"@{h}", fix=f"@{target}", where=WK[where])
        # identity
        if p["ig"] and main_ig and p["ig"] != main_ig:
            flag(a, "IDENTITY", f"These ads post from the Instagram account @{ig_names.get(p['ig']) or p['ig']}, not "
                 f"@{ig_names.get(main_ig) or main_ig} like the rest of the account.", "high",
                 quote=f"@{ig_names.get(p['ig']) or p['ig']}", fix=f"@{ig_names.get(main_ig) or main_ig}", where="identity")
        if p["page"] and main_page and p["page"] != main_page:
            flag(a, "IDENTITY", f"These ads post from a different Facebook Page ({p['page']}) than the rest of the account ({main_page}).",
                 "high", where="identity")
        # swapped text / utm
        b = max(p["bodies"], key=len) if p["bodies"] else ""
        dsc = max(p["descs"], key=len) if p["descs"] else ""
        if len(dsc) >= 90 and len(dsc) > len(b):
            flag(a, "SWAPPED_TEXT", f"The description ({len(dsc)} characters) is longer than the primary text ({len(b)}), so the two "
                 f"look swapped.", "medium", where="description")
        if not p["utm"] and not p["uses_existing_post"]:
            flag(a, "NO_UTM", "No tracking tags (url_tags) on the creative, so its clicks can't be told apart in reporting.", "low")
        # video spelling candidates
        for v in p["videos"]:
            for w, s, f, n in (video_codes.get(v) or {}).get("suspect_words", []):
                flag(a, "VIDEO_SPELLING?", f"on-screen '{w}' (maybe '{s}'), {n} frames; check {video_codes[v]['frames_dir']}/{f} by eye", "check")

    return findings

# ---------- per-account check ----------
def check_account(act, client, out, do_video, all_codes):
    print(f"== {client} ({act})", flush=True)
    acct = get(act, {"fields": "name,currency"})
    camps = {c["id"]: c for c in get_all(f"{act}/campaigns", {"fields": "id,name,effective_status", "limit": 200})
             if c["effective_status"] == "ACTIVE"}
    adsets = [s for s in get_all(f"{act}/adsets", {"fields": "id,name,campaign_id,effective_status", "limit": 200})
              if s["effective_status"] == "ACTIVE" and s["campaign_id"] in camps]
    ads = []
    for s in adsets:
        for a in get_all(f"{s['id']}/ads", {"fields": f"id,name,effective_status,creative{{{CR_FIELDS}}}", "limit": 100}):
            if a["effective_status"] in LIVE_AD:
                a["_adset"], a["_campaign"] = s["name"], camps[s["campaign_id"]]["name"]
                a["_p"] = parse(a.get("creative") or {})
                ads.append(a)
    print(f"   {len(camps)} live campaigns, {len(adsets)} ad sets, {len(ads)} live ads", flush=True)

    ctx = build_context(ads, client, all_codes)
    video_codes = ocr_codes(ads, os.path.join(out, "cache", act)) if do_video and ads and ensure_ocr() else {}
    findings = analyse(ads, ctx, video_codes)
    ig_ids, ig_names, all_code_seen, known = ctx["ig_ids"], ctx["ig_names"], ctx["codes_seen"], ctx["known"]

    res = {"account": act, "client": client, "account_name": acct.get("name"), "live_ads": len(ads),
           "ig_accounts": {k: ig_names.get(k) for k in ig_ids}, "codes_seen": dict(all_code_seen),
           "codes_listed": sorted(known), "video_codes": video_codes, "findings": findings,
           "ads": [{"id": a["id"], "name": a["name"], "campaign": a["_campaign"], "adset": a["_adset"],
                    "status": a["effective_status"], **{k: v for k, v in a["_p"].items()}} for a in ads]}
    json.dump(res, open(os.path.join(out, act.replace("act_", "") + ".json"), "w"), indent=1)
    return res

def report(results, out):
    order = {"high": 0, "medium": 1, "low": 2, "info": 3, "check": 4}
    lines = [f"# Ad copy check, {time.strftime('%Y-%m-%d %H:%M')}", ""]
    for r in results:
        lines.append(f"## {r['client']} ({r['account']}): {r['live_ads']} live ads")
        lines.append(f"IG accounts: {r['ig_accounts']} | codes in copy: {r['codes_seen']} | listed: {r['codes_listed']}")
        groups = defaultdict(dict)
        for f in r["findings"]:
            groups[(f["severity"], f["kind"], f["detail"])][f["ad_id"]] = f"{f['ad']} [{f['adset']}]"
        for (sev, kind, det), ids in sorted(groups.items(), key=lambda x: (order.get(x[0][0], 9), x[0][1])):
            names = list(ids.values())
            lines.append(f"- [{sev}] {kind}: {det} ({len(names)} ads: {'; '.join(names[:4])}{' …' if len(names) > 4 else ''})")
        if not r["findings"]:
            lines.append("- no findings")
        lines.append("")
    open(os.path.join(out, "report.md"), "w").write("\n".join(lines))
    print("\n".join(lines))

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("accounts", nargs="+", help='act_ID:"Client Name"')
    ap.add_argument("--out", required=True)
    ap.add_argument("--no-video", action="store_true")
    args = ap.parse_args()
    TOKEN = token()
    os.makedirs(args.out, exist_ok=True)
    codes = promo_codes()
    results = []
    for spec in args.accounts:
        act, _, client = spec.partition(":")
        act = act if act.startswith("act_") else "act_" + act
        try:
            results.append(check_account(act, client or act, args.out, not args.no_video, codes))
        except Exception as e:
            print(f"   FAILED {act}: {e}", file=sys.stderr)
    report(results, args.out)
