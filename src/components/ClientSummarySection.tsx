'use client';

import { ClientFacebookStats, PMSSummary, LeadAnalysis } from '@/types';
import { formatCurrency, formatNumber } from '@/lib/utils';

interface CampaignRevenue {
  followers: number;
  followersUses: number;
  retargeting: number;
  newLeads: number;
}

interface ClientSummarySectionProps {
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
    <div className="bg-white rounded-2xl border border-gray-100 shadow-[0_1px_4px_rgba(0,0,0,0.06)] px-6 py-5">
      <p className="text-xs font-semibold text-gray-400 uppercase tracking-widest mb-2">{label}</p>
      {value ? (
        <>
          <p className="text-3xl font-bold text-gray-900 tracking-tight">{value}</p>
          {sub && <p className="text-xs text-gray-400 mt-1">{sub}</p>}
        </>
      ) : (
        <p className="text-2xl font-bold text-gray-300">{placeholder ?? '—'}</p>
      )}
    </div>
  );
}

export default function ClientSummarySection({
  facebookStats,
  pmsSummary,
  campaignRevenue,
  instagramLeads,
  facebookLeads,
}: ClientSummarySectionProps) {
  const totalSpend =
    (facebookStats?.followers?.spend ?? 0) +
    (facebookStats?.retargeting?.spend ?? 0) +
    (facebookStats?.newLeads?.spend ?? 0);
  const hasSpend = totalSpend > 0;

  // Direct booking revenue = the platform's PMS direct-booking total. OTA
  // bookings (Airbnb/VRBO/Booking.com/…) are already excluded upstream by
  // roi-export, so every booking here is a direct booking.
  const directBookingRevenue = pmsSummary?.totalRevenue ?? 0;
  const bookingCount = pmsSummary?.directBookingCount ?? 0;
  const hasRevenue = !!pmsSummary && directBookingRevenue > 0;

  let revenueSub: string | undefined;
  if (hasRevenue && pmsSummary) {
    revenueSub =
      `${formatCurrency(pmsSummary.avgDirectBookingValue)} avg` +
      (pmsSummary.zeroRevenueCount > 0 ? ` · ${pmsSummary.zeroRevenueCount} $0 excluded` : '');
  }

  // Revenue attributed across all three Meta campaign types (Followers promo
  // attribution + Retargeting purchase events + New Leads matched bookings).
  const metaAttributedRevenue =
    campaignRevenue.followers + campaignRevenue.retargeting + campaignRevenue.newLeads;
  const hasMetaAttributedRevenue = metaAttributedRevenue > 0;

  // Bookings attributed to Meta — same per-campaign-type attribution logic used
  // in the Facebook Campaign Stats tabs: Followers via promo code, Retargeting
  // via FB purchase events, New Leads via matched PMS bookings.
  const metaAttributedBookings =
    campaignRevenue.followersUses +
    (facebookStats?.retargeting?.purchases ?? 0) +
    (facebookLeads?.matchCount ?? 0);
  const hasMetaAttributedBookings = metaAttributedBookings > 0;

  const costPerMetaBooking =
    hasSpend && hasMetaAttributedBookings ? totalSpend / metaAttributedBookings : null;

  // % of Booking Value = cost per Meta-attributed booking ÷ the client-wide avg
  // direct booking value (all sources, not just Meta) — how much of a typical
  // booking's value is spent acquiring a Meta-attributed one.
  const avgDirectBookingValue = pmsSummary?.avgDirectBookingValue ?? 0;
  const pctOfBookingValue =
    costPerMetaBooking !== null && avgDirectBookingValue > 0
      ? (costPerMetaBooking / avgDirectBookingValue) * 100
      : null;

  const metaRoas = hasSpend && hasMetaAttributedRevenue ? metaAttributedRevenue / totalSpend : null;

  const totalMetaLeads = facebookLeads?.totalGHLLeads ?? 0;
  const totalInstagramLeads = instagramLeads?.totalGHLLeads ?? 0;

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
          value={hasRevenue ? formatCurrency(directBookingRevenue) : undefined}
          sub={revenueSub}
          placeholder="No PMS data"
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
          sub={hasMetaAttributedBookings ? 'Followers + Retargeting + New Leads' : undefined}
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
          sub={hasMetaAttributedRevenue ? 'Followers + Retargeting + New Leads' : undefined}
          placeholder="No attribution data"
        />
        <SummaryCard
          label="ROAS"
          value={metaRoas !== null ? `${metaRoas.toFixed(2)}x` : undefined}
          sub={metaRoas !== null ? `${formatCurrency(metaAttributedRevenue)} Meta-attributed revenue ÷ ${formatCurrency(totalSpend)} spend` : undefined}
          placeholder="No data"
        />
      </div>

      {/* Row 4: GHL lead volume */}
      <div className="grid grid-cols-2 gap-4">
        <SummaryCard
          label="Meta Leads (from GHL)"
          value={totalMetaLeads > 0 ? formatNumber(totalMetaLeads) : undefined}
          sub={totalMetaLeads > 0 ? 'Facebook/Meta-tagged leads in GHL' : undefined}
          placeholder="No GHL data"
        />
        <SummaryCard
          label="Instagram Leads (from GHL)"
          value={totalInstagramLeads > 0 ? formatNumber(totalInstagramLeads) : undefined}
          sub={totalInstagramLeads > 0 ? 'Instagram-tagged leads in GHL' : undefined}
          placeholder="No GHL data"
        />
      </div>
    </div>
  );
}
