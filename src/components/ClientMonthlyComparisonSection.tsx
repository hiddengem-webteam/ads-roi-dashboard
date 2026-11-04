'use client';

import { useMemo } from 'react';
import { Loader2 } from 'lucide-react';
import type { ProcessedData } from '@/types';
import type { FinalizedPeriod } from '@/lib/analysis/finalizedPeriods';
import { isFinal, periodSortKey } from '@/lib/analysis/finalizedPeriods';
import { computeClientMonthMetrics, type ClientMonthMetrics } from '@/lib/analysis/clientMonthMetrics';
import { formatCurrency, formatNumber } from '@/lib/utils';

interface ClientMonthlyComparisonSectionProps {
  clientName: string;
  periods: FinalizedPeriod[];
  /** Loaded snapshots keyed by period id (the dashboard fetches the missing ones). */
  snapshots: Record<string, ProcessedData>;
  loading: boolean;
  currentPeriodId: string;
  onSelectPeriod: (periodId: string) => void;
}

type MetricKey = 'spend' | 'directRevenue' | 'attributedRevenue' | 'roas' | 'attributedBookings' | 'costPerAttributedBooking' | 'leads';

interface Column {
  key: MetricKey;
  label: string;
  format: (v: number) => string;
  /** When a drop is the good direction (cost per booking). */
  lowerIsBetter?: boolean;
}

const COLUMNS: Column[] = [
  { key: 'spend', label: 'Ad spend', format: formatCurrency },
  { key: 'directRevenue', label: 'Direct booking revenue', format: formatCurrency },
  { key: 'attributedRevenue', label: 'Meta-attributed revenue', format: formatCurrency },
  { key: 'roas', label: 'Blended ROAS', format: (v) => `${v.toFixed(2)}x` },
  { key: 'attributedBookings', label: 'Attributed bookings', format: formatNumber },
  { key: 'costPerAttributedBooking', label: 'Cost per attributed booking', format: formatCurrency, lowerIsBetter: true },
  { key: 'leads', label: 'New leads', format: formatNumber },
];

function Delta({ current, previous, lowerIsBetter }: { current: number | null; previous: number | null; lowerIsBetter?: boolean }) {
  if (current === null || previous === null || previous === 0) {
    return <span className="block text-[11px] text-[var(--muted-soft)] mt-0.5">—</span>;
  }
  const pct = ((current - previous) / Math.abs(previous)) * 100;
  if (Math.abs(pct) < 0.05) {
    return <span className="block text-[11px] text-[var(--muted-soft)] mt-0.5">no change</span>;
  }
  const good = lowerIsBetter ? pct < 0 : pct > 0;
  const sign = pct > 0 ? '+' : '−';
  return (
    <span className={`block text-[11px] font-semibold mt-0.5 ${good ? 'text-[var(--success-ink)]' : 'text-[var(--danger)]'}`}>
      {sign}{Math.abs(pct).toFixed(1)}% vs prior
    </span>
  );
}

// Month-by-month table for one client across every month that has a frozen
// snapshot. Each cell shows the month's figure and the change against the
// month before it (the next row down). Figures match the client view's
// summary cards for that month (see clientMonthMetrics.ts).
export default function ClientMonthlyComparisonSection({
  clientName,
  periods,
  snapshots,
  loading,
  currentPeriodId,
  onSelectPeriod,
}: ClientMonthlyComparisonSectionProps) {
  const rows = useMemo(() => {
    const sorted = [...periods].sort((a, b) => periodSortKey(b.id) - periodSortKey(a.id));
    const out: { period: FinalizedPeriod; metrics: ClientMonthMetrics }[] = [];
    for (const period of sorted) {
      const snap = snapshots[period.id];
      if (!snap) continue;
      const metrics = computeClientMonthMetrics(snap.clients[clientName], period);
      if (metrics) out.push({ period, metrics });
    }
    return out;
  }, [periods, snapshots, clientName]);

  const pending = periods.filter((p) => !snapshots[p.id]).length;
  const monthsWithoutSheet = rows.filter((r) => !isFinal(r.period)).length;

  return (
    <div className="space-y-4">
      <div className="bg-[var(--surface)] rounded-[12px] border border-[var(--border)] shadow-[var(--shadow-xs)] overflow-hidden">
        <div className="px-6 py-4 border-b border-[var(--border)] flex items-center justify-between gap-4">
          <div>
            <p className="text-[14px] font-bold text-[var(--foreground)]">Month by month · {clientName}</p>
            <p className="text-[12px] text-[var(--muted-soft)] mt-0.5">
              Each change is against the month below it. Click a month to open that month&apos;s client view.
            </p>
          </div>
          {loading && pending > 0 && (
            <span className="flex items-center gap-1.5 text-[12px] text-[var(--muted-soft)]">
              <Loader2 className="w-3.5 h-3.5 animate-spin" />
              Loading {pending} month{pending !== 1 ? 's' : ''}…
            </span>
          )}
        </div>

        {rows.length === 0 ? (
          <div className="px-6 py-12 text-center text-[13px] text-[var(--muted-soft)]">
            {loading ? 'Loading months…' : `No monthly data for ${clientName} yet.`}
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full text-[13px]">
              <thead>
                <tr className="bg-[var(--fill-gray)] border-b border-[var(--border)]">
                  <th className="px-6 py-3 text-left text-[11px] font-semibold text-[var(--muted)] uppercase tracking-[0.04em] whitespace-nowrap">Month</th>
                  {COLUMNS.map((c) => (
                    <th key={c.key} className="px-4 py-3 text-right text-[11px] font-semibold text-[var(--muted)] uppercase tracking-[0.04em] whitespace-nowrap">
                      {c.label}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-[var(--divider)]">
                {rows.map(({ period, metrics }, i) => {
                  const prev = rows[i + 1]?.metrics ?? null;
                  const isCurrent = period.id === currentPeriodId;
                  return (
                    <tr
                      key={period.id}
                      onClick={() => onSelectPeriod(period.id)}
                      className={`cursor-pointer transition-colors duration-150 hover:bg-[var(--fill-cool)] ${isCurrent ? 'bg-[var(--brand-bg)]' : 'bg-[var(--surface)]'}`}
                    >
                      <td className="px-6 py-3 whitespace-nowrap align-top">
                        <span className={`block font-semibold ${isCurrent ? 'text-[var(--brand-text)]' : 'text-[var(--foreground)]'}`}>{period.label}</span>
                        <span className="block text-[11px] text-[var(--muted-soft)] mt-0.5">
                          {isFinal(period) ? 'Final · sheet revenue' : 'Snapshot · AM booking sheet revenue'}
                        </span>
                      </td>
                      {COLUMNS.map((c) => {
                        const value = metrics[c.key];
                        const previous = prev ? prev[c.key] : null;
                        // Zero spend, bookings or leads is a real figure; zero revenue or a null ratio is "nothing to show".
                        const hasValue = value !== null && value !== undefined && (value !== 0 || c.key === 'spend' || c.key === 'attributedBookings' || c.key === 'leads');
                        return (
                          <td key={c.key} className="px-4 py-3 text-right align-top july-tabular whitespace-nowrap">
                            {hasValue ? (
                              <>
                                <span className="block font-semibold text-[var(--foreground)]">{c.format(value as number)}</span>
                                <Delta current={value as number} previous={previous as number | null} lowerIsBetter={c.lowerIsBetter} />
                              </>
                            ) : (
                              <span className="block text-[var(--muted-soft)]">—</span>
                            )}
                          </td>
                        );
                      })}
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>

      <div className="text-[12px] text-[var(--muted-soft)] leading-relaxed px-1">
        <p>
          Direct booking revenue is the Client Performance Tracking sheet figure on signed-off months and the AM booking-sheet or platform total on snapshot-only months.
          Meta-attributed revenue is promo-code bookings, Meta-reported retargeting purchases and lead-form bookings for campaigns that ran that month, capped at the direct booking revenue. New leads come from the sheet and are blank on months without sheet figures.
          {monthsWithoutSheet > 0 && ' Months marked Snapshot were frozen from the platform sync without a sheet pass.'}
        </p>
      </div>
    </div>
  );
}
