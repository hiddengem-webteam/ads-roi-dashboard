"""Purchase check rules shared by events_snapshot.py (ad-hoc) and write_report.py (weekly).

judge(m) takes the primary pixel's metrics for one client and returns (flag, notes):
  m = dict(live=bool, status=str, total_live=float, sales_budget=float,
           p28=int, p28_b=int, p28_s=int, p7=int, p_last=str,
           pms_online28=int|None, pms_direct28=int|None)
flag is one of "n/a", "ok", "warning", "critical".

Rules (2026-10-30):
  n/a       client Not Live on the sheet, or $0/day live
  capture   = Purchase 28d / PMS online bookings 28d (manual, owner, phone, walk-in excluded)
  effective = max(browser, server) Purchase; Meta deduplicates browser+server pairs with the same
              event_id, so the pair is counted once for the over-count test
  critical  Sales budget and: zero Purchase while the PMS has online bookings, or capture < 25%,
            or (Purchase < 5 and capture < 50%)
  warning   zero Purchase (no Sales budget, or no bookings to capture); Purchase < 5 with a Sales budget;
            capture < 50%; effective > 1.5x PMS direct bookings (over-count); 0 Purchase in 7d after
            >= 3 in the prior 21 days (stopped)
  ok        otherwise
A note (no flag) is added when Purchase exceeds 1.5x the online bookings but fits within all direct
bookings: the sender (usually the HG AI CAPI) is sending manual and owner entries as Purchase.
Capture and over-count are judged only when the PMS shows at least 5 online / direct bookings.
"""
MIN_PURCHASE_28D = 5
CAPTURE_CRIT, CAPTURE_WARN, OVERCOUNT = 0.25, 0.50, 1.5
MIN_PMS = 5
ORDER = ["ok", "warning", "critical"]

def judge(m):
    if not m["live"]:
        return "n/a", [f"{m['status']}, ${m['total_live']:.0f}/day live; {m['p28']} Purchase in 28d, not judged"]
    n, sales = m["p28"], m["sales_budget"] > 0
    online, direct = m.get("pms_online28"), m.get("pms_direct28")
    flag, notes = "ok", []
    def raise_to(f):
        nonlocal flag
        if ORDER.index(f) > ORDER.index(flag): flag = f
    cap = None
    if online is not None and online >= MIN_PMS:
        cap = n / online
        if sales and cap < CAPTURE_CRIT: raise_to("critical"); notes.append(f"captures {cap:.0%} of {online} PMS online bookings")
        elif cap < CAPTURE_WARN: raise_to("warning"); notes.append(f"captures {cap:.0%} of {online} PMS online bookings")
        else: notes.append(f"{cap:.0%} of {online} PMS online bookings")
    elif online is not None:
        notes.append(f"PMS shows only {online} online bookings, capture not judged")
    else:
        notes.append("no PMS data in the platform")
    if direct is not None and direct >= MIN_PMS:
        eff = max(m["p28_b"], m["p28_s"])
        if eff > OVERCOUNT * direct:
            raise_to("warning"); notes.append(f"over-count: {eff} {'browser' if m['p28_b'] >= m['p28_s'] else 'server'} Purchase vs {direct} PMS direct bookings ({eff/direct:.1f}x)")
        elif online is not None and online >= MIN_PMS and eff > OVERCOUNT * online and direct > online:
            notes.append(f"above the {online} online bookings but within the {direct} direct bookings: the CAPI is sending manual/owner entries as Purchase too (no ad could have driven those)")
    if n == 0:
        if sales and (online or 0) >= 1: raise_to("critical")
        else: raise_to("warning")
        notes.insert(0, "ZERO Purchase in 28d" + ("" if online is None or online else ", PMS has no online bookings either"))
    elif n < MIN_PURCHASE_28D and sales:
        raise_to("critical" if (cap is not None and cap < CAPTURE_WARN) else "warning")
        notes.insert(0, f"only {n} Purchase in 28d with ${m['sales_budget']:.0f}/day on Sales")
    if m["p7"] == 0 and n >= 3:
        raise_to("warning"); notes.append(f"stopped: 0 in the last 7d, last on {m['p_last']}")
    if n and m["p28_b"] == 0: notes.append("all server-side, browser never fires Purchase")
    if n and m["p28_s"] == 0: notes.append("all browser-side, no server Purchase")
    return flag, notes
