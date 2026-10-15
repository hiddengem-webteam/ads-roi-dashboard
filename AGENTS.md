<!-- BEGIN:nextjs-agent-rules -->
# This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` before writing any code. Heed deprecation notices.
<!-- END:nextjs-agent-rules -->

# Where past numbers and decisions live

When asked about a previous month's figures, a client's history, or why something was decided, query the `roi` schema in the HGM Reporting Supabase project (`ytewxihtllthqkvnmlex`) before re-reading files: `roi.monthly_client_metrics` (finalized months per client), `roi.weekly_*` (Monday review rows), `roi.decisions`, `roi.actions_log`, `roi.run_log`, and `roi.notes` (AM notes, HG AI diagnoses, full weekly reports; full-text via `body_tsv`). It is loaded from this repo by `scripts/sync-roi-memory.mts`; if a table looks stale, run that first. Live PMS and Meta data stay in the HiddenGem AI project (`ahpzvyhrnvzetpygujws`).

Finalized months (frozen snapshot + Client Performance Tracking sheet figures) are listed in `src/lib/analysis/finalizedPeriods.ts`; the main dashboard renders those from their snapshot. Add a month there when it is signed off.
