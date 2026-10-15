// Months whose numbers were finalized by hand (frozen snapshot + Client
// Performance Tracking sheet figures + AM notes). The main dashboard lists
// these ahead of the live-synced periods and renders them from the snapshot
// instead of re-processing the synced CSVs, so the figures match what was
// reported to clients. Add a month here once its snapshot is frozen
// (scripts/snapshot-period.mts) and its sheet figures are pulled.

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
  /** Per-client "Direct Booking Revenue" + "New Leads" from the Client Performance Tracking sheet. */
  sheet: Record<string, ClientReportingFigures>;
  /** Optional per-client AM notes shown above the summary cards. */
  notes?: Record<string, string>;
  /** When the month was signed off, for the badge tooltip. */
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
];

const MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december'];

/** Sortable number for a period id like "september-2026" (bigger = more recent). */
export function periodSortKey(id: string): number {
  const m = id.match(/^([a-z]+)-(\d{4})$/);
  if (!m) return 0;
  return Number(m[2]) * 100 + (MONTHS.indexOf(m[1]) + 1);
}
