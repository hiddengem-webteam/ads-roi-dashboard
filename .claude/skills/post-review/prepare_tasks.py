"""Turn the post-review's new tasks into Meta Ads Fix List documents (2026-11-16, Shawal).

  python3 .claude/skills/post-review/prepare_tasks.py YYYY-MM-DD

Reads  weekly/Post-Review/Weekly Checks/DATE-post-review.json   ("new_tasks", item "tasks" ids)
       weekly/Post-Review/inputs/fixlist/{tasks,accounts}/*.json  (this run's Fix List dump)
       .claude/skills/post-review/{ads.json,crm.json}
Writes weekly/Post-Review/inputs/DATE-fixlist/tasks/<id>.json and accounts/<slug>.json (one document per file)
       weekly/Post-Review/inputs/DATE-fixlist/writes.json  -> pass as `writes` to ArtifactData action "batch"
       and fills "task_index" and "tasks_added" in the post-review JSON, so the page and the email can show
       each linked task's text and whether it is new, open or done.
A new task whose id is already on the Fix List is skipped (the existing one is linked instead). A task for a
client with no accounts document gets one, so it does not sort last on the Fix List page.
"""
import json, glob, os, re, sys, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
DATE = sys.argv[1] if len(sys.argv) > 1 else datetime.date.today().isoformat()
PR = f"{REPO}/weekly/Post-Review/Weekly Checks/{DATE}-post-review.json"
DUMP = f"{REPO}/weekly/Post-Review/inputs/fixlist"
OUT = f"{REPO}/weekly/Post-Review/inputs/{DATE}-fixlist"
PRIORITIES = {"fix", "followup", "structure", "confirm", "minor", "tidy", "deferred"}

def norm(s): return re.sub(r"[^a-z0-9]", "", (s or "").lower().replace("à", "a").replace("á", "a"))
def slug(s): return re.sub(r"[^a-z0-9]+", "-", (s or "").lower().replace("&", " ").replace("à", "a").replace("á", "a")).strip("-")
def load(p):
    d = json.load(open(p, encoding="utf-8")); d = d.get("data", d); d["_id"] = os.path.splitext(os.path.basename(p))[0]; return d

pr = json.load(open(PR, encoding="utf-8"))
tasks = {t["_id"]: t for t in map(load, glob.glob(f"{DUMP}/tasks/*.json"))}
accounts = [load(p) for p in glob.glob(f"{DUMP}/accounts/*.json")]
known = {norm(n) for a in accounts for n in [a.get("name", "")] + list(a.get("aliases") or [])}
ads = json.load(open(f"{HERE}/ads.json", encoding="utf-8"))["accounts"]
ads_by = {norm(k): v for k, v in ads.items()}
crm_raw = json.load(open(f"{HERE}/crm.json", encoding="utf-8"))
crm = {norm(r[0]): dict(zip(crm_raw["cols"], r)) for r in crm_raw["rows"]}

os.makedirs(f"{OUT}/tasks", exist_ok=True); os.makedirs(f"{OUT}/accounts", exist_ok=True)
for f in glob.glob(f"{OUT}/*/*.json"): os.remove(f)
writes, added, skipped, new_accounts = [], [], [], []
order = max([int(t.get("order") or 0) for t in tasks.values()] + [0])
now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
for t in pr.get("new_tasks", []):
    tid = t["id"]
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{1,80}", tid): sys.exit(f"bad task id {tid!r}: lowercase letters, digits and hyphens")
    if t.get("priority") not in PRIORITIES: sys.exit(f"{tid}: priority must be one of {sorted(PRIORITIES)}")
    if tid in tasks: skipped.append(tid); continue
    order += 1
    doc = {k: t[k] for k in ("account", "priority", "change", "where", "note", "tag", "tone") if t.get(k)}
    doc.update({"order": order, "done": False, "source": f"post-review-{DATE}", "createdAt": now, "createdBy": None})
    p = f"{OUT}/tasks/{tid}.json"; json.dump(doc, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    writes.append({"op": "set", "collection": "tasks", "doc_id": tid, "file_path": p}); added.append(tid)
    tasks[tid] = {**doc, "_id": tid}
    k = norm(t["account"])
    if k not in known:
        a = ads_by.get(k); c = crm.get(k, {})
        spend30 = round(sum((x.get("w30") or {}).get("spend", 0) for x in a["ads"]), 2) if a else 0
        acc = {"name": t["account"], "advanced": (c.get("meta_ads") or c.get("setup") or "").lower() == "advanced", "am": c.get("am", ""),
               "adAccount": f"act_{a['id']}" if a else "", "spend30": spend30, "spendAsOf": DATE, "aliases": []}
        if not a: acc["spendNote"] = "no ad account mapped yet"
        sid = slug(t["account"]); p = f"{OUT}/accounts/{sid}.json"; json.dump(acc, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        writes.append({"op": "set", "collection": "accounts", "doc_id": sid, "file_path": p}); new_accounts.append(sid); known.add(k)

# every task id the page or the email names
ref = set()
for items in pr.get("sections", {}).values():
    for it in items: ref.update(it.get("tasks", []))
ref.update(t["task"] for t in pr.get("top_actions", []) if t.get("task"))
missing = sorted(r for r in ref if r not in tasks)
pr["task_index"] = {r: {k: tasks[r].get(k) for k in ("account", "priority", "change", "done", "source")} for r in sorted(ref) if r in tasks}
pr["tasks_added"] = added
json.dump(pr, open(PR, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(writes, open(f"{OUT}/writes.json", "w", encoding="utf-8"), indent=1)
print(f"{len(added)} new tasks, {len(new_accounts)} new accounts docs, {len(skipped)} already on the Fix List ({', '.join(skipped) or 'none'}); "
      f"{len(pr['task_index'])} task ids linked{'; MISSING ids: ' + ', '.join(missing) if missing else ''}")
print(f"writes for ArtifactData batch: {os.path.relpath(OUT, REPO)}/writes.json ({len(writes)} entries)")
