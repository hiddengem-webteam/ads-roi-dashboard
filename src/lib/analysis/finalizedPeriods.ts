// Months served from a frozen snapshot (public/data/snapshots, made by
// scripts/snapshot-period.mts) instead of re-processing synced CSVs at build
// time. Two kinds:
//  - Final: signed off by hand, with Client Performance Tracking sheet figures
//    (`sheet`) and AM notes. Marked "Final" in the selector; the client view
//    shows sheet revenue and leads.
//  - Snapshot only (no `sheet`): the platform sync's output frozen so the month
//    stays available on Netlify, where the sync does not run. Rendered like a
//    live month.
// The snapshots are committed on purpose (they hold guest names from the PMS
// exports); see .gitignore. Add a month here once its snapshot exists.

import type { ClientReportingFigures } from '@/components/september/septemberReportingSheetData';
import { SEPTEMBER_REPORTING_SHEET } from '@/components/september/septemberReportingSheetData';
import { SEPTEMBER_CLIENT_NOTES } from '@/components/september/septemberClientNotes';
import { AUGUST_REPORTING_SHEET } from '@/components/august/augustReportingSheetData';
import { CLIENT_REPORTING_SHEET as JULY_REPORTING_SHEET } from '@/components/july/clientReportingSheetData';

export interface FinalizedPeriod {
  id: string;
  label: string;
  /** Frozen ProcessedData snapshot, {period, data} shape (public/data/snapshots). */
  snapshot: string;
  /** Per-client "Direct Booking Revenue" + "New Leads" from the Client Performance Tracking sheet. Present only on signed-off months. */
  sheet?: Record<string, ClientReportingFigures>;
  /** Optional per-client AM notes shown above the summary cards. */
  notes?: Record<string, string>;
  /** When the month was signed off (Final) or frozen (snapshot only). */
  finalizedOn: string;
}

export const FINALIZED_PERIODS: FinalizedPeriod[] = [
  {
    id: 'september-2026',
    label: 'September 2026',
    snapshot: '/data/snapshots/september-2026.json',
    sheet: SEPTEMBER_REPORTING_SHEET,
    notes: SEPTEMBER_CLIENT_NOTES,
    finalizedOn: '2026-10-07',
  },
  {
    id: 'august-2026',
    label: 'August 2026',
    snapshot: '/data/snapshots/august-2026.json',
    sheet: AUGUST_REPORTING_SHEET,
    finalizedOn: '2026-09-03',
  },
  {
    id: 'july-2026',
    label: 'July 2026',
    snapshot: '/data/snapshots/july-2026.json',
    sheet: JULY_REPORTING_SHEET,
    finalizedOn: '2026-08-10',
  },
  // Snapshot-only months: platform sync output frozen on 2026-10-15.
  { id: 'june-2026', label: 'June 2026', snapshot: '/data/snapshots/june-2026.json', finalizedOn: '2026-10-15' },
  { id: 'may-2026', label: 'May 2026', snapshot: '/data/snapshots/may-2026.json', finalizedOn: '2026-10-15' },
  { id: 'april-2026', label: 'April 2026', snapshot: '/data/snapshots/april-2026.json', finalizedOn: '2026-10-15' },
  { id: 'march-2026', label: 'March 2026', snapshot: '/data/snapshots/march-2026.json', finalizedOn: '2026-10-15' },
  { id: 'february-2026', label: 'February 2026', snapshot: '/data/snapshots/february-2026.json', finalizedOn: '2026-10-15' },
];

/** True when the month carries sheet figures (signed off), not just a frozen sync. */
export function isFinal(p: FinalizedPeriod): boolean {
  return !!p.sheet;
}

const MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december'];

/** Sortable number for a period id like "september-2026" (bigger = more recent). */
export function periodSortKey(id: string): number {
  const m = id.match(/^([a-z]+)-(\d{4})$/);
  if (!m) return 0;
  return Number(m[2]) * 100 + (MONTHS.indexOf(m[1]) + 1);
}
