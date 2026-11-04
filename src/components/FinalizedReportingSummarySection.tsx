'use client';

import { ClientFacebookStats, PMSSummary, LeadAnalysis } from '@/types';
import { formatCurrency, formatNumber } from '@/lib/utils';
import type { FinalizedPeriod } from '@/lib/analysis/finalizedPeriods';
import type { ClientMonthMetrics } from '@/lib/analysis/clientMonthMetrics';

interface CampaignRevenue {
  followers: number;
  followersUses: number;
  retargeting: number;
  newLeads: number;
}

interface FinalizedReportingSummarySectionProps {
  clientName: string;
  period: FinalizedPeriod;
  facebookStats: ClientFacebookStats | null;
  pmsSummary: PMSSummary | null;
  campaignRevenue: CampaignRevenue;
  instagramLeads: LeadAnalysis | null;
  facebookLeads: LeadAnalysis | null;
  /** Oldest -> newest, last = this month; feeds the trend on each card. */
  history?: { period: FinalizedPeriod; metrics: ClientMonthMetrics | null }[];
}

type MetricKey = 'bookings' | 'directRevenue' | 'spend' | 'attributedBookings' | 'costPerAttributedBooking' | 'pctOfBookingValue' | 'attributedRevenue' | 'roas' | 'leads';

interface Trend {
  /** One per month, oldest -> newest; null where the month has no figure. */
  points: { label: string; value: number | null }[];
  /** Change vs the previous month, as a percentage; null when either side is missing. */
  deltaPct: number | null;
  prevLabel: string | null;
  /** A drop is the good direction (costs). */
  lowerIsBetter?: boolean;
}

function buildTrend(
  history: FinalizedReportingSummarySectionProps['history'],
  key: MetricKey,
  lowerIsBetter?: boolean,
): Trend | undefined {
  if (!history || history.length < 2) return undefined;
  const points = history.map(({ period, metrics }) => {
    const v = metrics ? metrics[key] : null;
    // Zero revenue, ROAS or cost means "nothing to show"; zero spend, bookings or leads is a real figure.
    const meaningful = v !== null && v !== undefined && (v !== 0 || key === 'spend' || key === 'bookings' || key === 'attributedBookings' || key === 'leads');
    return { label: period.label, value: meaningful ? v : null };
  });
  const current = points[points.length - 1];
  const prev = points[points.length - 2];
  const deltaPct =
    current.value !== null && prev.value !== null && prev.value !== 0
      ? ((current.value - prev.value) / Math.abs(prev.value)) * 100
      : null;
  return { points, deltaPct, prevLabel: prev.label, lowerIsBetter };
}

// Three-month sparkline: past months in the de-emphasis ink, this month's
// point in the brand accent. Months without a figure leave a gap.
function Sparkline({ points }: { points: Trend['points'] }) {
  const w = 72, h = 28, pad = 4;
  const values = points.map((p) => p.value).filter((v): v is number => v !== null);
  if (values.length < 2) return null;
  const min = Math.min(...values), max = Math.max(...values);
  const range = max - min || Math.abs(max) || 1;
  const step = (w - pad * 2) / (points.length - 1);
  const xy = points.map((p, i) => ({
    x: pad + i * step,
    y: p.value === null ? null : pad + (h - pad * 2) * (1 - (p.value - min) / range),
    label: p.label,
    value: p.value,
  }));
  const segments: string[] = [];
  for (let i = 1; i < xy.length; i++) {
    const a = xy[i - 1], b = xy[i];
    if (a.y !== null && b.y !== null) segments.push(`M${a.x},${a.y} L${b.x},${b.y}`);
  }
  return (
    <svg width={w} height={h} viewBox={`0 0 ${w} ${h}`} aria-hidden="true" className="flex-shrink-0">
      {segments.map((d, i) => (
        <path key={i} d={d} fill="none" stroke="var(--muted-soft)" strokeWidth="2" strokeLinecap="round" />
      ))}
      {xy.map((p, i) =>
        p.y === null ? null : (
          <circle key={i} cx={p.x} cy={p.y} r={i === xy.length - 1 ? 3.5 : 2.5} fill={i === xy.length - 1 ? 'var(--brand)' : 'var(--surface)'} stroke={i === xy.length - 1 ? 'var(--brand)' : 'var(--muted-soft)'} strokeWidth="2">
            <title>{`${p.label}: ${p.value}`}</title>
          </circle>
        ),
      )}
    </svg>
  );
}

function DeltaLine({ trend }: { trend: Trend }) {
  if (trend.deltaPct === null) {
    return <p className="text-[11px] text-[var(--muted-soft)] mt-1.5">No prior-month figure to compare</p>;
  }
  if (Math.abs(trend.deltaPct) < 0.05) {
    return <p className="text-[11px] text-[var(--muted-soft)] mt-1.5">No change vs {trend.prevLabel}</p>;
  }
  const up = trend.deltaPct > 0;
  const good = trend.lowerIsBetter ? !up : up;
  return (
    <p className={`text-[11px] font-semibold mt-1.5 july-tabular ${good ? 'text-[var(--success-ink)]' : 'text-[var(--danger)]'}`}>
      {up ? '▲' : '▼'} {Math.abs(trend.deltaPct).toFixed(1)}% vs {trend.prevLabel}
    </p>
  );
}

function SummaryCard({
  label,
  value,
  sub,
  placeholder,
  trend,
}: {
  label: string;
  value?: string;
  sub?: string;
  placeholder?: string;
  trend?: Trend;
}) {
  const months = trend ? trend.points.map((p) => `${p.label}: ${p.value === null ? '—' : p.value}`).join(' · ') : '';
  return (
    <div className="bg-[var(--surface)] rounded-[12px] border border-[var(--border)] shadow-[var(--shadow-xs)] px-6 py-6">
      <p className="text-[12px] font-semibold text-[var(--muted)] uppercase tracking-[0.04em] mb-2">{label}</p>
      {value ? (
        <>
          <div className="flex items-end justify-between gap-3">
            <p className="text-[26px] font-semibold text-[var(--foreground)] tracking-[-0.01em] leading-[1.15] july-tabular">{value}</p>
            {trend && (
              <span title={`Last ${trend.points.length} months · ${months}`}>
                <Sparkline points={trend.points} />
              </span>
            )}
          </div>
          {sub && <p className="text-[12px] text-[var(--muted-soft)] mt-1.5">{sub}</p>}
          {trend && <DeltaLine trend={trend} />}
        </>
      ) : (
        <p className="text-[20px] font-bold text-[var(--muted-soft)]">{placeholder ?? '—'}</p>
      )}
    </div>
  );
}

// Summary cards for a finalized month, rendered on the main dashboard when the
// selected period has a frozen snapshot. Differences from ClientSummarySection:
// - Total Direct Booking Revenue comes from the Client Performance Tracking
//   sheet's row for that month (period.sheet); clients absent from the sheet
//   fall back to the snapshot's PMS total with a note saying so.
// - The GHL lead cards are replaced by one "Total Leads" card from the sheet.
// - An optional AM note (period.notes) sits above the cards.
// Every other metric is computed from the snapshot exactly as before.
export default function FinalizedReportingSummarySection({
  clientName,
  period,
  facebookStats,
  pmsSummary,
  campaignRevenue,
  facebookLeads,
  history,
}: FinalizedReportingSummarySectionProps) {
  // Only signed-off months carry sheet figures; snapshot-only months never reach this component.
  const sheetFigures = period.sheet?.[clientName];

  const totalSpend =
    (facebookStats?.followers?.spend ?? 0) +
    (facebookStats?.retargeting?.spend ?? 0) +
    (facebookStats?.newLeads?.spend ?? 0);
  const hasSpend = totalSpend > 0;

  // Snapshot values still drive every derived metric (caps, ROAS, % of
  // booking value) so those stay identical to /july; only the two displayed
  // figures below swap to the reporting sheet.
  const snapshotRevenue = pmsSummary?.totalRevenue ?? 0;
  const bookingCount = pmsSummary?.directBookingCount ?? 0;
  const hasSnapshotRevenue = !!pmsSummary && snapshotRevenue > 0;

  // A zero in the sheet means the revenue cell isn't filled yet — fall back to
  // the AM booking-sheet total but keep the sheet's lead count.
  const sheetRevenue = sheetFigures && sheetFigures.directBookingRevenue > 0
    ? sheetFigures.directBookingRevenue
    : null;
  const displayRevenue = sheetRevenue ?? snapshotRevenue;
  const hasDisplayRevenue = sheetRevenue !== null ? true : hasSnapshotRevenue;
  const revenueSub = sheetRevenue !== null
    ? `From client reporting sheet · ${period.label}`
    : `AM booking sheet total — no ${period.label} revenue in the client reporting sheet yet`;

  // Cap Meta-attributed revenue at the revenue figure THIS page displays
  // (the reporting-sheet value when present), not the snapshot total —
  // otherwise "attributed" could exceed the total shown right above it
  // whenever the sheet's figure is lower than the snapshot's.
  const capRevenue = hasDisplayRevenue ? displayRevenue : (hasSnapshotRevenue ? snapshotRevenue : 0);
  // A campaign type only contributes to the blended Meta-attribution figures
  // if it actually ran this period (has spend) — e.g. promo-code revenue does
  // not count when no Followers campaign ran (per Shawal, Aug 2026).
  const followersRan = (facebookStats?.followers?.spend ?? 0) > 0;
  const retargetingRan = (facebookStats?.retargeting?.spend ?? 0) > 0;
  const newLeadsRan = (facebookStats?.newLeads?.spend ?? 0) > 0;
  const metaAttributedRevenueRaw =
    (followersRan ? campaignRevenue.followers : 0) +
    (retargetingRan ? campaignRevenue.retargeting : 0) +
    (newLeadsRan ? campaignRevenue.newLeads : 0);
  const metaAttributedRevenue = capRevenue > 0
    ? Math.min(metaAttributedRevenueRaw, capRevenue)
    : metaAttributedRevenueRaw;
  const hasMetaAttributedRevenue = metaAttributedRevenue > 0;

  const metaAttributedBookingsRaw =
    (followersRan ? campaignRevenue.followersUses : 0) +
    (retargetingRan ? facebookStats?.retargeting?.purchases ?? 0 : 0) +
    (newLeadsRan ? facebookLeads?.matchCount ?? 0 : 0);
  const metaAttributedBookings = bookingCount > 0
    ? Math.min(metaAttributedBookingsRaw, bookingCount)
    : metaAttributedBookingsRaw;
  const hasMetaAttributedBookings = metaAttributedBookings > 0;

  const costPerMetaBooking =
    hasSpend && hasMetaAttributedBookings ? totalSpend / metaAttributedBookings : null;

  // spend ÷ actual ad-attributed revenue — same formula as the per-campaign
  // "% of Booking Value" cards, so the two levels agree (per review, Oct 2026)
  const pctOfBookingValue =
    totalSpend > 0 && metaAttributedRevenue > 0
      ? (totalSpend / metaAttributedRevenue) * 100
      : null;

  const metaRoas = hasSpend && hasMetaAttributedRevenue ? metaAttributedRevenue / totalSpend : null;

  const totalLeads = sheetFigures?.newLeads ?? null;

  const note = period.notes?.[clientName];
  const trend = (key: MetricKey, lowerIsBetter?: boolean) => buildTrend(history, key, lowerIsBetter);

  return (
    <div className="space-y-4">
      {note && (
        <div className="bg-[var(--fill-blue)] border border-[var(--brand-border)] rounded-[12px] px-5 py-3.5">
          <p className="text-[11px] font-semibold text-[var(--brand)] uppercase tracking-[0.04em] mb-1">Note</p>
          <p className="text-[13px] text-[var(--foreground)] leading-relaxed">{note}</p>
        </div>
      )}
      {/* Row 1: overall direct booking totals */}
      <div className="grid grid-cols-2 gap-4">
        <SummaryCard
          label="Total Direct Bookings"
          value={bookingCount > 0 ? formatNumber(bookingCount) : undefined}
          sub={bookingCount > 0 ? 'All sources' : undefined}
          placeholder="No PMS data"
          trend={trend('bookings')}
        />
        <SummaryCard
          label="Total Direct Booking Revenue"
          value={hasDisplayRevenue ? formatCurrency(displayRevenue) : undefined}
          sub={hasDisplayRevenue ? revenueSub : undefined}
          placeholder="No revenue data"
          trend={trend('directRevenue')}
        />
      </div>

      {/* Row 2: Meta ad spend + attribution */}
      <div className="grid grid-cols-3 gap-4">
        <SummaryCard
          label="Overall Spend"
          value={hasSpend ? formatCurrency(totalSpend) : undefined}
          sub={hasSpend ? 'All campaign types combined' : undefined}
          placeholder="No ad data"
          trend={trend('spend', true)}
        />
        <SummaryCard
          label="Total Direct Bookings Attributed to Meta"
          value={hasMetaAttributedBookings ? formatNumber(metaAttributedBookings) : undefined}
          sub={hasMetaAttributedBookings ? (metaAttributedBookingsRaw > metaAttributedBookings ? 'Followers + Retargeting + New Leads · capped at total bookings' : 'Followers + Retargeting + New Leads') : undefined}
          placeholder="No attribution data"
          trend={trend('attributedBookings')}
        />
        <SummaryCard
          label="Cost per Total Direct Bookings Attributed to Meta"
          value={costPerMetaBooking !== null ? formatCurrency(costPerMetaBooking) : undefined}
          sub={costPerMetaBooking !== null ? `${formatCurrency(totalSpend)} ÷ ${metaAttributedBookings} booking${metaAttributedBookings !== 1 ? 's' : ''}` : undefined}
          placeholder="No data"
          trend={trend('costPerAttributedBooking', true)}
        />
      </div>

      {/* Row 3: Meta ad efficiency + revenue */}
      <div className="grid grid-cols-3 gap-4">
        <SummaryCard
          label="% of Booking Value"
          value={pctOfBookingValue !== null ? `${pctOfBookingValue.toFixed(1)}%` : undefined}
          sub={pctOfBookingValue !== null ? `${formatCurrency(totalSpend)} spend ÷ ${formatCurrency(metaAttributedRevenue)} Meta-attributed revenue` : undefined}
          placeholder="No data"
          trend={trend('pctOfBookingValue', true)}
        />
        <SummaryCard
          label="Direct Booking Revenue (Attributed to Meta Ads)"
          value={hasMetaAttributedRevenue ? formatCurrency(metaAttributedRevenue) : undefined}
          sub={hasMetaAttributedRevenue ? (metaAttributedRevenueRaw > metaAttributedRevenue ? 'Followers + Retargeting + New Leads · capped at total revenue' : 'Followers + Retargeting + New Leads') : undefined}
          placeholder="No attribution data"
          trend={trend('attributedRevenue')}
        />
        <SummaryCard
          label="Blended ROAS"
          value={metaRoas !== null ? `${metaRoas.toFixed(2)}x` : undefined}
          sub={metaRoas !== null ? `${formatCurrency(metaAttributedRevenue)} Meta-attributed revenue ÷ ${formatCurrency(totalSpend)} spend` : undefined}
          placeholder="No data"
          trend={trend('roas')}
        />
      </div>

      {/* Cap note: Meta-attributed revenue cannot exceed the month's direct
          booking revenue. When the three buckets add up to more than that
          (a promo-code guest is often also counted by Meta as a retargeting
          purchase), the attributed figure equals the total and this explains
          why the two cards above match. */}
      {hasMetaAttributedRevenue && metaAttributedRevenueRaw > metaAttributedRevenue && (
        <div className="bg-[var(--fill-blue)] border border-[var(--brand-border)] rounded-[12px] px-5 py-3.5">
          <p className="text-[11px] font-semibold text-[var(--brand)] uppercase tracking-[0.04em] mb-1">Why attributed revenue equals total direct revenue</p>
          <p className="text-[13px] text-[var(--foreground)] leading-relaxed">
            Promo-code bookings ({formatCurrency(followersRan ? campaignRevenue.followers : 0)}), Meta-reported retargeting purchases ({formatCurrency(retargetingRan ? campaignRevenue.retargeting : 0)}) and lead-form bookings ({formatCurrency(newLeadsRan ? campaignRevenue.newLeads : 0)}) add up to {formatCurrency(metaAttributedRevenueRaw)}, more than the {formatCurrency(capRevenue)} of direct booking revenue in {period.label}. The buckets overlap (a guest who used a promo code can also be counted by Meta as a retargeting purchase), so Meta-attributed revenue is capped at 100% of direct revenue and the ROAS uses the capped figure.
          </p>
        </div>
      )}

      {/* Row 4: combined leads from the client reporting sheet */}
      <div className="grid grid-cols-1 gap-4">
        <SummaryCard
          label="Total Leads"
          value={totalLeads !== null && totalLeads > 0 ? formatNumber(totalLeads) : undefined}
          sub={totalLeads !== null && totalLeads > 0 ? `New leads in ${period.label} · from client reporting sheet` : undefined}
          placeholder="Not listed in the client reporting sheet"
          trend={trend('leads')}
        />
      </div>
    </div>
  );
}
