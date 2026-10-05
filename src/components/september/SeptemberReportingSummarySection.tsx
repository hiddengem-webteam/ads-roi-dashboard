'use client';

import { ClientFacebookStats, PMSSummary, LeadAnalysis } from '@/types';
import { formatCurrency, formatNumber } from '@/lib/utils';
import { SEPTEMBER_REPORTING_SHEET } from './septemberReportingSheetData';
import { SEPTEMBER_CLIENT_NOTES } from './septemberClientNotes';

interface CampaignRevenue {
  followers: number;
  followersUses: number;
  retargeting: number;
  newLeads: number;
}

interface AugustReportingSummarySectionProps {
  clientName: string;
  facebookStats: ClientFacebookStats | null;
  pmsSummary: PMSSummary | null;
  campaignRevenue: CampaignRevenue;
  instagramLeads: LeadAnalysis | null;
  facebookLeads: LeadAnalysis | null;
}

function SummaryCard({
  label,
  value,
  sub,
  placeholder,
}: {
  label: string;
  value?: string;
  sub?: string;
  placeholder?: string;
}) {
  return (
    <div className="bg-[var(--surface)] rounded-[20px] border border-[var(--border)] shadow-[0_8px_22px_rgba(15,23,42,.04)] px-6 py-6">
      <p className="text-[12px] font-semibold text-[var(--muted)] uppercase tracking-[0.04em] mb-2">{label}</p>
      {value ? (
        <>
          <p className="text-[28px] font-extrabold text-[var(--foreground)] tracking-[-0.01em] leading-[1.15] july-tabular">{value}</p>
          {sub && <p className="text-[12px] text-[var(--muted-soft)] mt-1.5">{sub}</p>}
        </>
      ) : (
        <p className="text-[20px] font-bold text-[var(--muted-soft)]">{placeholder ?? '—'}</p>
      )}
    </div>
  );
}

// Client-reporting variant of ClientSummarySection (used only on
// /july-client-reporting-sheet). Differences from the /july version:
// - Total Direct Booking Revenue comes from the Client Performance Tracking
//   sheet's September 2026 row (clientReportingSheetData), not the snapshot's PMS
//   total; clients absent from that sheet fall back to the snapshot value
//   with a note saying so.
// - The two GHL lead cards (Meta / Instagram) are replaced by one combined
//   "Total Leads" card sourced from the same sheet's "New Leads" column.
// Every other metric is computed exactly as on /july, from the snapshot.
export default function AugustReportingSummarySection({
  clientName,
  facebookStats,
  pmsSummary,
  campaignRevenue,
  instagramLeads: _instagramLeads,
  facebookLeads,
}: AugustReportingSummarySectionProps) {
  const sheetFigures = SEPTEMBER_REPORTING_SHEET[clientName];

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
    ? 'From client reporting sheet · September 2026'
    : 'AM booking sheet total — no September revenue in the client reporting sheet yet';

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

  const note = SEPTEMBER_CLIENT_NOTES[clientName];

  return (
    <div className="space-y-4">
      {note && (
        <div className="bg-[var(--fill-blue)] border border-[rgba(10,95,255,.18)] rounded-[14px] px-5 py-3.5">
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
        />
        <SummaryCard
          label="Total Direct Booking Revenue"
          value={hasDisplayRevenue ? formatCurrency(displayRevenue) : undefined}
          sub={hasDisplayRevenue ? revenueSub : undefined}
          placeholder="No revenue data"
        />
      </div>

      {/* Row 2: Meta ad spend + attribution */}
      <div className="grid grid-cols-3 gap-4">
        <SummaryCard
          label="Overall Spend"
          value={hasSpend ? formatCurrency(totalSpend) : undefined}
          sub={hasSpend ? 'All campaign types combined' : undefined}
          placeholder="No ad data"
        />
        <SummaryCard
          label="Total Direct Bookings Attributed to Meta"
          value={hasMetaAttributedBookings ? formatNumber(metaAttributedBookings) : undefined}
          sub={hasMetaAttributedBookings ? (metaAttributedBookingsRaw > metaAttributedBookings ? 'Followers + Retargeting + New Leads · capped at total bookings' : 'Followers + Retargeting + New Leads') : undefined}
          placeholder="No attribution data"
        />
        <SummaryCard
          label="Cost per Total Direct Bookings Attributed to Meta"
          value={costPerMetaBooking !== null ? formatCurrency(costPerMetaBooking) : undefined}
          sub={costPerMetaBooking !== null ? `${formatCurrency(totalSpend)} ÷ ${metaAttributedBookings} booking${metaAttributedBookings !== 1 ? 's' : ''}` : undefined}
          placeholder="No data"
        />
      </div>

      {/* Row 3: Meta ad efficiency + revenue */}
      <div className="grid grid-cols-3 gap-4">
        <SummaryCard
          label="% of Booking Value"
          value={pctOfBookingValue !== null ? `${pctOfBookingValue.toFixed(1)}%` : undefined}
          sub={pctOfBookingValue !== null ? `${formatCurrency(totalSpend)} spend ÷ ${formatCurrency(metaAttributedRevenue)} Meta-attributed revenue` : undefined}
          placeholder="No data"
        />
        <SummaryCard
          label="Direct Booking Revenue (Attributed to Meta Ads)"
          value={hasMetaAttributedRevenue ? formatCurrency(metaAttributedRevenue) : undefined}
          sub={hasMetaAttributedRevenue ? (metaAttributedRevenueRaw > metaAttributedRevenue ? 'Followers + Retargeting + New Leads · capped at total revenue' : 'Followers + Retargeting + New Leads') : undefined}
          placeholder="No attribution data"
        />
        <SummaryCard
          label="Blended ROAS"
          value={metaRoas !== null ? `${metaRoas.toFixed(2)}x` : undefined}
          sub={metaRoas !== null ? `${formatCurrency(metaAttributedRevenue)} Meta-attributed revenue ÷ ${formatCurrency(totalSpend)} spend` : undefined}
          placeholder="No data"
        />
      </div>

      {/* Row 4: combined leads from the client reporting sheet */}
      <div className="grid grid-cols-1 gap-4">
        <SummaryCard
          label="Total Leads"
          value={totalLeads !== null && totalLeads > 0 ? formatNumber(totalLeads) : undefined}
          sub={totalLeads !== null && totalLeads > 0 ? 'New leads in September 2026 · from client reporting sheet' : undefined}
          placeholder="Not listed in the client reporting sheet"
        />
      </div>
    </div>
  );
}
