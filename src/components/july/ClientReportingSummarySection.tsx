'use client';

import { ClientFacebookStats, PMSSummary, LeadAnalysis } from '@/types';
import { formatCurrency, formatNumber } from '@/lib/utils';
import { CLIENT_REPORTING_SHEET } from './clientReportingSheetData';

interface CampaignRevenue {
  followers: number;
  followersUses: number;
  retargeting: number;
  newLeads: number;
}

interface ClientReportingSummarySectionProps {
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
//   sheet's July 2026 row (clientReportingSheetData), not the snapshot's PMS
//   total; clients absent from that sheet fall back to the snapshot value
//   with a note saying so.
// - The two GHL lead cards (Meta / Instagram) are replaced by one combined
//   "Total Leads" card sourced from the same sheet's "New Leads" column.
// Every other metric is computed exactly as on /july, from the snapshot.
export default function ClientReportingSummarySection({
  clientName,
  facebookStats,
  pmsSummary,
  campaignRevenue,
  instagramLeads: _instagramLeads,
  facebookLeads,
}: ClientReportingSummarySectionProps) {
  const sheetFigures = CLIENT_REPORTING_SHEET[clientName];

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

  const displayRevenue = sheetFigures ? sheetFigures.directBookingRevenue : snapshotRevenue;
  const hasDisplayRevenue = sheetFigures ? displayRevenue > 0 : hasSnapshotRevenue;
  const revenueSub = sheetFigures
    ? 'From client reporting sheet · July 2026'
    : 'Not listed in the client reporting sheet — showing dashboard value';

  // Cap Meta-attributed revenue at the revenue figure THIS page displays
  // (the reporting-sheet value when present), not the snapshot total —
  // otherwise "attributed" could exceed the total shown right above it
  // whenever the sheet's figure is lower than the snapshot's.
  const capRevenue = hasDisplayRevenue ? displayRevenue : (hasSnapshotRevenue ? snapshotRevenue : 0);
  const metaAttributedRevenueRaw =
    campaignRevenue.followers + campaignRevenue.retargeting + campaignRevenue.newLeads;
  const metaAttributedRevenue = capRevenue > 0
    ? Math.min(metaAttributedRevenueRaw, capRevenue)
    : metaAttributedRevenueRaw;
  const hasMetaAttributedRevenue = metaAttributedRevenue > 0;

  const metaAttributedBookingsRaw =
    campaignRevenue.followersUses +
    (facebookStats?.retargeting?.purchases ?? 0) +
    (facebookLeads?.matchCount ?? 0);
  const metaAttributedBookings = bookingCount > 0
    ? Math.min(metaAttributedBookingsRaw, bookingCount)
    : metaAttributedBookingsRaw;
  const hasMetaAttributedBookings = metaAttributedBookings > 0;

  const costPerMetaBooking =
    hasSpend && hasMetaAttributedBookings ? totalSpend / metaAttributedBookings : null;

  const avgDirectBookingValue = pmsSummary?.avgDirectBookingValue ?? 0;
  const pctOfBookingValue =
    costPerMetaBooking !== null && avgDirectBookingValue > 0
      ? (costPerMetaBooking / avgDirectBookingValue) * 100
      : null;

  const metaRoas = hasSpend && hasMetaAttributedRevenue ? metaAttributedRevenue / totalSpend : null;

  const totalLeads = sheetFigures?.newLeads ?? null;

  return (
    <div className="space-y-4">
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
          sub={pctOfBookingValue !== null ? `Cost per Meta booking ÷ ${formatCurrency(avgDirectBookingValue)} avg booking value` : undefined}
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
          sub={totalLeads !== null && totalLeads > 0 ? 'New leads in July 2026 · from client reporting sheet' : undefined}
          placeholder="Not listed in the client reporting sheet"
        />
      </div>
    </div>
  );
}
